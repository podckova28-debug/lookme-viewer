/* Ep05 — scenes 6–11: the test in four seconds and the hamster power plant, the week of a genius, Pepe can't be calculated,
   tech support for the whole street, correcting everybody, a brain that never switches off */

/* ================================================================ 6. the test, the missing sign, the hamster that lights the room */
function boardExam(g) { const ink = '#3a6fb0', red = '#c0262d'; g.save(); g.textAlign = 'left'; g.font = 'bold 42px ComicNeue'; g.fillStyle = red; g.fillText('EXAMEN SORPRESA · 50 MIN', 380, 205);
  g.font = 'bold 48px ComicNeue'; g.fillStyle = ink; g.fillText('x = ( −b    √(b² − 4ac) ) / 2a', 380, 300); g.restore(); }
function hamsterWheel(g, x, y, t, spin = 0, lit = 0) {
  g.save(); g.translate(x, y); shape(g, q => q.rect(-8, -10, 16, 10), '#8a8f99', 3); line(g, [[0, -10], [0, -120]], '#8a8f99', 6);
  g.save(); g.translate(0, -120); g.rotate(spin); shape(g, q => q.arc(0, 0, 100, 0, 7), null, 8); for (let i = 0; i < 8; i++) { const a = i / 8 * Math.PI * 2; line(g, [[0, 0], [Math.cos(a) * 96, Math.sin(a) * 96]], '#9aa0aa', 3); } g.restore();
  // the motor and its two wires up to the bulb
  shape(g, q => rrPath(q, 70, -60, 60, 46, 8), '#6b7280', 4); circ(g, 100, -37, 10, '#f2c230', 3);
  g.strokeStyle = '#e0453c'; g.lineWidth = 5; g.beginPath(); g.moveTo(130, -50); g.bezierCurveTo(200, -80, 160, -260, 120, -330); g.stroke();
  g.strokeStyle = '#3a6fb0'; g.beginPath(); g.moveTo(130, -26); g.bezierCurveTo(230, -60, 190, -280, 140, -330); g.stroke();
  g.restore(); }
function ceilingBulb(g, x, y, lit) { line(g, [[x, 0], [x, y - 40]], '#3a3f48', 4); shape(g, q => rrPath(q, x - 16, y - 46, 32, 20, 4), '#8a8f99', 3);
  g.save(); if (lit) { g.shadowColor = '#ffe27a'; g.shadowBlur = 60 * lit; } shape(g, q => q.arc(x, y, 30, 0, 7), lit ? '#ffe27a' : '#e8edf3', 4); g.restore(); }
function notebookPage(X, a, t, t0s, rows, title = 'EL DE LOS RIZOS') { if (a <= 0) return; X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.globalAlpha = clamp(a);
  X.fillStyle = 'rgba(10,8,18,.55)'; X.fillRect(0, 0, W, H);
  const s = .85 + .15 * back(a); X.translate(W / 2, H / 2); X.rotate(-.02); X.scale(s, s);
  shape(X, q => rrPath(q, -620, -420, 1240, 840, 18), '#fbf6e6', 8);
  X.strokeStyle = 'rgba(80,140,200,.35)'; X.lineWidth = 3; for (let y = -300; y < 400; y += 92) { X.beginPath(); X.moveTo(-600, y); X.lineTo(600, y); X.stroke(); }
  X.strokeStyle = 'rgba(210,60,60,.55)'; X.beginPath(); X.moveTo(-470, -410); X.lineTo(-470, 410); X.stroke();
  for (let i = 0; i < 7; i++) circ(X, -585, -330 + i * 110, 14, '#2a2430', 0);
  text(X, title, -430, -330, 64, '#c0262d', 'Bangers', 'left');
  rows.forEach(([d, s2], i) => { if (t < t0s[i]) return; const u = clamp((t - t0s[i]) / .6), full = d + ' ' + s2, n = Math.round(u * full.length);
    X.save(); X.font = 'bold 54px ComicNeue'; X.fillStyle = '#2b3a67'; X.textAlign = 'left'; X.fillText(full.slice(0, n), -430, -200 + i * 170); X.restore(); });
  if (t > t0s[2] + 1.2) { X.save(); X.translate(430, 290); X.rotate(.1); drawAnimal(X, 'hamster', 0, 60, .7, { t }); ceilingBulb(X, 70, -40, 1); X.strokeStyle = '#c0262d'; X.lineWidth = 7; X.beginPath(); X.ellipse(10, 0, 130, 100, 0, 0, 7); X.stroke(); X.restore(); }
  X.restore(); }
