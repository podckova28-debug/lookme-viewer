/* Ep06 — scenes 6–11: the board and the backpack, the week without pain, Pepe pecks, the ankle, slaps and high fives, nothing hurts inside */

/* ================================================================ 6. the profe's backpack: knee, elbow, forehead */
function backpack(g, x, y, s = 1) { g.save(); g.translate(x, y); g.scale(s, s); shape(g, q => rrPath(q, -60, -110, 120, 110, 26), '#4a6fa8', 5); shape(g, q => rrPath(q, -40, -60, 80, 44, 10), '#3a5a8c', 4);
  shape(g, q => { q.moveTo(-30, -110); q.quadraticCurveTo(0, -150, 30, -110); }, null, 6); g.restore(); }
function eraser(g, x, y, rot = 0) { g.save(); g.translate(x, y); g.rotate(rot); shape(g, q => rrPath(q, -40, -14, 80, 28, 5), '#2e333d', 4); shape(g, q => rrPath(q, -40, 4, 80, 10, 3), '#c9c2b8', 0); g.restore(); }
function notebookPage(X, a, t, t0s, rows, title = 'EL DE LOS RIZOS') { if (a <= 0) return; X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.globalAlpha = clamp(a);
  X.fillStyle = 'rgba(10,8,18,.55)'; X.fillRect(0, 0, W, H);
  const s = .85 + .15 * back(a); X.translate(W / 2, H / 2); X.rotate(-.02); X.scale(s, s);
  shape(X, q => rrPath(q, -620, -420, 1240, 840, 18), '#fbf6e6', 8);
  X.strokeStyle = 'rgba(80,140,200,.35)'; X.lineWidth = 3; for (let y = -300; y < 400; y += 92) { X.beginPath(); X.moveTo(-600, y); X.lineTo(600, y); X.stroke(); }
  X.strokeStyle = 'rgba(210,60,60,.55)'; X.beginPath(); X.moveTo(-470, -410); X.lineTo(-470, 410); X.stroke();
  for (let i = 0; i < 7; i++) circ(X, -585, -330 + i * 110, 14, '#2a2430', 0);
  text(X, title, -430, -330, 64, '#c0262d', 'Bangers', 'left');
  rows.forEach(([d, s2], i) => { if (t < t0s[i]) return; const u = clamp((t - t0s[i]) / .6), full = d + ' ' + s2, n = Math.round(u * full.length);
    X.save(); X.font = 'bold 44px ComicNeue'; X.fillStyle = '#2b3a67'; X.textAlign = 'left'; X.fillText(full.slice(0, n), -430, -190 + i * 200); X.restore(); });
  X.restore(); }
