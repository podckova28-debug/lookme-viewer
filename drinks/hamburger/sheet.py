# contact sheet 4x3: python3 sheet.py 1 12 -> scratchpad sheet_01.jpg
import sys,os; from PIL import Image, ImageDraw
a,b=int(sys.argv[1]),int(sys.argv[2]); W,H=480,270
S=Image.new("RGB",(W*4,H*3),"white"); d=ImageDraw.Draw(S)
for k,i in enumerate(range(a,b+1)):
    f=f"frames/jpg/f{i:02d}.jpg" if i<100 else f"frames/jpg/f{i}.jpg"
    if os.path.exists(f): S.paste(Image.open(f).resize((W,H)),((k%4)*W,(k//4)*H))
    d.rectangle([(k%4)*W,(k//4)*H,(k%4)*W+40,(k//4)*H+22],fill="black"); d.text(((k%4)*W+4,(k//4)*H+4),str(i),fill="white")
S.save(os.environ.get("OUT","/tmp/claude-0/-home-user-lookme-viewer/e6a327de-202d-5d69-ad39-e0c29b61606a/scratchpad")+f"/sheet_{a:03d}.jpg",quality=85)
