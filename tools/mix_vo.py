"""Lay narration (and optional music bed) over an assembled cut.

usage: python3 tools/mix_vo.py CUT.mp4 OUT.mp4 VO_DIR [--music BED.mp3] [--lead 0.4]
CUT.timeline.json (written by assemble.py) gives each block's start; VO_DIR/vo_<id>.wav is placed at start+lead.
Block sound is ducked under the voice with a sidechain compressor; music sits at -30 LUFS-ish under everything.
"""
import sys, os, json, argparse, subprocess
ap = argparse.ArgumentParser(); ap.add_argument('cut'); ap.add_argument('out'); ap.add_argument('vo_dir')
ap.add_argument('--music', default=''); ap.add_argument('--lead', type=float, default=0.4)
a = ap.parse_args()
tl = json.load(open(a.cut.rsplit('.', 1)[0] + '.timeline.json'))
ins, parts = ['-i', a.cut], []
k = 1
for seg in tl:
    f = os.path.join(a.vo_dir, f"vo_{seg['id']}.wav") if seg['id'] else None
    if f and os.path.exists(f):
        ms = int((seg['start'] + a.lead) * 1000)
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