SC.s06 = (X, t) => {
  const go = Lt('s06_01') + 1.6, trip = Lm('s06_02', .25), elbow = Lm('s06_02', .55), head = Lm('s06_02', .85), up = Le('s06_02') + .3, book = Lt('s06_06') - .1;
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 540, z: 1.0, z2: 1.04, lock: 1 },
    { t: trip - .4, cx: 1080, cy: 640, z: 1.7, z2: 1.8, lock: 1 },
    { t: Lt('s06_03') - .05, cx: 900, cy: 400, z: 1.6, z2: 1.65, lock: 1 },
    { t: Lt('s06_04') - .05, cx: 1420, cy: 470, z: 2.3, z2: 2.4, lock: 1 },
    { t: Lt('s06_05') - .05, cx: 1000, cy: 470, z: 2.3, z2: 2.4, lock: 1 },
  ]);
  const st = stage(cam); const solved = t > Lm('s06_03', .4);
  st.wld(g => { drawSet(g, 'classroom'); g.save(); g.font = 'bold 54px ComicNeue'; g.fillStyle = '#3a6fb0'; g.fillText('3x + 7 = 19', 420, 260); if (solved) { g.fillStyle = '#2f8f4e'; g.fillText('x = 4  ✓', 420, 340); } g.restore();
    if (t < head - .3) eraser(g, 1100, 584, 0); });
  const pp = standing(1450, { t, flip: -1, look: [-14, 6], mouth: -.1, brow: .4 });
  if (t > trip) { pp.wide = .6; pp.mouth = -.3; pp.brow = .8; pp.look = [-16, 10]; }
  if (t > Lt('s06_04') - .1) { pp.wide = .3; pp.lid = .2; }
  say(pp, t, ['s06_04']);
  st.wld(g => drawChar(g, 'profe', pp)); st.wld(g => teacherDesk(g, 1620));
  st.wld(g => { drawChar(g, 'ex2', seated(470, { t, look: [14, 6], mouth: t > trip ? -.3 : .1, wide: t > trip ? .7 : 0, hL: [-70, -170], hR: [70, -170] })); desk(g, 470, FEET, .8); });
  // you: get up, walk to the board, trip on the backpack (knee), hit the floor (elbow), the eraser drops on your head, get up, solve it
  let hp;
  if (t < go) hp = seated(860, { t, look: [14, 6], mouth: .2, hL: [-70, -170], hR: [70, -170] });
  else { const x = t < trip ? mix(860, 1000, R(t, go, trip, lin)) : t < up ? 1030 : mix(1030, 1080, R(t, up, up + .6, lin)); hp = standing(x, { t, look: [10, 0], mouth: .3, walk: t < trip ? 1 : 0, phase: walkPh(x) });
    if (t > trip && t < up) { const f = R(t, trip, trip + .25, outC); hp.lean = .9 * f; hp.y = FEET + 40 * f; hp.hL = [-160, -260]; hp.hR = [160, -260]; hp.look = [4, 20]; hp.mouth = .2; }
    if (t > up) { hp.look = [-14, -6]; hp.mouth = .6; hp.brow = -.3; }
    if (t > Lt('s06_03')) { hp.hR = [-160, -560]; hp.look = [-16, -14]; hp.flip = 1; }
    if (t > Lt('s06_04')) { hp.hR = null; hp.look = [16, 4]; hp.mouth = .8; } }
  say(hp, t, ['s06_05']);
  st.wld(g => drawHero(g, hp, { bump: t > head + .2 ? .7 : 0 }));
  if (t < go) st.wld(g => desk(g, 860, FEET, .8));
  st.wld(g => backpack(g, 1080, FEET, .9));
  if (t > head - .3 && t < head + 1.2) st.wld(g => { const u = R(t, head - .3, head, inC), [hx, hy] = headPt('tu', hp, 60); eraser(g, mix(1100, hx, u), mix(584, hy, u), u * 2 + (t > head ? (t - head) * 3 : 0)); });
  compose2(X, st, { amt: 0 });
  hits(X, cam, t, [{ t: trip, at: [1030 + 30, 880], cname: 'tu', p: hp, hero: 1 }, { t: elbow, at: [1130, 840], cname: 'tu', p: hp, hero: 1 }, { t: head, at: headPt('tu', hp, 80), cname: 'tu', p: hp, hero: 1 }]);
  [['¡PAF!', trip, 1060, 820], ['¡TOC!', elbow, 1160, 780], ['¡POC!', head, 980, 520]].forEach(([w2, tt, x, y]) => { if (t > tt && t < tt + .7) comicWord(X, w2, ...worldToScreen(cam, x, y), t - tt, 80); });
  notebookPage(X, R(t, book, book + .35, outC), t, [Lt('s06_07') + .1, Lm('s06_07', .55)], [['MARTES:', '«Se cayó tres veces. Sonrió tres veces».'], ['MIÉRCOLES:', '«Ya me da miedo».']]);
};

