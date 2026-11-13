/* Ep04 — scenes 12–17: Saturday at the bench, «Estoy aquí», the walk and the sunset, Pepe, the science, the end card */

function sunsetTint(X, a) { if (a <= 0) return; X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.globalCompositeOperation = 'multiply'; X.fillStyle = `rgba(255,178,120,${.55 * a})`; X.fillRect(0, 0, W, H);
  X.globalCompositeOperation = 'screen'; const gr = X.createRadialGradient(1700, 200, 0, 1700, 200, 1200); gr.addColorStop(0, `rgba(255,170,90,${.45 * a})`); gr.addColorStop(1, 'rgba(0,0,0,0)'); X.fillStyle = gr; X.fillRect(0, 0, W, H); X.restore(); }
/* Renata on the bench: phone in the right hand, Canela's leash in the left */
function renataSit(t, extra = {}) { return benchSit(1080, Object.assign({ t, look: [6, 18], mouth: -.1, brow: .3, hR: [60, -300], holdR: phoneHold, hL: [-90, -200] }, extra)); }
const RENATA_S = S0 * (CAST.valeria.s || 1);
function canelaAt(g, t, x, y, s, extra = {}) { return drawAnimal(g, 'canela', x, y, s, Object.assign({ t }, extra)); }

/* ================================================================ 12. Saturday: you came. She can't see you. Canela can smell you. */
SC.s12 = (X, t) => {
  const arrive = Lt('s12_03') + .2, sniff = Lt('s12_07') - .05, run = Lt('s12_08') - .1, sit = run + .9;
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 540, z: 1.0, z2: 1.04, lock: 1 },
    { t: Lt('s12_04') - .05, cx: 1120, cy: 600, z: 2.0, z2: 2.1, lock: 1 },
    { t: Lt('s12_06') - .05, cx: 700, cy: 520, z: 2.0, z2: 2.15, lock: 1 },
    { t: sniff, cx: 1320, cy: 860, z: 2.6, z2: 2.75, lock: 1 },
    { t: run, cx: 960, cy: 600, z: 1.15, z2: 1.2, lock: 1 },
    { t: sit + .2, cx: 720, cy: 820, z: 2.1, z2: 2.2, lock: 1 },
    { t: Lt('s12_09') - .05, cx: 1080, cy: 540, z: 2.2, z2: 2.3, lock: 1 },
  ]);
  const st = stageI(cam);
  const rp = renataSit(t);
  if (speaking(t, 's12_05')) { rp.open = talk(t, 's12_05'); rp.look = [-6, 6]; rp.brow = .6; }
  if (t > run) { rp.look = [-16, 10]; rp.brow = .5; rp.hL = [-170, -260]; }
  if (speaking(t, 's12_09')) { rp.open = talk(t, 's12_09'); rp.look = [-16, 14]; rp.brow = .2; rp.mouth = .3; }
  // Canela: sitting, then sniffing the air, then running to your feet
  let cpos = [1330, 1000, .85], cx = 1330;
  st.wld(g => { drawSet(g, 'park'); bench(g, 0); });
  st.wld(g => drawChar(g, 'valeria', rp)); st.wld(g => bench(g, 1));
  st.wld(g => pepeWatch(g, 1560, 760, .5, 640, t));
  if (t < run) st.wld(g => canelaAt(g, t, 1330, 1000, .85, { tilt: t > sniff ? -.3 + Math.sin(t * 9) * .08 : Math.sin(t * 1.6) * .06, bob: t > sniff ? -Math.abs(Math.sin(t * 9)) * 4 : 0 }));
  else if (t < sit) { const u = R(t, run, sit, lin); cx = mix(1330, 760, u); st.wld(g => drawSpr(g, 'canelaRun', cx, 1020, 120, { flip: 1, bob: -Math.abs(Math.sin(t * 13)) * 12 })); }
  else { cx = 760; st.wld(g => canelaAt(g, t, 760, 1050, .9, { tilt: -.35 + Math.sin(t * 2) * .05, bob: -Math.abs(Math.sin(t * 8)) * 4 })); }
  // the leash from her left hand to the collar
  st.wld(g => { const h = handPt('valeria', rp, -1); leash(g, h, [cx + (t < run ? -20 : 0), t < sit && t > run ? 960 : 900], t > run ? 10 : 70); });
  // you: walk in and stop right in front of her; almost speak; don't
  const hx = mix(-150, 640, R(t, Lt('s12_03') - .8, arrive, io)), walking = t < arrive && t > Lt('s12_03') - .8;
  const hp = ghost({ x: hx, y: 1010, s: .84, t, walk: walking ? 1 : 0, phase: walkPh(hx), look: [14, 8], mouth: .3, blush: .4 });
  if (t > Lt('s12_06') && t < sniff) { const u = R(t, Lt('s12_06'), Lm('s12_06', .4), io) * (1 - R(t, Lm('s12_06', .7), Le('s12_06'), io)); hp.hR = [mix(80, 150, u), mix(-200, -470, u)]; hp.open = u * .6; hp.brow = .6; }
  if (t > sit) { hp.look = [-4, 20]; hp.mouth = .6; hp.wide = .4; }
  if (t > Lt('s12_09')) { hp.look = [16, 6]; hp.mouth = -.2; hp.brow = .6; hp.sweat = 1; }
  if (t > Lt('s12_03') - .8) st.inv(g => drawChar(g, 'tu', hp));
  composeI(X, st, { inv: 1, t });
  sticker(X, 'SÁBADO · 5:00 PM', vis(t, .2, Lt('s12_03') - .2), 70, 70, 64);
  if (t > sniff + .2 && t < run) comicWord(X, 'SNIFF SNIFF', ...worldToScreen(cam, 1300, 760), t - sniff - .2, 64, '#ffffff', 1.4);
  if (t > sit + .3 && t < Lt('s12_09')) for (let i = 0; i < 3; i++) heartPop(X, ...worldToScreen(cam, 720 + i * 50, 840), loopU(t, sit + i * .3, 1.2), 1.2);
};

