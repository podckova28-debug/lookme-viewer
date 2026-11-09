"""Remove oil bubbles/splashes drawn over the upper cut walls of the cutaway (they must stay inside the crankcase)."""
import sys, subprocess, numpy as np, cv2, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
ci, co = sys.argv[1:3]
cap = cv2.VideoCapture(ci); fr = []
while True:
    ok, f = cap.read()
    if not ok: break
    fr.append(f)
H, W = fr[0].shape[:2]
sil = cv2.imread(ci.replace('.mp4', '_mask.png'), 0) > 128          # block silhouette from clipfix.py
yy, xx = np.mgrid[0:H, 0:W]
zone = sil & (((yy < 845) & ((xx < 250) | (xx > 488))) | ((yy >= 845) & (yy < 930) & ((xx < 175) | (xx > 565))))
zone = cv2.erode(zone.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
def yellow(f):
    h = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    return (h[..., 0] >= 8) & (h[..., 0] <= 40) & (h[..., 1] > 22) & (h[..., 2] > 80)
f0 = fr[0]
# walls are static and splashes are short-lived: the per-pixel median over the clip is a clean wall
clean = np.median(np.stack(fr[::3]), axis=0).astype(np.float32)
# the cut walls are static: inside the wall zone take the clean wall in every frame
Z = cv2.GaussianBlur(zone.astype(np.float32), (5, 5), 0)[..., None]
out = [(f.astype(np.float32) * (1 - Z) + clean * Z).astype(np.uint8) for f in fr]
p = subprocess.Popen([FF, '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', '30', '-i', '-',
                      '-c:v', 'libx264', '-crf', '12', '-pix_fmt', 'yuv420p', co], stdin=subprocess.PIPE)
p.stdin.write(np.stack(out).tobytes()); p.stdin.close(); p.wait()
print('ok', co, len(out))
