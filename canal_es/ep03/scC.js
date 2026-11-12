/* Ep03 scenes 11–17: animals keep no secrets, Canela, the choice, Renata, Pepe speaks, the science, the end card. */
const CHANNEL_NAME = 'PONLE QUE…';
function dashRing(X, x, y, r, t, col = '#ffd34d') { X.save(); X.strokeStyle = col; X.lineWidth = 8; X.setLineDash([22, 16]); X.lineDashOffset = -t * 60; X.beginPath(); X.arc(x, y, r, 0, 7); X.stroke(); X.restore(); }
function leash(g, a, b) { g.save(); g.strokeStyle = '#e0457b'; g.lineWidth = 5; g.lineCap = 'round'; g.beginPath(); g.moveTo(a[0], a[1]); g.quadraticCurveTo((a[0] + b[0]) / 2, Math.max(a[1], b[1]) + 60, b[0], b[1]); g.stroke(); g.restore(); }
/* a comic panel showing a little world (world coords 0..1920 x 0..1080 scaled into the box) */
/* a 16:9 comic panel: the little world (view cx, cy, z) is drawn in its own layer, then placed at x, y, w wide.
   Returns the camera that maps that world onto the screen, for bubbles drawn over the panel (the small tilt is ignored). */
function panel(X, x, y, w, a, draw, rot = 0, v = { cx: W / 2, cy: H / 2, z: 1 }) { if (a <= 0) return null;
  const P = layer('PANEL'), zc = window.__camz; window.__camz = 1;   // no depth-of-field blur inside a panel
  P.setTransform(v.z, 0, 0, v.z, W / 2 - v.cx * v.z, H / 2 - v.cy * v.z); draw(P); P.setTransform(1, 0, 0, 1, 0, 0); window.__camz = zc;
  const h = w * 9 / 16, s = .85 + .15 * back(a);
  X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.filter = 'none'; X.globalCompositeOperation = 'source-over'; X.globalAlpha = clamp(a);
  X.translate(x + w / 2, y + h / 2); X.rotate(rot); X.scale(s, s); X.translate(-w / 2, -h / 2);
  X.fillStyle = '#ffffff'; X.fillRect(-12, -12, w + 24, h + 24); X.drawImage(P.canvas, 0, 0, W, H, 0, 0, w, h);
  X.lineWidth = 8; X.strokeStyle = '#141014'; X.strokeRect(-12, -12, w + 24, h + 24); X.restore();
  const k = v.z * w / W; return { cx: v.cx - (x + w / 2 - W / 2) / k, cy: v.cy - (y + h / 2 - H / 2) / k, z: k }; }
/* the hero, fading in and out: tomorrow nobody will see you */
function flickerAlpha(t, t0, k = 1) { if (t < t0) return 1; const u = t - t0; return 1 - k * (.55 + .45 * Math.sin(u * 23) * Math.sin(u * 7.1)) * R(t, t0, t0 + .3); }

