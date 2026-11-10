/* Ep01 scenes 11–17: aging, nothing works, birthday applause, Pepe, the flowerpot, the twist, outro. */
const CHANNEL_NAME = 'PONLE QUE…';
function clockFace(g, x, y, r, label, spin, gray) { g.save(); g.translate(x, y); circ(g, 0, 0, r, gray ? '#c9d2dc' : '#fde047', 7); circ(g, 0, 0, r * .82, '#fbfaf6', 5);
  for (let i = 0; i < 12; i++) { const a = i * Math.PI / 6; line(g, [[Math.cos(a) * r * .66, Math.sin(a) * r * .66], [Math.cos(a) * r * .76, Math.sin(a) * r * .76]], OUT, 5); }
  const am = spin * 2 * Math.PI - Math.PI / 2, ah = spin * 2 * Math.PI / 12 - Math.PI / 2 + (gray ? 2.1 : 0);
  line(g, [[0, 0], [Math.cos(ah) * r * .4, Math.sin(ah) * r * .4]], OUT, 10); line(g, [[0, 0], [Math.cos(am) * r * .62, Math.sin(am) * r * .62]], OUT, 7); circ(g, 0, 0, 10, OUT, 0);
  text(g, label, 0, r + 70, 64, gray ? '#c9d2dc' : '#fde047', 'Bangers', 'center', OUT, 10); g.restore(); }
function calendarCard(g, a, t) { if (a <= 0) return; g.save(); g.globalAlpha = clamp(a); g.translate(W * .7, H * .45); g.rotate(.05); const k = .85 + .15 * back(a); g.scale(k, k);
  shape(g, q => rrPath(q, -200, -230, 400, 460, 16), '#fbfaf6', 7); shape(g, q => rrPath(q, -200, -230, 400, 110, 16), '#c0262d', 7); text(g, 'CALENDARIO', 0, -155, 54, '#ffffff', 'Bangers', 'center');
  for (const x of [-120, 120]) circ(g, x, -230, 16, '#9aa3ad', 4);
  text(g, '+13', 0, 60, 190, '#c0262d', 'Bangers', 'center'); text(g, 'DÍAS', 0, 170, 90, OUT, 'Bangers', 'center'); g.restore(); }
function tv(g, x, y, frame, paused) { shape(g, q => rrPath(q, x - 150, y - 100, 300, 190, 12), '#26262e', 6); g.save(); g.beginPath(); g.rect(x - 134, y - 86, 268, 162); g.clip();
  g.fillStyle = '#7fb5e0'; g.fillRect(x - 134, y - 86, 268, 162); g.fillStyle = '#5a9a5c'; g.fillRect(x - 134, y + 30, 268, 60); drawChar(g, 'ex3', { x: x - 40, y: y + 64, s: .17, still: 1, hR: [200, -500], mouth: .5 }); drawChar(g, 'ex4', { x: x + 50, y: y + 64, s: .17, still: 1, open: .6 });
  if (paused) { g.fillStyle = 'rgba(0,0,0,.35)'; g.fillRect(x - 134, y - 86, 268, 162); g.fillStyle = '#ffffff'; g.fillRect(x - 30, y - 40, 20, 70); g.fillRect(x + 10, y - 40, 20, 70); }
  g.restore(); tube(g, [[x, y + 90], [x, y + 116]], '#26262e', 14); }
function remote(g, x, y) { g.save(); g.translate(x, y); g.rotate(-.4); shape(g, q => rrPath(q, -12, -50, 24, 70, 8), '#2a2a32', 4); circ(g, 0, -34, 5, '#e25555', 0); g.restore(); }
function partyHat(g, x, y, s) { g.save(); g.translate(x, y); g.scale(s, s); shape(g, q => { q.moveTo(-40, 0); q.lineTo(0, -110); q.lineTo(40, 0); q.closePath(); }, '#6fb3e0', 5); g.strokeStyle = '#fde047'; g.lineWidth = 8; for (const k of [.3, .62]) { g.beginPath(); g.moveTo(-40 * (1 - k), -110 * k); g.lineTo(40 * (1 - k), -110 * k); g.stroke(); } circ(g, 0, -114, 12, '#e07a8a', 4); g.restore(); }
function smoke(g, x, y, k, t) { g.save(); g.strokeStyle = 'rgba(160,160,170,.75)'; g.lineWidth = 6; g.lineCap = 'round'; for (let i = -2; i <= 2; i++) { g.beginPath(); for (let j = 0; j < 8; j++) { const yy = y - j * 14 * k, xx = x + i * 30 + Math.sin(j * .9 + i + t * 2) * 8; j ? g.lineTo(xx, yy) : g.moveTo(xx, yy); } g.stroke(); } g.restore(); }
function guestClap(wt, seed, G) { const u = Math.abs(Math.sin(wt * Math.PI * 2.2 + seed)); return POSE.clap(u, G); }

