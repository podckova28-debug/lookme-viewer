/* Ep04 «¿Qué pasaría si fueras invisible?» — scenes 0–5.
   Beats are keyed to narration (Lt/Le/Lm from anim/episode.js). The hero is drawn with anim/invis.js: his own layer,
   glass look, everything he holds floats. Lines he says while invisible get a dashed «voice from nowhere» bubble. */
SC.missing = (X, t) => { X.fillStyle = '#1b1530'; X.fillRect(0, 0, W, H); text(X, SID + ' (sin animar)', W / 2, H / 2, 90, '#fde047', 'Bangers', 'center'); };
const CHANNEL_NAME = 'PONLE QUE…';
const vis = (t, a, b, fi = .25, fo = .3) => R(t, a, a + fi) * (1 - R(t, b, b + fo));
const loopU = (t, t0, P) => (((t - t0) % P) + P) % P / P;
function standing(x, extra = {}) { return Object.assign({ x, y: FEET, s: S0 }, extra); }
function benchSit(x, extra = {}) { return Object.assign({ x, y: 905, s: S0, sit: 1, noShadow: 1, hL: [-80, -125], hR: [80, -125], armsFront: 1 }, extra); }
function walker(g, n, x0, v, tt, extra = {}) { const x = x0 + v * tt; drawChar(g, n, Object.assign({ x, y: FEET, s: S0, t: tt, walk: 1, phase: walkPh(x), flip: v < 0 ? -1 : 1 }, extra)); return x; }
/* the invisible hero: no shadow (nothing there to cast it) */
function ghost(p) { return Object.assign({ noShadow: 1 }, p); }
/* world point of a character's mouth, for bubbles */
function mouthPt(cname, p) { const c = CAST[cname], G = charGeom(c, p), S = (p.s || 1) * (c.s || 1); return [p.x + ((p.hx || 0) + (p.look ? p.look[0] : 0)) * S * (p.flip || 1), p.y + (G.top - 70 + (p.hy || 0)) * S]; }
/* the hand position in world space (for things held by somebody else) */
function handPt(cname, p, side = 1) { const c = CAST[cname], G = charGeom(c, p), S = (p.s || 1) * (c.s || 1), h = side > 0 ? (p.hR || restHand(1, G)) : (p.hL || restHand(-1, G)); return [p.x + h[0] * S * (p.flip || 1), p.y + h[1] * S]; }
function rewindFX(X, k, t) { if (k <= 0) return;
  X.save(); X.globalAlpha = .25 * k; X.fillStyle = '#ffffff'; const r = rnd(Math.floor(t * 30));
  for (let i = 0; i < 9; i++) { const y = r() * H, h = 4 + r() * 18; X.fillRect(0, y, W, h); } X.restore();
  X.save(); X.globalAlpha = .55 * k; X.fillStyle = '#0d0b12'; X.fillRect(0, H - 150, W, 150); X.restore();
  X.save(); X.globalAlpha = k; text(X, '◀◀  REBOBINANDO', 70, H - 52, 76, '#ffffff', 'Bangers', 'left', OUT, 10); X.restore(); }
function crossSticker(X, s, a, x, y, ok = false) { if (a <= 0) return; sticker(X, s + (ok ? '  ✓' : '  ✗'), a, x, y, 60, ok ? '#a7f3a0' : '#ffd34d'); }
function heartPop(g, x, y, u, s = 1) { if (u <= 0 || u >= 1) return; g.save(); g.globalAlpha = 1 - u * u; g.translate(x, y - u * 90); g.scale(s * (.6 + .4 * back(Math.min(1, u * 3))), s * (.6 + .4 * back(Math.min(1, u * 3))));
  shape(g, q => { q.moveTo(0, 18); q.bezierCurveTo(-34, -6, -20, -34, 0, -16); q.bezierCurveTo(20, -34, 34, -6, 0, 18); }, '#ff5d7a', 4); g.restore(); }
