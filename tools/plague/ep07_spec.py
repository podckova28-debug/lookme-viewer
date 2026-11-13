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

# ---- cold open: Berlin, 24 March 1882
N('C01', "Berlin. The twenty-fourth of March, 1882. In a small library packed with Germany's top scientists, a quiet country doctor named Robert Koch stands up to speak.",
  sc('c01a', "A Berlin street in 1882 at dusk with grand stone buildings, gas lamps and a horse-drawn tram, light snow.", WL(), distant=True, text=cap('BERLIN · 24 MARCH 1882')),
  ch('c01b', W(), "A wood-panelled 1880s lecture library with bookshelves: a single stickman scientist with small round glasses and a dark frock coat stands at a table covered with microscopes and glass slides, both hands resting on the table."),
  sc('c01c', "Rows of empty wooden chairs in a wood-panelled library, a long table with a dozen brass microscopes lined up, lit by oil lamps. Lighting only from oil lamps and candles: no electric bulbs, no electric lamps.", C(.5, .5, 1.05)))
N('C02', "He has found the killer that, in his time, was causing one in seven deaths across Europe and America. When he sits down, nobody claps. The room is completely silent.",
  dg('d01a', "Seven simple coffin icons in a single row; one of them is drawn darker and marked with a small cough cloud symbol above it.", text=[cap('1 IN 7 DEATHS')]),
  sc('c02a', "A single brass microscope on a table lit by a brass oil lamp, a glass slide with tiny purple-stained rods beside it, everything else in shadow. Lighting only from oil lamps and candles: no electric bulbs, no electric lamps.", C(.5, .5, 1.05)))
N('C03', "The killer had been called consumption, phthisis, the white plague. People had blamed bad air, bad blood, a weak character. Even vampires.",
  dg('d02a', "Four small numbered icons side by side: (1) a swirling cloud of bad air, (2) a drop of blood, (3) a wilting flower, (4) a vampire silhouette with a cape.", text=[cap('BAD AIR? BAD BLOOD? WEAKNESS? VAMPIRES?')]),
  sc('c03a', "A dim Victorian sickroom with an empty iron bed, a basin and a jug, a white handkerchief on the pillow, a candle burning low.", C(.5, .5, 1.05)))
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
  dg('d04a', "Two clocks side by side: (1) a clock with many small rod bacteria multiplying around it quickly, (2) a clock with a single slow bacterium sitting beside a snail.", text=[cap('MOST BACTERIA: 20 MINUTES  ·  TB: ABOUT A DAY')]))
N('L03', "She travels through the air. When a sick person coughs, sneezes or even sings, tiny droplets float in the room for hours. Breathing in just a few bacteria can be enough.",
  dg('d05a', "Three numbered panels: (1) a stickman coughing a small cloud of tiny dots into a room, (2) the dots floating in the air near a window for a long time, (3) a second stickman breathing in a few dots.", people=True, text=[cap('THROUGH THE AIR')]),
  ch('c07a', W(), "A crowded 1880s tenement room: a stickman man in a waistcoat with thin black stick arms coughs into the crook of his own elbow, while a stickman woman in a long dress sits apart sewing by the window."))
K('L04', "A cough, a breath, a crowded room. That's all I need.",
  kg('c08a', C(.5, .45, 1.1), "The White Lady stands in a dim, empty Victorian tenement stairwell, gently breathing out a faint pale mist, smiling, both hands holding her shawl closed at her chest."))
N('L05', "But here's the strange part. Most people who catch her never get sick. The body walls her inside tiny knots called tubercles. That's where the name comes from. She can sleep there for years. Today, about a quarter of all humans carry her.",
  dg('d06a', "Three numbered steps inside a simple lung outline: (1) a few rod bacteria arrive, (2) round defender cells surround them, (3) a hard round knot like a little stone wall with the bacteria sleeping inside it.", text=[cap('TUBERCLES: SHE SLEEPS FOR YEARS')]),
  dg('d07a', "Four simple stickman icons in a row; one of them has a small sleeping bacterium drawn inside its chest.", people=True, text=[cap('ABOUT 1 IN 4 PEOPLE CARRY HER')]))
