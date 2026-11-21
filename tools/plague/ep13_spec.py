"""Episode 13 (The ENTIRE History of Measles): single source of truth. Same format as ep12_spec.py.

  python3 tools/plague/ep13_spec.py lines   -> voice list (id|ROLE|text), roles NARRATOR / MEASLES
  python3 tools/plague/ep13_spec.py frames  -> tools/plague/ep13_frames_todo.json
  python3 tools/plague/ep13_spec.py beats   -> tools/plague/ep13_beats.json (for beats.py)
"""
import sys, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
K_SHEET = '2657461c-b69a-4cb1-b444-66176fd591df'   # channel/plague/sheets/measles_a.jpg ('the Red Jester'), Higgsfield job
STYLE = ("2D animated history explainer frame, 16:9, no text. Hand-drawn ink illustration, clean black outlines, fine cross-hatching, muted palette of "
         "faded scarlet, cream, slate blue and sepia with soft warm lamp light or pale daylight. Not gory.")
MODERN = ("2D animated history explainer frame, 16:9, no text. Hand-drawn ink illustration, clean black outlines, the same muted palette, soft natural daylight. "
          "The setting is modern (2000s-2020s): nothing old-fashioned. Not gory.")
SN = ("Humans are simple STICKMEN: plain white round head, two dot eyes, no nose, no beard, thin black stick arms and stick legs, small black mitten hands, "
      "dressed exactly as described for this scene and era; anyone wearing glasses has his two dot eyes INSIDE the lenses and no other eyes. "
      "Only the few figures described, standing apart, never overlapping; each has exactly two arms and two hands; every arm comes straight out of its own shoulder "
      "and never bends around or behind an object; every bare arm is a thin black stick line, never a thick or skin-coloured human arm; "
      "head, body and feet of each figure face the same way, no twisted bodies; "
      "hands are empty unless an object is described; nothing floating; no flags, no banners; no readable text.")
KING = ("Measles exactly as on the attached sheet, 'the Red Jester': a lanky, giggling court jester in a faded cream-and-scarlet harlequin diamond costume "
        "with puffed sleeves and puffed breeches, a floppy two-pointed scarlet-and-cream jester's cap with little brass bells, a stiff white ruff collar, "
        "curled pointed scarlet shoes and black gloves; his pale face is speckled with small red spots, red-rimmed watery eyes, a red runny nose and a wide mischievous grin; "
        "a faint wisp of pink mist drifts from his mouth. Exactly ONE of him, with exactly two arms and two black-gloved hands; each arm comes from its own shoulder; "
        "no extra hands anywhere in the picture. He holds AT MOST ONE object, his other hand empty and clearly attached to its own arm.")
DIAG = ("Draw ONLY the diagram described below, filling the whole frame, as ONE single picture: no extra rows, no extra panels, no comic strips above or below it. "
        "A hand-drawn explainer diagram in ink and muted watercolour on aged paper, clean and readable like an old textbook plate, "
        "numbered stages as small circled digits with drawn arrows. No words, no letters, no numbers on axes, only circled digits. Not gory. ")
NOPEOPLE = ' No people and no human figures anywhere in the picture.'
SPOTS = "his round white head covered in small red spots"
def W(): return [[.5, .5, 1.0], [.5, .5, 1.04]]
def WL(): return [[.48, .5, 1.03], [.52, .5, 1.03]]
def WR(): return [[.52, .5, 1.03], [.48, .5, 1.03]]
def C(x, y, z=1.3): z = 1 + (z - 1) * .35; return [[x, y, z], [x, y, z + .02]]
def O(): return [[.5, .5, 1.05], [.5, .5, 1.0]]
STILL = [[.5, .5, 1.0], [.5, .5, 1.02]]

def sh(img, cam=None, prompt=None, refs='', text=None, sfx=None, w=1):
    s = {'img': img, 'cam': cam or W(), 'w': w}
    if prompt: s['prompt'] = prompt; s['refs'] = refs
    if text: s['text'] = text
    if sfx: s['sfx'] = sfx
    return s
