"""Ep01 sound: narration + procedural music, ambience and effects, all generated here (no third-party audio).
usage: python mix.py VO_DIR PROBE.json OUT.wav
VO_DIR has one wav per line id; PROBE.json comes from probe.js (claps + frozen state per scene)."""
import json, os, sys
import numpy as np, soundfile as sf
from scipy.signal import resample_poly, lfilter, butter

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
VO, PROBE, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
T = json.load(open(os.path.join(HERE, 'timing.json')))
P = json.load(open(PROBE))
TOTAL = T['total']; N = int((TOTAL + 1.0) * SR)
rng = np.random.default_rng(7)

def sc(sid): return T['scenes'][sid]
def Lt(sid, lid): return sc(sid)['start'] + sc(sid)['L'][lid][0]
def Ld(sid, lid): return sc(sid)['L'][lid][1]
def Le(sid, lid): return Lt(sid, lid) + Ld(sid, lid)
def Lm(sid, lid, f): return Lt(sid, lid) + Ld(sid, lid) * f
def secs(x): return np.arange(int(x * SR)) / SR
def env(n, a=.005, d=.2): t = np.arange(n) / SR; return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
def bp(x, lo, hi, order=2): b, a = butter(order, [lo / (SR / 2), hi / (SR / 2)], 'band'); return lfilter(b, a, x)
def lp(x, f, order=2): b, a = butter(order, f / (SR / 2), 'low'); return lfilter(b, a, x)
def hp(x, f, order=2): b, a = butter(order, f / (SR / 2), 'high'); return lfilter(b, a, x)
def movavg(x, n):
    c = np.cumsum(np.concatenate([[0.0], x])); y = (c[n:] - c[:-n]) / n; pad = n // 2
    return np.concatenate([np.full(pad, y[0]), y, np.full(len(x) - len(y) - pad, y[-1])])
def add(buf, x, t, g=1.0):
    i = int(t * SR)
    if i >= len(buf) or i + len(x) <= 0: return
    j0 = max(0, -i); x = x[j0:]; i = max(0, i); n = min(len(x), len(buf) - i); buf[i:i + n] += g * x[:n]

# ---------------------------------------------------------------- effects
def clap():
    n = int(.16 * SR); x = np.zeros(n); nz = rng.standard_normal(n)
    for k, d in enumerate([0, .009, .018]): i = int(d * SR); e = env(n - i, .0005, .012 if k < 2 else .05); x[i:] += nz[:n - i] * e
    return bp(x, 900, 5000) * 1.2
def sweep(f0, f1, dur, shape=1.0):
    t = secs(dur); f = f0 * (f1 / f0) ** ((t / dur) ** shape); ph = 2 * np.pi * np.cumsum(f) / SR; return np.sin(ph)
def freeze_fx():
    d = .7; t = secs(d); s = sweep(1400, 160, d, .6) * np.exp(-t * 3) * .35
    w = bp(rng.standard_normal(len(t)), 300, 3000) * np.exp(-t * 4) * .5
    ting = (np.sin(2 * np.pi * 2637 * secs(1.6)) + .6 * np.sin(2 * np.pi * 3951 * secs(1.6))) * np.exp(-secs(1.6) * 2.6) * .22
    out = np.zeros(len(ting)); out[:len(t)] += s + w; out += ting; return out
def unfreeze_fx():
    d = .45; t = secs(d); s = sweep(180, 1500, d, 1.4) * (t / d) * .3; w = bp(rng.standard_normal(len(t)), 400, 4000) * (t / d) ** 2 * .45
    return np.concatenate([s + w, (s + w)[-1] * np.exp(-secs(.08) * 60)])
def pop(): t = secs(.12); return np.sin(2 * np.pi * np.cumsum(np.linspace(500, 950, len(t))) / SR) * env(len(t), .002, .05) * .5
def ding(f=1568): t = secs(1.8); return (np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 1.5 * t) + .25 * np.sin(2 * np.pi * f * 2.76 * t)) * np.exp(-t * 2.2) * .28
def thud(): t = secs(.35); return (np.sin(2 * np.pi * np.cumsum(np.linspace(120, 50, len(t))) / SR) * np.exp(-t * 12) + bp(rng.standard_normal(len(t)), 200, 2000) * np.exp(-t * 40) * .4) * .8
def whoosh(d=.35): t = secs(d); return bp(rng.standard_normal(len(t)), 500, 4000) * np.sin(np.pi * t / d) ** 2 * .45
def snap(): t = secs(.06); return hp(rng.standard_normal(len(t)), 2500) * env(len(t), .0003, .008) * 1.4
def alarm(dur):
    t = secs(dur); sq = np.sign(np.sin(2 * np.pi * 2200 * t)) * .5 + np.sin(2 * np.pi * 2200 * t) * .5
    gate = ((t * 8) % 1 < .5) & ((t * 1.25) % 1 < .62); return lp(sq * gate, 6000) * .16
