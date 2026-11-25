# Tutankhamun full episode, the "living" edit (approved in the cold-open test):
#  every still has slow camera motion, chapter cards, year plate + age, round portrait insets, key-fact captions,
#  checked animated clips on a few shots, scene ambience (wind / tomb tone / chisel). Music bed added by mix_music.py.
# Run from scratchpad/tts (narration in health_out/tut_cNN/lNN_s0.wav). Output in $WORK.
import os, sys, glob, json, subprocess, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont
H = "/home/user/lookme-viewer/history"; T = H + "/tut"
sys.path.insert(0, H); sys.path.insert(0, T)
from shots import S
from chapter_card import _cover, draw_text, best_spot, card
from captions import CAP, YEAR, AGE, INSET, CLIP, held
SR, FPS, W, Hh = 24000, 30, 1920, 1080
SPEED = float(os.environ.get("SPEED", "1.1"))
WORK = os.environ.get("WORK", "health_out/tut_video"); os.makedirs(WORK + "/seg", exist_ok=True)
GAP_LINE, GAP_PART, CARD, TAIL = 0.22, 0.4, 1.7, 2.5
PARTS = [f"c{i:02d}" for i in range(12)]
TITLES = {"c01": "The Sun Disk", "c02": "The Crook", "c03": "The Stela", "c04": "The Cane", "c05": "The Chariot", "c06": "The Letter",
          "c07": "The Tomb", "c08": "The Chisel", "c09": "The Step", "c10": "The Mask", "c11": "The Mosquito"}
ONLY = os.environ.get("ONLY")   # e.g. "1-30": rebuild only these segments (patching), others are reused

def frame(k):
    d = S[k - 1][3]
    return f"{T}/frames/{d.split()[1]}.png" if d.startswith("REUSE") else (f"{T}/frames/f{k:03d}.png" if k <= 11 else f"{T}/ep/f{k:03d}.png")

# 1) narration timeline
audio, t, lines, cards = [], 0.0, {}, []
for p in PARTS:
    if p in TITLES:
        cards.append((t, p)); audio.append(np.zeros(int(CARD * SR), np.float32)); t += CARD
    fs = sorted(glob.glob(f"health_out/tut_{p}/l*_s0.wav"))
    n_txt = len([l for l in open(f"{T}/vo/{p}.txt") if l.strip()]); assert len(fs) == n_txt, (p, len(fs), n_txt)
    for i, f in enumerate(fs):
        w, sr = sf.read(f, dtype="float32"); assert sr == SR
        lines[(p, i)] = (t, len(w) / SR); audio += [w, np.zeros(int((GAP_LINE if i < len(fs) - 1 else GAP_PART) * SR), np.float32)]
        t += len(w) / SR + (GAP_LINE if i < len(fs) - 1 else GAP_PART)
