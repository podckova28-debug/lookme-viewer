"""Episode 5 soundtrack, all synthesized (no samples, no credits): music bed, party music, SFX, narration placement, ducking.

usage: python3 ep05_audio.py VO_DIR OUT.wav
VO_DIR holds the narration lines (vo_01.wav ... see CUES). Scene times match ep05.js.
"""
import sys, os, numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt, resample_poly

SR = 48000
import re as _re
_HERE = os.path.dirname(os.path.abspath(__file__)); _src = open(os.path.join(_HERE, 'ep05.js')).read() + open(os.path.join(_HERE, 'ep05b.js')).read()
DUR = {m[0]: float(m[1]) for m in _re.findall(r"\{ id: '(\w+)', dur: ([\d.]+)", _src)}
ORDER = _re.findall(r"'(\w+)'", _re.search(r"const ORDER = \[(.*?)\]", _src).group(1))
START, acc = {}, 0.0
for k in ORDER: START[k] = acc; acc += round(DUR[k] * 24) / 24      # scenes are whole frames
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

# narration (times line up with the action in ep05.js / ep05b.js)
VO = [('01', .3, 'vo_01.wav'), ('02', .3, 'vo_02.wav'), ('N1', .3, 'vo_N1a.wav'), ('N1', 3.0, 'vo_N1b.wav'), ('N1', 5.0, 'vo_N1c.wav'),
      ('03', .2, 'vo_03a.wav'), ('03', 5.6, 'vo_03b.wav'), ('04', .4, 'vo_04.wav'), ('05', .5, 'vo_05.wav'), ('N2', .3, 'vo_N2.wav'),
      ('05b', .3, 'vo_05b_a.wav'), ('05b', 3.0, 'vo_05b_b.wav'), ('N12', .4, 'vo_N12.wav'), ('NB', .3, 'vo_NB.wav'), ('05c', .3, 'vo_05c_a.wav'), ('05c', 4.3, 'vo_05c_b.wav'),
      ('N10', .3, 'vo_N10a.wav'), ('N10', 3.4, 'vo_N10b.wav'), ('N10', 6.3, 'vo_N10c.wav'), ('N10', 9.25, 'vo_N10d.wav'),
      ('N20', .3, 'vo_N20a.wav'), ('N20', 4.5, 'vo_N20b.wav'),
      ('06', .3, 'vo_06_0.wav'), ('06', 3.6, 'vo_06a.wav'), ('06', 8.0, 'vo_06b.wav'), ('N3', .5, 'vo_N3a.wav'), ('N3', 6.0, 'vo_N3b.wav'),
      ('B', .3, 'vo_B1.wav'), ('B', 3.15, 'vo_B2.wav'), ('B', 5.6, 'vo_B3.wav'), ('B', 8.6, 'vo_B4.wav'),
      ('N23', .3, 'vo_N23a.wav'), ('N23', 3.0, 'vo_N23b.wav'), ('N4', .3, 'vo_N4a.wav'), ('N4', 3.6, 'vo_N4b.wav'), ('N13', .3, 'vo_N13a.wav'), ('N13', 4.2, 'vo_N13b.wav'),
      ('06c', 1.0, 'vo_06c.wav'), ('07', .4, 'vo_08v2.wav'), ('NW', .3, 'vo_NWa.wav'), ('NW', 3.6, 'vo_NWb.wav'), ('NE', .3, 'vo_NEa.wav'), ('NE', 2.4, 'vo_NEb.wav'),
      ('N7', .3, 'vo_N7a.wav'), ('N7', 3.4, 'vo_N7b.wav'), ('N7', 6.6, 'vo_N7c.wav'), ('08', .4, 'vo_09v2.wav'), ('09', .3, 'vo_10.wav'), ('10', .8, 'vo_11.wav'),
      ('11', .5, 'vo_12.wav'), ('12', 2.9, 'vo_13.wav'), ('12b', .5, 'vo_12b.wav'), ('N8', .3, 'vo_N8a.wav'), ('N8', 5.4, 'vo_N8b.wav'), ('NK', .3, 'vo_NKa.wav'), ('NK', 3.2, 'vo_NKb.wav'),
      ('N17', .3, 'vo_N17a.wav'), ('N17', 3.0, 'vo_N17b.wav'), ('NX', .3, 'vo_NXa.wav'), ('NX', 2.6, 'vo_NXb.wav'), ('N9', .3, 'vo_N9a.wav'), ('N9', 2.8, 'vo_N9b.wav'),
      ('13', .2, 'vo_14a.wav'), ('13', 2.15, 'vo_14b.wav'), ('N19', .4, 'vo_N19a.wav'), ('N19', 3.4, 'vo_N19b.wav'), ('14', .4, 'vo_15a.wav'), ('14', 7.1, 'vo_15b.wav')]
