"""Freeze a region of a shot to one reference frame (birds, ropes, background extras). Free.

usage: python3 tools/hold_band.py IN.mp4 OUT.mp4 --box X0:Y0:X1:Y1 [--box ...] [--ref 0] [--feather 25] [--hero-col 0.06]

--box       region in fractions of width/height, replaced in every frame by the same region of frame --ref
--hero-col  protect the hero: the largest mustard-hoodie blob in each frame gives a column (its x-range widened
            by this fraction of the width) where the region is NOT replaced, from the top of the frame down.
            Use when the hero's head enters the frozen band. Without it the box is replaced everywhere,
            so pick boxes the hero never enters.
"""
import argparse, subprocess, numpy as np, cv2

ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('out')
ap.add_argument('--box', action='append', required=True)
ap.add_argument('--ref', type=int, default=0)
ap.add_argument('--feather', type=int, default=25)
ap.add_argument('--hero-col', type=float, default=None)
ap.add_argument('--patch', action='append', default=[], help='X0:Y0:X1:Y1:F  take this part of the reference from frame F (e.g. to drop a bird the hero walks through)')
ap.add_argument('--hero-hue', default='14:30')
ap.add_argument('--hero-shape', action='store_true', help='with --hero-col: inside the column keep only warm-coloured pixels (hoodie, skin, hair) that differ from the reference and connect to the hoodie; grey birds stay frozen')
a = ap.parse_args()

cap = cv2.VideoCapture(a.src); fps = cap.get(5)
frames = []
while True:
    ok, f = cap.read()
    if not ok: break
    frames.append(f)
h, w = frames[0].shape[:2]
ref = frames[a.ref].astype(np.float32)
for pt in a.patch:
    x0, y0, x1, y1, F = (float(v) for v in pt.split(':'))
    pm = np.zeros((h, w), np.float32); pm[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)] = 1
    pm = cv2.GaussianBlur(pm, (21, 21), 0)[..., None]
    ref = ref * (1 - pm) + frames[int(F)].astype(np.float32) * pm
base = np.zeros((h, w), np.float32)
for b in a.box:
    x0, y0, x1, y1 = (float(v) for v in b.split(':'))
    base[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)] = 1
k = a.feather * 2 + 1
base = cv2.GaussianBlur(base, (k, k), 0)
lo, hi = (int(v) for v in a.hero_hue.split(':'))


def hero_column(f):
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    m = ((hsv[..., 0] >= lo) & (hsv[..., 0] <= hi) & (hsv[..., 1] > 120) & (hsv[..., 2] > 120)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    if n < 2: return None
    i = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    if st[i, cv2.CC_STAT_AREA] < 0.01 * w * h: return None
    x, bw = st[i, cv2.CC_STAT_LEFT], st[i, cv2.CC_STAT_WIDTH]
    pad = int(a.hero_col * w)
    col = np.zeros((h, w), np.float32); col[:, max(0, x - pad):min(w, x + bw + pad)] = 1
    if not a.hero_shape: return cv2.GaussianBlur(col, (k, k), 0)
    hoodie = (lab == i).astype(np.uint8)
    diff = (np.abs(f.astype(np.int16) - ref.astype(np.int16)).max(axis=2) > 18)
    herocol = ((hsv[..., 0] <= 30) & (hsv[..., 1] > 40)) | (hsv[..., 2] < 95)  # hoodie, skin, dark hair
    near = cv2.dilate(hoodie, np.ones((21, 21), np.uint8))
    cand = ((diff & herocol).astype(np.uint8) | near) * col.astype(np.uint8)
    cand = cv2.morphologyEx(cand, cv2.MORPH_CLOSE, np.ones((11, 11), np.uint8))
    n2, lab2 = cv2.connectedComponents(cand)
    ids = np.unique(lab2[hoodie > 0]); keep = np.isin(lab2, ids[ids > 0]).astype(np.uint8)
    keep = cv2.morphologyEx(keep, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    return cv2.GaussianBlur(keep.astype(np.float32), (7, 7), 0)

tmp = a.out + '.v.mp4'
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{w}x{h}', '-r', str(fps),
                      '-i', '-', '-c:v', 'libx264', '-crf', '12', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
for f in frames:
    m = base
    if a.hero_col is not None:
        col = hero_column(f)
        if col is not None: m = base * (1 - col)
    g = f * (1 - m[..., None]) + ref * m[..., None]
    p.stdin.write(g.astype(np.uint8).tobytes())
p.stdin.close(); p.wait()
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-i', a.src, '-map', '0:v', '-map', '1:a?', '-c', 'copy', a.out], check=True)
print('ok', a.out, len(frames), 'frames')
