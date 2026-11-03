"""Static comic-page insert: 1-4 still images laid out as comic panels on paper, each slides in with a small
overshoot, then a slow push-in over the whole page (Ken Burns). Optional caption box and SFX burst.
Costs nothing: stills come from finished blocks or from 2-credit images.

usage: python3 tools/comic_page.py OUT.mp4 SECS LAYOUT IMG1 [IMG2 ...] [--caption "TEXT|LINE2"] [--sfx WORD] [--audio IN.wav]
LAYOUT: one | two | three | four  (three = big left + two stacked right)
"""
import sys, os, argparse, subprocess, tempfile, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANG = os.path.join(ROOT, 'assets/fonts/Bangers-Regular.ttf')
INK, PAPER, YEL, RED = (20, 16, 18), (243, 233, 212), (255, 226, 92), (214, 52, 40)
W, H, FPS, G = 1920, 1080, 24, 26

ap = argparse.ArgumentParser()
ap.add_argument('out'); ap.add_argument('secs', type=float); ap.add_argument('layout'); ap.add_argument('imgs', nargs='+')
ap.add_argument('--caption', default=''); ap.add_argument('--sfx', default=''); ap.add_argument('--audio', default='')
a = ap.parse_args()

def boxes(layout):
    m = 60
    if layout == 'one':   return [(m, m, W - m, H - m)]
    if layout == 'two':   return [(m, m, W // 2 - G // 2, H - m), (W // 2 + G // 2, m, W - m, H - m)]
    if layout == 'three': return [(m, m, int(W * .58), H - m), (int(W * .58) + G, m, W - m, H // 2 - G // 2), (int(W * .58) + G, H // 2 + G // 2, W - m, H - m)]
    return [(m, m, W // 2 - G // 2, H // 2 - G // 2), (W // 2 + G // 2, m, W - m, H // 2 - G // 2),
            (m, H // 2 + G // 2, W // 2 - G // 2, H - m), (W // 2 + G // 2, H // 2 + G // 2, W - m, H - m)]

def fill(im, w, h):
    s = max(w / im.width, h / im.height); im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    l, t = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((l, t, l + w, t + h))

def eb(t):
    t = max(0, min(1, t)); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2

bx = boxes(a.layout)
panels = []
for (x0, y0, x1, y1), p in zip(bx, a.imgs):
    im = fill(Image.open(p).convert('RGB'), x1 - x0, y1 - y0)
    fr = Image.new('RGB', (im.width + 16, im.height + 16), INK); fr.paste(im, (8, 8)); panels.append((x0 - 8, y0 - 8, fr))
fb = ImageFont.truetype(BANG, 74)
n = int(a.secs * FPS); tmp = tempfile.mkdtemp()
for i in range(n):
    t = i / FPS
    page = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(page)
    for k, (x, y, fr) in enumerate(panels):
        st = 0.12 + k * 0.28; e = eb((t - st) / 0.35)
        if t < st: continue
        dx = int((1 - e) * (220 if k % 2 == 0 else -220))
        page.paste(fr, (x + dx, y))
    if a.caption and t > 0.5:
        lines = a.caption.split('|'); tw = max(int(fb.getlength(s)) for s in lines) + 50; th = 82 * len(lines) + 30
        d.rectangle((70 + 8, H - 70 - th + 8, 70 + tw + 8, H - 70 + 8), fill=(0, 0, 0))
        d.rectangle((70, H - 70 - th, 70 + tw, H - 70), fill=YEL, outline=INK, width=6)
        for j, s in enumerate(lines): d.text((95, H - 70 - th + 14 + j * 82), s, font=fb, fill=INK)
    if a.sfx and t > 0.9:
        fs = ImageFont.truetype(BANG, int(120 * min(1, eb((t - 0.9) / 0.25))))
        d.text((W - 380, 150), a.sfx, font=fs, fill=RED, stroke_width=9, stroke_fill=INK, anchor='mm')
    z = 1 + 0.05 * t / a.secs
    page = page.resize((int(W * z), int(H * z)), Image.LANCZOS)
    l, u = (page.width - W) // 2, (page.height - H) // 2
    page.crop((l, u, l + W, u + H)).save(f'{tmp}/{i:04d}.png')
aud = ['-i', a.audio] if a.audio else ['-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo']
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', f'{tmp}/%04d.png', *aud, '-t', str(a.secs),
                '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-ar', '48000', a.out], check=True)
print('ok', a.out)
