"""Episode 11 (The ENTIRE History of Typhus): single source of truth. Same format as ep10_spec.py.

  python3 tools/plague/ep11_spec.py lines   -> voice list (id|ROLE|text), roles NARRATOR / TYPHUS
  python3 tools/plague/ep11_spec.py frames  -> tools/plague/ep11_frames_todo.json
  python3 tools/plague/ep11_spec.py beats   -> tools/plague/ep11_beats.json (for beats.py)
"""
import sys, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
K_SHEET = 'f7448d9f-13fa-4366-b3d0-6cce4dc1d4c8'   # channel/plague/sheets/typhus_a.jpg ('General Louse'), Higgsfield upload
STYLE = ("2D animated history explainer frame, 16:9, no text. Hand-drawn ink illustration, clean black outlines, fine cross-hatching, muted palette of faded military blue, "
         "grimy cream, sepia and snow grey with small feverish red accents and warm firelight. Not gory.")
MODERN = ("2D animated history explainer frame, 16:9, no text. Hand-drawn ink illustration, clean black outlines, the same muted palette, soft natural daylight. "
          "The setting is modern (2000s-2020s): nothing old-fashioned. Not gory.")
SN = ("Humans are simple STICKMEN: plain white round head, two dot eyes, no nose, no beard, thin black stick arms and stick legs, small black mitten hands, "
      "dressed exactly as described for this scene and era; anyone wearing glasses has his two dot eyes INSIDE the lenses and no other eyes. "
      "Only the few figures described, standing apart, never overlapping; each has exactly two arms and two hands; every arm comes straight out of its own shoulder "
      "and never bends around or behind an object; head, body and feet of each figure face the same way, no twisted bodies; "
      "hands are empty unless an object is described; nothing floating; no flags, no banners; no readable text.")
KING = ("Typhus exactly as on the attached sheet, 'General Louse': a gaunt Napoleonic-era officer in a tattered filthy dark-blue 1812 greatcoat with frayed gold epaulettes, "
        "a battered black bicorne hat, a grimy cravat, a pale face flushed with fever, glassy red-rimmed half-closed eyes, a faint red spotty rash on his neck and cheeks, "
        "a thin smug smile; a few tiny cartoon lice march on his epaulettes. Exactly ONE of him, with exactly two arms and two gloved hands; each arm comes from its own shoulder; "
        "no extra hands anywhere in the picture. He holds AT MOST ONE object, his other hand empty and clearly attached to its own arm.")
DIAG = ("Draw ONLY the diagram described below, filling the whole frame, as ONE single picture: no extra rows, no extra panels, no comic strips above or below it. "
        "A hand-drawn explainer diagram in ink and muted watercolour on aged paper, clean and readable like an old textbook plate, "
        "numbered stages as small circled digits with drawn arrows. No words, no letters, no numbers on axes, only circled digits. Not gory. ")
NOPEOPLE = ' No people and no human figures anywhere in the picture.'
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
def HOLD(sec, *s): B.append((None, None, sec, list(s)))
def K(i, t, *s): B.append((i, 'TYPHUS', t, list(s)))

SOLDIER = "a stickman French soldier in a tattered dark-blue 1812 greatcoat, a white cross-belt, a battered shako hat and rags wrapped around his boots"
SNOW = "a frozen snowy Russian road in December 1812 under a grey sky, broken carts and abandoned cannons half-buried in snow"

# ---- cold open: the retreat from Moscow
N('C01', "December 1812. A soldier of the greatest army on Earth can't stop scratching. Under his coat, something is crawling. He has a burning fever, and a red rash spreading across his chest.",
  ch('c01a', C(.5, .5, 1.05), f"Close medium shot on {SNOW}: {SOLDIER} stands hunched in the snow, scratching his chest under his open greatcoat with one hand, his other hand clutching the coat collar, shivering, sweat on his white round head despite the cold.", text=cap('December 1812')),
  ch('c01b', W(), f"Night by a small campfire on {SNOW}: {SOLDIER} sits on an upturned drum, staring into the fire with glassy eyes, wrapped in a grey blanket, while a second stickman soldier in a ragged greatcoat sits apart on a log, holding his hands out to the flames.", text=cap('A burning fever')))