/* ================================================================ 7. the week: the dentist, Croqueta's bite, the wet floor */
function drill(g, x, y, rot = -.5) { g.save(); g.translate(x, y); g.rotate(rot); shape(g, q => rrPath(q, -8, -90, 16, 90, 6), '#d9dee6', 3); shape(g, q => q.rect(-3, -110, 6, 22), '#8a8f99', 2); g.restore(); }
function wetSign(g, x) { shape(g, q => { q.moveTo(x - 60, FEET); q.lineTo(x, FEET - 200); q.lineTo(x + 60, FEET); q.closePath(); }, '#f2c230', 5); text(g, 'PISO', x, FEET - 90, 30, '#141014', 'Bangers', 'center'); text(g, 'MOJADO', x, FEET - 58, 26, '#141014', 'Bangers', 'center'); }
SC.s07 = (X, t) => {
  const c2 = Lt('s07_02') - .1, c3 = Lt('s07_03') - .1, c4 = Lt('s07_04') - .1, c5 = Lt('s07_05') - .1;
  if (t < c3) {   // 1+2: «what you can do without pain»; the dentist without anaesthesia
    const cam = shots(t, [], [{ t: 0, cx: 960, cy: 540, z: 1.0, z2: 1.05, lock: 1 }, { t: c2, cx: 1240, cy: 560, z: 1.7, z2: 1.8, lock: 1 }]);
    const st = stage(cam); st.wld(g => drawSet(g, 'clinica'));
    const work = t > Lm('s07_02', .3);
    const hp = { x: 1400, y: 790, s: S0, sit: 1, noShadow: 1, t, look: [-12, -8], mouth: .2, hL: [-70, -170], hR: [70, -170], lean: .38 };
    if (work) { hp.open = .8; hp.look = [-10, -14]; hp.brow = -.2; }
    if (t < c2) { hp.open = 0; hp.mouth = .5; }
    st.wld(g => drawHero(g, hp, { bump: .3 }));
    const dp = standing(1080, { t, look: [14, 2], mouth: -.2, brow: .5, hR: [210, -380], holdR: (g, x, y) => drill(g, x, y), sweat: work && t > Lm('s07_02', .65) ? 1 : 0 });
    if (work) { dp.hR = [260 + Math.sin(t * 30) * 4, -420]; dp.lean = .08; }
    st.wld(g => { drawChar(g, 'ex5', dp); const h = headInfo('ex5', dp); shape(g, q => rrPath(q, h.x - h.r * .55, h.y + h.r * .15, h.r * 1.1, h.r * .55, 10), '#e8f4ff', 3); });   // the dentist's mask
    compose2(X, st, { amt: 0 });
    if (work) hits(X, cam, t, [{ t: Lm('s07_02', .35), at: mouthPt('tu', hp), cname: 'tu', p: hp, hero: 1, dur: .3 }]);
    sticker(X, t < c2 ? 'UNA SEMANA SIN DOLOR' : 'ANESTESIA: NO', R(t, t < c2 ? .3 : c2 + .2, (t < c2 ? .3 : c2 + .2) + .3, back), 70, 70, 66);
    if (work && t > Lm('s07_02', .65)) { const [x, y] = worldToScreen(cam, 1020, 380); comicWord(X, '¡GLUP!', x + 40, y, (t - Lm('s07_02', .65)) % 1.2, 70, '#ffffff', 1.2); }
    return;
  }
  if (t < c4) {   // 3: Croqueta bites, you pet him
    const bite = c3 + .9;
    const cam = shots(t, [], [{ t: 0, cx: 760, cy: 640, z: 1.9, z2: 2.0, lock: 1 }, { t: Lm('s07_03', .6), cx: 960, cy: 600, z: 1.3, z2: 1.35, lock: 1 }]);
    const st = stage(cam); st.wld(g => { drawSet(g, 'bedroom'); bedBack(g); nightstand(g); });
    const leave = Lm('s07_03', .6), cx = t < leave ? 640 : mix(640, 1500, R(t, leave, leave + 2.6, lin));
    st.wld(g => drawAnimal(g, 'croqueta', cx, 716, .9, { t, head: t > bite && t < leave ? 'wide' : 'bored', flip: t > leave ? 1 : -1, open: t > bite - .2 && t < bite + .6 ? .8 : 0, tilt: Math.sin(t * 1.2) * .05 }));
    const hp = { x: 860, y: 945, s: S0, t, look: [-14, 6], mouth: .5, hL: [-200, -240] };
    if (t > bite + .4 && t < leave) { hp.hL = [-200 + Math.sin(t * 6) * 20, -280]; hp.mouth = .8; }
    st.wld(g => drawHero(g, hp, { bump: .5, cheek: 1 })); st.wld(g => bedFront(g, .6));
    compose2(X, st, { amt: 0 });
    hits(X, cam, t, [{ t: bite, at: [700, 690], cname: 'tu', p: hp, hero: 1, dur: .45 }]);
    if (t > bite - .1 && t < bite + .6) comicWord(X, '¡ÑAM!', ...worldToScreen(cam, 660, 560), t - bite + .1, 80);
    if (t > leave + .4) { const [x, y] = worldToScreen(cam, cx, 560); X.save(); X.globalAlpha = R(t, leave + .4, leave + .7); text(X, '¿…?', x, y, 90, '#ffffff', 'Bangers', 'center', OUT, 10); X.restore(); }
    return;
  }
  if (t < c5) {   // 4: the wet floor, a bow, applause
    const slip = c4 + 1.0, bow = Lm('s07_04', .5);
    const cam = shots(t, [], [{ t: 0, cx: 960, cy: 540, z: 1.1, z2: 1.15, lock: 1 }]);
    const st = stage(cam); st.wld(g => { drawSet(g, 'hallway'); wetSign(g, 1250); });
    [['ex1', 300], ['ex4', 460], ['ex2', 1500], ['ex6', 1660]].forEach(([n, x], i) => { const p = standing(x, { t, flip: x > 960 ? -1 : 1, look: [x > 960 ? -14 : 14, 4], mouth: .2 });
      if (t > bow + .3) { const G = charGeom(CAST[n], p); [p.hL, p.hR] = clapHands(t, bow + .5 + i * .07 + Math.floor((t - bow) / .35) * .35, G); p.mouth = .8; p.blink = 1; }
      st.wld(g => drawChar(g, n, p)); });
    const x = mix(700, 1060, R(t, c4 + .2, slip, lin)), hp = standing(x, { t, look: [10, 0], mouth: .3, walk: t < slip ? 1 : 0, phase: walkPh(x) });
    if (t > slip && t < bow - .4) { const f = R(t, slip, slip + .25, outC); hp.lean = -1.1 * f; hp.y = FEET + 30 * f; hp.hL = [-180, -500]; hp.hR = [180, -500]; hp.wide = .6; hp.mouth = .2; }
    if (t > bow) { hp.lean = .55 * bump(t, bow, bow + 1.2); hp.hR = [140, -300]; hp.hL = [-60, -340]; hp.mouth = .7; hp.look = [0, 14]; }
    st.wld(g => drawHero(g, hp, { bump: .6, cheek: 1 }));
    compose2(X, st, { amt: 0 });
    hits(X, cam, t, [{ t: slip + .2, at: [x - 60, 860], cname: 'tu', p: hp, hero: 1 }]);
    if (t > slip + .2 && t < slip + .9) comicWord(X, '¡ZAS!', ...worldToScreen(cam, x - 80, 760), t - slip - .2, 84);
    if (t > bow + .3) sticker(X, '¡BRAVO! ¡BRAVO!', R(t, bow + .3, bow + .6, back), 70, 70, 66);
    return;
  }
  // 5: Nacho stops asking
  const cam = shots(t, [], [{ t: 0, cx: 960, cy: 520, z: 1.5, z2: 1.6, lock: 1 }]);
  const st = stage(cam); st.wld(g => drawSet(g, 'hallway'));
  const np = standing(1150, { t, flip: -1, look: [-14, 4], mouth: .1, brow: .3, lid: .3 }); const G = charGeom(CAST.nacho, np); [np.hL, np.hR] = POSE.shrug(R(t, c5 + .8, c5 + 1.3), G);
  st.wld(g => drawChar(g, 'nacho', np));
  const hp = standing(800, { t, look: [14, 2], mouth: .8, brow: -.4 }); const G2 = charGeom(CAST.tu, hp); hp.hR = [150, G2.top + 20];
  st.wld(g => drawHero(g, hp, { bump: .8, cheek: 1, chin: 1 }));
  compose2(X, st, { amt: 0 });
  const [x, y] = worldToScreen(cam, 1150, 330); bubble(X, '¿TE DOL…? NAH.', x, y, R(t, c5 + .4, c5 + .7, back), 52);
};

