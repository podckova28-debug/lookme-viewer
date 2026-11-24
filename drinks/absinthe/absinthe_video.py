# Edit for "The ENTIRE History of Absinthe". Run from the TTS work dir (scratchpad/tts/cb).
# Same pipeline as rum_video.py, plus a slow push-in / pull-out on every still (motion = retention).
import glob, os, sys, subprocess, json, numpy as np, soundfile as sf
sys.path.insert(0, "/home/user/lookme-viewer/drinks/absinthe")
from shots import SHOTS, EXTRA

SR = 24000
OUT = "/home/user/lookme-viewer/drinks/absinthe"
FR = OUT + "/frames"
WORK = "health_out/abs_videoM"
os.makedirs(WORK, exist_ok=True)
GAP_SENT = 0.22
GAP_PART = 0.5
SPEED = float(os.environ.get("SPEED", "1.0"))
ZOOM = 0.06

CUES = {p: {} for p in range(9)}
for k, (p, l, d, n) in enumerate(SHOTS, 1):
    CUES[p][l] = k
for (p, l), k in EXTRA.items():
    assert l not in CUES[p], (p, l)
    CUES[p][l] = k

# 1) narration + timeline (take s0 unless a pick file names another seed)
PICK = {}
if os.path.exists(f"{OUT}/picks.txt"):
    for line in open(f"{OUT}/picks.txt"):
        if line.strip() and not line.startswith("#"):
            p, l, s = line.split(); PICK[(int(p), int(l))] = int(s)
audio, t, timeline, parts = [], 0.0, [], []
for p in range(9):
    fs = sorted(glob.glob(f"health_out/absM_p{p}/l*_s0.wav"))
    parts.append(t)
    for i, f in enumerate(fs):
        s = PICK.get((p, i), 0)
        if s: f = f.replace("_s0.wav", f"_s{s}.wav")
        if i in CUES[p]:
            timeline.append((t, CUES[p][i]))
        w, sr = sf.read(f, dtype="float32"); assert sr == SR
        audio.append(w); t += len(w) / SR
        g = GAP_SENT if i < len(fs) - 1 else GAP_PART
        audio.append(np.zeros(int(g * SR), np.float32)); t += g
sf.write(f"{WORK}/narration_raw.wav", np.concatenate(audio), SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{WORK}/narration_raw.wav", "-af", f"atempo={SPEED}", f"{WORK}/narration.wav"], check=True)
total = t / SPEED
timeline = [(a / SPEED, b) for a, b in timeline]
json.dump({"total": total, "timeline": timeline, "parts": [x / SPEED for x in parts]}, open(f"{WORK}/timeline.json", "w"), indent=1)
print("narration", round(total, 1), "s,", len(timeline), "shots", flush=True)

# 2) one clip per shot: white 1920x1080 canvas, slow zoom in (even shots) or out (odd shots)
FPS = 30
segs = []
for k, (start, frame) in enumerate(timeline):
    end = timeline[k + 1][0] if k + 1 < len(timeline) else total
    dur = end - start
    n = max(1, int(round(dur * FPS)))
    src = f"{FR}/f{frame:02d}.png"
    out = f"{WORK}/seg_{k:03d}.mp4"
    fd = min(0.12, dur / 4)
    z = f"1+{ZOOM}*on/{n}" if k % 2 == 0 else f"1+{ZOOM}-{ZOOM}*on/{n}"
    vf = (f"scale=3840:2160:force_original_aspect_ratio=decrease,pad=3840:2160:(ow-iw)/2:(oh-ih)/2:white,"
          f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s=1920x1080:fps={FPS},"
          f"fade=t=in:st=0:d={fd:.2f}:color=white,format=yuv420p")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", vf,
                    "-frames:v", str(n), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", out], check=True)
    segs.append(out)
    print("seg", k, frame, round(dur, 1), flush=True)

with open(f"{WORK}/segs.txt", "w") as fh:
    for s in segs:
        fh.write(f"file '{os.path.abspath(s)}'\n")

# 3) concat video + narration (loudness-normalised)
final = OUT + "/absinthe_v1_1080p.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{WORK}/segs.txt",
                "-i", f"{WORK}/narration.wav",
                "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", final], check=True)
print("VIDEO DONE", final, flush=True)
