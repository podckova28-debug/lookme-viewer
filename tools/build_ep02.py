"""Episode 2 (Hulk) final cut from source clips + stills.

- every clip is trimmed from its source (no patched intermediates);
- inside a scene: hard cuts; between scenes and around stills: 0.4 s dissolves;
- one look for the whole episode: per-shot colour match (LAB mean/std) of the wedding shots to the
  wedding start frame, then a mild common grade and a fine film grain, so 720p clips of different
  bitrate and light sit together;
- stills get a slow push-in.
Writes out/e2_cut.mp4 + out/e2_cut.timeline.json (for mix_vo.py).

usage: python3 tools/build_ep02.py STILLS_DIR
"""
import subprocess, json, sys, os
import numpy as np, cv2

STILLS = sys.argv[1]
C = 'assets/ep02/clips/e2_%s_unlim.mp4'
W, H, FPS, XF = 1920, 1080, 24, 10            # XF: dissolve length in frames
REF = cv2.imread('assets/ep02/frames/e2_11_start.png')

# (id, kind, source, in, out, transition-in, colour-match)   kind c=clip s=still
SEQ = [
    ('01', 'c', '01', 0.0, 8.2, 'cut', 0),
    ('02', 'c', '02', 0.4, 6.0, 'cut', 0),
    ('03', 'c', '03', 0.0, 10.08, 'cut', 0),
    ('S1', 's', 'S1.png', 0, 7.0, 'mix', 0),
    ('05a', 'c', '05', 0.0, 4.1, 'mix', 0),
    ('05b', 'c', '05', 7.0, 10.08, 'cut', 0),
    ('04', 'c', '04', 2.6, 10.0, 'mix', 0),
    ('06', 'c', '06', 0.0, 16.9, 'mix', 0),
    ('07', 'c', '07', 0.4, 13.0, 'cut', 0),
    ('08a', 'c', '08', 0.0, 15.9, 'mix', 0),
    ('08b', 'c', '08', 16.0, 20.06, 'cut', 0),
    ('10', 'c', '10', 4.65, 10.08, 'mix', 0),
    ('11', 'c', '11', 0.0, 11.32, 'mix', 1),
    ('12a', 'c', '12', 0.0, 3.74, 'cut', 1),
    ('12b', 'c', '12', 3.75, 10.0, 'cut', 1),
    ('13', 'c', '13', 0.0, 9.34, 'cut', 1),
    ('14', 'c', '14', 0.0, 14.25, 'cut', 1),
]

