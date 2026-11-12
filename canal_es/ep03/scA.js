/* Ep03 «¿Qué pasaría si pudieras hablar con los animales?» — scenes 0–5.
   Beats are keyed to narration (Lt/Le/Lm from anim/episode.js). Animals are cut-outs from anim/animals.js; when one talks,
   its mouth follows the voice (talk()) and talkBubble() turns its sound into words. */
SC.missing = (X, t) => { X.fillStyle = '#1b1530'; X.fillRect(0, 0, W, H); text(X, SID + ' (sin animar)', W / 2, H / 2, 90, '#fde047', 'Bangers', 'center'); };
const SOUND = { croqueta: 'MIAU', perro1: 'GUAU', perro2: 'GUAU', perros: 'GUAU', firulais: 'GRRR', bigotes: 'ÑIQ ÑIQ', canela: 'GUAU', palomas: 'RUU RUU', mosquito: 'BZZZ', pepe: 'RUU' };
const vis = (t, a, b, fi = .25, fo = .3) => R(t, a, a + fi) * (1 - R(t, b, b + fo));
const loopU = (t, t0, P) => (((t - t0) % P) + P) % P / P;
/* mouth opening for an animal that speaks any of these lines */
const openOf = (t, ids) => Math.max(0, ...ids.map(id => T().L[id] && speaking(t, id) ? talk(t, id) : 0));
/* the bubble + golden rings for a voiced animal line; m = world point of the mouth */
function say(X, cam, t, id, m, o = {}) { if (!T().L[id] || !m) return; const who = T().L[id][2];
  talkBubble(X, cam, m[0], m[1], id, o.sound || SOUND[who] || '…', Object.assign({ t }, o));
  if (speaking(t, id)) { const [sx, sy] = worldToScreen(cam, m[0], m[1]); soundRings(X, sx, sy, R(t, Lt(id), Lt(id) + .2), t, o.ring || 1); } }
/* an unvoiced gag line in the same bubble */
function gag(X, cam, t, m, t0, d, sound, words, o = {}) { if (!m) return; talkBubble(X, cam, m[0], m[1], null, sound, Object.assign({ t, t0, d, text: words, hold: .5 }, o)); }
function walker(g, n, x0, v, tt, extra = {}) { const x = x0 + v * tt; drawChar(g, n, Object.assign({ x, y: FEET, s: S0, t: tt, walk: 1, phase: walkPh(x), flip: v < 0 ? -1 : 1 }, extra)); return x; }
function standing(x, extra = {}) { return Object.assign({ x, y: FEET, s: S0 }, extra); }
function benchSit(x, extra = {}) { return Object.assign({ x, y: 905, s: S0, sit: 1, noShadow: 1, hL: [-80, -125], hR: [80, -125], armsFront: 1 }, extra); }
function heartPop(g, x, y, u, s = 1) { if (u <= 0 || u >= 1) return; g.save(); g.globalAlpha = 1 - u * u; g.translate(x, y - u * 90); g.scale(s * (.6 + .4 * back(Math.min(1, u * 3))), s * (.6 + .4 * back(Math.min(1, u * 3))));
  shape(g, q => { q.moveTo(0, 18); q.bezierCurveTo(-34, -6, -20, -34, 0, -16); q.bezierCurveTo(20, -34, 34, -6, 0, 18); }, '#ff5d7a', 4); g.restore(); }
function checkSticker(X, s, a, x, y) { if (a <= 0) return; sticker(X, s + '  ✓', a, x, y, 64, '#ffd34d'); }
function rewindFX(X, k, t) { if (k <= 0) return;
  X.save(); X.globalAlpha = .25 * k; X.fillStyle = '#ffffff'; const r = rnd(Math.floor(t * 30));
  for (let i = 0; i < 9; i++) { const y = r() * H, h = 4 + r() * 18; X.fillRect(0, y, W, h); } X.restore();
  X.save(); X.globalAlpha = .55 * k; X.fillStyle = '#0d0b12'; X.fillRect(0, H - 150, W, 150); X.restore();
  X.save(); X.globalAlpha = k; text(X, '◀◀  REBOBINANDO', 70, H - 52, 76, '#ffffff', 'Bangers', 'left', OUT, 10); X.restore(); }
const GANG = [[-10, 1.0], [35, 1.12, .8], [-35, .92, 1.1]];   // tints for the park gang: [hue, brightness, saturation]

