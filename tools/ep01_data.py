"""Single source of truth for episode 1, version 2 (after the 3 November script review).

Every block: id, scene title (ru), plate, sheets, hero look, five shots, audio, narration (en + ru).
build_ep01.py turns this into prompts, the narration script and the production board.
"""

LOOKS = {
    'home': 'HERO (scruffy guy, gray t-shirt, blue plaid pajama pants, barefoot, messy brown hair)',
    'interview': 'HERO (the same scruffy guy dressed for a job interview: white button-up shirt, thin dark tie, charcoal gray slacks, black and white sneakers, a black backpack on his back, messy brown hair)',
    'costume': 'HERO IN COSTUME (plain red hoodie with a small black marker spider on the chest and marker web on the hood, worn over a white shirt with a thin dark tie sticking out of the collar, hood up, round swim goggles with light blue lenses, charcoal gray slacks, black and white sneakers)',
    'costume_down': 'HERO IN COSTUME (plain red hoodie with a small black marker spider on the chest, hood down, round swim goggles pushed up on his forehead, white shirt collar and loosened tie showing, charcoal gray slacks, messy brown hair)',
    'none': None,
}
LOOK_NEG = {
    'home': 'the hero wearing the hoodie, goggles, shirt or tie',
    'interview': 'the hero wearing the hoodie or goggles, pajamas',
    'costume': '',
    'costume_down': '',
    'none': '',
}
PLATES = {
    '01_bedroom': 'the bedroom', '02_kitchen': 'the kitchen', '03_bathroom': 'the bathroom',
    '04_hallway': 'the apartment hallway with the front door', '05_yard': 'the suburban front yard',
    '06_suburb_street': 'the suburban street', '07_coffee_int': 'the coffee shop interior',
    '08_downtown_lamppost': 'the downtown sidewalk with a traffic light',
    '09_office_entrance': 'the office building glass entrance',
    '10_bus_street': 'the downtown street going downhill from left to right, the coffee shop with the green awning and a lamppost at the bottom',
    '11_living_night': 'the living room at night', '12_bedroom_night': 'the bedroom at night',
}
SHEETS = {
    'hero_home': 'hero_home', 'hero_interview': 'hero_interview', 'hero_costume': 'hero_costume',
    'dave': 'DAVE (roommate: big heavyset bald man with a thick dark-brown beard and small round glasses, navy bathrobe over gray t-shirt, blue plaid pajama pants, slippers, white mug, heavy-lidded calm eyes; he looks nothing like the hero)',
    'props': 'PROPS (black phone with yellow bell alarm, blue and white milk carton, white paper coffee cup with brown sleeve, swim goggles, red hoodie, brass door knob, white mug, black and white cat, web blob, pizza box)',
    'cast_secondary': 'SECONDARY CAST (elderly woman in purple coat and purple flowered hat, barista with hair bun and green apron, chubby bus driver with sandwich, police officer with notebook, neighbor in blue polo, TV reporter in purple blazer)',
}

# id, title_ru, plate, sheets (in order after the plate), look, shots, audio, vo_en, vo_ru
B = []
def blk(*a): B.append(dict(zip(['id','title','plate','sheets','look','shots','audio','vo_en','vo_ru'], a)))

# ---------------- ACT 1. HOME ----------------
blk('01','Просыпается на потолке, телефон прилип','01_bedroom',['hero_home','props'],'home',
 "SHOT 1 ECU: the hero's face upside down against the white ceiling, hair hanging, eyes snap open. HARD CUT. SHOT 2 WIDE from the doorway: the hero is stuck flat to the ceiling above the bed, arms and legs spread; he yanks one arm and it peels off with a stretch; the black and white cat below looks up. HARD CUT. SHOT 3 MEDIUM side: hanging by one hand he swings in an arc and falls flat onto the bed with a bounce. HARD CUT. SHOT 4 CU top-down nightstand: his hand grabs the black phone with the yellow bell alarm, a white web strand zips from his wrist and glues the phone to his palm. HARD CUT. SHOT 5 MEDIUM frontal: he sits up, holds the glued phone up, looks at it, then straight into the camera, deadpan; the cat does the same.",
 'sticky peel, bed thump, web zip, phone alarm, room tone.',
 "Today you woke up as Spider-Man. You know this because you're on the ceiling.",
 'Сегодня ты проснулся Человеком-пауком. Ты понял это, потому что висишь на потолке.')
blk('02','Телефон улетает на потолок до вечера','01_bedroom',['hero_home','props'],'home',
 "SHOT 1 CU: the hero shakes his hand hard; the black phone is glued to his palm by a big white sticky web blob, alarm ringing. HARD CUT. SHOT 2 MEDIUM: he flings his arm up, the phone tears loose with a stretching web strand and sticks to the white ceiling by a white web blob, still ringing. HARD CUT. SHOT 3 WIDE: he jumps under it with his arm stretched up and misses by a hand. HARD CUT. SHOT 4 CU: the black and white cat on the bed, slow blink. HARD CUT. SHOT 5 MEDIUM: he sits on the floor under the ringing phone on the ceiling and gives up.",
 'phone alarm, sticky tear, jump thud, sigh.',
 'Your phone is now also on the ceiling. It will stay there for the rest of the day.',
 'Твой телефон теперь тоже на потолке. И останется там до вечера.')
blk('03','Чутьё срабатывает на муху','01_bedroom',['hero_home','props'],'home',
 "SHOT 1 CU: a small fly lands on the windowsill. HARD CUT. SHOT 2 ECU: the hero's face, every hair on his head slowly stands up, eyes go wide. HARD CUT. SHOT 3 WIDE: he leaps from the floor and lands flat on the wall in a crouch like a spider. HARD CUT. SHOT 4 CU: the fly buzzes away out of the window. HARD CUT. SHOT 5 MEDIUM: he hangs on the wall, embarrassed; below, the black and white cat watches him, unimpressed.",
 'faint buzz, a high tingle sound, whoosh, wall thump, buzz fading.',
 'Spider-sense. In the movies it warns you about danger. Yours warns you about a fly.',
 'Паучье чутьё. В кино оно предупреждает об опасности. Твоё предупреждает о мухе.')
blk('04','Ванная, всё липнет к зеркалу','03_bathroom',['hero_home','props'],'home',
 "SHOT 1 MEDIUM over his shoulder: the hero stands at the sink, his back and shoulder big in the foreground, his sleepy face in the mirror; he pulls the red toothbrush out of the cup and it stays glued to his palm by a white web blob. HARD CUT. SHOT 2 CU side view of his hand: he flicks the hand hard, the red toothbrush flies off and splats onto the mirror glass with a white web blob. HARD CUT. SHOT 3 CU: his palm with the white soap bar glued to it by a white web blob; he shakes the hand, the soap stays on. HARD CUT. SHOT 4 CU on the mirror glass, no person in it: the red toothbrush, the yellow rubber duck and a blue shampoo bottle all stuck to the glass by white web blobs. HARD CUT. SHOT 5 MEDIUM over his shoulder: his real back in the foreground, his tired face in the mirror; he slowly raises both palms, the white soap bar still glued to one of them, white web strands dangling from both.",
 'sticky pop, wet splat on glass, sticky pop, soft thud, water drip.',
 'Everything you touch is yours now. Peeling it off does not count. You have to throw it.',
 'Всё, к чему ты прикасаешься, теперь твоё. Отлепить не считается. Надо выбросить.')
