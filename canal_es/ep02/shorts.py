"""Cut vertical Shorts (1080x1920) from the finished episode.
usage: python shorts.py EPISODE.mp4 OUT_DIR
Each Short: the 16:9 picture cropped to 4:3 in the middle, blurred copy as background,
hook title on top, burned-in subtitles from the narration timing, 'video completo' card at the end."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
EP, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
T = json.load(open(os.path.join(HERE, 'timing.json')))
LINES = {l['id']: l for l in json.load(open(os.path.join(HERE, 'vo_lines.json'), encoding='utf-8'))}
FONTS = os.path.join(HERE, '..', 'anim', 'fonts')
NAMES = {'valeria': 'RENATA', 'tu': 'TÚ', 'mama': 'MAMÁ', 'profe': 'PROFE', 'nacho': 'NACHO', 'chicos': 'TODOS'}
def S(sid): return T['scenes'][sid]
def Lt(sid, lid): return S(sid)['start'] + S(sid)['L'][lid][0]
def Le(sid, lid): return Lt(sid, lid) + S(sid)['L'][lid][1]

SHORTS = [
    ('short1_taza', S('s04')['start'], S('s04')['start'] + S('s04')['dur'], 'VES EL FUTURO...\\NY ATRAPAS LA TAZA'),
    ('short2_quemados', S('s05')['start'], S('s05')['start'] + S('s05')['dur'], '¿Y SI VIERAS CADA BALÓN\\NANTES DE QUE LO LANCEN?'),
    ('short3_cumple', Lt('s11', 's11_05') - .3, S('s11')['start'] + S('s11')['dur'], 'TU FIESTA SORPRESA...\\NCINCO SEGUNDOS ANTES'),
    ('short4_pizza', S('s10')['start'], Le('s10', 's10_08') + .8, 'RESPONDES ANTES\\NDE QUE TE PREGUNTEN'),
    ('short5_pregunta', Lt('s14', 's14_02') - .3, S('s14')['start'] + S('s14')['dur'], 'YA SABES LO QUE\\NTE VA A PREGUNTAR'),
    ('short6_pepe', S('s16')['start'], S('s16')['start'] + S('s16')['dur'], 'EN 5 SEGUNDOS\\NPEPE VA A HABLAR'),
    ('short7_ciencia', Lt('s17', 's17_05') - .4, Le('s17', 's17_06') + 1.0, 'TU CIUDAD PUEDE\\NVER EL FUTURO'),
]
def ts(x): x = max(0, x); h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60; return f'{h}:{m:02d}:{s:05.2f}'
HEAD = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Hook,Bangers,92,&H0047E0FD,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,7,0,8,60,60,150,1
Style: Sub,Bangers,74,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,6,0,2,80,80,330,1
Style: End,Bangers,80,&H00FFFFFF,&H000000FF,&H001C1CE0,&H00000000,0,0,0,0,100,100,1,0,3,14,0,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
for name, a, b, hook, *vert in SHORTS:
    dur = b - a; ev = [f'Dialogue: 0,{ts(0)},{ts(dur)},Hook,,0,0,0,,{hook}']
    for sid in T['order']:
        for lid, (t, d, who) in S(sid)['L'].items():
            st = S(sid)['start'] + t - a; en = st + d + .15
            if en < 0 or st > dur: continue
            txt = LINES[lid]['text'].replace('…', '...')
            if who != 'narrador': txt = NAMES.get(who, who.upper()) + ': ' + txt
            ev.append(f'Dialogue: 1,{ts(st)},{ts(min(en, dur))},Sub,,0,0,0,,{txt.upper()}')
    endpos = '\\pos(540,620)' if vert else ''
    ev.append(f'Dialogue: 2,{ts(dur - 2.2)},{ts(dur)},End,,0,0,0,,{{\\fad(200,0){endpos}}}VIDEO COMPLETO\\NEN EL CANAL')
    ass = os.path.join(OUT, name + '.ass'); open(ass, 'w', encoding='utf-8').write(HEAD + '\n'.join(ev) + '\n')
    out = os.path.join(OUT, name + '.mp4')
    if vert:   # 3D shots are rendered natively vertical (painted look, 1080x1920): no crop, no blurred bars
        sid = vert[0]; vv = os.path.join(OUT, name + '_vert.mp4')
        subprocess.run(['node', os.path.join(HERE, '..', 'anim', 'render.js'), os.path.join(HERE, f'ep02.html?scene={sid}&hyb=1&vert=1'), f'{dur:.3f}', vv, f'{a - S(sid)["start"]:.3f}'], check=True, cwd=HERE)
        vf = f"[0:v]subtitles='{ass}':fontsdir='{FONTS}'[v]"
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', vv, '-ss', f'{a:.3f}', '-t', f'{dur:.3f}', '-i', EP, '-filter_complex', vf, '-map', '[v]', '-map', '1:a',
                        '-af', f'afade=t=in:d=0.15,afade=t=out:st={dur - .4:.2f}:d=0.4', '-c:v', 'libx264', '-crf', '20', '-preset', 'medium', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out], check=True)
        print(name, round(dur, 1), 's (vertical 3D) ->', out); continue
    vf = ("[0:v]split[a][b];[a]scale=3414:1920,crop=1080:1920,boxblur=24:2,eq=brightness=-0.18[bg];"
          "[b]crop=1440:1080:240:0,scale=1080:810[fg];[bg][fg]overlay=0:540,"
          f"subtitles='{ass}':fontsdir='{FONTS}'[v]")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a:.3f}', '-t', f'{dur:.3f}', '-i', EP, '-filter_complex', vf, '-map', '[v]', '-map', '0:a',
                    '-af', f'afade=t=in:d=0.15,afade=t=out:st={dur - .4:.2f}:d=0.4', '-c:v', 'libx264', '-crf', '20', '-preset', 'medium', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out], check=True)
    print(name, round(dur, 1), 's ->', out)
