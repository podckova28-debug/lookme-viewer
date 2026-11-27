# frame -> (part, line index, prompt, note). One shot per script line (ketchup formula). Running gag: James Gillray at his desk drawing a tiny Napoleon.
STYLE = ("White background; detailed ink-line illustration, fine cross-hatching, soft muted watercolour, French blue, deep green and gold accents, "
         "playful humorous cartoon tone; cut out on white, lots of white space. ")
NAP46 = ("NAPOLEON at 46 (as in reference image): a pale, slightly plump man, short dark-brown hair combed forward, clean-shaven, "
         "plain dark-green coat with red collar, white waistcoat, white breeches, black boots, black bicorne hat worn sideways")
BOY = ("NAPOLEONE as a thin serious 9-year-old Corsican boy (as in reference image): olive skin, long straight dark hair, big grey eyes, "
       "a plain worn brown coat that is too big for him")
CADET = ("NAPOLEONE as a thin serious teenager of 15-16 (as in reference image): olive skin, long straight dark hair to the collar, "
         "big grey eyes, a blue French artillery officer's coat with red trim")
GILL = ("JAMES GILLRAY, an 18th-century English cartoonist with a round face, powdered grey wig tied back, spectacles, a brown coat, "
        "drawing with a quill at a slanted desk")