for sc, t, f in VO:
    if not os.path.exists(os.path.join(vo_dir, f)): print('MISSING', f); continue
    d = vo(sc, t, f); print(f'{f:13s} scene {sc:3s} at {t:4.1f}s  ends {t + d:4.1f}s / {DUR[sc]}s' + ('  OVER' if t + d > DUR[sc] + .2 else ''))

# extra sounds for the new scenes
def crinkle(d):
    imp = (rng.random(N(d)) < .006) * rng.uniform(.2, 1, N(d)); x = filt(imp, 'bandpass', [2000, 8000]) + .05 * filt(noise(d), 'highpass', 4000)
    return norm(fade(x, .02, .1), .35)
def puff_snd(): d = .35; return norm(fade(filt(noise(d), 'lowpass', 900) * expd(d, .08), .01, .1), .45)
def thup(): d = .12; return norm(filt(noise(d), 'lowpass', 500) * expd(d, .02) + .5 * np.sin(2 * np.pi * 120 * tt(d)) * expd(d, .03), .4)
def splat():
    d = .5; x = filt(noise(d), 'lowpass', 1500) * expd(d, .07) + .6 * sweep(300, 80, d, .5) * expd(d, .1); return norm(att(x, .001), .8)
def ding(f=1760): d = 1.2; t = tt(d); return norm((np.sin(2 * np.pi * f * t) + .4 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / .2)) * np.exp(-t / .5), .35)
def slide(d=1.0): return norm(fade(filt(noise(d), 'bandpass', [300, 1500]), .1, .2), .25)
ARMOR = [0, .12, .28, .44, .56, .72]

# music: calm bed through the day, headphone leak at the bus stop, party (from the guests' arrival), calm again at midnight
put('mus', 0, fade(bed(START['N7']), 1.5, 1.2), .55)
put('mus', S('06', 3.25), filt(party(2.75, .2 - 3.25 % .5, .7), 'bandpass', [1200, 5000]) * np.r_[np.ones(N(2.45)), np.linspace(1, 0, N(.3))], .35)
m = party(START['10'] - START['N7'] + .45, (START['09'] + .25 - START['N7']) % .5); m = tape_stop(m, .5); put('mus', S('N7', 0), fade(m, .6, .01), .6)
p_len = START['N19'] - S('12', 2.5); put('mus', S('12', 2.5), fade(party(p_len + .5, .25 - 2.5 % .5), .05, 1.0), .5)
put('mus', S('N19', .2), fade(bed(START['14'] - START['N19'] + DUR['14']), 2.0, 1.0), .45)

# ambience by location
LOC = {'01': 'night', '02': 'morning', 'N1': 'morning', 'N10': 'morning', '03': 'room', '05': 'room', '05b': 'room', '05c': 'room', 'N12': 'room', 'N20': 'room', '06c': 'room',
       '06': 'street', 'N4': 'street', 'B': 'shop', 'N13': 'shop', 'N23': 'cafe', 'N3': 'wind', 'N7': 'room', 'N19': 'night', '14': 'morning', 'NB': 'room', 'NW': 'room', 'NE': 'room', 'T0': 'night'}
