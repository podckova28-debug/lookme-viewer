"""What If #3 (rabies, 1885): cholera look, ~3.3 s per frame, still frames with a quick settle after each cut.
python3 timeline.py -> timeline.json ; python3 ../tools/qc.py timeline.json qc_groups.json ; python3 ../tools/build_whatif.py timeline.json out.mp4
"""
import json, os, wave
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
VO = 'voices/whatif03_rabies/fast'   # sped up 1.08x
def dur(i):
    w = wave.open(os.path.join(REPO, VO, i + '.wav')); return w.getnframes() / w.getframerate()

N = lambda text, x, y, tx=None, ty=None, **k: dict(text=text, x=x, y=y, **({'tx': tx, 'ty': ty} if tx is not None else {}), **k)
# line, frames, texts. 'after' = (frame, seconds, card): a silent status-card shot after the line
PLAN = [
 ('C01', ['m_street', 'c01b', 'c01c'], {'cap': 'France, November 1885', 'notes': {'c01c': [N('Drooling', 380, 170, 860, 440), N('(not a good sign)', 380, 245, size=46)]}}),
 ('C02', ['c02a'], {}),
 ('C03', ['m_rabies'], {'notes': {'m_rabies': [N('Rabies', 330, 430, 780, 300), N('(yes, the disease itself)', 330, 500, size=46)]}}),
 ('C04', ['c02b', 'c04a', 'c04b'], {'big': '1 choice', 'title': 'What happens if you get rabies in 1885',
         'notes': {'c02b': [N('2 bites', 1480, 260, 950, 520)]}}),
 ('H01', ['h01b', 'h01c'], {'day': 'Day 0'}),
 ('H02', ['h02a', 'm_diag'], {'cap': 'A few centimetres a day'}),
 ('H03', ['h03a'], {'after': ('h03b', 3.8, 'd0')}),
 ('H04', ['h04a', 'h04b'], {'cap': 'Step 1: a red-hot key', 'notes': {'h04a': [N("St Hubert's key", 300, 800, 325, 480)]}}),
 ('H05', ['h05a'], {'cap': '(this one might actually help)'}),
 ('H06', ['h06a', 'h06b'], {'cap': 'Step 2: hair of the dog', 'strike': True, 'notes': {'h06b': [N('Actual dog hair', 430, 620, 1100, 800)]}}),
 ('H07', ['h07a'], {}),
 ('H08', ['h08a', 'h08b', 'h08c'], {'day': 'Weeks 1-6'}),
 ('H09', ['h09a'], {}),
 ('H10', ['h10a', 'h10b'], {'big': 'Too late'}),
 ('H11', ['h11a', 'h11b'], {}),
 ('H12', ['h12a', 'h12b'], {'cap': '14 bites. 10 days of shots.', 'notes': {'h12a': [N('Louis Pasteur', 420, 110, 760, 230), N('(a chemist, not a doctor)', 420, 180, size=46), N('Joseph Meister, 9', 1150, 120, 1165, 380)]}}),
 ('H13', ['h13a', 'h13b'], {'cap': 'Paris or home?'}),
 ('H14', ['h14a'], {}),
 ('H15', ['h15a', 'h15b'], {'day': 'Week 6', 'card': 'w6', 'notes': {'h15a': [N('It itches', 640, 880, 1225, 655)]}}),
 ('H16', ['h16a', 'h16b'], {'day': 'Symptoms: day 2'}),
 ('H17', ['h17a', 'h17b'], {'notes': {'h17a': [N('Water', 330, 300, 340, 425)]}}),
 ('H18', ['h18a'], {'day': 'Symptoms: day 3', 'cap': 'Hydrophobia: fear of water', 'after': ('h18b', 3.8, 's3')}),
 ('H19', ['h19a'], {}),
 ('H20', ['h20a'], {'notes': {'h20a': [N('The virus', 1660, 170, 1305, 395), N('(ready for a ride)', 1660, 240, size=46)]}}),
 ('H21', ['h21z', 'h21a'], {}),
 ('H22', ['h22a'], {'day': 'The other path: Paris'}),
 ('H23', ['h23a', 'h23b', 'h23c'], {'cap': 'Every day, for 10 days', 'notes': {'h23c': [N('Dried 14 days', 360, 120, 270, 310), N('Dried 1 day', 1560, 120, 1650, 310)]}}),
 ('H24', ['h24a', 'h24b'], {'notes': {'h24a': [N('Your immune system', 1450, 980, 1378, 600)]}}),
 ('H25', ['h25a'], {'cap': '350 treated. 1 died.'}),
 ('H26', ['h26a'], {}),
 ('H27', ['h27a', 'h27b'], {'cardat': ('h27a', 'saved'), 'notes': {'h27b': [N('Joseph Meister', 1080, 130, 700, 255), N('(all grown up)', 1080, 200, size=46)]}}),
 ('T01', ['t01a'], {'day': 'Today'}),
 ('T02', ['t02a', 't02b'], {'notes': {'t02a': [N('15 minutes', 1650, 540, 1420, 330)]}}),
 ('T03', ['t03a'], {'cap': 'Works almost every time'}),
 ('T04', ['t04a', 't04b'], {'cap': 'About 59,000 deaths a year'}),
 ('T05', ['t05a'], {}),
 ('E01', ['e01a'], {'cap': 'Would you get on that train?'}),
]
NOTES = json.load(open(os.path.join(HERE, 'notes_extra.json'))) if os.path.exists(os.path.join(HERE, 'notes_extra.json')) else {}
OR, RD, PU, BL, GR = (230, 120, 40), (230, 60, 60), (170, 90, 160), (90, 150, 220), (90, 190, 90)
CARDS = {
 'd0':    ([('BITE', '2 HOLES', .25, RD), ('FEVER', 'NONE', 0, OR), ('VIRUS', 'IN YOUR ARM', .1, PU)], 'ANNOYED'),
 'w6':    ([('BITE', 'TINGLING', .45, RD), ('FEVER', '38°C', .5, OR), ('VIRUS', 'IN YOUR BRAIN', 1, PU)], 'OFF'),
 's3':    ([('THIRST', 'HUGE', .95, BL), ('SWALLOWING', 'NO', .05, GR), ('FEAR', 'MAX', 1, RD), ('VIRUS', 'EVERYWHERE', 1, PU)], 'TERRIFIED'),
 'saved': ([('BITE', '2 SCARS', .1, RD), ('FEVER', 'NONE', 0, OR), ('VIRUS', 'GONE', 0, PU)], 'ALIVE. THANKS, CHEMIST'),
}
CROP = {'t04a': [.56, .45, 1.6]}   # static crop on the first and only use: hides two stray stickmen at the map edges
CROP_OK = {'t04a'}   # NO zoomed re-use of a frame: the user hates jump zooms (qc.py fails on them)
SECTION = {'H01', 'H04', 'H08', 'H11', 'H15', 'H22', 'T01', 'E01'}
CARD_MIN, CARD_X = 3.6, 60   # cards on the left: the hero is on the right in the room

