"""covers.py <style> — обложки «Гаража Михалыча» 1080×1920 под сетку Instagram (3:4) и Shorts/Клипы (9:16).
Всё важное — в центральной зоне 3:4 (y 240…1680): её показывает сетка профиля. Верхний правый угол плитки
занят значком Reels/закрепа, нижний левый — счётчиком просмотров: туда текст не ставим.
style: band — тёмная шапка с заголовком над картинкой; sticker — комикс-наклейка в нижней трети."""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
V = '/tmp/claude-0/-home-user-lookme-viewer/8420a68c-a72b-5ef9-9faf-653836f3526a/scratchpad/video/'
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, 'fonts', os.environ.get('FONT', 'DelaGothicOne.ttf'))
W, H = 1080, 1920
NAVY, ORANGE, WHITE, CREAM = (27, 38, 66), (245, 136, 32), (255, 255, 255), (255, 248, 236)
# (ключ, кадр, лицо по высоте исходника 0..1, лицо по ширине, заголовок; *слово* — оранжевым)
EPS = [
 ('spare', 'mech_spare/kf/k1_hook.png', 0.50, 0.34, 'Гнать на\n*докатке?*'),
 ('redlight', 'mech_redlight/kf/k1_hook.png', 0.49, 0.59, '*Сцепление*\nна красном?'),
 ('tirep', 'mech_tirep/kf/k1_hook.png', 0.40, 0.36, '*Спускать*\nшины зимой?'),  # кадр v3: ниппель у края обода
 ('clutch', 'mech_clutch/kf/k1_hook.png', 0.43, 0.69, 'Выжимать\n*сцепление?*'),
 ('snow', 'mech_snow/kf/k1_hook.png', 0.47, 0.28, 'Снег с крыши\n*сам слетит?*'),
 ('gas92', 'mech_gas92/kf/k1_hook.png', 0.36, 0.51, '*95-й* лучше\n92-го?'),
 ('reverse', 'mech_reverse/kf/k1_hook.png', 0.42, 0.27, 'Задняя\n*на ходу?*'),
 ('tire', 'tire/kf/k1_hook.png', 0.34, 0.45, 'Зачем шинам\n*волоски?*'),
 ('warm', 'warm/kf/k1_hook.png', 0.30, 0.42, 'Греть мотор\n*10 минут?*'),
 ('diesel', 'diesel/kf/k1_hook.png', 0.30, 0.50, 'Бензин\nв *дизель*'),
 ('sugar', 'sugar/kf/k1_hook.png', 0.45, 0.45, '*Сахар* в бак:\nмотору конец?'),
 ('frit', 'frit/kf/k1_hook.png', 0.32, 0.55, '*Чёрные точки*\nна стекле?'),
 ('handbrake', 'handbrake/kf/k4_morning.png', 0.36, 0.45, 'Зимой\nбез *ручника?*'),
 ('phone', 'mech/v2/kf/k1n.png', 0.27, 0.48, '*Телефон*\nна заправке?'),
 ('kettle', 'kettle/kf/k1_hook.png', 0.31, 0.38, '*Кипяток*\nна лобовое?'),
 ('lamp', 'lamp/kf/k1_hook.png', 0.33, 0.58, 'Еду\nна *лампочке*'),
 ('nozzle', 'nozzle/kf/k1b_hook.png', 0.38, 0.12, 'Уехал с\n*пистолетом*'),
 ('neutral', 'mech_neutral/kf/k1_hook.png', 0.56, 0.57, '*Нейтралка*\nс горки?'),
 ('oil', 'mech_oil/kf/k1_pour.png', 0.445, 0.27, '*Перелить*\nмасло?'),
 ('dawn', 'mech_dawn/kf/mk1b_hook.png', 0.43, 0.70, '*Утром*\nвыгоднее?'),
 ('plus7', 'mech_plus7/kf/k1_hook.png', 0.47, 0.59, 'Менять резину\nпри *+7?*'),
]


def runs(line):
    """'Бензин в *дизель*' → [('Бензин в ', False), ('дизель', True)]"""
    out, hot = [], False
    for i, part in enumerate(line.split('*')):
        if part: out.append((part, i % 2 == 1))
    return out


def series_font(maxw, size):
    """Один кегль на все обложки серии — чтобы сетка выглядела ровно."""
    while size > 40:
        f = ImageFont.truetype(FONT, size)
        if all(f.getlength(''.join(t for t, _ in runs(l))) <= maxw for e in EPS for l in e[4].split('\n')): return f
        size -= 2
    return ImageFont.truetype(FONT, size)


def fit_font(lines, maxw, size):
    while size > 40:
        f = ImageFont.truetype(FONT, size)
        if max(f.getlength(''.join(t for t, _ in runs(l))) for l in lines) <= maxw: return f
        size -= 4
    return ImageFont.truetype(FONT, size)


