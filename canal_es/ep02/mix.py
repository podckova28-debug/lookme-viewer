"""Ep02 sound: narration + procedural music, ambience and effects, all generated here (no third-party audio).
usage: python mix.py VO_DIR PROBE.json OUT.wav
VO_DIR has one wav per line id; PROBE.json comes from probe.js (ghost/vision state per scene)."""
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
    ting = (np.sin(2 * np.pi * 1318.5 * secs(1.1)) + .45 * np.sin(2 * np.pi * 1975.5 * secs(1.1))) * np.exp(-secs(1.1) * 4.5) * .12
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
def heartbeat(): t = secs(.5); x = np.sin(2 * np.pi * np.cumsum(np.linspace(70, 40, len(t))) / SR) * np.exp(-t * 14); y = np.zeros(int(.75 * SR)); add(y, x, 0); add(y, x * .7, .22); return y * .9
def rewind(d): t = secs(d); s = sweep(300, 2600, d, .7) * .12; n = bp(rng.standard_normal(len(t)), 800, 6000) * .25 * (.6 + .4 * np.sin(2 * np.pi * 18 * t)); return (s + n) * np.minimum(1, t * 8)
def tick(): t = secs(.05); return hp(rng.standard_normal(len(t)), 3000) * env(len(t), .0005, .006) * .6
def blow(dur=.7): t = secs(dur); return bp(rng.standard_normal(len(t)), 600, 4000) * np.sin(np.pi * t / dur) * .35
def applause(dur, dens=28):
    x = np.zeros(int(dur * SR) + SR // 4)
    for k in range(int(dur * dens)): add(x, clap() * rng.uniform(.25, .7), rng.uniform(0, dur))
    return x

# ---------------------------------------------------------------- music: a light, curious loop, tape-stops when time stops
MOODS = {
    'happy': [[60, 64, 67], [57, 60, 64], [53, 57, 60], [55, 59, 62], [60, 64, 67], [52, 55, 59], [53, 57, 60], [55, 59, 62]],
    'tense': [[57, 60, 64], [57, 60, 64], [53, 57, 60], [52, 56, 59], [57, 60, 64], [50, 53, 57], [52, 56, 59], [52, 56, 59]],
    'sad':   [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62], [57, 60, 64], [53, 57, 60], [50, 53, 57], [52, 55, 59]],
}
def music(total, mood_at=lambda t: 'happy'):
    bpm = 96; beat = 60 / bpm; bar = 4 * beat
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    L = int((total + 4) * SR); x = np.zeros(L); r2 = np.random.default_rng(3)
    penta = [72, 74, 76, 79, 81, 84]
    nb = int(total / bar) + 2
    for b in range(nb):
        t0 = b * bar; md = mood_at(t0); ch = MOODS[md][b % 8]
        # bass
        for k in ((0, .5, 1, 1.5, 2, 2.5, 3, 3.5) if md == 'tense' else (0, 2)):
            t = secs(beat * (.45 if md == 'tense' else 1.2)); f = hz(ch[0] - 24); add(x, (np.sin(2 * np.pi * f * t) + .25 * np.sin(4 * np.pi * f * t)) * np.exp(-t * (9 if md == 'tense' else 3.2)) * (.42 if md == 'tense' else .5), t0 + k * beat)
        # plucked arpeggio (eighths)
        arp = [ch[0], ch[1], ch[2], ch[1] + 12, ch[2], ch[1], ch[0] + 12, ch[2]]
        for k, m in enumerate(arp):
            if md == 'sad' and k % 2: continue
            t = secs(.5); f = hz(m); add(x, (np.sin(2 * np.pi * f * t) + .35 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t * 20)) * np.exp(-t * 7) * .18, t0 + k * beat / 2)
        # soft offbeat ticks
        for k in range(4):
            t = secs(.06); add(x, hp(r2.standard_normal(len(t)), 7000) * np.exp(-t * 90) * .05, t0 + k * beat + beat / 2)
        # glockenspiel melody, sparse
        for k in range(4):
            if md == 'happy' and r2.random() < .45:
                t = secs(1.2); f = hz(r2.choice(penta)); add(x, (np.sin(2 * np.pi * f * t) + .4 * np.sin(2 * np.pi * 2.76 * f * t)) * np.exp(-t * 3) * .12, t0 + k * beat)
    return x
