/* Ep05 look: "genius mode" (500 IQ).
   While the hero thinks, the world turns into a blueprint: deep blue paper, the drawing's edges in pale cyan-white, a fine grid
   pinned to the world. The hero keeps his colour (st.col, as in the frozen-time look) with a soft white rim. White chalk notes then
   draw themselves on top: arrows, trajectories, dimension lines, boxes and labels with numbers. A badge in the corner: IQ 500.

   const st = stage(cam); st.wld(g => drawSet(g, 'street')); st.col(g => drawChar(g, 'tu', hp));
   const gm = geniusState(t, [[t0, t1], ...], cam, [wx, wy]);   // windows of thinking; the switch wipes out from (wx, wy)
   composeG(X, st, gm);
   chalk(X, cam, t, gm.a, [{ k: 'arrow', a: [x, y], b: [x, y], t0 }, { k: 'label', at: [x, y], s: '4,3 kg', t0 }, ...]);
   iqBadge(X, a, t, busy);  smoke(X, x, y, t, a);  storm(X, x, y, t, t0, a, items)                                         */
const GEN_PAPER = '#123a6e', GEN_INK = '#eaf6ff', GEN_GLOW = 'rgba(120,205,255,.9)', GEN_RED = '#ff8f9a', GEN_YEL = '#ffe27a';

/* edge filter for the blueprint (Laplacian of a slightly blurred grey copy, boosted); referenced as ctx.filter = 'url(#gEdge)' */
(function () { if (typeof document === 'undefined' || document.getElementById('gEdgeSvg')) return;
  const s = '<svg id="gEdgeSvg" width="0" height="0" style="position:absolute"><filter id="gEdge" color-interpolation-filters="sRGB">' +
    '<feColorMatrix type="saturate" values="0"/><feGaussianBlur stdDeviation="0.7"/>' +
    '<feConvolveMatrix order="3" kernelMatrix="-1 -1 -1 -1 8 -1 -1 -1 -1" preserveAlpha="true"/>' +
    '<feComponentTransfer><feFuncR type="linear" slope="4.2" intercept="-0.06"/><feFuncG type="linear" slope="4.2" intercept="-0.06"/><feFuncB type="linear" slope="4.2" intercept="-0.06"/></feComponentTransfer>' +
    '</filter></svg>';
  (document.body || document.documentElement).insertAdjacentHTML('beforeend', s); })();

/* windows of thinking -> state for composeG/chalk. a: smooth 0..1 for overlays; amt: 0/1; wipe while switching */
function geniusState(t, wins, cam, at, dur = .45) {
  let amt = 0, ev = null, a = 0;
  for (const [t0, t1] of wins) {
    if (t >= t0 && t < t1) amt = 1;
    a = Math.max(a, R(t, t0, t0 + dur, lin) * (1 - R(t, t1, t1 + .3, lin)));
    if (t >= t0 && t < t0 + dur) ev = { t0, dir: 1 }; else if (t >= t1 && t < t1 + dur) ev = { t0: t1, dir: -1 };
  }
  const [x, y] = at ? worldToScreen(cam, at[0], at[1]) : [W / 2, H / 2];
  window.__gen = amt;
  return ev ? { amt, a, wipe: (t - ev.t0) / dur, dir: ev.dir, x, y } : { amt, a, x, y };
}