SC.s06 = (X, t) => {
  const fast = Lt('s06_02') - .1, sign = Lt('s06_03') + .2, hamT = Lt('s06_07') - .05, book = Lt('s06_09') - .1, lit = Lt('s06_08') + .2;
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 540, z: 1.0, z2: 1.04, lock: 1 },
    { t: fast, cx: 860, cy: 600, z: 2.0, z2: 2.1, lock: 1 },
    { t: sign - .25, cx: 760, cy: 360, z: 1.7, z2: 1.75, lock: 1 },
    { t: Lt('s06_04') - .05, cx: 860, cy: 560, z: 1.9, z2: 2.0, lock: 1 },
    { t: Lt('s06_05') - .05, cx: 1400, cy: 470, z: 2.0, z2: 2.1, lock: 1 },
    { t: Lt('s06_06') - .05, cx: 1440, cy: 440, z: 2.8, z2: 2.95, lock: 1 },
    { t: hamT, cx: 1680, cy: 580, z: 2.2, z2: 2.3, lock: 1 },
    { t: lit - .25, cx: 1300, cy: 480, z: 1.15, z2: 1.2, lock: 1 },
  ]);
  const st = stage(cam), litA = R(t, lit, lit + .4);
  st.wld(g => { drawSet(g, 'classroom'); classDoor(g, 0); boardExam(g); if (t > Lt('s06_06') + .3) { g.save(); g.font = 'bold 60px ComicNeue'; g.fillStyle = '#c0262d'; g.fillText('±', 588, 304); g.restore(); } ceilingBulb(g, 1700, 200, t > hamT ? litA : 0); });
  const pp = standing(1440, { t, flip: -1, look: [-10, 10], mouth: -.1, brow: .4, hR: [120, -380], holdR: (g, x, y) => propBook(g, x + 6, y - 20, 90, 120, '#7b4b8a', -.2) });
  if (t > Lt('s06_02') && t < Lt('s06_04')) { pp.look = [-16, 4]; pp.brow = .8; pp.wide = .3; }
  if (t > Lt('s06_05')) { const k = (t - Lt('s06_05')) / Ld('s06_05'); if (k < .33) { pp.flip = 1; pp.look = [-10, -12]; } else if (k < .66) { pp.look = [4, 20]; pp.hR = [70, -340]; } else { pp.look = [-16, 4]; pp.lid = .35; pp.brow = 1; } }
  if (t > Lt('s06_06') - .1) { pp.flip = -1; pp.look = [-16, 4]; pp.lid = .45; pp.brow = 1; pp.mouth = -.4; }
  if (t > hamT) { pp.look = [14, 12]; pp.lid = 0; pp.brow = .2; pp.wide = litA; pp.mouth = .3 * litA; }
  say(pp, t, ['s06_01', 's06_06']);
  st.wld(g => drawChar(g, 'profe', pp));
  st.wld(g => { teacherDesk(g, 1620); drawSpr(g, 'cage', 1520, 704, 130); });
  const spin = t > hamT + 1.2 ? (t - hamT - 1.2) * (4 + 6 * R(t, hamT + 1.2, lit)) : 0;
  st.wld(g => { hamsterWheel(g, 1730, 700, t, spin, litA); if (t > hamT) drawAnimal(g, 'hamster', 1730, 690 + Math.abs(Math.sin(t * 14)) * -4 * (spin > 0 ? 1 : 0), .9, { t, head: 'side', flip: -1, tilt: Math.sin(t * 8) * .05 }); else drawAnimal(g, 'hamster', 1520, 712, .9, { t }); });
  st.wld(g => { drawChar(g, 'ex2', seated(470, { t, look: t > fast + .5 && t < sign ? [16, 4] : [14, 8], wide: t > fast + 1 && t < sign ? .8 : 0, mouth: .1, hL: [-70, -170], hR: [70, -170] })); desk(g, 470, FEET, .8); });
  const hp = seated(860, { t, look: [14, 6], mouth: .2, hL: [-70, -170], hR: [70, -170] });
  if (t > fast && t < fast + 1.6) { hp.hR = [60 + Math.sin(t * 40) * 40, -175]; hp.holdR = (g, x, y) => pencil(g, x, y); hp.look = [0, 18]; hp.brow = -.5; }
  if (t > fast + 1.6 && t < sign) { hp.hR = [110, -470]; hp.holdR = (g, x, y) => propPaper(g, x + 10, y - 30, -.05, .9); hp.mouth = .7; hp.look = [16, 0]; }
  if (t > sign) { hp.look = [-6, -14]; hp.brow = .3; }
  if (t > Lt('s06_04') - .1 && t < Lt('s06_05')) { hp.hR = [110, -520]; hp.look = [16, -4]; hp.mouth = .4; }
  if (t > hamT) { hp.x = 1180; hp.sit = 0; hp.y = FEET; hp.noShadow = 0; hp.look = [14, 12]; hp.mouth = .7; hp.hR = [150, -330]; }
  say(hp, t, ['s06_04']);
  st.col(g => drawChar(g, 'tu', hp)); if (t < hamT) st.wld(g => { desk(g, 860, FEET, .8); if (t > fast + 1.6) return; for (let i = 0; i < (t > fast ? Math.floor((t - fast) * 5) : 0); i++) propPaper(g, 840 + i * 6, 720 - i * 3, .1 * i, .6); });
  const gm = geniusState(t, [[fast, fast + 1.9], [sign, Lt('s06_04') - .2], [hamT + .1, lit]], cam, headPt('tu', hp, 60));
  genius(X, st, gm, t, [
    { k: 'label', at: [990, 420], s: 't = 4 s', t0: fast + .3, size: 60, col: GEN_YEL, out: fast + 1.9 },
    { k: 'label', at: [990, 480], s: '50 / 50 ✓', t0: fast + .9, size: 44, out: fast + 1.9 },
    { k: 'circle', at: [600, 285], r: 50, t0: sign + .2, out: Lt('s06_04') - .2 },
    { k: 'arrow', a: [700, 160], b: [620, 240], t0: sign + .5, out: Lt('s06_04') - .2 },
    { k: 'label', at: [700, 150], s: 'FALTA «±»', t0: sign + .6, col: GEN_RED, out: Lt('s06_04') - .2 },
    { k: 'box', at: [1730, 580], w: 260, h: 260, t0: hamT + .4, out: lit, s: 'SR. BIGOTES' },
    { k: 'label', at: [1300, 380], s: 'MOTOR + 2 CABLES', t0: hamT + 1.0, out: lit, size: 40 },
    { k: 'label', at: [1300, 440], s: '= 3 WATTS', t0: Lm('s06_07', .75), out: lit, size: 44, col: GEN_YEL },
  ]);
  if (t > hamT && litA > 0) { X.save(); X.globalCompositeOperation = 'screen'; X.globalAlpha = .25 * litA * (gm.amt ? 0 : 1); const [bx, by] = worldToScreen(cam, 1700, 200), gr = X.createRadialGradient(bx, by, 0, bx, by, 900); gr.addColorStop(0, '#fff3c4'); gr.addColorStop(1, 'rgba(0,0,0,0)'); X.fillStyle = gr; X.fillRect(0, 0, W, H); X.restore(); }
  if (t > Lt('s06_06') + .3 && t < hamT) comicWord(X, '¡HMPF!', ...worldToScreen(cam, 1560, 300), t - Lt('s06_06') - .3, 72, '#ffffff', 1.1);
  notebookPage(X, R(t, book, book + .35, outC), t, [Lt('s06_10') + .1, Lm('s06_10', .3), Lm('s06_10', .58)],
    [['LUNES:', 'sabe más que yo.'], ['MARTES:', 'sabe MUCHO más que yo.'], ['MIÉRCOLES:', 'el hámster da luz. No pregunten.']]);
};

