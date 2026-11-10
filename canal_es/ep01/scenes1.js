/* Ep01 "¿Qué pasaría si pudieras detener el tiempo?" — scenes 1–5.
   Every beat is keyed to narration times from timing.js (Lt = line start, Le = line end, Lm = point inside a line). */
let SID = 's01';
const SC = {};
const T = () => TIM.scenes[SID];
const Lt = id => T().L[id][0], Ld = id => T().L[id][1], Le = id => Lt(id) + Ld(id), Lm = (id, f) => Lt(id) + Ld(id) * f;
const speaking = (t, id) => t >= Lt(id) && t <= Le(id);
const talk = (t, id) => speaking(t, id) ? .25 + .45 * Math.abs(Math.sin((t - Lt(id)) * 13)) * (1 - .4 * Math.abs(Math.sin((t - Lt(id)) * 3.1))) : 0;
const S0 = .78, FEET = 930;
/* camera shots: hard cuts between entries; inside a shot cx/cy/z ease from first to second value */
function shots(t, claps, list) {
  // explicit shots: hard cuts between entries; inside a shot cx/cy/z ease from first to second value
  let i = 0; for (let k = 0; k < list.length; k++) if (t >= list[k].t) i = k;
  const s = list[i], end = i + 1 < list.length ? list[i + 1].t : T().dur, u = io(clamp((t - s.t) / Math.max(.01, end - s.t)));
  const v = (a, b) => typeof a === 'function' ? a(t) : mix(a, b == null ? a : b, u);
  const cam = { cx: v(s.cx, s.cx2), cy: v(s.cy, s.cy2), z: v(s.z, s.z2) };
  // extra coverage: cut on narration sentence starts inside long shots, alternating a punch-in and an offset angle;
  // never within 0.7 s of a clap, never closer than 1.5 s to another cut
  let seg = i + ':0';
  if (!s.lock) {
    const ct = (claps || []).map(c => c.t != null ? c.t : c), cuts = []; let last = s.t;
    const cand = [];   // sentence starts, plus the middle of long sentences
    for (const x of Object.values(T().L)) { cand.push(x[0]); if (x[1] > 3.0) cand.push(x[0] + x[1] * .5); }
    for (const lt of cand.sort((a, b) => a - b)) {
      if (lt < s.t + 1.1 || lt > end - .9 || lt - last < 1.25 || ct.some(c => Math.abs(lt - c) < .6)) continue; cuts.push(lt); last = lt; }
    let k = -1; for (let j = 0; j < cuts.length; j++) if (t >= cuts[j]) k = j;
    if (k >= 0) { const cend = k + 1 < cuts.length ? cuts[k + 1] : end, du = clamp((t - cuts[k]) / Math.max(.01, cend - cuts[k]));
      if (k % 2 === 0) { const z0 = cam.z; cam.z = z0 * (1.36 + .03 * du); cam.cy -= 70 / z0; cam.cx += (s.fx != null ? (s.fx - cam.cx) * .6 : 0); }
      else { const side = (k % 4 === 1 ? 1 : -1); cam.z *= 1.1 + .02 * du; cam.cx += side * 150 / cam.z; cam.cy -= 25 / cam.z; }
      seg = i + ':' + (k + 1); }
  }
  window.__seg = SID + '/' + seg;
  if (s.shake) { const k = s.shake * Math.max(0, 1 - (t - s.t) / .5); cam.sx = Math.sin(t * 80) * 14 * k; cam.sy = Math.cos(t * 67) * 10 * k; }
  // keep the frame inside the set
  const sw = s.w || W, hw = W / 2 / cam.z, hh = H / 2 / cam.z; cam.cx = clamp(cam.cx, hw, sw - hw); cam.cy = clamp(cam.cy, hh, H - hh);
  return cam;
}
const walkPh = x => x / 44;
function dropsSpray(g, x, y, n, seed, s = 1) { const r = rnd(seed); for (let i = 0; i < n; i++) { const a = Math.PI * (.85 + r() * .35), d = 30 + r() * 120 * s; circ(g, x + Math.cos(a) * d, y + Math.sin(a) * d * .5 + r() * 20, 4 + r() * 5, '#bfe6ff', 3); } }
function bubble(g, s, x, y, a, size = 60) { if (a <= 0) return; g.save(); g.globalAlpha = clamp(a); g.font = `${size}px Bangers`; const w = g.measureText(s).width + 50, h = size * 1.4, k = .8 + .2 * back(a);
  g.translate(x, y); g.scale(k, k); shape(g, q => { rrPath(q, -w / 2, -h, w, h, h / 2.2); }, '#ffffff', 5); shape(g, q => { q.moveTo(-14, -6); q.lineTo(0, 26); q.lineTo(14, -6); }, '#ffffff', 0);
  line(g, [[-14, -2], [0, 26], [14, -2]], OUT, 5); text(g, s, 0, -h * .28, size, OUT, 'Bangers', 'center'); g.restore(); }

