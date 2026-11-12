"""Episode 4 (The ENTIRE History of the Spanish Flu): single source of truth. Same format as ep03_spec.py.
Faster cutting (3-4 shots per line), ~20 explainer diagrams, mild camera only.

  python3 tools/plague/ep04_spec.py lines   -> voice list (id|ROLE|text), roles NARRATOR / FLU
  python3 tools/plague/ep04_spec.py frames  -> tools/plague/ep04_frames_todo.json
  python3 tools/plague/ep04_spec.py beats   -> tools/plague/ep04_beats.json (for beats.py)
"""
import sys, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
K_SHEET = 'd06e615f-e558-4cbd-bf64-9911c827908b'   # channel/plague/sheets/flu_turn.jpg
S_SHEET = '84427fc9-09ce-40e6-b032-6f2700874458'   # channel/plague/sheets/stickmen_common.jpg
STYLE = "2D animated history explainer frame, 16:9, no text. Hand-drawn ink illustration, clean black outlines, muted khaki-grey-sepia palette with cold blue-violet accents; warm light only from lamps, candles, lanterns. Not gory."
STICK = ("Humans are simple STICKMEN in the style of the attached stickman sheet: plain white round head, two dot eyes, no nose, no beard, thin black stick arms and legs, "
         "simple 1910s clothes. KEEP IT SIMPLE: only the few figures described, standing apart, never overlapping; each figure has exactly two arms "
         "and two hands, clearly attached to its own sleeves; nothing floating. No crowds, no ghost figures, no plague doctors.")
KING = ("The Spanish Flu exactly as on the attached sheet: a tall, lanky, charming young man in a long khaki-grey WWI army greatcoat worn open over a striped suit and waistcoat, "
        "a straw boater hat at a jaunty angle, a white gauze mask pulled down under his chin, pale feverish face with flushed red cheeks and a faint blue-violet tint on his lips "
        "and fingertips, bright too-friendly eyes and a wide charming grin; a white handkerchief and a slim walking cane. Exactly ONE of him, with exactly two arms and two hands.")
DIAG = ("A hand-drawn explainer diagram in ink and muted watercolour on aged paper, clean and readable like an old textbook plate, simple stickman figures "
        "(plain white round head, dot eyes, stick limbs, each with exactly two arms) where people appear, numbered stages as small circled digits with drawn arrows. "
        "No words, no letters, only circled digits. Not gory. ")

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
def stamp(t, **k): return {'text': t, 'x': 1380, 'y': 240, 'size': 96, 'style': 'stamp', 'pop': True, 'at': .5, **k}
def ch(img, cam, p, **k): return sh(img, cam, STICK + ' ' + p, 'S', **k)
def kg(img, cam, p, **k): return sh(img, cam, KING + ' ' + p, 'K', **k)
def dg(img, p, people=True, **k): return sh(img, STILL, (STICK + ' ' if people else '') + DIAG + p, 'S' if people else '', **k)

B = []
def N(i, t, *s): B.append((i, 'NARRATOR', t, list(s)))
def K(i, t, *s): B.append((i, 'FLU', t, list(s)))
def HOLD(sec, *s): B.append((None, None, sec, list(s)))

# ---- cold open: Kansas, March 1918
N('C01', "Kansas. The fourth of March, 1918. At an army training camp, a cook named Albert Gitchell reports to the infirmary with a fever, a sore throat and aching muscles.",
  sh('c01a', WL(), "A huge WWI army training camp on the flat Kansas prairie at dawn in 1918: rows of wooden barracks, a water tower, smoke from chimneys, frost on the ground. People only as tiny distant figures.", text=cap('CAMP FUNSTON, KANSAS · MARCH 1918')),
  ch('c01b', W(), "A 1918 army camp kitchen: a single stickman army cook in a white apron and cap stands by a big steaming pot, wiping his forehead, looking feverish."),
  ch('c01c', W(), "A 1918 army infirmary: the stickman cook sits on the edge of an iron bed while a stickman army nurse in a white uniform and cap holds a thermometer up to the light."),
  sh('c01d', C(.5, .5, 1.05), "A 1918 army sick-call book lying open on a wooden desk with an ink pen, a mug of coffee steaming beside it, morning light. No readable words. No people."))
N('C02', "By lunchtime, more than a hundred soldiers have the same symptoms. Within weeks, more than a thousand.",
  sh('c02a', W(), "A long 1918 army infirmary ward with many rows of iron beds with white sheets, seen down the length of the room, lamps, quiet. No people close up; beds look occupied only as blanket shapes."),
  sh('c02b', C(.5, .5, 1.1), "A wall clock in an army infirmary showing noon, next to a clipboard hanging on a nail with a long list of ticks. No people."),
  ch('c02c', W(), "Outside a wooden army barracks in the cold morning: two stickman soldiers in greatcoats help a third, pale and wrapped in a blanket, walk toward the infirmary, all standing apart enough to see each figure clearly."))
