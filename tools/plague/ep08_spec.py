"""Episode 8 (The ENTIRE History of Malaria): single source of truth. Same format as ep07_spec.py, built with the retention rules
from the start: static camera, a person in trouble in the first second, characters in almost every frame, natural captions.

  python3 tools/plague/ep08_spec.py lines   -> voice list (id|ROLE|text), roles NARRATOR / MALARIA
  python3 tools/plague/ep08_spec.py frames  -> tools/plague/ep08_frames_todo.json
  python3 tools/plague/ep08_spec.py beats   -> tools/plague/ep08_beats.json (for beats.py)
"""
import sys, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
K_SHEET = 'e059fb2c-82c5-4843-b690-a6ff18340477'   # channel/plague/sheets/malaria_a.jpg (the Marsh Count), Higgsfield upload
STYLE = ("2D animated history explainer frame, 16:9, no text. Hand-drawn ink illustration, clean black outlines, muted swamp-green, ochre and sepia palette "
         "with sickly yellow accents and warm lamp light. Not gory.")
MODERN = ("2D animated history explainer frame, 16:9, no text. Hand-drawn ink illustration, clean black outlines, the same muted green, ochre and sepia palette, "
          "soft natural daylight. The setting is modern (2000s-2020s): no lanterns, no oil lamps, no candles, nothing old-fashioned. Not gory.")
SN = ("Humans are simple STICKMEN: plain white round head, two dot eyes, no nose, no beard, thin black stick arms and stick legs, small black mitten hands, "
      "dressed exactly as described for this scene and era; anyone wearing glasses has his two dot eyes INSIDE the lenses and no other eyes. "
      "Only the few figures described, standing apart, never overlapping; each has exactly two arms and two hands attached to its sleeves; "
      "hands are empty unless an object is described; nothing floating; no flags; no readable text.")
KING = ("Malaria exactly as on the attached sheet, 'the Marsh Count': a tall, very thin 18th-century nobleman with sallow yellow-green skin, red-rimmed glittering eyes, "
        "a sly thin smile, a long thin needle-like nose like a mosquito's proboscis, black hair tied back with a ribbon, a black tricorn hat, a tattered dark marsh-green "
        "embroidered frock coat, a lace cravat, a ragged fur-trimmed cloak around his shoulders, and two large translucent veined mosquito wings on his back. "
        "He holds AT MOST ONE object at a time, his other hand empty and clearly attached to its own arm. Exactly ONE of him, with exactly two arms and two hands with normal-length fingers.")
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
def K(i, t, *s): B.append((i, 'MALARIA', t, list(s)))
def HOLD(sec, *s): B.append((None, None, sec, list(s)))

INDIA = "a whitewashed 1890s British army barracks ward in southern India with wooden shutters, a ceiling fan made of cloth (a punkah) and bright hot sunlight outside"
ROSS = "a stickman army doctor with small round glasses, a white 1890s tropical uniform jacket and khaki trousers"

# ---- cold open: the soldier's chills, then Ross and the mosquito (Secunderabad, 20 August 1897)
N('C01', "A young soldier is shaking so hard his teeth rattle. It's thirty-five degrees outside. He's buried under three blankets, and he's freezing. In a few hours, he'll be burning with fever. And in two days, it will all happen again.",
  ch('c01a', C(.5, .5, 1.05), f"Close medium shot inside {INDIA}: ONLY ONE figure in the whole picture, a young stickman soldier lying on an iron camp bed, buried under three grey wool blankets pulled up to his chin, shaking violently, little shiver lines around him, his dot eyes squeezed shut, teeth chattering. Nobody else in the room: no officers, no doctors, no servants, no other patients.", text=cap("It's 35 degrees, and he's freezing")),
  ch('c01b', W(), f"Inside {INDIA}: the same young stickman soldier now sits up on his iron camp bed with the blankets thrown off, in a damp white vest, flushed red cheeks and heat lines over his head, fanning his face with one hand, the other hand on the mattress.", text=cap('Then the fever')),
  ch('c01c', WR(), f"Inside {INDIA}: a stickman army nurse in a long grey 1890s dress, a white apron and a white cap stands beside the iron camp bed of the sleeping young stickman soldier, holding a glass thermometer up to the light with one hand, looking worried, her other hand at her side.", text=cap('And in two days, again')))
N('C02', "Nobody knows what causes it. In a hot little lab nearby, an army doctor named Ronald Ross has spent two years cutting open mosquitoes, looking for the answer. Secunderabad, India. August, 1897.",
  ch('c02a', W(), f"A cramped hot 1890s field laboratory with a wooden table, glass jars with gauze lids holding mosquitoes, and a brass microscope by an open window with bright sunlight: {ROSS} sits hunched over a brass microscope that stands on the table IN FRONT of him, peering into the eyepiece; BOTH of his arms come straight forward from his own shoulders: one hand turns the focus knob on the near side of the microscope, the other hand rests flat on the table beside the glass slide. No arm reaches around or behind the microscope. No armband, no red cross. Sweat drops on his head." + LAMPS, text=cap('Ronald Ross')),
  ch('c02b', WL(), f"A dusty 1890s Indian army cantonment street at midday with low whitewashed bungalows with verandas, palm trees and a pale hot sky: {ROSS} walks along the road carrying a small glass jar with a gauze lid in one hand, the other hand shading his eyes from the sun.", text=cap('Secunderabad, India — August 1897')))
