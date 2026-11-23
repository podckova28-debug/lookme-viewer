"""Plague ep01 v3: new frames (replacements for mutated / stock-cast / empty frames, plus frames for the new lines).
python3 tools/plague/ep01v3_frames.py -> tools/plague/pending/ep01v3/s0X.json + manifest.json"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = '80552411-22ff-414f-8f40-9af41f66ebff'
STYLE = ("2D animated history explainer frame, 16:9, no text. Hand-drawn ink illustration, clean black outlines, fine cross-hatching, "
         "muted grey-sepia palette with warm light from fire, candles and lanterns. Not gory.")
MODERN = ("2D animated history explainer frame, 16:9, no text. Hand-drawn ink illustration, clean black outlines, muted sepia palette, soft natural daylight. "
          "The setting is modern: nothing old-fashioned. Not gory.")
SN = ("Humans are simple STICKMEN: plain white round head, two dot eyes, simple mouth, no nose, no beard, thin black stick arms and stick legs, "
      "small solid BLACK mitten hands with no fingers; never white hands, never gloves, never skin-coloured or thick human arms. "
      "Dressed exactly as described for this scene and era, nobody else: no kings, no crowns, no popes, no emperors, no professors unless described. "
      "Only the few figures described, standing apart, never overlapping; each has exactly two arms and two hands; "
      "hands are empty unless an object is described; no flags, no banners; no readable text.")
PL = ("The Plague exactly as on the attached sheet: tall thin figure, tattered black-brown hooded cloak, shadowed grey face, small glowing white eyes, "
      "hooked grey nose, thin cruel smile, grey spotted bony hands, bronze clasp, red-eyed black rat on his shoulder. Exactly ONE of him, exactly two arms and two hands.")
DIAG = ("Draw ONLY the diagram described below, filling the whole frame, as ONE single picture: no extra panels. "
        "A hand-drawn explainer diagram in ink and muted watercolour on aged parchment, clean like an old textbook plate, "
        "numbered stages as small circled digits with drawn arrows. No words, no letters, no numbers except circled digits. Not gory, cartoon-simple. ")
STICKD = "Any human figure is a plain stickman outline with a round head, dot eyes and black stick limbs. "
F = {}
def ch(n, p, modern=False): F[n] = ((MODERN if modern else STYLE) + ' ' + SN + ' ' + p, [])
def pl(n, p, people=''): F[n] = (STYLE + ' ' + PL + ' ' + (SN + ' ' + people if people else 'No other people.') + ' ' + p, [P])
def dg(n, p, people=False): F[n] = (STYLE + ' ' + (STICKD if people else '') + DIAG + p + ('' if people else ' No people.'), [])

# ---- replacements: mutated hands / stock cast / crowds
ch('g11a', "A modern archaeological dig on a grassy hillside in daylight: one stickman archaeologist in a khaki shirt and a wide sun hat kneels in a shallow trench, brushing earth off an ancient skull with a small brush held in one black mitten hand.", True)
ch('g11b', "A bright modern laboratory: one stickman scientist in a white lab coat and safety glasses (eyes inside the lenses) holds up an old tooth with tweezers in one black mitten hand under a lamp, a DNA sequencer machine beside her.", True)
ch('g15a', "A Byzantine palace hall in 540 AD with gold mosaics: the emperor Justinian, a stickman in a long purple robe and a jewelled gold crown, stands at a big map table and points with one black mitten hand at a map of the Mediterranean; a stickman general in Roman-style armour and helmet stands apart, holding his helmet under one arm.")
ch('g17a', "A Byzantine palace bedchamber in 542 AD lit by oil lamps: the emperor, a stickman in a purple nightshirt with a small gold crown on the bedside table, lies sick in a large bed, sweating, with a visible swollen red lump on his neck; a stickman physician in a long grey robe stands apart holding a small cup.")
ch('g18a', "A Byzantine palace hall at dusk: the emperor, a stickman in a long purple robe and jewelled crown, sits alone at a map table with his round head resting on one black mitten hand, looking glum; on the map, little toy soldiers have fallen over.")
pl('g21b', "The Silk Road at sunset in the 1340s: a small caravan of camels crosses a desert, two stickman merchants in Central Asian robes and turbans walk apart beside the camels leading them by ropes; the Plague rides the last camel with his battered suitcase, smiling.", "Two stickman merchants.")
ch('g30a', "The University of Paris in 1348, a stone hall: three stickman physicians in long red and black academic robes and round caps stand apart; one points with a long stick at a big astrological chart showing three planets lined up, the other two nod seriously.")
pl('g31a', "A stone university hall in Paris: the Plague stands in an open doorway pointing at himself with one bony finger, offended, while three stickman physicians in red and black academic robes and round caps stand apart by a chart of planets, mouths open in surprise.", "Three stickman physicians.")
ch('g32b', "A medieval street at night: a stickman priest in a black cassock swings a smoking brass censer on a chain held in one black mitten hand; two stickman townspeople in plain tunics stand apart, each holding a little bunch of herbs to their face.")
ch('g35b', "The deck of a 1377 merchant sailing ship anchored in a calm bay outside a walled stone port: three stickman sailors in medieval tunics and caps sit apart on the deck waiting, bored; one scratches a tally mark on the mast with a knife held in one black mitten hand.")
ch('g36b', "A Venetian office in the 1400s with arched windows over a canal: a stickman official in a long red robe and a red cap sits at a desk, writing with a quill held in one black mitten hand in a big ledger, his other hand resting on the page; rows of tally marks on the wall behind.")
ch('g39a', "A wide wheat field after the Black Death: only two stickman peasants in plain tunics and straw hats reap with sickles held in one black mitten hand each, far apart from each other, with acres of uncut golden wheat around them and an empty farmhouse in the distance.")
ch('g39c', "A medieval manor courtyard: a stickman peasant in a patched tunic stands confidently with one black mitten hand held out, palm up, asking for more coins; a stickman lord in a fur-trimmed red robe stands apart frowning with his arms crossed, a small purse on the table beside him.")
ch('g41a', "England, 1381: five stickman peasants in tunics and hoods march apart along a muddy road toward a walled medieval city with a big stone gate, each holding one pitchfork, scythe or club in one black mitten hand; their faces are angry and determined.")
pl('g42b', "A medieval town square at dusk: the Plague stands alone in the middle with his arms spread as if expecting applause; three stickman townspeople in plain 1380s tunics and hoods stand far apart, staring at him with their arms crossed and frowns.", "Three stickman townspeople.")
ch('g44a', "A narrow London street in 1665 at dusk: wooden doors painted with large red crosses, a stickman watchman in a long coat and a hat stands guard outside one door holding a tall halberd in one black mitten hand; a covered cart waits further down the empty street.")
pl('g46a', "An English farm in 1666: a young stickman Isaac Newton with long curly hair in a dark 1660s coat sits under an apple tree reading a book held in both black mitten hands; the Plague lounges on a branch above him, dropping a single apple toward his head with a sly grin.", "One stickman Isaac Newton.")
ch('g46d', "A tailor's workshop in the English village of Eyam in 1665: a stickman tailor in a shirt and waistcoat unwraps a bundle of cloth from London on his workbench with both black mitten hands; a few tiny fleas jump out of the cloth. Scissors and thread on the bench.")
ch('g46e', "A green rocky dell outside the village of Eyam in 1666: the rector, a stickman in a black cassock with a white collar, stands on a rock speaking with one black mitten hand raised; five stickman villagers in plain 1660s rustic clothes, caps and bonnets sit apart from each other on the grass listening.")
ch('g46f', "The edge of the village of Eyam in 1666: a large boundary stone with holes filled with vinegar and a few coins in them; on the far side, one stickman man from the neighbouring village in a 1660s coat sets down a basket of bread on the ground and steps back, keeping his distance.")
# ---- replacements: empty frames -> information
ch('g10b', "A medieval sickroom lit by a candle: a stickman man in a nightshirt lies in bed, sweating and shivering under a blanket, with a visible swollen red lump on his neck; his stickman wife in a long dress and headscarf sits apart on a stool holding a cup of water.")
ch('g17b', "Constantinople in 542 AD, a stone street at dawn: two stickman gravediggers in plain tunics carry a stretcher with a figure covered by a white sheet, while a third stickman in a tunic leans on a shovel beside a long row of white shrouded shapes. Not gory.")
dg('g19a', "A simple map of the Mediterranean Sea with small port-city dots; around many ports, concentric red rings ripple outward again and again like waves, with small circled digits 1, 2, 3 beside three of the rings to show repeated waves.")
ch('g28a', "A medieval churchyard in 1348: two stickman gravediggers in plain tunics dig a long wide pit with shovels held in both black mitten hands, while a stickman priest in a black robe stands apart at the edge holding a small book; rows of white shrouded shapes wait beside the pit. Not gory.")
ch('g28b', "A medieval stone bell tower at dusk with a big bronze bell hanging still and silent; one stickman priest in a black robe stands below looking up at it sadly, holding the loose bell rope in one black mitten hand.")
ch('g28d', "A medieval churchyard at dusk crowded with many fresh earth graves and simple wooden crosses; one stickman woman in a long dark dress and headscarf stands alone among them with her head bowed.")
dg('g43a', "ONLY one long horizontal timeline drawn as a thin ink line across the whole page: one huge tall hump on the left, followed by many smaller humps of different heights repeating all the way to the right edge. No numbers.")
pl('g27a', "A Florentine family home in 1348, morning light: three stickmen in 14th-century Italian clothes, a father, a mother and a child, eat breakfast at a wooden table with bread and bowls, sitting apart; through the open window behind them, the Plague peeks in, grinning.", "Three stickman family members.")
# ---- new lines
dg('g_s01', "A simple standing stickman outline with four numbered magnifier circles: (1) a thermometer at very high, (2) wavy shiver lines around the body, (3) the head with pounding pain lines, (4) drooping weak arms; a small calendar beside showing a few days crossed off.", True)
ch('g_s01b', "A medieval cottage at night: a stickman man in a nightshirt sits up in bed wrapped in a blanket, shivering hard with sweat drops on his round head, holding his head with one black mitten hand; a candle on a stool.")
dg('g_s02', "A simple stickman body outline front view with three numbered circles marking the places where buboes appear: (1) the neck, (2) the armpit, (3) the groin; beside it one big magnifier circle showing a smooth round swollen lump the size of an egg drawn next to a small egg for comparison. Cartoon-simple, not gory.", True)
dg('g_s03', "Three numbered simple outline drawings in one row: (1) a hand whose fingertips are shaded dark grey, (2) a foot whose toes are shaded dark grey, (3) a simple face in profile with the tip of the nose shaded dark grey. Cartoon-simple, not gory.", True)
dg('g_s04', "Two simple stickman figures standing apart: the left one coughs out a small cloud of tiny dots (1), the cloud drifts to the right one (2), who then coughs his own cloud toward the edge of the page (3). A crossed-out rat icon above shows no rats needed.", True)
pl('g_sp', "A dim medieval scriptorium lit by candles: the Plague sits at a writing desk, signing a long parchment scroll with a grand flourish of a quill held in one bony hand, his other hand resting on the desk, smiling smugly.")
ch('g_t01', "Hong Kong in 1894: a simple straw-and-bamboo hut laboratory; a stickman scientist in a white tropical suit looks into a brass microscope with both black mitten hands on it; far apart at another bench in a different room seen through an open doorway, a second stickman scientist in a dark Western suit examines a glass slide.")
dg('g_t02', "ONLY one horizontal timeline across the page: a single wide hump rising on the left, a small steamship icon near its peak, and the line falling slowly back down to nothing at the right edge, where a small green tick is drawn. No numbers.")
dg('g_a01', "Three numbered simple outline panels in one row: (1) a neck with a small healed scar, (2) a hand missing one fingertip, (3) a foot missing one toe. Cartoon-simple, not gory.")
dg('g_a02', "Four numbered icons in one row: (1) a ship at anchor beside a small calendar, (2) a long sheet of paper with rows of tally marks, (3) a simple stone hospital building, (4) a group of three officials' hats around a table.")
ch('g_a02b', "A London parish office in 1665 lit by a candle: a stickman parish clerk in a dark coat and white collar sits at a desk writing a weekly list of the dead in a big ledger with a quill held in one black mitten hand; a pile of printed sheets beside him.")
pl('g_a03', "A modern harbour quarantine office with a big glass window: the Plague leans against the outside of the window, peering in with mock admiration, one bony hand on the glass and the other on his hip.")

def build():
    d = os.path.join(ROOT, 'tools/plague/pending/ep01v3'); os.makedirs(d, exist_ok=True)
    reqs, man = [], []
    for i, (n, (p, refs)) in enumerate(F.items()):
        par = {"model": "gpt_image_2_6", "aspect_ratio": "16:9", "prompt": p}
        if refs: par['medias'] = [{"role": "image_references", "value": r} for r in refs]
        reqs.append({"index": i, "params": par}); man.append({"index": i, "img": n, "out": f"assets/plague/ep01/frames/{n}.jpg"})
    for b in range(0, len(reqs), 8): json.dump(reqs[b:b+8], open(f'{d}/s{b//8:02d}.json', 'w'))
    json.dump(man, open(f'{d}/manifest.json', 'w'), indent=0)
    print(len(reqs), 'frames', (len(reqs)+7)//8, 'files')
build()
