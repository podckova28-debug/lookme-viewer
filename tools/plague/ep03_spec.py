"""Episode 3 (The ENTIRE History of Smallpox): single source of truth. Same format as ep02_spec.py.

  python3 tools/plague/ep03_spec.py lines   -> voice list (id|ROLE|text), roles NARRATOR / SMALLPOX
  python3 tools/plague/ep03_spec.py frames  -> tools/plague/ep03_frames_todo.json
  python3 tools/plague/ep03_spec.py beats   -> tools/plague/ep03_beats.json (for beats.py)
"""
import sys, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
K_SHEET = '3ab41c2f-b46e-4a4c-abc5-c37ae21cf2e4'   # channel/plague/sheets/smallpox_turn_c.jpg
S_SHEET = '84427fc9-09ce-40e6-b032-6f2700874458'   # channel/plague/sheets/stickmen_common.jpg
STYLE = "2D animated history explainer frame, 16:9, no text. Hand-drawn ink illustration, clean black outlines, muted grey-sepia palette with deep crimson accents; warm light only from candles, lanterns, fire. Not gory, no visible sores close up."
STICK = ("Humans are simple STICKMEN in the style of the attached stickman sheet: plain white round head, two dot eyes, no nose, no beard, thin black stick arms and legs, "
         "simple clothes of ordinary people of the period. KEEP IT SIMPLE: only the few figures described, standing apart, never overlapping; each figure has exactly two arms "
         "and two hands, clearly attached to its own sleeves; nothing floating. No crowds, no ghost figures, no plague doctors.")
KING = ("The Speckled Monster exactly as on the attached sheet: a tall, straight-backed 18th-century nobleman with a big full-bottomed powdered white periwig of tight curls "
        "to the shoulders, a long pale powdered face covered with raised red speckles and pockmark scars, two small black beauty patches, cold narrow pale eyes and a thin cruel "
        "sneer; a dark plum-black velvet coat with tarnished gold embroidery, lace jabot, a gold lorgnette on a chain. Exactly ONE Speckled Monster, with exactly two arms and two hands. Haughty and evil.")

def W(): return [[.5, .5, 1.0], [.5, .5, 1.05]]
def WL(): return [[.47, .5, 1.04], [.53, .5, 1.04]]
def WR(): return [[.53, .5, 1.04], [.47, .5, 1.04]]
def C(x, y, z=1.3): z = 1 + (z - 1) * .4; return [[x, y, z], [x, y, z + .03]]
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
def ch(img, cam, p, **k): return sh(img, cam, STICK + ' ' + p, 'S', **k)
def kg(img, cam, p, stick=False, **k): return sh(img, cam, (STICK + ' ' if stick else '') + KING + ' ' + p, 'K' + ('S' if stick else ''), **k)

B = []
def N(i, t, *s): B.append((i, 'NARRATOR', t, list(s)))
def K(i, t, *s): B.append((i, 'SMALLPOX', t, list(s)))
def HOLD(sec, *s): B.append((None, None, sec, list(s)))

# ---- cold open: Geneva 1980
N('C01', "Geneva. The eighth of May, 1980. The World Health Assembly makes an announcement that had never been made before, and has never been made since.",
  sh('c01a', WL(), "Geneva in 1980 seen across the lake on a spring morning: the Palais des Nations with its flags, mountains in the distance, calm water.", text=cap('GENEVA · 8 MAY 1980')),
  ch('c01b', W(), "A 1980 assembly hall: one stickman delegate in a suit stands at a podium with a microphone; two other stickman delegates sit apart at desks in the front row, listening."))
N('C02', "A disease that killed around three hundred million people in the twentieth century alone is gone. Not cured. Not controlled. Gone.",
  sh('c02a', C(.5, .5, 1.1), "An old 1970s world map pinned to a wall, covered in many red pins, all of them now crossed out with black ink X marks."))
K('C03', "Gone is such an ugly word.",
  kg('c03a', C(.5, .45, 1.1), "The Speckled Monster stands in a dark palace corridor lit by a single candle, hands clasped behind his back, lifting his chin in cold disdain."))
