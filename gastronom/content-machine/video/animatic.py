#!/usr/bin/env python3
"""Монтаж вертикального ролика v2: покадровый рендер (PIL) → ffmpeg.

    python animatic.py episodes/<эпизод>/timeline.json

Таймлайн состоит из «битов»: бит = одна реплика голоса (или пауза) и 1–N кадров,
которые делят её время по весам. Кадр — картинка (движение камеры рисуется здесь:
наезд, отъезд, панорама, тряска) или клип анимации (играет в родной скорости, без
растягивания и заморозки). Текст на экране — не субтитры, а полезный слой:
хук-заголовок, плашки с фактами, чек-лист, концовка.
Звук: голос + музыка с приглушением под голос + звуки, громкость -14 LUFS."""
import json, math, os, re, subprocess, sys, wave
import numpy as np
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FF = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS, SR = 1080, 1920, 30, 44100
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, 'fonts')
BROWN, ORANGE, CREAM, GREEN, DARK = (138, 90, 46), (224, 112, 15), (243, 230, 203), (47, 125, 67), (43, 33, 24)

def font(name, size): return ImageFont.truetype(os.path.join(FONTS, name), size)

def ff(args, **kw):
    r = subprocess.run([FF, '-hide_banner', '-loglevel', 'error', '-y', *args], capture_output=True, **kw)
    if r.returncode: sys.exit(r.stderr.decode() if isinstance(r.stderr, bytes) else r.stderr)
    return r

