# Chapter title card in the reference style: bold rounded yellow text, thick black outline, red brush underline.
import sys, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
def card(bg, text, out, W=1920, H=1080):
    from PIL import ImageEnhance
    im = Image.open(bg).convert("RGB")
    sc = max(W / im.width, H / im.height); im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - H) // 2; im = im.crop((l, t, l + W, t + H))
    im = ImageEnhance.Brightness(im.filter(ImageFilter.GaussianBlur(3))).enhance(0.62)
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype("/home/user/lookme-viewer/history/fonts/LilitaOne-Regular.ttf", 170)
    tw, th = d.textbbox((0, 0), text, font=f)[2:]
    x, y = (W - tw) // 2, int(H * 0.40)
    # red brush stroke under the text (slightly ragged)
    random.seed(len(text)); pts = []
    bx0, bx1, by = x - 30, x + tw + 30, y + th + 22
    brush = Image.new("RGBA", (W, H)); bd = ImageDraw.Draw(brush)
    for i in range(22):
        o = random.randint(-11, 11)
        bd.line([(bx0 + random.randint(0, 30), by + o), (bx1 - random.randint(0, 30), by + o + random.randint(-5, 5))], fill=(205, 30, 35, 240), width=14)
    brush = brush.filter(ImageFilter.GaussianBlur(0.8))
    im.paste(brush, (0, 0), brush)
    d = ImageDraw.Draw(im)
    d.text((x, y), text, font=f, fill=(255, 214, 0), stroke_width=12, stroke_fill=(0, 0, 0))
    im.save(out, quality=92)
if __name__ == "__main__":
    card(sys.argv[1], sys.argv[2], sys.argv[3])
