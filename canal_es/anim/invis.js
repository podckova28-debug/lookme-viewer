/* Ep04 look: the invisible hero.
   The hero is drawn into his own layer I (st.inv); the world (A) is drawn as usual. What he holds goes into A (floatHold),
   so it floats in the air. The frame is laid out as: world -> hero -> colour grade -> vignette.
   inv = 0: the hero in plain colour. inv = 1: glass — the world behind him bent as through a lens, a pale ghost of his drawing
   (so the viewer still reads his face), a cyan rim with a soft glow and a slow light sweep.

   const st = stageI(cam); st.wld(g => drawSet(g, 'kitchen')); st.inv(g => drawChar(g, 'tu', hp)); st.fg(g => kitchenTable(g));
   hp.holdR = floatHold(st, (g, x, y) => drawSpr(g, 'toast', x, y, 60));
   composeI(X, st, { inv: 1, t });
   voiceBubble(X, cam, t, id, [wx, wy])        // a line spoken by nobody you can see: dashed bubble, words typed with the voice */
const INV_COL = '#8ff3ff';
function stageI(cam) { const st = stage(cam), I = layer('I'); camApply(I, cam); st.I = I;
  st.inv = fn => fn(I);
  st.fg = fn => { fn(st.A); I.save(); I.globalCompositeOperation = 'destination-out'; fn(I); I.restore(); };   // world things in front of the hero
  return st; }
/* a prop held by the invisible hero: drawn into the world layer with the hand's transform, so it stays visible */
function floatHold(st, draw) { return (g, x, y) => { const m = g.getTransform(), A = st.A; A.save(); A.setTransform(m); draw(A, x, y); A.restore(); }; }

