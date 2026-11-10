/* Shared drawing library for code-drawn episodes (style: flat shapes, thin dark outline, warm rim light, letterbox). */
const W = 1920, H = 1080, OUT = '#1b1320', LW = 5, RIM = 'rgba(255,226,168,.95)', BAR = 72;
let X = null;
const setCtx = c => { X = c; };
const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
const io = t => { t = clamp(t); return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
const outq = t => { t = clamp(t); return 1 - Math.pow(1 - t, 3); };
const back = t => { t = clamp(t); const c1 = 1.15, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); };
const R = (t, a, b, f = io) => f(clamp((t - a) / (b - a)));
const mix = (a, b, u) => a + (b - a) * u;
const mix2 = (p, q, u) => [mix(p[0], q[0], u), mix(p[1], q[1], u)];
const bump = (t, a, b) => Math.max(0, Math.sin(clamp((t - a) / (b - a)) * Math.PI));
const blinkAmt = (t, list) => Math.max(0, ...list.map(b => bump(t, b, b + .16)));
const rng = seed => () => (seed = (seed * 16807) % 2147483647) / 2147483647;

/* ---------- primitives ---------- */
function rrPath(g, x, y, w, h, r) { g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); }
function shape(g, path, fill, lw = LW) { g.beginPath(); path(g); if (fill) { g.fillStyle = fill; g.fill(); } if (lw) { g.lineWidth = lw; g.strokeStyle = OUT; g.lineJoin = 'round'; g.stroke(); } }
function tube(pts, col, w) {
  X.lineCap = 'round'; X.lineJoin = 'round'; X.beginPath(); pts.forEach((p, i) => i ? X.lineTo(p[0], p[1]) : X.moveTo(p[0], p[1]));
  X.strokeStyle = OUT; X.lineWidth = w + 2 * LW; X.stroke(); X.strokeStyle = col; X.lineWidth = w; X.stroke();
}
function ik(sx, sy, tx, ty, L1, L2, out) {
  let dx = tx - sx, dy = ty - sy, d = Math.hypot(dx, dy); const m = L1 + L2 - 1; if (d > m) { tx = sx + dx / d * m; ty = sy + dy / d * m; d = m; }
  if (d < 1) d = 1;
  const b = Math.atan2(ty - sy, tx - sx), o = Math.acos(clamp((L1 * L1 + d * d - L2 * L2) / (2 * L1 * d), -1, 1));
  const e1 = [sx + L1 * Math.cos(b + o), sy + L1 * Math.sin(b + o)], e2 = [sx + L1 * Math.cos(b - o), sy + L1 * Math.sin(b - o)];
  return [(out > 0) === (e1[0] > e2[0]) ? e1 : e2, [tx, ty]];
}
function rimClip(path, fromX, col = RIM, w = 10) {
  X.save(); X.beginPath(); path(X); X.clip();
  const gr = X.createLinearGradient(fromX - 30, 0, fromX + 60, 0); gr.addColorStop(0, 'rgba(255,226,168,0)'); gr.addColorStop(1, col);
  X.beginPath(); path(X); X.strokeStyle = gr; X.shadowColor = 'rgba(255,214,150,.9)'; X.shadowBlur = 16; X.lineWidth = w * 1.3; X.stroke();
  X.globalCompositeOperation = 'lighter'; X.lineWidth = w * 3.2; X.globalAlpha = .12; X.stroke(); X.restore();
}
function shadeClip(path, toX, col) {
  X.save(); X.beginPath(); path(X); X.clip(); const gr = X.createLinearGradient(toX - 110, 0, toX + 70, 0);
  gr.addColorStop(0, col); gr.addColorStop(1, col.replace(/[\d.]+\)$/, '0)')); X.fillStyle = gr; X.fillRect(-5000, -5000, 10000, 10000); X.restore();
}
function mitten(x, y, r, col = '#f1ece6') { shape(X, g => g.arc(x, y, r, 0, 7), col); X.save(); X.beginPath(); X.arc(x, y, r - 5, -1.2, 0.2); X.strokeStyle = RIM; X.shadowColor = 'rgba(255,214,150,.9)'; X.shadowBlur = 10; X.lineWidth = 4; X.stroke(); X.restore(); }
function glow(x, y, r, a, rgb = '150,225,255') {
  if (a <= 0) return; X.save(); X.globalCompositeOperation = 'lighter';
  const g = X.createRadialGradient(x, y, 1, x, y, r); g.addColorStop(0, `rgba(${rgb},${a})`); g.addColorStop(1, `rgba(${rgb},0)`);
  X.fillStyle = g; X.beginPath(); X.arc(x, y, r, 0, 7); X.fill(); X.restore();
}
function text(s, x, y, size, fill = '#141014', align = 'left', font = 'Bangers', stroke = 0) {
  X.font = `${size}px ${font}`; X.textAlign = align; X.textBaseline = 'alphabetic';
  if (stroke) { X.lineWidth = stroke; X.strokeStyle = OUT; X.lineJoin = 'round'; X.strokeText(s, x, y); }
  X.fillStyle = fill; X.fillText(s, x, y); X.textAlign = 'left';
}