YOU = "stick-figure 'you' in a British sailor's flat round hat and striped shirt"
SHOTS = [
 # p0 — Saint Helena, 1815
 (0,0,f"{YOU} standing on the deck of a wooden sailing warship, saluting","you"),
 (0,1,"a large British wooden warship of 1815 with furled sails anchored next to a tall, steep, bare volcanic island rising from the ocean, no other land","Oct 1815"),
 (0,2,"a small hand-drawn map of the South Atlantic: Africa on the right, South America on the left, a tiny dot in the middle of the ocean with a red circle","Saint Helena"),
 (0,3,"a hand-drawn map with a long dotted line and a ruler from the tiny island to the coast of Africa","~2,000 km"),
 (0,4,f"{NAP46}, standing alone at the wooden rail of the ship with his hands behind his back, looking at the island, sad","the passenger"),
 (0,5,"an old map of Europe in 1810 where most of the continent is shaded French blue, a tiny golden crown sitting on Paris","1810"),
 (0,6,"an Austrian emperor in a white uniform handing over his young daughter in an 1810 wedding dress, she is holding a bouquet; both visible from the waist up","his own daughter"),
 (0,7,"seven little marching columns of soldiers in different uniforms, all heading toward one tiny French soldier, no flags","7 coalitions"),
 (0,8,"a small damp grey stone farmhouse on a misty windswept plateau, a few bent trees, a broken fence; objects only, no people","Longwood House"),
 (0,9,"a fat cartoon rat sitting in a gilded armchair inside a shabby room, wearing a tiny bicorne hat, looking smug","with rats"),
 (0,10,f"{YOU} scratching his head, a thought bubble above him showing a very tiny man in a bicorne hat",""),
 (0,11,"a tiny cartoon Napoleon in a bicorne hat standing next to a giant ruler and barely reaching the first mark","short?"),
 (0,12,"a big hand-drawn red 'WRONG' stamp across a little drawing of a tiny man in a bicorne hat; objects only","nope"),
 (0,13,f"{NAP46}, standing straight next to a tall wooden measuring board, his head at the 169 cm mark, two average Frenchmen of 1815 of exactly the same height standing on either side","1.69 m = average"),
 (0,14,f"{GILL}, grinning wickedly while drawing on a sheet of paper a ridiculous tiny Napoleon having a tantrum","Little Boney"),
 (0,15,"a dotted arrow from a small whitewashed house on a rocky Mediterranean island to a golden imperial throne with a bee pattern; objects only, no people","island → emperor?"),
 (0,16,f"{NAP46}, sitting on a wooden crate in a shabby room, chin in his hand, a rat looking at him from the floor","how?"),
 (0,17,"a big hand-drawn 'SPOILER' stamp in red ink; objects only",""),
 (0,18,"three items in a row on white: a bronze cannon, a snowflake with a frowning face, and a quill pen; objects only","cannons, winter, ..."),
 (0,19,f"{GILL}, looking up from his desk directly at the viewer and slowly sharpening his quill with a small knife, a sly smile","not done yet"),
 # p1 — Corsica and school
 (1,0,"a rugged mountainous Mediterranean island seen from the sea, small fishing boats, a little harbour town with a citadel","Corsica"),
 (1,1,"an old hand-drawn map of the western Mediterranean showing Corsica, Italy and the south of France, a little arrow to Corsica",""),
 (1,2,"an 18th-century Genoese merchant in a red cap and coat holding a deed with a wax seal; visible from the chest up",""),
 (1,3,"a hand-drawn map: a big arrow carrying the island of Corsica from Genoa to France like a parcel with a bow","1768"),
 (1,4,"a narrow street of tall pastel houses in the 18th-century town of Ajaccio, Corsica, a house with green shutters marked with a small star; no people","15 Aug 1769"),
 (1,5,"a newborn baby in white swaddling clothes in a wooden cradle, a tiny frown on his face","Napoleone di Buonaparte"),
 (1,6,"a hand-written baby name tag 'Napoleone di Buonaparte' with a small laurel doodle, and a French beret hovering over it confused; objects only","very French?"),
 (1,7,"CARLO BUONAPARTE, an elegant 18th-century Corsican lawyer in a powdered wig and a fancy but patched coat, proudly holding up an empty purse","noble, broke"),
 (1,8,"LETIZIA BUONAPARTE, a stern beautiful 18th-century Corsican mother in a dark dress, surrounded by a line of small children of different heights","13 children, 8 survive"),
 (1,9,f"{BOY} standing alone on a quay next to a small wooden trunk, waving goodbye, a ship behind him","age 9 → France"),
 (1,10,f"{BOY} at a school desk staring in panic at a French grammar book","French?"),
 (1,11,"a group of 1780s French schoolboys in blue uniforms laughing and pointing; visible from the waist up","the accent"),
 (1,12,f"{BOY} sitting alone on a bench in a school courtyard while other boys play in the background","no friends"),
 (1,13,f"{BOY} sitting under a tree with a tower of old books next to him, reading intensely",""),
 (1,14,"open old history books with small engravings of Alexander the Great on a horse and Julius Caesar in a laurel wreath, a stack of maths notes with triangles; objects only","heroes"),
 (1,15,"the grand 18th-century École Militaire building in Paris with its dome, soldiers at the gate","1784 Paris"),
 (1,16,f"{CADET} holding a letter with a black seal, looking down sadly","1785"),
 (1,17,f"{CADET} studying at a desk by candlelight with a clock behind him whose hands are spinning fast","2 years → 1"),
 (1,18,f"{CADET} standing proudly next to a small bronze cannon","age 16, artillery"),
 (1,19,"a long handwritten 1785 school ranking list on paper, one line in the middle circled in red ink: '42. Buonaparte'; objects only","42 / 58"),
 (1,20,"a small paper gold star with a sad face drooping; objects only","not a genius..."),
 (1,21,"a small paper gold star with a sly smile and a tiny wink; objects only","yet"),
 (1,22,"an old map of France with a cartoon dynamite stick fizzing in the middle of Paris; objects only","1789"),
 (1,23,f"{CADET} smiling for the first time, rubbing his hands next to a cannon","his speciality"),
]
NEG = " Anatomically correct people: every person has exactly two arms, two hands and five fingers per hand; no extra or floating limbs."
REF = {"NAPOLEON at 46": "nap46", "NAPOLEONE as a thin serious 9": "boy", "NAPOLEONE as a thin serious teen": "cadet", "JAMES GILLRAY": "gill"}
def prompt(i):
    p, l, d, n = SHOTS[i - 1]
    note = f" Handwritten marker note + arrow: '{n}'." if n else " No text."
    if "stick figure" in d or "stick-figure" in d:
        note += " Stick figures = simple white round-headed stick figure with dot eyes, exactly two arms and two legs; it is the only stick figure."
    else: note += " No stick figures; all people drawn realistically."
    extra = " Only what is described: do not add extra people or objects."
    r = refs(i)
    if r: extra += " The reference image shows this person: draw him with exactly that face, hair and clothes, but in the pose and scene described; use it only for him."
    return STYLE + d + "." + note + extra + NEG
