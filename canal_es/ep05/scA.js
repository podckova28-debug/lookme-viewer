/* Ep05 «¿Qué pasaría si tuvieras 500 de IQ?» — shared helpers and scenes 0–5.
   Beats are keyed to narration (Lt/Le/Lm from anim/episode.js). The genius look is anim/genio.js: while the hero thinks the world
   turns into a blueprint (hero in colour, st.col), chalk notes draw themselves, the IQ 500 badge sits top right. */
SC.missing = (X, t) => { X.fillStyle = '#1b1530'; X.fillRect(0, 0, W, H); text(X, SID + ' (sin animar)', W / 2, H / 2, 90, '#fde047', 'Bangers', 'center'); };
const CHANNEL_NAME = 'PONLE QUE…';
const vis = (t, a, b, fi = .25, fo = .3) => R(t, a, a + fi) * (1 - R(t, b, b + fo));
const loopU = (t, t0, P) => (((t - t0) % P) + P) % P / P;
function standing(x, extra = {}) { return Object.assign({ x, y: FEET, s: S0 }, extra); }
function seated(x, extra = {}) { return Object.assign({ x, y: 905, s: S0, sit: 1, noShadow: 1 }, extra); }
function benchSit(x, extra = {}) { return Object.assign({ x, y: 905, s: S0, sit: 1, noShadow: 1, hL: [-80, -125], hR: [80, -125], armsFront: 1 }, extra); }
function walker(g, n, x0, v, tt, extra = {}) { const x = x0 + v * tt; drawChar(g, n, Object.assign({ x, y: FEET, s: S0, t: tt, walk: 1, phase: walkPh(x), flip: v < 0 ? -1 : 1 }, extra)); return x; }
/* lip sync for whichever of the ids is being spoken */
function say(p, t, ids) { for (const id of ids) if (T().L[id] && speaking(t, id)) { p.open = talk(t, id); return true; } return false; }
/* world points of a character: mouth, top of the head */
function mouthPt(cname, p) { const c = CAST[cname], G = charGeom(c, p), S = (p.s || 1) * (c.s || 1); return [p.x + ((p.hx || 0) + (p.look ? p.look[0] : 0)) * S * (p.flip || 1), p.y + (G.top - 70 + (p.hy || 0)) * S]; }
function headPt(cname, p, dy = 0) { const c = CAST[cname], G = charGeom(c, p), S = (p.s || 1) * (c.s || 1); return [p.x + (p.hx || 0) * S * (p.flip || 1), p.y + (G.top - 100 - c.r * 1.1 + (p.hy || 0) + dy) * S]; }
function rewindFX(X, k, t) { if (k <= 0) return;
  X.save(); X.globalAlpha = .25 * k; X.fillStyle = '#ffffff'; const r = rnd(Math.floor(t * 30));
  for (let i = 0; i < 9; i++) { const y = r() * H, h = 4 + r() * 18; X.fillRect(0, y, W, h); } X.restore();
  X.save(); X.globalAlpha = .55 * k; X.fillStyle = '#0d0b12'; X.fillRect(0, H - 150, W, 150); X.restore();
  X.save(); X.globalAlpha = k; text(X, '◀◀  REBOBINANDO', 70, H - 52, 76, '#ffffff', 'Bangers', 'left', OUT, 10); X.restore(); }
function nightTint(X, a = 1) { X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.globalCompositeOperation = 'multiply'; X.fillStyle = `rgba(60,70,140,${.55 * a})`; X.fillRect(0, 0, W, H); X.restore(); }
function dashRing(X, x, y, r, t, col = '#ffd34d') { X.save(); X.strokeStyle = col; X.lineWidth = 8; X.setLineDash([22, 16]); X.lineDashOffset = -t * 60; X.beginPath(); X.arc(x, y, r, 0, 7); X.stroke(); X.restore(); }
function cooBubble(X, cam, wx, wy, t, t0, d, s = 'RUU') { const a = R(t, t0, t0 + .15, back) * (1 - R(t, t0 + d, t0 + d + .2)); if (a <= 0) return; const [x, y] = worldToScreen(cam, wx, wy); bubble(X, s, x, y - 20, a, 56); }
function pepeWatch(g, x, y, s, hx, t, extra = {}) { drawPigeon(g, x, y, s, Object.assign({ flip: hx < x ? -1 : 1, tilt: Math.sin(t * .9) * .06 }, extra)); }
function tears(g, x, y, t, a = 1) { if (a <= 0) return; for (let i = 0; i < 6; i++) { const u = loopU(t, i * .17, 1), xx = x + (i % 2 ? 62 : 0), yy = y + u * 240; g.save(); g.globalAlpha = (1 - u) * a;
  shape(g, q => { q.moveTo(xx, yy - 14); q.quadraticCurveTo(xx + 9, yy, xx, yy + 8); q.quadraticCurveTo(xx - 9, yy, xx, yy - 14); }, '#7cc8ff', 2); g.restore(); } }
