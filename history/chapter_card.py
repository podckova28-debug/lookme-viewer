# Chapter title card in the reference style: bold rounded yellow text, thick black outline, red brush underline.
import sys, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
def card(bg, text, out, W=1920, H=1080):
    im = Image.open(bg).convert("RGB").resize((W, H))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype("/home/user/lookme-viewer/history/fonts/LilitaOne-Regular.ttf", 150)
    tw, th = d.textbbox((0, 0), text, font=f)[2:]
    x, y = (W - tw) // 2, int(H * 0.40)
    # red brush stroke under the text (slightly ragged)
    random.seed(len(text)); pts = []
    bx0, bx1, by = x - 30, x + tw + 30, y + th + 30
    brush = Image.new("RGBA", (W, H)); bd = ImageDraw.Draw(brush)
    for i in range(14):
        o = random.randint(-6, 6)
        bd.line([(bx0 + random.randint(0, 25), by + o), (bx1 - random.randint(0, 25), by + o + random.randint(-4, 4))], fill=(205, 30, 35, 235), width=10)
    brush = brush.filter(ImageFilter.GaussianBlur(0.8))
    im.paste(brush, (0, 0), brush)
    d = ImageDraw.Draw(im)
    d.text((x, y), text, font=f, fill=(255, 214, 0), stroke_width=12, stroke_fill=(0, 0, 0))
    im.save(out, quality=92)
if __name__ == "__main__":
    card(sys.argv[1], sys.argv[2], sys.argv[3])
