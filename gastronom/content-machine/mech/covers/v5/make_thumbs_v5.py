"""Обложки v5 — новый формат для длинных роликов: фото, без Михалыча и без рисованного стиля канала.

Пользователь (11 нояб): «У нас обложки не вытягивают. Может вообще поменять формат — сделать без Михалыча и нашего
стиля. Попробуй для воды и жигулей».
Формат:
  - база — фотореалистичный кадр (gpt_image_2_5 medium, 2k): один крупный предмет-крючок или живое лицо с эмоцией,
    предмет заполняет кадр, треть кадра спокойная под текст;
  - текст 2–4 слова: узкий Oswald 700 капсом, белое + ключевое слово жёлтым, толстая чёрная обводка и тень;
  - плашки-цифры («40 ЛЕТ» зелёная, «5 ЛЕТ» красная) для сравнений;
  - один красный акцент: стрелка или кружок на главном;
  - цвет сочнее и контрастнее, края темнее; правый нижний угол свободен (счётчик длительности YouTube).

    python3 make_thumbs_v5.py <папка ролика> [имена] → <папка>/thumb/out5/thumb_<имя>.jpg и <папка>/thumb/sheet5.jpg
Базы — <папка>/thumb/base5/<база>.png.
"""
import os, sys, math
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, 'Oswald_wght_700.ttf')
W, H = 1280, 720
WHITE, YELLOW, BLACK, RED, GREEN = (255, 255, 255), (255, 214, 0), (12, 12, 16), (226, 30, 38), (22, 163, 74)


def photo(path, x0=0, y0=0, z=1.0, sat=1.15, con=1.1, vign=0.8):
    """Фото-база → 1280×720 с наездом (окно 1280/z × 720/z от (x0, y0) в координатах 1280×720), сочнее и с виньеткой."""
    im = Image.open(path).convert('RGB')
    im = im.crop((0, (im.height - im.width * 9 // 16) // 2, im.width, (im.height + im.width * 9 // 16) // 2))
    k = im.width / W
    im = im.crop((int(x0 * k), int(y0 * k), int((x0 + W / z) * k), int((y0 + H / z) * k))).resize((W, H), Image.LANCZOS)
    im = ImageEnhance.Color(im).enhance(sat); im = ImageEnhance.Contrast(im).enhance(con)
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=50, threshold=2))
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).ellipse([-W * 0.25, -H * 0.35, W * 1.25, H * 1.35], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(160))
    return Image.composite(im, ImageEnhance.Brightness(im).enhance(vign), m)


def _fit(lines, maxw, maxsize=400):
    size = maxsize
    while size > 40:
        f = ImageFont.truetype(FONT, size)
        if max(f.getlength(t) for t, _ in lines) <= maxw: return f, size
        size -= 4
    return ImageFont.truetype(FONT, 40), 40


def text_block(lines, maxw, angle=0, maxsize=400):
    """lines: [(текст, цвет)] → RGBA: обводка и жёсткая тень. Кегль — чтобы самая длинная строка была maxw."""
    f, size = _fit(lines, maxw, maxsize)
    sw = max(6, int(size * 0.085)); lh = int(size * 1.02)
    w = int(max(f.getlength(t) for t, _ in lines)) + 4 * sw + 40; h = lh * len(lines) + 4 * sw + int(size * 0.4)
    txt = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(txt)
    for i, (t, col) in enumerate(lines):
        d.text((2 * sw, 2 * sw + i * lh), t, font=f, fill=col, stroke_width=sw, stroke_fill=BLACK)
    a = txt.getchannel('A')
    sh = Image.new('RGBA', (w + 40, h + 40), (0, 0, 0, 0))
    sh.paste(Image.new('RGBA', (w, h), BLACK + (210,)), (int(size * 0.06), int(size * 0.07)), a)
    sh.alpha_composite(txt, (0, 0)); sh = sh.crop(sh.getbbox())
    return sh.rotate(angle, resample=Image.BICUBIC, expand=True) if angle else sh


