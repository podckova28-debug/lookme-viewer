"""Comic FX drawn over finished 1080p blocks: spider-sense vibration lines around the head and SFX bursts.

usage: python3 tools/fx_overlay.py IN.mp4 OUT.mp4 FX.json
FX.json: list of effects, each with "type" and frame range "f0"/"f1" (inclusive, 24 fps):
  {"type": "sense", "f0": 55, "f1": 87, "cx": 1040, "cy": 430, "rx": 560, "ry": 470}
  {"type": "burst", "f0": 58, "f1": 87, "x": 1600, "y": 170, "text": "TINGLE!", "size": 96, "rot": 8}
  {"type": "caption", "f0": 0, "f1": 60, "x": 60, "y": 50, "lines": ["7:02 AM"], "size": 64}
  {"type": "label", "f0": 30, "f1": 90, "x": 1200, "y": 700, "title": "DAVE", "sub": "Roommate. Nothing surprises him.", "size": 70}
"""
import sys, os, json, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANG = os.path.join(ROOT, 'assets/fonts/Bangers-Regular.ttf')
NEUE = os.path.join(ROOT, 'assets/fonts/ComicNeue-Bold.ttf')
INK, RED, YEL = (24, 20, 22, 255), (214, 52, 40, 255), (250, 206, 64, 255)

def ease_back(t):
    t = max(0.0, min(1.0, t)); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2

def squiggle(d, x0, y0, ang, length, amp, phase, width):
    pts = []
    for i in range(25):
        s = i / 24
        off = amp * math.sin(s * 3 * math.pi + phase) * (0.4 + 0.6 * s)
        x = x0 + math.cos(ang) * length * s - math.sin(ang) * off
        y = y0 + math.sin(ang) * length * s + math.cos(ang) * off
        pts.append((x, y))
    d.line(pts, fill=INK, width=width + 8, joint='curve')
    d.line(pts, fill=(255, 255, 255, 255), width=width, joint='curve')

