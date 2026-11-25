"""What If #2 (plague) v2, cholera look: shorter cut, ~2 s per frame, still frames with a quick settle after each cut.
python3 timeline_v2.py -> timeline_v2.json ; python3 ../tools/build_whatif.py timeline_v2.json out.mp4
"""
import json, os, wave
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
VO = 'voices/whatif02_plague/fast'   # kept lines, sped up 1.08x
def dur(i):
    w = wave.open(os.path.join(REPO, VO, i + '.wav')); return w.getnframes() / w.getframerate()

N = lambda text, x, y, tx=None, ty=None, **k: dict(text=text, x=x, y=y, **({'tx': tx, 'ty': ty} if tx is not None else {}), **k)
# line, frames, texts; 'notes' = {frame: [note, ...]}; 'card' goes on the LAST frame of the line
PLAN = [
 ('C01', ['s_market', 'c01b', 'c01c'], {'cap': 'Florence, June 1348', 'notes': {'c01c': [N('Flea', 420, 480, 640, 700)]}}),
 ('C02', ['c02a'], {'notes': {'c02a': [N('Flea', 330, 330, 680, 480)]}}),
 ('C03', ['s_plague_stall'], {'notes': {'s_plague_stall': [N('The Plague', 300, 470, 640, 280), N('(yes, the disease itself)', 300, 540, size=46)]}}),
 ('C04', ['c04b', 'c04c'], {'big': '50/50', 'title': 'What happens if you catch the Black Death'}),
 ('H01', ['h01a', 'h01c'], {'day': 'Day 0', 'notes': {'h01a': [N('Blocked gut', 1050, 140, 800, 330)]}}),
 ('H02', ['h02a', 'h02c'], {'cap': 'It spits them into you'}),
 ('H05', ['h05b', 's_market'], {'card': 'd0'}),
 ('H06', ['h06a', 'h06c'], {'day': 'Day 1-2'}),
 ('H07', ['diag_bubo', 'h07b', 'h07d'], {'cap': 'Lymph node'}),
 ('H10', ['room_d3'], {'day': 'Day 3', 'notes': {'room_d3': [N('39.5°C', 470, 260, 720, 330)]}}),
 ('H11', ['h11a', 'h11b'], {}),
 ('H13', ['h13b', 'h13a'], {'card': 'd3'}),
 ('H14', ['room_d4', 'h14d'], {'day': 'Day 4', 'notes': {'room_d4': [N('Egg-sized', 380, 560, 720, 790)]}}),
 ('H15', ['h15a', 'h15c'], {'cap': 'Bubo'}),
 ('H18', ['h18b', 'h18c'], {'day': 'Day 5'}),
 ('H19', ['h19b', 'h19c'], {'cap': 'The best test of 1348'}),
 ('H20', ['h20a', 'h20c', 'h20d'], {'cap': 'Diagnosis: bad air'}),
 ('H21', ['h21a'], {}),
 ('H22', ['h22a', 'room_d5_blood', 'h22c'], {'cap': 'Step 1: bloodletting', 'strike': True,
         'notes': {'room_d5_blood': [N('Your blood', 1500, 640, 1010, 690), N('(you needed that)', 1500, 720, size=48)]}}),
 ('H23', ['h23a', 'h23b', 'h23d'], {'cap': 'Step 2: theriac', 'strike': True,
         'notes': {'h23b': [N('Roasted viper', 1560, 170, 1140, 250)]}}),
 ('H24', ['h24a', 'h24b'], {'cap': 'Step 3: no baths', 'strike': True}),
 ('H25', ['h25b', 'h25d', 'h25e'], {'cap': 'Step 4: two fires', 'strike': True,
         'notes': {'h25d': [N('The Pope. Seriously.', 480, 170, 880, 380)]}}),
 ('H29', ['h29a'], {'day': 'Day 6'}),
 ('H30', ['h30a', 'h30b', 'h30d', 'h30f'], {'cap': 'Path 1: the blood'}),
 ('H31', ['h31a', 'h31d', 'h31e', 'h31f'], {'cap': 'Path 2: the lungs'}),
 ('H32', ['h32b', 'h32c'], {'cap': 'Path 3: hold the line'}),
 ('H33', ['h33a'], {}),
 ('H34', ['room_d6', 'h34c', 'h34a'], {'card': 'd6', 'notes': {'room_d6': [N('40°C', 330, 250, 640, 420), N('Apple-sized', 1560, 860, 1230, 720)]}}),
 ('H35', ['h35b'], {'day': 'Day 8'}),
 ('H36', ['h36a', 'h36c', 'h36d'], {}),
 ('H37', ['h37b', 'h37a'], {'card': 'd8'}),
 ('H38', ['h38a'], {}),
 ('H39', ['h39a', 'h39b', 'h39d', 'h39e'], {'card': 'd30', 'bigat': ('h39b', '1 in 2')}),
 ('T01', ['t01a'], {'day': 'Today'}),
 ('T03', ['t03a', 't03b', 't03d'], {}),
 ('T04', ['t04a', 't04c'], {'cap': 'Antibiotics, 10-14 days'}),
 ('T05', ['t05a', 't05b'], {}),
 ('E01', ['e01a', 'e01c'], {'cap': 'Which path did you get?'}),
]
CARDS = {
 'd0':  ([('FEVER', '36.8°C', .1, (230, 120, 40)), ('PULSE', '70', .35, (230, 60, 60)), ('BUBO', 'NONE', 0, (170, 90, 160)), ('ENERGY', '100%', 1, (90, 190, 90))], 'PEACH'),
 'd3':  ([('FEVER', '39.5°C', .75, (230, 120, 40)), ('PULSE', '110', .65, (230, 60, 60)), ('BUBO', 'NONE', 0, (170, 90, 160)), ('ENERGY', '20%', .2, (90, 190, 90))], 'VERY MUCH NOT GREAT'),
 'd6':  ([('FEVER', '40°C', .95, (230, 120, 40)), ('PULSE', '125', .85, (230, 60, 60)), ('BUBO', 'APPLE', .85, (170, 90, 160)), ('ENERGY', '5%', .05, (90, 190, 90))], '???'),
 'd8':  ([('FEVER', '38°C', .45, (230, 120, 40)), ('PULSE', '95', .5, (230, 60, 60)), ('BUBO', 'DRAINED', .3, (170, 90, 160)), ('ENERGY', '25%', .25, (90, 190, 90))], 'ALIVE?!'),
 'd30': ([('FEVER', '36.8°C', .1, (230, 120, 40)), ('PULSE', '72', .35, (230, 60, 60)), ('BUBO', 'GONE', 0, (170, 90, 160)), ('ENERGY', '80%', .8, (90, 190, 90))], 'NEVER AGAIN'),
}
CROP = {'s_plague_stall': [.67, .42, 1.5], 'h33a': [.64, .45, 1.45]}   # crop out the dome / the hero who is in bed that day
SECTION = {'H01', 'H06', 'H10', 'H14', 'H18', 'H29', 'H35', 'T01', 'E01'}
CARD_MIN = 3.6   # a status card stays long enough to read

