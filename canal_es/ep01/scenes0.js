/* Ep01 scene 0: cold open in media res. The pot hangs over Valeria's head, the world is frozen,
   the hero runs in; "Empecemos por el principio" rewinds the tape back to the start. */
function rewindFX(X, k, t) { if (k <= 0) return;
  X.save(); X.globalAlpha = .25 * k; X.fillStyle = '#ffffff'; const r = rnd(Math.floor(t * 30));
  for (let i = 0; i < 9; i++) { const y = r() * H, h = 4 + r() * 18; X.fillRect(0, y, W, h); } X.restore();
  X.save(); X.globalAlpha = .55 * k; X.fillStyle = '#0d0b12'; X.fillRect(0, H - 150, W, 150); X.restore();
  X.save(); X.globalAlpha = k; text(X, '◀◀  REBOBINANDO', 70, H - 52, 76, '#ffffff', 'Bangers', 'left', OUT, 10); X.restore(); }
SC.s00 = (X, t) => {
  const run0 = Lt('s00_03') - .2, run1 = Le('s00_03') + .3, rw = Lm('s00_05', .5);
  // the hero's path; after `rw` it plays backwards fast (the rewind)
  const path = tt => mix(-80, 1240, R(tt, run0, run1, outC));
  const tr = t < rw ? t : Math.max(0, rw - (t - rw) * 4);
  const hx = path(tr), running = tr > run0 && tr < run1;
  const cam = shots(t, [], [
    { t: 0, cx: 1400, cy: 330, z: 2.3, z2: 2.55, lock: 1 },
    { t: Lt('s00_02') - .05, cx: 960, cy: 540, z: 1.0, z2: 1.04, lock: 1 },
    { t: run0 + .1, cx: tt => path(tt < rw ? tt : Math.max(0, rw - (tt - rw) * 4)) + 220, cy: 560, z: 1.35, lock: 1 },
    { t: Lt('s00_04') - .05, cx: 1260, cy: 420, z: 2.3, z2: 2.45, lock: 1 },
    { t: rw, cx: 960, cy: 540, z: 1.0, lock: 1 },
  ]);
  const st = stage(cam); st.wld(g => drawSet(g, 'street'));
  const fr = { still: 1, t: 0, blink: 0, s: S0, y: FEET };
  st.wld(g => { drawChar(g, 'ex3', { ...fr, x: 420, walk: 1, phase: .9, look: [10, 0], mouth: .2 }); drawChar(g, 'ex2', { ...fr, x: 760, walk: 1, phase: 2.4, flip: -1, look: [-10, 4], open: .4 }); });
  const vblink = bump(t, Lm('s00_02', .55), Lm('s00_02', .55) + .22);   // on 'el mundo entero está congelado'   // clue: she blinks (rewatch payoff in s19_03)
  st.wld(g => drawChar(g, 'valeria', { ...fr, x: 1400, look: [4, 18], mouth: .1, blink: vblink, hR: [20, -380], holdR: (q, x, y) => propPhone(q, x, y - 40, .55, 76, -.1) }));
  st.wld(g => propPot(g, 1400, 349, .7, 0));
  st.col(g => drawPigeon(g, 1700, 170, .5, { flip: -1, tilt: .25 * bump(t, Lt('s00_04'), Lt('s00_04') + 1.2) }));   // clue: Pepe never turns grey
  // the hero: runs in, stops, looks up at the pot, sweating
  const hp = { x: hx, y: FEET, s: S0, t, walk: running ? 1 : 0, phase: walkPh(hx) * 1.9, lean: running ? .14 : 0, look: [16, -6], mouth: -.3, brow: .7, wide: .5, sweat: tr > run1 ? 1 : 0 };
  if (t >= rw) hp.lean = running ? -.14 : 0;
  if (tr > run1) { hp.look = [8, -22]; hp.hR = [150, -560]; hp.open = .4; }
  st.col(g => drawChar(g, 'tu', hp));
  compose2(X, st, { amt: 1 });
  if (running && t < rw) speedLines(X, ...worldToScreen(cam, hx, 600), .6, t);
  if (t < Lt('s00_02') - .05) sticker(X, '50 cm', R(t, Le('s00_01') - .6, Le('s00_01') - .3, outC), 1230, 360, 70);
  rewindFX(X, R(t, rw, rw + .25), t);
  if (t > T().dur - .25) { X.save(); X.globalAlpha = R(t, T().dur - .25, T().dur, lin); X.fillStyle = '#ffffff'; X.fillRect(0, 0, W, H); X.restore(); }
};
