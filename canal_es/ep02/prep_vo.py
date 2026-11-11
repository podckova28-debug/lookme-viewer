"""Turn a delivered voice folder into the one the pipeline reads: one WAV per line id of vo_lines.json.
usage: python prep_vo.py SRC_DIR DST_DIR
- crowd lines come as three takes (<id>_1/_2/_3.wav): they are layered into one file, tight offsets so the words
  stay readable under music;
- every line id must be present; missing ones are listed and the script fails."""
import json, os, shutil, sys
import numpy as np, soundfile as sf
from scipy.signal import resample_poly

HERE = os.path.dirname(os.path.abspath(__file__))
SRC, DST = sys.argv[1], sys.argv[2]; os.makedirs(DST, exist_ok=True)
lines = json.load(open(os.path.join(HERE, 'vo_lines.json'), encoding='utf-8'))
missing = []
for l in lines:
    i, src = l['id'], os.path.join(SRC, l['id'] + '.wav')
    takes = [os.path.join(SRC, f"{i}_{k}.wav") for k in (1, 2, 3)]
    if all(os.path.exists(t) for t in takes):
        xs = []
        for t in takes:
            x, sr = sf.read(t); x = x.mean(1) if x.ndim > 1 else x
            if sr != 24000: x = resample_poly(x, 24000, sr)
            xs.append(x / (np.sqrt(np.mean(x ** 2)) + 1e-9) * .08)
        offs, gains = [0, int(.02 * 24000), int(.04 * 24000)], [1.0, .65, .55]
        y = np.zeros(max(o + len(x) for o, x in zip(offs, xs)))
        for o, g, x in zip(offs, gains, xs): y[o:o + len(x)] += g * x
        sf.write(os.path.join(DST, i + '.wav'), (y * .89 / np.max(np.abs(y))).astype(np.float32), 24000, subtype='PCM_16')
    elif os.path.exists(src): shutil.copy(src, os.path.join(DST, i + '.wav'))
    else: missing.append(i)
if missing: sys.exit('missing lines: ' + ' '.join(missing))
print(len(lines), 'lines ready in', DST)
