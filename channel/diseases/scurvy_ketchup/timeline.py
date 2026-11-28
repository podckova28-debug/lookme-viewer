"""Smallpox (food-and-drinks format): one frame per VO line, quick settle (no zoom), section pauses, music.
python3 timeline.py -> timeline.json ; build_whatif.py timeline.json out.mp4"""
import json, os, wave
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
VO = 'voices/scurvy_ketchup/fast'
def dur(i):
    w = wave.open(os.path.join(REPO, VO, i + '.wav')); return w.getnframes() / w.getframerate()
ids = [l.split('|')[0] for l in open(os.path.join(REPO, 'voices/scurvy_ketchup/lines.txt')) if l.strip()]
shots, vo, marks = [], [], {}
t = 0.3
for k, i in enumerate(ids):
    if k and i[0] != ids[k - 1][0]: t += .28            # chapter break: 0.5 s total, as in the food channel
    if i[0] not in marks: marks[i[0]] = t
    d = dur(i); seg = d + .22   # audio-driven, like ketchup: 0.22 s between lines, no minimum
    vo.append({'file': f'{VO}/{i}.wav', 't': round(t + .03, 3)})
    shots.append({'img': i, 'from': [.5, .5, 1.02], 'to': [.5, .5, 1.0], 'settle': .25, 't0': round(t, 3), 't1': round(t + seg, 3)})
    t += seg
shots[0]['t0'] = 0.0
for a, b in zip(shots, shots[1:]): a['t1'] = b['t0']
TOTAL = round(t + 1.5, 3); shots[-1]['t1'] = TOTAL; shots[-1]['fade_out'] = 1.0
G = .4
music = [{'file': 'channel/diseases/music/tavern_bed_90s.mp3', 't0': 0, 't1': 'ALL', 'gain': G, 'fade_in': 1.0, 'fade_out': 3}]   # same bed as the food-and-drinks channel
spec = {'base': 'channel/diseases/scurvy_ketchup/f', 'fade_in': .3, 'music': music, 'shots': shots, 'texts': [], 'vo': vo, 'sfx': [], 'duration': TOTAL, 'vignette': 0}
json.dump(spec, open(os.path.join(HERE, 'timeline.json'), 'w'), indent=1)
print(len(shots), 'shots', f'{TOTAL:.1f} s')
for c, s in marks.items(): print(c, f'{int(s // 60)}:{int(s % 60):02d}')
