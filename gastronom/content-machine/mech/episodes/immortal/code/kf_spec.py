"""Промпты кадров «10 неубиваемых машин» → prompts.json, shots.json и запросы generate_image_batch (work/kf_req_*.json)."""
import json
MIKH_REF, DRIVER_REF, GARAGE_REF, YARD_REF = ('87ee183f-9089-4c8d-bbe2-f2bdaec3c14c', '53a2bd70-7357-464a-9e4d-a32495b0d3ee',
                                             '23313f2f-6cbd-489b-b445-5159ade03183', '08996e99-8177-4b7d-8b13-c1ae3a50f7bb')
STYLE = ('Wide horizontal 16:9 frame in EXACTLY the same flat 2D cartoon style as the reference images (bold dark outlines, '
         'soft cel shading, warm saturated colours). ')
MIKH = ('the mechanic Mikhalych exactly as in reference image 1: a stocky man about fifty, broad round face, rosy cheeks, bushy dark '
        'eyebrows with grey, thick short grey-streaked beard, dark-navy baseball cap with an orange visor, a pencil behind his ear, '
        'light-blue denim bib overalls with full trouser legs over an orange short-sleeved T-shirt, a red checked rag in the overalls pocket')
END = (' Exactly two arms and two hands with five fingers for every person. No text, no letters, no numbers, no logos, no badges, '
       'no emblems, no number plates.')
