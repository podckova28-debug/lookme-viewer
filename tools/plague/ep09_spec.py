"""Episode 9 (The ENTIRE History of Leprosy): single source of truth. Same format as ep08_spec.py, with the retention rules
(static camera, a person in trouble in the first second, characters in almost every frame, natural captions) and stricter anatomy
rules after the ep08 misses (third hand, an arm reaching around a microscope, a twisted body).

  python3 tools/plague/ep09_spec.py lines   -> voice list (id|ROLE|text), roles NARRATOR / LEPROSY
  python3 tools/plague/ep09_spec.py frames  -> tools/plague/ep09_frames_todo.json
  python3 tools/plague/ep09_spec.py beats   -> tools/plague/ep09_beats.json (for beats.py)
"""
import sys, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
K_SHEET = 'e662a14b-a9dc-4f9f-af5f-9819fa95fe5d'   # channel/plague/sheets/leprosy_a.jpg (the Grey Friar), Higgsfield upload
STYLE = ("2D animated history explainer frame, 16:9, no text. Hand-drawn ink illustration, clean black outlines, muted ash-grey, cold blue and sepia palette "
         "with warm candle and lamp light accents. Not gory: no wounds, no sores, no deformities drawn.")
MODERN = ("2D animated history explainer frame, 16:9, no text. Hand-drawn ink illustration, clean black outlines, the same muted grey, blue and sepia palette, "
          "soft natural daylight. The setting is modern (2000s-2020s): no lanterns, no oil lamps, no candles, nothing old-fashioned. Not gory.")
SN = ("Humans are simple STICKMEN: plain white round head, two dot eyes, no nose, no beard, thin black stick arms and stick legs, small black mitten hands, "
      "dressed exactly as described for this scene and era; anyone wearing glasses has his two dot eyes INSIDE the lenses and no other eyes. "
      "Only the few figures described, standing apart, never overlapping; each has exactly two arms and two hands; every arm comes straight out of its own shoulder "
      "and never bends around or behind an object; head, body and feet of each figure face the same way, no twisted bodies; "
      "hands are empty unless an object is described; nothing floating; no flags; no readable text.")
KING = ("Leprosy exactly as on the attached sheet, 'the Grey Friar': a very tall, thin, calm figure in a long tattered ash-grey hooded friar's robe tied with a rope belt, "
        "hood up, a smooth pale ash-grey face with half-closed pale icy-blue eyes and a thin patient smile, frost on the hem of his robe, a small brass hand bell hanging "
        "from his rope belt. Exactly ONE of him, with exactly two arms and two hands with normal-length fingers; each arm comes from its own shoulder; "
        "no extra hands anywhere in the picture, nothing poking out from under his robe. He holds AT MOST ONE object, his other hand empty and clearly attached to its own arm.")
DIAG = ("Draw ONLY the diagram described below, filling the whole frame, as ONE single picture: no extra rows, no extra panels, no comic strips above or below it. "
        "A hand-drawn explainer diagram in ink and muted watercolour on aged paper, clean and readable like an old textbook plate, "
        "numbered stages as small circled digits with drawn arrows. No words, no letters, no numbers on axes, only circled digits. Not gory. ")
NOPEOPLE = ' No people and no human figures anywhere in the picture.'
LAMPS = " Lighting only from oil lamps, candles or daylight: no electric bulbs."

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
def ch(img, cam, p, modern=False, **k): return sh(img, cam, (MODERN if modern else STYLE + ' ') + SN + ' ' + p, **k)
def kg(img, cam, p, **k): return sh(img, cam, STYLE + ' ' + KING + ' ' + p + ' No other people.', 'K', **k)
def dg(img, p, people=False, **k): return sh(img, STILL, STYLE + ' ' + (SN + ' ' if people else '') + DIAG + p + ('' if people else NOPEOPLE), **k)
def ob(img, p, cam=None, **k): return sh(img, cam or C(.5, .5, 1.05), STYLE + ' ' + p + NOPEOPLE, **k)

B = []
def N(i, t, *s): B.append((i, 'NARRATOR', t, list(s)))
def K(i, t, *s): B.append((i, 'LEPROSY', t, list(s)))
def HOLD(sec, *s): B.append((None, None, sec, list(s)))

DAMIEN = "a stickman Catholic priest with small round glasses, a long black 1880s cassock and a wide-brimmed black hat"
HUT = "a simple 1880s wooden cottage room in Hawaii with a plank floor, a small window onto palm trees and steep green sea cliffs"

# ---- cold open: Damien's scalded feet (Kalaupapa, December 1884)
N('C01', "A priest lowers his feet into a basin of water. It's scalding hot. Steam is rising off it. And he feels absolutely nothing.",
  ch('c01a', C(.5, .5, 1.05), f"Inside {HUT}: {DAMIEN} without his hat sits on a wooden chair, his bare stick feet resting in a large tin basin of water with thick steam rising from it; he looks down at the basin calmly, both hands resting on his knees.", text=cap('The water is scalding')),
  ch('c01b', W(), f"Inside {HUT}: a young Hawaiian stickman helper in a white 1880s shirt and dark trousers stands a step away from the seated priest, holding a steaming metal kettle in one hand, his mouth open in shock; the priest in his black cassock sits on the chair with his feet in the steaming basin, looking up at him; only these two figures.", text=cap('He feels nothing')))
