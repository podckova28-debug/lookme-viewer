"""End card: blurred last frame, SUBSCRIBE button that a cursor clicks (turns SUBSCRIBED, bell rings),
then an old-TV switch-off (picture squashes to a bright line, line shrinks to a dot, dot fades). Sound included.

usage: python3 tools/end_subscribe.py BG.png OUT.mp4 [--vo LINE.wav] [--hold 3.4]
"""
import argparse, subprocess, tempfile, os, math, glob
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANG = os.path.join(ROOT, 'assets/fonts/Bangers-Regular.ttf')
INK, YEL, RED, GRAY, WHITE = (20, 16, 18), (255, 226, 92), (214, 52, 40), (120, 120, 120), (255, 255, 255)
W, H, FPS = 1920, 1080, 24
ap = argparse.ArgumentParser(); ap.add_argument('bg'); ap.add_argument('out'); ap.add_argument('--vo', default=''); ap.add_argument('--hold', type=float, default=3.4); ap.add_argument('--title', default="DON'T MISS NEXT WEEK")
a = ap.parse_args()
T_CLICK, T_OFF = 1.6, a.hold           # click time, switch-off start
OFF = [0.22, 0.18, 0.25]               # squash, shrink, dot fade
TOTAL = T_OFF + sum(OFF) + 0.5
bg = Image.open(a.bg).convert('RGB').resize((W, H)).filter(ImageFilter.GaussianBlur(7)); bg = ImageEnhance.Brightness(bg).enhance(0.42)
F = lambda s: ImageFont.truetype(BANG, s)
def eb(t):
    t = max(0, min(1, t)); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2
def ease(t): t = max(0, min(1, t)); return t * t * (3 - 2 * t)
def cursor(d, x, y, press):
    s = 0.85 if press else 1.0
    pts = [(0, 0), (0, 46), (12, 35), (21, 56), (30, 52), (21, 32), (37, 32)]
    d.polygon([(x + px * s * 1.5, y + py * s * 1.5) for px, py in pts], fill=WHITE, outline=INK, width=4)
def bell(d, cx, cy, ang):
    r = 34; c, s_ = math.cos(ang), math.sin(ang)
    rot = lambda px, py: (cx + px * c - py * s_, cy + px * s_ + py * c)
    body = [rot(-r, 20), rot(-r * 0.8, -10), rot(-r * 0.4, -r), rot(r * 0.4, -r), rot(r * 0.8, -10), rot(r, 20)]
    d.polygon(body, fill=YEL, outline=INK, width=5); d.ellipse([cx - 9, cy + 18, cx + 9, cy + 36], fill=YEL, outline=INK, width=4)
def card(t):
    im = bg.copy(); d = ImageDraw.Draw(im)
    k = eb(t / 0.4)
    d.text((W / 2, 330 - (1 - k) * 300), a.title, font=F(150), fill=YEL, stroke_width=10, stroke_fill=INK, anchor='mm')
    clicked = t >= T_CLICK
    bw, bh, bx, by = 620, 150, W / 2 - 40, 600
    sc = 1.0 + (0.06 * math.sin(min(1, (t - T_CLICK) / 0.25) * math.pi) if clicked and t < T_CLICK + 0.25 else 0)
    w2, h2 = bw * sc / 2, bh * sc / 2
    d.rounded_rectangle((bx - w2 + 10, by - h2 + 10, bx + w2 + 10, by + h2 + 10), 30, fill=(0, 0, 0))
    d.rounded_rectangle((bx - w2, by - h2, bx + w2, by + h2), 30, fill=GRAY if clicked else RED, outline=INK, width=7)
    d.text((bx, by + 4), 'SUBSCRIBED' if clicked else 'SUBSCRIBE', font=F(96), fill=WHITE, stroke_width=5, stroke_fill=INK, anchor='mm')
    ang = 0.45 * math.sin((t - T_CLICK - 0.2) * 28) * max(0, 1 - (t - T_CLICK - 0.2) / 0.8) if t > T_CLICK + 0.2 else 0
    bell(d, bx + bw / 2 + 110, by - 4, ang)
    # cursor glides in from bottom right, presses, then rests
    p = ease((t - 0.5) / (T_CLICK - 0.55))
    cx, cy = (W + 80) + (bx + 120 - W - 80) * p, (H + 80) + (by + 10 - H - 80) * p
    if t > 0.5: cursor(d, cx, cy, T_CLICK - 0.06 <= t <= T_CLICK + 0.12)
    return im