blk('05','Идёт по стене коридора','04_hallway',['hero_home'],'home',
 "SHOT 1 WIDE: he walks along the hallway wall sideways, body horizontal, bare feet on the wallpaper, carrying a towel, not noticing. HARD CUT. SHOT 2 CU: framed photos tilt under his bare feet. HARD CUT. SHOT 3 MEDIUM: he glances down, sees the floor below him, freezes. HARD CUT. SHOT 4 WIDE: he peels off the wall and drops to the floor on his back. HARD CUT. SHOT 5 CU: he lies on the floor looking up at the tilted photos, blinks.",
 'soft footsteps on wall, frames creak, thump.',
 'Walls are optional now. So are floors.',
 'Стены теперь по желанию. Полы тоже.')
blk('06','Дэйв варит кофе, герой ползёт по потолку','02_kitchen',['hero_home','dave'],'home',
 "SHOT 1 WIDE: Dave at the coffee maker pouring coffee into his white mug, eyes on the mug; the hero crawls in along the ceiling from the right. HARD CUT. SHOT 2 CU: Dave sips, eyes half closed, one eyebrow rises a millimeter. HARD CUT. SHOT 3 MEDIUM: the hero drops from the ceiling and lands on a stool at the island with a thump, hair bounces. HARD CUT. SHOT 4 CU: Dave's face, no reaction at all, another sip. HARD CUT. SHOT 5 MEDIUM two-shot: the hero gestures at the ceiling, Dave points at a sticky footprint on the wall with his mug.",
 'coffee pour, sip, stool thump, quiet kitchen.',
 'This is Dave. Dave has lived with you for three years. Nothing surprises Dave.',
 'Это Дэйв. Дэйв живёт с тобой три года. Дэйва ничем не удивить.')
blk('07','Реакция: ловит тосты в воздухе','02_kitchen',['hero_home','dave'],'home',
 "SHOT 1 CU: two slices of toast pop high out of a chrome toaster next to the coffee maker. HARD CUT. SHOT 2 MEDIUM in slow motion: without looking, the hero catches both slices in mid-air, one flat on each open palm. HARD CUT. SHOT 3 CU: his face, very proud of himself, hands out of frame. HARD CUT. SHOT 4 CU: Dave silently holds out his plate. HARD CUT. SHOT 5 MEDIUM: the hero puts the toast on Dave's plate; Dave eats it.",
 'toaster pop, slow-motion whoosh, soft catch, crunch.',
 'Spider reflexes. Finally, a power that is actually useful.',
 'Реакция паука. Наконец-то сила, от которой есть польза.')
blk('08','Пакет молока прилип','02_kitchen',['hero_home','dave','props'],'home',
 "SHOT 1 CU: the hero picks up the blue milk carton, it glues to his palm by a white web blob. HARD CUT. SHOT 2 CU: he grabs the yellow chips bag with the other hand, it glues too by a white web blob. HARD CUT. SHOT 3 MEDIUM: he sits at the island with the carton in one hand and the chips bag in the other, staring at the empty bowl. HARD CUT. SHOT 4 MEDIUM: Dave calmly takes the hero's wrist and tilts it, pouring milk from the glued carton into the bowl, blank face. HARD CUT. SHOT 5 MEDIUM: the hero shakes both hands, the carton and the chips bag drop off onto the counter; he eats a spoonful.",
 'sticky pops, milk pouring, two thuds, cereal crunch.',
 'It lasted four seconds.',
 'Это продлилось четыре секунды.')
blk('09','Цель дня: собеседование в десять','02_kitchen',['hero_home','dave'],'home',
 "SHOT 1 CU: a paper calendar on the fridge, one day circled in red with a small drawing of a necktie. HARD CUT. SHOT 2 ECU: the hero's face, cereal spoon frozen halfway, eyes going wide. HARD CUT. SHOT 3 CU: a round kitchen wall clock reading 9:05, the short hour hand pointing at 9 and the long minute hand pointing at 1. HARD CUT. SHOT 4 MEDIUM: the hero puts a finger to his lips and points at himself, then at the ceiling, miming nobody can know. HARD CUT. SHOT 5 CU: Dave nods once, deadpan, and raises his mug.",
 'clock ticking, spoon clink, tense silence, sip.',
 "Oh. Right. At ten you have a job interview. First one in a year. Rule one: nobody can know.",
 'Ах да. В десять у тебя собеседование. Первое за год. Правило первое: никто не должен знать.')
blk('10','Галстук прилип, завязывает Дэйв','04_hallway',['hero_interview','dave'],'interview',
 "SHOT 1 MEDIUM side view: the hero in a white shirt stands in front of the hallway mirror trying to tie a thin dark tie, his real body and his reflection both visible. HARD CUT. SHOT 2 CU: the tie sticks to his fingers and twists into a knot around his hand. HARD CUT. SHOT 3 MEDIUM: he shakes the hand, the tie stays wrapped around it like a bandage. HARD CUT. SHOT 4 MEDIUM: Dave steps in with his mug in one hand, unwraps the tie with the other and ties it properly on the hero's neck. HARD CUT. SHOT 5 CU: Dave pats the knot once, sips.",
 'fabric, sticky pull, quiet hallway, sip.',
 'Rule two: wear a tie. Rule three: let Dave tie it.',
 'Правило второе: галстук. Правило третье: завязывает Дэйв.')
blk('11','Дэйв даёт рюкзак с костюмом','04_hallway',['hero_interview','dave','props'],'interview',
 "SHOT 1 MEDIUM: Dave silently holds out a black backpack to the hero. HARD CUT. SHOT 2 CU top-down into the open backpack: a plain red hoodie with a fresh black marker spider drawn on the chest, and round swim goggles. HARD CUT. SHOT 3 CU: the hero looks up at Dave. HARD CUT. SHOT 4 CU: Dave holds up a black marker and caps it with a click. HARD CUT. SHOT 5 WIDE: the hero zips the backpack and puts it on his back; Dave walks back into the kitchen.",
 'zipper, marker cap click, zipper.',
 "Dave made you something. Just in case. You didn't ask how he knew.",
 'Дэйв кое-что тебе собрал. На всякий случай. Ты не спросил, откуда он знает.')
