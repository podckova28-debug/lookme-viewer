# Shorts v2: 13 shots cut on word timings, number overlays, word-synced captions.
import json, os, subprocess
P="/home/user/lookme-viewer/merlyosha/pilot/shorts"; S=os.path.dirname(os.path.abspath(__file__))
V="/home/user/lookme-viewer/merlyosha/pilot/voice/shorts-02-voice.mp3"
W,H,FPS=1080,1920,30
def run(c): subprocess.run(c,shell=True,check=True)
words=json.load(open(f"{S}/shorts2_words.json",encoding="utf-8"))
clean=[]
for w in words:
    t=w["w"].strip(" ,.?!–-—:")
    if not t: continue
    if t=="%" and clean: clean[-1]["w"]+="%"; clean[-1]["e"]=w["e"]; continue
    clean.append({"w":t,"s":w["s"],"e":w["e"]})
for i,w in enumerate(clean):
    if w["w"]=="из" and i+1<len(clean) and clean[i+1]["w"]=="гарантии": w["w"]="и с"; clean[i+1]["w"]="гарантией"
    w["w"]={"четырех":"четырёх","шланге":"шланги","ее":"её"}.get(w["w"],w["w"])
assert len(clean)==92, len(clean)
sizes=[3,4,1,2,2,2, 2,2,2,2,2,2, 3,3,2,2,2,2, 2, 2,1,3,2,1,1, 2,1,2,3, 2,3,2,2,1, 1,2,2,2,2,2,2, 2,2, 2,3]
assert sum(sizes)==92, sum(sizes)
chunks=[]; p=0
for n in sizes: chunks.append(clean[p:p+n]); p+=n
def T(i): return clean[i]["s"]            # start of token i
def find(word,nth=0):
    k=[i for i,w in enumerate(clean) if w["w"]==word][nth]; return k
