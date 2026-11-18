/* Ep06 look: the pain signal.
   A hit sends a red glowing pulse along a nerve, from the hit point to the head. For everybody else it arrives: a red ring,
   «¡AY!», and the pain gauge jumps. For the hero (no pain) it fizzles halfway: sparks, a grey ✗, and the gauge stays at 0
   with «SIN SEÑAL» over TV static. During the week the hero collects plasters and a bump on the forehead (hurtMarks).

   nerve(X, cam, pts, t, t0, blocked)       pts: world polyline from the hit point up to the head
   painGauge(X, a, val, t, noSignal)        top-right dial 0..10
   painFlash(X, a)                          red rim for people who do feel it
   hurtMarks(g, cname, p, { bump, cheek, chin, ankle })                                                                    */
const PAIN_RED = '#ff3b3b', PAIN_GLOW = 'rgba(255,70,70,.95)';

function polyLen(sp) { let L = 0; for (let i = 1; i < sp.length; i++) L += Math.hypot(sp[i][0] - sp[i - 1][0], sp[i][1] - sp[i - 1][1]); return L; }
function polyAt(sp, f) { const L = polyLen(sp) * clamp(f); let acc = 0;
  for (let i = 1; i < sp.length; i++) { const d = Math.hypot(sp[i][0] - sp[i - 1][0], sp[i][1] - sp[i - 1][1]); if (acc + d >= L) { const k = (L - acc) / (d || 1); return [mix(sp[i - 1][0], sp[i][0], k), mix(sp[i - 1][1], sp[i][1], k)]; } acc += d; }
  return sp[sp.length - 1]; }
function polyPart(X, sp, f0, f1) { const L = polyLen(sp), a = L * f0, b = L * f1; let acc = 0, started = false; X.beginPath();
  for (let i = 1; i < sp.length; i++) { const d = Math.hypot(sp[i][0] - sp[i - 1][0], sp[i][1] - sp[i - 1][1]);
    const s0 = Math.max(a, acc), s1 = Math.min(b, acc + d);
    if (s1 > s0) { const p0 = mix2(sp[i - 1], sp[i], (s0 - acc) / (d || 1)), p1 = mix2(sp[i - 1], sp[i], (s1 - acc) / (d || 1)); if (!started) { X.moveTo(p0[0], p0[1]); started = true; } X.lineTo(p1[0], p1[1]); }
    acc += d; }
  X.stroke(); }
/* the signal along a nerve: blocked (the hero) stops at `stop` with sparks and a grey ✗; otherwise it reaches the head */
function nerve(X, cam, pts, t, t0, blocked = 1, dur = .55, stop = .55) {
  const u = (t - t0) / dur; if (u < 0 || u > 2.4) return;
  const sp = pts.map(p => worldToScreen(cam, p[0], p[1])), end = blocked ? stop : 1, a = clamp(u * 5) * (1 - R(u, 1.7, 2.4, lin)), z = cam.z || 1;
  X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.lineCap = 'round'; X.lineJoin = 'round';
  // the nerve itself: thin, faint, the whole way (the part past the break goes grey)
  X.globalAlpha = .8 * a; X.lineWidth = 6 * Math.min(1.6, z); X.shadowColor = PAIN_GLOW; X.shadowBlur = 10; X.strokeStyle = 'rgba(255,120,120,.95)'; polyPart(X, sp, 0, end); X.shadowBlur = 0;
  if (blocked) { X.strokeStyle = 'rgba(170,175,190,.9)'; X.lineWidth = 5 * Math.min(1.6, z); X.setLineDash([10, 10]); polyPart(X, sp, end, 1); X.setLineDash([]); }
  // the pulse: a bright head with a short glowing tail
  const h = Math.min(u, end);
  X.globalAlpha = a; X.shadowColor = PAIN_GLOW; X.shadowBlur = 30; X.strokeStyle = PAIN_RED; X.lineWidth = 14 * Math.min(1.6, z); polyPart(X, sp, Math.max(0, h - .22), h);
  const [px, py] = polyAt(sp, h); X.fillStyle = '#fff2f2'; X.beginPath(); X.arc(px, py, 14 * Math.min(1.6, z), 0, 7); X.fill();
  X.shadowBlur = 0;
  if (blocked && u > end) {   // fizzles: sparks, then a grey cross
    const k = clamp((u - end) / .5), r0 = 12 + 50 * k; X.globalAlpha = a * (1 - k * .6); X.strokeStyle = '#ffd34d'; X.lineWidth = 4;
    for (let i = 0; i < 8; i++) { const an = i / 8 * Math.PI * 2 + .3; X.beginPath(); X.moveTo(px + Math.cos(an) * r0 * .4, py + Math.sin(an) * r0 * .4); X.lineTo(px + Math.cos(an) * r0, py + Math.sin(an) * r0); X.stroke(); }
    X.globalAlpha = a * clamp(k * 3); X.strokeStyle = '#8f95a3'; X.lineWidth = 8; const c = 18;
    X.beginPath(); X.moveTo(px - c, py - c); X.lineTo(px + c, py + c); X.moveTo(px + c, py - c); X.lineTo(px - c, py + c); X.stroke(); }
  if (!blocked && u > 1) { const k = clamp((u - 1) / .5), [ex, ey] = sp[sp.length - 1]; X.globalAlpha = a * (1 - k); X.strokeStyle = PAIN_RED; X.lineWidth = 10 * (1 - k) + 2; X.shadowColor = PAIN_GLOW; X.shadowBlur = 20;
    X.beginPath(); X.arc(ex, ey, 30 + 90 * k, 0, 7); X.stroke(); }
  X.restore(); }

