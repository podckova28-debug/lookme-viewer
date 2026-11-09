"""Automatic QC for generated clips: finds the kinds of defects we kept missing by eye.

usage: python3 tools/qc/qc_clip.py CLIP.mp4 [CLIP2.mp4 ...] --out DIR [--prev PREV_CLIP.mp4] [--prompt PROMPT.txt]

For every clip it writes into DIR/<clip>/:
  shot_XX.jpg   contact sheet of each shot, 4 frames/s, 640 px wide, timecodes burned in (for the visual review)
  flag_*.jpg    before/after pairs for every automatic flag
  report.json   shots + flags
and DIR/report.html with everything on one page.

Automatic flags (numbers measured on a 320x180 grey/HSV copy):
  JUMP       a frame-to-frame change inside a shot far above the shot's normal motion -> morph, teleport, pop
  FROZEN     >= 0.9 s with almost no motion -> stuck pose, "static in flight", dead air
  IN_PLACE   lots of motion but its centre does not travel for >= 2 s -> walking/running in place
  COLOR_BLOB a saturated colour area that was not in the shot's first frame grows big -> red face mask, colour spill
  BG_DRIFT   static-camera shot whose background edges differ start vs end -> scenery/props changing
  SEAM       first frame differs a lot from the previous clip's last frame (when --prev is given)
These are hints, not verdicts: lightning, fire and real camera moves can trigger them. The visual checklist
(tools/qc/CHECKLIST.md) is still applied to every sheet.
"""
import argparse, json, os, subprocess, html
import cv2, numpy as np

FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'


def read_small(path, w=320, h=180):
    cap = cv2.VideoCapture(path); fps = cap.get(cv2.CAP_PROP_FPS) or 24
    fr = []
    while True:
        ok, f = cap.read()
        if not ok: break
        fr.append(cv2.resize(f, (w, h), interpolation=cv2.INTER_AREA))
    return np.array(fr), fps


def shots_of(gray, fps):
    d = np.abs(np.diff(gray.astype(np.int16), axis=0)).mean(axis=(1, 2))
    med = np.median(d) + 1e-3
    cuts = [i + 1 for i, v in enumerate(d) if v > max(22, 7 * med)]
    b = [0] + cuts + [len(gray)]
    return [(b[k], b[k + 1]) for k in range(len(b) - 1) if b[k + 1] - b[k] >= 3], d


