"""Сцены-схемы. Каждая: f(c, t, T, m) — t от начала клипа, T — длина клипа,
m — список (начало, конец) реплик, которые идут под этот клип (секунды от начала клипа)."""
import math, random
import schlib as L
from schlib import *

# машина сбоку поаккуратнее (под Гранту): капот, лобовое, крыша, багажник
L.SEDAN = [(10, -40), (0, -72), (6, -112), (40, -124), (220, -142), (332, -224), (482, -228), (578, -162),
           (690, -150), (704, -108), (700, -56), (686, -40)]
L.WIN = [(414, -214), (476, -214), (552, -158), (414, -154)]
L.WIN2 = [(340, -212), (402, -214), (402, -154), (298, -152)]

def seg(t, m, i):
    """Доля прохода по i-й реплике (0..1)."""
    a, b = m[min(i, len(m) - 1)]
    return clamp((t - a) / max(b - a, 0.01))

def appear(t, at, dur=0.35): return pop(ph(t, at, at + dur))

# ---------------- вступление ----------------
def S01(c, t, T, m):
    n = int(100 * ease(ph(t, 0.05, 1.1)))
    random.seed(int(t * 12))
    for i in range(7):
        a = random.random() * 6.28; r = random.uniform(330, 470)
        c.star(W / 2 + r * math.cos(a) * 1.5, 520 + r * math.sin(a) * 0.8, random.uniform(26, 52), 9, YEL, 4, rot=a)
    k = appear(t, 0.0)
    c.text(W / 2, 470, str(n), 300 * k, ORANGE, stroke=10, sc=INK)
    c.plate(W / 2, 700, 'вспышек в секунду', 64, k=appear(t, 0.4))
    # «никто не слышит» — перечёркнутое ухо-динамик
    kk = appear(t, T * 0.45)
    if kk > 0.05:
        x, y = W / 2, 880
        c.poly([(x - 60 * kk, y - 30 * kk), (x - 20 * kk, y - 30 * kk), (x + 25 * kk, y - 70 * kk), (x + 25 * kk, y + 70 * kk), (x - 20 * kk, y + 30 * kk), (x - 60 * kk, y + 30 * kk)], WHITE, 5)
        c.line([(x + 60 * kk, y - 60 * kk), (x + 150 * kk, y + 60 * kk)], 14, RED)
        c.line([(x + 150 * kk, y - 60 * kk), (x + 60 * kk, y + 60 * kk)], 14, RED)

ICONS = ['мотор', 'коробка', 'привод', 'тормоза', 'подвеска', '5 слов']

def icon(c, kind, x, y, s=1.0, t=0.0):
    if kind == 'мотор':
        c.rect(x - 70 * s, y - 50 * s, x + 70 * s, y + 55 * s, STEEL, 5, r=10)
        for i in range(4): c.rect(x - 58 * s + i * 30 * s, y - 80 * s, x - 36 * s + i * 30 * s, y - 50 * s, DSTEEL, 4)
    elif kind == 'коробка':
        c.gear(x - 25 * s, y, 45 * s, 10, t * 2, ORANGE); c.gear(x + 48 * s, y + 10 * s, 30 * s, 8, -t * 3 + 0.2, LBLUE)
    elif kind == 'привод':
        c.line([(x - 80 * s, y), (x + 80 * s, y)], 14 * s, DSTEEL)
        c.wheel(x - 80 * s, y, 42 * s, t * 3); c.wheel(x + 80 * s, y, 42 * s, t * 3)
    elif kind == 'тормоза':
        c.circ(x, y, 62 * s, STEEL, 5)
        for i in range(6):
            a = t * 2 + i * 1.047; c.circ(x + 38 * s * math.cos(a), y + 38 * s * math.sin(a), 8 * s, DSTEEL, 0)
        c.rect(x + 30 * s, y - 40 * s, x + 80 * s, y + 40 * s, RED, 5, r=10)
    elif kind == 'подвеска':
        c.spring(x, y - 70 * s, y + 70 * s, 70 * s, 6, 10 * s)
    elif kind == '5 слов':
        c.rect(x - 75 * s, y - 50 * s, x + 75 * s, y + 35 * s, WHITE, 5, r=24)
        c.poly([(x - 30 * s, y + 33 * s), (x - 50 * s, y + 70 * s), (x, y + 33 * s)], WHITE, 5)
        c.text(x, y - 8 * s, 'Аа', 46 * s, BLUE)
    elif kind == 'шины':
        c.wheel(x, y, 66 * s, t * 2)

def cards(c, t, items, shown, hi=None, y=540):
    n = len(items); gap = 290; x0 = W / 2 - gap * (n - 1) / 2
    for i, it in enumerate(items):
        k = shown[i]
        if k <= 0.02: continue
        x = x0 + i * gap
        on = hi is not None and hi == i
        c.rect(x - 125 * k, y - 140 * k, x + 125 * k, y + 140 * k, YEL if on else CREAMBOX, 5, r=28)
        icon(c, it, x, y - 30 * k, 0.95 * k, t)
        c.text(x, y + 95 * k, it, 40 * k)
        if i < n - 1 and k > 0.9: c.arrow(x + 132, y, x + gap - 132, y, 6, ORANGE, 22)

def S02(c, t, T, m):
    c.title('ПЛАН', appear(t, 0))
    shown = [appear(t, 0.15 + i * 0.45) for i in range(6)]
    hi = 5 if t > T * 0.25 else None
    if t > T * 0.75: hi = int((t - T * 0.75) / (T * 0.25) * 6) % 6
    cards(c, t, ICONS, shown, hi)

# ---------------- цепочка ----------------
def chain_car(c, t, stage, y0=820, s=1.75, glow=None):
    """Гранта сбоку в разрезе: мотор, коробка, привод на передние колёса. stage 0..4 — сколько звеньев подсвечено."""
    x0 = W / 2 - 702 * s / 2
    body = [(x0 + px * s, y0 + py * s) for px, py in L.SEDAN]
    c.poly(body, mix(BG, BLUE, 0.25), 5)
    c.poly([(x0 + px * s, y0 + py * s) for px, py in L.WIN], mix(BG, LBLUE, 0.5), 4)
    c.poly([(x0 + px * s, y0 + py * s) for px, py in L.WIN2], mix(BG, LBLUE, 0.5), 4)
    fx, fy = x0 + 130 * s, y0 - 40 * s; rx = x0 + 565 * s
    spin = t * 6 if stage >= 3 else 0
    c.wheel(fx, fy, 58 * s, spin); c.wheel(rx, fy, 58 * s, spin)
    ex, ey = x0 + 120 * s, y0 - 128 * s  # мотор над передней осью
    hot = lambda i: stage > i
    c.rect(ex - 70 * s, ey - 44 * s, ex + 70 * s, ey + 40 * s, ORANGE if hot(0) else STEEL, 5, r=10)
    c.rect(ex + 74 * s, ey - 20 * s, ex + 130 * s, ey + 50 * s, YEL if hot(1) else STEEL, 5, r=8)
    c.line([(ex + 100 * s, ey + 50 * s), (fx, fy)], 14, ORANGE if hot(2) else DSTEEL)
    if hot(0):
        random.seed(int(t * 10))
        c.star(ex + random.uniform(-40, 40) * s, ey + random.uniform(-20, 10) * s, 22, 8, YEL, 3)
    return dict(engine=(ex, ey - 44 * s), box=(ex + 102 * s, ey - 20 * s), drive=((ex + 100 * s + fx) / 2, (ey + 50 * s + fy) / 2), wheel=(fx, fy + 58 * s))

