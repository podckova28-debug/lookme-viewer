/* Ep03 scenes 6–10: the class hamster, the pet detective, Pepe says nothing, the cookie war, the night shift. */

/* ================================================================ 6. Señor Bigotes, the hamster who has seen everything */
function scorePaper(g, x, y, s, rot, label) { propPaper(g, x, y, rot, s); g.save(); g.translate(x, y); g.rotate(rot); text(g, label, 0, 18 * s, 54 * s, '#c0262d', 'Bangers', 'center'); g.restore(); }
function notes(g, x, y, t, a = 1) { if (a <= 0) return; g.save(); g.globalAlpha = a; for (let i = 0; i < 3; i++) { const u = ((t * .7 + i / 3) % 1); g.globalAlpha = a * Math.sin(u * Math.PI); text(g, i % 2 ? '♪' : '♫', x + u * 50 + i * 14, y - u * 90, 40, '#2a1420', 'Bangers', 'left'); } g.restore(); }
SC.s06 = (X, t) => {
  const exam = Lt('s06_07') - .05, away = Lt('s06_10') - .05;
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 560, z: 1.0, z2: 1.04, lock: 1 },
    { t: Lt('s06_02') - .05, cx: 1560, cy: 600, z: 2.6, z2: 2.75, lock: 1 },
    { t: Lt('s06_03') - .05, cx: 1500, cy: 560, z: 1.5, z2: 1.55, lock: 1 },
    { t: Lt('s06_04') - .05, cx: 1500, cy: 620, z: 2.3, z2: 2.4, lock: 1 },
    { t: Lt('s06_05') - .05, cx: 900, cy: 480, z: 2.0, z2: 2.1, lock: 1 },
    { t: Lt('s06_06') - .05, cx: 1560, cy: 600, z: 2.7, z2: 2.8, lock: 1 },
    { t: exam, cx: 1000, cy: 520, z: 1.25, z2: 1.3, lock: 1 },
    { t: Lt('s06_08') - .05, cx: 1300, cy: 460, z: 1.8, z2: 1.85, lock: 1 },
    { t: Lt('s06_09') - .05, cx: 1300, cy: 540, z: 1.35, z2: 1.4, lock: 1 },
    { t: away, cx: 1580, cy: 600, z: 2.9, z2: 3.1, lock: 1 },
  ]);
  const st = stage(cam); st.wld(g => { drawSet(g, 'classroom'); if (HYB) boardText(g, t > exam ? 'EXAMEN SORPRESA' : 'FOTOSÍNTESIS', t > exam ? '1) ¿?   2) ¿?' : ''); teacherDesk(g, 1620); drawSpr(g, 'cage', 1720, 704, 150); });
  st.col(g => drawPigeon(g, 260, 380, .38, { flip: 1, tilt: Math.sin(t * .8) * .12 }));
  st.wld(g => { drawChar(g, 'ex2', standing(380, { t, look: [6, 4], mouth: .1 })); drawChar(g, 'ex5', standing(560, { t, look: [8, 4], mouth: .1 })); });
  // profe: comes in with the graded papers
  if (t > exam) { const px = mix(1900, 1240, R(t, exam, exam + 1.4, io)), pp = { x: px, y: FEET, s: S0, t, flip: -1, walk: t < exam + 1.4 ? 1 : 0, phase: walkPh(px), look: [-14, 4], mouth: -.2, brow: .6 };
    if (t > Lt('s06_08') - .2) { pp.hR = [160, -440]; pp.holdR = (g, x, y) => scorePaper(g, x - 10, y - 40, .9, -.1, '10/10'); }
    if (speaking(t, 's06_08')) pp.open = talk(t, 's06_08');
    if (t > Le('s06_08')) { pp.lid = .45; pp.brow = .9; pp.mouth = -.3; }
    if (t > Lm('s06_09', .5)) { pp.flip = 1; pp.look = [16, 10]; }
    st.wld(g => drawChar(g, 'profe', pp)); }
  const hp = standing(860, { t, look: [14, 0], mouth: .1 });
  if (t > Lt('s06_02') && t < exam) { hp.look = [18, 6]; hp.wide = .4; hp.brow = .4; }
  if (speaking(t, 's06_05')) { hp.open = talk(t, 's06_05') * .6; hp.hR = [110, -560]; }
  if (t > exam && t < Lt('s06_08')) { hp.mouth = .8; hp.brow = -.2; hp.hR = [150, -560]; hp.holdR = (g, x, y) => scorePaper(g, x + 10, y - 40, .9, .1, '10/10'); }
  if (t > Lt('s06_08')) { hp.mouth = -.25; hp.sweat = 1; hp.brow = .6; hp.look = [16, 0]; }
  st.col(g => drawChar(g, 'tu', hp));
  let mH = null;
  st.col(g => { mH = drawAnimal(g, 'hamster', 1560, 712, 1.0, { t, head: t > away ? 'side' : 'n', flip: t > away ? -1 : 1, open: openOf(t, ['s06_02', 's06_04', 's06_06']), tilt: Math.sin(t * 2.2) * .05, bob: -Math.abs(Math.sin(t * 7)) * 2 }); });
  compose2(X, st, { amt: 0 });
  for (const id of ['s06_02', 's06_04', 's06_06']) say(X, cam, t, id, mH, { dx: -1, r: 70 });
  if (t > away) notes(X, ...worldToScreen(cam, 1520, 600), t, R(t, away + .3, away + .6));
};

