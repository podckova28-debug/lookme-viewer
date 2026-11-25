# Joan of Arc episode edit: narration lines -> timeline, 157 storyboard frames cut at (part, line, frac),
# chapter cards before c01..c11, sound effects on key shots. Static frames, hard cuts, no zoom.
# Run from scratchpad/tts/cb (narration wavs in health_out/rasp_cNN/lNN_s0.wav).
# Output: work dir with narration_sfx.wav + video_silent.mp4; then mix_music.py adds the music bed.
import os, sys, glob, json, subprocess, numpy as np, soundfile as sf
from PIL import Image
H = "/home/user/lookme-viewer/history"
sys.path.insert(0, H); sys.path.insert(0, H + "/joan")
from shots import S
import chapter_card
from chapter_card import card, draw_text, _cover, best_spot
from captions import CAP
from captions import POS
if os.environ.get('FONT'): chapter_card.FONT = H + '/fonts/' + os.environ['FONT']

SR = 24000
FR = H + "/joan/frames"
WORK = os.environ.get("WORK", "health_out/joan_video")
os.makedirs(WORK + "/img", exist_ok=True)
SPEED = float(os.environ.get("SPEED", "1.1"))
GAP_LINE, GAP_PART, CARD = 0.22, 0.4, 1.7      # seconds (CARD = title card hold, narration silent)
PARTS = [f"c{i:02d}" for i in range(12)]
TITLES = {"c01": "The Garden", "c02": "The Captain", "c03": "The Crowd", "c04": "The Banner", "c05": "The Arrow",
          "c06": "The Crown", "c07": "The Wall", "c08": "The Tower", "c09": "The Question", "c10": "The Dress", "c11": "The River"}
# shot number (1-based) -> (sfx, offset s, peak)
SFX = {1: ("clock", 0.0, .12), 2: ("stamp", 0.2, .16), 7: ("footsteps", 0.0, .12), 9: ("horn", 0.0, .16),
       17: ("swords", 0.0, .18), 19: ("quill", 0.0, .14), 21: ("horn", 0.0, .14), 24: ("thunder", 0.0, .12),
       29: ("knock", 0.0, .14), 34: ("papers", 0.0, .1), 36: ("footsteps", 0.0, .12), 42: ("footsteps", 0.0, .12),
       46: ("quill", 0.0, .14), 48: ("stamp", 0.2, .18), 55: ("swords", 0.2, .14), 56: ("quill", 0.0, .14),
       65: ("horn", 0.0, .18), 66: ("swords", 0.0, .2), 69: ("whoosh", 0.0, .2), 72: ("swords", 0.0, .22),
       76: ("clock", 0.0, .1), 85: ("swords", 0.0, .22), 88: ("horn", 0.0, .14), 96: ("whoosh", 0.0, .2),
       100: ("stamp", 0.2, .18), 103: ("thunder", 0.0, .18), 106: ("knock", 0.0, .2), 107: ("swords", 0.0, .18),
       111: ("whoosh", 0.0, .18), 113: ("papers", 0.0, .14), 117: ("knock", 0.0, .14), 126: ("clock", 0.0, .1),
       128: ("knock", 0.0, .2), 135: ("quill", 0.0, .14), 137: ("knock", 0.0, .22), 144: ("stamp", 0.2, .2),
       149: ("waves", 0.0, .14), 151: ("swords", 0.0, .18), 154: ("papers", 0.0, .16)}

SFX = {} if os.environ.get("NOSFX", "1") == "1" else SFX   # sound effects off by default (user: they sound odd)
CARD_WHOOSH = os.environ.get("NOSFX", "1") != "1"
TAIL = 2.5   # seconds of hold after the last line

