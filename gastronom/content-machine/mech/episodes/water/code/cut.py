#!/usr/bin/env python3
"""Сборка ролика из кадров 2K (плавный наезд/панорама, субпиксельно — без дрожания) и клипов 1080p.
Длины планов — из голоса. Раскладка — timeline.py (LINES, SHOTS, LABELS, CLIPS).

    python3 cut.py [--plan] [--from A --to B] [--out файл.mp4]
"""
import math, os, subprocess, sys, wave
import numpy as np, imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FF = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS, SR = 1920, 1080, 30, 44100
TEMPO = 0.8; LEAD = 0.10; TAIL = 0.20; XF = 0.5  # края реплик уже в vo/*.wav (pauses3: 30 мс до, 60 мс после)  # паузы короче, чем в sovhacks (0,25/0,45): «поработай с паузками»
FONT = '/home/user/gastronom/content-machine/video/fonts/Nunito-Black.ttf'
INK = (43, 33, 24); CREAM = (255, 248, 232)
HERE = os.path.dirname(os.path.abspath(__file__)); P = lambda p: os.path.join(HERE, p)
sys.path.insert(0, HERE)
from timeline import LINES, SHOTS, LABELS, CLIPS, MUSIC, OVERLAYS, PAUSE, TAILX, FALLBACK
try:
    from timeline import LINE_TEMPO
except ImportError:
    LINE_TEMPO = {}

def vo_line(lid):
    """Реплика без обрезки по порогу (края сделал pauses3.py) и со своим темпом для торопливых реплик."""
    return read_audio(P(f'vo/{lid}.wav'), TEMPO * LINE_TEMPO.get(lid, 1.0), trim=False)
import gfx

def read_audio(path, tempo=1.0, trim=True):
    af = []
    if trim: af.append('silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse')
    if tempo != 1.0: af.append(f'atempo={tempo}')
    raw = subprocess.run([FF, '-v', 'error', '-i', path, *(['-af', ','.join(af)] if af else []), '-f', 's16le', '-ac', '1', '-ar', str(SR), '-'],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768

def dur(path):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout)

# ---------- раскладка ----------
LT = {}  # реплика -> (начало с паузой, начало голоса, конец)
def plan():
    t = 0.0; shots = []; used = {}
    for lid, text in LINES:
        v = vo_line(lid); pre = PAUSE.get(lid, 0.0)
        T = pre + LEAD + len(v) / SR + TAIL + TAILX.get(lid, 0.0)
        LT[lid] = (t, t + pre + LEAD, t + T)
        ws = SHOTS[lid]; tot = sum(s[1] for s in ws); st = t
        for name, w, *mv in ws:
            d = T * w / tot
            shots.append(dict(name=name, line=lid, t=st, d=d, off=used.get(name, 0.0), mv=(mv[0] if mv else None)))
            used[name] = used.get(name, 0.0) + d; st += d
        t += T
    for i, s in enumerate(shots):
        c = CLIPS[s['name']]
        if c['file'].endswith('.mp4'): continue
        a, b = resolve(s['mv'] or c.get('mv') or 'in', c['file'])
        if i and shots[i - 1]['name'] == s['name'] and 'pose' in shots[i - 1]:
            a = shots[i - 1]['pose'][1]; s['cont'] = True
            if max(abs(x - y) for x, y in zip(a, b)) < 0.02: b = (a[0] * 1.08, a[1], a[2])
        s['pose'] = (a, b)
    return shots, t

PRESETS = {'in': ((1.0, .5, .5), (1.12, .5, .5)), 'out': ((1.12, .5, .5), (1.0, .5, .5)),
           'left': ((1.1, .56, .5), (1.1, .44, .5)), 'right': ((1.1, .44, .5), (1.1, .56, .5)),
           'up': ((1.1, .5, .56), (1.1, .5, .44)), 'down': ((1.1, .5, .44), (1.1, .5, .56))}
