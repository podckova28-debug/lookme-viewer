/* Ep02 scenes 6–11: rock-paper-scissors, the surprise question, small accidents, the lottery, dinner twice, no more surprises. */
function seated(name, x, extra = {}) { return Object.assign({ x, y: FEET, s: S0, sit: 1, hL: [-62, -296], hR: [62, -296], armsFront: 1 }, extra); }
/* rock / paper / scissors badge */
function rps(g, x, y, k, s = 1, col = '#ffffff', label) { g.save(); g.translate(x, y); g.scale(s, s); circ(g, 0, 0, 58, col, 6);
  if (k === 0) { shape(g, q => { q.moveTo(-30, 26); q.lineTo(-34, -10); q.quadraticCurveTo(-30, -30, -10, -30); q.lineTo(22, -30); q.quadraticCurveTo(36, -28, 34, -8); q.lineTo(30, 26); q.closePath(); }, '#a8794e', 5);
    for (const dx of [-16, 0, 16]) line(g, [[dx, -30], [dx, -14]], OUT, 4); }
  else if (k === 1) { shape(g, q => rrPath(q, -26, -34, 52, 66, 8), '#f4f1ea', 5); for (const dy of [-16, 0, 16]) line(g, [[-14, dy], [14, dy]], '#9aa3ad', 3); }
  else { for (const a of [-.35, .35]) { g.save(); g.rotate(a); shape(g, q => rrPath(q, -6, -40, 12, 42, 6), '#9aa3ad', 4); g.restore(); }
    for (const dx of [-12, 12]) circ(g, dx, 14, 13, '#e02424', 5); }
  if (label) text(g, RPS_NAME[k], 0, 104, 40, '#ffffff', 'Bangers', 'center', OUT, 8);
  g.restore(); }
const RPS_NAME = ['PIEDRA', 'PAPEL', 'TIJERA'];
function taco(g, x, y, s = 1) { g.save(); g.translate(x, y); g.scale(s, s);
  shape(g, q => { q.moveTo(-50, 10); q.quadraticCurveTo(0, -70, 50, 10); q.closePath(); }, '#7ec850', 5);
  for (const [dx, c] of [[-22, '#e0485c'], [0, '#f4f1ea'], [22, '#e0485c']]) circ(g, dx, -18, 10, c, 3);
  shape(g, q => { q.moveTo(-56, 14); q.quadraticCurveTo(0, -60, 56, 14); q.quadraticCurveTo(0, -20, -56, 14); }, '#f0c45a', 5); g.restore(); }