def cap(t, **k): return {'text': t, 'x': 960, 'y': 985, 'size': 50, 'at': .3, **k}
def label(t, x, y, size=64, **k): return {'text': t, 'x': x, 'y': y, 'size': size, 'at': .3, **k}
def ch(img, cam, p, modern=False, **k): return sh(img, cam, (MODERN if modern else STYLE + ' ') + SN + ' ' + p, **k)
def kg(img, cam, p, **k): return sh(img, cam, STYLE + ' ' + KING + ' ' + p + ' No other people.', 'K', **k)
def dg(img, p, people=False, **k): return sh(img, STILL, STYLE + ' ' + (SN + ' ' if people else '') + DIAG + p + ('' if people else NOPEOPLE), **k)
def ob(img, p, cam=None, modern=False, **k): return sh(img, cam or C(.5, .5, 1.05), (MODERN if modern else STYLE) + ' ' + p + NOPEOPLE, **k)

B = []
def N(i, t, *s): B.append((i, 'NARRATOR', t, list(s)))
def HOLD(sec, *s): B.append((None, None, sec, list(s)))
def K(i, t, *s): B.append((i, 'MEASLES', t, list(s)))

ROOM62 = "a cosy 1962 English country cottage bedroom with flowery wallpaper, a small window with rain outside and a bedside lamp"

# ---- cold open: England, 1962
N('C01', "England, November 1962. Seven-year-old Olivia has measles. Her father, the writer Roald Dahl, sits on her bed, teaching her to make little animals out of coloured pipe cleaners.",
  ch('c01a', C(.5, .5, 1.05), f"{ROOM62}: a small stickman girl in a pale nightdress, her round head covered in small red spots, sits up in bed under a quilt, holding a little pipe-cleaner animal in one hand; a tall stickman man in a 1960s cardigan sits apart on a chair beside the bed, holding a bundle of coloured pipe cleaners in one hand.", text=cap('England, 1962')),
  ob('c01b', "A close-up of a bedside table in a 1962 bedroom: a few little animals twisted from coloured pipe cleaners, a glass of water and a small lamp, rainy window behind.", text=cap('Pipe-cleaner animals')))
N('C02', "Then her fingers stop working. Within an hour she is unconscious. Within twelve hours, she is dead. The measles had reached her brain.",
  ch('c02a', W(), f"{ROOM62} at night, lamp light: the stickman girl lies still in bed with her eyes closed under the quilt, while the tall stickman man in a cardigan stands apart beside the bed, holding his head with both hands in shock.", text=cap('Measles encephalitis')))
N('C03', "For thousands of years, almost every child on Earth caught him. Most got better. Millions didn't.",
  ch('c03a', WL(), "A 1900s school classroom with wooden desks and a blackboard without writing: three stickman children in 1900s school clothes sit apart at their desks, all three with small red spots on their round heads, one coughing into his elbow, one resting her head on the desk.", text=cap('Almost every child')))
K('C04', "Everyone gets the measles. That's what they used to say. I loved that.",
  kg('c04a', C(.5, .45, 1.1), "Medium shot: the Red Jester leans against a child's wooden rocking horse in a dim Victorian nursery at night, grinning at the viewer and jingling the bells of his cap with one gloved hand, his other hand resting on the rocking horse's head."))
HOLD(4.6, kg('c05a', O(), "Title shot: the Red Jester stands on the left third of the frame on a dark empty theatre stage with a single spotlight, taking a deep bow with one gloved hand sweeping out, his other arm at his side, a wisp of pink mist around him; the right side of the frame is empty dark stage curtain.")
     | {'text': [label('MEASLES', 1300, 330, 140, style='title', pop=True, at=.15, len=4.2), label('THE RED JESTER', 1300, 470, 72, style='title', color=[230, 110, 110], at=.5, len=3.9)],
        'sfx': [{'kind': 'boom', 'at': .1, 'gain': .8}]})

# ---- who is he
N('L01', "So who is he? A virus. And the most contagious disease known to medicine. He floats in tiny droplets when you cough, sneeze or just breathe, and he can hang in the air of a room for up to two hours after you've left.",
  dg('d02a', "Four numbered steps in one row: (1) a simple stickman head coughing out a small cloud of tiny red dots, (2) the cloud of red dots hanging in an empty room, (3) a small clock face beside it, (4) a second stickman head walking into the cloud.", people=True, text=[cap('Two hours in the air')]),
  ch('c06a', W(), "A 1950s doctor's waiting room with wooden chairs and a coat stand: a stickman mother in a 1950s dress sits holding a coughing stickman toddler on her lap with both arms, while a faint pinkish haze hangs in the air of the room; a stickman man in a hat sits apart on another chair reading a newspaper without readable text.", text=cap('He lingers in the air')))
