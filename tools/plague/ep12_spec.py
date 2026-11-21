"""Episode 12 (The ENTIRE History of Yellow Fever): single source of truth. Same format as ep11_spec.py.

  python3 tools/plague/ep12_spec.py lines   -> voice list (id|ROLE|text), roles NARRATOR / YELLOWJACK
  python3 tools/plague/ep12_spec.py frames  -> tools/plague/ep12_frames_todo.json
  python3 tools/plague/ep12_spec.py beats   -> tools/plague/ep12_beats.json (for beats.py)
"""
import sys, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
K_SHEET = 'b07363b0-ee94-48ac-95f4-250f18d3dbbb'   # channel/plague/sheets/yellowfever_a.jpg ('Yellow Jack'), Higgsfield job
STYLE = ("2D animated history explainer frame, 16:9, no text. Hand-drawn ink illustration, clean black outlines, fine cross-hatching, muted tropical palette of "
         "faded canary yellow, sea teal, sun-bleached cream and sepia with small black accents and hot hazy sunlight or warm lamp light. Not gory.")
MODERN = ("2D animated history explainer frame, 16:9, no text. Hand-drawn ink illustration, clean black outlines, the same muted palette, soft natural daylight. "
          "The setting is modern (2000s-2020s): nothing old-fashioned. Not gory.")
SN = ("Humans are simple STICKMEN: plain white round head, two dot eyes, no nose, no beard, thin black stick arms and stick legs, small black mitten hands, "
      "dressed exactly as described for this scene and era; anyone wearing glasses has his two dot eyes INSIDE the lenses and no other eyes. "
      "Only the few figures described, standing apart, never overlapping; each has exactly two arms and two hands; every arm comes straight out of its own shoulder "
      "and never bends around or behind an object; head, body and feet of each figure face the same way, no twisted bodies; "
      "hands are empty unless an object is described; nothing floating; no flags, no banners; no readable text.")
KING = ("Yellow fever exactly as on the attached sheet, 'Yellow Jack': a tall, thin, grinning 1850s dandy with jaundiced yellow skin, yellow eyes with glowing amber irises "
        "and a wide sly grin, curly dark hair, a low wide-brimmed black planter's hat with one small cartoon mosquito with black-and-white striped legs perched on the brim, "
        "a faded canary-yellow tailcoat with black piping, a black-and-yellow horizontally striped waistcoat, a black silk cravat, narrow black trousers, cream spats and black gloves. "
        "Exactly ONE of him, with exactly two arms and two black-gloved hands; each arm comes from its own shoulder; no extra hands anywhere in the picture. "
        "He holds AT MOST ONE object, his other hand empty and clearly attached to its own arm.")
DIAG = ("Draw ONLY the diagram described below, filling the whole frame, as ONE single picture: no extra rows, no extra panels, no comic strips above or below it. "
        "A hand-drawn explainer diagram in ink and muted watercolour on aged paper, clean and readable like an old textbook plate, "
        "numbered stages as small circled digits with drawn arrows. No words, no letters, no numbers on axes, only circled digits. Not gory. ")
NOPEOPLE = ' No people and no human figures anywhere in the picture.'
MOSQ = "a small Aedes aegypti mosquito, black with white stripes on its legs and body"
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
def ob(img, p, cam=None, modern=False, **k): return sh(img, cam or C(.5, .5, 1.05), (MODERN if modern else STYLE) + ' ' + p + NOPEOPLE, **k)

B = []
def N(i, t, *s): B.append((i, 'NARRATOR', t, list(s)))
def HOLD(sec, *s): B.append((None, None, sec, list(s)))
def K(i, t, *s): B.append((i, 'YELLOWJACK', t, list(s)))

ARMYDOC = "a stickman US Army doctor in an 1900 khaki uniform shirt with rolled-up sleeves"
HAVANA = "a 1900 army camp hospital near Havana: a whitewashed wooden ward with tall shuttered windows, palm trees outside, hot hazy sunlight"

