"""Обложки v3 «На воде» — выразительный стиль вместо наклейки шортсов.

Пользователь (10 нояб): «Мы можем отклониться от классического стиля ради обложки — сейчас не выразительно».
Те же рисованные базы (base/th_pump, th_boom, th_secret), поверх:
  - огромный узкий Oswald 700 капсом: белое + ключевое слово жёлтым, толстая чёрная обводка, жёсткая тень, наклон −4°;
  - кадр сочнее и контрастнее, затемнение краёв (виньетка);
  - один красный акцент на обложку: кружок вокруг главного предмета или стрелка.
Правый нижний угол свободен (там счётчик длительности YouTube).

    python3 make_thumbs_v3.py → out/thumb_<имя>.jpg 1280×720 и sheet.jpg (крупно и как в ленте телефона)
"""
import os, sys, math
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageChops

D = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(D, 'Oswald_wght_700.ttf')
W, H = 1280, 720
WHITE, YELLOW, BLACK, RED = (255, 255, 255), (255, 214, 0), (12, 12, 16), (232, 28, 36)


def base(name, x0=0, y0=0, z=1.0):
    """База → 1280×720 с наездом: окно 1280/z × 720/z с левым верхним углом (x0, y0) в координатах базы 1280×720.
    Наезд убирает пустой фон («Много свободного места»): персонаж и предмет заполняют кадр."""
    im = Image.open(os.path.join(D, 'base', name + '.png')).convert('RGB').crop((0, 4, 2688, 1516))
    k = im.width / W
    im = im.crop((int(x0 * k), int(y0 * k), int((x0 + W / z) * k), int((y0 + H / z) * k))).resize((W, H), Image.LANCZOS)
    im = ImageEnhance.Color(im).enhance(1.22); im = ImageEnhance.Contrast(im).enhance(1.12)
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    # лёгкая виньетка: края темнее на ~20 %
    m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
    d.ellipse([-W * 0.25, -H * 0.35, W * 1.25, H * 1.35], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(160))
    dark = ImageEnhance.Brightness(im).enhance(0.8)
    return Image.composite(im, dark, m)


def text_block(lines, maxw, angle=-4):
    """lines: [(текст, цвет)] → RGBA-слой с обводкой и тенью. Кегль подбирается так, чтобы самая длинная строка была maxw."""
    size = 400
    while size > 40:
        f = ImageFont.truetype(FONT, size)
        if max(f.getlength(t) for t, _ in lines) <= maxw: break
        size -= 4
    sw = max(6, int(size * 0.085)); lh = int(size * 1.02)
    w = int(max(f.getlength(t) for t, _ in lines)) + 4 * sw + 40; h = lh * len(lines) + 4 * sw + int(size * 0.4)
    txt = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(txt)
    for i, (t, col) in enumerate(lines):
        d.text((2 * sw, 2 * sw + i * lh), t, font=f, fill=col, stroke_width=sw, stroke_fill=BLACK)
    # жёсткая тень: силуэт текста, сдвиг вниз-вправо
    a = txt.getchannel('A')
    sh = Image.new('RGBA', (w + 30, h + 30), (0, 0, 0, 0))
    sh.paste(Image.new('RGBA', (w, h), BLACK + (210,)), (int(size * 0.07), int(size * 0.08)), a)
    sh.alpha_composite(txt, (0, 0))
    sh = sh.crop(sh.getbbox())
    return sh.rotate(angle, resample=Image.BICUBIC, expand=True)


def ring(im, cx, cy, rx, ry, width=14):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=WHITE, width=width + 10)
    d.ellipse([cx - rx + 5, cy - ry + 5, cx + rx - 5, cy + ry - 5], outline=RED, width=width)
    out = im.convert('RGBA'); out.alpha_composite(lay); return out.convert('RGB')


def arrow(im, x0, y0, x1, y1, width=26):
    """Толстая красная стрелка с белой окантовкой от (x0, y0) к острию (x1, y1)."""
    ang = math.atan2(y1 - y0, x1 - x0); L = math.hypot(x1 - x0, y1 - y0)
    head, hw = width * 2.4, width * 1.9
    def pts(w, hd, hwid):
        ux, uy = math.cos(ang), math.sin(ang); px, py = -uy, ux
        bx, by = x1 - ux * hd, y1 - uy * hd
        return [(x0 + px * w / 2, y0 + py * w / 2), (bx + px * w / 2, by + py * w / 2), (bx + px * hwid, by + py * hwid),
                (x1, y1), (bx - px * hwid, by - py * hwid), (bx - px * w / 2, by - py * w / 2), (x0 - px * w / 2, y0 - py * w / 2)]
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.polygon(pts(width + 12, head + 6, hw + 8), fill=WHITE)
    d.polygon(pts(width, head, hw), fill=RED)
    out = im.convert('RGBA'); out.alpha_composite(lay); return out.convert('RGB')


def put(im, layer, x, y):
    out = im.convert('RGBA'); out.alpha_composite(layer, (int(x), int(y))); return out.convert('RGB')


def build(key):
    # координаты кружков — уже в кадре после наезда
    if key == 'pump':
        im = base('th_pump', 213, 0, 1.2)
        tb = text_block([('БЕНЗИН', WHITE), ('НЕ НУЖЕН?', YELLOW)], 620)
        return put(im, tb, 16, 10)
    if key == 'boom':
        im = base('th_boom', 200, 0, 1.25)
        im = ring(im, 419, 287, 169, 148)
        tb = text_block([('МОТОР', WHITE), ('НА ВОДЕ?!', YELLOW)], 490)
        return put(im, tb, 14, H - tb.height - 8)
    if key == 'secret':
        im = base('th_secret', 332, 0, 1.35)
        im = ring(im, 180, 540, 152, 172)
        tb = text_block([('ЭТО', WHITE), ('СКРЫВАЮТ?', YELLOW)], 560)
        return put(im, tb, 12, 6)
    raise KeyError(key)


KEYS = ['pump', 'boom', 'secret']

if __name__ == '__main__':
    os.makedirs(os.path.join(D, 'out'), exist_ok=True)
    keys = sys.argv[1:] or KEYS; outs = []
    for k in keys:
        im = build(k); im.save(os.path.join(D, 'out', f'thumb_{k}.jpg'), quality=93); outs.append(im)
    sheet = Image.new('RGB', (10 + 480 + 10 + 240 + 10, 10 + len(outs) * 280), (242, 242, 242))
    for i, im in enumerate(outs):
        sheet.paste(im.resize((480, 270), Image.LANCZOS), (10, 10 + i * 280))
        sheet.paste(im.resize((240, 135), Image.LANCZOS), (500, 10 + i * 280))
    sheet.save(os.path.join(D, 'sheet.jpg'), quality=90); print('ok', keys)