/* ================================================================ 1. cold open: frozen hallway */
SC.s01 = (X, t) => {
  const a = Lt('s01_02'), b = Le('s01_02'), k1 = a + 2.0, poke = a + 2.45, k2 = a + 2.9, k3 = b - .25;
  const heroX = tt => tt < k1 ? mix(140, 1300, clamp(tt / k1)) : tt < k2 ? 1300 : mix(1300, 1660, clamp((tt - k2) / (k3 - k2)));
  const hx = heroX(t), walking = t < k1 || (t > k2 && t < k3);
  const cam = shots(t, (typeof claps !== 'undefined' ? claps : []), [
    { t: 0, cx: tt => heroX(tt) + 180, cy: 560, z: 1.0, w: 2600 },
    { t: k2 + .35, cx: 1770, cy: 520, z: 1.6, z2: 1.7, w: 2600 },
    { t: Lt('s01_03') - .1, cx: 1660, cy: 600, z: 1.3, z2: 1.38, w: 2600 },
    { t: Lt('s01_06') - .1, cx: 1250, cy: 560, z: 1.0, z2: 1.05, w: 2600 },
    { t: Lt('s01_08') - .05, cx: 1665, cy: 470, z: 2.1, z2: 2.25, w: 2600 },
  ]);
  const st = stage(cam);
  st.wld(g => drawSet(g, 'hallway'));
  const fr = { still: 1, t: 0, blink: 0, s: S0, y: FEET };
  st.wld(g => {
    drawChar(g, 'ex1', { ...fr, x: 620, jump: 70, hL: [-80, -760], hR: [90, -770], open: .5, mouth: .5 });
    drawChar(g, 'ex2', { ...fr, x: 900, open: .45, hR: [170, -520], look: [10, 0] });
    drawChar(g, 'ex4', { ...fr, x: 1030, blink: 1, open: .7, look: [-10, 0], hL: [-150, -330] });
    drawChar(g, 'ex5', { ...fr, x: 1220, hR: [150, -720], look: [12, -8], mouth: .4 });
    drawChar(g, 'ex6', { ...fr, x: 1560, hL: [-120, -640], hR: [-30, -660], wide: .6, open: .4, look: [-12, -6] });
    drawChar(g, 'nacho', { ...fr, x: 1860, rot: -.22, hx: -10, hy: 10, blink: 1, open: .95, hL: [-60, -610], hR: [40, -600], lean: -.05 });
    dropsSpray(g, 1825, 455, 16, 3, 1.2);
    const bx = 1420 + 22 * R(t, poke, poke + .2, outC); propBall(g, bx, 470, 40, .3 + .6 * R(t, poke, poke + .3, outC));
  });
  // hero
  let hp = { x: hx, y: FEET, s: S0, t, walk: walking ? 1 : 0, phase: walkPh(hx), look: [8, -4], mouth: .35 };
  if (t > poke - .35 && t < poke + .4) { const u = bump(t, poke - .35, poke + .4); hp.hR = [mix(112, 150, u), mix(-200, -585, u)]; hp.look = [14, -14]; }
  if (t > k3 && t < Lt('s01_03')) { hp.hR = [170 + Math.sin(t * 16) * 22, -590]; hp.look = [16, -8]; hp.brow = .4; hp.mouth = .2; }
  if (t >= Lt('s01_03') - .1 && t < Lt('s01_06')) { const u = R(t, Lt('s01_03') - .1, Lt('s01_03') + .35, back), G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = POSE.shrug(u, G); hp.mouth = mix(.4, .9, u); hp.look = [0, 0];
    const fall = R(t, Lt('s01_05'), Le('s01_05')); hp.mouth = mix(hp.mouth, -.25, fall); hp.brow = .6 * fall; [hp.hL, hp.hR] = POSE.shrug(u * (1 - fall * .8), G); }
  if (t >= Lt('s01_06')) { hp.look = [0, 2]; hp.mouth = .2; }
  if (t >= Lt('s01_08') - .05) { const G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = POSE.shrug(R(t, Lt('s01_08'), Lt('s01_08') + .4, back) * .7, G); hp.mouth = -.3; hp.brow = .7; hp.sweat = 1; hp.look = [0, 0]; }
  st.col(g => drawChar(g, 'tu', hp));
  compose2(X, st, { amt: 1 });
};

