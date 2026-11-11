"""Episode 2 (The ENTIRE History of Cholera): single source of truth.

Same format as ep01_spec.py: every beat = one line (id, role, text) + the shots that cover it.

  python3 tools/plague/ep02_spec.py lines   -> voice list (id|ROLE|text), roles NARRATOR / CHOLERA
  python3 tools/plague/ep02_spec.py frames  -> tools/plague/ep02_frames_todo.json
  python3 tools/plague/ep02_spec.py beats   -> tools/plague/ep02_beats.json (for beats.py)
"""
import sys, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
K_SHEET = '578aebc8-20b7-4c82-930c-c1cc9e4e1b59'   # channel/plague/sheets/cholera_turn.jpg
S_SHEET = '84427fc9-09ce-40e6-b032-6f2700874458'   # channel/plague/sheets/stickmen_common.jpg
STYLE = "2D animated history explainer frame, 16:9, no text. Hand-drawn ink illustration, clean black outlines, muted grey-teal-sepia palette; warm light only from gas lamps, candles, lanterns. Not gory."
STICK = ("Humans are simple STICKMEN in the style of the attached stickman sheet: plain white round head, two dot eyes, no nose, no beard, thin black stick arms and legs, "
         "simple clothes of ordinary people of the period. KEEP IT SIMPLE: only the few figures described, standing apart, never overlapping; each figure has exactly two arms "
         "and two hands, clearly attached to its own sleeves; nothing floating. No crowds, no ghost figures, no kings, no plague doctors.")
KING = ("King Cholera exactly as on the attached sheet: a stout pot-bellied Victorian gentleman in a soaking-wet dark teal frock coat, brown waistcoat and cravat, a battered black "
        "top hat with a tarnished tin crown around it, clammy grey-blue skin, glowing pale-green eyes, a wide toothy grin; water drips from him constantly; a dented tin cup on a chain, "
        "and a small glass jar with a tiny shrimp-like copepod pet hanging from his watch chain. Exactly ONE King Cholera, with exactly two arms and two hands.")

def W(): return [[.5, .5, 1.0], [.5, .5, 1.05]]
def WL(): return [[.47, .5, 1.04], [.53, .5, 1.04]]
def WR(): return [[.53, .5, 1.04], [.47, .5, 1.04]]
def C(x, y, z=1.3): return [[x, y, z], [x, y, z + .08]]
def O(): return [[.5, .5, 1.08], [.5, .5, 1.0]]
STILL = [[.5, .5, 1.0], [.5, .5, 1.02]]

def sh(img, cam=None, prompt=None, refs='', text=None, sfx=None, w=1):
    s = {'img': img, 'cam': cam or W(), 'w': w}
    if prompt: s['prompt'] = prompt; s['refs'] = refs
    if text: s['text'] = text
    if sfx: s['sfx'] = sfx
    return s
def cap(t, **k): return {'text': t, 'x': 960, 'y': 985, 'size': 50, 'at': .3, **k}
def label(t, x, y, size=64, **k): return {'text': t, 'x': x, 'y': y, 'size': size, 'at': .3, **k}
def stamp(t, **k): return {'text': t, 'x': 1380, 'y': 240, 'size': 96, 'style': 'stamp', 'pop': True, 'at': .5, **k}
def ink(t, x, y, size=64, **k): return {'text': t, 'x': x, 'y': y, 'size': size, 'style': 'ink', 'at': .3, **k}
def ch(img, cam, p, **k): return sh(img, cam, STICK + ' ' + p, 'S', **k)            # stickman scene
def kg(img, cam, p, stick=False, **k): return sh(img, cam, (STICK + ' ' if stick else '') + KING + ' ' + p, 'K' + ('S' if stick else ''), **k)

B = []
def N(i, t, *s): B.append((i, 'NARRATOR', t, list(s)))
def K(i, t, *s): B.append((i, 'CHOLERA', t, list(s)))
def HOLD(sec, *s): B.append((None, None, sec, list(s)))

# ---- cold open: Broad Street, 1854
N('C01', "London. The last night of August, 1854. In Soho, on Broad Street, people start getting sick. Not slowly. By morning, whole families are down.",
  sh('c01a', WL(), "A narrow Victorian London street at night in 1854, Soho: soot-black brick houses, gas lamps in fog, a cast-iron public water pump on the corner. No people.", text=cap('BROAD STREET, LONDON · AUGUST 1854')),
  ch('c01b', C(.5, .5, 1.1), "Inside a cramped Victorian room at night: one stickman sits on the edge of a bed holding his stomach, sweating, a candle on a chair; a worried stickman woman stands by the door holding a basin."),
  sh('c01c', W(), "Morning in the same Victorian street: several doors marked with chalk crosses, shutters closed, a dropped bucket on the cobbles, fog. No people."))