/* the world layer as a blueprint, into X */
let GEN_E = null;
function blueprintOf(X, A, cam) {
  X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.filter = 'none'; X.globalAlpha = 1; X.globalCompositeOperation = 'source-over';
  X.fillStyle = GEN_PAPER; X.fillRect(0, 0, W, H);
  // shading: the inverted grey drawing, crushed, so big shapes still read as faint lighter-blue masses
  X.globalCompositeOperation = 'screen'; X.globalAlpha = .55; X.filter = 'grayscale(1) invert(1) contrast(2.4) brightness(.45)'; X.drawImage(A.canvas, 0, 0);
  // edges at half size (cheap, and soft like chalk), scaled back up
  if (!GEN_E) { GEN_E = document.createElement('canvas'); GEN_E.width = W / 2; GEN_E.height = H / 2; }
  const E = GEN_E.getContext('2d'); GEN_E.width = GEN_E.width; E.filter = 'url(#gEdge)'; E.drawImage(A.canvas, 0, 0, W / 2, H / 2); E.filter = 'none';
  E.globalCompositeOperation = 'multiply'; E.fillStyle = '#cfeaff'; E.fillRect(0, 0, W / 2, H / 2);
  X.filter = 'none'; X.globalAlpha = 1; X.imageSmoothingEnabled = true; X.drawImage(GEN_E, 0, 0, W, H);
  X.globalCompositeOperation = 'source-over';
  // grid pinned to the world
  const z = cam.z || 1, x0 = cam.cx - W / 2 / z, y0 = cam.cy - H / 2 / z, step = 40;
  for (let pass = 0; pass < 2; pass++) {
    X.beginPath(); X.lineWidth = pass ? 1.6 : 1; X.strokeStyle = pass ? 'rgba(200,232,255,.20)' : 'rgba(200,232,255,.08)';
    for (let gx = Math.floor(x0 / step) * step; gx < x0 + W / z + step; gx += step) { if ((Math.round(gx / step) % 5 === 0) !== !!pass) continue; const sx = (gx - x0) * z; X.moveTo(sx, 0); X.lineTo(sx, H); }
    for (let gy = Math.floor(y0 / step) * step; gy < y0 + H / z + step; gy += step) { if ((Math.round(gy / step) % 5 === 0) !== !!pass) continue; const sy = (gy - y0) * z; X.moveTo(0, sy); X.lineTo(W, sy); }
    X.stroke(); }
  X.restore();
}

/* compose: world (colour or blueprint, with a radial wipe while switching), then the hero in colour with a white rim */
function composeG(X, st, f = { amt: 0 }) {
  const A = st.A, M = st.M; X.setTransform(1, 0, 0, 1, 0, 0); X.filter = 'none'; X.globalAlpha = 1; X.globalCompositeOperation = 'source-over';
  const K = layer('K'); K.drawImage(A.canvas, 0, 0); K.globalCompositeOperation = 'destination-in'; K.drawImage(M.canvas, 0, 0); K.globalCompositeOperation = 'source-over';
  const blue = () => { blueprintOf(X, A, st.cam); X.save(); X.shadowColor = 'rgba(235,250,255,.85)'; X.shadowBlur = 16; X.drawImage(K.canvas, 0, 0); X.restore(); },
    color = () => X.drawImage(A.canvas, 0, 0);
  if (f.wipe != null && f.wipe > 0 && f.wipe < 1) {
    const rr = outC(f.wipe) * Math.hypot(W, H) * 1.05;
    if (f.dir > 0) { color(); X.save(); X.beginPath(); X.arc(f.x, f.y, rr, 0, 7); X.clip(); blue(); X.restore(); }
    else { blue(); X.save(); X.beginPath(); X.arc(f.x, f.y, rr, 0, 7); X.clip(); color(); X.restore(); }
    X.save(); X.strokeStyle = 'rgba(235,250,255,.95)'; X.lineWidth = 10 * (1 - f.wipe) + 2; X.shadowColor = GEN_GLOW; X.shadowBlur = 24;
    X.beginPath(); X.arc(f.x, f.y, rr, 0, 7); X.stroke(); X.restore();
  } else if (f.amt >= .5) blue(); else color();
  if (CUR_LOOK.grade && !(f.amt >= .5 && !(f.wipe > 0 && f.wipe < 1))) { X.save(); X.globalCompositeOperation = 'multiply'; X.fillStyle = CUR_LOOK.grade; X.fillRect(0, 0, W, H); X.restore(); }
  if (!VIG) { VIG = document.createElement('canvas'); VIG.width = W; VIG.height = H; const v = VIG.getContext('2d'), gr = v.createRadialGradient(W / 2, H * .46, H * .35, W / 2, H / 2, H * 1.05);
    gr.addColorStop(0, 'rgba(10,6,20,0)'); gr.addColorStop(1, 'rgba(10,6,20,.42)'); v.fillStyle = gr; v.fillRect(0, 0, W, H); }
  X.drawImage(VIG, 0, 0);
  window.__cam = st.cam;
}