N('C02', "Six months earlier, Napoleon marched into Russia with around six hundred thousand men. Now they are retreating through the snow. Fewer than one in five will make it home.",
  ch('c02a', WL(), "A huge army marching east across a summer plain in June 1812, seen from a hilltop: rows of tiny distant soldiers in blue coats and tall shakos, horses and cannons, dust in the air; in the foreground one stickman officer in a blue coat and bicorne hat sits on a calm brown horse, both hands on the reins, looking proudly ahead.", text=cap('Summer 1812: 600,000 men')),
  ch('c02b', W(), f"{SNOW}: a long thin line of stumbling stickman soldiers in ragged greatcoats trudges through a blizzard toward the horizon; in the foreground two of them help a third, his arms over their shoulders.", text=cap('The retreat from Moscow')))
N('C03', "Everyone blames the Russian winter. But in 2001, builders in Vilnius dug up a mass grave of Napoleon's soldiers. Inside their teeth, scientists found the real killer.",
  ch('c03a', C(.5, .5, 1.05), "A modern construction site in Vilnius with a yellow excavator: two stickman builders in hard hats and orange vests stand apart at the edge of a trench, one pointing down in surprise, the other holding a shovel in both hands; old bones and scraps of blue cloth are visible in the earth.", modern=True, text=cap('Vilnius, 2001')),
  ch('c03b', W(), "A bright modern laboratory: a stickman scientist in a white lab coat, blue gloves and safety glasses (eyes inside the lenses) holds up an old tooth with tweezers under a lamp with one hand, her other hand on the bench beside a microscope.", modern=True, text=cap('The answer was in their teeth')))
K('C04', "The winter gets all the credit. Typical. I did all the work.",
  kg('c04a', C(.5, .45, 1.1), "Medium shot: General Louse stands in a snowstorm at night beside a campfire, warming one gloved hand over the flames, smiling smugly at the viewer; his other hand rests on his hip; tiny lice march along his epaulettes."))
HOLD(4.6, kg('c05a', O(), "Title shot: General Louse stands on the left third of the frame on a snowy battlefield at dusk with broken wagons and a dead tree, saluting the viewer with one gloved hand, his other arm at his side; the right side of the frame is empty grey snowy sky.")
     | {'text': [label('TYPHUS', 1300, 330, 140, style='title', pop=True, at=.15, len=4.2), label('THE GENERAL OF WAR', 1300, 470, 72, style='title', color=[220, 120, 110], at=.5, len=3.9)],
        'sfx': [{'kind': 'boom', 'at': .1, 'gain': .8}]})

# ---- who is he
N('L01', "So who is he? A bacterium, Rickettsia prowazekii. Tiny, and so helpless that it can only live inside other cells. And it needs a partner: the body louse.",
  dg('d02a', "A scale comparison: a single round human cell drawn large (1) with many tiny rod-shaped bacteria living inside it (2), and beside it a body louse drawn large and simple (3)."),
  kg('c06a', C(.5, .45, 1.1), "General Louse sits at a camp table in a dim tent, studying a single tiny louse on his gloved fingertip through a small brass magnifying glass held in his other hand, smiling fondly at it.", text=cap('Rickettsia prowazekii')))
N('L02', "The louse drinks the blood of an infected person and gets infected itself. Then it moves to a new person, and leaves its droppings on the skin. The person scratches the itch, and rubs the bacteria right into the bite.",
  dg('d03a', "Four numbered steps in one row: (1) a louse drinking from a fevered arm, (2) the louse crawling onto a second arm, (3) tiny dark droppings on the skin, (4) a hand scratching the spot with small motion lines.", text=[cap('The itch does the rest')]),
  ch('c07a', W(), "A cramped 1810s army tent at night lit by a lantern: two stickman soldiers in shirts and braces sit apart on straw, both scratching themselves, one under his armpit, the other on his back with a stick held in one hand.", text=cap('Scratch, scratch')))
N('L03', "Lice love crowds, cold and dirt: people who can't wash or change their clothes. Soldiers. Prisoners. Refugees. Sailors. The starving.",
  ch('c08a', C(.5, .5, 1.05), "A dark crowded 18th-century prison cell with straw on the stone floor and a tiny barred window: three stickman prisoners in ragged shirts sit apart against the wall, one scratching his head, one sleeping, one staring at the window.", text=cap('Soldiers, prisoners, refugees')))