N('C02', "Within three days, a hundred and twenty-seven people are dead. The doctors blame the air. The smell. A bad cloud over the city.",
  ch('c02a', W(), "Two Victorian stickman doctors in top hats stand in the foggy street, one pointing up at a dark greenish cloud of smoke hanging over the rooftops, the other holding a handkerchief to his nose."),
  sh('c02b', C(.5, .4, 1.15), "A greenish foul cloud drawn like a cartoon fog with a frowning face drifting over Victorian London chimneys at dusk."))
K('C03', "The smell! Honestly. I have never been so insulted.",
  kg('c03a', C(.5, .45, 1.1), "Medium shot: King Cholera stands in the foggy street at night, one hand on his chest, deeply offended, nose in the air, dripping water."))
N('C04', "One doctor thinks they're wrong. He thinks the killer is hiding somewhere much closer. In the water pump on the corner.",
  ch('c04a', W(), "A single stickman doctor in a dark Victorian coat and top hat stands alone in the foggy street at night, staring thoughtfully at a cast-iron public water pump."),
  sh('c04b', C(.5, .5, 1.25), "Close-up of the spout of a cast-iron Victorian water pump at night, a single drop of water hanging from it, gas-lamp glow. Ominous."))
K('C05', "Clever man. I hate him already.",
  kg('c05a', C(.5, .45, 1.1), "King Cholera peeks out from behind the cast-iron water pump at night, grinning, narrowing his glowing eyes, one hand on the pump."))
HOLD(4.6, kg('c06a', O(), "Title shot: King Cholera stands on the left third of the frame on a wet cobbled London street at night, under a gas lamp, holding his tin cup up like a toast; empty dark fog on the right side.",)
     | {'text': [label('CHOLERA', 1300, 330, 170, style='title', pop=True, at=.15, len=4.2), label('1817 – 2026', 1300, 480, 80, style='title', color=[150, 196, 186], at=.5, len=3.9)],
        'sfx': [{'kind': 'boom', 'at': .1, 'gain': .8}]})

# ---- who is he
N('L01', "So who is he? Under a microscope, cholera is a bacterium called Vibrio cholerae. It's shaped like a little comma, with a long whip for a tail. And it swims fast.",
  sh('c07a', W(), "An old brass microscope on a cluttered Victorian desk lit by a gas lamp, glass slides, notebooks."),
  sh('c07b', C(.5, .5, 1.15), "View through a microscope: a round bright circular field on black, full of tiny comma-shaped curved bacteria each with one long whip-like tail, zooming around; one in the centre wears a tiny tin crown. Cute but sinister."),
  sh('c07c', W(), "A cartoon: a tiny comma-shaped bacterium with a whip-like tail racing through water like a speedboat, leaving a wake, with a smug face."))
K('L02', "Streamlined, darling. Streamlined.",
  kg('c08a', C(.5, .45, 1.1), "King Cholera smooths his wet lapels proudly and poses side-on, showing off his round silhouette, smug."))
N('L03', "He doesn't need rats or fleas. He travels by water. A sick person sheds billions of bacteria. If that waste gets into a well, a river or a water pipe, the next person who takes a drink gets him too.",
  sh('c09a', W(), "A comic diagram painted on aged parchment: a sick stickman, an arrow to a cesspit, an arrow through the soil to a well, an arrow to a cup, an arrow to a second stickman; tiny comma-shaped doodles travel along the arrows. No words."),
  ch('c09b', C(.5, .5, 1.1), "A single Victorian stickman fills a tin cup from a street water pump and is about to drink, unaware; murky water."))
N('L04', "Once inside, he makes a toxin that turns your gut into a pump. It pulls water out of the body and flushes it away. A patient can lose up to twenty litres of fluid in a single day.",
  sh('c10a', W(), "A cartoon cutaway diagram on aged paper: a simple stylised gut drawn like a pipe with a little hand-pump attached, water being pumped out of it. Not gross, symbolic. No words."),
  sh('c10b', C(.5, .5, 1.1), "A row of twenty large glass water bottles lined up on a wooden floor, lit by a candle. Symbolic, still life.", text=ink('20 L', 1500, 220, 120)))
