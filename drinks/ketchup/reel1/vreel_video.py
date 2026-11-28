# Instagram Reel / YouTube Short (1080x1920) built from the long video's frames without cropping the drawings:
# white margins are trimmed, the drawing is enlarged to the full width of a white 9:16 canvas, captions sit in the
# free space above it (Bebas Neue, white caps on an uneven red brush stripe). Run from the scratchpad (needs abs_s1/).
import os, sys, glob, json, random, subprocess, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageOps
HERE = os.path.dirname(os.path.abspath(__file__))
FR = os.path.join(HERE, "..", "frames", "jpg")
FONT = "/home/user/lookme-viewer/history/fonts/PatrickHand-Regular.ttf"   # same hand as the arrow notes in the frames
VO = "ket_r1"; WORK = "ket_r1v_video"; os.makedirs(WORK, exist_ok=True)
W, H = 1080, 1920
PH, MAXPAN, YC = 1080, 2.3, 0.62     # picture height, max picture width (x canvas width), picture centre (x canvas height)
FPS, GAP = 30, 0.05
# shots: (list of line indexes, frame or [top, bottom] frames)
SHOTS = [([i], i + 1) for i in range(12)]   # vframes/vN.jpg, native 9:16
LINES = [l.strip() for l in open(os.path.join(HERE, "vo.txt")) if l.strip()]
# shorter on-screen text where the spoken line is too long for 3 caption rows
CAPS = {}
PICK = {}
if os.path.exists(os.path.join(HERE, "picks.txt")):
    for l in open(os.path.join(HERE, "picks.txt")):
        if l.strip(): a, b = l.split(); PICK[int(a)] = int(b)

def trimmed(path):
    im = Image.open(path).convert("RGB")
    g = ImageOps.invert(im.convert("L")).point(lambda v: 255 if v > 18 else 0)
    return im.crop(g.getbbox())

ZOOM = 0.07
def picture(frame):
    # native vertical frame: content scaled to 94% of a 2x canvas, so the slow push-in never crops it
    im = Image.open(os.path.join(HERE, "vframes", f"v{frame}.jpg")).convert("RGB")
    cw, ch = W * 2, H * 2
    can = Image.new("RGB", (cw, ch), "white")
    th = int(ch * 0.94); tw = int(im.width * th / im.height)
    if tw > cw * 0.94: tw = int(cw * 0.94); th = int(im.height * tw / im.width)
    can.paste(im.resize((tw, th), Image.LANCZOS), ((cw - tw) // 2, ch - th - int(ch * 0.02)))
    return can

def chunks(text, dur):
    """Split a spoken line into 1-3 word captions timed by character length (speech fills the clip)."""
    words = text.replace(",", "").split()
    groups, cur = [], []
    for w in words:
        cur.append(w)
        n = len(" ".join(cur))
        if len(cur) == 3 or n >= 13 or w.endswith((".", "?", "!")):
            groups.append(" ".join(cur)); cur = []
    if cur: groups.append(" ".join(cur))
    total = sum(len(g) + 2 for g in groups); t, out = 0.0, []
    for g in groups:
        d = dur * (len(g) + 2) / total; out.append((t, t + d, g.rstrip("."))); t += d
    return out

def caption(text, seed):
    # handwritten marker like the arrow notes: dark ink, lowercase as spoken, thin uneven red underline
    random.seed(seed)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    size = 140
    f = ImageFont.truetype(FONT, size)
    while d.textlength(text, font=f) > W * 0.88: size -= 8; f = ImageFont.truetype(FONT, size)
    tw = d.textlength(text, font=f); x0 = (W - tw) / 2; y = 250
    top, bot = y + size * 1.02, y + size * 1.10
    pts = [(x0 - 18 + random.uniform(-6, 6), top + random.uniform(-5, 5))]
    for i in range(1, 9): pts.append((x0 - 18 + (tw + 36) * i / 8, top + random.uniform(-6, 4)))
    for i in range(8, -1, -1): pts.append((x0 - 18 + (tw + 36) * i / 8 + random.uniform(-4, 4), bot + random.uniform(-4, 8)))
    d.polygon(pts, fill=(200, 30, 36, 255))
    d.text((x0, y), text, font=f, fill=(40, 34, 30, 255), stroke_width=1, stroke_fill=(40, 34, 30, 255))
    return ov

# narration
SR = 24000; audio, t, starts, speechlen = [], 0.0, [], []
for i in range(len(LINES)):
    fn = f"{VO}/l{i:03d}.wav"
    if PICK.get(i): fn = fn.replace(".wav", f"_s{PICK[i]}.wav")
    w, sr = sf.read(fn, dtype="float32"); assert sr == SR
    starts.append(t); speechlen.append(len(w) / SR); audio += [w, np.zeros(int(GAP * SR), np.float32)]; t += len(w) / SR + GAP
total = t + 0.6; audio.append(np.zeros(int(0.6 * SR), np.float32))
nar = np.concatenate(audio)
SFX = "/home/user/lookme-viewer/drinks/music/sfx"
def sfx(name, at, gain):
    w, r = sf.read(f"{SFX}/{name}.wav", dtype="float32")
    if w.ndim > 1: w = w.mean(1)
    w = np.interp(np.arange(0, len(w), r / SR), np.arange(len(w)), w) * gain
    i = max(0, int(at * SR)); j = min(len(nar), i + len(w)); nar[i:j] += w[:j - i]
sfx("stamp", 0.0, 0.6)
for li in range(1, len(LINES)): sfx("whoosh", starts[li] - 0.12, 0.25)
for li in (5, 6, 7, 10): sfx("pop", starts[li], 0.35)
nar /= max(1.0, np.abs(nar).max() / 0.95)
sf.write(f"{WORK}/narration.wav", nar, SR)
ends = starts[1:] + [total]

segs = []
for k, (lines, frame) in enumerate(SHOTS):
    im = picture(frame); pic = f"{WORK}/pic_{k}.png"; im.save(pic)
    s0, s1 = starts[lines[0]], ends[lines[-1]]
    for li in lines:
        a, b = starts[li], ends[li]
        parts = chunks(CAPS.get(li, LINES[li]), speechlen[li])
        parts[-1] = (parts[-1][0], b - a, parts[-1][2])
        for ci, (c0, c1, txt) in enumerate(parts):
            ta, tb = a + c0, a + c1; n = max(1, round((tb - ta) * FPS))
            z0 = ZOOM * (ta - s0) / (s1 - s0); z1 = ZOOM * (tb - s0) / (s1 - s0)
            if k % 2: z0, z1 = ZOOM - z0, ZOOM - z1
            cap = f"{WORK}/cap_{li}_{ci}.png"; caption(txt, li * 10 + ci).save(cap)
            out = f"{WORK}/seg_{li:02d}_{ci:02d}.mp4"
            z = f"1+{z0:.5f}+({z1 - z0:.5f})*on/{n}"
            fc = (f"[0:v]zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS}[p];"
                  f"[p][1:v]overlay=0:0,format=yuv420p")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", pic, "-loop", "1", "-i", cap, "-filter_complex", fc,
                            "-frames:v", str(n), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", out], check=True)
            segs.append(out)
        print("line", li, frame, len(parts), flush=True)
with open(f"{WORK}/segs.txt", "w") as fh:
    for s in segs: fh.write(f"file '{os.path.abspath(s)}'\n")
print("TOTAL", round(total, 1))
