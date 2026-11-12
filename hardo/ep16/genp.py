import json
J=json.load(open('shots.json')); D=J['D']; S={int(k):v for k,v in J['S'].items()}
STY="49f55c6b-4f18-438d-a011-7ffb378e91e0"
KEYS1=['lighthouse keeper','post office worker','fire lookout','sheepherder','truck driver','weather observer']
KEYS2=['saturation diver','submariner','South Pole worker','station doctor','astronaut']
def refs(b,txt):
    who=S[b][0]; r=[]
    if who: r.append(D[who][0])
    if any(k in txt for k in KEYS1) and J['C1'] not in r: r.append(J['C1'])
    if any(k in txt for k in KEYS2) and J['C2'] not in r: r.append(J['C2'])
    return r
def chars(b):
    who=S[b][0]
    if who: return f"Characters from the reference sheet, if shown: {D[who][1]}. Each drawn at most once, each with exactly two arms and two hands. Anyone else looks clearly different from all reference sheet characters. "
    return "Each person, if any, drawn once with exactly two arms and two hands. Anyone not named looks clearly different from the reference sheet characters. "
NEG=" Light, airy, mostly white. No text, no letters, no numbers, no logos, no signs, no flags, no clocks. Nobody resembles a real person; no flags, no national symbols. "
def wide(b):
    who,setting,w,*_=S[b]
    p=("Illustration in EXACTLY the style of the references: thin clean line, realistic proportions, soft flat colour fills, small simple faces, no thick cartoon outline. "
       f"White background with a light partial setting drawn in the same thin line that fades into white at the edges: {setting}. "+chars(b)+NEG+
       f"SCENE: {w} Leave some empty white space at one side for a caption.")
    return {"index":b,"params":{"model":"gpt_image_2_6","aspect_ratio":"16:9","use_unlim":False,
        "medias":[{"value":v,"role":"image_references"} for v in refs(b,w)+[STY]],"prompt":p}}
if __name__=="__main__":
    W=[wide(b) for b in range(1,28)]
    for i in range(3): json.dump(W[i*12:(i+1)*12],open(f'_w{i}.json','w'),separators=(',',':'))
    print(open('_w0.json').read())