/* ---------------------------------------------------------------- chalk notes
   every note: k (kind), t0 (start), d (draw time, default .45), out (optional end time), col, lw (line width), scr: 1 for screen coords.
   kinds: arrow {a, b, head}, line {a, b}, arc {a, b, h, mark}, circle {at, r, ry}, box {at, w, h, s}, dim {a, b, s}, label {at, s, size, align},
          x {at, r}, tick {at, r}, poly {pts}                                                                               */
const chalkRnd = (i, k) => { const v = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return v - Math.floor(v); };
function chalkPath(X, pts, u, seed, jit = 2.2) {
  if (u <= 0 || pts.length < 2) return null;
  let L = 0; const seg = []; for (let i = 1; i < pts.length; i++) { const d = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); seg.push(d); L += d; }
  let left = clamp(u) * L; X.beginPath(); X.moveTo(pts[0][0], pts[0][1]); let last = pts[0];
  for (let i = 1; i < pts.length && left > 0; i++) {
    const d = seg[i - 1], k = Math.min(1, left / Math.max(d, 1e-6)), p = [mix(pts[i - 1][0], pts[i][0], k), mix(pts[i - 1][1], pts[i][1], k)];
    const nx = -(pts[i][1] - pts[i - 1][1]) / (d || 1), ny = (pts[i][0] - pts[i - 1][0]) / (d || 1), j = (chalkRnd(i, seed) - .5) * jit;
    X.lineTo(p[0] + nx * j, p[1] + ny * j); left -= d; last = p; }
  X.stroke(); return last; }
function chalkHead(X, a, b, size = 22) { const ang = Math.atan2(b[1] - a[1], b[0] - a[0]);
  X.beginPath(); X.moveTo(b[0] - Math.cos(ang - .45) * size, b[1] - Math.sin(ang - .45) * size); X.lineTo(b[0], b[1]); X.lineTo(b[0] - Math.cos(ang + .45) * size, b[1] - Math.sin(ang + .45) * size); X.stroke(); }
function chalkText(X, s, x, y, u, size = 44, align = 'left', col = GEN_INK) {
  const n = Math.round(clamp(u) * s.length); if (n <= 0) return; X.font = `bold ${size}px ComicNeue`; X.textAlign = align; X.fillStyle = col;
  X.lineWidth = Math.max(4, size * .14); X.strokeStyle = 'rgba(8,24,52,.75)'; X.strokeText(s.slice(0, n), x, y); X.fillText(s.slice(0, n), x, y); }
