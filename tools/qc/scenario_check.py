"""Scenario check: does the clip follow the script shot by shot, does the motion match the verbs, and does the
prompt agree with what already happened in the story (state ledger).

usage:
  # before generating: lint a prompt against the story state and the previous clip's last frame
  python3 tools/qc/scenario_check.py lint PROMPT.txt --ledger LEDGER.json [--prev PREV_CLIP.mp4 --out DIR]
  # after generating: compare the clip with the script
  python3 tools/qc/scenario_check.py check CLIP.mp4 PROMPT.txt --out DIR [--start START_FRAME.png] [--prev PREV_CLIP.mp4]

check writes DIR/board_XX.png ("script vs result": the SHOT text next to the first / middle / last frame of the
matching real shot) and DIR/scenario.md with automatic findings:
  SHOT_COUNT   the clip has more/fewer cuts than the script
  SHOT_TIMING  a cut lands far from the scripted time (times are scaled if the clip is longer than the script)
  CAMERA       the script says static / "same camera" but the frame moves or the layout differs from the start frame
  NO_TRAVEL    the shot text has a travel verb (walks, flies, rises, drives...) but nothing travels across the frame
  DEAD_AIR     a large part of the shot has no motion at all
  TAIL         the clip runs on after the last scripted shot (usually filler: freeze, repeat, improvisation)
lint writes findings when the prompt mentions something the ledger says is gone, destroyed, elsewhere or worn
differently, and extracts the previous clip's last frame so the prompt can be written from what is really there.

LEDGER.json example:
  {"facts": [
     {"what": "hero's yellow hatchback", "state": "destroyed in block 06", "forbid": ["his car", "hatchback", "drives off"]},
     {"what": "hero's clothes", "state": "gray t-shirt + gray sweatpants after block 05", "forbid": ["plaid", "pajama"]}
  ]}
"""
import argparse, json, os, re, sys, subprocess
import cv2, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qc_clip import read_small, shots_of

TRAVEL = r'\b(walks?|walking|runs?|running|flies|flying|flies up|rises?|rising|floats? up|drives?|driving|climbs?|' \
         r'falls?|falling|jumps?|leaps?|steps? (?:back|forward|aside|sideways|into)|moves? (?:to|across)|crosses|' \
         r'shoots? (?:up|straight up)|descends?|lands?|squeezes forward|out of frame|toward the camera)\b'
STATIC = r'(static|locked|no camera move|same camera|exactly (?:the|like the) start frame|start frame camera)'
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'


def parse_shots(text):
    out = []
    for m in re.finditer(r'SHOT\s+(\d+)\s*\(([\d.]+)\s*-\s*([\d.]+)\s*s\)\s*(.*?)(?=\nSHOT\s+\d+|\n\s*\n|\nAUDIO|\Z)', text, re.S):
        body = ' '.join(m.group(4).split())
        out.append(dict(n=int(m.group(1)), t0=float(m.group(2)), t1=float(m.group(3)), text=body,
                        travel=sorted(set(x.lower() for x in re.findall(TRAVEL, body, re.I))),
                        static=bool(re.search(STATIC, body + ' ' + text[:0], re.I) or re.search(r'no camera moves', text, re.I)),
                        same_cam=bool(re.search(r'(exactly (?:the|like the) (?:start frame|first reference)|start frame camera|same camera)', body, re.I))))
    return out


def global_shift(a, b):
    (dx, dy), resp = cv2.phaseCorrelate(np.float32(a), np.float32(b))
    return dx, dy, resp


def layout_sim(a, b):
    ea = cv2.Canny(a, 60, 140) > 0; eb = cv2.Canny(b, 60, 140) > 0
    ea = cv2.dilate(ea.astype(np.uint8), np.ones((5, 5))) > 0
    return (ea & eb).sum() / max(1, eb.sum())


def wrap(t, n=46):
    words, lines, cur = t.split(), [], ''
    for w in words:
        if len(cur) + len(w) + 1 > n: lines.append(cur); cur = w
        else: cur = (cur + ' ' + w).strip()
    if cur: lines.append(cur)
    return lines


