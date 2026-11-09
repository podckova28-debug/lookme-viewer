import sys, subprocess, imageio_ffmpeg, numpy as np
from PIL import Image, ImageDraw, ImageFont
FF=imageio_ffmpeg.get_ffmpeg_exe()
f=ImageFont.truetype('/home/user/gastronom/content-machine/video/fonts/Nunito-Black.ttf',22)
clip,a,b,st,cols,out=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),int(sys.argv[5]),sys.argv[6]
ts=list(np.arange(a,b+1e-6,st)); ims=[]
for t in ts:
    raw=subprocess.run([FF,'-v','error','-ss',f'{t:.3f}','-i',clip,'-frames:v','1','-vf','scale=400:-1','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
    h=len(raw)//(400*3); im=Image.fromarray(np.frombuffer(raw,np.uint8).reshape(h,400,3)); ImageDraw.Draw(im).text((5,5),f'{t:.2f}',fill='red',font=f); ims.append(im)
rows=(len(ims)+cols-1)//cols; W=Image.new('RGB',(400*cols,h*rows))
for i,im in enumerate(ims): W.paste(im,((i%cols)*400,(i//cols)*h))
W.save(out,quality=82)
