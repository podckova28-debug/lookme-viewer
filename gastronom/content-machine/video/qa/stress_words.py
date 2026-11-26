#!/usr/bin/env python3.13
"""Пословный отчёт об ударениях готовой озвучки: каждое слово из 2+ слогов — какой слог звучит ударным (длительность и
громкость гласных по выравниванию wav2vec2), какой нужен по словарю (textgate/RUAccent) и с каким запасом.
Ошибка — слышно не там; «?» — запас < 0,15 (детектор не уверен, слушать). Детектор шумный: это список на проверку.

    python3.13 qa/stress_words.py <папка проекта> [папка с вавками = vo] [дубль] → печать и <проект>/qa_out/stress_words[_дубль].json
    С дублем читает <папка>/<id>_<дубль>.wav (например vo_takes и c).
"""
import sys, os, json, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import voiceqa as Q

proj = os.path.abspath(sys.argv[1]); vo = os.path.join(proj, sys.argv[2] if len(sys.argv) > 2 else 'vo')
TAKE = sys.argv[3] if len(sys.argv) > 3 else ''
lines = Q.load_lines(os.path.join(proj, 'script.py'))
tg = {r['id']: r for r in json.load(open(os.path.join(proj, 'qa_out', 'textgate.json'), encoding='utf-8'))}
ac = Q.Acoustic(); rep = {}; bad = unsure = total = 0
for lid, text in lines:
    path = os.path.join(vo, f'{lid}_{TAKE}.wav' if TAKE else f'{lid}.wav')
    if not os.path.exists(path) and os.path.exists(path[:-4] + '.mp3'): path = path[:-4] + '.mp3'
    if not os.path.exists(path): continue
    x = Q.load_audio(path); dur = len(x) / Q.SR
    S = Q.script_tokens(text); em = ac.logits(x); fps = em.shape[0] / dur
    wf = Q.word_frames(ac, em, S); rows = []
    for i, s in enumerate(S):
        w = s['w']; nv = sum(1 for c in Q.norm(w) if c in Q.VOW)
        if nv < 2: continue
        exp = Q.expected_stress(w, tg[lid]['stressed'])
        r = Q.stress_of(ac, em, fps, x, wf[i], w, i == len(S) - 1)
        if r is None or exp is None: rows.append(dict(w=w, exp=exp, got=None)); continue
        got, margin, durs = r; total += 1
        flag = 'ОШИБКА' if got != exp else ('?' if margin < 0.15 else '')
        bad += flag == 'ОШИБКА'; unsure += flag == '?'
        rows.append(dict(w=w, exp=exp, got=got, margin=margin, durs=durs, flag=flag))
    rep[lid] = rows
    print(lid, ' '.join(f"{r['w']}[{'?' if r.get('got') is None else r['got']}/{r['exp']}{'!' if r.get('flag') == 'ОШИБКА' else ('?' if r.get('flag') == '?' else '')}]" for r in rows), flush=True)
json.dump(rep, open(os.path.join(proj, 'qa_out', f"stress_words{'_' + TAKE if TAKE else ''}.json"), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'слов {total}, слышно не там {bad}, неуверенно {unsure}')
for lid, rows in rep.items():
    for r in rows:
        if r.get('flag'): print(lid, r['w'], 'слышно на', r['got'] + 1, 'нужно на', r['exp'] + 1, 'запас', r['margin'], 'гласные', r['durs'], r['flag'])
