"""Cut every separate drawing out of a transparent sprite sheet.
usage: python slice_any.py SHEET.png OUT_DIR [min_area]
Writes OUT_DIR/p01.png, p02.png ... (row-major order, tight crop + 6 px margin) and prints each bbox,
so the parts can be renamed after a look at them."""
import os, sys
import numpy as np
from PIL import Image
from scipy import ndimage

sheet, out = sys.argv[1], sys.argv[2]; amin = int(sys.argv[3]) if len(sys.argv) > 3 else 4000
im = Image.open(sheet).convert('RGBA'); a = np.array(im)[..., 3] > 24
lab, n = ndimage.label(ndimage.binary_closing(a, iterations=3))
boxes = []
for i, sl in enumerate(ndimage.find_objects(lab), 1):
    area = int((lab[sl] == i).sum())
    if area >= amin: boxes.append((sl[0].start, sl[0].stop, sl[1].start, sl[1].stop, i))
H = im.height; boxes.sort(key=lambda b: (round(((b[0] + b[1]) / 2) / (H / 4)), b[2]))   # rough rows, then left to right
os.makedirs(out, exist_ok=True); arr = np.array(im)
for k, (y0, y1, x0, x1, i) in enumerate(boxes, 1):
    m = 6; y0, x0 = max(0, y0 - m), max(0, x0 - m); y1, x1 = min(H, y1 + m), min(im.width, x1 + m)
    crop = arr[y0:y1, x0:x1].copy(); keep = ndimage.binary_dilation(lab[y0:y1, x0:x1] == i, iterations=4); crop[..., 3] = np.where(keep, crop[..., 3], 0)
    Image.fromarray(crop).save(os.path.join(out, f'p{k:02d}.png')); print(f'p{k:02d}', x0, y0, x1 - x0, y1 - y0)
