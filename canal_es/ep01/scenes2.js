/* Ep01 scenes 6–10: exam, mustache, rain, Valeria's books, penalty. */
function paperFlat(g, x, y, s = 1, mark) { g.save(); g.translate(x, y); g.scale(s, s); shape(g, q => { q.moveTo(-46, -10); q.lineTo(46, -10); q.lineTo(54, 10); q.lineTo(-54, 10); q.closePath(); }, '#fbfaf6', 3);
  if (mark) { g.strokeStyle = '#c0262d'; g.lineWidth = 3; g.beginPath(); g.ellipse(26, 0, 14, 6, 0, 0, 7); g.stroke(); } g.restore(); }
function bigPaper(g, a, t) { if (a <= 0) return; g.save(); g.globalAlpha = clamp(a); g.translate(W / 2, H / 2 + (1 - outC(a)) * 300); g.rotate(-.04);
  shape(g, q => q.rect(-330, -420, 660, 840), '#fbfaf6', 6); text(g, 'EXAMEN DE MATEMÁTICAS', 0, -330, 52, OUT, 'Bangers', 'center');
  g.strokeStyle = '#9fb4d6'; g.lineWidth = 3; for (let i = 0; i < 9; i++) { g.beginPath(); g.moveTo(-280, -250 + i * 60); g.lineTo(280, -250 + i * 60); g.stroke(); }
  for (let i = 0; i < 6; i++) text(g, ['x = 3', 'x = −5', '✓', '(x+5)(x−3)=0', '✓', 'Δ = 64'][i], -240, -205 + i * 60, 40, '#3a6fb0', 'ComicNeue');
  const k = R(t, 0, .4, back); g.save(); g.translate(170, 200); g.scale(k, k); g.rotate(-.15); g.strokeStyle = '#c0262d'; g.lineWidth = 10; g.beginPath(); g.ellipse(0, 0, 150, 100, 0, 0, 7); g.stroke();
  text(g, '10/10', 0, 40, 130, '#c0262d', 'Bangers', 'center'); g.restore(); g.restore(); }
function textbook(g, x, y, s = 1, page = 0) { g.save(); g.translate(x, y); g.scale(s, s);
  shape(g, q => { q.moveTo(-110, -70); q.lineTo(0, -60); q.lineTo(110, -70); q.lineTo(110, 70); q.lineTo(0, 80); q.lineTo(-110, 70); q.closePath(); }, '#2f6db0', 5);
  shape(g, q => { q.moveTo(-100, -62); q.lineTo(-4, -52); q.lineTo(-4, 70); q.lineTo(-100, 62); q.closePath(); }, '#fbfaf6', 3); shape(g, q => { q.moveTo(100, -62); q.lineTo(4, -52); q.lineTo(4, 70); q.lineTo(100, 62); q.closePath(); }, '#fbfaf6', 3);
  g.strokeStyle = '#9aa3ad'; g.lineWidth = 3; for (let i = 0; i < 5; i++) { g.beginPath(); g.moveTo(-88, -36 + i * 20); g.lineTo(-16, -30 + i * 20); g.moveTo(16, -30 + i * 20); g.lineTo(88, -36 + i * 20); g.stroke(); }
  if (page > 0 && page < 1) { const a = page * Math.PI; shape(g, q => { q.moveTo(0, -56); q.lineTo(100 * Math.cos(a), -62); q.lineTo(100 * Math.cos(a), 62); q.lineTo(0, 74); q.closePath(); }, '#ffffff', 3); }
  g.restore(); }
function seated(name, x, extra = {}) { return Object.assign({ x, y: FEET, s: S0, sit: 1, hL: [-62, -296], hR: [62, -296], armsFront: 1 }, extra); }

