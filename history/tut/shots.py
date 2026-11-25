# Tutankhamun storyboard: (part, line, frac, description, location). A frame starts at `frac` of the narration line.
# Every recurring person is named "<Name> (as in the sheet)" and gets his single-person reference image (PREF).
# LOCATIONS: every shot of one place is drawn with that place's anchor frame as a reference, so walls, doors, light and props match.
# c00 reuses the approved cold-open test frames (REUSE fNNN).
import re
TUT9, TUT17 = "Tutankhaten age 9 (as in the sheet)", "Tutankhamun age 18 (as in the sheet)"
ANKH13, ANKH20 = "Ankhesenamun age 13 (as in the sheet)", "Ankhesenamun age 20 (as in the sheet)"
AKH, AY, HOR, CAR, CARN = ("%s (as in the sheet)" % n for n in ("Akhenaten", "Ay", "Horemheb", "Howard Carter", "Lord Carnarvon"))
S = [
 # c00 cold open (approved test frames)
 ("c00",0,0,"REUSE f001",None), ("c00",1,0,"REUSE f002",None), ("c00",2,0,"REUSE f003",None), ("c00",2,.55,"REUSE f004",None),
 ("c00",3,0,"REUSE f005",None), ("c00",4,0,"REUSE f006",None), ("c00",5,0,"REUSE f007",None), ("c00",6,0,"REUSE f008",None),
 ("c00",7,0,"REUSE f009",None), ("c00",8,0,"REUSE f010",None), ("c00",9,0,"REUSE f011",None),
 # c01 the sun disk
 ("c01",0,0,"bird's-eye view of a brand new white city on the east bank of the Nile in the desert around 1341 BC: white mud-brick palaces and open-air temples without roofs, wide straight streets, green fields along the river, cliffs behind","AMARNA_CITY"),
 ("c01",0,.6,"a simple illustrated map of ancient Egypt: the Nile from the delta down to Thebes, a small gold star in the middle of the river at Amarna, desert in ochre, sea in blue, no labels","MAP"),
 ("c01",1,0,f"a royal nursery in a sunlit palace room: a newborn baby in white linen in the arms of a nurse in a white dress, a carved relief of the sun disk with long rays ending in little hands on the wall behind","AMARNA_PALACE"),
 ("c01",2,0,f"{AKH} standing on a palace balcony raising both arms to the sun","AMARNA_PALACE"),
 ("c01",3,0,f"close-up portrait of {AKH} with his long narrow face, staring calmly, the sun disk behind his head","AMARNA_PALACE"),
 ("c01",4,0,"in a dim old temple of Amun at Thebes, painted statues of the gods Amun (blue skin, tall double-feather crown) and Osiris (green skin, white crown) being covered with cloth by workers, dust in the light","THEBES_TEMPLE"),
 ("c01",4,.6,"a huge open-air sun temple without a roof, hundreds of stone offering tables in rows under the blazing sun disk, priests in white","AMARNA_TEMPLE"),
 ("c01",5,0,"the great doors of an old temple at Thebes being shut and barred, priests with shaved heads in white robes walking away carrying scrolls, sad faces","THEBES_TEMPLE"),
 ("c01",6,0,"a small prince of 5 with a shaved head and one braided sidelock, white linen kilt, playing with a wooden toy horse in a sunlit palace courtyard with papyrus columns, painted floor of reeds and ducks","AMARNA_PALACE"),
 ("c01",6,.5,"a carved limestone relief: the royal family under the sun disk whose long rays end in little hands, the parents holding small children on their laps, Amarna art style","AMARNA_PALACE"),
 ("c01",7,0,"a modern laboratory: a scientist in a white coat looking at DNA bands on a computer screen beside an old mummy x-ray, no body shown","LAB"),
 ("c01",8,0,"a royal funeral procession at Amarna leaving the white city toward the desert cliffs, mourning women in white with raised arms, a gilded coffin on a sledge pulled by oxen","AMARNA_CITY"),
 ("c01",9,0,"a small prince of 6 with a shaved head and one braided sidelock, white linen kilt, standing alone in a large empty sunlit throne hall, looking up at an empty gold throne","AMARNA_PALACE"),
 # c02 the crook
 ("c02",0,0,f"{TUT9} sitting on a big golden throne far too large for him, his feet not touching the floor, in a dim throne hall with painted columns","THRONE_HALL"),
 ("c02",1,0,"close-up of small hands holding the royal crook and flail crossed over a boy's chest, the crook striped gold and dark blue, the flail with beaded strands","THRONE_HALL"),
 ("c02",1,.45,f"{ANKH13} standing next to {TUT9}, both in front of the throne, a priest joining their hands","THRONE_HALL"),
 ("c02",1,.8,"a painted limestone portrait bust of queen Nefertiti on a plinth in a sculptor's workshop, tall flat-topped blue crown, one eye unfinished","AMARNA_PALACE"),
 ("c02",2,0,f"{ANKH13} smiling shyly down at {TUT9} who is a head shorter than her","THRONE_HALL"),
 ("c02",3,0,f"{TUT9} on the throne looking lost while a crowd of officials bow and present scrolls","THRONE_HALL"),
 ("c02",4,0,f"{AY} and {HOR} standing behind the throne of {TUT9} in the throne hall, both looking down at the boy","THRONE_HALL"),
 ("c02",5,0,f"close-up of {AY} with a calm cunning look, holding a long staff","THRONE_HALL"),
 ("c02",5,.55,f"close-up of {HOR} in front of rows of Egyptian soldiers with spears and shields","ARMY_CAMP"),
 ("c02",6,0,f"{AY} and {HOR} whispering together over a papyrus map on a table, lit by an oil lamp in a clay dish","COUNCIL_ROOM"),
 ("c02",7,0,"an angry crowd of ordinary Egyptians in plain linen shouting in a dusty street of Thebes, fists raised, mud-brick houses","THEBES_STREET"),
 ("c02",8,0,"a sad old priest with a shaved head in a white robe sitting on the steps of a closed temple, weeds growing between the stones","THEBES_TEMPLE"),
 ("c02",9,0,f"{TUT9} looking at a stone relief of the sun disk with rays ending in hands, a crack running across it","AMARNA_PALACE"),
 # c03 the stela
 ("c03",0,0,f"{TUT9} on the throne as a scribe kneels in front of him writing on papyrus with a reed pen","THRONE_HALL"),
 ("c03",1,0,"close-up of a stone carver chiselling a royal cartouche on a wall, the old sun-disk sign being replaced by a seated figure of the god Amun, bronze chisel and wooden mallet","WORKSHOP"),
 ("c03",2,0,f"{ANKH13} looking at her reflection in a polished bronze mirror","THRONE_HALL"),
 ("c03",3,0,"the white city of Amarna empty and abandoned, sand blowing through open doorways and empty streets, a single palm tree","AMARNA_CITY"),
 ("c03",3,.5,"a long line of royal boats with square sails sailing south on the Nile, carrying furniture and statues away","NILE"),
 ("c03",4,0,"the huge temple of Karnak at Thebes with giant papyrus columns and obelisks, crowds of priests returning","KARNAK"),
 ("c03",4,.5,f"{TUT9} standing beside a tall rounded-top stone slab (stela) carved with figures of the king offering to the god Amun and rows of hieroglyphs, at Karnak","KARNAK"),
 ("c03",5,0,"a ruined Egyptian temple with fallen columns and weeds, then workmen rebuilding it with fresh stone blocks and ropes","KARNAK"),
 ("c03",5,.6,"goldsmiths in a workshop casting a gold statue of the god Amun, glowing crucible, bronze tools","WORKSHOP"),
 ("c03",6,0,f"{AY} dictating to a scribe while {TUT9} sits bored, swinging his legs","COUNCIL_ROOM"),
 ("c03",7,0,"priests in white robes carrying a gilded statue of the god Amun in a boat-shaped shrine on poles out of the temple, crowd cheering","KARNAK"),
 ("c03",8,0,"incense smoke rising in front of a restored statue of the god Amun with tall double feathers, oil lamps in clay dishes, crowd kneeling","KARNAK"),
 ("c03",9,0,"a stone relief of the pharaoh Akhenaten's face being hacked out by a chisel, dust flying, the rest of the wall untouched","KARNAK"),
 # c04 the cane
 ("c04",0,0,f"a painted wooden chest panel showing {TUT17} in a chariot shooting arrows at lions, idealised heroic Egyptian painting style","TOMB_ART"),
 ("c04",0,.55,f"a gilded statue of {TUT17} as a perfect young god standing on a black panther","TOMB_ART"),
 ("c04",1,0,f"{TUT17} slim and frail, leaning on a wooden walking stick in a palace corridor, a slight limp, looking tired","THRONE_HALL"),
 ("c04",2,0,"a modern hospital CT scanner room with a sealed wooden box going into the scanner, technicians in blue looking at screens showing a skeleton foot, no body visible","LAB"),
 ("c04",2,.6,"a magnified microscope view of tiny ring-shaped malaria parasites in red blood cells, a mosquito silhouette in the corner","LAB"),
 ("c04",3,0,"dozens of ancient Egyptian walking sticks laid out in rows on a museum table: gold, ebony, ivory, carved wood, some worn at the handle","MUSEUM"),
 ("c04",4,0,f"{TUT17} sitting on a chair to shoot arrows from a seated position, his walking stick leaning beside him, papyrus marsh","NILE"),
 ("c04",5,0,f"{TUT17} and {ANKH20} sitting together in a quiet garden by a pool, she rests her hand on his shoulder","PALACE_GARDEN"),
 ("c04",6,0,"two tiny gilded wooden coffins side by side in a dark tomb corner, lit by a single oil lamp in a clay dish","TOMB_ANTECHAMBER_ANCIENT"),
 ("c04",7,0,f"{TUT17} and {ANKH20} standing on a palace balcony at sunset, looking at the Nile, their long shadows","PALACE_GARDEN"),
 ("c04",8,0,f"{TUT17} standing straight in front of the throne, holding the crook and flail, determined, no cane in his hands, the cane leaning on the throne","THRONE_HALL"),
 ("c04",9,0,"a row of small comic portrait medallions of famous historical figures (a Russian monk with a black beard, a Japanese swordsman, a French girl in armour, a Mongol khan) on a dark background","CTA"),
 ("c04",10,0,"a big red play button with a hand pressing a subscribe bell, comic style, dark background","CTA"),
 ("c04",11,0,f"close-up of {TUT17} in shadow, an hourglass with sand running out on the table beside him","THRONE_HALL"),
 # c05 the chariot
 ("c05",0,0,f"a dark palace bedroom at night, an empty bed with crumpled linen, an oil lamp in a clay dish gone out, a crook and flail lying on a stool","PALACE_BEDROOM"),
 ("c05",1,0,"an Egyptian scribe holding a blank papyrus scroll, puzzled, reed pen in hand","COUNCIL_ROOM"),
 ("c05",2,0,"a black-and-white 1968 x-ray film of a human skull on a lightbox, with a small bright fragment inside, a doctor in a 1960s suit pointing at it","LAB"),
 ("c05",3,0,"a modern CT scanner in a tent in the Valley of the Kings at night in 2005, scientists looking at 3D scans of a skeleton on laptops, no body visible","LAB"),
 ("c05",4,0,"a 3D computer reconstruction on a screen of a broken left thigh bone near the knee, a red circle around the break","LAB"),
 ("c05",5,0,f"an ancient Egyptian chariot overturned on its side in the desert, one wheel still spinning, a startled horse running away, dust cloud, no person visible","DESERT"),
 ("c05",6,0,f"{TUT17} lying in bed with a bandaged left leg, sweating with fever, a physician with a shaved head mixing medicine in a bowl","PALACE_BEDROOM"),
 ("c05",7,0,"two modern scientists in a museum arguing in front of a wall of scan images and papers","MUSEUM"),
 ("c05",8,0,"an empty golden throne in the dark throne hall, a single beam of light falling on it","THRONE_HALL"),
 ("c05",9,0,"Egyptian courtiers and generals arguing loudly around the empty throne","THRONE_HALL"),
 ("c05",10,0,f"{ANKH20} as a young widow in white mourning clothes, alone, writing a letter by an oil lamp in a clay dish at night, determined face","PALACE_BEDROOM"),
 # c06 the letter
 ("c06",0,0,"a simple illustrated map of the ancient Near East: Egypt in the south, the Hittite kingdom in Anatolia in the north, a dotted route of a messenger between them, no labels","MAP"),
 ("c06",0,.5,"Suppiluliuma, the Hittite king (a heavy older man with a long dark beard, tall conical white cap, long blue robe with fringe, hooked shoes), on a stone throne in a grey stone hall with carved lions, receiving a clay tablet from a kneeling messenger","HITTITE_HALL"),
 ("c06",1,0,f"close-up of {ANKH20} in white mourning clothes pressing a seal onto a letter, tears in her eyes","PALACE_BEDROOM"),
 ("c06",2,0,"close-up of a clay tablet with dense wedge-shaped cuneiform writing, no readable letters","HITTITE_HALL"),
 ("c06",3,0,f"{ANKH20} in white mourning clothes looking out of a palace window at night toward the north, the Nile below","PALACE_BEDROOM"),
 ("c06",4,0,"Suppiluliuma (as in the anchor) reading the clay tablet with raised eyebrows, astonished","HITTITE_HALL"),
 ("c06",5,0,f"{ANKH20} in white mourning clothes turning away from {AY} who reaches out his hand to her in the throne hall, she refuses","THRONE_HALL"),
 ("c06",6,0,"Suppiluliuma (as in the anchor) laughing in disbelief with his advisers in the grey stone hall","HITTITE_HALL"),
 ("c06",7,0,"a Hittite envoy in a pointed cap and fringed robe riding in a chariot through the desert toward Egypt","DESERT"),
 ("c06",8,0,"the young Hittite prince Zannanza (age 20, slim, long black hair, pointed cap, short fringed tunic) saying goodbye to his father Suppiluliuma (as in the anchor) at a stone city gate guarded by carved lions","HITTITE_HALL"),
 ("c06",9,0,"an empty Hittite chariot standing in the desert at dusk, its horses gone, arrows stuck in the sand, no bodies","DESERT"),
 ("c06",10,0,"shadowy figures of armed men watching from behind rocks on a desert ridge, faces hidden","DESERT"),
 ("c06",11,0,f"close-up portrait of {ANKH20} in white mourning clothes, sad, a tear running down her cheek","PALACE_BEDROOM"),
 ("c06",12,0,f"{AY} as an old man smiling coldly, standing in the shadow of a column in the throne hall","THRONE_HALL"),
 ("c06",13,0,f"{AY} sitting on the golden throne now, wearing the blue war crown of a pharaoh, holding the crook and flail","THRONE_HALL"),
 # c07 the tomb
 ("c07",0,0,"a funeral procession in the Valley of the Kings: priests, mourning women with raised arms, a gilded shrine on a sledge pulled by men in white","VALLEY_ANCIENT"),
 ("c07",1,0,"workers hurriedly painting a tomb wall by oil lamps in clay dishes, paint still wet, half-finished figures","TOMB_BURIAL_CHAMBER"),
 ("c07",2,0,"a small simple cross-section diagram of a tomb with a staircase, a corridor and four small rooms, drawn like an architect's sketch on papyrus, no labels","MAP"),
 ("c07",3,0,f"a painted tomb wall in yellow background ancient Egyptian style: {AY} wearing a leopard skin priest robe and the blue war crown, touching the mouth of a mummy-shaped figure of Osiris with a ritual tool","TOMB_BURIAL_CHAMBER"),
 ("c07",4,0,"workers carrying gilded beds shaped like animals, chests and chariot parts down a narrow rock staircase into a tomb","VALLEY_ANCIENT"),
 ("c07",5,0,"a crowded small tomb room in ancient times: dismantled chariots, gilded animal beds, a golden throne, weapons, jars of food, a board game, a small child's chair, lit by oil lamps in clay dishes","TOMB_ANTECHAMBER_ANCIENT"),
 ("c07",5,.7,"close-up of a tiny carved wooden coffin box with a lock of brown hair inside","TOMB_ANTECHAMBER_ANCIENT"),
 ("c07",6,0,"workers plastering a doorway shut and pressing oval clay seals onto the wet white plaster, by an oil lamp in a clay dish","TOMB_DOOR"),
 ("c07",7,0,"two tomb robbers in plain loincloths crawling through a small tunnel into a tomb at night, holding a single oil lamp in a clay dish, grabbing small gold objects","TOMB_ANTECHAMBER_ANCIENT"),
 ("c07",7,.6,"officials resealing the tomb doorway with fresh plaster and seals, a guard watching, torches","TOMB_DOOR"),
 ("c07",8,0,f"{HOR} as an older general in armour standing on a hill looking down at the Valley of the Kings, hard face","VALLEY_ANCIENT"),
 # c08 the chisel
 ("c08",0,0,f"{AY} as a very old pharaoh on the throne wearing the blue war crown, tired, the crown too heavy","THRONE_HALL"),
 ("c08",1,0,f"{HOR} crowned as pharaoh with the blue war crown, holding the crook and flail, in the throne hall, cold triumphant look","THRONE_HALL"),
 ("c08",2,0,"workers knocking down the walls of an open-air sun temple with wooden mallets and levers, carved stone blocks piling up","AMARNA_TEMPLE"),
 ("c08",2,.55,"small carved stone blocks with sun-disk reliefs being stacked face-down inside the core of a new temple gateway (pylon) under construction","KARNAK"),
 ("c08",3,0,"REUSE f009",None),
 ("c08",4,0,"a long carved stone list of royal names in cartouches on a temple wall, a priest pointing along it, one place obviously missing between two names","KARNAK"),
 ("c08",5,0,"200 years later: ancient Egyptian workmen building simple stone huts on the floor of the Valley of the Kings, tools and water jars","VALLEY_ANCIENT"),
 ("c08",6,0,"the flat floor of the Valley of the Kings covered with rubble and stone chips, the ruins of small workmen's huts on top, no entrance visible","VALLEY_ANCIENT"),
 ("c08",7,0,"close-up of a royal cartouche of Tutankhamun hacked away on a stone wall, dust in the light","KARNAK"),
 ("c08",8,0,"ancient tomb robbers with sacks walking past the rubble-covered valley floor at night with torches, not noticing anything","VALLEY_ANCIENT"),
 ("c08",9,0,"time-lapse style: the rubble-covered valley floor under changing skies, sand drifting, the moon and the sun","VALLEY_ANCIENT"),
 # c09 the step
 ("c09",0,0,"the Valley of the Kings in 1910: tourists on donkeys and horse carriages, other archaeologists packing up, empty excavated pits","VALLEY_1922"),
 ("c09",1,0,f"{CAR} with a sun hat on his head standing in the valley in 1915, arms crossed, looking at the rubble, determined","VALLEY_1922"),
 ("c09",2,0,f"close-up of {CAR}'s hand holding a small blue faience cup with a royal cartouche, in his tent","CARTER_TENT"),
 ("c09",3,0,f"{CARN} and {CAR} shaking hands in front of a grand English country house (Highclere Castle) in 1914","HIGHCLERE"),
 ("c09",3,.55,f"{CAR} watching rows of Egyptian workmen in galabiyas and turbans carrying baskets of rubble, sweat, heat, nothing found","VALLEY_1922"),
 ("c09",4,0,f"{CARN} in a library at Highclere Castle shaking his head at {CAR}, holding a cheque book, serious","HIGHCLERE"),
 ("c09",5,0,f"an Egyptian boy water-carrier in a galabiya kneeling in the rubble, brushing sand off the top of a stone step cut into the rock, morning","VALLEY_1922"),
 ("c09",6,0,f"{CAR} and workmen uncovering more stone steps going down, one after another","VALLEY_1922"),
 ("c09",7,0,"a steep rock-cut staircase of sixteen steps leading down to a sealed plastered doorway with oval seals at the bottom","TOMB_DOOR"),
 ("c09",8,0,f"{CAR} at a small telegraph office in Luxor in 1922 handing a telegram form to a clerk","LUXOR"),
 ("c09",9,0,f"{CARN} arriving on a donkey in the Valley of the Kings, wearing his cream linen suit and panama hat","VALLEY_1922"),
 ("c09",9,.6,"REUSE f005",None),
 ("c09",10,0,"REUSE f008",None),
 # c10 the mask
 ("c10",0,0,f"{CAR} and an assistant carefully wrapping a gilded animal bed in cotton, the crowded antechamber around them lit by electric lamps","TOMB_ANTECHAMBER"),
 ("c10",1,0,f"{CAR} at a table in the tomb writing on numbered record cards, a photographer with a 1920s box camera on a tripod","TOMB_ANTECHAMBER"),
 ("c10",2,0,"four huge golden shrines nested one inside the other, shown opened like Russian dolls, in a small painted burial chamber","TOMB_BURIAL_CHAMBER"),
 ("c10",3,0,"a large yellow quartzite stone sarcophagus with carved goddesses spreading their wings at the corners","TOMB_BURIAL_CHAMBER"),
 ("c10",4,0,"three nested mummy-shaped coffins of gold and blue, shown side by side from large to small","TOMB_BURIAL_CHAMBER"),
 ("c10",5,0,f"{CAR} kneeling and looking in awe at the innermost solid gold coffin, lit by electric lamps","TOMB_BURIAL_CHAMBER"),
 ("c10",6,0,"the golden death mask of Tutankhamun with blue lapis stripes on the nemes headdress, cobra and vulture on the brow, on black velvet","MUSEUM"),
 ("c10",7,0,"extreme close-up of the calm eyes of the golden mask","MUSEUM"),
 ("c10",8,0,"1920s newspapers fanned out on a table, each with a big photograph of the golden treasure, no readable words","NEWSROOM"),
 ("c10",9,0,"a 1920s fashionable woman in a flapper dress with Egyptian-style jewellery standing in front of an Egyptian-style art deco cinema entrance","LONDON_1923"),
 ("c10",10,0,"the golden mask glowing in a spotlight, flashes of 1920s cameras all around","MUSEUM"),
 ("c10",11,0,f"{CARN} in his cream linen suit sitting on a terrace in Egypt, pale and tired, holding his cheek","CAIRO_HOTEL"),
 # c11 the mosquito
 ("c11",0,0,"close-up of a mosquito landing on a man's cheek, comic style, warm evening light","CAIRO_HOTEL"),
 ("c11",1,0,f"{CARN} shaving in front of a mirror in a hotel room, a tiny nick on his cheek, a straight razor in his hand","CAIRO_HOTEL"),
 ("c11",1,.55,f"{CARN} lying in a hotel bed in Cairo, pale with fever, a nurse and a doctor beside him, night","CAIRO_HOTEL"),
 ("c11",2,0,"1920s journalists in hats crowding outside a hotel with notebooks and box cameras, cigarette smoke","CAIRO_HOTEL"),
 ("c11",3,0,"1923 newspaper front page with a dramatic drawing of a ghostly pharaoh's face rising over the tomb, no readable words","NEWSROOM"),
 ("c11",4,0,"the city of Cairo at night in 1923 with minarets, all the electric lights going dark at once","CAIRO_CITY"),
 ("c11",4,.55,"a small terrier dog lying asleep on a rug in a dark English country house room, a clock showing two o'clock","HIGHCLERE"),
 ("c11",5,0,"a gallery of 1920s newspaper clippings pinned to a wall with string, ghostly pharaoh drawings, no readable words","NEWSROOM"),
 ("c11",6,0,f"{CAR} as an older man of 64 with grey hair and moustache, in a dark suit, sitting quietly in a London flat with Egyptian objects on the shelves, 1939","LONDON_1939"),
 ("c11",7,0,"the huge modern Grand Egyptian Museum near the pyramids of Giza, crowds of visitors walking toward it, bright day","GEM"),
 ("c11",8,0,"close-up of a hacked-out royal name on an ancient temple wall, sunlight","KARNAK"),
 ("c11",8,.55,"REUSE f010",None),
 ("c11",9,0,f"{TUT17} standing proudly in front of the golden mask that glows huge behind him, sunrise over the Nile","NILE"),
]
STYLE_REFS = ["5d5f0d40-6d72-4644-b3e1-0f824c81becb", "8e1e1260-e11b-4083-a4d6-5f15a0a4008c"]
STYLE = ("Use reference images 1 and 2 ONLY for drawing style: clean editorial comic illustration, even medium-weight black outlines, "
         "flat muted colours, minimal cel shading, calm simple backgrounds. Do not copy any person or scene from them. "
         "Ancient scenes are period-accurate Egypt of the 1330s BC (18th dynasty): white pleated linen, broad collars, wigs, bronze and wood tools, "
         "oil lamps in open clay dishes; NO camels, NO iron, NO coins, NO turbans, NO glass lanterns, NO candles in ancient scenes. "
         "1920s scenes: 1920s clothes and objects only. ")
