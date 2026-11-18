/* Ep06 — scenes 12–17: Renata leaves, the warning, the bus stop and all the pain at once, Pepe, the science, the end card */
function wings(g, x, y, s, u, flap = 0) { if (u <= 0) return; g.save(); g.translate(x, y); g.scale(s, s);
  for (const sd of [-1, 1]) { g.save(); g.scale(sd, 1); g.rotate(-.5 * u - flap * .5); shape(g, q => { q.moveTo(0, 0); q.quadraticCurveTo(120 * u, -110 * u, 200 * u, -40 * u); q.quadraticCurveTo(130 * u, 10, 0, 30); q.closePath(); }, '#8d93a6', 4);
    for (let i = 0; i < 3; i++) line(g, [[60 * u + i * 40 * u, -30 * u], [90 * u + i * 40 * u, 10]], '#6a7086', 3); g.restore(); }
  g.restore(); }
const openOfP = (t, ids) => Math.max(0, ...ids.map(id => T().L[id] && speaking(t, id) ? talk(t, id) : 0));
function chip(g, s, x, y, a, col = '#ffd34d') { if (a <= 0) return; g.save(); g.globalAlpha = clamp(a); g.font = '46px Bangers'; const w = g.measureText(s).width + 40; g.translate(x, y); g.scale(.8 + .2 * back(a), .8 + .2 * back(a));
  shape(g, q => rrPath(q, -w / 2, -34, w, 68, 16), col, 5); text(g, s, 0, 17, 46, '#141014', 'Bangers', 'center'); g.restore(); }
function suitcase(g, x, y) { shape(g, q => rrPath(q, x - 50, y - 120, 100, 120, 12), '#c0485a', 5); shape(g, q => rrPath(q, x - 20, y - 150, 40, 34, 8), null, 6); for (const dx of [-30, 30]) circ(g, x + dx, y + 4, 8, '#2e333d', 3); }
function bus(g, x, s = 1) { g.save(); g.translate(x, FEET); g.scale(s, s);
  shape(g, q => rrPath(q, -460, -420, 920, 380, 40), '#f4f1ea', 6); shape(g, q => rrPath(q, -460, -170, 920, 60, 10), '#2f8f4e', 0);
  for (let i = 0; i < 6; i++) shape(g, q => rrPath(q, -420 + i * 135, -370, 110, 120, 12), '#9fd0f0', 4);
  shape(g, q => rrPath(q, 360, -360, 80, 300, 10), '#cfe8f6', 4); text(g, 'OAXACA', -130, -105, 56, '#2f8f4e', 'Bangers', 'center');
  for (const dx of [-300, 300]) { circ(g, dx, -40, 56, '#2e333d', 5); circ(g, dx, -40, 24, '#9aa0aa', 3); } g.restore(); }

