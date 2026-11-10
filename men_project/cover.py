import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = sys.argv[1]; base, out = sys.argv[2], sys.argv[3]; lines = sys.argv[4].split("|"); block = sys.argv[5]
W, H = 1280, 720
CR = (182, 16, 30); INK = (14, 12, 11); CREAM = (244, 236, 216)
def font(sz):
    f = ImageFont.truetype(S + "/thumb/Oswald.ttf", sz); f.set_variation_by_name("Bold"); return f
src = Image.open(base).convert("RGB").resize((W, H), Image.LANCZOS)
SHIFT = int(sys.argv[6]) if len(sys.argv) > 6 else 140
im = Image.new("RGB", (W, H)); im.paste(src, (SHIFT, 0))
im.paste(src.crop((0, 0, SHIFT, H)).transpose(Image.FLIP_LEFT_RIGHT), (0, 0))  # left strip: plain paper
d = ImageDraw.Draw(im)
X, MAXW = 44, 470
def fit(s, sz):
    f = font(sz)
    while d.textlength(s, font=f) > MAXW and sz > 40: sz -= 4; f = font(sz)
    return f
items = [(l, fit(l, 150), "ink") for l in lines] + [(block, fit(block, 150), "block")]
hs = []
for s, f, kind in items:
    bb = d.textbbox((0, 0), s, font=f); hs.append(bb[3] - bb[1] + (34 if kind == "block" else 6))
total = sum(hs) + 10 * (len(items) - 1)
y = (H - total) / 2
for (s, f, kind), h in zip(items, hs):
    bb = d.textbbox((0, 0), s, font=f); tw = d.textlength(s, font=f)
    if kind == "block":
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
        sd.rectangle((X + 8, y + 10, X + tw + 44, y + h + 10), fill=(0, 0, 0, 120)); sh = sh.filter(ImageFilter.GaussianBlur(6))
        im.paste(sh, (0, 0), sh); d = ImageDraw.Draw(im)
        d.rectangle((X - 4, y, X + tw + 36, y + h), fill=CR)
        d.text((X + 16, y + 17 - bb[1]), s, font=f, fill=CREAM)
    else:
        d.text((X, y - bb[1]), s, font=f, fill=INK)
    y += h + 10
im.save(out, quality=93)