# single-person reference images (job ids), filled after chars/ are generated and checked
PREF = {"Tutankhaten age 9": "90700f16-d3cf-4596-94bd-56b4ca137ee8", "Tutankhamun age 18": "484419f6-a6de-4d02-8f13-dea2366247f3", "Ankhesenamun age 13": "362e890b-9c27-48a5-82c2-171a37d682f7", "Ankhesenamun age 20": "fd42eb4f-fb5c-4845-9391-b16b849ea2e0", "Akhenaten": "bde1d7e6-45a6-4bf5-9b0b-1647a9012ab1", "Ay": "dde33e9a-8fa7-4e3c-9b5f-eda3e286fcc5", "Horemheb": "a7d9ff14-d3ff-40a6-9191-64e7b7ab4591",
        "Howard Carter": "89a31d03-eac4-4dfd-ae1d-c66e98fcce88", "Lord Carnarvon": "5846c93b-ec5c-4baf-851c-5bdc6e10a004"}
LOOK = {"Tutankhaten age 9": "boy of 9, shaved head with a single braided sidelock of youth on the right side, long white pleated linen tunic with short sleeves and a white sash, gold-and-turquoise broad collar, sandals",
        "Tutankhamun age 18": "slim young king of 18, slight build, gentle face, blue-and-gold striped nemes headdress with a gold cobra on the brow, gold-and-turquoise broad collar, white pleated linen kilt and short cape",
        "Ankhesenamun age 13": "girl of 13, slim, long black braided wig to the shoulders with a thin gold circlet, white pleated linen dress, small turquoise collar",
        "Ankhesenamun age 20": "young queen of 20, long black braided wig to the shoulders with a thin gold circlet and a small cobra, white pleated linen dress, turquoise-and-gold broad collar, gold armbands",
        "Akhenaten": "pharaoh with a long narrow face, long chin, full lips, heavy-lidded eyes, tall blue khepresh crown, white pleated kilt, slight belly",
        "Ay": "old courtier of 60, wrinkled face, short grey wig, long white linen robe, gold collar of honour (rings of gold discs), long wooden staff",
        "Horemheb": "tough army general of 40, square jaw, short black wig, scale-armour linen corselet, bronze khopesh sword at the belt, red sash",
        "Howard Carter": "Englishman of 48, dark combed-back hair, thick dark moustache, dark bow tie, white shirt with rolled sleeves, grey tweed waistcoat",
        "Lord Carnarvon": "thin pale English aristocrat of 56, small grey moustache, cream linen suit, panama hat"}