/* ================================================================ 6. rock, paper, scissors for tacos */
SC.s06 = (X, t) => {
  const rounds = [[Lt('s06_02') - .1, 2, 0], [Lt('s06_03') - .1, 1, 2]];   // [reveal time, Nacho, you]
  for (let i = 0; i < 12; i++) rounds.push([Lt('s06_04') + i * .22, i % 3, (i % 3 + 2) % 3]);
  rounds.push([Lm('s06_05', .9), 0, 1]);
  let cur = null; for (const r of rounds) if (t >= r[0] - .9) cur = r;
  const wins = rounds.filter(r => t >= r[0]).length, shown = t > Lt('s06_04') ? Math.min(51, 2 + Math.floor(R(t, Lt('s06_04'), Le('s06_04') + .4, lin) * 49)) + (t > Lm('s06_05', .9) ? 0 : 0) : wins;
  const cam = shots(t, [], [
    { t: 0, cx: 1250, cy: 560, z: 1.15, z2: 1.2, w: 2600, lock: 1 },
    { t: Lt('s06_02') - .6, cx: 1250, cy: 520, z: 1.55, z2: 1.6, w: 2600, lock: 1 },
    { t: Lt('s06_04') - .05, cx: 1250, cy: 560, z: 1.25, z2: 1.3, w: 2600, lock: 1 },
    { t: Lt('s06_05') - .05, cx: 1420, cy: 470, z: 2.1, z2: 2.2, w: 2600, lock: 1 },
    { t: Lt('s06_06') - .05, cx: 1250, cy: 560, z: 1.2, w: 2600, lock: 1 },
    { t: Lt('s06_07') - .05, cx: 1420, cy: 470, z: 2.3, z2: 2.4, w: 2600, lock: 1 },
  ]);
  const st = stageF(cam); st.wld(g => drawSet(g, 'hallway'));
  st.col(g => drawPigeon(g, 2050, 610, .42, { flip: -1, tilt: Math.sin(t * .9) * .12 }));   // by the window: no ghost
  st.wld(g => { drawChar(g, 'ex2', { x: 640, y: FEET, s: S0, t, look: [10, 0], mouth: .3 }); drawChar(g, 'ex5', { x: 1900, y: FEET, s: S0, t, flip: -1, look: [-10, 0], mouth: .3 }); });
  const shake = r => r ? Math.abs(Math.sin(clamp((t - (r[0] - .9)) / .8) * Math.PI * 3)) * (t < r[0] ? 1 : 0) : 0;
  const np = { x: 1420, y: FEET, s: S0, t, flip: -1, look: [-14, 4], mouth: .3, hR: [170, -400 - 60 * shake(cur)] };
  const hp = { x: 1080, y: FEET, s: S0, t, look: [14, 4], mouth: .3, hR: [170, -400 - 60 * shake(cur)] };
  if (t > Lt('s06_02')) { hp.mouth = .6; hp.brow = -.3; np.mouth = -.2; np.brow = .6; }
  if (speaking(t, 's06_05') || (t > Lt('s06_05') && t < Lt('s06_06'))) { np.open = talk(t, 's06_05'); np.brow = .9; np.wide = .4; const G = charGeom(CAST.nacho, np); [np.hL, np.hR] = POSE.clap(1, G); }
  if (t > Lt('s06_07') - .05) { np.look = [10, -14]; np.mouth = .1; np.brow = .2; np.sweat = 1; np.hR = [120, -470]; np.rot = .08; }
  st.wld(g => drawChar(g, 'nacho', np)); st.col(g => drawChar(g, 'tu', hp));
  const ga = cur && t < Lt('s06_06') ? vis(t, cur[0] - .9, cur[0] - .05, .15, .1) : 0;
  if (ga > 0) st.fut(g => rps(g, 1520, 420, cur[1], 1.3));
  st.col(g => futEyes(g, 'tu', hp, ga));
  composeF(X, st, { ghost: ga, t, rim: .5 });
  if (cur && t >= cur[0] && t < Lt('s06_06')) { const [nx, ny] = worldToScreen(cam, 1520, 420), [hx, hy] = worldToScreen(cam, 980, 420), k = back(clamp((t - cur[0]) / .15)) * Math.min(1.6, cam.z);
    rps(X, nx, ny, cur[1], k, '#ffffff', 1); rps(X, hx, hy, cur[2], k, '#fde047', 1); }
  if (t > Lt('s06_02') - .1 && t < Lt('s06_06')) bigCounter(X, 'TÚ ' + shown + ' –', 'NACHO 0', 1);
  if (t > Lt('s06_06') && t < Lt('s06_07')) { const a = R(t, Lt('s06_06'), Lt('s06_06') + .3, back); X.save(); X.globalAlpha = .6 * a; X.fillStyle = '#0d0b12'; X.fillRect(0, 0, W, H); X.restore(); sticker(X, 'NACHO TE DEBE:', a, 700, 160, 70);
    const n = Math.min(37, Math.floor(R(t, Lt('s06_06') + .2, Le('s06_06'), lin) * 37)); text(X, n + ' TACOS', 960, 380, 110, '#fde047', 'Bangers', 'center', OUT, 14);
    for (let i = 0; i < Math.min(n, 14); i++) taco(X, 380 + i * 90, 520 + Math.sin(i * 1.7) * 18, .9); }
  if (t > Lt('s06_07')) sticker(X, 'DEUDA: 37 TACOS', R(t, Lt('s06_07'), Lt('s06_07') + .3, back), 70, 70, 60);
  futHUD(X, ga, 5 * (1 - clamp((t - (cur ? cur[0] - .9 : 0)) / .85)));
};

/* ================================================================ 7. Ramírez's surprise question, answered first */
function notebook(g, x, y, s, label, rot = 0, flip = 1) { g.save(); g.translate(x, y); g.rotate(rot); g.scale(s * flip, s);
  shape(g, q => rrPath(q, -80, -105, 160, 210, 10), '#c0262d', 6); shape(g, q => rrPath(q, -60, -60, 120, 60, 6), '#f4f1ea', 4);
  text(g, label, 0, -18, 44, OUT, 'Bangers', 'center'); for (let i = 0; i < 6; i++) circ(g, -80, -88 + i * 34, 6, '#d9d9d9', 3); g.restore(); }
