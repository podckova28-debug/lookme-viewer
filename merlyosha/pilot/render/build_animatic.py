# Builds the 16:9 animatic of pilot 01: clips + stills + voice + burned subtitles.
import subprocess, os, sys, json
P="/home/user/lookme-viewer/merlyosha"; S=os.path.dirname(os.path.abspath(__file__))
V=f"{P}/pilot/voice"; SB=f"{P}/pilot/storyboard"; R=f"{P}/pilot/render"; C=f"{P}/pilot/clips"
W,H,FPS=1280,720,25
def run(c): subprocess.run(c,shell=True,check=True)
# block boundaries scaled to voice (factor 0.82 of the script timecodes)
k=217.39/265
blocks=[("hook",0,12),("intro",12,25),("load",25,75),("spin",75,125),("motor",125,175),("programs",175,205),("niche",205,230),("recap",230,250),("outro",250,265)]
blocks=[(n,a*k,b*k) for n,a,b in blocks]
# visual plan per block: list of (kind, source, max_seconds or None=fill rest)
plan={
 "hook":[("clip",f"{C}/01-hook.mp4",7.5),("clip",f"{C}/05-thumbnail.mp4",None)],
 "intro":[("still",f"{P}/merlyosha-hero-kitchen.png",None)],
 "load":[("clip",f"{C}/02-drum.mp4",7.5),("still",f"{SB}/02-drum.png",None)],
 "spin":[("clip",f"{C}/03-spin.mp4",7.5),("still",f"{SB}/03-spin.png",None)],
 "motor":[("still",f"{P}/merlyosha-hero-kitchen.png",20),("still",f"{P}/model-sheet/turnaround.png",None)],
 "programs":[("clip",f"{C}/04-programs.mp4",7.5),("still",f"{SB}/04-programs.png",None)],
 "niche":[("still",f"{SB}/01-hook.png",None)],
 "recap":[("still",f"{P}/model-sheet/expressions.png",None)],
 "outro":[("clip",f"{C}/05-thumbnail.mp4",6),("still",f"{R}/endcard.png",None)],
}
segs=[]; i=0
for name,a,b in blocks:
    left=b-a
    items=plan[name]
    for kind,src,mx in items:
        d=left if mx is None else min(mx,left)
        if d<=0.05: continue
        out=f"{S}/seg_{i:02d}.mp4"; i+=1
        if kind=="clip":
            # slow the 5 s clip to fill d seconds (max 1.6x slower), then hold last frame if needed
            slow=min(d/5.0,1.6); 
            run(f'ffmpeg -y -loglevel error -i "{src}" -vf "setpts={slow}*PTS,scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,fps={FPS},tpad=stop_mode=clone:stop_duration=30" -t {d:.3f} -an -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p "{out}"')
        else:
            frames=int(d*FPS)+1
            run(f'ffmpeg -y -loglevel error -loop 1 -i "{src}" -vf "scale=2560:1440:force_original_aspect_ratio=increase,crop=2560:1440,zoompan=z=\'min(1.0+0.06*on/{frames},1.06)\':x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':d={frames}:s={W}x{H}:fps={FPS}" -t {d:.3f} -an -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p "{out}"')
        segs.append(out); left-=d
open(f"{S}/list.txt","w").write("".join(f"file '{s}'\n" for s in segs))
run(f'ffmpeg -y -loglevel error -f concat -safe 0 -i "{S}/list.txt" -c copy "{S}/video_noaudio.mp4"')
# subtitles: copy srt next to output (libass path escaping), burn in
run(f'cp "{V}/pilot-01-voice-aligned.srt" "{S}/subs.srt"')
style="FontName=DejaVu Sans,FontSize=22,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00202020,Outline=2,Shadow=0,MarginV=48,Alignment=2"
run(f'cd "{S}" && ffmpeg -y -loglevel error -i video_noaudio.mp4 -i "{V}/pilot-01-voice.mp3" -vf "subtitles=subs.srt:force_style=\'{style}\'" -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -c:a aac -b:a 160k -shortest "{R}/pilot-01-animatic-16x9.mp4"')
print("done", f"{R}/pilot-01-animatic-16x9.mp4")