N('C03', "Over the next two years, he will infect around a third of everyone on Earth, and kill tens of millions. More people than the war that was raging at the same time.",
  dg('d01a', "A simple globe with about one third of it shaded blue-violet; beside it two stacks of small coffins compared side by side: a shorter stack with a tiny soldier helmet on top and a much taller stack with a tiny boater hat on top.", people=False, text=[cap('1 IN 3 INFECTED  ·  MORE DEATHS THAN THE WAR')]),
  sh('c03a', WR(), "A WWI battlefield at dusk seen from far away: trenches, barbed wire, a ruined tree, a grey sky. People only as tiny distant figures."),
  sh('c03b', W(), "A 1918 newspaper boy's empty stand on a city street corner, piles of papers with blank front pages weighed down by a brick, grey sky. No people."))
K('C04', "Don't look so worried. It's just the flu.",
  kg('c04a', C(.5, .45, 1.1), "Medium shot: the Spanish Flu leans casually on his cane outside a wooden army barracks in the morning frost, tipping his boater hat to the viewer with a wide charming grin."))
HOLD(4.6, kg('c05a', O(), "Title shot: the Spanish Flu stands on the left third of the frame on a foggy 1918 railway platform at night under a gas lamp, holding his cane, grinning; dark empty fog on the right side.")
     | {'text': [label('THE SPANISH FLU', 1300, 330, 130, style='title', pop=True, at=.15, len=4.2), label('1918 – 1920', 1300, 470, 80, style='title', color=[160, 170, 220], at=.5, len=3.9)],
        'sfx': [{'kind': 'boom', 'at': .1, 'gain': .8}]})

# ---- who is he
N('L01', "So who is he? A virus. Influenza A, of a type called H1N1. Tiny balls studded with two kinds of spikes.",
  sh('c06a', W(), "A 1918 laboratory bench with a brass microscope, glass test tubes and a notebook, lamp light. No people."),
  dg('d02a', "A large magnified round virus particle covered in two kinds of spikes: (1) long club-shaped spikes, (2) short mushroom-shaped spikes; a tiny scale comparison with a pin head in the corner.", people=False, text=[cap('INFLUENZA A  ·  H1N1')]),
  sh('c06b', C(.5, .5, 1.1), "Microscope view: a round bright field with many small spiky round virus particles; one in the centre wears a tiny straw boater hat. Cute but sinister."),
  dg('d02b', "Size comparison on aged paper: a big round cell like a fried egg, a small rod-shaped bacterium beside it, and a tiny spiky ball virus far smaller still, each marked with circled digits 1, 2, 3.", people=False))
N('L02', "The H spikes work like a key that unlocks the cells lining your nose and lungs. The N spikes are scissors that cut the new copies loose, so they can go and infect the next cell.",
  dg('d03a', "Three numbered steps: (1) a spiky virus touches a cell wall with a key-shaped spike and a door opens, (2) inside the cell many new small viruses are being copied, (3) small scissors-shaped spikes snip the new viruses free and they float away to the next cells.", people=False, text=[cap('H: THE KEY  ·  N: THE SCISSORS')]))
K('L03', "A key and a pair of scissors. That's all I need.",
  kg('c07a', C(.5, .45, 1.1), "The Spanish Flu twirls a big old brass key on one finger and holds a pair of tailor's scissors in the other hand, smirking, in a dim hotel corridor."))
N('L04', "He spreads through coughs, sneezes and hands. And you can pass him on a day before you even feel sick.",
  dg('d04a', "Three panels: (1) a stickman sneezing a cloud of tiny droplets toward another stickman a step away, (2) a stickman's hand on a door handle with tiny dots on it, then another hand touching it, (3) a calendar with day 1 marked: a smiling healthy-looking stickman already giving off faint dots.", text=[cap('COUGHS  ·  HANDS  ·  BEFORE SYMPTOMS')]),
  ch('c08a', W(), "A crowded 1918 tram car interior: three stickman passengers in hats sitting apart on wooden benches, one coughing into his fist, the others looking worried."),
  ch('c08b', W(), "A 1918 office: one stickman clerk sneezes into a handkerchief while another stickman clerk at the next desk leans away, both seated apart."))
# ---- WHAT HE DOES TO YOU
N('S01', "So what does he do to you? Usually, it hits all at once. A sudden high fever, a pounding headache, aching muscles and total exhaustion. Most people get better in about a week.",
  dg('d05a', "Two numbered panels: (1) a healthy stickman walking in the morning sun, (2) the same stickman by afternoon in bed with a thermometer, sweat drops, wavy heat lines and an ice bag on his head, holding his aching back.", text=[label('WHAT HE DOES TO YOU', 960, 150, 72), cap('FEVER  ·  HEADACHE  ·  ACHES  ·  EXHAUSTION')]),
  ch('c09a', W(), "A 1918 bedroom: a single stickman in pyjamas sits up in bed sipping soup from a bowl, a calendar on the wall with a week crossed off, recovering, smiling weakly."),
  sh('c09b', C(.5, .45, 1.1), STICK + " " + KING + " The Spanish Flu sits on the end of a sick stickman's bed, cheerfully fanning him with his straw boater hat; the stickman in the bed looks miserable under a blanket.", "KS"))
