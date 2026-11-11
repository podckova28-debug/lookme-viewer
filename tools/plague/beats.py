"""Turn a list of beats (voice line + the shots that cover it) into a timeline json for build_scene.py.

Each beat lasts as long as its voice line (or a fixed 'hold' for silent beats) plus a short gap, and its
shots split that time evenly (or by 'w' weights). SFX and captions are given relative to their shot.
This keeps cuts tight to the narration: no dead air between lines.

usage: python3 tools/plague/beats.py tools/plague/cold_open_beats.json tools/plague/cold_open.json
"""
import sys, os, json, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src = json.load(open(sys.argv[1]))
GAP, LEAD = src.get('gap', .3), src.get('lead', .15)
MAXS = src.get('max_shot', 99)
DETAIL = [(.42, .45), (.58, .5), (.5, .42), (.38, .55), (.62, .45)]
dur = lambda f: float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', os.path.join(ROOT, f)]))
out = {k: src[k] for k in ('base', 'fade_in') if k in src}; out.update(shots=[], texts=[], vo=[], sfx=list(src.get('sfx_global', [])))
t = src.get('start', .4)
for b in src['beats']:
    if 'vo' in b:
        d = dur(b['vo']); out['vo'].append({'file': b['vo'], 't': round(t + LEAD, 3), **({'gain': b['gain']} if 'gain' in b else {})})
        length = LEAD + d + GAP + b.get('tail', 0)
    else:
        length = b['hold']
    ws = [s.get('w', 1) for s in b['shots']]; acc = t
    for s, w in zip(b['shots'], ws):
        sl = length * w / sum(ws)
        sh = {k: v for k, v in s.items() if k not in ('w', 'sfx', 'text')}
        n = max(1, int(sl / MAXS + .35)) if not s.get('text') else 1        # long shot -> wide + 1-2 detail cuts of the same frame
        for k in range(n):
            part = dict(sh); a0 = acc + sl * k / n; a1 = acc + sl * (k + 1) / n
            if k > 0:
                x, y = DETAIL[(len(out['shots']) + k) % len(DETAIL)]; z = max(1.3, sh['from'][2] + .25)
                part['from'] = [x, y, z]; part['to'] = [x + .01, y, z + .07]
            part['t0'] = round(a0, 3); part['t1'] = round(a1, 3); out['shots'].append(part)
        for e in s.get('sfx', []): out['sfx'].append({**{k: v for k, v in e.items() if k != 'at'}, 't': round(acc + e.get('at', 0), 3)})
        for tx in ([s['text']] if isinstance(s.get('text'), dict) else s.get('text', [])):
            out['texts'].append({**{k: v for k, v in tx.items() if k not in ('at', 'len')}, 't0': round(acc + tx.get('at', .2), 3), 't1': round(acc + tx.get('at', .2) + min(tx.get('len', 99), sl - tx.get('at', .2) - .15), 3)})
        acc += sl
    t += length
out['duration'] = round(t, 3)
out['shots'][-1]['fade_out'] = src.get('fade_out', 1.0)
for e in out['sfx']:
    if e.get('kind') in ('drone', 'wind') and e.get('args', {}).get('d') == 'ALL': e['args']['d'] = out['duration']
json.dump(out, open(sys.argv[2], 'w'), indent=1)
print('duration', out['duration'], 'shots', len(out['shots']))
