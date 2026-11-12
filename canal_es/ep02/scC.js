/* Ep02 scenes 12–18: five seconds ahead of everyone, Pepe has no future, the hallway, the question, eyes closed, Pepe's ghost,
   the science, the call to action. */
const CHANNEL_NAME = 'PONLE QUE…';
function dog(g, x, y, s, ph = 0, flip = 1) { g.save(); g.translate(x, y); g.scale(s * flip, s);
  for (const [dx, o] of [[-50, 0], [-30, Math.PI], [40, Math.PI], [60, 0]]) tube(g, [[dx, -40], [dx + Math.sin(ph + o) * 14, 0]], '#c98a4a', 16);
  ell(g, 0, -60, 80, 36, 0, '#d99a58'); line(g, [[-78, -70], [-110, -100 + Math.sin(ph * 2) * 10]], OUT, 14); line(g, [[-78, -70], [-110, -100 + Math.sin(ph * 2) * 10]], '#d99a58', 8);
  g.save(); g.translate(78, -96); ell(g, 0, 0, 40, 34, 0, '#d99a58'); ell(g, 34, 10, 22, 16, 0, '#d99a58'); circ(g, 52, 4, 7, OUT, 0); circ(g, 8, -8, 5, OUT, 0);
  ell(g, -18, -10, 14, 28, .4, '#8a5a2b'); g.restore(); g.restore(); }
function leaf(g, x, y, r, c = '#e0913a') { g.save(); g.translate(x, y); g.rotate(r); shape(g, q => { q.moveTo(-18, 0); q.quadraticCurveTo(0, -14, 18, 0); q.quadraticCurveTo(0, 14, -18, 0); }, c, 3); g.restore(); }
/* sitting on the park bench, seen from the front: the whole bench is drawn behind the sitter, hips on the seat, short
   (foreshortened) legs dangling in front of it with the feet off the ground (no floor shadow), hands resting on the thighs */
function benchSit(x, extra = {}) { return Object.assign({ x, y: 905, s: S0, sit: 1, noShadow: 1, hL: [-80, -125], hR: [80, -125], armsFront: 1 }, extra); }
function dashRing(g, x, y, r, t, col = '#fde047') { g.save(); g.strokeStyle = col; g.lineWidth = 8; g.setLineDash([22, 16]); g.lineDashOffset = -t * 60; g.beginPath(); g.arc(x, y, r, 0, 7); g.stroke(); g.restore(); }

