#!/usr/bin/env python3
"""Выбор лучшего дубля по сплошной проверке ударений (stress_audit.py) среди нескольких прогонов.

Оценка дубля (меньше — лучше): сумма запасов ударных ошибок + 1 за каждую ударную ошибку + 3 за каждое расхождение
текста («text») + 1 за «asr_only» с акустикой > 0,3 (слово распознано иначе, и звук не на стороне сценария).
Клон Alexey (Chatterbox) систематически тянет ударение на первый слог; от сида к сиду это меняется сильнее,
чем от настроек (эксперимент «Механик 90-х», 12 нояб: 16 подозрений у одного дубля, 9 у другого при тех же
настройках), поэтому лучший из 5–7 дублей — главный бесплатный способ снизить ошибки.

    python3 qa/pick_best_take.py --project <папка> qa_out/stress_audit.json qa_out/exp_*.json qa_out/ret_*.json
        → печать выбора и <папка>/qa_out/best_takes.json {id: файл}
"""
import sys, os, json, glob

def opt(k, d=None): return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d

proj = os.path.abspath(opt('--project', '.'))
files = [a for a in sys.argv[1:] if a.endswith('.json') and a != opt('--project')]
cand = {}
# забракованные по полной проверке (voiceqa) дубли: {"A5_q.wav": "лишний звук после текста", ...} — не выбирать
rej = json.load(open(os.path.join(proj, 'qa_out', 'take_rejects.json'), encoding='utf-8')) if os.path.exists(os.path.join(proj, 'qa_out', 'take_rejects.json')) else {}
for pat in files:
    for f in glob.glob(os.path.join(proj, pat)):
        for lid, v in json.load(open(f, encoding='utf-8')).items():
            if not os.path.exists(os.path.join(proj, 'vo_takes', v['take'])): continue   # дубль убран (устарел текст)
            if v['take'] in rej: continue
            s = v['suspects']
            st = [x for x in s if x['kind'] == 'stress']
            score = sum(x['margin'] for x in st) + len(st) + 3 * sum(1 for x in s if x['kind'] == 'text') \
                    + sum(1 for x in s if x['kind'] == 'asr_only' and (x.get('delta') or 0) > 0.3)
            cand.setdefault(lid, {})[v['take']] = dict(score=round(score, 2), stress=len(st),
                                                      words=[f"{x['word']}({x['got']}/{x['exp']})" for x in st])
best = {}
for lid, c in cand.items():
    t = min(c, key=lambda k: (c[k]['score'], k))
    best[lid] = t
    print(lid, '→', t, c[t]['score'], c[t]['words'], '| было:', {k: v['score'] for k, v in sorted(c.items())})
json.dump(best, open(os.path.join(proj, 'qa_out', 'best_takes.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
tot0 = sum(min(v['stress'] for k, v in c.items() if k.endswith(('_c.wav', '_e.wav', '_d.wav', '_f.wav'))) if any(k.endswith(('_c.wav', '_e.wav', '_d.wav', '_f.wav')) for k in c) else 0 for c in cand.values())
print('реплик', len(best), '| ударных подозрений у выбранных:', sum(cand[l][t]['stress'] for l, t in best.items()))