def frozen_pad(total):
    """Quiet, warm pad for stopped time: low chord tones that follow the music's progression, soft attack,
    lowpassed under 900 Hz, plus a little low 'air'. Nothing high or constant enough to tire the ears."""
    bpm = 96; bar = 4 * 60 / bpm
    prog = [[48, 55, 64], [45, 52, 60], [41, 48, 57], [43, 50, 59], [48, 55, 64], [40, 47, 55], [41, 48, 57], [43, 50, 59]]
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    L = int((total + 4) * SR); x = np.zeros(L); seg = int(bar * 2 * SR)          # one chord every two bars
    tt = np.arange(seg + SR) / SR
    win = np.minimum(1, tt / 1.2) * np.minimum(1, np.maximum(0, (seg / SR + 1.0 - tt)) / 1.2)   # slow fade in/out, overlapping
    for b in range(int(total / (bar * 2)) + 2):
        y = np.zeros(len(tt))
        for k, m in enumerate(prog[b % len(prog)]):
            f = hz(m); y += (np.sin(2 * np.pi * f * tt) + .25 * np.sin(2 * np.pi * 2 * f * tt + .5)) * (1 / (k + 1.4))
        add(x, y * win * (.75 + .25 * np.sin(2 * np.pi * .12 * tt)), b * seg / SR)
    x = lp(x, 900, 4)
    return x * .05 + lp(rng.standard_normal(L), 300) * .009

# ---------------------------------------------------------------- ep02 effects: the vision
def vision():
    """the ghost switches on: a soft rising shimmer with a glassy chime on top"""
    d = .9; t = secs(d); s = sweep(500, 2400, d, .7) * np.sin(np.pi * t / d) ** 2 * .10
    air = bp(rng.standard_normal(len(t)), 2000, 9000) * np.sin(np.pi * t / d) ** 2 * .10
    ch = np.zeros(int(1.6 * SR)); tc = secs(1.3)
    for f, g in [(1760, .10), (2637, .06), (3520, .04)]: add(ch, np.sin(2 * np.pi * f * tc) * np.exp(-tc * 3.5) * g, .25)
    out = np.zeros(len(ch)); out[:len(t)] += s + air; return out + ch
def echo_line(x):
    """a line heard from the future: thinner, with a short echo tail"""
    y = bp(x, 250, 5200); out = np.zeros(len(y) + int(.6 * SR)); add(out, y, 0)
    for k, g in [(.11, .38), (.23, .22), (.36, .12)]: add(out, y * g, k)
    return out * 1.05

# ---------------------------------------------------------------- timelines from the probe (100 Hz)
fr = np.zeros(int((TOTAL + 1) * 100), dtype=np.int8)    # "frozen" here = music stops: eyes shut, and the cut to black
gh = np.zeros(int((TOTAL + 1) * 100))
for sid in T['order']:
    pr = P[sid]; st = sc(sid)['start']; hz = pr['hz']
    for i, v in enumerate(pr.get('gh', [])):
        a = int((st + i / hz) * 100); gh[a:a + int(100 / hz) + 1] = v
s = 's15'; a, b = int((Lt(s, 's15_03') + .2) * 100), int((Lt(s, 's15_06') + .2) * 100); fr[a:b] = 1
s = 's16'; cut = Le(s, 's16_08') + .15; fr[int(cut * 100):int((sc(s)['start'] + sc(s)['dur']) * 100)] = 1

print('music...', flush=True)
n100 = len(fr); rate = np.zeros(n100); r = 1.0
for i in range(n100):
    tgt = 0.0 if fr[i] else 1.0; k = .045 if tgt < r else .12; r += (tgt - r) * k; rate[i] = r
pos = np.cumsum(rate) / 100.0
SECTIONS = [(sc('s12')['start'] + sc('s12')['L']['s12_01'][0], sc('s12')['start'] + sc('s12')['L']['s12_06'][0], 'sad'),
            (Lt('s14', 's14_05') - .3, sc('s15')['start'] + sc('s15')['L']['s15_03'][0], 'tense'),
            (Lt('s16', 's16_04') - .3, cut, 'tense')]
sec_m = [(np.interp(a, np.arange(n100) / 100.0, pos), np.interp(b, np.arange(n100) / 100.0, pos), m) for a, b, m in SECTIONS]
def mood_at(mt):
    for a, b, m in sec_m:
        if a - 1.5 <= mt < b: return m
    return 'happy'
