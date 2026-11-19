"""Episode 10 (The ENTIRE History of Polio): single source of truth. Same format as ep10_spec.py, with the retention rules
(static camera, a person in trouble in the first second, characters in almost every frame, natural captions) and the strict anatomy rules.

  python3 tools/plague/ep10_spec.py lines   -> voice list (id|ROLE|text), roles NARRATOR / POLIO
  python3 tools/plague/ep10_spec.py frames  -> tools/plague/ep10_frames_todo.json
  python3 tools/plague/ep10_spec.py beats   -> tools/plague/ep10_beats.json (for beats.py)
"""
import sys, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EP = 'ep10'
K_SHEET = '7f8fbe81-10a4-4c1a-9376-a30df5b7f2c7'   # channel/plague/sheets/polio_a.jpg ('Mr. Summer'), Higgsfield upload
STYLE = ("2D animated history explainer frame, 16:9, no text. Hand-drawn ink illustration, clean black outlines, muted 1950s palette of faded pool turquoise, "
         "sun-bleached cream and sepia with small red accents and warm summer light. Not gory.")
MODERN = ("2D animated history explainer frame, 16:9, no text. Hand-drawn ink illustration, clean black outlines, the same muted turquoise, cream and sepia palette, "
          "soft natural daylight. The setting is modern (2000s-2020s): nothing old-fashioned. Not gory.")
SN = ("Humans are simple STICKMEN: plain white round head, two dot eyes, no nose, no beard, thin black stick arms and stick legs, small black mitten hands, "
      "dressed exactly as described for this scene and era; anyone wearing glasses has his two dot eyes INSIDE the lenses and no other eyes. "
      "Only the few figures described, standing apart, never overlapping; each has exactly two arms and two hands; every arm comes straight out of its own shoulder "
      "and never bends around or behind an object; head, body and feet of each figure face the same way, no twisted bodies; "
      "hands are empty unless an object is described; nothing floating; no flags; no readable text.")
KING = ("Polio exactly as on the attached sheet, 'Mr. Summer': a tall, thin 1950s American gentleman with an unnaturally wide friendly salesman grin, pale grey-blue skin, "
        "hollow dark eyes, slicked-back hair, a cream-and-pale-blue striped seersucker suit, a red bow tie and a straw boater hat with a red band; his trouser hems and shoes "
        "are wet and drip pool water into small puddles. Exactly ONE of him, with exactly two arms and two hands with normal-length fingers; each arm comes from its own shoulder; "
        "no extra hands anywhere in the picture. He holds AT MOST ONE object, his other hand empty and clearly attached to its own arm.")
DIAG = ("Draw ONLY the diagram described below, filling the whole frame, as ONE single picture: no extra rows, no extra panels, no comic strips above or below it. "
        "A hand-drawn explainer diagram in ink and muted watercolour on aged paper, clean and readable like an old textbook plate, "
        "numbered stages as small circled digits with drawn arrows. No words, no letters, no numbers on axes, only circled digits. Not gory. ")
NOPEOPLE = ' No people and no human figures anywhere in the picture.'
LAMPS = ''
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
def K(i, t, *s): B.append((i, 'POLIO', t, list(s)))
def HOLD(sec, *s): B.append((None, None, sec, list(s)))
def K(i, t, *s): B.append((i, 'POLIO', t, list(s)))

BOY = "a ten-year-old stickman boy with a crew cut drawn as a small dark shape on top of his round white head, in a striped 1950s T-shirt and denim shorts"
WARD = "a large bright 1950s hospital ward with tall windows, white walls and a long row of big cream-coloured metal iron lung machines (sealed cylinders on legs with small round portholes)"

