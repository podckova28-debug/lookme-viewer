"""Episode 6 (The ENTIRE History of Rabies): single source of truth. Same format as ep05_spec.py.
Fast cutting from the start (~125 shots), ~30 explainer diagrams, mild camera only. Origin = lyssaviruses in bats; symptoms shown on characters.

  python3 tools/plague/ep06_spec.py lines   -> voice list (id|ROLE|text), roles NARRATOR / RABIES
  python3 tools/plague/ep06_spec.py frames  -> tools/plague/ep06_frames_todo.json
  python3 tools/plague/ep06_spec.py beats   -> tools/plague/ep06_beats.json (for beats.py)
"""
import sys, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
K_SHEET = '613e7f6d-97c4-481b-b6cc-dbeee60a59a4'   # channel/plague/sheets/cand_rabies.jpg
S_SHEET = '84427fc9-09ce-40e6-b032-6f2700874458'   # channel/plague/sheets/stickmen_common.jpg
STYLE = ("2D animated history explainer frame, 16:9, no text. Hand-drawn ink illustration, clean black outlines, muted night-blue, slate-grey and sepia palette "
         "with warm gaslight amber and small sickly-yellow accents. Not gory.")
STICK = ("Humans are simple STICKMEN in the style of the attached stickman sheet: plain white round head, two dot eyes, no nose, no beard, thin black stick arms and legs, "
         "dressed exactly as described for this scene and its era; anyone wearing glasses has his two dot eyes INSIDE the lenses and no other eyes. KEEP IT SIMPLE: only the few figures described, "
         "standing apart, never overlapping; each figure has exactly two arms and two hands, clearly attached to its own sleeves; nothing floating. No crowds, no ghost figures, no plague doctors.")
KING = ("Rabies exactly as on the attached sheet: a tall, wiry, predatory gentleman with the head of a lean grey wolf-dog, wild bristling fur, bloodshot yellow eyes and a little white froth at the corners "
        "of his toothy grin; a torn black Victorian tailcoat and waistcoat, a loose cravat, a broken leather dog collar with a short dangling chain around his neck. "
        "Exactly ONE of him, with exactly two arms and two hands with normal-length clawed fingers.")
DIAG = ("Draw ONLY the diagram described below, filling the whole frame: no extra rows, no extra panels, no comic strips above or below it. A hand-drawn explainer diagram in ink and muted watercolour on aged paper, "
        "clean and readable like an old textbook plate, simple stickman figures (plain white round head, dot eyes, stick limbs, each with exactly two arms) where people appear, "
        "numbered stages as small circled digits with drawn arrows. No words, no letters, no numbers on axes, only circled digits. Not gory. ")

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
def dg(img, p, people=True, **k): return sh(img, STILL, (STICK + ' ' if people else '') + DIAG + p, 'S' if people else '', **k)
def sc(img, p, cam=None, **k): return sh(img, cam or W(), p, **k)   # scenery, no refs
NS = {}
def cn(img, cam, p, modern=False, **k):   # stickmen WITHOUT the sheet (ancient / medieval / modern scenes); the full prompt is built into FIX below
    NS[img] = (modern, p); return sh(img, cam, p, 'N', **k)

B = []
def N(i, t, *s): B.append((i, 'NARRATOR', t, list(s)))
def K(i, t, *s): B.append((i, 'RABIES', t, list(s)))
def HOLD(sec, *s): B.append((None, None, sec, list(s)))

# ---- cold open: the bitten boy and his mother, then Paris, July 1885
N('C01', "A mother clutches her nine-year-old son, Joseph Meister, bleeding from fourteen bites of a mad dog. Two days later, on the sixth of July, 1885, she brings him to Louis Pasteur's laboratory in Paris.",
  ch('c01c', C(.5, .5, 1.05), "A village lane in Alsace in July 1885: a desperate stickman mother in a long dark Alsatian dress and a bonnet kneels on the ground and hugs her small stickman son, who wears a cap, a short jacket and short trousers, his arm and leg wrapped in white bandages; an overturned basket of bread lies beside them and a dog runs away far down the lane. Only these two figures. Not gory, no blood.", text=cap('Fourteen bites from a mad dog')),
  ch('c01a', WL(), "A Paris street in summer 1885 with Haussmann buildings, gas lamps and a horse cab: a stickman mother in a long dark Alsatian dress and a bonnet hurries along the pavement, leading her small stickman son in a cap, with a bandaged arm, by the hand toward the door of a stone laboratory building. Only these two figures.", text=cap('Paris — 6 July 1885')),
  ch('c01b', W(), "A 1880s laboratory doorway: a stickman mother in a long dark Alsatian dress and a bonnet stands holding the hand of a small stickman boy with a bandaged arm and leg, a cap on his head; both look scared.", text=cap('Joseph Meister, nine years old')))
N('C02', "She knew what came next. Once the symptoms began, nobody survived. Not ever.",
  ch('c02a', C(.5, .5, 1.05), "A dim 1885 bedroom lit by a single candle, rain on the window: a stickman mother in a long dark Alsatian dress and a bonnet sits on a chair beside a small bed and holds the hand of her small stickman son, who lies under the blanket with a bandaged arm; both look frightened; a wooden toy horse on the floor. Only these two figures."),
  dg('d01a', "A simple hourglass with sand running out, next to a small cross; beside it a long empty row of small circles where not one is ticked.", people=False, text=[cap('Once symptoms begin, almost no one survives')]))
N('C03', "Pasteur was not even a medical doctor. He had an experimental treatment that had only ever been tried on dogs. And he had to decide that night.",
  ch('c03a', W(), "A cluttered 1885 laboratory at night lit by an oil lamp: a stickman chemist with a short grey beard drawn as a simple line and a black skullcap stands thinking at a bench of glass jars and flasks, one hand on his chin.", text=cap('Louis Pasteur — a chemist, not a doctor')),
  ch('c03b', W(), "An 1880s laboratory kennel: two stickman lab assistants in long aprons stand apart beside a row of iron cages with calm dogs in them, one assistant holding a clipboard.", text=cap('Only ever tried on dogs')),
  ch('c03c', C(.5, .5, 1.05), "A dim 1885 laboratory corridor at midnight beside a tall grandfather clock: a single stickman chemist with a short grey beard drawn as a simple line, a black skullcap and a black frock coat paces past the clock with both hands clasped behind his back; a lit oil lamp on a side table.", text=cap('One night to decide')))
