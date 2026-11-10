/* Cut-out characters: AI-drawn body parts (one PNG per part) hung on the same skeleton as drawChar.
   Springs, IK, clap contact, walk cycle and poses come from lib.js unchanged; only the drawing differs.
   Faces stay procedural (face() from lib.js), so blinking, lip sync, brows and sweat keep working.
   Load after lib.js, sets.js and cut/specs.js; then `await CUT_READY` before rendering.
   ?hyb=1 pages also swap painted background plates in for the vector sets (CUT_BG). */

// Joint metrics of each part (image pixels) come from cut/specs.js, written by cut/slice.py.
// Rig proportions per character (rig units, same space as drawChar) are tuned here.
const CUT_DIMS = {
  tu:   { sh: 74, shy: 50, armW: 50, legW: 44, hipX: 30, handR: 27, torsoW: 204, headDrop: 18, shoeW: 66, shoeH: 56, restX: 124, restY: -16 },
  mama: { sh: 76, shy: 56, armW: 46, legW: 40, hipX: 30, handR: 25, torsoW: 200, headDrop: 12, shoeW: 58, shoeH: 44, restX: 124, restY: -16 },
};
const CUT_BG = { kitchen: 'cut/bg/kitchen.jpg' };

const CUT = {};
const CUT_BASE = (document.currentScript && document.currentScript.src || '').replace(/[^/]*$/, '');
function cutLoad(src) { return new Promise((ok, bad) => { const im = new Image(); im.onload = () => ok(im); im.onerror = () => bad(new Error('cutout: cannot load ' + src)); im.src = CUT_BASE + src; }); }
const CUT_READY = (async () => {
  for (const [name, spec] of Object.entries(CUT_SPEC)) {
    if (!CUT_DIMS[name] || !CAST[name]) continue;
    const parts = { dims: CUT_DIMS[name] };
    for (const k of ['head', 'torso', 'upper', 'fore', 'hand', 'fist', 'leg', 'shoe']) parts[k] = Object.assign({ img: await cutLoad(`cut/${name}/${k}.png`) }, spec[k]);
    CUT[name] = Object.assign({}, spec, parts);
    Object.assign(CAST[name], { cut: name, restX: CUT_DIMS[name].restX, restY: CUT_DIMS[name].restY });
  }
  if (new URLSearchParams(location.search).get('hyb')) {
    for (const [set, src] of Object.entries(CUT_BG)) {
      const img = await cutLoad(src);
      SET_BUILDERS[set] = () => { const c = mkCanvas(), g = c.getContext('2d'); g.imageSmoothingQuality = 'high'; g.drawImage(img, 0, 0, W, H); return { bg: c, raw: 1 }; };
    }
  }
  return true;
})();

