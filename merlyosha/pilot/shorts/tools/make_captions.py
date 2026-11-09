# Word-synced Shorts captions (ASS) from faster-whisper word timestamps.
import json, re, sys
words=json.load(open("shorts_words.json",encoding="utf-8"))
fix={"Первое":"Первая","мнёться":"мнётся"}
clean=[]
for w in words:
    t=w["w"].strip(" ,.?!–-—")
    if not t: continue
    t=fix.get(t,t)
    if t=="%" and clean: clean[-1]["w"]+="%"; clean[-1]["e"]=w["e"]; continue
    clean.append({"w":t,"s":w["s"],"e":w["e"]})
# phrase boundaries from the script (end of sentence) -> never join across them
ends={"переплачиваете","отжима","влажности","сильнее","1200","программы","тремя","быстрая","полоскание","нужна","канале","понимают"}
# manual phrase chunks (word counts) tuned for reading rhythm
j=[]
for w in clean:
    if j and j[-1]["w"]=="1000" and w["w"]=="1200": j[-1]["w"]="1000–1200"; j[-1]["e"]=w["e"]; continue
    j.append(w)
clean=j
sizes=[2,3,2,2,1,2,1,3,2,2,3,1,1,1,2,3,2,2,2,1,1,1,3,1,1,3,4,2,3,2,2,3]
assert sum(sizes)==len(clean), (sum(sizes),len(clean)," ".join(x["w"] for x in clean))
chunks=[]; p=0
for n in sizes: chunks.append(clean[p:p+n]); p+=n
cur=[]
if cur: chunks.append(cur)
def ts(x): h=int(x//3600); m=int(x%3600//60); s=x%60; return f"{h}:{m:02d}:{s:05.2f}"
hdr="""[Script Info]
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Montserrat,92,&H00FFFFFF,&H00FFFFFF,&H00202020,&H80000000,-1,0,0,0,100,100,1,0,1,8,3,5,60,60,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ev=[]
HL="&HA5E763&"  # mint #63E7A5 in BGR
for i,ch in enumerate(chunks):
    cs=ch[0]["s"]; ce=chunks[i+1][0]["s"] if i+1<len(chunks) else ch[-1]["e"]+0.6
    for j,w in enumerate(ch):
        ws=w["s"]; we=ch[j+1]["s"] if j+1<len(ch) else ce
        txt=" ".join((f"{{\\c{HL}}}{x['w'].upper()}{{\\c&HFFFFFF&}}" if k==j else x["w"].upper()) for k,x in enumerate(ch))
        ev.append(f"Dialogue: 0,{ts(ws)},{ts(we)},Cap,,0,0,0,,{{\\pos(540,1180)\\fad(40,0)}}{txt}")
open("shorts_captions.ass","w",encoding="utf-8").write(hdr+"\n".join(ev)+"\n")
print(len(chunks),"chunks;", " | ".join(" ".join(x["w"] for x in c) for c in chunks))