/* ---------- comic FX ---------- */
function burst(word, x, y, s, a, rot = -0.12, col = '#ffd23f') {
  if (a <= 0) return; const k = s * (0.7 + 0.3 * back(clamp(a * 1.6)));
  X.save(); X.globalAlpha = clamp(a * 3); X.translate(x, y); X.rotate(rot); X.scale(k, k);
  const n = 14; X.beginPath();
  for (let i = 0; i < n * 2; i++) { const ang = i / (n * 2) * Math.PI * 2, rr = i % 2 ? 78 : 128 + (i % 4 ? 0 : 18); X.lineTo(Math.cos(ang) * rr * 1.45, Math.sin(ang) * rr); }
  X.closePath(); X.fillStyle = col; X.fill(); X.lineWidth = 7; X.strokeStyle = OUT; X.stroke();
  text(word, 0, 26, 84, '#e8382f', 'center', 'Bangers', 12); X.restore();
}
function caption(s, a, y = 104) {
  if (a <= 0) return; X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.globalAlpha = clamp(a); X.font = '70px Bangers'; const w = X.measureText(s).width, k = .9 + .1 * back(a);
  X.translate(70, y); X.scale(k, k); X.fillStyle = '#fde047'; X.strokeStyle = '#141014'; X.lineWidth = 8; X.beginPath(); rrPath(X, 0, 0, w + 56, 100, 8); X.fill(); X.stroke();
  X.fillStyle = '#141014'; X.fillText(s, 28, 77); X.restore();
}
function sweatDrops(x, y, r, t, a) {
  if (a <= 0) return;
  for (const [dx, ph] of [[-.95, 0], [.98, .5]]) {
    const u = ((t * 1.3 + ph) % 1), yy = y - r * .3 + u * r * .7;
    X.save(); X.globalAlpha = a * (1 - u * .6);
    shape(X, g => { g.moveTo(x + dx * r, yy - 18); g.quadraticCurveTo(x + dx * r + 11, yy + 4, x + dx * r, yy + 8); g.quadraticCurveTo(x + dx * r - 11, yy + 4, x + dx * r, yy - 18); }, '#9fd8ff', 4);
    X.restore();
  }
}
function musicNotes(x, y, t, a, n = 3) {
  if (a <= 0) return; X.save(); X.globalAlpha = a;
  for (let i = 0; i < n; i++) { const u = (t * .7 + i / n) % 1; text(i % 2 ? '♪' : '♫', x + Math.sin(u * 6 + i) * 30 + i * 40, y - u * 160, 64, '#fde047', 'center', 'serif', 6); }
  X.restore();
}

