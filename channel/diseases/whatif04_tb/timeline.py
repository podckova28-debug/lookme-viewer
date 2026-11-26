"""What If #4 (consumption, London 1850): stage structure MIRROR -> HANDKERCHIEF -> ATLAS -> DOCTOR, stage label top-left.
python3 timeline.py -> timeline.json ; qc.py timeline.json qc_groups.json ; build_whatif.py timeline.json out.mp4
"""
import json, os, wave
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
VO = 'voices/whatif04_tb/fast'
def dur(i):
    w = wave.open(os.path.join(REPO, VO, i + '.wav')); return w.getnframes() / w.getframerate()
N = lambda text, x, y, tx=None, ty=None, **k: dict(text=text, x=x, y=y, **({'tx': tx, 'ty': ty} if tx is not None else {}), **k)

PLAN = [
 ('C01', ['c01a', 'c01b'], {'cap': 'London, 1850', 'notes': {'c01b': [N('the look', 600, 250, 1010, 385)]}}),
 ('C02', ['c02a'], {'cap': 'An actual quote'}),
 ('C03', ['c03a'], {'notes': {'c03a': [N('Tuberculosis', 760, 300, 1150, 440), N('(yes, the disease herself)', 760, 370, size=46)]}}),
 ('C04', ['c04n'], {'big': '3 years', 'title': 'What happens if you get consumption in 1850'}),
 ('P01', ['p01o', 'p01a'], {'day': 'How you caught it'}),
 ('P02', ['p02a', 'atlas0'], {'notes': {'p02a': [N('the prison', 1500, 220, 1150, 470)]}}),
 ('P02B', ['p02b'], {'notes': {'p02b': [N('a waxy coat', 420, 990, 560, 760), N('one split a day', 1300, 990, 1330, 780, at=.5)]}}),
 ('P03', ['p03s'], {'cap': 'Most adults in London'}),
 ('P04', ['p04a'], {}),
 ('P05', ['p05r', 'p05a'], {'notes': {'p05a': [N('breaking out', 330, 330, 720, 530)]}}),
 ('M1A', ['mc1'], {'day': 'Month 1', 'notes': {'mc1': [N('just tired', 1500, 300, 1080, 420)]}}),
 ('M1B', ['m_hanky'], {'cap': 'Still clean'}),
 ('M1C', ['at1'], {'notes': {'at1': [N('breaking out', 420, 250, 790, 380)]}}),
 ('M1E', ['m1e'], {'notes': {'m1e': [N('mucus', 1050, 980, 1250, 700)]}}),
 ('M1D', ['m1d'], {'cap': 'Cod liver oil', 'notes': {'m1d': [N('(it has vitamin D)', 1400, 690, 940, 520)]}, 'card': 'm1', 'card_x': 1200}),
 ('M6A', ['mc2'], {'day': 'Month 6', 'notes': {'mc2': [N('the hectic flush', 1500, 330, 1080, 470)]}}),
 ('M6F', ['m6f1', 'm6f2'], {'notes': {'m6f1': [N('the thermostat', 1450, 160, 1080, 300, at=.25)], 'm6f2': [N('wide open', 1150, 990, 1330, 780, at=.35)]}}),
 ('M6B', ['m6b'], {'notes': {'m6b': [N('soaked', 1050, 560, 640, 640)]}}),
 ('M6G', ['m6g1', 'm6g2'], {'notes': {'m6g2': [N('burning its own fuel', 1580, 820, 1355, 380, at=.3)]}}),
 ('M6C', ['hk2'], {'notes': {'hk2': [N('a pink speck', 1100, 420, 735, 670)]}}),
 ('M6D', ['m6d'], {'cap': 'Leeches', 'strike': True}),
 ('M6E', ['m6e'], {'card': 'm6', 'card_x': 1200}),   # the card sits beside the Lady, not over the pink speck
 ('Y1A', ['y1a', 'hk3'], {'day': 'Year 1'}),
 ('Y1B', ['at2'], {'notes': {'at2': [N('a hole', 420, 250, 760, 380), N('a broken vessel', 420, 650, 770, 470)]}}),
 ('Y1F', ['y1f'], {'notes': {'y1f': [N('like cheese', 960, 1000, 935, 640, at=.3)]}}),
 ('Y1C', ['y1c'], {'notes': {'y1c': [N('next', 1450, 250, 1040, 500)]}}),
 ('Y1D', ['y1d'], {'cap': 'Spes phthisica: the hope of the consumptive'}),
 ('Y1E', ['y1e'], {'cap': 'Go south. On a clerk\'s wages.', 'card': 'y1', 'card_x': 1150}),
 ('Y2A', ['mc4'], {'day': 'Year 2', 'notes': {'mc4': [N('the look. fashionable.', 1480, 300, 1090, 420)]}}),
 ('Y2B', ['y2b'], {}),
 ('Y2I', ['y2i'], {'notes': {'y2i': [N('voice box', 1560, 640, 1390, 440)]}}),
 ('Y2C', ['at3'], {}),
 ('Y2D', ['y2d'], {'big': '3 paths'}),
 ('Y2E', ['y2e'], {'cap': 'Path 1: galloping consumption'}),
 ('Y2F', ['y2f'], {'cap': 'Path 2: years of coughing'}),
 ('Y2G', ['at4', 'y2g'], {'cap': 'Path 3: the walls hold', 'notes': {'at4': [N('a scar for life', 420, 250, 765, 425)]}}),
 ('Y2H', ['y2h'], {}),
 ('T01', ['t01'], {'day': 'Today', 'notes': {'t01': [N('the spot', 1640, 520, 1250, 300)]}}),
 ('T02', ['t02'], {'cap': '4 drugs, 6 months. Don\'t stop.'}),
 ('T03', ['t03'], {'cap': 'About 1.2 million deaths a year'}),
 ('T04', ['t04'], {}),
 ('E01', ['e01'], {'cap': 'Which path would you get?'}),
]
OR, RD, PU, BL, GR = (230, 120, 40), (230, 60, 60), (170, 90, 160), (90, 150, 220), (90, 190, 90)
CARDS = {
 'm1': ([('WEIGHT', '-2 KG', .15, BL), ('FEVER', 'SLIGHT', .2, OR), ('COUGH', 'DRY', .3, PU)], 'TIRED'),
 'm6': ([('WEIGHT', '-6 KG', .45, BL), ('FEVER', 'EVERY AFTERNOON', .6, OR), ('COUGH', 'WET', .6, PU)], 'ANXIOUS'),
 'y1': ([('WEIGHT', '-11 KG', .75, BL), ('FEVER', 'DAILY', .8, OR), ('COUGH', 'BLOOD', .9, RD)], 'STRANGELY HOPEFUL'),
}
SECTION = {'P01', 'M1A', 'M6A', 'Y1A', 'Y2A', 'T01', 'E01'}
CARD_MIN = 3.6
shots, texts, vo, sfx, marks = [], [], [], [], {}
used = set()
def shot(f, a, b):
    shots.append({'img': f, 'from': [.5, .5, 1.025], 'to': [.5, .5, 1.0], 'settle': .3, 't0': round(a, 3), 't1': round(b, 3)})
