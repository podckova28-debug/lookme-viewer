/* Ep01 v3 scenes: 11b dinner with mum, 17 the Pepe twist, 18 ¿Algo de esto es real?, 19 call to action + end card */

/* ================================================================ 11b. dinner: mum notices, you cannot tell her */
SC.s11b = (X, t) => {
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 560, z: 1.12, z2: 1.18 },
    { t: Lt('s11b_02') - .05, cx: 1220, cy: 520, z: 2.0, z2: 2.08 },
    { t: Lt('s11b_03') - .05, cx: 740, cy: 520, z: 2.1, z2: 2.25 },
    { t: Lt('s11b_04') - .05, cx: 1220, cy: 520, z: 2.1, z2: 2.2 },
    { t: Lt('s11b_05') - .05, cx: 720, cy: 520, z: 2.0 },
    { t: Lt('s11b_06') - .05, cx: 960, cy: 560, z: 1.2, z2: 1.05, lock: 1 },
    { t: Lt('s11b_07') - .05, cx: 720, cy: 540, z: 1.5, z2: 2.0, lock: 1 },
  ]);
  const st = stage(cam); st.wld(g => drawSet(g, 'kitchenNight'));
  const mp = seated('mama', 1220, { t, look: [-14, 6], mouth: .3, hL: [-70, -300], hR: [70, -300] });
  if (t > Lt('s11b_01') + .6) { mp.look = [-16, -2]; mp.brow = .4; }
  if (t > Lt('s11b_02') - .05) { mp.open = talk(t, 's11b_02') + talk(t, 's11b_04'); mp.brow = .5; mp.mouth = .1; }
  if (t > Lt('s11b_02') - .05 && t < Lt('s11b_03')) { mp.hL = [-200, -470]; mp.look = [-18, -8]; }        // points at his hair
  if (t > Lt('s11b_04') - .05) { mp.brow = .7; mp.mouth = -.1; mp.look = [-16, 2]; mp.hL = [-150, -330]; }  // reaches across the table
  st.wld(g => drawChar(g, 'mama', mp));
  const hp = seated('tu', 720, { t, look: [6, 14], mouth: -.1, lid: .35, slump: .6, hL: [-60, -300], hR: [60, -300] });
  if (t > Lt('s11b_02') - .05) { hp.look = [14, 0]; hp.lid = .1; hp.wide = .2; }
  if (t > Lt('s11b_03') - .05 && t < Lt('s11b_04')) { hp.look = [4, -14]; hp.hR = [40, -640]; hp.wide = .3; }   // touches his hair
  if (t > Lt('s11b_05') - .05) { hp.open = talk(t, 's11b_05'); hp.mouth = .4; hp.lid = .3; hp.look = [14, 4]; }
  if (t > Lt('s11b_06') - .05) { hp.open = 0; hp.mouth = -.2; hp.lid = .45; hp.look = [4, 16]; hp.slump = 1; }
  st.col(g => drawChar(g, 'tu', hp));
  st.wld(g => { kitchenTable(g); for (const x of [740, 1200]) { ell(g, x, 776, 62, 12, 0, '#f4f1ea', 4); ell(g, x, 774, 40, 7, 0, '#e8a35a', 0); } propMug(g, 960, 760, .9, '#f4f1ea'); });
  compose2(X, st, { amt: 0 });
  if (t > Lm('s11b_03', .1) && t < Lt('s11b_04') - .1) sticker(X, '+0,5 MM POR DÍA', R(t, Lm('s11b_03', .1), Lm('s11b_03', .1) + .25, outC), 1180, 200, 64);
  if (t > Lt('s11b_06') - .05 && t < Lt('s11b_07') - .1) { const a = R(t, Lt('s11b_06') - .05, Lt('s11b_06') + .25, outC);
    sticker(X, 'TÚ: +13 DÍAS', a, 300, 180, 70); sticker(X, 'ELLA: UN MARTES', R(t, Lm('s11b_06', .55), Lm('s11b_06', .55) + .25, outC), 1180, 180, 70, '#ffffff'); }
};