function chalk(X, cam, t, a, notes) {
  if (a <= 0) return;
  X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.lineCap = 'round'; X.lineJoin = 'round';
  const P = (n, p) => n.scr ? p : worldToScreen(cam, p[0], p[1]);
  notes.forEach((n, idx) => {
    if (t < n.t0 || (n.out != null && t > n.out + .25)) return;
    const d = n.d || .45, u = clamp((t - n.t0) / d), fade = n.out != null ? 1 - R(t, n.out, n.out + .25, lin) : 1, col = n.col || GEN_INK;
    X.globalAlpha = clamp(a) * fade; X.strokeStyle = col; X.fillStyle = col; X.lineWidth = n.lw || 5; X.shadowColor = n.col === GEN_RED ? 'rgba(255,120,130,.8)' : GEN_GLOW; X.shadowBlur = 12;
    if (n.dash) X.setLineDash([16, 12]); else X.setLineDash([]);
    const seed = idx + 1 + Math.floor(t * 8) * .37;   // chalk lines "boil" a little, 8 times a second
    if (n.k === 'arrow' || n.k === 'line') { const a2 = P(n, n.a), b2 = P(n, n.b), e = chalkPath(X, [a2, mix2(a2, b2, .5), b2], u, seed); if (n.k === 'arrow' && u > .8 && e) { X.setLineDash([]); chalkHead(X, a2, b2, n.hs || 22); } }
    else if (n.k === 'poly') chalkPath(X, n.pts.map(p => P(n, p)), u, seed);
    else if (n.k === 'arc') { const a2 = n.a, b2 = n.b, pts = []; for (let i = 0; i <= 28; i++) { const s = i / 28; pts.push(P(n, [mix(a2[0], b2[0], s), mix(a2[1], b2[1], s) - 4 * n.h * s * (1 - s)])); }
      chalkPath(X, pts, u, seed, 1.5); if (n.mark && u >= 1) { X.setLineDash([]); const e = pts[pts.length - 1], r = 16; X.beginPath(); X.moveTo(e[0] - r, e[1] - r); X.lineTo(e[0] + r, e[1] + r); X.moveTo(e[0] + r, e[1] - r); X.lineTo(e[0] - r, e[1] + r); X.stroke(); } }
    else if (n.k === 'circle') { const c = P(n, n.at), z = n.scr ? 1 : cam.z, rx = n.r * z, ry = (n.ry || n.r) * z, pts = []; for (let i = 0; i <= 40; i++) { const an = -2.2 + i / 40 * (Math.PI * 2 + .5); pts.push([c[0] + Math.cos(an) * rx * (1 + .04 * Math.sin(i)), c[1] + Math.sin(an) * ry]); } chalkPath(X, pts, u, seed, 2.5); }
    else if (n.k === 'box') { const c = P(n, n.at), z = n.scr ? 1 : cam.z, w = n.w * z / 2, h = n.h * z / 2, L = Math.min(w, h) * .45, pr = clamp(u * 1.3);
      for (const [sx, sy] of [[-1, -1], [1, -1], [1, 1], [-1, 1]]) chalkPath(X, [[c[0] + sx * w, c[1] + sy * (h - L)], [c[0] + sx * w, c[1] + sy * h], [c[0] + sx * (w - L), c[1] + sy * h]], pr, seed, 1);
      if (n.s) chalkText(X, n.s, c[0] - w, c[1] - h - 14, clamp((t - n.t0 - d * .5) / .5), n.size || 38, 'left', col); }
    else if (n.k === 'dim') { const a2 = P(n, n.a), b2 = P(n, n.b), ang = Math.atan2(b2[1] - a2[1], b2[0] - a2[0]), nx = -Math.sin(ang) * 14, ny = Math.cos(ang) * 14;
      chalkPath(X, [[a2[0] + nx, a2[1] + ny], [a2[0] - nx, a2[1] - ny]], u * 3, seed, 0); chalkPath(X, [a2, b2], u, seed, 1.2); if (u > .7) chalkPath(X, [[b2[0] + nx, b2[1] + ny], [b2[0] - nx, b2[1] - ny]], (u - .7) * 3.3, seed, 0);
      if (n.s) { const m = mix2(a2, b2, .5); chalkText(X, n.s, m[0] + (n.ox || 0), m[1] - 18 + (n.oy || 0), clamp((u - .4) * 1.7), n.size || 38, 'center', col); } }
    else if (n.k === 'label') { const c = P(n, n.at);
      if (n.bg !== 0 && u > 0) { const sz = n.size || 44; X.save(); X.shadowBlur = 0; X.font = `bold ${sz}px ComicNeue`; const wd = X.measureText(n.s).width, x0 = n.align === 'center' ? c[0] - wd / 2 : n.align === 'right' ? c[0] - wd : c[0];
        X.globalAlpha *= clamp(u * 3); X.fillStyle = 'rgba(8,24,52,.58)'; X.beginPath(); rrPath(X, x0 - 12, c[1] - sz * .9, wd + 24, sz * 1.22, 10); X.fill(); X.restore(); }
      chalkText(X, n.s, c[0], c[1], u, n.size || 44, n.align || 'left', col); if (n.under && u >= 1) { X.font = `bold ${n.size || 44}px ComicNeue`; const wd = X.measureText(n.s).width, x0 = n.align === 'center' ? c[0] - wd / 2 : c[0]; chalkPath(X, [[x0, c[1] + 12], [x0 + wd, c[1] + 10]], 1, seed, 1); } }
    else if (n.k === 'x') { const c = P(n, n.at), r = (n.r || 18); chalkPath(X, [[c[0] - r, c[1] - r], [c[0] + r, c[1] + r]], u * 2, seed, 0); if (u > .5) chalkPath(X, [[c[0] + r, c[1] - r], [c[0] - r, c[1] + r]], (u - .5) * 2, seed + 1, 0); }
    else if (n.k === 'tick') { const c = P(n, n.at), r = n.r || 24; chalkPath(X, [[c[0] - r, c[1]], [c[0] - r * .3, c[1] + r * .7], [c[0] + r, c[1] - r * .9]], u, seed, 0); }
  });
  X.restore();
}

