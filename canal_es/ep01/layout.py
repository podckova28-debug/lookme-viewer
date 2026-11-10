"""Lay out ep01 narration on a timeline.
usage: python layout.py VO_DIR   (VO_DIR has one wav per line id, e.g. vo_kokoro or vo)
writes timing.json (for the mixer) and timing.js (for the animation pages).
Scene beats are animated against these times, so swapping the voice only needs a re-run."""
import json, re, sys, os
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
VO = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'vo_kokoro')
lines = json.load(open(os.path.join(HERE, 'vo_lines.json'), encoding='utf-8'))

# paragraph starts are flagged per line in vo_lines.json ('p': 1): a longer pause before them
para_first = {l['id'] for l in lines if l.get('p')}

GAP_SENT, GAP_PARA = 0.28, 0.65
LEAD = {'s00': 1.2, 's01': 1.0, 's10': 0.9, 's11b': 0.8, 's16': 0.8, 's18': 1.4, 's19': 0.4}
TAIL = {'s00': 1.3, 's04': 1.2, 's10': 1.2, 's11b': 0.8, 's13': 1.4, 's15': 1.2, 's16': 1.6, 's17': 1.2, 's18': 1.0, 's19': 5.5}
HOLD = {  # extra seconds after a line, for visual gags
    's00_01': .3, 's00_03': .5, 's00_04': .4,
    's04_08b': .5, 's06_06b': .3, 's07_04b': .7, 's09_05b': .4, 's10_06b': .6, 's10_07b': .6, 's12_04b': .3, 's13_01b': .3, 's13_02b': .2, 's14_05b': .4, 's17_00': .6,
    's01_02': .6, 's01_05': .8,
    's03_02': 1.1, 's03_03': .6, 's03_06': .8,
    's04_03': .6, 's04_05': .5, 's04_08': .25,
    's05_01': .5, 's05_02': 1.6,
    's06_03': .9, 's06_05': .6, 's06_08': 1.5,
    's07_02': 1.1, 's07_04': .9,
    's08_02': .4, 's08_04': 1.6,
    's09_01': .5, 's09_03': .8, 's09_05': .6,
    's10_02': .9, 's10_04': .6, 's10_06': .15,
    's11_05': .6, 's11_06': .4, 's11_07': .9,
    's13_03': .9, 's13_05': .3, 's13_11': 1.3,
    's14_04': .8, 's14_05': 1.0, 's14_06': .8,
    's15_02': .4, 's15_05': .6, 's15_07': .9, 's15_08': .4,
    's16_03': 1.1, 's16_04': .6, 's16_06': 1.3,
    's07_07': .8, 's07_08': .5, 's07_09': .6, 's11_05b': .5, 's11b_02': .4, 's11b_03': .4, 's11b_04': .3, 's11b_05': .6, 's11b_06': .6,
    's13_13b': .5, 's14_09': .5, 's14_10': .6, 's15_10': .5, 's15_11': .6, 's16_03b': .5, 's16_13': .5, 's16_15': .8, 's16_17': .6, 's16_18': 1.0,
    's17_06': 1.0, 's17_07': 1.2, 's17_08': .6, 's17_09': .8, 's17_10': .8,
    's18_01': .6, 's18_03': .8, 's18_04': .8, 's18_05': .6, 's18_07': .6, 's18_08': .8, 's19_05': 1.5,
}
SHORT_GAP = {f's13_{i:02d}': .15 for i in range(8, 11)}  # "Congelado. Sigue. Congelado. Sigue." back to back
FIXED = {'s02': 3.6}  # title card, no narration

scenes, order = {}, []
for l in lines:
    sid = l['id'].split('_')[0]
    if sid not in scenes: scenes[sid] = []; order.append(sid)
    scenes[sid].append(l)
for sid in FIXED:
    if sid not in scenes: scenes[sid] = []
order = sorted(set(order) | set(FIXED))

out, t0 = {'scenes': {}, 'order': order}, 0.0
for sid in order:
    if sid in FIXED and not scenes[sid]:
        fd = round(FIXED[sid] * 24) / 24; out['scenes'][sid] = {'start': round(t0, 4), 'dur': fd, 'L': {}}; t0 += fd; continue
    t, L = LEAD.get(sid, .7), {}
    for i, l in enumerate(scenes[sid]):
        if i:
            t += SHORT_GAP.get(scenes[sid][i - 1]['id'], GAP_PARA if l['id'] in para_first else GAP_SENT)
        d = sf.info(os.path.join(VO, l['id'] + '.wav')).duration
        L[l['id']] = [round(t, 3), round(d, 3), l['who']]
        t += d + HOLD.get(l['id'], 0)
    dur = round((t + TAIL.get(sid, 1.0)) * 24) / 24  # whole frames, so scene starts match the rendered video
    out['scenes'][sid] = {'start': round(t0, 4), 'dur': dur, 'L': L}
    t0 += dur
out['total'] = round(t0, 3); out['vo'] = os.path.basename(os.path.normpath(VO))
import numpy as np
env = {}
for l in lines:
    if l['who'] == 'narrador': continue
    x, sr = sf.read(os.path.join(VO, l['id'] + '.wav'), dtype='float32'); x = x.mean(1) if x.ndim > 1 else x
    hop = sr // 30; r = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2)) for i in range(0, len(x), hop)])
    env[l['id']] = [round(float(v), 3) for v in np.clip(r / (np.percentile(r, 95) + 1e-6), 0, 1)]
open(os.path.join(HERE, 'vo_env.js'), 'w').write('const VO_ENV = ' + json.dumps(env) + ';\n')
json.dump(out, open(os.path.join(HERE, 'timing.json'), 'w'), indent=1)
open(os.path.join(HERE, 'timing.js'), 'w').write('const TIM = ' + json.dumps(out) + ';\n')
print(f"total {int(t0 // 60)}:{t0 % 60:04.1f}  ({len(lines)} lines, voice: {out['vo']})")
for sid in order: s = out['scenes'][sid]; print(sid, f"{s['start']:7.1f}  dur {s['dur']:5.1f}")
