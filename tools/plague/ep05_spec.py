"""Episode 5 (The ENTIRE History of Scurvy): single source of truth. Same format as ep04_spec.py.
Fast cutting, ~35 explainer diagrams, mild camera only. Origin = the broken GULO gene; symptoms shown on characters.

  python3 tools/plague/ep05_spec.py lines   -> voice list (id|ROLE|text), roles NARRATOR / SCURVY
  python3 tools/plague/ep05_spec.py frames  -> tools/plague/ep05_frames_todo.json
  python3 tools/plague/ep05_spec.py beats   -> tools/plague/ep05_beats.json (for beats.py)
"""
import sys, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
K_SHEET = '75832aec-491a-45f6-9047-f3877d22af70'   # channel/plague/sheets/cand_scurvy.jpg
S_SHEET = '84427fc9-09ce-40e6-b032-6f2700874458'   # channel/plague/sheets/stickmen_common.jpg
STYLE = ("2D animated history explainer frame, 16:9, no text. Hand-drawn ink illustration, clean black outlines, muted sea-blue, slate-grey and sepia palette "
         "with warm lantern amber light and small bright citrus-yellow accents. Not gory.")
STICK = ("Humans are simple STICKMEN in the style of the attached stickman sheet: plain white round head, two dot eyes, no nose, no beard, thin black stick arms and legs, "
         "simple 18th-century sailor clothes; anyone wearing glasses has his two dot eyes INSIDE the lenses and no other eyes (striped shirts, short jackets, kerchiefs, knitted caps; officers in tricorn hats). KEEP IT SIMPLE: only the few figures described, standing apart, "
         "never overlapping; each figure has exactly two arms and two hands, clearly attached to its own sleeves; nothing floating. No crowds, no ghost figures, no plague doctors.")
KING = ("Scurvy exactly as on the attached sheet: a gaunt, sinister 18th-century sea captain in a tattered navy-blue sea coat with tarnished gold buttons and frayed gold epaulettes, "
        "a battered tricorn hat, long stringy grey hair, pale yellowish skin with bruise-like purple patches, sunken eyes and a wide grin with swollen purple gums and gaps of missing teeth; "
        "he carries a ship's lantern and a rusty brass spyglass. Exactly ONE of him, with exactly two arms and two hands with normal-length fingers.")
DIAG = ("Draw ONLY the diagram described below, filling the whole frame: no extra rows, no extra panels, no comic strips above or below it. A hand-drawn explainer diagram in ink and muted watercolour on aged paper, "
        "clean and readable like an old textbook plate, simple stickman figures (plain white round head, dot eyes, stick limbs, each with exactly two arms) where people appear, "
        "numbered stages as small circled digits with drawn arrows. No words, no letters, only circled digits. Not gory. ")

def W(): return [[.5, .5, 1.0], [.5, .5, 1.04]]
def WL(): return [[.48, .5, 1.03], [.52, .5, 1.03]]
def WR(): return [[.52, .5, 1.03], [.48, .5, 1.03]]
def C(x, y, z=1.3): z = 1 + (z - 1) * .35; return [[x, y, z], [x, y, z + .02]]
def O(): return [[.5, .5, 1.05], [.5, .5, 1.0]]
STILL = [[.5, .5, 1.0], [.5, .5, 1.02]]

def sh(img, cam=None, prompt=None, refs='', text=None, sfx=None, w=1):
    s = {'img': img, 'cam': cam or W(), 'w': w}
    if prompt: s['prompt'] = prompt; s['refs'] = refs
    if text: s['text'] = text
    if sfx: s['sfx'] = sfx
    return s
def cap(t, **k): return {'text': t, 'x': 960, 'y': 985, 'size': 50, 'at': .3, **k}
def label(t, x, y, size=64, **k): return {'text': t, 'x': x, 'y': y, 'size': size, 'at': .3, **k}
def ch(img, cam, p, **k): return sh(img, cam, STICK + ' ' + p, 'S', **k)
def kg(img, cam, p, **k): return sh(img, cam, KING + ' ' + p, 'K', **k)
def ks(img, cam, p, **k): return sh(img, cam, STICK + ' ' + KING + ' Scurvy has his own gaunt face, NOT a stickman head, and wears his tricorn hat. ' + p, 'KS', **k)
def dg(img, p, people=True, **k): return sh(img, STILL, (STICK + ' ' if people else '') + DIAG + p, 'S' if people else '', **k)

B = []
def N(i, t, *s): B.append((i, 'NARRATOR', t, list(s)))
def K(i, t, *s): B.append((i, 'SCURVY', t, list(s)))
def HOLD(sec, *s): B.append((None, None, sec, list(s)))