/* ================================================================ 11. you age: the extra hours, the gray hair */
SC.s11 = (X, t) => {
  const mirror = Lt('s11_06') - .1;
  if (t < mirror) {
    const cam = shots(t, [{ t: 0, cx: 960, cy: 560, z: 1.25, z2: 1.32 }]);
    const st = stage(cam); st.wld(g => { drawSet(g, 'bedroom'); bedBack(g); bedFront(g); nightstand(g); propAlarm(g, 1075, 700, .7, 6, 59, 0); drawCat(g, 1650, 1010, .7, { flip: -1 }); });
    const hp = { x: 1300, y: FEET + 40, s: S0, t, look: [0, 0], mouth: -.1, brow: .3 };
    if (t > Lt('s11_04')) { hp.wide = .3; hp.mouth = -.3; } if (t > Lt('s11_05')) { hp.sweat = 1; hp.mouth = -.5; }
    st.col(g => drawChar(g, 'tu', hp));
    compose2(X, st, { amt: 1 });
    if (t > Lt('s11_02') - .1 && t < Lt('s11_04') - .1) { const a = R(t, Lt('s11_02') - .1, Lt('s11_02') + .25, outC); X.save(); X.globalAlpha = a * .55; X.fillStyle = '#0d0b12'; X.fillRect(0, 0, W, H); X.restore(); X.save(); X.globalAlpha = a;
      clockFace(X, 560, 440, 190, 'EL MUNDO', .58, true); clockFace(X, 1360, 440, 190, 'TÚ', (t - Lt('s11_02')) * 1.4, false); X.restore();
      const items = [['SIESTA: +8 HORAS', .05], ['ESTUDIO: +3 HORAS', .36], ['PENAL: +20 MIN', .64]];
      items.forEach(([s, f], i) => sticker(X, s, R(t, Lm('s11_03', f), Lm('s11_03', f) + .25, outC), 90, 690 + i * 120, 58)); }
    if (t > Lt('s11_04') - .1 && t < Lt('s11_05')) { const n = Math.round(312 * R(t, Lt('s11_04'), Le('s11_04') - .2, outC)); bigCounter(X, 'HORAS EXTRA:', String(n), R(t, Lt('s11_04') - .1, Lt('s11_04') + .2, outC), 560, 760); }
    if (t > Lt('s11_05') - .1) calendarCard(X, R(t, Lt('s11_05') - .1, Lt('s11_05') + .3, outC), t);
    return;
  }
  const hairPt = [978, 196];
  const cam = shots(t, [{ t: mirror, cx: 960, cy: 470, z: 1.2, z2: 1.3 }, { t: Lt('s11_07') - .05, cx: hairPt[0], cy: hairPt[1] + 40, z: 3.6, z2: 3.9, shake: 1 }, { t: Lt('s11_08') - .05, cx: 960, cy: 330, z: 2.0, z2: 2.1 }]);
  const st = stage(cam); st.wld(g => drawSet(g, 'bathroom'));
  st.wld(g => { g.save(); g.beginPath(); g.rect(710, 100, 500, 430); g.clip(); mirrorGlass(g);
    const rp = { x: 960, y: 845, s: .95, t, look: [0, 0], mouth: .2, grayHair: 1 };
    if (t > Lt('s11_07') - .05) { rp.wide = .6; rp.look = [4, -10]; rp.mouth = -.2; } if (t > Lt('s11_08') - .05) { rp.wide = 1; rp.open = .8; rp.look = [0, 0]; rp.hL = [-70, -700]; rp.hR = [70, -700]; rp.armsFront = 1; }
    drawChar(g, 'tu', rp); g.restore(); });
  compose2(X, st, { amt: 0 });
  if (t > Lt('s11_07') - .05 && t < Lt('s11_08') - .05) { X.save(); X.globalAlpha = .5 * bump(t, Lt('s11_07') - .05, Lt('s11_07') + .4); X.fillStyle = '#ffffff'; X.fillRect(0, 0, W, H); X.restore(); }
  if (t > Lt('s11_08')) sticker(X, '16 AÑOS', R(t, Lt('s11_08'), Lt('s11_08') + .25, outC), 70, 60, 90);
};