N('S02', "But in 1918, many cases went much further. The lungs filled with fluid, and the patient began to drown from the inside.",
  dg('d06a', "Side-by-side diagram of two pairs of simple cartoon lungs: (1) healthy pink lungs full of air bubbles, (2) lungs half filled with blue fluid like water in a glass, with tiny bubbles struggling.", people=False, text=[cap('HEALTHY LUNGS  ·  LUNGS FILLED WITH FLUID')]),
  ch('c10b', W(), "A 1918 hospital ward: one stickman nurse in a white cap and apron stands beside a bed holding a basin, looking anxious; the patient's bed is behind a white screen."))
N('S03', "Starved of oxygen, the skin turned blue, then deep purple. Doctors called it heliotrope cyanosis, after the colour of a flower. Some people were dead within a day of feeling the first symptom.",
  dg('d07a', "Three portraits of the same stickman's round face in a row with arrows: (1) normal white, (2) tinged pale blue around the lips and cheeks, (3) a deep violet tint; beside them a small purple heliotrope flower in a pot.", text=[cap('HELIOTROPE CYANOSIS')]),
  sh('c10a', C(.5, .5, 1.05), "Still life: a small pot of purple heliotrope flowers on a hospital windowsill, morning light, an empty iron bed in soft focus behind. Somber. No people."),
  ch('c10c', W(), "A 1918 doctor stickman in a white coat with a head mirror stands by a hospital bed looking at his pocket watch, worried, a nurse stickman apart from him holding a tray."))
N('S04', "And for many more, the flu opened the door to bacteria. They died a week or two later, of pneumonia. In 1918 there were no antibiotics to stop it.",
  dg('d08a', "Two panels: (1) a door in the shape of lungs opened by a small spiky virus, (2) through the open door a crowd of little rod-shaped bacteria rushes in; in the corner an empty medicine shelf with a cross over it.", people=False, text=[cap('THEN CAME THE BACTERIA')]))
K('S05', "I don't always finish the job. I just leave the door open.",
  kg('c11a', C(.5, .45, 1.1), "The Spanish Flu holds a hospital door open with one hand like a polite doorman, bowing slightly, the other hand behind his back; a dark corridor beyond."))

# ---- the strange part
N('L05', "And here's the strangest part. Flu usually kills the very young and the very old. This one also killed people in their twenties and thirties. Healthy, strong, young adults.",
  dg('d09a', "A hand-drawn graph on aged paper: a curve of deaths by age shaped like a big letter W, with high peaks at babies, at young adults about 20 to 40, and at old people; a dotted normal U-shaped curve for comparison beneath it. Small stickman icons under the axis: a baby, a young man, an old man.", text=[cap('BABIES  ·  YOUNG ADULTS  ·  THE ELDERLY')]),
  ch('c12a', W(), "Three young healthy stickman men in 1918 work clothes and caps stand apart on a factory yard, strong and smiling, lunch tins in their hands."),
  ch('c12b', W(), "A 1918 dance hall with a gramophone and paper lanterns: two young stickman couples dance far apart from each other, cheerful."))
N('L06', "Why? One idea is that strong immune systems overreacted, and destroyed the lungs while fighting him. Another is that older people had met a similar flu decades earlier, and still had some protection.",
  dg('d10a', "Two panels: (1) inside a stickman's chest, a huge army of tiny shield-bearing defender cells fighting a few viruses and accidentally smashing everything around them, (2) an old stickman with a small faded shield labelled only by a tiny old calendar page, standing calmly while viruses bounce off.", text=[cap('AN IMMUNE OVERREACTION?  ·  OLD PROTECTION?')]))
N('L06b', "There had been flu pandemics before. In 1889, the so-called Russian flu swept the world by train and steamship. Anyone who'd lived through that may have been a little better prepared for him.",
  dg('d10b', "A timeline on aged paper with two marked points: (1) an 1889 steam train and a small spiky virus, (2) a 1918 troopship and a bigger spiky virus; an old stickman stands under point 1 with a small faint shield he still carries at point 2.", text=[cap('1889  ·  1918')]),
  sh('c13b', WL(), "An 1889 railway station with a steam locomotive and wooden carriages under an iron roof, smoke and steam. People only as tiny distant figures."))
K('L07', "I like them young. They have so much energy.",
  kg('c13a', C(.5, .45, 1.1), "The Spanish Flu leans against a lamppost outside a dance hall at night, watching through the window with a hungry grin, tapping his cane in rhythm."))

