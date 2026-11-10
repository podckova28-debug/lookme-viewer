#!/usr/bin/env python3.13
"""Проверка готового рендера длинного ролика: плашки, шрифты, звук, картинка.

    python3.13 renderqa.py --project <папка с cut.py/timeline.py/gfx.py> [--video final.mp4] [--out render_qa.json] [--pack qa_pack]
    python3.13 renderqa.py --video short.mp4          # без cut.py (шортсы): только звук и картинка готового файла

Плашки (все OVERLAYS и LABELS проекта — по той же раскладке, что и cut.py):
  • шрифт: каждая строка, которую gfx/plate рисует, перехватывается вместе с файлом шрифта; символ, которого нет в
    шрифте (₽, Š, −, °, «», кавычки-лапки), — ошибка: вместо него на экране будет пустой квадрат;
  • край кадра: плашка упирается в край — ошибка (длинная подпись не влезла);
  • лица: плашка рисуется на прозрачном холсте, голова ищется (detect_heads) на ЧИСТОМ кадре того же момента, собранном
    тем же cut.source() без плашек. Плашка закрывает ≥35 % головы — ошибка, ≥10 % — на разбор. Длинная плашка
    проверяется на каждом плане, который она перекрывает;
  • плашки друг на друге в одно время — на разбор.
Наезды камеры: зум кадра-картинки больше 1,25× (в кадре меньше 64 % картинки) — ошибка, 1,2–1,25× — на разбор;
край кадра режет голову персонажа — ошибка; персонаж целиком ушел за край — на разбор. Доказательство — pack/zoom_*.jpg.
Готовый файл (--video): громкость ebur128 (норма −16…−13 LUFS, пик ≤ −1 dBTP), тишина ≥ 1,2 с внутри ролика,
замершая картинка ≥ 2 с (клип кончился раньше плана), чёрные кадры, расхождение длины с раскладкой.
"""
import sys, os, re, json, subprocess
import numpy as np
from PIL import Image, ImageDraw

REC = []
_orig_text = ImageDraw.ImageDraw.text


def _text(self, xy, text, *a, **kw):
    font = kw.get('font', a[1] if len(a) > 1 else None)
    if text and font is not None and getattr(font, 'path', None): REC.append((str(text), font.path))
    return _orig_text(self, xy, text, *a, **kw)


ImageDraw.ImageDraw.text = _text
_cm = {}


def cmap(path):
    if path not in _cm:
        from fontTools.ttLib import TTFont
        _cm[path] = set(TTFont(path, fontNumber=0).getBestCmap().keys())
    return _cm[path]


def load(project):
    project = os.path.abspath(project); sys.path.insert(0, project)
    import cut                                           # noqa: E402  (модуль проекта)
    shots, total = cut.plan()
    return cut, shots, total


def windows(cut, shots):
    """[(имя, st, en, render(canvas, t))] — все плашки ролика с теми же временами, что в cut.py."""
    out = []
    for i, ov in enumerate(cut.OVERLAYS):
        st = cut.LT[ov['line']][0] + ov.get('at', 0.3)
        en = st + ov['dur'] if 'dur' in ov else cut.LT[ov.get('to', ov['line'])][2] - 0.2 + ov.get('extra', 0)
        name = f"{ov['type']}@{ov['line']}"
        out.append(dict(name=name, st=st, en=en, ov=ov, draw=lambda c, t, ov=ov, st=st, en=en: cut.gfx.draw(c, ov, t, en - st)))
    for s in shots:
        for lab in cut.LABELS.get(s['name'], []):
            if lab.get('line') and lab['line'] != s['line']: continue
            t0 = s['t'] + lab.get('at', 0.4); t1 = s['t'] + lab.get('until', s['d'] - 0.2)
            def draw(c, t, lab=lab):
                cut.paste(c, cut.plate(lab['text'], lab.get('size', 60), tuple(lab.get('color', cut.INK))), lab.get('x', cut.W / 2), lab.get('y', 980))
            out.append(dict(name=f"label@{s['name']}", st=t0, en=t1, ov=lab, draw=draw))
    return out


def mask_at(cut, w, t):
    c = Image.new('RGBA', (cut.W, cut.H), (0, 0, 0, 0)); n0 = len(REC)
    w['draw'](c, t - w['st'])
    return np.array(c)[:, :, 3] > 40, REC[n0:]