# ---- cold open: Havana, 1900
N('C01', "Havana, August 1900. An American army doctor, James Carroll, rolls up his sleeve. A colleague holds a small glass tube against his arm. Inside is a mosquito that has just fed on a yellow fever patient.",
  ch('c01a', C(.5, .5, 1.05), f"Medium shot in {HAVANA}: {ARMYDOC} sits on a wooden chair holding out his bare forearm, looking nervous, sweat on his head; a second stickman doctor in a white coat stands apart beside him, pressing a small glass test tube upside down onto the forearm with one hand, his other hand at his side.", text=cap('Havana, August 1900')),
  ob('c01b', f"An extreme close-up of a small glass test tube held upside down against bare skin, with {MOSQ} inside it, about to bite; warm hazy light.", text=cap('On purpose')))
N('C02', "Days later, Carroll is burning with fever, and the whites of his eyes are turning yellow. He survives. His colleague, Jesse Lazear, is bitten too. He does not.",
  ch('c02a', W(), f"{HAVANA}: a stickman patient lies in an iron hospital bed under a white mosquito net, his round head tinted pale yellow, sweating, while a stickman nurse in a long white 1900 dress and white cap stands apart beside the bed holding a cup of water in one hand.", text=cap('Fever, and the eyes turn yellow')),
  ch('c02b', C(.5, .5, 1.05), f"A small 1900 laboratory at night lit by an oil lamp: a stickman doctor in a white coat sits at a wooden desk looking into a brass microscope with both hands on the focus knob, while {MOSQ} lands on the back of his neck.", text=cap('Jesse Lazear')))
N('C03', "For three centuries, this fever terrorised the Americas. It emptied cities, wrecked an emperor's plans, and turned its victims yellow.",
  ch('c03a', WL(), "A deserted 1800s tropical port street at noon with closed shutters, palm trees and sailing ships in the harbour behind: a single stickman man in a 1800s linen coat and straw hat hurries away along the empty street, holding a white handkerchief over his face with one hand.", text=cap('Three centuries of terror')))
K('C04', "Sailors called me Yellow Jack. I always liked that name.",
  kg('c04a', C(.5, .45, 1.1), "Medium shot: Yellow Jack stands on a wooden harbour dock at dusk with sailing ships behind him, tipping his wide black hat to the viewer with one gloved hand, grinning, his other hand on his hip."))
HOLD(4.6, kg('c05a', O(), "Title shot: Yellow Jack stands on the left third of the frame on a misty tropical dock at dusk with palm trees and the dark masts of ships, bowing slightly to the viewer with one gloved hand on his chest, his other arm at his side; the right side of the frame is empty hazy yellow-grey sky.")
     | {'text': [label('YELLOW FEVER', 1300, 330, 130, style='title', pop=True, at=.15, len=4.2), label('YELLOW JACK', 1300, 470, 72, style='title', color=[235, 200, 80], at=.5, len=3.9)],
        'sfx': [{'kind': 'boom', 'at': .1, 'gain': .8}]})

# ---- who is he
N('L01', "So who is he? A virus. Tiny, even next to a bacterium. And he can't travel on his own. He rides inside one particular mosquito: Aedes aegypti, the one with white stripes on its legs.",
  dg('d02a', "A scale comparison: one rod-shaped bacterium drawn large (1), beside it a cluster of tiny round virus particles drawn much smaller (2), and beside them a mosquito with white-striped legs drawn large and simple (3)."),
  kg('c06a', C(.5, .45, 1.1), f"Yellow Jack stands in a sunny courtyard, holding up one gloved finger with {MOSQ} sitting on it, admiring it fondly like a pet bird, his other hand behind his back.", text=cap('Aedes aegypti')))
N('L02', "Only the female bites. She drinks infected blood, the virus multiplies inside her, and about a week later, every bite she gives passes him on.",
  dg('d03a', "Four numbered steps in one row: (1) a mosquito drinking from a fevered arm, (2) the same mosquito resting on a wall with a small clock icon, (3) tiny dots multiplying inside the mosquito's body, (4) the mosquito biting a second, healthy arm.", text=[cap('One bite is enough')]),
  ch('c07a', W(), f"A sunny 1800s bedroom with an open shuttered window: a stickman man in a white shirt sits on the edge of his bed, slapping at {MOSQ} on his own forearm with his other hand, annoyed.", text=cap('She bites by day')))
