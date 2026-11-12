import os, json, time, torch, numpy as np, soundfile as sf
torch.set_num_threads(4)
from cbload import load_latam
m=load_latam(); SR=m.sr
OUT="/home/user/lookme-viewer/canal_es/ep03/vo"; os.makedirs(OUT,exist_ok=True)
R="refs/"
REF={"narrador":R+"kokoro_em_alex.wav","valeria":R+"kokoro_af_heart.wav","mama":R+"kokoro_ef_dora.wav",
     "tu":R+"role_tu.wav","nacho":R+"role_nacho.wav","profe":R+"role_profe.wav",
     "croqueta":R+"role_croqueta.wav","perro1":R+"role_perro1.wav","perro2":R+"role_perro2.wav","firulais":R+"role_firulais.wav",
     "bigotes":R+"role_bigotes.wav","canela":R+"role_canela.wav","mosquito":R+"role_mosquito.wav","pepe":R+"role_pepe.wav"}
CHORUS={"perros":[("1",R+"es_am_michael.wav"),("2",R+"kokoro_am_adam.wav"),("3",R+"es_af_sarah.wav")],
        "palomas":[("1",R+"role_paloma1.wav"),("2",R+"role_paloma2.wav"),("3",R+"role_paloma3.wav")]}
# role: (exaggeration, cfg)
P={"narrador":(0.45,0.4),"valeria":(0.55,0.4),"mama":(0.4,0.4),"tu":(0.35,0.4),"nacho":(0.7,0.4),"profe":(0.3,0.3),
   "croqueta":(0.3,0.25),"perro1":(0.9,0.5),"perro2":(0.9,0.5),"perros":(0.8,0.4),"firulais":(0.6,0.35),"bigotes":(0.7,0.5),
   "canela":(0.85,0.5),"palomas":(0.6,0.4),"mosquito":(0.3,0.25),"pepe":(0.35,0.3)}
WARM={"s13_01","s13_02","s13_03","s15_01","s15_02","s15_03"}
def params(lid,who):
    e,c=P[who]
    if lid in WARM: e=0.35
    if lid.startswith("s16"): e=0.6
    if lid=="s15_09": e,c=0.3,0.3
    if lid in ("s14_06","s14_07"): e=0.4
    if lid=="s08_04": e,c=0.3,0.25
    if lid=="s09_04": e,c=0.8,0.5
    if lid=="s08_07": e=0.3
    return e,c
def trim(x,thr=0.008):
    i=np.where(np.abs(x)>thr)[0]; return x if len(i)==0 else x[max(0,i[0]-int(.03*SR)):min(len(x),i[-1]+int(.05*SR))]
def gen(t,ref,e,c,base=1000):
    t=t.lstrip("…").replace("¿…","¿").strip()
    for k in range(3):
        torch.manual_seed(base+k)
        w=trim(m.generate(t,language_id="es",exaggeration=e,cfg_weight=c,temperature=0.7,audio_prompt_path=ref).squeeze(0).numpy().astype(np.float32))
        if 0.3 < len(w)/SR < 0.12*len(t)+2.0: return w
    return w
if __name__=="__main__" or True:
    T0=time.time()
    for ln in open("es_ep03_lines.txt",encoding="utf-8"):
        lid,who,txt=ln.rstrip("\n").split("|",2)
        e,c=params(lid,who)
        jobs=[(f"{lid}_{s}",r) for s,r in CHORUS[who]] if who in CHORUS else [(lid,REF[who])]
        for fid,ref in jobs:
            if os.path.exists(f"{OUT}/{fid}.wav"): continue
            w=gen(txt,ref,e,c); sf.write(f"{OUT}/{fid}.wav",w,SR); print(fid,who,round(len(w)/SR,1),int(time.time()-T0),flush=True)
    print("FULL DONE",flush=True)