SC.s07 = (X, t) => {
  const ask0 = Lt('s07_05'), turn = Lt('s07_04') + .2, nb1 = Lm('s07_06', .55), nb2 = Lt('s07_08');
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 560, z: 1.0, z2: 1.04, lock: 1 },
    { t: Lt('s07_02') - .05, cx: 800, cy: 520, z: 1.8, z2: 1.9, lock: 1 },
    { t: Lt('s07_03') - .05, cx: 960, cy: 560, z: 1.15, lock: 1 },
    { t: Lt('s07_04') - .05, cx: 1500, cy: 470, z: 1.9, z2: 2.0, lock: 1 },
    { t: ask0 - .05, cx: 1180, cy: 520, z: 1.35, z2: 1.4, lock: 1 },
    { t: Lt('s07_06') - .05, cx: 1500, cy: 450, z: 2.3, z2: 2.45, lock: 1 },
    { t: Lt('s07_07') - .05, cx: 1500, cy: 520, z: 1.8, z2: 1.85, lock: 1 },
  ]);
  const st = stageF(cam); st.wld(g => { drawSet(g, 'classroom'); if (HYB) boardText(g, t > ask0 ? '6 × 7 = ?' : 'PREGUNTA SORPRESA', ''); teacherDesk(g, 1690); });
  st.col(g => drawPigeon(g, 260, 380, .38, { flip: 1, tilt: Math.sin(t * .8) * .12 }));
  st.wld(g => { drawChar(g, 'ex2', seated('ex2', 380, { t, look: [6, 4], mouth: .1 })); drawChar(g, 'ex3', seated('ex3', 1180, { t, look: t > Lt('s07_03') ? [-16, 0] : [4, 4], mouth: t > Lt('s07_03') ? -.2 : .1, wide: t > Lt('s07_03') ? .4 : 0 })); });
  // profe: at the board, back to the class, turns when you answer
  const facing = t > turn, pp = { x: 1500, y: FEET, s: S0, t, flip: facing ? -1 : 1, look: facing ? [-14, 4] : [16, -10], mouth: -.2, brow: .6, hR: [190, -560] };
  if (speaking(t, 's07_05')) { pp.open = talk(t, 's07_05'); pp.hR = [190, -560]; }
  if (t > Lt('s07_06') - .05) { pp.look = [-16, 6]; pp.lid = .45; pp.brow = .9; pp.mouth = -.3; }
  if (t > nb1) { pp.hR = [180, -420]; pp.holdR = (g, x, y) => notebook(g, x + 20, y - 40, .55, 'TÚ', -.1, pp.flip); }
  if (t > nb2) { pp.hL = [-180, -420]; pp.holdL = (g, x, y) => notebook(g, x - 20, y - 40, .55, 'TÚ 2', .1, pp.flip); }
  st.wld(g => drawChar(g, 'profe', pp));
  const hp = seated('tu', 800, { t, mouth: .1, look: [10, 2] });
  if (t > Lt('s07_02')) { hp.lid = .25; hp.mouth = .4; hp.brow = -.2; }
  if (t > Lt('s07_03') - .2 && t < Lt('s07_04') + .5) { hp.hR = [120, -640]; hp.open = talk(t, 's07_03'); }
  if (t > Lt('s07_06')) { hp.mouth = -.25; hp.sweat = 1; hp.lid = 0; hp.brow = .6; }
  st.col(g => drawChar(g, 'tu', hp));
  // the future: the professor already turned, already asking
  const ga = vis(t, Lt('s07_02') - .1, ask0 - .3);
  if (ga > 0) st.fut(g => drawChar(g, 'profe', { x: 1440, y: FEET, s: S0, t, flip: -1, look: [-14, 4], brow: .6, open: .2 + .5 * Math.abs(Math.sin(t * 8)), hR: [180, -520] }));
  st.col(g => futEyes(g, 'tu', hp, ga));
  composeF(X, st, { ghost: ga, t });
  if (ga > .2 && t < Lt('s07_03')) bubble(X, '¿6 × 7?', ...worldToScreen(cam, 1440, 280), ga, 60);
  if (t > Lt('s07_03') - .1 && t < Lt('s07_04') + 1.5) bubble(X, '¡42!', ...worldToScreen(cam, 820, 400), R(t, Lt('s07_03') - .1, Lt('s07_03') + .2, back), 70);
  if (t > ask0 && t < Lt('s07_06')) bubble(X, '¿6 × 7?', ...worldToScreen(cam, 1500, 300), R(t, ask0, ask0 + .25, back), 64);
  futHUD(X, ga, hudN(t, Lt('s07_02') - .1, ask0));
};

