"""Episode 1 (The ENTIRE History of the Plague): single source of truth.

Every beat = one narration/character line (id, role, text) + the shots that cover it.
A shot either reuses an existing frame or defines a new one to generate (prompt + references).

  python3 tools/plague/ep01_spec.py lines   -> voices list for TTS  (id|ROLE|text)
  python3 tools/plague/ep01_spec.py frames  -> frames_todo.json (new frames to generate)
  python3 tools/plague/ep01_spec.py beats   -> tools/plague/ep01_beats.json (for beats.py)
"""
import sys, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P_SHEET, S_SHEET = '80552411-22ff-414f-8f40-9af41f66ebff', '9185ef25-1343-4cea-8e45-133d20eb4894'  # stickmen_cast_nodoc.jpg (plague doctor removed)
STYLE = "2D animated history explainer frame, 16:9, no text. Hand-drawn ink illustration, clean black outlines, muted grey-sepia palette; warm light only from fire, candles, lanterns. Not gory."
STICK = "EVERY human is a simple STICKMAN exactly like the attached stickman sheet: plain white round head, two dot eyes, simple mouth, NO nose, NO beard, NO realistic faces, thin black stick arms and legs, simple period clothes. NO plague doctors, NO beaked or bird masks anywhere."
PLAGUE = "The Plague exactly as on the attached sheet: tall thin figure, tattered black-brown hooded cloak, shadowed face, small glowing white eyes, hooked grey nose, thin cruel smile, grey spotted bony hands, bronze clasp, red-eyed black rat on his shoulder; his trunk = battered leather trunk with city stickers."

def W(): return [[.5, .5, 1.0], [.5, .5, 1.05]]                      # wide, slow push
def WL(): return [[.47, .5, 1.04], [.53, .5, 1.04]]                  # slow pan right
def WR(): return [[.53, .5, 1.04], [.47, .5, 1.04]]
def C(x, y, z=1.4): return [[x, y, z], [x, y, z + .08]]              # close-up
def O(): return [[.5, .5, 1.08], [.5, .5, 1.0]]                      # pull out

def sh(img, cam=None, prompt=None, refs='', text=None, sfx=None, w=1):
    s = {'img': img, 'cam': cam or W(), 'w': w}
    if prompt: s['prompt'] = prompt; s['refs'] = refs
    if text: s['text'] = text
    if sfx: s['sfx'] = sfx
    return s
def cap(t, **k): return {'text': t, 'x': 960, 'y': 985, 'size': 50, 'at': .3, **k}                      # plate caption
def stamp(t, **k): return {'text': t, 'x': 1380, 'y': 240, 'size': 96, 'style': 'stamp', 'pop': True, 'at': .5, **k}
def ink(t, x, y, size=64, **k): return {'text': t, 'x': x, 'y': y, 'size': size, 'style': 'ink', 'at': .3, **k}   # written on paper in the frame
def dim(rect, **k): return {'style': 'dim', 'rect': rect, 'text': '', 'size': 1, 'x': 0, 'y': 0, 'at': 0, **k}
PANEL = [(444, 200, 800, 526), (840, 200, 1200, 526), (1244, 200, 1624, 526)]
MENU_W = [('BUBONIC', 'the lumps'), ('SEPTICEMIC', 'the blood'), ('PNEUMONIC', 'the lungs')]
def MENU(n):   # menu board: words written into the panels one by one, the current panel lit, the others dimmed
    out = []
    for i in range(n + 1):
        cx = (PANEL[i][0] + PANEL[i][2]) // 2
        out += [{**ink(MENU_W[i][0], cx, 562, 46, maxw=300, at=.3 if i == n else 0), 'style': 'tag'}]
    return out + [dim(PANEL[i], fill=[0, 0, 0, 150]) for i in range(3) if i != n]
STILL = [[.5, .5, 1.0], [.5, .5, 1.02]]   # near-static wide: keeps in-picture text aligned
def label(t, x, y, size=64, **k): return {'text': t, 'x': x, 'y': y, 'size': size, 'at': .3, **k}

B = []   # beats: (id, role, text, shots)  role None = silent hold (text holds seconds)
def N(i, t, *s): B.append((i, 'NARRATOR', t, list(s)))
def Pl(i, t, *s): B.append((i, 'PLAGUE', t, list(s)))
def HOLD(sec, *s): B.append((None, None, sec, list(s)))

# ---- 0:40 Who is he?
N('L06a', "So who is he, exactly? Under a microscope, the plague is a bacterium called Yersinia pestis. A tiny rod. Which explains the figure.",
  sh('f06a', W(), "An old brass microscope on a cluttered wooden desk in a dim study, a single oil lamp, glass slides, notebooks."),
  sh('f06b', C(.5, .5, 1.2), "View through a microscope: a round bright circular field on black, full of tiny rod-shaped bacteria drawn as little dark capsules; one of the rods in the centre wears a tiny black hood and has two tiny glowing white eyes. Cute but sinister."),
  sh('f06c', O(), PLAGUE + " Full-body shot: the Plague standing very tall and very thin against grey fog, emphasising how long and rod-like his silhouette is.", 'P'))