def S03(c, t, T, m):
    p = seg(t, m, 0)
    stage = 1 + int(p > 0.32) + int(p > 0.62) + int(p > 0.8) if p > 0.12 else 0
    if len(m) > 1 and t >= m[1][0]: stage = 4
    pts = chain_car(c, t, stage)
    labels = [('МОТОР — делает силу', pts['engine'], 0.12), ('КОРОБКА — передаёт и подстраивает', pts['box'], 0.38),
              ('ПРИВОД — до колёс', pts['drive'], 0.66)]
    for i, (s, (x, y), at) in enumerate(labels):
        k = appear(p, at, 0.06)
        if k > 0.02:
            ly = 170 + i * 105
            c.plate(W / 2, ly, s, 50, k=k)
            c.line([(W / 2 + (-260 + i * 180), ly + 36), (x, y)], 5, INK)
    if len(m) > 1 and t >= m[1][0]:
        c.plate(W / 2, 985, 'открываем капот!', 60, ORANGE, k=appear(t, m[1][0]))

# ---------------- мотор ----------------
def S04(c, t, T, m):
    c.title('4 ЦИЛИНДРА', appear(t, 0))
    offs = [0, math.pi, math.pi, 0]
    for i in range(4):
        cylinder(c, 420 + i * 360, 330, 200, 300, crank=t * 5 + offs[i], gas=ORANGE, gas_a=0.25, small=True, t=t, ports=False)

STROKES = [('ВДОХ', LBLUE), ('СЖАТИЕ', YEL), ('ВЗРЫВ', ORANGE), ('ВЫДОХ', SMOKE)]

def S05(c, t, T, m):
    c.title('4 ТАКТА', appear(t, 0))
    ats = [0.56, 0.67, 0.78, 0.88]
    if t < T * ats[0]:
        cr = t * 3.2; st = int((cr % (4 * math.pi)) / math.pi)
        name, col = STROKES[st]
        cylinder(c, 760, 330, 300, 420, crank=cr, gas=col, gas_a=0.6, iv=1 if st == 0 else 0, ev=1 if st == 3 else 0,
                 spark=1 if st == 2 and (cr % math.pi) < 0.5 else 0, t=t)
        c.plate(1420, 540, name, 90, col if st != 3 else INK)
        return
    for i, ((name, col), at) in enumerate(zip(STROKES, ats)):
        k = appear(t, T * at)
        if k <= 0.02: continue
        x = 300 + i * 440
        c.rect(x - 190 * k, 250, x + 190 * k, 900, CREAMBOX, 5, r=30)
        crank = [math.pi * ease(ph(t, T * at, T * at + 1.2)), math.pi + math.pi * ease(ph(t, T * at, T * at + 1.2)),
                 math.pi * ease(ph(t, T * at, T * at + 1.2)), math.pi + math.pi * ease(ph(t, T * at, T * at + 1.2))][i]
        cylinder(c, x, 380, 150 * k, 250 * k, crank=crank, gas=col, gas_a=0.7, iv=1 if i == 0 else 0, ev=1 if i == 3 else 0,
                 spark=1 if (i == 2 and ph(t, T * at, T * at + 0.4) < 1) else 0, small=True, t=t, ports=False)
        c.text(x, 840, name, 46 * k, INK)

def stroke_scene(c, t, T, i):
    name, col = STROKES[i]
    p = ease(ph(t, 0.3, T * 0.8))
    crank = (math.pi * p) if i in (0, 2) else (math.pi + math.pi * p)
    gas_a = {0: 0.25 + 0.4 * p, 1: 0.5 + 0.4 * p, 2: 0.9 - 0.5 * p, 3: 0.5 - 0.4 * p}[i]
    gcol = {0: LBLUE, 1: mix(LBLUE, YEL, p), 2: mix(ORANGE, SMOKE, p), 3: SMOKE}[i]
    spark = 1 - ph(t, 0.3, 0.9) if i == 2 else 0
    cylinder(c, 640, 330, 300, 420, crank=crank, gas=gcol, gas_a=gas_a, iv=1 if i == 0 else 0, ev=1 if i == 3 else 0,
             spark=spark, inj=1 if i == 0 and ph(t, 0.4, T * 0.6) < 1 else 0, flow_in=1 if i == 0 else 0,
             flow_out=1 if i == 3 else 0, t=t)
    c.plate(1390, 300, name, 110, col if i != 3 else INK, k=appear(t, 0))
    sub = ['поршень вниз — втягивает воздух и бензин', 'поршень вверх — сжимает смесь ×10',
           'искра — вспышка толкает поршень', 'поршень вверх — выхлоп в трубу'][i]
    words = sub.split(' — ')
    c.plate(1390, 470, words[0], 46, k=appear(t, 0.5))
    c.plate(1390, 560, words[1], 46, k=appear(t, 0.9))
    if i == 2:
        k = appear(t, T * 0.55)
        if k > 0.05: c.arrow(990, 600, 990, 760, 14, ORANGE, 40); c.plate(1390, 680, 'ВОТ ОНА, СИЛА', 60, RED, k=k)

def S05a(c, t, T, m): stroke_scene(c, t, T, 0)
def S05b(c, t, T, m): stroke_scene(c, t, T, 1)
def S05c(c, t, T, m): stroke_scene(c, t, T, 2)
def S05d(c, t, T, m): stroke_scene(c, t, T, 3)