K('L05', "Twenty litres. I do not do things by halves.",
  kg('c11a', C(.5, .45, 1.1), "King Cholera holds up his tin cup triumphantly like a trophy, water splashing from it, grinning."))
N('L06', "People could be healthy at breakfast and dead by dinner. Their skin turned grey-blue and wrinkled from losing so much water. The Victorians had a name for it: the blue death.",
  ch('c12a', W(), "A Victorian breakfast table in the morning: one stickman in a waistcoat eats toast happily, a cup of tea and a jug of water beside him."),
  sh('c12b', W(), "The same Victorian breakfast table at night: the chair is empty and pushed back, the candle burnt low, the toast untouched. No people. Somber."),
  sh('c12c', C(.5, .5, 1.1), "An old Victorian broadsheet poster on a brick wall with a drawing of a pale blue shadowy figure. Leave the poster without words.", text=ink('THE BLUE DEATH', 960, 300, 92)))
N('L07', "Untreated, the worst cases killed around half of their victims. Today, with treatment, fewer than one in a hundred die. Hold that thought.",
  kg('c13a', C(.5, .45, 1.1), "King Cholera holds up a small set of brass weighing scales, smirking, one hand on his belly."),
  sh('c13b', C(.5, .5, 1.05), "A glass of clean water and a small paper sachet on a simple wooden table, morning light. Calm, hopeful."))

# ---- origin
N('L08', "But where did he come from? His home is the brackish water where rivers meet the sea, especially the great delta of the Ganges, in what is now India and Bangladesh. There, Vibrio bacteria live quietly on the shells of tiny crustaceans called copepods.",
  sh('c14a', WL(), "The vast Ganges delta seen from above at sunrise: winding brackish channels, mangrove forests of the Sundarbans, mist, wooden fishing boats. Muted colours."),
  sh('c14b', W(), "An old parchment map of the Bay of Bengal and the Ganges delta drawn in ink with the river mouths highlighted. No words."),
  sh('c14c', C(.5, .5, 1.1), "Underwater cartoon close-up: a tiny shrimp-like copepod with one red eye drifting in green brackish water; little comma-shaped bacteria cling to its shell like passengers on a bus. Cute."))
K('L09', "Meet Pod. Pod is family.",
  kg('c15a', C(.5, .45, 1.1), "King Cholera lifts the little glass jar from his watch chain to his face and gazes lovingly at the tiny copepod inside; the copepod waves a feeler."))
N('L10', "And here's the twist. Most Vibrio cholerae are pretty harmless. The killer kind got its weapon from a virus. A virus that infects bacteria slipped into one of them and carried in the genes for the cholera toxin. So the deadliest diarrhoea in history is, basically, a bacterium that caught a virus.",
  sh('c16a', W(), "A cartoon on aged paper: a crowd of plain, harmless comma-shaped bacteria with sleepy friendly faces floating in water. No words."),
  sh('c16b', C(.5, .5, 1.1), "Cartoon: a tiny spidery bacteriophage virus, drawn like a lunar lander with a geometric head and thin legs, landing on a comma-shaped bacterium and injecting a glowing strand of DNA. Clear, simple, not scary."),
  sh('c16c', W(), "Cartoon: the same comma-shaped bacterium now glowing pale green, wearing a tiny tin crown, sinister grin. No words."))
K('L11', "We don't talk about how I got my powers. It's a sensitive subject.",
  kg('c17a', C(.5, .45, 1.1), "King Cholera turns his face away and holds up one palm to the viewer, refusing to talk, offended, dripping."))
N('L12', "Nobody knows exactly when that happened. Ancient texts from India may describe a cholera-like illness, and Portuguese visitors in the 1500s wrote about a disease that could kill a man within hours. But for centuries, he mostly stayed home, in Bengal.",
  sh('c18a', W(), "An ancient palm-leaf manuscript bundle and an old Portuguese leather-bound journal side by side on a wooden table, candle light. No readable words."),
  sh('c18b', WL(), "A riverside town in old Bengal: bathing steps down to a wide river, boats, temple domes, palm trees, morning haze. No people close up."))

# ---- 1817
N('L13', "Then, in 1817, everything changed. An outbreak started near the town of Jessore, in Bengal, and this time, it didn't stay put.",
  sh('c19a', W(), "A small Bengal town in 1817 by a river, thatched houses, palm trees, monsoon clouds; ominous green-grey mist rising from the water.", text=cap('JESSORE, BENGAL · 1817')))