# ---- cold open: the boy from the pool (1952)
N('C01', "A boy comes home from the town swimming pool with a headache. By the next morning, he can't move his legs. By evening, he can't breathe on his own.",
  ch('c01a', C(.5, .5, 1.05), f"A sunny 1950s American small-town public swimming pool with a diving board and a chain-link fence: {BOY} walks out of the pool gate with a rolled-up towel under one arm, rubbing his forehead with his other hand, looking unwell.", text=cap('Summer, 1952')),
  ch('c01b', W(), f"A 1950s American child's bedroom in the morning with a model airplane on a shelf: {BOY} sits up in bed in pyjamas, staring in fear at his own legs under the blanket, both hands pressed flat on the mattress, while his stickman mother in a 1950s house dress and apron rushes in through the doorway with both arms out.", text=cap("By morning, he can't move his legs")),
  ch('c01c', C(.5, .5, 1.05), f"Inside {WARD}: the stickman boy's head rests on a pillow sticking out of the round end of one iron lung machine, the rest of his body hidden inside the sealed cylinder; a stickman nurse in a white 1950s uniform and cap stands beside it, adjusting a dial on the machine with one hand.", text=cap("By evening, he can't breathe")))
N('C02', "He's put inside a giant metal tube that breathes for him. Around him, row after row of children in the same machines. That summer, nearly fifty-eight thousand Americans caught the same disease.",
  ch('c02a', WL(), f"A wide view of {WARD} with eight iron lung machines in a long row, a small stickman child's head resting on a pillow at the end of each one, two stickman nurses in white uniforms walking apart between them.", text=cap('Row after row of iron lungs')),
  dg('d01a', "ONLY a simple bar chart with no numbers: a row of bars rising over several years to one very tall bar on the right, the tall bar coloured red, with a tiny sun icon above it.", text=[cap('1952: nearly 58,000 cases')]))
N('C03', "Parents closed the pools, the cinemas and the summer camps. They kept their children inside. And every summer, they waited to see whose child would be next.",
  ch('c03a', C(.5, .5, 1.05), "A 1950s American public swimming pool on a hot sunny day, completely empty, with a chain-link gate: a stickman official in a short-sleeved shirt and tie is hanging a padlock on the gate with both hands, while a stickman girl in a swimsuit and holding a towel stands a step apart, looking sad.", text=cap('The pools closed')),
  ch('c03b', W(), "A 1950s suburban living room on a sunny afternoon: a stickman mother in a house dress stands at the window, pulling the curtains closed with both hands, while two stickman children sit apart on the rug, looking out wistfully.", text=cap('Children kept inside')))
K('C04', "Every summer, the same lovely game. Who gets to swim, and who stays home?",
  kg('c04a', C(.5, .45, 1.1), "Medium shot: Mr. Summer stands at the edge of an empty 1950s swimming pool in bright sunshine, tipping his straw boater hat with one hand and grinning at the viewer, his other hand in his pocket; water drips from his trouser hems into a puddle."))
HOLD(4.6, kg('c05a', O(), "Title shot: Mr. Summer stands on the left third of the frame on a deserted 1950s small-town street at sunset, between a closed ice-cream stand and a padlocked swimming pool gate, both hands resting on a closed striped beach umbrella planted in front of him like a cane; the right side of the frame is an empty orange sunset sky.")
     | {'text': [label('POLIO', 1300, 330, 140, style='title', pop=True, at=.15, len=4.2), label('THE SUMMER PLAGUE', 1300, 470, 72, style='title', color=[120, 200, 210], at=.5, len=3.9)],
        'sfx': [{'kind': 'boom', 'at': .1, 'gain': .8}]})

# ---- who is he
N('L01', "So who is he? A virus. Poliovirus. One of the smallest viruses we know: a tiny ball of genetic code, so small that a million of them would fit across the head of a pin.",
  dg('d02a', "A scale comparison: a small round ball-shaped virus particle with a faceted surface like a tiny football (1), next to a pin head drawn huge and round (2) with a dotted line showing the tiny virus is minuscule beside it."),
  kg('c06a', C(.5, .45, 1.1), "Mr. Summer bends down beside a 1950s swimming pool and peers through a brass magnifying glass held in one hand at a single drop of water on his fingertip, grinning; his other hand is the one with the drop.", text=cap('Poliovirus')))
N('L02', "He travels through dirty water and dirty hands. You swallow him, and he settles in your gut. Most of the time, nothing happens at all.",
  dg('d03a', "Three numbered steps in one row: (1) a hand under a tap with dirty water, (2) a simple outline of a person's belly with tiny round virus dots in the gut, (3) the same person smiling with a green tick.", text=[cap('Water, hands, mouth')]),
  ch('c07a', W(), "A busy 1950s community swimming pool on a hot day: two stickman children in swimsuits splash and laugh in the water, a stickman boy on the side drinks from a public water fountain with both hands on its rim.", text=cap('Most people never notice him')))