/* ---------- heads ---------- */
function head(cx, cy, r, rot, o) {
  X.save(); X.translate(cx, cy); X.rotate(rot);
  const circ = g => g.arc(0, 0, r, 0, 7);
  if (o.helmet) shape(X, g => g.arc(0, 0, r * 1.17, 0, 7), '#c4302b');
  if (o.hair === 'bun') shape(X, g => g.arc(r * .1, -r * 1.02, r * .36, 0, 7), o.hairCol || '#5a3324');
  { const gr = X.createRadialGradient(r * .28, -r * .26, r * .1, r * .05, -r * .05, r * 1.12); gr.addColorStop(0, '#f7f3ef'); gr.addColorStop(.62, '#ebe5ea'); gr.addColorStop(1, '#bfb5c3'); shape(X, circ, gr, 0); }
  X.save(); X.beginPath(); circ(X); X.clip(); X.beginPath(); X.arc(0, 0, r - 4, -1.45, 0.45); X.strokeStyle = RIM; X.shadowColor = 'rgba(255,214,150,.95)'; X.shadowBlur = 18; X.lineWidth = 9; X.stroke();
  X.globalCompositeOperation = 'lighter'; X.globalAlpha = .1; X.lineWidth = 30; X.stroke(); X.restore();
  shape(X, circ, null);
  if (o.hair === 'curly') {
    for (const [a, b, s] of [[-.72, -.52, .3], [-.5, -.78, .31], [-.16, -.92, .31], [.2, -.9, .3], [.52, -.76, .3], [.76, -.5, .28], [-.88, -.2, .24], [.88, -.18, .22], [-.3, -.68, .26], [.06, -.7, .26], [.38, -.62, .25]])
      shape(X, g => g.arc(a * r, b * r, s * r, 0, 7), '#1f1719', 4);
    X.strokeStyle = '#463638'; X.lineWidth = 4; for (const [a, b] of [[-.5, -.8], [.2, -.92], [.62, -.72]]) { X.beginPath(); X.arc(a * r, b * r, r * .13, 3.6, 5.2); X.stroke(); }
  }
  if (o.hair === 'bun' || o.hair === 'bob') {
    shape(X, g => { g.moveTo(-r * .98, r * .2); g.quadraticCurveTo(-r * 1.08, -r * 1.05, 0, -r * 1.02); g.quadraticCurveTo(r * 1.08, -r * 1.05, r * .98, r * .2); g.quadraticCurveTo(r * .78, -r * .55, 0, -r * .58); g.quadraticCurveTo(-r * .78, -r * .55, -r * .98, r * .2); }, o.hairCol || '#5a3324', 4);
  }
  if (o.hair === 'cap') {
    shape(X, g => { g.moveTo(-r * .95, -r * .25); g.quadraticCurveTo(-r * .9, -r * 1.05, 0, -r * 1.02); g.quadraticCurveTo(r * .9, -r * 1.05, r * .95, -r * .25); g.closePath(); }, o.hairCol || '#2f7d5b', 4);
    shape(X, g => rrPath(g, r * .2, -r * .4, r * 1.05, r * .2, r * .08), o.hairCol || '#2f7d5b', 4);
  }
  if (o.hair === 'chef') { for (const [a, b, rr] of [[-.45, -1.25, .36], [0, -1.42, .42], [.45, -1.25, .36], [-.2, -1.6, .3], [.25, -1.58, .3]]) shape(X, g => g.arc(a * r, b * r, rr * r, 0, 7), '#fbf8f2', 4);
    shape(X, g => rrPath(g, -r * .72, -r * 1.12, r * 1.44, r * .34, r * .08), '#fbf8f2', 4); }
  if (o.hair === 'band') shape(X, g => { g.moveTo(-r * .97, -r * .38); g.quadraticCurveTo(0, -r * .62, r * .97, -r * .38); g.lineTo(r * .9, -r * .55); g.quadraticCurveTo(0, -r * .8, -r * .9, -r * .55); g.closePath(); }, o.hairCol || '#e8b64a', 4);
  if (o.helmet) { for (const s of [-1, 1]) shape(X, g => { g.moveTo(s * r * .82, -r * .62); g.quadraticCurveTo(s * r * 1.2, 0, s * r * .8, r * .68); g.lineTo(s * r * .98, r * .28); g.quadraticCurveTo(s * r * 1.05, -r * .2, s * r * .82, -r * .62); }, '#c4302b', 4);
    shape(X, g => { g.moveTo(-r * .7, -r * .78); g.quadraticCurveTo(0, -r * 1.12, r * .7, -r * .78); g.lineTo(r * .6, -r * .66); g.quadraticCurveTo(0, -r * .95, -r * .6, -r * .66); g.closePath(); }, '#e3b44c', 4); }
  if (o.faceplate) {            // empty suit: closed helmet, eye slits
    shape(X, circ, '#c4302b'); X.save(); X.beginPath(); circ(X); X.clip(); X.fillStyle = 'rgba(0,0,0,.18)'; X.beginPath(); X.arc(-r * .3, r * .2, r, 0, 7); X.fill(); X.restore();
    shape(X, g => { g.moveTo(-r * .62, -r * .5); g.quadraticCurveTo(0, -r * .72, r * .62, -r * .5); g.lineTo(r * .56, r * .32); g.quadraticCurveTo(r * .3, r * .78, 0, r * .8); g.quadraticCurveTo(-r * .3, r * .78, -r * .56, r * .32); g.closePath(); }, '#e3b44c', 4);
    for (const sd of [-1, 1]) { shape(X, g => { g.moveTo(sd * r * .12, -r * .08); g.lineTo(sd * r * .46, -r * .14); g.lineTo(sd * r * .42, r * .0); g.lineTo(sd * r * .14, r * .04); g.closePath(); }, `rgba(200,240,255,${.35 + .65 * (o.eyes || 0)})`, 3);
      if (o.eyes) glow(sd * r * .3, -r * .05, r * .5, .6 * o.eyes); }
    X.strokeStyle = OUT; X.lineWidth = 4; X.beginPath(); X.moveTo(-r * .2, r * .5); X.lineTo(r * .2, r * .5); X.stroke(); X.restore(); return;
  }
  if (o.beard) {
    const bp = g => { g.moveTo(-r * .97, r * .02); g.quadraticCurveTo(-r * .98, r * .95, 0, r * 1.1); g.quadraticCurveTo(r * .98, r * .95, r * .97, r * .02);
      g.quadraticCurveTo(r * .8, r * .3, r * .5, r * .3); g.quadraticCurveTo(r * .22, r * .26, 0, r * .36); g.quadraticCurveTo(-r * .22, r * .26, -r * .5, r * .3); g.quadraticCurveTo(-r * .8, r * .3, -r * .97, r * .02); };
    { const gr = X.createLinearGradient(-r, 0, r, 0); gr.addColorStop(0, '#231915'); gr.addColorStop(.65, '#3a2a24'); gr.addColorStop(1, '#4d3a31'); shape(X, bp, gr); }
    X.save(); X.beginPath(); bp(X); X.clip(); X.beginPath(); X.arc(0, 0, r - 4, -1.0, 0.5); X.strokeStyle = 'rgba(255,214,150,.55)'; X.lineWidth = 8; X.stroke(); X.restore();
    // moustache
    shape(X, g => { g.moveTo(0, r * .36); g.quadraticCurveTo(-r * .2, r * .3, -r * .36, r * .44); g.quadraticCurveTo(-r * .18, r * .5, 0, r * .44); g.quadraticCurveTo(r * .18, r * .5, r * .36, r * .44); g.quadraticCurveTo(r * .2, r * .3, 0, r * .36); }, '#2a1e1a', 3);
    X.strokeStyle = 'rgba(120,90,75,.55)'; X.lineWidth = 3; X.lineCap = 'round'; for (const [a, b, c] of [[-.55, .62, .2], [.5, .66, .2], [-.25, .85, .15], [.3, .88, .15]]) { X.beginPath(); X.arc(a * r, b * r, c * r, -2.4, -1.4); X.stroke(); }
    if (o.blowO) { shape(X, g => g.ellipse(0, r * .58, r * .09 * o.blowO + 3, r * .11 * o.blowO + 3, 0, 0, 7), '#5a2e2a', 4); }
    else if (o.happy) { shape(X, g => { g.moveTo(-r * .16, r * .55); g.quadraticCurveTo(0, r * .7, r * .16, r * .55); g.closePath(); }, '#5a2e2a', 3); }
    else { X.strokeStyle = '#d9c3b0'; X.lineWidth = 5; X.lineCap = 'round'; X.beginPath(); X.moveTo(-r * .11, r * .58); X.quadraticCurveTo(0, r * .6, r * .11, r * .58); X.stroke(); }
    if (!o.partyHat) { X.fillStyle = 'rgba(255,255,255,.55)'; X.beginPath(); X.ellipse(r * .32, -r * .6, r * .16, r * .07, -.5, 0, 7); X.fill(); }
  }
  const [lx, ly] = o.look || [0, 0], ex = r * .33, ey = -r * .04;
  for (const s of [-1, 1]) {
    const x = s * ex + lx, y = ey + ly, bl = o.blink || 0;
    X.fillStyle = OUT; X.strokeStyle = OUT; X.lineCap = 'round';
    if (o.happy) { X.lineWidth = 5; X.beginPath(); X.arc(x, y + r * .04, r * .1, 1.15 * Math.PI, 1.85 * Math.PI); X.stroke(); }
    else if (bl > .8) { X.lineWidth = 5; X.beginPath(); X.arc(x, y - r * .03, r * .1, .2 * Math.PI, .8 * Math.PI); X.stroke(); }
    else {
      const ws = 1 + .35 * (+o.wide || 0); X.beginPath(); X.ellipse(x, y, r * .075 * ws, r * .1 * (1 - bl * .9) * ws, 0, 0, 7); X.fill();
      if (o.lid > 0) { X.fillStyle = o.beard ? '#e6e1e7' : '#ece8ee'; X.fillRect(x - r * .1, y - r * .13, r * .2, r * .13 * o.lid * 1.3); X.lineWidth = 4; X.beginPath(); X.moveTo(x - r * .1, y - r * .13 + r * .13 * o.lid * 1.3); X.lineTo(x + r * .1, y - r * .13 + r * .13 * o.lid * 1.3); X.stroke(); }
    }
    if (o.brow) { X.lineWidth = 5; X.beginPath(); const by = ey - r * .28, k = o.brow * s; X.moveTo(x - r * .12, by - k * r * .05); X.lineTo(x + r * .12, by + k * r * .05); X.stroke(); }
  }
  if (o.glasses) {
    X.strokeStyle = OUT; X.lineWidth = 5; for (const s of [-1, 1]) { X.beginPath(); X.arc(s * ex, ey, r * .23, 0, 7); X.stroke(); }
    X.beginPath(); X.moveTo(-ex + r * .23, ey); X.quadraticCurveTo(0, ey - r * .06, ex - r * .23, ey); X.stroke();
    X.strokeStyle = 'rgba(255,255,255,.6)'; X.lineWidth = 3; for (const s of [-1, 1]) { X.beginPath(); X.arc(s * ex, ey, r * .17, -1.1, -.5); X.stroke(); }
  }
  if (!o.beard) {
    const m = o.mouth || 0, my = r * .42, w = r * .2; X.strokeStyle = OUT; X.lineWidth = 5; X.lineCap = 'round';
    if (o.mouthOpen > .04) { shape(X, g => { g.moveTo(-w * 1.1, my - r * .03); g.quadraticCurveTo(0, my + r * .32 * o.mouthOpen, w * 1.1, my - r * .03); g.closePath(); }, '#4a1f22', 5); }
    else if (o.mouthO) shape(X, g => g.ellipse(0, my, r * .07, r * .09, 0, 0, 7), '#4a1f22', 4);
    else if (o.wavy) { X.beginPath(); for (let i = 0; i <= 8; i++) { const x = -w + i * w / 4, y = my + (i % 2 ? -1 : 1) * r * .03; i ? X.lineTo(x, y) : X.moveTo(x, y); } X.stroke(); }
    else { X.beginPath(); X.moveTo(-w, my - m * r * .04); X.quadraticCurveTo(0, my + m * r * .2, w, my - m * r * .04); X.stroke(); }
  }
  if (o.headphones) { shape(X, g => { g.arc(0, 0, r * 1.06, Math.PI * 1.05, Math.PI * 1.95); }, null, 14); X.strokeStyle = '#3b3f52'; X.lineWidth = 9; X.beginPath(); X.arc(0, 0, r * 1.06, Math.PI * 1.06, Math.PI * 1.94); X.stroke();
    for (const s of [-1, 1]) shape(X, g => rrPath(g, s * r * 1.02 - 20, -r * .12, 40, 62, 14), '#e8382f', 4); }
  if (o.partyHat) {
    shape(X, g => { g.moveTo(-r * .42, -r * .86); g.lineTo(r * .05, -r * 1.85); g.lineTo(r * .5, -r * .82); g.closePath(); }, '#e8382f');
    X.save(); X.beginPath(); X.moveTo(-r * .42, -r * .86); X.lineTo(r * .05, -r * 1.85); X.lineTo(r * .5, -r * .82); X.closePath(); X.clip();
    X.strokeStyle = '#fde047'; X.lineWidth = 12; for (let i = -2; i < 4; i++) { X.beginPath(); X.moveTo(-r, -r * .9 - i * r * .3); X.lineTo(r, -r * 1.2 - i * r * .3); X.stroke(); } X.restore();
    shape(X, g => { g.moveTo(-r * .42, -r * .86); g.lineTo(r * .05, -r * 1.85); g.lineTo(r * .5, -r * .82); g.closePath(); }, null);
    shape(X, g => g.arc(r * .05, -r * 1.88, r * .1, 0, 7), '#fde047', 4);
  }
  if (o.sweat) sweatDrops(0, 0, r, o.t || 0, o.sweat);
  X.restore();
}