/* ================================================================ 0. cold open: the whole park talks to you, except one */
SC.s00 = (X, t) => {
  const rw = Lm('s00_07', .45), tr = t < rw ? t : Math.max(0, rw - (t - rw) * 4);
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 560, z: 1.0, z2: 1.06, lock: 1 },
    { t: Lt('s00_03') - .05, cx: 470, cy: 760, z: 2.2, z2: 2.35, lock: 1 },
    { t: Lt('s00_04') - .05, cx: 1450, cy: 820, z: 2.3, z2: 2.45, lock: 1 },
    { t: Lt('s00_05') - .05, cx: 960, cy: 600, z: 1.05, z2: 1.12, lock: 1 },
    { t: Lt('s00_06') - .05, cx: 1080, cy: 700, z: 2.6, z2: 3.1, lock: 1 },
    { t: rw, cx: 960, cy: 540, z: 1.0, lock: 1 },
  ]);
  const sitT = Lt('s00_03') - .6, runIn = sitT - 1.2;
  const st = stage(cam); st.wld(g => { drawSet(g, 'park');
    if (tr < runIn) { const u = loopU(tr, 0, 4.4), x = -150 + 2250 * u; drawSpr(g, 'dogARun', x, 748, 92, { flip: -1, bob: -Math.abs(Math.sin(tr * 12)) * 8 }); }   // laps on the far path, behind everyone
    bench(g, 0); bench(g, 1); });
  // the golden dog: laps the far path, then runs in and sits in front of you, begging for the ball
  let mDog = null, mGang = null;
  st.col(g => { drawAnimal(g, 'dogB', 190, 945, .62, { t, tilt: Math.sin(t * 2 + 1) * .1 });
    if (tr >= runIn && tr < sitT) { const u = R(tr, runIn, sitT, lin); drawSpr(g, 'dogARun', mix(-160, 470, u), mix(1040, 1010, u), 170, { flip: -1, bob: -Math.abs(Math.sin(tr * 12)) * 14 }); }
    else if (tr >= sitT) mDog = drawAnimal(g, 'dogA', 470, 1010, 1.0, { open: openOf(t, ['s00_03']), t, tilt: Math.sin(t * 3) * .08, bob: -Math.abs(Math.sin(t * 9)) * 6 }); });
  // the gossip gang on the path, right
  st.col(g => { GANG.forEach(([hue, br, sa], i) => { const x = 1340 + i * 120, m = pigeonTalk(g, x, 960 + (i % 2) * 18, .85, { flip: -1, tint: i ? [hue, br, sa] : null, peck: i === 1 ? 0 : Math.max(0, Math.sin(t * 2.6 + i)) * .6, open: i === 1 ? openOf(t, ['s00_04']) : 0 }); if (i === 1) mGang = m; }); });
  const hp = benchSit(900, { t, look: [14, 6], mouth: .2 });
  if (t > Lt('s00_03') && t < Lt('s00_05')) { hp.look = [-16, 10]; hp.mouth = -.1; hp.brow = .3; }
  if (t > Lt('s00_04')) { hp.look = [18, 8]; hp.brow = .6; hp.mouth = -.2; }
  if (t > Lt('s00_06')) { hp.look = [16, 10]; hp.wide = .3; hp.brow = .5; hp.mouth = -.1; }
  if (t > rw) Object.assign(hp, { wide: 0, brow: 0, mouth: .1 });
  st.col(g => drawChar(g, 'tu', hp));
  st.col(g => drawPigeon(g, 1080, 792, .62, { flip: -1, front: t > Lt('s00_06') - .1, tilt: Math.sin(t * 1.1) * .04 }));   // Pepe: silent
  compose2(X, st, { amt: 0 }); window.__cam = cam;
  say(X, cam, t, 's00_03', mDog, { dx: 40, dy: -120 });
  say(X, cam, t, 's00_04', mGang, { dx: -380, dy: -120 });
  if (t > Lt('s00_05') - .1 && t < Lt('s00_06') - .1) {   // the whole park at once: little bubbles everywhere
    const P = [[300, 760, 'GUAU', '¡Hola!'], [1500, 850, 'RUU', '¿Galleta?'], [1700, 600, 'PÍO', '¡Buenos días!'], [600, 640, 'GUAU', '¡Pelota!'], [1250, 380, 'CRUAC', '¿Y este?']];
    P.forEach(([x, y, snd, w], i) => gag(X, cam, t, [x, y], Lt('s00_05') + i * .3, .8, snd, w, { size: 34, w: 300, dy: -60 })); }
  if (t > Lt('s00_06') + .3 && t < rw) { const [px, py] = worldToScreen(cam, 1080, 700); X.save(); X.globalAlpha = R(t, Lt('s00_06') + .3, Lt('s00_06') + .6); X.strokeStyle = '#ffd34d'; X.lineWidth = 8; X.setLineDash([22, 16]); X.lineDashOffset = -t * 60;
    X.beginPath(); X.arc(px, py, 90 * cam.z, 0, 7); X.stroke(); X.restore(); }
  rewindFX(X, R(t, rw, rw + .25), t);
  if (t > T().dur - .25) { X.save(); X.globalAlpha = R(t, T().dur - .25, T().dur, lin); X.fillStyle = '#ffffff'; X.fillRect(0, 0, W, H); X.restore(); }
};

