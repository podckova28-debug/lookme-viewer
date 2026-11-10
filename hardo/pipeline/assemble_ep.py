import subprocess, os, math, json, sys
from PIL import Image, ImageDraw, ImageFont
E = os.path.dirname(os.path.abspath(__file__))
FR, VO, CL, OUT = [os.path.join(E, d) for d in ("frames", "voice", "clips", "out")]
os.makedirs(os.path.join(OUT, "seg"), exist_ok=True); os.makedirs(os.path.join(OUT, "labeled"), exist_ok=True)
REVEAL = (0.15, 0.9)
GAP = 0.4; FPS = 30; W, H = 1920, 1080; TEMPO = 1.1
FONT = os.path.join(os.path.dirname(E), "pilot", "fonts", "PatrickHand.ttf")
plan = json.load(open(os.path.join(E, "plan.json")))
texts = json.load(open(os.path.join(E, "blocks.json")))
labels = plan["labels"]; blocks = plan["blocks"]
TEMPO = plan.get("tempo", TEMPO)  # paid ElevenLabs voice is sped up 1.1x; the free OmniVoice clone is generated at its final pace (tempo 1.0)
assert len(blocks) == len(texts), (len(blocks), len(texts))
NAME = sys.argv[1] if len(sys.argv) > 1 else "episode"
def draw_arrow(d, a, b, width, k=1):
    (x1,y1),(x2,y2) = a,b; mx,my=(x1+x2)/2,(y1+y2)/2; dx,dy=x2-x1,y2-y1; L=math.hypot(dx,dy) or 1
    cx,cy = mx - k*dy*0.18, my + k*dx*0.18
    pts=[((1-t)**2*x1+2*(1-t)*t*cx+t**2*x2, (1-t)**2*y1+2*(1-t)*t*cy+t**2*y2) for t in [i/24 for i in range(25)]]
    d.line(pts, fill="black", width=width, joint="curve")
    tx,ty = x2-cx, y2-cy; tl=math.hypot(tx,ty) or 1; tx,ty=tx/tl,ty/tl; hl=width*4.5
    for s in (1,-1):
        ang=math.radians(28)*s
        d.line([(x2,y2),(x2-hl*(tx*math.cos(ang)-ty*math.sin(ang)), y2-hl*(tx*math.sin(ang)+ty*math.cos(ang)))], fill="black", width=width)
def labeled(name):
    src = os.path.join(FR, f"{name}.png")
    if name not in labels: return src
    im = Image.open(src).convert("RGB"); w,h = im.size; d = ImageDraw.Draw(im)
    for lab in labels[name]:
        text,(tx,ty),(ax,ay),(bx,by),size = lab[:5]; k = lab[5] if len(lab)>5 else 1
        f = ImageFont.truetype(FONT, int(size*w/1536)); d.text((tx*w,ty*h), text, font=f, fill="black")
        if (ax,ay)==(bx,by): continue
        bb=f.getbbox(text); pad=int(10*w/1536)
        x0,y0,x1,y1 = tx*w+bb[0]-pad, ty*h+bb[1]-pad, tx*w+bb[2]+pad, ty*h+bb[3]+pad
        sx,sy = ax*w, ay*h
        if x0<=sx<=x1 and y0<=sy<=y1:
            # start given inside the text box: move it to the box edge facing the target
            cx,cy=(x0+x1)/2,(y0+y1)/2; dx,dy=bx*w-cx,by*h-cy
            tX = ((x1 if dx>0 else x0)-cx)/dx if dx else 1e9; tY = ((y1 if dy>0 else y0)-cy)/dy if dy else 1e9
            t=min(tX,tY); sx,sy = cx+dx*t, cy+dy*t
        draw_arrow(d, (sx,sy), (bx*w,by*h), max(3,int(7*w/1536)), k)
    out = os.path.join(OUT,"labeled",f"{name}.png"); im.save(out); return out
