# frame -> (part, line index, prompt, note). One shot per script line. Built to drinks/STYLE.md (ketchup = reference).
# Running gag: the "WHO INVENTED IT?" game-show stage, one more numbered podium each time (p0, p3 x5, p5, p8).
# Callbacks: the 1904 fair stand (p0 -> p8), the Mongol saddle myth (p1 -> p8), ketchup (p4, p7).
STYLE = ("White background; detailed ink-line illustration, fine cross-hatching, soft muted watercolour, warm brick red and mustard yellow accents, "
         "playful humorous cartoon tone; cut out on white, lots of white space. ")
YOU = "stick-figure 'you' "
WHO = ["a 15-year-old boy in an 1880s cap", "two brothers with big moustaches standing together", "an old cook with a white beard and an apron",
       "a man in an 1890s suit and bowler hat", "a man in a 1900 white cook's apron and cap", "a small white castle-shaped building wearing a tiny bow tie"]
def SHOW(n, extra=""):
    pods = "; ".join(f"podium {i + 1}: {WHO[i]}" for i in range(n))
    return (f"a cheerful 1950s TV game-show stage with a big red curtain and a sign 'WHO INVENTED IT?', {n} small wooden podium{'s' if n > 1 else ''} in a row, "
            f"numbered from 1 to {n}; {pods}; every contestant is visible only from the chest up and both hands are hidden behind the podium{extra}")