# ---------- звук ----------
def read_audio(path, tempo=1.0, trim=True):
    af = []
    if trim: af.append('silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse')
    if tempo != 1.0: af.append(f'atempo={tempo}')
    raw = subprocess.run([FF, '-hide_banner', '-loglevel', 'error', '-i', path, *(['-af', ','.join(af)] if af else []),
                          '-f', 's16le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768

def write_wav(path, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

def place(track, x, t, gain=1.0):
    s = int(t * SR); e = min(len(track), s + len(x))
    if e > s: track[s:e] += x[:e - s] * gain

# ---------- картинка ----------
def ease(t): return 0.5 - 0.5 * math.cos(math.pi * min(max(t, 0), 1))
def back(t):  # появление с лёгким перелётом
    t = min(max(t, 0), 1); c = 1.9
    return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2

class Still:
    """Картинка + движение камеры. move: in / out / up / down / left / right / hold / punch."""
    def __init__(self, path, move='in', focus=(0.5, 0.5), amount=0.08):
        im = Image.open(path).convert('RGB')
        s = max(W / im.width, H / im.height) * (1 + amount + 0.06)
        self.im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        self.base = max(W / self.im.width, H / self.im.height)  # доля картинки в кадре при zoom=1
        self.move, self.focus, self.amount = move, focus, amount

    def frame(self, p):
        a, fx, fy = self.amount, *self.focus
        z0, z1, c0, c1 = 1.0, 1.0, (fx, fy), (fx, fy)
        if self.move == 'in': z1 = 1 + a
        elif self.move == 'out': z0 = 1 + a
        elif self.move == 'punch': z0 = z1 = 1 + a
        elif self.move in ('up', 'down', 'left', 'right'):
            z0 = z1 = 1 + a * 0.6
            d = {'up': (0, 1), 'down': (0, -1), 'left': (1, 0), 'right': (-1, 0)}[self.move]
            c0 = (fx + d[0] * 0.04, fy + d[1] * 0.04); c1 = (fx - d[0] * 0.04, fy - d[1] * 0.04)
        e = ease(p); z = z0 + (z1 - z0) * e
        cx = c0[0] + (c1[0] - c0[0]) * e; cy = c0[1] + (c1[1] - c0[1]) * e
        cw, ch = self.im.width * self.base / z, self.im.height * self.base / z
        x = min(max(cx * self.im.width - cw / 2, 0), self.im.width - cw)
        y = min(max(cy * self.im.height - ch / 2, 0), self.im.height - ch)
        return self.im.resize((W, H), Image.BILINEAR, box=(x, y, x + cw, y + ch))

class Clip:
    """Клип анимации: кадры 30 fps, 1080×1920 (cover), с отступом ss. Не растягивается.
    to — взять только начало клипа (до «поплывшей» части); pingpong — проиграть его
    туда-обратно, чтобы хватило на длину кадра без заморозки. zoom > 1 — наезд: кадр крупнее,
    focus (x, y в долях) — куда смотрит камера; так из одного клипа получаются два шота."""
    def __init__(self, path, ss=0.0, speed=1.0, to=None, pingpong=False, zoom=1.0, focus=(0.5, 0.5), need=None):
        zw, zh = int(round(W * zoom / 2)) * 2, int(round(H * zoom / 2)) * 2
        crop = f'crop={W}:{H}:(iw-{W})*{focus[0]}:(ih-{H})*{focus[1]}'
        # читать из файла только нужный кусок: 9 клипов целиком в памяти — это 8+ ГБ и OOM (эп. 26)
        lim = [x for x in ((to * speed) if to else None, (need * speed + 0.3) if need and not pingpong else None) if x]
        tin = ['-t', f'{min(lim):.3f}'] if lim else []
        raw = subprocess.run([FF, '-hide_banner', '-loglevel', 'error', '-ss', str(ss), *tin, '-i', path, '-vf',
                              f'setpts=PTS/{speed},fps={FPS},scale={zw}:{zh}:force_original_aspect_ratio=increase:flags=lanczos,{crop}',
                              '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
        self.frames = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
        if to: self.frames = self.frames[:int(to * FPS)]
        if pingpong: self.frames = np.concatenate([self.frames, self.frames[-2::-1]])
    def frame_at(self, t):
        return Image.fromarray(self.frames[min(int(t * FPS), len(self.frames) - 1)])

# ---------- текст ----------
def wrap(d, txt, f, maxw):
    lines, cur = [], ''
    for w in txt.split():
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) > maxw and cur: lines.append(cur); cur = w
        else: cur = t
    lines.append(cur)
    if len(lines) == 2:  # ровные строки, без «висячего» слова
        words = txt.split(); best = None
        for i in range(1, len(words)):
            a, b = ' '.join(words[:i]), ' '.join(words[i:])
            m = max(d.textlength(a, font=f), d.textlength(b, font=f))
            if m <= maxw and (best is None or m < best[0]): best = (m, [a, b])
        if best: lines = best[1]
    return lines

_cache = {}
def title_img(txt, size=84, plate=False, color=None, box=None):
    """Крупный заголовок (хук). По умолчанию белый с тёмной обводкой и мягкой тенью;
    plate=True — тот же текст цветом на кремовой плашке ширины BOX_W, как у стикеров:
    читается на любом фоне (полки, посуда за спиной) и не спорит с остальными плашками."""
    key = ('title', txt, size, plate, color, box)
    bw = box or BOX_W  # ширина плашки; хук на обложке можно сделать шире ("box": 1000)
    if key in _cache: return _cache[key]
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    if plate:
        f = font('Nunito-Black.ttf', size)
        lines = txt.split('\n') if '\n' in txt else wrap(tmp, txt, f, bw - 80)
        f = _fit(tmp, max(lines, key=lambda ln: tmp.textlength(ln, font=f)), 'Nunito-Black.ttf', size, bw - 80)
        lh = int(f.size * 1.14); img, d = _box(bw, 44 + lh * len(lines))
        # строки — по общей линии шрифта ('ma'), а не по верху своих букв ('mt'): иначе строка из одних
        # строчных («самая дорогая») подпрыгивает, а строка с «?» («монета?») проседает
        cap = f.getbbox('Н', anchor='la')[1]
        for i, ln in enumerate(lines):
            d.text((20 + bw / 2, 20 + 22 - cap + i * lh), ln, font=f, fill=color or DARK, anchor='ma')
        _cache[key] = img
        return img
    f = font('Nunito-Black.ttf', size)
    lines = txt.split('\n') if '\n' in txt else wrap(tmp, txt, f, 940); lh = int(size * 1.14)
    img = Image.new('RGBA', (W, lh * len(lines) + 60), (0, 0, 0, 0)); sh = img.copy()
    d, ds = ImageDraw.Draw(img), ImageDraw.Draw(sh)
    for i, ln in enumerate(lines):
        x = (W - d.textlength(ln, font=f)) / 2; y = 20 + i * lh
        ds.text((x, y + 6), ln, font=f, fill=(0, 0, 0, 160), stroke_width=6, stroke_fill=(0, 0, 0, 160))
        d.text((x, y), ln, font=f, fill='white', stroke_width=5, stroke_fill=DARK)
    _cache[key] = Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)), img)
    return _cache[key]

# Все плашки и карточки одной ширины и по центру — текст стоит ровно от сцены к сцене.
BOX_W = 820
# Безопасная зона по вертикали: ниже ~1350 px в TikTok/Shorts лежат подпись и кнопки.
SAFE_Y = (230, 1350)

def _fit(d, txt, name, size, maxw, min_size=40):
    """Крупный шрифт, который помещается в ширину (без переноса)."""
    while size > min_size and d.textlength(txt, font=font(name, size)) > maxw: size -= 2
    return font(name, size)

def _box(pw, ph, radius=38):
    img = Image.new('RGBA', (pw + 40, ph + 40), (0, 0, 0, 0))
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((20, 28, 20 + pw, 28 + ph), radius, fill=(0, 0, 0, 90))
    img = Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)), img); d = ImageDraw.Draw(img)
    d.rounded_rectangle((20, 20, 20 + pw, 20 + ph), radius, fill=(255, 250, 240, 250), outline=DARK, width=5)
    return img, d