function floorShadow(x, y, w, a = .3) {
  X.save(); X.translate(x, y); X.scale(1, .14); const g = X.createRadialGradient(0, 0, 0, 0, 0, w); g.addColorStop(0, `rgba(10,4,16,${a})`); g.addColorStop(1, 'rgba(10,4,16,0)');
  X.fillStyle = g; X.beginPath(); X.arc(0, 0, w, 0, 7); X.fill(); X.restore();
}
/* quilted oven mitt; ang points from wrist to fingertips, side -1/1 puts the thumb on that side */
function ovenMitt(x, y, s, ang = -Math.PI / 2, side = 1) {
  X.save(); X.translate(x, y); X.rotate(ang + Math.PI / 2); X.scale(s, s);
  const body = g => { g.moveTo(-26, 18); g.lineTo(-30, -30); g.quadraticCurveTo(-30, -66, 0, -68); g.quadraticCurveTo(30, -66, 30, -30); g.lineTo(26, 18); g.closePath(); };
  shape(X, g => { g.ellipse(side * 30, -14, 13, 22, side * .5, 0, 7); }, '#d4553b', 4);
  shape(X, body, '#d4553b'); X.save(); X.beginPath(); body(X); X.clip(); X.strokeStyle = 'rgba(120,30,20,.35)'; X.lineWidth = 3;
  for (let i = -3; i <= 3; i++) { X.beginPath(); X.moveTo(-40 + i * 16, 20); X.lineTo(20 + i * 16, -70); X.stroke(); X.beginPath(); X.moveTo(40 + i * 16, 20); X.lineTo(-20 + i * 16, -70); X.stroke(); }
  X.beginPath(); body(X); X.strokeStyle = 'rgba(255,214,150,.7)'; X.lineWidth = 7; X.shadowColor = 'rgba(255,214,150,.8)'; X.shadowBlur = 8; X.stroke(); X.restore();
  shape(X, body, null); shape(X, g => rrPath(g, -30, 8, 60, 22, 8), '#f2ece2', 4); X.restore();
}