N('L02', "If you're not immune and you share a room with him, your chance of catching him is about nine in ten.",
  dg('d03a', "ONLY a single row of ten IDENTICAL plain stickman icons standing side by side across the page, no hats, no clothes, no numbers: just white round heads and black stick bodies; nine of them have small red spots on their heads, the last one is plain. Nothing else on the page.", people=True, text=[cap('9 in 10 catch it')]))
K('L03', "A cough, a sneeze, a breath. I'm not fussy. Nine out of ten, every time.",
  kg('c07a', C(.5, .45, 1.1), "The Red Jester stands in an empty 1950s doctor's waiting room, blowing a long wisp of pink mist across the room like blowing out birthday candles, one gloved hand on his hip, his other hand at his side."))

# ---- origin
N('L04', "Where did he come from? From cattle. His closest relative was rinderpest, a cattle plague. Scientists think the two split apart around two and a half thousand years ago.",
  dg('d04a', "A simple family tree: one trunk (1) splitting into two branches, one ending in a cow's head (2) and the other ending in a simple stickman head (3), with a small virus drawing at the fork.", people=True, text=[cap('Rinderpest and measles: brothers')]),
  ch('c08a', W(), "An ancient farm by a mud-brick city wall around 500 BC: a stickman herder in a simple tunic leads a cow by a rope held in one hand, while the cow coughs; a stickman woman in a long robe stands apart in a doorway holding a clay jar in both hands.", text=cap('About 2,500 years ago')))
N('L05', "And he needs big crowds. He burns through a village in weeks and then has no one left to infect. To keep going, he needs a city of at least a quarter of a million people, with new babies born all the time.",
  dg('d05a', "Two numbered panels in one row: (1) a tiny village of five huts with a small red flame burning out, (2) a big walled city full of houses with a steady small red flame in the middle.", text=[cap('He needs a big city')]),
  ch('c09a', C(.5, .5, 1.05), "A crowded ancient market street in a big city around 300 BC with stone columns and stalls: a stickman merchant in a tunic hands a bunch of grapes to a stickman woman in a long robe and headscarf, both standing apart, a small child in a tunic beside the woman.", text=cap('Cities made measles possible')))
N('L06', "Around the year nine hundred, the Persian doctor al-Razi became one of the first to describe him clearly, and to tell him apart from smallpox.",
  ch('c10a', W(), "A 900s Persian physician's study with arched windows, oil lamps, books and glass bottles: a stickman doctor in a long robe and a white turban sits at a low desk, writing in a large book with a reed pen held in one hand, his other hand on the page.", text=cap('Al-Razi, around 900')))
K('L07', "I started out on cows. Then I found something much better. Cities. Full of children.",
  kg('c11a', C(.5, .45, 1.1), "The Red Jester sits on a wooden fence in a meadow at dusk with a city skyline far behind him, patting a sleepy brown cow's head with one gloved hand and grinning at the viewer, his other hand resting on the fence."))

# ---- WHAT HE DOES TO YOU
N('S01', "So what does he do to you? About ten to fourteen days after you breathe him in: a high fever, a cough, a runny nose, and red, watery eyes.",
  dg('d06a', "A simple standing stickman outline with four numbered magnifier circles pointing to: (1) a thermometer at very high, (2) the mouth with a cough cloud, (3) the nose with a drip, (4) a red watery eye.", people=True, text=[label('What He Does to You', 960, 150, 72), cap('Fever, cough, red eyes')]),
  ch('c12a', C(.5, .5, 1.05), "A 1930s child's bedroom with the curtains drawn: a small stickman boy in striped pyjamas sits in bed with a hot water bottle, sneezing into a handkerchief held in one hand, while a stickman mother in a 1930s dress and cardigan stands apart beside the bed holding a thermometer in one hand.", text=cap('10 to 14 days later')))