/* ================================================================ 6. the exam */
SC.s06 = (X, t) => {
  const tc = Lm('s06_03', .6), tr = Lt('s06_06') + .1, claps = [{ t: tc }, { t: tr }], wt = worldClock(t, claps), fz = isFrozen(t, claps);
  const cam = shots(t, (typeof claps !== 'undefined' ? claps : []), [
    { t: 0, cx: 960, cy: 560, z: 1.0, z2: 1.04 },
    { t: Lt('s06_02') - .05, cx: 760, cy: 600, z: 1.7 },
    { t: Lt('s06_04') - .05, cx: 800, cy: 600, z: 1.5, z2: 1.6 },
    { t: Lm('s06_04', .55), cx: 1070, cy: 470, z: 2.2, z2: 2.35 },
    { t: Lt('s06_06') - .05, cx: 900, cy: 580, z: 1.3 },
    { t: Lt('s06_06b') - .05, cx: 1050, cy: 470, z: 2.1, z2: 2.2 },
    { t: Lt('s06_07') - .05, cx: 900, cy: 580, z: 1.3 },
    { t: Lt('s06_08') - .05, cx: 940, cy: 540, z: 1.55, z2: 1.62 },
  ]);
  const st = stage(cam); st.wld(g => { drawSet(g, 'classroom'); teacherDesk(g, 1690); });
  const W0 = { still: fz, t: wt, blink: fz ? 0 : null };
  // classmates
  st.wld(g => { drawChar(g, 'ex2', seated('ex2', 380, { ...W0, look: [0, 10], mouth: -.1, brow: .3 })); });
  st.wld(g => { drawChar(g, 'ex3', seated('ex3', 1260, { ...W0, look: [-4, 10], mouth: -.2 })); });
  // hero
  const hp = seated('tu', 800, { t, mouth: .1, look: [0, 8] });
  if (t > Lt('s06_02') && t < Le('s06_02')) { const u = (t - Lt('s06_02')) / Ld('s06_02'); hp.look = u < .55 ? [-18, 8] : [0, 6]; hp.mouth = u < .55 ? .3 : -.1; if (u > .6) hp.rot = Math.sin((u - .6) * 30) * .07; }
  if (t > Lt('s06_03') && t < tc + .6) { hp.mouth = .9; hp.brow = .4; hp.look = [0, 0]; }
  if (t > tc - .4 && t < tc + .7) { const G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = clapHands(t, tc, G, .25, -40); }
  const reading = t > Lm('s06_03', .85) && t < tr;
  if (reading) { const k = (t - Lm('s06_03', .85)); hp.hL = [-48, -268]; hp.hR = [48, -268]; hp.look = [Math.sin(k * 2) * 6, 16]; hp.rot = Math.sin(k * .9) * .08; hp.mouth = .1; hp.brow = .3;
    hp.holdR = (g, x, y) => textbook(g, x - 48, y - 46, .72, (k * .7) % 1); }
  if (t >= tr && t < Lt('s06_07')) { const k = t - tr; hp.hR = [40 + Math.sin(k * 40) * 14, -300]; hp.look = [4, 14]; hp.mouth = .4; hp.brow = .5;
    if (t > Lm('s06_06', .7)) { hp.hR = [150, -560]; hp.look = [16, -10]; hp.mouth = .7; hp.holdR = (g, x, y) => propPaper(g, x + 4, y - 40, .1, .9); } }
  if (t >= Lt('s06_07')) { hp.look = [16, -8]; hp.mouth = .8; }
  st.col(g => drawChar(g, 'tu', hp));
  // profe walks along the row with the stack, stops beside the hero
  const px = mix(1560, 1040, R(t, .2, Lt('s06_01') + 1.6, lin)), pWalk = !fz && t > .2 && t < Lt('s06_01') + 1.6;
  const pp = { x: px, y: FEET, s: S0, t: wt, still: fz, blink: fz ? 0 : null, walk: pWalk ? 1 : 0, phase: walkPh(px), look: [-14, 10], lid: .45, brow: .7, mouth: -.25, hR: [-40, -380], armsFront: 0,
    holdR: (g, x, y) => { for (let i = 0; i < 4; i++) propPaper(g, x - 10, y - 30 - i * 4, -.1, .8); } };
  if (t > Lt('s06_06') + .6) { pp.hR = [-70, -470]; pp.holdR = (g, x, y) => propPaper(g, x, y - 46, -.05, 1); pp.lid = .2; pp.brow = .9;
    const k = R(t, Lt('s06_08'), Le('s06_08') + 1.2, lin), n = Math.floor(k * 8); pp.look = n % 2 ? [-18, 4] : [0, -16]; pp.rot = n % 2 ? .06 : -.04; if (t > Le('s06_08')) { pp.wide = .5; pp.mouth = -.5; } }
  if (speaking(t, 's06_06b')) { pp.hR = [-60, -320]; pp.holdR = (g, x, y) => propPaper(g, x, y - 30, -.05, 1); pp.open = talk(t, 's06_06b'); pp.look = [-18, 2]; pp.lid = .35; pp.brow = .9; pp.mouth = -.3; }
  st.wld(g => drawChar(g, 'profe', pp));
  st.wld(g => { desk(g, 380, FEET + 6, .9); desk(g, 800, FEET + 6, .9); desk(g, 1260, FEET + 6, .9); });
  if (t > Lt('s06_01') + 1.6) st.wld(g => { paperFlat(g, 420, 708, .9); paperFlat(g, 1290, 708, .9); });
  if (t > Lt('s06_01') + 1.6 && !(t > Lm('s06_06', .7))) st.col(g => paperFlat(g, 830, 708, .9, t > tr + .4));
  const cp = worldToScreen(cam, ...clapPoint('tu', hp));
  compose2(X, st, freezeState(t, [{ t: tc, x: cp[0], y: cp[1], screen: 1 }, { t: tr, x: cp[0], y: cp[1], screen: 1 }], cam));
  if (t > Lt('s06_04') - .1 && t < Lm('s06_04', .55)) { const hrs = 1 + Math.min(2, Math.floor(R(t, Lt('s06_04'), Lm('s06_04', .5), lin) * 3)); bigCounter(X, 'ESTUDIANDO:', hrs + (hrs > 1 ? ' HORAS' : ' HORA'), R(t, Lt('s06_04') - .1, Lt('s06_04') + .2, outC)); }
  if (t > Lt('s06_07') - .05 && t < Lt('s06_08') - .05) bigPaper(X, R(t, Lt('s06_07') - .05, Lt('s06_07') + .25, outC), t - Lt('s06_07'));
  if (t > Lt('s06_08')) { const n = Math.min(4, 1 + Math.floor(R(t, Lt('s06_08'), Le('s06_08') + 1.2, lin) * 4)); sticker(X, 'REVISIÓN #' + n, R(t, Lt('s06_08'), Lt('s06_08') + .2, outC), 70, 60, 64); }
};

