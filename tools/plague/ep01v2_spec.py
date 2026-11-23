"""Plague ep01, v2 (retention rework): new cold open with open loops, cut digressions, 13 new explainer diagrams, fast pacing.
Reuses the v1 frames and voice-over (tools/plague/ep01_beats.json, assets/plague/ep01/vo_full), sped up 1.1x into vo_fast/.

  python3 tools/plague/ep01v2_spec.py frames  -> tools/plague/ep01v2_frames_todo.json (new diagrams only)
  python3 tools/plague/ep01v2_spec.py beats   -> tools/plague/ep01v2_beats.json
"""
import sys, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
V1 = json.load(open(os.path.join(ROOT, 'tools/plague/ep01_beats.json')))
COLD = json.load(open(os.path.join(ROOT, 'tools/plague/cold_open_beats.json')))
SHOTS = {}
for b in V1['beats']:
    if 'vo' in b: SHOTS[os.path.basename(b['vo'])[:-4]] = b['shots']
def v1(i): return [dict(s) for s in SHOTS[i]]
def img(i, idx): return dict(SHOTS[i][idx])

STYLE = ("2D animated history explainer frame, 16:9, no text. Hand-drawn ink illustration, clean black outlines, fine cross-hatching, "
         "muted grey-sepia palette with warm candle light accents. Not gory.")
DIAG = ("Draw ONLY the diagram described below, filling the whole frame, as ONE single picture: no extra rows, no extra panels, no comic strips above or below it. "
        "A hand-drawn explainer diagram in ink and muted watercolour on aged parchment, clean and readable like an old textbook plate, "
        "numbered stages as small circled digits with drawn arrows. No words, no letters, no numbers on axes, only circled digits. Not gory. ")
SN = ("Any human figure is a simple STICKMAN: plain white round head, two dot eyes, no nose, thin black stick arms and legs, small black mitten hands; "
      "each has exactly two arms and two hands. ")
NOPEOPLE = ' No people and no human figures anywhere in the picture.'
STILL = [[.5, .5, 1.0], [.5, .5, 1.02]]
def cap(t, **k): return {'text': t, 'x': 960, 'y': 985, 'size': 50, 'at': .3, **k}
NEW = {}
def dg(name, p, people=False, text=None):
    NEW[name] = STYLE + ' ' + (SN if people else '') + DIAG + p + ('' if people else NOPEOPLE)
    s = {'img': name, 'from': STILL[0], 'to': STILL[1], 'w': 1}
    if text: s['text'] = [cap(text)]
    return s