/* ================================================================ 11. animals keep no secrets */
SC.s11 = (X, t) => {
  const p1 = Lt('s11_03') - .1, p2 = Lt('s11_04') - .1, p3 = Lt('s11_05') - .1, full = Lt('s11_06') - .1, rule = Lt('s11_07') - .2;
  const cam = { cx: 960, cy: 540, z: 1 };
  const st = stage(cam); st.wld(g => drawSet(g, 'street'));
  if (t > full) {   // panel 3 at full size: Croqueta on the fence, telling the whole street
    const c2 = shots(t, [], [{ t: full, cx: 1100, cy: 640, z: 1.6, z2: 1.7, lock: 1 }, { t: rule, cx: 960, cy: 560, z: 1.0, lock: 1 }]); Object.assign(cam, c2);
    const s2 = stage(cam); s2.wld(g => { drawSet(g, 'street'); fence(g, 900, 1500, 960, 140); });
    let mC = null;
    s2.col(g => { mC = drawAnimal(g, 'croqueta', 1200, 830, .8, { head: 'bored', t, open: openOf(t, ['s11_06']), tilt: Math.sin(t * 1.4) * .05 });
      drawAnimal(g, 'dogA', 1000, 1010, .85, { t, tilt: .2 }); drawAnimal(g, 'dogB', 1420, 1010, .8, { t, tilt: -.25 }); drawAnimal(g, 'firu', 1650, 1000, .8, { t, tilt: -.1 }); });
    s2.col(g => drawChar(g, 'tu', standing(560, { t, look: [16, 2], mouth: -.3, blush: 1, brow: .7, hR: [70, -640] })));
    compose2(X, s2, { amt: 0 });
    say(X, cam, t, 's11_06', mC, { dx: -1, r: 80 });
    if (t > Le('s11_06')) comicWord(X, '¡¿3 VECES?!', ...worldToScreen(cam, 1100, 430), (t - Le('s11_06')) * .8, 80);
    ruleCard(X, 2, 'LOS ANIMALES NO MIENTEN.', 'Y NO GUARDAN SECRETOS.', R(t, rule, rule + .4, outC));
    return;
  }
  st.col(g => drawChar(g, 'tu', standing(960, { t, look: [0, 4], mouth: -.1, brow: .4 })));
  compose2(X, st, { amt: 0 });
  X.save(); X.fillStyle = 'rgba(20,16,30,.55)'; X.fillRect(0, 0, W, H); X.restore();
  if (t < p1) { sticker(X, 'SECRETOS DEL BARRIO', R(t, Lt('s11_02'), Lt('s11_02') + .25, back), 620, 460, 84); return; }
  // three panels pile up like cards: 1. doña Lupe talks to her plants (her dog tells you)
  let m1 = null, m2 = null;
  const c1 = panel(X, 70, 60, 1000, R(t, p1, p1 + .3, outC), g => { drawSet(g, 'park');
    drawSpr(g, 'plant', 1020, 950, 340); drawSpr(g, 'plant', 1280, 960, 260, { flip: -1 });
    m1 = drawAnimal(g, 'dogB', 620, 1010, 1.4, { t, open: t < Lt('s11_04') ? Math.abs(Math.sin(t * 10)) * .6 : 0, tilt: .2 }); }, -.03, { cx: 900, cy: 760, z: 1.55 });
  if (c1 && t > p1 + .5 && t < p2) gag(X, c1, t, m1, p1 + .5, 1.6, 'GUAU', 'Les habla a sus plantas.', { size: 40, w: 380, r: 120, dx: 1 });
  // 2. profe Ramírez sings in the shower (his cat tells you)
  const c2 = panel(X, 470, 250, 1000, R(t, p2, p2 + .3, outC), g => { drawSet(g, 'bathroom');
    drawChar(g, 'profe', { x: 960, y: FEET, s: S0, t, key: 'panel', look: [0, -10], open: .3 + .5 * Math.abs(Math.sin(t * 5)), lid: 1, hR: [150, -620], hL: [-150, -620] }); notes(g, 1160, 330, t, 1);
    g.save(); g.filter = 'grayscale(1) brightness(1.2)'; m2 = drawAnimal(g, 'croqueta', 560, 990, 1.3, { head: 'wide', t, open: t < p3 ? Math.abs(Math.sin(t * 9)) * .6 : 0 }); g.restore(); }, .025, { cx: 820, cy: 640, z: 1.45 });
  if (c2 && t > p2 + .5 && t < p3) gag(X, c2, t, m2, p2 + .5, 1.6, 'MIAU', 'Canta en la regadera.', { size: 40, w: 380, r: 120, dx: -1 });
  // 3. Croqueta tells the whole street what you say in your sleep
  panel(X, 850, 420, 1000, R(t, p3, p3 + .3, outC), g => { drawSet(g, 'street'); fence(g, 700, 1300, 960, 140);
    drawAnimal(g, 'croqueta', 1000, 830, 1.0, { head: 'bored', t, open: Math.abs(Math.sin(t * 8)) * .5 }); drawAnimal(g, 'dogA', 700, 1010, 1.0, { t, tilt: .2 }); drawAnimal(g, 'dogB', 1300, 1010, .95, { t, tilt: -.2 });
    drawChar(g, 'tu', standing(380, { t, key: 'panel', look: [16, 2], mouth: -.3, sweat: 1 })); }, -.02, { cx: 900, cy: 720, z: 1.4 });
};

