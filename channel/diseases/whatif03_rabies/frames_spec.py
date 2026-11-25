"""What If #3 (rabies, 1885): frame list. Every frame is an EDIT of a master (see tools/QC.md).
python3 frames_spec.py -> frames_todo.json  [{id, line, prompt, refs, stage}]
stage 1 needs only the masters; stage 2 needs the lab master (h12a) made in stage 1.
"""
import json, os
STYLE = '557f5d94-d7bb-494f-bfa1-5a92bfffb8b5'
STREET = '499e9dc8-cee6-4e93-a559-9fb7c886c373'    # m_street: lane, gate, hero in cap + blue smock, dog
ROOM = 'a2273ac4-c44e-440c-82a5-e60dc1e39d31'      # m_room: farmhouse bedroom, hero in nightshirt
RAB = 'b9ff30e0-3f5c-452b-84d9-79d546fb2b9e'       # m_rabies: Rabies at the gate
SHEET = '952b15fd-22dd-4d51-a743-d9c04adb1b46'     # Rabies character sheet
DIAG = '32fe4905-e9f3-4262-9dc4-e885d339919c'      # m_diag: nerve diagram with dog bite
LAB = 'a46d4de2-97e1-4b83-bb73-d7326ed35bd5'   # h12a, the lab master

KEEP = ("Keep EXACTLY the same drawing style, palette, camera angle and setting as the FIRST reference image; do not move or redraw the furniture or buildings. "
        "Humans are simple stickmen: plain smooth white round head with NO hair, two dot eyes, simple mouth and eyebrows, no nose, thin black stick arms and legs, small solid black mitten hands. "
        "Each figure has exactly two arms and two hands. No text, no letters. Not gory. ")
HERO = "the hero (same stickman as in the reference: flat dark-grey cloth cap, loose faded blue work smock, brown trousers)"
NIGHT = "the hero (same bald stickman as in the reference, long off-white nightshirt)"
MUM = "his mother, a stickman in a plain black dress and a white linen bonnet"
PRIEST = "the village priest, a stickman in a long black cassock and a round black wide-brimmed hat"
PASTEUR = "Louis Pasteur as a simple stickman (no beard) in a black frock coat and a small black skullcap"
MOD = ("2D animated explainer frame, 16:9, no text. Same ink-and-cross-hatching drawing style and muted palette as the reference, but the setting is the present day (2020s). "
       "Humans are simple stickmen: smooth white round heads with no hair, dot eyes, black stick limbs, small black mitten hands. Exactly two arms each. Not gory. ")
MODHERO = "the hero today (white round head, dark-grey baseball cap, blue jacket, jeans)"

F = []
def e(i, line, master, p, extra=(), stage=1): F.append({'id': i, 'line': line, 'prompt': 'Edit the FIRST reference image. ' + KEEP + p, 'refs': [master] + list(extra), 'stage': stage})
def street(i, line, p): e(i, line, STREET, p)
def room(i, line, p): e(i, line, ROOM, p)
def rab(i, line, p): F.append({'id': i, 'line': line, 'prompt': 'Same drawing style and the same character as the references. Rabies exactly as in the first reference (wolf-dog head, yellow eyes, a little froth, broken collar with chain, ragged dark frock coat), cartoon-theatrical, exactly one Rabies, two arms. No text. No street lamps. ' + p, 'refs': [RAB, SHEET], 'stage': 1})
def diag(i, line, p): F.append({'id': i, 'line': line, 'prompt': 'Same diagram style as the reference (ink and muted watercolour on aged paper, drawn arrows, no words, no letters, no numbers, plain stickman outlines). ' + p, 'refs': [DIAG], 'stage': 1})
def lab(i, line, p): e(i, line, LAB, p, (STYLE,), stage=2)
def mod(i, line, p): F.append({'id': i, 'line': line, 'prompt': MOD + p, 'refs': [STYLE], 'stage': 1})
def one(i, line, p, refs=(STYLE,)): F.append({'id': i, 'line': line, 'prompt': '2D animated history explainer frame, 16:9, no text. Same drawing style and palette as the reference (ink, fine cross-hatching, muted sepia). Humans are simple stickmen: smooth white round heads with no hair, dot eyes, black stick limbs, small black mitten hands; exactly two arms each. Not gory. No street lamps. ' + p, 'refs': list(refs), 'stage': 1})

