import sys, os
from PIL import Image, ImageDraw, ImageFont
names = sys.argv[2:]; out = sys.argv[1]; W = 640; H = 360
s = Image.new('RGB', (W * 3 + 20, (H + 6) * ((len(names) + 2) // 3)), (0, 0, 0))
f = ImageFont.truetype('/home/user/gastronom/content-machine/mech/covers/fonts/DelaGothicOne.ttf', 26)
for i, n in enumerate(names):
    im = Image.open(f'kf/{n}.png').convert('RGB').resize((W, H)); d = ImageDraw.Draw(im)
    d.text((10, 8), n, font=f, fill=(255, 255, 0), stroke_width=3, stroke_fill=(0, 0, 0))
    s.paste(im, ((i % 3) * (W + 10), (i // 3) * (H + 6)))
s.save(out, quality=86)
