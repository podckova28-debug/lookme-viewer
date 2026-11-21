import json,sys
sys.path.insert(0,'.')
from manual_arrow import lab
p=json.load(open('plan.json'))
A=[("F15","safety line",0.42,0.36,0.21,0.22,74,1),
   ("F16","harness",0.45,0.55,0.31,0.47,74,-1),
   ("F19","heavy net",0.62,0.55,0.47,0.82,74,1),
   ("F11","small bush plane",0.58,0.38,0.5,0.47,74,1),
   ("F13","back step",0.55,0.45,0.33,0.74,74,1),
   ("F17","heavy bundle",0.5,0.32,0.3,0.15,74,-1)]
for f,t,tx,ty,bx,by,s,k in A:
    p['labels'].setdefault(f,[]).append(lab(f,t,tx,ty,bx,by,s,k))
json.dump(p,open('plan.json','w'),indent=1)