/* ================================================================ 1. the premise: every animal, and they understand you too */
SC.s01 = (X, t) => {
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 540, z: 1.0, z2: 1.06, lock: 1 },
    { t: Lt('s01_02') - .05, cx: 960, cy: 560, z: 1.12, z2: 1.18, lock: 1 },
    { t: Lt('s01_03') - .05, cx: 1180, cy: 700, z: 1.9, z2: 2.0, lock: 1 },
    { t: Lt('s01_04') - .05, cx: 900, cy: 520, z: 1.6, z2: 1.7, lock: 1 },
    { t: Lt('s01_05') - .05, cx: 1180, cy: 470, z: 1.5, z2: 1.58, lock: 1 },   // the pigeon and your face in one shot
  ]);
  const st = stage(cam); st.wld(g => drawSet(g, 'street'));
  const walkEnd = Lt('s01_03') - .3, hx = mix(380, 900, R(t, 0, walkEnd, io)), hp = { x: hx, y: FEET, s: S0, t, walk: t < walkEnd ? 1 : 0, phase: walkPh(hx), look: [10, 0], mouth: .2 };
  let mDog = null, mPig = null, mMos = null;
  st.col(g => { const sit = t > Lt('s01_03') - .4; mDog = sit ? drawAnimal(g, 'dogB', 1240, 960, .9, { t, flip: -1, tilt: t > Lt('s01_03') + .4 ? -.22 : 0, open: t > Lm('s01_03', .5) && t < Lm('s01_03', .5) + .8 ? Math.abs(Math.sin(t * 14)) * .8 : 0 })
      : (drawSpr(g, 'dogBStand', 1300, 965, 170, { flip: 1 }), [1230, 830]); });
  st.col(g => { mPig = pigeonTalk(g, 1460, 345, .6, { flip: -1, open: t > Lt('s01_05') + .4 && t < Lt('s01_05') + 1.6 ? Math.abs(Math.sin(t * 12)) * .8 : 0, tilt: Math.sin(t) * .06 }); });
  if (t > Lt('s01_02') && t < Lt('s01_03') + 1) st.col(g => { const u = R(t, Lm('s01_02', .7), Lm('s01_02', 1.0), lin), x = mix(1700, hx + 70, u), y = 430 + Math.sin(t * 9) * 26; drawSpr(g, 'mosquito', x, y, 70, { flip: -1, rot: Math.sin(t * 20) * .05 }); mMos = [x - 30, y - 40]; });
  if (t > Lt('s01_03')) { hp.look = [16, 8]; hp.mouth = .5; }
  if (t > Lt('s01_03') + .2 && t < Lm('s01_03', .5)) { const G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = POSE.wave(t, G); }
  if (t > Lt('s01_04') && t < Lt('s01_05')) { hp.mouth = .9; hp.brow = -.3; const G = charGeom(CAST.tu, hp); hp.hR = [140, G.top + 20]; }
  if (t > Lt('s01_05') + .4) { hp.look = [18, -10]; hp.mouth = -.3; hp.brow = .7; hp.wide = .3; }
  st.col(g => drawChar(g, 'tu', hp));
  compose2(X, st, { amt: 0 });
  if (t > Lt('s01_02') - .05 && t < Lt('s01_03') - .05) [['PERROS', .02], ['GATOS', .2], ['PÁJAROS', .38], ['MOSQUITOS', .7]].forEach(([s, f], i) => checkSticker(X, s, R(t, Lm('s01_02', f), Lm('s01_02', f) + .12, outC), 90, 90 + i * 118));
  if (mMos && t > Lm('s01_02', .85)) gag(X, cam, t, mMos, Lm('s01_02', .85), .9, 'BZZZ', 'Buenas tardes.', { size: 34, w: 320, dx: 40, dy: -40 });
  if (t > Lt('s01_03')) { const [x, y] = worldToScreen(cam, hx + 40, 330); if (t < Lm('s01_03', .5) + .6) bubble(X, '¡HOLA!', x, y, R(t, Lt('s01_03') + .1, Lt('s01_03') + .4, back) * (1 - R(t, Lm('s01_03', .5) + .4, Lm('s01_03', .5) + .6)), 48); }
  if (mDog) gag(X, cam, t, mDog, Lm('s01_03', .5), .9, 'GUAU', '¡Hola, hola!', { size: 38, w: 320, dx: 40, dy: -110 });
  gag(X, cam, t, mPig, Lt('s01_05') + .4, 1.2, 'RUU', 'Qué peinado tan raro.', { size: 42, w: 420, dx: -380, dy: -90 });
};

