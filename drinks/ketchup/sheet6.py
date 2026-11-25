# 3x2 sheet at 640x360 per frame for close anatomy check: python3 sheet6.py 1
import sys; from PIL import Image, ImageDraw
a=int(sys.argv[1]); W,H=640,360
S=Image.new("RGB",(W*3,H*2),"white"); d=ImageDraw.Draw(S)
for k,i in enumerate(range(a,min(a+6,131))):
    S.paste(Image.open(f"frames/jpg/f{i:02d}.jpg").resize((W,H)),((k%3)*W,(k//3)*H)); d.text(((k%3)*W+4,(k//3)*H+4),str(i),fill="red")
S.save(f"/tmp/claude-0/-home-user-lookme-viewer/e6a327de-202d-5d69-ad39-e0c29b61606a/scratchpad/s6_{a:03d}.jpg",quality=88)
