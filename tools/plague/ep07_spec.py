"""Episode 7 (The ENTIRE History of Tuberculosis): single source of truth. Same format as ep06_spec.py.
Lessons from ep06 QC are built in: no stickman reference sheet (it pulls wrong-era costumes), clothes described in words,
a separate modern style, few props in stickmen's hands, no flags, diagrams one row only.

  python3 tools/plague/ep07_spec.py lines   -> voice list (id|ROLE|text), roles NARRATOR / TB
  python3 tools/plague/ep07_spec.py frames  -> tools/plague/ep07_frames_todo.json
  python3 tools/plague/ep07_spec.py beats   -> tools/plague/ep07_beats.json (for beats.py)
"""
import sys, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
K_SHEET = '1de80806-b140-40d9-8e0b-9a3a526ecee8'   # channel/plague/sheets/tb_b3.jpg (the White Lady, visibly ill)
STYLE = ("2D animated history explainer frame, 16:9, no text. Hand-drawn ink illustration, clean black outlines, muted grey-blue, bone-white and sepia palette "
         "with warm candle amber and small cold blue accents. Not gory.")
MODERN = ("2D animated history explainer frame, 16:9, no text. Hand-drawn ink illustration, clean black outlines, the same muted grey-blue, bone-white and sepia palette, "
          "soft natural daylight. The setting is modern (2000s-2020s): no lanterns, no gas lamps, no candles, nothing Victorian. Not gory.")
SN = ("Humans are simple STICKMEN: plain white round head, two dot eyes, no nose, no beard, thin black stick arms and stick legs, small black mitten hands, "
      "dressed exactly as described for this scene and era; anyone wearing glasses has his two dot eyes INSIDE the lenses and no other eyes. "
      "Only the few figures described, standing apart, never overlapping; each has exactly two arms and two hands attached to its sleeves; "
      "hands are empty unless an object is described; nothing floating; no flags.")
KING = ("Tuberculosis exactly as on the attached sheet, 'the White Lady': a ghostly, gaunt, emaciated Victorian woman with waxy grey-white skin, hollow cheeks with red feverish blotches, "
        "sunken dark-ringed glittering eyes, pale bluish lips, long unkempt dark hair, a tattered white high-collared Victorian nightgown and a grey knitted shawl; "
        "she holds AT MOST ONE object at a time (either a brass candle-holder OR a lace handkerchief, never both), her other hand empty and clearly attached to its own arm. Exactly ONE of her, with exactly two arms and two hands with normal-length fingers.")
DIAG = ("Draw ONLY the diagram described below, filling the whole frame, as ONE single picture: no extra rows, no extra panels, no comic strips above or below it. "
        "A hand-drawn explainer diagram in ink and muted watercolour on aged paper, clean and readable like an old textbook plate, "
        "numbered stages as small circled digits with drawn arrows. No words, no letters, no numbers on axes, only circled digits. Not gory. ")
NOPEOPLE = ' No people and no human figures anywhere in the picture.'
DISTANT = ' Any people are tiny distant stickman silhouettes only.'

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
def sc(img, p, cam=None, distant=False, modern=False, **k): return sh(img, cam or W(), (MODERN if modern else STYLE + ' ') + p + (DISTANT if distant else NOPEOPLE), **k)

B = []
def N(i, t, *s): B.append((i, 'NARRATOR', t, list(s)))
def K(i, t, *s): B.append((i, 'TB', t, list(s)))
def HOLD(sec, *s): B.append((None, None, sec, list(s)))

# ---- cold open: Koch stands up (Berlin, 24 March 1882 comes after, in passing)
LAMPS = " Lighting only from oil lamps and candles: no electric bulbs, no electric lamps."
N('C01', "A quiet country doctor stands up to speak, and Germany's top scientists, packed into a small library, stare back at him. Robert Koch. Berlin, the twenty-fourth of March, 1882.",
  ch('c01b', W(), "A wood-panelled 1880s lecture library with bookshelves: a single stickman scientist with small round glasses and a dark frock coat stands at a table covered with microscopes and glass slides, both hands resting on the table."),
  ch('c01c', C(.5, .5, 1.05), "A wood-panelled 1880s library seen from behind the audience: two stickman scientists in dark frock coats, high white collars and black bow ties sit apart on wooden chairs in the foreground, perfectly still, staring at a long table of brass microscopes at the front; their hands rest on their knees." + LAMPS),
  ch('c01a', WL(), "A Berlin street in 1882 at dusk with grand stone buildings, gas lamps and light snow: two stickman gentlemen in long dark overcoats and black top hats walk apart towards a lit doorway, one of them holding a leather briefcase, the other with his hands in his coat pockets.", text=cap('Berlin — 24 March 1882')))