K('L06', "I can wait. Years, if I have to.",
  kg('c09a', C(.5, .45, 1.1), "The White Lady sits patiently in a rocking chair in a dark room, knitting slowly, an hourglass on the table beside her."))

# ---- origin
N('L07', "But where did she come from? She is ancient. Some scientists think her family travelled with our ancestors out of Africa tens of thousands of years ago. Others think she is younger. Either way, she has been with us since long before cities.",
  dg('d08a', "A simple world map with dotted arrows spreading out from Africa across the continents, with small rod bacteria riding along the arrows.", text=[cap('OUT OF AFRICA?')]),
  sc('c10a', "A prehistoric camp at dusk on an African savannah, a few hide shelters and a campfire, acacia trees.", WL(), distant=True))
N('L08', "We find her in nine-thousand-year-old skeletons, and in the spines of Egyptian mummies, bent by a form of tuberculosis that attacks the bones.",
  sc('c10b', "An ancient Egyptian tomb chamber lit by an oil lamp, a painted wooden sarcophagus, hieroglyph-like carved patterns without readable writing.", C(.5, .5, 1.05)),
  dg('d09a', "A side view of a simple spine drawn as a stack of bones: (1) a healthy straight spine, (2) a spine with two collapsed bones and a sharp hunch.", text=[cap('TB OF THE SPINE')]))
N('L09', "Then, people began living in crowded towns and cities, and she found the perfect home.",
  sc('c10c', "A crowded ancient walled town with mud-brick houses packed tightly together, smoke rising, narrow alleys.", WR(), distant=True))
K('L10', "Villages were dull. Cities, now cities I loved.",
  kg('c11a', C(.5, .45, 1.1), "The White Lady stands on a balcony overlooking a crowded ancient city at night, arms spread wide as if embracing it."))

# ---- WHAT SHE DOES TO YOU
N('S01', "So what does she do to you? When she wakes up, it starts slowly. A cough that won't go away for weeks. Tiredness. A fever that comes back every evening.",
  dg('d10a', "Two numbered panels: (1) a healthy stickman walking in the sun, (2) the same stickman weeks later wrapped in a blanket, coughing, small heat lines over his head and a calendar showing many crossed-off days.", people=True, text=[label('WHAT SHE DOES TO YOU', 960, 150, 72), cap('A COUGH FOR WEEKS  ·  TIREDNESS  ·  FEVER')]),
  ch('c12a', W(), "A Victorian parlour: a single stickman woman in a long dark dress sits in an armchair with a blanket over her knees, coughing into her sleeve."))
N('S02', "Then the night sweats, soaking the sheets. And she eats away at your body. Patients grew thinner and thinner. That's why it was called consumption. It consumed you.",
  dg('d11a', "Three stickmen side by side drawn as the same person over time, each one thinner than the last, with numbered circles 1, 2, 3 under them.", people=True, text=[cap('CONSUMPTION: IT CONSUMED YOU')]),
  sc('c12b', "A Victorian bed at night with damp crumpled sheets and a wet nightshirt hanging on a chair, a candle on the bedside table, moonlight.", C(.5, .5, 1.05)))
N('S03', "In the lungs, she carves out holes. Patients began to cough up blood, often just a few red spots on a white handkerchief. For many, it was the first sign that this was serious.",
  dg('d12a', "Two simple cartoon lungs side by side: (1) healthy pink lungs, (2) lungs with several small dark holes; beside them a white handkerchief with three small red dots.", text=[cap('HOLES IN THE LUNGS')]),
  ch('c12c', W(), "A Victorian bedroom: a single stickman man in a nightshirt sits on the edge of his bed looking with alarm at a white handkerchief he holds in both hands, a few small red spots on it."))
N('S04', "She doesn't stop at the lungs. She can attack the bones, the kidneys, the brain, and the glands of the neck, which swell into lumps. That form had its own name: scrofula.",
  dg('d13a', "A standing stickman outline with four small numbered magnifier circles pointing to: (1) the lungs, (2) the spine, (3) the neck glands with a small swelling, (4) the head.", people=True, text=[cap('LUNGS  ·  BONES  ·  NECK  ·  BRAIN')]))
