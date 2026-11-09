#!/usr/bin/env python3
"""Паузы внутри реплики — в два уровня, без parselmouth (numpy + ffmpeg).

    python pauses2.py in.(wav|mp3) out.wav [SENT=0.24] [COMMA=0.13]

Тишина: кадры 10 мс тише −35 дБ от пика реплики. Паузы внутри (края не трогаем — их срезает монтаж):
длиннее 0,35 с — это граница предложения, сжимаем до SENT; 0,16…0,35 с — запятая, сжимаем до COMMA.
Склейка с плавным переходом 15 мс. Зачем: у Alexey (MiniMax) паузы между предложениями 0,3–0,5 с и на запятых
до 0,5 с — пользователь: «поработай с паузками» (эп. 24)."""
import sys, subprocess
import numpy as np, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe(); SR = 44100
src, dst = sys.argv[1], sys.argv[2]
SENT = float(sys.argv[3]) if len(sys.argv) > 3 else 0.24
COMMA = float(sys.argv[4]) if len(sys.argv) > 4 else 0.13
raw = subprocess.run([FF, '-v', 'error', '-i', src, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
h = SR // 100; n = len(x) // h
db = 20 * np.log10(np.sqrt((x[:n * h].reshape(n, h) ** 2).mean(1)) + 1e-9)
q = db - db.max() < -35
voiced = np.flatnonzero(~q); first, last = voiced[0], voiced[-1] + 1
out, i, cut = [], 0, []
pos = 0
spans = []
k = first
while k < last:
    if q[k]:
        j = k
        while j < last and q[j]: j += 1
        spans.append((k, j)); k = j
    else: k += 1
fade = int(0.015 * SR)
res = [x[:first * h]]; prev = first * h
for a, b in spans:
    dur = (b - a) / 100
    keep = SENT if dur > 0.35 else COMMA if dur > 0.16 else None
    if keep is None or dur <= keep: continue
    A, B = a * h, b * h; kh = int(keep * SR / 2)
    seg = x[prev:A + kh].copy(); tail = x[B - kh:B].copy()
    if len(seg) > fade and len(tail) > fade:
        w = np.linspace(0, 1, fade)
        tail[:fade] = tail[:fade] * w + seg[-fade:] * (1 - w); seg = seg[:-fade]
    res += [seg, tail]; prev = B; cut.append(f'{a/100:.2f}:{dur:.2f}→{keep:.2f}')
res.append(x[prev:])
y = np.concatenate(res)
p = subprocess.run([FF, '-v', 'error', '-y', '-f', 's16le', '-ar', str(SR), '-ac', '1', '-i', '-', dst],
                   input=(np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
print(f'{src.split("/")[-1]}: {len(x)/SR:.2f} → {len(y)/SR:.2f} с · ' + (', '.join(cut) or 'паузы в норме'))
