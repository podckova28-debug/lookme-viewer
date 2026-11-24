"""What If #1: What Happens If You Catch Cholera? (pilot of the second-person 'what happens if you...' format).
The hero is YOU: the same stickman in every frame. Timeline by hours, 1854 London, then the same cup of water today.

  python3 tools/plague/whatif01_spec.py lines   -> voice list (id|ROLE|text), roles NARRATOR / CHOLERA
  python3 tools/plague/whatif01_spec.py frames  -> tools/plague/whatif01_frames_todo.json
  python3 tools/plague/whatif01_spec.py beats   -> tools/plague/whatif01_beats.json
"""
import sys, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
K_SHEET = '578aebc8-20b7-4c82-930c-c1cc9e4e1b59'   # channel/plague/sheets/cholera_turn.jpg (King Cholera)
STYLE = ("2D animated history explainer frame, 16:9, no text. Hand-drawn ink illustration, clean black outlines, fine cross-hatching, "
         "muted grey-teal-sepia palette with a sickly green accent; warm light only from the sun, gas lamps and candles. Not gory, cartoon-simple.")
MODERN = ("2D animated history explainer frame, 16:9, no text. Hand-drawn ink illustration, clean black outlines, the same muted palette, soft natural daylight. "
          "The setting is modern (2020s): nothing old-fashioned. Not gory.")
SN = ("Humans are simple STICKMEN: plain white round head, two dot eyes, simple expressive mouth and eyebrows, no nose, no beard, thin black stick arms and stick legs, "
      "small solid BLACK mitten hands with no fingers; never white hands, never skin-coloured or thick human arms. "
      "Only the figures described, standing apart, never overlapping; each has exactly two arms and two hands; hands are empty unless an object is described; "
      "every arm is one smooth line from the shoulder to the hand, never bending back on itself, never doubled; no bare skin-coloured limbs anywhere; "
      "no flags, no banners; no readable text.")
YOU = ("YOU, the hero: a stickman with a plain white round head, a flat grey cloth cap, a brown waistcoat over a plain white shirt with LONG sleeves that reach all the way down to the wrists (sleeves NOT rolled up, no bare forearms, no cuffs at the elbows), a small solid black mitten hand at the end of each sleeve, and dark grey trousers")
YOU_MOD = ("YOU, the hero, in the present day: a stickman with a plain white round head, a grey baseball cap, a white T-shirt and blue jeans")
KING = ("King Cholera exactly as on the attached sheet: a stout pot-bellied Victorian gentleman in a soaking-wet dark teal frock coat, brown waistcoat and cravat, a battered black "
        "top hat with a tarnished tin crown around it, clammy grey-blue skin, glowing pale-green eyes, a wide toothy grin; water drips from him constantly; a dented tin cup on a chain. "
        "Exactly ONE King Cholera, with exactly two arms and two hands; he holds AT MOST ONE object, his other hand empty and attached to its own arm.")
DIAG = ("Draw ONLY the diagram described below, filling the whole frame, as ONE single picture: no extra panels. "
        "A hand-drawn explainer diagram in ink and muted watercolour on aged paper, clean like an old textbook plate, "
        "numbered stages as small circled digits with drawn arrows. No words, no letters, no numbers except circled digits. Not gory, cartoon-simple. ")
STICKD = "Any human figure is a plain stickman outline with a round head, dot eyes and black stick limbs. "
NOPEOPLE = ' No people and no human figures anywhere in the picture.'
def W(): return [[.5, .5, 1.0], [.5, .5, 1.04]]
def C(x, y, z=1.3): z = 1 + (z - 1) * .35; return [[x, y, z], [x, y, z + .02]]
def O(): return [[.5, .5, 1.05], [.5, .5, 1.0]]
STILL = [[.5, .5, 1.0], [.5, .5, 1.02]]

def sh(img, cam=None, prompt=None, refs='', text=None, w=1):
    s = {'img': img, 'cam': cam or W(), 'w': w}
    if prompt: s['prompt'] = prompt; s['refs'] = refs
    if text: s['text'] = text if isinstance(text, list) else [text]
    return s
