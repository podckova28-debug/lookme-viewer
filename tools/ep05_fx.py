"""Comic captions and SFX bursts for ep5, placed by scene-local times from out/e5_cut.timeline.json."""
import json
tl = {s['id']: s['start'] for s in json.load(open('out/e5_cut.timeline.json'))}
F = lambda b, t: int(round((tl[b] + t) * 24)); fx = []
def burst(b, t0, t1, x, y, text, rot=-8, size=100): fx.append({"type": "burst", "f0": F(b, t0), "f1": F(b, t1), "x": x, "y": y, "text": text, "size": size, "rot": rot})
def cap(b, t0, t1, line, x=60, y=50): fx.append({"type": "caption", "f0": F(b, t0), "f1": F(b, t1), "x": x, "y": y, "lines": [line], "size": 72})
cap('01', 0.3, 2.4, '6:58 AM')
burst('04', 1.2, 2.2, 880, 170, 'FWOOSH!', 8)
cap('05', 1.6, 4.8, '$9.99 / MONTH / PER FINGER')
cap('06', 0.3, 3.4, 'FINGERS PAID: 1')
cap('07', 1.6, 4.4, 'FAILED: 4 TIMES')
cap('08', 0.4, 4.4, 'HEART RATE: 164')
burst('09', 1.3, 2.1, 1500, 330, 'BONK!', -8)
burst('10', 1.3, 2.3, 1250, 330, 'ZAP!', 8)
burst('12', 1.8, 2.35, 1350, 330, 'SNAP!', -8)
burst('13', 1.6, 2.6, 1400, 260, 'CLICK!', 8)
cap('15', 1.8, 3.9, 'FREE TRIAL ENDED')
burst('16', 0.1, 0.9, 1560, 200, 'THUD!', -8)
cap('18', 1.6, 4.8, 'PAID BY: DAVE')
json.dump(fx, open('assets/ep05/fx.json', 'w'), indent=1)