/* ================================================================ 7. the week of a genius: Japanese, chess, penalties, the cube */
function tvSet(g, x, y, t, on = 1) { shape(g, q => rrPath(q, x - 230, y - 150, 460, 290, 16), '#23262e', 6); shape(g, q => rrPath(q, x - 210, y - 132, 420, 250, 8), on ? '#ffd1e3' : '#11141a', 3);
  if (on) { g.save(); g.beginPath(); g.rect(x - 210, y - 132, 420, 250); g.clip(); g.fillStyle = '#9fd6ff'; g.fillRect(x - 210, y - 132, 420, 140);
    const b = Math.sin(t * 6) * 6; shape(g, q => q.arc(x - 40, y + 10 + b, 70, 0, 7), '#fbe0cf', 4); shape(g, q => { q.moveTo(x - 115, y - 10 + b); q.lineTo(x - 70, y - 90 + b); q.lineTo(x - 30, y - 40 + b); q.lineTo(x + 10, y - 100 + b); q.lineTo(x + 35, y - 10 + b); q.closePath(); }, '#f05a8c', 4);
    for (const s of [-1, 1]) { shape(g, q => q.ellipse(x - 40 + s * 28, y + 10 + b, 16, 24, 0, 0, 7), '#2a2a5a', 3); circ(g, x - 40 + s * 28 + 5, y + b, 6, '#ffffff', 0); }
    text(g, '¡SUGOI!', x + 120, y - 60, 46, '#141014', 'Bangers', 'center'); g.restore(); }
  shape(g, q => q.rect(x - 20, y + 140, 40, 40), '#23262e', 4); shape(g, q => rrPath(q, x - 90, y + 176, 180, 16, 6), '#23262e', 3); }
function chessMonitor(g, x, y, t, dead = 0) { shape(g, q => rrPath(q, x - 210, y - 170, 420, 300, 18), '#d9dee6', 6); shape(g, q => rrPath(q, x - 188, y - 150, 376, 256, 8), dead ? '#0d0f14' : '#1f2a3a', 3);
  if (!dead) { const n = 8, s = 30, x0 = x - n * s / 2, y0 = y - 140; for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) { g.fillStyle = (i + j) % 2 ? '#7a5a3c' : '#e9d6b8'; g.fillRect(x0 + i * s, y0 + j * s, s, s); }
    const pc = [[1, 0, '♜'], [4, 0, '♚'], [6, 1, '♟'], [3, 7, '♔'], [5, 6, '♙'], [2, 4, '♛']]; g.font = '28px serif'; g.textAlign = 'center'; for (const [i, j, c] of pc) { g.fillStyle = j < 4 ? '#141014' : '#ffffff'; g.fillText(c, x0 + i * s + s / 2, y0 + j * s + s - 6); } }
  else { text(g, ':(', x, y - 10, 90, '#cfd6e6', 'Bangers', 'center'); }
  shape(g, q => q.rect(x - 22, y + 130, 44, 50), '#b8bec8', 4); shape(g, q => rrPath(q, x - 110, y + 176, 220, 18, 6), '#b8bec8', 3); }
function rubik(g, x, y, s, rot, solved) { g.save(); g.translate(x, y); g.rotate(rot); g.scale(s, s); const C = ['#e0453c', '#f2c230', '#4fbf6a', '#3a6fb0', '#ffffff', '#f08a3a'];
  shape(g, q => rrPath(q, -48, -48, 96, 96, 10), '#141014', 4); for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) { const c = solved ? C[0] : C[(i * 3 + j * 5 + Math.floor(rot * 3)) % 6]; shape(g, q => rrPath(q, -44 + i * 30, -44 + j * 30, 26, 26, 5), c, 0); } g.restore(); }
