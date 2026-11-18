/* Ep06 «¿Qué pasaría si dejaras de sentir dolor?» — shared helpers and scenes 0–5.
   Beats are keyed to narration (Lt/Le/Lm from anim/episode.js). The pain look is anim/dolor.js: a hit sends a red pulse along a
   nerve to the head; for the hero it fizzles halfway («SIN SEÑAL»), for everybody else it arrives («¡AY!»). */
SC.missing = (X, t) => { X.fillStyle = '#1b1530'; X.fillRect(0, 0, W, H); text(X, SID + ' (sin animar)', W / 2, H / 2, 90, '#fde047', 'Bangers', 'center'); };
const CHANNEL_NAME = 'PONLE QUE…';
const vis = (t, a, b, fi = .25, fo = .3) => R(t, a, a + fi) * (1 - R(t, b, b + fo));
const loopU = (t, t0, P) => (((t - t0) % P) + P) % P / P;
function standing(x, extra = {}) { return Object.assign({ x, y: FEET, s: S0 }, extra); }
function seated(x, extra = {}) { return Object.assign({ x, y: 905, s: S0, sit: 1, noShadow: 1 }, extra); }
function benchSit(x, extra = {}) { return Object.assign({ x, y: 905, s: S0, sit: 1, noShadow: 1, hL: [-80, -125], hR: [80, -125], armsFront: 1 }, extra); }
function say(p, t, ids) { for (const id of ids) if (T().L[id] && speaking(t, id)) { p.open = talk(t, id); return true; } return false; }
function mouthPt(cname, p) { const c = CAST[cname], G = charGeom(c, p), S = (p.s || 1) * (c.s || 1); return [p.x + ((p.hx || 0) + (p.look ? p.look[0] : 0)) * S * (p.flip || 1), p.y + (G.top - 70 + (p.hy || 0)) * S]; }
function headPt(cname, p, dy = 0) { const c = CAST[cname], G = charGeom(c, p), S = (p.s || 1) * (c.s || 1); return [p.x + (p.hx || 0) * S * (p.flip || 1), p.y + (G.top - 100 - c.r * 1.1 + (p.hy || 0) + dy) * S]; }
function rewindFX(X, k, t) { if (k <= 0) return;
  X.save(); X.globalAlpha = .25 * k; X.fillStyle = '#ffffff'; const r = rnd(Math.floor(t * 30));
  for (let i = 0; i < 9; i++) { const y = r() * H, h = 4 + r() * 18; X.fillRect(0, y, W, h); } X.restore();
  X.save(); X.globalAlpha = .55 * k; X.fillStyle = '#0d0b12'; X.fillRect(0, H - 150, W, 150); X.restore();
  X.save(); X.globalAlpha = k; text(X, '◀◀  REBOBINANDO', 70, H - 52, 76, '#ffffff', 'Bangers', 'left', OUT, 10); X.restore(); }
function nightTint(X, a = 1) { X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.globalCompositeOperation = 'multiply'; X.fillStyle = `rgba(60,70,140,${.55 * a})`; X.fillRect(0, 0, W, H); X.restore(); }
function dashRing(X, x, y, r, t, col = '#ffd34d') { X.save(); X.strokeStyle = col; X.lineWidth = 8; X.setLineDash([22, 16]); X.lineDashOffset = -t * 60; X.beginPath(); X.arc(x, y, r, 0, 7); X.stroke(); X.restore(); }
function cooBubble(X, cam, wx, wy, t, t0, d, s = 'RUU') { const a = R(t, t0, t0 + .15, back) * (1 - R(t, t0 + d, t0 + d + .2)); if (a <= 0) return; const [x, y] = worldToScreen(cam, wx, wy); bubble(X, s, x, y - 20, a, 56); }
function pepeWatch(g, x, y, s, hx, t, extra = {}) { drawPigeon(g, x, y, s, Object.assign({ flip: hx < x ? -1 : 1, tilt: Math.sin(t * .9) * .06 }, extra)); }
function heartPopX(g, x, y, u, s = 1) { if (u <= 0 || u >= 1) return; g.save(); g.globalAlpha = 1 - u * u; g.translate(x, y - u * 90); const k = s * (.6 + .4 * back(Math.min(1, u * 3))); g.scale(k, k);
  shape(g, q => { q.moveTo(0, 18); q.bezierCurveTo(-34, -6, -20, -34, 0, -16); q.bezierCurveTo(20, -34, 34, -6, 0, 18); }, '#ff5d7a', 4); g.restore(); }
