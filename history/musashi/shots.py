# Musashi storyboard: (part, line, frac, description). A frame starts at `frac` of the narration line.
# Character sheets: M = Musashi at 13 / 28 / 60 (left / centre / right), K = Kojiro, Seijuro, Kihei, Tadatoshi.
# No gore: fights are shown as the moment before or after the blow, silhouettes, or objects.
import re
S = [
 # c00 — cold open
 ("c00",0,0,"a small rocky island with a sandy beach in a calm strait at morning, mountains of two coasts on the horizon, pine trees, a calendar page pinned on a rock reading 'APRIL 1612'"),
 ("c00",1,0,"an old Japanese paper map of the strait between Honshu and Kyushu with a red pin on a tiny island"),
 ("c00",2,0,"Kojiro (adult, as in the sheet) standing on the beach, arms crossed, an extremely long sword across his back, crowd of officials and spectators behind a rope"),
 ("c00",2,.6,"close-up of an extremely long elegant katana blade glinting in the sun"),
 ("c00",3,0,"Kojiro staring at the empty sea, impatient, officials whispering behind him"),
 ("c00",4,0,"a sundial-like shadow of a tall pine moving across the sand, a small sign reading '1 HOUR'"),
 ("c00",5,0,"Kojiro pacing on the sand, angry, sweat on his brow, the shadow longer, a small sign reading '2 HOURS'"),
 ("c00",6,0,"a small wooden rowing boat with one rower landing on the beach, a tall man in grey standing in it, seen from behind"),
 ("c00",7,0,"close-up of Musashi's hands (adult) holding a rough wooden sword carved from a boat oar, wood shavings on his sleeves"),
 ("c00",8,0,"silhouettes of two swordsmen on a bright beach at the instant they pass each other, one falling, seen from far away, no blood"),
 ("c00",9,0,"heroic portrait of Musashi (adult) standing with a long and a short katana, wind in his loose hair, pale sky"),
 ("c00",9,.6,"an old leather-bound book 'THE BOOK OF FIVE RINGS' on a modern bookstore table next to business books"),
 # c01 — the placard
 ("c01",0,0,"a rural village in late-16th-century Harima, Japan, thatched houses, rice fields, smoke from a distant burning castle on the hills"),
 ("c01",1,0,"a stern samurai father in his forties with a topknot holding a jitte, a short iron truncheon with a side hook, practising in a dirt courtyard"),
 ("c01",2,0,"the stern father glaring down at a wild boy (Musashi age 13 as in the sheet) who glares back, arms crossed"),
 ("c01",3,0,"Musashi age 13 in a village street looking up at a tall wooden notice board with a samurai challenge written in Japanese brush characters"),
 ("c01",4,0,"Arima Kihei (as in the sheet) standing proudly beside his wooden challenge board, villagers watching nervously"),
 ("c01",5,0,"close-up: a boy's hand with a brush writing his name on the wooden challenge board, ink dripping"),
 ("c01",6,0,"Arima Kihei, a burly adult samurai, laughing scornfully with his hand on his katana"),
 ("c01",7,0,"Musashi age 13 holding a long wooden staff, barefoot, fierce stare, villagers behind him"),
 ("c01",8,0,"silhouette of a boy with a staff standing over a fallen adult samurai in the dust, crowd recoiling, no blood"),
 ("c01",9,0,"the empty challenge board knocked over in the dust, a broken staff beside it, evening light"),
 ("c01",10,0,"Musashi age 13 walking away down a long country road alone at sunset, staff on his shoulder"),
 # c02 — the battlefield
 ("c02",0,0,"the battle of Sekigahara in 1600, thousands of samurai with banners on poles charging across a misty valley, mountains around"),
 ("c02",0,.6,"an old paper map of Japan with a red pin at Sekigahara, two armies drawn as blocks of red and blue"),
 ("c02",1,0,"a young Musashi (between 13 and 28, as in the sheet) with a spear walking away from the smoking battlefield among fallen banners"),
 ("c02",2,0,"a scholar's desk with old Japanese documents and a magnifying glass over a map of Kyushu, a big question mark"),
 ("c02",3,0,"Tokugawa Ieyasu, an old heavy-set warlord in ornate armour seated on a camp stool under a white war curtain with crests"),
 ("c02",4,0,"a lone ronin (Musashi adult) in a worn kimono standing at a crossroads in the rain with a straw hat"),
 ("c02",5,0,"Musashi (adult) turning out an empty money pouch, a single coin falling"),
 ("c02",7,0,"Musashi (adult) walking along a mountain path with a straw hat and a travel bundle, mist below"),
 ("c02",8,0,"Musashi (adult) training alone with a wooden sword under a waterfall"),
 ("c02",8,.6,"Musashi (adult) sleeping under a tree beside a small fire, swords beside him"),
 ("c02",9,0,"Kyoto in 1604, wooden temples, pagoda and busy streets with merchants and samurai, Musashi (adult) arriving at the city gate"),
 ("c02",10,0,"the gate of a prestigious sword school in Kyoto with a family crest on curtains, students training inside"),
 # c03 — the pine tree
 ("c03",0,0,"the Yoshioka sword school hall in Kyoto, dozens of students in white training with wooden swords, the family crest on the wall"),
 ("c03",1,0,"Yoshioka Seijuro (as in the sheet) receiving a challenge letter from a servant, raising an eyebrow"),
 ("c03",2,0,"Yoshioka Seijuro waiting in a field at dawn with his students, looking at the sun, impatient"),
 ("c03",3,0,"Musashi (adult) and Yoshioka Seijuro facing each other with wooden swords in a field, the instant before the strike"),
 ("c03",4,0,"Yoshioka Seijuro on his knees in the grass, head bowed in shame, his students looking away"),
 ("c03",5,0,"Yoshioka Denshichiro, a younger tall samurai with a topknot and a long wooden sword, shouting a challenge"),
 ("c03",6,0,"a snowy temple courtyard at dusk, a fallen long wooden sword in the snow, Musashi (adult) walking away"),
 ("c03",7,0,"angry Yoshioka students in white sharpening real swords and spears by lamplight"),
 ("c03",8,0,"a huge old pine tree with low drooping branches at a crossroads outside Kyoto at night, a small boy in formal kimono with a guard of many armed students with spears and bows"),
 ("c03",9,0,"Musashi (adult) crouching hidden behind a rock near the big pine tree in the pre-dawn dark"),
 ("c03",10,0,"close-up of Musashi's eyes in the dark, watching, moonlight"),
 ("c03",11,0,"a dramatic dark silhouette of a swordsman with two swords bursting through a crowd of silhouetted armed men under the pine tree, dust and moonlight, no blood"),
 ("c03",12,0,"the Yoshioka sword school gate closed and abandoned, the crest curtain torn, autumn leaves"),
 ("c03",13,0,"an old man's hand (Musashi at 60) writing with a brush on a scroll in a cave by candlelight"),
 ("c03",14,0,"Musashi (adult) standing on a hill at sunrise, looking far away"),
 ("c03",16,0,"Kojiro (as in the sheet) drawing his extremely long sword in a temple courtyard, cherry blossoms swirling"),
 # c04 — the wooden sword
 ("c04",0,0,"Musashi (adult) walking through a series of different landscapes, mountains, villages, bridges, his straw hat on his back"),
 ("c04",1,0,"a fighter swinging a kusarigama, a sickle on a long chain, the chain whirling, Musashi (adult) facing him with two swords"),
 ("c04",2,0,"a group of samurai with long spears surrounding Musashi (adult), who holds a wooden sword calmly"),
 ("c04",3,0,"a monk with a long wooden staff facing Musashi (adult) on a bridge"),
 ("c04",4,0,"Musashi (adult) sitting on a rock carving a wooden sword with a knife, shavings at his feet"),
 ("c04",5,0,"a gleaming steel katana lying on a white cloth, cold light"),
 ("c04",6,0,"a plain wooden sword lying next to it on the same cloth, warm light"),
 ("c04",7,0,"Musashi (adult) in a fighting stance holding a long katana in one hand and a short sword in the other, the two-sword style"),
 ("c04",8,0,"a wall covered with tally marks carved in wood, more than sixty, a candle beside it"),
 ("c04",9,0,"travellers at a roadside tea house whispering, a poster with a portrait of a young swordsman with a ponytail on the wall"),
 ("c04",10,0,"Kojiro (as in the sheet) standing on a cliff, his crimson jacket and ponytail blowing in the wind, an extremely long sword on his back"),
 ("c04",11,0,"Kojiro's sword cutting through the air in a blur, a swallow in flight in front of it, feathers drifting"),
 # c05 — the oar
 ("c05",0,0,"an official notice on paper with a red seal announcing a duel, the date '13 APRIL 1612', a small drawing of an island"),
 ("c05",0,.6,"the port of Kokura with wooden ships and a castle, a small island visible in the strait"),
 ("c05",1,0,"Kojiro arriving on the island by an elegant boat at sunrise, officials bowing, his long sword on his back"),
 ("c05",2,0,"the empty beach where the opponent should be, footprints only from one side"),
 ("c05",3,0,"Musashi (adult) asleep on a futon in a merchant's house, a worried host trying to wake him"),
 ("c05",4,0,"Musashi (adult) sitting in a small rowing boat carving a long oar into a wooden sword with a knife, the rower looking back amazed"),
 ("c05",5,0,"Musashi (adult) jumping from the boat into knee-deep water holding the long oar-sword, Kojiro on the beach shouting in fury"),
 ("c05",6,0,"Kojiro drawing his extremely long sword and flinging the scabbard into the sea, splash"),
 ("c05",7,0,"Musashi (adult) standing in the shallows, calm, pointing at the floating scabbard"),
 ("c05",8,0,"close-up of the empty lacquered scabbard floating away on the waves"),
 ("c05",9,0,"Musashi and Kojiro leaping at each other on the beach, frozen mid-air, the oar and the long sword raised, sun behind"),
 ("c05",10,0,"close-up: a cut headband falling from Musashi's head, a few strands of hair"),
 ("c05",11,0,"silhouette from far away: one swordsman standing, one lying on the sand, officials frozen, no blood"),
 ("c05",12,0,"an old wooden signpost on the island being repainted with a new name"),
 ("c05",13,0,"the same island seen from the sea today, a small monument with two statues of the duellists"),
 ("c05",14,0,"Musashi (adult) rowing back across the strait alone, the oar-sword lying across the boat"),
 ("c05",15,0,"the oar-sword hanging on a wall in a quiet room, sunlight, dust"),
 # c06 — the stone
 ("c06",0,0,"a peaceful early-17th-century Japanese town, merchants, farmers, samurai without armour"),
 ("c06",1,0,"the siege of Osaka Castle, the huge white castle surrounded by armies, cannons and smoke, banners"),
 ("c06",2,0,"Musashi (between 28 and 60, greying temples) teaching a young boy to hold a wooden sword in a garden"),
 ("c06",3,0,"a young man in formal kamishimo kneeling before a daimyo lord, receiving an appointment scroll, Musashi watching proudly from the side"),
 ("c06",4,0,"Musashi (older, greying) waiting alone in an empty corridor of a castle, servants passing by ignoring him"),
 ("c06",5,0,"rebels behind the walls of a fortress on a cliff by the sea at Shimabara, Christian banners with crosses, besieging army below"),
 ("c06",6,0,"a stone thrown from a castle wall hitting the legs of an older samurai commander (Musashi in armour, greying) who falls from a ladder, soldiers catching him"),
 ("c06",7,0,"Musashi (older) lying with bandaged legs, writing a letter with a brush, a slightly embarrassed expression"),
 ("c06",8,0,"Musashi's armour and swords placed on a stand, a candle burning down"),
 ("c06",9,0,"an ink brush laid across a katana on a low table"),
 # c07 — the brush
 ("c07",0,0,"Musashi (at 60, as in the sheet) kneeling at a low table in a quiet room, preparing ink"),
 ("c07",1,0,"close-up of an ink stick being ground on a black stone, water, brushes"),
 ("c07",2,0,"three Japanese ink paintings on scrolls: geese flying, a monk, a bird on a branch"),
 ("c07",3,0,"a famous Japanese ink painting of a small shrike bird perched at the top of a long thin dead branch, displayed in a museum case with a small label"),
 ("c07",4,0,"Musashi (at 60) carving a small wooden statue, a raked stone garden behind him"),
 ("c07",5,0,"split image: on the left a sword cut, on the right a single brush stroke, the same curve"),
 ("c07",6,0,"Hosokawa Tadatoshi (as in the sheet) welcoming Musashi (at 60) in a castle hall in Kumamoto, retainers bowing"),
 ("c07",7,0,"Musashi (at 60) in a simple house with a garden, a servant bringing tea, a bag of rice and coins on a tray"),
 ("c07",8,0,"a funeral procession of a daimyo with white banners; Musashi (at 60) walking away up a mountain road alone"),
 # c08 — the cave
 ("c08",0,0,"the entrance of a rocky mountain cave with stone Buddhist statues nearby, mist, mountains near Kumamoto"),
 ("c08",1,0,"Musashi (at 60) sitting cross-legged on the rock floor of the cave writing on a long scroll by candlelight"),
 ("c08",2,0,"a scroll with Japanese brush calligraphy title, beside it a small handwritten paper tag reading 'THE BOOK OF FIVE RINGS'"),
 ("c08",4,0,"five round seals in a row: earth, water, fire, wind and an empty circle for void, each drawn simply"),
 ("c08",5,0,"pages of an old manual with small drawings of sword stances and footwork diagrams"),
 ("c08",6,0,"Musashi (at 60), thin and ill, writing a short list on a single sheet, a blanket over his shoulders"),
 ("c08",7,0,"a sheet of paper with twenty-one short vertical lines of brush calligraphy"),
 ("c08",8,0,"Musashi (at 60) sitting calmly at the cave entrance watching the sunset over mountains"),
 ("c08",9,0,"a candle burned down to the end in the cave"),
 ("c08",11,0,"a calendar page reading '13 JUNE 1645' pinned to a wooden post, a single white chrysanthemum"),
 ("c08",12,0,"an old stone grave marker beside a country road under pine trees, a helmet-shaped stone on top"),
 ("c08",13,0,"the scroll of the Book of Five Rings lying on a stand, a wooden sword beside it"),
 # c09 — the book
 ("c09",0,0,"a 1930s Japanese city street with trams and people in Western suits and kimonos"),
 ("c09",1,0,"a 1930s reader on a train reading a newspaper novel with a samurai illustration, other passengers peeking"),
 ("c09",2,0,"a 1970s typewriter with an English manuscript page, a Japanese dictionary and the old scroll beside it"),
 ("c09",3,0,"businessmen in 1980s suits in an office meeting room, one holding up 'THE BOOK OF FIVE RINGS'"),
 ("c09",4,0,"a modern bookstore shelf with copies of 'THE BOOK OF FIVE RINGS' in many languages next to business books"),
 ("c09",5,0,"an airport bookshop with travellers browsing, a stack of 'THE BOOK OF FIVE RINGS' in front"),
 ("c09",6,0,"a long row of over sixty wooden swords standing in racks in an empty hall"),
 ("c09",7,0,"Musashi (adult) in silhouette standing on the beach at sunset with the oar-sword, the book glowing in the sky behind like the sun"),
]
STYLE_REFS = ["5d5f0d40-6d72-4644-b3e1-0f824c81becb", "8e1e1260-e11b-4083-a4d6-5f15a0a4008c"]
REFS = {"M": "3b8f7699-fb8d-42fa-824f-1ec2d7157920", "K": "65ea223f-c502-4899-9a45-97a27c964782"}
WHO = {"M": ["Musashi"], "K": ["Kojiro", "Seijuro", "Kihei", "Tadatoshi"]}
SHEET = {"M": "the Musashi age sheet (left = age 13, centre = age 28, right = age 60)",
         "K": "the second lineup sheet (Kojiro, Seijuro, Kihei, Tadatoshi)"}
STYLE = ("Use reference images 1 and 2 ONLY for drawing style: clean editorial comic illustration, even medium-weight black outlines, "
         "flat muted colours, minimal cel shading, calm simple backgrounds, period-accurate early-17th-century Japan. Do not copy any person or scene from them. ")
def request(i):
    p, l, frac, desc = S[i - 1]
    medias = [{"role": "image_references", "value": v} for v in STYLE_REFS]
    char = ""
    for k, names in WHO.items():
        hit = [n for n in names if re.search(r"\b" + n + r"\b", desc)]
        if hit and REFS[k]:
            medias.append({"role": "image_references", "value": REFS[k]})
            char += f"{', '.join(hit)} must look exactly like the matching figure in {SHEET[k]}. "
    suffix = "Any words or numbers written in the scene must be exactly as given." if re.search(r"'[A-Z0-9][^']*'", desc) else "No text, no captions, no title."
    return {"index": i, "params": {"model": "gpt_image_2_6", "aspect_ratio": "16:9", "medias": medias,
                                   "prompt": STYLE + char + "No gore, no blood. SCENE (16:9): " + desc + ". " + suffix}}
if __name__ == "__main__":
    print(len(S))
