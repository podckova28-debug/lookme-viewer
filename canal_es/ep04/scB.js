/* Ep04 — scenes 6–11: roll call and the secret notebook, the week montage, Pepe sees you, machines, bumps, nobody waits */

/* ================================================================ 6. roll call: «¡Presente!» from an empty desk */
function notebookPage(X, a, t, t0s) { if (a <= 0) return; X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.globalAlpha = clamp(a);
  X.fillStyle = 'rgba(10,8,18,.55)'; X.fillRect(0, 0, W, H);
  const s = .85 + .15 * back(a); X.translate(W / 2, H / 2); X.rotate(-.02); X.scale(s, s);
  shape(X, q => rrPath(q, -620, -420, 1240, 840, 18), '#fbf6e6', 8);
  X.strokeStyle = 'rgba(80,140,200,.35)'; X.lineWidth = 3; for (let y = -300; y < 400; y += 92) { X.beginPath(); X.moveTo(-600, y); X.lineTo(600, y); X.stroke(); }
  X.strokeStyle = 'rgba(210,60,60,.55)'; X.beginPath(); X.moveTo(-470, -410); X.lineTo(-470, 410); X.stroke();
  for (let i = 0; i < 7; i++) circ(X, -585, -330 + i * 110, 14, '#2a2430', 0);
  text(X, 'EL DE LOS RIZOS', -430, -330, 64, '#c0262d', 'Bangers', 'left');
  const rows = [['LUNES:', 'sospechoso.'], ['MARTES:', 'muy sospechoso.'], ['MIÉRCOLES:', 'el hámster también.']];
  rows.forEach(([d, s2], i) => { if (t < t0s[i]) return; const u = clamp((t - t0s[i]) / .6), full = d + ' ' + s2, n = Math.round(u * full.length);
    X.save(); X.font = 'bold 58px ComicNeue'; X.fillStyle = '#2b3a67'; X.textAlign = 'left'; X.fillText(full.slice(0, n), -430, -210 + i * 184); X.restore(); });
  if (t > t0s[2] + .6) { X.save(); X.translate(420, 270); X.rotate(.1); drawAnimal(X, 'hamster', 0, 60, .7, { t }); X.strokeStyle = '#c0262d'; X.lineWidth = 7; X.beginPath(); X.ellipse(0, 0, 110, 90, 0, 0, 7); X.stroke(); X.restore(); }
  X.restore(); }