/* ================================================================ 8. Pepe pecks your hand: «exacto» */
SC.s08 = (X, t) => {
  const peck = Lm('s08_03', .55), look = Lt('s08_05') - .05;
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 560, z: 1.1, z2: 1.15, lock: 1 },
    { t: Lt('s08_02') - .05, cx: 900, cy: 520, z: 1.9, z2: 2.0, lock: 1 },
    { t: Lt('s08_03') - .05, cx: 1060, cy: 700, z: 2.4, z2: 2.5, lock: 1 },
    { t: look, cx: 1080, cy: 700, z: 3.4, z2: 3.6, lock: 1 },
    { t: Lt('s08_06') - .05, cx: 920, cy: 520, z: 2.2, z2: 2.3, lock: 1 },
    { t: Lt('s08_07') - .05, cx: 1080, cy: 710, z: 3.6, z2: 3.8, lock: 1 },
  ]);
  const st = stage(cam); st.wld(g => { drawSet(g, 'park'); bench(g, 0); bench(g, 1); });
  const hp = benchSit(900, { t, look: [14, 6], mouth: .2, brow: .3 });
  if (t > Lt('s08_03') - .1 && t < look + 1) { hp.hR = [200, -140]; hp.armsFront = 0; }
  if (t > peck) { hp.look = [16, 10]; hp.brow = .1; }
  if (t > Lt('s08_06') - .1) { hp.hR = [80, -125]; hp.armsFront = 1; hp.brow = .8; hp.look = [16, 6]; }
  say(hp, t, ['s08_02', 's08_06']);
  st.wld(g => drawHero(g, hp, { bump: .7, cheek: 1 }));
  const pk = t > peck - .15 && t < peck + .25 ? bump(t, peck - .15, peck + .25) : 0;
  st.wld(g => pigeonTalk(g, 1080, 792, .62, { flip: -1, front: t > look, peck: pk, open: speaking(t, 's08_07') ? .5 : 0, tilt: Math.sin(t * 1.1) * .04 }));
  compose2(X, st, { amt: 0 });
  hits(X, cam, t, [{ t: peck, at: [1050, 760], cname: 'tu', p: hp, hero: 1, dur: .45 }]);
  if (t > peck && t < peck + .6) comicWord(X, '¡TOC!', ...worldToScreen(cam, 1040, 700), t - peck, 70);
  if (t > look + .3 && t < Lt('s08_06') - .1) { const [x, y] = worldToScreen(cam, 1080, 600); bubble(X, '«EXACTO»', x, y - 30, R(t, look + .3, look + .6, back), 60); }
  if (t > Lt('s08_07')) cooBubble(X, cam, 1080, 660, t, Lt('s08_07'), Ld('s08_07') + .4);
};