N('L14', "The world was more connected than ever. Ships, armies and traders moved along the routes of the British Empire, and he rode along with them. Within a few years he reached Southeast Asia, China, Japan, the Persian Gulf and East Africa.",
  sh('c20a', W(), "A busy 1810s harbour with tall East India Company sailing ships, cargo crates and bales on the docks, morning light. People only as tiny distant figures."),
  ch('c20b', W(), "A column of three stickman soldiers in red coats with muskets on their shoulders marches along a dusty road, spaced apart."),
  sh('c20c', WL(), "An old world map drawn in ink on parchment with dotted lines spreading out from Bengal across Asia to China and Japan, west to the Persian Gulf and down to East Africa. No words."))
K('L15', "I'd been waiting centuries for decent transport.",
  kg('c21a', W(), "King Cholera sits on a crate on the deck of an East India Company sailing ship at sea, legs crossed, sipping from his tin cup like a passenger enjoying a cruise."))
N('L16', "That was the first cholera pandemic. There would be seven.",
  sh('c22a', STILL, "Seven empty wooden picture frames hanging in a row on a dark wood-panelled wall, the first one slightly lit by a candle. No pictures in them.",
     text=[ink('I', 260, 540, 90)]))

# ---- 1830s: west
N('L17', "The second one went west. Through Russia in 1830, and into Europe. In October 1831 he landed in the English port of Sunderland. Months later he was in London and Paris, and then across the Atlantic, in Quebec and New York.",
  sh('c23a', WL(), "An old parchment map of Europe drawn in ink with a dark stain spreading from Russia westward across the continent. No words.", text=ink('1830', 1650, 200, 110)),
  sh('c23b', W(), "The English port of Sunderland in 1831: a grey North Sea harbour, coal ships, brick warehouses, overcast sky.", text=cap('SUNDERLAND · OCTOBER 1831')),
  sh('c23c', W(), "New York harbour in 1832: sailing ships, the low skyline of brick buildings and church spires, choppy water, grey sky.", text=cap('NEW YORK · 1832')))
N('L18', "In Paris, around eighteen thousand people died in just a few months. In New York, so many people fled the city that whole streets went quiet.",
  sh('c24a', W(), "Paris in 1832: the river Seine, Notre-Dame in the mist, empty bridges, grey dawn. People only as tiny distant figures."),
  sh('c24b', WL(), "An empty New York street in 1832: brick houses with closed shutters, a lone cart, scattered papers blowing. No people."),
  ch('c24c', W(), "A horse-drawn cart piled with trunks and furniture leaves the city along a country road, a stickman family of three walking beside it."))
N('L19', "And people were terrified in a very specific way. In Britain and Russia, crowds rioted, convinced that doctors were poisoning the poor, or that hospitals were collecting bodies for dissection.",
  ch('c25a', W(), "Three angry stickmen with torches and clubs stand in front of the closed iron gate of a Victorian hospital at night, shouting, spaced apart."),
  ch('c25b', C(.5, .5, 1.1), "A nervous stickman doctor with a black bag hides behind a door, peeking out, sweating."))
K('L20', "I let them argue. It saves me time.",
  kg('c26a', C(.5, .45, 1.1), "King Cholera leans against a lamppost at night, arms folded, watching distant torchlight with an amused grin."))

N('L20b', "And he didn't care who you were. Former US president James K. Polk died of cholera in 1849, just three months after leaving office. The composer Tchaikovsky, officially, died of cholera in 1893, after drinking a glass of unboiled water.",
  ch('c26b', W(), "A stickman gentleman with grey hair in an 1840s black suit and cravat stands on the porch of a white Southern mansion with columns, a little tired.", text=cap('JAMES K. POLK · 1849')),
  sh('c26c', C(.5, .5, 1.1), "A grand piano in a dark 1890s St Petersburg drawing room, sheet music on the stand, a single glass of water on the piano lid, candle light. No people.", text=cap('ST PETERSBURG · 1893')))
K('L20c', "Presidents. Composers. I'm not picky.",
  kg('c26d', C(.5, .45, 1.1), "King Cholera conducts an invisible orchestra with his tin cup like a baton, eyes closed, blissful, water flying off his sleeves."))

