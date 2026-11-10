# Procedural (zero-credit) animated shots for the long documentaries.
# Every shot: AnimShot(spec, dur) with .frame(t) -> PIL RGB 1920x1080.
# spec strings (from plan.py SHOTS, prefixed "a:"):
#   chess:FROM:TO            chessboard filling FROM..TO squares + "N / 64" counter
#   map:FROM:TO              stylised city map, park area, pins dropping FROM..TO
#   timeline:YEAR            timeline 1974-2007, drawn up to YEAR, YEAR highlighted
#   headline:TEXT            newspaper slams in with a big headline
#   note                     handwritten note is "written", then a crimson circle marks a line
#   ticket                   metro ticket slides in, scan line, "time recorded"
#   cctv:IMG:HH:MM:SS        CCTV look over a still: grain, scanlines, REC, ticking timecode
#   board:IMG,IMG,IMG,IMG    evidence board, photos pinned, crimson string connects them
#   count:N:LABEL            big number counts up 0..N with a label
#   stamp:IMG:TEXT           still with Ken Burns, a rubber stamp slams on
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import render as R

W, H = R.W, R.H
CREAM, INK, CRIMSON = R.CREAM, R.INK, R.CRIMSON
GREY = (120, 114, 106)
LIGHT = (214, 205, 186)

def ease(x): return R.ease(x)
def pop(x):
    x = max(0.0, min(1.0, x))
    return 1 + 2.2 * (x - 1) ** 3 + 1.2 * (x - 1) ** 2 if x < 1 else 1.0  # slight overshoot

def zoom_frame(im, t, dur, z0=1.0, z1=1.06, cx=0.5, cy=0.5):
    z = z0 + (z1 - z0) * (t / max(dur, 1e-3))
    cw, ch = W / z, H / z
    x0 = (W - cw) * cx; y0 = (H - ch) * cy
    return im.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))

