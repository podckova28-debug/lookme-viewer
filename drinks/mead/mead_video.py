import glob, os, subprocess, json, numpy as np, soundfile as sf

SR = 24000
OUT = "/home/user/lookme-viewer/drinks/mead"
FR = OUT + "/frames"
WORK = "health_out/mead_video"
os.makedirs(WORK, exist_ok=True)
GAP_SENT = 0.45   # pause between sentences
GAP_PART = 0.9    # pause between parts

# part -> {sentence_index: frame_number}; a frame lasts until the next cue
CUES = {
 0: {0:1, 2:2, 3:3, 6:2, 9:4, 11:5, 12:6, 14:7},
 1: {0:7, 1:8, 2:9, 6:10, 8:11, 9:12, 10:13, 11:14},
 2: {0:15, 2:16, 4:17, 5:18, 7:19, 12:20},
 3: {0:21, 6:22, 7:23},
 4: {0:24, 1:25, 4:26, 7:27, 8:28, 10:29, 12:30},
 5: {0:2, 1:31, 2:32, 3:33, 4:34, 5:35, 7:2, 10:36},
 6: {0:37, 2:38, 5:39, 8:40, 9:6, 10:41},
 7: {0:42, 3:43, 4:44, 6:45, 11:46},
 8: {0:53, 1:47, 2:48, 3:49, 5:50, 8:51, 9:49, 11:52},
}

# 1) build narration track and timeline
audio, t, timeline = [], 0.0, []
for p in range(9):
    fs = sorted(glob.glob(f"health_out/mead_p{p}/l*_s0.wav"))
    for i, f in enumerate(fs):
        if i in CUES[p]:
            timeline.append((t, CUES[p][i]))
        w, sr = sf.read(f, dtype="float32"); assert sr == SR
        audio.append(w); t += len(w) / SR
        g = GAP_SENT if i < len(fs) - 1 else GAP_PART
        audio.append(np.zeros(int(g * SR), np.float32)); t += g
total = t
sf.write(f"{WORK}/narration.wav", np.concatenate(audio), SR)
json.dump({"total": total, "timeline": timeline}, open(f"{WORK}/timeline.json", "w"), indent=1)
print("narration", round(total, 1), "s,", len(timeline), "shots")

# 2) one clip per shot: slow push-in or pan on a white 1920x1080 canvas
FPS = 30
segs = []
for k, (start, frame) in enumerate(timeline):
    end = timeline[k + 1][0] if k + 1 < len(timeline) else total
    dur = end - start
    n = max(1, int(round(dur * FPS)))
    src = f"{FR}/f{frame:02d}.png"
    mode = k % 3
    if mode == 0:   # push in to centre
        z = f"zoompan=z='1+0.08*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
    elif mode == 1: # slow pan left->right at 1.08
        z = f"zoompan=z='1.08':x='(iw-iw/zoom)*on/{n}':y='ih/2-(ih/zoom/2)'"
    else:           # pull out from 1.1
        z = f"zoompan=z='1.1-0.08*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
    out = f"{WORK}/seg_{k:03d}.mp4"
    vf = (f"scale=2400:1350:force_original_aspect_ratio=decrease,pad=2400:1350:(ow-iw)/2:(oh-ih)/2:white,"
          f"{z}:d={n}:s=1920x1080:fps={FPS},format=yuv420p")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", src, "-vf", vf,
                    "-frames:v", str(n), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", out], check=True)
    segs.append(out)
    print("seg", k, frame, round(dur, 1), flush=True)

with open(f"{WORK}/segs.txt", "w") as fh:
    for s in segs:
        fh.write(f"file '{os.path.abspath(s)}'\n")

# 3) concat video + narration (loudness-normalised), 1080p30 H.264 + AAC
final = OUT + "/mead_v1_1080p.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{WORK}/segs.txt",
                "-i", f"{WORK}/narration.wav",
                "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", final], check=True)
print("VIDEO DONE", final, flush=True)
