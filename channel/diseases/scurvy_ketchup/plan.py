"""The Entire History of SCURVY - food-and-drinks (rum/ketchup) format, like smallpox_ketchup.
One line = one VO clip = one frame. Roles: N narrator (George), S Scurvy (villain, role_scurvy_santa_low).
Running gag: THE LEMON - a little lemon character that history keeps ignoring (a11 -> c09 -> d09 -> f07 -> f13 -> h12 -> i12 -> j09).
Callbacks: the reopening scar (a05 -> j08), the guinea pig (b05 -> i01), rum/grog (g07 cross-link).
Frame = (prompt, note, note_target). python3 plan.py -> voices/scurvy_ketchup/lines.txt + frames.json
"""
import json, os
ST = ("White background; detailed ink-line illustration, fine cross-hatching, soft muted watercolour, lemon-yellow and pewter grey accents, "
      "playful humorous cartoon tone; the whole subject is fully visible, cut out on white with white space around it, like a sticker. ")
PEOPLE = "Anatomy: every person has exactly one head, two arms attached at the shoulders, two hands with five fingers each, two legs; hands simple and clearly drawn. "
YOU = ("one simple hand-drawn stick figure: thin black ink line body, arms and legs, a round white head with dot eyes and an expressive mouth, "
       "simple white mitten hands, exactly two arms and two legs, wearing a small red-and-white striped knitted beanie, ")
LEMON = ("the lemon: one bright yellow lemon character with small dot eyes and a little mouth, thin black stick arms and legs and white mitten hands, ")
SC = ("Scurvy as a villain: a gaunt grinning ghostly old sea dog with pale grey-green skin and purple bruise spots, swollen purple gums with gaps where teeth fell out, "
      "a battered black tricorn, a tattered navy-blue 18th-century captain's coat with tarnished brass buttons, ")
SHIP = "on the wooden deck of an 18th-century sailing warship, only a small piece of deck, a mast and some ropes, white background around it, "
def NOTE(n, tgt): return (f" Big bold black brush-pen handwritten note on the white space: '{n}', with a thick hand-drawn arrow from the note to {tgt}. No other text."
                          if n else " No text anywhere.")