def tv_off(im, t):
    """t from 0 at switch-off start."""
    a1, a2, a3 = OFF; out = Image.new('RGB', (W, H), (0, 0, 0))
    if t < a1:   # squash vertically, brighten toward white
        k = ease(t / a1); h = max(4, int(H * (1 - k) ** 1.6))
        src = ImageEnhance.Brightness(im).enhance(1 + 2.5 * k).resize((W, h), Image.LANCZOS)
        out.paste(src, (0, (H - h) // 2))
    elif t < a1 + a2:   # bright line shrinks horizontally
        k = ease((t - a1) / a2); w = max(6, int(W * (1 - k)))
        d = ImageDraw.Draw(out); d.rectangle(((W - w) // 2, H // 2 - 3, (W + w) // 2, H // 2 + 3), fill=(235, 245, 255))
    elif t < a1 + a2 + a3:   # dot glows then fades
        k = (t - a1 - a2) / a3; r = int(10 * (1 - k) + 2); v = int(255 * (1 - k))
        glow = Image.new('RGB', (W, H), (0, 0, 0)); d = ImageDraw.Draw(glow)
        d.ellipse((W / 2 - r * 4, H / 2 - r * 4, W / 2 + r * 4, H / 2 + r * 4), fill=(v // 5, v // 5, v // 4))
        out = glow.filter(ImageFilter.GaussianBlur(10)); d = ImageDraw.Draw(out)
        d.ellipse((W / 2 - r, H / 2 - r, W / 2 + r, H / 2 + r), fill=(v, v, v))
    return out
tmp = tempfile.mkdtemp(); n = int(round(TOTAL * FPS))
for i in range(n):
    t = i / FPS
    fr = card(min(t, T_OFF)) if t < T_OFF else tv_off(card(T_OFF), t - T_OFF)
    fr.save(f'{tmp}/{i:04d}.png')
# sound: soft click on the press, a bell ding, then the CRT "thunk + falling whine"
SR = 48000; L = int(TOTAL * SR); au = np.zeros(L)
def put(sig, t0):
    s = int(t0 * SR); e = min(L, s + len(sig)); au[s:e] += sig[:e - s]
tt = lambda d: np.arange(int(d * SR)) / SR
x = tt(0.04); put(0.5 * np.random.randn(len(x)) * np.exp(-x * 120), T_CLICK)
x = tt(0.9); put(0.25 * (np.sin(2 * np.pi * 1320 * x) + 0.5 * np.sin(2 * np.pi * 2640 * x)) * np.exp(-x * 5), T_CLICK + 0.2)
x = tt(0.12); put(0.6 * np.sin(2 * np.pi * 70 * x) * np.exp(-x * 30), T_OFF)
x = tt(0.7); put(0.12 * np.sin(2 * np.pi * np.cumsum(np.linspace(15000, 3000, len(x))) / SR) * np.exp(-x * 4), T_OFF)
au = np.clip(au, -1, 1).astype(np.float32)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', f'{tmp}/fx.wav'], input=au.tobytes(), check=True)
amix = ['-i', a.vo, '-filter_complex', '[1:a]aformat=channel_layouts=stereo[f];[2:a]adelay=200|200,aformat=channel_layouts=stereo,volume=1.6[v];[f][v]amix=inputs=2:normalize=0:duration=first[a]', '-map', '0:v', '-map', '[a]'] if a.vo else ['-map', '0:v', '-map', '1:a']
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', f'{tmp}/%04d.png', '-i', f'{tmp}/fx.wav', *amix,
                '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-ar', '48000', '-ac', '2', a.out], check=True)
for f in glob.glob(f'{tmp}/*'): os.remove(f)
print('ok', a.out, f'{TOTAL:.2f}s')