function tissue(g, x, y) { shape(g, k => k.ellipse(x + 4, y - 20, 34, 26, .3, 0, 7), '#ffffff', 3); }
function pencil(g, x, y, rot = -.6) { g.save(); g.translate(x, y); g.rotate(rot); shape(g, q => q.rect(-6, -70, 12, 64), '#f2c230', 3); shape(g, q => { q.moveTo(-6, -6); q.lineTo(6, -6); q.lineTo(0, 12); q.closePath(); }, '#f1d9b0', 3); shape(g, q => q.rect(-6, -82, 12, 12), '#e88aa0', 3); g.restore(); }
function genius(X, st, gm, t, notes, busy = 0) { composeG(X, st, gm); chalk(X, st.cam, t, gm.a, notes || []); iqBadge(X, gm.a, t, busy); }
/* a memory in a thought cloud: (wx, wy) world point of the remembered scene at the cloud's centre, k its zoom */
function memCloud(X, x, y, r, a, wx, wy, k, draw, from) { if (a <= 0) return; const P = layer('MEM'), zc = window.__camz; window.__camz = k;
  P.setTransform(k, 0, 0, k, x - wx * k, y - wy * k); draw(P); P.setTransform(1, 0, 0, 1, 0, 0); window.__camz = zc;
  X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.globalAlpha = clamp(a); const s = .85 + .15 * back(a);
  if (from) for (let i = 0; i < 3; i++) { const u = (i + 1) / 4; shape(X, q => q.arc(mix(from[0], x, u * .7), mix(from[1], y + r * .8, u * .7), 12 + i * 8, 0, 7), '#ffffff', 5); }
  X.translate(x, y); X.scale(s, s); X.beginPath(); for (let i = 0; i < 12; i++) { const an = i / 12 * Math.PI * 2; X.arc(Math.cos(an) * r * .86, Math.sin(an) * r * .62, r * .32, 0, 7); } X.closePath();
  X.fillStyle = '#ffffff'; X.fill(); X.lineWidth = 8; X.strokeStyle = '#141014'; X.stroke();
  X.save(); X.beginPath(); X.ellipse(0, 0, r * .95, r * .68, 0, 0, 7); X.clip(); X.filter = 'sepia(.35)'; X.drawImage(P.canvas, -x, -y); X.restore();
  X.restore(); }
/* a rule card in the episode's own colours */
const ruleAt = (t, id, lines) => { const a = R(t, Lt(id) - .1, Lt(id) + .3, outC) * (1 - R(t, Le(id) + .4, Le(id) + .7)); return a; };

/* ---------------------------------------------------------------- the classroom on Friday (s00, s12, s13)
   the whiteboard spans x 330..1180, y 115..576; the door is drawn on the left wall; your desk at 860, the profe at 1470 */
const BOARD = { x0: 330, x1: 1180, y0: 115, y1: 576 };
function classDoor(g, open = 0) { shape(g, q => q.rect(40, 300, 250, 640), '#7a4f30', 5); shape(g, q => q.rect(58, 318, 214, 622), '#3a2618', 0);
  g.save(); g.translate(58, 318); g.scale(1 - .55 * open, 1); shape(g, q => rrPath(q, 0, 0, 214, 622, 6), '#c08451', 5); shape(g, q => rrPath(q, 40, 60, 134, 150, 6), '#cfe8f6', 4);
  circ(g, 186, 330, 12, '#e9c46a', 4); g.restore(); }
function boardProblem(g, t, solved = 1) {   // keep it above y≈420: seated heads cover the lower half of the board
  const ink = '#3a6fb0', red = '#c0262d', green = '#2f8f4e', x = 380;
  g.save(); g.font = 'bold 40px ComicNeue'; g.textAlign = 'left';
  g.fillStyle = red; g.fillText('PROBLEMA SIN RESOLVER · DESDE 1725', x, 205);
  g.fillStyle = ink; g.font = 'bold 44px ComicNeue';
  g.fillText('Σ (n² + 1) / n!  =  ?', x, 268); g.fillText('∫ e^(−x²) dx · ζ(3) …', x, 328); g.fillText('⇒  x³ + y³ ≠ z³ ?', 820, 268);
  if (solved > 0) { g.globalAlpha = clamp(solved); g.fillStyle = green; g.font = 'bold 46px ComicNeue'; g.fillText('= 2π · 7/3   Q.E.D.', 820, 328);
    g.save(); g.translate(1050, 400); g.rotate(-.1); g.strokeStyle = green; g.lineWidth = 8; g.strokeRect(-115, -46, 230, 84); g.font = '56px Bangers'; g.textAlign = 'center'; g.fillText('¡RESUELTO!', 0, 16); g.restore(); }
  g.restore(); }
function classroomSet(g, t, solved = 1, door = 0) { drawSet(g, 'classroom'); classDoor(g, door); boardProblem(g, t, solved); }
/* everybody in the classroom on Friday; o: { solved, renata (0..1 in the doorway), hp, pp, rp } */
function classroomFriday(st, t, o) {
  st.wld(g => classroomSet(g, t, o.solved, o.door || 0));
  if (o.rp) st.wld(g => drawChar(g, 'valeria', o.rp));
  st.wld(g => { drawChar(g, 'ex2', seated(1190, { t, look: [-14, 6], mouth: .1, hL: [-70, -170], hR: [70, -170] })); desk(g, 1190, FEET, .8); });
  st.wld(g => { drawChar(g, 'profe', o.pp); if (o.pp.cry) tears(g, o.pp.x - 34, 470, t, o.pp.cry); });
  st.wld(g => teacherDesk(g, 1620));
  st.col(g => drawChar(g, 'tu', o.hp)); st.wld(g => { desk(g, 860, FEET, .8); drawSpr(g, 'notebook', 880, 730, 54, { rot: .05 }); });
}