/* ================================================================ 12. Canela runs to you */
SC.s12 = (X, t) => {
  const free = Lt('s12_02') + .1, arrive = Le('s12_02') + .3, cut = Lm('s12_05', .98);
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 560, z: 1.0, z2: 1.06, lock: 1 },
    { t: Lt('s12_02') - .05, cx: 1200, cy: 640, z: 1.3, z2: 1.35, lock: 1 },
    { t: Lt('s12_03') - .05, cx: 1000, cy: 800, z: 2.5, z2: 2.6, lock: 1 },
    { t: Lt('s12_04') - .05, cx: 780, cy: 480, z: 2.0, z2: 2.1, lock: 1 },
    { t: Lt('s12_05') - .05, cx: 1000, cy: 820, z: 2.7, z2: 3.0, lock: 1 },
    { t: Lt('s12_06') - .05, cx: 900, cy: 620, z: 1.5, z2: 1.7, lock: 1 },
    { t: Lt('s12_07') - .05, cx: 900, cy: 520, z: 2.8, z2: 3.2, lock: 1 },
  ]);
  const st = stage(cam); st.wld(g => { drawSet(g, 'park'); bench(g, 0); bench(g, 1); });
  // Renata far back with the leash: Canela slips it and runs
  const rx = mix(2050, 1600, R(t, 0, free, io)), rp = { x: rx, y: 860, s: .62, t, flip: -1, walk: t < free ? 1 : 0, phase: walkPh(rx), look: [-14, 4], mouth: .2, hR: [110, -380] };
  if (t > free) { rp.wide = .7; rp.open = .5; rp.hR = [170, -560]; rp.jump = 8 * Math.abs(Math.sin(t * 6)); }
  st.wld(g => drawChar(g, 'valeria', rp));
  const hp = standing(760, { t, look: [16, 6], mouth: .3 });
  if (t > arrive) { hp.look = [16, 16]; hp.mouth = .6; }
  if (speaking(t, 's12_04')) { hp.open = talk(t, 's12_04'); hp.wide = .5; hp.brow = .5; hp.look = [16, 14]; }
  if (t > Le('s12_04')) { hp.look = [16, 16]; hp.wide = .6; hp.mouth = -.1; hp.blush = .6; }
  if (t > Lt('s12_07')) { hp.hR = [160, -640]; hp.lean = .06; }   // a hand to the ear: all you have to do is listen
  st.col(g => drawChar(g, 'tu', hp));
  let mC = null;
  st.col(g => { if (t < free) { drawAnimal(g, 'canela', rx - 140, 870, .55, { t, flip: -1 }); leash(g, [rx - 60, 860 - 290 * .62], [rx - 140, 870 - 90]); }
    else if (t < arrive) { const x = mix(rx - 140, 1000, R(t, free, arrive, lin)), y = mix(870, 1000, R(t, free, arrive, lin)); drawSpr(g, 'canelaRun', x, y, mix(80, 130, R(t, free, arrive, lin)), { flip: 1, bob: -Math.abs(Math.sin(t * 13)) * 12 }); }
    else { const frz = t > cut && t < Lt('s12_07') + 2; mC = drawAnimal(g, 'canela', 1000, 1000, 1.0, { t, open: frz ? .7 : openOf(t, ['s12_03', 's12_05']), tilt: frz ? .1 : Math.sin(t * 4) * .1, bob: frz ? 0 : -Math.abs(Math.sin(t * 9)) * 5 }); } });
  compose2(X, st, { amt: 0 });
  say(X, cam, t, 's12_03', mC, { dx: 1, r: 80 }); say(X, cam, t, 's12_05', mC, { dx: 1, r: 80, hold: 3.5 });
  if (t > cut) { X.save(); X.globalAlpha = R(t, cut, cut + .3) * .35; X.fillStyle = '#ffd34d'; X.fillRect(0, 0, W, H); X.restore();
    sticker(X, 'TODO LO QUE RENATA PIENSA DE TI', R(t, Lt('s12_06'), Lt('s12_06') + .25, back) * (1 - R(t, Lt('s12_07'), Lt('s12_07') + .2)), 360, 90, 66, '#ffffff'); }
  if (t > Lt('s12_07')) { const [x, y] = worldToScreen(cam, 830, 300); soundRings(X, x, y, 1, t, 1); }
};