/* ================================================================ 12. five seconds ahead of everyone; Pepe has no ghost */
SC.s12 = (X, t) => {
  const bench0 = Lt('s12_06') - .05;
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 560, z: 1.05, z2: 1.1, lock: 1 },
    { t: Lt('s12_03') - .05, cx: 960, cy: 500, z: 1.45, lock: 1 },
    { t: Lt('s12_05') - .05, cx: 960, cy: 560, z: 1.0, z2: 1.15, lock: 1 },
    { t: bench0, cx: 960, cy: 600, z: 1.1, z2: 1.15, lock: 1 },
    { t: Lt('s12_08') - .05, cx: 960, cy: 540, z: 1.0, lock: 1 },
    { t: Lt('s12_09') - .05, cx: 1080, cy: 720, z: 2.4, z2: 2.6, lock: 1 },
    { t: Lt('s12_12') - .05, cx: 990, cy: 640, z: 1.9, z2: 2.0, lock: 1 },
    { t: Lt('s12_13') - .05, cx: 1080, cy: 740, z: 3.0, z2: 3.2, lock: 1 },
  ]);
  const st = stageF(cam); let ga = 0;
  if (t < bench0) {
    st.wld(g => drawSet(g, 'park'));
    st.col(g => drawPigeon(g, 1700, 900, .42, { flip: -1, peck: Math.max(0, Math.sin(t * 2)) * .7 }));
    const laugh = Lt('s12_03') + .2, scare = Lt('s12_04') + .2, lag = 1.4;
    const crowd = [['nacho', 1250, -1], ['ex2', 1450, -1], ['ex4', 1650, -1]];
    for (const [n, x, f] of crowd) { const p = { x, y: FEET, s: S0, t, flip: f, look: [-12, 0], mouth: .2 };
      if (t > laugh + lag && t < laugh + lag + 1.4) { p.mouth = 1; p.blink = 1; p.rot = Math.sin(t * 14) * .05; }
      if (t > scare + lag && t < scare + lag + 1.2) { p.wide = 1; p.open = .8; p.jump = 40 * bump(t, scare + lag, scare + lag + .5); }
      if (t > Lt('s12_05')) { p.look = [-6, 0]; p.mouth = .5; p.flip = 1; p.x = x + 60; }
      st.wld(g => drawChar(g, n, p)); }
    const hp = { x: 800, y: FEET, s: S0, t, look: [14, 0], mouth: .2 };
    if (t > laugh && t < laugh + 1.4) { hp.mouth = 1; hp.blink = 1; hp.rot = Math.sin(t * 14) * .05; }
    if (t > laugh + lag && t < Lt('s12_04')) { hp.mouth = -.1; hp.brow = .3; }
    if (t > scare && t < scare + 1.2) { hp.wide = 1; hp.open = .8; hp.jump = 40 * bump(t, scare, scare + .5); }
    if (t > scare + lag) { hp.mouth = -.2; hp.brow = .4; }
    if (t > Lt('s12_05')) { hp.x = mix(800, 520, R(t, Lt('s12_05'), Le('s12_05'), io)); hp.look = [-14, 4]; hp.mouth = -.25; hp.brow = .5; hp.flip = -1; hp.walk = t < Le('s12_05') ? 1 : 0; hp.phase = walkPh(hp.x); }
    st.col(g => drawChar(g, 'tu', hp));
    if (t > Lt('s12_02') - .1 && t < Lt('s12_05')) sticker(X, '', 0);
    composeF(X, st, { ghost: 0, t });
    if (t > Lt('s12_02') && t < Lt('s12_05')) sticker(X, 'TÚ: +5 s', R(t, Lt('s12_02'), Lt('s12_02') + .25, back), ...worldToScreen(cam, 700, 300), 60, '#5ee7ff');
    if (t > laugh && t < laugh + 1.2) comicWord(X, '¡JA!', ...worldToScreen(cam, 800, 320), t - laugh, 70);
    if (t > laugh + lag && t < laugh + lag + 1.2) comicWord(X, '¡JAJAJA!', ...worldToScreen(cam, 1450, 300), t - laugh - lag, 70);
  } else {
    // passers-by and a dog on the far cross path, behind the bench; each with its ghost a few steps ahead
    const P = [['ex1', 150, 70], ['ex6', 1900, -60]], dg = tt => 1800 - 120 * (tt - bench0);
    const far = (cam.z || 1) < 1.45;   // the far path only in the wide shots (in the blurred close-ups a sharp passer-by reads as standing on the bench)
    st.wld(g => { drawSet(g, 'park'); if (far) { for (const [n, x0, v] of P) walker(g, n, x0, v, t - bench0, { s: .4, y: 724 }); dog(g, dg(t), 738, .4, t * 9, -1); } bench(g, 0); bench(g, 1); });
    const L = [[700, 0], [1250, 2.1], [1500, 1.1], [420, 3.0]], leafAt = (tt, i) => { const [x, ph] = L[i], u = ((tt * .12 + ph * .3) % 1); return [x + Math.sin(u * 9 + i) * 40, -60 + u * 1100, u * 9]; };
    st.wld(g => { for (let i = 0; i < L.length; i++) leaf(g, ...leafAt(t, i)); });
    const hp = benchSit(900, { t, look: [14, 6], mouth: .1 });
    if (t > Lt('s12_09')) { hp.look = [16, 12]; hp.wide = .4; hp.brow = .5; }
    if (speaking(t, 's12_12')) { hp.open = talk(t, 's12_12'); hp.brow = .7; }
    st.col(g => drawChar(g, 'tu', hp));
    st.col(g => drawPigeon(g, 1080, 792, .62, { flip: -1, front: t > Lt('s12_12'), tilt: t > Lt('s12_13') ? .25 * bump(t, Lt('s12_13') + .3, Lt('s12_13') + 1.4) : Math.sin(t * 1.1) * .06 }));
    ga = vis(t, Lt('s12_07') + .4, T().dur);
    if (ga > 0) st.fut(g => { if (far) { for (const [n, x0, v] of P) walker(g, n, x0, v, t - bench0 + 4.5, { s: .4, y: 724 }); dog(g, dg(t + 3), 738, .4, t * 9, -1); } for (let i = 0; i < L.length; i++) leaf(g, ...leafAt(t + 3.5, i)); });
    st.col(g => futEyes(g, 'tu', hp, ga * .8));
    composeF(X, st, { ghost: ga, t, rim: .6 });
    if (t > Lt('s12_09') - .05) { const [px, py] = worldToScreen(cam, 1080, 740); X.save(); X.globalAlpha = R(t, Lt('s12_09'), Lt('s12_09') + .3); dashRing(X, px, py, 95 * cam.z, t); X.restore(); }
    if (t > Lt('s12_10') && t < Lt('s12_12')) sticker(X, 'FUTURO DE PEPE: ???', R(t, Lt('s12_10'), Lt('s12_10') + .25, back), 70, 70, 66, '#5ee7ff');
    futHUD(X, ga * .9, 5 - ((t * .8) % 5));
  }
};