/* ================================================================ 2. title card */
SC.s02 = (X, t) => {
  const tc = .5, cam = { cx: 1250, cy: 560, z: 1.0 }, claps = [{ t: tc }], wt = worldClock(t, claps), fz = isFrozen(t, claps);
  const st = stage(cam); st.wld(g => drawSet(g, 'hallway'));
  st.wld(g => { const o = (n, x0, v, sd) => { const x = x0 + v * wt; drawChar(g, n, { x, y: FEET, s: S0, t: wt, still: fz, blink: fz ? 0 : null, walk: 1, phase: walkPh(x), flip: v < 0 ? -1 : 1 }); };
    o('ex3', 700, 120, 1); o('ex2', 960, -110, 2); o('nacho', 1600, -90, 3); o('ex5', 1850, 100, 4); });
  const hp = { x: 1250, y: FEET, s: S0, t, mouth: .6, look: [0, 0] }; const G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = clapHands(t, tc, G, 2.5); hp.armsFront = 1;
  st.col(g => drawChar(g, 'tu', hp));
  const [px, py] = worldToScreen(cam, ...clapPoint('tu', hp));
  compose2(X, st, { ...freezeState(t, [{ t: tc, x: px, y: py, screen: 1 }], cam) });
  titleCard(X, '¿QUÉ PASARÍA SI PUDIERAS', 'DETENER EL TIEMPO?', R(t, tc + .25, tc + .7, outC), t);
};

