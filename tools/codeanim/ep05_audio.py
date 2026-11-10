"""Episode 5 soundtrack, all synthesized (no samples, no credits): music bed, party music, SFX, narration placement, ducking.

usage: python3 ep05_audio.py VO_DIR OUT.wav
VO_DIR holds the narration lines (vo_01.wav ... see CUES). Scene times match ep05.js.
"""
import sys, os, numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt, resample_poly

SR = 48000
DUR = {'01': 6.2, '02': 4.2, '03': 10.6, '04': 5.4, '05': 3.8, '06': 8.0, '07': 5.6, '08': 5.0, '09': 5.4, '10': 4.2, '11': 4.4, '12': 6.8, '13': 6.2}
START, acc = {}, 0.0
for k, d in DUR.items(): START[k] = acc; acc += d
TOTAL = acc
rng = np.random.default_rng(5)
N = lambda s: int(round(s * SR))
tt = lambda d: np.arange(N(d)) / SR

def filt(x, kind, f, order=2):
    f = np.atleast_1d(f); sos = butter(order, f / (SR / 2) if len(f) > 1 else f[0] / (SR / 2), btype=kind, output='sos'); return sosfilt(sos, x)
def noise(d): return rng.standard_normal(N(d))
def expd(d, tau): return np.exp(-tt(d) / tau)
def att(x, a=.004):
    n = min(len(x), N(a)); x = x.copy(); x[:n] *= np.linspace(0, 1, n); return x
def fade(x, a=.005, b=.02):
    x = att(x, a); n = min(len(x), N(b)); x[-n:] *= np.linspace(1, 0, n); return x
def sweep(f0, f1, d, curve=1.0):
    u = np.linspace(0, 1, N(d)) ** curve; f = f0 + (f1 - f0) * u; return np.sin(2 * np.pi * np.cumsum(f) / SR)
def norm(x, peak=1.0): m = np.max(np.abs(x)) or 1; return x / m * peak

# ---------------- sound effects ----------------
def snap():
    d = .09; x = filt(noise(d), 'bandpass', [1800, 7000]) * expd(d, .012) + .6 * np.sin(2 * np.pi * 2300 * tt(d)) * expd(d, .008)
    return norm(att(x, .0005), .9)
def glass():
    d = 1.6; x = filt(noise(d), 'highpass', 1500) * expd(d, .12) * .8 + filt(noise(d), 'lowpass', 600) * expd(d, .05) * .6
    for _ in range(26):
        t0 = rng.uniform(0, .9); f = rng.uniform(2500, 7500); n0 = N(t0); seg = tt(d - t0)
        x[n0:] += np.sin(2 * np.pi * f * seg) * np.exp(-seg / rng.uniform(.03, .12)) * rng.uniform(.15, .4)
    return norm(att(x, .001), .95)
def whoosh(d=.45, f0=300, f1=2500):
    x = noise(d); u = np.linspace(0, 1, len(x)); out = np.zeros_like(x); y = 0.0
    fc = f0 + (f1 - f0) * np.sin(u * np.pi / 2); a = 1 - np.exp(-2 * np.pi * fc / SR)
    for i in range(len(x)): y += a[i] * (x[i] - y); out[i] = y
    return norm(out * np.sin(u * np.pi) ** 1.5, .6)
def clank(p=1.0, d=.7):
    x = sum(np.sin(2 * np.pi * f * p * tt(d)) * expd(d, tau) * g for f, tau, g in [(310, .35, 1), (797, .25, .7), (1243, .18, .55), (1905, .12, .4), (2620, .08, .3)])
    x += filt(noise(d), 'bandpass', [800, 5000]) * expd(d, .01) * 1.5
    return norm(att(x, .0008), .85)
def toaster_pop():
    d = .5; x = filt(noise(d), 'bandpass', [1500, 6000]) * expd(d, .006) * 2 + np.sin(2 * np.pi * (380 + 40 * np.sin(2 * np.pi * 18 * tt(d))) * tt(d)) * expd(d, .12) * .5
    return norm(att(x, .0005), .7)
