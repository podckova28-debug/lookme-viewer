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
GEN = ("GENERAL BONAPARTE at 27 (as in reference image): thin, pale, hollow cheeks, long straight dark hair to the collar, dark-blue general's coat "
       "with gold oak-leaf embroidery, red-white-blue sash, white breeches, black boots, black bicorne hat worn sideways")
EMP = ("EMPEROR NAPOLEON at 36 (as in reference image): short dark-brown hair combed forward, clean-shaven, dark-green coat with red collar, "
       "white waistcoat and breeches, black boots, black bicorne hat worn sideways")
JOS = ("JOSEPHINE (as in reference image): elegant woman with dark-brown curly hair tied up with a ribbon, white high-waisted muslin dress, thin red shawl")
WELL = "the DUKE OF WELLINGTON (as in reference image): tall lean British general with a big hooked nose, dark-blue frock coat, plain black bicorne hat worn front-to-back"
OBJ0 = "; objects only: absolutely no people, no hands, no faces anywhere in the picture"
SHOTS += [
 # p2 — Revolution, Toulon, grapeshot
 (2,0,"a Paris crowd of 1789 in tricolour cockades storming the stone towers of the Bastille, smoke, waving hats","1789"),
 (2,1,"a royal crown rolling off a wooden platform, a dark storm cloud above; no people, no blood","1793"),
 (2,2,f"{CADET} arriving on a rocky Corsican beach, eagerly waving his bicorne at a group of local Corsican rebels who look at him suspiciously","Corsica"),
 (2,3,"angry Corsican villagers with pitchforks chasing a small group of people down a mountain path, comic dust cloud",""),
 (2,4,"a small crowded rowing boat at night leaving a rocky island, a family with bundles and a mother sitting upright, a burning house on the shore behind","1793 flee"),
 (2,5,"a poor family of refugees in 18th-century clothes standing on a quay in the French port of Marseille with a few bundles and a wooden trunk, looking lost","refugees"),
 (2,6,"a quill crossing out the handwritten name 'Napoleone di Buonaparte' on old paper with a thick line" + OBJ0,""),
 (2,7,"a quill writing a new elegant signature on old paper: 'Napoleon Bonaparte'" + OBJ0,""),
 (2,8,f"{GEN} admiring his new signature on a sheet of paper, proud","Bonaparte"),
 (2,9,"British warships with sails anchored in a French Mediterranean harbour with a stone fortress on a hill, 1793; no flags","Toulon 1793"),
 (2,10,f"{GEN} pointing at a map of a harbour on a table while two old generals in powdered wigs scratch their heads","captain, 24"),
 (2,11,"French artillerymen in blue coats firing bronze cannons from a hilltop down at British sailing ships in a harbour below, smoke","the hills"),
 (2,12,"British sailing warships hurriedly leaving a harbour with full sails, cannonballs splashing around them; no flags","it works"),
 (2,13,f"{GEN} as a new brigadier general, an older officer pinning a gold star on his coat",""),
 (2,14,f"{GEN} sitting on a straw mattress behind iron prison bars, arms crossed, annoyed","1794 prison"),
 (2,15,f"{GEN} walking out of an open prison door into sunlight, putting his bicorne back on","2 weeks"),
 (2,16,"an angry royalist crowd of 1795 Parisians with muskets and white flags of the Bourbons marching up a Paris street toward a church with steps","Oct 1795"),
 (2,17,f"{GEN} standing calmly next to a row of bronze cannons in a Paris street, arms crossed","grapeshot"),
 (2,18,"an empty Paris street with steps of a church, smoke drifting, hats and a dropped white flag lying on the cobblestones; no people","minutes"),
 (2,19,"five French politicians of 1795 in red cloaks and plumed hats applauding and bowing gratefully; visible from the waist up",""),
 (2,20,"elegant Paris ladies and gentlemen of 1795 at a glittering salon party, fans and glasses, all turning their heads curiously toward a door","Paris society"),
 # p3 — Josephine and Italy
 (3,0,f"{GEN} at a candle-lit Paris salon, frozen and staring, while {JOS} smiles at him across the room holding a fan","1795"),
 (3,1,f"{JOS} smiling sweetly while a pile of unpaid bills falls out of her little silk purse","6 years older, in debt"),
 (3,2,f"{GEN} with cartoon hearts floating around his head, dreamy face",""),
 (3,3,f"a name card reading 'Rose' crossed out, and next to it a new name card reading 'Josephine' with a heart" + OBJ0,"Rose → Josephine"),
 (3,4,f"{GEN} and {JOS} signing a marriage register at a simple wooden table in a plain Paris town hall office, a clerk watching","March 1796"),
 (3,5,f"{GEN} galloping away on a horse, waving his bicorne back at {JOS} who stands in a doorway","2 days later"),
 (3,6,"a line of ragged hungry French soldiers of 1796 in torn blue coats, some barefoot, one eating a crust of bread, mountains behind",""),
 (3,7,"a hand-drawn map of northern Italy with French blue arrows pushing white Austrian arrows back again and again" + OBJ0,"1796–97"),
 (3,8,"French soldiers in blue coats charging across a long wooden bridge over a river at Lodi, Austrian soldiers in white coats retreating, smoke","Lodi"),
 (3,9,f"{GEN} holding a tricolour flag and leading soldiers onto a narrow bridge over marshes, smoke","Arcole"),
 (3,10,"French infantry in blue coats on a snowy mountain plateau firing at Austrian soldiers in white coats below, January 1797","Rivoli"),
 (3,11,"wagons loaded with gold coins, framed paintings and white marble statues rolling over the Alps toward France" + OBJ0,"loot"),
 (3,12,f"{GEN} at a camp table by candlelight writing a love letter with a quill, a tall stack of sealed letters beside him",""),
 (3,13,f"{JOS} lounging on a sofa ignoring a big pile of unopened letters, a cartoon cobweb on the pile","barely"),
 (3,14,f"{JOS} laughing on a sofa with a handsome young hussar officer with a curled moustache and a fancy fur-trimmed jacket; visible from the waist up","Hippolyte Charles"),
 (3,15,f"{GILL} looking up from a newspaper with a sly grin, a quill in his other hand","London"),
 (3,16,f"{GILL} dipping a quill into an inkpot, thinking, a small sparkle of an idea above his head",""),
 (3,17,"a sheet of paper on a drawing desk with a caricature of a tiny furious French general in a huge bicorne hat, handwritten title 'Little Boney'" + OBJ0,"Little Boney"),
 (3,18,"three caricature sketches pinned side by side, each showing the same French general in a bicorne smaller than the last, the third one tiny as a mouse" + OBJ0,"smaller..."),
 # p4 — Egypt and the coup
 (4,0,"a large French fleet of 1798 sailing across the Mediterranean, a dotted arrow on a small map inset going from France to Egypt and on toward India; no flags","1798 Egypt"),
 (4,1,"French soldiers in blue coats and white trousers marching off ships onto a sunny Egyptian beach with palm trees",""),
 (4,2,"a group of 18th-century French scientists in tailcoats stepping off a boat with telescopes, sketchbooks, measuring tapes and boxes of instruments","150+ scientists"),
 (4,3,"French infantry squares in blue coats firing at charging Mamluk horsemen in turbans and colourful robes, the Giza pyramids in the background","Pyramids 1798"),
 (4,4,"British sailing warships attacking French ships at night in a bay, one French ship exploding in a huge orange fireball; no flags","Battle of the Nile"),
 (4,5,f"{GEN} standing on an Egyptian beach looking at burning shipwrecks on the sea, hands on hips, a camel looking at him","stuck"),
 (4,6,"French scientists in tailcoats measuring a sphinx with a tape measure, sketching temple columns, and carrying a crate labelled 'FRAGILE' away from a temple","everything"),
 (4,7,"French soldiers in blue coats digging in rubble near an old fort and uncovering a dark grey stone slab covered with three bands of carved writing","Rosetta 1799"),
 (4,8,"close-up of the Rosetta Stone: dark granite slab with three bands of carved text, hieroglyphs on top, a magnifying glass over it" + OBJ0,"3 scripts"),
 (4,9,"the Rosetta Stone in a glass case in a museum gallery with classical columns; no people","British Museum"),
 (4,10,"a messenger on horseback galloping across the desert sand toward a French army tent, holding a letter",""),
 (4,11,"a cartoon map of Europe with arrows of enemy armies pressing on France, a small French government building with cracks in it" + OBJ0,"losing"),
 (4,12,f"{GEN} in a tent by lamplight, looking at the letter, a sly determined look",""),
 (4,13,"a small fast sailing frigate slipping away at night from the Egyptian coast, a few lights, the moon; no flags","Aug 1799"),
 (4,14,"French grenadiers in bearskin hats marching into a grand hall with columns, 1799","Nov 1799 coup"),
 (4,15,"a big hand-drawn 'OOPS' stamp in red ink on old paper" + OBJ0,""),
 (4,16,f"{GEN} being shoved and shouted at by angry deputies in red togas in a parliament hall, grenadiers in bearskin hats pushing through to rescue him",""),
 (4,17,f"{GEN} standing in front of three chairs, sitting down in the biggest middle chair, smug","First Consul"),
 (4,18,"a birthday cake with thirty candles and a tiny bicorne hat on top" + OBJ0,"age 30"),
 # p5 — Emperor
 (5,0,f"{EMP} rolling up his sleeves at a big desk covered with papers",""),
 (5,1,"a grand 1800 Paris bank building with columns, bags of coins and stacks of banknotes in front" + OBJ0,"Bank of France 1800"),
 (5,2,"a classroom of 1800s schoolboys in uniform sitting at wooden desks, a teacher at a blackboard","schools"),
 (5,3,"a straight new road lined with trees running across the French countryside toward the horizon, a mail coach on it",""),
 (5,4,"a thick leather-bound book 'Code Civil des Français' on a lectern, glowing softly" + OBJ0,"Civil Code 1804"),
 (5,5,"a world map with small copies of the same law book appearing in many countries" + OBJ0,"still today"),
 (5,6,f"{EMP} looking at the small 'First Consul' sign on his door and shaking his head",""),
 (5,7,"inside Notre-Dame cathedral 1804, the old pope Pius VII in white robes and a tall mitre seated by the altar, a crowd in court dress","2 Dec 1804"),
 (5,8,f"{EMP} in red velvet imperial robes and a golden laurel wreath, lifting a crown with both hands onto his own head, the pope sitting behind him looking surprised",""),
 (5,9,f"{EMP} in imperial robes placing a small crown on the head of {JOS} who kneels before him in a white gown",""),
 (5,10,"a huge painting of a coronation ceremony in a golden frame hanging in a museum gallery, a tiny museum guard in a peaked cap standing next to it for scale","10 m wide"),
 (5,11,"LETIZIA BUONAPARTE, a stern Corsican mother in a dark dress, at home in an armchair, knitting and rolling her eyes","stayed home"),
 (5,12,"British sailing warships breaking through a line of French ships at sea, cannon smoke, a French ship's mast falling; no flags","Trafalgar 1805"),
 (5,13,f"{EMP} on a cliff looking across the sea at the white cliffs of England through a telescope, sighing","no invasion"),
 (5,14,f"{EMP} on a white horse on a hill watching his army in a misty valley at sunrise, French soldiers charging up a plateau","Austerlitz 1805"),
 (5,15,f"{GILL} at his desk drawing a caricature of a tiny Napoleon and a tall British statesman carving a huge round globe like a pudding with knives and forks","plum pudding"),
 (5,16,"close-up of the caricature on paper: a tiny Napoleon in a huge bicorne standing on a chair to reach a globe-shaped pudding" + OBJ0,"still tiny"),
 (5,17,"a map of Europe in 1810 with most countries shaded French blue and small golden crowns on several capitals" + OBJ0,"1810"),
 (5,18,f"{EMP} pacing in a palace room, hands behind his back, frowning",""),
 (5,19,"an empty ornate baby cradle with a tiny imperial crown hanging above it, in a palace room" + OBJ0,"no heir"),
 # p6 — Marie-Louise and Russia
 (6,0,f"{JOS} sitting sadly by a window in a palace room, holding a handkerchief",""),
 (6,1,f"{EMP} and {JOS} in a palace hall reading a divorce document, she wipes a tear, he looks away","1810 divorce"),
 (6,2,f"{EMP} at a wedding with a young blonde 18-year-old Austrian archduchess in a white satin gown with a diamond tiara","Marie-Louise"),
 (6,3,"FRANCIS I of Austria, a thin long-faced man in a white uniform, smiling awkwardly through clenched teeth at a wedding; visible from the chest up","beaten twice"),
 (6,4,"a royal baby in an ornate cradle under a canopy with golden bees, 1811","1811"),
 (6,5,"the same royal baby wearing a tiny crown and holding a tiny sceptre, sitting on a velvet cushion, looking confused","King of Rome"),
 (6,6,"a big hand-drawn red warning sign with an exclamation mark on old paper" + OBJ0,"big mistake"),
 (6,7,"an enormous French army of 1812 in blue coats crossing a river on pontoon bridges into a vast flat land of forests and fields","June 1812, ~600,000"),
 (6,8,"empty Russian plains with a few birch trees, no soldiers in sight, French scouts on horses looking around confused","where are they?"),
 (6,9,"Russian villages and wheat fields burning behind a retreating column of Russian soldiers in green coats",""),
 (6,10,"a huge battle on a wide field with smoke, cannons and cavalry, a church on a hill, September 1812","Borodino"),
 (6,11,f"{EMP} riding a white horse through the gate of a deserted Russian city with onion domes and the Kremlin walls","Moscow"),
 (6,12,"empty Moscow streets with onion-domed churches and wooden houses, not a single person, a cat on a fence","empty"),
 (6,13,"Moscow burning at night, huge orange flames over the onion domes and the Kremlin walls" + OBJ0,""),
 (6,14,f"{EMP} sitting in a Kremlin room tapping his fingers on a table, staring at a clock",""),
 (6,15,"a messenger's tray with no letter on it, a cartoon cricket chirping next to it" + OBJ0,"silence"),
 (6,16,"a long column of French soldiers in blue coats and wagons leaving the smoking city of Moscow on a muddy road in autumn","Oct 1812"),
 (6,17,"the first snowflakes falling on a long column of marching French soldiers, a sky turning grey",""),
 (6,18,"French soldiers wrapped in blankets trudging through a blizzard past abandoned cannons, Cossack horsemen with lances in the distance","winter"),
 (6,19,"a few frozen French soldiers crossing back over a river bridge in the snow, five little soldier icons drawn in the corner with four of them crossed out","< 1 in 5"),
 # p7 — Leipzig, Elba, Waterloo
 (7,0,"cartoon armies of Russia, Prussia, Austria and Britain in different uniforms all marching from different directions toward one small French soldier; no flags",""),
 (7,1,"a huge battle around a German city with church towers, smoke and many soldiers, October 1813","Leipzig 1813"),
 (7,2,f"{EMP} riding away from the battle on his horse, head down",""),
 (7,3,f"{EMP} at a desk in a palace signing a document with a quill, a crown lying on its side next to him","April 1814"),
 (7,4,"a small rocky Mediterranean island with a little harbour town and a fort, off the coast of Italy","Elba"),
 (7,5,f"{EMP} wearing a very big crown that slips over his eyes, standing on a tiny rocky island","still 'emperor'"),
 (7,6,"a little wooden sign on a pole on a rocky beach that says 'EMPIRE' with an arrow pointing to a small fishing village" + OBJ0,"Emperor of Elba"),
 (7,7,f"{EMP} inspecting a row of goats standing in line like soldiers on a hillside","12,000 people + goats"),
 (7,8,"a wall calendar with ten pages torn off and lying on the floor" + OBJ0,"10 months"),
 (7,9,"a small sailing ship at night slipping away from an island, then landing at a sunny southern French beach with a few hundred soldiers","Feb 1815"),
 (7,10,"a regiment of French soldiers in blue coats with muskets blocking a road in the hills, officers looking nervous","the king's army"),
 (7,11,f"{EMP} standing alone in front of a line of soldiers with muskets, holding his coat open with both hands, chin up","here I am"),
 (7,12,"French soldiers throwing their hats in the air and cheering, some running forward with arms open",""),
 (7,13,"a royal carriage racing away from Paris at night, luggage falling off the roof","20 March 1815"),
 (7,14,"armies of Britain, Prussia, Austria and Russia marching together in a long column toward France; no flags","everyone"),
 (7,15,f"{WELL} on a horse on a ridge, looking through a telescope at a field with farmhouses, red-coated British infantry in squares below","Waterloo, 18 June 1815"),
 (7,16,"Prussian soldiers in dark-blue coats and black shakos pouring out of a forest onto a battlefield at evening","the Prussians"),
 (7,17,f"{EMP} standing alone on a battlefield at sunset, smoke and fallen cannons around, head bowed","over"),
 (7,18,f"{EMP} climbing aboard a British warship and handing his sword to a British naval captain in a blue coat","July 1815"),
 (7,19,"a tiny steep volcanic island in the middle of a vast ocean seen from far away, a single ship near it","St Helena"),
 (7,20,f"{YOU} on the deck of a ship, waving at the viewer","you again"),
 # p8 — St Helena, death, the height
 (8,0,f"{NAP46} in a straw hat working in a small garden at a damp farmhouse, holding a watering can, a rat watching from a fence","St Helena"),
 (8,1,f"{NAP46} arguing at a table with HUDSON LOWE, a thin red-haired British governor in a red uniform, both pointing at papers","Hudson Lowe"),
 (8,2,"an envelope with a wax seal addressed in big handwriting 'General Bonaparte'" + OBJ0,""),
 (8,3,f"{NAP46} sitting in an armchair, arms crossed, refusing to open a letter lying on the table, nose in the air","Emperor only"),
 (8,4,"a single candle on a bedside table being blown out by a breath of wind, a small window with rain; no people","5 May 1821"),
 (8,5,"a small bicorne hat resting on a pillow, a sprig of willow beside it" + OBJ0,"age 51"),
 (8,6,"a 19th-century doctor's notebook open on a table with a quill and spectacles, a simple anatomical stomach sketch" + OBJ0,"stomach cancer"),
 (8,7,"a strip of old green patterned wallpaper next to a glass test tube and a lock of dark hair in an envelope" + OBJ0,"arsenic?"),
 (8,8,"two modern historians in suits arguing over a book, pointing at different pages; visible from the waist up","still arguing"),
 (8,9,"a 19th-century tape measure laid out on a white sheet next to a notebook and a quill" + OBJ0,""),
 (8,10,"a handwritten note on old paper: '5 pieds 2 pouces'" + OBJ0,"5 ft 2?"),
 (8,11,"a small ruler marked 'pied' and 'pouce' lying next to a longer English ruler marked 'inch'; the French ruler units are visibly bigger" + OBJ0,"French units"),
 (8,12,"two simple height charts side by side on paper, a red line at the same height on both, labelled 'pieds' on one and 'feet' on the other" + OBJ0,"≈ 5 ft 6"),
 (8,13,f"{NAP46} standing between two ordinary men of the same height, all three shrugging",""),
 (8,14,"a British newspaper of 1821 lying on a table with a big headline 'Little Boney 5 FT 2'" + OBJ0,"the legend"),
 (8,15,f"{GILL}'s empty slanted drawing desk with his spectacles, a quill and a cold inkpot left on it, a small black ribbon; no people","June 1815"),
 (8,16,"an unfinished caricature on a drawing desk, the last panel blank" + OBJ0,""),
 (8,17,"a tiny cartoon Napoleon in a huge bicorne hat stepping out of a sheet of paper and winking" + OBJ0,""),
 (8,18,"many modern books, posters and mugs with a tiny cartoon Napoleon in a huge bicorne on them" + OBJ0,"outlived them both"),
 (8,19,"the golden dome of Les Invalides in Paris, and inside, a huge red stone tomb in a round open crypt, seen from the balcony above" + OBJ0,"1840 Paris"),
 (8,20,"a tiny modern tourist stick figure leaning over a balustrade looking down at a huge red tomb in a round crypt; the stick figure is a simple white round-headed stick figure with dot eyes","look down"),
 (8,21,f"{YOU} pointing at a big red subscribe-style button with a bicorne hat on top","subscribe"),
 (8,22,"two speech-bubble signs on poles on white: one with a laurel wreath, one with a broken crown" + OBJ0,"hero or tyrant?"),
 (8,23,f"{YOU} sitting on a cannon, holding a quill and an empty sheet of paper, waiting","comments"),
]
NEG = " Anatomically correct people: every person has exactly two arms, two hands and five fingers per hand; no extra or floating limbs."
REF = {"NAPOLEON at 46": "nap46", "GENERAL BONAPARTE at 27": "gen", "EMPEROR NAPOLEON at 36": "emp", "JOSEPHINE (": "jos", "DUKE OF WELLINGTON": "well", "NAPOLEONE as a thin serious 9": "boy", "NAPOLEONE as a thin serious teen": "cadet", "JAMES GILLRAY": "gill"}
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
FIX[77] = (f"{JOS} fully dressed, sitting at a small card table in a Paris salon playing cards with a dashing young hussar officer with a curled moustache "
           "in a blue fur-trimmed jacket, both laughing; a table between them")
