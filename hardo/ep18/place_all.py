import json,sys
sys.path.insert(0,'.')
from relabel import find, box
S=88; BIG=150
B={
1:[("5,070 deaths at work (2024)","F01",.45,.1,S),("up to 30x higher","F101",.5,.08,S),("10 deadliest jobs","F201",.6,.75,S),("just a normal workday","F401",.5,.08,S)],
2:[("ranked by death rate","F02",.3,.08,S),("source: U.S. BLS","F102",.05,.08,S),("danger meter","F202",.5,.08,S),("average job: 3.3 per 100,000","F402",.05,.08,S)],
3:[("#10 grounds maintenance","F03",.45,.08,S),("landscaper","F203",.05,.08,S),("~21 deaths per 100,000","F403",.45,.1,S)],
4:[("swinging branch","F04",.5,.1,S),("chainsaw up high","F104",.05,.08,S),("not the mower","F204",.5,.08,S),("no room for mistakes","F404",.45,.1,S)],
5:[("#9 truck driver","F05",.5,.08,S),("~26 deaths per 100,000","F405",.45,.1,S),("rain & mountains","F205",.05,.08,S)],
6:[("most deaths of any job","F06",.3,.08,S),("~800 drivers died (2024)","F406",.4,.1,S),("long hours","F106",.05,.85,S),("tired drivers","F206",.5,.1,S)],
7:[("#8 underground miner","F207",.3,.08,S),("huge machines","F07",.5,.1,S),("cutting drum","F107",.5,.85,S),("deep below the surface","F207",.3,.85,S)],
8:[("~36 deaths per 100,000","F08",.45,.1,S),("falling rock","F108",.55,.1,S),("roof supports","F408",.45,.1,S),("few ways out","F208",.45,.1,S)],
9:[("#7 construction helper","F09",.45,.08,S),("no railing","F209",.5,.1,S),("learning on the job","F409",.05,.08,S)],
10:[("first day on site","F10",.5,.1,S),("~36 deaths per 100,000","F210",.3,.85,S),("10x average","F410",.5,.08,S)],
11:[("#6 pilot","F11",.5,.1,S),("airliners: very safe","F111",.3,.1,S),("small plane","F211",.5,.08,S),("bush plane","F411",.6,.85,S)],
12:[("small planes, bad weather","F12",.4,.1,S),("~37 deaths per 100,000","F412",.45,.1,S)],
13:[("#5 garbage collector","F13",.45,.08,S),("before sunrise","F213",.6,.1,S),("riding on the back","F413",.5,.1,S)],
14:[("~37 deaths per 100,000","F14",.45,.1,S),("in the dark","F214",.6,.85,S),("passing traffic","F414",.05,.08,S),("their own heavy truck","F114",.3,.06,S)],
15:[("#4 ironworker","F15",.5,.08,S),("steel beams","F115",.6,.85,S),("bridges & skyscrapers","F215",.3,.08,S),("high above the ground","F415",.5,.1,S)],
16:[("~38 deaths per 100,000","F16",.45,.1,S),("always clipped in","F116",.5,.85,S),("one slip...","F416",.6,.1,S),("one loose beam","F216",.5,.85,S)],
17:[("#3 roofer","F17",.5,.08,S),("the way up","F217",.6,.85,S),("sun & wind","F417",.5,.1,S)],
18:[("~49 deaths per 100,000","F18",.45,.1,S),("15x the average job","F418",.45,.1,S),("roof anchor","F118",.05,.85,S),("#1 killer: falls","F218",.05,.08,S)],
19:[("#2 commercial fisherman","F19",.4,.08,S),("storms at sea","F119",.3,.06,S),("heavy, wet gear","F219",.55,.08,S),("heavy crab pots","F419",.5,.85,S)],
20:[("~89 deaths per 100,000","F20",.45,.1,S),("boats can sink fast","F420",.5,.85,S),("survival suit","F120",.05,.08,S),("rescue: hours away","F220",.45,.85,S)],
21:[("#1 logger","F21",.5,.08,S),("steep forests","F121",.4,.06,S),("chainsaw","F221",.05,.85,S),("far from any road","F421",.4,.06,S)],
22:[("~110 deaths per 100,000","F22",.45,.1,S),("30x the average job","F222",.3,.06,S),("most deaths: falling trees","F422",.3,.06,S),("logs roll the wrong way","F122",.3,.06,S)],
23:[("the danger is the job itself","F23",.4,.1,S),("giant tree","F223",.5,.1,S),("calm & careful","F423",.5,.85,S)],
24:[("what they share","F24",.5,.12,S),("heights · water","F124",.6,.5,S),("machines · falling trees","F224",.5,.1,S),("far from help","F424",.3,.12,S)],
25:[("firefighters: ~4 per 100,000","F25",.45,.3,S),("police: ~8.5 per 100,000","F25",.45,.55,S),("not even close","F125",.3,.85,S),("jobs we barely notice","F225",.05,.06,S),],
26:[("safety gear saves lives","F26",.45,.1,S),("clipped in","F126",.05,.08,S),("home safe","F226",.6,.1,S)],
27:[("which would you never do?","F27",.25,.12,S),("tell us below","F127",.05,.85,S),("subscribe!","F227",.05,.1,BIG),("next: jobs that may disappear","F427",.05,.1,S)],
}
NOMOVE={'huge machines','#8 underground miner','source: U.S. BLS','climbing rope','landscaper','not the mower','cutting drum','roof supports','few ways out','new vs. experienced','airliners: very safe','small plane','bush plane','every single week','in the dark','steel beams','always clipped in','one loose beam','the way up','roof anchor','#1 killer: falls','heavy crab pots','rescue: hours away','steep forests','30x the average job','giant tree','what they share','heights · water','machines · falling trees','far from help','firefighters: ~4 per 100,000','police: ~8.5 per 100,000','not even close','tell us below','next: jobs that may disappear','home safe','clipped in','danger meter','10 deadliest jobs','up to 30x higher','safety gear saves lives'}
p=json.load(open('plan_wish.json'))
used={s[1] for b in p['blocks'] for s in b}
L={}; occ={}
from PIL import Image
def wh(n): return Image.open(f"frames/{n}.png").size
for b,items in B.items():
    frames=[s[1] for s in p['blocks'][b-1]]
    for text,pref,wx,wy,sz in items:
        assert pref in used,(pref)
        sizes=[sz,int(sz*.85),int(sz*.72)]
        order=[pref] if (text.startswith('#') or text in NOMOVE) else [pref]+[f for f in frames if f!=pref]
        r=None
        for fr in order:
            if len(L.get(fr,[]))>=2: continue
            w,h=wh(fr); r=find(fr,text,wx,wy,sizes,occ.get(fr,[]))
            if r:
                L.setdefault(fr,[]).append(r); occ.setdefault(fr,[]).append(box(text,r[1][0],r[1][1],r[4],w,h))
                if fr!=pref: print(f"{b:2d} {fr} {r[4]} {text} (moved)")
                break
        if not r: print(f"{b:2d} MISS {text}")
p['labels']=L
json.dump(p,open('plan.json','w'),indent=1)