N('S05', "Without treatment, about half of those who fall sick with her eventually die. It can take years.",
  dg('d14a', "ONLY ten simple stickman icons standing in a single row across the middle of the page: five drawn faded grey with a tiny cross above, five bright. Nothing else on the page, no pictures above or below.", people=True, text=[cap('WITHOUT TREATMENT: ABOUT HALF DIE')]),
  sc('c12d', "An empty rocking chair by a window in a dim Victorian room, a shawl draped over it, a candle, rain on the glass.", C(.5, .5, 1.05)))
K('S06', "I don't rush. I take my time. Years, sometimes.",
  kg('c13a', C(.5, .45, 1.1), "The White Lady winds a large antique pocket watch slowly, holding it up to her candle, smiling softly."))

# ---- ancient & medieval
N('L11', "The ancient Greeks called her phthisis, the wasting. Hippocrates wrote that she was the most widespread disease of his time, and warned doctors not to visit late cases, to protect their reputation.",
  ch('c14a', W(), "An ancient Greek courtyard with white columns: a stickman physician in a white Greek chiton stands apart from a stickman patient lying on a couch, the physician turning away and raising one hand."),
  sc('c14b', "An ancient Greek temple of healing on a hill at sunset with white columns and olive trees.", WL(), distant=True))
N('L12', "In the Middle Ages, scrofula was called the King's Evil, because people believed the touch of a king could cure it. English and French kings touched thousands of sick people in great ceremonies.",
  ch('c15a', W(), "A medieval throne room: a stickman king with a small gold crown and a red robe gently touches the cheek of a kneeling stickman peasant in a brown tunic whose two small black mitten hands are pressed together in prayer at his chest; only these two figures, each with exactly two arms and two visible hands."),
  dg('d15a', "Three numbered steps: (1) a kneeling stickman, (2) a crowned stickman hand touching his cheek, (3) a small gold coin on a ribbon given as a keepsake.", people=True, text=[cap('THE ROYAL TOUCH')]))
N('L13', "King Charles the Second of England is said to have touched around ninety thousand people. It didn't help, but it was very popular.",
  ch('c15b', W(), "A grand 1670s palace hall: a stickman king with a long black curly wig, a gold crown and a velvet robe sits on a throne, raising one hand in blessing, looking slightly bored; only this one figure.", text=cap('CHARLES II')),
  dg('d16a', "A tally chart on aged paper: rows and rows of small tally marks filling the page, with a tiny crown icon in the corner.", text=[cap('ABOUT 90,000 TOUCHES')]))
K('L14', "Ninety thousand royal touches. And not one of them bothered me.",
  kg('c16a', C(.5, .45, 1.1), "The White Lady stands alone in an empty candlelit throne room, idly trying on a small gold crown, amused."))

# ---- the romantic disease
N('L15', "By the 1800s, she was everywhere. In parts of Europe, she caused about one in four deaths. Crowded factory towns, damp housing, no fresh air.",
  sc('c17a', "A crowded 19th-century industrial city with rows of smoky chimneys, narrow brick terraces and grey sky.", WL(), distant=True),
  dg('d17a', "Four simple coffin icons in a row; one of them is drawn darker with a small cough cloud above it.", text=[cap('1 IN 4 DEATHS IN PARTS OF EUROPE')]))
N('L16', "And yet, she became fashionable. A pale face, thin body, bright eyes and flushed cheeks were seen as beautiful. Women powdered their faces white and wore tight corsets to look consumptive.",
  ch('c17b', W(), "A Victorian dressing room: a single stickman lady in a long pale gown sits at a vanity mirror, powdering her face white with a large powder puff."),
  dg('d18a', "A Victorian fashion plate: a simple stickman woman in a long gown with a very narrow waist, with numbered arrows pointing to (1) a white powdered face, (2) pink cheeks, (3) a tight corset.", people=True, text=[cap('THE CONSUMPTIVE LOOK')]))