# cold open
street('c01b', 'C01', f"Closer view of the same lane: {HERO} stops and looks warily at the dog behind the gate, holding his bread tight.")
street('c01c', 'C01', "Close-up of the dog behind the same wooden gate: drooling, wild yellow eyes, snapping at the air. No people.")
street('c02a', 'C02', f"The dog has jumped over the gate and bites {HERO} on the forearm through his blue sleeve; the bread flies into the air; motion lines. Not gory, no blood.")
street('c02b', 'C02', f"Close-up of the hero's forearm with the blue sleeve pushed up: two small red bite marks on a black stick arm. No blood.")
street('c04a', 'C04', f"{HERO} stands alone in the lane clutching his forearm, looking worried; the dog runs off in the distance; the bread lies on the ground.")
rab('c04b', 'C04', "Close-up at the same wooden farm gate: Rabies grins at the viewer and holds up one clawed finger.")
# day 0
diag('h01b', 'H01', "One large magnified bullet-shaped virus particle covered in tiny spikes, next to a drop of saliva drawn as a big droplet full of the same tiny bullets.")
diag('h02a', 'H02', "Close-up of a nerve drawn as a long cable running up an arm: tiny bullet-shaped viruses crawl along inside it in a line, with arrows pointing up toward the shoulder.")
rab('h03a', 'H03', "Rabies strolls slowly along the same village lane at dusk with his hands behind his back, relaxed and smug.")
room('h03b', 'H03', f"{NIGHT} sits on the edge of the bed with a white bandage around his forearm, looking annoyed, arms crossed.")
# village medicine
room('h04a', 'H04', f"{PRIEST} stands by the table holding an iron key with tongs over a small iron pan of glowing coals; the key glows red; {NIGHT} sits on the bed, worried.")
room('h04b', 'H04', f"{PRIEST} presses the glowing key to the hero's forearm; a small puff of smoke; {NIGHT} squeezes his eyes shut and grits his teeth. Not gory.")
room('h05a', 'H05', f"{NIGHT} blows on his forearm with a pained face; {PRIEST} gives a small apologetic shrug.")
room('h06a', 'H06', f"{MUM} carefully places a small tuft of brown dog hair on the hero's forearm with great seriousness; {NIGHT} looks at it, very doubtful.")
room('h06b', 'H06', f"Close-up of the hero's forearm resting on the brown blanket: a little tuft of brown dog hair lies on two small bite marks.")
rab('h07a', 'H07', "Rabies laughs so hard he slaps his knee, leaning on the same wooden gate.")
# quiet weeks
street('h08a', 'H08', f"Late autumn: {HERO} splits firewood with an axe in the lane next to a woodpile, cheerful.")
room('h08b', 'H08', f"{NIGHT} sits at the table eating soup from a bowl, happy.")
room('h08c', 'H08', f"Night, dark blue window: {NIGHT} sleeps peacefully in the bed, smiling.")
diag('h09a', 'H09', "The same stickman outline as the reference: now the tiny bullet-shaped viruses have crawled up the nerve past the elbow and into the shoulder; the bite on the forearm has healed into two small scars.")
diag('h10a', 'H10', "The same stickman outline as the reference: the tiny viruses have reached the spinal cord and swarm into the brain, which glows red.")
# the choice
room('h11a', 'H11', f"{NIGHT} stands by the window reading a folded newspaper, eyes wide with hope.")
one('h12a', 'H12', f"A 1885 Paris laboratory: wooden benches with glass flasks and a microscope, rabbit cages stacked by the wall, tall windows. {PASTEUR} gently gives an injection with a glass syringe into the side of the belly of a small boy stickman (Joseph Meister, nine years old, in a sailor shirt) who sits on a stool; the boy's mother stands beside him.")
one('h12b', 'H12', "Close-up of stacked wooden rabbit cages with white rabbits in a 1885 laboratory, glass flasks on a bench. No people.")
room('h13a', 'H13', f"{NIGHT} sits on the edge of the bed holding a train ticket in one hand and the newspaper in the other, thinking hard.")
rab('h14a', 'H14', "Rabies holds a white rabbit up by the scruff with one hand and raises an eyebrow at it, mocking; at the same farm gate.")
# stay home
room('h15a', 'H15', f"Day: {NIGHT} sits on the bed and scratches the two old scars on his forearm, uneasy.")
room('h15b', 'H15', f"Day: {NIGHT} lies in bed under the brown blanket, sweaty and flushed, with a headache, a wet cloth on his forehead.")
room('h16a', 'H16', f"Night, dark window, candle: {NIGHT} sits bolt upright in bed, eyes huge, startled by the creaking door, shock lines.")
room('h16b', 'H16', f"Night: {NIGHT} paces the floor nervously, hands clasped, unable to sleep.")
room('h17a', 'H17', f"Day: {NIGHT} stands at the table lifting the tin cup of water toward his mouth, but recoils, one hand at his throat, cramp lines around his neck.")
room('h17b', 'H17', f"Day: {NIGHT} turns his face away from the tin cup and jug on the table, frightened of it, hands raised.")
room('h18a', 'H18', f"Day: {MUM} opens the small window; a breeze blows in (drawn as wind lines); {NIGHT} on the bed flinches and covers his face.")
room('h18b', 'H18', f"Day: status portrait: {NIGHT} sits on the edge of the bed facing the viewer, pale, sweaty, wide frightened eyes.")
rab('h19a', 'H19', "Rabies takes an elegant theatrical bow, one hand on his chest, at the same wooden gate.")
room('h20a', 'H20', f"Day: {NIGHT} lies weakly in bed, a small drop of drool at the corner of his mouth, eyes half closed. Not gross.")
room('h21a', 'H21', "Night: the same room in darkness, the candle just blown out with a thin wisp of smoke, the bed empty and neatly made, the blanket folded. No people. Quiet and sad.")
# Paris
one('h22a', 'H22', f"Inside an 1885 third-class railway carriage with wooden benches: {HERO} sits by the window with a bandaged forearm, looking out at passing snowy countryside, determined.")
one('h22b', 'H22', "An 1885 steam train arriving under the iron-and-glass roof of a Paris railway station, steam clouds, passengers with luggage.")
lab('h23a', 'H23', f"A wooden bench along the lab wall: a row of bitten people waiting (a shepherd boy, a woman, an old man), each with a bandage on an arm or leg; {HERO} sits at the end of the bench.")
lab('h23b', 'H23', f"{PASTEUR}'s assistant, a stickman in a white apron, gives {HERO} an injection with a glass syringe into the side of his belly; the hero lifts his smock and winces.")
lab('h23c', 'H23', "Close-up of a lab bench: a row of tall glass jars, each with a thin dried strip hanging inside on a thread; the strips get paler from left to right. No people.")
diag('h24a', 'H24', "The same stickman outline as the reference: little round shield-carrying defender cells race up the nerve and catch the tiny bullet-shaped viruses before they reach the shoulder.")
lab('h25a', 'H25', f"Outside view through the lab windows: a happy crowd of recovered patients with bandages leaving, waving; {PASTEUR} watches with his hands behind his back.")
rab('h26a', 'H26', "Rabies sulks with his arms crossed and his ears flat, kicking a pebble in the same village lane.")
room('h27a', 'H27', f"Day: {NIGHT} sits on the bed healthy and smiling, showing two small faded scars on his forearm; {MUM} beside him, relieved.")
one('h27b', 'H27', "The gate of the Pasteur Institute in Paris in the 1890s: a grown-up stickman caretaker in a dark uniform and cap holds a ring of keys and smiles.")
# today
mod('t01a', 'T01', f"A modern village street: a stray dog bites {MODHERO} on the forearm through his jacket sleeve; motion lines. Not gory.")
mod('t02a', 'T02', f"A modern bathroom sink: {MODHERO} washes his forearm with soap under running water, looking at a clock on the wall.")
mod('t02b', 'T02', f"A modern clinic: a stickman nurse in blue scrubs gives {MODHERO} a vaccine injection in the upper arm.")
mod('t03a', 'T03', f"{MODHERO} walks out of the clinic, relieved, giving a thumbs-up.")
one('t04a', 'T04', "Hand-drawn world map in ink and muted watercolour on aged paper, with many small red dots clustered over South and Southeast Asia and Africa. No words, no letters, no numbers.", (DIAG,))
mod('t04b', 'T04', "A dusty rural village road far from any town, a small stickman child walking with a stray dog, a long empty road to the horizon.")
mod('t05a', 'T05', "Rabies, the wolf-dog-headed gentleman from the reference sheet, lurks in the shadow of a modern alley next to a rubbish bin, grinning at the viewer.")
F[-1]['refs'] = [SHEET, STYLE]
# ending
one('e01a', 'E01', f"An 1885 village railway platform in the Jura: {HERO} holds a train ticket, looks straight at the viewer with one eyebrow raised; a steam train waits.", (STREET,))

if __name__ == '__main__':
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frames_todo.json')
    json.dump(F, open(out, 'w'), indent=1); print(len(F), 'frames;', sum(f['stage'] == 2 for f in F), 'in stage 2')
