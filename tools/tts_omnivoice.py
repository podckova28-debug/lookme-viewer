import json, time, torch, soundfile as sf, os
from omnivoice import OmniVoice
torch.set_num_threads(4)
lines = json.load(open('lines.json'))
ref_text = open('ref_text.txt').read().strip()
model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="cpu", dtype=torch.float32)
prompt = model.create_voice_clone_prompt(ref_audio="ref.wav", ref_text=ref_text)
os.makedirs('out', exist_ok=True)
for k, text in lines.items():
    t0 = time.time()
    a = model.generate(text=text, language="English", voice_clone_prompt=prompt, num_step=32)
    sf.write(f'out/vo_{k}.wav', a[0], 24000)
    print(k, round(len(a[0]) / 24000, 2), 's audio, gen', round(time.time() - t0, 1), 's', flush=True)
print('DONE', flush=True)