blk('12','Шнурки склеились','04_hallway',['hero_interview'],'interview',
 "SHOT 1 MEDIUM: the hero sits on the hallway floor in his shirt and tie tying his sneaker laces. HARD CUT. SHOT 2 CU: the laces stick to his fingers and to each other in a knot. HARD CUT. SHOT 3 CU: he pulls, the knot pulls both sneakers together. HARD CUT. SHOT 4 WIDE: he stands up and hops toward the door with both feet glued together. HARD CUT. SHOT 5 MEDIUM: he stops, breathes, rips the laces apart with a pop, nods to himself.",
 'laces, sticky pull, hopping thuds, pop.',
 'Nine twenty-two.',
 'Девять двадцать две.')
blk('13','Сила: ручка двери остаётся в руке','04_hallway',['hero_interview','dave','props'],'interview',
 "SHOT 1 WIDE: Dave in the kitchen doorway with his mug watches the hero walk to the front door. HARD CUT. SHOT 2 CU: the hero grips the brass door knob and turns it gently. HARD CUT. SHOT 3 CU: the knob crumples in his fist and snaps off the door. HARD CUT. SHOT 4 CU: he looks at the crushed knob, sets it carefully on the side table. HARD CUT. SHOT 5 WIDE: he pushes the door open with one finger; the door swings on its hinges on the side opposite the broken knob hole, and he walks out into the sunlight; the black and white cat sits by the side table.",
 'metal crunch, snap, door creak, birds.',
 'Spider strength. You opened a door. Technically.',
 'Паучья сила. Ты открыл дверь. Формально.')

# ---------------- ACT 2. CITY ----------------
blk('14','Сосед с воздуходувкой','05_yard',['hero_interview','cast_secondary'],'interview',
 "SHOT 1 WIDE: the hero walks along the sidewalk past the lawn trying to look casual; the neighbor in a blue polo shirt picks up the leaf blower. HARD CUT. SHOT 2 MEDIUM: the hero raises a hand to wave; a strand of white web zips out of his wrist. HARD CUT. SHOT 3 CU: the web splats onto the leaf blower, whips around the mailbox and the gnome, snaps tight. HARD CUT. SHOT 4 MEDIUM: the neighbor is tangled into the bundle, struggling, face red. HARD CUT. SHOT 5 WIDE: the hero gives a tiny apologetic wave and walks off fast.",
 'sneakers, web zip, wet splat, tight snap, birds.',
 "Say hi to the neighbor. Actually, don't.",
 'Поздоровайся с соседом. Хотя нет, не надо.')
blk('15','Кроссовок прилип к тротуару','06_suburb_street',['hero_interview'],'interview',
 "SHOT 1 WIDE: the hero walks fast down the sidewalk toward the camera. HARD CUT. SHOT 2 MEDIUM: a jogger passes, glances, keeps jogging. HARD CUT. SHOT 3 CU: his sneaker sticks to the pavement mid-step. HARD CUT. SHOT 4 MEDIUM: he pulls his foot out of the sneaker and stumbles forward in one sock. HARD CUT. SHOT 5 WIDE: a dog on a leash sits down next to the sneaker stuck on the sidewalk and looks at him.",
 'footsteps, jogger panting, sticky pop, stumble, dog sniff.',
 'The sidewalk is sticky now. Or you are.',
 'Тротуар теперь липкий. Или это ты.')
blk('16','Возвращает кроссовок','06_suburb_street',['hero_interview'],'interview',
 "SHOT 1 MEDIUM: he hops back on one foot to the stuck sneaker. HARD CUT. SHOT 2 CU: he tugs the sneaker, it peels off the pavement and sticks to his hand. HARD CUT. SHOT 3 MEDIUM: he hops on one foot trying to put it on while it is glued to his palm. HARD CUT. SHOT 4 CU: the dog tilts its head. HARD CUT. SHOT 5 WIDE: the sneaker finally pops off his hand onto his foot; he jogs away down the street.",
 'hopping, sticky pop, dog whine, footsteps.',
 'Nine thirty-one.',
 'Девять тридцать одна.')
blk('17','Пробует полететь на паутине, падает в кусты','06_suburb_street',['hero_interview'],'interview',
 "SHOT 1 MEDIUM: the hero stops under a big tree by the sidewalk, looks up at a branch, flexes his wrist like in the movies. HARD CUT. SHOT 2 CU: a web strand shoots up and sticks to the branch. HARD CUT. SHOT 3 WIDE: he jumps and swings forward on the strand, legs out, tie flying, heroic for one second. HARD CUT. SHOT 4 CU: the branch bends and snaps. HARD CUT. SHOT 5 WIDE: he lands face first in a hedge, legs sticking out, the branch on top of him.",
 'web zip, whoosh, wood snap, crash into leaves.',
 "You've seen this a thousand times in the movies. Your body hasn't.",
 'Ты видел это в кино тысячу раз. Твоё тело не видело ни разу.')
blk('18','Вылезает из кустов, почтальон','06_suburb_street',['hero_interview'],'interview',
 "SHOT 1 MEDIUM: the hero climbs out of the hedge with leaves stuck all over his shirt and tie. HARD CUT. SHOT 2 CU: he shakes himself like a wet dog, the leaves fly off in a cloud. HARD CUT. SHOT 3 WIDE: a mail carrier in a blue uniform with a mail bag walks past on the sidewalk, glances, keeps walking. HARD CUT. SHOT 4 CU: the mail carrier's face, polite nod. HARD CUT. SHOT 5 MEDIUM: the hero nods back, straightens his tie, walks on.",
 'rustling leaves, shake, footsteps, polite hum.',
 'Nobody notices. Nobody ever notices.',
 'Никто не замечает. Никто никогда не замечает.')
blk('19','Кофейня: ловит падающую полку с чашками','07_coffee_int',['hero_interview','props','cast_secondary'],'interview',
 "SHOT 1 MEDIUM: the hero at the counter, the barista in a green apron with a hair bun slides a white paper coffee cup with a brown sleeve toward him. HARD CUT. SHOT 2 WIDE: behind her a loaded wall shelf of white mugs breaks loose and starts to fall. HARD CUT. SHOT 3 MEDIUM fast: the hero vaults over the counter and fires web strands left and right, catching mug after mug in mid-air. HARD CUT. SHOT 4 WIDE: all the mugs hang in a neat row on white web strands under the shelf, swinging gently, not one broken. HARD CUT. SHOT 5 CU: the barista, one eyebrow raised, pushes the coffee cup toward him; he takes it, nods, and walks out.",
 'cup slide, wood crack, rapid web zips, porcelain clinks, gentle swinging.',
 'Coffee. You will carry this cup for the rest of the day. Remember it.',
 'Кофе. Ты будешь носить этот стакан весь день. Запомни его.')