let INV_SM = null;
function glassFX(X, I, a, t) {
  if (a <= 0) return;
  const src = X.canvas;
  // 1. refraction: the frame behind him, shifted and slightly magnified, seen only inside his silhouette
  const Rf = layer('Ir'), k = 1.035, ox = Math.sin(t * 1.7) * 5 + 7, oy = Math.cos(t * 1.3) * 4;
  Rf.drawImage(src, -W * (k - 1) / 2 + ox, -H * (k - 1) / 2 + oy, W * k, H * k);
  Rf.globalCompositeOperation = 'destination-in'; Rf.drawImage(I.canvas, 0, 0); Rf.globalCompositeOperation = 'source-over';
  // a cold tint and a moving light sweep inside the body
  Rf.globalCompositeOperation = 'source-atop'; Rf.fillStyle = 'rgba(160,235,255,.16)'; Rf.fillRect(0, 0, W, H);
  const u = ((t * .35) % 1.6) - .3, gx = u * W, sw = Rf.createLinearGradient(gx - 260, 0, gx + 260, H * .5);
  sw.addColorStop(0, 'rgba(255,255,255,0)'); sw.addColorStop(.5, 'rgba(235,252,255,.32)'); sw.addColorStop(1, 'rgba(255,255,255,0)');
  Rf.fillStyle = sw; Rf.fillRect(0, 0, W, H); Rf.globalCompositeOperation = 'source-over';
  X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.globalAlpha = clamp(a); X.drawImage(Rf.canvas, 0, 0); X.restore();
  // 2. pale ghost of the drawing: the face and folds stay readable for the viewer
  const Gh = layer('Ig'); Gh.filter = 'grayscale(1) brightness(1.75) contrast(1.25)'; Gh.drawImage(I.canvas, 0, 0); Gh.filter = 'none';
  Gh.globalCompositeOperation = 'source-atop'; Gh.fillStyle = 'rgba(150,235,255,.35)'; Gh.fillRect(0, 0, W, H); Gh.globalCompositeOperation = 'source-over';
  X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.globalAlpha = .26 * clamp(a); X.drawImage(Gh.canvas, 0, 0);
  // dark lines of the drawing, faint: multiply keeps only what is darker than the glass
  X.globalCompositeOperation = 'multiply'; X.globalAlpha = .1 * clamp(a); X.drawImage(Gh.canvas, 0, 0); X.restore();
  // 3. rim: silhouette dilated by 3 px minus the silhouette, in cyan, plus a low-res glow
  const E = layer('Ie'); for (const [dx, dy] of [[-3, 0], [3, 0], [0, -3], [0, 3], [-2, -2], [2, -2], [-2, 2], [2, 2]]) E.drawImage(I.canvas, dx, dy);
  E.globalCompositeOperation = 'source-in'; E.fillStyle = INV_COL; E.fillRect(0, 0, W, H);
  E.globalCompositeOperation = 'destination-out'; E.drawImage(I.canvas, 0, 0); E.globalCompositeOperation = 'source-over';
  if (!INV_SM) INV_SM = [0, 1].map(() => { const c = document.createElement('canvas'); c.width = W / 4; c.height = H / 4; return c; });
  const s0 = INV_SM[0].getContext('2d'), s1 = INV_SM[1].getContext('2d');
  s0.clearRect(0, 0, W / 4, H / 4); s0.drawImage(E.canvas, 0, 0, W / 4, H / 4);
  s1.clearRect(0, 0, W / 4, H / 4); s1.filter = 'blur(3px)'; s1.drawImage(INV_SM[0], 0, 0); s1.filter = 'none';
  const fl = .88 + .12 * Math.sin(t * 5.3) * Math.sin(t * 2.1);
  X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.globalCompositeOperation = 'screen'; X.globalAlpha = .85 * clamp(a) * fl; X.drawImage(INV_SM[1], 0, 0, W, H);
  X.globalCompositeOperation = 'source-over'; X.globalAlpha = .9 * clamp(a) * fl; X.drawImage(E.canvas, 0, 0); X.restore();
}
function composeI(X, st, o = {}) {
  const inv = o.inv == null ? 1 : clamp(o.inv), t = o.t || 0;
  X.setTransform(1, 0, 0, 1, 0, 0); X.filter = 'none'; X.globalAlpha = 1; X.globalCompositeOperation = 'source-over';
  X.drawImage(st.A.canvas, 0, 0);
  if (inv < 1) { X.save(); X.globalAlpha = 1 - inv; X.drawImage(st.I.canvas, 0, 0); X.restore(); }
  glassFX(X, st.I, inv, t);
  if (CUR_LOOK.grade) { X.save(); X.globalCompositeOperation = 'multiply'; X.fillStyle = CUR_LOOK.grade; X.fillRect(0, 0, W, H); X.restore(); }
  if (!VIG) { VIG = document.createElement('canvas'); VIG.width = W; VIG.height = H; const v = VIG.getContext('2d'), gr = v.createRadialGradient(W / 2, H * .46, H * .35, W / 2, H / 2, H * 1.05);
    gr.addColorStop(0, 'rgba(10,6,20,0)'); gr.addColorStop(1, 'rgba(10,6,20,.42)'); v.fillStyle = gr; v.fillRect(0, 0, W, H); }
  X.drawImage(VIG, 0, 0);
  window.__cam = st.cam; window.__frz = 0;
}
/* sparkles while he fades in or out: screen point x, y, spread r, u 0..1 through the transition */
function invSparkle(X, x, y, r, u, seed = 3) { if (u <= 0 || u >= 1) return; const rr = rnd(seed);
  X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.globalCompositeOperation = 'lighter';
  for (let i = 0; i < 26; i++) { const ang = rr() * 6.283, d = r * (.2 + rr() * .9) * (.6 + .6 * u), sx = x + Math.cos(ang) * d * .55, sy = y + Math.sin(ang) * d - u * 80 * rr(),
      s = (4 + rr() * 9) * Math.sin(Math.PI * clamp(u * 1.2 - rr() * .2)); if (s <= 0) continue;
    X.globalAlpha = .9; X.fillStyle = rr() < .5 ? '#ffffff' : INV_COL; X.beginPath(); X.moveTo(sx, sy - s * 2); X.lineTo(sx + s * .5, sy); X.lineTo(sx, sy + s * 2); X.lineTo(sx - s * .5, sy); X.closePath(); X.fill();
    X.beginPath(); X.moveTo(sx - s * 2, sy); X.lineTo(sx, sy + s * .5); X.lineTo(sx + s * 2, sy); X.lineTo(sx, sy - s * .5); X.closePath(); X.fill(); }
  X.restore(); }