MPOSE = ((1.16, .5, .44), (1.28, .5, .41))  # Михалыч в kf_m снят шире — камера ближе к нему
def resolve(mv, f=''):
    if f.startswith('kf_m/') and mv == 'in': return MPOSE
    return PRESETS[mv] if isinstance(mv, str) else mv

# ---------- источники ----------
def ease(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)

class Still:
    """Кадр 2K: камера от (zoom0, cx0, cy0) к (zoom1, cx1, cy1); zoom 1 = весь кадр по ширине."""
    cache = {}
    def __init__(self, shot):
        c = CLIPS[shot['name']]; f = P(c['file'])
        if f not in Still.cache: Still.cache = {f: Image.open(f).convert('RGB')}
        self.im = Still.cache[f]; self.iw, self.ih = self.im.size
        self.a, self.b = shot.get('pose') or resolve(shot['mv'] or c.get('mv') or 'in', c['file'])
        self.T = shot['d'] + (0 if shot.get('cont') else XF); self.k = 0
    def skip(self, n): self.k += n
    def next(self):
        x = ease(self.k / FPS / self.T); self.k += 1
        z = self.a[0] + (self.b[0] - self.a[0]) * x
        cx = self.a[1] + (self.b[1] - self.a[1]) * x; cy = self.a[2] + (self.b[2] - self.a[2]) * x
        cw = self.iw / z; ch = cw * H / W
        if ch > self.ih: ch = self.ih; cw = ch * W / H
        x0 = min(max(cx * self.iw - cw / 2, 0), self.iw - cw); y0 = min(max(cy * self.ih - ch / 2, 0), self.ih - ch)
        s = cw / W
        out = self.im.transform((W, H), Image.AFFINE, (s, 0, x0, 0, s, y0), resample=Image.BICUBIC)
        return np.asarray(out)
    def close(self): pass

class Clip:
    def __init__(self, shot):
        c = CLIPS[shot['name']]; f = P(c['file'])
        avail = c.get('to', dur(f)) - c.get('ss', 0); need = shot['off'] + shot['d'] + XF
        sp = min(1.0, avail / need); ss = c.get('ss', 0) + shot['off'] * sp; self.speed = sp
        vf = f'setpts=(PTS-STARTPTS)/{sp},fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}'
        self.p = subprocess.Popen([FF, '-v', 'error', '-ss', f'{ss:.3f}', '-i', f, '-vf', vf, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
        self.n = W * H * 3; self.last = None
    def skip(self, n):
        for _ in range(n): self.next()
    def next(self):
        b = self.p.stdout.read(self.n)
        if len(b) == self.n: self.last = np.frombuffer(b, np.uint8).reshape(H, W, 3)
        return self.last
    def close(self):
        try: self.p.kill()
        except Exception: pass

def source(shot):
    c = CLIPS[shot['name']]
    if c['file'].endswith('.mp4') and not os.path.exists(P(c['file'])) and shot['name'] in FALLBACK:
        print('нет клипа', shot['name'], '→ кадр', FALLBACK[shot['name']], flush=True)
        return Still(dict(shot, name=FALLBACK[shot['name']], mv='in', pose=None, cont=False))
    return Clip(shot) if c['file'].endswith('.mp4') else Still(shot)

# ---------- подписи ----------
_cache = {}
def plate(text, size=60, color=INK):
    k = (text, size, color)
    if k in _cache: return _cache[k]
    f = ImageFont.truetype(FONT, size); tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    lines = text.split('\n'); tw = max(tmp.textlength(s, font=f) for s in lines); lh = int(size * 1.18)
    pw, ph = int(tw + size * 1.1), int(lh * len(lines) + size * 0.5)
    im = Image.new('RGBA', (pw + 40, ph + 40), (0, 0, 0, 0)); sh = Image.new('RGBA', im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((20, 28, 20 + pw, 28 + ph), int(ph * 0.3), fill=(0, 0, 0, 90))
    im = Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)), im); d = ImageDraw.Draw(im)
    d.rounded_rectangle((20, 20, 20 + pw, 20 + ph), int(min(ph * 0.3, 40)), fill=CREAM + (245,), outline=INK, width=5)
    for i, s in enumerate(lines):
        d.text((20 + pw / 2, 20 + size * 0.25 + i * lh + lh / 2), s, font=f, fill=color, anchor='mm')
    _cache[k] = im; return im