blk('20','Чутьё на капучинатор: прыжок на потолок','07_coffee_int',['hero_interview','props','cast_secondary'],'interview',
 "SHOT 1 CU: the espresso machine's steam wand hisses loudly into a milk pitcher. HARD CUT. SHOT 2 ECU: the hero's face, hair slowly standing up. HARD CUT. SHOT 3 WIDE: he leaps straight up and sticks to the coffee shop ceiling on all fours, still holding the cup lump. HARD CUT. SHOT 4 CU: the barista looks up at him, no expression. HARD CUT. SHOT 5 MEDIUM: he drops down onto the floor and straightens his tie.",
 'loud steam hiss, high tingle, whoosh, ceiling thump, landing.',
 'Spider-sense, part two: the milk steamer.',
 'Паучье чутьё, часть вторая: капучинатор.')
blk('21','Платит монетами из банки с чаевыми','07_coffee_int',['hero_interview','props','cast_secondary'],'interview',
 "SHOT 1 CU: the barista slides a card reader toward him, deadpan. HARD CUT. SHOT 2 MEDIUM: he pats his empty pockets with the lump in one hand. HARD CUT. SHOT 3 CU: he looks up at the ceiling, remembering. HARD CUT. SHOT 4 CU: the barista takes two coins out of the glued tip jar and drops them in the register. HARD CUT. SHOT 5 CU: the hero peels the muffin and the tip jar off his cup and leaves them on the counter, keeping only the white paper coffee cup with the brown sleeve; he nods thank you.",
 'card reader beep, pockets patting, coins clink.',
 "Your wallet is in your phone. Your phone is on the ceiling.",
 'Кошелёк в телефоне. Телефон на потолке.')
blk('22','Сила: дверь кофейни снимается с петель','07_coffee_int',['hero_interview','props','cast_secondary'],'interview',
 "SHOT 1 MEDIUM: the hero pulls the coffee shop door gently to leave. HARD CUT. SHOT 2 CU: the door comes off its hinges in his hand. HARD CUT. SHOT 3 MEDIUM: he holds the whole door, the bell on top jingles. HARD CUT. SHOT 4 CU: the barista watches, no expression. HARD CUT. SHOT 5 WIDE: he leans the door neatly against the wall and walks out through the empty doorway with the white paper coffee cup.",
 'hinges cracking, bell jingle, door leaning.',
 'Spider strength, part two.',
 'Паучья сила, часть вторая.')
blk('23','Шляпа старушки, приклеил её к фонарю','10_bus_street',['hero_interview','cast_secondary','props'],'interview',
 "SHOT 1 WIDE: outside the coffee shop, a gust of wind lifts the elderly woman's purple flowered hat off her head. HARD CUT. SHOT 2 CU: the hero's eyes widen, he lunges and fires a web strand from his wrist. HARD CUT. SHOT 3 WIDE: the web catches the hat AND the woman and yanks them both against the lamppost at the bottom of the street, where they stick. HARD CUT. SHOT 4 CU low angle: the woman, hat back on, looks down at him with a slow stern stare. HARD CUT. SHOT 5 MEDIUM: the hero below spreads his arms in a helpless shrug.",
 'wind gust, web zip, thump on metal, street ambience.',
 "You tried to help. Remember this lady. You'll see her again.",
 'Ты хотел помочь. Запомни эту даму. Ты её ещё увидишь.')
blk('24','Сумочкой по очкам, уходит: опаздывает','10_bus_street',['hero_interview','cast_secondary','props'],'interview',
 "SHOT 1 CU: the hero's hands tug at the web on the woman, it stretches and snaps back. HARD CUT. SHOT 2 MEDIUM: her handbag swings and bonks him on the head. HARD CUT. SHOT 3 CU: he glances at a clock on the coffee shop wall, the hands at twenty to ten. HARD CUT. SHOT 4 MEDIUM: he holds up one finger to her, I will be back, and backs away. HARD CUT. SHOT 5 CU low angle: the woman on the lamppost, arms crossed, watches him go.",
 'elastic twang, soft bonk, clock tick, footsteps.',
 "You'll come back for her. Later. After the interview.",
 'Ты за ней вернёшься. Потом. После собеседования.')
blk('25','Прилип к светофору, голубь, коляска','08_downtown_lamppost',['hero_interview','props'],'interview',
 "SHOT 1 MEDIUM: the hero steps up to the traffic light pole to wait, leans on it; his cheek and free hand stick flat to the metal. HARD CUT. SHOT 2 CU: a pigeon lands on his head, settles in, blinks. HARD CUT. SHOT 3 WIDE: a woman pushing a stroller walks around him as if he were street furniture. HARD CUT. SHOT 4 CU: the pedestrian signal flips from the red hand to the white walking figure. HARD CUT. SHOT 5 MEDIUM: he rips himself off the pole with a stretchy pop, the pigeon flaps off, white paper coffee cup still in hand.",
 'sticky squelch, pigeon coo, stroller wheels, signal click, pop.',
 'Nine forty-four.',
 'Девять сорок четыре.')
blk('26','Реакция: ловит горшок, врезается в столб','08_downtown_lamppost',['hero_interview','props'],'interview',
 "SHOT 1 CU: a flowerpot slips off a balcony high above the sidewalk. HARD CUT. SHOT 2 MEDIUM in slow motion: without looking up, the hero catches the falling flowerpot in his free hand. HARD CUT. SHOT 3 CU: his face, extremely proud. HARD CUT. SHOT 4 MEDIUM: still looking at the flowerpot, he walks straight into a traffic light pole with a clang. HARD CUT. SHOT 5 CU: he rubs his forehead, sets the flowerpot down on a bench, walks on.",
 'scrape, slow-motion whoosh, soft catch, metal clang.',
 'Spider reflexes, part two. And then regular reflexes.',
 'Паучья реакция, часть вторая. А потом обычная.')
blk('27','Тем временем дома: Дэйв и холодильник','02_kitchen',['dave'],'none',
 "SHOT 1 MEDIUM: Dave alone at the fridge peels a long strand of white web off the door. HARD CUT. SHOT 2 CU: the web stretches like gum and will not come off his fingers. HARD CUT. SHOT 3 CU: he wipes his fingers on a pizza coupon, the coupon sticks. HARD CUT. SHOT 4 MEDIUM: he sticks the coupon back on the fridge with the web like a magnet. HARD CUT. SHOT 5 CU: he looks straight into the camera for one second and sips from his white mug.",
 'sticky stretch, paper, sip.',
 'Meanwhile, at home.',
 'Тем временем дома.')
blk('28','Офис, 9:58: поправляет галстук','09_office_entrance',['hero_interview','props'],'interview',
 "SHOT 1 WIDE: the hero arrives at the glass doors of the office building, slightly out of breath, white paper coffee cup in hand. HARD CUT. SHOT 2 CU over his shoulder: he and his reflection in the glass door; he straightens his tie. HARD CUT. SHOT 3 CU: a round clock on the lobby wall inside, the hands at two minutes to ten. HARD CUT. SHOT 4 MEDIUM: he takes a deep breath, eyes closed. HARD CUT. SHOT 5 CU: he smiles a tiny hopeful smile.",
 'city ambience, breathing, clock tick.',
 'Nine fifty-eight. You made it. Shirt, tie, coffee. You look almost normal.',
 'Девять пятьдесят восемь. Ты успел. Рубашка, галстук, кофе. Почти нормальный человек.')