N('L17', "Poets and artists seemed to die of her. John Keats at twenty-five. Frederic Chopin. The Bronte sisters. Operas like La Traviata and La Boheme ended with a beautiful heroine dying of consumption.",
  ch('c18a', W(), "An 1820s room in Rome: a thin young stickman poet in a white shirt sits by a window, writing with a quill, a blanket over his knees.", text=cap('JOHN KEATS · 1821')),
  ch('c18b', W(), "An 1840s Paris salon: a thin stickman pianist in a dark tailcoat plays a grand piano by candlelight, alone.", text=cap('FREDERIC CHOPIN · 1849')),
  sc('c18c', "An empty opera stage in the 1850s with red velvet curtains, a lonely bed on the stage lit by a spotlight, rows of empty theatre seats.", C(.5, .5, 1.05)))
K('L18', "I was the most romantic way to die. Artists adored me.",
  kg('c19a', C(.5, .45, 1.1), "The White Lady poses elegantly for a portrait in an empty artist's studio, sitting on a velvet chaise, a large blank canvas on an easel in front of her."))
N('L19', "In New England in the 1890s, families who lost several members to her became convinced the dead were feeding on the living. In 1892, the family of Mercy Brown dug up her body, burned her heart, and fed the ashes to her sick brother. He died anyway.",
  sc('c20a', "A small snowy New England graveyard in 1892 at dusk, a wooden fence, a little stone crypt, bare trees.", WL(), text=cap('RHODE ISLAND · 1892')),
  ch('c20b', W(), "A snowy graveyard at night: two stickman farmers in heavy winter coats and hats stand apart by a lantern on the ground, holding shovels, looking grim."))
K('L20', "A vampire. They called me a vampire. I've been called worse.",
  kg('c21a', C(.5, .45, 1.1), "The White Lady sits on a snowy gravestone at night, laughing quietly, both hands resting on her knees."))

# ---- Koch
N('L21', "Then came Robert Koch. Using new dyes, he stained lung tissue and found the bacteria hiding inside. He grew them, put them into animals, and proved that they caused the disease.",
  dg('d19a', "Four numbered steps: (1) a glass slide with a drop of stain, (2) under a microscope, small purple rods appear, (3) a small glass dish with bacteria growing, (4) a guinea pig in a cage.", text=[cap('STAIN  ·  SEE  ·  GROW  ·  PROVE')]),
  ch('c22a', W(), "An 1880s laboratory: a single stickman scientist with small round glasses and a dark frock coat looks through a brass microscope, one hand adjusting it."))
N('L22', "His talk that day changed medicine. The twenty-fourth of March is now World Tuberculosis Day. Koch won the Nobel Prize in 1905.",
  sc('c22b', "A grand 1880s lecture library seen from the doorway, oil lamps glowing, a long table of microscopes, the chairs now empty. Lighting only from oil lamps and candles: no electric bulbs, no electric lamps.", WR()),
  dg('d20a', "A calendar page with one day circled, next to a simple gold medal on a ribbon.", text=[cap('24 MARCH: WORLD TB DAY')]))
N('L23', "But knowing the cause didn't give a cure. Koch's own remedy, tuberculin, was a failure as a treatment. It later became a useful skin test, to find out who carries her.",
  dg('d21a', "Two numbered panels: (1) a small glass vial with a cross over it, (2) a forearm with a tiny injection point and a small round red bump next to a ruler.", text=[cap('NOT A CURE  ·  BUT A TEST')]))
K('L24', "They knew my name at last. They just couldn't do anything about it.",
  kg('c23a', C(.5, .45, 1.1), "The White Lady sits on a laboratory stool in an empty 1880s lab, examining a microscope with polite curiosity."))

# ---- sanatoriums
N('L25', "So doctors prescribed rest, good food, and fresh air. Sanatoriums opened in the mountains and by the sea. Patients lay wrapped in blankets on open balconies, even in the snow, for months or years.",
  sc('c24a', "A large white Swiss mountain sanatorium building with long open balconies in the snowy Alps, pine forest, bright cold sky.", WL(), distant=True, text=cap('DAVOS, SWITZERLAND')),
  ch('c24b', W(), "A long open sanatorium balcony in winter: three stickman patients in wool hats lie on reclining wooden chairs wrapped in thick blankets, spaced apart, snowy mountains behind."),
  dg('d22a', "Three numbered icons: (1) a bed, (2) a plate of food with milk and eggs, (3) a mountain with fresh air lines.", text=[cap('REST  ·  FOOD  ·  FRESH AIR')]))