def analyse(path, prev=None):
    fr, fps = read_small(path)
    n = len(fr); gray = np.array([cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in fr])
    hsv = np.array([cv2.cvtColor(f, cv2.COLOR_BGR2HSV) for f in fr])
    shots, d = shots_of(gray, fps)
    flags = []
    T = lambda i: round(i / fps, 2)
    for s0, s1 in shots:
        dd = d[s0:s1 - 1]
        if len(dd) < 4: continue
        base = np.median(dd) + 0.3
        # JUMP (bursts within 0.5 s are merged into one flag)
        js = [k for k, v in enumerate(dd) if v > max(9, 5 * base) and k > 0]
        grp = []
        for k in js:
            if grp and k - grp[-1][-1] <= fps / 2: grp[-1].append(k)
            else: grp.append([k])
        for gk in grp:
            k = gk[0]; v = float(max(dd[j] for j in gk)); dur = (gk[-1] - gk[0] + 1) / fps
            flags.append(dict(type='JUMP', t=T(s0 + k), f=s0 + k, value=round(v, 1),
                              note=f'резкое изменение кадра ({len(gk)} раз за {dur:.1f} с, до {v:.0f} при норме {base:.1f}): морф, телепорт, вспышка или быстрое действие'))
        # FROZEN
        run = 0
        for k, v in enumerate(list(dd) + [99]):
            if v < 0.45: run += 1
            else:
                if run >= 0.9 * fps:
                    flags.append(dict(type='FROZEN', t=T(s0 + k - run), f=s0 + k - run, dur=round(run / fps, 2),
                                      note=f'{run / fps:.1f} с почти без движения: застывшая поза или пустой кадр'))
                run = 0
        # IN_PLACE: motion centroid
        cen, en = [], []
        for i in range(s0 + 2, s1):          # i vs i-2: generated cartoons are often animated on twos
            m = cv2.absdiff(gray[i], gray[i - 2]) > 18
            e = m.mean(); en.append(e)
            ys, xs = np.nonzero(m)
            cen.append((xs.mean(), ys.mean()) if len(xs) > 30 else (np.nan, np.nan))
        cen = np.array(cen); en = np.array(en); win = int(2 * fps)
        k = 0
        while k + win <= len(en):
            seg = cen[k:k + win]; ok = ~np.isnan(seg[:, 0])
            if en[k:k + win].mean() > 0.01 and ok.sum() > win * 0.5:
                sx = np.nanpercentile(seg[ok, 0], 90) - np.nanpercentile(seg[ok, 0], 10)
                sy = np.nanpercentile(seg[ok, 1], 90) - np.nanpercentile(seg[ok, 1], 10)
                if sx < 12:   # horizontal travel of the moving part < 4% of the width in 2 s
                    flags.append(dict(type='IN_PLACE', t=T(s0 + k), f=s0 + k, dur=2.0,
                                      note='много движения, но центр движения не смещается: шаг или полёт на месте?'))
                    k += win; continue
            k += max(1, win // 2)
        # COLOR_BLOB: a grid cell (20x20 px of 320x180) that turns one saturated hue it did not have at shot start
        def cells(h):
            sat = (h[..., 1] > 120) & (h[..., 2] > 90); hh = h[..., 0].astype(int); hh[hh >= 172] = 0
            hb = hh // 8                                   # 16-degree bins, so red and orange hair/skin differ
            return np.stack([(sat & (hb == b)).reshape(9, 20, 16, 20).mean(axis=(1, 3)) for b in range(22)])
        c0 = cells(hsv[s0]); hit = None
        for i in range(s0 + 2, s1, 2):
            c = cells(hsv[i])
            near = np.stack([cv2.dilate((c0[b] > 0.1).astype(np.uint8), np.ones((3, 3))) for b in range(22)]) > 0
            g = (c > 0.6) & ~near                          # new colour with none of it nearby at shot start
            if g.any() and i + int(fps / 2) < s1:
                c2 = cells(hsv[i + int(fps / 2)]); g = g & (c2 > 0.5)   # and it stays for 0.5 s
            else:
                g = g & False
            if g.any():
                b, y, x = [int(v[0]) for v in np.nonzero(g)]
                hit = (i, b, x, y, int(g.sum())); break
        if hit:
            flags.append(dict(type='COLOR_BLOB', t=T(hit[0]), f=hit[0], value=hit[4],
                              note=f'в зоне x≈{hit[2] * 20 / 320:.0%} y≈{hit[3] * 20 / 180:.0%} появилось новое насыщенное пятно (оттенок {hit[1] * 16}°): маска на лице, заливка, огонь?'))
        # BG_DRIFT: only if the camera is static (border motion small on average)
        if s1 - s0 > fps:
            e0 = cv2.Canny(gray[s0], 60, 140) > 0; e1 = cv2.Canny(gray[s1 - 1], 60, 140) > 0
            band = np.zeros_like(e0); band[:40] = 1; band[:, :40] = 1; band[:, -40:] = 1
            a, bb = e0 & (band > 0), e1 & (band > 0)
            a = cv2.dilate(a.astype(np.uint8), np.ones((5, 5))) > 0
            inter = (a & bb).sum(); den = max(1, bb.sum())
            if den > 200 and inter / den < 0.45:
                flags.append(dict(type='BG_DRIFT', t=T(s1 - 1), f=s1 - 1, value=round(inter / den, 2),
                                  note=f'фон по краям кадра совпадает с началом шота только на {inter / den * 100:.0f}%: окружение поменялось или камера уехала'))
    if prev:
        pf, _ = read_small(prev)
        if len(pf):
            g0 = cv2.cvtColor(pf[-1], cv2.COLOR_BGR2GRAY); g1 = gray[0]
            v = float(np.abs(g0.astype(int) - g1.astype(int)).mean())
            if v > 18:
                flags.append(dict(type='SEAM', t=0.0, f=0, value=round(v, 1),
                                  note=f'первый кадр сильно отличается от конца предыдущего клипа ({v:.0f}): стык виден'))
    return dict(clip=path, fps=fps, frames=n, shots=[(T(a), T(b)) for a, b in shots],
                shot_frames=shots, flags=sorted(flags, key=lambda x: x['t']))


def sheets(path, rep, outdir):
    os.makedirs(outdir, exist_ok=True); files = []
    for k, (a, b) in enumerate(rep['shots']):
        t, part = a, 0
        while t < b - 0.05:                       # one 4x5 sheet = 5 s at 4 frames/s, long shots get several sheets
            seg = min(5.0, b - t); part += 1
            o = f'{outdir}/shot_{k + 1:02d}' + (f'_{part}' if b - a > 5.0 else '') + '.jpg'
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-t', str(max(0.3, seg)), '-i', path, '-vf',
                            f"fps=4,scale=640:-1,drawtext=fontfile={FONT}:text='%{{pts\\:hms\\:{t:.3f}}}':x=6:y=6:fontsize=20:fontcolor=yellow:borderw=2,tile=4x5",
                            '-frames:v', '1', o], check=True)
            files.append(o); t += 5.0
    cap = cv2.VideoCapture(path)
    for j, fl in enumerate(rep['flags']):
        f = fl['f']; pair = []
        for g in (max(0, f - 6), f, min(rep['frames'] - 1, f + 6)):
            cap.set(cv2.CAP_PROP_POS_FRAMES, g); ok, im = cap.read()
            if ok: pair.append(cv2.resize(im, (480, 270)))
        if pair:
            o = f'{outdir}/flag_{j + 1:02d}_{fl["type"]}.jpg'; cv2.imwrite(o, np.hstack(pair)); fl['img'] = os.path.basename(o)
    return files


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('clips', nargs='+'); ap.add_argument('--out', required=True)
    ap.add_argument('--prev', default=None); ap.add_argument('--prompt', default=None); a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True); allr = []
    for c in a.clips:
        prev = a.prev if c == a.clips[0] else None
        name = os.path.splitext(os.path.basename(c))[0]; od = os.path.join(a.out, name)
        r = analyse(c, prev); r['sheets'] = [os.path.basename(x) for x in sheets(c, r, od)]
        r['prompt'] = open(a.prompt).read() if a.prompt else ''
        r.pop('shot_frames'); json.dump(r, open(f'{od}/report.json', 'w'), ensure_ascii=False, indent=1)
        allr.append((name, r))
        print(f'{name}: {len(r["shots"])} shots, {len(r["flags"])} flags')
        for fl in r['flags']: print(f'   {fl["t"]:6.2f}s {fl["type"]:10s} {fl["note"]}')
    h = ['<html><meta charset="utf-8"><body style="font-family:sans-serif;background:#111;color:#eee">']
    for name, r in allr:
        h.append(f'<h2>{html.escape(name)}</h2><p>шоты: {r["shots"]}</p><ul>')
        for fl in r['flags']:
            h.append(f'<li><b>{fl["t"]} с · {fl["type"]}</b>: {html.escape(fl["note"])}<br>'
                     + (f'<img src="{name}/{fl["img"]}" width="1100">' if fl.get('img') else '') + '</li>')
        h.append('</ul>' + ''.join(f'<img src="{name}/{s}" width="1100"><br>' for s in r['sheets']))
    h.append('</body></html>'); open(os.path.join(a.out, 'report.html'), 'w').write('\n'.join(h))


if __name__ == '__main__':
    main()