N('S02', "Then tiny white spots appear inside the cheeks. And a few days later, the rash: red blotches that start on the face, then spread down the body.",
  dg('d07a', "Two numbered panels in one row: (1) a simple open mouth seen from the front with a few tiny white spots on the inside of the cheek, (2) a simple stickman body outline with red blotches on the face and arrows showing them spreading down over the chest, arms and legs.", people=True, text=[cap('White spots, then the rash')]),
  ch('c12b', W(), f"A 1930s child's bedroom in daylight: a small stickman girl in a long-sleeved white nightdress, her round white head covered in red blotches, sits up in bed looking glum, hugging a cloth doll with her two thin black stick arms, while a stickman doctor in a 1930s suit with a stethoscope stands apart, looking at her.", text=cap('The rash')))
N('S03', "Most children recover in a week or two. But he can also cause ear infections, blindness, and pneumonia, the most common cause of death. And in about one case in a thousand, he attacks the brain.",
  dg('d08a', "A simple stickman body outline front view with three numbered magnifier circles: (1) an ear with small pain lines, (2) a pair of lungs with dark patches, (3) a brain with a red glow.", people=True, text=[cap('Ears, eyes, lungs, brain')]),
  ch('c12c', C(.5, .5, 1.05), "A 1950s hospital children's ward with white iron cots: a small stickman boy with red spots lies in a cot under an oxygen tent of clear plastic, while a stickman nurse in a blue 1950s uniform and white cap stands apart, checking a clipboard held in one hand.", text=cap('Pneumonia')))
N('S04', "And there's something scientists only discovered recently. He wipes your immune memory. The protection you built against other germs can be partly erased, leaving you open to them again for years.",
  dg('d09a', "Two numbered panels in one row: (1) a simple shield covered in many small coloured badges, (2) the same shield with most of the badges gone and a red jester's cap drawn small beside it.", text=[cap('Immune amnesia')]))
K('S05', "Fever, spots, a little cough. And when I leave, I take your memories with me. Your immune memories, that is.",
  kg('c13a', C(.5, .45, 1.1), "The Red Jester tiptoes away from a sleeping child's bed in a dark Victorian nursery, carrying a small cloth sack over his shoulder with one gloved hand and holding a finger to his grinning lips with the other hand."))

# ---- the Americas, Hawaii
N('L08', "When Europeans crossed the Atlantic, he came with them, together with smallpox. People in the Americas had never met either of them. In Mexico, in fifteen thirty-one, so many died of measles that it was remembered as the small leprosy.",
  ch('c14a', WL(), "A 1531 village in central Mexico with adobe houses and maize fields: a stickman woman in a white cotton huipil dress kneels beside a sleeping mat on which a small stickman child with red spots lies under a woven blanket, the woman holding a clay cup in one hand.", text=cap('Mexico, 1531')),
  dg('d10a', "A simple map of the Atlantic Ocean with Europe on the right and the Americas on the left, one sailing ship icon crossing from right to left, with a small red-spotted circle and a small brown-spotted circle beside the ship.", text=[cap('Measles and smallpox crossed together')]))
N('L09', "In eighteen twenty-four, the young king of Hawaii, Kamehameha the Second, sailed to London with his queen, Kamāmalu. They hoped to meet King George. Instead, they caught measles. Both died in London.",
  ch('c15a', W(), "A grand 1824 London hotel room with tall windows, heavy curtains and a fireplace: a stickman man in a dark 1820s tailcoat lies in a large four-poster bed with red spots on his round head, while a stickman woman in a long 1820s dress sits apart in an armchair beside the bed, also with small red spots, holding a handkerchief in one hand.", text=cap('London, 1824')))
K('L10', "A king and a queen. Royalty. I do have excellent taste.",
  kg('c16a', C(.5, .45, 1.1), "The Red Jester stands in an empty grand 1824 London hall with tall windows, wearing a small toy paper crown on top of his jester's cap, adjusting it with one gloved hand and smirking at the viewer, his other hand on his hip."))

# ---- Faroe Islands: Panum
N('L11', "In eighteen forty-six, measles reached the Faroe Islands, in the North Atlantic, for the first time in sixty-five years. Of about eight thousand people, more than six thousand caught it.",
  ch('c17a', W(), "A green, windswept 1846 Faroe Islands village of small houses with grass roofs by a grey fjord: a stickman fisherman in a thick wool sweater and cap stands apart outside his house, coughing into his elbow, holding a fishing net in his other hand.", text=cap('Faroe Islands, 1846')))
