/* Ep02 «¿Qué pasaría si pudieras ver 5 segundos del futuro?» — scenes 1–5.
   Beats are keyed to narration (Lt/Le/Lm from anim/episode.js). The future is drawn with st.fut(...) and shown by composeF. */
SC.missing = (X, t) => { X.fillStyle = '#1b1530'; X.fillRect(0, 0, W, H); text(X, SID + ' (sin animar)', W / 2, H / 2, 90, '#fde047', 'Bangers', 'center'); };
const loopU = (t, t0, P) => (((t - t0) % P) + P) % P / P;
/* ghost opacity: on from a (fade in fi), off at b (fade out fo) */
const vis = (t, a, b, fi = .25, fo = .3) => R(t, a, a + fi) * (1 - R(t, b, b + fo));
/* countdown: 5 at g0, 0 at the real event ev */
const hudN = (t, g0, ev) => 5 * clamp(1 - (t - g0) / Math.max(.01, ev - g0));
const arc = (u, x0, y0, x1, y1, h) => [mix(x0, x1, u), mix(y0, y1, u) - Math.sin(u * Math.PI) * h];
function lyingHead(g, x = 300, y = 680, p = {}) { drawHead(g, CAST.tu, x, y, -1.35, Object.assign({ sleep: 1 }, p)); }
function puddle(g, x, y, k, col = '#6a3b22') { if (k <= 0) return; ell(g, x, y, 30 + 150 * k, 8 + 10 * k, 0, col, 4);
  for (const [dx, dy, r] of [[-120, -16, 10], [130, -12, 8], [80, -30, 6]]) if (k > .5) circ(g, x + dx * k, y + dy, r, col, 3); }
function angerMark(g, x, y, s, a) { if (a <= 0) return; g.save(); g.globalAlpha = clamp(a); g.translate(x, y); g.scale(s, s);
  for (let i = 0; i < 4; i++) { g.save(); g.rotate(i * Math.PI / 2); line(g, [[8, 8], [8, 26], [26, 8]], '#e02424', 7); g.restore(); } g.restore(); }

