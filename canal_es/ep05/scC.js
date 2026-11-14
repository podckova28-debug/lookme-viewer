/* Ep05 — scenes 12–17: back to Friday and the easiest question, «no sé», the cinema, the theory about Pepe, the science, the end card */
function lyingHead(g, x = 300, y = 680, p = {}) { drawHead(g, CAST.tu, x, y, -1.35, Object.assign({ sleep: 1 }, p)); }
function wings(g, x, y, s, u, flap = 0) { if (u <= 0) return; g.save(); g.translate(x, y); g.scale(s, s);
  for (const sd of [-1, 1]) { g.save(); g.scale(sd, 1); g.rotate(-.5 * u - flap * .5); shape(g, q => { q.moveTo(0, 0); q.quadraticCurveTo(120 * u, -110 * u, 200 * u, -40 * u); q.quadraticCurveTo(130 * u, 10, 0, 30); q.closePath(); }, '#8d93a6', 4);
    for (let i = 0; i < 3; i++) line(g, [[60 * u + i * 40 * u, -30 * u], [90 * u + i * 40 * u, 10]], '#6a7086', 3); g.restore(); }
  g.restore(); }
const openOfP = (t, ids) => Math.max(0, ...ids.map(id => T().L[id] && speaking(t, id) ? talk(t, id) : 0));
function screenFlicker(X, a, t, col = 'rgba(120,160,255,') { if (a <= 0) return; const k = .14 + .08 * Math.sin(t * 7) * Math.sin(t * 2.3); X.save(); X.setTransform(1, 0, 0, 1, 0, 0);
  X.globalCompositeOperation = 'screen'; const gr = X.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, col + (k * a) + ')'); gr.addColorStop(1, col + '0)'); X.fillStyle = gr; X.fillRect(0, 0, W, H); X.restore(); }
function chip(g, s, x, y, a, col = '#ffd34d') { if (a <= 0) return; g.save(); g.globalAlpha = clamp(a); g.font = '46px Bangers'; const w = g.measureText(s).width + 40; g.translate(x, y); g.scale(.8 + .2 * back(a), .8 + .2 * back(a));
  shape(g, q => rrPath(q, -w / 2, -34, w, 68, 16), col, 5); text(g, s, 0, 17, 46, '#141014', 'Bangers', 'center'); g.restore(); }

