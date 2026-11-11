"""Thumbnail compositor: painted art + the channel's title style.

    python miniatura.py ART.png OUT.jpg "LINEA BLANCA" "LINEA AMARILLA" [--right] [--tag "EPISODIO 1"] [--maxw 600] [--angle 4]

Two short uppercase lines, top-left (or top-right with --right): the first white, the second yellow,
heavy sans with a dark outline and soft shadow, tilted a few degrees (rising to the right),
over a gentle darkening so it reads on any art.
Output is 1280x720 JPEG under YouTube's 2 MB limit.
"""
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT = '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
W, H = 1280, 720
WHITE, YELLOW, INK = (255, 255, 255), (255, 210, 31), (14, 10, 24)


def fit(draw, text, maxw, size):
    while size > 40:
        f = ImageFont.truetype(FONT, size)
        if draw.textlength(text, font=f) <= maxw: return f
        size -= 4
    return ImageFont.truetype(FONT, size)


def compose(art, out, lines, right=False, tag=None, maxw=600, angle=4.0):
    im = Image.open(art).convert('RGB')
    k = max(W / im.width, H / im.height); im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    im = im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width - W) // 2 + W, (im.height - H) // 2 + H)).convert('RGBA')
    # darken the text side so the title reads on any art
    shade = Image.new('L', (W, H), 0); sd = ImageDraw.Draw(shade)
    for x in range(W):
        u = (W - 1 - x) / W if right else x / W
        sd.line([(x, 0), (x, H)], fill=int(150 * max(0, 1 - u / .55) ** 1.6))
    im = Image.composite(Image.new('RGBA', (W, H), (8, 10, 30, 255)), im, shade)

    d = ImageDraw.Draw(im); y = 46 + (angle * 9 if not right else 0); x0 = W - 52 if right else 52
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
    shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); shd = ImageDraw.Draw(shadow)
    for i, text in enumerate(lines):
        f = fit(d, text, maxw, 132 if len(lines) > 1 else 150)
        tw = d.textlength(text, font=f); x = x0 - tw if right else x0
        asc, desc = f.getmetrics()
        shd.text((x + 8, y + 10), text, font=f, fill=(0, 0, 0, 200), stroke_width=12, stroke_fill=(0, 0, 0, 200))
        ld.text((x, y), text, font=f, fill=WHITE if i == 0 else YELLOW, stroke_width=11, stroke_fill=INK)
        y += int((asc + desc) * .9)
    # tilt the title block around its first-line anchor
    cx, cy = x0, 46 + 60
    shadow = shadow.rotate(angle, resample=Image.BICUBIC, center=(cx, cy))
    layer = layer.rotate(angle, resample=Image.BICUBIC, center=(cx, cy))
    im = Image.alpha_composite(im, shadow.filter(ImageFilter.GaussianBlur(10)))
    im = Image.alpha_composite(im, layer)
    if tag:
        f = ImageFont.truetype(FONT, 34); tw = d.textlength(tag, font=f); d = ImageDraw.Draw(im)
        bx = (W - 40 - tw - 36) if right else 40; by = H - 86
        d.rounded_rectangle((bx, by, bx + tw + 36, by + 54), 12, fill=(225, 29, 46), outline=INK, width=4)
        d.text((bx + 18, by + 7), tag, font=f, fill=WHITE)
    im.convert('RGB').save(out, quality=90, optimize=True)


if __name__ == '__main__':
    a = sys.argv[1:]; right = '--right' in a; opt = {}
    for k in ('--tag', '--maxw', '--angle'):
        if k in a: i = a.index(k); opt[k] = a[i + 1]; del a[i:i + 2]
    a = [s for s in a if s != '--right']
    compose(a[0], a[1], a[2:], right, opt.get('--tag'), int(opt.get('--maxw', 600)), float(opt.get('--angle', 4)))