/* ================================================================ 13. the hallway: every dodge moves the crash to someone else */
SC.s13 = (X, t) => {
  const B = Lt('s13_03') + .3, C = Lt('s13_05') + .2, D = Lt('s13_08') + .1, hit = Lt('s13_09') + .15;
  const cam = shots(t, [], [
    { t: 0, cx: 1300, cy: 560, z: 1.0, z2: 1.05, w: 2600, lock: 1 },
    { t: Lt('s13_02') - .05, cx: 1250, cy: 480, z: 1.8, w: 2600, lock: 1 },
    { t: B - .3, cx: 1250, cy: 580, z: 1.1, w: 2600, lock: 1 },
    { t: Lt('s13_06') - .05, cx: 1150, cy: 580, z: 1.05, w: 2600, lock: 1 },
    { t: Lt('s13_07') - .05, cx: 900, cy: 480, z: 2.0, z2: 2.1, w: 2600, lock: 1 },
    { t: D - .2, cx: 1250, cy: 560, z: 1.25, shake: 0, w: 2600, lock: 1 },
    { t: hit, cx: 1250, cy: 560, z: 1.3, shake: 1, w: 2600, lock: 1 },
    { t: Lt('s13_10') - .05, cx: 1330, cy: 470, z: 2.2, z2: 2.3, w: 2600, lock: 1 },
    { t: Lt('s13_11') - .1, cx: 1300, cy: 560, z: 1.0, w: 2600, lock: 1 },
  ]);
  const st = stageF(cam); st.wld(g => drawSet(g, 'hallway'));
  st.col(g => drawPigeon(g, 2050, 610, .42, { flip: -1, tilt: Math.sin(t * .9) * .12 }));
  // Renata walks left, reading, books on her arm; she reaches the hero lane at `hit`
  const rx = tt => Math.max(1360, 2300 - (tt - .3) * 52), rp = { x: rx(t), y: FEET, s: S0, t, flip: -1, walk: t < hit ? 1 : 0, phase: walkPh(rx(t)), look: [-6, 18], mouth: .1, hL: [-90, -420], hR: [60, -430], armsFront: 1,
    holdL: (g, x, y) => { if (t < hit) for (let i = 0; i < 3; i++) propBook(g, x + 30, y - 20 - i * 26, 110, 24, ['#4f86b8', '#c0262d', '#5aa37a'][i]); } };
  if (t > hit) { rp.walk = 0; rp.look = [-14, 0]; rp.wide = .6; rp.open = .4; rp.hL = [-160, -560]; rp.hR = [160, -560]; rp.lean = -.08 * bump(t, hit, hit + .5); }
  if (speaking(t, 's13_10')) { rp.open = talk(t, 's13_10'); rp.wide = .2; rp.brow = .6; rp.lid = .3; rp.hL = [-110, -330]; rp.hR = [110, -330]; }
  if (t > Lt('s13_11')) { rp.lid = .3; rp.mouth = .3; rp.hL = [-110, -330]; rp.hR = [110, -330]; }
  st.wld(g => drawChar(g, 'valeria', rp));
  // lanes: main lane y=FEET (Renata's path), the "aside" lane is in front: lower and a bit bigger
  const front = { y: FEET + 80, s: S0 * 1.1 };
  const np = { x: 900, y: FEET, s: S0, t, look: [10, 0], mouth: .4 };
  if (t > B + .6 && t < C) { np.x = mix(900, 1300, R(t, B + .6, C - .4, io)); np.walk = t < C - .4 ? 1 : 0; np.phase = walkPh(np.x); }
  if (t > C) Object.assign(np, { x: mix(1300, 1130, R(t, C, C + .4, outC)), ...front, look: [14, 0], wide: .5, open: .3, walk: 0 });
  const pp = { x: mix(560, 1300, R(t, C + .4, D, lin)), y: FEET, s: S0, t, walk: t > C + .4 && t < D ? 1 : 0, phase: walkPh(700 + t * 80), look: [10, 0], mouth: -.2, brow: .6, hR: [150, -430], holdR: (g, x, y) => propMug(g, x, y - 20, .9, '#f4f1ea') };
  st.wld(g => drawChar(g, 'profe', pp));
  st.wld(g => drawChar(g, 'nacho', np));
  const hp = { x: 1300, y: FEET, s: S0, t, look: [14, 0], mouth: .1 };
  if (t > B) Object.assign(hp, { x: mix(1300, 1470, R(t, B, B + .4, outC)), ...front, look: [-14, -4], mouth: .2, flip: -1 });
  if (t > C - .2 && t < C + .4) { hp.hR = [200, -420]; }
  if (t > Lt('s13_07')) { hp.look = [-14, -4]; hp.brow = .9; hp.mouth = -.3; hp.sweat = 1; }
  const dv = R(t, D, hit, io);
  if (t > D) Object.assign(hp, { x: mix(1470, 1300, dv), y: mix(FEET + 80, FEET, dv), s: mix(S0 * 1.1, S0, dv), flip: 1, lean: .5 * dv * (1 - R(t, hit + .3, hit + .8)), hL: [-200, -560], hR: [200, -600], wide: .7, open: .6, look: [14, 0] });
  if (t > hit + .8) { hp.lean = 0; hp.hL = hp.hR = null; hp.look = [14, 0]; hp.mouth = -.3; hp.sweat = 1; hp.open = 0; hp.wide = .3; }
  st.col(g => drawChar(g, 'tu', hp));
  // books in the air after the crash
  if (t > hit) st.wld(g => { const u = t - hit; for (let i = 0; i < 3; i++) { const vx = [-160, 120, 260][i], vy = [-620, -760, -540][i], y = Math.min(905, 580 + vy * u + 900 * u * u);
    propBook(g, 1300 + vx * Math.min(u, 1.3), y, 110, 24, ['#4f86b8', '#c0262d', '#5aa37a'][i], y < 900 ? u * 6 + i : .1 * i); } });
  // the future, three versions: you, then Nacho, then the professor get hit
  const victim = t < B + .5 ? 0 : t < C + .2 ? 1 : 2, gStart = [Lt('s13_01') + .4, B + .5, C + .2][victim];
  const ga = t < D - .2 ? vis(t, gStart, [B + .45, C + .15, D - .2][victim], .2, .12) : 0;
  if (ga > 0) st.fut(g => { const u = loopU(t, gStart, 2.0), vx = 1300;
    drawChar(g, 'valeria', { x: mix(1660, 1380, R(u, 0, .45, lin)), y: FEET, s: S0, t, flip: -1, look: [-6, 18], lean: u > .45 ? -.1 : 0, wide: u > .45 ? .6 : 0, hL: u > .45 ? [-160, -560] : [-90, -420], hR: u > .45 ? [160, -560] : [60, -430] });
    const who = ['tu', 'nacho', 'profe'][victim]; drawChar(g, who, { x: vx, y: FEET, s: S0, t, look: [14, 0], lean: u > .45 ? .12 : 0, wide: u > .45 ? .7 : 0, open: u > .45 ? .5 : 0 });
    if (u > .45) for (let i = 0; i < 3; i++) { const k = (u - .45) * 1.6; propBook(g, 1300 + [-160, 120, 260][i] * k, 600 - 300 * k + 700 * k * k, 110, 24, '#ffffff', k * 6 + i); } });
  st.col(g => futEyes(g, 'tu', hp, ga));
  composeF(X, st, { ghost: ga, t });
  if (t > hit && t < hit + .8) comicWord(X, '¡PLAF!', ...worldToScreen(cam, 1290, 520), t - hit, 90);
  if (t > Lt('s13_02') - .05 && t < Lt('s13_03')) sticker(X, 'OTRA VEZ', R(t, Lt('s13_02'), Lt('s13_02') + .2, back), 70, 70, 70);
  futHUD(X, ga, hudN(t, gStart, [B + .45, C + .15, D - .2][victim] + .4));
  ruleCard(X, 2, 'SI CAMBIAS EL FUTURO, VES UNO NUEVO', t > Lm('s13_11', .6) ? 'NO UNO MEJOR' : '', R(t, Lt('s13_11') - .2, Lt('s13_11') + .2, outC));
};