def cap(t, **k): return {'text': t, 'x': 960, 'y': 985, 'size': 50, 'at': .3, **k}
def clock(t): return {'text': t, 'x': 1640, 'y': 110, 'size': 72, 'style': 'title', 'pop': True, 'at': .1}
def ch(img, cam, p, modern=False, **k): return sh(img, cam, (MODERN if modern else STYLE) + ' ' + SN + ' ' + p, **k)
def kg(img, cam, p, people='', **k): return sh(img, cam, STYLE + ' ' + KING + ' ' + (SN + ' ' + people if people else 'No other people.') + ' ' + p, 'K', **k)
def dg(img, p, people=False, **k): return sh(img, STILL, STYLE + ' ' + (STICKD if people else '') + DIAG + p + ('' if people else NOPEOPLE), **k)
def ob(img, p, cam=None, **k): return sh(img, cam or C(.5, .5, 1.05), STYLE + ' ' + p + NOPEOPLE, **k)

B = []
def N(i, t, *s): B.append((i, 'NARRATOR', t, list(s)))
def K(i, t, *s): B.append((i, 'CHOLERA', t, list(s)))
def HOLD(sec, *s): B.append((None, None, sec, list(s)))
SOHO = "a narrow cobbled Soho street in London in August 1854, soot-black brick houses, a cast-iron hand water pump with a long handle"
ROOM = "a small dim 1854 London attic room with a sloping ceiling, a narrow iron bed with a thin grey blanket, a tin bucket and a single candle"

# ---- cold open
N('C01', "London, August 1854. It's a hot morning in Soho. You're thirsty, so you walk to the pump on Broad Street, like everyone else, and fill your cup. The water is cold, and a little cloudy. You drink the whole thing.",
  ch('a01', C(.5, .5, 1.05), f"Bright hot morning on {SOHO}: {YOU} works the pump handle with one black mitten hand while holding a dented tin cup under the spout with the other, smiling, sweat on his head from the heat.", text=[cap('London, August 1854'), clock('8:00 AM')]),
  ch('a02', C(.5, .45, 1.2), f"Close-up: {YOU} drinks from a dented tin cup held in one black mitten hand, eyes closed, happy; the water in the cup is slightly cloudy with tiny faint green specks.", text=cap('A little cloudy')))
K('C02', "Cheers.",
  kg('a03', C(.5, .45, 1.1), f"On {SOHO}: far in the background, small, {YOU} walks away down the street with his back to the viewer; he appears ONLY ONCE in the picture. In the foreground, King Cholera leans on the water pump, raising his own dented tin cup in a toast to the viewer with one hand and grinning, his other hand on the pump.", people=f"One stickman: {YOU}."))
N('C03', "By tomorrow night, you could be dead. This is what happens if you catch cholera.",
  ch('a04', O(), f"{ROOM} at night, cold green light: {YOU} lies in the narrow bed, grey-blue and exhausted, eyes sunken, one black mitten hand hanging over the edge of the bed.", text=cap('Tomorrow night')))
HOLD(3.6, kg('a05', O(), "Title shot: King Cholera stands on the left third of the frame beside a dripping Victorian water pump in a dark foggy street, holding up a big brass pocket watch toward the viewer in one hand, his other hand on his belly; the right side of the frame is empty dark foggy sky.")
     | {'text': [{'text': 'WHAT HAPPENS IF', 'x': 1300, 'y': 300, 'size': 84, 'style': 'title', 'pop': True, 'at': .15, 'len': 3.3},
                 {'text': 'YOU CATCH CHOLERA', 'x': 1300, 'y': 420, 'size': 96, 'style': 'title', 'color': [150, 220, 170], 'at': .4, 'len': 3.1}]})