shots, texts, vo, sfx, marks = [], [], [], [], {}
t = 0.3
for i, frames, tx in PLAN:
    if i in SECTION: t += .35
    d = dur(i); seg = d + (.15 if i[0] != 'E' else .4); t0 = t; marks[i] = t0
    vo.append({'file': f'{VO}/{i}.wav', 't': round(t0 + .03, 3)})
    n = len(frames)
    if 'card' in tx and n > 1:
        last = max(CARD_MIN, seg / n); rest = (seg - last) / (n - 1); lens = [rest] * (n - 1) + [last]
    else:
        lens = [seg / n] * n
    tt = t0; starts = {}
    for k, (f, ln) in enumerate(zip(frames, lens)):
        c = CROP.get(f, [.5, .5, 1.0]); sh = {'img': f, 'from': [c[0], c[1], c[2] + .025], 'to': c, 'settle': .3, 't0': round(tt, 3), 't1': round(tt + ln, 3)}
        shots.append(sh); starts[f] = (tt, tt + ln); tt += ln
    t1 = t0 + seg
    if 'cap' in tx: texts.append({'style': 'cap', 'text': tx['cap'], 't0': t0 + .15, 't1': t1 - .05, 'maxw': 1500, 'pop': True})
    if 'day' in tx: texts.append({'style': 'day', 'text': tx['day'], 't0': t0, 't1': t1 + (2.0 if i != 'T01' else 0), 'pop': True})
    if 'big' in tx:
        bt = t0 + d * .5; texts.append({'style': 'big', 'text': tx['big'], 't0': bt, 't1': min(bt + 1.8, t1), 'pop': True})
    if 'bigat' in tx:
        f, txt = tx['bigat']; a, b = starts[f]; texts.append({'style': 'big', 'text': txt, 't0': a + .1, 't1': b, 'pop': True})
    if 'title' in tx:
        big_end = max([x['t1'] for x in texts if x['style'] == 'big' and x['t0'] >= t0] or [0])
        texts.append({'style': 'cap', 'text': tx['title'], 'y': 540, 'size': 96, 'maxw': 1700, 't0': max(starts[frames[-1]][0] + .2, big_end + .15), 't1': t1 + 1.2, 'pop': True})
    for f, notes in tx.get('notes', {}).items():
        a, b = starts[f]
        for nn in notes: texts.append({'style': 'note', 't0': a + .25, 't1': b, **nn})
    if 'card' in tx:
        rows, mood = CARDS[tx['card']]; a, b = starts[frames[-1]]
        texts.append({'style': 'card', 'rows': [list(r[:3]) + [list(r[3])] for r in rows], 'mood': mood, 't0': a + .1, 't1': b, 'pop': True})
        sfx.append({'kind': 'shutter', 't': round(a + .1, 3), 'gain': .3})
    if tx.get('strike'):
        st0 = t0 + max(1.0, d * .55)
        texts.append({'style': 'strike', 'text': tx['cap'], 'maxw': 1500, 't0': st0, 't1': t1 - .05})
        sfx.append({'kind': 'page', 't': round(st0, 3), 'gain': .6})
    t = t1
    if i == 'C04': t += 1.2; shots[-1]['t1'] = round(t, 3)   # hold the title on the last cold-open frame