SC.s07 = (X, t) => {
  const c2 = Lt('s07_02') - .1, c3 = Lt('s07_03') - .1, c4 = Lt('s07_04') - .1, c5 = Lt('s07_05') - .1;
  if (t < c3) {   // 1+2: «you find out everything a genius can do», then Japanese in an afternoon
    const cam = shots(t, [], [{ t: 0, cx: 960, cy: 540, z: 1.0, z2: 1.06, lock: 1 }, { t: c2, cx: 820, cy: 560, z: 1.45, z2: 1.5, lock: 1 }, { t: Lm('s07_02', .55), cx: 1160, cy: 560, z: 1.5, z2: 1.55, lock: 1 }]);
    const st = stage(cam); st.wld(g => { drawSet(g, 'bedroom'); bedBack(g); nightstand(g); });
    const tvOn = t > Lm('s07_02', .55); st.wld(g => tvSet(g, 1450, 560, t, tvOn));
    const hp = { x: 760, y: 945, s: S0, t, look: [10, 14], mouth: .4, brow: -.2, hL: [-60, -330], hR: [60, -330], holdR: (g, x, y) => propBook(g, x - 60, y - 30, 140, 100, '#c0262d', 0) };
    if (t < c2) { hp.look = [0, -6]; hp.holdR = null; hp.hL = null; hp.hR = null; hp.mouth = .7; }
    if (tvOn) { hp.holdR = null; hp.hL = null; hp.hR = null; hp.look = [16, 0]; hp.mouth = .9; hp.brow = -.4; }
    st.col(g => drawChar(g, 'tu', hp)); st.wld(g => bedFront(g, .6));
    const gm = geniusState(t, [[c2 + .2, Lm('s07_02', .55)]], cam, headPt('tu', hp, 60)), r = rnd(3);
    const kana = ['あ', 'い', 'う', 'え', 'お', 'か', 'き', '日本語', 'ありがとう', 'すごい'].map((s, i) => ({ k: 'label', at: [500 + r() * 700, 260 + r() * 300], s, t0: c2 + .4 + i * .2, size: 46 + (i > 6 ? 0 : 10), bg: 0 }));
    genius(X, st, gm, t, [...kana, { k: 'label', at: [930, 760], s: 'JAPONÉS: 100%', t0: c2 + 2.4, size: 52, col: GEN_YEL }]);
    if (tvOn) sticker(X, 'SUBTÍTULOS: NO', R(t, Lm('s07_02', .6), Lm('s07_02', .6) + .3, back), 70, 70, 64);
    if (t < c2) sticker(X, 'UNA SEMANA DE GENIO', R(t, .3, .6, back), 70, 70, 70);
    return;
  }
  if (t < c4) {   // 3: chess against the library computer, four moves, it switches itself off
    const dead = t > Lm('s07_03', .78);
    const cam = shots(t, [], [{ t: 0, cx: 960, cy: 560, z: 1.25, z2: 1.3, lock: 1 }, { t: Lm('s07_03', .45), cx: 1180, cy: 520, z: 2.0, z2: 2.1, lock: 1 }]);
    const st = stage(cam); st.wld(g => { drawSet(g, 'salaMaestros'); });
    const hp = standing(820, { t, look: [16, 6], mouth: .2, brow: -.4, hR: [260, -300], hL: [-60, -330] });
    if (dead) { hp.look = [16, 4]; hp.mouth = .6; hp.brow = .2; hp.hR = null; hp.hL = null; }
    st.col(g => drawChar(g, 'tu', hp));
    st.wld(g => { desk(g, 1180, FEET, 1); chessMonitor(g, 1180, 520, t, dead); });
    const gm = geniusState(t, [[c3 + .2, Lm('s07_03', .7)]], cam, headPt('tu', hp, 60));
    const sq = (i, j) => [1180 - 120 + i * 30 + 15, 520 - 140 + j * 30 + 15];
    genius(X, st, gm, t, [
      { k: 'arrow', a: sq(2, 4), b: sq(5, 1), t0: c3 + .6, d: .3, hs: 12, lw: 4 }, { k: 'arrow', a: sq(5, 6), b: sq(5, 4), t0: c3 + 1.2, d: .3, hs: 12, lw: 4 },
      { k: 'arrow', a: sq(1, 0), b: sq(1, 3), t0: c3 + 1.8, d: .3, hs: 12, lw: 4 }, { k: 'arrow', a: sq(5, 1), b: sq(4, 0), t0: c3 + 2.4, d: .3, hs: 12, lw: 4 },
      { k: 'label', at: [1180, 300], s: 'JAQUE MATE: 4', t0: c3 + 2.8, size: 52, col: GEN_YEL, align: 'center' },
    ]);
    sticker(X, 'TÚ VS. LA COMPUTADORA', R(t, c3 + .1, c3 + .4, back), 70, 70, 64);
    if (dead) comicWord(X, 'BIP… BUUU', ...worldToScreen(cam, 1180, 330), t - Lm('s07_03', .78), 72, '#ffffff', 1.4);
    return;
  }
  if (t < c5) {   // 4: penalties, 100 out of 100
    const kick = c4 + 1.2, sad = Lm('s07_04', .6);
    const cam = shots(t, [], [{ t: 0, cx: 960, cy: 560, z: 1.0, z2: 1.05, lock: 1 }, { t: sad, cx: 1560, cy: 520, z: 2.4, z2: 2.5, lock: 1 }]);
    const st = stage(cam); st.wld(g => { drawSet(g, 'field'); goal(g, 0); });
    const loop = 1.35, k = Math.floor(Math.max(0, t - kick) / loop), u = clamp((Math.max(0, t - kick) % loop) / .7), corner = k % 2 ? [1360, 330] : [1820, 330];
    const kp = { x: 1590, y: 650, s: .4, t, handCol: '#f08a3a', look: [-12, 6], mouth: -.1, brow: .4, hL: [-150, -380], hR: [150, -380] };
    if (t > kick) { const dir = k % 2 ? 1 : -1; kp.lean = dir * .35 * clamp(u * 2); kp.x = 1590 + dir * 50 * clamp(u * 2); }
    if (t > sad) Object.assign(kp, { x: 1590, y: 650, lean: 0, hL: [-40, -470], hR: [40, -470], look: [0, 20], mouth: -.5, brow: .8, wide: .2 });
    st.wld(g => drawChar(g, 'ex1', kp));
    const ballAt = s => [mix(860, corner[0], s), mix(900, corner[1], s) - Math.sin(s * Math.PI) * 140];
    if (t < sad) { const [bx, by] = t > kick ? ballAt(u) : [860, 900]; st.wld(g => propBall(g, bx, by, mix(34, 18, t > kick ? u : 0), u * 10)); }
    st.wld(g => goal(g, 1));
    const hp = standing(760, { t, look: [16, -6], mouth: .5, brow: -.4 });
    if (t > kick && t < sad && u < .25) { hp.lean = .12; hp.walk = 1; hp.phase = Math.PI * .5; }
    st.col(g => drawChar(g, 'tu', hp));
    const gm = geniusState(t, [[c4 + .3, sad]], cam, headPt('tu', hp, 60));
    genius(X, st, gm, t, [{ k: 'arc', a: [860, 900], b: [1820, 330], h: 140, t0: c4 + .5, d: .6, dash: 1, mark: 1, out: sad }, { k: 'arc', a: [860, 900], b: [1360, 330], h: 140, t0: c4 + .8, d: .6, dash: 1, mark: 1, out: sad },
      { k: 'label', at: [900, 300], s: 'ÁNGULO 23°', t0: c4 + 1.0, out: sad, size: 40 }, { k: 'label', at: [900, 350], s: 'V = 92 km/h', t0: c4 + 1.3, out: sad, size: 40 }]);
    if (t < sad + .4) bigCounter(X, 'PENALES:', Math.min(100, (t > kick ? (k + 1) * 9 + Math.floor(u * 9) : 0)) + '/100', R(t, c4 + .2, c4 + .5), 70, 70);
    if (t > sad + .3) sticker(X, 'EL PORTERO SE CAMBIA DE ESCUELA', R(t, sad + .3, sad + .6, back), 70, 70, 60);
    return;
  }
  // 5: the cube, eyes shut, one hand, while it falls
  const toss = c5 + .4, land = c5 + 2.6;
  const cam = shots(t, [], [{ t: 0, cx: 900, cy: 500, z: 1.7, z2: 1.85, lock: 1 }]);
  const st = stage(cam); st.wld(g => drawSet(g, 'hallway'));
  const hp = standing(900, { t, look: [0, -6], mouth: .3, sleep: t > toss - .2 ? 1 : 0, brow: -.3, hR: [110, -360] });
  const cu = R(t, toss, land, lin), cy = t < toss ? -360 : -360 - Math.sin(cu * Math.PI) * 520;
  const G = charGeom(CAST.tu, hp); if (t > toss && t < land) hp.hR = [110 + Math.sin(t * 30) * 25, Math.max(cy, -560)];
  st.col(g => drawChar(g, 'tu', hp));
  const [hx, hy] = [900 + 110 * S0, FEET + cy * S0 - 40];
  st.wld(g => rubik(g, hx, hy, .9, t > toss ? (t - toss) * 9 * (1 - cu) : 0, t > land - .3));
  const gm = geniusState(t, [[toss - .1, land + .2]], cam, headPt('tu', hp, 60));
  genius(X, st, gm, t, [{ k: 'label', at: [1080, 260], s: 'OJOS CERRADOS', t0: toss + .1, size: 40 }, { k: 'label', at: [1080, 320], s: '1 MANO', t0: toss + .5, size: 40 }, { k: 'label', at: [1080, 380], s: 't = 0,9 s', t0: toss + .9, size: 44, col: GEN_YEL }]);
  if (t > land - .2) { comicWord(X, '¡LISTO!', ...worldToScreen(cam, hx + 160, hy - 120), t - land + .2, 80); }
};