/* ================================================================ 8. the hero of small accidents */
SC.s08 = (X, t) => {
  const A = [Lm('s08_02', .55), Lm('s08_03', .55), Lm('s08_04', .6)];   // catch moments: pencil, juice, phone
  const sh = t < Lt('s08_02') - .1 ? 0 : t < Lt('s08_03') - .1 ? 1 : t < Lt('s08_04') - .1 ? 2 : 3;
  const cam = [
    { cx: 960, cy: 560, z: 1.0 }, { cx: 880, cy: 640, z: 1.9 }, { cx: 880, cy: 640, z: 1.9 }, { cx: 1300, cy: 640, z: 1.45 },
  ][sh];
  if (t > Lt('s08_05') - .05) Object.assign(cam, { cx: 1450, cy: 480, z: 2.0 });
  if (t > Lt('s08_06') - .05) Object.assign(cam, { cx: 1000, cy: 540, z: 1.1 });
  const st = stageF(cam); st.wld(g => drawSet(g, 'classroom'));
  st.col(g => drawPigeon(g, 260, 380, .38, { flip: 1, tilt: Math.sin(t * .8) * .12 }));
  const k = sh === 1 ? 0 : sh === 2 ? 1 : sh === 3 ? 2 : -1, tc = k >= 0 ? A[k] : 0, f0 = tc - .55;
  // hero stands at a desk; the object tips off, the hand is already there
  const hp = { x: 760, y: FEET, s: S0, t, look: [14, 6], mouth: .3, brow: -.1 };
  const reach = k >= 0 ? R(t, f0 - .1, tc, outC) : 0;
  st.wld(g => { desk(g, 1000, FLOOR, .9); if (sh === 0 || sh === 3) desk(g, 1500, FLOOR, .9); });
  const fall = (tt) => clamp((tt - f0) / .55);
  let obj = null;
  if (k === 0) obj = (g, u, held) => { const x = held ? null : mix(1080, 1120, u), y = mix(712, 900, u * u); if (!held) { g.save(); g.translate(x, y); g.rotate(u * 7); shape(g, q => rrPath(q, -40, -6, 80, 12, 4), '#f0c45a', 3); g.restore(); } };
  if (k === 1) obj = (g, u, held) => { if (held) return; const x = mix(1060, 1110, u), y = mix(690, 880, u * u); g.save(); g.translate(x, y); g.rotate(u * 1.6); shape(g, q => rrPath(q, -22, -40, 44, 70, 6), 'rgba(255,170,60,.9)', 4); g.restore(); };
  if (k === 2) obj = (g, u, held) => { if (held) return; const x = mix(1420, 1300, u), y = mix(520, 900, u * u); propPhone(g, x, y, .5, 40, u * 5); };
  if (obj && t < tc) st.wld(g => obj(g, fall(t), false));
  if (k >= 0) { const tx = k === 2 ? 1300 : 1110, ty = k === 2 ? 900 : 880; hp.x = k === 2 ? 1080 : 760; hp.hR = [mix(112, (tx - hp.x) / S0, reach), mix(-200, (ty - FEET + 10) / S0, reach)]; hp.lean = .1 * reach; hp.look = [16, 14];
    if (t > tc) hp.holdR = (g, x, y) => { if (k === 0) shape(g, q => rrPath(q, x - 40, y - 6, 80, 12, 4), '#f0c45a', 3); if (k === 1) shape(g, q => rrPath(q, x - 22, y - 60, 44, 70, 6), 'rgba(255,170,60,.9)', 4); if (k === 2) propPhone(g, x, y - 30, .5, 40, 0); }; }
  if (sh === 3) { const pp = { x: 1500, y: FEET, s: S0, t, flip: -1, look: [-14, 10], mouth: -.2, brow: .7, lid: .3, hL: [-120, -400] };
    if (speaking(t, 's08_05')) { pp.open = talk(t, 's08_05'); pp.hL = [-200, -420]; pp.holdL = (g, x, y) => propPhone(g, x, y - 30, .5, 40, 0); }
    if (t > Le('s08_05')) { pp.hL = [-160, -420]; pp.holdL = (g, x, y) => propPhone(g, x, y - 30, .5, 40, 0); }
    st.wld(g => drawChar(g, 'profe', pp)); if (t > Lt('s08_05') - .05) { hp.holdR = null; hp.hR = [140, -260]; hp.mouth = .5; } }
  if (t > Lt('s08_06') - .05) { hp.x = 900; hp.hR = null; hp.lean = 0; hp.look = [0, 0]; hp.mouth = .3; hp.brow = -.2;
    st.wld(g => { for (const [n, x, f] of [['ex2', 380, 1], ['ex4', 620, 1], ['ex6', 1220, -1], ['ex1', 1480, -1]]) drawChar(g, n, { x, y: FEET, s: S0, t, flip: f, look: [f * 16, 0], wide: .5, open: .3 }); }); }
  st.col(g => drawChar(g, 'tu', hp));
  if (sh === 0) st.wld(g => desk(g, 1000, FLOOR, .9));
  const ga = k >= 0 ? vis(t, f0 - 1.2, f0 - .05, .2, .15) : 0;
  if (ga > 0) st.fut(g => obj && obj(g, loopU(t, f0 - 1.2, 1.1) * 1.4, false));
  st.col(g => futEyes(g, 'tu', hp, ga));
  composeF(X, st, { ghost: ga, t });
  if (k === 2 && t > tc && t < Lt('s08_05')) sticker(X, '10 cm', R(t, tc, tc + .25, back), ...worldToScreen(cam, 1330, 820), 62);
  if (k >= 0 && t > tc && t < tc + .7) comicWord(X, '¡ZAS!', ...worldToScreen(cam, k === 2 ? 1300 : 1110, 760), t - tc, 80, '#5ee7ff');
  futHUD(X, ga, hudN(t, f0 - 1.2, tc));
};

/* ================================================================ 9. the lottery, five seconds too late */
function tvSet(g, x, y, draw) { shape(g, q => rrPath(q, x - 210, y - 135, 420, 260, 14), '#26262e', 7); g.save(); g.beginPath(); g.rect(x - 192, y - 118, 384, 222); g.clip();
  g.fillStyle = '#1b2a6b'; g.fillRect(x - 192, y - 118, 384, 222); draw(g); g.restore(); shape(g, q => rrPath(q, x - 30, y + 125, 60, 26, 4), '#26262e', 5); }
