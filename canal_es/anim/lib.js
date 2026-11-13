/* Code-drawn cartoon library for the Spanish "¿Qué pasaría si…?" channel.
   Style: flat shapes, thin dark outline, round pale heads with dot eyes, tube limbs, mitten hands.
   Everything is drawn into a canvas context passed as `g`, so the same characters can go
   to the "world" layer (which turns gray-blue when time stops) or the "color" layer. */
const VERT = typeof location !== 'undefined' && /[?&]vert=1/.test(location.search);   // 1080x1920 frames for native vertical Shorts (3D shots)
const W = VERT ? 1080 : 1920, H = VERT ? 1920 : 1080, OUT = '#1b1320', LW = 5;
let CUR_LOOK = {};   // per-location light: rim colour, grade tint (set by drawSet)
const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
const io = t => { t = clamp(t); return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
const outC = t => { t = clamp(t); return 1 - Math.pow(1 - t, 3); };
const inC = t => { t = clamp(t); return t * t * t; };
const back = t => { t = clamp(t); const c1 = 1.6, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); };
const R = (t, a, b, f = io) => f((t - a) / (b - a));
const lin = t => clamp(t);
function shade(hex, k) { // k>0 lighter (towards white), k<0 darker
  const n = parseInt(hex.slice(1), 16); let r = n >> 16, gg = n >> 8 & 255, b = n & 255; const t = k > 0 ? 255 : 0, a = Math.abs(k);
  r = Math.round(r + (t - r) * a); gg = Math.round(gg + (t - gg) * a); b = Math.round(b + (t - b) * a); return `rgb(${r},${gg},${b})`; }
const mix = (a, b, u) => a + (b - a) * u;
const mix2 = (p, q, u) => [mix(p[0], q[0], u), mix(p[1], q[1], u)];
const bump = (t, a, b) => Math.max(0, Math.sin(clamp((t - a) / (b - a)) * Math.PI));
const rnd = s => () => (s = (s * 16807) % 2147483647) / 2147483647;
const blinkAt = (t, list) => Math.max(0, ...list.map(b => bump(t, b, b + .16)));
/* natural blinking every ~3-4 s, offset by a seed */
const autoBlink = (t, seed = 0) => { const p = 3.3 + (seed % 5) * .37, u = ((t + seed * 1.37) % p); return bump(u, 0, .16); };

function rrPath(g, x, y, w, h, r) { r = Math.min(r, w / 2, h / 2); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); }
let INK = OUT, INK_W = .72;   // outline colour/weight; sets are built with a lighter, tinted ink
function shape(g, path, fill, lw = LW) { g.beginPath(); path(g); if (fill) { g.fillStyle = fill; g.fill(); } if (lw) { g.lineWidth = lw * INK_W; g.strokeStyle = INK; g.lineJoin = 'round'; g.stroke(); } }
function tubeHi(g, pts, col, w) { g.save(); g.lineCap = 'round'; g.lineJoin = 'round'; g.beginPath(); pts.forEach((p, i) => i ? g.lineTo(p[0] + w * .18, p[1] - w * .14) : g.moveTo(p[0] + w * .18, p[1] - w * .14)); g.strokeStyle = 'rgba(255,255,255,.22)'; g.lineWidth = w * .28; g.stroke(); g.restore(); }
function tube(g, pts, col, w, ol = LW) { g.lineCap = 'round'; g.lineJoin = 'round'; g.beginPath(); pts.forEach((p, i) => i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1]));
  if (ol) { g.strokeStyle = INK; g.lineWidth = w + 2 * ol * INK_W; g.stroke(); } g.strokeStyle = col; g.lineWidth = w; g.stroke(); }
function ik(sx, sy, tx, ty, L1, L2, out) { let dx = tx - sx, dy = ty - sy, d = Math.hypot(dx, dy); const m = L1 + L2 - 1; if (d > m) { tx = sx + dx / d * m; ty = sy + dy / d * m; d = m; }
  if (d < 1) d = 1; const b = Math.atan2(ty - sy, tx - sx), o = Math.acos(clamp((L1 * L1 + d * d - L2 * L2) / (2 * L1 * d), -1, 1));
  const e1 = [sx + L1 * Math.cos(b + o), sy + L1 * Math.sin(b + o)], e2 = [sx + L1 * Math.cos(b - o), sy + L1 * Math.sin(b - o)];
  const sc = e => e[1] + .35 * out * e[0];   // y grows downward: prefer the lower elbow, then the outer one
  return [sc(e1) >= sc(e2) ? e1 : e2, [tx, ty]]; }
function mitten(g, x, y, r, col = '#f1ece6') { shape(g, q => q.arc(x, y, r, 0, 7), col); }
function circ(g, x, y, r, fill, lw = LW) { shape(g, q => q.arc(x, y, r, 0, 7), fill, lw); }
function ell(g, x, y, rx, ry, rot, fill, lw = LW) { shape(g, q => q.ellipse(x, y, rx, ry, rot, 0, 7), fill, lw); }
function line(g, pts, col = OUT, w = LW) { const ink = col === OUT; g.lineCap = 'round'; g.lineJoin = 'round'; g.strokeStyle = ink ? INK : col; g.lineWidth = ink ? w * INK_W : w; g.beginPath(); pts.forEach((p, i) => i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1])); g.stroke(); }
function text(g, s, x, y, size, col, font = 'Bangers', align = 'left', stroke = null, sw = 8) { g.font = `${size}px ${font}`; g.textAlign = align; g.textBaseline = 'alphabetic';
  if (stroke) { g.lineJoin = 'round'; g.strokeStyle = stroke; g.lineWidth = sw; g.strokeText(s, x, y); } g.fillStyle = col; g.fillText(s, x, y); g.textAlign = 'left'; }

/* ---------------------------------------------------------------- cast */
const SKIN = '#ece8ee', SKIN_SH = '#cbc3cd', HAND = '#f1ece6';
const CAST = {
  tu:      { r: 100, hair: 'curly', hairCol: '#1f1719', body: 'hoodie', top: '#e4ae3c', topD: '#bf8a24', pants: '#3b4a6b', shoe: '#e9e2d4', seed: 1 },
  nacho:   { r: 104, hair: 'cap', hairCol: '#5a3a26', capCol: '#3f8a4f', body: 'track', top: '#d9643a', topD: '#b04a26', stripe: '#f4efe6', pants: '#2f3440', shoe: '#f2f2f2', s: 1.07, seed: 2, freckles: 1 },
  valeria: { r: 96, hair: 'ponytail', hairCol: '#2b1a1f', body: 'jacket', top: '#7a4fb3', topD: '#5d3a8f', inner: '#f4f1ea', pants: '#2c2f45', shoe: '#e9e2d4', s: .97, seed: 3, lashes: 1 },
  mama:    { r: 92, hair: 'bob', hairCol: '#6b3f2a', body: 'cardigan', top: '#3f8f8a', topD: '#2f6d69', inner: '#f2e6d8', apron: '#f6efe2', pants: '#4a3b52', shoe: '#5a4a5a', s: 1.0, legL: 238, torsoL: 290, seed: 4, lashes: 1, earrings: 1 },
  profe:   { r: 100, hair: 'baldSides', hairCol: '#9a9aa2', body: 'suit', top: '#7b5a3c', topD: '#5e4329', inner: '#f4f1ea', tie: '#b8343a', pants: '#4a3a2c', shoe: '#2a2020', s: 1.02, legL: 236, torsoL: 296, seed: 5, stache: 1, glasses: 1 },
  // extras: classmates and party guests
  ex1: { r: 96, hair: 'short', hairCol: '#3b2a20', body: 'tee', top: '#4f7fc4', topD: '#3a63a0', pants: '#33384a', shoe: '#ddd', seed: 6 },
  ex2: { r: 94, hair: 'bun', hairCol: '#1d1418', body: 'tee', top: '#e07a8a', topD: '#c05a6c', pants: '#3a3550', shoe: '#ddd', seed: 7, lashes: 1 },
  ex3: { r: 98, hair: 'buzz', hairCol: '#2a201c', body: 'hoodie', top: '#5aa37a', topD: '#3f8160', pants: '#2e3240', shoe: '#ddd', seed: 8 },
  ex4: { r: 95, hair: 'long', hairCol: '#8a5a2b', body: 'tee', top: '#f0d06a', topD: '#c9a843', pants: '#41405a', shoe: '#ddd', seed: 9, lashes: 1 },
  ex5: { r: 97, hair: 'short', hairCol: '#14100f', body: 'tee', top: '#9c6fcf', topD: '#7c52ad', pants: '#2c2f3c', shoe: '#ddd', seed: 10, glasses: 1 },
  ex6: { r: 93, hair: 'curlyShort', hairCol: '#2a1810', body: 'hoodie', top: '#e8875a', topD: '#c56a40', pants: '#384050', shoe: '#ddd', seed: 11 },
};