/* a red rim on the frame: somebody who does feel it */
function painFlash(X, a) { if (a <= 0) return; X.save(); X.setTransform(1, 0, 0, 1, 0, 0); const gr = X.createRadialGradient(W / 2, H / 2, H * .35, W / 2, H / 2, H * .95);
  gr.addColorStop(0, 'rgba(255,40,40,0)'); gr.addColorStop(1, `rgba(255,40,40,${.45 * clamp(a)})`); X.fillStyle = gr; X.fillRect(0, 0, W, H); X.restore(); }

/* TV static inside a rectangle (screen), seeded per frame */
function tvStatic(X, x, y, w, h, t, a = 1) { if (a <= 0) return; const r = rnd(1 + Math.floor(t * 24) * 7); X.save(); X.globalAlpha = clamp(a);
  for (let i = 0; i < 260; i++) { const v = Math.floor(80 + r() * 175); X.fillStyle = `rgb(${v},${v},${v})`; X.fillRect(x + r() * w, y + r() * h, 3 + r() * 9, 2 + r() * 3); } X.restore(); }

/* the pain gauge, top right: dial 0..10 green→red, needle, «DOLOR»; noSig: needle dead at 0, static and a blinking «SIN SEÑAL» */
function painGauge(X, a, val, t, noSig = 0, x = W - 175, y = 190, r = 115) {
  if (a <= 0) return; X.save(); X.setTransform(1, 0, 0, 1, 0, 0); const s = .85 + .15 * back(clamp(a)); X.globalAlpha = clamp(a); X.translate(x, y); X.scale(s, s);
  shape(X, q => rrPath(q, -r - 34, -r - 28, 2 * r + 68, r + 160, 22), 'rgba(14,12,24,.85)', 4);
  const seg = 10; for (let i = 0; i < seg; i++) { const a0 = Math.PI + i / seg * Math.PI + .02, a1 = Math.PI + (i + 1) / seg * Math.PI - .02, hue = 120 - i * 12;
    X.strokeStyle = `hsl(${hue},80%,55%)`; X.lineWidth = 22; X.beginPath(); X.arc(0, 0, r - 12, a0, a1); X.stroke(); }
  X.fillStyle = '#ffffff'; X.font = '26px Bangers'; X.textAlign = 'center'; X.fillText('0', -r + 12, 26); X.fillText('10', r - 12, 26);
  const v = noSig ? 0 : clamp(val / 10), wob = noSig ? 0 : Math.sin(t * 40) * .03 * clamp(val / 10), an = Math.PI + v * Math.PI + wob;
  X.strokeStyle = '#ffffff'; X.lineWidth = 7; X.lineCap = 'round'; X.beginPath(); X.moveTo(0, 0); X.lineTo(Math.cos(an) * (r - 30), Math.sin(an) * (r - 30)); X.stroke();
  circ(X, 0, 0, 12, '#ffffff', 0);
  if (noSig) { tvStatic(X, -r + 6, 38, 2 * r - 12, 50, t, .75); X.font = '44px Bangers'; X.fillStyle = Math.sin(t * 8) > -.4 ? '#ffffff' : '#9aa0aa'; X.strokeStyle = '#141014'; X.lineWidth = 8;
    X.strokeText('SIN SEÑAL', 0, 80); X.fillText('SIN SEÑAL', 0, 80); }
  else { X.font = '50px Bangers'; X.fillStyle = val >= 7 ? PAIN_RED : '#ffffff'; X.fillText(String(Math.round(val)) + ' / 10', 0, 80); }
  X.font = '32px Bangers'; X.fillStyle = '#fde047'; X.fillText('DOLOR', 0, 120);
  X.restore(); }

