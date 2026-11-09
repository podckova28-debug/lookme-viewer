"""Ep2 block 12 edit fixes:
- red 'angry' skin -> normal pale skin (hue remap) in the wide shot (face box) and the close-up;
- Dave reverse shot: 1.5x crop on Dave so the extra crowd and the hero's red ear leave the frame.
usage: fix_block12.py IN OUT"""
import sys, subprocess, cv2, numpy as np

def unred(f, box=None, reach=7, smax=255):
    x0, y0, x1, y1 = box or (0, 0, f.shape[1], f.shape[0])
    roi = f[y0:y1, x0:x1]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV).astype(np.float32)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    hd = np.minimum(np.abs(h - 2), 180 - np.abs(h - 2))        # distance from red
    w = np.clip((reach - hd) / 3, 0, 1) * np.clip((s - 60) / 30, 0, 1) * np.clip((smax - s) / 15, 0, 1)
    w = cv2.GaussianBlur(w, (5, 5), 0)
    out = hsv.copy()
    out[..., 0] = 14
    out[..., 1] = np.clip(s * 0.4, 38, 70)
    out[..., 2] = np.minimum(255, v * 1.06 + 8)
    new = cv2.cvtColor(out.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)
    roi[:] = (roi * (1 - w[..., None]) + new * w[..., None]).astype(np.uint8)
    return f

cap = cv2.VideoCapture(sys.argv[1]); fps = cap.get(cv2.CAP_PROP_FPS)
W, H = int(cap.get(3)), int(cap.get(4))
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(fps),
                      '-i', '-', '-i', sys.argv[1], '-map', '0:v', '-map', '1:a?', '-c:v', 'libx264', '-crf', '16',
                      '-pix_fmt', 'yuv420p', '-c:a', 'copy', sys.argv[2]], stdin=subprocess.PIPE)
i = 0
while True:
    ok, f = cap.read()
    if not ok: break
    if i < 90:                       # wide shot: only the hero's face
        f = unred(f, (230, 140, 440, 380))
    elif i < 171:                    # Dave reverse shot: crop the crowd away
        f = cv2.resize(f[40:580, 320:1280], (W, H), interpolation=cv2.INTER_LANCZOS4)
    elif i < 200:                    # close-up, fully red
        f = unred(f)
    elif i < 222:                    # red -> green blend passes through brown: reach further, spare the hair
        f = unred(f, reach=10, smax=190)
    p.stdin.write(f.tobytes()); i += 1
p.stdin.close(); p.wait()