/* ================================================================ 14. back to the beginning: you answer before she asks */
SC.s14 = (X, t) => {
  const arrive = Lt('s14_05') + 2.5, blurt = Lt('s14_08'), leaveG = Lt('s14_11');
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 560, z: 1.0, z2: 1.05, lock: 1 },
    { t: Lt('s14_03') - .05, cx: 760, cy: 470, z: 2.3, z2: 2.4, lock: 1 },
    { t: Lt('s14_04') - .05, cx: 960, cy: 540, z: 1.2, z2: 1.25, lock: 1 },
    { t: Lt('s14_05') - .05, cx: 1120, cy: 470, z: 2.0, z2: 2.1, lock: 1 },
    { t: Lt('s14_06') - .05, cx: 770, cy: 470, z: 2.5, z2: 2.9, lock: 1 },
    { t: blurt - .05, cx: 900, cy: 520, z: 1.5, lock: 1 },
    { t: Lt('s14_09') - .05, cx: 1120, cy: 470, z: 2.1, z2: 2.2, lock: 1 },
    { t: Lt('s14_10') - .05, cx: 940, cy: 520, z: 1.45, lock: 1 },
    { t: leaveG - .05, cx: 1000, cy: 540, z: 1.15, z2: 1.2, lock: 1 },
  ]);
  const st = stageF(cam); st.wld(g => drawSet(g, 'street'));
  st.wld(g => { walker(g, 'ex3', 1350, 60, t, { s: .6, y: 860 }); walker(g, 'ex5', 420, -45, t, { s: .6, y: 860 }); });
  st.col(g => drawPigeon(g, 1560, 360, .42, { flip: -1, tilt: Math.sin(t * .8) * .1 }));
  const rx = mix(1800, 1110, R(t, Lt('s14_02'), arrive, io)), rp = { x: rx, y: FEET, s: S0, t, walk: t > Lt('s14_02') && t < arrive ? 1 : 0, phase: walkPh(rx), flip: -1, look: [-10, 2], mouth: .3, blush: .4, hR: [70, -330], holdR: (g, x, y) => propBook(g, x + 4, y - 20, 70, 90, '#4f86b8', .2) };
  if (t > blurt) { rp.walk = 0; rp.wide = .7; rp.open = .2; rp.mouth = 0; rp.brow = .5; rp.blush = 0; }
  if (speaking(t, 's14_10')) { rp.open = talk(t, 's14_10'); rp.wide = .3; rp.brow = .8; }
  if (t > Le('s14_10')) { rp.lid = .4; rp.mouth = -.2; rp.wide = 0; }
  st.wld(g => drawChar(g, 'valeria', rp));
  const hp = { x: 760, y: FEET, s: S0, t, look: [14, 0], mouth: .1 };
  if (t > Lt('s14_03')) { hp.wide = .4; hp.brow = .4; }
  if (t > Lt('s14_05')) { hp.mouth = -.1; hp.brow = .7; hp.sweat = t > Lt('s14_06') ? 1 : 0; hp.rot = t > Lt('s14_07') ? Math.sin(t * 30) * .02 : 0; }
  if (speaking(t, 's14_08') || (t > blurt && t < Lt('s14_09'))) { hp.open = speaking(t, 's14_08') ? talk(t, 's14_08') : 0; hp.mouth = .9; hp.wide = .8; const G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = POSE.stretch(R(t, blurt, blurt + .3, back) * .9, G); }
  if (t > Lt('s14_09')) { hp.hL = hp.hR = null; hp.mouth = -.3; hp.sweat = 1; hp.wide = .2; }
  st.col(g => drawChar(g, 'tu', hp));
  // the future: first she asks (ghost in front of you), at the end she turns and walks away
  const ga1 = vis(t, Lt('s14_03') + .3, blurt - .1), ga2 = vis(t, leaveG - .2, T().dur);
  if (ga1 > 0) st.fut(g => drawChar(g, 'valeria', { x: 1090, y: FEET, s: S0, t, flip: -1, look: [-14, 0], blush: .6, open: speaking(t, 's14_04') ? talk(t, 's14_04') : .1, hL: [-60, -330], hR: [40, -470] }));
  if (ga2 > 0) st.fut(g => { const u = R(t, leaveG + .3, leaveG + 3.5, lin), x = 1110 + 600 * u; drawChar(g, 'valeria', { x, y: FEET, s: S0, t, flip: 1, walk: u > 0 && u < 1 ? 1 : 0, phase: walkPh(x), look: [10, 4], mouth: -.2 }); });
  const ga = Math.max(ga1, ga2);
  st.col(g => futEyes(g, 'tu', hp, ga));
  composeF(X, st, { ghost: ga, t });
  if (speaking(t, 's14_04')) bubble(X, '¿FERIA DE CIENCIAS?', ...worldToScreen(cam, 1090, 300), ga1, 50);
  if (t > blurt && t < Lt('s14_09') + .5) bubble(X, '¡SÍ! ¡SÍ QUIERO!', ...worldToScreen(cam, 760, 330), R(t, blurt, blurt + .2, back), 58);
  futHUD(X, ga, ga2 > 0 ? hudN(t, leaveG - .2, leaveG + 4.5) : hudN(t, Lt('s14_03') + .3, arrive + .6));
};

