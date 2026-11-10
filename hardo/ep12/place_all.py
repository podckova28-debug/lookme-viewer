import json,sys
sys.path.insert(0,'.')
from relabel import find, box, mask
from manual_arrow import lab
S=88; BIG=150
# per block: list of (text, preferred frame, wx, wy, size)
B={
1:[("robot teacher","F01",.6,.1,S),("heat officer","F101",.05,.1,S),("deepfake detective","F201",.6,.1,S),("already at work.","F401",.3,.1,S)],
2:[("1,000+ employers","F02",.05,.1,S),("+170 million jobs","F102",.6,.1,S),("10 jobs. 10 years.","F202",.3,.08,S),("forecasts, not promises.","F402",.05,.08,S)],
3:[("#10","F03",.75,.1,BIG),("robotaxi helper","F03",.66,.4,S),("nobody driving.","F103",.05,.1,S),("now what?","F203",.05,.1,S),("it asks a human.","F403",.05,.1,S)],
4:[("advice, not steering","F04",.6,.1,S),("one click.","F104",.05,.1,S),("~70 helpers","F204",.6,.85,S),("~3,000 cars","F404",.05,.1,S)],
5:[("#9","F05",.75,.1,BIG),("drone supervisor","F05",.66,.4,S),("out of sight.","F205",.6,.15,S),("proposed U.S. rules","F405",.05,.1,S)],
6:[("air traffic control","F06",.62,.1,S),("one person, many drones","F106",.05,.1,S),("parcels · medicine","F406",.05,.08,S)],
7:[("#8","F07",.75,.1,BIG),("deepfake detective","F07",.62,.4,S),("urgent transfer?","F107",.62,.1,S),("real or fake?","F207",.62,.1,S),("frame by frame.","F407",.05,.08,S)],
8:[("EU law: Aug 2026","F08",.62,.12,S),("the pixel that lies.","F108",.6,.9,S),("banks · newsrooms","F208",.62,.1,S),("courts, too.","F408",.05,.1,S)],
9:[("#7","F09",.75,.1,BIG),("battery recycler","F09",.66,.4,S),("under the floor","F109",.62,.1,S),("millions worn out","F209",.25,.06,S),("open it safely.","F409",.05,.08,S)],
10:[("50% lithium by 2027","F10",.05,.1,S),("80% by 2031","F110",.05,.1,S),("2031: recycled metal","F210",.05,.08,S),("old car, new car","F410",.3,.85,S)],
11:[("#6","F11",.75,.1,BIG),("chief heat officer","F11",.62,.4,S),("the first: 2021","F111",.05,.1,S),("like a fire chief","F211",.05,.08,S),("Miami-Dade","F411",.05,.08,S)],
12:[("plant shade","F12",.62,.15,S),("paint roofs white","F112",.05,.1,S),("cooling centers","F212",.05,.06,S),("Athens · Freetown · L.A.","F412",.05,.06,S)],
13:[("#5","F13",.75,.1,BIG),("data center tech","F13",.6,.4,S),("computer warehouse","F213",.05,.06,S),("hot.","F413",.05,.1,S)],
14:[("3 a.m. repairs","F14",.05,.1,S),("swap the broken part","F114",.05,.1,S),("2× the power by 2030","F214",.05,.06,S),("more than all of Japan","F414",.05,.08,S)],
15:[("#4","F15",.75,.1,BIG),("care robot tech","F15",.6,.4,S),("Japan: aging fast","F115",.05,.1,S),("2040: need 2.7M","F215",.05,.08,S),("today: <2.2M","F415",.05,.08,S)],
16:[("the robot lifts.","F16",.62,.15,S),("half engineer","F116",.05,.85,S),("half nurse","F416",.05,.1,S)],
17:[("#3","F17",.75,.1,BIG),("wind turbine tech","F17",.55,.4,S),("fastest-growing job","F117",.05,.1,S),("~300 ft up","F217",.05,.1,S)],
18:[("+60% in 10 years","F18",.62,.15,S),("clip in.","F118",.05,.1,S),("size of a bus","F218",.62,.08,S),("solar: +48%","F418",.05,.1,S)],
19:[("#2","F19",.75,.1,BIG),("AI auditor","F19",.66,.4,S),("who decided?","F119",.05,.1,S),("check it first.","F219",.62,.15,S),("it can't explain itself.","F419",.05,.08,S)],
20:[("caught.","F220",.05,.1,S),("fake applicants","F20",.25,.85,S),("same face. new name.","F120",.2,.06,S),("EU: Dec 2027","F420",.05,.08,S)],
21:[("#1","F21",.75,.1,BIG),("robot trainer","F21",.66,.4,S),("learning by copying","F121",.05,.1,S),("first steps.","F221",.62,.15,S),("ready.","F421",.05,.1,S)],
22:[("up to $48 an hour","F22",.62,.15,S),("7+ hours a day","F122",.05,.1,S),("5'7\" to 5'11\"","F222",.05,.1,S),("role model.","F422",.05,.08,S)],
23:[("BONUS","F23",.7,.1,BIG),("farmworker","F23",.66,.4,S),("+35 million by 2030","F123",.05,.1,S),("the biggest growth","F223",.25,.85,S),("everyone eats.","F423",.62,.12,S)],
24:[("drones over fields","F24",.05,.1,S),("sensors in the soil","F124",.05,.08,S),("the farm of the future","F424",.05,.08,S)],
25:[("new machine = new job","F25",.25,.06,S),("robots need teachers","F125",.05,.1,S),("cars need helpers","F225",.25,.06,S),("AI needs auditors","F425",.05,.06,S)],
26:[("calm. careful. curious.","F26",.05,.1,S),("+ one new skill","F126",.05,.1,S),("now hiring: people","F226",.25,.06,S),("robot caretakers","F426",.05,.06,S)],
27:[("which one?","F27",.62,.12,S),("tell us below","F127",.3,.85,S),("subscribe!","F227",.38,.06,BIG),("see you in 10 years","F427",.25,.06,S)],
}
NOMOVE={'see you in 10 years','cooling centers','robot teacher','heat officer','deepfake detective','robotaxi helper','drone supervisor','battery recycler','chief heat officer','data center tech','care robot tech','wind turbine tech','AI auditor','robot trainer','farmworker','hot.','fall sensor','urgent transfer?','half nurse','clip in.','one click.'}
p=json.load(open('plan_wish.json'))
clips={s[1] for b in p['blocks'] for s in b if s[0]=='clip'}
L={}; occ={}
from PIL import Image
def wh(n): return Image.open(f"frames/{n}.png").size
L['F216']=[lab("F216","fall sensor",0.66,0.1,0.455,0.15)]; w,h=wh('F216'); occ['F216']=[box("fall sensor",.66,.1,S,w,h)]
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
