import glob, os, sys, subprocess, json, numpy as np, soundfile as sf
sys.path.insert(0, "/home/user/lookme-viewer/drinks/rum")
from shots import SHOTS, EXTRA

SR = 24000
OUT = "/home/user/lookme-viewer/drinks/rum"
FR = OUT + "/frames"
WORK = "health_out/rum_videoM"
os.makedirs(WORK, exist_ok=True)
GAP_SENT = 0.22   # pause between sentences (faster pace than mead)
GAP_PART = 0.5    # pause between parts
SPEED = float(os.environ.get("SPEED", "1.0"))

# part -> {sentence_index: frame_number}; a frame lasts until the next cue
CUES = {p: {} for p in range(9)}
for k, (p, l, d, n) in enumerate(SHOTS, 1):
    CUES[p][l] = k
for (p, l), k in EXTRA.items():
    assert l not in CUES[p], (p, l)
    CUES[p][l] = k

# 1) build narration track and timeline
audio, t, timeline = [], 0.0, []
for p in range(9):
    fs = sorted(glob.glob(f"health_out/rumM_p{p}/l*_s0.wav"))
    for i, f in enumerate(fs):
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
json.dump({"total": total, "timeline": timeline}, open(f"{WORK}/timeline.json", "w"), indent=1)
print("narration", round(total, 1), "s,", len(timeline), "shots")

# 2) one clip per shot on a white 1920x1080 canvas (no zoom); animated clip if present
FPS = 30
segs = []
used_anim = set()
for k, (start, frame) in enumerate(timeline):
    end = timeline[k + 1][0] if k + 1 < len(timeline) else total
    dur = end - start
    n = max(1, int(round(dur * FPS)))
    src = f"{FR}/f{frame:02d}.png"
    out = f"{WORK}/seg_{k:03d}.mp4"
    fd = min(0.12, dur / 4)
    vf = (f"scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:white,"
          f"fps={FPS},fade=t=in:st=0:d={fd:.2f}:color=white,format=yuv420p")
    anim = f"{FR}/anim_up/f{frame:02d}.mp4"
    if not os.path.exists(anim): anim = f"{FR}/anim/f{frame:02d}.mp4"
    if os.path.exists(anim) and frame not in used_anim:
        used_anim.add(frame)
        avf = (f"scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:white,"
               f"fps={FPS},tpad=stop_mode=clone:stop_duration=60,fade=t=in:st=0:d={fd:.2f}:color=white,format=yuv420p")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", anim, "-vf", avf, "-an",
                        "-frames:v", str(n), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", out], check=True)
        segs.append(out); print("seg", k, frame, round(dur, 1), "ANIM", flush=True); continue
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", src, "-vf", vf,
                    "-frames:v", str(n), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-tune", "stillimage", out], check=True)
    segs.append(out)
    print("seg", k, frame, round(dur, 1), flush=True)

with open(f"{WORK}/segs.txt", "w") as fh:
    for s in segs:
        fh.write(f"file '{os.path.abspath(s)}'\n")

# 3) concat video + narration (loudness-normalised), 1080p30 H.264 + AAC
final = OUT + "/rum_v2_1080p.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{WORK}/segs.txt",
                "-i", f"{WORK}/narration.wav",
                "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", final], check=True)
print("VIDEO DONE", final, flush=True)
