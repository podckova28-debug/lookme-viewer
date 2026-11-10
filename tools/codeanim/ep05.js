/* Episode 5 (Iron Man, "don't snap"): scenes. Each scene: {id, dur, draw(t)}. Times are scene-local seconds. */
const scr = (x, y) => { const m = X.getTransform(); return [m.a * x + m.e, m.d * y + m.f, m.a]; };
const lightAt = (x, y, r, k = 1) => { const [sx, sy, z] = scr(x, y); return [sx, sy, r * z, k]; };
const TOP = gy => gy - 460;
const GUEST1 = { col: '#4fae7a', colD: '#2f8a5a', hair: 'cap', hairCol: '#2f6fb5', ph: 1.1 };
const GUEST2 = { col: '#e86fb4', colD: '#c24f93', hair: 'bun', hairCol: '#5a3324', sc: .94, ph: 2.3 };
const BAKER = { col: '#f4f1ea', colD: '#d8d0c4', hair: 'chef', ph: 3.3 };
const SUIT = { col: '#c4302b', colD: '#9d2420', hair: null, ph: 5, sc: .5 };
const GUEST3 = { col: '#8a6fd1', colD: '#6a52ad', hair: 'band', hairCol: '#e8b64a', sc: 1.04, ph: .4 };

function partyTable(t, lit) {
  shape(X, q => { q.moveTo(760, 760); q.lineTo(1160, 760); q.lineTo(1190, 944); q.lineTo(730, 944); q.closePath(); }, '#e8e1ec', 4);
  X.strokeStyle = 'rgba(0,0,0,.08)'; X.lineWidth = 8; for (let x = 780; x < 1180; x += 50) { X.beginPath(); X.moveTo(x, 770); X.lineTo(x - 10, 940); X.stroke(); }
  cake(t, 960, 760, lit); cakeTape(960, 760, 2 / 3, 18);
}
function speaker(x, y, on, t) {
  fillR(X, x - 60, y - 170, 120, 170, 12, '#2f2a3a'); for (const [yy, r] of [[-120, 30], [-50, 40]]) { const k = on ? 1 + Math.sin(t * 25) * .06 : 1; shape(X, g => g.arc(x, y + yy, r * k, 0, 7), '#4a4458', 4); shape(X, g => g.arc(x, y + yy, r * .35, 0, 7), '#1b1320', 3); }
}
function card(t, bg, fn) {
  X.setTransform(1, 0, 0, 1, 0, 0); X.fillStyle = bg; X.fillRect(0, 0, W, H);
  X.fillStyle = 'rgba(0,0,0,.07)'; for (let y = 0; y < H; y += 26) for (let x = (y / 26 % 2) * 13; x < W; x += 26) { X.beginPath(); X.arc(x, y, 5, 0, 7); X.fill(); }
  const z = 1 + .03 * t / 6; X.setTransform(z, 0, 0, z, W / 2 * (1 - z), H / 2 * (1 - z)); fn();
}
function pop(t, a, s) { return back(clamp((t - a) / .35)) * s; }

