#!/usr/bin/env python3
"""Выбор дубля «живее»: среди годных по проверкам — с самой подвижной интонацией.

Жалоба (эп. 28, 23 нояб): «голос какой-то вообще неэмоциональный». Метрика — разброс высоты голоса в полутонах
(prosody.py: std и диапазон p10–p90). Порядок отбора:
  1. voiceqa (qa_out/voice_all.json): без fail и warn;
  2. ударения (qa_out/aud_*.json, оценка как в qa/pick_best_take.py): не хуже лучшего дубля реплики + 0,5;
  3. из оставшихся — максимум живости = std + 0,25 × диапазон.
    python3 pick_lively.py --project <папка> → qa_out/best_takes.json и печать выбора
"""
import sys, os, re, json, glob

def opt(k, d=None): return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
proj = os.path.abspath(opt('--project', '.'))
Q = lambda *p: os.path.join(proj, 'qa_out', *p)

vq = json.load(open(Q('voice_all.json'), encoding='utf-8'))['takes']
ok = {f for lid, tk in vq.items() for f, r in tk.items() if r['fails'] == 0 and r['warns'] == 0}
# voiceqa пропускает служебные слова; здесь пропуск любого слова сценария (даже «в»: «А вот мороз») — брак
import difflib, importlib.util
_s = importlib.util.spec_from_file_location('script', os.path.join(proj, 'script.py')); _m = importlib.util.module_from_spec(_s); _s.loader.exec_module(_m)
LINES = dict(_m.LINES)
norm = lambda t: re.findall(r'[а-яё]+', t.lower().replace('ё', 'е'))
dropped = {}
for lid, tk in vq.items():
    for f, r in tk.items():
        a_, b_ = norm(LINES[lid]), norm(r['heard'])
        miss = [w for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a_, b_).get_opcodes() if op == 'delete' for w in a_[i1:i2]]
        if miss: dropped[f] = miss; ok.discard(f)

stress = {}
for f in glob.glob(Q('aud_*.json')):
    for lid, v in json.load(open(f, encoding='utf-8')).items():
        s = v['suspects']; st = [x for x in s if x['kind'] == 'stress']
        stress[v['take']] = sum(x['margin'] for x in st) + len(st) + 3 * sum(1 for x in s if x['kind'] == 'text') \
                            + sum(1 for x in s if x['kind'] == 'asr_only' and (x.get('delta') or 0) > 0.3)

pros = {}
for ln in open(Q('prosody3.txt'), encoding='utf-8'):
    m = re.match(r'(\S+)\s+([\d.]+)s f0\s+\d+\s+std ([\d.]+) st\s+range\s+([\d.]+) st', ln)
    if m: pros[m[1]] = float(m[3]) + 0.25 * float(m[4])

best, report = {}, []
for lid in sorted(vq):
    takes = sorted(f for f in vq[lid])
    good = [f for f in takes if f in ok and f in stress]
    if not good:
        report.append(f'{lid}: нет годных дублей — переозвучить'); continue
    floor = min(stress[f] for f in good) + 0.5
    near = [f for f in good if stress[f] <= floor]
    pick = max(near, key=lambda f: (pros.get(f, 0), -stress[f]))
    best[lid] = pick
    report.append(f"{lid} → {pick}  живость {pros.get(pick, 0):.2f}  ударения {stress[pick]:.2f} | "
                  + ' '.join(f"{f[-5]}:{pros.get(f, 0):.1f}/{stress.get(f, 99):.1f}{'' if f in ok else '✗'}" for f in takes))
json.dump(best, open(Q('best_takes.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('\n'.join(report)); print('пропущены слова:', dropped)