/* ================================================================ 13. the choice: what you tell Croqueta at night */
SC.s13 = (X, t) => {
  const back0 = Lt('s13_04') - .1;
  const cam = shots(t, [], [
    { t: 0, cx: 900, cy: 560, z: 1.3, z2: 1.4, lock: 1 },
    { t: back0, cx: 860, cy: 600, z: 1.5, z2: 1.55, lock: 1 },
    { t: Lt('s13_05') - .05, cx: 1000, cy: 820, z: 2.6, z2: 2.7, lock: 1 },
    { t: Lt('s13_06') - .05, cx: 800, cy: 500, z: 2.1, z2: 2.25, lock: 1 },
  ]);
  const st = stage(cam); st.wld(g => { drawSet(g, 'park'); bench(g, 0); bench(g, 1); });
  const hp = standing(760, { t, look: [16, 14], mouth: -.1, brow: .5 });
  if (t < back0) { hp.look = [-8, -12]; hp.brow = .6; hp.mouth = -.2; }
  if (speaking(t, 's13_04')) { hp.open = talk(t, 's13_04'); hp.hR = [190, -420]; hp.look = [16, 16]; hp.hy = 30; }
  if (t > Le('s13_04') && t < Lt('s13_06')) { hp.hR = [190, -420]; hp.look = [16, 16]; }
  if (speaking(t, 's13_06')) { hp.open = talk(t, 's13_06'); hp.look = [16, 14]; hp.brow = -.2; hp.hR = [120, -470]; }
  if (t > Le('s13_06')) { hp.mouth = .5; hp.brow = -.1; }
  st.col(g => drawChar(g, 'tu', hp));
  let mC = null; st.col(g => { mC = drawAnimal(g, 'canela', 1000, 1000, 1.0, { t, open: openOf(t, ['s13_05']), tilt: t > Lt('s13_05') ? -.18 : .1 }); });
  compose2(X, st, { amt: 0 });
  // memory panel: you, at night, telling Croqueta everything
  if (t < back0) { const a = R(t, .2, .6, outC) * (1 - R(t, back0 - .3, back0));
    panel(X, 1040, 110, 780, a, g => { drawSet(g, 'bedroom'); bedBack(g);
      drawChar(g, 'tu', { x: 640, y: FEET, s: S0, t, key: 'panel', look: [16, 12], open: Math.abs(Math.sin(t * 6)) * .5, blush: .7, hL: [-70, -380], hR: [80, -380] }); bedFront(g, .6);
      drawAnimal(g, 'croqueta', 420, 716, .9, { head: 'wide', t, tilt: .15 });
      for (let i = 0; i < 4; i++) heartPop(g, 700 + i * 70, 330, loopU(t, i * .35, 1.4), 1.4);
      nightTint(g, .6); }, .02, { cx: 760, cy: 600, z: 1.25 });
    if (t > Lt('s13_03')) { const a3 = R(t, Lt('s13_03'), Lt('s13_03') + .3, back) * (1 - R(t, back0 - .3, back0)); sticker(X, '¿Y SI LO SUPIERA TODO EL MUNDO?', a3, 980, 620, 54, '#ffffff'); } }
  say(X, cam, t, 's13_05', mC, { dx: 1, r: 80 });
  if (t > Lt('s13_04') && t < Lt('s13_05')) sticker(X, 'NO ME LO DIGAS', R(t, Lt('s13_04') + .3, Lt('s13_04') + .5, back), 90, 90, 70, '#ffffff');
};

