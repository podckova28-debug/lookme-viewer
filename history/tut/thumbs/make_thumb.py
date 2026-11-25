# Tutankhamun thumbnail (ankh emblem). Rasputin-style title: heavy slab-serif (Alfa Slab One, squeezed horizontally) black with white outline,
# years below, black circle emblem with a white arrow and a white ring.
from PIL import Image, ImageDraw, ImageFont
import sys
F = "/home/user/lookme-viewer/history/fonts/AlfaSlabOne-Regular.ttf"
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB").resize((1920, 1080), Image.LANCZOS)
W, H = im.size
def layer(text, size, stroke, squeeze):
    f = ImageFont.truetype(F, size); d = ImageDraw.Draw(Image.new("L", (1, 1)))
    b = d.textbbox((0, 0), text, font=f, stroke_width=stroke)
    L = Image.new("RGBA", (b[2] - b[0] + 4, b[3] - b[1] + 4), (0, 0, 0, 0))
    ImageDraw.Draw(L).text((2 - b[0], 2 - b[1]), text, font=f, fill="black", stroke_width=stroke, stroke_fill="white")
    return L.resize((int(L.width * squeeze), L.height), Image.LANCZOS)
T = layer("TUTANKHAMUN", 300, 12, .78)
T = T.resize((int(W * .55), int(T.height * W * .55 / T.width)), Image.LANCZOS)
Y = layer("1341 – 1323 BC", 200, 10, .80)
Y = Y.resize((int(Y.width * T.height * .62 / Y.height), int(T.height * .62)), Image.LANCZOS)
x1 = int(W * .885); ty = int(H * .085)
im.paste(T, (x1 - T.width, ty), T)
im.paste(Y, (x1 - Y.width - int(W * .02), ty + T.height + int(H * .015)), Y)
r = int(T.height * .40); cx = x1 + int(W * .012) + r + 10; cy = ty + T.height // 2
S = 4
def mask(fn):
    m = Image.new("L", (W * S, H * S), 0); fn(ImageDraw.Draw(m)); return m.resize((W, H), Image.LANCZOS)
white = mask(lambda d: d.ellipse([(cx - r - 9) * S, (cy - r - 9) * S, (cx + r + 9) * S, (cy + r + 9) * S], fill=255))
black = mask(lambda d: d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=255))
t = r * .12
def cr(d):   # white ankh
    d.ellipse([(cx - r*.26) * S, (cy - r*.72) * S, (cx + r*.26) * S, (cy - r*.08) * S], fill=255)
    d.ellipse([(cx - r*.13) * S, (cy - r*.58) * S, (cx + r*.13) * S, (cy - r*.2) * S], fill=0)
    d.rectangle([(cx - r*.07) * S, (cy - r*.12) * S, (cx + r*.07) * S, (cy + r*.75) * S], fill=255)
    d.rectangle([(cx - r*.45) * S, (cy - r*.04) * S, (cx + r*.45) * S, (cy + r*.1) * S], fill=255)
cross = mask(cr)
im.paste((255, 255, 255), mask=white); im.paste((0, 0, 0), mask=black); im.paste((255, 255, 255), mask=cross)
im.save(out.replace('.jpg', '.png'))
im.resize((1280, 720), Image.LANCZOS).save(out, quality=92)