def S06(c, t, T, m):
    split = T * 0.42
    if t < split:
        k = appear(t, 0)
        c.title('ГОРЯТ ПАРЫ, А НЕ ЖИДКОСТЬ', k, size=64)
        # слева: капля — не горит
        c.poly([(560, 380), (640, 560), (620, 620), (560, 650), (500, 620), (480, 560)], YEL, 5)
        c.plate(560, 760, 'жидкий бензин', 48, k=appear(t, 0.4)); c.check(560, 870, 40, False) if t > 1.0 else None
        # справа: облако пара + воздух — вспышка
        random.seed(3)
        for i in range(14):
            a = random.random() * 6.28; r = random.uniform(20, 150)
            c.circ(1360 + r * math.cos(a) + 10 * math.sin(t * 3 + i), 520 + r * math.sin(a) * 0.7, random.uniform(16, 30),
                   YEL if i % 2 else LBLUE, 3)
        if t > split * 0.55:
            c.star(1360, 520, 120 + 30 * math.sin(t * 20), 12, ORANGE, 5, rot=t * 3)
        c.plate(1360, 760, 'пары + воздух', 48, k=appear(t, 0.8)); c.check(1360, 870, 40, True) if t > split * 0.6 else None
    else:
        tt = t - split; TT = T - split; dirty = ease(ph(tt, TT * 0.35, TT * 0.6))
        c.title('ВОЗДУШНЫЙ ФИЛЬТР', appear(tt, 0), size=64)
        fx = 820
        c.rect(fx - 60, 300, fx + 60, 800, mix(WHITE, BROWN, dirty * 0.8), 6, r=12)
        for i in range(12): c.line([(fx - 50, 330 + i * 40), (fx + 50, 330 + i * 40)], 4, mix(STEEL, INK, dirty * 0.6))
        icon(c, 'мотор', 1450, 560, 2.0, tt)
        nflow = int(lerp(7, 2, dirty))
        for i in range(nflow):
            y = 360 + i * (400 / max(nflow - 1, 1)); k = (tt * 1.4 + i * 0.17) % 1
            c.arrow(380 + k * 300, y, 470 + k * 300, y, 10, LBLUE, 28)
            c.arrow(fx + 80 + k * 320, y, fx + 170 + k * 320, y, 10 * (1 - dirty * 0.5), LBLUE, 28)
        c.plate(820, 900, 'забился — мотор тянет хуже', 52, RED, k=appear(tt, TT * 0.55))

def S07(c, t, T, m):
    c.title('КОЛЕНВАЛ', appear(t, 0))
    offs = [0, math.pi, math.pi, 0]
    cy = 760; ang = t * 4
    c.line([(300, cy), (1620, cy)], 30, INK); c.line([(300, cy), (1620, cy)], 20, DSTEEL)
    for i in range(4):
        x = 480 + i * 320; a = ang + offs[i]
        px, py = x + 70 * math.sin(a), cy - 70 * math.cos(a)
        c.circ(x, cy, 90, (205, 205, 210), 5)
        top = py - 260
        c.line([(x - 92, 300), (x - 92, 640)], 8, DSTEEL); c.line([(x + 92, 300), (x + 92, 640)], 8, DSTEEL)
        c.rect(x - 80, top - 60, x + 80, top + 30, (196, 202, 210), 5, r=6)
        c.line([(x, top + 10), (px, py)], 24, INK); c.line([(x, top + 10), (px, py)], 14, DSTEEL)
        c.circ(px, py, 14, DSTEEL, 4)
    c.arc(1700, cy, 70, -60 + (t * 230) % 360, 200 + (t * 230) % 360, 10, ORANGE)

