import os, torch, numpy as np, soundfile as sf
torch.set_num_threads(4)
from chatterbox.tts import ChatterboxTTS
JOBS=[(f"rum_p{i}",f"../drinks/rum/p{i}.txt") for i in range(9)]
m=ChatterboxTTS.from_pretrained(device="cpu"); SR=m.sr
def trim(x,thr=0.008):
    i=np.where(np.abs(x)>thr)[0]; return x if len(i)==0 else x[max(0,i[0]-int(.03*SR)):min(len(x),i[-1]+int(.05*SR))]
for name,txt in JOBS:
    os.makedirs(f"health_out/{name}",exist_ok=True)
    for i,t in enumerate([l.strip() for l in open(txt,encoding='utf-8') if l.strip()]):
        f=f"health_out/{name}/l{i:02d}_s0.wav"
        if os.path.exists(f): continue
        torch.manual_seed(0)
        w=trim(m.generate(t,audio_prompt_path="refs/kokoro_bf_isabella_narr.wav",exaggeration=0.5,cfg_weight=0.5,temperature=0.7).squeeze(0).numpy().astype(np.float32))
        sf.write(f,w,SR); print(name,i,round(len(w)/SR,1),flush=True)
    print("JOB DONE",name,flush=True)
print("ALL DONE",flush=True)
