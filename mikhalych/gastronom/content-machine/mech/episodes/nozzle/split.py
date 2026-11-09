"""split.py — муфта в разрезе: половинки сначала сомкнуты, потом расходятся (без нейросети, из клипа c3_still).
Половинки — ровно те же пиксели, что в клипе: формы не меняются. Капли в зазоре проявляются после разъединения."""
import cv2, numpy as np, sys
src, out = 'clips/c3_still.mp4', 'clips/c3_split.mp4'
T_JOIN = float(sys.argv[1]) if len(sys.argv) > 1 else 1.3   # сколько держим сомкнутыми (под слово «расстёгивается»)
SHIFT = int(sys.argv[3]) if len(sys.argv) > 3 else 0          # сдвиг вверх, px исходника
T_SPLIT = 0.45                                               # сколько длится разъединение
T_TOTAL = float(sys.argv[2]) if len(sys.argv) > 2 else None  # длина клипа; кадры исходника идут туда-обратно
cap = cv2.VideoCapture(src); fps = cap.get(5); frames = []
while True:
    ok, f = cap.read()
    if not ok: break
    frames.append(f)
H, W = frames[0].shape[:2]
f0 = frames[0].astype(np.int16)
bg = np.median(np.concatenate([f0[:40, :40].reshape(-1, 3), f0[:40, -40:].reshape(-1, 3)]), axis=0)
diff = np.abs(f0 - bg).sum(2) > 40                      # не фон
cols = diff[:, int(W * 0.2):int(W * 0.8)].mean(1)        # доля «не фона» в строке (центральная полоса)
empty = cols < 0.07                                      # только капли
mid = H // 2; best = (0, 0)
y = int(H * 0.3)
while y < int(H * 0.7):
    if empty[y]:
        y0 = y
        while y < H and (empty[y] or empty[min(y + 12, H - 1)]): y += 1   # капли не рвут зазор
        if y - y0 > best[1] - best[0]: best = (y0, y)
    y += 1
g0, g1 = best; d = (g1 - g0) / 2
print('fps', fps, 'size', W, H, 'зазор', g0, g1, 'сдвиг', d)
n_total = len(frames)
def ease(x):                                              # с лёгким «щелчком» в конце
    x = min(max(x, 0), 1); c = 1.7
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2
vw = cv2.VideoWriter(out, cv2.VideoWriter_fourcc(*'mp4v'), fps, (W, H))
N = int(round((T_TOTAL or len(frames) / fps) * fps)); P = 2 * len(frames) - 2
for i in range(N):
    j = i % P; f = frames[j if j < len(frames) else P - j]   # пузырьки внутри — туда-обратно, детали стоят
    t = i / fps
    k = 1 - ease((t - T_JOIN) / T_SPLIT)                  # 1 — сомкнуты, 0 — разошлись
    off = int(round(d * k))
    canvas = np.empty_like(f)
    canvas[:] = f[g0:g1].mean(axis=(0, 1)) if False else bg.astype(np.uint8)
    # зазор с каплями — из самого кадра, капли проявляются по мере разъединения
    gap = f[g0:g1].astype(np.float32); base = np.empty_like(gap); base[:] = bg
    a = 1 - k
    canvas[g0:g1] = (base * (1 - a) + gap * a).astype(np.uint8)
    top = f[:g0]; bot = f[g1:]
    def paste(part, y):                                   # вставка с обрезкой по краям кадра
        a0, b0 = max(y, 0), min(y + len(part), H)
        if b0 > a0: canvas[a0:b0] = part[a0 - y:b0 - y]
    paste(top, off)
    if off > 0: canvas[:off] = top[:1]
    paste(bot, g1 - off)
    if off > 0: canvas[H - off:] = bot[-1:]
    if off < 0:                                           # «щелчок» дальше конечной точки: дотянуть шланги
        canvas[H + off:] = bot[-1:]
    if SHIFT:                                             # поднять муфту над субтитрами; шланг внизу дотянуть
        canvas = np.concatenate([canvas[SHIFT:], np.repeat(canvas[-1:], SHIFT, axis=0)])
    vw.write(canvas)
vw.release(); print('кадров', N, out)