/* ================================================================ 3. bedroom, the first clap */
function lyingHead(g, x = 300, y = 680, p = {}) { drawHead(g, CAST.tu, x, y, -1.35, Object.assign({ sleep: 1 }, p)); }
SC.s03 = (X, t) => {
  const tc = Lm('s03_03', .3), claps = [{ t: tc }], wt = worldClock(t, claps), fz = isFrozen(t, claps), up = Lt('s03_03') - .05;
  const cam = shots(t, (typeof claps !== 'undefined' ? claps : []), [
    { t: 0, cx: 700, cy: 600, z: 1.0, z2: 1.06 },
    { t: Lt('s03_02') - .1, cx: 760, cy: 660, z: 1.55, z2: 1.62 },
    { t: up, cx: 760, cy: 620, z: 1.25 },
    { t: Lt('s03_04') - .05, cx: 860, cy: 640, z: 1.5, z2: 1.55 },
    { t: Lt('s03_05') - .05, cx: 760, cy: 560, z: 1.0, z2: 1.04 },
    { t: Lt('s03_06') - .05, cx: 1080, cy: 650, z: 1.85, z2: 1.95 },
  ]);
  const st = stage(cam); st.wld(g => { drawSet(g, 'bedroom'); bedBack(g); nightstand(g); });
  const ring = wt > Lt('s03_02') && wt < tc ? wt : 0;
  st.wld(g => propAlarm(g, 1075, 700, .7, 6, 59, ring));
  // cat: sits on the rug, jumps toward the bed just before the clap and stays in mid-air
  const j0 = tc - .45, ju = clamp((wt - j0) / .9);
  st.wld(g => { if (wt < j0) drawCat(g, 1320, 1010, .7, { flip: -1, blink: autoBlink(wt, 4) }); else drawCat(g, mix(1320, 860, ju), 1010 - Math.sin(ju * Math.PI) * 380 - ju * 200, .7, { flip: -1, jump: .2 + .8 * Math.sin(Math.min(1, ju * 1.6) * Math.PI / 2), wide: 1 }); });
  if (t < up) { st.col(g => lyingHead(g, 300, 680, { sleep: t < Lt('s03_02') + .25, blink: 0, mouth: t > Lt('s03_02') ? -.4 : .2, brow: t > Lt('s03_02') + .3 ? -.6 : null, lid: t > Lt('s03_02') + .25 ? .5 : 0 }));
    st.wld(g => bedFront(g)); if (t < Lt('s03_02')) zzz(st.A, 360, 560, t); }
  else {
    const hp = { x: 470, y: 945, s: S0, t, mouth: -.2, brow: -.4, lid: .35, look: [0, 0] }; const G = charGeom(CAST.tu, hp);
    if (t < tc + 1.2) { [hp.hL, hp.hR] = clapHands(t, tc, G, .3, -80); hp.armsFront = 1; }
    if (t > tc + .2) { hp.lid = 0; hp.brow = .5; hp.mouth = -.1; }
    if (t >= Lt('s03_04') - .05) { hp.look = [16, 6]; hp.brow = .7; hp.wide = .3; }
    if (t >= Lt('s03_05') - .05) { hp.look = [Math.sin((t - Lt('s03_05')) * 3) * 18, 0]; hp.wide = .5; }
    if (t >= Lt('s03_06') - .05) { hp.look = [18, -4]; hp.hR = [mix(112, 330, R(t, Lt('s03_06'), Lt('s03_06') + .6)), mix(-200, -420, R(t, Lt('s03_06'), Lt('s03_06') + .6))]; hp.wide = .6; hp.open = .3; }
    if (t > up && t < up + .25) hp.hy = -20 * (1 - (t - up) / .25);
    st.col(g => drawChar(g, 'tu', hp));
    st.wld(g => bedFront(g, .6));
    var cp = worldToScreen(cam, ...clapPoint('tu', hp));
  }
  compose2(X, st, freezeState(t, [{ t: tc, x: cp ? cp[0] : W / 2, y: cp ? cp[1] : H / 2, screen: 1 }], cam));
};

/* ================================================================ 4. kitchen: the coffee sculpture, second clap */
function coffeeStream(g, sx, sy, ex, ey, wob = 0) { g.lineCap = 'round'; g.beginPath(); g.moveTo(sx, sy); g.bezierCurveTo(sx - 30, sy + 40, ex + wob, ey - 90, ex, ey);
  g.strokeStyle = OUT; g.lineWidth = 22; g.stroke(); g.strokeStyle = '#6a3b22'; g.lineWidth = 12; g.stroke(); g.strokeStyle = 'rgba(255,220,180,.35)'; g.lineWidth = 3; g.stroke(); }