function tears(g, x, y, t, a = 1) { if (a <= 0) return; for (let i = 0; i < 6; i++) { const u = loopU(t, i * .17, 1), xx = x + (i % 2 ? 62 : 0), yy = y + u * 240; g.save(); g.globalAlpha = (1 - u) * a;
  shape(g, q => { q.moveTo(xx, yy - 14); q.quadraticCurveTo(xx + 9, yy, xx, yy + 8); q.quadraticCurveTo(xx - 9, yy, xx, yy - 14); }, '#7cc8ff', 2); g.restore(); } }
/* a memory in a thought cloud: (wx, wy) world point of the remembered scene at the cloud's centre, k its zoom */
function memCloud(X, x, y, r, a, wx, wy, k, draw, from) { if (a <= 0) return; const P = layer('MEM'), zc = window.__camz; window.__camz = k;
  P.setTransform(k, 0, 0, k, x - wx * k, y - wy * k); draw(P); P.setTransform(1, 0, 0, 1, 0, 0); window.__camz = zc;
  X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.globalAlpha = clamp(a); const s = .85 + .15 * back(a);
  if (from) for (let i = 0; i < 3; i++) { const u = (i + 1) / 4; shape(X, q => q.arc(mix(from[0], x, u * .7), mix(from[1], y + r * .8, u * .7), 12 + i * 8, 0, 7), '#ffffff', 5); }
  X.translate(x, y); X.scale(s, s); X.beginPath(); for (let i = 0; i < 12; i++) { const an = i / 12 * Math.PI * 2; X.arc(Math.cos(an) * r * .86, Math.sin(an) * r * .62, r * .32, 0, 7); } X.closePath();
  X.fillStyle = '#ffffff'; X.fill(); X.lineWidth = 8; X.strokeStyle = '#141014'; X.stroke();
  X.save(); X.beginPath(); X.ellipse(0, 0, r * .95, r * .68, 0, 0, 7); X.clip(); X.filter = 'sepia(.35)'; X.drawImage(P.canvas, -x, -y); X.restore();
  X.restore(); }
function pepeMemory(X, cam, t, a, from) { memCloud(X, 1340, 360, 330, a, 1060, 690, .95, g => { drawSet(g, 'parkNight'); bench(g, 0); bench(g, 1);
  pigeonTalk(g, 1080, 792, .62, { flip: -1, front: 1, open: Math.abs(Math.sin(t * 11)) * .5 * a, tilt: Math.sin(t * 1.4) * .05 }); }, from); }

/* ---------------------------------------------------------------- hits: the pain signal for one event
   ev = { t, at: [x, y] world impact point, cname, p (the pose, for the head), hero: 1 (no pain), val (0..10 for others) }
   registered in EVENTS so the probe hands the times to the mixer (thud + fizzle, or thud + «¡ay!») */