Pl('L06b', "I travel light.",
  sh('f06d', C(.5, .45, 1.15), PLAGUE + " Medium shot: the Plague lifts his battered leather travel trunk with one bony finger, smug, in a foggy night street.", 'P'))
N('L07', "He lives in rodents, mostly rats, and he travels by flea. A flea bites an infected rat, the bacteria block the flea's gut, and the starving flea starts biting everything it can find. Including you.",
  sh('f07a', W(), "A black rat sitting on a barrel in a narrow medieval alley at night, lantern light, fog."),
  sh('f07b', C(.5, .5, 1.1), "Extreme close-up, cartoon-stylised: a single flea, drawn like a tiny armoured bug with a cranky face, standing on the fur of a rat. Not gross."),
  sh('f07c', W(), STICK + " A comic diagram painted on aged parchment: a rat, an arrow, a flea, an arrow, a stickman; small doodled germs travel along the arrows. No words.", 'S'),
  sh('f07d', C(.5, .45, 1.2), STICK + " A stickman peasant in a doorway scratching his ankle, annoyed, a tiny flea hopping onto him.", 'S'))
N('L08a', "His travel partner is the black rat, whose scientific name, and we are not making this up, is Rattus rattus.",
  sh('co_08', C(.38, .45, 1.25), text=label('RATTUS RATTUS', 1300, 760, 76, len=4.0)),
  sh('f08b', C(.5, .5, 1.1), PLAGUE + " Close-up of the rat on the Plague's shoulder, smug; on the rat's nose sits a tiny flea wearing a little postman's satchel.", 'P', text=label('(yes, really)', 1300, 900, 56, len=3.0)))
Pl('L08b', "Rattus handles transport. The fleas handle deliveries.",
  sh('f08c', W(), PLAGUE + " The Plague strides down a foggy cobbled road with his trunk; the rat rides on his shoulder; behind them several tiny fleas hop along carrying tiny mail satchels.", 'P'))
N('L09', "Once inside, he comes in three flavors. Bubonic: it attacks the lymph nodes, which swell up into lumps called buboes. That's where the name comes from. Septicemic: it gets into the blood. And pneumonic: it gets into the lungs, and that version can spread from person to person with a cough.",
  sh('f09a', W(), "A dark wooden tavern menu board with three empty framed panels in a row, each panel with a simple icon: a small round lump, a drop, a pair of lungs. Candlelit. No words.",
     text=[label('THE MENU', 960, 105, 56, len=99)]),
  sh('f09a', STILL, text=MENU(0)),
  sh('f09b', W(), STICK + " A stickman medieval doctor points with a stick at a big anatomical chart of a stickman with small dots at the neck, armpits and groin. Simple, not medical-gory.", 'S'),
  sh('f09a', STILL, text=MENU(1)),
  sh('f09a', STILL, text=MENU(2)),
  sh('f09d', W(), STICK + " A stickman coughing into his elbow in a market; a little cartoon cloud with tiny dark specks drifts toward another stickman who looks alarmed.", 'S'))
N('L10', "Without treatment, the bubonic plague killed around half of the people it infected. The pneumonic plague killed almost all of them.",
  sh('f10a', C(.5, .45, 1.15), PLAGUE + " The Plague holds up three long bony fingers proudly, cruel smile, fog behind.", 'P'),
  sh('f10b', W(), "A dark quiet medieval room: a single candle burning beside an empty bed with a folded blanket. Somber, still. No people."))

# ---- 1:40 Origins
N('L11', "For a long time, everyone assumed his story began in the Middle Ages. Then scientists learned to read DNA from ancient skeletons.",
  sh('f11a', W(), STICK + " An archaeological dig: a stickman archaeologist with a hat kneels in a trench and brushes dirt off an ancient tooth sticking out of the soil. Ropes, grid string, tools.", 'S'),
  sh('f11b', W(), STICK + " A modern genetics lab: a stickman scientist in a white coat looks at a screen showing a DNA double helix; an ancient tooth sits in a dish.", 'S'))
N('L12a', "And they found him inside the teeth of people who died about five thousand years ago, in the late Stone Age and the Bronze Age, from the Baltic all the way to Siberia.",
  sh('f12a', C(.5, .5, 1.1), PLAGUE + " A giant ancient tooth on a lab table; a tiny version of the Plague climbs out of a crack in it, stretching and yawning sleepily; the tiny rat yawns too. Funny.", 'P'),
  sh('f12b', WL(), "An old parchment map of Europe and northern Asia drawn in ink, from the Baltic Sea to Siberia, with a few small dark dots scattered across the steppe. No words."))
Pl('L12b', "Five thousand years, and nobody called?",
  sh('f12c', C(.5, .45, 1.15), PLAGUE + " The Plague brushes dust off his cloak, offended, looking at the viewer.", 'P'))