N('C02', "He has found the killer that, in his time, was causing one in seven deaths across Europe and America. When he sits down, nobody claps. The room is completely silent.",
  dg('d01a', "Seven simple coffin icons in a single row; one of them is drawn darker and marked with a small cough cloud symbol above it.", text=[cap('One in seven deaths')]),
  ch('c02a', C(.5, .5, 1.05), "A wood-panelled 1880s lecture library: a stickman scientist with small round glasses and a dark frock coat has just sat down at a table with brass microscopes, hands folded on the table, while two stickman scientists in dark frock coats sit apart on chairs facing him, motionless, hands in their laps, nobody clapping." + LAMPS, text=cap('Nobody claps')))
N('C03', "The killer had been called consumption, phthisis, the white plague. People had blamed bad air, bad blood, a weak character. Even vampires.",
  ch('c03a', C(.5, .5, 1.05), "A dim Victorian sickroom: a pale thin stickman young woman in a white nightgown lies in an iron bed, coughing into her sleeve, while a stickman mother in a long dark 1870s dress and a white apron stands apart by the window, pushing the window open with both hands to let the bad air out; a candle burning low on the bedside table.", text=cap('They called it the white plague')),
  dg('d02a', "Four small numbered icons side by side: (1) a swirling cloud of bad air, (2) a drop of blood, (3) a wilting flower, (4) a vampire silhouette with a cape.", text=[cap('Blamed on bad air, even vampires')]))
K('C04', "Vampires. How flattering. They never guessed it was me.",
  kg('c04a', C(.5, .45, 1.1), "Medium shot: the White Lady stands in a dark Victorian corridor holding a brass candle-holder in one hand, smiling faintly at the viewer, her other hand resting on the wall."))
HOLD(4.6, kg('c05a', O(), "Title shot: the White Lady stands on the left third of the frame in a misty moonlit Victorian cemetery among white stone crosses, holding a candle in one hand, her other arm hanging at her side; dark empty mist on the right side.")
     | {'text': [label('TUBERCULOSIS', 1300, 330, 120, style='title', pop=True, at=.15, len=4.2), label('THE WHITE PLAGUE', 1300, 460, 72, style='title', color=[190, 205, 230], at=.5, len=3.9)],
        'sfx': [{'kind': 'boom', 'at': .1, 'gain': .8}]})

# ---- who is she
N('L01', "So who is she? A bacterium. Mycobacterium tuberculosis. A tiny rod, wrapped in a thick, waxy coat that protects her from almost everything the body throws at her.",
  dg('d03a', "A smooth simple rod-shaped bacterium like a short capsule with NO tails, NO hairs and NO flagella, shown in cross-section with a thick waxy outer coat drawn like layers of candle wax (1) and the inside (2); beside it a much LARGER round red blood cell (3), about three times longer than the bacterium."),
  sc('c06a', "A microscope view: a round bright field with many small purple-red rod-shaped bacteria, some lying in little clumps.", C(.5, .5, 1.05)))
N('L02', "And she is slow. Most bacteria divide every twenty minutes. She takes about a day. She is in no hurry at all.",
  dg('d04a', "Two clocks side by side: (1) a clock with many small rod bacteria multiplying around it quickly, (2) a clock with a single slow bacterium sitting beside a snail.", text=[cap('Most bacteria: 20 minutes. She takes a day')]))
N('L03', "She travels through the air. When a sick person coughs, sneezes or even sings, tiny droplets float in the room for hours. Breathing in just a few bacteria can be enough.",
  dg('d05a', "Three numbered panels: (1) a stickman coughing a small cloud of tiny dots into a room, (2) the dots floating in the air near a window for a long time, (3) a second stickman breathing in a few dots.", people=True, text=[cap('She travels through the air')]),
  ch('c07a', W(), "A crowded 1880s tenement room: a stickman man in a waistcoat with thin black stick arms coughs into the crook of his own elbow, while a stickman woman in a long dress sits apart sewing by the window.", text=cap('One cough in a crowded room')))
K('L04', "A cough, a breath, a crowded room. That's all I need.",
  kg('c08a', C(.5, .45, 1.1), "The White Lady stands in a dim, empty Victorian tenement stairwell, gently breathing out a faint pale mist, smiling, both hands holding her shawl closed at her chest."))
N('L05', "But here's the strange part. Most people who catch her never get sick. The body walls her inside tiny knots called tubercles. That's where the name comes from. She can sleep there for years. Today, about a quarter of all humans carry her.",
  dg('d06a', "Three numbered steps inside a simple lung outline: (1) a few rod bacteria arrive, (2) round defender cells surround them, (3) a hard round knot like a little stone wall with the bacteria sleeping inside it.", text=[cap('Walled up in tubercles, she sleeps for years')]),
  dg('d07a', "Four simple stickman icons in a row; one of them has a small sleeping bacterium drawn inside its chest.", people=True, text=[cap('About one in four people carry her')]))
K('L06', "I can wait. Years, if I have to.",
  kg('c09a', C(.5, .45, 1.1), "The White Lady sits patiently in a rocking chair in a dark room, both empty hands resting in her lap, watching a large hourglass run down on the small table beside her."))