N('C03', "On the twentieth of August, in the stomach of one mosquito, he finally sees them. Tiny round cells that shouldn't be there. The killer had been hitching a ride all along.",
  dg('d01a', "A microscope view: a bright round field showing the pale stomach wall of a mosquito, and on it a few small round dark-ringed cysts, each one circled with a small drawn ring and numbered (1), (2).", text=[cap("Inside a mosquito's stomach")]),
  ch('c03a', C(.5, .5, 1.05), f"The cramped hot 1890s field laboratory: {ROSS} leans back from the brass microscope with both hands raised in triumph, mouth open in a delighted shout; jars of mosquitoes on the table." + LAMPS, text=cap('20 August 1897')))
K('C04', "Took them long enough. I've been flying for millions of years.",
  kg('c04a', C(.5, .45, 1.1), "Medium shot: the Marsh Count stands knee-deep in mist in a dark tropical swamp at dusk, wings spread, with a small cloud of tiny mosquitoes circling his tricorn hat; he smiles slyly at the viewer, one hand raised with a single finger lifted, the other hand holding his cloak closed."))
HOLD(4.6, kg('c05a', O(), "Title shot: the Marsh Count stands on the left third of the frame on a misty moonlit marsh among reeds and dead trees, wings half open, both hands empty and resting on a thin black walking cane planted in front of him; dark empty mist on the right side.")
     | {'text': [label('MALARIA', 1300, 330, 130, style='title', pop=True, at=.15, len=4.2), label('THE MARSH FEVER', 1300, 470, 72, style='title', color=[214, 200, 120], at=.5, len=3.9)],
        'sfx': [{'kind': 'boom', 'at': .1, 'gain': .8}]})

# ---- who is he
N('L01', "So who is he? Not a virus. Not a bacterium. Malaria is a parasite: a tiny single-celled creature called Plasmodium. And he can't travel on his own.",
  dg('d02a', "Scale comparison: a tiny teardrop-shaped single-celled parasite with a dark nucleus (1), next to a much LARGER round red blood cell (2) about five times its size."),
  kg('c06a', C(.5, .45, 1.1), "The Marsh Count stands by a still swamp pool at dusk, bending to peer through a brass magnifying glass held in one hand at a single drop of water on a lily leaf, amused; his other hand behind his back.", text=cap('Plasmodium, a single-celled parasite')))
N('L02', "He needs a ride: a mosquito called Anopheles. And only the females bite. They need blood to make their eggs.",
  dg('d03a', "Two large mosquitoes side by side: (1) a male mosquito with feathery antennae sipping from a flower, (2) a female Anopheles mosquito with her body tilted up, a tiny drop of red in her belly, and a small cluster of eggs drawn beside her.", text=[cap('Only the females bite')]),
  ch('c07a', WL(), "A village at dusk in 1890s India beside a flooded rice paddy, mud-brick huts with thatched roofs, an orange sky: a stickman farmer in a white dhoti and a simple white cotton shirt sits on a low wooden stool outside his hut, slapping at a mosquito on his forearm with his other hand.", text=cap('She bites at dusk and at night')))
N('L03', "When she bites, he slips into your blood and goes straight to the liver. There he hides and multiplies, quietly, for a week or two.",
  dg('d04a', "A simple standing stickman outline: (1) a mosquito biting the arm, (2) a dotted arrow running through the blood to the liver, (3) the liver drawn large with many tiny dots multiplying inside it.", people=True, text=[cap('First, he hides in the liver')]))
K('L04', "These wings are just for show. The real work is done by my air force.",
  kg('c08a', C(.5, .45, 1.1), "The Marsh Count stands on a rotten wooden jetty over a swamp at sunset, conducting a huge swarm of mosquitoes in the sky like an orchestra with one raised empty hand, his other hand resting on his hip, smiling proudly."))
N('L05', "Then thousands of new parasites burst out of the liver and invade your red blood cells. Inside each cell he multiplies again, until it bursts, and the new ones invade more cells. Over and over.",
  dg('d05a', "A circular cycle drawn with arrows: (1) a parasite entering a round red blood cell, (2) the parasite multiplying inside the cell, (3) the cell bursting and releasing many new parasites, (4) an arrow back to new red blood cells.", text=[cap('Into the blood cells, over and over')]),
  ob('d06a', "A microscope view: a bright round field full of pale pink round red blood cells, several of them with tiny purple ring shapes inside.", text=cap('What a doctor sees under the microscope')))
N('L06', "And when another mosquito bites you, she drinks him up with your blood, and carries him to the next person.",
  dg('d07a', "A big circle of arrows: (1) a stickman lying in bed, (2) a mosquito flying away from him, (3) a second stickman being bitten, then the arrow returns to (1).", people=True, text=[cap('Human, mosquito, human')]),
  ch('c09a', W(), "A 1890s Indian village hut at night lit by a small oil lamp: a stickman mother in a dark red cotton sari sits beside a sleeping child on a woven rope bed, waving a round palm-leaf fan over the child with one hand to keep mosquitoes away, her other hand on her knee.", text=cap('Every bite passes him on')))
K('L07', "Human, mosquito, human. A beautiful little arrangement, don't you think?",
  kg('c10a', C(.5, .45, 1.1), "The Marsh Count lounges in a hammock strung between two palm trees over a misty swamp at night, both hands folded behind his head, wings draped over the edge, smiling contentedly."))