def scribble(dur): t = secs(dur); am = .5 + .5 * np.sin(2 * np.pi * 13 * t) * np.sin(2 * np.pi * 3.1 * t); return bp(rng.standard_normal(len(t)), 2500, 7000) * am * .18
def pour(dur): t = secs(dur); return lp(bp(rng.standard_normal(len(t)), 300, 2500) * (.6 + .4 * np.sin(2 * np.pi * 7 * t)), 3000) * np.minimum(1, t * 5) * np.minimum(1, (dur - t) * 3) * .3
def cheer(dur=2.2):
    t = secs(dur); x = np.zeros(len(t))
    for k in range(14):
        f0 = rng.uniform(260, 520); vib = 1 + .03 * np.sin(2 * np.pi * rng.uniform(4, 7) * t); ph = 2 * np.pi * np.cumsum(f0 * vib * (1 + .25 * np.minimum(1, t * 3))) / SR
        saw = 2 * ((ph / (2 * np.pi)) % 1) - 1; x += bp(saw, 500, 2400) * rng.uniform(.5, 1)
    x += bp(rng.standard_normal(len(t)), 400, 3000) * .6
    return x / 14 * np.minimum(1, t * 4) * np.exp(-np.maximum(0, t - .6) * 1.6) * 1.2
def sting():
    out = np.zeros(int(2.4 * SR))
    for st_, f, d in [(0, 146.8, .22), (.28, 146.8, .22), (.62, 116.5, 1.6)]:
        t = secs(d + .3); ph = 2 * np.pi * f * t; saw = 2 * ((ph / (2 * np.pi)) % 1) - 1; sq = np.sign(np.sin(ph * 2)) * .3
        x = lp(saw + sq, 1400) * np.minimum(1, t / .02) * np.exp(-np.maximum(0, t - d) * 8) * .5; add(out, x, st_)
    return out
def whistle(dur): t = secs(dur); return np.sin(2 * np.pi * np.cumsum(np.linspace(1800, 700, len(t))) / SR) * np.minimum(1, t * 6) * .13
def coo(): t = secs(.9); f = 390 + 25 * np.sin(2 * np.pi * 6 * t); x = np.sin(2 * np.pi * np.cumsum(f) / SR) + .3 * np.sin(4 * np.pi * np.cumsum(f) / SR); return lp(x, 1200) * np.sin(np.pi * t / .9) ** 2 * .35
def tick(): t = secs(.05); return hp(rng.standard_normal(len(t)), 3000) * env(len(t), .0005, .006) * .6
def blow(dur=.7): t = secs(dur); return bp(rng.standard_normal(len(t)), 600, 4000) * np.sin(np.pi * t / dur) * .35
def applause(dur, dens=28):
    x = np.zeros(int(dur * SR) + SR // 4)
    for k in range(int(dur * dens)): add(x, clap() * rng.uniform(.25, .7), rng.uniform(0, dur))
    return x

# ---------------------------------------------------------------- frozen timeline
fr = np.zeros(int((TOTAL + 1) * 100), dtype=np.int8)   # 100 Hz
for sid in T['order']:
    pr = P[sid]; st = sc(sid)['start']; hz = pr['hz']
    for i, v in enumerate(pr['frz']):
        a = int((st + i / hz) * 100); fr[a:a + int(100 / hz) + 1] = v
# the end card plays with music
_e = int((Le('s17', 's17_04') + .9) * 100); fr[_e:] = 0
def frozen_at(t): i = int(t * 100); return fr[min(max(i, 0), len(fr) - 1)]

# ---------------------------------------------------------------- music: a light, curious loop, tape-stops when time stops
def music(total):
    bpm = 96; beat = 60 / bpm; bar = 4 * beat
    prog = [[60, 64, 67], [57, 60, 64], [53, 57, 60], [55, 59, 62], [60, 64, 67], [52, 55, 59], [53, 57, 60], [55, 59, 62]]
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    L = int((total + 4) * SR); x = np.zeros(L); r2 = np.random.default_rng(3)
    penta = [72, 74, 76, 79, 81, 84]
    nb = int(total / bar) + 2
    for b in range(nb):
        ch = prog[b % len(prog)]; t0 = b * bar
        # bass
        for k in (0, 2):
            t = secs(beat * 1.2); f = hz(ch[0] - 24); add(x, (np.sin(2 * np.pi * f * t) + .25 * np.sin(4 * np.pi * f * t)) * np.exp(-t * 3.2) * .5, t0 + k * beat)
        # plucked arpeggio (eighths)
        arp = [ch[0], ch[1], ch[2], ch[1] + 12, ch[2], ch[1], ch[0] + 12, ch[2]]
        for k, m in enumerate(arp):
            t = secs(.5); f = hz(m); add(x, (np.sin(2 * np.pi * f * t) + .35 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t * 20)) * np.exp(-t * 7) * .18, t0 + k * beat / 2)
        # soft offbeat ticks
        for k in range(4):
            t = secs(.06); add(x, hp(r2.standard_normal(len(t)), 7000) * np.exp(-t * 90) * .05, t0 + k * beat + beat / 2)
        # glockenspiel melody, sparse
        for k in range(4):
            if r2.random() < .45:
                t = secs(1.2); f = hz(r2.choice(penta)); add(x, (np.sin(2 * np.pi * f * t) + .4 * np.sin(2 * np.pi * 2.76 * f * t)) * np.exp(-t * 3) * .12, t0 + k * beat)
    return x