END=clean[-1]["e"]+0.6
def ts(x): h=int(x//3600); m=int(x%3600//60); s=x%60; return f"{h}:{m:02d}:{s:05.2f}"
HL="&HA5E763&"
hdr=f"""[Script Info]
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Montserrat,88,&H00FFFFFF,&H00FFFFFF,&H00202020,&H80000000,-1,0,0,0,100,100,1,0,1,8,3,5,60,60,0,1
Style: Num,Montserrat,170,&H00FFFFFF,&H00FFFFFF,&H00202020,&H80000000,-1,0,0,0,100,100,0,0,1,12,4,5,40,40,0,1
Style: NumRed,Montserrat,170,&H005252FF,&H00FFFFFF,&H00202020,&H80000000,-1,0,0,0,100,100,0,0,1,12,4,5,40,40,0,1
Style: NumGreen,Montserrat,170,&HA5E763,&H00FFFFFF,&H00202020,&H80000000,-1,0,0,0,100,100,0,0,1,12,4,5,40,40,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ev=[]
# captions (layer 0, lower-middle)
for i,ch in enumerate(chunks):
    ce=chunks[i+1][0]["s"] if i+1<len(chunks) else END
    for j,w in enumerate(ch):
        ws=w["s"]; we=ch[j+1]["s"] if j+1<len(ch) else ce
        txt=" ".join((f"{{\\c{HL}}}{x['w'].upper()}{{\\c&HFFFFFF&}}" if k==j else x["w"].upper()) for k,x in enumerate(ch))
        ev.append(f"Dialogue: 0,{ts(ws)},{ts(we)},Cap,,0,0,0,,{{\\pos(540,1290)\\fad(30,0)}}{txt}")
# number overlays (layer 1, top area) with pop-in
POP="\\fscx40\\fscy40\\t(0,140,\\fscx100\\fscy100)"
def ov(start,end,text,style="Num",y=420,x=540):
    n=len(text); fs=170 if n<=7 else (135 if n<=10 else 108)
    ev.append(f"Dialogue: 1,{ts(start)},{ts(end)},{style},,0,0,0,,{{\\pos({x},{y})\\an5\\fs{fs}{POP}\\fad(0,120)}}{text}")
i30=find("30"); i60=find("60"); iTys=find("тысяч")
ov(T(i30),T(iTys)+0.9,"30 000 ₽","Num",380)
ov(T(i60),T(iTys)+0.9,"60 000 ₽","NumRed",600)
ov(T(find("четыре")),T(find("переплачиваете"))+0.7,"4 ЦИФРЫ","NumRed",420)
ov(T(find("1400")),T(find("это")),"1400","NumRed",380)
ov(T(find("1200")),T(find("это")),"vs 1200","NumGreen",600)
ov(T(find("минус")),T(find("плюс")),"−10% ВЛАГИ","Num",420)
ov(T(find("мятые")),T(find("Загрузка")),"+ МЯТЫЕ","NumRed",420)
ov(T(find("10",0)),T(find("хватает")),"10 КГ","NumRed",420)
ov(T(find("восьми")),T(find("остальное")),"8 КГ ХВАТИТ","NumGreen",420)
ov(T(find("остальное")),T(find("24")),"ЛИШНЕЕ = ВОЗДУХ","Num",420)
ov(T(find("24")),T(find("тремя")),"24 ПРОГРАММЫ","NumRed",420)
ov(T(find("тремя")),T(find("а")),"НУЖНЫ 3","NumGreen",420)
ov(T(find("одну")),T(find("Инверторный")),"1 КНОПКА","NumGreen",420)
ov(T(find("10",1)),T(find("Нужен")),"ДО 10 ЛЕТ","Num",420)
ov(T(find("кухне")),T(find("в")),"КУХНЯ: ДА","NumGreen",420)
ov(T(find("ванной")),T(find("Бонус")),"ВАННАЯ: НЕТ","NumRed",420)
ov(T(find("5")),T(find("иначе")),"+5 СМ","NumGreen",420)
ov(T(find("Полный")),END,"ПОЛНЫЙ РАЗБОР","Num",420)
open(f"{S}/shorts2.ass","w",encoding="utf-8").write(hdr+"\n".join(ev)+"\n")
# shots keyed to words
shots=[("clip",f"{P}/clips/01-hook.mp4",0.0,T(find("Отжим"))),
       ("clip",f"{P}/clips/02-spin.mp4",T(find("Отжим")),T(find("плюс"))),
       ("in",f"{P}/frames/03-wrinkled.png",T(find("плюс")),T(find("Загрузка"))),
       ("out",f"{P}/frames/04-empty-drum.png",T(find("Загрузка")),T(find("хватает"))),
       ("in",f"{P}/frames/05-full-drum.png",T(find("хватает")),T(find("остальное"))),
       ("pan",f"{P}/frames/04-empty-drum.png",T(find("остальное")),T(find("24"))),
       ("clip",f"{P}/clips/04-programs.mp4",T(find("24")),T(find("а"))),
       ("in",f"{P}/frames/07-press-button.png",T(find("а")),T(find("Инверторный"))),
       ("pan",f"{P}/frames/08-motor.png",T(find("Инверторный")),T(find("Нужен"))),
       ("out",f"{P}/frames/10-measure.png",T(find("Нужен")),T(find("в"))),
       ("clip",f"{P}/clips/03-shake.mp4",T(find("в")),T(find("Бонус"))),
       ("in",f"{P}/frames/10-measure.png",T(find("Бонус")),T(find("иначе"))),
       ("in",f"{P}/frames/11-door-stuck.png",T(find("иначе")),T(find("Полный"))),
       ("clip",f"{P}/clips/05-cta.mp4",T(find("Полный")),END)]
segs=[]
for i,(kind,src,a,b) in enumerate(shots):
    d=b-a; out=f"{S}/s2_{i:02d}.mp4"
    if kind=="clip":
        slow=max(0.8,min(d/5.0,1.5))
        run(f'ffmpeg -y -loglevel error -i "{src}" -vf "setpts={slow}*PTS,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},tpad=stop_mode=clone:stop_duration=30" -t {d:.3f} -an -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p "{out}"')
    else:
        fr=int(d*FPS)+1
        if kind=="in":  z=f"'min(1.0+0.12*on/{fr},1.12)'"; x="'iw/2-(iw/zoom/2)'"
        elif kind=="out": z=f"'max(1.12-0.12*on/{fr},1.0)'"; x="'iw/2-(iw/zoom/2)'"
        else: z="1.12"; x=f"'(iw-iw/zoom)*on/{fr}'"
        run(f'ffmpeg -y -loglevel error -loop 1 -i "{src}" -vf "scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,zoompan=z={z}:x={x}:y=\'ih/2-(ih/zoom/2)\':d={fr}:s={W}x{H}:fps={FPS}" -t {d:.3f} -an -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p "{out}"')
    segs.append(out)
open(f"{S}/s2list.txt","w").write("".join(f"file '{s}'\n" for s in segs))
run(f'ffmpeg -y -loglevel error -f concat -safe 0 -i "{S}/s2list.txt" -c copy "{S}/s2_noaudio.mp4"')
run(f'cd "{S}" && ffmpeg -y -loglevel error -i s2_noaudio.mp4 -i "{V}" -vf "ass=shorts2.ass:fontsdir=../fonts" -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -c:a aac -b:a 160k -shortest "{P}/render/shorts-02-9x16.mp4"')
print("done", len(shots), "shots")