def sticker_img(big, small=None, color=ORANGE):
    """Плашка-факт фиксированной ширины: крупное значение цветом + подпись."""
    key = ('st', big, small, color)
    if key in _cache: return _cache[key]
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    fb = _fit(tmp, big, 'Nunito-Black.ttf', 88, BOX_W - 80)
    fs = font('Nunito-800.ttf', 44)
    sl = wrap(tmp, small, fs, BOX_W - 90) if small else []
    bh = fb.size + 14
    ph = 26 + bh + (len(sl) * 54 + 8 if sl else 0) + 22
    img, d = _box(BOX_W, ph)
    d.text((20 + BOX_W / 2, 20 + 26), big, font=fb, fill=color, anchor='mt')
    for i, t in enumerate(sl):
        d.text((20 + BOX_W / 2, 20 + 26 + bh + 8 + i * 54), t, font=fs, fill=DARK, anchor='mt')
    _cache[key] = img
    return img

# ---------- субтитры по словам, ценник, пузырь (Копейкин, эп. 3: «подписи нужны, но не в таком формате») ----------
SUB_YELLOW, SUB_RED = (255, 208, 40), (226, 58, 44)

def _stroke_text(img, xy, text, f, fill, sw=9, anchor='ls'):
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((xy[0], xy[1] + 7), text, font=f, fill=(0, 0, 0, 150), stroke_width=sw,
                            stroke_fill=(0, 0, 0, 150), anchor=anchor)
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)))
    ImageDraw.Draw(img).text(xy, text, font=f, fill=fill, stroke_width=sw, stroke_fill=DARK, anchor=anchor)

def subs_img(lines, size=104, maxw=940):
    """Кусок субтитров: lines = [[(слово, цвет, масштаб), …], …]; каждая строка по центру, сжимается в ширину."""
    key = ('sub', json.dumps(lines), size)
    if key in _cache: return _cache[key]
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1))); lh = int(size * 1.15)
    wrapped = []
    for words in lines:
        fs = [font('Nunito-Black.ttf', int(size * sc)) for _, _, sc in words]
        tot = sum(tmp.textlength(w, font=f) for (w, _, _), f in zip(words, fs)) + size * 0.28 * (len(words) - 1) + 18
        if tot > maxw and len(words) > 1:
            k = (len(words) + 1) // 2; wrapped += [words[:k], words[k:]]
        else: wrapped.append(words)
    lines = wrapped
    img = Image.new('RGBA', (W, lh * len(lines) + 60), (0, 0, 0, 0))
    for li, words in enumerate(lines):
        s0 = size
        while True:
            fs = [font('Nunito-Black.ttf', int(s0 * sc)) for _, _, sc in words]; gap = s0 * 0.28
            ws = [tmp.textlength(w, font=f) for (w, _, _), f in zip(words, fs)]
            tot = sum(ws) + gap * (len(words) - 1) + 18
            if tot <= maxw or s0 <= 64: break
            s0 -= 4
        x = (W - tot) / 2 + 9; y = 30 + int(s0 * 0.95) + li * lh
        for (w, c, _), f, wd in zip(words, fs, ws):
            _stroke_text(img, (x, y), w, f, tuple(c)); x += wd + gap
    _cache[key] = img.crop(img.getbbox() or (0, 0, 1, 1)) if img.getbbox() else img
    return _cache[key]