SC.s06 = (X, t) => {
  const sneak = Lt('s06_07') - .05, book = Lt('s06_08') - .2;
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 540, z: 1.0, z2: 1.04, lock: 1 },
    { t: Lt('s06_02') - .05, cx: 860, cy: 600, z: 1.9, z2: 2.0, lock: 1 },
    { t: Lt('s06_03') - .05, cx: 1460, cy: 470, z: 2.0, z2: 2.1, lock: 1 },
    { t: Lm('s06_03', .55), cx: 860, cy: 620, z: 2.2, z2: 2.3, lock: 1 },
    { t: Lt('s06_04') - .05, cx: 1560, cy: 560, z: 2.0, z2: 2.1, lock: 1 },
    { t: Lt('s06_06') - .05, cx: 1660, cy: 620, z: 2.9, z2: 3.05, lock: 1 },
    { t: sneak, cx: 1300, cy: 560, z: 1.3, z2: 1.35, lock: 1 },
  ]);
  const st = stageI(cam); st.wld(g => { drawSet(g, 'classroom'); if (HYB) boardText(g, 'PASE DE LISTA', ''); });
  st.wld(g => pepeWatch(g, 250, 382, .38, 860, t));
  // the profe behind his desk, the hamster in front of its cage
  const pp = standing(1470, { t, flip: -1, look: [-10, 14], mouth: -.1, brow: .4, hR: [120, -380], holdR: (g, x, y) => propPaper(g, x + 8, y - 34, -.1, .9) });
  if (speaking(t, 's06_01')) { pp.open = talk(t, 's06_01'); }
  if (t > Lt('s06_02') && t < Lt('s06_04')) { pp.look = [-16, 8]; pp.brow = .8; pp.wide = .3; }
  if (t > Lt('s06_04')) { pp.flip = 1; pp.look = [16, 12]; pp.lid = .45; pp.brow = .9; }
  if (t > Lt('s06_05') - .1 && t < sneak) { pp.lean = .14; pp.hy = 20; }
  if (speaking(t, 's06_05')) pp.open = talk(t, 's06_05');
  if (t > sneak) { pp.flip = 1; pp.look = [18, 16]; pp.lean = .1; pp.lid = .45; }   // still glaring at the hamster
  st.wld(g => drawChar(g, 'profe', pp));
  st.wld(g => { teacherDesk(g, 1620); drawSpr(g, 'cage', 1790, 704, 150); });
  st.wld(g => drawAnimal(g, 'hamster', 1640, 712, 1.0, { t, head: t > Lt('s06_06') ? 'side' : 'n', flip: t > Lt('s06_06') ? -1 : 1, tilt: Math.sin(t * 2.2) * .05, bob: -Math.abs(Math.sin(t * 7)) * 2 }));
  // classmates at their desks, and yours
  st.wld(g => { drawChar(g, 'ex2', { x: 420, y: 905, s: S0, sit: 1, noShadow: 1, t, look: [14, 6], mouth: .1, hL: [-70, -170], hR: [70, -170] }); desk(g, 420, FEET, .8); });
  if (t < sneak) {
    const hp = ghost({ x: 860, y: 905, s: S0, sit: 1, t, look: [14, 6], mouth: .2, hL: [-70, -170], hR: [70, -170] });
    if (speaking(t, 's06_02')) { hp.open = talk(t, 's06_02'); hp.hR = [120, -560]; }
    if (t > Lt('s06_03')) { const G = charGeom(CAST.tu, hp); hp.hR = POSE.wave(t, G)[1]; hp.mouth = .4; }
    if (t > Lt('s06_05')) { hp.hR = [60, -330]; hp.look = [16, 4]; hp.mouth = .8; hp.brow = -.1; }
    st.inv(g => drawChar(g, 'tu', hp)); st.fg(g => desk(g, 860, FEET, .8));
    composeI(X, st, { inv: 1, t });
    voiceBubble(X, cam, t, 's06_02', mouthPt('tu', hp), { dx: 1, r: 90 });
    if (t > Lt('s06_03') + .4 && t < Lt('s06_04')) { const [x, y] = worldToScreen(cam, 860, 300); X.save(); X.globalAlpha = vis(t, Lt('s06_03') + .4, Lt('s06_04') - .2); text(X, 'BANCA «VACÍA»', x, y, 60, '#ffffff', 'Bangers', 'center', OUT, 8); X.restore(); }
    if (t > Lt('s06_06') + .3) comicWord(X, '¡HMPF!', ...worldToScreen(cam, 1600, 560), t - Lt('s06_06') - .3, 72, '#ffffff', 1.1);
  } else {
    // you sneak to his desk; the notebook floats up
    const hx = mix(860, 1260, R(t, sneak, sneak + 1.4, io)), hp = ghost({ x: hx, y: FEET, s: S0, t, walk: t < sneak + 1.4 ? 1 : 0, phase: walkPh(hx), look: [14, 10], mouth: .5, lid: .2 });
    if (t > sneak + 1.4) { hp.hR = [140, -470]; hp.hL = [-40, -440]; hp.holdR = floatHold(st, (g, x, y) => drawSpr(g, 'notebook', x + 10, y + 40, 110, { rot: -.12 })); }
    st.inv(g => drawChar(g, 'tu', hp)); st.fg(g => desk(g, 860, FEET, .8));
    composeI(X, st, { inv: 1, t });
    notebookPage(X, R(t, book, book + .35, outC), t, [Lt('s06_08') + .1, Lm('s06_08', .36), Lm('s06_08', .66)]);
  }
};

