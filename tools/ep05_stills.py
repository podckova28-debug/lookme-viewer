"""Ep5 insert cards: text on the blank phone screen (S1) and on the examiner's form (S2).
usage: python3 tools/ep05_stills.py OUTDIR"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
HAND = 'assets/fonts/ComicNeue-Bold.ttf'

# S1: phone, same layout as the phone inserts of ep2 and ep4
im = Image.open('assets/ep05/keys/S1.png').convert('RGB').resize((1920, 1080), Image.LANCZOS)
a = np.array(im).astype(int); ys, xs = np.where(a.min(axis=2) > 235)
x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max(); w = x1 - x0
d = ImageDraw.Draw(im); cy = y0 + (y1 - y0) * 0.26
for t, col, sc in [('TODAY', (120, 120, 130), 0.10), ('10:00 AM', (30, 30, 40), 0.145), ('DRIVING', (220, 40, 60), 0.13),
                   ('TEST', (220, 40, 60), 0.13), ('Attempt #5', (30, 30, 40), 0.11)]:
    f = ImageFont.truetype(B, int(w * sc)); tw = d.textlength(t, font=f)
    d.text((x0 + (w - tw) / 2, cy), t, font=f, fill=col); cy += int(w * sc * 1.35)
im.save(os.path.join(OUT, 'S1.png'))

# S2: the form on the clipboard (coordinates measured on the 2688x1520 key)
im = Image.open('assets/ep05/keys/S2.png').convert('RGB'); d = ImageDraw.Draw(im)
INK, BLK, GRN = (28, 48, 140), (30, 30, 36), (30, 140, 60)
def c(text, y, font, size, fill, x0=1000, x1=1770):
    f = ImageFont.truetype(font, size); tw = d.textlength(text, font=f); d.text((x0 + (x1 - x0 - tw) / 2, y), text, font=f, fill=fill)
c('DRIVING TEST', 318, B, 84, BLK)
c('Attempt: #5', 478, HAND, 78, INK)
d.text((1140, 700), 'Parking: EXCELLENT', font=ImageFont.truetype(HAND, 72), fill=INK)
d.text((1136, 860), 'Result: PASS', font=ImageFont.truetype(HAND, 78), fill=INK)
for bx, by in ((980, 744), (966, 904)):                      # check marks in the two boxes
    d.line([(bx + 14, by + 44), (bx + 44, by + 76), (bx + 104, by - 16)], fill=GRN, width=16, joint='curve')
d.line([(1100, 1150), (1160, 1090), (1200, 1160), (1260, 1080), (1310, 1150), (1400, 1120), (1560, 1140)], fill=INK, width=9, joint='curve')
im.resize((1920, 1086), Image.LANCZOS).crop((0, 3, 1920, 1083)).save(os.path.join(OUT, 'S2.png'))