/* ================================================================ 15. eyes closed, ears covered: the first present moment in a month */
SC.s15 = (X, t) => {
  const shut = Lt('s15_03') + .2, ears = Lm('s15_03', .55), open = Lt('s15_06') + .2;
  const cam = shots(t, [], [
    { t: 0, cx: 940, cy: 540, z: 1.2, lock: 1 },
    { t: Lt('s15_02') - .05, cx: 770, cy: 480, z: 2.0, z2: 2.1, lock: 1 },
    { t: Lt('s15_04') - .05, cx: 770, cy: 470, z: 2.6, z2: 2.9, lock: 1 },
    { t: open - .25, cx: 770, cy: 470, z: 2.4, lock: 1 },
    { t: Lt('s15_07') - .05, cx: 1110, cy: 470, z: 2.2, z2: 2.3, lock: 1 },
    { t: Lt('s15_09') - .05, cx: 770, cy: 480, z: 2.2, lock: 1 },
    { t: Lt('s15_10') - .05, cx: 1110, cy: 470, z: 2.2, z2: 2.3, lock: 1 },
    { t: Lt('s15_11') - .05, cx: 940, cy: 520, z: 1.5, z2: 1.55, lock: 1 },
    { t: Lt('s15_12') - .05, cx: 940, cy: 540, z: 1.15, z2: 1.3, lock: 1 },
  ]);
  const st = stageF(cam); st.wld(g => drawSet(g, 'street'));
  st.col(g => drawPigeon(g, 1560, 360, .42, { flip: -1, tilt: Math.sin(t * .8) * .1 }));
  const rp = { x: 1110, y: FEET, s: S0, t, flip: -1, look: [-14, 0], mouth: -.1, lid: .3, hR: [70, -330], holdR: (g, x, y) => propBook(g, x + 4, y - 20, 70, 90, '#4f86b8', .2) };
  if (t > Lt('s15_07')) { rp.lid = 0; rp.mouth = .2; rp.brow = .3; }
  for (const id of ['s15_08', 's15_10']) if (speaking(t, id)) { rp.open = talk(t, id); rp.blush = .6; rp.mouth = .4; }
  if (t > Lt('s15_10')) { rp.blush = .7; rp.mouth = .6; rp.lid = 0; }
  st.wld(g => drawChar(g, 'valeria', rp));
  const hp = { x: 760, y: FEET, s: S0, t, look: [14, 0], mouth: -.2, brow: .6, sweat: 1 };
  if (t > shut && t < open) { hp.blink = 1; hp.sweat = 0; hp.brow = .5; hp.mouth = -.1; }
  if (t > ears && t < open + .3) { const G = charGeom(CAST.tu, hp); const hy = G.top - 60; hp.hL = [-118, hy]; hp.hR = [118, hy]; }
  if (t > open) { hp.look = [14, 0]; hp.wide = .3; hp.mouth = .1; hp.sweat = 0; }
  if (speaking(t, 's15_09')) { hp.open = talk(t, 's15_09'); hp.mouth = .3; }
  if (speaking(t, 's15_11')) { hp.open = talk(t, 's15_11'); hp.mouth = .7; hp.blush = .6; }
  if (t > Le('s15_11')) { hp.mouth = .9; hp.blush = .6; hp.brow = -.2; }
  st.col(g => drawChar(g, 'tu', hp));
  const ga = vis(t, -1, shut - .1, .1, .25);   // the last ghost: Renata walking away, until you shut your eyes
  if (ga > 0) st.fut(g => { const x = 1110 + 300 * R(t, 0, 3, lin); drawChar(g, 'valeria', { x, y: FEET, s: S0, t, flip: 1, walk: 1, phase: walkPh(x), look: [10, 4], mouth: -.2 }); });
  composeF(X, st, { ghost: ga, t });
  // eyes shut: the world goes dark and quiet, the countdown is yours, in white
  const dark = R(t, shut, shut + .6) * (1 - R(t, open, open + .5));
  if (dark > 0) { X.save(); X.globalAlpha = dark * .82; X.fillStyle = '#05060c'; X.fillRect(0, 0, W, H); X.restore();
    const c0 = Lt('s15_05'), d = Ld('s15_05'); for (let i = 0; i < 5; i++) { const a0 = c0 + d * i / 5; if (t > a0 && t < a0 + d / 5 + .15) { const u = (t - a0) / (d / 5); X.save(); X.globalAlpha = Math.min(1, dark * 1.2) * (1 - clamp((u - .9) / .3)); const k = .8 + .2 * back(clamp(u * 3)); X.translate(W / 2, H / 2); X.scale(k, k); text(X, String(5 - i), 0, 120, 340, '#ffffff', 'Bangers', 'center', OUT, 16); X.restore(); } } }
  if (t > Lt('s15_12')) { X.save(); X.globalCompositeOperation = 'screen'; X.globalAlpha = .35 * R(t, Lt('s15_12'), Lt('s15_12') + 1.5); const gr = X.createRadialGradient(W / 2, H * .45, 0, W / 2, H * .45, H); gr.addColorStop(0, '#ffd28a'); gr.addColorStop(1, 'rgba(0,0,0,0)'); X.fillStyle = gr; X.fillRect(0, 0, W, H); X.restore(); }
  futHUD(X, ga, hudN(t, -4, shut + .5));
  ruleCard(X, 3, 'HAY COSAS QUE ES MEJOR', t > Lm('s15_13', .45) ? 'ESCUCHAR UNA SOLA VEZ' : '', R(t, Lt('s15_13') - .2, Lt('s15_13') + .2, outC));
};