/* ---------------------------------------------------------------- head */
function hairBack(g, c, r, p) {
  if (c.hair === 'ponytail') { const sw = (p.tailSwing || 0);
    g.save(); g.translate(r * .78, -r * .5); g.rotate(-.35 + sw);
    shape(g, q => { q.moveTo(-r * .14, 0); q.quadraticCurveTo(r * .5, r * .3, r * .26, r * 1.05); q.quadraticCurveTo(r * .1, r * 1.2, -r * .05, r * .95); q.quadraticCurveTo(r * .1, r * .4, -r * .14, 0); }, c.hairCol);
    shape(g, q => rrPath(q, -r * .2, -r * .1, r * .3, r * .2, 6), '#e0b04a', 4); g.restore(); }
  if (c.hair === 'bob') shape(g, q => { q.moveTo(-r * 1.08, -r * .1); q.quadraticCurveTo(-r * 1.15, r * .72, -r * .75, r * .78); q.lineTo(r * .75, r * .78); q.quadraticCurveTo(r * 1.15, r * .72, r * 1.08, -r * .1); q.closePath(); }, c.hairCol);
  if (c.hair === 'long') shape(g, q => { q.moveTo(-r * 1.02, -r * .2); q.quadraticCurveTo(-r * 1.12, r * 1.1, -r * .7, r * 1.3); q.lineTo(r * .7, r * 1.3); q.quadraticCurveTo(r * 1.12, r * 1.1, r * 1.02, -r * .2); q.closePath(); }, c.hairCol);
  if (c.hair === 'bun') circ(g, 0, -r * 1.05, r * .34, c.hairCol);
}
function hairFront(g, c, r, p) {
  const H = c.hairCol;
  if (c.hair === 'curly' || c.hair === 'curlyShort') {
    const k = c.hair === 'curly' ? 1 : .82;
    for (const [a, b, s] of [[-.72, -.52, .3], [-.5, -.78, .31], [-.16, -.92, .31], [.2, -.9, .3], [.52, -.76, .3], [.76, -.5, .28], [-.88, -.2, .24], [.88, -.18, .22], [-.3, -.68, .26], [.06, -.7, .26], [.38, -.62, .25]])
      circ(g, a * r, b * r * k + (1 - k) * -r * .2, s * r * k, H, 4);
    g.strokeStyle = '#463638'; g.lineWidth = 4; for (const [a, b] of [[-.5, -.8], [.2, -.92], [.62, -.72]]) { g.beginPath(); g.arc(a * r, b * r * k, r * .13, 3.6, 5.2); g.stroke(); }
    if (p.grayHair) { g.strokeStyle = '#ffffff'; g.lineWidth = 5; g.beginPath(); g.moveTo(r * .1, -r * .95); g.bezierCurveTo(r * .25, -r * 1.25, r * .05, -r * 1.35, r * .22, -r * 1.5); g.stroke(); }
  }
  if (c.hair === 'cap') { // cap worn backwards-ish: dome + short brim to the side
    shape(g, q => { q.moveTo(-r * .98, -r * .25); q.quadraticCurveTo(-r * .95, -r * 1.12, 0, -r * 1.1); q.quadraticCurveTo(r * .95, -r * 1.12, r * .98, -r * .25); q.quadraticCurveTo(0, -r * .42, -r * .98, -r * .25); }, c.capCol);
    shape(g, q => { q.moveTo(-r * .9, -r * .3); q.quadraticCurveTo(-r * 1.45, -r * .32, -r * 1.5, -r * .14); q.quadraticCurveTo(-r * 1.2, -r * .1, -r * .86, -r * .18); q.closePath(); }, c.capCol);
    circ(g, 0, -r * 1.08, r * .07, '#2d6b3b', 3);
    shape(g, q => { q.moveTo(-r * .4, -r * .62); q.lineTo(r * .4, -r * .62); }, null, 3);
  }
  if (c.hair === 'ponytail' || c.hair === 'long') {
    shape(g, q => { q.moveTo(-r * 1.0, -r * .05); q.quadraticCurveTo(-r * 1.02, -r * 1.08, 0, -r * 1.06); q.quadraticCurveTo(r * 1.02, -r * 1.08, r * 1.0, -r * .05);
      q.quadraticCurveTo(r * .78, -r * .55, r * .2, -r * .58); q.quadraticCurveTo(-r * .3, -r * .52, -r * .62, -r * .38); q.quadraticCurveTo(-r * .86, -r * .3, -r * 1.0, -r * .05); }, H);
    g.strokeStyle = 'rgba(255,255,255,.18)'; g.lineWidth = 6; g.beginPath(); g.arc(-r * .2, -r * .55, r * .4, 3.6, 4.6); g.stroke();
  }
  if (c.hair === 'bob') shape(g, q => { q.moveTo(-r * 1.06, r * .1); q.quadraticCurveTo(-r * 1.1, -r * 1.12, 0, -r * 1.08); q.quadraticCurveTo(r * 1.1, -r * 1.12, r * 1.06, r * .1);
      q.quadraticCurveTo(r * .9, -r * .5, r * .3, -r * .55); q.quadraticCurveTo(-r * .2, -r * .7, -r * .55, -r * .45); q.quadraticCurveTo(-r * .9, -r * .2, -r * 1.06, r * .1); }, H);
  if (c.hair === 'short') shape(g, q => { q.moveTo(-r * .98, -r * .2); q.quadraticCurveTo(-r * 1.02, -r * 1.08, 0, -r * 1.06); q.quadraticCurveTo(r * 1.02, -r * 1.08, r * .98, -r * .2);
      q.quadraticCurveTo(r * .7, -r * .62, r * .1, -r * .6); q.quadraticCurveTo(-r * .5, -r * .7, -r * .98, -r * .2); }, H);
  if (c.hair === 'bun') shape(g, q => { q.moveTo(-r * .98, -r * .1); q.quadraticCurveTo(-r * 1.0, -r * 1.06, 0, -r * 1.04); q.quadraticCurveTo(r * 1.0, -r * 1.06, r * .98, -r * .1); q.quadraticCurveTo(r * .5, -r * .66, 0, -r * .66); q.quadraticCurveTo(-r * .5, -r * .66, -r * .98, -r * .1); }, H);
  if (c.hair === 'buzz') shape(g, q => { q.arc(0, 0, r, Math.PI * 1.08, Math.PI * 1.92); q.quadraticCurveTo(0, -r * .7, -r * .92, -r * .38); }, H, 4);
  if (c.hair === 'baldSides') { for (const s of [-1, 1]) shape(g, q => { q.moveTo(s * r * .92, -r * .48); q.quadraticCurveTo(s * r * 1.22, -r * .2, s * r * 1.0, r * .18); q.quadraticCurveTo(s * r * .86, -r * .1, s * r * .92, -r * .48); }, H, 4);
    g.fillStyle = 'rgba(255,255,255,.6)'; g.beginPath(); g.ellipse(r * .3, -r * .62, r * .2, r * .08, -.5, 0, 7); g.fill(); }
}
function face(g, c, r, p) {
  const [lx, ly] = p.look || [0, 0], ex = r * .33, ey = -r * .04, bl = p.blink || 0, wide = p.wide || 0;
  for (const s of [-1, 1]) { const x = s * ex + lx, y = ey + ly;
    g.fillStyle = OUT; g.strokeStyle = OUT; g.lineCap = 'round';
    if (bl > .8 || p.sleep) { g.lineWidth = 5; g.beginPath(); g.arc(x, y - r * .03, r * .1, .2 * Math.PI, .8 * Math.PI); g.stroke(); }
    else { const ry = r * (.1 + wide * .05) * (1 - bl * .9), rx = r * (.075 + wide * .04);
      if (wide > .3) { shape(g, q => q.ellipse(x, y, rx * 1.9, ry * 1.5, 0, 0, 7), '#ffffff', 4); g.fillStyle = OUT; g.beginPath(); g.ellipse(x, y, rx * .9, ry * .8, 0, 0, 7); g.fill(); }
      else { g.beginPath(); g.ellipse(x, y, rx, ry, 0, 0, 7); g.fill(); if (ry > r * .05) { g.fillStyle = 'rgba(255,255,255,.92)'; g.beginPath(); g.arc(x + rx * .35, y - ry * .42, rx * .38, 0, 7); g.fill(); g.fillStyle = OUT; } }
      if (p.lid > 0) { g.fillStyle = SKIN; g.fillRect(x - r * .11, y - r * .14, r * .22, r * .14 * p.lid * 1.3); g.lineWidth = 4; g.beginPath(); g.moveTo(x - r * .11, y - r * .14 + r * .14 * p.lid * 1.3); g.lineTo(x + r * .11, y - r * .14 + r * .14 * p.lid * 1.3); g.stroke(); }
      if (c.lashes) { g.lineWidth = 3.5; g.beginPath(); g.moveTo(x + s * r * .07, y - r * .06); g.lineTo(x + s * r * .15, y - r * .09); g.stroke(); } }
    if (p.brow != null || c.browAlways) { const k = (p.brow || 0) * s, by = ey - r * .3 - wide * r * .06; g.lineWidth = 6; g.beginPath(); g.moveTo(x - r * .12, by - k * r * .06); g.lineTo(x + r * .12, by + k * r * .06); g.stroke(); }
  }
  if (p.monocle) { const x = ex + lx, y = ey + ly; g.save(); g.strokeStyle = '#c9a227'; g.lineWidth = 6; g.beginPath(); g.arc(x, y, r * .19, 0, 7); g.stroke();
    g.fillStyle = 'rgba(220,240,255,.25)'; g.fill(); g.lineWidth = 3; g.beginPath(); g.moveTo(x + r * .17, y + r * .08); g.quadraticCurveTo(x + r * .4, y + r * .6, x + r * .22, y + r * .95); g.stroke(); g.restore(); }
  if (c.freckles) { g.fillStyle = 'rgba(160,90,60,.55)'; for (const s of [-1, 1]) for (const [a, b] of [[.3, .22], [.42, .18], [.36, .3]]) { g.beginPath(); g.arc(s * a * r, b * r, 3, 0, 7); g.fill(); } }
  if (p.blush) { g.fillStyle = `rgba(240,120,130,${.35 * p.blush})`; for (const s of [-1, 1]) { g.beginPath(); g.ellipse(s * r * .5, r * .26, r * .14, r * .08, 0, 0, 7); g.fill(); } }
  if (c.glasses) { g.strokeStyle = OUT; g.lineWidth = 5; for (const s of [-1, 1]) { g.beginPath(); g.arc(s * ex, ey, r * .22, 0, 7); g.stroke(); }
    g.beginPath(); g.moveTo(-ex + r * .22, ey); g.quadraticCurveTo(0, ey - r * .06, ex - r * .22, ey); g.stroke();
    g.strokeStyle = 'rgba(255,255,255,.6)'; g.lineWidth = 3; for (const s of [-1, 1]) { g.beginPath(); g.arc(s * ex, ey, r * .16, -1.1, -.5); g.stroke(); } }
  // mouth: curve (smile>0, frown<0), open (0..1 talking/surprise)
  const m = p.mouth || 0, my = r * .42, w = r * .2, op = p.open || 0;
  if (op > .05) { shape(g, q => q.ellipse(0, my + r * .02, w * (.55 + .25 * op), r * (.05 + .13 * op), 0, 0, 7), '#5a2430', 4); }
  else { g.strokeStyle = OUT; g.lineWidth = 5; g.lineCap = 'round'; g.beginPath(); g.moveTo(-w, my - m * r * .04); g.quadraticCurveTo(0, my + m * r * .2, w, my - m * r * .04); g.stroke(); }
  if (c.stache) shape(g, q => { q.moveTo(0, r * .27); q.bezierCurveTo(-r * .2, r * .18, -r * .42, r * .26, -r * .5, r * .42); q.bezierCurveTo(-r * .32, r * .34, -r * .12, r * .4, 0, r * .33);
    q.bezierCurveTo(r * .12, r * .4, r * .32, r * .34, r * .5, r * .42); q.bezierCurveTo(r * .42, r * .26, r * .2, r * .18, 0, r * .27); }, c.stacheCol || '#5a5a62', 4);
  if (p.marker > 0) { // marker mustache drawn by the hero; p.marker = how much has been drawn (0..1)
    g.save(); g.strokeStyle = '#1a1a2a'; g.lineWidth = 9; g.lineCap = 'round'; g.beginPath();
    const n = 40, k = Math.floor(n * clamp(p.marker));
    for (let i = 0; i <= k; i++) { const u = i / n * 2 - 1, x = u * r * .62, y = r * .31 - Math.sin(Math.abs(u) * Math.PI) * r * .06 - (Math.abs(u) > .8 ? (Math.abs(u) - .8) * r * .9 : 0); i ? g.lineTo(x, y) : g.moveTo(x, y); }
    g.stroke(); g.restore(); }
  if (c.earrings) { g.fillStyle = '#e9c46a'; for (const s of [-1, 1]) { g.beginPath(); g.arc(s * r * .98, r * .28, 7, 0, 7); g.fill(); } }
  if (p.sweat) { for (const [x, y] of [[r * .78, -r * .45], [-r * .85, -r * .3]]) shape(g, q => { q.moveTo(x, y - 18); q.quadraticCurveTo(x + 12, y + 4, x, y + 10); q.quadraticCurveTo(x - 12, y + 4, x, y - 18); }, '#9fd3ff', 3); }
}
function drawHead(g, c, x, y, rot, p) {
  const r = c.r; g.save(); g.translate(x, y); g.rotate(rot || 0);
  hairBack(g, c, r, p);
  { const gr = g.createRadialGradient(r * .32, -r * .38, r * .08, 0, 0, r * 1.05); gr.addColorStop(0, '#fbf9fc'); gr.addColorStop(.55, SKIN); gr.addColorStop(1, SKIN_SH); shape(g, q => q.arc(0, 0, r, 0, 7), gr, 0); }
  { g.save(); g.fillStyle = 'rgba(240,130,150,.16)'; for (const s of [-1, 1]) { g.beginPath(); g.ellipse(s * r * .5, r * .27, r * .15, r * .09, 0, 0, 7); g.fill(); } g.restore(); }
  if (p.rim) { g.beginPath(); g.arc(0, 0, r - 6, -1.35, .35); g.strokeStyle = p.rim; g.lineWidth = 6; g.stroke(); }
  shape(g, q => q.arc(0, 0, r, 0, 7), null);
  face(g, c, r, p);
  hairFront(g, c, r, p);
  g.restore();
}