def frozen_pad(total):
    t = np.arange(int((total + 1) * SR)) / SR
    x = (np.sin(2 * np.pi * 1046.5 * t) + .7 * np.sin(2 * np.pi * 1568 * t) + .4 * np.sin(2 * np.pi * 2093 * t)) * (.6 + .4 * np.sin(2 * np.pi * .35 * t))
    return x * .025 + lp(rng.standard_normal(len(t)), 900) * .02

print('music...', flush=True)
mus = music(TOTAL)
# tape: rate follows the frozen state (ramps down ~0.45 s, back up ~0.2 s)
n100 = len(fr); rate = np.zeros(n100); r = 1.0
for i in range(n100):
    tgt = 0.0 if fr[i] else 1.0; k = .045 if tgt < r else .12; r += (tgt - r) * k; rate[i] = r
pos = np.cumsum(rate) / 100.0  # music seconds at each 10 ms
tt = np.arange(N) / SR; mpos = np.interp(tt, np.arange(n100) / 100.0, pos) * SR
music_out = np.interp(mpos, np.arange(len(mus)), mus) * np.interp(tt, np.arange(n100) / 100.0, np.clip(rate * 1.4, 0, 1))
fz = np.interp(tt, np.arange(n100) / 100.0, movavg(fr.astype(float), 15))
pad = frozen_pad(TOTAL)[:N] * fz

# ---------------------------------------------------------------- ambience per scene (only while the world runs)
amb = np.zeros(N)
def room(d, lvl=.012): return lp(rng.standard_normal(int(d * SR)), 400) * lvl * 6
for sid in T['order']:
    s0, d = sc(sid)['start'], sc(sid)['dur']
    if sid == 's08':
        home = Lt('s08', 's08_05') - .1; add(amb, hp(lp(rng.standard_normal(int((home - s0) * SR)), 5000), 400) * .07, s0); add(amb, room(s0 + d - home), home)
    elif sid == 's13': t = secs(d); add(amb, bp(rng.standard_normal(len(t)), 250, 1800) * (.5 + .5 * np.abs(np.sin(2 * np.pi * .7 * t))) * .05, s0)
    elif sid in ('s14', 's15', 's10'): t = secs(d); add(amb, hp(lp(rng.standard_normal(len(t)), 2500), 150) * .015, s0)
    else: add(amb, room(d), s0)
amb *= (1 - fz)

# ---------------------------------------------------------------- effects timeline
fx = np.zeros(N)
for sid in T['order']:
    ev = P[sid]['ev']; s0 = sc(sid)['start']
    if not ev: continue
    state = ev['start']; claps = sorted(ev['claps'])
    for i, c in enumerate(claps):
        t = s0 + c; state = 1 - state; gap = (claps[i + 1] - c) if i + 1 < len(claps) else 9
        add(fx, clap(), t - .01, .9)
        if gap > .3: add(fx, freeze_fx() if state else unfreeze_fx(), t + .02, .8)
        else: add(fx, tick(), t + .02, .6)