/* ================================================================ 12. nothing works while time is stopped */
SC.s12 = (X, t) => {
  const tPhone = Lt('s12_02') - .1, tTap = Lt('s12_03') - .1, tTv = Lt('s12_04') - .1;
  if (t >= tTap && t < tTv) { // bathroom faucet: water stuck as an icicle
    const cam = shots(t, [{ t: tTap, cx: 1020, cy: 610, z: 3.1, z2: 3.3 }]);
    const st = stage(cam); st.wld(g => { drawSet(g, 'bathroom'); shape(g, q => { q.moveTo(1048, 600); q.quadraticCurveTo(1060, 640, 1052, 690); q.quadraticCurveTo(1046, 700, 1040, 690); q.quadraticCurveTo(1034, 640, 1048, 600); }, '#9fd3ff', 4); });
    st.col(g => { const k = R(t, tTap + .2, tTap + .6), y = 560; tube(g, [[1180, 760], [1100, 640], [1000, 560]], '#bf8a24', 34); mitten(g, 1000 + 6 * Math.sin(t * 10) * k, y, 22); });
    compose2(X, st, { amt: 1 }); return; }
  const cam = shots(t, [{ t: 0, cx: 960, cy: 560, z: 1.15 }, { t: tPhone, cx: 1180, cy: 560, z: 2.4, z2: 2.5 }, { t: tTv, cx: 1280, cy: 620, z: 1.25 }, { t: Lt('s12_05') - .1, cx: 960, cy: 560, z: 1.0 }]);
  const st = stage(cam); st.wld(g => { drawSet(g, 'bedroom'); bedBack(g); nightstand(g); propAlarm(g, 1075, 700, .7, 6, 59, 0); tv(g, 1710, 520, 0, t > tTv + .7); });
  let hp;
  if (t < tTv) { hp = { x: 1180, y: FEET + 40, s: S0, t, look: [0, 12], mouth: -.3, slump: R(t, Lt('s12_01') + .5, Lt('s12_01') + 1.2), brow: .4 };
    if (t > tPhone - .1) { hp.hR = [20, -380]; hp.look = [6, 16]; hp.holdR = (g, x, y) => { propPhone(g, x - 4, y - 50, .8, 3, -.1); line(g, [[x - 4, y + 10], [x + 30, y + 120], [x + 200, y + 160]], '#e8e4ee', 6); }; } }
  else { hp = { x: 600, y: 945, s: S0, t, look: [18, -4], mouth: -.2, brow: .6, hR: [190, -440], holdR: (g, x, y) => remote(g, x, y - 20) };
    if (t > tTv + .7) { hp.hR = [190 + Math.sin(t * 20) * 6, -440]; hp.mouth = -.5; }
    if (t > Lt('s12_05') - .1) { hp.slump = 1; hp.rot = .15; hp.blink = 1; hp.mouth = -.6; hp.hR = null; hp.holdR = null; } }
  if (t >= tTv) { st.col(g => drawChar(g, 'tu', hp)); st.wld(g => bedFront(g, .6)); } else { st.wld(g => bedFront(g)); st.col(g => drawChar(g, 'tu', hp)); }
  compose2(X, st, { amt: 1 });
  if (t > Lt('s12_05')) { const a = R(t, Lt('s12_05'), Lt('s12_05') + .35, outC); X.save(); X.globalAlpha = a * .85; X.fillStyle = '#ffffff'; X.strokeStyle = OUT; X.lineWidth = 10; for (const dx of [-110, 40]) { X.beginPath(); rrPath(X, W / 2 + dx, H / 2 - 170, 70, 340, 12); X.fill(); X.stroke(); } X.restore(); }
};