function hitPts(ev) { const h = headInfo(ev.cname, ev.p), [ax, ay] = ev.at, sd = ax < h.x ? -1 : 1; return [ev.at, [mix(ax, h.x + sd * h.r * .8, .55), mix(ay, h.y, .45) + 30], [h.x + sd * h.r * .85, h.y + h.r * .6], [h.x + sd * h.r * .45, h.y - h.r * .35]]; }   // up the side of the face to the temple, not across it
function hits(X, cam, t, list, gauge = 1) {
  if (typeof SID !== 'undefined') EVENTS[SID] = { hits: list.map(e => ({ t: e.t, hero: e.hero ? 1 : 0 })) };
  let g = null;
  for (const ev of list) { if (t < ev.t - .05 || t > ev.t + 2.6) continue; nerve(X, cam, hitPts(ev), t, ev.t, ev.hero ? 1 : 0, ev.dur || .5);
    if (!ev.hero) { const u = R(t, ev.t + .5, ev.t + 1.1, lin); painFlash(X, bump(t, ev.t + .45, ev.t + 1.2)); const h = headInfo(ev.cname, ev.p), [sx, sy] = worldToScreen(cam, h.x, h.y - h.r * 1.2); hitStars(X, sx, sy, u, cam.z * .8);
      if (t > ev.t + .45 && t < ev.t + 1.4) comicWord(X, ev.word || '¡AY!', sx + 60, sy - 40, t - ev.t - .45, 84, '#ff6b6b', .95); }
    if (gauge && t > ev.t + .2 && t < ev.t + 2.4) g = ev; }
  if (g) painGauge(X, R(t, g.t + .2, g.t + .45, lin) * (1 - R(t, g.t + 2.1, g.t + 2.4, lin)), g.hero ? 0 : (g.val || 8) * R(t, g.t + .45, g.t + .8, outC), t, g.hero ? 1 : 0);
}
/* the hero's damage as the week goes on (scene → marks) */
const DAMAGE = { s00: { bump: 1, cheek: 1, chin: 1, ankle: 1 }, s13: { bump: 1, cheek: 1, chin: 1, ankle: 1 }, s14: { bump: 1, cheek: 1, chin: 1, ankle: 1 }, s15: { bump: 1, cheek: 1, ankle: 1 }, s17: { bump: .6, cheek: 1, ankle: 1 } };
function drawHero(g, hp, marks) { drawChar(g, 'tu', hp); hurtMarks(g, 'tu', hp, marks || DAMAGE[SID] || {}); }

/* ================================================================ 0. cold open: Friday night, plaster number 31 */
function sauceBottle(g, x, y, s = 1, tilt = 0) { g.save(); g.translate(x, y); g.rotate(tilt); g.scale(s, s);
  shape(g, q => { q.moveTo(-34, 0); q.lineTo(-34, -120); q.quadraticCurveTo(-34, -150, -14, -160); q.lineTo(-14, -190); q.lineTo(14, -190); q.lineTo(14, -160); q.quadraticCurveTo(34, -150, 34, -120); q.lineTo(34, 0); q.closePath(); }, '#c2261f', 5);
  shape(g, q => rrPath(q, -18, -214, 36, 28, 6), '#2e333d', 4); shape(g, q => rrPath(q, -28, -104, 56, 62, 8), '#fff3d6', 3);
  shape(g, q => { q.moveTo(0, -96); q.quadraticCurveTo(16, -76, 6, -58); q.quadraticCurveTo(0, -66, -6, -58); q.quadraticCurveTo(-16, -76, 0, -96); }, '#ff8a1f', 2);
  text(g, 'ABUELA', 0, -46, 15, '#c2261f', 'Bangers', 'center'); g.restore(); }