N('L03', "She bites in the daytime, and lays her eggs in clean, still water: barrels, buckets, flower pots, anything that holds rain.",
  ch('c08a', C(.5, .5, 1.05), "A sunny 1800s tropical courtyard with a big wooden rain barrel under a drainpipe and clay flower pots: a stickman woman in a long 1800s dress and headscarf fills a bucket from the barrel with both hands, while two mosquitoes hover above the water.", text=cap('Barrels, buckets, flower pots')),
  ob('c08b', "An extreme close-up looking down into an old wooden rain barrel full of clear still water, tiny mosquito larvae wriggling near the surface, a few floating leaves, warm light.", text=cap('A mosquito nursery')))
K('L04', "Give me one forgotten bucket of rainwater, and I'll give you an epidemic.",
  kg('c09a', C(.5, .45, 1.1), "Yellow Jack leans on an old wooden rain barrel in a sunny courtyard, tapping the lid with one gloved finger and smiling slyly at the viewer, his other hand on his hip."))

# ---- origin
N('L05', "Where did he come from? The forests of Africa. There, he passed between monkeys and forest mosquitoes, and from time to time, he jumped to people.",
  dg('d04a', "A simple circular cycle with arrows: (1) a monkey in a tree, (2) a forest mosquito, (3) a second monkey, and a dotted side arrow from the mosquito to (4) a simple stickman head.", people=True, text=[cap('Monkeys, mosquitoes, people')]),
  ch('c10a', W(), "The edge of a dense African rainforest at dawn with tall trees and hanging vines, monkeys sitting high in the branches: a stickman man in a simple wrapped cloth carries a bundle of firewood on his shoulder with one hand, looking up at the monkeys.", text=cap('The forests of Africa')))
N('L06', "Then came the Atlantic slave trade. Ships carried enslaved Africans to the Americas, and in the ships' water barrels, the mosquito came too. The first clear epidemics hit Barbados and Yucatán in the sixteen-forties.",
  dg('d05a', "A simple map of the Atlantic Ocean with West Africa on the right and the Caribbean and Central America on the left, a few small sailing ship icons with arrows crossing from right to left, and a tiny mosquito icon on each ship."),
  ch('c11a', C(.5, .5, 1.05), "The sunny deck of a 1640s wooden sailing ship at sea: a stickman sailor in a loose shirt and kerchief scoops water from an open wooden water barrel with a tin cup held in one hand, mosquitoes hovering over the barrel.", text=cap('Barbados and Yucatán, 1640s')))
N('L07', "The Spanish called him vómito negro: black vomit. English sailors called him Yellow Jack, perhaps after the yellow flag ships raised when they had fever on board.",
  ch('c12a', WL(), "A 1700s sailing ship anchored alone off a tropical harbour, a plain solid yellow pennant with no markings hanging from its mast; in the foreground on the quay two stickman harbour men in 1700s coats and tricorn hats stand apart, one pointing at the ship with one hand.", text=cap('Yellow Jack')))
K('L08', "Black vomit, Yellow Jack. I prefer the second one. It has style.",
  kg('c13a', C(.5, .45, 1.1), "Yellow Jack stands in front of a tall gilded mirror in a dim 1850s dressing room, straightening his black cravat with one gloved hand and admiring himself, his other hand at his side."))

# ---- WHAT HE DOES TO YOU
N('S01', "So what does he do to you? Three to six days after the bite: sudden fever, chills, a pounding headache and a terrible backache. For most people, that's it. After a few days, they get better.",
  dg('d06a', "A simple standing stickman outline with three numbered magnifier circles pointing to: (1) the head with pounding pain lines, (2) a thermometer at very high, (3) the lower back with jagged pain lines.", people=True, text=[label('What He Does to You', 960, 150, 72), cap('Fever, headache, backache')]),
  ch('c14a', C(.5, .5, 1.05), "A cramped 1800s ship's cabin lit by a swinging lantern: a stickman sailor in a striped shirt lies in a hammock holding his head with both hands, shivering, while a stickman shipmate in a cap sits apart on a sea chest, looking worried.", text=cap('Three to six days after the bite')))
