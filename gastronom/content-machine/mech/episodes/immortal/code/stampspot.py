"""Подбор места штампа без голов: для каждого штампа пробует углы кадра, считает перекрытие голов (renderqa) и плашек."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'qa'))
import renderqa as R
from imgutils.detect import detect_heads
import numpy as np
cut, shots, total = R.load(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ws = R.windows(cut, shots)
CAND = [(1560, 270), (400, 270), (1560, 820), (400, 820), (960, 230)]
for w in ws:
    ov = w['ov']
    if ov.get('type') != 'stamp': continue
    others = [o for o in ws if o is not w and o['st'] < w['en'] and o['en'] > w['st'] and o['ov'].get('type') != 'stamp']
    best = None
    for x, y in CAND:
        ov['x'], ov['y'] = x, y; worst = 0; clash = 0
        for T in R.show_times(w, shots):
            m, _ = R.mask_at(cut, w, T); bg, s = R.background(cut, shots, T)
            for (x0, y0, x1, y1), _, sc in detect_heads(bg, conf_threshold=0.35):
                x0, y0, x1, y1 = map(int, (x0, y0, x1, y1)); worst = max(worst, m[y0:y1, x0:x1].sum() / max(1, (x1 - x0) * (y1 - y0)))
            for o in others:
                if o['st'] <= T < o['en']:
                    mo, _ = R.mask_at(cut, o, T); clash = max(clash, (m & mo).sum() / max(1, m.sum()))
        score = worst + clash
        print(w['name'], (x, y), f'головы {worst:.2f} плашки {clash:.2f}', flush=True)
        if best is None or score < best[0]: best = (score, x, y)
    print('>>', w['name'], 'лучшее', best[1:], f'{best[0]:.2f}', flush=True)