def _fit(im):
    sw, sh = im.size
    if abs(sw/sh - W/H) > 1e-3:
        if sw/sh > W/H: nw=int(sh*W/H); im=im.crop(((sw-nw)//2,0,(sw-nw)//2+nw,sh))
        else: nh=int(sw*H/W); im=im.crop((0,(sh-nh)//2,sw,(sh-nh)//2+nh))
    if im.size[0] < W*1.5: im = im.resize((W*2,H*2), Image.LANCZOS)
    return im
def kenburns(src, out, frames, z, zoom_in, ease=False, base=None):
    if base:   # labels write themselves on: reveal the label pixels left to right between REVEAL[0] and REVEAL[1] seconds
        import numpy as np
        lab = np.asarray(_fit(Image.open(src).convert("RGB"))); bas = np.asarray(_fit(Image.open(base).convert("RGB")))
        diff = np.abs(lab.astype(np.int16)-bas.astype(np.int16)).max(2) > 18
        ys, xs = np.nonzero(diff); order = np.argsort(xs, kind="stable"); ys, xs = ys[order], xs[order]
        canvas = bas.copy(); shown = 0; sw, sh = W*2, H*2
        f0, f1 = int(REVEAL[0]*FPS), max(int(REVEAL[0]*FPS)+1, int(REVEAL[1]*FPS))
    im = Image.open(src).convert("RGB"); sw, sh = im.size
    if abs(sw/sh - W/H) > 1e-3:
        if sw/sh > W/H: nw=int(sh*W/H); im=im.crop(((sw-nw)//2,0,(sw-nw)//2+nw,sh))
        else: nh=int(sw*H/W); im=im.crop((0,(sh-nh)//2,sw,(sh-nh)//2+nh))
        sw, sh = im.size
    if sw < W*1.5: im = im.resize((W*2,H*2), Image.LANCZOS); sw, sh = im.size
    proc = subprocess.Popen(["ffmpeg","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-an","-c:v","libx264","-preset","fast","-crf","19","-pix_fmt","yuv420p",out], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    for i in range(frames):
        if base:
            want = len(xs) if i >= f1 else (0 if i < f0 else int(len(xs)*(i-f0)/(f1-f0)))
            if want > shown: canvas[ys[shown:want], xs[shown:want]] = lab[ys[shown:want], xs[shown:want]]; shown = want
            im = Image.fromarray(canvas)
        p=i/max(frames-1,1); p = p*p*(3-2*p) if ease else p; zoom = 1+z*p if zoom_in else 1+z-z*p
        a=(sw/zoom)/W; x0=(sw-sw/zoom)/2; y0=(sh-sh/zoom)/2
        proc.stdin.write(im.transform((W,H), Image.AFFINE, (a,0,x0,0,a,y0), resample=Image.BILINEAR).tobytes())
    proc.stdin.close(); proc.wait()
    if proc.returncode: raise RuntimeError(proc.stderr.read().decode()[-500:])
def dur(f): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]).decode())
def run(cmd): subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
n = len(blocks)
def adur(f):  # decoded length: ffprobe's mp3 duration includes encoder padding (~0.07 s per file), which drifts the cut
    raw = subprocess.run(["ffmpeg","-v","error","-i",f,"-f","s16le","-ac","1","-ar","44100","-"], capture_output=True, check=True).stdout
    return len(raw)/2/44100
vdur = [adur(os.path.join(VO, f"{i:02d}.mp3"))/TEMPO for i in range(1,n+1)]
segs=[]; srt=[]; t=0.0; zoom_dir=1; jobs=[]; seg_t=[]; block_t=[]
STRONG = set(plan.get("zoom_strong", list(labels)))  # stat / label frames get a visible eased push-in
Z_NORMAL = plan.get("zoom", 0.04); Z_STRONG = plan.get("zoom_strong_amount", 0.06)  # keep small: big zooms cut off the frame edges
for bi, block in enumerate(blocks):
    block_t.append(t); seg_cursor=t
    total = vdur[bi]+GAP; srt.append((t,t+vdur[bi],texts[bi]))
    fixed = sum(s[2] for s in block if s[0]=="clip" and os.path.exists(os.path.join(CL,f"{s[1]}.mp4")))
    rest = total-fixed
    for kind,name,share in block:
        if kind=="clip":
            src=os.path.join(CL,f"{name}.mp4")
            if not os.path.exists(src):
                kind="still"; name=plan.get("clip_fallback",{}).get(name, name)
                d = total if len(block)==1 else rest*0.5
            else: d=share
        else:
            d = rest if share is None else rest*share
        out=os.path.join(OUT,"seg",f"{len(segs):02d}.mp4")
        if kind=="clip": jobs.append(("clip",src,out,d,None,0))
        else: jobs.append(("still",labeled(name),out,int(round(d*FPS)),zoom_dir>0,Z_STRONG if name in STRONG else Z_NORMAL)); zoom_dir*=-1
        segs.append(out); seg_t.append((seg_cursor,name)); seg_cursor+=d
    t+=total
def _base(src):
    if os.path.dirname(src)==os.path.join(OUT,"labeled"): return os.path.join(FR, os.path.basename(src))
    return None
def name_strong(src): return os.path.splitext(os.path.basename(src))[0] in STRONG
def _do(j):
    kind,src,out,d,zi,z=j
    import json as _json
    meta = out + ".json"; want = d if kind=="clip" else d/FPS
    if os.path.exists(out) and os.path.getsize(out)>1000 and os.path.exists(meta):
        try:
            m = _json.load(open(meta))
            ok = m.get("src")==src and m.get("kind")==kind and abs(m.get("want",-1)-want)<0.01 and bool(m.get("zi"))==bool(zi) and abs(m.get("z",0.06)-(z or 0.06))<1e-6 and bool(m.get("anim"))==bool(_base(src)) \
                 and abs(dur(out)-want) < 0.12 and os.path.getmtime(out) > os.path.getmtime(src)
        except Exception: ok = False
        if ok: return out
    for f in (out, meta):
        if os.path.exists(f): os.remove(f)
    _json.dump({"src":src,"kind":kind,"want":want,"zi":bool(zi),"z":z or 0.06,"anim":bool(_base(src))}, open(meta,"w"))
    if kind=="clip": run(["ffmpeg","-y","-i",src,"-vf",f"scale={W}:{H}:flags=lanczos,fps={FPS},tpad=stop_mode=clone:stop_duration=6,format=yuv420p","-t",f"{d:.3f}","-an","-c:v","libx264","-preset","fast","-crf","19",out])
    else: kenburns(src,out,d,z,zi,ease=False,base=_base(src))  # even, slow move; labels write on
    return out
from multiprocessing import Pool
with Pool(4) as pool:
    for i,o in enumerate(pool.imap_unordered(_do, jobs),1): print(f"seg {i}/{len(jobs)} done", flush=True)
open(os.path.join(OUT,"segs.txt"),"w").write("".join(f"file '{s}'\n" for s in segs))
run(["ffmpeg","-y","-f","concat","-safe","0","-i",os.path.join(OUT,"segs.txt"),"-c","copy",os.path.join(OUT,"video_silent.mp4")])
inputs=[]; [inputs.extend(["-i",os.path.join(VO,f"{i:02d}.mp3")]) for i in range(1,n+1)]
# ep14: atempo/apad lose ~30 ms per block; pad each block to its planned length so cuts and subtitles do not drift
fc = "".join(f"[{i}:a]aresample=44100,atempo={TEMPO},apad=whole_dur={vdur[i]+GAP:.5f},atrim=end={vdur[i]+GAP:.5f}[a{i}];" for i in range(n)) + "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1,loudnorm=I=-16:TP=-1.5[a]"
run(["ffmpeg","-y",*inputs,"-filter_complex",fc,"-map","[a]","-c:a","aac","-b:a","192k",os.path.join(OUT,"voice.m4a")])
VOICE = os.path.join(OUT,"voice.m4a")
def sfx_track():
    # plan["sfx"]: [[block (1-based), offset s, "alert"|"beep"|"pop", amplitude]]; plan["label_pop"]: amplitude of a pop at each label shot
    import numpy as np, wave
    ev = [(block_t[b-1]+off, kind, amp) for b,off,kind,amp in plan.get("sfx", [])]
    if plan.get("label_pop"): ev += [(t0+REVEAL[0],"pop",plan["label_pop"]) for t0,name in seg_t if name in labels]
    if not ev: return None
    sr=44100; total=sum(vdur)+GAP*n; buf=np.zeros(int(total*sr)+sr)
    def tone(f, d):
        x=np.arange(int(d*sr))/sr; y=np.sin(2*np.pi*f*x)+0.35*np.sin(4*np.pi*f*x)+0.15*np.sin(6*np.pi*f*x)
        env=np.minimum(1,np.minimum(x/0.01,(d-x)/0.03)); return y*env/1.5
    alert=np.concatenate([tone(853,0.42),tone(960,0.42)])
    gap=np.zeros(int(0.1*sr)); beep=np.concatenate([tone(1000,0.12),gap,tone(1000,0.12),gap,tone(1000,0.12)])  # phone alarm
    x=np.arange(int(0.09*sr))/sr; pop=np.sin(2*np.pi*(900*x-3000*x*x))*np.exp(-x/0.02)
    for t0,kind,amp in ev:
        y={"alert":alert,"beep":beep}.get(kind,pop)*amp; i=int(t0*sr); buf[i:i+len(y)]+=y[:len(buf)-i]
    p=os.path.join(OUT,"sfx.wav"); w=wave.open(p,"wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((np.clip(buf,-1,1)*32767).astype("<i2").tobytes()); w.close(); return p
_sfx = sfx_track()
if _sfx:
    VOICE = os.path.join(OUT,"voice_sfx.m4a")
    run(["ffmpeg","-y","-i",os.path.join(OUT,"voice.m4a"),"-i",_sfx,"-filter_complex","[1:a]aresample=44100,aformat=channel_layouts=stereo[s];[0:a][s]amix=inputs=2:duration=first:normalize=0[a]","-map","[a]","-c:a","aac","-b:a","192k",VOICE])
def ts(x): return f"{int(x//3600):02d}:{int(x%3600//60):02d}:{x%60:06.3f}".replace(".",",")
with open(os.path.join(OUT,f"{NAME}.srt"),"w",encoding="utf8") as f:
    total_len = min(sum(vdur)+GAP*n, dur(os.path.join(OUT,"video_silent.mp4")), dur(VOICE))  # ep12: planned length ran 0.5s past the real video
    import re as _re, textwrap as _tw
    def _chunks(tx, maxc=78):  # ep14: one cue per paragraph wrapped to 4-6 lines on YouTube; split into <=2 lines of <=42 chars
        out=[]
        for sent in _re.split(r'(?<=[.!?])\s+', tx.strip()):
            while len(sent)>maxc:
                cut=max((m.end() for m in _re.finditer(r'[,:;]\s', sent[:maxc])), default=0) or sent.rfind(' ',0,maxc)
                out.append(sent[:cut].strip()); sent=sent[cut:].strip()
            if sent: out.append(sent)
        return out
    def _onsets(i):  # ep15: speech onsets inside block i (timeline seconds from block start), from silencedetect
        r=subprocess.run(["ffmpeg","-i",os.path.join(VO,f"{i+1:02d}.mp3"),"-af","silencedetect=n=-40dB:d=0.25","-f","null","-"],capture_output=True,text=True).stderr
        return [float(x)/TEMPO for x in _re.findall(r"silence_end: ([\d.]+)",r)]
    k=0
    for bi,(a,b,tx) in enumerate(srt):
        blk=a; a+=0.25; b=min(b,total_len-0.3); parts=_chunks(tx); L=sum(len(p) for p in parts)
        on=[blk+o for o in _onsets(bi)]
        starts=[a]; acc=a
        for p in parts[:-1]:
            acc+=(b-a)*len(p)/L
            near=[o for o in on if abs(o-acc)<=0.9 and o>starts[-1]+0.7]
            starts.append(min(near,key=lambda o:abs(o-acc)) if near else acc)  # snap each new cue to the next speech onset
        ends=[x-0.04 for x in starts[1:]]+[b]
        for p,t0,t1 in zip(parts,starts,ends):
            k+=1
            f.write(f"{k}\n{ts(t0)} --> {ts(t1)}\n" + "\n".join(_tw.wrap(p.replace('A.I.','AI'),42)) + "\n\n")
run(["ffmpeg","-y","-i",os.path.join(OUT,"video_silent.mp4"),"-i",VOICE,"-map","0:v","-map","1:a","-c:v","copy","-c:a","copy","-shortest","-movflags","+faststart",os.path.join(OUT,f"{NAME}.mp4")])
print("video",round(dur(os.path.join(OUT,"video_silent.mp4")),2),"audio",round(dur(os.path.join(OUT,"voice.m4a")),2),"final",round(dur(os.path.join(OUT,f"{NAME}.mp4")),2))