# ---- origin
N('L08', "But where did he come from? Flu viruses live naturally in wild water birds, like ducks and geese. Every so often, one changes enough to jump into pigs, or straight into people.",
  sh('c14a', WL(), "A wide misty marsh at dawn with flocks of wild ducks and geese on the water and in the sky, reeds, a distant farm. No people."),
  dg('d11a', "A cycle diagram with arrows: (1) a wild duck, (2) a farm pig, (3) a stickman; small spiky virus icons travel along the arrows from the duck to the pig and to the stickman, and from the duck straight to the stickman.", text=[cap('BIRDS  ·  PIGS  ·  PEOPLE')]),
  sh('c14b', W(), "A muddy farmyard with pigs in a wooden pen and ducks swimming in a pond next to it, a barn behind. No people."))
N('L09', "The 1918 virus carried genes that look like they came from birds. But where it first crossed into humans, nobody knows. Kansas is one suspect. A British army camp in France is another. So is northern China.",
  dg('d12a', "An old world map on aged paper with three circled question marks drawn as small question-mark shapes in red ink: over central North America, over northern France, and over northern China. Small dotted lines between them. No people.", people=False, text=[cap('KANSAS?  ·  FRANCE?  ·  CHINA?')]),
  sh('c15a', WR(), "A WWI British army base camp in northern France with rows of tents and huts by the sea, grey sky, mud. People only as tiny distant figures."),
  sh('c15b', W(), "A northern Chinese village in 1917 with mud-brick houses and a dusty road, a group of labourers' bundles by a cart heading to a railway. People only as tiny distant figures."))
K('L10', "I'm a man of mystery. It's part of my charm.",
  kg('c16a', C(.5, .45, 1.1), "The Spanish Flu stands half in shadow under a streetlamp in fog, holding his boater hat over his heart, winking at the viewer."))
N('L11', "How do we know any of this? In 1997, a scientist named Johan Hultin travelled to a tiny village in Alaska, where the flu had killed almost every adult in 1918. Bodies buried in the frozen ground still held traces of the virus.",
  sh('c17a', W(), "A tiny snowy village on the coast of Alaska with a few wooden houses and a small white church under a pale sky, frozen sea. No people.", text=cap('BREVIG MISSION, ALASKA')),
  ch('c17b', W(), "An old stickman scientist with white hair, in a thick parka, kneels in the snow with a small pickaxe beside a shallow dig in frozen ground, a lantern beside him."),
  dg('d13a', "A cross-section diagram of frozen ground: snow on top, a layer of permanently frozen soil below shown with ice crystals, and deep inside it a tiny glowing virus symbol preserved in ice. No people.", people=False, text=[cap('FROZEN FOR 80 YEARS')]),
  sh('c17c', C(.5, .5, 1.05), "A small snow-covered cemetery of simple white wooden crosses on a hill by the frozen Alaskan sea, low winter sun. No people."))
N('L11b', "In November 1918, in that one village, seventy-two of its eighty or so adults died within five days.",
  dg('d13b', "Eighty small simple stickman icons arranged in neat rows on aged paper; most of them, seventy-two, are drawn faded grey with a tiny cross, and only a few at the end remain bright. No words.", text=[cap('72 OF ABOUT 80 ADULTS  ·  5 DAYS')]))
N('L12', "Together with old army tissue samples, it let scientists read his genes. And in 2005, they rebuilt the 1918 virus, inside a high security lab.",
  dg('d14a', "Four numbered steps: (1) a small frozen sample in a vial, (2) a long DNA strand being read like a ribbon of beads, (3) a stickman scientist in a full protective suit behind a glass window, (4) a single glowing spiky virus inside a sealed glass container.", text=[cap('1997  ·  2005: THE VIRUS REBUILT')]))
N('L12b', "Bringing him back was controversial. In tests, the rebuilt virus was far deadlier to lab mice than an ordinary flu. It's kept locked away in a top-security lab, and studied to help prepare for the next pandemic.",
  sh('c18b', W(), "A modern high-security laboratory corridor with heavy airlock doors, yellow warning stripes, a glass window and a red light above the door. No people."),
  dg('d14b', "Two lab cages side by side on aged paper: (1) with an ordinary small spiky virus and two lively mice, (2) with a spiky virus wearing a tiny boater hat and the mice lying still under a tiny blanket; a small padlock icon above the second cage.", people=False, text=[cap('ORDINARY FLU  ·  THE 1918 FLU')]))
K('L13', "Eighty years in the ice, and they still wouldn't let me rest.",
  kg('c18a', C(.5, .45, 1.1), "The Spanish Flu sits on an ice block in a snowy landscape, frost on his boater and eyebrows, arms folded, sulking."))