N('L03', "About three in four people infected never feel sick. Most others get a mild fever, like the flu. But in about one in two hundred, he slips out of the gut, into the nerves of the spine.",
  dg('d04a', "ONLY a single long row of twenty simple stickman icons across the page: nineteen of them plain and smiling, and one of them coloured red and lying down. Nothing else, no other rows.", text=[cap('About 1 in 200 is paralysed')]),
  dg('d05a', "A simple side view of a human spine with the spinal cord drawn as a bright cable, (1) tiny virus dots climbing into it from below, (2) a few nerve cells along it turning grey.", text=[cap('Into the spinal cord')]))
K('L04', "Hundreds of easy little visits, and nobody suspects a thing. Then, once in a while, I stay.",
  kg('c08a', C(.5, .45, 1.1), "Mr. Summer leans casually on the counter of a 1950s soda fountain, sipping a milkshake through a red-and-white straw from a tall glass held in one hand, winking at the viewer; his other hand rests flat on the counter."))
N('L05', "There, he destroys the nerve cells that move your muscles. The muscles they controlled go limp, usually in the legs. If he reaches the nerves for breathing, the chest stops moving.",
  dg('d06a', "Two numbered panels in one row: (1) a nerve cell sending a little lightning bolt down a line to a muscle shaped like a sausage, (2) the same nerve cell greyed out and broken, the lightning gone, the muscle limp.", text=[cap('The nerves die, the muscles go limp')]))

# ---- origin
N('L06', "Where did he come from? He's ancient. A carved stone from Egypt, about three and a half thousand years old, shows a priest with one thin, withered leg, leaning on a staff.",
  ch('c09a', C(.5, .5, 1.05), "A dim modern museum gallery with a large ancient Egyptian painted limestone stele on display under a spotlight, the carving showing a figure with a staff and one thin leg: a stickman visitor in a modern jacket stands in front of it looking closely, hands in his pockets.", modern=True, text=cap('Egypt, about 1400 BC')),
  dg('d07a', "A simple drawing in ancient Egyptian carved style: a standing man in a white kilt holding a long staff, one of his legs visibly thinner and shorter with the foot pointed down.", text=[cap('A withered leg')]))
N('L07', "For thousands of years, nearly every baby caught him in dirty water, while still protected by their mother's antibodies. The infection was mild, and it made them immune for life.",
  ch('c10a', W(), "A busy 19th-century village street with an open drain and a shared water pump: a stickman mother in a long skirt and shawl fills a wooden bucket at the pump with one hand while holding a baby on her hip with her other arm.", text=cap('Babies caught him early')))
N('L08', "Then, in the late eighteen hundreds, came clean water, sewers and soap. Babies stopped catching him. They met him later, as older children, without protection. And that's when the epidemics began.",
  dg('d08a', "Two numbered panels in one row: (1) a baby with a small shield beside it next to a dirty water pump, (2) a clean modern tap and a bigger child with no shield, a large virus ball approaching.", text=[cap('A disease of cleanliness')]))
K('L09', "You cleaned up your cities. How thoughtful. I'd never had such a lovely summer.",
  kg('c11a', C(.5, .45, 1.1), "Mr. Summer sits on a park bench beside a gleaming new 1900s public water fountain in a tidy city park, smiling contentedly with both hands folded on the handle of a closed striped beach umbrella."))

# ---- WHAT HE DOES TO YOU
N('S01', "So what does he do to you? It starts like summer flu: a fever, a sore throat, a headache, an aching back and a stiff neck.",
  dg('d09a', "A simple stickman outline with three numbered magnifier circles: (1) a thermometer by the head, (2) a sore red throat, (3) the neck drawn stiff with small strain lines.", people=True, text=[label('What He Does to You', 960, 150, 72), cap('It starts like summer flu')]),
  ch('c12a', C(.5, .5, 1.05), "A 1950s American kitchen: a stickman mother in a house dress holds the back of her hand to the forehead of her stickman daughter in a summer dress, who sits at the table with flushed cheeks, holding her stiff neck with one hand.", text=cap('A stiff neck')))