/* ---------------------------------------------------------------- body
   pose p (all optional):
   x,y ground position; s scale; flip -1 faces left;
   walk (0..1 amount) + phase (radians) ; sit (0..1) ;
   hL,hR hand targets in local coords (feet origin; y up is negative);
   holdL/holdR(g,x,y) draw a prop in that hand (after the arm) ;
   lean (radians) ; slump (0..1) ; jump (px up) ;
   head: hx,hy offsets, rot, look[], blink, mouth, open, brow, wide, lid, sleep, blush, sweat, marker, grayHair, tailSwing */
function charGeom(c, p) {
  const sit = p.sit || 0, walk = p.walk || 0, ph = p.phase || 0;
  const bob = -Math.abs(Math.sin(ph)) * 10 * walk;
  const breathe = p.still ? 0 : Math.sin((p.t || 0) * 2.2 + c.seed) * 2.5;
  const legL = c.legL || 200, hipY = -legL + sit * 92 * legL / 200 + bob - (p.jump || 0);
  const top = hipY - (c.torsoL || 262) + (p.slump || 0) * 14 - breathe;
  return { sit, walk, ph, hipY, top, sh: 82, rest: [c.restX || 116, c.restY || -34] };
}
const restHand = (s, G) => [s * G.rest[0], G.hipY + G.rest[1]];   // a little elbow bend at rest
/* Arm physics: every hand target goes through a damped spring (per scene, character and side),
   so gestures accelerate, overshoot a little and settle instead of snapping between poses.
   Sequential rendering (render.js) integrates it; a jump in time or a frozen character snaps. */
