"""Промпты кадров «Жигули vs одноразовые» → prompts.json, shots.json и запросы generate_image_batch (work/kf_req_*.json).
Кадры KM3/KM4/KM6/KG3 и клип M_M3 берём из ../immortal бесплатно (см. timeline.py)."""
import json
MIKH_REF, DRIVER_REF, GARAGE_REF, YARD_REF, KOP_REF = ('87ee183f-9089-4c8d-bbe2-f2bdaec3c14c', '53a2bd70-7357-464a-9e4d-a32495b0d3ee',
    '23313f2f-6cbd-489b-b445-5159ade03183', '08996e99-8177-4b7d-8b13-c1ae3a50f7bb', '4964dd32-5310-4899-a047-99e9a68d23fb')
STYLE = ('Wide horizontal 16:9 frame in EXACTLY the same flat 2D cartoon style as the reference images (bold dark outlines, '
         'soft cel shading, warm saturated colours). ')
MIKH = ('the mechanic Mikhalych exactly as in reference image 1: a stocky man about fifty, broad round face, rosy cheeks, bushy dark '
        'eyebrows with grey, thick short grey-streaked beard, dark-navy baseball cap with an orange visor, a pencil behind his ear, '
        'light-blue denim bib overalls with full trouser legs over an orange short-sleeved T-shirt, a red checked rag in the overalls pocket')
END = (' Exactly two arms and two hands with five fingers for every person. No text, no letters, no numbers, no logos, no badges, '
       'no emblems, no number plates.')
