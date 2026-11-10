import json,sys
sys.path.insert(0,'.')
from manual_arrow import lab
p=json.load(open('plan.json'))
p['labels'].setdefault('F09',[]).append(lab("F09","~30 lb helmet",0.56,0.1,0.355,0.12,88,-1))
p['labels'].setdefault('F215',[]).append(lab("F215","a dry habitat",0.70,0.22,0.45,0.36,80,1))
json.dump(p,open('plan.json','w'),indent=1)
p=json.load(open('plan.json'))
p['labels']['F17']+= [["all workers",[0.27,0.86],[0.27,0.86],[0.27,0.86],66],["divers",[0.515,0.86],[0.515,0.86],[0.515,0.86],66]]
json.dump(p,open('plan.json','w'),indent=1)
p=json.load(open('plan.json'))
for l in p['labels']['F17']:
    if l[0]=='about 1 in 600': l[1]=l[2]=l[3]=[0.06,0.2]; l[4]=74
json.dump(p,open('plan.json','w'),indent=1)
p=json.load(open('plan.json'))
json.dump(p,open('plan.json','w'),indent=1)