/* where a character's head is (world): centre and radius, as drawChar places it */
function headInfo(cname, p) { const c = CAST[cname], G = charGeom(c, p), S = (p.s || 1) * (c.s || 1), f = p.flip || 1;
  const hd = (typeof CUT_DIMS !== 'undefined' && CUT_DIMS[cname] && CUT_DIMS[cname].headDrop) || 10;
  return { x: p.x + (p.hx || 0) * S * f, y: p.y + (G.top - 100 + hd + (p.hy || 0) + (p.slump || 0) * 14) * S, r: c.r * S, f, S, G }; }
function curita(g, x, y, w, rot) { g.save(); g.translate(x, y); g.rotate(rot); const h = w * .36; shape(g, q => rrPath(q, -w / 2, -h / 2, w, h, h / 2), '#f3c79c', 3);
  shape(g, q => rrPath(q, -w * .17, -h * .38, w * .34, h * .76, 4), '#e5a978', 0); g.fillStyle = 'rgba(150,90,60,.45)';
  for (const sx of [-1, 1]) for (const dy of [-.18, .18]) { g.beginPath(); g.arc(sx * w * .33, dy * h, 1.6, 0, 7); g.fill(); } g.restore(); }
/* the week's damage on the hero: m = { bump 0..1, cheek, chin, ankle } (draw right after drawChar, same layer) */
function hurtMarks(g, cname, p, m = {}) {
  const h = headInfo(cname, p), r = h.r, f = h.f;
  if (m.bump > 0) { const bx = h.x - .26 * r * f, by = h.y - .44 * r, br = .17 * r * (.4 + .6 * m.bump);
    shape(g, q => q.ellipse(bx, by, br * 1.1, br, 0, 0, 7), '#f29a9a', 3); g.save(); g.globalAlpha = .8; circ(g, bx - br * .35, by - br * .35, br * .28, '#ffffff', 0); g.restore(); }
  if (m.cheek) curita(g, h.x + .44 * r * f, h.y + .22 * r, .42 * r, -.5 * f);
  if (m.chin) curita(g, h.x - .2 * r * f, h.y + .62 * r, .34 * r, .25 * f);
  if (m.ankle) { const ax = p.x + 30 * h.S * f + 2, ay = p.y - 34 * h.S; g.save(); g.translate(ax, ay); shape(g, q => rrPath(q, -26 * h.S, -24 * h.S, 52 * h.S, 40 * h.S, 8), '#f4f1ea', 3);
    g.strokeStyle = 'rgba(120,110,120,.5)'; g.lineWidth = 2; for (let i = 0; i < 3; i++) { g.beginPath(); g.moveTo(-24 * h.S, -16 * h.S + i * 12 * h.S); g.lineTo(24 * h.S, -10 * h.S + i * 12 * h.S); g.stroke(); } g.restore(); }
}
/* «¡AY!» comic word and stars over somebody's head */
function hitStars(X, x, y, u, s = 1) { if (u <= 0 || u >= 1) return; X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.globalAlpha = 1 - u * u;
  for (let i = 0; i < 5; i++) { const an = u * 5 + i / 5 * Math.PI * 2, px = x + Math.cos(an) * 70 * s, py = y + Math.sin(an) * 22 * s;
    X.save(); X.translate(px, py); X.rotate(an); X.beginPath(); for (let k = 0; k < 10; k++) { const rr = (k % 2 ? 7 : 16) * s, a2 = k / 10 * Math.PI * 2; X.lineTo(Math.cos(a2) * rr, Math.sin(a2) * rr); } X.closePath();
    X.fillStyle = '#fde047'; X.fill(); X.lineWidth = 3; X.strokeStyle = '#141014'; X.stroke(); X.restore(); }
  X.restore(); }
