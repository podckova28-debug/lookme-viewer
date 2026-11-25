# Genghis Khan storyboard: (part, line, frac, description). A frame starts at `frac` of the narration line.
# Sheets: T = Temujin at 9 / 16 / 44 / 64 (left to right); K = Hoelun, Borte, Jamukha, Toghrul (left to right).
# Every recurring person is named with "(as in the sheet)". No blood, no killing shown.
import re
T9, T16, T44, T64 = ("Temujin age %d (as in the sheet)" % a for a in (9, 16, 44, 64))
HO, BO, JA, TO = ("%s (as in the sheet)" % n for n in ("Hoelun", "Borte", "Jamukha", "Toghrul"))
S = [
 # c00 cold open
 ("c00",0,0,"the endless Mongolian steppe at night under a full moon, a winding river, distant felt tents"),
 ("c00",1,0,f"{T16} lying on his back in a dark freezing river among reeds, only his face above the water, moonlight, seen from above"),
 ("c00",2,0,f"close-up of {T16} in the river, a heavy square wooden cangue board locked around his neck and wrists, his eyes wide open"),
 ("c00",3,0,"silhouettes of Mongol riders on horseback searching the river bank in the moonlight, one pointing at the reeds"),
 ("c00",4,0,f"{T16} alone on an empty steppe at dawn, ragged clothes, no horse, looking at the horizon"),
 ("c00",5,0,"an old parchment map of Eurasia with a huge area from China to the Caspian Sea painted in red, and the Roman Empire outlined small for comparison"),
 ("c00",5,.6,f"{T44} as Genghis Khan on a white horse on a hill, a huge Mongol army behind him with horse-tail banners, pale sky"),
 ("c00",6,0,"a herd of horses galloping over an empty grassy hillside, trampling the ground, no grave visible, sunset"),
 ("c00",7,0,f"heroic portrait of {T44} as Genghis Khan standing on the steppe, wind in his fur-trimmed hat, a white banner with nine horse tails behind him"),
 # c01 the blood clot
 ("c01",0,0,"the Onon River winding through green Mongolian grassland in 1162, a few round white felt tents (gers) by the water, horses grazing"),
 ("c01",1,0,f"{HO} holding a newborn baby wrapped in felt inside a felt tent, firelight"),
 ("c01",2,0,"close-up of a newborn baby's tiny fist holding a small dark red clot, old women in headscarves leaning over in wonder, firelight, no gore"),
 ("c01",3,0,"Yesugei, a Mongol chief about 35 with a thin moustache and a fur hat, on horseback with a falcon on his arm"),
 ("c01",4,0,f"Yesugei on horseback leading away the horse of a young bride, {HO}, who looks back, a cart behind them on the steppe"),
 ("c01",5,0,"a Merkit warrior in a dark deel standing alone on a hill, watching riders disappear, his fists clenched"),
 ("c01",6,0,f"Yesugei and {T9} riding side by side across the steppe"),
 ("c01",7,0,f"{T9} meeting {BO} as a little girl of ten, both shy, in front of a felt tent, her father smiling"),
 ("c01",8,0,"Yesugei sitting down at a campfire with Tatar men in white felt hats who offer him a bowl, their faces friendly but eyes cold"),
 ("c01",9,0,"an empty saddle on a riderless horse standing outside a felt tent at dusk"),
 ("c01",10,0,"close-up of an overturned wooden bowl on the grass beside a campfire, dark liquid spilled"),
 ("c01",11,0,f"{T9} standing alone in front of his family's tent at dusk, looking at a crowd of clansmen turning their backs"),
 # c02 the fish
 ("c02",0,0,f"{HO} with seven small children standing by a felt tent while clansmen walk away"),
 ("c02",1,0,"a long line of carts, horses and herds of sheep leaving a camp across the steppe at dawn"),
 ("c02",2,0,f"{HO} and her children alone on the empty steppe with one small tent, grey sky, cold wind"),
 ("c02",3,0,f"{HO} with her skirt tied up, digging roots from the ground with a juniper stick"),
 ("c02",4,0,"Mongol boys fishing with hooks and nets in a river, one holding a marmot by a burrow"),
 ("c02",5,0,f"{T16} sitting on a rock, thin and watchful, holding a small bow, eyes narrowed"),
 ("c02",6,0,f"Begter, a bigger teenage boy with a smug face, snatching a basket of fish from {T16} and another boy"),
 ("c02",7,0,"close-up of a silver fish lying on the grass beside a muddy boot"),
 ("c02",8,0,f"{T16} and his brother Khasar walking away from the camp with bows in their hands, seen from behind, evening"),
 ("c02",9,0,f"{HO} shouting angrily at {T16}, pointing at him, inside the tent"),
 ("c02",10,0,f"{T16} sitting alone outside at sunset, his long shadow on the grass"),
 ("c02",11,0,"a group of Tayichiud riders in brown armour galloping over a hill toward a lone tent"),
 # c03 the cangue
 ("c03",0,0,"Tayichiud chiefs talking in a big tent, one pointing toward the distance with a worried face"),
 ("c03",1,0,f"Tayichiud warriors locking a heavy square wooden cangue board around the neck and wrists of {T16}"),
 ("c03",2,0,f"{T16} wearing the wooden cangue, carrying a heavy bucket between felt tents while men laugh"),
 ("c03",3,0,"a summer feast in a Tayichiud camp at night, men drinking from bowls around big fires, music"),
 ("c03",3,.6,f"{T16} in the cangue running away into the dark grassland, a young guard sitting dazed on the ground behind him"),
 ("c03",4,0,f"{T16} lying in the river among reeds, only his face and the edge of the wooden cangue above the water, moonlight"),
 ("c03",5,0,f"Sorkan Shira, a kind old Mongol man with a grey beard, standing on the river bank looking down at {T16} in the water, finger on his lips, moonlight"),
 ("c03",6,0,"a broken wooden cangue burning in a small fire inside a tent"),
 ("c03",6,.5,"a cart piled high with raw sheep wool outside a tent, searchers pushing spears into the wool, one boy's boot hidden deep inside"),
 ("c03",7,0,f"{T16} riding a horse alone across the steppe at dawn, looking back over his shoulder"),
 ("c03",8,0,f"{T16} on a hilltop at sunrise, arms spread, free"),
 ("c03",9,0,f"{T16} looking at the horizon where a distant camp with smoke rises, thinking"),
 # c04 the sable coat
 ("c04",0,0,f"{T16} riding into a camp of the Onggirat people, {BO} as a young woman of 17 stepping out of a tent"),
 ("c04",1,0,f"{BO} and her mother presenting a magnificent black sable fur coat to {T16}"),
 ("c04",2,0,f"close-up of {T16} folding the black sable coat over his saddle"),
 ("c04",3,0,f"{T16} kneeling and offering the black sable coat to {TO} seated in a large decorated tent"),
 ("c04",4,0,f"{TO} placing his hand on the shoulder of {T16}, smiling"),
 ("c04",5,0,f"{T16} and {BO} outside their tent at sunset with a few horses, a small happy camp"),
 ("c04",6,0,"three hundred Merkit riders galloping over a hill toward a small camp at dawn, dust, bows raised"),
 ("c04",7,0,f"split image: on the left Yesugei taking {HO} away years ago, on the right Merkit riders galloping now"),
 ("c04",8,0,f"Merkit riders carrying {BO} away on horseback, she reaches back, the camp in chaos"),
 ("c04",9,0,"a Mongol storyteller-style scene: a felt tent at night with a single lamp glowing, peaceful steppe"),
 ("c04",11,0,f"{T16} standing in the ruined empty camp, clenching his fist, looking toward the horizon"),
 # c05 the knucklebone
 ("c05",0,0,f"{T16} speaking to a group of warriors around a fire"),
 ("c05",1,0,f"{TO} pointing to a column of his Kereit horsemen"),
 ("c05",2,0,f"{JA} riding up with his own warriors, smiling at {T16}"),
 ("c05",3,0,f"two Mongol boys of eleven, young {JA} and young Temujin, exchanging small knucklebones on the frozen Onon River, snow"),
 ("c05",4,0,"a night attack: Mongol horsemen charging into a Merkit camp, tents and fleeing people in the dark, seen from far away, no blood"),
 ("c05",5,0,f"{T16} on horseback in the dark among fleeing people calling out, {BO} running toward his horse with outstretched arms"),
 ("c05",6,0,f"{BO} holding a newborn baby boy in a felt tent, {T16} beside her"),
 ("c05",7,0,"two Mongol women whispering behind a tent, glancing toward the baby"),
 ("c05",8,0,f"{T16} and {JA} sitting together by one fire, sharing a blanket and laughing, felt tents behind"),
 ("c05",9,0,f"{JA} talking with richly dressed noble Mongol chiefs, his back turned"),
 ("c05",10,0,f"{T16} handing a sword to a young shepherd in poor clothes, other common herders watching"),
 ("c05",11,0,f"{T16} and {JA} riding away from each other at night in two different directions, each followed by riders"),
 ("c05",12,0,"the empty steppe split by a river at night, campfires on both sides"),
 # c06 the muddy water
 ("c06",0,0,f"{JA} and {T16} facing each other across a valley at the head of two armies, banners"),
 ("c06",1,0,f"{T16} retreating with a few riders from a lost battle, dust and broken banners behind, seen from far"),
 ("c06",2,0,f"{T44} as a grown warrior with short beard riding at the head of a bigger army"),
 ("c06",3,0,"Mongol cavalry riding past a defeated Tatar camp with white felt hats left on the ground, seen from far, no blood"),
 ("c06",4,0,f"{TO} in his tent whispering with a younger man, his son, both glancing sideways"),
 ("c06",5,0,f"{TO}'s warriors hiding in ambush behind a hill, waiting"),
 ("c06",6,0,f"{T44} with a handful of exhausted riders arriving at a small muddy lake on the steppe"),
 ("c06",7,0,"tired Mongol warriors around a small fire beside a muddy lake, their horses thin"),
 ("c06",8,0,f"{T44} raising a bowl of muddy water toward the sky, his companions kneeling around him, solemn"),
 ("c06",9,0,"a circle of Mongol warriors drinking muddy water from their hands and bowls, determined faces"),
 ("c06",10,0,f"{T44}'s army charging into the Kereit camp at night, tents and fleeing riders, from far away, no blood"),
 ("c06",11,0,f"{TO} riding alone and exhausted across a desert border at dusk, guards with spears ahead of him"),
 ("c06",12,0,f"{JA} alone on a mountain ridge at dusk, looking down at the valley"),
 # c07 the white banner
 ("c07",0,0,"a huge Mongol army on a plain facing the Naiman army at the foot of mountains, banners, dust, seen from far"),
 ("c07",1,0,f"{JA} and a few ragged men climbing into rocky mountains"),
 ("c07",2,0,f"{JA} with his hands tied, pushed forward by his own men toward a Mongol tent"),
 ("c07",3,0,f"{T44} pointing sternly at the traitors kneeling before his guards, his face hard"),
 ("c07",4,0,f"{T44} and {JA} sitting face to face in a tent, a single lamp between them"),
 ("c07",5,0,f"{JA} shaking his head calmly, looking down"),
 ("c07",6,0,"two small knucklebones lying on a felt carpet in the lamplight"),
 ("c07",7,0,f"the great assembly of 1206 by the Onon River: thousands of Mongols around a white banner with nine horse-tail tassels, {T44} standing in front"),
 ("c07",8,0,f"{T44} raised on a white felt carpet by chiefs, as Genghis Khan"),
 ("c07",9,0,f"close-up portrait of {T44} as Genghis Khan, calm and serious"),
 ("c07",10,0,f"{T44} as Genghis Khan on a hill looking south toward a distant line of walls and mountains"),
 # c08 the wall
 ("c08",0,0,"Jebe, a young enemy archer in Taichiud armour, with a lean face, short beard and a red headband, aiming a bow from behind a rock on a battlefield, his face clearly visible in profile, the arrow in flight toward a rider's horse, no blood"),
 ("c08",1,0,f"Jebe the captured archer kneeling but looking up boldly at {T44} as Genghis Khan"),
 ("c08",2,0,f"{T44} as Genghis Khan handing a bow to Jebe the archer, who stands up surprised"),
 ("c08",3,0,"Mongol officers of different tribes eating together in one big tent"),
 ("c08",4,0,f"{T44} as Genghis Khan promoting a common soldier, placing a paiza tablet in his hand"),
 ("c08",5,0,"rows of Mongol horsemen in neat units of ten with officers, a vast disciplined army on the plain"),
 ("c08",6,0,"a long defensive wall of the Jin Empire on hills in northern China, Mongol horsemen looking at it from below"),
 ("c08",7,0,"Mongol horsemen riding around a walled Chinese city, frustrated, arrows bouncing off the walls"),
 ("c08",8,0,"Chinese engineers building a large wooden siege catapult for Mongol officers"),
 ("c08",9,0,"the walls of the Jin capital Zhongdu with smoke rising from inside, Mongol army outside, seen from far"),
 ("c08",10,0,"an old parchment map of Asia with a large red area from Manchuria to the Altai mountains"),
 ("c08",11,0,f"{T44} as Genghis Khan looking west at sunset toward distant mountains"),
 # c09 the caravan
 ("c09",0,0,"a rich Central Asian city of Khwarazm with blue domes and minarets, merchants in turbans, 13th century"),
 ("c09",0,.6,"Shah Muhammad of Khwarazm, a proud ruler with a black beard, white turban and jewels, on a throne, his Persian guards in turbans and mail behind him, no Mongols"),
 ("c09",1,0,"a long camel caravan loaded with silver, furs and silk crossing the desert, Mongol merchants walking beside"),
 ("c09",2,0,"the governor of Otrar in a turban pointing accusingly at the caravan merchants, his guards drawing swords, seen before any violence"),
 ("c09",2,.6,"abandoned camels and scattered bales of silk outside the gates of Otrar, empty, dusk"),
 ("c09",3,0,"three Mongol envoys bowing before Shah Muhammad on his throne"),
 ("c09",4,0,"two Mongol envoys riding back across the steppe with their beards shaved off, humiliated"),
 ("c09",5,0,f"{T44} as Genghis Khan rising from his seat in fury, the envoys kneeling before him"),
 ("c09",6,0,"a huge Mongol army crossing snowy mountain passes in a long line"),
 ("c09",7,0,"an old parchment map of Central Asia with Bukhara, Samarkand, Urgench and Merv each crossed out in red"),
 ("c09",8,0,"the ruins of a great desert city, broken domes and empty streets, smoke on the horizon, no people"),
 ("c09",9,0,"an empty ruined city gate in the desert half-covered by sand, a lone stray dog"),
 ("c09",10,0,"Shah Muhammad alone in a plain robe sitting on a rock on a small barren island in the Caspian Sea, grey waves"),
 ("c09",11,0,f"{T64} as an older Genghis Khan with grey in his beard, seated in his tent"),
 ("c09",12,0,"two adult Mongol princes in rich deels arguing furiously in front of an older khan's seat, one pointing at the other"),
 ("c09",13,0,f"{T64} as Genghis Khan alone at night outside his tent, looking up at the stars"),
 # c10 the elixir
 ("c10",0,0,"Changchun, an old Chinese Taoist monk with a long white beard, blue robe and topknot, sitting in meditation in a mountain temple"),
 ("c10",1,0,"Changchun the old monk riding in a cart with a few disciples across a vast desert, then snowy mountains"),
 ("c10",2,0,f"{T64} as Genghis Khan receiving Changchun the old monk in a large tent in the mountains, both seated"),
 ("c10",3,0,f"close-up of {T64} as Genghis Khan leaning forward, eyes hopeful"),
 ("c10",4,0,"close-up of Changchun the old monk speaking calmly, hands folded"),
 ("c10",5,0,"a small empty porcelain medicine bottle on a low table between them, lamplight"),
 ("c10",6,0,f"{T64} as Genghis Khan handing a golden tablet to Changchun the old monk, who bows"),
 ("c10",7,0,f"{T64} as Genghis Khan mounting his horse in front of his army"),
 ("c10",8,0,"an old parchment map of northwest China with the Western Xia kingdom circled in red"),
 ("c10",9,0,"a Mongol army marching toward desert mountains at sunset"),
 # c11 the grave
 ("c11",0,0,"the walled cities of the Western Xia kingdom by the Yellow River with Buddhist pagodas, the Mongol army approaching"),
 ("c11",1,0,f"{T64} as Genghis Khan on a winter hunt, his horse rearing as wild horses gallop past, snow"),
 ("c11",2,0,f"{T64} as Genghis Khan sitting wrapped in furs in his tent, in pain but studying a map"),
 ("c11",3,0,"a Mongol camp in the mountains in August, the khan's great tent with banners lowered, warriors kneeling outside"),
 ("c11",4,0,"a single burning lamp beside an empty fur-covered bed in a dark tent"),
 ("c11",5,0,"a funeral procession of riders and a covered cart crossing the steppe toward a forested sacred mountain"),
 ("c11",6,0,"a herd of horses trampling a grassy slope at the foot of a forested mountain, no grave visible, dusk"),
 ("c11",7,0,"modern scientists with a ground radar and a laptop on a grassy Mongolian mountainside, a satellite image on the screen"),
 ("c11",8,0,"an empty grassy mountain slope under a big sky, nothing to see"),
 ("c11",9,0,"a modern crowd of hundreds of men of many nations in a city street, seen from above"),
 ("c11",10,0,f"{T16} in the dark river with the wooden cangue, only his face above water, moonlight"),
 ("c11",11,0,f"{T64} as Genghis Khan riding away into the misty mountains, seen from behind"),
 ("c11",12,0,"the Mongolian steppe at sunset, wind in the grass, a lone white banner with horse tails, no people"),
]
STYLE_REFS = ["5d5f0d40-6d72-4644-b3e1-0f824c81becb", "8e1e1260-e11b-4083-a4d6-5f15a0a4008c"]
REFS = {"T": "c633ee8a-96bb-40cc-81a3-0e8a9214defa", "K": "4adc513c-cd7a-44d3-98fd-7c7b29dcf1f9"}
# minor recurring people without a sheet: their FIRST frame is generated alone, then used as the face reference (job id filled in)
ANCHOR = {"Yesugei": "1a8245e8-67db-4fb9-9422-bbfed600141d", "Jebe": "547440df-92f1-496f-bc71-cf155834c57c", "Shah Muhammad": None, "Changchun": "6a984ba8-3196-4056-a22a-6c10e8c3520e"}
NOT_PEOPLE = ["China", "Caspian Sea", "Genghis Khan", "Onon River", "Merkit", "Tatar", "Tayichiud", "Kereit", "Khwarazm", "Otrar", "Western Xia"]  # Genghis Khan = Temujin (sheet)
WHO = {"T": ["Temujin"], "K": ["Hoelun", "Borte", "Jamukha", "Toghrul"]}
SHEET = {"T": "the Temujin age sheet (left to right: age 9, 16, 44, 64)",
         "K": "the lineup sheet (Hoelun, Borte, Jamukha, Toghrul, left to right)"}
