"""Static story cards for ep01, drawn by code (no credits): newspaper front page, phone email, end card.

usage: python3 tools/still_cards.py OUTDIR DRIVER_PHOTO.png BG_FOR_END.png
"""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANG = os.path.join(ROOT, 'assets/fonts/Bangers-Regular.ttf')
NEUE = os.path.join(ROOT, 'assets/fonts/ComicNeue-Bold.ttf')
INK, PAPER, NEWS, YEL, RED = (20, 16, 18), (243, 233, 212), (236, 228, 208), (255, 226, 92), (214, 52, 40)
out, drv, bg = sys.argv[1:4]
F = lambda p, s: ImageFont.truetype(p, s)

# newspaper, 16:9 so it fills the panel
W, H = 1800, 1000
n = Image.new('RGB', (W, H), NEWS); d = ImageDraw.Draw(n)
d.text((W // 2, 70), 'THE DAILY HILL', font=F(BANG, 120), fill=INK, anchor='mm')
d.line((60, 140, W - 60, 140), fill=INK, width=6); d.line((60, 152, W - 60, 152), fill=INK, width=2)
d.text((70, 172), 'TUESDAY  ·  CITY EDITION  ·  25¢', font=F(NEUE, 30), fill=INK)
d.text((W // 2, 280), 'DRIVER STOPS RUNAWAY BUS', font=F(BANG, 132), fill=INK, anchor='mm')
d.text((W // 2, 380), '"I just went for a sandwich," says hero of the day', font=F(NEUE, 44), fill=INK, anchor='mm')
ph = Image.open(drv).convert('L').convert('RGB'); ph = ImageEnhance.Contrast(ph).enhance(1.25)
pw, phh = 900, 506; ph = ph.resize((pw, phh)); n.paste(ph, (70, 440)); d.rectangle((70, 440, 70 + pw, 440 + phh), outline=INK, width=5)
d.text((70, 956), 'Bus driver, at the scene.', font=F(NEUE, 28), fill=INK)
x0 = 1010
for i in range(15):
    y = 450 + i * 34; w = 720 if i % 5 != 4 else 430
    d.rectangle((x0, y, x0 + w, y + 14), fill=(150, 142, 126))
d.text((x0, 980 - 40), 'Also: strange white string on 5th St.  p.4', font=F(NEUE, 28), fill=INK)
n.save(f'{out}/news.png')

# phone with email
W, H = 1800, 1000
p = Image.new('RGB', (W, H), (52, 60, 84)); d = ImageDraw.Draw(p)
px0, py0, px1, py1 = 640, 40, 1160, 960
d.rounded_rectangle((px0 + 12, py0 + 12, px1 + 12, py1 + 12), 60, fill=(0, 0, 0))
d.rounded_rectangle((px0, py0, px1, py1), 60, fill=INK)
sx0, sy0, sx1, sy1 = px0 + 24, py0 + 24, px1 - 24, py1 - 24
d.rounded_rectangle((sx0, sy0, sx1, sy1), 40, fill=(250, 248, 242))
d.text(((sx0 + sx1) // 2, sy0 + 40), '6:00 PM', font=F(NEUE, 34), fill=INK, anchor='mm')
d.text((sx0 + 34, sy0 + 110), 'Inbox', font=F(BANG, 60), fill=INK)
d.rectangle((sx0 + 20, sy0 + 200, sx1 - 20, sy0 + 560), fill=(255, 244, 196), outline=INK, width=4)
d.text((sx0 + 44, sy0 + 222), 'HR Team', font=F(NEUE, 36), fill=INK)
d.text((sx0 + 44, sy0 + 272), 'Your application', font=F(NEUE, 32), fill=INK)
body = ['Thank you for coming in', 'today. Unfortunately, we', 'went with another', 'candidate.', '', 'Best of luck!']
for i, s in enumerate(body): d.text((sx0 + 44, sy0 + 330 + i * 36), s, font=F(NEUE, 28), fill=(70, 64, 60))
for i in range(3):
    y = sy0 + 600 + i * 90
    d.rectangle((sx0 + 20, y, sx1 - 20, y + 70), outline=(200, 194, 180), width=3)
    d.rectangle((sx0 + 44, y + 18, sx0 + 280, y + 32), fill=(200, 194, 180)); d.rectangle((sx0 + 44, y + 42, sx0 + 380, y + 52), fill=(220, 214, 200))
p.save(f'{out}/email.png')

# end card: blurred dark frame + DAY 2
b = Image.open(bg).convert('RGB').resize((1800, 1000)).filter(ImageFilter.GaussianBlur(6)); b = ImageEnhance.Brightness(b).enhance(0.4)
d = ImageDraw.Draw(b)
d.text((900, 380), 'DAY 2', font=F(BANG, 300), fill=YEL, stroke_width=14, stroke_fill=INK, anchor='mm')
d.text((900, 590), 'AS SPIDER-MAN', font=F(BANG, 120), fill=(255, 255, 255), stroke_width=8, stroke_fill=INK, anchor='mm')
d.rounded_rectangle((640, 720, 1160, 840), 26, fill=RED, outline=INK, width=6)
d.text((900, 780), 'SUBSCRIBE', font=F(BANG, 84), fill=(255, 255, 255), stroke_width=5, stroke_fill=INK, anchor='mm')
b.save(f'{out}/end.png')
print('ok')