N('S02', "But for about fifteen in every hundred, after a day of feeling better, the fever comes back. Much worse.",
  dg('d07a', "ONLY one simple line chart filling the whole page: a fever line rising, dipping down for a short calm stretch, then rising again much higher. No numbers.", text=[cap('The second wave')]))
N('S03', "Now he attacks the liver. The skin and eyes turn yellow. Patients bleed from the gums and the stomach, and vomit dark, old blood: the black vomit. Half of them die within about ten days.",
  dg('d08a', "A simple stickman body outline front view with two numbered magnifier circles: (1) a liver drawn in yellow with small cracks, (2) an eye with a yellow white.", people=True, text=[cap('The liver fails, the skin turns yellow')]),
  ch('c14b', W(), "A dim 1850s hospital ward lit by a candle: a stickman patient with a yellow-tinted round head lies weakly in an iron bed, a metal basin on a stool beside him, while a stickman nun in a black habit and white wimple stands apart, holding a wet cloth in one hand.", text=cap('Half of them die')))
N('S04', "But those who survive are immune for life. And that one fact shaped who lived and who died for centuries.",
  ch('c14c', C(.5, .5, 1.05), "A sunny 1850s street: a stickman man in a linen suit, recovered and smiling, walks past a shuttered house with a black cloth on its door, tipping his straw hat with one hand.", text=cap('Immune for life')))
K('S05', "First I let you think it's over. Then I come back for the second act. I do love a dramatic return.",
  kg('c15a', C(.5, .45, 1.1), "Yellow Jack steps out from between red velvet theatre curtains on an old wooden stage lit by footlights, one gloved arm raised in a grand theatrical gesture, his other hand on his chest, grinning."))

# ---- Philadelphia 1793
N('L09', "Port cities were his favourite stage. In seventeen ninety-three, he arrived in Philadelphia, then the capital of the United States. In about three months, some five thousand people died. Roughly one in ten.",
  ch('c16a', WL(), "A hot 1793 Philadelphia street of red-brick houses near the wharves: a stickman carter in a 1790s coat and tricorn hat leads a horse pulling a plain wooden cart, while a stickman gentleman in a 1790s coat stands apart in a doorway holding a handkerchief to his nose with one hand.", text=cap('Philadelphia, 1793')),
  dg('d09a', "ONLY a single row of ten simple stickman icons across the page: one drawn faded grey, nine drawn normal. Nothing else on the page.", people=True, text=[cap('About 1 in 10 died')]))
N('L10', "Twenty thousand people fled, among them President Washington and his government. Doctor Benjamin Rush bled his patients, which only made them weaker.",
  ch('c16b', W(), "A 1793 Philadelphia city gate road: a stickman family in 1790s clothes walks away from the city with bundles, the father carrying a trunk in both hands, the mother holding a small child's hand, a loaded horse cart beside them.", text=cap('20,000 fled')),
  ch('c16c', C(.5, .5, 1.05), "A 1793 sickroom with wooden shutters: a stickman doctor in a black 1790s coat and white wig holds a small white china bowl in one hand next to the arm of a stickman patient sitting up in bed, the patient looking pale and weak. Not gory.", text=cap('Dr Benjamin Rush')))
N('L11', "Rush believed Black people could not catch the fever, and asked the Free African Society for help. Richard Allen, Absalom Jones and many other Black Philadelphians nursed the sick and buried the dead. The belief was wrong. Many of them died too.",
  ch('c17a', W(), "A candlelit 1793 Philadelphia sickroom: a stickman man in a plain dark 1790s coat kneels beside a bed, giving a cup of water with one hand to a sick stickman patient, while a second stickman man in a dark coat stands apart by the door holding a lantern in one hand.", text=cap('Richard Allen and Absalom Jones')))
K('L12', "Vinegar, bonfires, cannon smoke. They tried everything. Except looking in the water barrel.",
  kg('c18a', C(.5, .45, 1.1), "Yellow Jack sits on an upturned rain barrel on a smoky 1793 street at night, a bonfire burning behind him, waving the smoke away from his face with one gloved hand, smirking, his other hand on his knee."))

