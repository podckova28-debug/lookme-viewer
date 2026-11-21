import sys, torch, numpy as np, soundfile as sf
torch.set_num_threads(4)
from chatterbox.tts import ChatterboxTTS
m=ChatterboxTTS.from_pretrained(device="cpu"); SR=m.sr
def trim(x,thr=0.008):
    i=np.where(np.abs(x)>thr)[0]; return x if len(i)==0 else x[max(0,i[0]-int(.03*SR)):min(len(x),i[-1]+int(.05*SR))]
# part line text ; seeds 1..4 -> lNN_sK.wav
REDO=[l.split('|') for l in open(sys.argv[1]) if l.strip()]
for p,i,t in REDO:
    for s in range(1,5):
        f=f"health_out/rum_p{p}/l{int(i):02d}_s{s}.wav"
        torch.manual_seed(s)
        w=trim(m.generate(t.strip(),audio_prompt_path="refs/kokoro_bf_isabella_narr.wav",exaggeration=0.5,cfg_weight=0.5,temperature=0.7).squeeze(0).numpy().astype(np.float32))
        sf.write(f,w,SR); print(p,i,s,round(len(w)/SR,1),flush=True)
print("REDO DONE",flush=True)