function nightTint(X, a = 1) { X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.globalCompositeOperation = 'multiply'; X.fillStyle = `rgba(60,70,140,${.55 * a})`; X.fillRect(0, 0, W, H); X.restore(); }
function dashRing(X, x, y, r, t, col = '#ffd34d') { X.save(); X.strokeStyle = col; X.lineWidth = 8; X.setLineDash([22, 16]); X.lineDashOffset = -t * 60; X.beginPath(); X.arc(x, y, r, 0, 7); X.stroke(); X.restore(); }
function leash(g, a, b, sag = 60) { g.save(); g.strokeStyle = '#e0457b'; g.lineWidth = 5; g.lineCap = 'round'; g.beginPath(); g.moveTo(a[0], a[1]); g.quadraticCurveTo((a[0] + b[0]) / 2, Math.max(a[1], b[1]) + sag, b[0], b[1]); g.stroke(); g.restore(); }
function plate(g, x, y, s = 1) { g.save(); g.translate(x, y); g.scale(s, s); shape(g, q => q.ellipse(0, 0, 90, 22, 0, 0, 7), '#ffffff', 4); shape(g, q => q.ellipse(0, -2, 60, 13, 0, 0, 7), '#eef1f4', 2); g.restore(); }
function crumbs(g, x, y, n = 7) { const r = rnd(11); for (let i = 0; i < n; i++) circ(g, x + (r() - .5) * 90, y + (r() - .5) * 12, 3 + r() * 3, '#d39a52', 2); }
function chairBack(g, x, y = 600) { shape(g, q => rrPath(q, x - 85, y, 170, 220, 18), '#b98252', 5); shape(g, q => rrPath(q, x - 60, y + 26, 120, 30, 8), '#a06c40', 3); }
/* a speech bubble for Pepe's coo or other unvoiced sounds */
function cooBubble(X, cam, wx, wy, t, t0, d, s = 'RUU') { const a = R(t, t0, t0 + .15, back) * (1 - R(t, t0 + d, t0 + d + .2)); if (a <= 0) return; const [x, y] = worldToScreen(cam, wx, wy); bubble(X, s, x, y - 20, a, 56); }
/* Pepe keeps turning his head toward you: side view, flipped to face hx */
function pepeWatch(g, x, y, s, hx, t, extra = {}) { drawPigeon(g, x, y, s, Object.assign({ flip: hx < x ? -1 : 1, tilt: Math.sin(t * .9) * .06 }, extra)); }
function panel(X, x, y, w, a, draw, rot = 0, v = { cx: W / 2, cy: H / 2, z: 1 }) { if (a <= 0) return null;
  const P = layer('PANEL'), zc = window.__camz; window.__camz = 1;
  P.setTransform(v.z, 0, 0, v.z, W / 2 - v.cx * v.z, H / 2 - v.cy * v.z); draw(P); P.setTransform(1, 0, 0, 1, 0, 0); window.__camz = zc;
  const h = w * 9 / 16, s = .85 + .15 * back(a);
  X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.filter = 'none'; X.globalCompositeOperation = 'source-over'; X.globalAlpha = clamp(a);
  X.translate(x + w / 2, y + h / 2); X.rotate(rot); X.scale(s, s); X.translate(-w / 2, -h / 2);
  X.fillStyle = '#ffffff'; X.fillRect(-12, -12, w + 24, h + 24); X.drawImage(P.canvas, 0, 0, W, H, 0, 0, w, h);
  X.lineWidth = 8; X.strokeStyle = '#141014'; X.strokeRect(-12, -12, w + 24, h + 24); X.restore();
  const k = v.z * w / W; return { cx: v.cx - (x + w / 2 - W / 2) / k, cy: v.cy - (y + h / 2 - H / 2) / k, z: k }; }
/* the park with Renata waiting on the bench (s00 and s12–s14) */
function parkRenata(st, t, rp, cp) { st.wld(g => { drawSet(g, 'park'); bench(g, 0); });
  st.wld(g => drawChar(g, 'valeria', rp)); st.wld(g => bench(g, 1));
  let m = null; st.wld(g => { m = drawAnimal(g, 'canela', cp.x, cp.y, cp.s || .9, Object.assign({ t }, cp)); }); return m; }
function phoneHold(g, x, y) { drawSpr(g, 'phone', x + 6, y + 30, 70, { rot: -.15 }); }

