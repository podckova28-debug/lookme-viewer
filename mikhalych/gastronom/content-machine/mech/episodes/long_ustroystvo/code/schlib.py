"""Библиотека движущихся схем для длинного ролика: рисуем в 2× (3840×2160) и уменьшаем — сглаживание.
Координаты во всех функциях — в пикселях итогового кадра 1920×1080."""
import math, subprocess
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS, K = 1920, 1080, 30, 2
FONTS = '/home/user/gastronom/content-machine/video/fonts/'

BG = (243, 230, 203); GRID = (234, 219, 190); INK = (43, 33, 24)
ORANGE = (236, 122, 32); BLUE = (48, 78, 136); LBLUE = (150, 200, 240); RED = (222, 56, 44)
YEL = (255, 206, 46); GREEN = (64, 152, 84); STEEL = (176, 184, 192); DSTEEL = (112, 120, 130)
PINK = (238, 140, 186); WHITE = (255, 250, 240); SMOKE = (150, 150, 150); BROWN = (139, 96, 56)
CREAMBOX = (255, 248, 232)

_fonts = {}
def font(size, bold=True):
    k = (size, bold)
    if k not in _fonts:
        _fonts[k] = ImageFont.truetype(FONTS + ('Nunito-Black.ttf' if bold else 'Nunito-800.ttf'), int(size * K))
    return _fonts[k]

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): x = clamp(x); return 0.5 - 0.5 * math.cos(math.pi * x)
def ph(t, a, b): return clamp((t - a) / (b - a)) if b > a else float(t >= a)
def lerp(a, b, k): return a + (b - a) * k
def mix(c1, c2, k): return tuple(int(lerp(a, b, clamp(k))) for a, b in zip(c1, c2))
def pop(x):  # появление с лёгким перелётом
    x = clamp(x); c = 1.7
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