for sc, kind in LOC.items():
    d = DUR[sc]
    if kind == 'night': put('amb', S(sc, 0), crickets(d) + ambience(d, 300, .03))
    elif kind == 'morning': put('amb', S(sc, 0), birds(d) + ambience(d, 400, .03))
    elif kind == 'room': put('amb', S(sc, 0), ambience(d, 400, .025))
    elif kind == 'street': put('amb', S(sc, 0), ambience(d, 700, .07) + birds(d) * .6)
    elif kind == 'shop': put('amb', S(sc, 0), ambience(d, 600, .035) + birds(d) * .2)
    elif kind == 'cafe': put('amb', S(sc, 0), ambience(d, 900, .05))
    elif kind == 'wind': put('amb', S(sc, 0), fade(filt(noise(d), 'bandpass', [200, 1200]) * (.6 + .4 * np.sin(2 * np.pi * .4 * tt(d))), .3, .3) * .12)
put('amb', S('01', 0), hum(DUR['01'], .05)); put('amb', S('02', 0), hum(DUR['02'], .07)); put('amb', S('N1', 0), hum(DUR['N1'], .07))
put('amb', S('08', 0), ambience(START['N19'] - START['08'], 500, .03))

# sfx
def fx(sc, t, x, g=1.0):
    if t < DUR[sc]: put('sfx', S(sc, t), x, g)      # nothing spills into the next scene