N('S02', "Then, within days, some patients feel their muscles weaken. A leg won't hold them up. An arm won't lift. The paralysis comes fast, and it's often lopsided.",
  ch('c12b', W(), f"A 1950s child's bedroom: {BOY} tries to stand up beside his bed but his legs buckle under him, both hands gripping the bedside table to hold himself up, his face scared.", text=cap("A leg won't hold him up")),
  dg('d10a', "A simple standing stickman outline with one leg drawn normally and the other leg tinted grey, thin and limp, with a numbered circle (1) on the grey leg.", people=True, text=[cap('Often just one side')]))
N('S03', "When he attacks the nerves of the chest, you can no longer breathe. Without help, you suffocate.",
  dg('d11a', "Two numbered panels in one row: (1) a ribcage and lungs with arrows showing breathing in and out, (2) the same ribcage with the arrows crossed out and the lungs pale.", text=[cap('The breathing muscles stop')]))
N('S04', "About one in ten of the paralysed died. Many survivors walked again. But many spent their lives in leg braces, on crutches, or in wheelchairs.",
  ch('c12c', W(), "A sunny 1950s school playground: a stickman boy wearing metal leg braces walks with two wooden crutches, smiling, while a stickman girl in a dress walks beside him a step apart, carrying a lunchbox in one hand.", text=cap('Leg braces and crutches')))
K('S05', "Fever, aches, a stiff neck. Who would worry? That's the beauty of it.",
  kg('c13a', C(.5, .45, 1.1), "Mr. Summer stands in a sunny 1950s suburban street holding a red ice-lolly in one hand, licking it, and giving a little innocent wave with his other hand, grinning slyly."))

# ---- early epidemics
N('L10', "In 1894, in Vermont, the first big American outbreak paralysed one hundred and thirty-two people, most of them children. Doctors had no idea what it was.",
  ch('c14a', WL(), "A quiet 1890s Vermont farm town with white wooden houses, a church and green hills: a stickman country doctor in a dark coat and bowler hat gets down from a horse-drawn buggy holding a leather medical bag in one hand.", text=cap('Vermont, 1894')))
N('L11', "In 1908, in Vienna, Karl Landsteiner showed that it was caused by something too small to see, passing it to monkeys. He had found a virus.",
  ch('c14b', C(.5, .5, 1.05), "A 1908 Vienna laboratory with tall windows, glass flasks and a brass microscope: a stickman scientist with small round glasses and a dark suit under a white coat holds up a small glass flask of clear liquid to the light with one hand, his other hand on the bench; a monkey sits in a cage in the background.", text=cap('Karl Landsteiner, 1908')))
N('L12', "In 1916, he hit New York. More than two thousand people died there, most of them children. Families fled the city, and houses with a sick child were marked with a warning sign.",
  ch('c15a', W(), "A 1916 New York City tenement street with fire escapes and laundry lines: a stickman health officer in a dark uniform and peaked cap nails a blank white quarantine card to a front door with a hammer held in one hand, while a stickman mother in a long 1910s skirt watches from the window above.", text=cap('New York, 1916')),
  dg('d12a', "A simple map outline of the island of Manhattan with many small red dots spreading across it.", text=[cap('More than 2,000 deaths in the city')]))
K('L13', "New York in 1916. My first really big city. I was a sensation.",
  kg('c16a', C(.5, .45, 1.1), "Mr. Summer stands on a 1916 New York street corner at night under a gas street lamp, tipping his straw boater to the viewer with one hand, his other hand on his hip, grinning, tall buildings behind him."))

# ---- FDR and the March of Dimes
N('L14', "In 1921, he caught a rising politician: Franklin Delano Roosevelt, thirty-nine years old. After a swim on holiday, his legs stopped working. They never worked again.",
  ch('c17a', WL(), "A rocky Canadian island seashore in summer 1921 with a large shingled summer cottage and pine trees: a tall stickman man in an old-fashioned 1920s one-piece bathing suit walks out of the cold sea, hugging himself and shivering.", text=cap('Franklin D. Roosevelt, 1921')),
  ch('c17b', C(.5, .5, 1.05), "A 1920s cottage bedroom: a stickman man with small round glasses (his two dot eyes inside the lenses) in pyjamas lies in bed, looking down at his legs under the blanket with a worried face, both hands resting on top of the blanket.", text=cap('His legs never worked again')))
