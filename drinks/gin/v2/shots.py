# Gin v2 (mead/ketchup formula). frame -> (part, line, desc, note). desc = int -> reuse frame N of the v1 gin video.
# Running gag: the tavern chalkboard score "GIN vs PARLIAMENT". Callbacks: the straw, the Dutch doctors.
STYLE = ("White background; detailed ink-line illustration, fine cross-hatching, soft muted watercolour, juniper blue-green and pewter grey accents, "
         "playful humorous cartoon tone; cut out on white, lots of white space, the whole drawing well inside the frame with wide empty margins. ")
YOU = "one simple white round-headed stick figure with dot eyes, exactly two arms and two legs, wearing a small black tricorn hat, "
BOARD = ("an old dark green wooden tavern chalkboard on a wooden easel, written on it in white chalk two columns headed 'GIN' and 'PARLIAMENT', "
         "a short chalk line under the headings; objects only, no people, no hands; ")
SHOTS = [
 # p0
 (0,0,1,""),(0,1,2,""),(0,2,3,""),(0,3,4,""),(0,4,5,""),(0,5,6,""),
 (0,6,YOU+"lying flat on his back on a pile of clean straw on a cellar floor, legs sticking up in the air, dizzy spirals above his head, a small empty pewter cup beside him","legs: off"),
 (0,7,"a pile of clean straw with a small fluffy pillow on top and a little folded towel, like a hotel bed, next to a tiny wooden sign with five painted stars; objects only, no people","customer service"),
 (0,8,8,""),(0,9,9,""),(0,10,11,""),
 (0,11,"one 18th-century member of Parliament in a white powdered wig and long dark coat, standing alone, slamming one rolled paper scroll down on a wooden table, determined face","again"),
 (0,12,"the same kind of 18th-century member of Parliament in a white wig, standing alone, sweating, holding up one new paper scroll, a pile of crumpled scrolls at his feet","and again"),
 (0,13,"one 18th-century member of Parliament in a crooked white wig slumped exhausted over a wooden table covered in a huge heap of paper scrolls","and again..."),
 (0,14,BOARD+"under GIN many chalk tally marks, under PARLIAMENT nothing","spoiler"),
 (0,15,12,""),(0,16,13,""),
 # p1
 (1,0,14,""),(1,1,15,""),(1,2,16,""),
 (1,3,"a 17th-century plague doctor in a long black coat and bird-beak mask standing alone, holding one small glass of genever in one hand and shrugging with the other hand","didn't work"),
 (1,4,18,""),
 (1,5,"three cheerful 17th-century Dutch townspeople standing in a queue at a wooden apothecary counter, each holding out one empty small cup, all pretending to cough, a bottle of genever on the counter","more medicine, please"),
 (1,6,20,""),(1,7,17,""),(1,8,21,""),(1,9,22,""),(1,10,23,""),
 (1,11,"two 17th-century English soldiers in morion helmets and breastplates standing side by side, jaws dropped, eyes wide, very impressed, their arms at their sides","impressed"),
 (1,12,24,""),(1,13,25,""),(1,14,26,""),
 # p2
 (2,0,27,""),(2,1,28,""),(2,2,30,""),(2,3,31,""),
 (2,4,"an 18th-century paper document with the word 'LICENCE' crossed out with a big red X, next to a small copper pot still; objects only, no people","no licence"),
 (2,5,"a 1690s Englishman in a nightcap and shirtsleeves standing alone next to a small rattling copper still, reading a book that is upside down, confused","no training"),
 (2,6,"a small copper still in a wooden shed bursting comically in a puff of grey smoke, its cork flying off; a 1690s man standing next to it with soot on his face and his hair standing up, arms at his sides","no idea"),
 (2,7,32,""),(2,8,33,""),(2,9,34,""),(2,10,35,""),(2,11,36,""),(2,12,37,""),(2,13,40,""),(2,14,41,""),
 # p3
 (3,0,"a big red rubber-stamp imprint reading 'EVERYTHING' in capital letters, slightly crooked; nothing else, no people",""),
 (3,1,42,""),(3,2,43,""),(3,3,45,""),(3,4,46,""),(3,5,47,""),
 (3,6,"a heavy 18th-century prison cell door with a small barred window, a small pewter cup of gin balanced on the stone ledge of the barred window, nobody visible behind the bars; objects only, no people, no hands, no faces","even prisons"),
 (3,7,48,""),
 (3,8,YOU+"holding one small cup of gin, staring at a stoneware jar with a paintbrush resting on it, face turned green, horrified","paint thinner?!"),
 (3,9,50,""),(3,10,52,""),(3,11,53,""),
 (3,12,"an 18th-century tax notice paper nailed to the wooden door of a gin shop, its text not readable, a big red seal on it; objects only, no people","a tax"),
 (3,13,BOARD+"under GIN the number 1, under PARLIAMENT the number 0","score"),
 (3,14,54,""),
 # p4 (serious)
 (4,0,55,""),(4,1,56,""),(4,2,57,""),(4,3,58,""),(4,4,60,""),(4,5,61,""),(4,6,62,""),(4,7,64,""),
 # p5
 (5,0,67,""),(5,1,68,""),(5,2,69,""),
 (5,3,"an 18th-century clerk's wooden desk with an open, completely empty ledger, a quill in an inkwell with a cobweb on it; objects only, no people","how many?"),
 (5,4,70,""),
 (5,5,"an antique hand-drawn map of England and Wales with only two tiny red pins stuck in it; objects only, no people, no flags","in the whole country"),
 (5,6,72,""),(5,7,73,""),
 (5,8,"one 18th-century glass bottle with a plain paper label handwritten 'Cuckold's Comfort' and a little drawing of a pair of horns on the label; objects only, no people",""),
 (5,9,"one 18th-century glass bottle with a plain paper label handwritten 'Parliament Gin', a tiny white powdered wig sitting on top of the cork; objects only, no people","our favourite"),
 (5,10,74,""),(5,11,75,""),(5,12,76,""),(5,13,77,""),(5,14,78,""),
 (5,15,BOARD+"under GIN the number 2, under PARLIAMENT the number 0","still nil"),
 (5,16,66,""),(5,17,80,""),
 # p6
 (6,0,81,""),(6,1,82,""),(6,2,83,""),
 (6,3,"in 18th-century engraving style, a boarded-up crumbling pawnbroker's shop with three balls hanging above the door and cobwebs on the window; objects only, no people","business: terrible"),
 (6,4,84,""),(6,5,85,""),(6,6,86,""),(6,7,87,""),
 (6,8,"a giant wooden mallet labelled 'MORAL' smashing down onto a small wooden table, dust and splinters flying, cartoon impact lines; objects only, no people, no hands","subtle?"),
 (6,9,88,""),(6,10,89,""),(6,11,92,""),(6,12,93,""),
 (6,13,BOARD+"under GIN the number 2, under PARLIAMENT the number 1 with a small chalk star next to it","finally!"),
 (6,14,94,""),(6,15,95,""),
 # p7
 (7,0,96,""),(7,1,97,""),
 (7,2,"a sugar bowl and a stoneware jar of turpentine both crossed out with red X marks, next to a juniper branch, coriander seeds and orange peel with a green tick; objects only, no people",""),
 (7,3,98,""),
 (7,4,"a single small glass of gin on a polished mahogany bar under an enormous glittering 1830s chandelier and blazing gas lamps, tall mirrors behind; objects only, no people","better lighting"),
 (7,5,99,""),(7,6,101,""),(7,7,102,""),(7,8,103,""),(7,9,104,""),
 (7,10,15,"remember?"),
 (7,11,105,""),(7,12,107,""),(7,13,108,""),(7,14,109,""),(7,15,110,""),
 (7,16,"a 1920s man in a flat cap standing next to an old bathtub full of clear liquid, holding one small glass, his face turned green, tongue out, eyes squeezed shut","awful"),
 (7,17,111,""),(7,18,112,""),(7,19,113,""),(7,20,114,""),
 # p8
 (8,0,115,""),(8,1,116,""),(8,2,117,""),
 (8,3,"a stylish modern gin bottle with a price tag reading '£40', next to a small pile of straw crossed out with a red X; objects only, no people","straw not included"),
 (8,4,118,""),(8,5,119,""),(8,6,120,""),(8,7,121,""),
 (8,8,BOARD+"under GIN the number 2, under PARLIAMENT the number 1, and at the bottom a small chalk drawing of the London skyline with a smiley face","final score"),
 (8,9,122,""),(8,10,123,""),(8,11,124,""),
 (8,12,"a heap of black sticky molasses barrels and cut sugar cane scraps with a few cartoon flies, next to a small wooden sailing warship and a sailing ship with a plain black flag; objects only, no people","trash → navy & pirates"),
 (8,13,125,""),
]
NEG = " Anatomically correct people: every person has exactly two arms, two hands and five fingers per hand; no extra or floating limbs."
def prompt(i):
    p,l,d,n = SHOTS[i-1]
    assert isinstance(d,str)
    note = f" Handwritten marker note + arrow: '{n}'." if n else " No other text."
    people = not ("no people" in d)
    if "stick figure" in d: note += " The stick figure is the only character."
    extra = " Only what is described: do not add extra people or objects."
    return STYLE + d + "." + note + extra + (NEG if people else "")
EXTRA = {}
if __name__ == "__main__":
    import collections
    c = collections.Counter((p,l) for p,l,_,_ in SHOTS); assert max(c.values())==1
    counts = collections.Counter(p for p,_,_,_ in SHOTS); print(dict(counts), len(SHOTS))
    print("new:", [i for i,s in enumerate(SHOTS,1) if isinstance(s[2],str)])