K('C04', "Fourteen bites. A child. And a chemist with a syringe. I liked my chances.",
  kg('c04a', C(.5, .45, 1.1), "Medium shot: Rabies leans in a dark Paris doorway at night under a gas lamp, grinning wolfishly at the viewer, one hand twirling the broken chain on his collar, the other in his pocket."))
HOLD(4.6, kg('c05a', O(), "Title shot: Rabies stands on the left third of the frame on a foggy cobbled street at night under a full moon, his long shadow stretching behind him; dark empty fog on the right side.")
     | {'text': [label('RABIES', 1300, 330, 150, style='title', pop=True, at=.15, len=4.2), label('4,000 YEARS OF MADNESS', 1300, 470, 68, style='title', color=[235, 210, 110], at=.5, len=3.9)],
        'sfx': [{'kind': 'boom', 'at': .1, 'gain': .8}]})

# ---- who is he
N('L01', "So who is he? Rabies is a virus. Under a powerful microscope, he looks like a tiny bullet. His family is called Lyssavirus, after Lyssa, the Greek spirit of rage and madness.",
  dg('d02a', "A large magnified bullet-shaped virus particle covered in tiny spikes, with a coiled strand inside; beside it, for scale, a round red blood cell drawn much larger, marked with circled digits 1 and 2.", people=False, text=[cap('The rabies virus')]),
  sc('c06a', "An ancient Greek vase painting on a black amphora showing a wild-haired winged spirit with snakes in her hair, in orange and black, displayed on a museum stand under a lamp. No people.", C(.5, .5, 1.05), text=cap('Lyssa, the Greek spirit of rage')))
N('L02', "He lives in the saliva of an infected animal. A bite pushes him into the wound. Dogs cause almost every human case in the world. But foxes, raccoons, jackals, monkeys and bats can carry him too.",
  dg('d03a', "A ring of five animals around a central small virus symbol: (1) a dog, (2) a fox, (3) a raccoon, (4) a jackal, (5) a bat; a thicker arrow leads from the dog to a stickman, thinner dotted arrows from the others.", text=[cap('Dogs cause almost every human case')]),
  ch('c06b', C(.5, .5, 1.05), "A dark 1880s back alley at night under a gas lamp: a thin stray dog with bristling fur and a little drool at its mouth snarls, and a single stickman man in a flat cap, a waistcoat and rolled shirtsleeves backs away from it with both empty hands raised. Not gory.", text=cap('It lives in the saliva')))
N('L03', "Then, he travels. Not through the blood, but along the nerves, slowly crawling toward the brain. That can take weeks, months, or sometimes more than a year. And all that time, you feel fine.",
  dg('d04a', "A standing stickman with a small bite mark on his ankle; a glowing dotted line runs from the ankle up through his stick leg and spine to his round head, with three small circled digits along the path and a small calendar icon beside it.", text=[cap('Crawling along the nerves to the brain')]),
  ch('c07a', W(), "A sunny 1880s village square: a single cheerful stickman with a small bandage on his ankle walks along carrying a loaf of bread, whistling.", text=cap('And all that time, you feel fine')))
N('L04', "When he finally reaches the brain, it's too late. He multiplies there, and spreads back out to the salivary glands, ready for the next bite.",
  dg('d05a', "A cartoon side view of a simple stickman head: (1) inside it a round brain full of many tiny bullet-shaped viruses, (2) arrows from the brain down to the mouth and jaw, where more tiny viruses gather in the saliva.", people=False, text=[cap('From the brain to the saliva')]))
K('L05', "I take the scenic route. Through your nerves. No hurry.",
  kg('c08a', C(.5, .45, 1.1), "Rabies strolls slowly along a long empty country road at dusk, hands behind his back, tail-like coat flapping, looking relaxed and smug."))

# ---- origin
N('L06', "But where did he come from? His closest relatives are viruses that live in bats. Most scientists think rabies began in bats, long ago, and then jumped into meat-eating animals like dogs and foxes.",
  cn('c09a', WL(), "A huge dark cave entrance in a forest at dusk with a cloud of bats streaming out into a purple sky: a single stickman bat scientist in a modern field jacket, cargo trousers and a head torch stands at the cave mouth looking up at the bats, holding one small notebook.", modern=True, text=cap('Scientists think it began in bats')),
  dg('d06a', "A family-tree diagram drawn on aged paper: at the root (1) a bat, branching out to (2) a fox, (3) a dog and (4) a raccoon, each with a small virus symbol; arrows show the jump from the bat to the meat-eaters.", people=False, text=[cap('Then it jumped to dogs and foxes')]))
N('L07', "Once he got into dogs, he had the perfect home. Dogs live right next to people. They have for at least fifteen thousand years.",
  cn('c09b', W(), "A prehistoric campfire at night outside a hide tent under the stars: two stickmen in simple Stone Age animal-hide tunics sit apart by the fire; one holds out a bone in one hand to a wolf-like dog lying beside him, the other warms both empty hands at the flames.", text=cap('At least 15,000 years together')),
  dg('d07a', "A timeline on aged paper: (1) a wild wolf, (2) a tamer wolf-dog by a campfire, (3) a farm dog by a hut, (4) a pet dog on a cushion; a small virus symbol hops along from the second stage onward.", people=False, text=[cap('From wild wolf to family dog')]))
K('L08', "Man's best friend. And mine.",
  kg('c10a', C(.5, .45, 1.1), "Rabies crouches beside a stray dog in a dark alley and pats its head with one hand, grinning at the viewer; the dog looks up at him."))

