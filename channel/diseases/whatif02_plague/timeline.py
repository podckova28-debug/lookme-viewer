"""What If #2 (plague): build the montage timeline from the VO lengths.
python3 timeline.py -> timeline.json ; then python3 ../tools/build_whatif.py timeline.json out.mp4
Shots are at most ~2.5 s: a long line gets several frames, and a frame that has to stay longer is split into two camera moves.
"""
import json, os, wave
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
VO = 'voices/whatif02_plague'
def dur(i):
    w = wave.open(os.path.join(REPO, VO, i + '.wav')); return w.getnframes() / w.getframerate()

# line -> frames, and optional texts {'cap': str, 'day': str, 'big': str, 'card': key, 'stamp': str, 'title': str}
PLAN = [
 ('C01', ['t00', 'c01b'], {'cap': 'Florence, June 1348'}),
 ('C02', ['c02a', 't01'], {}),
 ('C03', ['t02', 'c03b'], {}),
 ('C04', ['c04a', 'c04a'], {'big': '50/50', 'title': 'What happens if you catch the Black Death'}),
 ('H01', ['h01a', 'h01b'], {'day': 'Day 0'}),
 ('H02', ['h02b', 't01'], {'cap': 'It spits them into you'}),
 ('H03', ['h03a', 'h03b'], {'cap': 'Yersinia pestis'}),
 ('H04', ['h04a'], {}),
 ('H05', ['h05a'], {'card': 'd0'}),
 ('H06', ['h06a', 'h06b', 'h06c'], {'day': 'Day 1-2'}),
 ('H07', ['h07a', 'h07b', 'h07a'], {'cap': 'Lymph node'}),
 ('H08', ['h08a', 'h08b'], {}),
 ('H09', ['h09a'], {}),
 ('H10', ['h10a'], {'day': 'Day 3'}),
 ('H11', ['h11a', 'h11b'], {'big': '39.5°C'}),
 ('H12', ['h12a', 'h12b'], {}),
 ('H13', ['t03'], {'card': 'd3'}),
 ('H14', ['t04', 'h14b'], {'day': 'Day 4'}),
 ('H15', ['h15a', 'h15a'], {'cap': 'Bubo'}),
 ('H16', ['h16a', 'h16b'], {'cap': 'Egg. Then apple.'}),
 ('H17', ['h17a', 'h17b'], {'card': 'd4'}),
 ('H18', ['h18a'], {'day': 'Day 5'}),
 ('H19', ['t05', 'h19b'], {'cap': 'The best test of 1348'}),
 ('H20', ['h20a', 'h20b'], {'cap': 'Diagnosis: bad air'}),
 ('H21', ['h21a'], {}),
 ('H22', ['h22a', 'h22b'], {'cap': 'Step 1: bloodletting', 'stamp': True}),
 ('H23', ['h23a', 'h23b'], {'cap': 'Step 2: theriac', 'stamp': True}),
 ('H24', ['h24a', 'h24b'], {'cap': 'Step 3: no baths', 'stamp': True}),
 ('H25', ['t06', 'h25b'], {'cap': 'Step 4: two fires', 'stamp': True}),
 ('H26', ['h26a', 'h26b'], {'cap': 'Step 5: smell flowers', 'stamp': True}),
 ('H27', ['h27a', 'h27b'], {'cap': 'Gentile da Foligno, died June 1348'}),
 ('H28', ['h28a'], {}),
 ('H29', ['h29a'], {'day': 'Day 6'}),
 ('H30', ['h30b', 'h30a'], {'cap': 'Path 1: the blood'}),
 ('H31', ['h31a', 'h31b'], {'cap': 'Path 2: the lungs'}),
 ('H32', ['h32a'], {'cap': 'Path 3: hold the line'}),
 ('H33', ['h33a'], {}),
 ('H34', ['h34a'], {'card': 'd6'}),
 ('H35', ['h35a'], {'day': 'Day 8'}),
 ('H36', ['h36a', 'h36b'], {}),
 ('H37', ['h37a'], {'card': 'd8'}),
 ('H38', ['h38a'], {}),
 ('H39', ['h39a', 'h39b', 'h39c'], {'big': '1 in 2'}),
 ('H40', ['h40a', 'h40b'], {'cap': 'They called it the great mortality', 'card': 'd30'}),
 ('T01', ['t01a'], {'day': 'Today'}),
 ('T02', ['t02a', 't02b'], {'cap': '7 cases a year in the US'}),
 ('T03', ['t03a', 't03b'], {}),
 ('T04', ['t07'], {'cap': 'Antibiotics, 10-14 days'}),
 ('T05', ['t05a'], {}),
 ('T06', ['t06a'], {}),
 ('E01', ['e01a'], {'cap': 'Which path did you get?'}),
 ('E02', ['e02a'], {'cap': 'Next: rabies'}),
]
CARDS = {  # label, value, fill, colour
 'd0':  ([('FEVER', '36.8°C', .1, (230, 120, 40)), ('PULSE', '70', .35, (230, 60, 60)), ('BUBO', 'NONE', 0, (170, 90, 160)), ('ENERGY', '100%', 1, (90, 190, 90))], 'PEACH'),
 'd3':  ([('FEVER', '39.5°C', .75, (230, 120, 40)), ('PULSE', '110', .65, (230, 60, 60)), ('BUBO', 'NONE', 0, (170, 90, 160)), ('ENERGY', '20%', .2, (90, 190, 90))], 'VERY MUCH NOT GREAT'),
 'd4':  ([('FEVER', '39.8°C', .8, (230, 120, 40)), ('PULSE', '115', .7, (230, 60, 60)), ('BUBO', 'EGG', .45, (170, 90, 160)), ('ENERGY', '15%', .15, (90, 190, 90))], "DON'T TOUCH ME"),
 'd6':  ([('FEVER', '40°C', .95, (230, 120, 40)), ('PULSE', '125', .85, (230, 60, 60)), ('BUBO', 'APPLE', .85, (170, 90, 160)), ('ENERGY', '5%', .05, (90, 190, 90))], '???'),
 'd8':  ([('FEVER', '38°C', .45, (230, 120, 40)), ('PULSE', '95', .5, (230, 60, 60)), ('BUBO', 'DRAINING', .4, (170, 90, 160)), ('ENERGY', '25%', .25, (90, 190, 90))], 'ALIVE?!'),
 'd30': ([('FEVER', '36.8°C', .1, (230, 120, 40)), ('PULSE', '72', .35, (230, 60, 60)), ('BUBO', 'GONE', 0, (170, 90, 160)), ('ENERGY', '80%', .8, (90, 190, 90))], 'NEVER AGAIN'),
}
FIXCAM = {'h07a': ([.67, .5, 1.5], [.64, .5, 1.56])}   # keep the non-stickman figure on the left out of frame
SECTION_GAP = {'H01', 'H06', 'H10', 'H14', 'H18', 'H29', 'H35', 'T01', 'E01'}
MOVES = [([.5, .5, 1.0], [.5, .5, 1.08]), ([.45, .5, 1.1], [.55, .5, 1.1]), ([.5, .48, 1.12], [.5, .5, 1.0]), ([.55, .45, 1.06], [.45, .52, 1.12]),
         ([.5, .5, 1.15], [.5, .5, 1.03]), ([.4, .55, 1.1], [.5, .45, 1.16])]