def draw_title(d, lines, f, cx, y, base, hot, lh, stroke=0, stroke_fill=None, left=None):
    for i, l in enumerate(lines):
        rr = runs(l); tw = sum(f.getlength(t) for t, _ in rr); x = left if left is not None else cx - tw / 2
        for t, h in rr:
            d.text((x, y + i * lh), t, font=f, fill=hot if h else base, stroke_width=stroke, stroke_fill=stroke_fill)
            x += f.getlength(t)


def place(src, face_y, face_x, target_y, zoom=1.0):
    """Картинка на ширину кадра (× zoom), лицо — на высоте target_y; пустоты сверху заполняет размытым краем."""
    im = Image.open(V + src).convert('RGB')
    s = W / im.width * zoom; im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x0 = int(min(max(face_x * im.width - W / 2, 0), im.width - W)); y0 = int(face_y * im.height - target_y)
    can = Image.new('RGB', (W, H))
    if y0 < 0:  # не хватает верха — растянутый размытый верхний край
        top = im.crop((x0, 0, x0 + W, 200)).resize((W, -y0 + 200)).filter(ImageFilter.GaussianBlur(30)); can.paste(top, (0, 0))
    can.paste(im.crop((x0, max(y0, 0), x0 + W, max(y0, 0) + H - max(-y0, 0))), (0, max(-y0, 0)))
    return can


def band(key, src, fy, fx, title):
    can = place(src, fy, fx, 930)
    d = ImageDraw.Draw(can)
    d.rectangle([0, 0, W, 640], fill=NAVY); d.rectangle([0, 640, W, 658], fill=ORANGE)
    lines = title.split('\n'); f = series_font(850, 124); lh = int(f.size * 1.2)
    y = 628 - 34 - lh * len(lines)                      # текст прижат к низу шапки, подальше от значка
    draw_title(d, lines, f, 0, y, WHITE, ORANGE, lh, left=64)
    return can


# где держать лицо по высоте кадра; у «Кипятка» выше, чтобы струя на стекло была над наклейкой
FACE_Y = {'kettle': 560, 'snow': 900, 'clutch': 835, 'spare': 960, 'tirep': 760}   # snow: лицо низко, без сдвига вверх (иначе снизу чёрная полоса)
# «Лампочка»: в исходном кадре щиток приборов развёрнут к зрителю (ошибка модели, в ролике её тоже убирали зумом).
# Крупный план: зум 1,6, лицо на y 650 — приборка (верх щитка ≈0,74 высоты исходника) ниже края кадра 9:16.
ZOOM = {'reverse': (1.25, 640),                    # «Задняя на ходу»: лицо и рука на рычаге над наклейкой
        'lamp': (1.6, 650), 'nozzle': (1.1, 600),   # «Пистолет»: кадр выше и ближе — пистолет в баке над наклейкой
        'neutral': (1.3, 830),                     # «Нейтралка»: машина на весь кадр, иначе лицо в окне мелкое
        'dawn': (1.15, 700),                       # «Утром»: без зума внизу чёрная полоса
        'plus7': (1.2, 700),
        'redlight': (1.2, 760)}                   # «Сцепление на красном»: лицо в лобовом мелкое — ближе                       # «+7»: то же


def sticker(key, src, fy, fx, title):
    z, ty = ZOOM.get(key, (1.0, FACE_Y.get(key, 700)))
    can = place(src, fy, fx, ty, z).convert('RGBA')
    lines = title.split('\n'); f = series_font(820, 112); lh = int(f.size * 1.2)
    tw = max(f.getlength(''.join(t for t, _ in runs(l))) for l in lines)
    bw, bh = int(tw + 110), int(lh * len(lines) + 80)
    layer = Image.new('RGBA', (bw + 60, bh + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    d.rounded_rectangle([22, 22, bw + 22, bh + 22], 34, fill=NAVY)                       # комикс-тень
    d.rounded_rectangle([6, 6, bw + 6, bh + 6], 34, fill=CREAM, outline=NAVY, width=10)
    draw_title(d, lines, f, 6 + bw / 2, 6 + 36, NAVY, ORANGE, lh)
    layer = layer.rotate(3, resample=Image.BICUBIC, expand=True)
    cx, cy = W // 2, 1300                               # низ наклейки выше счётчика просмотров (y > 1540)
    can.alpha_composite(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)))
    return can.convert('RGB')


if __name__ == '__main__':
    style = sys.argv[1]; fn = {'band': band, 'sticker': sticker}[style]
    out = os.path.join(HERE, 'out', style + os.environ.get('SUFFIX', '')); os.makedirs(out, exist_ok=True)
    for e in EPS:
        fn(*e).save(os.path.join(out, f'mech_{e[0]}_cover.jpg'), quality=92)
    print('ok', out)
