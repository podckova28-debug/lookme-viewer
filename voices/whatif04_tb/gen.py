# What If #2 plague VO. usage: python gen.py lines.txt outdir [ids...]
import os, sys, re, torch, numpy as np, soundfile as sf
torch.set_num_threads(os.cpu_count() or 4)
from chatterbox.tts import ChatterboxTTS
ROLES = {'NARRATOR': ('refs/kokoro_bm_george.wav', .5, .5, .7), 'LADY': ('refs/role_tb_emma_low.wav', .45, .3, .7)}
lines, out = sys.argv[1], sys.argv[2]; only = set(sys.argv[3:]); seed = int(os.environ.get('SEED', 0))
m = ChatterboxTTS.from_pretrained(device='cpu'); SR = m.sr; os.makedirs(out, exist_ok=True)
def trim(x, thr=.008):
    i = np.where(np.abs(x) > thr)[0]
    return x if len(i) == 0 else x[max(0, i[0] - int(.03 * SR)):min(len(x), i[-1] + int(.05 * SR))]
def chunks(t, n=180):
    parts, cur = re.split(r'(?<=[.!?:])\s+', t), ''
    res = []
    for p in parts:
        if cur and len(cur) + len(p) + 1 > n: res.append(cur); cur = p
        else: cur = (cur + ' ' + p).strip()
    return res + [cur]
for l in open(lines, encoding='utf-8'):
    if not l.strip(): continue
    i, role, t = l.strip().split('|', 2)
    if only and i not in only: continue
    ref, e, c, temp = ROLES[role]; segs = []
    for ch in chunks(t):
        torch.manual_seed(seed)
        segs += [trim(m.generate(ch, audio_prompt_path=ref, exaggeration=e, cfg_weight=c, temperature=temp).squeeze(0).numpy().astype(np.float32)), np.zeros(int(.3 * SR), np.float32)]
    w = np.concatenate(segs[:-1]); sf.write(f'{out}/{i}.wav', w, SR); print(i, round(len(w) / SR, 1), flush=True)
