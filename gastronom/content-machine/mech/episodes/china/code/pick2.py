import json, collections, statistics
VC = {json.loads(l)['id']: json.loads(l) for l in open('work/vc_all.jsonl')}
ST = {json.loads(l)['id']: json.loads(l) for l in open('work/st2_all.jsonl')}
rates = [r['rate'] for r in VC.values() if r['rate']]; med = statistics.median(rates)
def st_bad(i, thr=0.6):
    return [(w['w'], w['exp'], w['got'], w['margin']) for w in ST.get(i, {}).get('words', []) if w['got'] != w['exp'] and w['margin'] >= thr]
def score(r):
    low = [w for w in r['low'] if w[1] < 0.6 and w[0] not in ('–', '—')]
    return r['mean'] * 100 - 10 * len(r['mism']) - 3 * len(low) - 4 * len(st_bad(r['id'])) - 6 * abs(r['rate'] / med - 1)
by = collections.defaultdict(list)
for i, r in VC.items(): by[i.rsplit('_', 1)[0]].append(r)
order = [k for k, _ in json.load(open('work/lines.json'))]
FORCE = {'B6': 'B6_b', 'B6t': 'B6t_b', 'B7': 'B7_b', 'I01': 'I01_a', 'B8': 'B8_b'}  # «Тэнет» — ударение на первый слог; I01_b рвёт фразу; B8_b чище
pick = {}
for k in order:
    rs = sorted(by[k], key=score, reverse=True)
    b = next((r for r in rs if r['id'] == FORCE.get(k)), rs[0]); pick[k] = b['id']
    alt = ' | '.join(f"{r['id']}:{score(r):.0f}({len(st_bad(r['id']))})" for r in rs)
    print(f"{k:5s} → {b['id']:9s} [{alt}]  st2: {st_bad(b['id'], 0.8)}")
json.dump(pick, open('work/pick.json', 'w'), ensure_ascii=False, indent=0)
# слова, где ударение «не там» во ВСЕХ дублях (кандидаты на системную ошибку голоса)
cnt = collections.Counter(); tot = collections.Counter()
for i, r in ST.items():
    for w in r['words']:
        tot[w['w'].lower()] += 1
        if w['got'] != w['exp'] and w['margin'] >= 0.8: cnt[w['w'].lower()] += 1
print('\nСистемно «не тот слог» (из всех вхождений):', [(w, f'{cnt[w]}/{tot[w]}') for w in cnt if cnt[w] == tot[w] and tot[w] >= 2])
