"""Ep06 sound: narration + procedural music, ambience and effects, all generated here (no third-party audio).
usage: python mix.py VO_DIR PROBE.json OUT.wav
VO_DIR has one wav per line id . PROBE.json (probe.js) carries every hit of the pain look per scene (EVENTS): a thud, then a fizzle for the hero or a slap for anybody else."""
import json, os, sys
import numpy as np, soundfile as sf
from scipy.signal import resample_poly, lfilter, butter

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
VO, PROBE, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
T = json.load(open(os.path.join(HERE, 'timing.json')))
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
    return x * .05   # no noise bed under the pad: after mastering it reads as hiss

# ---------------------------------------------------------------- shared small effects (from ep04)
def shimmer(d=1.2, base=1568):
    """glassy sparkle: a few high bell partials that twinkle in and out"""
    out = np.zeros(int((d + .6) * SR)); r3 = np.random.default_rng(int(base))
    for k in range(9):
        f = base * r3.choice([1, 1.25, 1.5, 2, 2.5, 3]); t = secs(.7); add(out, (np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * 2.76 * f * t)) * np.exp(-t * 6) * .07, r3.uniform(0, d))
    return out
def beep(f=880, d=.12): t = secs(d); return np.sign(np.sin(2 * np.pi * f * t)) * .5 * env(len(t), .002, .08) * .25
def fail(): out = np.zeros(int(.5 * SR)); add(out, beep(330, .14), 0); add(out, beep(262, .2), .17); return out
def crunch(): t = secs(.09); return bp(rng.standard_normal(len(t)), 1200, 6000) * env(len(t), .001, .03) * .6
def clink(): x = ding(2637) * .35; add(x, snap() * .3, 0); return x
def cash(): x = ding(2093) * .6; add(x, ding(2637) * .4, 0); return x
def flutter(d=.6):
    t = secs(d); am = (np.sin(2 * np.pi * 14 * t) > 0).astype(float) * .7 + .3
    return bp(rng.standard_normal(len(t)), 600, 3500) * am * np.sin(np.pi * t / d) * .35
def sniff(): t = secs(.16); return bp(rng.standard_normal(len(t)), 2000, 7000) * np.sin(np.pi * t / .16) * .25
def knock(): x = thud() * .8; return lp(x, 900)
def scream(d=.9):
    t = secs(d); x = np.zeros(len(t))
    for k in range(5): f0 = rng.uniform(700, 1100); ph = 2 * np.pi * np.cumsum(f0 * (1 + .3 * np.minimum(1, t * 4)) * (1 + .02 * np.sin(2 * np.pi * 7 * t))) / SR; x += bp(2 * ((ph / (2 * np.pi)) % 1) - 1, 700, 3500) * rng.uniform(.5, 1)
    return x / 5 * np.minimum(1, t * 10) * np.exp(-np.maximum(0, t - .3) * 3) * .5

# ---------------------------------------------------------------- ep06 effects: the pain signal
def fizzle():
    """the signal dying halfway: a short falling blip, then a crackle of static"""
    out = np.zeros(int(.9 * SR)); d = .28; t = secs(d)
    add(out, sweep(1400, 300, d, .8) * np.exp(-t * 6) * .16, .05)
    t2 = secs(.45); add(out, bp(rng.standard_normal(len(t2)), 1500, 7000) * (np.random.default_rng(5).random(len(t2)) > .55) * np.exp(-t2 * 4) * .22, .2)
    return out
