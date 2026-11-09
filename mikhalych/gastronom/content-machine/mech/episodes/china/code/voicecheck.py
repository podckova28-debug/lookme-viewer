"""Скрупулёзная проверка дублей Alexey: сверка ASR с текстом, уверенность по словам, ударение по слогам, темп, паузы.

    python3 voicecheck.py <id>=<file.mp3> ... > report.jsonl

Для каждого файла печатает JSON: слова (текст сценария ↔ услышанное, вероятность, время), паузы на каждой границе слов
с пунктуацией сценария, проверку ударения (какой слог самый «сильный» по громкости и длительности против словаря
RUAccent из work/stress.json), темп (слогов в секунду). Ударение по акустике шумное: это подсказка, не приговор.
"""
import sys, json, re, subprocess, difflib
import numpy as np, imageio_ffmpeg
from faster_whisper import WhisperModel
from num2words import num2words
FF = imageio_ffmpeg.get_ffmpeg_exe(); SR = 16000
VOW = 'аеёиоуыэюя'
LINES = dict(json.load(open('work/lines.json')))
STRESS = json.load(open('work/stress.json'))
LAT = {'cherry': 'чери', 'chery': 'чери', 'geely': 'джили', 'haval': 'хавейл', 'havel': 'хавейл', 'tenet': 'тенет', 'skywell': 'скайвелл',
       'jd': 'джей ди', 'power': 'пауэр', 'kai': 'кайи', 'kaiyi': 'кайи', 'tigo': 'тигго', 'tiggo': 'тигго', 'dealer': 'дилер',
       'trade': 'трейд', 'in': 'ин', 'volkswagen': 'фольксвагена'}

def norm(w):
    w = w.lower().replace('ё', 'е')
    w = re.sub(r'[^\w%-]', '', w)
    return w

def asr_tokens(words):
    out = []
    for w in words:
        t = norm(w.word)
        t = LAT.get(t, t)
        if re.fullmatch(r'\d+', t.replace('-', '')):
            n = int(re.sub(r'\D', '', t))
            for x in num2words(n, lang='ru').split(): out.append((x, w, True))
        elif t in ('%',): out.append(('процентов', w, True))
        else:
            for x in t.replace('-', ' ').split(): out.append((x, w, False))
    return out

def script_tokens(text):
    toks = []
    for m in re.finditer(r"[\w-]+|[.,:?!]", text):
        s = m.group(0)
        if re.fullmatch(r'[.,:?!]', s):
            if toks: toks[-1]['punct'] = s
            continue
        for x in s.replace('-', ' ').split(): toks.append(dict(w=x, n=norm(x), punct=''))
    return toks

def stress_index(word, lid):
    """Номер ударного гласного (0..) по RUAccent для слова из реплики; None, если слово односложное или не найдено."""
    s = STRESS.get(lid, '')
    for cand in re.findall(r"[\w+]+", s):
        plain = cand.replace('+', '')
        if norm(plain) == norm(word) and '+' in cand:
            pre = cand[:cand.index('+')]
            return sum(1 for c in pre.lower() if c in VOW)
    return None