/* ================================================================ 12. back to Friday: the problem, the tears, the question */
SC.s12 = (X, t) => {
  const solveT = Lt('s12_03') - .1, cryT = Lt('s12_04') - .05, doorT = Lt('s12_05') - .05, stuck = Lt('s12_07') - .1, tree = Lt('s12_08') - .05, sub = Lt('s12_09') - .05, many = Lt('s12_10') - .05, hola = Lt('s12_11') - .3;
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 540, z: 1.0, z2: 1.04, lock: 1 },
    { t: Lt('s12_02') - .05, cx: 1100, cy: 420, z: 1.6, z2: 1.7, lock: 1 },
    { t: solveT, cx: 880, cy: 680, z: 2.6, z2: 2.75, lock: 1 },
    { t: cryT, cx: 1400, cy: 470, z: 2.2, z2: 2.3, lock: 1 },
    { t: doorT, cx: 560, cy: 600, z: 1.35, z2: 1.42, lock: 1 },
    { t: Lt('s12_06') - .05, cx: 330, cy: 520, z: 2.3, z2: 2.4, lock: 1 },
    { t: stuck, cx: 860, cy: 500, z: 1.8, z2: 1.9, lock: 1 },
    { t: tree, cx: 860, cy: 420, z: 1.25, z2: 1.3, lock: 1 },
    { t: many, cx: 860, cy: 480, z: 1.35, z2: 1.55, lock: 1 },
    { t: hola, cx: 640, cy: 520, z: 1.7, z2: 1.75, lock: 1 },
  ]);
  const st = stage(cam);
  const door = R(t, doorT - .3, doorT + .3), solved = R(t, cryT + .6, cryT + 1.2);
  const pp = standing(1450, { t, flip: -1, look: [-14, 0], mouth: .2, brow: .3, hR: [-150, -470] });
  if (t > solveT) { pp.look = [-16, 10]; pp.hR = null; pp.wide = .4; }
  if (t > cryT) { pp.hR = [70, -420]; pp.holdR = (g, x, y) => drawSpr(g, 'notebook', x, y + 30, 70, { rot: -.2 }); pp.look = [-6, 16]; pp.mouth = -.4; pp.brow = 1; pp.lid = .3; pp.cry = 1; pp.wide = 0; }
  say(pp, t, ['s12_04']);
  const rp = standing(t > hola ? mix(170, 560, R(t, hola, hola + .8)) : 170, { t, look: [14, 4], mouth: .2, brow: -.2, blush: .3 });
  if (t < doorT - .2) rp.x = -300;
  if (t > hola) { rp.walk = t < hola + .8 ? 1 : 0; rp.phase = walkPh(rp.x); }
  if (t > stuck + 1.5) { rp.look = [16, 2]; rp.brow = .3; rp.mouth = -.1; }
  if (t > hola + .6) { const G = charGeom(CAST.valeria, rp); rp.hR = POSE.wave(t, G)[1]; rp.brow = .6; }
  say(rp, t, ['s12_06', 's12_11']);
  const hp = seated(860, { t, look: [-6, -8], mouth: .2, hL: [-70, -170], hR: [70, -170] });
  if (t > solveT && t < cryT) { hp.hR = [60 + Math.sin(t * 30) * 20, -175]; hp.holdR = (g, x, y) => pencil(g, x, y); hp.look = [0, 18]; hp.brow = -.5; }
  if (t > cryT) { hp.look = [16, -2]; hp.mouth = .5; hp.brow = -.3; }
  if (t > doorT) { hp.look = [-16, 2]; hp.mouth = .2; hp.brow = 0; }
  if (t > stuck) { hp.look = [-14, -4]; hp.wide = .6; hp.mouth = -.1; hp.brow = .3; }
  if (t > many) { hp.wide = 1; hp.mouth = -.4; hp.brow = 1; hp.sweat = 1; hp.look = [0, -6]; }
  classroomFriday(st, t, { solved, door, hp, pp, rp });
  const gm = geniusState(t, [[solveT + .1, cryT - .2], [stuck, 99]], cam, headPt('tu', hp, 60));
  const [hx, hy] = headPt('tu', hp);
  genius(X, st, gm, t, [
    { k: 'label', at: [950, 610], s: '∑ … = 2π · 7/3', t0: solveT + .4, size: 50, out: cryT - .2 }, { k: 'label', at: [950, 680], s: 'Q.E.D. ✓', t0: solveT + 1.1, size: 58, col: GEN_YEL, out: cryT - .2 },
    { k: 'line', a: [hx, hy - 30], b: [560, 230], t0: tree + .1, d: .4 }, { k: 'line', a: [hx, hy - 30], b: [1160, 230], t0: tree + .1, d: .4 },
    { k: 'label', at: [560, 210], s: '¿INVITACIÓN? 51%', t0: Lm('s12_08', .1), align: 'center', col: GEN_YEL, size: 54 },
    { k: 'label', at: [1160, 210], s: '¿TAREA? 49%', t0: Lm('s12_08', .55), align: 'center', col: GEN_YEL, size: 54 },
    { k: 'line', a: [560, 230], b: [420, 360], t0: sub, d: .3 }, { k: 'line', a: [1160, 230], b: [1300, 360], t0: sub, d: .3 },
    { k: 'label', at: [420, 400], s: 'DICES SÍ, ERA TAREA: MAL', t0: Lm('s12_09', .05), size: 44, align: 'center', col: GEN_RED },
    { k: 'label', at: [1300, 400], s: 'DICES NO, ERA CITA: PEOR', t0: Lm('s12_09', .55), size: 44, align: 'center', col: GEN_RED },
  ], t > many ? 1 : 0);
  const [sx, sy] = worldToScreen(cam, hx, hy);
  if (t > stuck) calcBar(X, sx, sy - 120, R(t, stuck + .2, stuck + .5) * (1 - R(t, tree - .2, tree)), Math.min(12, (t - stuck) * 20), t > stuck + .8 ? 1 : 0, t);
  if (t > many) { storm(X, sx, sy + 40, t, many + .1, R(t, many, many + .3) * (1 - R(t, hola - .4, hola)), ['SÍ', 'NO', '¿POR QUÉ?', '¿QUÉ DÍA?', 'DEPENDE', 'CLARO', 'TENGO TAREA', '¿ES UNA CITA?', '¿A QUÉ HORA?', 'SÍ… DIGO, NO', '¿CON QUIÉN?', 'ME TENGO QUE IR'], 1, 4000, 2.2);
    smoke(X, sx, sy - 10, t, R(t, many + .8, many + 1.2), cam.z * .7);
    if (t > Le('s12_10') - .2) { X.save(); X.globalAlpha = R(t, Le('s12_10') - .2, Le('s12_10') + .1); X.font = 'bold 54px ComicNeue'; X.textAlign = 'center'; X.lineWidth = 9; X.strokeStyle = 'rgba(8,24,52,.85)'; X.fillStyle = GEN_RED;
      X.strokeText('RESPUESTAS: 0', sx, sy - 230); X.fillText('RESPUESTAS: 0', sx, sy - 230); X.restore(); } }
  sticker(X, 'VIERNES', vis(t, .3, Lt('s12_02') - .2), 70, 70, 64);
  if (t > cryT + 1 && t < doorT) sticker(X, 'TRESCIENTOS AÑOS', R(t, cryT + .3, cryT + .6, back), 70, 70, 62);
};