# ---- cold open: Anson, 1740
N('C01', "September, 1740. Six British warships leave Portsmouth under Commodore George Anson, with nearly two thousand men aboard. Their mission: sail around South America and raid Spanish treasure ships.",
  sh('c01a', WL(), "An 18th-century English harbour at dawn: six tall wooden warships with furled sails at anchor, rowing boats ferrying barrels, gulls, a grey sky; the ships fly plain red ensigns (red flags with a small dark canton in the top corner), no Union Jacks. People only as tiny distant figures.", text=cap('PORTSMOUTH · SEPTEMBER 1740')),
  dg('d01a', "A sea chart of the Atlantic and South America with a dotted route from England down to the tip of South America, around Cape Horn and up the Pacific coast; six tiny ship icons on the route; a small treasure chest icon in the Pacific.", people=False, text=[cap('6 SHIPS  ·  NEARLY 2,000 MEN')]),
  ch('c01b', W(), "On the deck of an 18th-century warship: a stickman officer in a tricorn hat and blue coat stands at the rail with a telescope, a young stickman sailor coiling rope apart from him."))
N('C02', "Rounding Cape Horn, the men begin to fall ill. Their gums swell. Old wounds open up again. Men who were injured decades ago feel their long-healed bones come apart.",
  sh('c02a', WR(), "An 18th-century warship battling huge grey waves and sleet near Cape Horn, sails torn, dark storm clouds, rocky coast far away. People only as tiny distant figures."),
  ch('c02b', W(), "Below deck of an 18th-century warship by lantern light: two pale stickman sailors lie in separate canvas hammocks far apart, looking weak and miserable, a bucket on the floor."),
  ch('c02c', C(.5, .5, 1.05), "A ship's surgeon stickman in a dark coat holds a lantern up to look at an old stickman sailor sitting on a sea chest, who holds his own arm, worried."))
N('C03', "Almost four years later, Anson comes home with a fortune in Spanish silver. But well over a thousand of his men are dead. Only four were killed by the enemy.",
  sh('c03a', W(), "A single battered wooden warship with patched sails arriving in a calm English harbour in summer, chests of silver being lowered onto the quay. People only as tiny distant figures."),
  dg('d02a', "Two groups compared side by side: (1) on the left, just four tiny grave crosses beside a small cannon; (2) on the right, a huge field of many hundreds of tiny grave crosses beside a ship's lantern. No people.", people=False, text=[cap('KILLED BY THE ENEMY: 4  ·  DEAD OF DISEASE: OVER 1,000')]))
K('C04', "The Spanish took four. I took the rest.",
  kg('c04a', C(.5, .45, 1.1), "Medium shot: Scurvy stands on the dark deck of a sailing ship at night, holding up his lantern, grinning at the viewer with his gap-toothed smile."))
HOLD(4.6, kg('c05a', O(), "Title shot: Scurvy stands on the left third of the frame at the bow of a ghostly sailing ship in thick sea fog at night, lantern raised; dark empty fog over the sea on the right side.")
     | {'text': [label('SCURVY', 1300, 330, 140, style='title', pop=True, at=.15, len=4.2), label('THE SAILORS\' PLAGUE', 1300, 470, 72, style='title', color=[230, 200, 110], at=.5, len=3.9)],
        'sfx': [{'kind': 'boom', 'at': .1, 'gain': .8}]})

# ---- who is he
N('L01', "So who is he? Scurvy isn't a germ. You can't catch him from anyone. He's what happens when your body runs out of one thing: vitamin C.",
  dg('d03a', "Two panels: (1) a brass microscope with a big cross drawn over it, (2) a halved orange glowing softly, and next to it an empty dotted outline of the same orange half.", people=False, text=[cap('NOT A GERM  ·  A MISSING VITAMIN')]),
  sh('c06a', C(.5, .5, 1.05), "Still life on a ship's wooden table by lantern light: a hard ship's biscuit, a lump of salt beef, a tin mug of beer; in the shadow at the edge a single bright orange. No people."))
N('L02', "Your body uses vitamin C to make collagen, the glue that holds you together. It's in your skin, your gums, your blood vessels and your bones. And it's constantly being worn out and rebuilt.",
  dg('d04a', "A standing stickman with four magnifying circles drawn out from his body, each showing strong braided rope-like fibres: (1) in the skin, (2) in the gums, (3) in a blood vessel tube, (4) in a bone.", text=[cap('COLLAGEN: THE BODY\'S GLUE')]))
N('L03', "Without vitamin C, the rebuilding stops. Slowly, the glue gives way, and you start to come apart.",
  dg('d05a', "Two panels: (1) small orange droplets help a row of tiny fibres twist together into a strong braided rope, (2) without any droplets the same rope is fraying and unravelling into loose threads.", people=False, text=[cap('WITH VITAMIN C  ·  WITHOUT')]))
K('L04', "No germs. No fever. I simply take away the glue.",
  kg('c07a', C(.5, .45, 1.1), "In a dim ship's cabin, Scurvy slowly pulls a loose thread out of the frayed sleeve of an old sailor's jacket hanging on a hook, smiling to himself."))