K('L04', "Give me a war, a famine, a crowded jail. I'll do the rest.",
  kg('c09a', C(.5, .45, 1.1), "General Louse stands in a dark muddy army camp at night, arms spread wide toward rows of tents behind him like a host welcoming guests, smiling broadly."))

# ---- origin
N('L05', "Where did he come from? Rickettsia bacteria are ancient. They have lived inside insects and ticks for millions of years. But his partner, the body louse, is younger. It only appeared when humans started wearing clothes, perhaps a hundred thousand years ago.",
  dg('d04a', "Two numbered lice in one row: (1) a head louse in hair, (2) a body louse in the seam of a fur garment, with an arrow from (1) to (2).", text=[cap('Clothes made a new home for lice')]),
  ch('c10a', W(), "A prehistoric cave entrance at dusk with a campfire: a stickman early human wearing a rough fur wrap sits by the fire, scratching under the fur with one hand, while a second stickman in a fur wrap stands apart, scraping an animal hide with a stone held in one hand.", text=cap('About 100,000 years ago')))
N('L06', "His name comes from the Greek word typhos: smoke, or haze. Because his victims fall into a foggy daze. And no, he's not typhoid. Different germ, different disease. Same confusing name.",
  dg('d05a', "Two numbered panels in one row: (1) a simple drawing of a stickman head wrapped in swirling grey smoke, eyes dazed, (2) two small glass bottles labelled only with different simple symbols, a louse beside the first and a drop of dirty water beside the second, with a big not-equal sign between them.", text=[cap("Typhus is not typhoid")]))
K('L07', "Typhus. Typhoid. People mix us up all the time. Honestly, it's insulting.",
  kg('c11a', C(.5, .45, 1.1), "General Louse stands in front of an old wall with two portraits hanging on it, pointing at one of them with an annoyed frown with one gloved hand, his other hand on his hip; the portraits show only blank shadowy silhouettes."))

# ---- WHAT HE DOES TO YOU
N('S01', "So what does he do to you? About two weeks after the bite: a sudden high fever, a crushing headache, and pain in every muscle.",
  dg('d06a', "A simple standing stickman outline with three numbered magnifier circles pointing to: (1) the head with lightning pain lines, (2) a thermometer at very high, (3) aching arms and legs with small strain lines.", people=True, text=[label('What He Does to You', 960, 150, 72), cap('Fever, headache, aching muscles')]),
  ch('c12a', C(.5, .5, 1.05), "A cramped 19th-century ship's hold lit by a swinging lantern: a stickman sailor in a striped shirt lies in a hammock holding his head with both hands in pain, while a stickman shipmate in a cap sits apart on a barrel, looking worried.", text=cap('A crushing headache')))
N('S02', "A few days later, a rash appears on the chest and spreads outward, usually everywhere except the face, palms and soles.",
  dg('d07a', "A simple stickman body outline front view with small red dots on the chest and arrows showing the dots spreading outward to the arms and legs; the face, the palms and the soles are left clean with small circled ticks.", people=True, text=[cap('A rash that spreads outward')]))
N('S03', "Then comes the haze. Patients become confused, delirious, staring into nothing. In the old days, up to four in ten died, many from failing hearts or brains.",
  ch('c12b', W(), "A dim 1840s hospital ward lit by one candle: a stickman patient in a white nightshirt sits up in an iron bed, staring blankly into space with a smoky haze around his head, while a stickman nurse in a long grey dress and white cap holds his hand with one hand and a cup with the other.", text=cap('The haze')),
  dg('d08a', "ONLY a single row of ten simple stickman icons across the page: four drawn faded grey, six drawn normal. Nothing else on the page.", people=True, text=[cap('Up to 4 in 10 died')]))
N('S04', "And even if you survive, he can hide in your body for years, and wake up again when you're old. Doctors call it Brill-Zinsser disease.",
  ch('c12c', C(.5, .5, 1.05), "A modern hospital room: an elderly stickman man in a hospital gown sits on the bed, holding his head with one hand, while a stickman doctor in a white coat stands apart reading a chart.", modern=True, text=cap('He can wake up decades later')))
K('S05', "Fever, rash, a lovely fog in the head. And then, when you least expect it, I come back.",
  kg('c13a', C(.5, .45, 1.1), "General Louse leans casually against a misty doorway at night, tipping his bicorne hat with one gloved hand, grey smoke curling around him, his other hand in his coat pocket, smiling."))

