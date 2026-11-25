# Tutankhamun cold-open test (~40 s): the new "living" edit.
#  - every still gets slow camera motion (push-in / pull-out / pan), never static
#  - key moments are short AI animations (kling turbo) instead of stills
#  - year counter in the corner, character name card (portrait inset) when a person is introduced
#  - ambience per scene (desert wind / tomb room tone) + one action sound (chisel), music swells on the reveal
# Run from scratchpad/tts (narration in health_out/tut_c00/lNN_s0.wav), output in health_out/tut_test/.
import os, sys, json, glob, subprocess, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter
H = "/home/user/lookme-viewer/history"; T = H + "/tut"
sys.path.insert(0, H)
from chapter_card import _cover, draw_text
SR, FPS, W, Hh = 24000, 30, 1920, 1080
SPEED = 1.1
OUT = "health_out/tut_test"; os.makedirs(OUT + "/seg", exist_ok=True)

# shot list: (frame, narration line, fraction, motion, caption, clip)
# motion: in = slow push-in, out = pull-out, l / r = pan, clip = use animated mp4 frames/clipNNN.mp4
SHOTS = [
 (1, 0, 0,  "in",  "VALLEY OF THE KINGS, EGYPT", None),
 (2, 1, 0,  "out", None, None),
 (3, 2, 0,  "r",   None, None),
 (4, 2, .55, "in", None, None),
 (5, 3, 0,  None,  None, "clip005.mp4"),
 (6, 4, 0,  "l",   "LORD CARNARVON", None),
 (7, 5, 0,  "in",  None, None),
 (8, 6, 0,  None,  None, "clip008.mp4"),
 (9, 7, 0,  "r",   "3,000 YEARS", None),
 (10, 8, 0, "out", None, None),
 (11, 9, 0, "in",  "TUTANKHAMUN", None),
]
YEAR = {0: "1922", 1: "1922", 2: "1922", 3: "1922", 4: "1922", 5: "1922", 6: "1922", 7: "1922", 9: "TODAY", 10: "1341-1323 BC"}   # per shot index
INSET = {3: ("carter", "HOWARD CARTER")}   # shot index (0-based) -> portrait inset

# 1) narration timeline
lines, t, audio = [], 0.0, []
for i, f in enumerate(sorted(glob.glob("health_out/tut_c00/l*_s0.wav"))):
    w, sr = sf.read(f, dtype="float32"); assert sr == SR
    lines.append((t, len(w) / SR)); audio += [w, np.zeros(int(.28 * SR), np.float32)]; t += len(w) / SR + .28