def slap(): t = secs(.12); x = hp(rng.standard_normal(len(t)), 1200) * env(len(t), .0005, .025); y = np.sin(2 * np.pi * 180 * t) * np.exp(-t * 40) * .5; return (x + y) * .9
def ow_sting(): t = secs(.5); return np.sin(2 * np.pi * np.cumsum(np.linspace(900, 1500, len(t))) / SR) * np.exp(-t * 6) * .14
def drill(d): t = secs(d); f = 2400 + 150 * np.sin(2 * np.pi * 9 * t); return (np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * .3 + np.sin(2 * np.pi * np.cumsum(f * 2) / SR) * .2) * np.minimum(1, t * 8) * np.minimum(1, (d - t) * 8) * .06
def engine(d, rise=0): t = secs(d); f = 55 + 30 * rise * (t / d); x = np.sin(2 * np.pi * np.cumsum(f + 4 * np.sin(2 * np.pi * 7 * t)) / SR) + .5 * np.sign(np.sin(2 * np.pi * np.cumsum(f * 2) / SR)); return lp(x, 400) * np.minimum(1, t * 2) * .2
def hiss_door(): t = secs(.6); return bp(rng.standard_normal(len(t)), 1500, 6000) * np.exp(-t * 5) * .3
def chew(n=4): out = np.zeros(int((n * .22 + .3) * SR)); [add(out, crunch() * .5, k * .22) for k in range(n)]; return out
def steps(d, limp=0):
    out = np.zeros(int((d + .3) * SR)); k = 0; tt = 0
    while tt < d: add(out, lp(thud(), 700) * (.5 if (limp and k % 2) else .3), tt); tt += .42 + (.12 if (limp and k % 2) else 0); k += 1
    return out

# ---------------------------------------------------------------- hits from the probe
P = json.load(open(PROBE)) if os.path.exists(PROBE) else {}
HITS = []
for sid, pr in P.items():
    ev = pr.get('ev') or {}
    for h in ev.get('hits', []): HITS.append((sc(sid)['start'] + h['t'], h['hero']))

# ---------------------------------------------------------------- music: stops when the power runs out
fr = np.zeros(int((TOTAL + 1) * 100), dtype=np.int8)
s = 's14'; a, b = int((Lm(s, 's14_07', .72) - .2) * 100), int((Lt(s, 's14_10') + .2) * 100); fr[a:b] = 1
s = 's15'; a, b = int((Lt(s, 's15_06') - .3) * 100), int((Le(s, 's15_07') + .2) * 100); fr[a:b] = 1

print('music...', flush=True)
n100 = len(fr); rate = np.zeros(n100); r = 1.0
for i in range(n100):
    tgt = 0.0 if fr[i] else 1.0; k = .045 if tgt < r else .12; r += (tgt - r) * k; rate[i] = r
pos = np.cumsum(rate) / 100.0
SECTIONS = [(Lt('s09', 's09_01') - .3, Le('s11', 's11_07'), 'tense'),
            (Lt('s12', 's12_05') - .3, Lt('s13', 's13_07'), 'sad'),
            (Lt('s14', 's14_10') - .5, Le('s14', 's14_11') + 1, 'sad'),
            (Lt('s15', 's15_06') - 1, Le('s15', 's15_09') + 1, 'tense')]
sec_m = [(np.interp(a, np.arange(n100) / 100.0, pos), np.interp(b, np.arange(n100) / 100.0, pos), m) for a, b, m in SECTIONS]
def mood_at(mt):
    for a, b, m in sec_m:
        if a - 1.5 <= mt < b: return m
    return 'happy'
mus = music(pos[-1] + 2, mood_at)
tt = np.arange(N) / SR; mpos = np.interp(tt, np.arange(n100) / 100.0, pos) * SR
music_out = np.interp(mpos, np.arange(len(mus)), mus) * np.interp(tt, np.arange(n100) / 100.0, np.clip(rate * 1.4, 0, 1))
pad = np.zeros(N)
s15end = sc('s15')['start'] + sc('s15')['dur']; k0, k1 = int((Le('s15', 's15_09') + .3) * SR), int(s15end * SR)
music_out[k0:k1] *= np.linspace(1, 0, k1 - k0)

# ---------------------------------------------------------------- ambience: birds outdoors by day, crickets at night
amb = np.zeros(N)
def chirp(f0=3200, d=.09):
    t = secs(d); f = f0 * (1 + .25 * np.sin(np.pi * t / d)); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d) ** 2 * .05
