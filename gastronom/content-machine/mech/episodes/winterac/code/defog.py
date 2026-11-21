"""c4_clear без Wan: туман на лобовом уходит снизу вверх (Wan вместо этого сгущал туман). Кадр kf/k4_clear.png → clips/c4_clear.mp4."""
import numpy as np, subprocess, sys
from PIL import Image, ImageFilter
W, H, FPS, DUR = 1080, 1920, 30, 4.0
im = Image.open('kf/k4_clear.png').convert('RGB').resize((W, H), Image.LANCZOS)
a = np.asarray(im).astype(np.float32)
DASH = float(sys.argv[1]) if len(sys.argv) > 1 else 0.735       # верх торпеды в долях высоты
fog = np.asarray(im.filter(ImageFilter.GaussianBlur(22))).astype(np.float32)
fog = fog * 0.25 + np.array([226, 233, 240], np.float32) * 0.75   # молочная пелена
yy = np.arange(H, dtype=np.float32)[:, None]; xx = np.arange(W, dtype=np.float32)[None, :]
glass = (yy < DASH * H).astype(np.float32)
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                      '-c:v', 'libx264', '-crf', '15', '-preset', 'medium', '-pix_fmt', 'yuv420p', 'clips/c4_clear.mp4'], stdin=subprocess.PIPE)
for i in range(int(DUR * FPS)):
    t = i / FPS
    k = min(1.0, max(0.0, (t - 0.25) / 3.0)); k = k * k * (3 - 2 * k)
    edge = DASH * H - k * (DASH * H + 160) + 28 * np.sin(xx / 140 + t * 2.2)       # волнистая кромка поднимается
    m = np.clip((yy - edge) / 130.0, 0, 1)                                            # 1 — уже чисто (ниже кромки)
    f = glass * (1 - m)
    out = a * (1 - f[..., None]) + fog * f[..., None]
    p.stdin.write(out.clip(0, 255).astype(np.uint8).tobytes())
p.stdin.close(); p.wait(); print('ok')