class C:
    """Холст: обёртка над ImageDraw в координатах 1920×1080."""
    def __init__(self):
        self.im = Image.new('RGB', (W * K, H * K), BG)
        self.d = ImageDraw.Draw(self.im)

    def _p(self, pts): return [(x * K, y * K) for x, y in pts]

    def grid(self, step=60):
        for x in range(0, W, step): self.d.line([(x * K, 0), (x * K, H * K)], fill=GRID, width=K * 2)
        for y in range(0, H, step): self.d.line([(0, y * K), (W * K, y * K)], fill=GRID, width=K * 2)

    def poly(self, pts, fill=None, ow=5, oc=INK):
        self.d.polygon(self._p(pts), fill=fill)
        if ow: self.d.line(self._p(list(pts) + [pts[0], pts[1]]), fill=oc, width=int(ow * K), joint='curve')

    def rect(self, x0, y0, x1, y1, fill=None, ow=5, r=0, oc=INK):
        b = [x0 * K, y0 * K, x1 * K, y1 * K]
        if r: self.d.rounded_rectangle(b, int(r * K), fill=fill, outline=oc if ow else None, width=int(ow * K))
        else: self.d.rectangle(b, fill=fill, outline=oc if ow else None, width=int(ow * K))

    def circ(self, cx, cy, r, fill=None, ow=5, oc=INK):
        self.d.ellipse([(cx - r) * K, (cy - r) * K, (cx + r) * K, (cy + r) * K], fill=fill,
                       outline=oc if ow else None, width=int(ow * K))

    def line(self, pts, w=5, c=INK):
        self.d.line(self._p(pts), fill=c, width=int(w * K), joint='curve')

    def arc(self, cx, cy, r, a0, a1, w=6, c=INK):
        self.d.arc([(cx - r) * K, (cy - r) * K, (cx + r) * K, (cy + r) * K], a0, a1, fill=c, width=int(w * K))

    def arrow(self, x0, y0, x1, y1, w=10, c=ORANGE, head=34, oc=INK):
        a = math.atan2(y1 - y0, x1 - x0); bx, by = x1 - head * 0.8 * math.cos(a), y1 - head * 0.8 * math.sin(a)
        self.line([(x0, y0), (bx, by)], w + 6, oc); self.line([(x0, y0), (bx, by)], w, c)
        hp = [(x1, y1), (x1 - head * math.cos(a - 0.5), y1 - head * math.sin(a - 0.5)),
              (x1 - head * math.cos(a + 0.5), y1 - head * math.sin(a + 0.5))]
        self.poly(hp, c, 4, oc)

    def text(self, x, y, s, size=56, c=INK, anchor='mm', bold=True, stroke=0, sc=WHITE):
        if size < 2: return
        self.d.text((x * K, y * K), s, font=font(size, bold), fill=c, anchor=anchor,
                    stroke_width=int(stroke * K), stroke_fill=sc)

    def tw(self, s, size=56): return self.d.textlength(s, font=font(size)) / K

    def plate(self, x, y, s, size=56, c=INK, bg=CREAMBOX, k=1.0, pad=28):
        """Подпись на кремовой плашке; k — масштаб появления (0..1+)."""
        if k <= 0.02: return
        sz = size * k; w = self.tw(s, sz) + pad * 2 * k; h = sz * 1.45
        self.rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2, bg, 5 * k, r=h * 0.32)
        self.text(x, y + sz * 0.02, s, sz, c)

    def title(self, s, k=1.0, y=92, c=INK, size=74):
        self.plate(W / 2, y, s, size, c, k=k)

    def star(self, cx, cy, r, n=10, fill=YEL, ow=4, rot=0):
        pts = []
        for i in range(n * 2):
            rr = r if i % 2 == 0 else r * 0.45
            a = rot + math.pi * i / n
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        self.poly(pts, fill, ow)

    def gear(self, cx, cy, r, n, ang, fill=STEEL, ow=5, depth=None, hub=True):
        depth = depth or r * 0.16; pts = []
        for i in range(n):
            a0 = ang + 2 * math.pi * i / n; st = 2 * math.pi / n
            for f, rr in ((0.0, r), (0.12, r + depth), (0.43, r + depth), (0.55, r)):
                a = a0 + st * f; pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        self.poly(pts, fill, ow)
        if hub:
            self.circ(cx, cy, r * 0.28, mix(fill, WHITE, 0.35), ow)
            for i in range(3):  # спицы-метки, чтобы было видно вращение
                a = ang + i * 2 * math.pi / 3
                self.circ(cx + r * 0.6 * math.cos(a), cy + r * 0.6 * math.sin(a), r * 0.1, mix(fill, INK, 0.35), 0)

    def wheel(self, cx, cy, r, ang=0.0, tyre=(40, 40, 46), rim=STEEL, ow=5):
        self.circ(cx, cy, r, tyre, ow)
        self.circ(cx, cy, r * 0.62, rim, ow * 0.8)
        for i in range(5):
            a = ang + i * 2 * math.pi / 5
            self.line([(cx + r * 0.16 * math.cos(a), cy + r * 0.16 * math.sin(a)),
                       (cx + r * 0.56 * math.cos(a), cy + r * 0.56 * math.sin(a))], 7, DSTEEL)
        self.circ(cx, cy, r * 0.16, DSTEEL, ow * 0.6)

    def spring(self, x, y0, y1, w=60, coils=7, lw=10, c=DSTEEL):
        pts = [(x, y0)]
        n = coils * 2
        for i in range(1, n):
            pts.append((x + (w / 2 if i % 2 else -w / 2), lerp(y0, y1, i / n)))
        pts.append((x, y1))
        self.line(pts, lw + 6, INK); self.line(pts, lw, c)

    def check(self, cx, cy, r=34, ok=True):
        self.circ(cx, cy, r, GREEN if ok else RED, 4)
        if ok: self.line([(cx - r * 0.45, cy), (cx - r * 0.1, cy + r * 0.38), (cx + r * 0.5, cy - r * 0.35)], 9, WHITE)
        else:
            self.line([(cx - r * 0.4, cy - r * 0.4), (cx + r * 0.4, cy + r * 0.4)], 9, WHITE)
            self.line([(cx - r * 0.4, cy + r * 0.4), (cx + r * 0.4, cy - r * 0.4)], 9, WHITE)

    def frame(self): return self.im.reduce(K)


# ---------- машина сбоку и сверху ----------
SEDAN = [(20, -38), (2, -62), (8, -104), (150, -126), (250, -134), (335, -212), (478, -218), (572, -150),
         (690, -138), (702, -98), (698, -52), (680, -38)]
WIN = [(350, -200), (470, -205), (540, -150), (338, -146)]
WIN2 = [(320, -146), (342, -198), (262, -136)]