/* ================================================================ 12. Friday: «mañana me voy un mes a Oaxaca» */
SC.s12 = (X, t) => {
  const okay = Lt('s12_07') - .05, go = Lt('s12_09') - .05;
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 540, z: 1.0, z2: 1.04, lock: 1 },
    { t: Lt('s12_03') - .05, cx: 1150, cy: 470, z: 2.2, z2: 2.3, lock: 1 },
    { t: Lt('s12_05') - .05, cx: 980, cy: 520, z: 1.5, z2: 1.55, lock: 1 },
    { t: okay, cx: 840, cy: 470, z: 2.4, z2: 2.5, lock: 1 },
    { t: Lt('s12_08') - .05, cx: 1150, cy: 470, z: 2.4, z2: 2.5, lock: 1 },
    { t: go, cx: 960, cy: 540, z: 1.1, z2: 1.15, lock: 1 },
  ]);
  const st = stage(cam); st.wld(g => drawSet(g, 'street'));
  st.wld(g => pepeWatch(g, 1180, 470, .4, 840, t));
  const rx = t < go ? 1150 : mix(1150, 2150, R(t, go + .3, go + 3.5, lin));
  const rp = standing(rx, { t, flip: -1, look: [-14, 8], mouth: -.1, brow: .3, hL: [-90, -330], hR: [90, -330] });
  if (t > Lt('s12_03')) { rp.look = [-16, 2]; rp.brow = .5; rp.mouth = -.2; }
  if (t > okay + .4) { rp.wide = .4; rp.brow = .9; rp.mouth = -.5; }
  if (t > go) { rp.flip = 1; rp.look = [14, 10]; rp.walk = 1; rp.phase = walkPh(rx); rp.hL = null; rp.hR = null; rp.slump = .5; }
  say(rp, t, ['s12_03', 's12_04', 's12_08']);
  st.wld(g => drawChar(g, 'valeria', rp));
  const hx = mix(400, 840, R(t, Lt('s12_02'), Lt('s12_03') - .3, lin)), hp = standing(hx, { t, look: [14, 2], mouth: .4, walk: t > Lt('s12_02') && t < Lt('s12_03') - .3 ? 1 : 0, phase: walkPh(hx) });
  if (t > Lt('s12_06')) { hp.look = [16, 2]; hp.mouth = 0; hp.brow = .1; }
  if (t > go) { hp.look = [16, 0]; hp.mouth = -.1; }
  say(hp, t, ['s12_07']);
  st.wld(g => drawHero(g, hp, { bump: .9, cheek: 1, ankle: 1 }));
  compose2(X, st, { amt: 0 });
  hits(X, cam, t, [{ t: Lm('s12_06', .3), at: heartPt('tu', hp), cname: 'tu', p: hp, hero: 1, dur: .5 }, { t: Lt('s12_09') + .4, at: heartPt('tu', hp), cname: 'tu', p: hp, hero: 1, dur: .5 }]);
  sticker(X, 'VIERNES', vis(t, .3, Lt('s12_03') - .2), 70, 70, 64);
  if (t > Lt('s12_05') && t < okay) { sticker(X, '1 MES SIN RENATA', R(t, Lt('s12_05') + .1, Lt('s12_05') + .4, back), 70, 70, 60, '#ffb3b3'); sticker(X, 'SIN PASEOS CON CANELA', R(t, Lm('s12_05', .5), Lm('s12_05', .5) + .3, back), 70, 190, 60, '#ffb3b3'); }
  if (t > Lt('s12_10')) sticker(X, '«NI SIQUIERA LO QUE DEBERÍA»', R(t, Lm('s12_10', .4), Lm('s12_10', .4) + .3, back), 70, 70, 60);
};

