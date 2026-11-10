"""Generic episode cut builder (used from ep5 on): one short clip per scene + stills -> 1080p cut.

SPEC.json:
  {"clips": "assets/ep05/clips/e5_%s.mp4", "stills": "DIR", "out": "out/e5_cut.mp4",
   "seq": [{"id": "01", "src": "01", "in": 0, "out": 5.0, "tr": "cut"|"mix", "slow": 1.0, "zoom": [1.18, 1.0, 0.6]},
           {"id": "S1", "still": "S1.png", "dur": 5.5, "tr": "mix"}, ...]}
- clips are sampled by time, so 24 and 30 fps sources mix freely; "slow" > 1 stretches a scene (sound follows);
- "zoom": [factor, anchor_x 0..1, anchor_y 0..1] crops into the frame (to hide something at an edge);
- cuts inside a place, 0.4 s dissolves between places and around stills; one grade + fine grain over everything.
Writes OUT and OUT's .timeline.json for mix_vo.py.
usage: python3 tools/build_cut.py SPEC.json
"""
import subprocess, json, sys, os
import numpy as np, cv2
spec = json.load(open(sys.argv[1]))
W, H, FPS, XF = 1920, 1080, 24, 10

def read_clip(src, t0, t1, slow):
    cap = cv2.VideoCapture(src); sf = cap.get(cv2.CAP_PROP_FPS) or 24
    frames = []
    while True:
        ok, f = cap.read()
        if not ok: break
        frames.append(f)
    n = round((t1 - t0) * slow * FPS)
    idx = [min(len(frames) - 1, int(round((t0 + k / FPS / slow) * sf))) for k in range(n)]
    return [frames[i] for i in idx]

def zoomed(f, z):
    if not z: return f
    k, ax, ay = z; h, w = f.shape[:2]; cw, ch = int(w / k), int(h / k)
    x0, y0 = int((w - cw) * ax), int((h - ch) * ay)
    return f[y0:y0 + ch, x0:x0 + cw]

def still_frames(path, secs):
    img = cv2.resize(cv2.imread(path), (W, H), interpolation=cv2.INTER_AREA); n = round(secs * FPS); fr = []
    for i in range(n):
        M = cv2.getRotationMatrix2D((W / 2, H / 2), 0, 1 + 0.045 * i / max(1, n - 1))
        fr.append(cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT))
    return fr

rng = np.random.default_rng(7)
GRAIN = [rng.normal(0, 3.0, (H // 2, W // 2)).astype(np.float32) for _ in range(6)]
def finish(f, i):
    f = f.astype(np.float32)
    f = f + 0.35 * (f - cv2.GaussianBlur(f, (0, 0), 1.2))
    f = (f - 128) * 1.03 + 128 + 1.5
    return np.clip(f + cv2.resize(GRAIN[i % 6], (W, H))[..., None], 0, 255).astype(np.uint8)

out = spec['out']; vtmp = out + '.v.mp4'
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS),
                      '-i', '-', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', vtmp], stdin=subprocess.PIPE)
tl, audio, t, fi, tail = [], [], 0.0, 0, []
for s in spec['seq']:
    tr = s.get('tr', 'cut')
    if 'still' in s:
        fr = still_frames(os.path.join(spec['stills'], s['still']), s['dur']); audio.append(None)
    else:
        src = spec['clips'] % s['src']; slow = s.get('slow', 1.0)
        fr = [zoomed(f, s.get('zoom')) for f in read_clip(src, s['in'], s['out'], slow)]
        audio.append([src, s['in'], s['out'], slow, t, tr])
    fr = [cv2.resize(f, (W, H), interpolation=cv2.INTER_LANCZOS4) for f in fr]
    if tr == 'mix' and tail:
        n = min(XF, len(tail), len(fr))
        for k in range(n):
            w = (k + 1) / (n + 1); fr[k] = cv2.addWeighted(tail[len(tail) - n + k], 1 - w, fr[k], w, 0)
        tail = tail[:len(tail) - n]; t -= n / FPS
        if audio[-1]: audio[-1][4] = t
    for f in tail: p.stdin.write(finish(f, fi).tobytes()); fi += 1
    tl.append({'id': s['id'], 'start': round(t, 3), 'dur': round(len(fr) / FPS, 3)})
    t += len(fr) / FPS; tail = fr
for f in tail: p.stdin.write(finish(f, fi).tobytes()); fi += 1
p.stdin.close(); p.wait()

ins, parts = [], []
for a in audio:
    if not a: continue
    src, t0, t1, slow, st, tr = a; j = len(parts); d = (t1 - t0) * slow
    ins += ['-ss', str(t0), '-t', str(t1 - t0), '-i', src]
    tempo = f'atempo={1 / slow:.4f},' if abs(slow - 1) > 0.01 else ''
    fade = 0.4 if tr == 'mix' else 0.06; ms = int(st * 1000)
    parts.append(f'[{j}:a]aresample=48000,aformat=channel_layouts=stereo,{tempo}loudnorm=I=-24:TP=-3,afade=t=in:d={fade},'
                 f'afade=t=out:st={max(0, d - 0.1):.3f}:d=0.1,adelay={ms}|{ms}[a{j}]')
n = len(parts)
fc = ';'.join(parts) + ';' + ''.join(f'[a{j}]' for j in range(n)) + f'amix=inputs={n}:normalize=0:dropout_transition=0,apad[aout]'
subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-i', vtmp, '-filter_complex', fc, '-map', f'{n}:v', '-map', '[aout]',
                '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-t', str(round(t, 3)), '-movflags', '+faststart', out], check=True)
os.remove(vtmp)
json.dump(tl, open(out.rsplit('.', 1)[0] + '.timeline.json', 'w'), indent=1)
print('total', round(t, 2))