/* ================================================================ 13. «no sé»: the first time all week */
SC.s13 = (X, t) => {
  const off = Lm('s13_04', .55), cine = Lt('s13_07') - .05, rule = Lt('s13_10') - .1;
  const cam = shots(t, [], [
    { t: 0, cx: 860, cy: 520, z: 2.0, z2: 2.1, lock: 1 },
    { t: Lt('s13_02') - .05, cx: 760, cy: 460, z: 1.3, z2: 1.35, lock: 1 },
    { t: Lt('s13_03') - .05, cx: 600, cy: 470, z: 2.0, z2: 2.1, lock: 1 },
    { t: Lt('s13_04') - .05, cx: 860, cy: 520, z: 2.2, z2: 2.0, lock: 1 },
    { t: Lt('s13_05') - .05, cx: 720, cy: 520, z: 1.6, z2: 1.65, lock: 1 },
    { t: Lt('s13_06') - .05, cx: 860, cy: 500, z: 2.3, z2: 2.4, lock: 1 },
    { t: cine, cx: 580, cy: 470, z: 2.3, z2: 2.4, lock: 1 },
    { t: Lt('s13_08') - .05, cx: 860, cy: 500, z: 2.2, z2: 2.3, lock: 1 },
    { t: Lt('s13_09') - .05, cx: 700, cy: 520, z: 1.5, z2: 1.55, lock: 1 },
  ]);
  const st = stage(cam);
  const leave = Le('s13_09') + .3;
  const rp = standing(560, { t, look: [16, 4], mouth: -.1, brow: .4 });
  if (t > Lt('s13_05')) { rp.brow = -.1; rp.look = [16, 2]; rp.mouth = .2; }
  if (t > cine) { rp.blush = .6; rp.look = [16, 8]; rp.hL = [-60, -300]; rp.hR = [60, -300]; }
  if (t > Lt('s13_08')) { rp.mouth = .6; rp.brow = -.4; rp.hL = null; rp.hR = null; rp.blush = .8; }
  if (t > leave) { const u = R(t, leave, leave + 1.6, lin); rp.x = mix(560, 150, u); rp.walk = u < 1 ? 1 : 0; rp.phase = walkPh(rp.x); rp.flip = -1; rp.look = [-14, 0]; }
  say(rp, t, ['s13_07', 's13_09']);
  const pp = standing(1450, { t, flip: -1, look: [-14, 4], mouth: .2, brow: .2, hR: [70, -420], holdR: (g, x, y) => drawSpr(g, 'notebook', x, y + 30, 70, { rot: -.2 }) });
  if (t > Lt('s13_08')) { pp.look = [-16, 0]; pp.mouth = .4; pp.wide = .3; pp.brow = -.2; }
  const hp = seated(860, { t, look: [-14, -4], wide: .6, mouth: -.1, brow: .3, hL: [-70, -170], hR: [70, -170] });
  if (t > off) { hp.wide = 0; hp.brow = .1; hp.mouth = .1; hp.look = [-16, 0]; }
  if (t > Lt('s13_06')) { hp.mouth = .3; hp.blush = .3; }
  if (t > Lt('s13_08') - .1) { hp.look = [-16, -2]; hp.wide = .5; hp.brow = -.3; hp.blush = .7; }
  if (t > leave) { hp.mouth = .9; hp.blush = .9; hp.look = [-16, 0]; }
  say(hp, t, ['s13_05', 's13_08']);
  classroomFriday(st, t, { solved: 1, door: 1, hp, pp, rp });
  const gm = geniusState(t, [[-1, off]], cam, headPt('tu', hp, 60));
  genius(X, st, gm, t, [
    { k: 'label', at: [760, 240], s: 'CLIMA ✓', t0: Lm('s13_02', .2), size: 46 }, { k: 'label', at: [760, 300], s: 'TRÁFICO ✓', t0: Lm('s13_02', .4), size: 46 },
    { k: 'label', at: [760, 360], s: 'FRIJOLES EN UN FRASCO ✓', t0: Lm('s13_02', .7), size: 46 },
    { k: 'box', at: [560, 640], w: 250, h: 640, t0: Lt('s13_03') + .1, col: GEN_RED, s: 'LO QUE PIENSA ELLA', size: 34 },
    { k: 'label', at: [560, 470], s: '???', t0: Lm('s13_03', .5), size: 90, col: GEN_RED, align: 'center', bg: 0 },
  ]);
  if (t > Lt('s13_06') + .2 && t < cine) sticker(X, 'VECES QUE DIJISTE «NO SÉ»: 1', R(t, Lt('s13_06') + .2, Lt('s13_06') + .5, back), 70, 70, 60, '#ffffff');
  if (t > leave + .2) { const [x, y] = worldToScreen(cam, 860, 330); heartPopX(X, x, y, loopU(t, leave, 1.2), 1.4); }
  ruleCard(X, 3, 'A VECES, LO MÁS INTELIGENTE ES «NO SÉ»', 'Y LUEGO, PREGUNTAR', R(t, rule, rule + .3, outC));
};