N('L15', "He became President, and hid his wheelchair from the public. But in 1938, he founded a charity to fight polio. A comedian suggested a name: the March of Dimes. Americans mailed millions of dimes straight to the White House.",
  ch('c18a', W(), "The mailroom of the White House in 1938 overflowing with letters and envelopes: two stickman clerks in white shirts, waistcoats and sleeve garters stand apart among huge heaps of mail sacks, one of them holding up a single silver dime in one hand and smiling.", text=cap('The March of Dimes, 1938')),
  ob('c18b', "A huge heap of silver dime coins spilling out of a torn canvas mail sack onto a wooden floor, warm light.", text=cap('Millions of dimes')))
K('L16', "A President against me. And millions of children with their pocket money. I didn't see that coming.",
  kg('c19a', C(.5, .45, 1.1), "Mr. Summer sits sulking on a bench outside a grand white building with columns, picking up one small silver dime from the ground between finger and thumb of one hand and frowning at it, his other hand on his knee."))

# ---- the iron lung, Sister Kenny
N('L17', "Meanwhile, in 1928, two Harvard engineers built a machine to breathe for the paralysed: the iron lung. It changed the air pressure around the body, pulling air in and out of the lungs.",
  ch('c20a', WL(), "A 1928 Harvard laboratory workshop: two stickman engineers in waistcoats and rolled-up shirtsleeves stand apart beside a big newly built metal cylinder on legs, one of them tightening a bolt with a spanner held in one hand, the other holding a blueprint.", text=cap('The iron lung, 1928')),
  dg('d13a', "A simple cross-section of an iron lung machine: a person lying inside a sealed cylinder with only the head outside, (1) a pump at the end making the air pressure drop, (2) arrows showing the chest rising, (3) arrows showing air flowing into the mouth.", people=True, text=[cap('It breathed for you')]))
N('L18', "One boy, Paul Alexander, was put into an iron lung in 1952. He learned to breathe on his own for a few hours a day, became a lawyer, and wrote a book with a pen held in his mouth. He lived in his iron lung for seventy years.",
  ch('c20b', C(.5, .5, 1.05), "A cosy modern living room with bookshelves: an elderly stickman man's head rests on a pillow at the end of an old cream-coloured iron lung machine, holding a pen in his mouth and writing on a sheet of paper on a small stand in front of his face.", modern=True, text=cap('Paul Alexander: 70 years in an iron lung')))
N('L19', "An Australian nurse, Sister Elizabeth Kenny, fought doctors who put paralysed limbs in rigid casts. She used hot wet packs and gentle exercise instead. Patients got moving again.",
  ch('c21a', W(), "A 1940s hospital physiotherapy room: a stickman nurse in a white 1940s nurse's uniform and a tall white veil-like cap gently bends the leg of a stickman child lying on a treatment table, holding the knee in one hand and the ankle in the other; a steaming tub of hot wool cloths beside them.", text=cap('Sister Elizabeth Kenny')))

# ---- Salk
N('L20', "Then came Jonas Salk. In Pittsburgh, he grew the virus, killed it with formaldehyde, and made a vaccine from the dead virus. He tested it on himself and his own family.",
  ch('c22a', C(.5, .5, 1.05), "A 1950s Pittsburgh laboratory with rows of glass flasks and test tubes: a stickman scientist with small dark-framed glasses (his two dot eyes inside the lenses) and a white lab coat holds up a test tube to the light with one hand, his other hand on the bench.", text=cap('Jonas Salk')),
  dg('d14a', "Three numbered steps in one row: (1) a glass flask with virus balls, (2) a bottle of formaldehyde with a skull-free plain label shape pouring into the flask, (3) the virus balls drawn grey with crosses, beside a small vaccine vial.", text=[cap('A vaccine from killed virus')]))