/* ================================================================ 7. pet detective: lost posters get stamped, Nacho collects */
function corkboard(g) { g.fillStyle = '#b07a4a'; g.fillRect(0, 0, W, H); const r = rnd(4); g.fillStyle = 'rgba(80,40,20,.25)'; for (let i = 0; i < 600; i++) g.fillRect(r() * W, r() * H, 3, 3);
  shape(g, q => q.rect(30, 30, W - 60, H - 60), null, 14); }
function wanted(g, x, y, rot, art, label, stampU, t) { g.save(); g.translate(x, y); g.rotate(rot);
  shape(g, q => rrPath(q, -240, -320, 480, 640, 8), '#fbf7ec', 6); circ(g, 0, -300, 16, '#e02424', 4);
  text(g, 'SE BUSCA', 0, -215, 92, '#141014', 'Bangers', 'center'); shape(g, q => q.rect(-180, -180, 360, 300), '#e8eef4', 4);
  const I = ANI[art]; if (I) { const k = Math.min(320 / I.width, 270 / I.height); g.drawImage(I, -I.width * k / 2, -30 - I.height * k / 2, I.width * k, I.height * k); }
  text(g, label, 0, 200, 54, '#141014', 'Bangers', 'center'); text(g, 'RECOMPENSA', 0, 268, 40, '#c0262d', 'Bangers', 'center');
  if (stampU > 0) { const s = 1 + 1.6 * (1 - outC(clamp(stampU * 3))); g.save(); g.rotate(-.25); g.scale(s, s); g.globalAlpha = clamp(stampU * 4) * .9;
    shape(g, q => rrPath(q, -230, -60, 460, 120, 14), null, 0); g.strokeStyle = '#1f9d55'; g.lineWidth = 12; g.beginPath(); rrPath(g, -230, -60, 460, 120, 14); g.stroke();
    text(g, '¡ENCONTRADO!', 0, 30, 92, '#1f9d55', 'Bangers', 'center'); g.restore(); }
  g.restore(); }
