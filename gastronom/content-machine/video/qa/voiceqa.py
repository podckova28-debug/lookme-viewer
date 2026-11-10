#!/usr/bin/env python3.13
"""Проверка дублей озвучки ПОСЛЕ синтеза: без участия человека решает, какой дубль годен, и что переозвучить.

    python3.13 voiceqa.py --lines <script.py|lines.json> --takes <папка с <id>_<дубль>.mp3|wav> [--only I01,A2]
                          [--risk textgate.json] [--out voice_qa.json] [--engine minimax|silero]

На каждый дубль:
  1. Распознавание (faster-whisper medium) и сверка со сценарием по словам. Расхождение не считается ошибкой сразу:
     служебные слова, числа и безударные окончания (самая/самое, треснула/треснуло) пропускаются, а остальное
     перепроверяет акустическая модель wav2vec2 (CTC): на этом отрезке звук ближе к тексту сценария или к услышанному?
     Так «нáледь», которую whisper пишет «налить», проходит, а «на местах» вместо «на месте» — нет.
  2. Ударение в рискованных словах (lexicon.check, не из словаря RUAccent, имена и марки): длительность и громкость
     гласных по выравниванию wav2vec против словарного ударения. Последнее слово фразы растянуто паузой — там порог выше.
  3. Разрыв фразы: whisper поставил точку там, где в сценарии нет знака, и в этом месте тишина (как «этого. Года»).
  4. Проглоченное слово: слова сценария нет в распознавании и по выравниванию на него почти нет звука.
  5. Паузы без знака > 0,15 с — предупреждение (их снимает gapfix.py автоматически).
Итог по реплике: лучший дубль без ошибок; если таких нет — в списке переозвучки с причинами.
"""
import sys, os, re, json, glob, difflib, subprocess, importlib.util
import numpy as np, torch, imageio_ffmpeg
from num2words import num2words

HERE = os.path.dirname(os.path.abspath(__file__))
FF = imageio_ffmpeg.get_ffmpeg_exe(); SR = 16000
VIDEO = os.path.dirname(HERE)                         # qa/ лежит в content-machine/video/


def _models(sub):
    """Кэш моделей: $QA_MODELS/<sub>, затем content-machine/video/<sub> (в .gitignore), затем рабочая копия gastronom."""
    for d in (os.environ.get('QA_MODELS') and os.path.join(os.environ['QA_MODELS'], sub), os.path.join(VIDEO, sub),
              os.path.join('/home/user/gastronom/content-machine/video', sub)):
        if d and os.path.isdir(d): return d
    return os.path.join(VIDEO, sub)


_snap = sorted(glob.glob(os.path.join(_models('w2v'), 'models--jonatasgrosman--wav2vec2-large-xlsr-53-russian', 'snapshots', '*')))
W2V = _snap[-1] if _snap else 'jonatasgrosman/wav2vec2-large-xlsr-53-russian'   # нет кэша — скачается с HF
WHISPER_DIR = _models('whisper')
VOW = set('аеёиоуыэюя')
FUNC = {'и', 'а', 'но', 'не', 'ни', 'в', 'во', 'на', 'с', 'со', 'к', 'ко', 'о', 'об', 'у', 'по', 'за', 'из', 'же', 'ли', 'бы', 'то',
        'от', 'до', 'для', 'при', 'под', 'над', 'или', 'да', 'вот', 'уж', 'ведь', 'это', 'там', 'тут', 'так', 'как'}
ENDINGS = re.compile(r'(ого|его|ему|ому|ыми|ими|ая|яя|ое|ее|ые|ие|ый|ий|ой|ей|ую|юю|ым|им|ом|ем|а|о|е|и|ы|у|ю|я)$')
LEX = json.load(open(os.path.join(HERE, 'lexicon.json'), encoding='utf-8'))
STRESS_OVR = {'наледь': 0, 'наледи': 0, 'михалыча': 1, 'михалыч': 1, 'месте': 0, 'чери': 0, 'хавейл': 1, 'хавейла': 1,
              'тэнет': 0, 'тенет': 0, 'джили': 0, 'тигго': 0, 'кайи': 0,
              'самое': 0, 'самом': 0, 'самая': 0, 'самый': 0}   # RUAccent ставит «самоё» — эталон из словаря, не из него