# where a person never changes: (from shot, to shot, who, must-have words in the description)
CONTINUITY = [
 (53, 57, "Tutankhamun age 18", ["walking stick"]),          # the cane from the moment it is introduced
 (75, 88, "Ankhesenamun age 20", ["white mourning clothes"]), # widow from his death until Ay takes the throne
 (90, 102, "Ay (as", ["blue war crown"]),                     # Ay is king from shot 90
 (103, 103, "Horemheb (as", ["blue war crown"]),
]
NOT_PEOPLE = ["Valley of the Kings", "Karnak", "Amarna", "Thebes", "Nile", "Highclere", "Cairo", "Luxor", "Giza", "Osiris", "Amun", "Nefertiti"]
WHO = {"P": list(PREF)}
# LOCATIONS: description + anchor job (the first approved frame of that place becomes its anchor)
LOCATIONS = {
 "TOMB_DOOR": ("rock-cut corridor ending in a doorway of white plaster covered with rows of oval clay seal impressions", "7fdb6ba1-2ea7-4da5-bc31-8159ae75c175"),
 "TOMB_ANTECHAMBER": ("small rock-cut antechamber crammed with gilded animal beds, black-and-gold guardian statues, chests, chariot parts", "0f3c62a8-65b6-49c6-9379-41305e23467e"),
 "VALLEY_1922": ("the dry rocky Valley of the Kings with steep pale cliffs, rubble piles, workmen in white", "5e0a489e-d8bf-4b09-b62d-a43b45d567d4"),
 "TOMB_ANTECHAMBER_ANCIENT": ("the same small rock-cut antechamber as in 1922, crammed with gilded beds, statues, chests", "0f3c62a8-65b6-49c6-9379-41305e23467e"),
 "VALLEY_ANCIENT": ("the same Valley of the Kings cliffs, but ancient: no modern tents, no donkeys with baskets", "5e0a489e-d8bf-4b09-b62d-a43b45d567d4"),
 "KARNAK": ("sandstone temple walls with painted hieroglyphs and cartouches, giant columns, bright sun", "64be825d-4601-46f8-8763-c0a1a757ab1a"),
}
# minor recurring people: the first approved frame of the person becomes the anchor
ANCHOR = {"Suppiluliuma": None}
# locations that get an anchor = their first drawn frame (others like MAP, LAB, CTA, MUSEUM, NEWSROOM, DESERT stay free)
ANCHORED = ["AMARNA_CITY", "AMARNA_PALACE", "THEBES_TEMPLE", "AMARNA_TEMPLE", "THRONE_HALL", "COUNCIL_ROOM", "PALACE_GARDEN", "PALACE_BEDROOM",
            "HITTITE_HALL", "TOMB_BURIAL_CHAMBER", "HIGHCLERE", "CAIRO_HOTEL", "WORKSHOP", "NILE"]