# ---- origin
N('L08', "But where did he come from? Malaria parasites are ancient. They infect birds, lizards, monkeys and apes. The deadliest kind in humans, Plasmodium falciparum, most likely jumped to us from gorillas in Africa.",
  dg('d08a', "A single row of simple animal icons, numbered: (1) a bird, (2) a lizard, (3) a monkey, (4) a gorilla; then a bold arrow from the gorilla to a simple stickman.", people=True, text=[cap('Most likely from gorillas')]),
  ch('c11a', WL(), "The edge of an African rainforest at dusk beside a muddy stream, mosquitoes over the water: two stickman hunter-gatherers wearing simple plain brown leather loincloths and nothing else (bare white stick bodies) crouch apart by the water, one of them filling a round gourd with both hands, the other standing and pointing at a gorilla half-hidden among the distant trees.", text=cap('Africa, long before history')))
N('L09', "When people began to farm, clearing forests and digging ponds and ditches, the mosquitoes followed. He spread across Africa, then into Asia and Europe.",
  ch('c11b', W(), "An early farming village thousands of years ago with round mud huts and a field of millet: two stickman farmers in plain undyed linen tunics dig an irrigation ditch with wooden hoes, standing apart, a pool of still water beside them with a few mosquitoes above it.", text=cap('Farms meant still water')),
  dg('d09a', "A simple world map with dotted arrows spreading out from Africa into Asia and Europe, with tiny mosquito icons riding along the arrows.", text=[cap('Out of Africa')]))
N('L10', "We have found his DNA in Egyptian mummies, including the boy pharaoh, Tutankhamun.",
  ch('c11c', C(.5, .5, 1.05), "A modern bright laboratory: a stickman scientist in a white lab coat, blue gloves, a hair cap and a face mask leans over an ancient wrapped Egyptian mummy lying on a steel table, taking a tiny sample with long tweezers held in one hand.", modern=True, text=cap('Even Tutankhamun had him')))
N('L11', "He killed for so long that he changed our DNA. In parts of Africa, the gene for sickle-cell disease survived, because one copy of it protects against him.",
  dg('d10a', "Two red blood cells side by side: (1) a normal round red blood cell, (2) a curved sickle-shaped red blood cell with a small shield drawn beside it.", text=[cap('The sickle-cell gene: a shield')]))
K('L12', "I didn't just kill humans. I rewrote them.",
  kg('c12a', C(.5, .45, 1.1), "The Marsh Count sits at a desk in a dark candlelit library, writing with a long quill pen in a huge open book, smiling, his other hand flat on the page."))

# ---- WHAT HE DOES TO YOU
N('S01', "So what does he do to you? It begins with the cold. You shiver so hard your teeth chatter, under blankets, in the heat.",
  dg('d11a', "A single stickman wrapped in a blanket, shaking, with blue shiver lines around him and a thermometer beside him, under a big hot sun.", people=True, text=[label('What He Does to You', 960, 150, 72), cap('First, the chills')]),
  ch('c13a', W(), "A sunny courtyard of a mud-brick house in 1900s West Africa: a stickman man in a long pale cotton robe sits on a wooden bench wrapped tightly in a striped wool blanket, shivering, while a stickman woman in a bright patterned wrap dress stands apart in the doorway, looking at him worriedly, hands clasped.", text=cap('Shaking in the heat')))
N('S02', "Then the hot stage. A fever of forty degrees, a pounding headache, vomiting. Then come the sweats, soaking everything. And a few hours later, you feel almost fine.",
  dg('d12a', "Three numbered panels in one row of the same stickman in bed: (1) blue and shivering under a blanket, (2) red with heat lines over his head, (3) dripping with sweat drops, the sheets soaked.", people=True, text=[cap('Cold, then hot, then soaked in sweat')]),
  ch('c13b', C(.5, .5, 1.05), "A 1900s West African mud-brick room with a small window: a stickman man in a damp white shirt lies on a low bed, sweat drops on his head, while a stickman woman in a patterned wrap dress kneels apart beside him, wiping his forehead with a wet cloth in one hand.", text=cap('Then the sweats')))
N('S03', "Until it starts again. Every second or third day, as a new wave of blood cells bursts. The Romans had names for these fevers: tertian and quartan.",
  dg('d13a', "A single row of seven blank calendar sheets; on sheets 1, 3, 5 and 7 a small red thermometer icon, the others empty; circled digits 1 and 3 under the first and third sheets.", text=[cap('Every second or third day')]))
N('S04', "He destroys so many red blood cells that you turn pale and weak. Your spleen swells. And the deadliest kind can clog the tiny blood vessels of the brain. Coma. Death.",
  dg('d14a', "A simple standing stickman outline with three numbered magnifier circles pointing to: (1) the face, drawn pale, (2) the left side of the belly, with a swollen spleen, (3) the head, with tiny blood vessels blocked by dots.", people=True, text=[cap('Pale, weak, a swollen spleen')]),
  ch('c13c', C(.5, .5, 1.05), "A dim 1900s mission hospital ward at night lit by one oil lamp: a stickman patient lies very still in an iron bed with his eyes closed, while a stickman nurse in a long white dress and a white cap sits apart on a chair beside him, holding his wrist to check his pulse.", text=cap('When he reaches the brain')))
N('S05', "Children under five suffer the most. Their bodies haven't yet learned to fight back.",
  ch('c13d', W(), "A modern rural health clinic in Africa with a corrugated roof, a wooden bench and a bright window: a stickman mother in a colourful patterned dress and a headscarf sits on the bench holding a small feverish child with flushed cheeks in both arms, while a stickman nurse in light blue scrubs crouches apart in front of them, looking at the child.", modern=True, text=cap('Children suffer the most')))