/* ================================================================ 0. cold open: Friday 3 p.m., the easiest question in the world */
SC.s00 = (X, t) => {
  const rw = Lm('s00_07', .45), think = Lt('s00_05') - .1;
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 540, z: 1.0, z2: 1.05, lock: 1 },
    { t: Lt('s00_02') - .05, cx: 1440, cy: 470, z: 2.3, z2: 2.4, lock: 1 },
    { t: Lt('s00_03') - .05, cx: 560, cy: 600, z: 1.35, z2: 1.42, lock: 1 },
    { t: Lt('s00_04') - .05, cx: 330, cy: 520, z: 2.3, z2: 2.4, lock: 1 },
    { t: think, cx: 660, cy: 520, z: 1.6, z2: 1.66, lock: 1 },
    { t: Lt('s00_06') - .05, cx: 860, cy: 480, z: 1.3, z2: 1.45, lock: 1 },
    { t: rw, cx: 960, cy: 540, z: 1.0, lock: 1 },
  ]);
  const st = stage(cam);
  const door = R(t, Lt('s00_03') - .3, Lt('s00_03') + .3);
  const pp = standing(1450, { t, flip: -1, look: [-10, 6], mouth: -.4, brow: 1, lid: .3, cry: 1, hR: [70, -420], holdR: tissue });
  const rp = standing(170, { t, look: [14, 4], mouth: .2, brow: -.2, blush: .3, hR: [40, -360] });
  if (t < Lt('s00_03') - .2) rp.x = -300;
  say(rp, t, ['s00_04']);
  const hp = seated(860, { t, look: [6, 2], mouth: .5, brow: -.3, hR: [90, -210], holdR: (g, x, y) => pencil(g, x, y), hL: [-70, -170] });
  if (t > Lt('s00_03')) { hp.look = [-16, 2]; hp.mouth = .2; }
  if (t > think) { hp.look = [-14, -4]; hp.mouth = -.1; hp.wide = .5; hp.brow = .2; }
  if (t > Lt('s00_06')) { hp.wide = 1; hp.mouth = -.4; hp.brow = 1; hp.sweat = 1; hp.look = [0, -6]; }
  classroomFriday(st, t, { solved: 1, door, hp, pp, rp });
  const gm = geniusState(t, [[think, 99]], cam, headPt('tu', hp, 60));
  const [hx, hy] = headPt('tu', hp);
  genius(X, st, gm, t, [
    { k: 'label', at: [880, 400], s: '«¿TIENES ALGO QUE', t0: think + .5, size: 40, out: Lt('s00_06') },
    { k: 'label', at: [880, 445], s: 'HACER EL SÁBADO?»', t0: think + .8, size: 40, out: Lt('s00_06') },
    { k: 'label', at: [880, 510], s: 'DIFICULTAD: 1/10', t0: think + 1.3, size: 40, col: GEN_YEL, out: Lt('s00_06') },
    { k: 'arrow', a: [560, 470], b: [300, 420], t0: think + .4, out: Lt('s00_06') },
    { k: 'label', at: [380, 530], s: 'RENATA', t0: think + .6, size: 40, out: Lt('s00_06') },
  ], t > Lt('s00_06') ? 1 : 0);
  const [sx, sy] = worldToScreen(cam, hx, hy);
  if (t > Lt('s00_06')) { const a = R(t, Lt('s00_06'), Lt('s00_06') + .3);
    storm(X, sx, sy + 40, t, Lt('s00_06') + .1, a * (1 - R(t, rw, rw + .3)), ['SÍ', 'NO', '¿POR QUÉ?', '¿QUÉ DÍA?', 'DEPENDE', 'CLARO', 'TENGO TAREA', '¿ES UNA CITA?', '¿A QUÉ HORA?', 'SÍ… DIGO, NO', '¿CON QUIÉN?', 'ME TENGO QUE IR'], 1, 4000, 3);
    calcBar(X, sx, sy - 180 * cam.z * .5, a, Math.min(12, (t - Lt('s00_06')) * 30), t > Lt('s00_06') + .5 ? 1 : 0, t);
    smoke(X, sx, sy - 10, t, R(t, Lm('s00_06', .4), Lm('s00_06', .6)), cam.z * .7); }
  sticker(X, 'VIERNES · 3:00 PM', vis(t, .3, Lt('s00_02') - .2), 70, 70, 64);
  if (t > Lt('s00_02') && t < Lt('s00_03') - .1) { const [x, y] = worldToScreen(cam, 1450, 300); X.save(); X.globalAlpha = vis(t, Lt('s00_02') + .2, Lt('s00_03') - .3); text(X, 'OTRA VEZ', x - 260, y, 70, '#ffffff', 'Bangers', 'center', OUT, 10); X.restore(); }
  if (t > rw) rewindFX(X, R(t, rw, rw + .2), t);
};

/* ================================================================ 1. the power: 500 IQ, the whole street is a maths problem */
function trafficLight(g, x, red = 1) { shape(g, q => q.rect(x - 9, 420, 18, 520), '#4a4f5a', 4); shape(g, q => rrPath(q, x - 44, 360, 88, 220, 18), '#2e333d', 5);
  [['#e0453c', red], ['#f2c230', 0], ['#4fbf6a', 1 - red]].forEach(([c, on], i) => { g.save(); if (on) { g.shadowColor = c; g.shadowBlur = 30; } circ(g, x, 400 + i * 66, 24, on ? c : '#1b1e24', 3); g.restore(); }); }
