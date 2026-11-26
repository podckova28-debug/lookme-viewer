"""The Entire History of SMALLPOX - food-and-drinks (gin/ketchup) format for the diseases channel.
One line = one VO clip = one new frame (2-4 s). Roles: N narrator (George), S Smallpox (aristocrat villain, role_smallpox_daniel_low).
Running gag: tavern chalkboard SMALLPOX vs HUMANS (b0 spoiler -> b1 -> b2 -> final). Callbacks: beauty patches, the cow.
Frame = (prompt, note). note = short handwritten text baked into the picture with an arrow; '' = none.
python3 plan.py -> lines.txt (for voices/) + frames.json (prompts)
"""
import json, os
STYLE = ("White background; detailed ink-line illustration, fine cross-hatching, soft muted watercolour, dusty rose, pewter grey and old-gold accents, "
         "playful humorous cartoon tone; large close-up composition: the subject is big and fills most of the frame, rich fine detail and expressive faces; "
         "cut out on white with a little white space around it. Every person has exactly one head, two arms, two hands with five fingers, two legs. ")
def YOU(hat): return ("one simple hand-drawn stick figure: thin black ink line body, arms and legs, a round white head with dot eyes and an expressive mouth, "
                      f"simple outlined hands, exactly two arms and two legs, wearing {hat}, ")
TRI = 'a small black tricorn hat'
SP = ("Smallpox as a villain: a smug 18th-century aristocrat with a tall curly powdered wig, a pale face covered in small red pockmarks and two black beauty patches, "
      "a lace jabot, a dark plum velvet frock coat with gold embroidery, two pocket watches on chains, ")
BOARD = ("an old dark green wooden tavern chalkboard on a wooden easel, written on it in white chalk two columns headed 'SMALLPOX' and 'HUMANS', a chalk line under the headings; "
         "objects only, no people, no hands; ")
NOTE = " Handwritten black ink note on the white space: '{}' with a thin hand-drawn arrow pointing at it. No other text."
NOTEXT = " No text anywhere."