/* ================================================================ 14. Renata: some things you hear from the person */
SC.s14 = (X, t) => {
  const arrive = Lt('s14_02') - .1, rule = Lt('s14_09') - .2, yay = Lt('s14_11') - .1;
  const cam = shots(t, [], [
    { t: 0, cx: 1000, cy: 560, z: 1.1, z2: 1.15, lock: 1 },
    { t: arrive, cx: 1060, cy: 470, z: 1.6, z2: 1.65, lock: 1 },
    { t: Lt('s14_03') - .05, cx: 800, cy: 450, z: 2.0, z2: 2.1, lock: 1 },
    { t: Lt('s14_04') - .05, cx: 1180, cy: 430, z: 2.2, z2: 2.3, lock: 1 },
    { t: Lt('s14_05') - .05, cx: 1000, cy: 520, z: 1.4, z2: 1.5, lock: 1 },
    { t: Lt('s14_06') - .05, cx: 1180, cy: 440, z: 2.1, z2: 2.25, lock: 1 },
    { t: Lt('s14_08') - .05, cx: 820, cy: 450, z: 2.1, z2: 2.2, lock: 1 },
    { t: rule, cx: 1000, cy: 560, z: 1.1, lock: 1 },
    { t: yay, cx: 1000, cy: 800, z: 2.2, z2: 2.3, lock: 1 },
  ]);
  const st = stage(cam); st.wld(g => { drawSet(g, 'park'); bench(g, 0); bench(g, 1); });
  const rx = mix(2100, 1220, R(t, 0, arrive, io)), rp = { x: rx, y: FEET, s: S0, t, flip: -1, walk: t < arrive ? 1.3 : 0, phase: walkPh(rx) * 1.4, look: [-14, 4], mouth: .3, hR: [110, -380] };
  if (speaking(t, 's14_02')) { rp.open = talk(t, 's14_02'); rp.brow = .5; rp.sweat = 1; }
  if (speaking(t, 's14_04')) { rp.open = talk(t, 's14_04'); rp.brow = .9; rp.lid = .2; }
  if (t > Le('s14_04') && t < Lt('s14_06')) { rp.brow = .8; rp.mouth = -.1; rp.lid = .2; }
  if (t > Lt('s14_06')) { rp.mouth = .6; rp.blush = .6; rp.look = [-14, 6]; }
  if (speaking(t, 's14_06') || speaking(t, 's14_07')) rp.open = talk(t, speaking(t, 's14_06') ? 's14_06' : 's14_07');
  if (t > Lt('s14_07')) { rp.blush = 1; rp.look = [-16, 10]; rp.hL = [-60, -330]; }
  st.wld(g => drawChar(g, 'valeria', rp));
  const hp = standing(760, { t, look: [16, 4], mouth: .2 });
  if (speaking(t, 's14_03')) { hp.open = talk(t, 's14_03'); hp.hR = [140, -560]; hp.look = [16, -6]; }
  if (t > Lt('s14_04') && t < Lt('s14_06')) { hp.sweat = 1; hp.mouth = -.3; hp.brow = .7; hp.wide = .4; }
  if (t > Lt('s14_06')) { hp.mouth = .4; hp.blush = .5; hp.brow = 0; }
  if (speaking(t, 's14_08')) { hp.open = talk(t, 's14_08'); hp.blush = .9; }
  if (t > Le('s14_08')) { hp.mouth = 1; hp.blush = .9; }
  st.col(g => drawChar(g, 'tu', hp));
  let mC = null; st.col(g => { const hop = t > yay ? Math.abs(Math.sin(t * 9)) * 40 : 0; mC = drawAnimal(g, 'canela', 1000, 1000 - hop, 1.0, { t, open: openOf(t, ['s14_11']), tilt: Math.sin(t * 3) * .1 }); leash(g, [rx - 100, FEET - 380 * S0], animalMouthAt('canela', 1000, 1000 - hop, 1.0).map((v, i) => v + (i ? 70 : 0))); });
  compose2(X, st, { amt: 0 });
  if (t > Lt('s14_07') && t < rule) for (let i = 0; i < 5; i++) { const [x, y] = worldToScreen(cam, 900 + i * 60, 360); const u = loopU(t, Lt('s14_07') + i * .3, 1.6); if (u > 0 && u < 1) { X.save(); X.globalAlpha = 1 - u; text(X, '♥', x, y - u * 100, 50, '#ff5d7a', 'Bangers', 'center'); X.restore(); } }
  ruleCard(X, 3, 'HAY COSAS QUE TIENES QUE ESCUCHAR', t > Lt('s14_10') - .1 ? 'DE LA PERSONA. NO DE SU PERRO.' : 'DE LA PERSONA.', R(t, rule, rule + .4, outC) * (1 - R(t, yay - .3, yay)));
  say(X, cam, t, 's14_11', mC, { dx: 1, r: 80 });
};