# ---- origin
N('L07', "But where did she come from? She is ancient. Some scientists think her family travelled with our ancestors out of Africa tens of thousands of years ago. Others think she is younger. Either way, she has been with us since long before cities.",
  dg('d08a', "A simple world map with dotted arrows spreading out from Africa across the continents, with small rod bacteria riding along the arrows.", text=[cap('Out of Africa?')]),
  ch('c10a', WL(), "A prehistoric camp at dusk on an African savannah with a few hide shelters and acacia trees: two stickman hunter-gatherers in simple animal-hide wraps sit apart by a campfire, one of them coughing into his hand, the other holding a wooden spear upright.", text=cap('Tens of thousands of years ago')))
N('L08', "We find her in nine-thousand-year-old skeletons, and in the spines of Egyptian mummies, bent by a form of tuberculosis that attacks the bones.",
  ch('c10b', C(.5, .5, 1.05), "An ancient Egyptian tomb chamber lit by an oil lamp, hieroglyph-like carved patterns without readable writing: a stickman archaeologist in a 1920s khaki shirt, khaki trousers and a pith helmet kneels beside an open painted wooden sarcophagus, holding a small oil lamp over a wrapped mummy whose back is visibly hunched.", text=cap('The mummies of ancient Egypt')),
  dg('d09a', "A side view of a simple spine drawn as a stack of bones: (1) a healthy straight spine, (2) a spine with two collapsed bones and a sharp hunch.", text=[cap('Tuberculosis of the spine')]))
N('L09', "Then, people began living in crowded towns and cities, and she found the perfect home.",
  ch('c10c', WR(), "A narrow alley in a crowded ancient walled town with mud-brick houses packed tightly together and smoke rising: two stickman townspeople in simple undyed linen tunics and sandals pass each other a step apart, one of them coughing into his hand, the other carrying a clay water jar on his shoulder.", text=cap('The first crowded towns')))
K('L10', "Villages were dull. Cities, now cities I loved.",
  kg('c11a', C(.5, .45, 1.1), "The White Lady stands on a balcony overlooking a crowded ancient city at night, arms spread wide as if embracing it."))

# ---- WHAT SHE DOES TO YOU
N('S01', "So what does she do to you? When she wakes up, it starts slowly. A cough that won't go away for weeks. Tiredness. A fever that comes back every evening.",
  dg('d10a', "Two numbered panels: (1) a healthy stickman walking in the sun, (2) the same stickman weeks later wrapped in a blanket, coughing, small heat lines over his head and a calendar showing many crossed-off days.", people=True, text=[label('What She Does to You', 960, 150, 72), cap("A cough that won't go away")]),
  ch('c12a', W(), "A Victorian parlour: a single stickman woman in a long dark dress sits in an armchair with a blanket over her knees, coughing into her sleeve."))
N('S02', "Then the night sweats, soaking the sheets. And she eats away at your body. Patients grew thinner and thinner. That's why it was called consumption. It consumed you.",
  dg('d11a', "Three stickmen side by side drawn as the same person over time, each one thinner than the last, with numbered circles 1, 2, 3 under them.", people=True, text=[cap('Consumption: it consumed you')]),
  ch('c12b', C(.5, .5, 1.05), "A Victorian bedroom at night lit by a candle and moonlight: a thin stickman man in a damp, clinging white nightshirt sits up in bed among crumpled wet sheets, wiping his forehead with the back of his sleeve, his other hand on the mattress.", text=cap('Night sweats')))
N('S03', "In the lungs, she carves out holes. Patients began to cough up blood, often just a few red spots on a white handkerchief. For many, it was the first sign that this was serious.",
  dg('d12a', "Two simple cartoon lungs side by side: (1) healthy pink lungs, (2) lungs with several small dark holes; beside them a white handkerchief with three small red dots.", text=[cap('She carves holes in the lungs')]),
  ch('c12c', W(), "A Victorian bedroom: a single stickman man in a nightshirt sits on the edge of his bed looking with alarm at a white handkerchief he holds in both hands, a few small red spots on it.", text=cap('Often the first sign')))
N('S04', "She doesn't stop at the lungs. She can attack the bones, the kidneys, the brain, and the glands of the neck, which swell into lumps. That form had its own name: scrofula.",
  dg('d13a', "A standing stickman outline with four small numbered magnifier circles pointing to: (1) the lungs, (2) the spine, (3) the neck glands with a small swelling, (4) the head.", people=True, text=[cap('Not just the lungs')]))
N('S05', "Without treatment, about half of those who fall sick with her eventually die. It can take years.",
  dg('d14a', "ONLY ten simple stickman icons standing in a single row across the middle of the page: five drawn faded grey with a tiny cross above, five bright. Nothing else on the page, no pictures above or below.", people=True, text=[cap('Untreated, about half die')]),
  ch('c12d', C(.5, .5, 1.05), "A dim Victorian room with rain on the window and a candle: a stickman widow in a black high-necked 1870s mourning dress stands with her head bowed beside an empty rocking chair with a grey shawl draped over it, her hands clasped in front of her."))
