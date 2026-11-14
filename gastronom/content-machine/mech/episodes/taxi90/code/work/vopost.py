#!/usr/bin/env python3.13
"""Выбранные дубли → vo/<id>.wav с паузами по пунктуации сценария (одним шагом вместо pauses3 → wordgaps → gapfix).

    python3.13 work/vopost.py qa_out/voice.json [id ...]

Границы слов — выравнивание wav2vec2 по буквам (qa/voiceqa.py). На каждой границе — самая длинная тишина
(< пик−35 дБ) между началом последней буквы слова и началом следующего; её длина приводится к цели:
точка/«!» 0,29 с, «?» 0,33, двоеточие 0,21, запятая 0,12 (удлиняется, только если меньше 0,07), без знака > 0,08 → 0,05.
Края: 30 мс до первого звука и 60 мс после последнего. Склейки с плавным переходом 12 мс (render из pauses3).
"""
import sys, os, json, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, '..', 'qa')); sys.path.insert(0, HERE)
import voiceqa as Q
import pauses3 as P3

P3.TARGET.update({'.': 0.29, '!': 0.29, '?': 0.33, ':': 0.21, ',': 0.12, '': 0.05})


def boundaries(ac, path, text):
    x = Q.load_audio(path); dur = len(x) / Q.SR
    S = Q.script_tokens(text); em = ac.logits(x); fps = em.shape[0] / dur
    wf = Q.word_frames(ac, em, S); out = []
    for i in range(len(S) - 1):
        a, b = wf[i]['fs'], wf[i + 1]['fs']
        if not a or not b or a[-1] is None or b[0] is None: continue
        out.append(dict(after=S[i]['w'], p=S[i]['punct'], t1=a[-1] / fps, t2=b[0] / fps))
    return out


def main():
    rep = json.load(open(sys.argv[1], encoding='utf-8')); only = set(sys.argv[2:])
    lines = dict(Q.load_lines(os.path.join(ROOT, 'script.py')))
    takes = os.path.join(ROOT, 'vo_takes'); os.makedirs(os.path.join(ROOT, 'vo'), exist_ok=True)
    ac = Q.Acoustic()
    for lid, f in rep['picks'].items():
        if only and lid not in only: continue
        src = os.path.join(takes, f)
        b = boundaries(ac, src, lines[lid])
        x = P3.load(src); start, end, ops = P3.plan(x, dict(pauses=b)); y = P3.render(x, start, end, ops)
        with wave.open(os.path.join(ROOT, 'vo', f'{lid}.wav'), 'wb') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(P3.SR)
            w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
        print(lid, f, f'{len(x) / P3.SR:.2f} → {len(y) / P3.SR:.2f} с, правок {len(ops)}', flush=True)


if __name__ == '__main__':
    main()