# ---- hour 0
N('H01', "What you just swallowed is a bacterium: Vibrio cholerae. A tiny comma with a whip for a tail. Your stomach acid kills most of them. But you drank a whole cup, and some make it through.",
  dg('d01', "A simple cut-away of a stickman body from the side: (1) a cup pouring tiny green comma-shaped bacteria into the mouth, (2) the stomach drawn as a pool of acid where most bacteria dissolve, (3) a few surviving comma-shaped bacteria with tiny whip tails swimming on into the small intestine.", people=True, text=[cap('Vibrio cholerae'), clock('HOUR 0')]),
  ob('a06', "Microscope view: a round bright circular field full of tiny curved comma-shaped bacteria, each with a single thin whip-like tail, swimming; one of them in the centre wears a tiny battered top hat with a tin crown.", text=cap('A comma with a whip')))
N('H02', "They swim down to your small intestine, dig into its lining, and settle in. You feel completely fine. You go back to work.",
  ch('a07', W(), f"A busy 1854 London workshop with wooden benches and small high windows showing only grey sky and chimneys (no towers, no clock tower): {YOU} hammers a horseshoe on an anvil with a hammer in one black mitten hand, cheerful, a second stickman worker in an apron stands apart at another bench.", text=[cap('You feel fine'), clock('HOUR 2')]))
K('H03', "Don't mind me. I'm just moving in.",
  kg('a08', C(.5, .45, 1.1), "Inside a cartoon cut-away of a pink cave-like gut wall with soft folds: King Cholera unpacks a small battered suitcase onto the soft floor with one hand, hanging a tiny framed picture of a water pump on the wall with the other, grinning at the viewer."))

# ---- hour 20
N('H04', "Sometimes it takes days. For you, it takes about one. Overnight, the bacteria multiply into billions, and release a toxin.",
  dg('d02', "Three numbered panels in one row: (1) a few comma-shaped bacteria on a gut wall, (2) many more, (3) the gut wall completely covered in thousands of them, each releasing tiny green droplets of toxin. A small moon icon above the row.", text=[cap('Billions, overnight'), clock('HOUR 20')]))
N('H05', "The toxin flips a switch in the cells of your gut. Instead of absorbing water, they start pumping it out, along with salt, straight into your intestine.",
  dg('d03', "Two numbered panels in one row: (1) a healthy gut cell drawn as a simple box with blue water arrows going IN from the gut into the body, (2) the same cell with a green toxin droplet attached, and the blue water arrows and small white salt grains now pouring OUT into the gut.", text=[cap('The pump runs backwards')]))

# ---- hour 24
N('H06', "In the morning, it hits you all at once. Sudden, violent diarrhoea. Pale and watery, with little white flecks. Doctors call it rice-water stool. You can lose a litre of fluid an hour.",
  ch('a09', C(.5, .5, 1.05), f"Early morning in {ROOM}: {YOU} sits bolt upright in bed clutching his stomach with both black mitten hands, eyes wide in shock, sweat drops flying; a dawn light through the tiny window.", text=[cap('It hits all at once'), clock('HOUR 24')]),
  dg('d04', "A simple stickman body outline with a big water-drop meter beside it like a thermometer, its blue level dropping fast with a downward arrow; a small hourglass icon beside it.", people=True, text=[cap('Up to a litre an hour')]))
N('H07', "Then the vomiting starts. You can't keep a single sip of water down.",
  ch('a10', W(), f"{ROOM}: {YOU} leans weakly over a tin bucket beside the bed, one black mitten hand on the bed frame, while a stickman woman in a long 1850s dress and headscarf, his landlady, stands apart in the doorway holding a cup of water, worried.", text=cap("You can't keep water down")))
K('H08', "Most diseases take weeks. I'm on a schedule.",
  kg('a11', C(.5, .45, 1.1), "King Cholera stands at the foot of a narrow iron bed in a dim attic, checking a big brass pocket watch held in one hand and tapping his foot impatiently, his other hand on his belly, grinning.", people=f"One stickman: {YOU} lying in the bed under a grey blanket, eyes closed."))

# ---- hour 28
N('H09', "By the afternoon, you've lost so much water and salt that your muscles seize up. Painful cramps in your legs, your stomach, your hands.",
  dg('d05', "A simple standing stickman outline with three numbered magnifier circles: (1) a calf with jagged cramp lines, (2) a stomach with a knot, (3) a black mitten hand curled tight; small salt grains and water drops falling away from the figure.", people=True, text=[cap('Cramps'), clock('HOUR 28')]),
  ch('a12', C(.5, .5, 1.05), f"{ROOM} in afternoon light: {YOU} curls up on the bed gripping his leg with both black mitten hands, face twisted in pain.", text=cap('Cramps everywhere')))