SC.s07 = (X, t) => {
  const street = Lt('s07_05') - .05;
  if (t < street) {
    const cam = shots(t, [], [
      { t: 0, cx: 960, cy: 540, z: 1.0, z2: 1.05, lock: 1 },
      { t: Lt('s07_02') - .05, cx: 480, cy: 520, z: 1.55, z2: 1.6, lock: 1 },
      { t: Lt('s07_03') - .05, cx: 960, cy: 560, z: 1.55, z2: 1.6, lock: 1 },
      { t: Lt('s07_04') - .05, cx: 1440, cy: 520, z: 1.55, z2: 1.62, lock: 1 },
    ]);
    const st = stage(cam); st.wld(g => { corkboard(g);
      wanted(g, 480, 520, -.04, 'parrot', 'PERICO VERDE', t > Lm('s07_02', .55) ? (t - Lm('s07_02', .55)) : 0, t);
      wanted(g, 960, 560, .03, 'roofCat', 'GATO GRIS', t > Lm('s07_03', .55) ? (t - Lm('s07_03', .55)) : 0, t);
      wanted(g, 1440, 520, -.02, 'turtle', 'TORTUGA', t > Lm('s07_04', .75) ? (t - Lm('s07_04', .75)) : 0, t); });
    compose2(X, st, { amt: 0 });
    if (t < Lt('s07_02')) sticker(X, 'DETECTIVE DE MASCOTAS', R(t, .3, .6, back), 560, 60, 70);
    if (t > Lm('s07_04', .45) && t < street) sticker(X, '2 AÑOS PERDIDA… EN SU JARDÍN', R(t, Lm('s07_04', .45), Lm('s07_04', .45) + .2, back), 980, 940, 52, '#ffffff');
    return;
  }
  const cam = shots(t, [], [
    { t: street, cx: 960, cy: 560, z: 1.15, z2: 1.2, lock: 1 },
    { t: Lt('s07_06') - .05, cx: 1180, cy: 480, z: 1.8, z2: 1.9, lock: 1 },
    { t: Lt('s07_07') - .05, cx: 1080, cy: 520, z: 1.4, z2: 1.45, lock: 1 },
  ]);
  const st = stage(cam); st.wld(g => drawSet(g, 'street'));
  // the owner gets her tortoise back; Nacho takes the money
  const own = standing(560, { t, look: [14, 6], mouth: .8, hL: [-60, -330], hR: [60, -330] });
  st.wld(g => { drawChar(g, 'ex5', own); drawSpr(g, 'turtle', 560, 700, 110, { flip: 1 }); });
  st.col(g => drawChar(g, 'tu', standing(860, { t, look: [-14, 2], mouth: .5, brow: -.1 })));
  const np = standing(1180, { t, flip: -1, look: [-14, 2], mouth: .6, hR: [120, -470] });
  if (speaking(t, 's07_05')) { np.open = talk(t, 's07_05'); np.hR = [160, -560]; }
  if (t > Lt('s07_06')) { const k = Math.sin(t * 6); np.hR = [130, -430 + k * 20]; np.holdR = (g, x, y) => { shape(g, q => rrPath(q, x - 30, y - 18, 60, 36, 4), '#7fc97f', 4); text(g, '$', x, y + 12, 34, '#1b5e20', 'Bangers', 'center'); }; np.mouth = .9; np.lid = .3; }
  st.col(g => drawChar(g, 'nacho', np));
  compose2(X, st, { amt: 0 });
  if (t > Lt('s07_05') && t < Lt('s07_06')) sticker(X, '$100 POR MASCOTA', R(t, Lt('s07_05') + .2, Lt('s07_05') + .4, back), 1240, 120, 62);
  if (t > Lt('s07_06')) { const items = [['NACHO COBRA', .0], ['NACHO NO HACE NADA', .5]]; items.forEach(([s, f], i) => sticker(X, s, R(t, Lm('s07_06', f), Lm('s07_06', f) + .2, back), 80, 80 + i * 110, 58, i ? '#ffffff' : '#ffd34d')); }
  if (t > Lt('s07_07') + .3) sticker(X, '«NEGOCIOS»', R(t, Lm('s07_07', .7), Lm('s07_07', .7) + .2, back), 1250, 820, 70);
};

