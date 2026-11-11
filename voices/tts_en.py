# Commercial-safe English TTS: Chatterbox (MIT) cloning a Kokoro-82M (Apache-2.0) synthetic reference.
# Usage: python tts_en.py lines.txt out_dir refs/kokoro_bm_george.wav [exaggeration] [cfg_weight]
# lines.txt: one line per utterance -> out_dir/l000.wav, l001.wav ... (24 kHz mono, silence trimmed)
import os, sys, torch, numpy as np, soundfile as sf
torch.set_num_threads(os.cpu_count() or 4)
from chatterbox.tts import ChatterboxTTS
txt, out, ref = sys.argv[1:4]; e = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5; c = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
m = ChatterboxTTS.from_pretrained(device="cpu"); SR = m.sr; os.makedirs(out, exist_ok=True)
def trim(x, thr=0.008):
    i = np.where(np.abs(x) > thr)[0]
    return x if len(i) == 0 else x[max(0, i[0]-int(.03*SR)):min(len(x), i[-1]+int(.05*SR))]
for n, t in enumerate(l.strip() for l in open(txt, encoding="utf-8") if l.strip()):
    torch.manual_seed(0)
    w = trim(m.generate(t, audio_prompt_path=ref, exaggeration=e, cfg_weight=c, temperature=0.7).squeeze(0).numpy().astype(np.float32))
    sf.write(f"{out}/l{n:03d}.wav", w, SR); print(n, round(len(w)/SR, 1), flush=True)
