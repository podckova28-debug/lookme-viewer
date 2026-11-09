"""Comic captions and SFX bursts for ep2, placed by block-local times from out/e2_cut.timeline.json.
usage: python3 tools/ep02_fx.py  -> assets/ep02/fx_ep02.json"""
import json
tl = {s['id']: s['start'] for s in json.load(open('out/e2_cut.timeline.json'))}
F = lambda b, t: int(round((tl[b] + t) * 24))
fx = []
def burst(b, t0, t1, x, y, text, rot=-8, size=100): fx.append({"type": "burst", "f0": F(b, t0), "f1": F(b, t1), "x": x, "y": y, "text": text, "size": size, "rot": rot})
def cap(b, t0, t1, line, x=60, y=50): fx.append({"type": "caption", "f0": F(b, t0), "f1": F(b, t1), "x": x, "y": y, "lines": [line], "size": 72})
cap('01', 0.2, 2.0, '7:02 AM')
burst('01', 2.3, 3.1, 1450, 220, 'STUB!', 8)
burst('01', 5.3, 6.3, 1450, 200, 'CRUNCH!', -8)
burst('03', 4.5, 5.4, 1500, 200, 'CRUNCH!', 10)
burst('05a', 2.2, 3.1, 1500, 260, 'RIIIP!', -8)
cap('05b', 0.2, 2.9, 'JEANS DESTROYED: 3')
burst('06', 0.8, 1.8, 1450, 420, 'HONK!', 8)
burst('06', 8.6, 9.6, 520, 240, 'CRUNCH!', -8)
cap('08b', 0.2, 2.7, 'ON HOLD: 40 MIN')
burst('08b', 2.9, 3.8, 1450, 240, 'CRUNCH!', 8)
cap('12a', 1.4, 3.7, 'ANGER LEVEL: 0')
burst('13', 0.2, 1.1, 1500, 200, 'CREAK!', -8)
burst('13', 2.9, 3.8, 1450, 220, 'THUD!', 8)
json.dump(fx, open('assets/ep02/fx_ep02.json', 'w'), indent=1)