def board(path, shot, real, fps, out):
    cap = cv2.VideoCapture(path); ims = []
    a, b = real
    for f in (a, (a + b) // 2, max(a, b - 2)):
        cap.set(cv2.CAP_PROP_POS_FRAMES, f); ok, im = cap.read()
        im = cv2.resize(im, (480, 270)) if ok else np.zeros((270, 480, 3), np.uint8)
        cv2.putText(im, f'{f / fps:.2f}s', (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        ims.append(im)
    from PIL import Image, ImageDraw, ImageFont
    txt = Image.new('RGB', (480, 270), (24, 24, 28)); d = ImageDraw.Draw(txt); f = ImageFont.truetype(FONT, 15)
    y = 8
    for ln in [f"SHOT {shot['n']} ({shot['t0']}-{shot['t1']}s)"] + wrap(shot['text']):
        d.text((8, y), ln, font=f, fill=(240, 240, 240)); y += 19
        if y > 255: break
    row = np.hstack([cv2.cvtColor(np.array(txt), cv2.COLOR_RGB2BGR)] + ims)
    cv2.imwrite(out, row)


def check(a):
    prompt = open(a.prompt).read(); script = parse_shots(prompt)
    fr, fps = read_small(a.clip); gray = np.array([cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in fr])
    real, d = shots_of(gray, fps); dur = len(gray) / fps
    sdur = script[-1]['t1'] if script else dur
    os.makedirs(a.out, exist_ok=True); F = []
    if len(real) != len(script):
        F.append(('SHOT_COUNT', 0, f'в сценарии {len(script)} шотов, в ролике {len(real)} (склейки на ' +
                  ', '.join(f'{s / fps:.2f}' for s, _ in real[1:]) + ' с)'))
    scale = 1.0
    if dur > sdur * 1.3:
        F.append(('TAIL', sdur, f'ролик {dur:.1f} с при сценарии {sdur:.1f} с: после {sdur:.1f} с, скорее всего, наполнитель или самодеятельность модели'))
    start = cv2.cvtColor(cv2.resize(cv2.imread(a.start), (320, 180)), cv2.COLOR_BGR2GRAY) if a.start else None
    for i, sh in enumerate(script):
        if i < len(real): r = real[i]
        else:
            F.append(('SHOT_COUNT', sh['t0'], f'шот {sh["n"]} не найден в ролике')); continue
        if i > 0 and abs(r[0] / fps - sh['t0'] * scale) > 1.0:
            F.append(('SHOT_TIMING', r[0] / fps, f'шот {sh["n"]} начинается в {r[0] / fps:.2f} с вместо {sh["t0"]:.1f} с'))
        g = gray[r[0]:r[1]]
        # camera: accumulated global shift over the shot
        sx = sy = 0.0
        for k in range(2, len(g), 2):
            dx, dy, resp = global_shift(g[k - 2], g[k])
            if resp > 0.2: sx += dx; sy += dy
        if sh['static'] and (abs(sx) > 14 or abs(sy) > 10):
            F.append(('CAMERA', r[0] / fps, f'шот {sh["n"]}: по сценарию камера стоит, а кадр уехал на {sx:+.0f},{sy:+.0f} px (из 320x180)'))
        if sh['same_cam'] and start is not None:
            ls = layout_sim(start, g[0])
            if ls < 0.35:
                F.append(('CAMERA', r[0] / fps, f'шот {sh["n"]}: должен совпадать со стартовым кадром, а совпадение расстановки {ls:.0%}'))
        # travel
        if sh['travel']:
            cen = []
            for k in range(2, len(g)):
                m = cv2.absdiff(g[k], g[k - 2]) > 18; ys, xs = np.nonzero(m)
                if len(xs) > 40: cen.append((xs.mean(), ys.mean()))
            if len(cen) > 6:
                c = np.array(cen); q = max(1, len(c) // 5)
                p0, p1 = c[:q].mean(0), c[-q:].mean(0); dist = np.hypot(*(p1 - p0))
                if dist < 45 and abs(sx) < 14 and abs(sy) < 10:
                    F.append(('NO_TRAVEL', r[0] / fps, f'шот {sh["n"]}: в тексте «{", ".join(sh["travel"])}», но центр движения сместился всего на {dist:.0f} px из 320 и камера не ехала'))
        # dead air
        dd = np.array([np.abs(g[k].astype(np.int16) - g[k - 2]).mean() for k in range(2, len(g))])  # on twos
        if len(dd) > 6:
            dead = (dd < 0.6).mean()
            if dead > 0.4:
                F.append(('DEAD_AIR', r[0] / fps, f'шот {sh["n"]}: {dead:.0%} времени почти нет движения'))
        board(a.clip, sh, r, fps, os.path.join(a.out, f'board_{sh["n"]:02d}.png'))
    if len(real) > len(script):
        for k, r in enumerate(real[len(script):]):
            board(a.clip, dict(n=len(script) + k + 1, t0=round(r[0] / fps, 2), t1=round(r[1] / fps, 2),
                               text='(ЛИШНИЙ ШОТ: в сценарии его нет)'), r, fps, os.path.join(a.out, f'board_{len(script) + k + 1:02d}.png'))
    md = [f'# Сценарий vs ролик: {os.path.basename(a.clip)}', '',
          f'Ролик {dur:.1f} с, шотов {len(real)}; сценарий {sdur:.1f} с, шотов {len(script)}.', '']
    md += [f'- **{t}** {s:.2f} с: {msg}' for t, s, msg in F] or ['- автоматических замечаний нет']
    md += ['', 'Доски «сценарий vs результат»: ' + ', '.join(sorted(x for x in os.listdir(a.out) if x.startswith('board_')))]
    open(os.path.join(a.out, 'scenario.md'), 'w').write('\n'.join(md)); print('\n'.join(md))


def lint(a):
    prompt = open(a.prompt).read(); low = prompt.lower(); F = []
    if a.ledger:
        for fact in json.load(open(a.ledger)).get('facts', []):
            for w in fact.get('forbid', []):
                for m in re.finditer(re.escape(w.lower()), low):
                    neg = low[max(0, m.start() - 60):m.start()]
                    if 'negative' in low[:m.start()].split('\n')[-1] or re.search(r'\b(no|not|never|without)\b[^.]*$', neg):
                        continue
                    F.append(f'«{w}» в промте, а по истории: {fact["what"]} — {fact["state"]}')
    if re.search(r'continue the reference video|sequel|from its very last frame', low) and not a.prev:
        F.append('промт продолжает предыдущий ролик: передай --prev, чтобы сверить его с реальным последним кадром')
    if a.prev:
        os.makedirs(a.out, exist_ok=True); o = os.path.join(a.out, 'prev_last_frame.png')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-sseof', '-0.15', '-i', a.prev, '-frames:v', '1', o], check=True)
        F.append(f'последний кадр предыдущего ролика: {o} — описание начала в промте сверить с ним')
    shots = parse_shots(prompt)
    for s in shots:
        if len(s['text'].split()) > 75:
            F.append(f'SHOT {s["n"]}: {len(s["text"].split())} слов — слишком много действий на один шот, модель их смешает')
        if s['t1'] - s['t0'] < 2.5 and len(re.findall(r'[,;:]', s['text'])) > 4:
            F.append(f'SHOT {s["n"]}: {s["t1"] - s["t0"]:.1f} с на много действий')
    print('\n'.join(f'- {x}' for x in F) or '- замечаний нет')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('mode', choices=['check', 'lint'])
    ap.add_argument('a1'); ap.add_argument('a2', nargs='?')
    ap.add_argument('--out', default='qc_scenario'); ap.add_argument('--start'); ap.add_argument('--prev'); ap.add_argument('--ledger')
    x = ap.parse_args()
    if x.mode == 'check': x.clip, x.prompt = x.a1, x.a2; check(x)
    else: x.prompt = x.a1; lint(x)
