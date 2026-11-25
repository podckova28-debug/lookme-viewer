# usage: mix_music.py video.mp4 narration.wav music.mp3 out.mp4
# Builds a seamless long music bed (copies joined with 3 s crossfades), sets it ~20 dB under the voice,
# Fix 2026-11-25: narration is padded with 5 s of silence before loudnorm — loudnorm used to swallow the last ~3 s (the final line).
# ducks it a further ~6 dB while the narrator speaks, fades in/out, and remuxes with the untouched video.
import sys, subprocess, json, math, os
video, narr, music, out = sys.argv[1:5]
dur = lambda f: float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],capture_output=True,text=True).stdout)
T, M = dur(narr), dur(music)
XF = 3.0
n = max(1, math.ceil((T + 5) / (M - XF)))
tmp = os.path.splitext(out)[0] + "_bed.wav"
inputs = sum([["-i", music] for _ in range(n)], [])
if n == 1:
    fc = "[0:a]anull[bed]"
else:
    fc, prev = "", "[0:a]"
    for k in range(1, n):
        lab = f"[x{k}]" if k < n - 1 else "[bed]"
        fc += f"{prev}[{k}:a]acrossfade=d={XF}:c1=tri:c2=tri{lab};"; prev = lab
    fc = fc.rstrip(";")
subprocess.run(["ffmpeg","-v","error","-y",*inputs,"-filter_complex",fc,"-map","[bed]","-ar","48000","-ac","2",tmp],check=True)
fc = (f"[1:a]apad=pad_dur=5,aresample=48000,loudnorm=I=-16:TP=-1.5:LRA=11,aformat=channel_layouts=stereo,asplit=2[v][key];"
      f"[2:a]atrim=0:{T+1.5:.2f},volume=-23dB,afade=t=in:d=1.5,afade=t=out:st={T-1.5:.2f}:d=3[m];"
      f"[m][key]sidechaincompress=threshold=0.03:ratio=4:attack=30:release=500:makeup=1[md];"
      f"[v][md]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89,apad[a]")
subprocess.run(["ffmpeg","-v","error","-y","-i",video,"-i",narr,"-i",tmp,"-filter_complex",fc,
                "-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","192k","-t",f"{dur(video):.3f}","-movflags","+faststart",out],check=True)
print("MIX DONE", out, round(T,1), "s, music copies", n)