def card(name, a, b, x=440):
    rows, mood = CARDS[name]; ch = 130 + 100 * len(rows) + 90
    texts.append({'style': 'card', 'x': x, 'y': (1080 - ch) // 2, 'dim': True, 'rows': [list(r[:3]) + [list(r[3])] for r in rows], 'mood': mood, 't0': a + .1, 't1': b, 'pop': True})
    sfx.append({'kind': 'shutter', 't': round(a + .1, 3), 'gain': .3})
t = 0.3
for i, frames, tx in PLAN:
    frames = [f for f in frames if f not in used] or frames   # a frame is shown once only (mc1 opens the title, then Month 1 reuses nothing)
    if i in SECTION: t += .35
    d = dur(i); seg = max(2.2, d + (.15 if i[0] != 'E' else .4)); t0 = t; marks[i] = t0
    vo.append({'file': f'{VO}/{i}.wav', 't': round(t0 + .03, 3)})
    n = len(frames)
    if 'card' in tx and n > 1:
        last = max(CARD_MIN, seg / n); rest = (seg - last) / (n - 1); lens = [rest] * (n - 1) + [last]
    else:
        lens = [seg / n] * n
    tt = t0; starts = {}
    for f, ln in zip(frames, lens):
        shot(f, tt, tt + ln); starts[f] = (tt, tt + ln); tt += ln; used.add(f)
    t1 = t0 + seg
    if 'cap' in tx: texts.append({'style': 'cap', 'text': tx['cap'], 't0': t0 + .15, 't1': (starts[frames[-1]][0] if 'card' in tx else t1 - .05), 'maxw': 1500, 'pop': True})
    if 'big' in tx:
        bt = t0 + d * .45; texts.append({'style': 'big', 'text': tx['big'], 't0': bt, 't1': min(bt + 1.8, t1), 'pop': True})
    if 'title' in tx:
        big_end = max([x['t1'] for x in texts if x['style'] == 'big' and x['t0'] >= t0] or [0])
        texts.append({'style': 'cap', 'text': tx['title'], 'y': 540, 'size': 96, 'maxw': 1700, 't0': max(starts[frames[-1]][0] + .2, big_end + .15), 't1': t1 + 1.6, 'pop': True})
    for f, notes in tx.get('notes', {}).items():
        if f not in starts: continue
        a, b = starts[f]
        for nn in notes:
            nn = dict(nn); at = nn.pop('at', 0)   # 'at': when the note appears, as a fraction of the shot
            texts.append({'style': 'note', 't0': a + .25 + at * (b - a), 't1': b, **nn})
    if 'card' in tx:
        a, b = starts[frames[-1]]; card(tx['card'], max(a, b - CARD_MIN), b, tx.get('card_x', 440))   # the scene shows first, the card only at the end
    if tx.get('strike'):
        st0 = t0 + max(1.0, d * .55)
        texts.append({'style': 'strike', 'text': tx['cap'], 'maxw': 1500, 't0': st0, 't1': t1 - .05})
        sfx.append({'kind': 'page', 't': round(st0, 3), 'gain': .6})
    t = t1
    if 'day' in tx: texts.append({'style': 'day', 'text': tx['day'], 't0': t0, 't1': t + 2.0, 'pop': True})
    if i == 'C04': t += 1.6; shots[-1]['t1'] = round(t, 3)
shots[0]['t0'] = 0.0
DAYS = sorted([x for x in texts if x['style'] == 'day'], key=lambda x: x['t0'])
for a, b in zip(DAYS, DAYS[1:]): a['t1'] = min(a['t1'], b['t0'] - .1)
for a, b in zip(shots, shots[1:]): a['t1'] = b['t0']
shots[-1]['t1'] = round(t + 1.2, 3); shots[-1]['fade_out'] = 1.0; TOTAL = round(t + 1.2, 3)
mt = lambda i: round(marks[i], 2)
G = .55
music = [
 {'file': 'channel/diseases/music/cholera_a.mp3', 't0': 0, 't1': mt('M6A') + 1, 'gain': G, 'fade_in': 1.5, 'fade_out': 3},
 {'file': 'channel/diseases/music/cholera_b.mp3', 't0': mt('M6A') - 1, 't1': mt('T01') + 1, 'gain': G, 'fade_in': 3, 'fade_out': 3},
 {'file': 'channel/diseases/music/cholera_a.mp3', 't0': mt('T01') - 1, 't1': 'ALL', 'gain': G, 'fade_in': 3, 'fade_out': 3},
]
spec = {'base': 'channel/diseases/whatif04_tb/f2', 'fade_in': .3, 'music': music, 'shots': shots, 'texts': texts, 'vo': vo, 'sfx': sfx, 'duration': TOTAL}
json.dump(spec, open(os.path.join(HERE, 'timeline.json'), 'w'), indent=1)
print(f'{len(shots)} shots ({len({s["img"] for s in shots})} unique), {TOTAL:.1f} s')
for i in sorted(SECTION, key=lambda k: marks[k]): print(i, f'{int(marks[i] // 60)}:{int(marks[i] % 60):02d}')