/* ================================================================ 7. the week: free cinema, the ghost torta, the teachers' lounge */
function screenFlicker(X, a, t, col = 'rgba(120,160,255,') { if (a <= 0) return; const k = .14 + .08 * Math.sin(t * 7) * Math.sin(t * 2.3); X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.globalCompositeOperation = 'screen'; X.fillStyle = col + (k * a) + ')'; X.fillRect(0, 0, W, H); X.restore(); }
SC.s07 = (X, t) => {
  const caf = Lt('s07_04') - .05, sala = Lt('s07_06') - .05, sitOn = Lt('s07_03') - .05, grab = Lt('s07_04') + .5;
  if (t < caf) {
    const cam = shots(t, [], [{ t: 0, cx: 960, cy: 540, z: 1.0, z2: 1.05, lock: 1 }, { t: Lt('s07_02') - .05, cx: 960, cy: 640, z: 1.5, z2: 1.6, lock: 1 }, { t: sitOn, cx: 960, cy: 660, z: 1.7, z2: 1.8, lock: 1 }]);
    const st = stageI(cam); st.wld(g => drawSet(g, 'cine'));
    st.wld(g => { drawChar(g, 'ex5', { x: 420, y: 1120, s: .9, sit: 1, noShadow: 1, t, look: [0, -12], mouth: .1 }); drawChar(g, 'ex2', { x: 1500, y: 1120, s: .9, sit: 1, noShadow: 1, t, look: [0, -12], mouth: .3 }); });
    const squash = t > sitOn + .5 ? 1 : 0;
    const hp = ghost({ x: 960, y: 1120, s: .9, sit: 1, t, look: [0, -10], mouth: .7, hR: [110, -260], hL: [-60, -250], holdR: floatHold(st, (g, x, y) => drawSpr(g, 'popcorn', x + 10, y + 40, 120)) });
    if (squash) { hp.wide = .9; hp.brow = 1; hp.mouth = -.4; hp.hy = -60; hp.look = [0, -6]; hp.hL = [-170, -520 + Math.sin(t * 14) * 30]; hp.hR = [170, -520 - Math.sin(t * 14) * 30]; hp.holdR = null; }
    st.inv(g => drawChar(g, 'tu', hp));
    if (t > sitOn) { const u = R(t, sitOn, sitOn + .5, io); st.fg(g => drawChar(g, 'ex3', { x: mix(1500, 960, Math.min(1, u * 1.4)), y: mix(1080, 1130, u), s: .98, sit: u, noShadow: 1, t, look: [0, -8], mouth: .2, walk: u < .7 ? 1 : 0, phase: t * 6 })); }
    composeI(X, st, { inv: 1, t }); screenFlicker(X, 1, t);
    sticker(X, 'CINE: BOLETO ✗', vis(t, Lt('s07_02') + .2, sitOn - .2), 70, 70, 60);
    if (t > sitOn + .5) comicWord(X, '¡UF!', ...worldToScreen(cam, 1060, 620), t - sitOn - .5, 96);
    return;
  }
  if (t < sala) {
    const cam = shots(t, [], [{ t: 0, cx: 960, cy: 540, z: 1.05, z2: 1.1, lock: 1 }, { t: grab + .8, cx: 960, cy: 540, z: 1.0, z2: 1.02, lock: 1 }]);
    const st = stageI(cam); st.wld(g => drawSet(g, 'cafeteria'));
    const scared = t > grab + .4, kids = [['ex2', 1380], ['ex6', 1560], ['ex4', 1740]];
    st.wld(g => kids.forEach(([n, x], i) => drawChar(g, n, standing(x, { t, flip: -1, look: [-16, scared ? -6 : 6], mouth: scared ? -.5 : .2, wide: scared ? 1 : 0, brow: scared ? 1 : 0, open: scared ? .9 : 0,
      hL: scared ? [-90, -520] : null, hR: scared ? [90, -520] : null }))));
    const hx = t < grab ? mix(300, 960, R(t, caf, grab, io)) : mix(960, -200, R(t, grab + .3, grab + 2.4, lin)), moving = t < grab - .1 || t > grab + .3;
    const hp = ghost({ x: hx, y: FEET, s: S0, t, walk: moving ? 1.3 : 0, phase: walkPh(hx) * 1.3, flip: t > grab + .2 ? -1 : 1, look: [12, 4], mouth: .8 });
    if (t < grab) st.wld(g => drawSpr(g, 'torta', 980, 640, 90));
    else { hp.hR = [130, -470]; hp.holdR = floatHold(st, (g, x, y) => drawSpr(g, 'torta', x, y + 30, 90, { rot: Math.sin(t * 8) * .15 })); }
    st.inv(g => drawChar(g, 'tu', hp));
    composeI(X, st, { inv: 1, t });
    if (scared) comicWord(X, '¡AAAH!', ...worldToScreen(cam, 1560, 300), t - grab - .4, 96, '#ffffff', 1.2);
    if (t > Lt('s07_05') - .05) { const a = R(t, Lt('s07_05'), Lt('s07_05') + .3, back); sticker(X, 'LEYENDA ESCOLAR: LA TORTA FANTASMA', a, 70, 70, 62, '#ffffff');
      X.save(); X.globalAlpha = a; X.translate(1600, 300); X.rotate(Math.sin(t * 3) * .1); shape(X, q => { q.moveTo(-90, 60); q.quadraticCurveTo(-100, -90, 0, -100); q.quadraticCurveTo(100, -90, 90, 60); for (let i = 0; i < 4; i++) q.lineTo(60 - i * 50, 60 + (i % 2 ? 0 : 26)); q.closePath(); }, 'rgba(255,255,255,.92)', 5);
      X.drawImage(SPR.torta, -55, -70, 110, 76); circ(X, -26, -20, 9, OUT, 0); circ(X, 26, -20, 9, OUT, 0); X.restore(); }
    return;
  }
  // the teachers' lounge: the TV is where the camera is
  const cam = shots(t, [], [{ t: 0, cx: 960, cy: 560, z: 1.05, z2: 1.1, lock: 1 }, { t: Lt('s07_07') - .05, cx: 1000, cy: 560, z: 1.9, z2: 2.05, lock: 1 }]);
  const st = stageI(cam); st.wld(g => drawSet(g, 'salaMaestros'));
  const cry = t > Lt('s07_07') - .05;
  st.wld(g => { drawChar(g, 'ex5', benchSit(760, { t, y: 930, look: [0, -4], mouth: .2, wide: .2 }));
    drawChar(g, 'profe', benchSit(1040, { t, y: 930, look: [0, -6], mouth: cry ? -.5 : -.1, brow: cry ? 1 : .2, lid: cry ? .3 : 0, hR: cry ? [70, -400] : [80, -125],
      holdR: cry ? (q, x, y) => shape(q, k => k.ellipse(x + 4, y - 20, 34, 26, .3, 0, 7), '#ffffff', 3) : null })); drawSpr(g, 'tissues', 1300, 930, 70); });
  if (cry) st.wld(g => { for (let i = 0; i < 6; i++) { const u = loopU(t, i * .17, 1), x = 1000 + (i % 2 ? 70 : 0), y = 520 + u * 260; g.save(); g.globalAlpha = 1 - u; shape(g, q => { q.moveTo(x, y - 14); q.quadraticCurveTo(x + 9, y, x, y + 8); q.quadraticCurveTo(x - 9, y, x, y - 14); }, '#7cc8ff', 2); g.restore(); } });
  const hp = ghost(standing(330, { t, look: [16, 2], mouth: cry ? .7 : -.1, wide: .4, brow: .4, hR: cry ? [40, -470] : null }));
  st.inv(g => drawChar(g, 'tu', hp));
  composeI(X, st, { inv: 1, t }); screenFlicker(X, 1, t);
  sticker(X, 'SALA DE MAESTROS: ULTRASECRETO', vis(t, .2, Lt('s07_07') - .2), 70, 70, 60);
  if (t > Lt('s07_07')) { const a = R(t, Lt('s07_07') + .2, Lt('s07_07') + .4); X.save(); X.globalAlpha = a; shape(X, q => rrPath(q, 360, 900, 1200, 110, 14), 'rgba(10,10,20,.82)', 0); text(X, '«¡GUSTAVO… ERA TU GEMELO!»', 960, 975, 62, '#ffffff', 'Bangers', 'center'); X.restore(); }
};