const ARMS = {};
/* a second copy of a character drawn in the same frame (ep02's future ghost) tags its springs, or the two copies drag each other's arms */
let ARM_TAG = '';
function armSpring(key, target, t, still, stiff = 1) {
  let s = ARMS[key];
  if (!s || still || !(t > s.t) || t - s.t > .25) { ARMS[key] = { x: target[0], y: target[1], vx: 0, vy: 0, t }; return target.slice(); }
  const w = 2 * Math.PI * 4.4 * stiff, z = .56, dt = t - s.t, n = Math.max(1, Math.ceil(dt * 480)), h = dt / n;
  for (let i = 0; i < n; i++) { const ax = w * w * (target[0] - s.x) - 2 * z * w * s.vx, ay = w * w * (target[1] - s.y) - 2 * z * w * s.vy; s.vx += ax * h; s.vy += ay * h; s.x += s.vx * h; s.y += s.vy * h; }
  s.t = t; return [s.x, s.y];
}
/* mitten with a thumb on the inner side of the forearm; `squash` flattens it on a clap */
function hand(g, e, h, r, col, squash = 0) {
  let dx = h[0] - e[0], dy = h[1] - e[1]; const L = Math.hypot(dx, dy) || 1; dx /= L; dy /= L;
  let px = -dy, py = dx; if (px * -Math.sign(h[0] || 1) < 0) { px = -px; py = -py; }
  const tx = h[0] + dx * r * .1 + px * r * .8, ty = h[1] + dy * r * .1 + py * r * .8;
  if (!squash) circ(g, tx, ty, r * .42, col, 4);
  shape(g, q => q.ellipse(h[0], h[1], r * (1 - .2 * squash), r * (1 + .1 * squash), 0, 0, 7), col);
}
/* hand targets -> springs -> clap contact -> IK; shared by the vector and the cut-out renderer */
function solveArms(c, cname, p, G, shx, shy) {
  const shL = [-shx, G.top + shy], shR = [shx, G.top + shy], walk = G.walk, ph = G.ph;
  const swing = Math.sin(ph) * walk * 34, tt = p.t || 0, idle = p.still ? 0 : 1;
  const iL = [Math.sin(tt * 1.7 + c.seed) * 3 * idle, Math.cos(tt * 1.3 + c.seed) * 2.5 * idle], iR = [Math.sin(tt * 1.5 + c.seed + 2) * 3 * idle, Math.cos(tt * 1.1 + c.seed + 1) * 2.5 * idle];
  let hL = p.hL || [restHand(-1, G)[0] - swing * .35 + iL[0], restHand(-1, G)[1] + Math.abs(swing) * .12 + iL[1]];
  let hR = p.hR || [restHand(1, G)[0] + swing * .35 + iR[0], restHand(1, G)[1] + Math.abs(swing) * .12 + iR[1]];
  const clapT = Math.abs(hR[0] - hL[0]) < 60 && Math.abs(hR[1] - hL[1]) < 60;   // hands meeting: stiffer spring, no pass-through
  const akey = (typeof SID !== 'undefined' ? SID : '') + ':' + (typeof cname === 'string' ? cname : 'x') + (p.key || '') + ARM_TAG;
  if (p.t != null && !p.noSpring) { hL = armSpring(akey + 'L', hL, tt, p.still, clapT ? 1.8 : 1); hR = armSpring(akey + 'R', hR, tt, p.still, clapT ? 1.8 : 1); }
  const rH = p.handCol ? 23 : 19;
  if (clapT && hR[0] - hL[0] < 2 * rH * .8) { const m = (hL[0] + hR[0]) / 2; hL = [m - rH * .8, hL[1]]; hR = [m + rH * .8, hR[1]]; }
  const squash = clapT ? clamp(1 - (hR[0] - hL[0] - 2 * rH * .8) / (rH * .9)) * (Math.abs(hR[1] - hL[1]) < rH ? 1 : 0) : 0;
  const [eL, hLf] = ik(shL[0], shL[1], hL[0], hL[1], 108, 104, -1), [eR, hRf] = ik(shR[0], shR[1], hR[0], hR[1], 108, 104, 1);
  return { shL, shR, eL, hLf, eR, hRf, squash };
}
function drawChar(g, cname, p) {
  const c = typeof cname === 'string' ? CAST[cname] : cname, G = charGeom(c, p);
  if (c.cut && typeof drawCut === 'function') return drawCut(g, c, cname, p, G);
  const S = (p.s || 1) * (c.s || 1);
  g.save(); g.translate(p.x || 0, p.y || 0); g.scale(S * (p.flip || 1), S); if (p.lean) g.rotate(p.lean);
  const { hipY, top, sit, walk, ph } = G;
  const legW = 22;
  if (!p.noShadow) { g.save(); const sg = g.createRadialGradient(-26, -2, 4, -26, -2, 110); sg.addColorStop(0, 'rgba(20,14,32,.30)'); sg.addColorStop(1, 'rgba(20,14,32,0)'); g.fillStyle = sg; g.beginPath(); g.ellipse(-26, -2, 110, 18, 0, 0, 7); g.fill(); g.restore(); }
  // legs
  for (const s of [-1, 1]) {
    if (sit > .5) {
      const kx = s * 36, ky = hipY + 8;
      tube(g, [[s * 30, hipY], [kx, ky]], c.pants, legW + 8);
      const fs = s > 0 ? (p.footSwing || 0) : 0;
      tube(g, [[kx, ky], [kx + s * 4 + fs, -10 - Math.abs(fs) * .4]], c.pants, legW);
      ell(g, kx + s * 10 + fs, -8 - Math.abs(fs) * .4, 24, 11, 0, c.shoe, 4);
    } else {
      const sw = Math.sin(ph + (s > 0 ? 0 : Math.PI)) * walk, lift = Math.max(0, Math.cos(ph + (s > 0 ? 0 : Math.PI))) * walk * 22;
      const fx = s * 30 + sw * 34, fy = -10 - lift - (p.jump || 0);
      tube(g, [[s * 30, hipY], [fx, fy]], c.pants, legW);
      ell(g, fx + s * 9, fy + 2, 24, 11, 0, c.shoe, 4);
    }
  }
  // far arm (screen left = -1), behind the torso
  const { shL, shR, eL, hLf, eR, hRf, squash } = solveArms(c, cname, p, G, G.sh, 46);
  const armCol = c.sleeve || c.topD;
  const farArm = () => { tube(g, [shL, eL, hLf], armCol, 34); tubeHi(g, [shL, eL, hLf], armCol, 34); if (c.stripe) tube(g, [mix2(shL, eL, .2), eL, mix2(eL, hLf, .8)], c.stripe, 6, 0); hand(g, eL, hLf, p.handCol ? 22 : 18, p.handCol || HAND, squash); if (p.holdL) p.holdL(g, hLf[0], hLf[1]); };
  if (!p.armsFront) farArm();
  // torso
  const wT = c.body === 'suit' ? 96 : 88, wH = wT - 4, hem = hipY + 6;
  const torso = q => { q.moveTo(-wT, top + 34); q.quadraticCurveTo(-wT - 4, top + 4, -62, top); q.lineTo(62, top); q.quadraticCurveTo(wT + 4, top + 4, wT, top + 34);
    q.lineTo(wH, hem - 12); q.quadraticCurveTo(wH, hem, wH - 10, hem); q.lineTo(-wH + 10, hem); q.quadraticCurveTo(-wH, hem, -wH, hem - 12); q.closePath(); };
  { const gr = g.createLinearGradient(wT, top, -wT, hem); gr.addColorStop(0, shade(c.top, .16)); gr.addColorStop(.45, c.top); gr.addColorStop(1, shade(c.top, -.14)); shape(g, torso, gr, 0); }
  g.save(); g.beginPath(); torso(g); g.clip(); g.fillStyle = 'rgba(0,0,0,.13)'; g.fillRect(-wT - 10, top - 10, 44, 400);
  if (CUR_LOOK.rim) { g.globalAlpha = .45; g.fillStyle = CUR_LOOK.rim; g.fillRect(wH - 16, top, 24, 420); g.globalAlpha = 1; }
  if (c.body === 'jacket' || c.body === 'cardigan' || c.body === 'suit') { g.fillStyle = c.inner; g.beginPath(); g.moveTo(-30, top); g.lineTo(30, top); g.lineTo(c.body === 'suit' ? 0 : 26, hem); g.lineTo(c.body === 'suit' ? 0 : -26, hem); g.closePath(); g.fill();
    g.strokeStyle = OUT; g.lineWidth = 4; g.beginPath(); g.moveTo(-30, top); g.lineTo(c.body === 'suit' ? -2 : -26, hem); g.moveTo(30, top); g.lineTo(c.body === 'suit' ? 2 : 26, hem); g.stroke(); }
  if (c.body === 'suit') { shape(g, q => { q.moveTo(-9, top + 8); q.lineTo(9, top + 8); q.lineTo(14, top + 150); q.lineTo(0, top + 172); q.lineTo(-14, top + 150); q.closePath(); }, c.tie, 3);
    shape(g, q => { q.moveTo(-30, top); q.lineTo(-62, top + 70); q.lineTo(-24, top + 120); }, null, 4); shape(g, q => { q.moveTo(30, top); q.lineTo(62, top + 70); q.lineTo(24, top + 120); }, null, 4); }
  if (c.body === 'cardigan') { g.fillStyle = '#f2e6d8'; for (let i = 0; i < 4; i++) { g.beginPath(); g.arc(34, top + 60 + i * 52, 6, 0, 7); g.fill(); } }
  if (c.apron) { shape(g, q => { q.moveTo(-50, top + 120); q.lineTo(50, top + 120); q.lineTo(62, hem + 2); q.lineTo(-62, hem + 2); q.closePath(); }, c.apron, 4); line(g, [[-50, top + 120], [-wT, top + 132]], OUT, 3); line(g, [[50, top + 120], [wT, top + 132]], OUT, 3);
    shape(g, q => rrPath(q, -26, top + 170, 52, 40, 6), 'rgba(0,0,0,.06)', 3); }
  if (c.body === 'track') { g.fillStyle = c.stripe; g.fillRect(-wT - 4, top + 30, 12, 300); g.fillRect(wT - 8, top + 30, 12, 300); shape(g, q => { q.moveTo(0, top); q.lineTo(0, hem); }, null, 4); }
  if (c.body === 'tee') { g.strokeStyle = 'rgba(0,0,0,.18)'; g.lineWidth = 4; g.beginPath(); g.arc(0, top - 6, 34, .3, Math.PI - .3); g.stroke(); }
  g.restore();
  shape(g, torso, null);
  g.save(); g.strokeStyle = 'rgba(20,10,30,.18)'; g.lineWidth = 3; g.lineCap = 'round';
  g.beginPath(); g.moveTo(-wT + 18, top + 70); g.quadraticCurveTo(-wT + 34, top + 100, -wT + 22, top + 130); g.moveTo(wT - 20, top + 80); g.quadraticCurveTo(wT - 34, top + 108, wT - 24, top + 136); g.moveTo(-30, hem - 26); g.quadraticCurveTo(0, hem - 18, 30, hem - 26); g.stroke(); g.restore();
  if (c.body === 'hoodie') { shape(g, q => { q.moveTo(-56, top + 2); q.lineTo(0, top + 52); q.lineTo(56, top + 2); }, c.topD, 4);
    shape(g, q => { q.moveTo(-58, hem - 92); q.lineTo(58, hem - 92); q.lineTo(72, hem - 30); q.lineTo(-72, hem - 30); q.closePath(); }, 'rgba(0,0,0,.08)', 4); }
  // neck + head
  const hx = (p.hx || 0), hy = top - 100 + (p.hy || 0) + (p.slump || 0) * 14;
  tube(g, [[0, top + 4], [hx * .6, hy + c.r * .8]], SKIN, 13);
  // secondary motion: idle head sway and ponytail swing while walking (live characters only)
  const tt = p.t || 0, live = !p.still && p.t != null, headIdle = live && p.rot == null ? Math.sin(tt * .8 + c.seed) * .025 : 0;
  const tail = p.tailSwing != null ? p.tailSwing : (live ? Math.sin(ph * 2) * .18 * walk + Math.sin(tt * 1.6 + c.seed) * .05 : 0);
  drawHead(g, c, hx, hy, (p.rot || 0) + headIdle, Object.assign({ blink: p.blink != null ? p.blink : (p.still ? 0 : autoBlink(p.t || 0, c.seed)) }, p, { rim: p.rim !== undefined ? p.rim : CUR_LOOK.rim, tailSwing: tail }));
  // far arm in front (for clapping, typing) and near arm
  if (p.armsFront) farArm();
  tube(g, [shR, eR, hRf], c.sleeve || c.top, 36); tubeHi(g, [shR, eR, hRf], c.sleeve || c.top, 36); if (c.stripe) tube(g, [mix2(shR, eR, .2), eR, mix2(eR, hRf, .8)], c.stripe, 6, 0);
  hand(g, eR, hRf, p.handCol ? 24 : 20, p.handCol || HAND, squash); if (p.holdR) p.holdR(g, hRf[0], hRf[1]);
  g.restore();
  return G;
}
/* local hand positions for common gestures (feed into hL/hR) */
const POSE = {
  clap: (u, G) => { // u: 0 rest -> 1 hands together at chest; returns [hL, hR]
    const y = G.top + 150, gap = mix(150, 14, u);
    return [[-gap, y + (1 - u) * 60], [gap, y + (1 - u) * 60]]; },
  wave: (t, G) => [restHand(-1, G), [150 + Math.sin(t * 9) * 26, G.top - 30]],
  shrug: (u, G) => [[mix(-108, -170, u), mix(G.hipY - 8, G.top + 60, u)], [mix(108, 170, u), mix(G.hipY - 8, G.top + 60, u)]],
  point: (u, G, dir = 1) => [restHand(-1, G), [mix(108, 230 * dir, u), mix(G.hipY - 8, G.top + 30, u)]],
  hips: (G) => [[-128, G.hipY - 40], [128, G.hipY - 40]],
  stretch: (u, G) => [[mix(-108, -80, u), mix(G.hipY - 8, G.top - 220, u)], [mix(108, 80, u), mix(G.hipY - 8, G.top - 220, u)]],
  carry: (G) => [[-70, G.top + 170], [70, G.top + 170]],
};
/* clap with a short bounce; returns hands for time t and clap time tc (hands meet at tc) */
function clapHands(t, tc, G, hold = .25, yOff = 0) {
  const u = t < tc ? R(t, tc - .32, tc, inC) : 1 - R(t, tc + hold, tc + hold + .35, io);
  const hands = POSE.clap(u, G); hands[0][1] += yOff * u; hands[1][1] += yOff * u; if (t >= tc && t < tc + .08) { hands[0][0] += 6; hands[1][0] -= 6; }
  return hands;
}