# ---- WHAT HE DOES TO YOU
N('S01', "So what does he do to you? It starts like flu. Fever, a headache, tiredness. And a strange tingling or itching at the place you were bitten, sometimes months after the bite had healed.",
  dg('d08a', "Two numbered panels: (1) a stickman in bed with a thermometer and wavy heat lines, (2) the same stickman scratching his ankle where small tingling zigzag lines appear around an old healed bite mark.", text=[label('WHAT HE DOES TO YOU', 960, 150, 72), cap('It starts like flu')]),
  ch('c11a', W(), "A 19th-century cottage: a single stickman sits on a stool by the fire, rubbing his ankle with a puzzled look, a blanket around his shoulders.", text=cap('A tingling at the old bite')))
N('S02', "Then he takes over the brain. Most victims become restless, confused and terrified. They hallucinate, lash out, and can't sleep.",
  dg('d09a', "A stickman's round head with the brain drawn inside it, tangled with dark scribbles and small lightning bolts; around the head, small drawings of floating eyes, shadows and twisting shapes.", text=[cap('Confusion and terror')]),
  ch('c11b', W(), "A dim 19th-century bedroom at night: a single frightened stickman sits up in bed, clutching the blanket, staring at a frightening shadow on the wall shaped like a wolf."))
N('S03', "And then the strangest symptom of all. The victim is desperately thirsty, but the moment they try to drink, their throat clamps shut in a painful spasm. Soon even the sight of water sets it off. The old name for rabies was hydrophobia: fear of water.",
  dg('d10a', "Three numbered panels: (1) a thirsty stickman reaching for a glass of water, (2) the stickman's throat drawn with jagged spasm lines as he tries to drink, (3) the stickman turning away in fear from a jug of water.", text=[cap('Hydrophobia — fear of water')]),
  ch('c11c', W(), "A 19th-century sickroom: a stickman nurse in a white apron offers a cup of water to a stickman patient sitting in bed, who flinches back in fear, holding up one hand."))
N('S04', "Because they can't swallow, saliva builds up in the mouth. That's the frothing that people remember. And it's full of the virus.",
  dg('d11a', "A simple cartoon side view of a stickman's mouth and throat as a tube: (1) the throat tube is pinched shut with spasm lines, (2) small bubbles of saliva collect in the mouth, full of tiny bullet-shaped viruses.", people=False, text=[cap('Saliva full of the virus')]))
N('S05', "Some people have the quieter form. A slow paralysis creeps up from the bitten limb. Either way, it ends in a coma, and death, usually within a week or two.",
  dg('d12a', "A stickman lying on a bed, with grey shading rising from his feet up his stick legs to his chest, marked with circled digits 1, 2 and 3 for the stages of paralysis.", text=[cap('The quieter form: slow paralysis')]),
  ch('c11d', C(.5, .5, 1.05), "A 19th-century hospital ward in grey morning light: a stickman patient lies still in bed under a blanket with his eyes closed, and a stickman doctor in a black frock coat stands apart beside the bed with his head bowed, holding his top hat in one hand; an untouched cup of water on a stool. Somber, not gory.", text=cap('Death within a week or two')))
K('S06', "Angry hosts bite. Biting spreads me. I am a very good designer.",
  kg('c12a', C(.5, .45, 1.1), "Rabies stands in a dark study in front of a blackboard covered with simple chalk drawings of a dog, a bite, a brain and arrows, holding a piece of chalk in one hand, the other hand behind his back, looking proud."))

# ---- ancient history
N('L09', "He is one of the oldest diseases we know. Around four thousand years ago, the Laws of Eshnunna in Mesopotamia said: if a mad dog bites a man and he dies, the owner must pay two-thirds of a mina of silver.",
  sc('c13a', "A clay tablet covered in rows of wedge-shaped cuneiform marks displayed on a museum stand under a warm lamp. No people.", C(.5, .5, 1.05), text=cap('The Laws of Eshnunna — about 1800 BC')),
  dg('d13a', "Three numbered panels: (1) a snarling dog on a rope leash held by a stickman owner, (2) the dog biting a second stickman's leg, (3) the owner handing over a small pile of silver pieces on a balance scale.", text=[cap('Two-thirds of a mina of silver')]))
N('L10', "The Greeks and Romans knew him well. The Roman writer Celsus advised burning the wound with a hot iron. Others prescribed the liver of the mad dog, or throwing the patient into a pond.",
  ch('c14a', W(), "An ancient Roman doctor's room with a marble table and oil lamps: a stickman Roman physician in a white toga heats a small iron rod over a brazier, a stickman patient with a bandaged leg sits apart on a stool, looking nervous.", text=cap('Celsus: burn the wound')),
  dg('d14a', "Three numbered Roman remedies on aged paper: (1) a hot iron rod over a brazier, (2) a small bowl with a dark lump of liver, (3) a stickman being dunked into a pond by two other stickmen.", text=[cap("A hot iron, or the mad dog's liver")]))
N('L11', "That's where a famous phrase comes from. For a dog bite, people put a hair of the very dog that bit you into the wound. Today, hair of the dog means a drink to cure a hangover.",
  dg('d15a', "Two numbered panels: (1) a stickman with a bitten arm places a single dog hair on the wound while a scruffy dog looks on, (2) the same stickman years later at a tavern table holding a mug, looking hungover.", text=[cap('"The hair of the dog that bit you"')]))
K('L12', "A hot poker, a dog's liver, and a pond. My favourite century.",
  kg('c15a', C(.5, .45, 1.1), "Rabies sits in a Roman marble bath house beside a pool, leaning back with his arms spread along the edge, grinning, a laurel wreath tilted on his wolf head."))

# ---- Middle Ages to 1800s
N('L13', "In the Middle Ages, people prayed to Saint Hubert, the patron saint of hunters. At his shrines, priests burned bite wounds with a red-hot iron key, called a Saint Hubert's key.",
  cn('c16a', WR(), "A small medieval stone chapel in a forest with a statue of a hunter saint with a stag above the door, candles burning: a single stickman medieval peasant in a plain brown wool tunic, hood and leggings, with one arm in a white bandage, kneels and prays at the chapel door.", text=cap('Saint Hubert, patron saint of hunters')),
  dg('d16a', "Three numbered steps: (1) an ornate old iron key with a cross-shaped end, (2) the same key glowing orange in a small brazier of coals, (3) the key resting on a stone chapel altar beside a candle and a small carved stag.", people=False, text=[cap("Saint Hubert's key")]))
