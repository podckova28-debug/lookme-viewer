"""YouTube thumbnail 1280x720 from a frame: punchier colour, crop, 2-3 words of comic lettering.

usage: python3 tools/thumb.py FRAME.png OUT.png "TEXT LINE 1" ["LINE 2"] --crop x,y,w,h --pos left|right --color yellow|white
"""
import sys, os, argparse
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANG = os.path.join(ROOT, 'assets/fonts/Bangers-Regular.ttf')
COL = {'yellow': (255, 214, 56), 'white': (255, 255, 255), 'red': (232, 60, 46)}

ap = argparse.ArgumentParser()
ap.add_argument('frame'); ap.add_argument('out'); ap.add_argument('lines', nargs='+')
ap.add_argument('--crop', default=None); ap.add_argument('--pos', default='left'); ap.add_argument('--color', default='yellow')
ap.add_argument('--size', type=int, default=150)
a = ap.parse_args()

im = Image.open(a.frame).convert('RGB')
if a.crop:
    x, y, w, h = map(int, a.crop.split(',')); im = im.crop((x, y, x + w, y + h))
im = im.resize((1280, 720), Image.LANCZOS)
im = ImageEnhance.Color(im).enhance(1.25); im = ImageEnhance.Contrast(im).enhance(1.12)
im = im.filter(ImageFilter.UnsharpMask(2, 80, 2))
d = ImageDraw.Draw(im)
f = ImageFont.truetype(BANG, a.size)
y = 40
for i, line in enumerate(a.lines):
    tw = f.getlength(line)
    x = 48 if a.pos == 'left' else 1280 - 48 - tw
    col = COL[a.color] if i == 0 else COL['white']
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    sd.text((x + 8, y + 10), line, font=f, fill=(0, 0, 0, 170), stroke_width=12, stroke_fill=(0, 0, 0, 170))
    im.paste(sh.filter(ImageFilter.GaussianBlur(6)), (0, 0), sh.filter(ImageFilter.GaussianBlur(6)))
    d = ImageDraw.Draw(im)
    d.text((x, y), line, font=f, fill=col, stroke_width=11, stroke_fill=(20, 16, 18))
    y += int(a.size * 0.95)
im.save(a.out)
