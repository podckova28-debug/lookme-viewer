"""Thumbnail lettering in the channel style (ep01 F1 / ep03 A): heavy white + yellow lines, thick black outline, soft shadow.
usage: python3 tools/thumb2.py ART.png OUT.jpg --line "TEXT:white" --line "TEXT:yellow" --x 1240 --y 60 --size 120 [--align right|left]"""
import argparse
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
ap = argparse.ArgumentParser(); ap.add_argument('art'); ap.add_argument('out'); ap.add_argument('--line', action='append')
ap.add_argument('--x', type=int, default=1240); ap.add_argument('--y', type=int, default=50); ap.add_argument('--size', type=int, default=130)
ap.add_argument('--align', default='right'); a = ap.parse_args()
F = '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
COL = {'white': (255, 255, 255), 'yellow': (255, 214, 0)}
im = Image.open(a.art).convert('RGB').resize((1280, 720), Image.LANCZOS)
im = ImageEnhance.Color(im).enhance(1.15); im = ImageEnhance.Contrast(im).enhance(1.08)
y = a.y
for spec in a.line:
    txt, col = spec.rsplit(':', 1); sz = a.size
    f = ImageFont.truetype(F, sz); tw = f.getlength(txt)
    x = a.x - tw if a.align == 'right' else a.x
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((x + 6, y + 9), txt, font=f, fill=(0, 0, 0, 200), stroke_width=16, stroke_fill=(0, 0, 0, 200))
    sh = sh.filter(ImageFilter.GaussianBlur(7)); im.paste(sh, (0, 0), sh)
    ImageDraw.Draw(im).text((x, y), txt, font=f, fill=COL[col], stroke_width=13, stroke_fill=(16, 12, 14))
    y += int(sz * 1.08)
im.save(a.out, quality=92); print(a.out)
