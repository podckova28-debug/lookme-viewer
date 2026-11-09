"""Плашки («контейнеры») ролика — единая дизайн-система.
Токены: палитра 5 цветов, шрифты Oswald (заголовки) + Inter (подписи), поля 96 px, тайминги 0.15/0.25/0.4 с,
плавные кривые: выход easeOutCubic, вход в кадр — без «резиновых» подпрыгиваний (кроме удара штампа).
Каждый элемент рисуется в 2× и уменьшается (сглаженные края), статичные части кэшируются.
"""
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

W, H = 1920, 1080
MX, MY = 96, 72
INK = (27, 22, 18); CREAM = (255, 244, 222); RED = (204, 51, 40); OCHRE = (232, 168, 40); GREEN = (46, 140, 76)
COL = dict(green=GREEN, red=RED, ochre=OCHRE, ink=INK)
F = '/tmp/claude-0/-home-user-lookme-viewer/8420a68c-a72b-5ef9-9faf-653836f3526a/scratchpad/sovhacks/fonts/'
OSW_B, OSW_M = F + 'Oswald_wght_700.ttf', F + 'Oswald_wght_500.ttf'
INT_XB, INT_SB = '/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf', '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
FAST, NORMAL, SLOW = 0.15, 0.25, 0.4
CH_LABEL = 'ЧАСТЬ'
MUTED = (196, 184, 162); GREY = (120, 112, 100)
S = 2  # суперсэмплинг

_fc = {}
def font(path, size):
    k = (path, size)
    if k not in _fc: _fc[k] = ImageFont.truetype(path, size * S)
    return _fc[k]

def clamp(x): return max(0.0, min(1.0, x))
def out_cubic(x): x = clamp(x); return 1 - (1 - x) ** 3
def in_cubic(x): x = clamp(x); return x ** 3

def down(im):
    return im.resize((im.width // S, im.height // S), Image.LANCZOS)

def shadow(im, r=10, dy=8, a=110):
    pad = r * 3
    base = Image.new('RGBA', (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    sh = Image.new('RGBA', base.size, (0, 0, 0, 0))
    m = im.getchannel('A').point(lambda v: v * a // 255)
    sh.paste((0, 0, 0, 255), (pad, pad + dy), m)
    sh.putalpha(sh.getchannel('A').filter(ImageFilter.GaussianBlur(r)))
    base.alpha_composite(sh); base.alpha_composite(im, (pad, pad))
    return base, pad

def with_alpha(im, a):
    if a >= 0.999: return im
    im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * a))); return im

def tracked(d, xy, text, f, fill, track=0):
    """Текст с разрядкой (для мелких заголовков)."""
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill); x += d.textlength(ch, font=f) + track * S
    return x

_cache = {}
def cached(key, fn):
    if key not in _cache: _cache[key] = fn()
    return _cache[key]

# ---------------- 1. Заставка главы: красный блок с номером + кремовая полоса с названием ----------------
def _chapter_parts(num, title):
    fb = font(OSW_B, 118); fl = font(OSW_M, 30); ft = font(OSW_B, 62)
    bs = 176 * S
    block = Image.new('RGBA', (bs, bs), (0, 0, 0, 0)); d = ImageDraw.Draw(block)
    d.rounded_rectangle((0, 0, bs - 1, bs - 1), 18 * S, fill=RED + (255,))
    d.text((bs / 2, bs / 2 + 4 * S), str(num), font=fb, fill=CREAM, anchor='mm')
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    tw = tmp.textlength(title, font=ft); bw = int(tw + 64 * S); bh = 136 * S
    bar = Image.new('RGBA', (bw, bh), (0, 0, 0, 0)); d = ImageDraw.Draw(bar)
    d.rounded_rectangle((0, 0, bw - 1, bh - 1), 14 * S, fill=CREAM + (250,))
    tracked(d, (32 * S, 10 * S), CH_LABEL, fl, RED, track=4)
    d.text((32 * S, 92 * S), title, font=ft, fill=INK, anchor='lm')
    b, bp = shadow(down(block)); r, rp = shadow(down(bar))
    return b, bp, r, rp

def chapter(fr, t, dur, num, title):
    b, bp, r, rp = cached(('ch', num, title), lambda: _chapter_parts(num, title))
    k_in = out_cubic(t / SLOW); k_out = in_cubic((t - (dur - NORMAL)) / NORMAL)
    a = k_in * (1 - k_out); dy = -24 * k_out
    x0 = MX - 60 * (1 - k_in); y0 = MY + dy
    fr.alpha_composite(with_alpha(b, a), (int(x0 - bp), int(y0 - bp)))
    # полоса проявляется «шторкой» слева направо с задержкой
    kb = out_cubic((t - 0.1) / SLOW)
    if kb > 0:
        cw = int((r.width - 2 * rp) * kb) + rp
        part = r.crop((0, 0, cw + rp, r.height))
        fr.alpha_composite(with_alpha(part, (1 - k_out)), (int(x0 + 176 + 14 - rp), int(y0 + 20 - rp)))

# ---------------- 2. Маленький индикатор «3/10» на всю главу ----------------
def _chip(text):
    f = font(OSW_M, 38); tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    w = int(tmp.textlength(text, font=f) + 60 * S); h = 60 * S
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), h // 2, fill=INK + (215,))
    d.ellipse((16 * S, h / 2 - 7 * S, 30 * S, h / 2 + 7 * S), fill=RED)
    d.text((40 * S, h / 2), text, font=f, fill=CREAM, anchor='lm')
    return down(im)

