"""Lay narration (and optional music bed) over an assembled cut.

usage: python3 tools/mix_vo.py CUT.mp4 OUT.mp4 VO_DIR [--music BED.mp3] [--lead 0.4]
CUT.timeline.json (written by assemble.py) gives each block's start; VO_DIR/vo_<id>.wav is placed at start+lead,
VO_DIR/vo_<id>@<secs>.wav pieces at start+secs. A long line pushes the next one so two lines never overlap.
Block sound is ducked under the voice with a sidechain compressor; music sits at -30 LUFS-ish under everything.
"""
import sys, os, json, argparse, subprocess
ap = argparse.ArgumentParser(); ap.add_argument('cut'); ap.add_argument('out'); ap.add_argument('vo_dir')
ap.add_argument('--music', default=''); ap.add_argument('--lead', type=float, default=0.4)
ap.add_argument('--at', action='append', default=[], help='ID=SECS: start this line SECS into its block instead of --lead')
ap.add_argument('--gap', type=float, default=0.35, help='minimum silence between two lines; a long line pushes the next one')
a = ap.parse_args()
at = {k: float(v) for k, v in (x.split('=', 1) for x in a.at)}
dur = lambda f: float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]))
tl = json.load(open(a.cut.rsplit('.', 1)[0] + '.timeline.json'))
ins, parts = ['-i', a.cut], []
import glob
k = 1; prev_end = 0.0
items = []   # (wanted time, file, block)
for seg in tl:
    if not seg['id']: continue
    f = os.path.join(a.vo_dir, f"vo_{seg['id']}.wav")
    if os.path.exists(f): items.append((seg['start'] + at.get(seg['id'], a.lead), f, seg))
    for g in glob.glob(os.path.join(a.vo_dir, f"vo_{seg['id']}@*.wav")):   # vo_ID@SECS.wav: a piece placed SECS into the block
        items.append((seg['start'] + float(g.rsplit('@', 1)[1][:-4]), g, seg))
for want, f, seg in sorted(items, key=lambda i: i[0]):
        t0 = max(want, prev_end + a.gap); d = dur(f); prev_end = t0 + d
        end_blk = seg['start'] + seg['dur']
        print(f"vo {os.path.basename(f)[3:-4]:10s} at {t0:7.2f}s  len {d:4.1f}s  push {t0 - want:+.1f}s  " + (f"OVER block end by {prev_end - end_blk:.1f}s" if prev_end > end_blk else ''))
        ms = int(t0 * 1000)
        ins += ['-i', f]; parts.append(f'[{k}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms},volume=1.6[v{k}]'); k += 1
if not parts: sys.exit('no narration files found')
fc = ';'.join(parts) + ';' + ''.join(f'[v{i}]' for i in range(1, k)) + f'amix=inputs={k-1}:normalize=0:dropout_transition=0,asplit=2[vo][vokey];'
fc += '[0:a]aresample=48000[bed];[bed][vokey]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[duck]'
mix_in = '[duck][vo]'; n = 2
if a.music:
    ins += ['-stream_loop', '-1', '-i', a.music]
    fc += f';[{k}:a]aresample=48000,aformat=channel_layouts=stereo,volume=0.12[mus]'; mix_in += '[mus]'; n = 3
fc += f';{mix_in}amix=inputs={n}:normalize=0:duration=first,alimiter=limit=0.89,loudnorm=I=-15:TP=-1.5:LRA=11[aout]'
subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', fc, '-map', '0:v', '-map', '[aout]', '-c:v', 'copy',
                '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', a.out], check=True)
print('ok', a.out, 'lines', k - 1)