CHAR = {l.split()[0]: l.split()[1] for l in open(__file__.rsplit("/", 1)[0] + "/chars/jobs.txt")} if __file__.count("/") else {}
def refs(i):
    d = SHOTS[i - 1][2]; return [v for k, v in REF.items() if k in d]
def request(i):
    return {"index": i, "params": {"model": "gpt_image_2_6", "aspect_ratio": "16:9", "use_unlim": False, "prompt": prompt(i),
            "medias": [{"role": "image_references", "value": CHAR[r]} for r in refs(i)]}}
if __name__ == "__main__":
    print(len(SHOTS))
# per-frame review fixes (wave 2): objects-only where people were added, garbled rulers, anachronisms
OBJ = "; objects only: absolutely no people, no hands, no faces anywhere in the picture"
FIX = {
 3: "a small old hand-drawn paper map of the South Atlantic lying flat on white: Africa on the right, South America on the left, a tiny dot in the middle of the ocean circled in red" + OBJ,
 4: "an old paper map lying flat on white with a long dotted line and a brass ruler from a tiny island to the coast of Africa" + OBJ,
 6: "an old paper map of Europe in 1810 lying flat on white where most of the continent is shaded French blue, a tiny golden crown sitting on Paris" + OBJ,
 12: "a tiny cartoon Napoleon in a bicorne hat and blue coat standing next to a giant blank wooden ruler with no numbers at all, his hat barely reaching its first mark",
 14: "NAPOLEON at 46 (as in reference image) standing straight between two ordinary Frenchmen of 1815, a working man in a brown coat and a soldier in a blue coat, all three exactly the same height, a thin red horizontal line touching the tops of all three heads; no ruler, no numbers",
 18: "a big hand-drawn 'SPOILER' rubber stamp mark in red ink in the middle of white paper" + OBJ,
 19: "three items in a row on white: a plain bronze cannon on a wooden carriage with no decorations, a snowflake with a frowning face, and a white goose-feather quill pen" + OBJ,
 29: "LETIZIA BUONAPARTE, a stern beautiful 18th-century Corsican mother in a dark dress, standing with exactly EIGHT children of different heights in a row beside her, five boys and three girls; count them: eight children",
 30: "NAPOLEONE as a thin serious 9-year-old Corsican boy (as in reference image) standing alone on a stone quay next to a small wooden trunk, waving goodbye, a wooden sailing ship behind him with NO flags at all",
 35: "two open old history books on white: one with an engraving of Alexander the Great riding a horse, one with an engraving of Julius Caesar in a laurel wreath next to plain Roman temple columns, no amphitheatre; a stack of maths notes with simple triangles" + OBJ,
 40: "a long handwritten 1785 school ranking list on a single sheet of old paper lying flat, one line in the middle circled in red ink" + OBJ,
 41: "a small paper gold star lying on white with a sad drooping face" + OBJ,
 43: "an old paper map of France lying flat on white, a round black powder keg with a lit fizzing fuse sitting on Paris, no scale bar, no compass" + OBJ,
}
for _k, _d in FIX.items(): SHOTS[_k - 1] = SHOTS[_k - 1][:2] + (_d,) + SHOTS[_k - 1][3:]
FIX[40] = ("a short handwritten 1785 school ranking list on a single sheet of old paper lying flat, only five lines are visible and readable: "
           "'40. Lambert', '41. Morel', '42. Buonaparte', '43. Dubois', '44. Petit'; the line '42. Buonaparte' is circled in red ink" + OBJ)
SHOTS[39] = SHOTS[39][:2] + (FIX[40],) + SHOTS[39][3:]
