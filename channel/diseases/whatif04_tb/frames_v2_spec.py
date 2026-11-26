"""TB v2 frames (London 1850). Stage A: new location masters + frames that need no new master. Stage B: edit chains (mirror, atlas, handkerchief)."""
import json, sys
STYLE='557f5d94-d7bb-494f-bfa1-5a92bfffb8b5'; LADY='1de80806-b140-40d9-8e0b-9a3a526ecee8'
ROOM='9c809db2-3560-4517-ae6a-dc3bdbf33ffb'; MIR='28d3da00-9350-4451-be4a-ffdbdfc9df48'; ATLAS='89440100-3626-481d-b4d4-8c3c9663237f'
CLINIC='7298fb19-0ec5-4ebe-8245-6b926b539383'
M=json.load(open('masters_v2.json')) if len(sys.argv) > 1 and sys.argv[1] == 'B' else {}
SN=("All people are simple cartoon stickmen: big plain smooth white round head with a black outline and NO hair, two dot eyes, simple mouth and eyebrows, no nose; "
    "thin BLACK stick arms and legs (never skin-coloured), small black mitten hands. Medium-wide shot, every person fully visible from head to feet. "
    "Anatomy: every person has exactly one head, two arms from the shoulders, two mitten hands, two legs; each hand holds at most one thing. No text, no readable writing, no numbers. Not gory. ")
KEEP="Edit the FIRST reference image. Keep EXACTLY the same place, drawing style, palette, camera angle and every piece of furniture, window and wall; do not add or remove furniture. "
HERO="the young clerk from the SECOND reference image (same stickman: dark brown frock coat, cream waistcoat, white shirt, black neck-tie)"
DOC="a doctor of 1850: a stickman in a black frock coat, a tall black top hat, a white high collar"
NEW=("2D animated history explainer frame, 16:9, no text. Same ink-and-fine-cross-hatching drawing style and muted sepia palette as the reference. London 1850, no electric light, no clock tower. ")
DIAG=("Hand-drawn explainer diagram in ink and muted watercolour on aged paper, 16:9, same style as the reference, no words, no letters, no numbers. ")
F=[]
def add(i, line, prompt, refs): F.append({'id': i, 'line': line, 'prompt': prompt, 'refs': refs})
if not M:
    add('m_office','P01',NEW+"Background, NO PEOPLE: an 1850 London counting house: a row of tall slanted wooden clerks' desks with high stools, ledgers and inkpots, tall dusty windows with grey daylight, a wooden floor. Straight-on camera.",[STYLE])
    add('m_street','C04',NEW+"Background, NO PEOPLE: a foggy London street in 1850: brick terraced houses, a narrow pavement, a horse-drawn cab waiting in the fog, chimney smoke, grey sky. Straight-on camera at eye level, open pavement in the middle.",[STYLE])
    add('m_stairs','Y1C',NEW+"Background, NO PEOPLE: the narrow wooden staircase of an 1850 London lodging house, worn wooden steps going up to the right, a simple wooden banister, peeling wallpaper, a small window with grey light at the top. Medium-wide shot.",[STYLE])
    add('m_hanky','M1B',NEW+"Close-up still life, NO PEOPLE: a clean folded white linen handkerchief with a thin plain hem lying on a dark wooden table top next to a candle in a brass holder. Nothing else.",[STYLE])
    add('m_park','Y2G',NEW+"Background, NO PEOPLE: a London park in early spring 1850: a gravel path, bare trees with first green buds, a wooden bench, a pale sun in the mist. Straight-on camera.",[STYLE])
    add('y2d','Y2D',DIAG+"A simple country road seen from behind a small stickman outline standing at a fork, where the road splits into three paths going into the distance: the left path goes down into dark fog, the middle path goes on flat and grey, the right path goes up toward a faint sunrise.",[STYLE])
    add('t02','T02',NEW.replace('London 1850, no electric light, no clock tower. ','Present day. ')+"Close-up still life, NO PEOPLE: a modern plastic weekly pill organizer with coloured pills in its compartments, next to a printed wall calendar page with many small square day boxes, most of them crossed out with a pen. No readable text, no numbers.",[STYLE])
    add('t03','T03',DIAG+"A world map in ink and muted watercolour with many small red dots clustered over South and South-East Asia and Africa, fewer elsewhere.",[STYLE])
    add('t04','T04',"Tuberculosis as 'the White Lady' exactly as on the reference sheet (gaunt woman, waxy grey-white skin, red cheek blotches, dark-ringed eyes, long dark hair, tattered off-white nightgown, grey knitted shawl, lit candle in a brass holder) stands in a modern 2020s city street at dusk among glass buildings, smiling ironically at the viewer, one hand raised in a little wave. Ink-and-cross-hatching style, muted palette, not horror. Exactly one figure, two arms, two hands. No text, no signs.",[LADY,STYLE])
    add('t01','T01',KEEP+SN+"The hero in modern clothes (a stickman in a dark grey hoodie and jeans) sits by the desk; a stickman doctor in blue scrubs and a blue scrub cap stands at the lit X-ray box on the wall and points at a bright white patch in the upper part of the lung picture.",[CLINIC])
