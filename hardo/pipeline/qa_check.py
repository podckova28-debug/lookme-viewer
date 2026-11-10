#!/usr/bin/env python3
"""QA for Hardo episodes. Usage: qa_check.py <episode_dir> [--name NAME]
Expects: <dir>/plan.json, <dir>/blocks.json, <dir>/voice/NN.mp3, <dir>/clips/*.mp4,
<dir>/out/<NAME>.mp4 + .srt, <dir>/out/thumb_*_1280x720.jpg (optional).
Writes <dir>/out/qa_report.md and qa_report.json. Exit code 1 if any FAIL."""
import sys, os, json, re, subprocess, math, glob
from PIL import Image, ImageChops, ImageStat, ImageFont
import numpy as np

def probe(f):
    j = json.loads(subprocess.check_output(["ffprobe","-v","error","-print_format","json","-show_streams","-show_format",f]))
    v = next((s for s in j["streams"] if s["codec_type"]=="video"), None)
    a = next((s for s in j["streams"] if s["codec_type"]=="audio"), None)
    return j, v, a
def dur(f): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]))
def srt_parse(path):
    cues=[]; txt=open(path,encoding="utf8").read().strip()
    for block in re.split(r"\n\s*\n", txt):
        lines=block.strip().splitlines()
        if len(lines)<3: continue
        m=re.match(r"(\d+):(\d+):(\d+),(\d+) --> (\d+):(\d+):(\d+),(\d+)", lines[1])
        if not m: continue
        g=list(map(int,m.groups()))
        a=g[0]*3600+g[1]*60+g[2]+g[3]/1000; b=g[4]*3600+g[5]*60+g[6]+g[7]/1000
        cues.append((a,b," ".join(lines[2:])))
    return cues