/* ================================================================ 13. the birthday applause */
SC.s13 = (X, t) => {
  const blow = Lm('s13_03', .45), clapOn = Lm('s13_03', .72);
  const strobe = []; for (let k = Le('s13_11') + .12; k < Le('s13_11') + 1.25; k += .14) strobe.push({ t: k }); if (strobe.length % 2) strobe.pop();
  const claps = [{ t: Lt('s13_05') + .2 }, { t: Lm('s13_07', .15) }, { t: Lm('s13_07', .6) }, { t: Lm('s13_07', .85) }, { t: Lt('s13_08') }, { t: Lt('s13_09') }, { t: Lt('s13_10') }, { t: Lt('s13_11') }, ...strobe];
  const wt = worldClock(t, claps), fz = isFrozen(t, claps), after = Lt('s13_12') - .1;
  const cam = shots(t, [
    { t: 0, cx: 960, cy: 560, z: 1.05 },
    { t: Lt('s13_02') - .05, cx: 960, cy: 520, z: 1.8, z2: 1.9 },
    { t: Lt('s13_03') - .05, cx: 960, cy: 560, z: 1.2 },
    { t: Lt('s13_04') - .05, cx: 1380, cy: 560, z: 1.6 },
    { t: Lt('s13_06') - .05, cx: 960, cy: 560, z: 1.05, z2: 1.1 },
    { t: Lt('s13_08') - .05, cx: 1200, cy: 560, z: 1.35 },
    { t: after, cx: 1180, cy: 600, z: 1.3, z2: 1.36 },
    { t: Lt('s13_14') - .2, cx: 1500, cy: 640, z: 1.4 },
  ]);
  const st = stage(cam); st.wld(g => drawSet(g, 'party'));
  const W0 = { still: fz, t: wt, blink: fz ? 0 : null };
  const singing = wt < blow, clapping = wt > clapOn && t < after;
  const guests = [['ex1', 560, 1], ['ex4', 740, 2], ['ex5', 1180, 3], ['ex2', 1340, 4]];
  guests.forEach(([n, x, sd]) => { const p = { ...W0, x, y: FEET, s: S0, look: [x < 960 ? 12 : -12, 6], mouth: .6 }; const G = charGeom(CAST[n], p);
    if (singing) { p.open = .3 + .3 * Math.abs(Math.sin(wt * 6 + sd)); p.rot = Math.sin(wt * 3 + sd) * .05; }
    if (clapping || (fz && t < after && t > clapOn)) { [p.hL, p.hR] = guestClap(wt, sd, G); p.armsFront = 1; p.open = .5; p.blink = fz ? 0 : (p.blink ?? null); }
    if (t > after) { p.open = Math.abs(Math.sin(t * 4 + sd)) * .4; p.mouth = .8; p.look = [Math.sin(t + sd) * 14, 0]; p.still = 0; p.t = t; }
    st.wld(g => drawChar(g, n, p)); });
  const np = { ...W0, x: 960, y: FEET, s: S0, marker: 1, look: [0, 8], mouth: .8 };
  if (wt > blow - .3 && wt < blow + .6) { np.open = .7; np.lean = .08; np.look = [0, 18]; np.hy = 14; }
  if (clapping || (fz && t > clapOn && t < after)) { const G = charGeom(CAST.nacho, np); [np.hL, np.hR] = guestClap(wt, 0, G); np.armsFront = 1; np.mouth = 1; }
  if (t > after) { np.still = 0; np.t = t; np.mouth = 1; np.holdR = (g, x, y) => { shape(g, q => { q.moveTo(x - 30, y - 10); q.lineTo(x + 30, y - 10); q.lineTo(x, y - 60); q.closePath(); }, '#f6c6d4', 4); }; np.hR = [80, -360]; }
  st.wld(g => { drawChar(g, 'nacho', np); const S = S0 * CAST.nacho.s, hy = FEET + S * (charGeom(CAST.nacho, np).top - 100 + (np.hy || 0)); partyHat(g, 960 + (np.lean || 0) * 200, hy - CAST.nacho.r * S * .95, .8); });
  // hero on the right
  let hp = { x: 1520, y: FEET, s: S0, t, look: [-14, 4], mouth: .7 };
  const G = charGeom(CAST.tu, hp);
  if (t > Lt('s13_04') - .2 && t < after) { hp.armsFront = 1; let near = null; for (const c of claps) if (Math.abs(t - c.t) < .2) near = c;
    if (near) [hp.hL, hp.hR] = clapHands(t, near.t, G, .05); else [hp.hL, hp.hR] = POSE.clap(Math.abs(Math.sin(t * Math.PI * 2.2)), G);
    hp.mouth = t > Lt('s13_07') ? -.3 : .6; hp.wide = t > Lt('s13_07') ? .5 : 0; hp.sweat = t > Lt('s13_08') ? 1 : 0; }
  if (t > after) { hp.slump = 1; hp.lid = .6; hp.mouth = -.4; hp.sweat = 1; hp.look = [0, 10]; }
  if (t > Lt('s13_14') - .2) { hp = { x: 1580, y: FEET - 30, s: S0, t, sit: 1, hL: [-40, -110], hR: [40, -110], armsFront: 0, look: [-10, 0], mouth: .1, brow: .5 }; }
  st.col(g => drawChar(g, 'tu', hp));
  st.wld(g => { partyTable(g); propCake(g, 960, 760, .8, 1, wt, wt < blow); if (wt > blow && t < after) smoke(g, 960, 640, .55 * R(wt, blow, blow + 1.2), fz ? 0 : wt); });
  const cp = worldToScreen(cam, ...clapPoint('tu', hp));
  compose2(X, st, freezeState(t, claps.map(c => ({ t: c.t, x: cp[0], y: cp[1], screen: 1 })), cam));
  if (t > Lt('s13_13') - .05 && t < Lt('s13_14') - .2) bigCounter(X, 'APLAUSO:', '40 MINUTOS', R(t, Lt('s13_13') - .05, Lt('s13_13') + .25, outC), 70, 60);
  ruleCard(X, 2, 'EN LAS FIESTAS,', 'TE SIENTAS SOBRE TUS MANOS', R(t, Lt('s13_14') - .1, Lt('s13_14') + .25, outC));
};

