"""Обложки «Почему Жигули жили по 40 лет, а новые одноразовые» — по рецепту v4 «На воде» — снова классическая наклейка шортсов, но плотный кадр.

Пользователь (10 нояб): «Ладно, верни нас классический стиль обложки и попробуй еще раз».
Что учтено из прошлых попыток:
  - v1: спокойные базы (Михалыч просто стоит) — «не цепляют вообще»;
  - v3: «много свободного места» — в базах треть кадра пустой тёмный фон.
Поэтому: наклейка как в шортсах (make_thumbs.sticker: кремовая плашка, тёмно-синяя обводка и комикс-тень, наклон 3°,
Dela Gothic One, ключевое слово оранжевым), но крупнее, а база приближена (окно 1280/z × 720/z), чтобы Михалыч и
предмет заполняли кадр. Правый нижний угол свободен (счётчик длительности YouTube).

    python3 make_thumbs_v4.py → out4/thumb_<имя>.jpg 1280×720 и sheet4.jpg
"""
import os, sys
from PIL import Image, ImageEnhance
import make_thumbs as mt

D = os.path.dirname(os.path.abspath(__file__))
W, H = 1280, 720

# имя → (база, заголовок, наезд (x0, y0, z) в координатах базы 1280×720, центр наклейки x, y)
V = {
    'vs': ('th_vs', 'Кто\n*вечнее*?', (0, 0, 1.0), 250, 150),
    'bin': ('th_bin', 'Машина\n*на выброс*?', (0, 0, 1.0), 320, 590),
    'parts': ('th_parts', 'Вечные\n*Жигули*?', (0, 0, 1.0), 300, 150),
}
mt.SERIES[:] = [v[1] for v in V.values()]
_size = mt.series_size


def series_size(maxw=600, size=112):           # наклейка крупнее, чем в v2 (там 560 / 104)
    return _size(maxw, size)


mt.series_size = series_size


def base(name, x0, y0, z):
    im = Image.open(os.path.join(D, 'base', name + '.png')).convert('RGB').crop((0, 4, 2688, 1516))
    k = im.width / W
    im = im.crop((int(x0 * k), int(y0 * k), int((x0 + W / z) * k), int((y0 + H / z) * k))).resize((W, H), Image.LANCZOS)
    im = ImageEnhance.Color(im).enhance(1.1); im = ImageEnhance.Contrast(im).enhance(1.05)
    return im


def build(key):
    b, title, (x0, y0, z), cx, cy = V[key]
    return mt.sticker(base(b, x0, y0, z), title, cx, cy)


if __name__ == '__main__':
    out = os.path.join(D, 'out4'); os.makedirs(out, exist_ok=True)
    keys = sys.argv[1:] or [k for k in V if os.path.exists(os.path.join(D, 'base', V[k][0] + '.png'))]
    ims = []
    for k in keys:
        im = build(k); im.save(os.path.join(out, f'thumb_{k}.jpg'), quality=93); ims.append(im)
    sheet = Image.new('RGB', (10 + 480 + 10 + 240 + 10, 10 + len(ims) * 280), (242, 242, 242))
    for i, im in enumerate(ims):
        sheet.paste(im.resize((480, 270), Image.LANCZOS), (10, 10 + i * 280))
        sheet.paste(im.resize((240, 135), Image.LANCZOS), (500, 10 + i * 280))
    sheet.save(os.path.join(D, 'sheet4.jpg'), quality=90); print('ok', keys)
