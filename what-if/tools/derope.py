"""Remove a thin tan rope/cable that a video model hung above an object.
usage: python3 tools/derope.py IN.mp4 OUT.mp4 [--x0 150 --x1 750]
Tracks tan pixels (rope colour) row by row from the top edge down, stops where the blob widens
(knob/dome), masks them and inpaints from the surrounding sky. Audio is copied."""
import cv2, numpy as np, subprocess, sys, argparse
ap = argparse.ArgumentParser(); ap.add_argument('inp'); ap.add_argument('out'); ap.add_argument('--x0', type=int, default=150); ap.add_argument('--x1', type=int, default=750)
a = ap.parse_args()
cap = cv2.VideoCapture(a.inp); fps = cap.get(5); W = int(cap.get(3)); H = int(cap.get(4))
tmp = a.out + '.v.mp4'
wr = cv2.VideoWriter(tmp, cv2.VideoWriter_fourcc(*'mp4v'), fps, (W, H)); n = 0; hit = 0
while True:
    ok, f = cap.read()
    if not ok: break
    b, g, r = [f[:, :, i].astype(int) for i in range(3)]
    tan = (r > 80) & (g > 0.55 * r) & (g > b + 15) & (r > b + 30)
    mask = np.zeros((H, W), np.uint8)
    # start: tan pixels in the top rows
    xs = np.where(tan[2, a.x0:a.x1])[0]
    if len(xs):
        cx = a.x0 + int(np.median(xs))
        for y in range(H):
            lo, hi = max(0, cx - 14), min(W, cx + 15)
            row = np.where(tan[y, lo:hi])[0]
            if len(row) == 0:
                # allow small gaps (rain streaks)
                continue
            if len(row) > 10: break          # reached the knob / dome
            cx = lo + int(np.mean(row)); mask[y, lo + row.min(): lo + row.max() + 1] = 255
        if mask.any():
            hit += 1
            mask = cv2.dilate(mask, np.ones((3, 5), np.uint8))
            f = cv2.inpaint(f, mask, 4, cv2.INPAINT_TELEA)
    wr.write(f); n += 1
wr.release()
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp, '-i', a.inp, '-map', '0:v', '-map', '1:a?', '-c:v', 'libx264', '-crf', '17', '-pix_fmt', 'yuv420p', '-c:a', 'copy', a.out], check=True)
import os; os.remove(tmp); print(f'{a.out}: {hit}/{n} frames cleaned')
