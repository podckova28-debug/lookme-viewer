# On-screen text in the reference style (Archive in Minutes): ALL CAPS, white fill, black outline, soft drop shadow,
# hand-drawn red brush stroke under the words, over the undimmed illustration.
#   card()    - chapter title, large, centred
#   caption() - key fact (name / date / number), top centre, smaller
import sys, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
FONTS = "/home/user/lookme-viewer/history/fonts/"
FONT = FONTS + "BebasNeue-Regular.ttf"
RED = (229, 57, 53)

def _cover(bg, W, H):
    im = Image.open(bg).convert("RGB")
    sc = max(W / im.width, H / im.height); im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((l, t, l + W, t + H)).convert("RGBA")

def draw_text(im, text, size, cy, font=None, fill=(255, 255, 255), stroke=None, brush=True, maxw=0.88, cx=None):
    font = font or FONT; W, H = im.size; text = text.upper()
    while True:
        f = ImageFont.truetype(font, size); st = stroke or max(4, size // 14)
        x0, y0, x1, y1 = ImageDraw.Draw(im).textbbox((0, 0), text, font=f, stroke_width=st)
        if x1 - x0 <= W * maxw or size < 40: break
        size -= 4
    cx = W / 2 if cx is None else cx
    x, y = int(cx - (x1 - x0) / 2) - x0, int(cy - (y1 - y0) / 2) - y0
    if brush:   # ragged red marker stroke under the words, slightly tilted
        random.seed(text); b = Image.new("RGBA", im.size); bd = ImageDraw.Draw(b)
        bx0, bx1, by = x + x0 - size * .15, x + x1 + size * .15, y + y1 + size * .02
        tilt = random.uniform(-1, 1) * size * .06; wd = max(6, size // 9)
        for i in range(24):
            o = random.uniform(-1, 1) * wd * .9
            bd.line([(bx0 + random.uniform(0, size * .2), by + o - tilt), (bx1 - random.uniform(0, size * .2), by + o + tilt)],
                    fill=RED + (240,), width=wd)
        im.alpha_composite(b.filter(ImageFilter.GaussianBlur(0.8)))
    sh = Image.new("RGBA", im.size); off = max(4, size // 18)
    ImageDraw.Draw(sh).text((x + off, y + off), text, font=f, fill=(0, 0, 0, 160), stroke_width=st, stroke_fill=(0, 0, 0, 160))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(max(3, size // 30))))
    ImageDraw.Draw(im).text((x, y), text, font=f, fill=fill, stroke_width=st, stroke_fill=(0, 0, 0))
    return im

def text_size(text, size, font=None, W=1920, maxw=0.9):
    font = font or FONT; text = text.upper(); d = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    while True:
        f = ImageFont.truetype(font, size); st = max(4, size // 14)
        x0, y0, x1, y1 = d.textbbox((0, 0), text, font=f, stroke_width=st)
        if x1 - x0 <= W * maxw or size < 40: return x1 - x0, y1 - y0, size
        size -= 4

def best_spot(im, text, size=104):
    """Pick where the caption hides the least detail: top or bottom band, left / centre / right.
    Detail = edge density + skin-tone pixels (faces, hands), measured on the caption box plus a margin."""
    import numpy as np
    W, H = im.size; tw, th, size = text_size(text, size)
    a = np.asarray(im.convert("RGB").resize((W // 4, H // 4)), dtype=np.float32)
    g = a.mean(2); e = np.abs(np.diff(g, axis=0))[:, :-1] + np.abs(np.diff(g, axis=1))[:-1, :]
    r, gg, b = a[..., 0], a[..., 1], a[..., 2]
    skin = ((r > 150) & (r > gg + 15) & (gg > b + 5) & (r - b > 35) & (r - b < 120)).astype(np.float32)[:-1, :-1]
    best = None
    for cy, ybias in ((H * .12, 0), (H * .87, .08)):
        for cx, xbias in ((W / 2, 0), (60 + tw / 2 + 20, .04), (W - 60 - tw / 2 - 20, .04)):
            if cx - tw / 2 < 40 or cx + tw / 2 > W - 40: continue
            x0, x1 = int((cx - tw / 2 - 30) / 4), int((cx + tw / 2 + 30) / 4)
            y0, y1 = int((cy - th / 2 - 25) / 4), int((cy + th / 2 + 40) / 4)
            sc = e[y0:y1, x0:x1].mean() / 30 + 2.5 * skin[y0:y1, x0:x1].mean() + ybias + xbias
            if best is None or sc < best[0]: best = (sc, cx, cy)
    return best[1], best[2], size

def card(bg, text, out, W=1920, H=1080, font=None):
    im = _cover(bg, W, H); draw_text(im, text, 190, H * .42, font=font, maxw=.86); im.convert("RGB").save(out, quality=92)

def caption(bg, text, out, W=1920, H=1080, font=None):
    im = _cover(bg, W, H); draw_text(im, text, 110, H * .13, font=font, maxw=.9); im.convert("RGB").save(out, quality=92)

if __name__ == "__main__":
    card(sys.argv[1], sys.argv[2], sys.argv[3])