shots, texts, vo, sfx, marks = [], [], [], [], {}
def shot(f, a, b):
    c = CROP.get(f, [.5, .5, 1.0])
    shots.append({'img': f, 'from': [c[0], c[1], c[2] + .025], 'to': c, 'settle': .3, 't0': round(a, 3), 't1': round(b, 3), **({'crop_ok': True} if f in CROP_OK else {})})
def card(name, a, b):
    rows, mood = CARDS[name]
    texts.append({'style': 'card', 'x': CARD_X, 'y': 190, 'rows': [list(r[:3]) + [list(r[3])] for r in rows], 'mood': mood, 't0': a + .1, 't1': b, 'pop': True})
    sfx.append({'kind': 'shutter', 't': round(a + .1, 3), 'gain': .3})
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
    for f, ln in zip(frames, lens):
        shot(f, tt, tt + ln); starts[f] = (tt, tt + ln); tt += ln
    t1 = t0 + seg
    if 'cap' in tx: texts.append({'style': 'cap', 'text': tx['cap'], 't0': t0 + .15, 't1': t1 - .05, 'maxw': 1500, 'pop': True})
    if 'big' in tx:
        bt = t0 + d * .5; texts.append({'style': 'big', 'text': tx['big'], 't0': bt, 't1': min(bt + 1.8, t1), 'pop': True})
    if 'title' in tx:
        big_end = max([x['t1'] for x in texts if x['style'] == 'big' and x['t0'] >= t0] or [0])
        texts.append({'style': 'cap', 'text': tx['title'], 'y': 540, 'size': 96, 'maxw': 1700, 't0': max(starts[frames[-1]][0] + .2, big_end + .15), 't1': t1 + 1.6, 'pop': True})
    for f, notes in {**tx.get('notes', {}), **NOTES.get(i, {})}.items():
        a, b = starts[f]
        for nn in notes: texts.append({'style': 'note', 't0': a + .25, 't1': b, **nn})
    if 'card' in tx: card(tx['card'], *starts[frames[-1]])
    if 'cardat' in tx: f, c = tx['cardat']; card(c, *starts[f])
    if tx.get('strike'):
        st0 = t0 + max(1.0, d * .55)
        texts.append({'style': 'strike', 'text': tx['cap'], 'maxw': 1500, 't0': st0, 't1': t1 - .05})
        sfx.append({'kind': 'page', 't': round(st0, 3), 'gain': .6})
    t = t1
    if 'after' in tx:
        f, s, c = tx['after']; shot(f, t, t + s); card(c, t, t + s); t += s
    if 'day' in tx: texts.append({'style': 'day', 'text': tx['day'], 't0': t0, 't1': t + (2.0 if i != 'T01' else 0), 'pop': True})
    if i == 'C04': t += 1.6; shots[-1]['t1'] = round(t, 3)   # hold the title on the last cold-open frame
shots[0]['t0'] = 0.0
for a, b in zip(shots, shots[1:]): a['t1'] = b['t0']   # no holes: the previous frame covers section pauses
shots[-1]['t1'] = round(t + 1.2, 3); shots[-1]['fade_out'] = 1.0; TOTAL = round(t + 1.2, 3)
mt = lambda i: round(marks[i], 2)
G = .55
music = [
 {'file': 'channel/diseases/music/cholera_a.mp3', 't0': 0, 't1': mt('H15') + 1, 'gain': G, 'fade_in': 1.5, 'fade_out': 3},
 {'file': 'channel/diseases/music/cholera_b.mp3', 't0': mt('H15') - 1, 't1': mt('T01') + 1, 'gain': G, 'fade_in': 3, 'fade_out': 3},
 {'file': 'channel/diseases/music/cholera_a.mp3', 't0': mt('T01') - 1, 't1': 'ALL', 'gain': G, 'fade_in': 3, 'fade_out': 3},
]
spec = {'base': 'channel/diseases/whatif03_rabies/frames', 'fade_in': .3, 'music': music, 'shots': shots, 'texts': texts, 'vo': vo, 'sfx': sfx, 'duration': TOTAL}
json.dump(spec, open(os.path.join(HERE, 'timeline.json'), 'w'), indent=1)
print(f'{len(shots)} shots ({len({s["img"] for s in shots})} unique), {TOTAL:.1f} s, avg {TOTAL / len(shots):.2f} s/shot')
for i in sorted(SECTION, key=lambda k: marks[k]): print(i, f'{int(marks[i] // 60)}:{int(marks[i] % 60):02d}')