N('C04', "Getting there took thousands of years, a milkmaid, a cow called Blossom, and twenty-two orphan boys on a ship.",
  ch('c04a', W(), "An English countryside farmyard in the 1790s: a stickman milkmaid in a bonnet sits on a stool milking a brown and white cow, a wooden bucket."),
  ch('c04b', W(), "An 18th-century sailing ship at sea; on deck, three small stickman boys in simple clothes stand apart at the rail looking at the ocean."))
K('C05', "I hate that cow.",
  kg('c05a', C(.5, .45, 1.1), "The Speckled Monster glares with pure hatred at a gilded portrait of a brown and white cow hanging on a palace wall, his lip curling."))
HOLD(4.6, kg('c06a', O(), "Title shot: the Speckled Monster stands on the left third of the frame in a dark candlelit palace hall with a black-and-white checkered floor, hands behind his back, looking at the viewer; dark empty space on the right side.")
     | {'text': [label('SMALLPOX', 1300, 330, 160, style='title', pop=True, at=.15, len=4.2), label('THE SPECKLED MONSTER', 1300, 480, 64, style='title', color=[214, 120, 110], at=.5, len=3.9)],
        'sfx': [{'kind': 'boom', 'at': .1, 'gain': .8}]})

# ---- who is he
N('L01', "So who is he? Smallpox is caused by the variola virus. A big, brick-shaped virus, one of the largest that infect humans.",
  sh('c07a', W(), "An old brass microscope on a cluttered desk lit by a candle, glass slides, notebooks."),
  sh('c07b', C(.5, .5, 1.15), "View through a microscope: a round bright circular field on black with several large brick-shaped virus particles with rounded corners and a bumpy surface; one in the centre wears a tiny powdered wig. Cute but sinister."))
K('L02', "I'm not big. I'm important.",
  kg('c08a', C(.5, .45, 1.1), "The Speckled Monster adjusts his lace jabot in front of a tall gilded mirror, admiring himself, vain."))
N('L03', "He spread from person to person, through the air, and on clothes and bedding. About two weeks after catching him came a high fever, and then a rash that turned into hard, painful blisters, all over the face and body.",
  ch('c09a', W(), "A simple 18th-century cottage room: one stickman lies in bed under a blanket with a cold cloth on his forehead and small red dots on his white round face; a candle and a jug on a stool."),
  sh('c09b', W(), "A pile of folded linen sheets and a blanket on a wooden chair by a window, with a faint sinister reddish haze around them. Symbolic still life."))
N('L04', "Around three in ten people who caught the classic form died. Survivors were often left with deep scars, and some went blind.",
  sh('c10a', STILL, "Ten small simple wooden figurines standing in a row on a dark wooden shelf, candle light. Symbolic still life.",
     text=[label('3 / 10', 960, 260, 110)]))
K('L05', "I like to leave a little something to remember me by.",
  kg('c11a', C(.5, .45, 1.1), "The Speckled Monster bows slightly and taps his own speckled cheek with one finger, cold smile."))
N('L06', "The English called him: the speckled monster.",
  sh('c12a', C(.5, .5, 1.05), "An 18th-century engraving-style printed broadsheet pinned to a wooden wall, showing a drawing of a tall dark silhouette in a big wig. Leave the broadsheet without words.",
     text=[label('THE SPECKLED MONSTER', 960, 900, 80)]))

# ---- origin
N('L07', "But where did he come from? His closest living relatives are poxviruses of animals: one found in African gerbils, and camelpox. So scientists think smallpox began as a virus of rodents that jumped into humans, probably somewhere in Africa or Asia, and adapted to us so well that it stopped needing animals at all.",
  sh('c13a', W(), "A small African gerbil sitting at the entrance of its burrow in dry savanna at dusk, acacia trees. Cute, no people."),
  sh('c13b', W(), "Two camels resting in desert dunes at sunset, a lone palm tree. No people."),
  sh('c13c', WL(), "A comic diagram on aged parchment: a small rodent, an arrow, a camel, an arrow, a human silhouette; a brick-shaped virus doodle travelling along the arrows. No words."))
K('L08', "I outgrew the gerbils. Humans had so much more potential.",
  kg('c14a', C(.5, .45, 1.1), "The Speckled Monster looks down his nose through his gold lorgnette at a tiny gerbil sitting on a velvet cushion, unimpressed."))