/* ================================================================ 14. talking to Pepe */
SC.s14 = (X, t) => {
  const sitT = Lt('s14_03') + .2;
  const cam = shots(t, [
    { t: 0, cx: 960, cy: 560, z: 1.0 },
    { t: Lt('s14_02') + .8, cx: 1450, cy: 520, z: 1.5 },
    { t: sitT - .1, cx: 960, cy: 600, z: 1.3, z2: 1.36 },
    { t: Lt('s14_06') - .05, cx: 1060, cy: 760, z: 3.0, z2: 3.15 },
    { t: Lt('s14_07') - .05, cx: 960, cy: 620, z: 1.45, z2: 1.55 },
  ]);
  const st = stage(cam); st.wld(g => { drawSet(g, 'park'); bench(g, 0); });
  st.wld(g => drawChar(g, 'ex3', { x: 1560, y: 900, s: .7, still: 1, walk: 1, phase: .8, jump: 20, mouth: .3, look: [-10, 0], hL: [-150, -380], hR: [140, -330] }));
  let hp;
  if (t < sitT) { const hx = t < Lt('s14_02') + .8 ? mix(150, 1380, R(t, 0, Lt('s14_02') + .6, lin)) : 1380; hp = { x: hx, y: 930, s: S0, t, walk: t < Lt('s14_02') + .6 ? 1 : 0, phase: walkPh(hx), look: [12, 0], mouth: -.1 };
    if (t > Lt('s14_02') + .8) { hp.hR = [160 + Math.sin(t * 14) * 20, -560]; hp.look = [16, -4]; hp.mouth = -.3; }
    if (t > Lt('s14_03') - .3) { hp.x = mix(1380, 880, R(t, Lt('s14_03') - .3, sitT, lin)); hp.walk = 1; hp.phase = walkPh(hp.x); hp.flip = -1; } }
  else { hp = { x: 880, y: 905, s: S0, t, sit: 1, look: [16, 6], open: talk(t, 's14_03') * 0 };
    const talking = (t > sitT && t < Lt('s14_06') - .1) || t > Lt('s14_07') + .6; if (talking) hp.open = .25 + .35 * Math.abs(Math.sin(t * 11)) * Math.abs(Math.sin(t * 2.3));
    if (t > Lt('s14_05') - .1 && t < Lt('s14_06')) { hp.hR = [120 + Math.sin(t * 5) * 40, -380 + Math.cos(t * 4) * 40]; }
    if (t > Lt('s14_07') - .05) { hp.hR = [210, -330]; hp.mouth = .9; hp.blush = .4; hp.open = 0; } }
  st.col(g => drawChar(g, 'tu', hp));
  st.wld(g => { bench(g, 1); drawPigeon(g, 1060, 792, .62, { flip: -1 }); });
  compose2(X, st, { amt: 1 });
  if (t > Lt('s14_04') - .05 && t < Lt('s14_05') + .2) { const a = R(t, Lt('s14_04') - .05, Lt('s14_04') + .25, outC), [px, py] = worldToScreen(cam, 1030, 690); sticker(X, 'PEPE', a, px - 40, py - 260, 90); X.save(); X.globalAlpha = a; line(X, [[px + 30, py - 120], [px + 20, py - 40]], OUT, 10); line(X, [[px + 30, py - 120], [px + 20, py - 40]], '#fde047', 5); X.restore(); }
  if (t > Lt('s14_05') - .05 && t < Lt('s14_06') - .05) { const [bx, by] = worldToScreen(cam, 820, 380); const icons = ['♥', 'CANA', '10/10'];
    icons.forEach((s, i) => { const f = R(t, Lm('s14_05', i * .3), Lm('s14_05', i * .3) + .25, outC); bubble(X, s, bx - 220 + i * 230, by - 40 * (i % 2), f, 60); }); }
  if (t > Lt('s14_07')) sticker(X, 'SEMANA 3', R(t, Lt('s14_07'), Lt('s14_07') + .25, outC), 70, 60, 80);
};