/* ================================================================ 2. title card */
SC.s02 = (X, t) => {
  const cam = { cx: 960, cy: 540, z: 1.0 }, st = stage(cam); st.wld(g => { drawSet(g, 'park'); drawSpr(g, 'dogARun', mix(-200, 2100, t / 3.6), 748, 92, { flip: -1, bob: -Math.abs(Math.sin(t * 12)) * 8 }); });
  st.col(g => { drawAnimal(g, 'croqueta', 1500, 980, .8, { head: 'bored', t });
    pigeonTalk(g, 420, 960, .8, { flip: 1, peck: Math.max(0, Math.sin(t * 3)) * .6 }); });
  compose2(X, st, { amt: 0 });
  [[260, 700, 'GUAU'], [1640, 660, 'MIAU'], [380, 840, 'RUU']].forEach(([x, y, s], i) => { const a = R(t, .2 + i * .15, .5 + i * .15, back); if (a > 0) bubble(X, s, x, y - 120, a, 56); });
  titleCard(X, '¿QUÉ PASARÍA SI PUDIERAS', 'HABLAR CON LOS ANIMALES?', R(t, .3, .8, outC), t);
};

/* ================================================================ 3. 5 a.m.: Croqueta has always been talking */
function lyingHead(g, x = 300, y = 680, p = {}) { drawHead(g, CAST.tu, x, y, -1.35, Object.assign({ sleep: 1 }, p)); }
SC.s03 = (X, t) => {
  const up = Lt('s03_06') - .2, plate = Lt('s03_05') - .05;
  const cam = shots(t, [], [
    { t: 0, cx: 640, cy: 640, z: 1.15, z2: 1.2, lock: 1 },
    { t: Lt('s03_02') - .05, cx: 420, cy: 640, z: 1.9, z2: 2.0, lock: 1 },
    { t: Lt('s03_03') - .05, cx: 460, cy: 560, z: 2.6, z2: 2.75, lock: 1 },
    { t: Lt('s03_04') - .05, cx: 360, cy: 660, z: 2.4, z2: 2.5, lock: 1 },
    { t: plate, cx: 1250, cy: 900, z: 2.6, z2: 2.8, lock: 1 },
    { t: up, cx: 560, cy: 620, z: 1.45, z2: 1.5, lock: 1 },
    { t: Lt('s03_07') - .05, cx: 470, cy: 560, z: 2.3, z2: 2.4, lock: 1 },
    { t: Lt('s03_09') - .05, cx: 640, cy: 600, z: 1.15, z2: 1.2, lock: 1 },
  ]);
  const st = stage(cam); st.wld(g => { drawSet(g, 'bedroom'); bedBack(g); nightstand(g); propAlarm(g, 1075, 740, .55, 5, 0, t < Lt('s03_02') ? 1 : 0); });
  st.wld(g => drawSpr(g, 'bowl', 1250, 940, 70));
  st.col(g => drawPigeon(g, 1380, 562, .45, { flip: -1, tilt: Math.sin(t * .7) * .1 }));   // Pepe on the sill, silent
  // the hero: asleep, woken, then sitting up out of bed
  let hp = null;
  if (t < up) st.col(g => lyingHead(g, 300, 680, { sleep: t < Lt('s03_04'), mouth: t > Lt('s03_04') ? -.2 : .2, wide: t > Lt('s03_04') ? .7 : 0, look: [16, -6], brow: t > Lt('s03_04') ? .6 : null }));
  else { hp = { x: 640, y: FEET, s: S0, t, look: [-16, -2], mouth: -.1, brow: .6, wide: .5 };
    if (t < up + .3) { hp.hy = -40 * (1 - (t - up) / .3); }
    if (speaking(t, 's03_06')) { hp.open = talk(t, 's03_06'); hp.wide = .8; }
    if (t > Lt('s03_07')) { hp.wide = .3; hp.brow = .3; hp.mouth = -.2; }
    st.col(g => drawChar(g, 'tu', hp)); }
  st.wld(g => bedFront(g, t < up ? 1 : .6));
  // Croqueta: paws on your face (a little stomp), then sits on the pillow and lectures you
  let mCat = null;
  st.col(g => { const lect = t > up; const x = lect ? 380 : 410, y = lect ? 716 : 690, stomp = !lect && t > Lt('s03_02') && t < Lt('s03_04') ? Math.abs(Math.sin(t * 8)) * 10 : 0;
    mCat = drawAnimal(g, 'croqueta', x, y + stomp * .4, .9, { head: 'bored', t, open: openOf(t, ['s03_03', 's03_05', 's03_07', 's03_08']), tilt: Math.sin(t * 1.3) * .05 - (lect ? .06 : 0), squash: stomp * .004 }); });
  compose2(X, st, { amt: 0 });
  if (t < Lt('s03_04')) zzz(X, ...worldToScreen(cam, 300, 560), t, 1 - R(t, Lt('s03_03'), Lt('s03_03') + .3));
  for (const id of ['s03_03', 's03_05', 's03_07', 's03_08']) say(X, cam, t, id, mCat, { r: 70, w: 500 });   // above the cat, narrow: never over your face
  if (t > plate && t < up) sticker(X, 'VACÍO', R(t, plate + .3, plate + .5, back), ...worldToScreen(cam, 1180, 760), 60, '#ffffff');
  if (t > Lt('s03_09') - .05) { const items = ['LA COMIDA: CARTÓN', 'TU MÚSICA: NO', 'TUS AMIGOS: TAMPOCO'];
    sticker(X, 'OPINIONES DE CROQUETA', R(t, Lt('s03_09'), Lt('s03_09') + .2, outC), 1040, 120, 56, '#ffd34d');
    items.forEach((s, i) => sticker(X, s, R(t, Lm('s03_09', .3 + i * .22), Lm('s03_09', .3 + i * .22) + .2, outC), 1080, 240 + i * 100, 46, '#ffffff')); }
};