D01 = dg('d01', "A scale comparison: one single human hair drawn as a thick vertical column on the left (1), a grain of dust drawn smaller (2), and a tiny rod-shaped bacterium drawn as a minute dark capsule (3) under a big magnifying glass.", text='About 1/50 the width of a hair')
D02 = dg('d02', "Four numbered steps in one row: (1) a cartoon flea drinking from a black rat, (2) a cut-away view of the flea's gut packed with a dark clump of tiny rods blocking it, (3) the hungry flea with a grumbling stomach jumping, (4) the flea biting a bare stick arm again and again with small motion lines.", people=True, text="A blocked flea bites everything")
D03 = dg('d03', "A simple standing stickman outline front view with three numbered magnifier circles: (1) a swollen lump in the armpit, (2) a drop of blood with tiny dark rods in it, (3) a pair of lungs with a small cough cloud.", people=True, text='Lumps, blood, lungs')
D04 = dg('d04', "ONLY two rows of ten identical plain stickman icons, one row above the other: in the top row (1) five icons are faded grey and five are normal; in the bottom row (2) nine icons are faded grey and one is normal. Nothing else on the page.", people=True, text='Bubonic: about half. Pneumonic: almost all')
D05 = dg('d05', "Three numbered steps in one row: (1) an ancient human jaw bone with one tooth highlighted, (2) a tiny drill taking a sample from inside the tooth, (3) a twisted DNA strand with a tiny rod-shaped bacterium beside it.", text='His DNA, hidden in ancient teeth')
D06 = dg('d06', "ONLY one long horizontal timeline drawn as a thin ink line across the whole page, with three numbered wave-shaped humps rising from it far apart: (1) a medium hump on the left with a tiny domed church icon above it, (2) a huge tall hump in the middle with a tiny sailing ship icon above it, (3) a medium hump on the right with a tiny steamship icon above it. No numbers, no years.", text='Three pandemics')
D07 = dg('d07', "A simple old map of the Black Sea and the Mediterranean: a walled port on the Crimean coast (1), dotted arrows with small sailing galley icons going through the narrow strait past a domed city (2) and on across the sea to the island of Sicily (3).", text='Caffa to Messina, 1347')
D08 = dg('d08', "ONLY a single row of ten identical plain stickman icons standing side by side across the page: the first three are faded solid grey, the next three are drawn with dotted grey outlines, the last four are drawn normally in black ink. Nothing else on the page.", people=True, text='Between 3 and 6 in every 10 Europeans')
D09 = dg('d09', "Four numbered panels in one row: (1) three planets lined up in the sky, crossed out with a red X, (2) a cloud of wavy green bad-smell fumes, crossed out with a red X, (3) a knotted whip, crossed out with a red X, (4) a black rat with a flea on it, marked with a green tick.", text='They blamed everything but the rats')
D11 = dg('d11', "A sailing ship anchored alone out in a harbour bay (1), and beside it a simple wall calendar page with many small boxes all crossed off one by one (2), with an arrow from the calendar to a gangplank finally lowered onto the quay (3).", text='Wait 40 days before coming ashore')
D12 = dg('d12', "Two numbered panels in one row: (1) before: many small stickman workers in a field and one tiny coin above each of them, (2) after: only a few stickman workers in the same field and a big stack of coins above each of them.", people=True, text='Fewer workers, higher wages')
D15 = dg('d15', "Three numbered steps in one row: (1) a small glass medicine bottle of pills, (2) tiny rod-shaped bacteria cracking and breaking apart, (3) a simple shield with a green tick.", text='Cured with antibiotics')
D16 = dg('d16', "ONLY a simple world map filling the whole page with a few small red dots: on the island of Madagascar, in central Africa, and in the south-western United States. Nothing else.", text='Still here: Madagascar, Congo, the American West')

B = []
def N(i, shots, role='NARRATOR', vo=None): B.append({'id': i, 'role': role, 'vo': vo, 'shots': shots})
def HOLD(sec, shots): B.append({'hold': sec, 'shots': shots})
def S(name, cam=None, text=None):
    c = cam or [[.5, .5, 1.0], [.5, .5, 1.04]]
    s = {'img': name, 'from': c[0], 'to': c[1], 'w': 1}
    if text: s['text'] = [cap(text)] if isinstance(text, str) else text
    return s
CL = [[.5, .5, 1.06], [.5, .5, 1.1]]

# ---- new cold open: person in trouble first, then open loops (pope, Eyam, Newton), then "he's still here"
N('C01', [S('co_02', CL, 'Messina, Sicily · October 1347'), S('co_01'), S('co_03', CL), S('co_12')], vo='assets/plague/ep01/vo_v2/C01.wav')
N('C02', [S('co_06'), S('co_09')], role='PLAGUE', vo='assets/plague/ep01/vo_fast/p1_m.wav')
N('C03', [S('co_07', CL, 'Up to half of Europe'), S('f27g', None, 'A pope between two fires'), S('f46c', None, 'A village that locked itself in'), S('f46b', None, 'Isaac Newton')], vo='assets/plague/ep01/vo_v2/C03.wav')
N('C04', [D06, S('co_10')], vo='assets/plague/ep01/vo_v2/C04.wav')
N('C05', [S('co_08', CL)], role='PLAGUE', vo='assets/plague/ep01/vo_v2/C05.wav')
title = [b for b in COLD['beats'] if 'hold' in b][-1]
HOLD(3.6, [dict(title['shots'][0])])