/* ================================================================ 8. nobody sees you. Except Pepe. */
SC.s08 = (X, t) => {
  const pass = Lt('s08_03'), crouch = Lt('s08_05') - .3;
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 540, z: 1.0, z2: 1.05, lock: 1 },
    { t: pass - .05, cx: 1080, cy: 720, z: 2.0, z2: 2.1, lock: 1 },
    { t: crouch, cx: 980, cy: 680, z: 2.2, z2: 2.3, lock: 1 },
    { t: Lt('s08_06') - .05, cx: 1080, cy: 740, z: 3.2, z2: 3.4, lock: 1 },
    { t: Lt('s08_07') - .05, cx: 1000, cy: 600, z: 1.5, z2: 1.55, lock: 1 },
  ]);
  // the far path (a walker, a dog) goes behind the bench; the near walker passes in front of it
  const st = stageI(cam); st.wld(g => { drawSet(g, 'park'); walker(g, 'ex1', -200, 110, t, { look: [10, 4], mouth: .1, s: .62, y: 840 });
    drawSpr(g, 'dogARun', mix(-200, 2100, loopU(t, 0, 7)), 760, 80, { flip: -1, bob: -Math.abs(Math.sin(t * 12)) * 6 }); bench(g, 0); bench(g, 1); });
  st.wld(g => walker(g, 'ex6', 2100, -190, t, { look: [-10, 2], mouth: .3 }));
  const hx = t < crouch ? (t < Lm('s08_04', .5) ? mix(300, 1320, R(t, 0, Lm('s08_04', .5), io)) : mix(1320, 840, R(t, Lm('s08_04', .5), crouch, io))) : 840;
  const hp = ghost({ x: hx, y: FEET, s: S0, t, walk: t < crouch ? 1 : 0, phase: walkPh(hx), flip: t > Lm('s08_04', .5) && t < crouch ? -1 : 1, look: [10, 4], mouth: .2 });
  if (t > pass) { hp.look = [16, 10]; hp.brow = .5; }
  if (t > crouch) { hp.sit = .6; hp.lean = .1; hp.look = [18, 14]; hp.wide = .5; }
  if (speaking(t, 's08_05')) hp.open = talk(t, 's08_05') * .6;
  st.inv(g => drawChar(g, 'tu', hp));
  let mP = null; st.wld(g => { const front = t > Lt('s08_05') + .3; mP = pigeonTalk(g, 1100, 792, .62, { flip: hx < 1100 ? -1 : 1, front, open: speaking(t, 's08_06') ? Math.abs(Math.sin(t * 10)) * .7 : 0, tilt: Math.sin(t * 1.1) * .05 }); });
  composeI(X, st, { inv: 1, t });
  [['LA GENTE', .02], ['LOS PERROS', .35], ['LAS CÁMARAS', .7]].forEach(([s, f], i) => crossSticker(X, s, vis(t, Lm('s08_02', f), Lt('s08_05') - .2, .12), 90, 90 + i * 112));
  crossSticker(X, 'PEPE', vis(t, Lm('s08_03', .6), Lt('s08_05') - .2, .12), 90, 90 + 3 * 112, true);
  if (t > pass + .3 && t < crouch) { const [px, py] = worldToScreen(cam, 1100, 735); dashRing(X, px, py, 60 * cam.z, t); }
  voiceBubble(X, cam, t, 's08_05', mouthPt('tu', hp), { dx: -1, r: 90 });
  if (mP) cooBubble(X, cam, mP[0], mP[1] - 60, t, Lt('s08_06'), Math.max(.6, Ld('s08_06')));
  if (t > Lt('s08_07')) sticker(X, 'PEPE NO DA ENTREVISTAS', R(t, Lt('s08_07') + .1, Lt('s08_07') + .35, back), 70, 70, 70);
};