N('L12c', "But where did he come from in the first place? His ancestor was a fairly harmless bug called Yersinia pseudotuberculosis. It lived in soil and water, and at worst it gave you a bad stomach ache. Then, over a handful of mutations, it picked up a few new genes, threw away a lot of old ones, and turned into something much worse.",
  sh('f12d', W(), "A cute harmless little rod-shaped microbe with a sleepy friendly face, drawn like a small pale capsule with a tiny smile, lounging in a puddle of muddy water among pebbles and grass. Cartoon, gentle, muted colours."),
  sh('f12e', WL(), "A comic diagram on aged parchment, left to right: a small friendly pale rod-shaped microbe, then an arrow with a few glowing little DNA strands flying into it and some old strands falling away, then the same rod now dark, wearing a tiny black hood with two small glowing white eyes. No words."),
  sh('f12d', C(.5, .5, 1.3)))
Pl('L12d', "Everyone starts somewhere.",
  sh('f12f', C(.5, .45, 1.1), PLAGUE + " The Plague holds an old oval framed portrait of a cute harmless little pale rod-shaped microbe with a tiny bow tie, looking at it with a nostalgic, cruel smirk. He holds the frame with both hands. No trunk.", 'P'))
N('L13a', "Those early versions probably couldn't travel by flea yet. That trick came later, as the bacterium evolved. Some researchers think the plague may have helped empty out parts of Stone Age Europe. Others aren't convinced.",
  sh('f13a', W(), STICK + " A Bronze Age village of round thatched huts on a misty river, stickmen in furs and simple tunics working, smoke from fires.", 'S'),
  sh('f13b', WL(), STICK + " " + PLAGUE + " Instead of the trunk the Plague carries a small leather sack, walking into the Bronze Age village of thatched huts; stickmen look at him curiously.", 'PS'),
  sh('f13c', W(), "The same kind of Bronze Age village, now quiet and half empty, an overgrown path, a lone dog, mist. No people."))
Pl('L13b', "Allegedly.",
  sh('f13d', C(.5, .45, 1.15), PLAGUE + " The Plague shrugs innocently, palms up, eyebrows raised under the hood.", 'P'))

# ---- 2:40 Justinian
N('L14', "His first big headline came in 541 AD, in Constantinople, the capital of the Eastern Roman Empire.",
  sh('f14a', WL(), "Panorama of Byzantine Constantinople in 541 AD: the great domes of Hagia Sophia, city walls, the Bosporus with ships, pale sky.",
     text=cap('CONSTANTINOPLE · 541 AD')))
N('L15', "The emperor Justinian was busy trying to win back the old Roman Empire. Then grain ships arrived from Egypt. With grain. With rats. With fleas. And with him.",
  sh('f15a', W(), STICK + " A stickman Byzantine emperor in purple robes and a jewelled crown moves little army figurines on a big map of the Mediterranean on a marble table.", 'S'),
  sh('f15b', W(), "Big grain ships with square sails arriving into the harbour of Constantinople, dock workers unloading sacks."),
  sh('f15c', C(.5, .55, 1.2), "Close-up of grain sacks on a ship's deck; a few black rats peek out between the sacks."),
  sh('f15d', W(), PLAGUE + " The Plague sits on top of the grain sacks on the ship with his trunk, waving cheerfully; the rat munches grain.", 'P'))
N('L17', "The historian Procopius wrote that at its worst, up to ten thousand people a day were dying in the city. Even the emperor himself caught it.",
  sh('f17a', W(), STICK + " A stickman Byzantine historian writing on a long scroll by candlelight, his face shocked at what he is writing.", 'S'),
  sh('f17b', W(), "Empty streets of Constantinople, shuttered doors, a few lit windows, grey dusk. No people. Sad and quiet."),
  sh('f17c', W(), STICK + " " + PLAGUE + " The stickman emperor lies sick in a big bed, crown still on his head, a cold towel on his forehead; the Plague sits on the edge of the bed calmly checking a long list.", 'PS'))
N('L18', "Justinian survived. His dream of rebuilding Rome mostly didn't.",
  sh('f18a', W(), STICK + " The stickman emperor, recovered but tired, looks sadly at a map of the Mediterranean where most of his army figurines have fallen over.", 'S'))
N('L19', "For the next two hundred years, he kept coming back to the Mediterranean in waves. And then, he vanished. For about six hundred years.",
  sh('f19a', WL(), "An old parchment map of the Mediterranean Sea drawn in ink with dark ink-wash smudges rippling out from the coasts like waves. No words.",
     text=label('541 – 750', 1450, 200, 84, len=99)),
  sh('f19b', W(), PLAGUE + " The Plague closes the door of an old house behind him and hangs a wooden sign on the door that reads exactly: \"BACK IN 600 YEARS\".", 'P'))
Pl('L20', "I needed some me-time.",
  sh('f20a', W(), PLAGUE + " The Plague lounges in a hammock between two trees on a misty Central Asian steppe, hands behind his head; the rat sleeps on his chest; the trunk is parked below.", 'P'))

