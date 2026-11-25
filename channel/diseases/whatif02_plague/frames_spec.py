"""What If #2 (plague, Florence 1348): frame prompts.
python3 frames_spec.py -> frames_todo.json  [{id, line, prompt, ref}]
Frames already made in test/: t00 (C01), t01 (C02), t02 (C03), t03 (DAY 3 card), t04 (H14), t05 (H19), t06 (H25), t07 (T04).
"""
import json, os
STYLE = ("2D animated comedy history explainer frame, 16:9, no text, no letters. Hand-drawn ink illustration, clean black outlines, light cross-hatching, "
         "WARM bright palette: Tuscan ochre, terracotta, olive green and sky blue, sunny and playful, like a funny educational cartoon, not horror, not gory. NO cathedral dome and no domed church anywhere in the picture.")
MOD = ("2D animated comedy explainer frame, 16:9, no text, no letters. Hand-drawn ink illustration, clean black outlines, the same warm bright palette, "
       "soft daylight. The setting is modern (2020s), nothing old-fashioned.")
DIAG = ("Hand-drawn explainer diagram in ink and warm watercolour on aged cream paper, clean like a funny textbook plate, drawn arrows, "
        "no words, no letters, no numbers. Cartoon-simple, not gory. ")
SN = ("Humans are simple STICKMEN: plain white round head, two dot eyes, big expressive cartoon mouth and eyebrows, no nose, no beard, thin black stick legs, "
      "small solid black hands. Only the figures described, standing apart; each has exactly two arms and two hands; no readable text, no flags.")
YOU = ("YOU, the hero: a stickman with a plain white round head, a soft dark-green felt cap, a knee-length rust-red wool tunic with long sleeves, "
       "a brown leather belt, grey hose and simple brown shoes")
YOU_NIGHT = ("YOU, the hero, without his cap, in a plain long off-white linen nightshirt with long sleeves")
YOU_MOD = "YOU, the hero in the present day: a stickman with a plain white round head, a dark-green baseball cap, a rust-red hoodie and blue jeans"
DOC = "the physician: a stickman in a long scarlet doctor's gown and a round red cap (no beak mask, no mask at all)"
MUM = "your mother: a stickman in a simple brown dress and a white linen headscarf"
PL = ("The Plague exactly as on the attached character sheet (tall gaunt hooded figure in a ragged dark-brown cloak, glowing white eyes, spotted grey hands, "
      "a black rat on his shoulder, a battered leather suitcase), drawn in the same warm comic cartoon style, smug and theatrical rather than scary. "
      "Exactly one Plague, two arms, two hands.")
ROOM = "a simple 1348 Florentine bedroom with ochre plaster walls, a wooden bed with a straw mattress, a small window showing green Tuscan hills and blue sky (no buildings)"
FL = "a sunny market square in Florence in June 1348, terracotta roofs, fruit stalls, a few cats (no cathedral, no dome)"
CARD = ("Status-portrait composition: the hero is waist-up, front-facing, placed in the LEFT half of the frame, centred vertically; the right 40% of the frame is a plain "
        "calm ochre plaster wall with nothing on it (space for a graphic).")

F = []
def s(i, line, p, ref=False, base=STYLE, people=True): F.append({'id': i, 'line': line, 'prompt': f"{base} {SN if people else 'No people.'} {p}", 'ref': ref})
def d(i, line, p, people=False): F.append({'id': i, 'line': line, 'prompt': STYLE + ' ' + DIAG + p + ('' if people else ' No people.'), 'ref': False})
def pl(i, line, p, people=''): s(i, line, f"{PL} {people} {p}", ref=True)