/* ================================================================ 9. problem 1: a twisted ankle since Monday */
/* the doctor's stethoscope, in the character's own coordinates (p.onBody): tubing round the neck, earpieces on one side, chest piece on the other */
function stethoscope(g, G) {
  const y = G.top, tubeC = '#323846';
  const branch = pts => { g.save(); g.lineCap = 'round'; g.lineJoin = 'round'; g.beginPath(); g.moveTo(...pts[0]); g.bezierCurveTo(...pts[1], ...pts[2], ...pts[3]);
    g.strokeStyle = INK; g.lineWidth = 13; g.stroke(); g.strokeStyle = tubeC; g.lineWidth = 8; g.stroke(); g.restore(); };
  branch([[-44, y + 4], [-52, y + 40], [-40, y + 78], [-26, y + 100]]);
  branch([[44, y + 4], [52, y + 50], [40, y + 110], [32, y + 140]]);
  for (const dx of [-8, 8]) { g.save(); g.lineCap = 'round'; g.strokeStyle = '#c9ced6'; g.lineWidth = 5; g.beginPath(); g.moveTo(-26, y + 100); g.lineTo(-26 + dx, y + 116); g.stroke(); g.restore(); circ(g, -26 + dx, y + 118, 5, '#323846', 2); }
  circ(g, 32, y + 156, 17, '#d7dbe2', 3); circ(g, 32, y + 156, 9, '#aab1bc', 0);
}
function xray(g, x, y, a) { if (a <= 0) return; g.save(); g.globalAlpha = clamp(a); shape(g, q => rrPath(q, x - 120, y - 100, 240, 210, 8), '#1a2233', 0);
  g.strokeStyle = 'rgba(220,235,255,.9)'; g.lineWidth = 16; g.lineCap = 'round'; g.beginPath(); g.moveTo(x - 20, y - 90); g.lineTo(x - 10, y + 30); g.stroke();
  g.beginPath(); g.moveTo(x - 30, y + 50); g.quadraticCurveTo(x + 40, y + 40, x + 90, y + 70); g.stroke(); g.lineWidth = 10; for (let i = 0; i < 4; i++) { g.beginPath(); g.moveTo(x + 50 + i * 12, y + 60); g.lineTo(x + 70 + i * 12, y + 90); g.stroke(); }
  g.strokeStyle = PAIN_RED; g.lineWidth = 6; g.beginPath(); g.arc(x - 18, y + 40, 34, 0, 7); g.stroke(); g.restore(); }