N('L14', "Some historians think rabies helped inspire the legends of werewolves and vampires. Biting, rage, sleeplessness, fear of water and mirrors, wandering at night. It all sounds a little familiar.",
  cn('c16b', WL(), "A medieval village at night under a full moon, thatched houses and a dark forest edge: a single frightened stickman villager in a plain wool tunic and hood stands in his doorway holding up one lantern, staring at a wolf howling on a distant hill."),
  dg('d17a', "Side-by-side comparison: (1) a simple cartoon werewolf silhouette howling at the moon, (2) a simple cartoon vampire silhouette with a cape avoiding a mirror; between them a small virus symbol with arrows pointing to both.", people=False, text=[cap('Werewolves and vampires?')]))
K('L15', "Werewolves, vampires. People always make me sound more glamorous than I am.",
  kg('c17a', C(.5, .45, 1.1), "Rabies stands on a moonlit hilltop with a full moon behind him, adjusting his cravat with both hands, posing like a gentleman for a portrait."))
N('L16', "By the 1800s, cities were full of stray dogs, and rabies panics swept Europe and America. Mad dog scares filled the newspapers. Police shot strays in the street.",
  ch('c18a', WR(), "A busy 1880s city street with gas lamps and a horse cart: a stickman mother in a long Victorian dress and a bonnet pulls her small stickman son in a cap and short trousers away by the hand from three snarling stray dogs at the kerb. Only these two figures.", text=cap('Panic across Europe and America')),
  ch('c18b', W(), "An 1880s city street corner: a stickman policeman in a dark helmet and coat stands holding a long rope noose-pole, a stickman newspaper boy with a cap holds up a blank newspaper, both apart.", text=cap('Police hunted strays in the street')))
N('L17', "Britain fought back with muzzles and quarantine. Every dog had to wear a muzzle, and imported pets were locked up for six months. By 1902, rabies was gone from Britain.",
  dg('d18a', "Three numbered panels: (1) a dog wearing a leather muzzle, (2) a dog in a quarantine kennel with a calendar showing six months, (3) a map outline of Britain with a big green tick.", people=False, text=[cap('Gone from Britain by 1902')]),
  ch('c18c', W(), "A Victorian London park: a single stickman gentleman in a top hat walks a small dog wearing a leather muzzle on a leash."))

# ---- Pasteur
N('L18', "But nobody had a cure. Then came Louis Pasteur. He had already shown that germs cause disease, and made a vaccine for anthrax in sheep. Now he turned to rabies.",
  ch('c19a', W(), "An 1880s laboratory: a stickman chemist with a short grey beard drawn as a simple line and a black skullcap looks through a brass microscope on a bench of flasks.", text=cap('Louis Pasteur')),
  dg('d19a', "Three numbered icons on aged paper: (1) a glass flask with a swan-shaped neck, (2) a sheep with a small syringe and a green tick, (3) a dog with a question mark.", people=False, text=[cap('Next target: rabies')]))
N('L19', "He couldn't see the rabies virus. It was far too small for his microscopes. So he grew it in the spinal cords of rabbits, and dried the cords in glass flasks. The longer they dried, the weaker the virus became.",
  dg('d20a', "A row of five glass flasks, each holding a thin pale strip of dried tissue hanging inside, numbered with circled digits 1 to 5; beside each flask a small virus symbol that gets smaller and fainter from flask 1 to flask 5.", people=False, text=[cap('The longer it dries, the weaker he gets')]),
  ch('c19b', C(.5, .5, 1.05), "An 1885 laboratory lit by a lamp: a single stickman lab assistant in a long apron places one tall glass flask with a cotton stopper on a shelf of identical flasks, each holding a thin pale dried strip; a rabbit hutch with white rabbits below.", text=cap('Grown in rabbits, dried in flasks')))
N('L20', "His plan: start with the weakest virus, then give stronger and stronger doses, to train the body to fight before the real virus reached the brain.",
  dg('d21a', "A staircase diagram: a stickman climbs five numbered steps; on each step a syringe with a slightly bigger virus symbol, and on the top step the stickman holds a small round shield while a large virus bounces off it.", text=[cap('Weak first, then stronger and stronger')]))
K('L21', "Dried rabbit spine. That's what he planned to stab me with.",
  kg('c20a', C(.5, .45, 1.1), "Rabies peers suspiciously at a tall glass flask on a laboratory bench, holding it up to the lamp with one hand, his other hand covering his nose, ears flattened."))

# ---- Joseph Meister
N('L22', "On the evening of the sixth of July, Joseph got his first injection. Over ten days, he got thirteen. Each one stronger than the last.",
  ch('c21a', W(), "An 1885 doctor's room lit by a lamp: a stickman doctor in a black frock coat holds a small syringe beside a small stickman boy with a cap sitting on a chair, a stickman mother standing apart behind him.", text=cap('The evening of 6 July 1885')),
  dg('d22a', "A calendar on aged paper with ten days in a row, thirteen small syringe icons spread across them, each syringe a little darker than the one before.", people=False, text=[cap('13 injections in 10 days')]))
N('L23', "Then they waited. Days, then weeks. Joseph never got sick. He went home to Alsace a healthy boy. Years later, he came back to work as the caretaker at the Pasteur Institute.",
  ch('c21b', WL(), "A sunny Alsace village lane in summer with half-timbered houses, flower boxes and a church tower: a healthy small stickman boy in a cap and short trousers runs ahead happily, and his stickman mother in a long dark Alsatian dress and a bonnet follows a few steps behind, smiling. Only these two figures.", text=cap('Home to Alsace, healthy')),
  ch('c21c', W(), "A courtyard of a grand 1890s institute building in Paris: a grown-up stickman caretaker in a blue work coat and cap sweeps the steps with a broom, smiling.", text=cap('Later, caretaker of the Pasteur Institute')))