else:
    H=M['mir1']
    def room(i, line, p, extra=()): add(i, line, KEEP+SN+p, [ROOM, H]+list(extra))
    add('c04n','C04',KEEP+SN+f"{HERO} walks out of a door on the left onto the foggy pavement, coughing into his fist, tired.",[M['m_street'],H])
    add('p01o','P01',KEEP+SN+"Four clerks (stickmen in dark frock coats) stand at the tall desks writing in ledgers; the one in the middle coughs into the air, a faint cloud drifting toward the others. Nobody touches anybody.",[M['m_office']])
    add('p03s','P03',KEEP+SN+"A crowd of six 1850 Londoners (stickmen in dark coats, top hats and bonnets) walk along the foggy pavement in both directions; in the chest of four of them a tiny round grey stone lump glows faintly through the clothes, like an X-ray.",[M['m_street']])
    room('p05r','P05',f"Night, cold blue light, one candle: {HERO} sits on the chair at the small table in the middle of the room doing accounts in a ledger by the candle, a thin blanket round his shoulders, a small puff of breath vapour from his mouth.")
    room('m1d','M1D',f"Day: {DOC} stands by the bed holding a big spoon of yellow oil toward {HERO}, who sits on the bed and leans away, grimacing in disgust; a brown bottle in the doctor's other hand.")
    room('m6b','M6B',f"Night, blue light: {HERO}, now in a long off-white nightshirt, sits up in the bed, the grey sheets around him dark and soaked with sweat, sweat drops on his round head, exhausted.")
    room('m6d','M6D',f"Day: {HERO} lies on the bed in his white shirt; {DOC} stands beside the bed holding a small glass jar with three small dark leeches inside, about to put one on the hero's chest; the hero looks at the jar, worried. Not gory.")
    room('m6e','M6E',"No people except one figure: Tuberculosis as 'the White Lady' exactly as on the THIRD reference sheet (gaunt woman, waxy grey-white skin, red cheek blotches, dark-ringed eyes, long dark hair, tattered off-white nightgown, grey knitted shawl), standing by the bed, holding a small glass jar with dark leeches up to the light and smiling at it with ironic delight. Exactly one figure, two arms, two hands.",[LADY])
    room('y1a','Y1A',f"Day: {HERO} stands in the middle of the room staring in horror at an open white handkerchief in his hands with a bright red stain on it; shock lines around his head. Not gory.")
    add('y1c','Y1C',KEEP+SN+"On the stairs a small boy (a stickman boy in a brown jacket, short trousers and a flat cap) sits on a step and coughs into his fist; his mother (a stickman woman in a grey dress, white apron and white cap) stands two steps below and looks at him, worried.",[M['m_stairs']])
    room('y1d','Y1D',f"Day: {HERO}, visibly thinner, stands at the window looking out with a dreamy, hopeful smile, one hand on his chest, a few small sparkles of optimism around his head.")
    room('y1e','Y1E',f"Evening, candle: {HERO}, thinner, sits on the chair at the small table counting a few small coins in his hand with a sad face; above his head a thought bubble shows a steamship and palm trees on a sunny island.")
    add('y2b','Y2B',KEEP+SN+f"{HERO}, very thin, his frock coat hanging loose, stops halfway up the stairs, clinging to the banister with both hands, out of breath, head down.",[M['m_stairs'],M['mir3']])
    room('y2e','Y2E',"Night: the room is empty and dark, nobody in it; the bed is neatly made, the brown frock coat hangs on the chair, the candle on the table has just gone out with a thin wisp of smoke. Quiet and sad.")
    room('y2f','Y2F',f"Day: {HERO}, very thin and grey, lies in the bed in a nightshirt, coughing; at the door the landlady (stickman woman in grey dress, white apron, white cap) and her small son (brown jacket, flat cap) stand and both cough into their fists too.")
    add('y2g','Y2G',KEEP+SN+f"{HERO}, thin and pale but smiling, walks slowly along the gravel path with a walking stick, enjoying the pale sun.",[M['m_park'],M['mir2']])
    room('y2h','Y2H',"One figure only: Tuberculosis as 'the White Lady' exactly as on the THIRD reference sheet (gaunt woman, waxy grey-white skin, red cheek blotches, dark-ringed eyes, long dark hair, tattered off-white nightgown, grey knitted shawl) sits on the chair by the bed with her lit candle, holding up three fingers with a calm, ironic smile at the viewer. Exactly one figure, two arms, two hands.",[LADY])
    add('e01','E01',KEEP+SN+f"{HERO} (healthy, as in Month 1) stands on the foggy pavement facing the viewer, one eyebrow raised, hands in his coat pockets, as if asking the viewer a question.",[M['m_street'],H])
    # handkerchief chain
    add('hk2','M6C',"Edit the reference image. Keep EXACTLY the same handkerchief, table, candle, framing and style. Change ONLY: one small pink speck of blood in the middle of the handkerchief. No text.",[M['m_hanky']])
    add('hk3','Y1A',"Edit the reference image. Keep EXACTLY the same handkerchief, table, candle, framing and style. Change ONLY: the handkerchief is now unfolded and crumpled, with a bright red blood stain the size of a coin in the middle. Not gory. No text.",[M['m_hanky']])
    # atlas chain: disease always in the lung on the VIEWER'S LEFT
    A="Edit the reference engraving page. Keep EXACTLY the same page, paper, border, drawing style and the same lungs. NO words, NO letters, NO numbers. Change ONLY this: "
    add('at1','M1C',A+"in the upper part of the lung on the LEFT side of the picture, a small round greyish-yellow walled-off nodule the size of a pea, with a darker blotchy patch starting to spread around it.",[ATLAS])
    add('at2','Y1B',A+"in the upper part of the lung on the LEFT side of the picture, a ragged dark hollow cavity the size of a walnut with a crumbling yellowish rim, a thin red trickle where a small blood vessel at its edge is broken; small grey nodules around it. Not gory.",[ATLAS])
    add('at3','Y2C',A+"BOTH lungs now have several ragged dark hollow cavities with crumbling yellowish rims in their upper halves (the biggest one in the upper part of the lung on the LEFT side of the picture), and many small grey nodules; the lung tissue is darker and blotchy. Not gory.",[ATLAS])
    add('at4','Y2G',A+"in the upper part of the lung on the LEFT side of the picture, a closed-up, healed scar: a small puckered whitish-grey star-shaped scar with a thin chalky rim where a cavity used to be; the rest of the lungs is pink.",[ATLAS])
if __name__=='__main__':
    R=[{'index':k,'params':{'model':'gpt_image_2_5','prompt':f['prompt'],'quality':'low','resolution':'1k','aspect_ratio':'16:9','medias':[{'value':r,'role':'image_references'} for r in f['refs']]}} for k,f in enumerate(F)]
    tag='B' if M else 'A'
    json.dump({'a':R[:12],'b':R[12:24],'c':R[24:],'ids':[f['id'] for f in F]},open(f'frames_v2_{tag}.json','w'),indent=1)
    json.dump(F,open(f'frames_v2_{tag}_todo.json','w'),indent=1)
    print(tag,len(F),[f['id'] for f in F])