CARS = {
 'buhanka': 'a Soviet UAZ-452 "Bukhanka" van: rounded loaf-shaped body, olive-green paint, round headlights, small side windows, high ground clearance',
 'niva': 'a classic Lada Niva 2121: small boxy three-door off-roader, beige paint, round headlights, black plastic grille',
 'logan': 'a first-generation Renault Logan sedan (2004-2012 shape): simple boxy budget sedan, silver paint',
 'corolla': 'a 1990s Toyota Corolla sedan (E100 generation shape), white paint',
 'camry': 'a 1990s Toyota Camry sedan (XV10 generation shape), dark cherry-red paint',
 'accord': 'a 1990 Honda Accord sedan (fourth generation shape, low flat hood, slim headlights), metallic blue paint',
 'ls400': 'a first-generation 1990s Lexus LS400 large luxury sedan, dark green paint',
 'lc80': 'a 1990s Toyota Land Cruiser 80 large boxy SUV, white paint, rectangular headlights',
 'lx470': 'a 2006 Lexus LX470 large luxury SUV (twin of the Land Cruiser 100), silver paint',
 'w124': 'a Mercedes-Benz W124 sedan (late 1980s E-class shape), cream-beige taxi colour, plain grille without any star emblem',
 'w115': 'an older 1970s Mercedes-Benz W115 sedan, black body with a yellow roof like an old Greek taxi, plain grille without any star emblem',
 'p1800': 'a red 1960s Volvo P1800 sports coupe (long hood, small tail fins, chrome bumpers)',
}
M, D, G, Y = 'M', 'D', 'G', 'Y'   # какие референсы: Михалыч, водитель, гараж, двор
F = [  # (имя, референсы, состав, промпт)
 ('KI1', [Y], [], f'A small cartoon planet Earth seen from space with a road running all the way around its equator, and {CARS["p1800"]} driving along that road, tiny speed lines, stars around, playful and bright.'),
 ('KI2', [M, G], ['mikhalych'], f'Inside a cosy garage workshop (grey corrugated metal wall, pegboard with tools, warm hanging lamp, stacked tyres, small window). {MIKH} leans on a long wooden workbench, chest-up, proud and smiling at the viewer. On the workbench in front of him stands a neat row of ten small toy model cars: an olive-green UAZ Bukhanka van, a beige Lada Niva, a silver budget sedan, a white taxi sedan, a white 1990s Corolla, a red 1990s Camry, a blue 1990s Accord, a dark-green 1990s Lexus sedan, a white Land Cruiser 80, a beige Mercedes W124.'),
 ('KI3', [Y], [], f'A Russian courtyard of Soviet panel apartment blocks on a sunny autumn day, exactly the place from the reference image. Parked in a row along the kerb: {CARS["buhanka"]}; {CARS["niva"]}; {CARS["w124"]}; {CARS["lc80"]}. Wide shot, no people.'),
 ('KA1', [Y], [], f'Hero shot: {CARS["buhanka"]} driving along a muddy country road through a green field, splashes of mud, birch trees, low three-quarter front view, big in the frame.'),
 ('KA2', [M], ['mikhalych'], f'In an open green field next to {CARS["buhanka"]} with its side door open, {MIKH} kneels inside the van cab where the engine cover between the two front seats is lifted, fixing the engine with a spanner, calm and confident, chest-up and close.'),
 ('KA3', [M], ['mikhalych'], f'{MIKH} lies on his back on a creeper under {CARS["buhanka"]} in a garage, pumping a grease gun into a suspension joint, a satisfied grin; side view of the van chassis with leaf springs.'),
 ('KB1', [], [], f'Hero shot: {CARS["niva"]} driving along a snowy village road between wooden houses, snow flying from the wheels, three-quarter front view, big in the frame.'),
 ('KB2', [M], ['mikhalych'], f'A village yard on a sunny weekend: {CARS["niva"]} is lifted on a red bottle jack with one wheel removed, {MIKH} crouches next to it holding a socket wrench, an open toolbox with spanners lies on the grass, relaxed and happy.'),
 ('KC1', [Y], [], f'{CARS["logan"]} parked in the Russian courtyard of panel blocks from the reference image, three-quarter front view, big in the frame, sunny day, no people.'),
 ('KC2', [], [], 'A clean cartoon cutaway diagram of a simple four-cylinder petrol engine: a heavy dark-grey cast-iron cylinder block, a lighter silver aluminium cylinder head, four pistons and connecting rods, a toothed timing belt on the front; dark blue background, glowing outlines, educational style.'),
 ('KC3', [M, G], ['mikhalych'], f'Inside a garage workshop, {MIKH} holds up a torn black toothed timing belt in one hand and a bent engine valve in the other, frowning and shaking his head; close medium shot.'),
 ('KD1', [], [], 'A Russian city taxi stand at night with glowing street lights: two compact budget sedans in taxi livery, one white and one yellow, each with a plain glowing taxi roof light with no letters; wet asphalt reflections, three-quarter front view, no people.'),
 ('KD3', [], [], 'A huge outdoor used-car market seen from above at an angle: long rows of many ordinary compact sedans and hatchbacks of different colours, a few sellers far away, sunny day.'),
 ('KD4', [M], ['mikhalych'], f'{MIKH} leans into the open driver door of a white compact sedan that used to be a taxi (worn shiny steering wheel, worn driver seat, a removed taxi roof light lying on the roof), shining a torch and squinting suspiciously; close medium shot.'),
 ('KE1', [Y], [], f'{CARS["corolla"]} parked in the Russian courtyard of panel blocks from the reference image, three-quarter front view, big in the frame, sunny, no people.'),
 ('KE2', [], [], 'A funny wide view: an endless parade of Toyota Corolla sedans of many different generations and colours (from 1960s to modern) driving in a long line that stretches to the horizon over green hills, bright sunny sky, no people visible.'),
 ('KE3', [M, G], ['mikhalych'], f'Inside a garage workshop, {MIKH} knocks with his knuckles on a heavy dark-grey cast-iron engine block standing on an engine stand, listening with a satisfied smile; close medium shot.'),
 ('KF1', [], [], f'{CARS["camry"]} on a country highway at golden hour, three-quarter front view, big in the frame.'),
 ('KF3', [], [], 'A funny cartoon gag: a cheerful old four-cylinder car engine with a happy face drawn on its valve cover drinks from a fuel can that pours petrol mixed with sand grains, tiny sparkles; garage background, playful.'),
 ('KF4', [], [], 'Extreme close-up of an old car instrument cluster: a mechanical odometer drum spinning backwards in a blur, a small screwdriver poking into the cluster from the side, a sneaky hand; the digits are motion-blurred and unreadable.'),
 ('KG1', [], [], f'{CARS["accord"]} driving along an American interstate highway through wide prairie, green road sign posts without any text, three-quarter front view, speed lines.'),
 ('KG2', [], [], f'At a car dealership in the USA, a happy grey-haired American man in a plaid shirt shakes hands with a smiling dealer in a suit and receives a set of car keys; behind them, {CARS["accord"]} with a big red bow on the roof; balloons; cheerful.'),
 ('KG3', [M, G], ['mikhalych'], f'Inside a garage workshop, {MIKH} pours golden fresh engine oil from a can into the engine of an open-hood car, a new oil filter in his other hand; careful and focused; close medium shot.'),
 ('KH1', [], [], f'{CARS["ls400"]} on a night city boulevard with warm street lights, three-quarter front view, glossy reflections, big in the frame.'),
 ('KH2', [M, G], ['mikhalych'], f'Inside a garage workshop, {MIKH} looks with a big magnifying glass at a clean silver V8 car engine on an engine stand, eyebrows raised in amazement; close medium shot.'),
 ('KJ1', [], [], f'Hero shot: {CARS["lc80"]} wading through a shallow taiga river among pine forest, water splashing, three-quarter front view, big in the frame.'),
 ('KJ2', [], [], 'A clean cartoon cutaway diagram of a big inline six-cylinder diesel engine: dark-grey cast-iron block and cast-iron cylinder head, six pistons in a row, a mechanical fuel injection pump on the side, no turbocharger; dark blue background, glowing outlines, educational style.'),
 ('KJ3', [], [], f'{CARS["lx470"]} on a wide Moscow avenue with Stalin-era buildings in the background, winter evening, city lights, three-quarter front view, big in the frame.'),
 ('KK1', [], [], f'{CARS["w124"]} with a plain taxi roof light (no letters) parked on a steep cobbled street of Porto, Portugal, with blue-and-white tiled house facades and the river in the distance, sunny, three-quarter front view.'),
 ('KK2', [], [], 'A clean cartoon cutaway diagram of a five-cylinder diesel car engine: dark-grey cast-iron block, five pistons in a row, a double-row timing chain on the front, a mechanical inline fuel injection pump; dark blue background, glowing outlines, educational style.'),
 ('KK3', [], [], f'Inside a bright modern car museum hall: {CARS["w124"]} with a plain taxi roof light stands on a raised round podium under spotlights; a few small visitors far in the background, seen from behind.'),
 ('KK4', [], [], f'{CARS["w115"]} driving along a sunny Greek seaside promenade with palm trees and white buildings, three-quarter front view, big in the frame.'),
 ('KM3', [], [], 'A funny cartoon comparison side by side: on the left a big relaxed car engine lying in a hammock sipping lemonade with a happy face; on the right a tiny engine with a big turbocharger sweating and straining with an exhausted face; bright background.'),
 ('KM4', [M, G], ['mikhalych'], f'Inside a garage workshop, {MIKH} stares in despair at the open engine bay of a modern car stuffed with a huge tangle of wires, connectors and electronic control boxes, scratching his head; close medium shot.'),
 ('KM6', [M], ['mikhalych'], f'Close shot: {MIKH} pokes his finger straight through a badly rusted car rocker panel full of holes and rust flakes on an old white SUV, grimacing; garage light.'),
 ('KM7', [M, D, G], ['mikhalych', 'driver'], f'Inside a garage workshop: an old white boxy 1990s Toyota Land Cruiser 80, heavily rusted at the bottom, stands on a two-post lift. On the left, the young driver from reference image 2 (short dark hair, black jacket) holds an empty open wallet, shocked. On the right, {MIKH} points at the rusty underbody, shrugging.'),
 ('KZ1', [M, Y], ['mikhalych'], f'The Russian courtyard of panel blocks from the reference image at warm sunset: {MIKH} stands with his arms folded, smiling, next to {CARS["niva"]} and {CARS["w124"]}; medium-wide shot, cosy mood.'),
]
REF = {M: MIKH_REF, D: DRIVER_REF, G: GARAGE_REF, Y: YARD_REF}
prompts, shots, reqs = {}, {'frames': {}, 'clips': {}}, []
for i, (n, refs, cast, p) in enumerate(F, 1):
    if not refs:   # без референса стиль плывёт: двор как образец рисовки, но не места
        refs = [Y]; p = 'Use the reference image ONLY as a sample of the drawing style, not of the place or objects. ' + p
    text = STYLE + p + END
    prompts[n] = text; shots['frames'][n] = {'cast': cast}
    reqs.append(dict(index=i, params=dict(model='gpt_image_2_5', quality='medium', resolution='2k', aspect_ratio='16:9',
                                          medias=[dict(role='image_references', value=REF[r]) for r in refs], prompt=text)))
json.dump(prompts, open('prompts.json', 'w'), ensure_ascii=False, indent=1)
json.dump(shots, open('shots.json', 'w'), ensure_ascii=False, indent=1)
for b in range(0, len(reqs), 12):
    json.dump(reqs[b:b + 12], open(f'work/kf_req_{b // 12}.json', 'w'), ensure_ascii=False)
print(len(F), 'frames;', [r['index'] for r in reqs][:3], '... names', [n for n, *_ in F])
