import json,sys
sys.path.insert(0,'.')
from manual_arrow import lab
p=json.load(open('plan.json'))
A=[("F13","master sweep",0.60,0.22,0.19,0.09,80,1),
   ("F15","the pit",0.64,0.62,0.47,0.72,80,1),
   ("F105","a leech",0.62,0.62,0.445,0.64,80,1),
   ("F213","a climbing boy",0.66,0.45,0.528,0.425,80,1)]
for f,t,tx,ty,bx,by,s,k in A:
    p['labels'].setdefault(f,[]).append(lab(f,t,tx,ty,bx,by,s,k))
json.dump(p,open('plan.json','w'),indent=1)