SC.s04 = (X, t) => {
  const tc = Lm('s04_06', .12), claps = [{ t: tc }], wt = worldClock(t, claps, 1), fz = isFrozen(t, claps, 1);
  const cam = shots(t, (typeof claps !== 'undefined' ? claps : []), [
    { t: 0, cx: 900, cy: 560, z: 1.0, z2: 1.05 },
    { t: Lt('s04_02') - .05, cx: 1140, cy: 560, z: 1.7, z2: 1.78 },
    { t: Lt('s04_03') - .05, cx: 990, cy: 640, z: 1.6, z2: 1.7 },
    { t: Lt('s04_06') - .05, cx: 960, cy: 600, z: 1.2 },
    { t: Lt('s04_07') - .05, cx: 990, cy: 660, z: 1.65, z2: 1.75 },
    { t: Le('s04_08') + .05, cx: 1060, cy: 600, z: 1.35 },
    { t: Lt('s04_09') - .1, cx: 960, cy: 560, z: 1.0 },
  ]);
  const st = stage(cam); st.wld(g => drawSet(g, 'kitchen'));
  // mom pours: pot held over where the mug was; the mug gets slid aside by the hero
  const slide = R(t, Lm('s04_03', .45), Le('s04_03'));
  const mugX = mix(960, 870, slide), potX = 1080, potY = 610;
  const mp = { x: 1210, y: FEET, s: S0, t: wt, still: fz, blink: fz ? 0 : null, mouth: .3, look: [-14, 10], hL: [(potX + 30 - 1210) / (S0 * 1.03), (potY - 10 - FEET) / (S0 * 1.03)], hR: [128, -250] };
  if (wt > .3) { mp.look = [-10, 18]; mp.open = R(wt, .4, .7); mp.wide = R(wt, .4, .7) * .7; }
  st.wld(g => drawChar(g, 'mama', mp));
  st.wld(g => { const sx = potX - 62, sy = potY - 36;
    if (!fz && wt > .05) coffeeStream(g, sx, sy, 960, 780, Math.sin(wt * 20) * 4); else coffeeStream(g, sx, sy, 960, 724);
    propCoffeePot(g, potX, potY, .7, -.75); });
  // puddle on the table after the world resumes
  const pud = clamp(wt / 2.2);
  st.wld(g => { kitchenTable(g); if (pud > 0) { ell(g, 960, 784, 40 + 190 * pud, 10 + 8 * pud, 0, '#6a3b22', 4); if (pud > .5) for (const dx of [-140, 160]) { const k = R(wt, 1.2, 2.2); shape(g, q => rrPath(q, 960 + dx * pud - 6, 790, 12, 30 + 120 * k, 6), '#6a3b22', 3); } }
    propMug(g, mugX, 752, 1, '#f4f1ea'); });
  // hero walks in behind the table
  const hxw = mix(160, 840, R(t, .2, Lt('s04_02') - .2, lin)), walking = t > .2 && t < Lt('s04_02') - .2;
  const hp = { x: hxw, y: FEET, s: S0, t, walk: walking ? 1 : 0, phase: walkPh(hxw), mouth: .2, look: [14, 0] };
  if (t > Lt('s04_03') - .05) { hp.look = [16, 10]; hp.rot = .08; hp.brow = .5; hp.wide = .3; }
  if (t > Lm('s04_03', .3) && t < Le('s04_03') + .15) { const u = R(t, Lm('s04_03', .3), Lm('s04_03', .45)); hp.hR = [mix(112, (mugX + 36 - hxw) / S0, u), mix(-200, (744 - FEET) / S0, u)]; }
  const touch = R(t, Lt('s04_04'), Lt('s04_04') + .4) * (1 - R(t, Le('s04_05') + .2, Le('s04_05') + .5));
  if (touch > 0) { hp.hR = [mix(112, (995 - hxw) / S0, touch), mix(-200, (650 - FEET) / S0, touch)]; hp.holdR = (g, x, y) => { if (t > Lt('s04_04') + .35) circ(g, x + 4, y - 18, 7, '#6a3b22', 3); }; }
  if (t > Lt('s04_05')) { hp.mouth = .7; hp.brow = .8; hp.wide = .2; }
  if (t > tc - .5 && t < tc + 1.2) { const G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = clapHands(t, tc, G, .3); hp.armsFront = 1; hp.holdR = null; }
  if (t > tc + .6) { hp.look = [10, 16]; hp.wide = .6; hp.mouth = -.3; hp.open = t > Lt('s04_08') ? .3 : 0; }
  if (t > Le('s04_08') + .05) { hp.sweat = 1; hp.look = [16, 0]; }
  st.col(g => drawChar(g, 'tu', hp));
  st.wld(g => kitchenTable(g));
  st.wld(g => propMug(g, mugX, 752, 1, '#f4f1ea'));
  const cp = worldToScreen(cam, ...clapPoint('tu', hp));
  compose2(X, st, freezeState(t, [{ t: tc, x: cp[0], y: cp[1], screen: 1 }], cam, 1));
  if (t > Le('s04_08') - .1 && t < Lt('s04_09') - .1) { const [bx, by] = worldToScreen(cam, 1260, 420); bubble(X, '¿EH?', bx, by, R(t, Le('s04_08') - .1, Le('s04_08') + .2, outC), 70); }
  ruleCard(X, 1, 'UN APLAUSO: TODO SE DETIENE', t > Lt('s04_10') - .1 ? 'OTRO APLAUSO: TODO SIGUE' : '', R(t, Lt('s04_09') - .2, Lt('s04_09') + .2, outC));
};