/* ---------- armor pieces (stand-alone sprites for flying in) ---------- */
const RED = '#c4302b', REDD = '#9d2420', GOLD = '#e3b44c';
function pieceSprite(kind, x, y, rot, s = 1) {
  X.save(); X.translate(x, y); X.rotate(rot); X.scale(s, s);
  if (kind === 'chest') { shape(X, g => rrPath(g, -95, -110, 190, 220, 34), RED); shape(X, g => g.arc(0, -40, 26, 0, 7), '#bfefff', 4); shape(X, g => g.rect(-95, 60, 190, 16), GOLD, 4); }
  else if (kind === 'helmet') { shape(X, g => g.arc(0, 0, 112, 0, 7), RED); shape(X, g => g.arc(0, 0, 74, 0, 7), REDD, 4); shape(X, g => rrPath(g, -60, -100, 120, 26, 12), GOLD, 4); }
  else { const L = kind.startsWith('leg') ? 170 : 150; shape(X, g => rrPath(g, -24, -L / 2, 48, L, 24), RED); shape(X, g => g.rect(-24, -8, 48, 14), GOLD, 4); }
  X.restore();
}
/* armor assembly: pieces leave `src` at given times and land on the body; returns which parts are on */
const ARMOR_ORDER = [['legL', 0], ['legR', .12], ['chest', .28], ['armL', .44], ['armR', .56], ['helmet', .72]];
function armorState(t, t0, dur = .42) { const s = {}; for (const [k, d] of ARMOR_ORDER) s[k] = t >= t0 + d + dur ? 1 : 0; return s; }
function armorFlights(t, t0, src, gx, gy, sc = 1, dur = .42) {
  const top = gy - 460 * sc;
  const dst = { legL: [gx - 30 * sc, gy - 105 * sc], legR: [gx + 30 * sc, gy - 105 * sc], chest: [gx, top + 120 * sc], armL: [gx - 110 * sc, top + 110 * sc], armR: [gx + 110 * sc, top + 110 * sc], helmet: [gx, top - 100 * sc] };
  for (const [k, d] of ARMOR_ORDER) {
    const a = t0 + d, u = (t - a) / dur; if (u < 0 || u >= 1) continue;
    const e = outq(u), p = mix2(src, dst[k], e), arc = Math.sin(u * Math.PI) * -120;
    pieceSprite(k, p[0], p[1] + arc, (1 - e) * (k === 'helmet' ? 6 : 9) * (k.endsWith('L') ? -1 : 1), sc * (k === 'helmet' ? .9 : .85));
    X.save(); X.globalAlpha = .35 * (1 - e); X.strokeStyle = '#fff'; X.lineWidth = 6; X.beginPath(); X.moveTo(p[0], p[1] + arc); X.lineTo(mix(src[0], p[0], .7), mix(src[1], p[1] + arc, .7)); X.stroke(); X.restore();
  }
}
function clankFlash(t, t0, gx, gy, sc = 1, dur = .42) {
  const top = gy - 460 * sc; const pts = { legL: [gx - 30, gy - 105], legR: [gx + 30, gy - 105], chest: [gx, top + 120], armL: [gx - 110, top + 110], armR: [gx + 110, top + 110], helmet: [gx, top - 100] };
  for (const [k, d] of ARMOR_ORDER) { const at = t0 + d + dur; const f = bump(t, at, at + .18); if (f > 0) glow(pts[k][0], pts[k][1], 90 * f, .8 * f, '255,240,190'); }
}

