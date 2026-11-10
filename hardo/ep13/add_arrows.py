import json,sys
sys.path.insert(0,'.')
from manual_arrow import lab
p=json.load(open('plan.json'))
p['labels'].setdefault('F09',[]).append(lab("F09","~30 lb helmet",0.56,0.1,0.355,0.12,88,-1))
p['labels'].setdefault('F215',[]).append(lab("F215","a dry habitat",0.70,0.22,0.45,0.36,80,1))
json.dump(p,open('plan.json','w'),indent=1)
