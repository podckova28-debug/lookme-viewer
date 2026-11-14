import json,sys
sys.path.insert(0,'.')
from manual_arrow import lab
p=json.load(open('plan.json'))
A=[("F03","treatment tank",0.64,0.50,0.52,0.33,74,1),
   ("F09","bolting machine",0.62,0.50,0.44,0.24,74,-1),
   ("F17","steel cables",0.58,0.40,0.33,0.33,74,1),
   ("F21","radar",0.66,0.50,0.45,0.62,74,1),
   ("F19","control panels",0.62,0.50,0.48,0.26,74,-1),
   ("F07","drill pipe",0.64,0.55,0.49,0.50,74,1)]
for f,t,tx,ty,bx,by,s,k in A:
    p['labels'].setdefault(f,[]).append(lab(f,t,tx,ty,bx,by,s,k))
json.dump(p,open('plan.json','w'),indent=1)