def background(cut, shots, T):
    s = next((x for x in shots if x['t'] <= T < x['t'] + x['d']), shots[-1])
    src = cut.source(s); src.skip(int(round((T - s['t']) * cut.FPS))); fr = src.next(); src.close()
    return Image.fromarray(fr).convert('RGB') if fr is not None else None, s


def show_times(w, shots):
    """Момент «плашка раскрыта» на каждом плане, который она перекрывает."""
    a = w['st'] + min(1.6, 0.5 * (w['en'] - w['st']))
    ts = [a]
    for s in shots:
        lo, hi = max(a, s['t']), min(w['en'] - 0.3, s['t'] + s['d'])
        if hi - lo > 0.4 and all(abs(x - (lo + hi) / 2) > 0.8 for x in ts): ts.append((lo + hi) / 2)
    return sorted(ts)


def check_overlays(cut, shots, pack):
    from imgutils.detect import detect_heads
    issues = []; glyphs = {}
    ws = windows(cut, shots)
    for w in ws:
        for T in show_times(w, shots):
            m, rec = mask_at(cut, w, T)
            for text, fpath in rec:
                miss = sorted({ch for ch in text if not ch.isspace() and ord(ch) not in cmap(fpath)})
                for ch in miss: glyphs.setdefault((ch, os.path.basename(fpath)), set()).add(w['name'])
            if not m.any(): continue
            cov = m.mean(); ys, xs = np.where(m)
            if cov > 0.5: continue                            # полноэкранная заставка/затемнение
            edge = xs.min() <= 1 or ys.min() <= 1 or xs.max() >= cut.W - 2 or ys.max() >= cut.H - 2
            bg, s = background(cut, shots, T)
            if bg is None: continue
            def evidence(tag):
                comp = bg.convert('RGBA'); c = Image.new('RGBA', comp.size, (0, 0, 0, 0)); w['draw'](c, T - w['st'])
                comp.alpha_composite(c); f = f"{tag}_{w['name'].replace('@', '_')}_{T:.0f}.jpg"
                comp.convert('RGB').resize((960, 540)).save(os.path.join(pack, f), quality=85); return f
            if edge:
                issues.append(dict(level='review', code='edge', t=round(T, 1), what=w['name'], image=evidence('edge'),
                                   msg=f"{w['name']} {T:.1f} с: плашка упирается в край кадра (обрезана?)"))
            worst = 0
            for (x0, y0, x1, y1), _, sc in detect_heads(bg, conf_threshold=0.35):
                x0, y0, x1, y1 = [int(v) for v in (x0, y0, x1, y1)]
                area = max(1, (x1 - x0) * (y1 - y0)); cover = m[y0:y1, x0:x1].sum() / area
                worst = max(worst, cover)
            if worst >= 0.10:
                lvl = 'fail' if worst >= 0.35 else 'review'
                issues.append(dict(level=lvl, code='face', t=round(T, 1), what=w['name'], shot=s['name'], cover=worst, image=evidence('face'),
                                   msg=f"{w['name']} {T:.1f} с (план {s['name']}): закрывает {worst * 100:.0f} % головы"))
    best = {}                                          # одна строка на плашку и вид флага — самый тяжелый случай
    for z in issues:
        k = (z['what'], z['code']); o = best.get(k)
        if o is None or (z['level'] == 'fail', z.get('cover', 0)) > (o['level'] == 'fail', o.get('cover', 0)): best[k] = z
    issues = list(best.values())
    for (ch, font), names in sorted(glyphs.items()):
        issues.append(dict(level='fail', code='glyph', what=sorted(names)[0],
                           msg=f"символа «{ch}» (U+{ord(ch):04X}) нет в шрифте {font}: будет квадрат — {', '.join(sorted(names)[:4])}"))
    # плашки одновременно и внахлест
    for i, a in enumerate(ws):
        for b in ws[i + 1:]:
            lo, hi = max(a['st'], b['st']), min(a['en'], b['en'])
            if hi - lo < 0.3: continue
            T = (lo + hi) / 2; ma, _ = mask_at(cut, a, T); mb, _ = mask_at(cut, b, T)
            if ma.mean() > 0.5 or mb.mean() > 0.5: continue
            inter = (ma & mb).sum(); small = max(1, min(ma.sum(), mb.sum()))
            if inter / small > 0.02:
                issues.append(dict(level='review', code='overlap', t=round(T, 1), what=f"{a['name']}+{b['name']}",
                                   msg=f"{a['name']} и {b['name']} {T:.1f} с: плашки внахлест ({inter / small * 100:.0f} %)"))
    return issues, len(ws)


