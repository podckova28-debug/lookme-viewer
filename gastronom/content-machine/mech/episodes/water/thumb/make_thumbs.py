"""Обложки «Почему машины до сих пор не ездят на воде?» — в стиле обложек шортсов «Гаража Михалыча».

Рисованная база (gpt_image_2_5 по референсу стиля, без текста) + наклейка как в шортсах (covers/covers.py sticker):
кремовая плашка, тёмно-синяя обводка и комикс-тень, наклон 3°, Dela Gothic One, ключевое слово оранжевым.
Под 16:9: наклейка слева внизу (правый нижний угол — счётчик длительности YouTube, туда ничего не ставим).
На табличке за лобовым стеклом — «ПРОДАМ» в перспективе (углы таблички в SIGNS, в пикселях базы 2688×1520).

    python3 make_thumbs3.py            → out3/thumb_<имя>.jpg 1280×720 и sheet3.jpg (как в ленте телефона)
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
D = os.path.dirname(os.path.abspath(__file__))
FONT = '/home/user/gastronom/content-machine/mech/covers/fonts/DelaGothicOne.ttf'
W, H = 1280, 720
NAVY, ORANGE, WHITE, CREAM, RED = (27, 38, 66), (245, 136, 32), (255, 255, 255), (255, 248, 236), (205, 30, 30)

def runs(line):
    out = []
    for i, part in enumerate(line.split('*')):
        if part: out.append((part, i % 2 == 1))
    return out

def base(name):
    im = Image.open(os.path.join(D, 'base', name + '.png')).convert('RGB')
    im = im.crop((0, 4, 2688, 1516))
    return im

def sign_text(im, quad, text='ПРОДАМ', col=RED):
    """Пишет текст на табличке: quad — углы TL, TR, BR, BL в пикселях базы."""
    import numpy as np
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = quad
    w = int(max(x1 - x0, x2 - x3)); h = int(max(y3 - y0, y2 - y1))
    flat = Image.new('RGBA', (w * 2, h * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(flat)
    size = h * 2
    while size > 10:
        f = ImageFont.truetype(FONT, size)
        bb = d.textbbox((0, 0), text, font=f)
        if bb[2] - bb[0] <= w * 2 * 0.86 and bb[3] - bb[1] <= h * 2 * 0.62: break
        size -= 4
    bb = d.textbbox((0, 0), text, font=f)
    d.text(((w * 2 - (bb[2] - bb[0])) / 2 - bb[0], (h * 2 - (bb[3] - bb[1])) / 2 - bb[1]), text, font=f, fill=col + (235,))
    flat = flat.resize((w, h), Image.LANCZOS)
    # перспектива: для каждой точки результата ищем точку в плоском прямоугольнике
    src = [(0, 0), (w, 0), (w, h), (0, h)]; dst = quad
    A = []; B = []
    for (X, Y), (u, v) in zip(dst, src):
        A.append([X, Y, 1, 0, 0, 0, -u * X, -u * Y]); B.append(u)
        A.append([0, 0, 0, X, Y, 1, -v * X, -v * Y]); B.append(v)
    coef = np.linalg.solve(np.array(A, float), np.array(B, float))
    layer = flat.transform(im.size, Image.PERSPECTIVE, tuple(coef), Image.BICUBIC)
    out = im.convert('RGBA'); out.alpha_composite(layer)
    return out.convert('RGB')

SERIES = []     # заголовки всех обложек серии: кегль один на всех, как в шортсах (заполняется ниже из V)

def series_size(maxw=640, size=84):
    while size > 30:
        f = ImageFont.truetype(FONT, size)
        if all(f.getlength(''.join(t for t, _ in runs(l))) <= maxw for title in SERIES for l in title.split('\n')): return size
        size -= 2
    return size

def sticker(im, title, cx, cy, angle=3, margin=22):
    """Наклейка как на обложках шортсов (covers.py sticker), пропорции те же: поля по бокам ≈ 0,5 кегля, сверху и снизу
    ровно по 0,42 кегля от букв (центруем по реальным буквам, с хвостиками «у», «р», «д», а не по метрикам шрифта)."""
    lines = title.split('\n'); f = ImageFont.truetype(FONT, series_size()); lh = int(f.size * 1.2)
    # 1) текст на отдельном слое → реальные границы букв
    tl = Image.new('RGBA', (2000, lh * len(lines) + f.size * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(tl)
    for i, l in enumerate(lines):
        rr = runs(l); w = sum(f.getlength(t) for t, _ in rr); x = 1000 - w / 2
        for t, hot in rr:
            d.text((x, f.size // 2 + i * lh), t, font=f, fill=ORANGE if hot else NAVY); x += f.getlength(t)
    tl = tl.crop(tl.getbbox())
    # 2) плашка вокруг букв
    px, py = int(f.size * 0.52), int(f.size * 0.42)
    sh, rad, ow = int(f.size * 0.15), int(f.size * 0.32), max(5, int(f.size * 0.09))
    bw, bh = tl.width + 2 * px + 2 * ow, tl.height + 2 * py + 2 * ow
    layer = Image.new('RGBA', (bw + sh + 20, bh + sh + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    d.rounded_rectangle([4 + sh, 4 + sh, bw + 4 + sh, bh + 4 + sh], rad, fill=NAVY)            # комикс-тень
    d.rounded_rectangle([4, 4, bw + 4, bh + 4], rad, fill=CREAM, outline=NAVY, width=ow)
    layer.alpha_composite(tl, (4 + ow + px, 4 + ow + py))
    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
    x = int(cx - layer.width / 2); y = int(cy - layer.height / 2)
    x = max(margin, min(W - margin - layer.width, x)); y = max(margin, min(H - margin - layer.height, y))   # не обрезать у краёв
    out = im.convert('RGBA'); out.alpha_composite(layer, (x, y))
    return out.convert('RGB')

def finish(im):
    im = im.resize((W, H), Image.LANCZOS)
    im = ImageEnhance.Color(im).enhance(1.08); im = ImageEnhance.Contrast(im).enhance(1.04)
    return im

SIGNS = {}
V = {          # имя обложки → (база, заголовок, центр наклейки x, y в 1280×720)
    'hose': ('th_hose', 'Залил *воду*\nв бак?!', 330, 570),
    'glass': ('th_glass', 'Машина\n*на воде*?', 360, 570),
    'jar': ('th_jar', '*Водородный*\nгенератор?', 360, 150),
}
SERIES[:] = [v[1] for v in V.values()]

def build(key):
    b, title, cx, cy = V[key]
    im = base(b)
    if b in SIGNS: im = sign_text(im, SIGNS[b])
    im = finish(im)
    return sticker(im, title, cx, cy)

if __name__ == '__main__':
    os.makedirs(os.path.join(D, 'out'), exist_ok=True)
    keys = sys.argv[1:] or list(V)
    outs = []
    for k in keys:
        im = build(k); im.save(os.path.join(D, 'out', f'thumb_{k}.jpg'), quality=93); outs.append(im)
    # лист превью: крупно (как на компьютере) и мелко (как в ленте телефона)
    sheet = Image.new('RGB', (10 + 480 + 10 + 240 + 10, 10 + len(outs) * 280), (242, 242, 242))
    for i, im in enumerate(outs):
        sheet.paste(im.resize((480, 270), Image.LANCZOS), (10, 10 + i * 280))
        sheet.paste(im.resize((240, 135), Image.LANCZOS), (500, 10 + i * 280))
    sheet.save(os.path.join(D, 'sheet.jpg'), quality=90); print('ok', keys)
