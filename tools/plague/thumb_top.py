"""Story-scene thumbnail with the fixed channel layout: title top-centre (Cinzel), years below, soft dark top band.
The art is shifted down by `shift` px; the gap on top is filled with a blurred mirror of the top strip."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F = 'assets/fonts/Cinzel.ttf'
W = (246, 236, 214)

def make(src, out, name, years, col, shift=90, s1=104, s2=58):
    art = Image.open(src).convert('RGB').resize((1280, 720), Image.LANCZOS)
    im = Image.new('RGB', (1280, 720))
    if shift:
        strip = art.crop((0, 0, 1280, shift)).transpose(Image.FLIP_TOP_BOTTOM).filter(ImageFilter.GaussianBlur(18))
        im.paste(strip, (0, 0))
    body = art.crop((0, 0, 1280, 720 - shift))
    m = Image.new('L', body.size, 255); fd = min(80, shift)
    for y in range(fd): m.paste(int(255 * y / fd), (0, y, 1280, y + 1))
    im.paste(body, (0, shift), m)
    im = im.convert('RGBA')
    h = 270; g = Image.new('L', (1, h))
    for y in range(h): g.putpixel((0, y), int(225 * (1 - y / h) ** 1.5))
    band = Image.new('RGBA', (1280, h), (0, 0, 0, 255)); band.putalpha(g.resize((1280, h))); im.alpha_composite(band, (0, 0))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(F, s1)
    while f.getlength(name) > 1000: s1 -= 4; f = ImageFont.truetype(F, s1)
    d.text((640, 40), name, font=f, fill=W, anchor='mt', stroke_width=5, stroke_fill=(10, 8, 6))
    d.text((640, 40 + int(s1 * 1.12)), years, font=ImageFont.truetype(F, s2), fill=col, anchor='mt', stroke_width=4, stroke_fill=(10, 8, 6))
    im.convert('RGB').save(out, quality=93)