/* ================================================================ 13. «Bueno. Se le olvidó.» — «Renata… Estoy aquí.» */
SC.s13 = (X, t) => {
  const jump = Lt('s13_07') - .05;
  const cam = shots(t, [], [
    { t: 0, cx: 1080, cy: 540, z: 2.0, z2: 2.1, lock: 1 },
    { t: Lt('s13_03') - .05, cx: 680, cy: 520, z: 1.9, z2: 2.4, lock: 1 },
    { t: Lt('s13_06') - .05, cx: 860, cy: 560, z: 1.35, z2: 1.42, lock: 1 },
    { t: jump, cx: 900, cy: 520, z: 1.3, z2: 1.25, lock: 1, shake: 1 },
    { t: Lt('s13_08') - .05, cx: 700, cy: 520, z: 2.0, z2: 2.1, lock: 1 },
  ]);
  const st = stageI(cam);
  let rp = renataSit(t);
  if (t > Lt('s13_01') + .3) { rp.hR = [80, -125]; rp.holdR = null; rp.look = [-4, 16]; }
  if (speaking(t, 's13_02')) { rp.open = talk(t, 's13_02'); rp.brow = .7; rp.mouth = -.3; }
  if (t > Le('s13_02')) { rp.mouth = -.3; rp.brow = .8; rp.look = [-2, 20]; rp.slump = .5; }
  if (t > jump) { rp = { x: 1040, y: FEET, s: S0, t, flip: -1, look: [-16, 4], wide: 1, brow: 1, mouth: -.5, hL: [-60, -500], hR: [60, -500], jump: Math.max(0, Math.sin(clamp((t - jump) / .45) * Math.PI)) * 90 };
    if (speaking(t, 's13_07')) rp.open = 1; }
  st.wld(g => { drawSet(g, 'park'); bench(g, 0); }); st.wld(g => drawChar(g, 'valeria', rp)); st.wld(g => bench(g, 1));
  st.wld(g => canelaAt(g, t, 760, 1050, .9, { tilt: -.35 + Math.sin(t * 2) * .05 }));
  const hp = ghost({ x: 640, y: 1010, s: .84, t, look: [16, 6], mouth: -.2, brow: .6 });
  if (t > Lt('s13_03')) { hp.look = [6, 4]; hp.brow = .3; hp.mouth = -.1; }
  if (t > Lt('s13_05')) { hp.look = [16, 4]; hp.brow = -.2; hp.mouth = .1; }
  if (speaking(t, 's13_06')) { hp.open = talk(t, 's13_06') * .7; hp.blush = .6; }
  if (t > jump) { hp.wide = .8; hp.brow = 1; hp.hL = [-160, -480]; hp.hR = [160, -480]; }
  if (speaking(t, 's13_08')) { hp.open = talk(t, 's13_08'); hp.hL = [-150, -420 + Math.sin(t * 12) * 30]; hp.hR = [150, -420 - Math.sin(t * 12) * 30]; }
  st.inv(g => drawChar(g, 'tu', hp));
  composeI(X, st, { inv: 1, t });
  if (t > Lt('s13_03') && t < Lt('s13_06')) { X.save(); X.globalAlpha = .35 * R(t, Lt('s13_03'), Lt('s13_03') + .8); X.fillStyle = '#0d0b18'; X.fillRect(0, 0, W, H); X.restore(); }   // the moment slows down
  if (t > Lt('s13_04') && t < Lt('s13_06')) sticker(X, 'SI NO DICES NADA… NO VINISTE', R(t, Lt('s13_04') + .2, Lt('s13_04') + .45, back), 70, 70, 62, '#ffffff');
  voiceBubble(X, cam, t, 's13_06', mouthPt('tu', hp), { dx: 1, r: 100 });
  voiceBubble(X, cam, t, 's13_08', mouthPt('tu', hp), { dx: 1, r: 100, w: 620 });
  if (t > jump && t < jump + .9) comicWord(X, '¡AAAH!', ...worldToScreen(cam, 1100, 260), t - jump, 100);
};