/* ================================================================ 9. problem 1: machines don't see you either */
let DOOR = null;
function superDoors(g, open) {   // the painted sliding doors of the 'super' plate, opened by `open` 0..1
  const bg = SETS.super.bg, x0 = 660, x1 = 1264, y0 = 304, y1 = 890, mid = 966;
  if (!DOOR) { // the doorway with both doors gone: the aisle's left half mirrored
    DOOR = document.createElement('canvas'); DOOR.width = x1 - x0; DOOR.height = y1 - y0; const d = DOOR.getContext('2d'), hw = 290;
    d.drawImage(bg, x0, y0, hw, y1 - y0, 0, 0, hw, y1 - y0); d.save(); d.translate(DOOR.width, 0); d.scale(-1, 1); d.drawImage(bg, x0, y0, hw, y1 - y0, 0, 0, hw, y1 - y0); d.restore();
    d.drawImage(bg, x0 + hw - 4, y0, 4, y1 - y0, hw, 0, DOOR.width - 2 * hw, y1 - y0); }
  if (open <= 0) return; const o = io(clamp(open)) * 290;
  g.save(); g.beginPath(); g.rect(x0, y0, x1 - x0, y1 - y0); g.clip(); g.drawImage(DOOR, x0, y0);
  g.drawImage(bg, x0, y0, mid - x0, y1 - y0, x0 - o, y0, mid - x0, y1 - y0); g.drawImage(bg, mid, y0, x1 - mid, y1 - y0, mid + o, y0, x1 - mid, y1 - y0); g.restore(); }
function phoneUI(g, x, y, s, t, t0) { g.save(); g.translate(x, y); g.scale(s, s); g.drawImage(SPR.phone, -95, -170, 190, 340);
  g.fillStyle = '#0e1726'; g.beginPath(); rrPath(g, -80, -150, 160, 300, 18); g.fill();
  const u = t - t0, fail = u > 1.6; g.strokeStyle = fail ? '#ff4d4d' : '#ffffff'; g.lineWidth = 5;
  for (const [sx, sy] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) { g.beginPath(); g.moveTo(sx * 50, sy * 30 - sy * 60); g.lineTo(sx * 50, sy * 60); g.lineTo(sx * 50 - sx * 22, sy * 60); g.stroke(); }
  if (!fail) { const yy = -60 + ((u * 120) % 120); g.strokeStyle = 'rgba(120,220,255,.9)'; g.beginPath(); g.moveTo(-44, yy); g.lineTo(44, yy); g.stroke(); }
  else { text(g, 'ROSTRO NO', 0, 100, 22, '#ff6b6b', 'Bangers', 'center'); text(g, 'DETECTADO', 0, 124, 22, '#ff6b6b', 'Bangers', 'center'); text(g, '✗', 0, 12, 60, '#ff4d4d', 'Bangers', 'center'); }
  g.restore(); }