/* ================================================================ 8. and then there is Pepe */
SC.s08 = (X, t) => {
  const offer = Lm('s08_03', .3), slow = Lm('s08_03', .62);
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 600, z: 1.1, z2: 1.15, lock: 1 },
    { t: Lt('s08_02') - .05, cx: 990, cy: 650, z: 1.6, z2: 1.65, lock: 1 },
    { t: Lt('s08_03') - .05, cx: 990, cy: 660, z: 1.9, z2: 1.95, lock: 1 },
    { t: Lt('s08_04') - .05, cx: 930, cy: 560, z: 2.4, z2: 2.55, lock: 1 },
    { t: Lt('s08_05') - .05, cx: 1080, cy: 740, z: 3.4, z2: 3.8, lock: 1 },
    { t: Lt('s08_06') - .05, cx: 1450, cy: 860, z: 2.0, z2: 2.1, lock: 1 },
    { t: Lt('s08_07') - .05, cx: 1450, cy: 880, z: 2.6, z2: 2.75, lock: 1 },
  ]);
  const st = stage(cam); st.wld(g => { drawSet(g, 'park'); bench(g, 0); bench(g, 1); });
  const hp = benchSit(900, { t, look: [16, 8], mouth: .2 });
  if (t > Lt('s08_03') && t < slow) { hp.look = [18, 10]; hp.mouth = .6; hp.brow = -.2; }
  if (t > offer && t < Lt('s08_04')) { hp.hR = [150, -300]; hp.holdR = (g, x, y) => drawSpr(g, 'cookie', x + 14, y + 16, 46); }
  if (t > slow) { hp.lean = .08; hp.look = [18, 12]; hp.brow = .5; }
  if (speaking(t, 's08_04')) { hp.open = talk(t, 's08_04') * 1.1; hp.wide = .3; hp.hR = [130, -330 + Math.sin(t * 5) * 30]; }
  if (t > Le('s08_04')) { hp.open = 0; hp.mouth = -.2; hp.brow = .6; }
  st.col(g => drawChar(g, 'tu', hp));
  st.col(g => drawPigeon(g, 1080, 792, .62, { flip: -1, front: t > Lt('s08_04'), tilt: Math.sin(t * 1.1) * .03 }));
  // the gang on the path; they go quiet and scatter when you ask about Pepe
  const flee = Le('s08_07') + .2; let mG = null;
  st.col(g => GANG.forEach(([hue, br, sa], i) => { const u = R(t, flee + i * .1, flee + .9 + i * .1, inC), x = 1360 + i * 120 + u * 500, y = 960 + (i % 2) * 18 - u * 700;
    const m = pigeonTalk(g, x, y, .85, { flip: t > Lt('s08_06') ? 1 : -1, tint: i ? [hue, br, sa] : null, peck: t < Lt('s08_06') ? Math.max(0, Math.sin(t * 2.6 + i)) * .6 : 0, tilt: t > Lt('s08_06') ? -.15 : 0, open: i === 1 ? openOf(t, ['s08_07']) : 0 }); if (i === 1) mG = m; }));
  compose2(X, st, { amt: 0 });
  if (t > Lt('s08_02') - .05 && t < Lt('s08_03')) { [[300, 820, 'GUAU', '¡Hola!'], [1700, 900, 'RUU', '¡Hola!'], [520, 640, 'PÍO', '¡Hola!']].forEach(([x, y, s, w], i) => gag(X, cam, t, [x, y], Lt('s08_02') + i * .3, .7, s, w, { size: 36, w: 260 })); }
  if (t > Lm('s08_02', .5) && t < Lt('s08_03')) sticker(X, 'PEPE: …', R(t, Lm('s08_02', .55), Lm('s08_02', .55) + .2, back), 1250, 200, 64, '#ffffff');
  if (t > Lt('s08_03') && t < offer) bubble(X, '¿?', ...worldToScreen(cam, 980, 380), R(t, Lt('s08_03'), Lt('s08_03') + .25, back), 60);
  if (t > Lt('s08_05')) { const [px, py] = worldToScreen(cam, 1080, 735); X.save(); X.globalAlpha = R(t, Lt('s08_05'), Lt('s08_05') + .3) * (1 - R(t, Lt('s08_06') - .2, Lt('s08_06'))); X.strokeStyle = '#ffd34d'; X.lineWidth = 8; X.setLineDash([22, 16]); X.lineDashOffset = -t * 60; X.beginPath(); X.arc(px, py, 70 * cam.z, 0, 7); X.stroke(); X.restore(); }
  say(X, cam, t, 's08_07', mG, { dx: -1, r: 60 });
};