/* ================================================================ 0. cold open: Saturday, 5 p.m., right in front of her */
SC.s00 = (X, t) => {
  const rw = Lm('s00_07', .45);
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 560, z: 1.0, z2: 1.06, lock: 1 },
    { t: Lt('s00_02') - .05, cx: 1180, cy: 640, z: 1.9, z2: 2.0, lock: 1 },
    { t: Lt('s00_03') - .05, cx: 940, cy: 560, z: 1.25, z2: 1.32, lock: 1 },
    { t: Lt('s00_04') - .05, cx: 1080, cy: 520, z: 2.4, z2: 2.55, lock: 1 },
    { t: Lt('s00_05') - .05, cx: 680, cy: 520, z: 2.3, z2: 2.45, lock: 1 },
    { t: Lt('s00_06') - .05, cx: 960, cy: 540, z: 1.15, z2: 1.0, lock: 1 },
    { t: rw, cx: 960, cy: 540, z: 1.0, lock: 1 },
  ]);
  const st = stageI(cam);
  const rp = benchSit(1080, { t, look: [6, 18], mouth: -.1, brow: .3, hR: [60, -300], holdR: phoneHold });
  if (speaking(t, 's00_04')) { rp.open = talk(t, 's00_04'); rp.look = [-10, -4]; rp.brow = .6; rp.hR = [60, -300]; }
  if (t > Le('s00_04')) { rp.look = [4, 18]; rp.mouth = -.25; rp.brow = .7; }
  parkRenata(st, t, rp, { x: 1330, y: 1000, s: .85, tilt: Math.sin(t * 1.6) * .06 });
  st.wld(g => pepeWatch(g, 1560, 760, .5, 640, t));   // on the grass: looking straight at you
  const hp = ghost(standing(640, { t, y: 1010, s: .84, look: [14, 8], mouth: .3, blush: .6, hL: [-60, -330], hR: [60, -330] }));
  if (t > Lt('s00_04')) { hp.look = [16, 4]; hp.mouth = -.1; hp.brow = .5; }
  if (t > Lt('s00_05')) { hp.mouth = -.3; hp.brow = .8; hp.blush = 0; hp.hL = null; hp.hR = null; hp.slump = .6; }
  if (t > Lt('s00_03') + .6 && t < Lt('s00_04')) { const G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = POSE.wave(t, G); hp.mouth = .6; }   // waves; she doesn't see
  st.inv(g => drawChar(g, 'tu', hp));
  composeI(X, st, { inv: 1, t });
  sticker(X, 'SÁBADO · 5:00 PM', vis(t, .3, Lt('s00_02') - .2), 70, 70, 64);
  if (t > Lt('s00_03') + .2 && t < Lt('s00_05')) { const [x, y] = worldToScreen(cam, 640, 330); X.save(); X.globalAlpha = vis(t, Lt('s00_03') + .2, Lt('s00_05') - .3); text(X, '↓ TÚ', x, y, 64, INV_COL, 'Bangers', 'center', OUT, 10); X.restore(); }
  if (t > rw) rewindFX(X, R(t, rw, rw + .2), t);
};

