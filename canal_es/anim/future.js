/* Ep02 look: "five seconds of future".
   The present is drawn as usual (stage A/M). What will happen in five seconds is drawn into a ghost layer F with the same
   camera, then laid over the frame as a cyan, glowing, slightly flickering hologram. A countdown ring (5…1) sits in the corner.

   const st = stageF(cam); st.wld(...); st.col(...); st.fut(g => drawChar(g, 'mama', futurePose));
   composeF(X, st, { ghost: 1, t });           // ghost: 0..1 opacity of the vision
   futHUD(X, a, secondsLeft);                   // optional countdown ring */
const FUT_COL = '#5ee7ff', FUT_DEEP = '#0b7fa8';
function stageF(cam) { const st = stage(cam), F = layer('F'); camApply(F, cam); st.F = F; st.fut = fn => fn(F); return st; }

let FUT_SCAN = null;
function futScanlines() { if (FUT_SCAN) return FUT_SCAN; FUT_SCAN = document.createElement('canvas'); FUT_SCAN.width = W; FUT_SCAN.height = H;
  const g = FUT_SCAN.getContext('2d'); g.fillStyle = 'rgba(0,0,0,.28)'; for (let y = 0; y < H; y += 6) g.fillRect(0, y, W, 2); return FUT_SCAN; }

/* the ghost layer as a hologram: cyan body that keeps a little of the drawing's colour, a soft glow, scanlines, a little flicker.
   Everything heavy happens at 1/6 resolution (the glow) or without canvas filters, so a frame stays cheap. */
const FUT_Q = 6; let FUT_SMALL = null;
function ghostFX(X, F, a, t = 0) {
  if (a <= 0) return;
  const flick = .9 + .1 * Math.sin(t * 37) * Math.sin(t * 13.3), k = clamp(a) * flick;
  const Gt = layer('Gt');   // tinted copy: 28% of the original colour under a cyan wash, scanlines cut out
  Gt.drawImage(F.canvas, 0, 0); Gt.globalCompositeOperation = 'source-atop'; Gt.fillStyle = 'rgba(94,231,255,.74)'; Gt.fillRect(0, 0, W, H);
  Gt.globalCompositeOperation = 'destination-out'; Gt.drawImage(futScanlines(), 0, 0); Gt.globalCompositeOperation = 'source-over';
  if (!FUT_SMALL) { FUT_SMALL = [0, 1].map(() => { const c = document.createElement('canvas'); c.width = W / FUT_Q; c.height = H / FUT_Q; return c; }); }
  const s0 = FUT_SMALL[0].getContext('2d'), s1 = FUT_SMALL[1].getContext('2d'), w = W / FUT_Q, h = H / FUT_Q;
  s0.clearRect(0, 0, w, h); s0.drawImage(F.canvas, 0, 0, w, h); s0.globalCompositeOperation = 'source-in'; s0.fillStyle = FUT_COL; s0.fillRect(0, 0, w, h); s0.globalCompositeOperation = 'source-over';
  s1.clearRect(0, 0, w, h); s1.filter = 'blur(3px)'; s1.drawImage(FUT_SMALL[0], 0, 0); s1.filter = 'none';
  X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.imageSmoothingEnabled = true;
  X.globalCompositeOperation = 'screen'; X.globalAlpha = .7 * k; X.drawImage(FUT_SMALL[1], 0, 0, W, H);
  X.globalAlpha = .3 * k; X.drawImage(FUT_SMALL[0], 0, 0, W, H);
  X.globalCompositeOperation = 'source-over'; X.globalAlpha = .62 * k;
  const jx = Math.sin(t * 23) * 2.5 * (1 - flick) * 10;   // tiny horizontal jitter on flicker
  X.drawImage(Gt.canvas, jx, 0);
  X.globalCompositeOperation = 'screen'; X.globalAlpha = .18 * k; X.drawImage(FUT_SMALL[0], jx + 4, 0, W, H);   // chromatic edge
  X.restore();
}

