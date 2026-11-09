"""Обложки длинного «Что будет, если…»: база без текста + текст кодом (функции из thumb2/make.py: Oswald 700, обводка, тень)."""
import sys, os
sys.path.insert(0, '/tmp/claude-0/-home-user-lookme-viewer/8420a68c-a72b-5ef9-9faf-653836f3526a/scratchpad/thumb2')
import make as M
from PIL import Image, ImageEnhance
D = os.path.dirname(os.path.abspath(__file__))
def base(name):
    im = Image.open(os.path.join(D, 'base', name)).convert('RGB').crop((0, 4, 2688, 1516)).resize((M.W, M.H), Image.LANCZOS)
    im = ImageEnhance.Color(im).enhance(1.12); im = ImageEnhance.Contrast(im).enhance(1.06)
    return im.convert('RGBA')
V = {}
def hose():
    im = base('hose.png'); M.headline(im, [('УЕХАЛ', M.WHITE, 150), ('С ПИСТОЛЕТОМ?!', M.YEL, 120)], 24, 4, 560, angle=-4); return im
def diesel():
    im = base('diesel.png'); M.headline(im, [('БЕНЗИН', M.WHITE, 170), ('В ДИЗЕЛЬ?!', M.YEL, 170)], 26, 10, 470, angle=-4)
    M.DELA = M.OSW  # в Dela Gothic нет знака ₽ — плашка шрифтом Oswald
    M.badge(im, 'ДО 60 000 ₽', 40, 548, M.RED, 46, angle=-6); return im
def kettle():
    im = base('kettle.png'); M.headline(im, [('КИПЯТОК', M.YEL, 160), ('НА СТЕКЛО?!', M.WHITE, 150)], 24, 8, 500, angle=-4); return im
V = {'hose': hose, 'diesel': diesel, 'kettle': kettle}
if __name__ == '__main__':
    outs = []
    for n, f in V.items():
        im = f().convert('RGB'); im.save(os.path.join(D, 'out', f'thumb_{n}.jpg'), quality=93); outs.append(im)
    sheet = Image.new('RGB', (380 + 190 + 30, len(outs) * 216 + 10), (240, 240, 240))
    for k, im in enumerate(outs):
        sheet.paste(im.resize((360, 202), Image.LANCZOS), (10, 10 + k * 216)); sheet.paste(im.resize((168, 94), Image.LANCZOS), (390, 10 + k * 216))
    sheet.save(os.path.join(D, 'sheet.jpg'), quality=90); print('ok')
