"""Сравнение: тот же кадр клипа, кусок 1:1 из 1080p — слева простое растягивание, справа ИИ-апскейл."""
import subprocess, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
m, t, cx, cy = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
def frame(f):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', f, '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                         capture_output=True).stdout
    return Image.frombytes('RGB', (1920, 1080), raw)
cw, ch = 760, 620; x0 = int(cx * 1920 - cw / 2); y0 = int(cy * 1080 - ch / 2)
a = frame(f'clips/{m}.mp4').crop((x0, y0, x0 + cw, y0 + ch)); b = frame(f'clips/ai/{m}.mp4').crop((x0, y0, x0 + cw, y0 + ch))
out = Image.new('RGB', (cw * 2 + 20, ch + 90), (20, 20, 20)); out.paste(a, (0, 90)); out.paste(b, (cw + 20, 90))
d = ImageDraw.Draw(out); f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 40)
d.text((cw / 2, 45), 'Было: растянуто', font=f, fill=(230, 230, 230), anchor='mm')
d.text((cw * 1.5 + 20, 45), 'Стало: ИИ-апскейл', font=f, fill=(255, 200, 80), anchor='mm')
out.save(f'work/compare_{m}.jpg', quality=92); print(f'work/compare_{m}.jpg')