/* ================================================================ 7. the marker mustache */
function boardOverlay(g, l1, l2) { shape(g, q => q.rect(430, 130, 1060, 420), '#f8fbfb', 0); text(g, l1, 520, 260, 74, '#3a6fb0', 'ComicNeue'); text(g, l2, 520, 380, 64, '#c0262d', 'ComicNeue'); }
SC.s07 = (X, t) => {
  const tc = Lm('s07_02', .22), tr = Lt('s07_04') + .05, claps = [{ t: tc }, { t: tr }], wt = worldClock(t, claps), fz = isFrozen(t, claps);
  const drawStart = Lm('s07_02', .6), drawEnd = Le('s07_02') + 1.0, wake = tr + .5, mirror = Lm('s07_04', .35), nod = Lt('s07_04b') - .05;
  const cam = shots(t, (typeof claps !== 'undefined' ? claps : []), [
    { t: 0, cx: 760, cy: 580, z: 1.15, z2: 1.2 },
    { t: drawStart - .1, cx: 1000, cy: 520, z: 2.2, z2: 2.35 },
    { t: Lt('s07_03') - .05, cx: 860, cy: 560, z: 1.45 },
    { t: tr - .05, cx: 800, cy: 580, z: 1.2 },
    { t: mirror, cx: 1730, cy: 330, z: 2.4, z2: 2.5 },
    { t: nod - .1, cx: 1000, cy: 520, z: 2.0 },
    { t: Lt('s07_05') - .1, cx: 1000, cy: 560, z: 1.35, z2: 1.45 },
  ]);
  const st = stage(cam); st.wld(g => { drawSet(g, 'classroom'); boardOverlay(g, 'HISTORIA', 'Independencia: 1810'); });
  const W0 = { still: fz, t: wt, blink: fz ? 0 : null };
  st.wld(g => drawChar(g, 'ex4', seated('ex4', 1420, { ...W0, look: [0, 12], mouth: -.1 })));
  // Nacho asleep on his desk, then wakes and admires the mustache
  const hp0 = {};
  const asleep = wt < wake - (tr - worldClock(tr, claps)) ? true : false;
  const awakeK = R(t, wake, wake + .4);
  const np = seated('nacho', 1000, { ...W0, marker: R(t, drawStart, drawEnd, lin), hL: [-90, -290], hR: [90, -290] });
  if (t < wake) { np.sleep = 1; np.hy = 70; np.rot = .28; np.mouth = .4; }
  else { np.hy = 70 * (1 - awakeK); np.rot = .28 * (1 - awakeK); np.look = t < nod ? [18, -6] : [0, 0]; np.brow = t > mirror + .4 ? .8 : .2; np.wide = t > mirror + .4 && t < nod ? .5 : 0; np.mouth = t > nod ? .9 : .1;
    if (t > nod) np.hy += Math.abs(Math.sin((t - nod) * 7)) * -14 * (1 - R(t, nod + 1, nod + 1.4)); }
  if (t > Lt('s07_05') - .1) { Object.assign(hp0, { sit: 0, hL: null, hR: null, armsFront: 0, mouth: .9, look: [14, 0] }); Object.assign(np, { sit: 0, hL: POSE.hips(charGeom(CAST.nacho, { sit: 0 }))[0], hR: POSE.hips(charGeom(CAST.nacho, { sit: 0 }))[1], armsFront: 0, mouth: 1, look: [0, 0], hy: 0, rot: 0, brow: .6, lid: .3 }); }
  if (speaking(t, 's07_04b')) { np.open = talk(t, 's07_04b'); np.lid = .35; np.brow = .5; }
  st.wld(g => drawChar(g, 'nacho', np));
  // hero: seated, then walks over with a marker while time is stopped
  const out = t > tc + .4 && t < tr;
  let hp;
  if (!out) { hp = Object.assign(seated('tu', 520, { t, look: [16, 0], mouth: .7, brow: -.3 }), hp0); if (t > tc - .4 && t < tc + .5) { const G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = clapHands(t, tc, G, .2, -40); }
    if (t > tr - .4 && t < tr + .5) { const G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = clapHands(t, tr, G, .2, -40); hp.mouth = .9; }
    if (t > tr + .5) { hp.look = [18, 0]; hp.mouth = t > nod ? .9 : .3; } }
  else { const hx = mix(520, 860, R(t, tc + .4, drawStart - .1, lin)); hp = { x: hx, y: FEET, s: S0, t, walk: t < drawStart - .1 ? 1 : 0, phase: walkPh(hx), look: [16, 8], mouth: .8, brow: -.4 };
    if (t > drawStart - .1 && t < drawEnd + .2) { const k = R(t, drawStart, drawEnd, lin), ang = (k * 2 - 1); hp.hR = [(1000 - 860 + ang * 48) / S0, (628 - FEET) / S0 + Math.sin(k * 30) * 4]; hp.rot = .1;
      hp.holdR = (g, x, y) => { g.save(); g.translate(x, y); g.rotate(-.6); shape(g, q => rrPath(q, -8, -70, 16, 70, 6), '#2a2a3a', 3); shape(g, q => rrPath(q, -8, -20, 16, 20, 4), '#ffffff', 2); g.restore(); }; }
    if (t > Lt('s07_03') - .05) { [hp.hL, hp.hR] = POSE.hips(charGeom(CAST.tu, hp)); hp.holdR = null; hp.mouth = 1; hp.look = [14, 0]; hp.rot = 0; } }
  st.col(g => drawChar(g, 'tu', hp));
  if (t < Lt('s07_05') - .1) st.wld(g => { desk(g, 520, FEET + 6, .9); desk(g, 1000, FEET + 6, .9); });
  st.wld(g => desk(g, 1420, FEET + 6, .9));
  // reflection in the window glass
  if (t > mirror - .1 && t < nod - .1) st.wld(g => { g.save(); g.beginPath(); g.rect(1600, 160, 260, 340); g.clip(); g.globalAlpha = .5; drawHead(g, CAST.nacho, 1730, 330, 0, { marker: 1, look: [0, 0], wide: .4, brow: .8 }); g.restore(); });
  const cp = worldToScreen(cam, ...clapPoint('tu', hp));
  compose2(X, st, freezeState(t, [{ t: tc, x: cp[0], y: cp[1], screen: 1 }, { t: tr, x: cp[0], y: cp[1], screen: 1 }], cam));
  if (t < tc) zzz(X, ...worldToScreen(cam, 1040, 520), t);
  if (t > Lt('s07_05') - .1) { const days = ['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES'], k = Math.min(4, Math.floor(R(t, Lt('s07_05'), T().dur - .4, lin) * 5)); sticker(X, days[k], 1, 70, 60, 80); }
};

