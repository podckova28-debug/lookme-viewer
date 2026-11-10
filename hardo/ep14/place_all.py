import json,sys
sys.path.insert(0,'.')
from relabel import find, box, mask
from manual_arrow import lab
S=88; BIG=150
# per block: list of (text, preferred frame, wx, wy, size)
B={
1:[("no alarm clocks","F101",.05,.1,S),("paid to wake you up","F201",.62,.1,S),("paid to empty it","F401",.05,.1,S)],
2:[("10 jobs + a bonus","F02",.3,.1,S),("from bad to unbelievable","F402",.05,.1,S)],
3:[("#10 the knocker-upper","F03",.55,.1,S),("shifts before dawn","F403",.62,.1,S),("tap tap tap","F103",.05,.1,S),("I'm up!","F203",.62,.1,S)],
4:[("pea shooter","F04",.62,.1,S),("dried peas","F104",.05,.1,S),("a few pence a week","F204",.05,.1,S),("last ones: 1970s","F404",.62,.1,S)],
5:[("#9 the leech collector","F05",.55,.1,S),("leeches for everything","F205",.05,.1,S),("1800s medicine","F405",.05,.1,S),("bare legs = bait","F105",.05,.1,S)],
6:[("up to 2,500 a day","F106",.05,.1,S),("France: 30 million+ a year","F206",.05,.1,S),("blood loss","F06",.62,.1,S),("infections","F406",.62,.1,S)],
7:[("#8 the mudlark","F07",.6,.1,S),("barefoot","F107",.05,.1,S),("anything to sell","F207",.05,.85,S)],
8:[("coal · rope · bones · nails","F108",.05,.1,S),("a few pennies","F08",.62,.1,S),("London's sewer","F208",.62,.1,S),("winter too","F408",.05,.1,S)],
9:[("#7 the pure finder","F09",.55,.1,S),("gloves & book covers","F109",.05,.1,S),("softening leather","F209",.62,.1,S),("\"pure\" = dog poo","F409",.05,.1,S)],
10:[("one glove","F110",.05,.1,S),("sold by the bucket","F410",.62,.1,S),("very elegant gloves","F210",.62,.1,S)],
11:[("#6 the whipping boy","F11",.55,.1,S),("the prince","F111",.05,.1,S),("his friend pays","F211",.05,.1,S)],
12:[("very little evidence","F212",.05,.1,S),("maybe never existed","F412",.05,.1,S),("best version of the job","F12",.62,.1,S)],
13:[("#5 the climbing boy","F13",.55,.1,S),("up into the dark","F113",.05,.1,S),("narrow chimney","F213",.05,.1,S)],
14:[("1788: age 8+","F14",.62,.1,S),("hardly enforced","F114",.05,.1,S),("stuck · burned · sick","F414",.05,.1,S),("1875: police licence","F214",.05,.1,S)],
15:[("#4 the gong farmer","F15",.55,.1,S),("the privy","F415",.05,.1,S),("by hand","F215",.62,.1,S),("into barrels","F115",.05,.1,S)],
16:[("night work only","F16",.05,.1,S),("ugh!","F416",.05,.1,S),("sixpence a day","F116",.05,.1,S)],
17:[("#3 the sin eater","F17",.55,.1,S),("Wales & western England","F117",.05,.1,S),("bread & salt","F117",.05,.85,S),("eat the sins","F217",.62,.1,S)],
18:[("shunned","F18",.62,.1,S),("everyone's sins","F118",.05,.1,S),("historians argue","F218",.05,.1,S),("put it on a CV?","F418",.05,.1,S)],
19:[("#2 the Groom of the Stool","F19",.5,.1,S),("the king's privy","F119",.05,.1,S),("royal toilet","F219",.05,.1,S),("every day. personally.","F419",.62,.1,S)],
20:[("plot twist","F20",.62,.1,S),("closest to the king","F120",.05,.1,S),("private secretary","F220",.62,.1,S),("everyone wanted it","F420",.62,.1,S)],
21:[("#1 the resurrection man","F21",.55,.1,S),("fresh graves","F121",.05,.1,S),("sold to anatomists","F421",.62,.1,S)],
22:[("~8 guineas (1828)","F122",.05,.1,S),("months of wages","F22",.62,.1,S),("iron cages","F222",.62,.1,S),("Anatomy Act 1832","F422",.05,.1,S)],
23:[("BONUS","F23",.75,.12,BIG),("Cuba, 1860s","F423",.05,.1,S),("even Shakespeare","F223",.05,.1,S)],
24:[("the lector","F224",.62,.1,S),("paid from their wages","F24",.62,.1,S),("still exists today","F124",.05,.1,S)],
25:[("no machine yet","F25",.45,.1,S),("no medicine","F425",.05,.1,S)],
26:[("your job feels bad?","F26",.62,.1,S),("could be worse","F126",.05,.1,S),("could be leeches","F226",.62,.1,S)],
27:[("your pick?","F27",.6,.3,S),("tell us below","F127",.05,.85,S),("subscribe!","F227",.62,.1,BIG),("next: our century","F427",.05,.1,S)],
}
NOMOVE={"your pick?","still exists today","the privy","Cuba, 1860s","the lector","royal toilet","put it on a CV?","medical schools","even Shakespeare","named after novels","they chose the books","pea shooter","bare legs = bait","iron cages","tap tap tap","I'm up!","#10 the knocker-upper","#9 the leech collector","#8 the mudlark","#7 the pure finder","#6 the whipping boy","#5 the climbing boy","#4 the gong farmer","#3 the sin eater","#2 the Groom of the Stool","#1 the resurrection man","BONUS","subscribe!","bread & salt","one glove","the \"gong\"","his friend pays","the prince","barefoot","dried peas","shunned"}
p=json.load(open('plan_wish.json'))
clips={s[1] for b in p['blocks'] for s in b if s[0]=='clip'}
L={}; occ={}
from PIL import Image
def wh(n): return Image.open(f"frames/{n}.png").size

miss=[]
for b,items in B.items():
    frames=[f"F{b:02d}",f"F{200+b}",f"F{400+b}",f"F{100+b}"]
    for text,pref,wx,wy,sz in items:
        sizes=[sz,int(sz*.85),int(sz*.72),int(sz*.62)]
        order=[pref] if (text in NOMOVE or text.startswith('#') or text=='BONUS') else [pref]+[f for f in frames if f!=pref]
        r=None
        for fr in order:
            if fr in clips: continue
            if len(L.get(fr,[]))>=2: continue
            w,h=wh(fr)
            r=find(fr,text,wx,wy,sizes,occ.get(fr,[]))
            if r:
                L.setdefault(fr,[]).append(r); occ.setdefault(fr,[]).append(box(text,r[1][0],r[1][1],r[4],w,h))
                print(f"{b:2d} {fr:5s} {r[4]:3d} {text}" + ("" if fr==pref else f"   (moved from {pref})")); break
        if not r: miss.append((b,text)); print(f"{b:2d} MISS {text}")
p['labels']=L
json.dump(p,open('plan.json','w'),indent=1)
print('labels',sum(len(v) for v in L.values()),'missing',len(miss))