N('L24', "Months later, a fifteen-year-old shepherd named Jean-Baptiste Jupille was badly bitten while fighting off a rabid dog to protect younger children. Pasteur treated him too, and he lived.",
  ch('c22a', W(), "A green hillside in the French Jura in 1885: a teenage stickman shepherd with a crook stands in front of three small stickman children, facing a snarling dog, all standing apart.", text=cap('Jean-Baptiste Jupille, age 15')),
  sc('c22b', "A bronze statue of a boy wrestling a dog on a stone plinth in a garden courtyard, leaves around it. No people.", C(.5, .5, 1.05)))
N('L25', "Soon people came from all over the world. In 1886, nineteen Russians bitten by a rabid wolf travelled all the way to Paris. Most of them survived. Donations poured in, and in 1888 the Pasteur Institute opened.",
  dg('d23a', "A map of Europe on aged paper with a dotted route from western Russia to Paris, a small wolf icon at the start, a small train icon on the route, and a building icon at Paris.", people=False, text=[cap('From Smolensk to Paris — 1886')]),
  ch('c23a', WR(), "A grand red-brick and stone institute building in Paris in 1888 with a wrought-iron gate and trees around: at the open gate, a stickman chemist with a short grey beard drawn as a simple line, a black skullcap and a black frock coat welcomes a stickman mother in a shawl and a long dress who holds the hand of her small stickman child. Only these three figures.", text=cap('The Pasteur Institute — 1888')))
K('L26', "One little boy. And suddenly, I'm the villain everyone has a cure for.",
  kg('c24a', C(.5, .45, 1.1), "Rabies stands outside the iron gate of a grand institute at night, gripping the bars with both hands, glaring in, ears flat."))

# ---- the 20th century
N('L27', "The vaccine got better, and safer. And the real breakthrough was vaccinating dogs. Where dogs are vaccinated, human rabies almost disappears.",
  ch('c25a', W(), "A modern village vet clinic under a tree: a stickman vet in a white coat gives a small injection to a calm dog held by a stickman girl, both standing apart."),
  dg('d24a', "Two side-by-side numbered panels: (1) a town of small houses with many dogs and many small red virus symbols, (2) the same town with every dog wearing a small blue collar tag and no virus symbols at all.", people=False, text=[cap('Vaccinate the dogs, save the people')]))
N('L28', "Today, if you're bitten, the treatment works almost every time, as long as you get it before symptoms start. Wash the wound for fifteen minutes with soap and water, then get the vaccine, and an antibody injection.",
  dg('d25a', "Three numbered steps on aged paper: (1) a stickman washing a bitten hand under a running tap with soap and a small clock showing fifteen minutes, (2) a syringe of vaccine, (3) a second syringe with small Y-shaped antibody symbols.", text=[cap('Wash the wound for fifteen minutes')]),
  ch('c25b', W(), "A modern clinic: a stickman nurse in blue scrubs washes the bitten hand of a stickman patient at a sink, a bar of soap beside them.", text=cap('Treat it before symptoms start')))
N('L29', "And then, in 2004, something nobody had seen before. A fifteen-year-old girl in Wisconsin, Jeanna Giese, was bitten by a bat and developed rabies. Doctors put her in a coma to protect her brain. She survived.",
  cn('c26a', WL(), "Outside a small brick church in Wisconsin in autumn at dusk: a teenage stickman girl with a ponytail in a 2000s hoodie and jeans holds out one hand toward a small bat fluttering just above her fingers.", modern=True, text=cap('Wisconsin — 2004')),
  ch('c26b', W(), "A modern hospital room: a teenage stickman girl with a ponytail lies in a hospital bed with monitors beside her, a stickman doctor in a white coat stands apart checking a screen.", text=cap('Jeanna Giese, age 15')))
N('L30', "It was a miracle, but a rare one. The same approach has failed in most other patients. Once he reaches the brain, he still almost always wins.",
  dg('d26a', "A row of many small simple stickman icons on aged paper, almost all grey with a tiny cross, and only one or two bright ones with a small star.", text=[cap('A handful of survivors')]))
K('L31', "One girl beat me. One. I still have nightmares about that hospital.",
  kg('c27a', C(.5, .45, 1.1), "Rabies sits hunched on the edge of an empty modern hospital bed at night, holding his head in both hands, ears drooping."))

# ---- WHAT HE LEAVES BEHIND
N('A01', "And for those who survive? Survivors are so rare that each one is studied by doctors around the world. Most are left with serious brain damage. A lucky few recover almost completely.",
  dg('d27a', "Three numbered panels: (1) a stickman in a hospital bed with a heart monitor, (2) the stickman in a wheelchair with a stickman therapist beside him, (3) the stickman walking with a small cane, smiling.", text=[label('WHAT HE LEAVES BEHIND', 960, 150, 72), cap('Most survivors have brain damage')]))
N('A02', "For the world, he left behind the first vaccine ever made in a laboratory for people, a network of Pasteur Institutes on five continents, and dog vaccination laws in country after country.",
  dg('d28a', "Three numbered icons on aged paper: (1) a glass vial with a small syringe, (2) a world map with small institute building icons on five continents, (3) a dog wearing a collar with a round vaccination tag.", people=False, text=[cap('Pasteur Institutes on five continents')]),
  sc('c28a', "A modern rabies vaccine vial and a syringe on a clean steel tray in a bright laboratory, a small dog tag beside it. No people.", C(.5, .5, 1.05), text=cap('The first lab-made vaccine for people')))
K('A03', "He took a disease that couldn't be cured, and made it something you can prevent with two injections. Rude.",
  kg('c28b', C(.5, .45, 1.1), "Rabies sits in a modern veterinary waiting room, alone, wearing a plastic cone collar around his neck, arms folded, sulking."))

# ---- today
N('L32', "So is he gone? Far from it. Rabies still kills around fifty-nine thousand people every year, mostly in Asia and Africa. About four in ten of them are children.",
  dg('d29a', "A world map on aged paper with Asia and Africa shaded dark red, the Americas and Europe much lighter, and small stickman child icons over the dark regions.", people=False, text=[cap('About 59,000 deaths a year')]),
  ch('c29a', W(), "A dusty village road in rural South Asia at evening: a small stickman boy in a school uniform walks home with a school bag, a stray dog lying by the roadside ahead of him.", text=cap('Four in ten are children')))