/* ================================================================ 16. night bench: Pepe gets a ghost, and the ghost opens its beak */
SC.s16 = (X, t) => {
  const g0 = Lt('s16_05') + .2, beak = Lt('s16_06') + Ld('s16_06') * .55, cut = Le('s16_08') + .15;
  if (t >= cut) { X.fillStyle = '#000'; X.fillRect(0, 0, W, H); if (t > cut + .5) text(X, '…', W / 2, H / 2 + 30, 120, 'rgba(255,255,255,.5)', 'Bangers', 'center'); return; }
  const cam = shots(t, [], [
    { t: 0, cx: 980, cy: 640, z: 1.3, z2: 1.35, lock: 1 },
    { t: Lt('s16_02') - .05, cx: 990, cy: 650, z: 1.6, z2: 1.65, lock: 1 },
    { t: Lt('s16_03') - .05, cx: 1080, cy: 740, z: 2.6, z2: 2.7, lock: 1 },
    { t: Lt('s16_04') - .05, cx: 900, cy: 520, z: 2.6, z2: 2.8, lock: 1 },
    { t: g0 - .2, cx: 1100, cy: 700, z: 2.2, z2: 2.3, lock: 1 },
    { t: Lt('s16_06') - .05, cx: 1140, cy: 660, z: 3.0, z2: 3.3, lock: 1 },
    { t: Lt('s16_07') - .05, cx: 1120, cy: 690, z: 2.4, z2: 2.8, lock: 1 },
  ]);
  const st = stageF(cam); st.wld(g => { drawSet(g, 'parkNight'); bench(g, 0); bench(g, 1); });
  const hp = benchSit(900, { t, look: [14, 6], mouth: .3, open: t < Lt('s16_03') ? Math.abs(Math.sin(t * 7)) * .4 : 0 });
  if (t > Lt('s16_04')) { hp.open = 0; hp.wide = .7; hp.mouth = -.1; hp.brow = .8; }
  if (t > Lt('s16_07')) { hp.sweat = 1; hp.wide = 1; }
  st.col(g => drawChar(g, 'tu', hp));
  st.col(g => drawPigeon(g, 1080, 792, .62, { flip: -1, tilt: Math.sin(t * 1.1) * .06 }));
  const ga = vis(t, g0, cut + 1, .6);
  if (ga > 0) st.fut(g => { const u = R(t, beak, beak + .4, back); drawPigeon(g, 1150, 780 - 20 * ga, .7, { flip: -1, front: t > Lt('s16_06'), tilt: -.15 * u });
    if (u > 0) { g.save(); g.globalAlpha = u; shape(g, q => q.ellipse(1150, 700, 9, 14 * u, 0, 0, 7), '#0b2a3a', 3); g.restore(); } });
  st.col(g => futEyes(g, 'tu', hp, ga));
  composeF(X, st, { ghost: ga, t });
  if (t > Lt('s16_02') && t < Lt('s16_03')) { const items = [[0, 'feria'], [.4, 'ojos'], [.75, 'tacos']]; for (const [f, k] of items) { const a0 = Lm('s16_02', f); if (t > a0) { const a = R(t, a0, a0 + .25, back), [x, y] = [560 + f * 900, 200];
      X.save(); X.globalAlpha = a; X.translate(x, y); X.scale(a, a); circ(X, 0, 0, 70, '#ffffff', 5); if (k === 'tacos') taco(X, 0, 16, .9); else if (k === 'ojos') { line(X, [[-30, 0], [-10, 8]], OUT, 6); line(X, [[10, 8], [30, 0]], OUT, 6); } else text(X, '★', 0, 24, 70, '#5ee7ff', 'Bangers', 'center'); X.restore(); } } }
  if (t > beak) bubble(X, '…', ...worldToScreen(cam, 1150, 640), R(t, beak, beak + .3, back) * ga, 70);
  const cd = Lt('s16_08'), n = t < cd ? 5 : 5 - Math.min(4, Math.floor((t - cd) / (Ld('s16_08') / 4)) + 1) + 1;
  futHUD(X, ga, t < Lt('s16_07') ? 5 : n, t > Lt('s16_07') ? W / 2 : W - 150, t > Lt('s16_07') ? 190 : 150, t > Lt('s16_07') ? 120 : 86);
};