K('S06', "Cold. Hot. Wet. Repeat. I do love a good routine.",
  kg('c14a', C(.5, .45, 1.1), "The Marsh Count stands in a dim swamp, wrapped tightly in his fur-trimmed cloak with one hand, pretending to shiver, while fanning himself with a black lace fan held in his other hand, smirking."))

# ---- ancient world
N('L13', "People have described his fevers for thousands of years. Ancient Chinese and Indian texts, and the Greek doctor Hippocrates, wrote about regular fevers and swollen spleens. And they all noticed something: it was worse near marshes.",
  ch('c15a', W(), "An ancient Chinese study with paper screens and a low wooden desk: a stickman physician in a long dark blue Han-dynasty robe and a small black cap kneels at the desk, writing with a brush on a long roll of bamboo strips.", text=cap('Ancient China')),
  ch('c15b', WL(), "The edge of a reedy marsh in ancient Greece on a hazy summer evening, with a white stone house behind: a stickman physician in a white Greek chiton points at the misty marsh with one hand, while a sick stickman villager in a brown tunic sits apart on a rock, hugging himself and shivering.", text=cap('Worse near the marshes')))
N('L14', "Ancient Rome was surrounded by marshes, and he loved it there. The Romans even built temples to Febris, the goddess of fever, and prayed for her mercy.",
  ch('c16a', C(.5, .5, 1.05), "A small ancient Roman temple interior with marble columns and a stone altar with a little flame: a stickman Roman man in a white toga lays a small bunch of flowers on the altar with both hands, head bowed, while a pale stickman woman in a long Roman stola stands apart behind him, wrapped in a shawl.", text=cap('A temple to Febris, goddess of fever')),
  ch('c16b', WR(), "The flat marshy countryside outside ancient Rome with reeds, still pools and a long stone aqueduct in the distance: a stickman Roman farmer in a short brown tunic wades through the shallow marsh leading an ox, mosquitoes over the water.", text=cap('The marshes around Rome')))
N('L15', "Centuries later, Italians blamed the foul air that rose from the swamps at night. Mala aria. Bad air. That's where his name comes from.",
  ch('c16c', C(.5, .5, 1.05), "An 18th-century Italian farmhouse at night beside a misty marsh, green fog creeping towards it: a stickman man in a white shirt and a brown waistcoat leans out of a window, pulling the wooden shutters closed with both hands, looking warily at the fog.", text=cap("Mal'aria: bad air")))
K('L16', "Bad air. They named me after a smell. How rude.",
  kg('c17a', C(.5, .45, 1.1), "The Marsh Count stands among reeds in green night fog, eyes closed, breathing in deeply with a pleased smile, one empty hand on his chest, the other hand at his side."))
N('L17', "He may have killed Alexander the Great at thirty-two. He killed popes and crusaders, and the poet Dante. Whole armies marching into his marshes simply melted away.",
  ch('c18a', W(), "A palace bedroom in ancient Babylon with tall painted columns and hanging curtains: a young stickman king in a white Greek tunic with a thin gold band on his head lies on a couch with heat lines over his head, while a stickman soldier in a bronze Greek helmet and red cloak stands apart by the door, head lowered.", text=cap('Alexander the Great, perhaps')),
  ch('c18b', WL(), "A misty marsh road near Ravenna in 1321, with a medieval church tower in the distance: a thin stickman poet in a long red medieval robe and a red hood with a laurel wreath walks slowly along the road, hugging himself as if cold.", text=cap('Dante, 1321')),
  ch('c18c', C(.5, .5, 1.05), "A medieval army camp beside a marsh at dawn with a few tents: two stickman crusaders in chainmail and white tunics sit apart on the ground wrapped in blankets, shivering, their helmets lying beside them.", text=cap('Armies melted away')))

# ---- the bark
N('L18', "Then, in the 1600s, Jesuit missionaries in Peru learned of a bitter bark from the cinchona tree. Ground into powder and mixed with wine, it stopped the fevers.",
  ch('c19a', W(), "A green Andean mountain forest in the 1600s with mist in the valleys: a stickman Jesuit priest in a plain black cassock and a wide black hat stands apart watching, while a stickman Quechua man in a red woven poncho and a knitted cap peels a long strip of reddish bark from a cinchona tree with both hands.", text=cap('Peru, 1600s')),
  dg('d16a', "Four numbered steps in one row: (1) a cinchona tree, (2) strips of reddish bark, (3) a stone mortar with brown powder, (4) a cup of red wine.", text=[cap('Bark, powder, wine')]))
N('L19', "In Europe, it was called Jesuit's bark. Some Protestants refused to take a Catholic cure. Legend says Oliver Cromwell was one of them, and he died of a fever in 1658.",
  ch('c19b', C(.5, .5, 1.05), "A 1650s English bedroom with dark wood panelling and a curtained four-poster bed, lit only by two plain wax candles in simple brass candlesticks (no oil lamps, no glass lamp chimneys, no lanterns): a stickman man in a plain white nightshirt sits up in bed raising one hand to refuse, while a stickman doctor in a black 1650s coat and a wide white collar stands apart, holding out a small cup in one hand." + LAMPS, text=cap('Oliver Cromwell, 1658')))