SC.s09 = (X, t) => {
  const doc = Lt('s09_05') - .05, rule = Lt('s09_07') - .1;
  if (t < doc) {
    const cam = shots(t, [], [{ t: 0, cx: 960, cy: 540, z: 1.0, z2: 1.04, lock: 1 }, { t: Lt('s09_02') - .05, cx: 900, cy: 700, z: 1.7, z2: 1.75, lock: 1 }, { t: Lt('s09_03') - .05, cx: 1200, cy: 480, z: 2.2, z2: 2.3, lock: 1 }, { t: Lt('s09_04') - .05, cx: 820, cy: 480, z: 2.2, z2: 2.3, lock: 1 }]);
    const st = stage(cam); st.wld(g => drawSet(g, 'kitchen'));
    const mp = standing(1250, { t, flip: -1, look: [-14, 10], mouth: -.2, brow: .7 }); if (t > Lt('s09_02')) { mp.look = [-16, 18]; mp.wide = .4; }
    say(mp, t, ['s09_03']); st.wld(g => drawChar(g, 'mama', mp));
    const x = mix(500, 860, R(t, Lt('s09_02'), Lt('s09_03') - .2, lin)), lim = Math.abs(Math.sin(walkPh(x))) ;
    const hp = standing(x, { t, look: [10, 0], mouth: .4, walk: t > Lt('s09_02') && t < Lt('s09_03') - .2 ? .8 : 0, phase: walkPh(x), hy: -14 * lim, lean: .05 * Math.sin(walkPh(x) * 2) });
    if (t > Lt('s09_03')) { hp.look = [16, 4]; hp.mouth = .2; }
    if (t > Lt('s09_04')) { hp.look = [6, 22]; hp.wide = .5; hp.brow = .5; }
    say(hp, t, ['s09_04']);
    st.wld(g => drawHero(g, hp, { bump: .8, cheek: 1, ankle: 1 }));
    compose2(X, st, { amt: 0 });
    sticker(X, 'PROBLEMA #1', vis(t, .2, Lt('s09_02') - .2), 70, 70, 70); sticker(X, 'MIÉRCOLES', vis(t, Lt('s09_02') + .1, Lt('s09_03') - .2), 70, 70, 64);
    return;
  }
  const cam = shots(t, [], [{ t: 0, cx: 900, cy: 520, z: 1.3, z2: 1.35, lock: 1 }, { t: Lm('s09_05', .45), cx: 640, cy: 380, z: 2.4, z2: 2.5, lock: 1 }, { t: Lt('s09_06') - .05, cx: 1000, cy: 560, z: 1.3, z2: 1.35, lock: 1 }]);
  const st = stage(cam); st.wld(g => { drawSet(g, 'clinica'); xray(g, 630, 360, R(t, Lm('s09_05', .4), Lm('s09_05', .4) + .4)); });
  const dp = standing(900, { t, look: [-14, -8], mouth: -.2, brow: .5, lid: .2, onBody: stethoscope });
  { const G = charGeom(CAST.ex4, dp); dp.hR = [24, G.top - 6]; }   // thinking: near hand under the chin, elbow down
  st.wld(g => drawChar(g, 'ex4', dp));
  const hp = { x: 1400, y: 790, s: S0, sit: 1, noShadow: 1, t, look: [-14, -2], mouth: .4, hL: [-70, -170], hR: [70, -170], lean: .38, footSwing: Math.sin(t * 2.6) * 14 };
  st.wld(g => drawHero(g, hp, { bump: .8, cheek: 1, ankle: 1 }));
  compose2(X, st, { amt: 0 });
  if (t > Lt('s09_05') + .2) sticker(X, 'TOBILLO TORCIDO · DESDE EL LUNES', R(t, Lm('s09_05', .5), Lm('s09_05', .5) + .3, back) * (1 - R(t, rule - .3, rule)), 70, H - 190, 58, '#ffb3b3');
  if (t > Lt('s09_06')) { ['LUN', 'MAR', 'MIÉ'].forEach((d, i) => { const a = R(t, Lm('s09_06', .1 + i * .2), Lm('s09_06', .1 + i * .2) + .25, back) * (1 - R(t, rule - .3, rule)); sticker(X, d + ': CORRISTE', a, W - 470, 120 + i * 110, 52, '#ffffff'); }); }
  ruleCard(X, 2, 'EL DOLOR ES UNA ALARMA.', 'Y LA TUYA ESTÁ APAGADA', R(t, rule, rule + .3, outC));
};

