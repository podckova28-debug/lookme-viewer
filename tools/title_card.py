"""Series title insert: last frame of the previous block frozen, darkened, slow push-in, comic title lettering.

usage: python3 tools/title_card.py PREV_BLOCK.mp4 OUT.mp4 [secs]
"""
import sys, os, subprocess, tempfile, math
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANG = os.path.join(ROOT, 'assets/fonts/Bangers-Regular.ttf')
INK = (20, 16, 18)
src, out = sys.argv[1], sys.argv[2]; secs = float(sys.argv[3]) if len(sys.argv) > 3 else 2.5
tmp = tempfile.mkdtemp()
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-sseof', '-0.1', '-i', src, '-frames:v', '1', f'{tmp}/last.png'], check=True)
base = Image.open(f'{tmp}/last.png').convert('RGB').resize((1920, 1080))
base = ImageEnhance.Brightness(base.filter(ImageFilter.GaussianBlur(3))).enhance(0.45)
f1 = ImageFont.truetype(BANG, 96); f2 = ImageFont.truetype(BANG, 250)
n = int(secs * 24)
def eb(t):
    t = max(0, min(1, t)); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2
for i in range(n):
    t = i / 24
    z = 1 + 0.04 * t / secs
    fr = base.resize((int(1920 * z), int(1080 * z)), Image.LANCZOS)
    l, u = (fr.width - 1920) // 2, (fr.height - 1080) // 2
    fr = fr.crop((l, u, l + 1920, u + 1080)); d = ImageDraw.Draw(fr)
    k1 = eb(t / 0.3); k2 = eb((t - 0.25) / 0.35)
    d.text((960 - (1 - k1) * 1400, 360), 'WHAT IF YOU WOKE UP AS', font=f1, fill=(255, 255, 255), stroke_width=8, stroke_fill=INK, anchor='mm')
    if t > 0.25:
        s = 0.6 + 0.4 * k2
        f2s = ImageFont.truetype(BANG, max(10, int(250 * s)))
        d.text((960, 560), 'SPIDER-MAN?', font=f2s, fill=(255, 214, 56), stroke_width=int(14 * s), stroke_fill=INK, anchor='mm')
    fr.save(f'{tmp}/{i:04d}.png')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', '24', '-i', f'{tmp}/%04d.png', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
                '-shortest', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-c:a', 'aac', out], check=True)
print('ok', out)