/* image rows y0..y1 of part P land exactly on the bone a->b; w = drawn width of the part's body */
function cutSeg(g, P, a, b, w, y0 = P.y0, y1 = P.y1) {
  const dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy) || 1, ky = L / (y1 - y0), kx = w / P.w, I = P.img;
  g.save(); g.translate(a[0], a[1]); g.rotate(Math.atan2(dy, dx) - Math.PI / 2);
  g.drawImage(I, -P.cx * kx, -y0 * ky, I.width * kx, I.height * ky); g.restore();
}
/* mitten at h, fingers pointing away from the elbow e, thumb towards the body (P.thumb: side of the thumb in the PNG) */
function cutHand(g, P, e, h, r, squash) {
  const th = Math.atan2(h[1] - e[1], h[0] - e[0]) - Math.PI / 2, k = r / P.R;
  const fx = (P.thumb || 1) * (Math.cos(th) * -Math.sign(h[0] || 1) < 0 ? -1 : 1);
  g.save(); g.translate(h[0], h[1]); g.rotate(th); g.scale(fx * k * (1 - .2 * squash), k * (1 + .1 * squash));
  g.drawImage(P.img, -P.cx, -P.cy); g.restore();
}
function drawCut(g, c, cname, p, G) {
  const R = CUT[c.cut], D = R.dims, S = (p.s || 1) * (c.s || 1);
  g.save(); g.translate(p.x || 0, p.y || 0); g.scale(S * (p.flip || 1), S); if (p.lean) g.rotate(p.lean);
  const { hipY, top, sit, walk, ph } = G, tt = p.t || 0;
  if (!p.noShadow) { g.save(); const sg = g.createRadialGradient(-20, -2, 4, -20, -2, 120); sg.addColorStop(0, 'rgba(60,30,10,.30)'); sg.addColorStop(1, 'rgba(60,30,10,0)'); g.fillStyle = sg; g.beginPath(); g.ellipse(-20, -2, 120, 20, 0, 0, 7); g.fill(); g.restore(); }
  // legs: one painted trouser leg per side, hip to ankle; front-view sneaker over the ankle
  for (const s of [-1, 1]) {
    let fx, fy;
    if (sit > .5) { const fs = s > 0 ? (p.footSwing || 0) : 0; fx = s * 40 + fs; fy = -10 - Math.abs(fs) * .4; }
    else { const sw = Math.sin(ph + (s > 0 ? 0 : Math.PI)) * walk, lift = Math.max(0, Math.cos(ph + (s > 0 ? 0 : Math.PI))) * walk * 22;
      fx = s * D.hipX + sw * 34; fy = -10 - lift - (p.jump || 0); }
    cutSeg(g, R.leg, [s * D.hipX, hipY - 16], [fx, fy - 4], D.legW);
    const W2 = D.shoeW, H2 = D.shoeH, I = R.shoe.img;
    g.drawImage(I, fx + s * 3 - R.shoe.cx * W2 / R.shoe.w, fy + 12 - H2, I.width * W2 / R.shoe.w, H2);
  }
  const A = solveArms(c, cname, p, G, D.sh, D.shy);
  const arm = (sh, e, hf) => {
    let dx = hf[0] - e[0], dy = hf[1] - e[1]; const L = Math.hypot(dx, dy) || 1; dx /= L; dy /= L;
    const wr = [hf[0] - dx * D.handR * .55, hf[1] - dy * D.handR * .55];
    g.save(); g.fillStyle = R.sleeve; g.strokeStyle = 'rgba(58,26,40,.95)'; g.lineWidth = 3.2; g.beginPath(); g.arc(e[0], e[1], D.armW * .47, 0, 7); g.fill(); g.stroke(); g.restore();   // elbow cap
    cutSeg(g, R.upper, sh, e, D.armW); cutSeg(g, R.fore, e, wr, D.armW * .96);
    cutHand(g, p.fist ? R.fist : R.hand, e, hf, D.handR, A.squash);
  };
  const farArm = () => { arm(A.shL, A.eL, A.hLf); if (p.holdL) p.holdL(g, A.hLf[0], A.hLf[1]); };
  if (!p.armsFront) farArm();
  // torso: hem on the hips, top on the shoulders (breathing stretches it a hair)
  { const hem = hipY + 8, I = R.torso.img, kx = D.torsoW / R.torso.w, ky = (hem - top + 6) / I.height;
    g.drawImage(I, -R.torso.cx * kx, hem - I.height * ky, I.width * kx, I.height * ky); }
  // head: painted hair and skin, procedural face on top
  const hx = p.hx || 0, hy = top - 100 + D.headDrop + (p.hy || 0) + (p.slump || 0) * 14, r = c.r;
  const live = !p.still && p.t != null, rot = (p.rot || 0) + (live && p.rot == null ? Math.sin(tt * .8 + c.seed) * .025 : 0);
  g.save(); g.translate(hx, hy); g.rotate(rot);
  { const P = R.head, k = r / P.R; g.drawImage(P.img, -P.cx * k, -P.cy * k, P.img.width * k, P.img.height * k); }
  g.fillStyle = 'rgba(240,130,150,.18)'; for (const s of [-1, 1]) { g.beginPath(); g.ellipse(s * r * .5, r * .27, r * .15, r * .09, 0, 0, 7); g.fill(); }
  face(g, c, r, Object.assign({ blink: p.blink != null ? p.blink : (p.still ? 0 : autoBlink(tt, c.seed)) }, p));
  g.restore();
  if (p.armsFront) farArm();
  arm(A.shR, A.eR, A.hRf); if (p.holdR) p.holdR(g, A.hRf[0], A.hRf[1]);
  g.restore();
  return G;
}