/* ================================================================ 1. the power */
SC.s01 = (X, t) => {
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 540, z: 1.0, z2: 1.06, lock: 1 },
    { t: Lt('s01_02') - .05, cx: 900, cy: 560, z: 1.15, z2: 1.2, lock: 1 },
    { t: Lt('s01_03') - .05, cx: 860, cy: 520, z: 2.0, z2: 2.1, lock: 1 },
    { t: Lt('s01_04') - .05, cx: 1000, cy: 560, z: 1.05, z2: 1.1, lock: 1 },
    { t: Lt('s01_05') - .05, cx: 860, cy: 480, z: 1.8, z2: 1.9, lock: 1 },
    { t: Lt('s01_06') - .05, cx: 960, cy: 540, z: 1.1, z2: 1.15, lock: 1 },
  ]);
  const st = stageI(cam); st.wld(g => drawSet(g, 'street'));
  // a security camera on the school wall, sweeping, sees nothing
  st.wld(g => { const a = Math.sin(t * .9) * .35; g.save(); g.translate(330, 300); shape(g, q => q.rect(-10, -10, 20, 40), '#7b8794', 4); g.rotate(.5 + a); shape(g, q => rrPath(q, -20, 10, 90, 44, 8), '#e9edf2', 4); circ(g, 68, 32, 9, '#141014', 3);
    circ(g, -6, 20, 5, Math.sin(t * 6) > 0 ? '#ff4d4d' : '#7a2020', 0); g.restore(); });
  const walkEnd = Lt('s01_03') - .3, hx = mix(260, 860, R(t, 0, walkEnd, io));
  const hp = ghost({ x: hx, y: FEET, s: S0, t, walk: t < walkEnd ? 1 : 0, phase: walkPh(hx), look: [10, 2], mouth: .4 });
  if (t > Lt('s01_03')) { hp.look = [0, 10]; hp.mouth = .1; hp.brow = .4; const G = charGeom(CAST.tu, hp); hp.hL = [-120, G.top + 210]; hp.hR = [120, G.top + 210]; }   // looks at his own (missing) hoodie
  let jump = 0; if (t > Lt('s01_04') && t < Lt('s01_06')) { jump = Math.abs(Math.sin((t - Lt('s01_04')) * 5)) * 60; hp.mouth = 1; hp.brow = -.3; const G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = POSE.stretch(1, G); }
  hp.jump = jump;
  if (t > Lt('s01_06')) { hp.jump = 0; hp.mouth = -.2; hp.brow = .6; hp.hL = null; const G = charGeom(CAST.tu, hp); hp.hR = POSE.wave(t, G)[1]; hp.look = [16, 4]; }
  st.inv(g => drawChar(g, 'tu', hp));
  // passers-by walk past right in front of you, as if the spot were empty (drawn in front, so the glass never bends their faces)
  st.fg(g => { walker(g, 'ex2', 2100, -150, t, { look: [-10, 4] }); walker(g, 'ex5', -300, 120, Math.max(0, t - 6), { look: [10, 4] }); });
  if (t > Lt('s01_06')) st.fg(g => walker(g, 'ex3', 1700, -170, t - Lt('s01_06'), { look: [-12, 6], mouth: .2 }));
  composeI(X, st, { inv: 1, t });
  [['TU MAMÁ', .02], ['LAS CÁMARAS', .3], ['EL ESPEJO', .62]].forEach(([s, f], i) => crossSticker(X, s, vis(t, Lm('s01_02', f), Lt('s01_03') - .1, .12), 90, 90 + i * 112));
  if (t > Lt('s01_03') + .5) sticker(X, 'LA ROPA TAMBIÉN', vis(t, Lt('s01_03') + .5, Lt('s01_04') - .1, .15), 90, 90, 64, '#ffffff');
  if (t > Lm('s01_03', .55)) sticker(X, 'NO HAY MANUAL', vis(t, Lm('s01_03', .55), Lt('s01_04') - .1, .15), 90, 210, 64);
  if (t > Lt('s01_06') + .6) comicWord(X, '…', ...worldToScreen(cam, hx + 60, 300), t - Lt('s01_06') - .6, 90, '#ffffff', 1.2);
};

/* ================================================================ 2. title card */
SC.s02 = (X, t) => {
  const cam = { cx: 960, cy: 540, z: 1.0 }, st = stageI(cam); st.wld(g => { drawSet(g, 'park'); bench(g, 0); bench(g, 1); });
  st.wld(g => pepeWatch(g, 1500, 800, .55, 700, t));
  const hp = ghost(standing(700, { t, look: [10, 6], mouth: .6 })); const G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = POSE.wave(t, G);
  st.inv(g => drawChar(g, 'tu', hp));
  composeI(X, st, { inv: 1, t });
  titleCard(X, '¿QUÉ PASARÍA SI', 'FUERAS INVISIBLE?', R(t, .3, .8, outC), t);
};

/* ================================================================ 3. Monday: nobody in the mirror */
function towel(g, x, y, rot = 0) { g.save(); g.translate(x, y); g.rotate(rot); shape(g, q => rrPath(q, -46, 0, 92, 150, 10), '#e07a8a', 4);
  for (const yy of [110, 126]) shape(g, q => q.rect(-46, yy, 92, 8), '#ffffff', 0); g.restore(); }
