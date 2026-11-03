"""Sell an impact between two existing shots, for free: a fast ease-in push toward a point, a white flash, then a
decaying camera shake. Frame count and audio stay exactly the same (frames are replaced, not inserted).

usage: python3 tools/impact.py IN.mp4 OUT.mp4 --push F0 F1 CX CY [--zoom 2.2] [--flash F N] [--shake F0 F1 [--amp 22]]
CX, CY are 0..1 of the frame (the point the camera rushes at).
"""
import argparse, subprocess, tempfile, os, glob, math
from PIL import Image
ap = argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('out')
ap.add_argument('--push', nargs=4, type=float); ap.add_argument('--zoom', type=float, default=2.2)
ap.add_argument('--flash', nargs=2, type=int); ap.add_argument('--shake', nargs=2, type=int); ap.add_argument('--amp', type=float, default=22)
a = ap.parse_args()
tmp = tempfile.mkdtemp()
subprocess.run(['ffmpeg', '-v', 'error', '-i', a.src, '-vsync', '0', f'{tmp}/%05d.png'], check=True)
frames = sorted(glob.glob(f'{tmp}/*.png'))
W, H = Image.open(frames[0]).size
def zoom_at(im, z, cx, cy):
    w, h = W / z, H / z
    l = min(max(cx * W - w / 2, 0), W - w); t = min(max(cy * H - h / 2, 0), H - h)
    return im.crop((int(l), int(t), int(l + w), int(t + h))).resize((W, H), Image.LANCZOS)
for i, f in enumerate(frames):
    im = None
    if a.push and a.push[0] <= i <= a.push[1]:
        k = (i - a.push[0]) / max(1, a.push[1] - a.push[0]); z = 1 + (a.zoom - 1) * k ** 2.2
        im = zoom_at(Image.open(f).convert('RGB'), z, a.push[2], a.push[3])
    if a.flash and a.flash[0] <= i < a.flash[0] + a.flash[1]:
        im = Image.new('RGB', (W, H), (255, 252, 240))
    if a.shake and a.shake[0] <= i <= a.shake[1]:
        k = (i - a.shake[0]) / max(1, a.shake[1] - a.shake[0]); amp = a.amp * (1 - k) ** 1.5
        dx, dy = amp * math.sin(i * 2.7), amp * math.cos(i * 3.9)
        base = Image.open(f).convert('RGB'); s = 1.05
        big = base.resize((int(W * s), int(H * s)), Image.LANCZOS)
        l, t = (big.width - W) / 2 + dx, (big.height - H) / 2 + dy
        im = big.crop((int(l), int(t), int(l) + W, int(t) + H))
    if im is not None: im.save(f)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', '24', '-i', f'{tmp}/%05d.png', '-i', a.src, '-map', '0:v', '-map', '1:a',
                '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-shortest', a.out], check=True)
for f in frames: os.remove(f)
print('ok', a.out, len(frames), 'frames')