N('L09', "To survive, he needed lots of people living close together. So he probably only became a big problem after the rise of farming, and the first cities.",
  ch('c15a', WL(), "An ancient city of mud-brick houses on a river plain with fields, palm trees and a ziggurat; three stickmen in simple tunics walk apart on a dusty road."))
N('L10', "The Egyptian pharaoh Ramses the Fifth, who died more than three thousand years ago, has a rash of bumps on his mummified face that looks a lot like smallpox. Though nobody can prove it.",
  sh('c16a', W(), "An ancient Egyptian royal tomb lit by torches: a golden sarcophagus, painted hieroglyph-style walls without readable writing.", text=cap('RAMSES V · 1145 BC')),
  sh('c16b', C(.5, .5, 1.1), "A museum display case with an ancient wrapped mummy lying in it, dim spotlight. Respectful, not gross, no face visible."))
N('L10b', "The Antonine Plague, which swept across the Roman Empire from the year 165, may also have been him. It killed millions of people, and possibly the co-emperor Lucius Verus.",
  sh('c16c', WL(), "Ancient Rome around 165 AD: marble temples, the Colosseum, red-tiled roofs under a heavy grey sky, smoke from a few fires. People only as tiny distant figures.", text=cap('ROME · 165 AD')))
N('L11', "What we can prove is newer. In 2020, scientists found smallpox DNA in the teeth of Viking-age skeletons, from about fourteen hundred years ago. By then, he was already all over northern Europe.",
  ch('c17a', W(), "A modern genetics lab: one stickman scientist in a white coat holds up an ancient tooth with tweezers next to a screen with a DNA helix."),
  sh('c17b', WL(), "A Viking longship pulled up on a misty Scandinavian beach, wooden longhouses behind, grey sea.", text=cap('VIKING AGE · ABOUT 600 AD')))
K('L12', "Even the Vikings had me. I was fashionable early.",
  kg('c18a', W(), "The Speckled Monster stands on the prow of a Viking longship in the fog, hands behind his back, wig blowing in the wind, smug."))

# ---- crowns
N('L13', "Over the centuries, he spread across Asia, Africa and Europe, and he didn't care about rank. Queen Elizabeth the First of England caught him in 1562 and survived. Louis the Fifteenth of France died of him in 1774.",
  ch('c19a', W(), "A Tudor palace chamber: a stickman queen with a red Elizabethan wig, a big white ruff and a pale white face sits upright on a throne, candles around her.", text=cap('ELIZABETH I · 1562')),
  ch('c19b', W(), "A dim royal bedchamber at Versailles: a grand canopy bed with heavy curtains drawn, a gilded crown on a cushion on a side table, a single candle.", text=cap('LOUIS XV · 1774')))
N('L14', "So did Queen Mary the Second of England, the young tsar Peter the Second of Russia, and the Holy Roman Emperor Joseph the First.",
  sh('c20a', WL(), "Three empty gilded thrones in a row in a dark palace hall, each with a crown resting on its seat, candles, long shadows."))
K('L15', "I collect crowns. Every collector has a favourite piece.",
  kg('c21a', W(), "The Speckled Monster walks along a glass display cabinet full of royal crowns in a dark gallery, admiring them through his lorgnette."))
N('L16', "Rich women covered their scars with thick white make-up and little black patches of fabric on the face. Those patches became high fashion.",
  ch('c22a', C(.5, .5, 1.05), "An 18th-century dressing table with a mirror: a stickman lady in a tall powdered wig and a wide silk gown dabs white powder on her round white face; a small box of black beauty patches on the table."))

# ---- Americas
N('L17', "Then came the darkest chapter. After 1492, Europeans reached the Americas, and he came with them, into a world where nobody had ever met him before.",
  sh('c23a', WL(), "Spanish caravels with big crosses on their sails approaching a green tropical coast at dawn, mist. People only as tiny distant figures."))
N('L18', "In 1520, as Spanish conquistadors fought the Aztecs, smallpox swept through their capital, Tenochtitlan, and killed the new emperor, Cuitlahuac, after only a few months on the throne.",
  sh('c24a', W(), "The great Aztec capital Tenochtitlan on its lake: white temple pyramids, causeways, canals and canoes, volcanoes behind, smoke rising, dusk. People only as tiny distant figures.", text=cap('TENOCHTITLAN · 1520')),
  ch('c24b', C(.5, .5, 1.05), "Inside a stone Aztec palace room: a stickman Aztec ruler with a feathered headdress lies sick on a woven mat, a feather fan and a clay bowl beside him, torchlight."))