STYLE = ("Use reference images 1 and 2 ONLY for drawing style: clean editorial comic illustration, even medium-weight black outlines, "
         "flat muted colours, minimal cel shading, calm simple backgrounds, period-accurate 12th-13th-century Mongolia and Asia. "
         "Do not copy any person or scene from them. Mongols wear deel robes, felt boots and fur hats; no Japanese or Chinese clothing on Mongols. ")
def first(n): return next(k for k, x in enumerate(S, 1) if n in x[3])
def request(i):
    p, l, frac, desc = S[i - 1]
    medias = [{"role": "image_references", "value": v} for v in STYLE_REFS]
    char = ""
    for k, names in WHO.items():
        hit = [n for n in names if re.search(r"\b" + n + r"\b", desc) and "sheet" in desc]
        if hit and REFS[k]:
            medias.append({"role": "image_references", "value": REFS[k]})
            char += f"{', '.join(hit)} must look exactly like the matching figure in {SHEET[k]}. "
            if k == "K": char += f"Only {', '.join(hit)} from that lineup sheet may appear; do not add the other people of the sheet. "
    for n, job in ANCHOR.items():
        if n in desc and job and first(n) != i:
            medias.append({"role": "image_references", "value": job})
            char += f"{n} must look exactly like the man in the last reference image (same face, hair and clothes). "
    suffix = "Any words or numbers written in the scene must be exactly as given." if re.search(r"'[A-Z0-9][^']*'", desc) else "No text, no captions, no title, no letters anywhere."
    return {"index": i, "params": {"model": "gpt_image_2_5", "variant": "flare", "quality": "low", "aspect_ratio": "16:9", "use_unlim": False, "medias": medias,
                                   "prompt": STYLE + char + "No gore, no blood, no dead bodies. SCENE (16:9): " + desc + ". " + suffix}}
if __name__ == "__main__":
    print(len(S))
