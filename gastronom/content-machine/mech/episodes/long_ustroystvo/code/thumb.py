from PIL import Image, ImageDraw, ImageFont, ImageFilter
FONT = '/home/user/gastronom/content-machine/video/fonts/Nunito-Black.ttf'
INK = (43, 33, 24); CREAM = (255, 248, 232); OR = (236, 122, 32)
im = Image.open('thumb_base2.png').convert('RGBA').resize((1280, 720), Image.LANCZOS)
lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
def big(txt, x, y, size, fill, stroke=12):
    f = ImageFont.truetype(FONT, size)
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((x + 6, y + 8), txt, font=f, fill=(0, 0, 0, 150), stroke_width=stroke, stroke_fill=(0, 0, 0, 150))
    lay.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)))
    ImageDraw.Draw(lay).text((x, y), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=INK)
big('КАК УСТРОЕНА', 34, 18, 104, CREAM)
big('МАШИНА', 34, 130, 132, OR, 14)
# плашка «за 8 минут»
f = ImageFont.truetype(FONT, 46); t = 'ЗА 8 МИНУТ'
w = d.textlength(t, font=f); x0, y0 = 44, 292
d.rounded_rectangle((x0, y0, x0 + w + 44, y0 + 70), 22, fill=CREAM, outline=INK, width=6)
d.text((x0 + 22, y0 + 35), t, font=f, fill=INK, anchor='lm')
out = Image.alpha_composite(im, lay).convert('RGB')
out.save('thumb_long_ustroystvo.jpg', quality=92)
out.resize((640, 360)).save('qa/thumb_final_small.jpg')
print('ok')