# ---- war fever
N('L08', "His first clear appearance in history: Spain, 1489. During the siege of Granada, the Spanish army lost about three thousand men in battle, and around seventeen thousand to a strange new fever.",
  ch('c14a', WL(), "A 1489 Spanish army camp on a dry plain with the walls of a Moorish city on a hill in the distance: a stickman soldier in a steel helmet and a red tunic lies on a straw mat under a canvas awning, sweating, while a stickman friar in a brown robe kneels apart beside him holding a cup of water in one hand.", text=cap('Granada, 1489')),
  dg('d09a', "Two simple numbered stacks of coffin icons side by side: (1) a short stack with a crossed-swords icon above it, (2) a much taller stack with a small louse icon above it.", text=[cap('17,000 to fever, 3,000 to swords')]))
N('L09', "From then on he followed every army. He killed more soldiers than bullets did in war after war. They called him camp fever, war fever, ship fever.",
  ch('c14b', W(), "A 1630s army camp in mud and rain with tents and a smoking fire: two stickman soldiers in floppy hats, breastplates and baggy breeches stand apart, one leaning on a long pike held in one hand, the other wrapped in a cloak, shivering.", text=cap('Camp fever, war fever, ship fever')))
N('L10', "And jail fever. In 1577, at a trial in Oxford, sick prisoners were brought into a packed courtroom. Within weeks, the judge, the sheriff and hundreds of others were dead. It became known as the Black Assize.",
  ch('c15a', C(.5, .5, 1.05), "A crowded 1577 English courtroom with dark wooden panelling: a stickman judge in a red robe and a white wig sits high at the bench, while below him two ragged stickman prisoners stand in chains, scratching, and a stickman sheriff in a black doublet stands apart, holding a staff in one hand.", text=cap('Oxford, 1577: the Black Assize')))
K('L11', "One trial, and I sentenced the judge. Now that's justice.",
  kg('c16a', C(.5, .45, 1.1), "General Louse sits in an empty dark wooden judge's chair in a candlelit courtroom, banging a small wooden gavel held in one gloved hand, grinning, his other hand resting on the bench."))

# ---- Napoleon
N('L12', "Then 1812. Napoleon's soldiers marched in summer heat, packed together, unwashed, wearing the same clothes for weeks. Typhus spread through the ranks before they even reached Moscow.",
  ch('c17a', W(), "A dusty 1812 Polish village road in summer heat: a column of stickman French soldiers in blue coats and shakos marches past, one of them stopping to scratch his back with his musket barrel held in both hands, while another sits apart under a tree, wiping his forehead.", text=cap('Summer 1812')))
N('L13', "On the retreat, it got worse. Soldiers crowded into any shelter, stripped the coats from the dead, and the lice moved with the coats. In Vilnius, thousands died in a few weeks.",
  ch('c17b', C(.5, .5, 1.05), f"A dark burned-out barn on {SNOW} at night: a stickman soldier pulls a ragged blue greatcoat off a heap of abandoned clothes with both hands, while a second stickman soldier sits apart by a tiny fire, wrapped in a blanket and shivering.", text=cap('The lice moved with the coats')),
  dg('d10a', "A simple map of Europe from Paris to Moscow with a thick band going east and a very thin band coming back west, the band shrinking as it goes.", text=[cap('About 600,000 went in, few came back')]))
K('L14', "Napoleon conquered half of Europe. I conquered Napoleon.",
  kg('c18a', C(.5, .45, 1.1), "General Louse stands proudly on a snowy hill at dusk, one gloved hand tucked inside the front of his greatcoat like a famous portrait pose, his other hand behind his back, a burning city glowing on the horizon behind him."))

# ---- famine and ships
N('L15', "In 1847, during Ireland's Great Famine, starving families crowded into workhouses and onto ships to America. So many died on the way that people called them coffin ships.",
  ch('c19a', W(), "The crowded dark hold of an 1847 sailing emigrant ship lit by a lantern: a stickman mother in a shawl holds a small child on her lap with both arms, while a stickman father in a ragged coat sits apart on a wooden bunk, coughing; barrels and ropes around them.", text=cap('Ireland, 1847: the coffin ships')))
