import json,genp
S=genp.S; D=genp.D; J=genp.J
FJ={int(l.split()[0]):l.split()[1] for l in open('frame_jobs.txt')}
def req(b,kind,txt):
    who=S[b][0]
    nop = "No people" in txt
    meds=[]
    if not nop:
        meds=genp.refs(b,txt)
        if who and D[who][0] not in meds: meds=[D[who][0]]+meds
    if 'robot' in txt and J['C2'] not in meds: meds=[J['C2']]+meds
    meds.append(FJ[b])
    head="PURE WHITE background, close-up. " if kind==1 else "White background, light partial setting fading to white; a different shot, not a copy. "
    if nop: ch="No humans at all. "
    elif who: ch=f"If shown: {D[who][1]}, drawn once. Everyone has exactly two arms and two hands; others look clearly different from the reference sheets. "
    else: ch="Everyone has exactly two arms and two hands; anyone not named looks clearly different from the reference sheets. "
    p=("Same style as the references (thin clean line, realistic proportions, soft flat colours, small simple faces). Keep the setting and colours of the last reference. "
       +head+ch+"No text, letters, numbers, logos, signs or clocks; nobody resembles a real person. SCENE: "+txt)
    return {"index":kind*100+b,"params":{"model":"gpt_image_2_6","aspect_ratio":"16:9","use_unlim":False,
      "medias":[{"value":v,"role":"image_references"} for v in meds],"prompt":p}}
R=[]
for b in range(1,28):
    for kind,col in ((1,3),(2,4),(4,5)): R.append(req(b,kind,S[b][col]))
for i in range(0,len(R),12): json.dump(R[i:i+12],open(f'_x{i//12}.json','w'),separators=(',',':'))
print(len(R))