shots, texts, vo, sfx = [], [], [], []
t = 0.4; mv = 0; marks = {}
for i, frames, tx in PLAN:
    if i in SECTION_GAP: t += .5
    d = dur(i); gap = .3 if i[0] != 'E' else .5
    seg = d + gap; t0 = t; marks[i] = t0
    vo.append({'file': f'{VO}/{i}.wav', 't': round(t0 + .05, 3)})
    # split frames so no shot exceeds 2.6 s
    units = []
    per = seg / len(frames)
    for f in frames:
        n = max(1, round(per / 2.4)); units += [f] * n
    ut = seg / len(units); prev = None
    for k, f in enumerate(units):
        a, b = MOVES[mv % len(MOVES)]; mv += 1
        if f in FIXCAM: a, b = FIXCAM[f]
        if tx.get('card') and k == len(units) - 1 and f in ('h05a', 'h17b', 'h34a', 'h37a', 'h40b', 't03'):
            a, b = [.5, .5, 1.0], [.5, .5, 1.02]   # card frames stay still
        shots.append({'img': f, 'from': a, 'to': b, 't0': round(t0 + k * ut, 3), 't1': round(t0 + (k + 1) * ut, 3)})
        if f != prev and k > 0: sfx.append({'kind': 'page', 't': round(t0 + k * ut, 3), 'gain': .25})
        prev = f
    t1 = t0 + seg
    if 'cap' in tx: texts.append({'style': 'cap', 'text': tx['cap'], 't0': t0 + .2, 't1': t1 - .1, 'maxw': 1500, 'pop': True})
    if 'day' in tx: texts.append({'style': 'day', 'text': tx['day'], 't0': t0, 't1': t1 + (2.5 if i != 'T01' else 0), 'pop': True})
    if 'big' in tx:
        bt = t0 + (d * .55 if i == 'C04' else .3)
        texts.append({'style': 'big', 'text': tx['big'], 't0': bt, 't1': min(bt + 2.2, t1), 'pop': True})
    if 'title' in tx: texts.append({'style': 'cap', 'text': tx['title'], 'y': 540, 'size': 96, 'maxw': 1700, 't0': t0 + d * .55 + 2.0, 't1': t1 + 1.6, 'pop': True})
    if 'card' in tx:
        rows, mood = CARDS[tx['card']]; ct = shots[-1]['t0']
        texts.append({'style': 'card', 'rows': [list(r[:3]) + [list(r[3])] for r in rows], 'mood': mood, 't0': ct, 't1': t1, 'pop': True})
        sfx.append({'kind': 'shutter', 't': round(ct, 3), 'gain': .35})
    if 'stamp' in tx:
        st0 = t0 + max(1.2, d * .6)   # cross the treatment out a little after it is named
        texts.append({'style': 'strike', 'text': tx['cap'], 'maxw': 1500, 't0': st0, 't1': t1 - .1})
        sfx.append({'kind': 'page', 't': round(st0, 3), 'gain': .7})
    t = t1
    if i == 'C04': t += 1.6; shots[-1]['t1'] = round(t, 3)   # hold the title on the last cold-open frame