def lab_stats(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(np.float32)
    return lab.reshape(-1, 3).mean(0), lab.reshape(-1, 3).std(0) + 1e-3
REF_ST = lab_stats(REF)

def shots(frames):
    """split into shots at big frame differences"""
    small = [cv2.resize(f, (160, 90)).astype(np.float32) for f in frames]
    cuts = [0] + [i for i in range(1, len(small)) if np.abs(small[i] - small[i - 1]).mean() > 30] + [len(frames)]
    return list(zip(cuts[:-1], cuts[1:]))

def match(frames, strength=0.65):
    out = []
    for a, b in shots(frames):
        m, s = lab_stats(frames[(a + b) // 2])
        rm, rs = REF_ST
        scale = 1 + strength * (rs / s - 1); shift = strength * (rm - m)
        scale[1:] = np.clip(scale[1:], 0.8, 1.25); scale[0] = np.clip(scale[0], 0.85, 1.2)
        for f in frames[a:b]:
            lab = cv2.cvtColor(f, cv2.COLOR_BGR2LAB).astype(np.float32)
            lab = (lab - m) * scale + m + shift
            out.append(cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR))
    return out

def read_clip(src, t0, t1):
    cap = cv2.VideoCapture(src); cap.set(cv2.CAP_PROP_POS_FRAMES, round(t0 * FPS)); fr = []
    for _ in range(round((t1 - t0) * FPS)):
        ok, f = cap.read()
        if not ok: break
        fr.append(f)
    return fr

def still_frames(path, secs):
    img = cv2.imread(path); img = cv2.resize(img, (W, H), interpolation=cv2.INTER_AREA)
    n = round(secs * FPS); fr = []
    for i in range(n):
        z = 1 + 0.045 * i / max(1, n - 1)
        M = cv2.getRotationMatrix2D((W / 2, H / 2), 0, z)
        fr.append(cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT))
    return fr

rng = np.random.default_rng(7)
GRAIN = [rng.normal(0, 3.2, (H // 2, W // 2)).astype(np.float32) for _ in range(6)]
def finish(f, i):
    if f.shape[1] != W: f = cv2.resize(f, (W, H), interpolation=cv2.INTER_LANCZOS4)
    f = f.astype(np.float32)
    blur = cv2.GaussianBlur(f, (0, 0), 1.2); f = f + 0.35 * (f - blur)          # light, even sharpening
    f = (f - 128) * 1.03 + 128 + 1.5                                              # common contrast
    g = cv2.resize(GRAIN[i % 6], (W, H), interpolation=cv2.INTER_LINEAR)[..., None]
    return np.clip(f + g, 0, 255).astype(np.uint8)

os.makedirs('out', exist_ok=True)
vtmp = 'out/e2_cut_video.mp4'
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS),
                      '-i', '-', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', vtmp], stdin=subprocess.PIPE)
tl, audio, t, fi, tail = [], [], 0.0, 0, []
for bid, kind, src, a, b, tr, cm in SEQ:
    if kind == 'c':
        fr = read_clip(C % src, a, b)
        if cm: fr = match(fr)
        audio.append((C % src, a, b, t, tr))
    else:
        fr = still_frames(os.path.join(STILLS, src), b)
        audio.append((None, 0, b, t, tr))
    fr = [cv2.resize(f, (W, H), interpolation=cv2.INTER_LANCZOS4) for f in fr]
    if tr == 'mix' and tail:
        n = min(XF, len(tail), len(fr))
        for k in range(n):                       # overlap: blend held tail with the new head
            w = (k + 1) / (n + 1)
            fr[k] = cv2.addWeighted(tail[len(tail) - n + k], 1 - w, fr[k], w, 0)
        tail = tail[:len(tail) - n]
        t -= n / FPS; audio[-1] = audio[-1][:3] + (t, tr)
    for f in tail: p.stdin.write(finish(f, fi).tobytes()); fi += 1
    tl.append({'id': bid, 'start': round(t, 3), 'dur': round(len(fr) / FPS, 3)})
    t += len(fr) / FPS
    tail = fr
for f in tail: p.stdin.write(finish(f, fi).tobytes()); fi += 1
p.stdin.close(); p.wait()

# audio: each clip's own sound at its place, 60 ms fades, dissolves crossfade naturally by overlap
ins, parts = [], []
for k, (src, a, b, st, tr) in enumerate(audio):
    if src is None: continue
    fade = 0.4 if tr == 'mix' else 0.06
    ins += ['-ss', str(a), '-t', str(b - a), '-i', src]
    j = len(ins) // 6 - 1
    ms = int(st * 1000)
    parts.append(f'[{j}:a]aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-24:TP=-3,afade=t=in:d={fade},'
                 f'afade=t=out:st={max(0, b - a - 0.08)}:d=0.08,adelay={ms}|{ms}[a{j}]')
n = len(parts)
fc = ';'.join(parts) + ';' + ''.join(f'[a{j}]' for j in range(n)) + f'amix=inputs={n}:normalize=0:dropout_transition=0,apad[aout]'
subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-i', vtmp, '-filter_complex', fc, '-map', f'{n}:v', '-map', '[aout]',
                '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-t', str(round(t, 3)), '-movflags', '+faststart', 'out/e2_cut.mp4'], check=True)
os.remove(vtmp)
json.dump(tl, open('out/e2_cut.timeline.json', 'w'), indent=1)
print('total', round(t, 2))