/* ================================================================ 17. callback, then the twist: Pepe moves too */
function pepeMontage(X, t, t0, t1) {   // 'en el mundo congelado, Pepe nunca se puso gris': frozen moments, Pepe circled in colour
  const clips = [['s00', () => 1.6, [1700, 140]], ['s03', () => TIM.scenes.s03.L.s03_06[0] + .6, [1380, 535]],
    ['s10', () => TIM.scenes.s10.L.s10_04[0] + 1.2, [1560, 245]], ['s14', () => TIM.scenes.s14.L.s14_06[0] + .3, [1060, 760]]];
  const n = clips.length, k = Math.min(n - 1, Math.floor((t - t0) / ((t1 - t0) / n))), u = ((t - t0) / ((t1 - t0) / n)) % 1;
  const [sid, tt, [px, py]] = clips[k], keep = SID; SID = sid; SC[sid](X, tt()); const cam = window.__cam; SID = keep;
  const [sx, sy] = worldToScreen(cam, px, py);
  X.save(); X.strokeStyle = '#fde047'; X.lineWidth = 12; X.beginPath(); X.arc(sx, sy, 90 + 30 * (1 - outC(clamp(u * 3))), 0, 7); X.stroke(); X.restore();
  if (u < .12) { X.save(); X.globalAlpha = 1 - u / .12; X.fillStyle = '#ffffff'; X.fillRect(0, 0, W, H); X.restore(); }
  sticker(X, 'REBOBINA Y MIRA', 1, 70, 60, 70, '#ffffff');
}
SC.s17 = (X, t) => {
  if (t < Lm('s17_00', .55)) {   // callback to the cold open: the pot over her head
    const sid = SID, k = R(t, Lt('s17_00'), Lm('s17_00', .55), lin); SID = 's00'; SC.s00(X, 1.2 + k * 2.5); SID = sid;
    X.save(); X.globalCompositeOperation = 'multiply'; X.fillStyle = 'rgba(255,225,180,1)'; X.fillRect(0, 0, W, H); X.restore();
    X.save(); X.globalAlpha = .12; X.fillStyle = '#000'; for (let y = (t * 60) % 6; y < H; y += 6) X.fillRect(0, y, W, 2); X.restore(); return; }
  const m0 = Lm('s17_10', .42), m1 = T().dur - .3;
  if (t > m0 && t < m1) { pepeMontage(X, t, m0, m1); return; }
  const turn = Lm('s17_07', .2);
  const cam = shots(t, [], [
    { t: 0, cx: 1060, cy: 600, z: 1.15, z2: 1.25 },
    { t: Lt('s17_07') - .1, cx: 1080, cy: 735, z: 3.6, z2: 3.8, lock: 1 },
    { t: Lt('s17_08') - .05, cx: 920, cy: 560, z: 2.1, lock: 1 },
    { t: Lt('s17_09') - .05, cx: 1080, cy: 735, z: 4.0, z2: 4.2, lock: 1 },
    { t: Lt('s17_10') - .05, cx: 1060, cy: 600, z: 1.3, z2: 1.45, lock: 1 },
  ]);
  const st = stage(cam); st.wld(g => { drawSet(g, 'parkNight'); bench(g, 0); });
  const chat = t < Lt('s17_07') - .1, yak = k => chat ? .2 + .3 * Math.abs(Math.sin(t * (9 + k)) * Math.sin(t * (2.1 + k))) : 0;
  const vp = { x: 1240, y: 905, s: S0, t, sit: 1, look: [-16, 2], mouth: .6, blush: .4, hL: [-40, -300], hR: [40, -300], armsFront: 1, open: yak(1) };
  const hp = { x: 900, y: 905, s: S0, t, sit: 1, look: [16, 2], mouth: .5, blush: .4, hL: [-40, -300], hR: [40, -300], armsFront: 1, open: yak(0) };
  if (t > turn) { vp.look = [-6, 18]; hp.look = [10, 18]; vp.wide = hp.wide = .6; vp.mouth = hp.mouth = -.1; }        // both look down at Pepe
  if (t > Lt('s17_08') - .05) { hp.open = talk(t, 's17_08'); hp.wide = .9; hp.brow = .8; }
  st.col(g => { drawChar(g, 'valeria', vp); drawChar(g, 'tu', hp); });
  st.wld(g => bench(g, 1));
  const front = t > turn, tilt = t > Lt('s17_09') ? Math.sin((t - Lt('s17_09')) * 3) * .12 : 0;
  st.col(g => drawPigeon(g, 1080, 792, .62, { flip: -1, front, tilt: front ? tilt : -.3 * R(t, turn - .3, turn) }));
  compose2(X, st, { amt: 1 });   // the park is frozen: only the three of them are in colour
  if (t > Lt('s17_05') - .05 && t < Lt('s17_07') - .1) { const [x1, y1] = worldToScreen(cam, 900, 470), [x2, y2] = worldToScreen(cam, 1240, 470);
    bubble(X, '…', x1, y1, R(t, Lm('s17_05', .2), Lm('s17_05', .2) + .25, outC), 54); bubble(X, '¡JA!', x2, y2, R(t, Lm('s17_05', .6), Lm('s17_05', .6) + .25, outC), 54); }
};