/* ================================================================ 14. the cinema: you know the ending and you say nothing */
SC.s14 = (X, t) => {
  const on = Lt('s14_02') + .2, shut = Lt('s14_03') - .05, off = Lt('s14_05') - .2, laugh = Lt('s14_08') - .05;
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 600, z: 1.05, z2: 1.1, lock: 1 },
    { t: on - .2, cx: 960, cy: 560, z: 1.25, z2: 1.3, lock: 1 },
    { t: shut, cx: 860, cy: 620, z: 2.3, z2: 2.4, lock: 1 },
    { t: Lt('s14_05') - .05, cx: 960, cy: 640, z: 1.6, z2: 1.65, lock: 1 },
    { t: Lt('s14_07') - .05, cx: 1060, cy: 620, z: 2.3, z2: 2.4, lock: 1 },
    { t: laugh, cx: 960, cy: 640, z: 1.5, z2: 1.6, lock: 1 },
  ]);
  const st = stage(cam); st.wld(g => drawSet(g, 'cine'));
  st.wld(g => { drawChar(g, 'ex5', { x: 420, y: 1120, s: .9, sit: 1, noShadow: 1, t, look: [0, -12], mouth: .1 }); drawChar(g, 'ex2', { x: 1520, y: 1120, s: .9, sit: 1, noShadow: 1, t, look: [0, -12], mouth: .3 }); });
  const rp = { x: 1080, y: 1120, s: .9, sit: 1, noShadow: 1, t, look: [0, -12], mouth: .3, hR: [-60, -250], hL: [-140, -260] };
  if (t > Lt('s14_05') - .1) { rp.look = [-16, 0]; rp.mouth = .4; rp.brow = -.3; }
  if (t > Lt('s14_07') - .1) { rp.look = [-14, 2]; rp.lid = .35; rp.mouth = .7; rp.brow = -.6; }
  if (t > laugh) { rp.lid = 0; rp.sleep = 1; rp.mouth = 1; rp.open = .5 + .3 * Math.abs(Math.sin(t * 9)); rp.blush = .7; rp.rot = Math.sin(t * 8) * .05; rp.hR = [40, -400]; }
  say(rp, t, ['s14_05', 's14_07']);
  st.wld(g => drawChar(g, 'valeria', rp));
  const hp = { x: 840, y: 1120, s: .9, sit: 1, noShadow: 1, t, look: [0, -12], mouth: .4, hR: [110, -260], hL: [-60, -250], holdR: (g, x, y) => drawSpr(g, 'popcorn', x + 10, y + 40, 120) };
  if (t > on) { hp.look = [0, -14]; hp.brow = -.5; hp.mouth = .6; }
  if (t > shut) { hp.mouth = -.6; hp.brow = .7; hp.wide = .3; hp.look = [10, -4]; }
  if (t > Lt('s14_05')) { hp.look = [16, 0]; hp.mouth = .1; hp.brow = .2; hp.wide = 0; }
  if (t > Lt('s14_06') - .1) { hp.wide = .9; hp.brow = -.6; hp.mouth = .7; }
  if (t > Lt('s14_07')) { hp.wide = .2; hp.blush = .7; hp.mouth = .4; hp.look = [16, 4]; }
  if (t > laugh) { hp.mouth = .9; hp.sleep = 0; hp.blush = .9; }
  say(hp, t, ['s14_06']);
  st.col(g => drawChar(g, 'tu', hp));
  const gm = geniusState(t, [[on, off]], cam, headPt('tu', hp, 60));
  genius(X, st, gm, t, [
    { k: 'label', at: [560, 200], s: 'MINUTO 3 DE 118', t0: on + .3, size: 40 },
    { k: 'label', at: [560, 260], s: 'EL MALO: EL TÍO', t0: Lm('s14_02', .4), size: 44, col: GEN_YEL },
    { k: 'label', at: [560, 320], s: 'SE SALVAN: TODOS MENOS EL TÍO', t0: Lm('s14_02', .58), size: 40 },
    { k: 'label', at: [560, 380], s: 'EL PERRO: ES UN ROBOT', t0: Lm('s14_02', .8), size: 44, col: GEN_RED },
    { k: 'line', a: [540, 248], b: [1280, 392], t0: Lt('s14_04') + .5, d: .5, lw: 7, col: GEN_RED },
    { k: 'label', at: [470, 450], s: 'NO DECIR NADA: 99% DIFÍCIL', t0: shut + .3, size: 44, col: GEN_YEL },
  ]);
  screenFlicker(X, 1 - gm.a, t);
  if (t > shut + .2 && t < Lt('s14_05') - .2) { const mp2 = mouthPt('tu', hp), [x, y] = worldToScreen(cam, mp2[0], mp2[1] + 26); X.save(); X.globalAlpha = R(t, shut + .2, shut + .5); X.strokeStyle = '#141014'; X.lineWidth = 7; X.beginPath(); X.moveTo(x - 40, y); X.lineTo(x + 40, y); X.stroke();
    for (let i = -3; i <= 3; i++) { X.beginPath(); X.moveTo(x + i * 11, y - 8); X.lineTo(x + i * 11, y + 8); X.stroke(); } X.restore(); }
  sticker(X, 'SÁBADO · CINE', vis(t, .3, on - .3), 70, 70, 64);
  if (t > laugh + .3) { const [x, y] = worldToScreen(cam, 1080, 520); X.save(); X.globalAlpha = R(t, laugh + .3, laugh + .6); X.font = 'bold 46px ComicNeue'; X.textAlign = 'center'; X.lineWidth = 8; X.strokeStyle = 'rgba(8,24,52,.85)'; X.fillStyle = GEN_YEL;
    X.strokeText('NO CALCULADO', x, y - 140); X.fillText('NO CALCULADO', x, y - 140); X.restore(); heartPopX(X, x, y - 40, loopU(t, laugh, 1.1), 1.2); }
};