# ---- 4:10 Black Death
N('L21', "He spent it somewhere in Central Asia, getting ready for the comeback. In the 1340s he headed west along the Silk Road, with merchants, caravans and armies.",
  sh('f21a', WL(), "An old parchment map of the Silk Road from Central Asia to the Black Sea drawn in ink, with a dotted line of tiny footprints and tiny rat paw prints heading west. No words."),
  sh('f21b', W(), STICK + " " + PLAGUE + " A camel caravan of stickman merchants crossing a desert at dusk; at the back of the caravan the Plague rides a camel with his trunk strapped on.", 'PS'))
N('L22', "In 1346, the army of the Golden Horde was besieging Caffa, a Genoese trading port in Crimea. The plague broke out among the besiegers.",
  sh('f22a', W(), STICK + " The walled Genoese port of Caffa on the Black Sea coast, and outside the walls a huge camp of tents of a besieging army.", 'S', text=cap('CAFFA · 1346')),
  sh('f22b', W(), STICK + " In the besiegers' camp, stickman soldiers in pointed helmets sit by tents looking sick and miserable, one coughing, one shivering in a blanket.", 'S'))
N('L23', "One chronicler claimed they launched their dead over the city walls. Historians still argue about whether that really happened. Either way, Genoese ships soon sailed away from Caffa, and the plague sailed with them.",
  sh('f23a', W(), STICK + " A stickman medieval chronicler with a quill, a big question mark floating above his head.", 'S'),
  sh('f23b', W(), "A distant dark silhouette of a wooden catapult against a dusk sky beyond city walls. Far away, nothing graphic."),
  sh('f23c', W(), PLAGUE + " Genoese galleys sail away from Caffa at sunset; at the stern of the last ship stands the Plague, waving goodbye.", 'P'))
N('L24', "Which brings us back to Messina. October 1347.",
  sh('co_01', W(), text=cap('MESSINA · OCTOBER 1347')),
  sh('co_06', C(.45, .45, 1.3)))
N('L25', "From Sicily, he toured Europe faster than any king ever could. 1348: Italy, France, Spain and England. 1349: Germany, Scandinavia. By 1351, Russia.",
  sh('f25a', C(.55, .62, 1.6), "An old parchment map of medieval Europe drawn in ink from Spain to Russia, with a dark ink-wash stain spreading north from Sicily across Italy and France. No words."),
  sh('f25a', C(.45, .5, 1.25), text=ink('1348', 1650, 200, 120, len=99)),
  sh('f25a', C(.55, .4, 1.15), text=ink('1349', 1650, 200, 120, len=99)),
  sh('f25a', W(), text=ink('1351', 1650, 200, 120, len=99)))
Pl('L26', "Every city. Sold out.",
  sh('f26a', C(.47, .62, 1.45), PLAGUE + " Close-up of the Plague's battered leather travel trunk covered in old travel stickers that read exactly: \"MESSINA 1347\", \"FLORENCE 1348\", \"PARIS 1348\", \"LONDON 1348\", \"BERGEN 1349\". His bony hand rests on it.", 'P'))
N('L27', "In Florence, the writer Giovanni Boccaccio described people who ate breakfast with their families in the morning, and that same night dined with their ancestors in the next world.",
  sh('f27a', WL(), "Florence in 1348: the great red dome of the cathedral above grey rooftops, the river Arno, overcast sky.", text=cap('FLORENCE · 1348')),
  sh('f27b', W(), STICK + " A stickman writer in a red medieval cap writing at a wooden desk by a window, quill and stacks of paper.", 'S'))
N('L27a', "Boccaccio also wrote one of the most famous books of the Middle Ages about it, the Decameron: ten young people flee Florence to a villa in the countryside and pass the time telling each other a hundred stories. History's first quarantine binge-watch.",
  sh('f27c', W(), STICK + " Ten young stickman nobles in colourful medieval clothes sit in a circle in the sunny garden of a Tuscan villa, one telling a story with big gestures, the others listening.", 'S'),
  sh('f27c', C(.5, .55, 1.35)),
  sh('f27d', W(), STICK + " The same young stickman nobles laughing and eating grapes on a villa terrace with cypress trees, a big open book on the table.", 'S'),
  sh('f27e', W(), PLAGUE + " The Plague peeks out from behind a stone column of the villa, sulking and left out, watching the party.", 'P'))
Pl('L27aP', "I wasn't invited. Rude.", sh('f27e', C(.4, .4, 1.45)))
N('L27b', "Even the Pope took precautions. In Avignon, Pope Clement the Sixth followed his doctor's advice and spent his days sitting between two enormous fires, to purify the air. Strangely enough, it may have helped: fleas don't love extreme heat.",
  sh('f27f', WL(), "The papal palace of Avignon on the Rhône, grey Gothic towers, overcast sky.", text=cap('AVIGNON · 1348')),
  sh('f27g', W(), STICK + " A stickman Pope in white robes and a tall papal hat sits on a throne between two enormous roaring bonfires, sweating, fanning himself.", 'S'),
  sh('f27g', C(.5, .45, 1.4)),
  sh('f27h', C(.5, .55, 1.1), "Cartoon: a few tiny fleas running away from a big fire, sweating and fanning themselves."))
Pl('L27bP', "Honestly? Respect.",
  sh('f27i', W(), PLAGUE + " The Plague stands at a distance from the fires, slowly clapping, impressed; the rat claps too.", 'P'))