/* ================================================================ 14. her hand, the walk, rule 3, the sunset: you reappear */
SC.s14 = (X, t) => {
  const reach = Lt('s14_02'), take = Lt('s14_03') + .2, walk0 = Lt('s14_06') - .1, rule = Lt('s14_08') - .2, sun = Lt('s14_10') - .1, appear = Lm('s14_10', .55);
  const cam = shots(t, [], [
    { t: 0, cx: 1040, cy: 520, z: 2.1, z2: 2.2, lock: 1 },
    { t: reach - .05, cx: 860, cy: 600, z: 1.5, z2: 1.6, lock: 1 },
    { t: Lt('s14_03') - .05, cx: 870, cy: 690, z: 3.0, z2: 3.2, lock: 1 },
    { t: Lt('s14_04') - .05, cx: 1040, cy: 520, z: 2.1, z2: 2.2, lock: 1 },
    { t: walk0, cx: 960, cy: 560, z: 1.05, z2: 1.1, lock: 1 },
    { t: rule, cx: 960, cy: 540, z: 1.0, lock: 1 },
    { t: sun, cx: 880, cy: 560, z: 1.45, z2: 1.55, lock: 1 },
    { t: Lt('s14_11') - .05, cx: 960, cy: 540, z: 1.0, z2: 1.04, lock: 1 },
    { t: Lt('s14_12') - .05, cx: 1040, cy: 520, z: 2.3, z2: 2.4, lock: 1 },
    { t: Lt('s14_13') - .05, cx: 720, cy: 510, z: 2.3, z2: 2.4, lock: 1 },
  ]);
  const st = stageI(cam); st.wld(g => { drawSet(g, 'park'); bench(g, 0); bench(g, 1); });
  const walking = t > walk0 && t < rule, wu = R(t, walk0, rule - .3, lin), base = mix(-300, 1500, wu);
  let rp, hp, cxy;
  if (walking) {
    rp = { x: base + 230, y: FEET, s: S0, t, walk: 1, phase: walkPh(base + 230), look: [-12, 6], mouth: .7, blush: .6, hL: [-110, -330] };
    hp = ghost({ x: base, y: FEET + 10, s: S0, t, walk: 1, phase: walkPh(base), look: [12, 4], mouth: .7, blush: .6, hR: [130, -330], hL: [-100, -300] });
    cxy = [base + 520, 1000];
    st.wld(g => drawSpr(g, 'canelaRun', cxy[0], cxy[1], 110, { flip: -1, bob: -Math.abs(Math.sin(t * 12)) * 8 }));
    st.wld(g => leash(g, handPt('tu', hp, 1), [cxy[0] - 50, cxy[1] - 70], 30));   // the floating leash: held by nobody you can see
    // passers-by stop and stare at the girl talking to a flying leash
    st.wld(g => { drawChar(g, 'ex4', standing(1480, { t, flip: -1, look: [-16, 6], mouth: -.3, wide: .8, brow: .9, s: .62, y: 840 })); drawChar(g, 'ex6', standing(1640, { t, flip: -1, look: [-16, 4], mouth: -.4, wide: .6, s: .62, y: 840 })); });
  } else {
    rp = { x: 1040, y: FEET, s: S0, t, flip: -1, look: [-16, 4], mouth: .1, brow: .5 };
    hp = ghost({ x: 700, y: 1010, s: .84, t, look: [16, 6], mouth: .2, brow: .4 });
    if (speaking(t, 's14_01')) { rp.open = talk(t, 's14_01') * .6; rp.brow = .8; rp.wide = .3; }
    const u = R(t, reach, take, io);
    if (t > reach) { rp.hR = [mix(80, 224, u), mix(-200, -317, u)]; rp.wide = .4; }
    if (t > take) { hp.hR = [202, -381]; hp.blush = .9; hp.mouth = .6; hp.brow = 0; rp.blush = .7; }
    if (speaking(t, 's14_04')) { rp.open = talk(t, 's14_04'); rp.mouth = .5; rp.brow = .6; }
    if (speaking(t, 's14_05') || t > Le('s14_05')) { if (speaking(t, 's14_05')) rp.open = talk(t, 's14_05'); rp.mouth = .8; rp.blush = 1; rp.look = [-16, 8]; }
    if (t > sun) { rp.mouth = .6; rp.blush = 1; hp.blush = 1; hp.mouth = .5; }
    if (t > Lt('s14_11')) { rp.wide = .6; hp.wide = .6; hp.sweat = 1; }
    if (speaking(t, 's14_12')) rp.open = talk(t, 's14_12') * .5;
    if (speaking(t, 's14_13')) hp.open = talk(t, 's14_13') * .5;
    cxy = [880, 1050];
    st.wld(g => canelaAt(g, t, cxy[0], cxy[1], .9, { tilt: t > take ? Math.sin(t * 3) * .1 : -.35, bob: t > Lt('s14_11') ? -Math.abs(Math.sin(t * 9)) * 30 : 0 }));
    if (t > Lt('s14_11')) st.wld(g => { drawChar(g, 'ex4', standing(1500, { t, flip: -1, look: [-16, 6], mouth: -.4, wide: 1, brow: 1, s: .62, y: 840 })); drawChar(g, 'ex1', standing(240, { t, look: [16, 6], mouth: -.4, wide: 1, brow: 1, s: .62, y: 840 }));
      drawChar(g, 'ex6', standing(1720, { t, flip: -1, look: [-16, 4], mouth: .8, wide: .6, s: .62, y: 840 })); });
  }
  st.wld(g => drawChar(g, 'valeria', rp));
  st.inv(g => drawChar(g, 'tu', hp));
  const inv = 1 - R(t, appear - .5, appear + .7, io);
  composeI(X, st, { inv, t });
  sunsetTint(X, R(t, sun, sun + 1.2));
  if (t > appear - .6 && t < appear + 1.2) { const [x, y] = worldToScreen(cam, hp.x, hp.y - 260 * hp.s); invSparkle(X, x, y, 330 * cam.z * hp.s, R(t, appear - .6, appear + 1.2, lin)); }
  if (t > take && t < take + .9) comicWord(X, '♥', ...worldToScreen(cam, 870, 600), t - take, 90, '#ff5d7a', .9);
  if (walking && t > Lt('s14_07')) comicWord(X, '¿?', ...worldToScreen(cam, 1600, 300), t - Lt('s14_07'), 90, '#fde047', 1.2);
  if (t > Lt('s14_11') + .2 && t < Lt('s14_12')) for (const [wx, wy] of [[240, 420], [1500, 420], [1720, 420]]) comicWord(X, '¡!', ...worldToScreen(cam, wx, wy), t - Lt('s14_11') - .2, 70, '#ffffff', 1.0);
  ruleCard(X, 3, 'SI NADIE TE PUEDE VER,', t > Lm('s14_08', .5) ? 'DI QUE ESTÁS AHÍ.' : '', R(t, rule, rule + .4, outC) * (1 - R(t, sun - .3, sun)));
};