/* ================================================================ 15. the theory: «tú me das los poderes» */
SC.s15 = (X, t) => {
  const on = Lt('s15_02') + .1, open = Lt('s15_08'), fly = Lt('s15_11') - .1, vanish = Lm('s15_11', .9), allNight = Lt('s15_12') - .05;
  const cam = shots(t, [], [
    { t: 0, cx: 980, cy: 640, z: 1.3, z2: 1.35, lock: 1 },
    { t: on - .1, cx: 990, cy: 560, z: 1.15, z2: 1.2, lock: 1 },
    { t: Lt('s15_03') - .05, cx: 920, cy: 560, z: 2.2, z2: 2.3, lock: 1 },
    { t: Lt('s15_04') - .05, cx: 990, cy: 600, z: 1.7, z2: 1.75, lock: 1 },
    { t: Lt('s15_05') - .05, cx: 1080, cy: 730, z: 3.0, z2: 3.3, lock: 1 },
    { t: Lt('s15_06') - .05, cx: 920, cy: 540, z: 2.4, z2: 2.5, lock: 1 },
    { t: Lt('s15_07') - .05, cx: 1080, cy: 720, z: 3.2, z2: 3.4, lock: 1 },
    { t: open - .05, cx: 1040, cy: 680, z: 2.2, z2: 2.3, lock: 1 },
    { t: Lt('s15_10') - .05, cx: 1080, cy: 720, z: 3.4, z2: 3.7, lock: 1 },
    { t: fly, cx: 1100, cy: 520, z: 1.2, z2: 1.15, lock: 1 },
    { t: allNight, cx: 900, cy: 560, z: 1.8, z2: 1.9, lock: 1 },
  ]);
  const st = stage(cam); st.wld(g => { drawSet(g, 'parkNight'); bench(g, 0); bench(g, 1); });
  const hp = benchSit(900, { t, look: [14, 6], mouth: .3, brow: -.3 });
  if (t > on) { hp.look = [16, 8]; hp.brow = -.5; }
  if (t > Lt('s15_04')) { const G = charGeom(CAST.tu, hp); hp.hR = POSE.point(1, G, 1)[1]; hp.armsFront = 0; hp.brow = -.7; }
  if (t > Lt('s15_05')) { hp.hR = [80, -125]; hp.armsFront = 1; hp.wide = .6; hp.brow = .8; hp.mouth = -.1; hp.look = [16, 8]; }
  if (t > Lt('s15_09')) { hp.wide = .9; hp.brow = 1; hp.mouth = -.4; }
  if (t > fly) { hp.look = [14, -14]; hp.mouth = -.2; hp.wide = .4; }
  if (t > allNight) { hp.look = [0, -10]; hp.lid = .35; hp.brow = .6; hp.mouth = -.3; hp.wide = 0; }
  say(hp, t, ['s15_02', 's15_03', 's15_04', 's15_06']);
  st.col(g => drawChar(g, 'tu', hp));
  let mP = null;
  if (t < fly) st.col(g => { const u = R(t, open, open + .5, back); wings(g, 1080, 720, .62, u, Math.sin(t * 6) * .2 * u); mP = pigeonTalk(g, 1080, 792, .62, { flip: -1, front: t > Lt('s15_04'), open: openOfP(t, ['s15_05', 's15_07', 's15_09', 's15_10']), tilt: Math.sin(t * 1.1) * .04 }); });
  else { const u = R(t, fly, vanish, lin), px = mix(1080, 1700, u), py = mix(792, 120, io(u)), a = 1 - R(t, vanish - .2, vanish + .2);
    if (a > 0) st.col(g => { g.save(); g.globalAlpha = a; wings(g, px, py - 70, .62, 1, Math.sin(t * 22)); pigeonTalk(g, px, py, .62, { flip: 1, tilt: -.2 }); g.restore(); }); }
  const gm = geniusState(t, [[on, Lt('s15_05') - .1], [allNight + .2, 99]], cam, headPt('tu', hp, 60));
  const ev = Lt('s15_05') - .1;
  const node = (x, y, s, k) => [{ k: 'circle', at: [x, y], r: 62, t0: Lm('s15_02', k), d: .4, out: ev }, { k: 'label', at: [x, y + 100], s, t0: Lm('s15_02', k) + .2, size: 38, align: 'center', out: ev }, { k: 'line', a: [x, y + 62], b: [1080, 650], t0: Lm('s15_02', k) + .5, d: .4, dash: 1, out: ev }];
  genius(X, st, gm, t, [
    { k: 'label', at: [420, 302], s: '1', t0: Lm('s15_02', .3), size: 64, align: 'center', bg: 0, out: ev }, ...node(420, 280, 'TIEMPO DETENIDO: SE MOVÍA', .28),
    { k: 'label', at: [960, 282], s: '2', t0: Lm('s15_02', .5), size: 64, align: 'center', bg: 0, out: ev }, ...node(960, 260, 'SIN FUTURO', .48),
    { k: 'label', at: [1500, 302], s: '3', t0: Lm('s15_02', .72), size: 64, align: 'center', bg: 0, out: ev }, ...node(1500, 280, 'ME VEÍA (INVISIBLE)', .7),
    { k: 'label', at: [1080, 520], s: 'CONCLUSIÓN: PEPE', t0: Lt('s15_04') + .1, size: 56, align: 'center', col: GEN_YEL, under: 1, out: ev },
    { k: 'label', at: [640, 260], s: '¿POR QUÉ?', t0: allNight + .5, size: 46, bg: 0 }, { k: 'label', at: [1060, 330], s: '¿PARA QUÉ?', t0: allNight + 1.0, size: 46, bg: 0 },
    { k: 'label', at: [700, 420], s: '¿«DOLER»?', t0: allNight + 1.6, size: 46, col: GEN_RED, bg: 0 }, { k: 'label', at: [1120, 220], s: '3:00 AM → 6:00 AM', t0: allNight + 2.2, size: 40, col: GEN_YEL },
  ]);
  if (mP) for (const id of ['s15_05', 's15_07', 's15_09', 's15_10']) talkBubble(X, cam, mP[0], mP[1], id, 'RUU', { t, dx: 1, r: 40, size: 62, w: 760 });
  if (t > fly) { const [x, y] = worldToScreen(cam, mix(1080, 1700, R(t, fly, vanish, lin)), mix(792, 120, io(R(t, fly, vanish, lin))) - 40); if (t < vanish + .3) comicWord(X, 'FLAP FLAP', x, y - 60, t - fly, 60, '#ffffff', 1.2); }
  if (t > allNight + .1) sticker(X, 'TODA LA NOCHE', R(t, allNight + .1, allNight + .4, back), 70, 70, 64);
  if (t > Le('s15_12') + .3) { X.save(); X.globalAlpha = R(t, Le('s15_12') + .3, T().dur, lin); X.fillStyle = '#000'; X.fillRect(0, 0, W, H); X.restore(); }
};