/* ---------------------------------------------------------------- animals */
function drawCat(g, x, y, s, p = {}) { // orange tabby, side view, p.jump (0 sit .. 1 mid-air stretched)
  g.save(); g.translate(x, y); g.scale(s * (p.flip || 1), s); const j = p.jump || 0;
  g.rotate(-.25 * j);
  // tail
  line(g, [[-70, -40], [-120 - 30 * j, -90 + 30 * j], [-110 - 50 * j, -150 + 60 * j]], OUT, 26); line(g, [[-70, -40], [-120 - 30 * j, -90 + 30 * j], [-110 - 50 * j, -150 + 60 * j]], '#e8914a', 16);
  // legs
  const legs = j > .3 ? [[-50, -20, -95, 10], [-30, -20, -70, 14], [40, -30, 100, -10], [60, -30, 120, -4]] : [[-45, -20, -45, 0], [-25, -20, -25, 0], [35, -20, 35, 0], [55, -20, 55, 0]];
  for (const [a, b, c2, d] of legs) { tube(g, [[a, b], [c2, d]], '#e8914a', 18); }
  ell(g, 0, -55 + 10 * j, 85 + 20 * j, 48 - 8 * j, 0, '#f0a35c');
  g.strokeStyle = '#c86f2c'; g.lineWidth = 7; for (const xx of [-30, 0, 30]) { g.beginPath(); g.moveTo(xx, -100 + 10 * j); g.lineTo(xx + 8, -70 + 10 * j); g.stroke(); }
  // head
  g.save(); g.translate(78 + 18 * j, -105 + 6 * j);
  for (const s2 of [-1, 1]) shape(g, q => { q.moveTo(s2 * 20, -30); q.lineTo(s2 * 40, -72); q.lineTo(s2 * 48, -22); q.closePath(); }, '#f0a35c', 4);
  circ(g, 0, 0, 46, '#f0a35c');
  const bl = p.blink || 0; g.fillStyle = OUT;
  for (const s2 of [-1, 1]) { if (bl > .8) line(g, [[s2 * 16 - 7, -6], [s2 * 16 + 7, -6]], OUT, 4); else { g.beginPath(); g.ellipse(s2 * 16, -6, 5 + 3 * (p.wide || 0), 8 + 4 * (p.wide || 0), 0, 0, 7); g.fill(); } }
  g.fillStyle = '#e57b8a'; g.beginPath(); g.moveTo(-6, 8); g.lineTo(6, 8); g.lineTo(0, 15); g.fill();
  line(g, [[-30, 12], [-60, 6]], OUT, 2.5); line(g, [[-30, 18], [-60, 22]], OUT, 2.5); line(g, [[30, 12], [60, 6]], OUT, 2.5); line(g, [[30, 18], [60, 22]], OUT, 2.5);
  g.restore(); g.restore();
}
function drawPigeon(g, x, y, s, p = {}) { // Pepe: gray pigeon, iridescent neck, orange eye; side view facing right
  g.save(); g.translate(x, y); g.scale(s * (p.flip || 1), s);
  for (const dx of [-10, 12]) { line(g, [[dx, -20], [dx, 0]], '#d9687a', 6); line(g, [[dx - 8, 0], [dx + 10, 0]], '#d9687a', 5); }
  shape(g, q => { q.moveTo(-90, -40); q.lineTo(-120, -30); q.lineTo(-92, -22); q.closePath(); }, '#6b7280', 4); // tail
  ell(g, -10, -48, 74, 40, -.08, '#a3aab6');
  shape(g, q => { q.moveTo(-60, -60); q.quadraticCurveTo(-10, -86, 30, -58); q.quadraticCurveTo(-10, -38, -60, -60); }, '#8a92a0', 4); // wing
  g.strokeStyle = '#555b66'; g.lineWidth = 5; g.beginPath(); g.moveTo(-40, -52); g.lineTo(-20, -52); g.moveTo(-30, -44); g.lineTo(-8, -44); g.stroke();
  const tilt = p.tilt || 0, peck = p.peck || 0;
  g.save(); g.translate(48, -78 + peck * 30); g.rotate(tilt + peck * .5);
  shape(g, q => { q.moveTo(-34, 30); q.quadraticCurveTo(-30, -6, 0, -30); q.quadraticCurveTo(26, -34, 32, -6); q.quadraticCurveTo(30, 26, 6, 40); q.closePath(); }, '#7a8290');
  g.save(); g.beginPath(); g.moveTo(-34, 30); g.quadraticCurveTo(-30, -6, 0, -30); g.quadraticCurveTo(26, -34, 32, -6); g.quadraticCurveTo(30, 26, 6, 40); g.closePath(); g.clip();
  const gr = g.createLinearGradient(-30, 30, 20, 0); gr.addColorStop(0, '#5fae8a'); gr.addColorStop(1, '#8b6bb8'); g.fillStyle = gr; g.globalAlpha = .65; g.fillRect(-40, 4, 80, 40); g.restore();
  shape(g, q => { q.moveTo(-34, 30); q.quadraticCurveTo(-30, -6, 0, -30); q.quadraticCurveTo(26, -34, 32, -6); q.quadraticCurveTo(30, 26, 6, 40); }, null);
  shape(g, q => { q.moveTo(30, -12); q.lineTo(50, -6); q.lineTo(30, -2); q.closePath(); }, '#3a3a40', 3);
  circ(g, 12, -14, 9, '#f0a050', 3); const bl = p.blink || 0;
  if (bl > .8) line(g, [[6, -14], [18, -14]], OUT, 3); else { g.fillStyle = OUT; g.beginPath(); g.arc(13, -14, 4, 0, 7); g.fill(); }
  g.restore(); g.restore();
}

