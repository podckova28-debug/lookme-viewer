"""Hold parts of a shot still (frozen-time continuity) while the hero keeps moving. Free.

usage: python3 tools/freeze.py IN.mp4 OUT.mp4 [--keep F0:F1 ...] [--hold F0:F1:X0:Y0:X1:Y1:H ...] [--hero-hue 14:30]
--keep   frame ranges to keep (inclusive, source numbering); dropped frames become a hard cut
--hold   in source frames F0..F1, the box X0,Y0,X1,Y1 (fractions of width/height) is replaced by the same box from frame H,
         except where the hero is (mustard-yellow hoodie, grown to cover head and legs)
"""
import argparse, subprocess, numpy as np, cv2
ap = argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('out')
ap.add_argument('--keep', nargs='*', default=[]); ap.add_argument('--hold', nargs='*', default=[]); ap.add_argument('--hero-hue', default='14:30')
ap.add_argument('--world', nargs='*', default=[], help='F0:F1[:H] strict frozen world: only changes touching the hero survive; H = starting world frame (default F0)')
a = ap.parse_args()
cap = cv2.VideoCapture(a.src); fps = cap.get(5); w = int(cap.get(3)); h = int(cap.get(4))
frames = []
while True:
    ok, f = cap.read()
    if not ok: break
    frames.append(f)
keep = set(range(len(frames))) if not a.keep else {i for r in a.keep for i in range(int(r.split(':')[0]), int(r.split(':')[1]) + 1)}
holds = [tuple(float(v) for v in s.split(':')) for s in a.hold]
lo, hi = (int(v) for v in a.hero_hue.split(':'))
def hero_mask(f):
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    m = ((hsv[..., 0] >= lo) & (hsv[..., 0] <= hi) & (hsv[..., 1] > 120) & (hsv[..., 2] > 120)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    return cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(w * .05), int(h * .26))))

worlds = []
for s_ in a.world:
    v = [int(x) for x in s_.split(':')]; worlds.append((v[0], v[1], v[2] if len(v) > 2 else v[0]))
canvas = {}
out = []
for i, f in enumerate(frames):
    g = f.copy()
    for (f0, f1, H) in worlds:
        if f0 <= i <= f1:
            key = (f0, f1)
            if key not in canvas: canvas[key] = frames[H].astype(np.int16).copy()
            C = canvas[key]; hm = hero_mask(f)
            diff = (np.abs(f.astype(np.int16) - C).max(axis=2) > 28).astype(np.uint8)
            diff = cv2.morphologyEx(diff, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
            n, lab = cv2.connectedComponents(np.maximum(diff, hm))
            touch = np.unique(lab[hm > 0]); live = np.isin(lab, touch[touch > 0]).astype(np.uint8)
            live = cv2.dilate(live, np.ones((5, 5), np.uint8))
            m = cv2.GaussianBlur(live.astype(np.float32), (9, 9), 0)[..., None]
            g = (f * m + C * (1 - m)).astype(np.uint8)
            far = cv2.dilate(hm, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(w * .12), int(h * .12))))
            upd = (live > 0) & (far == 0)
            C[upd] = f[upd]
    if i not in keep: continue
    act = [x for x in holds if x[0] <= i <= x[1]]
    f = g
    if act:
        hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
        hero = ((hsv[..., 0] >= lo) & (hsv[..., 0] <= hi) & (hsv[..., 1] > 120) & (hsv[..., 2] > 120)).astype(np.uint8)
        hero = cv2.dilate(hero, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(w * .06), int(h * .30))))
        for f0, f1, x0, y0, x1, y1, H in act:
            box = np.zeros((h, w), np.float32); box[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)] = 1
            m = cv2.GaussianBlur(box * (1 - hero), (15, 15), 0)[..., None]
            g = (g * (1 - m) + frames[int(H)] * m).astype(np.uint8)
    out.append(g)
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{w}x{h}', '-r', str(fps), '-i', '-',
                      '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', a.out + '.v.mp4'], stdin=subprocess.PIPE)
for g in out: p.stdin.write(g.tobytes())
p.stdin.close(); p.wait()
# audio: same kept ranges
ks = sorted(keep); segs = []; s = ks[0]; prev = s
for k in ks[1:] + [None]:
    if k is None or k != prev + 1: segs.append((s, prev)); s = k
    prev = k if k is not None else prev
fc = ''.join(f'[1:a]atrim={s0 / fps:.4f}:{(s1 + 1) / fps:.4f},asetpts=PTS-STARTPTS[a{j}];' for j, (s0, s1) in enumerate(segs))
fc += ''.join(f'[a{j}]' for j in range(len(segs))) + f'concat=n={len(segs)}:v=0:a=1[a]'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', a.out + '.v.mp4', '-i', a.src, '-filter_complex', fc, '-map', '0:v', '-map', '[a]',
                '-c:v', 'copy', '-c:a', 'aac', '-shortest', a.out], check=True)
print('ok', a.out, len(out), 'frames')