SHOTS = [
 # p0 — the 1904 fair
 (0,0,YOU+"in a straw boater hat walking through the crowded 1904 St. Louis World's Fair, white palace-like exhibition halls, flags without symbols, balloons","you"),
 (0,1,YOU+"in a straw boater hat fanning himself, sweating in the sun, his stomach rumbling with little cartoon rumble lines","1904, hungry"),
 (0,2,"a cheerful 1904 food-stand cook in a white apron and cap slapping a sizzling beef patty between two slices of white bread on a hot griddle, steam rising",""),
 (0,3,"a plain white plate crossed out with a big red X, no people","no plate"),
 (0,4,"a single metal fork crossed out with a big red X, no people","no fork"),
 (0,5,YOU+"in a straw boater hat happily walking and biting a hamburger in bread at the same time, little motion lines",""),
 (0,6,YOU+"in a straw boater hat holding a hamburger up like a trophy, confetti falling",""),
 (0,7,"a simple early hamburger: a thick beef patty between two slices of plain bread, glowing in a spotlight like a celebrity, no people","meet the hamburger"),
 (0,8,"a gigantic mountain of hamburgers towering over a tiny modern American city skyline, no people","billions a year"),
 (0,9,"a hamburger standing on a small globe like a king, wearing a tiny gold crown, no people","most famous sandwich on Earth"),
 (0,10,YOU+"in a straw boater hat scratching his head, a big question mark above him, holding a half-eaten hamburger","who invented it?"),
 (0,11,YOU+"in a straw boater hat giving a confident thumbs up next to a big hand-drawn red tick mark","easy!"),
 (0,12,SHOW(5),"5 inventors?!"),
 (0,13,"two old family photo albums on a table, each with a handwritten label, a little cartoon lightning bolt of argument between them, no people","still arguing"),
 (0,14,"an old map of Germany with the port city of Hamburg marked, and a large red question mark next to it, no people","not from Hamburg"),
 (0,15,"a hamburger bun with the word 'HAMBURG' written on top in sesame seeds, a tiny old German harbour town drawn on a hill behind it, no people","?"),
 (0,16,"a road sign pointing back in time with the words 'THIS WAY: 1800s', no people","let's go"),
 # p1 — Mongol myth, Hamburg
 (1,0,"an old leather-bound book of legends lying open, a little puff of magic dust coming out, no people","a legend"),
 (1,1,"a 13th-century Mongol rider in a fur hat and quilted robe on a small sturdy steppe horse, galloping across grassland",""),
 (1,2,"a 13th-century Mongol rider sitting on a slab of raw red meat placed under his saddle, the horse looking back at it suspiciously","the legend"),
 (1,3,"three historians in tweed jackets searching through piles of old books and scrolls with magnifying glasses",""),
 (1,4,"an empty wooden box labelled 'PROOF', open, with a single cobweb inside, no people","none"),
 (1,5,"a small steppe horse looking straight at the viewer, very unimpressed, one eyebrow raised, a slab of meat on its back, no people","the horse would like a word"),
 (1,6,"the 19th-century port of Hamburg with tall sailing ships and early steamships at the docks, brick warehouses, church spires","Hamburg"),
 (1,7,"a proud 19th-century German butcher in an apron standing in front of his shop, holding up a big piece of beef",""),
 (1,8,"a 19th-century German cook in a kitchen frying a round minced beef patty with onions in a black iron pan",""),
 (1,9,"a big 1880s steamship crowded with emigrants on deck, leaving the port of Hamburg, waving","to New York"),
 (1,10,"a 19th-century emigrant family on a ship's deck with a suitcase, a basket and a small frying pan sticking out of the bag",""),
 (1,11,"an 1880s New York restaurant chalkboard menu with the words 'HAMBURG STEAK' circled, no people",""),
 (1,12,"a minced beef patty with fried onions on a plain white plate with a knife and fork, no bread, no people","Hamburg steak"),
 (1,13,"the same plate of Hamburg steak with a little sad empty dotted outline of a missing bun next to it, no people","still no bun"),
 # p2 — Hamburg steak in America
 (2,0,"a busy 1880s New York street with horse-drawn carriages and a small cheap restaurant with a sign reading 'HAMBURG STEAK 10c'","1880s"),
 (2,1,"a single copper coin next to a plate of Hamburg steak, a small green tick, no people","cheap"),
 (2,2,"an old tough piece of beef going into a cast-iron meat grinder and coming out as soft minced meat, no people",""),
 (2,3,"a happy old man in 1880s clothes with almost no teeth smiling while eating minced beef with a spoon","great news"),
 (2,4,"a suspicious 1880s diner peering at his plate of minced beef through a magnifying glass, one eyebrow raised","what's in it?"),
 (2,5,"a 19th-century cast-iron hand-crank meat grinder clamped to a butcher's wooden counter, minced beef coming out, no people",""),
 (2,6,"a row of 1880s butcher shops, every window full of trays of minced beef",""),
 (2,7,"a Hamburg steak on a plate floating in the air with a big red question mark beside it, no people","problem:"),
 (2,8,YOU+"standing in a busy 1880s street holding a plate of Hamburg steak with a knife and fork, looking around for a table, there is none","you need a table"),
 (2,9,"busy 1890s American workers in caps rushing past with lunch pails, a big clock on a building","hurry!"),
 (2,10,"1890s factory workers eating lunch standing up next to a brick wall, no tables",""),
 (2,11,"an 1890s county fair crowd walking past stalls, everyone eating something on the move",""),
 (2,12,YOU+"holding a slice of bread in one hand and a Hamburg steak on a fork in the other, about to put them together, a light bulb above his head",""),
 (2,13,"a cheerful 1950s TV game-show stage with a big red curtain and a sign 'WHO INVENTED IT?', one single small wooden podium numbered 1 under a spotlight, nobody behind it, a big question mark floating where the contestant should be, no people","who?"),
 # p3 — the contestants
 (3,0,SHOW(1),"contestant 1"),
 (3,1,"a 15-year-old boy in 1880s clothes and a cap at a county fair stand in Wisconsin, a tray of meatballs in front of him","Charlie Nagreen, 1885"),
 (3,2,"fairgoers in 1880s clothes walking past a stand of meatballs, one man dropping a meatball from his hand as he walks",""),
 (3,3,"a teenage boy in 1880s clothes squashing a meatball flat with a spatula and putting it between two slices of bread, proud smile",""),
 (3,4,"a small Wisconsin town welcome sign reading 'SEYMOUR — HOME OF THE HAMBURGER', a giant statue of a hamburger behind it, no people","Hamburger Charlie"),
 (3,5,SHOW(2),"contestant 2"),
 (3,6,"two brothers with big moustaches in 1880s clothes at a wooden fair stand with a frying pan, a banner above reading 'ERIE COUNTY FAIR'","the Menches brothers, 1885"),
 (3,7,"a small 1880s American village signpost reading 'HAMBURG, N.Y.', a confused tiny German flag-free harbour drawn in a thought bubble beside it, no people","another Hamburg!"),
 (3,8,"an empty sausage tray with a few crumbs and a sign 'NO MORE PORK', next to a pile of beef, no people",""),
 (3,9,SHOW(3),"contestant 3"),
 (3,10,"an old cook with a white beard and an apron in a small 1880s Texas town café, frying patties, a cowboy hat on a hook","Old Dave, Athens, Texas"),
 (3,11,SHOW(4),"contestant 4"),
 (3,12,"a man in 1890s clothes proudly putting a beef patty on a round yeast bun at a backyard grill in Oklahoma","Oscar Bilby, Tulsa, 1891"),
 (3,13,"a 1990s state governor at a podium signing an official proclamation with a hamburger drawn on it","1995: official!"),
 (3,14,"a crowd of the other contestants in old-fashioned clothes standing with arms crossed, unimpressed","nobody agreed"),
 (3,15,SHOW(5),"contestant 5"),
 (3,16,"a tiny old brick lunch shop in New Haven, Connecticut, around 1900, a hand-painted sign reading LOUIS LUNCH","Louis Lassen, 1900"),
 (3,17,"a man in 1900 clothes in a hurry, checking his pocket watch, while a cook hands him a beef patty between two slices of toast",""),
 (3,18,"a tiny old brick lunch shop seen from outside today, with a modern street around it, still open, warm light in the window, nobody visible inside, no people","still open"),
 (3,19,"a beef patty between two slices of toast on a paper plate, a little toast-shaped halo above it, no people","on toast!"),
 (3,20,"a ketchup bottle being politely stopped by a small hand-painted sign 'NO KETCHUP, THANK YOU', no people","no ketchup!"),
 (3,21,"five little light bulbs lighting up at the same time above five different small towns on an old map of the USA, no people","same idea, same time"),
 # p4 — The Jungle
 (4,0,"a hamburger with a dark storm cloud above it, no people","a problem"),
 (4,1,"a 1906 book with a dark green cover titled 'THE JUNGLE' lying on a desk next to a typewriter, a writer's round glasses beside it, no people","Upton Sinclair, 1906"),
 (4,2,"a rat sitting on a sack in a dark 1900s meat warehouse, no people",""),
 (4,3,"a dirty floor of an old meat factory with puddles and grime, no people",""),
 (4,4,"a sad sick cow lying in a muddy pen, flies around, no people",""),
 (4,5,"a huge steaming industrial iron vat in a dark 1900s factory, an old hand-painted wooden board on it reading DANGER in plain letters, no people, nothing gruesome","the vats"),
 (4,6,"a 1906 American family at breakfast reading the newspaper, all with horrified faces, one dropping a sausage from a fork",""),
 (4,7,"a chart on a wall with a line falling sharply, next to the US Capitol dome drawn small, no people","meat sales ↓  new laws"),
 (4,8,"a classic glass ketchup bottle wearing a tiny party hat, a calendar page reading 1906 beside it, no people","remember?"),
 (4,9,"a bowl of minced beef with a big red warning triangle sign stuck in it, no people","worst reputation"),
 (4,10,YOU+"in a straw boater hat peering through a big magnifying glass at a bowl of minced beef, a big question mark inside the lens","what's in there?"),
 (4,11,"an early 1900s horse-drawn lunch wagon at night, workers in caps buying plain beef patties in simple bread rolls from a window, no cheese, no lettuce, no sesame seeds",""),
 (4,12,"a lady and a gentleman in fancy 1910s clothes turning away from a plain beef patty in a simple bread roll on a plate (no cheese, no lettuce, no sesame seeds) with their noses in the air",""),
 (4,13,"a hamburger on a plate holding up a tiny white flag of help, no people","SOS"),
 # p5 — White Castle
 (5,0,"a small 1920s Kansas town street with early cars, a bright sunrise","Wichita, 1921"),
 (5,1,"two men in 1920s suits and hats shaking hands in front of a tiny white burger stand building shaped like a little castle with turrets","Anderson & Ingram"),
 (5,2,"a tiny white burger stand building shaped like a castle with small turrets, gleaming white and spotless, sparkles, no people","white = clean"),
 (5,3,"a 1920s cook in a spotless white uniform and white paper hat behind a gleaming counter",""),
 (5,4,"customers in 1920s clothes watching through a big window as a cook in white makes hamburgers on a griddle","see everything"),
 (5,5,"a single small burger with a 5-cent coin next to it, a price tag, no people","5¢"),
 (5,6,"a 1920s man happily carrying a paper bag overflowing with small burgers",""),
 (5,7,"a 1930 university laboratory with a doctor in a white coat holding a clipboard, a stack of small burgers on the table",""),
 (5,8,"a thin university student in a 1930 sweater sitting at a table with a tower of small burgers and a glass of water","1930"),
 (5,9,YOU+"in a straw boater hat staring in disbelief at a 1930 wall calendar with thirteen weeks crossed out, a small burger drawn on every day","13 weeks"),
 (5,10,"a thin university student in a 1930 sweater eating a small burger at breakfast with a newspaper, then at lunch, then at dinner by candlelight, three little scenes in a row",""),
 (5,11,"a doctor in a white coat giving the thumbs up to a smiling thin university student in a 1930 sweater, a stethoscope around his neck","healthy!"),
 (5,12,"a thin university student in a 1930 sweater with a slightly haunted smile and twitching eye, staring at one more small burger","...and his feelings?"),
 (5,13,"a small white castle-shaped burger stand next to a big hand-drawn number one, no people","first chain"),
 (5,14,SHOW(6),"contestant 6"),
 (5,15,"an old map of California with a little road leading to a sunny town and a small arrow, no people","California"),
 # p6 — McDonald's
 (6,0,"two adult brothers in their thirties, both grown men of the same height, in 1940 short-sleeved shirts, standing proudly in front of a small octagonal drive-in restaurant with a barbecue sign, palm trees","San Bernardino, 1940"),
 (6,1,"a 1940s waitress in a uniform carrying a tray of food to a customer sitting in a 1940 car",""),
 (6,2,"a long 1940s menu board with twenty five barbecue dishes listed, the text too small to read, no people","25 kinds of BBQ"),
 (6,3,"a pile of broken white plates and a few missing forks drawn as dotted outlines, no people","broken plates"),
 (6,4,"a 'CLOSED — BACK SOON' sign hanging on the door of a small 1948 drive-in, no people","1948"),
 (6,5,"a short 1948 menu board with only nine items: hamburger, cheeseburger, fries, three milkshakes, drinks, the text simple, no people","9 items"),
 (6,6,"a small white paper bag with a hamburger peeking out, a crossed-out plate beside it, no people",""),
 (6,7,"a 1940s waitress cap and an order pad crossed out with a red X, no people","no waitresses"),
 (6,8,"a 1948 fast food kitchen drawn like a factory assembly line, a conveyor of hamburgers, gears and arrows, cooks in white paper hats","assembly line"),
 (6,9,"three cooks in white paper hats side by side: one at a griddle, one at a fryer, one at a milkshake machine, each focused on one job",""),
 (6,10,YOU+"in a straw boater hat at a 1948 burger window holding a stopwatch showing 30 seconds and a hamburger with a 15-cent price tag, amazed","15¢ / 30 sec"),
 (6,11,"a cheerful little round-headed cartoon chef in a white paper hat running fast with a tray of hamburgers, speed lines, a sign 'SPEEDEE SERVICE'","Speedee"),
 (6,12,"a 1954 salesman in a suit and hat holding a catalogue of milkshake mixers, standing in front of a busy hamburger stand with a long queue","Ray Kroc, 1954"),
 (6,13,"a 1954 salesman in a suit with his jaw dropped and his hat flying off, staring at the long queue",""),
 (6,14,"a 1950s map of the USA dotted with dozens of tiny identical burger-stand icons, no people","everywhere"),
 (6,15,"a cheque for '$2,700,000' on a desk with a fountain pen, no people","1961"),
 (6,16,"a giant hamburger standing over the planet Earth like a rising sun, no people","next: the world"),
 # p7 — cheeseburger, global, Hamburg, ketchup
 (7,0,"three cartoon hamburgers in a row, each wearing a different hat: a cowboy hat, a beret, a chef's hat, no mirrors, no people","always changing"),
 (7,1,"a teenage cook in a 1920s diner in Pasadena dropping a slice of yellow cheese onto a sizzling patty, surprised face","Pasadena, 1920s"),
 (7,2,"a perfect cheeseburger with melting cheese in a spotlight, sparkles, no people","the cheeseburger"),
 (7,3,"a teenage cook in a 1920s diner apron winking at the viewer, holding a slice of cheese",""),
 (7,4,"a big 1950s burger in a paper wrapper with a small crown drawn on the wrapper, no logos, no people","1957: the Whopper"),
 (7,5,"a hamburger flying around the globe like a small airplane with a vapour trail, no people","global"),
 (7,6,"a long queue of people in 1990 winter coats and fur hats standing in the snow in Moscow, a modern burger restaurant ahead","Moscow, 1990"),
 (7,7,"a hamburger stand on the waterfront of modern Hamburg, Germany, with harbour cranes and the city behind it","hamburger in Hamburg"),
 (7,8,"a hamburger wearing a tiny American cowboy hat arriving with a suitcase at the Hamburg harbour, no people","import!"),
 (7,9,"a smiling man and woman from Hamburg in sailor caps, each wearing a name badge that says 'HAMBURGER'",""),
 (7,10,"a smiling man and woman in sailor caps, each with a name badge saying HAMBURGER, rolling their eyes at a tourist who points at their badges and laughs",""),
 (7,11,"a hamburger looking around lonely with a little question mark, no people","best friend?"),
 (7,12,"a classic glass ketchup bottle waving hello, no people","remember?"),
 (7,13,"a hamburger and a ketchup bottle hugging like best friends, little hearts above them, no people",""),
 # p8 — today and payoff
 (8,0,"a row of five different burgers: beef, chicken, fish, bean and a giant mushroom burger, no people","today"),
 (8,1,"a scientist in a white coat in a modern laboratory holding a petri dish with a tiny burger patty growing in it","2013: lab burger"),
 (8,2,"a tiny burger on a plate next to a huge stack of euro banknotes, no people","€250,000"),
 (8,3,"two food tasters in a modern studio chewing politely with slightly unconvinced faces, glasses of water ready","a little dry"),
 (8,4,SHOW(6),"so who?"),
 (8,5,"five old sepia portraits in oval frames hanging on a wall side by side, each a different 19th-century man shown head and shoulders only, a question mark above each","Charlie? Menches? Dave? Oscar? Louis?"),
 (8,6,"a big hand-drawn 'ALL OF THEM' rubber stamp imprint in red ink on plain paper, nothing else, no people, no animals",""),
 (8,7,"a big hand-drawn 'NONE OF THEM' stamp in red ink, no people",""),
 (8,8,"a timeline ribbon from left to right with simple objects only: a German frying pan, a fair ticket, a book titled 'THE JUNGLE', a small white castle and a stopwatch, no people","Hamburg → fair → Jungle → castle → speed"),
 (8,9,"an official-looking birth certificate with a lab burger drawn on it and a red wax seal, no people","birth certificate"),
 (8,10,YOU+"in a straw boater hat at the 1904 fair stand again, holding a hamburger and a pencil, voting on a little ballot","vote!"),
 (8,11,YOU+"in a straw boater hat pointing down at an empty speech bubble",""),
 (8,12,"a hamburger on a plate glancing sideways at a paper cone of golden fries next to it, no people",""),
 (8,13,"a paper cone of golden fries wearing a small French beret with a big question mark, no people","next: THE FRIES"),
]
NEG = " Anatomically correct people: every person has exactly two arms, two hands and five fingers per hand; no extra or floating limbs."
def prompt(i):
    p,l,d,n = SHOTS[i-1]
    note = f" Handwritten marker note + arrow: '{n}'." if n else " No other handwritten notes."
    people = "no people" not in d
    if "stick-figure" in d:
        note += " Stick figures = simple white round-headed stick figure with dot eyes, exactly two arms and two legs; it is the only stick figure."
    elif people: note += " No stick figures; all people drawn realistically."
    extra = " Only what is described: do not add extra people or objects. No brand logos."
    return STYLE + d + "." + note + extra + (NEG if people else "")
EXTRA = {}
if __name__ == "__main__":
    import collections
    c = collections.Counter(p for p,_,_,_ in SHOTS)
    L = {p: len(open(f"vo/p{p}.txt").read().strip().splitlines()) for p in range(9)}
    assert all(c[p] == L[p] for p in range(9)), (dict(c), L)
    for p in range(9): assert [l for q,l,_,_ in SHOTS if q==p] == list(range(L[p])), p
    print(len(SHOTS), "stick:", sum("stick-figure" in s[2] for s in SHOTS), "notes:", sum(bool(s[3]) for s in SHOTS), "no-people:", sum("no people" in s[2] for s in SHOTS))
