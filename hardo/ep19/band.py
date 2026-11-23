import sys,numpy as np,shutil
from PIL import Image
for f in sys.argv[1:]:
    p=f'frames/{f}.png'; shutil.copy(p,f'old/band/{f}.png')
    a=np.asarray(Image.open(p).convert('RGB')).astype(np.float32); h,w,_=a.shape
    ink=(a.min(2)<212)
    top=ink[:int(h*.22)].mean(); bot=ink[int(h*.78):].mean()
    y=np.arange(h)/h
    if top<=bot: al=np.clip((0.27-y)/0.12,0,1)   # full white above 15%, fades out by 27%
    else: al=np.clip((y-0.73)/0.12,0,1)
    al=al[:,None,None]**1.2
    out=a*(1-al)+255*al
    Image.fromarray(out.astype('uint8')).save(p); print(f,'top' if top<=bot else 'bottom')