/* ================================================================ 16. is any of this real? */
function bellCurve(g, t, a, show500) { if (a <= 0) return; g.save(); g.globalAlpha = clamp(a); const x0 = 400, x1 = 1150, y0 = 470, px = v => mix(x0, x1, (v - 40) / 140), ink = '#2d2a40', red = '#c0262d', blue = '#3a6fb0';
  line(g, [[x0, y0], [x1, y0]], ink, 5);
  for (const v of [70, 100, 130, 160]) { line(g, [[px(v), y0 - 8], [px(v), y0 + 8]], ink, 4); text(g, String(v), px(v), y0 + 44, 34, ink, 'Bangers', 'center'); }
  g.beginPath(); for (let i = 0; i <= 80; i++) { const v = 40 + i * 140 / 80, y = y0 - 230 * Math.exp(-(((v - 100) / 15) ** 2) / 2); i ? g.lineTo(px(v), y) : g.moveTo(px(v), y); } g.strokeStyle = blue; g.lineWidth = 6; g.stroke();
  line(g, [[px(160), y0 - 60], [px(160), y0 - 6]], red, 5); text(g, '1 DE CADA 30 000', px(160) - 20, y0 - 80, 34, red, 'Bangers', 'center');
  if (show500 > 0) { g.globalAlpha = clamp(a) * clamp(show500); line(g, [[x1 - 40, y0 - 170], [x1 + 20, y0 - 170]], red, 6); shape(g, q => { q.moveTo(x1 + 30, y0 - 170); q.lineTo(x1 + 6, y0 - 184); q.lineTo(x1 + 6, y0 - 156); q.closePath(); }, red, 0);
    text(g, '500 → (FUERA DE LA ESCALA)', x1 - 170, y0 - 200, 36, red, 'Bangers', 'center'); }
  g.restore(); }