def subs_chunks(words, keys, t_lead, t_from, t_end):
    """Слова → куски по 1–2 слова (до 13 букв, предлоги прилипают к следующему); ключевое слово цветом и крупнее, отдельной строкой.
    Возвращает [(начало, конец, lines)] в секундах от начала бита."""
    clean = lambda w: w.strip('.,!?;:«»"()…—–-').strip()
    # конец предложения: кусок на нём обрывается («Второе.» и «Первый» — в разные куски)
    # 5-е поле — слово стоит перед запятой/точкой: короткое слово («20,», «90.») к следующему не прилипает,
    # и кусок на нём обрывается («МИНУС 20» | «В ЧАЙНИКЕ»), а не «20 В ЧАЙНИКЕ»
    items = [(clean(w), s + t_lead, e + t_lead, w.rstrip('»"').endswith(('.', '!', '?', '…')),
              w.rstrip('»"').endswith((',', ';', ':', '.', '!', '?', '…', '—')))
             for w, s, e in words if clean(w) and s + t_lead >= t_from - 0.05]
    units, buf = [], []  # короткое слово прилипает к следующему: «в стружку», «на полоски»
    for it in items:
        buf.append(it)
        if len(it[0]) > 2 or it[0].lower() in keys or it[4]: units.append(buf); buf = []
    if buf: units.append(buf)
    chunks, cur = [], []
    def flush():
        if cur: chunks.append([w for u in cur for w in u]); cur.clear()
    letters = lambda us: sum(len(w[0]) for u in us for w in u)
    for u in units:
        if any(w[0].lower() in keys for w in u):
            if cur and letters(cur) + letters([u]) > 16: flush()
            cur.append(u); flush(); continue
        tail = letters([u]) <= 3 and u[-1][4] and letters(cur) + letters([u]) <= 16  # «20,» дописывается к «МИНУС»
        if cur and (len(cur) >= 2 or letters(cur) + letters([u]) > 13) and not tail: flush()
        cur.append(u)
        if u[-1][3] or u[-1][4]: flush()
    flush()
    out = []
    for i, ch in enumerate(chunks):
        st = ch[0][1]; en = chunks[i + 1][0][1] if i + 1 < len(chunks) else min(ch[-1][2] + 0.35, t_end)
        plain = [(w.upper(), WHITE_T, 1.0) for w, *_ in ch if w.lower() not in keys]
        hot = [(w.upper(), keys[w.lower()], 1.2) for w, *_ in ch if w.lower() in keys]
        lines = [l for l in (plain, hot) if l]
        out.append((st, en, lines))
    return out
WHITE_T = (255, 255, 255)

def _tag_img(text, angle, size, color):
    """Сам ценник (повёрнутый) и его полуразмеры без поворота — от его края начинается стрелка."""
    key = ('tagimg', text, angle, size, color)
    if key in _cache: return _cache[key]
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1))); f = font('Nunito-Black.ttf', size)
    tw = tmp.textlength(text, font=f); pw, ph = int(tw + 110), int(size * 1.55)
    t = Image.new('RGBA', (pw + 40, ph + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    d.rounded_rectangle((20, 20, 20 + pw, 20 + ph), 28, fill=tuple(color) + (255,), outline=DARK, width=7)
    d.ellipse((38, 20 + ph / 2 - 13, 64, 20 + ph / 2 + 13), fill=(255, 255, 255, 255), outline=DARK, width=5)
    d.text((20 + pw / 2 + 20, 20 + ph / 2), text, font=f, fill=DARK, anchor='mm')
    _cache[key] = (t.rotate(angle, expand=True, resample=Image.BICUBIC), (pw + 14) / 2, (ph + 14) / 2)
    return _cache[key]

_warned = set()
def tag_layer(text, at, target, angle=-6, size=74, color=SUB_YELLOW, cache=True):
    """Жёлтый ценник со стрелкой к предмету — слой во весь кадр. Стрелка идёт от края ценника
    к target; если предмет движется, target меняется каждый кадр (cache=False)."""
    key = ('tag', text, tuple(at), tuple(target), angle, size, color)
    if cache and key in _cache: return _cache[key]
    t, hw, hh = _tag_img(text, angle, size, color)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    (sx, sy), (tx, ty) = at, target
    dx, dy = tx - sx, ty - sy; dist = math.hypot(dx, dy) or 1
    k = min(hw / abs(dx) if dx else 1e9, hh / abs(dy) if dy else 1e9)  # выход луча из прямоугольника ценника
    ex, ey = sx + dx * k, sy + dy * k
    gap = 14; ux, uy = dx / dist, dy / dist; tx2, ty2 = tx - ux * gap, ty - uy * gap
    vis = math.hypot(tx2 - ex, ty2 - ey)
    if (k >= 1 or vis < 80) and text not in _warned:
        _warned.add(text); print(f'⚠ ценник «{text}»: стрелка {vis:.0f} px — ценник лежит на предмете, отодвинь его')
    d.line((ex, ey, tx2, ty2), fill=DARK, width=20); d.line((ex, ey, tx2, ty2), fill=(255, 255, 255), width=10)
    a = math.atan2(dy, dx); L = 54
    d.polygon([(tx2, ty2), (tx2 - L * math.cos(a - 0.45), ty2 - L * math.sin(a - 0.45)),
               (tx2 - L * math.cos(a + 0.45), ty2 - L * math.sin(a + 0.45))], fill=(255, 255, 255), outline=DARK, width=6)
    lay.alpha_composite(t, (int(sx - t.width / 2), int(sy - t.height / 2)))
    if cache: _cache[key] = lay
    return lay

def track_at(track, t):
    """Точка предмета в момент t (секунды бита) по треку [[t, x, y], …] из track.py."""
    if t <= track[0][0]: return track[0][1:]
    for (t1, x1, y1), (t2, x2, y2) in zip(track, track[1:]):
        if t <= t2:
            k = (t - t1) / ((t2 - t1) or 1)
            return (x1 + (x2 - x1) * k, y1 + (y2 - y1) * k)
    return track[-1][1:]

def bubble_layer(text, at, tail, size=84, color=SUB_RED):
    """Пузырь-реплика героя (как в комиксе), хвост к губам — слой во весь кадр."""
    key = ('bub', text, tuple(at), tuple(tail), size, color)
    if key in _cache: return _cache[key]
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1))); f = font('Nunito-Black.ttf', size)
    w, h = tmp.textlength(text, font=f) + 120, size * 1.9; cx, cy = at
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.polygon([(cx - 40, cy + h / 2 - 12), (cx + 40, cy + h / 2 - 12), tuple(tail)], fill=(255, 255, 255), outline=DARK, width=7)
    d.ellipse((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), fill=(255, 255, 255), outline=DARK, width=7)
    d.polygon([(cx - 34, cy + h / 2 - 16), (cx + 34, cy + h / 2 - 16),
               (tail[0] + (cx - tail[0]) * 0.25, tail[1] + (cy - tail[1]) * 0.25)], fill=(255, 255, 255))
    d.text((cx, cy), text, font=f, fill=tuple(color), anchor='mm')
    _cache[key] = lay
    return lay