function lottoBall(g, x, y, n, r = 44, col = '#ffffff') { circ(g, x, y, r, col, 5); circ(g, x, y, r * .55, '#fde047', 3); text(g, String(n), x, y + r * .26, r * .7, OUT, 'Bangers', 'center'); }
SC.s09 = (X, t) => {
  const N = [7, 12, 21, 33], T0 = Lt('s09_03'), at = i => T0 + i * Ld('s09_03') / 4 + .05;
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 560, z: 1.05, z2: 1.1, lock: 1 },
    { t: Lt('s09_02') - .05, cx: 1180, cy: 480, z: 1.5, z2: 1.55, lock: 1 },
    { t: T0 - .05, cx: 1180, cy: 440, z: 2.1, z2: 2.2, lock: 1 },
    { t: Lt('s09_04') - .05, cx: 900, cy: 520, z: 1.4, lock: 1 },
    { t: Lt('s09_05') - .05, cx: 960, cy: 560, z: 1.05, lock: 1 },
    { t: Lt('s09_06') - .05, cx: 760, cy: 470, z: 2.5, z2: 2.6, lock: 1 },
  ]);
  const st = stageF(cam); st.wld(g => drawSet(g, 'kitchenNight'));
  st.col(g => drawPigeon(g, 1560, 420, .4, { flip: -1, tilt: Math.sin(t * .6) * .12 }));
  const shownTV = i => t >= at(i) + 1.0;   // the real ball comes out a beat after you already saw it
  st.wld(g => tvSet(g, 1180, 470, q => { text(q, 'SORTEO', 1180, 390, 44, '#fde047', 'Bangers', 'center'); for (let i = 0; i < 4; i++) if (shownTV(i)) lottoBall(q, 1030 + i * 100, 470, N[i], 40); }));
  const hp = { x: 760, y: FEET, s: S0, t, look: [16, -4], mouth: .2, sit: 0 };
  if (t > T0) { hp.mouth = .5; hp.wide = .3; }
  if (t > Lt('s09_04')) { const G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = POSE.stretch(R(t, Lt('s09_04'), Lt('s09_04') + .3, back), G); hp.mouth = 1; hp.blink = 1; hp.look = [0, 0]; }
  if (t > Lt('s09_05') - .05) { hp.hL = hp.hR = null; hp.mouth = -.1; hp.blink = 0; hp.wide = .3; hp.look = [14, 4]; }
  if (t > Lt('s09_06') - .1) { hp.mouth = 0; hp.open = .25; hp.brow = 0; hp.wide = 0; hp.look = [0, 0]; }
  st.col(g => drawChar(g, 'tu', hp));
  st.wld(g => kitchenTable(g));
  const ga = vis(t, T0 - .3, at(3) + .9);
  if (ga > 0) st.fut(g => { for (let i = 0; i < 4; i++) if (t >= at(i) && !shownTV(i)) lottoBall(g, 1030 + i * 100, 470, N[i], 40); });
  st.col(g => futEyes(g, 'tu', hp, ga));
  composeF(X, st, { ghost: ga, t });
  if (t > Lt('s09_04') - .05 && t < Lt('s09_05')) sticker(X, '4 DE 4 ✔', R(t, Lt('s09_04'), Lt('s09_04') + .25, back), 70, 70, 74, '#7ee38a');
  if (t > Lt('s09_05') + .3) { const a = R(t, Lt('s09_05') + .3, Lt('s09_05') + .6, back); X.save(); X.globalAlpha = a; X.translate(W - 520, 150); X.rotate(.06);
    shape(X, q => rrPath(q, 0, 0, 430, 220, 16), '#f4f1ea', 6); text(X, 'BOLETOS', 215, 80, 60, OUT, 'Bangers', 'center'); text(X, 'VENTA: AYER', 215, 170, 64, '#e02424', 'Bangers', 'center'); X.restore(); }
  futHUD(X, ga, 5 - ((t - T0 + .3) * 2.2) % 5);
};

