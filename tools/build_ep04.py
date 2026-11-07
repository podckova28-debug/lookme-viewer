"""Episode 4 (Superman) cut: Wan clips + stills -> out/e4_cut.mp4 + timeline.json for mix_vo.py.
usage: python3 tools/build_ep04.py WORKDIR"""
import subprocess, json, sys, os
S = sys.argv[1]; C = 'assets/ep04/clips'; K = 'assets/ep04/keys'
# (id, kind, src, start, end_or_dur, extra)
seq = [('01','c','01',0,None),('02','c','02',0,None),('03','c','03ab',0,5.6),('S1','s',f'{S}/S1.png',5.6,'zoom'),
 ('04','c','04',0,None),('05a','c','05a',0,None),('05b','c','05b',0,None),('06a','c','06a',0,None),('06b','c','06b',0,None),
 ('07','c','07',0,None),('08','c','08',0,None),('09a','c','09a',0,None),('09b','c','09b',0,None),('10a','c','10a',0,None),
 ('11','c','11',0,None),('12a','c','12a',0,None),('12b','c','12b',0,None),('13','c','13',0,None),('14a','c','14a',0,2.6),
 ('14b','c','14b',0,None),('15','c','15',0,None),('16','c','16',0,None),('17','c','17',0,None),('S4','s',f'{S}/S4.png',4.6,'zoom'),
 ('18','c','18',0,None),('19b','c','19b',0,None)]
dur = lambda f: float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
parts, tl, t = [], [], 0.0
for i,(bid,kind,src,a,b) in enumerate(seq):
    out = f'{S}/q{i:02d}.mp4'
    if kind == 'c':
        f = f'{C}/{src}.mp4'; end = b if b else dur(f)
        vf = f'trim={a}:{end},setpts=PTS-STARTPTS,scale=1920:1080:flags=lanczos,fps=24,setsar=1'
        if bid == '19b': vf += ',tpad=stop_mode=clone:stop_duration=1.2'
        af = f'atrim={a}:{end},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-23:TP=-2,afade=t=in:d=0.03' + (',apad=pad_dur=1.2' if bid=='19b' else '')
        cmd = ['ffmpeg','-y','-loglevel','error','-i',f,'-vf',vf,'-af',af,'-c:v','libx264','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-shortest',out]
    else:
        d = a
        z = "zoompan=z='min(zoom+0.0007,1.05)':d=1:s=1920x1080:fps=24" if b == 'zoom' else "zoompan=z=1.06:y='ih/2-(ih/zoom/2)+sin(on/24*2.2)*12':x='iw/2-(iw/zoom/2)':d=1:s=1920x1080:fps=24"
        cmd = ['ffmpeg','-y','-loglevel','error','-loop','1','-t',str(d),'-i',src,'-f','lavfi','-t',str(d),'-i','anullsrc=r=48000:cl=stereo',
               '-vf',f'scale=1920:1080:flags=lanczos,{z},setsar=1','-c:v','libx264','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest',out]
    subprocess.run(cmd, check=True); d = dur(out); parts.append(out); tl.append({'id': bid, 'start': round(t,3), 'dur': round(d,3)}); t += d
open(f'{S}/list.txt','w').write(''.join(f"file '{p}'\n" for p in parts))
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',f'{S}/list.txt','-c','copy','out/e4_cut.mp4'], check=True)
json.dump(tl, open('out/e4_cut.timeline.json','w'), indent=1); print('total', round(t,2))
