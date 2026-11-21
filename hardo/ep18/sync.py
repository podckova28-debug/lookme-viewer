# ep18: cut each shot on the word it illustrates (whisper word timestamps), labels on the shot where they are spoken
import json,re
W={int(k):v for k,v in json.load(open('words.json')).items()}
P=json.load(open('plan.json')); TEMPO=P['tempo']; GAP=P['gap']
import subprocess
def adur(f):
    raw=subprocess.run(["ffmpeg","-v","error","-i",f,"-f","s16le","-ac","1","-ar","44100","-"],capture_output=True).stdout; return len(raw)/2/44100
# block: [(frame, cue words or None for the first shot, [labels...])]
X={
1:[("F01",None,["5,070 deaths at work (2024)"]),("F401","went to",["just a normal workday"]),("F201","But the",["not spread evenly"]),("F101","In some",["up to 30x higher"])],
2:[("F02",None,["ranked by death rate"]),("F102","from the",["source: U.S. BLS"]),("F402","For the",["average job: 3.3 per 100,000"]),("F202","Keep that",["danger meter"])],
3:[("F03",None,["#10 grounds maintenance"]),("F203","That's landscapers",["landscapers"]),("F103","climb",[]),("F403","Their rate",["~21 deaths per 100,000"])],
4:[("F204",None,["not the mower"]),("F404","It's the",["it's the tree"]),("F04","Climbers",["swinging branch"]),("F104","chainsaw",["chainsaw up high"])],
5:[("F05",None,["#9 truck driver"]),("F205","The rate",["~26 deaths per 100,000"]),("F105","But this",[]),("F206","no other",["one big difference"])],
6:[("F06",None,["most deaths of any job"]),("F406","Almost",["~800 drivers died (2024)"]),("F106","Long hours",["long hours"]),("F405","tired",["tired drivers"])],
7:[("F207",None,["#8 underground miner"]),("F07","They drive",["huge machines"]),("F107","cut coal",["cutting drum"]),("F407","deep below",[])],
8:[("F08",None,["~36 deaths per 100,000"]),("F408","Underground",["tight tunnels"]),("F108","falling rock",[]),("F208","very few",["few ways out"])],
9:[("F09",None,["#7 construction helper"]),("F109","They carry",[]),("F209","clean up",["no railing"]),("F409","Often",["often a first job"])],
10:[("F10",None,["first day on site"]),("F110","New workers",[]),("F210","Their rate",["~36 deaths per 100,000"]),("F410","more than",["10x the average"])],
11:[("F11",None,["#6 pilot"]),("F211","This one",["small plane"]),("F111","flying on",["airliners: very safe"]),("F411","safest",["bush plane"])],
12:[("F12",None,["small planes"]),("F112","crop dusters",["crop duster"]),("F212","often in",["bad weather"]),("F412","The rate",["~37 deaths per 100,000"])],
13:[("F13",None,["#5 garbage collector"]),("F113","You see",[]),("F213","and probably",["before sunrise"]),("F413","dangerous",["riding on the back"])],
14:[("F14",None,["~37 deaths per 100,000"]),("F214","early in",["in the dark"]),("F414","passing traffic",["passing traffic"]),("F114","their own",["their own heavy truck"])],
15:[("F15",None,["#4 ironworker"]),("F115","steel skeletons",["steel beams"]),("F215","bridges",["bridges & skyscrapers"]),("F415","walking",["high above the ground"])],
16:[("F16",None,["~38 deaths per 100,000"]),("F116","They wear",["always clipped in"]),("F416","one slip",["one slip..."]),("F216","one loose",["one loose beam"])],
17:[("F17",None,["#3 roofer"]),("F417","Every house",["every house needs one"]),("F217","someone has",["the way up"]),("F117","on a slope",["steep slope"])],
18:[("F18",None,["~49 deaths per 100,000"]),("F418","That's about",["15x the average job"]),("F118","And the main",["roof anchor"]),("F218","Falls",["#1 killer: falls"])],
19:[("F19",None,["#2 commercial fisherman"]),("F119","Out at",["storms at sea"]),("F219","heavy gear",["heavy, wet gear"]),("F419","a deck",["a deck that never stops"])],
20:[("F20",None,["~89 deaths per 100,000"]),("F120","When something",["survival suit"]),("F420","a boat",["boats can sink fast"]),("F220","the nearest",["rescue: hours away"])],
21:[("F21",None,["#1 logger"]),("F221","They cut",["chainsaw"]),("F121","in steep",["steep forests"]),("F421","far from",["far from any road"])],
22:[("F22",None,["~110 deaths per 100,000"]),("F222","That's more",["30x the average job"]),("F422","And most",["most deaths: falling trees"]),("F122","a log",["logs roll the wrong way"])],
23:[("F23",None,["think about that"]),("F423","A job",[]),("F123","the most",["the cut"]),("F223","the very",["the job is the danger"])],
24:[("F24",None,["what they share"]),("F124","Heights",["heights · water"]),("F224","Heavy machines",["machines · falling trees"]),("F424","And very",["far from help"])],
25:[("F125",None,["not on the list"]),("F25","Firefighters",["firefighters: ~4 per 100,000","police: ~8.5 per 100,000"]),("F225","The deadliest",["jobs we barely notice"]),("F425","barely",[])],
26:[("F26",None,["safety gear saves lives"]),("F126","But next",["clipped in"]),("F426","or up",["riskier than yours"]),("F226","remember",["home safe"])],
27:[("F27",None,["which would you never do?"]),("F127","Tell us",["tell us below"]),("F227","subscribe",["subscribe!"]),("F427","Next time",["next: jobs that may disappear"])],
}
norm=lambda s: re.sub(r"[^a-z0-9']","",s.lower())
blocks=[]; LAB={}
for b in range(1,28):
    words=W[b]; total_src=adur(f"voice/{b:02d}.mp3"); total=total_src/TEMPO+GAP
    starts=[0.0]; pos=0
    for fr,cue,_ in X[b][1:]:
        c=[norm(x) for x in cue.split()]; hit=None
        for i in range(pos,len(words)):
            if all(i+j<len(words) and norm(words[i+j][0]).startswith(c[j][:5]) for j in range(len(c))): hit=i; break
        if hit is None:
            for i in range(pos,len(words)):
                if norm(words[i][0]).startswith(c[0][:4]): hit=i; break
        if hit is None: raise SystemExit(f"block {b}: cue '{cue}' not found in {' '.join(w for w,_ in words)}")
        pos=hit+1; starts.append(max(0.0,words[hit][1]/TEMPO-0.12))
    # minimum shot length 1.0 s
    for i in range(1,len(starts)):
        starts[i]=max(starts[i],starts[i-1]+1.0)
    ends=starts[1:]+[total]
    assert ends[-1]-starts[-1]>=0.8,(b,starts,total)
    blocks.append([["still",fr,round((e-s)/total,5)] for (fr,_,_),s,e in zip(X[b],starts,ends)])
    for fr,_,labs in X[b]: LAB[fr]=labs
P['blocks']=blocks
json.dump(P,open('plan_wish.json','w'),indent=1)
json.dump(LAB,open('labels_sync.json','w'),indent=1)
print('ok',sum(len(b) for b in blocks),'shots')
