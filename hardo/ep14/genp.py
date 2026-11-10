import json,sys
J=json.load(open('shots.json')); D=J['D']; S={int(k):v for k,v in J['S'].items()}
STY="49f55c6b-4f18-438d-a011-7ffb378e91e0"
# fix descriptions to match sheets
D["KU"][1]=D["KU"][1].replace("brown wool overcoat","long brown overcoat, dark waistcoat and tie")
D["CB"][1]=D["CB"][1].replace("soot-blackened face and clothes","soot-smudged face, dark waistcoat over a dirty shirt, short trousers, boots")
D["PF"][1]=D["PF"][1].replace("lidded bucket","grey metal bucket with a lid")
MENTIONS={2:["C1","C2"],27:["C1","C2"],26:["C1"],25:[],1:["C1","C2"]}
HIST="Historical scenes are light, airy and pale, never dark or gloomy; night scenes are pale blue-grey and fade to white. Children are shown tastefully, never hurt on screen."
def refs(b):
    who=S[b][0]
    if who: return [D[who][0]]
    m=MENTIONS.get(b,[]); return [J[x] for x in m]
def chars(b):
    who=S[b][0]
    if who: return f"Characters from the reference sheet, if shown: {D[who][1]}. Each drawn at most once, each with exactly two arms and two hands. Anyone else looks clearly different from all reference sheet characters. "
    return "Each person, if any, drawn once with exactly two arms and two hands. Anyone not named looks clearly different from the reference sheet characters. "
def wide(b):
    who,setting,w,*_=S[b]
    p=("Illustration in EXACTLY the style of the references: thin clean line, realistic proportions, soft flat colour fills, small simple faces, no thick cartoon outline. "
       f"White background with a light partial setting drawn in the same thin line that fades into white at the edges: {setting}. "+chars(b)+HIST+
       " No text, no letters, no numbers, no logos, no signs, no flags, no clocks. Nobody resembles a real person. "
       f"SCENE: {w} Leave some empty white space at one side for a caption.")
    return {"index":b,"params":{"model":"gpt_image_2_6","aspect_ratio":"16:9","use_unlim":False,
        "medias":[{"value":v,"role":"image_references"} for v in refs(b)+[STY]],"prompt":p}}
if __name__=="__main__":
    W=[wide(b) for b in range(1,28)]
    json.dump(W[:14],open('_w0.json','w'));json.dump(W[14:],open('_w1.json','w'))
    print(W[2]['params']['prompt'])