def tacho(c, cx, cy, r, val, vmax, label, unit, col=ORANGE, ticks=None):
    c.circ(cx, cy, r, WHITE, 6)
    ticks = ticks or [i for i in range(0, vmax + 1, vmax // 6)]
    for v in ticks:
        a = math.radians(-225 + 270 * v / vmax)
        c.line([(cx + r * 0.82 * math.cos(a), cy + r * 0.82 * math.sin(a)), (cx + r * 0.95 * math.cos(a), cy + r * 0.95 * math.sin(a))], 6, INK)
        c.text(cx + r * 0.66 * math.cos(a), cy + r * 0.66 * math.sin(a), str(v // 1000 if vmax >= 3000 else v), r * 0.14, INK)
    a = math.radians(-225 + 270 * clamp(val / vmax))
    c.line([(cx, cy), (cx + r * 0.78 * math.cos(a), cy + r * 0.78 * math.sin(a))], 12, col)
    c.circ(cx, cy, r * 0.08, INK, 0)
    c.text(cx, cy + r * 0.45, unit, r * 0.11, INK)
    c.plate(cx, cy + r + 60, label, 50)

def S08(c, t, T, m):
    if t < m[0][1]:
        p = seg(t, m, 0)
        rpm = 3000 * ease(ph(p, 0.15, 0.45))
        tacho(c, 560, 520, 300, rpm, 6000, f'{int(round(rpm, -2))} об/мин', '×1000 об/мин')
        k = appear(p, 0.62, 0.08)
        if k > 0.02:
            c.plate(1350, 330, '1 вспышка = 2 оборота', 58, k=k)
            ang = (t - m[0][0]) * 7
            c.circ(1350, 620, 150, (205, 205, 210), 6)
            c.circ(1350 + 110 * math.cos(ang), 620 + 110 * math.sin(ang), 24, ORANGE, 4)
            if (ang / (4 * math.pi)) % 1 < 0.12: c.star(1350, 620, 80, 10, YEL, 4)
    else:
        p = seg(t, m, 1)
        c.plate(W / 2, 220, '25 вспышек в секунду', 70, k=appear(p, 0.02, 0.1))
        k = appear(p, 0.3, 0.1)
        for i in range(4):
            if k > 0.02:
                x = 520 + i * 290
                c.rect(x - 70 * k, 420 - 90 * k, x + 70 * k, 420 + 90 * k, STEEL, 5, r=10)
                if int(t * 25 + i * 6) % 4 == 0: c.star(x, 400, 44, 9, YEL, 4)
        c.plate(W / 2, 570, '× 4 цилиндра', 56, k=appear(p, 0.38, 0.1))
        kk = appear(p, 0.5, 0.1)
        if kk > 0.02: c.text(W / 2, 760, '= 100 в секунду', 120 * kk, ORANGE, stroke=8, sc=INK)

def S09(c, t, T, m):
    c.title('ОХЛАЖДЕНИЕ', appear(t, 0))
    # мотор справа, радиатор слева, контур антифриза
    c.rect(1050, 380, 1450, 760, STEEL, 6, r=16)
    for i in range(4): c.rect(1090 + i * 90, 420, 1160 + i * 90, 600, mix(STEEL, ORANGE, 0.5 + 0.3 * math.sin(t * 6 + i)), 4, r=6)
    for i in range(3):
        y = 320 - i * 18 + (t * 40 % 18)
        c.line([(1120 + i * 110, y), (1140 + i * 110, y - 30), (1120 + i * 110, y - 60)], 6, RED)
    c.rect(380, 360, 560, 800, mix(STEEL, WHITE, 0.3), 6, r=10)
    for i in range(10): c.line([(395, 390 + i * 40), (545, 390 + i * 40)], 4, DSTEEL)
    # вентилятор
    c.circ(470, 580, 80, None, 5)
    for i in range(4):
        a = t * 10 + i * 1.57
        c.poly([(470, 580), (470 + 75 * math.cos(a), 580 + 75 * math.sin(a)), (470 + 75 * math.cos(a + 0.6), 580 + 75 * math.sin(a + 0.6))], DSTEEL, 3)
    # трубы и поток
    loop = [(560, 430), (1050, 430), (1050, 430)]
    c.line([(560, 430), (1050, 430)], 22, INK); c.line([(560, 430), (1050, 430)], 14, PINK)
    c.line([(560, 730), (1050, 730)], 22, INK); c.line([(560, 730), (1050, 730)], 14, PINK)
    for i in range(6):
        k = (t * 0.5 + i / 6) % 1
        c.circ(1050 - k * 490, 430, 11, mix(RED, PINK, k), 3)
        c.circ(560 + k * 490, 730, 11, mix(PINK, RED, k), 3)
    c.plate(800, 360, 'антифриз', 50, k=appear(t, T * 0.35))
    c.plate(470, 880, 'радиатор', 50, k=appear(t, T * 0.6))
    c.plate(1250, 880, 'мотор греется', 50, RED, k=appear(t, 0.3))

def S10(c, t, T, m):
    first = t < m[0][1]
    p = seg(t, m, 0) if first else seg(t, m, 1)
    c.title('ЭЛЕКТРИЧЕСТВО', appear(t, 0))
    # мотор со шкивом, ремень к генератору, аккумулятор
    c.rect(300, 420, 700, 780, STEEL, 6, r=16)
    ang = t * 5 if (not first or p > 0.35) else 0
    c.circ(500, 860, 70, DSTEEL, 5); c.circ(820, 760, 50, DSTEEL, 5)
    c.line([(500, 790), (820, 710)], 8, INK); c.line([(500, 930), (820, 810)], 8, INK)
    c.line([(500 + 50 * math.cos(ang), 860 + 50 * math.sin(ang)), (500, 860)], 8, WHITE)
    broken = not first and p > 0.05
    c.rect(760, 660, 900, 760, (90, 160, 120) if not broken else SMOKE, 5, r=12)
    c.text(830, 615, 'генератор', 36)
    if broken: c.check(830, 710, 36, False)
    # аккумулятор
    charge = 1.0 if first else 1 - ease(ph(p, 0.15, 0.85))
    c.rect(1000, 760, 1220, 900, INK, 5, r=10)
    c.rect(1012, 772, 1012 + 196 * charge, 888, GREEN if charge > 0.3 else RED, 0)
    c.text(1110, 950, 'аккумулятор', 40)
    # потребители
    cons = [('фары', 1560, 460), ('печка', 1560, 640), ('магнитола', 1560, 820)]
    live = (first and p > 0.35) or (not first and charge > 0.02)
    src = (900, 710) if (first or not broken) else (1220, 830)
    for name, x, y in cons:
        c.line([src, (x - 120, y)], 7, YEL if live else SMOKE)
        c.rect(x - 120, y - 60, x + 120, y + 60, YEL if live else CREAMBOX, 5, r=20)
        c.text(x, y, name, 40)
    if first:
        k = appear(p, 0.08, 0.06)
        if k > 0.02 and p < 0.4:
            c.line([(1000, 830), (650, 700)], 10, YEL); c.star(640, 700, 50, 9, YEL, 4)
            c.plate(960, 250, 'аккумулятор — чтобы завести', 52, k=k)
        if p >= 0.4: c.plate(960, 250, 'дальше всё питает генератор', 52, k=appear(p, 0.4, 0.06))
    else:
        c.plate(960, 250, 'генератор сломался — едем на аккумуляторе', 48, RED, k=appear(p, 0.02, 0.1))

# ---------------- коробка ----------------
def S11(c, t, T, m):
    p = seg(t, m, 0)
    erpm = lerp(800, 5000, ease(ph(p, 0.55, 0.9)))
    wrpm = lerp(0, 900, ease(ph(p, 0.35, 0.8)))
    tacho(c, 560, 500, 280, erpm, 6000, 'мотор: 800–5000', '×1000 об/мин', ORANGE)
    tacho(c, 1360, 500, 280, wrpm, 1000, 'колесо: 0–900', 'об/мин', BLUE, ticks=[0, 200, 400, 600, 800, 1000])
    k = appear(p, 0.85, 0.08)
    if k > 0.02: c.text(W / 2, 500, '≠', 200 * k, RED, stroke=8, sc=INK)

def gear_pair(c, t, r1, r2, n1, n2, w1, label, col1=ORANGE, col2=LBLUE, cy=560):
    d = r1 + r2 + 18; x1 = W / 2 - d / 2; x2 = W / 2 + d / 2
    a1 = t * w1; a2 = -a1 * r1 / r2 + math.pi / n2
    c.gear(x1, cy, r1, n1, a1, col1); c.gear(x2, cy, r2, n2, a2, col2)
    c.plate(x1, cy + r1 + 90, 'от мотора', 44); c.plate(x2, cy + r2 + 90, 'к колёсам', 44)
    c.title(label)

def S12(c, t, T, m):
    if t < m[0][1]:
        gear_pair(c, t, 110, 230, 10, 21, 4.0, '1-я: крутишь много — едешь медленно')
    else:
        gear_pair(c, t, 230, 110, 21, 10, 1.5, '5-я: мотор спокойно — машина летит')

def rot_arrow(c, cx, cy, r, cw, col):
    a0, a1 = (-150, -30) if cw else (-30, -150)
    c.arc(cx, cy, r, min(a0, a1), max(a0, a1), 12, col)
    ae = math.radians(a1); x, y = cx + r * math.cos(ae), cy + r * math.sin(ae)
    tang = ae + (math.pi / 2 if cw else -math.pi / 2)
    c.arrow(x - 30 * math.cos(tang), y - 30 * math.sin(tang), x + 10 * math.cos(tang), y + 10 * math.sin(tang), 10, col, 38)

def S13(c, t, T, m):
    p = seg(t, m, 0)
    c.title('ЗАДНЯЯ ПЕРЕДАЧА', appear(t, 0))
    a = t * 2.2
    # вперёд
    c.text(300, 330, 'вперёд', 50)
    c.gear(600, 330, 110, 12, a, ORANGE); c.gear(830, 330, 100, 11, -a * 1.1 + 0.3, LBLUE)
    rot_arrow(c, 830, 330, 150, True, GREEN)
    if p > 0.2:
        k = appear(p, 0.2, 0.08)
        c.text(300, 720, 'назад', 50 * k)
        c.gear(600, 720, 110, 12, a, ORANGE); c.gear(750, 820, 48, 6, -a * 2.3, YEL)
        c.gear(900, 720, 100, 11, a * 1.1, LBLUE)
        rot_arrow(c, 900, 720, 140, False, RED)
        c.plate(750, 960, 'маленькая шестерёнка разворачивает вращение', 44, k=appear(p, 0.3, 0.08))
    k = appear(p, 0.68, 0.06)
    if k > 0.02:
        c.rect(1240, 380 + 60 * (1 - k), 1760, 760, CREAMBOX, 6, r=26)
        c.text(1500, 470, 'отдельный ролик:', 42 * k)
        c.text(1500, 560, 'Задняя', 70 * k, RED)
        c.text(1500, 640, 'на ходу?', 70 * k, RED)

def clutch(c, t, gap, spin2, cy=560):
    a1 = t * 6; a2 = spin2
    x = W / 2
    c.rect(x - 360, cy - 230, x - 300, cy + 230, ORANGE, 6, r=10)  # маховик
    for i in range(3):
        aa = a1 + i * 2.09; c.circ(x - 330, cy + 170 * math.sin(aa), 12, INK, 0)
    xd = x - 290 + gap
    c.rect(xd, cy - 200, xd + 40, cy + 200, BROWN, 6, r=8)  # диск сцепления
    c.rect(xd + 50, cy - 190, xd + 90, cy + 190, STEEL, 6, r=8)  # нажимной диск
    for i in range(3):
        aa = a2 + i * 2.09; c.circ(xd + 20, cy + 150 * math.sin(aa), 10, INK, 0)
    c.spring(xd + 160, cy - 150, cy + 150, 60, 5, 10) if False else None
    for i in range(3):
        sx = xd + 110 + i * 0; c.line([(xd + 90, cy - 120 + i * 120), (xd + 200, cy - 120 + i * 120)], 10, DSTEEL)
    c.line([(x - 600, cy), (x - 360, cy)], 24, INK); c.line([(xd + 90, cy), (x + 560, cy)], 24, INK)
    c.text(x - 480, cy - 270, 'мотор', 44); c.text(x + 420, cy - 270, 'коробка', 44)

def S14(c, t, T, m):
    if t < m[0][1]:
        p = seg(t, m, 0)
        if p < 0.33:
            c.title('ПЕРЕКЛЮЧИТЬ НА ХОДУ?', appear(t, 0), size=64)
            c.gear(820, 560, 150, 14, t * 6, ORANGE); c.gear(1100, 560, 120, 11, -t * 2, LBLUE)
            random.seed(int(t * 15))
            for i in range(5): c.star(960 + random.uniform(-30, 30), 560 + random.uniform(-80, 80), 26, 7, YEL, 3)
            c.check(960, 860, 50, False)
        else:
            c.title('СЦЕПЛЕНИЕ', appear(p, 0.33, 0.06))
            clutch(c, t, 0, t * 6)
            c.plate(W / 2, 880, 'два диска прижимает пружина', 50, k=appear(p, 0.6, 0.08))
    else:
        p = seg(t, m, 1)
        press = ease(ph(p, 0.05, 0.18)) * (1 - ease(ph(p, 0.62, 0.78)))
        gap = 70 * press
        spin2 = t * 6 * (1 - press) if press < 0.98 else 0
        c.title('СЦЕПЛЕНИЕ', 1)
        clutch(c, t, gap, (m[1][0] * 6) + (t - m[1][0]) * 6 * (1 - press))
        # педаль
        px, py = 1580, 800
        c.line([(px, py - 220), (px - 60 + 40 * press, py + 20 * press)], 14, DSTEEL)
        c.rect(px - 110 + 40 * press, py - 10 + 20 * press, px - 10 + 40 * press, py + 30 + 20 * press, INK, 0, r=8)
        msg = 'жмёшь педаль — диски расходятся' if p < 0.45 else ('переключил' if p < 0.62 else 'отпустил — сцепились')
        c.plate(W / 2, 880, msg, 52)

def fan(c, cx, cy, r, ang, col):
    c.circ(cx, cy, r + 14, None, 6)
    for i in range(4):
        a = ang + i * 1.5708
        c.poly([(cx, cy), (cx + r * math.cos(a), cy + r * math.sin(a)), (cx + r * math.cos(a + 0.7), cy + r * math.sin(a + 0.7))], col, 4)
    c.circ(cx, cy, r * 0.15, INK, 0)

def S15(c, t, T, m):
    p = seg(t, m, 0)
    c.title('ГИДРОТРАНСФОРМАТОР', appear(t, 0), size=64)
    on = ph(p, 0.4, 0.5)
    w1 = 9 * on
    k2 = ease(ph(p, 0.62, 0.95))
    a1 = 9 * max(t - m[0][0] - (m[0][1] - m[0][0]) * 0.4, 0) if on else 0
    a2 = 6 * k2 * max(t - m[0][0] - (m[0][1] - m[0][0]) * 0.62, 0)
    fan(c, 560, 540, 190, a1, ORANGE); fan(c, 1360, 540, 190, a2, LBLUE)
    if on > 0:
        for i in range(5):
            k = (t * 1.5 + i / 5) % 1
            y = 400 + i * 70
            c.line([(780 + k * 360, y), (850 + k * 360, y)], 8, mix(LBLUE, BG, k * 0.5))
    c.plate(560, 820, 'от мотора', 48, k=appear(p, 0.45, 0.06)); c.plate(1360, 820, 'к колёсам', 48, k=appear(p, 0.7, 0.06))

def S16(c, t, T, m):
    p = seg(t, m, 0)
    c.title('ВАРИАТОР', appear(t, 0))
    k = 0.5 + 0.5 * math.sin((t - m[0][0]) * 1.3 - 1.5)
    r1 = lerp(80, 210, k); r2 = lerp(210, 80, k)
    x1, x2, cy = 650, 1270, 560
    for x, r, col in ((x1, r1, ORANGE), (x2, r2, LBLUE)):
        c.circ(x, cy, 230, mix(BG, col, 0.25), 5)
        c.circ(x, cy, r, col, 6)
        c.circ(x, cy, 26, INK, 0)
    # ремень — касательные
    for sgn in (-1, 1):
        c.line([(x1, cy + sgn * r1), (x2, cy + sgn * r2)], 16, INK)
    c.plate(W / 2, 880, 'конусы сдвигаются — передача меняется плавно', 46, k=appear(p, 0.3, 0.08))

def S17(c, t, T, m):
    p = seg(t, m, 0)
    c.title('РОБОТ = МЕХАНИКА + КОМПЬЮТЕР', appear(t, 0), size=60)
    # Н-схема
    cx, cy = 760, 560
    for dx in (-140, 0, 140):
        c.line([(cx + dx, cy - 160), (cx + dx, cy + 160)], 10, DSTEEL)
    c.line([(cx - 140, cy), (cx + 140, cy)], 10, DSTEEL)
    pos = [(-140, -160), (-140, 160), (0, -160), (0, 160), (140, -160)]
    i = int((t - m[0][0]) * 1.4) % 5; j = (i + 1) % 5; f = ease(((t - m[0][0]) * 1.4) % 1)
    kx = lerp(pos[i][0], pos[j][0], f); ky = lerp(pos[i][1], pos[j][1], f)
    c.circ(cx + kx, cy + ky, 44, INK, 0)
    # компьютер
    c.rect(1180, 420, 1480, 640, (60, 70, 80), 6, r=16)
    for r_ in range(3): c.line([(1210, 470 + r_ * 50), (1450, 470 + r_ * 50)], 6, GREEN)
    c.line([(1180, 530), (cx + kx + 40, cy + ky)], 6, YEL)
    c.plate(1330, 720, 'дёргает за тебя', 46, k=appear(p, 0.4, 0.08))

# ---------------- привод ----------------
def S18(c, t, T, m):
    first = t < m[0][1]; p = seg(t, m, 0 if first else 1)
    if first: mode = 'f'
    else: mode = 'r' if p < 0.45 else 'a'
    wf = {k: ORANGE for k in ('fl', 'fr', 'rl', 'rr') if (mode == 'a') or (mode == 'f' and k[0] == 'f') or (mode == 'r' and k[0] == 'r')}
    car_top(c, W / 2, 560, 1.3, 0, wheel_fill=wf)
    lab = {'f': 'ПЕРЕДНИЙ ПРИВОД — тянет', 'r': 'ЗАДНИЙ ПРИВОД — толкает', 'a': 'ПОЛНЫЙ — грязь и снег'}[mode]
    c.title(lab, size=64)
    k = (t * 1.2) % 1
    if mode == 'f': c.arrow(1380 + k * 60, 560, 1560 + k * 60, 560, 14, ORANGE, 44)
    if mode == 'r': c.arrow(340 + k * 60, 560, 520 + k * 60, 560, 14, ORANGE, 44)
    if mode == 'a':
        c.arrow(1380 + k * 60, 560, 1560 + k * 60, 560, 14, ORANGE, 44); c.arrow(340 + k * 60, 560, 520 + k * 60, 560, 14, ORANGE, 44)

def S19(c, t, T, m):
    p = seg(t, m, 0)
    c.title('ПОВОРОТ', appear(t, 0))
    cx, cy = 960, 1180
    Ro, Ri = 760, 520
    prog = ease(ph(p, 0.3, 0.9))
    a0, a1 = math.radians(200), math.radians(200 + 140 * prog)
    c.arc(cx, cy, Ro, 200, 340, 6, mix(BG, ORANGE, 0.4)); c.arc(cx, cy, Ri, 200, 340, 6, mix(BG, BLUE, 0.4))
    if prog > 0.01:
        c.arc(cx, cy, Ro, 200, 200 + 140 * prog, 22, ORANGE); c.arc(cx, cy, Ri, 200, 200 + 140 * prog, 22, BLUE)
    for R, col in ((Ro, ORANGE), (Ri, BLUE)):
        x, y = cx + R * math.cos(a1), cy + R * math.sin(a1)
        c.wheel(x, y, 44, t * (6 if R == Ro else 4))
    c.plate(1500, 300, 'внешнее — путь длиннее', 46, ORANGE, k=appear(p, 0.35, 0.08))
    c.plate(1500, 400, 'внутреннее — короче', 46, BLUE, k=appear(p, 0.45, 0.08))
    c.plate(W / 2, 980, 'внешнее колесо крутится быстрее', 54, k=appear(p, 0.8, 0.08))

def diff(c, t, wl, wr, y=600, ice=False):
    xl, xr = 420, 1500
    c.line([(xl, y), (xr, y)], 30, INK); c.line([(xl, y), (xr, y)], 18, DSTEEL)
    if ice:
        c.poly([(260, y + 120), (600, y + 120), (640, y + 190), (220, y + 190)], LBLUE, 4)
        c.text(430, y + 240, 'лёд', 44, BLUE)
    c.wheel(xl, y, 130, wl); c.wheel(xr, y, 130, wr)
    # коробка дифференциала
    c.rect(860, y - 150, 1060, y + 150, mix(STEEL, WHITE, 0.2), 6, r=20)
    sat = (wl - wr) * 0.5
    c.gear(910, y, 55, 9, wl, ORANGE); c.gear(1010, y, 55, 9, wr, LBLUE)
    c.gear(960, y - 90, 34, 7, sat, YEL); c.gear(960, y + 90, 34, 7, -sat, YEL)

def S20(c, t, T, m):
    if t < m[0][1]:
        p = seg(t, m, 0)
        if p < 0.32:
            c.title('КОЛЁСА НАМЕРТВО?', appear(t, 0), size=64)
            car_top(c, W / 2, 560, 1.0, -0.25 * ease(ph(p, 0, 0.3)), steer=-0.4)
            random.seed(int(t * 8))
            for i in range(6): c.line([(700 + i * 30, 760 + random.uniform(-10, 10)), (720 + i * 30, 740 + random.uniform(-10, 10))], 6, INK)
            c.plate(W / 2, 920, 'одно колесо проскальзывает', 50, RED, k=appear(p, 0.12, 0.06))
        else:
            c.title('ДИФФЕРЕНЦИАЛ', appear(p, 0.32, 0.06))
            tt = t - m[0][0]
            diff(c, t, tt * 3.0, tt * 4.4)
            c.plate(W / 2, 900, 'каждое колесо — со своей скоростью', 50, k=appear(p, 0.6, 0.08))
    else:
        tt = t - m[1][0]
        c.title('ОДНО КОЛЕСО НА ЛЬДУ', appear(tt, 0), size=64)
        diff(c, t, tt * 9, 0.4, ice=True)
        c.arrow(700, 330, 470, 430, 12, RED, 40)
        c.plate(980, 300, 'всё вращение — сюда', 50, RED, k=appear(tt, 0.4))

def S20b(c, t, T, m):
    c.title('ОДНО КОЛЕСО НА ЛЬДУ', appear(t, 0), size=64)
    diff(c, t, t * 9, 0.4, ice=True)
    c.arrow(700, 330, 470, 430, 12, RED, 40)
    c.plate(980, 300, 'всё вращение — сюда', 50, RED, k=appear(t, 0.4))

# ---------------- тормоза ----------------
def S21(c, t, T, m):
    p = (t - m[0][0]) / max(T, 0.1)
    c.title('ТОРМОЗНАЯ ЖИДКОСТЬ', appear(t, 0), size=64)
    car_top(c, 1120, 580, 1.25, 0, color=mix(BG, BLUE, 0.3))
    press = ease(ph(t, 0.3, 1.2))
    # педаль и главный цилиндр
    c.line([(260, 400), (300 + 40 * press, 640)], 14, DSTEEL); c.rect(250 + 40 * press, 630, 360 + 40 * press, 670, INK, 0, r=8)
    c.rect(400, 520, 560, 600, STEEL, 5, r=10); c.rect(410 + 60 * press, 530, 440 + 60 * press, 590, DSTEEL, 4)
    pos = {'fl': (1120 + 620 * 1.25 * 0.3, 580 - 140 * 1.25), 'fr': (1120 + 620 * 1.25 * 0.3, 580 + 140 * 1.25),
           'rl': (1120 - 620 * 1.25 * 0.3, 580 - 140 * 1.25), 'rr': (1120 - 620 * 1.25 * 0.3, 580 + 140 * 1.25)}
    wave = ease(ph(t, 1.0, 3.0))
    for k, (x, y) in pos.items():
        path = [(560, 560), (700, 560), (700, y), (x, y)]
        c.line(path, 12, INK); c.line(path, 6, mix(STEEL, RED, wave))
        c.rect(x - 40, y - 26, x + 40, y + 26, RED if wave > 0.95 else STEEL, 5, r=8)
    if len(m) > 1 and t > m[1][0]:
        c.plate(W / 2, 960, 'жидкость не сжимается — давление сразу у всех колёс', 44, k=appear(t, m[1][0] + 0.5))

def S22(c, t, T, m, hot=False):
    tt = t
    c.title('ДИСКОВЫЙ ТОРМОЗ' if not hot else 'ДВИЖЕНИЕ — В ТЕПЛО', appear(t, 0), size=64)
    clamp_k = ease(ph(t, 0.8, 1.5)) if not hot else 1
    heat = ease(ph(t, 0.5, T * 0.8)) if hot else 0
    speed = 6 * (1 - 0.8 * ease(ph(t, 1.2, T))) if not hot else 1.5
    ang = speed * t
    col = mix(STEEL, (240, 110, 40), heat)
    c.circ(800, 560, 300, col, 6)
    for i in range(8):
        a = ang + i * 0.785; c.circ(800 + 210 * math.cos(a), 560 + 210 * math.sin(a), 18, mix(DSTEEL, RED, heat), 0)
    c.circ(800, 560, 90, DSTEEL, 6)
    # суппорт с колодками
    off = 40 * (1 - clamp_k)
    c.rect(1040, 380, 1180, 740, RED, 6, r=20)
    c.rect(1010 - off, 420, 1050 - off, 700, BROWN, 4)
    if hot:
        for i in range(4):
            y = 260 - (t * 60 + i * 30) % 120
            c.line([(650 + i * 100, y + 40), (670 + i * 100, y), (650 + i * 100, y - 40)], 7, RED)
        temp = int(lerp(20, 400, heat))
        c.rect(1450, 300, 1510, 800, WHITE, 5, r=28); c.rect(1462, 800 - 480 * heat, 1498, 788, RED, 0, r=16)
        c.circ(1480, 830, 50, RED, 5)
        c.plate(1480, 940, f'≈ {temp} °C', 56, RED)
    else:
        c.plate(800, 960, 'колодки сжимают диск', 52, k=appear(t, 1.0))

def S22h(c, t, T, m): S22(c, t, T, m, hot=True)

def S23(c, t, T, m):
    c.title('БАРАБАННЫЙ ТОРМОЗ', appear(t, 0), size=64)
    push = ease(ph(t, 0.8, 1.6))
    ang = 6 * (1 - 0.8 * ease(ph(t, 1.2, T))) * t
    c.circ(W / 2, 560, 320, DSTEEL, 6); c.circ(W / 2, 560, 280, BG, 5)
    for i in range(6):
        a = ang + i * 1.047; c.circ(W / 2 + 300 * math.cos(a), 560 + 300 * math.sin(a), 10, INK, 0)
    for sgn in (-1, 1):
        x = W / 2 + sgn * (180 + 70 * push)
        c.arc(W / 2 + sgn * 70 * push, 560, 250, 120 if sgn < 0 else -60, 240 if sgn < 0 else 60, 34, BROWN)
    c.rect(W / 2 - 60, 300, W / 2 + 60, 360, STEEL, 5, r=8)
    c.arrow(W / 2 - 20, 330, W / 2 - 150, 330, 8, RED, 28); c.arrow(W / 2 + 20, 330, W / 2 + 150, 330, 8, RED, 28)
    c.plate(W / 2, 960, 'колодки распираются изнутри', 52, k=appear(t, 1.0))

def S24(c, t, T, m):
    p = seg(t, m, 0)
    c.title('А-Б-С', appear(t, 0))
    # колесо с датчиком
    c.wheel(330, 560, 160, t * 4 * (0.5 + 0.5 * math.sin(t * 9)))
    c.rect(470, 470, 530, 520, YEL, 4, r=8); c.text(500, 420, 'датчик', 36)
    # график давления — пила
    x0, x1, y0, y1 = 650, 1750, 780, 330
    c.line([(x0, y0), (x1, y0)], 6); c.line([(x0, y0), (x0, y1)], 6)
    c.text(x0 + 10, y1 - 30, 'давление', 36, anchor='lm'); c.text(x1, y0 + 40, 'время', 36, anchor='rm')
    prog = ease(ph(p, 0.25, 0.85))
    pts = []
    n = 160
    for i in range(int(n * prog) + 1):
        f = i / n; x = lerp(x0, x1, f)
        saw = (f * 22) % 1
        v = 0.85 - 0.35 * (saw if saw < 0.6 else (1 - saw) * 1.5)
        pts.append((x, lerp(y0, y1, v)))
    if len(pts) > 1: c.line(pts, 8, RED)
    c.plate(1200, 900, 'отпустил — сжал: до 40 раз в секунду', 52, RED, k=appear(p, 0.7, 0.06))

def S25(c, t, T, m):
    p = seg(t, m, 0)
    c.title('ТОРМОЗА СИЛЬНЕЕ МОТОРА', appear(t, 0), size=64)
    for i, (lab, tot, col, at) in enumerate((('разгон 0–100 км/ч', 11.2, ORANGE, 0.35), ('тормоз 100–0 км/ч', 3.5, RED, 0.62))):
        cx = 600 + i * 720
        v = tot * ease(ph(p, at, at + 0.25))
        c.circ(cx, 560, 220, WHITE, 8); c.rect(cx - 30, 300, cx + 30, 340, INK, 0)
        a = math.radians(-90 + 360 * (v % 12) / 12)
        c.line([(cx, 560), (cx + 180 * math.cos(a), 560 + 180 * math.sin(a))], 12, col)
        c.circ(cx, 560, 16, INK, 0)
        c.text(cx, 660, f'{v:.1f} с', 60, col)
        c.plate(cx, 870, lab, 54, k=appear(p, at - 0.05, 0.06))

def bounce_car(c, t, t0, damp, x, label):
    tt = max(t - t0, 0)
    off = 60 * math.exp(-damp * tt) * math.sin(tt * 7) if t >= t0 else 0
    cy = 600
    c.line([(x - 320, cy + 170), (x + 320, cy + 170)], 6)
    c.spring(x - 180, cy + 10 + off, cy + 150, 54, 6, 10)
    if damp > 1:
        c.rect(x - 10 - 20, cy + 20 + off, x + 30, cy + 100 + off, DSTEEL, 4, r=6); c.line([(x, cy + 100), (x, cy + 150)], 10, INK)
    c.rect(x - 300, cy - 120 + off, x + 300, cy + 10 + off, BLUE, 6, r=40)
    c.rect(x - 160, cy - 200 + off, x + 120, cy - 120 + off, LBLUE, 6, r=30)
    c.plate(x, cy + 280, label, 48)

def S26(c, t, T, m):
    if t < m[0][1]:
        p = seg(t, m, 0)
        c.title('ПРУЖИНА', appear(t, 0))
        bounce_car(c, t, m[0][0] + (m[0][1] - m[0][0]) * 0.45, 0.25, W / 2, 'одна пружина — качели')
    else:
        c.title('ПРУЖИНА + АМОРТИЗАТОР', size=64)
        bounce_car(c, t, m[1][0] + 0.3, 0.25, 520, 'без амортизатора')
        bounce_car(c, t, m[1][0] + 0.3, 3.5, 1400, 'с амортизатором')

def palm(c, x, y, s=1.0, col=(240, 196, 160)):
    c.rect(x - 70 * s, y - 60 * s, x + 70 * s, y + 90 * s, col, 5, r=40 * s)
    for i in range(4):
        fx = x - 55 * s + i * 37 * s
        c.rect(fx - 15 * s, y - 170 * s + abs(i - 1.5) * 18 * s, fx + 15 * s, y - 40 * s, col, 5, r=15 * s)
    c.rect(x + 60 * s, y - 40 * s, x + 130 * s, y + 0 * s, col, 5, r=18 * s)

def S27(c, t, T, m):
    if t < m[0][1]:
        p = seg(t, m, 0)
        c.title('ПЯТНО КОНТАКТА', appear(t, 0))
        c.rect(300, 760, 1620, 800, (90, 90, 96), 0)
        c.wheel(700, 520, 240, 0)
        k = appear(p, 0.4, 0.08)
        c.rect(600, 750, 800, 772, ORANGE, 4) if k > 0.02 else None
        c.rect(1200, 380, 1520, 700, mix(BG, ORANGE, 0.5), 5, r=20)
        palm(c, 1360, 560, 1.0 * k)
        c.plate(1360, 900, 'каждое — примерно с ладонь', 50, k=appear(p, 0.6, 0.08))
    else:
        p = seg(t, m, 1)
        c.title('4 ЛАДОНИ ДЕРЖАТ ВСЮ МАШИНУ', size=60)
        wf = {k: ORANGE for k in ('fl', 'fr', 'rl', 'rr')}
        car_top(c, 760, 600, 1.15, 0, wheel_fill=wf)
        for i, s in enumerate(('разгоняют', 'тормозят', 'поворачивают')):
            c.plate(1560, 380 + i * 120, s, 50, k=appear(p, 0.08 + i * 0.12, 0.06))
        c.plate(W / 2, 960, 'резина — самое важное', 56, RED, k=appear(p, 0.6, 0.06))

# ---------------- 5 слов ----------------
def word_card(c, t, word, sub):
    c.plate(W / 2, 150, word, 110, ORANGE, k=appear(t, 0))
    c.plate(W / 2, 920, sub, 48, k=appear(t, 0.6))

def S28a(c, t, T, m):
    word_card(c, t, 'ТУРБИНА', 'выхлоп крутит — воздух задувает')
    c.circ(760, 540, 180, mix(BG, SMOKE, 0.5), 6); c.circ(1160, 540, 180, mix(BG, LBLUE, 0.5), 6)
    c.line([(760, 540), (1160, 540)], 20, INK)
    for x, col in ((760, SMOKE), (1160, LBLUE)):
        for i in range(8):
            a = t * 12 + i * 0.785
            c.line([(x, 540), (x + 150 * math.cos(a), 540 + 150 * math.sin(a))], 10, mix(col, INK, 0.4))
    for i in range(3):
        k = (t + i / 3) % 1
        c.circ(480 + k * 200, 540 - 40 + i * 40, 20, mix(SMOKE, BG, k * 0.5), 3)
        c.arrow(1360 + k * 140, 500 + i * 40, 1440 + k * 140, 500 + i * 40, 8, LBLUE, 26)

def S28b(c, t, T, m):
    word_card(c, t, 'ИНЖЕКТОР', 'бензин брызгает электроника')
    c.poly([(900, 260), (1020, 260), (990, 560), (930, 560)], DSTEEL, 6)
    c.rect(880, 240, 1040, 300, INK, 0, r=10); c.line([(1040, 270), (1260, 270)], 8, YEL)
    c.rect(1260, 220, 1400, 320, (60, 70, 80), 5, r=12)
    random.seed(int(t * 20))
    for i in range(26):
        k = random.random(); a = math.radians(random.uniform(60, 120))
        c.circ(960 + k * 280 * math.cos(a), 580 + k * 280 * math.sin(a), 8 + 6 * k, YEL, 2)

def S28c(c, t, T, m):
    word_card(c, t, 'ЭУР', 'моторчик помогает крутить руль')
    a = 0.6 * math.sin(t * 2)
    c.circ(800, 540, 220, None, 34); c.circ(800, 540, 220, None, 0)
    c.arc(800, 540, 220, 0, 360, 40, INK)
    for i in range(3):
        aa = a + i * 2.094 + 1.57
        c.line([(800, 540), (800 + 210 * math.cos(aa), 540 + 210 * math.sin(aa))], 30, INK)
    c.circ(800, 540, 50, INK, 0)
    c.rect(1180, 460, 1380, 620, (90, 160, 120), 6, r=16); c.text(1280, 540, 'мотор', 40, WHITE)
    c.gear(1100, 540, 60, 10, t * 6, YEL)
    c.arrow(1080, 380, 960, 330, 10, ORANGE, 30)

def S28d(c, t, T, m):
    word_card(c, t, 'ESP', 'подтормаживает колесо — не развернёт')
    p = ph(t, 0.3, T * 0.9)
    cx, cy, R = 960, 1450, 900
    c.arc(cx, cy, R, 225, 315, 6, mix(BG, INK, 0.3))
    a = math.radians(225 + 90 * p)
    x, y = cx + R * math.cos(a), cy + R * math.sin(a)
    brake = (t * 3) % 1 < 0.5
    car_top(c, x, y, 0.5, a + math.pi / 2, wheel_fill={'rr': RED if brake else (40, 40, 46)})

def S28e(c, t, T, m):
    word_card(c, t, 'КРОССОВЕР', 'та же легковушка, только повыше')
    hgt = lerp(1.0, 1.35, ease(ph(t, 0.6, T * 0.6)))
    lift = lerp(0, 40, ease(ph(t, 0.6, T * 0.6)))
    car_side(c, 960 - 702 * 0.95 / 2, 760 - lift, 0.95, height=hgt)
    if lift > 1:
        c.line([(960 - 300, 760 - lift + 20), (960 + 300, 760 - lift + 20)], 2, BG)

def S29(c, t, T, m):
    c.title('ВОТ И ВСЯ МАШИНА', appear(t, 0))
    items = ['мотор', 'коробка', 'привод', 'тормоза', 'подвеска', 'шины']
    ats = [0.1, 0.25, 0.38, 0.52, 0.66, 0.8]
    shown = [appear(t, T * a) for a in ats]
    hi = max([i for i, a in enumerate(ats) if t >= T * a] or [0])
    cards(c, t, items, shown, hi)

def S30(c, t, T, m):
    c.title('РУЧНИК — ТРОС', appear(t, 0))
    pull = ease(ph(t, 0.4, 1.2))
    c.rect(300, 600, 360, 700, INK, 0, r=10)
    ang = math.radians(-20 - 40 * pull)
    c.line([(330, 650), (330 + 220 * math.cos(ang), 650 + 220 * math.sin(ang))], 26, DSTEEL)
    c.line([(360, 660), (1300, 660)], 8, mix(INK, ORANGE, pull))
    c.line([(1300, 660), (1450, 520)], 8, mix(INK, ORANGE, pull)); c.line([(1300, 660), (1450, 800)], 8, mix(INK, ORANGE, pull))
    for y in (520, 800):
        c.circ(1520, y, 90, DSTEEL, 5); c.circ(1520, y, 70, BG, 4)
    c.plate(900, 900, 'тянет задние тормоза', 52, k=appear(t, 0.8))

SCENES = {k: v for k, v in globals().items() if k.startswith('S') and callable(v) and k[1:3].isdigit()}