# ---- Haiti
N('L13', "Then, Haiti. In eighteen-oh-two, Napoleon sent a large army to retake the French colony of Saint-Domingue, where enslaved people had risen up and won their freedom.",
  ch('c19a', WL(), "A tropical beach in 1802 with steep green mountains behind: rowing boats land on the sand, and three stickman French soldiers in 1802 dark-blue uniforms with white trousers and black bicorne hats wade ashore apart from each other, each holding a musket upright in one hand.", text=cap('Saint-Domingue, 1802')))
N('L14', "The Haitian army, led by Toussaint Louverture and later Jean-Jacques Dessalines, fought back and waited for the rainy season. Yellow fever tore through the French. Tens of thousands died, including their commander, General Leclerc.",
  ch('c19b', W(), "A 1802 Haitian mountain ridge in the rain: a stickman Haitian officer in a 1800s dark-blue coat with red facings and a bicorne hat stands on a rocky ledge looking down at the valley below, one hand resting on the hilt of a sword at his belt, palm trees around him.", text=cap('Waiting for the rains')),
  ch('c19c', C(.5, .5, 1.05), "A 1802 French army field hospital under palm-thatch roofs in the tropical rain: rows of cots, a stickman French soldier with a yellow-tinted round head lies on one cot under a blanket, while a stickman army surgeon in a dark coat stands apart holding a lantern in one hand.", text=cap('The fever tore through the French')))
N('L15', "In eighteen-oh-four, Haiti declared independence, the first nation born from a successful uprising of enslaved people. And Napoleon, his American plans in ruins, had already sold Louisiana to the United States.",
  ch('c20a', W(), "A sunny town square in Gonaïves in January 1804 with palm trees: a small crowd of stickman Haitian men and women in 1800s clothes cheer with raised arms, standing apart from each other; no flags.", text=cap('Haiti, 1804: independence')),
  dg('d10a', "A simple old-style map of North America with the huge territory west of the Mississippi River shaded in yellow and a small sailing ship icon near New Orleans.", text=[cap('1803: the Louisiana Purchase')]))
K('L16', "One nation freed, half a continent sold. Not bad for a mosquito.",
  kg('c21a', C(.5, .45, 1.1), "Yellow Jack stands beside an old wooden map table in a candlelit room, leaning over a large map of North America and tapping it with one gloved finger, grinning at the viewer, his other hand on the table edge."))

# ---- the American South
N('L17', "In the eighteen hundreds, he struck the American South again and again. In eighteen seventy-eight, an epidemic swept up the Mississippi River. In Memphis alone, more than five thousand people died, and most of the city fled.",
  ch('c22a', W(), "A crowded 1878 railway platform in Memphis with a steam train: a stickman father in a 1870s suit and bowler hat helps a stickman mother in a long bustled dress up the carriage steps, holding a suitcase in his other hand.", text=cap('Memphis, 1878')),
  dg('d11a', "A simple map of the Mississippi River from New Orleans in the south up to Memphis, with small yellow spots spreading upstream along the river and an arrow pointing north.", text=[cap('Up the Mississippi')]))
N('L18', "Nobody knew how he spread. Doctors blamed bad air from swamps and rotting rubbish, or the clothes and bedding of the sick. Cities burned tar barrels in the streets to clean the air.",
  dg('d12a', "Three numbered panels in one row: (1) wavy green smoke rising from a swamp, crossed out, (2) a pile of bedding and clothes, crossed out, (3) a small mosquito with a big question mark.", text=[cap('Bad air? Dirty sheets?')]),
  ch('c22b', C(.5, .5, 1.05), "A dark 1878 street at night: a tar barrel burns in the middle of the road with thick black smoke, while a stickman policeman in a 1870s uniform and helmet stands apart, holding a long iron poker in one hand.", text=cap('Burning tar to clean the air')))