# ---- the name
N('L14', "So why Spanish? He wasn't Spanish. In 1918, the countries at war censored their newspapers, so they wouldn't hurt morale. Spain was neutral, and its press reported the outbreak freely. Even the Spanish king got sick.",
  ch('c19a', W(), "A 1918 newspaper office with a printing press: one stickman censor in a military uniform crosses out lines on a page with a big black pen. No readable words."),
  sh('c19b', W(), "Madrid in 1918: a sunny square with the royal palace, trams and kiosks with stacks of newspapers. People only as tiny distant figures.", text=cap('MADRID · MAY 1918')),
  ch('c19c', C(.5, .5, 1.05), "A royal bedroom: a stickman king with a small crown and a thin moustache drawn as a simple line lies in a grand bed with a thermometer in his mouth."),
  sh('c19d', C(.5, .5, 1.05), "A newspaper lying on a cafe table in Madrid next to a cup of coffee, its front page showing a drawing of a crown; no readable words."),
  ch('c19e', W(), "A Spanish newspaper office in 1918: a stickman editor in shirtsleeves and an armband happily typing on a typewriter, a stack of fresh newspapers beside him, no censor in sight."))
N('L15', "So the world assumed Spain was hit hardest, and the name stuck. In Spain, people called it the French flu.",
  dg('d15a', "A cartoon map of Western Europe: lots of countries covered with big black censor bars and padlocks, while Spain is open with a small loudspeaker on it and newspaper icons flying out of it. No words.", people=False, text=[cap('CENSORED  ·  CENSORED  ·  SPAIN: NOT CENSORED')]))
K('L16', "I am NOT Spanish! I did not even start in Spain!",
  kg('c20a', C(.5, .45, 1.1), "The Spanish Flu, outraged, waves his cane at a newspaper stand covered with blank newspapers, his face flushed, his boater hat bouncing."))

# ---- three waves
N('L17', "He came in three waves. A mild one in the spring of 1918. Then, that autumn, a far deadlier wave swept the world in a few months. And a third wave in early 1919.",
  dg('d16a', "A hand-drawn graph on aged paper of deaths over time from early 1918 to mid 1919: a small hump in spring 1918, an enormous sharp spike in October-November 1918, and a medium hump in early 1919, each hump marked with a circled digit 1, 2, 3.", people=False, text=[cap('SPRING 1918  ·  AUTUMN 1918  ·  WINTER 1919')]),
  sh('c21a', WL(), "A large 1918 city hospital at night with every window lit, ambulances and horse carts lined up outside in the rain. People only as tiny distant figures."),
  sh('c21b', W(), "A 1918 school gymnasium converted into an emergency hospital: rows of camp beds under the climbing ropes and basketball hoops. No people close up."))
N('L18', "The war helped him travel. Troopships packed with soldiers crossed the Atlantic, and trains carried them across whole continents. Tens of thousands of American soldiers died of flu and pneumonia, almost as many as were killed in battle.",
  sh('c22a', W(), "A huge grey WWI troopship at a harbour pier with smoke from its funnels, gangways, crates, a grey Atlantic sky. People only as tiny distant figures."),
  dg('d17a', "A world map on aged paper with thick arrows of troopship routes across the Atlantic and railway lines across Europe, North America and India, small spiky virus icons riding along every arrow.", people=False, text=[cap('BY SHIP AND BY TRAIN')]),
  ch('c22b', W(), "Below deck in a crowded 1918 troopship: three stickman soldiers in uniforms sit apart in narrow bunks, one coughing, a dim lamp swinging."),
  sh('c22c', WL(), "A long 1918 troop train stopped at a country station at dusk, soldiers' rifles stacked against the carriages, steam rising. People only as tiny distant figures."))
K('L19', "World war. Best travel deal of the century.",
  kg('c23a', W(), "The Spanish Flu lounges on a pile of soldiers' kit bags on the deck of a troopship at sea, hat tipped back, enjoying the sea breeze."))

N('L19b', "Governments at war didn't want panic. Officials called it ordinary influenza and told people not to worry. Newspapers printed cheerful advice, while the hospitals filled up.",
  ch('c23b', W(), "A 1918 government office: a stickman official in a dark suit speaks confidently at a small podium with a smile, holding up a blank leaflet."),
  dg('d17b', "A split image: (1) on the left a sunny newspaper front page with a big smiling sun drawing, (2) on the right the same day: a hospital with a long line of stretchers outside. No words.", text=[cap('WHAT THEY SAID  ·  WHAT WAS HAPPENING')]))
K('L19c', "Just the flu, they said. I do love a good understatement.",
  kg('c23c', C(.5, .45, 1.1), "The Spanish Flu reads a newspaper on a park bench, chuckling behind it, his cane leaning on the bench beside him."))