def cricket(d=.35):
    t = secs(d); return np.sin(2 * np.pi * 4300 * t) * ((t * 30) % 1 < .5) * np.sin(np.pi * t / d) * .012
r_amb = np.random.default_rng(11)
for sid in ('s01', 's05', 's08', 's12', 's14'):
    s0, d = sc(sid)['start'], sc(sid)['dur']; tb = s0 + 1.5
    while tb < s0 + d - 1:
        f0 = r_amb.uniform(2600, 3800)
        for k in range(r_amb.integers(2, 4)): add(amb, chirp(f0 * r_amb.uniform(.95, 1.08)), tb + k * .13, r_amb.uniform(.5, 1))
        tb += r_amb.uniform(2.5, 5.5)
for sid in ('s15', 's17'):
    s0, d = sc(sid)['start'], sc(sid)['dur']; tb = s0 + .5
    while tb < s0 + d - .5: add(amb, cricket(), tb, r_amb.uniform(.6, 1)); tb += r_amb.uniform(.8, 1.6)

# ---------------------------------------------------------------- effects timeline (times mirror the scene code)
fx = np.zeros(N)
for t0, hero in HITS:
    add(fx, thud(), t0 - .02, .8)
    if hero: add(fx, fizzle(), t0 + .25, .7)
    else: add(fx, slap(), t0, .7); add(fx, ow_sting(), t0 + .45, .5)