N('H10', "Your eyes sink into your skull. The skin on your fingers wrinkles, like you've been in the bath for hours. Your voice becomes a hoarse whisper.",
  dg('d06', "Three numbered panels in one row: (1) a simple stickman face with deep dark sunken eye sockets, (2) a cartoon mitten hand with wrinkled lines like after a long bath, (3) a tiny speech bubble with a faint dotted whisper squiggle.", people=True, text=[cap('Sunken eyes, wrinkled hands')]))
N('H11', "Your blood gets thick and dark, and your skin turns grey and blue. Victorian Londoners had a name for it: the blue death.",
  ch('a13', C(.5, .45, 1.15), f"Close-up in {ROOM}: {YOU} lies on the pillow, his round head now tinted grey-blue, eyes sunken, lips pale, staring at the ceiling; cold green-grey light.", text=[cap('The blue death'), clock('HOUR 30')]))

# ---- the 1854 doctor
N('H12', "Your landlady sends for a doctor. It's 1854, so here's your treatment.",
  ch('a14', W(), f"{ROOM}: a stickman doctor in a black 1850s frock coat and a tall black top hat walks in carrying a black leather bag in one black mitten hand, while {YOU} lies grey-blue in the bed.", text=cap('The doctor arrives')))
N('H13', "He might bleed you, to remove the bad blood. Give you calomel, which is mercury, to clear out your bowels. Opium for the cramps, and brandy for strength.",
  dg('d07', "Four numbered icons in one row on a doctor's tray: (1) a small lancet and a bowl, (2) a small bottle with a mercury drop symbol, (3) a small brown opium bottle with a poppy, (4) a small brandy glass.", text=[cap('Bleeding, mercury, opium, brandy')]),
  ch('a15', C(.5, .5, 1.05), f"{ROOM}: the stickman doctor in a black frock coat holds a small white bowl in one black mitten hand beside the arm of {YOU}, who is too weak to protest; a candle on a stool. Not gory, nothing shown on the arm.", text=cap('Bleeding the patient')))
N('H14', "Every single one of these makes it worse. You're dying because you're losing fluid, and the doctor is taking even more.",
  dg('d08', "A simple water-drop meter like a thermometer, almost empty, with two red arrows pulling the last drops out of it: (1) a lancet icon, (2) a mercury bottle icon.", text=[cap('Making it worse')]))
K('H15', "Bleeding a man who's drying out. Honestly, your doctors were my best assistants.",
  kg('a16', C(.5, .45, 1.1), "King Cholera stands proudly beside an 1850s doctor's black leather bag on a table, patting the bag with one hand like a good friend, his other hand on his belly, grinning at the viewer, in a dim attic."))

# ---- hour 36
N('H16', "Your kidneys shut down. Your heart struggles with too little blood. The pulse at your wrist almost vanishes.",
  dg('d09', "A simple stickman body outline with three numbered magnifier circles: (1) two kidneys greyed out, (2) a heart with a weak dotted beat line, (3) a wrist with a nearly flat pulse line.", people=True, text=[cap('Kidneys, heart, pulse'), clock('HOUR 36')]))
N('H17', "Untreated, around half of people with severe cholera die. Some within hours of the first symptoms.",
  dg('d10', "ONLY a single row of ten IDENTICAL plain stickman icons standing side by side across the page, no hats, no clothes: five drawn faded pale grey, five drawn normally in black ink. Nothing else on the page.", people=True, text=[cap('Severe and untreated: about half die')]))
N('H18', "And all this time, you're pouring out billions of fresh bacteria. If any of it reaches the water supply, the next person drinks you.",
  dg('d11', "A simple circular cycle with arrows: (1) a sick stickman in bed, (2) a bucket emptied into a brick cesspit, (3) dirty water seeping underground into a well, (4) a water pump, (5) a healthy stickman drinking from a cup, then back to (1).", people=True, text=[cap('The next person drinks you')]))