N('C02', "His name is Father Damien. For eleven years, he has lived among the outcasts of Kalaupapa, a strip of land in Hawaii cut off by sea cliffs, where people with one disease were sent and never allowed to leave. Molokai, December 1884.",
  ch('c02a', WL(), f"A small 1880s village of white wooden cottages on a flat grassy peninsula under enormous green sea cliffs, the ocean behind: {DAMIEN} walks along a dirt path beside a stickman Hawaiian man in a white shirt and straw hat; they talk, standing a step apart.", text=cap('Father Damien')),
  ch('c02b', W(), "A huge wall of green sea cliffs dropping straight into a rough blue ocean, a flat grassy peninsula at their foot with a tiny cluster of white cottages and a small white church: on the rocky shore in the foreground two stickman Hawaiian patients in plain white shirts stand apart, looking out at a sailing ship far away on the sea.", text=cap('Kalaupapa, Molokai — 1884')))
N('C03', "Now he knows. At his next sermon, he no longer says 'you lepers'. He says, 'we lepers'.",
  ch('c03a', C(.5, .5, 1.05), f"Inside a small white wooden 1880s mission church with simple pews and a plain wooden altar, daylight through the windows: {DAMIEN} without his hat stands at the front with both hands open towards the people, while two stickman Hawaiian patients in white shirts sit apart on a front pew, looking up at him.", text=cap('"We lepers"')))
K('C04', "Eleven years among my patients. Did he really think I wouldn't notice him?",
  kg('c04a', C(.5, .45, 1.1), "Medium shot: the Grey Friar stands at the open door of a dim little wooden church at dusk, the sea and green cliffs behind him, looking in with a patient smile, one empty hand resting on the door frame, his other hand hanging at his side."))
HOLD(4.6, kg('c05a', O(), "Title shot: the Grey Friar stands on the left third of the frame on a misty grey medieval road at dusk with bare trees, his hood up, both hands folded calmly in front of his rope belt; dark empty grey mist on the right side.")
     | {'text': [label('LEPROSY', 1300, 330, 130, style='title', pop=True, at=.15, len=4.2), label('THE OLDEST STIGMA', 1300, 470, 72, style='title', color=[180, 205, 225], at=.5, len=3.9)],
        'sfx': [{'kind': 'boom', 'at': .1, 'gain': .8}]})

# ---- who is he
N('L01', "So who is he? A bacterium. Mycobacterium leprae, a close cousin of tuberculosis. In 1873, a Norwegian doctor, Gerhard Armauer Hansen, spotted him under the microscope. He was one of the very first germs ever linked to a human disease.",
  dg('d02a', "A scale comparison: a small bundle of thin rod-shaped bacteria lying side by side like a pack of cigars (1), next to a much LARGER long nerve fibre drawn as a pale cable (2), with the bacteria nestled against it."),
  ch('c06a', W(), "An 1870s hospital laboratory in Bergen, Norway, with wooden panelling, a tall window onto a grey harbour with wooden houses: a stickman doctor in a dark 1870s frock coat and a high collar sits at a table looking into a brass microscope that stands directly in front of him, one hand on the focus knob at the side of the microscope, his other hand flat on the table." + LAMPS, text=cap('Gerhard Armauer Hansen, 1873')))
N('L02', "And he is slow. Incredibly slow. He divides only about once every two weeks. And after a hundred and fifty years, scientists still can't grow him in a lab dish.",
  dg('d03a', "Two scenes side by side in one row: (1) a single rod bacterium beside a big calendar with fourteen days crossed out, (2) a snail beside it for comparison."),
  ch('c07a', C(.5, .5, 1.05), "A bright modern laboratory: a stickman scientist in a white lab coat and blue gloves holds up an empty round glass petri dish in one hand, frowning at it in confusion, her other hand on her hip.", modern=True, text=cap("He still won't grow in a lab")))
N('L03', "He loves the cold. He settles in the coolest parts of the body: the skin, the nose, the ears, the hands and feet. And above all, the nerves.",
  dg('d04a', "A simple standing stickman outline in front view; its hands, feet, nose area and ears are tinted cold blue, the chest and belly tinted warm orange; numbered circles (1) hands, (2) feet, (3) face.", people=True, text=[cap('The coolest parts of the body')]))
K('L04', "Warm hearts don't interest me. I prefer cold hands.",
  kg('c08a', C(.5, .45, 1.1), "The Grey Friar stands by a frosted window in a cold dark stone room at night, gently drawing a line in the frost on the glass with one fingertip, smiling softly; his other hand hidden in his sleeve."))
