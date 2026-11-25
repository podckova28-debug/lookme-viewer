"""What If #2 (plague) v2, cholera look: frame list. Every frame uses reference images so the hero, the room and the doctor stay the same.
python3 frames_v2_spec.py -> frames_v2_todo.json  [{id, line, prompt, refs}]
Already made (frames_v2/): s_market, s_plague_stall, room_d3, room_doctor_flask, hall_fires (unused), diag_bubo, room_d4, room_d5_blood, room_d6.
"""
import json, os
# reference media (Higgsfield ids)
STYLE_REF = '557f5d94-d7bb-494f-bfa1-5a92bfffb8b5'   # cholera a01 (style)
DAY = 'dafceeaf-7d1b-465e-8a1c-eac836cdd114'         # s_market: hero by day
ROOM = 'b7db792c-151d-43ab-8306-28052215b8e6'        # room_d3: the attic room + hero in nightshirt
DOC = '5206c05e-13ee-4864-beae-e9223341db6a'         # room_doctor_flask: the physician
PL = '2cdb3bb6-a537-4d7c-9d20-9d33bc91262e'          # plague character sheet
PLS = '3b2790be-45d6-40c2-9767-147255115080'         # s_plague_stall: plague in this style
DIAG = '2ba4b711-de15-40f2-8178-1f2215bc50f7'        # diag_bubo: diagram style

ST = ("2D animated history explainer frame, 16:9, no text, no letters. Same drawing style as the reference images: hand-drawn ink illustration, "
      "clean black outlines, fine cross-hatching, muted grey-teal-sepia palette with a sickly green accent; warm light only from the sun, candles and fire. "
      "Not gory, cartoon-simple. No cathedral dome anywhere.")
SN = ("Humans are simple STICKMEN: plain white round head, two dot eyes, simple expressive mouth and eyebrows, no nose, thin black stick arms and legs, "
      "small solid black mitten hands. Each figure has exactly two arms and two hands.")
HERO = "YOU, the hero, exactly as in the reference: flat faded dark-green cloth cap, faded brown-red knee-length tunic, leather belt, grey hose"
NIGHT = "YOU, the hero, exactly as in the reference: bald plain white round head, long off-white linen nightshirt"
ROOMD = "the same small attic bedroom as the reference (sloping wooden ceiling, narrow wooden bed with straw mattress, small table with a candle and a tin bowl, small window)"
DOCD = "the physician exactly as in the reference (long dark-red gown, round red cap, no mask)"
MUM = "his mother, a stickman in a plain grey-brown dress and a white linen headscarf"
PLD = "The Plague exactly as in the references (tall gaunt hooded figure, ragged dark-brown cloak, glowing white eyes, spotted grey hands, black rat on his shoulder, battered suitcase); exactly one Plague"
STREET = "the same narrow stone market street in Florence, 1348, as in the reference, with the fruit stall"
DG = ("Hand-drawn explainer diagram in ink and muted watercolour on aged paper, same style as the reference diagram, drawn arrows, "
      "no words, no letters, no numbers. Any human figure is a plain stickman outline. ")
MOD = ("2D animated explainer frame, 16:9, no text. Same ink-and-cross-hatching drawing style and muted palette as the reference, but the setting is the present day (2020s). "
       "Humans are simple stickmen with white round heads, dot eyes, black stick limbs and small black mitten hands.")
MODHERO = "YOU, the hero today: the same stickman (white round head, dot eyes) in a dark-green baseball cap, a faded brown-red hoodie and jeans"

F = []
def f(i, line, p, refs): F.append({'id': i, 'line': line, 'prompt': p, 'refs': refs})
def day(i, line, p, refs=(DAY, STYLE_REF)): f(i, line, f"{ST} {SN} {p}", list(refs))
def room(i, line, p, extra=()): f(i, line, f"{ST} {SN} Inside {ROOMD}. {p}", [ROOM] + list(extra))
def pl(i, line, p): f(i, line, f"{ST} {SN} {PLD}. {p}", [PLS, PL])
def dg(i, line, p): f(i, line, f"{ST} {DG}{p}", [DIAG])
def ins(i, line, p, refs=(STYLE_REF,)): f(i, line, f"{ST} {p}", list(refs))
def mod(i, line, p, refs=()): f(i, line, f"{MOD} {p}", [STYLE_REF] + list(refs))