N('H19', "That's exactly what happened at Broad Street. A baby's nappies were washed into a cesspit right beside the pump. In ten days, more than five hundred people in the neighbourhood died.",
  ch('a17', W(), f"Dusk on {SOHO}: a stickman woman in a long 1850s dress and headscarf pours a bucket of water into an open brick cesspit grate beside a house, unaware; just a few steps away stands the water pump.", text=cap('A cesspit beside the pump')),
  dg('d12', "A simple old street map of a few Soho blocks with one water pump icon in the middle and many small black bars stacked outside the houses closest to it, fewer bars further away.", text=[cap('500 dead in 10 days')]))

# ---- survival and John Snow
N('H20', "But let's say you're lucky, and you survive. You'll be weak for weeks. And the next people in your street might owe their lives to a doctor named John Snow.",
  ch('a18', C(.5, .5, 1.05), f"{ROOM} in pale morning light: {YOU}, thin and tired but alive, sits up in bed sipping broth from a bowl held in both black mitten hands, the landlady in a headscarf stands apart smiling.", text=[cap('You survive'), clock('DAY 3')]))
N('H21', "Snow mapped every death and saw them clustered around the pump. On the eighth of September, he persuaded the council to take off its handle.",
  ch('a19', W(), f"Daylight on {SOHO}: a stickman doctor with short dark side whiskers drawn as simple lines, a dark 1850s frock coat and no hat, holds the long iron pump handle he has just removed in both black mitten hands, while a stickman parish official in a top hat stands apart, watching.", text=cap('John Snow, 8 September 1854')))
N('H22', "The workers at the brewery on Broad Street drank beer, not water. Not one of them died.",
  ch('a20', C(.5, .5, 1.05), f"Inside an 1854 London brewery with big wooden vats and small high windows showing only grey sky (no towers, no clock tower): two stickman brewery workers in leather aprons and caps stand apart, each raising a tankard of beer in one black mitten hand, cheerful and healthy.", text=cap('The brewery workers drank beer')))
K('H23', "They took away my handle. Rude.",
  kg('a21', C(.5, .45, 1.1), "King Cholera stands beside a water pump with no handle in a foggy Soho street, staring at the empty slot where the handle used to be, his arms crossed, sulking."))

# ---- today
N('T01', "Now. Same cup of water, but today.",
  ch('a22', W(), f"A modern small town street after a flood, with a water tank and puddles: {YOU_MOD} drinks from a plastic cup held in one black mitten hand, sunny daylight.", modern=True, text=[cap('Same cup, today'), clock('2026')]))
N('T02', "The cure turned out to be ridiculously simple: put back what you lose. Clean water, a little salt and a little sugar, by mouth, or through a drip if you can't drink.",
  dg('d13', "Three numbered steps in one row: (1) a glass of clean water, (2) a small spoon of salt and a small spoon of sugar pouring in, (3) the glass with a green tick and a happy simple stickman head beside it.", people=True, text=[cap('Water, salt, sugar')]),
  ch('a23', C(.5, .5, 1.05), f"A bright modern clinic tent: {YOU_MOD} sits on a cot drinking from a plastic cup held in BOTH his black mitten hands, an IV drip bag hanging on a metal stand beside the cot (its tube simply coiled on the stand, not attached to him), while a stickman nurse in blue scrubs stands apart, checking a clipboard.", modern=True, text=cap('Oral rehydration')))
N('T03', "With it, fewer than one in a hundred cholera patients die. The Lancet called it potentially the most important medical advance of the twentieth century.",
  dg('d14', "ONLY two rows of ten identical plain stickman icons, one above the other: top row (1) five faded grey and five normal; bottom row (2) all ten normal in black ink with one tiny faded corner on the last one.", people=True, text=[cap('From 1 in 2 to under 1 in 100')]))
N('T04', "Add antibiotics, and you're back on your feet in a few days.",
  ch('a24', W(), f"A sunny modern street: {YOU_MOD} walks out of a small clinic smiling, waving goodbye with one black mitten hand to a stickman nurse in blue scrubs in the doorway.", modern=True, text=[cap('Back on your feet'), clock('DAY 3')]))