/* ---------- people ---------- */
/* generic person. spec: {col, colD, hair, hairCol, legs, r, sc}  pose: see fields used below */
function person(t, gx, gy, spec, p = {}) {
  const sc = spec.sc || 1, r = (spec.r || 100) * sc, br = Math.sin(t * 2.2 + (spec.ph || 0)) * 2.5 * sc + (p.bounce || 0);
  const jit = p.jitter ? (Math.sin(t * 23) * .7 + Math.sin(t * 37 + 1) * .3) * p.jitter : 0, K = 'P' + (spec.id ||= ++SMID);
  const top = gy - 460 * sc - br + sm('P' + (spec.id ||= ++SMID) + 'sl0', t, p.slump || 0, .12) * 12 - (p.inhale || 0) * 7, A = p.armor || {};
  const Y = spec.col, Yd = spec.colD, LEG = spec.legs || '#efe6d6';
  if (!p.noShadow) floorShadow(gx, gy - 4 * sc, 125 * sc, .45);
  // legs
  for (const [dx, k] of [[-30, 'legL'], [30, 'legR']]) {
    if (A[k]) { tube([[gx + dx * sc, gy - 200 * sc], [gx + dx * sc, gy - 22 * sc]], RED, 34 * sc); shape(X, g => g.arc(gx + dx * sc, gy - 110 * sc, 13 * sc, 0, 7), GOLD, 4); shape(X, g => g.ellipse(gx + dx * sc + (dx > 0 ? 10 : -10), gy - 10 * sc, 30 * sc, 14 * sc, 0, 0, 7), RED, 4); }
    else { tube([[gx + dx * sc, gy - 200 * sc], [gx + dx * sc, gy - 12 * sc]], LEG, 16 * sc); shape(X, g => g.ellipse(gx + dx * sc + (dx > 0 ? 8 : -8), gy - 8 * sc, 22 * sc, 10 * sc, 0, 0, 7), spec.shoes || '#e2d8c6', 4); }
  }
  gx += Math.sin(t * .9 + (spec.ph || 0) * 2.1) * 3.5 * sc * (p.still ? 0 : 1);           // idle weight shift (feet stay planted)
  const sh = sc * 92, sy = top + 46 * sc;
  const restL = [gx - 112 * sc, gy - 212 * sc], restR = [gx + 112 * sc, gy - 212 * sc];
  const pocketL = [gx - 38 * sc, gy - 250 * sc], pocketR = [gx + 38 * sc, gy - 250 * sc];
  let hl = p.handL || (p.pockets ? pocketL : restL), hr = p.handR || (p.pockets ? pocketR : restR);
  hl = smRel(K + 'hl', t, hl, gx, gy, .055); hr = smRel(K + 'hr', t, hr, gx, gy, .055);
  p = Object.assign({}, p, { look: sm(K + 'lk', t, p.look || [0, 0], .07), headRot: sm(K + 'hrot', t, p.headRot || 0, .09) + Math.sin(t * .75 + (spec.ph || 0) * 1.3) * .025 * (p.still ? 0 : 1), headX: sm(K + 'hx', t, p.headX || 0, .09),
    headDrop: sm(K + 'hd', t, p.headDrop || 0, .09), wide: sm(K + 'wd', t, p.wide ? 1 : 0, .06), mouthOpen: sm(K + 'mo', t, +p.mouthOpen || 0, .05), slump: sm(K + 'sl', t, p.slump || 0, .12) });
  hl = [hl[0] + jit, hl[1]]; hr = [hr[0] - jit, hr[1]];
  const armCol = k => A[k] ? RED : (k === 'armL' ? Yd : Y);
  const handCol = k => A[k] ? GOLD : '#f1ece6';
  // far (left) arm behind body
  let [e, h] = ik(gx - sh, sy, hl[0], hl[1], 108 * sc, 104 * sc, -1); tube([[gx - sh, sy], e, h], armCol('armL'), 34 * sc);
  const mL = p.mittL ?? p.mitts, mR = p.mittR ?? p.mitts;
  spec._hl = h;
  if (!p.pockets) { if (mL) ovenMitt(h[0], h[1], 1.0 * sc, Math.atan2(h[1] - e[1], h[0] - e[0]), 1); else mitten(h[0], h[1], 18 * sc, handCol('armL')); }
  if (p.cup) { shape(X, g => rrPath(g, h[0] - 18 * sc, h[1] - 52 * sc, 36 * sc, 46 * sc, 8), '#f4f1ea', 4); shape(X, g => g.rect(h[0] - 18 * sc, h[1] - 52 * sc, 36 * sc, 12 * sc), '#8a5a3c', 4); }
  // torso
  const torso = g => {
    g.moveTo(gx - 100 * sc, top + 34 * sc); g.quadraticCurveTo(gx - 104 * sc, top + 4 * sc, gx - 70 * sc, top); g.lineTo(gx + 70 * sc, top); g.quadraticCurveTo(gx + 104 * sc, top + 4 * sc, gx + 100 * sc, top + 34 * sc);
    g.lineTo(gx + 104 * sc, gy - 208 * sc); g.quadraticCurveTo(gx + 104 * sc, gy - 196 * sc, gx + 90 * sc, gy - 196 * sc); g.lineTo(gx - 90 * sc, gy - 196 * sc); g.quadraticCurveTo(gx - 104 * sc, gy - 196 * sc, gx - 104 * sc, gy - 208 * sc); g.closePath();
  };
  shape(X, torso, A.chest ? RED : Y, 0); shadeClip(torso, gx - 62 * sc, 'rgba(90,40,10,.3)'); rimClip(torso, gx + 50 * sc); shape(X, torso, null);
  if (A.chest) {
    shape(X, g => g.rect(gx - 104 * sc, gy - 250 * sc, 208 * sc, 18 * sc), GOLD, 4);
    for (const s of [-1, 1]) shape(X, g => g.arc(gx + s * 86 * sc, top + 26 * sc, 30 * sc, 0, 7), GOLD, 4);
    shape(X, g => g.arc(gx, top + 96 * sc, 30 * sc, 0, 7), '#cdf3ff', 4);
    glow(gx, top + 96 * sc, (44 + 90 * (p.chestGlow || 0)) * sc, .55 + .3 * (p.chestGlow || 0));
  } else {
    shape(X, g => { g.moveTo(gx - 56 * sc, top + 2); g.lineTo(gx, top + 52 * sc); g.lineTo(gx + 56 * sc, top + 2); }, Yd, 4);
    shape(X, g => { g.moveTo(gx - 58 * sc, gy - 288 * sc); g.lineTo(gx + 58 * sc, gy - 288 * sc); g.lineTo(gx + 72 * sc, gy - 226 * sc); g.lineTo(gx - 72 * sc, gy - 226 * sc); g.closePath(); }, 'rgba(0,0,0,.08)', 4);
    if (p.chestLight) { glow(gx, top + 96 * sc, (40 + 90 * p.chestLight) * sc, .95 * p.chestLight); shape(X, g => g.arc(gx, top + 96 * sc, 16 * sc, 0, 7), 'rgba(220,250,255,.9)', 0); }
  }
  // neck + head
  const hx = gx + (p.headX || 0) + jit * .5, hy = top - 100 * sc + (p.headDrop || 0);
  tube([[gx, top + 4], [hx, hy + 80 * sc]], LEG === RED ? '#efe6d6' : '#efe6d6', 13 * sc);
  head(hx, hy, r, p.headRot || 0, { hair: spec.hair, hairCol: spec.hairCol, helmet: A.helmet, blink: p.blink, mouth: p.mouth, mouthOpen: p.mouthOpen, mouthO: p.mouthO, wavy: p.wavy,
    look: p.look, brow: p.brow, lid: p.lid, wide: p.wide, happy: p.happy, headphones: p.headphones, sweat: p.sweat, t, partyHat: p.partyHat, faceplate: p.faceplate, eyes: p.eyes });
  // near (right) arm in front
  [e, h] = ik(gx + sh, sy, hr[0], hr[1], 108 * sc, 104 * sc, 1); tube([[gx + sh, sy], e, h], armCol('armR'), 36 * sc);
  if (p.pockets) return;
  if (p.snapR !== undefined) {               // snapping hand: thumb + middle finger, a click flash at the snap moment
    shape(X, g => rrPath(g, h[0] - 8 * sc, h[1] - 44 * sc, 16 * sc, 36 * sc, 8 * sc), handCol('armR'), 4);
    mitten(h[0], h[1], 20 * sc, handCol('armR'));
    if (p.snapR > 0) { X.save(); X.strokeStyle = `rgba(255,240,170,${p.snapR})`; X.lineWidth = 6; for (let i = 0; i < 6; i++) { const a = -Math.PI / 2 + (i - 2.5) * .45; X.beginPath(); X.moveTo(h[0] + Math.cos(a) * 40, h[1] - 40 + Math.sin(a) * 40); X.lineTo(h[0] + Math.cos(a) * (70 + 30 * p.snapR), h[1] - 40 + Math.sin(a) * (70 + 30 * p.snapR)); X.stroke(); } X.restore(); }
  } else if (mR) ovenMitt(h[0], h[1], 1.05 * sc, Math.atan2(h[1] - e[1], h[0] - e[0]), -1); else mitten(h[0], h[1], 20 * sc, handCol('armR'));
  if (p.coverChest) { mitten(gx - 20 * sc, top + 100 * sc, 22 * sc); mitten(gx + 22 * sc, top + 92 * sc, 22 * sc);
    X.save(); X.globalCompositeOperation = 'lighter'; X.globalAlpha = .55 * p.coverChest; X.fillStyle = '#9fe4ff';
    for (const [a, l] of [[-2.75, 260], [-0.55, 300], [-0.15, 250], [0.5, 230], [2.6, 240], [3.0, 200]]) { X.beginPath(); X.moveTo(gx, top + 96 * sc); X.lineTo(gx + Math.cos(a - .05) * l, top + 96 * sc + Math.sin(a - .05) * l); X.lineTo(gx + Math.cos(a + .05) * l, top + 96 * sc + Math.sin(a + .05) * l); X.fill(); }
    X.restore(); glow(gx, top + 96 * sc, 110, .5); }
}
const HERO = { col: '#e4ae3c', colD: '#bf8a24', hair: 'curly' };

