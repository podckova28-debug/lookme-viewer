"""Кадры «Шипы или липучка»: gpt_image_2_6 low 1k 16:9 (0,25 кр). → ../prompts.json, ../shots.json, kf_req_<n>.json (партии по 12).
Михалыч — реф. 87ee183f; Костя (сосед, липучка) — реф. KI1 (d0a08880), там он впервые нарисован; гараж 23313f2f, двор 08996e99.
Марок нет: шины и машины без логотипов. Цифры на экране — только графикой кодом, на кадрах ни цифр, ни текста."""
import json, os
D = os.path.dirname(os.path.abspath(__file__))
MIKH, GAR, YARD, KI1 = '87ee183f-9089-4c8d-bbe2-f2bdaec3c14c', '23313f2f-6cbd-489b-b445-5159ade03183', '08996e99-8177-4b7d-8b13-c1ae3a50f7bb', 'd0a08880-0883-49e2-a1b8-ebb0c40738a0'
STYLE = 'Wide horizontal 16:9 frame in EXACTLY the same flat 2D cartoon style as the reference images (bold dark outlines, soft cel shading, warm saturated colours). '
END = ' Exactly two arms and two hands with five fingers each per person. No text, no letters, no numbers, no logos, no brand names, no number plates.'
M = 'the mechanic Mikhalych exactly as in reference image 1 (about fifty, grey-streaked beard, dark-navy cap with an orange visor, pencil behind his ear, light-blue denim bib overalls over an orange T-shirt, red checked rag)'
K = 'his neighbour Kostya exactly as the young man on the right in reference image 2 (slim, about twenty-seven, clean-shaven, short light-brown hair with a quiff, dark-blue puffer jacket over a grey hoodie, jeans)'
STUD = 'a winter tyre with shiny metal studs in the tread'; FRIC = 'a studless winter tyre with many fine zigzag sipes'
F = [  # (имя, кто: 'M' / 'MK' / 'K' / None, сцена)
 ('KI2', 'K', '{K} stands next to a car in a snowy courtyard covering his ears with both hands and grimacing comically, as if the studded tyres of a passing car are rattling loudly; slush on the asphalt.'),
 ('KI3', 'M', '{M} proudly rests his hand on a stack of four tyres with shiny metal studs in his garage, confident smile, winter light from the open door.'),
 ('KI4', 'M', '{M} in his garage strikes an old brass boxing bell hanging on the wall with a spanner, grinning, as if announcing the first round; two tyres, one studded and one studless, lean against the workbench like boxers in corners.'),
 ('KK1', None, 'Extreme close-up of a winter tyre tread with shiny round metal studs set in the rubber blocks, frost crystals on the rubber, cold blue light.'),
 ('KK2', None, 'Extreme close-up at road level: a studded winter tyre rolling on clear blue ice, the metal studs biting into the ice and throwing up tiny ice shavings.'),
 ('KK3', None, 'Extreme close-up of a studless winter tyre tread: soft rubber blocks cut by many thin zigzag sipes, like a fine grid, frost crystals, cold light.'),
 ('KK4', None, 'Two winter tyres side by side on a white background like a catalogue photo: on the left a Nordic studless tyre with dense fine sipes and small blocks, on the right a European winter tyre with wide grooves and fewer sipes. No text.'),
 ('KA1', None, 'A wide frozen lake test track under a grey sky: two identical small silver hatchbacks (generic, no badges) brake side by side on clear ice, orange cones mark the stopping zone, one car has already stopped while the other is still sliding past it; snow banks along the track.'),
 ('KA2', None, 'A small silver hatchback (generic, no badges) braking hard on clear blue ice of a frozen lake, ice spray from the tyres, a test driver in a helmet inside, orange cones ahead.'),
 ('KA3', None, 'On clear ice of a frozen lake a long yellow measuring tape stretches from an orange cone to the front wheel of a stopped silver hatchback (generic, no badges); a test engineer in a winter jacket kneels with a clipboard; no numbers visible.'),
 ('KB1', None, 'A snowy courtyard of apartment blocks with an icy slope: one small car (generic, no badges) easily drives up the icy slope while another one next to it spins its wheels, throwing ice and snow, unable to climb.'),
 ('KC1', None, 'A packed-snow test road between snow banks in a forest: a small grey hatchback (generic, no badges) brakes, snow dust flying from the tyres, orange cones, overcast winter day.'),
 ('KD1', None, 'A wet asphalt test track in cold rain, early winter: a small red hatchback (generic, no badges) brakes hard, water spray from the tyres, puddles reflecting grey sky, orange cones.'),
 ('KE1', None, 'A dry clean asphalt road on a sunny cold early winter day, frost on the grass at the roadside: a small blue hatchback (generic, no badges) brakes hard, a faint puff of road dust, orange cones.'),
 ('KF1', 'K', '{K} drives a small car on a highway on a grey winter day, view through the side window into the cabin: he winces comically at a loud humming noise from the tyres, one hand on the steering wheel.'),
 ('KF2', 'M', '{M} weighs a studded winter wheel on an old mechanical floor scale in his garage, looking at the scale with raised eyebrows; a studless wheel waits next to him. The scale dial has no numbers.'),
 ('KG1', 'MK', 'A tyre shop with racks of winter tyres: {M} and {K} stand in front of two tyres on display, each tyre with a blank white price tag without any numbers; {K} points at the cheaper-looking studless tyre and smiles, {M} rubs his beard.'),
 ('KG2', None, 'A small modern electric hatchback (generic, no badges) charging at a winter charging station at dusk, snow on the ground, the charging cable plugged in, cold blue light.'),
 ('KH1', None, 'A road at around zero degrees: melting slush and a thin glossy layer of wet ice on the asphalt, puddles with ice edges, grey thaw sky, a car (generic, no badges) driving carefully.'),
 ('KH2', None, 'A frozen road in a hard frost: thick white rime on the trees, hard dry ice on the road, a small car (generic, no badges) taking a curve on a frozen lake test track, sparkling frost in the air, pale low sun.'),
 ('KL1', 'M', '{M} in his garage tears a page off a big wall calendar decorated with snowflakes, the pages have only pictures and no numbers; snowy yard outside.'),
 ('KL2', None, 'A small car (generic, no badges) raised on a lift in a tyre shop, all four wheels fitted with studded winter tyres, a tyre fitter in overalls tightens a wheel nut.'),
 ('KL3', None, 'Close-up of the rear window of a small car (generic, no badges) in a snowy yard with a blank white triangle sticker with a red border, the triangle is completely empty, no letters inside.'),
 ('KL4', 'M', '{M} sits on a stool and counts the shiny metal studs on a new studded tyre with his finger, squinting, concentrated, garage lamp light.'),
 ('KM1', None, 'A spring city street in Scandinavia: worn ruts in the asphalt along the lanes, a cloud of grey road dust raised by passing cars, a street sweeper truck, colourful wooden houses, bare trees.'),
 ('KM2', None, 'A Nordic city street in winter with wooden houses and a tram line, cars (generic, no badges) driving on studded tyres on a snowy road, a gentle snowfall.'),
 ('KM3', 'M', '{M} drives calmly and carefully on a quiet snowy suburban road in a small car (generic, no badges), relaxed hands on the steering wheel, new studded tyres visible, view from outside through the open side window.'),
 ('KM4', 'M', '{M} stands outside his garage in the morning looking at the first frost on the grass and a thin layer of rime on a parked car, holding a mug of tea, a thermometer without numbers on the wall.'),
 ('KZ1', 'MK', '{M} and {K} shake hands in the garage and laugh, a studded tyre and a studless tyre lean against the workbench between them; warm light.'),
 ('KZ2', 'M', 'Split picture with a clean vertical divider: on the left a clean city avenue with cleared asphalt and slush, on the right an icy country road with private wooden houses and snow banks; {M} stands in the middle foreground pointing to both sides.'),
 ('KZ3', 'M', '{M} changes wheels in his garage: the car (generic, no badges) on a jack, a stack of studded winter tyres next to him, he tightens a wheel nut with a cross wrench, smiling.'),
 ('KZ4', 'M', '{M} faces the viewer, smiling warmly, holding a studded winter tyre in front of him with both hands, in his garage; close medium shot, his face big in the frame.'),
]
REF = {'M': [MIKH, GAR], 'MK': [MIKH, KI1], 'K': [GAR, KI1], None: [GAR, YARD]}
prompts, shots, reqs = {}, {'frames': {}}, []
for i, (n, who, scene) in enumerate(F):
    pre = STYLE + ('Use the reference images ONLY as a sample of the drawing style; do NOT draw the people from them. ' if who is None else '')
    if who == 'K': pre = STYLE + 'Reference image 2 shows Kostya on the right; do NOT draw the older bearded man from the references. '
    p = pre + scene.format(M=M, K=K) + END
    prompts[n] = p
    shots['frames'][n] = {'cast': ['mikhalych'] if who in ('M', 'MK') else []}
    reqs.append(dict(index=i, params=dict(model='gpt_image_2_6', quality='low', resolution='1k', aspect_ratio='16:9', prompt=p,
                                         medias=[dict(role='image_references', value=v) for v in REF[who]])))
shots['frames']['KI1'] = {'cast': ['mikhalych']}
json.dump(prompts, open(os.path.join(D, '..', 'prompts.json'), 'w'), ensure_ascii=False, indent=1)
json.dump(shots, open(os.path.join(D, '..', 'shots.json'), 'w'), ensure_ascii=False, indent=1)
for b in range(0, len(reqs), 12):
    json.dump(reqs[b:b + 12], open(os.path.join(D, f'kf_req_{b // 12}.json'), 'w'), ensure_ascii=False)
print(len(F), 'кадров,', (len(reqs) + 11) // 12, 'партии')