def car_side(c, x, y, s=1.0, color=BLUE, alpha_body=None, wheel_ang=0.0, height=1.0, flip=False):
    """Седан сбоку, перед слева. (x, y) — точка у земли под передним краем. height — высота кузова (кроссовер)."""
    def tr(pts):
        out = []
        for px, py in pts:
            py2 = py * height if py < -60 else py
            px2 = (702 - px) if flip else px
            out.append((x + px2 * s, y + py2 * s))
        return out
    c.poly(tr(SEDAN), color if alpha_body is None else alpha_body, 5)
    c.poly(tr(WIN), LBLUE, 4); c.poly(tr(WIN2), LBLUE, 4)
    fx, rx = (130, 565) if not flip else (572, 137)
    by = y - 40 * s
    c.wheel(x + fx * s, by - (0 if height == 1 else 0), 58 * s, wheel_ang)
    c.wheel(x + rx * s, by, 58 * s, wheel_ang)
    return dict(front=(x + fx * s, by), rear=(x + rx * s, by))

def rot(pts, cx, cy, a):
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + (px - cx) * ca - (py - cy) * sa, cy + (px - cx) * sa + (py - cy) * ca) for px, py in pts]

def car_top(c, cx, cy, s=1.0, a=0.0, color=BLUE, wheel_fill=None, steer=0.0):
    """Машина сверху, перед справа. wheel_fill — dict {'fl','fr','rl','rr': цвет}. Возвращает центры колёс."""
    L, Wd = 620 * s, 280 * s
    body = []
    r = 70 * s
    for k in range(4):  # скруглённый прямоугольник
        qx = cx + (L / 2 - r) * (1 if k in (0, 1) else -1); qy = cy + (Wd / 2 - r) * (1 if k in (1, 2) else -1)
        a0 = [-90, 0, 90, 180][k]
        for i in range(7):
            aa = math.radians(a0 + 15 * i); body.append((qx + r * math.cos(aa), qy + r * math.sin(aa)))
    wf = wheel_fill or {}
    pos = {'fl': (cx + L * 0.3, cy - Wd / 2), 'fr': (cx + L * 0.3, cy + Wd / 2),
           'rl': (cx - L * 0.3, cy - Wd / 2), 'rr': (cx - L * 0.3, cy + Wd / 2)}
    out = {}
    for k, (wx, wy) in pos.items():
        st = steer if k[0] == 'f' else 0
        wpts = [(wx - 52 * s, wy - 22 * s), (wx + 52 * s, wy - 22 * s), (wx + 52 * s, wy + 22 * s), (wx - 52 * s, wy + 22 * s)]
        wpts = rot(wpts, wx, wy, st)
        c.poly(rot(wpts, cx, cy, a), wf.get(k, (40, 40, 46)), 4)
        out[k] = rot([(wx, wy)], cx, cy, a)[0]
    c.poly(rot(body, cx, cy, a), color, 5)
    glass = [(cx + L * 0.12, cy - Wd * 0.36), (cx + L * 0.24, cy - Wd * 0.3), (cx + L * 0.24, cy + Wd * 0.3), (cx + L * 0.12, cy + Wd * 0.36)]
    c.poly(rot(glass, cx, cy, a), LBLUE, 4)
    roof = [(cx - L * 0.2, cy - Wd * 0.34), (cx + L * 0.1, cy - Wd * 0.34), (cx + L * 0.1, cy + Wd * 0.34), (cx - L * 0.2, cy + Wd * 0.34)]
    c.poly(rot(roof, cx, cy, a), mix(color, WHITE, 0.15), 4)
    rg = [(cx - L * 0.32, cy - Wd * 0.32), (cx - L * 0.22, cy - Wd * 0.34), (cx - L * 0.22, cy + Wd * 0.34), (cx - L * 0.32, cy + Wd * 0.32)]
    c.poly(rot(rg, cx, cy, a), LBLUE, 4)
    return out