N('L19', "A few years later he reached the Inca Empire. The emperor Huayna Capac died, probably of smallpox, and his sons fought a civil war over the throne, just as the Spanish arrived.",
  sh('c25a', WL(), "An Inca city of fitted stone walls and terraces high in the Andes, misty mountain peaks, llamas. People only as tiny distant figures.", text=cap('INCA EMPIRE · ABOUT 1527')))
N('L20', "Smallpox, measles and other new diseases killed a huge share of the native population across the Americas. In some places, most of the people died.",
  sh('c26a', W(), "An empty village of thatched huts at dusk in the Americas, a cold campfire, abandoned baskets, long shadows. Somber, quiet. No people."))

# ---- variolation
N('L21', "Long before vaccines, people noticed something. If you survived smallpox, you never got it again. So in China, India, Africa and the Ottoman Empire, people tried something risky: they deliberately gave healthy people a mild dose.",
  ch('c27a', W(), "A Chinese medicine shop in the 1600s: a stickman healer in a robe and cap holds a small silver tube and a tiny dish of powder; a stickman patient sits on a stool in front of him."))
N('L22', "In China, they ground up dried scabs and blew the powder up your nose. In other places, they scratched a little pus from a sick person into the skin. It was called variolation.",
  ch('c28a', C(.5, .5, 1.05), "Close shot: a stickman healer gently blows through a thin silver tube toward the nose of a stickman child sitting still, the child squinting. Not scary, a little funny.", text=cap('VARIOLATION')))
K('L23', "Snorting me. How rude. And yet, effective.",
  kg('c29a', C(.5, .45, 1.1), "The Speckled Monster recoils in disgust, holding a lace handkerchief to his nose, offended."))
N('L24', "Variolation usually caused a milder illness. It still killed about one or two people in a hundred, but that was far better than three in ten.",
  sh('c10a', STILL, text=[label('1–2 / 100', 960, 260, 100)]))
N('L25', "In 1717, Lady Mary Wortley Montagu, the wife of the British ambassador in Constantinople, saw it done. Smallpox had scarred her face and killed her brother. She had her own son variolated, and brought the idea home to England.",
  sh('c30a', WL(), "Constantinople in 1717 across the Bosphorus: domes and minarets, sailing ships, a golden evening sky. People only as tiny distant figures.", text=cap('CONSTANTINOPLE · 1717')),
  ch('c30b', W(), "An Ottoman-style room with carpets and cushions: a stickman lady in an 18th-century English gown and a turban-like headscarf watches as an old stickman woman healer kneels beside a small stickman boy, holding a needle to his arm."))
N('L26', "In Boston in 1721, an enslaved West African man named Onesimus told the minister Cotton Mather that he'd been variolated as a child back home. Mather spread the word. During that year's epidemic, about fourteen percent of the people who caught smallpox naturally died. Among those who were variolated, about two percent.",
  sh('c31a', WL(), "Colonial Boston harbour in 1721: wooden wharves, sailing ships, brick and clapboard houses, a white church steeple. People only as tiny distant figures.", text=cap('BOSTON · 1721')),
  ch('c31b', W(), "A colonial study: a stickman man in simple working clothes and a stickman minister in a black coat with white bands and a wig sit apart at a table, talking; a candle and books."),
  sh('c31c', STILL, "A simple hand-drawn bar chart on aged paper filling the frame: one tall bar on the left, one very short bar on the right. No words.",
     text=[label('14%', 640, 230, 80), label('2%', 1290, 640, 80, at=.8)]))
K('L27', "Two percent. Still. Two percent of something is something.",
  kg('c32a', C(.5, .45, 1.1), "The Speckled Monster counts on his fingers with a sour expression, sitting stiffly in a gilded armchair."))

