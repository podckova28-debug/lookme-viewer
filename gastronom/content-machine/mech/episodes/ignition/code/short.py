#!/usr/bin/env python3
"""Шорт «Что будет, если на ходу выключить зажигание?» — cutout-анимация кодом, 1080×1920, 30 к/с.
ИИ один раз нарисовал спрайты (spr/*.png) и озвучил реплики (vo/*.mp3); всё движение считается здесь:
колёса, стрелка тахометра, ключ в замке, руль, педаль, плашки, субтитры по словам, звуковые эффекты.

  python short.py --frame 5.0 qa/f.png       — один кадр
  python short.py --sheet qa/sheet.jpg       — лист кадров для проверки
  python short.py --audio work/mix.wav       — только звук
  python short.py --out short.mp4 --parallel 4
"""
import os, sys, math, subprocess, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(D), 'sovhacks'))
import gfx
from gfx import INK, CREAM, RED, OCHRE, GREEN, OSW_B, OSW_M, out_cubic, in_cubic, clamp
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS, SR, TEMPO = 1080, 1920, 30, 48000, 1.08
LZ, BC = Image.LANCZOS, Image.BICUBIC

# ======================= озвучка и тайминг =======================
VO = [('L1', 'vo/L1.mp3'), ('L2', 'vo/L2b.mp3'), ('L3', 'vo/L3b.mp3'), ('L4', 'vo/L4b.mp3'),
      ('L5', 'vo/L5.mp3'), ('L6', 'vo/L6.mp3'), ('L7', 'vo/L7.mp3'), ('L8', 'vo/L8.mp3')]
GAP = dict(L1=0.20, L2=0.45, L3=0.30, L4=0.30, L5=0.30, L6=0.30, L7=0.30, L8=0.35)
TAIL = 0.6
# время слов (faster-whisper, от начала речи, темп 1.08) и подписи к ним
WT = {
 'L1': [-0.08, 0.31, 0.74, 0.98, 1.18, 1.64, 2.14],
 'L2': [-0.14, 0.38, 0.88, 1.29, 1.92, 2.10],
 'L3': [-0.15, 0.35, 1.16, 1.29, 1.57, 1.72, 2.31, 2.87],
 'L4': [-0.15, 0.20, 0.44, 0.64, 0.98, 1.44, 2.40, 2.55, 2.79, 3.40, 3.73, 4.03],
 'L5': [-0.17, 0.22, 0.91, 1.11, 1.33, 1.83, 2.33, 2.72, 2.91, 3.22, 3.70, 4.45, 4.95, 5.39, 5.72, 5.91],
 'L6': [-0.14, 0.15, 0.41, 0.91, 1.13, 2.11, 2.15, 2.54, 3.28, 3.50, 3.82],
 'L7': [-0.12, 0.14, 0.34, 0.68, 0.84, 1.05, 1.18, 1.97, 2.53, 2.79, 3.57, 3.94, 4.44, 4.73, 5.21, 5.33],
 'L8': [-0.16, 0.34, 0.49, 0.56, 0.80, 1.14, 1.60, 1.91, 2.02],
}
WORDS = {
 'L2': ['ЕДЕШЬ', 'ШЕСТЬДЕСЯТ', '— И', 'ЩЁЛК,', 'КЛЮЧ', 'НАЗАД'],
 'L3': ['МОТОР', 'ГЛОХНЕТ,', 'НО', 'МАШИНА', 'ПО', 'ИНЕРЦИИ', 'КАТИТСЯ', 'ДАЛЬШЕ'],
 'L4': ['А', 'ВОТ', 'РУЛЬ', 'ВДРУГ', 'СТАНОВИТСЯ', 'ТЯЖЁЛЫМ', 'ПОТОМУ', 'ЧТО', 'УСИЛИТЕЛЬ', 'БОЛЬШЕ', 'НЕ', 'РАБОТАЕТ'],
 'L5': ['С', 'ТОРМОЗОМ', 'ТО', 'ЖЕ', 'САМОЕ:', 'ПАРА', 'НАЖАТИЙ', '— И', 'ПЕДАЛЬ', 'СТАНОВИТСЯ', 'ТУГОЙ', 'ДАВИТЬ',
        'ПРИДЁТСЯ', 'ИЗО', 'ВСЕХ', 'СИЛ'],
 'L6': ['А', 'ЕСЛИ', 'ВЫДЕРНЕШЬ', 'КЛЮЧ', 'СОВСЕМ,', 'НА', 'МНОГИХ', 'МАШИНАХ', 'РУЛЬ', 'МОЖЕТ', 'ЗАБЛОКИРОВАТЬСЯ'],
 'L7': ['ТАК', 'ЧТО', 'ЗАГЛОХ', 'НА', 'ХОДУ —', 'НЕ', 'ПАНИКУЙ'],
}
CHUNKS = {
 'L2': [[0, 1], [2, 3], [4, 5]],
 'L3': [[0, 1], [2, 3], [4, 5], [6, 7]],
 'L4': [[0, 1, 2], [3, 4], [5], [6, 7], [8], [9, 10, 11]],
 'L5': [[0, 1], [2, 3, 4], [5, 6], [7, 8], [9, 10], [11, 12], [13, 14, 15]],
 'L6': [[0, 1, 2], [3, 4], [5, 6, 7], [8, 9], [10]],
 'L7': [[0, 1, 2], [3, 4], [5, 6]],
}


def load_voice(path):
    raw = subprocess.run([FF, '-v', 'error', '-i', path, '-af', f'atempo={TEMPO}', '-ac', '1', '-ar', str(SR),
                          '-f', 'f32le', '-'], capture_output=True).stdout
    x = np.frombuffer(raw, np.float32).copy()
    nz = np.nonzero(np.abs(x) > 10 ** (-45 / 20))[0]
    x = x[nz[0]: nz[-1] + int(0.05 * SR)]
    f = int(0.004 * SR); x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    return x


VOICE, START, END = {}, {}, {}
_t = 0.0
for _l, _p in VO:
    VOICE[_l] = load_voice(os.path.join(D, _p))
    _t += GAP[_l]; START[_l] = _t; _t += len(VOICE[_l]) / SR; END[_l] = _t
TOTAL = END['L8'] + TAIL
NFR = int(math.ceil(TOTAL * FPS))


def wt(l, i, off=0.06):
    return START[l] + max(0.0, WT[l][i] + off)


# ключевые события
TC = START['L2'] + 1.29 + 0.08          # «щёлк» — ключ в «выкл»
T_PULL = wt('L6', 2) + 0.05              # «выдернешь» — ключ вынимают
T_LOCK = wt('L6', 10)                    # «заблокироваться» — руль клинит
T_HEAVY = wt('L4', 5)                    # «тяжёлым»

SCENES = [
 (0.0, 'hook'),
 (END['L1'] + 0.12, 'road'),
 (wt('L2', 2) - 0.08, 'lock'),
 (TC + 0.35, 'tach'),
 (wt('L3', 2) - 0.10, 'road'),
 (START['L4'] - 0.12, 'steer'),
 (START['L5'] - 0.12, 'brake'),
 (START['L6'] - 0.12, 'lock'),
 (wt('L6', 5) - 0.10, 'steer2'),
 (START['L7'] - 0.12, 'advice'),
]


def scene_at(t):
    i = max(k for k, (t0, _) in enumerate(SCENES) if t0 <= t)
    t0, name = SCENES[i]
    t1 = SCENES[i + 1][0] if i + 1 < len(SCENES) else TOTAL
    return name, t0, t1