N('L12', "Denmark sent a young doctor, Peter Panum. He travelled from village to village and tracked every case. He worked out that measles appears about two weeks after exposure. And he noticed something remarkable: the old people who'd had measles back in seventeen eighty-one didn't catch it again.",
  ch('c17b', C(.5, .5, 1.05), "Inside a small dim 1846 Faroese cottage with a peat fire: a young stickman doctor in a dark 1840s coat sits at a wooden table, writing in an open notebook with ONE pencil held in his right hand, his left mitten hand resting flat on the page holding nothing, while an old stickman man in a wool sweater sits apart by the fire, smiling and healthy, without spots.", text=cap('Peter Panum')),
  dg('d11a', "A simple timeline with two numbered points: (1) a small sick stickman with red spots at the left end, (2) the same stickman, now old with a walking stick and no spots, at the right end, a long arrow between them and a green tick above him.", people=True, text=[cap('Immune for life')]))
K('L13', "Sixty-five years I was away. They remembered me. That's the one thing I can't stand.",
  kg('c18a', C(.5, .45, 1.1), "The Red Jester stands on a windswept green Faroese hillside above a fjord, his cap bells blowing in the wind, glaring annoyed at the viewer with his gloved arms crossed."))

# ---- Fiji
N('L14', "Then Fiji, eighteen seventy-five. The Fijian king Cakobau returned from Sydney on a British warship. On board, his son had measles. Crowds came to welcome them home. Within months, tens of thousands of Fijians were dead, perhaps a quarter of the population.",
  ch('c19a', WL(), "An 1875 tropical harbour in Fiji with palm trees and thatched houses, a large dark British steam warship anchored offshore: in the foreground on the beach two stickman Fijian men in wrapped sulu cloths stand apart, waving at the ship with raised hands.", text=cap('Fiji, 1875')),
  ch('c19b', C(.5, .5, 1.05), "Inside a dim 1875 Fijian thatched house with woven mats: a stickman woman in a wrapped sulu cloth kneels beside a sick stickman man who lies on his back on a mat under a patterned cloth, his round head covered in red spots resting on a woven pillow, his two thin stick arms on top of the cloth; the woman holds a coconut-shell cup near his face with one hand, her other hand on her knee.", text=cap('Perhaps a quarter died')))

# ---- the vaccine
N('L15', "For most of history, measles was just a part of childhood. In the United States alone, before the vaccine, three to four million people caught it every year, and four to five hundred died.",
  ch('c20a', W(), "A 1950s American suburban street in summer with white picket fences: two stickman children with red spots on their round heads look sadly out of a front window, while a third stickman child on a bicycle rides past on the pavement, waving with one hand.", text=cap('3 to 4 million cases a year')))
N('L16', "In nineteen fifty-four, in Boston, the scientists John Enders and Thomas Peebles took a sample from a sick thirteen-year-old boy, David Edmonston, and managed to grow the virus in the lab.",
  ch('c21a', C(.5, .5, 1.05), "A 1954 Boston laboratory with glass cabinets and test-tube racks: a stickman scientist in a white coat and small round glasses (eyes inside the lenses) holds a glass flask up to the window light with one hand, while a second stickman scientist in a white coat stands apart at a microscope with both hands on the focus knob.", text=cap('Boston, 1954')),
  ch('c21b', W(), "A 1954 school sick room: a stickman boy of thirteen with red spots on his round head sits on a cot in a sweater, holding a cotton swab stick in one hand, while a stickman doctor in a white coat stands apart holding a small glass tube in one hand.", text=cap('David Edmonston, 13')))
N('L17', "His virus, weakened step by step, became the first measles vaccine in nineteen sixty-three. A better one by Maurice Hilleman followed. Then, the combined MMR shot. Cases collapsed.",
  dg('d12a', "ONLY one simple line chart filling the whole page: a jagged line of high yearly peaks on the left, then a small syringe icon on the line, after which the line drops almost to nothing. No numbers.", text=[cap('1963: the vaccine')]),
  ch('c22a', C(.5, .5, 1.05), "A 1960s doctor's office with a poster-free wall and a wooden desk: a stickman doctor in a white coat gives an injection with one hand into the upper arm of a small stickman girl in a 1960s dress sitting on the examination table, who looks away bravely; her mother in a 1960s coat stands apart, holding the girl's hand.", text=cap('Maurice Hilleman, MMR')))