/* ---------------------------------------------------------------- props */
function propBook(g, x, y, w, h, col, rot = 0) { g.save(); g.translate(x, y); g.rotate(rot); shape(g, q => rrPath(q, -w / 2, -h / 2, w, h, 4), col, 4); g.fillStyle = '#f4f1ea'; g.fillRect(w / 2 - 10, -h / 2 + 4, 6, h - 8); g.restore(); }
function propPaper(g, x, y, rot = 0, s = 1) { g.save(); g.translate(x, y); g.rotate(rot); g.scale(s, s); shape(g, q => q.rect(-36, -48, 72, 96), '#fbfaf6', 3); g.strokeStyle = '#9fb4d6'; g.lineWidth = 3; for (let i = 0; i < 6; i++) { g.beginPath(); g.moveTo(-26, -30 + i * 14); g.lineTo(26, -30 + i * 14); g.stroke(); } g.restore(); }
function propBall(g, x, y, r, rot = 0) { g.save(); g.translate(x, y); g.rotate(rot); circ(g, 0, 0, r, '#ffffff'); g.fillStyle = OUT;
  const pent = (cx, cy, k) => { g.beginPath(); for (let i = 0; i < 5; i++) { const a = -Math.PI / 2 + i * 2 * Math.PI / 5; g.lineTo(cx + Math.cos(a) * k, cy + Math.sin(a) * k); } g.closePath(); g.fill(); };
  pent(0, 0, r * .3); for (let i = 0; i < 5; i++) { const a = -Math.PI / 2 + i * 2 * Math.PI / 5; g.save(); g.beginPath(); g.arc(0, 0, r - 2, 0, 7); g.clip(); pent(Math.cos(a) * r * .85, Math.sin(a) * r * .85, r * .26); g.restore(); }
  g.strokeStyle = OUT; g.lineWidth = 3; for (let i = 0; i < 5; i++) { const a = -Math.PI / 2 + i * 2 * Math.PI / 5; g.beginPath(); g.moveTo(Math.cos(a) * r * .3, Math.sin(a) * r * .3); g.lineTo(Math.cos(a) * r * .62, Math.sin(a) * r * .62); g.stroke(); }
  g.restore(); }
function propMug(g, x, y, s = 1, col = '#f4f1ea') { g.save(); g.translate(x, y); g.scale(s, s); shape(g, q => rrPath(q, -26, -34, 52, 62, 10), col); g.beginPath(); g.arc(26, -4, 16, -1.4, 1.4); g.lineWidth = 11; g.strokeStyle = OUT; g.stroke(); g.lineWidth = 5; g.strokeStyle = col; g.stroke(); g.restore(); }
function propCoffeePot(g, x, y, s = 1, tilt = 0) { g.save(); g.translate(x, y); g.scale(s, s); g.rotate(tilt);
  shape(g, q => { q.moveTo(-40, -60); q.lineTo(40, -60); q.lineTo(52, 40); q.quadraticCurveTo(0, 56, -52, 40); q.closePath(); }, '#d9dde3');
  g.save(); g.beginPath(); g.moveTo(-46, 0); g.lineTo(46, 0); g.lineTo(52, 40); g.quadraticCurveTo(0, 56, -52, 40); g.closePath(); g.clip(); g.fillStyle = '#5a3420'; g.fillRect(-60, 0, 120, 60); g.restore();
  shape(g, q => { q.moveTo(-40, -60); q.lineTo(40, -60); q.lineTo(52, 40); q.quadraticCurveTo(0, 56, -52, 40); q.closePath(); }, null);
  shape(g, q => rrPath(q, -46, -76, 92, 20, 6), '#2a2a30', 4); shape(g, q => { q.moveTo(-40, -50); q.lineTo(-74, -64); q.lineTo(-66, -48); q.closePath(); }, '#d9dde3', 4);
  g.beginPath(); g.moveTo(40, -40); g.quadraticCurveTo(84, -30, 46, 26); g.lineWidth = 14; g.strokeStyle = OUT; g.stroke(); g.lineWidth = 6; g.strokeStyle = '#2a2a30'; g.stroke();
  g.restore(); }
function propAlarm(g, x, y, s, hh, mm, ring = 0) { g.save(); g.translate(x + (ring ? Math.sin(ring * 90) * 4 : 0), y); g.scale(s, s); g.rotate(ring ? Math.sin(ring * 70) * .06 : 0);
  for (const sx of [-1, 1]) { circ(g, sx * 42, -78, 22, '#d64545'); line(g, [[sx * 34, 40], [sx * 46, 58]], OUT, 8); }
  circ(g, 0, -4, 74, '#d64545'); circ(g, 0, -4, 58, '#fbfaf6', 4);
  g.strokeStyle = OUT; g.lineCap = 'round'; for (let i = 0; i < 12; i++) { const a = i * Math.PI / 6; g.lineWidth = 3; g.beginPath(); g.moveTo(Math.cos(a) * 48, -4 + Math.sin(a) * 48); g.lineTo(Math.cos(a) * 54, -4 + Math.sin(a) * 54); g.stroke(); }
  const am = (mm / 60) * 2 * Math.PI - Math.PI / 2, ah = ((hh % 12) + mm / 60) / 12 * 2 * Math.PI - Math.PI / 2;
  g.lineWidth = 6; g.beginPath(); g.moveTo(0, -4); g.lineTo(Math.cos(ah) * 30, -4 + Math.sin(ah) * 30); g.stroke();
  g.lineWidth = 4; g.beginPath(); g.moveTo(0, -4); g.lineTo(Math.cos(am) * 44, -4 + Math.sin(am) * 44); g.stroke();
  g.fillStyle = OUT; g.beginPath(); g.arc(0, -4, 6, 0, 7); g.fill();
  if (ring) { g.strokeStyle = OUT; g.lineWidth = 6; for (const sx of [-1, 1]) for (const k of [1, 2]) { g.beginPath(); g.arc(sx * 42, -78, 30 + k * 16, sx > 0 ? -1.2 : Math.PI + .2, sx > 0 ? -.2 : Math.PI + 1.2); g.stroke(); } }
  g.restore(); }