# ---- who is he
N('L06a', [img('L06a', 0), img('L06a', 1), D01, img('L06a', 2)])
N('L06b', v1('L06b'), role='PLAGUE')
N('L07', [img('L07', 0), img('L07', 1), D02, img('L07', 3)])
N('L08a', v1('L08a')); N('L08b', v1('L08b'), role='PLAGUE')
N('L09', v1('L09') + [D03])
N('L10', [img('L10', 0), D04, img('L10', 1)])
# ---- origin
N('L11', v1('L11'))
N('L12a', [img('L12a', 0), D05, img('L12a', 1)])
N('L12b', v1('L12b'), role='PLAGUE')
# ---- Justinian
N('L14', v1('L14') + [D06])
N('L15', v1('L15')); N('L17', v1('L17')); N('L18', v1('L18')); N('L19', v1('L19')); N('L20', v1('L20'), role='PLAGUE')
# ---- Black Death
N('L21', v1('L21')); N('L22', v1('L22'))
N('L23', [img('L23', 0), img('L23', 1), D07, img('L23', 2)])
N('L24', v1('L24')); N('L25', v1('L25')[:2]); N('L26', v1('L26'), role='PLAGUE'); N('L27', v1('L27'))
N('L28', [img('L28', 0), D08, img('L28', 1), img('L28', 2)])
HOLD(2.0, [dict([b for b in V1['beats'] if 'hold' in b and b['shots'][0]['img'] == 'f28d'][0]['shots'][0])])
# ---- how people fought back (pope payoff right after "bad air")
N('L30', v1('L30')); N('L31', v1('L31'), role='PLAGUE'); N('L32', v1('L32'))
N('L27b', v1('L27b')); N('L27bP', v1('L27bP'), role='PLAGUE')
N('L33', v1('L33') + [D09])
N('L34', v1('L34')); N('L35', v1('L35'))
N('L36', [img('L36', 0), D11, img('L36', 1)]); N('L36P', v1('L36P'), role='PLAGUE')
N('L37', v1('L37')); N('L38', v1('L38'), role='PLAGUE')
# ---- after
N('L39', [img('L39', 0), D12, img('L39', 1), img('L39', 2)])
N('L41', v1('L41')); N('L42a', v1('L42a'), role='PLAGUE'); N('L42b', v1('L42b'))
# ---- London 1665: Newton and Eyam payoffs
N('L43', v1('L43')); N('L44', v1('L44')); N('L45', v1('L45')); N('L46', v1('L46'))
N('L46a', v1('L46a')); N('L46b', v1('L46b')); N('L47', v1('L47')); N('L48', v1('L48'), role='PLAGUE')
# ---- third pandemic
N('L49', v1('L49')); N('L50', v1('L50')); N('L51', v1('L51'), role='PLAGUE')
N('L51a', v1('L51a')); N('L51aP', v1('L51aP'), role='PLAGUE'); N('L52', v1('L52'))
N('L53', [img('L53', 0), D15, img('L53', 1)])
# ---- today
N('L54', [D16] + v1('L54')); N('L55', v1('L55'), role='PLAGUE'); N('L56', v1('L56'))
N('L57', v1('L57')); N('L58', v1('L58'))
HOLD(5.0, [dict([b for b in V1['beats'] if 'hold' in b][-1]['shots'][0])])

MUSIC = [(0, 178, 'plague_a.mp3'), (174, 352, 'plague_b.mp3'), (348, 'ALL', 'plague_a.mp3')]

def frames():
    out = [{'img': k, 'prompt': v, 'refs': []} for k, v in NEW.items()]
    json.dump(out, open(os.path.join(ROOT, 'tools/plague/ep01v2_frames_todo.json'), 'w'), indent=1); print(len(out), 'frames')

def beats():
    out = {'base': 'assets/plague/ep01/frames', 'keep_zoom': ['f26a'], 'static': True, 'fade_in': .8, 'start': 0.0, 'lead': .35, 'gap': .35, 'max_shot': 2.6,
           'sfx_global': COLD['sfx_global'], 'beats': []}
    M = 'assets/plague/music/'
    out['music'] = [{'file': M + f, 't0': float(a0), 't1': a1, 'gain': 1.0, 'fade_in': 2.0 if a0 == 0 else 4.0, 'fade_out': 5.0 if a1 == 'ALL' else 4.0}
                    for a0, a1, f in MUSIC]
    for b in B:
        if 'hold' in b: out['beats'].append({'hold': b['hold'], 'shots': b['shots']}); continue
        vo = b['vo'] or f"assets/plague/ep01/vo_fast/{b['id']}.wav"
        out['beats'].append({'vo': vo, **({'gain': 1.05} if b['role'] == 'PLAGUE' else {}), 'shots': b['shots']})
    json.dump(out, open(os.path.join(ROOT, 'tools/plague/ep01v2_beats.json'), 'w'), indent=1); print(len(out['beats']), 'beats')

{'frames': frames, 'beats': beats}[sys.argv[1]]()
