/* Backgrounds, rendered once into offscreen canvases (+ blurred copies for close-ups). */
const BGS = {};
function mk() { const c = document.createElement('canvas'); c.width = W; c.height = H; return [c, c.getContext('2d')]; }
function blurOf(c, px = 7) { const [b, g] = mk(); g.filter = `blur(${px}px)`; g.drawImage(c, 0, 0); return b; }
function lg(g, y0, y1, stops) { const gr = g.createLinearGradient(0, y0, 0, y1); stops.forEach(([o, c]) => gr.addColorStop(o, c)); return gr; }
function fillR(g, x, y, w, h, r, col, lw = 4) { shape(g, q => rrPath(q, x, y, w, h, r), col, lw); }
function vignette(g, a = .5) { const gr = g.createRadialGradient(W / 2, H * .55, 300, W / 2, H * .55, 1250); gr.addColorStop(0, 'rgba(0,0,0,0)'); gr.addColorStop(1, `rgba(0,0,0,${a})`); g.fillStyle = gr; g.fillRect(0, 0, W, H); }
function skyline(g, x0, x1, base, seed, cols, lit = .28) {
  const r = rng(seed);
  for (const [col, hmin, hmax, gap] of cols) for (let x = x0 - 20; x < x1;) {
    const bw = 50 + r() * 90, bh = hmin + r() * (hmax - hmin), by = base - bh; g.fillStyle = col; g.fillRect(x, by, bw, bh);
    if (r() < .3) { g.fillRect(x + bw * .3, by - 26, 22, 26); g.fillRect(x + bw * .3 + 4, by - 34, 14, 8); }
    g.fillStyle = 'rgba(255,214,140,.85)'; for (let yy = by + 14; yy < base - 8; yy += 20) for (let xx = x + 8; xx < x + bw - 8; xx += 15) if (r() < lit) g.fillRect(xx, yy, 6, 8);
    x += bw + gap;
  }
}