# ---- origin
N('L05', "But where did he come from? Almost every animal makes its own vitamin C. Dogs, cats, goats, rats. They never get scurvy, whatever they eat.",
  dg('d06a', "A row of four animals: (1) a dog, (2) a cat, (3) a goat, (4) a rat; each has a tiny factory chimney drawn on its side puffing out small orange droplets. No people.", people=False, text=[cap('THEY MAKE THEIR OWN')]),
  sh('c08a', W(), "A ship's dog and a cat lying side by side on a coil of rope on a sunny deck, healthy and lazy, sea behind. No people."))
N('L06', "But about sixty million years ago, our early primate ancestors lost that ability. A single gene, the one that makes the last step of vitamin C, broke.",
  sh('c08b', WL(), "An ancient tropical forest canopy at sunrise, full of fruit trees heavy with figs and berries, mist in the valleys. No people. A small primate sits on a branch eating fruit."),
  dg('d07a', "A long DNA strand drawn as a twisted ladder; one section of it is cracked and broken with a small jagged gap; beside it a little gear-shaped factory whose chimney has stopped smoking. No people.", people=False, text=[cap('ONE BROKEN GENE  ·  ABOUT 60 MILLION YEARS AGO')]))
N('L07', "They lived in forests full of fruit, so it didn't matter. The broken gene was passed down to monkeys, to apes, and to us. Guinea pigs and some bats lost it too.",
  dg('d08a', "A family tree drawn on aged paper: at the root a small primate in a fruit tree, branching upward to a monkey, an ape, and a simple stickman; a small separate branch to the side with a guinea pig and a bat. Every animal on the tree holds a piece of fruit. Only the tree, its animals and the one stickman on it: no other people, no landscape, no ships around it.", text=[cap('MONKEYS  ·  APES  ·  US')]))
K('L08', "Your ancestors traded a gene for a bowl of fruit. I've been waiting ever since.",
  kg('c09a', C(.5, .45, 1.1), "Scurvy sits on a sea chest in a dark ship's hold, tossing a single wrinkled old apple up and down in one hand, the lantern beside him."))
N('L09', "The body only stores a few weeks' worth. After one to three months without fresh fruit or vegetables, he arrives.",
  dg('d09a', "A row of twelve simple glass jars for twelve weeks, each a little emptier of orange liquid than the last, the final jars completely empty; a small calendar above them. No people.", people=False, text=[cap('1 TO 3 MONTHS WITHOUT FRESH FOOD')]))

# ---- WHAT HE DOES TO YOU
N('S01', "So what does he do to you? First, you just feel tired. Weak, gloomy, with aching legs and joints. Officers often mistook it for laziness.",
  dg('d10a', "Two numbered panels: (1) a lively stickman sailor climbing the rigging, (2) the same stickman weeks later slumped against the mast with drooping eyes, little pain lines around his knees and ankles, a small grey rain cloud over his head.", text=[label('WHAT HE DOES TO YOU', 960, 150, 72), cap('TIRED  ·  WEAK  ·  ACHING')]),
  ch('c10a', W(), "On deck: a stickman bosun in a jacket points angrily at a tired stickman sailor sitting on a barrel with a mop beside him; they stand well apart."))
N('S02', "Then the spots. Tiny red and purple dots around the hairs on the legs, and big bruises from the slightest bump. Even the hairs themselves grow twisted, like corkscrews.",
  dg('d11a', "Just ONE single picture, not a sequence, no numbered stages: a stickman sailor in rolled-up trousers with small red dots drawn on his stick shins and a purple bruise patch on his forearm; a magnifying circle beside him shows one tiny hair twisted like a corkscrew.", text=[cap('SPOTS  ·  BRUISES  ·  CORKSCREW HAIRS')]))
N('S03', "Then the gums. They swell, turn purple and spongy, and bleed at a touch. The teeth loosen, and some fall out. And the breath became famously foul.",
  dg('d12a', "A simple cartoon textbook diagram of a smiling mouth, drawn twice: (1) neat white teeth with healthy pink gums, (2) puffy purple swollen gums with one gap where a tooth is missing and a loose tooth tilted. Clean, simple, not realistic.", people=False, text=[cap('SWOLLEN GUMS  ·  LOOSE TEETH')]),
  ch('c10b', C(.5, .5, 1.05), "A stickman sailor holding a ship's biscuit sadly in one hand, unable to bite it, touching his cheek with the other hand; a small green stink cloud drawn near his mouth."))
N('S04', "And then, the strangest part. Old scars open up again. Bones that healed years ago come apart at the old break. Without the glue, the body forgets its old repairs.",
  dg('d13a', "Only two close-up panels side by side, no people or figures anywhere: (1) a close-up of a simple pale forearm with an old stitched scar line whose stitches are coming undone like a loosening seam, (2) an X-ray style drawing of a long bone with an old healed break line, the two halves pulling apart at that line.", people=False, text=[cap('OLD WOUNDS REOPEN  ·  OLD BREAKS COME APART')]))