N('L05', "Strangely, he is one of the hardest diseases to catch. He spreads through droplets from the nose and mouth, usually after months of close contact. And about ninety-five percent of people are naturally immune.",
  dg('d05a', "ONLY a single row of ten simple stickman icons across the page; nine of them have a small shield drawn in front of them, one has no shield and is tinted grey.", people=True, text=[cap('About 95% are naturally immune')]),
  ch('c09a', W(), "A small 1880s Hawaiian cottage at evening: a stickman father in a white shirt and a stickman mother in a long loose blue 1880s Hawaiian dress sit apart at a low wooden table sharing a meal from one bowl, each holding a spoon in one hand.", text=cap('Months of close contact')))
N('L06', "But he is patient. After infection, he can wait five years, sometimes twenty, before the first sign appears.",
  dg('d06a', "ONLY one long single row of twenty small blank calendar sheets across the page, with a sleeping rod bacterium drawn on the first one and a small red dot on the last one."))
K('L07', "Twenty years? That's nothing. I have all the time in the world.",
  kg('c10a', C(.5, .45, 1.1), "The Grey Friar sits on a stone bench in a misty grey cloister, both empty hands folded in his lap, watching a large hourglass on the bench beside him with a calm smile."))

# ---- origin
N('L08', "Where did he come from? His family is ancient. He may have started in East Africa or the Near East, and travelled with humans for tens of thousands of years. The oldest known case is a skeleton from India, about four thousand years old.",
  dg('d08a', "A simple world map with dotted arrows spreading out from East Africa across the Near East to India, Europe and East Asia, with tiny rod bacteria riding along the arrows.", text=[cap('He travelled with us')]),
  ch('c11a', C(.5, .5, 1.05), "A bright modern archaeological dig in a dry Indian landscape: a stickman archaeologist in a khaki shirt and a wide sun hat kneels in a shallow trench, gently brushing earth off an ancient skeleton with a small brush in one hand, her other hand on her knee.", modern=True, text=cap('India, 4,000 years ago')))
N('L09', "Along the way, he threw away almost half of his own genes. He can no longer survive on his own. He needs us.",
  dg('d09a', "A long DNA double helix drawn across the page from left to right: the left half bright and complete, the right half faded, broken and crumbling into pieces."))
N('L10', "And he has a few other friends. In the southern United States, nine-banded armadillos carry him, and can pass him to people. In Britain, even some red squirrels have him.",
  ch('c11b', WL(), "A sunny modern Texas ranch yard with a wooden fence and dry grass: a stickman rancher in a cowboy hat, a checked shirt and jeans crouches down, looking curiously at a nine-banded armadillo walking past him on the ground; only this one human figure.", modern=True, text=cap('Armadillos in the American South')),
  dg('d10a', "Two animals side by side: (1) a nine-banded armadillo, (2) a red squirrel on a branch, each with a tiny rod bacterium icon beside it.", text=[cap('Even red squirrels in Britain')]))
K('L11', "Armadillos. Squirrels. I'm not fussy about my company.",
  kg('c12a', C(.5, .45, 1.1), "The Grey Friar sits on a log at the edge of a misty autumn forest, holding out one open hand with a hazelnut on his palm to a red squirrel on the log beside him, his other hand resting on his knee."))

# ---- WHAT HE DOES TO YOU
N('S01', "So what does he do to you? It starts quietly. A pale or reddish patch on the skin. It doesn't itch. It doesn't hurt. And if you touch it, you can barely feel it.",
  dg('d11a', "A large simple stickman forearm drawn as a pale tube with one round pale patch on it, and a small feather touching the patch with a question mark beside it.", people=True, text=[label('What He Does to You', 960, 150, 72), cap('A patch you can barely feel')]),
  ch('c13a', C(.5, .5, 1.05), "A bright modern clinic room: a stickman doctor in a white coat gently touches the forearm of a stickman patient with a small wisp of cotton wool held in one hand; the patient in a short-sleeved shirt sits on an examination couch with his eyes closed, holding his arm out; a small pale round patch on the forearm.", modern=True, text=cap("Eyes closed: can you feel this?")))
N('S02', "Because he attacks the nerves. Slowly, the hands and feet go numb. You can grab a hot pot and not notice. You can walk all day with a stone in your shoe.",
  dg('d12a', "Three numbered panels in one row: (1) a healthy nerve drawn as a bright cable, (2) the same nerve with small rod bacteria clustered on it and turning grey, (3) a stickman hand outline tinted grey with a small zero-sound symbol.", people=True, text=[cap('He attacks the nerves')]),
  ch('c13b', W(), "A simple rural kitchen in 1900s India with a clay stove: a stickman cook in a white dhoti and a white cotton shirt lifts a steaming hot clay pot off the fire by its rim with one bare hand, looking calm, not noticing the heat; his other hand at his side.", text=cap('Burns you never feel')))