/* ================================================================ 15. night bench: Pepe speaks */
SC.s15 = (X, t) => {
  const beak = Lt('s15_05') + .3, fade = Lt('s15_10') + .2;
  const cam = shots(t, [], [
    { t: 0, cx: 980, cy: 640, z: 1.3, z2: 1.35, lock: 1 },
    { t: Lt('s15_02') - .05, cx: 990, cy: 650, z: 1.6, z2: 1.65, lock: 1 },
    { t: Lt('s15_03') - .05, cx: 1080, cy: 740, z: 2.6, z2: 2.7, lock: 1 },
    { t: Lt('s15_04') - .05, cx: 920, cy: 540, z: 2.4, z2: 2.5, lock: 1 },
    { t: Lt('s15_05') - .05, cx: 1080, cy: 730, z: 3.0, z2: 3.6, lock: 1 },
    { t: Lt('s15_07') - .05, cx: 900, cy: 520, z: 2.6, z2: 2.7, lock: 1 },
    { t: Lt('s15_08') - .05, cx: 1080, cy: 730, z: 3.4, z2: 3.6, lock: 1 },
    { t: Lt('s15_09') - .05, cx: 990, cy: 640, z: 1.6, z2: 1.7, lock: 1 },
    { t: Lt('s15_10') - .05, cx: 1080, cy: 730, z: 3.2, z2: 3.6, lock: 1 },
    { t: Lt('s15_11') - .05, cx: 920, cy: 560, z: 2.0, z2: 2.1, lock: 1 },
    { t: Lt('s15_12') - .05, cx: 1080, cy: 730, z: 3.6, z2: 4.0, lock: 1 },
  ]);
  const st = stage(cam); st.wld(g => { drawSet(g, 'parkNight'); bench(g, 0); bench(g, 1); });
  const hp = benchSit(900, { t, look: [14, 6], mouth: .3, open: t < Lt('s15_03') ? Math.abs(Math.sin(t * 7)) * .4 : 0 });
  if (speaking(t, 's15_04')) { hp.open = talk(t, 's15_04'); hp.look = [16, 8]; hp.mouth = .1; }
  if (t > beak) { hp.open = 0; hp.wide = 1; hp.mouth = -.1; hp.brow = .9; hp.look = [16, 8]; }
  if (speaking(t, 's15_07')) hp.open = talk(t, 's15_07');
  if (speaking(t, 's15_11')) { hp.open = talk(t, 's15_11'); hp.lean = .06; }
  if (t > fade && t < Lt('s15_11')) { hp.look = [-4, 20]; hp.hR = [60, -330]; }   // looks at his own hand: it flickers
  const ha = flickerAlpha(t, fade, .8) * (t > Lt('s15_11') ? 1 : 1);
  st.col(g => { g.save(); g.globalAlpha = t > fade && t < Lt('s15_11') ? ha : 1; drawChar(g, 'tu', hp); g.restore(); });
  let mP = null; st.col(g => { mP = pigeonTalk(g, 1080, 792, .62, { flip: -1, front: t > Lt('s15_04'), open: openOf(t, ['s15_06', 's15_08', 's15_10', 's15_12']), tilt: Math.sin(t * 1.1) * .04 }); });
  compose2(X, st, { amt: 0 });
  if (t > Lt('s15_02') && t < Lt('s15_03')) { const items = ['croqueta', 'hamster', 'canela']; items.forEach((k, i) => { const a0 = Lm('s15_02', .25 + i * .25); if (t > a0) { const a = R(t, a0, a0 + .25, back), [x, y] = [560 + i * 400, 200];
      X.save(); X.globalAlpha = a; X.translate(x, y); X.scale(a, a); circ(X, 0, 0, 90, '#ffffff', 6); X.save(); X.beginPath(); X.arc(0, 0, 84, 0, 7); X.clip(); const [ay, as] = { croqueta: [150, .7], hamster: [150, 1.3], canela: [178, 1.05] }[k]; drawAnimal(X, k, 0, ay, as, { t }); X.restore(); X.restore(); } }); }
  // Pepe's words: golden, no scramble needed: he speaks perfect Spanish
  for (const id of ['s15_06', 's15_08', 's15_10', 's15_12']) say(X, cam, t, id, mP, { dx: 1, r: 40, size: 64, w: 760 });
  if (t > beak - .3 && t < Lt('s15_06')) { const [px, py] = worldToScreen(cam, 1080, 735); dashRing(X, px, py, 70 * cam.z, t); }
  if (t > Le('s15_12') + .3) { X.save(); X.globalAlpha = R(t, Le('s15_12') + .3, T().dur, lin); X.fillStyle = '#000'; X.fillRect(0, 0, W, H); X.restore(); }
};

/* ================================================================ 16. is any of this real? */
function chip(g, s, x, y, a, col = '#ffd34d') { if (a <= 0) return; g.save(); g.globalAlpha = clamp(a); g.font = '48px Bangers'; const w = g.measureText(s).width + 40; g.translate(x, y); g.scale(.8 + .2 * back(a), .8 + .2 * back(a));
  shape(g, q => rrPath(q, -w / 2, -36, w, 72, 16), col, 5); text(g, s, 0, 18, 48, '#141014', 'Bangers', 'center'); g.restore(); }
