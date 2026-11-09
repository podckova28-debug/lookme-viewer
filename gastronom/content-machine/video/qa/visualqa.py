#!/usr/bin/env python3.13
"""Проверка кадров и клипов на мутации без участия человека.

    python3.13 visualqa.py --frames <папка kf | файлы> [--clips <папка clips>] [--manifest shots.json]
                           [--out visual_qa.json] [--pack qa_pack]

Детекторы для рисованных картинок (imgutils/deepghs, CPU, ~1 с на кадр):
  • кто в кадре: люди (detect_person) → сходство персонажа CCIP с эталонами qa/refs/<имя>_N.png.
    Сверка с планом (manifest: cast) — «не тот персонаж» = ошибка (так пойман Михалыч за рулём вместо водителя);
  • руки: на весь кадр и на увеличенный кроп каждого человека; рук больше, чем 2 × людей → на разбор
    (так поймана третья рука Михалыча на щетке в зимнем KG4). Слабые «руки» вне фигуры человека — это рукавицы и
    тряпки, они отбрасываются;
  • текст на кадре: OCR с распознаванием (en_PP-OCRv4_rec), флаг только на читаемое слово от 3 букв
    (логотипы, вывески, английские надписи). Голый детектор текста на рисунке срабатывал на инструменты и иконки;
  • клипы: кадры через 0,5 с + кадры резких скачков движения; персонаж появился/сменился, рук стало больше,
    появился текст → на разбор с временем и подсказкой обрезки `to`.
Смысловой брак (разбитое стекло, снег в салоне, не тот предмет) детекторы не видят: на каждый клип собирается полоса
кадров для обязательного разбора по чек-листу (README «Автопроверка»). В пакет кладутся только кадры с флагами
и полосы клипов, с рамками детекторов и крупными кропами.

manifest (необязательно): {"frames": {"KG1b": {"cast": ["driver"]}, "KC1": {"cast": [], "text_ok": false}},
                           "clips": {"M_G2": {"cast": ["driver"]}}}
Состав можно получить из промптов: make_manifest() — Михалыч по слову «Mikhalych», водитель по «driver»/«young man»,
«No people» → пусто.
"""
import sys, os, re, json, glob, subprocess
import numpy as np, imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont
from imgutils.detect import detect_person, detect_hands
from imgutils.metrics import ccip_extract_feature, ccip_difference
from imgutils.ocr import ocr

HERE = os.path.dirname(os.path.abspath(__file__))
FF = imageio_ffmpeg.get_ffmpeg_exe()
FONT = next((f for f in (os.path.join(HERE, '..', '..', 'mech', 'covers', 'fonts', 'DelaGothicOne.ttf'),
                          '/home/user/gastronom/content-machine/mech/covers/fonts/DelaGothicOne.ttf') if os.path.exists(f)), None)
CCIP_KNOWN = 0.10     # разница CCIP до эталона: меньше — это он
P_THR, H_THR, T_THR = 0.40, 0.30, 0.60
H_STRAY = 0.60      # рука далеко от всех людей ниже этой уверенности — предмет, не рука


def _font(size):
    return ImageFont.truetype(FONT, size) if FONT else ImageFont.load_default(size)


def load_refs():
    refs = {}
    for f in sorted(glob.glob(os.path.join(HERE, 'refs', '*.png'))):
        name = os.path.basename(f).rsplit('_', 1)[0]
        refs.setdefault(name, []).append(ccip_extract_feature(Image.open(f).convert('RGB')))
    return refs


def iou(a, b):
    ix = max(0, min(a[2], b[2]) - max(a[0], b[0])); iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    i = ix * iy; u = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - i
    return i / u if u else 0


def inside(b, k):
    """Доля площади меньшего бокса, лежащая в другом."""
    ix = max(0, min(b[2], k[2]) - max(b[0], k[0])); iy = max(0, min(b[3], k[3]) - max(b[1], k[1]))
    m = min((b[2] - b[0]) * (b[3] - b[1]), (k[2] - k[0]) * (k[3] - k[1]))
    return ix * iy / m if m else 0


def read_text(im):
    out = []
    for b, t, s in ocr(im, recognize_model='en_PP-OCRv4_rec'):
        if s >= T_THR and len(re.findall(r'[A-Za-zА-Яа-яЁё]', t)) >= 3:
            out.append(dict(box=[int(v) for v in b], text=t, score=round(float(s), 2)))
    return out


