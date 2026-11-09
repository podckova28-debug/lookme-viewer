"""Clip fixes for ep. 13.
  foam:  python3 clipfix.py foam  in.mp4 out.mp4   — everything outside the engine block = clean background
  dip:   python3 clipfix.py dip   in.mp4 out.mp4   — dipstick band + drip column = frame 0 (oil level must not change)"""
import sys, subprocess, numpy as np, cv2, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
mode, ci, co = sys.argv[1:4]
cap = cv2.VideoCapture(ci); fr = []
while True:
    ok, f = cap.read()
    if not ok: break
    fr.append(f)
F = np.stack(fr).astype(np.float32); N, H, W, _ = F.shape
f0 = fr[0]
if mode == 'foam':
    navy = np.median(f0[:H // 8].reshape(-1, 3), axis=0)
    diff = np.abs(f0.astype(np.float32) - navy).max(axis=2)
    nb = (diff > 38).astype(np.uint8)
    nb = cv2.morphologyEx(nb, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(nb)
    blk = np.isin(lab, [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] > 0.01 * H * W]).astype(np.uint8)
    cnts, _ = cv2.findContours(blk, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    fill = np.zeros_like(blk); cv2.drawContours(fill, cnts, -1, 1, -1)
    fill = cv2.dilate(fill, np.ones((5, 5), np.uint8))
    inside = cv2.GaussianBlur(fill.astype(np.float32), (7, 7), 0)[..., None]
    # clean background: inpaint every non-navy pixel of frame 0
    d0 = (np.abs(f0.astype(np.float32) - navy).max(axis=2) > 20).astype(np.uint8)
    d0 = cv2.dilate(d0, np.ones((7, 7), np.uint8))
    bg = cv2.inpaint(f0, d0, 9, cv2.INPAINT_TELEA).astype(np.float32)
    out = F * inside + bg[None] * (1 - inside)
    cv2.imwrite(co.replace('.mp4', '_mask.png'), (inside[..., 0] * 255).astype(np.uint8))
else:
    s = W / 768.0
    m = np.zeros((H, W), np.uint8)
    # band along the dipstick from the hand to the tip (768-scale coords, see fix_dip.py)
    p_hand, p_tip = np.array([400, 700]) * s, np.array([712, 800]) * s
    cv2.line(m, tuple(int(v) for v in p_hand), tuple(int(v) for v in p_tip), 1, int(44 * s))
    cv2.rectangle(m, (int(640 * s), int(770 * s)), (W, H), 1, -1)   # drip column under the tip
    M = cv2.GaussianBlur(m.astype(np.float32), (15, 15), 0)[..., None]
    out = F * (1 - M) + f0.astype(np.float32)[None] * M
    cv2.imwrite(co.replace('.mp4', '_mask.png'), (M[..., 0] * 255).astype(np.uint8))
out = out.clip(0, 255).astype(np.uint8)
p = subprocess.Popen([FF, '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', '30', '-i', '-',
                      '-c:v', 'libx264', '-crf', '12', '-pix_fmt', 'yuv420p', co], stdin=subprocess.PIPE)
p.stdin.write(out.tobytes()); p.stdin.close(); p.wait()
print('ok', co, N, 'frames', W, H)