N('L27c', "By the way, nobody back then called it the Black Death. People called it the great pestilence, or the great mortality. The name 'Black Death' only caught on centuries later.",
  sh('f27j', STILL, "An open aged parchment manuscript on a desk, with blank space for writing in the middle, candle, quill.",
     text=[ink('THE GREAT', 625, 520, 62, len=99), ink('PESTILENCE', 625, 610, 72, len=99), ink('THE GREAT', 1200, 520, 62, at=1.6, len=99), ink('MORTALITY', 1200, 610, 72, at=1.6, len=99)]),
  sh('f27j', C(.5, .5, 1.1), text=stamp('THE BLACK DEATH', x=960, y=560, size=104, rot=-5, at=.4, len=99)))
Pl('L27cP', "Took them long enough to get my name right.",
  sh('f27k', C(.5, .5, 1.1), PLAGUE + " The Plague polishes a small brass nameplate on his trunk with a cloth, satisfied; the nameplate reads exactly: \"THE BLACK DEATH\".", 'P'))
N('L28', "Towns lost a third of their people, half, sometimes more. For Europe as a whole, estimates run from about thirty to sixty percent of the population, in about five years. It was one of the deadliest disasters in human history.",
  sh('f28a', WL(), "An empty medieval street, every shutter closed, a church bell tower at the end, fog. No people. Quiet and sad."),
  sh('f28b', W(), "An empty medieval market square, an abandoned cart, scattered baskets, a lone crow, grey morning. No people."),
  sh('f28c', W(), "Inside a stone church: many candles burning, empty pews, soft light. No people."))
HOLD(3.0, sh('f28d', O(), "A church bell tower at dusk silhouetted against a grey sky, a single bird. Calm, mournful."))

# ---- 7:00 Fighting back
N('L30', "So how did people fight back? Mostly, badly. The top medical experts in Paris officially concluded that the cause was a conjunction of Saturn, Jupiter and Mars, back in 1345.",
  sh('f30a', W(), STICK + " A grand medieval university hall in Paris: stickman scholars in long robes and caps gather around a huge astrological star chart, pointing seriously.", 'S'),
  sh('f30b', C(.5, .5, 1.1), "Close-up of an ornate medieval astrological chart with three planets drawn as faces lined up, Saturn with rings, Jupiter, red Mars."))
Pl('L31', "Excuse me? I did the work.",
  sh('f31a', W(), STICK + " " + PLAGUE + " The Plague bursts through the doors of the scholars' hall, indignant, pointing at himself; the rat on his shoulder points too; the stickman scholars stare.", 'PS'))
N('L32', "Others blamed bad air, which they called miasma. So people carried flowers and herbs, burned incense, and tried very hard to avoid bad smells.",
  sh('f32a', W(), STICK + " Medieval stickman townspeople walk down a street holding big bouquets of flowers and herbs pressed to their noses.", 'S'),
  sh('f32b', W(), STICK + " A stickman swinging a smoking incense burner in a street, clouds of fragrant smoke.", 'S'),
  sh('f32c', C(.5, .45, 1.25), STICK + " A stickman sniffing the air suspiciously, eyes narrowed.", 'S'))
N('L33', "Some decided God was angry, and marched from town to town whipping their own backs in penance. They were called the flagellants. It did not help.",
  sh('f33a', WL(), STICK + " Wide shot from far away: a procession of stickmen in hooded robes carrying banners and crosses walks along a country road between two towns. Distant, no details of injuries.", 'S'),
  sh('f33b', W(), STICK + " Stickman villagers by the road watch the procession pass, unimpressed, one holding a flower to his nose.", 'S'))
N('L34', "And some people went looking for someone to blame. Across Europe, Jewish communities were falsely accused of poisoning the wells, and thousands of people were murdered. It is one of the darkest chapters of this whole story.",
  sh('f34a', W(), "A dark old European town square at night with an old stone well in the middle, rain, no people. Somber."),
  sh('f34b', C(.5, .55, 1.1), "Memorial candles burning on a wet stone step in the rain, a small pile of stones beside them. Quiet, respectful."))
N('L35', "But one idea actually worked. In 1377, the port city of Ragusa, today's Dubrovnik, ordered ships from infected places to wait thirty days before anyone could come ashore.",
  sh('f35a', WL(), "The walled port city of Ragusa (Dubrovnik) on the Adriatic coast on a clear morning, terracotta roofs, stone walls, calm sea (still muted colours).", text=cap('RAGUSA · 1377')),
  sh('f35b', W(), STICK + " A merchant ship anchored offshore; bored stickman sailors on deck, one scratching tally marks on the mast to count days.", 'S'))
N('L36', "Later, places like Venice stretched it to forty days. In Italian, forty days is quaranta giorni. And that's where we get the word quarantine.",
  sh('f36a', WL(), "The Venetian lagoon with a merchant ship at anchor flying a yellow flag, Venice skyline in the distance, mist."),
  sh('f36b', C(.5, .5, 1.1), STICK + " A stickman Venetian official with a big ledger counting days; a wall behind him full of tally marks.", 'S',
     text=label('QUARANTA GIORNI = QUARANTINE', 960, 150, 58, at=1.2, len=99)))
