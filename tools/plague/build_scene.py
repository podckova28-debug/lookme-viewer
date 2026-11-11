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
FONT = os.path.join(ROOT, 'assets/fonts/Cinzel-VF.ttf')
spec = json.load(open(sys.argv[1])); out = sys.argv[2]
base = os.path.join(ROOT, spec['base'])
TOTAL = spec['duration']
N = lambda s: int(round(s * SR))
rng = np.random.default_rng(3)

def ease(u): u = min(max(u, 0), 1); return u * u * (3 - 2 * u)

# ---------------- picture ----------------
def font(size, weight='Black'):
    f = ImageFont.truetype(FONT, size); f.set_variation_by_name(weight); return f

def text_layer(items, t):
    """items: [{text, x, y, size, t0, t1, color, anchor, weight, track}] -> RGBA overlay or None"""
    lay = None
    for it in items:
        a = min(1, (t - it['t0']) / .35, (it.get('t1', 1e9) - t) / .35)
        if a <= 0: continue
        if lay is None: lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        k = 1 + .25 * (1 - ease(min(1, (t - it['t0']) / .45))) if it.get('pop') else 1
        f = font(int(it['size'] * k), it.get('weight', 'Black'))
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        col = tuple(it.get('color', [244, 238, 224]))
        sw = max(3, it['size'] // 14)
        d.text((it['x'], it['y']), it['text'], font=f, fill=col + (255,), anchor=it.get('anchor', 'mm'), stroke_width=sw, stroke_fill=(16, 12, 10, 255))
        if it.get('plate'):   # dark band behind small captions
            bx = d.textbbox((it['x'], it['y']), it['text'], font=f, anchor=it.get('anchor', 'mm'), stroke_width=sw)
            P = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(P).rectangle((bx[0] - 30, bx[1] - 16, bx[2] + 30, bx[3] + 16), fill=(10, 8, 8, 150))
            L = Image.alpha_composite(P, L)
        L.putalpha(L.getchannel('A').point(lambda v: int(v * a)))
        lay = Image.alpha_composite(lay, L)
    return lay

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
    g = rng.normal(0, 5.5, (H // 2, W // 2, 1)).astype(np.float32); f += cv2.resize(g, (W, H))[..., None]
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
    x = filt(noise(d), 'lowpass', 500) * (.55 + .45 * np.sin(2 * np.pi * tt(d) / 5.5) ** 2)
    return fade(x + .3 * filt(noise(d), 'bandpass', [800, 2500]) * (.5 + .5 * np.sin(2 * np.pi * tt(d) / 3.7 + 1)) ** 4, 1, 1)
def wind(d): return fade(filt(noise(d), 'bandpass', [180, 700]) * (.6 + .4 * np.sin(2 * np.pi * tt(d) / 7)), 1.5, 1.5)
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
    v = L['vo']; env = np.convolve(np.abs(v), np.ones(N(.08)) / N(.08), 'same'); env = np.minimum(env / .06, 1)
    k = np.exp(-1 / (SR * .25)); sm = np.empty_like(env); y = 0.0
    for i in range(0, len(env), 48): y = max(env[i], y * k ** 48); sm[i:i + 48] = y
    mix = v + L['fx'] * (1 - .45 * sm) * .7 + L['mus'] * (1 - .5 * sm) * .45
    mix = mix[:N(TOTAL)]; mix = mix / np.max(np.abs(mix)) * .89
    wavfile.write(path, SR, (np.stack([mix, mix], 1) * 32767).astype(np.int16))

if __name__ == '__main__':
    tmp_v, tmp_a = out + '.v.mp4', out + '.a.wav'
    sound(tmp_a); picture(tmp_v)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp_v, '-i', tmp_a, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                    '-af', 'loudnorm=I=-15:TP=-1.5:LRA=11', '-shortest', '-movflags', '+faststart', out], check=True)
    os.remove(tmp_v); os.remove(tmp_a); print('wrote', out)