/* ================================================================ 3. bedroom: Croqueta's ghost jumps first */
SC.s03 = (X, t) => {
  const g0 = Lt('s03_02') + .55, rt = Lt('s03_06') + Ld('s03_06') * .45, land = rt + .75, aside = Lt('s03_05') + .15, up = aside;
  const cam = shots(t, [], [
    { t: 0, cx: 760, cy: 600, z: 1.0, z2: 1.05 },
    { t: Lt('s03_02') - .1, cx: 620, cy: 700, z: 1.5, z2: 1.6, lock: 1 },
    { t: Lt('s03_03') - .05, cx: 1300, cy: 900, z: 2.0, z2: 2.1, lock: 1 },
    { t: Lt('s03_04') - .05, cx: 820, cy: 640, z: 1.08, z2: 1.12, lock: 1 },
    { t: aside - .05, cx: 640, cy: 640, z: 1.25, lock: 1 },
    { t: rt - .3, cx: 760, cy: 700, z: 1.2, z2: 1.3, lock: 1 },
    { t: Lt('s03_07') - .05, cx: 360, cy: 640, z: 2.2, z2: 2.3, lock: 1 },
  ]);
  const st = stageF(cam); st.wld(g => { drawSet(g, 'bedroom'); bedBack(g); nightstand(g); });
  st.col(g => drawPigeon(g, 1380, 562, .45, { flip: -1, tilt: Math.sin(t * .7) * .1 }));   // Pepe on the sill: the only thing with no ghost, all episode
  // the real cat: asleep on the rug, then the same jump five seconds later, then sulking on the pillow
  const ju = clamp((t - rt) / (land - rt));
  if (t < rt) st.wld(g => { drawCat(g, 1320, 1010, .7, { flip: -1 }); if (t < Lt('s03_04') + 2) zzz(g, 1290, 820, t); });
  else if (t < land) st.wld(g => { const [x, y] = arc(outC(ju), 1320, 1010, 330, 700, 420); drawCat(g, x, y, .7, { flip: -1, jump: .3 + .7 * Math.sin(ju * Math.PI) }); });
  // the hero: lying awake, then out of bed and to the side
  let hp = null;
  if (t < up) st.col(g => lyingHead(g, 300, 680, { sleep: t < Lt('s03_02') + .2, mouth: t > g0 ? -.3 : .2, wide: t > g0 ? .6 : 0, look: t > g0 ? [14, 6] : [0, 0], brow: t > g0 ? .6 : null }));
  else { hp = { x: 640, y: 945, s: S0, t, mouth: .1, look: [-16, 6], brow: .4, wide: .3 };
    if (t < up + .3) { hp.hy = -40 * (1 - (t - up) / .3); hp.lean = -.2 * (1 - (t - up) / .3); }
    if (t > land) { hp.mouth = .5; hp.brow = .2; hp.wide = 0; const G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = POSE.shrug(R(t, land + .2, land + .6, back) * .6, G); }
    if (t > Lt('s03_07')) { hp.mouth = -.25; hp.brow = .7; hp.sweat = 1; hp.hL = hp.hR = null; }
    st.col(g => drawChar(g, 'tu', hp)); }
  st.wld(g => bedFront(g, t < up ? 1 : .6));
  if (t >= land) st.wld(g => { drawCat(g, 360, 712, .62, { flip: t > Lt('s03_07') ? 1 : -1 }); angerMark(g, 470, 560, 1.2, R(t, Lt('s03_07') + .2, Lt('s03_07') + .5, back)); });
  // the future: the cat lands on your face, again and again, until it really does
  const ga = vis(t, g0, rt - .1);
  if (ga > 0) st.fut(g => { const u = loopU(t, g0, 2.1), k = clamp(u / .55);
    const [x, y] = arc(outC(k), 1320, 1010, 330, 690, 420); drawCat(g, x, y, .7, { flip: -1, jump: k < 1 ? .3 + .7 * Math.sin(k * Math.PI) : 0 }); });
  if (hp) st.col(g => futEyes(g, 'tu', hp, ga));
  composeF(X, st, { ghost: ga, t });
  futPulse(X, ...worldToScreen(cam, 300, 680), (t - g0) / .7);
  futHUD(X, ga, hudN(t, g0, rt));
};