function streetCable(g) { g.save(); g.strokeStyle = '#2b2630'; g.lineWidth = 4; g.beginPath(); g.moveTo(-20, 150); g.quadraticCurveTo(960, 260, 1940, 140); g.stroke(); g.restore(); }
const cableY = x => { const u = (x + 20) / 1960; return (1 - u) * (1 - u) * 150 + 2 * u * (1 - u) * 260 + u * u * 140; };
const CABLE_P = [140, 260, 370, 520, 610, 760, 1080, 1190, 1320, 1460, 1720];
function leaf(g, x, y, rot) { g.save(); g.translate(x, y); g.rotate(rot); shape(g, q => { q.moveTo(-22, 0); q.quadraticCurveTo(0, -16, 22, 0); q.quadraticCurveTo(0, 16, -22, 0); }, '#6fae4a', 3); line(g, [[-20, 0], [20, 0]], '#4a7f30', 2); g.restore(); }
const LEAF = { a: [880, 430], b: [1030, 926] };
function leafAt(u) { return [mix(LEAF.a[0], LEAF.b[0], u) + Math.sin(u * 9) * 40 * (1 - u), mix(LEAF.a[1], LEAF.b[1], u)]; }
SC.s01 = (X, t) => {
  const on = Lm('s01_03', .3), off = Lm('s01_06', .6), q1 = Lt('s01_04'), q2 = Lm('s01_04', .36), q3 = Lm('s01_04', .68);
  const cam = shots(t, [], [
    { t: 0, cx: 760, cy: 560, z: 1.25, z2: 1.32, lock: 1 },
    { t: Lt('s01_02') - .05, cx: 960, cy: 540, z: 1.0, z2: 1.04, lock: 1 },
    { t: on - .1, cx: 760, cy: 520, z: 1.6, z2: 1.7, lock: 1 },
    { t: q1 - .05, cx: 1520, cy: 500, z: 1.8, z2: 1.9, lock: 1 },
    { t: q2 - .05, cx: 900, cy: 280, z: 1.7, z2: 1.75, lock: 1 },
    { t: q3 - .05, cx: 960, cy: 640, z: 1.45, z2: 1.5, lock: 1 },
    { t: Lt('s01_05') - .05, cx: 720, cy: 520, z: 1.9, z2: 2.0, lock: 1 },
    { t: Lt('s01_06') - .05, cx: 1080, cy: 300, z: 2.2, z2: 2.6, lock: 1 },
  ]);
  const st = stage(cam), lu = R(t, q3 + .3, q3 + 2.8, lin);
  st.wld(g => { drawSet(g, 'street'); streetCable(g); trafficLight(g, 1640, t < q1 + 2.6 ? 1 : 0);
    CABLE_P.forEach((x, i) => { const pepe = i === 6; drawPigeon(g, x, cableY(x) - 2, .26, { flip: i % 3 ? 1 : -1, tilt: Math.sin(t * 1.1 + i) * .08, peck: pepe ? 0 : Math.max(0, Math.sin(t * 1.7 + i * 2)) * .3 }); });
    if (lu < 1) leaf(g, ...leafAt(lu), Math.sin(t * 4) * .8); else leaf(g, LEAF.b[0], LEAF.b[1] - 6, .1); });
  const hp = standing(700, { t, look: [10, -2], mouth: .3 });
  if (t > on) { hp.look = [14, -10]; hp.mouth = .6; hp.brow = -.4; }
  if (t > Lt('s01_05')) { hp.look = [6, 0]; hp.mouth = .9; }
  if (t > Lt('s01_06')) { hp.look = [14, -14]; hp.mouth = -.1; hp.brow = .6; }
  st.col(g => drawChar(g, 'tu', hp));
  const gm = geniusState(t, [[on, off]], cam, headPt('tu', hp, 60));
  const pepeX = CABLE_P[6], pepeY = cableY(pepeX);
  genius(X, st, gm, t, [
    { k: 'box', at: [1640, 470], w: 140, h: 270, t0: q1 + .1 },
    { k: 'label', at: [1460, 330], s: 'VERDE EN 2,6 s', t0: q1 + .3, col: GEN_YEL },
    { k: 'arrow', a: [1480, 345], b: [1600, 390], t0: q1 + .5, d: .3 },
    ...CABLE_P.map((x, i) => ({ k: 'tick', at: [x, cableY(x) - 50], r: 12, t0: q2 + .1 + i * .07, d: .2 })),
    { k: 'label', at: [700, 120], s: '11 PALOMAS', t0: q2 + .9, size: 46, col: GEN_YEL },
    { k: 'arc', a: LEAF.a, b: LEAF.b, h: -60, t0: q3 + .1, d: .8, dash: 1, mark: 1 },
    { k: 'label', at: [1070, 880], s: 'AQUÍ, EN 2,5 s', t0: q3 + .7 },
    { k: 'label', at: [pepeX - 20, pepeY - 70], s: '?', t0: Lt('s01_06') + .3, size: 70, col: GEN_RED },
  ]);
  // the IQ scale (screen): 100 normal, 160 «Einstein, dicen», 500 you (off the scale)
  const sa = vis(t, Lt('s01_02') - .1, on);
  if (sa > 0) { X.save(); X.globalAlpha = sa; const x0 = 260, x1 = 1660, y = 860, px = v => mix(x0, x1, (v - 40) / 160);
    shape(X, q => rrPath(q, x0 - 60, y - 120, x1 - x0 + 120, 200, 18), 'rgba(13,11,18,.75)', 0); X.strokeStyle = '#ffffff'; X.lineWidth = 6; X.beginPath(); X.moveTo(x0, y); X.lineTo(x1, y); X.stroke();
    for (let v = 40; v <= 200; v += 20) { X.beginPath(); X.moveTo(px(v), y - 14); X.lineTo(px(v), y + 14); X.stroke(); text(X, String(v), px(v), y + 54, 34, '#cfd6e6', 'Bangers', 'center'); }
    const pin = (v, s, u, col) => { if (u <= 0) return; const k = back(u); X.save(); X.translate(px(v), y - 20); X.scale(k, k); shape(X, q => { q.moveTo(0, 0); q.lineTo(-16, -30); q.lineTo(16, -30); q.closePath(); }, col, 4); text(X, s, 0, -44, 44, col, 'Bangers', 'center', OUT, 8); X.restore(); };
    pin(100, '100 · NORMAL', R(t, Lt('s01_02') + .1, Lt('s01_02') + .4), '#ffffff'); pin(160, '160 · EINSTEIN (DICEN)', R(t, Lm('s01_02', .45), Lm('s01_02', .45) + .3), '#fde047');
    if (t > Lt('s01_03')) { const u = R(t, Lt('s01_03'), Lt('s01_03') + .5, inC); X.save(); X.translate(mix(px(160), x1 + 140, u), y - 40); text(X, 'TÚ: 500 →→→', 0, 0, 64, '#ff8f9a', 'Bangers', 'center', OUT, 10); X.restore(); }
    X.restore(); }
  sticker(X, 'IQ 500', vis(t, Lt('s01_01') + .2, Lt('s01_02') - .1), 70, 70, 80);
};

