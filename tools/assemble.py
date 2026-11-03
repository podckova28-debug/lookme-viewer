"""Join finished 1080p blocks into one cut with frame-exact audio.

Each segment's audio is padded or trimmed to exactly its video duration before the join, so sync never drifts.
Loudness: every segment with real sound is normalised to -23 LUFS (two-pass measured gain, no pumping);
silent segments (title cards) stay silent.

usage: python3 tools/assemble.py OUT.mp4 [ID=]SEG1.mp4 [ID=]SEG2.mp4 ...
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

out, raw = sys.argv[1], sys.argv[2:]
ids = [a.split('=', 1)[0] if '=' in a else None for a in raw]
segs = [a.split('=', 1)[1] if '=' in a else a for a in raw]
timeline = []
args, fc, cat = [], '', ''
total = 0.0
for i, s in enumerate(segs):
    n = frames(s); d = n / 24.0
    timeline.append({'id': ids[i], 'start': round(total, 3), 'dur': round(d, 3)}); total += d
    lu = loudness(s)
    gain = 0.0 if lu < -60 else max(-12.0, min(15.0, -23.0 - lu))
    args += ['-i', s]
    fc += (f'[{i}:v]scale=1920:1080,setsar=1,fps=24,trim=end_frame={n},setpts=PTS-STARTPTS[v{i}];'
           f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,volume={gain:.2f}dB,'
           f'apad,atrim=0:{d:.6f},asetpts=PTS-STARTPTS[a{i}];')
    cat += f'[v{i}][a{i}]'
    print(f'{s.split("/")[-1]:28s} frames={n} dur={d:.3f}s loud={lu:.1f} gain={gain:+.1f}dB')
fc += f'{cat}concat=n={len(segs)}:v=1:a=1[v][a];[a]alimiter=limit=0.89[ao]'
subprocess.run(['ffmpeg', '-v', 'error', '-y', *args, '-filter_complex', fc, '-map', '[v]', '-map', '[ao]',
                '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
                '-movflags', '+faststart', out], check=True)
v = float(probe(out, 'v', 'duration')); a = float(probe(out, 'a', 'duration'))
print(f'OUT video={v:.3f}s audio={a:.3f}s expected={total:.3f}s')
json.dump(timeline, open(out.rsplit('.', 1)[0] + '.timeline.json', 'w'), indent=1)