/* ================================================================ 4. kitchen: the mug falls in the future, you catch it in the present */
SC.s04 = (X, t) => {
  const g0 = Lt('s04_01') + .35, kt = Lt('s04_04') + Ld('s04_04') * .55, catchT = kt + .42;
  const cam = shots(t, [], [
    { t: 0, cx: 760, cy: 580, z: 1.05, z2: 1.1, lock: 1 },
    { t: Lt('s04_02') - .05, cx: 600, cy: 800, z: 1.8, z2: 1.9, lock: 1 },
    { t: Lt('s04_03') - .05, cx: 700, cy: 620, z: 1.3, z2: 1.35, lock: 1 },
    { t: Lt('s04_04') - .05, cx: 600, cy: 700, z: 1.45, z2: 1.55, lock: 1 },
    { t: Lt('s04_05') - .05, cx: 820, cy: 520, z: 1.7, z2: 1.75, lock: 1 },
    { t: Lt('s04_06') - .05, cx: 480, cy: 540, z: 1.8, z2: 1.85, lock: 1 },
    { t: Lt('s04_07') - .1, cx: 760, cy: 560, z: 1.0, lock: 1 },
  ]);
  const st = stageF(cam); st.wld(g => drawSet(g, 'kitchen'));
  st.col(g => drawPigeon(g, 1560, 420, .4, { flip: -1, tilt: Math.sin(t * .6) * .12 }));   // on the window frame, no ghost
  // mom reads her phone; at kt her elbow sweeps left and knocks the mug off the table's left end
  const MX = 900, mugX0 = 640, mugY0 = 748;
  const mom = (tt, ghost) => { const k = R(tt, -.25, .1, outC) * (1 - R(tt, .6, 1.0)); const p = { x: MX, y: FEET, s: S0, t: ghost ? t : t, mouth: .2, look: [6, 16], hR: [90, -420], holdR: (q, x, y) => propPhone(q, x, y - 30, .5, 64, .1),
      hL: [mix(-150, -330, k), mix(-300, -350, k)] };
    if (tt > .1 && tt < 1.4) { p.look = [-16, 14]; p.wide = .5; p.open = .4; } return p; };
  const mp = mom(t - kt, false);
  if (speaking(t, 's04_05')) { mp.open = talk(t, 's04_05'); mp.look = [-18, 4]; mp.brow = .8; mp.wide = .6; mp.hR = [70, -520]; }
  if (t > Le('s04_05')) { mp.look = [-18, 4]; mp.brow = .5; mp.wide = .3; }
  st.wld(g => drawChar(g, 'mama', mp));
  st.wld(g => kitchenTable(g));
  // the mug: on the table, slides and falls at kt; you catch it at catchT
  const mugAt = (tt, caught) => { if (tt < .12) return [mugX0, mugY0, 0];
    const u = (tt - .12); if (u < .2) return [mugX0 - 260 * u / .2 * .4, mugY0, -u * 3];
    const f = u - .2, x = mugX0 - 104 - 160 * f, y = mugY0 + 520 * f * f + 30 * f; return caught && tt > catchT - kt ? null : [x, Math.min(y, 1000), -.6 - f * 6]; };
  const hx = mix(250, 420, R(t, .2, Lt('s04_02'), io)), hp = { x: hx, y: FEET, s: S0, t, walk: t > .2 && t < Lt('s04_02') ? 1 : 0, phase: walkPh(hx), mouth: .2, look: [14, 0] };
  const ga = vis(t, g0, kt - .2);
  if (t > g0) { hp.look = [16, 4]; hp.brow = .5; hp.wide = .4 * ga; }
  // reach: start just before the knock, hand meets the falling mug
  const reach = R(t, kt - .05, catchT, outC);
  const catchPt = [mugX0 - 104 - 160 * (catchT - kt - .32), mugY0 + 520 * (catchT - kt - .32) ** 2 + 30 * (catchT - kt - .32)];
  if (reach > 0) { hp.lean = .12 * reach * (1 - R(t, catchT + .4, catchT + .9)); hp.hR = [mix(112, (catchPt[0] - hx) / S0, reach), mix(-200, (catchPt[1] + 26 - FEET) / S0, reach)]; hp.look = [16, 12]; hp.wide = .5; hp.mouth = .4; }
  if (t > catchT) { hp.holdR = (g, x, y) => propMug(g, x + 6, y - 26, 1.0, '#f4f1ea'); }
  if (t > catchT + .9) { const u = R(t, catchT + .9, catchT + 1.4, io); hp.hR = [mix((catchPt[0] - hx) / S0, 150, u), mix((catchPt[1] + 26 - FEET) / S0, -470, u)]; hp.lean = 0; }
  if (speaking(t, 's04_06') || t > Le('s04_06')) { hp.mouth = speaking(t, 's04_06') ? .3 + talk(t, 's04_06') * .5 : .6; hp.look = [12, -2]; hp.brow = -.3; hp.lid = .3; }
  st.col(g => drawChar(g, 'tu', hp));
  const m = mugAt(t - kt, true); if (m) st.wld(g => propMug(g, m[0], m[1], 1.25, '#f4f1ea'));
  // the future: elbow, fall, crash, puddle — on a loop until it is about to happen for real
  if (ga > 0) st.fut(g => { const u = loopU(t, g0, 2.6) * 2.6 - .3;
    drawChar(g, 'mama', Object.assign(mom(u, true), { still: 1 }));
    const mg = mugAt(u, false); if (mg && mg[1] < 1000) propMug(g, mg[0], mg[1], 1.25, '#f4f1ea');
    else if (mg) { puddle(g, 420, 1010, R(u, 1.1, 1.5, outC)); for (const [dx, r] of [[-60, .4], [40, -.6], [90, .9]]) shape(g, q => { q.save(); q.translate(420 + dx, 1000); q.rotate(r); rrPath(q, -18, -12, 36, 24, 6); q.restore(); }, '#f4f1ea', 4); } });
  st.col(g => futEyes(g, 'tu', hp, ga));
  composeF(X, st, { ghost: ga, t });
  futPulse(X, ...worldToScreen(cam, 640, 740), (t - g0) / .7);
  futHUD(X, ga, hudN(t, g0, kt));
  ruleCard(X, 1, 'VES Y OYES TODO 5 SEGUNDOS ANTES', t > Lt('s04_08') - .1 ? 'TODO. SIEMPRE. NO SE APAGA.' : '', R(t, Lt('s04_07') - .2, Lt('s04_07') + .2, outC));
};