SC.s03 = (X, t) => {
  const mir = Lt('s03_02') - .05, wave = Lt('s03_04') - .05, catIn = Lt('s03_07') - .05, bump = Lm('s03_07', .8);
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 540, z: 1.0, z2: 1.04, lock: 1 },
    { t: mir, cx: 960, cy: 330, z: 2.0, z2: 2.15, lock: 1 },                // the mirror: empty
    { t: Lt('s03_03') - .05, cx: 960, cy: 470, z: 2.3, z2: 2.4, lock: 1 },  // you, very close
    { t: wave, cx: 960, cy: 330, z: 2.0, z2: 2.05, lock: 1 },
    { t: Lm('s03_04', .5), cx: 960, cy: 470, z: 2.4, z2: 2.5, lock: 1 },
    { t: Lt('s03_05') - .05, cx: 960, cy: 540, z: 1.1, z2: 1.15, lock: 1 },
    { t: catIn, cx: 900, cy: 700, z: 1.5, z2: 1.55, lock: 1 },
    { t: Lt('s03_08') - .05, cx: 1000, cy: 820, z: 2.6, z2: 2.75, lock: 1 },
  ]);
  const mirrorShot = (t >= mir && t < Lt('s03_03') - .05) || (t >= wave && t < Lm('s03_04', .5));
  const st = stageI(cam); st.wld(g => drawSet(g, 'bathroom'));
  const hp = ghost(standing(960, { t, look: [0, 4], mouth: .2, lid: t < mir ? .45 : 0 }));
  if (t < mir) { const G = charGeom(CAST.tu, hp); const u = Math.sin(t * 7); hp.hL = [-70, G.top + 120 + u * 20]; hp.hR = [70, G.top + 120 - u * 20]; }   // splashing water on the face
  if (t > Lt('s03_03') - .05) { hp.wide = .7; hp.brow = .9; hp.mouth = -.3; hp.lid = 0; }
  if (speaking(t, 's03_03')) hp.open = talk(t, 's03_03');
  if (t > wave && t < Lt('s03_05')) { const G = charGeom(CAST.tu, hp); hp.hR = POSE.wave(t, G)[1]; if (t > Lm('s03_04', .5)) { hp.open = .9; hp.hR = null; } }
  if (t > Lt('s03_05')) { hp.wide = .2; hp.brow = .5; hp.mouth = -.2; hp.look = [10, -8]; }
  if (t > catIn) { hp.look = [-6, 18]; hp.brow = .4; }
  // the towel he holds is the only thing in the mirror
  const towelOn = t > mir - .6 && t < Lt('s03_05');
  if (towelOn && !mirrorShot) { hp.hR = hp.hR || [120, -360]; hp.holdR = floatHold(st, (g, x, y) => towel(g, x - 10, y - 30, .1)); }
  if (mirrorShot) st.wld(g => { // reflection: the room behind, and only the towel
    g.save(); g.beginPath(); rrPath(g, 712, 100, 496, 430, 10); g.clip(); g.fillStyle = 'rgba(215,240,246,.55)'; g.fillRect(700, 90, 520, 450);
    if (towelOn) towel(g, 1010 + Math.sin(t * 2) * 8, 300 + Math.sin(t * 1.3) * 6, -.1);
    if (t > wave && t < Lm('s03_04', .5)) text(g, '…', 960, 330, 90, '#7a9aa6', 'Bangers', 'center');
    g.restore(); });
  else st.inv(g => drawChar(g, 'tu', hp));
  // Croqueta: walks in, bumps into your leg, looks up at nothing
  if (t > catIn) { if (t < bump) { const x = mix(1900, 1040, R(t, catIn, bump, lin)); st.wld(g => drawSpr(g, 'catWalk', x, 960, 150, { flip: 1, bob: -Math.abs(Math.sin(t * 10)) * 5 })); }
    else st.wld(g => drawAnimal(g, 'croqueta', 1060, 965, .8, { head: t > Lt('s03_08') ? 'bored' : 'wide', t, flip: -1, tilt: t > Lt('s03_08') ? -.35 : -.1 })); }
  composeI(X, st, { inv: 1, t });
  if (mirrorShot && t > mir) sticker(X, 'ESPEJO: 0 PERSONAS', R(t, mir + .2, mir + .4, back), 70, 70, 60, '#ffffff');
  if (t > bump && t < bump + .8) comicWord(X, '¡TOC!', ...worldToScreen(cam, 1000, 820), t - bump, 80);
  // the memory: Pepe, last night
  if (t > Lt('s03_05') && t < catIn) { const a = R(t, Lt('s03_05'), Lt('s03_05') + .3, outC) * (1 - R(t, catIn - .3, catIn));
    panel(X, 1000, 120, 820, a, g => { drawSet(g, 'parkNight'); bench(g, 0); bench(g, 1); pigeonTalk(g, 1080, 792, .62, { flip: -1, front: 1, open: Math.abs(Math.sin(t * 9)) * .6 }); nightTint(g, .3); }, .02, { cx: 1080, cy: 720, z: 3.2 });
    sticker(X, '«MAÑANA, NADIE TE VA A VER»', R(t, Lt('s03_05') + .4, Lt('s03_05') + .7, back) * (1 - R(t, catIn - .3, catIn)), 1000, 640, 52, '#ffffff'); }
  if (speaking(t, 's03_03') || (t > Lt('s03_03') && t < Le('s03_03') + .4)) voiceBubble(X, cam, t, 's03_03', mouthPt('tu', hp), { dx: 1, r: 90 });
};

