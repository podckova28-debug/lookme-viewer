"""Паузы по пунктуации сценария (а не по длине тишины, как pauses2.py).

    python3 pauses3.py report.jsonl <id> in.mp3 out.wav

Берёт границы слов из отчёта voicecheck.py (время конца/начала слова и знак после слова в сценарии) и на каждой
границе ставит тишину нужной длины: точка 0,30 с, «!» 0,30, «?» 0,34, двоеточие 0,22, запятая 0,14; где знака нет,
пауза длиннее 0,07 с — запинка, сжимаем до 0,05. Короткую паузу на точке/вопросе/двоеточии удлиняем вставкой тишины,
на запятой — только если её почти нет (< 0,07 → 0,10). Края: 30 мс до первого звука и 60 мс после последнего
(мягкие «с», «х», «ф» в начале не срезаются). Склейки с плавным переходом 12 мс."""
import sys, json, subprocess, os
import numpy as np, imageio_ffmpeg, wave
FF = imageio_ffmpeg.get_ffmpeg_exe(); SR = 44100; H = SR // 100
TARGET = {'.': 0.30, '!': 0.30, '?': 0.34, ':': 0.22, ',': 0.14, '': 0.05}

def load(p):
    raw = subprocess.run([FF, '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768

def plan(x, rep):
    n = len(x) // H
    db = 20 * np.log10(np.sqrt((x[:n * H].reshape(n, H) ** 2).mean(1)) + 1e-9); peak = db.max()
    q = db < peak - float(os.environ.get('QDB', 35))  # QDB=28 — если в паузе слышно дыхание
    loud = np.flatnonzero(db > peak - 48)
    start = max(0, (loud[0] - 3) * H); end = min(len(x), (loud[-1] + 7) * H)
    ops = []  # (pos, old_len, new_len) в сэмплах: заменить отрезок [pos, pos+old_len) тишиной длины new_len
    for b in rep['pauses']:
        T = TARGET.get(b['p'], 0.05)
        a0, a1 = int((b['t1'] - 0.12) * 100), int((b['t2'] + 0.12) * 100)
        a0, a1 = max(a0, 0), min(a1, n)
        best = None; k = a0
        while k < a1:
            if q[k]:
                j = k
                while j < a1 and q[j]: j += 1
                if best is None or j - k > best[1] - best[0]: best = (k, j)
                k = j
            else: k += 1
        cur = (best[1] - best[0]) / 100 if best and best[1] - best[0] >= 2 else 0.0
        if b['p'] == '': T = 0.05 if cur > 0.07 else None
        if T is None: continue
        if cur > T + 0.01:
            s0, s1 = best[0] * H, best[1] * H
            ops.append((s0, s1 - s0, int(T * SR)))
        elif cur + 0.01 < T and (b['p'] in '.!?:' or (b['p'] == ',' and cur < 0.07)):
            if b['p'] == ',': T = 0.10
            if best and cur > 0:
                s0, s1 = best[0] * H, best[1] * H
            else:  # тишины нет: вставляем в самой тихой точке у границы
                w0, w1 = int((b['t1'] - 0.05) * 100), int((b['t2'] + 0.05) * 100)
                w0, w1 = max(w0, 0), max(min(w1, n), max(w0, 0) + 1)
                m = w0 + int(np.argmin(db[w0:w1])); s0 = s1 = m * H + H // 2
            ops.append((s0, s1 - s0, int(T * SR)))
    ops = sorted(o for o in ops if start <= o[0] < end)
    return start, end, ops

def render(x, start, end, ops):
    fade = int(0.012 * SR); out = []; pos = start
    def tail(seg):  # плавно гасим конец куска
        seg = seg.copy(); k = min(fade, len(seg)); seg[len(seg) - k:] *= np.linspace(1, 0, k); return seg
    def head(seg):
        seg = seg.copy(); k = min(fade, len(seg)); seg[:k] *= np.linspace(0, 1, k); return seg
    for s0, old, new in ops:
        if s0 < pos: continue
        out.append(tail(x[pos:s0 + min(old, fade)]) if old else x[pos:s0])
        out.append(np.zeros(max(0, new - (2 * min(old, fade) if old else 0)), np.float32))
        pos = s0 + old - (min(old, fade) if old else 0)
        if old: out.append(head(x[pos:pos + min(old, fade)])); pos += min(old, fade)
    out.append(x[pos:end])
    y = np.concatenate(out)
    k = int(0.02 * SR); y[:k] *= np.linspace(0, 1, k); y[-k:] *= np.linspace(1, 0, k)
    return y

if __name__ == '__main__':
    rpath, rid, src, dst = sys.argv[1:5]
    rep = next(json.loads(l) for l in open(rpath) if json.loads(l)['id'] == rid)
    x = load(src); start, end, ops = plan(x, rep); y = render(x, start, end, ops)
    with wave.open(dst, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
    print(rid, f'{len(x) / SR:.2f} → {len(y) / SR:.2f} с,', len(ops), 'правок')