Pl('L36P', "Forty days? I have a schedule.",
  sh('f36c', W(), PLAGUE + " On the deck of the anchored ship the Plague stands with arms crossed, tapping his foot impatiently and checking a pocket watch.", 'P'))
N('L37', "And that famous plague doctor with the bird mask? It didn't exist during the Black Death. The costume first shows up about three hundred years later, in the 1600s. The beak was stuffed with herbs to filter out the bad air.",
  sh('f37a', W(), STICK + " A stickman plague doctor in a long black coat, wide-brimmed hat and beaked bird mask over his round head strides into a 1600s street.", 'S',
     text=stamp('WRONG CENTURY')),
  sh('f37b', C(.5, .5, 1.1), "Cutaway diagram of a beaked plague doctor mask showing dried herbs, flowers and spices stuffed inside the beak, on aged paper."))
Pl('L38', "Cute. Didn't work.",
  sh('f38a', W(), STICK + " " + PLAGUE + " The Plague leans in and inspects the stickman plague doctor up close, one eyebrow raised, unimpressed; the doctor freezes.", 'PS'))

# ---- 9:00 After
N('L39', "When the Black Death finally moved on, Europe was a different place. With so many workers gone, the survivors could suddenly ask for higher wages.",
  sh('f39a', WL(), STICK + " A wide medieval wheat field with only three stickman peasants working, lots of empty space, a castle on a hill.", 'S'),
  sh('f39b', W(), STICK + " In a castle hall a stickman lord clutches his head in despair at an empty work rota.", 'S'),
  sh('f39c', C(.5, .5, 1.15), STICK + " A confident stickman peasant holds out his hand with a few coins, demanding more, smug.", 'S'))
N('L40', "Lords tried to stop them. In England, a law tried to freeze wages at their old, pre-plague level. It didn't really work.",
  sh('f40a', STILL, "A royal decree scroll with a red wax seal pinned to a wooden post in a village. Leave the scroll surface plain.",
     text=[ink('STATUTE OF', 1505, 320, 66, maxw=470, len=99), ink('LABOURERS', 1505, 405, 66, maxw=470, len=99), ink('1351', 1505, 535, 96, at=.8, len=99)]),
  sh('f40b', W(), STICK + " Stickman peasants walk past the decree on the post, ignoring it completely, one yawning.", 'S'))
N('L41', "Thirty years later, England got the Peasants' Revolt. Many historians argue the plague helped crack the old feudal system wide open.",
  sh('f41a', WL(), STICK + " A crowd of angry stickman peasants with pitchforks, scythes and banners marching toward medieval London.", 'S', text=cap('ENGLAND · 1381')),
  sh('f41b', C(.5, .5, 1.1), "A stone castle wall with a big crack running down it, dust falling. Symbolic."))
Pl('L42a', "You're welcome?", sh('f42a', C(.5, .45, 1.15), PLAGUE + " The Plague shrugs with open hands, faking modesty.", 'P'))
N('L42b', "Nobody thanked him.",
  sh('f42b', W(), STICK + " " + PLAGUE + " A crowd of stickmen glare at the Plague with arms crossed; he stands alone, awkward.", 'PS'))

# ---- 10:00 London
N('L43', "But he never really left. For three hundred years, he kept coming back every few decades.",
  sh('f43a', STILL, "A long aged parchment scroll unrolled across the frame like a timeline, with small ink vignettes of towns along it and dark ink blots at intervals. Leave the scroll free of words.",
     text=[ink('1350', 230, 770, 80), ink('1500', 960, 770, 80, at=1.0), ink('1650', 1700, 770, 80, at=1.8)]))
N('L44', "His last big show in England was London, 1665. The Great Plague killed around a hundred thousand people, close to a quarter of the city.",
  sh('f44a', WL(), STICK + " London in 1665: crowded timber-framed houses, the Thames with boats, old St Paul's cathedral with its tower, grey sky.", 'S', text=cap('LONDON · 1665')),
  sh('f44b', C(.5, .5, 1.1), "A wooden door in old London with a large red cross painted on it, shut, a lantern beside it. No people."),
  sh('f44c', W(), STICK + " A stickman plague doctor in a beaked mask, black coat and hat walks down a narrow 1665 London street with a cane.", 'S'))
N('L45', "Cambridge University shut down, and a young student named Isaac Newton went home to his family's farm.",
  sh('f45a', W(), STICK + " The gate of a Cambridge college shut with a sign that reads exactly \"CLOSED\"; a young stickman student with long curly hair and a bag walks away.", 'S'))
N('L46', "With nothing else to do, he worked on calculus, light and gravity. Quarantine productivity at its finest.",
  sh('f46a', W(), STICK + " " + PLAGUE + " A young stickman Isaac Newton sits under an apple tree on a farm reading; hidden in the branches above the Plague sits and drops an apple toward his head with a sly grin.", 'PS'),
  sh('f46b', W(), STICK + " Young stickman Newton in a dark room holds a glass prism; a beam of sunlight splits into a rainbow on the wall; notebooks full of equations.", 'S'))