# ---- Finlay, Reed, the volunteers
N('L19', "In eighteen eighty-one, a Cuban doctor, Carlos Finlay, said: it's the mosquito. For twenty years, almost nobody believed him.",
  ch('c23a', W(), "A 1881 study in Havana with tall shuttered windows and shelves of glass jars: a stickman doctor with small round glasses (eyes inside the lenses) and a dark suit holds up a glass jar with a mosquito inside in one hand, while a second stickman doctor in a frock coat stands apart, shaking his head with arms crossed.", text=cap('Carlos Finlay, 1881')))
N('L20', "Then, in nineteen hundred, the US Army sent Walter Reed and a commission to Havana. Volunteers slept for weeks in a closed hut full of the soiled sheets and clothes of yellow fever patients. None of them got sick.",
  ch('c24a', C(.5, .5, 1.05), "Inside a small closed wooden hut in 1900, dim and stuffy: two stickman soldier volunteers in white undershirts lie apart on two narrow cots, surrounded by heaps of crumpled dirty bedding and old clothes, one of them reading a book held in both hands.", text=cap('The dirty-sheets hut')),
  ch('c24b', W(), "A 1900 tent camp near Havana with palm trees: a stickman officer in a 1900 khaki army uniform, a campaign hat and small round glasses (eyes inside the lenses) stands apart outside a small wooden hut, writing in a notebook held in one hand.", text=cap('Walter Reed')))
N('L21', "Volunteers bitten by infected mosquitoes did get sick. The mosquito was the answer. A year later, an American nurse, Clara Maass, volunteered for the same kind of experiment. She died at twenty-five. Finlay had been right all along.",
  ch('c25a', C(.5, .5, 1.05), "A screened 1900 wooden hut with fine wire mesh windows: a stickman soldier volunteer in a white undershirt sits on a cot holding his bare arm out, while a stickman doctor in a white coat stands apart holding a small glass tube against the arm with one hand.", text=cap('The mosquito was the answer')),
  ch('c25b', W(), "A sunny 1901 Havana hospital veranda with arches: a stickman nurse in a long white uniform dress, a white apron and a small white nurse's cap stands calmly, rolling up her sleeve with one hand, her other hand holding the cuff.", text=cap('Clara Maass, 1901')))
K('L22', "They let my mosquitoes bite them. On purpose! Who does that?",
  kg('c26a', C(.5, .45, 1.1), "Yellow Jack stands in a screened wooden hut, staring wide-eyed and shocked at the viewer, one gloved hand pressed to his cheek, his other arm at his side, his hat pushed back."))

# ---- Gorgas, Havana and Panama
N('L23', "Once they knew, the fight was simple. William Gorgas and his teams emptied, covered or oiled every barrel and puddle in Havana. Within months, yellow fever was gone from the city.",
  ch('c27a', W(), "A sunny 1901 Havana courtyard: a stickman sanitary inspector in a 1900 khaki uniform and campaign hat pours a thin stream of oil from a metal can held in both hands into an open rain barrel, while a stickman woman in a long dress watches from a doorway.", text=cap('William Gorgas, Havana')),
  dg('d13a', "Three numbered steps in one row: (1) a barrel with a lid on it, (2) a puddle with a thin oil film, (3) a window with fine wire mesh screen.", text=[cap('Lids, oil and screens')]))
N('L24', "In Panama, the French had tried to dig a canal in the eighteen-eighties. Around twenty thousand workers died, many of yellow fever and malaria. The Americans brought in Gorgas, cleared out the mosquitoes, and in nineteen fourteen, the canal opened.",
  ch('c28a', WL(), "A muddy 1880s canal cutting in the Panama jungle in heavy rain: two stickman workers in shirts and wide hats stand apart in the mud, one swinging a pickaxe held in both hands, the other leaning on a shovel, exhausted; steam dredgers in the distance.", text=cap('Panama, 1880s')),
  ch('c28b', W(), "The Panama Canal locks in 1914 under a clear sky: a steamship moves slowly through the open lock gates, and a stickman lock worker in a white shirt and cap stands apart on the concrete wall, waving his cap in one hand.", text=cap('1914: the canal opens')))