SC.s09 = (X, t) => {
  const phone = Lt('s09_04') - .05, sink = Lt('s09_07') - .05, rule = Lt('s09_09') - .2, lady = Lm('s09_03', .45), opn = lady + 1.0, inside = opn + 1.6;
  let cam;
  if (t < phone) {
    cam = shots(t, [], [{ t: 0, cx: 960, cy: 560, z: 1.0, z2: 1.05, lock: 1 }, { t: Lt('s09_02') - .05, cx: 960, cy: 600, z: 1.35, z2: 1.42, lock: 1 }, { t: lady - .5, cx: 1000, cy: 580, z: 1.15, z2: 1.2, lock: 1 }]);
    const st = stageI(cam); st.wld(g => drawSet(g, 'super'));
    const open = R(t, opn, opn + .5) * (1 - R(t, inside + .2, inside + .7));
    st.wld(g => { superDoors(g, open); const led = open > 0 ? '#5fe36b' : '#ff4d4d'; circ(g, 966, 286, 7, led, 2); });
    // the lady: walks up, the doors open for her, she goes in
    if (t > lady) { const lx = mix(1900, 980, R(t, lady, opn, io)), into = R(t, opn + .4, inside, io), lp = standing(lx, { t, flip: -1, s: S0 * (1 - .25 * into), y: FEET - 70 * into, walk: t < opn || (t > opn + .4 && t < inside) ? 1 : 0, phase: walkPh(lx) + t * 3, look: [-10, 2], mouth: .2 });
      st.wld(g => { g.save(); g.globalAlpha = 1 - R(t, inside - .5, inside); drawChar(g, 'ex4', lp); g.restore(); }); }
    const hp = ghost(standing(820, { t, look: [14, -6], mouth: .2 }));
    if (t > Lt('s09_02') && t < lady) { const G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = POSE.wave(t * 1.2, G); hp.jump = Math.abs(Math.sin(t * 6)) * 40; hp.mouth = .6; hp.brow = .5; }
    if (t > lady && t < opn + .4) { hp.look = [16, 0]; hp.mouth = .3; }
    if (t > opn + .4) { const into = R(t, opn + .5, inside + .1, io); hp.x = mix(820, 960, into); hp.s = S0 * (1 - .25 * into); hp.y = FEET - 70 * into; hp.walk = into < 1 ? 1 : 0; hp.phase = t * 6; hp.inv = into; }
    if (!(t > inside + .1)) st.inv(g => drawChar(g, 'tu', hp));
    composeI(X, st, { inv: 1, t });
    if (t > Lt('s09_02') + .3 && t < lady) sticker(X, 'SENSOR: NADIE', R(t, Lt('s09_02') + .3, Lt('s09_02') + .5, back), 70, 70, 64, '#ffffff');
    if (t > opn && t < opn + .8) comicWord(X, '¡FIUUU!', ...worldToScreen(cam, 960, 380), t - opn, 80, '#ffffff', .8);
    return;
  }
  if (t < sink) {   // the phone does not know your face
    cam = shots(t, [], [{ t: phone, cx: 1000, cy: 470, z: 2.1, z2: 2.2, lock: 1 }]);
    const st = stageI(cam); st.wld(g => drawSet(g, 'street'));
    const hp = ghost(standing(900, { t, look: [16, 2], mouth: .1, brow: .5, hR: [190, -500], hL: [-100, -240] }));
    for (const id of ['s09_05']) if (speaking(t, id)) { hp.open = talk(t, id) * .5; hp.brow = .9; }
    hp.holdR = floatHold(st, (g, x, y) => phoneUI(g, x - 60, y - 70, .62, t, phone + .2));
    st.inv(g => drawChar(g, 'tu', hp));
    composeI(X, st, { inv: 1, t });
    voiceBubble(X, cam, t, 's09_05', mouthPt('tu', hp), { dx: 1, r: 95 });
    if (t > Lt('s09_06') - .05) sticker(X, '«ROSTRO NO DETECTADO»', R(t, Lt('s09_06'), Lt('s09_06') + .25, back), 70, 70, 64);
    return;
  }
  // the school sink: the sensor does not see your hands
  cam = shots(t, [], [{ t: sink, cx: 960, cy: 560, z: 1.7, z2: 1.8, lock: 1 }, { t: Lt('s09_08') - .05, cx: 960, cy: 640, z: 2.6, z2: 2.7, lock: 1 }, { t: rule, cx: 960, cy: 540, z: 1.0, lock: 1 }]);
  const st = stageI(cam); st.wld(g => { drawSet(g, 'bathroom'); circ(g, 1000, 572, 7, '#ff4d4d', 2); });
  const shake = Math.sin(t * 14) * 18, hp = ghost(standing(960, { t, look: [0, 18], mouth: -.2, brow: .7, hL: [-40 + shake, -290], hR: [40 - shake, -290] }));
  if (t > Lt('s09_08')) { hp.sweat = 1; hp.mouth = -.4; }
  st.inv(g => drawChar(g, 'tu', hp));
  composeI(X, st, { inv: 1, t });
  if (t > Lt('s09_08') - .05) bigCounter(X, 'SIN LAVARTE LAS MANOS:', '3 DÍAS', R(t, Lt('s09_08'), Lt('s09_08') + .25, outC));
  ruleCard(X, 2, 'LAS MÁQUINAS TAMPOCO TE VEN.', t > Lm('s09_09', .45) ? 'NI PUERTAS, NI CÁMARAS, NI TU TELÉFONO.' : '', R(t, rule, rule + .4, outC));
};