function propPot(g, x, y, s = 1, rot = 0) { g.save(); g.translate(x, y); g.rotate(rot); g.scale(s, s);
  for (const [dx, dy, r, c] of [[-26, -70, 30, '#4d8a52'], [22, -82, 34, '#5a9a5c'], [0, -104, 30, '#4d8a52'], [-6, -66, 22, '#e86a8a']]) circ(g, dx, dy, r, c, 4);
  shape(g, q => { q.moveTo(-52, -50); q.lineTo(52, -50); q.lineTo(40, 30); q.lineTo(-40, 30); q.closePath(); }, '#c8643e'); shape(g, q => rrPath(q, -58, -62, 116, 22, 5), '#d9774f', 4); g.restore(); }
function propCake(g, x, y, s, flames = 1, t = 0, lit = true) { g.save(); g.translate(x, y); g.scale(s, s);
  shape(g, q => q.ellipse(0, 6, 150, 26, 0, 0, 7), '#e8e4f0', 4);
  shape(g, q => { q.rect(-120, -110, 240, 110); }, '#f6c6d4'); shape(g, q => q.ellipse(0, -110, 120, 24, 0, 0, 7), '#fbe2ea', 4);
  g.fillStyle = '#ffffff'; for (let i = 0; i < 9; i++) { g.beginPath(); g.arc(-108 + i * 27, -96, 12, 0, Math.PI); g.fill(); }
  shape(g, q => { q.rect(-120, -110, 240, 110); }, null, 4);
  for (let i = 0; i < 5; i++) { const cx = -60 + i * 30; shape(g, q => rrPath(q, cx - 6, -170, 12, 56, 4), ['#6fb3e0', '#f0d06a', '#9c6fcf', '#5aa37a', '#e07a8a'][i], 3);
    if (lit) { const f = flames, wob = Math.sin(t * 18 + i) * 3 * (f > 0 ? 1 : 0); shape(g, q => { q.moveTo(cx, -200 + wob); q.quadraticCurveTo(cx + 12, -182, cx, -172); q.quadraticCurveTo(cx - 12, -182, cx, -200 + wob); }, '#ffb339', 3); } }
  g.restore(); }
function propPhone(g, x, y, s, pct = 3, rot = 0) { g.save(); g.translate(x, y); g.rotate(rot); g.scale(s, s); shape(g, q => rrPath(q, -40, -76, 80, 152, 14), '#26262e'); shape(g, q => rrPath(q, -32, -64, 64, 124, 6), '#3e4a5c', 3);
  shape(g, q => rrPath(q, -18, -16, 32, 18, 3), null, 4); g.fillStyle = '#e25555'; g.fillRect(-15, -13, 26 * pct / 100 + 2, 12); g.fillStyle = OUT; g.fillRect(14, -11, 5, 8);
  text(g, pct + '%', 0, 30, 26, '#ffffff', 'Bangers', 'center'); g.restore(); }
function bigCounter(g, label, value, a, x = 70, y = 70) { if (a <= 0) return; g.save(); g.globalAlpha = clamp(a); g.font = '64px Bangers'; const s1 = label + ' ', w1 = g.measureText(s1).width; g.font = '84px Bangers'; const w2 = g.measureText(value).width;
  const s = .9 + .1 * back(a); g.translate(x, y); g.scale(s, s); shape(g, q => rrPath(q, 0, 0, w1 + w2 + 64, 112, 10), '#fde047', 6);
  text(g, s1, 30, 80, 64, '#141014'); text(g, value, 30 + w1, 84, 84, '#c0262d'); g.restore(); }
function sticker(g, s, a, x = 70, y = 70, size = 68, bg = '#fde047', fg = '#141014') { if (a <= 0) return; g.save(); g.globalAlpha = clamp(a); g.font = `${size}px Bangers`; const w = g.measureText(s).width, sc = .9 + .1 * back(a);
  g.translate(x, y); g.scale(sc, sc); shape(g, q => rrPath(q, 0, 0, w + 56, size * 1.45, 10), bg, 6); text(g, s, 28, size * 1.1, size, fg); g.restore(); }
/* full-screen rule card over a dimmed frame */
function ruleCard(g, n, l1, l2, a) { if (a <= 0) return; g.save(); g.globalAlpha = clamp(a) * .55; g.fillStyle = '#0d0b12'; g.fillRect(0, 0, W, H); g.globalAlpha = clamp(a);
  const s = .85 + .15 * back(a); g.translate(W / 2, H / 2); g.scale(s, s); g.rotate(-.02);
  shape(g, q => rrPath(q, -700, -260, 1400, 520, 22), '#fde047', 8);
  text(g, 'REGLA #' + n, 0, -120, 120, '#c0262d', 'Bangers', 'center');
  text(g, l1, 0, 20, 88, '#141014', 'Bangers', 'center'); if (l2) text(g, l2, 0, 140, 88, '#141014', 'Bangers', 'center');
  g.restore(); }
function titleCard(g, l1, l2, a, t) { if (a <= 0) return; g.save(); g.globalAlpha = clamp(a); const s = .8 + .2 * back(a); g.translate(W / 2, H / 2); g.scale(s, s);
  g.rotate(-.025); text(g, l1, 0, -40, 150, '#fde047', 'Bangers', 'center', '#141014', 22); text(g, l2, 0, 130, 150, '#ffffff', 'Bangers', 'center', '#141014', 22); g.restore(); }
function zzz(g, x, y, t, a = 1) { if (a <= 0) return; g.save(); g.globalAlpha = a; for (let i = 0; i < 3; i++) { const u = ((t * .6 + i / 3) % 1); g.globalAlpha = a * Math.sin(u * Math.PI); text(g, 'Z', x + u * 60 + i * 10, y - u * 120, 40 + i * 14, '#ffffff', 'Bangers', 'left', OUT, 7); } g.restore(); }
function speedLines(g, cx, cy, a, t) { if (a <= 0) return; g.save(); g.globalAlpha = a * .5; g.strokeStyle = '#ffffff'; g.lineWidth = 6; const rr = rnd(5);
  for (let i = 0; i < 40; i++) { const ang = rr() * 6.283, r1 = 500 + rr() * 200 + ((t * 600) % 80); g.beginPath(); g.moveTo(cx + Math.cos(ang) * r1, cy + Math.sin(ang) * r1); g.lineTo(cx + Math.cos(ang) * (r1 + 400), cy + Math.sin(ang) * (r1 + 400)); g.stroke(); } g.restore(); }

/* ---------------------------------------------------------------- layers, camera and the time-stop look */
const LAY = {};
/* a cleared layer always gets one all-but-transparent pixel: a layer that stays empty after clearRect can otherwise be read by
   drawImage() as an old recycled frame on long renders (see invis.js) */
function layer(name) { if (!LAY[name]) { const c = document.createElement('canvas'); c.width = W; c.height = H; LAY[name] = c; } const g = LAY[name].getContext('2d'); g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, W, H);
  g.save(); g.fillStyle = 'rgba(0,0,0,0.004)'; g.fillRect(0, 0, 1, 1); g.restore(); return g; }
/* shot: {cx,cy,z} world point at screen center, zoom; shake optional */
function camApply(g, cam) { const z = cam.z || 1; g.setTransform(z, 0, 0, z, W / 2 - cam.cx * z + (cam.sx || 0), H / 2 - cam.cy * z + (cam.sy || 0)); }
function worldToScreen(cam, x, y) { const z = cam.z || 1; return [W / 2 + (x - cam.cx) * z + (cam.sx || 0), H / 2 + (y - cam.cy) * z + (cam.sy || 0)]; }
/* compose: world layer (turns gray-blue by `frz` 0..1, with a radial wipe from (wx,wy) when `wipe` in 0..1),
   then the color layer on top (characters that keep moving while time is stopped). */