/* ================================================================ 15. the flowerpot */
SC.s15 = (X, t) => {
  const tc = Lt('s15_03') + .1, tr = Lm('s15_07', .55), claps = [{ t: tc }, { t: tr }], wt = worldClock(t, claps), fz = isFrozen(t, claps);
  const fall0 = tc - 1.76, grab = Lm('s15_05', .15), headPot = Lm('s15_06', .8);
  const cam = shots(t, [
    { t: 0, cx: 900, cy: 560, z: 1.0 },
    { t: Lt('s15_02') - .1, cx: 1380, cy: 330, z: 1.45 },
    { t: tc + .4, cx: 1140, cy: 520, z: 1.25 },
    { t: Lt('s15_06') - .05, cx: 1300, cy: 500, z: 1.7, z2: 1.8 },
    { t: tr - .6, cx: 1300, cy: 520, z: 1.45 },
    { t: Lt('s15_08') - .1, cx: 1340, cy: 470, z: 1.9, z2: 2.0 },
  ]);
  const st = stage(cam); st.wld(g => drawSet(g, 'street'));
  // Valeria walks under the balcony reading her phone
  const vx = mix(500, 1400, R(wt, .3, Lm('s15_01', .8), lin)), vp = { x: vx, y: FEET, s: S0, t: wt, still: fz, blink: fz ? 0 : null, walk: wt < Lm('s15_01', .8) ? 1 : 0, phase: walkPh(vx), look: [4, 18], mouth: .1, hR: [20, -380], holdR: (g, x, y) => propPhone(g, x, y - 40, .55, 76, -.1) };
  if (fz && t > grab + .4) vp.look = [-3, 16];               // clue: she glances at the hero
  if (t > tr + .3) { vp.look = [-18, 0]; vp.hR = [30, -300]; vp.lid = .25; vp.mouth = .5; vp.brow = .4; vp.open = talk(t, 's15_08'); if (t > Lt('s15_09')) { vp.mouth = .9; vp.open = 0; vp.lid = .4; } }
  st.wld(g => drawChar(g, 'valeria', vp));
  // the pot: wobbles on the rail, falls, stops half a meter above her head
  const potY = t < fall0 ? 39 : Math.min(349, 39 + .5 * 200 * Math.pow(Math.max(0, wt - worldClock(fall0, claps)), 2));
  const wob = t < fall0 && wt > Lm('s15_01', .6) ? Math.sin(wt * 18) * .12 * R(wt, Lm('s15_01', .6), fall0) : 0;
  const potHeld = t > grab;
  if (!potHeld) st.wld(g => { propPot(g, 1400, potY, .7, wob); if (t > fall0 && t < tc) for (let i = 0; i < 3; i++) line(g, [[1360 + i * 40, potY - 110], [1360 + i * 40, potY - 170]], 'rgba(255,255,255,.8)', 5); });
  // hero
  let hp = { x: 300, y: FEET, s: S0, t, look: [16, -4], mouth: .4, blush: .5 };
  if (t < tc - .3 && t > 1.2) hp.hR = [150 + Math.sin(t * 10) * 18, -600];
  if (t > Lt('s15_02') - .1 && t < tc - .3) { hp.wide = .8; hp.open = .6; hp.blush = 0; hp.hR = null; }
  if (t > tc - .4 && t < tc + .4) { const G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = clapHands(t, tc, G, .15); hp.armsFront = 1; }
  if (t > tc + .4 && t < grab) { hp.x = mix(300, 1270, R(t, tc + .4, grab - .2, lin)); hp.walk = 1; hp.phase = walkPh(hp.x) * 1.8; hp.lean = .1; hp.mouth = -.2; hp.blush = 0; }
  if (t >= grab - .2 && t < grab + .5) { hp.x = 1270; hp.jump = 170 * bump(t, grab - .2, grab + .45); hp.hR = [(1400 - 1270) / S0, (potY - 10 - FEET) / S0 + hp.jump]; hp.look = [14, -20]; hp.blush = 0;
    if (t > grab) hp.holdR = (g, x, y) => propPot(g, x, y + 20, .7, 0); }
  if (t >= grab + .5) { hp.x = 1270; hp.hL = [-40, -330]; hp.hR = [40, -330]; hp.armsFront = 1; hp.holdR = (g, x, y) => propPot(g, x - 40, y + 30, .7, 0); hp.look = [14, 4]; hp.mouth = .2; hp.blush = 0;
    if (t > Lt('s15_06') + .3) { hp.look = [Math.sin((t - Lt('s15_06')) * 2.4) * 18, 0]; hp.sweat = 1; hp.mouth = -.4; hp.wide = .3; }
    if (t > headPot) { hp.hL = [-60, -690]; hp.hR = [60, -690]; hp.holdR = null; hp.potOnHead = 1; hp.look = [0, -12]; hp.mouth = .3; }
    if (t > tr - .45 && t < tr + .4) { const G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = clapHands(t, tr, G, .1); }
    if (t > tr + .4) { hp.look = [16, 0]; hp.mouth = -.3; hp.sweat = 1; hp.hL = null; hp.hR = null; }
    if (t > Lt('s15_09') - .05) { hp.open = talk(t, 's15_09'); hp.hR = [130, -560]; hp.mouth = .3; } }
  st.col(g => { if (hp.potOnHead) { const G = charGeom(CAST.tu, { ...hp, t }), yc = FEET + S0 * (G.top - 100 + (hp.hy || 0)); drawChar(g, 'tu', hp); propPot(g, hp.x, yc - CAST.tu.r * S0 * 1.02 - 21, .7, 0); } else drawChar(g, 'tu', hp); });
  const cp = worldToScreen(cam, ...clapPoint('tu', hp));
  compose2(X, st, freezeState(t, [{ t: tc, x: cp[0], y: cp[1], screen: 1 }, { t: tr, x: cp[0], y: cp[1], screen: 1 }], cam));
  if (t > Lt('s15_06') + .4 && t < headPot) { const [bx, by] = worldToScreen(cam, 1180, 300); bubble(X, '¿Y AHORA?', bx, by, R(t, Lt('s15_06') + .4, Lt('s15_06') + .7, outC), 54); }
};

