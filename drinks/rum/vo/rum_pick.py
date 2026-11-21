import sys, re, glob, subprocess, difflib, numpy as np
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8")
norm=lambda s: re.sub(r"[^a-z0-9' ]+"," ",s.lower().replace("-"," ")).split()
for l in open(sys.argv[1]):
    if not l.strip(): continue
    p,i,t=l.strip().split('|'); i=int(i)
    ref=t.replace('Teekee','Tiki')
    for f in sorted(glob.glob(f"cb/health_out/rum_p{p}/l{i:02d}_*.wav")):
        a=np.frombuffer(subprocess.run(["ffmpeg","-v","quiet","-i",f,"-ar","16000","-ac","1","-f","f32le","-"],capture_output=True).stdout,np.float32)
        h=" ".join(s.text.strip() for s in m.transcribe(a,language="en",beam_size=5)[0])
        r=difflib.SequenceMatcher(None,norm(ref),norm(h)).ratio()
        print(f"{f.split('/')[-2]}/{f.split('/')[-1]}|{len(a)/16000:.2f}|{r:.2f}|{h}",flush=True)