const SCENES = [
/* 01: night, chest glows through the blanket like a night light; he wakes and looks at it */
{ id: '01', dur: 5.9, draw(t) {
  camera(t, [{ a: 0, b: 99, cx: 860, cy: 600, z: 1.12, dz: .1, dx: -60 }]);
  X.drawImage(BGS.bedN, 0, 0);
  const wake = R(t, 3.0, 3.4), lift = R(t, 3.6, 4.2);
  bedFront(t, 1, () => {
    head(535 + lift * 6, 668 - lift * 18, 82, -1.42 + lift * .28, { hair: 'curly', blink: 1 - wake, look: [mix(0, 10, lift), mix(0, 16, lift)], wide: lift > .5, mouth: .2 });
  });
  const pulse = .85 + .15 * Math.sin(t * 2.2), cx = 700, cy = 664;
  darkness(.82, [lightAt(cx, cy, 520 * pulse, 1), lightAt(cx, cy - 300, 380, .6)]);
  glow(cx, cy, 460 * pulse, .24, '120,200,255'); shape(X, g => g.arc(cx, cy, 20, 0, 7), 'rgba(220,250,255,.95)', 0); glow(cx, cy, 70, .9);
  letterbox();
} },
/* 02: morning, standing by the bed, covering the chest: the light leaks through his fingers */
{ id: '02', dur: 3.2, draw(t) {
  camera(t, [{ a: 0, b: 99, cx: 1430, cy: 560, z: 1.32, dz: .05 }]);
  X.drawImage(BGS.bedD, 0, 0); bedFront(t, 0);
  const gx = 1480, gy = 944, top = TOP(gy);
  person(t, gx, gy, HERO, { handL: [gx - 20, top + 100], handR: [gx + 22, top + 92], coverChest: .8 + .2 * Math.sin(t * 3), wavy: 1, look: [0, 14], brow: .7, blink: blinkAmt(t, [1.6, 3.4]) });
  letterbox();
} },
/* 03: kitchen. He snaps ("I remember!"), the window bursts, the suit flies in and locks on; toast lands in Dave's mug; Dave sips */
{ id: '03', dur: 8.4, draw(t) {
  t = t < 5.4 ? t : t + 2.2;                          // the close-up starts right after the line
  const s = camera(t, [{ a: 0, b: 7.6, cx: 980, cy: 560, z: 1.06, dz: .03, shake: t => bump(t, 1.6, 2.1) * 10 }, { a: 7.6, b: 99, cx: 640, cy: 420, z: 1.6, dz: .05, blur: 1 }]);
  X.drawImage(s.blur ? BGS.kitchenB : BGS.kitchen, 0, 0);
  windowCracks(R(t, 1.55, 1.7));
  const dgx = 560, dgy = 944, hgx = 1300, hgy = 944, ht = TOP(hgy);
  const toastIn = t > 2.6;
  dave(t, dgx, dgy, { blink: blinkAmt(t, [1.0, 4.5, 6.2, 9.9]) || (t > 8.9 && t < 9.6 ? 1 : 0), lift: R(t, 8.4, 8.9) * (1 - R(t, 9.7, 10.2)), toastInMug: toastIn, splash: t - 2.6, steam: toastIn ? 0 : 1 });
  if (!s.blur) {
    const A = armorState(t, 1.7), full = A.helmet;
    const think = R(t, .2, .6) * (1 - R(t, .95, 1.05)), snap = R(t, .95, 1.05) * (1 - R(t, 1.5, 1.9));
    const rest = [hgx + 112, hgy - 212], thinkP = [hgx + 150, ht - 5], raiseP = [hgx + 190, ht - 60];
    const handR = t < .95 ? mix2(rest, thinkP, R(t, .2, .6)) : t < 1.5 ? mix2(thinkP, raiseP, R(t, .95, 1.05)) : mix2(raiseP, rest, R(t, 1.5, 1.9));
    const looking = R(t, 3.3, 3.8);
    person(t, hgx, hgy, HERO, { armor: A, handR: looking > 0 ? mix2(handR, [hgx + 150, ht + 40], looking) : handR, snapR: (snap > .5 || (t > .4 && t < 1.5)) ? bump(t, 1.1, 1.35) : undefined,
      wide: t > 1.55 && t < 3.3, mouthO: t > 1.6 && t < 3.0, mouth: t < 1.0 ? .6 : (looking > 0 ? .9 : 0), happy: t < .9 && think > .5, chestGlow: full ? .2 + .15 * Math.sin(t * 3) : 0,
      look: looking > 0 ? [18, 14] : (t > 1.6 && t < 3 ? [-10, -8] : [0, 0]), blink: blinkAmt(t, [4.6, 6.6]), headRot: think * .08 });
    armorFlights(t, 1.7, [1650, 330], hgx, hgy); clankFlash(t, 1.7, hgx, hgy);
    shards(t, 1.6, [1600, 360]);
    // toast pops out of the toaster and arcs into Dave's mug
    if (t > 1.75 && t < 2.6) { const u = R(t, 1.75, 2.6, x => x), x = mix(955, dgx + 30, u), y = mix(530, 534, u) - Math.sin(u * Math.PI) * 330;
      toastSlice(x, y, u * 9, .95); }
    burst('SNAP!', hgx + 260, ht - 120, .7, bump(t, 1.1, 1.6), .15);
    burst('CRASH!', 1560, 230, .9, bump(t, 1.6, 2.3), -.12);
  }
  letterbox();
} },
/* 04: rule card */
{ id: '04', dur: 4.7, draw(t) {
  card(t, '#fde047', () => {
    X.save(); X.translate(960, 300); X.scale(pop(t, .3, 1), pop(t, .3, 1)); text("TODAY: DAVE'S BIRTHDAY", 0, 0, 92, '#e8382f', 'center', 'Bangers', 12); X.restore();
    X.save(); X.translate(960, 390); X.scale(pop(t, 2.0, 1), pop(t, 2.0, 1)); text('RULE #1', 0, 0, 80, '#141014', 'center'); X.restore();
    X.save(); X.translate(960, 600); X.scale(pop(t, 2.9, 1), pop(t, 2.9, 1)); text("DON'T SNAP.", 0, 0, 210, '#141014', 'center', 'Bangers', 0); X.restore();
    const a = R(t, 3.4, 3.75); if (a > 0) { X.save(); X.globalAlpha = a; X.translate(960, 830); X.scale(1.5, 1.5);
      shape(X, g => rrPath(g, -10, -70, 20, 60, 10), '#f1ece6', 4); shape(X, g => g.arc(0, 0, 40, 0, 7), '#f1ece6');
      X.strokeStyle = '#e8382f'; X.lineWidth = 16; X.beginPath(); X.arc(0, -20, 90, 0, 7); X.stroke(); X.beginPath(); X.moveTo(-64, -84); X.lineTo(64, 44); X.stroke(); X.restore(); }
  });
  letterbox();
} },
/* 05: Dave tapes the broken window; the suit lies in a pile at the hero's feet */
{ id: '05', dur: 3.6, draw(t) {
  camera(t, [{ a: 0, b: 99, cx: 1180, cy: 560, z: 1.08, dz: .03 }]);
  X.drawImage(BGS.kitchen, 0, 0); windowCracks(1); const u = R(t, .3, 3.4, x => x); windowTape(u);
  const { x, y, w, h } = KWIN, cx = x + w * .62, cy = y + h * .55, strips = [[-150, -90, 150, 90], [-150, 90, 150, -90], [-170, 0, 170, 0]];
  const i = Math.min(2, Math.floor(u * 3)), v = clamp(u * 3 - i), st = strips[i], hand = [cx + mix(st[0], st[2], v), cy + mix(st[1], st[3], v)];
  dave(t, 1260, 944, { exact: 1, noMug: 1, handR: hand, handL: [1110, 640], tapeRoll: 1, look: [16, -12], blink: blinkAmt(t, [2.2]) });
  const gx = 640;
  for (const [k, px, py, rot] of [['chest', gx - 130, 900, -.3], ['legL', gx + 150, 920, 1.4], ['helmet', gx + 40, 905, .2], ['armL', gx - 220, 925, 1.2]]) pieceSprite(k, px, py, rot, .5);
  person(t, gx, 944, HERO, { wavy: 1, look: [20, -6], brow: .4, handL: [gx - 60, TOP(944) - 30], blink: blinkAmt(t, [1.2]) });
  caption('WINDOWS: 1', R(t, .3, .55) * (1 - R(t, 3.4, 3.7)));
  letterbox();
} },
/* 05b: Dave's solution: oven mitts. The hero tries to snap in them: nothing */
{ id: '05b', dur: 6.6, draw(t) {
  const s = camera(t, [{ a: 0, b: 2.4, cx: 960, cy: 560, z: 1.12, dz: .03 }, { a: 2.4, b: 99, cx: 1366, cy: 470, z: 1.75, dz: .05 }]);
  X.drawImage(BGS.kitchen, 0, 0); windowCracks(1); windowTape(1);
  const gx = 1250, gy = 944, ht = TOP(gy), dg = 700;
  const give = R(t, .4, 1.0) * (1 - R(t, 1.7, 2.1)), take = R(t, 1.1, 1.6), on = t > 1.75;
  dave(t, dg, gy, { noMug: 1, handR: mix2([dg + 110, gy - 240], [dg + 300, gy - 330], give), look: [14, 0], blink: blinkAmt(t, [3.0, 6.2]) });
  if (!on && give > .05) { ovenMitt(DAVEH[0] + 14, DAVEH[1] - 18, 1.0, -1.2, 1); ovenMitt(DAVEH[0] + 34, DAVEH[1] - 4, 1.0, -1.5, 1); }
  const tries = [[2.9, 3.5], [4.6, 5.2]], tr = Math.max(...tries.map(([a, b]) => bump(t, a, b)));
  const up = R(t, 2.5, 2.8) * (1 - R(t, 5.4, 5.7)), thumb = R(t, 5.8, 6.2);
  const hr = t < 1.75 ? mix2([gx + 112, gy - 212], [dg + 280, gy - 330], take * (1 - R(t, 1.6, 1.75))) :
    mix2(mix2([gx + 112, gy - 212], [gx + 160, ht + 10 + tr * 10], up), [gx + 150, ht + 60], thumb);
  person(t, gx, gy, HERO, { mitts: on ? 1 : 0, handR: hr, handL: on ? [gx - 70, gy - 260] : undefined, jitter: t > 4.4 && t < 5.3 ? 2.5 : 0,
    look: up > 0 ? [16, -10] : [-14, 0], brow: tr > .2 ? .7 : 0, mouth: thumb > .5 ? .9 : .2, happy: thumb > .6, wide: t > 3.5 && t < 4.4, blink: blinkAmt(t, [1.3, 7.0]) });
  if (on) { const k = bump(t, 1.75, 2.1); if (k > 0) sparkle(gx + 130, gy - 230, .8, k); }
  for (const [a, b] of tries) puff(gx + 190, ht - 60, bump(t, a + .1, b + .5), t > 4.4 ? 'PFF!' : 'pff');
  letterbox();
} },
/* 05c: the hero can't wrap the present in mitts; Dave wraps his own present */
{ id: '05c', dur: 6.6, draw(t) {
  camera(t, [{ a: 0, b: 99, cx: 900, cy: 520, z: 1.25, dz: .05 }]);
  X.drawImage(BGS.kitchen, 0, 0); windowCracks(1); windowTape(1);
  const gy = 944, hg = 1090, dg = 520, bx = 830, by = 604;
  const daveIn = R(t, 3.4, 3.8), wrap = R(t, 3.9, 4.6);
  const fumble = t < 3.4 ? 1 : 0, w1 = Math.sin(t * 9) * 26, w2 = Math.cos(t * 7) * 20;
  dave(t, dg, gy, { noMug: 1, handR: daveIn > 0 ? mix2([dg + 150, gy - 250], [bx - 40 + (wrap > 0 && wrap < 1 ? Math.sin(t * 40) * 40 : 0), by - 60 + (wrap > 0 && wrap < 1 ? Math.cos(t * 37) * 30 : 0)], daveIn * (1 - R(t, 5.0, 5.4))) : undefined,
    look: [daveIn > 0 ? 14 : 18, daveIn > 0 ? 8 : 0], lid: .35, blink: blinkAmt(t, [1.8, 6.0]) });
  present(t, bx, by, wrap);
  person(t, hg, gy, HERO, { mitts: 1, handL: fumble ? [bx + 40 + w1, by - 60 + w2 * .5] : [hg - 112, gy - 212], handR: fumble ? [bx + 110 - w2, by - 90 + w1 * .4] : [hg + 112, gy - 212],
    look: fumble ? [-20, 12] : [-22, 4], brow: fumble ? .8 : 0, sweat: fumble ? .7 : 0, wavy: !fumble, mouth: -.3, blink: blinkAmt(t, [5.2]) });
  if (fumble) { const tx = bx + 110 - w2, ty = by - 90 + w1 * .4; X.save(); X.lineCap = 'butt'; X.strokeStyle = OUT; X.lineWidth = 22; X.beginPath(); X.moveTo(tx + 10, ty - 30); X.quadraticCurveTo(tx + 40 + w1 * .5, ty + 10, tx + 20, ty + 60 + w2 * .3); X.stroke(); X.strokeStyle = '#c9c4b8'; X.lineWidth = 16; X.stroke(); X.restore(); }
  if (wrap > .95) sparkle(bx + 40, by - 150, .9, bump(t, 4.55, 5.2));
  letterbox();
} },
/* 06: bus stop. The phone ignores oven mitts; one mitt comes off; music; he snaps to the beat; the suit drops in; the bus leaves */
{ id: '06', dur: 10.0, draw(t) {
  camera(t, [{ a: 0, b: 99, cx: 1000, cy: 560, z: 1.05, dz: .04, shake: t => bump(t, 6.85, 7.2) * 9 }]);
  X.drawImage(BGS.street, 0, 0);
  const bx = t < 3.4 ? 1950 : t < 4.8 ? mix(1950, 260, outq((t - 3.4) / 1.4)) : t < 7.6 ? 260 : mix(260, -1100, R(t, 7.6, 9.2, x => x * x));
  bus(bx, t > 4.9 && t < 7.3);
  busStopFront();
  const gx = 800, gy = 944, ht = TOP(gy), A = armorState(t, 5.9);
  const music = t > 3.3 && t < 5.85, beat = music ? Math.abs(Math.sin((t - .2) * Math.PI * 2 + Math.PI / 2)) * 8 : 0;
  const tap = t < 2.8 ? Math.abs(Math.sin(t * 8)) : 0, off = R(t, 2.8, 3.1), tap2 = bump(t, 3.1, 3.35);
  const snapUp = R(t, 4.6, 4.9) * (1 - R(t, 5.85, 6.05));
  person(t, 1480, gy, GUEST2, { cup: 1, handL: [1480 - 60, gy - 330], look: t > 5.9 ? [-22, 0] : [0, 0], wide: t > 6.2, mouthO: t > 6.4, blink: blinkAmt(t, [1.0, 9.6]) });
  const hl = [gx - 10, gy - 290];
  const hr = snapUp > 0 ? mix2([gx + 112, gy - 212], [gx + 175, ht - 40], snapUp) : (t < 3.4 ? mix2([gx + 62, gy - 360 + tap * 16], [gx + 150, gy - 250], off * (1 - tap2)) : undefined);
  person(t, gx, gy, HERO, { armor: A, headphones: !A.helmet, mittL: !A.armL, mittR: t < 2.85, bounce: beat, happy: music, mouth: music ? .8 : (t > 8.8 ? -.8 : (t < 2.8 ? -.3 : 0)),
    headRot: music ? Math.sin((t - .2) * Math.PI * 2) * .05 : 0, handL: A.armL ? undefined : hl, handR: hr,
    snapR: snapUp > .5 ? Math.max(bump(t, 5.1, 5.3), bump(t, 5.6, 5.8)) : undefined,
    look: t > 7.6 ? [-24, 0] : (t < 3.4 ? [4, 16] : [0, 0]), brow: t < 2.8 ? .6 : 0, wide: t > 5.9 && t < 7.4, chestGlow: A.chest ? .2 : 0, blink: blinkAmt(t, [8.6, 10.2]) });
  if (!A.armL && HERO._hl) { ovenMitt(HERO._hl[0], HERO._hl[1], 1.0, -Math.PI / 2 - .2, 1); phone(HERO._hl[0] + 4, HERO._hl[1] - 66, t > 3.15, -.12); }
  if (off > 0) { const u = R(t, 2.85, 3.5, x => x); if (u < 1) ovenMitt(mix(gx + 150, gx + 330, u), gy - 250 - Math.sin(u * Math.PI) * 160 + u * 200, 1.0, u * 8, -1); else ovenMitt(gx + 330, gy - 40, 1.0, 1.4, -1); }
  if (music) musicNotes(gx + 120, ht - 120, t, 1 - R(t, 5.5, 5.85));
  armorFlights(t, 5.9, [gx + 300, -300], gx, gy); clankFlash(t, 5.9, gx, gy);
  burst('SNAP!', gx + 270, ht - 150, .6, Math.max(bump(t, 5.1, 5.45), bump(t, 5.6, 5.95)), .15);
  burst('CLANK!', gx - 260, ht - 60, .75, bump(t, 6.85, 7.5), -.1);
  letterbox();
} },
/* B: bakery. The empty suit waits outside. The box slips out of the mitts, he catches it bare-handed, snaps for joy: the suit comes through the window */
{ id: 'B', dur: 10.6, draw(t) {
  const s = camera(t, [{ a: 0, b: 6.3, cx: 960, cy: 560, z: 1.02, dz: .04, shake: t => bump(t, 7.15, 7.6) * 10 }, { a: 6.3, b: 8.4, cx: 960, cy: 560, z: 1.06, dz: .02, shake: t => bump(t, 7.15, 7.6) * 10 }, { a: 8.4, b: 99, cx: 1260, cy: 470, z: 1.4, dz: .05 }]);
  X.drawImage(BGS.bakery, 0, 0);
  const gx = 980, gy = 944, ht = TOP(gy), T0 = 7.25, A = armorState(t, T0);
  const launched = t > 7.1;
  if (!launched) person(t, 410, 622, SUIT, { armor: { legL: 1, legR: 1, chest: 1, armL: 1, armR: 1 }, faceplate: 1, eyes: Math.max(.15, bump(t, 6.95, 7.15)), still: 1, noShadow: 1, chestGlow: .1, blink: 0 });
  if (launched && t < 8.5) windowCracks(1, BWIN);
  if (t >= 8.5) { windowCracks(1, BWIN); }
  bakeryWindow(launched);
  // baker behind the counter
  person(t, 1520, gy, BAKER, { handL: t < 1.6 ? mix2([1520 - 112, gy - 212], [1250, 570], R(t, .3, 1.0)) : undefined, handR: t < 1.6 ? mix2([1520 + 112, gy - 212], [1330, 570], R(t, .3, 1.0)) : undefined,
    look: t > 7.2 ? [-24, -4] : [-18, 6], happy: t < 4.4, wide: t > 7.2 && t < 8.6, mouthO: t > 7.3 && t < 8.4, mouth: .6, lid: t > 8.6 ? .45 : 0, blink: blinkAmt(t, [2.6, 10.6]) });
  bakeryCounter();
  // the box: handed over, slips around in the mitts, flies up, caught bare-handed, then flattened by the chest plate
  let box = [1290, 560], rot = 0, sq = 0;
  if (t < 1.6) box = mix2([1290, 560], [1080, 600], R(t, .3, 1.5));
  else if (t < 4.6) { const w = R(t, 2.4, 4.6, x => x); box = [1080 + Math.sin(t * 7) * 40 * w, 600 + Math.abs(Math.sin(t * 6)) * -60 * w]; rot = Math.sin(t * 8) * .5 * w; }
  else if (t < 5.4) { const u = R(t, 4.6, 5.4, x => x); box = [mix(1080, 1060, u), 600 - Math.sin(u * Math.PI) * 300]; rot = u * 6.3; }
  else box = [1060, 610];
  if (t > T0 + .5) { sq = R(t, T0 + .5, T0 + .7); box = [1000, mix(610, 650, sq)]; }
  const mitts = t < 4.75, hold = t < 4.6 || t > 5.35;
  const hl = hold ? [box[0] - 70, box[1] + 10] : [gx - 150, ht + 40], hr = hold ? [box[0] + 70, box[1] + 10] : [gx + 160, ht + 40];
  const yes = R(t, 6.4, 6.7) * (1 - R(t, 7.6, 8.0));
  person(t, gx, gy, HERO, { armor: A, mitts, handL: hl, handR: yes > 0 ? mix2(hr, [gx + 170, ht - 50], yes) : hr, snapR: yes > .5 ? bump(t, 6.8, 7.0) : undefined,
    look: t < 4.6 ? [12, 10] : (t < 5.4 ? [10, -16] : [10, 6]), wide: t > 2.4 && t < 5.5, sweat: t > 2.6 && t < 5.4 ? .8 : 0, mouthO: t > 4.6 && t < 5.4,
    happy: t > 5.6 && t < 7.1, mouth: t > 8.6 ? -.9 : .5, brow: t > 8.6 ? -.5 : 0, chestGlow: A.chest ? .2 : 0, blink: blinkAmt(t, [1.2, 10.2]) });
  if (hold && HERO._hl && HERO._hr && sq === 0 && !(t > 4.55 && t < 5.45)) box = [(HERO._hl[0] + HERO._hr[0]) / 2, (HERO._hl[1] + HERO._hr[1]) / 2 - 12];
  cakeBox(box[0], box[1], rot, sq);
  if (t > 4.7 && t < 5.6) { const u = R(t, 4.7, 5.6, x => x); ovenMitt(mix(gx - 60, gx - 300, u), gy - 300 - Math.sin(u * Math.PI) * 200 + u * 260, 1.0, u * 7, 1); ovenMitt(mix(gx + 80, gx + 340, u), gy - 300 - Math.sin(u * Math.PI) * 240 + u * 260, 1.0, -u * 8, -1); }
  if (t >= 5.6) { ovenMitt(gx - 300, gy - 40, 1.0, -1.4, 1); ovenMitt(gx + 340, gy - 40, 1.0, 1.5, -1); }
  armorFlights(t, T0, [410, 470], gx, gy); clankFlash(t, T0, gx, gy); shards(t, 7.1, [450, 400], 22, 11);
  burst('SNAP!', gx + 250, ht - 140, .6, bump(t, 6.8, 7.3), .15);
  burst('CRASH!', 420, 260, .9, bump(t, 7.1, 7.8), -.1);
  if (sq > 0) burst('SQUISH', 1000, 470, .55, bump(t, T0 + .55, T0 + 1.1), .1, '#f7c6dc');
  caption('WINDOWS: 2', R(t, 8.4, 8.65));
  letterbox();
} },
/* 06c: home again. Dave fixes the cake with tape; the suit is a pile on the floor again */
{ id: '06c', dur: 4.6, draw(t) {
  camera(t, [{ a: 0, b: 99, cx: 900, cy: 580, z: 1.3, dz: .06 }]);
  X.drawImage(BGS.kitchen, 0, 0); windowCracks(1); windowTape(1);
  const gy = 944, dg = 520, hg = 1270, cx = 900, cy = 604;
  const u = R(t, .6, 3.6, x => x), lean = 1 - u;
  X.save(); X.translate(cx, cy); X.transform(1, 0, -.35 * lean, 1, 0, 0); X.scale(1 + .18 * lean, 1 - .3 * lean); X.translate(-cx, -cy); cake(t, cx, cy, -1); X.restore();
  cakeTape(cx, cy, u);
  const i = Math.min(2, Math.floor(u * 3)), v = clamp(u * 3 - i), st = [[-120, -40, 120, -120], [-120, -120, 120, -30], [-40, -128, 30, 0]][i];
  const hand = u > 0 && u < 1 ? [cx + mix(st[0], st[2], v), cy + mix(st[1], st[3], v)] : [dg + 150, gy - 250];
  dave(t, dg, gy, { exact: 1, noMug: 1, tapeRoll: 1, handR: hand, look: [16, 6], lid: .3, blink: blinkAmt(t, [4.3]), headRot: R(t, 4.0, 4.3) * (1 - R(t, 4.6, 4.9)) * .06 });
  for (const [k, px, py, rot] of [['chest', hg + 170, 905, -.3], ['helmet', hg + 280, 900, .3], ['legL', hg - 170, 925, 1.3]]) pieceSprite(k, px, py, rot, .5);
  person(t, hg, gy, HERO, { look: [-20, 4], brow: .5, wavy: 1, pockets: 1, sweat: .4, blink: blinkAmt(t, [2.2, 5.0]) });
  if (u >= 1) sparkle(cx + 60, cy - 200, .7, bump(t, 3.7, 4.3));
  letterbox();
} },
/* 07: counters card (7 snaps, 4 windows) with Dave and a stack of tape */
{ id: '07', dur: 5.3, draw(t) {
  card(t, '#4a3a52', () => {
    const n1 = Math.min(7, Math.floor(R(t, .9, 1.95, x => x) * 7.99)), n2 = Math.min(4, Math.floor(R(t, 2.3, 2.95, x => x) * 4.99));
    X.save(); X.translate(150, 230); X.scale(pop(t, .3, 1), pop(t, .3, 1)); X.translate(-150, -230); fillR(X, 150, 230, 820, 190, 18, '#fde047', 8); text('6:00 PM', 190, 210, 64, '#fde047', 'left', 'Bangers', 8); text(`SNAPS: ${n1}`, 200, 360, 130, '#141014'); X.restore();
    if (t > 2.15) { X.save(); X.translate(150, 470); X.scale(pop(t, 2.15, 1), pop(t, 2.15, 1)); X.translate(-150, -470); fillR(X, 150, 470, 820, 190, 18, '#fde047', 8); text(`WINDOWS: ${n2}`, 200, 600, 130, '#141014'); X.restore(); }
    X.save(); X.translate(1430, 990); X.scale(.85, .85); X.translate(-1430, -990); dave(t, 1430, 990, { noMug: 1, tapeRoll: 1, handR: [1580, 640], handL: [1300, 700], blink: blinkAmt(t, [2.8]) }); X.restore();
    for (let i = 0; i < 4; i++) if (t > 3.75 + i * .2) { const y = 600 - i * 52; shape(X, g => g.ellipse(1640, y, 60, 26, 0, 0, 7), '#c9c4b8'); shape(X, g => g.ellipse(1640, y, 24, 10, 0, 0, 7), '#4a3a52', 4); }
  });
  letterbox();
} },
/* 08: the party. Everyone is happy, he keeps his hands in his pockets */
{ id: '08', dur: 3.6, draw(t) { party(t, 'hands'); } },
/* 09: everybody starts snapping to the music; he sweats */
{ id: '09', dur: 4.6, draw(t) { party(t, 'snapping'); } },
/* 10: the power goes out */
{ id: '10', dur: 3.3, draw(t) { party(t, 'dark'); } },
/* 11: close-up in the dark: fine, one snap */
{ id: '11', dur: 3.4, draw(t) { party(t, 'onesnap'); } },
/* 12: the suit crashes in, his chest lights the room, the speaker plugs into it, everyone dances */
{ id: '12', dur: 5.6, draw(t) { party(t, 'suit'); } },
/* 12b: Dave danced. A little. */
{ id: '12b', dur: 4.2, draw(t) { party(t + 4.0, 'suit', { shots: [{ a: 0, b: 99, cx: 1000, cy: 485, z: 1.45, dz: .02 }], daveDance: t }); } },
/* 13: Dave's wish: new windows; he blows the candles out */
{ id: '13', dur: 6.2, draw(t) { party(t, 'wish'); } },
/* 14: next morning. New windows (Dave's wish). The hero stretches, snaps by accident: window number six. Dave sips */
{ id: '14', dur: 9.2, draw(t) {
  t = t + .6 * R(t, 2.6, 3.4, x => x);
  const s = camera(t, [{ a: 0, b: 7.0, cx: 980, cy: 560, z: 1.06, dz: .03, shake: t => bump(t, 4.5, 4.9) * 10 }, { a: 7.0, b: 99, cx: 640, cy: 420, z: 1.6, dz: .05, blur: 1 }]);
  X.drawImage(s.blur ? BGS.kitchenDayB : BGS.kitchenDay, 0, 0);
  const gx = 1300, gy = 944, ht = TOP(gy), T0 = 4.65, A = armorState(t, T0);
  if (t < 4.5) for (const [x, y, ph] of [[1250, 200, 0], [1700, 330, 1.3], [1480, 470, 2.4]]) sparkle(x, y, .8, .5 + .5 * Math.sin(t * 3 + ph));
  windowCracks(R(t, 4.5, 4.62));
  dave(t, 560, gy, { look: t < 4.5 ? [20, -10] : [16, 0], lid: t < 4.5 ? .1 : .3, happy: t < 4.4, lift: R(t, 7.6, 8.1) * (1 - R(t, 9.0, 9.5)), blink: blinkAmt(t, [2.4, 6.0]) || (t > 8.2 && t < 8.9 ? 1 : 0) });
  if (!s.blur) {
    const st = R(t, .9, 1.6) * (1 - R(t, 5.6, 6.2)), yawn = bump(t, 1.2, 3.2);
    person(t, gx, gy, HERO, { armor: A, handL: mix2([gx - 112, gy - 212], [gx - 135, ht - 115], st), handR: mix2([gx + 112, gy - 212], [gx + 145, ht - 125], st), snapR: st > .9 ? bump(t, 4.3, 4.5) : undefined,
      mouthOpen: yawn * 1.2, blink: yawn > .2 ? 1 : blinkAmt(t, [6.6]), inhale: yawn, wide: t > 4.5 && t < 6.0, mouthO: t > 4.6 && t < 5.8, mouth: t > 6.2 ? -.6 : .4, look: t > 6.0 ? [-20, 0] : [0, 0], chestGlow: A.chest ? .2 : 0 });
    armorFlights(t, T0, [1650, 330], gx, gy); clankFlash(t, T0, gx, gy); shards(t, 4.5, [1600, 360]);
    burst('SNAP!', gx + 230, ht - 230, .6, bump(t, 4.3, 4.8), .15);
    burst('CRASH!', 1560, 230, .9, bump(t, 4.5, 5.2), -.12);
  }
  caption('WINDOWS: 6', R(t, 6.2, 6.45));
  letterbox();
} },
];

