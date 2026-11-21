import sys,numpy as np
from PIL import Image
def fade(path,target=136):
    im=np.asarray(Image.open(path).convert('RGB')).astype(np.float32)
    h,w,_=im.shape
    y,x=np.mgrid[0:h,0:w]
    cx,cy=w*0.42,h*0.48
    r=np.sqrt(((x-cx)/(w*0.62))**2+((y-cy)/(h*0.62))**2)
    for g in np.arange(0.0,0.5,0.01):
        for r0 in (0.75,0.6,0.45):
            a=np.clip((r-r0)/(1.05-r0),0,1)**1.4
            a=np.clip(a+g,0,1)[...,None]
            out=im*(1-a)+255*a
            m=(0.299*out[...,0]+0.587*out[...,1]+0.114*out[...,2]).mean()
            if m>=target: return out,m,g,r0
    return out,m,g,r0
for f in sys.argv[1:]:
    p=f'frames/{f}.png'
    import shutil; shutil.copy(p,f'old/dark/{f}.png')
    out,m,g,r0=fade(p)
    Image.fromarray(out.clip(0,255).astype('uint8')).save(p)
    print(f,round(m),round(g,2),r0)