/* ================================================================ 0. cold open: Renata's question is already in your ears */
function rewindFX(X, k, t) { if (k <= 0) return;
  X.save(); X.globalAlpha = .25 * k; X.fillStyle = '#ffffff'; const r = rnd(Math.floor(t * 30));
  for (let i = 0; i < 9; i++) { const y = r() * H, h = 4 + r() * 18; X.fillRect(0, y, W, h); } X.restore();
  X.save(); X.globalAlpha = .55 * k; X.fillStyle = '#0d0b12'; X.fillRect(0, H - 150, W, 150); X.restore();
  X.save(); X.globalAlpha = k; text(X, '◀◀  REBOBINANDO', 70, H - 52, 76, '#ffffff', 'Bangers', 'left', OUT, 10); X.restore(); }
function walker(g, n, x0, v, tt, extra = {}) { const x = x0 + v * tt; drawChar(g, n, Object.assign({ x, y: FEET, s: S0, t: tt, walk: 1, phase: walkPh(x), flip: v < 0 ? -1 : 1 }, extra)); return x; }
SC.s00 = (X, t) => {
  const rw = Lm('s00_05', .45), tr = t < rw ? t : Math.max(0, rw - (t - rw) * 4);   // the tape runs back after rw
  const cam = shots(t, [], [
    { t: 0, cx: 760, cy: 470, z: 2.5, z2: 2.7, lock: 1 },
    { t: Lt('s00_02') - .05, cx: 960, cy: 560, z: 1.15, z2: 1.2, lock: 1 },
    { t: Lt('s00_03') - .05, cx: 1120, cy: 470, z: 2.1, z2: 2.25, lock: 1 },
    { t: Lt('s00_04') - .05, cx: 770, cy: 480, z: 2.4, z2: 2.6, lock: 1 },
    { t: rw, cx: 960, cy: 540, z: 1.0, lock: 1 },
  ]);
  const st = stageF(cam); st.wld(g => drawSet(g, 'street'));
  st.wld(g => { walker(g, 'ex3', 1350, 60, tr, { s: .6, y: 860 }); walker(g, 'ex5', 420, -45, tr, { s: .6, y: 860, look: [-8, 0] }); });
  st.col(g => drawPigeon(g, 1560, 360, .42, { flip: -1, tilt: Math.sin(t * .8) * .1 }));   // on the lamp: no ghost
  // Renata walks up; her ghost already stands in front of you, asking
  const rx = mix(1750, 1250, R(tr, 0, 13, lin)), rp = { x: rx, y: FEET, s: S0, t: tr, walk: 1, phase: walkPh(rx), flip: -1, look: [-10, 2], mouth: .2, hR: [70, -330], holdR: (g, x, y) => propBook(g, x + 4, y - 20, 70, 90, '#4f86b8', .2) };
  st.wld(g => drawChar(g, 'valeria', rp));
  const hp = { x: 760, y: FEET, s: S0, t, look: [16, 0], mouth: -.1, brow: .5, wide: .4 };
  if (t > Lt('s00_04')) { hp.open = .5 * R(t, Lt('s00_04'), Lt('s00_04') + .5); hp.sweat = 1; hp.brow = .8; hp.lean = .06; }
  if (t > rw) { hp.wide = 0; hp.open = 0; }
  st.col(g => drawChar(g, 'tu', hp));
  const ga = vis(t, .2, rw - .2, .5);
  if (ga > 0) st.fut(g => drawChar(g, 'valeria', { x: 1090, y: FEET, s: S0, t, flip: -1, look: [-14, 0], open: .2 + .5 * Math.abs(Math.sin(t * 9)) * (Math.sin(t * 1.3) > -.3 ? 1 : 0), blush: .5, hL: [-60, -330], hR: [40, -470] }));
  st.col(g => futEyes(g, 'tu', hp, ga));
  composeF(X, st, { ghost: ga, t });
  if (t > Lt('s00_02') && t < rw) bubble(X, '¿…?', ...worldToScreen(cam, 1100, 300), R(t, Lt('s00_02'), Lt('s00_02') + .3, back) * ga, 64);
  futHUD(X, ga, 5 - (t / (rw + 1.5)) * 5);
  rewindFX(X, R(t, rw, rw + .25), t);
  if (t > T().dur - .25) { X.save(); X.globalAlpha = R(t, T().dur - .25, T().dur, lin); X.fillStyle = '#ffffff'; X.fillRect(0, 0, W, H); X.restore(); }
};