/* ================================================================ 9. the cookie war, and Renata walks by */
SC.s09 = (X, t) => {
  const ren = Lt('s09_06') - .9, back0 = Lt('s09_08');
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 560, z: 1.0, z2: 1.05, lock: 1 },
    { t: Lt('s09_03') - .05, cx: 1080, cy: 760, z: 1.9, z2: 2.0, lock: 1 },
    { t: Lt('s09_04') - .05, cx: 860, cy: 520, z: 1.7, z2: 1.8, lock: 1 },
    { t: Lt('s09_05') - .05, cx: 960, cy: 540, z: 1.0, z2: 1.05, lock: 1 },
    { t: Lt('s09_06') - .05, cx: 1300, cy: 480, z: 1.7, z2: 1.8, lock: 1 },
    { t: Lt('s09_07') - .05, cx: 860, cy: 480, z: 2.0, z2: 2.1, lock: 1 },
    { t: back0 - .05, cx: 1100, cy: 560, z: 1.2, z2: 1.25, lock: 1 },
  ]);
  const st = stage(cam); st.wld(g => drawSet(g, 'street'));
  // passers-by stop and stare at the boy shouting at birds
  if (t > Lt('s09_05') - .3) st.wld(g => { drawChar(g, 'ex1', standing(260, { t, look: [14, 4], mouth: -.2, wide: .5, brow: .5 })); drawChar(g, 'ex4', standing(1640, { t, flip: -1, look: [-14, 4], mouth: -.2, wide: .5 })); });
  const hp = standing(860, { t, look: [14, 10], mouth: .4, hR: [140, -420], holdR: (g, x, y) => drawSpr(g, 'cookie', x + 10, y + 18, 50) });
  if (t > Lt('s09_03')) { hp.look = [16, 14]; hp.brow = .6; hp.mouth = -.2; }
  if (t > Lt('s09_04') - .1 && t < Lt('s09_05') + .5) { hp.hR = [120, -640]; hp.hL = [-170 + Math.sin(t * 16) * 30, -500]; hp.open = speaking(t, 's09_04') ? talk(t, 's09_04') : .3; hp.brow = .9; hp.jump = 10 * Math.abs(Math.sin(t * 8)); }
  if (t > Lt('s09_06')) { hp.look = [16, 0]; hp.hL = null; hp.jump = 0; hp.open = 0; hp.mouth = -.2; hp.brow = .4; hp.wide = .4; }
  if (speaking(t, 's09_07')) { hp.open = talk(t, 's09_07'); hp.lid = .2; }
  if (t > Le('s09_07')) { hp.sweat = 1; hp.mouth = -.3; }
  st.col(g => drawChar(g, 'tu', hp));
  // the gang closes in on the cookie
  let mG = null;
  st.col(g => GANG.forEach(([hue, br, sa], i) => { const close = R(t, Lt('s09_03'), Le('s09_03'), lin), x = mix(1300 + i * 140, 1000 + i * 90, close), y = 990 + (i % 2) * 14;
    const scat = t > Lt('s09_04') ? Math.sin((t - Lt('s09_04')) * 12 + i) * 18 : 0;
    const m = pigeonTalk(g, x + scat, y, .9, { flip: -1, tint: i ? [hue, br, sa] : null, open: i === 0 ? openOf(t, ['s09_03']) : (speaking(t, 's09_03') ? Math.abs(Math.sin(t * 11 + i)) * .5 : 0), tilt: -.1 }); if (i === 0) mG = m; }));
  // Renata: walks in, stops, then backs away slowly, still facing you
  if (t > ren) { const rx = t < back0 ? mix(1900, 1300, R(t, ren, Lt('s09_06'), io)) : mix(1300, 2000, R(t, back0, T().dur, lin)), rp = { x: rx, y: FEET, s: S0, t, flip: -1, walk: (t < Lt('s09_06') || t > back0) ? 1 : 0, phase: walkPh(rx) * (t > back0 ? -1 : 1), look: [-14, 6], mouth: -.1, brow: .5, wide: .3, hR: [70, -330], holdR: (g, x, y) => propBook(g, x + 4, y - 20, 70, 90, '#4f86b8', .2) };
    if (speaking(t, 's09_06')) rp.open = talk(t, 's09_06');
    if (t > Le('s09_06')) { rp.wide = .7; rp.brow = .8; rp.mouth = -.3; }
    st.wld(g => drawChar(g, 'valeria', rp)); }
  compose2(X, st, { amt: 0 });
  say(X, cam, t, 's09_03', mG, { dx: 1, r: 60 });
  if (t > Lt('s09_05') + .2 && t < ren) comicWord(X, '¡¿?!', ...worldToScreen(cam, 260, 330), (t - Lt('s09_05') - .2) * .7, 80);
};

/* ================================================================ 10. the night shift: the mosquito, the 3 a.m. dogs */
function nightTint(X, a = 1) { X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.globalCompositeOperation = 'multiply'; X.fillStyle = `rgba(60,70,140,${.85 * a})`; X.fillRect(0, 0, W, H); X.globalCompositeOperation = 'source-over';
  X.fillStyle = `rgba(8,10,30,${.35 * a})`; X.fillRect(0, 0, W, H); X.restore(); }
