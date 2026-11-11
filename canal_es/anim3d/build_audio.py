"""Voice + ambience for the 3D rain shot. usage: python build_audio.py VO_DIR OUT.wav  -> prints the cues JSON
Lines s08_02..s08_05 from the episode; rain until the clap, a clap, then the low frozen-time pad."""
import json, sys, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, resample_poly
VO, OUT = sys.argv[1], sys.argv[2]; SR = 48000; rng = np.random.default_rng(3)
def load(i):
    x, sr = sf.read(f'{VO}/{i}.wav'); x = x.mean(1) if x.ndim > 1 else x
    return resample_poly(x, SR // 1000, sr // 1000) if sr != SR else x
L = {i: load(i) for i in ['s08_02', 's08_03', 's08_04', 's08_05']}; d = {i: len(x) / SR for i, x in L.items()}
at = {'s08_02': 1.0}; tc = at['s08_02'] + d['s08_02'] + .1
at['s08_03'] = tc + .8; at['s08_04'] = at['s08_03'] + d['s08_03'] + .5; at['s08_05'] = at['s08_04'] + d['s08_04'] + .7
end = at['s08_05'] + d['s08_05'] + 1.3; n = int(end * SR); out = np.zeros(n); t = np.arange(n) / SR
for i, x in L.items(): a = int(at[i] * SR); x = x / (np.sqrt(np.mean(x[np.abs(x) > .01] ** 2)) + 1e-9) * .11; out[a:a + len(x)] += x[:n - a]
bp = lambda x, lo, hi: sosfilt(butter(2, [lo, hi], 'bandpass', fs=SR, output='sos'), x)
rain = bp(rng.standard_normal(n), 400, 6000) * .05 * (t < tc) * np.minimum(1, t / .5)
clap = np.zeros(n); k = int(tc * SR); m = int(.09 * SR); clap[k:k + m] = bp(rng.standard_normal(m), 900, 5000) * np.exp(-np.arange(m) / SR * 60) * .9
pad = sum(np.sin(2 * np.pi * f * t) for f in (110, 164.8, 220)) * .012 * np.clip((t - tc) / 1.2, 0, 1) * np.clip((end - t) / 1.0, 0, 1)
mix = out + rain + clap + pad; mix *= .89 / np.max(np.abs(mix)); sf.write(OUT, mix.astype(np.float32), SR)
print(json.dumps({'clap': round(tc, 3), 'walk': round(at['s08_04'] + .2, 3), 'end': round(end, 3)}))