audio.append(np.zeros(int(TAIL * SR), np.float32)); t += TAIL
narr = np.concatenate(audio); narr *= .7 / np.abs(narr).max()
sf.write(WORK + "/narr_raw.wav", narr, SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", WORK + "/narr_raw.wav", "-af", f"atempo={SPEED}", WORK + "/narr.wav"], check=True)
total = t / SPEED

# 2) cut list: shots + chapter cards
cuts = [((lines[(p, l)][0] + fr * lines[(p, l)][1]) / SPEED, k) for k, (p, l, fr, *_) in enumerate(S, 1)]
cuts += [(tc / SPEED, "card_" + p) for tc, p in cards]
cuts.sort(key=lambda c: c[0]); assert cuts[0][0] < .01
starts = [c[0] for c in cuts] + [total]

# 3) overlays
FONT = H + "/fonts/BebasNeue-Regular.ttf"
def overlay(k, base):
    L = Image.new("RGBA", (W, Hh), (0, 0, 0, 0))
    if not isinstance(k, int): return L
    yr, age = held(YEAR, k), held(AGE, k)
    if k in CAP:
        cx, cy, sz = best_spot(base, CAP[k])
        if cy > Hh / 2 and (yr and cx > W * .45 or k in INSET and cx < W * .55):   # never on the year plate / portrait
            cx, cy = W / 2, Hh * .12
        draw_text(L, CAP[k], sz, cy, maxw=.9, cx=cx)
    if yr:
        d = ImageDraw.Draw(L); f1 = ImageFont.truetype(FONT, 96); f2 = ImageFont.truetype(FONT, 58)
        w = max(d.textlength(yr, font=f1), d.textlength(age, font=f2) if age else 0) + 56
        h = 124 + (64 if age else 0); x0, y0 = W - 48 - w, Hh - 44 - h
        d.rounded_rectangle([x0, y0, x0 + w, y0 + h], 14, fill=(12, 12, 12, 215))
        d.rectangle([x0, y0 + h - 12, x0 + w, y0 + h], fill=(200, 30, 30, 255))
        d.text((x0 + 28, y0 + 58), yr, font=f1, fill="white", anchor="lm")
        if age: d.text((x0 + 28, y0 + 140), age, font=f2, fill=(255, 215, 120), anchor="lm")
    if k in INSET:
        who, name = INSET[k]
        p = Image.open(f"{T}/chars/inset_{who}.png").convert("RGB").resize((300, 300))
        m = Image.new("L", (300, 300), 0); ImageDraw.Draw(m).ellipse([0, 0, 299, 299], fill=255)
        ring = Image.new("RGBA", (316, 316), (0, 0, 0, 0)); ImageDraw.Draw(ring).ellipse([0, 0, 315, 315], fill=(255, 255, 255, 255))
        L.alpha_composite(ring, (60, Hh - 420)); L.paste(p, (68, Hh - 412), m)
        draw_text(L, name, 64, Hh - 70, cx=218, maxw=.3)
    return L

MOT = ["in", "r", "out", "l"]
def segment(i, k, dur):
    out = f"{WORK}/seg/s{i:03d}.mp4"; n = max(1, round(dur * FPS))
    if isinstance(k, str):
        p = k[5:]; first = next(j for j, s in enumerate(S, 1) if s[0] == p)
        img = f"{WORK}/seg/{k}.jpg"; card(frame(first), TITLES[p], img); mot = "in"
        base = None
    else:
        img = f"{WORK}/seg/b{k:03d}.png"; base = _cover(frame(k), W, Hh); base.convert("RGB").save(img); mot = MOT[k % 4]
    ov = f"{WORK}/seg/ov{i:03d}.png"; overlay(k, base).save(ov)
    if isinstance(k, int) and k in CLIP:
        src, _, lim = CLIP[k].partition(":"); src = f"{T}/frames/{src}"
        cd = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
        if lim: cd = min(cd, float(lim))
        vf = f"trim=0:{cd:.3f},setpts=PTS-STARTPTS,setpts={max(1.0, dur / cd):.4f}*PTS,scale={W}:{Hh}:force_original_aspect_ratio=increase,crop={W}:{Hh},fps={FPS}"
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", src, "-i", ov, "-filter_complex",
               f"[0:v]{vf}[v];[v][1:v]overlay=0:0,format=yuv420p,tpad=stop_mode=clone:stop_duration=30", "-frames:v", str(n)]
    else:
        z = {"in": "1+0.08*on/{n}", "out": "1.08-0.08*on/{n}", "l": "1.08", "r": "1.08"}[mot].format(n=n)
        x = {"in": "iw/2-(iw/zoom/2)", "out": "iw/2-(iw/zoom/2)", "l": "(iw-iw/zoom)*(1-on/{n})", "r": "(iw-iw/zoom)*on/{n}"}[mot].format(n=n)
        vf = f"scale=3840:2160,zoompan=z='{z}':x='{x}':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{Hh}:fps={FPS}"
        cmd = ["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", img, "-i", ov, "-filter_complex", f"[0:v]{vf}[v];[v][1:v]overlay=0:0,format=yuv420p", "-frames:v", str(n)]
    subprocess.run(cmd + ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-r", str(FPS), out], check=True)

rng = None
if ONLY: rng = set(int(x) for x in ONLY.split(",")) if "," in ONLY or "-" not in ONLY else set(range(int(ONLY.split("-")[0]), int(ONLY.split("-")[1]) + 1))
acc = 0; frames_at = []
for i, (st, k) in enumerate(cuts):
    n = round(starts[i + 1] * FPS) - acc; acc += n; frames_at.append(n)
    if rng is None or i in rng or not os.path.exists(f"{WORK}/seg/s{i:03d}.mp4"): segment(i, k, n / FPS)
    if i % 20 == 0: print("seg", i, "/", len(cuts), flush=True)
with open(f"{WORK}/seg/list.txt", "w") as fh:
    for i in range(len(cuts)): fh.write(f"file 's{i:03d}.mp4'\n")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{WORK}/seg/list.txt", "-c", "copy", f"{WORK}/video_silent.mp4"], check=True)

# 4) scene ambience under the narration (beds per run of consecutive shots of one kind + chisel hits)
LOC = {k: s[4] for k, s in enumerate(S, 1)}
def amb(k):
    if not isinstance(k, int): return None
    if k <= 2: return "desert_wind"
    if k <= 8: return "tomb_tone"
    l = LOC.get(k) or ""
    if l.startswith("TOMB"): return "tomb_tone"
    if l.startswith("VALLEY") or l in ("DESERT", "AMARNA_CITY"): return "desert_wind"
    return None
CHISEL = {3, 39, 50, 104, 110, 148}
runs, cur = [], None
for i, (st, k) in enumerate(cuts):
    a_ = amb(k)
    if cur and cur[0] == a_: cur[2] = starts[i + 1]
    else:
        if cur and cur[0]: runs.append(tuple(cur))
        cur = [a_, st, starts[i + 1]]
if cur and cur[0]: runs.append(tuple(cur))
VOL = {"desert_wind": .3, "tomb_tone": .5}
def bed(src, a, b, vol, fade=.8):
    return (f"amovie={src}:loop=0,atrim=0:{b - a:.2f},afade=t=in:d={fade},afade=t=out:st={max(0, b - a - fade):.2f}:d={fade},"
            f"volume={vol},adelay={int(a * 1000)}|{int(a * 1000)}")
parts = [bed(f"{T}/sfx/{n}.mp3", a, b, VOL[n]) for n, a, b in runs if b - a > 1]
parts += [bed(f"{T}/sfx/chisel.mp3", starts[i] + .2, min(starts[i + 1], starts[i] + 3), .22, .2) for i, (st, k) in enumerate(cuts) if k in CHISEL]
fc = ";".join(f"{p},aresample=48000,aformat=channel_layouts=mono[a{i}]" for i, p in enumerate(parts))
fc += f";[0:a]aresample=48000[n];[n]" + "".join(f"[a{i}]" for i in range(len(parts))) + f"amix=inputs={len(parts) + 1}:duration=first:normalize=0[o]"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", WORK + "/narr.wav", "-filter_complex", fc, "-map", "[o]", WORK + "/narration_sfx.wav"], check=True)
json.dump({"total": total, "cuts": [[round(s, 2), str(k)] for s, k in cuts], "ambience": runs}, open(f"{WORK}/timeline.json", "w"))
print(f"DONE {total:.1f}s, {len(cuts)} cuts, {len(runs)} ambience beds", flush=True)