K('L25', "Screens, oil, and lids on barrels. That's how they beat me? Lids!",
  kg('c29a', C(.5, .45, 1.1), "Yellow Jack stands in a sunny courtyard holding up a round wooden barrel lid in one gloved hand, glaring at it in disgust, his other hand on his hip."))

# ---- the vaccine
N('L26', "Then, in nineteen thirty-seven, Max Theiler created a vaccine called seventeen D. One shot protects for life. He won the Nobel Prize for it.",
  ch('c30a', C(.5, .5, 1.05), "A 1930s laboratory in New York with glass cabinets: a stickman scientist in a white coat holds up a small glass vaccine vial to the light with one hand, his other hand on a rack of chicken eggs on the bench.", text=cap('Max Theiler, 1937')),
  dg('d14a', "Three numbered icons in one row: (1) a small vaccine vial, (2) a single syringe, (3) a simple shield with a green tick.", text=[cap('One shot, protected for life')]))
N('L27', "Travellers to some countries still have to prove they've had it, with a vaccination certificate printed on a yellow card.",
  ob('c31a', "A modern travel desk: a small folded yellow vaccination booklet without readable writing lies open next to a passport and a pair of sunglasses on a wooden table, soft daylight.", modern=True, text=cap('The yellow card')))

# ---- WHAT HE LEAVES BEHIND
N('A01', "For survivors, he leaves weeks of exhaustion, and then lifelong immunity. He never comes back for them.",
  dg('d15a', "Three numbered panels in one row: (1) a simple bed with a tired stickman lying down, (2) a calendar with several weeks crossed out, (3) a simple shield with a green tick.", people=True, text=[label('What He Leaves Behind', 960, 150, 72), cap('Exhaustion, then immunity')]))
N('A02', "For the world, he left a free Haiti, the Louisiana Purchase, the Panama Canal, and a new rule of public health: to stop a disease, stop the insect that carries it.",
  dg('d16a', "Three numbered icons in one row: (1) a small island with palm trees and a rising sun, (2) a simple map of North America with a shaded middle, (3) a ship in a canal lock.", text=[cap('He redrew the map')]),
  ch('c32a', W(), "A 1910s Panama street: a stickman mosquito-control worker in a white shirt and cap walks apart along a row of houses with screened windows, carrying a metal oil can in one hand.", text=cap('Stop the insect, stop the disease')))
K('A03', "A country, a canal, half a continent. Admit it. I'm all over your maps.",
  kg('c33a', C(.5, .45, 1.1), "Yellow Jack sits in a leather armchair in a candlelit study beside a large old globe, spinning the globe with one gloved hand, grinning at the viewer, his other hand resting on the armrest."))

# ---- today
N('T01', "Today, he hasn't gone. He still lives in the forests of Africa and South America, among monkeys and mosquitoes. Every year, tens of thousands of people still die, most of them in Africa, even though one shot would protect them.",
  dg('d17a', "ONLY a simple world map filling the whole page: tropical Africa and northern South America shaded in yellow. Nothing else.", text=[cap('Still here')]),
  ch('c34a', C(.5, .5, 1.05), "A modern outdoor vaccination point under a tree in a West African village: a stickman nurse in a blue medical tunic gives an injection with one hand into the upper arm of a stickman young woman in a bright patterned dress, who holds her sleeve up; a cool box on a small table.", modern=True, text=cap('One shot would protect them')))
N('T02', "And his mosquito, Aedes aegypti, now lives in cities across the warm parts of the world. The same mosquito carries dengue and Zika.",
  ch('c35a', W(), "A modern tropical city rooftop with blue plastic water tanks and potted plants: a stickman man in a T-shirt and shorts puts a lid on a big plastic water tank with both hands, apartment buildings behind him.", modern=True, text=cap('Dengue, Zika, yellow fever')))
K('T03', "Every flower pot. Every old tyre full of rain. I'm still waiting.",
  kg('c36a', C(.5, .45, 1.1), "Yellow Jack crouches beside an old rubber tyre full of rainwater in a weedy modern backyard at dusk, dipping one gloved fingertip into the water and smiling at the viewer, his other hand resting on his knee."))