/* ================================================================ 2. title card */
SC.s02 = (X, t) => {
  const cam = { cx: 960, cy: 540, z: 1.0 }, st = stage(cam);
  st.wld(g => classroomSet(g, t, 1, 0));
  const hp = seated(860, { t, look: [0, -8], mouth: .7, brow: -.4 }); st.col(g => drawChar(g, 'tu', hp)); st.wld(g => desk(g, 860, FEET, .8));
  const gm = geniusState(t, [[-1, 99]], cam, headPt('tu', hp, 60));
  genius(X, st, gm, t, [{ k: 'circle', at: [860, 470], r: 170, t0: .2, d: .8 }, { k: 'arc', a: [600, 700], b: [1300, 700], h: 300, t0: .4, d: .9, dash: 1 }]);
  titleCard(X, '¿QUÉ PASARÍA SI', 'TUVIERAS 500 DE IQ?', R(t, .3, .8, outC), t);
};

/* ================================================================ 3. Monday: you open your eyes already thinking */
SC.s03 = (X, t) => {
  const on = Lt('s03_02') - .1, off = Lt('s03_05') - .1, ring = Lm('s03_02', .55), off2 = Lt('s03_06');
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 540, z: 1.0, z2: 1.06, lock: 1 },
    { t: on, cx: 940, cy: 620, z: 1.9, z2: 2.0, lock: 1 },
    { t: Lt('s03_03') - .05, cx: 680, cy: 600, z: 1.5, z2: 1.55, lock: 1 },
    { t: Lt('s03_04') - .05, cx: 520, cy: 680, z: 2.1, z2: 2.25, lock: 1 },
    { t: off, cx: 960, cy: 560, z: 1.7, z2: 1.75, lock: 1 },
    { t: Lt('s03_06') - .05, cx: 960, cy: 520, z: 1.2, z2: 1.3, lock: 1 },
    { t: Lt('s03_07') - .05, cx: 960, cy: 560, z: 1.9, z2: 2.0, lock: 1 },
  ]);
  const st = stage(cam), sitUp = R(t, .4, 1.2);
  st.wld(g => { drawSet(g, 'bedroom'); bedBack(g); nightstand(g); propAlarm(g, 1030, 740, .55, 7, 0, t > ring - .1 && t < ring + .35 ? 1 : 0); });
  st.wld(g => drawAnimal(g, 'croqueta', 480, 716, .8, { t, head: 'bored', tilt: Math.sin(t * .7) * .05 }));
  const hp = { x: 800, y: 945, s: S0, t, look: [0, 0], mouth: 0, lid: .5 * (1 - sitUp), hy: -30 * (1 - sitUp) };
  if (t > on) { hp.look = [16, 4]; hp.lid = 0; hp.wide = .2; }
  if (t > ring - .4 && t < ring + .6) { hp.hR = [290, -270]; }
  if (t > Lt('s03_03')) { hp.look = [-16, 6]; hp.brow = -.2; }
  if (t > off) { hp.look = [0, 0]; hp.wide = .8; hp.brow = .8; hp.mouth = -.2; hp.hL = [-70, -560]; hp.hR = [70, -560]; }
  if (t > Lt('s03_06')) { hp.wide = .2; hp.brow = .4; hp.hL = null; hp.hR = null; hp.look = [10, -10]; }
  if (t > Lt('s03_07')) { hp.mouth = .8; hp.brow = -.5; hp.look = [6, 0]; hp.wide = 0; }
  say(hp, t, ['s03_05']);
  st.col(g => drawChar(g, 'tu', hp)); st.wld(g => bedFront(g, .6));
  const gm = geniusState(t, [[on, off], [Lt('s03_07') + .1, 99]], cam, headPt('tu', hp, 60));
  genius(X, st, gm, t, [
    { k: 'circle', at: [1030, 700], r: 70, t0: on + .2, out: off },
    { k: 'label', at: [1000, 560], s: 'SUENA EN 3 s', t0: on + .4, out: off, col: GEN_YEL },
    { k: 'label', at: [1000, 610], s: '…LA APAGO EN 2', t0: on + 1.1, out: off },
    { k: 'box', at: [470, 640], w: 230, h: 170, t0: Lt('s03_03') + .3, out: off },
    { k: 'label', at: [360, 530], s: 'CROQUETA', t0: Lt('s03_03') + .5, out: off, size: 40, col: GEN_YEL },
    { k: 'label', at: [330, 780], s: '4,3 kg', t0: Lm('s03_04', .05), out: off, size: 38 },
    { k: 'label', at: [330, 830], s: '87% DORMIDO', t0: Lm('s03_04', .3), out: off, size: 38 },
    { k: 'label', at: [330, 880], s: '13% PLANEANDO ALGO', t0: Lm('s03_04', .65), out: off, size: 38, col: GEN_RED },
    { k: 'label', at: [1000, 380], s: 'ESTO ME GUSTA', t0: Lt('s03_07') + .4, col: GEN_YEL },
  ]);
  if (t > ring - .1 && t < ring + .5) comicWord(X, '¡CLIC!', ...worldToScreen(cam, 1030, 620), t - ring + .1, 80);
  if (t > Lt('s03_06') - .1 && t < Lt('s03_07') - .1) { const a = R(t, Lt('s03_06'), Lt('s03_06') + .35, outC) * (1 - R(t, Lt('s03_07') - .4, Lt('s03_07') - .1)), [hx2, hy2] = worldToScreen(cam, ...headPt('tu', hp));
    memCloud(X, 1340, 360, 330, a, 1060, 690, .95, g => { drawSet(g, 'parkNight'); bench(g, 0); bench(g, 1); pigeonTalk(g, 1080, 792, .62, { flip: -1, front: 1, open: t > Lm('s03_06', .3) ? Math.abs(Math.sin(t * 11)) * .5 : 0, tilt: Math.sin(t * 1.4) * .05 }); }, [hx2 + 60, hy2]);
    bubble(X, 'MAÑANA VAS A SER EL MÁS LISTO DEL MUNDO', 1100, 160, R(t, Lm('s03_06', .3), Lm('s03_06', .3) + .3, back), 46);
    if (t > Lm('s03_06', .8)) bubble(X, 'NO TE VA A GUSTAR', 1440, 690, R(t, Lm('s03_06', .8), Lm('s03_06', .8) + .3, back), 52); }
};