blk('29','Охранник открывает дверь','09_office_entrance',['hero_interview'],'interview',
 "SHOT 1 MEDIUM: inside the glass lobby a security guard in a gray uniform looks up from his desk at the hero. HARD CUT. SHOT 2 CU: the guard nods and presses a button. HARD CUT. SHOT 3 CU: the glass door lock clicks open, a small green light turns on. HARD CUT. SHOT 4 CU: the hero reaches for the door handle, very carefully, with two fingers. HARD CUT. SHOT 5 MEDIUM: his fingers touch the handle.",
 'muffled lobby hum, buzz, lock click.',
 'This is the door to your new life.',
 'Это дверь в твою новую жизнь.')
blk('30','Тем временем: водитель и ручник','10_bus_street',['cast_secondary'],'none',
 "SHOT 1 WIDE side view: a yellow school bus parked at the top of the street; the chubby bus driver gets out holding a sandwich and leaves the door open. HARD CUT. SHOT 2 CU: inside the empty cab, the handbrake lever slowly clicks down by itself. HARD CUT. SHOT 3 CU: the driver takes a big bite of the sandwich, eyes closed, happy. HARD CUT. SHOT 4 WIDE side view: behind him the empty bus slowly starts to roll from left to right down the hill. HARD CUT. SHOT 5 MEDIUM: the driver opens his eyes, sees it, mouth full, freezes with the sandwich in his hand.",
 'engine idle, ratchet click, bite, tires rolling, gulp.',
 'Meanwhile, at the top of the hill, a man wants a sandwich.',
 'Тем временем наверху улицы человек хочет сэндвич.')
blk('31','Пустой автобус разгоняется','10_bus_street',[],'none',
 "SHOT 1 CU side view through the window of the rolling yellow school bus: the empty driver seat. HARD CUT. SHOT 2 CU: the steering wheel turns slowly by itself. HARD CUT. SHOT 3 CU: a soda can rattles in the cup holder. HARD CUT. SHOT 4 CU: the speedometer needle creeps up. HARD CUT. SHOT 5 WIDE side view: the empty bus picks up speed from left to right down the hill.",
 'rattling, creaking wheel, rising engine hum.',
 '', '')
blk('32','Выбор: дверь или автобус','09_office_entrance',['hero_interview'],'interview',
 "SHOT 1 ECU: the hero's face at the office door, his hair slowly stands up, eyes go wide. HARD CUT. SHOT 2 CU: in the glass of the door, the reflection of a yellow bus rolling past down the street behind him. HARD CUT. SHOT 3 CU: his fingers on the door handle, the lobby clock behind the glass at ten o'clock. HARD CUT. SHOT 4 CU: his face, looking at the door, then over his shoulder. HARD CUT. SHOT 5 MEDIUM: he lets go of the handle and turns away from the door.",
 'high tingle sound rising, bus rumble, clock tick, silence.',
 "And this time your spider-sense isn't about a fly.",
 'И в этот раз чутьё не про муху.')
blk('33','Переодевание за две секунды','09_office_entrance',['hero_interview','hero_costume','props'],'costume',
 "SHOT 1 CU: the hero swings the black backpack off his shoulder and rips the zipper open. HARD CUT. SHOT 2 MEDIUM: he pulls the red hoodie with the marker spider over his head on top of his shirt, the tie sticks out of the collar. HARD CUT. SHOT 3 CU: he snaps the round swim goggles over his eyes. HARD CUT. SHOT 4 CU: he pulls the hood up. HARD CUT. SHOT 5 WIDE: in costume, white paper coffee cup in hand, he turns and runs down the street to the right.",
 'zipper rip, fabric whoosh, goggle snap, running steps.',
 'Dave. You beautiful, weird man.',
 'Дэйв. Странный ты, прекрасный человек.')

# ---------------- ACT 3. RESCUE ----------------
blk('34','Догоняет автобус, паутина в бампер','10_bus_street',['hero_costume','cast_secondary','props'],'costume',
 "SHOT 1 WIDE side view: the empty yellow school bus rolls left to right down the hill; the bus driver with the sandwich runs after it on the left. HARD CUT. SHOT 2 MEDIUM: the hero in costume overtakes the driver, white paper coffee cup in his left hand. HARD CUT. SHOT 3 CU: the hero's right wrist raises, aiming. HARD CUT. SHOT 4 WIDE side view: a web line shoots and splats onto the rear bumper of the bus moving right. HARD CUT. SHOT 5 MEDIUM side view: the web line snaps taut, the hero grips it with both hands and leans back as it starts to pull him to the right.",
 'bus rumble, running, panting, web zip and splat, twang.',
 'The bus is rolling down the hill. At the bottom: the lady you glued to a lamppost.',
 'Автобус катится с горы. Внизу та самая дама, которую ты приклеил к фонарю.')
blk('35','Старушка на фонаре видит автобус','10_bus_street',['cast_secondary'],'none',
 "SHOT 1 CU: the elderly woman glued to the lamppost at the bottom of the hill hears a rumble and turns her head. HARD CUT. SHOT 2 WIDE side view from the sidewalk: far up the hill on the left, the yellow bus rolls down from left to right toward her lamppost on the right. HARD CUT. SHOT 3 MEDIUM: she tugs at the web with all her strength, it does not give. HARD CUT. SHOT 4 CU: her hat slides over one eye. HARD CUT. SHOT 5 CU: she grips her handbag and stares the bus down.",
 'rising bus rumble, straining, web creak.',
 '', '')
blk('36','Едет за автобусом на «водных лыжах»','10_bus_street',['hero_costume','props'],'costume',
 "SHOT 1 MEDIUM side view, camera tracks right, continuing from the start frame: the web line yanks the hero forward; he skids along the asphalt on his sneakers behind the bus like a water-skier, leaning back, the white paper coffee cup held high in his left hand. HARD CUT. SHOT 2 CU: his sneakers smoking on the asphalt. HARD CUT. SHOT 3 CU: his right hand grabs a passing parking meter and locks on. HARD CUT. SHOT 4 WIDE low angle: the parking meter bends to the right and tears out of the sidewalk. HARD CUT. SHOT 5 MEDIUM side view, camera tracks right: he lets go of the meter, it clatters away behind him, and he keeps skidding behind the bus moving right.",
 'skidding, metal groan, concrete crack, clatter.',
 'In the movies he swings. You water-ski.',
 'В кино он летает на паутине. Ты едешь на водных лыжах.')