N('L18', "Twenty-four years after Olivia died, Roald Dahl wrote an open letter begging parents to vaccinate their children. He had already dedicated one of his most famous books, The BFG, to her.",
  ch('c23a', W(), "A cosy 1986 writing hut with an old armchair, a writing board on its arms and a lamp: an older stickman man in a cardigan sits in the armchair, writing a letter with a pencil held in one hand, his other hand holding the page, a small framed photograph of a girl on the shelf behind him.", text=cap('Roald Dahl, 1986')))
K('L19', "Two little shots. That's all it takes to shut me out. It's humiliating.",
  kg('c24a', C(.5, .45, 1.1), "The Red Jester sits slumped on an empty wooden school bench in a sunny 1960s school corridor, holding a tiny syringe at arm's length between two gloved fingertips with disgust, his other hand on his knee."))

# ---- WHAT HE LEAVES BEHIND
N('A01', "For survivors, he leaves lifelong immunity to measles, but a weakened defence against other germs for years. And very rarely, seven to ten years later, a deadly brain disease called SSPE.",
  dg('d13a', "Three numbered panels in one row: (1) a simple shield with a green tick, (2) a cracked shield, (3) a calendar with a small brain drawing and a question mark.", text=[label('What He Leaves Behind', 960, 150, 72), cap('Immunity, and a hidden cost')]))
N('A02', "For the world, he left the idea of herd immunity. If about ninety-five in a hundred people are immune, he can't find enough victims, and even those who can't be vaccinated, like tiny babies, are protected.",
  dg('d14a', "A simple crowd diagram on aged paper: many small blue stickman icons standing in a grid, one small red-spotted stickman at the edge, and one tiny baby icon in the middle protected by the blue ones, with small blocked arrows from the red one.", people=True, text=[cap('Herd immunity: 95 in 100')]),
  ch('c25a', W(), "A sunny modern playground: three stickman children in bright T-shirts play apart on a slide and swings, while a stickman mother in jeans stands apart holding a baby in a sling with both arms.", modern=True, text=cap('Protecting the ones who can\'t be vaccinated')))
K('A03', "Ninety-five in a hundred. Leave me one gap, just one, and I'll find it.",
  kg('c26a', C(.5, .45, 1.1), "The Red Jester peeks through a small gap in a tall wooden fence around a sunny playground, one bright eye pressed to the gap, grinning, both gloved hands holding the fence boards on either side of the gap."))

# ---- today
N('T01', "In two thousand, the United States declared measles eliminated. But two years earlier, in nineteen ninety-eight, a fraudulent study had claimed the MMR vaccine was linked to autism. It was retracted, and its author lost his licence, but the fear spread. Vaccination rates fell. And he came back.",
  ch('c27a', C(.5, .5, 1.05), "A modern living room in the evening: a worried stickman father in a hoodie sits on a sofa scrolling on a smartphone held in one hand, the screen glowing with no readable text, while a small stickman child plays with toy blocks on the rug apart from him.", modern=True, text=cap('A fraudulent study, 1998')))
N('T02', "Today, measles still infects millions every year. In twenty twenty-four, around ninety-five thousand people died, most of them children under five. And since the year two thousand, the vaccine has saved almost sixty million lives.",
  dg('d15a', "ONLY a simple world map filling the whole page with many small red dots scattered across Africa, Asia, Europe and the Americas. Nothing else.", text=[cap('About 95,000 deaths in 2024')]),
  ch('c28a', W(), "A modern clinic in a sunny town: a stickman nurse in a blue medical tunic gives an injection with one hand into the upper arm of a small stickman child in a T-shirt sitting on his mother's lap; the mother in a bright headscarf holds the child with both arms.", modern=True, text=cap('Nearly 60 million lives saved')))
K('T03', "Every time you forget me, I come back. And you always forget.",
  kg('c29a', C(.5, .45, 1.1), "The Red Jester sits on a modern playground swing at dusk, swinging gently, holding the chain with one gloved hand and waving slowly at the viewer with the other hand, grinning."))