N('S05', "In the end, the victim bleeds inside, the heart gives out, and some died suddenly, just from being moved.",
  ch('c10c', W(), "Below deck by lantern light: ONLY TWO figures, nobody else: a very pale sailor stickman lies in a canvas hammock with both arms under a blanket; a ship's surgeon stickman in a dark coat stands a step away from the hammock, holding a small brown medicine bottle in one hand, his other hand on his own hip, looking worried."),
  sh('c10d', C(.5, .5, 1.05), "An empty canvas hammock gently swaying below deck of an 18th-century ship, a lantern swinging, a folded jacket and a knitted cap left on a sea chest. Somber. No people."))
K('S06', "Every scar you ever had, I give back. Free of charge.",
  kg('c11a', C(.5, .45, 1.1), "Scurvy bows like a polite shopkeeper behind a wooden counter in a ship's store room, holding out an empty open palm with one hand, the other hand holding his lantern."))

# ---- ancient times
N('L10', "He's an old enemy. Ancient writers described soldiers with rotting gums and swollen legs. So did crusaders in the 1200s.",
  dg('d14a', "A timeline with three numbered icons: (1) a Roman legionary helmet, (2) a crusader shield with a cross, (3) a small sailing ship; a tiny tricorn hat floats above each of them.", people=False, text=[cap('ROME  ·  THE CRUSADES  ·  THE AGE OF SAIL')]),
  sh('c12a', WR(), "A medieval crusader army camp in the desert at sunset with tents and banners, horses tethered. People only as tiny distant figures."))
N('L11', "But on land, he was rarely a monster. There was almost always something fresh to eat. It was the sea that gave him his kingdom.",
  sh('c12b', W(), "A medieval village vegetable garden in summer with cabbages, onions and an apple tree, a wooden fence and a cottage. No people."),
  sh('c12c', WL(), "An endless empty grey ocean with a single small sailing ship on the horizon under a huge sky. No people."))

# ---- the age of sail
N('L12', "From the 1500s, ships began making voyages that lasted months. Sailors lived on salt beef, dry biscuit and beer. Almost no vitamin C at all.",
  dg('d15a', "Three numbered items on aged paper: (1) a barrel of salt beef, (2) a hard square ship's biscuit with tiny weevils, (3) a barrel of beer; next to each a small empty glass gauge with no orange liquid. No people.", people=False, text=[cap('SALT BEEF  ·  BISCUIT  ·  BEER')]),
  ch('c13a', W(), "A ship's galley: a stickman cook in an apron bangs a hard biscuit on a table to knock weevils out, a big pot of salt beef boiling behind him."))
N('L13', "By one estimate, between 1500 and 1800, he killed some two million sailors. More than storms, shipwrecks and enemy guns combined.",
  dg('d16a', "A hand-drawn bar chart on aged paper: three short bars with small icons beneath them (a storm cloud, a broken ship, a cannon), and one enormous bar beside them with a small tricorn hat icon beneath it. The chart fills the whole frame; nothing drawn above or around it: no pictures, no comic panels. No people.", people=False, text=[cap('ABOUT 2 MILLION SAILORS  ·  1500 TO 1800')]))
K('L14', "Long voyage. No fresh food. My favourite kind of ship.",
  kg('c14a', C(.5, .45, 1.1), "Scurvy stands at the ship's wheel at sunset, steering with one hand, spyglass tucked under his other arm, smiling happily at the open sea."))
N('L15', "In 1497, Vasco da Gama set out to sail around Africa to India. Off East Africa, his men's gums grew so swollen they could hardly eat. When local traders brought them oranges, many recovered.",
  dg('d17a', "A map of Africa and the Indian Ocean on aged paper with a dotted route from Portugal down the west coast, around the southern tip, up the east coast and across to India; a small orange icon at the East African coast.", people=False, text=[cap('VASCO DA GAMA  ·  1497')]),
  sh('c15a', WR(), "A tropical East African harbour in 1498 with Portuguese caravels at anchor, palm trees, a small dhow with baskets of oranges approaching. People only as tiny distant figures."))
N('L15b', "But on the long way home, the oranges ran out. By the time he reached Portugal, more than half his crew were dead.",
  ch('c15b', W(), "On the deck of a caravel: a stickman sailor turns over an empty woven fruit basket, a second stickman sailor sits apart from him leaning on a barrel, looking weak."))
N('L16', "In 1536, the French explorer Jacques Cartier was trapped by ice on the St. Lawrence River in Canada. Twenty-five of his men died. Then a local Iroquoian man named Domagaya showed them a cure: a tea made from the needles and bark of a tree.",
  sh('c16a', WL(), "Two small 16th-century French ships frozen into a white river in winter, snow-covered forest and hills around, smoke from a small hut on shore. People only as tiny distant figures.", text=cap('CANADA · WINTER 1536')),
  ch('c16b', W(), "In a snowy 1530s forest by a frozen river: a stickman Iroquoian man in a fur cloak and leather leggings, with no feather headdress, points to an evergreen white cedar tree with flat scaly fronds, while a stickman French explorer in 1530s clothes (a dark doublet, a short cape and a soft flat cap, NOT a tricorn) watches him, both standing apart."),
  dg('d18a', "Four numbered steps: (1) an evergreen cedar branch, (2) needles and strips of bark chopped on a board, (3) boiled in a pot over a fire, (4) a stickman sailor drinking a steaming cup and standing up straight again.", text=[cap('CEDAR TEA')]))
