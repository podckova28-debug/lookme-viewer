import glob, os, subprocess, json, numpy as np, soundfile as sf

SR = 24000
OUT = "/home/user/lookme-viewer/drinks/mead"
FR = OUT + "/frames"
WORK = "health_out/mead_video_v4"
os.makedirs(WORK, exist_ok=True)
GAP_SENT = 0.22   # pause between sentences (faster pace)
GAP_PART = 0.5    # pause between parts
SPEED = float(os.environ.get("SPEED", "1.0"))

# part -> {sentence_index: frame_number}; a frame lasts until the next cue
CUES = {
 0: {0:1, 2:2, 3:3, 6:2, 9:54, 10:4, 11:5, 12:6, 13:55, 14:56, 16:57, 17:58, 18:59, 19:7},
 1: {0:7, 1:8, 2:9, 4:60, 6:10, 8:11, 9:12, 10:13, 11:14, 13:7, 14:61},
 2: {0:62, 1:15, 2:16, 3:63, 4:17, 5:18, 6:64, 7:19, 10:65, 12:20, 14:66},
 3: {0:67, 2:68, 3:69, 4:70, 5:21, 6:22, 7:23, 8:71},
 4: {0:24, 1:25, 4:26, 6:72, 7:27, 8:28, 9:73, 10:29, 12:30, 13:74, 14:30},
 5: {0:2, 1:31, 2:32, 3:33, 4:34, 5:35, 7:2, 10:36, 12:75},
 6: {0:37, 1:76, 2:38, 3:77, 4:78, 5:39, 7:79, 8:40, 9:6, 10:41},
 7: {0:42, 1:80, 3:43, 4:44, 5:81, 6:45, 8:82, 9:83, 11:46, 12:6, 13:84, 14:46},
 8: {0:53, 1:47, 2:48, 3:49, 5:50, 6:85, 7:86, 8:51, 9:87, 11:52},
}

# 1) build narration track and timeline
audio, t, timeline = [], 0.0, []
for p in range(9):
    fs = sorted(glob.glob(f"health_out/meadM_p{p}/l*_s0.wav"))
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

# 2) one clip per shot: slow push-in or pan on a white 1920x1080 canvas
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
final = OUT + "/mead_v4_1080p.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{WORK}/segs.txt",
                "-i", f"{WORK}/narration.wav",
                "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", final], check=True)
print("VIDEO DONE", final, flush=True)