# ---- cold open: the market street
day('c01b', 'C01', f"Close-up in {STREET}: {HERO} bites a ripe peach, eyes closed with pleasure, juice dripping, warm morning sun.")
ins('c01c', 'C01', f"Low close-up of the cobblestones of {STREET}: a tiny flea crouches between two stones, watching a stickman's grey-hosed ankle step past.", (DAY, STYLE_REF))
ins('c01d', 'C01', "Extreme close-up: a tiny flea with a mischievous little face crouches like a sprinter on a cobblestone, legs coiled, ready to jump.")
ins('c02a', 'C02', "The tiny flea in mid-air, leaping toward a stickman's ankle in a grey wool stocking and a brown leather shoe, motion lines.", (DAY, STYLE_REF))
ins('c02b', 'C02', "Extreme close-up of a grey wool stocking on a black stick ankle: the flea bites into it, tiny impact lines. No skin visible.")
day('c04a', 'C04', f"In {STREET}: {HERO} freezes mid-step with the peach halfway to his mouth, eyes wide, as if he just heard terrible news.")
pl('c04b', 'C04', f"Close-up in {STREET}: The Plague flips a gold coin into the air with his thumb, grinning at the viewer; the rat watches the coin.")
day('c04c', 'C04', f"Wide shot of {STREET} at dusk, long shadows, stalls closing; {HERO} walks home small in the distance; a lonely, ominous mood.")
# ---- day 0: the flea
dg('h01a', 'H01', "A big flea in cut-away view: inside its stomach a dark green plug blocks the way; the flea has a miserable little face.")
ins('h01b', 'H01', "A flea clutching its belly with a miserable, hungry face, sitting on a grey wool stocking.")
dg('h01c', 'H01', "A flea trying to drink a drop of blood; the blood backs up out of its mouth because of the green plug in its gut; arrows show the backflow.")
ins('h01d', 'H01', "Close-up of the flea, now angry and starving, gritting its teeth, crouched on the grey wool stocking.")
ins('h02a', 'H02', "The flea biting the grey wool stocking again and again, motion lines, small impact marks.")
ins('h02b', 'H02', "Close-up: the flea hiccups and spits a tiny green droplet into the bite, looking guilty.")
dg('h02c', 'H02', "Cross-section of skin: a flea's mouthparts pierce in, tiny green rod-shaped bacteria pour into the skin and the small blood vessels below.")
day('h05b', 'H05', f"In {STREET}: {HERO} waves cheerfully at a neighbour, peach in his other hand, healthy and happy.")
# ---- days 1-2
day('h06a', 'H06', f"A 1348 wool workshop with bolts of dyed cloth and a loom: {HERO} carries a big roll of cloth on his shoulder, whistling.")
day('h06b', 'H06', f"A simple 1348 kitchen with a hearth: {HERO} eats bread and soup at a wooden table, a cat begging at his feet.")
room('h06c', 'H06', f"Night, moonlight through the window: {NIGHT} sleeps peacefully on his back, smiling.")
dg('h07a', 'H07', "A plain stickman outline seen from the front: a dotted arrow runs from a red dot on the ankle up the leg to a glowing dot at the top of the thigh; small dots at the armpits and neck.")
dg('h07b', 'H07', "A lymph node drawn as a little round sieve that catches small green germs while clear fluid passes through, with a determined little face.")
ins('h07c', 'H07', "Close-up of a stickman's leg in a grey wool stocking: a faint glowing dotted line travels up from the ankle toward the hip, as if seen through the cloth.")
dg('h07d', 'H07', "Close-up of the top of a stickman outline's thigh: one round lymph node glows warm orange, small rod-shaped bacteria gathering around it.")
# ---- day 3: fever
room('h10b', 'H10', f"Close-up: {NIGHT} under the thin grey blanket, teeth chattering, shivering lines, sweat on his head; bright summer sun in the window behind.")
room('h11a', 'H11', f"{NIGHT} stands by the bed and winces, shielding his eyes from a sharp beam of sunlight from the window, jagged headache lines around his head.")
room('h11b', 'H11', f"Close-up: {NIGHT}'s round head flushed pink and hot, little steam puffs rising from it, sweat drops flying.")
room('h11c', 'H11', f"{NIGHT} sits on the edge of the bed and touches his forehead with the back of his hand, worried.")
room('h13a', 'H13', f"Status-portrait composition: {NIGHT} sits on the edge of the bed facing the viewer, flushed and sweaty, in the LEFT half of the frame; the right part of the frame shows only the plain dim plaster wall.")
room('h13b', 'H13', f"{NIGHT} tries to stand up, wobbling, knees buckling, one hand on the bed post.")
room('h13c', 'H13', f"{NIGHT} collapses back onto the pillow, exhausted, arms spread.")
# ---- day 4: the bubo
room('h14b', 'H14', f"Close-up: {NIGHT} stares down at the top of his thigh, eyes huge, mouth open in shock; a round bump shows under the nightshirt cloth.")
room('h14c', 'H14', f"{NIGHT} flinches and yelps as the nightshirt cloth brushes the bump at his hip, little spark-like pain lines.")
room('h14d', 'H14', f"{NIGHT} walks stiffly across the room with his legs apart like a cowboy, wincing, because anything touching his hip hurts.")
dg('h15a', 'H15', "Cut-away of a swollen lymph node shaped like a small hard egg: inside, crowds of tiny green rod-shaped bacteria and round white defender cells fighting.")
dg('h15b', 'H15', "Close-up inside the swollen node: round white defender cells wrestle green rod-shaped bacteria in a comic dust cloud.")
room('h15c', 'H15', f"Side view: {NIGHT} stands in profile, a round egg-sized bulge clearly visible under the nightshirt at the top of his thigh (cartoon-simple, clothed).")
pl('h15d', 'H15', "The Plague sticks a new travel sticker onto his battered suitcase, very satisfied, in a dim stone street.")
# ---- day 5: the doctor
room('h18a', 'H18', f"{MUM} stands in the doorway of the room and waves urgently down the stairs, calling for help; {NIGHT} lies in bed behind her.")
room('h18b', 'H18', f"{DOCD} enters through the low door with a leather bag, chin high, very important; {MUM} bows.", (DOC,))
room('h18c', 'H18', f"{DOCD} stands in the middle of the room with his hands on his hips, proud; {NIGHT} looks up at him hopefully from the bed.", (DOC,))
room('h19b', 'H19', f"Close-up: {DOCD} sniffs a glass flask of yellow liquid with his eyes closed, like a wine expert.", (DOC,))
room('h19c', 'H19', f"{DOCD} swirls the flask of yellow liquid and peers at it against the candle, deep in thought; {NIGHT} in bed covers his face with both hands.", (DOC,))
room('h19d', 'H19', f"Close-up: {NIGHT} in bed with a mortified, disbelieving face, one eyebrow raised.")
ins('h20a', 'H20', "A grand 1348 university hall in Paris with tall gothic windows: four stickman professors in long black gowns sit at a long table and point solemnly at the ceiling.")
ins('h20b', 'H20', "Close-up: an old stickman professor in a black gown and cap points up at the sky with great certainty.")
dg('h20c', 'H20', "A night sky: three planets with grumpy faces line up in a row inside a simple star constellation of a water-bearer pouring a jug.")
dg('h20d', 'H20', "Green mist pours down from three grumpy planets in the night sky onto a tiny walled medieval city.")
room('h20e', 'H20', f"{DOCD} nods solemnly and points at the window as if the air itself is guilty; {NIGHT} looks at the window, confused.", (DOC,))
pl('h21a', 'H21', "The Plague shrugs with both palms up and an offended, confused face; the rat shrugs too.")
room('h22a', 'H22', f"{DOCD} unpacks a small lancet and a tin bowl from his leather bag with a cheerful smile; {NIGHT} watches from the bed, worried.", (DOC,))
room('h22c', 'H22', f"{NIGHT} slumps against the wall even paler than before, eyes swirling, totally drained, an arm bandaged.")
ins('h22d', 'H22', "Close-up of a small tin bowl on the bedside table, a little dark red liquid inside (not gory), the candle beside it.", (ROOM,))
ins('h23a', 'H23', "A 1348 apothecary shop: a stickman apothecary stirs a big bubbling cauldron; jars, a honey pot and red poppies on shelves.")
ins('h23b', 'H23', "Close-up of the cauldron: a grumpy cartoon viper pokes its head out of the bubbling brown syrup.")
ins('h23c', 'H23', "Shelf close-up in the apothecary shop: a honey pot, a bunch of red poppies and many small clay jars.")
room('h23d', 'H23', f"{MUM} spoon-feeds {NIGHT} a dark syrup; he makes a disgusted face, eyes watering.")
room('h23e', 'H23', f"Close-up: {NIGHT} gagging, tongue out, after swallowing the syrup.")
room('h24a', 'H24', f"{DOCD} stands in front of a wooden bath tub with steaming water and spreads his arms to block it, shouting.", (DOC,))
room('h24b', 'H24', f"{NIGHT} sniffs his own armpit and recoils; little stink lines and two flies circle.")
room('h25a', 'H25', f"{DOCD} sets up two big iron braziers with roaring fires on both sides of the bed, very pleased.", (DOC,))
room('h25b', 'H25', f"{NIGHT} sits on a stool exactly between the two blazing braziers, sweating buckets, giving the viewer a deadpan 'are you serious?' look; {DOCD} gives a thumbs-up.", (DOC,))
room('h25c', 'H25', f"Close-up: {NIGHT}'s face between the two fires, dripping with sweat, deadpan, orange firelight.")
ins('h25d', 'H25', "A stone hall of the papal palace in Avignon: a stickman pope in white robes and a tall white mitre sits on a throne exactly between two big fires, sweating, deadpan.")
ins('h25e', 'H25', "Close-up: the stickman pope's face between the fires, the exact same deadpan sweaty expression, orange firelight.")
# ---- day 6: three paths
ins('h29a', 'H29', f"A dusty crossroads at dusk with three wooden signposts pointing three ways (blank boards): {NIGHT.replace('exactly as in the reference: ', '')} stands at the junction, lost.", (ROOM, STYLE_REF))
pl('h29b', 'H29', "The Plague stands at a dusty crossroads with three signposts and gestures at the roads like a game-show host.")
dg('h30a', 'H30', "A red river of blood seen from above: dozens of tiny green rod-shaped bacteria sail down it on little boats, spreading everywhere.")
dg('h30b', 'H30', "A large hand outline with simple blood vessels; small dark clots block the vessels at the fingertips, and the fingertips are shaded dark grey-blue.")
ins('h30c', 'H30', "Close-up of a stickman's black mitten hand resting on a grey blanket, its tips turning darker, a sad, quiet mood.", (ROOM,))
dg('h30d', 'H30', "A blood vessel tube cut open: tiny dark clots jam it like a traffic jam.")
pl('h30e', 'H30', "The Plague, grim and satisfied, chalks another tally mark on a stone wall.")
ins('h30f', 'H30', "The first of three dusty roads leads into a dark, gloomy forest; its wooden signpost leans.")
room('h31a', 'H31', f"{NIGHT} lets out a huge cough that becomes a big greenish cloud; two visiting stickman neighbours leap backwards in horror.")
ins('h31b', 'H31', "Close-up: two stickman neighbours in medieval clothes flee down a narrow stairway, covering their mouths.")
dg('h31c', 'H31', "A pair of lungs drawn like two sponges, speckled with tiny green dots.")
dg('h31d', 'H31', "A coughing stickman outline: tiny droplets with green dots fly out in a cone toward three other stickman outlines; arrows.")
pl('h31e', 'H31', "The Plague rubs his spotted hands together with delight, the rat grinning.")
ins('h31f', 'H31', "The second dusty road disappears into a thick grey fog; its signpost is cracked.")
dg('h32a', 'H32', "A lymph node drawn as a small stone castle on a hill: little round white defender cells stand on the walls.")
dg('h32b', 'H32', "The castle gate: round white defender cells push back an army of small green rod-shaped bacteria.")
ins('h32c', 'H32', "The third dusty road leads toward a sunrise over green hills; its signpost stands straight.")
pl('h33a', 'H33', "Close-up: The Plague flips a big gold coin high into the air with his thumb, grinning; the rat watches it spin.")
room('h34a', 'H34', f"Night, the candle burned low: status-portrait composition, {NIGHT} propped on the pillow facing the viewer, pale grey-blue face, glassy half-closed eyes, in the LEFT half of the frame; the right part shows only the dark wall.", (DAY,))
room('h34b', 'H34', f"Night: close-up of {NIGHT}'s pale grey-blue face on the pillow, glassy eyes, a wet cloth on his forehead.")
room('h34c', 'H34', f"Night: {MUM} sits on a stool by the bed and gently wipes his forehead with a cloth by the light of a low candle.")
ins('h35a', 'H35', "Close-up: a gold coin lands flat on a wooden floor, bright morning light falling on it.")
room('h35b', 'H35', "Dawn: the first warm sunlight pours through the small window across the empty floor of the room; peaceful.")
room('h36a', 'H36', f"Morning sunlight: {NIGHT} sits up in bed, colour back in his face, a small tired smile.")
room('h36b', 'H36', f"Morning: {NIGHT} stretches his arms weakly, yawning.")
room('h36c', 'H36', f"Close-up: {NIGHT} touches a clean linen bandage at his hip with relief.")
room('h36d', 'H36', f"{MUM} brings a steaming bowl of soup; {NIGHT} reaches for it, smiling.")
room('h36e', 'H36', f"{NIGHT} eats soup in bed with a spoon, happily.")
room('h37a', 'H37', f"Status-portrait composition: {NIGHT} sits up in bed with a bowl of soup facing the viewer, pale but smiling, in the LEFT half of the frame; the right part shows only the plain wall.")
ins('h37b', 'H37', "A narrow medieval street: three thin stickman survivors in plain clothes with bandages shuffle out of their doors into the sun, blinking.")
room('h37c', 'H37', f"{NIGHT} gives a weak thumbs-up from the bed.")
pl('h38a', 'H38', "The Plague walks away down a dim stone street with his suitcase, his back to the viewer, waving over his shoulder; the rat looks back.")
day('h39a', 'H39', f"{HERO}, thinner, steps out of a stone doorway leaning on a wooden walking stick, squinting at the bright sun.")
ins('h39b', 'H39', f"{STREET}, now empty and silent: the fruit stall covered with cloth, shutters closed, one cat sitting on the cobbles.", (DAY, STYLE_REF))
ins('h39c', 'H39', "A row of closed wooden shutters and doors on a quiet medieval street, a few marked with painted crosses.")
dg('h39d', 'H39', "An old map of Europe and the Mediterranean with simple coastlines; dark grey shading spreads across it from the south-east, small arrows.")
day('h39e', 'H39', f"Status-portrait composition: {HERO}, thinner, leaning on his walking stick in the empty street, facing the viewer, in the LEFT half of the frame; the right part shows a plain stone wall.")
# ---- today
mod('t01a', 'T01', f"A dry hiking trail in the American southwest with red rocks: {MODHERO} walks happily.")
mod('t01b', 'T01', "Close-up: a tiny flea crouches on a white sports sock above a hiking boot.")
mod('t03a', 'T03', f"A bright modern clinic: {MODHERO} sits on an exam table pointing at his hip, worried; a stickman doctor with a ponytail in a white coat listens.")
mod('t03b', 'T03', "The stickman doctor with a ponytail in a white coat holds up a small sample tube and looks at it carefully.")
mod('t03c', 'T03', "A modern lab: a computer screen shows a microscope image of small rod-shaped bacteria; a stickman lab worker points at it.")
mod('t03d', 'T03', "Comic insert: an old-fashioned glass flask of yellow liquid flies out of a modern clinic window with motion lines.")
mod('t04a', 'T04', "Close-up: a black mitten hand holds a blister pack of white pills.")
mod('t04b', 'T04', f"{MODHERO} takes a pill with a glass of water at a kitchen counter.")
mod('t04c', 'T04', f"{MODHERO} relaxes on a sofa under a blanket, feeling better, a cat on his lap.")
mod('t05a', 'T05', f"{MODHERO} stands outside the clinic, stretching happily in the sun.")
mod('t05b', 'T05', f"Evening campfire on a desert trail: {MODHERO} toasts a marshmallow on a stick and winks at the viewer.")
mod('t05c', 'T05', "The stickman doctor with a ponytail in a white coat gives a thumbs-up and smiles.")
# ---- ending
day('e01a', 'E01', f"In {STREET}: {HERO} leans on the fruit stall holding a peach and looks straight at the viewer with one eyebrow raised.")
ins('e01b', 'E01', "The three dusty roads with their signposts seen from above at sunset.")
pl('e01c', 'E01', "The Plague peeks around a stone corner at the viewer with a sly grin.")
ins('e02a', 'E02', "A dark medieval village doorway at night: a growling cartoon dog with wild eyes and frothy drool stands in it. Funny-scary, not gory.")
day('e02b', 'E02', f"Night: {HERO} backs away down a street holding a lantern, terrified.")

if __name__ == '__main__':
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frames_v2_todo.json')
    json.dump(F, open(out, 'w'), indent=1); print(len(F), 'frames ->', out)
