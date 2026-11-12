"""Lay out ep03 narration on a timeline.
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
LEAD = {'s00': 1.2, 's01': .9, 's03': .9, 's08': .8, 's10': .9, 's12': .8, 's15': 1.0, 's16': 1.4, 's17': .4}
TAIL = {'s00': 1.3, 's03': 1.0, 's04': 1.0, 's05': 1.0, 's06': 1.2, 's07': 1.0, 's08': 1.2, 's09': 1.4, 's10': 1.2, 's11': 1.0, 's13': .8, 's14': 1.4, 's15': 1.8, 's16': 1.0, 's17': 5.5}
HOLD = {  # extra seconds after a line, for visual gags
    's00_02': .3, 's00_03': .3, 's00_04': .4, 's00_06': .9,
    's01_02': .5, 's01_03': .3, 's01_04': .4,
    's03_02': .5, 's03_03': .4, 's03_05': .6, 's03_06': .4, 's03_07': .3, 's03_08': .5, 's03_09': .6,
    's04_01': .3, 's04_02': .3, 's04_03': .2, 's04_04': .3, 's04_05': .7, 's04_06': .6, 's04_07': .6, 's04_09': .5,
    's05_02': .2, 's05_03': .3, 's05_04': .4, 's05_05': .5, 's05_06': .3, 's05_07': .6, 's05_08': .3, 's05_09': .8,
    's06_01': .3, 's06_02': .4, 's06_03': .3, 's06_04': .3, 's06_05': .2, 's06_06': .5, 's06_07': .6, 's06_08': .5, 's06_09': .7, 's06_10': .9,
    's07_01': .3, 's07_02': .6, 's07_03': .6, 's07_04': .8, 's07_05': .4, 's07_06': .5, 's07_07': .7,
    's08_01': .4, 's08_02': .4, 's08_03': .4, 's08_04': .5, 's08_05': 1.0, 's08_06': .3, 's08_07': .8,
    's09_02': .3, 's09_03': .2, 's09_04': .4, 's09_05': .5, 's09_06': .4, 's09_07': .5, 's09_08': .6,
    's10_01': .3, 's10_02': .6, 's10_03': .3, 's10_04': .1, 's10_05': .1, 's10_06': .4, 's10_07': .5, 's10_08': .5, 's10_09': .6,
    's11_02': .3, 's11_03': .6, 's11_04': .6, 's11_05': .4, 's11_06': .7, 's11_07': .4,
    's12_01': .3, 's12_02': .6, 's12_03': .3, 's12_04': .3, 's12_05': .5, 's12_06': .3, 's12_07': .8,
    's13_01': .4, 's13_02': .5, 's13_03': .6, 's13_04': .3, 's13_05': .3, 's13_06': .7,
    's14_01': .3, 's14_02': .3, 's14_03': .4, 's14_04': .6, 's14_05': .6, 's14_06': .4, 's14_07': .5, 's14_08': .6, 's14_09': .3, 's14_10': .6,
    's15_02': .4, 's15_03': .8, 's15_04': .8, 's15_05': 1.0, 's15_06': .7, 's15_07': .5, 's15_08': .6, 's15_09': .5, 's15_10': .8, 's15_11': .9,
    's16_01': .6, 's16_03': .6, 's16_04': .8, 's16_06': .8, 's16_08': .6,
    's17_03': .4, 's17_05': 1.2,
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
open(os.path.join(HERE, 'vo_text.js'), 'w', encoding='utf-8').write('const VO_TEXT = ' + json.dumps({l['id']: l['text'] for l in lines}, ensure_ascii=False) + ';\n')
print(f"total {int(t0 // 60)}:{t0 % 60:04.1f}  ({len(lines)} lines, voice: {out['vo']})")
for sid in order: s = out['scenes'][sid]; print(sid, f"{s['start']:7.1f}  dur {s['dur']:5.1f}")