N('S03', "Those unnoticed injuries get infected, again and again. Over many years, fingers and toes can become shortened. They don't simply fall off. That's a myth. The damage comes from wounds that no one could feel.",
  dg('d13a', "Three numbered steps in one row, drawn simply and not gory: (1) a hand outline touching a hot stove, (2) the hand with a small bandage, (3) a calendar with many years and the bandaged hand again.", text=[cap("Fingers don't just fall off")]))
N('S04', "The nerves of the face can fail too. The eyes can't blink properly and slowly go blind. In the worst form, the skin of the face thickens into lumps.",
  dg('d14a', "A simple standing stickman outline in front view with three numbered magnifier circles pointing to: (1) an eye with a half-closed eyelid, (2) a hand, (3) a foot.", people=True, text=[cap('Eyes, hands and feet')]))
N('S05', "He almost never kills you directly. What he takes is feeling. And then, very often, your place among other people.",
  ch('c13c', WL(), "The edge of a medieval village at dusk with timber houses: a single stickman in a long grey hooded cloak stands alone on the road outside the village fence, while two stickman villagers in brown tunics stand far away inside the fence, turned away from him.", text=cap('Then, your place among people')))
K('S06', "I rarely kill anyone. I simply make sure nobody wants to touch you.",
  kg('c14a', C(.5, .45, 1.1), "The Grey Friar stands alone in an empty grey medieval square, slowly pulling a grey glove onto one hand with the other hand, smiling softly."))

# ---- ancient world
N('L12', "People have known him for thousands of years. In ancient India, the surgeon Sushruta described the disease and treated it with oil pressed from the seeds of the chaulmoogra tree.",
  ch('c15a', W(), "An ancient Indian courtyard with carved stone pillars and a banyan tree: a stickman physician in a white dhoti and a white shawl over one shoulder pours a little oil from a small clay jug held in one hand onto a stone dish, while a stickman patient in a simple cotton wrap sits apart on a mat watching.", text=cap('Sushruta, ancient India')),
  ob('c15b', "A small heap of round brown chaulmoogra seeds and a small clay jar of golden oil on a carved stone ledge, warm daylight.", text=cap('Chaulmoogra oil')))
N('L13', "In the Bible, the Hebrew word 'tzaraat' was translated as leprosy. It probably covered many different skin conditions. But the name stuck, and so did the fear.",
  ch('c15c', C(.5, .5, 1.05), "An ancient Near Eastern stone courtyard with a tent of goat hair: a stickman priest in a long white linen robe and a white turban looks closely at the forearm of a stickman man in a brown woven robe, who holds his own arm out; they stand a step apart.", text=cap('Tzaraat: many diseases, one fear')))
K('L14', "They gave my name to every rash in the world. I took it as a compliment.",
  kg('c16a', C(.5, .45, 1.1), "The Grey Friar sits at a long wooden table in a dim scriptorium, reading a huge open old book with an amused smile, one hand turning a page, the other hand resting flat on the table."))

# ---- Middle Ages
N('L15', "In medieval Europe, he was everywhere. Thousands of leper houses, named lazar houses after Saint Lazarus, were built just outside the towns.",
  ch('c17a', WL(), "A small medieval stone lazar house with a little chapel and a walled garden, standing alone on a hill outside a walled town with church spires: a stickman monk in a brown habit carries a basket of bread in one hand along the path towards it, while a stickman patient in a grey hooded cloak stands apart at the gate.", text=cap('A lazar house outside the walls')),
  dg('d15a', "A simple map of medieval Europe with many small house icons scattered across it, each one just outside a walled-town icon.", text=[cap('Thousands of them')]))
N('L16', "In some places, a person diagnosed was led into church for a ceremony like a funeral. Afterwards, they had to wear special clothes and gloves, and carry a bell or a wooden clapper to warn people they were coming.",
  ch('c17b', C(.5, .5, 1.05), "A dim medieval stone church lit by candles: a stickman priest in a black robe and a white surplice stands at the altar step with one hand raised, while a stickman in a plain grey hooded cloak kneels a few steps in front of him, head bowed, hands folded.", text=cap('A ceremony like a funeral')),
  dg('d16a', "Four numbered objects in one row: (1) a long grey hooded cloak, (2) a pair of grey gloves, (3) a wooden clapper made of three small boards on a handle, (4) a small wooden bowl.", text=[cap('Cloak, gloves, clapper, bowl')]),
  ch('c17c', W(), "A muddy medieval country road between fields: a single stickman in a long grey hooded cloak and grey gloves walks along the road, carrying a wooden clapper in one hand; ahead of him a stickman peasant woman in a brown dress and a white headscarf steps off the road onto the grass to let him pass.", text=cap('A clapper to warn people')))
N('L17', "They couldn't enter the market, touch the food, or drink from a shared well. They were still alive, but treated as if they had already died.",
  ch('c17d', W(), "A medieval market square with a bread stall: a stickman baker in a white apron stands behind the stall and steps back, both hands raised, while a stickman in a grey hooded cloak and grey gloves stands a few steps away from the stall, pointing at a loaf with a long wooden stick held in one hand.", text=cap('Not allowed to touch the food')))