# ---- miasma
N('L21', "So what did the experts think caused it? Bad air. The miasma theory said disease came from foul smells rising from rotting rubbish and filth.",
  ch('c27a', W(), "A Victorian lecture room: one stickman professor in a frock coat points with a cane at a big drawing of a green stinking cloud on a blackboard. No words on the board."),
  sh('c27b', C(.5, .5, 1.1), "Cartoon: a pile of rotting rubbish in a Victorian alley with a wavy green smell rising from it, drawn as a ghostly cloud with a mean face.", text=stamp('MIASMA', x=1400, y=230)))
N('L22', "To be fair, Victorian London really did stink. Sewage ran into cesspits, and straight into the Thames. The same river that much of the city drank from.",
  sh('c28a', WL(), "The river Thames in the 1850s: brown murky water, sewage outflow pipes pouring into it, old wooden wharves, factory chimneys, the dome of St Paul's in smog."),
  ch('c28b', C(.5, .5, 1.1), "A single stickman water seller fills buckets straight from the murky Thames at a wooden jetty, a sewage pipe pouring in just upstream."))
K('L23', "They blamed the smell. The smell! I am offended on a personal level.",
  kg('c29a', C(.5, .45, 1.1), "King Cholera, outraged, points at a stinking pile of rubbish in an alley and then at himself, as if to say 'that's not me'."))
N('L24', "So cities scrubbed, burned tar and fumigated. None of it touched him. Because he wasn't in the air. He was in the cup.",
  ch('c30a', W(), "A Victorian street with a barrel of burning tar sending up thick black smoke; one stickman sweeps the cobbles with a broom, another sprinkles lime from a bucket, apart from each other."),
  sh('c30b', C(.5, .55, 1.25), "Close-up of a dented tin cup full of cloudy water on a wooden windowsill, gas light. Ominous still life."))

# ---- John Snow
N('L25', "Enter John Snow. A London doctor, famous for something else entirely. He was one of the first experts in anaesthesia, and he gave chloroform to Queen Victoria when she gave birth.",
  ch('c31a', C(.5, .45, 1.05), "Portrait shot: a stickman Victorian doctor with neat dark side-whiskers drawn as simple lines, a dark frock coat and cravat, standing calmly in his study with books and a small glass inhaler on the desk."),
  sh('c31b', W(), "A small brown glass bottle of chloroform and a folded cloth on an elegant palace side table, a royal crest on the wallpaper. No people.", text=cap('JOHN SNOW · 1813–1858')))
N('L26', "Snow didn't buy the bad-air idea. Cholera hit the gut, not the lungs, so he suspected people were swallowing it. In 1849 he published his theory. Almost nobody listened.",
  ch('c32a', W(), "The stickman doctor John Snow writes at his desk by lamp light, a stack of papers, a glass of water beside him that he eyes suspiciously."),
  ch('c32b', W(), "A Victorian meeting room: three stickman gentlemen in top hats sit with arms folded, unimpressed, one yawning, while a thin pamphlet lies ignored on the table."))
N('L27', "Then came Broad Street. Snow went door to door, marked every death on a map, and noticed they clustered around one public water pump.",
  ch('c33a', W(), "The stickman doctor John Snow knocks on a door in a narrow Soho street, holding a notebook, foggy daylight."),
  sh('c33b', STILL, "A hand-drawn street map of Soho on aged paper, the streets drawn as clean lines, with many small black bars stacked along the houses clustered around one pump symbol in the middle. No words.",
     text=[ink('THE PUMP', 960, 230, 70)]),
  sh('c33b', C(.5, .5, 1.5)))
N('L28', "The exceptions told the same story. Workers at a nearby brewery mostly drank beer, and stayed healthy. A workhouse down the street had its own well, and very few there died. And a widow who lived miles away, but liked the taste of the Broad Street water and had it delivered, died.",
  ch('c34a', W(), "A Victorian brewery yard: two cheerful stickman brewery workers in aprons raise tankards of beer, wooden barrels stacked behind them."),
  sh('c34b', W(), "A grim Victorian workhouse building with its own small private well in the courtyard, a bucket on the rim. No people."),
  ch('c34c', W(), "A stickman delivery boy carries a big stoneware jug of water up the path to a pretty house on a green hill outside London."))
K('L29', "She had excellent taste. In water, anyway.",
  kg('c35a', C(.5, .45, 1.1), "King Cholera raises his tin cup in a toast with a wicked grin, as if at a wine tasting, pinky finger out."))