SC.s16 = (X, t) => {
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 470, z: 1.12, z2: 1.16, lock: 1 },
    { t: Lt('s16_02') - .05, cx: 960, cy: 440, z: 1.2, z2: 1.26, lock: 1 },
    { t: Lt('s16_05') - .05, cx: 960, cy: 440, z: 1.2, z2: 1.26, lock: 1 },
    { t: Lt('s16_07') - .05, cx: 1010, cy: 430, z: 1.2, z2: 1.28, lock: 1 },
    { t: Lt('s16_09') - .05, cx: 1420, cy: 560, z: 1.9, z2: 2.0, lock: 1 },
  ]);
  const ink = '#2d2a40', red = '#c0262d', blue = '#3a6fb0';
  const st = stage(cam);
  st.wld(g => { drawSet(g, 'classroom'); teacherDesk(g, 1620);
    text(g, '¿ALGO DE ESTO ES REAL?', 966, 205, 70, red, 'Bangers', 'center');
    if (t > Lt('s16_02') - .1 && t < Lt('s16_05') - .1) {   // 1. prairie dogs have words for you
      drawSpr(g, 'prairie', 560, 560, 260);
      for (let i = 0; i < 3; i++) { const r = ((t * 120 + i * 60) % 180) + 20; g.save(); g.globalAlpha = 1 - r / 200; g.strokeStyle = red; g.lineWidth = 6; g.beginPath(); g.arc(590, 370, r, -.6, .6); g.stroke(); g.restore(); }
      text(g, 'PERRITO DE LA PRADERA', 560, 610, 40, ink, 'Bangers', 'center');
      if (t > Lt('s16_03')) { chip(g, '¡HUMANO!', 900, 330, R(t, Lt('s16_03') + .2, Lt('s16_03') + .5)); chip(g, 'ALTO', 900, 430, R(t, Lm('s16_03', .55), Lm('s16_03', .55) + .3)); chip(g, 'ROPA: AMARILLA', 1000, 530, R(t, Lm('s16_03', .85), Lm('s16_03', .85) + .3)); }
      if (t > Lt('s16_04')) drawChar(g, 'tu', { x: 1300, y: 700, s: .42, t, look: [-16, 0], mouth: -.2, wide: .5 }); }
    if (t > Lt('s16_05') - .1 && t < Lt('s16_07') - .1) {   // 2. adult cats barely meow at each other
      drawAnimal(g, 'croqueta', 520, 620, .8, { head: 'bored', t }); g.save(); g.filter = 'grayscale(1) brightness(1.15)'; drawAnimal(g, 'croqueta', 780, 620, .8, { head: 'bored', t, flip: -1 }); g.restore();
      text(g, '…', 650, 330, 90, ink, 'Bangers', 'center'); text(g, 'GATO + GATO', 650, 670, 44, ink, 'Bangers', 'center');
      if (t > Lt('s16_06')) { drawAnimal(g, 'croqueta', 1200, 620, .8, { head: 'wide', t, open: Math.abs(Math.sin(t * 6)) * .6 }); text(g, '¡MIAU!', 1240, 340, 70, red, 'Bangers', 'center');
        drawChar(g, 'tu', { x: 1420, y: 660, s: .36, t, flip: -1, look: [-16, 8], mouth: .6 }); text(g, 'GATO → HUMANO', 1300, 700, 44, blue, 'Bangers', 'center'); } }
    if (t > Lt('s16_07') - .1 && t < Lt('s16_09') - .1) {   // 3. pigeons can learn written words
      const words = ['DOG', 'BIRD', 'WORD', 'TREE', 'CAKE', 'MILK']; words.forEach((w, i) => { const a = R(t, Lt('s16_07') + .3 + i * .25, Lt('s16_07') + .55 + i * .25); if (a > 0) { g.save(); g.globalAlpha = a; shape(g, q => rrPath(q, 470 + (i % 3) * 200, 290 + Math.floor(i / 3) * 120, 170, 90, 10), '#fbf7ec', 5); text(g, w, 555 + (i % 3) * 200, 352 + Math.floor(i / 3) * 120, 54, ink, 'Bangers', 'center'); g.restore(); } });
      if (t > Lt('s16_08')) text(g, '58 PALABRAS', 760, 580, 70, red, 'Bangers', 'center'); }
  });
  const nod = Math.sin(t * 2.2) * .06;
  st.col(g => { pigeonTalk(g, 1600, 692, .95, { flip: -1, front: 1, tilt: nod });
    if (t > Lt('s16_07')) { g.save(); g.globalAlpha = R(t, Lt('s16_07'), Lt('s16_07') + .3); g.strokeStyle = '#141014'; g.lineWidth = 3; for (const s2 of [-1, 1]) { g.beginPath(); g.arc(1571 + s2 * 14, 547, 10, 0, 7); g.stroke(); } g.beginPath(); g.moveTo(1567, 547); g.lineTo(1575, 547); g.stroke(); g.restore(); } });   // reading glasses
  compose2(X, st, { amt: 0 });
  if (t > Lt('s16_09')) sticker(X, 'PEPE SABE LEER', R(t, Lm('s16_09', .7), Lm('s16_09', .7) + .25, back), 90, 90, 80);
};