N('L27b', "Smallpox even shaped the American Revolution. George Washington had survived it as a young man. In 1777, worried it would wreck his army, he ordered the soldiers of the Continental Army to be variolated. One of the first mass immunisation campaigns in history.",
  ch('c32b', W(), "A snowy 1777 army camp of canvas tents: a tall stickman general in a blue coat with gold epaulettes and a black tricorn hat stands outside a tent; two stickman soldiers in tricorns wait in line a few steps apart.", text=cap('GEORGE WASHINGTON · 1777')))
K('L27c', "Washington. A very rude man.",
  kg('c32c', C(.5, .45, 1.1), "The Speckled Monster stands in the snow at the edge of an army camp, arms crossed, scowling at a row of tents."))
N('L27d', "He had famous survivors too. The eleven-year-old Mozart caught smallpox in 1767, and recovered. And Abraham Lincoln came down with a mild case right after giving the Gettysburg Address.",
  ch('c32d', W(), "An 18th-century music room: a small stickman boy in a little powdered wig and a red coat sits at a harpsichord playing, candles and sheet music.", text=cap('MOZART · 1767')),
  ch('c32e', W(), "A very tall thin stickman in a black suit, a tall black stovepipe hat and a simple line-drawn chin beard stands at a wooden lectern outdoors, autumn trees behind.", text=cap('ABRAHAM LINCOLN · 1863')))

# ---- Jenner
N('L28', "Then came the cow. In the English countryside, people had a story: milkmaids who caught cowpox, a mild disease from cows' udders, never got smallpox.",
  ch('c33a', W(), "A sunny 1790s English meadow with a thatched farmhouse: a stickman milkmaid in a bonnet carries two buckets on a yoke, a brown and white cow grazing nearby."))
N('L29', "In 1796, the doctor Edward Jenner tested it. He took fluid from a cowpox blister on the hand of a milkmaid, Sarah Nelmes, who had caught it from a cow called Blossom, and scratched it into the arm of an eight-year-old boy, James Phipps.",
  ch('c34a', W(), "An 18th-century country doctor's study: a stickman doctor in a dark coat and a short white wig holds a small lancet near the arm of a stickman boy sitting on a chair; a stickman milkmaid in a bonnet stands a few steps away holding her bandaged hand.", text=cap('EDWARD JENNER · 1796')),
  sh('c34b', C(.5, .5, 1.1), "A friendly brown and white cow standing in a green field, looking at the viewer, a little bell on her collar.", text=cap('BLOSSOM')))
N('L30', "Six weeks later, Jenner exposed the boy to real smallpox. Nothing happened. He was protected.",
  ch('c35a', W(), "The stickman boy stands smiling with his arms up in a sunny garden, healthy; the stickman doctor in a white wig watches from a few steps away, relieved."))
N('L31', "Jenner called it vaccination, from vacca, the Latin word for cow. Blossom's hide still hangs in the library of St George's medical school in London.",
  sh('c36a', W(), "A quiet old library with wooden bookshelves; a framed brown and white cowhide hangs on the wall like a precious exhibit, lit by a lamp. No people.", text=[label('VACCA = COW', 960, 200, 72)]))
K('L32', "I have been beaten. By a cow. Put that on my gravestone.",
  kg('c37a', C(.5, .45, 1.1), "The Speckled Monster stands in a muddy field staring in furious disbelief at a calm brown and white cow chewing grass in front of him."))
N('L33', "Testing it on a child would never be allowed today. But it worked, and it spread fast.",
  sh('c38a', WL(), "An old map of Europe drawn in ink on parchment with small glowing dots spreading out from England across the continent. No words."))

# ---- Balmis
N('L34', "There was one problem. The vaccine had to be kept alive, and in 1803 there were no fridges. So Spain came up with a solution that sounds unbelievable.",
  sh('c39a', W(), "The port of A Coruna in Spain in 1803: a sailing corvette at the quay, stone buildings, grey morning. People only as tiny distant figures.", text=cap('A CORUÑA · 1803')))
N('L35', "The Balmis expedition sailed for the Americas with twenty-two orphan boys. Every week or so, the cowpox was passed from the arm of one boy to the next, a living chain that kept the vaccine fresh across the Atlantic.",
  ch('c40a', W(), "Below deck on an 1803 sailing ship, lantern light: a stickman doctor in a dark coat carefully touches a small lancet to the arm of one stickman boy, while a second boy waits on a bench; two other boys sleep in hammocks."),
  sh('c40b', WL(), "An old map of the Atlantic Ocean drawn in ink on parchment with a dotted route from Spain to the Caribbean, a small sailing ship drawn on the route. No words."))