/* ================================================================ 15. night: «Yo siempre te he visto.» Pepe flies off. Or vanishes. */
function wings(g, x, y, s, u, flap = 0) { if (u <= 0) return; g.save(); g.translate(x, y); g.scale(s, s);
  for (const sd of [-1, 1]) { g.save(); g.scale(sd, 1); g.rotate(-.5 * u - flap * .5); shape(g, q => { q.moveTo(0, 0); q.quadraticCurveTo(120 * u, -110 * u, 200 * u, -40 * u); q.quadraticCurveTo(130 * u, 10, 0, 30); q.closePath(); }, '#8d93a6', 4);
    for (let i = 0; i < 3; i++) line(g, [[60 * u + i * 40 * u, -30 * u], [90 * u + i * 40 * u, 10]], '#6a7086', 3); g.restore(); }
  g.restore(); }
SC.s15 = (X, t) => {
  const open = Lt('s15_06'), fly = Lt('s15_09') - .1, vanish = Lm('s15_10', .35);
  const cam = shots(t, [], [
    { t: 0, cx: 980, cy: 640, z: 1.3, z2: 1.35, lock: 1 },
    { t: Lt('s15_02') - .05, cx: 990, cy: 650, z: 1.6, z2: 1.65, lock: 1 },
    { t: Lt('s15_03') - .05, cx: 920, cy: 540, z: 2.4, z2: 2.5, lock: 1 },
    { t: Lt('s15_05') - .05, cx: 1080, cy: 730, z: 3.0, z2: 3.4, lock: 1 },
    { t: open - .05, cx: 1040, cy: 680, z: 2.2, z2: 2.3, lock: 1 },
    { t: Lt('s15_07') - .05, cx: 1080, cy: 720, z: 3.2, z2: 3.5, lock: 1 },
    { t: Lt('s15_08') - .05, cx: 920, cy: 540, z: 2.4, z2: 2.5, lock: 1 },
    { t: fly, cx: 1100, cy: 520, z: 1.2, z2: 1.15, lock: 1 },
  ]);
  const st = stageI(cam); st.wld(g => { drawSet(g, 'parkNight'); bench(g, 0); bench(g, 1); });
  const hp = benchSit(900, { t, look: [14, 6], mouth: .3, open: t < Lt('s15_03') ? Math.abs(Math.sin(t * 7)) * .4 : 0 });
  for (const id of ['s15_03', 's15_04']) if (speaking(t, id)) { hp.open = talk(t, id); hp.look = [16, 8]; hp.brow = id === 's15_04' ? .5 : 0; }
  if (t > Lt('s15_05')) { hp.wide = .6; hp.brow = .8; hp.mouth = -.1; hp.look = [16, 8]; }
  if (t > fly) { hp.look = [14, -14]; hp.mouth = -.2; }
  st.wld(g => drawChar(g, 'tu', hp));
  let mP = null;
  if (t < fly) st.wld(g => { const u = R(t, open, open + .5, back); wings(g, 1080, 720, .62, u, Math.sin(t * 6) * .2 * u); mP = pigeonTalk(g, 1080, 792, .62, { flip: -1, front: t > Lt('s15_04'), open: openOfP(t, ['s15_05', 's15_07', 's15_08']), tilt: Math.sin(t * 1.1) * .04 }); });
  else { const u = R(t, fly, vanish, lin), px = mix(1080, 1500, u), py = mix(792, 260, io(u)), a = 1 - R(t, vanish - .2, vanish + .2);
    if (a > 0) st.wld(g => { g.save(); g.globalAlpha = a; wings(g, px, py - 70, .62, 1, Math.sin(t * 22)); pigeonTalk(g, px, py, .62, { flip: 1, tilt: -.2 }); g.restore(); }); }
  composeI(X, st, { inv: 0, t });
  if (t > Lt('s15_02') && t < Lt('s15_03')) { const items = [['torta'], ['tissues'], ['heart']]; items.forEach(([k], i) => { const a0 = Lm('s15_02', .1 + i * .3); if (t > a0) { const a = R(t, a0, a0 + .25, back), [x, y] = [560 + i * 400, 200];
      X.save(); X.globalAlpha = a; X.translate(x, y); X.scale(a, a); circ(X, 0, 0, 90, '#ffffff', 6); if (k === 'heart') heartPop(X, 0, 30, .2, 2.2); else X.drawImage(SPR[k], -60, -50, 120, 120 * SPR[k].height / SPR[k].width); X.restore(); } }); }
  if (mP) for (const id of ['s15_05', 's15_07', 's15_08']) talkBubble(X, cam, mP[0], mP[1], id, 'RUU', { t, dx: 1, r: 40, size: 62, w: 760 });
  if (t > vanish - .3 && t < vanish + 1) { const u = R(t, fly, vanish, lin), [x, y] = worldToScreen(cam, mix(1080, 1500, u), mix(792, 260, io(u)) - 40); invSparkle(X, x, y, 160 * cam.z, R(t, vanish - .3, vanish + 1, lin), 7); }
  if (t > Le('s15_10') + .3) { X.save(); X.globalAlpha = R(t, Le('s15_10') + .3, T().dur, lin); X.fillStyle = '#000'; X.fillRect(0, 0, W, H); X.restore(); }
};
const openOfP = (t, ids) => Math.max(0, ...ids.map(id => T().L[id] && speaking(t, id) ? talk(t, id) : 0));

