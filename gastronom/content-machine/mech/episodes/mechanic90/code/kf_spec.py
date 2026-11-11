"""Кадры «Ты — механик 90-х»: gpt_image_2_6 low 1k 16:9 (0,25 кр). → ../prompts.json, ../shots.json, kf_req_<n>.json (партии по 12).
Возрасты героя: Y18 (1994–96, реф. молодой Михалыч 81306003), Y22 (конец 90-х), Y30 (нулевые), Y40 (десятые), M (сейчас, реф. 87ee183f)."""
import json, os
D = os.path.dirname(os.path.abspath(__file__))
YOUNG, MIKH, GAR, YARD = '81306003-6fca-45bf-9fc6-12ab93663859', '87ee183f-9089-4c8d-bbe2-f2bdaec3c14c', '23313f2f-6cbd-489b-b445-5159ade03183', '08996e99-8177-4b7d-8b13-c1ae3a50f7bb'
STYLE = 'Wide horizontal 16:9 frame in EXACTLY the same flat 2D cartoon style as the reference images (bold dark outlines, soft cel shading, warm saturated colours). '
END = ' Exactly two arms and two hands with five fingers each. No text, no letters, no numbers, no logos, no badges, no number plates.'
H = {
 'Y18': ('the young mechanic from reference image 1 (eighteen, slim, clean-shaven, thick dark hair, broad round face, rosy cheeks, bushy dark eyebrows, faded blue work overalls over a striped sailor undershirt)', [YOUNG, GAR]),
 'Y22': ('the young mechanic from reference image 1, now about twenty-two: a bit stockier, short dark stubble, thick dark hair, blue work overalls over a striped undershirt', [YOUNG, GAR]),
 'Y30': ('the mechanic who is a mix of reference image 1 (young) and reference image 2 (old): about thirty, stocky, short neat dark beard without grey, dark-navy cap with an orange visor, blue bib overalls over an orange T-shirt', [YOUNG, MIKH]),
 'Y40': ('the mechanic from reference image 2 but about forty: dark beard with the first grey streaks, dark-navy cap with an orange visor, pencil behind his ear, light-blue denim bib overalls over an orange T-shirt', [MIKH, YOUNG]),
 'M':   ('the mechanic Mikhalych exactly as in reference image 1 (about fifty, grey-streaked beard, dark-navy cap with an orange visor, pencil behind his ear, light-blue denim bib overalls over an orange T-shirt, red checked rag)', [MIKH, GAR]),
}
F = [  # (имя, герой или None, сцена)
 ('KI2', None, 'Extreme close-up split down the middle: on the left a young smooth hand, on the right an old weathered greasy hand with grey hairs, both gripping the SAME worn chrome spanner across the split; warm garage light.'),
 ('KI3', 'Y18', '{H} stands as a dark silhouette in the open door of a brick garage box at sunset in a Soviet garage cooperative, a spanner in his hand, long shadow on the ground, rows of garage doors, orange sky; calm empty upper half of the sky.'),
 ('KA1', 'Y18', '{H} walks into a run-down Soviet truck depot in the mid-1990s: half of the repair bays empty and boarded up, an old rusty bus and a lorry without wheels, puddles, grey sky, peeling paint.'),
 ('KA2', 'Y18', '{H} stands confused in a dim depot office while a tired foreman in a grey jacket hands him two old car tyres instead of money; a cashbox on the desk is empty.'),
 ('KA3', None, 'A queue of old Soviet cars in the muddy yard of a 1990s repair depot: beige and red VAZ Zhiguli sedans, a blue Moskvich-2141 hatchback and a black Volga GAZ-24, bonnets open, steam from one radiator, grey autumn day.'),
 ('KA4', None, 'Top-down flat lay on a greasy wooden workbench: an old carburettor, an ignition distributor with its cap, a cardan cross joint and a clutch disc, a few spanners, oily rag; warm lamp light.'),
 ('KA5', 'Y18', '{H} leans his ear close to the running engine of an old beige VAZ-2101 Zhiguli with the bonnet open, eyes closed, listening carefully; a little exhaust haze, depot background.'),
 ('KA6', 'Y18', '{H} lovingly unrolls a canvas tool roll on a bench showing a full set of shiny spanners of different sizes, smiling proudly, a single bulb above.'),
 ('KB1', 'Y22', '{H} lifts the rolling door of his own brick garage box in a Soviet garage cooperative in spring 1996, rows of identical garage doors with rusty locks, puddles, a few old Zhiguli parked along the lane.'),
 ('KB2', 'Y22', 'Inside a small brick garage box {H} digs an inspection pit in the concrete floor with a shovel, knee-deep, sweating, a pile of earth and broken concrete beside him, one bulb.'),
 ('KB3', 'Y22', 'Winter inside a frosty brick garage box: {H} in a quilted jacket over his overalls blows on his cold fingers next to an old car with the bonnet open, an electric kettle steaming and a small homemade electric heater glowing orange; frost on the walls.'),
 ('KB4', 'Y22', 'A Soviet garage cooperative lane in the 1990s: two neighbours in tracksuits point the way to {H} standing by his open garage, a third man walks up with his old Zhiguli; friendly mood.'),
 ('KB5', 'Y22', '{H} shakes hands with a calm client in a leather jacket by an old car; the client holds out a small wad of banknotes for spare parts; ordinary daylight, no weapons, friendly business mood.'),
 ('KC1', 'Y22', 'A used 1980s German boxy dark-blue four-door sedan (generic, no badges) rolls into the garage cooperative lane for the first time; {H} stares at it amazed, a spanner hanging from his hand; neighbours peek out.'),
 ('KC2', 'Y22', '{H} stands bent under the open bonnet of the used 1980s German boxy dark-blue sedan, completely puzzled, scratching his head; the engine bay is full of unfamiliar hoses and boxes.'),
 ('KC3', 'Y22', 'A chaotic 1990s open-air car parts market: rows of stalls and tarpaulins piled with used engines, headlights, bumpers and gearboxes from foreign cars, crowds in leather jackets and tracksuits; {H} searches with a scrap of paper in his hand.'),
 ('KC4', None, 'A cargo ship in a Russian Far East port in the 1990s unloading used Japanese right-hand-drive sedans and vans (generic, no badges) on the quay by crane, hills and the sea behind, seagulls.'),
 ('KC5', 'Y22', '{H} pulls a messy tangle of twisted wires and electrical tape out from under a dashboard of a foreign car, making a comic horrified face; a burnt fuse in his other hand.'),
 ('KC6', 'Y22', 'Night in the garage: {H} sits on an upturned bucket and puts a few banknotes into an old tin coffee can hidden on a shelf behind jars of bolts, smiling quietly; lamp light.'),
 ('KD1', 'Y22', 'August 1998, morning in the garage cooperative: a group of worried men in tracksuits and {H} crowd around a small portable radio on the bonnet of a Zhiguli, shocked faces, newspapers in hands with no readable text.'),
 ('KD2', 'Y22', '{H} stands in a small car parts shop in 1998 staring in shock at a shelf of imported spare parts in boxes, each box with a blank paper price tag and a blank new tag pinned over it; the shop seller shrugs.'),
 ('KD3', None, 'A very old patched VAZ Zhiguli sedan with mismatched doors and a bumper tied with wire drives past an empty new-car showroom with dark windows; grey 1998 autumn street.'),
 ('KD4', 'Y22', 'A line of old cars waiting outside {H}\'s garage box in the cooperative; owners in worn coats count coins; {H} wipes his hands and looks at the long queue.'),
 ('KD5', 'Y22', '{H} at a workbench carefully rebuilds an old carburettor from tiny parts laid out on a rag, magnifying glass, concentrated face; late evening lamp.'),
 ('KE1', 'Y30', 'Early 2000s: {H} in a clean jacket stands amazed in a bright new car showroom full of shiny new compact foreign cars (generic, no badges), balloons, polished floor.'),
 ('KE2', 'Y30', 'Early 2000s: in front of {H}\'s garage stand a silver first-generation compact hatchback with round headlights and a simple beige budget sedan (both generic, no badges); {H} with a spanner, smiling.'),
 ('KE3', None, 'A young Russian family at a desk in a bank office in the 2000s happily signing car loan papers, the car keys on the desk, a bank clerk smiling; no readable text.'),
 ('KE4', 'Y30', 'Under the open bonnet of a 2000s Lada sedan with a fuel-injection engine full of wires and sensors {H} scratches the back of his cap, worried, looking at a tangle of wiring.'),
 ('KE5', 'Y30', '{H} holds a new boxed car diagnostic scanner with a cable in his hands in a small shop, hesitating, the box is expensive-looking; the seller waits.'),
 ('KE6', 'Y30', '{H} confidently plugs the diagnostic scanner cable under the dashboard of a 2000s car, the scanner screen glowing green with simple graph lines, he smiles.'),
 ('KF1', 'Y30', '2009: a big car dealership with an almost empty showroom, a lonely salesman yawning, a few cars with blank price tags; {H} looks in through the glass from outside.'),
 ('KF2', None, 'A car scrapyard in 2010: a hydraulic press crushing an old beige VAZ Zhiguli sedan, a crane holding another one, a pile of flattened old cars.'),
 ('KF3', 'Y30', '{H} stands sadly in the garage lane watching an old red VAZ-2101 kopeika being driven away on a tow truck towards the scrapyard, his hand raised in farewell.'),
 ('KG1', 'Y40', '2010s: the lane in front of {H}\'s garage is jammed with identical white and yellow taxi sedans (generic, no badges) waiting for service; {H} counts them, amused.'),
 ('KG2', 'Y40', '{H} replaces a timing belt on a modern engine with his eyes closed and a calm smile, hands working confidently, the car on a lift.'),
 ('KG3', 'Y40', '{H} teaches a young apprentice in clean overalls to listen to a running engine: both lean over the open bonnet, {H} holds up a finger "listen", the apprentice concentrates.'),
 ('KG4', 'Y40', 'Winter 2014 evening: {H} looks at a smartphone in his hand with a worried face in his garage, a long invoice from a parts supplier on the bench; snow outside the door.'),
 ('KG5', 'Y40', '{H} stacks boxes of spare parts on tall metal shelves in a back room of his garage, the shelves full of oil filters, brake pads and belts in plain boxes.'),
 ('KH1', 'M', '2020: a quiet empty city courtyard of panel blocks, cars parked for weeks covered with fallen leaves and dust; {H} stands alone at his open garage door with a cup of tea, looking at the empty street.'),
 ('KH2', None, '2022: a large car dealership building with all brand signs removed, empty clean spots on the facade, an empty showroom with no cars, a cleaner with a mop; grey sky.'),
 ('KH3', 'M', 'A modern compact crossover (generic, no badges) stands on a lift without its front bumper and headlight; on the garage wall a paper calendar with many days crossed out in red; {H} shrugs, waiting.'),
 ('KH4', 'M', 'A brand-new modern Chinese-style compact crossover (generic, no badges) drives into {H}\'s garage; {H} opens the bonnet and stares at the engine for a long moment, curious, one eyebrow raised.'),
 ('KH5', 'M', '{H} sits by the open bonnet of the modern crossover with a laptop on his knees connected by a cable, the screen glowing; on the wall behind him hangs an old faded photo of a 1990s German boxy sedan.'),
 ('KZ1', 'M', '{H} in his garage in 2026, tired but content, wiping his greasy hands with the red checked rag, warm evening light, an old Zhiguli and a modern crossover side by side behind him.'),
 ('KZ2', 'M', 'A garage wall covered with old faded photographs pinned up: a beige VAZ Zhiguli, a 1990s German boxy sedan, a white taxi sedan, a modern crossover, and photos of a young mechanic; {H} looks at them from the side, nostalgic.'),
 ('KZ3', 'M', '{H} leans his ear close to a running engine with his eyes closed, listening, exactly like his younger self did thirty years ago; warm light.'),
 ('KZ4', 'M', '{H} faces the viewer, smiling warmly, holding up the same worn chrome spanner as in his youth, in his garage; close medium shot, his face big in the frame.'),
]
prompts, frames, reqs = {}, {}, []
for i, (n, h, scene) in enumerate(F):
    who, refs = H[h] if h else ('', [GAR, YARD])
    txt = STYLE + (scene.replace('{H}', who) if h else 'Use the reference images ONLY as a sample of the drawing style. ' + scene) + END
    prompts[n] = txt; frames[n] = {'cast': ['mikhalych'] if h else []}
    reqs.append({'index': i, 'params': {'model': 'gpt_image_2_6', 'quality': 'low', 'resolution': '1k', 'aspect_ratio': '16:9', 'prompt': txt,
                 'medias': [{'role': 'image_references', 'value': r} for r in refs]}})
json.dump(prompts, open(os.path.join(D, '..', 'prompts.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump({'frames': frames}, open(os.path.join(D, '..', 'shots.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for k in range(0, len(reqs), 12):
    json.dump(reqs[k:k + 12], open(os.path.join(D, f'kf_req_{k // 12}.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print(len(F), 'кадров,', (len(reqs) + 11) // 12, 'партий')
