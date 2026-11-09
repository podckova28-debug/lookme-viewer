import sys, os
from PIL import Image, ImageDraw, ImageFont
fs = sys.argv[2:]; out = sys.argv[1]
f = ImageFont.truetype('/home/user/gastronom/content-machine/video/fonts/Nunito-Black.ttf', 22)
th = []
for p in fs:
    im = Image.open(p).convert('RGB'); im.thumbnail((640, 360))
    c = Image.new('RGB', (640, 390), 'white'); c.paste(im, (0, 30)); ImageDraw.Draw(c).text((8, 4), os.path.basename(p), fill='black', font=f); th.append(c)
cols = 3; rows = (len(th) + 2) // 3
s = Image.new('RGB', (640 * cols, 390 * rows), 'white')
for i, t in enumerate(th): s.paste(t, ((i % 3) * 640, (i // 3) * 390))
s.save(out, quality=82)
