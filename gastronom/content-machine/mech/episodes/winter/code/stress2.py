"""Ударение по разметке гласных: wav2vec2 (русский, по буквам) выравнивает текст сценария по звуку (CTC Viterbi),
для каждого гласного берём длительность, громкость и тон; самый «сильный» гласный слова сравниваем со словарём.

    python3.13 stress2.py <id>=<file> ... > out.jsonl
"""
import sys, json, re, subprocess
import numpy as np, torch, imageio_ffmpeg
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
FF = imageio_ffmpeg.get_ffmpeg_exe(); SR = 16000
M = '/home/user/gastronom/content-machine/video/w2v/models--jonatasgrosman--wav2vec2-large-xlsr-53-russian/snapshots/2329100508896c6d9b157019803ab5601e6f3406'
proc = Wav2Vec2Processor.from_pretrained(M); model = Wav2Vec2ForCTC.from_pretrained(M).eval()
torch.set_num_threads(4)
vocab = proc.tokenizer.get_vocab(); blank = proc.tokenizer.pad_token_id; sep = vocab.get('|', None)
VOW = set('аеиоуыэюяё')
LINES = dict(json.load(open('work/lines.json'))); STRESS = json.load(open('work/stress.json'))
OVR = {'тенет': 0, 'тэнет': 0, 'чери': 0, 'кайи': 0, 'самое': 0, 'хавейл': 1, 'хавейла': 1, 'тигго': 0, 'джили': 0}

def load(p):
    raw = subprocess.run([FF, '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768

def expected(word, lid):
    w = word.lower().replace('ё', 'е')
    if w in OVR: return OVR[w]
    for cand in re.findall(r"[\w+]+", STRESS.get(lid, '')):
        if cand.replace('+', '').lower().replace('ё', 'е') == w and '+' in cand:
            return sum(1 for c in cand[:cand.rindex('+')].lower().replace('+', '') if c in VOW)  # главное ударение — последнее «+»
    return None

def align(em, tokens):
    T, N = em.shape[0], len(tokens)
    tr = torch.full((T + 1, N + 1), -1e9); tr[0, 0] = 0
    tr[1:, 0] = torch.cumsum(em[:, blank], 0)
    for t in range(T):
        stay = tr[t, 1:] + em[t, blank]
        chg = tr[t, :-1] + em[t, tokens]
        tr[t + 1, 1:] = torch.maximum(stay, chg)
    # обратный проход
    t, j = T, N; first = [None] * N
    while t > 0 and j > 0:
        stay = tr[t - 1, j] + em[t - 1, blank]; chg = tr[t - 1, j - 1] + em[t - 1, tokens[j - 1]]
        if chg > stay: first[j - 1] = t - 1; j -= 1
        t -= 1
    return first

def f0_track(x, hop=160, win=640):
    out = []
    for i in range(0, len(x) - win, hop):
        s = x[i:i + win] - x[i:i + win].mean()
        if np.sqrt((s ** 2).mean()) < 0.01: out.append(0); continue
        ac = np.correlate(s, s, 'full')[win - 1:]; lo, hi = SR // 300, SR // 70
        k = lo + int(np.argmax(ac[lo:hi])); out.append(SR / k if ac[k] > 0.3 * ac[0] else 0)
    return np.array(out)

def main():
    for arg in sys.argv[1:]:
        lid, path = arg.split('=', 1); base = lid.split('_')[0]
        text = LINES[base]; x = load(path)
        with torch.no_grad():
            em = torch.log_softmax(model(torch.tensor(x)[None]).logits[0], -1)
        fps = em.shape[0] / (len(x) / SR)
        words = []; tokens = []; idx = []
        for m in re.finditer(r"[А-Яа-яЁё-]+", text):
            w = m.group(0).replace('-', '')
            chars = [c for c in w.lower().replace('ё', 'е') if c in vocab]
            if not chars: continue
            words.append(dict(w=m.group(0), start=len(tokens), n=len(chars), chars=chars, final=bool(re.match(r'\s*[.,:?!]', text[m.end():m.end() + 2]))))
            tokens += [vocab[c] for c in chars]
            if sep is not None: tokens.append(sep)
        first = align(em, torch.tensor(tokens))
        db = 20 * np.log10(np.sqrt(np.convolve(x ** 2, np.ones(160) / 160, 'same')) + 1e-6)
        f0 = f0_track(x)
        res = []
        for w in words:
            vs = []
            for k in range(w['n']):
                c = w['chars'][k]
                if c not in VOW: continue
                a = first[w['start'] + k]; b = first[w['start'] + k + 1] if w['start'] + k + 1 < len(first) else None
                if a is None or b is None: continue
                t0, t1 = a / fps, max(b, a + 1) / fps
                seg = db[int(t0 * SR):int(t1 * SR)]
                fz = f0[int(t0 * 100):int(t1 * 100)]; fz = fz[fz > 0]
                vs.append(dict(dur=t1 - t0, db=float(seg.max()) if len(seg) else -60, f0=float(np.median(fz)) if len(fz) else 0))
            nv = sum(1 for c in w['chars'] if c in VOW)
            if nv < 2 or len(vs) != nv: continue
            exp = expected(w['w'], base)
            if exp is None: continue
            # последний гласный перед паузой забирает паузу себе (CTC): ограничиваем его медианой остальных × 1,3
            others = [v['dur'] for v in vs[:-1]]
            if others: vs[-1]['dur'] = min(vs[-1]['dur'], float(np.median(others)) * 1.3 if (w['final'] or vs[-1]['dur'] > 0.25) else vs[-1]['dur'])
            md = max(v['dur'] for v in vs) or 1e-3; mdb = max(v['db'] for v in vs)
            f0s = [v['f0'] for v in vs if v['f0'] > 0]; mf = max(f0s) if f0s else 0
            sc = []
            for v in vs:
                st = 12 * np.log2(v['f0'] / mf) if v['f0'] > 0 and mf > 0 else -3
                sc.append(v['dur'] / md + 0.35 * (v['db'] - mdb) / 6)
            got = int(np.argmax(sc)); srt = sorted(sc)
            res.append(dict(w=w['w'], exp=exp, got=got, margin=round(float(srt[-1] - srt[-2]), 2),
                            durs=[round(v['dur'], 3) for v in vs]))
        print(json.dumps(dict(id=lid, words=res), ensure_ascii=False), flush=True)

if __name__ == '__main__':
    main()