/* ================================================================ 8. frozen rain */
function rain(g, wt, x0, y0, x1, y1, n, seed, frozen, skip) { const r = rnd(seed); g.save(); g.beginPath(); g.rect(x0, y0, x1 - x0, y1 - y0); g.clip();
  for (let i = 0; i < n; i++) { const x = x0 + r() * (x1 - x0), sp = 900 + r() * 500, y = y0 + ((r() * (y1 - y0) + wt * sp) % (y1 - y0 + 80)) - 40, len = frozen ? 18 : 46;
    if (skip && skip(x, y)) continue;
    if (frozen) { g.fillStyle = 'rgba(210,235,255,.9)'; g.strokeStyle = 'rgba(40,60,90,.8)'; g.lineWidth = 2; g.beginPath(); g.ellipse(x, y, 4, 9, 0, 0, 7); g.fill(); g.stroke(); g.fillStyle = '#ffffff'; g.beginPath(); g.arc(x - 1, y - 4, 1.5, 0, 7); g.fill(); }
    else { g.strokeStyle = 'rgba(220,235,255,.75)'; g.lineWidth = 3; g.beginPath(); g.moveTo(x, y); g.lineTo(x - 6, y + len); g.stroke(); } }
  g.restore(); }
function umbrellaStand(g, x) { shape(g, q => rrPath(q, x - 34, 820, 68, 120, 8), '#5a6fb0', 5); tube(g, [[x - 10, 830], [x - 30, 600]], '#c0262d', 14); shape(g, q => { q.moveTo(x - 30, 560); q.quadraticCurveTo(x - 60, 610, x - 46, 700); q.lineTo(x - 18, 700); q.quadraticCurveTo(x - 6, 610, x - 30, 560); }, '#c0262d', 4); }
SC.s08 = (X, t) => {
  const tc = Lt('s08_02') + .15, claps = [{ t: tc }], wt = worldClock(t, claps), fz = isFrozen(t, claps), home = Lt('s08_05') - .1;
  if (t < home) {
    const cam = shots(t, (typeof claps !== 'undefined' ? claps : []), [{ t: 0, cx: 620, cy: 560, z: 1.25 }, { t: Lt('s08_03') - .05, cx: 900, cy: 520, z: 2.0, z2: 2.2 }, { t: Lt('s08_04') - .05, cx: 960, cy: 560, z: 1.0 }]);
    const st = stage(cam); st.wld(g => drawSet(g, 'streetRain'));
    const awning = (x, y) => x > 230 && x < 640 && y > 380;
    const walkT0 = Lt('s08_04') - .2, hx = t < walkT0 ? 420 : mix(420, 2050, R(t, walkT0, home - .2, lin));
    const hp = { x: hx, y: FEET, s: S0, t, mouth: -.5, brow: .6, look: [0, -14], walk: t > walkT0 ? 1 : 0, phase: walkPh(hx) };
    if (t > tc - .4 && t < tc + .5) { const G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = clapHands(t, tc, G, .2); hp.armsFront = 1; }
    if (t > tc + .3) { hp.mouth = .7; hp.brow = .2; hp.look = [10, -10]; }
    if (t > Lt('s08_03') + .5 && t < walkT0) { hp.x = mix(420, 760, R(t, Lt('s08_03') + .5, Lt('s08_03') + 1.6, lin)); hp.walk = t < Lt('s08_03') + 1.6 ? 1 : 0; hp.phase = walkPh(hp.x); hp.hR = [130, -560]; hp.look = [16, -14]; hp.wide = .3; }
    if (t >= walkT0) { const k = t - walkT0; hp.x = mix(760, 2050, R(t, walkT0, home - .2, lin)); hp.phase = walkPh(hp.x); hp.lean = Math.sin(k * 5) * .12; hp.hy = Math.abs(Math.sin(k * 5)) * 22; hp.look = [16, 0]; hp.mouth = .6; }
    st.col(g => drawChar(g, 'tu', hp));
    st.wld(g => { shape(g, q => q.rect(230, 352, 410, 34), '#7a5a3a', 5); rain(g, wt, 0, 0, W, FEET, fz ? 520 : 420, 7, fz, awning); });
    const cp = worldToScreen(cam, ...clapPoint('tu', hp));
    compose2(X, st, freezeState(t, [{ t: tc, x: cp[0], y: cp[1], screen: 1 }], cam));
    if (t > Lt('s08_03') && t < Lt('s08_04')) { X.save(); X.globalCompositeOperation = 'screen'; const r = rnd(4); for (let i = 0; i < 26; i++) { const u = (t * .7 + r()) % 1; X.globalAlpha = Math.sin(u * Math.PI) * .9; X.fillStyle = '#ffffff'; const x = r() * W, y = r() * H; X.beginPath(); X.moveTo(x, y - 14); X.lineTo(x + 4, y); X.lineTo(x, y + 14); X.lineTo(x - 4, y); X.fill(); } X.restore(); }
  } else {
    const k = t - home, cam = shots(t, (typeof claps !== 'undefined' ? claps : []), [{ t: home, cx: 900, cy: 560, z: 1.15, z2: 1.2 }, { t: Lm('s08_06', .3), cx: 1000, cy: 520, z: 1.5, z2: 1.58 }]);
    const st = stage(cam); st.wld(g => { drawSet(g, 'kitchen'); g.save(); rain(g, t * 1.0, 1180, 140, 1740, 470, 90, 3, false); g.restore(); umbrellaStand(g, 140); });
    const hx = mix(260, 720, R(t, home, home + 1.6, lin));
    st.col(g => drawChar(g, 'tu', { x: hx, y: FEET, s: S0, t, walk: k < 1.6 ? 1 : 0, phase: walkPh(hx), mouth: .9, brow: -.2, look: [14, 0] }));
    const u = Lm('s08_06', .5), mp = { x: 1250, y: FEET, s: S0, t, look: [-16, 0], mouth: .1, hR: [-36, -330], holdR: (g, x, y) => propMug(g, x - 10, y - 20, .9) };
    if (t > Lm('s08_06', .25)) { mp.look = [-20, 12]; mp.lid = .3; }
    if (t > u) { mp.look = [-18, 0]; mp.lid = .55; mp.brow = .6; mp.mouth = -.3; }
    if (t > Lm('s08_06', .82)) { mp.look = [8, -6]; mp.lid = .2; mp.brow = null; mp.mouth = .2; mp.hR = [-24, -470]; }
    st.col(g => drawChar(g, 'mama', mp));
    compose2(X, st, { amt: 0 });
    sticker(X, '100% SECO', R(t, Lt('s08_05') + .2, Lt('s08_05') + .5, outC) * (1 - R(t, Lt('s08_06') + .5, Lt('s08_06') + .8)), 70, 60, 84);
  }
};

