"""Обложки v6 — все длинные ролики Михалыча, по 3 варианта для «Тестирования и сравнения» YouTube.

Пользователь (11 нояб): «Просмотри обложки наших видео ещё раз. Как добиться CTR 5 %» → «Переделай обложки всех видео».
Правила (разбор лидеров — analytics/2026-11-11_mech_ctr_covers.md):
  - фото, без Михалыча и рисованного стиля; одна понятная штука крупно; живое лицо — в одном варианте из трёх;
  - 2–3 слова утверждения, лучше с цифрой из сценария («−10 000 ₽», «5 ИЗ 10», «3 МЕСЯЦА»), вопрос — не на всех;
  - красная стрелка или кружок на главном; у трёх вариантов ролика — разные кадры и разные крючки;
  - обещание обложки — то, что есть в ролике; правый нижний угол свободен (счётчик длительности).
Хелперы — из ../thumb5/make_thumbs_v5.py (photo, text_block, plate, ring, arrow, put).

    python3 make_thumbs_v6.py [видео ...] → out/<видео>_<вариант>.jpg и sheet_<видео>.jpg
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'thumb5'))
import make_thumbs_v5 as v5
from make_thumbs_v5 import photo, text_block, plate, ring, arrow, put, W, H, WHITE, YELLOW, RED, GREEN
from PIL import Image

S = os.path.dirname(HERE)
B = lambda n: os.path.join(HERE, 'base', n + '.png')
B5 = lambda proj, n: os.path.join(S, proj, 'thumb', 'base5', n + '.png')


def tl(im, lines, maxw, x=22, y=16, **kw):            # текст в левом верхнем углу
    tb = text_block(lines, maxw, **kw); return put(im, tb, x, y), tb

def bl(im, lines, maxw, x=22, pad=14, **kw):           # текст в левом нижнем углу
    tb = text_block(lines, maxw, **kw); return put(im, tb, x, H - tb.height - pad), tb


V = {}
def cover(video, key, note):
    def deco(fn): V.setdefault(video, []).append((key, note, fn)); return fn
    return deco


# ---------- «Топ 7 ошибок в мороз, которые губят машину» ----------
@cover('winter', 'kettle', 'Кипяток на лобовое: «−10 000 ₽ за 1 секунду» (итог ролика, Z1)')
def _():
    im = photo(B('winter_kettle'))
    im = put(im, plate('−10 000 ₽', RED, size=128, angle=-3), 26, 34)
    im, tb = bl(im, [('ЗА 1', WHITE), ('СЕКУНДУ', YELLOW)], 400)
    return arrow(im, 470, 300, 690, 410)

@cover('winter', 'face', 'Живое лицо и трещина: «7 ошибок в мороз»')
def _():
    im = photo(B('winter_face'))
    im = ring(im, 455, 310, 175, 115)
    im, tb = bl(im, [('7 ОШИБОК', YELLOW), ('В МОРОЗ', WHITE)], 520)
    return im

@cover('winter', 'roof', 'Снег с крыши на лобовое: «самая опасная» (Z2)')
def _():
    im = photo(B('winter_roof'))
    im, tb = bl(im, [('СНЕГ', WHITE), ('С КРЫШИ', YELLOW)], 470)
    im = put(im, plate('САМАЯ ОПАСНАЯ ОШИБКА', RED, size=58, angle=-2), 26, H - tb.height - 96)
    return arrow(im, 820, 440, 730, 230)


# ---------- «Что из 10 советских автолайфхаков работает до сих пор?» ----------
@cover('sovhacks', 'fire', 'Паяльная лампа под поддоном: «грели огнём — опасно» (L25–L28)')
def _():
    im = photo(B('sov_fire'))
    im, tb = tl(im, [('ГРЕЛИ', WHITE), ('ОГНЁМ', YELLOW)], 430)
    im = put(im, plate('ОПАСНО', RED, size=84, angle=-4), 30, tb.height + 20)
    return arrow(im, 380, 470, 760, 470)

@cover('sovhacks', 'tights', 'Колготки вместо ремня генератора (L05–L09)')
def _():
    im = photo(B('sov_tights'))
    im, tb = tl(im, [('КОЛГОТКИ', YELLOW), ('ВМЕСТО', WHITE), ('РЕМНЯ', WHITE)], 440)
    return arrow(im, 420, 330, 800, 360)

@cover('sovhacks', 'flatlay', 'Все хитрости на верстаке: «5 из 10 работают» (L52)')
def _():
    im = photo(B('sov_flatlay'))
    im = put(im, plate('5 ИЗ 10', GREEN, size=140, angle=-3), 24, 30)
    im, tb = bl(im, [('РАБОТАЮТ', WHITE), ('ДО СИХ ПОР', YELLOW)], 440)
    return im


# ---------- «10 опытов над машиной, которые лучше не повторять» ----------
@cover('whatif', 'sugar', 'Сахар в бензобак (опыт 5)')
def _():
    im = photo(B('whatif_sugar'))
    im, tb = tl(im, [('САХАР', WHITE), ('В БАК', YELLOW)], 420)
    im = put(im, plate('ЧТО БУДЕТ?', RED, size=72, angle=-3), 28, tb.height + 18)
    return arrow(im, 360, 560, 650, 470)

@cover('whatif', 'nozzle', 'Уехал с пистолетом в баке (опыт 2)')
def _():
    im = photo(B('whatif_nozzle'), sat=1.12)
    im, tb = tl(im, [('УЕХАЛ С', WHITE), ('ПИСТОЛЕТОМ', YELLOW)], 600, x=190, y=10)
    return arrow(im, 760, 320, 870, 250, width=22)

@cover('whatif', 'face', 'Живое лицо: бензин в дизель (опыт 1) + «10 опытов»')
def _():
    im = photo(B('whatif_face'))
    im, tb = tl(im, [('БЕНЗИН', WHITE), ('В ДИЗЕЛЬ', YELLOW)], 470)
    return put(im, plate('10 ОПЫТОВ', RED, size=76, angle=-3), 30, H - 140)


# ---------- «Почему продают китайские машины и брать ли их с пробегом» ----------
@cover('china', 'lot', 'Площадка с кроссоверами: объявлений в 2,5 раза больше (A2)')
def _():
    im = photo(B('china_lot'))
    im, tb = tl(im, [('ПРОДАЮТ', WHITE), ('МАССОВО', YELLOW)], 470)
    return put(im, plate('×2,5', RED, size=150, angle=4), 520, 30)

@cover('china', 'wait', 'Разбитый кроссовер на подъёмнике: запчасть ждать до 3 месяцев (E2–E3)')
def _():
    im = photo(B('china_wait'))
    im, tb = tl(im, [('ЗАПЧАСТЬ', WHITE), ('ЖДАТЬ', YELLOW)], 400)
    return put(im, plate('3 МЕСЯЦА', RED, size=120, angle=-3), 26, H - 190)

@cover('china', 'rust', 'Фонарик на ржавом пороге: «С пробегом? Смотри сюда» (D8–D9)')
def _():
    im = photo(B('china_rust'))
    im = ring(im, 820, 330, 230, 110)
    im, tb = tl(im, [('С ПРОБЕГОМ?', WHITE), ('СМОТРИ СЮДА', YELLOW)], 580)
    return im


# ---------- «Почему машины до сих пор не ездят на воде?» ----------
@cover('water', 'face', 'Живое лицо со стаканом воды — стоит на YouTube с 11 нояб (v5)')
def _():
    return v5.water_face(os.path.join(S, 'water'))

@cover('water', 'pour', 'Вода из бутылки в бак')
def _():
    im = photo(B5('water', 'ph_pour'))
    im, tb = bl(im, [('ЗАЛИЛ ВОДУ', WHITE), ('В БАК', YELLOW)], 560)
    return arrow(im, 470, 520, 760, 420)

@cover('water', 'jar', '«Водородный генератор» в банке: не экономит (проверки FTC/EPA, Popular Mechanics)')
def _():
    im = photo(B5('water', 'ph_jar'))
    im = ring(im, 838, 372, 175, 228)
    im, tb = tl(im, [('ВОДОРОД', WHITE), ('ИЗ БАНКИ', YELLOW)], 470)
    return put(im, plate('НЕ ЭКОНОМИТ', RED, size=70, angle=-3), 28, tb.height + 18)


# ---------- «10 машин, которые Михалыч за 30 лет так и не смог убить» ----------
@cover('immortal', 'odo', 'Одометр: 999 999 км почти без ремонта (Lexus LX 470, J5–J6)')
def _():
    im = photo(B('imm_odo'))
    im, tb = tl(im, [('999 999', YELLOW), ('КМ', YELLOW)], 470)
    im = put(im, plate('ПОЧТИ БЕЗ РЕМОНТА', GREEN, size=56, angle=-2), 26, tb.height + 14)
    return arrow(im, 500, 420, 780, 330)

@cover('immortal', 'taxi', 'Такси в музее: почти 2 млн км (W124 200 D из Порту, K3)')
def _():
    im = photo(B('imm_taxi'))
    im = put(im, plate('2 МЛН КМ', GREEN, size=120, angle=-3), 26, 30)
    im, tb = bl(im, [('ТАКСИ', WHITE), ('В МУЗЕЕ', YELLOW)], 330)
    return im

@cover('immortal', 'hammer', 'Живое лицо со сломанной кувалдой: «их не убить»')
def _():
    im = photo(B('imm_hammer'))
    im, tb = tl(im, [('ИХ НЕ', WHITE), ('УБИТЬ', YELLOW)], 400)
    return put(im, plate('10 МАШИН', RED, size=78, angle=-3), 28, tb.height + 18)


# ---------- «Почему „Жигули“ жили по 40 лет, а новые машины — одноразовые?» ----------
@cover('disposable', 'vs', '«Копейка» против дымящего кроссовера: 40 лет / 5 лет (v5)')
def _():
    return v5.zhig_vs(os.path.join(S, 'disposable'))

@cover('disposable', 'rust', 'Сгнившая «копейка»: дожила примерно 1 из 30 (C1–C2)')
def _():
    im = photo(B5('disposable', 'ph_rust'))
    im = ring(im, 600, 470, 150, 120)
    im, tb = tl(im, [('ДОЖИЛА', WHITE), ('1 ИЗ 30', YELLOW)], 400)
    return im

@cover('disposable', 'grandpa', 'Дед у «копейки»: «Ездит 40 лет / А новые на выброс?» (v5)')
def _():
    return v5.zhig_grandpa(os.path.join(S, 'disposable'))


# ---------- «Ты — механик 90-х (и это вся твоя жизнь)» ----------
@cover('mechanic90', 'tyres', 'Живое лицо: зарплата двумя покрышками (A2)')
def _():
    im = photo(B('m90_tyres'))
    im, tb = tl(im, [('ЗАРПЛАТА', WHITE), ('ПОКРЫШКАМИ', YELLOW)], 575)
    return put(im, plate('1994', RED, size=120, angle=-3), 30, tb.height + 22)

@cover('mechanic90', 'split', 'Тот же гараж: 1994 и 2026 — «30 лет в гараже» (I02, Z4)')
def _():
    im = photo(B('m90_split'))
    im = put(im, plate('1994', GREEN, size=96, angle=-3), 40, 26)
    im = put(im, plate('2026', RED, size=96, angle=3), W // 2 + 40, 26)
    im, tb = bl(im, [('30 ЛЕТ', YELLOW), ('В ГАРАЖЕ', WHITE)], 420)
    return im

@cover('mechanic90', 'hands', 'Один ключ в молодой и старой руке (I02: «не выпустишь из рук 30 лет»)')
def _():
    im = photo(B('m90_hands'))
    im, tb = tl(im, [('МЕХАНИК 90-Х', WHITE)], 640)
    return put(im, plate('ВСЯ ЖИЗНЬ', RED, size=84, angle=-3), 30, tb.height + 18)


# --- рисовка Михалыча (пользователь, 12 нояб: «И всё-таки дай обложку в рисовке Михалыча») ---
def _half(path, cx, z=1.0):
    """Половина обложки 640×720 из кадра 16:9: высота кадра → 720, окно 640 по центру cx (доля ширины)."""
    from PIL import ImageEnhance
    im = Image.open(path).convert('RGB'); k = H * z / im.height
    im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    x0 = int(min(max(cx * im.width - W // 4, 0), im.width - W // 2)); y0 = (im.height - H) // 2
    im = im.crop((x0, y0, x0 + W // 2, y0 + H))
    return ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(1.12)).enhance(1.06)

@cover('mechanic90', 'toon_split', 'Рисовка: молодой в 1994 и Михалыч в 2026 — «30 лет в гараже» (кадры KI1 и KZ4, без генерации)')
def _():
    from PIL import ImageDraw
    im = Image.new('RGB', (W, H))
    im.paste(_half(B('m90_toon_young'), 0.68, 1.0), (0, 0)); im.paste(_half(B('m90_toon_old'), 0.52, 1.0), (W // 2, 0))
    d = ImageDraw.Draw(im); d.rectangle([W // 2 - 5, 0, W // 2 + 5, H], fill=WHITE)
    im = put(im, plate('1994', GREEN, size=84, angle=-3), 18, 18)
    im = put(im, plate('2026', RED, size=84, angle=3), W // 2 + 18, 18)
    im, tb = bl(im, [('30 ЛЕТ', YELLOW), ('В ГАРАЖЕ', WHITE)], 420)
    return im

@cover('mechanic90', 'toon_tyres', 'Рисовка: молодой Михалыч с двумя покрышками — «Зарплата покрышками» (A2)')
def _():
    im = photo(B('m90_toon_tyres'), sat=1.08, con=1.05, vign=0.85)
    im, tb = tl(im, [('ЗАРПЛАТА', WHITE), ('ПОКРЫШКАМИ', YELLOW)], 560)
    return put(im, plate('1994', RED, size=120, angle=-3), 30, tb.height + 22)

@cover('mechanic90', 'toon_photo', 'Рисовка: Михалыч смотрит на своё фото в 18 лет — «Это вся моя жизнь» (Z4)')
def _():
    im = photo(B('m90_toon_photo'), sat=1.08, con=1.05, vign=0.85)
    im, tb = tl(im, [('МЕХАНИК С 1994', YELLOW)], 620, y=8)
    return im


if __name__ == '__main__':
    out = os.path.join(HERE, 'out'); os.makedirs(out, exist_ok=True)
    vids = sys.argv[1:] or list(V)
    for v in vids:
        ims = []
        for key, note, fn in V[v]:
            im = fn(); im.save(os.path.join(out, f'{v}_{key}.jpg'), quality=93); ims.append(im)
        sheet = Image.new('RGB', (10 + 3 * 650, 10 + 370 + 190), (242, 242, 242))
        for i, im in enumerate(ims):
            sheet.paste(im.resize((640, 360), Image.LANCZOS), (10 + i * 650, 10))
            sheet.paste(im.resize((320, 180), Image.LANCZOS), (10 + i * 650, 380))
        sheet.save(os.path.join(HERE, f'sheet_{v}.jpg'), quality=85); print('ok', v, [k for k, _, _ in V[v]])