/* while the vision is on, the edges of the frame get a cold rim, like looking through it */
let FUT_VIG = null;
function futVignette(X, a) { if (a <= 0) return;
  if (!FUT_VIG) { FUT_VIG = document.createElement('canvas'); FUT_VIG.width = W; FUT_VIG.height = H; const v = FUT_VIG.getContext('2d'), gr = v.createRadialGradient(W / 2, H / 2, H * .45, W / 2, H / 2, H * 1.0);
    gr.addColorStop(0, 'rgba(94,231,255,0)'); gr.addColorStop(1, 'rgba(40,170,220,.32)'); v.fillStyle = gr; v.fillRect(0, 0, W, H); }
  X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.globalAlpha = clamp(a); X.drawImage(FUT_VIG, 0, 0); X.restore(); }

function composeF(X, st, f = {}) {
  compose2(X, st, f.frz || { amt: 0 });
  const a = f.ghost == null ? 1 : f.ghost; window.__ghost = a;
  futVignette(X, a * (f.rim == null ? 1 : f.rim));
  ghostFX(X, st.F, a, f.t || 0);
}

/* countdown ring, top right: n seconds left (5..0, fractional), a = opacity */
function futHUD(X, a, n, x = W - 150, y = 150, r = 86) {
  if (a <= 0) return; const sec = Math.max(0, Math.ceil(n - 1e-6)), u = clamp(n / 5);
  X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.globalAlpha = clamp(a);
  X.fillStyle = 'rgba(6,20,34,.55)'; X.beginPath(); X.arc(x, y, r + 16, 0, 7); X.fill();
  X.lineCap = 'round'; X.lineWidth = 14; X.strokeStyle = 'rgba(94,231,255,.22)'; X.beginPath(); X.arc(x, y, r, 0, 7); X.stroke();
  X.shadowColor = FUT_COL; X.shadowBlur = 24; X.strokeStyle = FUT_COL; X.beginPath(); X.arc(x, y, r, -Math.PI / 2, -Math.PI / 2 + u * Math.PI * 2); X.stroke();
  X.shadowBlur = 18; X.font = `${r * 1.25}px Bangers`; X.textAlign = 'center'; X.fillStyle = '#e9fdff'; X.fillText(String(sec), x, y + r * .44);
  X.shadowBlur = 0; X.font = '34px Bangers'; X.fillStyle = FUT_COL; X.fillText('FUTURO', x, y + r + 54);
  X.restore(); }

/* a quick cyan pulse when the vision switches on (screen point) */
function futPulse(X, x, y, u) { if (u <= 0 || u >= 1) return; X.save(); X.setTransform(1, 0, 0, 1, 0, 0);
  const rr = outC(u) * Math.hypot(W, H) * .8; X.globalAlpha = 1 - u; X.strokeStyle = FUT_COL; X.lineWidth = 16 * (1 - u) + 3; X.shadowColor = FUT_COL; X.shadowBlur = 30;
  X.beginPath(); X.arc(x, y, rr, 0, 7); X.stroke(); X.restore(); }

/* cyan glints in the hero's eyes while he is "seeing" (world coords of the head centre from charGeom) */
function futEyes(g, cname, p, a) { if (a <= 0) return; const c = CAST[cname], G = charGeom(c, p), S = (p.s || 1) * (c.s || 1), f = p.flip || 1, r = c.r;
  const hd = (typeof CUT_DIMS !== 'undefined' && CUT_DIMS[cname] && CUT_DIMS[cname].headDrop) || 10;
  const hyl = G.top - 100 + hd + (p.hy || 0) + (p.slump || 0) * 14, [lx, ly] = p.look || [0, 0];
  g.save(); g.globalAlpha = clamp(a); g.globalCompositeOperation = 'lighter';
  for (const s of [-1, 1]) { const x = p.x + ((p.hx || 0) + s * r * .33 + lx) * S * f, y = p.y + (hyl - r * .04 + ly) * S, rr = 30 * S;
    const gr = g.createRadialGradient(x, y, 0, x, y, rr); gr.addColorStop(0, 'rgba(170,248,255,.95)'); gr.addColorStop(1, 'rgba(94,231,255,0)'); g.fillStyle = gr; g.fillRect(x - rr, y - rr, 2 * rr, 2 * rr); }
  g.restore(); }