/* kitchen at dusk with the big window on the right (window rect is exported for cracks / tape) */
const KWIN = { x: 1120, y: 120, w: 760, h: 430 };
function bgKitchen(day = false) {
  const [b, g] = mk(); const { x: wx, y: wy, w: ww, h: wh } = KWIN;
  g.fillStyle = lg(g, 0, H, day ? [[0, '#5a4a63'], [.6, '#665470'], [1, '#54445c']] : [[0, '#3d2f47'], [.6, '#4a3a52'], [1, '#3a2e44']]); g.fillRect(0, 0, W, H);
  g.save(); g.beginPath(); g.rect(wx, wy, ww, wh); g.clip();
  g.fillStyle = lg(g, wy, wy + wh, day ? [[0, '#7fb3e0'], [.7, '#cfe4f2'], [1, '#f2e6c8']] : [[0, '#3e3156'], [.5, '#8a5d7c'], [.85, '#e7a26a'], [1, '#f7cf8a']]); g.fillRect(wx, wy, ww, wh);
  if (!day) { const sx = wx + 520, sy = wy + wh - 34; g.globalAlpha = .16; g.fillStyle = '#ffe7b0';
    for (let i = 0; i < 9; i++) { const a = -Math.PI * .95 + i * Math.PI * .11; g.beginPath(); g.moveTo(sx, sy); g.lineTo(sx + Math.cos(a - .035) * 900, sy + Math.sin(a - .035) * 900); g.lineTo(sx + Math.cos(a + .035) * 900, sy + Math.sin(a + .035) * 900); g.fill(); }
    g.globalAlpha = 1; g.fillStyle = '#ffe8b4'; g.beginPath(); g.arc(sx, sy, 46, Math.PI, 0); g.fill(); }
  skyline(g, wx, wx + ww, wy + wh, 11, day ? [['#9fb0cf', 60, 170, 30], ['#7d8db0', 110, 250, 6]] : [['#5a456c', 60, 170, 30], ['#45344f', 110, 250, 6]], day ? .05 : .28);
  g.restore();
  g.strokeStyle = OUT; g.lineWidth = 14; g.strokeRect(wx, wy, ww, wh); g.lineWidth = 9; g.beginPath(); g.moveTo(wx + ww / 2, wy); g.lineTo(wx + ww / 2, wy + wh); g.moveTo(wx, wy + wh * .38); g.lineTo(wx + ww, wy + wh * .38); g.stroke();
  const gr = g.createRadialGradient(wx + ww * .6, wy + wh, 30, wx + ww * .6, wy + wh, 1100); gr.addColorStop(0, day ? 'rgba(255,245,220,.18)' : 'rgba(255,190,120,.20)'); gr.addColorStop(1, 'rgba(255,190,120,0)'); g.fillStyle = gr; g.fillRect(0, 0, W, H);
  for (let i = 0; i < 4; i++) { const x = 40 + i * 262; fillR(g, x, 96, 240, 268, 6, '#564460'); g.fillStyle = '#e0b45c'; g.beginPath(); rrPath(g, x + 212, 212, 9, 40, 4); g.fill(); }
  shape(g, q => q.rect(-10, 604, W + 20, 30), '#6e5670', 4); shape(g, q => q.rect(-10, 634, W + 20, 310), '#4c3c55', 4);
  for (let i = 0; i < 8; i++) { const x = 24 + i * 240; fillR(g, x, 660, 218, 246, 6, '#53425c'); g.fillStyle = '#e0b45c'; g.beginPath(); rrPath(g, x + 90, 684, 40, 9, 4); g.fill(); }
  fillR(g, 360, 520, 104, 86, 26, '#9a8796'); shape(g, q => q.rect(394, 504, 36, 18), '#7d6a7a', 4);
  shape(g, q => q.rect(1640, 556, 70, 50), '#a8644a', 4); for (const [dx, dy, r] of [[-14, -14, 26], [16, -22, 28], [2, -40, 24]]) shape(g, q => q.arc(1675 + dx, 556 + dy, r, 0, 7), '#4d7a52', 4);
  // toaster
  fillR(g, 880, 540, 120, 66, 18, '#b9b0bd'); g.fillStyle = OUT; g.fillRect(905, 538, 30, 8); g.fillRect(945, 538, 30, 8);
  g.fillStyle = lg(g, 944, H, [[0, '#2e2536'], [1, '#211a28']]); g.fillRect(0, 944, W, H - 944); g.strokeStyle = OUT; g.lineWidth = 4; g.beginPath(); g.moveTo(0, 944); g.lineTo(W, 944); g.stroke();
  if (day) { g.save(); g.globalCompositeOperation = 'screen'; g.fillStyle = 'rgba(255,214,170,.16)'; g.fillRect(0, 0, W, H);
    g.globalAlpha = .12; g.fillStyle = '#fff4d6'; for (const [x0, x1] of [[wx + 40, wx + 300], [wx + 400, wx + 700]]) { g.beginPath(); g.moveTo(x0, wy + wh); g.lineTo(x1, wy + wh); g.lineTo(x1 - 520, 944); g.lineTo(x0 - 620, 944); g.closePath(); g.fill(); } g.restore(); }
  vignette(g, .45); return b;
}
function windowCracks(a, win = KWIN) {
  if (a <= 0) return; const { x, y, w, h } = win, cx = x + w * .62, cy = y + h * .55, r = rng(5);
  X.save(); X.globalAlpha = a; X.strokeStyle = '#f5f7ff'; X.lineWidth = 4;
  for (let i = 0; i < 11; i++) { const ang = i / 11 * Math.PI * 2 + r() * .3; let px = cx, py = cy; X.beginPath(); X.moveTo(px, py);
    for (let k = 0; k < 4; k++) { px += Math.cos(ang + (r() - .5) * .6) * (40 + r() * 70); py += Math.sin(ang + (r() - .5) * .6) * (40 + r() * 70); X.lineTo(clamp(px, x, x + w), clamp(py, y, y + h)); } X.stroke(); }
  X.beginPath(); for (let i = 0; i < 12; i++) { const ang = i / 12 * Math.PI * 2, rr = 70 + r() * 50; X.lineTo(cx + Math.cos(ang) * rr, cy + Math.sin(ang) * rr * .9); } X.closePath();
  X.fillStyle = 'rgba(20,14,30,.55)'; X.fill(); X.stroke(); X.restore();
}
function windowTape(u, win = KWIN) {
  if (u <= 0) return; const { x, y, w, h } = win, cx = x + w * .62, cy = y + h * .55;
  const strips = [[-150, -90, 150, 90], [-150, 90, 150, -90], [-170, 0, 170, 0]];
  strips.forEach(([x0, y0, x1, y1], i) => { const v = clamp(u * 3 - i); if (v <= 0) return;
    X.save(); X.strokeStyle = OUT; X.lineWidth = 46; X.lineCap = 'butt'; X.beginPath(); X.moveTo(cx + x0, cy + y0); X.lineTo(cx + mix(x0, x1, v), cy + mix(y0, y1, v)); X.stroke();
    X.strokeStyle = '#c9c4b8'; X.lineWidth = 38; X.stroke(); X.restore(); });
}
function shards(t, t0, src, n = 18, seed = 3) {
  const u = t - t0; if (u < 0 || u > 1.2) return; const r = rng(seed);
  for (let i = 0; i < n; i++) {
    const ang = Math.PI * (.75 + r() * .7), sp = 500 + r() * 700, x = src[0] + Math.cos(ang) * sp * u, y = src[1] + Math.sin(ang) * sp * u + 900 * u * u * .5, s = 10 + r() * 22;
    X.save(); X.globalAlpha = clamp(1.2 - u); X.translate(x, y); X.rotate(r() * 6 + u * (r() * 12 - 6));
    shape(X, g => { g.moveTo(0, -s); g.lineTo(s * .7, s * .6); g.lineTo(-s * .6, s * .4); g.closePath(); }, 'rgba(200,235,255,.85)', 3); X.restore();
  }
}