T_CTC = 0.45        # нат/символ: насколько звук должен быть ближе к услышанному, чтобы считать это ошибкой.
                    # Настройка по эталонам: «налеть» вместо «наледь» +1,00 (ошибка); «почасти»/«почисти» +0,40 и
                    # «вести»/«везти» +0,39 (не ошибки: дубли приняты на слух, «везти» звучит как «вести»)
T_STRESS, T_STRESS_FINAL = 0.20, 0.50        # для слов из словаря риска (lexicon, нет в словаре RUAccent)
T_OMO, T_OMO_FINAL = 0.50, 0.60               # для омографов: на верных дублях зимнего ролика запас доходил до 0,47


def norm(w): return re.sub(r'[^\w%]', '', w.lower().replace('ё', 'е'))


def load_lines(path):
    if os.path.basename(path).startswith('jobs') and path.endswith('.txt'):          # шортсы: «vo m01 <uuid> текст»
        return [(m.group(1), m.group(2).strip()) for m in re.finditer(r'^vo\s+(\S+)\s+\S+\s+(.+)$', open(path, encoding='utf-8').read(), re.M)]
    if path.endswith('.json'): return [tuple(x) for x in json.load(open(path, encoding='utf-8'))]
    spec = importlib.util.spec_from_file_location('script_mod', path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return list(m.LINES)


def load_audio(p):
    raw = subprocess.run([FF, '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def script_tokens(text):
    toks = []
    for m in re.finditer(r"[\w-]+|[.,:?!»]", text):
        s = m.group(0)
        if s == '»': continue
        if re.fullmatch(r'[.,:?!]', s):
            if toks: toks[-1]['punct'] = s
            continue
        for x in s.replace('-', ' ').split():
            if norm(x): toks.append(dict(w=x, n=norm(x), punct=''))
    return toks


def asr_tokens(words):
    out = []
    for k, w in enumerate(words):
        raw = w.word.strip(); p = raw[-1] if raw and raw[-1] in '.!?,:' else ''
        t = norm(raw)
        if re.fullmatch(r'\d+', t):
            parts = num2words(int(t), lang='ru').split()
            for j, x in enumerate(parts): out.append(dict(n=x, w=w, num=True, punct=p if j == len(parts) - 1 else ''))
        elif t == '%': out.append(dict(n='процентов', w=w, num=True, punct=p))
        else:
            for j, x in enumerate(t.replace('-', ' ').split()): out.append(dict(n=x, w=w, num=False, punct=p))
    return out


VOICED = str.maketrans('бвгджз', 'пфктшс')
UNVOICED = str.maketrans('пкстфш', 'бгздвж')


def phon(word, st):
    """Как слово звучит (упрощённо): редукция безударных о→а, е/я/э→и, оглушение конца и перед глухой («везти» = «вести»),
    озвончение перед звонкой («сделать» = «зделать»), -ого/-его, -тся/-ться, стн/здн, сч."""
    w = word.lower().replace('ё', 'о') if 'ё' in word else word.lower()
    w = re.sub(r'(т|)ь?ся$', 'ца', w) if re.search(r'ть?ся$', w) else w
    w = re.sub(r'([ое])го$', lambda m: m.group(1) + 'во', w)
    w = w.replace('стн', 'сн').replace('здн', 'зн').replace('сч', 'щ').replace('зч', 'щ')
    out = []; vi = 0
    for c in w:
        if c in VOW:
            if st is not None and vi != st:
                c = {'о': 'а', 'е': 'и', 'я': 'и', 'э': 'и'}.get(c, c)
            vi += 1
        out.append(c)
    w = ''.join(out)
    w = re.sub(r'([бвгджз])(ь?)$', lambda m: m.group(1).translate(VOICED) + m.group(2), w)
    w = re.sub(r'([бвгджз])(?=ь?[кпстфхцчшщ])', lambda m: m.group(1).translate(VOICED), w)
    w = re.sub(r'([пкстфш])(?=[бгджз])', lambda m: m.group(1).translate(UNVOICED), w)
    return w


def variants(word, st):
    v = {word, phon(word, st)}
    v |= {x.replace('ь', '') for x in v}
    return v


def stress_list(stressed_line, toks):
    """Номер ударного гласного для каждого слова сценария по строке RUAccent («н+аледь»), по порядку."""
    st = [c for c in re.findall(r"[\w+-]+", stressed_line or '')]
    marks = []
    for c in st:
        for part in c.replace('-', ' ').split():
            plain = norm(part.replace('+', ''))
            if not plain: continue
            k = part.rindex('+') if '+' in part else None
            marks.append((plain, sum(1 for ch in part[:k].lower().replace('+', '') if ch in VOW) if k is not None else None))
    out = []; j = 0
    for t in toks:
        val = STRESS_OVR.get(t['n'])
        while j < len(marks) and marks[j][0] != t['n']: j += 1
        if j < len(marks):
            if val is None: val = marks[j][1]
            j += 1
        if val is None and sum(1 for c in t['n'] if c in VOW) == 1: val = 0
        out.append(val)
    return out


def same_stem(a, b):
    sa, sb = ENDINGS.sub('', a), ENDINGS.sub('', b)
    return len(sa) >= 3 and sa == sb


class Acoustic:
    def __init__(self):
        from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
        torch.set_num_threads(4)
        self.proc = Wav2Vec2Processor.from_pretrained(W2V); self.model = Wav2Vec2ForCTC.from_pretrained(W2V).eval()
        self.vocab = self.proc.tokenizer.get_vocab(); self.blank = self.proc.tokenizer.pad_token_id; self.sep = self.vocab.get('|')

    def logits(self, x):
        with torch.no_grad(): return torch.log_softmax(self.model(torch.tensor(x)[None]).logits[0], -1)

    def ids(self, s): return [self.vocab[c] for c in s.lower().replace('ё', 'е') if c in self.vocab]

    def align(self, em, tokens):
        T, N = em.shape[0], len(tokens)
        tr = torch.full((T + 1, N + 1), -1e9); tr[0, 0] = 0; tr[1:, 0] = torch.cumsum(em[:, self.blank], 0)
        tk = torch.tensor(tokens)
        for t in range(T):
            tr[t + 1, 1:] = torch.maximum(tr[t, 1:] + em[t, self.blank], tr[t, :-1] + em[t, tk])
        t, j = T, N; first = [None] * N
        while t > 0 and j > 0:
            if tr[t - 1, j - 1] + em[t - 1, tk[j - 1]] > tr[t - 1, j] + em[t - 1, self.blank]: first[j - 1] = t - 1; j -= 1
            t -= 1
        return first

    def ctc_per_char(self, em, f0, f1, text):
        tg = self.ids(text.replace(' ', '|')) if self.sep is not None else self.ids(text.replace(' ', ''))
        if not tg or f1 - f0 < len(tg) + 1: return None
        lp = em[f0:f1].unsqueeze(1)
        loss = torch.nn.functional.ctc_loss(lp, torch.tensor([tg]), torch.tensor([f1 - f0]), torch.tensor([len(tg)]),
                                            blank=self.blank, reduction='sum', zero_infinity=True)
        return float(loss) / len(tg)


def word_frames(ac, em, toks):
    """Выравнивание сценария по буквам: для каждого слова — кадры начала каждой буквы."""
    seq = []; spans = []
    for t in toks:
        ch = ac.ids(t['n'])
        spans.append((len(seq), len(ch), [c for c in t['n'] if c in ac.vocab]))
        seq += ch
        if ac.sep is not None: seq.append(ac.sep)
    first = ac.align(em, seq)
    out = []
    for k, (s, n, chars) in enumerate(spans):
        fs = first[s:s + n]; nxt = first[s + n] if s + n < len(first) else em.shape[0]
        out.append(dict(chars=chars, fs=fs, end=nxt))
    return out


def stress_of(ac, em, fps, x, wf, word, final):
    """Самый сильный гласный слова по длительности и громкости; None, если не хватает данных."""
    db = 20 * np.log10(np.sqrt(np.convolve(x ** 2, np.ones(160) / 160, 'same')) + 1e-6)
    vs = []
    for k, c in enumerate(wf['chars']):
        if c not in VOW: continue
        a = wf['fs'][k]; b = wf['fs'][k + 1] if k + 1 < len(wf['fs']) else wf['end']
        if a is None or b is None: return None
        t0, t1 = a / fps, max(b, a + 1) / fps; seg = db[int(t0 * SR):int(t1 * SR)]
        vs.append(dict(dur=t1 - t0, db=float(seg.max()) if len(seg) else -60))
    if len(vs) < 2: return None
    others = [v['dur'] for v in vs[:-1]]
    if final or vs[-1]['dur'] > 0.25: vs[-1]['dur'] = min(vs[-1]['dur'], float(np.median(others)) * 1.3)
    md = max(v['dur'] for v in vs) or 1e-3; mdb = max(v['db'] for v in vs)
    sc = [v['dur'] / md + 0.35 * (v['db'] - mdb) / 6 for v in vs]
    srt = sorted(sc)
    return int(np.argmax(sc)), round(float(srt[-1] - srt[-2]), 2), [round(v['dur'], 3) for v in vs]


def expected_stress(word, stressed_line):
    w = norm(word)
    if w in STRESS_OVR: return STRESS_OVR[w]
    for cand in re.findall(r"[\w+]+", stressed_line or ''):
        if norm(cand.replace('+', '')) == w and '+' in cand:
            return sum(1 for c in cand[:cand.rindex('+')].lower().replace('+', '') if c in VOW)
    return None


def check_take(wm, ac, path, text, risk, stressed_line, omo=(), stress=True):
    x = load_audio(path); dur = len(x) / SR
    segs, _ = wm.transcribe(x, language='ru', beam_size=5, word_timestamps=True, vad_filter=False,
                            initial_prompt='Михалыч рассказывает про машины.')
    words = [w for s in segs for w in s.words]
    S = script_tokens(text); A = asr_tokens(words)
    em = ac.logits(x); fps = em.shape[0] / dur
    wf = word_frames(ac, em, S)
    SL = stress_list(stressed_line, S)
    def t_of(i): return (wf[i]['fs'][0] or 0) / fps if wf[i]['fs'] and wf[i]['fs'][0] is not None else None
    issues = []; heard = ' '.join(w.word.strip() for w in words)
    sm = difflib.SequenceMatcher(a=[s['n'] for s in S], b=[a['n'] for a in A], autojunk=False)
    amap = {}
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal':
            for k in range(i2 - i1): amap[i1 + k] = j1 + k
            continue
        sw = [s['n'] for s in S[i1:i2]]; aw = [a['n'] for a in A[j1:j2]]
        if any(a['num'] for a in A[j1:j2]): continue                                   # числа ASR пишет цифрами
        content = [w for w in sw if w not in FUNC]
        if not content and all(w in FUNC for w in aw): continue                          # служебные слова
        if len(sw) == len(aw) and all(a == b or same_stem(a, b) or (a in FUNC and b in FUNC) for a, b in zip(sw, aw)): continue
        if ''.join(sw) == ''.join(aw): continue                                         # «то же»/«тоже», «от дыхания»/«отдыхания»
        tsya = lambda ws: [re.sub(r'ться$', 'тся', w) for w in ws]
        if tsya(sw) == tsya(aw): continue                                               # «гнутся»/«гнуться» звучат одинаково
        if re.search(r'[a-z]', ''.join(aw)):                                             # ASR записал латиницей («trade in»):
            issues.append(dict(level='info', code='asr_latin', msg=f"ASR латиницей: «{' '.join(aw)}» вместо «{' '.join(sw)}»"))
            continue                                                                     # акустическая модель латиницу не читает
        if i1 == i2:                                                                     # лишнее слово в распознавании
            if any(w not in FUNC for w in aw): issues.append(dict(level='warn', code='extra', msg=f"лишнее в распознавании: «{' '.join(aw)}»"))
            continue
        f0 = int(max(0, (t_of(i1) or 0) - 0.08) * fps)
        f1 = int(min(dur, (t_of(i2) if i2 < len(S) and t_of(i2) else dur) + 0.08) * fps)
        if not aw:                                                                       # слово сценария не услышано
            d = sum((wf[k]['end'] - (wf[k]['fs'][0] or wf[k]['end'])) / fps for k in range(i1, i2))
            nv = sum(1 for w in sw for c in w if c in VOW) or 1
            if content and d < 0.07 * nv:
                issues.append(dict(level='fail', code='swallowed', msg=f"проглочено: «{' '.join(sw)}» ({d:.2f} с)", t=round(f0 / fps, 2)))
            continue
        L = S[i1 - 1]['n'] if i1 > 0 else ''; R = S[i2]['n'] if i2 < len(S) else ''
        f0 = int(max(0, (t_of(i1 - 1) if i1 > 0 and t_of(i1 - 1) is not None else (t_of(i1) or 0)) - 0.05) * fps)
        f1 = int(min(dur, (t_of(i2 + 1) if i2 + 1 < len(S) and t_of(i2 + 1) else dur) + 0.05) * fps)
        import itertools
        combos = list(itertools.product(*[sorted(variants(S[k]['n'], SL[k])) for k in range(i1, i2)]))[:32]
        cand = [' '.join(x for x in (L, ' '.join(c), R) if x) for c in combos]
        scores = [ac.ctc_per_char(em, f0, f1, c) for c in cand]; scores = [z for z in scores if z is not None]
        la = ac.ctc_per_char(em, f0, f1, ' '.join(x for x in (L, ' '.join(aw), R) if x))
        if not scores or la is None: continue
        ls = min(scores); delta = ls - la
        rec = dict(script=' '.join(sw), heard=' '.join(aw), delta=round(delta, 2), t=round(f0 / fps, 2))
        if delta > T_CTC: issues.append(dict(level='fail', code='text', msg=f"звучит «{rec['heard']}» вместо «{rec['script']}» (акустика +{delta:.2f})", **rec))
        else: issues.append(dict(level='info', code='asr_only', msg=f"ASR: «{rec['heard']}» вместо «{rec['script']}», акустика за сценарий ({delta:+.2f})", **rec))
    # ударения в рискованных словах
    risk = {norm(r) for r in risk}; omo = {norm(r) for r in omo} - risk
    if not stress: risk, omo = set(), set()   # Silero: ударение задано разметкой «+», акустический детектор на этом голосе не работает
    for i, s in enumerate(S):
        if s['n'] not in risk and s['n'] not in omo: continue
        is_omo = s['n'] in omo
        exp = SL[i]
        final = bool(s['punct']) or i == len(S) - 1
        r = stress_of(ac, em, fps, x, wf[i], s['w'], final) if exp is not None else None
        if not r: continue
        got, margin, durs = r
        thr = (T_OMO_FINAL if final else T_OMO) if is_omo else (T_STRESS_FINAL if final else T_STRESS)
        if got != exp and margin > thr:
            issues.append(dict(level='fail', code='stress', msg=f"ударение «{s['w']}»{' (омограф)' if is_omo else ''}: слышно на {got + 1}-м слоге, нужно на {exp + 1}-м (запас {margin})", t=round(t_of(i) or 0, 2)))
        else:
            issues.append(dict(level='info', code='stress_ok', msg=f"ударение «{s['w']}» в норме ({got + 1}-й слог, нужно {exp + 1}-й, запас {margin})"))
    # паузы и разрывы
    h = 160; dbf = np.array([20 * np.log10(np.sqrt(np.mean(x[k:k + h] ** 2)) + 1e-9) for k in range(0, len(x) - h, h)])
    q = dbf < dbf.max() - 50
    inv = {v: k for k, v in amap.items()}
    for i in range(len(S) - 1):
        a0 = wf[i]['fs'][-1] if wf[i]['fs'] and wf[i]['fs'][-1] is not None else None; b0 = wf[i + 1]['fs'][0] if wf[i + 1]['fs'] else None
        if a0 is None or b0 is None: continue
        i0, i1_ = int(a0 / fps * 100), int(b0 / fps * 100) + 3
        best = run = 0
        for v in q[i0:i1_]: run = run + 1 if v else 0; best = max(best, run)
        sil = best * 0.01
        j = amap.get(i)
        asr_break = j is not None and A[j]['punct'] in '.!?' and A[j]['punct'] != '' and (j + 1 >= len(A) or A[j + 1]['w'] is not A[j]['w'])
        if not S[i]['punct']:
            if asr_break and sil >= 0.15:
                issues.append(dict(level='fail', code='break', msg=f"разрыв фразы после «{S[i]['w']}»: ASR ставит «{A[j]['punct']}», тишина {sil:.2f} с", t=round(a0 / fps, 2)))
            elif sil > 0.15:
                issues.append(dict(level='warn', code='pause', msg=f"пауза без знака после «{S[i]['w']}» {sil:.2f} с (снимет gapfix)"))
    # хвост: клон (Chatterbox) иногда дописывает после фразы бормотание или дыхание, которое ASR не записывает
    # (immortal D2: текст кончился на 7,4 с, дальше 4 с звука). Считается звук громче пик−40 дБ позже 0,4 с от начала последней буквы.
    lf = [v for v in (wf[-1]['fs'] if wf else []) if v is not None]
    if lf:
        last = lf[-1] / fps; k0 = int((last + 0.4) * 100)   # начало последней буквы + 0,4 с на саму букву и затухание
        loud = dbf[k0:] > dbf.max() - 40; tail = float(loud.sum()) * 0.01
        if tail > 0.5:
            issues.append(dict(level='fail', code='tail', msg=f"лишний звук после текста: {tail:.1f} с (текст кончился на {last:.1f} с из {dur:.1f})", t=round(last, 2)))
    probs = [w.probability for w in words]
    return dict(file=path, heard=heard, issues=issues, fails=sum(1 for z in issues if z['level'] == 'fail'),
                warns=sum(1 for z in issues if z['level'] == 'warn'), conf=round(float(np.mean(probs)) if probs else 0, 3), dur=round(dur, 2))


def main():
    args = sys.argv[1:]
    def opt(name, default=None):
        if name in args: i = args.index(name); v = args[i + 1]; del args[i:i + 2]; return v
        return default
    lines = load_lines(opt('--lines')); tdir = opt('--takes'); only = opt('--only'); out = opt('--out', 'voice_qa.json'); riskf = opt('--risk')
    engine = opt('--engine', 'minimax')   # silero — ударения ставятся разметкой, проверка ударения по звуку отключена
    risk_by = {r['id']: r['risk'] for r in json.load(open(riskf, encoding='utf-8'))} if riskf else {}
    stressed_by = {r['id']: r['stressed'] for r in json.load(open(riskf, encoding='utf-8'))} if riskf else {}
    omo_by = {r['id']: r.get('omographs', []) for r in json.load(open(riskf, encoding='utf-8'))} if riskf else {}
    check_words = {k.rstrip('*') for sec in ('check', 'replace', 'avoid') for k in LEX[sec] if not k.startswith('_') and ' ' not in k}
    check_words |= set(STRESS_OVR)
    from faster_whisper import WhisperModel
    wm = WhisperModel('medium', device='cpu', compute_type='int8', cpu_threads=4, download_root=WHISPER_DIR)
    ac = Acoustic()
    files = sorted(os.listdir(tdir)); res = {}
    for lid, text in lines:
        if only and lid not in only.split(','): continue
        takes = [f for f in files if re.fullmatch(re.escape(lid) + r'(_[a-z0-9]+)?\.(mp3|wav)', f)]   # A1_b.mp3 или m01.wav
        risk = set(risk_by.get(lid, [])) | {norm(w) for w in re.findall(r'[\w-]+', text) if norm(w) in check_words or any(norm(w).startswith(c) for c in check_words if len(c) >= 5)}
        res[lid] = {}
        for f in takes:
            r = check_take(wm, ac, os.path.join(tdir, f), text, risk, stressed_by.get(lid, ''), omo_by.get(lid, []), stress=engine != 'silero')
            res[lid][f] = r
            print(json.dumps(dict(id=lid, take=f, fails=r['fails'], warns=r['warns'], issues=[z['msg'] for z in r['issues'] if z['level'] != 'info']), ensure_ascii=False), flush=True)
    picks, retake = {}, {}
    for lid, tk in res.items():
        if not tk: continue
        best = min(tk, key=lambda f: (tk[f]['fails'], tk[f]['warns'], -tk[f]['conf']))
        if tk[best]['fails']: retake[lid] = [z['msg'] for z in tk[best]['issues'] if z['level'] == 'fail']
        else: picks[lid] = best
    json.dump(dict(takes=res, picks=picks, retake=retake), open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"\nГодных реплик {len(picks)} из {len(res)}; переозвучить {len(retake)}: " + '; '.join(f"{k}: {' | '.join(v)}" for k, v in retake.items()))


if __name__ == '__main__':
    main()
