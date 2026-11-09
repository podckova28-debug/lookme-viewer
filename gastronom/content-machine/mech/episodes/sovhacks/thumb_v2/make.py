"""Обложки длинного ролика «10 советских гаражных хитростей»: база без текста (gpt_image_2_5) + текст кодом.
python make.py — собирает все варианты из VARIANTS в out/ и лист превью qa/sheet.jpg (как в ленте телефона)."""
import os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D = os.path.dirname(os.path.abspath(__file__))
DELA = '/home/user/gastronom/content-machine/mech/covers/fonts/DelaGothicOne.ttf'
OSW = '/tmp/claude-0/-home-user-lookme-viewer/8420a68c-a72b-5ef9-9faf-653836f3526a/scratchpad/sovhacks/fonts/Oswald_wght_700.ttf'
W, H = 1280, 720
YEL, WHITE, INK, RED, GREEN = (255, 222, 23), (255, 255, 255), (16, 16, 20), (226, 38, 38), (40, 170, 70)

def fit(text, maxw, size, font=None):
    font = font or OSW
    while size > 20:
        f = ImageFont.truetype(font, size)
        if f.getlength(text) <= maxw: return f
        size -= 2
    return ImageFont.truetype(font, size)

def headline(im, lines, x, y, maxw, angle=-4, gap=0.0):
    """lines: [(текст, цвет, кегль)] — каждая строка подгоняется по ширине maxw; обводка и мягкая тень."""
    lay = Image.new('RGBA', (W * 2, H * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    cy = 40
    for text, col, size in lines:
        f = fit(text, maxw * 2, size * 2); sw = max(12, f.size // 11)
        d.text((40, cy), text, font=f, fill=col, stroke_width=sw, stroke_fill=INK)
        bb = d.textbbox((40, cy), text, font=f, stroke_width=sw)
        cy = bb[3] - int(f.size * 0.13) + int(f.size * gap)
    bb = lay.getbbox(); lay = lay.crop(bb)
    lay = lay.resize((lay.width // 2, lay.height // 2), Image.LANCZOS).rotate(angle, resample=Image.BICUBIC, expand=True)
    sh = Image.new('RGBA', lay.size, (0, 0, 0, 0)); sh.putalpha(lay.getchannel('A').point(lambda a: int(a * 0.55)))
    sh = sh.filter(ImageFilter.GaussianBlur(9))
    im.alpha_composite(sh, (x + 8, y + 10)); im.alpha_composite(lay, (x, y))
    return (x, y, x + lay.width, y + lay.height)

def badge(im, text, x, y, col, size=40, angle=-6):
    f = ImageFont.truetype(DELA, size * 2)
    tw = int(f.getlength(text)); bh = int(size * 2 * 1.5)
    lay = Image.new('RGBA', (tw + 120, bh + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([14, 14, tw + 100, bh + 14], 26, fill=INK)
    d.rounded_rectangle([4, 4, tw + 90, bh + 4], 26, fill=col, outline=WHITE, width=8)
    d.text((47, 4 + bh // 2), text, font=f, fill=WHITE, anchor='lm')
    lay = lay.resize((lay.width // 2, lay.height // 2), Image.LANCZOS).rotate(angle, resample=Image.BICUBIC, expand=True)
    im.alpha_composite(lay, (x, y))

def arrow(im, p0, p1, col=RED, w=16, head=46, bend=0.25):
    """Изогнутая стрелка от p0 к p1 с белой обводкой."""
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    (x0, y0), (x1, y1) = p0, p1
    mx, my = (x0 + x1) / 2 - (y1 - y0) * bend, (y0 + y1) / 2 + (x1 - x0) * bend
    pts = [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t * t * y1) for t in [i / 40 for i in range(41)]]
    ang = math.atan2(pts[-1][1] - pts[-4][1], pts[-1][0] - pts[-4][0])
    hp = [(x1 + 6 * math.cos(ang), y1 + 6 * math.sin(ang)),
          (x1 - head * math.cos(ang - 0.5), y1 - head * math.sin(ang - 0.5)),
          (x1 - head * math.cos(ang + 0.5), y1 - head * math.sin(ang + 0.5))]
    body = pts[:-3]
    for c, ww in ((WHITE, w + 12), (col, w)):
        d.line(body, fill=c, width=ww, joint='curve')
        for p in (body[0],): d.ellipse([p[0] - ww / 2, p[1] - ww / 2, p[0] + ww / 2, p[1] + ww / 2], fill=c)
        hh = [(x + (6 if c == WHITE else 0) * math.cos(ang), y + (6 if c == WHITE else 0) * math.sin(ang)) for x, y in hp]
        d.polygon(hh if c == col else [(hp[0][0] + 8 * math.cos(ang), hp[0][1] + 8 * math.sin(ang)),
                                       (hp[1][0] - 8 * math.cos(ang - 0.5), hp[1][1] - 8 * math.sin(ang - 0.5)),
                                       (hp[2][0] - 8 * math.cos(ang + 0.5), hp[2][1] - 8 * math.sin(ang + 0.5))], fill=c)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(lay.getchannel('A').point(lambda a: int(a * 0.5)))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)), (5, 7)); im.alpha_composite(lay)

def base(name, crop=None, bright=1.0):
    im = Image.open(os.path.join(D, 'base', name)).convert('RGB')
    if crop: im = im.crop(crop)
    im = im.resize((W, H), Image.LANCZOS)
    if bright != 1.0:
        from PIL import ImageEnhance
        im = ImageEnhance.Brightness(im).enhance(bright)
    from PIL import ImageEnhance
    im = ImageEnhance.Color(im).enhance(1.12); im = ImageEnhance.Contrast(im).enhance(1.06)
    return im.convert('RGBA')

CROP = (0, 4, 2688, 1516)
def v_fire1():
    im = base('fire1.png', CROP)
    headline(im, [('ГРЕЛИ', WHITE, 170), ('ОГНЁМ?!', YEL, 170)], 30, 6, 420, angle=-4)
    badge(im, 'ОПАСНО!', 40, 590, RED, 44, angle=-7)
    return im
def v_fire2():
    im = base('fire2.png', CROP)
    headline(im, [('ГРЕЛИ', WHITE, 170), ('ОГНЁМ?!', YEL, 170)], 24, 110, 420, angle=-4)
    badge(im, 'ОПАСНО!', 470, 26, RED, 40, angle=6)
    return im
def v_egg():
    im = base('egg2.png', CROP)
    headline(im, [('ЯЙЦО', YEL, 220), ('В РАДИАТОР?!', WHITE, 140)], 28, 14, 560, angle=-4)
    arrow(im, (360, 520), (690, 610), bend=0.3)
    return im
def v_tights():
    im = base('tights1.png', CROP)
    headline(im, [('КОЛГОТКИ', YEL, 160), ('ВМЕСТО', WHITE, 104), ('РЕМНЯ?!', WHITE, 104)], 22, 10, 500, angle=-4)
    arrow(im, (330, 540), (560, 470), bend=-0.35)
    return im
VARIANTS = {'fire1': v_fire1, 'fire2': v_fire2, 'egg': v_egg, 'tights': v_tights}

if __name__ == '__main__':
    import sys
    names = sys.argv[1:] or list(VARIANTS)
    outs = []
    for n in names:
        im = VARIANTS[n]().convert('RGB'); p = os.path.join(D, 'out', f'thumb_{n}.jpg'); im.save(p, quality=93); outs.append((n, im))
    # лист превью: полный размер в ленте телефона (≈360×202) и мелкий в поиске (168×94), рядом старая обложка
    old = Image.open('/tmp/claude-0/-home-user-lookme-viewer/8420a68c-a72b-5ef9-9faf-653836f3526a/scratchpad/sovhacks/thumb_sovhacks.jpg').convert('RGB')
    rows = [('old', old)] + outs
    sheet = Image.new('RGB', (380 + 190 + 30, len(rows) * 216 + 10), (240, 240, 240))
    for k, (n, im) in enumerate(rows):
        sheet.paste(im.resize((360, 202), Image.LANCZOS), (10, 10 + k * 216))
        sheet.paste(im.resize((168, 94), Image.LANCZOS), (390, 10 + k * 216))
    sheet.save(os.path.join(D, 'qa', 'sheet.jpg'), quality=90); print('ok', [n for n, _ in outs])