K('L18', "Ring the bell, everybody moves away. That bell was my favourite invention.",
  kg('c18a', C(.5, .45, 1.1), "The Grey Friar stands in an empty medieval street at dusk, holding up the small brass bell from his belt in one hand and ringing it gently, smiling; his other hand empty at his side."))
N('L19', "He even reached a throne. Baldwin the Fourth of Jerusalem was a boy when his tutor noticed he felt no pain when the other boys pinched his arm. He became king at thirteen. At sixteen, he defeated Saladin at the Battle of Montgisard. He died at twenty-three.",
  ch('c19a', W(), "A sunny 1170s palace courtyard in Jerusalem with pale stone arches: two stickman boys in short medieval tunics stand on either side of a third stickman boy in a fine blue tunic, each of them pinching one of his arms, while the boy in blue smiles calmly; a stickman tutor in a long black clerical robe watches from a bench a few steps away.", text=cap('He felt no pain')),
  ch('c19b', C(.5, .5, 1.05), "Inside a large 1170s crusader army tent: a young stickman king in a long white surcoat with a small gold crown on his head and white gloves stands at a wooden table with a map, one hand resting on the hilt of a sword in its scabbard at his belt, the other hand on the map; a stickman knight in chainmail stands apart by the tent pole.", text=cap('Baldwin IV, king at 13')),
  dg('d17a', "A simple battle map of a hilly plain with two groups of small banners without symbols: a small group (1) charging with an arrow towards a much larger group (2), which scatters.", text=[cap('Montgisard, 1177')]))
N('L20', "Then, after the 1300s, he slowly faded from most of Europe. Nobody knows exactly why. Perhaps the plague killed the weakest. Perhaps tuberculosis, his cousin, gave people some protection.",
  dg('d18a', "ONLY one simple line chart filling the whole page: a thick line high on the left, then slowly falling to the bottom on the right; a tiny lazar-house icon in the top left corner. No numbers.", text=[cap('He faded from Europe')]),
  ch('c20a', WL(), "An abandoned overgrown medieval stone lazar house on a green hill, ivy on the walls, the roof half fallen: a stickman shepherd in a brown tunic and a straw hat leads one sheep past it on the path, holding a wooden crook in one hand.", text=cap('Empty leper houses')))
K('L21', "I didn't leave Europe. I was crowded out by my own family.",
  kg('c21a', C(.5, .45, 1.1), "The Grey Friar sits alone in an empty overgrown medieval stone chapel with ivy and broken windows, chin resting on one hand, looking bored, his other hand on his knee."))

# ---- Norway and Hansen
N('L22', "But in the 1800s, he was still common in western Norway. Norway created the world's first national register of patients. And in the port of Bergen, a young doctor went hunting for the cause.",
  ch('c22a', WL(), "A grey 1870s Norwegian harbour town with colourful wooden warehouses along the quay and sailing ships: a stickman doctor in a dark overcoat and a bowler hat walks along the quay carrying a leather medical bag in one hand, his other hand in his coat pocket.", text=cap('Bergen, Norway')),
  ch('c22b', C(.5, .5, 1.05), "An 1870s office with tall shelves of thick ledgers: a stickman clerk in a dark waistcoat and sleeve garters sits at a desk writing in a huge open ledger with a dip pen held in one hand, his other hand holding the page flat." + LAMPS, text=cap("The world's first patient register")))
N('L23', "In 1873, Hansen saw tiny rods inside his patients' tissue. Many doctors still believed the disease was hereditary. Hansen proved it was caused by a germ.",
  ob('d19a', "A microscope view: a bright round field with pale pink tissue and many small dark red rod-shaped bacteria lying in bundles.", text=cap('Tiny rods, 1873')),
  ch('c22c', W(), "The 1870s Bergen hospital laboratory with wooden panelling and a tall window onto the grey harbour: the stickman doctor in a dark frock coat stands beside the table with the brass microscope, raising one fist in triumph, his other hand flat on the table." + LAMPS, text=cap('A germ, not a curse')))
N('L24', "But he went too far. In 1879, to prove the disease was contagious, he tried to infect a patient's eye without her consent. She took him to court, and he lost his hospital post.",
  ch('c22d', C(.5, .5, 1.05), "An 1880 Norwegian courtroom with dark wooden panelling and a high judge's bench: a stickman judge in a black robe sits behind the bench, looking down sternly, while the stickman doctor in a dark frock coat stands below him with his head bowed, both hands clasped in front of him; only these two figures.", text=cap('Taken to court, 1880')))
K('L25', "Even the man who discovered me had a dark side. I liked him immediately.",
  kg('c23a', C(.5, .45, 1.1), "The Grey Friar sits alone on a wooden bench at the back of an empty dark 1880s courtroom, legs crossed, one empty hand resting on his knee, the other on the bench, smiling slyly."))