N('T05', "But cholera hasn't gone. Every year, millions still catch it, wherever the water is dirty: after wars, floods and earthquakes. Tens of thousands still die, for lack of clean water, salt and sugar.",
  dg('d15', "ONLY a simple world map filling the whole page with small green dots clustered in parts of Africa, South Asia, the Middle East and Haiti. Nothing else.", text=[cap('Still millions of cases a year')]),
  ch('a25', W(), "A modern refugee camp with white tents after a flood: a stickman aid worker in a blue vest holds a sealed jerrycan of clean water out with both his black mitten hands toward a stickman woman in a bright headscarf, who reaches for its handle with one black mitten hand, her other arm at her side; they stand a step apart. The aid worker has exactly two arms, the woman exactly two arms.", modern=True, text=cap('Clean water saves lives')))
K('T06', "I don't need a pump anymore. Just one broken pipe.",
  kg('a26', C(.5, .45, 1.1), "King Cholera crouches beside a cracked modern water pipe leaking into a muddy puddle at dusk, dipping his tin cup into the puddle with one hand and grinning at the viewer, his other hand on his knee."))

# ---- ending
N('E01', "So, if you ever find yourself in Soho in 1854, and someone offers you a nice cold cup from the Broad Street pump: say no thanks. Have a beer.",
  ch('a27', C(.5, .5, 1.05), f"Bright morning on {SOHO}: {YOU} stands next to the pump, holding up one black mitten hand to politely refuse a cup, and holding a tankard of beer in the other, grinning.", text=cap('No thanks')))
N('E02', "Next time: what happens if you're bitten by a rabid dog?",
  ch('a28', C(.5, .5, 1.04), "A dark 1880s French village lane at night, ominous: on the left third of the frame a single stickman boy in a long smock and dark trousers (thin black stick legs, no bare skin) looks down in fear at a small red mark on his trouser leg, while far behind him a shadowy dog with glowing eyes slinks away; the right side of the frame is dark empty misty sky."))
HOLD(5.0, sh('a28', O(), text=[{'text': 'NEXT TIME', 'x': 1380, 'y': 360, 'size': 110, 'style': 'title', 'pop': True, 'at': .2, 'len': 4.6},
                              {'text': 'SUBSCRIBE', 'x': 1380, 'y': 500, 'size': 64, 'at': .8, 'len': 4.0}]))

# ---- extra cut-ins
EXTRA = {
  'H04': ch('a29', W(), f"A cosy 1854 London pub in the evening lit by gas lamps: {YOU} sits at a wooden table eating a pie with a fork in one black mitten hand, laughing, a tankard beside him.", text=[cap('Still fine at dinner'), clock('HOUR 12')]),
  'H07': ch('a30', W(), f"Morning on {SOHO}: the landlady, a stickman woman in a long 1850s dress and headscarf, fills a jug at the water pump with one black mitten hand, working the handle with the other.", text=cap('More water from the same pump')),
  'H10': ch('a31', C(.5, .45, 1.15), f"{ROOM}: close-up of {YOU} lying on the pillow, whispering something with a tiny faint speech squiggle, to the landlady who leans in apart from the bed, a hand cupped to her ear.", text=cap('A hoarse whisper')),
  'H13': ch('a32', W(), f"{ROOM}: the stickman doctor in a black frock coat pours brandy from a small bottle into a spoon held in one black mitten hand, while {YOU} lies grey-blue in the bed.", text=cap('Brandy for strength')),
  'H16': ch('a33', C(.5, .5, 1.05), f"{ROOM} by candlelight. Two figures only. On the left, {YOU} LIES flat on his back in the bed under the grey blanket, his grey-blue round head on the pillow, eyes closed, one sleeved arm resting on top of the blanket. On the right, standing beside the bed, a stickman doctor with NO cap, in a black frock coat, bends over him holding a brass pocket watch in his raised right hand and touching the patient's wrist with two fingers of his left black mitten hand, frowning. Only the doctor holds the watch.", text=cap('A pulse you can barely feel')),
  'H18': ch('a34', W(), f"A narrow dark 1854 back yard with a brick cesspit grate: the landlady in a long dress and headscarf carries a tin bucket in one black mitten hand toward the grate, her other hand holding her apron.", text=cap('Into the cesspit')),
  'H19': ch('a35', W(), f"An empty {SOHO} at noon: several doors with black mourning cloth, a covered handcart waiting outside one house, shutters closed, no people.", text=cap('Broad Street, September 1854')),
  'H21': ch('a36', C(.5, .5, 1.05), "A dim 1854 study lit by a candle: a stickman doctor with short dark side whiskers drawn as simple lines and a dark frock coat sits at a desk, marking small black bars on a street map with a pen held in one black mitten hand.", text=cap('Mapping every death')),
  'T02': ob('a37', "A modern table: a small foil sachet of oral rehydration salts without readable writing, torn open beside a clear glass of water with a spoon, soft daylight."),
  'T05': ch('a38', C(.5, .5, 1.05), "A modern village courtyard: a stickman woman in a bright headscarf boils water in a metal pot over a small gas burner, stirring with a spoon held in one black mitten hand, a child in a T-shirt standing apart beside her.", modern=True, text=cap('Boil it first')),
}
for _i, _r, _t, _sh in B:
    if _i in EXTRA: _sh.insert(1, EXTRA[_i])