KOP = 'a white 1970s VAZ-2101 "Kopeyka" Zhiguli sedan like the white car in the reference image (small boxy sedan, chrome bumpers, round double headlights)'
SEVEN = 'VAZ-2107 Zhiguli sedans (boxy 1980s Soviet sedans with a tall chrome grille and rectangular headlights)'
CROSS = 'a modern silver compact crossover SUV'
M, D, G, Y, K = 'M', 'D', 'G', 'Y', 'K'
F = [  # (имя, референсы, состав, промпт)
 ('KI1', [D, Y, K], ['driver'], f'The Russian courtyard of panel blocks from reference image 2 on a grey autumn day. In the centre a tow truck is loading {CROSS} with a broken-down look (hood slightly open, steam). Next to it the young driver from reference image 1 (short dark hair, black jacket) stands with his hands spread in frustration. On the right, {KOP} drives past happily, shiny and old.'),
 ('KI2', [M, K, G], ['mikhalych'], f'Inside a cosy garage workshop (grey corrugated metal wall, pegboard with tools, warm hanging lamp). {MIKH} leans on the open hood of {KOP}, chest-up, with a warm nostalgic smile at the viewer.'),
 ('KI3', [M, K, G], ['mikhalych'], f'Inside a garage workshop: {KOP} on the left and {CROSS} on the right stand nose to nose like rivals. Between them {MIKH} spreads his hands in a questioning gesture, eyebrows raised, looking at the viewer.'),
 ('KA1', [K], [], f'A 1970s Soviet car factory assembly line in a huge bright hall: a long row of identical small boxy Zhiguli sedans in white, beige, red and pale blue moving along the conveyor, workers in blue overalls far away, cranes and lamps overhead.'),
 ('KA2', [Y], [], f'The Russian courtyard of panel blocks from the reference image, sunny day: many old {SEVEN} in different faded colours (red, white, green, beige) parked in rows along the kerb, a cat on one roof. No people.'),
 ('KB1', [M, G], ['mikhalych'], f'Inside a garage workshop, {MIKH} reads a small old Soviet car owner manual booklet with a plain faded blue cover, his eyebrows shoot up in surprise; close medium shot.'),
 ('KB2', [K], [], 'A clean cartoon cutaway diagram of an old Soviet four-cylinder carburettor petrol engine: cast-iron block, camshaft on top driven by a chain, a round air filter on the carburettor, pistons and crankshaft visible; dark blue background, glowing outlines, educational style.'),
 ('KB3', [M, G], ['mikhalych'], f'Inside a garage workshop, {MIKH} holds up a worn engine camshaft with visibly worn rounded cams, squinting at it critically against the lamp light; close medium shot.'),
 ('KC1', [K], [], f'A huge car scrapyard: towering piles of rusty crushed old Zhiguli sedans and other Soviet cars, a yellow crane with a claw lifting a rusty car; in the clean foreground stands one shiny polished {KOP}; dramatic sunset sky.'),
 ('KC2', [K], [], f'A dark warehouse full of dim grey silhouettes of many old cars; a single bright spotlight from above lights one polished {KOP} in the middle, like a museum exhibit.'),
 ('KC3', [Y], [], 'A funny cartoon gag in a cosy village hallway: on a wooden shelf under a warm lamp stands one pair of shiny well-kept old leather boots like a trophy; next to it a big wicker basket overflowing with many torn worn-out boots with holes. No people.'),
 ('KC4', [M, K, G], ['mikhalych'], f'Inside a garage at night under a hanging lamp: {MIKH} lies on his back on a creeper half under {KOP}, only his legs, chest and happy face visible, a wrench in his hand, a toolbox nearby; cosy and familiar.'),
 ('KD1', [K], [], 'A clean cartoon cutaway of an old Soviet sedan seen from the side on a garage inspection pit: the engine stays in the car, the oil pan is removed and new piston rings and bearing shells are being fitted from below by a pair of hands with a wrench; dark blue glowing schematic background.'),
 ('KD2', [K], [], f'A 1980s Soviet car service station with a big garage door; a long queue of old {SEVEN} and other Zhiguli in faded colours waits outside along the road, the drivers chatting and smoking far away, overcast sky.'),
 ('KD3', [M, G], ['mikhalych'], f'Inside a garage workshop, {MIKH} holds a single new car tyre with both arms like a precious treasure, glowing sparkles around it, a proud and careful face; close medium shot.'),
 ('KD4', [Y], [], 'A row of Soviet brick garages in a garage cooperative on a sunny weekend: open doors, old Zhiguli inside, a pair of legs in work trousers sticking out from under one car, a man in a cap with a teapot on a stool, tools on the ground, cosy nostalgic mood.'),
 ('KE1', [M, G], ['mikhalych'], f'Inside a garage workshop, {CROSS} with its hood open; {MIKH} stands beside it with a thoughtful hand on his beard, looking into the compact engine bay full of plastic covers; medium shot.'),
 ('KE3', [Y], [], 'A funny cartoon comparison: on the left an old car exhaust pipe puffing a big thick cloud of dark smoke; on the right a modern car exhaust pipe with only a tiny transparent wisp and little green leaves around it; bright neutral background, no people.'),
 ('KE6', [Y], [], 'A dense city traffic jam on a wide multi-lane avenue at evening rush hour: rows of modern cars crawling bumper to bumper, red brake lights glowing, apartment blocks and street lights around, light snow. No readable signs.'),
 ('KE7', [M, Y], ['mikhalych'], f'A snowy courtyard on a frosty morning: a car battery with a sad cartoon face and a thermometer stuck in the snow showing deep cold; {MIKH} in a warm jacket over his overalls holds red and black jumper cables, smiling encouragingly; medium shot.'),
 ('KF2', [Y], [], 'A modern car factory: a bare grey steel car body hangs from an overhead conveyor and dips into a huge glowing bath of molten zinc for galvanization, sparks of silver splash, robotic arms around; dramatic industrial lighting, no people.'),
 ('KF3', [K], [], 'A car crash test laboratory: a white old boxy Soviet sedan with crumpled front end against a solid concrete test barrier, a yellow-and-black crash test dummy in the driver seat, bright studio lights, high-speed cameras on tripods; clinical, no blood, no injury.'),
 ('KF4', [Y], [], 'A modern Russian highway at golden hour: smooth asphalt with bright white markings, metal crash barriers in the middle, a few modern cars driving calmly, forest and fields along the road. No readable signs.'),
 ('KF5', [M, K, G], ['mikhalych'], f'Inside a garage workshop, {MIKH} stands next to {KOP} holding a very long paper chain of dozens of old Soviet pay envelopes that stretches across the whole floor to the car, amused face; medium shot.'),
 ('KG1', [M, G], ['mikhalych'], f'Inside a garage workshop, {MIKH} holds a small old ticking alarm clock up to his ear with a sceptical squint, one eyebrow raised, as if checking a conspiracy; close medium shot.'),
 ('KG2', [Y], [], 'A 1920s cartoon scene: a group of plump businessmen in old-fashioned suits and bowler hats sit around a round table under a single giant glowing incandescent light bulb, shaking hands conspiratorially; dark wood room, warm light. No real people, invented cartoon characters.'),
 ('KG3', [D, Y], ['driver'], f'The Russian courtyard of panel blocks from reference image 2: the young driver from reference image 1 (short dark hair, black jacket) stands next to {CROSS} with a thoughtful face, one hand holding a phone with a repair estimate (no readable text), the other scratching his head.'),
 ('KH3', [M, Y], ['mikhalych'], f'A self-service car wash in winter: {MIKH} in a warm jacket over his overalls crouches and sprays water with a pressure washer wand under the sill of {CROSS} covered with grey road salt and slush; steam and water splashes.'),
 ('KZ1', [M, K, Y], ['mikhalych'], f'The Russian courtyard of panel blocks at warm sunset: {MIKH} stands with his arms folded and a kind smile between a clean shiny {KOP} on the left and a clean {CROSS} on the right; medium-wide shot, cosy reconciliation mood.'),
]
REF = {M: MIKH_REF, D: DRIVER_REF, G: GARAGE_REF, Y: YARD_REF, K: KOP_REF}
prompts, shots, reqs = {}, {'frames': {}, 'clips': {}}, []
for i, (n, refs, cast, p) in enumerate(F, 1):
    if refs == [Y] and 'courtyard' not in p:
        p = 'Use the reference image ONLY as a sample of the drawing style, not of the place or objects. ' + p
    if refs == [K] and 'reference image' not in p:
        p = 'Use the reference image as a sample of the drawing style and of the old Zhiguli car design. ' + p
    text = STYLE + p + END
    prompts[n] = text; shots['frames'][n] = {'cast': cast}
    reqs.append(dict(index=i, params=dict(model='gpt_image_2_5', quality='medium', resolution='2k', aspect_ratio='16:9',
                                          medias=[dict(role='image_references', value=REF[r]) for r in refs], prompt=text)))
json.dump(prompts, open('prompts.json', 'w'), ensure_ascii=False, indent=1)
json.dump(shots, open('shots.json', 'w'), ensure_ascii=False, indent=1)
for b in range(0, len(reqs), 12):
    json.dump(reqs[b:b + 12], open(f'work/kf_req_{b // 12}.json', 'w'), ensure_ascii=False)
print(len(F), 'frames')