/* ================================================================ 1. the premise: everyone walks behind their own ghost */
function crossSticker(X, s, a, x, y, ok) { if (a <= 0) return; sticker(X, s, a, x, y, 70, ok ? '#5ee7ff' : '#ffffff');
  if (!ok) { X.save(); X.globalAlpha = clamp(a); X.font = '70px Bangers'; const w = X.measureText(s).width + 40; X.strokeStyle = '#e02424'; X.lineWidth = 12; X.lineCap = 'round';
    X.beginPath(); X.moveTo(x - 6, y + 70); X.lineTo(x + w + 26, y + 6); X.stroke(); X.restore(); } }
SC.s01 = (X, t) => {
  const P = [['ex1', -150, 62, .8, 952], ['ex6', 2070, -62, .8, 952], ['ex4', 1480, 36, .78, 942]];   // on the sidewalk (not up the wall), never crossing the hero
  const duck = Lm('s01_04', .2), catchT = Lm('s01_04', .5), say = Lm('s01_04', .78);
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 540, z: 1.0, z2: 1.06, lock: 1 },
    { t: Lt('s01_02') - .05, cx: 900, cy: 560, z: 1.2, z2: 1.24, lock: 1 },
    { t: Lt('s01_03') - .05, cx: 900, cy: 470, z: 2.0, z2: 2.1, lock: 1 },
    { t: Lt('s01_04') - .05, cx: 960, cy: 560, z: 1.15, z2: 1.2, lock: 1 },
    { t: say - .3, cx: 1050, cy: 500, z: 1.7, z2: 1.8, lock: 1 },
    { t: Lt('s01_05') - .05, cx: 1050, cy: 480, z: 2.0, z2: 2.1, lock: 1 },
  ]);
  const st = stageF(cam); st.wld(g => drawSet(g, 'street'));
  st.col(g => drawPigeon(g, 1700, 560, .4, { flip: -1, peck: Math.max(0, Math.sin(t * 2.4)) * .6 }));
  const wl = t < Lt('s01_04') - .1;
  // a ball for the dodge, a mug for the catch, a question for the answer
  const hp = { x: 900, y: FEET, s: S0, t, look: [10, 0], mouth: .2 };
  if (t > Lt('s01_03') && t < Lt('s01_04')) { const G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = POSE.shrug(R(t, Lt('s01_03'), Lt('s01_03') + .4, back) * .6, G); hp.mouth = -.2; hp.brow = .4; }
  const bu = (t - duck + .6) / 1.0;
  if (t > Lt('s01_04') - .1) {
    st.wld(g => { drawChar(g, 'ex1', { x: 1650, y: FEET, s: S0, t, flip: -1, hR: t < duck - .6 ? [160, -560] : [220, -400], look: [-10, 0], mouth: .3 }); drawChar(g, 'ex2', { x: 1220, y: FEET, s: S0, t, flip: -1, look: [-12, 2], mouth: .1 }); });
    if (bu > 0 && bu < 1) st.wld(g => propBall(g, mix(1560, 300, bu), 470 + Math.sin(bu * Math.PI) * -60, 34, bu * 8));
    if (t > duck - .25 && t < duck + .45) { hp.jump = -60 * bump(t, duck - .25, duck + .45); hp.slump = 3 * bump(t, duck - .25, duck + .45); hp.hy = 60 * bump(t, duck - .25, duck + .45); }
    const mu = R(t, catchT - .5, catchT);
    if (t > catchT - .5) { if (t < catchT) st.wld(g => propMug(g, 1040, mix(600, 760, mu * mu), 1.1, '#e07a8a')); else { hp.hR = [180, -330]; hp.holdR = (g, x, y) => propMug(g, x + 6, y - 22, 1.0, '#e07a8a'); } }
    if (t > say) { hp.look = [14, -2]; hp.mouth = .7; hp.brow = -.2; }
  }
  if (t > Lt('s01_05')) { hp.mouth = -.25; hp.sweat = 1; hp.brow = .7; }
  st.col(g => drawChar(g, 'tu', hp));
  if (wl) st.wld(g => { for (const [n, x0, v, s, y] of P.slice().sort((a, b) => a[4] - b[4])) walker(g, n, x0, v, t, { s, y }); });   // closer than the hero: drawn after him
  // ghosts: walkers five 'seconds' ahead (a few steps), the ball arriving early, the question asked early
  const gw = vis(t, .4, Lt('s01_03') - .2) + vis(t, Le('s01_03') + .2, Lt('s01_04') - .3), gb = vis(t, Lt('s01_04') - .1, Lt('s01_05') + 2.5);
  if (gw > 0) st.fut(g => { for (const [n, x0, v, s, y] of P) walker(g, n, x0, v, t + 4.5, { s, y }); });
  if (gb > 0) st.fut(g => { const u = (t - duck + 1.8) / 1.0; if (u > 0 && u < 1) propBall(g, mix(1560, 300, u), 470 - Math.sin(u * Math.PI) * 60, 34, u * 8);
    if (t > Lt('s01_04') + .5 && t < catchT - .4) propMug(g, 1040, 760, 1.1, '#e07a8a');
    if (t > catchT && t < Lt('s01_05') + 2) drawChar(g, 'ex2', { x: 1220, y: FEET, s: S0, t, flip: -1, look: [-12, 0], open: .3 + .4 * Math.abs(Math.sin(t * 8)), hR: [150, -470] }); });
  const ga = Math.max(gw, gb);
  st.col(g => futEyes(g, 'tu', hp, ga * .8));
  composeF(X, st, { ghost: ga, t, rim: .6 });
  if (t > Lt('s01_02') - .05 && t < Lt('s01_03') - .05) { crossSticker(X, '5 AÑOS', R(t, Lm('s01_02', .02), Lm('s01_02', .12), outC), 120, 120); crossSticker(X, '5 DÍAS', R(t, Lm('s01_02', .36), Lm('s01_02', .46), outC), 120, 250);
    crossSticker(X, '5 SEGUNDOS', R(t, Lm('s01_02', .68), Lm('s01_02', .78), outC), 120, 380, true); }
  if (t > say && t < Lt('s01_05') + .1) bubble(X, '¡TE VES INCREÍBLE!', ...worldToScreen(cam, 900, 330), R(t, say, say + .3, back), 50);
  if (t > Lt('s01_05') + .3) bubble(X, '¿…QUÉ?', ...worldToScreen(cam, 1220, 330), R(t, Lt('s01_05') + .3, Lt('s01_05') + .6, back), 54);
  if (t > Lt('s01_04') && t < Lt('s01_05')) { const lab = t < catchT - .5 ? '¡ESQUIVAR!' : t < say - .3 ? '¡ATRAPAR!' : '¡ACERTAR!'; sticker(X, lab, 1, 70, 70, 64, '#5ee7ff'); }
  futHUD(X, ga * .9, 5 - ((t * .9) % 5));
};

