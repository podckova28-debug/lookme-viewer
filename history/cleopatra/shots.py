# frame -> (part, line index, prompt, note). One shot per script line (ketchup/Napoleon formula).
# Running gag: the Roman propaganda POET writing a scroll "THE EVIL EGYPTIAN QUEEN".
STYLE = ("White background; detailed ink-line illustration, fine cross-hatching, soft muted watercolour, turquoise, gold and deep red accents, "
         "playful humorous cartoon tone; cut out on white, lots of white space. Ancient Mediterranean of the 1st century BC: no modern objects, "
         "no glass bottles, no paper books (only papyrus scrolls and wax tablets), no stirrups, no flags. ")
C21 = ("CLEOPATRA at 21 (as in reference image): olive skin, large dark eyes, strong slightly hooked nose, dark-brown hair in the Greek melon hairstyle "
       "pulled into a low bun with a flat white diadem ribbon, white Greek chiton with turquoise-and-gold border, deep red himation")
C39 = ("CLEOPATRA at 39 (as in reference image): olive skin, large dark eyes, strong slightly hooked nose, dark-brown hair in the Greek melon hairstyle "
       "with a flat white diadem ribbon, gold collar, deep purple Greek gown with gold border")
CAES = ("JULIUS CAESAR (as in reference image): thin wiry Roman, long lined face, receding short grey-brown hair combed forward, clean-shaven, "
        "bronze muscle cuirass, red cloak")