def paste(fr, im, cx, cy, scale=1.0, alpha=1.0):
    if alpha <= 0.01 or scale <= 0.02: return
    if abs(scale - 1) > 0.01: im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if alpha < 0.99: a = im.getchannel('A').point(lambda v: int(v * alpha)); im = im.copy(); im.putalpha(a)
    fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))

def pop(x):
    x = max(0, min(1, x)); c = 1.4
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2

# ---------- сборка ----------
def main():
    shots, total = plan()
    if '--plan' in sys.argv:
        for i, s in enumerate(shots): print(f"{i:3d} {s['t']:7.2f} {s['d']:5.2f}с {s['line']} {s['name']:8s} off={s['off']:.2f}")
        print('итого', round(total, 1)); return
    arg = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
    a = float(arg('--from', 0.0)); b = float(arg('--to', total))
    out = P(arg('--out', 'final.mp4')); seg = arg('--seg')
    os.makedirs(P('work'), exist_ok=True)
    if '--parallel' in sys.argv and not seg:
        return parallel(shots, total, int(arg('--parallel')), out)
    # звук
    n = int(total * SR) + SR; voice = np.zeros(n, np.float32)
    for lid, _ in LINES:
        v = vo_line(lid); s0 = int(LT[lid][1] * SR); voice[s0:s0 + len(v)] += v[:max(0, n - s0)]
    ovs = []
    for ov in OVERLAYS:
        st = LT[ov['line']][0] + ov.get('at', 0.3)
        en = st + ov['dur'] if 'dur' in ov else LT[ov.get('to', ov['line'])][2] - 0.2 + ov.get('extra', 0)
        ovs.append((st, en, ov))
    mix = voice.copy()
    if MUSIC:
        m = read_audio(P(MUSIC['file']), trim=False); m = np.tile(m, int(math.ceil(n / len(m))))[:n]
        k = int(SR * 0.3); cs = np.concatenate([[0.0], np.cumsum(np.abs(voice), dtype=np.float64)])
        idx = np.arange(n); env = ((cs[np.clip(idx - k // 2 + k, 0, n)] - cs[np.clip(idx - k // 2, 0, n)]) / k).astype(np.float32)
        duck = 1 - 0.65 * np.clip(env / 0.03, 0, 1)
        fade = np.ones(n, np.float32); fade[-SR * 2:] = np.linspace(1, 0, SR * 2); fade[:SR // 2] = np.linspace(0, 1, SR // 2)
        mix += m * MUSIC.get('gain', 0.14) * duck * fade
    if not seg:
        pcm = (np.clip(mix[int(a * SR):int(b * SR)] * 0.92, -1, 1) * 32767).astype(np.int16)
        wav = P('work/mix.wav')
        with wave.open(wav, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
        if '--audio-only' in sys.argv: return
    # видео
    vid = P(seg) if seg else P('work/video.mp4')
    enc = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', vid], stdin=subprocess.PIPE)
    srcs = {}; si = 0
    for fn in range(int(round(a * FPS)), int(round(b * FPS))):
        t = fn / FPS
        while si < len(shots) - 1 and t >= shots[si + 1]['t']: si += 1
        s = shots[si]
        for j in list(srcs):
            if j < si - 1 or (j == si - 1 and t > s['t'] + XF): srcs.pop(j).close()
        if si not in srcs:
            srcs[si] = source(s)
            srcs[si].skip(int(round((t - s['t']) * FPS)))
        cur = srcs[si].next()
        if si - 1 in srcs and t - s['t'] < XF and not s.get('cont'):
            prev = srcs[si - 1].next(); k = ease((t - s['t']) / XF)
            if prev is not None and cur is not None: cur = (prev.astype(np.float32) * (1 - k) + cur.astype(np.float32) * k).astype(np.uint8)
        fr = Image.fromarray(cur).convert('RGBA')
        for st, en, ov in ovs:
            if st <= t < en: gfx.draw(fr, ov, t - st, en - st)
        for lab in LABELS.get(s['name'], []):
            if lab.get('line') and lab['line'] != s['line']: continue
            t0 = s['t'] + lab.get('at', 0.4); t1 = s['t'] + lab.get('until', s['d'] - 0.2)
            if not (t0 <= t < t1): continue
            paste(fr, plate(lab['text'], lab.get('size', 60), tuple(lab.get('color', INK))), lab.get('x', W / 2), lab.get('y', 980),
                  pop((t - t0) / 0.35), min(1, (t1 - t) / 0.2))
        enc.stdin.write(fr.convert('RGB').tobytes())
        if fn % 300 == 0: print(f'{t:6.1f} / {b:.1f} с', flush=True)
    enc.stdin.close(); enc.wait()
    for x in srcs.values(): x.close()
    if seg: print('сегмент готов', seg, flush=True); return
    subprocess.run([FF, '-v', 'error', '-y', '-i', vid, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-af', 'loudnorm=I=-15:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a', '192k', '-ar', str(SR), '-movflags', '+faststart', '-shortest', out], check=True)
    print('готово:', out, round(b - a, 1), 'с')

def loudnorm2(wav, I=-14, TP=-1.5, LRA=11):
    """Двухпроходная нормализация: однопроходный loudnorm на голосе Silero недотягивал (−16,8 LUFS вместо −14)."""
    import json as _j, re as _r
    pre = 'acompressor=threshold=0.05:ratio=3:attack=5:release=120:makeup=2.5,alimiter=limit=0.7:attack=3:release=60:level=false,'
    err = subprocess.run([FF, '-hide_banner', '-i', wav, '-af', pre + f'loudnorm=I={I}:TP={TP}:LRA={LRA}:print_format=json', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    m = _j.loads(_r.findall(r'\{[^{}]*\}', err)[-1])
    return pre + (f"loudnorm=I={I}:TP={TP}:LRA={LRA}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
            f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")

def parallel(shots, total, N, out):
    """Видео — N процессами по кускам (границы в серединах планов, не на склейках), звук — целиком, громкость — в конце."""
    nf = int(round(total * FPS)); cuts = [0]
    for i in range(1, N):
        target = total * i / N
        s = min(shots, key=lambda s: abs(s['t'] + s['d'] / 2 - target))
        cuts.append(int(round((s['t'] + s['d'] / 2) * FPS)))
    cuts.append(nf)
    subprocess.run([sys.executable, P('cut.py'), '--audio-only'], check=True)
    procs = []
    for i in range(N):
        a, b = cuts[i] / FPS, cuts[i + 1] / FPS
        procs.append(subprocess.Popen([sys.executable, P('cut.py'), '--seg', f'work/seg{i}.mp4', '--from', f'{a:.6f}', '--to', f'{b:.6f}'],
                                      stdout=open(P(f'work/seg{i}.log'), 'w'), stderr=subprocess.STDOUT))
    for p in procs: p.wait()
    assert all(p.returncode == 0 for p in procs), 'сегмент упал — см. work/seg*.log'
    with open(P('work/segs.txt'), 'w') as f:
        for i in range(N): f.write(f"file 'seg{i}.mp4'\n")
    subprocess.run([FF, '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', P('work/segs.txt'), '-i', P('work/mix.wav'),
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-af', loudnorm2(P('work/mix.wav')), '-c:a', 'aac', '-b:a', '192k',
                    '-ar', str(SR), '-movflags', '+faststart', '-shortest', out], check=True)
    print('готово:', out, round(total, 1), 'с')

if __name__ == '__main__':
    main()