/* a line from someone nobody can see: dashed cyan bubble, a crossed-out eye badge, words typed along with the voice */
function voiceBubble(X, cam, t, id, m, o = {}) {
  const L = T().L[id]; if (!L || !m) return; const t0 = L[0], d = L[1], hold = o.hold == null ? .35 : o.hold;
  const a = R(t, t0 - .04, t0 + .12, outC) * (1 - R(t, t0 + d + hold, t0 + d + hold + .2)); if (a <= 0) return;
  const txt = o.text || VO_TEXT[id]; let [mx, my] = worldToScreen(cam, m[0], m[1]); mx = clamp(mx, 90, W - 90); my = clamp(my, 260, H - 150);
  const size = o.size || 52, maxW = o.w || 660;
  X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.font = `bold ${size}px ComicNeue`;
  const lines = wrapLines(X, txt, maxW), lw = Math.max(...lines.map(l => X.measureText(l).width)), lh = size * 1.12, bw = Math.max(lw, 160) + 56, bh = lines.length * lh + 40;
  const rr = (o.r || 110) * (cam.z || 1);
  let bx, by; if (o.dx == null) { bx = mx - bw / 2; by = my - rr * 1.7 - bh; } else { bx = o.dx < 0 ? mx - rr * 1.15 - bw : mx + rr * 1.15; by = my - rr * .9 - bh * .6 + (o.dy || 0); }
  bx = clamp(bx, 30, W - bw - 30); by = clamp(by, 24, H - bh - 30);
  const s = .85 + .15 * back(R(t, t0 - .04, t0 + .2)); X.translate(bx + bw / 2, by + bh / 2); X.scale(s, s); X.translate(-bw / 2, -bh / 2); X.globalAlpha = clamp(a);
  const tx = clamp(mx - bx, 50, bw - 50), ty = bh, ex = tx + (mx - bx - tx) * .5, ey = ty + Math.max(30, ((my - by) - ty) * .5);
  X.fillStyle = 'rgba(236,252,255,.94)'; X.strokeStyle = '#1b6f86'; X.lineWidth = 6; X.setLineDash([18, 12]); X.lineDashOffset = -t * 40;
  X.beginPath(); X.moveTo(tx - 26, ty - 4); X.quadraticCurveTo(tx - 6, (ty + ey) / 2, ex, ey); X.quadraticCurveTo(tx + 10, (ty + ey) / 2, tx + 26, ty - 4); X.closePath(); X.fill(); X.stroke();
  X.beginPath(); rrPath(X, 0, 0, bw, bh, 30); X.fill(); X.stroke(); X.setLineDash([]);
  X.fillStyle = 'rgba(236,252,255,1)'; X.fillRect(tx - 22, bh - 9, 44, 12);
  // badge: an eye, crossed out
  X.save(); X.translate(bw - 14, 14); X.fillStyle = INV_COL; X.beginPath(); X.arc(0, 0, 26, 0, 7); X.fill(); X.lineWidth = 5; X.strokeStyle = '#1b3a46'; X.stroke();
  X.lineWidth = 4; X.beginPath(); X.ellipse(0, 0, 15, 9, 0, 0, 7); X.stroke(); X.fillStyle = '#1b3a46'; X.beginPath(); X.arc(0, 0, 4.5, 0, 7); X.fill();
  X.lineWidth = 5; X.beginPath(); X.moveTo(-15, 13); X.lineTo(15, -13); X.stroke(); X.restore();
  const ph = t - t0, typed = clamp((ph - .05) / Math.max(.3, d * .92)); let budget = Math.max(1, Math.round(typed * txt.length));
  X.fillStyle = '#163845'; X.textAlign = 'left'; X.textBaseline = 'alphabetic'; X.font = `bold ${size}px ComicNeue`;
  lines.forEach((l, i) => { const shown = l.slice(0, Math.max(0, budget)); budget -= l.length + 1; X.fillText(shown, 28, 20 + lh * (i + .8)); });
  X.restore();
}
