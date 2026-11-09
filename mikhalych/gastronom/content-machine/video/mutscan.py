#!/usr/bin/env python3
"""Поиск мутаций в ИИ-клипах: лист кадров в пиках движения.

    python mutscan.py clips/M1.mp4 clips/M2.mp4 ... [--to M5=6.6] [--out qa/mut]

Глюки Kling/Seedance/Wan (кисть превращается в месиво, кулак сливается с плечом, рука прыгает) длятся 0,15–0,2 с
и между кадрами через 0,7 с не видны. Зато они всегда на резком движении: разность соседних кадров в 4–7 раз выше
медианы клипа. Скрипт берёт по каждому клипу 8 самых сильных пиков, склеивает близкие (< 0,2 с) и кладёт кадр
каждого пика на лист 3×2 (`<out>/peaks_N.jpg`). Подозрительное место дальше смотреть кадрами через 0,07 с.
Провал резкости по ячейкам такие глюки не ловит: у месива остаются чёрные контуры (проверено 5 нояб 2026).
"""
import io, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

args = [a for a in sys.argv[1:]]
out = 'qa/mut'
if '--out' in args: i = args.index('--out'); out = args[i + 1]; del args[i:i + 2]
lim = {}
while '--to' in args:
    i = args.index('--to'); k, v = args[i + 1].split('='); lim[k] = float(v); del args[i:i + 2]
os.makedirs(out, exist_ok=True)
W, H = 320, 180


def probe(f):
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=r_frame_rate:format=duration',
                        '-of', 'default=nw=1:nk=1', f], capture_output=True, text=True).stdout.split()
    a, b = r[0].split('/'); return float(a) / float(b), float(r[1])


items = []
for f in args:
    name = os.path.splitext(os.path.basename(f))[0]; fps, dur = probe(f); to = lim.get(name, dur)
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-vf', f'scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'],
                         capture_output=True).stdout
    F = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)
    d = np.array([np.abs(F[k] - F[k - 1]).mean() for k in range(1, len(F))]); T = np.arange(1, len(F)) / fps
    med = float(np.median(d)) or 1e-3
    top = sorted((float(T[k]), float(d[k] / med)) for k in np.argsort(-d)[:8] if T[k] <= to)
    clusters = []
    for t, v in top:
        if clusters and t - clusters[-1][-1][0] < 0.2: clusters[-1].append((t, v))
        else: clusters.append([(t, v)])
    for c in clusters:
        t, v = max(c, key=lambda x: x[1])
        png = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{max(0, t - 0.02):.3f}', '-i', f, '-frames:v', '1', '-f', 'image2pipe',
                              '-vcodec', 'png', '-'], capture_output=True).stdout
        items.append((f'{name} {t:.2f}s ×{v:.0f}', Image.open(io.BytesIO(png)).convert('RGB')))
    print(name, f'{len(F)} кадров, пики:', ', '.join(f'{max(c, key=lambda x: x[1])[0]:.2f} с' for c in clusters))

font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 28)
w, h = 640, 360
for k in range(0, len(items), 6):
    S = Image.new('RGB', (3 * w + 16, 2 * h + 8))
    for i, (lab, im) in enumerate(items[k:k + 6]):
        im.thumbnail((w, h)); x, y = (i % 3) * (w + 8), (i // 3) * (h + 8); S.paste(im, (x, y))
        dr = ImageDraw.Draw(S); dr.rectangle((x, y, x + len(lab) * 17 + 16, y + 40), fill=0); dr.text((x + 8, y + 4), lab, font=font, fill=(255, 220, 0))
    S.save(f'{out}/peaks_{k // 6}.jpg', quality=88)
print(f'{len(items)} кадров на {(len(items) + 5) // 6} листах в {out}/')
