"""Re-aim the hand-drawn arrows baked into frames: erase the old arrow, draw a new ink arrow from the note to the target.
# USER: only f13 (Onesimus) is re-aimed; all other frames keep their original arrows. Run: python3 -c "import arrows; im,_=arrows.fix('f13',*arrows.ARROWS['f13']); im.save('f/f13.jpg',quality=93)"
ARROWS = id: (old_tip_x, old_tip_y, target_x, target_y). python3 arrows.py -> f/<id>.jpg rewritten from raw/<id>.png, review/arrows_*.jpg"""
import numpy as np, math, random
from PIL import Image, ImageDraw
from scipy import ndimage
ARROWS = {
 'g12': (1330, 305, 1285, 300, 'direct'),
 'g01': (1580, 330, 1540, 320, 'direct'),
 'f10': (1690, 245, 1640, 250, 'direct'),
 'b02': (1580, 305, 1540, 335, 'direct'),
 'a02': (1280, 340, 930, 590, 'direct', (1345, 320)), 'a03': (1218, 200, 1148, 360, 'direct', (1290, 125)), 'a05': (1455, 195, 1040, 150, 'direct'), 'a06': (1605, 325, 1475, 335, 'direct'),
 'a10': (1345, 365, 1170, 250), 'b04': (1725, 340, 1560, 520, 'direct'), 'b09': (1490, 195, 1150, 500), 'b10': (1520, 408, 1110, 330, 'direct'),
 'c02': (1175, 248, 615, 200, 'direct'), 'd02': (1262, 172, 850, 220), 'd03': (1510, 155, 1340, 175, 'direct'), 'e01': (1362, 262, 600, 230),
 'e02': (1628, 232, 1400, 560), 'e03': (1293, 355, 1450, 540), 'e08': (1212, 375, 1065, 310, 'direct'), 'f02': (1715, 495, 1610, 535, 'direct', (1760, 420)),
 'f05': (338, 618, 318, 835, 'direct', (300, 470)), 'f06': (1598, 570, 1300, 860, 'direct', (1560, 440)), 'f12': (1462, 198, 1230, 330), 'f13': (1700, 185, 365, 230, 'direct', None, ((1620, 50, 1870, 225), 'Onesimus', (170, 110))),
 'f14': (1642, 318, 1125, 660), 'g02': (1470, 158, 800, 450), 'g04': (1425, 315, 1020, 330), 'g05': (1143, 268, 870, 260),
 'g07': (573, 312, 630, 240, 'direct', (565, 200)), 'g09': (1392, 158, 1270, 230), 'g10': (1680, 537, 1250, 550), 'g13': (1780, 160, 1150, 175, 'direct', None, ((1700, 10, 1890, 205), 'moo?', (1290, 60))),
 'h03': (1632, 192, 900, 450), 'h09': (1402, 200, 955, 220, 'direct'), 'h10': (957, 192, 780, 190), 'h12': (1650, 90, 1240, 880, 'direct', None, ((1440, 30, 1800, 260), '8 May 1980', (1700, 580))),
}
INK = (28, 24, 22)

