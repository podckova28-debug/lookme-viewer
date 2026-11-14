import json,sys
J=json.load(open('shots.json')); D=J['D']; S={int(k):v for k,v in J['S'].items()}
STY="49f55c6b-4f18-438d-a011-7ffb378e91e0"
K1=['wastewater','ironworker','drill operator','roof bolter','locomotive engineer']; K2=['ship captain','power line worker','elevator mechanic','reactor operator','air traffic controller']
def refs(b,txt):
    who=S[b][0]; r=[]
    if who: r.append(D[who][0])
    if any(k in txt for k in K1) and J['C1'] not in r: r.append(J['C1'])
    if any(k in txt for k in K2) and J['C2'] not in r: r.append(J['C2'])
    return r
def ch(b,nop=False):
    if nop: return "No people."
    who=S[b][0]
    return (f"If shown: {D[who][1]}, drawn once. " if who else "")+"Every person has exactly two arms and two hands."
def R(i,meds,p): return {"index":i,"params":{"model":"gpt_image_2_6","aspect_ratio":"16:9","use_unlim":False,"medias":[{"value":v,"role":"image_references"} for v in meds],"prompt":p}}
END=" No text, numbers, logos, signs or clocks. Nobody resembles a real person."
def wide(b):
    who,setting,w,*_=S[b]
    p=f"Exactly the reference style: thin clean line, realistic proportions, soft flat colours, small simple faces. Mostly white; light setting fading to white: {setting}. {ch(b)}{END} SCENE: {w} Leave white space at one side."
    return R(b,refs(b,w)+[STY],p)
FJ={}
try: FJ={int(l.split()[0]):l.split()[1] for l in open('frame_jobs.txt') if l.strip()}
except: pass
def extra(b,kind,txt):
    nop="No people" in txt
    meds=([] if nop else refs(b,txt))+[FJ[b]]
    head="Close-up on PURE WHITE." if kind==1 else "Different shot, not a copy; light setting fading to white."
    p=f"Same style as the references; keep the setting and colours of the last one. {head} {ch(b,nop)}{END} SCENE: {txt}"
    return R(kind*100+b,meds,p)
if sys.argv[1]=='w':
    W=[wide(b) for b in range(1,28)]
    for i in range(3): json.dump(W[i*12:(i+1)*12],open(f'_w{i}.json','w'),separators=(',',':'))
else:
    X=[extra(b,k,S[b][c]) for b in range(1,28) for k,c in ((1,3),(2,4),(4,5))]
    for i in range(0,len(X),12): json.dump(X[i:i+12],open(f'_x{i//12}.json','w'),separators=(',',':'))
    print(len(X))