/* ================================================================ 4. the kitchen: Croqueta snitches on mom */
SC.s04 = (X, t) => {
  const rule = Lt('s04_08') - .2;
  const cam = shots(t, [], [
    { t: 0, cx: 900, cy: 560, z: 1.0, z2: 1.05, lock: 1 },
    { t: Lt('s04_02') - .05, cx: 1420, cy: 780, z: 2.1, z2: 2.2, lock: 1 },
    { t: Lt('s04_03') - .05, cx: 780, cy: 560, z: 1.45, z2: 1.5, lock: 1 },
    { t: Lt('s04_04') - .05, cx: 900, cy: 480, z: 2.2, z2: 2.3, lock: 1 },
    { t: Lt('s04_05') - .05, cx: 1300, cy: 600, z: 1.35, z2: 1.4, lock: 1 },
    { t: Lt('s04_06') - .05, cx: 1430, cy: 780, z: 2.5, z2: 2.6, lock: 1 },
    { t: Lt('s04_07') - .05, cx: 860, cy: 520, z: 1.7, z2: 1.75, lock: 1 },
    { t: rule, cx: 960, cy: 560, z: 1.0, lock: 1 },
  ]);
  const st = stage(cam); st.wld(g => drawSet(g, 'kitchen'));
  st.col(g => drawPigeon(g, 1560, 420, .4, { flip: -1, tilt: Math.sin(t * .6) * .12 }));
  // mom: cooking, then caught, hiding the wrapper behind her back
  const mp = standing(960, { t, look: [-12, 6], mouth: .2 });
  if (t < Lt('s04_03')) { mp.hR = [70, -440]; mp.look = [6, 18]; }
  if (t > Lt('s04_03')) { mp.look = [-16, 2]; mp.wide = .4; mp.hL = [-40, -300]; mp.hR = [120, -260]; }
  if (speaking(t, 's04_04')) { mp.open = talk(t, 's04_04'); mp.brow = .6; mp.wide = .6; }
  if (speaking(t, 's04_07')) { mp.open = talk(t, 's04_07'); mp.brow = .9; mp.wide = .3; mp.look = [-14, 4]; }
  if (t > Le('s04_07')) { mp.brow = .9; mp.mouth = -.2; }
  st.wld(g => drawChar(g, 'mama', mp));
  if (t > Lt('s04_03')) st.wld(g => drawSpr(g, 'choco', 1080, 760, 70, { rot: .3 }));   // half hidden behind her
  st.wld(g => kitchenTable(g));
  const hp = standing(560, { t, look: [14, 0], mouth: .2 });
  if (t > Lt('s04_02') && t < Lt('s04_03')) { hp.look = [18, 12]; hp.wide = .5; hp.brow = .6; hp.mouth = -.1; }
  if (speaking(t, 's04_03')) { hp.open = talk(t, 's04_03'); hp.look = [16, -2]; hp.brow = .5; }
  if (t > Lt('s04_05') - .1 && t < Lt('s04_07')) { hp.look = [18, 12]; hp.brow = .6; hp.lid = .3; hp.mouth = -.2; }
  if (t > Lt('s04_07')) { hp.look = [14, -2]; hp.sweat = 1; hp.mouth = -.3; hp.wide = .4; }
  st.col(g => drawChar(g, 'tu', hp));
  let mCat = null;
  st.col(g => { mCat = drawAnimal(g, 'croqueta', 1430, 960, .85, { head: 'bored', t, flip: -1, open: openOf(t, ['s04_02', 's04_06']), tilt: speaking(t, 's04_06') || t > Le('s04_06') ? .32 : Math.sin(t * 1.2) * .05 }); });
  compose2(X, st, { amt: 0 });
  say(X, cam, t, 's04_02', mCat, { dx: -620, dy: -120 }); say(X, cam, t, 's04_06', mCat, { dx: -520, dy: -110 });
  if (t > Lt('s04_02') + .8 && t < Lt('s04_03')) { const [x, y] = worldToScreen(cam, 1610, 640), a = R(t, Lt('s04_02') + .8, Lt('s04_02') + 1.1, back); X.save(); X.globalAlpha = a; X.translate(x, y); X.scale(a, a);
    circ(X, 0, 0, 90, '#ffffff', 6); X.drawImage(ANI.choco, -40, -60, 80, 110); line(X, [[-50, -50], [50, 50]], '#e02424', 12); X.restore(); }
  if (t > Le('s04_07') + .1 && t < rule) comicWord(X, '¿?', ...worldToScreen(cam, 900, 260), t - Le('s04_07') - .1, 90);
  ruleCard(X, 1, 'ENTIENDES A LOS ANIMALES. ELLOS A TI.', t > Lt('s04_09') - .1 ? 'LOS DEMÁS SOLO OYEN «MIAU»… Y A TI' : '', R(t, rule, rule + .4, outC));
};

