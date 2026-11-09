#!/usr/bin/env python3
"""Free narrator voice: clone Grady with OmniVoice (k2-fsa/OmniVoice, CPU) and voice every block.
Usage (inside a venv with `pip install omnivoice soundfile`):
  tts_omnivoice.py texts.json out_dir speed
texts.json: {"01": "block text", ...}. Reference: ref_grady.wav (24 kHz mono, a paid Grady block) + ref_grady.txt (its exact text),
both in the working directory. speed 0.85 gives about the pace of the paid voice after its 1.1x tempo, so set plan "tempo": 1.0.
A 0.12 s lead-in of silence is added so the first word is never clipped. ~65-85 s per block on CPU.
Check the result with faster-whisper (word-level transcript) before the build."""
import sys, json, time, torch, soundfile as sf, numpy as np
from omnivoice import OmniVoice
texts=json.load(open(sys.argv[1])); out=sys.argv[2]; speed=float(sys.argv[3])
m=OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="cpu", dtype=torch.float32)
p=m.create_voice_clone_prompt(ref_audio="ref_grady.wav", ref_text=open("ref_grady.txt").read())
for k,t in texts.items():
    t0=time.time()
    a=m.generate(text=t, language="English", voice_clone_prompt=p, num_step=16, speed=speed)
    w=np.concatenate([np.zeros(int(0.12*24000)),np.asarray(a[0]).squeeze()])
    sf.write(f"{out}/{k}.wav",w,24000)
    print(k,round(time.time()-t0,1),round(len(w)/24000,2),flush=True)