N, S = 'N', 'S'
L = [
 # ---- a: cold open ----
 ('a01',N,"It's seventeen forty one. You're a sailor on a British warship, sailing around the bottom of South America.", YOU+"standing "+SHIP+"holding a rope, huge grey waves behind the ship", 'Cape Horn, 1741', 'the ship'),
 ('a02',N,"You've been at sea for six months. And something is wrong with your mouth.", YOU+"holding a small hand mirror up to his wide-open mouth, worried eyebrows", '', ''),
 ('a03',N,"Your gums are swollen, purple, and bleeding.", "a cartoon close-up of an open mouth with swollen purple gums and a few drops of blood, teeth still in place; not gory", 'ouch', 'the purple gums'),
 ('a04',N,"You touch a tooth with your tongue. It wobbles.", "a cartoon close-up of one tooth wobbling, with little motion lines on both sides, a tongue pushing it", 'wobble', 'the tooth'),
 ('a05',N,"Then something really strange happens. A scar from a fight ten years ago opens up again.", YOU+"looking in horror at his own forearm, where an old scar line has split open a little, small shock lines around his head; not gory", '10 years old', 'the scar on the arm'),
 ('a06',N,"As if ten years of healing never happened.", "a cartoon wall calendar with pages flying backwards off it, a small rewind symbol above it; objects only, no people", '', ''),
 ('a07',S,"Ahoy, sailor. Long way from home, aren't we?", SC+"leaning on a ship's rail, waving one hand at the viewer with a creepy friendly grin", 'Scurvy (yes, the disease)', 'him'),
 ('a08',N,"Scurvy. Between fifteen hundred and eighteen hundred, by one estimate, it killed about two million sailors.", "a long row of many tiny identical sailor caps lying on the white ground, stretching into the distance; objects only", '2,000,000', 'the row of caps'),
 ('a09',N,"More than storms, shipwrecks and enemy cannons put together.", "a brass balance scale: on one pan a small storm cloud, a tiny shipwreck and a cannon; on the other pan one single lemon-yellow sailor's cap, and that pan is much heavier and lower; objects only", '', ''),
 ('a10',N,"And the cure was sitting in every port market on Earth.", "a small cheerful harbour market stall with a striped awning, baskets piled with lemons, oranges and green vegetables; no people", 'the cure', 'the basket of lemons'),
 ('a11',N,"This lemon.", LEMON+"standing alone, waving hello with one hand, proud smile", '', ''),
 ('a12',N,"Keep an eye on the lemon. People are going to ignore it for about three hundred years.", LEMON+"sitting alone on a small wooden bench, waiting, twiddling its thumbs, a little cobweb on the bench", '', ''),

 # ---- b: what it is ----
 ('b01',N,"So what is scurvy? It's not a germ. Nobody gives it to you.", "a large magnifying glass looking at an empty white circle: nothing inside, no germs; objects only", 'no germ', 'the empty lens'),
 ('b02',N,"It's what happens when your body runs out of one thing. Vitamin C.", "a cartoon fuel gauge on a body-shaped outline, the needle at EMPTY, a small orange slice icon on the gauge; objects only", 'vitamin C', 'the needle'),
 ('b03',N,"Most animals make their own vitamin C. Dogs, cats, rats, goats. They don't need oranges.", "a smug dog, a cat, a rat and a goat standing in a row, each with a tiny factory chimney puffing orange smoke on its back", '', ''),
 ('b04',N,"Humans can't. Somewhere in our distant past, the gene that makes it broke.", "a single cartoon DNA strand with one small broken link, a tiny repair spanner lying next to it; objects only", 'broken', 'the broken link'),
 ('b05',N,"Same for guinea pigs, fruit bats and some monkeys. Remember the guinea pig. It's coming back.", "a cute ginger-and-white guinea pig sitting front and centre, a fruit bat hanging and a small monkey beside it", 'remember me', 'the guinea pig'),
 ('b06',N,"Now, why does missing one vitamin make your body fall apart?", YOU+"scratching his head, a big question mark above him", '', ''),
 ('b07',N,"Because your body is held together by a protein called collagen. It's in your skin, gums, blood vessels and bones.", "a plain empty white human body silhouette outline (no face, no skeleton) with a network of golden ropes drawn inside it, running through skin, gums, blood vessels and bones like scaffolding; objects only", 'collagen', 'the golden ropes'),
 ('b08',N,"Think of collagen as a rope. And to tie that rope tightly, your body needs vitamin C.", "a thick golden rope being twisted tight by a small orange-slice character with tiny mitten hands and no feet; objects only", '', ''),
 ('b09',N,"Without it, the new rope comes out loose and weak.", "the same golden rope, now loose, frayed and floppy, a sad face drawn on the knot; objects only", 'weak', 'the frayed rope'),
 ('b10',N,"And your body replaces collagen all the time. Old rope wears out, and new, weak rope goes in.", "a cartoon conveyor belt moving from left to right: on the left strong golden ropes go in, on the right only floppy frayed ropes come out; objects only", '', ''),
 ('b11',N,"So after a month or two without vitamin C, you start coming apart at the seams.", YOU+"standing with his body drawn like a rag doll with stitched seams, a few stitches coming undone, worried face", '', ''),
 ('b12',N,"First, you're tired. Your legs ache.", YOU+"slumped against a barrel, exhausted, heavy eyelids, small ache lines on his legs", 'tired', 'his legs'),
 ('b13',N,"Then tiny blood vessels start to leak. Bruises appear out of nowhere.", "a cartoon close-up of a forearm with several purple bruises and many tiny red dots; not gory", 'bruises', 'the purple bruises'),
 ('b14',N,"Your gums swell and bleed, and your teeth come loose.", "a cartoon close-up of an open mouth: swollen purple gums and one tooth falling out with motion lines; not gory", '', ''),
 ('b15',N,"And old wounds, even old broken bones, can come apart, because the scar was made of collagen too.", "a simple cartoon X-ray of a shin bone with an old healed fracture line that is splitting open again, a small crack symbol; objects only", 'old fracture', 'the crack'),
 ('b16',N,"Without vitamin C, you die. Usually from bleeding, heart failure, or an infection your body can't fight off.", "a ship's hammock hanging empty, a sailor's striped cap lying on it, a single candle gone out with a thin wisp of smoke; objects only", '', ''),
 ('b17',S,"I'm in no hurry. I take you apart, one rope at a time.", SC+"sitting cross-legged, slowly unravelling a golden rope with his bony fingers, grinning", '', ''),
 ('b18',N,"And here's the cruel part. The cure works in days. A few lemons, and you start to recover almost at once.", "a cartoon calendar with only three days crossed off, a lemon next to it, a small green tick mark; objects only", 'days', 'the calendar'),

 # ---- c: the great voyages ----
 ('c01',N,"For most of history, scurvy was rare. People ate fresh food. A few cases in a long winter or a siege.", "a cosy medieval farm table with bread, apples, cabbage and onions; objects only", '', ''),
 ('c02',N,"Then, in the fourteen nineties, Europeans started sailing across whole oceans.", "a 15th-century caravel with big square sails crossing a wide blue ocean towards the horizon", '', ''),
 ('c03',N,"Months at sea with no fresh food. Just salted meat, and hard biscuits full of weevils.", "an old wooden barrel of grey-brown salted pork chunks in brine and a stack of hard square ship's biscuits with a few tiny cartoon weevils peeking out; objects only", 'lunch', 'the biscuits'),
 ('c04',N,"Ship's biscuit was so hard, you could break a tooth on it. If scurvy hadn't loosened your teeth first.", YOU+"biting a hard square biscuit, his teeth bending, eyes watering", '', ''),
 ('c05',N,"In fourteen ninety seven, Vasco da Gama sailed from Portugal, around Africa, to India.", "a hand-drawn sepia map of Africa and the Indian Ocean with a dotted route line from Portugal around the southern tip of Africa to India and a tiny ship on it; no text on the map", 'Vasco da Gama', 'the tiny ship'),
 ('c06',N,"More than half his men never came home. Most of them were killed by scurvy.", "a row of sailors' caps hung on wooden pegs, more than half of the pegs empty; objects only", '', ''),
 ('c07',N,"On the way, his crew noticed something. On the coast of East Africa, they ate oranges, and the sick men got better.", "two 15th-century Portuguese sailors in simple tunics sitting on a beach under a palm tree, eating oranges and smiling, a pile of oranges between them", '', ''),
 ('c08',N,"They wrote it down. And then forgot about it.", "an old leather logbook lying closed under a thick layer of dust and a cobweb; objects only", 'forgotten', 'the dusty logbook'),
 ('c09',N,"The lemon was not impressed.", LEMON+"with arms crossed and an unimpressed flat face, one eyebrow raised", '', ''),
 ('c10',N,"In fifteen nineteen, Magellan's fleet crossed the Pacific. More than three months with no fresh food.", "a small 16th-century ship alone in the middle of a huge empty calm Pacific Ocean, a tiny sun above it", 'Magellan, 1520', 'the ship'),
 ('c11',N,"The men ate rats. Sawdust. The leather wrapped around the ship's ropes, soaked in seawater and grilled.", "a sad tin plate with a grilled strip of old leather, a small pile of sawdust and a fork; objects only", "chef's special", 'the plate'),
 ('c12',N,"Out of about two hundred and seventy men, only eighteen made it home.", "eighteen tiny sailor stick figures standing in a small group on one side, and a much larger faded grey crowd of outlines on the other side", '18', 'the small group'),

 # ---- d: Cartier ----
 ('d01',N,"But a cure had already been found. In Canada.", "a snowy pine forest by a frozen river, a small wooden fort; no people", '', ''),
 ('d02',N,"Fifteen thirty five. The French explorer Zhahk Kartyay spends the winter with his ships frozen in the ice of the Saint Lawrence river.", "two small 16th-century French ships stuck in thick ice on a frozen river, snow on their decks and rigging", 'Jacques Cartier, 1535', 'the ships'),
 ('d03',N,"Twenty five of his men die of scurvy. Almost all the others are sick.", "a row of simple wooden crosses half-buried in snow beside a frozen river; objects only", '', ''),
 ('d04',N,"Then Kartyay notices something. A local man named Domagaya had been very sick, and now he's walking around, healthy.", "a 16th-century French explorer with a beard, plumed hat and heavy cloak staring in surprise at a healthy smiling young Iroquoian man in a fur-trimmed deerskin cloak walking past in the snow", 'Domagaya', 'the young man in deerskin'),
 ('d05',N,"Domagaya's people, the Saint Lawrence Irokwoyans, showed the French a tree. They boiled its bark and needles into a tea.", "a young Iroquoian man in a deerskin cloak holding out a steaming clay bowl of green tea made from evergreen needles, a cedar tree beside him, snow on the ground", 'the tree', 'the cedar'),
 ('d06',N,"Within days, the sick men recovered. Kartyay called it a miracle.", "a bearded 16th-century French sailor in a wool cap sitting up in a bunk, drinking from a clay bowl, colour back in his cheeks, surprised and happy", 'a miracle', 'the sailor'),
 ('d07',N,"The tree was probably a white cedar, packed with vitamin C.", "a single white cedar tree with flat scaly evergreen sprays, drawn like a botanical illustration, a small orange slice icon next to it; objects only", 'white cedar', 'the tree'),
 ('d08',N,"And Europe? Forgot that too.", "a small cartoon map of Europe sleeping with a nightcap and a snore bubble; no text", '', ''),
 ('d09',N,"Lemon, meet tree. Join the club.", LEMON+"sitting on a wooden bench next to a small cedar sapling character with a face, both bored, waiting", '', ''),

 # ---- e: Anson and the theories ----
 ('e01',N,"Back to you, on that ship in seventeen forty one. You're sailing with Commodore George Anson, around the world.", "an 18th-century British naval commander in a blue coat with gold buttons and a tricorn, standing proudly on a ship's deck with a telescope under his arm", 'Anson', 'the commander'),
 ('e02',N,"He left England with about nineteen hundred men.", "six 18th-century British warships with full white sails in a row at sea", '', ''),
 ('e03',N,"More than thirteen hundred of them died.", "a single battered warship with torn sails and a broken mast drifting alone on grey sea", '', ''),
 ('e04',N,"Only four were killed by the enemy. Almost all the rest were killed by scurvy.", "a simple cartoon tally: a tiny cannon with four small marks next to it, and a big lemon-yellow skull-and-crossbones flag with a huge pile of tally marks next to it; objects only", 'enemy: 4', 'the cannon'),
 ('e05',N,"Navies were losing more men to a missing vitamin than to war.", "a cartoon cannonball and a tiny orange slice on a boxing ring, the orange slice standing as the winner with a belt; objects only", '', ''),
 ('e06',S,"Best crew I ever had.", SC+"standing at a ship's wheel, steering happily, a ragged flag behind him", '', ''),
 ('e07',N,"And doctors had theories. Lots of theories.", "an 18th-century ship's surgeon in a powdered wig and dark coat holding a big quill, thinking hard, many small thought bubbles above him", '', ''),
 ('e08',N,"Bad air. Damp. Laziness. Sadness. Too much salt. Not enough exercise.", "a messy wooden blackboard covered with chalk doodles: a cloud, rain drops, a sleeping face, a sad face, a salt shaker and a running shoe, all crossed with question marks; objects only, no words", '', ''),
 ('e09',N,"The cures were just as creative. Vinegar. Seawater. Sulphuric acid. Being buried up to your neck in the earth.", YOU+"buried up to his neck in a pile of soil on a beach, only his head and cap showing, unhappy face", 'a cure?', 'his head'),

 # ---- f: Lind ----
 ('f01',N,"Then, in seventeen forty seven, a Scottish naval surgeon named James Lind tried something new.", "a young 18th-century Scottish naval surgeon with his own tied-back hair, a plain blue coat and a white cravat, holding a notebook, determined look", 'James Lind', 'the surgeon'),
 ('f02',N,"On board H M S Salisbury, he took twelve sailors with scurvy, all about equally sick.", "twelve small simple sick sailor stick figures in striped caps lying in two neat rows of hammocks; simple, same size", '12', 'the hammocks'),
 ('f03',N,"He split them into six pairs, and gave each pair a different cure.", "six numbered wooden bowls in a row on a table, each with a different thing: cider, vinegar, seawater, a small bottle with a skull, a garlic paste, and oranges and a lemon; objects only, numbers 1 to 6 on the bowls", '6 pairs', 'the bowls'),
 ('f04',N,"Cider. Vinegar. Seawater. Sulphuric acid. A paste of garlic and mustard. And two oranges and a lemon a day.", "a close-up of the last bowl holding two oranges and one lemon, glowing slightly; objects only", 'pair 6', 'the bowl'),
 ('f05',N,"It was one of the first controlled trials in the history of medicine.", "an old leather notebook open on a table with a neat hand-drawn table of six rows and two columns of tick marks, a quill beside it; no readable words", '', ''),
 ('f06',N,"Within a week, one of the citrus pair was back at work. The other was nursing the rest.", "one healthy smiling sailor in a striped cap climbing the ship's rigging, and another one carrying a bowl of soup to a hammock", '', ''),
 ('f07',N,"The lemon. Finally.", LEMON+"standing on a small wooden podium with both arms raised in triumph, little sparkles around it", '', ''),
 ('f08',N,"So Lind told the Navy to give everyone citrus, and scurvy was gone. Right?", YOU+"smiling hopefully, giving a thumbs up", '', ''),
 ('f09',N,"No.", LEMON+"face-palming with one hand, deeply disappointed", '', ''),
 ('f10',N,"Lind himself didn't fully trust his own result. He thought scurvy had lots of causes.", "the same young Scottish surgeon in a plain blue coat shrugging with both palms up, unsure face", '', ''),
 ('f11',N,"And to make lemon juice keep on long voyages, he boiled it down into a thick syrup.", "a big copper pot of lemon juice bubbling on a stove, steam rising, a few lemons beside it; objects only", '', ''),
 ('f12',N,"But heat destroys vitamin C. His syrup barely worked.", "a small glass bottle of dark brown syrup with a sad face drawn on the label, a crossed-out orange slice icon above it; objects only", 'useless', 'the bottle'),
 ('f13',N,"The lemon was ignored. Again.", LEMON+"sitting alone on the bench again, now with a longer cobweb, a small rain cloud above its head", '', ''),

 # ---- g: Cook and 1795 ----
 ('g01',N,"Captain James Cook did better. On his voyages in the seventeen seventies, almost nobody died of scurvy.", "an 18th-century British sea captain in a blue naval coat and white wig, standing confidently by a globe", 'Captain Cook', 'the captain'),
 ('g02',N,"His secret? He stopped for fresh food wherever he could. And he made the crew eat sauerkraut.", "a big wooden barrel overflowing with pale sauerkraut, a fork stuck in it; objects only", 'sauerkraut', 'the barrel'),
 ('g03',N,"The sailors refused. So Cook had it served only at the officers' table.", "two 18th-century naval officers in blue coats at a small fancy table, eating sauerkraut from silver plates with great pleasure", '', ''),
 ('g04',N,"Within a week, the crew were demanding sauerkraut too.", "two eager sailors in striped shirts holding out empty bowls, begging, puppy eyes", 'we want some', 'the sailors'),
 ('g05',N,"Sauerkraut has only a little vitamin C. The fresh food probably did most of the work. But Cook got the credit.", "a small gold trophy cup with a forkful of sauerkraut on top; objects only", '', ''),
 ('g06',N,"Finally, in seventeen ninety five, the Royal Navy ordered lemon juice for every sailor, every day. Mixed into their rum.", "a sailor's tin mug with a lemon being squeezed into it, juice dripping, a small rum barrel behind it; objects only", '1795', 'the mug'),
 ('g07',N,"If you watched our rum video, you already know this drink. Grog.", "a cheerful wooden barrel labelled with a painted lemon, a tin ladle and two tin mugs; objects only, no letters", 'grog', 'the barrel'),
 ('g08',N,"Scurvy almost vanished from the British Navy.", "a smiling healthy sailor in a striped shirt flexing his arm on a ship's deck, a lemon in his other hand", '', ''),
 ('g09',N,"Some historians think it helped Britain in the long wars against Napoleon. Its ships could stay at sea for months.", "a line of British warships blockading a coast, calm sea, a small bicorne hat sinking in the water beside them as a joke", '', ''),
 ('g10',S,"That was not fair at all.", SC+"sulking on a crate with his arms crossed, kicking a lemon away", '', ''),

 # ---- h: limes ----
 ('h01',N,"Then the Navy made a mistake.", "a single banana peel on a wooden ship's deck; objects only", 'uh oh', 'the banana peel'),
 ('h02',N,"In the mid eighteen hundreds, it switched from Mediterranean lemons to cheaper limes from British colonies in the Caribbean.", "a big yellow lemon and a small green lime on a weighing scale, a price tag with a tiny coin on the lime; objects only", 'cheaper', 'the lime'),
 ('h03',N,"Limes have much less vitamin C. And the way the juice was made and stored destroyed even more.", "a glass jug of lime juice next to old copper pipes and vats, the jug's orange-slice icon fading; objects only", '', ''),
 ('h04',N,"That's where the nickname came from. Limeys.", "a grinning 19th-century American sailor pointing and laughing at a British sailor holding a lime", 'limey!', 'the British sailor'),
 ('h05',N,"The juice was now almost useless. But on ships that stopped in ports, nobody noticed.", "a ship's tin mug of pale greenish liquid with a tiny question mark floating above it; objects only", '', ''),
 ('h06',N,"Until the polar expeditions. Months in the ice. No fresh food.", "a 19th-century wooden expedition ship frozen into Arctic pack ice, a polar bear watching from a distance", '', ''),
 ('h07',N,"In eighteen seventy five, a British Arctic expedition came back with scurvy, even though every man drank his lime juice.", "two 19th-century Arctic explorers in heavy fur coats, pale and tired, each holding a small bottle of lime juice, looking confused", '', ''),
 ('h08',N,"Doctors were baffled. Citrus didn't work? Maybe it was never about fruit.", "a Victorian doctor with side whiskers and a frock coat scratching his head, looking at a lime through a magnifying glass", '', ''),
 ('h09',N,"New theory: scurvy came from spoiled tinned meat.", "an old dented tin can of meat with a green stink cloud rising from it; objects only", 'new theory', 'the tin'),
 ('h10',N,"Antarctic explorers were still getting scurvy in the nineteen hundreds.", "an early 1900s explorer in a fur hood and goggles pushed up on his forehead, standing by a sledge in Antarctic snow, pale and gloomy", '', ''),
 ('h11',N,"The lemon had been right since fourteen ninety eight. And now even the Navy didn't believe it.", "a lemon character pinned under a heavy stack of old rule books, still pointing up with one finger", '', ''),
 ('h12',N,"Poor lemon.", LEMON+"sitting alone on the bench, now covered in snow, a tiny icicle on its nose", '', ''),

 # ---- i: guinea pigs and Szent-Gyorgyi ----
 ('i01',N,"The answer came from a guinea pig. Told you it would come back.", "the cute ginger-and-white guinea pig sitting proudly on a small lab bench, wearing a tiny lab coat", 'told you', 'the guinea pig'),
 ('i02',N,"In nineteen oh seven, two Norwegian scientists, Axel Holst and Tayodor Frolik, were studying a disease of sailors.", "two early-1900s scientists with moustaches in white lab coats at a wooden lab bench with glass flasks", 'Holst & Frølich', 'the two scientists'),
 ('i03',N,"They fed guinea pigs nothing but grain. And the guinea pigs got scurvy.", "a sad guinea pig in a small cage with a bowl of grain, a few small bruise spots on it, droopy eyes", '', ''),
 ('i04',N,"Then they added fresh cabbage, or lemon juice. And the guinea pigs got better.", "the same guinea pig in its small lab cage happily munching a cabbage leaf, a lemon slice beside it, sparkles around it", '', ''),
 ('i05',N,"If they had picked rats, which make their own vitamin C, they would have found nothing.", "a smug rat with a tiny factory chimney on its back puffing orange smoke, shrugging", 'useless', 'the rat'),
 ('i06',N,"Pure luck.", "a single four-leaf clover; objects only", '', ''),
 ('i07',N,"Then, in nineteen twenty eight, a Hungarian scientist, Albert Sent Jurjee, found a strange acid in cabbages and in adrenal glands.", "a 1930s Hungarian scientist with dark hair and a lab coat holding up a test tube with a cabbage on the bench", 'Szent-Györgyi', 'the scientist'),
 ('i08',N,"He needed kilos of it. So he looked around his city, Seged, famous for one crop. Paprika.", "a big heap of bright red paprika peppers spilling out of a wicker basket; objects only", 'Szeged', 'the paprika'),
 ('i09',N,"Paprika turned out to be packed with it.", "one red paprika pepper glowing like treasure with golden sparkles; objects only", '', ''),
 ('i10',N,"He called it ascorbic acid. Literally, the anti scurvy acid. Vitamin C.", "a small glass jar of white crystal powder with a big orange slice icon on its label; objects only, no letters", 'vitamin C', 'the jar'),
 ('i11',N,"He won the Nobel Prize in nineteen thirty seven.", "a gold medal on a ribbon lying on a red velvet cushion next to a paprika pepper; objects only", '1937', 'the medal'),
 ('i12',N,"And the lemon was finally, officially, right.", LEMON+"wearing a tiny gold medal, standing on a podium, crying happy tears", '', ''),

 # ---- j: today ----
 ('j01',N,"So, scurvy is gone today. Right?", YOU+"in a modern grey hoodie instead of the sailor cap, shrugging with a hopeful smile", '', ''),
 ('j02',N,"Not quite. Doctors still see it.", "a modern doctor in blue scrubs looking at a clipboard with raised eyebrows", '', ''),
 ('j03',N,"In people who eat almost nothing but toast, instant noodles or fast food for months.", "a modern plate with a slice of toast, a cup of instant noodles and a burger, no vegetables at all; objects only", '', ''),
 ('j04',N,"In elderly people living alone, in people with alcohol problems, and after some stomach surgeries.", "an elderly man in a cardigan sitting alone at a kitchen table with a cup of tea and plain toast", '', ''),
 ('j05',N,"The cure hasn't changed since Lind. Vitamin C. Most people start feeling better within days.", "a modern pharmacy bottle of vitamin C tablets next to a glass of orange juice; objects only, no letters", '', ''),
 ('j06',N,"And you need very little. One orange a day is plenty. So is a pepper, a kiwi, or a handful of strawberries.", "one orange, one red pepper, one kiwi cut in half and a few strawberries arranged neatly; objects only", 'that\'s it', 'the orange'),
 ('j07',S,"One orange. That's all it ever took to get rid of me. Embarrassing, really.", SC+"holding an orange at arm's length with two fingers like something disgusting, making a face", '', ''),
 ('j08',N,"So, back to you, on that ship in seventeen forty one, with the old scar opening up.", YOU+"standing on a ship's deck in a striped sailor's cap, holding a lemon in one thin stick hand and looking at it, a small scar line on the other thin stick arm", '', ''),
 ('j09',N,"The cure was a lemon. It cost almost nothing in any port. And it took the world three hundred years to listen to it.", LEMON+"standing on the white background, arms crossed, a small satisfied smile, a tiny crown on its head", '', ''),
 ('j10',N,"Would you have trusted the lemon? Tell me in the comments.", YOU+"holding a lemon up to the viewer, one eyebrow raised", '', ''),
]

if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    voices = os.path.join(here, '../../../voices/scurvy_ketchup'); os.makedirs(voices, exist_ok=True)
    with open(os.path.join(voices, 'lines.txt'), 'w') as f:
        for i, r, t, *_ in L: f.write(f"{i}|{'NARRATOR' if r == N else 'SCURVY'}|{t}\n")
    def has_people(p): return not ('objects only' in p or 'no people' in p.lower() or p.startswith(LEMON))
    frames = [{'id': i, 'line': t, 'prompt': ST + (PEOPLE if has_people(p) else '') + p + '.' + NOTE(n, tg)} for i, r, t, p, n, tg in L]
    json.dump(frames, open(os.path.join(here, 'frames.json'), 'w'), indent=1)
    words = sum(len(t.split()) for _, _, t, *_ in L)
    assert len({x[0] for x in L}) == len(L)
    assert not any('often' in t.lower() for _, _, t, *_ in L)
    print(len(L), 'lines', words, 'words', f'~{words / 2.95 / 60:.1f} min')
