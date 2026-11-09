# Builds the 9:16 Shorts cut: vertical clips + stills, word-synced captions, voice.
import subprocess, os
P="/home/user/lookme-viewer/merlyosha/pilot/shorts"; S=os.path.dirname(os.path.abspath(__file__))
V="/home/user/lookme-viewer/merlyosha/pilot/voice/shorts-01-voice.mp3"
W,H,FPS=1080,1920,30
def run(c): subprocess.run(c,shell=True,check=True)
# (kind, source, start, end) on the voice timeline (seconds)
plan=[("clip",f"{P}/clips/01-hook.mp4",0.0,4.0),
      ("clip",f"{P}/clips/02-spin.mp4",4.0,9.0),
      ("clip",f"{P}/clips/03-shake.mp4",9.0,13.2),
      ("still",f"{P}/frames/01-hook.png",13.2,16.3),
      ("clip",f"{P}/clips/04-programs.mp4",16.3,23.0),
      ("still",f"{P}/frames/04-programs.png",23.0,31.3),
      ("clip",f"{P}/clips/05-cta.mp4",31.3,36.0),
      ("still",f"{P}/frames/05-cta.png",36.0,38.4)]
segs=[]
for i,(kind,src,a,b) in enumerate(plan):
    d=b-a; out=f"{S}/vseg_{i:02d}.mp4"
    if kind=="clip":
        slow=min(d/5.0,1.5)
        run(f'ffmpeg -y -loglevel error -i "{src}" -vf "setpts={slow}*PTS,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},tpad=stop_mode=clone:stop_duration=30" -t {d:.3f} -an -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p "{out}"')
    else:
        fr=int(d*FPS)+1
        run(f'ffmpeg -y -loglevel error -loop 1 -i "{src}" -vf "scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,zoompan=z=\'min(1.0+0.08*on/{fr},1.08)\':x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':d={fr}:s={W}x{H}:fps={FPS}" -t {d:.3f} -an -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p "{out}"')
    segs.append(out)
open(f"{S}/vlist.txt","w").write("".join(f"file '{s}'\n" for s in segs))
run(f'ffmpeg -y -loglevel error -f concat -safe 0 -i "{S}/vlist.txt" -c copy "{S}/vshorts_noaudio.mp4"')
os.makedirs(f"{P}/render",exist_ok=True)
run(f'cd "{S}" && ffmpeg -y -loglevel error -i vshorts_noaudio.mp4 -i "{V}" -vf "ass=shorts_captions.ass:fontsdir=../fonts" -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -c:a aac -b:a 160k -shortest "{P}/render/shorts-01-9x16.mp4"')
print("done")
