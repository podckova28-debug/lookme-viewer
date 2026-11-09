"""Раскладка: длины планов по репликам, сквозные отрезки для повторяющихся клипов."""
import json
from shotmap import SHOTS
L = json.load(open('lines.json'))
def plan():
    t = 0.0; shots = []; used = {}; marks = {}
    for l in L:
        T = l['T']; ws = SHOTS[l['id']]; tot = sum(w for _, w in ws); st = t
        for name, w in ws:
            d = T * w / tot
            off = used.get(name, 0.0)
            shots.append(dict(name=name, line=l['id'], t=st, d=d, off=off))
            marks.setdefault(name, []).append((off, off + d))
            used[name] = off + d; st += d
        t += T
    return shots, used, marks, t
if __name__ == '__main__':
    shots, used, marks, total = plan()
    print('итого', round(total, 1))
    for k in sorted(used):
        print(k, round(used[k], 2), [tuple(round(x, 2) for x in mm) for mm in marks[k]])