# ---- ending
N('L20', "For thousands of years, he was a part of growing up, a disease almost every child caught and too many never survived. He was beaten by a doctor on a windswept island, a sick boy in Boston, and two small shots. But every time we forget him, he comes back.",
  sh('c01a', C(.5, .5, 1.05)), sh('c17b', C(.5, .5, 1.05)), sh('c21b', W()), sh('c22a', C(.5, .5, 1.05)),
  kg('c30a', C(.5, .45, 1.1), "The Red Jester walks away down a misty cobbled street at dusk, seen from behind in profile, his cap bells swinging, his gloved hands clasped behind his back, a faint wisp of pink mist trailing behind him."))
N('L21', "Next time: the strangling angel of children. He was stopped in Alaska by a team of sled dogs racing through a blizzard.",
  ch('c31a', C(.5, .5, 1.04), "A dark snowy Alaskan landscape in 1925 at night during a blizzard, ominous: on the left third of the frame a single stickman musher in a thick fur parka stands behind a dog sled pulled by a team of huskies, holding the sled handle with both hands; the right side of the frame is dark empty swirling snow."))
HOLD(5.0, sh('c31a', O(), text=[label('NEXT TIME', 1380, 360, 110, style='title', pop=True, at=.2, len=4.6), label('SUBSCRIBE', 1380, 500, 64, at=.8, len=4.0)]))

# ---- extra cut-ins
EXTRA = {
  'C03': [(None, ch('c03b', C(.5, .5, 1.05), "A dim Victorian nursery with two small iron beds: two small stickman children in nightshirts lie apart in the beds, both with red spots on their round heads, while a stickman mother in a long Victorian dress and apron sits on a chair between them, holding a cup in one hand.", text=cap('A part of childhood')))],
  'L02': [(None, ch('c06c', W(), "A 1900s school classroom with wooden desks: one small stickman boy with a few red spots on his round head coughs into his elbow, while two other stickman children sit apart at their desks, turning to look at him.", text=cap('One cough is enough')))],
  'L06': [(None, ob('c10b', "An old open hand-written Arabic-style medical book on a wooden desk lit by an oil lamp, its pages covered in decorative patterns and small drawings of spotted skin, with no readable writing; a reed pen and an ink pot beside it.", text=cap('Measles and smallpox are different')))],
  'L08': [(None, ch('c14b', W(), "A 1500s Caribbean beach with a large 1500s sailing ship with plain undecorated cream sails anchored offshore, no crosses or emblems on the sails, no flags: two stickman Spanish sailors in loose shirts, breeches and caps pull a rowing boat up the sand with both hands, palm trees behind them.", text=cap('They came by ship')))],
  'L11': [(None, ob('c17c', "A grey windswept fjord in the Faroe Islands in 1846 with steep green cliffs, a few small wooden fishing boats pulled up on the shore and grass-roofed houses.", text=cap('Remote islands in the North Atlantic')))],
  'L15': [(None, ch('c20b', C(.5, .5, 1.05), "A 1950s living room with a television set and a sofa: a small stickman girl with red spots on her round head lies on the sofa under a blanket, while a stickman mother in a 1950s dress sits apart in an armchair, reading the thermometer held up in one hand.", text=cap('Every family knew it')))],
  'L16': [(None, ob('c21c', "A 1950s laboratory bench: a glass flask of pink cell-culture liquid, a rack of test tubes and a brass microscope under a desk lamp.", text=cap('Growing the virus')))],
  'L17': [(None, ch('c22b', W(), "A 1960s school gym: a short queue of three stickman children in 1960s school clothes stand apart in a line, waiting, while a stickman nurse in a white uniform and cap sits at a small table with a box of syringes, holding one up in one hand.", text=cap('Queueing for the shot')))],
  'T02': [(None, ch('c28b', W(), "A dusty modern rural road with green hills: a stickman health worker in a blue vest rides a small motorbike with both hands on the handlebars, a blue cool box strapped on the back seat.", modern=True, text=cap('Vaccines on the move')))],
  'S02': [(None, ob('c12e', "A close-up of a 1930s bedside table: an old glass thermometer, a glass of water, a spoon and a small medicine bottle without a label, soft lamp light.", text=cap('Days of fever')))],
  'L01': [(None, ob('c06b', "An extreme close-up of a beam of window light in an empty room, with tiny glittering droplets hanging in the air like dust, soft warm light.", text=cap('Tiny droplets')))],
  'L05': [(None, ch('c09b', W(), "A tiny remote village of a few round thatched huts on a hillside: one stickman villager in a simple tunic stands apart outside his hut, looking at an empty path.", text=cap('A village runs out of victims')))],
  'S03': [(None, ch('c12d', W(), "A dim 1900s sickroom: a small stickman child with red spots on his round head sits in bed with a bandage wrapped around one ear, while a stickman grandmother in a shawl sits apart, knitting with two needles held in both hands.", text=cap('Ear infections')))],
  'L09': [(None, ob('c15b', "An 1824 sailing ship with plain cream sails and no flags or pennants anywhere, on a grey sea approaching the white cliffs of England under a cloudy sky.", text=cap('A long voyage to London')))],
  'L14': [(None, ob('c19c', "An empty 1875 Fijian village at dusk: thatched houses with closed doors, a canoe pulled up on the sand, palm trees and a quiet lagoon.", text=cap('Villages fell silent')))],
  'T01': [(None, ch('c27b', W(), "A modern school entrance: a stickman school nurse in a cardigan pins a plain paper notice without readable writing to a noticeboard with one hand, while a stickman parent in a coat stands apart reading it, holding a child's hand.", modern=True, text=cap('Outbreaks return')))],
}
for _i, _r, _t, _sh in B:
    for _pos, _s in EXTRA.get(_i, []):
        if _pos is None: _sh.append(_s)
        else: _sh.insert(_pos, _s)

