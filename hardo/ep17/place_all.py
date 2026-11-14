import json,sys
sys.path.insert(0,'.')
from relabel import find, box
S=88; BIG=150
B={
1:[("~$150,000 a year","F01",.45,.3,S),("no degree needed?","F101",.05,.1,S),("nobody applies","F201",.5,.06,S),("help wanted","F401",.05,.1,S)],
2:[("10 jobs that pay well","F02",.3,.08,S),("typical US job: $50,980","F102",.05,.08,S),("money vs. price","F202",.3,.06,S),("why so empty?","F402",.05,.1,S)],
3:[("#10 wastewater plant operator","F03",.4,.08,S),("everything you flush","F103",.55,.08,S),("clean water out","F203",.55,.1,S),("open 24/7","F403",.05,.1,S)],
4:[("median: ~$60,000","F04",.45,.1,S),("dangerous gases","F104",.6,.08,S),("nights & holidays","F204",.45,.08,S),("wet, slippery floors","F404",.05,.1,S)],
5:[("#9 ironworker","F05",.5,.08,S),("50 stories up","F205",.55,.08,S),("bolting skyscrapers","F105",.05,.08,S),("narrow beams","F405",.05,.1,S)],
6:[("median: ~$63,000","F06",.45,.1,S),("always clipped in","F106",.05,.08,S),("too windy? stop","F206",.45,.08,S),("ice = no work","F406",.05,.1,S)],
7:[("#8 rig drill operator","F07",.45,.08,S),("deep into the ground","F107",.4,.06,S),("far out at sea","F207",.05,.1,S),("noise & mud","F407",.05,.1,S)],
8:[("median: ~$68,000","F08",.45,.1,S),("weeks away","F408",.05,.1,S),("7 days a week","F208",.05,.08,S),("home is a bunk","F108",.05,.08,S)],
9:[("#7 roof bolter","F09",.5,.08,S),("steel roof bolt","F109",.4,.06,S),("holds the ceiling up","F209",.45,.06,S),("looking up all day","F409",.05,.1,S)],
10:[("~$75,000 a year","F10",.45,.1,S),("far below the surface","F210",.45,.08,S),("dark & dusty","F410",.05,.1,S)],
11:[("#6 locomotive engineer","F11",.05,.08,S),("over a mile long","F111",.3,.06,S),("throttle","F211",.05,.08,S),("runs day and night","F411",.05,.1,S)],
12:[("median: ~$81,000","F12",.45,.1,S),("calls from the road","F112",.05,.08,S),("another motel","F212",.5,.08,S),("seniority picks shifts","F412",.05,.1,S)],
13:[("#5 ship captain","F13",.45,.08,S),("lakes · rivers · oceans","F113",.3,.06,S),("barges too","F213",.05,.08,S),("always on watch","F413",.05,.1,S)],
14:[("median: ~$92,000","F14",.45,.1,S),("family on a photo","F114",.05,.85,S),("months at sea","F214",.45,.08,S),("7 days a week on board","F414",.05,.08,S)],
15:[("#4 power line worker","F15",.45,.08,S),("no power at home","F115",.05,.08,S),("first out after storms","F215",.4,.06,S),("live wires down","F415",.05,.1,S)],
16:[("median: ~$95,000","F16",.05,.1,S),("insulated tools","F116",.05,.08,S),("sleep in the truck","F216",.05,.08,S),("high-voltage towers","F416",.05,.1,S)],
17:[("#3 elevator mechanic","F17",.45,.08,S),("inside the shaft","F217",.45,.06,S),("steel cables","F117",.05,.08,S),("cramped machine room","F417",.05,.1,S)],
18:[("median: ~$110,000","F18",.45,.1,S),("on call 24/7","F118",.05,.08,S),("stuck? he's coming","F218",.05,.08,S),("going down?","F418",.05,.1,S)],
19:[("#2 nuclear reactor operator","F19",.35,.08,S),("cooling towers","F119",.05,.06,S),("every light matters","F219",.45,.06,S),("controls the reactor","F419",.05,.1,S)],
20:[("median: ~$123,000","F20",.45,.1,S),("heavy security","F120",.05,.08,S),("rotating night shifts","F220",.05,.06,S),("fully alert","F420",.05,.1,S)],
21:[("#1 air traffic controller","F21",.4,.08,S),("thousands of planes a day","F221",.3,.06,S),("keep them apart","F421",.3,.85,S),("every dot is a plane","F121",.05,.06,S)],
22:[("median: ~$148,000","F22",.45,.1,S),("about 3x the typical job","F122",.05,.06,S),("total focus","F222",.05,.85,S),("must retire at 56","F422",.05,.08,S)],
23:[("~3,000 short (US)","F23",.45,.1,S),("10-hour days, 6 days a week","F123",.05,.85,S),("end of the shift","F223",.45,.08,S),("coffee, again","F423",.05,.1,S)],
24:[("heights · darkness · danger","F24",.25,.15,S),("the price","F124",.05,.08,S),("high up · deep down","F224",.55,.1,S),("storms","F424",.05,.1,S)],
25:[("training, not a degree","F25",.45,.1,S),("no diploma needed","F125",.25,.85,S),("learn on the job","F225",.45,.06,S),("steady nerves","F425",.05,.1,S)],
26:[("which way?","F26",.55,.1,S),("pay or price?","F126",.05,.06,S),("worth it?","F226",.05,.08,S),("proud of it","F426",.05,.1,S)],
27:[("which would you do?","F27",.3,.08,S),("tell us below","F127",.05,.85,S),("subscribe!","F227",.05,.1,BIG),("next: jobs that may disappear","F427",.05,.1,S)],
}
NOMOVE={'sleep in the truck','high up · deep down','cramped machine room','lakes · rivers · oceans','throttle','steel roof bolt','steel cables','cooling towers','family on a photo','home is a bunk','calls from the road','no power at home','insulated tools','heavy security','every dot is a plane','about 3x the typical job','the price','pay or price?','no diploma needed','typical US job: $50,980','dangerous gases','everything you flush','help wanted','no degree needed?','tell us below','going down?','on call 24/7'}
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