/* ================================================================ 16. the twist: Valeria moves */
let FLASH = false;
SC.s16 = (X, t) => {
  const tc = Lm('s16_01', .3), claps = [{ t: tc }], fz = isFrozen(t, claps), flash = Lt('s16_08') - .15;
  if (t > flash) { // flashback to the books, now with Valeria's eyes following the hero
    const sid = SID, u = R(t, flash, T().dur - .2, lin); SID = 's09'; FLASH = true; const t9 = mix(TIM.scenes.s09.L.s09_03[0] + .5, TIM.scenes.s09.L.s09_03[0] + TIM.scenes.s09.L.s09_03[1] * .97, u);
    SC.s09(X, t9); FLASH = false; SID = sid;
    X.save(); X.globalCompositeOperation = 'multiply'; X.fillStyle = 'rgba(255,225,180,1)'; X.fillRect(0, 0, W, H); X.restore();
    X.save(); X.globalAlpha = .12; X.fillStyle = '#000'; for (let y = (t * 60) % 6; y < H; y += 6) X.fillRect(0, y, W, 2); X.restore();
    sticker(X, 'FLASHBACK', 1, 70, 60, 70, '#ffffff');
    return; }
  const walkEnd = Lt('s16_02') + .3;
  const cam = shots(t, [
    { t: 0, cx: tt => mix(120, 760, R(tt, 0, walkEnd, lin)), cy: 540, z: 1.8 },
    { t: Lt('s16_02') - .05, cx: 960, cy: 560, z: 1.0, z2: 1.06 },
    { t: Lt('s16_03') - .05, cx: 1240, cy: 820, z: 2.6, z2: 2.7 },
    { t: Lm('s16_03', .8), cx: 1180, cy: 620, z: 1.6 },
    { t: Lt('s16_05') - .05, cx: 900, cy: 560, z: 1.7 },
    { t: Lt('s16_06') - .05, cx: 1180, cy: 560, z: 1.8, z2: 1.9 },
    { t: Lt('s16_07') - .05, cx: 1000, cy: 600, z: 1.2, z2: 1.26 },
  ]);
  const st = stage(cam); st.wld(g => { drawSet(g, 'parkNight'); bench(g, 0); });
  // Valeria on the bench, in color: swings her foot, then turns to the hero
  const vp = { x: 1240, y: 905, s: S0, t, sit: 1, look: [10, -6], mouth: .2, hL: [-40, -300], hR: [40, -300], armsFront: 1, tailSwing: Math.sin(t * 2) * .08 };
  vp.lean = Math.sin(t * 1.4) * .02; vp.footSwing = Math.sin(t * 4.2) * 34;
  if (t > Lm('s16_03', .5)) { vp.look = [-18, 0]; vp.mouth = .6; vp.lid = .2; }
  if (t > Lt('s16_04') - .05) { vp.open = talk(t, 's16_04') + talk(t, 's16_06'); vp.lid = .3; vp.mouth = .7; vp.brow = .3; }
  if (t > Lm('s16_04', .7) && t < Le('s16_04') + .5) { vp.hR = [120, -470]; vp.holdR = (g, x, y) => { const k = bump(t, Lm('s16_04', .9), Lm('s16_04', .9) + .3); if (k > 0) { g.save(); g.strokeStyle = '#fde047'; g.lineWidth = 5; for (let i = 0; i < 8; i++) { const a = i * Math.PI / 4; g.beginPath(); g.moveTo(x + Math.cos(a) * 26, y - 20 + Math.sin(a) * 26); g.lineTo(x + Math.cos(a) * (26 + 30 * k), y - 20 + Math.sin(a) * (26 + 30 * k)); g.stroke(); } g.restore(); } }; }
  st.col(g => drawChar(g, 'valeria', vp));
  // hero arrives
  let hp;
  if (t < walkEnd) { const hx = mix(120, 760, R(t, 0, walkEnd, lin)); hp = { x: hx, y: 930, s: S0, t, walk: 1, phase: walkPh(hx), look: [14, 0], mouth: .3 };
    if (t > tc - .4 && t < tc + .4) { const G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = clapHands(t, tc, G, .15); hp.armsFront = 1; } if (t > Lt('s16_02')) { hp.walk = 0; hp.x = 760; hp.wide = .5; } }
  else { hp = { x: 760, y: 930, s: S0, t, look: [16, 0], mouth: -.2, wide: .6 }; if (t > Lt('s16_05') - .05) { hp.open = talk(t, 's16_05'); hp.hR = [160, -420]; }
    if (t > Lt('s16_06')) { hp.wide = 1; hp.open = t > Lm('s16_06', .8) ? .6 : 0; hp.hR = null; }
    if (t > Lt('s16_07') - .05) { hp = { x: 900, y: 905, s: S0, t, sit: 1, look: [16, 0], wide: .8, mouth: -.2, hL: [-40, -300], hR: [40, -300], armsFront: 1 }; } }
  st.col(g => drawChar(g, 'tu', hp));
  st.wld(g => { bench(g, 1); drawPigeon(g, 1080, 792, .62, { flip: -1 }); });
  const cp = worldToScreen(cam, ...clapPoint('tu', hp));
  compose2(X, st, freezeState(t, [{ t: tc, x: cp[0], y: cp[1], screen: 1 }], cam));
  if (t > Lm('s16_06', .75)) sticker(X, '19 AÑOS', R(t, Lm('s16_06', .75), Lm('s16_06', .75) + .25, outC), 70, 60, 90);
};