blk('37','Запрыгивает на крышу автобуса','10_bus_street',['hero_costume','props'],'costume',
 "SHOT 1 MEDIUM side view, camera tracks right, continuing from the start frame: the hero pulls himself along the web line, springs up and lands in a crouch on the roof of the bus moving right, white paper coffee cup upright. HARD CUT. SHOT 2 CU: his goggles, he looks ahead to the right, eyes narrow. HARD CUT. SHOT 3 MEDIUM tracking: he runs forward along the roof. HARD CUT. SHOT 4 CU: he stops and raises his wrist, thinking. HARD CUT. SHOT 5 MEDIUM side view, camera tracks right: he crouches on the roof and raises his wrist toward the buildings on the left, eyes focused behind the goggles.",
 'landing thump, running on metal, wind, heartbeat.',
 'Think. Not like in the movies. Like you.',
 'Думай. Не как в кино. Как ты.')
blk('38','Промах: паутина утащила зонт хот-догов','10_bus_street',['hero_costume','props'],'costume',
 "SHOT 1 MEDIUM side view, camera tracks right, continuing from the start frame: crouched on the roof of the bus moving right, he fires a web strand up-left. HARD CUT. SHOT 2 CU: the web strand misses the building and sticks to a hot dog cart umbrella on the sidewalk. HARD CUT. SHOT 3 WIDE: the umbrella is yanked off the cart and flies after the bus like a kite. HARD CUT. SHOT 4 CU: the hot dog vendor holds a hot dog in tongs, staring. HARD CUT. SHOT 5 MEDIUM: the hero cuts the strand, the umbrella floats away, he aims again.",
 'web zip, umbrella whoosh, flapping, focused breath.',
 'Close.',
 'Почти.')
blk('39','Автобус всё ближе к старушке','10_bus_street',['hero_costume','cast_secondary'],'costume',
 "SHOT 1 WIDE side view: the bus with the hero on its roof speeds down the hill from left to right toward the lamppost. HARD CUT. SHOT 2 CU: the elderly woman on the lamppost, eyes wide. HARD CUT. SHOT 3 CU: the hero on the roof sees her ahead. HARD CUT. SHOT 4 CU: the woman closes her eyes. HARD CUT. SHOT 5 CU: the hero sets his jaw and raises both wrists.",
 'bus roaring, wind, heartbeat, silence for one beat.',
 '', '')
blk('40','Сеть между домами, автобус останавливается','10_bus_street',['hero_costume','cast_secondary','props'],'costume',
 "SHOT 1 WIDE low angle: the hero fires web strand after strand left and right, a big white web net builds across the street in front of the lamppost. HARD CUT. SHOT 2 WIDE side view: the bus moving right plows into the net, the net stretches deep like a trampoline. HARD CUT. SHOT 3 WIDE side view: the net springs back and the bus stops half a meter from the woman on the lamppost. HARD CUT. SHOT 4 CU: the hero on the roof looks at the white paper coffee cup in his hand; the coffee sloshes once and settles, not a drop spilled. HARD CUT. SHOT 5 MEDIUM: he hops off the roof and his own web glues him flat to the side of the bus, where he hangs, cup upright, blinking.",
 'web zips, deep elastic twang, brake squeal, tiny slosh, sticky slap.',
 'And not a single drop.',
 'И ни капли.')
blk('41','Старушка нос к носу с автобусом, кивает','10_bus_street',['hero_costume','cast_secondary'],'costume',
 "SHOT 1 CU: the elderly woman opens her eyes, face to face with the bus grille, half a meter away. HARD CUT. SHOT 2 CU: she slowly looks up at the hero glued to the side of the bus. HARD CUT. SHOT 3 CU: the hero, glued, gives a small awkward wave. HARD CUT. SHOT 4 CU: her face softens a millimeter, she gives one approving nod. HARD CUT. SHOT 5 WIDE: the two of them stuck in place, the net sagging between the buildings.",
 'engine ticking, quiet, a small wave rustle.',
 '', '')
blk('42','В кофейне никто не поднял глаз','07_coffee_int',['cast_secondary'],'none',
 "SHOT 1 MEDIUM from inside the coffee shop: the barista behind the counter looks up from her phone as the yellow nose of the bus wrapped in web fills the front window. HARD CUT. SHOT 2 CU: her face, one eyebrow, back to the phone. HARD CUT. SHOT 3 WIDE: customers at tables glance up, then back to their laptops. HARD CUT. SHOT 4 CU: a muffin in the pastry case wobbles and settles. HARD CUT. SHOT 5 MEDIUM: the barista wipes the counter.",
 'muffled thud through glass, espresso machine, quiet chatter.',
 'Inside the coffee shop, nobody looks up.',
 'В кофейне никто не поднял глаз.')
blk('43','Водитель и полицейский','10_bus_street',['hero_costume','cast_secondary'],'costume',
 "SHOT 1 WIDE: the bus driver with the sandwich arrives panting, stares at the net. HARD CUT. SHOT 2 MEDIUM: a police officer with a notebook walks up, looks at the hero glued to the bus. HARD CUT. SHOT 3 CU: the officer's tired skeptical face, pencil raised. HARD CUT. SHOT 4 CU: the hero, still glued, gives a small nod. HARD CUT. SHOT 5 MEDIUM: the officer writes, looks at the bent parking meter up the street, writes more.",
 'panting, pencil scratch, distant siren.',
 "Here's how the city will remember today.",
 'Вот каким город запомнит этот день.')
blk('44','Репортёр берёт интервью у водителя','10_bus_street',['hero_costume','cast_secondary'],'costume',
 "SHOT 1 WIDE: a TV reporter with a microphone and a cameraman interview the bus driver in the foreground; the hero glued to the bus is a small figure in the background. HARD CUT. SHOT 2 CU: the driver talks and shrugs, sandwich in hand. HARD CUT. SHOT 3 MEDIUM: the cameraman pans past the hero without stopping. HARD CUT. SHOT 4 CU: the hero peels one arm free and waves weakly at the camera. HARD CUT. SHOT 5 WIDE: the reporter and cameraman walk away.",
 'crowd murmur, camera click, wind.',
 '', '')
blk('45','Толпа аплодирует водителю','10_bus_street',['hero_costume','cast_secondary'],'costume',
 "SHOT 1 MEDIUM: a small crowd gathers on the sidewalk around the bus stopped in the web net. HARD CUT. SHOT 2 WIDE: the bus driver steps forward in front of the bus, the crowd starts clapping for him. HARD CUT. SHOT 3 CU: the driver, surprised, takes a small bow. HARD CUT. SHOT 4 CU: the hero, glued to the side of the bus behind the crowd, blinks. HARD CUT. SHOT 5 MEDIUM: the driver shakes hands with people, the hero in the background gives a thumbs up to nobody.",
 'crowd murmur, applause, cheers.',
 'Hero of the day. The bus driver. Twenty-two years of service.',
 'Герой дня. Водитель автобуса. Двадцать два года стажа.')
