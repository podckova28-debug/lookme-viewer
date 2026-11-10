"""Slice an AI prop sprite sheet (transparent PNG) into named sprites, in reading order (rows top to bottom, left to right).
usage: python props.py SHEET.png name1 name2 ...   -> anim/cut/props/<name>.png"""
import os, sys
import numpy as np
from PIL import Image
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__))
sheet, names = sys.argv[1], sys.argv[2:]
A = np.array(Image.open(sheet).convert('RGBA')); a = A[..., 3].astype(float)
lab, n = ndimage.label(a > 40); sizes = ndimage.sum(np.ones_like(a), lab, range(1, n + 1)); objs = ndimage.find_objects(lab)
comps = [(objs[i], i + 1) for i in range(n) if sizes[i] > 3000]
if len(comps) != len(names): sys.exit(f'found {len(comps)} sprites, expected {len(names)}')
rowh = A.shape[0] / 3
comps.sort(key=lambda c: (int(((c[0][0].start + c[0][0].stop) / 2) // rowh), c[0][1].start))
os.makedirs(os.path.join(HERE, 'props'), exist_ok=True)
for name, ((sy, sx), k) in zip(names, comps):
    core = ndimage.binary_dilation((lab == k) & (a > 128), iterations=2); ys, xs = np.where(core); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    crop = A[y0:y1, x0:x1].copy()
    crop[..., 3] = np.where(core[y0:y1, x0:x1], (np.clip((crop[..., 3].astype(float) - 110) / 110, 0, 1) * 255), 0).astype(np.uint8)
    Image.fromarray(crop).save(os.path.join(HERE, 'props', name + '.png'), optimize=True)
    print(name, crop.shape[1], 'x', crop.shape[0])
