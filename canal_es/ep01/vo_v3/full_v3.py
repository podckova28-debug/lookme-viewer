import os, time, torch, numpy as np, soundfile as sf
torch.set_num_threads(4)
from cbload import load_latam
m=load_latam(); SR=m.sr
OUT="/home/user/lookme-viewer/canal_es/ep01/vo_v3"; os.makedirs(OUT,exist_ok=True)
REF={"narrador":"refs/kokoro_em_alex.wav","valeria":"refs/kokoro_af_heart.wav","mama":"refs/kokoro_ef_dora.wav",
     "tu":"refs/role_tu.wav","nacho":"refs/role_nacho.wav","profe":"refs/role_profe.wav"}
CHORUS=[("1","refs/role_chico1.wav"),("2","refs/role_chico2.wav"),("3","refs/kokoro_af_sky.wav")]
WARM={"s11_05b","s11b_06","s11b_07","s13_13b","s16_16","s16_17","s16_14","s16_15"}
def trim(x,thr=0.008):
    i=np.where(np.abs(x)>thr)[0]; return x if len(i)==0 else x[max(0,i[0]-int(.03*SR)):min(len(x),i[-1]+int(.05*SR))]
def params(lid,who):
    e={"narrador":0.45,"valeria":0.55,"mama":0.4,"tu":0.35,"nacho":0.7,"profe":0.3,"chicos":0.8}[who]
    if lid in WARM: e=0.35
    if lid.startswith("s18"): e=0.6
    return e, (0.3 if who=="profe" else 0.4)
def gen(txt,ref,e,c,lid):
    t=txt.lstrip("…").strip()
    best=None
    for k in range(3):
        torch.manual_seed(1000+k)
        w=trim(m.generate(t,language_id="es",exaggeration=e,cfg_weight=c,temperature=0.7,audio_prompt_path=ref).squeeze(0).numpy().astype(np.float32))
        d=len(w)/SR; n=len(t)
        ok = 0.3 < d < 0.12*n+2.0
        if ok: return w,k
        best=w if best is None else best
        print("  retry",lid,round(d,1),"s",flush=True)
    return best,9
T0=time.time()
for ln in open("lines_v3.txt",encoding="utf-8"):
    lid,who,txt=ln.rstrip("\n").split("|",2)
    e,c=params(lid,who)
    jobs=[(f"{lid}_{s}",r) for s,r in CHORUS] if who=="chicos" else [(lid,REF[who])]
    for fid,ref in jobs:
        if os.path.exists(f"{OUT}/{fid}.wav"): continue
        w,k=gen(txt,ref,e,c,fid); sf.write(f"{OUT}/{fid}.wav",w,SR)
        print(fid,who,round(len(w)/SR,1),"s try",k,"t+",int(time.time()-T0),flush=True)
print("FULL DONE",int(time.time()-T0),flush=True)