ZOOM_REVIEW, ZOOM_FAIL = 1.20, 1.25   # 1,2× — в кадре 69 % картинки; больше 1,25× (меньше 64 %) — «обрезает большую часть кадра»


def crop_rect(z, cx, cy, iw, ih, W=1920, H=1080):
    """Тот же расчет кадрирования, что в cut.Still.next: прямоугольник картинки, который попадает в кадр."""
    cw = iw / z; ch = cw * H / W
    if ch > ih: ch = ih; cw = ch * W / H
    x0 = min(max(cx * iw - cw / 2, 0), iw - cw); y0 = min(max(cy * ih - ch / 2, 0), ih - ch)
    return x0, y0, x0 + cw, y0 + ch


def check_zoom(cut, shots, pack):
    """Наезды на кадры-картинки: сколько картинки остается в кадре и не режет ли край кадра головы."""
    from imgutils.detect import detect_heads
    from PIL import ImageDraw
    issues = []; heads_cache = {}
    for s in shots:
        c = cut.CLIPS[s['name']]
        if c['file'].endswith('.mp4') or 'pose' not in s: continue
        f = cut.P(c['file']); a, b = s['pose']; zmax = max(a[0], b[0])
        if f not in heads_cache:
            im = Image.open(f).convert('RGB'); sc = 1280 / im.width; sm = im.resize((1280, int(im.height * sc)))
            hs = [tuple(v / sc for v in box) for box, _, _ in detect_heads(sm, conf_threshold=0.35)]
            hs = [h for h in hs if (h[2] - h[0]) >= 0.02 * im.width]   # мелкие «головы» (фонари, пуговицы) — не головы
            heads_cache[f] = (im.size, hs, sm, sc)
        (iw, ih), heads, sm, sc = heads_cache[f]
        what = f"{s['name']}@{s['line']}"; probs = []; lvl = None
        if zmax > ZOOM_FAIL: lvl = 'fail'; probs.append(f'зум {zmax:.2f}× — в кадре {100 / zmax ** 2:.0f} % картинки')
        elif zmax > ZOOM_REVIEW + 1e-6: lvl = 'review'; probs.append(f'зум {zmax:.2f}× — в кадре {100 / zmax ** 2:.0f} % картинки')
        for pose in (a, b):
            x0, y0, x1, y1 = crop_rect(*pose, iw, ih)
            for hx0, hy0, hx1, hy1 in heads:
                area = max(1, (hx1 - hx0) * (hy1 - hy0))
                inside = max(0, min(x1, hx1) - max(x0, hx0)) * max(0, min(y1, hy1) - max(y0, hy0)) / area
                if 0.15 < inside < 0.85:
                    lvl = 'fail'; probs.append(f'край кадра режет голову ({inside * 100:.0f} % в кадре)')
                elif inside <= 0.15 and pose[0] > 1.0:
                    lvl = lvl or 'review'; probs.append('персонаж ушел за край кадра')
        if not probs: continue
        ev = sm.copy(); d = ImageDraw.Draw(ev)
        for pose, col in ((a, (60, 220, 60)), (b, (230, 60, 60))):
            d.rectangle([v * sc for v in crop_rect(*pose, iw, ih)], outline=col, width=5)
        for hb in heads: d.rectangle([v * sc for v in hb], outline=(255, 220, 0), width=3)
        name = f"zoom_{s['name']}_{s['line']}.jpg"; ev.save(os.path.join(pack, name), quality=82)
        issues.append(dict(level=lvl, code='zoom', what=what, t=round(s['t'], 1), image=name,
                           msg=f"{what} {s['t']:.1f} с: " + '; '.join(dict.fromkeys(probs)) + ' (зелёная рамка — начало, красная — конец)'))
    return issues


