import json,sys
sys.path.insert(0,'.')
from relabel import find, box, mask
from manual_arrow import lab
S=88; BIG=150
# per block: list of (text, preferred frame, wx, wy, size)
B={
1:[("essays · art · translation","F01",.55,.1,S),("is my job next?","F101",.05,.1,S)],
2:[("10 jobs AI can barely touch","F02",.2,.06,S),("real research","F102",.05,.1,S),("pays better than you think","F402",.05,.1,S)],
3:[("#10 the roofer","F03",.6,.1,S),("200,000 real AI chats","F203",.05,.1,S),("which jobs can AI help?","F103",.05,.1,S),("near the very bottom","F403",.05,.1,S)],
4:[("steep · wet · windy","F04",.6,.1,S),("weather","F404",.05,.1,S),("can't climb a ladder","F204",.62,.1,S)],
5:[("#9 the massage therapist","F05",.55,.1,S),("same study, same result","F205",.6,.1,S)],
6:[("AI can guess","F106",.05,.1,S),("can't feel the knot","F06",.6,.1,S),("no thanks","F406",.05,.1,S),("much better","F206",.6,.1,S)],
7:[("#8 the plumber","F07",.6,.1,S),("every house is a puzzle","F07",.6,.3,S),("a leak behind the wall","F207",.6,.1,S)],
8:[("the exact opposite","F08",.6,.1,S),("still getting calls","F408",.05,.1,S)],
9:[("#7 the electrician","F09",.55,.1,S),("+9% by 2034 (US)","F209",.05,.1,S),("~77,000 new jobs","F409",.05,.1,S)],
10:[("the AI boom needs them","F410",.05,.1,S),("data centers","F10",.6,.1,S),("charging stations","F110",.05,.1,S)],
11:[("#6 wind turbine technician","F11",.5,.1,S),("almost +50% by 2034","F211",.05,.1,S)],
12:[("hundreds of feet up","F12",.05,.1,S),("as big as a bus","F412",.05,.1,S),("clip in","F111",.05,.1,S),("no software update","F112",.05,.1,S)],
13:[("#5 hazmat removal worker","F13",.55,.1,S),("asbestos · lead · toxic waste","F113",.05,.1,S),("suit up","F213",.62,.1,S),("sealed off","F413",.05,.1,S)],
14:[("top 10 least touched by AI","F414",.3,.06,S),("strict rules","F14",.6,.1,S),("every mistake is dangerous","F214",.55,.1,S)],
15:[("#4 the phlebotomist","F15",.55,.1,S),("draws your blood","F215",.62,.1,S),("touched least of all","F415",.4,.06,S)],
16:[("calming a 5-year-old","F16",.6,.1,S),("brave!","F216",.05,.1,S),("no machine does this yet","F416",.05,.1,S)],
17:[("#3 the embalmer","F17",.6,.1,S),("a quiet job","F417",.05,.1,S),("so families can say goodbye","F217",.05,.1,S)],
18:[("steady hands","F118",.05,.1,S),("respect","F18",.05,.1,S),("least affected by AI","F418",.4,.06,S),("too human to hand over","F218",.05,.1,S)],
19:[("#2 the nurse practitioner","F19",.55,.1,S),("examine · diagnose · treat","F219",.05,.1,S),("fastest growing in healthcare","F119",.05,.1,S),("~+40% by 2034 (US)","F419",.4,.06,S)],
20:[("AI helps with notes","F120",.05,.1,S),("someone sits with you","F20",.6,.1,S),("trusted with the decision","F220",.05,.1,S)],
21:[("#1 the home health aide","F21",.05,.1,S),("medicine on time","F121",.05,.1,S),("the human side of care","F421",.05,.1,S)],
22:[("+740,000 jobs by 2034","F222",.3,.06,S),("more than any other job (US)","F422",.05,.85,S)],
23:[("most exposed to AI","F23",.55,.1,S),("data entry clerks","F223",.05,.1,S),("postal clerks","F423",.05,.1,S)],
24:[("tasks change","F124",.05,.1,S),("170M new · 92M lost by 2030 (WEF)","F24",.4,.1,S)],
25:[("Moravec's paradox","F25",.05,.1,S),("easy for a 1-year-old","F425",.05,.1,S)],
26:[("hands · unpredictable places · trust","F26",.1,.1,S),("still mostly true","F126",.05,.1,S),("not anytime soon","F226",.05,.1,S)],
27:[("your pick?","F27",.6,.3,S),("tell us below","F127",.05,.85,S),("subscribe!","F227",.62,.1,BIG),("next: jobs AI is changing now","F427",.05,.1,S)],
}
NOMOVE={l.strip() for l in """#10 the roofer|#9 the massage therapist|#8 the plumber|#7 the electrician|#6 wind turbine technician|#5 hazmat removal worker|#4 the phlebotomist|#3 the embalmer|#2 the nurse practitioner|#1 the home health aide|subscribe!|brave!|can't climb a ladder|no thanks|much better|data centers|charging stations|suit up|sealed off|draws your blood|respect|steady hands|medicine on time|tell us below|Moravec's paradox|easy for a 1-year-old|still mostly true|not anytime soon|as big as a bus|no software update|is my job next?|real research|weather|AI can guess|can't feel the knot|the exact opposite|still getting calls|clip in|calming a 5-year-old|no machine does this yet|a quiet job|AI helps with notes|trusted with the decision|someone sits with you|tasks change|your pick?|a leak behind the wall|every house is a puzzle|next: jobs AI is changing now|200,000 real AI chats|near the very bottom|which jobs can AI help?""".split("|")}
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
