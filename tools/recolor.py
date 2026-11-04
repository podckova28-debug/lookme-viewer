"""Recolor one garment in a clip by hue range (free continuity fix), e.g. a yellow hoodie into a white t-shirt.

usage: python3 tools/recolor.py IN.mp4 OUT.mp4 HUE_LO HUE_HI [--sat 90] [--to white|gray] [--ymax 1.0]
Hues are OpenCV 0..180 (yellow ≈ 18..30). Only pixels in the hue band with saturation above --sat change,
optionally only above a vertical limit (--ymax as fraction of height, to protect e.g. a window).
"""
import argparse, subprocess, numpy as np, cv2
ap = argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('out'); ap.add_argument('lo', type=int); ap.add_argument('hi', type=int)
ap.add_argument('--sat', type=int, default=90); ap.add_argument('--to', default='white'); ap.add_argument('--ymin', type=float, default=0.0)
a = ap.parse_args()
cap = cv2.VideoCapture(a.src); fps = cap.get(cv2.CAP_PROP_FPS); w = int(cap.get(3)); h = int(cap.get(4))
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{w}x{h}', '-r', str(fps), '-i', '-',
                      '-i', a.src, '-map', '0:v', '-map', '1:a?', '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', '-c:a', 'copy', a.out], stdin=subprocess.PIPE)
while True:
    ok, f = cap.read()
    if not ok: break
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    m = ((hsv[..., 0] >= a.lo) & (hsv[..., 0] <= a.hi) & (hsv[..., 1] > a.sat)).astype(np.uint8)
    m[:int(h * a.ymin)] = 0
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    m = cv2.GaussianBlur(m.astype(np.float32), (5, 5), 0)[..., None]
    v = hsv[..., 2:3].astype(np.float32) / 255
    tgt = (np.clip(v * 1.15 + 0.08, 0, 1) * (255 if a.to == 'white' else 170)).repeat(3, 2) * np.array([0.97, 0.98, 1.0])
    f = (f * (1 - m) + tgt * m).astype(np.uint8)
    p.stdin.write(f.tobytes())
p.stdin.close(); p.wait(); print('ok', a.out)
