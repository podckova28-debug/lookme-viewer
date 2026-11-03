"""Comic 'power card' insert: a framed panel slides in over a halftone burst, title + caption + SFX lettering.

usage: python3 tools/comic_card.py PANEL.png OUT.mp4 "SPIDER-SENSE" "POWER #1" "Range: one fly." "TINGLE!" [secs]
"""
import sys, os, math, subprocess, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1920, 1080, 24
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANG = os.path.join(ROOT, 'assets/fonts/Bangers-Regular.ttf')
NEUE = os.path.join(ROOT, 'assets/fonts/ComicNeue-Bold.ttf')
INK = (24, 20, 22)
PAPER = (246, 236, 214)
RED = (214, 52, 40)
YEL = (250, 206, 64)

def ease_back(t):           # overshoot ease-out
    c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2

def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))

def background():
    bg = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(bg)
    cx, cy = W * 0.62, H * 0.5
    for i in range(28):                               # sun-burst rays
        a0 = i * 2 * math.pi / 28; a1 = a0 + math.pi / 28
        r = 2400
        d.polygon([(cx, cy), (cx + r * math.cos(a0), cy + r * math.sin(a0)), (cx + r * math.cos(a1), cy + r * math.sin(a1))],
                  fill=(250, 222, 150) if i % 2 else PAPER)
    dots = Image.new('L', (W, H), 0); dd = ImageDraw.Draw(dots)   # halftone dots, bigger toward the edges
    for y in range(0, H, 22):
        for x in range((y // 22) % 2 * 11, W, 22):
            rr = 1.5 + 6.5 * clamp(math.hypot(x - cx, y - cy) / 1300)
            dd.ellipse((x - rr, y - rr, x + rr, y + rr), fill=255)
    bg.paste(Image.new('RGB', (W, H), (232, 120, 80)), (0, 0), dots.point(lambda v: v * 0.55))
    return bg

def panel(img_path, pw=1080, ph=680):
    im = Image.open(img_path).convert('RGB')
    s = max(pw / im.width, ph / im.height); im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    l = (im.width - pw) // 2; t = (im.height - ph) // 2
    return im.crop((l, t, l + pw, t + ph))

def outlined(d, xy, text, font, fill, stroke=8, sc=INK, anchor='la'):
    d.text(xy, text, font=font, fill=fill, stroke_width=stroke, stroke_fill=sc, anchor=anchor)

def burst(text, size):
    f = ImageFont.truetype(BANG, size)
    tw = int(f.getlength(text)) + 140; th = size + 160
    im = Image.new('RGBA', (tw, th), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx, cy = tw / 2, th / 2; pts = []
    for i in range(36):
        a = i * 2 * math.pi / 36; r = (0.5 if i % 2 else 0.36)
        pts.append((cx + r * tw * math.cos(a), cy + r * th * 1.05 * math.sin(a)))
    d.polygon(pts, fill=YEL, outline=INK, width=7)
    outlined(d, (cx, cy + 6), text, f, RED, 7, anchor='mm')
    return im

def main():
    src, out, title, kicker, caption, sfx = sys.argv[1:7]
    secs = float(sys.argv[7]) if len(sys.argv) > 7 else 2.5
    n = int(secs * FPS)
    bg = background(); pan = panel(src)
    fb = ImageFont.truetype(BANG, 150); fk = ImageFont.truetype(BANG, 54); fc = ImageFont.truetype(NEUE, 46)
    bst = burst(sfx, 120)
    tmp = tempfile.mkdtemp()
    for i in range(n):
        t = i / FPS
        fr = bg.copy(); d = ImageDraw.Draw(fr)
        # panel: slide in from the right with overshoot, then a slow push-in
        k = ease_back(clamp(t / 0.35)); zoom = 1 + 0.035 * clamp((t - 0.35) / (secs - 0.35))
        pw, ph = int(pan.width * zoom), int(pan.height * zoom)
        p = pan.resize((pw, ph), Image.LANCZOS).crop(((pw - pan.width) // 2, (ph - pan.height) // 2, (pw - pan.width) // 2 + pan.width, (ph - pan.height) // 2 + pan.height))
        framed = Image.new('RGB', (pan.width + 28, pan.height + 28), INK); framed.paste(p, (14, 14))
        rot = framed.convert('RGBA').rotate(-2.2, expand=True, resample=Image.BICUBIC)
        x = int(W * 0.415 + (1 - k) * 1300); y = int(H * 0.5 - rot.height / 2 + 30)
        sh = Image.new('RGBA', rot.size, (0, 0, 0, 0)); sh.paste((20, 16, 18, 150), (0, 0), rot.split()[3])
        fr.paste(sh.filter(ImageFilter.GaussianBlur(6)), (x + 18, y + 22), sh.filter(ImageFilter.GaussianBlur(6)))
        fr.paste(rot, (x, y), rot)
        # title block from the left
        kt = ease_back(clamp((t - 0.12) / 0.35)); tx = int(70 - (1 - kt) * 900)
        d.rectangle((tx, 120, tx + 330, 190), fill=INK); d.text((tx + 22, 126), kicker, font=fk, fill=YEL)
        outlined(d, (tx, 200), title, fb, (255, 255, 255), 10)
        # caption box
        kc = clamp((t - 0.55) / 0.2)
        if kc > 0:
            cw = int(fc.getlength(caption)) + 60
            box = Image.new('RGBA', (cw, 92), (0, 0, 0, 0)); bd = ImageDraw.Draw(box)
            bd.rectangle((0, 0, cw - 1, 91), fill=(255, 255, 255), outline=INK, width=6); bd.text((30, 18), caption, font=fc, fill=INK)
            box.putalpha(box.split()[3].point(lambda v: int(v * kc)))
            fr.paste(box, (tx + 10, 430), box)
        # SFX burst pops in
        ks = clamp((t - 0.45) / 0.18)
        if ks > 0:
            s = ease_back(ks) * (1 + 0.03 * math.sin(t * 30))
            b = bst.resize((max(1, int(bst.width * s)), max(1, int(bst.height * s))), Image.LANCZOS).rotate(8, expand=True, resample=Image.BICUBIC)
            fr.paste(b, (int(W * 0.80 - b.width / 2), int(H * 0.20 - b.height / 2)), b)
        fr.save(f'{tmp}/{i:04d}.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', f'{tmp}/%04d.png', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
                    '-shortest', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-c:a', 'aac', out], check=True)

main()