/* ================================================================ 9. Valeria's books */
const BOOKS = [{ w: 62, h: 84, c: '#4f86b8' }, { w: 54, h: 72, c: '#c0262d' }, { w: 46, h: 62, c: '#5aa37a' }, { w: 38, h: 52, c: '#f0d06a' }];
SC.s09 = (X, t) => {
  const trip = Lm('s09_01', .55), tc = Lt('s09_03') + .15, tr = Lm('s09_04', .3), claps = [{ t: tc }, { t: tr }], wt = worldClock(t, claps), fz = isFrozen(t, claps);
  const cam = shots(t, (typeof claps !== 'undefined' ? claps : []), [
    { t: 0, cx: 1000, cy: 560, z: 1.0, w: 2600 },
    { t: Lt('s09_02') - .05, cx: 520, cy: 470, z: 2.2, z2: 2.3, w: 2600 },
    { t: Lt('s09_03') - .05, cx: 920, cy: 560, z: 1.15, w: 2600 },
    { t: Lt('s09_05') - .05, cx: 1180, cy: 500, z: 1.9, z2: 2.0, w: 2600 },
    { t: Lt('s09_07') - .05, cx: 520, cy: 520, z: 1.8, z2: 1.9, w: 2600 },
  ]);
  const st = stage(cam); st.wld(g => drawSet(g, 'hallway'));
  // Valeria walks in carrying the books, trips at `trip`, books fly; frozen in the air at the clap
  const vx = mix(1750, 1180, R(wt, .1, trip, lin)), vWalk = wt < trip;
  const vp = { x: vx, y: FEET, s: S0, t: wt, still: fz, blink: fz ? 0 : null, walk: vWalk ? 1 : 0, phase: walkPh(vx), flip: -1, look: [-6, 6], mouth: .2 };
  const G = charGeom(CAST.valeria, vp); [vp.hL, vp.hR] = POSE.carry(G);
  const fly = clamp((wt - trip) / 1.4);
  if (wt > trip) { vp.lean = -.18 * bump(wt, trip, trip + .5); vp.wide = .7; vp.open = .5; vp.hL = [-120, G.top - 30]; vp.hR = [120, G.top - 30]; vp.flip = 1; }
  // books: held, flying, back in her hands sorted by size
  const sorted = t > Lm('s09_03', .9);
  // twist clue: while "frozen", her eyes quietly follow the hero
  if (fz && t > tc + .8) { vp.look = [mix(-4, -16, R(t, tc + .8, tc + 2.5)), 2]; vp.brow = R(t, Lm('s09_03', .6), Lm('s09_03', .8)) * .5; }
  if (sorted) { vp.hL = [-70, G.top + 190]; vp.hR = [70, G.top + 190]; vp.lean = 0; vp.wide = 0; vp.open = 0; vp.flip = 1; }
  if (t > tr + .2) { const u = t - tr; vp.look = [Math.sin(u * 2.5) * 16, 8]; vp.mouth = -.1; vp.brow = .3; }
  if (speaking(t, 's09_05b')) { vp.open = talk(t, 's09_05b'); vp.look = [12, -4]; vp.brow = .5; }
  if (t > Lt('s09_06') - .05) { vp.look = [6, -18]; vp.lid = .45; vp.brow = .9; vp.mouth = -.3; }
  if (typeof FLASH !== 'undefined' && FLASH) { vp.look = [-16 + Math.sin(t * 3) * 4, 2]; vp.mouth = .8; vp.lid = .25; vp.wide = 0; vp.open = 0; vp.brow = t > Lm('s09_03', .75) ? .9 : .3; vp.still = 0; vp.t = t; vp.blink = null; }
  ((typeof FLASH !== 'undefined' && FLASH) ? st.col : st.wld)(g => drawChar(g, 'valeria', vp));
  const vS = S0 * CAST.valeria.s;
  if (!sorted) st.wld(g => BOOKS.forEach((b, i) => { if (wt < trip) { propBook(g, vx, FEET + (G.top + 150) * vS - i * 22, b.w * 1.2, b.h * .5, b.c, 0); return; }
      const vx0 = (i - 1.5) * 160, vy0 = -620 - i * 90, gx = vx + vx0 * fly * 1.2, gy = FEET + (G.top + 150) * vS + vy0 * fly + 700 * fly * fly;
      if (t > Lm('s09_03', .2 + i * .14)) return; propBook(g, gx, gy, b.w, b.h, b.c, fly * (i + 1) * 2.2); }));
  if (sorted) st.wld(g => BOOKS.forEach((b, i) => propBook(g, vx, FEET + (G.top + 190) * vS - 20 - (BOOKS.length - 1 - i) * 0 - i * 20, b.w * 1.3, b.h * .45, b.c, 0)));
  // hero: by the lockers; zips around while time is stopped
  let hp = { x: 520, y: FEET, s: S0, t, look: [16, 0], mouth: .4 };
  if (t > Lt('s09_02') - .05) { hp.blush = 1; hp.mouth = .8; hp.look = [18, -4]; hp.lid = .2; }
  if (t > tc - .4 && t < tc + .4) { const G2 = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = clapHands(t, tc, G2, .15); hp.armsFront = 1; hp.blush = 0; }
  let zip = false;
  if (t > tc + .35 && t < Lm('s09_03', .95)) { zip = true; const k = R(t, tc + .35, Lm('s09_03', .95), lin), stops = [520, 1000, 1180, 1340, 1060, 1180]; const seg = k * (stops.length - 1), i = Math.min(stops.length - 2, Math.floor(seg)), u = seg - i;
    hp.x = mix(stops[i], stops[i + 1], io(clamp(u * 1.6))); hp.walk = 1; hp.phase = walkPh(hp.x) * 2.5; hp.lean = (stops[i + 1] - stops[i]) > 0 ? .1 : -.1; hp.mouth = .9; hp.blush = 0;
    hp.hL = [-70, -380]; hp.hR = [70, -380]; const carry = Math.floor(k * 5); hp.holdR = (g, x, y) => { for (let j = 0; j < Math.min(4, carry); j++) propBook(g, x - 70, y - 10 - j * 18, BOOKS[3 - j].w * 1.2, BOOKS[3 - j].h * .42, BOOKS[3 - j].c, 0); }; }
  if (t >= Lm('s09_03', .95) && t < tr + .4) { hp.x = mix(1180, 520, R(t, Lm('s09_03', .95), Le('s09_03') + .5, lin)); hp.walk = 1; hp.phase = walkPh(hp.x) * 2.5; if (t > Le('s09_03') + .5) hp.walk = 0; hp.mouth = .9;
    const G2 = charGeom(CAST.tu, hp); if (t > tr - .4) { [hp.hL, hp.hR] = clapHands(t, tr, G2, .15); hp.armsFront = 1; } }
  if (t > tr + .4) { hp.look = [16, 0]; hp.mouth = .2; hp.blush = .6; }
  if (t > Lt('s09_07') - .05) { hp.hR = [30, -620]; hp.rot = .1; hp.mouth = -.4; hp.blink = 1; hp.blush = 0; }
  st.col(g => drawChar(g, 'tu', hp));
  const cp = worldToScreen(cam, ...clapPoint('tu', hp));
  compose2(X, st, freezeState(t, [{ t: tc, x: cp[0], y: cp[1], screen: 1 }, { t: tr, x: cp[0], y: cp[1], screen: 1 }], cam));
  if (zip) speedLines(X, ...worldToScreen(cam, hp.x, 600), .8, t);
  if (t > Lt('s09_02') - .05 && t < Lt('s09_03') - .05) { X.save(); for (let i = 0; i < 4; i++) { const u = (t * .9 + i / 4) % 1, [sx, sy] = worldToScreen(cam, 580 + i * 30 - 40, 330 - u * 120); X.globalAlpha = Math.sin(u * Math.PI); text(X, '♥', sx, sy, 50 + i * 6, '#e0546a', 'Arial', 'center', OUT, 5); } X.restore(); }
  if (t > Lt('s09_06')) { const [bx, by] = worldToScreen(cam, 1260, 300); bubble(X, '¿FANTASMAS?', bx, by, R(t, Lt('s09_06'), Lt('s09_06') + .3, outC) * (1 - R(t, Lt('s09_07') - .3, Lt('s09_07'))), 56); }
};