N('L46a', "That same year, the plague reached Eyam, a small village in the north of England, reportedly in a bundle of cloth from London. And the villagers did something extraordinary. Led by their rector, they agreed to seal themselves off so the disease wouldn't spread to the towns around them. Neighbors left food at the village edge, and the villagers paid with coins left in holes in the boundary stones, soaked in vinegar.",
  sh('f46c', WL(), "The small stone village of Eyam among green-grey hills of Derbyshire, a church tower, dry stone walls, mist.", text=cap('EYAM · 1665')),
  sh('f46d', W(), STICK + " A stickman tailor in Eyam unwraps a bundle of cloth that arrived by cart from London.", 'S'),
  sh('f46e', W(), STICK + " A stickman rector in black clerical clothes speaks to the gathered villagers in an open green dell, they listen solemnly.", 'S'),
  sh('f46f', W(), STICK + " On a hill at the village edge, stickman neighbours leave baskets of bread and food beside a large boundary stone and walk away.", 'S'),
  sh('f46g', C(.5, .5, 1.1), "Close-up of a weathered boundary stone with small holes carved in it, the holes filled with vinegar and a few old coins."))
N('L46b', "A large share of the village died. But the plague didn't get past them.",
  sh('f46h', O(), "The church of Eyam at sunset, quiet graveyard grass, a single warm window. Calm, respectful. No people."))
N('L46c', "And no, the nursery rhyme Ring a ring o' roses is probably not about the plague. That theory only appeared in the twentieth century, and most folklorists don't buy it.",
  sh('f46i', W(), STICK + " Stickman children holding hands and dancing in a ring on a village green, cheerful.", 'S', text=stamp('MYTH')))
Pl('L46cP', "I would never write something that catchy.",
  sh('f46j', C(.5, .45, 1.15), PLAGUE + " The Plague crosses his arms, offended, next to a music stand with a sheet of music.", 'P'))
N('L47', "Then, in September 1666, the Great Fire of London burned through much of the city. People said the fire had burned the plague away. Historians aren't so sure. The outbreak was already fading.",
  sh('f47a', WL(), "The Great Fire of London at night, 1666: an orange glow over the city, old St Paul's silhouetted, smoke, the Thames reflecting fire.", text=cap('SEPTEMBER 1666')),
  sh('f47b', W(), STICK + " Stickmen passing leather buckets of water in a chain toward a burning timber house.", 'S'))
Pl('L48', "I left on my own terms.",
  sh('f48a', W(), PLAGUE + " On a hill outside the burning city the Plague stands calmly holding a delicate teacup and saucer, sipping, unbothered, the orange glow behind him.", 'P'))
N('L48a', "Western Europe's last big outbreak came in 1720, in Marseille. A merchant ship carrying him arrived, and the quarantine was cut short, reportedly so its valuable cargo could make it to a trade fair in time.",
  sh('f48b', WL(), "The old port of Marseille in 1720 with a large merchant sailing ship, stone forts, hills.", text=cap('MARSEILLE · 1720')),
  sh('f48c', W(), STICK + " Stickman merchants in tricorn hats arguing with a stickman quarantine officer, waving contracts and bags of money.", 'S'))
N('L48b', "Roughly half the city died. Authorities built a long wall of stone across the countryside to keep the plague in. After that, he mostly stopped visiting Western Europe.",
  sh('f48d', WL(), STICK + " A long dry-stone wall snaking across the hills of Provence, stickman workers building it, soldiers standing guard.", 'S'))
Pl('L48bP', "They built me a wall. I've never felt so appreciated.",
  sh('f48e', C(.5, .45, 1.15), PLAGUE + " The Plague stands on top of the stone wall with a hand on his heart, touched, pretending to wipe a tear.", 'P'))

# ---- 11:00 Third pandemic
N('L49', "His last world tour began in China in the mid-1800s. By 1894 he reached Hong Kong, and from there steamships carried him to every inhabited continent. India alone lost more than ten million people.",
  sh('f49a', WL(), "Hong Kong harbour in 1894: steamships and sailing junks, colonial buildings at the foot of steep green hills, smoke from funnels.", text=cap('HONG KONG · 1894')),
  sh('f49b', W(), "An old world map drawn in ink with dotted steamship routes radiating from Hong Kong to every continent, little steamship icons. No words."))
N('L50', "But this time, science was waiting for him. In Hong Kong in 1894, a doctor named Alexandre Yersin found the culprit under his microscope. That's why he's called Yersinia pestis.",
  sh('f50a', W(), STICK + " A stickman doctor with a moustache looks into a brass microscope in a small straw-roofed hut laboratory, glassware around him.", 'S'),
  sh('f06b', C(.5, .5, 1.3)))
Pl('L51', "He named me after himself?",
  sh('f51a', C(.5, .45, 1.1), PLAGUE + " The Plague stares down in outrage at a name badge pinned to his cloak that reads exactly: \"YERSINIA PESTIS\".", 'P'))