# cold open
s('c01b', 'C01', f"Close-up on {FL}: {YOU} bites into a ripe peach, eyes closed in bliss, juice splashing, sunshine sparkles.")
s('c02a', 'C02', "Low angle on a market stall cloth: a tiny cartoon flea with a mischievous grin crouches like a sprinter, eyeing a grey-stockinged stickman ankle walking past.", people=False)
pl('c03b', 'C03', "Close-up: The Plague grins at the viewer and spreads one arm wide as if greeting an old friend; the rat on his shoulder waves; sunny Florentine rooftops behind.")
s('c04a', 'C04', f"On {FL}: {YOU} freezes mid-step with the peach halfway to his mouth, eyes wide, comic shock lines, as if he just heard terrible news.")
# day 0: the flea
d('h01a', 'H01', "A big cartoon rat flea in cut-away view: inside its stomach a dark green plug blocks the way; the flea clutches its belly with a miserable face.")
d('h01b', 'H01', "A cartoon flea tries to drink a drop of red liquid; the liquid backs up out of its mouth because of a green plug in its gut; the flea looks frustrated.")
s('h02a', 'H02', "Extreme close-up of a grey wool stocking on a stickman's ankle: a hungry cartoon flea bites again and again, motion lines, tiny green blobs going into the stocking.", people=False)
s('h02b', 'H02', "Close-up: the cartoon flea with tiny boots hiccups a small green blob, covering its mouth, embarrassed; Tuscan street blurred behind.", people=False)
d('h03a', 'H03', "A big circular magnified view, like looking down a microscope: pale pink background with many small rod-shaped bacteria that are darker at both ends, like tiny safety pins; one of them wears a tiny dark-brown hood and grins.")
d('h03b', 'H03', "Side-by-side comparison: a metal safety pin next to one magnified rod-shaped bacterium with dark tips at both ends; an arrow between them.")
pl('h04a', 'H04', "The Plague bows theatrically to the viewer in an empty Florentine alley, one hand on his chest, the other holding his suitcase; the rat bows too.")
s('h05a', 'H05', f"{CARD} {YOU} smiles happily holding a half-eaten peach, healthy, rosy cheeks, relaxed.")
# days 1-2
s('h06a', 'H06', f"A sunny 1348 wool workshop with bolts of dyed cloth: {YOU} carries a big roll of red cloth on his shoulder, whistling, cheerful.")
s('h06b', 'H06', f"A simple kitchen table: {YOU} happily eats bread and soup from a wooden bowl, a cat begging at his feet.")
s('h06c', 'H06', f"Night, {ROOM}, moonlight: {YOU_NIGHT} sleeps peacefully, smiling, a cat curled on his feet.")
d('h07a', 'H07', "A plain stickman body outline seen from the front: a dotted arrow runs from a small red dot on the ankle up the leg to a glowing round dot at the top of the thigh, where the leg joins the body; smaller dots at the armpits and the neck.", people=True)
d('h07b', 'H07', "A cartoon lymph node drawn as a round little sieve-shaped filter that catches small green germs while letting clear fluid through; the filter has a determined face.")
d('h08a', 'H08', "A round white cartoon immune cell wearing a tiny guard helmet opens its mouth wide and swallows a small green rod-shaped bacterium; the bacterium is smiling.")
d('h08b', 'H08', "The same round white immune cell drawn as a little carriage rolling along a pink vessel road; inside it, several small green rod-shaped bacteria ride as happy passengers, waving.")
pl('h09a', 'H09', "The Plague rides inside a small open wooden cart like a passenger, leaning back with his arms crossed behind his head, smug; the rat holds the reins.")
# day 3
s('h10a', 'H10', f"{ROOM}, blazing sun outside: {YOU_NIGHT} shivers violently under three thick blankets, teeth chattering; a cat on the windowsill lies flat, melting from the heat.")
s('h11a', 'H11', f"{ROOM}: {YOU_NIGHT} winces and shields his eyes from a bright beam of sunlight from the window, jagged headache lines around his head.")
s('h11b', 'H11', f"Close-up: {YOU_NIGHT}'s round head glows red like a lantern, steam puffs from its top, sweat drops flying.")
s('h12a', 'H12', f"A steep narrow stone staircase inside a house, plain plaster walls, no windows: {YOU_NIGHT} climbs it like a mountaineer, roped up, with a walking stick, exhausted.")
s('h12b', 'H12', f"The same staircase: {YOU_NIGHT} lies face-down halfway up the stairs, exhausted; a cat casually steps over him.")
# day 4
s('h14b', 'H14', f"{ROOM}: {YOU_NIGHT} walks stiff-legged like a cowboy, wincing, because even the cloth of his nightshirt touching his upper thigh hurts; little 'ouch' spark lines.")
d('h15a', 'H15', "A cut-away of a swollen round lymph node drawn like a crowded little fortress: inside, many small green rod-shaped bacteria and round white defender cells in a comic dust-cloud brawl.")
s('h16a', 'H16', "Night, a 1348 writing room with a candle: a stickman writer in a simple red cap and brown robe writes with a quill in a big manuscript, wide-eyed, as if recording something astonishing.")
s('h16b', 'H16', "Close-up of an old market balance scale on a wooden counter: an egg sits on one pan and a red apple on the other; a curious cat looks on.", people=False)
pl('h17a', 'H17', "The Plague sticks a new travel sticker onto his battered suitcase with a satisfied grin, like a tourist collecting souvenirs.")
s('h17b', 'H17', f"{CARD} {YOU_NIGHT}, sweaty, pale, grey shadows under his eyes, wincing in pain, one hand on his hip.")
# day 5: the doctor
s('h18a', 'H18', f"The doorway of {ROOM}: {DOC} steps in triumphantly with light rays behind him, holding a leather bag; {MUM} bows gratefully.")
s('h19b', 'H19', f"{ROOM}: {DOC} sniffs a glass flask of yellow liquid with his eyes closed like a wine taster; {YOU_NIGHT} in bed covers his face in embarrassment.")
s('h20a', 'H20', "A grand 1348 university hall in Paris: four stickman professors in long black academic gowns sit at a long table and point solemnly at the ceiling.")
d('h20b', 'H20', "A night-sky diagram: three cartoon planets with grumpy faces lined up in a row inside a simple constellation of a water-bearer pouring a jug; green mist pours down from them onto a tiny walled city.")
pl('h21a', 'H21', "The Plague shrugs with both palms up and an offended, confused face; the rat shrugs too.")
s('h22a', 'H22', f"{ROOM}: {DOC} holds a small bowl under {YOU_NIGHT}'s outstretched black stick arm, a thin trickle dripping into the bowl (not gory); the hero looks away, grimacing.")
s('h22b', 'H22', f"{ROOM}: {YOU_NIGHT} slumps in bed even more limp than before, tongue out, eyes spirals, totally drained.")
s('h23a', 'H23', "A 1348 apothecary shop: a stickman apothecary stirs a big bubbling cauldron; a grumpy cartoon viper pokes its head out of the pot; jars, a honey pot and red poppies on the shelves.")
s('h23b', 'H23', f"{ROOM}: {MUM} spoon-feeds {YOU_NIGHT} a dark syrup; he makes a disgusted face, eyes watering.")
s('h24a', 'H24', f"A wooden bathtub full of steaming water: {DOC} stands in front of it with his arms spread wide, blocking it, shouting 'no!' (no text).")
s('h24b', 'H24', f"{ROOM}: {YOU_NIGHT} sniffs his own armpit and recoils; little stink lines and two flies circle; a cat flees.")
s('h25b', 'H25', "A stone hall of the papal palace in Avignon: a stickman pope in white robes and a tall white papal hat sits on a chair exactly between two big bonfires, sweating, with a bored deadpan face.")
s('h26a', 'H26', f"{ROOM}: {YOU_NIGHT} holds an enormous bouquet of flowers and herbs right under his nose, so big that only his eyes are visible above it.")
s('h26b', 'H26', f"A Florentine street: {DOC} walks along holding a vinegar-soaked sponge on a stick to his nose, his face scrunched up.")
s('h27a', 'H27', "A scholar's study in 1348 Perugia: a stickman scholar in a dark-blue gown writes a treatise at a desk piled with books, confident and proud.")
s('h27b', 'H27', "The same scholar's study, empty: the chair is empty, the quill rests on an unfinished page, a thin wisp of smoke rises from a candle that just went out.", people=False)
pl('h28a', 'H28', "The Plague places one hand over his heart and bows his hooded head in mock-solemn respect, eyes glinting.")
# day 6: three paths
s('h29a', 'H29', f"A dusty country crossroads with three wooden signposts pointing three different ways (the boards are blank): {YOU_NIGHT} stands barefoot at the junction, confused, scratching his head.")
d('h30a', 'H30', "A large cartoon hand outline with simple blood vessels drawn inside; small dark dots (clots) block the vessels near the fingertips, and the fingertips are shaded dark grey-blue.")
d('h30b', 'H30', "A red river (the bloodstream) seen from above: dozens of tiny green rod-shaped bacteria sail down it on little boats, flooding everywhere.")
s('h31a', 'H31', f"{ROOM}: {YOU_NIGHT} lets out a huge cough that makes a big comic greenish cloud; two visiting stickmen neighbours leap backwards in horror.")
d('h31b', 'H31', "A simple pair of lungs drawn like two sponges, speckled with tiny green dots; small arrows show the dots flying out with a cough.")
d('h32a', 'H32', "A round lymph node drawn as a small stone castle on a hill: little round white defender cells stand on the walls, pushing back an army of small green rod-shaped bacteria at the gate.")
pl('h33a', 'H33', "The Plague flips a big gold coin into the air with his thumb, grinning; the rat watches the coin.")
s('h34a', 'H34', f"{CARD} {YOU_NIGHT} lies propped up on a pillow, very pale grey-blue face, glassy half-closed eyes, sweat, mouth open, exhausted.")
# day 8: survival
s('h35a', 'H35', "The dusty crossroads with three wooden signposts: a bright sunbeam breaks through the clouds and lights up only the right-hand road; a gold coin lies in the dust.", people=False)
s('h36a', 'H36', f"Morning, {ROOM}, window open, sunlight pouring in: {YOU_NIGHT} sits up in bed and stretches weakly, with a small tired smile.")
s('h36b', 'H36', f"{ROOM}: {MUM} brings a steaming bowl of soup; {YOU_NIGHT} smiles weakly and reaches for it.")
s('h37a', 'H37', f"{CARD} {YOU_NIGHT}, pale but smiling, sitting up in bed with a bowl of soup.")
pl('h38a', 'H38', "The Plague walks away down a narrow sunny Florentine street with his suitcase, his back to the viewer, waving over his shoulder; the rat looks back at the viewer.")
s('h39a', 'H39', f"A house doorway: {YOU}, thinner, wobbles out with a wooden walking stick, squinting at the bright sun.")
s('h39b', 'H39', "The same sunny market square in Florence, now empty and quiet: stalls closed with cloth covers, shutters shut, a single cat sitting in the middle.", people=False)
d('h39c', 'H39', "A hand-drawn old map of Europe and the Mediterranean, simple coastlines, with dark grey shading spreading across it from the south-east, small arrows.")
s('h40a', 'H40', "A 1348 monastery scriptorium: a stickman monk in a brown habit writes in a huge chronicle book with a quill, very serious.")
s('h40b', 'H40', f"{CARD} {YOU}, healthy again but a bit thinner, cap back on, giving a thumbs-up and a big grin, standing on a sunny street.")
# today
s('t01a', 'T01', f"A dry hiking trail in the 2020s American southwest: {YOU_MOD} walks happily; a tiny cartoon flea with boots crouches on his white sock.", base=MOD)
d('t02a', 'T02', "A simple hand-drawn world map in warm colours with a few small red dots: on Madagascar, in central Africa, and in the south-west of the United States.")
s('t02b', 'T02', "A sunny desert prairie with a burrow: a cheerful cartoon prairie dog wearing a tiny cowboy hat stands upright; a tiny flea sits on its head.", base=MOD, people=False)
s('t03a', 'T03', f"A bright modern clinic: a stickman woman doctor with a ponytail in a white coat holds up a small sample tube and looks at it; {YOU_MOD} sits on an exam table, hopeful.", base=MOD)
s('t03b', 'T03', "Comic insert: an old-fashioned glass flask of yellow liquid flies out of a modern clinic window with motion lines.", base=MOD, people=False)
s('t05a', 'T05', f"Evening campfire on a desert trail: {YOU_MOD} toasts a marshmallow on a stick and winks at the viewer.", base=MOD)
F.append({'id': 't06a', 'line': 'T06', 'prompt': f"{MOD} No people. {PL} Dusk: The Plague crouches in the shadow under a wooden porch in a modern desert town, glowing eyes, a sly grin, a prairie dog next to him.", 'ref': True})
s('e01a', 'E01', f"On {FL}: {YOU} leans on a fruit stall holding a peach, looking straight at the viewer with one eyebrow raised.")
s('e02a', 'E02', "Teaser: a dark village doorway at night; a growling cartoon dog with wild eyes and frothy drool stands in it; a stickman backs away holding a lantern. Funny-scary, not gory.")

if __name__ == '__main__':
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frames_todo.json')
    json.dump(F, open(out, 'w'), indent=1); print(len(F), 'frames ->', out)