s = 's02'; add(fx, pop(), sc(s)['start'] + .75, .8); add(fx, whoosh(.4), sc(s)['start'] + .6, .6)
s = 's03'; a = Lt(s, 's03_02'); b = Lm(s, 's03_03', .3); add(fx, alarm(b - a), a, .9)
s = 's04'; tr = Lm(s, 's04_06', .12); add(fx, pour(2.4), tr + .05, .9); add(fx, pop(), Lt(s, 's04_09') - .15, .8); add(fx, pop(), Lt(s, 's04_10') - .1, .6); add(fx, pop(), Le(s, 's04_08') - .05, .6)
s = 's05'; add(fx, ding(1760), Lt(s, 's05_04'), .7); add(fx, thud(), Lm(s, 's05_01', .86), .5)
s = 's06'; tr = Lt(s, 's06_06') + .1; add(fx, scribble(Lm(s, 's06_06', .7) - tr - .2), tr + .2, 1); add(fx, ding(), Lt(s, 's06_07') + .05, .8)
for k in range(4): add(fx, pop(), Lt(s, 's06_08') + k * (Ld(s, 's06_08') + 1.2) / 4, .45)
s = 's07'; a = Lm(s, 's07_02', .6); b = Le(s, 's07_02') + 1.0; add(fx, scribble(b - a), a, 1.2); add(fx, ding(2093), Lm(s, 's07_04', .75), .5)
s = 's09'; add(fx, thud(), Lm(s, 's09_01', .55), .5)
for k in range(5): add(fx, whoosh(.25), Lt(s, 's09_03') + .5 + k * .75, .5)
s = 's10'; kick = Lt(s, 's10_02') + .25; add(fx, thud(), kick, .9); g = Lt(s, 's10_05') + .1; add(fx, whoosh(.3), g, .6); add(fx, cheer(2.4), g + .25, .9)
s = 's11'; [add(fx, tick(), Lt(s, 's11_02') + k * .5, .5) for k in range(int((Le(s, 's11_03') - Lt(s, 's11_02')) / .5))]; add(fx, sting(), Lt(s, 's11_07') - .15, .9)
s = 's13'; add(fx, blow(), Lm(s, 's13_03', .45) - .3, .7); a = Lm(s, 's13_03', .72); b = Lt(s, 's13_12') - .1
ap = applause(b - a); gate = 1 - np.interp((a + np.arange(len(ap)) / SR), tt, fz); add(fx, ap * gate * .5, a)
add(fx, pop(), Lt(s, 's13_14') - .1, .8)
s = 's15'; tc = Lt(s, 's15_03') + .1; add(fx, whistle(1.76), tc - 1.76, 1)
s = 's16'; add(fx, snap(), Lm(s, 's16_04', .9) + .05, .9); add(fx, whoosh(.6), Lt(s, 's16_08') - .3, .7); add(fx, pop(), Lm(s, 's16_06', .75), .5)
s = 's17'; add(fx, coo(), Lm(s, 's17_04', .55) + .3, .9); add(fx, pop(), Lm(s, 's17_03', .7), .6)

# ---------------------------------------------------------------- narration
vo = np.zeros(N); voice_env = np.zeros(N)
for sid in T['order']:
    for lid, (t, d, who) in sc(sid)['L'].items():
        x, sr = sf.read(os.path.join(VO, lid + '.wav'), dtype='float32')
        if x.ndim > 1: x = x.mean(1)
        if sr != SR: x = resample_poly(x, SR // 1000, sr // 1000) if sr in (24000, 16000, 22050, 44100) and SR % 1000 == 0 and sr % 1000 == 0 else resample_poly(x, SR, sr)
        rms = np.sqrt(np.mean(x[np.abs(x) > .01] ** 2)) if np.any(np.abs(x) > .01) else .1; x = x * (.11 / rms)
        add(vo, x, sc(sid)['start'] + t); add(voice_env, np.ones(len(x)), sc(sid)['start'] + t)
duck = 1 - .55 * movavg(np.minimum(voice_env, 1), int(.25 * SR))

mix = vo * 1.0 + music_out * .55 * duck + pad * .7 + amb * duck + fx * .55
mix = mix / max(1e-6, np.max(np.abs(mix))) * .89
sf.write(OUT, mix.astype(np.float32), SR)
print('wrote', OUT, round(len(mix) / SR, 1), 's')