N('L17', "Within days, the men were walking again. The cure had been found. And then it was forgotten. Again and again.",
  sh('c16c', C(.5, .5, 1.05), "A wooden cup of steaming green-brown tea on a snowy wooden barrel by a campfire, pine needles floating in it, a small cedar twig beside it. No lantern, no lemon, no fruit, nothing modern. No people."))
N('L17b', "In 1601, the English captain James Lancaster gave his crew three spoonfuls of lemon juice every morning. His men stayed healthy. The other ships in his fleet were so sick, his sailors had to help work them.",
  dg('d19a', "Four sailing ships at sea seen from the side: (1) the flagship with a small lemon flag and tiny healthy stickman sailors standing on deck, (2) (3) (4) three other ships with tiny stickman sailors lying down on deck; little arrows show sailors rowing from the flagship to help.", text=[cap('3 SPOONS OF LEMON JUICE A DAY')]),
  ch('c17a', W(), "On deck at morning: a stickman captain in a tricorn hat holds a big spoon and a bottle of yellow juice, a stickman sailor stands in front of him with his mouth open for a spoonful."))
K('L18', "Lemons. I hate lemons.",
  kg('c18a', C(.5, .45, 1.1), "Scurvy holds a single lemon at arm's length between two fingers, recoiling in disgust, his other hand holding his lantern."))

# ---- James Lind
N('L19', "Then, in 1747, a Scottish naval surgeon named James Lind did something new. On board HMS Salisbury, he took twelve sailors with scurvy, and split them into six pairs.",
  sh('c19a', W(), "An 18th-century Royal Navy warship at sea in calm weather, flying a large plain red ensign at the stern (a red flag with a small canton in the top corner), NOT a Union Jack. People only as tiny distant figures.", text=cap('HMS SALISBURY · 1747')),
  ch('c19b', W(), "A ship's sick bay: ONLY ONE figure, nobody else: a stickman naval surgeon in a dark coat and white wig stands holding an open notebook in one hand and a single quill in the other, in front of a row of empty canvas hammocks."))
N('L20', "Each pair got a different cure. Cider. Diluted sulfuric acid. Vinegar. Seawater. A spicy paste. And two oranges and a lemon every day.",
  dg('d20a', "Six numbered pairs of simple stickman sailors in hammocks in a row; under each pair one item: (1) a jug of cider, (2) a small dark glass bottle with drops, (3) a vinegar bottle, (4) a bucket of seawater, (5) a bowl of spicy paste, (6) two oranges and a lemon.", text=[cap('CIDER  ·  ACID  ·  VINEGAR  ·  SEAWATER  ·  PASTE  ·  CITRUS')]))
N('L21', "The citrus pair recovered so fast that within six days, one of them was fit for duty again. It was one of the first controlled trials in medical history.",
  dg('d21a', "The same six numbered pairs of stickman sailors: pairs 1 to 5 still lying in their hammocks looking weak, while pair 6 stands on deck happily, one of them pulling a rope; a small orange and lemon beside them.", text=[cap('DAY 6: THE CITRUS PAIR IS BACK ON DUTY')]),
  ch('c19c', C(.5, .5, 1.05), "A stickman sailor happily pulling a rope on a sunny deck, an orange peel on a barrel beside him."))
N('L21b', "But Lind himself wasn't sure what it meant. He suggested boiling the juice down to store it, and boiling destroys vitamin C. The Navy took almost fifty years to act.",
  dg('d22a', "Three numbered panels: (1) a glass of fresh lemon juice full of bright orange dots, (2) the juice boiling in a pot over a fire with steam, the dots escaping with the steam, (3) a small thick bottle with only a few dots left.", people=False, text=[cap('BOILED JUICE: MOST OF THE VITAMIN C GONE')]),
  sh('c19d', C(.5, .5, 1.05), "An 18th-century Admiralty office desk piled with stacks of papers and dusty files tied with ribbon, a quill and a candle, a clock on the wall. No people."))
K('L22', "Fifty years of paperwork. I kept myself busy.",
  kg('c20a', C(.5, .45, 1.1), "Scurvy sits with his boots up on a big desk in an empty Admiralty office, idly stamping papers with a rubber stamp, grinning."))

