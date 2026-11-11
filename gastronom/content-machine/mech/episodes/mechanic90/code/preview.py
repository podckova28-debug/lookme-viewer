"""Пробные стоп-кадры монтажа до прихода озвучки: голос заменён тишиной длиной «слова / 2,4 с».
Проверяет графику (карточки глав, плашки, подписи, год) на лицах и переполнение текста.

    python3 work/preview.py [реплика@доля ...] → qa/preview_<n>.jpg (листы по 12 кадров 640×360)
Без аргументов — середина каждой реплики с графикой и 2 с после начала каждой главы.
"""
import os, sys
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, D); os.chdir(D)
import numpy as np
import cut, gfx
from PIL import Image, ImageDraw

TXT = dict(cut.LINES)
cut.vo_line = lambda lid: np.zeros(int(cut.SR * len(TXT[lid].split()) / 2.4), np.float32)
shots, total = cut.plan()
ovs = []
for ov in cut.OVERLAYS:
    st = cut.LT[ov['line']][0] + ov.get('at', 0.3)
    en = st + ov['dur'] if 'dur' in ov else cut.LT[ov.get('to', ov['line'])][2] - 0.2 + ov.get('extra', 0)
    ovs.append((st, en, ov))

def frame(t):
    si = max(i for i, s in enumerate(shots) if s['t'] <= t); s = shots[si]
    src = cut.source(s); src.skip(int(round((t - s['t']) * cut.FPS))); cur = src.next(); src.close()
    fr = Image.fromarray(cur).convert('RGBA')
    for st, en, ov in ovs:
        if st <= t < en: gfx.draw(fr, ov, t - st, en - st)
    return fr.convert('RGB'), s

if len(sys.argv) > 1:
    pts = []
    for a in sys.argv[1:]:
        lid, k = a.split('@'); a0, _, b0 = cut.LT[lid]; pts.append((lid, a0 + (b0 - a0) * float(k)))
else:
    with_ov = {ov['line'] for ov in cut.OVERLAYS if ov['type'] in ('bars', 'caption', 'title')}
    pts = [(l, (cut.LT[l][0] + cut.LT[l][2]) / 2) for l, _ in cut.LINES if l in with_ov]
    import timeline
    pts += [(a, cut.LT[a][0] + 2.0) for a, *_ in timeline.CHAPTERS] + [(a, cut.LT[a][0] + 5.0) for a, *_ in timeline.CHAPTERS[:2]]
    pts.sort(key=lambda p: p[1])
os.makedirs('qa', exist_ok=True)
for n in range(0, len(pts), 12):
    part = pts[n:n + 12]; sheet = Image.new('RGB', (3 * 650, ((len(part) + 2) // 3) * 370), 'white'); d = ImageDraw.Draw(sheet)
    for k, (lid, t) in enumerate(part):
        fr, s = frame(t); x, y = (k % 3) * 650, (k // 3) * 370
        sheet.paste(fr.resize((640, 360), Image.LANCZOS), (x, y))
        d.rectangle([x, y, x + 150, y + 20], fill='black'); d.text((x + 4, y + 4), f'{lid} {s["name"]} {t:.1f}s', fill='white')
    sheet.save(f'qa/preview_{n // 12}.jpg', quality=82); print('qa/preview_%d.jpg' % (n // 12), [p[0] for p in part])
print('итого ≈', round(total / 60, 1), 'мин (оценка, голос — тишина)')
