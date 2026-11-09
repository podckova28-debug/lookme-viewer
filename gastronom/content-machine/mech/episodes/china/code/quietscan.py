# Независимая проверка пауз: все тихие участки (< пик−35 дБ) длиннее 0,10 с внутри реплики,
# сопоставленные с ближайшей границей слов из распознавания. Ловит то, что окно ±0,12 с в voicecheck режет.
import json, sys, wave, numpy as np
rep = sys.argv[1]; THR = float(sys.argv[2]) if len(sys.argv) > 2 else 35
def load(f):
    w = wave.open(f); sr = w.getframerate(); ch = w.getnchannels()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
    return (x.reshape(-1, ch).mean(1) if ch > 1 else x), sr
for l in open(rep):
    r = json.loads(l); k = r['id'].rsplit('_', 1)[0]
    x, sr = load(f'vo/{k}.wav'); h = int(sr * 0.01)
    db = np.array([20 * np.log10(np.sqrt(np.mean(x[i:i + h] ** 2)) + 1e-9) for i in range(0, len(x) - h, h)])
    q = db < db.max() - THR
    runs = []; i = 0
    while i < len(q):
        if q[i]:
            j = i
            while j < len(q) and q[j]: j += 1
            runs.append((i * 0.01, j * 0.01)); i = j
        else: i += 1
    runs = [(a, b) for a, b in runs if a > 0.05 and b < len(q) * 0.01 - 0.05 and b - a > 0.10]
    for a, b in runs:
        m = (a + b) / 2
        p = min(r['pauses'], key=lambda p: abs((p['t1'] + p['t2']) / 2 - m)) if r['pauses'] else None
        tag = repr(p['p']) if p else '?'
        bad = p is None or p['p'] == '' or abs((p['t1'] + p['t2']) / 2 - m) > 0.35
        if bad: print(f"{k:5s} {a:5.2f}–{b:5.2f} ({b-a:.2f} с) после «{p['after'] if p else '?'}» знак {tag}")