N('L30', "On the seventh of September, Snow showed his evidence to the local officials. The next day, they removed the handle from the pump.",
  ch('c36a', W(), "A Victorian parish meeting room: the stickman doctor John Snow stands at a table spreading out his map in front of three seated stickman officials who lean in."),
  ch('c36b', C(.5, .5, 1.1), "A stickman workman in a cap unscrews and lifts the iron handle off a cast-iron public water pump in a foggy Soho street; the stickman doctor watches from a few steps away.", text=cap('8 SEPTEMBER 1854')))
K('L31', "My pump. My beautiful pump.",
  kg('c37a', C(.5, .45, 1.1), "King Cholera hugs the handle-less cast-iron water pump in the fog, weeping theatrically, water streaming off his hat."))
N('L32', "The outbreak was already fading by then, and the officials soon went back to blaming the air. Later, a local priest found the likely source: a baby's dirty nappies, washed into a cesspit just a few feet from the well.",
  ch('c38a', W(), "A Victorian vicar stickman in black clerical clothes and a white collar walks down Broad Street holding a notebook, thinking."),
  sh('c38b', W(), "Cutaway diagram on aged paper: a brick cesspit under a house cellar, a cracked wall, dirty water seeping through the soil into the shaft of a public well a few feet away. No words."))
N('L33', "Snow died in 1858, before most people accepted that he was right.",
  sh('c39a', C(.5, .5, 1.05), "A simple Victorian gravestone in a quiet London cemetery under a tree, autumn leaves, soft light. Leave the stone blank."))

# ---- Great Stink & sewers
N('L34', "That same summer, the Thames smelled so bad that Parliament could barely work. The papers called it the Great Stink.",
  sh('c40a', WL(), "The Houses of Parliament on the Thames in the hot summer of 1858, wavy green stench lines rising from the brown river, hazy sun.", text=stamp('THE GREAT STINK', x=1380, y=230, size=84)),
  ch('c40b', C(.5, .5, 1.1), "Inside Parliament: two stickman politicians in frock coats hold handkerchiefs over their noses, the windows hung with soaked curtains."))
N('L35', "Finally, the government paid for a huge new sewer system, designed by the engineer Joseph Bazalgette. Over a thousand miles of sewers, carrying London's waste away, downstream.",
  ch('c41a', W(), "A Victorian engineer stickman with big side-whiskers drawn as simple lines and a top hat studies huge blueprints of tunnels spread on a table."),
  sh('c41b', WL(), "A vast brick sewer tunnel under construction in the 1860s, a long curved brick vault receding into darkness, scaffolding, lanterns. People only as tiny distant figures."),
  sh('c41c', W(), "A grand Victorian pumping station interior with ornate painted cast-iron columns and huge beam engines. No people."))
N('L36', "And here's the irony. They built it to get rid of the smell. But by keeping sewage out of the drinking water, it did what all the fumigating never could. It cut him off.",
  sh('c42a', C(.5, .5, 1.1), "Cutaway diagram on aged paper: a clean water pipe running to a house tap on top, and below it a separate big sewer pipe carrying waste away, clearly apart. No words."))
K('L37', "Defeated by plumbing. Do you know how humiliating that is?",
  kg('c43a', W(), "King Cholera sits dejected on the edge of a brick sewer outlet, chin in his hand, his crown slipping sideways, a small puddle around him."))

# ---- germs
N('L38', "Across Europe, scientists were hunting for the actual culprit. In 1854, the same year as Broad Street, an Italian, Filippo Pacini, saw comma-shaped bacteria in the guts of cholera victims in Florence. Hardly anyone noticed.",
  ch('c44a', W(), "A stickman Italian scientist with round spectacles peers into a brass microscope in a sunlit study in Florence, the red cathedral dome visible through the window.", text=cap('FLORENCE · 1854')))
N('L39', "Thirty years later, the German scientist Robert Koch found them again, in Egypt and then in Calcutta. And this time, the world paid attention.",
  ch('c45a', W(), "A stickman German scientist with small round glasses and a white coat holds up a glass test tube in a bright 1880s laboratory, triumphant.", text=cap('CALCUTTA · 1884')),
  sh('c45b', C(.5, .5, 1.1), "An 1880s scientific drawing on paper of curved comma-shaped bacteria seen through a microscope, neat ink. No words."))
N('L40', "Not everyone was convinced. In 1892, an old-school professor, Max von Pettenkofer, asked for a flask of live cholera bacteria, and drank it. To prove they were harmless.",
  ch('c46a', C(.5, .45, 1.1), "An elderly stickman professor with a big bushy grey moustache drawn as simple lines, in a frock coat, raises a small glass flask of cloudy liquid to drink it, confident."))