/* ================================================================ 8. everything, except Pepe */
SC.s08 = (X, t) => {
  const on = Lt('s08_02') - .1, pep = Lt('s08_03') - .05, err = Lt('s08_04') + .2, off = Lm('s08_08', .4);
  const cam = shots(t, [], [
    { t: 0, cx: 900, cy: 560, z: 1.2, z2: 1.25, lock: 1 },
    { t: on, cx: 960, cy: 520, z: 1.0, z2: 1.04, lock: 1 },
    { t: pep, cx: 1320, cy: 680, z: 2.2, z2: 2.4, lock: 1 },
    { t: Lt('s08_05') - .05, cx: 1300, cy: 700, z: 2.6, z2: 2.7, lock: 1 },
    { t: Lt('s08_06') - .05, cx: 900, cy: 560, z: 1.6, z2: 1.65, lock: 1 },
    { t: Lt('s08_07') - .05, cx: 1340, cy: 700, z: 3.0, z2: 3.1, lock: 1 },
    { t: Lt('s08_08') - .05, cx: 760, cy: 520, z: 1.9, z2: 2.0, lock: 1 },
  ]);
  const st = stage(cam), lu = R(t, on + 1.6, on + 4, lin);
  st.wld(g => { drawSet(g, 'park'); bench(g, 0); bench(g, 1); if (lu < 1) leaf(g, mix(1500, 1620, lu) + Math.sin(lu * 9) * 30, mix(300, 930, lu), Math.sin(t * 4)); });
  // Pepe stays in colour: the blueprint can't take him
  const coo = speaking(t, 's08_07');
  st.col(g => pigeonTalk(g, 1340, 792, .62, { flip: -1, front: t > Lt('s08_06'), open: coo ? .5 : 0, tilt: Math.sin(t * 1.2) * .06 }));
  const hp = standing(820, { t, look: [14, 8], mouth: .3 });
  if (t > pep) { hp.look = [16, 12]; hp.brow = .5; hp.mouth = -.1; }
  if (t > Lt('s08_05')) { hp.hR = [220, -330]; hp.holdR = (g, x, y) => { g.save(); g.translate(x, y); g.rotate(-.1); shape(g, q => q.rect(-10, -150, 26, 170), '#f2c230', 3); for (let i = 0; i < 8; i++) line(g, [[-10, -140 + i * 20], [2, -140 + i * 20]], '#141014', 2); g.restore(); }; hp.look = [16, 14]; hp.brow = .8; }
  if (t > Lt('s08_06') - .1) { hp.hR = null; hp.holdR = null; hp.look = [16, 10]; hp.brow = .6; }
  if (t > Lt('s08_08')) { hp.look = [6, 2]; hp.mouth = -.4; hp.brow = 1; }
  say(hp, t, ['s08_06']);
  st.col(g => drawChar(g, 'tu', hp));
  const gm = geniusState(t, [[on, off]], cam, headPt('tu', hp, 60));
  const glitch = t > err ? (Math.sin(t * 23) > .3 ? 6 : 0) : 0;
  genius(X, st, gm, t, [
    { k: 'label', at: [140, 160], s: 'LLUVIA HOY: 0%', t0: on + .3, size: 40, out: pep },
    { k: 'label', at: [140, 220], s: 'VIENTO: 6 km/h NE', t0: on + .7, size: 40, out: pep },
    { k: 'arc', a: [1500, 300], b: [1620, 930], h: -40, t0: on + 1.4, d: .7, dash: 1, mark: 1, out: pep },
    { k: 'label', at: [1440, 250], s: 'HOJA: 2,4 s', t0: on + 1.8, size: 40, out: pep },
    { k: 'box', at: [1335 + glitch, 715], w: 190, h: 200, t0: pep + .3, col: t > err ? GEN_RED : GEN_INK, s: t > err ? 'DATOS INSUFICIENTES' : 'PEPE', size: 34 },
    { k: 'dim', a: [1240, 820], b: [1240, 610], s: '¿? cm', t0: Lt('s08_05') + .2, ox: -80, col: GEN_RED },
    { k: 'label', at: [1420, 640], s: 'PLUMAS: 1… 2… ERROR', t0: Lm('s08_05', .4), size: 36, col: GEN_RED },
  ]);
  if (t > Lt('s08_07')) cooBubble(X, cam, 1340, 660, t, Lt('s08_07'), Ld('s08_07') + .4);
  if (t > err && t < Lt('s08_06') && gm.a > 0) { X.save(); X.globalAlpha = .12 * gm.a; X.fillStyle = Math.sin(t * 30) > 0 ? '#ff8f9a' : '#123a6e'; X.fillRect(0, 0, W, H); X.restore(); }
};

/* ================================================================ 9. problem 1: you're the street's tech support */
function supportTable(g, x) { for (const dx of [-210, 196]) shape(g, q => q.rect(x + dx, 726, 14, 210), '#6b6f78', 3); shape(g, q => rrPath(q, x - 230, 700, 460, 26, 6), '#c4945c', 5);
  shape(g, q => { q.moveTo(x - 200, 726); q.lineTo(x + 200, 726); q.lineTo(x + 190, 850); q.lineTo(x - 190, 850); q.closePath(); }, '#fffbe8', 5);
  text(g, 'SOPORTE TÉCNICO', x, 784, 52, '#c0262d', 'Bangers', 'center'); text(g, 'GRATIS (POR AHORA)', x, 830, 34, '#141014', 'Bangers', 'center'); }
