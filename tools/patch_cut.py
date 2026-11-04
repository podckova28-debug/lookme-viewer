"""Swap fixed versions of shots into a finished cut without rebuilding it. Free.

usage: python3 tools/patch_cut.py CUT.mp4 OUT.mp4 OLD1.mp4:NEW1.mp4[@FRAME] [OLD2.mp4:NEW2.mp4 ...] [--xfade 7]

Each OLD clip is the exact clip that went into CUT (same size/fps, overlays included); NEW is the fixed one
(same length; a shorter NEW repeats its last frame). The position of OLD in CUT is found by frame matching.
In crossfade frames at both ends the change is blended in (CUT + a*(NEW-OLD)), so dissolves stay intact;
where the cut frame equals the OLD frame (a hard cut) the NEW frame is used as is.
Audio is copied from CUT untouched.
"""
import argparse, subprocess, numpy as np, cv2

ap = argparse.ArgumentParser()
ap.add_argument('cut'); ap.add_argument('out'); ap.add_argument('pairs', nargs='+')
ap.add_argument('--xfade', type=int, default=7)
a = ap.parse_args()

def read_all(p, size=None):
    c = cv2.VideoCapture(p); fs = []
    while True:
        ok, f = c.read()
        if not ok: break
        fs.append(cv2.resize(f, size) if size else f)
    return fs

small = (192, 108)
cut_small = np.stack([f.astype(np.int16) for f in read_all(a.cut, small)])
cap = cv2.VideoCapture(a.cut); fps = cap.get(5); W = int(cap.get(3)); H = int(cap.get(4)); N = len(cut_small)

jobs = []
for pr in a.pairs:
    at = None
    if '@' in pr: pr, at = pr.split('@'); at = int(at)  # OLD:NEW@FRAME forces the position
    old_p, new_p = pr.split(':')
    old = read_all(old_p, small); n_new = int(cv2.VideoCapture(new_p).get(7))
    if at is not None:
        jobs.append({'s0': at, 'L': len(old), 'old_p': old_p, 'new_p': new_p}); print(f'{old_p} at frame {at} (given)'); continue
    mot = [np.abs(old[k + 1].astype(np.int16) - old[k]).mean() for k in range(len(old) - 1)]
    lo_, hi_ = len(old) // 5, len(old) * 4 // 5
    probe = sorted((lo_ + np.argsort(mot[lo_:hi_])[-3:]).tolist())  # moving frames away from the dissolves
    starts = []
    for k in probe:
        o = old[k].astype(np.int16)
        d = np.array([np.abs(c - o).mean() for c in cut_small]); starts.append(int(np.argmin(d)) - k)
    s0 = max(set(starts), key=starts.count)
    if starts.count(s0) < 2: raise SystemExit(f'{old_p}: unclear position {starts}')
    print(f'{old_p} at frame {s0} ({s0 / fps:.2f}s), {len(old)} frames')
    jobs.append({'s0': s0, 'L': len(old), 'old_p': old_p, 'new_p': new_p})

dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', a.cut, '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE)
tmp = a.out + '.v.mp4'
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(fps), '-i', '-',
                        '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
X = a.xfade
for i in range(N):
    f = np.frombuffer(dec.stdout.read(W * H * 3), np.uint8).reshape(H, W, 3)
    for jb in jobs:
        j = i - jb['s0']; L = jb['L']
        if j == 0: jb['o'] = cv2.VideoCapture(jb['old_p']); jb['n'] = cv2.VideoCapture(jb['new_p']); jb['last'] = None
        if 0 <= j < L:
            _, of = jb['o'].read()
            ok, nf = jb['n'].read()
            if ok: jb['last'] = nf
            else: nf = jb['last']
            al = (j + 1) / (X + 1) if j < X else ((L - j) / (X + 1) if j >= L - X else 1.0)
            if al < 1 and np.abs(cv2.resize(f, small).astype(np.int16) - cv2.resize(of, small)).mean() < 4: al = 1.0  # hard cut, no dissolve here
            f = np.clip(f.astype(np.float32) + al * (nf.astype(np.float32) - of.astype(np.float32)), 0, 255).astype(np.uint8)
    enc.stdin.write(f.tobytes())
enc.stdin.close(); enc.wait()
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-i', a.cut, '-map', '0:v', '-map', '1:a', '-c', 'copy', '-movflags', '+faststart', a.out], check=True)
print('ok', a.out)
