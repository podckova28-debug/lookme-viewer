import sys; sys.path.insert(0, '.')
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import gfx
im = Image.open('thumb_base.png').convert('RGBA').resize((1280, 720), Image.LANCZOS)
lay = Image.new('RGBA', im.size, (0, 0, 0, 0))
def big(txt, x, y, size, fill, stroke=10):
    f = ImageFont.truetype(gfx.OSW_B, size)
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((x + 5, y + 8), txt, font=f, fill=(0, 0, 0, 160), stroke_width=stroke, stroke_fill=(0, 0, 0, 160))
    lay.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    ImageDraw.Draw(lay).text((x, y), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=gfx.INK)
big('10', 48, -6, 220, gfx.OCHRE, 12)
big('СОВЕТСКИХ', 48, 236, 112, gfx.CREAM)
big('ХИТРОСТЕЙ', 48, 360, 112, gfx.CREAM)
im = Image.alpha_composite(im, lay)
# штамп
st = gfx._stamp('РАБОТАЕТ?', None, gfx.RED).rotate(-12, resample=Image.BICUBIC, expand=True)
k = 150 / st.height * 1.25
st = st.resize((int(st.width * k), int(st.height * k)), Image.LANCZOS)
print(st.size)
im.alpha_composite(st, (36, 712 - st.height))
im.convert('RGB').save('thumb_sovhacks.jpg', quality=92)
print('ok')
