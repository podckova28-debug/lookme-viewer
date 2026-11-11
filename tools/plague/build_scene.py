"""Plague channel: assemble a scene from still frames + narration into an mp4.

Fast cuts (2-3 s), slow camera moves inside each frame (push / pull / pan), captions and a title card,
synthesized ambience, SFX and a dark drone. Everything is local and free; only the frames and the
voice lines come from generation.

usage: python3 tools/plague/build_scene.py tools/plague/cold_open.json out/plague_cold_open.mp4
"""
import sys, os, json, math, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy.io import wavfile
from scipy.signal import butter, sosfilt, resample_poly

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W, H, FPS, SR = 1920, 1080, 24, 48000
FONT_SC = os.path.join(ROOT, 'assets/fonts/IMFellEnglishSC.ttf')   # old-print small caps, matches the ink look
FONT_RM = os.path.join(ROOT, 'assets/fonts/IMFellEnglish.ttf')
spec = json.load(open(sys.argv[1])); out = sys.argv[2]
base = os.path.join(ROOT, spec['base'])
TOTAL = spec['duration']
N = lambda s: int(round(s * SR))
rng = np.random.default_rng(3)

def ease(u): u = min(max(u, 0), 1); return u * u * (3 - 2 * u)

# ---------------- picture ----------------
_fc = {}
def font(size, lower=False):
    k = (size, lower)
    if k not in _fc: _fc[k] = ImageFont.truetype(FONT_RM if lower else FONT_SC, size)
    return _fc[k]

INK, CREAM, GOLD, RED = (50, 32, 20), (242, 232, 208), (184, 146, 84), (176, 38, 28)