def analyze(im, refs):
    """Люди с именами, руки, текст на одном кадре (PIL RGB, ≤1280)."""
    W, H = im.size
    persons = []
    for box, _, s in detect_person(im, conf_threshold=P_THR):
        x0, y0, x1, y1 = [int(v) for v in box]
        crop = im.crop((x0, y0, x1, y1))
        d = {k: min(float(ccip_difference(ccip_extract_feature(crop), r)) for r in v) for k, v in refs.items()} if refs else {}
        who = min(d, key=d.get) if d else 'other'
        if d and d[who] > CCIP_KNOWN: who = 'other'
        persons.append(dict(box=[x0, y0, x1, y1], score=round(s, 2), who=who, diff={k: round(v, 3) for k, v in d.items()}))
    hands = [(tuple(b), s) for b, _, s in detect_hands(im, conf_threshold=H_THR)]
    for p in persons:
        x0, y0, x1, y1 = p['box']; pw, ph = x1 - x0, y1 - y0
        x0, y0, x1, y1 = max(0, x0 - .12 * pw), max(0, y0 - .12 * ph), min(W, x1 + .12 * pw), min(H, y1 + .12 * ph)
        crop = im.crop((int(x0), int(y0), int(x1), int(y1))); sc = 1024 / max(crop.size)
        crop = crop.resize((max(1, int(crop.width * sc)), max(1, int(crop.height * sc))))
        for (a0, b0, a1, b1), _, s in detect_hands(crop, conf_threshold=H_THR):
            hands.append(((x0 + a0 / sc, y0 + b0 / sc, x0 + a1 / sc, y0 + b1 / sc), s))
    keep = []
    for b, s in sorted(hands, key=lambda z: -z[1]):
        if all(iou(b, k[0]) < 0.3 and inside(b, k[0]) < 0.6 for k in keep): keep.append((b, s))
    if persons:   # слабая «рука», отделенная от всех людей зазором больше трети своей ширины, — рукавица/тряпка на столе
        def gap(b, p):
            return max(0, p[0] - b[2], b[0] - p[2], p[1] - b[3], b[1] - p[3]) / max(1, min(b[2] - b[0], b[3] - b[1]))
        keep = [(b, s) for b, s in keep if s >= H_STRAY or any(gap(b, p['box']) <= 0.33 for p in persons)]
    return dict(persons=persons, hands=[dict(box=[int(v) for v in b], score=round(s, 2)) for b, s in keep], text=read_text(im))


def judge_frame(a, exp, text_ok=False):
    issues = []
    named = {p['who'] for p in a['persons'] if p['who'] != 'other'}
    if exp is not None:
        wrong = named - set(exp)
        if wrong and exp: issues.append(dict(level='fail', code='cast', msg=f"в кадре {', '.join(sorted(wrong))}, а по плану {', '.join(exp)}"))
        elif wrong: issues.append(dict(level='review', code='cast_extra', msg=f"в кадре {', '.join(sorted(wrong))}, хотя по плану без людей"))
        miss = set(exp) - named
        if miss and a['persons']: issues.append(dict(level='review', code='cast_missing', msg=f"не опознан {', '.join(sorted(miss))} (поза/ракурс?)"))
    n = max(1, len(a['persons']))
    if len(a['hands']) > 2 * n: issues.append(dict(level='review', code='hands', msg=f"рук {len(a['hands'])} на {len(a['persons'])} чел. — проверить лишнюю руку"))
    if a['text'] and not text_ok: issues.append(dict(level='review', code='text', msg='надпись на кадре: ' + ', '.join(f"«{t['text']}»" for t in a['text'][:3])))
    return issues


def draw_boxes(im, a, title=''):
    im = im.copy(); d = ImageDraw.Draw(im); f = _font(18)
    for p in a['persons']:
        d.rectangle(p['box'], outline=(0, 200, 255), width=3); d.text((p['box'][0] + 4, p['box'][1] + 2), p['who'], font=f, fill=(0, 200, 255), stroke_width=2, stroke_fill=(0, 0, 0))
    for i, h in enumerate(a['hands'], 1):
        d.rectangle(h['box'], outline=(255, 60, 60), width=3); d.text((h['box'][0] + 2, h['box'][1] - 20), f'рука {i}', font=f, fill=(255, 80, 80), stroke_width=2, stroke_fill=(0, 0, 0))
    for t in a['text']: d.rectangle(t['box'], outline=(255, 220, 0), width=3)
    if title: d.text((10, 8), title, font=_font(26), fill=(255, 255, 0), stroke_width=3, stroke_fill=(0, 0, 0))
    return im


