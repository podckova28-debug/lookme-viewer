# Whisper check: python qa.py lines.txt dir -> dir/_qa.tsv (id, score, duration, heard)
import sys, re, difflib, subprocess, numpy as np, soundfile as sf
from faster_whisper import WhisperModel
lines, d = sys.argv[1], sys.argv[2]
m = WhisperModel('small', device='cpu', compute_type='int8')
norm = lambda s: re.sub(r'[^a-z ]', '', s.lower().replace('-', ' '))
out = []
for l in open(lines):
    if not l.strip(): continue
    i, r, t = l.strip().split('|', 2)
    try: w, sr = sf.read(f'{d}/{i}.wav')
    except Exception: continue
    a = subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{d}/{i}.wav', '-ar', '16000', '-ac', '1', '-f', 'f32le', '-'], capture_output=True).stdout
    segs, _ = m.transcribe(np.frombuffer(a, np.float32), language='en', beam_size=5)
    h = ' '.join(s.text for s in segs).strip()
    sc = difflib.SequenceMatcher(None, norm(t).split(), norm(h).split()).ratio()
    out.append(f'{i}\t{sc:.2f}\t{len(w)/sr:.1f}\t{h}'); print(out[-1], flush=True)
open(f'{d}/_qa.tsv', 'w').write('id\tscore\tsec\theard\n' + '\n'.join(out) + '\n')