blk('46','Отлипает от автобуса, 10:41','10_bus_street',['hero_costume'],'costume',
 "SHOT 1 WIDE: the street is empty now, the hero still glued to the side of the bus. HARD CUT. SHOT 2 CU: he peels one arm off with a long sticky stretch. HARD CUT. SHOT 3 CU: he peels his hood off the bus, his messy hair pops out. HARD CUT. SHOT 4 MEDIUM: he drops to the sidewalk, the white paper coffee cup still upright. HARD CUT. SHOT 5 CU: he looks up the street toward the office building far away, then at the lamppost.",
 'long sticky peels, thud, evening wind.',
 'Ten forty-one.',
 'Десять сорок одна.')
blk('47','Отклеивает старушку, уходят вместе','10_bus_street',['hero_costume','cast_secondary'],'costume',
 "SHOT 1 MEDIUM: he pulls the web off the lamppost, the elderly woman still wrapped. HARD CUT. SHOT 2 CU: she drops into his arms, then the web glues her to his side. HARD CUT. SHOT 3 CU: both look at the web joining them, then at each other. HARD CUT. SHOT 4 WIDE: they walk off together down the sunset sidewalk in step, glued at the side, long shadows. HARD CUT. SHOT 5 CU from behind: her hand pats his shoulder once.",
 'web peel, two sets of footsteps, evening birds.',
 'You came back for her. Just later than you planned.',
 'Ты за ней вернулся. Просто позже, чем собирался.')

# ---------------- ACT 4. EVENING ----------------
blk('48','Диван, горошек на спину','11_living_night',['hero_costume','dave'],'costume_down',
 "SHOT 1 MEDIUM: the hero lies face down on the green couch, hood down, groaning. HARD CUT. SHOT 2 CU: Dave puts a bag of frozen peas on the hero's back. HARD CUT. SHOT 3 CU: the bag sticks to the hoodie. HARD CUT. SHOT 4 MEDIUM: Dave sits down in the armchair, sips from his mug, watches TV. HARD CUT. SHOT 5 CU: the hero gives a muffled thumbs up from the cushion.",
 'groan, crinkle of the frozen bag, sticky pat, TV murmur, sip.',
 'Everything hurts. Even the peas.',
 'Болит всё. Даже горошек.')
blk('49','Новости: он на заднем плане','11_living_night',['hero_costume','dave','props'],'costume_down',
 "SHOT 1 WIDE: the hero and Dave slump side by side on the green couch with game controllers, TV glow on them. HARD CUT. SHOT 2 CU on the TV: a news report shows the yellow bus in a web net with a tiny red figure stuck to its side. HARD CUT. SHOT 3 CU: Dave's eyes slide sideways toward the hero without his head moving. HARD CUT. SHOT 4 MEDIUM: the hero reaches for the controller, a web strand snaps it up and glues it over his face. HARD CUT. SHOT 5 MEDIUM two-shot: the hero sits with the controller on his face, Dave slowly sips, the cat on the armrest blinks.",
 'controller clicks, muffled TV, web zip, plastic slap, sip.',
 "On the news, you're the guy in the background.",
 'В новостях ты парень на заднем плане.')
blk('50','Письмо: выбрали другого','11_living_night',['hero_costume','dave'],'costume_down',
 "SHOT 1 CU: Dave's phone lights up on the coffee table with an envelope icon. HARD CUT. SHOT 2 CU: Dave reads it, eyebrows up a millimeter. HARD CUT. SHOT 3 MEDIUM: he turns the phone to the hero. HARD CUT. SHOT 4 CU: the hero's face, the hope slowly draining. HARD CUT. SHOT 5 MEDIUM two-shot: Dave pats the hero's knee twice and hands him a slice of pizza.",
 'phone buzz, quiet, two pats, box creak.',
 'The email came at six. They went with another candidate.',
 'Письмо пришло в шесть. Они выбрали другого кандидата.')
blk('51','Дэйв ведёт список','02_kitchen',['dave'],'none',
 "SHOT 1 MEDIUM: Dave alone in the dark kitchen at night writes on a notepad by the light of the open fridge. HARD CUT. SHOT 2 CU: the notepad, a long list, he adds one more line. HARD CUT. SHOT 3 CU: he tears off the page. HARD CUT. SHOT 4 MEDIUM: he sticks the page on the fridge next to the web, it sticks instantly. HARD CUT. SHOT 5 CU: he looks at the camera for one second and closes the fridge, darkness.",
 'pen scratch, paper tear, fridge hum, door close.',
 'Dave is keeping a list. Dave is always keeping a list.',
 'Дэйв ведёт список. Дэйв всегда ведёт список.')
blk('52','Ложится спать, телефон всё ещё на потолке','12_bedroom_night',['hero_home','props'],'home',
 "SHOT 1 WIDE: the hero in his t-shirt and pajama pants climbs into bed; the red hoodie hangs on a hook on the open bedroom door. HARD CUT. SHOT 2 CU: he looks up at the ceiling where the black phone with the yellow bell still hangs by a web. HARD CUT. SHOT 3 MEDIUM: he pulls the blanket up, it sticks to his hands, he gives up and lies under a tented blanket. HARD CUT. SHOT 4 CU: the cat settles on the nightstand, watches him. HARD CUT. SHOT 5 WIDE: lights off, moonlight through the blinds, he closes his eyes.",
 'bed creak, blanket rustle, cat settling, quiet night.',
 'You told yourself it was one weird day.',
 'Ты сказал себе, что это был просто странный день.')
blk('53','Чутьё: настоящий сигнал','12_bedroom_night',['hero_home','props'],'home',
 "SHOT 1 CU: the hero asleep, mouth open, the black and white cat curled on his chest. HARD CUT. SHOT 2 CU: the black phone hanging from the ceiling by a web lights up with a notification glow. HARD CUT. SHOT 3 CU: the hero's eyes snap open, every hair on his head slowly stands up. HARD CUT. SHOT 4 MEDIUM: far outside the window, red and blue police lights flicker on the buildings. HARD CUT. SHOT 5 MEDIUM: he sits up and looks at the red hoodie hanging on the hook on the open bedroom door.",
 'soft snore, phone buzz from above, a faint high tingle, distant siren.',
 'Your spider-sense disagrees.',
 'Твоё чутьё не согласно.')
blk('54','Дэйв: пустая кровать, окно открыто','12_bedroom_night',['dave','props'],'none',
 "SHOT 1 WIDE from inside the dark bedroom: Dave appears in the doorway in his bathrobe, mug in hand. HARD CUT. SHOT 2 MEDIUM: the bed is empty, the hook on the bedroom door is empty, the window is wide open, the blinds swaying. HARD CUT. SHOT 3 CU: a strand of white web stretches from the window frame out into the night. HARD CUT. SHOT 4 CU: Dave takes a long sip. HARD CUT. SHOT 5 MEDIUM: he closes the window, the web strand snaps, he walks away; the cat watches from the bed.",
 'floor creak, wind, sip, window click, distant siren.',
 'Day two starts tonight.',
 'Второй день начинается сегодня ночью.')

