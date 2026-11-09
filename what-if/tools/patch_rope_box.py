"""Inpaint a reddish rope inside a box from time T onward.
usage: python3 tools/patch_rope_box.py IN OUT T x0 y0 x1 y1   (pixel coords of the source video)"""
import cv2, numpy as np, subprocess, sys, os
inp, out, T = sys.argv[1], sys.argv[2], float(sys.argv[3]); x0, y0, x1, y1 = map(int, sys.argv[4:8])
cap = cv2.VideoCapture(inp); fps = cap.get(5); W = int(cap.get(3)); H = int(cap.get(4))
tmp = out + '.v.mp4'; wr = cv2.VideoWriter(tmp, cv2.VideoWriter_fourcc(*'mp4v'), fps, (W, H)); i = 0
while True:
    ok, f = cap.read()
    if not ok: break
    if i / fps >= T:
        b, g, r = [f[y0:y1, x0:x1, k].astype(int) for k in range(3)]
        m = ((r > 90) & (r > g + 35) & (r > b + 40) & ((r + g + b) < 560)).astype(np.uint8) * 255
        full = np.zeros((H, W), np.uint8); full[y0:y1, x0:x1] = cv2.dilate(m, np.ones((5, 5), np.uint8))
        f = cv2.inpaint(f, full, 6, cv2.INPAINT_TELEA)
    wr.write(f); i += 1
wr.release()
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp, '-i', inp, '-map', '0:v', '-map', '1:a?', '-c:v', 'libx264', '-crf', '17', '-pix_fmt', 'yuv420p', '-c:a', 'copy', out], check=True); os.remove(tmp)