def main():
    d = sys.argv[1]; name = None
    if "--name" in sys.argv: name = sys.argv[sys.argv.index("--name")+1]
    out = os.path.join(d,"out")
    mp4s = sorted([f for f in glob.glob(os.path.join(out,"*.mp4")) if "light" not in f and "preview" not in f and "silent" not in f and "/seg/" not in f])
    mp4 = os.path.join(out, name+".mp4") if name else mp4s[0]
    srt = mp4[:-4]+".srt"
    plan = json.load(open(os.path.join(d,"plan.json"))); blocks = json.load(open(os.path.join(d,"blocks.json")))
    TEMPO = plan.get("tempo",1.2); GAP = plan.get("gap",0.4); FPS=30
    checks=[]
    def add(name, ok, detail=""): checks.append({"check":name,"status":"PASS" if ok else "FAIL","detail":detail})
    def warn(name, detail): checks.append({"check":name,"status":"WARN","detail":detail})

    # 1. container
    j,v,a = probe(mp4); D = float(j["format"]["duration"])
    add("1080p30", v and v["width"]==1920 and v["height"]==1080 and v["r_frame_rate"] in ("30/1","30000/1001"), f"{v['width']}x{v['height']} @ {v['r_frame_rate']}")
    add("audio track present", a is not None and a["codec_name"]=="aac", a["codec_name"] if a else "none")
    vd=float(v.get("duration",D)); ad=float(a.get("duration",D)) if a else 0
    add("video/audio length match", abs(vd-ad) <= 0.6, f"video {vd:.2f}s audio {ad:.2f}s")
    # 2. narration coverage
    n=len(blocks); vfiles=[os.path.join(d,"voice",f"{i:02d}.mp3") for i in range(1,n+1)]
    missing=[f for f in vfiles if not os.path.exists(f)]
    add("all voice blocks present", not missing, f"{n-len(missing)}/{n}")
    if not missing:
        def adur(f):  # decoded length (ffprobe's mp3 duration includes encoder padding)
            raw=subprocess.run(["ffmpeg","-v","error","-i",f,"-f","s16le","-ac","1","-ar","44100","-"],capture_output=True).stdout
            return len(raw)/2/44100
        planned = sum(adur(f)/TEMPO for f in vfiles) + GAP*n
        add("narration fits the cut (no clipped ending)", D >= planned - 1.0, f"planned {planned:.1f}s, final {D:.1f}s")
    # 3. SRT
    if os.path.exists(srt):
        cues=srt_parse(srt)
        add("srt cue count == blocks", len(cues)==n, f"{len(cues)} cues / {n} blocks")
        add("srt inside video duration", cues and cues[-1][1] <= D-0.05, f"last cue ends {cues[-1][1]:.2f}s, video {D:.2f}s" if cues else "no cues")
        overlaps=[i for i in range(1,len(cues)) if cues[i][0] < cues[i-1][1]-0.01]
        add("srt no overlaps", not overlaps, f"{len(overlaps)} overlaps")
        mism=[i for i,(s,e,t) in enumerate(cues) if t.strip()!=blocks[i].strip()] if len(cues)==n else []
        add("srt text == script", not mism, f"{len(mism)} differ")
    else: add("srt file exists", False, srt)
    # 4. clips present and >= planned length
    bad=[]
    for block in plan["blocks"]:
        for kind,nm,share in block:
            if kind=="clip":
                p=os.path.join(d,"clips",f"{nm}.mp4")
                if not os.path.exists(p): bad.append(f"{nm}: missing")
                elif dur(p) < share-0.1: bad.append(f"{nm}: {dur(p):.2f}s < {share}s")
    nclips=sum(1 for b in plan["blocks"] for s in b if s[0]=="clip")
    add("animated clips present and long enough", not bad, f"{nclips} clips; "+("; ".join(bad) if bad else "ok"))
    # 5. frames: white background, no black/dark, no frozen video
    tmp=os.path.join(out,"qa_frames"); os.makedirs(tmp,exist_ok=True)
    for f in glob.glob(os.path.join(tmp,"*.jpg")): os.remove(f)
    subprocess.run(["ffmpeg","-v","error","-y","-i",mp4,"-vf","fps=1/2,scale=480:270",os.path.join(tmp,"f%05d.jpg")],check=True)
    frames=sorted(glob.glob(os.path.join(tmp,"*.jpg")))
    lum=[]; dark=[]; frozen=[]; prev=None; still_run=0
    for i,f in enumerate(frames):
        im=Image.open(f).convert("L"); m=ImageStat.Stat(im).mean[0]; lum.append(m)
        if m < 120: dark.append((i*2, round(m)))
        if prev is not None:
            diff=ImageStat.Stat(ImageChops.difference(im,prev)).mean[0]
            still_run = still_run+1 if diff < 0.15 else 0
            if still_run >= 3: frozen.append(i*2)
        prev=im
    add("white-background rule (mean luminance >= 120 on all samples)", not dark, f"{len(dark)} dark samples of {len(frames)}" + (f", first at {dark[0][0]}s" if dark else ""))
    add("no frozen video (>=6s without any motion)", not frozen, f"{len(frozen)} frozen samples" + (f", first at {frozen[0]}s" if frozen else ""))
    add("no pure black frames", all(l>30 for l in lum), f"min luminance {min(lum):.0f}")
    # 6. labels inside safe area (text box visible at the tightest zoom: plan zoom (default 4%), zoom_strong_amount (default 6%) for labelled frames)
    FONT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"pilot","fonts","PatrickHand.ttf")
    if not os.path.exists(FONT): FONT=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"pilot","fonts","PatrickHand.ttf")
    oob=[]
    for fr,labs in plan.get("labels",{}).items():
        src=os.path.join(d,"frames",f"{fr}.png")
        if not os.path.exists(src): oob.append(f"{fr}: frame missing"); continue
        w,h=Image.open(src).size
        for lab in labs:
            text,(tx,ty),a1,a2,size = lab[:5]
            font=ImageFont.truetype(FONT,int(size*w/1536)); bb=font.getbbox(text)
            x1=tx*w+bb[2]; y1=ty*h+bb[3]
            z = plan.get("zoom_strong_amount", 0.06) if fr in set(plan.get("zoom_strong", plan.get("labels", {}).keys() if "label_pop" in plan else [])) else plan.get("zoom", 0.04)
            m = (1-1/(1+z))/2 + 0.005   # part of each edge hidden at the tightest zoom, plus a small margin
            x0=tx*w+bb[0]; y0=ty*h+bb[1]
            if x0/w < m or y0/h < m or x1/w > 1-m or y1/h > 1-m: oob.append(f"{fr}:'{text}' box {x0/w:.3f}-{x1/w:.3f} x {y0/h:.3f}-{y1/h:.3f}, zoom {z:.0%}")
    add("hand-written labels inside safe area", not oob, "; ".join(oob) if oob else f"{sum(len(v) for v in plan.get('labels',{}).values())} labels ok")
    # 6b. labels must sit on white, arrows must point at ink, start outside the text and not be stubs
    overl=[]; miss=[]; badstart=[]; short=[]
    for fr,labs in plan.get("labels",{}).items():
        src=os.path.join(d,"frames",f"{fr}.png")
        if not os.path.exists(src): continue
        im=Image.open(src).convert("L"); w,h=im.size; arr=np.asarray(im)
        for lab in labs:
            text,(tx,ty),a1,(bx,by),size = lab[:5]
            if tuple(a1)==(bx,by): continue  # label without arrow
            font=ImageFont.truetype(FONT,int(size*w/1536)); bb=font.getbbox(text); pad=int(10*w/1536)
            x0,y0,x1,y1=tx*w+bb[0]-pad,ty*h+bb[1]-pad,tx*w+bb[2]+pad,ty*h+bb[3]+pad; sx,sy=a1[0]*w,a1[1]*h
            if x0<=sx<=x1 and y0<=sy<=y1:  # renderer snaps the start to the box edge facing the target
                cx,cy=(x0+x1)/2,(y0+y1)/2; dx,dy=bx*w-cx,by*h-cy
                tX=((x1 if dx>0 else x0)-cx)/dx if dx else 1e9; tY=((y1 if dy>0 else y0)-cy)/dy if dy else 1e9
                t=min(tX,tY); sx,sy=cx+dx*t,cy+dy*t
                if t>1: badstart.append(f"{fr}:'{text}' arrow target lies inside its own text")
            if ((sx/w-bx)**2+((sy/h-by)*h/w)**2)**0.5 < 0.06: short.append(f"{fr}:'{text}' arrow shorter than 6% of width (from {sx/w:.2f},{sy/h:.2f})")
            font=ImageFont.truetype(FONT,int(size*w/1536)); bb=font.getbbox(text)
            x0,y0,x1,y1=int(tx*w+bb[0]),int(ty*h+bb[1]),int(tx*w+bb[2]),int(ty*h+bb[3])
            x0,y0=max(0,x0),max(0,y0); x1,y1=min(w,x1),min(h,y1)
            region=arr[y0:y1,x0:x1]; ink=(region<200).mean() if region.size else 1
            if ink>0.06: overl.append(f"{fr}:'{text}' {ink*100:.0f}% ink under text")
            r=int(0.03*w); cx,cy=int(bx*w),int(by*h)
            tip=arr[max(0,cy-r):cy+r, max(0,cx-r):cx+r]; tink=(tip<215).mean() if tip.size else 0
            if tink<0.03: miss.append(f"{fr}:'{text}' arrow tip on white ({tink*100:.1f}% ink)")
    add("labels do not cover drawing (ink under text < 6%)", not overl, "; ".join(overl) if overl else "ok")
    add("arrows point at something (ink near tip)", not miss, "; ".join(miss) if miss else "ok")
    add("arrows start outside their text and are not stubs", not badstart and not short, "; ".join(badstart+short) if badstart or short else "ok")
    # 6c. clip drift: static clips must not change more than 15% of pixels first->last, moving clips < 45%
    drift=[]; statics=set(plan.get("static_clips",[]))
    for block in plan["blocks"]:
        for kind,nm,share in block:
            if kind!="clip": continue
            cp=os.path.join(d,"clips",f"{nm}.mp4")
            if not os.path.exists(cp): continue
            tdir=os.path.join(out,"qa_clip"); os.makedirs(tdir,exist_ok=True)
            for f in glob.glob(os.path.join(tdir,"*.png")): os.remove(f)
            subprocess.run(["ffmpeg","-v","error","-y","-i",cp,"-vf","fps=1,scale=320:180",os.path.join(tdir,"c%03d.png")],check=True)
            fr=sorted(glob.glob(os.path.join(tdir,"*.png")))
            if len(fr)<2: continue
            a=np.asarray(Image.open(fr[0]).convert("L")).astype(int); z=np.asarray(Image.open(fr[-1]).convert("L")).astype(int)
            changed=min((np.abs(a-np.roll(np.roll(z,dy,0),dx,1))>40).mean() for dx in range(-8,9,2) for dy in range(-8,9,2))
            lim=0.15 if nm in statics else 0.45
            if changed>lim: drift.append(f"{nm}: {changed*100:.0f}% changed (limit {lim*100:.0f}%)")
    add("animated clips keep the scene (no morphing drift)", not drift, "; ".join(drift) if drift else "ok")
    # 6d. vision heuristics (qa_vision): pair animatability, clip anomalies, clocks vs script, baked marks, hero duplicates
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import qa_vision as qv
        badpairs=[]
        for nm,(fa,fb) in plan.get("clip_pairs",{}).items():
            pa,pb=os.path.join(d,"frames",f"{fa}.png"),os.path.join(d,"frames",f"{fb}.png")
            if os.path.exists(pa) and os.path.exists(pb):
                r=qv.pair_score(pa,pb)
                if not r["animatable"]: badpairs.append(f"{nm}: {fa}->{fb} pixel {r['pixel_diff']:.2f} layout {r['layout_diff']:.2f}")
        add("first/last frame pairs are animatable (same composition)", not badpairs, "; ".join(badpairs) if badpairs else f"{len(plan.get('clip_pairs',{}))} pairs ok")
        anomalies=[]
        for block in plan["blocks"]:
            for kind,nm,share in block:
                if kind=="clip" and os.path.exists(os.path.join(d,"clips",f"{nm}.mp4")):
                    r=qv.clip_report(os.path.join(d,"clips",f"{nm}.mp4"))
                    if not r["ok"]: anomalies.append(f"{nm}: "+"; ".join(r["issues"]))
        if anomalies: warn("clip anomaly hints (look at these clips frame by frame)", " | ".join(anomalies))
        else: add("clip anomaly hints (morph / phantom / multiplication)", True, "none")
        clockmsgs=[]; allow=set(plan.get("allow_clones",[]))
        for bi,block in enumerate(plan["blocks"]):
            times=qv.script_times(blocks[bi])
            for kind,nm,share in block:
                fp=os.path.join(d,"frames",f"{nm}.png")
                if kind!="still" or not os.path.exists(fp): continue
                for c in qv.read_clocks(fp):
                    if not c.get("time"): continue
                    m=qv.clock_matches(c,times)
                    if times and m is False: clockmsgs.append(f"{nm}: clock reads {c['time']}, script says {['%d:%02d'%x for x in times]}")
                    elif not times: clockmsgs.append(f"{nm}: clock reads {c['time']}, no time in this block")
        if clockmsgs: warn("clocks agree with the script (detector reading, verify by eye)", " | ".join(clockmsgs))
        else: add("clocks agree with the script", True, "all readable clocks match")
        marks=[]
        for block in plan["blocks"]:
            for kind,nm,share in block:
                fp=os.path.join(d,"frames",f"{nm}.png")
                if kind=="still" and os.path.exists(fp):
                    mk=qv.isolated_marks(fp)
                    if mk: marks.append(f"{nm}: {len(mk)} at {[tuple(float(x) for x in m['bbox']) for m in mk]}")
        if marks: warn("isolated black marks (possible baked-in arrows/symbols)", " | ".join(marks))
        else: add("no isolated black marks (baked-in arrows)", True, "none")
        if plan.get("hero_color"):
            lo,hi=plan["hero_color"]; dup=[]
            for block in plan["blocks"]:
                for kind,nm,share in block:
                    fp=os.path.join(d,"frames",f"{nm}.png")
                    if kind=="still" and os.path.exists(fp) and nm not in allow:
                        cl=[c for c in qv.hero_clusters(fp,lo,hi) if c[2]>0.012]
                        if len(cl)>1: dup.append(f"{nm}: {len(cl)} hero-coloured figures")
            if dup: warn("hero appears once per frame (colour clusters)", " | ".join(dup))
            else: add("hero appears once per frame (colour clusters)", True, "ok")
    except Exception as e:
        warn("vision heuristics", f"skipped: {type(e).__name__}: {e}")
    # 7. audio loudness + silence
    lo=subprocess.run(["ffmpeg","-i",mp4,"-af","ebur128=peak=true","-f","null","-"],capture_output=True,text=True).stderr
    m=re.search(r"I:\s*(-?\d+\.\d) LUFS", lo.split("Summary:")[-1] if "Summary:" in lo else lo)
    I=float(m.group(1)) if m else None
    add("loudness around -16 LUFS", I is not None and -19 <= I <= -13, f"{I} LUFS" if I is not None else "n/a")
    si=subprocess.run(["ffmpeg","-i",mp4,"-af","silencedetect=noise=-40dB:d=2.5","-f","null","-"],capture_output=True,text=True).stderr
    sil=re.findall(r"silence_duration: ([\d.]+)", si)
    long_sil=[float(x) for x in sil if float(x)>2.5]
    add("no silence gaps > 2.5s", not long_sil, f"{len(long_sil)} gaps" + (f", longest {max(long_sil):.1f}s" if long_sil else ""))
    # 8. thumbnails
    th=glob.glob(os.path.join(out,"thumb_*_1280x720.jpg"))
    badth=[os.path.basename(t) for t in th if Image.open(t).size!=(1280,720) or os.path.getsize(t)>2_000_000]
    add("thumbnails 1280x720 jpg < 2MB", th and not badth, f"{len(th)} thumbnails" + ("; bad: "+", ".join(badth) if badth else ""))
    # 9. faststart
    add("mp4 faststart (moov first)", b"moov" in open(mp4,"rb").read(2_000_000), "")
    # report
    fails=[c for c in checks if c["status"]=="FAIL"]
    rep=[f"# QA report: {os.path.basename(mp4)}", "", f"Duration {D:.1f}s, {len(frames)} sampled frames, {len(checks)} checks, {len(fails)} FAIL", "", "| Check | Status | Detail |","|---|---|---|"]
    rep += [f"| {c['check']} | {c['status']} | {c['detail']} |" for c in checks]
    open(os.path.join(out,"qa_report.md"),"w",encoding="utf8").write("\n".join(rep)+"\n")
    json.dump({"file":mp4,"duration":D,"checks":checks}, open(os.path.join(out,"qa_report.json"),"w"), indent=1, ensure_ascii=False)
    print("\n".join(rep)); sys.exit(1 if fails else 0)
if __name__=="__main__": main()