/* ================================================================ 10. problem 2: you don't know how hard a slap is */
SC.s10 = (X, t) => {
  const slap = Lm('s10_02', .7), hi5 = Lm('s10_04', .25), far = Lt('s10_06') - .05;
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 540, z: 1.05, z2: 1.1, lock: 1 },
    { t: Lt('s10_02') - .05, cx: 900, cy: 520, z: 1.6, z2: 1.7, lock: 1 },
    { t: Lt('s10_04') - .05, cx: 1040, cy: 520, z: 1.7, z2: 1.8, lock: 1 },
    { t: Lt('s10_05') - .05, cx: 900, cy: 500, z: 2.0, z2: 2.1, lock: 1 },
    { t: far, cx: 960, cy: 540, z: 1.0, z2: 1.04, lock: 1 },
  ]);
  const st = stage(cam); st.wld(g => drawSet(g, 'hallway'));
  const np = standing(t < Lt('s10_04') ? 1040 : 1550, { t, flip: -1, look: [-14, 4], mouth: .4 });
  if (t > slap && t < slap + 2.5) { np.lean = -.25 * (1 - R(t, slap + .3, slap + 1.2)); np.wide = .9; np.brow = 1; np.open = .7; np.hL = [-60, -330]; np.hR = [150, -470]; }
  say(np, t, ['s10_03']);
  const rp = standing(t < Lt('s10_04') ? 1550 : 1120, { t, flip: -1, look: [-14, 4], mouth: .4, brow: -.2 });
  if (t > hi5 - .4 && t < hi5 + .2) rp.hR = [180, -560];
  if (t > hi5 + .2) { rp.hR = [70, -470]; rp.hL = [-40, -470]; rp.wide = .6; rp.brow = .8; rp.mouth = -.3; rp.open = .3 + .3 * Math.abs(Math.sin(t * 5)); }   // blowing on her fingers
  if (t > far) { np.x = 1650; rp.x = 1780; np.walk = 0; const G = charGeom(CAST.nacho, np); np.hR = POSE.wave(t, G)[1]; const G2 = charGeom(CAST.valeria, rp); rp.hR = POSE.wave(t + .3, G2)[1]; rp.wide = 0; rp.open = 0; rp.mouth = .3; np.wide = 0; np.open = 0; np.mouth = .2; }
  st.wld(g => { drawChar(g, 'nacho', np); drawChar(g, 'valeria', rp); });
  if (t > far) st.wld(g => [['ex1', 160], ['ex4', 280]].forEach(([n, x]) => { const p = standing(x, { t, look: [14, 2], mouth: .2 }); const G = charGeom(CAST[n], p); p.hR = POSE.wave(t + x, G)[1]; drawChar(g, n, p); }));
  const hp = standing(t < Lt('s10_04') ? 860 : 940, { t, look: [14, 2], mouth: .7, brow: -.3 });
  if (t > slap - .4 && t < slap + .2) { hp.hR = [200, -420 + 120 * R(t, slap - .3, slap, inC)]; hp.armsFront = 1; }
  if (t > hi5 - .4 && t < hi5 + .2) hp.hR = [200, -560];
  if (t > Lt('s10_05')) { hp.look = [6, 10]; hp.mouth = -.1; hp.brow = .5; }
  if (t > far) { hp.x = 760; hp.look = [16, -2]; hp.mouth = -.3; const G = charGeom(CAST.tu, hp); hp.hR = POSE.wave(t, G)[1]; }
  st.wld(g => drawHero(g, hp, { bump: .9, cheek: 1, ankle: 1 }));
  compose2(X, st, { amt: 0 });
  hits(X, cam, t, [{ t: slap, at: [1010, 640], cname: 'nacho', p: np, hero: 0, val: 9, word: '¡AAAY!' }, { t: hi5, at: [1180, 420], cname: 'valeria', p: rp, hero: 0, val: 7, word: '¡AU!' }]);
  if (t > slap - .05 && t < slap + .6) comicWord(X, '¡PLAF!', ...worldToScreen(cam, 980, 520), t - slap + .05, 84);
  if (t > hi5 - .05 && t < hi5 + .6) comicWord(X, '¡CHOCA!', ...worldToScreen(cam, 1080, 330), t - hi5 + .05, 74);
  sticker(X, 'PROBLEMA #2', vis(t, .2, Lt('s10_02') - .2), 70, 70, 70);
  if (t > far + .2) sticker(X, 'JUEVES: SALUDOS DE LEJOS', R(t, far + .2, far + .5, back), 70, 70, 62);
};

