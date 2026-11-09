"""Точная подрезка пауз по границам слов из wordgaps.py (выравнивание wav2vec2 по буквам).
Режем только чистую тишину (< пик−50 дБ): голову и хвост паузы оставляем, середину вынимаем, стык 10 мс.

    python3 work/gapfix.py work/wg_done.jsonl [--dry]

Цели чистой тишины: точка 0,28 с, «?» 0,32, двоеточие 0,20, запятая 0,12 (режем, только если > 0,20).
Без знака: > 0,12 с → 0,08 (смычки согласных не трогаем); явные запинки внутри словосочетания → 0,04;
смысловые границы без знака (подлежащее | сказуемое, перечисление) → 0,12. Крючок I01 после числа — 0,40.
Удлинять не нужно: самые короткие точки и двоеточия и так ≥ 0,17 с."""
import sys, json, wave, numpy as np, os, shutil
TGT = {'.': 0.28, '!': 0.28, '?': 0.32, ':': 0.20, ',': 0.12}
HITCH = {('A2', 'китайских'), ('A6', 'и'), ('A7', 'машин'), ('F4', 'лет')}
NATURAL = {('I04', 'ломается'): 0.12, ('A4', 'машин'): 0.12, ('A8', 'России'): 0.12, ('I01', 'тысячи'): 0.40,
           ('Z4', 'Михалыча'): 0.22, ('B10', 'компаниями'): 0.18}  # Z4: двоеточие за кавычкой; B10: конец придаточного перед сказуемым
dry = '--dry' in sys.argv
os.makedirs('vo_v4', exist_ok=True)
for l in open(sys.argv[1]):
    r = json.loads(l); k = r['id']; cuts = []
    for g in r['gaps']:
        s = g['sil50']
        if g['p'] == ',' and s <= 0.20: continue
        if (k, g['after']) in NATURAL: T = NATURAL[(k, g['after'])]
        elif g['p']: T = TGT[g['p']]
        elif (k, g['after']) in HITCH: T = 0.04
        elif s > 0.12: T = 0.08
        else: continue
        if s > T + 0.03:
            cuts.append((g['e50'] - s, g['e50'], T, g['after'] + g['p'], g['nxt']))
    if not cuts: continue
    for c in cuts: print(f"{k:5s} «{c[3]} | {c[4]}» {c[1]-c[0]:.2f} → {c[2]:.2f}")
    if dry: continue
    src = f'vo/{k}.wav'
    if not os.path.exists(f'vo_v4/{k}.wav'): shutil.copy(src, f'vo_v4/{k}.wav')
    w = wave.open(f'vo_v4/{k}.wav'); sr = w.getframerate(); ch = w.getnchannels(); sw = w.getsampwidth()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, ch).astype(np.float32)
    xf = int(0.010 * sr); out = []; pos = 0
    for a, b, T, *_ in sorted(cuts):
        A, B = int(a * sr), int(b * sr); keep = int(T / 2 * sr)
        h_end = A + keep; t_beg = B - keep
        if t_beg - h_end <= xf: continue
        out.append(x[pos:h_end - xf])
        fade = np.linspace(1, 0, xf)[:, None]
        out.append(x[h_end - xf:h_end] * fade + x[t_beg - xf:t_beg] * (1 - fade))
        pos = t_beg
    out.append(x[pos:])
    y = np.clip(np.concatenate(out), -32768, 32767).astype(np.int16)
    o = wave.open(src, 'wb'); o.setnchannels(ch); o.setsampwidth(sw); o.setframerate(sr); o.writeframes(y.tobytes()); o.close()