/* bedroom: bed with the headboard on the left, window with blinds */
function bgBedroom(night = false) {
  const [b, g] = mk();
  g.fillStyle = lg(g, 0, H, [[0, '#4b5a86'], [1, '#3f4b70']]); g.fillRect(0, 0, W, H);
  // window with blinds
  const wx = 620, wy = 150, ww = 560, wh = 340;
  g.fillStyle = lg(g, wy, wy + wh, night ? [[0, '#1d2340'], [1, '#2b3460']] : [[0, '#ffe2a8'], [1, '#ffd08a']]); g.fillRect(wx, wy, ww, wh);
  for (let y = wy + 8; y < wy + wh; y += 30) { g.fillStyle = night ? '#3c4670' : '#f3e6cf'; g.fillRect(wx, y, ww, 18); g.strokeStyle = 'rgba(0,0,0,.25)'; g.lineWidth = 2; g.strokeRect(wx, y, ww, 18); }
  g.strokeStyle = OUT; g.lineWidth = 14; g.strokeRect(wx, wy, ww, wh);
  if (!night) { g.globalAlpha = .18; g.fillStyle = '#fff1c8'; g.beginPath(); g.moveTo(wx, wy + wh); g.lineTo(wx + ww, wy + wh); g.lineTo(wx + ww + 300, 944); g.lineTo(wx - 200, 944); g.fill(); g.globalAlpha = 1; }
  // posters
  fillR(g, 1360, 170, 200, 270, 6, '#d9534f'); g.fillStyle = '#fde047'; g.beginPath(); g.arc(1460, 280, 60, 0, 7); g.fill(); fillR(g, 1600, 210, 170, 220, 6, '#2f7d5b');
  fillR(g, 160, 200, 180, 230, 6, '#6b5fa8');
  // nightstand + lamp
  fillR(g, 180, 700, 170, 244, 8, '#7a5a48'); g.fillStyle = '#e0b45c'; g.fillRect(250, 760, 30, 8);
  shape(g, q => q.rect(255, 610, 20, 90), '#9a8796', 4); shape(g, q => { q.moveTo(210, 610); q.lineTo(320, 610); q.lineTo(295, 540); q.lineTo(235, 540); q.closePath(); }, night ? '#6a5f7a' : '#f3d7a0', 4);
  // bed: headboard, mattress, pillow
  fillR(g, 400, 560, 60, 384, 12, '#7a5a48'); fillR(g, 1260, 700, 40, 244, 10, '#7a5a48');
  fillR(g, 440, 720, 840, 70, 16, '#e9e4ee'); shape(g, q => q.rect(450, 790, 820, 70), '#7a5a48', 4);
  // floor + rug
  g.fillStyle = lg(g, 944, H, [[0, '#5a4636'], [1, '#43352a']]); g.fillRect(0, 944, W, H - 944); g.strokeStyle = OUT; g.lineWidth = 4; g.beginPath(); g.moveTo(0, 944); g.lineTo(W, 944); g.stroke();
  shape(g, q => q.ellipse(960, 1010, 520, 50, 0, 0, 7), '#8a4f5a', 4);
  vignette(g, .45); return b;
}
function bedFront(t, night, sleeper) {   // pillow + blanket drawn over the sleeping hero
  fillR(X, 452, 655, 170, 80, 36, '#ffffff');
  if (sleeper) sleeper();
  shape(X, q => { q.moveTo(600, 760); q.quadraticCurveTo(610, 650, 700, 648); q.quadraticCurveTo(820, 640, 900, 670); q.quadraticCurveTo(1100, 680, 1270, 700); q.lineTo(1270, 800); q.quadraticCurveTo(930, 820, 600, 800); q.closePath(); }, '#3f5aa0');
  X.save(); X.beginPath(); X.moveTo(600, 760); X.quadraticCurveTo(610, 650, 700, 648); X.quadraticCurveTo(820, 640, 900, 670); X.quadraticCurveTo(1100, 680, 1270, 700); X.lineTo(1270, 800); X.quadraticCurveTo(930, 820, 600, 800); X.closePath(); X.clip();
  X.strokeStyle = 'rgba(255,255,255,.12)'; X.lineWidth = 16; for (let x = 640; x < 1300; x += 70) { X.beginPath(); X.moveTo(x, 640); X.lineTo(x - 60, 820); X.stroke(); } X.restore();
}