def chip(fr, t, dur, text):
    im = cached(('chip', text), lambda: _chip(text))
    a = out_cubic(t / NORMAL) * (1 - in_cubic((t - (dur - NORMAL)) / NORMAL))
    fr.alpha_composite(with_alpha(im, a * 0.95), (MX, MY))

# ---------------- 3. Подпись-факт внизу слева ----------------
def _caption(text):
    f = font(INT_XB, 44); tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    words = text.split(); lines = []; cur = ''
    for w_ in words:
        test = (cur + ' ' + w_).strip()
        if tmp.textlength(test, font=f) > 1420 * S and cur: lines.append(cur); cur = w_
        else: cur = test
    lines.append(cur)
    lh = 56 * S; tw = max(tmp.textlength(l, font=f) for l in lines)
    w = int(tw + 40 * S + 34 * S); h = int(lh * len(lines) + 36 * S)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 12 * S, fill=INK + (222,))
    d.rounded_rectangle((0, 0, 10 * S, h - 1), 5 * S, fill=RED)
    for i, l in enumerate(lines):
        d.text((34 * S, 18 * S + i * lh + lh / 2), l, font=f, fill=CREAM, anchor='lm')
    return shadow(down(im), r=8, dy=6, a=90)

def caption(fr, t, dur, text):
    im, p = cached(('cap', text), lambda: _caption(text))
    k = out_cubic(t / NORMAL); ko = in_cubic((t - (dur - 0.2)) / 0.2)
    y = H - MY - (im.height - 2 * p) + 16 * (1 - k)
    fr.alpha_composite(with_alpha(im, k * (1 - ko)), (int(MX - p), int(y - p)))

# ---------------- 4. Штамп вердикта ----------------
def _stamp(text, sub, color):
    fb = font(OSW_B, 120 if len(text) <= 9 else 98); fs = font(OSW_B, 44)
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    tw = max(tmp.textlength(text, font=fb), tmp.textlength(sub or '', font=fs))
    w = int(tw + 120 * S); h = int((240 if sub else 160) * S)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    c = color + (255,)
    d.rounded_rectangle((6 * S, 6 * S, w - 6 * S, h - 6 * S), 22 * S, fill=CREAM + (225,))
    d.rounded_rectangle((6 * S, 6 * S, w - 6 * S, h - 6 * S), 22 * S, outline=c, width=10 * S)
    d.rounded_rectangle((24 * S, 24 * S, w - 24 * S, h - 24 * S), 12 * S, outline=c, width=4 * S)
    d.text((w / 2, (96 if sub else h / S / 2 + 2) * S), text, font=fb, fill=c, anchor='mm')
    if sub: d.text((w / 2, 180 * S), sub, font=fs, fill=c, anchor='mm')
    # фактура резинового штампа: выщербины в краске
    rnd = random.Random(hash(text) & 0xffff)
    mask = Image.new('L', im.size, 255); md = ImageDraw.Draw(mask)
    for _ in range(int(w * h / (S * S) / 2200)):
        x, y = rnd.randrange(w), rnd.randrange(h); r = rnd.choice((2, 3, 4)) * S
        md.ellipse((x - r, y - r, x + r, y + r), fill=rnd.randrange(90, 200))
    mask = mask.filter(ImageFilter.GaussianBlur(1.2 * S))
    im.putalpha(ImageChops.multiply(im.getchannel('A'), mask))
    im = down(im).rotate(7, resample=Image.BICUBIC, expand=True)
    return im

