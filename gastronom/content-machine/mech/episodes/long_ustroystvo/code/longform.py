#!/usr/bin/env python3
"""Сборка длинного ролика 16:9: потоковое чтение клипов (без загрузки в память), подписи-плашки,
мягкие склейки, голос + музыка с приглушением, громкость −14 LUFS.

    python3 longform.py [--plan] [--from N --to M]   (секунды, для пробного куска)
"""
import json, math, os, subprocess, sys
import numpy as np
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FF = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS, SR = 1920, 1080, 30, 44100
TEMPO = 1.07; LEAD = 0.15; XF = 0.25
FONT = '/home/user/gastronom/content-machine/video/fonts/Nunito-Black.ttf'
INK = (43, 33, 24); CREAM = (255, 248, 232); ORANGE = (236, 122, 32); RED = (222, 56, 44); BLUE = (48, 78, 136)
HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda p: os.path.join(HERE, p)

from shotmap_long import SHOTS, CLIPS, LABELS

# ---------------- звук ----------------
def read_audio(path, tempo=1.0, trim=True):
    af = []
    if trim: af.append('silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse')
    if tempo != 1.0: af.append(f'atempo={tempo}')
    raw = subprocess.run([FF, '-v', 'error', '-i', path, *(['-af', ','.join(af)] if af else []), '-f', 's16le', '-ac', '1',
                          '-ar', str(SR), '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768

# ---------------- раскладка ----------------
def plan():
    L = json.load(open(P('lines.json')))
    t = 0.0; shots = []; used = {}
    for l in L:
        T = l['T']; ws = SHOTS[l['id']]; tot = sum(w for _, w in ws); st = t
        for name, w in ws:
            d = T * w / tot
            shots.append(dict(name=name, line=l['id'], t=st, d=d, off=used.get(name, 0.0)))
            used[name] = used.get(name, 0.0) + d; st += d
        l['t0'] = t; t += T
    # скорость клипа: растягиваем, только если исходника не хватает
    for s in shots:
        c = CLIPS[s['name']]; avail = c.get('to', 999) - c.get('ss', 0)
        if avail >= 998:
            avail = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', P(c['file'])],
                                         capture_output=True, text=True).stdout or 0) - c.get('ss', 0)
        need = used[s['name']] + XF
        s['speed'] = 1.0 if c.get('loop') else (min(1.0, avail / need) if need > 0 else 1.0)
        s['avail'] = avail
    return L, shots, t

# ---------------- источники кадров ----------------
class Src:
    def __init__(self, shot):
        c = CLIPS[shot['name']]; sp = shot['speed']
        ss = c.get('ss', 0) + shot['off'] * sp
        loop = []
        if c.get('loop'):  # клип с привязкой конец=начало крутим по кругу
            dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', P(c['file'])],
                                       capture_output=True, text=True).stdout)
            ss = ss % (dur - 0.05); loop = ['-stream_loop', '-1']
        self.n = W * H * 3; self.last = None
        vf = f'setpts=(PTS-STARTPTS)/{sp},fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}'
        if c.get('up', True): vf += ',unsharp=5:5:0.5'
        self.p = subprocess.Popen([FF, '-v', 'error', *loop, '-ss', f'{ss:.3f}', '-i', P(c['file']), '-vf', vf, '-f', 'rawvideo',
                                   '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    def next(self):
        b = self.p.stdout.read(self.n)
        if len(b) == self.n: self.last = np.frombuffer(b, np.uint8).reshape(H, W, 3)
        return self.last
    def close(self):
        try: self.p.kill()
        except Exception: pass

# ---------------- плашки ----------------
_cache = {}
def plate(text, size=64, color=INK):
    k = (text, size, color)
    if k in _cache: return _cache[k]
    f = ImageFont.truetype(FONT, size)
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    lines = text.split('\n'); tw = max(tmp.textlength(s, font=f) for s in lines); lh = int(size * 1.18)
    pw, ph = int(tw + size * 1.1), int(lh * len(lines) + size * 0.5)
    im = Image.new('RGBA', (pw + 40, ph + 40), (0, 0, 0, 0))
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((20, 28, 20 + pw, 28 + ph), int(ph * 0.3), fill=(0, 0, 0, 90))
    im = Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)), im)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((20, 20, 20 + pw, 20 + ph), int(min(ph * 0.3, 40)), fill=CREAM + (250,), outline=INK, width=6)
    for i, s in enumerate(lines):
        d.text((20 + pw / 2, 20 + size * 0.25 + i * lh + lh / 2), s, font=f, fill=color, anchor='mm')
    _cache[k] = im
    return im

def paste(fr, im, cx, cy, scale=1.0, alpha=1.0):
    if alpha <= 0.01 or scale <= 0.02: return
    if abs(scale - 1) > 0.01: im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if alpha < 0.99:
        a = im.getchannel('A').point(lambda v: int(v * alpha)); im = im.copy(); im.putalpha(a)
    fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))

def pop(x):
    x = max(0, min(1, x)); c = 1.7
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2