N('L16', "On Grosse Île, a quarantine island in Canada, more than five thousand of them are buried. Many of the doctors and nurses who cared for them died too.",
  ch('c19b', C(.5, .5, 1.05), "A windswept island on a wide grey river with rows of simple white wooden crosses on a grassy hill: a stickman nurse in a long dark 1840s dress and white apron stands among the crosses with her head bowed, holding a small bunch of wildflowers in both hands.", text=cap('Grosse Île, Canada')))

# ---- Nicolle and the bath
N('L17', "Then a French doctor in Tunisia, Charles Nicolle, noticed something odd. Typhus patients infected people outside the hospital. But once they had been bathed and given clean clothes at the door, they infected no one.",
  ch('c20a', W(), "The entrance hall of an early 1900s hospital in Tunis with white walls, a tiled floor and arched doorways: a stickman orderly in a white jacket pours a bucket of water into a big tin bathtub with both hands, while a stickman doctor with small round glasses (eyes inside the lenses) and a dark suit stands apart, watching closely, a notebook in one hand.", text=cap('Charles Nicolle, Tunis')))
N('L18', "So it wasn't the patient. It was something on the patient. In 1909 he proved it: the louse. He won the Nobel Prize in 1928.",
  dg('d11a', "Three numbered steps in one row: (1) a pile of dirty clothes with a few lice on it, (2) a bathtub with steam, (3) a clean folded shirt with a green tick.", text=[cap('Wash the clothes, stop the fever')]),
  ch('c20b', C(.5, .5, 1.05), "A 1909 laboratory in Tunis with arched windows: a stickman doctor with small round glasses (eyes inside the lenses) and a white coat holds up a small glass tube containing a single louse to the window light with one hand, smiling, his other hand on the bench beside a monkey cage.", text=cap('1909: the louse')))
N('L19', "Two scientists who studied him, Howard Ricketts and Stanislaus von Prowazek, both died of typhus. The bacterium was named after them.",
  ch('c20c', W(), "A quiet 1910s laboratory at dusk: two empty wooden stools at a bench with microscopes and glass flasks; a stickman colleague in a white coat stands apart by the window with his head bowed, holding a hat in both hands.", text=cap('Ricketts and Prowazek')))
K('L20', "They found my secret. So I took them both. Then they named me after them. Fair trade.",
  kg('c21a', C(.5, .45, 1.1), "General Louse stands in a dim old laboratory, reading a small brass nameplate on a microscope with exaggerated interest, holding a candle in one gloved hand, his other hand on his chin."))

# ---- the great war and Russia
N('L21', "In the First World War, he swept through Serbia in 1915, killing around a hundred and fifty thousand people. After the Russian Revolution, there may have been twenty-five million cases and three million deaths. Lenin said: either socialism defeats the louse, or the louse defeats socialism.",
  ch('c22a', C(.5, .5, 1.05), "A snowy Russian railway station in 1919 with a steam train: stickman soldiers in long grey coats and fur hats sit apart on the platform wrapped in blankets, while a stickman nurse in a white headscarf with a small red cross walks between them carrying a bucket in one hand.", text=cap('Russia, 1919: 25 million cases')),
  dg('d12a', "A simple map of Eastern Europe and Russia with a dark red stain spreading from the west across to the east, and many tiny louse icons along it.", text=[cap('Either socialism defeats the louse...')]))

# ---- Weigl
N('L22', "In Lviv, the biologist Rudolf Weigl made a vaccine from the guts of infected lice. To keep his lice alive, he needed human feeders, people who let lice drink their blood every day.",
  ch('c23a', W(), "A 1930s laboratory in Lviv: a stickman man in a white coat sits at a table with his forearm resting on the table, a small wooden box with a mesh side strapped to his forearm, reading a book held in his other hand; a stickman scientist with glasses (eyes inside the lenses) and a white coat stands apart, checking a clipboard.", text=cap("Rudolf Weigl's lice feeders")),
  dg('d13a', "Three numbered steps in one row: (1) a small wooden matchbox-sized cage strapped to a forearm, (2) a louse being infected with a tiny needle under a microscope, (3) a small vaccine vial.", text=[cap('A vaccine from lice')]))
N('L23', "During the Nazi occupation, Weigl hired scientists, artists and resistance fighters as feeders. The job protected them. And his team secretly smuggled vaccine into the ghettos.",
  ch('c23b', C(.5, .5, 1.05), "A dark 1940s city street at night in the snow: a stickman man in a long dark coat and flat cap hands a small paper-wrapped package to a stickman woman in a headscarf through a gap in a wooden fence, both looking around nervously.", text=cap('Smuggled vaccine')))