/* ================================================================ 4. the toaster: fixed with a spoon and a paper clip */
function toaster(g, x, y, s = 1, k = {}) { g.save(); g.translate(x, y); g.scale(s, s);
  shape(g, q => rrPath(q, -90, -110, 180, 110, 26), k.fixed ? '#d9dee6' : '#c4cad3', 5); shape(g, q => rrPath(q, -60, -122, 50, 18, 6), '#3a3f48', 3); shape(g, q => rrPath(q, 10, -122, 50, 18, 6), '#3a3f48', 3);
  shape(g, q => rrPath(q, 70, -70, 26, 14, 5), '#e0453c', 3); circ(g, -50, -40, 10, '#2e333d', 3);
  if (k.smoke) for (let i = 0; i < 3; i++) { const u = loopU(k.t || 0, i * .33, 1); g.save(); g.globalAlpha = (1 - u) * .7; circ(g, -20 + i * 20, -130 - u * 90, 14 + u * 16, '#9aa0aa', 3); g.restore(); }
  if (k.toast > 0) for (const dx of [-35, 35]) { g.save(); g.beginPath(); g.rect(-90, -400, 180, 280); g.clip(); drawSpr(g, 'toast', dx, -110 - k.toast * 70, 90, { rot: dx * .002 }); g.restore(); }
  g.restore(); }
function spoon(g, x, y, rot) { g.save(); g.translate(x, y); g.rotate(rot); shape(g, q => rrPath(q, -4, -60, 8, 60, 3), '#c8ccd4', 3); shape(g, q => q.ellipse(0, -72, 12, 18, 0, 0, 7), '#c8ccd4', 3); g.restore(); }
SC.s04 = (X, t) => {
  const on = Lt('s04_03') - .1, off = Le('s04_04') + .4, pop = Lm('s04_04', .75);
  const cam = shots(t, [], [
    { t: 0, cx: 1160, cy: 600, z: 1.5, z2: 1.55, lock: 1 },
    { t: Lt('s04_02') - .05, cx: 1120, cy: 620, z: 2.0, z2: 2.1, lock: 1 },
    { t: on, cx: 960, cy: 560, z: 1.35, z2: 1.4, lock: 1 },
    { t: Lt('s04_04') - .05, cx: 1080, cy: 660, z: 2.3, z2: 2.4, lock: 1 },
    { t: Lt('s04_05') - .05, cx: 1040, cy: 560, z: 1.6, z2: 1.65, lock: 1 },
    { t: Lt('s04_06') - .05, cx: 760, cy: 520, z: 2.2, z2: 2.3, lock: 1 },
    { t: Lt('s04_07') - .05, cx: 960, cy: 540, z: 1.0, z2: 1.05, lock: 1 },
    { t: Lt('s04_09') - .05, cx: 1500, cy: 760, z: 2.2, z2: 2.4, lock: 1 },
  ]);
  const st = stage(cam), fixed = t > Lm('s04_03', .7);
  st.wld(g => { drawSet(g, 'kitchen'); });
  // mamá at the counter hitting the toaster; you come in from the left
  const bang = !fixed && t < on ? Math.max(0, Math.sin(t * 9)) : 0;
  const mp = standing(1270, { t, flip: -1, look: [-14, 10], mouth: -.3, brow: .9, hR: [200, -260 - bang * 120], hL: [-90, -330] });
  if (t > on) { mp.look = [-16, 2]; mp.mouth = .1; mp.brow = .2; mp.hR = null; mp.hL = null; }
  if (t > pop) { mp.wide = .7; mp.mouth = .5; mp.brow = .6; }
  if (t > Lt('s04_05')) { mp.wide = .3; mp.brow = .9; mp.look = [-16, 4]; mp.mouth = -.1; }
  say(mp, t, ['s04_01', 's04_05']);
  st.wld(g => drawChar(g, 'mama', mp));
  const hx = mix(300, 820, R(t, Lt('s04_02') + .3, Lt('s04_02') + 1.8, io)), walking = t > Lt('s04_02') + .3 && t < Lt('s04_02') + 1.8;
  const hp = standing(hx, { t, walk: walking ? 1 : 0, phase: walkPh(hx), look: [14, 6], mouth: .2 });
  if (t > on) { hp.look = [16, 10]; hp.brow = -.3; hp.mouth = .4; }
  if (t > Lm('s04_03', .4) && t < Lt('s04_04')) { hp.hR = [260 + Math.sin(t * 14) * 10, -250]; hp.holdR = (g, x, y) => spoon(g, x, y, .6); hp.hL = [220, -240]; }
  if (t > Lt('s04_05')) { hp.look = [14, 2]; hp.mouth = .5; hp.brow = -.5; hp.hR = null; hp.hL = null; }
  if (t > Lt('s04_06')) { const G = charGeom(CAST.tu, hp); hp.hR = [60, G.top - 10]; hp.mouth = .6; hp.blush = .4; }
  if (t > Lt('s04_09')) { hp.look = [16, 12]; hp.brow = .6; hp.mouth = -.1; }
  say(hp, t, ['s04_06']);
  st.col(g => drawChar(g, 'tu', hp));
  st.wld(g => { kitchenTable(g); toaster(g, 1080, 800, 1, { fixed, smoke: !fixed, t, toast: t > pop ? R(t, pop, pop + .25, back) : 0 }); });
  st.wld(g => drawCat(g, 1560, 930, .7, { t }));
  const gm = geniusState(t, [[on, off]], cam, headPt('tu', hp, 60));
  genius(X, st, gm, t, [
    { k: 'box', at: [1080, 740], w: 230, h: 170, t0: on + .3, out: off },
    { k: 'arrow', a: [1260, 560], b: [1150, 680], t0: on + .5, out: Lt('s04_04') - .1 },
    { k: 'label', at: [1170, 540], s: 'RESORTE SUELTO', t0: on + .6, out: Lt('s04_04') - .1, size: 40 },
    { k: 'label', at: [1220, 620], s: '+ CUCHARA', t0: Lm('s04_03', .45), out: Lt('s04_04') - .1, size: 40, col: GEN_YEL },
    { k: 'label', at: [1220, 670], s: '+ CLIP', t0: Lm('s04_03', .6), out: Lt('s04_04') - .1, size: 40, col: GEN_YEL },
    { k: 'label', at: [1190, 560], s: 't = 2:14', t0: Lt('s04_04') + .5, out: off, size: 56, col: GEN_YEL },
    { k: 'label', at: [1190, 610], s: 'PAN PERFECTO', t0: Lm('s04_04', .5), out: off, size: 40 },
  ]);
  if (t > pop - .05 && t < pop + .6) comicWord(X, '¡TOC!', ...worldToScreen(cam, 1080, 600), t - pop + .05, 80);
  if (t > Lt('s04_07') - .1 && t < Lt('s04_09') - .1) ruleCard(X, 1, 'LO SABES TODO.', 'Y LO QUE NO, LO APRENDES LEYENDO', R(t, Lt('s04_07') + .1, Lt('s04_07') + .4, outC) * (1 - R(t, Lt('s04_09') - .4, Lt('s04_09') - .1)));
  if (t > Lt('s04_09') + .3) { const [x, y] = worldToScreen(cam, 1560, 760); X.save(); X.globalAlpha = R(t, Lt('s04_09') + .3, Lt('s04_09') + .6); text(X, '???', x, y, 110, '#ff8f9a', 'Bangers', 'center', OUT, 12); X.restore(); }
  if (t < on && bang > .9) comicWord(X, '¡PAF!', ...worldToScreen(cam, 1140, 640), .3, 72, '#ffffff', .6);
};

