# usage: python3 sheet.py OUT.png img1 img2 ...   (labels each tile with its file name time)
import sys, cv2, numpy as np, re
out, files = sys.argv[1], sys.argv[2:]
tiles = []
for f in files:
    im = cv2.resize(cv2.imread(f), (640, 360)); lab = re.sub(r'.*/s', '', f).replace('.jpg', '')
    cv2.rectangle(im, (0, 0), (150, 30), (0, 0, 0), -1); cv2.putText(im, lab, (6, 22), 0, .7, (0, 255, 255), 2); tiles.append(im)
while len(tiles) % 3: tiles.append(np.zeros_like(tiles[0]))
cv2.imwrite(out, np.vstack([np.hstack(tiles[i:i + 3]) for i in range(0, len(tiles), 3)]))