N('L26', "It helped some people, and it kept the sick away from their families. But many never came home.",
  sc('c24c', "An empty wooden reclining chair on a snowy sanatorium balcony at dusk, a folded blanket on it, mountains in the distance.", C(.5, .5, 1.05)))
K('L27', "Mountain air. Very pleasant. I came along for the view.",
  kg('c25a', C(.5, .45, 1.1), "The White Lady lounges on a reclining chair on an empty snowy sanatorium balcony, wrapped in a blanket, both hands holding a teacup, enjoying the mountain view."))

# ---- vaccine and cure
N('L28', "In 1921, two French scientists, Albert Calmette and Camille Guerin, made a vaccine called BCG. They weakened a cattle form of the bacteria by growing it over and over, two hundred and thirty times, for thirteen years.",
  ch('c26a', W(), "A 1910s laboratory at the Pasteur Institute: two stickman scientists in white coats stand apart at a bench with rows of small glass flasks, one holding up a flask."),
  dg('d23a', "A long row of small glass flasks connected by arrows, numbered (1) at the start and (2) at the end, with a calendar showing thirteen years and a small cow icon at the start.", text=[cap('230 TIMES  ·  13 YEARS  ·  BCG')]))
N('L29', "BCG protects young children well, and it is still given to millions of babies today. But it doesn't protect adults very well. They needed a cure.",
  ch('c26b', W(), modern=True, p="A modern clinic: a stickman nurse in blue scrubs holds a tiny syringe in one hand next to the upper arm of a baby, her other hand resting on her own hip; a stickman mother in a cardigan holds the baby in both arms; only these three figures, each nurse and mother with exactly two arms coming out of the shoulders, normal length."))
N('L30', "In 1943, in a lab in New Jersey, a young student, Albert Schatz, working under Selman Waksman, discovered streptomycin, an antibiotic found in soil bacteria. It was the first drug that could kill her.",
  sc('c27a', "A 1940s American university laboratory with soil samples in glass jars, petri dishes and a window onto a farm field. No flags, no banners, no pennants anywhere.", C(.5, .5, 1.05), text=cap('NEW JERSEY · 1943')),
  ch('c27b', W(), "A 1940s basement laboratory: a single young stickman student in a white coat holds up a petri dish to the light, smiling."),
  dg('d24a', "Three numbered steps: (1) a scoop of farm soil, (2) a petri dish with a clear ring around a mould colony, (3) a small medicine bottle.", text=[cap('SOIL  ·  BACTERIA  ·  STREPTOMYCIN')]))
N('L31', "Waksman alone won the Nobel Prize, and Schatz spent years fighting for credit. More drugs followed. Taken together, for months, they could finally cure her.",
  dg('d25a', "Three different simple pill shapes joined by a plus sign, then an arrow to a calendar of six months and a green tick.", text=[cap('SEVERAL DRUGS  ·  MONTHS  ·  CURED')]),
  sc('c28a', "A 1950s mobile chest X-ray van parked in a town square, its door open, a short queue line painted on the ground.", WR(), distant=True))
N('L32', "Mass X-ray vans toured towns and cities. Sanatoriums emptied, and closed. In rich countries, cases fell year after year.",
  dg('d26a', "A simple line chart falling steeply from left to right, with small sanatorium building icons along the top that become fainter.", text=[cap('CASES FALL')]),
  ch('c28b', W(), "A 1950s X-ray room: a single stickman man in a vest stands with his chest against a large X-ray plate, a stickman technician in a white coat apart behind a small screen."))
K('L33', "Pills. Little pills. Do you know how humiliating that is?",
  kg('c29a', C(.5, .45, 1.1), "The White Lady sits sulking in an empty 1950s pharmacy, staring at a small brown pill bottle on the counter in front of her."))