N('L36', "The boys were cared for on the voyage by Isabel Zendal, the head of their orphanage. The expedition went on to carry the vaccine as far as the Philippines and China.",
  ch('c41a', W(), "On the deck of a sailing ship at sunset: a stickman woman in a long dark dress and a white headscarf sits with an arm around a small stickman boy, two more boys sitting near her, looking at the sea."))
K('L37', "Children. Carrying my doom. In a boat. I was not consulted.",
  kg('c42a', W(), "The Speckled Monster stands alone on a rocky shore in the wind, hands behind his back, watching a small sailing ship disappear over the horizon, scowling."))

# ---- eradication
N('L38', "Over the next century and a half, vaccination pushed him out of Europe and North America. But in 1967 he still infected millions of people a year, in Asia, Africa and South America.",
  sh('c43a', W(), "A 1960s world map on a wall with many red pins across Asia, Africa and South America, very few in Europe and North America."))
N('L39', "That year, the World Health Organization launched an all-out campaign to wipe him off the planet. It was led by an American doctor, D. A. Henderson.",
  ch('c44a', W(), "A 1960s office: one stickman doctor with short hair and glasses in a white shirt and tie leans over a big world map spread on a desk, a telephone and folders beside it.", text=cap('WHO · 1967')))
N('L40', "Instead of trying to vaccinate everyone, teams hunted for every single case. When they found one, they vaccinated everyone around it, building a ring of immune people he couldn't cross. It was called ring vaccination.",
  sh('c45a', STILL, "Top-down simple diagram on aged paper: one red dot in the centre, surrounded by a neat ring of small green dots, then plain empty paper around them. No words."),
  ch('c45b', W(), "A village in 1970s South Asia: a stickman health worker with a bag kneels and vaccinates the arm of a stickman villager, while two more villagers wait apart."))
N('L41', "A simple tool helped too: a two-pronged needle that held exactly one dose, and could be used by almost anyone after a short lesson.",
  sh('c46a', C(.5, .5, 1.1), "Close-up still life: a small steel bifurcated needle with two short prongs lying next to a tiny glass vaccine vial on a white cloth. Simple, clean."))
K('L42', "They hunted me. Village by village. Like a common criminal.",
  kg('c47a', W(), "The Speckled Monster hides behind a mud wall in a hot dusty village, peeking out nervously, holding his wig on with one hand."))
N('L43', "Even during the Cold War, the United States and the Soviet Union worked together on it. The Soviet Union donated huge amounts of vaccine.",
  sh('c48a', W(), "Two wooden crates of vaccine vials side by side on a dock, one stencilled with a red star, the other with stars and stripes, a small olive branch between them. No people, no words."))
N('L44', "In 1975, a two-year-old girl in Bangladesh, Rahima Banu, became the last person to catch the deadly major form naturally. She survived.",
  ch('c49a', W(), "A village in Bangladesh by a river: a small stickman girl sits in the doorway of a hut, smiling, a stickman health worker kneeling a few steps away.", text=cap('BANGLADESH · 1975')))
N('L45', "In October 1977, a hospital cook in Somalia, Ali Maow Maalin, caught the milder form. He was the last natural case in history. He recovered, and later spent years working to wipe out polio.",
  ch('c50a', W(), "A sunny town in Somalia with white houses and the sea behind: one stickman man in a simple shirt stands smiling outside a small hospital building.", text=cap('MERCA, SOMALIA · 1977')))
N('L46', "There was one more death. In 1978, a medical photographer, Janet Parker, caught smallpox from a laboratory in Birmingham, in England, and died. She was the last person known to die of smallpox.",
  sh('c51a', W(), "A 1970s university building at dusk in Birmingham, England, a lit window on an upper floor, a camera on a desk visible through it. Quiet, somber.", text=cap('BIRMINGHAM · 1978')))
N('L47', "And on the eighth of May, 1980, the world declared smallpox eradicated. The only human disease ever wiped out.",
  sh('c02a', C(.5, .5, 1.1), text=stamp('ERADICATED', x=1380, y=240, size=96)))