s = 's00'; rw = Lm(s, 's00_07', .45)
for k in range(5): add(fx, snap(), Lt(s, 's00_02') + k * .3, .3)
add(fx, pop(), Lt(s, 's00_04') + .4, .5); add(fx, rewind(sc(s)['start'] + sc(s)['dur'] - rw), rw, .9)
s = 's01'; add(fx, whoosh(.5), Lm(s, 's01_02', .15) - .5, .5)
for f in [0, .25, .5, .78]: add(fx, pop(), Lm(s, 's01_03', f) + .1, .5)
s = 's02'; add(fx, pop(), sc(s)['start'] + .75, .8)
s = 's03'; add(fx, steps(1.6), Lt(s, 's03_01') + 1.2, .8); add(fx, steps(1.5), Lt(s, 's03_05'), .8)
add(fx, pop(), Lt(s, 's03_07') + .1, .5); add(fx, pop(), Lm(s, 's03_07', .55), .5)
s = 's04'; add(fx, chew(4), Lm(s, 's04_03', .35), .8); add(fx, sting(), Lt(s, 's04_05') + .1, .35); add(fx, steps(2.0), Lm(s, 's04_05', .5), .3)
add(fx, pop(), Lt(s, 's04_07') + .1, .8)
s = 's05'
for f in ('s05_02', 's05_03'): add(fx, thud(), Lm(s, f, .45) - .6, .5)
add(fx, cheer(2.4), Lt(s, 's05_07') - .05, .9); add(fx, pop(), Lt(s, 's05_06'), .5)
s = 's06'; add(fx, steps(1.0), Lt(s, 's06_01') + 1.6, .6); add(fx, scribble(1.2), Lt(s, 's06_03') + .3, .7)
add(fx, whoosh(.4), Lt(s, 's06_06') - .2, .6); add(fx, scribble(Ld(s, 's06_07')), Lt(s, 's06_07') + .1, .9)
s = 's07'; add(fx, pop(), sc(s)['start'] + .3, .6); add(fx, drill(3.0), Lm(s, 's07_02', .3), 1.0); add(fx, pop(), Lt(s, 's07_02'), .5)
add(fx, whoosh(.6), Lm(s, 's07_03', .6), .4); add(fx, steps(1.0), Lt(s, 's07_04') - .1, .5); add(fx, whoosh(.4), Lt(s, 's07_04') + .9, .7)
add(fx, applause(2.5), Lm(s, 's07_04', .5) + .5, .6); add(fx, pop(), Lt(s, 's07_05') + .3, .5)
s = 's08'; add(fx, coo(), Lt(s, 's08_07'), .8); add(fx, pop(), Lt(s, 's08_05') + .3, .5)
s = 's09'; add(fx, steps(2.2, limp=1), Lt(s, 's09_02'), .8); add(fx, pop(), sc(s)['start'] + .2, .6); add(fx, ding(1046), Lm(s, 's09_05', .45), .4); add(fx, pop(), Lt(s, 's09_07') - .1, .8)
s = 's10'; add(fx, pop(), sc(s)['start'] + .2, .6); add(fx, pop(), Lt(s, 's10_06'), .5)
s = 's11'; add(fx, pop(), sc(s)['start'] + .2, .6); add(fx, pop(), Lt(s, 's11_03') + .2, .5); add(fx, steps(2.4), Lt(s, 's11_07') + .3, .4); add(fx, pop(), Lm(s, 's11_07', .7), .6)
s = 's12'; add(fx, steps(2.0), Lt(s, 's12_02'), .5); add(fx, pop(), Lt(s, 's12_05') + .1, .5); add(fx, steps(3.0), Lt(s, 's12_09') + .3, .4)
s = 's13'; add(fx, pop(), Lt(s, 's13_03') + .5, .5); add(fx, pop(), Lt(s, 's13_07') - .1, .8)
s = 's14'; board = Lt(s, 's14_07') - .05; off = Lm(s, 's14_07', .72)
add(fx, engine(max(.5, board - sc(s)['start'] - .2)), sc(s)['start'] + .2, .45); add(fx, steps(2.0, limp=1), sc(s)['start'] + .6, .7)
add(fx, hiss_door(), board, .7); add(fx, engine(off - board + .5, rise=1), board + .2, .6)
add(fx, ding(1568), off - .05, .5); add(fx, whoosh(.8), off, .5)
add(fx, pop(), Lt(s, 's14_11') + .2, .4)
s = 's15'; add(fx, flutter(.8), Lt(s, 's15_05'), .8); add(fx, flutter(1.4), Lt(s, 's15_08') - .1, .9)
s = 's16'
for lid in ('s16_02', 's16_04', 's16_06'): add(fx, whoosh(.3), Lt(s, lid) - .2, .5)
for lid, f in [('s16_02', .4), ('s16_03', .4), ('s16_05', .2)]: add(fx, pop(), Lm(s, lid, f) + .2, .45)
add(fx, pop(), Lm(s, 's16_07', .3), .6)
s = 's17'; add(fx, pop(), Lt(s, 's17_01'), .5); add(fx, pop(), Lt(s, 's17_02'), .5); add(fx, ding(1568), Lt(s, 's17_03') + .2, .5); add(fx, pop(), Lt(s, 's17_04') + .3, .6); add(fx, coo(), Le(s, 's17_04') + .2, .8)

# ---------------------------------------------------------------- narration
vo = np.zeros(N); voice_env = np.zeros(N)
for sid in T['order']:
    for lid, (t, d, who) in sc(sid)['L'].items():
        x, sr = sf.read(os.path.join(VO, lid + '.wav'), dtype='float32')
        if x.ndim > 1: x = x.mean(1)
        if sr != SR: x = resample_poly(x, SR, sr)
        rms = np.sqrt(np.mean(x[np.abs(x) > .01] ** 2)) if np.any(np.abs(x) > .01) else .1; x = x * (.11 / rms)
        add(vo, x, sc(sid)['start'] + t); add(voice_env, np.ones(len(x)), sc(sid)['start'] + t)
duck = 1 - .55 * movavg(np.minimum(voice_env, 1), int(.25 * SR))
mix = vo * 1.0 + music_out * .55 * duck + pad * .55 + amb * duck + fx * .55
mix = mix / max(1e-6, np.max(np.abs(mix))) * .89
sf.write(OUT, mix.astype(np.float32), SR)
print('wrote', OUT, round(len(mix) / SR, 1), 's')