/* ================================================================ 17. is any of this real? */
SC.s17 = (X, t) => {
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 470, z: 1.12, z2: 1.16, lock: 1 },
    { t: Lt('s17_02') - .05, cx: 1010, cy: 400, z: 1.3, z2: 1.36, lock: 1 },
    { t: Lt('s17_05') - .05, cx: 1010, cy: 400, z: 1.3, z2: 1.36, lock: 1 },
    { t: Lt('s17_07') - .05, cx: 1010, cy: 400, z: 1.3, z2: 1.38, lock: 1 },
    { t: Lt('s17_08') - .05, cx: 960, cy: 480, z: 1.12, z2: 1.2, lock: 1 },
  ]);
  const a = (k) => clamp(k), ink = '#2d2a40', red = '#c0262d', blue = '#3a6fb0';
  const st = stageF(cam);
  st.wld(g => { drawSet(g, 'classroom'); teacherDesk(g, 1620);
    text(g, '¿ALGO DE ESTO ES REAL?', 966, 205, 70, red, 'Bangers', 'center');
    if (t > Lt('s17_02') - .1 && t < Lt('s17_05') - .1) {   // 1. you never see the present
      if (t < Lt('s17_04') - .1) { // eye -> brain, 0.1 s late; a moving ball and where your brain guesses it is
        shape(g, q => q.ellipse(600, 330, 64, 36, 0, 0, 7), '#ffffff', 5); circ(g, 600, 330, 22, blue, 4); circ(g, 600, 330, 10, ink, 0);
        line(g, [[680, 330], [820, 330]], ink, 6); shape(g, q => { q.moveTo(820, 314); q.lineTo(846, 330); q.lineTo(820, 346); q.closePath(); }, ink, 0);
        shape(g, q => q.ellipse(930, 330, 80, 60, 0, 0, 7), '#f2b8c6', 5); text(g, '0,1 s', 750, 300, 40, red, 'Bangers', 'center');
        text(g, 'NUNCA VES EL PRESENTE', 1180, 345, 46, ink, 'Bangers', 'left');
        if (t > Lt('s17_03') + 3) { const u = ((t - Lt('s17_03') - 3) * .5) % 1, bx = 640 + u * 620; g.globalAlpha = a((t - Lt('s17_03') - 3) * 3); propBall(g, bx, 420, 30, u * 9); g.globalAlpha = 1; }
      } else { // the penalty
        shape(g, q => q.rect(980, 260, 360, 200), 'rgba(255,255,255,.0)', 6); line(g, [[980, 460], [980, 260], [1340, 260], [1340, 460]], ink, 8);
        for (let i = 1; i < 6; i++) line(g, [[980 + i * 60, 262], [980 + i * 60, 458]], 'rgba(45,42,64,.25)', 2);
        const u = ((t - Lt('s17_04')) * .45) % 1; propBall(g, mix(620, 1260, outC(clamp(u * 1.6))), mix(470, 320, outC(clamp(u * 1.6))), 26, u * 12);
        text(g, '11 m', 800, 520, 40, ink, 'ComicNeue', 'center'); text(g, '< 0,5 s', 720, 330, 64, red, 'Bangers', 'center');
        text(g, 'EL PORTERO ADIVINA', 990, 520, 40, blue, 'Bangers', 'left'); } }
    if (t > Lt('s17_05') - .1 && t < Lt('s17_07') - .1) {   // 2. the seismic alert
      shape(g, q => { q.moveTo(470, 470); q.quadraticCurveTo(560, 300, 520, 250); q.lineTo(470, 250); q.closePath(); }, '#7fb6e0', 4);
      text(g, 'COSTA', 520, 520, 36, ink, 'ComicNeue', 'center'); circ(g, 540, 380, 12, red, 3);
      for (let i = 0; i < 3; i++) { const r = ((t * 70 + i * 90) % 270) + 10; g.save(); g.globalAlpha = 1 - r / 280; g.strokeStyle = '#a0522d'; g.lineWidth = 6; g.beginPath(); g.arc(540, 380, r, -1, 1); g.stroke(); g.restore(); }
      for (const [dx, h] of [[0, 120], [60, 170], [120, 100]]) shape(g, q => rrPath(q, 1180 + dx, 460 - h, 50, h, 4), '#9aa3ad', 4);
      text(g, 'CDMX', 1260, 520, 40, ink, 'Bangers', 'center');
      if (t > Lt('s17_06')) { const u = clamp((t - Lt('s17_06')) / 1.2); line(g, [[560, 360], [mix(560, 1160, u), 360]], blue, 7); if (u >= 1) { text(g, '¡ALERTA SÍSMICA!', 1260, 290, 44, red, 'Bangers', 'center'); }
        text(g, 'hasta 60 s antes', 860, 300, 40, blue, 'Bangers', 'center'); } }
    if (t > Lt('s17_07') - .1 && t < Lt('s17_08') - .1) {   // 3. sunlight is eight minutes old
      circ(g, 580, 360, 90, '#fde047', 6); for (let i = 0; i < 12; i++) { const an = i * Math.PI / 6; line(g, [[580 + Math.cos(an) * 110, 360 + Math.sin(an) * 110], [580 + Math.cos(an) * 140, 360 + Math.sin(an) * 140]], '#f0a020', 6); }
      circ(g, 1300, 360, 50, '#5aa0e0', 5); shape(g, q => q.ellipse(1290, 350, 22, 14, .4, 0, 7), '#7ec850', 0);
      const u = clamp((t - Lt('s17_07')) / 3); line(g, [[690, 360], [mix(690, 1240, u), 360]], '#f0a020', 5); text(g, '8 MINUTOS', 960, 320, 54, red, 'Bangers', 'center'); text(g, 'VES EL PASADO', 960, 470, 44, ink, 'Bangers', 'center'); }
    if (t > Lt('s17_08') - .1) { g.globalAlpha = a((t - Lt('s17_08')) * 2); text(g, 'NADIE VE EL FUTURO', 966, 340, 72, ink, 'Bangers', 'center'); text(g, 'TODOS LO ADIVINAMOS', 966, 430, 72, blue, 'Bangers', 'center'); g.globalAlpha = 1; }
  });
  const nod = Math.sin(t * 2.2) * .06 + (t > Lt('s17_08') ? .2 * bump(t, Lt('s17_08') + .4, Lt('s17_08') + 1.1) : 0);
  st.col(g => drawPigeon(g, 1600, 692, .95, { flip: -1, front: 1, tilt: nod }));
  // the guessed ball, drawn as a ghost just ahead of the real one: your brain's five-second power, one tenth of a second long
  const gb = t > Lt('s17_03') + 3 && t < Lt('s17_04') - .1 ? 1 : 0;
  if (gb) st.fut(g => { const u = ((t - Lt('s17_03') - 3) * .5) % 1; propBall(g, 640 + u * 620 + 70, 420, 30, u * 9); });
  composeF(X, st, { ghost: gb * a((t - Lt('s17_03') - 3) * 3), t, rim: 0 });
};

