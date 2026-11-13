"""Title overlay for story-scene thumbnails: Cinzel, cream + coloured years, soft dark halo, safe margins."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F = 'assets/fonts/Cinzel.ttf'
W = (246, 236, 214)

def title(src, out, name, years, col, cx, y0, maxw, s1=120, s2=72, gap=1.08, margin=72):
    im = Image.open(src).convert('RGB').resize((1280, 720), Image.LANCZOS).convert('RGBA')
    items, y = [], y0
    for txt, size, c in [(name, s1, W), (years, s2, col)]:
        f = ImageFont.truetype(F, size)
        while f.getlength(txt) > maxw: size -= 4; f = ImageFont.truetype(F, size)
        items.append((txt, f, c, y, size)); y += int(size * gap)
    # keep the whole block inside safe margins
    half = max(f.getlength(t) for t, f, *_ in items) / 2
    cx = min(max(cx, margin + half), 1280 - margin - half); y0 = max(y0, margin * 0.75)
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    for t, f, c, y, size in items: ds.text((cx, y), t, font=f, fill=(0, 0, 0, 235), anchor='mt', stroke_width=size // 5, stroke_fill=(0, 0, 0, 235))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(14))); d = ImageDraw.Draw(im)
    for t, f, c, y, size in items: d.text((cx, y), t, font=f, fill=c, anchor='mt', stroke_width=max(4, size // 16), stroke_fill=(10, 8, 6))
    im.convert('RGB').save(out, quality=93)
    return y