def stamp(fr, t, dur, text, sub=None, color='green', x=1560, y=270):
    im = cached(('st', text, sub, color), lambda: _stamp(text, sub, COL[color]))
    hit = FAST  # удар
    if t < hit:
        k = clamp(t / hit); sc = 1.55 - 0.55 * (k ** 2); a = k
        jx = jy = 0
    else:
        sc = 1.0; a = 1.0; q = t - hit
        amp = 7 * max(0.0, 1 - q / 0.14); jx = amp * math.sin(q * 90); jy = amp * 0.5 * math.cos(q * 70)
    a *= (1 - in_cubic((t - (dur - NORMAL)) / NORMAL)) * 0.93
    if a <= 0.01: return
    imr = im if abs(sc - 1) < 0.01 else im.resize((int(im.width * sc), int(im.height * sc)), Image.BICUBIC)
    fr.alpha_composite(with_alpha(imr, a), (int(x - imr.width / 2 + jx), int(y - imr.height / 2 + jy)))

# ---------------- 5. Затемнение фона под крупные заголовки ----------------
def dim(fr, t, dur, amount=0.5):
    a = out_cubic(t / NORMAL) * (1 - in_cubic((t - (dur - NORMAL)) / NORMAL)) * amount
    if a > 0.01: fr.alpha_composite(Image.new('RGBA', fr.size, (14, 10, 8, int(255 * a))))

# ---------------- 6. Заголовок вступления (строки появляются по очереди) ----------------
def _title_lines(lines):
    out = []
    for text, size, color in lines:
        f = font(OSW_B, size); tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
        tw = tmp.textlength(text, font=f); w = int(tw + 40 * S); h = int(size * 1.35 * S)
        im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.text((w / 2, h / 2), text, font=f, fill=color, anchor='mm', stroke_width=5 * S, stroke_fill=INK)
        out.append(shadow(down(im), r=12, dy=8, a=120))
    return out

def title(fr, t, dur, lines, y=430, gap=12):
    parts = cached(('ti', tuple(lines)), lambda: _title_lines(lines))
    dim(fr, t, dur, 0.42)
    yy = y; ko = in_cubic((t - (dur - NORMAL)) / NORMAL)
    for i, (im, p) in enumerate(parts):
        k = out_cubic((t - 0.12 * i) / SLOW)
        hh = im.height - 2 * p
        fr.alpha_composite(with_alpha(im, k * (1 - ko)), (int(W / 2 - im.width / 2), int(yy - p + 30 * (1 - k))))
        yy += hh + gap
    # красная линия под заголовком растёт из центра
    kl = out_cubic((t - 0.12 * len(parts)) / SLOW) * (1 - ko)
    if kl > 0:
        lw = int(420 * kl); d = ImageDraw.Draw(fr)
        d.rounded_rectangle((W / 2 - lw / 2, yy + 6, W / 2 + lw / 2, yy + 16), 5, fill=RED + (int(255 * (1 - ko)),))

# ---------------- 7. Итоговая таблица ----------------
BADGE = {'РАБОТАЕТ': GREEN, 'МИФ': RED, 'ОПАСНО': RED, 'СТАРЫЕ МАШИНЫ': OCHRE, 'НА ТРОЕЧКУ': OCHRE,
         'ДО 60 000 ₽': RED, 'ДО 20 000 ₽': RED, 'РЕМОНТ КОРОБКИ': RED, 'ОТ 12 000 ₽': RED, 'ЗАГЛОХНЕШЬ': OCHRE,
         'ПРОМЫТЬ БАК': GREEN, 'НЕ СТРАШНО': GREEN, 'БЕЗОПАСНО': GREEN, 'ЗАВИСИТ': OCHRE}