def shadow_paste(base, card, x, y, blur=10, off=(12, 16), alpha=110):
    sh = Image.new("RGBA", (card.width + 60, card.height + 60), (0, 0, 0, 0))
    m = card.split()[3] if card.mode == "RGBA" else Image.new("L", card.size, 255)
    blk = Image.new("RGBA", card.size, (0, 0, 0, alpha)); blk.putalpha(m.point(lambda v: v * alpha // 255))
    sh.alpha_composite(blk, (30, 30)); sh = sh.filter(ImageFilter.GaussianBlur(blur))
    base.paste(sh, (int(x - 30 + off[0]), int(y - 30 + off[1])), sh)
    base.paste(card, (int(x), int(y)), card if card.mode == "RGBA" else None)

def load_img(sid, w=None):
    im = Image.open(f"{R.ROOT}/img/{sid}.png").convert("RGB")
    if w: im = im.resize((w, int(w * im.height / im.width)), Image.LANCZOS)
    return im

# ---------------------------------------------------------------- chess
class Chess:
    def __init__(self, a, b, dur):
        self.a, self.b, self.dur = int(a), int(b), dur
        rng = random.Random(64); self.order = list(range(64)); rng.shuffle(self.order)
        self.cell = 104; self.x0 = 230; self.y0 = (H - 8 * self.cell) // 2
        bg = R.paper(); d = ImageDraw.Draw(bg)
        c = self.cell; x0, y0 = self.x0, self.y0
        d.rectangle((x0 - 26, y0 - 26, x0 + 8 * c + 26, y0 + 8 * c + 26), fill=(70, 52, 38))
        for r in range(8):
            for k in range(8):
                col = LIGHT if (r + k) % 2 == 0 else (92, 84, 76)
                d.rectangle((x0 + k * c, y0 + r * c, x0 + (k + 1) * c - 1, y0 + (r + 1) * c - 1), fill=col)
        f = R.font(34)
        for k in range(8):
            d.text((x0 + k * c + c / 2 - 8, y0 + 8 * c + 30), "ABCDEFGH"[k], font=f, fill=INK)
            d.text((x0 - 60, y0 + k * c + c / 2 - 22), str(8 - k), font=f, fill=INK)
        self.bg = bg
    def frame(self, t):
        im = self.bg.copy(); d = ImageDraw.Draw(im)
        span = max(1, self.b - self.a)
        p = ease(t / (self.dur * 0.8)) if self.b > self.a else 1.0
        n_now = self.a + (self.b - self.a) * p
        c = self.cell
        for i in range(int(math.ceil(n_now))):
            sq = self.order[i]; r, k = divmod(sq, 8)
            local = 1.0 if i < self.a else min(1.0, (n_now - i) * 1.0 + 0.0)
            s = pop(local) if i >= self.a else 1.0
            rad = int(c * 0.34 * s)
            cx = self.x0 + k * c + c // 2; cy = self.y0 + r * c + c // 2
            if rad > 0:
                d.ellipse((cx - rad + 4, cy - rad + 6, cx + rad + 4, cy + rad + 6), fill=(30, 20, 18))
                d.ellipse((cx - rad, cy - rad, cx + rad, cy + rad), fill=CRIMSON)
        cnt = int(round(n_now))
        f1, f2, f3 = R.font(250), R.font(110), R.font(56)
        xr = self.x0 + 8 * c + 170
        s = f"{cnt}"
        d.text((xr, 250), s, font=f1, fill=CRIMSON)
        tw = d.textlength(s, font=f1)
        d.text((xr + tw + 20, 370), "/ 64", font=f2, fill=INK)
        d.rectangle((xr, 600, xr + 560, 608), fill=INK)
        d.text((xr, 630), "КЛЕТОК ЗАНЯТО", font=f3, fill=INK)
        return zoom_frame(im, t, self.dur, 1.0, 1.04, 0.35, 0.5)

# ---------------------------------------------------------------- map
class Map:
    def __init__(self, a, b, dur):
        self.a, self.b, self.dur = int(a), int(b), dur
        rng = random.Random(11)
        bg = R.paper(); d = ImageDraw.Draw(bg)
        # streets
        for _ in range(38):
            if rng.random() < 0.5:
                y = rng.randint(0, H); d.line((0, y, W, y + rng.randint(-160, 160)), fill=(170, 162, 148), width=rng.choice([3, 3, 6]))
            else:
                x = rng.randint(0, W); d.line((x, 0, x + rng.randint(-160, 160), H), fill=(170, 162, 148), width=rng.choice([3, 3, 6]))
        # blocks
        for _ in range(160):
            x, y = rng.randint(0, W), rng.randint(0, H); w, h = rng.randint(30, 90), rng.randint(20, 60)
            d.rectangle((x, y, x + w, y + h), fill=(196, 188, 170))
        # river
        pts = [(0, 880)] + [(x, 880 - 90 * math.sin(x / 300) - x * 0.12) for x in range(0, W + 1, 40)]
        d.line(pts, fill=(140, 134, 124), width=26)
        # park polygon
        cx, cy = 980, 540
        poly = []
        for k in range(28):
            ang = 2 * math.pi * k / 28
            rr = 330 + 70 * math.sin(3 * ang) + rng.randint(-25, 25)
            poly.append((cx + rr * 1.45 * math.cos(ang), cy + rr * 0.95 * math.sin(ang)))
        self.poly = poly
        mask = Image.new("L", (W, H), 0); ImageDraw.Draw(mask).polygon(poly, fill=255)
        park = Image.new("RGB", (W, H), (92, 96, 84)); pd = ImageDraw.Draw(park)
        for x in range(-H, W, 22): pd.line((x, H, x + H, 0), fill=(70, 74, 64), width=6)
        for _ in range(500):
            x, y = rng.randint(0, W), rng.randint(0, H); r = rng.randint(6, 14)
            pd.ellipse((x - r, y - r, x + r, y + r), fill=(60, 64, 56))
        bg.paste(park, (0, 0), mask)
        d.line(poly + [poly[0]], fill=INK, width=6)
        f = R.font(64)
        lab = "БИТЦЕВСКИЙ ПАРК"; tw = d.textlength(lab, font=f)
        d.rectangle((cx - tw / 2 - 24, cy - 50, cx + tw / 2 + 24, cy + 46), fill=CREAM)
        d.text((cx - tw / 2, cy - 48), lab, font=f, fill=INK)
        d.rectangle((60, 60, 600, 150), fill=CREAM); d.rectangle((60, 60, 76, 150), fill=CRIMSON)
        d.text((100, 62), "МОСКВА · ЮГ", font=R.font(66), fill=INK)
        self.bg = bg
        self.pins = []
        while len(self.pins) < 70:
            x, y = rng.randint(500, 1460), rng.randint(180, 900)
            if mask.getpixel((x, y)) and abs(y - cy) > 60: self.pins.append((x, y))
    def frame(self, t):
        im = self.bg.copy(); d = ImageDraw.Draw(im)
        p = ease(t / (self.dur * 0.8)) if self.b > self.a else 1.0
        n_now = self.a + (self.b - self.a) * p
        for i in range(int(math.ceil(n_now))):
            x, y = self.pins[i]
            local = 1.0 if i < self.a else min(1.0, n_now - i)
            drop = int((1 - ease(local)) * 120)
            d.ellipse((x - 9, y - 4, x + 9, y + 6), fill=(40, 30, 28))
            d.line((x, y, x, y - 40 - drop), fill=INK, width=4)
            d.ellipse((x - 16, y - 70 - drop, x + 16, y - 38 - drop), fill=CRIMSON, outline=INK, width=3)
        if self.b > 0:
            f = R.font(54); s = f"{int(round(n_now))}"
            d.rectangle((W - 480, 60, W - 60, 170), fill=CREAM); d.rectangle((W - 480, 60, W - 464, 170), fill=CRIMSON)
            d.text((W - 440, 64), s, font=R.font(90), fill=CRIMSON)
            d.text((W - 440 + d.textlength(s, font=R.font(90)) + 18, 96), "МЕТОК", font=f, fill=INK)
        return zoom_frame(im, t, self.dur, 1.0, 1.12, 0.5, 0.5)

# ---------------------------------------------------------------- timeline
YEARS = [1974, 1992, 2001, 2006, 2007]
class Timeline:
    def __init__(self, year, dur):
        self.year, self.dur = int(year), dur
    def frame(self, t):
        im = R.paper(); d = ImageDraw.Draw(im)
        x0, x1, y = 160, W - 160, 600
        pos = {yy: x0 + (x1 - x0) * i / (len(YEARS) - 1) for i, yy in enumerate(YEARS)}
        target = pos[self.year]
        p = ease(t / 1.4)
        prev = [yy for yy in YEARS if yy < self.year]
        start = pos[prev[-1]] if prev else x0
        cur = start + (target - start) * p
        d.line((x0, y, x1, y), fill=(180, 172, 158), width=8)
        d.line((x0, y, cur, y), fill=INK, width=12)
        for yy in YEARS:
            xx = pos[yy]
            on = xx <= cur + 1
            d.ellipse((xx - 18, y - 18, xx + 18, y + 18), fill=(CRIMSON if yy == self.year and on else (INK if on else (180, 172, 158))))
            f = R.font(54 if yy != self.year else 64)
            s = str(yy); tw = d.textlength(s, font=f)
            d.text((xx - tw / 2, y + 40), s, font=f, fill=INK if on else (170, 162, 148))
        if p > 0.6:
            k = ease((t - 0.9) / 0.5)
            f = R.font(260); s = str(self.year); tw = d.textlength(s, font=f)
            d.text((target - tw / 2 if 300 < target < W - 300 else W / 2 - tw / 2, 170 + int(30 * (1 - k))), s, font=f,
                   fill=tuple(int(CREAM[i] + (CRIMSON[i] - CREAM[i]) * k) for i in range(3)))
        return zoom_frame(im, t, self.dur, 1.0, 1.03)

# ---------------------------------------------------------------- headline
class Headline:
    def __init__(self, text, dur):
        self.dur = dur; self.text = text.upper()
        rng = random.Random(5)
        pw, ph = 1300, 900
        pg = Image.new("RGBA", (pw, ph), (232, 226, 212, 255)); d = ImageDraw.Draw(pg)
        d.text((60, 30), "ГОРОДСКИЕ НОВОСТИ", font=R.font(86), fill=INK)
        d.line((60, 140, pw - 60, 140), fill=INK, width=6); d.line((60, 152, pw - 60, 152), fill=INK, width=2)
        f = R.font(120); words = self.text.split(); lines, cur = [], ""
        for w_ in words:
            if d.textlength((cur + " " + w_).strip(), font=f) > pw - 120: lines.append(cur); cur = w_
            else: cur = (cur + " " + w_).strip()
        lines.append(cur)
        y = 180
        for ln in lines:
            d.text((60, y), ln, font=f, fill=INK); y += 140
        d.rectangle((60, y + 10, 560, y + 330), fill=(150, 144, 134))
        for col in range(3):
            xx = 60 + col * 400
            for k in range(22):
                yy = y + 360 + k * 20 if col < 1 else y + 20 + k * 22
                if col == 0 and yy > ph - 40: break
                if col > 0 and (xx < 600): continue
                ln_w = rng.randint(220, 360)
                if yy < ph - 30: d.rectangle((xx if col else 60, yy, (xx if col else 60) + ln_w, yy + 8), fill=(150, 144, 134))
        for k in range(16):
            yy = y + 20 + k * 22
            if yy < ph - 30: d.rectangle((620, yy, 620 + rng.randint(420, 620), yy + 8), fill=(150, 144, 134))
        d.rectangle((0, 0, pw - 1, ph - 1), outline=(170, 162, 148), width=4)
        self.page = pg
    def frame(self, t):
        im = R.paper()
        k = ease(t / 0.55)
        sc = 0.25 + 0.75 * k; ang = (1 - k) * 540 - 3
        pg = self.page.resize((int(self.page.width * sc), int(self.page.height * sc)), Image.BICUBIC).rotate(ang, expand=True, resample=Image.BICUBIC)
        shadow_paste(im, pg, (W - pg.width) / 2, (H - pg.height) / 2)
        return zoom_frame(im, t, self.dur, 1.0, 1.08)

# ---------------------------------------------------------------- note
class Note:
    def __init__(self, dur):
        self.dur = dur
        rng = random.Random(3)
        self.lines = []
        for k in range(7):
            pts = []; x = 0
            wlen = rng.randint(560, 820) if k != 2 else 760
            while x < wlen:
                pts.append((x, rng.uniform(-10, 10) + 8 * math.sin(x / 9))); x += 6
            self.lines.append(pts)
    def frame(self, t):
        im = R.paper()
        nw, nh = 1000, 760
        note = Image.new("RGBA", (nw, nh), (244, 240, 228, 255)); d = ImageDraw.Draw(note)
        for k in range(10): d.line((40, 90 + k * 66, nw - 40, 90 + k * 66), fill=(186, 196, 210), width=2)
        d.line((110, 0, 110, nh), fill=(214, 150, 150), width=3)
        write_p = min(1.0, t / (self.dur * 0.55))
        total = sum(len(l) for l in self.lines); budget = int(total * write_p)
        for k, pts in enumerate(self.lines):
            if budget <= 0: break
            seg = pts[:budget]; budget -= len(pts)
            yy = 80 + k * 66
            if len(seg) > 1: d.line([(150 + x, yy + y) for x, y in seg], fill=(40, 46, 88), width=5)
        circ_p = ease((t - self.dur * 0.6) / 0.8)
        if circ_p > 0:
            yy = 80 + 2 * 66; cx, cy, rx, ry = 150 + 380, yy, 430, 52
            steps = int(80 * circ_p)
            pts = [(cx + rx * math.cos(2 * math.pi * s / 80 - 2.6), cy + ry * math.sin(2 * math.pi * s / 80 - 2.6)) for s in range(steps + 1)]
            if len(pts) > 1: d.line(pts, fill=CRIMSON, width=9)
        note = note.rotate(-3, expand=True, resample=Image.BICUBIC)
        shadow_paste(im, note, 230, 150)
        lab_p = ease((t - self.dur * 0.6 - 0.6) / 0.4)
        if lab_p > 0:
            dd = ImageDraw.Draw(im)
            dd.line((1240, 360, 1420, 300), fill=CRIMSON, width=8)
            f = R.font(72)
            dd.rectangle((1400, 220, 1400 + 440, 220 + 200), fill=CREAM)
            dd.rectangle((1400, 220, 1416, 420), fill=CRIMSON)
            dd.text((1440, 226), "ИМЯ", font=f, fill=INK)
            dd.text((1440, 316), "И ТЕЛЕФОН", font=f, fill=CRIMSON)
        return zoom_frame(im, t, self.dur, 1.0, 1.06, 0.4, 0.4)

# ---------------------------------------------------------------- ticket
class Ticket:
    def __init__(self, dur): self.dur = dur
    def frame(self, t):
        im = R.paper()
        tw_, th_ = 1100, 640
        c = Image.new("RGBA", (tw_, th_), (236, 232, 222, 255)); d = ImageDraw.Draw(c)
        d.rounded_rectangle((0, 0, tw_ - 1, th_ - 1), 40, outline=INK, width=6)
        d.rectangle((0, 70, tw_, 150), fill=CRIMSON)
        d.text((60, 76), "ПРОЕЗДНОЙ БИЛЕТ", font=R.font(62), fill=CREAM)
        d.text((60, 190), "МЕТРОПОЛИТЕН", font=R.font(54), fill=INK)
        d.rectangle((0, 420, tw_, 520), fill=(40, 36, 34))
        rng = random.Random(9)
        for k in range(14): d.rectangle((60 + k * 50, 300, 90 + k * 50, 300 + rng.randint(30, 80)), fill=GREY)
        k = ease(t / 0.6)
        x = W / 2 - tw_ / 2 + (1 - k) * 1400
        rot = c.rotate(4 * (1 - k) - 2, expand=True, resample=Image.BICUBIC)
        shadow_paste(im, rot, x, H / 2 - th_ / 2 - 40)
        d2 = ImageDraw.Draw(im)
        sp = (t - 1.0) / 1.0
        if 0 < sp < 1:
            sx = W / 2 - tw_ / 2 + tw_ * sp
            d2.rectangle((sx - 4, 180, sx + 4, H - 180), fill=CRIMSON)
        if t > 2.1:
            kk = ease((t - 2.1) / 0.4)
            f = R.font(70); s = "ВРЕМЯ ПРОХОДА ЗАФИКСИРОВАНО"; sw = d2.textlength(s, font=f)
            y = H - 200 + int(20 * (1 - kk))
            d2.rectangle((W / 2 - sw / 2 - 30, y - 10, W / 2 + sw / 2 + 30, y + 96), fill=INK)
            d2.text((W / 2 - sw / 2, y), s, font=f, fill=CREAM)
        return zoom_frame(im, t, self.dur, 1.0, 1.04)

# ---------------------------------------------------------------- cctv
class Cctv:
    def __init__(self, sid, hh, mm, ss, dur):
        self.dur = dur; self.t0 = int(hh) * 3600 + int(mm) * 60 + int(ss)
        src = load_img(sid, W + 120).convert("L")
        src = Image.eval(src, lambda v: int(30 + v * 0.75))
        self.src = Image.merge("RGB", (src, src, src))
        sl = Image.new("L", (W, H), 0); d = ImageDraw.Draw(sl)
        for y in range(0, H, 4): d.line((0, y, W, y), fill=40)
        self.scan = sl
        yy, xx = np.mgrid[0:H, 0:W]
        v = 1 - 0.55 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
        self.vig = np.clip(v, 0.25, 1)[..., None].astype(np.float32)
    def frame(self, t):
        ox = int(60 - 60 * t / self.dur)
        im = self.src.crop((ox, 20, ox + W, 20 + H))
        a = np.asarray(im).astype(np.float32)
        a = a * self.vig + np.random.default_rng(int(t * 30)).normal(0, 14, (H, W, 1)).astype(np.float32)
        a -= np.asarray(self.scan)[..., None].astype(np.float32) * 0.5
        im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
        d = ImageDraw.Draw(im); f = R.font(54)
        s = self.t0 + int(t)
        d.text((60, 50), "CAM 03", font=f, fill=(235, 235, 235))
        ts = f"14.06.2006  {s // 3600:02d}:{(s // 60) % 60:02d}:{s % 60:02d}"
        d.text((W - 60 - d.textlength(ts, font=f), H - 110), ts, font=f, fill=(235, 235, 235))
        if int(t * 2) % 2 == 0:
            d.ellipse((W - 250, 62, W - 216, 96), fill=(220, 30, 30))
        d.text((W - 200, 50), "REC", font=f, fill=(235, 235, 235))
        return im

# ---------------------------------------------------------------- evidence board
class Board:
    def __init__(self, ids, dur):
        self.dur = dur
        rng = random.Random(21)
        bg = Image.new("RGB", (W, H), (120, 92, 66))
        n = np.random.default_rng(4).normal(0, 12, (H // 3, W // 3)).astype(np.float32)
        n = np.array(Image.fromarray(n).resize((W, H)))
        bg = Image.fromarray(np.clip(np.asarray(bg).astype(np.float32) + n[..., None], 0, 255).astype(np.uint8))
        spots = [(180, 140), (1080, 110), (240, 590), (1160, 560)]
        self.pins = []
        for i, sid in enumerate(ids[:4]):
            ph = load_img(sid, 620)
            ph = ph.crop((0, 0, 620, min(ph.height, 380)))
            fr = Image.new("RGBA", (660, 460), (240, 236, 226, 255)); fr.paste(ph, (20, 20))
            fr = fr.rotate(rng.uniform(-5, 5), expand=True, resample=Image.BICUBIC)
            x, y = spots[i]
            shadow_paste(bg, fr, x, y)
            px, py = x + fr.width // 2, y + 24
            self.pins.append((px, py))
        self.bg = bg
    def frame(self, t):
        im = self.bg.copy(); d = ImageDraw.Draw(im)
        order = [0, 3, 1, 2]
        segs = [(self.pins[order[k]], self.pins[order[k + 1]]) for k in range(3)]
        p = ease((t - 0.4) / (self.dur * 0.7)) * len(segs)
        for k, (a, b) in enumerate(segs):
            q = max(0.0, min(1.0, p - k))
            if q <= 0: continue
            ex = a[0] + (b[0] - a[0]) * q; ey = a[1] + (b[1] - a[1]) * q
            d.line((a[0], a[1], ex, ey), fill=CRIMSON, width=7)
        for (x, y) in self.pins:
            d.ellipse((x - 16, y - 16, x + 16, y + 16), fill=CRIMSON, outline=(60, 10, 10), width=3)
        return zoom_frame(im, t, self.dur, 1.0, 1.07)

# ---------------------------------------------------------------- count
class Count:
    def __init__(self, n, label, dur): self.n, self.label, self.dur = int(n), label, dur
    def frame(self, t):
        im = R.paper(); d = ImageDraw.Draw(im)
        v = int(round(self.n * ease(t / 1.6)))
        f = R.font(420); s = str(v); tw = d.textlength(s, font=f)
        d.text(((W - tw) / 2, 130), s, font=f, fill=CRIMSON)
        f2 = R.font(96); lw = d.textlength(self.label, font=f2)
        d.rectangle((W / 2 - 160, 720, W / 2 + 160, 730), fill=INK)
        d.text(((W - lw) / 2, 760), self.label, font=f2, fill=INK)
        return zoom_frame(im, t, self.dur, 1.0, 1.04)

# ---------------------------------------------------------------- stamp
class Stamp:
    def __init__(self, sid, text, dur):
        self.dur = dur; self.base = R.ImgShot(sid, dur, "in"); self.text = text
    def frame(self, t):
        im = self.base.frame(t)
        k = ease((t - 0.8) / 0.25)
        if k > 0:
            f = R.font(200); s = self.text
            tmp = ImageDraw.Draw(Image.new("RGB", (10, 10))); sw = int(tmp.textlength(s, font=f))
            st = Image.new("RGBA", (sw + 120, 300), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
            sd.rectangle((8, 8, sw + 112, 292), outline=CRIMSON + (255,), width=14)
            sd.text((60, 30), s, font=f, fill=CRIMSON + (255,))
            st = st.rotate(-8, expand=True, resample=Image.BICUBIC)
            sc = 1.3 - 0.3 * k
            st = st.resize((int(st.width * sc), int(st.height * sc)), Image.BICUBIC)
            st.putalpha(st.split()[3].point(lambda v: int(v * 0.9 * k)))
            im.paste(st, ((W - st.width) // 2, (H - st.height) // 2), st)
        return im

def make(spec, dur):
    parts = spec.split(":")
    k = parts[0]
    if k == "chess": return Chess(parts[1], parts[2], dur)
    if k == "map": return Map(parts[1], parts[2], dur)
    if k == "timeline": return Timeline(parts[1], dur)
    if k == "headline": return Headline(":".join(parts[1:]), dur)
    if k == "note": return Note(dur)
    if k == "ticket": return Ticket(dur)
    if k == "cctv": return Cctv(parts[1], parts[2], parts[3], parts[4], dur)
    if k == "board": return Board(parts[1].split(","), dur)
    if k == "count": return Count(parts[1], ":".join(parts[2:]), dur)
    if k == "stamp": return Stamp(parts[1], ":".join(parts[2:]), dur)
    raise ValueError(spec)

class AnimShot:
    def __init__(self, spec, dur):
        self.dur = dur; self.a = make(spec, dur)
    def frame(self, t): return self.a.frame(t)

# ---------------------------------------------------------------- lineup
class Lineup:
    """4 character cutouts in a row (left part of character plates), labels pop under each."""
    def __init__(self, ids, labels, dur):
        self.dur = dur; self.labels = labels
        self.cuts = []
        for sid in ids:
            im = load_img(sid)
            w, h = im.size
            c = im.crop((int(w * 0.04), int(h * 0.04), int(w * 0.42), int(h * 0.98)))
            c = c.resize((400, int(400 * c.height / c.width)), Image.LANCZOS)
            self.cuts.append(c)
    def frame(self, t):
        im = R.paper(); d = ImageDraw.Draw(im)
        n = len(self.cuts); gap = (W - n * 400) / (n + 1)
        for i, c in enumerate(self.cuts):
            k = ease((t - 0.25 * i) / 0.45)
            if k <= 0: continue
            x = gap + i * (400 + gap); y = int((H - c.height - 100) / 2) + int((1 - k) * 80)
            card = c.copy().convert("RGBA"); card.putalpha(int(255 * k))
            shadow_paste(im, card, x, y, blur=8, alpha=int(90 * k))
            kl = ease((t - 0.25 * i - 0.5) / 0.3)
            if kl > 0 and i < len(self.labels):
                f = R.font(58); s = self.labels[i]; sw = d.textlength(s, font=f)
                ly = y + c.height + 10
                d.rectangle((x + 200 - sw / 2 - 20, ly, x + 200 + sw / 2 + 20, ly + 84), fill=INK)
                d.text((x + 200 - sw / 2, ly + 2), s, font=f, fill=CREAM)
        return zoom_frame(im, t, self.dur, 1.0, 1.04)

# ---------------------------------------------------------------- myth -> fact
class Myth:
    def __init__(self, myth, fact, dur): self.myth, self.fact, self.dur = myth.upper(), fact.upper(), dur
    def frame(self, t):
        im = R.paper(); d = ImageDraw.Draw(im)
        f0, f1 = R.font(60), R.font(104)
        # myth card
        k = ease(t / 0.4)
        y = 190 + int((1 - k) * 40)
        d.text((W / 2 - d.textlength("МИФ", font=f0) / 2, y), "МИФ", font=f0, fill=GREY)
        mw = d.textlength(self.myth, font=f1)
        if mw > W - 200:
            f1 = R.font(int(104 * (W - 200) / mw)); mw = d.textlength(self.myth, font=f1)
        d.text((W / 2 - mw / 2, y + 80), self.myth, font=f1, fill=INK)
        s = ease((t - 0.9) / 0.4)
        if s > 0:
            d.line((W / 2 - mw / 2 - 20, y + 150, W / 2 - mw / 2 - 20 + (mw + 40) * s, y + 150), fill=CRIMSON, width=14)
        kf = ease((t - 1.5) / 0.4)
        if kf > 0:
            f2, f3 = R.font(60), R.font(110)
            fy = 600 + int((1 - kf) * 40)
            lab = "НА САМОМ ДЕЛЕ"
            d.text((W / 2 - d.textlength(lab, font=f2) / 2, fy), lab, font=f2, fill=CRIMSON)
            fw = d.textlength(self.fact, font=f3)
            if fw > W - 200:
                f3 = R.font(int(110 * (W - 200) / fw)); fw = d.textlength(self.fact, font=f3)
            d.rectangle((W / 2 - fw / 2 - 40, fy + 80, W / 2 + fw / 2 + 40, fy + 230), fill=CRIMSON)
            d.text((W / 2 - fw / 2, fy + 86), self.fact, font=f3, fill=CREAM)
        return zoom_frame(im, t, self.dur, 1.0, 1.03)

# ---------------------------------------------------------------- checklist
class Checklist:
    def __init__(self, title, items, dur): self.title, self.items, self.dur = title.upper(), [x.upper() for x in items], dur
    def frame(self, t):
        im = R.paper(); d = ImageDraw.Draw(im)
        f0, f1 = R.font(84), R.font(76)
        d.rectangle((240, 120, 256, 230), fill=CRIMSON)
        d.text((290, 120), self.title, font=f0, fill=INK)
        step = max(0.6, (self.dur * 0.7) / max(1, len(self.items)))
        for i, it in enumerate(self.items):
            k = ease((t - 0.5 - i * step) / 0.35)
            if k <= 0: continue
            y = 300 + i * 150
            x = 290 + int((1 - k) * 60)
            d.rectangle((x, y + 10, x + 80, y + 90), outline=INK, width=6)
            kk = ease((t - 0.8 - i * step) / 0.25)
            if kk > 0:
                d.line([(x + 14, y + 50), (x + 34, y + 76), (x + 34 + 60 * kk, y + 76 - 70 * kk)], fill=CRIMSON, width=12)
            d.text((x + 120, y), it, font=f1, fill=INK)
        return zoom_frame(im, t, self.dur, 1.0, 1.04, 0.3, 0.4)

# ---------------------------------------------------------------- dots 1 of 100
class Dots:
    def __init__(self, n, label, dur): self.n, self.label, self.dur = int(n), label.upper(), dur
    def frame(self, t):
        im = R.paper(); d = ImageDraw.Draw(im)
        cols, rows, r, g = 20, 5, 26, 78
        x0 = (W - (cols - 1) * g) / 2; y0 = 210
        k = ease(t / 1.2)
        shown = int(100 * k)
        rng = random.Random(7); red = set(rng.sample(range(100), self.n))
        for i in range(shown):
            cx = x0 + (i % cols) * g; cy = y0 + (i // cols) * g
            col = (150, 144, 134)
            if i in red and t > 1.5:
                col = CRIMSON
                pr = r + int(10 * max(0, math.sin((t - 1.5) * 4)))
                d.ellipse((cx - pr, cy - pr, cx + pr, cy + pr), fill=col); continue
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col)
        if t > 1.8:
            kk = ease((t - 1.8) / 0.4)
            f = R.font(84); sw = d.textlength(self.label, font=f)
            y = 680 + int(30 * (1 - kk))
            d.rectangle((W / 2 - sw / 2 - 40, y, W / 2 + sw / 2 + 40, y + 130), fill=INK)
            d.text((W / 2 - sw / 2, y + 12), self.label, font=f, fill=CREAM)
        return zoom_frame(im, t, self.dur, 1.0, 1.03)

# ---------------------------------------------------------------- archive portraits row
class Portraits:
    """4 tall archival portraits (waist-up) side by side, revealed one by one, label bar under each."""
    PW, PH, TOP = 423, 760, 70
    def __init__(self, ids, labels, dur):
        self.dur = dur; self.labels = labels; self.ph = []
        rot = [-1.2, 0.8, -0.6, 1.1]
        for i, sid in enumerate(ids):
            im = Image.open(f"{R.ROOT}/img/{sid}.png").convert("RGB")
            w, h = im.size
            ch = int(h * 0.93); cw = int(ch * self.PW / self.PH)
            if cw > w: cw = w; ch = int(cw * self.PH / self.PW)
            x0 = (w - cw) // 2
            big = im.crop((x0, 0, x0 + cw, ch)).resize((int(self.PW * 1.08), int(self.PH * 1.08)), Image.LANCZOS)
            self.ph.append((big, rot[i % 4]))
    def frame(self, t):
        im = R.paper(); d = ImageDraw.Draw(im)
        n = len(self.ph); gap = 36; side = (W - n * self.PW - (n - 1) * gap) / 2
        for i, (big, rot) in enumerate(self.ph):
            k = ease((t - 0.35 * i) / 0.5)
            if k <= 0: continue
            # crop window shrinks over time = push in, anchored near the face (upper third)
            sc = 1.0 + 0.07 * min(1.0, max(0.0, t - 0.35 * i) / max(self.dur, 1e-3))
            ww, hh = big.width / sc, big.height / sc
            x0 = (big.width - ww) / 2; y0 = (big.height - hh) * 0.25
            photo = big.resize((self.PW, self.PH), Image.BILINEAR, box=(x0, y0, x0 + ww, y0 + hh))
            card = Image.new("RGBA", (self.PW + 24, self.PH + 24), (246, 240, 226, 255))
            card.paste(photo, (12, 12))
            card = card.rotate(rot, expand=True, resample=Image.BICUBIC)
            card.putalpha(card.split()[3].point(lambda v: int(v * k)))
            x = side + i * (self.PW + gap) - 12; y = self.TOP + int((1 - k) * 90)
            shadow_paste(im, card, x, y, blur=10, alpha=int(110 * k))
            kl = ease((t - 0.35 * i - 0.6) / 0.3)
            if kl > 0 and i < len(self.labels):
                f = R.font(56); s = self.labels[i]; sw = d.textlength(s, font=f)
                cx = side + i * (self.PW + gap) + self.PW / 2
                ly = self.TOP + self.PH + 48 + int((1 - kl) * 20)
                d.rectangle((cx - sw / 2 - 22, ly, cx + sw / 2 + 22, ly + 82), fill=INK)
                d.text((cx - sw / 2, ly + 2), s, font=f, fill=CREAM)
        return zoom_frame(im, t, self.dur, 1.0, 1.03)

# ---------------------------------------------------------------- what the neighbours said
class Quotes:
    """Background picture (slow push-in, darkened) + quote slips popping in at given times (s)."""
    def __init__(self, sid, times, quotes, dur):
        self.dur = dur; self.times = times; self.quotes = quotes
        src = Image.open(f"{R.ROOT}/img/{sid}.png").convert("RGB")
        self.bg = src.resize((W, int(W * src.height / src.width)), Image.LANCZOS)
        self.dark = Image.new("RGB", (W, H), (18, 16, 14))
        self.slips = []
        rot = [-3.0, 2.2, -1.4]
        for i, q in enumerate(quotes):
            txt = "«" + q.upper() + "»"
            f = R.font(118 if len(txt) < 14 else 96)
            tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
            tw = int(tmp.textlength(txt, font=f))
            sl = Image.new("RGBA", (tw + 120, 220), (244, 238, 224, 255)); d = ImageDraw.Draw(sl)
            d.text((60, 22), txt, font=f, fill=INK)
            d.rectangle((60, 176, 60 + min(tw, 260), 184), fill=CRIMSON)
            d.text((60 + min(tw, 260) + 20, 160), "СОСЕДИ", font=R.font(40), fill=GREY)
            self.slips.append(sl.rotate(rot[i % 3], expand=True, resample=Image.BICUBIC))
        self.pos = [(100, 70), (1240, 110), (0, 370)]  # keep the bottom (people on the bench) clear
    def frame(self, t):
        z = 1.0 + 0.07 * (t / max(self.dur, 1e-3))
        cw, chh = W / z, H / z
        x0 = (W - cw) / 2; y0 = max(0.0, (self.bg.height - chh) / 2)
        im = self.bg.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + chh))
        first = self.times[0] if self.times else 0
        im = Image.blend(im, self.dark, 0.45 * ease((t - first + 0.4) / 0.5))
        for i, sl in enumerate(self.slips):
            if i >= len(self.times) or t < self.times[i]: continue
            k = pop((t - self.times[i]) / 0.35)
            s = sl.resize((max(1, int(sl.width * k)), max(1, int(sl.height * k))), Image.BICUBIC)
            x, y = self.pos[i % 3]
            if i == len(self.slips) - 1: x = (W - sl.width) // 2
            shadow_paste(im, s, x + (sl.width - s.width) / 2, y + (sl.height - s.height) / 2, blur=10, alpha=140)
        return im

_make_old = make
def make(spec, dur):
    parts = spec.split(":")
    k = parts[0]
    if k == "lineup": return Lineup(parts[1].split(","), parts[2].split("|"), dur)
    if k == "portraits": return Portraits(parts[1].split(","), parts[2].split("|"), dur)
    if k == "quotes": return Quotes(parts[1], [float(x) for x in parts[2].split(",")], ":".join(parts[3:]).split("|"), dur)
    if k == "myth":
        a, b = ":".join(parts[1:]).split("|", 1); return Myth(a, b, dur)
    if k == "list":
        xs = ":".join(parts[1:]).split("|"); return Checklist(xs[0], xs[1:], dur)
    if k == "dots": return Dots(parts[1], ":".join(parts[2:]), dur)
    return _make_old(spec, dur)
