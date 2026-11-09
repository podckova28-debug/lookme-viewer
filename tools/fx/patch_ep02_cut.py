"""Edit fixes on the Ep2 rough cut (times are on the cut's own timeline):
- highway: hero's plaid pajama pants -> gray (desaturate blue inside a box);
- park: the intact phone lying on the bench is replaced by a patch from a clean plate of the same frame
  (assets/ep02/frames/park_no_phone.png, phone removed with an image edit; the camera is static);
- kitchen: the moment the flattened toaster is whole again is cut.
usage: patch_ep02_cut.py IN OUT"""
import sys, subprocess, cv2, numpy as np

PANTS = (66.0, 69.7, (500, 560, 840, 815))          # t0, t1, box (1920x1080)
PHONE = (107.0, 110.98, (1262, 858, 1466, 988), 'assets/ep02/frames/park_no_phone.png')  # box, clean plate
CUT = (25.35, 26.40)

def gray_pants(f, box):
    x0, y0, x1, y1 = box
    roi = f[y0:y1, x0:x1]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    hh, ss, vv = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    # the plaid is a dusty lavender (hue ~160-180/0-5, low saturation); road and cars are warm and saturated
    m = (((hh >= 140) | (hh <= 8)) & (ss < 85) & (vv > 55) & (vv < 128)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)       # keep only the pants blob(s), not road speckles
    m = np.isin(lab, [k for k in range(1, n) if st[k, cv2.CC_STAT_AREA] > 1500]).astype(np.uint8)
    ys, xs = np.nonzero(m)
    if len(xs):                                                # legs only: the road shadow spreads sideways
        top = ys < np.percentile(ys, 40)
        cx = np.median(xs[top]) if top.any() else np.median(xs)
        m[:, :max(0, int(cx) - 42)] = 0; m[:, int(cx) + 42:] = 0
    m = cv2.dilate(m, np.ones((3, 3), np.uint8)).astype(np.float32)
    # flat gray sweatpants: the plaid lines are averaged away, the broad shading stays
    gr = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY).astype(np.float32)
    num = cv2.GaussianBlur(gr * m, (0, 0), 6); den = cv2.GaussianBlur(m, (0, 0), 6) + 1e-3
    g = np.clip(num / den * 1.25 + 12, 0, 225)
    g = np.stack([g * 0.98, g * 0.99, g], -1)
    a = cv2.GaussianBlur(m, (5, 5), 0)[..., None]
    roi[:] = (roi * (1 - a) + g * a).astype(np.uint8)

PLATE = {}
def fill_phone(f, box, plate):
    x0, y0, x1, y1 = box
    if 'p' not in PLATE:
        PLATE['p'] = cv2.imread(plate)[y0:y1, x0:x1].astype(np.float32)
        a = np.ones((y1 - y0, x1 - x0), np.float32)
        a = cv2.erode(a, np.ones((17, 17), np.uint8), borderType=cv2.BORDER_CONSTANT, borderValue=0)
        PLATE['a'] = cv2.GaussianBlur(a, (0, 0), 4)[..., None]
    a = PLATE['a']
    f[y0:y1, x0:x1] = (f[y0:y1, x0:x1] * (1 - a) + PLATE['p'] * a).astype(np.uint8)

src, dst = sys.argv[1], sys.argv[2]
cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS); W, H = int(cap.get(3)), int(cap.get(4))
tmp = dst + '.v.mp4'
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(fps),
                      '-i', '-', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
i = 0
while True:
    ok, f = cap.read()
    if not ok: break
    t = i / fps
    if PANTS[0] <= t < PANTS[1]: gray_pants(f, PANTS[2])
    if PHONE[0] <= t < PHONE[1]: fill_phone(f, PHONE[2], PHONE[3])
    if not (CUT[0] <= t < CUT[1]): p.stdin.write(f.tobytes())
    i += 1
p.stdin.close(); p.wait()
a, b = CUT
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-i', src, '-filter_complex',
                f'[1:a]atrim=0:{a},asetpts=PTS-STARTPTS[a1];[1:a]atrim=start={b},asetpts=PTS-STARTPTS[a2];[a1][a2]concat=n=2:v=0:a=1[a]',
                '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-shortest', dst], check=True)