N('L21', "In 1954, the biggest medical trial in history: about one point eight million children, the Polio Pioneers. They lined up at their schools for injections and lollipops.",
  ch('c22b', W(), "A 1954 American school gymnasium: a short line of three stickman children in 1950s clothes waits apart; at the front, a stickman nurse in a white uniform gives an injection with a small syringe held in one hand to the upper arm of a stickman boy, who holds a red lollipop in his hand.", text=cap('1.8 million Polio Pioneers')))
N('L22', "On the twelfth of April 1955, the results were announced: the vaccine was safe and effective. Church bells rang across America. Asked who owned the patent, Salk said: 'Could you patent the sun?'",
  ch('c23a', WL(), "A sunny 1955 American small-town main street: two stickman neighbours in 1950s clothes stand apart on the pavement holding up a newspaper between them with both hands, cheering, while a church bell tower rings in the background.", text=cap('12 April 1955')),
  ch('c23b', C(.5, .5, 1.05), "A 1955 television studio: a stickman scientist with small dark-framed glasses (eyes inside the lenses) and a dark suit sits at a desk in front of a big boxy TV camera and a microphone, smiling modestly, both hands folded on the desk.", text=cap('"Could you patent the sun?"')))
K('L23', "Dead viruses. They beat me with my own dead. That's just bad manners.",
  kg('c24a', C(.5, .45, 1.1), "Mr. Summer stands in front of a 1950s pharmacy window full of small vaccine vials, pressing one hand flat against the glass and staring in horror, his other hand pulling his boater hat down."))
N('L24', "But weeks later, disaster. One company, Cutter, had shipped batches with live virus. Thousands of children got sick, about two hundred were paralysed, and ten died. It changed how vaccines are made and checked forever.",
  ch('c24b', W(), "A 1955 factory laboratory with metal tanks and racks of glass vials: two stickman inspectors in white coats stand apart, one holding up a vial with one hand and looking at it with alarm, the other writing on a clipboard.", text=cap('The Cutter incident, 1955')))

# ---- Sabin and eradication
N('L25', "Then Albert Sabin made a vaccine from a living but weakened virus, given by mouth on a sugar cube. In 1959, the Soviet Union tested it on millions of children. It was cheap, easy, and it spread protection to others.",
  ch('c25a', C(.5, .5, 1.05), "A 1960 school classroom: a stickman nurse in a white coat and white kerchief holds out a sugar cube on a small spoon in one hand to a stickman girl with a big white hair bow in a brown school dress, who opens her mouth to take it.", text=cap('A sugar cube, 1959')),
  dg('d15a', "Two numbered vaccines side by side: (1) a syringe, (2) a sugar cube with a pink drop on it.", text=[cap('Injection or sugar cube')]))
N('L26', "In 1988, he was still paralysing about three hundred and fifty thousand children a year, in a hundred and twenty-five countries. The world launched a campaign to wipe him out. Rotary clubs, health workers and volunteers carried vaccine to every village.",
  ch('c26a', W(), "A modern dusty village road in South Asia: a stickman health worker in a vest and cap carries a blue cool box by its handle in one hand, kneels and holds a small dropper over the open mouth of a small child held in a stickman mother's arms; the mother in a colourful sari.", modern=True, text=cap('Door to door, village to village')),
  dg('d16a', "ONLY a simple world map filling the whole page with most countries shaded red. Nothing else, no pictures, no panels.", text=[cap('1988: 350,000 cases a year')]))
N('L27', "It worked. Cases fell by more than ninety-nine percent. Two of his three types are gone forever.",
  dg('d17a', "ONLY one simple line chart filling the whole page and nothing else: a thick line high on the left falling steeply almost to the bottom on the right, with a small green tick at the end. No numbers.", text=[cap('Down more than 99%')]))
K('L28', "Three of me there used to be. Now there's only one left. I'm feeling rather lonely.",
  kg('c27a', C(.5, .45, 1.1), "Mr. Summer sits alone at a small table in an empty 1950s diner booth, slumped, holding a single melting ice-cream cone in one hand, his other hand propping up his chin, looking glum."))