/* ================================================================ 17. outro: Pepe wants to know */
SC.s17 = (X, t) => {
  const end = Le('s17_04') + .9, pepeAlive = Lm('s17_04', .55);
  const cam = shots(t, [{ t: 0, cx: 1000, cy: 600, z: 1.2, z2: 1.5 }, { t: Lt('s17_04') - .1, cx: 1080, cy: 740, z: 3.0, z2: 3.2 }]);
  const st = stage(cam); st.wld(g => { drawSet(g, 'parkNight'); bench(g, 0); });
  st.col(g => { drawChar(g, 'valeria', { x: 1240, y: 905, s: S0, t, sit: 1, look: [-14, 4], mouth: .6, hL: [-40, -300], hR: [40, -300], armsFront: 1 });
    drawChar(g, 'tu', { x: 900, y: 905, s: S0, t, sit: 1, look: [14, 4], mouth: .4, blush: .5, hL: [-40, -300], hR: [40, -300], armsFront: 1 }); });
  st.wld(g => bench(g, 1));
  if (t < pepeAlive) st.wld(g => drawPigeon(g, 1080, 792, .62, { flip: -1 }));
  else st.col(g => drawPigeon(g, 1080, 792, .62, { flip: -1, tilt: -.5 * R(t, pepeAlive, pepeAlive + .25), blink: blinkAt(t, [pepeAlive + .45, pepeAlive + 1.1]) }));
  compose2(X, st, { amt: 1 });
  if (t > Lt('s17_02') - .05 && t < Lt('s17_04') - .1) sticker(X, '¿QUÉ HARÍAS TÚ?', R(t, Lt('s17_02') - .05, Lt('s17_02') + .25, outC), 70, 60, 70);
  if (t > Lm('s17_03', .7) && t < Lt('s17_04') - .1) { const a = R(t, Lm('s17_03', .7), Lm('s17_03', .7) + .3, back); X.save(); X.translate(W / 2, H - 200); X.scale(a, a); shape(X, q => rrPath(q, -260, -60, 520, 120, 20), '#e02424', 6); text(X, 'SUSCRÍBETE', 0, 26, 76, '#ffffff', 'Bangers', 'center'); X.restore(); }
  if (t > end) { const a = R(t, end, end + .5, outC); X.save(); X.globalAlpha = a; X.fillStyle = '#141a2e'; X.fillRect(0, 0, W, H);
    text(X, CHANNEL_NAME, W / 2, 230, 150, '#fde047', 'Bangers', 'center', OUT, 18);
    text(X, 'PRÓXIMO EPISODIO:', W / 2, 400, 64, '#ffffff', 'Bangers', 'center');
    text(X, '¿Y SI PUDIERAS VER QUIÉN', W / 2, 500, 84, '#ffffff', 'Bangers', 'center', OUT, 10); text(X, 'ESTÁ ENAMORADO DE TI?', W / 2, 600, 84, '#ffffff', 'Bangers', 'center', OUT, 10);
    shape(X, q => rrPath(q, W / 2 - 300, 720, 600, 130, 22), '#e02424', 7); text(X, 'SUSCRÍBETE', W / 2, 812, 84, '#ffffff', 'Bangers', 'center');
    drawPigeon(X, 1600, 960, .9, { flip: -1, blink: autoBlink(t, 3) }); X.restore(); }
};
