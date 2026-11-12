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
ZMAX, KEEP = src.get('zoom_max', 1.12), set(src.get('keep_zoom', []))   # keep_zoom: frames that need a crop (e.g. to hide a stray banner)
DETAIL = [(.46, .48), (.54, .5), (.5, .46), (.45, .52), (.55, .48)]   # gentle: second half of a long shot drifts, it does not crop
dur = lambda f: float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', os.path.join(ROOT, f)]))
out = {k: src[k] for k in ('base', 'fade_in', 'music') if k in src}; out.update(shots=[], texts=[], vo=[], sfx=list(src.get('sfx_global', [])))
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
        if sh['img'] not in KEEP:   # cap camera zoom: frames are composed wide, deep crops cut characters
            sh['from'] = sh['from'][:2] + [min(sh['from'][2], ZMAX)]; sh['to'] = sh['to'][:2] + [min(sh['to'][2], ZMAX + .03)]
        n = 1   # one continuous shot per frame: no detail cuts of the same picture (user: no repeated frames back to back)
        for k in range(n):
            part = dict(sh); a0 = acc + sl * k / n; a1 = acc + sl * (k + 1) / n
            if k > 0:
                x, y = DETAIL[(len(out['shots']) + k) % len(DETAIL)]; z = min(1.12, max(1.06, sh['from'][2] + .06))
                part['from'] = [x, y, z]; part['to'] = [x + .015, y, z + .03]
            part['t0'] = round(a0, 3); part['t1'] = round(a1, 3); out['shots'].append(part)
        for e in s.get('sfx', []): out['sfx'].append({**{k: v for k, v in e.items() if k != 'at'}, 't': round(acc + e.get('at', 0), 3)})
        for tx in ([s['text']] if isinstance(s.get('text'), dict) else s.get('text', [])):
            out['texts'].append({**{k: v for k, v in tx.items() if k not in ('at', 'len')}, 't0': round(acc + tx.get('at', .2), 3), 't1': round(acc + tx.get('at', .2) + min(tx.get('len', 99), sl - tx.get('at', .2) - .15), 3)})
        acc += sl
    t += length
# merge back-to-back shots of the same picture into one continuous slow move
merged = []
for sh in out['shots']:
    if merged and merged[-1]['img'] == sh['img'] and abs(merged[-1]['t1'] - sh['t0']) < 1e-3 and not sh.get('fade_out'):
        merged[-1]['t1'] = sh['t1']; merged[-1]['to'] = sh['to']
    else: merged.append(sh)
for sh in merged:   # long holds get a gentle push proportional to their length, never a crop
    d = sh['t1'] - sh['t0']; z0 = sh['from'][2]
    if d > 6 and abs(sh['to'][2] - z0) < .1 and sh['img'] not in KEEP: sh['to'] = sh['to'][:2] + [min(ZMAX + .03, max(sh['to'][2], z0 + .012 * d))]
out['shots'] = merged
for tx in out['texts']:   # persist: keep the item on screen until its (merged) shot ends - used by scheme blocks
    if tx.pop('persist', False):
        sh = next((m for m in merged if m['t0'] - 1e-3 <= tx['t0'] < m['t1']), None)
        if sh: tx['t1'] = round(sh['t1'] - .1, 3)
out['duration'] = round(t, 3)
out['shots'][-1]['fade_out'] = src.get('fade_out', 1.0)
for e in out['sfx']:
    if e.get('kind') in ('drone', 'wind') and e.get('args', {}).get('d') == 'ALL': e['args']['d'] = out['duration']
json.dump(out, open(sys.argv[2], 'w'), indent=1)
print('duration', out['duration'], 'shots', len(out['shots']))