function router(g, x, y, s = 1) { g.save(); g.translate(x, y); g.scale(s, s); shape(g, q => rrPath(q, -60, -26, 120, 30, 8), '#2e333d', 4); for (const dx of [-40, 40]) line(g, [[dx, -26], [dx * 1.2, -80]], '#2e333d', 6); for (let i = 0; i < 4; i++) circ(g, -36 + i * 24, -11, 4, i < 2 ? '#4fbf6a' : '#e0453c', 0); g.restore(); }
function smallTv(g, x, y, s = 1) { g.save(); g.translate(x, y); g.scale(s, s); shape(g, q => rrPath(q, -80, -60, 160, 110, 10), '#23262e', 5); shape(g, q => rrPath(q, -68, -48, 136, 86, 5), '#5a6170', 0); g.strokeStyle = 'rgba(255,255,255,.4)'; g.lineWidth = 2; for (let i = 0; i < 6; i++) { g.beginPath(); g.moveTo(-68, -40 + i * 14); g.lineTo(68, -40 + i * 14 + 4); g.stroke(); } g.restore(); }
function notebookStack(g, x, y, n, sway = 0) { for (let i = 0; i < n; i++) { const c = ['#3a6fb0', '#e0453c', '#4fbf6a', '#f2c230', '#9c6fcf'][i % 5]; propBook(g, x + Math.sin(i * 1.7) * 6 + sway * i * 1.2, y - i * 18, 110, 18, c, 0); } }
SC.s09 = (X, t) => {
  const tues = Lt('s09_02') - .05, fix = Lt('s09_03') - .05, nach = Lt('s09_04') - .05, wide = Lt('s09_06') - .05;
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 540, z: 1.0, z2: 1.05, lock: 1 },
    { t: fix, cx: 860, cy: 560, z: 1.5, z2: 1.55, lock: 1 },
    { t: nach, cx: 1100, cy: 520, z: 1.6, z2: 1.7, lock: 1 },
    { t: wide, cx: 960, cy: 540, z: 1.0, z2: .98, lock: 1 },
  ]);
  const st = stage(cam), k3 = (t - fix) / Ld('s09_03');
  st.wld(g => drawSet(g, 'street'));
  // the queue: doña Lupe's internet, the neighbour's TV; at the end the line reaches the horizon
  const Q = [['ex4', 1180, 'router'], ['ex1', 1360, 'tv'], ['ex5', 1540, 'phone'], ['ex6', 1700, 'router'], ['ex2', 1850, 'tv']];
  Q.forEach(([n, x, item], i) => { if (t < wide && i > 2) return; const served = t > fix && k3 > (i + 1) * .3 && i < 2 && t < wide;
    const p = standing(x - (served ? 0 : 0), { t, flip: -1, look: [-14, 6], mouth: served ? .6 : -.2, brow: served ? -.4 : .5, hR: [100, -360], hL: [-100, -360] });
    if (!served) p.holdR = (g, x2, y2) => item === 'router' ? router(g, x2 - 90, y2 + 10, .9) : item === 'tv' ? smallTv(g, x2 - 90, y2 - 10, .8) : propPhone(g, x2, y2 - 20, .5, 80, 0);
    st.wld(g => drawChar(g, n, p)); });
  if (t > wide) st.wld(g => { for (let i = 0; i < 12; i++) drawChar(g, ['ex1', 'ex2', 'ex3', 'ex4', 'ex5', 'ex6'][i % 6], { x: 1300 + i * 70, y: 760 - i * 6, s: .42 - i * .015, t: t + i, flip: -1, look: [-10, 4], mouth: -.2 }); });
  const hp = standing(700, { t, look: [14, 6], mouth: .3, hR: [130, -330], hL: [-60, -330] });
  if (t > fix && t < nach) { hp.hR = [150 + Math.sin(t * 22) * 30, -330]; hp.hL = [90 + Math.cos(t * 19) * 30, -320]; hp.look = [10, 18]; hp.brow = -.5; }
  if (t > nach) { hp.look = [16, -6]; hp.wide = .6; hp.brow = .6; hp.mouth = -.2; hp.hR = null; hp.hL = null; }
  if (t > wide) { hp.slump = 1; hp.mouth = -.5; hp.lid = .3; hp.look = [0, 10]; hp.sweat = 1; }
  st.col(g => drawChar(g, 'tu', hp));
  st.wld(g => { supportTable(g, 760);
    const fixed = t > fix ? Math.floor(clamp(k3) * 6) : 0; for (let i = 0; i < fixed; i++) router(g, 580 + i * 20, 700 - i * 4, .5);
    if (t > Lm('s09_03', .6)) { const ring = Math.sin(t * 30) * .08; propPhone(g, 920, 690, .5, 60, ring); } });
  const np = standing(1060, { t, flip: -1, look: [-14, 0], mouth: .6, brow: -.4, hL: [-70, -300], hR: [70, -300] });
  if (t > nach) { const u = R(t, nach, nach + 1.0); np.x = mix(1400, 1060, u); np.walk = u < 1 ? 1 : 0; np.phase = walkPh(np.x); np.hR = [110, -330]; np.hL = [-110, -330]; np.armsFront = 1; np.holdR = (g, x, y) => notebookStack(g, x - 70, y + 10, 18, Math.sin(t * 3) * .5);
    if (speaking(t, 's09_05')) { np.open = talk(t, 's09_05'); } if (t < wide) st.wld(g => drawChar(g, 'nacho', np)); }
  const gm = geniusState(t, [[fix + .1, nach - .2]], cam, headPt('tu', hp, 60));
  genius(X, st, gm, t, [
    { k: 'label', at: [460, 300], s: 'INTERNET DE DOÑA LUPE ✓', t0: Lm('s09_03', .05), size: 38 },
    { k: 'label', at: [460, 360], s: 'TELE DEL VECINO ✓', t0: Lm('s09_03', .35), size: 38 },
    { k: 'label', at: [460, 420], s: 'CELULAR DE LA ABUELA ✓ ✓ ✓', t0: Lm('s09_03', .65), size: 38, col: GEN_YEL },
  ]);
  sticker(X, 'MARTES', vis(t, tues + .1, fix - .2), 70, 70, 64);
  if (t > Lm('s09_03', .6) && t < nach) { const [x, y] = worldToScreen(cam, 920, 560); bubble(X, 'ABUELA (3)', x, y, R(t, Lm('s09_03', .6), Lm('s09_03', .6) + .3, back), 46); }
  if (t > nach + .4 && t < wide) { const [x, y] = worldToScreen(cam, 1200, 300); X.save(); X.globalAlpha = R(t, nach + .4, nach + .7); text(X, 'TAREA DEL SEMESTRE', x, y, 54, '#fde047', 'Bangers', 'center', OUT, 10); X.restore(); }
  if (t > wide + .3) sticker(X, 'LOS PROBLEMAS DE TODOS = TU PROBLEMA', R(t, wide + .3, wide + .6, back), 70, 70, 58);
};