/* ================================================================ 10. problem 2: everybody bumps into you */
SC.s10 = (X, t) => {
  const b1 = Lm('s10_01', .6), b2 = Lt('s10_03') - .1, ninja = Lt('s10_05') - .05;
  const hx = t < ninja ? mix(500, 1500, R(t, 0, ninja, lin)) : mix(1200, 1900, R(t, ninja, T().dur, lin));
  const cam = shots(t, [], [
    { t: 0, cx: (tt => clamp(mix(500, 1500, R(tt, 0, ninja, lin)) + 120, 960, 1640)), cy: 560, z: 1.0, lock: 1, w: 2600 },
    { t: b2 - .3, cx: 1300, cy: 520, z: 1.8, z2: 1.9, lock: 1, w: 2600 },
    { t: Lt('s10_04') - .05, cx: 1300, cy: 560, z: 1.1, z2: 1.15, lock: 1, w: 2600 },
    { t: ninja, cx: (tt => clamp(mix(1200, 1900, R(tt, ninja, T().dur, lin)), 960, 1640)), cy: 520, z: 1.3, lock: 1, w: 2600 },
  ]);
  const st = stageI(cam); st.wld(g => drawSet(g, 'hallway'));
  const bump = [b1, Lm('s10_02', .2), Lm('s10_02', .55), Lm('s10_02', .85), b2].filter(x => x < ninja), last = Math.max(-9, ...bump.filter(b => t > b));
  const kick = t - last < .4 ? (1 - (t - last) / .4) : 0;
  const hp = ghost({ x: hx, y: FEET, s: S0, t, walk: kick > .1 ? 0 : 1, phase: walkPh(hx), look: [12, 2], mouth: .2, lean: -kick * .35, wide: kick, brow: kick });
  if (t > ninja) { Object.assign(hp, { lean: 0, walk: .6, look: [14, 0], mouth: -.3, sweat: 1, hL: [-170, -430], hR: [170, -430], y: FEET - 60, s: S0 * .95 }); }
  st.inv(g => drawChar(g, 'tu', hp));
  // the crowd: everybody walks left, right through where you are
  if (t < ninja) st.wld(g => { const names = ['ex1', 'ex2', 'ex4', 'ex5', 'ex6']; bump.slice(0, 4).forEach((b, i) => { const x = hx + (b - t) * 220 + 10; if (x > hx - 900 && x < hx + 1600) drawChar(g, names[i], { x, y: FEET, s: S0, t, walk: 1, phase: walkPh(x), flip: -1, look: [-10, 4], mouth: .2 }); }); });
  if (t > b2 - 1.5 && t < ninja) { const nx = t < b2 ? hx + (b2 - t) * 220 + 10 : hx - (t - b2) * 90 - 40, np = { x: nx, y: FEET, s: S0, t, walk: t < b2 || t > Lt('s10_04') ? 1 : 0, phase: walkPh(nx), flip: -1, look: [-10, 4], mouth: .2 };
    if (speaking(t, 's10_03')) { np.open = talk(t, 's10_03'); np.flip = 1; np.look = [14, -4]; np.brow = .6; np.wide = t > Lm('s10_03', .5) ? .8 : 0; }
    st.wld(g => drawChar(g, 'nacho', np)); }
  if (t > ninja) st.fg(g => { for (let i = 0; i < 3; i++) { const x = 2400 - ((t - ninja) * 260 + i * 520) % 2600; drawChar(g, ['ex2', 'ex6', 'ex1'][i], { x, y: FEET + 30, s: S0 * 1.05, t, walk: 1, phase: walkPh(x), flip: -1, look: [-10, 4], mouth: .2 }); } });
  composeI(X, st, { inv: 1, t });
  for (const b of bump) if (t > b && t < b + .7) comicWord(X, '¡PUM!', ...worldToScreen(cam, hx + 60, 360), t - b, 84);
  if (t > ninja + .3) sticker(X, 'MODO NINJA (MUY CANSADO)', R(t, ninja + .3, ninja + .55, back), 70, 70, 64);
};