/* ================================================================ 5. don Chuy's jar: 1,342 beans */
function tacoStand(g, x) { shape(g, q => rrPath(q, x - 260, 640, 520, 300, 10), '#c96a3a', 6); shape(g, q => rrPath(q, x - 240, 660, 480, 60, 8), '#f2e3c4', 4);
  for (let i = 0; i < 8; i++) shape(g, q => { q.moveTo(x - 300 + i * 75, 380); q.lineTo(x - 225 + i * 75, 380); q.lineTo(x - 225 + i * 75, 450); q.quadraticCurveTo(x - 262 + i * 75, 480, x - 300 + i * 75, 450); q.closePath(); }, i % 2 ? '#ffffff' : '#e0453c', 4);
  shape(g, q => q.rect(x - 250, 450, 10, 200), '#7a4f30', 4); shape(g, q => q.rect(x + 240, 450, 10, 200), '#7a4f30', 4);
  shape(g, q => rrPath(q, x - 220, 300, 440, 84, 12), '#2f8f4e', 6); text(g, 'TACOS DON CHUY', x, 362, 56, '#ffffff', 'Bangers', 'center', OUT, 8); }
function beanJar(g, x, y, s = 1, n = 1) { g.save(); g.translate(x, y); g.scale(s, s);
  shape(g, q => rrPath(q, -70, -190, 140, 190, 24), 'rgba(220,240,255,.5)', 5);
  g.save(); g.beginPath(); g.rect(-64, -180 + 170 * (1 - n), 128, 176); g.clip(); const r = rnd(5);
  for (let i = 0; i < 90; i++) ell(g, -56 + r() * 112, -12 - r() * 166, 10, 6, r() * 3, i % 3 ? '#7a3b2a' : '#5a2a1e', 1.5); g.restore();
  shape(g, q => rrPath(q, -78, -214, 156, 30, 8), '#e0453c', 5); g.restore(); }
