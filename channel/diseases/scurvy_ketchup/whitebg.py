"""Turn a dark/vignette background white: flood-fill from the frame border over smooth (low-texture) pixels, feather the edge."""
import sys, numpy as np, cv2
from PIL import Image
def whiten(src, dst):
    im = np.asarray(Image.open(src).convert('RGB').resize((1920, 1080), Image.LANCZOS)).astype(np.float32)
    g = cv2.cvtColor(im.astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(np.float32)
    tex = cv2.GaussianBlur(np.abs(cv2.Laplacian(g, cv2.CV_32F, ksize=3)), (0, 0), 3)
    smooth = (tex < 6).astype(np.uint8)
    smooth = cv2.morphologyEx(smooth, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    n, lab = cv2.connectedComponents(smooth)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(border)).astype(np.float32)
    bg = cv2.GaussianBlur(cv2.erode(bg, np.ones((3, 3), np.uint8)), (0, 0), 4)[..., None]
    out = im * (1 - bg) + 255 * bg
    Image.fromarray(out.clip(0, 255).astype(np.uint8)).save(dst, quality=93)
if __name__ == '__main__':
    for i in sys.argv[1:]: whiten(f'raw/{i}.png', f'f/{i}.jpg')