# ---------- цилиндр мотора ----------
def cylinder(c, cx, top, w=300, h=420, crank=0.0, gas=None, gas_a=1.0, iv=0.0, ev=0.0, spark=0.0,
             inj=0.0, flow_in=0.0, flow_out=0.0, t=0.0, small=False, ports=True):
    """Разрез цилиндра. crank — угол коленвала в рад (0 — поршень в ВМТ). iv/ev — открытие клапанов 0..1.
    gas — цвет смеси в камере. spark 0..1 — вспышка свечи. Возвращает y верха поршня."""
    ow = 4 if small else 6
    stroke = h * 0.42; rod = h * 0.55
    crx, cry = cx, top + h + rod * 0.5
    crr = stroke / 2
    px = crx + crr * math.sin(crank); py = cry - crr * math.cos(crank)
    piston_y = py - math.sqrt(max(rod ** 2 - (px - crx) ** 2, 1))  # низ поршня (палец)
    ptop = piston_y - h * 0.14
    # камера (газ)
    head_bot = top + h * 0.12
    if gas:
        c.rect(cx - w / 2 + 8, head_bot, cx + w / 2 - 8, ptop, mix(BG, gas, gas_a), 0)
    # стенки
    c.rect(cx - w / 2 - 34, top, cx - w / 2, top + h + 10, STEEL, ow)
    c.rect(cx + w / 2, top, cx + w / 2 + 34, top + h + 10, STEEL, ow)
    # головка с каналами
    c.rect(cx - w / 2 - 34, top - h * 0.16, cx + w / 2 + 34, head_bot, STEEL, ow)
    # впускной канал (слева) и выпускной (справа)
    if ports: c.poly([(cx - w / 2 - 120, top - h * 0.05), (cx - w * 0.18, top - h * 0.05), (cx - w * 0.18, head_bot), (cx - w / 2 - 120, top + h * 0.06)],
           mix(BG, LBLUE, 0.6), ow)
    if ports: c.poly([(cx + w / 2 + 120, top - h * 0.05), (cx + w * 0.18, top - h * 0.05), (cx + w * 0.18, head_bot), (cx + w / 2 + 120, top + h * 0.06)],
           mix(BG, SMOKE, 0.5), ow)
    # клапаны
    for vx, op, col in ((cx - w * 0.28, iv, LBLUE), (cx + w * 0.28, ev, SMOKE)):
        dy = op * h * 0.07
        c.line([(vx, top - h * 0.2), (vx, head_bot - 4 + dy)], 10 if not small else 7, DSTEEL)
        c.poly([(vx - w * 0.13, head_bot + dy), (vx + w * 0.13, head_bot + dy), (vx + w * 0.07, head_bot - 12 + dy), (vx - w * 0.07, head_bot - 12 + dy)], col, 4)
    # свеча
    c.rect(cx - 16, top - h * 0.3, cx + 16, head_bot + 4, WHITE, 4)
    c.rect(cx - 22, top - h * 0.36, cx + 22, top - h * 0.28, DSTEEL, 4)
    if spark > 0:
        c.star(cx, head_bot + 28, 34 + 40 * spark, 9, YEL, 4, rot=t * 9)
    # форсунка во впускном канале
    if ports: c.poly([(cx - w / 2 - 70, top - h * 0.2), (cx - w / 2 - 40, top - h * 0.2), (cx - w / 2 - 50, top - h * 0.04), (cx - w / 2 - 60, top - h * 0.04)], DSTEEL, 4)
    if inj > 0:
        for i in range(6):
            k = (t * 2.5 + i / 6) % 1
            c.circ(cx - w / 2 - 55 + k * 60, top - h * 0.02 + k * 40, 7, YEL, 2)
    # потоки
    if flow_in > 0:
        for i in range(4):
            k = (t * 1.2 + i / 4) % 1
            c.arrow(cx - w / 2 - 190 + k * 120, top + h * 0.0, cx - w / 2 - 120 + k * 120, top + h * 0.0, 8, LBLUE, 26)
    if flow_out > 0:
        for i in range(3):
            k = (t * 1.2 + i / 3) % 1
            c.circ(cx + w / 2 + 60 + k * 140, top - h * 0.0 - k * 20, 18 + 10 * k, mix(SMOKE, BG, k * 0.6), 3)
    # поршень
    c.rect(cx - w / 2 + 6, ptop, cx + w / 2 - 6, piston_y + h * 0.04, (196, 202, 210), ow, r=6)
    for i in range(2): c.line([(cx - w / 2 + 6, ptop + 14 + i * 14), (cx + w / 2 - 6, ptop + 14 + i * 14)], 4, DSTEEL)
    # шатун и кривошип
    c.circ(crx, cry, crr + 24, (205, 205, 210), ow)
    c.line([(cx, piston_y), (px, py)], 26 if not small else 18, INK)
    c.line([(cx, piston_y), (px, py)], 16 if not small else 10, DSTEEL)
    c.circ(px, py, 14, DSTEEL, 4); c.circ(cx, piston_y, 12, DSTEEL, 4)
    c.circ(crx, cry, 16, INK, 0)
    return ptop


def render(scene, T, out, m=None, **kw):
    """scene(c, t, T, **kw) → mp4 1920×1080 30 к/с длиной T."""
    n = int(round(T * FPS))
    enc = subprocess.Popen([FF, '-hide_banner', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                            '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast',
                            '-crf', '18', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i in range(n):
        c = C(); c.grid(); scene(c, i / FPS, T, m if m is not None else [(0, T)])
        enc.stdin.write(c.frame().tobytes())
    enc.stdin.close(); enc.wait()