# ---- Hawaii
N('L26', "Meanwhile in Hawaii, the disease spread fast. From 1866, the kingdom began sending patients to Kalaupapa. Families were torn apart at the docks. Over a century, about eight thousand people were sent there.",
  ch('c24a', W(), "A wooden dock in 1860s Honolulu with a small steamship tied up: a stickman Hawaiian mother in a long loose yellow 1860s dress stands on the dock reaching out one arm towards her stickman son in a white shirt, who is being led up the gangplank by a stickman official in a dark uniform and cap holding the boy's shoulder with one hand.", text=cap('Honolulu, 1866')),
  dg('d20a', "ONLY a simple map of the Hawaiian islands filling the page, with a dotted arrow from the island of Oahu to a small flat peninsula on the north coast of Molokai under high cliffs.", text=[cap('About 8,000 people sent to Kalaupapa')]))
N('L27', "That's where Father Damien came, in 1873. He built houses, a church, and coffins. He died there in 1889, at forty-nine. Today, he is a saint.",
  ch('c25a', WL(), f"A sunny 1870s building site in Kalaupapa under green sea cliffs: {DAMIEN} without his hat hammers a nail into the wooden wall of a half-built cottage with a hammer held in one hand, holding the plank with his other hand, while a stickman Hawaiian man in a white shirt stands apart, carrying a plank on his shoulder.", text=cap('He built houses and a church')),
  ch('c25b', C(.5, .5, 1.05), "A simple grave with a white wooden cross under a pandanus tree beside a small white church, green cliffs behind: a stickman nun in a black habit and a white wimple kneels beside the grave, laying a small bunch of flowers on it with both hands.", text=cap('Father Damien, died 1889')))
K('L28', "He stayed with them to the end. I'll admit it. That one, I respected.",
  kg('c26a', C(.5, .45, 1.1), "The Grey Friar stands a few steps away from a simple white wooden cross under a pandanus tree at sunset, his hood lowered slightly, both empty hands folded in front of his rope belt, head bowed."))

# ---- Alice Ball and the cure
N('L29', "For centuries, the best treatment was still chaulmoogra oil. Swallowed, it made people sick. Injected, it formed painful lumps. Then, in 1915, a twenty-three-year-old chemist in Hawaii, Alice Ball, found a way to make it injectable.",
  ch('c27a', W(), "A 1915 university chemistry laboratory in Honolulu with wooden benches, glass flasks and a window onto palm trees: a young stickwoman chemist with short dark curly hair, in a long 1910s skirt, a white blouse and a white lab apron, holds up a small glass flask of golden oil to the window light with her right hand; her left arm hangs straight down at her side, its hand empty by her skirt. Exactly two arms and two hands on her, both attached to her shoulders; nothing lying on the bench except glassware: no gloves, no extra hands.", text=cap('Alice Ball, 1915')),
  dg('d21a', "Three numbered steps in one row: (1) a bottle of thick golden oil, (2) a glass flask over a small flame with an arrow, (3) a small glass syringe.", text=[cap('Oil you could inject')]))
N('L30', "She died the next year, at just twenty-four. A university president published her work under his own name. Her credit was only restored decades later.",
  ch('c27b', C(.5, .5, 1.05), "A 1910s university office with a big wooden desk: a stickman man in a dark three-piece suit sits at the desk, writing his signature on the cover page of a thick report with a fountain pen held in one hand, his other hand holding the page flat; a framed diploma on the wall.", text=cap('Someone else took the credit')))
N('L31', "The real cure came from Carville, Louisiana, America's leprosy hospital. In 1941, Doctor Guy Faget tried a new sulfa drug called Promin. Patients began to get better. They called it the Miracle at Carville.",
  ch('c28a', WL(), "A white 1940s hospital building with tall columns and a long veranda under big oak trees with Spanish moss in Louisiana: on the veranda a stickman nun nurse in a white habit stands beside a stickman patient sitting in a wicker wheelchair, smiling; only these two figures.", text=cap('Carville, Louisiana')),
  ch('c28b', W(), "A bright 1940s hospital ward: a stickman doctor in a white coat and small round glasses gives an injection with a small glass syringe held in one hand into the upper arm of a stickman patient in pyjamas sitting on the edge of a bed; the doctor's other hand rests on the patient's shoulder.", text=cap('Promin, 1941')))
N('L32', "Then came dapsone, a cheap pill. But he learned to resist it. So in 1981, the World Health Organization combined three drugs. Since then, millions of people have been cured.",
  dg('d22a', "Three different simple pill shapes joined by plus signs in one row, then an arrow to a small calendar and a big green tick.", text=[cap('Three drugs together, 1981')]),
  ch('c28c', C(.5, .5, 1.05), "A sunny modern village health post in India: a stickman health worker in a pale blue sari hands a small blister pack of pills to a stickman man in a white kurta, who takes it with both hands, smiling; they stand a step apart.", modern=True, text=cap('Millions cured')))
