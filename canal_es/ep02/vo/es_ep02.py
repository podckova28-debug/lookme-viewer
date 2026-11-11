import os, json, time, torch, numpy as np, soundfile as sf
torch.set_num_threads(4)
from cbload import load_latam
m=load_latam(); SR=m.sr
OUT="/home/user/lookme-viewer/canal_es/ep02/vo"; os.makedirs(OUT,exist_ok=True)
REF={"narrador":"refs/kokoro_em_alex.wav","valeria":"refs/kokoro_af_heart.wav","mama":"refs/kokoro_ef_dora.wav",
     "tu":"refs/role_tu.wav","nacho":"refs/role_nacho.wav","profe":"refs/role_profe.wav"}
CHORUS=[("1","refs/role_chico1.wav"),("2","refs/role_chico2.wav"),("3","refs/kokoro_af_sky.wav")]
WARM={"s15_03","s15_04","s15_05","s15_12","s15_13","s16_07","s16_08"}
DRY={"s05_04","s06_02","s06_03"}
def params(lid,who):
    e={"narrador":0.45,"valeria":0.55,"mama":0.4,"tu":0.35,"nacho":0.7,"profe":0.3,"chicos":0.8}[who]
    if lid in WARM: e=0.35
    if lid.startswith("s17"): e=0.6
    if lid in DRY: e=0.3
    if lid=="s14_04": e=0.4
    if lid=="s11_09": e=0.25
    return e,(0.3 if who=="profe" else 0.4)
def trim(x,thr=0.008):
    i=np.where(np.abs(x)>thr)[0]; return x if len(i)==0 else x[max(0,i[0]-int(.03*SR)):min(len(x),i[-1]+int(.05*SR))]
def gen(t,ref,e,c):
    t=t.lstrip("…").strip()
    for k in range(3):
        torch.manual_seed(1000+k)
        w=trim(m.generate(t,language_id="es",exaggeration=e,cfg_weight=c,temperature=0.7,audio_prompt_path=ref).squeeze(0).numpy().astype(np.float32))
        if 0.3 < len(w)/SR < 0.12*len(t)+2.0: return w
    return w
T0=time.time()
for L in json.load(open("es_ep02.json",encoding="utf-8")):
    lid,who,txt=L["id"],L["who"],L["text"]
    e,c=params(lid,who)
    jobs=[(f"{lid}_{s}",r) for s,r in CHORUS] if who=="chicos" else [(lid,REF[who])]
    for fid,ref in jobs:
        if os.path.exists(f"{OUT}/{fid}.wav"): continue
        w=gen(txt,ref,e,c); sf.write(f"{OUT}/{fid}.wav",w,SR); print(fid,who,round(len(w)/SR,1),int(time.time()-T0),flush=True)
print("FULL DONE",flush=True)