# ---------------- v3 restructure (3 Nov): less sticking, threat earlier, longer chase ----------------
blk('38a','Пролетает сквозь кофейню и обратно','10_bus_street',['hero_costume','cast_secondary','props'],'costume',
 "SHOT 1 WIDE side view: the yellow bus with the hero crouched on its roof roars left to right past the coffee shop. HARD CUT. SHOT 2 MEDIUM: the hero swings off the roof on a web line through the open doorway of the coffee shop. HARD CUT. SHOT 3 CU inside: the barista with the hair bun looks up from her phone as he whooshes past the counter. HARD CUT. SHOT 4 MEDIUM: he swings back out through the doorway, a fresh muffin now in his mouth, white paper coffee cup still upright. HARD CUT. SHOT 5 WIDE side view: he lands back on the roof of the bus moving right.",
 'bus roar, whoosh in, bell jingle, whoosh out, roof thump.',
 'Breakfast. Technically.',
 'Завтрак. Формально.')
blk('38b','Перекрёсток: машины уворачиваются','10_bus_street',['hero_costume','props'],'costume',
 "SHOT 1 WIDE high angle: the driverless yellow bus moving left to right runs a red light at an intersection; cars brake and swerve. HARD CUT. SHOT 2 CU: a taxi driver covers his eyes. HARD CUT. SHOT 3 MEDIUM: the hero on the roof fires a web line at the traffic light pole and pulls, the bus tilts and squeezes between two cars. HARD CUT. SHOT 4 CU: the side mirror of a car folds in with a click as the bus passes. HARD CUT. SHOT 5 WIDE side view: the bus continues left to right down the hill, the hero still on the roof, coffee cup upright.",
 'horns, screeching brakes, web zip, mirror click, bus roar.',
 'Red light. Nobody is driving. Nobody is stopping.',
 'Красный свет. За рулём никого. Никто не тормозит.')
blk('38c','Мусорный бак и голуби','10_bus_street',['hero_costume','props'],'costume',
 "SHOT 1 MEDIUM tracking right: the hero on the roof of the bus moving right sees a green dumpster in the path. HARD CUT. SHOT 2 CU: he fires two web lines at the dumpster. HARD CUT. SHOT 3 WIDE side view: he yanks the dumpster out of the way just before the bus hits it, it rolls onto the sidewalk. HARD CUT. SHOT 4 CU: a flock of gray pigeons explodes off the dumpster lid. HARD CUT. SHOT 5 MEDIUM: the hero on the roof spits out a feather, still holding the coffee cup upright.",
 'bus roar, web zips, heavy metal roll, wings flapping, a small pfft.',
 '', '')
blk('38d','Замедление: старушка и прыжок','10_bus_street',['hero_costume','cast_secondary'],'costume',
 "SHOT 1 WIDE side view in slow motion: the bus moving left to right is only a few car lengths from the lamppost at the bottom of the hill. HARD CUT. SHOT 2 CU slow motion: the elderly woman glued to the lamppost, her purple hat lifting in the wind. HARD CUT. SHOT 3 MEDIUM slow motion: the hero leaps off the front of the bus roof into the air, arms wide. HARD CUT. SHOT 4 CU slow motion: his goggles reflect the lamppost and the woman. HARD CUT. SHOT 5 WIDE slow motion: he hangs in the air over the street between the bus and the woman, wrists aimed at the buildings on both sides.",
 'everything slows: deep heartbeat, stretched wind, a single high tone.',
 "Four hours ago you couldn't hold a phone.",
 'Четыре часа назад ты не мог удержать телефон.')

blk('24a','Вор с сумкой: паутина не глядя','10_bus_street',['hero_interview','props'],'interview',
 "SHOT 1 WIDE side view: on the busy sidewalk a man in a black hoodie snatches a woman's red handbag and sprints left to right past the hero. HARD CUT. SHOT 2 CU: the hero, still in shirt and tie, glances at his wrist watch, does not look up. HARD CUT. SHOT 3 CU: without looking he flicks his wrist sideways, a web strand zips out. HARD CUT. SHOT 4 WIDE side view: the thief is yanked off his feet and glued flat to a bus stop bench by a big white web blob, the red handbag dangling from the web. HARD CUT. SHOT 5 MEDIUM: the hero keeps walking right, adjusting his tie, as if nothing happened; behind him people stare at the glued thief.",
 'running steps, a shout, web zip, thump on the bench, street ambience.',
 'Rule one: nobody can know. Rule one is already in trouble.',
 'Правило первое: никто не должен знать. У правила первого уже проблемы.')
blk('38e','Велосипедист на пути автобуса','10_bus_street',['hero_costume','props'],'costume',
 "SHOT 1 WIDE side view: a delivery cyclist with a big pizza box pedals across the street right in front of the bus moving left to right. HARD CUT. SHOT 2 CU: the cyclist's face, earbuds in, sees nothing. HARD CUT. SHOT 3 MEDIUM: the hero on the bus roof fires a web line and lifts the cyclist, bike and all, into the air. HARD CUT. SHOT 4 WIDE: the bus passes under the dangling cyclist. HARD CUT. SHOT 5 MEDIUM: the hero lowers him gently onto the sidewalk behind the bus; the cyclist keeps pedaling in the air for a second, then rides off.",
 'bus roar, bicycle bell, web zip, whoosh, soft landing, tires.',
 '', '')

DROP = {'08', '12', '17', '18', '20', '21', '22', '25', '26', '27', '29'}
ORDER = ['01','02','03','04','05','06','07','09','10','11','13','14','15','16','19',
         '30','31','23','24','24a','28','32','33','34','35','36','37','38','38a','38b','38e','38c','38d','39','40','41',
         '42','43','44','45','46','47','48','49','50','51','52','53','54']
_by = {b['id']: b for b in B}
B[:] = [_by[i] for i in ORDER]

INSERTS = [
    ('после 00', 'Крючок 0:00 - 0:04: три кадра из блока 40, автобус в сети, герой с целым кофе. Рассказчик: «In four hours you will stop a bus and not spill a drop. But first, you need to get off the ceiling.»'),
    ('после 02', 'Титр серии «What If You Woke Up as SPIDER-MAN?», 3 секунды.'),
    ('после 09', 'Календарь: «DAY 1 · 9:05 AM · Interview at 10:00».'),
    ('после 17', '«Фильм против реальности»: в кино он летит на паутине между небоскрёбами, ты лежишь лицом в кустах.'),
    ('после 46', 'Календарь: «10:41 AM · Interview: missed».'),
    ('после 54', 'Карточка следующей серии «DAY 2 as SPIDER-MAN» и призыв подписаться.'),
]

CHAIN = {'36': '34', '37': '36', '38': '37'}  # block -> block whose last frame is the start frame
for b in B:
    b['chain_from'] = CHAIN.get(b['id'])
