#!/bin/bash
# usage: sheet.sh SCENE OUT.png t1 t2 ... : stills at given times tiled 3 wide (each 640x360)
S=$1; OUT=$2; shift 2; D=$(mktemp -d)
node ../anim/still.js "ep01.html?scene=$S" $D/f.png "$@"
python3 - "$D" "$OUT" "$@" <<'PY'
import sys, os
from PIL import Image, ImageDraw
d, out, ts = sys.argv[1], sys.argv[2], sys.argv[3:]
ims = [Image.open(os.path.join(d, f'f_{t}.png') if len(ts) > 1 else os.path.join(d, 'f.png')).resize((640, 360)) for t in ts]
cols = 3; rows = (len(ims) + 2) // 3; sh = Image.new('RGB', (cols * 640, rows * 360), 'black')
for i, (im, t) in enumerate(zip(ims, ts)):
    sh.paste(im, ((i % 3) * 640, (i // 3) * 360)); ImageDraw.Draw(sh).text(((i % 3) * 640 + 8, (i // 3) * 360 + 6), t, fill='white')
sh.save(out)
PY
rm -rf $D