/* ---------------------------------------------------------------- the IQ 500 badge, top right (busy: a spinner while it computes) */
function brainIcon(g, x, y, s, col = '#ff9ec4', ink = '#3a1530') {
  g.save(); g.translate(x, y); g.scale(s, s); g.lineJoin = 'round'; g.lineCap = 'round';
  const lobe = (sx) => { g.beginPath(); g.moveTo(0, -46); g.bezierCurveTo(sx * 30, -66, sx * 70, -52, sx * 66, -20); g.bezierCurveTo(sx * 84, -6, sx * 78, 34, sx * 52, 40);
    g.bezierCurveTo(sx * 40, 58, sx * 10, 56, 0, 44); g.closePath(); g.fillStyle = col; g.fill(); g.lineWidth = 6; g.strokeStyle = ink; g.stroke(); };
  lobe(-1); lobe(1);
  g.lineWidth = 4.5; g.strokeStyle = ink; g.beginPath(); g.moveTo(0, -44); g.lineTo(0, 44);
  for (const sx of [-1, 1]) { g.moveTo(sx * 18, -30); g.quadraticCurveTo(sx * 40, -36, sx * 46, -14); g.moveTo(sx * 14, 2); g.quadraticCurveTo(sx * 36, -6, sx * 54, 14); g.moveTo(sx * 20, 26); g.quadraticCurveTo(sx * 30, 36, sx * 44, 30); }
  g.stroke(); g.restore(); }
function iqBadge(X, a, t, busy = 0, x = W - 150, y = 150, r = 86) {
  if (a <= 0) return; X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.globalAlpha = clamp(a);
  X.fillStyle = 'rgba(8,22,48,.62)'; X.beginPath(); X.arc(x, y, r + 16, 0, 7); X.fill();
  X.lineWidth = 12; X.strokeStyle = 'rgba(234,246,255,.22)'; X.beginPath(); X.arc(x, y, r, 0, 7); X.stroke();
  X.shadowColor = GEN_GLOW; X.shadowBlur = 22; X.strokeStyle = GEN_INK; X.lineCap = 'round';
  if (busy > 0) { const s0 = t * 6; X.globalAlpha = clamp(a) * clamp(busy); X.beginPath(); X.arc(x, y, r, s0, s0 + 1.6); X.stroke(); X.beginPath(); X.arc(x, y, r, s0 + Math.PI, s0 + Math.PI + 1.6); X.stroke(); X.globalAlpha = clamp(a); }
  else { X.beginPath(); X.arc(x, y, r, 0, 7); X.stroke(); }
  X.shadowBlur = 0; brainIcon(X, x, y - 8, .78 + .04 * Math.sin(t * 3) * clamp(busy));
  X.font = '40px Bangers'; X.textAlign = 'center'; X.fillStyle = GEN_YEL; X.shadowColor = '#000'; X.shadowBlur = 0; X.lineWidth = 7; X.strokeStyle = '#0d0b12';
  X.strokeText('IQ 500', x, y + r + 50); X.fillText('IQ 500', x, y + r + 50);
  X.restore(); }

/* a light bulb that pops over the head (screen point), u: 0..1 pop */
function bulb(X, x, y, u, s = 1) { if (u <= 0) return; const k = back(clamp(u * 1.4)) * s; X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.translate(x, y); X.scale(k, k);
  X.shadowColor = '#ffe27a'; X.shadowBlur = 50; shape(X, q => { q.arc(0, -14, 44, Math.PI * .8, Math.PI * 2.2); q.lineTo(18, 30); q.lineTo(-18, 30); q.closePath(); }, '#ffe27a', 6); X.shadowBlur = 0;
  shape(X, q => rrPath(q, -20, 30, 40, 26, 5), '#a8b0bc', 5); line(X, [[-12, 4], [-4, -14], [4, 4], [12, -14]], '#c98a1a', 4);
  X.globalAlpha = .9; for (let i = 0; i < 8; i++) { const an = i / 8 * Math.PI * 2 - Math.PI / 2, r0 = 62 + 6 * Math.sin(u * 20), r1 = r0 + 22; line(X, [[Math.cos(an) * r0, -14 + Math.sin(an) * r0], [Math.cos(an) * r1, -14 + Math.sin(an) * r1]], '#ffe27a', 6); }
  X.restore(); }