# ---- Captain Cook
N('L23', "Meanwhile, Captain James Cook sailed around the world, and lost almost no men to scurvy. He loaded his ships with sauerkraut, and stopped for fresh food wherever he could.",
  sh('c21a', WL(), "HMS Endeavour, a small three-masted ship, anchored in a turquoise Pacific bay with palm trees and green mountains. People only as tiny distant figures.", text=cap('CAPTAIN COOK · 1768')),
  dg('d23a', "A map of the Pacific on aged paper with Cook's dotted route weaving between islands; at each stop a small icon of fresh food: greens, fish, fruit; a barrel of sauerkraut drawn by the ship icon. No people.", people=False, text=[cap('SAUERKRAUT  ·  FRESH FOOD AT EVERY STOP')]))
N('L24', "When his sailors refused the sauerkraut, Cook had it served only at the officers' table. Within a week, the crew were demanding their share.",
  dg('d24a', "Three numbered panels: (1) a stickman sailor pushing away a bowl of sauerkraut, (2) two stickman officers in tricorn hats eating sauerkraut at a fine table while a sailor peeks curiously, (3) stickman sailors lining up with bowls in front of a barrel.", text=[cap('THE SAUERKRAUT TRICK')]),
  ch('c21b', W(), "A ship's officers' cabin: a stickman captain in a tricorn hat sits at a table eating from a bowl of sauerkraut with great show, a stickman sailor peeking through the door."))
N('L24b', "But Cook also praised malt and other remedies that did nothing. So it was hard to tell which of his tricks really worked.",
  sh('c21c', C(.5, .5, 1.05), "Still life on a ship's table: a barrel labelled only with a drawn cabbage, a sack of malt, jars and bottles of different remedies, a ship's log open beside them with no readable words. No people."))

# ---- the Navy
N('L25', "Finally, in 1795, pushed by the physician Gilbert Blane, the Royal Navy gave every sailor a daily ration of lemon juice. Within a few years, scurvy almost vanished from the fleet.",
  ch('c22a', W(), "On deck of a Royal Navy ship: a stickman sailor ladles lemon juice from a barrel into a tin cup held out by another stickman sailor standing apart; a lemon on the barrel."),
  dg('d25a', "A hand-drawn line graph on aged paper of scurvy cases in naval hospitals by year: a high line in the 1780s that falls steeply after a small lemon icon marked at 1795, and stays near the bottom. The graph fills the whole frame; nothing drawn above or around it: no pictures, no comic panels. No people.", people=False, text=[cap('ROYAL NAVY: LEMON JUICE FROM 1795')]))
N('L26', "Healthy crews could now stay at sea for months, blockading the ports of France. Some historians think lemon juice helped Britain win the Napoleonic Wars.",
  dg('d26a', "A map of the coast of France on aged paper with a ring of small British warship icons patrolling offshore for months, a calendar showing many months crossed off, and a small lemon icon beside the fleet.", people=False, text=[cap('MONTHS AT SEA  ·  BLOCKADING FRANCE')]),
  sh('c22b', WR(), "A line of Royal Navy warships under full sail on a grey sea in 1805, cannon smoke drifting far away. People only as tiny distant figures."))
N('L26b', "Later, the Navy switched to cheaper limes from its own colonies. That's how British sailors got the nickname Limeys. But limes have far less vitamin C than lemons.",
  dg('d27a', "Two fruits compared side by side: (1) a big yellow lemon with a tall glass gauge full of orange liquid, (2) a small green lime with a gauge only a quarter full. No people.", people=False, text=[cap('LEMON  ·  LIME')]))
K('L27', "Cheap limes. Bless the accountants.",
  kg('c23a', C(.5, .45, 1.1), "Scurvy raises a small green lime toward the viewer like a toast with one hand, his other hand holding his lantern by its handle down at his side, delighted, in a dim ship's store room full of barrels. The spyglass is tucked in his belt."))

# ---- the comeback
N('L28', "And so he came back. In 1875, a British Arctic expedition sailed with lime juice, and still came down with scurvy. Doctors started to doubt citrus altogether.",
  sh('c24a', WL(), "Two 19th-century wooden expedition ships frozen into Arctic sea ice under a pale sky, snow drifts, a small sledge on the ice. People only as tiny distant figures.", text=cap('THE ARCTIC · 1875')),
  ch('c24b', W(), "Inside a frozen ship's cabin: a stickman ship's doctor in a fur coat frowns at a bottle of greenish lime juice he holds up to a lamp."))
N('L29', "New theories blamed tainted tinned meat, or a germ. On Robert Falcon Scott's first Antarctic expedition, in 1902, men fell ill with scurvy, and recovered on fresh seal meat.",
  dg('d28a', "Two numbered panels with big question marks: (1) an old tin can of meat with a wavy smell line, (2) a few tiny rod-shaped bacteria under a magnifying glass; each with a large question mark above it. No people.", people=False, text=[cap('BAD TINNED MEAT?  ·  A GERM?')]),
  sh('c25a', W(), "A wooden expedition hut and a three-masted ship in Antarctic ice under a low sun, seals lying on the ice nearby. People only as tiny distant figures.", text=cap('ANTARCTICA · 1902')))