# ---- DDT and Naples
N('L24', "In Naples, in the winter of 1943, typhus broke out among a city full of refugees. Teams sprayed more than a million people with the new insecticide DDT. For the first time in history, a typhus epidemic was stopped in winter.",
  ch('c24a', W(), "A 1943 street in Naples with crowds queueing apart: a stickman soldier in a 1940s uniform and helmet sprays white powder from a metal hand pump held in both hands down the collar of a stickman man in a cap, who holds his arms out, laughing.", text=cap('Naples, 1943')),
  dg('d14a', "ONLY one simple line chart filling the whole page: a line rising steeply then falling straight down to nothing, a small snowflake icon above the peak. No numbers.", text=[cap('Stopped in winter')]))
N('L25', "And then antibiotics. Today, a few days of doxycycline cure him.",
  ob('c25a', "A small modern blister pack of pills and a glass of water on a clean white table, soft daylight.", text=cap('A few days of antibiotics')))
K('L26', "Powder and pills. Thousands of years of glorious war, and they beat me with powder and pills.",
  kg('c26a', C(.5, .45, 1.1), "General Louse sits on an upturned ammunition crate in a muddy trench, white powder dusted all over his greatcoat and hat, coughing, waving the powder away with one gloved hand, his other hand on his knee, looking deeply offended."))

# ---- WHAT HE LEAVES BEHIND
N('A01', "For survivors, the fever could leave damaged hearts, lost fingers and toes from poor circulation, and years later, the chance he comes back.",
  dg('d15a', "Three numbered panels in one row: (1) a simple heart with a crack, (2) a foot outline with a bandage on the toes, (3) a sleeping bacterium with a calendar and a question mark.", text=[label('What He Leaves Behind', 960, 150, 72), cap('He can come back')]))
N('A02', "For the world, he left a different kind of mark. He shaped wars, sank armies, and sent millions across the ocean. He gave us delousing stations, quarantine islands, and the habit of washing and changing clothes as public health.",
  ch('c27a', W(), "A 1919 delousing station with white tiled walls and steam: a stickman soldier in a towel stands at a counter handing over a bundle of uniform to a stickman attendant in a white apron, who takes it with both hands, a big steaming oven door open behind him.", text=cap('Delousing stations')),
  dg('d16a', "Three numbered icons in one row: (1) a crossed-out marching army, (2) a ship on waves, (3) a bar of soap with bubbles.", text=[cap('He shaped wars and migrations')]))
K('A03', "Every time you change your shirt, you're thinking of me. Whether you know it or not.",
  kg('c28a', C(.5, .45, 1.1), "General Louse stands in a dim old laundry room among hanging white shirts on lines, holding one clean white shirt up in one gloved hand and inspecting it with distaste, his other hand on his hip."))

# ---- today
N('T01', "Today, he is rare. But he hasn't gone. He still appears where war, poverty and cold come together: in highland villages, refugee camps and prisons. In the United States, he even lives in flying squirrels.",
  dg('d17a', "ONLY a simple world map filling the whole page: a few small red dots in the highlands of East Africa, the Andes and Central Africa. Nothing else.", text=[cap('Still here')]),
  ch('c29a', C(.5, .5, 1.05), "A cold modern refugee camp in mountains with white tents: a stickman aid worker in a fleece jacket and woollen hat hands a folded blanket to a stickman man in a padded jacket, who takes it with both hands; they stand a step apart.", modern=True, text=cap('Refugee camps, prisons, highlands')))
K('T02', "I'm a patient soldier. Give me another war, and I'll be back on duty.",
  kg('c30a', C(.5, .45, 1.1), "General Louse stands at attention in a misty empty field at dawn, saluting the viewer with one gloved hand, his other arm at his side, a tiny louse also saluting on his epaulette."))

# ---- ending
N('L27', "For five centuries, wars were decided not just by generals, but by a tiny insect in a dirty shirt. He was beaten by a bath, a powder and a pill. But he's still waiting, wherever people are cold, crowded and forgotten.",
  sh('c01a', C(.5, .5, 1.05)), sh('d03a', STILL), sh('c20a', W()), sh('c24a', W()),
  kg('c31a', C(.5, .45, 1.1), "General Louse walks away along a misty snowy road at dusk, seen from behind in profile, his ragged greatcoat flapping, his gloved hands clasped behind his back."))