def lines():
    for i, r, t, _ in B:
        if i: print(f"{i}|{r}|{t}")

def frames():
    seen, out = set(), []
    for _, _, _, shots in B:
        for s in shots:
            if 'prompt' in s and s['img'] not in seen:
                seen.add(s['img'])
                out.append({'img': s['img'], 'prompt': s['prompt'], 'refs': [K_SHEET] if 'K' in s['refs'] else []})
    json.dump(out, open(os.path.join(ROOT, 'tools/plague/ep13_frames_todo.json'), 'w'), indent=1); print(len(out), 'frames')

def beats():
    out = {'base': 'assets/plague/ep13/frames', 'keep_zoom': [], 'static': True, 'fade_in': .8, 'start': 0.0, 'lead': .35, 'gap': .35, 'max_shot': 2.6,
           'sfx_global': [{'kind': 'drone', 't': 0.0, 'args': {'d': 'ALL'}, 'gain': .9}, {'kind': 'wind', 't': 0.0, 'args': {'d': 'ALL'}, 'gain': .12}], 'beats': []}
    M = 'assets/plague/music/'
    out['music'] = [{'file': M + f, 't0': float(a0), 't1': a1, 'gain': 1.0, 'fade_in': 2.0 if a0 == 0 else 4.0, 'fade_out': 5.0 if a1 == 'ALL' else 4.0}
                    for a0, a1, f in MUSIC]
    for i, r, t, shots in B:
        sl = []
        for s in shots:
            d = {'img': s['img'], 'from': s['cam'][0], 'to': s['cam'][1], 'w': s['w']}
            if 'text' in s: d['text'] = s['text']
            if 'sfx' in s: d['sfx'] = s['sfx']
            sl.append(d)
        if i: out['beats'].append({'vo': f'assets/plague/ep13/vo_fast/{i}.wav', **({'gain': 1.05} if r == 'MEASLES' else {}), 'shots': sl})
        else: out['beats'].append({'hold': t, 'shots': sl})
    json.dump(out, open(os.path.join(ROOT, 'tools/plague/ep13_beats.json'), 'w'), indent=1); print(len(out['beats']), 'beats')

# Set after the voice-over exists, from the real chapter boundaries.
MUSIC = [(0, 141, 'plague_a.mp3'), (137, 220, 'plague_b.mp3'), (216, 271, 'cholera_a.mp3'), (267, 'ALL', 'cholera_b.mp3')]   # open..symptoms | Americas..Fiji | vaccine+Dahl | aftermath..end

{'lines': lines, 'frames': frames, 'beats': beats}[sys.argv[1]]()
