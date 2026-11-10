/* Episode 5, extra scenes for the long cut. Same conventions as ep05.js (scene-local seconds, gy = 944 floor). */
const BOSS = { col: '#5c6a7a', colD: '#46525f', hair: 'cap', hairCol: '#3b3f52', ph: 2.7, sc: 1.45 };
const WAITER = { col: '#3b3f52', colD: '#2a2333', hair: 'cap', hairCol: '#e8382f', ph: 1.9 };
const CLERK = { col: '#e3b44c', colD: '#bf8a24', hair: 'bob', hairCol: '#2c201d', ph: 3.6 };
const NEIGH = { col: '#9fb8d8', colD: '#7a96bd', hair: 'nightcap', hairCol: '#5d70a3', legs: '#9fb8d8', shoes: '#5d70a3', ph: 4.4, sc: 1.12 };
const hero = (col, colD) => Object.assign({}, HERO, { col, colD, id: (HERO.id ||= ++SMID) });
const ARMOR_ON = { legL: 1, legR: 1, chest: 1, armL: 1, armR: 1, helmet: 1 };
function textPop(s, x, y, size, col, t0, t, stroke = 10) { const k = pop(t, t0, 1); if (k <= 0) return; X.save(); X.translate(x, y); X.scale(k, k); text(s, 0, 0, size, col, 'center', 'Bangers', stroke); X.restore(); }
function hoodieDrop(gx, gy, u, col) {        // a hoodie pulled on over the head (falls from above onto the torso)
  if (u <= 0 || u >= 1) return; const top = TOP(gy), dy = (1 - outq(u)) * -360;
  X.save(); X.translate(0, dy); shape(X, g => { g.moveTo(gx - 104, top + 20); g.quadraticCurveTo(gx - 104, top, gx - 70, top - 4); g.lineTo(gx + 70, top - 4); g.quadraticCurveTo(gx + 104, top, gx + 104, top + 20); g.lineTo(gx + 108, gy - 200); g.lineTo(gx - 108, gy - 200); g.closePath(); }, col); X.restore();
}