def paste_layer(fr, lay, scale, alpha):
    """Слой во весь кадр с появлением: масштаб вокруг центра его содержимого."""
    bb = lay.getbbox()
    if not bb: return
    paste_scaled(fr, lay.crop(bb), (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2, scale, alpha)

def card_img(header, rows, shown, check=True, color=GREEN):
    """Карточка фиксированной ширины: заголовок и строки, которые появляются по одной.
    rows — строки или пары (слева, справа), например ('Халапеньо', 'до 8 000')."""
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    fh = _fit(tmp, header, 'Nunito-Black.ttf', 60, BOX_W - 80)
    fi = font('Nunito-800.ttf', 50)
    rowh = 80; ph = 118 + rowh * len(rows) + 26
    img, d = _box(BOX_W, ph, 44)
    d.text((20 + BOX_W / 2, 20 + 30), header, font=fh, fill=color, anchor='mt')
    x0, x1 = 20 + 48, 20 + BOX_W - 48
    for i, row in enumerate(rows):
        a = min(max(shown - i, 0), 1)
        if a <= 0: continue
        fade = lambda c: tuple(int(255 - (255 - v) * a) for v in c)
        y = 20 + 126 + i * rowh
        left, right = (row if isinstance(row, (list, tuple)) else (row, None))
        tx = x0
        if check:
            d.ellipse((x0, y, x0 + 54, y + 54), fill=fade(color))
            d.line((x0 + 13, y + 28, x0 + 24, y + 39, x0 + 42, y + 16), fill='white', width=8, joint='curve')
            tx = x0 + 76
        if right:
            fr = _fit(tmp, right, 'Nunito-Black.ttf', 50, 320)
            d.text((x1, y + 27), right, font=fr, fill=fade(ORANGE), anchor='rm')
            fl = _fit(tmp, left, 'Nunito-800.ttf', 50, x1 - tx - d.textlength(right, font=fr) - 30)
        else:
            fl = _fit(tmp, left, 'Nunito-800.ttf', 50, x1 - tx)
        d.text((tx, y + 27), left, font=fl, fill=fade(DARK), anchor='lm')
    return img

def checklist_img(items, shown, header='Как правильно'):
    """Совместимость с первым эпизодом: карточка «Как правильно» с галочками (header — для английских версий)."""
    return card_img(header, items, shown)

def reading_time(o):
    """Сколько секунд текст должен висеть, чтобы его успели прочитать."""
    words = ' '.join(str(x) for x in [o.get('text', ''), o.get('big', ''), o.get('small', ''), o.get('header', '')]
                     + [' '.join(r) if isinstance(r, (list, tuple)) else r for r in o.get('items', o.get('rows', []))]).split()
    need = max(2.5, 1.0 + 0.32 * len(words))
    if o.get('reveal'): need += max(o['reveal'])
    return need

def paste_scaled(base, img, cx, cy, scale, alpha=1.0):
    if scale <= 0.01 or alpha <= 0: return
    im = img if abs(scale - 1) < 1e-3 else img.resize((max(1, int(img.width * scale)), max(1, int(img.height * scale))), Image.BILINEAR)
    if alpha < 1:
        a = im.getchannel('A').point(lambda v: int(v * alpha)); im = im.copy(); im.putalpha(a)
    base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))