/* ================================================================ 11. problem 3: by Wednesday, nobody waits for you */
function tray(g, x, y, food = 'torta') { shape(g, q => rrPath(q, x - 90, y - 16, 180, 26, 6), '#f08a3c', 4); if (food) drawSpr(g, food, x, y - 6, 54); }
SC.s11 = (X, t) => {
  const home = Lt('s11_07') - .05, card = Lt('s11_09') - .2;
  if (t < home) {
    const cam = shots(t, [], [
      { t: 0, cx: 960, cy: 540, z: 1.0, z2: 1.04, lock: 1 },
      { t: Lt('s11_03') - .05, cx: 700, cy: 520, z: 2.0, z2: 2.1, lock: 1 },
      { t: Lt('s11_04') - .05, cx: 1220, cy: 520, z: 2.0, z2: 2.1, lock: 1 },
      { t: Lt('s11_05') - .05, cx: 860, cy: 540, z: 1.5, z2: 1.55, lock: 1 },
      { t: Lt('s11_06') - .05, cx: 960, cy: 520, z: 2.3, z2: 2.5, lock: 1 },
    ]);
    const st = stageI(cam); st.wld(g => drawSet(g, 'cafeteria'));
    const np = { x: 700, y: 905, s: S0, sit: 1, noShadow: 1, t, look: [14, 6], mouth: .5, hL: [-60, -170], hR: [70, -170] };
    if (speaking(t, 's11_03')) { np.open = talk(t, 's11_03'); np.look = [16, 0]; np.brow = .3; }
    if (speaking(t, 's11_05') || t > Le('s11_05')) { np.open = speaking(t, 's11_05') ? talk(t, 's11_05') : 0; np.hR = [300, -220]; np.look = [18, 8]; np.mouth = .7; }
    const rp = { x: 1220, y: 905, s: S0, sit: 1, noShadow: 1, t, flip: -1, look: [-10, 14], mouth: -.1, brow: .4, hL: [-60, -170], hR: [70, -170] };
    if (speaking(t, 's11_04')) { rp.open = talk(t, 's11_04'); rp.look = [-6, 16]; rp.brow = .7; }
    if (t > Le('s11_04')) { rp.mouth = -.25; rp.brow = .7; rp.look = [-4, 18]; }
    st.wld(g => { drawChar(g, 'nacho', np); drawChar(g, 'valeria', rp); });
    const hp = ghost({ x: 960, y: 905, s: S0, sit: 1, t, look: [t > Lt('s11_04') ? 12 : -12, 8], mouth: -.3, brow: .6, slump: .6, hL: [-60, -170], hR: [60, -170] });
    st.inv(g => drawChar(g, 'tu', hp));
    st.fg(g => { kitchenTable(g); tray(g, 700, 790, 'tacos'); tray(g, 960, 790, null); tray(g, 1220, 790, 'torta'); });
    composeI(X, st, { inv: 1, t });
    sticker(X, 'MIÉRCOLES', vis(t, .2, Lt('s11_03') - .2), 70, 70, 70);
    if (t > Lt('s11_06')) { const [x, y] = worldToScreen(cam, 960, 300); X.save(); X.globalAlpha = R(t, Lt('s11_06') + .1, Lt('s11_06') + .4); text(X, 'A 50 CM', x, y, 70, INV_COL, 'Bangers', 'center', OUT, 10); X.restore(); }
    return;
  }
  // at home: Mom talks to your door all week
  const cam = shots(t, [], [{ t: home, cx: 760, cy: 560, z: 1.15, z2: 1.2, lock: 1 }, { t: card, cx: 960, cy: 540, z: 1.0, lock: 1 }]);
  const st = stageI(cam); st.wld(g => { drawSet(g, 'bedroom'); bedBack(g);
    shape(g, q => rrPath(q, 60, 300, 280, 640, 10), '#c48a55', 6); shape(g, q => rrPath(q, 100, 340, 200, 240, 8), '#b07848', 4); shape(g, q => rrPath(q, 100, 620, 200, 260, 8), '#b07848', 4); circ(g, 300, 640, 14, '#e3c27a', 4); });
  const hp = ghost({ x: 640, y: 905, s: S0, sit: 1, t, look: [-16, 8], mouth: -.3, brow: .5, slump: .5, hL: [-60, -150], hR: [60, -150] });
  st.inv(g => drawChar(g, 'tu', hp));
  st.fg(g => bedFront(g, .5));
  composeI(X, st, { inv: 1, t }); nightTint(X, .5);
  const knock = Lt('s11_07') + .3; if (t > knock && t < knock + .9) comicWord(X, 'TOC TOC', ...worldToScreen(cam, 200, 380), t - knock, 70, '#ffffff', .9);
  if (t > knock + .6 && t < card) { const a = vis(t, knock + .6, card - .3); X.save(); X.globalAlpha = a; const [x, y] = worldToScreen(cam, 200, 280); shape(X, q => rrPath(q, x - 30, y - 120, 420, 90, 26), '#fff6dc', 5); X.font = 'bold 40px ComicNeue'; X.fillStyle = '#2a1420'; X.fillText('¿Estás bien, mijo?', x - 6, y - 62); X.restore(); }
  if (t > Lt('s11_08')) sticker(X, 'MAMÁ: «ES LA ADOLESCENCIA»', vis(t, Lt('s11_08'), card - .2), 70, 70, 60);
  ruleCard(X, '2 Y MEDIO', 'SER INVISIBLE ES MUY DIVERTIDO…', t > Lm('s11_09', .5) ? '…LOS PRIMEROS DOS DÍAS.' : '', R(t, card, card + .4, outC));
};
