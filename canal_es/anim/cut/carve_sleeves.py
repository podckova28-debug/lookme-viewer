"""Cut painted sleeves off a cut-out torso, so the only sleeve is the one on the moving arm (no doubled arms).
usage: python carve_sleeves.py NAME [NAME ...]   (reads/writes <name>/torso.png; original kept by git)
T-shirts: everything outside the body sides below the armpit is cut (vertical sides up to the shoulder).
Jackets: cut along the traced sleeve seams (SEAMS below: (y, x) points, left and right).
The new edges get the same dark outline as the rest of the part."""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
SEAMS = {   # torso image px: sleeve seam polylines (outside of them is sleeve)
  'valeria': ([(40, 160), (60, 150), (100, 128), (130, 117), (200, 103), (300, 97), (350, 79), (400, 55), (440, 43), (480, 40), (600, 40)],
              [(40, 340), (60, 346), (100, 368), (130, 383), (200, 403), (250, 399), (300, 404), (350, 419), (400, 440), (440, 445), (480, 449), (600, 449)]),
}
OUT = np.array([50, 16, 40])
def interp(poly, ys): py, px = zip(*poly); return np.interp(ys, py, px)
def carve(name):
    im = np.asarray(Image.open(f'{name}/torso.png').convert('RGBA')).astype(float); h, w, _ = im.shape; a = im[:, :, 3] > 128
    ys = np.arange(h)
    if name in SEAMS:
        xl, xr = interp(SEAMS[name][0], ys), interp(SEAMS[name][1], ys)
    else:   # T-shirt: armpit = first row below the widest (sleeve) rows where the sides step inwards
        L = np.array([np.argmax(r) if r.any() else w for r in a]); R = np.array([w - 1 - np.argmax(r[::-1]) if r.any() else -1 for r in a])
        wid = R - L; ytop = int(np.argmax(wid > 0)); yw = int(np.argmax(wid)); ya = yw
        while ya < h - 1 and not (L[ya] - L[yw] > .55 * (L[ya + 40] - L[yw] if ya + 40 < h else 1) and wid[ya] < wid[yw] - 60): ya += 1
        ya = min(h - 1, ya + 12); xl0, xr0 = L[ya], R[ya]
        yb = min(h - 1, ya + 45)   # below the armpit, blend from the cut line into the body side (no leftover sleeve hem ticks)
        xl = np.where(ys < ya, xl0, np.where(ys < yb, xl0 + (L[yb] - xl0) * (ys - ya) / (yb - ya), -1.0))
        xr = np.where(ys < ya, xr0, np.where(ys < yb, xr0 + (R[yb] - xr0) * (ys - ya) / (yb - ya), w + 1.0))
        # the painted armhole seam bows inwards between shoulder and armpit: cut along a bow just inside it
        yb = min(h - 1, ya + 70); xl = np.where(ys < yb, np.minimum(xl0, np.where(ys < ya, xl0, xl0 + (L[yb] - xl0) * (ys - ya) / (yb - ya))), -1.0)
        xr = np.where(ys < yb, np.maximum(xr0, np.where(ys < ya, xr0, xr0 + (R[yb] - xr0) * (ys - ya) / (yb - ya))), w + 1.0)
        ysh = ytop + .25 * (ya - ytop); u = np.clip((ys - ysh) / (yb - ysh), 0, 1); bow = (6 * (1 - u) + 30 * np.sin(np.pi * u) * (ys >= ysh)) * (ys < yb)
        xl = np.where(ys < yb, xl + bow, xl); xr = np.where(ys < yb, xr - bow, xr)
        print(name, 'armpit row', ya, 'body sides', xl0, xr0)
    X = np.arange(w)[None, :]
    keep = (X >= xl[:, None]) & (X <= xr[:, None])
    keep = ndi.gaussian_filter(keep.astype(float), 14) > .5         # round the shoulder corners
    newa = a & keep
    cut = a & ~keep                                                   # removed sleeve pixels
    edge = newa & ~ndi.binary_erosion(newa, iterations=7)             # a 7 px band along the new silhouette
    near_cut = ndi.binary_dilation(cut, iterations=9)
    out = im.copy()
    paint = edge & near_cut
    lum = im[:, :, :3].mean(2)
    out[paint, :3] = OUT * .92 + out[paint, :3] * .08
    alpha = np.where(newa, im[:, :, 3], 0.0)
    alpha = np.where(cut, 0.0, alpha)
    # 1 px antialias on the cut edge
    soft = ndi.gaussian_filter(newa.astype(float), .8)
    alpha = np.where(near_cut, np.minimum(im[:, :, 3], soft * 255), alpha)
    out[:, :, 3] = alpha
    Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(f'{name}/torso.png')
    print(name, 'carved', int(cut.sum()), 'px')
for n in sys.argv[1:]: carve(n)