/* ================================================================ 13. the warning: pain isn't the enemy */
SC.s13 = (X, t) => {
  const rule = Lt('s13_07') - .1;
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 560, z: 1.25, z2: 1.32, lock: 1 },
    { t: Lt('s13_03') - .05, cx: 860, cy: 520, z: 2.0, z2: 2.1, lock: 1 },
    { t: Lt('s13_04') - .05, cx: 960, cy: 540, z: 1.1, z2: 1.15, lock: 1 },
    { t: Lt('s13_06') - .05, cx: 860, cy: 520, z: 2.4, z2: 2.55, lock: 1 },
  ]);
  const st = stage(cam); st.wld(g => drawSet(g, 'kitchenNight'));
  const mp = standing(1180, { t, flip: -1, look: [-14, 6], mouth: .1, brow: .3, hR: [190, -340], holdR: (g, x, y) => curita(g, x + 6, y - 4, 60, .3) });
  if (t > Lt('s13_02')) { mp.hR = null; mp.holdR = null; mp.look = [-16, 4]; mp.mouth = .3; mp.brow = 0; }
  st.wld(g => drawChar(g, 'mama', mp));
  const hp = seated(860, { t, look: [10, 4], mouth: -.1, brow: .3, hL: [-80, -170], hR: [80, -170] });
  if (t > Lt('s13_02')) { hp.look = [0, -6]; hp.wide = .3; hp.brow = .6; }
  if (t > Lt('s13_05')) { hp.look = [-10, 4]; hp.wide = 0; hp.mouth = -.2; hp.brow = .8; }
  if (t > Lt('s13_06')) { hp.mouth = .2; hp.brow = .2; }
  st.wld(g => drawHero(g, hp)); st.wld(g => kitchenTable(g));
  compose2(X, st, { amt: 0 });
  const rows = [['TOBILLO', '¡PARA!', Lm('s13_04', .05)], ['SALSA', '¡ES DEMASIADO!', Lm('s13_04', .55)], ['RENATA', 'TE IMPORTA', Lm('s13_05', .4)]];
  if (t > Lt('s13_03') && t < rule) { sticker(X, 'EL DOLOR = UN AVISO', R(t, Lm('s13_03', .5), Lm('s13_03', .5) + .3, back), 70, 70, 66);
    rows.forEach(([a2, b2, t0], i) => { const a = R(t, t0, t0 + .3, back); if (a > 0) sticker(X, a2 + '  →  ' + b2, a, 70, 200 + i * 120, 58, i === 2 ? '#ffb3b3' : '#ffffff'); }); }
  if (t > Lt('s13_05') && t < rule) { const [x, y] = worldToScreen(cam, ...heartPt('tu', hp)); X.save(); X.globalAlpha = .5 + .5 * Math.sin(t * 6); heartPopX(X, x, y + 40, .1, 1.3); X.restore(); }
  ruleCard(X, 3, 'SI ALGO DEBERÍA DOLERTE, TE IMPORTA.', 'Y ESO HAY QUE DECIRLO', R(t, rule, rule + .3, outC));
};

