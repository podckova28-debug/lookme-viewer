"""Paint out a coloured mark (e.g. a green print on a cake) inside a box.

For each shot range: pixels in BOX that match the HSV range are dilated, and
replaced either from a clean plate (a frame of the same static shot before the
mark appeared, aligned by phase correlation) or, if no plate is given, by
row-wise interpolation (keeps horizontal tier lines). Only pixels inside the
object's light silhouette (low saturation, bright, holes filled) are touched. Audio is copied unchanged.

usage: clean_mark.py IN OUT --shot F0 F1 X0 Y0 X1 Y1 [PLATE_FRAME] ... [--hsv h0 s0 v0 h1 s1 v1]
"""
import argparse, subprocess, cv2, numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('inp'); ap.add_argument('out')
ap.add_argument('--shot', nargs='+', action='append', type=int, required=True)
ap.add_argument('--rects', action='append', default=[],
                help='per --shot, in order: object silhouette as x0,y0,x1,y1;... (absolute px)')
ap.add_argument('--hsv', nargs=6, type=int, default=[28, 90, 20, 60, 255, 175])
ap.add_argument('--dilate', type=int, default=4)
a = ap.parse_args()
lo, hi = tuple(a.hsv[:3]), tuple(a.hsv[3:])

frames = []
cap = cv2.VideoCapture(a.inp)
fps = cap.get(cv2.CAP_PROP_FPS)
while True:
    ok, f = cap.read()
    if not ok: break
    frames.append(f)

def silhouette(roi, mark):
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    light = cv2.inRange(hsv, (0, 0, 140), (180, 90, 255)) | mark
    light = cv2.morphologyEx(light, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(light)
    if n < 2: return light
    big = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    sil = (lab == big).astype(np.uint8) * 255
    ff = sil.copy(); h, w = sil.shape
    cv2.floodFill(ff, np.zeros((h + 2, w + 2), np.uint8), (0, 0), 255)
    return sil | cv2.bitwise_not(ff)

def rowfill(roi, m, sil):
    out = roi.astype(np.float32).copy()
    for y in range(roi.shape[0]):
        bad = m[y] > 0
        if not bad.any(): continue
        good = np.nonzero((sil[y] > 0) & ~bad)[0]
        if len(good) < 2: continue
        xs = np.nonzero(bad)[0]
        for c in range(3):
            out[y, xs, c] = np.interp(xs, good, out[y, good, c])
    return out

k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * a.dilate + 1,) * 2)
for si, s in enumerate(a.shot):
    f0, f1, x0, y0, x1, y1 = s[:6]
    rect_sil = None
    if si < len(a.rects) and a.rects[si]:
        rect_sil = np.zeros((y1 - y0, x1 - x0), np.uint8)
        for r in a.rects[si].split(';'):
            rx0, ry0, rx1, ry1 = map(int, r.split(','))
            rect_sil[ry0 - y0:ry1 - y0, rx0 - x0:rx1 - x0] = 255
    plate = frames[s[6]][y0:y1, x0:x1].astype(np.float32) if len(s) > 6 else None
    for i in range(f0, min(f1, len(frames))):
        roi = frames[i][y0:y1, x0:x1]
        m = cv2.inRange(cv2.cvtColor(roi, cv2.COLOR_BGR2HSV), lo, hi)
        if not m.any(): continue
        sil = rect_sil if rect_sil is not None else silhouette(roi, m)
        m = cv2.dilate(m, k) & sil
        if not m.any(): continue
        if plate is not None:
            g1 = cv2.cvtColor(plate.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)
            g2 = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY).astype(np.float32)
            (dx, dy), _ = cv2.phaseCorrelate(g1, g2)
            M = np.float32([[1, 0, dx], [0, 1, dy]])
            src = cv2.warpAffine(plate, M, (x1 - x0, y1 - y0), borderMode=cv2.BORDER_REPLICATE)
        else:
            src = rowfill(roi, m, sil)
        alpha = cv2.GaussianBlur(m.astype(np.float32) / 255, (5, 5), 0)[..., None]
        frames[i][y0:y1, x0:x1] = (roi * (1 - alpha) + src * alpha).clip(0, 255).astype(np.uint8)

h, w = frames[0].shape[:2]
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{w}x{h}',
                      '-r', str(fps), '-i', '-', '-i', a.inp, '-map', '0:v', '-map', '1:a?', '-c:v', 'libx264',
                      '-crf', '16', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-shortest', a.out], stdin=subprocess.PIPE)
for f in frames: p.stdin.write(f.tobytes())
p.stdin.close(); p.wait()