fx('01', 3.0, whoosh(.5, 200, 900), .25)                       # blanket shift on waking
fx('03', 1.22, snap()); fx('03', 1.6, glass(), .9)
for d in ARMOR: fx('03', 1.7 + d, whoosh(.4), .4); fx('03', 1.7 + d + .42, clank(1 + d * .3), .55)
fx('03', 1.75, toaster_pop(), .7); fx('03', 2.6, plop(), .8); fx('03', 2.62, splat()[:N(.25)] * .5, .6); fx('03', 6.25, slurp(), .9)
fx('04', .3, pop()); fx('04', 2.0, pop(), .8); fx('04', 2.9, pop(), 1.0); fx('04', 3.4, tick(), 1.2)
fx('05', .3, pop(), .7)
for i in range(3): fx('05', .3 + i * 1.03, tape_rip(.95), .8)
# 05b oven mitts
fx('05b', .45, whoosh(.4, 300, 1200), .25); fx('05b', 1.7, thup(), .9); fx('05b', 1.78, ding(2093), .5)
fx('05b', 3.05, puff_snd(), .9); fx('05b', 4.75, puff_snd(), 1.0); fx('05b', 5.9, pop(), .5)
# 05c present
fx('05c', .2, crinkle(3.2), .9); fx('05c', 3.9, whoosh(.25, 800, 4000), .4); fx('05c', 4.0, crinkle(.5), 1.0); fx('05c', 4.15, tape_rip(.3), .7); fx('05c', 4.3, tape_rip(.25), .7)
fx('05c', 4.55, pop(), .7); fx('05c', 4.6, ding(1568), .5)
# 06 bus stop
for k in range(7): fx('06', .2 + k * .393, thup(), .6)
fx('06', 2.85, whoosh(.5, 300, 1500), .3); fx('06', 3.5, thup(), .7); fx('06', 3.18, click(), .7)
fx('06', 3.4, engine(1.5, .8, .5), .5); fx('06', 4.8, hiss(.6), .6); fx('06', 4.95, hiss(.4), .4); fx('06', 4.9, engine(3.3, .35, .35), .5)
fx('06', 5.2, snap()); fx('06', 5.7, snap())
for d in ARMOR: fx('06', 5.9 + d, whoosh(.4, 600, 3000), .35); fx('06', 5.9 + d + .42, clank(1.1 + d * .3), .5)
fx('06', 6.85, clank(.8, 1.0), .8); fx('06', 7.3, hiss(.5), .5); fx('06', 7.6, engine(2.4, .5, .0) * np.linspace(1, .2, N(2.4)), .7)
# B bakery
fx('B', .3, slide(1.2)); fx('B', 1.5, thup(), .5)
for k in range(5): fx('B', 2.5 + k * .52, thup(), .6)
fx('B', 4.6, whoosh(.5, 300, 1600), .4); fx('B', 4.8, whoosh(.5, 400, 2200), .3); fx('B', 5.38, thunk(), .7); fx('B', 5.5, thup(), .6); fx('B', 5.62, thup(), .6)
fx('B', 6.88, snap()); fx('B', 6.95, power_up()[:N(.3)], .5); fx('B', 7.1, glass(), 1.0)
for d in ARMOR: fx('B', 7.25 + d, whoosh(.4), .35); fx('B', 7.25 + d + .42, clank(1 + d * .3), .55)
fx('B', 7.95, splat(), 1.0); fx('B', 8.4, pop(), .7)
# 06c Dave fixes the cake
for i in range(3): fx('06c', .6 + i, tape_rip(.95), .8)
fx('06c', 3.7, ding(2093), .5)
fx('07', .3, pop()); fx('07', 2.15, pop())
for k in range(1, 8): fx('07', .9 + k / 7.99 * 1.05, tick())
for k in range(1, 5): fx('07', 2.3 + k / 4.99 * .65, tick())
for i in range(4): fx('07', 3.75 + i * .2, thunk())
for k in range(3): fx('09', .75 + k * .5, snap(), .6)
for k in range(9): fx('09', .75 + 1.5 + k * .5, snap(), .5); fx('09', .87 + 1.5 + k * .5, snap(), .35)
fx('10', .3, power_down(), .8); fx('10', .3, click(), .8)
fx('11', 2.72, snap(), 1.0)
fx('12', .15, glass(), .9)
for d in ARMOR: fx('12', .4 + d, whoosh(.4), .35); fx('12', .4 + d + .42, clank(1 + d * .3), .5)
fx('12', 1.3, power_up(), .7); put('amb', S('12', 1.6), hum(START['13'] + DUR['13'] - S('12', 1.6), .05)); fx('12', 2.4, click(), .8); fx('12', 2.42, thunk(), .9)
fx('13', 3.35, blow(), 1.0); fx('13', 3.95, horn(), .7); fx('13', 5.15, slurp(), .9)
# new scenes
fx('N1', 2.55, puff_snd(), .9); fx('N1', 3.25, puff_snd(), .9); fx('N1', 4.9, power_up(), .5)
fx('N2', .2, pop(), .8)
for a in (1.3, 2.0, 2.7, 3.6): fx('N2', a, crinkle(.35), .9)
fx('N12', 1.4, crinkle(2.2), 1.0)
for k in range(10): fx('N12', 1.6 + k * .2, tick(), .25)
fx('N12', 4.7, slurp(), .8)
for k in range(7): fx('N20', .2 + k * .4, thup(), .5)
fx('N20', 3.0, sweep(180, 120, .6, 1) * expd(.6, .3) * .4, .6); fx('N20', 4.15, whoosh(.3, 400, 3000), .4); fx('N20', 4.3, crinkle(2.0), .7); fx('N20', 6.35, whoosh(.25, 800, 4000), .4); fx('N20', 6.8, ding(1568), .5)
fx('N10', .3, ding(1320), .3); fx('N10', 3.3, ding(1760), .25)
for a in [4.0, 4.9, 5.6, 6.2, 6.7, 7.1, 8.2, 8.9]: fx('N10', a, filt(snap(), 'bandpass', [1000, 4000]), .7 if a < 7.5 else .45)
for a in [8.2, 8.9]: fx('N10', a + .05, thup(), .7)
fx('N10', 9.75, pop(), .5)
fx('N3', 0, fade(filt(noise(DUR['N3']), 'bandpass', [400, 2500]), .3, .3) * .15, 1.0); fx('N3', 5.35, thunk(), 1.0); fx('N3', 5.38, clank(.7, .8), .7); fx('N3', 5.5, whoosh(.6, 300, 2000), .5)
fx('N3', 9.0, thunk(), 1.0); fx('N3', 9.02, filt(noise(.6), 'lowpass', 300) * expd(.6, .15), 1.0)
fx('N23', .7, snap(), .7)
for a in (2.8, 5.0, 6.6): fx('N23', a, snap())
for a in (4.2, 6.4, 8.2): fx('N23', a, ding(2637)[:N(.4)], .4)
for a in (1.9, 3.3, 5.3): fx('N4', a, norm(filt(noise(.12), 'lowpass', 3000) * expd(.12, .02), 1.0), .9)
fx('N4', 6.4, whoosh(1.2, 200, 800), .2)
fx('N13', 1.9, np.sin(2 * np.pi * 1975 * tt(.15)) * .25, 1.0); fx('N13', 3.0, glass()[:N(.6)], .8); fx('N13', 3.0, click(), 1.0); fx('N13', 3.6, pop(), .6)
fx('N7', .05, ding(1319), .5); fx('N7', .45, ding(1047), .5)
for a in (3.3, 6.5): fx('N7', a, whoosh(.3, 500, 3000), .35)
for a in (1.4, 4.7, 7.9): fx('N7', a, thup(), .8)
fx('N8', .05, thunk(), .6); fx('N8', .25, thunk(), .6)
fx('N17', 2.35, click(), 1.0); fx('N17', 2.38, filt(noise(.5), 'highpass', 3000) * expd(.5, .1), .5)
for a in (.9, 1.4, 1.9): fx('N17', a, tick(), .8)
fx('N9', 1.0, crinkle(.9), 1.0); fx('N9', 2.6, ding(1568), .5)

