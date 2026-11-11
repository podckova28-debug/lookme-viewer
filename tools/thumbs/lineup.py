import sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
S = sys.argv[1]; out = sys.argv[2]
W, H = 1280, 720
CR = (182, 16, 30); INK = (14, 12, 11); CREAM = (244, 236, 216)
def font(sz):
    f = ImageFont.truetype(S + "/thumb/Oswald.ttf", sz); f.set_variation_by_name("Bold"); return f
im = Image.new("RGB", (W, H), INK)
TOP = 0; tw = W // 4
for i in range(4):
    s = Image.open(f"{S}/ctr/L{i+1}.png").convert("RGB")
    w, h = s.size
    ch = int(h * 0.62); cw = int(ch * tw / H)
    crop = s.crop(((w - cw) // 2, int(h * 0.02), (w - cw) // 2 + cw, int(h * 0.02) + ch)).resize((tw, H), Image.LANCZOS)
    crop = ImageEnhance.Contrast(crop).enhance(1.25)
    im.paste(crop, (i * tw, 0))
d = ImageDraw.Draw(im)
for i in range(1, 4): d.rectangle((i * tw - 4, 0, i * tw + 4, H), fill=INK)
# dark bottom gradient for the headline
g = Image.new("L", (W, H), 0); gd = ImageDraw.Draw(g)
for y in range(H - 330, H): gd.line((0, y, W, y), fill=int(235 * (y - (H - 330)) / 330))
im.paste(Image.new("RGB", (W, H), INK), (0, 0), g)
d = ImageDraw.Draw(im)
f1 = font(118); s1 = "КТО ИЗ НИХ"
f2 = font(132); s2 = "МАНЬЯК?"
w1 = d.textlength(s1, font=f1); w2 = d.textlength(s2, font=f2)
bb1 = d.textbbox((0, 0), s1, font=f1); bb2 = d.textbbox((0, 0), s2, font=f2)
total = w1 + 30 + w2 + 60
x = (W - total) / 2; y = H - 175
d.text((x, y - bb1[1] + 10), s1, font=f1, fill=CREAM)
bx = x + w1 + 30
d.rectangle((bx, y - 10, bx + w2 + 60, y + (bb2[3] - bb2[1]) + 40), fill=CR)
d.text((bx + 30, y + 14 - bb2[1]), s2, font=f2, fill=CREAM)
im.save(out, quality=93)