# ---- WHAT HE LEAVES BEHIND
N('A01', "And for survivors? Decades later, many feel new weakness, pain and exhaustion: post-polio syndrome. The nerves that took over the work are finally wearing out.",
  dg('d18a', "Two numbered panels in one row: (1) a young stickman walking with one crutch, (2) the same stickman as an old man sitting tired in an armchair with the crutch beside him.", people=True, text=[label('What He Leaves Behind', 960, 150, 72), cap('Post-polio syndrome')]))
N('A02', "For the world, he left a lot. Intensive care was born in Copenhagen in 1952, when students took turns squeezing air into paralysed patients by hand. Polio survivors helped launch the disability rights movement. And the idea of vaccinating the whole world.",
  ch('c28a', C(.5, .5, 1.05), "A 1952 Copenhagen hospital room: a stickman medical student in a white coat sits beside a hospital bed, squeezing a black rubber breathing bag rhythmically with both hands, connected by a tube to a stickman patient lying in the bed.", text=cap('Copenhagen, 1952: the first intensive care')),
  dg('d19a', "Three numbered icons in one row: (1) a modern hospital intensive-care bed with a monitor, (2) a wheelchair ramp leading up to a building door, (3) a globe with a small vaccine dropper.", text=[cap('He left more than braces')]))
K('A03', "Intensive care units. Ramps. Vaccines for the whole planet. I really was terribly influential.",
  kg('c29a', C(.5, .45, 1.1), "Mr. Summer stands proudly at the top of a modern concrete wheelchair ramp in front of a hospital entrance, both thumbs tucked into his waistcoat, beaming at the viewer."))

# ---- today
N('T01', "Today, the wild virus survives in just two countries: Pakistan and Afghanistan. A few dozen to about a hundred children a year. And where vaccination slips, he sneaks back, as he did in New York in 2022.",
  dg('d20a', "ONLY a simple map filling the whole page showing Pakistan and Afghanistan shaded red and the surrounding countries pale. Nothing else.", text=[cap('Only two countries left')]),
  ch('c30a', W(), "A modern health clinic in a mountain town in Pakistan: a stickman health worker in a long tunic and a headscarf gives two drops of vaccine from a small dropper held in one hand into the mouth of a small stickman boy, while his stickman father in a long tunic and cap holds the boy.", modern=True, text=cap('Two drops in the mouth')))
N('T02', "Two drops of vaccine. That's all it takes. We are closer than ever to wiping him off the planet, only the second human disease after smallpox.",
  ch('c30b', C(.5, .5, 1.05), "A bright modern clinic: a smiling stickman toddler sits on a stickman mother's lap, the mother in a T-shirt and jeans holding up the child's hand, while a stickman nurse in blue scrubs marks the child's little finger with a purple pen held in one hand.", modern=True, text=cap('Closer than ever')))
K('T03', "Two drops. That's all you need to finish me. So why haven't you yet?",
  kg('c31a', C(.5, .45, 1.1), "Mr. Summer stands at the edge of an empty swimming pool at dusk, looking straight at the viewer with a tense, nervous grin, both hands gripping the brim of his boater hat."))

# ---- ending
N('L29', "Thousands of years. He crippled pharaohs' priests, a President, and millions of children. He was beaten by a dead virus, a sugar cube and two drops. And he isn't quite gone yet.",
  sh('c01c', C(.5, .5, 1.05)), sh('c18b', C(.5, .5, 1.05)), sh('c23a', WL()), sh('c26a', W()),
  kg('c32a', C(.5, .45, 1.1), "Mr. Summer walks away along a deserted 1950s seaside boardwalk at sunset, seen from behind in profile, swinging a closed striped beach umbrella in one hand, his other hand in his pocket, leaving wet footprints."))
N('L30', "Next time: a killer carried by lice. It followed armies for centuries, and it destroyed Napoleon's march on Moscow.",
  ch('c33a', C(.5, .5, 1.04), "A dark snowy winter road in 1812 Russia at dusk, ominous: on the left third of the frame a single exhausted stickman soldier in a tattered dark blue Napoleonic greatcoat and a battered bicorne hat trudges through the snow leaning on his musket held in both hands; the right side of the frame is dark empty snowy mist."))
HOLD(5.0, sh('c33a', O(), text=[label('NEXT TIME', 1380, 360, 110, style='title', pop=True, at=.2, len=4.6), label('SUBSCRIBE', 1380, 500, 64, at=.8, len=4.0)]))