/* ================================================================ 14. Saturday 6:55: «te voy a extrañar», then all the pain at once */
SC.s14 = (X, t) => {
  const arrive = Lt('s14_02') - .3, board = Lt('s14_07') - .05, off = Lm('s14_07', .72), all = Lt('s14_08') - .05, yell = Lt('s14_09') - .05, heart = Lt('s14_10') + .2;
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 540, z: 1.0, z2: 1.05, lock: 1 },
    { t: Lt('s14_02') - .05, cx: 1080, cy: 480, z: 2.2, z2: 2.3, lock: 1 },
    { t: Lt('s14_03') - .05, cx: 800, cy: 480, z: 2.2, z2: 2.35, lock: 1 },
    { t: Lt('s14_05') - .05, cx: 1080, cy: 470, z: 2.4, z2: 2.5, lock: 1 },
    { t: Lt('s14_06') - .05, cx: 940, cy: 520, z: 1.6, z2: 1.65, lock: 1 },
    { t: board, cx: 960, cy: 540, z: 1.0, z2: 1.03, lock: 1 },
    { t: all, cx: 800, cy: 500, z: 1.7, z2: 1.85, lock: 1 },
    { t: Lt('s14_10') - .05, cx: 800, cy: 480, z: 2.3, z2: 2.45, lock: 1 },
  ]);
  const st = stage(cam); st.wld(g => drawSet(g, 'street'));
  const bx = t < off - 1.6 ? 1500 : mix(1500, 2800, R(t, off - 1.6, off, inC));
  const rp = standing(1100, { t, flip: -1, look: [-14, 4], mouth: .2, brow: .3, hR: [90, -300], holdR: (g, x, y) => suitcase(g, x + 30, y + 150) });
  if (t > Lt('s14_05')) { rp.mouth = .6; rp.blush = .6; rp.brow = -.2; }
  if (t > Lt('s14_06') + Ld('s14_06') + .3) { const u = R(t, board, board + 1.2, lin); rp.x = mix(1100, 1250, u); rp.walk = u > 0 && u < 1 ? 1 : 0; rp.phase = walkPh(rp.x); rp.flip = 1; }
  say(rp, t, ['s14_02', 's14_06']);
  st.wld(g => bus(g, bx, 1.15));
  if (t < board + 1.2) st.wld(g => drawChar(g, 'valeria', rp));
  const hx = mix(250, 800, R(t, .6, arrive, lin)), lim = Math.abs(Math.sin(walkPh(hx)));
  const hp = standing(hx, { t, look: [14, 2], mouth: .2, walk: t < arrive ? .8 : 0, phase: walkPh(hx), hy: t < arrive ? -14 * lim : 0 });
  if (t > Lt('s14_03')) { hp.look = [16, 6]; hp.brow = .5; hp.mouth = .1; }
  if (t > Lt('s14_04')) { hp.blush = .6; hp.mouth = .3; }
  if (t > board) { hp.look = [16, 0]; hp.mouth = .5; const G = charGeom(CAST.tu, hp); hp.hR = POSE.wave(t, G)[1]; }
  if (t > off) { hp.hR = null; hp.look = [0, 0]; hp.wide = .5; hp.mouth = -.2; }
  if (t > all) { hp.wide = 1; hp.brow = 1; hp.mouth = -.6; hp.jump = Math.abs(Math.sin(t * 9)) * 50; hp.walk = 1; hp.phase = Math.PI * .5; hp.hL = [-40, -60]; hp.hR = [180, -560]; hp.sweat = 1; }
  if (t > yell - .1 && t < Le('s14_09') + .3) { hp.open = .9; }
  if (t > heart) { hp.jump = 0; hp.walk = 0; hp.hL = null; hp.hR = [-20, -470]; hp.wide = 0; hp.brow = .6; hp.mouth = .2; hp.look = [16, -4]; hp.sweat = 0; }
  if (t > Lt('s14_11')) { hp.mouth = .6; hp.brow = .3; }
  say(hp, t, ['s14_03', 's14_04', 's14_09']);
  st.wld(g => drawHero(g, hp));
  if (t > Lt('s14_11')) st.wld(g => tears(g, ...(() => { const h = headInfo('tu', hp); return [h.x + h.r * .28, h.y + h.r * .1]; })(), t, .6));
  compose2(X, st, { amt: 0 });
  sticker(X, 'SÁBADO · 6:55 AM', vis(t, .3, Lt('s14_02') - .2), 70, 70, 64);
  if (t > off - .1 && t < all) { X.save(); X.globalAlpha = bump(t, off - .1, off + .4) * .8; X.fillStyle = '#ffffff'; X.fillRect(0, 0, W, H); X.restore(); sticker(X, 'SE ACABÓ EL PODER', R(t, off, off + .3, back), 70, 70, 70, '#ffb3b3'); }
  // everything from the week arrives at once, then the one that isn't anywhere in the body
  const h = headInfo('tu', hp), parts = [[h.x - 20, FEET - 10], [h.x + 30, FEET - 40], [h.x - 40, FEET - 160], [h.x + 110, h.y + h.r * 2.6], [h.x - h.r * .5, h.y + h.r * .4], [h.x, h.y + h.r * .6]];
  hits(X, cam, t, [...parts.map((at, i) => ({ t: all + .1 + i * .25, at, cname: 'tu', p: hp, hero: 0, val: 10, word: ['¡AY!', '¡AU!', '¡UY!', '¡AY!', '¡AUCH!', '¡AAAY!'][i] })),
    { t: heart, at: heartPt('tu', hp), cname: 'tu', p: hp, hero: 0, val: 6, dur: 1.2, word: '…' }]);
  if (t > yell && t < Le('s14_09') + .6) comicWord(X, '¡AAAAAAY!', ...worldToScreen(cam, h.x + 160, h.y - h.r * 1.6), t - yell, 120, '#ff6b6b', 1.1);
  if (t > heart + 1.0) { const [x, y] = worldToScreen(cam, ...heartPt('tu', hp)); X.save(); X.globalAlpha = R(t, heart + 1, heart + 1.4); heartPopX(X, x, y + 40, .1, 1.4); X.restore(); }
};