/* street with a bus stop; the road runs BEHIND the characters */
function bgStreet() {
  const [b, g] = mk();
  g.fillStyle = lg(g, 0, 700, [[0, '#8fc3e8'], [1, '#e8eef0']]); g.fillRect(0, 0, W, 700);
  skyline(g, 0, W, 560, 21, [['#b7c3da', 120, 260, 20]], .0);
  const r = rng(9);
  for (let x = -40; x < W;) { const bw = 220 + r() * 160, bh = 300 + r() * 160, col = ['#b86b4b', '#c98d5a', '#8f6aa8', '#6a8fb0'][Math.floor(r() * 4)];
    fillR(g, x, 640 - bh, bw, bh + 40, 4, col);
    for (let yy = 640 - bh + 30; yy < 600; yy += 70) for (let xx = x + 26; xx < x + bw - 50; xx += 64) fillR(g, xx, yy, 34, 44, 3, '#f2e3c4', 3);
    x += bw + 10; }
  // road (behind), curb, sidewalk (front)
  g.fillStyle = '#4b4752'; g.fillRect(0, 640, W, 190); g.fillStyle = '#efe9d8'; for (let x = 20; x < W; x += 160) g.fillRect(x, 732, 90, 10);
  shape(g, q => q.rect(-10, 828, W + 20, 22), '#bdb6aa', 4); g.fillStyle = lg(g, 850, H, [[0, '#d8d1c3'], [1, '#c4bcae']]); g.fillRect(0, 850, W, H - 850);
  g.strokeStyle = 'rgba(0,0,0,.12)'; g.lineWidth = 3; for (let x = 0; x < W; x += 180) { g.beginPath(); g.moveTo(x, 850); g.lineTo(x - 60, H); g.stroke(); }
  // trees + lamp post
  for (const tx of [160, 1780]) { shape(g, q => q.rect(tx - 12, 620, 24, 230), '#7a5a48', 4); for (const [dx, dy, rr] of [[-50, 0, 70], [40, -20, 80], [0, -80, 70]]) shape(g, q => q.arc(tx + dx, 600 + dy, rr, 0, 7), '#5c9a5e', 4); }
  shape(g, q => q.rect(560, 380, 18, 470), '#4e4a58', 4); fillR(g, 540, 360, 90, 34, 14, '#4e4a58'); shape(g, q => q.ellipse(612, 398, 22, 10, 0, 0, 7), '#fff3c4', 3);
  vignette(g, .3); return b;
}
function busStopFront(g = X) {   // shelter drawn over the background, behind characters
  fillR(g, 1180, 470, 560, 26, 8, '#3c4a5c'); shape(g, q => q.rect(1196, 496, 14, 354), '#3c4a5c', 4); shape(g, q => q.rect(1710, 496, 14, 354), '#3c4a5c', 4);
  g.save(); g.globalAlpha = .28; g.fillStyle = '#bfe3ff'; g.fillRect(1210, 500, 500, 300); g.restore(); g.strokeStyle = OUT; g.lineWidth = 4; g.strokeRect(1210, 500, 500, 300);
  fillR(g, 1260, 760, 400, 22, 8, '#7a5a48'); shape(g, q => q.rect(1290, 782, 14, 60), '#4e4a58', 4); shape(g, q => q.rect(1616, 782, 14, 60), '#4e4a58', 4);
  shape(g, q => q.rect(1100, 470, 12, 380), '#4e4a58', 4); shape(g, q => q.arc(1106, 450, 44, 0, 7), '#2f6fb5'); text('BUS', 1106, 466, 42, '#fff', 'center');
}
function bus(x, doorOpen) {
  const y = 470, w = 900, h = 330;
  fillR(X, x, y, w, h, 34, '#e8b23a'); shape(X, g => g.rect(x, y + 200, w, 40), '#c4302b', 4);
  for (let i = 0; i < 6; i++) fillR(X, x + 40 + i * 130, y + 40, 100, 120, 12, '#bfe3ff');
  const dx = x + w - 170; fillR(X, dx, y + 40, 120, 270, 10, doorOpen ? '#2a2333' : '#bfe3ff'); if (!doorOpen) { X.strokeStyle = OUT; X.lineWidth = 4; X.beginPath(); X.moveTo(dx + 60, y + 40); X.lineTo(dx + 60, y + 310); X.stroke(); }
  for (const wx of [x + 150, x + w - 260]) { shape(X, g => g.arc(wx, y + h, 56, 0, 7), '#2a2333'); shape(X, g => g.arc(wx, y + h, 22, 0, 7), '#9a95a6', 4); }
  fillR(X, x + w - 30, y + 230, 30, 40, 10, '#fff3c4');
}