K('S06', "I don't rush. I take my time. Years, sometimes.",
  kg('c13a', C(.5, .45, 1.1), "The White Lady holds up a large antique pocket watch on its chain in one hand, studying it with a soft patient smile, her other hand empty and resting at her side; a candle burns on a small table beside her, not in her hands."))

# ---- ancient & medieval
N('L11', "The ancient Greeks called her phthisis, the wasting. Hippocrates wrote that she was the most widespread disease of his time, and warned doctors not to visit late cases, to protect their reputation.",
  ch('c14a', W(), "An ancient Greek courtyard with white columns: a stickman physician in a white Greek chiton stands apart from a stickman patient lying on a couch, the physician turning away and raising one hand.", text=cap('Ancient Greece: phthisis, "the wasting"')),
  ch('c14b', WL(), "An ancient Greek temple of healing on a hill at sunset with white columns and olive trees: a single elderly stickman physician in a white chiton and a grey woollen cloak sits on a stone bench, writing on a papyrus scroll on his knee with a reed pen.", text=cap('Hippocrates')))
N('L12', "In the Middle Ages, scrofula was called the King's Evil, because people believed the touch of a king could cure it. English and French kings touched thousands of sick people in great ceremonies.",
  ch('c15a', W(), "A medieval throne room: a stickman king with a small gold crown and a red robe gently touches the cheek of a kneeling stickman peasant in a brown tunic whose two small black mitten hands are pressed together in prayer at his chest; only these two figures, each with exactly two arms and two visible hands.", text=cap("The King's Evil")),
  dg('d15a', "Three numbered steps: (1) a kneeling stickman, (2) a crowned stickman hand touching his cheek, (3) a small gold coin on a ribbon given as a keepsake.", people=True, text=[cap('The royal touch')]))
N('L13', "King Charles the Second of England is said to have touched around ninety thousand people. It didn't help, but it was very popular.",
  ch('c15b', W(), "A grand 1670s palace hall: a stickman king with a long black curly wig, a gold crown and a velvet robe sits on a throne, raising one hand in blessing, looking slightly bored; only this one figure.", text=cap('King Charles II of England')),
  dg('d16a', "A tally chart on aged paper: rows and rows of small tally marks filling the page, with a tiny crown icon in the corner.", text=[cap('About 90,000 people touched')]))
K('L14', "Ninety thousand royal touches. And not one of them bothered me.",
  kg('c16a', C(.5, .45, 1.1), "The White Lady stands alone in an empty candlelit throne room, idly trying on a small gold crown, amused."))

# ---- the romantic disease
N('L15', "By the 1800s, she was everywhere. In parts of Europe, she caused about one in four deaths. Crowded factory towns, damp housing, no fresh air.",
  ch('c17a', WL(), "A narrow 1850s factory-town street of brick terraces under rows of smoky chimneys and a grey sky: two stickman mill workers in flat caps, patched jackets and waistcoats walk home apart, one of them coughing into his fist, the other with his hands in his pockets.", text=cap('The factory towns of the 1800s')),
  dg('d17a', "Four simple coffin icons in a row; one of them is drawn darker with a small cough cloud above it.", text=[cap('One in four deaths in parts of Europe')]))
N('L16', "And yet, she became fashionable. A pale face, thin body, bright eyes and flushed cheeks were seen as beautiful. Women powdered their faces white and wore tight corsets to look consumptive.",
  ch('c17b', W(), "A Victorian dressing room: a single stickman lady in a long pale gown sits at a vanity mirror, powdering her face white with a large powder puff.", text=cap('Pale was beautiful')),
  dg('d18a', "A Victorian fashion plate: a simple stickman woman in a long gown with a very narrow waist, with numbered arrows pointing to (1) a white powdered face, (2) pink cheeks, (3) a tight corset.", people=True, text=[cap('The consumptive look')]))
N('L17', "Poets and artists seemed to die of her. John Keats at twenty-five. Frederic Chopin. The Bronte sisters. Operas like La Traviata and La Boheme ended with a beautiful heroine dying of consumption.",
  ch('c18a', W(), "An 1820s room in Rome: a thin young stickman poet in a white shirt sits by a window, writing with a quill, a blanket over his knees.", text=cap('John Keats, dead at 25')),
  ch('c18b', W(), "An 1840s Paris salon: a thin stickman pianist in a dark tailcoat plays a grand piano by candlelight, alone.", text=cap('Frédéric Chopin — 1849')),
  ch('c18c', C(.5, .5, 1.05), "An 1850s opera stage with red velvet curtains, lit by footlights: a stickman soprano in a long white nightgown lies on a stage bed with one arm stretched out dramatically, while a stickman tenor in a dark velvet costume kneels apart beside the bed, his hands pressed to his heart.", text=cap('La Traviata')))