N('L20', "In 1820, two French chemists, Pelletier and Caventou, pulled the active ingredient out of the bark: quinine.",
  ch('c20a', W(), "An 1820 Paris pharmacy laboratory with shelves of glass jars and a brick furnace: two stickman chemists in dark tailcoats and high white collars stand apart at a wooden bench, one holding up a small glass flask of white crystals to the window light, the other leaning on the bench watching.", text=cap('Quinine, 1820')))
N('L21', "Quinine was so bitter that British officers in India mixed it with soda and sugar into tonic water, then added gin to help it go down. That, the story goes, is how the gin and tonic was born.",
  ch('c20b', C(.5, .5, 1.05), "A shady veranda of an 1870s colonial bungalow in India with wicker chairs and potted palms: a stickman British officer in a white uniform and a white pith helmet sits in a wicker chair holding a tall glass of fizzy drink in one hand, pulling a face at the bitter taste.", text=cap('The gin and tonic')),
  dg('d17a', "A recipe in one row: (1) a small bottle of quinine powder, (2) a soda water siphon, (3) a sugar bowl, (4) a bottle of gin, then an arrow to a tall glass with ice and a slice of lime.", text=[cap('Medicine you could drink')]))
K('L22', "They fought me with cocktails. I have never been so insulted.",
  kg('c21a', C(.5, .45, 1.1), "The Marsh Count stands at the counter of an empty dim colonial bar, holding one tall glass of gin and tonic at arm's length with one hand and glaring at it in disgust, his other hand on the counter."))
N('L23', "Quinine let European armies push deep into West Africa, a coast they had called the white man's grave. The bark that saved lives also helped build empires.",
  ch('c22a', WL(), "A wide brown river through dense African rainforest in the 1880s: two stickman European explorers in khaki jackets and white pith helmets stand apart at the front of a small wooden steam launch, one of them looking through a brass telescope.", text=cap("The white man's grave")))

# ---- Laveran, Ross, Grassi
N('L24', "But what was he? In 1880, in Algeria, a French army doctor, Alphonse Laveran, looked at the blood of a feverish soldier and saw tiny creatures wriggling inside the red cells. Hardly anyone believed him.",
  ch('c23a', W(), "An 1880 French military hospital room in Algeria with white walls, arched windows and bright North African sunlight: a stickman army doctor in a dark blue French army coat and a red kepi on the table beside him looks into a brass microscope, while a feverish stickman soldier sits apart on a bed in the background, wrapped in a blanket." + LAMPS, text=cap('Alphonse Laveran — Algeria, 1880')),
  ob('d18a', "A microscope view: a bright round field with pale pink red blood cells, one of them with a dark crescent-shaped parasite inside, and beside it a small round body with several long thin wriggling threads coming out of it.", text=cap('Creatures inside the blood')))
N('L25', "Then Ross found him inside the mosquito, and proved the whole cycle in birds. In Italy, a team led by Giovanni Battista Grassi proved it in humans. The two men fought bitterly over the credit. Ross won the Nobel Prize in 1902.",
  dg('d19a', "A circle of arrows: (1) a small sparrow, (2) a mosquito biting it, (3) the mosquito biting a second sparrow, then back to (1).", text=[cap('Ross proved it in birds')]),
  ch('c24a', W(), "An 1898 Italian laboratory in Rome with tall windows and glass jars with gauze lids full of mosquitoes: a stickman scientist in a dark three-piece suit, holds up one jar to the light with one hand.", text=cap('Giovanni Battista Grassi, Rome')),
  ch('c24b', C(.5, .5, 1.05), "A grand 1900s academic hall with tall windows and portraits without faces: two stickman scientists in dark frock coats stand back to back a few steps apart, each with arms crossed and nose in the air, refusing to look at each other.", text=cap('A bitter fight for the credit')))
K('L26', "Two great scientists fighting over who discovered me. I was flattered.",
  kg('c25a', C(.5, .45, 1.1), "The Marsh Count sits alone in the front row of an empty old lecture hall with wooden benches, slowly clapping his two empty hands, smiling smugly."))

# ---- Panama
N('L27', "Meanwhile in Panama, the French were trying to dig a canal. Malaria and yellow fever killed around twenty thousand workers, and the French gave up.",
  ch('c26a', W(), "A muddy 1880s canal construction site cut through green Panama jungle in heavy humid heat, with a steam excavator and rail wagons behind: two stickman workers in loose shirts and straw hats stand apart in the mud with shovels, one of them wiping his forehead with his sleeve.", text=cap('Panama, 1880s')),
  dg('d20a', "ONLY a simple map filling the whole page and nothing else: the narrow isthmus of Panama between two oceans, a dotted line for the canal route across it, and many small cross icons along the line. No circles, no vignettes, no pictures around the map, no panels.", text=[cap('About 20,000 dead')]))
N('L28', "When the Americans tried again in 1904, a doctor named William Gorgas went after the mosquitoes. He drained swamps, poured oil on ponds, and put screens on every window. The canal opened in 1914.",
  ch('c26b', WL(), "A jungle pond in 1905 Panama: a stickman sanitation worker in a work shirt and a wide straw hat sprays oil onto the water from a metal sprayer can, while a stickman doctor in a white linen suit and a white hat, stands apart watching with his hands behind his back.", text=cap('William Gorgas')),
  dg('d21a', "Three numbered icons in one row: (1) a ditch draining a swamp, (2) an oil can pouring a film onto a pond, (3) a window covered with a fine wire screen.", text=[cap('Drain, oil, screen')]),
  ch('c26c', W(), "A wide canal with concrete locks in green Panama hills in 1914, a steamship with two funnels gliding through: two stickman workers in shirts and caps stand apart on the canal bank, one waving his cap in the air.", text=cap('Opened in 1914')))
