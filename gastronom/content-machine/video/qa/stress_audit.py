#!/usr/bin/env python3.13
"""Сплошная проверка ударений и произношения в выбранных дублях: каждое слово из 2+ слогов, а не только словарь риска.

Зачем: voiceqa смотрит ударение лишь в рискованных словах (марки, имена, омографы) — «Механик 90-х» (12 нояб) прошёл
её чисто, а пользователь услышал «очень много ошибок». Здесь detector ударения (voiceqa.stress_of) гоняется по всем
словам, плюс собираются все расхождения распознавания (в т. ч. info «asr_only», которые voiceqa не считает ошибкой).
Детектор шумный: результат — ранжированный список подозрений, а не вердикт.

    python3.13 qa/stress_audit.py --project <папка> [--picks qa_out/voice.json] [--takes vo_takes] [--ids A1,B2]
        → <папка>/qa_out/stress_audit.json и печать: реплика, слово, слышно/нужно, запас
"""
import sys, os, json, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import voiceqa as Q

def opt(k, d=None): return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d

proj = os.path.abspath(opt('--project', '.'))
lines = Q.load_lines(os.path.join(proj, 'script.py'))
if '--take' in sys.argv: picks = {k: f"{k}_{opt('--take')}.wav" for k, _ in lines}   # проверить конкретный дубль у всех реплик
else: picks = json.load(open(os.path.join(proj, opt('--picks', 'qa_out/voice.json')), encoding='utf-8'))['picks']
takes = os.path.join(proj, opt('--takes', 'vo_takes'))
tg = {r['id']: r for r in json.load(open(os.path.join(proj, 'qa_out', 'textgate.json'), encoding='utf-8'))}
only = set(opt('--ids', '').split(',')) - {''}
fix = {}
sf = os.path.join(proj, 'stress.json')
if os.path.exists(sf): fix = {k: v for k, v in json.load(open(sf, encoding='utf-8')).items()}

from faster_whisper import WhisperModel
wm = WhisperModel('medium', device='cpu', compute_type='int8', cpu_threads=4, download_root=Q.WHISPER_DIR)
ac = Q.Acoustic()
out = {}
for lid, text in lines:
    if only and lid not in only: continue
    f = picks.get(lid)
    if not f or not os.path.exists(os.path.join(takes, f)): continue
    stressed = tg[lid]['stressed']
    allw = {Q.norm(w) for w in re.findall(r'[\w-]+', text) if sum(1 for c in Q.norm(w) if c in Q.VOW) >= 2}
    r = Q.check_take(wm, ac, os.path.join(takes, f), text, allw, stressed, omo=(), stress=True)
    iss = r['issues'] if isinstance(r, dict) else r
    sus = []
    for i in iss:
        if i['code'] == 'stress':
            m = re.search(r'«(.+?)».*слышно на (\d+).*нужно на (\d+).*запас ([\d.]+)', i['msg'])
            sus.append(dict(kind='stress', word=m.group(1), got=int(m.group(2)), exp=int(m.group(3)), margin=float(m.group(4)), t=i.get('t')))
        elif i['code'] in ('text', 'asr_only', 'extra', 'missing', 'swallow'):
            sus.append(dict(kind=i['code'], msg=i['msg'], t=i.get('t'), delta=i.get('delta')))
    out[lid] = dict(take=f, heard=r.get('heard') if isinstance(r, dict) else None, suspects=sus)
    for s in sus:
        if s['kind'] == 'stress': print(f"{lid}\t{s['word']}\tслышно {s['got']}, нужно {s['exp']}\tзапас {s['margin']}", flush=True)
        else: print(f"{lid}\t{s['kind']}\t{s['msg']}", flush=True)
json.dump(out, open(os.path.join(proj, opt('--out', 'qa_out/stress_audit.json')), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
n = sum(1 for v in out.values() for s in v['suspects'] if s['kind'] == 'stress')
print('реплик', len(out), 'подозрений на ударение', n, 'расхождений распознавания', sum(len(v['suspects']) for v in out.values()) - n)
