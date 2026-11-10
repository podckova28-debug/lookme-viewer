import json,sys
sys.path.insert(0,'.')
from relabel import find, box, mask
from manual_arrow import lab
S=88; BIG=150
# per block: list of (text, preferred frame, wx, wy, size)
B={
1:[("60 ft down","F01",.62,.1,S),("can't see a thing","F101",.05,.1,S),("the Gulf of Mexico","F201",.62,.1,S),("start a fire. underwater.","F401",.05,.1,S)],
2:[("what the sea breaks","F02",.6,.1,S),("fixed underwater","F202",.62,.1,S),("most dangerous job?","F402",.05,.1,S)],
3:[("dive school","F03",.62,.1,S),("2–7 months","F103",.05,.1,S),("$15,000–$24,000","F203",.55,.1,S),("+ room & food","F403",.05,.1,S)],
4:[("now do it blind","F04",.62,.1,S),("by touch","F104",.05,.1,S),("murky tank","F204",.62,.1,S),("practice","F404",.05,.1,S)],
5:[("graduated!","F05",.62,.1,S),("not a diver yet","F05",.62,.3,S),("the bottom rung","F205",.62,.1,S),],
6:[("tender","F06",.62,.1,S),("the umbilical","F106",.05,.1,S),("air · radio · hot water","F206",.55,.1,S)],
7:[("weeks offshore","F07",.62,.1,S),("12-hour shifts","F107",.05,.1,S),("so does your stomach","F407",.05,.1,S)],
8:[("you're diving.","F08",.62,.1,S),("the boss","F108",.05,.1,S),("finally!","F208",.62,.1,S),("your turn","F408",.05,.1,S)],
9:[("hot-water suit","F109",.05,.1,S),("in you go","F209",.62,.1,S),("heater on deck","F409",.05,.1,S)],
10:[("down the line","F10",.05,.1,S),("light turns green","F110",.05,.1,S),("33 ft: 2× pressure","F210",.05,.1,S)],
11:[("zero visibility","F11",.62,.1,S),("by touch","F111",.05,.1,S),("read the steel","F411",.62,.1,S)],
12:[("the supervisor","F12",.62,.1,S),("helmet camera","F112",.05,.1,S),("talk the whole time","F212",.6,.1,S),("silence = trouble","F412",.05,.1,S)],
13:[("wet welding","F13",.62,.1,S),("the stinger","F113",.05,.1,S),("the only light","F213",.05,.1,S),("steam & bubbles","F413",.05,.1,S)],
14:[("\"make it hot\"","F14",.05,.1,S),("power on","F114",.05,.1,S),("never touch it live","F214",.6,.1,S),("hundreds of amps","F414",.05,.1,S)],
15:[("welding in dry air","F15",.62,.1,S),("a clean weld","F115",.05,.1,S),("brittle vs. clean","F415",.05,.1,S)],
16:[("\"15% die\"?","F16",.62,.1,S),("myth.","F116",.05,.1,S),("not true","F216",.62,.1,S),("but...","F416",.05,.1,S)],
17:[("~159 per 100,000 a year","F17",.05,.1,S),("about 1 in 600","F117",.05,.85,S),("Alaska study","F217",.05,.1,S),("40× the average","F417",.05,.1,S)],
18:[("Delta P","F18",.62,.1,S),("sucked in","F118",.05,.1,S),("pre-dive check","F218",.5,.1,S),("tangled hoses","F418",.05,.1,S)],
19:[("the bends","F19",.05,.1,S),("gas bubbles","F119",.05,.85,S),("joint pain","F219",.62,.1,S),("knees · elbows · shoulders","F419",.05,.1,S)],
20:[("come up slowly","F20",.62,.1,S),("wait.","F120",.05,.1,S),("dinner. without you.","F420",.05,.1,S)],
21:[("saturation diving","F21",.62,.1,S),("up to 28 days","F121",.05,.1,S),("living under pressure","F221",.05,.1,S),("home for a month","F421",.62,.1,S)],
22:[("helium voices","F22",.62,.1,S),("room service","F122",.05,.1,S),("the diving bell","F422",.05,.1,S)],
23:[("going home takes days","F23",.55,.1,S),("~8 days from 650 ft","F123",.05,.1,S),("no early exit","F223",.62,.1,S),("daylight!","F423",.05,.1,S)],
24:[("~$61,300 a year","F24",.62,.1,S),("median pay (BLS)","F124",.05,.1,S),("sat divers earn more","F224",.05,.1,S),("going home","F424",.05,.1,S)],
25:[("home!","F25",.62,.1,S),("diesel.","F125",.05,.1,S),("bad signal","F225",.62,.1,S),("no birthday","F425",.05,.1,S)],
26:[("why do it?","F26",.62,.1,S),("nobody sees it","F126",.05,.1,S),("ships · bridges · lights","F226",.05,.1,S),("holding it together","F426",.05,.1,S)],
27:[("your best weld","F27",.05,.1,S),("60 ft down","F127",.05,.1,S),("would you do it?","F227",.05,.1,S),("subscribe!","F427",.05,.06,BIG)],
}
NOMOVE={'not a diver yet','tangled hoses','room service','no birthday','dinner. without you.','going home','tender','the supervisor','the umbilical','the stinger','Delta P','the bends','saturation diving','subscribe!','the diving bell','wet welding','dive school'}
p=json.load(open('plan_wish.json'))
clips={s[1] for b in p['blocks'] for s in b if s[0]=='clip'}
L={}; occ={}
from PIL import Image
def wh(n): return Image.open(f"frames/{n}.png").size

miss=[]
for b,items in B.items():
    frames=[f"F{b:02d}",f"F{200+b}",f"F{400+b}",f"F{100+b}"]
    for text,pref,wx,wy,sz in items:
        sizes=[sz,int(sz*.85),int(sz*.72)] if sz==BIG else [sz,int(sz*.85),int(sz*.72)]
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