/* ================================================================ 15. Pepe: «para saber qué te importa» */
function icePack(g, x, y) { shape(g, q => rrPath(q, x - 44, y - 30, 88, 46, 18), '#a9dcf5', 4); line(g, [[x - 30, y - 14], [x + 30, y - 14]], 'rgba(255,255,255,.8)', 4); }
SC.s15 = (X, t) => {
  const open = Lt('s15_05'), fly = Lt('s15_08') - .1, vanish = Lm('s15_08', .9);
  const cam = shots(t, [], [
    { t: 0, cx: 980, cy: 640, z: 1.3, z2: 1.35, lock: 1 },
    { t: Lt('s15_02') - .05, cx: 920, cy: 540, z: 2.3, z2: 2.4, lock: 1 },
    { t: Lt('s15_03') - .05, cx: 1080, cy: 730, z: 3.0, z2: 3.3, lock: 1 },
    { t: Lt('s15_04') - .05, cx: 920, cy: 540, z: 2.3, z2: 2.4, lock: 1 },
    { t: open - .05, cx: 1040, cy: 680, z: 2.2, z2: 2.3, lock: 1 },
    { t: Lt('s15_06') - .05, cx: 1080, cy: 720, z: 3.2, z2: 3.5, lock: 1 },
    { t: fly, cx: 1100, cy: 520, z: 1.2, z2: 1.15, lock: 1 },
    { t: Lt('s15_09') - .05, cx: 900, cy: 600, z: 1.7, z2: 1.85, lock: 1 },
  ]);
  const st = stage(cam); st.wld(g => { drawSet(g, 'parkNight'); bench(g, 0); bench(g, 1); });
  const hp = benchSit(900, { t, look: [14, 6], mouth: .2, brow: .3 });
  if (t > Lt('s15_06')) { hp.wide = .5; hp.brow = .7; }
  if (t > fly) { hp.look = [14, -14]; hp.mouth = -.2; }
  if (t > Lt('s15_09')) { hp.look = [0, -6]; hp.brow = .7; hp.wide = 0; hp.mouth = -.3; }
  say(hp, t, ['s15_02', 's15_04']);
  st.wld(g => { drawHero(g, hp); icePack(g, 922, 870); });
  let mP = null;
  if (t < fly) st.wld(g => { const u = R(t, open, open + .5, back); wings(g, 1080, 720, .62, u, Math.sin(t * 6) * .2 * u); mP = pigeonTalk(g, 1080, 792, .62, { flip: -1, front: t > Lt('s15_02'), open: openOfP(t, ['s15_03', 's15_06', 's15_07']), tilt: Math.sin(t * 1.1) * .04 }); });
  else { const u = R(t, fly, vanish, lin), px = mix(1080, 1700, u), py = mix(792, 120, io(u)), a = 1 - R(t, vanish - .2, vanish + .2);
    if (a > 0) st.wld(g => { g.save(); g.globalAlpha = a; wings(g, px, py - 70, .62, 1, Math.sin(t * 22)); pigeonTalk(g, px, py, .62, { flip: 1, tilt: -.2 }); g.restore(); }); }
  compose2(X, st, { amt: 0 });
  if (mP) for (const id of ['s15_03', 's15_06', 's15_07']) talkBubble(X, cam, mP[0], mP[1], id, 'RUU', { t, dx: 1, r: 40, size: 62, w: 760 });
  if (t > Lt('s15_09') + .5) { const [x, y] = worldToScreen(cam, 900, 330); X.save(); X.globalAlpha = R(t, Lt('s15_09') + .5, Lt('s15_09') + .8); text(X, '$$$ … ¿?', x, y, 90, '#fde047', 'Bangers', 'center', OUT, 10); X.restore(); }
  if (t > Le('s15_09') + .3) { X.save(); X.globalAlpha = R(t, Le('s15_09') + .3, T().dur, lin); X.fillStyle = '#000'; X.fillRect(0, 0, W, H); X.restore(); }
};