K('L18', "I was the most romantic way to die. Artists adored me.",
  kg('c19a', C(.5, .45, 1.1), "The White Lady poses elegantly for a portrait in an empty artist's studio, sitting on a velvet chaise, a large blank canvas on an easel in front of her."))
N('L19', "In New England in the 1890s, families who lost several members to her became convinced the dead were feeding on the living. In 1892, the family of Mercy Brown dug up her body, burned her heart, and fed the ashes to her sick brother. He died anyway.",
  ch('c20a', WL(), "A small snowy New England graveyard in 1892 at dusk with a wooden fence, a little stone crypt and bare trees: a single stickman farmer in a heavy 1890s wool winter coat and a felt hat stands at a snowy grave with his head bowed, his hands clasped in front of him.", text=cap('Rhode Island — 1892')),
  ch('c20b', W(), "A snowy graveyard at night: two stickman farmers in heavy winter coats and hats stand apart by a lantern on the ground, holding shovels, looking grim.", text=cap('They dug up Mercy Brown')))
K('L20', "A vampire. They called me a vampire. I've been called worse.",
  kg('c21a', C(.5, .45, 1.1), "The White Lady sits on a snowy gravestone at night, laughing quietly, both hands resting on her knees."))

# ---- Koch
N('L21', "Then came Robert Koch. Using new dyes, he stained lung tissue and found the bacteria hiding inside. He grew them, put them into animals, and proved that they caused the disease.",
  dg('d19a', "Four numbered steps: (1) a glass slide with a drop of stain, (2) under a microscope, small purple rods appear, (3) a small glass dish with bacteria growing, (4) a guinea pig in a cage.", text=[cap('From a stain to proof')]),
  ch('c22a', W(), "An 1880s laboratory: a single stickman scientist with small round glasses and a dark frock coat looks through a brass microscope, one hand adjusting it."))
N('L22', "His talk that day changed medicine. The twenty-fourth of March is now World Tuberculosis Day. Koch won the Nobel Prize in 1905.",
  ch('c22b', WR(), "A grand 1880s lecture library with oil lamps glowing and a long table of brass microscopes: a stickman scientist with small round glasses and a dark frock coat stands at the table, while two stickman scientists in dark frock coats stand apart beside him, each bending to look into a different microscope." + LAMPS, text=cap('Nobel Prize, 1905')),
  dg('d20a', "A calendar page with one day circled, next to a simple gold medal on a ribbon.", text=[cap('24 March is now World TB Day')]))
N('L23', "But knowing the cause didn't give a cure. Koch's own remedy, tuberculin, was a failure as a treatment. It later became a useful skin test, to find out who carries her.",
  dg('d21a', "Two numbered panels: (1) a small glass vial with a cross over it, (2) a forearm with a tiny injection point and a small round red bump next to a ruler.", text=[cap('Not a cure, but a test')]))
K('L24', "They knew my name at last. They just couldn't do anything about it.",
  kg('c23a', C(.5, .45, 1.1), "The White Lady sits on a laboratory stool in an empty 1880s lab, examining a microscope with polite curiosity."))

# ---- sanatoriums
N('L25', "So doctors prescribed rest, good food, and fresh air. Sanatoriums opened in the mountains and by the sea. Patients lay wrapped in blankets on open balconies, even in the snow, for months or years.",
  ch('c24a', WL(), "A large white Swiss mountain sanatorium with long open balconies in the snowy Alps, pine forest, bright cold sky: in the foreground a stickman nurse in a long white 1900s apron dress and a white cap pushes a wooden wheelchair along a snowy path, a stickman patient in a wool hat sitting in it wrapped in a thick blanket.", text=cap('Davos, Switzerland')),
  ch('c24b', W(), "A long open sanatorium balcony in winter: three stickman patients in wool hats lie on reclining wooden chairs wrapped in thick blankets, spaced apart, snowy mountains behind.", text=cap('For months, even years')),
  dg('d22a', "Three numbered icons: (1) a bed, (2) a plate of food with milk and eggs, (3) a mountain with fresh air lines.", text=[cap('The prescription: fresh air')]))
N('L26', "It helped some people, and it kept the sick away from their families. But many never came home.",
  ch('c24c', C(.5, .5, 1.05), "A snowy sanatorium balcony at dusk, mountains in the distance: a single stickman nurse in a long white 1900s apron dress and a white cap stands with her head bowed, laying a folded blanket on an empty wooden reclining chair.", text=cap('Many never came home')))
K('L27', "Mountain air. Very pleasant. I came along for the view.",
  kg('c25a', C(.5, .45, 1.1), "The White Lady lounges on a reclining chair on an empty snowy sanatorium balcony, wrapped in a blanket, both hands holding a teacup, enjoying the mountain view."))