shots[-1]['t1'] = round(t + 1.5, 3); TOTAL = round(t + 1.5, 3)
shots[-1]['fade_out'] = 1.2
mt = lambda i: round(marks[i], 2)
music = [
 {'file': 'channel/diseases/music/main_theme.mp3', 't0': 0, 't1': mt('H29') + 1, 'fade_in': 1.5, 'fade_out': 2.5},
 {'file': 'channel/diseases/music/sneaky_theme.mp3', 't0': mt('H29') - 1, 't1': mt('H35') + 1, 'fade_in': 2, 'fade_out': 2.5},
 {'file': 'channel/diseases/music/main_theme.mp3', 't0': mt('H35') - .5, 't1': mt('T01') + 1, 'fade_in': 2, 'fade_out': 2.5},
 {'file': 'channel/diseases/music/today_theme.mp3', 't0': mt('T01') - .5, 't1': 'ALL', 'fade_in': 2, 'fade_out': 3},
]
spec = {'base': 'channel/diseases/whatif02_plague/frames', 'fade_in': .4, 'music': music, 'shots': shots, 'texts': texts, 'vo': vo, 'sfx': sfx, 'duration': TOTAL}
json.dump(spec, open(os.path.join(HERE, 'timeline.json'), 'w'), indent=1)
print(f'{len(shots)} shots, {TOTAL:.1f} s, avg {TOTAL / len(shots):.2f} s/shot')
for i in ['H01', 'H06', 'H10', 'H14', 'H18', 'H29', 'H35', 'T01', 'E01']:
    print(i, f'{int(marks[i] // 60)}:{int(marks[i] % 60):02d}')