def plate(text, bg, fg=WHITE, size=120, angle=0, pad=(34, 10)):
    """Плашка-цифра: цветной прямоугольник с текстом, белая окантовка и тень («40 ЛЕТ», «5 ЛЕТ»)."""
    f = ImageFont.truetype(FONT, size); tw = f.getlength(text)
    bb = f.getbbox(text); th = bb[3] - bb[1]
    w, h = int(tw + 2 * pad[0]), int(th + 2 * pad[1] + size * 0.18)
    im = Image.new('RGBA', (w + 30, h + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([10, 12, w + 10, h + 12], fill=BLACK + (170,))
    d.rectangle([0, 0, w, h], fill=WHITE); d.rectangle([6, 6, w - 6, h - 6], fill=bg)
    d.text((w / 2, h / 2), text, font=f, fill=fg, anchor='mm')
    return im.rotate(angle, resample=Image.BICUBIC, expand=True) if angle else im


def ring(im, cx, cy, rx, ry, width=14):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=WHITE, width=width + 10)
    d.ellipse([cx - rx + 5, cy - ry + 5, cx + rx - 5, cy + ry - 5], outline=RED, width=width)
    out = im.convert('RGBA'); out.alpha_composite(lay); return out.convert('RGB')


def arrow(im, x0, y0, x1, y1, width=26):
    """Толстая красная стрелка с белой окантовкой от (x0, y0) к острию (x1, y1)."""
    ang = math.atan2(y1 - y0, x1 - x0)
    head, hw = width * 2.4, width * 1.9
    def pts(w, hd, hwid):
        ux, uy = math.cos(ang), math.sin(ang); px, py = -uy, ux
        bx, by = x1 - ux * hd, y1 - uy * hd
        return [(x0 + px * w / 2, y0 + py * w / 2), (bx + px * w / 2, by + py * w / 2), (bx + px * hwid, by + py * hwid),
                (x1, y1), (bx - px * hwid, by - py * hwid), (bx - px * w / 2, by - py * w / 2), (x0 - px * w / 2, y0 - py * w / 2)]
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.polygon(pts(width + 12, head + 6, hw + 8), fill=WHITE); d.polygon(pts(width, head, hw), fill=RED)
    out = im.convert('RGBA'); out.alpha_composite(lay); return out.convert('RGB')


def put(im, layer, x, y):
    out = im.convert('RGBA'); out.alpha_composite(layer, (int(x), int(y))); return out.convert('RGB')


def B(proj, name): return os.path.join(proj, 'thumb', 'base5', name + '.png')


# ---------- обложки по роликам: имя → функция(папка ролика) ----------
def water_pour(p):
    im = photo(B(p, 'ph_pour'))
    tb = text_block([('ВОДА', WHITE), ('В БАК?!', YELLOW)], 470)   # низ слева — чистая красная краска
    return put(im, tb, 22, H - tb.height - 14)

def water_nozzle(p):
    im = photo(B(p, 'ph_nozzle'))
    tb = text_block([('БЕНЗИН', WHITE), ('ИЗ КРАНА?', YELLOW)], 500)
    return put(im, tb, 22, 18)

def water_face(p):
    im = photo(B(p, 'ph_face'))
    tb = text_block([('ПОЕДЕТ', WHITE), ('НА ВОДЕ?', YELLOW)], 560)
    return put(im, tb, 22, 18)

def water_jar(p):
    im = photo(B(p, 'ph_jar'))
    im = ring(im, 838, 372, 175, 228)
    tb = text_block([('МОТОР', WHITE), ('НА ВОДЕ?', YELLOW)], 520)
    return put(im, tb, 22, 18)

def zhig_vs(p):
    im = photo(B(p, 'ph_vs'))
    im = put(im, plate('40 ЛЕТ', GREEN, size=130, angle=3), 70, 40)
    im = put(im, plate('5 ЛЕТ', RED, size=130, angle=-3), 790, 40)
    tb = text_block([('ПОЧЕМУ?', YELLOW)], 560)
    return put(im, tb, (W - tb.width) / 2, H - tb.height - 12)

def zhig_rust(p):
    im = photo(B(p, 'ph_rust'))
    tb = text_block([('ВЕЧНЫЕ', WHITE), ('ЖИГУЛИ?', YELLOW)], 520)
    return put(im, tb, 22, 18)

def zhig_grandpa(p):
    im = photo(B(p, 'ph_grandpa'))
    im = put(im, plate('ЕЗДИТ 40 ЛЕТ', GREEN, size=96, angle=-2), 30, 40)
    tb = text_block([('А НОВЫЕ', WHITE), ('НА ВЫБРОС?', YELLOW)], 520)
    return put(im, tb, 22, H - tb.height - 20)

def zhig_bin(p):
    im = photo(B(p, 'ph_bin'), 150, 60, 1.13)   # ближе: машина в баке крупнее, пустая стена слева уже
    tb = text_block([('ОДНОРАЗОВЫЕ', YELLOW), ('МАШИНЫ?', WHITE)], 640)
    return put(im, tb, 18, 14)


SPECS = {
    'water': {'pour': water_pour, 'nozzle': water_nozzle, 'face': water_face, 'jar': water_jar},
    'disposable': {'vs': zhig_vs, 'rust': zhig_rust, 'grandpa': zhig_grandpa, 'bin': zhig_bin},
}

if __name__ == '__main__':
    proj = os.path.abspath(sys.argv[1]); spec = SPECS[os.path.basename(proj)]
    keys = sys.argv[2:] or [k for k in spec]
    out = os.path.join(proj, 'thumb', 'out5'); os.makedirs(out, exist_ok=True); ims = []
    for k in keys:
        try: im = spec[k](proj)
        except FileNotFoundError as e: print('нет базы', k, e); continue
        im.save(os.path.join(out, f'thumb_{k}.jpg'), quality=93); ims.append(im)
    # лист: крупно и как в ленте телефона
    sheet = Image.new('RGB', (10 + 640 + 10 + 320 + 10, 10 + len(ims) * 370), (242, 242, 242))
    for i, im in enumerate(ims):
        sheet.paste(im.resize((640, 360), Image.LANCZOS), (10, 10 + i * 370))
        sheet.paste(im.resize((320, 180), Image.LANCZOS), (660, 10 + i * 370))
    sheet.save(os.path.join(proj, 'thumb', 'sheet5.jpg'), quality=90); print('ok', keys)