SHOTS[76] = SHOTS[76][:2] + (FIX[77],) + SHOTS[76][3:]
# wave 4: per-frame review of 45-188 (factual / logic errors only; credits limited)
NOFLAG = " Absolutely no flags or banners anywhere."
FIX6 = {
45: "a Paris crowd of 1789 with small red-white-blue cockades on their hats storming the stone towers of the Bastille, smoke, waving hats and pikes" + NOFLAG,
49: "a small crowded rowing boat at night leaving a rocky island: a worried widowed mother in a dark dress and shawl with several teenage children holding bundles, no adult men, anxious faces, a burning house on the shore behind",
50: "a poor widowed mother in a dark dress with several teenage children, no adult men, standing on a stone quay in the French port of Marseille with a few bundles and a wooden trunk, looking lost",
56: "British wooden warships with sails anchored in a French Mediterranean harbour with a stone fortress on a hill, 1793; no people" + NOFLAG,
73: "a hand-drawn map of northern Italy with thick French-blue arrows pushing white arrows back again and again" + OBJ0 + "; no flags, no words, no labels on the map",
81: f"{GILL} looking up from a folded newspaper with no readable text, a sly grin, holding a single feather quill in his other hand",
82: "a blank sheet of paper on a slanted drawing desk next to an inkpot and a feather quill" + OBJ0,
85: "a large French fleet of 1798 sailing across the Mediterranean, with a small map inset showing a dotted arrow from the south of France across the sea to Egypt" + OBJ0 + NOFLAG,
98: "a small fast sailing frigate slipping away at night from a flat sandy Egyptian coast with a few palm trees, the moon above; no pyramids, no people" + NOFLAG,
103: "a birthday cake with two big number candles '3' and '0' on top, lit, and a tiny bicorne hat beside them" + OBJ0,
109: "a world map where small copies of the same leather law book stand only on France, Belgium, the Netherlands, Italy, Spain, Portugal, Latin America, Louisiana and Quebec; nothing on other countries" + OBJ0 + "; no text",
112: f"{EMP} without any hat, in red velvet imperial robes with ermine, lifting a golden laurel wreath with both hands onto his own bare head, the old pope in white robes sitting behind him looking surprised",
113: f"{EMP} without any hat, in red velvet imperial robes and a golden laurel wreath on his head, placing a small crown on the head of {JOS} who kneels before him in a white satin coronation gown",
121: "a map of Europe in 1810 with most countries shaded French blue and small golden crowns on several capitals" + OBJ0 + "; absolutely no words or labels on the map",
132: "an enormous French army of 1812 in blue coats crossing a river on pontoon bridges into a vast flat summer land of green fields and forests under a hot sun, no snow" + NOFLAG,
133: "empty Russian plains in hot summer with dry yellow grass and a few birch trees, no soldiers in sight, two French scouts on horses looking around confused; no snow",
135: "empty Moscow streets in early autumn with onion-domed churches and wooden houses, not a single person, a cat on a fence, no snow; the Kremlin towers have plain spires with no stars",
136: "Moscow burning at night, huge orange flames over the onion domes and the Kremlin walls; the Kremlin towers have plain spires with no stars on top" + OBJ0,
137: f"{EMP} sitting in a Kremlin room with a vaulted painted ceiling, tapping his fingers on a table, staring at a clock; no window views",
138: "a long column of French soldiers in blue coats and wagons leaving the smoking city of Moscow on a muddy autumn road, brown leaves, no snow yet; no stars on any tower",
144: "Prussian soldiers of 1813 in dark-blue coats and plain black cylindrical shakos (no spikes, no spiked helmets) standing with Austrian soldiers in white coats, a huge battle with smoke around a German town with church towers" + NOFLAG,
148: "a small rocky Mediterranean island with a little harbour town, fishing boats and a stone fort, off the coast of Italy; no people",
152: "a wall calendar with ten blank torn-off pages lying on the floor, no month names, no symbols" + OBJ0,
154: "a regiment of French royal soldiers of 1815 in dark-blue coats and tall black shakos with white cockades, muskets, blocking a road in the hills, two officers in shakos looking nervous",
157: "a royal carriage racing away from Paris at night with luggage falling off the roof, curtains drawn so nobody inside is visible, a coachman seen only from behind",
158: "armies of 1815 marching together in a long column: British infantry in red coats and shakos, Prussians in dark-blue coats and plain black shakos without spikes, Austrians in white coats, Russians in green coats; serious faces" + NOFLAG,
162: f"{EMP} climbing a rope ladder onto a British wooden warship, a British naval captain in a blue coat and bicorne saluting him politely at the rail; no sword being handed over",
165: f"{NAP46} without the bicorne, wearing only a wide straw gardening hat, working in a small garden at a damp farmhouse, holding a watering can, a rat watching from a fence",
169: "a single candle on a bedside table just blown out, a thin curl of smoke rising, a small window with rain behind; no faces, no people" ,
176: "two rulers side by side on white: a French ruler marked 'pouce' with each unit clearly LONGER, and an English ruler marked 'inch' with each unit visibly shorter; the 'pouce' marks are spaced wider than the 'inch' marks" + OBJ0,
179: "a British newspaper of 1821 lying on a table with a big headline 'Little Boney 5 FT 2' and a small engraving of an island; no date line" + OBJ0,
180: "an empty slanted drawing desk with a pair of round spectacles, a feather quill and a cold inkpot left on it, a small black mourning ribbon on the corner; no people",
181: "an unfinished caricature on a drawing desk: three small panels each showing a tiny Napoleon in a huge bicorne hat stamping his feet, and the fourth panel left completely blank" + OBJ0,
}
for _k, _d in FIX6.items(): SHOTS[_k - 1] = SHOTS[_k - 1][:2] + (_d,) + SHOTS[_k - 1][3:]
# Kremlin in 1812: walls and towers WHITEWASHED (white), golden double-headed eagles on the tower spires, no Grand Kremlin Palace (built 1838-49)
KREM = ("the Moscow Kremlin as it looked in 1812: WHITE whitewashed walls and white towers with green tent roofs topped by small golden double-headed eagles, "
        "golden domes of the cathedrals inside; NO red brick, NO stars, NO large yellow-and-white palace")
FIX7 = {
135: f"{EMP} riding a white horse through an open gate of {KREM}, the street around him empty, early autumn",
136: f"empty Moscow streets in early autumn with wooden houses and onion-domed churches, not a single person, a cat on a fence, in the background {KREM}",
137: f"Moscow burning at night: huge orange flames and smoke over wooden houses and onion domes, in the middle {KREM}" + OBJ0,
140: f"a long column of French soldiers in blue coats and wagons leaving Moscow on a muddy autumn road, brown leaves, no snow; in the far background smoke rising over {KREM}",
}
for _k, _d in FIX7.items(): SHOTS[_k - 1] = SHOTS[_k - 1][:2] + (_d,) + SHOTS[_k - 1][3:]