function energyBars(g, t, a) { if (a <= 0) return; g.save(); g.globalAlpha = clamp(a); const ink = '#2d2a40';
  brainIcon(g, 520, 330, 1.1);
  const bar = (y, pct, lbl, col, u) => { shape(g, q => rrPath(q, 700, y, 400, 54, 10), '#ffffff', 4); shape(g, q => rrPath(q, 700, y, 400 * pct / 25 * u, 54, 10), col, 0); text(g, lbl, 700, y - 12, 36, ink, 'Bangers', 'left'); text(g, pct + '%', 700 + 400 * pct / 25 * u + 50, y + 42, 40, ink, 'Bangers', 'center'); };
  bar(270, 2, 'PESO DEL CUERPO', '#9aa0aa', R(t, Lt('s16_04') + .3, Lt('s16_04') + .9)); if (t > Lm('s16_04', .45)) bar(400, 20, 'ENERGÍA QUE GASTA', '#f08a3a', R(t, Lm('s16_04', .45), Lm('s16_04', .45) + .8));
  g.restore(); }
function iqSheet(g, t, a) { if (a <= 0) return; g.save(); g.globalAlpha = clamp(a); g.translate(620, 440); g.rotate(-.05); g.scale(.85, .85);
  shape(g, q => rrPath(q, -170, -200, 340, 400, 8), '#fbf6e6', 5); text(g, 'PRUEBA DE IQ', 0, -140, 44, '#2d2a40', 'Bangers', 'center');
  for (let i = 0; i < 6; i++) line(g, [[-130, -80 + i * 40], [130, -80 + i * 40]], 'rgba(80,140,200,.5)', 3);
  text(g, 'NOMBRE: A. EINSTEIN', -130, -96, 28, '#2b3a67', 'ComicNeue', 'left'); text(g, '?', 40, 150, 160, '#c0262d', 'Bangers', 'center'); g.restore(); }
SC.s16 = (X, t) => {
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 470, z: 1.12, z2: 1.16, lock: 1 },
    { t: Lt('s16_02') - .05, cx: 900, cy: 420, z: 1.25, z2: 1.3, lock: 1 },
    { t: Lt('s16_04') - .05, cx: 900, cy: 420, z: 1.25, z2: 1.3, lock: 1 },
    { t: Lt('s16_06') - .05, cx: 960, cy: 430, z: 1.2, z2: 1.28, lock: 1 },
    { t: Lt('s16_07') - .05, cx: 1440, cy: 560, z: 1.9, z2: 2.0, lock: 1 },
  ]);
  const red = '#c0262d';
  const st = stage(cam);
  st.wld(g => { drawSet(g, 'classroom'); teacherDesk(g, 1620);
    text(g, '¿ALGO DE ESTO ES REAL?', 760, 205, 70, red, 'Bangers', 'center');
    if (t > Lt('s16_02') - .1 && t < Lt('s16_04') - .1) bellCurve(g, t, R(t, Lt('s16_02'), Lt('s16_02') + .4), R(t, Lt('s16_03') + .2, Lt('s16_03') + .6));
    if (t > Lt('s16_04') - .1 && t < Lt('s16_06') - .1) energyBars(g, t, R(t, Lt('s16_04'), Lt('s16_04') + .3));
    if (t > Lt('s16_06') - .1) iqSheet(g, t, R(t, Lt('s16_06'), Lt('s16_06') + .4));
  });
  st.wld(g => pigeonTalk(g, 1600, 692, .95, { flip: -1, front: 1, tilt: Math.sin(t * 2.2) * .06 }));
  composeG(X, st, { amt: 0 });
  if (t > Lt('s16_02') + .3 && t < Lt('s16_04') - .1) chip(X, 'PROMEDIO = 100', 1460, 260, R(t, Lt('s16_02') + .3, Lt('s16_02') + .6));
  if (t > Lt('s16_03') + .5 && t < Lt('s16_04') - .1) chip(X, 'NO ALCANZAN LOS HUMANOS', 1460, 360, R(t, Lt('s16_03') + .5, Lt('s16_03') + .8), '#ffb3b3');
  if (t > Lt('s16_05') && t < Lt('s16_06') - .1) { const [x, y] = worldToScreen(cam, 520, 230); smoke(X, x, y, t, R(t, Lt('s16_05'), Lt('s16_05') + .3) * (1 - R(t, Lm('s16_05', .45), Lm('s16_05', .55))), .8);
    if (t > Lm('s16_05', .45)) chip(X, 'HUMO: SOLO EN LA ANIMACIÓN', 1400, 260, R(t, Lm('s16_05', .45), Lm('s16_05', .45) + .3), '#ffffff'); }
  if (t > Lm('s16_06', .5) && t < Lt('s16_07') - .1) chip(X, '«160» = CÁLCULO DE INTERNET', 1400, 300, R(t, Lm('s16_06', .5), Lm('s16_06', .5) + .3));
  if (t > Lt('s16_07')) sticker(X, 'SABER PREGUNTAR: NO SE MIDE', R(t, Lm('s16_07', .3), Lm('s16_07', .3) + .25, back), 90, 90, 70);
};