/* ================================================================ 17. call to action, end card */
SC.s17 = (X, t) => {
  const end = Le('s17_05') + .9, inv = Lt('s17_04');
  const cam = shots(t, [], [{ t: 0, cx: 1000, cy: 600, z: 1.25, z2: 1.35, lock: 1 }, { t: Lt('s17_03') - .05, cx: 1080, cy: 735, z: 3.0, z2: 3.3, lock: 1 }, { t: inv - .05, cx: 980, cy: 600, z: 1.5, z2: 1.55, lock: 1 }, { t: Lt('s17_05') - .1, cx: 1080, cy: 735, z: 3.6, z2: 3.9, lock: 1 }]);
  const st = stage(cam); st.wld(g => { drawSet(g, 'parkNight'); bench(g, 0); bench(g, 1); });
  st.col(g => { g.save(); g.globalAlpha = t > inv ? flickerAlpha(t, inv + .3, .9) : 1; drawChar(g, 'tu', benchSit(900, { t, look: t > inv ? [-6, 18] : [14, 4], mouth: t > inv ? -.2 : .4, wide: t > inv ? .7 : 0, footSwing: Math.sin(t * 2.4) * 10 })); g.restore(); });
  st.col(g => pigeonTalk(g, 1080, 792, .62, { flip: -1, front: 1, tilt: Math.sin(t * 1.3) * .08 }));
  compose2(X, st, { amt: 0 });
  if (t > Lt('s17_01') - .05 && t < Lt('s17_03') - .1) sticker(X, '¿QUÉ LE PREGUNTARÍAS A TU MASCOTA?', R(t, Lt('s17_01') - .05, Lt('s17_01') + .25, outC), 70, 60, 62);
  if (t > Lt('s17_02') - .05 && t < Lt('s17_03') - .1) sticker(X, '↓ COMENTARIOS ↓', R(t, Lt('s17_02') - .05, Lt('s17_02') + .25, outC), 70, 180, 60, '#ffffff');
  if (t > Lt('s17_03') && t < inv) { const [px, py] = worldToScreen(cam, 1080, 735); dashRing(X, px, py, 70 * cam.z, t); sticker(X, 'PEPE: 0 PALABRAS… HASTA EL FINAL', R(t, Lt('s17_03') + .2, Lt('s17_03') + .45, back), 70, 70, 58, '#ffd34d'); }
  if (t > Lm('s17_04', .5) && t < Lt('s17_05') - .1) { const a = R(t, Lm('s17_04', .5), Lm('s17_04', .5) + .3, back); X.save(); X.translate(W / 2, H - 200); X.scale(a, a); shape(X, q => rrPath(q, -260, -60, 520, 120, 20), '#e02424', 6); text(X, 'SUSCRÍBETE', 0, 26, 76, '#ffffff', 'Bangers', 'center'); X.restore(); }
  if (t > end) { const a = R(t, end, end + .5, outC); X.save(); X.globalAlpha = a; X.fillStyle = '#141a2e'; X.fillRect(0, 0, W, H);
    text(X, CHANNEL_NAME, W / 2, 230, 150, '#fde047', 'Bangers', 'center', OUT, 18);
    text(X, 'PRÓXIMO EPISODIO:', W / 2, 400, 64, '#ffffff', 'Bangers', 'center');
    text(X, '¿Y SI FUERAS', W / 2, 500, 84, '#ffffff', 'Bangers', 'center', OUT, 10); text(X, 'INVISIBLE?', W / 2, 600, 84, '#ffffff', 'Bangers', 'center', OUT, 10);
    shape(X, q => rrPath(q, W / 2 - 300, 720, 600, 130, 22), '#e02424', 7); text(X, 'SUSCRÍBETE', W / 2, 812, 84, '#ffffff', 'Bangers', 'center');
    pigeonTalk(X, 1600, 960, .9, { flip: -1, front: 1, tilt: Math.sin(t * 1.5) * .1 }); X.restore(); }
};