/* ================================================================ 16. is any of this real? */
function chip(g, s, x, y, a, col = '#ffd34d') { if (a <= 0) return; g.save(); g.globalAlpha = clamp(a); g.font = '46px Bangers'; const w = g.measureText(s).width + 40; g.translate(x, y); g.scale(.8 + .2 * back(a), .8 + .2 * back(a));
  shape(g, q => rrPath(q, -w / 2, -34, w, 68, 16), col, 5); text(g, s, 0, 17, 46, '#141014', 'Bangers', 'center'); g.restore(); }
function cloakDiagram(g, t, cx, cy, a) { if (a <= 0) return; g.save(); g.globalAlpha = clamp(a); const R0 = 150, r0 = 62;
  for (let k = 0; k < 18; k++) { const x0 = 420 + ((t * 110 + k * 64) % 1150); g.beginPath(); let first = true;
    for (let y = 230; y <= 560; y += 6) { const d = Math.hypot(x0 - cx, y - cy); let x = x0; if (d < R0) { const f = 1 - d / R0; x = x0 - Math.sin(f * Math.PI / 2) * 70; }
      const inside = Math.hypot(x - cx, y - cy) < r0 + 6; if (inside) { first = true; continue; } if (first) { g.moveTo(x, y); first = false; } else g.lineTo(x, y); }
    g.strokeStyle = 'rgba(58,111,176,.75)'; g.lineWidth = 5; g.stroke(); }
  for (let i = 0; i < 3; i++) { g.save(); g.strokeStyle = 'rgba(120,80,160,.55)'; g.lineWidth = 6; g.setLineDash([10, 8]); g.beginPath(); g.arc(cx, cy, r0 + 30 + i * 28, 0, 7); g.stroke(); g.restore(); }
  const gr = g.createRadialGradient(cx - 20, cy - 20, 6, cx, cy, r0); gr.addColorStop(0, '#f6b97a'); gr.addColorStop(1, '#b4642e'); shape(g, q => q.arc(cx, cy, r0, 0, 7), gr, 5);
  g.restore(); }