# ---- comeback & today
N('L34', "But she came back. In the 1980s and 90s, HIV weakened millions of immune systems, and she woke up in them. And when patients stopped their pills too early, she learned to survive the drugs.",
  dg('d27a', "Two numbered panels: (1) a sleeping bacterium inside a weakened round shield with cracks, waking up, (2) a bacterium with a small armour plate bouncing pills away.", text=[cap('WEAKENED DEFENCES  ·  DRUG RESISTANCE')]))
N('L35', "Today, she is once again the world's deadliest infectious disease. More than ten million people fall ill every year, and over a million die, mostly in Asia and Africa.",
  dg('d28a', "ONLY a simple world map filling the whole page: South Asia, Southeast Asia and Africa shaded dark, other regions pale. Nothing else, no pictures, no rows of panels, no ships.", text=[cap('10 MILLION SICK  ·  OVER 1 MILLION DEATHS A YEAR')]),
  ch('c30a', W(), modern=True, p="A busy modern clinic waiting room in South Asia: ONLY two stickman patients in everyday clothes and cloth face masks sit apart on plastic chairs, hands in their laps; nobody else in the room, no staff, no other patients."))
N('L36', "And yet, almost everyone can be cured, with a six-month course of cheap pills. The problem is not the medicine. It's getting it to the people who need it.",
  dg('d29a', "ONLY a single row of six simple blank calendar sheets across the page, each with one small white pill drawn on it, and a big green tick at the end. Nothing above or below, no other pictures, no digits.", text=[cap('6 MONTHS OF PILLS  ·  CURED')]),
  ch('c30b', W(), modern=True, p="A modern rural health worker in a vest walks along a dirt village road carrying a small medical bag, waving to a stickman family outside a house; the health worker and two family members, standing apart."))

# ---- WHAT SHE LEAVES BEHIND
N('A01', "And for those who survive? Many are left with scarred lungs, short of breath for life. Some carry her quietly, and she can wake again when they are old or ill.",
  dg('d30a', "Three numbered panels: (1) a pair of simple lungs with pale scar lines, (2) a stickman walking slowly up stairs, out of breath, (3) a small sleeping bacterium inside a knot, with a question mark.", people=True, text=[label('WHAT SHE LEAVES BEHIND', 960, 150, 72), cap('SCARRED LUNGS  ·  SHE CAN WAKE AGAIN')]))
N('A02', "For the world, she left more than graves. Sanatoriums inspired modern architecture: white walls, big windows, balconies and sunlight. The idea of tracing contacts and screening whole populations. And World Tuberculosis Day.",
  sc('c31a', "A white 1930s modernist building with flat roofs, long horizontal balconies, huge windows and sunlight, pine trees.", WL()),
  dg('d31a', "Three numbered icons: (1) a white modernist building with balconies, (2) a chain of connected stickman icons for contact tracing, (3) a chest X-ray image.", people=True, text=[cap('ARCHITECTURE  ·  CONTACT TRACING  ·  SCREENING')]))
K('A03', "They built whole buildings just to get away from me. I'm almost touched.",
  kg('c32a', C(.5, .45, 1.1), "The White Lady stands in a bright, empty white modernist sanatorium hall full of sunlight, looking up at the tall windows, both hands clasped in front of her."))

# ---- ending
N('L37', "Thousands of years. A billion lives, by some estimates. Not beaten by kings, poets or mountain air, but by a dye, a soil bacterium, and six months of pills. And she isn't finished yet.",
  sh('c01b', W()), sh('d19a', STILL), sh('c24a', W()), sh('d24a', STILL), sh('c30b', W()))
N('L38', "Next time: a killer that rides on the wings of a mosquito. It may have killed more people than any other disease in history.",
  sc('c33a', "A dark tropical swamp at night under a full moon, a single huge mosquito silhouette hovering over the water, mist. Ominous.", C(.5, .5, 1.04)))
HOLD(5.0, sh('c33a', O(), text=[label('NEXT TIME', 1380, 360, 110, style='title', pop=True, at=.2, len=4.6), label('SUBSCRIBE', 1380, 500, 64, at=.8, len=4.0)]))

