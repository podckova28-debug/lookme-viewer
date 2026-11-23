"""Насколько живая речь: разброс высоты голоса (полутоны), диапазон, динамика громкости.
    cbx_env/bin/python voiceclone/expr/prosody.py <файлы...>"""
import sys, glob, numpy as np, librosa
def prosody(p):
    y, sr = librosa.load(p, sr=16000)
    f0, vf, _ = librosa.pyin(y, fmin=65, fmax=260, sr=sr, frame_length=1024, hop_length=160)
    f = f0[vf & ~np.isnan(f0)]
    if len(f) < 20: return None
    st = 12 * np.log2(f / np.median(f))
    st = st[np.abs(st) < 12]                      # октавные ошибки pyin не считаем
    rms = librosa.feature.rms(y=y, frame_length=1024, hop_length=160)[0]
    db = 20 * np.log10(rms[rms > rms.max() * 0.05] + 1e-9)
    return dict(dur=len(y) / sr, f0=float(np.median(f)), st_std=float(np.std(st)),
                st_range=float(np.percentile(st, 90) - np.percentile(st, 10)), db_std=float(np.std(db)))
if __name__ == '__main__':
    paths = [q for a in sys.argv[1:] for q in sorted(glob.glob(a))]
    for p in paths:
        r = prosody(p)
        if r: print(f"{p.split('/')[-1]:28s} {r['dur']:5.1f}s f0 {r['f0']:5.0f}  std {r['st_std']:4.2f} st  range {r['st_range']:5.2f} st  dB±{r['db_std']:4.1f}", flush=True)