K('L33', "Three pills. Four thousand years, and they beat me with three pills.",
  kg('c29a', C(.5, .45, 1.1), "The Grey Friar sits at a small table in an empty modern clinic room, staring glumly at a small blister pack of pills lying on the table in front of him, chin resting on one hand, his other hand flat on the table."))

# ---- WHAT HE LEAVES BEHIND
N('A01', "And for those who are cured? The bacteria are gone, but nerve damage stays. Many people live with numb hands and feet, and must check them for injuries every single day.",
  dg('d23a', "Three numbered objects in one row and NO people: (1) a simple bare foot outline seen from below with a small magnifying glass over its sole, (2) a pair of thick protective sandals, (3) a small hand mirror.", text=[label('What He Leaves Behind', 960, 150, 72), cap('Checking for injuries every day')]),
  ch('c30a', W(), "A bright modern courtyard in India: an elderly stickman man in a white kurta and thick protective sandals sits on a plastic chair, holding a small hand mirror under the sole of his raised foot with one hand to check it, his other hand on his knee.", modern=True, text=cap('Numb hands and feet')))
N('A02', "For the world, he left a word. 'Leper' came to mean an outcast. Japan only abolished its isolation law in 1996. And in India, leprosy was grounds for divorce until 2019.",
  ch('c30b', C(.5, .5, 1.05), "A quiet Japanese sanatorium on a small island by the sea, a low wooden building with a veranda and pine trees: an elderly stickman man in a grey cardigan and slippers stands alone on the veranda, looking out at the sea, both hands resting on the wooden railing.", modern=True, text=cap('Japan ended isolation only in 1996')),
  dg('d24a', "Three numbered icons in one row: (1) a medieval clapper, (2) a locked gate in a wall, (3) a torn document with a broken wax seal.", text=[cap("'Leper' came to mean outcast")]))
K('A03', "Medicine cured me. Your fear of me? That's much harder to cure.",
  kg('c31a', C(.5, .45, 1.1), "The Grey Friar stands in a dim stone corridor, his reflection in a tall old mirror beside him, looking at the viewer with a sad calm smile, both empty hands folded in front of his rope belt."))

# ---- today
N('T01', "Today, around two hundred thousand new cases are found every year. More than half are in India, and many in Brazil and Indonesia.",
  dg('d25a', "ONLY a simple world map filling the whole page: India shaded dark red, Brazil and Indonesia shaded medium red, other regions pale. Nothing else, no pictures, no panels.", text=[cap('About 200,000 new cases a year')]),
  ch('c32a', W(), "A sunny modern street in a small Brazilian town with colourful houses: a stickman community health worker in a white polo shirt and a cap knocks on an open blue door with one hand, holding a clipboard in the other, while a stickman woman in a sundress stands in the doorway.", modern=True, text=cap('Brazil, Indonesia, India')))
N('T02', "Treatment is free. And if he's found early, there's no damage at all. His strongest allies today are shame and silence.",
  ch('c32b', C(.5, .5, 1.05), "A bright modern clinic room: a young stickwoman in a colourful kurta sits on a chair, showing a small pale patch on her own forearm to a stickman doctor in a white coat who leans forward to look; the doctor's hands rest on his own knees; both calm.", modern=True, text=cap('Treatment is free')))
K('T03', "Hide me, and I win. Show me to a doctor, and I lose. It really is that simple.",
  kg('c33a', C(.5, .45, 1.1), "The Grey Friar stands half hidden in the shadow of a bright modern clinic doorway, peeking in with one hand on the door frame, his other hand hidden in his sleeve, looking uneasy."))

# ---- ending
N('L34', "Four thousand years. Kings, priests and whole nations treated the sick as if they were already dead. In the end, he was beaten by three cheap pills, and by people who refused to look away.",
  sh('c03a', C(.5, .5, 1.05)), sh('c17c', W()), sh('c22c', W()), sh('c28c', C(.5, .5, 1.05)),
  kg('c34a', C(.5, .45, 1.1), "The Grey Friar walks away slowly along a misty grey road at dusk, seen from behind in profile, his hood up, the small brass bell swinging at his rope belt, both hands hidden in his sleeves."))
N('L35', "Next time: a summer terror that emptied the swimming pools, and locked children inside iron lungs.",
  ch('c35a', C(.5, .5, 1.04), "A dark 1950s hospital ward at night, ominous, lit by one lamp: on the left third of the frame a big metal cylindrical iron lung machine on legs, with the head of a small stickman child resting on a pillow at its open end: a plain white round head with exactly TWO small dot eyes and nothing else on the face, looking up; nobody else; the right side of the frame is dark empty shadow."))
HOLD(5.0, sh('c35a', O(), text=[label('NEXT TIME', 1380, 360, 110, style='title', pop=True, at=.2, len=4.6), label('SUBSCRIBE', 1380, 500, 64, at=.8, len=4.0)]))

