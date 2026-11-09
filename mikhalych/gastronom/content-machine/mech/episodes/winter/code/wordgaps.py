"""Паузы между словами по принудительному выравниванию wav2vec2 (точнее, чем метки whisper):
для каждой границы слов — длина тишины (< пик−35 дБ и чистая тишина < пик−50 дБ) между последней буквой слова и первой буквой следующего.

    python3.13 work/wordgaps.py <id> ... > out.jsonl
"""
import sys, json, re, torch, numpy as np
sys.path.insert(0, 'work')
import stress2 as S
THR = 35
for lid in sys.argv[1:]:
    text = S.LINES[lid]; x = S.load(f'vo/{lid}.wav')
    with torch.no_grad():
        em = torch.log_softmax(S.model(torch.tensor(x)[None]).logits[0], -1)
    fps = em.shape[0] / (len(x) / S.SR)
    words = []; tokens = []
    for m in re.finditer(r"[А-Яа-яЁё-]+", text):
        w = m.group(0).replace('-', '')
        chars = [c for c in w.lower().replace('ё', 'е') if c in S.vocab]
        if not chars: continue
        p = re.match(r'\s*([.,:?!])', text[m.end():m.end() + 2])
        words.append(dict(w=m.group(0), start=len(tokens), n=len(chars), p=p.group(1) if p else ''))
        tokens += [S.vocab[c] for c in chars]
        if S.sep is not None: tokens.append(S.sep)
    first = S.align(em, torch.tensor(tokens))
    h = 160; db = np.array([20 * np.log10(np.sqrt(np.mean(x[i:i + h] ** 2)) + 1e-9) for i in range(0, len(x) - h, h)])
    q = db < db.max() - THR; q50 = db < db.max() - 50
    out = []
    for a, b in zip(words, words[1:]):
        fl = first[a['start'] + a['n'] - 1]; fn = first[b['start']]
        if fl is None or fn is None: continue
        t0, t1 = fl / fps, fn / fps
        i0, i1 = int(t0 * 100), int(t1 * 100) + 3   # от начала последней буквы до начала следующего слова (+30 мс на смычку)
        def longest(qq):
            best = run = 0; be = None
            for k, v in enumerate(qq[i0:i1]):
                run = run + 1 if v else 0
                if run > best: best = run; be = i0 + k + 1
            return best, be
        b35, e35 = longest(q); b50, e50 = longest(q50)
        out.append(dict(after=a['w'], p=a['p'], nxt=b['w'], sil=round(b35 * 0.01, 2), sil50=round(b50 * 0.01, 2),
                        s50=round(((e50 or 0) - b50) * 0.01, 2), e50=round((e50 or 0) * 0.01, 2), t0=round(t0, 2), t=round(t1, 2)))
    print(json.dumps(dict(id=lid, gaps=out), ensure_ascii=False), flush=True)
