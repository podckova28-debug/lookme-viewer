"""Stage 1 masters for What If #4 (TB): empty locations, one hero per era (on plain cream paper, used only as a character reference), diagram master.
Every scene frame later is an EDIT of one location master + the era hero as the second reference."""
import json
STYLE = '557f5d94-d7bb-494f-bfa1-5a92bfffb8b5'
LOC = ("2D animated history explainer background, 16:9, NO PEOPLE, no text, no readable writing. Same ink-and-fine-cross-hatching drawing style and muted sepia palette as the reference. "
       "Straight-on camera at eye level, medium-wide shot; the middle of the floor is open space where people can stand. No street lamps. ")
HERO = ("Character reference: a single simple cartoon stickman standing, full body, facing the viewer, centered on a plain cream paper background, nothing else. "
        "Same ink-and-cross-hatching drawing style as the reference. Big plain smooth white round head with a black outline and NO hair, two dot eyes, simple eyebrows and mouth, no nose; "
        "thin black stick arms and legs, small black mitten hands. Exactly one head, two arms, two hands, two legs, arms hanging by his sides. No text. ")
M = {
 'm_salon':   LOC + "An elegant 1850s London drawing room: tall window with heavy curtains, a fireplace with a gilt mirror above it, a velvet sofa, a small round table with a teapot, candles, patterned wallpaper.",
 'm_rome':    LOC + "A small rented room in Rome, 1820: whitewashed walls, a narrow bed, one tall shuttered window with a view of a sunny piazza and stone steps, a simple chair and a small table with a jug.",
 'm_farm':    LOC + "A snowy New England farmyard in winter 1892: a white clapboard farmhouse with a porch, a red barn, a wooden fence, bare trees, deep snow, grey sky.",
 'm_cem':     LOC + "A small snowy country cemetery in Rhode Island, 1892: simple slate gravestones, a stone stone-walled family crypt built into a small hill with a wooden door, bare trees, a wooden fence, grey winter sky.",
 'm_kitchen': LOC + "The plain kitchen of a New England farmhouse, 1892: a cast-iron stove, a wooden table with chairs, a window with snow outside, a shelf with tin cups and jars, an oil lamp.",
 'm_porch':   LOC + "The long open-air 'cure porch' of a mountain sanatorium in 1905: a row of simple wooden reclining beds with thick blankets along a covered wooden veranda, snow on the railing, snowy pine-covered mountains behind.",
 'm_dining':  LOC + "The dining hall of a 1905 mountain sanatorium: long tables with white tablecloths, plates, big jugs of milk, tall windows with snowy mountains, a large weighing scale with a sliding weight standing by the wall.",
 'm_ward47':  LOC + "A 1947 British hospital ward: two rows of white iron beds with white sheets, tall windows, a nurse's desk with a lamp, a medicine trolley with small glass bottles, pale green walls.",
 'm_clinic':  LOC + "A modern 2020s clinic consultation room: a desk with a computer monitor, a lit X-ray viewing box on the wall, an examination couch, a window, plants.",
 'm_diag':    "Hand-drawn explainer diagram in ink and muted watercolour on aged paper, 16:9, no words, no letters, no numbers. A large simple outline of a human chest seen from the front with both lungs drawn in soft pink, the airways branching like a tree; the rest of the page is empty paper. Clear and simple.",
 'h_1892':    HERO + "Dressed as a New England farm boy of 1892: brown wool flat cap, grey wool jacket over a white shirt, dark trousers, worn boots, a knitted scarf.",
 'h_1905':    HERO + "Dressed as a sanatorium patient of 1905: a thick grey wool dressing gown over striped pyjamas, a knitted wool hat, slippers.",
 'h_1947':    HERO + "Dressed as a British hospital patient of 1947: plain blue-and-white striped hospital pyjamas, bare feet in leather slippers.",
 'h_today':   HERO + "Dressed in modern 2020s clothes: dark grey hoodie, blue jeans, white sneakers.",
}
R = [{'index': k, 'params': {'model': 'gpt_image_2_5', 'prompt': p, 'quality': 'low', 'resolution': '1k', 'aspect_ratio': '16:9',
      'medias': [{'value': STYLE, 'role': 'image_references'}]}} for k, (i, p) in enumerate(M.items())]
json.dump({'r': R[:12], 'r2': R[12:], 'ids': list(M)}, open('masters_todo.json', 'w'), indent=1)
print(len(R), list(M))
