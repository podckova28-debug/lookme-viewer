"""Lay out ep02 narration on a timeline.
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
LEAD = {'s00': 1.4, 's01': .9, 's03': .8, 's12': .9, 's14': .8, 's16': .9, 's17': 1.4, 's18': .4}
TAIL = {'s00': 1.3, 's03': 1.0, 's04': 1.2, 's05': 1.2, 's06': 1.0, 's11': 1.4, 's13': 1.2, 's14': 1.0, 's15': 1.6, 's16': 1.6, 's17': 1.0, 's18': 5.5}
HOLD = {  # extra seconds after a line, for visual gags
    's00_02': .3, 's00_04': .6,
    's01_02': .6, 's01_04': .4,
    's03_02': .5, 's03_03': .4, 's03_04': .6, 's03_05': .5, 's03_06': .7, 's03_07': .8,
    's04_01': .4, 's04_02': .5, 's04_03': .4, 's04_04': .6, 's04_05': .2, 's04_06': .6, 's04_08': .3,
    's05_03': .6, 's05_04': 1.4, 's05_05': .8, 's05_07': .6, 's05_08': .9,
    's06_01': .8, 's06_02': .6, 's06_03': .6, 's06_04': .9, 's06_05': .6, 's06_07': .8,
    's07_02': .5, 's07_03': .5, 's07_04': .4, 's07_05': .6, 's07_06': .6, 's07_08': .9,
    's08_01': .3, 's08_02': .8, 's08_03': .8, 's08_04': .8, 's08_05': .5, 's08_06': .8,
    's09_02': .5, 's09_03': .6, 's09_04': .5, 's09_05': .4, 's09_06': 1.0,
    's10_02': .5, 's10_03': .6, 's10_04': .5, 's10_05': .3, 's10_06': .4, 's10_07': .6, 's10_08': .5, 's10_10': .6,
    's11_02': .5, 's11_03': .6, 's11_04': .6, 's11_06': .6, 's11_07': .9, 's11_08': .3, 's11_09': .7, 's11_10': .4, 's11_11': .8,
    's12_03': .3, 's12_04': .3, 's12_05': .6, 's12_06': .6, 's12_07': .4, 's12_08': .6, 's12_09': .8, 's12_10': .6, 's12_12': .6, 's12_13': .8,
    's13_01': .4, 's13_02': .3, 's13_03': .4, 's13_04': .5, 's13_05': .4, 's13_06': .5, 's13_07': .2, 's13_08': .2, 's13_09': .7, 's13_10': .5, 's13_11': .5,
    's14_03': .3, 's14_04': .6, 's14_06': .7, 's14_07': .3, 's14_08': .6, 's14_09': .5, 's14_10': .5, 's14_11': .8,
    's15_02': .4, 's15_03': .8, 's15_04': .8, 's15_05': .6, 's15_06': .5, 's15_07': .6, 's15_08': .4, 's15_09': .5, 's15_10': .4, 's15_11': .8, 's15_12': .5, 's15_13': .6,
    's16_02': .4, 's16_03': .6, 's16_04': .5, 's16_05': .7, 's16_06': .8, 's16_07': .6, 's16_08': .2,
    's17_01': .6, 's17_03': .8, 's17_04': .8, 's17_06': .8, 's17_07': .8, 's17_08': .8,
    's18_03': .4, 's18_05': 1.5,
}
SHORT_GAP = {}
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