/* ================================================================ 2. title card */
SC.s02 = (X, t) => {
  /* at zoom 1 any other cy shows the bare canvas past the painting's edge */
  const cam = { cx: 960, cy: 540, z: 1.0 }, st = stageF(cam); st.wld(g => drawSet(g, 'street'));
  const P = [['ex3', 300, 90], ['ex2', 1700, -80], ['nacho', 900, 60], ['ex5', 1300, -70]];
  st.wld(g => { for (const [n, x0, v] of P) walker(g, n, x0, v, t); });
  st.fut(g => { for (const [n, x0, v] of P) walker(g, n, x0, v, t + 3.2); });
  composeF(X, st, { ghost: R(t, .1, .5), t });
  titleCard(X, '¿QUÉ PASARÍA SI PUDIERAS', 'VER 5 SEGUNDOS DEL FUTURO?', R(t, .3, .8, outC), t);
};

/* ================================================================ 5. dodgeball: you see every ball before it is thrown */
function fieldLine(g) { g.save(); g.strokeStyle = 'rgba(255,255,255,.85)'; g.lineWidth = 10; g.setLineDash([30, 22]); g.beginPath(); g.moveTo(1010, 760); g.lineTo(1060, 1080); g.stroke(); g.restore(); }
SC.s05 = (X, t) => {
  const t3 = Lt('s05_04'), D = [t3 + .1, Lm('s05_04', .45), Lm('s05_04', .8)];   // duck, jump, spin
  const endT = Lt('s05_06') - .1;
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 560, z: 1.0, z2: 1.04, lock: 1 },
    { t: Lt('s05_02') - .05, cx: 560, cy: 520, z: 1.7, z2: 1.8, lock: 1 },
    { t: Lt('s05_03') - .05, cx: 900, cy: 560, z: 1.2, z2: 1.25, lock: 1 },
    { t: t3 - .05, cx: 600, cy: 600, z: 1.35, z2: 1.45, lock: 1 },
    { t: Lt('s05_05') - .05, cx: 960, cy: 560, z: 1.05, lock: 1 },
    { t: endT, cx: 1000, cy: 560, z: 1.1, z2: 1.15, lock: 1 },
    { t: Lt('s05_07') - .05, cx: 1450, cy: 470, z: 2.1, z2: 2.2, lock: 1 },
    { t: Lt('s05_08') - .05, cx: 1450, cy: 470, z: 2.5, z2: 2.6, lock: 1 },
  ]);
  const st = stageF(cam); st.wld(g => { drawSet(g, 'field'); fieldLine(g); });
  st.col(g => drawPigeon(g, 1180, 300, .38, { flip: -1, tilt: Math.sin(t) * .1 }));   // on the goal's crossbar
  const left = [['ex5', 160], ['ex4', 360]], right = [['ex1', 1240], ['ex6', 1660], ['ex3', 1830]];
  const out = t > endT;
  // teammates and rivals: the others leave the court before the end
  st.wld(g => { for (const [n, x] of left) drawChar(g, n, { x: out ? x - 600 : x, y: FEET, s: S0, t, look: [10, 0], mouth: .3 });
    for (const [n, x, i] of right.map((r, i) => [...r, i])) { const thr = (t * 1.3 + i * .7) % 2.4 < .3; drawChar(g, n, { x: out ? x + 700 : x, y: FEET, s: S0, t, flip: -1, look: [-10, 0], mouth: .4, hR: thr ? [200, -420] : [150, -560] }); }
    drawChar(g, 'nacho', { x: 1450, y: FEET, s: S0, t, flip: -1, look: [-12, 0], mouth: t > Lt('s05_07') ? -.2 : .5, sweat: t > Lt('s05_07') ? 1 : 0, brow: t > Lt('s05_07') ? .8 : 0, wide: t > Lt('s05_07') ? .6 : 0,
      hR: [120, -470], holdR: (q, x, y) => propBall(q, x, y - 10, 38), rot: t > Lt('s05_07') ? Math.sin(t * 40) * .02 : 0 }); });
  // balls: from the right side toward you; ghosts arrive first
  const ballAt = (tt, i) => { const t0 = i < 3 ? D[i] - .55 : 7 + i * .55, u = (tt - t0) / .8; if (u < 0 || u > 1) return null; const y0 = [520, 600, 500][i % 3]; return [mix(1500, 200, u), y0 + (i === 0 ? -40 : 0)]; };
  st.wld(g => { for (let i = 0; i < 14; i++) { const b = ballAt(t, i); if (b && t < endT) propBall(g, b[0], b[1], 42, t * 9); } });
  const hp = { x: 640, y: FEET, s: S0, t, look: [14, 0], mouth: .2, brow: .2 };
  if (t > Lt('s05_02') && t < Lt('s05_03')) { hp.mouth = -.3; hp.brow = .6; hp.sweat = 1; }
  if (t > Lt('s05_03')) { hp.mouth = .5; hp.brow = -.3; hp.lid = .2; }
  const dk = bump(t, D[0] - .3, D[0] + .4), jp = bump(t, D[1] - .3, D[1] + .45), sp = R(t, D[2] - .2, D[2] + .4);
  if (dk > 0) { hp.hy = 120 * dk; hp.slump = 4 * dk; hp.jump = -40 * dk; }
  if (jp > 0) { hp.jump = 170 * jp; const G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = POSE.stretch(jp, G); }
  if (sp > 0 && sp < 1) hp.flip = Math.cos(sp * Math.PI * 2) > 0 ? 1 : -1;
  if (t > Lt('s05_05') && t < endT) { hp.x = 620 + Math.sin(t * 5) * 60; hp.lean = Math.sin(t * 10) * .12; }
  if (t > Lt('s05_08')) { hp.mouth = .3; hp.brow = .2; hp.lid = 0; }
  st.col(g => drawChar(g, 'tu', hp));
  const ga = vis(t, Lt('s05_03') - .1, endT - .3);
  if (ga > 0) st.fut(g => { for (let i = 0; i < 14; i++) { const b = ballAt(t + .9, i); if (b) propBall(g, b[0], b[1], 42, t * 9); } });
  st.col(g => futEyes(g, 'tu', hp, ga));
  composeF(X, st, { ghost: ga, t });
  futHUD(X, ga, 5 - ((t * 1.6) % 5));
  if (t > Lt('s05_05') - .05 && t < Lt('s05_06') + .5) { const n = Math.min(43, Math.floor(R(t, Lt('s05_05') - .3, Le('s05_05'), lin) * 43)); bigCounter(X, 'ESQUIVADOS:', String(n), R(t, Lt('s05_05') - .1, Lt('s05_05') + .2, outC)); }
  if (t > Lt('s05_08')) bubble(X, '¿QUÉ ERES?', ...worldToScreen(cam, 1450, 330), R(t, Lt('s05_08'), Lt('s05_08') + .25, back), 72);
};