def plop(): d = .25; return norm(sweep(260, 950, d, .5) * expd(d, .05), .7)
def slurp():
    d = .9; x = filt(noise(d), 'bandpass', [400, 2500]) * (0.5 + .5 * np.sin(2 * np.pi * 23 * tt(d))) ** 2
    return norm(fade(x * np.sin(np.linspace(0, np.pi, len(x))), .05, .15), .45)
def tape_rip(d=.9):
    imp = (rng.random(N(d)) < .02) * rng.uniform(.3, 1, N(d)); x = filt(imp + .15 * noise(d), 'bandpass', [900, 5000])
    return norm(fade(x * np.linspace(1, .6, len(x)), .01, .08), .5)
def pop():
    d = .18; return norm(sweep(500, 1300, d, .4) * expd(d, .04) + filt(noise(d), 'highpass', 3000) * expd(d, .004), .55)
def tick(): d = .06; return norm(np.sin(2 * np.pi * 1900 * tt(d)) * expd(d, .012), .4)
def thunk(): d = .2; return norm(np.sin(2 * np.pi * 150 * tt(d)) * expd(d, .05) + .3 * filt(noise(d), 'lowpass', 1200) * expd(d, .015), .6)
def hiss(d=.7): return norm(fade(filt(noise(d), 'highpass', 2500) * np.linspace(1, .2, N(d)), .02, .2), .35)
def engine(d, a0, a1):
    t = tt(d); f = 46 + 6 * np.sin(2 * np.pi * .3 * t); ph = 2 * np.pi * np.cumsum(f) / SR
    x = sum(np.sin(ph * h) / h for h in range(1, 7)) + .4 * filt(noise(d), 'lowpass', 400)
    return filt(x, 'lowpass', 900) / 3 * np.linspace(a0, a1, N(d))
def power_down():
    d = .9; return norm(sweep(240, 30, d, .6) * np.linspace(1, 0, N(d)), .6)
def power_up():
    d = 1.0; x = sweep(70, 520, d, .7) * np.linspace(0, 1, N(d)) ** .6 + .3 * sweep(140, 1040, d, .7) * np.linspace(0, 1, N(d))
    return norm(fade(x, .05, .1), .5)
def hum(d, a=1.0):
    t = tt(d); x = (np.sin(2 * np.pi * 110 * t) + .4 * np.sin(2 * np.pi * 220 * t) + .15 * np.sin(2 * np.pi * 330 * t)) * (1 + .15 * np.sin(2 * np.pi * .35 * t))
    return fade(x / 1.6 * a, .4, .4)
def blow(): d = .7; return norm(fade(filt(noise(d), 'bandpass', [300, 1800]) * np.sin(np.linspace(0, np.pi, N(d))) ** .7, .05, .2), .5)
def horn():
    d = .7; t = tt(d); f = 470 + 25 * np.minimum(t / .1, 1) + 8 * np.sin(2 * np.pi * 7 * t); ph = 2 * np.pi * np.cumsum(f) / SR
    x = sum(np.sin(ph * h) / h for h in range(1, 12)); return norm(fade(filt(x, 'lowpass', 3500), .02, .1), .4)
def click(): d = .03; return norm(filt(noise(d), 'bandpass', [1000, 6000]) * expd(d, .004), .5)
def crickets(d):
    x = np.zeros(N(d)); t0 = .2
    while t0 < d - .3:
        for k in range(3):
            n0 = N(t0 + k * .06); seg = tt(.04); x[n0:n0 + len(seg)] += np.sin(2 * np.pi * 4600 * seg) * np.sin(np.linspace(0, np.pi, len(seg)))
        t0 += rng.uniform(.6, 1.1)
    return x * .12
def birds(d):
    x = np.zeros(N(d)); t0 = .3
    while t0 < d - .4:
        for k in range(rng.integers(2, 4)):
            f0 = rng.uniform(2800, 4200); seg = sweep(f0, f0 * rng.uniform(1.2, 1.5), .08) * np.sin(np.linspace(0, np.pi, N(.08))); n0 = N(t0 + k * .11); x[n0:n0 + len(seg)] += seg
        t0 += rng.uniform(1.0, 1.8)
    return x * .1