/* Dave: bald, beard, round glasses, navy bathrobe, plaid pants, mug */
function dave(t, gx, gy, p = {}) {
  const br = Math.sin(t * 1.7 + 1) * 2.5 + (p.bounce || 0), top = gy - 520 - br;
  const N = '#2c3d6e', Nd = '#1f2c52', Nl = '#5d70a3';
  if (!p.noShadow) floorShadow(gx, gy - 4, 175, .45);
  for (const dx of [-46, 46]) {
    const leg = g => rrPath(g, gx + dx - 26, gy - 200, 52, 196, 14);
    shape(X, leg, '#3e5a95', 0); X.save(); X.beginPath(); leg(X); X.clip(); X.strokeStyle = '#7192cc'; X.lineWidth = 4;
    for (let y = gy - 196; y < gy; y += 24) { X.beginPath(); X.moveTo(gx + dx - 30, y); X.lineTo(gx + dx + 30, y); X.stroke(); }
    for (let x = gx + dx - 14; x < gx + dx + 30; x += 20) { X.beginPath(); X.moveTo(x, gy - 200); X.lineTo(x, gy); X.stroke(); } X.restore(); shape(X, leg, null);
    shape(X, g => g.ellipse(gx + dx + (dx > 0 ? 10 : -10), gy - 6, 40, 13, 0, 0, 7), '#25233c', 4);
  }
  gx += Math.sin(t * .8 + 2) * 3 * (p.still ? 0 : 1);
  const hl = smRel('Dhl', t, p.handL || [gx - 150, gy - 250], gx, gy, .06);
  p = Object.assign({}, p, { look: sm('Dlk', t, p.look || [5, 0], .07), headRot: sm('Drot', t, p.headRot || 0, .09) + Math.sin(t * .6 + 1) * .02 * (p.still ? 0 : 1), lid: sm('Dlid', t, p.lid ?? .25, .08) });
  let [e, h] = ik(gx - 124, top + 60, hl[0], hl[1], 124, 118, -1); tube([[gx - 124, top + 60], e, h], Nd, 46);
  if (p.tapeRoll) { shape(X, g => g.arc(h[0], h[1] - 30, 30, 0, 7), '#b8b8c0'); shape(X, g => g.arc(h[0], h[1] - 30, 13, 0, 7), '#4a3d4c', 4); }
  mitten(h[0], h[1], 22);
  const robe = g => {
    g.moveTo(gx - 132, top + 52); g.quadraticCurveTo(gx - 130, top + 10, gx - 80, top + 4); g.lineTo(gx + 80, top + 4); g.quadraticCurveTo(gx + 130, top + 10, gx + 132, top + 52);
    g.lineTo(gx + 150, gy - 178); g.quadraticCurveTo(gx + 150, gy - 164, gx + 134, gy - 164); g.lineTo(gx - 134, gy - 164); g.quadraticCurveTo(gx - 150, gy - 164, gx - 150, gy - 178); g.closePath();
  };
  shape(X, robe, N, 0); shadeClip(robe, gx - 80, 'rgba(10,15,40,.35)'); rimClip(robe, gx + 70); shape(X, robe, null);
  shape(X, g => { g.moveTo(gx - 48, top + 6); g.lineTo(gx, top + 140); g.lineTo(gx + 48, top + 6); }, '#8e8b98', 4);
  shape(X, g => { g.moveTo(gx - 62, top + 6); g.lineTo(gx - 46, top + 6); g.lineTo(gx + 10, top + 214); g.lineTo(gx - 6, top + 214); g.closePath(); }, Nl, 4);
  shape(X, g => { g.moveTo(gx + 62, top + 6); g.lineTo(gx + 46, top + 6); g.lineTo(gx + 2, top + 170); g.lineTo(gx - 8, top + 150); g.closePath(); }, Nl, 4);
  shape(X, g => g.rect(gx - 146, gy - 330, 292, 30), Nd, 4); shape(X, g => rrPath(g, gx + 34, gy - 336, 30, 98, 10), Nl, 4);
  const rot = p.headRot || 0, hx = gx + rot * -60, hy = top - 112;
  tube([[gx, top + 6], [hx, hy + 90]], '#efe6d6', 14);
  head(hx, hy, 114, rot, { beard: 1, glasses: 1, blink: p.blink, look: p.look || [5, 0], lid: p.lid ?? .25, partyHat: p.partyHat, blowO: p.blowO, happy: p.happy, t });
  if (p.noMug) { const hr = smRel('Dhr', t, p.handR || [gx + 150, gy - 250], gx, gy, .06); [e, h] = ik(gx + 124, top + 60, hr[0], hr[1], 124, 118, 1); tube([[gx + 124, top + 60], e, h], N, 46); mitten(h[0], h[1], 23); return; }
  const lift = p.lift || 0, tx = gx + 70, ty = mix(top + 178, hy + 112, lift);
  [e, h] = ik(gx + 124, top + 60, tx, ty, 124, 118, 1); tube([[gx + 124, top + 60], e, h], N, 46);
  X.save(); X.translate(h[0] - 40, h[1] - 10); X.rotate(-0.42 * lift);
  shape(X, g => rrPath(g, -32, -40, 64, 76, 12), '#f4f1ea'); X.beginPath(); X.arc(-32, -2, 22, 1.5, 4.7); X.lineWidth = 12; X.strokeStyle = OUT; X.stroke(); X.lineWidth = 6; X.strokeStyle = '#f4f1ea'; X.stroke();
  X.fillStyle = '#6b4a36'; X.beginPath(); X.ellipse(0, -38, 26, 6, 0, 0, 7); X.fill();
  if (p.toastInMug) { shape(X, g => rrPath(g, -22, -80, 44, 48, 10), '#d9a35a', 4); shape(X, g => rrPath(g, -15, -73, 30, 34, 8), '#f3d7a0', 0); }
  X.restore();
  mitten(h[0], h[1], 23);
  if ((p.steam ?? 1) > 0) {
    X.strokeStyle = `rgba(255,255,255,${.4 * (p.steam ?? 1)})`; X.lineWidth = 5; X.lineCap = 'round';
    for (const d of [-12, 10]) { X.beginPath(); for (let i = 0; i < 7; i++) { const yy = h[1] - 56 - i * 13, xx = h[0] - 40 + d + Math.sin(t * 3.5 + i * .9 + d) * 7; i ? X.lineTo(xx, yy) : X.moveTo(xx, yy); } X.stroke(); }
  }
}

