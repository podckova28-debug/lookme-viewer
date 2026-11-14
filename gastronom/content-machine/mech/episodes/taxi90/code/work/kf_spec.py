"""Кадры «Ты — таксист 90-х»: gpt_image_2_6 low 1k 16:9 (0,25 кр). → ../prompts.json, ../shots.json, kf_req_<n>.json (партии по 12).
Герой-таксист — реф. 155ce53e (эталон, 14 нояб); Михалыч — 87ee183f; гараж 23313f2f, двор 08996e99 (образец стиля).
Марок нет: машины без логотипов («generic, no badges»). Цифры на экране — только графикой кодом, на кадрах ни цифр, ни текста.
Возраст героя: 1992 — около 30; 2000-е — около 40; 2010-е — около 50; 2020-е — около 60 (седые усы)."""
import json, os
D = os.path.dirname(os.path.abspath(__file__))
HERO, MIKH, GAR, YARD = '155ce53e-b48d-41f9-8128-412289224060', '87ee183f-9089-4c8d-bbe2-f2bdaec3c14c', '23313f2f-6cbd-489b-b445-5159ade03183', '08996e99-8177-4b7d-8b13-c1ae3a50f7bb'
STYLE = 'Wide horizontal 16:9 frame in EXACTLY the same flat 2D cartoon style as the reference images (bold dark outlines, soft cel shading, warm saturated colours). '
END = ' Exactly two arms and two hands with five fingers each per person. No text, no letters, no numbers, no logos, no brand names, no number plates.'
_H = 'the taxi driver exactly as the man in reference image 1 (same face, thick moustache, grey flat cap'
H90 = _H + ', about thirty, dark-brown hair and dark moustache, worn brown leather jacket over a grey ribbed sweater)'
H00 = _H + ', now about forty, dark moustache, a dark-grey padded jacket over a grey sweater)'
H10 = _H + ', now about fifty, moustache with some grey hairs, a dark-blue fleece jacket)'
H20 = _H + ', now about sixty, grey moustache and grey temples, a dark-blue zip jacket)'
M = 'the mechanic Mikhalych exactly as in reference image 1 (about fifty, grey-streaked beard, dark-navy cap with an orange visor, pencil behind his ear, light-blue denim bib overalls over an orange T-shirt, red checked rag)'
OLD = 'a small boxy white 1970s Soviet-style sedan (generic, no badges)'
OWN = 'his own older silver compact car exactly as the car in reference image 2 (generic, no badges, no taxi stripes)'  # канон: та же серебристая, что KD4/KE2/KG5/KZ3
VOLGA = 'a big rounded white 1970s Soviet-style sedan with a black-and-white checker stripe on the doors and a small green light on the windscreen (generic, no badges)'
F = [  # (имя, кто: 'H' — герой, 'MH' — Михалыч и герой, None — без людей из рефов, сцена)
 # вступление, 1992
 ('KI1', 'H', 'A gloomy winter morning at the closed gates of a big old factory with a chain and padlock on the gate, snow; {H90} walks away from the gates, hands in his jacket pockets, sad but determined.'),
 ('KI2', 'H', '{H90} sits behind the steering wheel of {OLD}, driving out of a snowy courtyard of grey apartment blocks at dawn, both hands on the wheel, view from the front through the windscreen.'),
 ('KI3', 'H', 'A city street at night in the early 1990s with orange streetlights and wet asphalt; {H90} leans on the side of {OLD}, arms crossed, looking at the viewer with a tired half-smile; the right half of the frame is the empty dark street.'),
 # 1 частник
 ('KA1', None, 'A big Soviet taxi depot yard in 1991: long rows of identical big rounded white 1970s Soviet-style sedans with a black-and-white checker stripe on the doors and a small green light on the windscreen (generic, no badges) parked in lines in front of a brick garage building, overcast sky.'),
 ('KA2', None, 'An auction in a shabby hall: an auctioneer with a wooden gavel at a lectern, a small crowd of men in jackets raising hands; through the big window behind them several big rounded white 1970s Soviet-style sedans with a black-and-white checker stripe on the doors and a small green light on the windscreen (generic, no badges) are parked outside in a row, all white, none yellow.'),
 ('KA3', None, 'A wide city street in winter 1992 with almost no cars and no taxis at all; an empty taxi stand with a bare pole; people in winter coats waiting at the curb.'),
 ('KA4', None, 'A small grocery shop in 1992: a shop assistant crosses out an old price on a cardboard tag and writes a new bigger one, an elderly woman with a string bag looks on in shock; tags show only scribbles, no readable digits.'),
 ('KA5', 'H', 'A snowy city curb: a man in a fur hat and winter coat raises his hand; {H90} stops {OLD} next to him, the passenger window rolled down.'),
 ('KA6', 'H', 'View from the back seat: {H90} at the wheel turns his head to the open passenger window where a man in a fur hat leans in to talk, they bargain, the driver shows an open palm.'),
 ('KA7', None, 'Close-up of the dashboard of an old 1970s Soviet-style car: simple round gauges with blank faces, a cassette radio, a small fir-tree air freshener hanging from the mirror, no taxi meter, snowy street through the windscreen.'),
 ('KA8', 'H', '{H90} at the wheel at night looks into the rear-view mirror with a careful attentive look, a passenger silhouette sits in the back seat, warm dashboard light on his face.'),
 # 2 середина 90-х
 ('KB1', 'H', '{H90} sits in his car and counts a thick bundle of crumpled paper banknotes, the notes have no readable digits, evening light.'),
 ('KB2', None, 'A long wide avenue leading to the outskirts of a big city at dusk, endless rows of grey concrete apartment blocks, a small white boxy sedan drives away along the empty road.'),
 ('KB3', 'H', 'An old 1990s petrol station with a simple mechanical fuel pump with a blank dial; {H90} fills {OLD} with a fuel nozzle, a puddle and a kiosk behind.'),
 ('KB4', None, 'A taxi stand in a 1990s city: {VOLGA} waits at the curb, a second one behind it, grey winter day.'),
 ('KB5', None, 'A small 1990s taxi office: a woman dispatcher with permed hair talks on a black rotary telephone, writes on a paper pad, a big paper city map on the wall.'),
 # 3 дефолт
 ('KC1', None, 'Close-up of two hands on a kitchen table: one holds a thick stack of large old paper banknotes, the other a few small new banknotes, all notes without readable digits, a cup of tea nearby.'),
 ('KC2', None, 'A street in August 1998: a worried crowd stands at the closed glass door of a bank, a man reads a newspaper with a blank front page, summer heat.'),
 ('KC3', 'H', 'A long line of private cars of different kinds parked along a curb with their drivers waiting; {H90} leans out of the window of {OLD} at the front of the line, looking at the empty sidewalk.'),
 ('KC4', 'H', '{H90} sits at a small kitchen table late at night under a lamp, tired, counting a few small banknotes and writing in a little notebook, a teapot and car keys on the table.'),
 ('KC5', None, 'A quiet courtyard of apartment blocks at night: {OLD} parked under a single streetlight, all windows dark, light snow.'),
 # 4 рация, 2000-е
 ('KD1', None, 'A dispatch office of the early 2000s: a woman dispatcher with a headset speaks into a desk radio microphone, a desktop computer with a thick monitor, a city map with pins on the wall, a coffee mug.'),
 ('KD2', 'H', '{H00} sits in his car holding a handheld radio microphone on a coiled cord near his mouth, writing an address on a notepad on the steering wheel, evening city lights.'),
 ('KD3', None, 'A busy big-city avenue at night in the early 2000s full of cars with headlights, illuminated shop windows, light rain.'),
 ('KD4', 'H', 'A car dealership showroom of the 2000s: {H00} shakes hands with a smiling salesman in a tie next to a brand-new compact silver sedan (generic, no badges), holding a folder of papers under his arm.'),
 # 5 закон
 ('KE1', None, 'Near a big railway station in winter 2011: a crowd of private cars of different makes with their drivers standing nearby offering rides to arriving passengers with suitcases, only one official taxi with a roof light among them.'),
 ('KE2', 'H', '{H10} kneels by the front door of his silver compact sedan (generic, no badges) and sticks a black-and-white checkerboard stripe sticker on the door; an orange roof light without letters already sits on the roof.'),
 ('KE3', 'H', 'Inside a taxi: {H10} turns from the driver seat and hands a small printed paper receipt to a smiling woman passenger in the back seat.'),
 ('KE4', None, 'A modern big-city street with many bright lemon-yellow taxi sedans (generic, no badges) with checker stripes and orange roof lights without letters, a sunny day.'),
 # 6 приложение
 ('KF1', 'H', 'Close-up over the shoulder of {H10} in the driver seat: a smartphone in a windscreen holder shows a simple map with a route line and a car icon, no text on the screen, his hand reaches to tap the screen.'),
 ('KF2', None, 'A woman in a winter coat waits alone at a dark snowy roadside at night, checking her wristwatch impatiently, no cars around.'),
 ('KF3', 'H', '{H10} drives at night, relaxed, following the route on a phone navigator in a holder, city lights reflecting on the windscreen.'),
 ('KF4', None, 'A busy sidewalk in a modern city: many people walk while looking at their smartphones, nobody raises a hand, a yellow taxi pulls up to a man who is looking at his phone.'),
 # 7 двадцатые
 ('KG1', None, 'An empty big-city avenue on a spring morning in 2020: no people, no traffic, one yellow taxi parked at the curb, pigeons on the sidewalk, blossoming trees.'),
 ('KG2', 'HC', '{H20} sits in the driver seat of {OWN} parked in a courtyard of apartment blocks on an early autumn day with yellow leaves; through the open driver window he looks at a green checkmark on his smartphone screen with satisfaction, no other text on the screen.'),
 ('KG3', 'HC', '{H20} stands next to {OWN} at dawn after a long night shift and stretches his back with both hands on his lower back, yawning; an empty street of grey apartment blocks, no domes, no churches, no recognisable landmarks.'),
 ('KG4', None, 'A taxi company lot: a row of brand-new identical sedans (generic, no badges) with checker stripes, an inspector in a vest checks papers on a clipboard.'),
 ('KG5', 'H', '{H20} pats the roof of his own older silver sedan (generic, no badges) with a relieved smile, in a quiet courtyard.'),
 # итог, 2026
 ('KZ1', 'HC', '{H20} sits behind the wheel of {OWN} parked on a river embankment at dusk, generic city lights and apartment towers in the distance, no domes, no churches, no recognisable landmarks; a thoughtful calm look, view through the open driver window.'),
 ('KZ2', 'H', 'Night ride: {H20} drives through the city, an elderly woman passenger with a shopping bag sits in the back seat and smiles, warm interior light.'),
 ('KZ3', 'MH', 'In a garage: {M} leans over the open bonnet of a silver sedan (generic, no badges), and {H20} stands next to him, both laughing; tools on the wall, warm lamp light.'),
]
KG5_JOB = '1caee284-1ffa-4166-b221-ee827154a17d'  # кадр KG5: серебристая машина героя 2020-х
REF = {'H': [HERO, YARD], 'HC': [HERO, KG5_JOB], 'MH': [MIKH, HERO], None: [GAR, YARD]}
prompts, shots, reqs = {}, {'frames': {}}, []
for i, (n, who, scene) in enumerate(F):
    if who is None: pre = STYLE + 'Use the reference images ONLY as a sample of the drawing style; do NOT draw the people from them. '
    elif who == 'HC': pre = STYLE + 'Reference image 1 shows the taxi driver; reference image 2 shows his car and the drawing style. '
    elif who == 'H': pre = STYLE + 'Reference image 1 shows the taxi driver; image 2 is only a sample of the drawing style. '
    else: pre = STYLE + 'Reference image 1 shows the mechanic Mikhalych, reference image 2 shows the taxi driver. '
    p = pre + scene.format(H90=H90, H00=H00, H10=H10, H20=H20, M=M, OLD=OLD, VOLGA=VOLGA, OWN=OWN) + END
    if who == 'MH': p = p.replace('the taxi driver exactly as the man in reference image 1', 'the taxi driver exactly as the man in reference image 2')
    prompts[n] = p
    shots['frames'][n] = {'cast': ['mikhalych'] if who == 'MH' else []}
    reqs.append(dict(index=i, params=dict(model='gpt_image_2_6', quality='low', resolution='1k', aspect_ratio='16:9', prompt=p,
                                         medias=[dict(role='image_references', value=v) for v in REF[who]])))
json.dump(prompts, open(os.path.join(D, '..', 'prompts.json'), 'w'), ensure_ascii=False, indent=1)
json.dump(shots, open(os.path.join(D, '..', 'shots.json'), 'w'), ensure_ascii=False, indent=1)
import sys
if len(sys.argv) > 1:  # перегенерация выбранных: python3 kf_spec.py KA2 KG2 … → kf_req_fix.json
    fix = [r for r in reqs if F[r['index']][0] in sys.argv[1:]]
    json.dump(fix, open(os.path.join(D, 'kf_req_fix.json'), 'w'), ensure_ascii=False)
    print('fix', [F[r['index']][0] for r in fix]); sys.exit()
for b in range(0, len(reqs), 12):
    json.dump(reqs[b:b + 12], open(os.path.join(D, f'kf_req_{b // 12}.json'), 'w'), ensure_ascii=False)
print(len(F), 'кадров,', (len(reqs) + 11) // 12, 'партии')