# скорость машины, обороты, подсветка приборов
def speed_kmh(t):
    return 60.0 if t < TC else 60.0 - 14.0 * (1 - math.exp(-(t - TC) / 3.0))


def scroll(t):  # пройденный путь фона дороги, px (60 км/ч = 900 px/с)
    if t < TC: return 900.0 * t
    u = t - TC
    return 900.0 * TC + 15.0 * (46.0 * u + 42.0 * (1 - math.exp(-u / 3.0)))


def rpm(t):
    if t < TC + 0.25: return 2.3 + 0.05 * math.sin(2 * math.pi * 9 * t)
    u = (t - TC - 0.25) / 0.9
    if u < 1: return 2.3 * (1 - u) ** 1.6
    q = t - TC - 1.15  # стрелка упирается в ноль и чуть отскакивает
    return -0.10 * math.exp(-q / 0.08) * math.cos(q * 40) if q < 0.4 else 0.0


def backlight(t):
    return 1.0 - 0.85 * clamp((t - TC - 0.9) / 0.5)


# ======================= ассеты =======================
def spr(n): return Image.open(os.path.join(D, 'spr', n + '.png')).convert('RGBA')


def rgb(n): return Image.open(os.path.join(D, 'spr', n + '.png')).convert('RGB')


BG_ROAD, BG_DASH = rgb('bg_road'), rgb('bg_dash')
SB, Y0 = 0.7714, -100                       # масштаб и сдвиг фона дороги
FAR = BG_ROAD.crop((0, 0, 1520, 1690)).resize((round(1520 * SB), round(1690 * SB)), LZ)
GY = Y0 + FAR.height
_strip = BG_ROAD.crop((0, 1690, 1520, 2688)).resize((FAR.width, round(998 * SB)), LZ)
_tile = np.concatenate([np.asarray(_strip), np.asarray(_strip)[:, ::-1]], axis=1).astype(np.float32)


def hblur(a, r):  # горизонтальное размытие движения, бесшовное по кругу
    n = a.shape[1]; ext = np.concatenate([a[:, -r:], a, a[:, :r + 1]], axis=1)
    c = np.cumsum(ext, axis=1); out = (c[:, 2 * r + 1:] - c[:, :-2 * r - 1]) / (2 * r + 1)
    return out[:, :n]


GROUND = Image.fromarray(np.clip(hblur(_tile, 9), 0, 255).astype(np.uint8))
TILE_W = GROUND.width

# фон кабины (1086×1920 → кадр 1080)
DASH = BG_DASH.resize((1086, 1920), LZ).crop((3, 0, 1083, 1920))
DIAL_C, DIAL_R = (538, 1086), 255
LOCK_BG = ImageEnhance.Brightness(DASH.filter(ImageFilter.GaussianBlur(16))).enhance(0.55)
MIH_BG = ImageEnhance.Brightness(BG_ROAD.resize((1086, 1920), LZ).crop((3, 0, 1083, 1920))
                                 .filter(ImageFilter.GaussianBlur(7))).enhance(0.82)


def top_shade(h=900, a=150):
    g = Image.new('L', (1, h)); g.putdata([int(a * (1 - y / h) ** 1.6) for y in range(h)])
    m = Image.new('RGBA', (W, h), (12, 9, 7, 0)); m.putalpha(g.resize((W, h))); return m


SHADE = top_shade()

# машина: кузов + колёса, которые крутим отдельно
CS = 0.43
CAR = spr('car').resize((round(2048 * CS), round(1360 * CS)), LZ)
CAR_X, CAR_Y = round(540 - 1024 * CS), round(1560 - 1068 * CS)
WHEEL_R = 160 * CS
_rd = round(150 * CS)
WHEELS = []
for _cx, _cy in ((414, 910), (1649, 910)):
    cx, cy = _cx * CS, _cy * CS
    box = (round(cx) - _rd - 2, round(cy) - _rd - 2, round(cx) + _rd + 3, round(cy) + _rd + 3)
    disc = CAR.crop(box)
    m = Image.new('L', (disc.width * 4, disc.height * 4), 0)
    ImageDraw.Draw(m).ellipse((8, 8, disc.width * 4 - 9, disc.height * 4 - 9), fill=255)
    m = m.resize(disc.size, LZ)
    disc.putalpha(Image.fromarray((np.asarray(disc.getchannel('A')) * (np.asarray(m) / 255)).astype(np.uint8)))
    WHEELS.append((box[0], box[1], disc))

# ключ: головка + кусочек лезвия, ось вращения — в замочной скважине
KS = 0.61
_key = spr('key').crop((0, 0, 1024, 580))
_key = _key.resize((round(1024 * KS), round(580 * KS)), LZ)
_kp = (round(510 * KS), round(560 * KS))
_kr = int(math.hypot(max(_kp[0], _key.width - _kp[0]), _kp[1])) + 30
KEY = Image.new('RGBA', (2 * _kr, 2 * _kr), (0, 0, 0, 0)); KEY.alpha_composite(_key, (_kr - _kp[0], _kr - _kp[1]))
_ksh = Image.new('RGBA', KEY.size, (0, 0, 0, 0)); _ksh.paste((0, 0, 0, 150), (0, 0), KEY.getchannel('A'))
KEY_SH = _ksh.filter(ImageFilter.GaussianBlur(10))
LOCK_C = (540, 900)
LKS = 1.22  # масштаб замка

# руль с руками
STS = 0.62
STEER = spr('steer').resize((round(2048 * STS), round(2048 * STS)), LZ)
HUB_SPR = (1024 * STS, 1000 * STS)
HUB = (540, 1330)

# педаль и нога — два слоя: педаль качается на оси, нога едет за площадкой
PS = 0.62
_p = spr('pedal')
_pa = np.asarray(_p).copy()
_mask = np.zeros(_pa.shape[:2], bool)
_cre = {860: 1411, 900: 1456, 940: 1475, 980: 1483, 1020: 1484, 1060: 1480, 1100: 1472, 1140: 1461, 1180: 1447,
        1220: 1429, 1260: 1409, 1300: 1384, 1340: 1356, 1380: 1322, 1420: 1283, 1460: 1239, 1500: 1191,
        1540: 1139, 1580: 1086, 1620: 1037}
_ky = sorted(_cre)
for y in range(2048):
    if y < 860: x0 = 1600
    elif y <= 1620: x0 = int(np.interp(y, _ky, [_cre[k] for k in _ky])) + 34
    else: x0 = 1040
    _mask[y, x0:] = True
_ped = _pa.copy(); _ped[~_mask, 3] = 0
_foot = _pa.copy(); _foot[_mask, 3] = 0
PEDAL = Image.fromarray(_ped).resize((round(2048 * PS),) * 2, LZ)
FOOT = Image.fromarray(_foot).resize((round(2048 * PS),) * 2, LZ)
PIV_SPR = (1846 * PS, 107 * PS)
PED_POS = (-181, -20)                       # левый верх спрайта в кадре
PIV = (PED_POS[0] + PIV_SPR[0], PED_POS[1] + PIV_SPR[1])
CONTACT = (PED_POS[0] + 1470 * PS, PED_POS[1] + 1150 * PS)

MIH = {n: spr(n).resize((1100, 1100), LZ) for n in ('mih_wow', 'mih_advice')}

# ======================= текст =======================
_fc = {}


def F(path, size):
    k = (path, size)
    if k not in _fc: _fc[k] = ImageFont.truetype(path, size * 2)
    return _fc[k]


_tc = {}


def cache(key, fn):
    if key not in _tc: _tc[key] = fn()
    return _tc[key]