/* ---------- camera ---------- */
function camera(t, shots, scene) {
  const s = shots.find(s => t >= s.a && t < s.b) || shots[shots.length - 1];
  const u = clamp((t - s.a) / (s.b - s.a)), z = s.z + (s.dz || 0) * u;
  let cx = s.cx + (s.dx || 0) * u, cy = s.cy + (s.dy || 0) * u;
  const hw = W / (2 * z), hh = (H - 2 * BAR) / (2 * z);              // keep the frame inside the background
  cx = clamp(cx, hw + 6, W - hw - 6); cy = clamp(cy, hh + 6 - BAR / z, H - hh - 6 + BAR / z);
  const shake = s.shake ? s.shake(t) : 0; if (s !== LASTSHOT) { SMS.clear(); LASTSHOT = s; }
  X.setTransform(1, 0, 0, 1, 0, 0); X.fillStyle = '#000'; X.fillRect(0, 0, W, H);
  X.setTransform(z, 0, 0, z, W / 2 - cx * z + Math.sin(t * .6) * 4 + shake * (Math.sin(t * 31) * .7 + Math.sin(t * 53 + 2) * .3), H / 2 - cy * z + shake * (Math.cos(t * 27) * .7 + Math.cos(t * 47 + 1) * .3));
  return s;
}
function letterbox() { X.setTransform(1, 0, 0, 1, 0, 0); X.fillStyle = '#000'; X.fillRect(0, 0, W, BAR); X.fillRect(0, H - BAR, W, BAR); }
/* darkness with holes of light (for night / power cut) */
let DARK = null;
function darkness(a, lights, col = '10,10,32') {
  if (a <= 0) return;
  if (!DARK) { DARK = document.createElement('canvas'); DARK.width = W; DARK.height = H; }
  const g = DARK.getContext('2d'); g.setTransform(1, 0, 0, 1, 0, 0); g.globalCompositeOperation = 'source-over'; g.clearRect(0, 0, W, H);
  g.fillStyle = `rgba(${col},${a})`; g.fillRect(0, 0, W, H); g.globalCompositeOperation = 'destination-out';
  for (const [x, y, r, k] of lights) { const gr = g.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, `rgba(0,0,0,${k ?? 1})`); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); }
  const m = X.getTransform(); X.setTransform(1, 0, 0, 1, 0, 0); X.drawImage(DARK, 0, 0); X.setTransform(m);
}

/* ---------- softness: temporal smoothing of poses (sequential renders; resets on jumps and cuts) ---------- */
const SMS = new Map(); let SMID = 0, LASTSHOT = null;
function sm(key, t, v, tau = .08) {
  const s = SMS.get(key), arr = Array.isArray(v);
  if (!s || t < s.t || t - s.t > .12) { SMS.set(key, { t, v: arr ? v.slice() : v }); return v; }
  const k = 1 - Math.exp(-(t - s.t) / tau); s.t = t;
  s.v = arr ? s.v.map((x, i) => x + (v[i] - x) * k) : s.v + (v - s.v) * k; return arr ? s.v.slice() : s.v;
}
const smRel = (key, t, p, ox, oy, tau) => { const r = sm(key, t, [p[0] - ox, p[1] - oy], tau); return [r[0] + ox, r[1] + oy]; };

/* ---------- soft frame: motion blur (sub-frames) + bloom + light haze + vignette + grain ---------- */
let ACC = null, PP = null;
function renderSoft(draw, t, n = 3, shutter = .5) {
  if (!ACC) { ACC = document.createElement('canvas'); ACC.width = W; ACC.height = H; }
  const g = ACC.getContext('2d');
  for (let i = 0; i < n; i++) { X.setTransform(1, 0, 0, 1, 0, 0); X.globalAlpha = 1; draw(t + ((i + .5) / n - .5) * shutter / 24); g.globalAlpha = 1 / (i + 1); g.drawImage(X.canvas, 0, 0); }
  X.setTransform(1, 0, 0, 1, 0, 0); X.globalAlpha = 1; X.drawImage(ACC, 0, 0); post(t);
}
function post(t) {
  if (!PP) {
    PP = { b: document.createElement('canvas'), n: document.createElement('canvas') }; PP.b.width = 480; PP.b.height = 270; PP.n.width = PP.n.height = 256;
    const ng = PP.n.getContext('2d'), id = ng.createImageData(256, 256), r = rng(7);
    for (let i = 0; i < id.data.length; i += 4) { const v = 128 + (r() - .5) * 90; id.data[i] = id.data[i + 1] = id.data[i + 2] = v; id.data[i + 3] = 255; } ng.putImageData(id, 0, 0);
  }
  X.setTransform(1, 0, 0, 1, 0, 0);
  const bg = PP.b.getContext('2d'); bg.filter = 'none'; bg.clearRect(0, 0, 480, 270); bg.filter = 'brightness(.85) contrast(2.4) blur(7px)'; bg.drawImage(X.canvas, 0, 0, 480, 270);
  X.save(); X.globalCompositeOperation = 'screen'; X.globalAlpha = .3; X.drawImage(PP.b, 0, 0, W, H); X.restore();
  X.save(); let gr = X.createRadialGradient(W * .62, H * .3, 50, W * .62, H * .3, W * .7); gr.addColorStop(0, 'rgba(255,196,150,.07)'); gr.addColorStop(1, 'rgba(255,196,150,0)');
  X.globalCompositeOperation = 'screen'; X.fillStyle = gr; X.fillRect(0, 0, W, H);
  gr = X.createRadialGradient(W / 2, H / 2, H * .45, W / 2, H / 2, W * .62); gr.addColorStop(0, 'rgba(14,6,22,0)'); gr.addColorStop(1, 'rgba(14,6,22,.42)');
  X.globalCompositeOperation = 'source-over'; X.fillStyle = gr; X.fillRect(0, 0, W, H);
  X.globalCompositeOperation = 'overlay'; X.globalAlpha = .06; const ox = Math.floor((t * 24 * 97) % 256), oy = Math.floor((t * 24 * 61) % 256);
  X.translate(-ox, -oy); X.fillStyle = X.createPattern(PP.n, 'repeat'); X.fillRect(0, 0, W + 256, H + 256); X.restore();
  letterbox();
}