def end_card(p, mascot, title, sub):
    bg = Image.new('RGBA', (W, H), CREAM + (255,)); d = ImageDraw.Draw(bg)
    for r in range(0, 1400, 140):  # мягкие круги-«тарелки» на фоне
        d.ellipse((W / 2 - r, H * 0.42 - r, W / 2 + r, H * 0.42 + r), outline=(236, 220, 188, 255), width=26)
    m = mascot.copy(); m.thumbnail((720, 900), Image.LANCZOS)
    s = back(p / 0.35) if p < 0.35 else 1
    paste_scaled(bg, m, W / 2, H * 0.42 + (1 - s) * 200, 0.6 + 0.4 * s)
    ft, fs = font('Nunito-Black.ttf', 96), font('Nunito-800.ttf', 50)
    a = min(max((p - 0.15) / 0.2, 0), 1)
    d = ImageDraw.Draw(bg)
    d.text((W / 2, H * 0.72), title, font=ft, fill=BROWN + (int(255 * a),), anchor='mm')
    d.text((W / 2, H * 0.72 + 96), sub, font=fs, fill=DARK + (int(230 * a),), anchor='mm')
    return bg

# ---------- сборка ----------
def main(tl_path):
    tl = json.load(open(tl_path, encoding='utf-8')); base = os.path.dirname(os.path.abspath(tl_path))
    work = os.path.join(base, 'work'); os.makedirs(work, exist_ok=True)
    P = lambda p: os.path.join(base, p)
    tempo = tl.get('voice_tempo', 1.0)
    voice = np.zeros(SR * 120, np.float32); sfx = np.zeros(SR * 120, np.float32)
    shots, overlays, t0 = [], [], 0.0
    for b in tl['beats']:
        v = read_audio(P(b['voice']), b.get('tempo', tempo)) if b.get('voice') else np.zeros(0, np.float32)
        lead, tail = b.get('pad', [0.12, 0.22])
        T = max(len(v) / SR + lead + tail, b.get('min', 0))
        # текст должен успеть прочитаться: при необходимости бит удлиняется
        texts = b.get('text', [])
        # несколько текстов в бите — только по очереди: у всех, кроме последнего, есть until,
        # и следующий появляется не раньше, чем уходит предыдущий
        seq = sorted([o for o in texts if o.get('kind') not in ('tag', 'bubble')], key=lambda o: o.get('at', 0))
        for a, c in zip(seq, seq[1:]):
            if 'until' not in a or a['until'] > c.get('at', 0):
                sys.exit(f'тексты в бите наложатся: {[o.get("kind") for o in texts]} — задай until и разнеси по времени')
        for o in texts:
            if 'until' not in o and o.get('kind') not in ('tag', 'bubble'): T = max(T, o.get('at', 0) + reading_time(o) + 0.2)
            elif 'until' in o and o['until'] - o.get('at', 0) < reading_time(o) - 0.5:
                print(f'⚠ текст «{o.get("text") or o.get("big") or o.get("header")}» держится меньше, чем нужно на чтение')
            cy = o.get('pos', (W / 2, H * 0.2))[1]
            if not SAFE_Y[0] <= cy <= SAFE_Y[1]: print(f'⚠ текст «{o.get("text") or o.get("big") or o.get("header")}» вне безопасной зоны (y={cy})')
        if len(v): place(voice, v, t0 + lead)
        ws = [s.get('w', 1) for s in b['shots']]; st = t0; spans = []
        for s, wgt in zip(b['shots'], ws):
            d = T * wgt / sum(ws)
            shots.append(dict(s, t=st, d=d)); spans.append((st - t0, st - t0 + d, s.get('subs_y'))); st += d
        for fx in b.get('sfx', []):
            place(sfx, read_audio(P(fx['file']), trim=False), t0 + fx.get('at', 0), fx.get('gain', 1.0))
        for o in b.get('text', []):
            overlays.append(dict(o, t=t0 + o.get('at', 0), end=t0 + (o['until'] if 'until' in o else T), bt=t0))
        # субтитры по словам; в бите с заголовком (хук, вопрос в конце) их нет — обложка остаётся чистой,
        # а обрывок фразы после заголовка («ДЛЯ ЧЕЛОВЕКА») только мешает
        st = tl.get('subs')
        has_title = any(o.get('kind') == 'title' for o in texts)
        if st and b.get('words') and b.get('subs', not has_title):
            t_from = max([o.get('until', T) for o in texts if o.get('kind') == 'title'] + [0])
            keys = {k.lower(): tuple(v) for k, v in st.get('keys', {}).items()}
            for a, e, lines in subs_chunks(b['words'], keys, lead, t_from, T):
                # высота: у кадра своя ("subs_y" у шота), иначе у бита, иначе общая
                # кусок, который переходит через склейку, на склейке переезжает на высоту нового кадра
                cuts = [a] + [s0 for s0, _, _ in spans if a + 0.05 < s0 < e - 0.05] + [e]
                for c0, c1 in zip(cuts, cuts[1:]):
                    sy = next((y for s0, s1, y in spans if s0 <= c0 + 0.05 < s1 and y), None) or b.get('subs_y', st.get('y', 1250))
                    overlays.append(dict(kind='subs', lines=lines, t=t0 + c0, end=t0 + c1,
                                         pos=(W / 2, sy), size=st.get('size', 104)))
        t0 += T
    total = t0
    if '--plan' in sys.argv:  # длины кадров — по ним заказываются клипы анимации
        for i, sh in enumerate(shots):
            print(f'{i:2d}  {sh["t"]:6.2f}  {sh["d"]:5.2f} с  {sh.get("img") or sh.get("clip") or "end"}')
        print(f'итого {total:.1f} с'); return
    # источники кадров
    for s in shots:
        if 'img' in s: s['src'] = Still(P(s['img']), s.get('move', 'in'), tuple(s.get('focus', (0.5, 0.5))), s.get('amount', 0.08))
        elif 'clip' in s:
            s['src'] = Clip(P(s['clip']), s.get('ss', 0), s.get('speed', 1.0), s.get('to'), s.get('pingpong', False),
                            s.get('zoom', 1.0), tuple(s.get('focus', (0.5, 0.5))), need=s['d'] + 0.5)
            have = len(s['src'].frames) / FPS
            if have + 0.05 < s['d']: print(f'⚠ клип {s["clip"]} короче кадра: {have:.2f} < {s["d"]:.2f} с — конец заморозится')
    mascot = Image.open(os.path.join(HERE, '..', '..', 'public', 'admin', 'reference.png')).convert('RGBA')
    # рендер
    vid = os.path.join(work, 'video.mp4')
    enc = subprocess.Popen([FF, '-hide_banner', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                            '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium',
                            '-crf', '18', '-pix_fmt', 'yuv420p', vid], stdin=subprocess.PIPE)
    xfade = tl.get('xfade', 0)
    def shot_frame(sh, t):  # кадр шота в момент t (после конца шота — его последний кадр)
        if isinstance(sh['src'], Still): return sh['src'].frame(min((t - sh['t']) / sh['d'], 1.0)).convert('RGBA')
        return sh['src'].frame_at(t - sh['t']).convert('RGBA')
    nframes = int(round(total * FPS)); si = 0
    for n in range(nframes):
        t = n / FPS
        while si < len(shots) - 1 and t >= shots[si + 1]['t']: si += 1
        s = shots[si]; p = (t - s['t']) / s['d']
        if s.get('end_card'):
            fr = end_card(p, mascot, s['end_card'][0], s['end_card'][1])
        else:
            fr = shot_frame(s, t)
        # мягкий переход: первые xfade секунд кадр проявляется поверх продолжения предыдущего
        # ("cut": true у кадра — оставить резкую склейку, например для комедийного удара)
        if xfade and si > 0 and t - s['t'] < xfade and not s.get('cut') and not s.get('end_card') \
                and not shots[si - 1].get('end_card'):
            fr = Image.blend(shot_frame(shots[si - 1], t), fr, (t - s['t']) / xfade)
        sh = s.get('shake')
        if sh and sh[0] <= t - s['t'] <= sh[0] + sh[1]:
            k = 1 - (t - s['t'] - sh[0]) / sh[1]; amp = sh[2] * k
            dx, dy = amp * math.sin(t * 95), amp * math.cos(t * 77)
            big = fr.resize((int(W * 1.04), int(H * 1.04)), Image.BILINEAR)
            fr = big.crop((int(W * 0.02 + dx), int(H * 0.02 + dy), int(W * 0.02 + dx) + W, int(H * 0.02 + dy) + H))
        fl = s.get('flash')
        if fl is not None and 0 <= t - s['t'] - fl < 0.18:
            a = 1 - (t - s['t'] - fl) / 0.18
            fr = Image.blend(fr, Image.new('RGBA', (W, H), (255, 255, 255, 255)), a * 0.85)
        for o in overlays:
            if not (o['t'] <= t < o['end']): continue
            q = t - o['t']; out = min(max((o['end'] - t) / 0.15, 0), 1)
            sc = back(q / 0.28) if q < 0.28 else 1.0
            cx, cy = o.get('pos', (W / 2, H * 0.2))
            if o['kind'] == 'title':
                col = tuple(o['color']) if o.get('color') else None
                paste_scaled(fr, title_img(o['text'], o.get('size', 84), o.get('plate', False), col, o.get('box')), cx, cy, 0.85 + 0.15 * sc, out)
            elif o['kind'] == 'sticker': paste_scaled(fr, sticker_img(o['big'], o.get('small'), tuple(o.get('color', ORANGE))), cx, cy, sc, out)
            elif o['kind'] == 'subs':
                s2 = back(q / 0.16) if q < 0.16 else 1.0
                paste_scaled(fr, subs_img(o['lines'], o.get('size', 104)), cx, cy, 0.8 + 0.2 * s2, min(out * 3, 1))
            elif o['kind'] == 'tag':  # "track" — стрелка ведёт за движущимся предметом (track.py)
                tg = [round(v) for v in track_at(o['track'], t - o['bt'])] if o.get('track') else o['target']
                paste_layer(fr, tag_layer(o['text'], o['pos'], tg, o.get('angle', -6), o.get('size', 74),
                                          tuple(o.get('color', SUB_YELLOW)), cache=not o.get('track')), sc, out)
            elif o['kind'] == 'bubble':
                paste_layer(fr, bubble_layer(o['text'], o['pos'], o['tail'], o.get('size', 84),
                                             tuple(o.get('color', SUB_RED))), sc, out)
            elif o['kind'] == 'card':
                shown = sum(min(max((q - r) / 0.2, 0), 1) for r in o['reveal'])
                paste_scaled(fr, card_img(o['header'], o['rows'], shown, o.get('check', True), tuple(o.get('color', GREEN))), cx, cy, sc, out)
            elif o['kind'] == 'checklist':
                shown = sum(min(max((q - r) / 0.2, 0), 1) for r in o['reveal'])  # reveal — от начала карточки
                paste_scaled(fr, checklist_img(o['items'], shown, o.get('header', 'Как правильно')), cx, cy, sc, out)
        enc.stdin.write(fr.convert('RGB').tobytes())
    enc.stdin.close(); enc.wait()
    # звук: голос + музыка (приглушение под голосом) + звуки
    n = int(total * SR); mix = voice[:n] + sfx[:n] * tl.get('sfx_gain', 0.8)
    if tl.get('music'):
        m = read_audio(P(tl['music']['file']), trim=False)[int(tl['music'].get('start', 0) * SR):]  # start — с какой секунды трека
        m = np.resize(m, n) if len(m) < n else m[:n]
        env = np.abs(voice[:n]); k = int(SR * 0.25)
        env = np.convolve(env, np.ones(k) / k, 'same'); duck = 1 - tl['music'].get('duck', 0.55) * np.clip(env / 0.03, 0, 1)
        fade = np.ones(n); fo = int(SR * 1.2); fade[-fo:] = np.linspace(1, 0, fo)
        mix += m * tl['music'].get('gain', 0.22) * duck * fade
    wav = os.path.join(work, 'mix.wav'); write_wav(wav, mix * 0.9)
    out = P(tl['out'])
    ff(['-i', vid, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11',
        '-c:a', 'aac', '-b:a', '192k', '-ar', str(SR), '-movflags', '+faststart', '-shortest', out])
    print(f'готово: {out} ({total:.1f} с, кадров: {len(shots)})')

if __name__ == '__main__':
    main(sys.argv[1])
