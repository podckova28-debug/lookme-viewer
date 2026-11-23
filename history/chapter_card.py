# On-screen text in the reference style (Archive in Minutes): ALL CAPS, white fill, black outline, soft drop shadow,
# hand-drawn red brush stroke under the words, over the undimmed illustration.
#   card()    - chapter title, large, centred
#   caption() - key fact (name / date / number), top centre, smaller
import sys, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
FONTS = "/home/user/lookme-viewer/history/fonts/"
FONT = FONTS + "Bangers-Regular.ttf"
RED = (229, 57, 53)

def _cover(bg, W, H):
    im = Image.open(bg).convert("RGB")
    sc = max(W / im.width, H / im.height); im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((l, t, l + W, t + H)).convert("RGBA")

def draw_text(im, text, size, cy, font=None, fill=(255, 255, 255), stroke=None, brush=True, maxw=0.88):
    font = font or FONT; W, H = im.size; text = text.upper()
    while True:
        f = ImageFont.truetype(font, size); st = stroke or max(4, size // 14)
        x0, y0, x1, y1 = ImageDraw.Draw(im).textbbox((0, 0), text, font=f, stroke_width=st)
        if x1 - x0 <= W * maxw or size < 40: break
        size -= 4
    x, y = (W - (x1 - x0)) // 2 - x0, int(cy - (y1 - y0) / 2) - y0
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

def card(bg, text, out, W=1920, H=1080, font=None):
    im = _cover(bg, W, H); draw_text(im, text, 190, H * .42, font=font, maxw=.86); im.convert("RGB").save(out, quality=92)

def caption(bg, text, out, W=1920, H=1080, font=None):
    im = _cover(bg, W, H); draw_text(im, text, 110, H * .13, font=font, maxw=.9); im.convert("RGB").save(out, quality=92)

if __name__ == "__main__":
    card(sys.argv[1], sys.argv[2], sys.argv[3])
