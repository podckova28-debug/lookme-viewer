# Chapter title card in the reference style (Archive in Minutes): ALL CAPS comic block lettering (Luckiest Guy, Apache 2.0),
# yellow fill, thick black outline, soft offset drop shadow, red marker/brush stroke under the text, over the dimmed chapter frame.
import sys, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
FONT = "/home/user/lookme-viewer/history/fonts/LuckiestGuy-Regular.ttf"
def card(bg, text, out, W=1920, H=1080, fill=(255, 214, 0)):
    text = text.upper()
    im = Image.open(bg).convert("RGB")
    sc = max(W / im.width, H / im.height); im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - H) // 2; im = im.crop((l, t, l + W, t + H))
    im = ImageEnhance.Brightness(im.filter(ImageFilter.GaussianBlur(3))).enhance(0.62).convert("RGBA")
    size = 165
    while True:
        f = ImageFont.truetype(FONT, size)
        x0, y0, x1, y1 = ImageDraw.Draw(im).textbbox((0, 0), text, font=f, stroke_width=12)
        if x1 - x0 <= W * 0.86 or size < 90: break
        size -= 5
    tw, th = x1 - x0, y1 - y0
    x, y = (W - tw) // 2 - x0, int(H * 0.36) - y0
    # red brush stroke behind the lower part of the letters
    random.seed(len(text)); brush = Image.new("RGBA", (W, H)); bd = ImageDraw.Draw(brush)
    bx0, bx1, by = x + x0 - 40, x + x1 + 40, y + y1 - 8
    for i in range(26):
        o = random.randint(-16, 16)
        bd.line([(bx0 + random.randint(0, 35), by + o), (bx1 - random.randint(0, 35), by + o + random.randint(-6, 6))],
                fill=(205, 30, 35, 245), width=16)
    im.alpha_composite(brush.filter(ImageFilter.GaussianBlur(0.8)))
    # soft offset drop shadow
    sh = Image.new("RGBA", (W, H)); ImageDraw.Draw(sh).text((x + 10, y + 12), text, font=f, fill=(0, 0, 0, 170), stroke_width=12, stroke_fill=(0, 0, 0, 170))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    ImageDraw.Draw(im).text((x, y), text, font=f, fill=fill, stroke_width=12, stroke_fill=(0, 0, 0))
    im.convert("RGB").save(out, quality=92)
if __name__ == "__main__":
    card(sys.argv[1], sys.argv[2], sys.argv[3])
