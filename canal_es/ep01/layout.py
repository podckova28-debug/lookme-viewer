"""Lay out ep01 narration on a timeline.
usage: python layout.py VO_DIR   (VO_DIR has one wav per line id, e.g. vo_kokoro or vo)
writes timing.json (for the mixer) and timing.js (for the animation pages).
Scene beats are animated against these times, so swapping the voice only needs a re-run."""
import json, re, sys, os
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
VO = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'vo_kokoro')
lines = json.load(open(os.path.join(HERE, 'vo_lines.json'), encoding='utf-8'))

# paragraph starts: first sentence of each "> " paragraph in the script
md = open(os.path.join(HERE, '..', 'ep01_detener_el_tiempo.md'), encoding='utf-8').read()
para_first = set()
for sec in re.split(r'^### ', md, flags=re.M)[1:]:
    sec = sec.split('\n---\n')[0]; num = int(re.match(r'(\d+)\.', sec).group(1)); k = 0
    for l in sec.splitlines()[1:]:
        if l.startswith('> ') and l[2:].strip():
            parts = re.split(r'(?<=[.!?…])\s+(?=[¿¡A-ZÁÉÍÓÚÑ])', l[2:].strip())
            for i, _ in enumerate(parts):
                k += 1
                if i == 0: para_first.add(f's{num:02d}_{k:02d}')
        elif re.match(r'\*\*(VALERIA|TÚ):\*\*', l):
            k += 1; para_first.add(f's{num:02d}_{k:02d}')

GAP_SENT, GAP_PARA = 0.28, 0.65
LEAD = {'s01': 1.6, 's10': 0.9, 's16': 0.8}
TAIL = {'s04': 1.2, 's10': 1.2, 's13': 1.4, 's15': 1.2, 's16': 1.6, 's17': 5.5}
HOLD = {  # extra seconds after a line, for visual gags
    's01_02': .6, 's01_05': .8,
    's03_02': 1.1, 's03_03': .6, 's03_06': .8,
    's04_03': .6, 's04_05': .5, 's04_08': 1.1,
    's05_01': .5, 's05_02': 1.6,
    's06_03': .9, 's06_05': .6, 's06_08': 1.5,
    's07_02': 1.1, 's07_04': .9,
    's08_02': .4, 's08_04': 1.6,
    's09_01': .5, 's09_03': .8, 's09_05': .6,
    's10_02': .9, 's10_04': .6, 's10_06': 1.1,
    's11_05': .6, 's11_06': .4, 's11_07': .9,
    's13_03': .9, 's13_05': .3, 's13_11': 1.3,
    's14_04': .8, 's14_05': 1.0, 's14_06': .8,
    's15_02': .4, 's15_05': .6, 's15_07': .9, 's15_08': .4,
    's16_03': 1.1, 's16_04': .6, 's16_06': 1.3,
    's17_04': 1.5,
}
SHORT_GAP = {f's13_{i:02d}': .15 for i in range(8, 11)}  # "Congelado. Sigue. Congelado. Sigue." back to back
FIXED = {'s02': 3.6}  # title card, no narration

scenes, order = {}, []
for l in lines:
    sid = l['id'][:3]
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
json.dump(out, open(os.path.join(HERE, 'timing.json'), 'w'), indent=1)
open(os.path.join(HERE, 'timing.js'), 'w').write('const TIM = ' + json.dumps(out) + ';\n')
print(f"total {int(t0 // 60)}:{t0 % 60:04.1f}  ({len(lines)} lines, voice: {out['vo']})")
for sid in order: s = out['scenes'][sid]; print(sid, f"{s['start']:7.1f}  dur {s['dur']:5.1f}")