fx('T0', .3, whoosh(.5, 300, 2000), .4); fx('T0', .9, pop(), .9); fx('T0', 1.0, ding(1319), .5)
fx('NB', .4, fade(filt(noise(4.2), 'bandpass', [1500, 5000]) * (.5 + .5 * np.sin(2 * np.pi * 2.7 * tt(4.2))) ** 2, .05, .2) * .35, 1.0)
for i in range(6): fx('NB', 1.0 + i * .5, plop(), .5)
fx('NW', .05, ding(1319), .5); fx('NW', .4, ding(1047), .5); fx('NW', .4, sweep(180, 120, .6, 1) * expd(.6, .3) * .4, .5); fx('NW', 3.2, thup(), .9)
for a in (2.4, 3.9, 5.5): fx('NE', a, ding(1760), .35)
fx('NE', 5.55, thunk(), .7)
fx('NX', 1.6, ding(2637)[:N(.5)], .5); fx('NX', 1.66, ding(2349)[:N(.5)], .4)
# Dave sings (a soft lead line over the party track)
def sing(notes, beat=.5):
    out = np.zeros(N(beat * sum(d for _, d in notes)) + SR); t0 = 0.0
    for m, d in notes:
        dd = d * beat; tt_ = tt(dd); f = midi(m) * (1 + .012 * np.sin(2 * np.pi * 5.5 * tt_) * np.minimum(tt_ / .2, 1))
        ph = 2 * np.pi * np.cumsum(f) / SR; x = (np.sin(ph) + .35 * np.sin(2 * ph) + .12 * np.sin(3 * ph)) * fade(np.ones(N(dd)), .04, .08)
        out[N(t0):N(t0) + len(x)] += x; t0 += dd
    return filt(out, 'lowpass', 2500) * .25
fx('NK', .75, sing([(69, 1), (72, 1), (76, 2), (74, 1), (72, 1), (69, 2), (67, 1), (69, 1), (72, 2), (76, 1), (74, 1)]), .9)

# 14 the morning after
fx('14', .3, ding(2349), .35); fx('14', 1.4, ding(1975), .25)
fx('14', 3.8, snap()); fx('14', 3.9, glass(), 1.0)
for d in ARMOR: fx('14', 4.05 + d, whoosh(.4), .4); fx('14', 4.05 + d + .42, clank(1 + d * .3), .55)
fx('14', 5.6, pop(), .7); fx('14', 7.05, slurp(), .9)

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
