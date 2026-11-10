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
    mm = ndimage.binary_dilation(lab == k, iterations=3)[sy.start - 3 if sy.start >= 3 else 0:sy.stop + 3, sx.start - 3 if sx.start >= 3 else 0:sx.stop + 3]
    crop = A[max(0, sy.start - 3):sy.stop + 3, max(0, sx.start - 3):sx.stop + 3].copy()
    crop[..., 3] = np.where(mm, (np.clip((crop[..., 3].astype(float) - 40) / 160, 0, 1) * 255), 0).astype(np.uint8)
    Image.fromarray(crop).save(os.path.join(HERE, 'props', name + '.png'), optimize=True)
    print(name, crop.shape[1], 'x', crop.shape[0])
