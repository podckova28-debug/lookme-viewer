# Generate N alternative takes of one chapter (seeds 1000+k): python3 -I gen_takes.py CH N -> vo/takeCH_k.wav
# Then: python3 -I tts_qa.py pick --text "<chapter text>" vo/takeCH_*.wav
import sys, os, re, json, time
sys.path.insert(0, os.environ.get("OVLIB", "/home/user/ov/lib")); os.environ["HF_HOME"] = os.environ.get("OVHF", "/home/user/hf")
import torch, numpy as np, soundfile as sf
from omnivoice import OmniVoice
torch.set_num_threads(os.cpu_count() or 4)
ROOT = "/home/user/hw"; n = int(sys.argv[1]); N = int(sys.argv[2])
model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="cpu", dtype=torch.float32)
prompt = torch.load(f"{ROOT}/ref/harrison_prompt.pt", weights_only=False)
text = json.load(open(f"{ROOT}/script.json"))["chapters"][n-1]["text"]
sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
merged = []
for s in sents:
    if merged and len(s) < 14: merged[-1] += " " + s
    else: merged.append(s)
for k in range(N):
    torch.manual_seed(1000 + k)
    pieces = [np.zeros(int(24000 * 0.15), dtype=np.float32)]
    for s in merged:
        a = np.asarray(model.generate(text=s, voice_clone_prompt=prompt, num_step=16)[0], dtype=np.float32).reshape(-1)
        pieces.append(a); pieces.append(np.zeros(int(24000 * 0.32), dtype=np.float32))
    sf.write(f"{ROOT}/vo/take{n:02d}_{k}.wav", np.concatenate(pieces), 24000)
    print("take", k, "done", flush=True)
