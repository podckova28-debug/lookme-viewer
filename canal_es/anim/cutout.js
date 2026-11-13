/* Hybrid look: AI-painted plates, props and cut-out characters on top of the code animation.
   Characters: AI-drawn body parts (one PNG per part) hung on the same skeleton as drawChar. Springs, IK, clap
   contact, walk cycle and poses come from lib.js unchanged; faces stay procedural (face() from lib.js), so
   blinking, lip sync, brows, glasses, mustaches and sweat keep working.
   Props and animals: the vector prop functions are replaced by sprites fitted to the same world boxes, so scene
   code (positions, layering) does not change.
   Load after lib.js, sets.js and cut/specs.js; then `await CUT_READY` before rendering.
   Only pages opened with ?hyb=1 switch to the hybrid look; without it everything stays vector. */

const HYB = new URLSearchParams(location.search).has('hyb');

// Rig proportions per character (rig units, same space as drawChar). Joint metrics of the parts (image pixels)
// come from cut/specs.js, written by cut/slice.py.
const CUT_BASE_DIMS = { sh: 74, shy: 50, armW: 48, legW: 42, hipX: 30, handR: 26, torsoW: 200, headDrop: 14, shoeW: 62, restX: 124, restY: -16 };
const CUT_DIMS = {
  tu:      { armW: 50, legW: 44, handR: 27, torsoW: 204, headDrop: 18, shoeW: 66 },
  mama:    { sh: 76, shy: 56, armW: 46, legW: 40, handR: 25, headDrop: 12, shoeW: 58 },
  nacho:   { armW: 50, legW: 44, handR: 27, torsoW: 206, headDrop: 12, shoeW: 66 },
  valeria: { armW: 44, legW: 40, handR: 25, torsoW: 194, headDrop: 12, shoeW: 60 },
  profe:   { sh: 78, shy: 54, armW: 48, legW: 44, torsoW: 212, headDrop: 10, shoeW: 64 },
  // bare: short sleeves; the row of upper.png where the sleeve ends (the arm below it is drawn as one seamless tube)
  ex1: { headDrop: 8, bare: 211 }, ex2: { headDrop: 8, armW: 44, legW: 40, bare: 212 }, ex3: { headDrop: 16 }, ex4: { headDrop: 8, armW: 44, legW: 40, bare: 199 }, ex5: { headDrop: 8, bare: 204 }, ex6: { headDrop: 16 },
};
const CUT_FACE = { mama: { earrings: 0 } };   // features the painted head already has
const CUT_BG = { kitchen: 'kitchen', kitchenNight: 'kitchenNight', hallway: 'hallway', bedroom: 'bedroom', classroom: 'classroom', street: 'street', streetRain: 'streetRain',
  field: 'field', party: 'party', park: 'park', parkNight: 'parkNight', bathroom: 'bathroom',
  super: 'super', cafeteria: 'cafeteria', cine: 'cine', salaMaestros: 'salaMaestros' };
const CUT_PROPS = ['bed', 'blanket', 'nightstand', 'kitchenTable', 'teacherDesk', 'bench', 'goal', 'partyTable', 'pepeBody', 'pepeHead', 'pepeFront', 'catSit', 'catJump', 'flowerPot',
  'toast', 'torta', 'phone', 'glassFrog', 'tacos', 'popcorn', 'tissues', 'notebook'];

const CUT = {}, SPR = {};
const CUT_BASE = (document.currentScript && document.currentScript.src || '').replace(/[^/]*$/, '');
function cutLoad(src) { return new Promise((ok, bad) => { const im = new Image(); im.onload = () => ok(im); im.onerror = () => bad(new Error('cutout: cannot load ' + src)); im.src = CUT_BASE + src; }); }
const CUT_READY = (async () => {
  if (!HYB) return true;
  for (const [name, spec] of Object.entries(CUT_SPEC)) {
    if (!CAST[name]) continue;
    const D = Object.assign({}, CUT_BASE_DIMS, CUT_DIMS[name] || {}), parts = { dims: D };
    for (const k of ['head', 'torso', 'upper', 'fore', 'hand', 'fist', 'leg', 'shoe']) parts[k] = Object.assign({ img: await cutLoad(`cut/${name}/${k}.png`) }, spec[k]);
    D.shoeH = D.shoeH || D.shoeW * parts.shoe.img.height / parts.shoe.w * .82;
    CUT[name] = Object.assign({}, spec, parts);
    Object.assign(CAST[name], { cut: name, restX: D.restX, restY: D.restY }, CUT_FACE[name] || {});
  }
  for (const k of CUT_PROPS) SPR[k] = await cutLoad(`cut/props/${k}.png`);
  for (const [set, file] of Object.entries(CUT_BG)) {
    const img = await cutLoad(`cut/bg/${file}.jpg`), w = set === 'hallway' ? 2600 : W;
    SET_BUILDERS[set] = () => { const c = mkCanvas(w, H), g = c.getContext('2d'); g.imageSmoothingQuality = 'high'; g.drawImage(img, 0, 0, w, H); return { bg: c, raw: 1 }; };
  }
  installHybridProps();
  return true;
})();

