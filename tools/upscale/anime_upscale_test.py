import sys, time, torch, torch.nn as nn, torch.nn.functional as F, cv2, numpy as np
class SRVGG(nn.Module):
    def __init__(s, nf=64, nc=16, up=4):
        super().__init__(); s.up = up
        b = [nn.Conv2d(3, nf, 3, 1, 1), nn.PReLU(nf)]
        for _ in range(nc): b += [nn.Conv2d(nf, nf, 3, 1, 1), nn.PReLU(nf)]
        b.append(nn.Conv2d(nf, 3 * up * up, 3, 1, 1)); s.body = nn.ModuleList(b); s.ps = nn.PixelShuffle(up)
    def forward(s, x):
        o = x
        for l in s.body: o = l(o)
        return s.ps(o) + F.interpolate(x, scale_factor=s.up, mode='nearest')
torch.set_num_threads(4)
m = SRVGG(); sd = torch.load('animev3.pth', map_location='cpu'); m.load_state_dict(sd.get('params', sd.get('params_ema', sd))); m.eval()
src, t = sys.argv[1], float(sys.argv[2])
cap = cv2.VideoCapture(src); cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000); ok, f = cap.read()
x = torch.from_numpy(f[:, :, ::-1].copy()).permute(2, 0, 1).float()[None] / 255
t0 = time.time()
with torch.no_grad(): y = m(x)
print('sec/frame', round(time.time() - t0, 2), f.shape)
y = (y[0].clamp(0, 1).permute(1, 2, 0).numpy()[:, :, ::-1] * 255).astype(np.uint8)
a = cv2.resize(f, (1920, 1080), interpolation=cv2.INTER_LANCZOS4); b = cv2.resize(y, (1920, 1080), interpolation=cv2.INTER_AREA)
cv2.imwrite(sys.argv[3] + '_plain.png', a); cv2.imwrite(sys.argv[3] + '_up.png', b)
c = lambda im: im[250:700, 650:1450]
cv2.imwrite(sys.argv[3] + '_cmp.png', np.hstack([c(a), c(b)]))