/* ================================================================ 16. is any of this real? */
function dna(g, x, y, t, a) { if (a <= 0) return; g.save(); g.globalAlpha = clamp(a); for (let i = 0; i < 18; i++) { const yy = y + i * 18, ph = i * .5 + t * 1.5, x1 = x + Math.sin(ph) * 60, x2 = x - Math.sin(ph) * 60;
    line(g, [[x1, yy], [x2, yy]], i === 9 ? PAIN_RED : 'rgba(80,100,140,.6)', i === 9 ? 6 : 3); circ(g, x1, yy, 7, '#3a6fb0', 2); circ(g, x2, yy, 7, '#e0453c', 2); } g.restore(); }
function chili(g, x, y, s = 1) { g.save(); g.translate(x, y); g.scale(s, s); g.rotate(-.4); shape(g, q => { q.moveTo(-90, 0); q.quadraticCurveTo(-60, -50, 40, -36); q.quadraticCurveTo(90, -30, 100, 10); q.quadraticCurveTo(10, 10, -90, 0); }, '#d92b2b', 5);
  shape(g, q => { q.moveTo(-90, 0); q.lineTo(-120, -20); q.lineTo(-104, 4); q.closePath(); }, '#3f8a4f', 4); g.restore(); }
function sensor(g, x, y, fire, t) { shape(g, q => rrPath(q, x - 40, y - 60, 80, 120, 18), '#f4d9c8', 5); shape(g, q => rrPath(q, x - 14, y - 60, 28, 120, 6), fire ? '#ffb347' : '#e8c4b0', 3);
  if (fire) for (let i = 0; i < 3; i++) { const f = .8 + .2 * Math.sin(t * 10 + i); shape(g, q => { const bx = x - 30 + i * 30, by = y - 70; q.moveTo(bx, by); q.quadraticCurveTo(bx + 18, by - 30 * f, bx, by - 60 * f); q.quadraticCurveTo(bx - 18, by - 30 * f, bx, by); }, '#ff8a1f', 3); } }
function brainSimple(g, x, y, s, hot) { g.save(); g.translate(x, y); g.scale(s, s); shape(g, q => { q.ellipse(0, 0, 110, 80, 0, 0, 7); }, '#ffb3c8', 6); line(g, [[0, -78], [0, 78]], '#a0506a', 4);
  for (const sx of [-1, 1]) { line(g, [[sx * 20, -50], [sx * 60, -30], [sx * 30, 0]], '#a0506a', 4); line(g, [[sx * 30, 20], [sx * 80, 30]], '#a0506a', 4); }
  if (hot) { g.save(); g.globalAlpha = hot; shape(g, q => q.ellipse(0, -30, 40, 26, 0, 0, 7), '#ff3b3b', 0); g.restore(); } g.restore(); }
