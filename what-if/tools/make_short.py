"""Vertical 1080x1920 Short from horizontal 1080p blocks.

Layout: blurred, darkened copy of the video as background; the video itself scaled up 1.35x and centre-cropped to
1080x820 in the middle; hook title on top; burned captions (one phrase at a time) under the picture.

usage: python3 tools/make_short.py OUT.mp4 "HOOK LINE 1|HOOK LINE 2" CLIP1.mp4:"caption a|caption b" CLIP2.mp4:"..." ...
Each clip's captions are spread evenly across its duration. Clip loudness is matched to -16 LUFS for mobile.
"""
import sys, os, subprocess, tempfile, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANG = os.path.join(ROOT, 'assets/fonts/Bangers-Regular.ttf')
NEUE = os.path.join(ROOT, 'assets/fonts/ComicNeue-Bold.ttf')

def dur(p):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]).decode())

out, hook = sys.argv[1], sys.argv[2].split('|')
clips = [a.split(':', 1) for a in sys.argv[3:]]
tmp = tempfile.mkdtemp()
# 1) join clips
lst = os.path.join(tmp, 'l.txt')
open(lst, 'w').write(''.join(f"file '{os.path.abspath(c)}'\n" for c, _ in clips))
joined = os.path.join(tmp, 'j.mp4')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c:v', 'libx264', '-crf', '16', '-c:a', 'aac', '-ar', '48000', joined], check=True)
# 2) caption schedule
caps, t = [], 0.0
for c, text in clips:
    d = dur(c); parts = [p.strip() for p in text.split('|') if p.strip()]
    for i, p in enumerate(parts):
        caps.append((t + d * i / len(parts) + 0.3, t + d * (i + 1) / len(parts) - 0.15, p))
    t += d
def tf(s, name):
    p = os.path.join(tmp, name); open(p, 'w', encoding='utf-8').write(s); return p
f = ("[0:v]split[a][b];"
     "[a]scale=-2:1920,crop=1080:1920,boxblur=24:2,eq=brightness=-0.22:saturation=0.8[bg];"
     "[b]scale=-2:820*1.0,scale=iw*1.35:ih*1.35,crop=1080:820[fg];"
     "[bg][fg]overlay=0:560[v0]")
last = 'v0'
for i, line in enumerate(hook):
    col = '0xFFD638' if i == 0 else 'white'
    f += (f";[{last}]drawtext=fontfile={BANG}:textfile={tf(line, f'h{i}.txt')}:fontsize=104:fontcolor={col}:"
          f"borderw=9:bordercolor=0x141012:x=(w-text_w)/2:y={180 + i * 120}[h{i}]")
    last = f'h{i}'
for i, (a, b, text) in enumerate(caps):
    f += (f";[{last}]drawtext=fontfile={NEUE}:textfile={tf(text, f'c{i}.txt')}:fontsize=62:fontcolor=white:"
          f"borderw=7:bordercolor=0x141012:x=(w-text_w)/2:y=1450:enable='between(t,{a:.2f},{b:.2f})'[c{i}]")
    last = f'c{i}'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', joined, '-filter_complex', f, '-map', f'[{last}]', '-map', '0:a',
                '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p',
                '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out], check=True)
print('ok', out, round(t, 1), 's')