# ---- ending
N('L28', "For three hundred years, he decided the fate of cities, colonies and empires. He was beaten by a Cuban doctor nobody believed, volunteers who rolled up their sleeves, and a lid on a water barrel. But he's still out there, in the forest, waiting for a gap.",
  sh('c01a', C(.5, .5, 1.05)), sh('c19c', W()), sh('c25a', C(.5, .5, 1.05)), sh('c27a', W()),
  kg('c37a', C(.5, .45, 1.1), "Yellow Jack walks away along a misty jungle path at dusk, seen from behind in profile, his canary-yellow tailcoat swinging, his gloved hands clasped behind his back, a mosquito on his hat brim."))
N('L29', "Next time: the most contagious disease known to medicine. He helped topple an empire in the Americas, and he's making a comeback.",
  ch('c38a', C(.5, .5, 1.04), "A dark 1500s Aztec city at night by a lake with stepped temples, ominous: on the left third of the frame a single stickman Aztec man in a white cotton cloak sits weakly against a stone wall, his round head covered in small red spots; the right side of the frame is dark empty misty sky."))
HOLD(5.0, sh('c38a', O(), text=[label('NEXT TIME', 1380, 360, 110, style='title', pop=True, at=.2, len=4.6), label('SUBSCRIBE', 1380, 500, 64, at=.8, len=4.0)]))

# ---- extra cut-ins
EXTRA = {
  'L05': [(None, ob('c10b', f"An extreme close-up of {MOSQ} resting on a big green rainforest leaf, a drop of water beside it, dappled light.", text=cap('A forest mosquito')))],
  'S01': [(None, ch('c14d', W(), "A sunny 1800s tropical veranda: a stickman man in a white shirt sits in a cane chair, wrapped in a blanket despite the heat, shivering, while a stickman woman in a long dress stands apart holding a cup of tea in one hand.", text=cap('Chills in the heat')))],
  'L09': [(None, ch('c16d', C(.5, .5, 1.05), "The busy 1793 Philadelphia wharf with sailing ships: a stickman sailor in a striped shirt rolls a big wooden water barrel down a gangplank with both hands, while a stickman merchant in a tricorn hat stands apart watching.", text=cap('It came by ship')))],
  'L14': [(None, ob('c19d', "An abandoned 1802 French military camp in the tropical rain: empty tents, a stack of muskets and a fallen black bicorne hat in the mud, palm trees and mountains in the mist.", text=cap('General Leclerc died in 1802')))],
  'L17': [(None, ch('c22c', C(.5, .5, 1.05), "An empty 1878 Memphis street at noon with shuttered shops: a stickman doctor in a black frock coat and top hat walks alone carrying a leather medical bag in one hand.", text=cap('A city emptied')))],
  'L23': [(None, ob('c27b', "A sunny 1901 Havana patio with a row of wooden rain barrels, each covered with a tight wooden lid, and a window covered with fine wire mesh behind them.", text=cap('Lids on every barrel')))],
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
    json.dump(out, open(os.path.join(ROOT, 'tools/plague/ep12_frames_todo.json'), 'w'), indent=1); print(len(out), 'frames')

def beats():
    out = {'base': 'assets/plague/ep12/frames', 'keep_zoom': [], 'static': True, 'fade_in': .8, 'start': 0.0, 'lead': .45, 'gap': .6, 'max_shot': 3.2,
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
        if i: out['beats'].append({'vo': f'assets/plague/ep12/vo/{i}.wav', **({'gain': 1.05} if r == 'YELLOWJACK' else {}), 'shots': sl})
        else: out['beats'].append({'hold': t, 'shots': sl})
    json.dump(out, open(os.path.join(ROOT, 'tools/plague/ep12_beats.json'), 'w'), indent=1); print(len(out['beats']), 'beats')

# Set after the voice-over exists, from the real chapter boundaries.
MUSIC = [(0, 170, 'plague_a.mp3'), (166, 270, 'plague_b.mp3'), (266, 360, 'cholera_a.mp3'), (356, 'ALL', 'cholera_b.mp3')]

{'lines': lines, 'frames': frames, 'beats': beats}[sys.argv[1]]()