# ---- extra cut-ins for faster cutting (pos None = end)
EXTRA = {
  'C01': [(None, sc('c01d', "A rack of small glass test tubes and a stack of handwritten notebooks on a wooden desk lit by a brass oil lamp with a glass chimney. Lighting only from oil lamps and candles: no electric bulbs, no electric lamps.", C(.5, .5, 1.05)))],
  'L01': [(None, sc('c06b', "A single candle melting in a dark room, thick layers of white wax dripping down, a metaphor for a waxy coat.", C(.5, .5, 1.05)))],
  'L03': [(None, sc('c07b', "Sunbeams through a dusty window in a dark crowded Victorian room, specks floating in the light.", C(.5, .5, 1.05)))],
  'L05': [(None, ch('c07c', W(), "A busy 1880s factory floor: two stickman workers in caps stand apart at a loom, both looking perfectly healthy."))],
  'L07': [(None, sc('c10d', "A dusty archaeological dig site with a small trench, brushes and tools, bones partly uncovered in the earth.", C(.5, .5, 1.05)))],
  'S01': [(None, sc('c12e', "A clock on a Victorian mantelpiece at evening, a thermometer in a glass beside it, a teapot.", C(.5, .5, 1.05)))],
  'S03': [(None, sc('c12f', "A white lace handkerchief lying on a dark wooden table beside a candle, three small red spots on it.", C(.5, .5, 1.05)))],
  'S04': [(None, ch('c12g', W(), "A Victorian doctor's room: a stickman doctor in a frock coat gently examines the neck of a stickman child sitting on a stool; only these two."))],
  'L11': [(None, sc('c14c', "An ancient Greek scroll and a clay oil lamp on a marble table, olive branches.", C(.5, .5, 1.05)))],
  'L12': [(None, sc('c15c', "A small medieval gold coin with an angel design on a red ribbon, lying on a red velvet cushion, a plain stone wall behind. No flags, no banners, no pennants anywhere.", C(.5, .5, 1.05)))],
  'L15': [(None, ch('c17c', W(), "A damp 1850s basement room: a single stickman mother in a shawl sits by a tiny window, rocking a cradle, mould on the walls."))],
  'L17': [(None, sc('c18d', "A small writing desk with an inkwell, a quill and a pile of poems, a vase of white lilies, soft window light.", C(.5, .5, 1.05)))],
  'L19': [(None, sc('c20c', "An old wooden farmhouse in snowy Rhode Island at night, one lit window, smoke from the chimney.", WR()))],
  'L21': [(None, sc('c22c', "Small glass bottles of bright blue and brown stains on a laboratory shelf in 1882, a dropper beside them.", C(.5, .5, 1.05)))],
  'L25': [(None, sc('c24d', "A snowy mountain village in the Alps with chalets and a small railway station, bright blue sky.", WR(), distant=True))],
  'L28': [(None, sc('c26c', "A row of 1920s glass culture flasks with yellowish medium on a shelf, a cow pasture through the window.", C(.5, .5, 1.05)))],
  'L30': [(None, sc('c27c', "A handful of dark rich farm soil in a glass dish on a lab bench, a microscope beside it.", C(.5, .5, 1.05)))],
  'L32': [(None, sc('c28c', "A 1950s chest X-ray film on a light box showing simple pale lungs, in a dim room.", C(.5, .5, 1.05)))],
  'L34': [(None, sc('c30c', "A modern hospital corridor with a sign-free isolation room door and a small round window, soft light.", C(.5, .5, 1.05), modern=True))],
  'L35': [(None, sc('c30d', "A crowded modern South Asian city street at dusk with buses, rickshaws and shop signs without readable words.", WL(), distant=True, modern=True))],
  'A01': [(None, ch('c31b', W(), "A modern park: a single elderly stickman in a cardigan sits on a bench catching his breath, a walking stick beside him.", modern=True))],
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
    out = {'base': 'assets/plague/ep07/frames', 'keep_zoom': [], 'fade_in': .8, 'start': 0.0, 'lead': .45, 'gap': .6, 'max_shot': 3.2,
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