function dropper(g, x, y, rot = 0) { g.save(); g.translate(x, y); g.rotate(rot); shape(g, q => rrPath(q, -6, -70, 12, 64, 5), 'rgba(220,240,255,.85)', 3); shape(g, q => q.ellipse(0, -80, 11, 16, 0, 0, 7), '#2e333d', 3); circ(g, 0, 6, 5, '#c2261f', 0); g.restore(); }
SC.s00 = (X, t) => {
  const rw = Lm('s00_07', .45);
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 560, z: 1.25, z2: 1.32, lock: 1 },
    { t: Lt('s00_02') - .05, cx: 1000, cy: 520, z: 1.7, z2: 1.78, lock: 1 },
    { t: Lt('s00_03') - .05, cx: 1180, cy: 480, z: 2.3, z2: 2.4, lock: 1 },
    { t: Lt('s00_04') - .05, cx: 860, cy: 520, z: 2.4, z2: 2.55, lock: 1 },
    { t: Lt('s00_05') - .05, cx: 960, cy: 540, z: 1.2, z2: 1.25, lock: 1 },
    { t: Lt('s00_06') - .05, cx: 860, cy: 520, z: 1.9, z2: 2.1, lock: 1 },
    { t: rw, cx: 960, cy: 540, z: 1.0, lock: 1 },
  ]);
  const st = stage(cam); st.wld(g => drawSet(g, 'kitchenNight'));
  const mp = standing(1180, { t, flip: -1, look: [-14, 6], mouth: -.2, brow: .7, hR: [200, -330], holdR: (g, x, y) => curita(g, x + 6, y - 4, 60, .3) });
  if (t < Lt('s00_03') - .2) { const k = Math.sin(t * 2.4); mp.hR = [190 + k * 10, -340 + k * 6]; }
  say(mp, t, ['s00_03']);
  if (t > Lt('s00_04')) { mp.lid = .4; mp.brow = 1; mp.mouth = -.4; mp.hR = null; mp.holdR = null; const G = charGeom(CAST.mama, mp); [mp.hL, mp.hR] = POSE.hips(G); }
  st.wld(g => drawChar(g, 'mama', mp));
  const hp = seated(860, { t, look: [10, -4], mouth: .6, brow: -.4, hL: [-80, -170], hR: [80, -170] });
  if (t > Lt('s00_04') - .1) { hp.look = [14, -2]; hp.mouth = .8; const G = charGeom(CAST.tu, hp); hp.hR = [150, G.top + 20]; }   // thumbs up
  if (t > Lt('s00_06')) { hp.mouth = .1; hp.look = [0, 4]; hp.hR = [80, -170]; }
  say(hp, t, ['s00_04']);
  st.wld(g => drawHero(g, hp)); st.wld(g => kitchenTable(g));
  compose2(X, st, { amt: 0 });
  sticker(X, 'VIERNES · 9:00 PM', vis(t, .3, Lt('s00_02') - .2), 70, 70, 64);
  if (t > Lt('s00_02') - .05 && t < Lt('s00_03') - .1) bigCounter(X, 'CURITAS:', String(Math.min(31, Math.floor(18 + (t - Lt('s00_02')) * 6))), R(t, Lt('s00_02'), Lt('s00_02') + .3), 70, 70);
  if (t > Lt('s00_04') && t < Lt('s00_06')) painGauge(X, R(t, Lt('s00_04') + .2, Lt('s00_04') + .5, lin), 0, t, 1);
  if (t > Lt('s00_06') && t < rw) { const a = R(t, Lt('s00_06') + .2, Lt('s00_06') + .5, outC); const [hx, hy] = worldToScreen(cam, ...headPt('tu', hp));
    memCloud(X, 1340, 340, 330, a, 640, 520, 1.25, g => { drawSet(g, 'street'); drawChar(g, 'valeria', { x: 640 + 300 * R(t, Lt('s00_06') + .4, rw, lin), y: FEET, s: S0, t, walk: 1, phase: t * 5, look: [14, 6], mouth: -.3, brow: .5 }); }, [hx + 60, hy]); }
  if (t > rw) rewindFX(X, R(t, rw, rw + .2), t);
};