def down(im): return im.resize((im.width // 2, im.height // 2), LZ)


def text_img(text, size, fill, stroke=0, path=OSW_B, shadow=True):
    def mk():
        f = F(path, size); d0 = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
        l, t, r, b = d0.textbbox((0, 0), text, font=f, stroke_width=stroke * 2)
        im = Image.new('RGBA', (r - l + 40, b - t + 40), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((20 - l, 20 - t), text, font=f, fill=fill, stroke_width=stroke * 2, stroke_fill=INK)
        im = down(im)
        return gfx.shadow(im, r=10, dy=7, a=120)[0] if shadow else im
    return cache(('t', text, size, fill, stroke, path, shadow), mk)


def paste_c(fr, im, cx, cy, a=1.0, sc=1.0, rot=0.0):
    if a <= 0.01: return
    if abs(sc - 1) > 0.005: im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), BC)
    if abs(rot) > 0.05: im = im.rotate(rot, resample=BC, expand=True)
    if a < 0.999: im = gfx.with_alpha(im, a)
    fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def sub_img(words, active, size=92):
    def mk():
        f = F(OSW_B, size); d0 = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
        sp = 24 * 2; ws = [d0.textlength(w_, font=f) for w_ in words]
        tw = sum(ws) + sp * (len(words) - 1)
        im = Image.new('RGBA', (int(tw + 80), int(size * 2 * 1.5)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        x = 40
        for i, w_ in enumerate(words):
            d.text((x, im.height / 2), w_, font=f, fill=OCHRE if i == active else CREAM, anchor='lm',
                   stroke_width=11 * 2, stroke_fill=INK)
            x += ws[i] + sp
        im = down(im)
        if im.width > 940: im = im.resize((940, int(im.height * 940 / im.width)), LZ)
        return gfx.shadow(im, r=12, dy=8, a=130)[0]
    return cache(('s', tuple(words), active, size), mk)


def plate_img(text, size=62, label=None, accent=RED, dot=None):
    def mk():
        f = F(OSW_B, size); fl = F(OSW_M, 28); d0 = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
        tw = d0.textlength(text, font=f); lw = d0.textlength(label, font=fl) + len(label) * 6 if label else 0
        padx = 44 * 2; dotw = (size * 2 * 0.45 + 24 * 2) if dot else 0
        w = int(max(tw + dotw, lw) + padx * 2 + 14 * 2); h = int(size * 2 * 1.45 + (44 * 2 if label else 0))
        im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, w - 1, h - 1), 20 * 2, fill=INK + (236,))
        d.rounded_rectangle((0, 0, 14 * 2, h - 1), 7 * 2, fill=accent)
        y = 22 * 2
        if label:
            gfx.tracked(d, (padx + 14 * 2, y), label, fl, OCHRE, track=3); y += 40 * 2
        cy = y + (h - y) / 2 - 6 * 2
        x = padx + 14 * 2
        if dot:
            r = size * 2 * 0.22; d.ellipse((x, cy - r, x + 2 * r, cy + r), fill=dot); x += 2 * r + 24 * 2
        d.text((x, cy), text, font=f, fill=CREAM, anchor='lm')
        return gfx.shadow(down(im), r=10, dy=8, a=110)[0]
    return cache(('p', text, size, label, accent, dot), mk)


def card_img(num, text):
    def mk():
        fn = F(OSW_B, 84); ft = F(OSW_B, 58)
        w, h, sq = 900 * 2, 132 * 2, 132 * 2
        im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((sq - 30 * 2, 10 * 2, w - 1, h - 10 * 2), 16 * 2, fill=CREAM + (250,))
        d.rounded_rectangle((0, 0, sq, h - 1), 20 * 2, fill=RED)
        d.text((sq / 2, h / 2 - 4 * 2), str(num), font=fn, fill=CREAM, anchor='mm')
        d.text((sq + 34 * 2, h / 2 - 2 * 2), text, font=ft, fill=INK, anchor='lm')
        return gfx.shadow(down(im), r=12, dy=9, a=120)[0]
    return cache(('c', num, text), mk)


def speed_img(v):
    def mk():
        fl = F(OSW_M, 28); fb = F(OSW_B, 120); fu = F(OSW_B, 46)
        w, h = 400 * 2, 230 * 2
        im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, w - 1, h - 1), 22 * 2, fill=INK + (236,))
        d.rounded_rectangle((0, 0, 14 * 2, h - 1), 7 * 2, fill=OCHRE)
        gfx.tracked(d, (48 * 2, 22 * 2), 'СКОРОСТЬ', fl, OCHRE, track=4)
        d.text((48 * 2, 150 * 2), str(v), font=fb, fill=CREAM, anchor='ls')
        nx = 48 * 2 + d.textlength(str(v), font=fb) + 16 * 2
        d.text((nx, 146 * 2), 'КМ/Ч', font=fu, fill=CREAM, anchor='ls')
        return gfx.shadow(down(im), r=10, dy=8, a=110)[0]
    return cache(('v', v), mk)


# ======================= приборы, замок, замок руля =======================
def ang_v(v):  # значение 0..8 → угол (рад), 0 внизу слева, 8 внизу справа
    return math.radians(225 - v * 33.75)