/* ================================================================ 5. sleeping eight more hours */
SC.s05 = (X, t) => {
  const tc = Lm('s05_01', .22), claps = [{ t: tc }], wt = worldClock(t, claps), fz = isFrozen(t, claps), flop = Lm('s05_01', .86), wake = Lt('s05_03') - .05;
  const cam = shots(t, (typeof claps !== 'undefined' ? claps : []), [
    { t: 0, cx: 1000, cy: 580, z: 1.12 },
    { t: flop, cx: 520, cy: 640, z: 1.5, z2: 1.6 },
    { t: wake, cx: 700, cy: 620, z: 1.3 },
    { t: Lm('s05_03', .45), cx: 1075, cy: 690, z: 2.6, z2: 2.7 },
    { t: Lt('s05_04') - .05, cx: 640, cy: 560, z: 1.2, z2: 1.28 },
  ]);
  const st = stage(cam); st.wld(g => { drawSet(g, 'bedroom'); bedBack(g); nightstand(g); propAlarm(g, 1075, 700, .7, 6, 59, 0); drawCat(g, 1650, 1010, .7, { flip: -1, blink: fz ? 0 : autoBlink(wt, 4) }); });
  let hp = null;
  if (t < flop) { hp = { x: 1300, y: FEET + 40, s: S0, t, mouth: .8, look: [0, 0], brow: .3 }; const G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = clapHands(t, tc, G, .4); hp.armsFront = 1;
    if (t > flop - .35) { hp.lean = -.35 * R(t, flop - .35, flop); hp.blink = 1; }
    st.wld(g => bedFront(g, 1)); st.col(g => drawChar(g, 'tu', hp)); }
  else if (t < wake) { st.col(g => lyingHead(g, 300, 680, { sleep: 1, mouth: .5 })); st.wld(g => bedFront(g, 1)); }
  else { const sp = { x: 470, y: 945, s: S0, t, mouth: .5, look: [16, 4], brow: .4 };
    if (t > Lm('s05_03', .45)) { sp.wide = .5; sp.mouth = .8; }
    if (t > Lt('s05_04') - .05) { const G = charGeom(CAST.tu, sp); [sp.hL, sp.hR] = POSE.stretch(R(t, Lt('s05_04'), Lt('s05_04') + .5, back), G); sp.blink = 1; sp.mouth = 1; sp.look = [0, 0]; }
    if (t > wake && t < wake + .25) sp.hy = -20 * (1 - (t - wake) / .25);
    st.col(g => drawChar(g, 'tu', sp)); st.wld(g => bedFront(g, .6)); hp = sp; }
  const cp = hp ? worldToScreen(cam, ...clapPoint('tu', hp)) : [W / 2, H / 2];
  compose2(X, st, freezeState(t, [{ t: tc, x: cp[0], y: cp[1], screen: 1 }], cam));
  if (t > flop && t < wake) { zzz(X, ...worldToScreen(cam, 360, 560), t); const hrs = Math.min(8, Math.floor(R(t, flop + .3, wake - .4, lin) * 8) + 1); bigCounter(X, 'SIESTA:', '+' + hrs + (hrs === 1 ? ' HORA' : ' HORAS'), R(t, flop + .2, flop + .5, outC)); }
  if (t > Lt('s05_04')) for (let i = 0; i < 5; i++) { const u = (t * .8 + i / 5) % 1, [sx, sy] = worldToScreen(cam, 640 + Math.cos(i * 1.3) * 260, 360 + Math.sin(i * 2.1) * 120); X.save(); X.globalAlpha = Math.sin(u * Math.PI); text(X, '✦', sx, sy, 60, '#fde047', 'Arial', 'center', OUT, 6); X.restore(); }
};