SC.s10 = (X, t) => {
  const dogs = Lt('s10_04') - .05, pillow = Lt('s10_07') - .05, sleepT = Lt('s10_08') - .05;
  const cam = shots(t, [], [
    { t: 0, cx: 640, cy: 640, z: 1.15, z2: 1.2, lock: 1 },
    { t: Lt('s10_02') - .05, cx: 330, cy: 600, z: 2.4, z2: 2.55, lock: 1 },
    { t: Lt('s10_03') - .05, cx: 900, cy: 520, z: 1.3, z2: 1.35, lock: 1 },
    { t: dogs, cx: 1320, cy: 380, z: 1.8, z2: 1.9, lock: 1 },
    { t: pillow, cx: 520, cy: 640, z: 1.6, z2: 1.65, lock: 1 },
    { t: sleepT, cx: 640, cy: 640, z: 1.15, z2: 1.2, lock: 1 },
    { t: Lt('s10_09') - .05, cx: 1260, cy: 900, z: 2.6, z2: 2.7, lock: 1 },
  ]);
  const st = stage(cam); st.wld(g => { drawSet(g, 'bedroom'); bedBack(g); nightstand(g); propAlarm(g, 1075, 740, .55, 3, 0); });
  st.col(g => lyingHead(g, 300, 680, { sleep: 0, wide: t < sleepT ? .4 : 0, lid: t > sleepT ? .55 : 0, look: t > dogs && t < pillow ? [16, -10] : [6, -14], mouth: -.2, brow: .6 }));
  st.wld(g => bedFront(g, t > pillow && t < sleepT ? 2.3 : 1));   // blanket pulled over your head
  st.wld(g => drawSpr(g, 'catSleep', 1260, 940, 120));
  st.wld(g => { g.save(); g.filter = 'brightness(.3) saturate(.4)'; drawSpr(g, 'dogBStand', 1180, 560, 56, { flip: 1 }); drawSpr(g, 'firuStand', 1420, 556, 70, { flip: -1 }); g.restore(); });   // the night dogs, far away through the window
  let mM = null;
  if (t < dogs) st.col(g => { const x = 380 + Math.sin(t * 2.3) * 60, y = 560 + Math.sin(t * 3.7) * 30; drawSpr(g, 'mosquito', x, y, 80, { flip: Math.cos(t * 2.3) > 0 ? -1 : 1, rot: Math.sin(t * 25) * .04 }); mM = [x - 10, y - 50]; });
  compose2(X, st, { amt: 0 });
  nightTint(X);
  // moonlight from the window
  X.save(); X.globalCompositeOperation = 'screen'; X.globalAlpha = .25; const [wx, wy] = worldToScreen(cam, 1320, 330); const gr = X.createRadialGradient(wx, wy, 20, wx, wy, 520 * cam.z); gr.addColorStop(0, 'rgba(150,170,255,1)'); gr.addColorStop(1, 'rgba(150,170,255,0)'); X.fillStyle = gr; X.fillRect(0, 0, W, H); X.restore();
  say(X, cam, t, 's10_02', mM, { dx: 1, r: 40 });
  // the dogs outside, through the window
  say(X, cam, t, 's10_04', [1170, 520], { dx: -1, r: 40 }); say(X, cam, t, 's10_05', [1430, 515], { dx: 1, r: 40 }); say(X, cam, t, 's10_06', [1180, 520], { dx: 1, r: 40 });
  if (t > Lt('s10_07') && t < sleepT) sticker(X, 'NADIE.', R(t, Lm('s10_07', .2), Lm('s10_07', .2) + .2, back), 1250, 120, 80, '#ffffff');
  if (t > sleepT) { bigCounter(X, 'TÚ:', '3 H', R(t, Lm('s10_08', .1), Lm('s10_08', .1) + .2, outC), 80, 70); bigCounter(X, 'CROQUETA:', '14 H', R(t, Lm('s10_08', .55), Lm('s10_08', .55) + .2, outC), 80, 200); }
  say(X, cam, t, 's10_09', [1280, 860], { dx: -1, r: 50 });
  zzz(X, ...worldToScreen(cam, 1300, 840), t, t > sleepT ? 1 : .6);
};