/* ================================================================ 18. call to action, end card */
SC.s18 = (X, t) => {
  const end = Le('s18_05') + .9;
  const cam = shots(t, [], [{ t: 0, cx: 1060, cy: 600, z: 1.25, z2: 1.35, lock: 1 }, { t: Lt('s18_05') - .1, cx: 1080, cy: 735, z: 3.6, z2: 3.8, lock: 1 }]);
  const st = stageF(cam); st.wld(g => { drawSet(g, 'parkNight'); bench(g, 0); bench(g, 1); });
  st.col(g => { drawChar(g, 'valeria', benchSit(1230, { t, look: [-14, 4], mouth: .6 }));
    drawChar(g, 'tu', benchSit(900, { t, look: [14, 4], mouth: .4, blush: .5, footSwing: Math.sin(t * 2.4) * 10 })); });
  st.col(g => drawPigeon(g, 1080, 792, .62, { flip: -1, front: 1, tilt: Math.sin(t * 1.3) * .08 }));
  composeF(X, st, { ghost: 0, t });
  if (t > Lt('s18_01') - .05 && t < Lt('s18_03') - .1) sticker(X, '¿QUÉ HARÍAS TÚ?', R(t, Lt('s18_01') - .05, Lt('s18_01') + .25, outC), 70, 60, 70);
  if (t > Lt('s18_02') - .05 && t < Lt('s18_03') - .1) sticker(X, '↓ COMENTARIOS ↓', R(t, Lt('s18_02') - .05, Lt('s18_02') + .25, outC), 70, 180, 60, '#ffffff');
  if (t > Lt('s18_03') - .05 && t < Lt('s18_04') - .1) {   // inset: the bedroom, the cat's ghost mid-air, Pepe on the sill with none
    const a = R(t, Lt('s18_03') - .05, Lt('s18_03') + .3, back), keep = SID, LX = layer('INSET');
    const tt = TIM.scenes.s03.L.s03_04[0] + 1.2 + ((t - Lt('s18_03')) * .6) % 1.5; SID = 's03'; SC.s03(LX, tt); const c0 = window.__cam; SID = keep; const [fx, fy] = worldToScreen(c0, 1250, 600);
    X.save(); X.translate(1300, 360); X.scale(a, a); shape(X, q => rrPath(q, -330, -195, 660, 390, 18), '#5ee7ff', 8);
    X.drawImage(LX.canvas, fx - 300, fy - 170, 600, 338, -310, -175, 620, 350);
    const [px, py] = worldToScreen(c0, 1380, 540); dashRing(X, (px - (fx - 300)) * 620 / 600 - 310, (py - (fy - 170)) * 350 / 338 - 175, 60, t); X.restore();
    sticker(X, 'PEPE: SIN FANTASMA', a, 1000, 600, 52, '#5ee7ff'); }
  if (t > Lm('s18_04', .5) && t < Lt('s18_05') - .1) { const a = R(t, Lm('s18_04', .5), Lm('s18_04', .5) + .3, back); X.save(); X.translate(W / 2, H - 200); X.scale(a, a); shape(X, q => rrPath(q, -260, -60, 520, 120, 20), '#e02424', 6); text(X, 'SUSCRÍBETE', 0, 26, 76, '#ffffff', 'Bangers', 'center'); X.restore(); }
  if (t > end) { const a = R(t, end, end + .5, outC); X.save(); X.globalAlpha = a; X.fillStyle = '#141a2e'; X.fillRect(0, 0, W, H);
    text(X, CHANNEL_NAME, W / 2, 230, 150, '#fde047', 'Bangers', 'center', OUT, 18);
    text(X, 'PRÓXIMO EPISODIO:', W / 2, 400, 64, '#ffffff', 'Bangers', 'center');
    text(X, '¿Y SI PUDIERAS HABLAR', W / 2, 500, 84, '#ffffff', 'Bangers', 'center', OUT, 10); text(X, 'CON LOS ANIMALES?', W / 2, 600, 84, '#ffffff', 'Bangers', 'center', OUT, 10);
    shape(X, q => rrPath(q, W / 2 - 300, 720, 600, 130, 22), '#e02424', 7); text(X, 'SUSCRÍBETE', W / 2, 812, 84, '#ffffff', 'Bangers', 'center');
    drawPigeon(X, 1600, 960, .9, { flip: -1, front: 1, tilt: Math.sin(t * 1.5) * .1 }); X.restore(); }
};