/* ================================================================ 17. call to action, end card */
SC.s17 = (X, t) => {
  const end = Le('s17_04') + .9;
  const cam = shots(t, [], [{ t: 0, cx: 1000, cy: 600, z: 1.25, z2: 1.35, lock: 1 }, { t: Lt('s17_02') - .05, cx: 1080, cy: 735, z: 3.0, z2: 3.3, lock: 1 }, { t: Lt('s17_03') - .05, cx: 940, cy: 560, z: 1.6, z2: 1.7, lock: 1 }, { t: Lt('s17_04') - .1, cx: 1080, cy: 735, z: 3.6, z2: 3.9, lock: 1 }]);
  const st = stage(cam); st.wld(g => { drawSet(g, 'parkNight'); bench(g, 0); bench(g, 1); });
  const worried = t > Lt('s17_03');
  st.wld(g => drawChar(g, 'tu', benchSit(900, { t, look: worried ? [14, 4] : [10, -8], mouth: worried ? -.3 : .5, brow: worried ? .8 : -.3, wide: worried ? .4 : 0, footSwing: Math.sin(t * 2.4) * 10 })));
  st.wld(g => pigeonTalk(g, 1080, 792, .62, { flip: -1, front: 1, tilt: Math.sin(t * 1.3) * .08 }));
  if (t > Lt('s17_02')) st.wld(g => { g.save(); g.globalAlpha = R(t, Lt('s17_02') + .2, Lt('s17_02') + .5); g.strokeStyle = '#141014'; g.lineWidth = 2.5; for (const s2 of [-1, 1]) { g.beginPath(); g.arc(1061 + s2 * 9, 697, 6.5, 0, 7); g.stroke(); } g.beginPath(); g.moveTo(1058, 697); g.lineTo(1064, 697); g.stroke();
    g.translate(1046, 724); g.rotate(-.7); shape(g, q => rrPath(q, -3, -26, 6, 30, 2), '#c0262d', 2); g.restore(); });   // reading glasses and a red pen
  composeG(X, st, { amt: 0 });
  if (t > Lt('s17_01') - .05 && t < Lt('s17_03') - .1) sticker(X, '¿QUÉ HARÍAS CON 500 DE IQ?', R(t, Lt('s17_01') - .05, Lt('s17_01') + .25, outC), 70, 60, 58);
  if (t > Lt('s17_02') - .05 && t < Lt('s17_03') - .1) { sticker(X, '↓ COMENTARIOS ↓', R(t, Lt('s17_02') - .05, Lt('s17_02') + .25, outC), 70, 180, 60, '#ffffff'); sticker(X, 'PEPE LOS CORRIGE', R(t, Lm('s17_02', .6), Lm('s17_02', .6) + .25, back), 70, 300, 60); }
  if (t > Lt('s17_04') && t < end) { const [px, py] = worldToScreen(cam, 1080, 735); dashRing(X, px, py, 70 * cam.z, t); sticker(X, 'ESE ES EL PROBLEMA', R(t, Lt('s17_04') + .3, Lt('s17_04') + .55, back), 70, 70, 70); }
  if (t > end) { const a = R(t, end, end + .5, outC); X.save(); X.globalAlpha = a; X.fillStyle = '#141a2e'; X.fillRect(0, 0, W, H);
    text(X, CHANNEL_NAME, W / 2, 230, 150, '#fde047', 'Bangers', 'center', OUT, 18);
    text(X, 'PRÓXIMO EPISODIO:', W / 2, 400, 64, '#ffffff', 'Bangers', 'center');
    text(X, '¿Y SI DEJARAS', W / 2, 500, 84, '#ffffff', 'Bangers', 'center', OUT, 10); text(X, 'DE SENTIR DOLOR?', W / 2, 600, 84, '#ffffff', 'Bangers', 'center', OUT, 10);
    shape(X, q => rrPath(q, W / 2 - 300, 720, 600, 130, 22), '#e02424', 7); text(X, 'SUSCRÍBETE', W / 2, 812, 84, '#ffffff', 'Bangers', 'center');
    pigeonTalk(X, 1600, 960, .9, { flip: -1, front: 1, tilt: Math.sin(t * 1.5) * .1 }); X.restore(); }
};
