#!/usr/bin/env python3
"""S19: машина (кадр ИИ) едет по дуге, следы колёс рисуются кодом — внешнее колесо по большой дуге, внутреннее по малой.
Мутаций быть не может: машина — одна картинка, двигается только целиком."""
import math, subprocess, os
import numpy as np
import imageio_ffmpeg
from PIL import Image, ImageFilter, ImageDraw

FF = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS, DUR = 1920, 1080, 30, 11.5
HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda p: os.path.join(HERE, p)
OR = (236, 122, 32); BL = (110, 190, 240); INK = (43, 33, 24)

# --- фон: асфальт в тоне кадра S19 ---
ref = np.asarray(Image.open(P('mkf/S19.png')).convert('RGB'), np.float32)
base = np.median(ref[500:740, 950:1330].reshape(-1, 3), axis=0)
rng = np.random.default_rng(7)
noise = rng.normal(0, 7, (H, W, 1)).astype(np.float32)
bg = np.clip(base + noise, 0, 255)
spk = rng.random((H, W)) < 0.004
bg[spk] -= 35
spk = rng.random((H, W)) < 0.003
bg[spk] += 28
bgim = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8)).convert('RGBA')

# --- спрайт машины: белый фон -> прозрачный (заливка от краёв) ---
spr = Image.open(P('mkf/spr_S19.png')).convert('RGB')
a = np.asarray(spr).astype(np.int16)
white = (a.min(axis=2) > 232)
# связная с краями область белого
from collections import deque
h, w = white.shape; bgmask = np.zeros_like(white); q = deque()
for x in range(w):
    for y in (0, h - 1):
        if white[y, x] and not bgmask[y, x]: bgmask[y, x] = 1; q.append((y, x))
for y in range(h):
    for x in (0, w - 1):
        if white[y, x] and not bgmask[y, x]: bgmask[y, x] = 1; q.append((y, x))
while q:
    y, x = q.popleft()
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        yy, xx = y + dy, x + dx
        if 0 <= yy < h and 0 <= xx < w and white[yy, xx] and not bgmask[yy, xx]:
            bgmask[yy, xx] = 1; q.append((yy, xx))
alpha = Image.fromarray(((1 - bgmask) * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.7))
car = spr.convert('RGBA'); car.putalpha(alpha)
car = car.crop(car.getbbox())
CL = 420  # длина машины на экране
car = car.resize((CL, int(car.height * CL / car.width)), Image.LANCZOS)
CW = car.height
# тень
sh = Image.new('RGBA', (car.width + 60, car.height + 60), (0, 0, 0, 0))
sh.paste((0, 0, 0, 110), (30, 30), car.getchannel('A'))
sh = sh.filter(ImageFilter.GaussianBlur(10))

# --- траектория: поворот направо по дуге (центр поворота снизу) ---
CX, CY, R = 960, 980, 600
TW = CW * 0.78  # колея
A0, A1 = math.radians(150), math.radians(38)

def ease(x):
    x = max(0, min(1, x)); return x * x * (3 - 2 * x)

def pose(t):
    k = ease((t - 0.4) / 8.6)
    th = A0 + (A1 - A0) * k
    return th

# --- следы: заранее рисуем полные дуги со сглаживанием (2x), открываем угловой маской ---
S = 2
tr = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0)); d = ImageDraw.Draw(tr)
REAR = CL * 0.30  # задняя ось позади центра машины
def arc(r, col, wd):
    st, en = -math.degrees(A0) - 3, -math.degrees(A1) + 3
    for ww, c in ((wd + 10, INK), (wd, col)):
        rr = r + ww / 2  # PIL рисует толщину внутрь от рамки — центрируем на радиусе r
        d.arc([(CX - rr) * S, (CY - rr) * S, (CX + rr) * S, (CY + rr) * S], st, en, fill=c + (255,), width=int(ww * S))
# задняя ось на радиусе R => центр машины чуть дальше; следы задних колёс
arc(R + TW / 2, OR, 24)
arc(R - TW / 2, BL, 24)
tr = tr.resize((W, H), Image.LANCZOS)
trn = np.asarray(tr).astype(np.float32)
yy, xx = np.mgrid[0:H, 0:W]
ang = np.arctan2(-(yy - CY), xx - CX)  # математический угол
ang = np.where(ang < 0, ang + 2 * np.pi, ang)

def frame(t):
    th = pose(t)
    fr = bgim.copy()
    # маска раскрытия следов: от A0 до текущего угла задней оси
    rear_th = th
    m = ((ang <= A0) & (ang >= rear_th)).astype(np.float32)
    lay = trn.copy(); lay[..., 3] *= m
    fr.alpha_composite(Image.fromarray(lay.astype(np.uint8)))
    # машина: центр — на радиусе sqrt(R^2+REAR^2), курс — касательная (по часовой)
    px = CX + R * math.cos(th); py = CY - R * math.sin(th)
    head = th - math.pi / 2  # направление движения при убывающем угле
    cx = px + REAR * math.cos(head); cy = py - REAR * math.sin(head)
    deg = math.degrees(head)
    rc = car.rotate(deg, resample=Image.BICUBIC, expand=True)
    rs = sh.rotate(deg, resample=Image.BICUBIC, expand=True)
    fr.alpha_composite(rs, (int(cx - rs.width / 2 + 10), int(cy - rs.height / 2 + 14)))
    fr.alpha_composite(rc, (int(cx - rc.width / 2), int(cy - rc.height / 2)))
    return fr.convert('RGB')

if __name__ == '__main__':
    import sys
    if '--test' in sys.argv:
        ims = [frame(t).resize((640, 360)) for t in (0, 3, 6, 9.5)]
        s = Image.new('RGB', (1280, 720))
        for i, im in enumerate(ims): s.paste(im, ((i % 2) * 640, (i // 2) * 360))
        s.save(P('qa/S19code_test.jpg'), quality=85); print('test ok'); sys.exit()
    out = P('mclips/S19.mp4')
    if os.path.exists(out) and not os.path.exists(P('mclips/S19_ai_v2.mp4')): os.rename(out, P('mclips/S19_ai_v2.mp4'))
    enc = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        enc.stdin.write(frame(i / FPS).tobytes())
    enc.stdin.close(); enc.wait(); print('готово', out)