def sense(d, e, f):
    # angles in degrees, 0 = right, counter-clockwise on screen is negative y
    angs = [200, 180, 160, 140, 120, -20, 0, 20, 40, 60]
    k = (f - e['f0'])
    grow = ease_back(k / 6)
    hold = (k // 2) % 2          # on twos, alternate the wiggle phase
    for j, a in enumerate(angs):
        a = math.radians(-a)
        r0x, r0y = e['rx'] * (1.0 + 0.04 * hold), e['ry'] * (1.0 + 0.04 * hold)
        x0 = e['cx'] + math.cos(a) * r0x; y0 = e['cy'] + math.sin(a) * r0y
        L = 175 * grow * (0.85 + 0.3 * ((j * 7) % 3) / 2)
        if L > 4:
            squiggle(d, x0, y0, a, L, 20, hold * math.pi + j, 13)

_burst_cache = {}
def burst_img(text, size, rot):
    key = (text, size, rot)
    if key not in _burst_cache:
        f = ImageFont.truetype(BANG, size)
        tw = int(f.getlength(text)) + 120; th = size + 140
        im = Image.new('RGBA', (tw, th), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        cx, cy = tw / 2, th / 2
        pts = [(cx + (0.5 if i % 2 else 0.36) * tw * math.cos(i * math.pi / 18), cy + (0.5 if i % 2 else 0.36) * th * 1.05 * math.sin(i * math.pi / 18)) for i in range(36)]
        d.polygon(pts, fill=YEL, outline=INK, width=7)
        d.text((cx, cy + 6), text, font=f, fill=RED, stroke_width=7, stroke_fill=INK, anchor='mm')
        _burst_cache[key] = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    return _burst_cache[key]

def burst(canvas, e, f):
    k = f - e['f0']; s = ease_back(k / 5) * (1 + 0.03 * math.sin(k * 1.3))
    b = burst_img(e['text'], e.get('size', 96), e.get('rot', 8))
    b = b.resize((max(1, int(b.width * s)), max(1, int(b.height * s))), Image.LANCZOS)
    canvas.alpha_composite(b, (int(e['x'] - b.width / 2), int(e['y'] - b.height / 2)))

def slide_alpha(e, f, dur=5):
    k = f - e['f0']; out = e['f1'] - f
    return max(0.0, min(1.0, k / dur, out / 4 + 0.0001))

def caption(canvas, e, f):
    """Yellow comic narration box, black border, Bangers lettering. Pops in, fades out."""
    fnt = ImageFont.truetype(BANG, e.get('size', 64))
    pad = int(e.get('size', 64) * 0.35)
    tw = max(int(fnt.getlength(t)) for t in e['lines']); lh = int(e.get('size', 64) * 1.05)
    box = Image.new('RGBA', (tw + 2 * pad + 10, lh * len(e['lines']) + 2 * pad + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(box)
    d.rectangle((8, 8, box.width - 1, box.height - 1), fill=(20, 16, 18, 200))
    d.rectangle((0, 0, box.width - 9, box.height - 9), fill=(255, 226, 92, 255), outline=INK, width=6)
    for i, t in enumerate(e['lines']):
        d.text((pad, pad - 4 + i * lh), t, font=fnt, fill=INK)
    a = slide_alpha(e, f); s = 0.85 + 0.15 * ease_back(min(1, (f - e['f0']) / 5))
    b = box.resize((max(1, int(box.width * s)), max(1, int(box.height * s))), Image.LANCZOS)
    b.putalpha(b.split()[3].point(lambda v: int(v * a)))
    canvas.alpha_composite(b, (e['x'], e['y']))

def label(canvas, e, f):
    """Character intro: big name in white Bangers with ink outline, one line under it in a white box."""
    sz = e.get('size', 70)
    ft = ImageFont.truetype(BANG, sz); fs = ImageFont.truetype(NEUE, int(sz * 0.56))
    tw = max(int(ft.getlength(e['title'])), int(fs.getlength(e['sub'])) + 40) + 40
    box = Image.new('RGBA', (tw, int(sz * 2.3)), (0, 0, 0, 0)); d = ImageDraw.Draw(box)
    d.text((10, 0), e['title'], font=ft, fill=(255, 255, 255, 255), stroke_width=8, stroke_fill=INK)
    sy = int(sz * 1.15); sw = int(fs.getlength(e['sub'])) + 40
    d.rectangle((10, sy, 10 + sw, sy + int(sz * 0.8)), fill=(255, 255, 255, 255), outline=INK, width=5)
    d.text((30, sy + int(sz * 0.12)), e['sub'], font=fs, fill=INK)
    a = slide_alpha(e, f); dx = int((1 - ease_back(min(1, (f - e['f0']) / 6))) * -120)
    box.putalpha(box.split()[3].point(lambda v: int(v * a)))
    canvas.alpha_composite(box, (e['x'] + dx, e['y']))

def main():
    src, out, fxp = sys.argv[1:4]
    fx = json.load(open(fxp))
    rd = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    wr = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24', '-i', '-',
                           '-i', src, '-map', '0:v', '-map', '1:a?', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16',
                           '-pix_fmt', 'yuv420p', '-c:a', 'copy', out], stdin=subprocess.PIPE)
    f = 0
    while True:
        buf = rd.stdout.read(W * H * 3)
        if len(buf) < W * H * 3: break
        act = [e for e in fx if e['f0'] <= f <= e['f1']]
        if act:
            fr = Image.frombuffer('RGB', (W, H), buf).convert('RGBA')
            layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
            for e in act:
                if e['type'] == 'sense': sense(d, e, f)
            for e in act:
                if e['type'] == 'burst': burst(layer, e, f)
                elif e['type'] == 'caption': caption(layer, e, f)
                elif e['type'] == 'label': label(layer, e, f)
            buf = Image.alpha_composite(fr, layer).convert('RGB').tobytes()
        wr.stdin.write(buf); f += 1
    wr.stdin.close(); wr.wait(); rd.wait()
    print('frames', f)

main()