/* ================================================================ 10. the penalty */
SC.s10 = (X, t) => {
  const kick = Lt('s10_02') + .25, tc = Lt('s10_03') + .1, tr = Lt('s10_05') + .1, claps = [{ t: tc }, { t: tr }], wt = worldClock(t, claps), fz = isFrozen(t, claps);
  const pick = Lm('s10_04', .3), place = Lm('s10_04', .9), goalT = tr;
  const cam = shots(t, (typeof claps !== 'undefined' ? claps : []), [
    { t: 0, cx: 960, cy: 560, z: 1.0 },
    { t: kick + .05, cx: 760, cy: 600, z: 1.1 },
    { t: Lt('s10_04') - .05, cx: 900, cy: 560, z: 1.05 },
    { t: place - .7, cx: 1320, cy: 420, z: 1.8 },
    { t: Lt('s10_06') - .05, cx: 1080, cy: 560, z: 1.15 },
    { t: Lt('s10_07') - .05, cx: 1590, cy: 500, z: 2.8, z2: 2.95 },
  ]);
  const st = stage(cam); st.wld(g => { drawSet(g, 'field'); goal(g, 0); });
  const W0 = { still: fz, t: wt, blink: fz ? 0 : null };
  // spectators
  const cheer = t > goalT + .2 && t < Lt('s10_07');
  for (const [n, x] of [['ex1', 200], ['ex4', 330], ['ex5', 460]]) { const p = { ...W0, x, y: 700, s: .5, look: [10, 0], mouth: .3 }; if (cheer) { const G = charGeom(CAST[n], p); [p.hL, p.hR] = POSE.stretch(1, G); p.jump = Math.abs(Math.sin(t * 9 + x)) * 50; p.open = .7; p.blink = 1; } st.wld(g => drawChar(g, n, p)); }
  // Nacho in goal (far away, small)
  const np = { ...W0, x: 1590, y: 650, s: .4, handCol: '#f08a3a', look: [-12, 6], mouth: -.1, brow: .4, hL: [-150, -380], hR: [150, -380] };
  if (t > kick && t < tc) { np.lean = -.25 * R(t, kick, kick + .5); np.look = [-18, -4]; }
  if (t > Lt('s10_07') - .05) { Object.assign(np, { hL: [-40, -470], hR: [40, -470], look: [0, 20], mouth: -.5, wide: .3, brow: .8, lean: 0, rot: Math.sin(t * 1.3) * .08, blink: autoBlink(t, 2), still: 0, t }); }
  if (cheer) { np.mouth = -.5; np.wide = .6; }
  if (speaking(t, 's10_07b')) { np.open = talk(t, 's10_07b'); np.wide = .5; }
  st.wld(g => drawChar(g, 'nacho', np));
  // ball: shot flies wide toward the school, freezes mid-air, gets carried, placed in the top corner, then hits the net
  const FLY = 4.0, b0 = [860, 900], b1 = [170, 360];
  const ballAt = u => ({ x: mix(b0[0], b1[0], u), y: mix(b0[1], b1[1], u) - Math.sin(u * Math.PI) * 200, r: mix(34, 18, u), rot: u * 12 });
  const uF = clamp((worldClock(tc, claps) - worldClock(kick, claps)) / FLY), BF = ballAt(uF), corner = [1338, 318];
  let ball = null, carried = false, netBulge = 0;
  if (t < kick) ball = { x: 860, y: 900, r: 34, rot: 0 };
  else if (t < pick) ball = ballAt(clamp((wt - worldClock(kick, claps)) / FLY));
  else if (t < place) carried = true;
  else if (t < goalT) ball = { x: corner[0], y: corner[1], r: 18, rot: 0 };
  else { const u = clamp((t - goalT) / .5); ball = { x: corner[0] + 130 * u, y: corner[1] + 200 * u * u, r: 18, rot: u * 4 }; netBulge = bump(t, goalT, goalT + .7); }
  if (ball && (t < pick || t >= place)) st.wld(g => propBall(g, ball.x, ball.y, ball.r, ball.rot));
  st.wld(g => { goal(g, 1); if (netBulge) { g.save(); g.strokeStyle = 'rgba(255,255,255,.8)'; g.lineWidth = 3; for (let i = 0; i < 6; i++) { g.beginPath(); g.arc(1470, 430, 60 + i * 18 * netBulge, -1.2, 1.2); g.stroke(); } g.restore(); } });
  // hero
  let hp = { x: 700, y: 930, s: S0, t, look: [16, 0], mouth: .5, brow: -.2 };
  if (t < kick) { hp.x = mix(620, 790, R(t, Lm('s10_01', .55), kick - .05, lin)); hp.walk = t > Lm('s10_01', .55) ? 1 : 0; hp.phase = walkPh(hp.x) * 1.6; }
  else { hp.x = 800; if (t < kick + .4) { hp.walk = 1; hp.phase = Math.PI * .5; hp.lean = .12; } hp.look = [-14, -14]; hp.mouth = -.4; hp.wide = .4; }
  if (t > tc - .4 && t < tc + .4) { const G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = clapHands(t, tc, G, .15); hp.armsFront = 1; }
  const hs = .5, reachX = BF.x + 60;
  if (t > tc + .4 && t < pick) { const u = R(t, tc + .4, pick - .3, lin); hp.x = mix(800, reachX, u); hp.y = mix(930, 660, u); hp.s = mix(S0, hs, u); hp.walk = u < 1 ? 1 : 0; hp.phase = walkPh(hp.x); hp.look = [-14, -12]; hp.mouth = .2; hp.flip = -1;
    if (t > pick - .3) { hp.flip = 1; hp.hR = [(BF.x - reachX) / hs, (BF.y - 660) / hs]; hp.look = [-14, -18]; } }
  if (carried) { const u = R(t, pick, place - .55, lin), s2 = mix(hs, .42, u); hp.x = mix(reachX, 1290, u); hp.y = mix(660, 650, u); hp.s = s2; hp.walk = u < 1 ? 1 : 0; hp.phase = walkPh(hp.x) * 1.4; hp.flip = 1;
    hp.hL = [-60, -330]; hp.hR = [60, -300]; hp.armsFront = 1; hp.look = [0, 12]; hp.mouth = .8; hp.lean = Math.sin(t * 6) * .04;
    hp.holdR = (g, x, y) => propBall(g, x - 60, y - 40, 34, Math.sin(t * 6) * .3);
    if (t > place - .55) { hp.x = 1290; hp.walk = 0; hp.jump = 150 * bump(t, place - .55, place + .15); hp.hR = [(corner[0] - 1290) / .42, (corner[1] - 650) / .42 + hp.jump]; hp.hL = [60, -620]; hp.look = [10, -20]; hp.holdR = (g, x, y) => propBall(g, x, y - 30, 34, 0); } }
  if (t >= place && t < goalT) { hp.x = mix(1290, 1050, R(t, place, place + .8, lin)); hp.y = 650; hp.s = .42; hp.walk = t < place + .8 ? 1 : 0; hp.phase = walkPh(hp.x); hp.flip = -1; hp.mouth = .9;
    if (t > goalT - .4) { const G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = clapHands(t, goalT, G, .15); hp.armsFront = 1; } }
  if (t >= goalT) { hp.x = 1050; hp.y = 650; hp.s = .42; hp.flip = 1; if (cheer) { const G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = POSE.stretch(1, G); hp.jump = Math.abs(Math.sin(t * 8)) * 60; hp.blink = 1; hp.mouth = 1; } }
  st.col(g => drawChar(g, 'tu', hp));
  const cp = worldToScreen(cam, ...clapPoint('tu', hp));
  compose2(X, st, freezeState(t, [{ t: tc, x: cp[0], y: cp[1], screen: 1 }, { t: tr, x: cp[0], y: cp[1], screen: 1 }], cam));
  if (t > Lt('s10_06') - .05 && t < Lt('s10_07') - .05) titleCard(X, '¡GOOOL!', '', R(t, Lt('s10_06') - .05, Lt('s10_06') + .25, outC), t);
  if (t > Lt('s10_07')) { const k = R(t, Lt('s10_07'), T().dur, lin); X.save(); X.globalCompositeOperation = 'multiply'; X.fillStyle = `rgba(255,${Math.round(mix(255, 170, k))},${Math.round(mix(255, 120, k))},1)`; X.fillRect(0, 0, W, H); X.restore();
    sticker(X, ['14:00', '15:30', '17:00', '18:45'][Math.min(3, Math.floor(k * 4))], 1, 70, 60, 80); }
};