/* ================================================================ 11. problem 3: nothing hurts inside either */
function examPaper(g, x, y, s = 1) { g.save(); g.translate(x, y); g.scale(s, s); g.rotate(-.06); shape(g, q => q.rect(-120, -160, 240, 320), '#ffffff', 5);
  for (let i = 0; i < 7; i++) line(g, [[-90, -100 + i * 34], [90, -100 + i * 34]], 'rgba(80,120,180,.4)', 3);
  g.strokeStyle = '#c0262d'; g.lineWidth = 7; g.beginPath(); g.arc(60, -110, 46, 0, 7); g.stroke(); text(g, '5', 60, -88, 64, '#c0262d', 'Bangers', 'center'); g.restore(); }
function heartPt(cname, p) { const h = headInfo(cname, p); return [h.x - 20 * h.S * h.f, h.y + h.r * 2.3]; }
SC.s11 = (X, t) => {
  const caf = Lt('s11_04') - .05;
  if (t < caf) {
    const cam = shots(t, [], [{ t: 0, cx: 900, cy: 520, z: 1.3, z2: 1.35, lock: 1 }, { t: Lt('s11_03') - .05, cx: 900, cy: 560, z: 2.0, z2: 2.1, lock: 1 }]);
    const st = stage(cam); st.wld(g => drawSet(g, 'classroom'));
    const hp = seated(860, { t, look: [6, 16], mouth: .1, hL: [-70, -170], hR: [70, -170] });
    if (t > Lt('s11_03')) { hp.hR = [120, -330]; hp.holdR = (g, x, y) => examPaper(g, x + 40, y - 60, .6); hp.look = [10, -4]; hp.mouth = .4; }
    st.wld(g => drawHero(g, hp, { bump: .9, cheek: 1 })); st.wld(g => desk(g, 860, FEET, .8));
    compose2(X, st, { amt: 0 });
    if (t > Lt('s11_03')) hits(X, cam, t, [{ t: Lm('s11_03', .45), at: heartPt('tu', hp), cname: 'tu', p: hp, hero: 1, dur: .4 }]);
    sticker(X, 'PROBLEMA #3', vis(t, .2, Lt('s11_03') - .2), 70, 70, 70);
    return;
  }
  const leave = Lt('s11_07') - .05;
  const cam = shots(t, [], [{ t: 0, cx: 960, cy: 540, z: 1.2, z2: 1.25, lock: 1 }, { t: Lt('s11_05') - .05, cx: 820, cy: 500, z: 2.0, z2: 2.1, lock: 1 }, { t: Lt('s11_06') - .05, cx: 1120, cy: 500, z: 2.2, z2: 2.3, lock: 1 }, { t: leave, cx: 960, cy: 540, z: 1.2, z2: 1.25, lock: 1 }]);
  const st = stage(cam); st.wld(g => drawSet(g, 'cafeteria'));
  const nx = t < leave ? 1120 : mix(1120, 2100, R(t, leave + .3, leave + 3, lin));
  const np = standing(nx, { t, flip: -1, look: [-14, 14], mouth: -.4, brow: .9, slump: .8, lid: .3, walk: t > leave + .3 ? .7 : 0, phase: walkPh(nx) });
  if (t > leave) { np.flip = 1; np.look = [14, 10]; }
  say(np, t, ['s11_06']);
  st.wld(g => drawChar(g, 'nacho', np));
  const hp = standing(820, { t, look: [16, 4], mouth: .2 });
  if (t > Lt('s11_05') - .1) { const G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = POSE.shrug(.7, G); hp.mouth = .3; }
  if (t > Lt('s11_06')) { hp.hL = null; hp.hR = null; hp.mouth = 0; hp.brow = .2; }
  say(hp, t, ['s11_05']);
  st.wld(g => drawHero(g, hp, { bump: .9, cheek: 1, ankle: 1 }));
  compose2(X, st, { amt: 0 });
  hits(X, cam, t, [{ t: Lt('s11_07') + .3, at: heartPt('tu', hp), cname: 'tu', p: hp, hero: 1, dur: .4 }]);
  if (t > Lt('s11_07') + .3) { const [x, y] = worldToScreen(cam, ...heartPt('tu', hp)); X.save(); X.globalAlpha = R(t, Lt('s11_07') + .3, Lt('s11_07') + .6); heartPopX(X, x, y + 40, .1, 1.4); X.restore(); }
  if (t > Lm('s11_07', .7)) sticker(X, 'DEBERÍA', R(t, Lm('s11_07', .7), Lm('s11_07', .7) + .25, back), 70, 70, 80, '#ffb3b3');
};