# ---- cities fight back
N('L20', "Cities tried to fight back, and how they did it made a huge difference. On the twenty-eighth of September, 1918, Philadelphia went ahead with a giant parade to sell war bonds. Around two hundred thousand people packed the streets.",
  sh('c24a', W(), "Broad Street in Philadelphia in 1918 decorated with American flags and bunting for a parade, a marching band in the distance, City Hall tower. People only as tiny distant figures.", text=cap('PHILADELPHIA · 28 SEPTEMBER 1918')),
  ch('c24b', W(), "Two stickman spectators in 1918 hats stand on a crowded pavement waving small flags, cheering at a parade going by."),
  sh('c24c', W(), "Paper bunting and flags fluttering above a crowded parade route in 1918, a brass band's tuba and drums glinting in the sun, seen from above. People only as tiny distant figures."))
N('L21', "Within three days, every hospital bed in the city was full. Within six weeks, more than twelve thousand people in Philadelphia were dead.",
  sh('c25a', W(), "A 1918 hospital corridor lined with extra iron beds and stretchers along both walls, a single lamp, quiet and grim. No people close up."),
  dg('d18a', "A calendar page of three days with each day crossed out, next to a simple hospital icon with a red full sign drawn as a solid red bar across its door. No people.", people=False, text=[cap('3 DAYS LATER: NO BEDS LEFT')]))
N('L21b', "Cities ran short of doctors, nurses, gravediggers and even coffins. Schools and churches became hospitals, and volunteers stepped in where the professionals had fallen ill.",
  sh('c25b', W(), "A carpenter's workshop in 1918 stacked to the ceiling with plain wooden boxes, sawdust on the floor, a single lamp. Somber. No people."),
  ch('c25c', W(), "A 1918 church turned into a hospital: two stickman volunteers, a woman with a Red Cross armband and a young man, carry a stack of folded blankets between the pews, walking apart."),
  dg('d18b', "Three numbered icons in a row on aged paper: (1) a doctor's black bag with a tiny cross, (2) a shovel, (3) a plain wooden box, each with a small red down-arrow showing shortage. No people.", people=False, text=[cap('NOT ENOUGH DOCTORS  ·  GRAVEDIGGERS  ·  COFFINS')]))
N('L22', "St. Louis did the opposite. Its health commissioner closed schools, theatres, churches and dance halls early. St. Louis suffered about half the death rate of Philadelphia.",
  ch('c26a', W(), "A St. Louis street in 1918: a theatre with closed doors and a padlock, an empty church with closed gates, and one stickman official in a suit nailing a blank notice to a door."),
  dg('d19a', "Two side-by-side hand-drawn graphs on aged paper: on the left a very tall sharp red spike (1), on the right a low, flat, gentle hill of the same width (2); a small parade drum icon under the left one and a small padlock icon under the right one.", people=False, text=[cap('PHILADELPHIA  ·  ST. LOUIS')]),
  ch('c26b', W(), "A 1918 health office: a stickman health commissioner in a suit and spectacles signs an order at his desk, a telephone and a map of the city behind him."))
K('L23', "St. Louis was no fun at all.",
  kg('c27a', C(.5, .45, 1.1), "The Spanish Flu stands alone in an empty closed street at dusk, looking at a padlocked theatre door, disappointed, hands in his greatcoat pockets."))
N('L24', "People wore gauze masks. In San Francisco, it became the law. Those who refused were fined, and in 1919, some formed an Anti-Mask League.",
  ch('c28a', W(), "A San Francisco street in 1918 with a cable car: two stickmen in hats wear white gauze face masks over their round heads, walking apart."),
  ch('c28b', W(), "A stickman policeman in a 1918 uniform writes a ticket for a stickman man in a bowler hat who is holding his gauze mask in his hand, arguing."))
N('L24a', "Across America, Red Cross volunteers sewed masks by the hundreds of thousands, from layers of cotton gauze.",
  ch('c28e', W(), "A 1918 Red Cross workroom: two stickman women volunteers in white aprons with red crosses sit at separate sewing machines making white gauze masks, a stack of finished masks on the table."),
  dg('d19c', "How a 1918 gauze mask was made, in four numbered steps on aged paper: (1) a roll of cotton gauze, (2) folded into several layers, (3) stitched at the edges, (4) tied on with four cotton strings over a stickman's mouth and nose.", text=[cap('GAUZE, FOLDED, STITCHED, TIED')]))
N('L24b', "People also tried everything else. Onions, garlic, camphor bags around the neck, whisky. And some doctors prescribed huge doses of aspirin, which may have poisoned some of the very patients they were trying to save.",
  sh('c28c', C(.5, .5, 1.05), "Still life of 1918 folk remedies on a kitchen table: a string of onions, garlic bulbs, a small cloth camphor bag on a string, a bottle of whisky and a glass. No people."),
  dg('d19b', "A big old glass medicine bottle of white pills tipped over, the pills spilling into a hand-drawn chart where a small safe dose and a huge 1918 dose are compared as two piles of pills, the huge one with a small skull symbol. No people.", people=False, text=[cap('THE ASPIRIN PROBLEM')]))
