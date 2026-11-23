# Rasputin episode edit: narration lines -> timeline, 144 storyboard frames cut at (part, line, frac),
# chapter cards before c01..c11, sound effects on key shots. Static frames, hard cuts, no zoom.
# Run from scratchpad/tts/cb (narration wavs in health_out/rasp_cNN/lNN_s0.wav).
# Output: work dir with narration_sfx.wav + video_silent.mp4; then mix_music.py adds the music bed.
import os, sys, glob, json, subprocess, numpy as np, soundfile as sf
from PIL import Image
H = "/home/user/lookme-viewer/history"
sys.path.insert(0, H); sys.path.insert(0, H + "/rasputin")
from shots import S
from chapter_card import card

SR = 24000
FR = H + "/rasputin/frames"
WORK = os.environ.get("WORK", "health_out/rasp_video")
os.makedirs(WORK + "/img", exist_ok=True)
SPEED = float(os.environ.get("SPEED", "1.0"))
GAP_LINE, GAP_PART, CARD = 0.25, 0.45, 1.7      # seconds (CARD = title card hold, narration silent)
PARTS = [f"c{i:02d}" for i in range(12)]
TITLES = {"c01": "The Village", "c02": "The Road", "c03": "The Capital", "c04": "The Secret", "c05": "The Telegram",
          "c06": "The Knife", "c07": "The Throne Room", "c08": "The Cakes", "c09": "The Bridge", "c10": "The Letter",
          "c11": "The Song"}
# shot number (1-based) -> (sfx, offset s, peak)
SFX = {2: ("footsteps", 0.0, .16), 9: ("thunder", 0.2, .22), 10: ("typewriter", 0.0, .16), 24: ("match", 0.0, .18),
       37: ("typewriter", 0.0, .16), 59: ("typewriter", 0.0, .16), 63: ("papers", 0.0, .16), 65: ("quill", 0.0, .16),
       66: ("typewriter", 0.0, .14), 68: ("stamp", 0.3, .2), 75: ("typewriter", 0.0, .16), 79: ("whoosh", 0.1, .18),
       96: ("stamp", 0.2, .22), 103: ("clock", 0.0, .16), 106: ("quill", 0.0, .14), 110: ("footsteps", 0.0, .16),
       111: ("knock", 0.0, .3), 115: ("knock", 0.3, .3), 119: ("typewriter", 0.0, .14), 126: ("thunder", 0.0, .25),
       131: ("quill", 0.0, .14), 133: ("typewriter", 0.0, .16), 144: ("thunder", 0.3, .18)}

def load_sfx(name, peak):
    raw = subprocess.run(["ffmpeg", "-v", "quiet", "-i", f"{H}/sfx/{name}.mp3", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.float32).copy(); return a / (np.abs(a).max() + 1e-9) * peak

# 1) narration + line start times; cards occupy silent slots before each chapter
audio, t, lines, cards = [], 0.0, {}, []
for p in PARTS:
    if p in TITLES:
        cards.append((t, p)); audio.append(np.zeros(int(CARD * SR), np.float32)); t += CARD
    fs = sorted(glob.glob(f"health_out/rasp_{p}/l*_s0.wav"))
    n_txt = len([l for l in open(f"../hist/rasputin/{p}.txt") if l.strip()])
    assert len(fs) == n_txt, (p, len(fs), n_txt)
    for i, f in enumerate(fs):
        w, sr = sf.read(f, dtype="float32"); assert sr == SR
        lines[(p, i)] = (t, len(w) / SR)
        audio.append(w); t += len(w) / SR
        g = GAP_LINE if i < len(fs) - 1 else GAP_PART
        audio.append(np.zeros(int(g * SR), np.float32)); t += g
narr = np.concatenate(audio); narr *= 0.7 / np.abs(narr).max()
total = len(narr) / SR

# 2) shot cut times
cuts = []
for k, (p, l, frac, refs, desc) in enumerate(S, 1):
    s0, d = lines[(p, l)]
    cuts.append((s0 + frac * d, f"{FR}/f{k:03d}.png", k))
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
    elif isinstance(c[2], str):
        put("whoosh", max(0, c[0] - 0.15), .2)
mix = narr + fx
sf.write(f"{WORK}/narration_raw.wav", mix, SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{WORK}/narration_raw.wav", "-af", f"atempo={SPEED}", f"{WORK}/narration_sfx.wav"], check=True)
total /= SPEED
cuts = [(a / SPEED, b, c) for a, b, c in cuts]

# 4) frames -> 1920x1080 jpgs (cover + centre crop), concat-demuxer list with durations
def prep(src):
    out = f"{WORK}/img/{os.path.basename(src).rsplit('.', 1)[0]}.jpg"
    if src.startswith(WORK): return src
    if not os.path.exists(out):
        im = Image.open(src).convert("RGB"); sc = max(1920 / im.width, 1080 / im.height)
        im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
        l, tp = (im.width - 1920) // 2, (im.height - 1080) // 2
        im.crop((l, tp, l + 1920, tp + 1080)).save(out, quality=93)
    return out
FPS = 30
with open(f"{WORK}/list.txt", "w") as fh:
    acc = 0
    for k, (st, src, tag) in enumerate(cuts):
        end = cuts[k + 1][0] if k + 1 < len(cuts) else total
        nf = round(end * FPS) - acc; acc += nf
        fh.write(f"file '{os.path.abspath(prep(src))}'\nduration {nf / FPS:.6f}\n")
    fh.write(f"file '{os.path.abspath(prep(cuts[-1][1]))}'\n")
json.dump({"total": total, "cuts": [(round(a, 2), str(c)) for a, b, c in cuts]}, open(f"{WORK}/timeline.json", "w"), indent=0)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{WORK}/list.txt",
                "-vf", f"fps={FPS},format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-tune", "stillimage",
                "-t", f"{total:.3f}", f"{WORK}/video_silent.mp4"], check=True)
lens = [cuts[k + 1][0] - cuts[k][0] for k in range(len(cuts) - 1)]
print(f"DONE total {total:.1f}s, {len(cuts)} cuts, avg {np.mean(lens):.2f}s, max {max(lens):.2f}s", flush=True)