/* ================================================================ 10. dinner: you answer before she asks */
SC.s10 = (X, t) => {
  const q0 = Lt('s10_06');   // the real question
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 560, z: 1.05, z2: 1.08, lock: 1 },
    { t: Lt('s10_03') - .1, cx: 900, cy: 520, z: 1.5, lock: 1 },
    { t: Lt('s10_04') - .05, cx: 1190, cy: 470, z: 2.1, lock: 1 },
    { t: Lt('s10_05') - .05, cx: 960, cy: 560, z: 1.15, lock: 1 },
    { t: Lt('s10_07') - .05, cx: 760, cy: 470, z: 2.1, lock: 1 },
    { t: Lt('s10_08') - .05, cx: 1190, cy: 470, z: 2.2, z2: 2.35, lock: 1 },
    { t: Lt('s10_09') - .05, cx: 1300, cy: 560, z: 1.0, w: 2600, lock: 1 },
  ]);
  const hall = t > Lt('s10_09') - .05;
  const st = stageF(cam);
  if (!hall) {
    st.wld(g => drawSet(g, 'kitchenNight'));
    st.col(g => drawPigeon(g, 1560, 420, .4, { flip: -1, tilt: Math.sin(t * .6) * .12 }));
    const mp = { x: 1190, y: FEET, s: S0, t, flip: -1, look: [-8, 14], mouth: .2, hL: [-130, -300], hR: [140, -330] };
    if (speaking(t, 's10_04')) { mp.open = talk(t, 's10_04'); mp.look = [-16, 0]; mp.brow = .7; mp.wide = .3; }
    if (speaking(t, 's10_06')) { mp.open = talk(t, 's10_06'); mp.look = [-16, 0]; mp.mouth = .4; }
    if (t > Lt('s10_08') - .05) { mp.look = [-16, 0]; mp.wide = .7; mp.mouth = -.3; mp.brow = .9; const u = R(t, Lt('s10_08'), Lt('s10_08') + .4, back); mp.hR = [mix(140, 60, u), mix(-330, -560, u)]; mp.holdR = (g, x, y) => { line(g, [[x, y - 70], [x, y + 40]], '#9aa3ad', 10); line(g, [[x - 30, y - 30], [x + 30, y - 30]], '#9aa3ad', 10); }; }
    st.wld(g => drawChar(g, 'mama', mp));
    const hp = seated('tu', 760, { t, look: [14, 0], mouth: .1 });
    if (speaking(t, 's10_03')) { hp.open = talk(t, 's10_03'); hp.mouth = .4; }
    if (speaking(t, 's10_07')) { hp.open = talk(t, 's10_07'); hp.lid = .3; }
    if (t > Lt('s10_08')) { hp.mouth = -.2; hp.sweat = 1; hp.brow = .5; }
    st.col(g => drawChar(g, 'tu', hp));
    st.wld(g => kitchenTable(g));
    const ga = vis(t, Lt('s10_02') + .5, Lt('s10_04') - .1);
    if (ga > 0) st.fut(g => drawChar(g, 'mama', Object.assign({}, mp, { look: [-16, 0], open: .2 + .5 * Math.abs(Math.sin(t * 8)), mouth: .4 })));
    st.col(g => futEyes(g, 'tu', hp, ga));
    composeF(X, st, { ghost: ga, t });
    if (ga > .3) bubble(X, '¿QUÉ QUIERES DE CENAR?', ...worldToScreen(cam, 1190, 300), ga, 46);
    if (t > Lt('s10_03') - .05 && t < Lt('s10_05')) bubble(X, '¡PIZZA!', ...worldToScreen(cam, 760, 380), R(t, Lt('s10_03') - .05, Lt('s10_03') + .2, back), 64);
    if (t > Lt('s10_05') && t < q0) sticker(X, '+5 SEGUNDOS', R(t, Lt('s10_05'), Lt('s10_05') + .25, back), 70, 70, 74, '#5ee7ff');
    if (t > q0 && t < Lt('s10_07')) bubble(X, '¿QUÉ QUIERES DE CENAR?', ...worldToScreen(cam, 1190, 300), R(t, q0, q0 + .25, back), 46);
    if (t > Lt('s10_07') - .05 && t < Lt('s10_08')) bubble(X, '…pizza.', ...worldToScreen(cam, 760, 380), R(t, Lt('s10_07') - .05, Lt('s10_07') + .2, back), 54);
    futHUD(X, ga, hudN(t, Lt('s10_02') + .5, q0));
  } else {
    // the hallway: you answer everyone early, and the questions stop
    st.wld(g => drawSet(g, 'hallway'));
    st.col(g => drawPigeon(g, 2050, 610, .42, { flip: -1, tilt: Math.sin(t * .9) * .12 }));
    const u = R(t, Lt('s10_10'), Le('s10_10'), io);
    st.wld(g => { for (const [n, x, f] of [['ex2', 900, 1], ['ex1', 1650, -1], ['ex5', 1880, -1]]) drawChar(g, n, { x: x - f * 260 * u, y: FEET, s: S0, t, flip: u > .1 ? -f : f, look: [f * 14, 0], mouth: -.2, brow: .4 }); });
    const hp = { x: 1300, y: FEET, s: S0, t, look: [0, 0], mouth: .5 };
    if (t > Lt('s10_10')) { hp.mouth = -.25; hp.brow = .5; }
    st.col(g => drawChar(g, 'tu', hp));
    composeF(X, st, { ghost: 0, t });
    const B = [['¡SÍ!', 1300, 300, 0], ['¡A LAS 5!', 1300, 300, .33], ['¡AZUL!', 1300, 300, .66]];
    for (const [s, x, y, f] of B) { const a0 = Lm('s10_09', f); if (t > a0 && t < a0 + .9) bubble(X, s, ...worldToScreen(cam, x, y), R(t, a0, a0 + .15, back), 60); }
    if (t > Lt('s10_10')) bubble(X, '…', ...worldToScreen(cam, 1300, 300), R(t, Lt('s10_10') + .5, Lt('s10_10') + .8, back), 60);
  }
};