SCENES.push(
/* N1: morning, he tries to cover the glow with hoodies */
{ id: 'N1', dur: 7.6, draw(t) {
  camera(t, [{ a: 0, b: 99, cx: 1400, cy: 560, z: 1.3, dz: .05 }]);
  X.drawImage(BGS.bedD, 0, 0); bedFront(t, 0);
  const gx = 1480, gy = 944, ht = TOP(gy), n = t < 2.75 ? 0 : t < 3.45 ? 1 : 2;
  const cols = [['#e4ae3c', '#bf8a24'], ['#4fae7a', '#2f8a5a'], ['#8a6fd1', '#6a52ad']];
  const shrug = R(t, 4.8, 5.2) * (1 - R(t, 6.6, 7.0)), beams = R(t, 4.9, 5.3);
  person(t, gx, gy, hero(...cols[n]), { layers: cols.slice(0, n).map(c => c[0]), chestLight: .9 + .1 * Math.sin(t * 4),
    handL: shrug > 0 ? mix2([gx - 112, gy - 212], [gx - 190, ht + 60], shrug) : (t < 2.4 ? [gx - 30, ht + 110] : undefined),
    handR: shrug > 0 ? mix2([gx + 112, gy - 212], [gx + 190, ht + 60], shrug) : (t < 2.4 ? [gx + 30, ht + 100] : undefined),
    look: [0, 14], brow: .6, wavy: n > 0, mouth: -.3, blink: blinkAmt(t, [1.4, 6.2]) });
  hoodieDrop(gx, gy, R(t, 2.5, 2.8, x => x), cols[1][0]); hoodieDrop(gx, gy, R(t, 3.2, 3.5, x => x), cols[2][0]);
  if (beams > 0) { X.save(); X.globalCompositeOperation = 'lighter'; X.globalAlpha = .45 * beams; X.fillStyle = '#9fe4ff';
    for (const [a, l] of [[-2.75, 300], [-0.5, 340], [-0.1, 300], [0.5, 280], [2.6, 280], [3.05, 240]]) { X.beginPath(); X.moveTo(gx, ht + 96); X.lineTo(gx + Math.cos(a - .05) * l, ht + 96 + Math.sin(a - .05) * l); X.lineTo(gx + Math.cos(a + .05) * l, ht + 96 + Math.sin(a + .05) * l); X.fill(); } X.restore(); }
  for (const [a, b] of [[2.5, 2.8], [3.2, 3.5]]) { const k = bump(t, a + .2, b + .4); if (k > 0) puff(gx + 120, ht - 40, k, 'FWUMP'); }
  letterbox();
} },
/* N2: Dave's list */
{ id: 'N2', dur: 5.4, draw(t) {
  card(t, '#4a3a52', () => {
    X.save(); X.translate(820, 560); X.rotate(-.04); X.scale(pop(t, .2, 1), pop(t, .2, 1));
    fillR(X, -360, -380, 720, 760, 14, '#fdf6d8', 8); X.strokeStyle = 'rgba(80,120,200,.35)'; X.lineWidth = 3; for (let y = -260; y < 360; y += 70) { X.beginPath(); X.moveTo(-330, y); X.lineTo(330, y); X.stroke(); }
    X.strokeStyle = 'rgba(220,80,80,.5)'; X.beginPath(); X.moveTo(-270, -380); X.lineTo(-270, 380); X.stroke();
    text("DAVE'S LIST", 0, -290, 96, '#2c3d6e', 'center', 'Bangers', 0);
    [['1. CAKE', 1.3], ['2. BALLOONS', 2.0], ['3. MORE TAPE', 2.7]].forEach(([s, a], i) => { if (t > a) { X.save(); X.globalAlpha = R(t, a, a + .15); text(s, -230, -150 + i * 110, 84, '#2c201d', 'left', 'Bangers', 0); X.restore(); } });
    if (t > 3.6) { X.save(); X.globalAlpha = R(t, 3.6, 3.8); text("RULE #1: DON'T SNAP", 0, 250, 70, '#e8382f', 'center', 'Bangers', 0);
      X.strokeStyle = '#e8382f'; X.lineWidth = 7; X.beginPath(); X.moveTo(-300, 275); X.lineTo(-300 + 600 * R(t, 3.8, 4.2), 275); X.stroke(); X.restore(); }
    X.restore();
    X.save(); X.translate(1530, 990); X.scale(.8, .8); X.translate(-1530, -990); dave(t, 1530, 990, { noMug: 1, handR: [1690, 700], blink: blinkAmt(t, [2.4]) }); X.restore();
    shape(X, g => rrPath(g, 1648, 560, 16, 110, 6), '#e8b23a', 3);
  });
  letterbox();
} },
/* N12: breakfast in oven mitts: cereal everywhere */
{ id: 'N12', dur: 6.6, draw(t) {
  camera(t, [{ a: 0, b: 99, cx: 900, cy: 560, z: 1.2, dz: .05 }]);
  X.drawImage(BGS.kitchen, 0, 0); windowCracks(1); windowTape(1);
  const gx = 1180, gy = 944, ht = TOP(gy), bx = 920;
  cerealBowl(bx, 600);
  dave(t, 520, gy, { look: [18, 4], lid: .3, lift: R(t, 4.6, 5.0) * (1 - R(t, 5.8, 6.2)), blink: blinkAmt(t, [2.2]) || (t > 5.1 && t < 5.7 ? 1 : 0) });
  const shake = t > 1.4 && t < 3.6 ? Math.sin(t * 22) * 22 : 0, tilt = R(t, .9, 1.4);
  person(t, gx, gy, HERO, { mitts: 1, handL: [1010 + shake * .5, 520 + shake], handR: [1100 + shake * .5, 540 + shake], look: [-20, 6], brow: t > 1.4 ? .8 : 0, wide: t > 1.6 && t < 3.8, mouth: t > 3.8 ? -.6 : .3, sweat: t > 2 ? .6 : 0, blink: blinkAmt(t, [4.4]) });
  const hl = HERO._hl || [1010, 520], hr = HERO._hr || [1100, 540], c = [(hl[0] + hr[0]) / 2, (hl[1] + hr[1]) / 2 - 20];
  X.save(); X.translate(c[0], c[1]); X.rotate(-tilt * 2.0); fillR(X, -40, -70, 80, 130, 8, '#e8382f'); fillR(X, -30, -40, 60, 50, 6, '#fde047', 3); text('FLAKES', 0, 40, 22, '#fdf6d8', 'center', 'Bangers', 0); X.restore();
  // flakes: a jet from the box, then everywhere; they land on the counter, the floor and his head
  const r = rng(9);
  for (let i = 0; i < 70; i++) { const t0 = 1.4 + r() * 2.2, ang = -Math.PI * (.15 + r() * .9), sp = 300 + r() * 700, u = t - t0;
    const land = r() < .3 ? 600 : (r() < .5 ? ht - 168 : 930), lx = c[0] - 60 + (r() - .5) * 80;
    if (u < 0) continue; let x = lx + Math.cos(ang) * sp * u, y = c[1] - 60 + Math.sin(ang) * sp * u + 1400 * u * u;
    if (y > land) { y = land; x = lx + Math.cos(ang) * sp * Math.min(u, .6); if (land === ht - 168) x = gx - 60 + (i % 7) * 20; }
    flake(x, y, i + u * 8, .9); }
  burst('SHAKE!', bx + 260, 300, .55, bump(t, 1.5, 2.1), -.12);
  letterbox();
} },
/* N20: doors and shoelaces in oven mitts (Dave helps with both) */
{ id: 'N20', dur: 8.0, draw(t) {
  if (t < 4.2) {
    camera(t, [{ a: 0, b: 99, cx: 900, cy: 560, z: 1.15, dz: .04 }]);
    X.drawImage(BGS.hall, 0, 0);
    const open = R(t, 3.0, 3.6), knob = hallDoor(open);
    const gx = 1040, gy = 944, ht = TOP(gy), fum = t < 2.9;
    dave(t, 560, gy, { noMug: 1, handR: t > 2.6 && t < 3.7 ? [knob[0] + 10, knob[1]] : undefined, look: [16, 6], lid: .35, blink: blinkAmt(t, [1.6]) });
    person(t, gx, gy, HERO, { mitts: 1, handL: fum ? [knob[0] + 28 + Math.sin(t * 16) * 14, knob[1] + Math.cos(t * 13) * 18] : undefined, look: fum ? [-16, 4] : [-10, 0], brow: fum ? .7 : 0, sweat: fum ? .6 : 0, wavy: !fum, blink: blinkAmt(t, [3.6]) });
  } else {
    const u = t - 4.2; camera(u, [{ a: 0, b: 99, cx: 960, cy: 560, z: 1.0, dz: .03 }]);
    X.fillStyle = lg(X, 0, H, [[0, '#5a4636'], [1, '#43352a']]); X.fillRect(0, 0, W, H); vignette(X, .4);
    // a giant sneaker, laces wobbling
    // a sneaker in side view: sole, upper, toe cap, tongue, eyelets, criss-cross laces
    const upper = g => { g.moveTo(420, 850); g.lineTo(424, 640); g.quadraticCurveTo(430, 560, 520, 556); g.lineTo(760, 572); g.quadraticCurveTo(840, 540, 900, 548); g.lineTo(1220, 640); g.quadraticCurveTo(1500, 690, 1540, 850); g.closePath(); };
    shape(X, upper, '#3f6fb5', 6); X.save(); X.beginPath(); upper(X); X.clip(); X.fillStyle = 'rgba(0,0,0,.14)'; X.fillRect(380, 760, 1200, 120);
    shape(X, g => { g.moveTo(1290, 860); g.quadraticCurveTo(1300, 690, 1420, 712); g.quadraticCurveTo(1540, 750, 1560, 860); g.closePath(); }, '#f4f1ea', 5);
    shape(X, g => { g.moveTo(520, 760); g.quadraticCurveTo(900, 700, 1260, 790); }, null, 0); X.strokeStyle = '#fdf6d8'; X.lineWidth = 26; X.beginPath(); X.moveTo(500, 780); X.quadraticCurveTo(900, 690, 1280, 800); X.stroke(); X.restore();
    shape(X, g => { g.moveTo(760, 572); g.quadraticCurveTo(770, 470, 860, 480); g.quadraticCurveTo(900, 500, 900, 548); g.closePath(); }, '#2f5a99', 5);
    fillR(X, 380, 846, 1190, 74, 30, '#f4f1ea', 6); X.strokeStyle = 'rgba(0,0,0,.15)'; X.lineWidth = 6; for (let x = 430; x < 1540; x += 60) { X.beginPath(); X.moveTo(x, 900); X.lineTo(x + 20, 900); X.stroke(); }
    const eye = i => [mix(820, 1160, i / 4), mix(596, 652, i / 4)], eyeB = i => [mix(860, 1190, i / 4), mix(640, 700, i / 4)];
    for (let i = 0; i < 5; i++) for (const e of [eye(i), eyeB(i)]) shape(X, g => g.arc(e[0], e[1], 9, 0, 7), '#e7e0d6', 3);
    X.strokeStyle = '#f4f1ea'; X.lineWidth = 9; X.lineCap = 'round'; for (let i = 0; i < 4; i++) { X.beginPath(); X.moveTo(...eye(i)); X.lineTo(...eyeB(i + 1)); X.moveTo(...eyeB(i)); X.lineTo(...eye(i + 1)); X.stroke(); }
    const tied = u > 2.6;
    X.strokeStyle = '#f4f1ea'; X.lineWidth = 9;
    if (!tied) for (let i = 0; i < 2; i++) { X.beginPath(); X.moveTo(...eye(0)); X.bezierCurveTo(760 + i * 60 + Math.sin(u * 9 + i) * 70, 700, 700 + Math.cos(u * 7 + i) * 90, 780, 640 + i * 70 + Math.sin(u * 5) * 40, 830); X.stroke(); }
    else { for (const sd of [-1, 1]) { X.beginPath(); X.ellipse(800 + sd * 50, 560, 50, 24, sd * .3, 0, 7); X.stroke(); } X.beginPath(); X.moveTo(800, 574); X.lineTo(750, 670); X.moveTo(800, 574); X.lineTo(860, 662); X.stroke(); sparkle(880, 510, 1, bump(u, 2.6, 3.4)); }
    if (!tied) { ovenMitt(640 + Math.sin(u * 8) * 40, 520 + Math.cos(u * 6) * 30, 2.4, .4 + Math.sin(u * 5) * .2, 1); ovenMitt(1000 + Math.cos(u * 7) * 40, 500 + Math.sin(u * 9) * 30, 2.4, -.4, -1); }
    else { shape(X, g => g.arc(960, 440, 52, 0, 7), '#f1ece6'); X.save(); X.lineCap = 'round'; X.strokeStyle = OUT; X.lineWidth = 120; X.beginPath(); X.moveTo(1000, 400); X.lineTo(1400, -100); X.stroke(); X.strokeStyle = '#2c3d6e'; X.lineWidth = 108; X.stroke(); X.restore(); shape(X, g => g.arc(960, 440, 52, 0, 7), '#f1ece6'); }
    if (u > 2.1 && u < 2.6) { const k = R(u, 2.1, 2.6); X.save(); X.lineCap = 'round'; X.strokeStyle = OUT; X.lineWidth = 120; X.beginPath(); X.moveTo(mix(1700, 1000, k), mix(-200, 400, k)); X.lineTo(1800, -300); X.stroke(); X.strokeStyle = '#2c3d6e'; X.lineWidth = 108; X.stroke(); X.restore(); shape(X, g => g.arc(mix(1660, 960, k), mix(-160, 440, k), 52, 0, 7), '#f1ece6'); }
  }
  letterbox();
} },
/* N10: working from home. The boss snaps on every idea; the mitts hold */
{ id: 'N10', dur: 11.0, draw(t) {
  const SN = [4.0, 4.9, 5.6, 6.2, 6.7, 7.1, 8.2, 8.9];
  const snapAt = t => Math.max(...SN.map(a => bump(t, a - .1, a + .12)));
  if (t < 3.3 || t >= 7.5) {
    const close = t >= 7.5;
    camera(t, close ? [{ a: 0, b: 99, cx: 1450, cy: 470, z: 1.9, dz: .06 }] : [{ a: 0, b: 99, cx: 1380, cy: 560, z: 1.3, dz: .04 }]);
    X.drawImage(BGS.bedD, 0, 0); bedFront(t, 0);
    const gx = 1450, gy = 944, ht = TOP(gy), tw = snapAt(t), up = close ? bump(t, 8.2, 9.2) : 0, thumb = R(t, 9.6, 9.9);
    person(t, gx, gy, HERO, { mitts: 1, handL: up > 0 ? mix2([gx - 70, 690], [gx + 40, 600], up) : [gx - 70, 690 - tw * 14], handR: thumb > 0 ? [gx + 150, ht + 70] : mix2([gx + 70, 690 - tw * 18], [gx + 120, ht + 20], up),
      look: [0, 18], brow: close && t < 9.5 ? .8 : 0, sweat: close && t < 9.6 ? .8 : 0, wavy: close && t < 9.6, happy: thumb > .5, mouth: .4, blink: blinkAmt(t, [2.1]) });
    laptopDesk(gx, 700);
    if (tw > 0 && close) puff(gx + 170, ht - 20, tw, '!');
  } else {
    camera(t, [{ a: 0, b: 99, cx: 960, cy: 560, z: 1.0, dz: .03 }]);
    X.fillStyle = '#1d2030'; X.fillRect(0, 0, W, H);
    fillR(X, 200, 120, 1520, 840, 18, '#2c3346', 6);
    X.save(); X.beginPath(); rrPath(X, 230, 150, 1460, 700, 12); X.clip();
    X.fillStyle = lg(X, 150, 850, [[0, '#a3b6c9'], [1, '#7d8ea3']]); X.fillRect(230, 150, 1460, 700);
    fillR(X, 300, 200, 400, 300, 8, '#c9d4de'); fillR(X, 1300, 220, 300, 400, 8, '#8a9bb0');
    const bx = 900, gy = 1250, sn = snapAt(t), bt = gy - 460 * 1.45;
    person(t, bx, gy, BOSS, { handR: [bx + 250, bt - 40], snapR: sn, look: [0, 0], happy: sn > .3, mouth: .9, brow: -.4, blink: blinkAmt(t, [5.3]) });
    SN.forEach(a => { const k = bump(t, a, a + .9); if (k > 0) { const x = bx + 330 + ((a * 97) % 260) - 130, y = 300 - (t - a) * 110; glow(x, y, 110, .7 * k, '255,240,170'); shape(X, g => g.arc(x, y, 50 * k, 0, 7), '#fde047', 4); shape(X, g => g.rect(x - 20 * k, y + 44 * k, 40 * k, 26 * k), '#9a95a6', 3); } });
    X.restore();
    fillR(X, 230, 870, 1460, 60, 8, '#232838', 0); for (const [x, c] of [[860, '#e8382f'], [960, '#4e5a70'], [1060, '#4e5a70']]) shape(X, g => g.arc(x, 900, 22, 0, 7), c, 3);
    fillR(X, 250, 780, 200, 50, 6, 'rgba(0,0,0,.5)', 0); text('BOSS', 350, 818, 40, '#fff', 'center', 'Bangers', 0);
    // self view: you, sweating, the chest glowing through the hoodie
    X.save(); fillR(X, 1440, 600, 230, 230, 10, '#3c4670', 4); X.beginPath(); rrPath(X, 1444, 604, 222, 222, 8); X.clip(); X.translate(1555, 860); X.scale(.42, .42); X.translate(-1555, -860);
    person(t, 1555, 1075, HERO, { look: [0, 6], wavy: 1, sweat: .9, chestLight: .9, still: 1, noShadow: 1 }); X.restore();
  }
  letterbox();
} },
/* N3: the flight. The suit can fly; you cannot */
{ id: 'N3', dur: 10.0, draw(t) {
  camera(t, [{ a: 0, b: 99, cx: 960, cy: 560, z: 1.0, dz: .02, shake: t => bump(t, 5.3, 5.8) * 12 + bump(t, 9.0, 9.5) * 16 }]);
  X.drawImage(BGS.sky, 0, 0);
  scrollLayer(SKYL.far, t * 140); scrollLayer(SKYL.near, t * 420);
  // a billboard drifts in on the near layer and gets hit
  const bbx = 2300 - (t - 3.0) * 420; if (bbx > -600) { shape(X, g => g.rect(bbx + 200, 640, 26, 440), '#4e4a58', 4); fillR(X, bbx, 420, 460, 230, 10, '#f4f1e0'); text('FLY SAFE', bbx + 230, 560, 100, '#2f6fb5', 'center', 'Bangers', 0); }
  const hit = t > 5.35, spin = R(t, 5.35, 6.0) * Math.PI * 2;
  const fx = 760 + Math.sin(t * 1.3) * 120 + (t > 8.6 ? (t - 8.6) * 300 : 0), fy = t < 8.6 ? 470 + Math.sin(t * 2.1) * 90 + (hit ? 80 : 0) : 550 + (t - 8.6) * (t - 8.6) * 600;
  X.save(); X.translate(fx, fy); X.rotate(1.42 + Math.sin(t * 4.5) * .16 + spin + (t > 8.6 ? (t - 8.6) * 1.2 : 0)); X.scale(.62, .62);
  for (const fxp of [-30, 30]) { glow(fxp, 240, 90, .7, '255,200,120'); shape(X, g => { g.moveTo(fxp - 14, 236); g.quadraticCurveTo(fxp, 330 + Math.sin(t * 40) * 20, fxp + 14, 236); g.closePath(); }, '#ffcf6a', 3); }
  person(t, 0, 230, HERO, { armor: ARMOR_ON, handL: [-40, 230 - 460 - 170], handR: [40, 230 - 460 - 160], still: 1, noShadow: 1, chestGlow: .3, look: [0, -8], wide: hit && t < 6.5, mouthO: hit && t < 6.4 });
  X.restore();
  for (let i = 0; i < 4; i++) bird(((i * 520 + 1900) - t * (220 + i * 30)) % 2300 - 100, 220 + i * 70 + Math.sin(t * 2 + i) * 20, t + i, .9);
  burst('BONK!', 1000, 380, .75, bump(t, 5.35, 6.0), .12);
  if (t > 9.0) { burst('THUD!', 1250, 820, .9, bump(t, 9.0, 9.8), -.1); X.save(); X.globalAlpha = .7 * (1 - R(t, 9.0, 10.0)); for (let i = 0; i < 6; i++) shape(X, g => g.arc(1100 + i * 70, 1000 - R(t, 9, 10) * 60, 50 + i * 6, 0, 7), '#d8d1c3', 0); X.restore(); }
  letterbox();
} },
/* N23: café. In the suit snapping is safe: he snaps for the waiter again and again */
{ id: 'N23', dur: 9.6, draw(t) {
  camera(t, [{ a: 0, b: 99, cx: 960, cy: 560, z: 1.03, dz: .03 }]);
  X.drawImage(BGS.cafe, 0, 0);
  const gy = 944, hg = 1330, ht = TOP(gy), cg = 380;
  // waiter route: kitchen (right) -> customer -> hero -> back and forth
  const legs = [[0, 1850], [1.3, 640], [2.4, 640], [3.4, 920], [4.4, 920], [5.0, 1750], [5.3, 1750], [6.0, 920], [6.6, 920], [7.0, 1650], [7.3, 1650], [7.9, 920], [9.6, 920]];
  let wx = 1850; for (let i = 0; i < legs.length - 1; i++) { const [a, x0] = legs[i], [b, x1] = legs[i + 1]; if (t >= a && t < b) wx = mix(x0, x1, io((t - a) / (b - a))); }
  if (t >= 9.6) wx = 920;
  const moving = legs.some(([a, x0], i) => i < legs.length - 1 && t >= a && t < legs[i + 1][0] && x0 !== legs[i + 1][1]);
  const cups = (t > 4.2) + (t > 6.4) + (t > 8.2), annoyed = R(t, 6.0, 8.0);
  cafeTable(cg); cafeTable(hg - 210, cups);
  person(t, cg, gy, GUEST3, { handR: t > .3 && t < 1.2 ? [cg + 175, ht - 40] : undefined, snapR: t > .3 && t < 1.2 ? bump(t, .6, .8) : undefined, look: [12, 0], happy: t > 2.0, blink: blinkAmt(t, [3.3]) });
  person(t, wx, gy, WAITER, { walk: moving ? wx / 38 : undefined, handL: [wx - 80, 620], look: [wx > hg ? -14 : 14, 0], brow: -annoyed * .8, mouth: .5 - annoyed * 1.2, lid: annoyed * .5, blink: blinkAmt(t, [2.0, 5.2]) });
  shape(X, g => g.ellipse(wx - 90, 610, 60, 10, 0, 0, 7), '#c9c4b8', 4);
  const SN = [2.8, 5.0, 6.6], up = Math.max(...SN.map(a => bump(t, a - .5, a + .5)));
  person(t, hg, gy, HERO, { armor: ARMOR_ON, handR: mix2([hg + 112, gy - 212], [hg + 175, ht - 40], clamp(up * 1.6)), snapR: up > .3 ? Math.max(...SN.map(a => bump(t, a - .05, a + .15))) : undefined, handL: [hg - 150, 620],
    happy: t > 2.6, mouth: .9, look: [-12, 0], chestGlow: .2, blink: blinkAmt(t, [1.6]) });
  SN.forEach(a => burst('SNAP!', hg + 260, ht - 140, .5, bump(t, a, a + .4), .15));
  const n = 4 + (t > 2.8) + (t > 5.0) + (t > 6.6); if (t > 2.8) caption(`SNAPS: ${n}`, 1);
  letterbox();
} },
/* N4: balloons. The suit has a very strong grip */
{ id: 'N4', dur: 8.4, draw(t) {
  camera(t, [{ a: 0, b: 99, cx: 1000, cy: 560, z: 1.12, dz: .04 }]);
  X.drawImage(BGS.street, 0, 0);
  const gy = 944, vg = 1300, hg = 760, ht = TOP(gy);
  const POPS = [1.9, 3.3, 5.3], alive = [0, 1, 2, 3].map(i => i < 3 ? t < POPS[i] : t < 6.4);
  const hand = [vg - 200, 660];
  person(t, vg, gy, GUEST3, { handL: hand, look: [-14, -6], wide: t > 1.9 && t < 2.8, lid: t > 5.5 ? .5 : 0, mouth: t > 5.5 ? -.2 : .6, blink: blinkAmt(t, [3.9, 7.4]) });
  const B = [[-150, -300, '#e8382f'], [-60, -360, '#3fb6e8'], [20, -290, '#7bd36b'], [-70, -230, '#fde047']];
  B.forEach(([dx, dy, c], i) => { let bx = hand[0] + dx + Math.sin(t * 1.4 + i) * 8, by = hand[1] + dy + Math.sin(t * 1.9 + i) * 6;
    if (i === 3 && t > 6.4) { const u = t - 6.4; bx += u * 60; by -= u * u * 160 + u * 120; }
    if (!alive[i] && i < 3) { const k = bump(t, POPS[i], POPS[i] + .4); if (k > 0) burst('POP!', bx, by, .4, k, 0, '#ffffff'); return; }
    X.strokeStyle = OUT; X.lineWidth = 3; X.beginPath(); X.moveTo(bx, by + 52); X.quadraticCurveTo(bx + 10, by + 140, i === 3 && t > 6.4 ? bx : hand[0], i === 3 && t > 6.4 ? by + 200 : hand[1]); X.stroke();
    shape(X, g => g.ellipse(bx, by, 42, 52, 0, 0, 7), c); X.fillStyle = 'rgba(255,255,255,.45)'; X.beginPath(); X.ellipse(bx + 14, by - 18, 9, 14, -.5, 0, 7); X.fill(); });
  const reach = Math.max(...POPS.map(a => bump(t, a - .7, a + .3))), tgt = t < 2.5 ? [hand[0] - 150, hand[1] - 300] : t < 4 ? [hand[0] - 60, hand[1] - 330] : [hand[0] + 20, hand[1] - 290];
  person(t, hg, gy, HERO, { armor: ARMOR_ON, handR: mix2([hg + 112, gy - 212], [tgt[0] - 40, tgt[1] + 30], reach), look: t > 6.4 ? [10, -16] : [14, -8], brow: t > 3.4 ? .6 : 0, wide: POPS.some(a => t > a && t < a + .6), mouth: t > 6.4 ? -.8 : .2, chestGlow: .2, blink: blinkAmt(t, [4.4]) });
  if (t > 7.0) caption('BALLOONS: 0', R(t, 7.0, 7.25));
  letterbox();
} },
/* N13: hardware store. Signing with an armoured finger: screens count too */
{ id: 'N13', dur: 7.6, draw(t) {
  camera(t, [{ a: 0, b: 99, cx: 1100, cy: 540, z: 1.12, dz: .05, shake: t => bump(t, 2.95, 3.3) * 8 }]);
  X.drawImage(BGS.store, 0, 0);
  const gy = 944, cg = 1560, hg = 990, ht = TOP(gy), cracked = t > 3.0;
  person(t, cg, gy, CLERK, { handL: t < 2.2 ? mix2([cg - 112, gy - 212], [1320, 560], R(t, 1.0, 1.6)) : undefined, look: t > 3.0 ? [-22, 4] : [-16, 6], wide: t > 3.0 && t < 4.0, lid: t > 4.2 ? .5 : 0, mouth: .4, blink: blinkAmt(t, [1.9, 6.4]) });
  storeCounter(cracked);
  const reach = R(t, 2.2, 2.9) * (1 - R(t, 3.6, 4.2));
  person(t, hg, gy, HERO, { armor: ARMOR_ON, handR: mix2([hg + 112, gy - 212], [1218, 470], reach), snapR: reach > .5 ? 0 : undefined, look: [16, 4], wide: t > 3.0 && t < 4.4, mouthO: t > 3.1 && t < 4.0, mouth: t > 4.4 ? -.6 : .4, chestGlow: .2, blink: blinkAmt(t, [5.6]) });
  if (cracked && t < 3.5) { glow(1245, 460, 120, .8 * (1 - R(t, 3.0, 3.5)), '200,240,255'); }
  burst('CRUNCH', 1300, 300, .6, bump(t, 3.0, 3.6), -.1);
  if (t > 3.6) caption('SCREENS: 1', R(t, 3.6, 3.85));
  letterbox();
} },
/* N7: Dave's friends arrive; every handshake becomes an elbow bump */
{ id: 'N7', dur: 9.8, draw(t) {
  const k = t < 3.3 ? 0 : t < 6.5 ? 1 : 2, u = t - [0, 3.3, 6.5][k];
  camera(u, [{ a: 0, b: 99, cx: 980, cy: 560, z: 1.1, dz: .05 }]);
  X.drawImage(BGS.hall, 0, 0); hallDoor(1);
  const gy = 944, hg = 1330, ht = TOP(gy), G = [GUEST3, GUEST1, GUEST2][k];
  dave(t, 520, gy, { partyHat: 1, look: [16, 2], lid: .3, blink: blinkAmt(t, [2.0, 5.5, 8.4]) });
  const offer = R(u, .3, .8), bumpE = R(u, 1.3, 1.6) * (1 - R(u, 2.4, 2.8));
  const gx = mix(930, 1010, R(u, 0, .6));
  person(t, gx, gy, G, { handR: offer > 0 ? mix2([gx + 112, gy - 212], [hg - 170, gy - 330], offer * (1 - bumpE * .4)) : undefined, look: [16, 0], happy: u < 1.3, mouth: u > 1.6 ? .1 : .7, brow: u > 1.6 ? .4 : 0, wide: u > 1.6 && u < 2.4, blink: blinkAmt(u, [2.6]) });
  person(t, hg, gy, HERO, { pockets: bumpE < .1, handL: bumpE > 0 ? [hg - 60, gy - 360] : undefined, look: [-18, 0], wavy: 1, sweat: .3, partyHat: 0, blink: blinkAmt(u, [.9]) });
  if (bumpE > .5 && bumpE < 1) burst('BUMP', hg - 210, ht + 150, .35, bump(u, 1.4, 1.9), .1, '#fde047');
  if (u < .25 && k > 0) { X.save(); X.globalAlpha = 1 - u / .25; X.fillStyle = '#fff'; X.fillRect(0, 0, W, H); X.restore(); }
  letterbox();
} },
/* N8: the neighbour came to complain. He stayed */
{ id: 'N8', dur: 8.4, draw(t) {
  party(t + 6.0, 'suit', { shots: [{ a: 0, b: 99, cx: 900, cy: 560, z: 1.0, dz: .02 }], lights: [[t < 1.6 ? mix(-160, 230, io(t / 1.6)) : 230, 640, 420, .85]], extra: tt => {
    const gy = 1050, nx = t < 1.6 ? mix(-160, 230, io(t / 1.6)) : 230, dance = R(t, 4.6, 5.0), sw = Math.sin(t * Math.PI * 2);
    person(t, nx, gy, NEIGH, { walk: t < 1.6 ? t * 9 : undefined, bounce: dance * Math.abs(sw) * 10,
      handL: dance > 0 ? mix2([nx - 80, gy - 290], [nx - 170 - sw * 20, gy - 600], dance) : [nx - 80, gy - 290], handR: dance > 0 ? mix2([nx + 80, gy - 290], [nx + 170 + sw * 20, gy - 600], dance) : [nx + 80, gy - 290],
      brow: t < 4.0 ? -.9 : 0, mouth: t < 4.0 ? -.9 : .9, happy: dance > .5, mouthOpen: dance > .5 ? .7 : 0, wide: t > 3.6 && t < 4.4, blink: blinkAmt(t, [2.4]) });
  } });
} },
/* N17: group photo. Every photo looked like this */
{ id: 'N17', dur: 6.6, draw(t) {
  if (t < 2.5) {
    party(t + 6.0, 'suit', { shots: [{ a: 0, b: 99, cx: 960, cy: 560, z: 1.02, dz: .03 }] });
    if (t > .9) { const n = 3 - Math.floor((t - .9) / .5); if (n > 0) textPop(String(n), 560, 260, 170, '#fde047', .9 + (3 - n) * .5, t, 14); }
    const f = bump(t, 2.3, 2.7); if (f > 0) { X.setTransform(1, 0, 0, 1, 0, 0); X.fillStyle = `rgba(255,255,255,${f})`; X.fillRect(0, 0, W, H); }
  } else {
    X.setTransform(1, 0, 0, 1, 0, 0); X.fillStyle = '#2c1f30'; X.fillRect(0, 0, W, H); vignette(X, .5);
    const k = back(clamp((t - 2.5) / .45)); X.save(); X.translate(960, 560); X.rotate(-.06 + .02 * Math.sin(t)); X.scale(.8 + .2 * k, .8 + .2 * k);
    fillR(X, -520, -440, 1040, 900, 10, '#fbf8f2', 6);
    X.save(); X.beginPath(); X.rect(-470, -390, 940, 700); X.clip();
    X.fillStyle = '#efe9ee'; X.fillRect(-470, -390, 940, 700);
    X.globalAlpha = .18; for (const [x, y] of [[-380, -40], [-230, -60], [-60, -120], [120, -50], [290, -40]]) { shape(X, g => g.arc(x, y, 70, 0, 7), '#8a8296', 4); shape(X, g => rrPath(g, x - 80, y + 70, 160, 300, 30), '#8a8296', 4); }
    X.globalAlpha = 1; const gr = X.createRadialGradient(330, 60, 10, 330, 60, 700); gr.addColorStop(0, '#ffffff'); gr.addColorStop(.35, 'rgba(255,255,255,.95)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); X.fillStyle = gr; X.fillRect(-470, -390, 940, 700);
    X.restore(); X.strokeStyle = OUT; X.lineWidth = 4; X.strokeRect(-470, -390, 940, 700);
    text("DAVE'S BIRTHDAY", 0, 400, 64, '#2c3d6e', 'center', 'Bangers', 0); X.restore();
  }
  letterbox();
} },
/* N9: Dave opens the present he wrapped himself. It is tape */
{ id: 'N9', dur: 6.6, draw(t) {
  const open = R(t, 1.0, 1.8), lift = R(t, 2.2, 2.7);
  party(t + 6.0, 'suit', { shots: [{ a: 0, b: 99, cx: 960, cy: 470, z: 1.55, dz: .04 }],
    daveP: { noMug: 1, lid: .35, look: [2, 10], handR: lift > 0 ? [1000, mix(700, 540, lift)] : [930 + Math.sin(t * 20) * 30 * (open > 0 && open < 1), 700] },
    extra: tt => {
      present(t, 860, 760, 1 - open, 0);
      if (open > 0) { X.save(); X.globalAlpha = 1 - R(t, 1.6, 2.0); for (let i = 0; i < 6; i++) { const a = i * 1.05, d = open * 160; shape(X, g => g.ellipse(860 + Math.cos(a) * d, 680 + Math.sin(a) * d * .5 - open * 60, 34, 16, a, 0, 7), '#8a6fd1', 3); } X.restore(); }
      if (lift > 0) { const [x, y] = DAVEH; shape(X, g => g.arc(x + 4, y - 44, 40, 0, 7), '#c9c4b8'); shape(X, g => g.arc(x + 4, y - 44, 16, 0, 7), '#4a3d4c', 4); sparkle(x + 60, y - 100, .7, bump(t, 2.6, 3.2)); }
    } });
} },
/* N19: midnight. Dave asleep on the sofa; you are his night light */
{ id: 'N19', dur: 7.6, draw(t) {
  camera(t, [{ a: 0, b: 99, cx: 560, cy: 640, z: 1.35, dz: .06 }]);
  X.drawImage(BGS.living, 0, 0); windowCracks(1, LWIN);
  cake(t, 960, 760, -1);
  // Dave lying on the sofa under a blanket, head on the armrest
  head(150, 640, 96, -1.15, { beard: 1, glasses: 1, blink: 1, partyHat: 0, t });
  shape(X, g => { g.moveTo(200, 700); g.quadraticCurveTo(300, 600, 560, 640); g.lineTo(600, 760); g.lineTo(200, 770); g.closePath(); }, '#2c3d6e');
  shape(X, g => g.ellipse(560, 700, 30, 50, .3, 0, 7), '#25233c', 4);
  for (let i = 0; i < 3; i++) { const u = ((t * .5 + i / 3) % 1); X.save(); X.globalAlpha = Math.sin(u * Math.PI); text('z', 240 + u * 90 + i * 16, 520 - u * 180, 50 + i * 12, '#e8e1ec', 'center', 'Bangers', 6); X.restore(); }
  const gx = 860, gy = 944, ht = TOP(gy);
  person(t, gx, gy, HERO, { armor: ARMOR_ON, look: [-22, 10], happy: t > 3.6, mouth: .5, chestGlow: .6 + .1 * Math.sin(t * 2), blink: blinkAmt(t, [2.0, 5.8]) });
  darkness(.84, [lightAt(gx, ht + 96, 430, 1), lightAt(200, 650, 260, .55)]);
  glow(gx, ht + 96, 600, .16, '110,190,255');
  letterbox();
} },
);
/* final running order */
const ORDER = ['T0', '01', '02', 'N1', '03', '04', '05', 'N2', '05b', 'N12', 'NB', '05c', 'N10', 'N20', '06', 'N3', 'B', 'N23', 'N4', 'N13', '06c', '07', 'NW', 'NE', 'N7', '08', '09', '10', '11', '12', '12b', 'N8', 'NK', 'N17', 'NX', 'N9', '13', 'N19', '14'];
window.ORDER = ORDER;
const _init05 = window.init;
window.init = id => {
  BGS.hall = bgHall(); BGS.bedNB = blurOf(bgBedroom(true), 8); BGS.store = bgStore(); BGS.cafe = bgCafe(); BGS.sky = bgSky();
  SKYL.far = skyLayer(41, [['#b7c3da', 140, 300, 30]], 900, 0); SKYL.near = skyLayer(43, [['#8f7aa8', 200, 420, 60], ['#6a8fb0', 260, 520, 90]], 1080, .1);
  return _init05(id);
};

const GLAZIER = { col: '#e8822f', colD: '#c26a22', hair: 'cap', hairCol: '#2f6fb5', ph: 3.0 };
function foam(x, y, r, a = 1) { if (a <= 0) return; X.save(); X.globalAlpha = a; for (const [dx, dy, rr] of [[0, 0, 1], [.8, .3, .7], [-.7, .4, .8], [.2, -.6, .6], [-.3, .9, .5]]) shape(X, g => g.arc(x + dx * r, y + dy * r, rr * r * .6, 0, 7), '#ffffff', 3); X.restore(); }
function glassPane(x, y, w, h) { X.save(); X.globalAlpha = .75; fillR(X, x - w / 2, y - h / 2, w, h, 6, '#cfe8f7', 5); X.globalAlpha = .6; X.strokeStyle = '#ffffff'; X.lineWidth = 10; X.beginPath(); X.moveTo(x - w * .3, y - h * .35); X.lineTo(x - w * .05, y - h * .45); X.moveTo(x - w * .32, y - h * .15); X.lineTo(x + w * .1, y - h * .4); X.stroke(); X.restore(); }
function micro(x, y) { shape(X, g => rrPath(g, x - 9, y - 10, 18, 70, 8), '#2a2333', 3); shape(X, g => g.arc(x, y - 22, 20, 0, 7), '#9a95a6', 4); X.strokeStyle = 'rgba(0,0,0,.3)'; X.lineWidth = 2; for (let i = -1; i <= 1; i++) { X.beginPath(); X.moveTo(x - 16, y - 22 + i * 7); X.lineTo(x + 16, y - 22 + i * 7); X.stroke(); } }

SCENES.push(
/* T0: title card */
{ id: 'T0', dur: 4.0, draw(t) {
  X.setTransform(1, 0, 0, 1, 0, 0); X.drawImage(BGS.bedNB, 0, 0); X.fillStyle = 'rgba(10,8,30,.55)'; X.fillRect(0, 0, W, H);
  glow(960, 760, 420 + 30 * Math.sin(t * 2.2), .35, '120,200,255');
  const z = 1 + .03 * t; X.setTransform(z, 0, 0, z, W / 2 * (1 - z), H / 2 * (1 - z));
  textPop('WHAT IF YOU WOKE UP AS', 960, 400, 96, '#f4f1e0', .3, t, 12);
  X.save(); X.translate(960, 600); const k = pop(t, .9, 1); X.scale(k, k); X.rotate(-.03);
  text('IRON MAN?', 0, 0, 260, '#e8382f', 'center', 'Bangers', 22); X.restore();
  if (t > 3.4) { X.setTransform(1, 0, 0, 1, 0, 0); X.fillStyle = `rgba(0,0,0,${R(t, 3.4, 4.0)})`; X.fillRect(0, 0, W, H); }
  letterbox();
} },
/* NB: brushing teeth in oven mitts: a foam beard, just like Dave's */
{ id: 'NB', dur: 6.4, draw(t) {
  camera(t, [{ a: 0, b: 99, cx: 1250, cy: 500, z: 1.45, dz: .05 }]);
  X.drawImage(BGS.hall, 0, 0); hallDoor(0);
  const gx = 1180, gy = 944, ht = TOP(gy), sc = t > .4 && t < 4.6 ? Math.sin(t * 17) : 0, hy = ht - 66;
  // foam grows into a beard and splatters the mirror
  const fb = R(t, .8, 4.0);
  person(t, gx, gy, HERO, { mitts: 1, handR: t < 4.8 ? [gx + 70 + sc * 34, hy + 30] : [gx + 112, gy - 212], handL: [gx - 112, gy - 212], look: [0, 4], brow: .6, mouth: .3, wide: t > 4.8, blink: blinkAmt(t, [2.8]) });
  if (t < 4.8 && HERO._hr) { const [x, y] = HERO._hr; X.save(); X.translate(x, y); X.rotate(Math.PI * 1.05); fillR(X, -6, -10, 12, 120, 6, '#3fb6e8', 3); fillR(X, -10, 104, 20, 30, 4, '#ffffff', 3); X.restore(); }
  if (fb > 0) { const r = rng(5); for (let i = 0; i < 14; i++) { const a = Math.PI * (.05 + .9 * (i / 13)), d = 70 + r() * 18; if (i / 14 < fb) foam(gx + Math.cos(a) * d * 1.05, ht - 100 + 40 + Math.sin(a) * d * .9, 26 + r() * 10); } }
  for (let i = 0; i < 6; i++) { const t0 = 1 + i * .5; if (t > t0) { const u = Math.min(1, (t - t0) / .25); foam(mix(gx + 90, 1390 + (i * 37) % 110, u), mix(hy, 300 + (i * 53) % 160, u), 14); } }
  letterbox();
} },
/* NW: Dave called the window guy. They are on a first-name basis */
{ id: 'NW', dur: 8.0, draw(t) {
  camera(t, [{ a: 0, b: 99, cx: 960, cy: 560, z: 1.1, dz: .04 }]);
  X.drawImage(BGS.hall, 0, 0); const open = R(t, .3, .8); hallDoor(open);
  const gy = 944, dg = 560, wx = t < 2.2 ? mix(930, 1120, io((t - .8) / 1.4)) : 1120, walking = t > .8 && t < 2.2, five = bump(t, 3.0, 3.8);
  dave(t, dg, gy, { noMug: 1, handR: five > 0 ? [dg + 220, 520] : undefined, happy: t > 2.8, look: [16, 0], blink: blinkAmt(t, [5.2]) });
  if (t > .5) { person(t, wx, gy, GLAZIER, { walk: walking ? t * 9 : undefined, handL: five > 0 ? [dg + 260, 520] : [wx - 100, 600], handR: [wx + 100, 600], happy: t > 2.6, mouth: .8, look: [-14, 0], blink: blinkAmt(t, [4.4]) });
    X.save(); fillR(X, wx - 50, 680, 100, 40, 8, '#fdf6d8', 3); text('RICK', wx, 712, 30, '#2c201d', 'center', 'Bangers', 0); X.restore();
    if (five < .2) glassPane(wx, 600, 260, 300); else glassPane(1500, 760, 260, 300); }
  if (five > .6) burst('HI RICK!', 900, 300, .55, bump(t, 3.2, 4.0), -.08, '#fde047');
  person(t, 1560, gy, HERO, { pockets: 1, look: [-18, 0], wavy: 1, sweat: .4, blink: blinkAmt(t, [1.4, 6.0]) });
  letterbox();
} },
/* NE: practising in the mirror before the party */
{ id: 'NE', dur: 8.6, draw(t) {
  camera(t, [{ a: 0, b: 99, cx: 1250, cy: 540, z: 1.35, dz: .04 }]);
  X.drawImage(BGS.hall, 0, 0); hallDoor(0);
  const gx = 1180, gy = 944, ht = TOP(gy), pose = t < 2.4 ? 0 : t < 3.9 ? 1 : t < 5.5 ? 2 : 3;
  const sit = pose === 3 ? R(t, 5.5, 5.8) : 0, gyy = gy + sit * 150;
  if (pose === 3) { fillR(X, gx - 150, gy - 200, 300, 40, 8, '#8a5a3c'); }
  person(t, gx, gyy, HERO, { pockets: pose === 1, behind: pose === 2, handL: pose === 3 ? [gx - 80, gyy - 200] : (pose === 0 ? [gx - 112, gy - 212] : undefined), handR: pose === 2 ? [gx + 40, gy - 240] : (pose === 3 ? [gx + 80, gyy - 200] : (pose === 0 ? [gx + 112, gy - 212] : undefined)),
    look: [0, 2], brow: pose === 0 ? 0 : .5, mouth: pose === 0 ? .3 : .7, happy: pose > 0 && t % 1.6 < .8, blink: blinkAmt(t, [1.2, 7.6]), noShadow: pose === 3 });
  if (pose === 3) { shape(X, g => rrPath(g, gx - 160, gy - 180, 320, 200, 10), '#7a4f3a'); X.strokeStyle = 'rgba(0,0,0,.2)'; X.lineWidth = 6; X.strokeRect(gx - 130, gy - 150, 260, 140); }
  const tick = [2.4, 3.9, 5.5].map(a => bump(t, a, a + .4)); tick.forEach((k, i) => { if (k > 0) sparkle(gx + 160, ht - 40 + i * 20, .8, k); });
  letterbox();
} },
/* NX: Dave's speech. It was short */
{ id: 'NX', dur: 5.6, draw(t) {
  party(t + 6.0, 'suit', { shots: [{ a: 0, b: 99, cx: 980, cy: 470, z: 1.5, dz: .04 }], daveP: { lift: R(t, 1.4, 1.8) * .5 * (1 - R(t, 4.4, 4.8)) + R(t, 3.6, 4.0) * .5 * (1 - R(t, 4.4, 4.8)), look: [0, 0], lid: .3, steam: 0 },
    extra: tt => { const a = R(t, 1.6, 1.9) * (1 - R(t, 3.4, 3.7)); if (a > 0) { X.save(); X.globalAlpha = a; shape(X, g => { g.ellipse(1250, 230, 170, 80, 0, 0, 7); }, '#ffffff'); shape(X, g => { g.moveTo(1120, 280); g.lineTo(1060, 330); g.lineTo(1160, 295); g.closePath(); }, '#ffffff', 0); text('THANKS.', 1250, 255, 76, '#141014', 'center', 'Bangers', 0); X.restore(); } } });
} },
/* NK: then Dave sang. Dave is very good */
{ id: 'NK', dur: 7.4, draw(t) {
  party(t + 6.0, 'suit', { shots: [{ a: 0, b: 99, cx: 980, cy: 470, z: 1.42, dz: .06 }], daveP: { noMug: 1, handR: [1030, 420], blowO: .45 + .55 * Math.abs(Math.sin(t * 5.5)), blink: t > 1.2 ? .95 : 0, headRot: Math.sin(t * 2.2) * .06 },
    extra: tt => { if (DAVEH) micro(DAVEH[0] - 10, DAVEH[1] - 40); musicNotes(1150, 330, t, 1, 4); } });
} },
);
