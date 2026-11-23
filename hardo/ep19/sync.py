# ep18: cut each shot on the word it illustrates (whisper word timestamps), labels on the shot where they are spoken
import json,re
W={int(k):v for k,v in json.load(open('words.json')).items()}
P=json.load(open('plan.json')); TEMPO=P['tempo']; GAP=P['gap']
import subprocess
def adur(f):
    raw=subprocess.run(["ffmpeg","-v","error","-i",f,"-f","s16le","-ac","1","-ar","44100","-"],capture_output=True).stdout; return len(raw)/2/44100
# block: [(frame, cue words or None for the first shot, [labels...])]
X={
1:[("F01",None,["+5.9 million jobs by 2035"]),("F101","But some",["some are shrinking"]),("F201","Fast",["fast"]),("F401","A few",["up to 1 in 3 jobs gone"])],
2:[("F02",None,["10 fastest-shrinking jobs"]),("F102","ranked",["source: U.S. BLS, 2025-2035"]),("F402","Not overnight",["not overnight"]),("F202","But year",["year by year"])],
3:[("F03",None,["#10 sewing machine operator"]),("F103","About a",["~117,000 today"]),("F403","still",[]),("F203","in factories",["fewer seats filled"])],
4:[("F04",None,["-15% by 2035"]),("F104","Most clothing",["made overseas"]),("F204","and machines",["machines sew too"]),("F404","simple seams",[])],
5:[("F05",None,["#9 camera repairer"]),("F105","There are",["tiny parts"]),("F205","fewer than",["fewer than 2,000 left"]),("F405","whole country",[])],
6:[("F06",None,["-15.5%"]),("F106","Most photos",["phones took over"]),("F206","And when",["replace, not repair"]),("F406","replace",[])],
7:[("F07",None,["#8 file clerk"]),("F207","Their job",["rows of records"]),("F107","in order",["everything in order"]),("F407","the right",["the right folder"])],
8:[("F208",None,["paper into computers"]),("F108","A search",["1 second vs 10 minutes"]),("F408","Expected",["-15.8%"])],
9:[("F09",None,["#7 carpet installer"]),("F109","This one",["a surprise"]),("F209","people still",["homes still sell"]),("F409","renovate",["renovations too"])],
10:[("F10",None,["it's the floor"]),("F110","Many",["wood · tile · vinyl"]),("F410","Expected",["-16.4%"])],
11:[("F11",None,["#6 print binding worker"]),("F111","stitch",["glue & stitch"]),("F211","trim",[]),("F411","books",["books · magazines · catalogs"])],
12:[("F112",None,["less is printed"]),("F212","today",["read on screens"]),("F12","and modern",["machines need fewer hands"]),("F412","Expected",["-17.5%"])],
13:[("F13",None,["#5 telemarketer"]),("F113","The person",[]),("F213","who calls",["call centre"]),("F413","dinner",["dinner time call"])],
14:[("F114",None,["unknown caller?"]),("F414","answer",["declined"]),("F214","and many",["robocalls"]),("F14","About one",["1 in 5 jobs gone (-21.4%)"])],
15:[("F15",None,["#4 foundry mold maker"]),("F115","hot liquid",["molten metal"]),("F215","into",[]),("F415","engine",["engine parts"])],
16:[("F116",None,["robots pour"]),("F16","including",["3D-printed molds"]),("F216","directly",[]),("F416","Expected",["-23%"])],
17:[("F17",None,["#3 data entry keyer"]),("F417","from forms",["forms & invoices"]),("F117","into computers",["all day long"])],
18:[("F18",None,["scanners read forms"]),("F118","software",[]),("F218","That's why",["1 in 4 jobs (-25.5%)"]),("F418","About thirty",["~34,000 fewer"])],
19:[("F19",None,["#2 switchboard operator"]),("F119","They answer",[]),("F419","connect",["connecting calls"]),("F219","the right",["the right department"])],
20:[("F20",None,["automated menu"]),("F220","Press one",["1 sales · 2 support"]),("F120","press two",[]),("F420","Switchboard",["switchboard: -26%","phone operators: -27.6%"])],
21:[("F21",None,["#1 word processor & typist"]),("F221","Their whole",["the old typing pool"]),("F121","letters",[]),("F421","for other",["for other people"])],
22:[("F22",None,["everyone types"]),("F122","voice",["voice typing"]),("F422","Expected",["-34.4%"]),("F222","That's one",["1 in 3 jobs"])],
23:[("F23",None,["~40,400 today"]),("F223","to about",["~26,500 in 2035"]),("F423","in twenty",[])],
24:[("F24",None,["what they share"]),("F424","Most of",["one task, again and again"]),("F124","sewing",[]),("F224","And a",["machines do it best"])],
25:[("F125",None,["a slow decline"]),("F25","Tens",["tens of thousands still work"]),("F225","And their",["precision · patience"]),("F425","dealing",["people skills"])],
26:[("F26",None,["don't panic"]),("F426","learn",["learn the next skill"]),("F126","a little",["one step ahead"]),("F226","everyone",["new skill, new job"])],
27:[("F27",None,["which surprised you?"]),("F127","Tell us",["tell us below"]),("F227","subscribe",["subscribe!"]),("F427","Next time",["next: jobs of the future"])],
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