def load_sfx(name, peak):
    raw = subprocess.run(["ffmpeg", "-v", "quiet", "-i", (f"{H}/sfx/{name}.mp3" if os.path.exists(f"{H}/sfx/{name}.mp3") else f"{H}/../mythology/sfx/{name}.mp3"), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.float32).copy(); return a / (np.abs(a).max() + 1e-9) * peak

# 1) narration + line start times; cards occupy silent slots before each chapter
audio, t, lines, cards = [], 0.0, {}, []
for p in PARTS:
    if p in TITLES:
        cards.append((t, p)); audio.append(np.zeros(int(CARD * SR), np.float32)); t += CARD
    fs = sorted(glob.glob(f"health_out/joan_{p}/l*_s0.wav"))
    n_txt = len([l for l in open(f"{H}/joan/vo/{p}.txt") if l.strip()])
    assert len(fs) == n_txt, (p, len(fs), n_txt)
    for i, f in enumerate(fs):
        w, sr = sf.read(f, dtype="float32"); assert sr == SR
        lines[(p, i)] = (t, len(w) / SR)
        audio.append(w); t += len(w) / SR
        g = GAP_LINE if i < len(fs) - 1 else GAP_PART
        audio.append(np.zeros(int(g * SR), np.float32)); t += g
audio.append(np.zeros(int(TAIL * SR), np.float32)); t += TAIL
narr = np.concatenate(audio); narr *= 0.7 / np.abs(narr).max()
total = len(narr) / SR

# 2) shot cut times
cuts = []
for k, (p, l, frac, desc) in enumerate(S, 1):
    s0, d = lines[(p, l)]
    cuts.append((s0 + frac * d, f"{FR}/f{k:03d}.png", k))
CAP_Y = float(os.environ.get("CAP_Y", "0.13"))
for (tc, p) in cards:
    first = next(k for k, s in enumerate(S, 1) if s[0] == p)
    out = f"{WORK}/img/card_{p}.jpg"; card(f"{FR}/f{first:03d}.png", TITLES[p], out)
    cuts.append((tc, out, f"card_{p}"))
cuts.sort(key=lambda c: c[0])
assert cuts[0][0] < 0.01

# 3) sound effects under the narration (+ whoosh on every chapter card)
fx = np.zeros_like(narr)
def put(name, at, peak):
    a = load_sfx(name, peak); i = int(at * SR); j = min(len(fx), i + len(a)); fx[i:j] += a[:j - i]
for c in cuts:
    if isinstance(c[2], int) and c[2] in SFX:
        nm, off, pk = SFX[c[2]]; put(nm, c[0] + off, pk)
    elif isinstance(c[2], str) and CARD_WHOOSH:
        put("whoosh", max(0, c[0] - 0.15), .2)
mix = narr + fx
sf.write(f"{WORK}/narration_raw.wav", mix, SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{WORK}/narration_raw.wav", "-af", f"atempo={SPEED}", f"{WORK}/narration_sfx.wav"], check=True)
total /= SPEED
cuts = [(a / SPEED, b, c) for a, b, c in cuts]

# 4) frames -> 1920x1080 jpgs (cover + centre crop), concat-demuxer list with durations
def prep(src, tag=None):
    if src.startswith(WORK): return src
    out = f"{WORK}/img/{os.path.basename(src).rsplit('.', 1)[0]}.jpg"
    if not os.path.exists(out):
        im = _cover(src, 1920, 1080)
        if isinstance(tag, int) and tag in CAP:
            cx, cy, sz = POS.get(tag) or best_spot(im, CAP[tag])
            draw_text(im, CAP[tag], sz, cy, maxw=.9, cx=cx)
        im.convert("RGB").save(out, quality=93)
    return out
FPS = 30
with open(f"{WORK}/list.txt", "w") as fh:
    acc = 0
    for k, (st, src, tag) in enumerate(cuts):
        end = cuts[k + 1][0] if k + 1 < len(cuts) else total
        nf = round(end * FPS) - acc; acc += nf
        fh.write(f"file '{os.path.abspath(prep(src, tag))}'\nduration {nf / FPS:.6f}\n")
    fh.write(f"file '{os.path.abspath(prep(cuts[-1][1], cuts[-1][2]))}'\n")
json.dump({"total": total, "cuts": [(round(a, 2), str(c)) for a, b, c in cuts]}, open(f"{WORK}/timeline.json", "w"), indent=0)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{WORK}/list.txt",
                "-vf", f"fps={FPS},format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-tune", "stillimage",
                "-t", f"{total:.3f}", f"{WORK}/video_silent.mp4"], check=True)
lens = [cuts[k + 1][0] - cuts[k][0] for k in range(len(cuts) - 1)]
print(f"DONE total {total:.1f}s, {len(cuts)} cuts, avg {np.mean(lens):.2f}s, max {max(lens):.2f}s", flush=True)