L = [
 # ---- p0 cold open ----
 ('a01','N',"It's seventeen fifty, London, and you wake up with a fever.", YOU(TRI)+"sitting up in a small wooden bed under a patched blanket, sweating, a thermometer-like wavy heat line above his head, a candle on a stool", ''),
 ('a02','N',"Your back hurts like someone kicked it.", YOU(TRI)+"standing bent over, both hands pressed to his lower back, a big cartoon boot print on his back", 'ow'),
 ('a03','N',"Three days later, the spots come.", YOU(TRI)+"looking into a small hand mirror with horror, his round white head covered in small red spots", 'day 3'),
 ('a04','N',"Everyone in the street knows exactly what this is.", "a narrow 18th-century London street of crooked brick houses, neighbours leaning out of every window pointing down, shocked faces", ''),
 ('a05','S',"Good morning.", SP+"standing in the doorway of a poor bedroom, bowing politely with one hand on his chest and smirking at the viewer", 'Smallpox (yes, the disease)'),
 ('a06','N',"Smallpox. In the twentieth century alone, it killed about three hundred million people.", "a huge heap of tiny identical simple black ink stick figures piled up like a mountain, seen from a distance", '300,000,000'),
 ('a07','N',"More than all the wars of that century put together.", "an old brass balance scale: on the left pan a pile of small old helmets, rifles and cannonballs, on the right pan one single small red smallpox pustule-shaped bead, and the right pan is much heavier and lower", ''),
 ('a08','N',"And yet, it's the only human disease we've ever wiped off the planet.", "a hand-drawn globe of the Earth with a big old-fashioned rubber eraser rubbing out a small red spotted blob on it, crumbs of eraser around", ''),
 ('a09','N',"Here's the score so far.", BOARD+"under SMALLPOX a huge number of chalk tally marks filling the column, under HUMANS nothing", ''),
 ('a10','N',"So how did we beat it? With a cow. Eventually.", "a friendly brown and white dairy cow standing proudly like a hero, chest out, a small red superhero cape tied around its neck", 'our hero'),

 # ---- p1 what it does ----
 ('b01','N',"First, what it is.", "an old brass microscope on a wooden desk with a glass slide under it", ''),
 ('b02','N',"Smallpox is a virus, a tiny brick-shaped box packed with instructions.", "a large magnified circle like a microscope view: one oval brick-shaped virus particle with a bumpy wavy outer coat, drawn like a little lumpy parcel, a coiled thread of DNA visible inside", 'variola'),
 ('b03','N',"Someone sick coughs near you, and you breathe it in.", YOU(TRI)+"standing next to another coughing stick figure in a tricorn hat, a small cloud of tiny dots drifting from the cougher's mouth into his nose", ''),
 ('b04','N',"For about twelve days, nothing happens. You feel fine.", YOU(TRI)+"whistling happily, walking with a small basket of bread, small calendar pages flying around him", 'days 1-12'),
 ('b05','N',"Meanwhile the virus is quietly copying itself in your blood.", "a cut-away view of a red blood vessel tube, many small brick-shaped virus particles multiplying inside it like a crowd, some copying themselves", ''),
 ('b06','N',"Then the fever hits, and the virus settles into your skin.", "a large magnified cross-section of human skin layers, pink and cream, small brick-shaped virus particles moving up into the top layer", 'your skin'),
 ('b07','N',"The spots turn into hard bumps, like dried peas under the skin.", "a close-up of a hand-drawn forearm skin with round raised firm cream-coloured bumps, next to a small pile of dried green peas for comparison", 'like peas'),
 ('b08','N',"They fill with pus, mostly on your face, hands and feet.", "a simple outline figure of a person seen from the front, many small red dots densely on the face, hands and feet, fewer on the chest and belly", 'face, hands, feet'),
 ('b09','N',"About three in ten people die.", "three simple ink stick figures in tricorn hats standing in a row with seven more, ten in total, three of them faded and grey, seven black", '3 in 10'),
 ('b10','N',"The rest live, but the bumps leave deep scars for life. Some go blind.", "a close-up of a cheerful 18th-century man's face, alive and smiling, his cheeks covered in small round pitted scars, one eye clouded white", 'survived'),
 ('b11','S',"I always leave a little souvenir.", SP+"holding up one small framed oval portrait of a scarred face like a gift, smiling proudly", ''),

 # ---- p2 ancient world ----
 ('c01','N',"Smallpox is old. Very old.", "a crumbling ancient stone sundial half buried in sand", ''),
 ('c02','N',"This is Pharaoh Ramses the Fifth. He died more than three thousand years ago.", "an ancient Egyptian royal mummy lying in an open painted wooden coffin, wrapped in linen, only the dark leathery face visible", 'Ramses V'),
 ('c03','N',"His mummy's face is covered in small bumps that look a lot like smallpox.", "a close-up of an ancient Egyptian mummy's dark leathery face with many small raised round bumps on the cheeks, a magnifying glass held over it by a hand in a white glove", 'hmm'),
 ('c04','S',"Lovely man. Terrible skin.", SP+"standing beside an ancient Egyptian sarcophagus, leaning one elbow on it casually, winking", ''),
 ('c05','N',"It travelled the way everything travelled: with traders and armies.", "an ancient caravan of camels loaded with bundles walking left to right, Roman-style soldiers marching behind them, small red dots floating in the dust around them", ''),
 ('c06','N',"Every new city was a new buffet.", SP+"sitting at a long banquet table set with a big platter on which tiny model cities are served like cakes, a napkin tucked into his jabot, knife and fork in hand", ''),
 ('c07','N',"And by the fifteen hundreds, it was everywhere in Europe, Asia and Africa. Except one place.", "an old hand-drawn world map in sepia, Europe, Asia and Africa covered in many small red dots, the Americas completely clean with no dots", ''),

 # ---- p3 Americas ----
 ('d01','N',"Fifteen twenty. A Spanish ship lands in Mexico.", "a 16th-century Spanish galleon with patched sails anchored off a tropical shore with palm trees", ''),
 ('d02','N',"On board is one man with smallpox.", "a single sick 16th-century Spanish sailor in a striped shirt sitting on a barrel, his face covered in red spots, looking miserable", 'one man'),
 ('d03','N',"The people of the Americas had never met this virus. Their bodies had no defence at all.", "a magnified circle of blood with a few round white immune cells sitting on deckchairs, relaxed, completely unaware, while brick-shaped viruses sneak in", 'never met it'),
 ('d04','N',"In the Aztec capital, Tenochtitlan, it spread through the whole city.", "a grand Aztec city of Tenochtitlan with temple pyramids on a lake and causeways, seen from a hill, a pale grey haze settling over it", ''),
 ('d05','N',"It killed the emperor himself, Cuitlahuac.", "an Aztec emperor's feathered headdress and a jade necklace lying alone on an empty stone throne", ''),
 ('d06','N',"Across the Americas, millions died, sometimes before a single Spanish soldier even arrived.", "an old map of the Americas with a red stain spreading inland from the coast far ahead of a tiny drawing of a few Spanish soldiers on the beach", 'ahead of the army'),
 ('d07','N',"Historians still argue about the numbers. But they don't argue about this: smallpox did more damage than any sword.", "an old steel Spanish sword lying on the ground next to a much larger shadow shaped like a pockmarked hand", ''),
 ('d08','N',"Scoreboard.", BOARD+"under SMALLPOX the column is completely full of tally marks and they continue onto the wooden frame, under HUMANS nothing", ''),

 # ---- p4 Europe 18th century ----
 ('e01','N',"Back in Europe, the seventeen hundreds were smallpox's golden age.", SP+"lounging on a gilded rococo armchair with his feet on a footstool, holding a small glass of wine, very pleased with himself", 'golden age'),
 ('e02','N',"It killed about four hundred thousand Europeans a year.", "a long queue of tiny ink stick figures in tricorn hats and bonnets stretching across the frame and into the distance", '400,000 a year'),
 ('e03','N',"And it did not care who you were.", "a velvet cushion with a golden royal crown and a plain wooden peasant's bowl side by side, both with a few small red spots on them", ''),
 ('e04','N',"It killed a queen of England, a young emperor of Russia, and a king of France.", "three ornate empty royal thrones side by side, each with a crown resting on its seat", 'Mary II, Peter II, Louis XV'),
 ('e05','S',"I collect crowns.", SP+"standing in front of a glass cabinet displaying several royal crowns on little stands like trophies, polishing one with a cloth", ''),
 ('e06','N',"Survivors had faces full of scars. So fashion stepped in.", "a fine 18th-century lady in a big powdered wig and silk gown looking sadly at her pockmarked cheek in a hand mirror", ''),
 ('e07','N',"Little black patches of silk, glued onto the face. Stars, moons, hearts.", "an open small round silver patch box full of tiny black silk beauty patches shaped like stars, crescent moons and hearts, a small brush beside it", 'beauty patches'),
 ('e08','N',"One patch to hide a scar. Five patches to hide the rest.", "the same 18th-century lady in a big powdered wig smiling proudly at her hand mirror, her face dotted with many little black patches shaped like stars, moons and hearts", 'nailed it'),
 ('e09','N',"Very fashionable. Not very effective.", "a close-up of a lady's cheek: one black heart-shaped beauty patch next to several uncovered pockmark scars around it", ''),

 # ---- p5 variolation ----
 ('f01','N',"But people had noticed one thing.", "a single small brass oil lamp glowing, a thin idea-like spark above the flame", ''),
 ('f02','N',"If you survived smallpox once, you never got it again.", YOU(TRI)+"with a few pale scars on his round head, standing calmly with arms crossed while a cloud of red dots bounces off him", 'immune'),
 ('f03','N',"So in China, doctors ground up dried smallpox scabs and blew the powder up your nose.", "an 18th-century Chinese doctor in a long robe and small cap holding a thin silver tube to the nose of a nervous young boy, a small dish of grey powder on the table", ''),
 ('f04','N',"In India and Africa, they scratched a little pus from a mild case into the skin.", "a close-up of a hand holding a small thin blade over another person's forearm with a tiny scratch, a small dish next to them, calm careful faces", ''),
 ('f05','N',"You got a small case on purpose, so you'd never get the big one.", "a simple cartoon comparison: on the left a tiny red dot labelled with a small smiley face, on the right a huge spiky red monster blob with a big cross through it", 'small > big'),
 ('f06','N',"It was called variolation. And it worked, mostly.", "a single small glass vial with a cork, holding a little grey powder, standing on a wooden table", 'variolation'),
 ('f07','N',"Seventeen seventeen. Lady Mary Wortley Montagu, wife of the British ambassador in Constantinople, sees it done.", "an elegant 18th-century English lady in a travelling dress and Ottoman-style turban, her face lightly pockmarked, watching an old Turkish woman with a small needle and a nutshell of matter", 'Lady Mary'),
 ('f08','N',"She'd had smallpox herself. It killed her brother and took her eyelashes.", "the same elegant lady in an Ottoman-style turban looking into a small mirror at her eyes, which have no eyelashes, a small sad smile", ''),
 ('f09','N',"So she had her own son done.", "the same elegant lady holding the hand of a small boy in a little 18th-century coat while an old Turkish woman scratches his arm gently with a needle; the boy is brave", ''),
 ('f10','N',"Back in London, doctors were not impressed.", "three grumpy 18th-century physicians in huge white wigs and black coats with folded arms, frowning", 'hmph'),
 ('f11','N',"So in seventeen twenty one, they tested it on six prisoners, who were promised freedom if they lived.", "six 18th-century prisoners in rough shirts standing in a row in a stone cell, each holding out one arm, one doctor in a wig holding a small lancet", 'Newgate, 1721'),
 ('f12','N',"All six lived. All six walked free.", "six happy 18th-century men in rough shirts walking out of an open prison gate into the sunlight, one throwing his hat in the air", 'free'),
 ('f13','N',"That same year, Boston tried it too. The preacher Cotton Mather had learned it from an enslaved African man named Onesimus.", "an 18th-century African man in a simple linen shirt and waistcoat explaining calmly, pointing to a small scar on his own forearm, while a Puritan preacher in a black coat and white bands listens, surprised", 'Onesimus'),
 ('f14','N',"The catch: you could still die from it, about one or two in a hundred. And you were contagious.", "a small brass balance scale, one pan with two tiny black beads and the other with a hundred tiny white beads", '1-2 in 100'),
 ('f15','S',"Still. Not bad. I'm rather proud of you.", SP+"slowly clapping his hands in a theatre box, smirking", ''),

 # ---- p6 Jenner ----
 ('g01','N',"Now, the cow.", "the same friendly brown and white dairy cow with a small red superhero cape, standing in a green meadow", 'remember me?'),
 ('g02','N',"In the English countryside, there was an old rumour about milkmaids.", "a sunny English country farm with a thatched cottage, a wooden fence and a milk churn", ''),
 ('g03','N',"They caught cowpox from the cows, a mild disease with a few blisters on the hands.", "a cheerful 18th-century English milkmaid in a white bonnet and apron sitting on a stool milking a brown and white cow, two or three small blisters on her hand", 'cowpox'),
 ('g04','N',"And then, somehow, they never caught smallpox.", "the same cheerful milkmaid in a white bonnet smiling at the viewer, her face perfectly smooth and clear with no spots", 'no smallpox. ever.'),
 ('g05','N',"Seventeen ninety six. A country doctor called Edward Jenner decides to test the rumour.", "an 18th-century English country doctor with grey hair, a dark blue coat and a white cravat, rubbing his chin thoughtfully in his study", 'Edward Jenner'),
 ('g06','N',"A milkmaid, Sarah Nelmes, has cowpox, which she caught from a cow named Blossom.", "a young milkmaid in a bonnet showing her hand with a blister, standing next to a brown and white cow with a little bell", 'Blossom'),
 ('g07','N',"Jenner takes a little fluid from her blister and scratches it into the arm of an eight year old boy, James Phipps.", "the same doctor in a dark blue coat gently scratching the arm of a brave little boy in a shirt and waistcoat with a small lancet, a milkmaid watching", 'James, age 8'),
 ('g08','N',"James gets a mild cowpox. Then Jenner does something nobody would allow today.", "the little boy sitting on a chair with a small bandage on his arm, looking a bit bored", ''),
 ('g09','N',"He scratches real smallpox into the boy's arm.", "the same doctor holding a small glass vial marked with a tiny red skull, looking nervous, sweat drop on his forehead", 'yikes'),
 ('g10','N',"And nothing happens.", "the little boy in a waistcoat standing completely healthy and smiling, holding a toy wooden sword, no spots at all", 'nothing'),
 ('g11','S',"I beg your pardon?", SP+"staggering back in shock with his mouth open, his powdered wig slipping sideways, one hand on his chest", ''),
 ('g12','N',"Jenner called it vaccination, from vacca, the Latin word for cow.", "the cow in the little red cape standing proudly on a small wooden podium with a gold medal ribbon around its neck", 'vacca = cow'),
 ('g13','N',"Some people were terrified it would turn them into cows.", "a funny satirical 18th-century cartoon of three people in a doctor's room with small cow heads and horns sprouting from their arms and cheeks, looking alarmed", 'moo?'),
 ('g14','N',"It did not.", "a smiling 18th-century man in a coat showing his perfectly normal arm with one small round vaccination scar", ''),
 ('g15','N',"Scoreboard.", BOARD+"under SMALLPOX a full column of tally marks, under HUMANS one single fresh chalk tally mark", ''),

 # ---- p7 eradication ----
 ('h01','N',"But a vaccine only works if it reaches people.", "a small glass vaccine vial on a wooden table, and behind it a huge distant mountain range and a desert, very far away", ''),
 ('h02','N',"By the nineteen fifties, rich countries were free of smallpox. Much of the world was not.", "a hand-drawn world map with Europe and North America clean, while large parts of Africa, South Asia and South America still covered in red dots", ''),
 ('h03','N',"So in nineteen sixty seven, the World Health Organization tried something no one had ever done.", "a large meeting table seen from above with many papers, a world map spread on it and many hands pointing at it", ''),
 ('h04','N',"Wipe out a disease. Everywhere.", "a hand-drawn globe of the Earth with a big old-fashioned rubber eraser rubbing out a red spotted blob on it", ''),
 ('h05','N',"Their secret weapon was a needle with two prongs. Cheap, simple, and it needed far less vaccine.", "a close-up of a small steel bifurcated needle with a forked two-pronged tip, a tiny drop held between the prongs", 'two prongs'),
 ('h06','N',"And instead of vaccinating everyone, they hunted.", "a vaccinator in a simple 1970s shirt and cap walking along a dusty village road with a bag and a notebook, determined", ''),
 ('h07','N',"Find one case, then vaccinate everyone around it, in a ring.", "a simple cartoon map of a village seen from above, one house in the middle marked red, a circle of houses around it each marked with a green tick", 'ring'),
 ('h08','N',"No one to jump to, nowhere to go.", SP+"standing alone in the middle of a chalk circle on the ground, looking around nervously, the circle surrounded by smiling vaccinated stick figures", ''),
 ('h09','N',"Nineteen seventy seven, Somalia. A hospital cook named Ali Maow Maalin catches smallpox.", "a young Somali man in a simple shirt sitting on a hospital bed, a few spots on his face, a dusty landscape through the window", 'Ali Maow Maalin'),
 ('h10','N',"He survives. He's the last person ever to catch it naturally.", "the same young man standing smiling outside a small hospital building, healthy", 'the last one'),
 ('h11','N',"He spent the rest of his life vaccinating children against polio.", "the same man, older, kneeling and giving oral vaccine drops into the mouth of a little child held by her mother", ''),
 ('h12','N',"On the eighth of May, nineteen eighty, the world declared smallpox gone.", "an official-looking parchment certificate with a red wax seal and a ribbon, on a wooden desk, a pen beside it, no readable text", '8 May 1980'),
 ('h13','S',"This is outrageous.", SP+"packing a small leather travel suitcase in a hurry, his wig crooked, looking indignant", ''),
 ('h14','N',"Final score.", BOARD+"the SMALLPOX column is crossed out with a big chalk X, and under HUMANS the word 'WIN' written large and underlined twice", ''),

 # ---- p8 ending ----
 ('i01','N',"Well, almost gone.", "a single heavy steel laboratory freezer door with frost on it and a big padlock", ''),
 ('i02','N',"Two freezers still hold the virus: one in the United States, one in Russia.", "two heavy steel laboratory freezers side by side with frost and padlocks, a tiny American flag on one and a tiny Russian flag on the other", ''),
 ('i03','N',"Scientists have argued for decades about whether to destroy them.", "a long table of scientists in white lab coats arguing, some pointing up, some shaking their heads", ''),
 ('i04','S',"I'll wait.", SP+"sitting inside a frosty freezer on a small chair, wrapped in a blanket, sipping a cup of tea, smiling politely at the viewer", ''),
 ('i05','N',"So next time someone asks if vaccines ever really work, tell them about the cow.", "the cow in the little red cape winking at the viewer, a small heart floating above its head", ''),
 ('i06','N',"Would you have let Jenner scratch your arm in seventeen ninety six? Tell me in the comments.", YOU(TRI)+"rolling up the sleeve of one arm and holding it out bravely, eyes squeezed shut, the cow peeking in from the side of the frame", ''),
]

if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    voices = os.path.join(here, '../../../voices/smallpox_ketchup'); os.makedirs(voices, exist_ok=True)
    with open(os.path.join(voices, 'lines.txt'), 'w') as f:
        for i, r, t, _, _ in L: f.write(f"{i}|{'NARRATOR' if r == 'N' else 'SMALLPOX'}|{t}\n")
    frames = [{'id': i, 'line': t, 'prompt': STYLE + p + (NOTE.format(n) if n else NOTEXT)} for i, r, t, p, n in L]
    json.dump(frames, open(os.path.join(here, 'frames.json'), 'w'), indent=1)
    words = sum(len(t.split()) for _, _, t, _, _ in L)
    assert not any('often' in t.lower() for _, _, t, _, _ in L)
    print(len(L), 'lines', words, 'words', f'~{words / 2.6 / 60 * 1/1.08:.1f} min')
