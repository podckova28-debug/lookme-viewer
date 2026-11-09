#!/usr/bin/env python3
"""S05c: огонь вылезал над головкой цилиндра. Всё вне внутренней полости (выше купола камеры, стенки, фон)
берём из первого кадра клипа (там чисто); внутри цилиндра и картера — сам клип."""
import subprocess, numpy as np, imageio_ffmpeg, os, shutil
from PIL import Image, ImageDraw, ImageFilter
FF = imageio_ffmpeg.get_ffmpeg_exe()
src = 'mclips/S05c_raw.mp4'
if not os.path.exists(src): shutil.move('mclips/S05c.mp4', src)
W, H, OX = 864, 496, 232
m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
X = lambda x: x + OX
# цилиндр: от купола камеры вниз; купол — по линии головки
d.polygon([(X(114), 114), (X(150), 101), (X(200), 90), (X(250), 101), (X(290), 114), (X(290), 300), (X(114), 300)], fill=255)
# картер
d.rounded_rectangle((X(90), 272, X(316), 474), 30, fill=255)
m = m.filter(ImageFilter.GaussianBlur(1.5))
M = (np.asarray(m, np.float32) / 255)[..., None]
raw = subprocess.run([FF, '-v', 'error', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).astype(np.float32)
static = fr[0]
out = (fr * M + static * (1 - M)).clip(0, 255).astype(np.uint8)
enc = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24', '-i', '-',
                        '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', 'mclips/S05c.mp4'], stdin=subprocess.PIPE)
enc.stdin.write(out.tobytes()); enc.stdin.close(); enc.wait()
print(len(fr), 'кадров')
