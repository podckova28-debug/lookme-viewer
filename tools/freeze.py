"""Hold parts of a shot still (frozen-time continuity) while the hero keeps moving. Free.

usage: python3 tools/freeze.py IN.mp4 OUT.mp4 [--keep F0:F1 ...] [--hold F0:F1:X0:Y0:X1:Y1:H ...] [--hero-hue 14:30]
--keep   frame ranges to keep (inclusive, source numbering); dropped frames become a hard cut
--hold   in source frames F0..F1, the box X0,Y0,X1,Y1 (fractions of width/height) is replaced by the same box from frame H,
         except where the hero is (mustard-yellow hoodie, grown to cover head and legs)
"""
import argparse, subprocess, numpy as np, cv2
ap = argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('out')
ap.add_argument('--keep', nargs='*', default=[]); ap.add_argument('--hold', nargs='*', default=[]); ap.add_argument('--hero-hue', default='14:30')
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
out = []
for i, f in enumerate(frames):
    if i not in keep: continue
    g = f.copy()
    act = [x for x in holds if x[0] <= i <= x[1]]
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
