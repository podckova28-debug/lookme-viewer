"""Re-time a finished cut without re-assembling it: keep, speed up, hold and insert frames. Free.

usage: python3 tools/recut.py IN.mp4 OUT.mp4 EDL.json
EDL.json: list of steps, applied in order, frame numbers of IN (24 fps):
  {"keep": [F0, F1]}                    frames F0..F1 inclusive at normal speed
  {"keep": [F0, F1], "speed": 1.6}      the same frames played faster (frames dropped evenly)
  {"keep": [F0, F1], "hold": 48}        ...then the last frame held for 48 more frames
  {"freeze": F, "frames": 72}           frame F shown for 72 frames (an inserted beat)
Writes OUT (video only) and OUT.map.json: [[in_frame, out_frame], ...] for every kept frame, to move narration.
"""
import sys, json, subprocess, numpy as np

src, out, edlp = sys.argv[1:4]
edl = json.load(open(edlp))
probe = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', src]).decode().strip().split(',')
W, H = int(probe[0]), int(probe[1]); FS = W * H * 3

need = set()
for s in edl:
    if 'freeze' in s: need.add(s['freeze'])
rd = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
wr = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24', '-i', '-',
                       '-c:v', 'libx264', '-preset', 'medium', '-crf', '15', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
cache, pos, last, lastn = {}, 0, None, -1
def frame(n):
    """Frames are read forward only; frames needed later (freezes, read-ahead) are kept in a cache."""
    global pos, last, lastn
    if n in cache: return cache[n]
    if n == lastn: return last
    while pos <= n:
        b = rd.stdout.read(FS)
        if len(b) < FS: raise SystemExit(f'ran out of frames at {pos}')
        if pos in need: cache[pos] = b
        last, lastn = b, pos; pos += 1
    if lastn != n: raise SystemExit(f'frame {n} was already passed')
    return last

# freezes refer to frames that may come later than the current read position: collect them first
order = []
for s in edl:
    if 'keep' in s:
        f0, f1 = s['keep']; n = f1 - f0 + 1; sp = s.get('speed', 1.0)
        m = int(round(n / sp)); idx = [f0 + min(n - 1, int(i * sp)) for i in range(m)]
        order += [('k', i) for i in idx] + [('h', idx[-1])] * s.get('hold', 0)
    else:
        order += [('f', s['freeze'])] * s['frames']
# serve in output order; reading is sequential, so freezes of future frames need a pre-read
mp, outn = [], 0
for kind, f in order:
    if kind == 'f' and f >= pos:
        # read ahead to the freeze frame, keeping every frame on the way for the later 'keep'
        while pos <= f:
            b = rd.stdout.read(FS); cache[pos] = b; pos += 1
    b = cache[f] if f in cache else frame(f)
    if kind == 'k': mp.append([f, outn])
    wr.stdin.write(b); outn += 1
    for k in [k for k in cache if k < f and k not in need]: del cache[k]
wr.stdin.close(); wr.wait()
json.dump(mp, open(out + '.map.json', 'w'))
print('ok', out, outn, 'frames', f'{outn / 24:.2f}s')