N('L29b', "On land, he struck whenever fresh food ran out. In the Irish famine of the 1840s, scurvy spread, because potatoes had been the poor's main source of vitamin C. He followed armies, sieges, gold rushes and prison camps.",
  dg('d29a', "Two numbered panels: (1) a healthy potato with a small glass gauge half full of orange liquid beside it, (2) a field of blackened, blighted potato plants with an empty gauge.", people=False, text=[cap('POTATOES: THE POOR\'S VITAMIN C')]),
  sh('c25b', WR(), "A gold-rush camp of the 1850s in the mountains: canvas tents, sluice boxes, piles of tins and sacks of flour, no vegetables anywhere. People only as tiny distant figures."))
K('L30', "When the food runs out, I'm always there.",
  kg('c26a', C(.5, .45, 1.1), "Scurvy sits on an empty overturned flour barrel in an empty frontier store with bare shelves, lantern on the floor, smiling patiently."))

# ---- the science
N('L31', "The breakthrough came by accident. In 1907, two Norwegian doctors, Axel Holst and Theodor Frølich, were feeding guinea pigs a diet of grain. The guinea pigs got scurvy.",
  ch('c27a', W(), "An early 1900s laboratory with wooden cages of guinea pigs on shelves: two stickman doctors in white coats and spectacles, standing apart, look at one cage with surprise.", text=cap('OSLO · 1907')),
  sh('c27b', C(.5, .5, 1.05), "Close view of a wooden cage with two small guinea pigs eating grain from a dish, a label card on the cage with no readable words, lab glassware behind. No people."))
N('L32', "Like us, guinea pigs can't make their own vitamin C. At last, scientists had an animal they could test. Food by food, they could measure what kept scurvy away.",
  dg('d30a', "Three numbered cages of guinea pigs: (1) fed only grain, the guinea pig looks scruffy and sad, (2) grain plus a cabbage leaf, the guinea pig looks healthy, (3) grain plus a slice of lemon, the guinea pig looks healthy. No people.", people=False, text=[cap('FOOD BY FOOD')]))
N('L33', "In 1912, the biochemist Casimir Funk gave a name to a new idea: vitamins. Tiny substances in food that the body can't live without.",
  ch('c28a', W(), "A 1912 laboratory: a stickman chemist in a waistcoat and spectacles writes on a blackboard covered with simple drawings of fruit, vegetables and grains, chalk in hand."))
N('L34', "And in the 1930s, the Hungarian scientist Albert Szent-Györgyi isolated the anti-scurvy substance, with help from the paprika peppers of his home town, Szeged. He won the Nobel Prize in 1937. It was named ascorbic acid. Literally: no scurvy.",
  sh('c28b', WL(), "A sunny field of red paprika peppers in Hungary with strings of drying red peppers hanging on a farmhouse wall. No people.", text=cap('SZEGED, HUNGARY')),
  dg('d31a', "Three numbered steps: (1) a red paprika pepper, (2) a glass flask with sparkling white crystals, (3) a simple hexagon-ring molecule drawing with a small medal next to it.", people=False, text=[cap('PAPRIKA  ·  CRYSTALS  ·  ASCORBIC ACID')]),
  ch('c28c', W(), "A 1930s laboratory: a stickman scientist in a white coat holds up a glass flask of white crystals to the light, a heap of red paprika peppers on the bench beside him."))
K('L35', "They named it after me. No scurvy. How hurtful.",
  kg('c29a', C(.5, .45, 1.1), "Scurvy holds a small glass jar of white crystals up to his lantern, scowling at it, offended."))

# ---- WHAT HE LEAVES BEHIND
N('A01', "And for the survivors? The good news: scurvy can be fully cured. With vitamin C, the bleeding stops and the gums heal within days. But lost teeth never grow back, and damage to joints can last.",
  dg('d32a', "Three numbered panels: (1) a weak stickman sailor in a hammock eating an orange, (2) a few days later sitting up, smiling, with a small sun icon, (3) weeks later standing strong on deck but with one small gap in his smile and a little bandage on his knee.", text=[label('WHAT HE LEAVES BEHIND', 960, 150, 72), cap('CURED IN DAYS  ·  LOST TEETH STAY LOST')]))
N('A02', "And for the world, he left something enormous: the idea of vitamins. Daily recommended amounts. Vitamins added to food. One of the first controlled trials. And a nickname for every British sailor.",
  dg('d33a', "Four numbered icons on aged paper: (1) a simple glass bottle of vitamin pills, (2) a carton of juice with a small sun symbol, (3) a notebook page with six pairs of tick marks, (4) a sailor's round hat with a small lime on it. No people.", people=False, text=[cap('VITAMINS  ·  FORTIFIED FOOD  ·  CLINICAL TRIALS')]))
K('A03', "No vaccine. No hospital. Just fruit. Humiliating.",
  kg('c30a', C(.5, .45, 1.1), "Scurvy sits alone on a jetty at dusk next to a wooden crate of lemons, chin on his hand, gloomy, his lantern dimmed."))