N('L28', "Next time: a fever that turns its victims yellow. It freed a nation, stopped an emperor, and was beaten by doctors who let mosquitoes bite them on purpose.",
  ch('c32a', C(.5, .5, 1.04), "A dark tropical port at night with sailing ships and palm trees, ominous: on the left third of the frame a single stickman sailor in a striped shirt leans weakly against a barrel on the dock, his round head tinted pale yellow; the right side of the frame is dark empty misty sea."))
HOLD(5.0, sh('c32a', O(), text=[label('NEXT TIME', 1380, 360, 110, style='title', pop=True, at=.2, len=4.6), label('SUBSCRIBE', 1380, 500, 64, at=.8, len=4.0)]))

# ---- extra cut-ins
EXTRA = {
  'L02': [(None, ob('c07b', "An extreme close-up of the seam of an old wool army coat with a few tiny lice hiding in the stitches, warm lantern light.", text=cap('Hiding in the seams')))],
  'L03': [(None, ch('c08b', W(), "A crowded 1840s workhouse dormitory with rows of straw mattresses: two stickman men in ragged clothes lie apart on the mattresses under thin blankets, one scratching his arm.", text=cap('No baths, no clean clothes')))],
  'S02': [(None, ch('c12d', C(.5, .5, 1.05), "A 1910s army field hospital tent: a stickman doctor in a white coat holds up a lantern with one hand to look at the bare chest of a stickman soldier sitting on a cot, which is covered in small red spots; the soldier holds his shirt open with both hands.", text=cap('The rash')))],
  'L09': [(None, ch('c14c', C(.5, .5, 1.05), "The crowded dark gun deck of an 18th-century warship lit by a lantern: a stickman sailor in a striped shirt lies in a hammock, sweating, while a stickman ship's surgeon in a long coat stands apart holding a lantern in one hand.", text=cap('Ship fever')))],
  'L13': [(None, ch('c17c', W(), "A snowy 1812 Vilnius street at night with old stone houses: stickman soldiers in ragged greatcoats crowd apart into the doorway of a church to escape the cold, one carrying a lantern in one hand.", text=cap('Vilnius, December 1812')))],
  'L17': [(None, ob('c20d', "A big tin bathtub full of steaming water, a bar of soap and a neatly folded clean white shirt on a wooden stool beside it, in a white-tiled room.", text=cap('Bath and clean clothes')))],
  'L21': [(None, ch('c22b', W(), "A 1915 Serbian mountain village in winter: a stickman doctor in a long coat and a cap with a small red cross armband kneels beside a stickman patient lying on straw outside a small stone house, holding his wrist with one hand.", text=cap('Serbia, 1915')))],
  'L24': [(None, ob('c24b', "A dented 1940s metal hand pump duster and a paper bag of white DDT powder on a cobbled Naples street, white powder spilled on the stones.", text=cap('DDT')))],
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
    json.dump(out, open(os.path.join(ROOT, 'tools/plague/ep11_frames_todo.json'), 'w'), indent=1); print(len(out), 'frames')

def beats():
    out = {'base': 'assets/plague/ep11/frames', 'keep_zoom': [], 'static': True, 'fade_in': .8, 'start': 0.0, 'lead': .45, 'gap': .6, 'max_shot': 3.2,
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
        if i: out['beats'].append({'vo': f'assets/plague/ep11/vo/{i}.wav', **({'gain': 1.05} if r == 'TYPHUS' else {}), 'shots': sl})
        else: out['beats'].append({'hold': t, 'shots': sl})
    json.dump(out, open(os.path.join(ROOT, 'tools/plague/ep11_beats.json'), 'w'), indent=1); print(len(out['beats']), 'beats')

MUSIC = [(0, 172, 'plague_a.mp3'), (168, 268, 'plague_b.mp3'), (264, 352, 'cholera_a.mp3'), (348, 'ALL', 'cholera_b.mp3')]   # open+who+origin+symptoms | wars+Napoleon+famine | Nicolle+WWI+Weigl | DDT+aftermath+today

{'lines': lines, 'frames': frames, 'beats': beats}[sys.argv[1]]()
