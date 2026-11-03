"""Paint a navy-blue figure (e.g. a stray bus driver) out of a frame range, per frame, with OpenCV inpaint.

usage: python3 tools/remove_blue.py IN.mp4 OUT.mp4 F0 F1 "x0,y0,x1,y1"
Only pixels in the box (in source pixels) with navy hue are masked; audio is copied.
"""
import sys, subprocess, numpy as np, cv2
src, dst, f0, f1, box = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), list(map(int, sys.argv[5].split(',')))
w, h = map(int, subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', src]).decode().split(','))
rd = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE)
wr = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{w}x{h}', '-r', '24', '-i', '-', '-i', src,
                       '-map', '0:v', '-map', '1:a?', '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', '-c:a', 'copy', dst], stdin=subprocess.PIPE)
x0, y0, x1, y1 = box; n = 0; k = np.ones((5, 5), np.uint8)
while True:
    b = rd.stdout.read(w * h * 3)
    if len(b) < w * h * 3: break
    fr = np.frombuffer(b, np.uint8).reshape(h, w, 3).copy()
    if f0 <= n <= f1:
        hsv = cv2.cvtColor(fr, cv2.COLOR_BGR2HSV)
        m = ((hsv[..., 0] > 100) & (hsv[..., 0] < 130) & (hsv[..., 1] > 70) & (hsv[..., 2] < 200)).astype(np.uint8) * 255
        roi = np.zeros_like(m); roi[y0:y1, x0:x1] = 255; m &= roi
        m = cv2.dilate(cv2.morphologyEx(m, cv2.MORPH_CLOSE, k), k, iterations=2)
        if m.any(): fr = cv2.inpaint(fr, m, 7, cv2.INPAINT_TELEA)
    wr.stdin.write(fr.tobytes()); n += 1
wr.stdin.close(); wr.wait(); rd.wait(); print('frames', n)