/* ================================================================ 1. the power: no pain at all (touch, cold and tickles still work) */
SC.s01 = (X, t) => {
  const kick = Lm('s01_02', .15), list = Lt('s01_03') - .05;
  const cam = shots(t, [], [
    { t: 0, cx: 900, cy: 560, z: 1.2, z2: 1.28, lock: 1 },
    { t: Lt('s01_02') - .05, cx: 960, cy: 540, z: 1.0, z2: 1.03, lock: 1 },
    { t: list, cx: 760, cy: 520, z: 1.6, z2: 1.7, lock: 1 },
    { t: Lt('s01_04') - .05, cx: 760, cy: 500, z: 2.0, z2: 2.1, lock: 1 },
    { t: Lt('s01_05') - .05, cx: 1000, cy: 520, z: 1.25, z2: 1.35, lock: 1 },
  ]);
  const st = stage(cam); st.wld(g => drawSet(g, 'street'));
  st.wld(g => pepeWatch(g, 1180, 470, .4, 760, t));   // on the tree branch: watching
  const bx = mix(1900, 790, R(t, kick - .5, kick, lin)), by = mix(820, 470, R(t, kick - .5, kick, lin)), after = R(t, kick, kick + .9, lin);
  if (t > kick - .5 && t < kick + .9) st.wld(g => propBall(g, t < kick ? bx : mix(790, 1300, after), t < kick ? by : 470 + after * 400 - Math.sin(after * Math.PI) * 200, 30, t * 8));
  const hp = standing(760, { t, look: [10, 0], mouth: .4 });
  if (t > kick && t < kick + 1.5) { hp.look = [6, 4]; hp.mouth = .6; hp.brow = -.3; hp.rot = -.08 * (1 - R(t, kick, kick + .5)); }
  if (t > list) { hp.look = [0, 0]; hp.mouth = .5; }
  if (t > Lt('s01_04')) { hp.mouth = .9; hp.brow = -.5; const G = charGeom(CAST.tu, hp); hp.hR = [150, G.top + 20]; }
  if (t > Lt('s01_05')) { hp.hR = null; hp.mouth = -.1; hp.brow = .5; hp.look = [14, -10]; }
  st.wld(g => drawHero(g, hp));
  compose2(X, st, { amt: 0 });
  hits(X, cam, t, [{ t: kick, at: headPt('tu', hp, 120), cname: 'tu', p: hp, hero: 1 }]);
  if (t > kick && t < kick + .7) comicWord(X, '¡PUM!', ...worldToScreen(cam, 830, 380), t - kick, 84);
  const items = [['TOCAR', 1, 0], ['FRÍO', 1, .25], ['COSQUILLAS', 1, .5], ['DOLOR', 0, .78]];
  if (t > list && t < Lt('s01_05') - .1) items.forEach(([s, ok, f], i) => { const a = R(t, Lm('s01_03', f), Lm('s01_03', f) + .25, back); if (a > 0) sticker(X, s + (ok ? '  ✓' : '  ✗'), a, 1180, 140 + i * 140, 70, ok ? '#a7f3a0' : '#ffb3b3'); });
};

/* ================================================================ 2. title card */
SC.s02 = (X, t) => {
  const cam = { cx: 960, cy: 540, z: 1.0 }, st = stage(cam); st.wld(g => drawSet(g, 'street'));
  const hp = standing(760, { t, look: [6, -4], mouth: .9, brow: -.5 }); const G = charGeom(CAST.tu, hp); hp.hR = [150, G.top + 20];
  st.wld(g => drawHero(g, hp, { bump: 1, cheek: 1 })); compose2(X, st, { amt: 0 });
  painGauge(X, R(t, .1, .4), 0, t, 1);
  titleCard(X, '¿QUÉ PASARÍA SI', 'NO SINTIERAS DOLOR?', R(t, .3, .8, outC), t);
};