K('L48', "Eradicated. Such a strong word. I prefer: retired.",
  kg('c52a', C(.5, .45, 1.1), "The Speckled Monster sits stiffly in a gilded armchair in an empty dusty palace hall with sheets over the furniture, sipping tea from a fine china cup, pretending not to care."))

# ---- today
N('L49', "So is he really gone? Almost. Officially, live samples of the virus are kept in just two laboratories, one in the United States and one in Russia.",
  sh('c53a', W(), "A high-security laboratory corridor with two heavy steel freezer doors side by side, warning lights, cold blue light. No people.", text=[label('USA', 690, 860, 60), label('RUSSIA', 1230, 860, 60)]))
N('L50', "For decades, scientists have argued about whether to destroy them for good. So far, nobody has.",
  ch('c54a', W(), "A conference room: two stickman scientists in suits sit apart at a long table arguing, one pointing at a document, the other with arms folded."))
K('L51', "Two freezers. That's my whole kingdom now. But I am very, very patient.",
  kg('c55a', C(.5, .45, 1.1), "The Speckled Monster stands in a frosty steel freezer room, frost on his wig and eyebrows, hands behind his back, smiling coldly."))
N('L52', "Thousands of years of scarred faces. Hundreds of millions of lives. Beaten by a milkmaid's blister, a living chain of orphans, and doctors who hunted down every last case.",
  sh('c19b', W()), sh('c24a', W()), sh('c34b', W()), sh('c40a', W()), sh('c45a', W()), sh('c02a', W()))
N('L53', "Next time: a flu that came home with the soldiers at the end of a world war, and killed more people than the war itself.",
  sh('c56a', C(.5, .5, 1.05), "A 1918 train station at night in fog: a steam train with soldiers' kit bags piled on the platform, a gas lamp; on the platform stands a tall dark silhouette in a long military greatcoat and a gauze mask. Ominous."))
HOLD(5.0, sh('c56a', O(), text=[label('NEXT TIME', 1380, 360, 110, style='title', pop=True, at=.2, len=4.6), label('SUBSCRIBE', 1380, 500, 64, at=.8, len=4.0)]))

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
    json.dump(out, open(os.path.join(ROOT, 'tools/plague/ep03_frames_todo.json'), 'w'), indent=1); print(len(out), 'frames')

def beats():
    out = {'base': 'assets/plague/ep03/frames', 'fade_in': .8, 'start': 0.0, 'lead': .45, 'gap': .6, 'max_shot': 3.2,
           'sfx_global': [{'kind': 'drone', 't': 0.0, 'args': {'d': 'ALL'}, 'gain': .9}, {'kind': 'wind', 't': 0.0, 'args': {'d': 'ALL'}, 'gain': .1}], 'beats': []}
    M = 'assets/plague/music/'   # shared library: plague_* for ancient/early modern chapters, cholera_* for 18th c. onward
    out['music'] = [{'file': M + f, 't0': float(a0), 't1': a1, 'gain': 1.0, 'fade_in': 2.0 if a0 == 0 else 4.0, 'fade_out': 5.0 if a1 == 'ALL' else 4.0}
                    for a0, a1, f in MUSIC]
    for i, r, t, shots in B:
        sl = []
        for s in shots:
            d = {'img': s['img'], 'from': s['cam'][0], 'to': s['cam'][1], 'w': s['w']}
            if 'text' in s: d['text'] = s['text']
            if 'sfx' in s: d['sfx'] = s['sfx']
            sl.append(d)
        if i: out['beats'].append({'vo': f'assets/plague/ep03/vo/{i}.wav', **({'gain': 1.05} if r == 'SMALLPOX' else {}), 'shots': sl})
        else: out['beats'].append({'hold': t, 'shots': sl})
    json.dump(out, open(os.path.join(ROOT, 'tools/plague/ep03_beats.json'), 'w'), indent=1); print(len(out['beats']), 'beats')

MUSIC = [(0, 'ALL', 'plague_a.mp3')]   # re-split by chapter once the voice-over (and real timings) exist

{'lines': lines, 'frames': frames, 'beats': beats}[sys.argv[1]]()