# ---- vaccine and cure
N('L28', "In 1921, two French scientists, Albert Calmette and Camille Guerin, made a vaccine called BCG. They weakened a cattle form of the bacteria by growing it over and over, two hundred and thirty times, for thirteen years.",
  ch('c26a', W(), "A 1910s laboratory at the Pasteur Institute: two stickman scientists in white coats stand apart at a bench with rows of small glass flasks, one holding up a flask.", text=cap('Calmette and Guérin, 1921')),
  dg('d23a', "A long row of small glass flasks connected by arrows, numbered (1) at the start and (2) at the end, with a calendar showing thirteen years and a small cow icon at the start.", text=[cap('Grown 230 times over 13 years')]))
N('L29', "BCG protects young children well, and it is still given to millions of babies today. But it doesn't protect adults very well. They needed a cure.",
  ch('c26b', W(), modern=True, p="A modern clinic: a stickman nurse in blue scrubs holds a tiny syringe in one hand next to the upper arm of a baby, her other hand resting on her own hip; a stickman mother in a cardigan holds the baby in both arms; only these three figures, each nurse and mother with exactly two arms coming out of the shoulders, normal length.", text=cap('Still given to millions of babies')))
N('L30', "In 1943, in a lab in New Jersey, a young student, Albert Schatz, working under Selman Waksman, discovered streptomycin, an antibiotic found in soil bacteria. It was the first drug that could kill her.",
  ch('c27a', C(.5, .5, 1.05), "A 1940s American university laboratory with soil samples in glass jars, petri dishes and a window onto a farm field: a young stickman student in a white lab coat works at the bench with a glass jar of soil, while an older stickman professor in a grey 1940s three-piece suit and round glasses stands apart by the door, hands behind his back, watching. No flags, no banners, no pennants anywhere.", text=cap('New Jersey — 1943')),
  ch('c27b', W(), "A 1940s basement laboratory: a single young stickman student in a white coat holds up a petri dish to the light, smiling.", text=cap('Albert Schatz')),
  dg('d24a', "Three numbered steps: (1) a scoop of farm soil, (2) a petri dish with a clear ring around a mould colony, (3) a small medicine bottle.", text=[cap('A cure from the soil')]))
N('L31', "Waksman alone won the Nobel Prize, and Schatz spent years fighting for credit. More drugs followed. Taken together, for months, they could finally cure her.",
  dg('d25a', "Three different simple pill shapes joined by a plus sign, then an arrow to a calendar of six months and a green tick.", text=[cap('Several drugs, taken for months')]),
  ch('c28a', WR(), "A bright 1950s hospital ward with a row of tidy beds: a recovered stickman woman in a 1950s wool coat and a small hat walks towards the door carrying one small suitcase, smiling, while a stickman nurse in a white 1950s uniform and cap stands apart by a bed, waving goodbye with one hand.", text=cap('Finally, a cure')))
N('L32', "Mass X-ray vans toured towns and cities. Sanatoriums emptied, and closed. In rich countries, cases fell year after year.",
  dg('d26a', "A simple line chart falling steeply from left to right, with small sanatorium building icons along the top that become fainter.", text=[cap('Cases fall, year after year')]),
  ch('c28b', W(), "A 1950s X-ray room: a single stickman man in a vest stands with his chest against a large X-ray plate, a stickman technician in a white coat apart behind a small screen.", text=cap('X-rays for whole towns')))
K('L33', "Pills. Little pills. Do you know how humiliating that is?",
  kg('c29a', C(.5, .45, 1.1), "The White Lady sits sulking in an empty 1950s pharmacy, staring at a small brown pill bottle on the counter in front of her."))

# ---- comeback & today
N('L34', "But she came back. In the 1980s and 90s, HIV weakened millions of immune systems, and she woke up in them. And when patients stopped their pills too early, she learned to survive the drugs.",
  dg('d27a', "Two numbered panels: (1) a sleeping bacterium inside a weakened round shield with cracks, waking up, (2) a bacterium with a small armour plate bouncing pills away.", text=[cap('She learned to survive the drugs')]))
N('L35', "Today, she is once again the world's deadliest infectious disease. More than ten million people fall ill every year, and over a million die, mostly in Asia and Africa.",
  dg('d28a', "ONLY a simple world map filling the whole page: South Asia, Southeast Asia and Africa shaded dark, other regions pale. Nothing else, no pictures, no rows of panels, no ships.", text=[cap('Over 10 million fall ill every year')]),
  ch('c30a', W(), modern=True, p="A busy modern clinic waiting room in South Asia: ONLY two stickman patients in everyday clothes and cloth face masks sit apart on plastic chairs, hands in their laps; nobody else in the room, no staff, no other patients.", text=cap('Mostly in Asia and Africa')))