mus = music(pos[-1] + 2, mood_at)
tt = np.arange(N) / SR; mpos = np.interp(tt, np.arange(n100) / 100.0, pos) * SR
music_out = np.interp(mpos, np.arange(len(mus)), mus) * np.interp(tt, np.arange(n100) / 100.0, np.clip(rate * 1.4, 0, 1))
fz = np.interp(tt, np.arange(n100) / 100.0, movavg(fr.astype(float), 15))
pad = frozen_pad(TOTAL)[:N] * fz
pad[int(cut * SR):int((sc('s16')['start'] + sc('s16')['dur']) * SR)] = 0   # the cut to black is silent
ghs = np.interp(tt, np.arange(n100) / 100.0, movavg(gh, 20))
shimmer = lp(hp(rng.standard_normal(N), 4000), 9000) * .012 * ghs   # a faint high air while the vision is on

# ---------------------------------------------------------------- ambience per scene
amb = np.zeros(N)
def room(d, lvl=.012): return lp(rng.standard_normal(int(d * SR)), 400) * lvl * 6
for sid in T['order']:
    s0, d = sc(sid)['start'], sc(sid)['dur']
    if sid in ('s00', 's01', 's02', 's05', 's12', 's14', 's15'): t = secs(d); add(amb, hp(lp(rng.standard_normal(len(t)), 2500), 150) * .015, s0)
    elif sid == 's16': t = secs(d); add(amb, hp(lp(rng.standard_normal(len(t)), 1800), 200) * .010, s0)
    elif sid == 's17': pass
    else: add(amb, room(d), s0)
amb *= (1 - fz)

# ---------------------------------------------------------------- effects timeline
fx = np.zeros(N)
# vision onsets: every time a ghost appears
on = False
for i in range(len(gh)):
    if gh[i] > .3 and not on: add(fx, vision(), i / 100 - .15, .9); on = True
    elif gh[i] < .05: on = False