ANT = ("MARK ANTONY (as in reference image): big muscular Roman, short dark curly hair, short dark beard, bronze muscle cuirass, red cloak")
OCT = ("OCTAVIAN (as in reference image): slim young Roman with a cold face, light-brown hair in a short fringe, clean-shaven, white toga with a narrow purple border")
POET = ("the ROMAN POET (as in reference image): skinny bald man with a big nose, sly grin, laurel wreath, cream tunic, writing with a reed pen on a long papyrus scroll")
YOU = "stick-figure 'you' as a Roman legionary with a small bronze helmet with a red crest and a red tunic"
OBJ = "; objects only: absolutely no people, no hands, no faces anywhere in the picture"
SHOTS = [
 # p0 — the tomb, 30 BC
 (0,0,f"{YOU} standing at attention holding a tall rectangular red Roman shield","you"),
 (0,1,"a massive two-storey stone mausoleum with a tall bronze door, by the sea in Alexandria, palm trees, a lighthouse tower far away, hot August light; no people","Aug 30 BC"),
 (0,2,"a dim tomb interior lit by oil lamps in clay dishes, heaps of gold coins, jewel chests and ivory, two worried servant women in plain linen dresses standing by a closed bronze door",""),
 (0,3,f"{C39} sitting proudly on a gilded couch inside a dim tomb, chin up","Cleopatra"),
 (0,4,"a fallen Roman general's red cloak and bronze helmet lying on a stone floor next to a broken sword" + OBJ,""),
 (0,5,"burning ancient wooden warships with oars sinking in a bay, black smoke; no people","no navy"),
 (0,6,f"{OCT} pointing at a drawing of a woman in chains being led in a Roman triumph parade, smiling coldly","Octavian"),
 (0,7,f"{YOU} scratching his helmet with three thought bubbles above him",""),
 (0,8,"a small papyrus sign with a pyramid and a sphinx drawn on it" + OBJ,"Egyptian?"),
 (0,9,"a golden hand mirror with sparkles and little hearts around it" + OBJ,"most beautiful?"),
 (0,10,"a coiled cobra next to a basket of figs" + OBJ,"snake?"),
 (0,11,"a big hand-drawn red 'WRONG' stamp across the little papyrus sign with the pyramid" + OBJ,"nope"),
 (0,12,"a big question mark made of ancient silver coins" + OBJ,"unknown"),
 (0,13,"two ancient scholars in togas arguing over a scroll, pointing at different lines; visible from the waist up","still arguing"),
 (0,14,f"{YOU} squinting closely at a small ancient silver coin showing a woman's profile with a big nose",""),
 (0,15,f"{OCT} standing with arms crossed, and next to him {POET}","who wrote it?"),
 (0,16,"a big hand-drawn 'SPOILER' stamp in red ink on papyrus" + OBJ,""),
 (0,17,f"{POET} grinning wickedly and holding up a long scroll with the big painted title 'THE EVIL EGYPTIAN QUEEN'","the writer"),
 (0,18,f"{POET} scribbling furiously, a huge pile of finished scrolls growing beside him","very busy"),
 # p1 — a Greek family
 (1,0,"an old papyrus map of the eastern Mediterranean with a dotted line from Macedonia to Egypt" + OBJ,""),
 (1,1,"the ancient harbour city of Alexandria with white marble palaces, the tall Pharos lighthouse and many trading ships; no flags","c. 69 BC"),
 (1,2,"a family tree on papyrus with twelve little gold crowns on the branches" + OBJ,"~300 years"),
 (1,3,"a big hand-drawn red 'NOT EGYPTIAN' stamp across a picture of a pyramid" + OBJ,"not Egyptian"),
 (1,4,"a white Greek marble column with a laurel wreath, a Greek amphora and a lyre" + OBJ,"Greek!"),
 (1,5,"PTOLEMY I, a tough Macedonian general in a bronze helmet and cloak, carrying away a small model of Egypt with a pyramid under his arm like stolen luggage","Ptolemy"),
 (1,6,"a row of six identical Greek kings in diadems, all with the same face and the same name tag" + OBJ.replace('no faces','') ,"Ptolemy, Ptolemy, Ptolemy..."),
 (1,7,"three name tags on papyrus: 'Cleopatra', 'Berenice', 'Arsinoe'" + OBJ,""),
 (1,8,"a big gold Roman-numeral VII on a royal seal" + OBJ,"Cleopatra VII"),
(1,9,"an old papyrus scroll titled 'FAMILY RULES' with a wax seal" + OBJ,"family tradition"),
 (1,10,"a Greek royal wedding where a young king and a young queen who look exactly alike, like brother and sister, hold hands awkwardly",""),
 (1,11,"a family tree on papyrus with several branches cut off by a cartoon dagger" + OBJ,""),
 (1,12,"a small poison vial, a dagger and a cushion on a palace table with a 'family dinner' card" + OBJ,"a lot"),
 (1,13,f"{C21} as a girl of 15 studying Egyptian hieroglyphs on a papyrus with a reed pen, an old Egyptian priest-teacher with a shaved head nodding","Egyptian"),
 (1,14,f"{C21} surrounded by speech bubbles in Greek, Hebrew, Aramaic and hieroglyphs","~9 languages"),
 (1,15,"a Greek kithara (lyre) with many strings and a few musical notes floating from it" + OBJ,"Plutarch"),
 (1,16,f"{C21} tapping her temple with one finger and smiling slyly","clever"),
 (1,17,"a game board with Roman and Egyptian pieces, a dark storm cloud gathering over it" + OBJ,""),
 # p2 — brother-husband, Caesar arrives
 (2,0,"an old Greek king's golden diadem lying on a pillow next to a candle that has gone out; no people","51 BC"),
 (2,1,f"{C21} crowned with the diadem on a throne, looking determined","18"),
 (2,2,"a papyrus will with a royal seal and two little crowns drawn on it" + OBJ,"rule together"),
 (2,3,"PTOLEMY XIII, a sulky ten-year-old Greek boy king with a too-big diadem, sticking out his tongue","10"),
 (2,4,f"{C21} and the sulky boy king PTOLEMY XIII standing apart at a small wedding, both rolling their eyes",""),
 (2,5,"two thrones pulled apart, one tipped over" + OBJ,"badly"),
 (2,6,"three scheming bearded court advisers in Greek robes whispering behind their hands and glaring","the advisers"),
 (2,7,f"{C21} being pushed out of a palace gate by palace guards, her red himation flying","48 BC"),
 (2,8,f"{C21} standing on a desert hill in front of a camp of soldiers with spears and tents, arms crossed","Syria"),
 (2,9,"a big Roman war galley with oars and a ram sailing into Alexandria harbour, the Pharos lighthouse behind; no flags",""),
 (2,10,f"{CAES} standing on the prow of a galley, arms crossed, stern face","Julius Caesar"),
 (2,11,"a Roman general on horseback galloping away along a beach, looking back nervously; no stirrups","Pompey"),
 (2,12,"the three scheming bearded advisers bowing and offering a covered silver platter with a cloth over it",""),
 (2,13,"a closed silver platter with a cloth over it on a table, a fly buzzing above" + OBJ,"surprise"),
 (2,14,f"{CAES} looking disgusted and turning his face away, holding his nose",""),
 (2,15,f"{C21} with a small sparkle of an idea above her head, eyes narrowed",""),
 (2,16,"a hand-drawn diagram: a crown, an arrow, and a Roman helmet, with the words 'first wins'" + OBJ,"first to Caesar"),
 (2,17,f"{C21} frowning at a papyrus map of Alexandria with the palace circled","one problem"),
 (2,18,"palace walls of Alexandria at night lined with Greek soldiers with spears and torches; no people inside the windows","guarded"),
 # p3 — the carpet
 (3,0,"a small rowing boat at night slipping to the palace steps of Alexandria, one oarsman, a long rolled bundle in the boat",""),
 (3,1,"APOLLODORUS, a strong Sicilian servant in a plain tunic, carrying a long rolled patterned carpet on his shoulder up palace stairs at night","the carpet"),
 (3,2,f"{CAES} sitting at a desk with scrolls, looking up surprised as the servant puts a rolled carpet on the floor",""),
 (3,3,f"{C21} rolling out of an unrolled carpet onto a marble floor and standing up with a dramatic 'ta-da' pose","surprise!"),
 (3,4,f"{CAES} raising his eyebrows, arms crossed","52"),
 (3,5,f"{C21} smiling confidently, hands on hips","21"),
 (3,6,f"{CAES} and {C21} shaking hands at breakfast at sunrise, a bowl of fruit on the table","allies"),
 (3,7,"a small heart drawn on a papyrus contract with a wax seal" + OBJ,"more than allies"),
 (3,8,"the sulky boy king PTOLEMY XIII stamping his feet and throwing his diadem on the floor in a tantrum","war"),
 (3,9,"warehouses and scroll shelves burning by the harbour in Alexandria, papyrus scrolls flying in the smoke; no people","the Library?"),
 (3,10,"a heavy golden breastplate lying on the muddy bank of the Nile among reeds" + OBJ,"drowned"),
 (3,11,f"{C21} back on the throne, smiling, the diadem on her head","queen again"),
 (3,12,"a twelve-year-old Greek boy king PTOLEMY XIV in a diadem holding a marriage papyrus, looking bored","just paperwork"),
 (3,13,f"{C21} holding a swaddled baby, smiling","47 BC"),
 (3,14,"a baby in a tiny Roman red cloak and a tiny laurel wreath in a cradle","Caesarion"),
 (3,15,"the same baby frowning seriously like a tiny general, arms crossed","little Caesar"),
 (3,16,f"{OCT} as a teenager in a toga reading a letter in Rome, narrowing his eyes","Octavian"),
 # p4 — Rome and the Ides of March
 (4,0,f"{C21} arriving in Rome on a litter carried by servants, Romans in togas staring with open mouths","46 BC Rome"),
 (4,1,"a Roman villa with gardens across a river, Rome's temples on the other bank; no people","across the Tiber"),
 (4,2,"a golden statue of a woman with a diadem in a Roman temple, Romans pointing at it" ,"gold statue"),
 (4,3,"three outraged Roman senators in togas with purple stripes, clutching their chests; visible from the waist up","horrified"),
 (4,4,"a little sign 'FOREIGN QUEEN' with an arrow" + OBJ,""),
 (4,5,"a sign 'IN ROME' with an exclamation mark" + OBJ,""),
 (4,6,"a gold statue with a sign 'WITH A GOLD STATUE'" + OBJ,""),
 (4,7,"Roman senators in togas surrounding a man at the foot of a statue, daggers raised, seen from behind; no blood","Ides of March, 44 BC"),
 (4,8,"a red Roman general's cloak lying on marble steps with twenty-three tally marks chalked beside it; no blood" + OBJ,"23"),
 (4,9,"a papyrus will with a wax seal being unrolled" + OBJ,""),
 (4,10,"a baby's cradle crossed out with a red X" + OBJ,"not Caesarion"),
 (4,11,f"{OCT} as a young man holding up the will with a small cold smile","Octavian"),
 (4,12,"a Roman road with a fast litter rushing toward a harbour, dust flying; no faces visible","leave!"),
 (4,13,"a goblet tipped over on a table next to a small vial" + OBJ,"44 BC"),
 (4,14,"two modern historians in suits nodding seriously at an ancient vial in a museum case; visible from the waist up","poisoned?"),
 (4,15,f"{C21} on the throne holding a three-year-old boy on her lap who wears a tiny diadem","co-ruler, age 3"),
 (4,16,"the toddler king napping on a throne cushion, drooling" ,"easy"),
 # p5 — Antony
 (5,0,"a map of the Mediterranean split in two halves, a red half and a gold half, two little Roman helmets on either side" + OBJ,"West / East"),
 (5,1,f"{ANT} sitting in a Roman camp chair tapping his foot impatiently, a summons scroll in his hand","41 BC Tarsus"),
 (5,2,f"a huge golden barge with purple sails and silver oars on a river, flute players and incense, {C21} reclining under a gold canopy dressed as Aphrodite","Aphrodite"),
 (5,3,f"{ANT} standing on a riverbank with his jaw dropped",""),
 (5,4,f"{ANT} and {C39} at a lavish banquet with dancers and musicians, golden cups","a party"),
 (5,5,"a banquet table covered with empty plates and tipped cups at dawn" + OBJ,"for days"),
 (5,6,f"{C21} holding up one finger in a wager, {ANT} laughing","10,000,000 sesterces"),
 (5,7,f"{C21} dropping a giant pearl from her earring into a gold cup of vinegar","the pearl"),
 (5,8,"a modern scientist in a lab coat watching a pearl in a glass beaker, a clock showing many hours passed, yawning","scientists"),
 (5,9,"a pearl at the bottom of a beaker barely dissolved, a stopwatch beside it" + OBJ,"very long"),
 (5,10,"a big gold star with the words 'great story'" + OBJ,""),
 (5,11,f"{ANT} following {C21} up the steps of an Alexandrian palace like a happy puppy","Alexandria"),
 (5,12,f"{ANT} and several Roman and Greek friends raising wine cups at a rowdy feast, a sign on the wall 'INIMITABLE LIVERS'","the club"),
 (5,13,f"{C21} holding two babies in her arms","40 BC twins"),
 (5,14,"two babies in a cradle, one with a little sun above it and one with a little moon","Sun & Moon"),
 (5,15,f"{POET} sharpening his reed pen with a knife and grinning","meanwhile..."),
 # p6 — propaganda war
 (6,0,f"{ANT} at a Roman wedding with OCTAVIA, a calm Roman lady in a white stola, both looking politely bored","Octavia"),
 (6,1,f"{ANT} sneaking out of a Roman house at night with a bag, waving goodbye","anyway"),
 (6,2,f"a grand ceremony in Alexandria: {ANT} and {C39} sitting on two golden thrones on a silver platform, a cheering crowd","34 BC"),
 (6,3,"a map of the eastern Mediterranean with kingdoms gift-wrapped in ribbons" + OBJ,"kingdoms as gifts"),
 (6,4,f"{OCT} rubbing his hands with a cold smile","perfect"),
 (6,5,f"{OCT} speaking to the Roman Senate in a hall with marble benches, pointing at a painting of an Egyptian sorceress","bewitched!"),
 (6,6,f"{OCT} reading out a scroll in the Senate, senators gasping","the will"),
 (6,7,"a red X over a little drawing of a Roman general" + OBJ,"not Antony..."),
 (6,8,"a little drawing of a queen with a red target circle around it" + OBJ,"...Cleopatra"),
 (6,9,"two signs side by side: 'ROMAN GENERAL' crossed out, 'FOREIGN QUEEN' with a tick" + OBJ,"easier enemy"),
 (6,10,f"{POET} and two more grinning Roman poets in laurel wreaths writing scrolls at a long table, one titled 'THE EVIL EGYPTIAN QUEEN'","the poets"),
 (6,11,"a wall of scrolls with titles 'HARLOT QUEEN', 'DRUNK', 'MONSTER OF THE NILE'" + OBJ,""),
 (6,12,"the three Roman poets shrugging, a little empty portrait frame in front of them labelled 'never met her'","never met her"),
 # p7 — Actium, Antony's death
 (7,0,"two fleets of ancient oared warships facing each other off a rocky Greek coast","2 Sept 31 BC Actium"),
 (7,1,"sixty ships with purple sails breaking through the middle of a sea battle and sailing away" + OBJ.replace('no faces',''),"60 ships"),
 (7,2,f"{ANT} jumping into a small fast ship to follow, looking back at his fleet",""),
 (7,3,"Roman soldiers on a beach laying down their shields and spears in surrender","abandoned"),
 (7,4,"three question marks over a map of the battle" + OBJ,"why?"),
 (7,5,"three small icons on papyrus: a map with an escape arrow, a frightened face, and a wind cloud" + OBJ.replace('no faces',''),""),
 (7,6,f"{POET} smugly writing one big word on his scroll",""),
 (7,7,"a scroll with the single word 'COWARD' in big red letters" + OBJ,"cowardice"),
 (7,8,f"{OCT} at the head of a Roman army marching toward the walls of Alexandria","30 BC"),
 (7,9,f"{ANT} in his tent receiving a messenger who whispers with a sad face","false news"),
 (7,10,"a Roman sword lying on the floor of a tent next to a red cloak; no blood" + OBJ,""),
 (7,11,f"{C39} and two servant women pulling ropes at a high window of a stone mausoleum, the ropes going down out of sight","the window"),
 (7,12,f"{C39} kneeling and weeping over a red cloak on the floor of a tomb","goodbye"),
 (7,13,f"{C39} standing defiantly as Roman soldiers enter the tomb through a window","captured"),
 # p8 — death and legacy
 (8,0,f"{OCT} drawing a plan of a triumph parade with a little queen in chains","alive!"),
 (8,1,f"{C39} looking at a small painting of a captured queen in chains in a Roman parade, cold and determined",""),
 (8,2,"a peasant in a straw hat carrying a basket of green figs past two Roman guards who wave him through","10 Aug 30 BC"),
 (8,3,"an empty golden couch in a dim tomb, a diadem ribbon and a gold collar lying on the cushion, a basket of figs on the floor; no people","39"),
 (8,4,"a single snuffed oil lamp with a curl of smoke" + OBJ,"age 39"),
 (8,5,"a basket of figs with a big question mark above it" + OBJ,"a snake?"),
 (8,6,"two ancient Greek historians in togas shrugging at each other; visible from the waist up","they weren't sure"),
 (8,7,"a measuring tape next to a very long Egyptian cobra that is much longer than a small fig basket" + OBJ,"~2 m"),
 (8,8,"a small ancient poison vial and a hairpin on a table" + OBJ,"poison?"),
 (8,9,"a teenage boy's small diadem lying on a road; no people" ,"Caesarion"),
 (8,10,"two small Roman helmets, one crossed out" + OBJ,"too many Caesars"),
 (8,11,"a map of Egypt being stamped with a Roman eagle seal" + OBJ,"Roman province"),
 (8,12,f"{OCT} in a white toga being crowned with a golden laurel wreath, the name tag 'AUGUSTUS'","Augustus"),
 (8,13,f"{POET} proudly handing a finished scroll 'THE EVIL EGYPTIAN QUEEN' to {OCT}, who stamps it 'OFFICIAL'","official"),
 (8,14,"a Hollywood-style seductive queen poster in Egyptian costume with a black wig" + OBJ.replace('no faces, ',''),"the seductress"),
 (8,15,"the same poster stamped 'EGYPTIAN?' with a red question mark" + OBJ.replace('no faces, ',''),""),
 (8,16,"a ruined Roman marble bust of a man with a crack across it" + OBJ.replace('no faces, ',''),"ruined Rome?"),
 (8,17,"a big red 'WRONG' stamp across the poster" + OBJ.replace('no faces, ',''),"nope"),
 (8,18,f"{C21} as a confident Greek queen standing over a map of the Mediterranean, surrounded by speech bubbles in many scripts and a stack of scrolls","21 years"),
 (8,19,"a sandy archaeological dig in Alexandria with an empty pit and a shovel; no people","tomb not found"),
 (8,20,f"{YOU} pointing at a big red subscribe-style button with a small diadem on top","subscribe"),
 (8,21,"two signs on poles: one with a laurel wreath 'genius', one with a snake 'villain'" + OBJ,"genius or villain?"),
 (8,22,f"{YOU} sitting on a stone with a wax tablet and a stylus, waiting","comments"),
]
NEG = " Anatomically correct people: every person has exactly two arms, two hands, two legs and five fingers per hand; no extra or floating limbs."
REF = {"CLEOPATRA at 21": "c21", "CLEOPATRA at 39": "c39", "JULIUS CAESAR": "caes", "MARK ANTONY": "ant", "OCTAVIAN (": "oct", "ROMAN POET (": "poet"}
CHAR = {}
import os
_j = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chars/jobs.txt")
if os.path.exists(_j): CHAR = {l.split()[0]: l.split()[1] for l in open(_j)}
def refs(i):
    d = SHOTS[i - 1][2]; return [v for k, v in REF.items() if k in d]
def prompt(i):
    p, l, d, n = SHOTS[i - 1]
    note = f" Handwritten marker note with ONE simple clean arrow (one smooth stroke, one arrowhead, no underline): '{n}'." if n else " No handwritten notes."
    if "stick figure" in d or "stick-figure" in d:
        note += " Stick figures = simple white round-headed stick figure with dot eyes, exactly two arms and two legs; it is the only stick figure."
    else: note += " No stick figures; all people drawn realistically."
    extra = " Only what is described: do not add extra people or objects."
    r = refs(i)
    if r: extra += " Reference images show the named people: draw each with exactly that face, hair and clothes, in the pose described."
    return STYLE + d + "." + note + extra + NEG
def request(i):
    m = [{"role": "image_references", "value": CHAR[r]} for r in refs(i) if r in CHAR]
    q = {"model": "gpt_image_2_6", "aspect_ratio": "16:9", "use_unlim": False, "prompt": prompt(i)}
    if m: q["medias"] = m
    return {"index": i, "params": q}
if __name__ == "__main__":
    print(len(SHOTS))