audio.append(np.zeros(int(2.0 * SR), np.float32)); t += 2.0
narr = np.concatenate(audio); narr *= .7 / np.abs(narr).max()
sf.write(OUT + "/narr_raw.wav", narr, SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", OUT + "/narr_raw.wav", "-af", f"atempo={SPEED}", OUT + "/narr.wav"], check=True)
total = t / SPEED
starts = [(lines[l][0] + fr * lines[l][1]) / SPEED for _, l, fr, *_ in SHOTS] + [total]

# 2) overlays (caption, year tag, inset) rendered on a transparent layer per shot
FONT = H + "/fonts/BebasNeue-Regular.ttf"
def overlay(k, cap):
    L = Image.new("RGBA", (W, Hh), (0, 0, 0, 0))
    if cap: draw_text(L, cap, 92, 120)
    yr = YEAR.get(k)
    if yr:
        # year plate: big, top-left, solid dark plate + red bar (brand), readable on any background and on a phone
        f = ImageFont.truetype(FONT, 96); d = ImageDraw.Draw(L)
        tw = d.textlength(yr, font=f); x0, y0 = W - 48 - (tw + 56), Hh - 44 - 124   # bottom-right, away from the title
        d.rounded_rectangle([x0, y0, x0 + tw + 56, y0 + 124], 14, fill=(12, 12, 12, 215))
        d.rectangle([x0, y0 + 112, x0 + tw + 56, y0 + 124], fill=(200, 30, 30, 255))
        d.text((x0 + 28, y0 + 58), yr, font=f, fill="white", anchor="lm")
    if k in INSET:
        who, name = INSET[k]
        p = Image.open(f"{T}/chars/{who}.png").convert("RGB"); cw = int(p.width * .34); x0 = int(p.width * .5 - cw * .55); y0 = int(p.height * .02); p = p.crop((x0, y0, x0 + cw, y0 + cw))
        p = p.resize((300, 300)); m = Image.new("L", (300, 300), 0); ImageDraw.Draw(m).ellipse([0, 0, 299, 299], fill=255)
        ring = Image.new("RGBA", (316, 316), (0, 0, 0, 0)); ImageDraw.Draw(ring).ellipse([0, 0, 315, 315], fill=(255, 255, 255, 255))
        L.alpha_composite(ring, (60, Hh - 420)); L.paste(p, (68, Hh - 412), m)
        draw_text(L, name, 64, Hh - 70, cx=218, maxw=.3)
    L.save(f"{OUT}/seg/ov{k:02d}.png")

# 3) one mp4 segment per shot
for k, (fr, l, frac, mot, cap, clip) in enumerate(SHOTS):
    dur = starts[k + 1] - starts[k]; n = max(1, round(dur * FPS)); overlay(k, cap)
    out = f"{OUT}/seg/s{k:02d}.mp4"
    if clip:   # animated clip, slowed/held to fit the slot
        src = f"{T}/frames/{clip}"
        cd = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
        pts = max(1.0, dur / cd)
        vf = f"setpts={pts:.4f}*PTS,scale={W}:{Hh}:force_original_aspect_ratio=increase,crop={W}:{Hh},fps={FPS}"
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", src, "-i", f"{OUT}/seg/ov{k:02d}.png", "-filter_complex",
               f"[0:v]{vf}[v];[v][1:v]overlay=0:0,format=yuv420p,tpad=stop_mode=clone:stop_duration=10", "-frames:v", str(n)]
    else:
        img = f"{OUT}/seg/b{k:02d}.png"; _cover(f"{T}/frames/f{fr:03d}.png", W, Hh).convert("RGB").save(img)
        z = {"in": "1+0.08*on/{n}", "out": "1.08-0.08*on/{n}", "l": "1.08", "r": "1.08"}[mot].format(n=n)
        x = {"in": "iw/2-(iw/zoom/2)", "out": "iw/2-(iw/zoom/2)", "l": "(iw-iw/zoom)*(1-on/{n})", "r": "(iw-iw/zoom)*on/{n}"}[mot].format(n=n)
        vf = f"scale=3840:2160,zoompan=z='{z}':x='{x}':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{Hh}:fps={FPS}"
        cmd = ["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", img, "-i", f"{OUT}/seg/ov{k:02d}.png", "-filter_complex",
               f"[0:v]{vf}[v];[v][1:v]overlay=0:0,format=yuv420p", "-frames:v", str(n)]
    subprocess.run(cmd + ["-c:v", "libx264", "-preset", "medium", "-crf", "19", "-r", str(FPS), out], check=True)
with open(f"{OUT}/seg/list.txt", "w") as fh:
    for k in range(len(SHOTS)): fh.write(f"file 's{k:02d}.mp4'\n")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{OUT}/seg/list.txt", "-c", "copy", f"{OUT}/video.mp4"], check=True)

# 4) sound: ambience beds + one action sound + music swell, under the narration
S = T + "/sfx/"
def bed(src, a, b, vol, fade=.8):
    return f"amovie={src},atrim=0:{b - a:.2f},afade=t=in:d={fade},afade=t=out:st={max(0, b - a - fade):.2f}:d={fade},volume={vol},adelay={int(a * 1000)}|{int(a * 1000)}"
music = H + "/music/secret_underscore_90s.mp3"
parts = [
 bed(S + "desert_wind.mp3", 0, starts[2], 0.35),
 bed(S + "chisel.mp3", starts[2] + .2, starts[3], 0.25, .2),
 bed(S + "tomb_tone.mp3", starts[2], starts[8], 0.6),
 bed(music, starts[7], total, 0.6, 1.0),            # music enters on the reveal ("wonderful things")
]
fc = ";".join(f"{p}[a{i}]" for i, p in enumerate(parts))
fc += f";[1:a]aresample=48000,apad=pad_dur=3,loudnorm=I=-16:TP=-1.5[n];" + "".join(f"[a{i}]" for i in range(len(parts))) + \
      f"amix=inputs={len(parts)}:normalize=0[fx];[n][fx]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89[a]"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/video.mp4", "-i", f"{OUT}/narr.wav", "-filter_complex", fc,
                "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.3f}",
                "-movflags", "+faststart", f"{OUT}/test.mp4"], check=True)
json.dump({"total": total, "cuts": [[round(s, 2), str(SHOTS[k][0])] for k, s in enumerate(starts[:-1])]}, open(f"{OUT}/timeline.json", "w"))
print("DONE", round(total, 1), "s")