def _score_rows(rows):
    fn = font(OSW_M, 36); ft = font(INT_SB, 36); fb = font(OSW_M, 28)
    out = []
    for i, (name, verdict) in enumerate(rows, 1):
        w, h = 1180 * S, 62 * S
        im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.text((10 * S, h / 2), f'{i:>2}', font=fn, fill=OCHRE, anchor='lm')
        d.text((80 * S, h / 2), name, font=ft, fill=CREAM, anchor='lm')
        bw = int(d.textlength(verdict, font=fb) + 40 * S); c = BADGE.get(verdict, OCHRE)
        d.rounded_rectangle((w - bw - 6 * S, 10 * S, w - 6 * S, h - 10 * S), 21 * S, fill=c)
        d.text((w - bw / 2 - 6 * S, h / 2 + 1 * S), verdict, font=fb, fill=CREAM, anchor='mm')
        out.append(down(im))
    pw, ph = 1260, 62 * len(rows) + 150
    panel = Image.new('RGBA', (pw * S, ph * S), (0, 0, 0, 0)); d = ImageDraw.Draw(panel)
    d.rounded_rectangle((0, 0, pw * S - 1, ph * S - 1), 26 * S, fill=INK + (232,))
    d.text((pw * S / 2, 58 * S), 'ИТОГО', font=font(OSW_B, 56), fill=CREAM, anchor='mm')
    d.rounded_rectangle((pw * S / 2 - 60 * S, 96 * S, pw * S / 2 + 60 * S, 104 * S), 4 * S, fill=RED)
    return out, shadow(down(panel), r=14, dy=10, a=120)

def score(fr, t, dur, rows):
    rims, (panel, p) = cached(('sc', tuple(rows)), lambda: _score_rows(rows))
    dim(fr, t, dur, 0.5)
    ko = in_cubic((t - (dur - NORMAL)) / NORMAL); kp = out_cubic(t / SLOW)
    px = W / 2 - panel.width / 2; py = (H - (panel.height - 2 * p)) / 2 - p
    fr.alpha_composite(with_alpha(panel, kp * (1 - ko)), (int(px), int(py + 20 * (1 - kp))))
    for i, im in enumerate(rims):
        k = out_cubic((t - 0.3 - 0.12 * i) / NORMAL)
        if k <= 0: continue
        fr.alpha_composite(with_alpha(im, k * (1 - ko)), (int(W / 2 - im.width / 2 + 24 * (1 - k)), int(py + p + 128 + i * 62)))

# ---------------- 8. Графики: столбики и доли ----------------
def _panel(w, h, title, source):
    pn = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(pn)
    d.rounded_rectangle((0, 0, w * S - 1, h * S - 1), 26 * S, fill=INK + (236,))
    d.text((56 * S, 64 * S), title, font=font(OSW_B, 54), fill=CREAM, anchor='lm')
    d.rounded_rectangle((56 * S, 104 * S, 176 * S, 112 * S), 4 * S, fill=RED)
    if source: d.text((56 * S, (h - 40) * S), source, font=font(INT_SB, 24), fill=MUTED, anchor='lm')
    return shadow(down(pn), r=14, dy=10, a=120)

