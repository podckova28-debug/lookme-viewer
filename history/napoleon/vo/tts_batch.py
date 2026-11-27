import os, sys, torch, numpy as np, soundfile as sf
torch.set_num_threads(4)
from chatterbox.tts import ChatterboxTTS
VO="/home/user/lookme-viewer/history/napoleon/vo"
m=ChatterboxTTS.from_pretrained(device="cpu"); SR=m.sr
def trim(x,thr=0.008):
    i=np.where(np.abs(x)>thr)[0]; return x if len(i)==0 else x[max(0,i[0]-int(.03*SR)):min(len(x),i[-1]+int(.05*SR))]
seed=int(os.environ.get("SEED","0")); only=os.environ.get("ONLY")  # ONLY="c03:4,c05:2"
want=None if not only else {tuple(x.split(':')) for x in only.split(',')}
for k in range(int(os.environ.get("NPARTS","9"))):
    p=f"p{k}"; os.makedirs(f"health_out/nap_{p}",exist_ok=True)
    for i,t in enumerate([l.strip() for l in open(f"{VO}/{p}.txt") if l.strip()]):
        if want and (p,str(i)) not in want: continue
        f=f"health_out/nap_{p}/l{i:02d}_s{seed}.wav"
        if os.path.exists(f): continue
        torch.manual_seed(seed)
        w=trim(m.generate(t,audio_prompt_path="kokoro_am_echo.wav",exaggeration=0.5,cfg_weight=0.5,temperature=0.7).squeeze(0).numpy().astype(np.float32))
        sf.write(f,w,SR); print(p,i,round(len(w)/SR,1),flush=True)
print("ALL DONE",flush=True)