K('L41', "I respect the confidence.",
  kg('c47a', C(.5, .45, 1.1), "King Cholera slowly applauds with his two hands, impressed, eyebrows raised, a grin spreading across his face."))
N('L42', "He got a nasty case of diarrhoea, and survived. Nobody is quite sure why. He was lucky. Others weren't.",
  ch('c48a', W(), "The elderly stickman professor with a bushy moustache sits pale in an armchair wrapped in a blanket, clutching his stomach, a hot water bottle on his lap."))
N('L43', "That same year, Hamburg was drinking unfiltered water from the river Elbe, and about eight and a half thousand people died. Next door, the town of Altona filtered its water. It was barely touched.",
  sh('c49a', W(), "The port of Hamburg in 1892: warehouses, ships on the river Elbe, church spires, grey sky.", text=cap('HAMBURG · 1892')),
  sh('c49b', W(), "Cutaway diagram on aged paper of a Victorian sand-filter bed: layers of sand and gravel, murky water on top, clean water coming out below. No words."))

N('L43b', "He also changed how countries work together. In 1851, European states met in Paris for the first International Sanitary Conference, mostly because of him. It was the start of international cooperation on health that, a century later, led to the World Health Organization.",
  ch('c49c', W(), "A grand 1851 Paris conference hall with chandeliers: three stickman diplomats in different national uniforms sit apart around a long table with a big map of Europe and Asia.", text=cap('PARIS · 1851')))
K('L43c', "I brought the nations together. You're welcome.",
  kg('c49d', C(.5, .45, 1.1), "King Cholera takes a deep theatrical bow, sweeping off his crowned top hat, water splashing on the parquet floor of a grand hall."))

# ---- the cure
N('L44', "Clean water stopped him from spreading. But for the people already sick, the problem was simple. The body was running dry.",
  sh('c50a', C(.5, .5, 1.1), "A cracked dry riverbed under a hot sun, a single small puddle left. Symbolic."))
N('L45', "In the 1960s, researchers in Dhaka and Calcutta tested a treatment so simple it sounds like a joke. Clean water, a little salt and a little sugar, in the right amounts. Oral rehydration solution.",
  ch('c51a', W(), "A 1960s research hospital ward in Dhaka: one stickman doctor in a white coat measures salt and sugar with a small spoon into a jug of clean water on a table."),
  sh('c51b', STILL, "Three simple things on a clean wooden table, side by side with space between them: a glass jug of clean water, a small bowl of salt, a small bowl of sugar. Bright, hopeful.",
     text=[ink('WATER', 480, 880, 60), ink('SALT', 960, 880, 60, at=.8), ink('SUGAR', 1440, 880, 60, at=1.3)]))
N('L46', "In 1971, during Bangladesh's war of independence, cholera swept through the refugee camps. A doctor named Dilip Mahalanabis ran out of IV drips, and gave out this drink instead. In other camps, around thirty percent of cholera patients died. In his, under four percent.",
  sh('c52a', WL(), "A large refugee camp in 1971 under monsoon clouds, rows of tents and makeshift shelters, mud paths. People only as tiny distant figures."),
  ch('c52b', W(), "A stickman doctor in a white coat hands a cup of drink to a stickman patient sitting up on a simple camp bed; big drums of water and sacks behind them."),
  sh('c52c', STILL, "A simple hand-drawn bar chart on aged paper: one tall dark bar on the left, one very short bar on the right. No words.",
     text=[ink('30%', 640, 230, 80), ink('<4%', 1290, 640, 80, at=.8)]))
N('L47', "The medical journal The Lancet later called it potentially the most important medical advance of the twentieth century.",
  sh('c53a', C(.5, .5, 1.05), "An old printed medical journal lying open on a desk next to a glass of water, a pair of reading glasses on top. No readable words."))
K('L48', "Salt. Sugar. Water. That's it?",
  kg('c54a', C(.5, .45, 1.1), "King Cholera stares in disbelief at a small glass of rehydration drink on a table in front of him, his crown tilted, mouth open."))
N('L49', "That's it. Today there are also cholera vaccines, and antibiotics for severe cases.",
  sh('c55a', C(.5, .5, 1.05), "A small vaccine vial and a strip of pills beside a glass of water on a clean clinic table. Simple, clean."))