def check_file(video, total):
    FF = __import__('imageio_ffmpeg').get_ffmpeg_exe()
    fc = ('[0:a]ebur128=peak=true,silencedetect=noise=-40dB:d=1.2[a];'
          '[0:v]scale=480:-2,freezedetect=n=-60dB:d=2,blackdetect=d=0.15:pix_th=0.06[v]')
    err = subprocess.run([FF, '-nostats', '-hide_banner', '-i', video, '-filter_complex', fc, '-map', '[a]', '-map', '[v]', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    issues = []
    dur = re.search(r'Duration: (\d+):(\d+):([\d.]+)', err); dur = int(dur.group(1)) * 3600 + int(dur.group(2)) * 60 + float(dur.group(3)) if dur else 0
    summ = err[err.rfind('Summary:'):] if 'Summary:' in err else ''
    I = re.search(r'I:\s+(-?[\d.]+) LUFS', summ); P = re.search(r'Peak:\s+(-?[\d.]+|-inf) dBFS', summ)
    I = float(I.group(1)) if I else None; P = float(P.group(1)) if P and P.group(1) != '-inf' else None
    if I is None: issues.append(dict(level='fail', code='audio', msg='нет звуковой дорожки или ebur128 не посчитал громкость'))
    elif not -16.0 <= I <= -13.0: issues.append(dict(level='fail', code='loudness', msg=f'громкость {I} LUFS, норма −16…−13 (YouTube −14)'))
    if P is not None and P > -1.0: issues.append(dict(level='review', code='peak', msg=f'пик {P} dBTP — выше −1, возможны щелчки после перекодирования'))
    for m in re.finditer(r'silence_start: ([\d.]+)[\s\S]*?silence_end: ([\d.]+) \| silence_duration: ([\d.]+)', err):
        a, b = float(m.group(1)), float(m.group(2))
        if a > 0.5 and b < dur - 3: issues.append(dict(level='review', code='silence', t=round(a, 1), msg=f'тишина {float(m.group(3)):.1f} с на {a:.1f} с'))
    for m in re.finditer(r'freeze_start: ([\d.]+)[\s\S]*?freeze_duration: ([\d.]+)', err):
        a = float(m.group(1))
        if a < dur - 3: issues.append(dict(level='review', code='freeze', t=round(a, 1), msg=f'картинка замерла на {float(m.group(2)):.1f} с с {a:.1f} с (клип короче плана?)'))
    for m in re.finditer(r'black_start:([\d.]+) black_end:([\d.]+)', err):
        a = float(m.group(1))
        if 0.3 < a < dur - 2: issues.append(dict(level='review', code='black', t=round(a, 1), msg=f'черный кадр {a:.1f}–{float(m.group(2)):.1f} с'))
    if total and abs(dur - total) > 0.6: issues.append(dict(level='review', code='length', msg=f'длина файла {dur:.1f} с, по раскладке {total:.1f} с'))
    return issues, dict(duration=round(dur, 2), lufs=I, peak=P)


def main():
    args = sys.argv[1:]
    def opt(n, d=None):
        if n in args: i = args.index(n); v = args[i + 1]; del args[i:i + 2]; return v
        return d
    project = opt('--project'); video = opt('--video'); out = opt('--out', 'render_qa.json'); pack = opt('--pack', 'qa_pack')
    os.makedirs(pack, exist_ok=True)
    issues, n_ov, total = [], 0, 0
    if project and os.path.exists(os.path.join(project, 'cut.py')):   # шортсы собираются другим скриптом — только файл
        cut, shots, total = load(project)
        issues, n_ov = check_overlays(cut, shots, pack)
        issues += check_zoom(cut, shots, pack)
    stats = {}
    if video:
        fi, stats = check_file(video, total); issues += fi
    for z in issues: print(('ОШИБКА ' if z['level'] == 'fail' else 'разбор  ') + z['msg'], flush=True)
    res = dict(project=project, video=video, overlays=n_ov, plan_total=round(total, 2), stats=stats, issues=issues)
    json.dump(res, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    nf = sum(z['level'] == 'fail' for z in issues)
    print(f"\nПлашек {n_ov}: ошибок {nf}, на разбор {len(issues) - nf}. " + (f"Файл: {stats.get('duration')} с, {stats.get('lufs')} LUFS, пик {stats.get('peak')}." if stats else ''))
    sys.exit(1 if nf else 0)


if __name__ == '__main__':
    main()