N('L33', "Almost all of those deaths could be prevented. The world has set a goal: zero human deaths from dog rabies by 2030.",
  dg('d30a', "A simple downward line chart on aged paper falling toward zero, with a small dog icon with a vaccination tag at the end of the line and a small target symbol.", people=False, text=[cap('Zero deaths by 2030')]),
  ch('c29b', W(), "A sunny modern village square: a stickman health worker in a vest gives a dog a vaccine while a stickman child holds the dog's lead, a small table with a cool box behind them."))
N('L34', "In the Americas, dog rabies is almost gone. There, most human cases now come from bats. Their bites are so small, people sometimes don't even notice them.",
  cn('c30a', C(.5, .5, 1.05), "A modern North American attic bedroom at night with wooden beams and moonlight through a small window: a single stickman in modern pyjamas sleeps peacefully in bed, while a small bat hangs from the beam right above him.", modern=True, text=cap('In the Americas, mostly bats')),
  dg('d31a', "A close-up comparison on aged paper: (1) a large dog bite drawn as two rows of marks, (2) a bat bite drawn as two tiny dots next to a coin for scale.", people=False, text=[cap('A bat bite: two tiny dots')]))
K('L35', "I've made some new friends. They fly.",
  kg('c31a', C(.5, .45, 1.1), "Rabies stands in a moonlit bell tower with a small bat perched on his raised finger, smiling at it fondly."))
N('L36', "Four thousand years. Tens of millions of lives. Beaten not by a cure, but by a nine-year-old boy, a chemist, and a needle for every dog.",
  sh('c01a', W()), sh('d20a', STILL), sh('c21a', W()), sh('c25a', W()), sh('c23a', W()))
N('L37', "Next time: a killer once thought to be beautiful. Poets died of her. Painters made her fashionable. She was the white plague.",
  sc('c32a', "A dim 19th-century sanatorium corridor at night, a row of tall windows with moonlight, a pale ghostly woman's silhouette in a long white dress holding a single candle at the far end. Ominous.", C(.5, .5, 1.04)))
HOLD(5.0, sh('c32a', O(), text=[label('NEXT TIME', 1380, 360, 110, style='title', pop=True, at=.2, len=4.6), label('SUBSCRIBE', 1380, 500, 64, at=.8, len=4.0)]))

# ---- extra cut-ins for faster cutting (pos None = end)
EXTRA = {
  'C02': [(None, ch('c02b', W(), "An 1880s country doctor's study: a single stickman doctor in a black frock coat sits at his desk shaking his head sadly, an open medical book in front of him."))],
  'L01': [(0, ch('c06c', C(.5, .5, 1.05), "A modern virology laboratory: a single stickman scientist in a white lab coat sits at a modern electron microscope, pointing with one hand at a computer screen that shows a tiny bullet-shaped virus.", text=cap('Shaped like a tiny bullet')))],
  'L03': [(None, ch('c07b', C(.5, .5, 1.05), "A cosy 1880s kitchen: a single cheerful stickman man in shirtsleeves and a waistcoat crosses off another day with one pencil on a wall calendar full of crossed-off days, a cup of coffee on the table below.", text=cap('Sometimes more than a year')))],
  'L04': [(None, ch('c07c', W(), "A cottage at night: a single stickman sits awake at the kitchen table holding his head with one hand, a candle burning low, the clock showing three in the morning."))],
  'L06': [(None, kg('c09c', C(.5, .5, 1.05), "Rabies kneels at the edge of a moonlit forest, a fruit bat hanging upside down from the branch just above his shoulder; he holds out one empty clawed hand toward a curious red fox that sniffs it, grinning at the viewer."))],
  'S02': [(None, ch('c11e', C(.5, .5, 1.05), "A dim 19th-century bedroom at night lit by a flickering candle: a wild-eyed stickman patient in a long white nightshirt lashes out with one arm, and a stickman man in a waistcoat steps back from him with both empty hands raised; they stand apart; a wolf-shaped shadow on the wall.", text=cap('Lashing out, unable to sleep')))],
  'S03': [(None, ch('c11f', C(.5, .5, 1.05), "A 19th-century sickroom lit by a candle: a stickman woman in a long dress and a white apron pours water from one jug into a cup on the bedside table, while the stickman patient in a nightshirt sitting up in bed turns his head away in terror, covering his eyes with one hand; they are apart.", text=cap('Even the sight of water')))],
  'S04': [(None, ch('c11g', W(), "A 19th-century sickroom: a stickman doctor in a frock coat holds a cloth and a small basin beside the bed of a stickman patient whose mouth has a little white froth; they are apart, not gory."))],
  'L09': [(None, cn('c13b', WR(), "A sunny ancient Mesopotamian street of mud-brick houses with a ziggurat in the distance and a palm tree: a stickman in a long fringed wool robe backs away from a snarling dog, while a stickman dog owner in a plain knee-length wool tunic holds the dog's rope leash; the two men stand apart.", text=cap('If the man dies, the owner pays')))],
  'L11': [(None, cn('c14b', WL(), "A cosy modern pub with old wooden beams and a fireplace: a single tired stickman in a modern jumper and jeans sits slumped on a bar stool, resting his head on one hand, a pint glass on the bar in front of him; a dog sleeps by the hearth.", modern=True, text=cap('Today: a hangover cure')))],
  'L13': [(None, ch('c16c', W(), "Inside a candlelit medieval chapel: a stickman priest in a brown robe holds an iron key over a small brazier, a stickman peasant with a bandaged arm waits a few steps away."))],
  'L16': [(None, ch('c18d', C(.5, .5, 1.05), "An 1880s street news kiosk: a single stickman gentleman in a bowler hat and an overcoat holds up one open newspaper with a big drawing of a snarling dog on the front page and no readable words, looking alarmed.", text=cap('Mad dog scares filled the papers')))],
  'L17': [(None, ch('c18e', WR(), "A row of clean Victorian quarantine kennels with dogs resting inside, a brick wall and a gate, morning light: a single stickman kennel keeper in a flat cap and a long brown work coat carries one bowl of food toward the kennels.", text=cap('Six months in quarantine')))],
  'L18': [(None, ch('c19c', WL(), "A green French meadow in 1881 with a small wooden pen and a farmhouse behind: a stickman vet in a black frock coat and a bowler hat gives a sheep an injection with one small syringe, while a stickman shepherd in a blue smock and a flat cap holds the sheep steady; the two men stand apart on either side of the sheep.", text=cap('Anthrax vaccine for sheep, 1881')))],
  'L20': [(None, ch('c20b', W(), "An 1885 laboratory: a single stickman lab assistant in a long apron carefully fills a small glass syringe from a flask under a lamp."))],
  'L22': [(None, sc('c21d', "A small 1885 glass syringe with a metal plunger on a white cloth beside a flask and an oil lamp. No people.", C(.5, .5, 1.05)))],
  'L24': [(None, ch('c22c', W(), "An 1885 laboratory room: a teenage stickman shepherd with a bandaged hand sits on a chair while a stickman doctor in a frock coat prepares a syringe, both apart."))],
  'L25': [(None, ch('c23b', W(), "A Paris railway platform in 1886: three stickman Russian peasants in fur hats and long coats with bandaged hands stand apart beside their bundles, looking tired and hopeful.", text=cap('Nineteen Russians bitten by a wolf')))],
  'L27': [(None, ch('c25c', C(.5, .5, 1.05), "A peaceful sunny modern village street: a stickman mother in a T-shirt and jeans and her small stickman child in shorts walk side by side, apart, the child holding the lead of a happy dog with a round vaccination tag on its collar."))],
  'L29': [(None, cn('c26c', C(.5, .5, 1.05), "A bright modern hospital room by day: a teenage stickman girl with a ponytail in a hospital gown sits up in bed, smiling weakly, while a stickman doctor in a white coat stands apart beside the bed giving a thumbs-up with one hand.", modern=True, text=cap('She survived')))],
  'A01': [(None, ch('c27b', W(), "A sunny modern hospital garden: a single stickman teenager walks slowly with a cane on a path, a stickman physiotherapist walking apart beside her.", text=cap('A lucky few recover')))],
  'L32': [(None, cn('c29c', WR(), "A dusty rural village street in South Asia at dusk with small shops and a parked motorbike: a stickman mother in a sari hurries her small stickman son in a school uniform, with a bandaged leg, by the hand toward a small modern clinic; a stray dog lies by a shop. Only these two figures.", modern=True, text=cap('Mostly in Asia and Africa')))],
  'L36': [],
}
for _k, (_i, _r, _t, _sh) in enumerate(B):
    for _pos, _s in EXTRA.get(_i, []):
        if _pos is None: _sh.append(_s)
        else: _sh.insert(_pos, _s)