# ---- today
N('L50', "So, is he gone? Not even close. The seventh pandemic began in Indonesia in 1961, and it has never officially ended.",
  sh('c22a', STILL, text=[ink('I', 260, 540, 90, at=0), ink('VII', 1660, 540, 90, at=.4)]),
  sh('c56a', W(), "A tropical harbour in Sulawesi, Indonesia, 1961: wooden boats, stilt houses over the water, palm trees. People only as tiny distant figures.", text=cap('SULAWESI · 1961')))
N('L51', "In 2010, after a huge earthquake, cholera reached Haiti, carried in by United Nations peacekeepers, and killed nearly ten thousand people. In Yemen, during the war, there were more than two and a half million suspected cases.",
  sh('c57a', W(), "Port-au-Prince in 2010 after the earthquake: damaged buildings, tents, hills behind, dusty light. People only as tiny distant figures.", text=cap('HAITI · 2010')),
  sh('c57b', W(), "An old town in Yemen with tall mud-brick tower houses decorated with white trim, dusty sky, a water tanker truck in the street. No people close up.", text=cap('YEMEN · 2016–2021')))
N('L52', "Today he still infects millions of people every year, and kills tens of thousands. Almost always in places without clean water.",
  ch('c58a', W(), "A stickman girl carries a yellow plastic jerrycan of water along a dusty path toward a village, a muddy pond in the background."))
K('L53', "I don't need an empire. I just need one dirty well.",
  kg('c59a', W(), "King Cholera sits on the rim of an old stone well at dusk, swinging his legs, tipping his top hat with the crown to the viewer, smiling slyly."))
N('L54', "Two hundred years. Seven pandemics. A killer that emptied whole neighbourhoods, beaten not by a miracle drug, but by pipes, filters, and a spoonful of salt and sugar.",
  sh('c01a', W()), sh('c23a', W()), sh('c41b', W()), sh('c51b', W()), sh('c43a', C(.5, .5, 1.15)))
N('L55', "Next time: a killer that left its mark on the faces of emperors, and was beaten so completely it no longer exists in the wild.",
  sh('c60a', C(.5, .5, 1.05), "A dark palace corridor at night: the silhouette of a tall figure in a powdered 18th-century wig and long coat stands at the far end in shadow; a single candle; a portrait of a cow hangs on the wall. Ominous."))
HOLD(5.0, sh('c60a', O(), text=[label('NEXT TIME', 1380, 360, 110, style='title', pop=True, at=.2, len=4.6), label('SUBSCRIBE', 1380, 500, 64, at=.8, len=4.0)]))

def lines():
    for i, r, t, _ in B:
        if i: print(f"{i}|{r}|{t}")

def frames():
    seen, out = set(), []
    for _, _, _, shots in B:
        for s in shots:
            if 'prompt' in s and s['img'] not in seen:
                seen.add(s['img']); refs = []
                if 'K' in s['refs']: refs.append(K_SHEET)
                if 'S' in s['refs']: refs.append(S_SHEET)
                out.append({'img': s['img'], 'prompt': STYLE + ' ' + s['prompt'], 'refs': refs})
    json.dump(out, open(os.path.join(ROOT, 'tools/plague/ep02_frames_todo.json'), 'w'), indent=1); print(len(out), 'frames')

def beats():
    out = {'base': 'assets/plague/ep02/frames', 'fade_in': .8, 'start': 0.0, 'lead': .45, 'gap': .6, 'max_shot': 3.2,
           'sfx_global': [{'kind': 'drone', 'args': {'d': 'ALL'}, 'gain': .9}, {'kind': 'wind', 'args': {'d': 'ALL'}, 'gain': .1}], 'beats': []}
    for i, r, t, shots in B:
        sl = []
        for s in shots:
            d = {'img': s['img'], 'from': s['cam'][0], 'to': s['cam'][1], 'w': s['w']}
            if 'text' in s: d['text'] = s['text']
            if 'sfx' in s: d['sfx'] = s['sfx']
            sl.append(d)
        if i: out['beats'].append({'vo': f'assets/plague/ep02/vo/{i}.wav', **({'gain': 1.05} if r == 'CHOLERA' else {}), 'shots': sl})
        else: out['beats'].append({'hold': t, 'shots': sl})
    json.dump(out, open(os.path.join(ROOT, 'tools/plague/ep02_beats.json'), 'w'), indent=1); print(len(out['beats']), 'beats')

{'lines': lines, 'frames': frames, 'beats': beats}[sys.argv[1]]()
