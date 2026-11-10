import json,sys
sys.path.insert(0,'.')
from manual_arrow import lab
p=json.load(open('plan.json'))
A=[("F06","a robot arm",0.66,0.40,0.535,0.44,80,1),
   ("F23","an AI translator",0.62,0.48,0.47,0.46,74,-1),
   ("F08","old pipes",0.70,0.55,0.60,0.43,80,1)]
for f,t,tx,ty,bx,by,s,k in A:
    p['labels'].setdefault(f,[]).append(lab(f,t,tx,ty,bx,by,s,k))
json.dump(p,open('plan.json','w'),indent=1)
