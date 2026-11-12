import json,sys
sys.path.insert(0,'.')
from manual_arrow import lab
p=json.load(open('plan.json'))
A=[("F03","brass oil lamp",0.50,0.80,0.20,0.70,63,1),
   ("F15","pipeline",0.66,0.62,0.50,0.80,74,-1),
   ("F21","the station",0.62,0.50,0.42,0.36,74,1),
   ("F13","weather station",0.60,0.50,0.50,0.68,74,1),
   ("F05","post office",0.55,0.40,0.30,0.35,74,-1),
   ("F19","the last plane",0.62,0.45,0.60,0.26,74,1),
   ("F410","the herder",0.45,0.40,0.31,0.66,74,-1),
   ("F420","the station",0.58,0.62,0.40,0.45,74,1),
   ("F113","Gough Island",0.74,0.82,0.635,0.47,63,1),
   ("F10","sheep wagon",0.33,0.10,0.15,0.28,63,-1)]
for f,t,tx,ty,bx,by,s,k in A:
    p['labels'].setdefault(f,[]).append(lab(f,t,tx,ty,bx,by,s,k))
p['labels'].setdefault('F116',[]).append(['helium + oxygen',[0.378,0.82],[0.378,0.82],[0.378,0.82],45])
json.dump(p,open('plan.json','w'),indent=1)
