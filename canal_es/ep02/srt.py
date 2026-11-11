"""Writes out/subtitulos_es.srt from timing.json + vo_lines.json (narration and dialogue)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); T = json.load(open(os.path.join(HERE, 'timing.json')))
L = {l['id']: l for l in json.load(open(os.path.join(HERE, 'vo_lines.json'), encoding='utf-8'))}
NAMES = {'valeria': 'RENATA', 'tu': 'TÚ', 'mama': 'MAMÁ', 'profe': 'PROFE', 'nacho': 'NACHO', 'chicos': 'TODOS'}
def ts(x): h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60; return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"
ev = []
for sid in T['order']:
    for lid, (t, d, who) in T['scenes'][sid]['L'].items():
        a = T['scenes'][sid]['start'] + t; tx = L[lid]['text']
        ev.append((a, a + d + .2, (f"{NAMES[who]}: " if who in NAMES else '') + tx))
ev.sort(); out = []
for i, (a, b, tx) in enumerate(ev):
    if i + 1 < len(ev): b = min(b, ev[i + 1][0] - .02)
    out.append(f"{i + 1}\n{ts(a)} --> {ts(b)}\n{tx}\n")
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True); open(os.path.join(HERE, 'out', 'subtitulos_es.srt'), 'w', encoding='utf-8').write('\n'.join(out)); print(len(out), 'cues')