N('L36', "And yet, almost everyone can be cured, with a six-month course of cheap pills. The problem is not the medicine. It's getting it to the people who need it.",
  dg('d29a', "ONLY a single row of six simple blank calendar sheets across the page, each with one small white pill drawn on it, and a big green tick at the end. Nothing above or below, no other pictures, no digits.", text=[cap('Six months of cheap pills')]),
  ch('c30b', W(), modern=True, p="A modern rural health worker in a vest walks along a dirt village road carrying a small medical bag, waving to a stickman family outside a house; the health worker and two family members, standing apart.", text=cap('The hard part: reaching people')))

# ---- WHAT SHE LEAVES BEHIND
N('A01', "And for those who survive? Many are left with scarred lungs, short of breath for life. Some carry her quietly, and she can wake again when they are old or ill.",
  dg('d30a', "Three numbered panels: (1) a pair of simple lungs with pale scar lines, (2) a stickman walking slowly up stairs, out of breath, (3) a small sleeping bacterium inside a knot, with a question mark.", people=True, text=[label('What She Leaves Behind', 960, 150, 72), cap('She can wake again')]))
N('A02', "For the world, she left more than graves. Sanatoriums inspired modern architecture: white walls, big windows, balconies and sunlight. The idea of tracing contacts and screening whole populations. And World Tuberculosis Day.",
  ch('c31a', WL(), "A white 1930s modernist sanatorium with flat roofs, long horizontal balconies, huge windows, sunlight and pine trees: on a sunny balcony two stickman patients in light 1930s dressing gowns lie apart on reclining chairs, faces turned up to the sun, hands resting on their blankets.", text=cap('White walls, big windows, sunlight')),
  dg('d31a', "Three numbered icons: (1) a white modernist building with balconies, (2) a chain of connected stickman icons for contact tracing, (3) a chest X-ray image.", people=True, text=[cap('She left more than graves')]))
K('A03', "They built whole buildings just to get away from me. I'm almost touched.",
  kg('c32a', C(.5, .45, 1.1), "The White Lady stands in a bright, empty white modernist sanatorium hall full of sunlight, looking up at the tall windows, both hands clasped in front of her."))

# ---- ending
N('L37', "Thousands of years. A billion lives, by some estimates. Not beaten by kings, poets or mountain air, but by a dye, a soil bacterium, and six months of pills. And she isn't finished yet.",
  sh('c01b', W()), sh('d19a', STILL), sh('c24a', W()), sh('d24a', STILL), sh('c30b', W()))
N('L38', "Next time: a killer that rides on the wings of a mosquito. It may have killed more people than any other disease in history.",
  ch('c33a', C(.5, .5, 1.04), "A dark tropical swamp at night under a full moon, mist over the water, ominous: on the left third of the frame a single stickman villager in a simple cotton shirt and trousers sleeps in a hammock strung between two trees, while one huge dark mosquito silhouette hovers over the water near him; the right side is dark empty mist."))
HOLD(5.0, sh('c33a', O(), text=[label('NEXT TIME', 1380, 360, 110, style='title', pop=True, at=.2, len=4.6), label('SUBSCRIBE', 1380, 500, 64, at=.8, len=4.0)]))