/* ================================================================ 10. problem 2: you can't stop correcting people */
SC.s10 = (X, t) => {
  const c83 = Lt('s10_03') - .1, sky = Lt('s10_04') - .05, lect = Lt('s10_05') - .1, gone = Lt('s10_06') - .05, thu = Lt('s10_07') - .05, rule = Lt('s10_08') - .1;
  if (t < thu) {
    const cam = shots(t, [], [
      { t: 0, cx: 960, cy: 560, z: 1.1, z2: 1.15, lock: 1 },
      { t: Lt('s10_02') - .05, cx: 1180, cy: 520, z: 2.0, z2: 2.1, lock: 1 },
      { t: c83, cx: 820, cy: 500, z: 1.8, z2: 1.85, lock: 1 },
      { t: sky, cx: 1360, cy: 520, z: 2.0, z2: 2.1, lock: 1 },
      { t: lect, cx: 960, cy: 480, z: 1.15, z2: 1.2, lock: 1 },
    ]);
    const st = stage(cam); st.wld(g => drawSet(g, 'street'));
    const np = standing(1160, { t, flip: -1, look: [-14, 0], mouth: .5, brow: -.3 });
    if (speaking(t, 's10_02')) { np.open = talk(t, 's10_02'); np.hR = [200, -480]; np.hL = [-200, -480]; }
    if (t > c83) { np.look = [-16, 2]; np.mouth = -.3; np.brow = .7; np.lid = .3; }
    if (t > lect) { np.look = [-16, -4]; np.lid = .5; np.mouth = -.2; }
    const rp = standing(1400, { t, flip: -1, look: [-4, -16], mouth: .5, brow: -.2, blush: .3 });
    say(rp, t, ['s10_04']);
    if (t > lect) { rp.look = [-16, 4]; rp.mouth = -.1; rp.brow = .5; }
    if (t > gone) { const u = R(t, gone, gone + 2.4, lin); rp.x = mix(1400, 2100, u); rp.walk = u < 1 ? 1 : 0; rp.phase = walkPh(rp.x); rp.flip = 1; rp.look = [14, 0]; }
    st.wld(g => { drawChar(g, 'nacho', np); drawChar(g, 'valeria', rp); });
    const hp = standing(800, { t, look: [14, 0], mouth: .3 });
    say(hp, t, ['s10_03', 's10_05']);
    if (t > c83) { hp.brow = -.5; hp.look = [16, -2]; }
    if (t > lect) { const G = charGeom(CAST.tu, hp); hp.hR = POSE.point(1, G, 1)[1]; hp.hR[1] -= 120; hp.look = [10, -14]; hp.brow = -.6; hp.mouth = .5; }
    if (t > gone + .6) { hp.look = [16, 0]; hp.hR = null; hp.brow = .4; }
    st.col(g => drawChar(g, 'tu', hp));
    const gm = geniusState(t, [[c83, c83 + 1.4], [lect, gone + 1]], cam, headPt('tu', hp, 60));
    const dots = []; for (let i = 0; i < 18; i++) dots.push({ k: 'tick', at: [330 + (i % 6) * 56, 250 + Math.floor(i / 6) * 64], r: 14, t0: c83 + .1 + i * .04, d: .15, out: c83 + 1.4 });
    genius(X, st, gm, t, [...dots, { k: 'label', at: [310, 470], s: '= 83 PERSONAS', t0: c83 + .6, out: c83 + 1.4, col: GEN_YEL },
      { k: 'circle', at: [1700, 160], r: 90, t0: lect + .2, out: gone + 1 },
      { k: 'arrow', a: [1600, 210], b: [1160, 330], t0: lect + .5, out: gone + 1 }, { k: 'label', at: [1240, 260], s: 'LUZ BLANCA', t0: lect + .6, out: gone + 1, size: 40 },
      { k: 'arrow', a: [1160, 330], b: [1000, 180], t0: lect + 1.0, out: gone + 1, col: '#9fd6ff' }, { k: 'arrow', a: [1160, 330], b: [1300, 470], t0: lect + 1.1, out: gone + 1, col: '#9fd6ff' },
      { k: 'label', at: [760, 160], s: 'AZUL: SE DISPERSA MÁS', t0: lect + 1.4, out: gone + 1, size: 40, col: '#9fd6ff' },
      { k: 'label', at: [760, 230], s: '∝ 1 / λ⁴', t0: lect + 2.0, out: gone + 1, size: 50, col: GEN_YEL },
    ]);
    if (t > gone + .3) { const [x, y] = worldToScreen(cam, 1500, 330); X.save(); X.globalAlpha = R(t, gone + .3, gone + .6); text(X, '…', x, y, 120, '#ffffff', 'Bangers', 'center', OUT, 10); X.restore(); }
    return;
  }
  // Thursday: the hallway goes quiet around you
  const cam = shots(t, [], [{ t: 0, cx: 960, cy: 540, z: 1.0, z2: 1.08, lock: 1 }]);
  const st = stage(cam); st.wld(g => drawSet(g, 'hallway'));
  const k = t - thu;
  [['ex1', 300, 1], ['ex4', 1500, -1], ['nacho', 1250, -1], ['ex2', 520, 1]].forEach(([n, x0, dir], i) => { const away = k > .6 + i * .4; st.wld(g => drawChar(g, n, standing(x0 + (away ? dir * -120 * R(t, thu + .6 + i * .4, thu + 1.4 + i * .4) : 0), { t, flip: away ? -dir : dir, look: [away ? -dir * 14 : dir * 14, 4], mouth: away ? -.3 : .4, brow: away ? .5 : 0 }))); });
  const hp = standing(960, { t, look: [0, 4], mouth: .5, brow: .3, hR: [140, -470] });
  if (k > 2) { hp.mouth = -.4; hp.hR = null; hp.slump = .6; hp.brow = .8; hp.look = [0, 12]; }
  st.col(g => drawChar(g, 'tu', hp));
  composeG(X, st, { amt: 0 });
  sticker(X, 'JUEVES', vis(t, thu + .1, rule - .2), 70, 70, 64);
  ruleCard(X, 2, 'TENER LA RAZÓN Y CAER BIEN', 'SON DOS COSAS DISTINTAS', R(t, rule, rule + .3, outC));
};