/* ================================================================ 4. breakfast: a plate for an empty chair, a floating toast */
SC.s04 = (X, t) => {
  const rule = Lt('s04_08') - .2, grab = Lt('s04_04') + .2, turn = Lt('s04_05') - .05, catIn = Lt('s04_06') - .4;
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 540, z: 1.0, z2: 1.04, lock: 1 },
    { t: Lt('s04_02') - .05, cx: 900, cy: 640, z: 1.6, z2: 1.7, lock: 1 },
    { t: Lt('s04_03') - .05, cx: 1220, cy: 470, z: 2.0, z2: 2.1, lock: 1 },
    { t: Lt('s04_04') - .05, cx: 860, cy: 560, z: 2.0, z2: 2.15, lock: 1 },
    { t: turn, cx: 1000, cy: 560, z: 1.3, z2: 1.35, lock: 1 },
    { t: Lt('s04_06') - .05, cx: 900, cy: 700, z: 2.2, z2: 2.3, lock: 1 },
    { t: Lt('s04_07') - .05, cx: 1100, cy: 520, z: 1.6, z2: 1.7, lock: 1 },
    { t: rule, cx: 960, cy: 540, z: 1.0, lock: 1 },
  ]);
  const st = stageI(cam); st.wld(g => { drawSet(g, 'kitchen'); chairBack(g, 860); });
  st.wld(g => pepeWatch(g, 1560, 420, .4, 860, t));   // on the window sill, watching you
  // mom: calls, brings the plate, looks at the empty chair, turns away, turns back
  const mx = t < Lt('s04_02') ? 1500 : mix(1500, 1200, R(t, Lt('s04_02'), Lt('s04_02') + 1, io));
  const mp = standing(mx, { t, flip: -1, look: [-12, 4], mouth: .2, walk: t > Lt('s04_02') && t < Lt('s04_02') + 1 ? 1 : 0, phase: walkPh(mx) });
  if (speaking(t, 's04_01')) { mp.open = talk(t, 's04_01'); mp.look = [-14, -6]; mp.hL = [-100, -470]; }
  if (t < Lt('s04_02') + .9 && t > Lt('s04_02') - .5) { mp.hR = [150, -380]; mp.holdR = (g, x, y) => { plate(g, x + 10, y - 10, .9); drawSpr(g, 'toast', x + 10, y - 16, 56); }; }
  if (t > Lt('s04_03') - .1 && t < turn) { mp.look = [-16, 14]; mp.brow = .7; const G = charGeom(CAST.mama, mp); [mp.hL, mp.hR] = POSE.hips(G); }
  if (speaking(t, 's04_03')) { mp.open = talk(t, 's04_03'); mp.brow = .9; }
  const away = t > turn - .6 && t < turn + .2; if (away) { mp.flip = 1; mp.look = [12, 0]; }
  if (t > turn + .2) { mp.flip = -1; mp.look = [-16, 14]; mp.wide = .6; mp.brow = .8; }
  if (speaking(t, 's04_07')) { mp.open = talk(t, 's04_07'); mp.look = [-16, 18]; mp.brow = 1; const G = charGeom(CAST.mama, mp); mp.hR = POSE.point(1, G, -1)[1]; mp.hR = [-230, G.top + 120]; }
  st.wld(g => drawChar(g, 'mama', mp));
  // you, sitting behind the table; the toast floats from the plate to your mouth, bite by bite
  const hp = ghost({ x: 860, y: 905, s: S0, sit: 1, t, look: [10, 10], mouth: .2 });
  if (t > Lt('s04_03') - .1 && t < grab) { hp.look = [16, 2]; hp.brow = .6; hp.mouth = -.2; }
  const toastLeft = 1 - R(t, grab + .6, turn - .4, lin);
  if (t > grab && t < turn - .3) { hp.hR = [110, -470]; hp.mouth = .6 + Math.abs(Math.sin(t * 9)) * .4; hp.look = [6, 4];
    hp.holdR = floatHold(st, (g, x, y) => { g.save(); g.beginPath(); g.rect(x - 60, y - 80 + 80 * (1 - toastLeft), 140, 120); g.clip(); drawSpr(g, 'toast', x + 14, y + 30, 66, { rot: -.2 }); g.restore(); }); }
  if (t > turn - .3) { hp.look = [14, 4]; hp.mouth = .5; hp.lid = .3; }
  if (t > Lt('s04_07')) { hp.sweat = 1; hp.mouth = -.2; }
  st.inv(g => drawChar(g, 'tu', hp));
  st.fg(g => { kitchenTable(g); if (t > Lt('s04_02') + .7) { plate(g, 860, 784); if (t < grab) drawSpr(g, 'toast', 860, 786, 52); else if (t > turn - .5) crumbs(g, 860, 778); } });
  // Croqueta: strolls in and sits by the plate, licking his lips
  if (t > catIn) { if (t < Lt('s04_06') + .4) st.wld(g => drawSpr(g, 'catWalk', mix(1950, 1040, R(t, catIn, Lt('s04_06') + .4, lin)), 960, 150, { flip: 1, bob: -Math.abs(Math.sin(t * 10)) * 5 }));
    else st.fg(g => drawAnimal(g, 'croqueta', 1040, 778, .7, { head: t > Lt('s04_07') ? 'wide' : 'bored', t, flip: -1, tilt: t > Lt('s04_07') ? .25 : -.05 })); }
  composeI(X, st, { inv: 1, t });
  if (t > Lt('s04_02') + .8 && t < Lt('s04_04')) { const [x, y] = worldToScreen(cam, 860, 470); X.save(); X.globalAlpha = vis(t, Lt('s04_02') + .8, Lt('s04_04') - .2); text(X, 'SILLA «VACÍA»', x, y - 120, 56, '#ffffff', 'Bangers', 'center', OUT, 8); X.restore(); }
  if (t > turn + .2 && t < turn + 1) comicWord(X, '¿?', ...worldToScreen(cam, 1180, 260), t - turn - .2, 90);
  ruleCard(X, 1, 'NADIE TE VE. PERO SÍ TE PUEDEN OÍR.', t > Lt('s04_09') - .1 ? 'Y LO QUE AGARRAS… FLOTA.' : '', R(t, rule, rule + .4, outC));
};