# ---- extra cut-ins for faster cutting (pos None = end)
EXTRA = {
  'C01': [(2, ch('c01d', C(.5, .5, 1.05), "Medium shot in a wood-panelled 1880s library: a single stickman doctor with small round glasses, a neat dark frock coat and a high white collar stands at a table of brass microscopes, holding one sheet of handwritten notes in one hand and reading from it aloud, his other hand resting on the table." + LAMPS, text=cap('Robert Koch')))],
  'L01': [(None, kg('c06b', C(.5, .45, 1.1), "The White Lady stands calmly in a dark candlelit room, pulling her grey knitted shawl tightly around her shoulders with both empty hands like a coat of armour, looking untouchable and smug."))],
  'L03': [(None, ch('c07b', C(.5, .5, 1.05), "Sunbeams through a dusty window in a dark crowded 1880s tenement room, faint specks in the light: a stickman girl in a plain grey pinafore dress stands in the sunbeam taking a deep breath, while a stickman old man in a waistcoat sits apart on a stool in the shadow, coughing into his elbow."))],
  'L05': [(None, ch('c07c', W(), "A busy 1880s factory floor: two stickman workers in caps stand apart at a loom, both looking perfectly healthy.", text=cap('Most carriers never get sick')))],
  'L07': [(None, ch('c10d', C(.5, .5, 1.05), "A dusty modern archaeological dig in bright daylight: a single stickman archaeologist in a khaki shirt and a wide-brimmed sun hat kneels in a shallow trench, brushing earth off ancient bones with a small brush in one hand.", text=cap('Long before cities')))],
  'S01': [(None, ch('c12e', C(.5, .5, 1.05), "A Victorian parlour at evening with a clock on the mantelpiece: a stickman mother in a long dark dress stands holding a glass thermometer up to the oil lamp to read it, while her stickman son in a nightshirt sits apart on the sofa wrapped in a blanket, with flushed cheeks.", text=cap('A fever every evening')))],
  'S03': [(None, sc('c12f', "A white lace handkerchief lying on a dark wooden table beside a candle, three small red spots on it.", C(.5, .5, 1.05)))],
  'S04': [(None, ch('c12g', W(), "A Victorian doctor's room: a stickman doctor in a frock coat gently examines the neck of a stickman child sitting on a stool; only these two.", text=cap('Scrofula')))],
  'L11': [(None, ch('c14c', C(.5, .5, 1.05), "A sunny ancient Greek street with white houses: a stickman physician in a white chiton walks away down the street, glancing back, while a very thin sick stickman in a ragged brown tunic sits apart on a doorstep, wrapped in a cloak, coughing."))],
  'L12': [(None, sc('c15c', "A small medieval gold coin with an angel design on a red ribbon, lying on a red velvet cushion, a plain stone wall behind. No flags, no banners, no pennants anywhere.", C(.5, .5, 1.05)))],
  'L15': [(None, ch('c17c', W(), "A damp 1850s basement room: a single stickman mother in a shawl sits by a tiny window, rocking a cradle, mould on the walls.", text=cap('Damp rooms, no fresh air')))],
  'L17': [(None, ch('c18d', C(.5, .5, 1.05), "An 1840s Yorkshire parsonage parlour lit by a candle: two stickman young women in plain dark high-necked dresses sit apart at a wooden table, each writing in a notebook with a quill pen."))],
  'L19': [(None, ch('c20c', WR(), "Inside an 1890s New England farmhouse bedroom at night lit by an oil lamp: a thin sick stickman young man in a nightshirt lies in bed under a patchwork quilt, while his stickman father in a work shirt and braces sits apart on a chair, holding out a small cup to him.", text=cap('He died anyway')))],
  'L21': [(None, sc('c22c', "Small glass bottles of bright blue and brown stains on a laboratory shelf in 1882, a dropper beside them.", C(.5, .5, 1.05)))],
  'L25': [(None, ch('c24d', WR(), "A small Alpine railway station in the snow with chalets and a bright blue sky: a pale stickman young woman in a long 1900s travelling coat and a hat arrives carrying one small suitcase, while a stickman porter in a dark uniform and cap stands apart by the train."))],
  'L28': [(None, ch('c26c', C(.5, .5, 1.05), "A 1910s laboratory with a row of glass culture flasks of yellowish medium on the bench and a cow pasture through the window: a single stickman scientist in a white coat and small round glasses leans over the bench, transferring a culture into a fresh flask with a long thin wire loop held in one hand."))],
  'L30': [(None, sc('c27c', "A handful of dark rich farm soil in a glass dish on a lab bench, a microscope beside it.", C(.5, .5, 1.05)))],
  'L32': [(None, sc('c28c', "A 1950s chest X-ray film on a light box showing simple pale lungs, in a dim room.", C(.5, .5, 1.05)))],
  'L34': [(None, ch('c30c', C(.5, .5, 1.05), "A modern hospital isolation room with soft light and no signs: a stickman patient in a hospital gown sits on the bed, turning away from a small paper cup of pills on the bedside table, while a stickman doctor in a white coat and a face mask stands apart by the door, looking worried.", modern=True, text=cap('Stopping the pills too early')))],
  'L35': [(None, ch('c30d', WL(), "A crowded modern South Asian city street at dusk with buses, rickshaws and shop signs without readable words: in the foreground a thin stickman man in a simple shirt and a checked lungi stops to cough into his elbow, while a stickman woman in a sari walks past, apart from him.", modern=True, text=cap('Over a million die every year')))],
  'A01': [(None, ch('c31b', W(), "A modern park: a single elderly stickman in a cardigan sits on a bench catching his breath, a walking stick beside him.", modern=True, text=cap('Short of breath for life')))],
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
    json.dump(out, open(os.path.join(ROOT, 'tools/plague/ep07_frames_todo.json'), 'w'), indent=1); print(len(out), 'frames')

def beats():
    out = {'base': 'assets/plague/ep07/frames', 'keep_zoom': [], 'static': True, 'fade_in': .8, 'start': 0.0, 'lead': .45, 'gap': .6, 'max_shot': 3.2,
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
        if i: out['beats'].append({'vo': f'assets/plague/ep07/vo/{i}.wav', **({'gain': 1.05} if r == 'TB' else {}), 'shots': sl})
        else: out['beats'].append({'hold': t, 'shots': sl})
    json.dump(out, open(os.path.join(ROOT, 'tools/plague/ep07_beats.json'), 'w'), indent=1); print(len(out['beats']), 'beats')

MUSIC = [(0, 200, 'plague_a.mp3'), (196, 345, 'plague_b.mp3'), (341, 438, 'cholera_a.mp3'), (434, 'ALL', 'cholera_b.mp3')]   # open+who+origin+symptoms | history+romance+Koch | sanatoria+cure | comeback+aftermath

{'lines': lines, 'frames': frames, 'beats': beats}[sys.argv[1]]()