SC.s16 = (X, t) => {
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 470, z: 1.12, z2: 1.16, lock: 1 },
    { t: Lt('s16_02') - .05, cx: 900, cy: 420, z: 1.25, z2: 1.3, lock: 1 },
    { t: Lt('s16_04') - .05, cx: 900, cy: 420, z: 1.25, z2: 1.3, lock: 1 },
    { t: Lt('s16_06') - .05, cx: 900, cy: 430, z: 1.2, z2: 1.28, lock: 1 },
    { t: Lt('s16_07') - .05, cx: 1440, cy: 560, z: 1.9, z2: 2.0, lock: 1 },
  ]);
  const red = '#c0262d', ink = '#2d2a40';
  const st = stage(cam);
  st.wld(g => { drawSet(g, 'classroom'); teacherDesk(g, 1620);
    text(g, '¿ALGO DE ESTO ES REAL?', 760, 205, 70, red, 'Bangers', 'center');
    if (t > Lt('s16_02') - .1 && t < Lt('s16_04') - .1) { dna(g, 480, 245, t, R(t, Lt('s16_02'), Lt('s16_02') + .4)); line(g, [[560, 407], [610, 407]], PAIN_RED, 5); text(g, 'UN SOLO GEN', 620, 420, 40, PAIN_RED, 'Bangers', 'left');
      if (t > Lt('s16_03')) { const a = R(t, Lt('s16_03'), Lt('s16_03') + .4); g.save(); g.globalAlpha = a; shape(g, q => rrPath(q, 800, 250, 300, 300, 10), '#fffbe8', 5); text(g, 'REVISAR CADA DÍA:', 950, 300, 32, ink, 'Bangers', 'center');
        ['MANOS ✓', 'PIES ✓', 'BOCA ✓', 'RODILLAS ✓'].forEach((s, i) => text(g, s, 840, 360 + i * 46, 34, '#2f8f4e', 'Bangers', 'left')); g.restore(); } }
    if (t > Lt('s16_04') - .1 && t < Lt('s16_06') - .1) { const a = R(t, Lt('s16_04'), Lt('s16_04') + .4); g.save(); g.globalAlpha = a; chili(g, 520, 420, 1.6); sensor(g, 880, 400, t > Lm('s16_04', .5), t);
        line(g, [[640, 400], [800, 400]], ink, 5); text(g, 'CAPSAICINA', 560, 520, 36, red, 'Bangers', 'center'); text(g, 'SENSOR DE CALOR', 860, 520, 36, ink, 'Bangers', 'center'); g.restore(); }
    if (t > Lt('s16_06') - .1) { const a = R(t, Lt('s16_06'), Lt('s16_06') + .4); g.save(); g.globalAlpha = a; brainSimple(g, 760, 360, 1.1, .5 + .5 * Math.sin(t * 5));
        text(g, 'GOLPE', 470, 300, 40, ink, 'Bangers', 'center'); line(g, [[520, 310], [660, 330]], ink, 5); text(g, 'RECHAZO', 1060, 300, 40, red, 'Bangers', 'center'); line(g, [[1000, 310], [860, 330]], red, 5); g.restore(); }
  });
  st.wld(g => pigeonTalk(g, 1600, 692, .95, { flip: -1, front: 1, tilt: Math.sin(t * 2.2) * .06 }));
  compose2(X, st, { amt: 0 });
  if (t > Lt('s16_02') + .4 && t < Lt('s16_04') - .1) chip(X, 'MUY RARO', 1460, 260, R(t, Lt('s16_02') + .4, Lt('s16_02') + .7));
  if (t > Lt('s16_03') + .4 && t < Lt('s16_04') - .1) chip(X, 'NO ES UN SUPERPODER', 1460, 360, R(t, Lt('s16_03') + .4, Lt('s16_03') + .7), '#ffb3b3');
  if (t > Lt('s16_05') && t < Lt('s16_06') - .1) chip(X, 'PREMIO NOBEL 2021', 1460, 300, R(t, Lt('s16_05') + .2, Lt('s16_05') + .5), '#ffffff');
  if (t > Lt('s16_07')) sticker(X, '«DUELE» SIN QUE TE TOQUEN', R(t, Lm('s16_07', .3), Lm('s16_07', .3) + .25, back), 90, 90, 70);
};