/* ================================================================ 11. no more surprises: movies, jokes, your own party */
/* the party plate says FELIZ CUMPLE NACHO (ep01): cover NACHO with wall and hang three stars instead */
function partyBannerFix(g) { g.save(); const gr = g.createLinearGradient(0, 100, 0, 240); gr.addColorStop(0, 'rgb(249,182,130)'); gr.addColorStop(1, 'rgb(252,185,131)');
  g.fillStyle = gr; g.filter = 'blur(3px)'; g.fillRect(1378, 104, 345, 128); g.filter = 'none';
  g.strokeStyle = '#3a2a2a'; g.lineWidth = 3; g.beginPath(); g.moveTo(1380, 178); g.quadraticCurveTo(1540, 196, 1700, 130); g.stroke();
  for (const [x, y, c] of [[1440, 186, '#fde047'], [1540, 184, '#5ee7ff'], [1640, 160, '#e07a8a']]) { g.save(); g.translate(x, y + 26); g.fillStyle = c; g.strokeStyle = OUT; g.lineWidth = 4; g.beginPath();
    for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + i * Math.PI / 5, r = i % 2 ? 14 : 32; g.lineTo(Math.cos(a) * r, Math.sin(a) * r); } g.closePath(); g.fill(); g.stroke(); g.restore(); }
  g.restore(); }
function sofa(g, x, y) { shape(g, q => rrPath(q, x - 330, y - 230, 660, 170, 40), '#4a5fa8', 7); shape(g, q => rrPath(q, x - 360, y - 110, 720, 120, 30), '#5a70b8', 7);
  for (const dx of [-360, 330]) shape(g, q => rrPath(q, x + dx, y - 170, 40, 170, 18), '#3f528f', 6); }