# ---------------- сборка ----------------
def main():
    L, shots, total = plan()
    if '--plan' in sys.argv:
        for i, s in enumerate(shots):
            flag = ' ⚠ медленно' if s['speed'] < 0.8 else ''
            print(f"{i:3d} {s['t']:7.2f} {s['d']:5.2f}с {s['name']:6s} off={s['off']:5.2f} speed={s['speed']:.2f}{flag}")
        print('итого', round(total, 1)); return
    a = float(sys.argv[sys.argv.index('--from') + 1]) if '--from' in sys.argv else 0.0
    b = float(sys.argv[sys.argv.index('--to') + 1]) if '--to' in sys.argv else total
    out = P(sys.argv[sys.argv.index('--out') + 1]) if '--out' in sys.argv else P('long_ustroystvo.mp4')
    work = P('work'); os.makedirs(work, exist_ok=True)
    # звук
    n = int(total * SR) + SR
    voice = np.zeros(n, np.float32)
    for l in L:
        v = read_audio(P(f"vo_final/{l['id']}.mp3"), TEMPO)
        s0 = int((l['t0'] + LEAD) * SR); voice[s0:s0 + len(v)] += v[:max(0, n - s0)]
    mix = voice.copy()
    mus = CLIPS.get('_music')
    if mus:
        m = read_audio(P(mus['file']), trim=False)
        reps = int(math.ceil(n / len(m))); m = np.tile(m, reps)[:n]
        k = int(SR * 0.25); cs = np.concatenate([[0.0], np.cumsum(np.abs(voice), dtype=np.float64)])
        idx = np.arange(n); lo = np.clip(idx - k // 2, 0, n); hi = np.clip(idx - k // 2 + k, 0, n)
        env = ((cs[hi] - cs[lo]) / k).astype(np.float32)  # скользящее среднее (как convolve 'same'), но быстро
        duck = 1 - 0.6 * np.clip(env / 0.03, 0, 1)
        fade = np.ones(n); fo = int(SR * 2); fade[-fo:] = np.linspace(1, 0, fo); fade[:int(SR * 0.5)] = np.linspace(0, 1, int(SR * 0.5))
        mix += m * mus.get('gain', 0.16) * duck * fade
    sa, sb = int(a * SR), int(b * SR)
    pcm = (np.clip(mix[sa:sb] * 0.9, -1, 1) * 32767).astype(np.int16)
    wav = os.path.join(work, 'mix.wav')
    import wave
    with wave.open(wav, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    # видео
    vid = os.path.join(work, 'video.mp4')
    enc = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', vid], stdin=subprocess.PIPE)
    srcs = {}
    si = 0
    n0, n1 = int(round(a * FPS)), int(round(b * FPS))
    for fn in range(n0, n1):
        t = fn / FPS
        while si < len(shots) - 1 and t >= shots[si + 1]['t']: si += 1
        s = shots[si]
        for j in list(srcs):  # закрываем отработавшие источники
            if j < si - 1 or (j == si - 1 and t > shots[si]['t'] + XF): srcs.pop(j).close()
        if si not in srcs:
            srcs[si] = Src(s)
            # догоняем, если начали с середины плана (пробный кусок)
            for _ in range(int((t - s['t']) * FPS)): srcs[si].next()
        cur = srcs[si].next()
        if si - 1 in srcs and t - s['t'] < XF and CLIPS[s['name']].get('cut') is None:
            prev = srcs[si - 1].next()
            k = (t - s['t']) / XF
            if prev is not None and cur is not None:
                cur = (prev.astype(np.float32) * (1 - k) + cur.astype(np.float32) * k).astype(np.uint8)
        fr = Image.fromarray(cur if cur is not None else np.zeros((H, W, 3), np.uint8)).convert('RGBA')
        # плашки этого плана
        for lab in LABELS.get(s['name'], []):
            t0 = s['t'] + lab.get('at', 0.3) - (s['off'] if lab.get('abs') else 0)
            t1 = s['t'] + (lab['until'] if 'until' in lab else s['d'] - 0.15)
            if lab.get('line') and lab['line'] != s['line']: continue
            if not (t0 <= t < t1): continue
            q = t - t0; out_a = min(1, (t1 - t) / 0.15)
            paste(fr, plate(lab['text'], lab.get('size', 64), tuple(lab.get('color', INK))), lab.get('x', W / 2), lab.get('y', 110),
                  pop(q / 0.3), out_a)
        enc.stdin.write(fr.convert('RGB').tobytes())
        if fn % 300 == 0: print(f'{t:6.1f} / {b:.1f} с', flush=True)
    enc.stdin.close(); enc.wait()
    for x in srcs.values(): x.close()
    subprocess.run([FF, '-v', 'error', '-y', '-i', vid, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a', '192k', '-ar', str(SR),
                    '-movflags', '+faststart', '-shortest', out], check=True)
    print('готово:', out, round(b - a, 1), 'с')

if __name__ == '__main__':
    main()