def draw_item(it, k):
    """one text/box item -> full-frame RGBA layer. styles:
       ink   - dark ink printed onto a paper surface in the picture (menu panels, book pages, decrees, maps)
       plate - cream letters on a dark museum-label plate with a thin gold rule (captions, labels over scenes)
       stamp - red rubber stamp: red letters in a red frame on a pale patch, slightly rotated
       title - big cream letters with a soft shadow (title card)
       dim   - darkened soft rectangle (to spotlight one part of the picture)"""
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    st = it.get('style', 'plate')
    if st == 'dim':
        d.rounded_rectangle(it['rect'], 24, fill=tuple(it.get('fill', (0, 0, 0, 120))))
        return L.filter(ImageFilter.GaussianBlur(10))
    txt = it['text']; low = any(c.islower() for c in txt); size = int(it['size'] * k)
    while it.get('maxw') and size > 20 and font(size, low).getlength(txt) > it['maxw'] * k: size -= 2   # shrink to fit
    f = font(size, low)
    x, y, anc = it['x'], it['y'], it.get('anchor', 'mm')
    bx = d.textbbox((x, y), txt, font=f, anchor=anc)
    if st == 'ink' and it.get('force_ink'):   # dark ink kept only where explicitly asked; by default all text is light-on-shadow for legibility
        col = tuple(it.get('color', INK)); sw = max(1, size // 34)
        d.text((x, y), txt, font=f, fill=col + (235,), anchor=anc, stroke_width=sw, stroke_fill=col + (235,))
        return L
    if st == 'tag':   # paper label pinned in the picture: dark ink on a cream card with a thin dark border
        px, py = int(size * .45), int(size * .22)
        box = (bx[0] - px, bx[1] - py, bx[2] + px, bx[3] + py)
        S = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(S).rectangle((box[0] + 4, box[1] + 6, box[2] + 4, box[3] + 6), fill=(0, 0, 0, 140))
        L = Image.alpha_composite(S.filter(ImageFilter.GaussianBlur(5)), L); d = ImageDraw.Draw(L)
        d.rectangle(box, fill=(236, 224, 198, 255), outline=INK + (255,), width=max(2, size // 22))
        d.text((x, y), txt, font=f, fill=INK + (255,), anchor=anc, stroke_width=max(1, size // 34), stroke_fill=INK + (255,))
        return L
    if st == 'title':
        col = tuple(it.get('color', CREAM)); sw = max(1, size // 40)
        S = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(S).text((x + 4, y + 6), txt, font=f, fill=(0, 0, 0, 220), anchor=anc, stroke_width=sw + 4, stroke_fill=(0, 0, 0, 220))
        L = Image.alpha_composite(S.filter(ImageFilter.GaussianBlur(8)), L); d = ImageDraw.Draw(L)
        d.text((x, y), txt, font=f, fill=col + (255,), anchor=anc, stroke_width=sw, stroke_fill=col + (255,))
        return L
    if st == 'stamp':
        px, py = int(size * .35), int(size * .18)
        T = Image.new('RGBA', (bx[2] - bx[0] + 2 * px + 40, bx[3] - bx[1] + 2 * py + 40), (0, 0, 0, 0)); td = ImageDraw.Draw(T)
        r = (20, 20, T.width - 20, T.height - 20)
        td.rectangle(r, fill=(238, 226, 200, 235)); td.rectangle(r, outline=RED + (255,), width=max(4, size // 16))
        td.rectangle((r[0] + size // 9, r[1] + size // 9, r[2] - size // 9, r[3] - size // 9), outline=RED + (255,), width=max(2, size // 40))
        td.text((T.width / 2, T.height / 2), txt, font=f, fill=RED + (255,), anchor='mm', stroke_width=max(1, size // 30), stroke_fill=RED + (255,))
        T = T.rotate(it.get('rot', -6), resample=Image.BICUBIC, expand=True)
        L.alpha_composite(T, (int(x - T.width / 2), int(y - T.height / 2)))
        return L
    # plate (default caption): cream letters on a soft dark shadow, no box
    col = tuple(it.get('color', CREAM)); sw = max(1, size // 40)
    S = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(S)
    sd.text((x + 2, y + 3), txt, font=f, fill=(0, 0, 0, 235), anchor=anc, stroke_width=sw + max(6, size // 5), stroke_fill=(0, 0, 0, 235))
    L = Image.alpha_composite(S.filter(ImageFilter.GaussianBlur(max(6, size // 5))), L); d = ImageDraw.Draw(L)
    d.text((x, y), txt, font=f, fill=col + (255,), anchor=anc, stroke_width=sw + 1, stroke_fill=(20, 14, 10, 255))
    d.text((x, y), txt, font=f, fill=col + (255,), anchor=anc, stroke_width=sw, stroke_fill=col + (255,))
    return L

def text_layer(items, t):
    lay = None
    for it in items:
        a = min(1, (t - it['t0']) / .35, (it.get('t1', 1e9) - t) / .35)
        if a <= 0: continue
        if lay is None: lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        k = 1 + .25 * (1 - ease(min(1, (t - it['t0']) / .45))) if it.get('pop') else 1
        key = (id(it), round(k, 3))
        L = _lc.get(key)
        if L is None:
            L = draw_item(it, k)
            if k == 1: _lc[key] = L
        if a < 1: L = L.copy(); L.putalpha(L.getchannel('A').point(lambda v: int(v * a)))
        lay = Image.alpha_composite(lay, L)
    return lay
_lc = {}

class Frame:
    cache = {}
    @classmethod
    def get(cls, name):
        if name not in cls.cache:
            im = cv2.imread(os.path.join(base, name + '.jpg'))
            s = 2 * W / im.shape[1]   # work at 2x output width so pushes stay sharp
            cls.cache[name] = cv2.resize(im, None, fx=s, fy=s, interpolation=cv2.INTER_LANCZOS4)
        return cls.cache[name]

def render_shot(sh, t):
    """camera = rectangle (cx, cy, zoom) interpolated from 'from' to 'to'; coords are 0..1 of the image"""
    im = Frame.get(sh['img']); ih, iw = im.shape[:2]
    u = ease((t - sh['t0']) / (sh['t1'] - sh['t0'])) if sh.get('ease', True) else (t - sh['t0']) / (sh['t1'] - sh['t0'])
    a, b = sh.get('from', [.5, .5, 1.0]), sh.get('to', [.5, .5, 1.06])
    cx, cy, z = [a[i] + (b[i] - a[i]) * u for i in range(3)]
    cw, ch = iw / z, iw / z * H / W
    if ch > ih: ch = ih; cw = ch * W / H
    x0 = min(max(cx * iw - cw / 2, 0), iw - cw); y0 = min(max(cy * ih - ch / 2, 0), ih - ch)
    shake = sh.get('shake', 0)
    if shake: x0 += math.sin(t * 37) * shake; y0 += math.cos(t * 29) * shake
    M = np.float32([[W / cw, 0, -x0 * W / cw], [0, H / ch, -y0 * H / ch]])
    return cv2.warpAffine(im, M, (W, H), flags=cv2.INTER_AREA if cw > W else cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

vig = None
def finish(img, t):
    global vig
    if vig is None:
        yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
        vig = (1 - .32 * np.clip(r - .55, 0, 1) ** 1.4)[..., None].astype(np.float32)
    f = img.astype(np.float32) * vig
    g = rng.normal(0, 2.2, (H // 2, W // 2, 1)).astype(np.float32); f += cv2.resize(g, (W, H))[..., None]
    return np.clip(f, 0, 255).astype(np.uint8)

def picture(path):
    shots = spec['shots']; texts = spec.get('texts', [])
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p', path], stdin=subprocess.PIPE)
    n = int(round(TOTAL * FPS))
    for i in range(n):
        t = i / FPS
        sh = next((s for s in shots if s['t0'] <= t < s['t1']), shots[-1])
        img = render_shot(sh, t)
        fo = sh.get('fade_out')
        if fo and t > sh['t1'] - fo: img = (img * max(0, (sh['t1'] - t) / fo)).astype(np.uint8)
        if t < spec.get('fade_in', 0): img = (img * (t / spec['fade_in'])).astype(np.uint8)
        lay = text_layer(texts, t)
        if lay is not None:
            base_im = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)).convert('RGBA')
            img = cv2.cvtColor(np.array(Image.alpha_composite(base_im, lay).convert('RGB')), cv2.COLOR_RGB2BGR)
        ff.stdin.write(finish(img, t).tobytes())
    ff.stdin.close(); ff.wait()

# ---------------- sound ----------------
tt = lambda d: np.arange(N(d)) / SR
def filt(x, kind, f, order=2):
    f = np.atleast_1d(f); return sosfilt(butter(order, f / (SR / 2) if len(f) > 1 else f[0] / (SR / 2), btype=kind, output='sos'), x)
def noise(d): return rng.standard_normal(N(d))
def fade(x, a=.01, b=.05):
    x = x.copy(); na, nb = min(len(x), N(a)), min(len(x), N(b)); x[:na] *= np.linspace(0, 1, na); x[-nb:] *= np.linspace(1, 0, nb); return x
def norm(x, p=1.0): return x / (np.max(np.abs(x)) or 1) * p
def sweep(f0, f1, d, c=1.0): u = np.linspace(0, 1, N(d)) ** c; return np.sin(2 * np.pi * np.cumsum(f0 + (f1 - f0) * u) / SR)

def waves(d):
    x = filt(noise(d), 'lowpass', 300, 4) * (.55 + .45 * np.sin(2 * np.pi * tt(d) / 5.5) ** 2)
    return fade(x + .08 * filt(noise(d), 'bandpass', [600, 1400]) * (.5 + .5 * np.sin(2 * np.pi * tt(d) / 3.7 + 1)) ** 4, 1, 1)
def wind(d): return fade(filt(noise(d), 'bandpass', [150, 450], 4) * (.6 + .4 * np.sin(2 * np.pi * tt(d) / 7)), 1.5, 1.5)
def creak(d=.9, f=180):
    t = tt(d); pulses = (np.sin(2 * np.pi * (35 + 25 * t / d) * t) > .7).astype(float)
    return fade(filt(pulses * noise(d) * .5 + pulses, 'bandpass', [f, f * 6]) * np.sin(np.linspace(0, np.pi, N(d))), .05, .2)
def bell(f=196, d=4.0):
    t = tt(d); x = sum(g * np.sin(2 * np.pi * f * m * t) * np.exp(-t / (1.8 / m ** .5)) for m, g in [(1, 1), (2.0, .5), (2.4, .35), (3.0, .25), (4.2, .15)])
    return norm(fade(x, .002, .3), .5)
def step(): d = .16; return norm(filt(noise(d), 'lowpass', 900) * np.exp(-tt(d) / .025) + .4 * np.sin(2 * np.pi * 90 * tt(d)) * np.exp(-tt(d) / .04), .5)
def squeak(): d = .22; return norm(sweep(3200, 4400, d, .5) * np.sin(np.linspace(0, np.pi, N(d))) ** 2, .25)
def scurry(d=1.5):
    x = np.zeros(N(d))
    for k in range(int(d * 14)): n0 = N(rng.uniform(0, d - .05)); s = filt(noise(.03), 'bandpass', [2000, 6000]) * np.exp(-tt(.03) / .006); x[n0:n0 + len(s)] += s
    return x * .4
def murmur(d): return fade(filt(noise(d), 'bandpass', [250, 1100]) * (.5 + .5 * np.abs(np.sin(2 * np.pi * tt(d) * 1.7))), .4, .6) * .35
def gasp(): d = .5; return norm(fade(filt(noise(d), 'bandpass', [600, 2600]) * np.exp(-tt(d) / .18), .02, .1), .4)
def shutter(): d = .25; return norm(filt(noise(d), 'lowpass', 1500) * np.exp(-tt(d) / .03) + .5 * np.sin(2 * np.pi * 120 * tt(d)) * np.exp(-tt(d) / .05), .7)
def page(): d = .45; return norm(fade(filt(noise(d), 'highpass', 2500) * np.sin(np.linspace(0, np.pi, N(d))) ** 3, .02, .1), .35)
def boom(d=3.0):
    x = sweep(70, 28, d, .4) * np.exp(-tt(d) / .9) + .5 * filt(noise(d), 'lowpass', 160) * np.exp(-tt(d) / .4)
    return norm(fade(x, .003, .5), .9)
def riser(d=1.2): return norm(fade(filt(noise(d), 'bandpass', [300, 3000]) * np.linspace(0, 1, N(d)) ** 3, .1, .02), .45)
def drone(d):
    t = tt(d); out = np.zeros(N(d))
    for f, g in [(55, .5), (65.4, .35), (82.4, .3), (110, .18), (130.8, .12)]:
        out += g * np.sin(2 * np.pi * f * t + .6 * np.sin(2 * np.pi * .07 * t * f / 55))
    out *= .7 + .3 * np.sin(2 * np.pi * t / 9)
    pulse = np.zeros(N(d))
    for k in np.arange(0, d, 2.4):     # slow heartbeat-like low pulse
        n0 = N(k); s = sweep(60, 40, .5, .5) * np.exp(-tt(.5) / .14); pulse[n0:n0 + len(s)] += s[:len(pulse) - n0]
    return fade(filt(out, 'lowpass', 900) * .6 + pulse * .5, 2, 2)
SFX = dict(waves=waves, wind=wind, creak=creak, bell=bell, step=step, squeak=squeak, scurry=scurry, murmur=murmur, gasp=gasp,
           shutter=shutter, page=page, boom=boom, riser=riser, drone=drone)

def sound(path):
    L = {k: np.zeros(N(TOTAL) + SR * 5) for k in ('vo', 'fx', 'mus')}
    def put(layer, t, x, g=1.0): n0 = N(t); n1 = min(n0 + len(x), len(L[layer])); L[layer][n0:n1] += x[:n1 - n0] * g
    for v in spec['vo']:
        sr, x = wavfile.read(os.path.join(ROOT, v['file'])); x = x.astype(np.float64); x = x.mean(1) if x.ndim > 1 else x
        if sr != SR: x = resample_poly(x, SR, sr)
        put('vo', v['t'], x / (np.max(np.abs(x)) or 1) * .85, v.get('gain', 1.0))
    for e in spec['sfx']:
        args = e.get('args', {}); x = SFX[e['kind']](**args); put('mus' if e['kind'] == 'drone' else 'fx', e['t'], x, e.get('gain', 1.0))
    bed = np.zeros_like(L['mus'])
    for m in spec.get('music', []):   # music bed: each entry loops its file (3 s crossfades) over [t0, t1] with fades
        raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', os.path.join(ROOT, m['file']), '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'])
        x = np.frombuffer(raw, np.float32).astype(np.float64); x = x / (np.sqrt(np.mean(x ** 2)) or 1) * .07   # equal loudness per track
        t1 = TOTAL if m.get('t1', 'ALL') == 'ALL' else m['t1']; need = N(t1 - m['t0']); xf = N(3.0)
        y = x.copy()
        while len(y) < need:
            r = np.linspace(0, 1, xf); y = np.concatenate([y[:-xf], y[-xf:] * (1 - r) + x[:xf] * r, x[xf:]])
        y = y[:need].copy(); fi, fo = N(m.get('fade_in', 3.0)), N(m.get('fade_out', 3.0))
        y[:fi] *= np.linspace(0, 1, fi); y[-fo:] *= np.linspace(1, 0, fo)
        n0 = N(m['t0']); bed[n0:n0 + len(y)] += y[:len(bed) - n0] * m.get('gain', 1.0)
    v = L['vo']; env = np.convolve(np.abs(v), np.ones(N(.08)) / N(.08), 'same'); env = np.minimum(env / .06, 1)
    k = np.exp(-1 / (SR * .25)); sm = np.empty_like(env); y = 0.0
    for i in range(0, len(env), 48): y = max(env[i], y * k ** 48); sm[i:i + 48] = y
    mix = v + L['fx'] * (1 - .6 * sm) * .5 + L['mus'] * (1 - .55 * sm) * .4 * (.5 if spec.get('music') else 1) + bed * (1 - .6 * sm)
    mix = mix[:N(TOTAL)]; mix = mix / np.max(np.abs(mix)) * .89
    wavfile.write(path, SR, (np.stack([mix, mix], 1) * 32767).astype(np.int16))

def still(t, path):
    sh = next((s for s in spec['shots'] if s['t0'] <= t < s['t1']), spec['shots'][-1])
    img = render_shot(sh, t); lay = text_layer(spec.get('texts', []), t)
    if lay is not None:
        img = cv2.cvtColor(np.array(Image.alpha_composite(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)).convert('RGBA'), lay).convert('RGB')), cv2.COLOR_RGB2BGR)
    cv2.imwrite(path, finish(img, t))

if __name__ == '__main__' and os.environ.get('RANGE'):   # RANGE="86,104" -> re-render only that span (video only) for patching
    a0, a1 = map(float, os.environ['RANGE'].split(','))
    shots = spec['shots']; texts = spec.get('texts', [])
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i in range(int(round(a0 * FPS)), int(round(a1 * FPS))):
        t = i / FPS; sh = next((s for s in shots if s['t0'] <= t < s['t1']), shots[-1]); img = render_shot(sh, t)
        lay = text_layer(texts, t)
        if lay is not None:
            img = cv2.cvtColor(np.array(Image.alpha_composite(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)).convert('RGBA'), lay).convert('RGB')), cv2.COLOR_RGB2BGR)
        ff.stdin.write(finish(img, t).tobytes())
    ff.stdin.close(); ff.wait()
elif __name__ == '__main__' and os.environ.get('STILLS'):   # STILLS="12.5,40" -> OUT_12.5.jpg ...: check text placement without a render
    for t in os.environ['STILLS'].split(','): still(float(t), f'{out}_{t}.jpg')
elif __name__ == '__main__':
    tmp_v, tmp_a = out + '.v.mp4', out + '.a.wav'
    sound(tmp_a); picture(tmp_v)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp_v, '-i', tmp_a, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                    '-af', 'loudnorm=I=-15:TP=-1.5:LRA=11', '-shortest', '-movflags', '+faststart', out], check=True)
    os.remove(tmp_v); os.remove(tmp_a); print('wrote', out)
