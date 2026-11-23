import json,sys
sys.path.insert(0,'.')
from relabel import find, box
from PIL import Image
p=json.load(open('plan_wish.json')); LAB=json.load(open('labels_sync.json'))
BIG={'subscribe!':108}
L={}
for fr,labs in LAB.items():
    w,h=Image.open(f"frames/{fr}.png").size; occ=[]
    for k,text in enumerate(labs):
        sz=BIG.get(text,88); wy=.1 if k==0 else .3
        r=find(fr,text,.45,wy,[sz,int(sz*.85),int(sz*.72),int(sz*.62)],occ)
        if not r: print("MISS",fr,text); continue
        L.setdefault(fr,[]).append(r); occ.append(box(text,r[1][0],r[1][1],r[4],w,h))
        if r[4]<sz*.7: print("small",fr,text,r[4])
p['labels']=L
json.dump(p,open('plan.json','w'),indent=1)