/* ================================================================ 18. ¿Algo de esto es real? (real science, Pepe presents) */
function boardClock(g, x, y, r, sec, label) {
  circ(g, x, y, r, '#fbfaf6', 5); g.save(); g.strokeStyle = '#2d2a40'; g.lineCap = 'round';
  for (let i = 0; i < 12; i++) { const a = i * Math.PI / 6; g.lineWidth = i % 3 ? 3 : 6; g.beginPath(); g.moveTo(x + Math.cos(a) * r * .8, y + Math.sin(a) * r * .8); g.lineTo(x + Math.cos(a) * r * .92, y + Math.sin(a) * r * .92); g.stroke(); }
  const a = -Math.PI / 2 + sec * Math.PI / 30; g.strokeStyle = '#c0262d'; g.lineWidth = 5; g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.cos(a) * r * .78, y + Math.sin(a) * r * .78); g.stroke();
  g.strokeStyle = '#2d2a40'; g.lineWidth = 8; g.beginPath(); g.moveTo(x, y); g.lineTo(x + r * .45, y - r * .2); g.stroke(); g.restore(); circ(g, x, y, 7, '#2d2a40', 0);
  if (label) text(g, label, x, y + r + 46, 40, '#2d2a40', 'ComicNeue', 'center');
}
SC.s18 = (X, t) => {
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 470, z: 1.12, z2: 1.16, lock: 1 },
    { t: Lt('s18_02') - .05, cx: 1010, cy: 400, z: 1.3, z2: 1.36, lock: 1 },
    { t: Lt('s18_04') - .05, cx: 1010, cy: 400, z: 1.32, z2: 1.36, lock: 1 },
    { t: Lt('s18_05') - .05, cx: 1010, cy: 400, z: 1.3, z2: 1.38, lock: 1 },
    { t: Lt('s18_08') - .05, cx: 960, cy: 480, z: 1.12, z2: 1.2, lock: 1 },
  ]);
  const st = stage(cam);
  st.wld(g => { drawSet(g, 'classroom'); teacherDesk(g, 1620);
    const a = k => clamp(k); g.save();
    text(g, '¿ALGO DE ESTO ES REAL?', 966, 205, 70, '#c0262d', 'Bangers', 'center');
    if (t > Lt('s18_02') - .1 && t < Lt('s18_04') - .1) {        // 1. chronostasis: the second hand seems to stop
      const s0 = Lt('s18_02'), hold = Lm('s18_02', .7), sec = t < hold ? Math.floor(t - s0) : Math.floor(hold - s0) + Math.floor(Math.max(0, t - hold - 1.4));
      boardClock(g, 640, 370, 115, sec, 'UNO');
      if (t > Lm('s18_02', .6)) { g.globalAlpha = a((t - Lm('s18_02', .6)) * 3); shape(g, q => q.ellipse(870, 300, 54, 30, 0, 0, 7), '#ffffff', 5); circ(g, 870 + Math.sin(t * 9) * 16, 300, 14, '#2d2a40', 0);
        line(g, [[815, 320], [770, 340]], '#3a6fb0', 5); g.globalAlpha = 1; }
      if (t > Lt('s18_03')) { g.globalAlpha = a((t - Lt('s18_03')) * 3); text(g, 'CRONOSTASIS', 990, 380, 64, '#3a6fb0', 'Bangers', 'left'); text(g, 'tu cerebro rellena', 990, 440, 36, '#2d2a40', 'ComicNeue', 'left'); text(g, 'el hueco', 990, 486, 36, '#2d2a40', 'ComicNeue', 'left'); g.globalAlpha = 1; } }
    if (t > Lt('s18_04') - .1 && t < Lt('s18_05') - .1) {        // 2. your body does not pause
      const beat = 1 + .12 * Math.pow(Math.max(0, Math.sin(t * Math.PI * 2.4)), 8);
      g.save(); g.translate(680, 350); g.scale(beat, beat); shape(g, q => { q.moveTo(0, 60); q.bezierCurveTo(-150, -30, -90, -150, 0, -80); q.bezierCurveTo(90, -150, 150, -30, 0, 60); }, '#e0485c', 6); g.restore();
      text(g, '100.000 latidos / día', 680, 490, 38, '#2d2a40', 'ComicNeue', 'center');
      if (t > Lm('s18_04', .55)) { g.globalAlpha = a((t - Lm('s18_04', .55)) * 3); shape(g, q => rrPath(q, 1060, 300, 60, 180, 6), '#f4e3b0', 4);
        for (let i = 0; i < 9; i++) line(g, [[1060, 310 + i * 19], [1080, 310 + i * 19]], '#2d2a40', 3);
        g.strokeStyle = '#2b1a1f'; g.lineWidth = 6; g.beginPath(); g.moveTo(1140, 470); g.quadraticCurveTo(1160, 400, 1145, 470 - 160 * a((t - Lm('s18_04', .55)) * 1.2)); g.stroke();
        text(g, '+0,5 mm / día', 1190, 400, 40, '#2d2a40', 'ComicNeue', 'left'); g.globalAlpha = 1; } }
    if (t > Lt('s18_05') - .1 && t < Lt('s18_08') - .1) {        // 3. your head is older than your feet
      g.strokeStyle = '#2d2a40'; g.lineWidth = 7; g.lineCap = 'round'; circ(g, 560, 300, 34, '#fbfaf6', 6);
      g.beginPath(); g.moveTo(560, 334); g.lineTo(560, 440); g.moveTo(560, 365); g.lineTo(515, 410); g.moveTo(560, 365); g.lineTo(605, 410); g.moveTo(560, 440); g.lineTo(525, 520); g.moveTo(560, 440); g.lineTo(595, 520); g.stroke();
      boardClock(g, 700, 310, 50, (t - Lt('s18_05')) * 1.06); boardClock(g, 700, 480, 50, (t - Lt('s18_05')));
      text(g, 'más rápido', 765, 322, 30, '#c0262d', 'ComicNeue', 'left'); text(g, 'más lento', 765, 492, 30, '#3a6fb0', 'ComicNeue', 'left');
      if (t > Lt('s18_06') - .1) { g.globalAlpha = a((t - Lt('s18_06')) * 3); text(g, 'RELOJES ATÓMICOS · 2010', 990, 300, 44, '#3a6fb0', 'Bangers', 'left'); g.globalAlpha = 1; }
      if (t > Lt('s18_07') - .1) { g.globalAlpha = a((t - Lt('s18_07')) * 3); text(g, '30 cm más arriba =', 990, 380, 36, '#2d2a40', 'ComicNeue', 'left'); text(g, '+90 milmillonésimas', 990, 428, 36, '#c0262d', 'ComicNeue', 'left'); text(g, 'de segundo en 79 años', 990, 474, 32, '#2d2a40', 'ComicNeue', 'left'); g.globalAlpha = 1; } }
    if (t > Lt('s18_08') - .1) { g.globalAlpha = a((t - Lt('s18_08')) * 2); text(g, 'EL TIEMPO NUNCA PASA', 966, 340, 72, '#2d2a40', 'Bangers', 'center'); text(g, 'IGUAL PARA TODOS', 966, 430, 72, '#2d2a40', 'Bangers', 'center'); g.globalAlpha = 1; }
    g.restore(); });
  // Pepe presents from the teacher's desk, looking at us
  const nod = Math.sin(t * 2.2) * .06 + (t > Lt('s18_08') ? .2 * bump(t, Lt('s18_08') + .4, Lt('s18_08') + 1.1) : 0);
  st.col(g => drawPigeon(g, 1600, 692, .95, { flip: -1, front: 1, tilt: nod }));
  compose2(X, st, { amt: 0 });
};