# ---- QC fixes: explicit prompts without the stickman sheet (it pulls wrong-era costumes) and a modern style for modern scenes
SN = ("Humans are simple STICKMEN: plain white round head, two dot eyes, no nose, thin black stick arms, stick legs and stick feet everywhere (no realistic skin, hands as small black mitts), "
      "dressed exactly as described. Only the figures described, standing apart; each has exactly two arms and two hands attached to its sleeves. ")
MODERN = ("2D animated history explainer frame, 16:9, no text. Hand-drawn ink illustration, clean black outlines, the same muted slate-blue, grey and sepia palette as the rest of the series, soft natural daylight. "
          "The setting is modern (2000s-2020s): no lanterns, no gas lamps, no oil lamps, nothing Victorian. Not gory. ")
NOEIF = " Absolutely NO Eiffel Tower anywhere (it did not exist yet)."
FIX = {
  'c04a': (STYLE + ' ' + KING + " Medium shot: Rabies leans in a dark Paris doorway in 1885 under a gas lamp, grinning wolfishly at the viewer, one hand twirling the broken chain on his collar, the other in his pocket; a wet Haussmann-style street behind him." + NOEIF, [K_SHEET]),
  'c01a': (STYLE + ' ' + SN + "A Paris street in summer 1885 with Haussmann buildings, gas lamps and a horse cab: a stickman mother in a long dark 1880s Alsatian dress and a bonnet hurries along the pavement, leading her small stickman son in a cap, a short jacket and short trousers, with a bandaged arm, by the hand toward the door of a stone laboratory building. Only these two figures; no other people." + NOEIF, []),
  'c23a': (STYLE + ' ' + SN + "A grand red-brick and stone institute building in Paris in 1888 with a wrought-iron gate and trees around, no flags: at the open gate, a stickman chemist with a short grey beard drawn as a simple line, a black skullcap and a black 1880s frock coat welcomes a stickman mother in a shawl and a long 1880s dress who holds the hand of her small stickman child in a cap. Only these three figures, standing apart." + NOEIF, []),
  'c23b': (STYLE + ' ' + SN + "A Paris railway station of 1886 with an iron and glass roof and a steam train: three stickman Russian peasants in 1880s fur hats and long sheepskin coats, with bandaged hands, stand apart beside their cloth bundles, looking tired and hopeful." + NOEIF, []),
  'c18b': (STYLE + ' ' + SN + "An 1880s London street corner: a stickman policeman in a tall dark Victorian police helmet and dark coat holds a dog's leather muzzle in one hand and a coiled rope leash in the other, no poles, no nooses, no knots; a stickman newspaper boy in a flat cap holds up a blank newspaper; both stand apart.", []),
  'd01a': (STYLE + ' ' + DIAG + "ONLY these three things side by side, nothing above or below them: (1) an hourglass with the sand running out, (2) a small plain cross, (3) a single row of ten empty circles, none of them ticked. No people and no human figures anywhere in the picture.", []),
  'd04a': (STYLE + ' ' + SN + DIAG + "One single standing stickman with stick legs and stick feet and a tiny dot bite mark on his stick ankle; a glowing dotted line runs from the ankle up his stick leg and spine into his round head, with circled digits 1, 2, 3 along the path; a small calendar icon beside him. No magnifier circles, no anatomy.", []),
  'd08a': (STYLE + ' ' + SN + DIAG + "Two numbered panels: (1) a stickman in a plain nightshirt lying in bed with a thermometer in his mouth and wavy heat lines above him, both arms on top of the blanket; (2) the same stickman sitting on a stool scratching his thin black stick ankle, where small zigzag tingling lines appear.", []),
  'd09a': (STYLE + ' ' + DIAG + "ONE single large simple cartoon stickman head in the centre: a plain white circle with two wide dot eyes and a frightened wavy mouth; inside the circle a dark tangled storm cloud with small yellow lightning bolts; around the head a few small drawings of floating shadows and twisting shapes. No brain anatomy, no skull, no body, no other figures.", []),
  'd14a': (STYLE + ' ' + SN + DIAG + "Three numbered ancient Roman remedies; every figure is an ancient Roman in a plain white toga and sandals: (1) a hot iron rod glowing over a bronze brazier, (2) a small clay bowl with a dark lump of liver, (3) a stickman in a toga being lowered into a garden pond by two other stickmen in togas.", []),
  'd21a': (STYLE + ' ' + SN + DIAG + "A staircase of five numbered steps; ONE single stickman in a plain shirt and trousers climbs it; on each step a small glass syringe with a small bullet-shaped virus symbol that gets bigger step by step; on the top step the stickman holds a small round shield while a large bullet-shaped virus bounces off it.", []),
  'd26a': (STYLE + ' ' + DIAG + "ONLY a neat grid of about forty small identical simple stickman icons (white round heads, stick bodies) filling the frame, all drawn in faded grey with a tiny cross above each, except two bright ones with a small gold star above them. Nothing else: no scenes, no rows of pictures.", []),
  'd25a': (MODERN + SN + DIAG.replace('on aged paper', 'on clean light paper') + "Three numbered steps with modern stickmen: (1) a stickman in a T-shirt washes his hand under a modern chrome tap with soap, a small clock showing fifteen minutes, (2) a modern plastic syringe of vaccine, (3) a second modern syringe with small Y-shaped antibody symbols.", []),
  'c25a': (MODERN + SN + "A modern 2020s village vet clinic under a tree in a sunny rural town: a stickman vet in modern blue scrubs gives a small injection to a calm dog held by a stickman girl in a modern T-shirt and jeans; both stand apart.", []),
  'c25b': (MODERN + SN + "A modern clinic treatment room: a stickman nurse in blue scrubs washes the hand of a stickman patient in a modern T-shirt and jeans at a modern sink with a soap dispenser; both stand apart.", []),
  'c29b': (MODERN + SN + "A sunny modern African village square with a concrete building and a parked motorbike: a stickman health worker in a modern hi-vis vest and cap gives a dog a vaccine while a stickman child in a T-shirt and shorts holds the dog's lead; a modern blue cool box on a plastic table behind them.", []),
  'c25c': (MODERN + SN + "A peaceful sunny modern village street with concrete houses: a stickman mother in a modern T-shirt and jeans and her small stickman child in a T-shirt and shorts walk side by side, apart, smiling; the child holds the lead of a happy dog wearing a collar with a round vaccination tag. No readable words.", []),
  'c28a': (MODERN + "A modern vaccine vial and a modern plastic syringe on a clean steel tray in a bright modern laboratory with white cabinets, a small round dog tag beside them. No people and no human figures anywhere in the picture.", []),
  'c06c': (MODERN + SN + "A modern virology laboratory with white cabinets: a single stickman scientist in a white lab coat sits at a modern electron microscope, pointing with one hand at a computer screen that shows one tiny bullet-shaped virus. No readable words.", []),
  'd29a': (STYLE + ' ' + DIAG + "ONLY a simple world map filling the whole frame: Africa and South and Southeast Asia shaded dark red-brown; Europe, North America, South America and Australia pale; a few small stickman child icons over the dark regions. Nothing else, no extra rows or panels.", []),
  'd30a': (STYLE + ' ' + DIAG + "ONLY one simple line chart filling the whole frame: a line that falls from high on the left to zero on the right, with a small dog icon wearing a round tag at the end of the line and a small target symbol. No axis numbers, no extra pictures, no rows of panels. No people.", []),
  'd31a': (STYLE + ' ' + DIAG + "Two side-by-side close-up squares on aged paper: (1) a plain beige square with two neat curved rows of small dark dots like a dog's bite pattern, (2) a plain beige square with just two tiny dark dots next to a small coin for scale. No blood, no wounds. No people.", []),
}
for _i, (_m, _p) in NS.items():   # stickmen scenes outside 1600-1900: explicit era clothing, no stickman sheet
    FIX.setdefault(_i, ((MODERN if _m else STYLE + ' ') + SN + _p, []))

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
                out.append({'img': s['img'], 'prompt': STYLE + ' ' + pr, 'refs': refs} if s['img'] not in FIX else {'img': s['img'], 'prompt': FIX[s['img']][0], 'refs': FIX[s['img']][1]})
    json.dump(out, open(os.path.join(ROOT, 'tools/plague/ep06_frames_todo.json'), 'w'), indent=1); print(len(out), 'frames')

def beats():
    out = {'base': 'assets/plague/ep06/frames', 'keep_zoom': [], 'static': True, 'fade_in': .8, 'start': 0.0, 'lead': .45, 'gap': .6, 'max_shot': 3.2,
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
        if i: out['beats'].append({'vo': f'assets/plague/ep06/vo/{i}.wav', **({'gain': 1.05} if r == 'RABIES' else {}), 'shots': sl})
        else: out['beats'].append({'hold': t, 'shots': sl})
    json.dump(out, open(os.path.join(ROOT, 'tools/plague/ep06_beats.json'), 'w'), indent=1); print(len(out['beats']), 'beats')

MUSIC = [(0, 184, 'cholera_a.mp3'), (180, 280, 'plague_b.mp3'), (276, 430, 'cholera_b.mp3'), (426, 'ALL', 'plague_a.mp3')]   # open+who+origin | symptoms+ancient | 1800s+Pasteur | modern+aftermath+today

{'lines': lines, 'frames': frames, 'beats': beats}[sys.argv[1]]()
