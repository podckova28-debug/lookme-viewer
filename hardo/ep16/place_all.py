import json,sys
sys.path.insert(0,'.')
from relabel import find, box
S=88; BIG=150
B={
1:[("alone","F01",.4,.3,S),("no coworkers","F101",.6,.1,S),("just you and the wind","F201",.55,.1,S),("no small talk","F401",.05,.1,S)],
2:[("10 loneliest jobs on Earth","F02",.35,.08,S),("practice for Mars","F102",.05,.1,S),("counted down","F202",.3,.15,S)],
3:[("#10 the lighthouse keeper","F03",.45,.1,S),("lamp lit every night","F203",.45,.1,S),("only way off: a boat","F403",.05,.1,S)],
4:[("machines took over","F104",.05,.1,S),("UK: last keepers left 1998","F204",.5,.1,S),("US: last keeper retired 2023","F04",.45,.3,S),("goodbye","F404",.05,.1,S)],
5:[("#9 the penguin postmaster","F05",.45,.1,S),("Port Lockroy, Antarctica","F205",.3,.06,S),("~5 months a season","F405",.05,.1,S)],
6:[("tens of thousands of postcards","F106",.3,.06,S),("counting gentoo penguins","F06",.5,.1,S),("no running water","F206",.05,.1,S),("just you and the penguins","F406",.05,.1,S)],
7:[("#8 the fire lookout","F07",.55,.1,S),("watching for smoke","F207",.05,.1,S),("Kerouac: 63 days in 1956","F407",.05,.1,S)],
8:[("smoke!","F08",.6,.1,S),("planes · cameras · satellites","F208",.4,.06,S),("a few hundred still staffed","F408",.05,.1,S)],
9:[("#7 the sheepherder","F09",.55,.1,S),("months on the move","F209",.05,.85,S),("a horse and two dogs","F409",.05,.1,S)],
10:[("no signal","F10",.55,.1,S),("coyotes","F110",.6,.1,S),("“struck by sagebrush”","F210",.5,.1,S),("nobody to talk to","F410",.05,.1,S)],
11:[("#6 the long-haul trucker","F11",.05,.1,S),("~2.2 million US truck drivers","F211",.3,.06,S),("hours alone","F411",.05,.1,S)],
12:[("eats alone","F12",.55,.1,S),("calls home","F212",.05,.1,S),("millions of strangers","F412",.05,.1,S)],
13:[("#5 the island weather observer","F13",.4,.1,S),("2,000+ km from any continent","F213",.35,.06,S),("wind","F413",.05,.1,S)],
14:[("one ship a year","F14",.5,.1,S),("fresh food!","F114",.3,.06,S),("~13 months on the island","F214",.3,.06,S),("forgot it? wait a year","F414",.05,.1,S)],
15:[("#4 the saturation diver","F15",.5,.1,S),("up to 28 days under pressure","F415",.05,.1,S)],
16:[("squeaky voice","F16",.55,.1,S),("days to decompress","F216",.55,.1,S),("slowly back to normal","F416",.05,.1,S)],
17:[("#3 the submariner","F17",.3,.06,S),("2–3 months underwater","F217",.05,.1,S),("no sunlight · no internet","F417",.05,.1,S)],
18:[("stay hidden","F18",.05,.1,S),("~40 words from home","F118",.55,.1,S),("all the news for months","F418",.05,.1,S)],
19:[("#2 the South Pole winter crew","F19",.35,.1,S),("~40 people stay","F119",.3,.06,S),("the last plane leaves","F219",.4,.06,S),("see you in October","F419",.05,.1,S)],
20:[("6 months of darkness","F20",.55,.1,S),("below −100°F","F120",.05,.1,S),("help is far away","F420",.3,.85,S),("check-up","F220",.05,.1,S)],
21:[("#1 Concordia winter crew","F21",.45,.1,S),("nearest humans: 600 km","F121",.05,.06,S),("no plane can reach them","F421",.05,.1,S)],
22:[("~4 months without sun","F22",.55,.1,S),("“White Mars”","F222",.4,.06,S),("down to −80°C","F422",.05,.1,S)],
23:[("BONUS: Apollo command module pilot","F23",.3,.06,S),("alone in orbit","F123",.05,.1,S),("2 on the Moon","F223",.55,.1,S),("1969","F423",.05,.1,S)],
24:[("~47 min without radio","F24",.4,.1,S),("silence","F124",.05,.1,S),("“almost joy”","F224",.6,.1,S),("every orbit","F424",.05,.85,S)],
25:[("quiet · focus · the view","F25",.6,.1,S),("peace","F125",.05,.1,S),("a view almost nobody sees","F225",.05,.85,S),("why choose this?","F425",.05,.1,S)],
26:[("practice for Mars","F26",.6,.1,S),("nobody to talk to","F126",.05,.1,S),("call a friend","F226",.05,.1,S),("loneliness ≠ distance","F426",.3,.1,S)],
27:[("which could you handle?","F27",.3,.08,S),("tell us below","F127",.05,.85,S),("subscribe!","F227",.05,.1,BIG),("next: jobs that pay insanely well","F427",.35,.1,S)],
}
NOMOVE={'nearest humans: 600 km','a horse and two dogs','calls home'}
p=json.load(open('plan_wish.json'))
used={s[1] for b in p['blocks'] for s in b}
L={}; occ={}
from PIL import Image
def wh(n): return Image.open(f"frames/{n}.png").size
for b,items in B.items():
    frames=[s[1] for s in p['blocks'][b-1]]
    for text,pref,wx,wy,sz in items:
        assert pref in used,(pref)
        sizes=[sz,int(sz*.85),int(sz*.72),int(sz*.62),int(sz*.52)]
        order=[pref] if (text.startswith('#') or text.startswith('BONUS') or text in NOMOVE) else [pref]+[f for f in frames if f!=pref]
        r=None
        for fr in order:
            if len(L.get(fr,[]))>=2: continue
            w,h=wh(fr)
            r=find(fr,text,wx,wy,sizes,occ.get(fr,[]))
            if r:
                L.setdefault(fr,[]).append(r); occ.setdefault(fr,[]).append(box(text,r[1][0],r[1][1],r[4],w,h))
                print(f"{b:2d} {fr:5s} {r[4]:3d} {text}" + ("" if fr==pref else f"   (moved from {pref})")); break
        if not r: print(f"{b:2d} MISS {text}")
p['labels']=L
json.dump(p,open('plan.json','w'),indent=1)