# ---- extra cut-ins for faster cutting (pos None = end)
EXTRA = {
  'L02': [(None, ob('c07b', "A 1950s public swimming pool seen up close at the water's edge on a sunny day, sparkling turquoise water, a red-and-white striped inflatable ball floating.", text=cap('A summer swim')))],
  'L05': [(None, ch('c08b', C(.5, .5, 1.05), "A 1950s hospital examination room: a stickman doctor in a white coat with a head mirror gently tests the reflex of a stickman girl's knee with a small rubber hammer held in one hand, while she sits on the edge of the examination couch.", text=cap('The legs go limp')))],
  'L07': [(None, ch('c10b', C(.5, .5, 1.05), "A crowded 1880s city backyard with washing lines: a stickman toddler in a simple smock plays happily in a puddle with a tin cup, while a stickman grandmother in a shawl sits apart on a stool shelling peas.", text=cap('Mild, and immune for life')))],
  'S03': [(None, ch('c12d', C(.5, .5, 1.05), f"Inside {WARD} at night lit by soft lamps: a stickman nurse in a white uniform holds up a small round hand mirror at an angle above the face of a stickman girl whose head rests on a pillow outside an iron lung, so she can see the room.", text=cap('The only view: a mirror')))],
  'L12': [(None, ch('c15b', C(.5, .5, 1.05), "A crowded 1916 New York railway station platform with a steam train: a stickman father in a straw boater and a suit carries a suitcase in one hand and holds his stickman daughter's hand with the other, hurrying toward the train.", text=cap('Families fled the city')))],
  'L15': [(None, ch('c18c', C(.5, .5, 1.05), "A 1940s radio studio with a big chrome microphone: a stickman comedian in a dark suit and bow tie speaks into the microphone, holding up one silver dime in one hand.", text=cap('Send a dime')))],
  'L17': [(None, ob('c20c', "A single old cream-coloured iron lung machine standing in an empty modern museum hall, round portholes along its side, soft spotlight.", text=cap('About the price of a house')))],
  'L21': [(None, ob('c22c', "A small 1950s badge pinned to a child's sweater, round and blue with a simple picture of a smiling child, next to a wrapped red lollipop on a school desk.", text=cap('Polio Pioneers')))],
  'L25': [(None, ch('c25b', W(), "A 1960s American public school hall: a stickman father in a short-sleeved shirt and his stickman son stand apart in a short queue, the boy holding a small white paper cup with a sugar cube in it in one hand, about to eat it.", text=cap('Sugar Cube Sundays')))],
  'T01': [(None, ch('c30c', C(.5, .5, 1.05), "A modern city sewage plant laboratory: a stickman scientist in a white lab coat, blue gloves and safety glasses (eyes inside the lenses) holds up a small glass sample bottle of murky water to the light with one hand.", modern=True, text=cap('Found in the sewage')))],
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
    json.dump(out, open(os.path.join(ROOT, 'tools/plague/ep10_frames_todo.json'), 'w'), indent=1); print(len(out), 'frames')

def beats():
    out = {'base': 'assets/plague/ep10/frames', 'keep_zoom': [], 'static': True, 'fade_in': .8, 'start': 0.0, 'lead': .45, 'gap': .6, 'max_shot': 3.2,
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
        if i: out['beats'].append({'vo': f'assets/plague/ep10/vo/{i}.wav', **({'gain': 1.05} if r == 'POLIO' else {}), 'shots': sl})
        else: out['beats'].append({'hold': t, 'shots': sl})
    json.dump(out, open(os.path.join(ROOT, 'tools/plague/ep10_beats.json'), 'w'), indent=1); print(len(out['beats']), 'beats')

MUSIC = [(0, 190, 'cholera_a.mp3'), (186, 340, 'plague_b.mp3'), (336, 470, 'cholera_b.mp3'), (466, 'ALL', 'plague_a.mp3')]   # open+who+origin+symptoms | epidemics+FDR+iron lung | Salk+Sabin | eradication+aftermath+today

{'lines': lines, 'frames': frames, 'beats': beats}[sys.argv[1]]()