/* ---------------------------------------------------------------- characters */
/* image rows y0..y1 of part P land exactly on the bone a->b; w = drawn width of the part's body */
function cutSeg(g, P, a, b, w, y0 = P.y0, y1 = P.y1, rows = 0) {   // rows > 0: draw only the image rows 0..rows (same placement)
  const dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy) || 1, ky = L / (y1 - y0), kx = w / P.w, I = P.img, n = rows || I.height;
  g.save(); g.translate(a[0], a[1]); g.rotate(Math.atan2(dy, dx) - Math.PI / 2);
  g.drawImage(I, 0, 0, I.width, n, -P.cx * kx, -y0 * ky, I.width * kx, n * ky); g.restore();
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
  // legs: one painted trouser leg per side, hip to ankle; front-view shoe over the ankle
  for (const s of [-1, 1]) {
    let fx, fy;
    if (sit > .5) { const fs = s > 0 ? (p.footSwing || 0) : 0; fx = s * 40 + fs; fy = -10 - Math.abs(fs) * .4; }
    else { const sw = Math.sin(ph + (s > 0 ? 0 : Math.PI)) * walk, lift = Math.max(0, Math.cos(ph + (s > 0 ? 0 : Math.PI))) * walk * 22;
      fx = s * D.hipX + sw * 34; fy = -10 - lift - (p.jump || 0); }
    cutSeg(g, R.leg, [s * D.hipX, hipY - 16], [fx, fy - 4], D.legW);
    const I = R.shoe.img, k = D.shoeW / R.shoe.w;
    g.drawImage(I, fx + s * 3 - R.shoe.cx * k, fy + 12 - D.shoeH, I.width * k, D.shoeH);
  }
  const A = solveArms(c, cname, p, G, D.sh, D.shy);
  const arm = (sh, e, hf) => {
    let dx = hf[0] - e[0], dy = hf[1] - e[1]; const L = Math.hypot(dx, dy) || 1; dx /= L; dy /= L;
    const wr = [hf[0] - dx * D.handR * .55, hf[1] - dy * D.handR * .55];
    if (D.bare) {   // bare arm: one outlined tube shoulder -> elbow -> wrist, so the elbow bends without a visible joint; the painted sleeve on top
      const w = D.armW * .97, ow = D.armW * .065, u = .3, s0 = [sh[0] + (e[0] - sh[0]) * u, sh[1] + (e[1] - sh[1]) * u];   // starts under the sleeve
      g.save(); g.lineJoin = 'round'; g.lineCap = 'round'; g.beginPath(); g.moveTo(s0[0], s0[1]); g.lineTo(e[0], e[1]); g.lineTo(wr[0], wr[1]);
      g.strokeStyle = 'rgb(50,16,40)'; g.lineWidth = w; g.stroke(); g.strokeStyle = R.sleeve; g.lineWidth = w - 2 * ow; g.stroke(); g.restore();
      cutSeg(g, R.upper, sh, e, D.armW, R.upper.y0, R.upper.y1, D.bare + 4);
    } else {
      g.save(); g.fillStyle = R.sleeve; g.strokeStyle = 'rgba(58,26,40,.95)'; g.lineWidth = 3.2; g.beginPath(); g.arc(e[0], e[1], D.armW * .47, 0, 7); g.fill(); g.stroke(); g.restore();   // elbow cap
      cutSeg(g, R.upper, sh, e, D.armW); cutSeg(g, R.fore, e, wr, D.armW * .96);
    }
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
  cutHeadImg(g, R, r);
  face(g, c, r, Object.assign({ blink: p.blink != null ? p.blink : (p.still ? 0 : autoBlink(tt, c.seed)) }, p));
  g.restore();
  if (p.armsFront) farArm();
  arm(A.shR, A.eR, A.hRf); if (p.holdR) p.holdR(g, A.hRf[0], A.hRf[1]);
  g.restore();
  return G;
}
function cutHeadImg(g, R, r) {
  const P = R.head, k = r / P.R; g.drawImage(P.img, -P.cx * k, -P.cy * k, P.img.width * k, P.img.height * k);
  g.fillStyle = 'rgba(240,130,150,.18)'; for (const s of [-1, 1]) { g.beginPath(); g.ellipse(s * r * .5, r * .27, r * .15, r * .09, 0, 0, 7); g.fill(); }
}