K('L24c', "Onions. Against me. Adorable.",
  kg('c28d', C(.5, .45, 1.1), "The Spanish Flu holds up a string of onions at arm's length with two fingers, wrinkling his nose in amused disgust."))
N('L25', "Isolation could work wonders. In 1918, a ship from New Zealand brought the flu to Western Samoa, and about one in five people there died. Next door, the governor of American Samoa quarantined the islands. Not a single person died of flu.",
  dg('d20a', "Two neighbouring tropical island groups on a sea chart: the left islands (1) with a steamship arriving and many small black crosses over the villages; the right islands (2) circled by a ring of small buoys and a closed gate symbol, with no crosses at all, a small green tick above them.", people=False, text=[cap('WESTERN SAMOA: 1 IN 5  ·  AMERICAN SAMOA: ZERO')]),
  sh('c29a', W(), "A calm tropical harbour in Samoa with palm trees and thatched fale houses, a small steamship anchored far out at sea, a wooden barrier across the jetty. No people close up."),
  sh('c29b', W(), "A small steamship at a tropical wooden pier in 1918, crates being unloaded under palm trees, a cloudy sky. People only as tiny distant figures."))
K('L26', "A closed harbour. How terribly rude.",
  kg('c30a', C(.5, .45, 1.1), "The Spanish Flu stands in a small rowing boat at sea, staring at a closed tropical harbour gate, mopping his feverish forehead with his handkerchief."))

N('L26b', "No country lost more people than India. As many as twelve million or more died there, in just a few months. Among those who fell ill was a forty-nine-year-old lawyer named Mohandas Gandhi. He survived.",
  sh('c30b', WL(), "Bombay harbour in 1918: steamships at the docks, colonial buildings, the Gateway area under a hazy sky, the sea. People only as tiny distant figures.", text=cap('BOMBAY · 1918')),
  dg('d20b', "A hand-drawn bar chart on aged paper of deaths by country: one enormous bar (1) with a small map outline of India next to it, and several much shorter bars beside it with tiny map outlines of other countries. No words.", people=False, text=[cap('INDIA: THE HARDEST HIT')]),
  ch('c30c', W(), "A simple 1918 Indian house interior: a thin bald stickman with small round glasses wrapped in a white shawl rests on a low bed, a cup of water beside him.", text=cap('MOHANDAS GANDHI · 1918')))
# ---- famous
N('L27', "Nobody was too important. President Woodrow Wilson caught it in 1919, during the peace talks in Paris. A sixteen-year-old named Walt Disney survived it. The painter Edvard Munch drew himself recovering.",
  ch('c31a', W(), "A grand 1919 Paris hotel bedroom: a stickman with small round glasses and a long serious face, in a dark suit, lies propped up in bed with papers on the blanket.", text=cap('WOODROW WILSON · PARIS 1919')),
  ch('c31b', W(), "A 1918 small-town room: a teenage stickman with a cap sits on a bed with a blanket over his shoulders, sketching little cartoon animals in a notebook.", text=cap('WALT DISNEY · 16')),
  ch('c31c', W(), "A 1919 painter's studio: a thin stickman artist in a dressing gown sits wrapped in a blanket in an armchair beside an easel with a blank canvas.", text=cap('EDVARD MUNCH')),
  ch('c31d', W(), "A Vienna art studio in 1918: an empty easel with an unfinished painting, a thin young stickman painter lying on a sofa under a blanket, brushes in a jar."))
N('L27b', "And then, by 1920, he faded. So many people had caught him and survived that he ran out of easy victims. Slowly, he turned into ordinary seasonal flu.",
  dg('d21b', "Three numbered panels: (1) a crowd of stickmen, most of them unshielded, a big spiky virus jumping between them, (2) the same crowd, now most holding small round shields, the virus bouncing off, (3) the virus small and tired, sitting alone.", text=[cap('1918  ·  1919  ·  1920')]),
  sh('c31e', W(), "A 1920 city street on a sunny spring day: open shop doors, a tram, bunting, a cinema with its doors open again. People only as tiny distant figures."))
# ---- WHAT HE LEAVES BEHIND
N('A01', "And for those who survived? Many were weak for weeks. Some had heart and lung problems for years. And children who were still in the womb during the pandemic grew up, on average, a little less healthy and a little poorer.",
  dg('d21a', "Three panels: (1) a pale stickman walking slowly with a cane and a blanket, (2) a simple heart and lungs drawn with small crack lines, (3) a pregnant stickman woman in 1918, an arrow, and the grown-up child decades later with a slightly smaller money bag and a small plaster on his forehead.", text=[label('WHAT HE LEAVES BEHIND', 960, 150, 72), cap('WEAK FOR WEEKS  ·  HEART AND LUNGS  ·  THE NEXT GENERATION')]),
  ch('c32b', W(), "A 1919 park bench: a thin pale stickman in a coat and scarf sits resting, a walking stick beside him, autumn leaves falling."))