# ---- extra cut-ins for faster cutting (pos None = end)
EXTRA = {
  'C02': [(1, ch('c02c', C(.5, .5, 1.05), f"Inside {HUT}: {DAMIEN} sits alone at a small wooden table by the window, writing a letter with a dip pen held in one hand, his other hand holding the paper flat." + LAMPS, text=cap('Eleven years in Kalaupapa')))],
  'L05': [(None, ch('c09b', C(.5, .5, 1.05), "A modern bright family living room: a stickman father in a T-shirt and a stickman daughter in a school uniform sit apart on a sofa, both laughing, healthy; only these two.", modern=True, text=cap('Most people never get sick')))],
  'L09': [(None, kg('c11c', C(.5, .45, 1.1), "The Grey Friar stands by a dark stone table, calmly dropping a crumpled scroll into a small fire burning in a stone bowl, with one hand; his other hand hidden in his sleeve."))],
  'S02': [(None, ch('c13d', C(.5, .5, 1.05), "A dusty 1900s Indian village road: a stickman farmer in a white dhoti and a white shirt walks along the road barefoot, calm, not noticing a small sharp stone under his foot; only this one figure.", text=cap("Wounds you don't notice")))],
  'L12': [(None, ch('c15d', W(), "An ancient Indian forest at dawn: a stickman villager in a simple cotton wrap reaches up with one hand to pick a round brown fruit from a tall chaulmoogra tree, holding a small woven basket in the other hand."))],
  'L15': [(None, ch('c17e', C(.5, .5, 1.05), "The walled garden of a medieval lazar house: a stickman monk in a brown habit pours water from a jug held in one hand into a wooden bowl held out by a stickman patient in a grey hooded cloak, who holds the bowl with both hands; they stand a step apart.", text=cap('Cared for, but kept apart')))],
  'L19': [(None, ch('c19c', W(), "A rocky hillside in the Holy Land in 1177 under a bright sky: a young stickman king in a white surcoat with a small gold crown sits on a calm brown horse, both of his hands holding the reins; the horse has exactly four legs; two stickman knights in chainmail stand apart on foot beside the horse.", text=cap('Victory at sixteen')))],
  'L22': [(None, ob('c22e', "An old leather-bound register book lying open on a wooden desk, pages covered with neat unreadable handwritten columns, a dip pen and an inkwell beside it, warm lamp light."))],
  'L26': [(None, ch('c24b', C(.5, .5, 1.05), "A small rowing boat on a rough grey-blue sea under huge green cliffs: two stickman Hawaiian patients in plain white shirts sit apart in the boat, looking back at the sea, while a stickman boatman in a dark jacket rows with both hands on the oars.", text=cap('A one-way journey')))],
  'L29': [(None, ob('c27c', "A 1910s laboratory bench with a glass flask of golden oil, a small brass burner with a flame and a glass syringe lying on a white cloth, warm window light, palm leaves outside."))],
  'L31': [(None, ch('c28d', C(.5, .5, 1.05), "A 1940s hospital ward with tall windows: a stickman patient in pyjamas walks out through the open door with a small suitcase in one hand, waving with the other hand to a stickman nun nurse in a white habit who waves back from beside an empty bed.", text=cap('The Miracle at Carville')))],
  'T01': [(None, ch('c32c', W(), "A busy modern Indian health camp under a white tent: a stickman doctor in a white coat sits at a folding table writing on a form with a pen held in one hand, while a stickman woman in a sari sits apart on a plastic chair in front of the table; only these two.", modern=True, text=cap('More than half in India')))],
}
for _i, _r, _t, _sh in B:
    for _pos, _s in EXTRA.get(_i, []):
        if _pos is None: _sh.append(_s)
        else: _sh.insert(_pos, _s)

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
    json.dump(out, open(os.path.join(ROOT, 'tools/plague/ep09_frames_todo.json'), 'w'), indent=1); print(len(out), 'frames')

def beats():
    out = {'base': 'assets/plague/ep09/frames', 'keep_zoom': [], 'static': True, 'fade_in': .8, 'start': 0.0, 'lead': .45, 'gap': .6, 'max_shot': 3.2,
           'sfx_global': [{'kind': 'drone', 't': 0.0, 'args': {'d': 'ALL'}, 'gain': .9}, {'kind': 'wind', 't': 0.0, 'args': {'d': 'ALL'}, 'gain': .12}], 'beats': []}
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
        if i: out['beats'].append({'vo': f'assets/plague/ep09/vo/{i}.wav', **({'gain': 1.05} if r == 'LEPROSY' else {}), 'shots': sl})
        else: out['beats'].append({'hold': t, 'shots': sl})
    json.dump(out, open(os.path.join(ROOT, 'tools/plague/ep09_beats.json'), 'w'), indent=1); print(len(out['beats']), 'beats')

MUSIC = [(0, 200, 'cholera_a.mp3'), (196, 360, 'plague_a.mp3'), (356, 470, 'plague_b.mp3'), (466, 'ALL', 'cholera_b.mp3')]   # open+who+origin+symptoms | ancient+medieval | Norway+Hawaii | cure+aftermath+today

{'lines': lines, 'frames': frames, 'beats': beats}[sys.argv[1]]()
