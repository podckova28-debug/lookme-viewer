"""Выбор дублей: сначала меньше ударных подозрений с запасом > 0,5 (порог надёжности из qa/README), затем текст, затем сумма запасов.
Пишет qa_out/pick2.json {id: [дубли по возрастанию балла]} и собирает vo_cand/ (2 лучших на реплику)."""
import json, os, glob, sys
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(D)
ORDER = ['c', 'v', 'q', 'x', 'y', 'x2', 'y2', 'rc', 'rv', 'rq', 'rx', 'ry', 'dc', 'dv', 'dq', 'dx', 'dy']   # поздние перекрывают ранние
BAN = {'G1_v.wav': '«Бесна» вместо «Весна»', 'Z4_q.wav': '«рацией телефоном», «торт»', 'A1_q.wav': '«таксопак»', 'A1_y.wav': '«Код назад»',
       'A8_q.wav': '«Пассажиры»', 'A3_v.wav': '«ввозят»', 'G2_y.wav': 'проглочено «С»', 'G1_y.wav': 'проглочено «В»'}
cand = {}
for t in ORDER:
    f = f'qa_out/aud_{t}.json'
    if not os.path.exists(f): continue
    for lid, v in json.load(open(f, encoding='utf-8')).items():
        cand.setdefault(lid, {})[v['take']] = v
res = {}
for lid, c in cand.items():
    sc = {}
    for take, v in c.items():
        if take in BAN or not os.path.exists(f'vo_takes/{take}'): continue
        s = v['suspects']; st = [x for x in s if x['kind'] == 'stress']
        strong = [x for x in st if x['margin'] > 0.5]
        sc[take] = (len(strong) * 10 + 3 * sum(1 for x in s if x['kind'] == 'text')
                    + sum(1 for x in s if x['kind'] == 'asr_only' and (x.get('delta') or 0) > 0.3)
                    + sum(x['margin'] for x in st) * 0.5, [f"{x['word']}({x['margin']})" for x in strong])
    res[lid] = sorted(sc, key=lambda k: (sc[k][0], k))
    b = res[lid][0]
    print(lid, '→', b, round(sc[b][0], 2), sc[b][1], '| ', {k: round(sc[k][0], 1) for k in res[lid][:4]})
json.dump(res, open('qa_out/pick2.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
os.makedirs('vo_cand', exist_ok=True)
for f in os.listdir('vo_cand'): os.remove(os.path.join('vo_cand', f))
for lid, l in res.items():
    for f in l[:2]: os.symlink(os.path.abspath(f'vo_takes/{f}'), f'vo_cand/{f}')
print('кандидатов', len(os.listdir('vo_cand')))