K('L29', "Panama was one of my finest projects. Until that Gorgas fellow ruined it.",
  kg('c27a', C(.5, .45, 1.1), "The Marsh Count sits sulking on a muddy riverbank beside a drained, dried-up pond in the jungle, chin in one hand, his other hand resting on his knee."))

# ---- DDT and the eradication dream
N('L30', "After the Second World War came a new weapon: DDT. In 1955, the World Health Organization set out to wipe malaria off the planet. Teams sprayed the walls of millions of homes.",
  ch('c28a', W(), "A village of mud-walled houses in the 1950s under a hot sun: a stickman spray worker in white overalls and a cloth cap sprays the outside wall of a house with a metal hand-pump sprayer tank on his back, while a stickman villager in a simple shirt and shorts stands apart in the doorway watching.", text=cap('Millions of homes sprayed')),
  dg('d22a', "ONLY a simple world map filling the whole page and nothing else: North America and Europe shaded pale with a small green tick on each, Africa south of the Sahara and South Asia shaded dark. No pictures above or below the map, no extra panels, no rows, no objects.", text=[cap('The plan: wipe him out')]))
N('L31', "He vanished from the United States, from Europe, from much of Asia. Sri Lanka got down to just seventeen cases in a whole year.",
  dg('d23a', "ONLY one simple line chart filling the whole page and nothing else: a thick line starting high on the left and falling steeply almost to the bottom on the right; a tiny island icon in the top right corner. No pictures above the chart, no panels, no rows, no numbers.", text=[cap('Sri Lanka, 1963: just 17 cases')]))
N('L32', "But the mosquitoes became resistant to DDT, the money ran out, and the spraying stopped. Within a few years, Sri Lanka was back to half a million cases. In 1969, the dream of eradication was abandoned.",
  dg('d24a', "A simple line chart with no numbers: a line that falls to almost nothing in the middle, then shoots steeply back up to the top on the right, with a small mosquito icon at the top.", text=[cap('Back to half a million cases')]),
  ch('c28b', C(.5, .5, 1.05), "A 1960s village house with a rusty, abandoned hand-pump sprayer tank leaning against the mud wall: a stickman villager in a simple shirt sits on the doorstep wrapped in a blanket, shivering, with mosquitoes in the evening air.", text=cap('The spraying stopped')))
K('L33', "They thought they'd won. I just took a little holiday.",
  kg('c29a', C(.5, .45, 1.1), "The Marsh Count steps off a small wooden rowing boat onto a tropical jetty at sunset, carrying one old leather suitcase in one hand, tipping his tricorn hat with the other, grinning."))

# ---- Tu Youyou
N('L34', "Worse, the parasite was learning to survive the drugs. During the Vietnam War, he was killing soldiers on both sides. So in 1967, China launched a secret project to find a new cure.",
  ch('c30a', W(), "A dense green jungle in the 1960s: a stickman soldier in a plain olive-green uniform with no insignia lies in a hammock strung between two trees, shivering under a thin blanket, while a stickman medic in the same plain uniform kneels apart beside him holding a canteen in one hand.", text=cap('Vietnam, 1960s')),
  ch('c30b', WL(), "A simple 1960s Chinese laboratory with plain walls, wooden benches, glass flasks and bundles of dried herbs: two stickman scientists in white lab coats work apart at the bench, one weighing dried leaves on a small scale, the other reading a notebook.", text=cap('Project 523')))
N('L35', "A scientist named Tu Youyou searched through more than two thousand old recipes. In a book written sixteen hundred years ago, she found one for fevers: soak sweet wormwood in cold water, and drink the juice.",
  ch('c31a', C(.5, .5, 1.05), "A 1960s Chinese library room with stacks of old string-bound books: a stickman woman scientist with short straight black hair and a white lab coat sits at a desk reading an ancient thread-bound Chinese book, holding it open with both hands.", text=cap('Tu Youyou')),
  dg('d25a', "Three numbered steps in one row: (1) a feathery sweet wormwood plant, (2) its leaves soaking in a bowl of cold water, (3) green juice squeezed into a small cup.", text=[cap('A 1,600-year-old recipe')]))
N('L36', "Cold water, not boiling. That was the clue: heat destroyed the medicine. In 1972, her team isolated artemisinin. It has saved millions of lives, and in 2015, Tu Youyou won the Nobel Prize.",
  ch('c31b', W(), "The simple 1960s-70s Chinese laboratory: a stickman woman scientist with short straight black hair and a white lab coat holds up a small glass flask of clear liquid to the window light with one hand, smiling, her other hand on the bench.", text=cap('Artemisinin, 1972')),
  ch('c31c', C(.5, .5, 1.05), "A grand modern concert hall stage with blue lighting and flowers: an elderly stickwoman with short grey hair in a dark jacket holds a gold medal in a small open case with both hands, smiling, while a stickman man in a black tailcoat stands apart, applauding.", modern=True, text=cap('Nobel Prize, 2015')))
K('L37', "Beaten by a weed. A common little weed!",
  kg('c32a', C(.5, .45, 1.1), "The Marsh Count kneels in a sunny field, glaring furiously at a single small feathery sweet wormwood plant growing in front of him, both empty hands clenched into fists on his knees."))

