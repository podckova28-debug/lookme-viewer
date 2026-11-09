"""Join finished 1080p blocks into one cut with frame-exact audio.

Each segment's audio is padded or trimmed to exactly its video duration before the join, so sync never drifts.
Loudness: every segment with real sound is normalised to -23 LUFS (two-pass measured gain, no pumping);
silent segments (title cards) stay silent.

usage: python3 tools/assemble.py [--xfade SECS] OUT.mp4 [ID=]SEG1.mp4 [ID=]SEG2.mp4 ...
--xfade: every join becomes a short dissolve (picture and sound) of SECS; prefix an id with ! (e.g. !ff=seg.mp4)
to keep a hard cut into that segment (smash cuts, flash-forwards).
Writes OUT.timeline.json with each segment id, start and duration (for narration mixing).
"""
import sys, subprocess, json, re

def probe(path, stream, key):
    out = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', stream, '-show_entries', f'stream={key}',
                                   '-of', 'csv=p=0', path]).decode().strip()
    return out

def frames(path):
    n = subprocess.check_output(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v', '-show_entries',
                                 'stream=nb_read_frames', '-of', 'csv=p=0', path]).decode().strip()
    return int(n)

def loudness(path):
    err = subprocess.run(['ffmpeg', '-i', path, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    m = re.findall(r'^\s+I:\s+(-?[\d.]+) LUFS', err, re.M)
    return float(m[-1]) if m else -70.0

argv = sys.argv[1:]
X = 0.0
if argv[0] == '--xfade': X = float(argv[1]); argv = argv[2:]
out, raw = argv[0], argv[1:]
hard = [a.startswith('!') for a in raw]; raw = [a.lstrip('!') for a in raw]
ids = [a.split('=', 1)[0] if '=' in a else None for a in raw]
segs = [a.split('=', 1)[1] if '=' in a else a for a in raw]
import tempfile, os
X = round(X * 24) / 24          # whole frames, so dissolves never drift
timeline, items = [], []
total = 0.0
for i, s in enumerate(segs):
    n = frames(s); d = n / 24.0
    total -= X if (i > 0 and X and not hard[i]) else 0.0
    timeline.append({'id': ids[i], 'start': round(total, 3), 'dur': round(d, 3)}); total += d
    lu = loudness(s)
    gain = 0.0 if lu < -60 else max(-12.0, min(15.0, -23.0 - lu))
    items.append({'path': s, 'n': n, 'd': d, 'gain': gain, 'hard': hard[i]})
    print(f'{s.split("/")[-1]:28s} frames={n} dur={d:.3f}s loud={lu:.1f} gain={gain:+.1f}dB')

def join(its, dst, final):
    """One ffmpeg pass over a few inputs: normalise each, then dissolve (or hard-cut) them in order."""
    args, fc = [], ''
    for k, it in enumerate(its):
        args += ['-i', it['path']]
        fc += (f'[{k}:v]scale=1920:1080,setsar=1,fps=24,trim=end_frame={it["n"]},setpts=PTS-STARTPTS,settb=1/24[v{k}];'
               f'[{k}:a]aresample=48000,aformat=channel_layouts=stereo,volume={it["gain"]:.2f}dB,'
               f'apad,atrim=0:{it["d"]:.6f},asetpts=PTS-STARTPTS[a{k}];')
    L = its[0]['d']; cv, ca = '[v0]', '[a0]'
    for k in range(1, len(its)):
        if its[k]['hard'] or not X:
            fc += f'{cv}{ca}[v{k}][a{k}]concat=n=2:v=1:a=1[cc{k}][ca{k}];[cc{k}]settb=1/24,fps=24[cv{k}];'; L += its[k]['d']
        else:
            fc += (f'{cv}[v{k}]xfade=transition=fade:duration={X}:offset={L - X:.6f}[cv{k}];'
                   f'{ca}[a{k}]acrossfade=d={X}:c1=tri:c2=tri[ca{k}];'); L += its[k]['d'] - X
        cv, ca = f'[cv{k}]', f'[ca{k}]'
    fc += f'{cv}null[v];{ca}' + ('alimiter=limit=0.89[ao]' if final else 'anull[ao]')
    enc = (['-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart']
           if final else ['-c:v', 'libx264', '-preset', 'fast', '-crf', '11', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le'])
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *args, '-filter_complex', fc, '-map', '[v]', '-map', '[ao]', *enc, dst], check=True)
    return L

CH = 6   # inputs per pass; 35 decoded 1080p streams in one graph runs out of memory
if len(items) <= CH:
    join(items, out, True)
else:
    tmp = tempfile.mkdtemp(); chunks = []
    for c in range(0, len(items), CH):
        part = items[c:c + CH]; dst = f'{tmp}/c{c:03d}.mkv'
        L = join(part, dst, False)
        chunks.append({'path': dst, 'n': round(L * 24), 'd': round(L * 24) / 24, 'gain': 0.0, 'hard': part[0]['hard']})
    while len(chunks) > CH:   # keep folding if there are very many chunks
        nxt = []
        for c in range(0, len(chunks), CH):
            part = chunks[c:c + CH]; dst = f'{tmp}/m{len(nxt)}_{c:03d}.mkv'
            L = join(part, dst, False); nxt.append({'path': dst, 'n': round(L * 24), 'd': round(L * 24) / 24, 'gain': 0.0, 'hard': part[0]['hard']})
        chunks = nxt
    join(chunks, out, True)
    for f in os.listdir(tmp): os.remove(os.path.join(tmp, f))
v = float(probe(out, 'v', 'duration')); a = float(probe(out, 'a', 'duration'))
print(f'OUT video={v:.3f}s audio={a:.3f}s expected={total:.3f}s')
json.dump(timeline, open(out.rsplit('.', 1)[0] + '.timeline.json', 'w'), indent=1)