def load(path):
    raw = subprocess.run([FF, '-v', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768

def frames_db(x, hop=0.005, win=0.02):
    h = int(hop * SR); w = int(win * SR); n = max(1, (len(x) - w) // h)
    e = np.array([np.sqrt(np.mean(x[i * h:i * h + w] ** 2)) for i in range(n)])
    return 20 * np.log10(e + 1e-7), hop

def nuclei(db, hop, t0, t1):
    """Ядра слогов внутри [t0, t1]: локальные максимумы громкости, разделённые провалом ≥ 2 дБ."""
    a, b = int(t0 / hop), int(t1 / hop)
    seg = db[a:b]
    if len(seg) < 6: return []
    k = 3; sm = np.convolve(seg, np.ones(k) / k, mode='same')
    peaks = []
    for i in range(1, len(sm) - 1):
        if sm[i] >= sm[i - 1] and sm[i] > sm[i + 1] and sm[i] > sm.max() - 18: peaks.append(i)
    # склеиваем пики без провала 2 дБ между ними
    merged = []
    for p in peaks:
        if merged and (sm[merged[-1]:p + 1].min() > min(sm[merged[-1]], sm[p]) - 2.0 or (p - merged[-1]) * hop < 0.06):
            if sm[p] > sm[merged[-1]]: merged[-1] = p
        else: merged.append(p)
    res = []
    for p in merged:
        top = sm[p]; l = p; r = p
        while l > 0 and sm[l - 1] > top - 4: l -= 1
        while r < len(sm) - 1 and sm[r + 1] > top - 4: r += 1
        res.append(dict(t=(a + p) * hop, db=float(top), dur=(r - l + 1) * hop))
    return res

def main():
    m = WhisperModel('medium', device='cpu', compute_type='int8', cpu_threads=4,
                     download_root='/home/user/gastronom/content-machine/video/whisper')
    for arg in sys.argv[1:]:
        lid, path = arg.split('=', 1); base = lid.split('_')[0]
        text = LINES[base]
        x = load(path); db, hop = frames_db(x)
        segs, _ = m.transcribe(path, language='ru', beam_size=5, word_timestamps=True, vad_filter=False,
                               initial_prompt='Чери, Джили, Хавейл, Тенет, Кайи, Скайвелл, Тигго, утильсбор, сайлентблоки.')
        words = [w for s in segs for w in s.words]
        A = asr_tokens(words); S = script_tokens(text)
        sm = difflib.SequenceMatcher(a=[s['n'] for s in S], b=[a[0] for a in A], autojunk=False)
        amap = {}
        mism = []
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op == 'equal':
                for k in range(i2 - i1): amap[i1 + k] = A[j1 + k][1]
            else:
                sw = ' '.join(s['w'] for s in S[i1:i2]); aw = ' '.join(a[0] for a in A[j1:j2])
                numeric = any(a[2] for a in A[j1:j2])
                ratio = difflib.SequenceMatcher(a=norm(sw), b=norm(aw)).ratio()
                if not numeric and ratio < 0.85: mism.append(dict(script=sw, heard=aw, ratio=round(ratio, 2)))
                for k in range(i2 - i1):
                    if j1 + min(k, max(0, j2 - j1 - 1)) < len(A) and j2 > j1: amap[i1 + k] = A[j1 + min(k, j2 - j1 - 1)][1]
        # паузы на границах: тишина (ниже −35 дБ от пика) между концом слова i и началом слова i+1
        peak = db.max(); pauses = []
        for i in range(len(S) - 1):
            w1, w2 = amap.get(i), amap.get(i + 1)
            if w1 is None or w2 is None or w1 is w2: continue
            lo, hi = max(0, w1.end - 0.12), w2.start + 0.12
            a, b = int(lo / hop), int(hi / hop)
            q = db[a:b] < peak - 35
            best = run = 0
            for v in q:
                run = run + 1 if v else 0; best = max(best, run)
            pauses.append(dict(after=S[i]['w'], p=S[i]['punct'], sil=round(best * hop, 3), gap=round(max(0, w2.start - w1.end), 3), t1=round(w1.end, 3), t2=round(w2.start, 3)))
        # ударение
        stress = []
        for i, s in enumerate(S):
            nv = sum(1 for c in s['n'] if c in VOW)
            if nv < 2: continue
            w = amap.get(i)
            if w is None: continue
            exp = stress_index(s['w'], base)
            if exp is None: continue
            nu = nuclei(db, hop, max(0, w.start - 0.02), w.end + 0.02)
            if len(nu) != nv: stress.append(dict(w=s['w'], exp=exp, nuc=len(nu), nv=nv, ok=None)); continue
            final = bool(s['punct'])
            score = [n['db'] + 12 * np.log10(n['dur'] + 1e-3) - (3.0 if final and j == nv - 1 else 0) for j, n in enumerate(nu)]
            got = int(np.argmax(score)); srt = sorted(score)
            stress.append(dict(w=s['w'], exp=exp, got=got, margin=round(float(srt[-1] - srt[-2]), 1), ok=(got == exp)))
        probs = [w.probability for w in words]
        dur = (words[-1].end - words[0].start) if words else 0
        syl = sum(sum(1 for c in s['n'] if c in VOW) for s in S)
        rep = dict(id=lid, file=path, heard=' '.join(w.word.strip() for w in words), mean=round(float(np.mean(probs)), 3) if probs else 0,
                   min=round(float(np.min(probs)), 3) if probs else 0,
                   low=[(w.word.strip(), round(w.probability, 2)) for w in words if w.probability < 0.75],
                   mism=mism, pauses=pauses, t0=round(words[0].start, 3) if words else 0, tN=round(words[-1].end, 3) if words else 0, stress=stress, rate=round(syl / dur, 2) if dur else 0, speech=round(dur, 2))
        print(json.dumps(rep, ensure_ascii=False), flush=True)

if __name__ == '__main__':
    main()
