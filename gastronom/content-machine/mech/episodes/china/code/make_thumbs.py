"""Обложки «Россияне массово продают китайские машины»: база без текста + текст кодом (thumb2/make.py).
На базе badge эмблема похожа на реальный логотип, поэтому закрашиваем её и рисуем нейтральный «?»."""
import sys, os
sys.path.insert(0, '/tmp/claude-0/-home-user-lookme-viewer/8420a68c-a72b-5ef9-9faf-653836f3526a/scratchpad/thumb2')
import make as M
from PIL import Image, ImageEnhance, ImageDraw, ImageFont, ImageFilter
D = os.path.dirname(os.path.abspath(__file__))
def raw(name):
    return Image.open(os.path.join(D, 'base', name)).convert('RGB')
def fit(im):
    im = im.crop((0, 4, 2688, 1516)).resize((M.W, M.H), Image.LANCZOS)
    im = ImageEnhance.Color(im).enhance(1.12); im = ImageEnhance.Contrast(im).enhance(1.06)
    return im.convert('RGBA')
def neutral_emblem(im, cx=698, cy=934, r=152):
    d = ImageDraw.Draw(im)
    for k in range(r, 0, -2):  # тёмный диск с лёгким градиентом
        v = int(38 + 30 * (1 - k / r)); d.ellipse((cx - k, cy - k, cx + k, cy + k), fill=(v, v + 2, v + 6))
    f = ImageFont.truetype(M.OSW, 250)
    q = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(q).text((cx, cy + 6), '?', font=f, anchor='mm', fill=(214, 220, 228, 255))
    im.paste(q, (0, 0), q)
    return im
def lot_a():
    im = fit(raw('lot.png')); M.headline(im, [('ПРОДАЮТ', M.WHITE, 150), ('МАССОВО?', M.YEL, 150)], 30, 16, 600, angle=-4)
    M.DELA = M.OSW; M.badge(im, '+37%', 48, 430, M.RED, 64, angle=-6); return im
def lot_c():
    im = fit(raw('lot.png')); M.headline(im, [('ПОЧЕМУ', M.YEL, 150), ('ПРОДАЮТ?', M.WHITE, 150)], 30, 16, 600, angle=-4)
    M.DELA = M.OSW; M.badge(im, '264 000 ЗА 9 МЕСЯЦЕВ', 48, 430, M.RED, 40, angle=-6); return im
def badge_b():
    im = fit(neutral_emblem(raw('badge.png'))); M.headline(im, [('СМЕНИЛИ', M.WHITE, 140), ('ШИЛЬДИК', M.YEL, 140)], 30, 10, 640, angle=-4); return im
V = {'prodayut': lot_a, 'shildik': badge_b, 'pochemu': lot_c}
if __name__ == '__main__':
    outs = []
    for n, f in V.items():
        im = f().convert('RGB'); im.save(os.path.join(D, 'out', f'thumb_{n}.jpg'), quality=93); outs.append(im)
    sheet = Image.new('RGB', (380 + 190 + 30, len(outs) * 216 + 10), (240, 240, 240))
    for k, im in enumerate(outs):
        sheet.paste(im.resize((360, 202), Image.LANCZOS), (10, 10 + k * 216)); sheet.paste(im.resize((168, 94), Image.LANCZOS), (390, 10 + k * 216))
    sheet.save(os.path.join(D, 'sheet.jpg'), quality=90); print('ok')