const FROZEN_FILTER = 'grayscale(1) brightness(1.06) contrast(.88)';
function compose(X, world, color, frz) {
  X.setTransform(1, 0, 0, 1, 0, 0); X.fillStyle = '#000'; X.fillRect(0, 0, W, H);
  const f = frz || { amt: 0 };
  const drawGray = () => { X.save(); X.filter = FROZEN_FILTER; X.drawImage(world.canvas, 0, 0); X.restore(); X.save(); X.globalCompositeOperation = 'multiply'; X.fillStyle = 'rgba(170,195,230,1)'; X.fillRect(0, 0, W, H); X.restore();
    X.save(); X.globalCompositeOperation = 'screen'; X.fillStyle = 'rgba(40,55,80,.35)'; X.fillRect(0, 0, W, H); X.restore(); };
  if (f.wipe != null && f.wipe > 0 && f.wipe < 1) {
    const rmax = Math.hypot(W, H), rr = outC(f.wipe) * rmax;
    // going to frozen: gray grows from the clap point; going back: color grows
    if (f.dir > 0) { X.drawImage(world.canvas, 0, 0); X.save(); X.beginPath(); X.arc(f.x, f.y, rr, 0, 7); X.clip(); drawGray(); X.restore(); }
    else { drawGray(); X.save(); X.beginPath(); X.arc(f.x, f.y, rr, 0, 7); X.clip(); X.drawImage(world.canvas, 0, 0); X.restore(); }
    X.save(); X.strokeStyle = 'rgba(255,255,255,.85)'; X.lineWidth = 10 * (1 - f.wipe) + 2; X.beginPath(); X.arc(f.x, f.y, rr, 0, 7); X.stroke(); X.restore();
  } else if (f.amt >= .5) drawGray(); else X.drawImage(world.canvas, 0, 0);
  if (color) X.drawImage(color.canvas, 0, 0);
}
/* frozen-state helper: list of clap events [{t, x, y}] toggling the state (first stops time).
   returns {amt, wipe, dir, x, y, since} for time t */
const EVENTS = {};
function freezeState(t, claps, cam, start = 0) {
  if (typeof SID !== 'undefined' && !(typeof FLASH !== 'undefined' && FLASH)) EVENTS[SID] = { claps: claps.map(c => c.t), start };
  let state = start, last = null;
  for (const c of claps) if (t >= c.t) { state = 1 - state; last = c; }
  if (last && t < last.t + .55) { const [sx, sy] = last.screen ? [last.x, last.y] : worldToScreen(cam, last.x, last.y); return { amt: state, wipe: (t - last.t) / .55, dir: state ? 1 : -1, x: sx, y: sy, since: t - last.t }; }
  return { amt: state, since: last ? t - last.t : 1e9 };
}

/* ---------------------------------------------------------------- masked compositing
   A: the full scene in color, drawn in painter's order.
   M: mask of things that keep their color while time is stopped (drawn with `col`);
      world things drawn after them erase the mask (`wld`), so occlusion stays correct.
   Final frame: gray(A) with the masked color on top, or plain A while the world runs. */
function stage(cam) { window.__camz = cam.z || 1; const A = layer('A'), M = layer('M'); camApply(A, cam); camApply(M, cam);
  return { A, M, cam,
    wld(fn) { fn(A); M.save(); M.globalCompositeOperation = 'destination-out'; fn(M); M.restore(); },
    col(fn) { fn(A); fn(M); } }; }
function drawGrayOf(X, A) { X.save(); X.filter = FROZEN_FILTER; X.drawImage(A.canvas, 0, 0); X.restore();
  X.save(); X.globalCompositeOperation = 'multiply'; X.fillStyle = 'rgba(170,195,230,1)'; X.fillRect(0, 0, W, H); X.restore();
  X.save(); X.globalCompositeOperation = 'screen'; X.fillStyle = 'rgba(40,55,80,.35)'; X.fillRect(0, 0, W, H); X.restore(); }
let VIG = null;
function compose2(X, st, f) {
  window.__frz = (f && f.amt >= .5) ? 1 : 0;
  const A = st.A, M = st.M; X.setTransform(1, 0, 0, 1, 0, 0); X.filter = 'none'; X.globalAlpha = 1;
  const K = layer('K'); K.drawImage(A.canvas, 0, 0); K.globalCompositeOperation = 'destination-in'; K.drawImage(M.canvas, 0, 0); K.globalCompositeOperation = 'source-over';
  const gray = () => { drawGrayOf(X, A); X.drawImage(K.canvas, 0, 0); }, color = () => X.drawImage(A.canvas, 0, 0);
  f = f || { amt: 0 };
  if (f.wipe != null && f.wipe > 0 && f.wipe < 1) {
    const rr = outC(f.wipe) * Math.hypot(W, H) * 1.05;
    if (f.dir > 0) { color(); X.save(); X.beginPath(); X.arc(f.x, f.y, rr, 0, 7); X.clip(); gray(); X.restore(); }
    else { gray(); X.save(); X.beginPath(); X.arc(f.x, f.y, rr, 0, 7); X.clip(); color(); X.restore(); }
    X.save(); X.strokeStyle = 'rgba(255,255,255,.9)'; X.lineWidth = 12 * (1 - f.wipe) + 2; X.beginPath(); X.arc(f.x, f.y, rr, 0, 7); X.stroke(); X.restore();
  } else if (f.amt >= .5) gray(); else color();
  // colour grade per location and a soft vignette: the light that flat fills lack
  if (CUR_LOOK.grade && !(f.amt >= .5 && !(f.wipe > 0 && f.wipe < 1))) { X.save(); X.globalCompositeOperation = 'multiply'; X.fillStyle = CUR_LOOK.grade; X.fillRect(0, 0, W, H); X.restore(); }
  if (!VIG) { VIG = document.createElement('canvas'); VIG.width = W; VIG.height = H; const v = VIG.getContext('2d'), gr = v.createRadialGradient(W / 2, H * .46, H * .35, W / 2, H / 2, H * 1.05);
    gr.addColorStop(0, 'rgba(10,6,20,0)'); gr.addColorStop(1, 'rgba(10,6,20,.42)'); v.fillStyle = gr; v.fillRect(0, 0, W, H); }
  X.drawImage(VIG, 0, 0);
  window.__cam = st.cam;
  if (f.wipe != null && f.wipe > 0 && f.wipe < 1 && !(typeof FLASH !== 'undefined' && FLASH)) comicWord(X, '¡CLAP!', f.x + 40, f.y - 170, f.wipe * .55, 84, '#fde047', .55);
}
/* world clock: advances only while the world runs (claps toggle; start=1 means frozen at t=0) */
function worldClock(t, claps, start = 0) { let state = start, last = 0, acc = 0;
  for (const c of claps) { if (c.t > t) break; if (state === 0) acc += c.t - last; last = c.t; state = 1 - state; }
  if (state === 0) acc += t - last; return acc; }
function isFrozen(t, claps, start = 0) { let s = start; for (const c of claps) if (t >= c.t) s = 1 - s; return s === 1; }
/* world-space point between the hands at chest height, for the clap ripple */
function clapPoint(cname, p) { const c = CAST[cname], G = charGeom(c, p), S = (p.s || 1) * (c.s || 1); return [p.x, p.y + S * (G.top + 150)]; }
function dropsSpray(g, x, y, n, seed, s = 1) { const r = rnd(seed); for (let i = 0; i < n; i++) { const a = Math.PI * (.85 + r() * .35), d = 30 + r() * 120 * s; circ(g, x + Math.cos(a) * d, y + Math.sin(a) * d * .5 + r() * 20, 4 + r() * 5, '#bfe6ff', 3); } }

/* comic sound word: pops in with overshoot, wobbles, fades; u = seconds since it appeared */
function comicWord(g, word, x, y, u, size = 96, col = '#fde047', dur = .75) {
  if (u < 0 || u > dur) return; const k = back(clamp(u / .18)), a = 1 - clamp((u - dur + .18) / .18);
  g.save(); g.globalAlpha = a; g.translate(x, y); g.rotate(-.12 + Math.sin(u * 30) * .03 * (1 - clamp(u / .4))); g.scale(k, k);
  g.font = `${size}px Bangers`; g.textAlign = 'center'; const w = g.measureText(word).width;
  g.beginPath(); for (let i = 0; i < 22; i++) { const ang = i / 22 * Math.PI * 2, r = (i % 2 ? .42 : .62) * (w + 60); g.lineTo(Math.cos(ang) * r, Math.sin(ang) * r * .55); } g.closePath();
  g.fillStyle = '#ffffff'; g.fill(); g.lineWidth = 5; g.strokeStyle = OUT; g.stroke();
  g.lineJoin = 'round'; g.strokeStyle = OUT; g.lineWidth = size * .18; g.strokeText(word, 0, size * .35); g.fillStyle = col; g.fillText(word, 0, size * .35);
  g.restore(); }
