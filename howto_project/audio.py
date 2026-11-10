#!/usr/bin/env python3
# Build narration track, music bed with ducking, final mix and an .srt for YouTube.
import json, subprocess, re
ROOT = "/home/user/hw"
tl = json.load(open(f"{ROOT}/spec/timeline.json"))
script = json.load(open(f"{ROOT}/script.json"))
total = tl["total"]

def run(cmd): subprocess.run(cmd, check=True)

# 1) narration: each chapter VO delayed to its global start
inputs, flt = [], []
for i, (n, st) in enumerate(tl["vo"]):
    inputs += ["-i", f"{ROOT}/vo/v{n:02d}.mp3"]
    ms = int(round(st * 1000))
    flt.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms}[v{i}]")
mix = "".join(f"[v{i}]" for i in range(len(tl["vo"])))
flt.append(f"{mix}amix=inputs={len(tl['vo'])}:normalize=0:duration=longest,apad,atrim=0:{total:.3f}[vo]")
run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(flt), "-map", "[vo]", "-c:a", "pcm_s16le", f"{ROOT}/out/vo_full.wav"])

# 2) music bed: m1 | m2 | m3 at chapter boundaries with 3 s crossfades
segs = tl["segs"]; t = 0; bounds = {}
for name, d in segs:
    bounds[name] = t; t += d
b2 = bounds["ch06"]; b3 = bounds["ch12"]
XF = 3.0
flt = [
    f"[0:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{b2 + XF:.3f},afade=t=in:d=2[m1]",
    f"[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{b3 - b2 + XF:.3f}[m2]",
    f"[2:a]aresample=48000,aformat=channel_layouts=stereo,apad,atrim=0:{total - b3 + 1:.3f},afade=t=out:st={total - b3 - 4:.3f}:d=4.5[m3]",
    f"[m1][m2]acrossfade=d={XF}[m12]",
    f"[m12][m3]acrossfade=d={XF},atrim=0:{total:.3f},volume=0.30[bed]",
]
run(["ffmpeg", "-v", "error", "-y", "-i", f"{ROOT}/mus/m1.m4a", "-i", f"{ROOT}/mus/m2.m4a", "-i", f"{ROOT}/mus/m3.m4a",
     "-filter_complex", ";".join(flt), "-map", "[bed]", "-c:a", "pcm_s16le", f"{ROOT}/out/bed.wav"])

# 3) duck the bed under the voice and mix
run(["ffmpeg", "-v", "error", "-y", "-i", f"{ROOT}/out/vo_full.wav", "-i", f"{ROOT}/out/bed.wav", "-filter_complex",
     "[0:a]asplit=2[vo][sc];[1:a][sc]sidechaincompress=threshold=0.02:ratio=8:attack=30:release=600[bd];"
     "[vo][bd]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-15:TP=-1.5:LRA=9[a]",
     "-map", "[a]", "-ar", "48000", "-c:a", "aac", "-b:a", "256k", f"{ROOT}/out/mix.m4a"])

# 4) SRT from the script, timed through whisper word timestamps
words = {}
for line in open(f"{ROOT}/vo/wts.log"):
    if not line.startswith("v"): continue
    p = line.split(); n = int(p[0][1:])
    words[n] = [float(x.rsplit("@", 1)[1]) for x in p[1:]]
durs = {}
for n in range(1, 18):
    durs[n] = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                    f"{ROOT}/vo/v{n:02d}.mp3"], capture_output=True, text=True).stdout)
def fmt(s):
    h = int(s // 3600); m = int(s % 3600 // 60); sec = s % 60
    return f"{h:02d}:{m:02d}:{int(sec):02d},{int(round((sec - int(sec)) * 1000)) % 1000:03d}"
out = []; k = 1
vo_start = dict(tl["vo"])
for ch in script["chapters"]:
    n = ch["n"]; text = ch["text"]
    ws = words.get(n, []); st0 = vo_start[n]
    sw = text.split(); ns = len(sw); nw = max(1, len(ws))
    # caption chunks: split on sentence ends, then cap at ~9 words
    chunks, cur = [], []
    for w in sw:
        cur.append(w)
        if re.search(r"[.?!:]$", w) or len(cur) >= 9:
            chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    idx = 0
    for c in chunks:
        i0, i1 = idx, idx + len(c); idx = i1
        a = ws[min(nw - 1, round(i0 * nw / ns))] if ws else 0
        b = ws[min(nw - 1, round(i1 * nw / ns))] if (ws and i1 < ns) else durs[n]
        if b <= a: b = a + 1.2
        out.append(f"{k}\n{fmt(st0 + a)} --> {fmt(st0 + b - 0.05)}\n{' '.join(c)}\n"); k += 1
open(f"{ROOT}/out/howto.srt", "w").write("\n".join(out))
print("AUDIO_OK", total)