/* ================================================================ 11. problem 3: a brain that never switches off */
function shirt(g, x, y, c, rot) { g.save(); g.translate(x, y); g.rotate(rot); shape(g, q => { q.moveTo(-40, -50); q.lineTo(-70, -30); q.lineTo(-58, -6); q.lineTo(-40, -14); q.lineTo(-40, 50); q.lineTo(40, 50); q.lineTo(40, -14); q.lineTo(58, -6); q.lineTo(70, -30); q.lineTo(40, -50); q.quadraticCurveTo(0, -30, -40, -50); }, c, 4); g.restore(); }
SC.s11 = (X, t) => {
  const night = Lt('s11_02') - .05, shirts = Lt('s11_03') - .05, caf = Lt('s11_04') - .05, grab = Lt('s11_06') - .05;
  if (t < shirts) {   // 1–2: «the worst one», a brain that never switches off: lying awake at night
    const cam = shots(t, [], [{ t: 0, cx: 640, cy: 600, z: 1.4, z2: 1.5, lock: 1 }]);
    const st = stage(cam); st.wld(g => { drawSet(g, 'bedroom'); bedBack(g); nightstand(g); propAlarm(g, 1075, 740, .55, 3, 12, 0); });
    st.col(g => lyingHead(g, 300, 680, { sleep: 0, wide: .5, look: [10, -16], mouth: -.2, brow: .5 })); st.wld(g => bedFront(g, 1));
    const gm = geniusState(t, [[night + .2, 99]], cam, [300, 600]);
    const r = rnd(8); const swirl = []; for (let i = 0; i < 12; i++) swirl.push({ k: 'label', at: [500 + r() * 700, 250 + r() * 380], s: ['π = 3,14159…', 'E = mc²', '¿Y SI…?', 'Σ', '√2', 'ZZZ ✗', '3:12 AM', '∞', 'Δx', 'p > 0,05', 'H₂O', '42'][i], t0: night + .4 + i * .2, size: 40 + (i % 3) * 8, bg: 0 });
    genius(X, st, gm, t, swirl);
    nightTint(X, 1 - gm.a);
    sticker(X, 'PROBLEMA #3', vis(t, .2, night - .1), 70, 70, 70);
    return;
  }
  if (t < caf) {   // 3: forty combinations to choose a shirt
    const cam = shots(t, [], [{ t: 0, cx: 960, cy: 540, z: 1.15, z2: 1.2, lock: 1 }]);
    const st = stage(cam); st.wld(g => { drawSet(g, 'bedroom'); bedBack(g); nightstand(g); });
    const hp = standing(1000, { t, look: [0, 4], mouth: -.1, brow: .6, hL: [-160, -380], hR: [160, -380] });
    const C = ['#e0453c', '#3a6fb0', '#4fbf6a', '#f2c230', '#9c6fcf', '#ffffff', '#f08a3a'];
    st.wld(g => { for (let i = 0; i < 9; i++) { const u = loopU(t, i * .23, 1.8); shirt(g, 1000 + Math.cos(i * 2.1 + t) * (260 + u * 120), 520 + Math.sin(i * 1.7 + t * 1.3) * 200, C[i % 7], Math.sin(t * 3 + i)); } });
    st.col(g => drawChar(g, 'tu', hp));
    const gm = geniusState(t, [[shirts + .1, caf - .3]], cam, headPt('tu', hp, 60));
    const grid = []; for (let i = 0; i < 8; i++) for (let j = 0; j < 5; j++) grid.push({ k: 'x', at: [180 + i * 36, 260 + j * 40], r: 10, t0: shirts + .3 + (i * 5 + j) * .04, d: .12 });
    genius(X, st, gm, t, [...grid, { k: 'label', at: [180, 500], s: '40 COMBINACIONES', t0: shirts + 1.6, size: 44, col: GEN_YEL }]);
    if (t > Lm('s11_03', .75)) sticker(X, '30 MIN DESPUÉS…', R(t, Lm('s11_03', .75), Lm('s11_03', .75) + .3, back), 70, 70, 64);
    return;
  }
  // 4–7: torta or quesadilla
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 540, z: 1.0, z2: 1.04, lock: 1 },
    { t: Lt('s11_05') - .05, cx: 860, cy: 480, z: 1.35, z2: 1.45, lock: 1 },
    { t: grab, cx: 1000, cy: 520, z: 1.6, z2: 1.65, lock: 1 },
    { t: Lt('s11_07') - .05, cx: 860, cy: 520, z: 1.9, z2: 2.0, lock: 1 },
  ]);
  const st = stage(cam); st.wld(g => drawSet(g, 'cafeteria'));
  const got = t > grab + .5;
  const np = standing(1250, { t, flip: -1, look: [-14, 4], mouth: .2, brow: .2 });
  if (t > Lm('s11_05', .5)) { np.brow = .9; np.mouth = -.4; np.lid = .4; np.look = [-16, 0]; }
  if (t > grab) { np.hR = [-180, -380]; np.hL = [140, -360]; np.mouth = .5; np.brow = .8; np.lean = -.08; np.holdR = !got ? (g, x, y) => drawSpr(g, 'torta', x, y + 30, 80) : null; }
  if (t > grab + 1.2) { np.hR = null; np.hL = null; np.lean = 0; np.mouth = .6; np.brow = -.3; np.lid = 0; }
  say(np, t, ['s11_06']);
  st.wld(g => drawChar(g, 'nacho', np));
  const hp = standing(820, { t, look: [6, -6], mouth: -.1, brow: .2 });
  if (t > Lt('s11_05') - .1) { hp.look = [6, -12]; hp.brow = -.5; hp.hR = [70, -440]; }
  if (got) { hp.hR = [130, -320]; hp.holdR = (g, x, y) => drawSpr(g, 'torta', x, y + 30, 80); hp.look = [10, 14]; hp.brow = .7; hp.mouth = -.3; }
  st.col(g => drawChar(g, 'tu', hp));
  const gm = geniusState(t, [[Lt('s11_05') - .1, grab]], cam, headPt('tu', hp, 60));
  const crit = [['PRECIO', '$35 / $30'], ['CALORÍAS', '540 / 480'], ['FILA', '4 min / 6 min'], ['CLIMA', '22°C'], ['¿QUÉ DICE DE MÍ?', '???']];
  genius(X, st, gm, t, crit.map(([a2, b2], i) => ({ k: 'label', at: [1040, 220 + i * 62], s: a2 + ': ' + b2, t0: Lm('s11_05', .05 + i * .17), size: 40, col: i === 4 ? GEN_RED : GEN_INK })), gm.amt);
  if (t > Lt('s11_04') - .05 && t < Lt('s11_05') + .5) bubble(X, '¿TORTA O QUESADILLA?', W - 420, 300, R(t, Lt('s11_04') + .2, Lt('s11_04') + .5, back) * (1 - R(t, Lt('s11_05') + .2, Lt('s11_05') + .5)), 60);
  if (t > Lt('s11_07') + .2) sticker(X, '+ LISTO = + LENTO PARA LO FÁCIL', R(t, Lt('s11_07') + .2, Lt('s11_07') + .5, back), 70, 70, 60);
};