/* smoke out of the curls when the brain overheats: puffs rising from (x, y) on screen */
function smoke(X, x, y, t, a, s = 1) { if (a <= 0) return; X.save(); X.setTransform(1, 0, 0, 1, 0, 0);
  for (let i = 0; i < 7; i++) { const u = ((t * .7 + i / 7) % 1), px = x + Math.sin(t * 1.3 + i * 2.1) * 40 * u * s + (i % 3 - 1) * 30 * s, py = y - u * 230 * s, r = (18 + 46 * u) * s;
    X.globalAlpha = clamp(a) * (1 - u) * .85; shape(X, q => q.arc(px, py, r, 0, 7), '#d9dbe4', 4); X.globalAlpha = clamp(a) * (1 - u) * .5; shape(X, q => q.arc(px - r * .3, py - r * .3, r * .35, 0, 7), '#ffffff', 0); }
  X.restore(); }

/* a storm of scenarios flying out of the head: cards with options, a counter that climbs */
function storm(X, x, y, t, t0, a, items, n0 = 1, n1 = 4000, dur = 4) { if (a <= 0 || t < t0) return; X.save(); X.setTransform(1, 0, 0, 1, 0, 0);
  const k = t - t0;
  for (let i = 0; i < 18; i++) { const u = ((k * .45 + i / 18) % 1), an = (i * 2.399) % (Math.PI * 2), rr = 140 + u * 760, s = items[i % items.length];
    if (k * .45 + i / 18 < 1 && u > k * .45) continue;   // cards come out one after another at the start
    const px = x + Math.cos(an) * rr * 1.25, py = y + Math.sin(an) * rr * .62 - 60;
    X.globalAlpha = clamp(a) * Math.sin(Math.PI * u) * .95; X.font = 'bold 34px ComicNeue'; const w = X.measureText(s).width + 34;
    X.save(); X.translate(px, py); X.rotate((chalkRnd(i, 3) - .5) * .3); X.scale(.6 + .5 * u, .6 + .5 * u);
    shape(X, q => rrPath(q, -w / 2, -30, w, 52, 10), 'rgba(10,30,62,.85)', 3); X.strokeStyle = GEN_INK; X.lineWidth = 2.5; X.strokeRect(-w / 2 + 5, -25, w - 10, 42);
    X.fillStyle = GEN_INK; X.textAlign = 'center'; X.fillText(s, 0, 7); X.restore(); }
  const cnt = Math.round(mix(n0, n1, clamp(k / dur) ** 1.6)).toLocaleString('es-MX');
  X.globalAlpha = clamp(a); X.font = 'bold 46px ComicNeue'; X.textAlign = 'center'; X.lineWidth = 8; X.strokeStyle = 'rgba(8,24,52,.85)'; X.fillStyle = GEN_YEL;
  X.strokeText('ESCENARIOS: ' + cnt, x, y - 300); X.fillText('ESCENARIOS: ' + cnt, x, y - 300);
  X.restore(); }

/* a progress bar «CALCULANDO… n%» at a screen point; stuck: blinks red */
function calcBar(X, x, y, a, pct, stuck = 0, t = 0, label = 'CALCULANDO…') { if (a <= 0) return; X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.globalAlpha = clamp(a);
  const w = 420, h = 34, blink = stuck && Math.sin(t * 9) > 0; shape(X, q => rrPath(q, x - w / 2 - 16, y - 66, w + 32, 116, 16), 'rgba(8,22,48,.82)', 4);
  X.font = 'bold 36px ComicNeue'; X.textAlign = 'center'; X.fillStyle = blink ? GEN_RED : GEN_INK; X.fillText(label + ' ' + Math.round(pct) + '%', x, y - 22);
  X.strokeStyle = GEN_INK; X.lineWidth = 3; X.strokeRect(x - w / 2, y - 4, w, h); X.fillStyle = blink ? GEN_RED : GEN_YEL; X.fillRect(x - w / 2 + 4, y, (w - 8) * clamp(pct / 100), h - 8);
  X.restore(); }
