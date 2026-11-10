# Free local TTS: OmniVoice voice clone of Harrison. Usage: python3 -I gen.py 1 2 3 ...
# Env: OVLIB (site-packages dir), OVHF (HF_HOME), BUDGET (s, stop starting chapters after), NSTEP (default 16).
import sys, os, re, json, time
sys.path.insert(0, os.environ.get("OVLIB", "/home/user/ov/lib")); os.environ["HF_HOME"] = os.environ.get("OVHF", "/home/user/hf")
import torch, numpy as np, soundfile as sf
from omnivoice import OmniVoice
torch.set_num_threads(os.cpu_count() or 4)
ROOT = "/home/user/hw"
script = json.load(open(f"{ROOT}/script.json"))["chapters"]
model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="cpu", dtype=torch.float32)
pp = f"{ROOT}/ref/harrison_prompt.pt"
if os.path.exists(pp):
    prompt = torch.load(pp, weights_only=False)
else:
    prompt = model.create_voice_clone_prompt(ref_audio=f"{ROOT}/ref/ref.wav", ref_text=open(f"{ROOT}/ref/ref.txt").read().strip())
    torch.save(prompt, pp)
os.makedirs(f"{ROOT}/vo", exist_ok=True)
T_START = time.time(); BUDGET = float(os.environ.get('BUDGET', '760'))
for n in map(int, sys.argv[1:]):
    if time.time() - T_START > BUDGET: print('budget stop', flush=True); break
    out = f"{ROOT}/vo/v{n:02d}.wav"
    if os.path.exists(out): continue
    text = script[n - 1]["text"]
    sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
    merged = []
    for s in sents:
        if merged and len(s) < 14: merged[-1] += " " + s
        else: merged.append(s)
    pieces = [np.zeros(int(24000 * 0.15), dtype=np.float32)]; t0 = time.time()
    for s in merged:
        a = model.generate(text=s, voice_clone_prompt=prompt, num_step=int(os.environ.get('NSTEP', '16')))[0]
        a = np.asarray(a, dtype=np.float32).reshape(-1)
        pieces.append(a); pieces.append(np.zeros(int(24000 * 0.32), dtype=np.float32))
    sf.write(out, np.concatenate(pieces), 24000)
    print(f"v{n:02d} done {time.time()-t0:.0f}s audio {sum(len(p) for p in pieces)/24000:.1f}s", flush=True)