# ---- WHAT HE LEAVES BEHIND
N('A01', "And for those who survive? People who catch him again and again build up some protection, but it fades if they move away. Some kinds hide in the liver and wake up months or even years later. And children who survive can be left with anaemia and damage to the brain.",
  dg('d26a', "Three numbered panels in one row: (1) a stickman holding a small cracked shield, (2) a liver with a few sleeping parasites and a calendar beside it, (3) a small pale stickman child sitting on a chair.", people=True, text=[label('What He Leaves Behind', 960, 150, 72), cap('He can wake up years later')]),
  ch('c33a', W(), "A modern family kitchen in an East African town with bright daylight: a stickman man in a short-sleeved shirt sits at the table wrapped in a blanket, shivering, while a stickman woman in a patterned dress stands apart holding a glass of water out to him.", modern=True, text=cap('Back again, years later')))
N('A02', "For the world, he left more than graves. The sickle-cell gene. Quinine and tonic water. The Panama Canal. Screens on our windows and nets over our beds. And the twentieth of August: World Mosquito Day, in honour of Ronald Ross.",
  dg('d27a', "Four numbered icons in one row: (1) a sickle-shaped red blood cell, (2) a tall glass of tonic water with lime, (3) a steamship in a canal lock, (4) a bed under a mosquito net.", text=[cap('He left more than graves')]),
  ch('c33b', C(.5, .5, 1.05), "A simple modern bedroom at night with a soft lamp: a stickman mother in a cotton dress tucks the edge of a white mosquito net under the mattress of a bed with both hands, where a small stickman child lies asleep inside the net; the child is a simple stickman too, with a plain white round head, two dot eyes, no hair, no nose, no mouth.", modern=True, text=cap('Nets over our beds')))
K('A03', "Every net, every screen, every bitter drink. That's my portrait, really.",
  kg('c34a', C(.5, .45, 1.1), "The Marsh Count stands in an old gilded picture frame hanging on a dark wall, posing proudly as if he were a painted portrait, one hand on his chest, the other hand empty at his side."))

# ---- today
N('T01', "Today, he still infects about two hundred and fifty million people a year, and kills around six hundred thousand. Most of them are children under five, in Africa.",
  dg('d28a', "ONLY a simple world map filling the whole page: Africa south of the Sahara shaded dark red, parts of South Asia and South America shaded lighter, other regions pale. Nothing else, no pictures, no rows of panels.", text=[cap('About 600,000 deaths a year')]),
  ch('c35a', W(), "A modern rural clinic in Africa with a bright window and a wooden table: a stickman nurse in light blue scrubs pricks the finger of a small child sitting on a stickman mother's lap; the mother in a patterned dress holds the child with both arms; only these three figures, each adult with exactly two arms.", modern=True, text=cap('Most are children under five')))
N('T02', "But we are fighting back. Bed nets treated with insecticide have saved millions of lives. A rapid test takes about fifteen minutes. And in 2021, the first malaria vaccine was recommended, with a second following in 2023.",
  ch('c35b', WL(), "A sunny modern village in Africa: a stickman health worker in a green polo shirt hands a folded blue mosquito net in a plastic bag to a stickman woman in a patterned dress and headscarf, who takes it with both hands; only these two figures, standing a step apart.", modern=True, text=cap('Bed nets have saved millions')),
  ch('c35c', C(.5, .5, 1.05), "A modern clinic room with a bright window: a stickman nurse in light blue scrubs gives an injection with a small syringe held in one hand to the upper arm of a toddler sitting on a stickman father's lap; the father in a short-sleeved shirt holds the child with both arms.", modern=True, text=cap('The first malaria vaccine, 2021')))
N('T03', "Some scientists are even changing the genes of mosquitoes, so they can no longer carry him.",
  ch('c35d', W(), "A bright modern insect laboratory with mesh cages on shelves: a stickman scientist in a white lab coat and safety glasses with his two dot eyes inside the lenses peers closely at a mesh cage full of mosquitoes, holding a clipboard in one hand.", modern=True, text=cap("Mosquitoes that can't carry him")))
K('T04', "Vaccines. Nets. Gene editing. They really are taking this personally.",
  kg('c36a', C(.5, .45, 1.1), "The Marsh Count stands trapped inside a big white mosquito net hanging over an empty bed, pressing both empty hands against the net from the inside, scowling, his long needle nose poking at the mesh."))

# ---- ending
N('L38', "Some say he has killed more people than anything else in history. That's hard to prove. But for thousands of years, he decided who could live near the water. And he is still here, waiting at dusk.",
  sh('c03a', C(.5, .5, 1.05)), sh('d16a', STILL), sh('c26b', WL()), sh('c31a', C(.5, .5, 1.05)),
  kg('c37a', C(.5, .45, 1.1), "The Marsh Count stands at the edge of a still swamp at dusk under an orange sky, wings open, looking out over the water towards a distant village with a few lit windows, seen in profile. Both of his arms are hidden INSIDE his closed fur-trimmed cloak; only ONE hand is visible, holding the cloak closed at his chest; no other hands anywhere, no hands hanging at his sides."))
N('L39', "Next time: the oldest stigma in history. A disease so feared that its victims had to ring a bell wherever they walked.",
  ch('c38a', C(.5, .5, 1.04), "A dark misty medieval country road at dusk with bare trees, ominous: on the left third of the frame a single lonely stickman figure in a long hooded grey robe, seen exactly in side profile, walks to the RIGHT towards the mist: his head, his body and both of his feet all point the same way, to the right. He carries a small brass hand bell in his front hand, held low in front of him; his other arm is hidden inside his wide sleeve. Exactly one figure, two legs, no twisting; the right side is dark empty mist."))