def waves():
    """wave 1 = first shot of every anchored location without an anchor yet + first Suppiluliuma; wave 2 = everything else"""
    w1, seen = [], set()
    for k, x in enumerate(S, 1):
        if x[3].startswith("REUSE"): continue
        if x[4] in ANCHORED and x[4] not in seen and not LOCATIONS.get(x[4]): seen.add(x[4]); w1.append(k)
    k = first("Suppiluliuma")
    if k not in w1: w1.append(k)
    w2 = [k for k, x in enumerate(S, 1) if not x[3].startswith("REUSE") and k not in w1]
    return w1, w2
def first(n): return next(k for k, x in enumerate(S, 1) if n in x[3])
def request(i, loc_anchor=None):
    p, l, frac, desc, loc = S[i - 1]
    medias = [{"role": "image_references", "value": v} for v in STYLE_REFS]
    char = ""
    for n, mid in PREF.items():
        if re.search(re.escape(n) + r" \(as in the sheet\)", desc):
            assert mid, f"no reference for {n}"
            medias.append({"role": "image_references", "value": mid})
            char += f"Reference image {len(medias)} shows {n.split(' age')[0]} ({LOOK[n]}): draw him/her with exactly that face, hair and clothes. "
    for n, job in ANCHOR.items():
        if n in desc and job and first(n) != i:
            medias.append({"role": "image_references", "value": job}); char += f"{n} must look exactly like the man in reference image {len(medias)} (same face, beard and clothes). "
    a = loc_anchor or (LOCATIONS.get(loc, (None, None))[1] if loc else None)
    if a:
        medias.append({"role": "image_references", "value": a})
        char += f"Reference image {len(medias)} shows the place: keep the same walls, architecture, light and props (do not copy its people). "
    if char.count("shows") > 1 or "Reference image 3 shows" in char: char += "Each named person appears ONCE; nobody else may wear their clothes or look like them. "
    suffix = "No text, no captions, no title, no letters anywhere."
    return {"index": i, "params": {"model": "gpt_image_2_5", "variant": "flare", "quality": "low", "aspect_ratio": "16:9", "use_unlim": False, "medias": medias,
                                   "prompt": STYLE + char + "No gore, no blood, no dead bodies, no unwrapped mummy. Anatomically correct hands with five fingers, objects held with a natural grip. SCENE (16:9): " + desc + ". " + suffix}}