function eyeDiagram(g, x, y, t, a, seeThrough) { if (a <= 0) return; g.save(); g.globalAlpha = clamp(a); g.translate(x, y);
  if (seeThrough) g.setLineDash([12, 8]); shape(g, q => q.arc(0, 0, 110, 0, 7), seeThrough ? 'rgba(220,245,255,.5)' : '#ffffff', 6);
  shape(g, q => q.ellipse(-92, 0, 14, 44, 0, 0, 7), seeThrough ? 'rgba(150,220,255,.5)' : '#7fb6e8', 4); g.setLineDash([]);
  const ray = (yy, u) => { g.strokeStyle = '#f5b400'; g.lineWidth = 5; g.beginPath(); g.moveTo(-320, yy); g.lineTo(-92, yy * .6);
    if (seeThrough) g.lineTo(320, yy * .6 + (yy * .2)); else g.lineTo(100, 0); g.stroke(); };
  for (const yy of [-60, -20, 20, 60]) ray(yy);
  if (!seeThrough) { const gl = .6 + .4 * Math.sin(t * 6); g.save(); g.shadowColor = '#ffde59'; g.shadowBlur = 30 * gl; shape(g, q => q.arc(102, 0, 16, 0, 7), '#ffde59', 4); g.restore(); }
  else text(g, '?', 150, -40, 64, '#c0262d', 'Bangers', 'center');
  g.restore(); }