HOLD(5.0, sh('c38a', O(), text=[label('NEXT TIME', 1380, 360, 110, style='title', pop=True, at=.2, len=4.6), label('SUBSCRIBE', 1380, 500, 64, at=.8, len=4.0)]))

# ---- extra cut-ins for faster cutting (pos None = end)
EXTRA = {
  'C02': [(1, ch('c02c', C(.5, .5, 1.05), f"The cramped hot 1890s field laboratory: {ROSS} holds a small glass jar with a gauze lid up to his face with one hand, peering at the single mosquito inside, his other hand at his side." + LAMPS, text=cap('Two years of mosquitoes')))],
  'L03': [(None, ch('c07b', C(.5, .5, 1.05), "An 1890s Indian village hut at night: a stickman farmer in a white dhoti and a white cotton shirt sleeps on a woven rope bed, one arm hanging out, while a single mosquito lands on his arm.", text=cap('A week or two of silence')))],
  'L08': [(None, ch('c11d', W(), "A modern African rainforest field camp in daylight: a stickman scientist in a khaki field shirt and a sun hat kneels by a small sample tube rack on a folding table, looking up at the forest canopy, a notebook in one hand.", modern=True, text=cap('Traced back through gorilla parasites')))],
  'L11': [(None, ch('c12b', W(), "A sunny modern West African village: a stickman mother in a patterned dress sits on a bench holding a smiling healthy baby in both arms, while a stickman grandmother in a headscarf sits apart beside her.", modern=True, text=cap('One copy protects')))],
  'S03': [(None, ch('c13e', W(), "A small ancient Roman house with a tiled roof and a courtyard: a stickman Roman man in a short tunic lies on a wooden couch with a blanket, while a stickman Roman doctor in a white toga stands apart counting on the fingers of one raised hand.", text=cap('Tertian and quartan fevers')))],
  'L18': [(None, ob('c19c', "A single cinchona tree branch with glossy green leaves, pink flower clusters and a strip of reddish-brown bark lying on a rough wooden table beside a small stone mortar, warm daylight from a window; no lamps, no lanterns, no maps.", text=cap('The cinchona tree')))],
  'L21': [(None, ob('c20c', "A 1870s silver tray on a veranda table with a soda siphon, a green glass gin bottle without a label and two tall glasses with lime slices, palm leaves behind, warm afternoon light."))],
  'L24': [(None, ch('c23b', C(.5, .5, 1.05), "An 1880s lecture hall with wooden benches, dark wood panelling and a blackboard, no windows: two stickman professors in dark frock coats and top hats sit apart in the front row, shaking their heads with arms crossed.", text=cap('Hardly anyone believed him')))],
  'L27': [(None, ch('c26d', C(.5, .5, 1.05), "A wooden 1880s workers' hospital barracks in the Panama jungle: a stickman worker lies in a hammock under a thin blanket, shivering, while a stickman nun nurse in a long white habit stands apart beside him holding a cup of water in one hand.", text=cap('Malaria and yellow fever')))],
  'L30': [(None, ob('c28c', "A 1950s metal hand-pump sprayer tank with a long spray lance and straps, standing on dusty ground beside a mud wall freshly marked with a pale spray pattern, hot sun.", text=cap('DDT, 1955')))],
  'L35': [(None, ob('c31d', "A small bundle of feathery green sweet wormwood leaves next to a plain porcelain bowl of cold water on a wooden table, soft daylight.", text=cap('Sweet wormwood')))],
  'T01': [(None, ch('c35e', C(.5, .5, 1.05), "A modern African village at dusk with mud-brick houses and a few solar lamps: a stickman mother in a patterned dress sits outside her door, holding a sleeping child in both arms, a few mosquitoes in the orange sky."))],
  'T02': [(None, ob('c35f', "A modern bright clinic table with a white plastic tray: a small white rapid diagnostic test cassette and a small lancet lying on it, a box of blue gloves beside them, soft daylight from a window; modern only, no lanterns, no oil lamps, no mosquito nets, nothing old-fashioned; no letters or words on anything.", text=cap('A test in fifteen minutes')))],
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
    json.dump(out, open(os.path.join(ROOT, 'tools/plague/ep08_frames_todo.json'), 'w'), indent=1); print(len(out), 'frames')

def beats():
    out = {'base': 'assets/plague/ep08/frames', 'keep_zoom': [], 'static': True, 'fade_in': .8, 'start': 0.0, 'lead': .45, 'gap': .6, 'max_shot': 3.2,
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
        if i: out['beats'].append({'vo': f'assets/plague/ep08/vo/{i}.wav', **({'gain': 1.05} if r == 'MALARIA' else {}), 'shots': sl})
        else: out['beats'].append({'hold': t, 'shots': sl})
    json.dump(out, open(os.path.join(ROOT, 'tools/plague/ep08_beats.json'), 'w'), indent=1); print(len(out['beats']), 'beats')

MUSIC = [(0, 190, 'cholera_a.mp3'), (186, 330, 'plague_a.mp3'), (326, 470, 'plague_b.mp3'), (466, 'ALL', 'cholera_b.mp3')]   # open+who+origin+symptoms | ancient+bark | science+Panama+DDT | cure+aftermath+today

{'lines': lines, 'frames': frames, 'beats': beats}[sys.argv[1]]()
