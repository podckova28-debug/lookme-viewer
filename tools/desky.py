"""Inpaint every warm-coloured thin thing (rope, chain, hook) in the blue sky above a red dome.
usage: python3 tools/desky.py IN.mp4 OUT.mp4"""
import cv2, numpy as np, subprocess, sys, os
inp, out = sys.argv[1:3]
cap = cv2.VideoCapture(inp); fps = cap.get(5); W = int(cap.get(3)); H = int(cap.get(4))
tmp = out + '.v.mp4'; wr = cv2.VideoWriter(tmp, cv2.VideoWriter_fourcc(*'mp4v'), fps, (W, H)); hit = 0; n = 0
while True:
    ok, f = cap.read()
    if not ok: break
    b, g, r = [f[:, :, i].astype(int) for i in range(3)]
    red = (r > 150) & (g < 90) & (b < 90)
    ys, xs = np.where(red)
    if len(ys) > 200:
        top = np.percentile(ys, 1); cx = int(np.median(xs))
        warm = (r > b + 8) & (r > 45)
        m = np.zeros((H, W), np.uint8)
        y1 = int(max(0, top - 4)); x0, x1 = max(0, cx - 200), min(W, cx + 200)
        m[:y1, x0:x1] = (warm[:y1, x0:x1] * 255).astype(np.uint8)
        if m.any():
            hit += 1; m = cv2.dilate(m, np.ones((5, 5), np.uint8)); f = cv2.inpaint(f, m, 5, cv2.INPAINT_TELEA)
    wr.write(f); n += 1
wr.release()
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp, '-i', inp, '-map', '0:v', '-map', '1:a?', '-c:v', 'libx264', '-crf', '17', '-pix_fmt', 'yuv420p', '-c:a', 'copy', out], check=True)
os.remove(tmp); print(out, hit, n)
