import cv2, numpy as np, sys
src, out = sys.argv[1], sys.argv[2]
img = cv2.imread(src)
H, W = img.shape[:2]
s = W / 768.0
p_max = np.array([551, 743]) * s   # hole further from the tip (MAX)
p_min = np.array([604, 763]) * s   # hole closer to the tip (MIN)
d = (p_min - p_max); d /= np.linalg.norm(d)
cut = (p_max + p_min) / 2
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
yy, xx = np.mgrid[0:H, 0:W]
proj = (xx - cut[0]) * d[0] + (yy - cut[1]) * d[1]
perp = -(xx - cut[0]) * d[1] + (yy - cut[1]) * d[0]
gold = (hsv[..., 0] >= 12) & (hsv[..., 0] <= 32) & (hsv[..., 1] > 35) & (hsv[..., 2] > 70)
zone = (proj < 0) & (np.abs(perp) < 40 * s) & (xx > 300 * s) & (yy > 600 * s) & (yy < 800 * s)
m = gold & zone
g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
steel = np.clip(140 + (g - g[m].mean()) * 0.9 + 45, 0, 255) if m.any() else g
outimg = img.copy()
for c, k in enumerate((1.03, 1.0, 0.97)):   # slightly cool steel tint (BGR)
    ch = outimg[..., c].astype(np.float32)
    ch[m] = np.clip(steel[m] * k, 0, 255)
    outimg[..., c] = ch.astype(np.uint8)
# soften the seam
mm = cv2.dilate(m.astype(np.uint8), np.ones((3, 3), np.uint8))
blur = cv2.GaussianBlur(outimg, (3, 3), 0)
outimg[mm > 0] = blur[mm > 0]
cv2.imwrite(out, outimg)
print('pixels', int(m.sum()))
