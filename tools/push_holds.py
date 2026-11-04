"""Turn every frozen stretch of a cut into a slow camera push-in, so held frames never look stuck. Free.

usage: python3 tools/push_holds.py IN.mp4 OUT.mp4 [--min 20] [--zoom 0.07]
A stretch of at least --min frames with no visible change gets a smooth push-in (eased) toward the frame centre,
up to 1+zoom at its end; the next shot starts at normal scale. Audio is copied.
"""
import argparse, subprocess, numpy as np, cv2
ap = argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('out')
ap.add_argument('--min', type=int, default=20); ap.add_argument('--zoom', type=float, default=0.07)
a = ap.parse_args()
cap = cv2.VideoCapture(a.src); W, H = int(cap.get(3)), int(cap.get(4))
sw, sh = 192, 108
small = []
while True:
    ok, f = cap.read()
    if not ok: break
    small.append(cv2.cvtColor(cv2.resize(f, (sw, sh), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY).astype(np.int16))
n = len(small)
still = [False] + [np.abs(small[i] - small[i - 1]).mean() < 0.3 for i in range(1, n)]
runs, i = [], 0
while i < n:
    if still[i]:
        j = i
        while j < n and still[j]: j += 1
        if j - i >= a.min: runs.append((i - 1, j - 1))
        i = j
    else: i += 1
diff = [0.0] + [float(np.abs(small[i] - small[i - 1]).mean()) for i in range(1, n)]
merged = []
for s, e in runs:   # a push never resets inside one shot: runs with no cut between them become one push
    if merged and not any(diff[k] > 12 for k in range(merged[-1][1] + 1, s + 1)): merged[-1] = (merged[-1][0], e)
    else: merged.append((s, e))
runs = merged
scale = np.ones(n)
for s, e in runs:
    L = e - s
    for k in range(L + 1):
        t = k / L; scale[s + k] = 1 + a.zoom * (t * t * (3 - 2 * t))
print('pushes:', ' '.join(f'{s/24:.1f}s+{(e-s)/24:.1f}' for s, e in runs))
cap = cv2.VideoCapture(a.src); tmp = a.out + '.v.mp4'
wr = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', '24', '-i', '-',
                       '-c:v', 'libx264', '-preset', 'medium', '-crf', '15', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
for i in range(n):
    ok, f = cap.read()
    if scale[i] > 1.0001:
        z = scale[i]; M = np.float32([[z, 0, (1 - z) * W / 2], [0, z, (1 - z) * H / 2]])
        f = cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    wr.stdin.write(f.tobytes())
wr.stdin.close(); wr.wait()
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-i', a.src, '-map', '0:v', '-map', '1:a?', '-c', 'copy', a.out], check=True)
print('ok', a.out)