def fix(i, ox, oy, tx, ty, mode='edge', start=None, label=None):
    im = Image.open(f'raw/{i}.png').convert('RGB').resize((1920, 1080), Image.LANCZOS)
    a = np.asarray(im).astype(int); g = a.mean(2)
    dark = g < 140
    lab, n = ndimage.label(ndimage.binary_dilation(dark, iterations=2))
    ys, xs = np.nonzero(lab)
    d = (xs - ox) ** 2 + (ys - oy) ** 2; k = d.argmin()
    if d[k] > 60 ** 2: return im, f'no arrow near tip'
    arrow = lab == lab[ys[k], xs[k]]
    ay, ax = np.nonzero(arrow)
    if np.ptp(ax) > 600 or np.ptp(ay) > 600 or arrow.sum() > 30000: return im, f'arrow merged with drawing ({np.ptp(ax)}x{np.ptp(ay)})'
    ab = (ax.min(), ay.min(), ax.max(), ay.max())
    # note text = small components near the arrow
    white = ndimage.uniform_filter((g > 235).astype(float), 61)
    sl = ndimage.find_objects(lab); note = None
    for j, s in enumerate(sl, 1):
        if j == lab[ys[k], xs[k]] or s is None: continue
        y0, y1, x0, x1 = s[0].start, s[0].stop, s[1].start, s[1].stop
        if y1 - y0 > 130 or x1 - x0 > 450: continue
        if white[y0:y1, x0:x1].mean() < .9: continue   # text sits on white paper; drawing details don't
        if x1 < ab[0] - 160 or x0 > ab[2] + 160 or y1 < ab[1] - 120 or y0 > ab[3] + 120: continue
        note = (x0, y0, x1, y1) if note is None else (min(note[0], x0), min(note[1], y0), max(note[2], x1), max(note[3], y1))
    # erase arrow
    m = ndimage.binary_dilation(arrow, iterations=7)
    b = a.copy(); b[m] = 255; im = Image.fromarray(b.astype(np.uint8))
    # start: edge of note box closest to target (or old arrow tail)
    if note:
        cx = min(max(tx, note[0]), note[2]); cy = min(max(ty, note[1]), note[3])
        sx, sy = cx, cy
        L = math.hypot(tx - sx, ty - sy) or 1; sx += (tx - sx) / L * 18; sy += (ty - sy) / L * 18
    else:
        far = ((ax - ox) ** 2 + (ay - oy) ** 2).argmax(); sx, sy = ax[far], ay[far]
    if label:   # (erase box, text, centre): wipe the baked note, write it again where it fits
        (x0, y0, x1, y1), text, (lx, ly) = label
        b = np.asarray(im).copy(); b[y0:y1, x0:x1] = 255; im = Image.fromarray(b)
        from PIL import ImageFont
        fnt = ImageFont.truetype('../fonts/CaveatBrush-Regular.ttf', 64)
        ImageDraw.Draw(im).text((lx, ly), text, font=fnt, fill=INK, anchor='mm')
        bb = ImageDraw.Draw(im).textbbox((lx, ly), text, font=fnt, anchor='mm')
        sx = min(max(tx, bb[0]), bb[2]); sy = min(max(ty, bb[1]), bb[3]); L0 = math.hypot(tx - sx, ty - sy) or 1
        sx += (tx - sx) / L0 * 16; sy += (ty - sy) / L0 * 16
    if start: sx, sy = start
    # end: walk BACK from the target toward the note; the tip goes where the subject around the target ends
    g2 = np.asarray(im.convert('L')).astype(int); L = math.hypot(tx - sx, ty - sy); ex, ey = tx, ty; run = 0
    for t in (np.linspace(1, 0, int(L)) if mode == 'edge' else []):
        x, y = int(sx + (tx - sx) * t), int(sy + (ty - sy) * t)
        if (g2[max(0, y - 3):y + 4, max(0, x - 3):x + 4] < 225).sum() == 0:
            run += 1
            if run == 6: ex, ey = x, y; break
        else: run = 0
    L = math.hypot(ex - sx, ey - sy)
    if L < 25: return im, 'too short'
    ux, uy = (ex - sx) / L, (ey - sy) / L; ex, ey = ex - ux * 22, ey - uy * 22   # stop a little short of the subject, like a hand-drawn note
    # hand-drawn curve
    random.seed(i); bend = 0 if i in ('f06',) else random.choice([-1, 1]) * min(60, L * .15)
    px, py = -uy, ux; pts = []
    for t in np.linspace(0, 1, 40):
        w = math.sin(math.pi * t) * bend
        pts.append((sx + (ex - sx) * t + px * w, sy + (ey - sy) * t + py * w))
    dr = ImageDraw.Draw(im)
    hx, hy = pts[-1]; vx, vy = hx - pts[-4][0], hy - pts[-4][1]; vl = math.hypot(vx, vy) or 1; vx, vy = vx / vl, vy / vl
    heads = []
    for sgn in (1, -1):
        c, sn = math.cos(2.55), sgn * math.sin(2.55)
        dx, dy = vx * c - vy * sn, vx * sn + vy * c
        heads.append((hx, hy, hx + dx * 22, hy + dy * 22))
    for col, w in ((INK, 3),):   # thin pen line like the baked-in notes, no halo
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]): dr.line((x0, y0, x1, y1), fill=col, width=w)
        for h in heads: dr.line(h, fill=col, width=w)
        for (x, y) in pts: dr.ellipse((x - w / 2 + .5, y - w / 2 + .5, x + w / 2 - .5, y + w / 2 - .5), fill=col)
    return im, 'ok'

if __name__ == '__main__':
    out = []
    for i, v in ARROWS.items():
        im, st = fix(i, *v); print(i, st)
        if st == 'ok': im.save(f'f/{i}.jpg', quality=93)
        out.append((i, im, st))
    for s in range(0, len(out), 4):
        W = Image.new('RGB', (1920, 1080), 'gray'); D = ImageDraw.Draw(W)
        for k, (i, im, st) in enumerate(out[s:s + 4]):
            W.paste(im.resize((956, 538)), ((k % 2) * 962, (k // 2) * 542)); D.text(((k % 2) * 962 + 6, (k // 2) * 542 + 4), f'{i} {st}', fill='red')
        W.save(f'review/arrows_{s // 4}.jpg', quality=85)
