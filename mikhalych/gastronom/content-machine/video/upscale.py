#!/usr/bin/env python3.13
"""Бесплатный ИИ-апскейл клипов Wan 480p локально: Real-ESRGAN realesr-animevideov3 (модель для рисованного видео), CPU.

    python3.13 upscale.py in.mp4 out.mp4 [WxH=1920x1080] [--to СЕК] [--fp32]

Кадр → ×4 сетью → уменьшение lanczos до WxH → x264 crf 16. Веса realesr-animevideov3.pth (Real-ESRGAN v0.2.5.0, BSD-3, 2,5 МБ)
лежат рядом со скриптом или в $ESRGAN_W; если их нет — скачиваются с GitHub-релиза и сверяются по sha256 (в git не кладём).
Загрузка только тензоров (weights_only=True). Архитектура SRVGGNetCompact переписана здесь, без basicsr.
Нужен torch (CPU) — в контейнере он стоит под python3.13. Сеть считается в bf16 (AMX/AVX512-BF16): на 4 ядрах Xeon
≈0,8 с на кадр 854×480 вместо ≈2 с в fp32, отличие от fp32 — PSNR 48 дБ (на глаз не видно)."""
import os, sys, subprocess, time
import numpy as np, torch, torch.nn as nn, torch.nn.functional as F

class SRVGGNetCompact(nn.Module):
    def __init__(self, num_feat=64, num_conv=16, upscale=4):
        super().__init__(); self.upscale = upscale
        body = [nn.Conv2d(3, num_feat, 3, 1, 1), nn.PReLU(num_parameters=num_feat)]
        for _ in range(num_conv): body += [nn.Conv2d(num_feat, num_feat, 3, 1, 1), nn.PReLU(num_parameters=num_feat)]
        body.append(nn.Conv2d(num_feat, 3 * upscale * upscale, 3, 1, 1))
        self.body = nn.ModuleList(body); self.upsampler = nn.PixelShuffle(upscale)
    def forward(self, x, bf16=True):
        out = x
        with torch.autocast('cpu', dtype=torch.bfloat16, enabled=bf16):  # AMX/AVX512-BF16: в разы быстрее fp32
            for layer in self.body: out = layer(out)
        return self.upsampler(out.float()) + F.interpolate(x, scale_factor=self.upscale, mode='nearest')

URL = 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-animevideov3.pth'
SHA = 'b8a8376811077954d82ca3fcf476f1ac3da3e8a68a4f4d71363008000a18b75d'

def fetch(path):
    import hashlib, urllib.request
    if not os.path.exists(path):
        print('скачиваю веса', URL, flush=True); urllib.request.urlretrieve(URL, path + '.part'); os.replace(path + '.part', path)
    if hashlib.sha256(open(path, 'rb').read()).hexdigest() != SHA: sys.exit(f'{path}: sha256 не совпал — удалите файл')

def load(path):
    fetch(path)
    sd = torch.load(path, map_location='cpu', weights_only=True)
    sd = sd.get('params', sd.get('params_ema', sd))
    m = SRVGGNetCompact(); m.load_state_dict(sd, strict=True); m.eval(); return m.to(memory_format=torch.channels_last)

def probe(f):
    out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,r_frame_rate',
                          '-of', 'csv=p=0', f], capture_output=True, text=True).stdout.strip().split(',')
    w, h = int(out[0]), int(out[1]); a, b = out[2].split('/'); return w, h, float(a) / float(b)

def main():
    argv = sys.argv[1:]; to = None; bf16 = '--fp32' not in argv; argv = [a for a in argv if a != '--fp32']
    if '--to' in argv: i = argv.index('--to'); to = float(argv[i + 1]); del argv[i:i + 2]
    src, dst = argv[0], argv[1]; W, H = map(int, (argv[2] if len(argv) > 2 else '1920x1080').split('x'))
    wpath = os.environ.get('ESRGAN_W', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'realesr-animevideov3.pth'))
    torch.set_num_threads(os.cpu_count() or 4); m = load(wpath)
    w, h, fps = probe(src)
    dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', src, *(['-t', str(to)] if to else []), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                           stdout=subprocess.PIPE)
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{w * 4}x{h * 4}', '-r', str(fps),
                            '-i', '-', '-vf', f'scale={W}:{H}:flags=lanczos', '-c:v', 'libx264', '-crf', '16', '-preset', 'medium',
                            '-pix_fmt', 'yuv420p', dst], stdin=subprocess.PIPE)
    n, t0, sz = 0, time.time(), w * h * 3
    with torch.inference_mode():
        while True:
            buf = dec.stdout.read(sz)
            if len(buf) < sz: break
            x = torch.from_numpy(np.frombuffer(buf, np.uint8).reshape(h, w, 3).copy()).permute(2, 0, 1)[None].float().div(255).contiguous(memory_format=torch.channels_last)
            y = m(x, bf16).clamp(0, 1)[0].permute(1, 2, 0).mul(255).round().byte().numpy()
            enc.stdin.write(y.tobytes()); n += 1
    enc.stdin.close(); enc.wait(); dec.wait()
    print(f'{os.path.basename(src)} → {dst}: {n} кадров, {(time.time() - t0) / max(n, 1):.2f} с/кадр', flush=True)

if __name__ == '__main__': main()