/* ================================================================ 3. Monday: the little toe against the bed */
function toyBrick(g, x, y, s = 1) { g.save(); g.translate(x, y); g.scale(s, s); shape(g, q => rrPath(q, -30, -26, 60, 26, 4), '#3a6fb0', 4); for (const dx of [-15, 15]) shape(g, q => rrPath(q, dx - 9, -36, 18, 12, 3), '#3a6fb0', 3); g.restore(); }
SC.s03 = (X, t) => {
  const toe = Lm('s03_01', .82), brick = Lm('s03_05', .45);
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 560, z: 1.05, z2: 1.1, lock: 1 },
    { t: toe - .5, cx: 900, cy: 760, z: 2.0, z2: 2.1, lock: 1 },
    { t: Lt('s03_03') - .05, cx: 920, cy: 560, z: 1.7, z2: 1.75, lock: 1 },
    { t: Lt('s03_05') - .05, cx: 1260, cy: 760, z: 1.9, z2: 2.0, lock: 1 },
    { t: Lt('s03_06') - .05, cx: 960, cy: 540, z: 1.1, z2: 1.15, lock: 1 },
    { t: Lt('s03_07') - .05, cx: 1100, cy: 520, z: 1.8, z2: 1.9, lock: 1 },
  ]);
  const st = stage(cam); st.wld(g => { drawSet(g, 'bedroom'); bedBack(g); nightstand(g); if (t < brick + .1) toyBrick(g, 1300, 930, 1.1); });
  st.wld(g => drawAnimal(g, 'croqueta', 480, 716, .8, { t, head: 'bored', tilt: Math.sin(t * .7) * .05 }));
  let hx = mix(800, 900, R(t, Lt('s03_01') + 1.2, toe, lin)); if (t > Lt('s03_05')) hx = mix(900, 1270, R(t, Lt('s03_05'), brick, lin));
  const walking = (t > Lt('s03_01') + 1.2 && t < toe) || (t > Lt('s03_05') && t < brick);
  const hp = standing(hx, { t, walk: walking ? 1 : 0, phase: walkPh(hx), look: [10, 4], mouth: .1, lid: t < Lt('s03_01') + 1 ? .5 : 0 });
  if (t > toe) { hp.look = [6, 22]; hp.brow = .3; hp.mouth = -.1; }
  if (t > Lt('s03_03')) { hp.wide = .5; hp.brow = .6; }
  if (t > brick) { hp.look = [8, 22]; hp.wide = .3; }
  if (t > Lt('s03_06')) { hp.look = [-10, -10]; hp.wide = 0; hp.brow = .4; }
  if (t > Lt('s03_07')) { const G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = POSE.shrug(1, G); hp.mouth = .3; hp.look = [10, -4]; hp.brow = .5; }
  say(hp, t, ['s03_03']);
  if (t < Lt('s03_01') + 1.1) { st.wld(g => drawHero(g, Object.assign({}, hp, { x: 700, y: 945 }))); st.wld(g => bedFront(g, .6)); }
  else st.wld(g => drawHero(g, hp));
  compose2(X, st, { amt: 0 });
  hits(X, cam, t, [{ t: toe, at: [878, 925], cname: 'tu', p: hp, hero: 1, dur: .7 }, { t: brick, at: [1294, 925], cname: 'tu', p: hp, hero: 1, dur: .7 }]);
  if (t > toe && t < toe + .7) comicWord(X, '¡TOC!', ...worldToScreen(cam, 820, 840), t - toe, 80);
  if (t > brick && t < brick + .7) comicWord(X, '¡CRAC!', ...worldToScreen(cam, 1330, 840), t - brick, 80);
  sticker(X, 'LUNES', vis(t, .3, toe - .6), 70, 70, 64);
  if (t > Lt('s03_06') - .1 && t < Lt('s03_07') - .1) { const a = R(t, Lt('s03_06'), Lt('s03_06') + .35, outC) * (1 - R(t, Lt('s03_07') - .4, Lt('s03_07') - .1)), [hx2, hy2] = worldToScreen(cam, ...headPt('tu', hp));
    pepeMemory(X, cam, t, a, [hx2 + 60, hy2]);
    bubble(X, 'MAÑANA, NADA TE VA A DOLER', 1120, 160, R(t, Lm('s03_06', .3), Lm('s03_06', .3) + .3, back), 46);
    if (t > Lm('s03_06', .7)) bubble(X, 'NI SIQUIERA LO QUE DEBERÍA', 1440, 690, R(t, Lm('s03_06', .7), Lm('s03_06', .7) + .3, back), 50); }
  if (t > Lt('s03_07')) { sticker(X, '«NADA TE VA A DOLER»  ✓', R(t, Lt('s03_07') + .1, Lt('s03_07') + .35, back), 70, 70, 56, '#a7f3a0'); sticker(X, '«NI LO QUE DEBERÍA»  ???', R(t, Lm('s03_07', .55), Lm('s03_07', .55) + .25, back), 70, 190, 56, '#ffb3b3'); }
};