/* living room for the party (evening) */
const LWIN = { x: 1330, y: 170, w: 470, h: 360 };
function bgLiving() {
  const [b, g] = mk(); const { x: wx, y: wy, w: ww, h: wh } = LWIN;
  g.fillStyle = lg(g, 0, H, [[0, '#5b3f5e'], [1, '#4a3350']]); g.fillRect(0, 0, W, H);
  g.strokeStyle = 'rgba(255,255,255,.04)'; g.lineWidth = 30; for (let x = 0; x < W; x += 90) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x, 944); g.stroke(); }
  g.save(); g.beginPath(); g.rect(wx, wy, ww, wh); g.clip(); g.fillStyle = lg(g, wy, wy + wh, [[0, '#141a3a'], [1, '#2c2a5a']]); g.fillRect(wx, wy, ww, wh);
  skyline(g, wx, wx + ww, wy + wh, 31, [['#2a2850', 80, 200, 20], ['#1f1d40', 120, 260, 6]], .35); g.fillStyle = '#f4f1e0'; g.beginPath(); g.arc(wx + 380, wy + 70, 30, 0, 7); g.fill(); g.restore();
  g.strokeStyle = OUT; g.lineWidth = 14; g.strokeRect(wx, wy, ww, wh); g.lineWidth = 9; g.beginPath(); g.moveTo(wx + ww / 2, wy); g.lineTo(wx + ww / 2, wy + wh); g.stroke();
  // floor lamp with warm light
  shape(g, q => q.rect(1210, 420, 12, 524), '#4e4a58', 4); shape(g, q => { q.moveTo(1160, 420); q.lineTo(1272, 420); q.lineTo(1250, 340); q.lineTo(1182, 340); q.closePath(); }, '#f3d7a0', 4);
  const gr = g.createRadialGradient(1216, 400, 10, 1216, 400, 700); gr.addColorStop(0, 'rgba(255,200,130,.25)'); gr.addColorStop(1, 'rgba(255,200,130,0)'); g.fillStyle = gr; g.fillRect(0, 0, W, H);
  // sofa on the left
  fillR(g, 60, 640, 520, 170, 40, '#3f6f8f'); fillR(g, 40, 720, 90, 200, 30, '#35607d'); fillR(g, 510, 720, 90, 200, 30, '#35607d'); fillR(g, 110, 760, 420, 120, 24, '#4a7ea0');
  // table with cloth (the cake is drawn per frame)
  shape(g, q => { q.moveTo(760, 760); q.lineTo(1160, 760); q.lineTo(1190, 944); q.lineTo(730, 944); q.closePath(); }, '#e8e1ec', 4);
  g.strokeStyle = 'rgba(0,0,0,.08)'; g.lineWidth = 8; for (let x = 780; x < 1180; x += 50) { g.beginPath(); g.moveTo(x, 770); g.lineTo(x - 10, 940); g.stroke(); }
  // garland with letters
  const word = 'HAPPY BIRTHDAY DAVE'; const x0 = 140, x1 = 1220, n = word.length;
  g.strokeStyle = OUT; g.lineWidth = 4; g.beginPath(); for (let i = 0; i <= 40; i++) { const u = i / 40, x = mix(x0, x1, u), y = 120 + Math.sin(u * Math.PI) * 60; i ? g.lineTo(x, y) : g.moveTo(x, y); } g.stroke();
  const cols = ['#e8382f', '#fde047', '#3fb6e8', '#7bd36b', '#e86fb4'];
  for (let i = 0; i < n; i++) { if (word[i] === ' ') continue; const u = (i + .5) / n, x = mix(x0, x1, u), y = 120 + Math.sin(u * Math.PI) * 60;
    shape(g, q => { q.moveTo(x - 26, y); q.lineTo(x + 26, y); q.lineTo(x, y + 66); q.closePath(); }, cols[i % 5], 4);
    g.font = '34px Bangers'; g.textAlign = 'center'; g.fillStyle = OUT; g.fillText(word[i], x, y + 36); g.textAlign = 'left'; }
  g.fillStyle = lg(g, 944, H, [[0, '#3b2a3e'], [1, '#2c1f30']]); g.fillRect(0, 944, W, H - 944); g.strokeStyle = OUT; g.lineWidth = 4; g.beginPath(); g.moveTo(0, 944); g.lineTo(W, 944); g.stroke();
  vignette(g, .45); return b;
}
function cake(t, x, y, lit = 1) {
  fillR(X, x - 110, y - 70, 220, 70, 14, '#f3e3ef'); fillR(X, x - 80, y - 130, 160, 60, 14, '#f7c6dc');
  X.strokeStyle = '#e86fb4'; X.lineWidth = 6; X.beginPath(); for (let i = 0; i <= 10; i++) { const xx = x - 110 + i * 22; X.lineTo(xx, y - 70 + (i % 2 ? 10 : 0)); } X.stroke();
  for (let i = 0; i < 5; i++) { const cx = x - 56 + i * 28; shape(X, g => g.rect(cx - 5, y - 168, 10, 38), ['#3fb6e8', '#fde047', '#7bd36b', '#e86fb4', '#e8382f'][i], 3);
    if (lit < 0) continue;
    if (lit > 0) { const f = 1 + Math.sin(t * 18 + i * 2) * .15; X.save(); X.globalAlpha = lit; shape(X, g => { g.moveTo(cx, y - 196 * f + 168 * (f - 1)); g.quadraticCurveTo(cx + 10, y - 176, cx, y - 168); g.quadraticCurveTo(cx - 10, y - 176, cx, y - 196 * f + 168 * (f - 1)); }, '#ffb53a', 3); X.restore(); glow(cx, y - 180, 40, .5 * lit, '255,190,90'); }
    else { X.save(); X.globalAlpha = .5; X.strokeStyle = '#ddd'; X.lineWidth = 4; X.beginPath(); X.moveTo(cx, y - 172); X.quadraticCurveTo(cx + 12 * Math.sin(t * 3 + i), y - 200, cx + 4, y - 228); X.stroke(); X.restore(); }
  }
}
function balloons(t, x, y) {
  const set = [[-60, 0, '#e8382f'], [10, -40, '#3fb6e8'], [70, 10, '#fde047'], [-20, 60, '#7bd36b']];
  for (const [dx, dy, c] of set) { const bx = x + dx + Math.sin(t * 1.3 + dx) * 8, by = y + dy + Math.sin(t * 1.7 + dy) * 6;
    X.strokeStyle = OUT; X.lineWidth = 3; X.beginPath(); X.moveTo(bx, by + 52); X.quadraticCurveTo(bx + 10, by + 140, x, y + 260); X.stroke();
    shape(X, g => g.ellipse(bx, by, 42, 52, 0, 0, 7), c); X.fillStyle = 'rgba(255,255,255,.45)'; X.beginPath(); X.ellipse(bx + 14, by - 18, 9, 14, -.5, 0, 7); X.fill(); }
}