SC.s16 = (X, t) => {
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 470, z: 1.12, z2: 1.16, lock: 1 },
    { t: Lt('s16_02') - .05, cx: 960, cy: 440, z: 1.2, z2: 1.26, lock: 1 },
    { t: Lt('s16_05') - .05, cx: 960, cy: 440, z: 1.2, z2: 1.26, lock: 1 },
    { t: Lt('s16_07') - .05, cx: 1000, cy: 430, z: 1.2, z2: 1.28, lock: 1 },
    { t: Lt('s16_09') - .05, cx: 1420, cy: 560, z: 1.9, z2: 2.0, lock: 1 },
  ]);
  const ink = '#2d2a40', red = '#c0262d', blue = '#3a6fb0';
  const st = stageI(cam);
  st.wld(g => { drawSet(g, 'classroom'); teacherDesk(g, 1620);
    text(g, '¿ALGO DE ESTO ES REAL?', 966, 205, 70, red, 'Bangers', 'center');
    if (t > Lt('s16_02') - .1 && t < Lt('s16_05') - .1) {   // 1. the microwave cloak
      cloakDiagram(g, t, 760, 400, R(t, Lt('s16_02'), Lt('s16_02') + .4));
      chip(g, 'DUKE · 2006', 1240, 290, R(t, Lt('s16_02') + .3, Lt('s16_02') + .6));
      if (t > Lt('s16_03')) chip(g, 'MICROONDAS ✓', 1240, 390, R(t, Lt('s16_03') + .2, Lt('s16_03') + .5), '#a7f3a0');
      if (t > Lt('s16_04')) chip(g, 'LUZ ✗', 1240, 490, R(t, Lt('s16_04') + .1, Lt('s16_04') + .4));
      text(g, 'CILINDRO DE COBRE', 760, 610, 38, ink, 'Bangers', 'center'); }
    if (t > Lt('s16_05') - .1 && t < Lt('s16_07') - .1) {   // 2. the glass frog hides its blood
      const sleep = R(t, Lt('s16_06'), Lm('s16_06', .7), io);
      shape(g, q => q.ellipse(720, 420, 230, 120, -.2, 0, 7), '#7cc576', 5); line(g, [[540, 470], [900, 370]], '#4f9a4a', 5);
      drawSpr(g, 'glassFrog', 720, 560, 280, { alpha: 1 - .55 * sleep });
      if (t > Lt('s16_06')) { const r = rnd(5); for (let i = 0; i < 14; i++) { const u = clamp(sleep * 1.3 - r() * .3), x0 = 640 + r() * 160, y0 = 360 + r() * 160; circ(g, mix(x0, 722, u), mix(y0, 470, u), 7, '#e2453c', 2); }
        shape(g, q => q.ellipse(722, 470, 30, 22, 0, 0, 7), 'rgba(200,210,225,.85)', 3); text(g, 'Z z z', 900, 300, 48, blue, 'Bangers', 'center'); }
      text(g, 'RANA DE CRISTAL', 720, 620, 40, ink, 'Bangers', 'center');
      chip(g, 'SUR DE MÉXICO → SUDAMÉRICA', 1240, 300, R(t, Lt('s16_05') + .4, Lt('s16_05') + .7));
      if (t > Lt('s16_06')) chip(g, '89% GLÓBULOS ROJOS → HÍGADO', 1240, 420, R(t, Lm('s16_06', .3), Lm('s16_06', .3) + .3), '#ffb3b3'); }
    if (t > Lt('s16_07') - .1 && t < Lt('s16_09') - .1) {   // 3. a truly invisible eye would see nothing
      eyeDiagram(g, 760, 400, t, R(t, Lt('s16_07') + .2, Lt('s16_07') + .5), false); text(g, 'OJO NORMAL: ATRAPA LA LUZ', 760, 600, 36, ink, 'Bangers', 'center');
      if (t > Lt('s16_08')) { eyeDiagram(g, 1240, 400, t, R(t, Lt('s16_08'), Lt('s16_08') + .3), true); text(g, 'OJO INVISIBLE: NADA', 1240, 600, 36, red, 'Bangers', 'center'); } }
  });
  st.wld(g => pigeonTalk(g, 1600, 692, .95, { flip: -1, front: 1, tilt: Math.sin(t * 2.2) * .06 }));
  composeI(X, st, { inv: 0, t });
  if (t > Lt('s16_04') + .3 && t < Lt('s16_05') - .1) sticker(X, 'SOLO SI ERES UN CILINDRO', R(t, Lm('s16_04', .5), Lm('s16_04', .5) + .25, back), 90, 90, 64, '#ffffff');
  if (t > Lt('s16_07') && t < Lt('s16_09') - .1) sticker(X, 'INVISIBLE = CIEGO', R(t, Lm('s16_07', .5), Lm('s16_07', .5) + .25, back), 90, 90, 64);
  if (t > Lt('s16_09')) sticker(X, '¿Y CÓMO ME ESTÁS VIENDO?', R(t, Lm('s16_09', .6), Lm('s16_09', .6) + .25, back), 90, 90, 74);
};

