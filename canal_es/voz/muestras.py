import warnings, sys; warnings.filterwarnings('ignore')
import numpy as np, soundfile as sf
from kokoro import KPipeline
p = KPipeline(lang_code='e', repo_id='hexgrad/Kokoro-82M')
text = ("Imagina que mañana despiertas y descubres que puedes detener el tiempo. "
        "Aplaudes una vez... y todo el mundo se congela. Los pájaros, los coches, "
        "tu profesor de matemáticas a mitad de un bostezo. Suena genial, ¿verdad? "
        "Pues espera. Porque en diez minutos vas a descubrir el primer problema.")
for v in ['em_alex', 'em_santa', 'ef_dora']:
    chunks = [a.numpy() if hasattr(a,'numpy') else a for _,_,a in p(text, voice=v, speed=1.0)]
    gap = np.zeros(int(24000*0.25), dtype=np.float32)
    out = np.concatenate(sum([[c, gap] for c in chunks], []))
    sf.write(f'muestra_{v}.wav', out, 24000); print(v, round(len(out)/24000,1), 's')