s = 's00'; rw = Lm(s, 's00_05', .45)
for k in range(int((Lt(s, 's00_05') - sc(s)['start']) / .85)): add(fx, heartbeat(), sc(s)['start'] + .4 + k * .85, .8)
add(fx, rewind(sc(s)['start'] + sc(s)['dur'] - rw), rw, .9)
s = 's01'; add(fx, whoosh(.4), Lm(s, 's01_04', .2) - .3, .7); add(fx, pop(), Lm(s, 's01_04', .5), .6); add(fx, pop(), Lm(s, 's01_04', .78), .5)
for k, f in enumerate([.02, .36, .68]): add(fx, pop(), Lm(s, 's01_02', f), .5 + .2 * (k == 2))
s = 's02'; add(fx, pop(), sc(s)['start'] + .75, .8); add(fx, whoosh(.4), sc(s)['start'] + .6, .6)
s = 's03'; rt = Lt(s, 's03_06') + Ld(s, 's03_06') * .45; add(fx, whoosh(.5), rt, .7); add(fx, thud(), rt + .75, .5); add(fx, blow(.5), rt + .75, .6)
s = 's04'; kt = Lt(s, 's04_04') + Ld(s, 's04_04') * .55; add(fx, whoosh(.3), kt + .1, .6); add(fx, pop(), kt + .42, .8); add(fx, pop(), Lt(s, 's04_07') - .15, .8); add(fx, pop(), Lt(s, 's04_08') - .1, .6)
s = 's05'; add(fx, whistle(1.0), sc(s)['start'] + .4, .9); t3 = Lt(s, 's05_04')
for i, d in enumerate([t3 + .1, Lm(s, 's05_04', .45), Lm(s, 's05_04', .8)]): add(fx, whoosh(.35), d - .45, .8)
for i in range(3, 14): add(fx, whoosh(.3), sc(s)['start'] + 7 + i * .55, .5)
add(fx, sting(), Lt(s, 's05_08') - .1, .5)
s = 's06'; R6 = [Lt(s, 's06_02') - .1, Lt(s, 's06_03') - .1] + [Lt(s, 's06_04') + i * .22 for i in range(12)] + [Lm(s, 's06_05', .9)]
for r6 in R6: add(fx, pop(), r6, .6)
add(fx, ding(), Lt(s, 's06_06') + .1, .7)
s = 's07'; add(fx, pop(), Lt(s, 's07_03') - .1, .7); add(fx, pop(), Lm(s, 's07_06', .55), .6); add(fx, pop(), Lt(s, 's07_08'), .7)
s = 's08'
for c in [Lm(s, 's08_02', .55), Lm(s, 's08_03', .55), Lm(s, 's08_04', .6)]: add(fx, whoosh(.3), c - .3, .6); add(fx, pop(), c, .8)
s = 's09'; T0 = Lt(s, 's09_03')
for i in range(4): add(fx, ding(1568 + 196 * i), T0 + i * Ld(s, 's09_03') / 4 + 1.05, .45)
add(fx, ding(2093), Lt(s, 's09_04'), .5); add(fx, sting(), Lt(s, 's09_06') - .05, .8)
s = 's10'; add(fx, pop(), Lt(s, 's10_03') - .05, .6); add(fx, pop(), Lt(s, 's10_07') - .05, .5); add(fx, sting(), Lt(s, 's10_08') + .1, .4)
s = 's11'; jump = Lt(s, 's11_08') - .15; add(fx, cheer(2.6), jump, .9); add(fx, applause(1.8), jump + .3, .25); add(fx, pop(), jump, .8)
add(fx, ding(1046), Lt(s, 's11_05'), .5); add(fx, sting(), Lt(s, 's11_10'), .6)
s = 's13'; hit = Lt(s, 's13_09') + .15; add(fx, whoosh(.4), hit - .35, .7); add(fx, thud(), hit, .9); add(fx, pop(), hit + .05, .7); add(fx, pop(), Lt(s, 's13_11') - .15, .8)
s = 's14'
for k in range(int((Lt(s, 's14_08') - Lt(s, 's14_05')) / .75)): add(fx, heartbeat(), Lt(s, 's14_05') + k * .75, .8)
add(fx, pop(), Lt(s, 's14_08'), .7)
s = 's15'; c0, d5 = Lt(s, 's15_05'), Ld(s, 's15_05')
for k in range(int((Lt(s, 's15_06') - Lt(s, 's15_03')) / .95)): add(fx, heartbeat(), Lt(s, 's15_03') + .4 + k * .95, .55)
for i in range(5): add(fx, tick(), c0 + d5 * i / 5, 1.2)
add(fx, ding(1318), Lt(s, 's15_06') + .2, .6); add(fx, pop(), Lt(s, 's15_13') - .15, .8)
s = 's16'
for i in range(4): add(fx, tick(), Lt(s, 's16_08') + Ld(s, 's16_08') * i / 4, 1.3)
add(fx, coo(), Lm(s, 's16_03', .5), .5)
s = 's17'
for k in ['s17_02', 's17_05', 's17_07', 's17_08']: add(fx, whoosh(.3), Lt(s, k) - .2, .5)
s = 's18'; add(fx, pop(), Lm(s, 's18_04', .5), .6); add(fx, coo(), Le(s, 's18_05') + .2, .8)
fx[int(cut * SR):int((sc('s16')['start'] + sc('s16')['dur']) * SR)] = 0

# ---------------------------------------------------------------- narration
L_ = {l['id']: l for l in json.load(open(os.path.join(HERE, 'vo_lines.json'), encoding='utf-8'))}
vo = np.zeros(N); voice_env = np.zeros(N)
for sid in T['order']:
    for lid, (t, d, who) in sc(sid)['L'].items():
        x, sr = sf.read(os.path.join(VO, lid + '.wav'), dtype='float32')
        if x.ndim > 1: x = x.mean(1)
        if sr != SR: x = resample_poly(x, SR, sr)
        rms = np.sqrt(np.mean(x[np.abs(x) > .01] ** 2)) if np.any(np.abs(x) > .01) else .1; x = x * (.11 / rms) * (1.35 if who == 'chicos' else 1.0)
        if L_[lid].get('fx') == 'futuro': x = echo_line(x)
        add(vo, x, sc(sid)['start'] + t); add(voice_env, np.ones(len(x)), sc(sid)['start'] + t)
duck = 1 - .55 * movavg(np.minimum(voice_env, 1), int(.25 * SR))
mix = vo * 1.0 + music_out * .55 * duck + pad * .55 * (1 - .35 * (1 - duck)) + amb * duck + fx * .55 + shimmer
mix = mix / max(1e-6, np.max(np.abs(mix))) * .89
sf.write(OUT, mix.astype(np.float32), SR)
print('wrote', OUT, round(len(mix) / SR, 1), 's')
