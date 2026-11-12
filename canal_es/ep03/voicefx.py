"""Voice colour for the animals, applied to a folder of line WAVs before layout (so durations already include it).
usage: python voicefx.py SRC_DIR DST_DIR
Speed/pitch by resampling (small animals faster and higher, Pepe a touch slower and deeper); the mosquito gets a faint wing buzz.
Everyone else is copied as is."""
import json, os, shutil, sys
import numpy as np, soundfile as sf
from scipy.signal import resample_poly

HERE = os.path.dirname(os.path.abspath(__file__)); SRC, DST = sys.argv[1], sys.argv[2]; os.makedirs(DST, exist_ok=True)
RATE = {'bigotes': 1.1, 'mosquito': 1.12}   # >1: faster and higher. The delivered voices are already pitched per animal; only the two smallest get a little more
lines = json.load(open(os.path.join(HERE, 'vo_lines.json'), encoding='utf-8'))
for l in lines:
    s, d = os.path.join(SRC, l['id'] + '.wav'), os.path.join(DST, l['id'] + '.wav'); r = RATE.get(l['who'])
    if not r: shutil.copy(s, d); continue
    x, sr = sf.read(s, dtype='float32'); x = x.mean(1) if x.ndim > 1 else x
    up, down = 100, int(round(100 * r)); y = resample_poly(x, up, down)          # played back at sr: r times faster, r times higher
    if l['who'] == 'mosquito':
        t = np.arange(len(y)) / sr; y = y * (1 + .12 * np.sin(2 * np.pi * 34 * t)) + .012 * np.sign(np.sin(2 * np.pi * 410 * t)) * np.abs(y).max()
    sf.write(d, (y / max(1e-6, np.abs(y).max()) * .9).astype(np.float32), sr)
print(len(lines), 'lines ->', DST)