/* ================================================================ 19. call to action, end card */
SC.s19 = (X, t) => {
  const end = Le('s19_05') + .9;
  const cam = shots(t, [], [{ t: 0, cx: 1060, cy: 600, z: 1.25, z2: 1.35, lock: 1 }, { t: Lt('s19_05') - .1, cx: 1080, cy: 735, z: 3.6, z2: 3.8, lock: 1 }]);
  const st = stage(cam); st.wld(g => { drawSet(g, 'parkNight'); bench(g, 0); });
  st.col(g => { drawChar(g, 'valeria', { x: 1240, y: 905, s: S0, t, sit: 1, look: [-14, 4], mouth: .6, hL: [-40, -300], hR: [40, -300], armsFront: 1 });
    drawChar(g, 'tu', { x: 900, y: 905, s: S0, t, sit: 1, look: [14, 4], mouth: .4, blush: .5, hL: [-40, -300], hR: [40, -300], armsFront: 1 }); });
  st.wld(g => bench(g, 1));
  st.col(g => drawPigeon(g, 1080, 792, .62, { flip: -1, front: 1, tilt: Math.sin(t * 1.3) * .08 }));
  compose2(X, st, { amt: 0 });
  if (t > Lt('s19_01') - .05 && t < Lt('s19_04') - .1) sticker(X, '¿QUÉ HARÍAS TÚ?', R(t, Lt('s19_01') - .05, Lt('s19_01') + .25, outC), 70, 60, 70);
  if (t > Lt('s19_02') - .05 && t < Lt('s19_03') - .1) sticker(X, '↓ COMENTARIOS ↓', R(t, Lt('s19_02') - .05, Lt('s19_02') + .25, outC), 70, 180, 60, '#ffffff');
  if (t > Lt('s19_03') - .05 && t < Lt('s19_04') - .1) {   // inset: the blink from the cold open
    const a = R(t, Lt('s19_03') - .05, Lt('s19_03') + .3, back), keep = SID, LX = layer('INSET');
    const b0 = TIM.scenes.s00.L.s00_02[0] + TIM.scenes.s00.L.s00_02[1] * .55, loop = ((t - Lt('s19_03')) * .8) % 1;
    SID = 's00'; SC.s00(LX, b0 - .15 + loop * .55); const c0 = window.__cam; SID = keep; const [fx, fy] = worldToScreen(c0, 1400, 520);
    X.save(); X.translate(1300, 360); X.scale(a, a); shape(X, q => rrPath(q, -330, -195, 660, 390, 18), '#fde047', 8);
    X.drawImage(LX.canvas, fx - 300, fy - 170, 600, 338, -310, -175, 620, 350); X.restore();
    sticker(X, '¿VISTE EL PARPADEO?', a, 1010, 600, 56); }
  if (t > Lm('s19_04', .6) && t < Lt('s19_05') - .1) { const a = R(t, Lm('s19_04', .6), Lm('s19_04', .6) + .3, back); X.save(); X.translate(W / 2, H - 200); X.scale(a, a); shape(X, q => rrPath(q, -260, -60, 520, 120, 20), '#e02424', 6); text(X, 'SUSCRÍBETE', 0, 26, 76, '#ffffff', 'Bangers', 'center'); X.restore(); }
  if (t > end) { const a = R(t, end, end + .5, outC); X.save(); X.globalAlpha = a; X.fillStyle = '#141a2e'; X.fillRect(0, 0, W, H);
    text(X, CHANNEL_NAME, W / 2, 230, 150, '#fde047', 'Bangers', 'center', OUT, 18);
    text(X, 'PRÓXIMO EPISODIO:', W / 2, 400, 64, '#ffffff', 'Bangers', 'center');
    text(X, '¿Y SI PUDIERAS VER', W / 2, 500, 84, '#ffffff', 'Bangers', 'center', OUT, 10); text(X, '5 SEGUNDOS DEL FUTURO?', W / 2, 600, 84, '#ffffff', 'Bangers', 'center', OUT, 10);
    shape(X, q => rrPath(q, W / 2 - 300, 720, 600, 130, 22), '#e02424', 7); text(X, 'SUSCRÍBETE', W / 2, 812, 84, '#ffffff', 'Bangers', 'center');
    drawPigeon(X, 1600, 960, .9, { flip: -1, front: 1, tilt: Math.sin(t * 1.5) * .1 }); X.restore(); }
};
