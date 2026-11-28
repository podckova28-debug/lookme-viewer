# Cleopatra in the Food & Drinks (ketchup) format: white canvas, one picture per narration line,
# smooth sub-pixel push-in / pull-out on every still, short white flash between pictures. Music added by mix_music.py.
# Run from scratchpad/tts (narration in health_out/nap_pN/lNN_s0.wav).
import glob, os, sys, subprocess, json, numpy as np, soundfile as sf
from PIL import Image
D = "/home/user/lookme-viewer/history/cleopatra"; sys.path.insert(0, D)
from shots import SHOTS
SR, FPS, W, H = 24000, 30, 1920, 1080
WORK = "health_out/cleo_video"; os.makedirs(WORK + "/seg", exist_ok=True)
GAP_LINE, GAP_PART, TAIL = 0.22, 0.5, 1.5
ZOOM = float(os.environ.get("ZOOM", "0"))   # user: no zoom, it crops the drawings
SPEED = float(os.environ.get("SPEED", "1.05"))
PARTS = sorted({p for p, *_ in SHOTS})
CUE = {(p, l): k for k, (p, l, *_) in enumerate(SHOTS, 1)}

audio, t, cuts = [], 0.0, []
for p in PARTS:
    fs = sorted(glob.glob(f"health_out/cleo_p{p}/l*_s0.wav"))
    for i, f in enumerate(fs):
        if (p, i) in CUE: cuts.append((t, CUE[(p, i)]))
        w, sr = sf.read(f, dtype="float32"); assert sr == SR
        audio.append(w); t += len(w) / SR
        g = GAP_LINE if i < len(fs) - 1 else GAP_PART
        audio.append(np.zeros(int(g * SR), np.float32)); t += g
audio.append(np.zeros(int(TAIL * SR), np.float32)); t += TAIL
sf.write(f"{WORK}/narr_raw.wav", np.concatenate(audio), SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{WORK}/narr_raw.wav", "-af", f"atempo={SPEED},aresample=48000", f"{WORK}/narr.wav"], check=True)
total = t / SPEED; cuts = [(a / SPEED, k) for a, k in cuts]
json.dump({"total": total, "cuts": cuts}, open(f"{WORK}/timeline.json", "w"))

def segment(i, k, n):
    im = Image.open(f"{D}/frames/f{k:03d}.png").convert("RGB")
    sc = min(2 * W / im.width, 2 * H / im.height); im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    src = Image.new("RGB", (2 * W, 2 * H), "white"); src.paste(im, ((2 * W - im.width) // 2, (2 * H - im.height) // 2))
    out = f"{WORK}/seg/s{i:03d}.mp4"
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    fl = min(4, n // 4)
    for f in range(n):
        u = f / max(1, n - 1); u = u * u * (3 - 2 * u) * .35 + u * .65
        z = 1 + ZOOM * u if i % 2 == 0 else 1 + ZOOM * (1 - u)
        cw, ch = 2 * W / z, 2 * H / z; x0, y0 = (2 * W - cw) / 2, (2 * H - ch) / 2
        fr = src.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch))
        if f < fl: fr = Image.blend(Image.new("RGB", (W, H), "white"), fr, (f + 1) / (fl + 1))
        pr.stdin.write(fr.tobytes())
    pr.stdin.close(); pr.wait(); assert pr.returncode == 0

acc = 0
with open(f"{WORK}/seg/list.txt", "w") as fh:
    for i, (st, k) in enumerate(cuts):
        en = cuts[i + 1][0] if i + 1 < len(cuts) else total
        n = round(en * FPS) - acc; acc += n
        segment(i, k, n); fh.write(f"file 's{i:03d}.mp4'\n"); print("seg", i, k, round(n / FPS, 1), flush=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{WORK}/seg/list.txt", "-c", "copy", f"{WORK}/video_silent.mp4"], check=True)
print(f"DONE {total:.1f}s {len(cuts)} cuts", flush=True)
