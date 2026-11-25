"""Proof of the cut-out pipeline: E1A (attic 1820, hero walks in, coughs, sees blood) + C03 (the White Lady appears).
python3 proof.py -> proof.json ; python3 ../tools/build_whatif.py proof.json proof.mp4
"""
import json, os, wave, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
VO = 'voices/whatif04_tb'
def dur(i):
    w = wave.open(os.path.join(REPO, VO, i + '.wav')); return w.getnframes() / w.getframerate()
N = lambda text, x, y, tx=None, ty=None, **k: dict(text=text, x=x, y=y, **({'tx': tx, 'ty': ty} if tx is not None else {}), **k)

d1, d2 = dur('E1A'), dur('C03')
t1 = .3 + d1 + .4
HERO = {'sprite': 'hero1820_walk', 'x': 250, 'to_x': 820, 'move': [0, 2.4], 'y': 990, 'h': 600,
        'poses': [[0, 'hero1820_walk'], [2.4, 'hero1820_stand'], [d1 * .55, 'hero1820_cough'], [d1 * .55 + 1.6, 'hero1820_hanky']],
        'cough': [[d1 * .55, d1 * .55 + 1.4]]}
LADY = {'sprite': 'lady_stand', 'x': 1420, 'y': 965, 'h': 700, 'fade_in': [.2, 1.4], 'phase': 1.3}
HERO2 = dict(HERO, x=820, to_x=820, move=[0, 0], poses=[[0, 'hero1820_hanky']], cough=[])
shots = [
 {'img': 'attic1820', 'from': [.5, .5, 1.0], 'to': [.5, .5, 1.0], 't0': 0, 't1': t1, 'actors': [HERO]},
 {'img': 'attic1820', 'from': [.5, .5, 1.0], 'to': [.5, .5, 1.0], 't0': t1, 't1': t1 + d2 + 1.6, 'actors': [HERO2, LADY]},
]
hk = d1 * .55 + 1.6
texts = [
 {'style': 'day', 'text': 'Century 1: London, 1820', 't0': .2, 't1': t1, 'pop': True},
 {'style': 'note', 't0': hk + .3, 't1': t1, **N('a red spot', 470, 520, 815, 640)},
 {'style': 'note', 't0': t1 + .6, 't1': t1 + d2 + 1.6, **N('Tuberculosis', 1700, 230, 1460, 300)},
 {'style': 'note', 't0': t1 + .6, 't1': t1 + d2 + 1.6, **N('(yes, the disease herself)', 1700, 300, size=46)},
]
vo = [{'file': f'{VO}/E1A.wav', 't': .3}, {'file': f'{VO}/C03.wav', 't': t1 + .3}]
spec = {'base': 'channel/diseases/whatif04_tb/bg', 'sprite_base': 'channel/diseases/whatif04_tb/sprites', 'fade_in': .3,
        'music': [{'file': 'channel/diseases/music/cholera_a.mp3', 't0': 0, 't1': 'ALL', 'gain': .5, 'fade_in': 1, 'fade_out': 1.5}],
        'shots': shots, 'texts': texts, 'vo': vo, 'sfx': [], 'duration': round(t1 + d2 + 1.6, 2)}
shots[-1]['fade_out'] = .8
json.dump(spec, open(os.path.join(HERE, 'proof.json'), 'w'), indent=1)
print(spec['duration'])
