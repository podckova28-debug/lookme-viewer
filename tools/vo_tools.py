"""Free narration fixes on finished takes, using word timestamps (faster-whisper, local).

  tighten SRC OUT              squeeze every pause longer than 0.45 s inside a line down to 0.3 s, trim the edges
  cut SRC OUT "first words" "last words"   keep only that phrase (inclusive), tightened
  words SRC                    print word timings

Pauses inside lines are what sounds like a stumble; cutting by words lets one take be split across shots.
"""
import sys, re, subprocess, numpy as np

SR = 48000
_model = None
def model():
    global _model
    if _model is None:
        from faster_whisper import WhisperModel
        _model = WhisperModel('small.en', device='cpu', compute_type='int8')
    return _model

def load(path, sr):
    pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(pcm, np.float32).copy()

def words(path):
    segs, _ = model().transcribe(load(path, 16000), word_timestamps=True)
    return [(re.sub(r'[^a-z0-9]', '', w.word.lower()), w.start, w.end) for s in segs for w in s.words]

def save(x, out):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-ar', str(SR), out],
                   input=x.astype(np.float32).tobytes(), check=True)

def tighten(x, ws, max_gap=0.45, keep=0.3, edge=0.12, lo=0.0, hi=None):
    """Rebuild the line from word spans; any gap longer than max_gap shrinks to keep (cut in the quiet middle)."""
    out = [np.zeros(int(edge * SR), np.float32)]
    hi = len(x) / SR if hi is None else hi
    t0 = max(lo, ws[0][1] - 0.06)
    for (_, s, e), nxt in zip(ws, ws[1:] + [None]):
        if nxt is None:
            out.append(x[int(t0 * SR):int(min(hi, e + 0.25) * SR)]); break
        gap = nxt[1] - e
        if gap > max_gap:
            out.append(x[int(t0 * SR):int((e + keep / 2) * SR)])
            t0 = nxt[1] - keep / 2
    y = np.concatenate(out + [np.zeros(int(edge * SR), np.float32)])
    f = int(0.01 * SR); y[-f:] *= np.linspace(1, 0, f)
    return y

def find(ws, phrase, from_end=False):
    p = [re.sub(r'[^a-z0-9]', '', t) for t in phrase.lower().replace('-', ' ').split()]
    seq = [w[0] for w in ws]
    hits = [i for i in range(len(seq) - len(p) + 1) if seq[i:i + len(p)] == p]
    if not hits: sys.exit(f'phrase not found: {phrase!r} in {seq}')
    return hits[-1] + len(p) - 1 if from_end else hits[0]

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'words':
        for w in words(sys.argv[2]): print(f'{w[1]:6.2f} {w[2]:6.2f} {w[0]}')
        sys.exit()
    src, out = sys.argv[2], sys.argv[3]
    x, ws = load(src, SR), words(src)
    lo, hi = 0.0, None
    if cmd == 'cut':
        i, j = find(ws, sys.argv[4]), find(ws, sys.argv[5], True)
        lo = (ws[i - 1][2] + ws[i][1]) / 2 if i > 0 else 0.0          # never take a sliver of the word before
        hi = (ws[j][2] + ws[j + 1][1]) / 2 if j + 1 < len(ws) else None  # or the word after
        ws = ws[i:j + 1]
    y = tighten(x, ws, lo=lo, hi=hi); save(y, out)
    print(f'{out.split("/")[-1]}: {len(x) / SR:.1f}s -> {len(y) / SR:.1f}s  "{" ".join(w[0] for w in ws)}"')