/* ================================================================ 5. Nacho's conscience: thirty-seven tacos */
SC.s05 = (X, t) => {
  const lock = Lt('s05_08') - .05;
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 540, z: 1.0, z2: 1.05, lock: 1 },
    { t: Lt('s05_02') - .05, cx: 1060, cy: 470, z: 1.8, z2: 1.9, lock: 1 },
    { t: Lt('s05_03') - .05, cx: 980, cy: 460, z: 2.1, z2: 2.2, lock: 1 },
    { t: Lt('s05_04') - .05, cx: 1080, cy: 450, z: 2.4, z2: 2.55, lock: 1 },
    { t: Lt('s05_05') - .05, cx: 1000, cy: 500, z: 1.6, z2: 1.7, lock: 1 },
    { t: Lt('s05_07') - .05, cx: 1080, cy: 520, z: 2.0, z2: 2.1, lock: 1 },
    { t: lock, cx: 960, cy: 540, z: 1.25, z2: 1.3, lock: 1, w: 2600 },
    { t: Lt('s05_09') - .05, cx: 1300, cy: 600, z: 2.6, z2: 2.75, lock: 1, w: 2600 },
  ]);
  const st = stageI(cam);
  if (t < lock) {
    st.wld(g => drawSet(g, 'street'));
    st.wld(g => pepeWatch(g, 1700, 520, .42, 940, t));
    const walkEnd = Lt('s05_03') - .2, nx = mix(700, 1120, R(t, 0, walkEnd, io));
    const np = { x: nx, y: FEET, s: S0, t, walk: t < walkEnd ? 1 : 0, phase: walkPh(nx), look: [12, 4], mouth: .3 };
    if (t > Lt('s05_03')) { np.look = [-6, -6]; np.wide = .8; np.brow = .9; np.mouth = -.3; np.sweat = 1; }
    if (speaking(t, 's05_04')) { np.open = talk(t, 's05_04'); np.look = [-16, -4 + Math.sin(t * 9) * 6]; np.flip = Math.sin(t * 5) > 0 ? 1 : -1; }
    if (t > Lt('s05_05')) { np.look = [8, -12]; np.wide = .9; np.brow = 1; np.mouth = -.4; np.hL = [-110, -540]; np.hR = [110, -540]; np.flip = 1; }
    if (speaking(t, 's05_07') || t > Le('s05_07')) { np.open = speaking(t, 's05_07') ? talk(t, 's05_07') : 0; np.mouth = .5; np.wide = .5; np.brow = .3; np.hL = [-60, -420]; np.hR = [60, -420]; np.hy = 20; }
    const hx = nx - 230 + 60 * R(t, Lt('s05_03') - .6, Lt('s05_03'), io), hp = ghost({ x: hx, y: FEET, s: S0, t, walk: t < walkEnd + .4 ? 1 : 0, phase: walkPh(hx), look: [14, 2], mouth: .5, lean: t > Lt('s05_03') - .2 ? .12 : 0 });
    if (t > Lt('s05_03') - .2) { const G = charGeom(CAST.tu, hp); hp.hR = [120, G.top + 40]; hp.hL = [-90, G.top + 200]; hp.mouth = .8; hp.lid = .3; }
    for (const id of ['s05_03', 's05_05', 's05_06']) if (speaking(t, id)) hp.open = talk(t, id) * .6;
    st.inv(g => drawChar(g, 'tu', hp)); st.fg(g => drawChar(g, 'nacho', np));   // you whisper from behind him
    composeI(X, st, { inv: 1, t });
    if (t > Lt('s05_02') - .05 && t < Lt('s05_03') - .1) bigCounter(X, 'NACHO TE DEBE:', '37 TACOS', R(t, Lt('s05_02'), Lt('s05_02') + .25, outC));
    for (const id of ['s05_03', 's05_05', 's05_06']) voiceBubble(X, cam, t, id, mouthPt('tu', hp), { dx: -1, r: 90, w: 560 });
    if (t > Lt('s05_04') && t < Lt('s05_05')) comicWord(X, '¡¿?!', ...worldToScreen(cam, 1180, 220), t - Lt('s05_04'), 90);
  } else {
    // that afternoon: an open locker, a tray of tacos, a note
    st.wld(g => { drawSet(g, 'hallway'); const x0 = 1180, y0 = 470;
      shape(g, q => q.rect(x0, y0, 150, 380), '#2b2f3a', 5);   // open locker
      shape(g, q => { q.moveTo(x0 + 150, y0); q.lineTo(x0 + 250, y0 - 30); q.lineTo(x0 + 250, y0 + 410); q.lineTo(x0 + 150, y0 + 380); q.closePath(); }, '#5d86b8', 5);
      shape(g, q => q.rect(x0 + 6, y0 + 200, 138, 10), '#7b8794', 3);
      drawSpr(g, 'tacos', x0 + 75, y0 + 200, 70);
      g.save(); g.translate(x0 + 92, y0 + 112); g.rotate(-.06 + Math.sin(t * 2) * .02); shape(g, q => q.rect(-58, -48, 116, 96), '#ffe66d', 4); text(g, 'PERDÓN', 0, 10, 34, '#2a2a2a', 'ComicNeue', 'center'); g.restore(); });
    st.inv(g => drawChar(g, 'tu', ghost(standing(980, { t, look: [16, 8], mouth: 1, brow: -.2 }))));
    composeI(X, st, { inv: 1, t });
    bigCounter(X, 'TACOS RECUPERADOS:', '37', R(t, lock + .3, lock + .6, outC));
  }
};