N('L51a', "In 1900 he even reached San Francisco. The governor of California insisted there was no plague at all, because it would be bad for business. There was. It took years, and a huge campaign against the city's rats, to get rid of him.",
  sh('f51b', WL(), STICK + " San Francisco around 1900: cable cars, Victorian buildings, the bay, stickmen in hats.", 'S', text=cap('SAN FRANCISCO · 1900')),
  sh('f51c', W(), STICK + " " + PLAGUE + " A stickman governor at a podium waves his hands dismissively to a crowd; right behind him stands the Plague, smiling.", 'PS'),
  sh('f51d', W(), STICK + " Stickman city workers with traps and nets chasing rats through a street; rats fleeing.", 'S'))
Pl('L51aP', "Denial is my favorite disinfectant.", sh('f51c', C(.62, .4, 1.5)))
N('L52', "Meanwhile, in 1898, Paul-Louis Simond showed how rat fleas spread him.",
  sh('f52a', W(), STICK + " A stickman scientist with round glasses holds a magnifying glass over a glass jar with a flea inside.", 'S'))
N('L53', "And in the 1940s, antibiotics arrived. For the first time in five thousand years, the plague could be cured.",
  sh('f53a', W(), STICK + " A 1940s laboratory: a stickman woman scientist in a white coat raises a vial of medicine triumphantly.", 'S'),
  sh('f53b', W(), PLAGUE + " The Plague backs away in alarm, shielding himself with his trunk; the rat hides inside his hood.", 'P'))

# ---- 12:00 Today
N('L54', "So where is he now? Still around. Every year there are cases, mostly in Madagascar and the Democratic Republic of the Congo, and even a handful in the American Southwest, where he lives in prairie dogs.",
  sh('f54a', W(), "An old brass globe on a desk turned to show Africa and Madagascar, a few tiny glowing dots."),
  sh('f54b', W(), "Prairie dogs standing by their burrows in the dry American Southwest desert, mesas in the distance."))
Pl('L55', "I'm not gone. I'm semi-retired.",
  sh('f55a', W(), PLAGUE + " The Plague relaxes in a striped deck chair next to a prairie dog burrow in the desert, the trunk beside him with a new sticker that reads \"ARIZONA\", a small wooden sign reading exactly \"SEMI-RETIRED\".", 'P'))
N('L56', "But caught early, it's cured with a course of common antibiotics.",
  sh('f56a', C(.5, .5, 1.05), "A paper pharmacy bag on a counter with a small bottle of pills and a glass of water. Simple, clean."))
N('L57', "Five thousand years. Three pandemics. One of the deadliest diseases humanity has ever faced. Beaten, in the end, by a course of pills and a forty-day wait.",
  sh('f13a', W()), sh('f14a', W()), sh('co_01', W()), sh('f44a', W()), sh('f53a', W()), sh('f26a', C(.47, .62, 1.45)))
N('L58', "Next time: a killer that's been hiding in the water supply.",
  sh('f58a', C(.5, .5, 1.05), "An old cast-iron street water pump in a foggy Victorian street at night; a single drop of water falls from the spout, and inside the drop there is a tiny dark silhouette of a mysterious figure. Ominous."))
HOLD(5.0, sh('f58a', O(), text=[label('NEXT TIME', 1380, 360, 110, style='title', pop=True, at=.2, len=4.6), label('SUBSCRIBE', 1380, 500, 64, at=.8, len=4.0)]))

def lines():
    for i, r, t, _ in B:
        if i: print(f"{i}|{r}|{t}")

def frames():
    seen, out = set(), []
    for _, _, _, shots in B:
        for s in shots:
            if 'prompt' in s and s['img'] not in seen:
                seen.add(s['img']); refs = []
                if 'P' in s['refs']: refs.append(P_SHEET)
                if 'S' in s['refs']: refs.append(S_SHEET)
                out.append({'img': s['img'], 'prompt': STYLE + ' ' + s['prompt'], 'refs': refs})
    json.dump(out, open(os.path.join(ROOT, 'tools/plague/ep01_frames_todo.json'), 'w'), indent=1); print(len(out), 'frames')

def beats():
    cold = json.load(open(os.path.join(ROOT, 'tools/plague/cold_open_beats.json')))
    out = dict(cold); out['beats'] = list(cold['beats'])
    for i, r, t, shots in B:
        sl = []
        for s in shots:
            d = {'img': s['img'], 'from': s['cam'][0], 'to': s['cam'][1], 'w': s['w']}
            if 'text' in s: d['text'] = s['text']
            if 'sfx' in s: d['sfx'] = s['sfx']
            sl.append(d)
        if i: out['beats'].append({'vo': f'assets/plague/ep01/vo_full/{i}.wav', **({'gain': 1.05} if r == 'PLAGUE' else {}), 'shots': sl})
        else: out['beats'].append({'hold': t, 'shots': sl})
    json.dump(out, open(os.path.join(ROOT, 'tools/plague/ep01_beats.json'), 'w'), indent=1); print(len(out['beats']), 'beats')

{'lines': lines, 'frames': frames, 'beats': beats}[sys.argv[1]]()