/* ================================================================ 5. on the way to school: every dog loves you. Almost every dog. */
function fence(g, x0, x1, y = 960, h = 230) { for (let x = x0; x < x1; x += 46) shape(g, q => { q.moveTo(x, y); q.lineTo(x, y - h); q.lineTo(x + 18, y - h - 20); q.lineTo(x + 36, y - h); q.lineTo(x + 36, y); q.closePath(); }, '#e8d7b9', 4);
  for (const yy of [y - h * .3, y - h * .78]) shape(g, q => q.rect(x0 - 10, yy - 10, x1 - x0 + 20, 20), '#d8c4a1', 4); }
function mailman(g, x, t, extra = {}) { const p = Object.assign({ x, y: FEET, s: S0, t, walk: 1, phase: walkPh(x), flip: -1, look: [-10, 0], mouth: .2, hR: [90, -360],
  holdR: (q, hx, hy) => { q.save(); q.translate(hx, hy - 20); q.rotate(-.2); shape(q, k => rrPath(k, -34, -22, 68, 44, 4), '#f4f1ea', 4); line(q, [[-34, -22], [0, 4], [34, -22]], OUT, 3); q.restore(); } }, extra); drawChar(g, 'ex3', p); }
SC.s05 = (X, t) => {
  const firuT = Lt('s05_05') - .05;
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 540, z: 1.0, z2: 1.05, lock: 1 },
    { t: Lt('s05_02') - .05, cx: 1180, cy: 760, z: 2.0, z2: 2.1, lock: 1 },
    { t: Lt('s05_03') - .05, cx: 1440, cy: 780, z: 2.2, z2: 2.3, lock: 1 },
    { t: Lt('s05_04') - .05, cx: 1000, cy: 600, z: 1.2, z2: 1.3, lock: 1 },
    { t: firuT, cx: 1400, cy: 720, z: 1.6, z2: 1.7, lock: 1 },
    { t: Lt('s05_06') - .05, cx: 1440, cy: 690, z: 2.6, z2: 2.8, lock: 1 },
    { t: Lt('s05_08') - .05, cx: 1200, cy: 560, z: 1.25, z2: 1.3, lock: 1 },
  ]);
  const st = stage(cam); st.wld(g => drawSet(g, 'street'));
  let mA = null, mB = null, mF = null;
  if (t < firuT) {
    const walkEnd = Lt('s05_02') - .3, hx = mix(300, 860, R(t, 0, walkEnd, io));
    const hp = { x: hx, y: FEET, s: S0, t, walk: t < walkEnd ? 1 : 0, phase: walkPh(hx), look: [12, 6], mouth: .3 };
    if (t > Lt('s05_02')) { hp.look = [16, 12]; hp.mouth = .7; hp.brow = -.2; }
    if (t > Lt('s05_04')) { const G = charGeom(CAST.tu, hp); hp.hL = [-110, G.top + 200]; hp.hR = [130, G.top + 230]; hp.mouth = 1; }
    st.col(g => drawChar(g, 'tu', hp));
    const arrive = Lt('s05_02') - .4;
    st.col(g => { if (t < arrive) { drawSpr(g, 'dogARun', mix(1950, 1200, R(t, arrive - 1.6, arrive, lin)), 990, 170, { flip: 1, bob: -Math.abs(Math.sin(t * 12)) * 14 }); drawSpr(g, 'dogBStand', mix(2100, 1460, R(t, arrive - 1.2, arrive + .3, lin)), 995, 150, { flip: 1, bob: -Math.abs(Math.sin(t * 11)) * 10, rot: Math.sin(t * 11) * .04 }); }
      else { mA = drawAnimal(g, 'dogA', 1180, 1000, .95, { t, open: openOf(t, ['s05_02']), tilt: Math.sin(t * 4) * .1, bob: -Math.abs(Math.sin(t * 10)) * 5 });
        mB = drawAnimal(g, 'dogB', 1450, 1005, .9, { t, open: openOf(t, ['s05_03']), tilt: Math.sin(t * 5 + 1) * .12, bob: -Math.abs(Math.sin(t * 11)) * 6 }); } });
    st.col(g => { if (t > Lt('s05_04')) for (let i = 0; i < 6; i++) heartPop(g, [1150, 1210, 1420, 1480, 1300, 1000][i], 760 - (i % 2) * 40, loopU(t, Lt('s05_04') + i * .25, 1.5), .9); });
  } else {
    st.wld(g => { const mx = mix(2150, -250, R(t, Lt('s05_06') - .3, Le('s05_07') + 1.5, lin)); mailman(g, mx, t, { s: .6, y: 860 }); });   // the mailman walks past on the far sidewalk, untouched
    st.wld(g => { mF = drawAnimal(g, 'firu', 1440, 990, 1.0, { t, open: openOf(t, ['s05_06', 's05_07']), tilt: Math.sin(t * .8) * .03, flip: t > Le('s05_06') ? -1 : 1 }); fence(g, 1180, 1720, 1000, 120); });
    st.col(g => drawChar(g, 'tu', standing(820, { t, look: [16, 4], mouth: -.1, brow: .4 })));
  }
  compose2(X, st, { amt: 0 });
  say(X, cam, t, 's05_02', mA, { dx: -420, dy: -120 }); say(X, cam, t, 's05_03', mB, { dx: 1 });
  say(X, cam, t, 's05_06', mF, { dx: -560, dy: -110 }); say(X, cam, t, 's05_07', mF, { dx: -520, dy: -110 });
  if (t > Lt('s05_08') - .05) bigCounter(X, 'FIRULAIS VS. CARTERO:', t > Lt('s05_09') - .05 ? '0 – 2555' : '0 – …', R(t, Lt('s05_08'), Lt('s05_08') + .25, outC));
};