def _bars_static(title, rows, source, vmax):
    w = 1500; h = 190 + 118 * len(rows) + 60
    panel = _panel(w, h, title, source)
    labs = []
    for name, v, txt, col in rows:
        im = Image.new('RGBA', (w * S, 40 * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.text((0, 20 * S), name, font=font(INT_SB, 34), fill=CREAM, anchor='lm')
        labs.append(down(im))
    vals = []
    for name, v, txt, col in rows:
        f = font(OSW_B, 46); tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
        tw = int(tmp.textlength(txt, font=f) + 20 * S)
        im = Image.new('RGBA', (tw, 70 * S), (0, 0, 0, 0)); ImageDraw.Draw(im).text((0, 35 * S), txt, font=f, fill=CREAM, anchor='lm')
        vals.append(down(im))
    return panel, labs, vals, w, h

def bars(fr, t, dur, title, rows, source='', vmax=None):
    vmax = vmax or max(r[1] for r in rows)
    (panel, p), labs, vals, w, h = cached(('bars', title, tuple(rows), source), lambda: _bars_static(title, rows, source, vmax))
    dim(fr, t, dur, 0.55)
    ko = in_cubic((t - (dur - NORMAL)) / NORMAL); kp = out_cubic(t / SLOW)
    px = W / 2 - w / 2; py = (H - h) / 2
    fr.alpha_composite(with_alpha(panel, kp * (1 - ko)), (int(px - p), int(py - p + 20 * (1 - kp))))
    lay = Image.new('RGBA', fr.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); track = w - 112 - 330; texts = []
    for i, (name, v, txt, col) in enumerate(rows):
        y = py + 160 + i * 118
        a = out_cubic((t - 0.25 - 0.18 * i) / NORMAL) * (1 - ko)
        if a <= 0: continue
        fr.alpha_composite(with_alpha(labs[i], a), (int(px + 56), int(y - 4)))
        k = out_cubic((t - 0.4 - 0.25 * i) / 0.9)
        x0 = px + 56; yb = y + 44; bw = max(8, track * v / vmax * k)
        d.rounded_rectangle((x0, yb, x0 + track, yb + 40), 8, fill=(255, 244, 222, int(30 * a)))
        d.rounded_rectangle((x0, yb, x0 + bw, yb + 40), 8, fill=COL.get(col, col) + (int(255 * a),) if isinstance(col, str) else col + (int(255 * a),))
        texts.append((with_alpha(vals[i], a * clamp(k * 1.5)), (int(x0 + track + 28), int(yb + 20 - vals[i].height / 2))))
    fr.alpha_composite(lay)
    for im, xy in texts: fr.alpha_composite(im, xy)

def _stack_static(title, segs, source, brace):
    w = 1640; h = 560
    panel = _panel(w, h, title, source)
    return panel, w, h

def stack(fr, t, dur, title, segs, source='', brace=None):
    """segs: [(доля %, подпись, цвет)]; brace: (сколько первых сегментов, текст)."""
    (panel, p), w, h = cached(('stack', title, tuple(segs), source), lambda: _stack_static(title, segs, source, brace))
    dim(fr, t, dur, 0.55)
    ko = in_cubic((t - (dur - NORMAL)) / NORMAL); kp = out_cubic(t / SLOW)
    px = W / 2 - w / 2; py = (H - h) / 2
    fr.alpha_composite(with_alpha(panel, kp * (1 - ko)), (int(px - p), int(py - p + 20 * (1 - kp))))
    lay = Image.new('RGBA', fr.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); x0 = px + 56; tot = w - 112; yb = py + 250; bh = 92
    tot_v = sum(s[0] for s in segs); x = x0
    fv = ImageFont.truetype(OSW_B, 44); fl = ImageFont.truetype(INT_SB, 24)
    for i, (v, lab, col) in enumerate(segs):
        k = out_cubic((t - 0.3 - 0.22 * i) / NORMAL) * (1 - ko)
        sw = tot * v / tot_v
        if k > 0:
            c = COL.get(col, col) if isinstance(col, str) else col
            d.rounded_rectangle((x + 1, yb, x + 1 + (sw - 2) * k, yb + bh), 8, fill=c + (int(255 * (1 - ko)),))
            if sw > 120:
                txt = f'{v:.1f}%'.replace('.', ',')
                d.text((x + sw / 2, yb + bh + 46), txt, font=fv, fill=CREAM + (int(255 * k),), anchor='mm')
                for j, ln in enumerate(lab.split('\n')):
                    d.text((x + sw / 2, yb + bh + 92 + j * 30), ln, font=fl, fill=MUTED + (int(255 * k),), anchor='mm')
        x += sw
    if brace:
        n, txt = brace; kb = out_cubic((t - 0.4 - 0.22 * len(segs)) / SLOW) * (1 - ko)
        if kb > 0:
            bw = tot * sum(s[0] for s in segs[:n]) / tot_v
            yy = yb - 26; a = int(255 * kb)
            d.line((x0 + 4, yy + 14, x0 + 4, yy, x0 + bw - 4, yy, x0 + bw - 4, yy + 14), fill=OCHRE + (a,), width=6)
            d.text((x0 + bw / 2, yy - 38), txt, font=ImageFont.truetype(OSW_B, 48), fill=OCHRE + (a,), anchor='mm')
    fr.alpha_composite(lay)

def draw(fr, ov, t, dur):
    k = ov['type']
    if k == 'chapter': chapter(fr, t, dur, ov['num'], ov['title'])
    elif k == 'chip': chip(fr, t, dur, ov['text'])
    elif k == 'caption': caption(fr, t, dur, ov['text'])
    elif k == 'stamp': stamp(fr, t, dur, ov['text'], ov.get('sub'), ov.get('color', 'green'), ov.get('x', 1560), ov.get('y', 270))
    elif k == 'title': title(fr, t, dur, ov['lines'], ov.get('y', 430))
    elif k == 'score': score(fr, t, dur, ov['rows'])
    elif k == 'bars': bars(fr, t, dur, ov['title'], ov['rows'], ov.get('source', ''), ov.get('vmax'))
    elif k == 'stack': stack(fr, t, dur, ov['title'], ov['segs'], ov.get('source', ''), ov.get('brace'))