# shot order must follow the narration
ORDER = {'H04': ['a29', 'd02'], 'H13': ['a15', 'd07', 'a32'], 'H21': ['a36', 'a19']}
for _n, (_i, _r, _t, _sh) in enumerate(B):
    if _i in ORDER:
        _by = {x['img']: x for x in _sh}
        B[_n] = (_i, _r, _t, [_by[k] for k in ORDER[_i]] + [x for x in _sh if x['img'] not in ORDER[_i]])

def lines():
    for i, r, t, _ in B:
        if i: print(f"{i}|{r}|{t}")

def frames():
    seen, out = set(), []
    for _, _, _, shots in B:
        for s in shots:
            if 'prompt' in s and s['img'] not in seen:
                seen.add(s['img'])
                out.append({'img': s['img'], 'prompt': s['prompt'], 'refs': [K_SHEET] if 'K' in s['refs'] else []})
    json.dump(out, open(os.path.join(ROOT, 'tools/plague/whatif01_frames_todo.json'), 'w'), indent=1); print(len(out), 'frames')

def beats():
    out = {'base': 'assets/plague/whatif01/frames', 'keep_zoom': [], 'static': True, 'fade_in': .8, 'start': 0.0, 'lead': .35, 'gap': .35, 'max_shot': 2.6,
           'sfx_global': [{'kind': 'drone', 't': 0.0, 'args': {'d': 'ALL'}, 'gain': .9}], 'beats': []}
    M = 'assets/plague/music/'
    out['music'] = [{'file': M + f, 't0': float(a0), 't1': a1, 'gain': 1.0, 'fade_in': 2.0 if a0 == 0 else 4.0, 'fade_out': 5.0 if a1 == 'ALL' else 4.0}
                    for a0, a1, f in MUSIC]
    for i, r, t, shots in B:
        sl = []
        for s in shots:
            d = {'img': s['img'], 'from': s['cam'][0], 'to': s['cam'][1], 'w': s['w']}
            if 'text' in s: d['text'] = s['text']
            sl.append(d)
        if i: out['beats'].append({'vo': f'assets/plague/whatif01/vo_fast/{i}.wav', **({'gain': 1.05} if r == 'CHOLERA' else {}), 'shots': sl})
        else: out['beats'].append({'hold': t, 'shots': sl})
    json.dump(out, open(os.path.join(ROOT, 'tools/plague/whatif01_beats.json'), 'w'), indent=1); print(len(out['beats']), 'beats')

MUSIC = [(0, 120, 'cholera_a.mp3'), (116, 236, 'cholera_b.mp3'), (232, 'ALL', 'cholera_a.mp3')]

{'lines': lines, 'frames': frames, 'beats': beats}[sys.argv[1]]()