/* ================================================================ 4. grandma's sauce: served with a dropper */
SC.s04 = (X, t) => {
  const eat = Lm('s04_03', .3), pale = Lt('s04_05') - .05, catGo = Lm('s04_05', .5);
  const cam = shots(t, [], [
    { t: 0, cx: 1160, cy: 560, z: 1.5, z2: 1.55, lock: 1 },
    { t: Lt('s04_02') - .05, cx: 1080, cy: 700, z: 2.6, z2: 2.75, lock: 1 },
    { t: Lt('s04_03') - .05, cx: 860, cy: 520, z: 2.0, z2: 2.1, lock: 1 },
    { t: pale, cx: 1080, cy: 560, z: 1.3, z2: 1.35, lock: 1 },
    { t: Lt('s04_06') - .05, cx: 1220, cy: 500, z: 2.2, z2: 2.3, lock: 1 },
    { t: Lt('s04_07') - .05, cx: 960, cy: 540, z: 1.0, z2: 1.04, lock: 1 },
  ]);
  const st = stage(cam); st.wld(g => drawSet(g, 'kitchen'));
  const mp = standing(1250, { t, flip: -1, look: [-14, 6], mouth: .2, brow: .5, hR: [-120, -380] });
  if (t > Lt('s04_02') - .1) { mp.hR = null; mp.look = [-16, 4]; }
  if (t > eat) { mp.wide = .8; mp.mouth = .6; mp.brow = .9; mp.look = [-16, 0]; mp.open = .7; }
  if (t > pale) { mp.sweat = 1; }
  if (t > Lt('s04_06') - .1) { mp.open = 0; const G = charGeom(CAST.mama, mp); [mp.hL, mp.hR] = [[-170, G.top - 5], [170, G.top - 5]]; }   // hands up in alarm: elbows down and out, forearms showing
  say(mp, t, ['s04_01', 's04_06']);
  st.wld(g => drawChar(g, 'mama', mp));
  const hp = standing(820, { t, look: [14, 8], mouth: .3, brow: -.2 });
  if (t > Lt('s04_03') - .1 && t < eat + .6) { hp.hR = [100, -320 - R(t, Lt('s04_03'), eat, io) * 200]; hp.holdR = (g, x, y) => { g.save(); g.translate(x, y); g.rotate(-.9); shape(g, q => rrPath(q, -5, -70, 10, 70, 4), '#c8ccd4', 3); shape(g, q => q.ellipse(0, -80, 16, 11, 0, 0, 7), '#c2261f', 3); g.restore(); }; }
  if (t > eat) { hp.mouth = .7; hp.look = [10, -4]; hp.brow = -.6; hp.lid = .3; }
  if (t > Lt('s04_05')) { hp.lid = 0; hp.look = [16, 2]; }
  say(hp, t, ['s04_04']);
  st.wld(g => drawHero(g, hp));
  st.wld(g => { kitchenTable(g); sauceBottle(g, 1060, 792, .9); dropper(g, 1130, 788, .9); });
  const cx = t < catGo ? 1560 : mix(1560, 2100, R(t, catGo, catGo + 2.2, lin));
  st.wld(g => drawCat(g, cx, 930, .7, { t, flip: t > catGo ? 1 : -1 }));
  compose2(X, st, { amt: 0 });
  if (t > eat) { const k = R(t, eat, eat + .6), [mx, my] = worldToScreen(cam, ...mouthPt('tu', hp));
    if (t < Lt('s04_07')) { X.save(); X.globalAlpha = k; text(X, 'PICANTE: 2 000 000', mx + 160, my - 160, 54, '#ff6b2b', 'Bangers', 'left', OUT, 8); X.restore(); painGauge(X, k * (1 - R(t, Lt('s04_06') - .3, Lt('s04_06'))), 0, t, 1); } }
  sticker(X, '1 GOTA = 3 FAMILIAS', vis(t, Lm('s04_02', .4), Lt('s04_03') - .1), 70, 70, 62);
  ruleCard(X, 1, 'NO TE DUELE NADA.', 'PERO TU CUERPO SÍ SE LASTIMA', R(t, Lt('s04_07') + .1, Lt('s04_07') + .4, outC));
};

