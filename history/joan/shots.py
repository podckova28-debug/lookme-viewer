# Joan of Arc storyboard: (part, line, frac, description). A frame starts at `frac` of the narration line.
# Character sheets: J = Joan at 13 / 17 / 19 (left / centre / right), K = Charles VII, Baudricourt, Cauchon, Talbot.
# No fire, no blood, no wounds shown: the execution is shown through the crowd, smoke far away, the wooden cross, the river.
import re
S = [
 # c00 — cold open
 ("c00",0,0,"the medieval city of Rouen in Normandy in 1431 seen from a hill at dawn, cathedral spire, river Seine, half-timbered houses"),
 ("c00",1,0,"a parchment calendar page pinned to a wooden post reading '30 MAY 1431'"),
 ("c00",2,0,"a huge silent crowd of medieval townspeople, monks and English soldiers in red surcoats filling an old market square, seen from above"),
 ("c00",3,0,"a high wooden scaffold platform in the middle of the market square, a small figure in a long grey dress standing on it between two guards, seen from far away, grey sky"),
 ("c00",3,.55,"close-up of a tall white paper cap lying on a wooden table, written on it in black gothic letters exactly 'HERETIC RELAPSED APOSTATE IDOLATER'"),
 ("c00",4,0,"Joan age 19 (as in the sheet, short dark hair, grey dress) looking up, eyes calm and wet, grey sky behind, head and shoulders"),
 ("c00",5,0,"an English soldier in a red surcoat kneeling and tying two small sticks together into a rough little wooden cross with a strip of cloth"),
 ("c00",5,.6,"Joan age 19 (as in the sheet, short dark hair, long grey dress) holding a small rough wooden cross made of two sticks against her chest with both hands, grey sky, from the chest up"),
 ("c00",6,0,"Joan age 17 (as in the sheet) in armour on a white horse with a white banner leading charging French soldiers toward a fortress, pale sky"),
 ("c00",6,.6,"a cathedral interior, a young king kneeling as a gold crown is placed on his head, Joan age 17 (as in the sheet, short dark bob hair) in armour with a white banner beside the altar"),
 ("c00",7,0,"King Charles (as in the sheet) sitting alone on a throne in an empty hall, looking away, a letter dropped on the floor"),
 ("c00",8,0,"heroic portrait of Joan age 17 (as in the sheet) in armour holding her white banner on a hill, wind in her short hair, pale sky, an army behind her"),
 # c01 — the garden
 ("c01",0,0,"the small village of Domremy in 1412, stone and timber farmhouses, a little church, the river Meuse winding through green meadows"),
 ("c01",0,.6,"an old parchment map of France with a red pin at Domremy on the eastern border"),
 ("c01",1,0,"Jacques d'Arc, a sturdy French peasant farmer about forty with a short beard, ploughing a field with two oxen"),
 ("c01",2,0,"Isabelle, a peasant mother in a white coif, teaching a little girl to spin wool with a drop spindle by the hearth, a wooden crucifix on the wall"),
 ("c01",3,0,"medieval battle in the Hundred Years War, English longbowmen shooting volleys across a field at French knights, smoke, pale sky"),
 ("c01",4,0,"an old parchment map of France with the north and Paris coloured red for England, Burgundy coloured red-orange, the south blue for the French"),
 ("c01",5,0,"medieval nobles signing a treaty on parchment at a long table in a cathedral hall in 1420, red wax seals, a small crown on a cushion"),
 ("c01",5,.6,"a young sad prince in blue velvet staring out of a castle window, a crown on a table behind him out of reach"),
 ("c01",6,0,"Burgundian soldiers on horseback with red diagonal cross (saltire) banners raiding a medieval village, peasants running with bundles and cattle, smoke rising from barns far away, no fleurs-de-lis"),
 ("c01",6,.6,"a peasant family with a cart and cows fleeing along a road at dusk, a girl looking back over her shoulder"),
 ("c01",7,0,"Joan age 13 (as in the sheet) standing in her father's vegetable garden at noon, looking up in awe at a bright soft light in the sky beside the church"),
 ("c01",8,0,"a stained-glass window showing the archangel Michael with sword and scales, and two female saints with a wheel and a cross"),
 ("c01",9,0,"Joan age 13 (as in the sheet) kneeling alone in a small dim village church, hands folded, finger on her lips"),
 ("c01",10,0,"Joan age 13 (as in the sheet) standing on a hill above her village, looking west toward a distant road and the horizon, wind in her braid"),
 # c02 — the captain
 ("c02",0,0,"the walled fortress town of Vaucouleurs on a hill above the Meuse in 1428, stone towers, a gate"),
 ("c02",0,.55,"Joan age 13-16 (as the left figure of the sheet but a little older, red dress) standing before Robert de Baudricourt (as in the sheet) in a stone hall"),
 ("c02",1,0,"Robert de Baudricourt (as in the sheet) laughing loudly with his soldiers, pointing at the door"),
 ("c02",2,0,"a snowy road in January leading to the gate of Vaucouleurs, a girl in a red dress walking alone through the snow"),
 ("c02",3,0,"an old woman whispering to townspeople in a medieval street, a parchment with a drawing of a maiden in armour"),
 ("c02",4,0,"townspeople following Joan (as the left figure of the sheet, same face, red dress, braid, white coif) through a narrow medieval street, some kneeling, children running after her"),
 ("c02",5,0,"a messenger on a tired horse arriving at a castle gate with a sealed letter, Robert de Baudricourt (as in the sheet) reading it, frowning"),
 ("c02",6,0,"close-up of scissors cutting long dark brown hair, the braid falling to the floor"),
 ("c02",6,.5,"Joan age 17 (as in the sheet, short dark bob hair) in a man's dark tunic, hose and riding boots, mounting a horse, six armed men on horseback beside her at the town gate at dusk"),
 ("c02",7,0,"seven riders crossing a river ford at night under the moon, dark forest around them"),
 ("c02",7,.6,"an old parchment map of France with a red dotted route from Vaucouleurs west to Chinon on the Loire"),
 ("c02",8,0,"the castle of Chinon on a hill above the river Loire at sunset, long walls and towers"),
 # c03 — the crowd
 ("c03",0,0,"a great hall in the castle of Chinon at night, lit by torches and a huge fireplace, hundreds of richly dressed courtiers"),
 ("c03",1,0,"King Charles (as in the sheet) as the young Dauphin sitting nervously, counting a few coins from a small purse, worried face"),
 ("c03",2,0,"King Charles (as in the sheet) standing hidden among courtiers in plain clothes, while another richly dressed man sits on the throne"),
 ("c03",3,0,"Joan age 17 (as in the sheet, short dark hair) in a man's dark tunic kneeling before King Charles (as in the sheet) dressed in plain clothes, in the middle of a crowd of astonished French courtiers, no bishop, no knights in red"),
 ("c03",4,0,"Joan age 17 (as in the sheet) whispering to King Charles (as in the sheet) in a window alcove, the courtiers far away"),
 ("c03",5,0,"close-up of King Charles (as in the sheet), eyes wide, slowly nodding"),
 ("c03",7,0,"the town of Poitiers in 1429, a hall where a group of churchmen in black and white robes sit at a long table questioning a girl in a dark tunic"),
 ("c03",7,.6,"close-up of an old theologian with a quill, frowning over a big open book"),
 ("c03",8,0,"two noble ladies in tall headdresses walking toward a closed chamber door, a candle in hand"),
 ("c03",9,0,"a parchment document with a red wax seal on a table, a hand putting down a quill"),
 ("c03",10,0,"an old parchment map of France with a red pin on Orleans on the Loire, surrounded by small drawn English forts"),
 # c04 — the banner
 ("c04",0,0,"the medieval city of Orleans on the river Loire under siege in 1429, English wooden forts and siege camps around the walls, a long stone bridge"),
 ("c04",0,.6,"English archers with longbows in a wooden fort watching the walls of Orleans, a short fat 15th-century bombard cannon on a wooden sled beside them, no telescope"),
 ("c04",1,0,"an old parchment map: an arrow from Orleans pointing south across France"),
 ("c04",2,0,"an armourer fitting a polished steel breastplate on Joan age 17 (as in the sheet) in a workshop"),
 ("c04",3,0,"a white banner being sewn by women, painted with Christ holding the globe between two angels, with the words exactly 'JHESUS MARIA'"),
 ("c04",4,0,"a small stone church at Fierbois, a priest kneeling behind the altar and lifting an old rusty sword marked with five small crosses on the blade, candlelight"),
 ("c04",5,0,"a scribe writing a letter on parchment while Joan age 17 (as in the sheet) dictates, pointing a finger, in a tent"),
 ("c04",6,0,"close-up of a scribe's hand with a quill drawing a small cross at the bottom of a parchment letter, a steel armoured gauntlet resting on the table beside it"),
 ("c04",7,0,"an English commander in armour in a war tent reading a letter, his officers looking over his shoulder"),
 ("c04",8,0,"Joan age 17 (as in the sheet) in armour on a white horse entering the gate of Orleans at night, a huge crowd with torches cheering, the white banner above"),
 ("c04",9,0,"English soldiers laughing around a campfire, one waving a crumpled letter"),
 ("c04",10,0,"Joan age 17 (as in the sheet) in armour standing on the walls of Orleans at night, looking at English campfires below"),
 ("c04",12,0,"a sand hourglass on a stone ledge of the city walls of Orleans, English forts below, dawn"),
 # c05 — the arrow
 ("c05",0,0,"French captains in armour arguing over a map at a table in a hall, the door closed"),
 ("c05",1,0,"Joan age 17 (as in the sheet) outside a closed door, armour on, banner in hand, listening, frowning"),
 ("c05",2,0,"Joan age 17 (as in the sheet) galloping out of the city gate with her white banner, soldiers running behind her"),
 ("c05",3,0,"French soldiers with ladders climbing the wooden walls of an English fort east of Orleans, the white banner in front"),
 ("c05",4,0,"a second English fort with its flag being pulled down by French soldiers, smoke rising far away"),
 ("c05",5,0,"Les Tourelles, two massive stone towers on the bridge of Orleans across the Loire, English soldiers on top, French attackers with ladders below"),
 ("c05",6,0,"Joan age 17 (as in the sheet) on a ladder against a stone wall, an arrow in flight toward her, the moment before it hits, no blood"),
 ("c05",7,0,"soldiers carrying Joan age 17 (as in the sheet) away from the walls on their shoulders, her face in pain, no blood visible"),
 ("c05",8,0,"Joan age 17 (as in the sheet) standing up at sunset, raising her white banner high, a bandage on her shoulder over the armour"),
 ("c05",9,0,"hundreds of French soldiers charging toward the towers at sunset behind the white banner"),
 ("c05",10,0,"the English flag falling from the top of the Tourelles towers, French soldiers cheering on the walls"),
 ("c05",11,0,"the English army in long lines in a field outside Orleans at morning, facing the walls"),
 ("c05",11,.6,"the English army marching away along a road, their backs turned, banners lowered"),
 ("c05",12,0,"the people of Orleans ringing church bells and dancing in the streets, flowers thrown"),
 ("c05",13,0,"portrait of Joan age 17 (as in the sheet) smiling slightly, bandaged shoulder, the city behind her"),
 ("c05",14,0,"a crowd of townspeople kneeling as Joan age 17 (as in the sheet) rides past in armour with her banner"),
 ("c05",15,0,"Joan age 17 (as in the sheet) pointing at a map with a red pin on Reims, French captains looking at each other"),
 # c06 — the crown
 ("c06",0,0,"the gothic cathedral of Reims with its two towers and great rose window, seen from the square"),
 ("c06",0,.6,"an old parchment map with a long red line from the Loire north to Reims through red English territory"),
 ("c06",1,0,"old French generals in armour shaking their heads at a war council"),
 ("c06",2,0,"Joan age 17 (as in the sheet) slamming her gauntlet on the table, determined"),
 ("c06",3,0,"French soldiers entering a small walled town on the Loire through an open gate, townspeople watching"),
 ("c06",4,0,"French cavalry charging across an open field at Patay into surprised English archers who are still planting their stakes, June sun"),
 ("c06",5,0,"John Talbot (as in the sheet) on foot surrounded by French knights, lowering his sword, captured"),
 ("c06",6,0,"a long French army column marching north through wheat fields, townspeople opening a town gate and holding out keys"),
 ("c06",7,0,"inside Reims cathedral at the coronation of 1429, King Charles (as in the sheet) kneeling in royal blue robes with fleurs-de-lis as a thin grey-haired archbishop in a white mitre places a gold crown on his head, French nobles in blue around, no English soldiers"),
 ("c06",8,0,"Joan age 17 (as in the sheet) in armour standing near the altar of the cathedral holding her white banner, coloured light from the stained glass"),
 ("c06",9,0,"close-up of the white banner in the cathedral, torn at the edges and stained by battle"),
 ("c06",10,0,"an old parchment map of France: the blue French area now much bigger, red arrows pushed back"),
 ("c06",11,0,"Joan age 17 (as in the sheet) on horseback on a hill looking at the distant walls and towers of medieval Paris"),
 # c07 — the wall
 ("c07",0,0,"King Charles (as in the sheet) on a throne listening to Burgundian envoys in rich clothes, bowing, scrolls in hand"),
 ("c07",1,0,"bored French soldiers sitting around in a camp for weeks, dice games, horses tied, autumn leaves"),
 ("c07",2,0,"the walls and the gate of Saint-Honore of medieval Paris in 1429, a deep moat in front, French soldiers with bundles of sticks and ladders attacking"),
 ("c07",3,0,"Joan age 17 (as in the sheet) in armour standing at the edge of a water-filled moat, probing the water with the shaft of her lance, crossbowmen on the walls above"),
 ("c07",3,.65,"Joan age 17 (as in the sheet) sitting on the ground by the moat holding her thigh, a soldier kneeling beside her, no blood"),
 ("c07",4,0,"dusk over the walls of Paris, Joan age 17 (as in the sheet) still sitting by the moat, refusing the hand of a captain"),
 ("c07",5,0,"a French army packing up tents and marching away from Paris in the rain"),
 ("c07",6,0,"King Charles (as in the sheet) handing a parchment with a big wax seal to Joan age 17 (as in the sheet), who kneels, French courtiers in blue and green smiling politely, no bishop, no knights in red"),
 ("c07",7,0,"Joan age 17 (as in the sheet) in a fine dress at a royal court banquet, looking out of the window at the snow, restless"),
 ("c07",8,0,"Joan age 17 (as in the sheet) in armour standing on a town wall in spring, eyes closed, listening, a soft light behind her"),
 ("c07",9,0,"a dark storm cloud over a green spring field, a small white banner on a hill"),
 # c08 — the tower
 ("c08",0,0,"the walled town of Compiegne on the river Oise in May 1430, Burgundian siege camps around it, French riders galloping out of the gate over a bridge"),
 ("c08",1,0,"French riders turning back in confusion as many Burgundian soldiers attack from the sides"),
 ("c08",2,0,"the drawbridge gate of Compiegne being raised and closed, soldiers outside reaching for it"),
 ("c08",3,0,"a Burgundian archer pulling Joan age 17 (as in the sheet, same face, short dark bob hair, steel armour, red cloak) off her horse by the cloak, Burgundian soldiers around, no blood"),
 ("c08",4,0,"Joan age 17 (as in the sheet) in armour without her helmet, standing calmly in a Burgundian camp, Burgundian knights around her holding her banner, a castle in the distance"),
 ("c08",5,0,"King Charles (as in the sheet) at a table covered in gold coins, turning his face away from a messenger"),
 ("c08",6,0,"the tall square stone tower of the castle of Beaurevoir at night under the moon"),
 ("c08",6,.6,"a small figure in a grey tunic dropping from the top window of a very tall stone tower at night, seen from far below"),
 ("c08",7,0,"Joan age 19 (as in the sheet) lying on a straw bed in a castle room, bruised and bandaged, a guard at the door"),
 ("c08",8,0,"a heavy chest of gold coins pushed across a table from an English lord to a Burgundian lord, a contract with seals"),
 ("c08",9,0,"English lords in a dark council room looking at a map of France"),
 ("c08",10,0,"a bishop's crozier and a thick legal book on a table beside a candle, a shadow of horns on the wall behind"),
 # c09 — the question
 ("c09",0,0,"the castle of Rouen in winter 1431, round towers, English flags with lions, snow"),
 ("c09",1,0,"Pierre Cauchon (as in the sheet) seated in a high chair in a courtroom, cold eyes"),
 ("c09",2,0,"a large medieval courtroom full of judges and theologians in black and white robes on benches, scribes writing"),
 ("c09",3,0,"Joan age 19 (as in the sheet) alone on a small wooden stool in the middle of the courtroom, all eyes on her"),
 ("c09",4,0,"a dark cell in a castle tower, Joan age 19 (as in the sheet) sitting on a bench with an iron chain on her ankle, three English soldiers guarding"),
 ("c09",5,0,"many judges pointing and shouting at Joan age 19 (as in the sheet), who sits upright, calm"),
 ("c09",6,0,"close-up of Pierre Cauchon (as in the sheet) leaning forward with a thin smile"),
 ("c09",7,0,"a theologian in a black robe standing and asking a question, finger raised"),
 ("c09",8,0,"a golden balance scale on the judges' table, one pan tipped down"),
 ("c09",9,0,"the same golden balance scale tipped to the other side"),
 ("c09",10,0,"Joan age 19 (as in the sheet) answering, looking straight at the judges, calm and clear"),
 ("c09",11,0,"the judges frozen in silence, one scribe's quill stopped in mid-air"),
 ("c09",12,0,"Pierre Cauchon (as in the sheet) slamming a thick book shut, furious"),
 ("c09",13,0,"a dark corridor in the castle, an English guard holding a torch"),
 ("c09",14,0,"a wooden executioner's cart in an empty grey courtyard, rain"),
 # c10 — the dress
 ("c10",0,0,"the cemetery of Saint-Ouen abbey in Rouen, May 1431, two wooden platforms, a big crowd, English soldiers, Joan age 19 (as in the sheet) on one platform"),
 ("c10",1,0,"a preacher in a black and white habit shouting and pointing from the other platform"),
 ("c10",2,0,"a hooded executioner standing beside a horse-drawn wooden cart at the edge of the crowd, waiting"),
 ("c10",3,0,"Joan age 19 (as in the sheet) on the platform, frightened, a clerk holding up a short parchment and a quill to her"),
 ("c10",4,0,"close-up of a girl's hand drawing a small mark at the bottom of a parchment"),
 ("c10",5,0,"Pierre Cauchon (as in the sheet) reading a sentence from a scroll"),
 ("c10",5,.6,"a heavy iron door of a prison cell closing"),
 ("c10",6,0,"Joan age 19 (as in the sheet) in her cell, wearing the dark grey man's tunic and hose again, guards in the doorway staring"),
 ("c10",7,0,"a big question mark drawn in ink on an old parchment"),
 ("c10",8,0,"a woman's grey dress lying on the floor of a prison cell, a guard's boot beside it"),
 ("c10",9,0,"Joan age 19 (as in the sheet) sitting in the corner of the cell, knees drawn up, tunic laced tight, watching the guards"),
 ("c10",10,0,"Joan age 19 (as in the sheet) on her knees, eyes closed, a soft light from a high barred window"),
 ("c10",11,0,"the judges signing a document one after another"),
 ("c10",12,0,"close-up of a judge's parchment with the words exactly 'RELAPSED HERETIC'"),
 ("c10",13,0,"an empty market square at dawn, a tall wooden post in the middle, seen from far away, grey sky"),
 # c11 — the river
 ("c11",0,0,"English soldiers leading Joan age 19 (as in the sheet) in a long grey dress through a huge silent crowd in the old market square of Rouen"),
 ("c11",1,0,"a priest in a white surplice holding up a large processional crucifix high above a silent crowd in a market square, looking ahead, grey sky, no gallows, no rope"),
 ("c11",2,0,"the crowd in the square seen from behind, many people with heads bowed and hands to their faces, grey smoke rising far away above the rooftops"),
 ("c11",3,0,"a small boat on the river Seine at Rouen at dusk, a man emptying an urn into the water from a bridge, seen from far away"),
 ("c11",4,0,"an English official in dark clothes walking away from the square, head down, shaken"),
 ("c11",5,0,"French cannons and soldiers defeating the English at the battle of Castillon in 1453, English flags falling"),
 ("c11",5,.6,"an old parchment map of France almost all blue, only a tiny red spot at Calais"),
 ("c11",6,0,"a solemn church court in 1456 in Notre-Dame of Paris, an old woman in black (Joan's mother) kneeling before churchmen, a papal letter with a seal"),
 ("c11",6,.6,"close-up of an old trial document being torn in half"),
 ("c11",7,0,"Saint Peter's Basilica in Rome in 1920, a huge crowd in the square, a tapestry of a girl in armour hanging from the balcony"),
 ("c11",8,0,"close-up of a small rough wooden cross made of two sticks lying on a stone, a single ray of light on it"),
 ("c11",9,0,"a gilded statue of Joan of Arc in armour on horseback with her banner on a stone pedestal in an old French town square with gothic church and half-timbered houses at sunset, pigeons, pale sky, no modern buildings"),
]
STYLE_REFS = ["5d5f0d40-6d72-4644-b3e1-0f824c81becb", "8e1e1260-e11b-4083-a4d6-5f15a0a4008c"]
REFS = {"J": "ac9f7bd4-bea4-4bd2-ab0f-1a3e7eb0e885", "K": "eeb244aa-692a-488f-a79e-351e6c74413a"}
WHO = {"J": ["Joan"], "K": ["Charles", "Baudricourt", "Cauchon", "Talbot"]}
SHEET = {"J": "the Joan age sheet (left = age 13 peasant, centre = age 17 in armour, right = age 19 prisoner)",
         "K": "the lineup sheet (Charles VII, Baudricourt, Cauchon, Talbot, left to right)"}