shots[0]['t0'] = 0.0
for a, b in zip(shots, shots[1:]): a['t1'] = b['t0']   # no holes: the previous frame covers section pauses
shots[-1]['t1'] = round(t + 1.2, 3); shots[-1]['fade_out'] = 1.0; TOTAL = round(t + 1.2, 3)
mt = lambda i: round(marks[i], 2)
G = .55   # music quieter than before
music = [
 {'file': 'channel/diseases/music/cholera_a.mp3', 't0': 0, 't1': mt('H18') + 1, 'gain': G, 'fade_in': 1.5, 'fade_out': 3},
 {'file': 'channel/diseases/music/cholera_b.mp3', 't0': mt('H18') - 1, 't1': mt('T01') + 1, 'gain': G, 'fade_in': 3, 'fade_out': 3},
 {'file': 'channel/diseases/music/cholera_a.mp3', 't0': mt('T01') - 1, 't1': 'ALL', 'gain': G, 'fade_in': 3, 'fade_out': 3},
]
spec = {'base': 'channel/diseases/whatif02_plague/frames_v2', 'fade_in': .3, 'music': music, 'shots': shots, 'texts': texts, 'vo': vo, 'sfx': sfx, 'duration': TOTAL}
json.dump(spec, open(os.path.join(HERE, 'timeline_v2.json'), 'w'), indent=1)
used = {s['img'] for s in shots}
print(f'{len(shots)} shots ({len(used)} unique), {TOTAL:.1f} s, avg {TOTAL / len(shots):.2f} s/shot')
for i in ['H01', 'H06', 'H10', 'H14', 'H18', 'H29', 'H35', 'T01']: print(i, f'{int(marks[i] // 60)}:{int(marks[i] % 60):02d}')