def _dial(lit):
    R, S2 = DIAL_R, 2
    n = (R + 30) * 2 * S2
    im = Image.new('RGBA', (n, n), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    c = n / 2
    on = CREAM if lit else (88, 88, 94); red = RED if lit else (92, 40, 36)
    a0, a1 = 225 - 6.5 * 33.75, 225 - 8 * 33.75
    rr = (R - 14) * S2
    d.arc((c - rr, c - rr, c + rr, c + rr), -a0, -a1, fill=red, width=16 * S2)
    for i in range(17):
        v = i / 2; a = ang_v(v); major = i % 2 == 0
        r1, r2 = (R - 4) * S2, (R - (36 if major else 22)) * S2
        col = (red if v >= 6.5 else on)
        d.line((c + r1 * math.cos(a), c - r1 * math.sin(a), c + r2 * math.cos(a), c - r2 * math.sin(a)),
               fill=col, width=(7 if major else 4) * S2)
    f = ImageFont.truetype(OSW_B, 54 * S2)
    for v in range(9):
        a = ang_v(v); r = (R - 82) * S2
        d.text((c + r * math.cos(a), c - r * math.sin(a)), str(v), font=f, fill=(red if v >= 7 else on), anchor='mm')
    fs = ImageFont.truetype(OSW_M, 26 * S2)
    d.text((c, c + 92 * S2), '×1000 ОБ/МИН', font=fs, fill=OCHRE if lit else (80, 80, 86), anchor='mm')
    im = im.resize((n // S2, n // S2), LZ)
    if lit:  # подсветка — мягкое свечение
        glow = Image.new('RGBA', im.size, (0, 0, 0, 0))
        glow.paste((255, 196, 120, 255), (0, 0), im.getchannel('A'))
        glow = glow.filter(ImageFilter.GaussianBlur(9)); glow = gfx.with_alpha(glow, 0.75)
        glow.alpha_composite(im); im = glow
    return im


DIAL_ON, DIAL_OFF = _dial(True), _dial(False)


def draw_dial(fr, t, value):
    b = backlight(t)
    im = Image.blend(DIAL_OFF, DIAL_ON, b) if 0.01 < b < 0.99 else (DIAL_ON if b >= 0.99 else DIAL_OFF)
    fr.alpha_composite(im, (DIAL_C[0] - im.width // 2, DIAL_C[1] - im.height // 2))
    # стрелка
    S2 = 2; n = 600 * S2
    nd = Image.new('RGBA', (n, n), (0, 0, 0, 0)); d = ImageDraw.Draw(nd); c = n / 2
    a = ang_v(value); ca, sa = math.cos(a), math.sin(a); px, py = -sa, -ca
    L, T, w0, w1 = (DIAL_R - 30) * S2, 44 * S2, 9 * S2, 3 * S2
    pts = [(c + ca * L + px * w1, c - sa * L + py * w1), (c + ca * L - px * w1, c - sa * L - py * w1),
           (c - ca * T - px * w0, c + sa * T - py * w0), (c - ca * T + px * w0, c + sa * T + py * w0)]
    d.polygon(pts, fill=(244, 92, 40), outline=INK)
    d.ellipse((c - 30 * S2, c - 30 * S2, c + 30 * S2, c + 30 * S2), fill=(40, 40, 44), outline=(150, 150, 156), width=5 * S2)
    nd = nd.resize((n // S2, n // S2), LZ)
    fr.alpha_composite(gfx.shadow(nd, r=6, dy=6, a=110)[0], (DIAL_C[0] - 300 - 18, DIAL_C[1] - 300 - 18))


def _lock_face(state):
    S2 = 2; n = 900 * S2
    im = Image.new('RGBA', (n, n), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = n / 2
    for i in range(30):  # хромовое кольцо — градиент
        r = (235 - i * 1.2) * S2; v = int(105 + 85 * math.sin(i / 29 * math.pi) ** 2)
        d.ellipse((c - r, c - r, c + r, c + r), fill=(v, v, v + 6))
    d.arc((c - 222 * S2, c - 222 * S2, c + 222 * S2, c + 222 * S2), 200, 290, fill=(245, 245, 250), width=7 * S2)
    d.ellipse((c - 235 * S2, c - 235 * S2, c + 235 * S2, c + 235 * S2), outline=INK, width=8 * S2)
    d.ellipse((c - 196 * S2, c - 196 * S2, c + 196 * S2, c + 196 * S2), fill=(36, 36, 40), outline=INK, width=6 * S2)
    d.ellipse((c - 150 * S2, c - 150 * S2, c + 150 * S2, c + 150 * S2), outline=(58, 58, 64), width=4 * S2)
    f = ImageFont.truetype(OSW_B, 62 * S2)
    for name, ang, col in (('ВЫКЛ', -40, RED), ('ВКЛ', 40, GREEN)):
        a = math.radians(90 - ang); act = (state == name)
        r = 372 * S2
        cc = col if act else (150, 146, 140)
        tx, ty = c + r * math.cos(a), c - r * math.sin(a)
        if act:
            tw = d.textlength(name, font=f)
            d.rounded_rectangle((tx - tw / 2 - 20 * S2, ty - 44 * S2, tx + tw / 2 + 20 * S2, ty + 44 * S2), 14 * S2,
                                fill=INK + (230,))
        d.text((tx, ty), name, font=f, fill=cc if act else (210, 204, 196), anchor='mm', stroke_width=0 if act else 6 * S2,
               stroke_fill=INK)
        r1, r2 = 244 * S2, 268 * S2  # риска
        d.line((c + r1 * math.cos(a), c - r1 * math.sin(a), c + r2 * math.cos(a), c - r2 * math.sin(a)),
               fill=cc if act else (200, 196, 190), width=8 * S2)
    im = im.resize((int(n / S2 * LKS), int(n / S2 * LKS)), LZ)
    return gfx.shadow(im, r=16, dy=14, a=150)[0]


def _slot():
    im = Image.new('RGBA', (120, 120), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((44, 18, 76, 102), 8, fill=(10, 10, 12), outline=(70, 70, 76), width=3)
    return im.resize((146, 146), LZ)


LOCK_FACE = {s: _lock_face(s) for s in ('ВКЛ', 'ВЫКЛ')}
SLOT = _slot()


def padlock_img():
    def mk():
        S2 = 2; w, h = 240 * S2, 280 * S2
        im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.arc((50 * S2, 10 * S2, 190 * S2, 170 * S2), 180, 360, fill=INK, width=44 * S2)
        d.arc((58 * S2, 18 * S2, 182 * S2, 162 * S2), 180, 360, fill=(190, 190, 196), width=28 * S2)
        d.rectangle((50 * S2, 88 * S2, 94 * S2, 130 * S2), fill=INK); d.rectangle((146 * S2, 88 * S2, 190 * S2, 130 * S2), fill=INK)
        d.rectangle((58 * S2, 88 * S2, 86 * S2, 130 * S2), fill=(190, 190, 196)); d.rectangle((154 * S2, 88 * S2, 182 * S2, 130 * S2), fill=(190, 190, 196))
        d.rounded_rectangle((14 * S2, 118 * S2, 226 * S2, 270 * S2), 26 * S2, fill=RED, outline=INK, width=9 * S2)
        d.ellipse((102 * S2, 160 * S2, 138 * S2, 196 * S2), fill=INK)
        d.polygon([(110 * S2, 186 * S2), (130 * S2, 186 * S2), (136 * S2, 232 * S2), (104 * S2, 232 * S2)], fill=INK)
        return gfx.shadow(down(im), r=12, dy=10, a=140)[0]
    return cache('padlock', mk)


# ======================= сцены =======================
def e_back(x, s=1.70158):
    x = clamp(x) - 1; return 1 + (s + 1) * x ** 3 + s * x ** 2


def draw_car(fr, t):
    s = scroll(t); v = speed_kmh(t) * 15
    run = t < TC
    # линии скорости
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for i, (y, ln) in enumerate(((1170, 260), (1250, 340), (1330, 220), (1420, 300), (1480, 200))):
        x = (W + 500) - ((s * 1.25 + i * 431) % (W + 900))
        a = int(120 * min(1, v / 900))
        d.rounded_rectangle((x, y, x + ln, y + 7), 4, fill=(255, 255, 255, a))
    fr.alpha_composite(ov)
    # тень
    sh = cache('carsh', lambda: _carsh())
    fr.alpha_composite(sh, (CAR_X + 20, 1530))
    # выхлоп, пока мотор работает
    if t < TC + 0.4:
        sm = Image.new('RGBA', (420, 220), (0, 0, 0, 0)); d = ImageDraw.Draw(sm)
        ox, oy = CAR_X + 18 - 360, CAR_Y + 428 - 150
        for k in range(int(t / 0.11) - 7, int(t / 0.11) + 1):
            tk = k * 0.11; age = t - tk
            if age < 0 or age > 0.75 or tk > TC: continue
            rnd = random.Random(k)
            px = 360 - age * 260 - rnd.random() * 10; py = 150 - age * 40 + rnd.random() * 8
            r = 12 + age * 40; a = int(70 * (1 - age / 0.75))
            d.ellipse((px - r, py - r, px + r, py + r), fill=(225, 222, 215, a))
        fr.alpha_composite(sm.filter(ImageFilter.GaussianBlur(9)), (ox, oy))
    bounce = (1.6 * math.sin(2 * math.pi * 11 * t) if run else 0.0)
    fr.alpha_composite(CAR, (CAR_X, int(CAR_Y + bounce)))
    ang = math.degrees(s / WHEEL_R); dstep = math.degrees(v / FPS / WHEEL_R)
    nsamp = int(clamp(dstep / 4 / 12) * 12) + 1
    for (bx, by, disc) in WHEELS:
        if nsamp <= 1:
            im = disc.rotate(-ang, resample=BC)
        else:
            acc = np.zeros((disc.height, disc.width, 4), np.float32)
            for j in range(nsamp):
                acc += np.asarray(disc.rotate(-(ang - dstep * j / nsamp), resample=BC), np.float32)
            im = Image.fromarray((acc / nsamp).astype(np.uint8))
        fr.alpha_composite(im, (CAR_X + bx, CAR_Y + by))


def _carsh():
    m = Image.new('RGBA', (CAR.width - 40, 70), (0, 0, 0, 0))
    ImageDraw.Draw(m).ellipse((0, 10, m.width, 60), fill=(0, 0, 0, 130))
    return m.filter(ImageFilter.GaussianBlur(12))


def scene_road(t, lt):
    fr = Image.new('RGB', (W, H))
    s = scroll(t)
    fx = -int(min(FAR.width - W, 10 + s * 0.011))
    fr.paste(FAR, (fx, Y0))
    gx = -int(s % TILE_W)
    fr.paste(GROUND, (gx, GY)); fr.paste(GROUND, (gx + TILE_W, GY))
    fr = fr.convert('RGBA')
    draw_car(fr, t)
    return fr


def scene_tach(t, lt):
    fr = DASH.convert('RGBA')
    draw_dial(fr, t, rpm(t))
    return fr


def key_state(t):
    """угол головки ключа (PIL, + против часовой), насколько вынут (0..1)"""
    if t < TC: a = -40.0
    else:
        k = clamp((t - TC) / 0.13); a = -40 + 80 * e_back(k, 2.2)
    out = clamp((t - T_PULL) / 0.32) if t > T_PULL - 0.5 else 0.0
    return a, out


def scene_lock(t, lt):
    fr = LOCK_BG.convert('RGBA')
    st = 'ВКЛ' if t < TC + 0.06 else 'ВЫКЛ'
    face = LOCK_FACE[st]
    fr.alpha_composite(face, (LOCK_C[0] - face.width // 2, LOCK_C[1] - face.height // 2))
    a, out = key_state(t)
    sl = SLOT.rotate(a, resample=BC)
    fr.alpha_composite(sl, (LOCK_C[0] - 73, LOCK_C[1] - 73))
    if out < 1:
        k = out_cubic(out); sc = 1 + 0.45 * k; alpha = 1 - k
        sh = KEY_SH.rotate(a, resample=BC)
        paste_c(fr, sh, LOCK_C[0] + 14 + 40 * k, LOCK_C[1] + 16 + 50 * k, alpha * (1 - 0.5 * k), sc * (1 + 0.1 * k))
        km = KEY.rotate(a, resample=BC)
        paste_c(fr, km, LOCK_C[0], LOCK_C[1] - 60 * k, alpha, sc)
    return fr


def steer_angle(t, name):
    if name == 'steer':
        lt = t - START['L4']
        a = -3.0 * out_cubic((lt - 0.35) / 0.5)
        if t > T_HEAVY - 0.2:
            k = (t - T_HEAVY + 0.2) / 3.0
            a += -3.2 * out_cubic(k) + 0.9 * math.sin(t * 2 * math.pi * 13) * min(1, k * 4)
        return a
    t0 = wt('L6', 8)  # «руль» — пробует повернуть
    if t < T_LOCK:
        return -7.0 * out_cubic((t - t0 + 0.1) / 0.55)
    q = t - T_LOCK
    return -7.0 * out_cubic((T_LOCK - t0 + 0.1) / 0.55) + 2.0 * math.exp(-q / 0.12) * math.cos(q * 45)


def scene_steer(t, lt, name):
    fr = DASH.convert('RGBA')
    draw_dial(fr, t, 0.0)
    a = steer_angle(t, name)
    im = STEER.rotate(a, resample=BC, center=HUB_SPR)
    fr.alpha_composite(im, (int(HUB[0] - HUB_SPR[0]), int(HUB[1] - HUB_SPR[1])))
    strain = (name == 'steer' and t > T_HEAVY - 0.1) or (name == 'steer2' and wt('L6', 8) < t < T_LOCK + 0.6)
    if strain:  # штрихи усилия у рук
        d = ImageDraw.Draw(fr); ph = int(t * 10) % 2
        for (hx, hy), angs in (((HUB[0] - 345, HUB[1] - 400), (115, 140, 165)), ((HUB[0] + 335, HUB[1] - 345), (65, 40, 15))):
            for ag in angs:
                ang = math.radians(ag); r0, r1 = 85 + ph * 10, 135 + ph * 10
                d.line((hx + r0 * math.cos(ang), hy - r0 * math.sin(ang), hx + r1 * math.cos(ang), hy - r1 * math.sin(ang)),
                       fill=CREAM + (255,), width=10)
    if name == 'steer2' and t >= T_LOCK - 0.02:
        q = t - T_LOCK
        if q < 0.5:  # красная вспышка-кольцо
            ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
            r = 120 + q * 900; al = int(200 * (1 - q / 0.5))
            d.ellipse((HUB[0] - r, HUB[1] - r, HUB[0] + r, HUB[1] + r), outline=RED + (al,), width=18)
            fr.alpha_composite(ov)
        sc = 1.0 + 0.7 * (1 - out_cubic(q / 0.12))
        paste_c(fr, padlock_img(), HUB[0], HUB[1] - 40, min(1, q / 0.06), sc)
    return fr


def pedal_angle(t):
    lt = t - START['L5']
    def press(t0, depth, dn=0.17, hold=0.07, up=0.22):
        x = lt - t0
        if x < 0 or x > dn + hold + up: return 0.0
        if x < dn: return depth * out_cubic(x / dn)
        if x < dn + hold: return depth
        return depth * (1 - in_cubic((x - dn - hold) / up) ** 0.6)
    a = press(WT['L5'][5] + 0.02, 12) + press(WT['L5'][6] + 0.02, 12)
    t3 = WT['L5'][9]
    if lt > t3:  # тугая: еле идёт
        a += 2.6 * out_cubic((lt - t3) / 0.5)
        t4 = WT['L5'][11]
        if lt > t4:
            k = (lt - t4) / 1.6
            a += 2.6 * out_cubic(k) + 0.45 * math.sin(lt * 2 * math.pi * 15) * min(1, k * 3)
    return a


def scene_brake(t, lt):
    fr = cache('brakebg', _brake_bg).copy()
    a = pedal_angle(t)
    th = math.radians(a)
    dx, dy = CONTACT[0] - PIV[0], CONTACT[1] - PIV[1]
    nx = math.cos(th) * dx + math.sin(th) * dy; ny = -math.sin(th) * dx + math.cos(th) * dy
    mx, my = nx - dx, ny - dy
    pim = PEDAL.rotate(a, resample=BC, center=PIV_SPR)
    fr.alpha_composite(pim, PED_POS)
    fr.alpha_composite(FOOT, (int(PED_POS[0] + mx), int(PED_POS[1] + my)))
    return fr


def _brake_bg():
    im = Image.new('RGB', (W, H))
    y = np.linspace(0, 1, H)[:, None]; x = np.linspace(-1, 1, W)[None, :]
    base = 64 - 30 * y - 14 * x ** 2
    arr = np.stack([base + 4, base + 1, base - 2], -1)
    floor = (np.arange(H)[:, None] > (1165 + (np.arange(W)[None, :] / W) * 100))
    rnd = np.random.default_rng(3).normal(0, 3.5, (H, W))
    arr = np.where(floor[..., None], (np.stack([30 + 0 * y + 0 * x] * 3, -1) + rnd[..., None] - 4 * y[..., None]), arr)
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    d.line([(0, 1165), (W, 1265)], fill=(20, 18, 17), width=6)
    return im.convert('RGBA')


def mih_draw(fr, t, lt, name, jolt=None, nods=()):
    im = MIH[name]
    br = math.sin(2 * math.pi * t / 2.4)
    sc = 1 + 0.008 * br
    rot = 0.8 * math.sin(2 * math.pi * t / 3.1)
    if lt < 0.3: sc *= 0.93 + 0.07 * e_back(lt / 0.3)
    for tj in ([jolt] if jolt else []) + list(nods):
        q = t - tj
        if 0 <= q < 0.4: sc *= 1 + 0.035 * math.sin(q / 0.4 * math.pi)
    w_ = int(im.width * sc); h_ = int(im.height * sc)
    m = im.resize((w_, h_), BC) if abs(sc - 1) > 0.002 else im
    if abs(rot) > 0.05: m = m.rotate(rot, resample=BC, center=(w_ / 2, h_))
    fr.alpha_composite(m, (int(540 - w_ / 2), int(H + 40 - h_ + 4 * br)))


def scene_hook(t, lt):
    fr = MIH_BG.convert('RGBA'); fr.alpha_composite(SHADE)
    mih_draw(fr, t, lt, 'mih_wow', jolt=wt('L1', 6))
    return fr


def scene_advice(t, lt):
    fr = MIH_BG.convert('RGBA'); fr.alpha_composite(SHADE)
    mih_draw(fr, t, lt, 'mih_advice', nods=(wt('L7', 7), wt('L7', 10), wt('L7', 13), wt('L8', 5)))
    return fr


SCENE_FN = dict(hook=scene_hook, road=scene_road, lock=scene_lock, tach=scene_tach, brake=scene_brake,
                advice=scene_advice)

# ======================= наложения =======================
def subtitles():
    out = []
    ys = dict(L2=None, L3=None, L4=700, L5=1430, L6=None, L7=760)
    for l, chunks in CHUNKS.items():
        for ci, ch in enumerate(chunks):
            t0 = max(START[l] - 0.05, wt(l, ch[0]))
            t1 = wt(l, chunks[ci + 1][0]) if ci + 1 < len(chunks) else END[l] + 0.2
            out.append(dict(l=l, words=[WORDS[l][i] for i in ch], times=[wt(l, i) for i in ch], t0=t0, t1=t1))
    return out


SUBS = subtitles()
SUB_Y = dict(road=930, lock=1500, tach=1460, steer=700, steer2=700, brake=1490, advice=780, hook=None)


def draw_subs(fr, t, scene):
    y = SUB_Y.get(scene)
    if y is None: return
    for s in SUBS:
        if s['t0'] <= t < s['t1']:
            if s['l'] == 'L7' and t > wt('L7', 7) - 0.1: return
            act = max([i for i, tt in enumerate(s['times']) if tt <= t] or [0])
            im = sub_img(s['words'], act)
            k = out_cubic((t - s['t0']) / 0.12)
            paste_c(fr, im, 540, y, 1.0, 0.86 + 0.14 * k)


def appear(t, t0, t1, fin=0.25, fout=0.2):
    if t < t0 or t >= t1: return 0.0
    return out_cubic((t - t0) / fin) * (1 - in_cubic((t - (t1 - fout)) / fout))


def overlays(fr, t, scene, lt, t0s, t1s):
    # — заголовок крючка
    if scene == 'hook':
        lines = [('ЧТО БУДЕТ, ЕСЛИ', 104, CREAM, 0.0), ('НА ХОДУ', 104, CREAM, wt('L1', 3)),
                 ('ВЫКЛЮЧИТЬ', 132, OCHRE, wt('L1', 5)), ('ЗАЖИГАНИЕ?', 132, OCHRE, wt('L1', 6))]
        y = 250
        for text, size, col, ta in lines:
            im = text_img(text, size, col, stroke=7)
            k = out_cubic((t - ta) / 0.3) if ta > 0 else 1.0
            if k > 0: paste_c(fr, im, 540, y + 26 * (1 - k), k, 1.0 if ta == 0 else 0.9 + 0.1 * k)
            y += int(size * 1.22)
    # — скорость на дороге
    if scene == 'road':
        v = int(round(speed_kmh(t)))
        k = out_cubic(lt / 0.25)
        paste_c(fr, speed_img(v), 540, 300 - 20 * (1 - k), k)
        if t > TC:
            k2 = out_cubic((t - t0s - 0.15) / 0.25)
            paste_c(fr, plate_img('МОТОР ВЫКЛЮЧЕН', 44, dot=RED, accent=RED), 540, 470 - 16 * (1 - k2), k2)
    if scene == 'lock' and t < START['L3']:
        q = t - TC
        if 0 <= q < 0.75:
            k = out_cubic(q / 0.12); a = 1 - in_cubic((q - 0.55) / 0.2)
            paste_c(fr, text_img('ЩЁЛК!', 150, OCHRE, stroke=9), 770, 330, a, 0.6 + 0.4 * e_back(k), -10)
    if scene == 'tach':
        ta = wt('L3', 1)
        k = appear(t, ta, t1s + 1)
        paste_c(fr, plate_img('МОТОР ЗАГЛОХ', 66, accent=RED), 540, 330 - 20 * (1 - out_cubic((t - ta) / 0.25)), k)
    if scene == 'steer':
        if t > T_HEAVY:
            gfx.stamp(fr, t - T_HEAVY, wt('L4', 8) - T_HEAVY - 0.05, 'ТЯЖЁЛЫЙ', None, 'red', 540, 300)
        ta = wt('L4', 8)
        k = appear(t, ta, t1s + 1)
        paste_c(fr, plate_img('УСИЛИТЕЛЬ РУЛЯ ВЫКЛЮЧЕН', 50, dot=RED), 540, 300 - 20 * (1 - out_cubic((t - ta) / 0.25)), k)
    if scene == 'brake':
        draw_brake_gauge(fr, t)
        ta = wt('L5', 10)
        if t > ta: gfx.stamp(fr, t - ta, 1.6, 'ТУГАЯ', None, 'red', 560, 300)
    if scene == 'steer2' and t > T_LOCK:
        gfx.stamp(fr, t - T_LOCK, 3.0, 'ЗАБЛОКИРОВАН', 'РУЛЬ', 'red', 540, 300)
    if scene == 'advice':
        tp = wt('L7', 5)
        if tp < t < wt('L7', 7) - 0.1:
            gfx.stamp(fr, t - tp, wt('L7', 7) - 0.1 - tp, 'НЕ ПАНИКУЙ', None, 'green', 540, 330)
        cards = [(1, 'ДЕРЖИ РУЛЬ КРЕПЧЕ', wt('L7', 7)), (2, 'ТОРМОЗИ СИЛЬНЕЕ', wt('L7', 10)),
                 (3, 'УХОДИ К ОБОЧИНЕ', wt('L7', 13))]
        tend = START['L8'] - 0.1
        for i, (n, text, ta) in enumerate(cards):
            k = appear(t, ta, tend + 0.2, 0.3, 0.2)
            if k > 0:
                im = card_img(n, text)
                fr.alpha_composite(gfx.with_alpha(im, k), (int(540 - im.width / 2 - 60 * (1 - k)), int(230 + i * 170)))
        if t > START['L8'] - 0.1:
            y = 260
            for text, size, col, ta in (('ЗНАЛ ЛИ ТЫ', 112, CREAM, START['L8'] - 0.05),
                                        ('ПРО «КАМЕННЫЙ»', 112, OCHRE, wt('L8', 4)), ('РУЛЬ?', 112, OCHRE, wt('L8', 5))):
                k = out_cubic((t - ta) / 0.3)
                if k > 0: paste_c(fr, text_img(text, size, col, stroke=7), 540, y + 26 * (1 - k), k)
                y += 132
            ta = wt('L8', 6)
            k = out_cubic((t - ta) / 0.3)
            if k > 0:
                paste_c(fr, plate_img('ПИШИ В КОММЕНТАРИЯХ', 56, accent=OCHRE), 540, 700 + 20 * (1 - k), k)
                d = ImageDraw.Draw(fr); bob = 10 * math.sin((t - ta) * 7)
                cx, cy = 540, 800 + bob
                d.polygon([(cx - 34, cy), (cx + 34, cy), (cx, cy + 40)], fill=OCHRE + (int(255 * k),), outline=INK)


def draw_brake_gauge(fr, t):
    """Запас усилителя: две «порции» на два нажатия, потом — сила ноги."""
    lt = t - START['L5']
    p1, p2 = WT['L5'][5] + 0.2, WT['L5'][6] + 0.2
    t4 = WT['L5'][11]
    k_in = out_cubic((t - SCENES[6][0]) / 0.25)
    S2 = 2; w, h = 900 * S2, 214 * S2
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 22 * S2, fill=INK + (238,))
    fl = F(OSW_M, 36); fb = F(OSW_B, 70)
    if lt < t4:
        empty = lt >= p2
        d.rounded_rectangle((0, 0, 14 * S2, h - 1), 7 * S2, fill=RED if empty else GREEN)
        gfx.tracked(d, (46 * S2, 22 * S2), 'ЗАПАС УСИЛИТЕЛЯ ТОРМОЗА', fl, OCHRE, track=3)
        for i, pt in enumerate((p1, p2)):
            x0 = 46 * S2 + i * 190 * S2; full = lt < pt
            fk = clamp((lt - pt) / 0.15) if not full else 0
            col = GREEN if full else tuple(int(72 + (GREEN[j] + 120 - 72) * (1 - fk) * 0.6) for j in range(3))
            d.rounded_rectangle((x0, 86 * S2, x0 + 166 * S2, 186 * S2), 16 * S2, fill=col, outline=CREAM, width=4 * S2)
            d.text((x0 + 83 * S2, 134 * S2), str(i + 1), font=F(OSW_B, 64), fill=CREAM if full else (40, 40, 44), anchor='mm')
        d.text((440 * S2, 134 * S2), 'ПУСТО' if empty else 'ЕСТЬ', font=fb, fill=RED if empty else GREEN, anchor='lm')
    else:
        k = out_cubic((lt - t4) / 1.4)
        d.rounded_rectangle((0, 0, 14 * S2, h - 1), 7 * S2, fill=RED)
        gfx.tracked(d, (46 * S2, 22 * S2), 'СИЛА НАЖАТИЯ', fl, OCHRE, track=3)
        x0, x1 = 46 * S2, 620 * S2
        d.rounded_rectangle((x0, 92 * S2, x1, 178 * S2), 18 * S2, fill=(60, 56, 52))
        xf = x0 + (x1 - x0) * (0.25 + 0.75 * k)
        col = tuple(int(OCHRE[j] + (RED[j] - OCHRE[j]) * k) for j in range(3))
        d.rounded_rectangle((x0, 92 * S2, xf, 178 * S2), 18 * S2, fill=col)
        d.text((650 * S2, 135 * S2), 'МАКС' if k > 0.9 else f'{int(25 + 75 * k)}%', font=fb, fill=RED if k > 0.9 else CREAM, anchor='lm')
    im = gfx.shadow(down(im), r=10, dy=8, a=110)[0]
    paste_c(fr, im, 540, 1300 + 20 * (1 - k_in), k_in)


# ======================= камера: толчок на склейке, тряска, наезд =======================
SHAKES = [(TC, 7, 0.25), (T_LOCK, 14, 0.4)]


def camera(t, scene, lt, t0s, t1s):
    z = 1.0; cx, cy = W / 2, H / 2
    if scene in ('tach',): z = 1.0 + 0.10 * out_cubic(lt / 1.6); cx, cy = DIAL_C
    if scene in ('steer', 'steer2'): z = 1.0 + 0.035 * (lt / max(0.1, t1s - t0s)); cy = 1100
    if scene in ('hook', 'advice'): z = 1.0 + 0.02 * (lt / max(0.1, t1s - t0s))
    if scene == 'lock': z = 1.0 + 0.04 * (lt / max(0.1, t1s - t0s)); cx, cy = LOCK_C
    if t0s > 0 and lt < 0.2: z *= 1.05 - 0.05 * out_cubic(lt / 0.2)
    sx = sy = 0.0
    for ts, amp, dur in SHAKES:
        q = t - ts
        if 0 <= q < dur:
            a = amp * (1 - q / dur); sx += a * math.sin(q * 97); sy += a * math.cos(q * 71)
    if scene == 'steer' and t > T_HEAVY: sx += 1.6 * math.sin(t * 83); sy += 1.2 * math.cos(t * 67)
    if scene == 'brake' and t > wt('L5', 11): sx += 1.8 * math.sin(t * 79); sy += 1.4 * math.cos(t * 61)
    return z, cx, cy, sx, sy


def render(t):
    scene, t0s, t1s = scene_at(t)
    lt = t - t0s
    if scene in ('steer', 'steer2'): fr = scene_steer(t, lt, scene)
    else: fr = SCENE_FN[scene](t, lt)
    z, cx, cy, sx, sy = camera(t, scene, lt, t0s, t1s)
    if abs(z - 1) > 0.001 or abs(sx) > 0.05 or abs(sy) > 0.05:
        fr = fr.transform((W, H), Image.AFFINE, (1 / z, 0, cx - cx / z + sx, 0, 1 / z, cy - cy / z + sy), resample=BC)
    overlays(fr, t, scene, lt, t0s, t1s)
    draw_subs(fr, t, scene)
    return fr.convert('RGB')


# ======================= звук =======================
def synth():
    n = int(TOTAL * SR) + SR
    rng = np.random.default_rng(7)
    voice = np.zeros(n, np.float32); sfx = np.zeros(n, np.float32)
    for l, x in VOICE.items():
        i = int(START[l] * SR); voice[i:i + len(x)] += x

    def put(t, y, g=1.0):
        i = int(t * SR); j = min(n, i + len(y)); sfx[i:j] += g * y[:j - i]

    def tt(d): return np.arange(int(d * SR)) / SR

    def noise(d): return rng.standard_normal(int(d * SR)).astype(np.float32)

    def lp(x, a):  # однополюсный ФНЧ
        y = np.empty_like(x); acc = 0.0
        for i in range(len(x)): acc += a * (x[i] - acc); y[i] = acc
        return y

    def lp_fast(x, k):
        c = np.cumsum(np.concatenate([[0], x])); return ((c[k:] - c[:-k]) / k).astype(np.float32)

    # мотор: от начала дорожной сцены до щелчка + затухание
    r0 = SCENES[1][0]
    d = TC + 1.2 - r0; u = tt(d); tabs = r0 + u
    f0 = np.where(tabs < TC, 76.0, 76.0 * np.exp(-(tabs - TC) / 0.35) + 6)
    ph = 2 * np.pi * np.cumsum(f0) / SR
    eng = sum(np.sin(k * ph + k) / k for k in range(1, 7)) * (1 + 0.25 * np.sin(2 * np.pi * 13 * u))
    rumble = lp_fast(noise(d + 0.01), 60)[:len(u)] * 3
    amp = np.where(tabs < TC, 1.0, np.exp(-(tabs - TC) / 0.3))
    amp *= np.clip((u) / 0.15, 0, 1)
    put(r0, ((eng * 0.6 + rumble) * amp).astype(np.float32), 0.05)
    # затихающие «чихи» мотора
    for k, dt_ in enumerate((0.12, 0.3, 0.52)):
        y = lp_fast(noise(0.09), 12)[:int(0.08 * SR)] * np.exp(-tt(0.08) / 0.03); put(TC + dt_, y, 0.25 / (k + 1))
    # щелчок ключа
    for dt_, g in ((0.0, 0.6), (0.035, 0.4)):
        y = noise(0.006) * np.exp(-tt(0.006) / 0.0015); put(TC + dt_, y, g)
        put(TC + dt_, np.sin(2 * np.pi * 2600 * tt(0.03)) * np.exp(-tt(0.03) / 0.006), g * 0.4)
    # шум колёс на дороге
    for (t0, nm) in SCENES:
        pass
    # «пшш» на двух нажатиях тормоза
    for i in (5, 6):
        ts = START['L5'] + WT['L5'][i] + 0.04
        y = noise(0.4); y = y - lp_fast(np.concatenate([y, y[:7]]), 8)[:len(y)]
        put(ts, y * np.minimum(1, tt(0.4) / 0.02) * np.exp(-tt(0.4) / 0.12), 0.10)
    # глухой удар третьего нажатия
    ts = START['L5'] + WT['L5'][9]
    put(ts, np.sin(2 * np.pi * 70 * tt(0.2)) * np.exp(-tt(0.2) / 0.06), 0.25)
    # ключ вынимают: металлический шорох
    y = noise(0.18); y = y - lp_fast(np.concatenate([y, y[:5]]), 6)[:len(y)]
    put(T_PULL, y * np.sin(np.linspace(0, np.pi, len(y))), 0.12)
    # клац замка руля
    put(T_LOCK, np.sin(2 * np.pi * 55 * tt(0.3)) * np.exp(-tt(0.3) / 0.09), 0.7)
    put(T_LOCK, noise(0.01) * np.exp(-tt(0.01) / 0.002), 0.6)
    put(T_LOCK, np.sin(2 * np.pi * 1800 * tt(0.12)) * np.exp(-tt(0.12) / 0.03), 0.15)
    # удары штампов и появление карточек
    for ts in (T_HEAVY, wt('L5', 10), wt('L7', 5)):
        put(ts, np.sin(2 * np.pi * 90 * tt(0.15)) * np.exp(-tt(0.15) / 0.04), 0.3)
    for ts in (wt('L7', 7), wt('L7', 10), wt('L7', 13), wt('L8', 6)):
        u = tt(0.05); put(ts, np.sin(2 * np.pi * (700 + 8000 * u) * u) * np.exp(-u / 0.015), 0.10)
    # свист на склейках
    for (t0, nm) in SCENES[1:]:
        y = noise(0.28); y = lp_fast(np.concatenate([y, y[:4]]), 5)[:len(y)]
        y = y - lp_fast(np.concatenate([y, y[:40]]), 41)[:len(y)]
        put(max(0, t0 - 0.14), y * np.sin(np.linspace(0, np.pi, len(y))) ** 2, 0.08)
    # музыка с приглушением под голос
    raw = subprocess.run([FF, '-v', 'error', '-stream_loop', '-1', '-i', os.path.join(D, 'music', 'bg.m4a'),
                          '-t', str(n / SR), '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    mus = np.frombuffer(raw, np.float32)[:n].copy(); mus = np.pad(mus, (0, n - len(mus)))
    env = lp_fast(np.abs(voice), 2400); env = np.pad(env, (0, n - len(env)))
    duck = 1 - 0.45 * np.clip(env / 0.05, 0, 1)
    mus *= 0.11 * duck
    fo = int(0.8 * SR); mus[int(TOTAL * SR) - fo:int(TOTAL * SR)] *= np.linspace(1, 0, fo); mus[int(TOTAL * SR):] = 0
    mix = voice + sfx + mus
    return mix[:int(TOTAL * SR)]


def write_audio(path):
    import wave
    x = synth()
    tmp = path + '.raw.wav'
    with wave.open(tmp, 'wb') as w_:
        w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(SR)
        w_.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
    subprocess.run([FF, '-y', '-v', 'error', '-i', tmp, '-af', 'loudnorm=I=-13:TP=-1.5:LRA=11', '-ar', str(SR), path], check=True)
    os.remove(tmp)


# ======================= вывод =======================
def encode(frames, out):
    p = subprocess.Popen([FF, '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                          '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', out],
                         stdin=subprocess.PIPE)
    for i in frames:
        p.stdin.write(render(i / FPS).tobytes())
    p.stdin.close(); p.wait()


def _seg(args):
    a, b, out = args
    encode(range(a, b), out); return out


def main():
    av = sys.argv
    if '--frame' in av:
        t = float(av[av.index('--frame') + 1]); render(t).save(av[av.index('--frame') + 2]); return
    if '--sheet' in av:
        out = av[av.index('--sheet') + 1]
        ts = [float(x) for x in av[av.index('--sheet') + 2].split(',')] if len(av) > av.index('--sheet') + 2 else \
             [i * 1.0 for i in range(int(TOTAL) + 1)]
        cols = 6; tw, th = 270, 480
        sheet = Image.new('RGB', (cols * tw, ((len(ts) + cols - 1) // cols) * (th + 30)), (20, 20, 20))
        d = ImageDraw.Draw(sheet)
        for i, t in enumerate(ts):
            im = render(min(t, TOTAL - 0.01)).resize((tw, th), LZ)
            x, y = (i % cols) * tw, (i // cols) * (th + 30)
            sheet.paste(im, (x, y + 30)); d.text((x + 6, y + 6), f'{t:.2f}s {scene_at(t)[0]}', fill=(255, 255, 0))
        sheet.save(out, quality=88); return
    if '--audio' in av:
        write_audio(av[av.index('--audio') + 1]); return
    if '--times' in av:
        for l in START: print(l, round(START[l], 2), round(END[l], 2))
        print('TC', round(TC, 2), 'PULL', round(T_PULL, 2), 'LOCK', round(T_LOCK, 2), 'TOTAL', round(TOTAL, 2))
        for t0, nm in SCENES: print(f'{t0:6.2f} {nm}')
        return
    out = av[av.index('--out') + 1] if '--out' in av else os.path.join(D, 'short.mp4')
    N = int(av[av.index('--parallel') + 1]) if '--parallel' in av else 4
    os.makedirs(os.path.join(D, 'work'), exist_ok=True)
    wav = os.path.join(D, 'work', 'mix.wav'); write_audio(wav)
    import multiprocessing as mp
    bounds = [round(NFR * i / N) for i in range(N + 1)]
    segs = [(bounds[i], bounds[i + 1], os.path.join(D, 'work', f'seg{i}.mp4')) for i in range(N)]
    with mp.get_context('fork').Pool(N) as pool:
        files = pool.map(_seg, segs)
    lst = os.path.join(D, 'work', 'segs.txt')
    with open(lst, 'w') as f: f.writelines(f"file '{x}'\n" for x in files)
    subprocess.run([FF, '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-i', wav, '-c:v', 'copy',
                    '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out], check=True)
    print('готово', out, f'{TOTAL:.2f} с')


if __name__ == '__main__':
    main()