STYLE = ("Use reference images 1 and 2 ONLY for drawing style: clean editorial comic illustration, even medium-weight black outlines, "
         "flat muted colours, minimal cel shading, calm simple backgrounds, period-accurate early-15th-century France. Do not copy any person or scene from them. ")
def request(i):
    p, l, frac, desc = S[i - 1]
    medias = [{"role": "image_references", "value": v} for v in STYLE_REFS]
    char = ""
    for k, names in WHO.items():
        hit = [n for n in names if re.search(r"\b" + n + r"\b", desc) and "sheet" in desc]
        if hit and REFS[k]:
            medias.append({"role": "image_references", "value": REFS[k]})
            char += f"{', '.join(hit)} must look exactly like the matching figure in {SHEET[k]}. "
            if k == "K": char += f"Only {', '.join(hit)} from that lineup sheet may appear; do not add the other men of the sheet. "
    suffix = "Any words or numbers written in the scene must be exactly as given." if re.search(r"'[A-Z0-9][^']*'", desc) else "No text, no captions, no title."
    return {"index": i, "params": {"model": "gpt_image_2_6", "aspect_ratio": "16:9", "use_unlim": False, "medias": medias,
                                   "prompt": STYLE + char + "No gore, no blood, no fire. SCENE (16:9): " + desc + ". " + suffix}}
if __name__ == "__main__":
    import json, sys
    print(len(S))
    if len(sys.argv) > 2:
        a, b = int(sys.argv[1]), int(sys.argv[2])
        json.dump({"requests": [request(i) for i in range(a, b + 1)]}, open(f"/tmp/claude-0/-home-user-lookme-viewer/affc662e-abb6-58d9-acf8-69d7acdec6d3/scratchpad/req_{a}.json", "w"))