function party(t, mode, opt = {}) {
  const gy = 944, hg = 1520, ht = TOP(gy);
  let shots;
  if (mode === 'snapping') shots = [{ a: 0, b: 2.8, cx: 960, cy: 560, z: 1.02, dz: .03 }, { a: 2.8, b: 99, cx: 1322, cy: 440, z: 1.62, dz: .05, blur: 1 }];
  else if (mode === 'onesnap') shots = [{ a: 0, b: 99, cx: 1322, cy: 440, z: 1.62, dz: .06, blur: 1 }];
  else if (mode === 'wish') shots = [{ a: 0, b: 99, cx: 1000, cy: 400, z: 1.42, dz: .05 }];
  else if (mode === 'suit') shots = [{ a: 0, b: 99, cx: 960, cy: 560, z: 1.0, dz: .03, shake: t => bump(t, .2, .6) * 9 }];
  else shots = [{ a: 0, b: 99, cx: 960, cy: 560, z: 1.02, dz: .03 }];
  if (opt.shots) shots = opt.shots;
  const s = camera(t, shots);
  X.drawImage(s.blur ? BGS.livingB : BGS.living, 0, 0);
  const dark = mode === 'dark' ? R(t, .3, .45) : (mode === 'onesnap' || mode === 'suit' || mode === 'wish') ? 1 : 0;
  const suitT0 = .4, A = mode === 'suit' ? armorState(t, suitT0) : (mode === 'wish' ? armorState(99, 0) : {});
  const lit = mode === 'wish' ? 1 - R(t, 3.6, 3.75) : 1;
  if (mode === 'suit' || mode === 'wish') windowCracks(mode === 'suit' ? R(t, .15, .3) : 1, LWIN);
  balloons(t, 250, 380);
  const music = mode === 'snapping' || (mode === 'suit' && t > 2.6) || mode === 'wish';
  const beatB = music ? Math.abs(Math.sin(t * Math.PI * 2)) * 10 : 0;
  const snapUp = mode === 'snapping' ? R(t, .5, .8) : 0;
  const dance = mode === 'suit' ? R(t, 2.6, 3.0) : 0;
  const sad = mode === 'dark' ? R(t, .6, 1.2) : (mode === 'onesnap' ? 1 : (mode === 'suit' ? 1 - R(t, 2.5, 2.9) : 0));
  // guests: snapping above their heads / dancing with arms up
  for (const [spec, gx, ph] of [[GUEST3, 300, 0], [GUEST1, 560, .25], [GUEST2, 1270, .5]]) {
    const top = TOP(gy) * 1, up = Math.max(snapUp, dance), sw = Math.sin(t * Math.PI * 2 + ph * 6);
    const hand = up > 0 ? mix2([gx + 112, gy - 212], [gx + 150 + sw * 20, top - 90], up) : undefined;
    person(t, gx, gy, spec, { bounce: beatB * (up > 0 || dance > 0 ? 1 : 0) * (.6 + ph), handR: hand, handL: dance > 0 ? mix2([gx - 112, gy - 212], [gx - 150 - sw * 20, top - 90], dance) : undefined,
      snapR: snapUp > .5 ? bump((t + .5 - .18 - ph * .04) % .5, .0, .14) : undefined, happy: (mode === 'hands' || mode === 'snapping' || dance > .5 || mode === 'wish') && sad < .5,
      mouth: sad > 0 ? -.9 * sad : .7, mouthOpen: dance > .5 ? .8 : 0, blink: blinkAmt(t, [1.1 + ph * 3, 3.9 + ph]), look: [mode === 'wish' ? 10 : 0, 0] });
  }
  // Dave behind the table, party hat
  const dg = 960;
  const wishEyes = mode === 'wish' && t > .4 && t < 3.2;
  const dd = opt.daveDance, dk = dd === undefined ? 0 : R(dd, .5, 1.0);
  dave(t, dg, gy - 30, { bounce: dk * Math.abs(Math.sin(t * Math.PI * 2)) * 6, headRot: dk * Math.sin(t * Math.PI * 2) * .07, partyHat: 1, blink: wishEyes ? 1 : blinkAmt(t, [2.2, 4.4]), blowO: mode === 'wish' ? bump(t, 3.3, 3.9) : 0, lift: mode === 'wish' ? R(t, 5.0, 5.4) * (1 - R(t, 5.85, 6.2)) : 0, steam: 1,
    happy: (mode === 'wish' && t > 3.9 && t < 4.9) || (dd !== undefined && dd > 3.2), look: mode === 'hands' ? [14, 0] : [5, 0],
    ...(dd !== undefined ? { lift: R(dd, 2.6, 3.0) * (1 - R(dd, 4.0, 4.4)) * .45, steam: 0 } : {}) });
  partyTable(t, lit);
  // the hero on the right
  const pockets = mode === 'hands' || mode === 'snapping' || (mode === 'dark') || (mode === 'onesnap' && t < 1.0);
  const out = mode === 'onesnap' ? R(t, 1.0, 1.5) : 0, raise = mode === 'onesnap' ? R(t, 1.6, 2.2) : 0;
  const hr = mode === 'onesnap' && out > 0 ? mix2([hg + 38, gy - 250], mix2([hg + 70, ht + 40], [hg + 160, ht - 50], raise), out) : undefined;
  person(t, hg, gy, HERO, { armor: A, pockets: pockets && !hr, handR: hr, snapR: mode === 'onesnap' && raise > .9 ? bump(t, 2.6, 2.85) : undefined,
    jitter: mode === 'snapping' ? 3 + 3 * R(t, 1.5, 3.5) : 0, sweat: mode === 'snapping' ? R(t, 1.0, 1.6) : (mode === 'hands' ? .6 : 0),
    wavy: mode === 'hands' || mode === 'snapping', wide: mode === 'snapping' && t > 1.5, brow: mode === 'onesnap' ? -.8 : (mode === 'snapping' ? .6 : 0),
    look: mode === 'onesnap' ? [raise * 16, -raise * 14] : (mode === 'snapping' ? [-18, 0] : [0, 0]), mouth: mode === 'onesnap' ? -.2 : (dance > .5 ? .9 : .3),
    happy: mode === 'wish', chestGlow: A.chest ? .45 : 0, bounce: dance * beatB, blink: blinkAmt(t, [.9, 3.2]) });
  if (mode === 'suit') { armorFlights(t, suitT0, [LWIN.x + 200, LWIN.y + 150], hg, gy); clankFlash(t, suitT0, hg, gy); shards(t, .2, [LWIN.x + 250, LWIN.y + 200], 16, 7); }
  if (mode === 'suit' || mode === 'wish') { const on = mode === 'wish' || t > 2.4; speaker(hg + 260, gy, on, t);
    X.strokeStyle = OUT; X.lineWidth = 8; X.beginPath(); X.moveTo(hg + 260, gy - 90); X.quadraticCurveTo(hg + 200, gy - 20, hg + 30, TOP(gy) + 110); X.stroke(); X.strokeStyle = '#3b3f52'; X.lineWidth = 4; X.stroke(); }
  if (music) musicNotes(mode === 'snapping' ? 700 : hg + 230, 420, t, 1);
  // light: lamp off in the dark; the chest becomes the light source
  const chestOn = mode === 'suit' ? R(t, 1.3, 1.9) : (mode === 'wish' ? 1 : 0);
  const lights = [lightAt(960, 600, 260 * lit, .9)];
  if (chestOn > 0) lights.push(lightAt(hg, TOP(gy) + 96, 1400 * chestOn, 1));
  if (mode === 'onesnap') lights.push(lightAt(hg, 600, 520, .55));
  darkness(dark * .86 * (1 - .15 * chestOn), lights);
  if (chestOn > 0) { glow(hg, TOP(gy) + 96, 900 * chestOn, .16, '110,190,255');
    if (mode === 'suit' && t > 2.6 || mode === 'wish') { X.save(); X.globalCompositeOperation = 'lighter'; X.globalAlpha = .13; X.fillStyle = '#9fe4ff';
      for (let i = 0; i < 6; i++) { const a = t * .9 + i * Math.PI / 3; X.beginPath(); X.moveTo(hg, TOP(gy) + 96); X.lineTo(hg + Math.cos(a - .07) * 2200, TOP(gy) + 96 + Math.sin(a - .07) * 2200); X.lineTo(hg + Math.cos(a + .07) * 2200, TOP(gy) + 96 + Math.sin(a + .07) * 2200); X.fill(); } X.restore(); } }
  if (mode === 'onesnap') burst('SNAP!', hg + 230, ht - 170, .85, bump(t, 2.6, 3.2), .12);
  if (mode === 'suit') burst('CRASH!', 1560, 250, .9, bump(t, .15, .8), -.12);
  if (mode === 'wish' && t > .5 && t < 3.4) {           // thought bubble: a brand-new window
    const a = R(t, .5, .8) * (1 - R(t, 3.1, 3.4)); X.save(); X.globalAlpha = a;
    for (const [x, y, r] of [[1085, 300, 14], [1125, 262, 22]]) shape(X, g => g.arc(x, y, r, 0, 7), '#fff');
    shape(X, g => g.ellipse(1300, 200, 190, 110, 0, 0, 7), '#fff'); fillR(X, 1220, 140, 160, 120, 6, '#bfe3ff', 6);
    X.strokeStyle = OUT; X.lineWidth = 6; X.beginPath(); X.moveTo(1300, 140); X.lineTo(1300, 260); X.moveTo(1220, 200); X.lineTo(1380, 200); X.stroke();
    text('✦', 1390, 160, 50, '#fde047', 'center', 'serif', 5); X.restore(); }
  if (mode === 'wish') { const f = bump(t, 3.4, 3.9); if (f > 0) { X.save(); X.globalAlpha = f * .7; X.strokeStyle = '#fff'; X.lineWidth = 6; for (let i = -1; i <= 1; i++) { X.beginPath(); X.moveTo(990, 560 + i * 20); X.lineTo(1000 + 40 * f, 600 + i * 30); X.stroke(); } X.restore(); } }
  letterbox();
}

/* ---------- page API ---------- */
let CUR = null;
window.init = id => {
  BGS.bedN = bgBedroom(true); BGS.bedD = bgBedroom(false); BGS.kitchen = bgKitchen(false); BGS.kitchenDay = bgKitchen(true); BGS.kitchenDayB = blurOf(BGS.kitchenDay); BGS.kitchenB = blurOf(BGS.kitchen);
  BGS.street = bgStreet(); BGS.bakery = bgBakery(); BGS.living = bgLiving(); BGS.livingB = blurOf(BGS.living);
  CUR = SCENES.find(s => s.id === id); return CUR.dur;
};
window.render = t => renderSoft(CUR.draw, t);
window.SCENES_META = SCENES.map(s => ({ id: s.id, dur: s.dur }));
