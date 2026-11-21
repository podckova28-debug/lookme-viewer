import numpy as np, soundfile as sf
from kokoro import KPipeline
p=KPipeline(lang_code='b')
for f,t in [("health_out/rum_p8/l05_k.wav","Tiki was born.")]:
    w=np.concatenate([a.numpy() if hasattr(a,'numpy') else a for _,_,a in p(t,voice='bf_isabella',speed=0.95)])
    i=np.where(np.abs(w)>0.008)[0]; w=w[max(0,i[0]-720):i[-1]+1200]
    sf.write(f,w.astype(np.float32),24000); print(f,round(len(w)/24000,2))