/* ---------- bakery (day): shop window on the left (the suit waits outside), counter with a display case on the right ---------- */
const BWIN = { x: 90, y: 150, w: 640, h: 480 };
function bgBakery() {
  const [b, g] = mk(); const { x: wx, y: wy, w: ww, h: wh } = BWIN;
  g.fillStyle = lg(g, 0, H, [[0, '#caa391'], [.7, '#d8b39d'], [1, '#c39a86']]); g.fillRect(0, 0, W, H);
  g.strokeStyle = 'rgba(255,255,255,.07)'; g.lineWidth = 40; for (let x = 0; x < W; x += 110) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x, 944); g.stroke(); }
  // outside, seen through the window: sky, a facade across the street, the sidewalk
  g.save(); g.beginPath(); g.rect(wx, wy, ww, wh); g.clip();
  g.fillStyle = lg(g, wy, wy + wh, [[0, '#9cc8e8'], [1, '#e9eef0']]); g.fillRect(wx, wy, ww, wh);
  fillR(g, wx - 20, wy + 60, 360, 400, 4, '#b8826a'); fillR(g, wx + 360, wy + 20, 320, 440, 4, '#8f7aa8');
  for (let yy = wy + 100; yy < wy + 380; yy += 80) for (const xx of [wx + 30, wx + 130, wx + 230, wx + 400, wx + 500]) fillR(g, xx, yy, 50, 56, 3, '#f2e3c4', 3);
  g.fillStyle = '#4b4752'; g.fillRect(wx, wy + 440, ww, 30); g.fillStyle = '#d8d1c3'; g.fillRect(wx, wy + 470, ww, 20); g.restore();
  // wall shelves with bread, menu board
  for (const sy of [340, 500]) { shape(g, q => q.rect(840, sy, 560, 18), '#8a5a3c', 4);
    for (let i = 0; i < 6; i++) { const x = 880 + i * 88; shape(g, q => q.ellipse(x, sy - 26, 38, 26, 0, Math.PI, 0), ['#d9a35a', '#c98a45', '#e3b46a'][i % 3], 4); g.strokeStyle = 'rgba(90,50,20,.5)'; g.lineWidth = 3; for (const d of [-12, 4, 20]) { g.beginPath(); g.moveTo(x + d - 6, sy - 40); g.lineTo(x + d + 4, sy - 22); g.stroke(); } } }
  fillR(g, 1640, 110, 260, 210, 10, '#2f3a35'); g.strokeStyle = '#8a5a3c'; g.lineWidth = 12; g.strokeRect(1640, 110, 260, 210);
  g.font = '56px Bangers'; g.textAlign = 'center'; g.fillStyle = '#f4f1e0'; g.fillText('CAKES', 1770, 175); g.font = '34px Bangers'; g.fillStyle = '#fde047'; g.fillText('BIRTHDAY $20', 1770, 228); g.fillStyle = '#f7c6dc'; g.fillText('WINDOWS ???', 1770, 280); g.textAlign = 'left';
  // floor tiles
  g.fillStyle = '#e9e1d4'; g.fillRect(0, 944, W, H - 944);
  for (let y = 944, row = 0; y < H; y += 46, row++) for (let x = (row % 2) * 46 - 46; x < W; x += 92) { g.fillStyle = '#b9a99a'; g.fillRect(x, y, 46, 46); }
  g.strokeStyle = OUT; g.lineWidth = 4; g.beginPath(); g.moveTo(0, 944); g.lineTo(W, 944); g.stroke();
  // sunlight from the window falling on the floor
  g.save(); g.globalAlpha = .16; g.fillStyle = '#fff1c8'; g.beginPath(); g.moveTo(wx, wy + wh); g.lineTo(wx + ww, wy + wh); g.lineTo(wx + ww + 420, 1080); g.lineTo(wx + 160, 1080); g.fill(); g.restore();
  vignette(g, .35); return b;
}
function bakeryWindow(broken) {      // frame + glass drawn over whatever stands outside
  const { x, y, w, h } = BWIN;
  if (!broken) { X.save(); X.globalAlpha = .18; X.fillStyle = '#e8f6ff'; X.beginPath(); X.moveTo(x + 60, y); X.lineTo(x + 200, y); X.lineTo(x + 60, y + 200); X.closePath(); X.fill(); X.beginPath(); X.moveTo(x + 260, y); X.lineTo(x + 300, y); X.lineTo(x + 80, y + 300); X.lineTo(x + 60, y + 280); X.closePath(); X.fill(); X.restore(); }
  X.strokeStyle = OUT; X.lineWidth = 16; X.strokeRect(x, y, w, h); X.lineWidth = 10; X.beginPath(); X.moveTo(x, y + 90); X.lineTo(x + w, y + 90); X.stroke();
  X.save(); X.strokeStyle = '#d9534f'; X.lineWidth = 34; X.beginPath(); X.moveTo(x, y + 45); X.lineTo(x + w, y + 45); X.stroke(); X.restore();
  text('B A K E R Y', x + w / 2, y + 62, 46, '#fde047', 'center', 'Bangers', 6);
  shape(X, g => rrPath(g, x + w - 170, y + 120, 120, 54, 8), '#f4f1e0', 4); text('OPEN', x + w - 110, y + 160, 38, '#2f7d5b', 'center');
}
function bakeryCounter() {           // counter with glass display case, drawn in front of the baker
  shape(X, g => g.rect(1150, 590, 800, 26), '#8a5a3c', 4); shape(X, g => g.rect(1150, 616, 800, 340), '#a8735a', 4);
  X.save(); X.globalAlpha = .9; fillR(X, 1190, 640, 700, 170, 10, '#f3ece6'); X.restore();
  for (let i = 0; i < 4; i++) { const cx = 1290 + i * 165; fillR(X, cx - 60, 740, 120, 60, 12, ['#f7c6dc', '#f3e3ef', '#e9c47a', '#c98a5a'][i]); fillR(X, cx - 40, 700, 80, 42, 12, ['#f3e3ef', '#f7c6dc', '#f3e3ef', '#e9c47a'][i]); shape(X, g => g.arc(cx, 694, 9, 0, 7), '#e8382f', 3); }
  X.save(); X.globalAlpha = .22; X.fillStyle = '#ffffff'; X.beginPath(); X.moveTo(1240, 640); X.lineTo(1320, 640); X.lineTo(1250, 810); X.lineTo(1190, 810); X.closePath(); X.fill(); X.restore();
  X.strokeStyle = OUT; X.lineWidth = 6; X.strokeRect(1190, 640, 700, 170);
  fillR(X, 1740, 520, 140, 72, 10, '#5c6a7a'); fillR(X, 1760, 500, 100, 28, 6, '#2a2333'); text('$20', 1810, 522, 26, '#7bd36b', 'center', 'Bangers', 0);
}
/* cake box held by the hero: sq = squash 0..1 (flattened by the chest plate) */
function cakeBox(x, y, rot = 0, sq = 0) {
  X.save(); X.translate(x, y); X.rotate(rot); X.scale(1 + sq * .5, 1 - sq * .62);
  fillR(X, -75, -55, 150, 110, 10, '#f7f1ea'); shape(X, g => g.rect(-75, -55, 150, 22), '#f7c6dc', 4);
  X.strokeStyle = '#e86fb4'; X.lineWidth = 5; X.beginPath(); X.moveTo(0, -55); X.lineTo(0, 55); X.stroke(); text('DAVE', 0, 20, 34, '#c24f93', 'center');
  X.restore();
  if (sq > .6) { X.save(); X.globalAlpha = clamp((sq - .6) * 3); for (const [dx, dy, r] of [[-110, -10, 14], [104, 4, 12], [-80, 30, 9], [92, -22, 8]]) shape(X, g => g.arc(x + dx, y + dy, r, 0, 7), '#f7c6dc', 3); X.restore(); }
}
/* present on the kitchen counter: v = 0 cardboard + crumpled paper (wobbling), 1 = neatly wrapped */
function present(t, x, y, v, mess = 1) {
  X.save(); X.translate(x, y); X.scale(1.3, 1.3); X.translate(-x, -y);
  if (v < 1) {
    fillR(X, x - 80, y - 110, 160, 110, 6, '#c9935e');
    const r = rng(4), n = 9; X.save(); X.globalAlpha = mess * (1 - v);
    shape(X, g => { for (let i = 0; i < n; i++) { const a = i / n * Math.PI * 2, rr = 70 + r() * 40 + Math.sin(t * 9 + i) * 8; const px = x - 20 + Math.cos(a) * rr * 1.1, py = y - 70 + Math.sin(a) * rr * .55; i ? g.lineTo(px, py) : g.moveTo(px, py); } g.closePath(); }, '#8a6fd1', 4);
    X.fillStyle = '#fde047'; for (let i = 0; i < 6; i++) { const a = i * 1.1, px = x - 20 + Math.cos(a) * 50, py = y - 70 + Math.sin(a) * 26; X.beginPath(); X.arc(px, py, 5, 0, 7); X.fill(); }
    X.restore();
  }
  if (v > 0) {
    X.save(); X.globalAlpha = clamp(v * 1.5); const s = .8 + .2 * back(v);
    X.translate(x, y); X.scale(s, s); fillR(X, -80, -110, 160, 110, 6, '#8a6fd1');
    X.fillStyle = '#fde047'; for (let i = 0; i < 8; i++) { X.beginPath(); X.arc(-60 + (i % 4) * 40, -85 + Math.floor(i / 4) * 50, 5, 0, 7); X.fill(); }
    shape(X, g => g.rect(-12, -110, 24, 110), '#fde047', 3); shape(X, g => g.rect(-80, -66, 160, 20), '#fde047', 3);
    for (const sd of [-1, 1]) shape(X, g => g.ellipse(sd * 26, -118, 28, 15, sd * .5, 0, 7), '#fde047', 4); shape(X, g => g.arc(0, -118, 10, 0, 7), '#e8b23a', 3);
    X.restore();
  }
  X.restore();
}
function phone(x, y, on, rot = 0) {
  X.save(); X.translate(x, y); X.rotate(rot); fillR(X, -22, -40, 44, 80, 8, '#2a2333');
  X.fillStyle = on ? '#9fe4ff' : '#3a4a5c'; X.fillRect(-16, -32, 32, 60); if (on) { X.fillStyle = '#2a2333'; X.beginPath(); X.moveTo(-6, -12); X.lineTo(8, -2); X.lineTo(-6, 8); X.fill(); } X.restore();
}
function sparkle(x, y, s, a = 1) {
  if (a <= 0) return; X.save(); X.globalAlpha = a; X.translate(x, y); X.scale(s, s); X.fillStyle = '#fffbe6';
  X.beginPath(); for (let i = 0; i < 8; i++) { const r = i % 2 ? 6 : 26, ang = i * Math.PI / 4; X.lineTo(Math.cos(ang) * r, Math.sin(ang) * r); } X.closePath(); X.fill(); X.restore(); glow(x, y, 40 * s, .5 * a, '255,250,220');
}
function puff(x, y, a, word = 'pff') {
  if (a <= 0) return; X.save(); X.globalAlpha = clamp(a); const k = .6 + .5 * a;
  for (const [dx, dy, r] of [[0, 0, 30], [28, -12, 24], [-26, -10, 22], [8, -30, 20]]) shape(X, g => g.arc(x + dx * k, y + dy * k - (1 - a) * 30, r * k, 0, 7), '#ece8ee', 4);
  text(word, x + 70, y - 30 - (1 - a) * 30, 64, '#f4f1e0', 'left', 'Bangers', 10); X.restore();
}
function cakeTape(x, y, u = 1) {    // tape holding Dave's cake together
  const strips = [[-120, -40, 120, -120], [-120, -120, 120, -30], [-40, -128, 30, 0]];
  strips.forEach(([x0, y0, x1, y1], i) => { const v = clamp(u * 3 - i); if (v <= 0) return;
    X.save(); X.lineCap = 'butt'; X.strokeStyle = OUT; X.lineWidth = 30; X.beginPath(); X.moveTo(x + x0, y + y0); X.lineTo(x + mix(x0, x1, v), y + mix(y0, y1, v)); X.stroke();
    X.strokeStyle = '#c9c4b8'; X.lineWidth = 24; X.stroke(); X.restore(); });
}
