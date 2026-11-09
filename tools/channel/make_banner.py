"""YouTube banner 2560x1440: three comic panels inside the 423-px strip that
desktop shows (Dave | title | chaos), brand-yellow halftone everywhere else.
usage: make_banner.py ART.png OUT.png"""
import sys
from PIL import Image, ImageDraw, ImageFont

art = Image.open(sys.argv[1]).convert('RGB')
u = art.width / 1280  # crop boxes below are in 1280-wide units
W, H = 2560, 1440
Y0, Y1 = 512, 928          # panel strip (desktop shows 508..931)
YEL, INK = (254, 211, 5), (20, 20, 20)
FONT = 'assets/fonts/Bangers-Regular.ttf'

bg = Image.new('RGB', (W, H), YEL)
d = ImageDraw.Draw(bg)
for y in range(0, H, 28):              # light halftone
    for x in range((y // 28 % 2) * 14, W, 28):
        d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=(242, 196, 0))

def panel(box, x0, x1):
    c = art.crop(tuple(int(v * u) for v in box))
    h = Y1 - Y0
    c = c.resize((int(c.width * h / c.height), h), Image.LANCZOS)
    w = x1 - x0                         # crop to panel width, centred
    if c.width > w:
        off = (c.width - w) // 2
        c = c.crop((off, 0, off + w, h))
    bg.paste(c, (x0, Y0))
    d.rectangle((x0 - 8, Y0 - 8, x1 + 8, Y1 + 8), outline=INK, width=12)

panel((40, 205, 540, 585), 470, 1030)       # Dave on the couch
panel((700, 175, 1280, 555), 1540, 2090)    # upside-down guy, green arm, speed blur

# title panel
x0, x1 = 1062, 1508
d.rectangle((x0, Y0, x1, Y1), fill=(255, 255, 255))
d.rectangle((x0 - 8, Y0 - 8, x1 + 8, Y1 + 8), outline=INK, width=12)

def text(t, size, y, fill):
    f = ImageFont.truetype(FONT, size)
    while d.textlength(t, font=f) > (x1 - x0 - 40):
        size -= 4; f = ImageFont.truetype(FONT, size)
    tw = d.textlength(t, font=f)
    d.text(((x0 + x1 - tw) / 2, y), t, font=f, fill=fill, stroke_width=max(4, size // 14), stroke_fill=INK)

text('WHAT IF', 104, Y0 + 24, YEL)
text('YOU WOKE', 104, Y0 + 130, YEL)
text('UP AS...', 104, Y0 + 236, YEL)
f = ImageFont.truetype('assets/fonts/ComicNeue-Bold.ttf', 30)
t = 'New powers. Same Dave.'
d.text(((x0 + x1 - d.textlength(t, font=f)) / 2, Y1 - 46), t, font=f, fill=INK)
bg.save(sys.argv[2])