/* ---------------------------------------------------------------- props, animals, board */
// draw sprite rows [f0..f1] (fractions of its height) into the world box x, y, w, h
function spr(g, k, x, y, w, h, f0 = 0, f1 = 1) { const I = SPR[k]; g.drawImage(I, 0, I.height * f0, I.width, I.height * (f1 - f0), x, y, w, h); }
function installHybridProps() {
  const vecHead = window.drawHead;
  window.drawHead = (g, c, x, y, rot, p) => { if (!c.cut) return vecHead(g, c, x, y, rot, p); const R = CUT[c.cut];
    g.save(); g.translate(x, y); g.rotate(rot || 0); cutHeadImg(g, R, c.r); face(g, c, c.r, p); g.restore(); };
  const BED = { x: 50, w: 950, top: 383, h: 562 };   // mattress top lands at y≈700, legs on the floor
  window.bedBack = g => spr(g, 'bed', BED.x, BED.top, BED.w, BED.h);
  window.bedFront = (g, cover = 1) => { const top = 712 + (1 - cover) * 50; spr(g, 'blanket', 250, top, 760, 948 - top); };
  window.nightstand = g => spr(g, 'nightstand', 990, 756, 172, 186);
  window.kitchenTable = g => spr(g, 'kitchenTable', 540, 770, 840, 172);
  window.teacherDesk = (g, x) => spr(g, 'teacherDesk', x - 235, 690, 470, 252);
  window.desk = (g, x, y = FLOOR, s = 1) => spr(g, 'teacherDesk', x - 155 * s, y - 262 * s, 310 * s, 262 * s);
  window.partyTable = g => spr(g, 'partyTable', 545, 748, 830, 194);
  window.bench = (g, front) => { const x = 605, y = 618, w = 710, h = 326, seat = .47;   // backrest behind the sitters, seat and legs in front
    if (!front) spr(g, 'bench', x, y, w, h * seat, 0, seat); else spr(g, 'bench', x, y + h * seat, w, h * (1 - seat), seat, 1); };
  window.goal = (g, front) => { if (!front) spr(g, 'goal', 1286, 266, 610, 390); };
  window.boardOverlay = (g, l1, l2) => boardText(g, l1, l2);   // the painted board is blank: text only
  window.propPot = (g, x, y, s = 1, rot = 0) => { g.save(); g.translate(x, y); g.rotate(rot); g.scale(s, s); spr(g, 'flowerPot', -72, -134, 144, 166); g.restore(); };
  window.drawCat = (g, x, y, s, p = {}) => { const j = p.jump || 0; g.save(); g.translate(x, y); g.scale(s * -(p.flip || 1), s);   // sprites face left
    if (j > .3) { g.rotate(.25 * j); spr(g, 'catJump', -150, -150, 300, 145); } else spr(g, 'catSit', -70, -200, 140, 200);
    g.restore(); };
  // Pepe: body + head on a neck pivot; p.front turns the head to the viewer, p.tilt/p.peck rotate it
  window.drawPigeon = (g, x, y, s, p = {}) => { g.save(); g.translate(x, y); g.scale(s * (p.flip || 1), s);
    spr(g, 'pepeBody', -108, -118, 176, 122);
    const px = 30, py = -96 + (p.peck || 0) * 30;
    g.translate(px, py); g.rotate((p.tilt || 0) + (p.peck || 0) * .5);
    if (p.front) { g.scale(1 / (p.flip || 1), 1); spr(g, 'pepeFront', -28, -84, 56, 86); } else spr(g, 'pepeHead', -34, -82, 80, 84);
    g.restore(); };
}
function boardText(g, l1, l2) { text(g, l1, 520, 260, 74, '#3a6fb0', 'ComicNeue'); if (l2) text(g, l2, 520, 380, 64, '#c0262d', 'ComicNeue'); }