if __name__ == "__main__":
    print(len(S), "shots;", sum(1 for x in S if x[3].startswith("REUSE")), "reused")
# frame-QC redraws (wave 3): replace descriptions of rejected frames
FIX = {
55:"a magnified microscope view of tiny ring-shaped malaria parasites inside round red blood cells, filling the whole picture, a small mosquito silhouette in one corner, no people",
56:"dozens of ancient Egyptian walking sticks laid out in rows on a museum table under glass: straight sticks of gold, ebony, ivory and carved wood, some with forked or knobbed tops, no curved cane handles, no people",
59:"two tiny gilded wooden mummy-shaped coffins side by side in a dark ancient tomb corner, lit by a single oil lamp in a clay dish, no people",
69:"a computer screen in a modern lab showing a 3D reconstruction of a broken left thigh bone near the knee with a red circle around the break, no people",
101:f"{HOR} as an older general in armour standing on a rocky hill looking down at the empty ancient Valley of the Kings, hard face, no tents, no donkeys, no turbans, no modern people",
109:"the flat floor of the Valley of the Kings covered with rubble and stone chips, ruins of small ancient stone workmen's huts on top, no tomb entrance visible, no people",
110:"close-up of a royal cartouche on a sandstone temple wall hacked away with a chisel, the hieroglyphs inside destroyed, dust in the sunlight, an ancient Egyptian hand with a copper chisel and wooden mallet, no modern people",
112:"the rubble-covered floor of the Valley of the Kings at dusk under a dramatic sky, sand drifting over ruined huts, no tomb entrance visible, no people",
120:f"{CAR} kneeling at the top of a rock-cut staircase, Egyptian workmen in white galabiyas and turbans digging out more stone steps going down, 1922, daylight",
121:"a steep rock-cut staircase of sixteen steps leading down to a sealed plastered doorway with oval seals at the bottom, daylight from above, no people",
123:f"{CARN} arriving on a donkey in the Valley of the Kings, wearing his cream linen suit and panama hat, Egyptian workmen in white galabiyas and turbans in the background, 1922",
128:"four huge golden shrines nested one inside the other, shown opened like Russian dolls, in a small painted burial chamber, lit by 1920s electric lamps on stands, no people",
129:"a large yellow quartzite stone sarcophagus with carved goddesses spreading their wings at the corners, in a painted burial chamber lit by 1920s electric lamps, no people",
130:"three nested mummy-shaped coffins of gold and blue lying side by side from large to small on wooden trestles in a 1920s workshop in a tomb, electric lamps, no people",
132:"the golden death mask of Tutankhamun with blue lapis stripes on the nemes headdress, cobra and vulture on the brow, on black velvet, dramatic light, no people",
138:f"close-up of {CARN} without a hat, a mosquito landing on his cheek, warm evening light on a hotel terrace in Egypt",
139:f"{CARN} without a hat, in a white shirt with rolled sleeves, shaving with a straight razor in front of a mirror in a 1923 hotel room, a tiny nick on his cheek",
74:"Egyptian courtiers with short black wigs and generals in armour arguing loudly around the empty golden throne, NOBODY wears a royal striped headdress or a crown, nobody sits on the throne",
141:"1920s journalists in hats crowding outside the entrance of a colonial-era hotel in Cairo with notebooks and box cameras, palm trees, no skyscrapers, no modern buildings",
}
for _k, _d in FIX.items(): S[_k - 1] = S[_k - 1][:3] + (_d,) + S[_k - 1][4:]
# anchors of locations drawn in wave 1 (approved)
for _n, _j in {"AMARNA_CITY": "83f1c44e-9c6e-4578-a149-bdd662b0327a", "AMARNA_PALACE": "520aa24e-066f-4e3b-9b29-69fe8749e85d", "THEBES_TEMPLE": "e314b28e-b065-4536-af5c-15dc65e9b558",
  "AMARNA_TEMPLE": "012963e6-0b15-4cc8-912b-c2ceecaf86b5", "THRONE_HALL": "ebedbe2f-0da2-421c-825a-20030aa9bb4d", "COUNCIL_ROOM": "a4d470bc-d102-4d08-8aa3-bf0ccbe8cf2a",
  "WORKSHOP": "c30fe711-9321-46ef-9d02-aea26f6e7539", "NILE": "36420679-f0bb-49cf-9840-09a9ee5d04a6", "PALACE_GARDEN": "af952a47-97f2-4124-a9bb-859299271691",
  "PALACE_BEDROOM": "17d71bec-c4bd-417f-a503-02210599d389", "HITTITE_HALL": "95f032df-217c-4570-a698-0e55cd5a665b", "TOMB_BURIAL_CHAMBER": "9dc767fb-a83e-4c39-a6aa-8e6835bbaa58",
  "HIGHCLERE": "c51776d5-fec7-46b8-83dd-9ea87c8e3f7a", "CAIRO_HOTEL": "6d311907-f4ed-400a-9922-a379d2f00074"}.items(): LOCATIONS[_n] = ("", _j)
ANCHOR["Suppiluliuma"] = "95f032df-217c-4570-a698-0e55cd5a665b"
# VALLEY_ANCIENT must not inherit 1922 tents/donkeys: use the approved ancient valley frame instead
LOCATIONS["VALLEY_ANCIENT"] = ("", "13b1c9e7-494b-4cc2-ad93-cf4280cc8ac3")   # frame 91, ancient funeral in the valley