# ---- today
N('L36', "So is he gone? Not quite. Doctors still see him today, in people who eat almost no fruit or vegetables, in people who drink heavily, in old people living alone, and in crises where food aid has no fresh produce.",
  dg('d34a', "Three numbered panels: (1) an old stickman alone in a kitchen with an almost empty cupboard, (2) a stickman eating only from a box of crackers in front of a TV, (3) a row of tents with sacks of flour and no fresh food.", text=[cap('POOR DIETS  ·  LIVING ALONE  ·  CRISES')]),
  sh('c31a', W(), "A modern hospital clinic room with a desk, a computer and a bowl of oranges on the windowsill, bright and clean. No people."))
N('L37', "And the cure hasn't changed. A single orange a day is more than enough to keep him away.",
  dg('d35a', "A single orange cut in half beside a simple daily calendar; an arrow from the orange to a full glass gauge of orange liquid. No people.", people=False, text=[cap('ONE ORANGE A DAY IS ENOUGH')]),
  sh('c31b', C(.5, .5, 1.05), "A wooden kitchen table in morning sunlight with a bowl of oranges, lemons and a halved orange on a plate. No people."))
K('L38', "One orange. That's all it ever took. Don't tell anyone.",
  kg('c32a', C(.5, .45, 1.1), "Scurvy in a modern supermarket fruit aisle at night, no one else around, holding one orange behind his back with a guilty grin, lantern in his other hand."))
N('L39', "Three centuries at sea. Some two million sailors. Beaten not by a drug, but by lemons, a guinea pig, and a handful of paprika.",
  sh('c01a', W()), sh('d19a', STILL), sh('c19a', W()), sh('c27b', C(.5, .5, 1.05)), sh('c28b', W()))
N('L40', "Next time: a killer that waits in the bite of an animal. Once his symptoms begin, he is almost always fatal. And the first person saved from him was a nine-year-old boy.",
  sh('c33a', C(.5, .5, 1.04), "A foggy 19th-century cobbled street at night under a full moon: the dark silhouette of a tall gentleman in a tailcoat with the head of a wolf stands under a gas lamp, a broken chain hanging from his collar. Ominous."))
HOLD(5.0, sh('c33a', O(), text=[label('NEXT TIME', 1380, 360, 110, style='title', pop=True, at=.2, len=4.6), label('SUBSCRIBE', 1380, 500, 64, at=.8, len=4.0)]))

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
                pr = s['prompt']
                if not refs: pr += ' No people and no human figures anywhere in the picture.' if 'tiny distant' not in pr and 'silhouette' not in pr else ' Any people are tiny distant stickman silhouettes only.'
                out.append({'img': s['img'], 'prompt': STYLE + ' ' + pr, 'refs': refs})
    json.dump(out, open(os.path.join(ROOT, 'tools/plague/ep05_frames_todo.json'), 'w'), indent=1); print(len(out), 'frames')

def beats():
    out = {'base': 'assets/plague/ep05/frames', 'keep_zoom': [], 'fade_in': .8, 'start': 0.0, 'lead': .45, 'gap': .6, 'max_shot': 3.2,
           'sfx_global': [{'kind': 'drone', 't': 0.0, 'args': {'d': 'ALL'}, 'gain': .9}, {'kind': 'wind', 't': 0.0, 'args': {'d': 'ALL'}, 'gain': .14}], 'beats': []}
    M = 'assets/plague/music/'
    out['music'] = [{'file': M + f, 't0': float(a0), 't1': a1, 'gain': 1.0, 'fade_in': 2.0 if a0 == 0 else 4.0, 'fade_out': 5.0 if a1 == 'ALL' else 4.0}
                    for a0, a1, f in MUSIC]
    for i, r, t, shots in B:
        sl = []
        for s in shots:
            d = {'img': s['img'], 'from': s['cam'][0], 'to': s['cam'][1], 'w': s['w']}
            if 'text' in s: d['text'] = s['text']
            if 'sfx' in s: d['sfx'] = s['sfx']
            sl.append(d)
        if i: out['beats'].append({'vo': f'assets/plague/ep05/vo/{i}.wav', **({'gain': 1.05} if r == 'SCURVY' else {}), 'shots': sl})
        else: out['beats'].append({'hold': t, 'shots': sl})
    json.dump(out, open(os.path.join(ROOT, 'tools/plague/ep05_beats.json'), 'w'), indent=1); print(len(out['beats']), 'beats')

MUSIC = [(0, 170, 'plague_a.mp3'), (166, 330, 'plague_b.mp3'), (326, 480, 'plague_a.mp3'), (476, 'ALL', 'cholera_b.mp3')]   # set after the timeline: open+who | sail+Lind | navy+science | aftermath+today

{'lines': lines, 'frames': frames, 'beats': beats}[sys.argv[1]]()