/* ================================================================ 17. call to action, end card */
SC.s17 = (X, t) => {
  const end = Le('s17_04') + .9;
  const cam = shots(t, [], [{ t: 0, cx: 1000, cy: 600, z: 1.25, z2: 1.35, lock: 1 }, { t: Lt('s17_02') - .05, cx: 1080, cy: 735, z: 3.0, z2: 3.3, lock: 1 }, { t: Lt('s17_03') - .05, cx: 940, cy: 560, z: 1.6, z2: 1.7, lock: 1 }, { t: Lt('s17_04') - .1, cx: 1080, cy: 735, z: 3.6, z2: 3.9, lock: 1 }]);
  const st = stageI(cam); st.wld(g => { drawSet(g, 'parkNight'); bench(g, 0); bench(g, 1); });
  const smart = t > Lt('s17_03');
  st.wld(g => drawChar(g, 'tu', benchSit(900, { t, look: smart ? [10, -16] : [14, 4], mouth: smart ? .7 : .4, brow: smart ? -.3 : 0, footSwing: Math.sin(t * 2.4) * 10 })));
  st.wld(g => pigeonTalk(g, 1080, 792, .62, { flip: -1, front: 1, tilt: Math.sin(t * 1.3) * .08 }));
  if (t > Lt('s17_02')) st.wld(g => { g.save(); g.globalAlpha = R(t, Lt('s17_02') + .2, Lt('s17_02') + .5); g.strokeStyle = '#141014'; g.lineWidth = 3; g.lineWidth = 2.5; for (const s2 of [-1, 1]) { g.beginPath(); g.arc(1061 + s2 * 9, 697, 6.5, 0, 7); g.stroke(); } g.beginPath(); g.moveTo(1058, 697); g.lineTo(1064, 697); g.stroke(); g.restore(); });   // reading glasses
  composeI(X, st, { inv: 0, t });
  if (t > Lt('s17_01') - .05 && t < Lt('s17_03') - .1) sticker(X, '¿QUÉ HARÍAS SI FUERAS INVISIBLE UN DÍA?', R(t, Lt('s17_01') - .05, Lt('s17_01') + .25, outC), 70, 60, 58);
  if (t > Lt('s17_02') - .05 && t < Lt('s17_03') - .1) { sticker(X, '↓ COMENTARIOS ↓', R(t, Lt('s17_02') - .05, Lt('s17_02') + .25, outC), 70, 180, 60, '#ffffff'); sticker(X, 'PEPE LOS LEE', R(t, Lm('s17_02', .5), Lm('s17_02', .5) + .25, back), 70, 300, 60); }
  if (smart && t < Lt('s17_04') - .1) { const [x, y] = worldToScreen(cam, 900, 300); const a = R(t, Lt('s17_03') + .2, Lt('s17_03') + .5, back); X.save(); X.globalAlpha = a; X.translate(x, y); X.scale(a, a); X.shadowColor = '#fde047'; X.shadowBlur = 40;
    shape(X, q => q.arc(0, -10, 46, 0, 7), '#fde047', 5); X.shadowBlur = 0; shape(X, q => q.rect(-20, 30, 40, 26), '#9aa3ad', 4); text(X, 'IQ 500', 0, -110, 56, '#ffffff', 'Bangers', 'center', OUT, 8); X.restore(); }
  if (t > Lt('s17_04') && t < end) { const [px, py] = worldToScreen(cam, 1080, 735); dashRing(X, px, py, 70 * cam.z, t); sticker(X, 'NO TE VA A GUSTAR', R(t, Lt('s17_04') + .3, Lt('s17_04') + .55, back), 70, 70, 70); }
  if (t > end) { const a = R(t, end, end + .5, outC); X.save(); X.globalAlpha = a; X.fillStyle = '#141a2e'; X.fillRect(0, 0, W, H);
    text(X, CHANNEL_NAME, W / 2, 230, 150, '#fde047', 'Bangers', 'center', OUT, 18);
    text(X, 'PRÓXIMO EPISODIO:', W / 2, 400, 64, '#ffffff', 'Bangers', 'center');
    text(X, '¿Y SI TUVIERAS', W / 2, 500, 84, '#ffffff', 'Bangers', 'center', OUT, 10); text(X, '500 DE IQ?', W / 2, 600, 84, '#ffffff', 'Bangers', 'center', OUT, 10);
    shape(X, q => rrPath(q, W / 2 - 300, 720, 600, 130, 22), '#e02424', 7); text(X, 'SUSCRÍBETE', W / 2, 812, 84, '#ffffff', 'Bangers', 'center');
    pigeonTalk(X, 1600, 960, .9, { flip: -1, front: 1, tilt: Math.sin(t * 1.5) * .1 }); X.restore(); }
};