/* ================================================================ 17. call to action, end card */
SC.s17 = (X, t) => {
  const end = Le('s17_04') + .9;
  const cam = shots(t, [], [{ t: 0, cx: 1000, cy: 600, z: 1.25, z2: 1.35, lock: 1 }, { t: Lt('s17_02') - .05, cx: 1080, cy: 735, z: 3.0, z2: 3.3, lock: 1 }, { t: Lt('s17_03') - .05, cx: 940, cy: 560, z: 1.6, z2: 1.7, lock: 1 }, { t: Lt('s17_04') - .1, cx: 1080, cy: 735, z: 3.6, z2: 3.9, lock: 1 }]);
  const st = stage(cam); st.wld(g => { drawSet(g, 'parkNight'); bench(g, 0); bench(g, 1); });
  const rich = t > Lt('s17_03');
  st.wld(g => { const hp = benchSit(900, { t, look: rich ? [10, -16] : [14, 4], mouth: rich ? .7 : .4, brow: rich ? -.3 : 0, footSwing: Math.sin(t * 2.4) * 10 }); drawHero(g, hp); icePack(g, 922, 870); });
  st.wld(g => pigeonTalk(g, 1080, 792, .62, { flip: -1, front: 1, tilt: Math.sin(t * 1.3) * .08 }));
  if (t > Lt('s17_02')) st.wld(g => { g.save(); g.globalAlpha = R(t, Lt('s17_02') + .2, Lt('s17_02') + .5); g.strokeStyle = '#141014'; g.lineWidth = 2.5; for (const s2 of [-1, 1]) { g.beginPath(); g.arc(1061 + s2 * 9, 697, 6.5, 0, 7); g.stroke(); } g.beginPath(); g.moveTo(1058, 697); g.lineTo(1064, 697); g.stroke(); g.restore(); });
  compose2(X, st, { amt: 0 });
  if (t > Lt('s17_01') - .05 && t < Lt('s17_03') - .1) sticker(X, '¿QUÉ HARÍAS SIN DOLOR UN DÍA?', R(t, Lt('s17_01') - .05, Lt('s17_01') + .25, outC), 70, 60, 58);
  if (t > Lt('s17_02') - .05 && t < Lt('s17_03') - .1) { sticker(X, '↓ COMENTARIOS ↓', R(t, Lt('s17_02') - .05, Lt('s17_02') + .25, outC), 70, 180, 60, '#ffffff'); sticker(X, 'PEPE LOS LEE TODOS', R(t, Lm('s17_02', .5), Lm('s17_02', .5) + .25, back), 70, 300, 60); }
  if (rich && t < Lt('s17_04') - .1) { const [x, y] = worldToScreen(cam, 900, 300); const a = R(t, Lt('s17_03') + .2, Lt('s17_03') + .5, back); X.save(); X.globalAlpha = a; text(X, '$ $ $', x, y, 110, '#7ad66a', 'Bangers', 'center', OUT, 12); X.restore(); }
  if (t > Lt('s17_04') && t < end) { const [px, py] = worldToScreen(cam, 1080, 735); dashRing(X, px, py, 70 * cam.z, t); sticker(X, 'NO TE VA A ALCANZAR', R(t, Lt('s17_04') + .3, Lt('s17_04') + .55, back), 70, 70, 70); }
  if (t > end) { const a = R(t, end, end + .5, outC); X.save(); X.globalAlpha = a; X.fillStyle = '#141a2e'; X.fillRect(0, 0, W, H);
    text(X, CHANNEL_NAME, W / 2, 230, 150, '#fde047', 'Bangers', 'center', OUT, 18);
    text(X, 'PRÓXIMO EPISODIO:', W / 2, 400, 64, '#ffffff', 'Bangers', 'center');
    text(X, '¿Y SI TUVIERAS', W / 2, 500, 84, '#ffffff', 'Bangers', 'center', OUT, 10); text(X, 'DINERO INFINITO?', W / 2, 600, 84, '#ffffff', 'Bangers', 'center', OUT, 10);
    shape(X, q => rrPath(q, W / 2 - 300, 720, 600, 130, 22), '#e02424', 7); text(X, 'SUSCRÍBETE', W / 2, 812, 84, '#ffffff', 'Bangers', 'center');
    pigeonTalk(X, 1600, 960, .9, { flip: -1, front: 1, tilt: Math.sin(t * 1.5) * .1 }); X.restore(); }
};