N('A02', "And for the world? Many countries set up their first health ministries. Scientists began tracking flu around the globe. And they started building flu vaccines.",
  dg('d22a', "Three panels: (1) a stately government building with a medical cross emblem over its door, (2) a world map with small observation stations linked by dotted lines, (3) a 1940s glass vial and a syringe.", people=False, text=[cap('HEALTH MINISTRIES  ·  GLOBAL FLU WATCH  ·  VACCINES')]),
  sh('c32c', W(), "A grand 1919 government building in London with a new brass plaque by the door showing only a medical cross symbol, a black car outside. No people."))
K('A03', "I made the world take flu seriously. You're welcome.",
  kg('c32a', C(.5, .45, 1.1), "The Spanish Flu takes a theatrical bow in an empty 1920s ballroom, sweeping off his boater hat, his cane under his arm."))

# ---- today
N('L28', "So is he gone? Not quite. His descendants still circulate. The 2009 swine flu pandemic carried genes that came from him.",
  dg('d23a', "A family tree drawn on aged paper: at the top one spiky virus with a tiny boater hat labelled only with a circled 1, branching down through several generations of smaller spiky viruses to a modern one at the bottom with a tiny pig snout, circled 2.", people=False, text=[cap('1918  ·  2009')]),
  sh('c33a', W(), "A modern hospital corridor in 2009 with blue chairs and a hand sanitiser dispenser, clean and bright. No people."))
N('L29', "Every year, seasonal flu still kills hundreds of thousands of people worldwide. Twice a year, experts pick which strains go into the next flu vaccine.",
  ch('c34a', W(), "A modern clinic: a stickman nurse in blue scrubs gives a flu jab in the arm of a stickman man in a T-shirt who is smiling, both standing apart a little."),
  dg('d24a', "A calendar wheel of twelve months with two highlighted points opposite each other, and from each a small vaccine vial with arrows to a globe. No people.", people=False, text=[cap('A NEW VACCINE EVERY SEASON')]),
  ch('c34b', W(), "A modern laboratory: a single stickman scientist in a white coat and safety glasses looks at a rack of small sample tubes under bright light."))
K('L30', "I never really left. I just changed my hat.",
  kg('c35a', C(.5, .45, 1.1), "The Spanish Flu stands in a modern city street at night, swapping his straw boater for a modern baseball cap, winking at the viewer."))
N('L31', "Two years. Three waves. Around fifty million lives. Beaten not by a cure, but by closed doors, quarantined harbours, and the science he forced us to build.",
  sh('c01a', W()), sh('c24a', W()), sh('d19a', STILL), sh('c29a', W()), sh('c17a', W()))
N('L32', "Next time: a killer that didn't need a germ at all. For centuries it stalked sailors on long voyages, and it was finally beaten by a lemon.",
  sh('c36a', C(.5, .5, 1.04), "Night on the deck of an 18th-century sailing ship in mist: the dark silhouette of a gaunt captain in a tricorn hat and long coat holding a lantern stands by the mast; a wooden crate of bright yellow lemons at his feet. Ominous."))
HOLD(5.0, sh('c36a', O(), text=[label('NEXT TIME', 1380, 360, 110, style='title', pop=True, at=.2, len=4.6), label('SUBSCRIBE', 1380, 500, 64, at=.8, len=4.0)]))

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
    json.dump(out, open(os.path.join(ROOT, 'tools/plague/ep04_frames_todo.json'), 'w'), indent=1); print(len(out), 'frames')

def beats():
    out = {'base': 'assets/plague/ep04/frames', 'fade_in': .8, 'start': 0.0, 'lead': .45, 'gap': .6, 'max_shot': 3.2,
           'sfx_global': [{'kind': 'drone', 't': 0.0, 'args': {'d': 'ALL'}, 'gain': .9}, {'kind': 'wind', 't': 0.0, 'args': {'d': 'ALL'}, 'gain': .1}], 'beats': []}
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
        if i: out['beats'].append({'vo': f'assets/plague/ep04/vo/{i}.wav', **({'gain': 1.05} if r == 'FLU' else {}), 'shots': sl})
        else: out['beats'].append({'hold': t, 'shots': sl})
    json.dump(out, open(os.path.join(ROOT, 'tools/plague/ep04_beats.json'), 'w'), indent=1); print(len(out['beats']), 'beats')

MUSIC = [(0, 162, 'cholera_a.mp3'), (158, 322, 'cholera_b.mp3'), (318, 468, 'cholera_a.mp3'), (464, 'ALL', 'cholera_b.mp3')]   # intro+symptoms | origin+name+waves | cities+India | aftermath+today

{'lines': lines, 'frames': frames, 'beats': beats}[sys.argv[1]]()