/* ================================================================ 5. goalkeeper: fourteen saves, twelve with the face */
SC.s05 = (X, t) => {
  const s1 = Lm('s05_02', .45), s2 = Lm('s05_03', .45), win = Lt('s05_07') - .05;
  const cam = shots(t, [], [
    { t: 0, cx: 960, cy: 560, z: 1.0, z2: 1.05, lock: 1 },
    { t: Lt('s05_02') - .05, cx: 1560, cy: 480, z: 2.3, z2: 2.4, lock: 1 },
    { t: Lt('s05_04') - .05, cx: 700, cy: 520, z: 1.8, z2: 1.9, lock: 1 },
    { t: Lt('s05_05') - .05, cx: 1590, cy: 470, z: 3.0, z2: 3.1, lock: 1 },
    { t: Lt('s05_06') - .05, cx: 1300, cy: 500, z: 1.4, z2: 1.45, lock: 1 },
    { t: win, cx: 1300, cy: 520, z: 1.5, z2: 1.6, lock: 1 },
  ]);
  const st = stage(cam); st.wld(g => { drawSet(g, 'field'); goal(g, 0); });
  // the striker (far left) and Nacho by the goal
  st.wld(g => drawChar(g, 'ex3', { x: 860, y: 900, s: .62, t, flip: 1, look: [14, 0], mouth: .4, walk: 0 }));
  const hp = { x: 1590, y: 650, s: .4, t, look: [-14, 4], mouth: .4, brow: -.3, hL: [-150, -380], hR: [150, -380] };
  const shot = (tt, k) => { const u = clamp((t - (tt - .6)) / .6); return u > 0 && u < 1 ? [mix(900, 1590, u), mix(860, 506, u) - Math.sin(u * Math.PI) * 120, mix(30, 15, u)] : null; };
  for (const tt of [s1, s2]) { const b = shot(tt); if (b) st.wld(g => propBall(g, b[0], b[1], b[2], t * 10)); if (t > tt && t < tt + .6) { hp.rot = -.25 * (1 - R(t, tt, tt + .6)); hp.hy = -10; } }
  if (t > Lt('s05_05')) { hp.look = [-16, 0]; hp.mouth = .4; hp.brow = .2; hp.wide = .3; }
  if (t > win) { const G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = POSE.stretch(1, G); hp.mouth = 1; hp.y = 650 - Math.abs(Math.sin(t * 7)) * 40; hp.blink = 1; }
  say(hp, t, ['s05_05']);
  if (t > win) st.wld(g => ['ex1', 'ex2', 'ex4', 'ex6'].forEach((n, i) => { const p = { x: [1380, 1470, 1710, 1800][i], y: 640, s: .38, t: t + i, look: [0, -8], mouth: .8, open: .6 }; const G = charGeom(CAST[n], p); [p.hL, p.hR] = POSE.stretch(1, G); p.jump = Math.abs(Math.sin(t * 8 + i)) * 40; drawChar(g, n, p); }));   // behind you: you're the one they cheer
  if (t > win) hp.y = 690 - Math.abs(Math.sin(t * 7)) * 50;
  st.wld(g => drawHero(g, hp, { bump: t > s2 ? .5 : 0 }));
  st.wld(g => goal(g, 1));
  const np = standing(560, { t, s: .7, y: 880, look: [16, -2], mouth: .6, brow: .6, wide: .6 });
  if (t > Lt('s05_04') - .1) { const G = charGeom(CAST.nacho, np); [np.hL, np.hR] = [[-120, G.top - 40], [120, G.top - 40]]; np.wide = 1; }
  say(np, t, ['s05_04']);
  st.wld(g => drawChar(g, 'nacho', np));
  compose2(X, st, { amt: 0 });
  hits(X, cam, t, [s1, s2].map(tt => ({ t: tt, at: headPt('tu', hp, 150), cname: 'tu', p: hp, hero: 1, dur: .45 })));
  for (const tt of [s1, s2]) if (t > tt && t < tt + .6) comicWord(X, '¡PUM!', ...worldToScreen(cam, 1590, 430), t - tt, 80);
  if (t > Lt('s05_06') - .05 && t < win + 2) { const a = R(t, Lt('s05_06'), Lt('s05_06') + .3, back); sticker(X, 'ATAJADAS: 14', a, 70, 70, 64); sticker(X, 'CON LA CARA: 12', R(t, Lm('s05_06', .55), Lm('s05_06', .55) + .3, back), 70, 190, 64, '#ffb3b3'); }
  if (t > win) bigCounter(X, 'MARCADOR:', '1 - 0', R(t, win + .1, win + .4), W - 560, 70);
};