SC.s11 = (X, t) => {
  const door = Lt('s11_06') + .2, jump = Lt('s11_08') - .15, prac = Lt('s11_07');
  const part = t < Lt('s11_05') - .05 ? (t < Lt('s11_03') - .05 ? 'movie' : 'joke') : 'party';
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 560, z: 1.05, lock: 1 },
    { t: Lt('s11_02') - .05, cx: 1000, cy: 520, z: 1.4, z2: 1.45, lock: 1 },
    { t: Lt('s11_03') - .05, cx: 1000, cy: 520, z: 1.35, z2: 1.4, lock: 1 },
    { t: Lt('s11_04') - .05, cx: 1200, cy: 470, z: 2.2, z2: 2.3, lock: 1 },
    { t: Lt('s11_05') - .05, cx: 960, cy: 560, z: 1.0, lock: 1 },
    { t: door - .2, cx: 700, cy: 520, z: 1.3, lock: 1 },
    { t: prac - .05, cx: 420, cy: 470, z: 2.4, z2: 2.5, lock: 1 },
    { t: jump, cx: 960, cy: 560, z: 1.05, shake: 1, lock: 1 },
    { t: Lt('s11_09') - .05, cx: 420, cy: 470, z: 2.5, z2: 2.6, lock: 1 },
    { t: Lt('s11_11') - .05, cx: 1360, cy: 470, z: 2.1, z2: 2.2, lock: 1 },
  ]);
  const st = stageF(cam); let ga = 0, hp;
  if (part !== 'party') {
    st.wld(g => drawSet(g, 'kitchenNight'));
    st.col(g => drawPigeon(g, 1560, 420, .4, { flip: -1, tilt: Math.sin(t * .6) * .12 }));
    if (part === 'movie') {
      st.wld(g => tvSet(g, 1180, 470, q => { const u = (t - Lt('s11_02')) / Ld('s11_02'); text(q, u < .6 ? '…' : 'FIN', 1180, 500, 90, '#ffffff', 'Bangers', 'center'); }));
      hp = { x: 760, y: FEET, s: S0, t, look: [16, -4], mouth: -.1, lid: .45, brow: -.2 };
      st.col(g => drawChar(g, 'tu', hp));
      ga = vis(t, Lt('s11_02') - .1, Lm('s11_02', .6));
      if (ga > 0) st.fut(g => text(g, 'FIN', 1180, 500, 90, '#ffffff', 'Bangers', 'center'));
    } else {
      const np = { x: 1200, y: FEET, s: S0, t, flip: -1, look: [-14, 0], mouth: .6, open: Math.abs(Math.sin(t * 7)) * .5, hR: [170, -520] };
      if (t > Lt('s11_04')) { np.open = 0; np.mouth = -.3; np.brow = .6; np.hy = -4 * Math.sin(t * 3); np.wide = .3; np.blush = 1; }   // holding his breath
      hp = { x: 760, y: FEET, s: S0, t, look: [14, 0], mouth: 1, blink: t < Lm('s11_03', .7) ? 1 : 0, rot: Math.sin(t * 14) * .05 };
      if (t > Lm('s11_03', .7)) { hp.mouth = -.2; hp.rot = 0; hp.brow = .4; }
      st.wld(g => drawChar(g, 'nacho', np)); st.col(g => drawChar(g, 'tu', hp));
    }
    st.col(g => futEyes(g, 'tu', hp, ga));
    composeF(X, st, { ghost: ga, t });
    if (part === 'joke' && t < Lt('s11_04')) { bubble(X, '¿SABES QUÉ LE DIJO…', ...worldToScreen(cam, 1200, 300), 1, 44); if (t < Lm('s11_03', .7)) comicWord(X, '¡JAJAJA!', ...worldToScreen(cam, 760, 330), (t - Lt('s11_03')) % .7, 70, '#fde047'); }
    if (part === 'joke' && t > Lt('s11_04') + .4) sticker(X, 'SIN CHISTES: DÍA 1', R(t, Lt('s11_04') + .4, Lt('s11_04') + .7, back), 70, 70, 62);
  } else {
    st.wld(g => { drawSet(g, 'party'); partyBannerFix(g); });
    st.col(g => drawPigeon(g, 430, 488, .4, { flip: -1, tilt: Math.sin(t * .8) * .12 }));   // on the window sill
    const G6 = [['nacho', 1360], ['ex2', 1520], ['ex4', 1680], ['ex6', 1830]];
    const up = R(t, jump, jump + .3, back), hidden = t < jump;
    // guests: crouched behind the sofa, then they jump out with confetti
    for (const [n, x] of G6) { const p = { x, y: FEET + (hidden ? 300 : 0) - 60 * bump(t, jump, jump + .4), s: S0, t, look: [-14, 0], mouth: hidden ? -.1 : .9, wide: hidden ? 0 : .6, flip: -1 };
      if (!hidden) { const G = charGeom(CAST[n], p); [p.hL, p.hR] = POSE.stretch(up, G); }
      if (n === 'nacho' && speaking(t, 's11_11')) { p.open = talk(t, 's11_11'); p.mouth = .2; p.lid = .4; p.brow = .8; p.hL = p.hR = null; }
      if (n === 'nacho' && t > Lt('s11_10') && !speaking(t, 's11_11')) { p.mouth = 0; p.lid = .3; p.brow = .6; p.hL = p.hR = null; }
      st.wld(g => drawChar(g, n, p)); }
    st.wld(g => sofa(g, 1590, 890));
    if (t < Lt('s11_06')) st.wld(g => { text(g, 'VIERNES', 960, 260, 90, '#e02424', 'Bangers', 'center'); });
    hp = { x: t < door ? -200 : mix(260, 420, R(t, door, door + .8, io)), y: FEET, s: S0, t, walk: t > door && t < door + .8 ? 1 : 0, phase: walkPh(t * 80), look: [16, 0], mouth: .2 };
    if (t > prac && t < jump) { const k = Math.floor((t - prac) / .55) % 4; Object.assign(hp, [{ wide: .8, open: .8, brow: .9 }, { wide: .2, open: .3, brow: -.6, mouth: .9 }, { wide: 1, open: 1, brow: 1, hy: -10 }, { wide: .5, open: .6, brow: .4, rot: .1 }][k]); }
    if (t > Lt('s11_09') - .1 && t < Lt('s11_11')) { Object.assign(hp, { wide: .15, open: .35, brow: .2, mouth: 0, rot: 0 }); const G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = POSE.shrug(.4, G); }
    if (t > Lt('s11_11')) { hp.sweat = 1; hp.mouth = -.25; hp.wide = 0; hp.open = 0; }
    st.col(g => drawChar(g, 'tu', hp));
    ga = vis(t, door + .1, jump - .2);
    if (ga > 0) st.fut(g => { const uu = loopU(t, door + .1, 1.6); for (const [n, x] of G6) { const p = { x, y: FEET - 60 * bump(uu, .1, .4), s: S0, t, look: [-14, 0], mouth: .9, wide: .6, flip: -1 }; const G = charGeom(CAST[n], p); [p.hL, p.hR] = POSE.stretch(R(uu, .1, .3, back), G); drawChar(g, n, p); } });
    st.col(g => futEyes(g, 'tu', hp, ga));
    composeF(X, st, { ghost: ga, t });
    if (t > jump && t < jump + 1.6) { const r = rnd(7); X.save(); for (let i = 0; i < 70; i++) { const u = (t - jump) * (.7 + r() * .6), x = r() * W, y = -40 + u * (500 + r() * 500); X.fillStyle = ['#fde047', '#e02424', '#5ee7ff', '#7ee38a'][i % 4]; X.fillRect(x + Math.sin(u * 6 + i) * 30, y, 14, 22); } X.restore(); }
    if (t > Lt('s11_10') && t < Lt('s11_11')) sticker(X, 'ACTUACIÓN: 0/10', R(t, Lt('s11_10'), Lt('s11_10') + .25, back), 70, 70, 70, '#ffffff');
    futHUD(X, ga, hudN(t, door + .1, jump));
  }
};