def clip_frames(path, step=0.5):
    raw = subprocess.run([FF, '-v', 'error', '-i', path, '-vf', 'scale=320:180', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True).stdout
    G = np.frombuffer(raw, np.uint8).reshape(-1, 180, 320).astype(np.float32)
    probe = subprocess.run([FF, '-i', path], capture_output=True, text=True).stderr
    m = re.search(r'(\d+(?:\.\d+)?) fps', probe); fps = float(m.group(1)) if m else 24.0
    d = np.array([np.abs(G[k] - G[k - 1]).mean() for k in range(1, len(G))]); med = float(np.median(d)) or 1e-3
    spikes = sorted({round((k + 1) / fps, 2) for k in np.argsort(-d)[:4] if d[k] / med > 4})
    dur = len(G) / fps
    times = sorted(set([round(t, 2) for t in np.arange(0, dur - 0.05, step)] + spikes))
    return times, spikes, dur


def grab(path, t):
    raw = subprocess.run([FF, '-v', 'error', '-ss', f'{t:.3f}', '-i', path, '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True).stdout
    import io
    im = Image.open(io.BytesIO(raw)).convert('RGB'); im.thumbnail((1280, 1280)); return im


def check_clip(path, refs, exp):
    times, spikes, dur = clip_frames(path)
    rows = []; issues = []; raw = []
    base = None
    for t in times:
        a = analyze(grab(path, t), refs)
        named = sorted({p['who'] for p in a['persons'] if p['who'] != 'other'})
        rows.append(dict(t=t, named=named, hands=len(a['hands']), persons=len(a['persons']), text=[x['text'] for x in a['text']], spike=t in spikes))
        if base is None: base = rows[-1]; continue
        r = rows[-1]
        if exp is not None and set(named) - set(exp):
            who = ', '.join(sorted(set(named) - set(exp)))
            raw.append(('fail', 'cast', t, f"в кадре {who}, а по плану {', '.join(exp)}") if exp else ('review', 'cast_extra', t, f"в кадре {who}, хотя по плану без людей"))
        if r['hands'] > 2 * max(1, r['persons']) and r['hands'] > base['hands']:
            raw.append(('review', 'hands', t, f"рук {r['hands']} на {r['persons']} чел. (в начале {base['hands']})"))
        new = [x for x in r['text'] if x not in base['text']]
        if new: raw.append(('review', 'text', t, 'появилась надпись ' + ', '.join(f'«{x}»' for x in new[:2])))
    # одинаковые флаги — одной строкой с интервалом от первого до последнего случая
    for level, code, t, msg in raw:
        last = next((z for z in reversed(issues) if z['code'] == code), None)
        if last and last['msg0'] == msg: last['t1'] = t; continue
        issues.append(dict(level=level, code=code, t=t, t1=t, msg0=msg))
    for z in issues:
        z['msg'] = (f"{z['t']:.1f}–{z['t1']:.1f} с: " if z['t1'] > z['t'] else f"{z['t']:.1f} с: ") + z.pop('msg0')
    first_bad = min([z['t'] for z in issues], default=None)
    if first_bad is not None and first_bad > 1.0:   # клип хорош до первого флага: подсказка, где обрезать
        for z in issues: z['to'] = round(first_bad - 0.15, 2)
    return dict(dur=round(dur, 2), spikes=spikes, rows=rows, issues=issues)


def strip_times(r):
    """8 равномерных кадров до самого конца клипа (брак чаще в конце) + моменты флагов, затем скачки — не больше 12."""
    base = [round(float(t), 2) for t in np.linspace(0, r['dur'] - 0.1, 8)]
    extra = [z['t'] for z in r['issues']] + [t for t in r['spikes'] if t not in [z['t'] for z in r['issues']]]
    out = list(base)
    for t in extra:
        if len(out) >= 12: break
        if all(abs(t - u) > 0.12 for u in out): out.append(t)
    return sorted(out)


def strip(path, times, title):
    ims = [grab(path, t) for t in times[:12]]
    w, h = 384, 216; s = Image.new('RGB', (w * min(5, len(ims)) + 10, (h + 26) * ((len(ims) + 4) // 5) + 40), (20, 20, 20))
    d = ImageDraw.Draw(s); f = _font(18); d.text((8, 8), title, font=_font(22), fill=(255, 255, 0))
    for i, (im, t) in enumerate(zip(ims, times)):
        x, y = 5 + (i % 5) * w, 40 + (i // 5) * (h + 26)
        s.paste(im.resize((w - 6, h)), (x, y)); d.text((x + 4, y + h + 2), f'{t:.1f} с', font=f, fill=(230, 230, 230))
    return s


def make_manifest(prompts):
    """prompts: {имя: текст промпта} → {имя: {"cast": [...]}} по ключевым словам промпта."""
    out = {}
    for k, p in prompts.items():
        pl = p.lower(); cast = []
        if 'mikhalych' in pl and 'no bearded man' not in pl: cast.append('mikhalych')
        if re.search(r'young (man|driver)|the driver', pl): cast.append('driver')
        if 'no people' in pl: cast = []
        out[k] = dict(cast=cast)
    return out


def main():
    args = sys.argv[1:]
    def opt(n, d=None):
        if n in args: i = args.index(n); v = args[i + 1]; del args[i:i + 2]; return v
        return d
    fr = opt('--frames'); cl = opt('--clips'); man = opt('--manifest'); out = opt('--out', 'visual_qa.json'); pack = opt('--pack', 'qa_pack')
    M = json.load(open(man, encoding='utf-8')) if man else {}
    os.makedirs(pack, exist_ok=True); refs = load_refs(); res = dict(frames={}, clips={})
    files = sorted(glob.glob(os.path.join(fr, '*.png')) + glob.glob(os.path.join(fr, '*.jpg'))) if fr and os.path.isdir(fr) else (fr.split(',') if fr else [])
    for f in files:
        k = os.path.splitext(os.path.basename(f))[0]; spec = M.get('frames', {}).get(k, {})
        im = Image.open(f).convert('RGB'); im.thumbnail((1280, 1280))
        a = analyze(im, refs); iss = judge_frame(a, spec.get('cast'), spec.get('text_ok', False))
        res['frames'][k] = dict(cast=sorted({p['who'] for p in a['persons']}), hands=len(a['hands']), issues=iss)
        if iss: draw_boxes(im, a, f"{k}: " + '; '.join(z['msg'] for z in iss)[:90]).save(os.path.join(pack, f'frame_{k}.jpg'), quality=88)
        print(json.dumps(dict(frame=k, cast=res['frames'][k]['cast'], hands=len(a['hands']), issues=[z['msg'] for z in iss]), ensure_ascii=False), flush=True)
    if cl and os.path.isdir(cl):     # длинные: исходники *_raw.mp4 (рядом лежат апскейлы); шортсы: все клипы
        allc = sorted(glob.glob(os.path.join(cl, '*.mp4'))); cfiles = [f for f in allc if f.endswith('_raw.mp4')] or allc
    else: cfiles = cl.split(',') if cl else []
    for f in cfiles:
        k = os.path.basename(f).replace('_raw.mp4', '').replace('.mp4', ''); spec = M.get('clips', {}).get(k, {})
        r = check_clip(f, refs, spec.get('cast')); res['clips'][k] = r
        times = strip_times(r)
        strip(f, times, f"{k}: " + ('; '.join(z['msg'] for z in r['issues']) or 'флагов нет — проверить по чек-листу')[:110]).save(os.path.join(pack, f'clip_{k}.jpg'), quality=86)
        print(json.dumps(dict(clip=k, spikes=r['spikes'], issues=[z['msg'] + (f" → to={z['to']}" if 'to' in z else '') for z in r['issues']]), ensure_ascii=False), flush=True)
    json.dump(res, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    nf = sum(1 for v in res['frames'].values() if any(z['level'] == 'fail' for z in v['issues']))
    nr = sum(1 for v in res['frames'].values() if v['issues'] and not any(z['level'] == 'fail' for z in v['issues']))
    print(f"\nКадров {len(res['frames'])}: ошибок {nf}, на разбор {nr}. Клипов {len(res['clips'])}: с флагами "
          f"{sum(1 for v in res['clips'].values() if v['issues'])}. Пакет: {pack}/")


if __name__ == '__main__':
    main()