function contestSign(g, x, y) { shape(g, q => rrPath(q, x - 150, y - 90, 300, 180, 10), '#fffbe8', 5); text(g, 'CONCURSO', x, y - 34, 44, '#c0262d', 'Bangers', 'center'); text(g, '¿CUÁNTOS FRIJOLES?', x, y + 14, 34, '#141014', 'Bangers', 'center'); text(g, 'PREMIO: TACOS 1 AÑO', x, y + 58, 30, '#2f8f4e', 'Bangers', 'center'); }
SC.s05 = (X, t) => {
  const on = Lt('s05_04') - .1, off = Le('s05_05') + .3, later = Lt('s05_06') - .05;
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 560, z: 1.0, z2: 1.05, lock: 1 },
    { t: Lt('s05_02') - .05, cx: 1300, cy: 620, z: 2.0, z2: 2.1, lock: 1 },
    { t: Lt('s05_03') - .05, cx: 640, cy: 520, z: 2.1, z2: 2.2, lock: 1 },
    { t: on, cx: 1100, cy: 580, z: 1.6, z2: 1.7, lock: 1 },
    { t: Lt('s05_05') - .05, cx: 900, cy: 520, z: 2.2, z2: 2.3, lock: 1 },
    { t: later, cx: 1300, cy: 600, z: 1.7, z2: 1.8, lock: 1 },
    { t: Lt('s05_08') - .05, cx: 760, cy: 520, z: 1.7, z2: 1.8, lock: 1 },
  ]);
  const st = stage(cam), counted = t > Lt('s05_07') - .1, cnt = R(t, later + .4, Lt('s05_07') - .3, lin);
  st.wld(g => { drawSet(g, 'street'); tacoStand(g, 1350); contestSign(g, 1700, 560); });
  // don Chuy behind his counter (an apron over the tee), counting the beans one by one after the cut
  st.wld(g => { const dp = standing(1350, { t, look: [-6, 14], mouth: .2, hL: [-80, -330], hR: [80, -330] });
    if (t > later) { dp.look = [0, 18]; dp.lid = .4; dp.hR = [60 + Math.sin(t * 12) * 30, -340]; }
    if (counted) { dp.wide = .8; dp.lid = 0; dp.look = [-14, 0]; dp.mouth = .8; dp.open = .6; }
    dp.x = 1440; drawChar(g, 'ex3', dp); });
  st.wld(g => { shape(g, q => rrPath(q, 1080, 700, 540, 26, 8), '#9b6b45', 4); beanJar(g, 1180, 700, 1, 1 - .9 * cnt); if (t > later) { const r = rnd(9); for (let i = 0; i < Math.floor(cnt * 40); i++) ell(g, 1350 + r() * 220, 690 - r() * 30, 10, 6, r() * 3, '#7a3b2a', 1.5); } });
  const np = standing(560, { t, look: [14, 2], mouth: .5, s: S0 });
  if (t > Lt('s05_03') - .1 && t < Le('s05_03') + .4) { np.hR = [180, -560]; np.hL = [-180, -560]; np.brow = -.6; np.mouth = .9; }
  if (counted) { np.look = [14, -4]; np.wide = 1; np.mouth = .9; }
  if (t > Lt('s05_08') - .1) { np.look = [16, 0]; np.wide = 0; np.mouth = .8; np.brow = -.6; np.hR = [210, -380]; np.blush = .6; }
  say(np, t, ['s05_03', 's05_08']);
  st.wld(g => drawChar(g, 'nacho', np));
  const hp = standing(820, { t, look: [14, 4], mouth: .3 });
  if (t > on) { hp.look = [16, 8]; hp.brow = -.4; hp.mouth = .1; }
  if (t > Lt('s05_05')) { hp.look = [10, 0]; hp.mouth = .5; hp.brow = -.6; }
  if (counted) { hp.look = [-8, 0]; hp.mouth = .7; }
  say(hp, t, ['s05_05']);
  st.col(g => drawChar(g, 'tu', hp));
  const gm = geniusState(t, [[on, off]], cam, headPt('tu', hp, 60));
  genius(X, st, gm, t, [
    { k: 'dim', a: [1090, 510], b: [1090, 700], s: '19 cm', t0: on + .3, ox: -70, oy: 100 },
    { k: 'dim', a: [1108, 740], b: [1252, 740], s: 'Ø 14 cm', t0: on + .7, oy: 70 },
    { k: 'label', at: [1380, 470], s: 'V = 2,9 L', t0: Lm('s05_04', .35), col: GEN_YEL },
    { k: 'label', at: [1380, 530], s: 'FRIJOL = 1,4 cm³', t0: Lm('s05_04', .55), size: 38 },
    { k: 'label', at: [1380, 580], s: 'HUECOS: 36%', t0: Lm('s05_04', .75), size: 38 },
    { k: 'label', at: [1380, 660], s: '= 1342', t0: Lt('s05_05') - .1, size: 64, col: GEN_YEL, under: 1 },
  ]);
  if (t > later && t < Lt('s05_07') - .1) sticker(X, '3 HORAS DESPUÉS…', R(t, later, later + .3, back), 70, 70, 64);
  if (t > Lt('s05_06') + .4 && t < Lt('s05_07') - .1) { const [x, y] = worldToScreen(cam, 1480, 470); text(X, String(Math.floor(cnt * 1342)), x, y, 80, '#ffffff', 'Bangers', 'center', OUT, 10); }
  if (counted) { const a = R(t, Lt('s05_07'), Lt('s05_07') + .3, back), [x, y] = worldToScreen(cam, 1180, 430); X.save(); X.globalAlpha = clamp(a); X.translate(x, y); X.scale(a, a); X.rotate(-.08);
    shape(X, q => rrPath(q, -170, -70, 340, 120, 14), '#a7f3a0', 7); text(X, '1342 ✓', 0, 26, 86, '#141014', 'Bangers', 'center'); X.restore(); }
  if (t > Lt('s05_08') + .3) { const [x, y] = worldToScreen(cam, 700, 300); heartPopX(X, x, y, loopU(t, Lt('s05_08'), 1.1), 1.3); }
};
function heartPopX(g, x, y, u, s = 1) { if (u <= 0 || u >= 1) return; g.save(); g.globalAlpha = 1 - u * u; g.translate(x, y - u * 90); const k = s * (.6 + .4 * back(Math.min(1, u * 3))); g.scale(k, k);
  shape(g, q => { q.moveTo(0, 18); q.bezierCurveTo(-34, -6, -20, -34, 0, -16); q.bezierCurveTo(20, -34, 34, -6, 0, 18); }, '#ff5d7a', 4); g.restore(); }