def ambience(d, lp=500, a=.05): return fade(filt(noise(d), 'lowpass', lp) * a, .3, .3)

# ---------------- music ----------------
def ep_note(f, d, g=1.0):
    t = tt(d); x = (np.sin(2 * np.pi * f * t) + .25 * np.sin(4 * np.pi * f * t) * np.exp(-t / .3) + .08 * np.sin(6 * np.pi * f * t) * np.exp(-t / .15))
    return att(x * np.exp(-t / 1.2) * g * (1 + .08 * np.sin(2 * np.pi * 5 * t)), .008)
def midi(m): return 440 * 2 ** ((m - 69) / 12)
def bed(d):
    """soft lo-fi bed, 92 bpm: electric piano chords, sub bass, soft kick and shaker"""
    out = np.zeros(N(d) + SR * 3); beat = 60 / 92
    prog = [[48, 52, 55, 59], [45, 48, 52, 55], [41, 45, 48, 52], [43, 47, 50, 53]]
    mel = [72, 74, 76, 79, 81]; b, i = 0.0, 0
    while b < d:
        ch = prog[(i // 4) % 4]; n0 = N(b)
        if i % 4 == 0:
            for m in ch[1:]: seg = ep_note(midi(m + 12), beat * 4, .22); out[n0:n0 + len(seg)] += seg
            seg = np.sin(2 * np.pi * midi(ch[0] - 12) * tt(beat * 2)) * np.exp(-tt(beat * 2) / .6) * .5; out[n0:n0 + len(seg)] += att(seg, .01)
        if i % 4 == 2:
            seg = np.sin(2 * np.pi * midi(ch[0] - 12) * tt(beat * 2)) * np.exp(-tt(beat * 2) / .6) * .4; out[n0:n0 + len(seg)] += att(seg, .01)
        if i % 2 == 0: seg = sweep(110, 45, .25, .3) * expd(.25, .08) * .5; out[n0:n0 + len(seg)] += seg
        for h in (0, .5):
            m0 = N(b + h * beat); seg = filt(noise(.05), 'highpass', 6000) * expd(.05, .012) * (.08 if h else .05); out[m0:m0 + len(seg)] += seg
        if rng.random() < .45:
            seg = ep_note(midi(rng.choice(mel)), beat * 2, .12); m0 = N(b + rng.choice([0, .5]) * beat); out[m0:m0 + len(seg)] += seg
        b += beat; i += 1
    return filt(out[:N(d)], 'lowpass', 5000)
def saw(f, d):
    t = tt(d); return sum(np.sin(2 * np.pi * f * h * t) / h for h in range(1, 14))
def party(d, offset=.25, bright=1.0):
    """party track, 120 bpm, beats at offset + k*0.5 s (matches the bounce in ep05.js)"""
    out = np.zeros(N(d) + SR * 2); beat = .5
    prog = [57, 53, 48, 55]; b, i = offset - beat * int(offset / beat + 1), 0
    while b < d:
        if b >= 0:
            n0 = N(b); ch = prog[(i // 4) % 4]
            k = sweep(150, 42, .28, .25) * expd(.28, .1); out[n0:n0 + len(k)] += k * .9
            if i % 2 == 1:
                c = sum(np.roll(filt(noise(.12), 'bandpass', [900, 2500]) * expd(.12, .02), N(j * .012)) for j in range(3)); out[n0:n0 + len(c)] += c * .35
            for h in (.5,):
                m0 = N(b + h * beat); hh = filt(noise(.06), 'highpass', 7000) * expd(.06, .015) * .25; out[m0:m0 + len(hh)] += hh
                st = sum(saw(midi(m), .18) for m in (ch + 12, ch + 16 if ch in (48, 53) else ch + 15, ch + 19)) * expd(.18, .07) * .06
                out[m0:m0 + len(st)] += filt(st, 'lowpass', 2500 * bright)
            for h, o in ((0, 0), (.5, 12)):
                m0 = N(b + h * beat); bs = saw(midi(ch - 24 + o), .22) * expd(.22, .1) * .18; out[m0:m0 + len(bs)] += filt(bs, 'lowpass', 700)
        b += beat; i += 1
    return out[:N(d)]
def tape_stop(x, d=.6):
    """last part of x slows to a halt"""
    n = N(d); seg = x[-n:]; u = np.linspace(0, 1, n); rate = (1 - u) ** 1.5; pos = np.cumsum(rate); pos = pos / pos[-1] * (n * .45)
    y = np.interp(pos, np.arange(n), seg) * (1 - u) ** .5; return np.concatenate([x[:-n], y])

# ---------------- timeline ----------------
L = {k: np.zeros(N(TOTAL) + SR * 3) for k in ('vo', 'sfx', 'mus', 'amb')}
def put(layer, t, x, g=1.0):
    n0 = N(t); n1 = min(n0 + len(x), len(L[layer])); L[layer][n0:n1] += x[:n1 - n0] * g
def S(sc, t): return START[sc] + t

vo_dir, out = sys.argv[1], sys.argv[2]
def vo(sc, t, name, g=1.0):
    sr, x = wavfile.read(os.path.join(vo_dir, name)); x = x.astype(np.float64); x = x.mean(1) if x.ndim > 1 else x
    if sr != SR: x = resample_poly(x, SR, sr)
    x = x / (np.max(np.abs(x)) or 1) * .8; put('vo', S(sc, t), x, g); return len(x) / SR

# narration (times line up with the action in ep05.js)
VO = [('01', .3, 'vo_01.wav'), ('02', .6, 'vo_02.wav'), ('03', .2, 'vo_03a.wav'), ('03', 7.8, 'vo_03b.wav'), ('04', .4, 'vo_04.wav'), ('05', .5, 'vo_05.wav'),
      ('06', .3, 'vo_06a.wav'), ('06', 5.6, 'vo_06b.wav'), ('07', .4, 'vo_08.wav'), ('08', .5, 'vo_09.wav'), ('09', .3, 'vo_10.wav'), ('10', .8, 'vo_11.wav'),
      ('11', .5, 'vo_12.wav'), ('12', 3.4, 'vo_13.wav'), ('13', .4, 'vo_14a.wav'), ('13', 1.9, 'vo_14b.wav')]
for sc, t, f in VO:
    if not os.path.exists(os.path.join(vo_dir, f)): print('MISSING', f); continue
    d = vo(sc, t, f); print(f'{f:12s} scene {sc} at {t:4.1f}s  ends {t + d:4.1f}s / {DUR[sc]}s' + ('  OVER' if t + d > DUR[sc] + .2 else ''))

# music
put('mus', 0, fade(bed(START['08']), 1.5, 1.2), .55)
put('mus', S('06', 0), filt(party(2.75, .1, .7), 'bandpass', [1200, 5000]) * np.r_[np.ones(N(2.6)), np.linspace(1, 0, N(.15))], .35)   # headphone leak
m = party(START['10'] - START['08'] + .45, .25); m = tape_stop(m, .5); put('mus', S('08', 0), fade(m, .3, .01), .7)
put('mus', S('12', 2.5), fade(party(DUR['12'] - 2.5 + DUR['13'], .25 - 2.5 % .5), .05, 1.0), .5)
put('mus', S('13', DUR['13']), fade(bed(4.0), .5, 2.5), .5)

# ambience
put('amb', S('01', 0), crickets(DUR['01']) + ambience(DUR['01'], 300, .03)); put('amb', S('01', 0), hum(DUR['01'], .05))
put('amb', S('02', 0), birds(DUR['02']) + ambience(DUR['02'], 400, .03)); put('amb', S('02', 0), hum(DUR['02'], .07))
put('amb', S('03', 0), ambience(DUR['03'] + DUR['04'] * 0, 400, .025)); put('amb', S('05', 0), ambience(DUR['05'], 400, .025))
put('amb', S('06', 0), ambience(DUR['06'], 700, .07) + birds(DUR['06']) * .6)
put('amb', S('08', 0), ambience(DUR['08'] + DUR['09'] + DUR['10'] + DUR['11'] + DUR['12'] + DUR['13'], 500, .03))

# sfx
fx = lambda sc, t, x, g=1.0: put('sfx', S(sc, t), x, g)
fx('01', 3.0, whoosh(.5, 200, 900), .25)                       # blanket shift on waking
fx('03', 1.22, snap()); fx('03', 1.6, glass(), .9)
for k, d in [('legL', 0), ('legR', .12), ('chest', .28), ('armL', .44), ('armR', .56), ('helmet', .72)]:
    fx('03', 1.7 + d, whoosh(.4), .4); fx('03', 1.7 + d + .42, clank(1 + d * .3), .55)
fx('03', 1.75, toaster_pop(), .7); fx('03', 2.6, plop(), .8); fx('03', 8.45, slurp(), .9)
fx('04', .3, pop()); fx('04', 2.0, pop(), .8); fx('04', 2.9, pop(), 1.0); fx('04', 3.4, tick(), 1.2)
fx('05', .3, pop(), .7)
for i in range(3): fx('05', .3 + i * 1.03, tape_rip(.95), .8)
fx('06', 0, engine(1.7, .8, .5), .5); fx('06', 1.5, hiss(.6), .6); fx('06', 1.75, hiss(.4), .4)
fx('06', 1.6, engine(3.4, .35, .35), .5); fx('06', 2.1, snap()); fx('06', 2.6, snap())
for k, d in [('legL', 0), ('legR', .12), ('chest', .28), ('armL', .44), ('armR', .56), ('helmet', .72)]:
    fx('06', 2.7 + d, whoosh(.4, 600, 3000), .35); fx('06', 2.7 + d + .42, clank(1.1 + d * .3), .5)
fx('06', 3.85, clank(.8, 1.0), .8); fx('06', 4.6, hiss(.5), .5); fx('06', 5.0, engine(2.6, .5, .0) * np.linspace(1, .2, N(2.6)), .7)
fx('07', .3, pop()); fx('07', 1.5, pop())
for k in range(1, 8): fx('07', .4 + k / 7 * 1.0, tick())
for k in range(1, 5): fx('07', 1.6 + k / 4 * .8, tick())
for i in range(4): fx('07', 3.2 + i * .25, thunk())
for k in range(3): fx('09', .75 + k * .5, snap(), .6)
for k in range(9): fx('09', .75 + 1.5 + k * .5, snap(), .5); fx('09', .87 + 1.5 + k * .5, snap(), .35)
fx('10', .3, power_down(), .8); fx('10', .3, click(), .8)
fx('11', 2.72, snap(), 1.0)
fx('12', .15, glass(), .9)
for k, d in [('legL', 0), ('legR', .12), ('chest', .28), ('armL', .44), ('armR', .56), ('helmet', .72)]:
    fx('12', .4 + d, whoosh(.4), .35); fx('12', .4 + d + .42, clank(1 + d * .3), .5)
fx('12', 1.3, power_up(), .7); put('amb', S('12', 1.6), hum(DUR['12'] - 1.6 + DUR['13'], .05)); fx('12', 2.4, click(), .8); fx('12', 2.42, thunk(), .9)
fx('13', 2.75, blow(), 1.0); fx('13', 3.35, horn(), .7); fx('13', 4.75, slurp(), .9)

# ducking: music/ambience/sfx dip under the narration
v = L['vo']; env = np.convolve(np.abs(v), np.ones(N(.05)) / N(.05), 'same'); env = np.minimum(env / .05, 1)
sm = np.zeros_like(env); a_up, a_dn = 1 - np.exp(-1 / (SR * .03)), 1 - np.exp(-1 / (SR * .35)); y = 0.0
for i in range(0, len(env), 48):           # 1 ms steps
    target = env[i]; y += ((a_up if target > y else a_dn) * 48) * (target - y); sm[i:i + 48] = y
mix = v * 1.0 + L['mus'] * (1 - .55 * sm) * .5 + L['amb'] * (1 - .4 * sm) + L['sfx'] * (1 - .35 * sm) * .8
mix = mix[:N(TOTAL)]
mix = mix / np.max(np.abs(mix)) * .89
wavfile.write(out, SR, (np.stack([mix, mix], 1) * 32767).astype(np.int16))
print('wrote', out, f'{TOTAL:.1f}s')
