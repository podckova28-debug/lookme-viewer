import json, statistics, collections
R = [json.loads(l) for l in open('work/vc_final.jsonl')]
VOW = set('аеёиоуыэюя')
L = dict(json.load(open('work/lines.json')))
by = collections.defaultdict(list); hitch = []; probs = []
art = {}
for r in R:
    k = r['id'].rsplit('_', 1)[0]
    for p in r['pauses']:
        by[p['p'] or '—'].append(p['sil'])
        if p['p'] == '' and p['sil'] > 0.10: hitch.append((k, p['after'], p['sil']))
    syl = sum(1 for c in L[k].lower() if c in VOW)
    pz = sum(p['sil'] for p in r['pauses'])
    art[k] = syl / max(0.5, r['speech'] - pz)
    if r['mism'] or [w for w in r['low'] if w[1] < 0.6 and w[0] not in '–—']: probs.append((k, r['mism'], [w for w in r['low'] if w[1] < 0.6 and w[0] not in '–—'], r['heard']))
print('Паузы после реплики (тишина, с): знак → медиана [мин–макс], n')
for p, v in sorted(by.items()):
    print(f'  {p!r:5s} {statistics.median(v):.2f} [{min(v):.2f}–{max(v):.2f}] n={len(v)}')
print('Запинки без знака > 0,10 с:', hitch)
med = statistics.median(art.values())
print(f'Темп артикуляции: медиана {med:.2f} слог/с')
fast = {k: round(v / med, 2) for k, v in art.items() if v / med > 1.10}
slow = {k: round(v / med, 2) for k, v in art.items() if v / med < 0.88}
print('  быстрее медианы >10%:', fast); print('  медленнее <−12%:', slow)
tempo = {k: round(max(0.92, (med * 1.06) / art[k]), 3) for k in fast}
json.dump(tempo, open('work/line_tempo.json', 'w'), ensure_ascii=False)
print('LINE_TEMPO =', tempo)
print('Остались расхождения/низкая уверенность:')
for x in probs: print('  ', x[0], x[1], x[2], '|', x[3])
