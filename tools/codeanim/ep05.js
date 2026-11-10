/* Episode 5 (Iron Man, "don't snap"): scenes. Each scene: {id, dur, draw(t)}. Times are scene-local seconds. */
const scr = (x, y) => { const m = X.getTransform(); return [m.a * x + m.e, m.d * y + m.f, m.a]; };
const lightAt = (x, y, r, k = 1) => { const [sx, sy, z] = scr(x, y); return [sx, sy, r * z, k]; };
const TOP = gy => gy - 460;
const GUEST1 = { col: '#4fae7a', colD: '#2f8a5a', hair: 'cap', hairCol: '#2f6fb5', ph: 1.1 };
const GUEST2 = { col: '#e86fb4', colD: '#c24f93', hair: 'bun', hairCol: '#5a3324', sc: .94, ph: 2.3 };
const GUEST3 = { col: '#8a6fd1', colD: '#6a52ad', hair: 'band', hairCol: '#e8b64a', sc: 1.04, ph: .4 };

function partyTable(t, lit) {
  shape(X, q => { q.moveTo(760, 760); q.lineTo(1160, 760); q.lineTo(1190, 944); q.lineTo(730, 944); q.closePath(); }, '#e8e1ec', 4);
  X.strokeStyle = 'rgba(0,0,0,.08)'; X.lineWidth = 8; for (let x = 780; x < 1180; x += 50) { X.beginPath(); X.moveTo(x, 770); X.lineTo(x - 10, 940); X.stroke(); }
  cake(t, 960, 760, lit);
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
{ id: '01', dur: 6.2, draw(t) {
  camera(t, [{ a: 0, b: 99, cx: 860, cy: 600, z: 1.12, dz: .1, dx: -60 }]);
  X.drawImage(BGS.bedN, 0, 0);
  const wake = R(t, 3.0, 3.4), lift = R(t, 3.6, 4.2);
  bedFront(t, 1, () => {
    head(535 + lift * 6, 668 - lift * 18, 82, -1.42 + lift * .28, { hair: 'curly', blink: 1 - wake, look: [mix(0, 10, lift), mix(0, 16, lift)], wide: lift > .5, mouth: .2 });
  });
  const pulse = .85 + .15 * Math.sin(t * 2.2), cx = 700, cy = 664;
  darkness(.82, [lightAt(cx, cy, 520 * pulse, 1), lightAt(cx, cy - 300, 380, .6)]);
  glow(cx, cy, 520 * pulse, .38, '120,200,255'); shape(X, g => g.arc(cx, cy, 20, 0, 7), 'rgba(220,250,255,.95)', 0); glow(cx, cy, 70, .9);
  letterbox();
} },
/* 02: morning, standing by the bed, covering the chest: the light leaks through his fingers */
{ id: '02', dur: 4.2, draw(t) {
  camera(t, [{ a: 0, b: 99, cx: 1430, cy: 560, z: 1.32, dz: .05 }]);
  X.drawImage(BGS.bedD, 0, 0); bedFront(t, 0);
  const gx = 1480, gy = 944, top = TOP(gy);
  person(t, gx, gy, HERO, { handL: [gx - 20, top + 100], handR: [gx + 22, top + 92], coverChest: .8 + .2 * Math.sin(t * 3), wavy: 1, look: [0, 14], brow: .7, blink: blinkAmt(t, [1.6, 3.4]) });
  letterbox();
} },
/* 03: kitchen. He snaps ("I remember!"), the window bursts, the suit flies in and locks on; toast lands in Dave's mug; Dave sips */
{ id: '03', dur: 10.6, draw(t) {
  const s = camera(t, [{ a: 0, b: 7.6, cx: 980, cy: 560, z: 1.06, dz: .03, shake: t => bump(t, 1.6, 2.1) * 10 }, { a: 7.6, b: 99, cx: 640, cy: 420, z: 1.6, dz: .05, blur: 1 }]);
  X.drawImage(s.blur ? BGS.kitchenB : BGS.kitchen, 0, 0);
  windowCracks(R(t, 1.55, 1.7));
  const dgx = 560, dgy = 944, hgx = 1300, hgy = 944, ht = TOP(hgy);
  const toastIn = t > 2.6;
  dave(t, dgx, dgy, { blink: blinkAmt(t, [1.0, 4.5, 6.2, 9.9]) || (t > 8.9 && t < 9.6 ? 1 : 0), lift: R(t, 8.4, 8.9) * (1 - R(t, 9.7, 10.2)), toastInMug: toastIn, steam: toastIn ? 0 : 1 });
  if (!s.blur) {
    const A = armorState(t, 1.7), full = A.helmet;
    const think = R(t, .2, .6) * (1 - R(t, .95, 1.05)), snap = R(t, .95, 1.05) * (1 - R(t, 1.5, 1.9));
    const handR = think > 0 && snap === 0 ? [hgx + 60, ht - 40] : mix2([hgx + 112, hgy - 212], [hgx + 190, ht - 60], snap);
    const looking = R(t, 3.3, 3.8);
    person(t, hgx, hgy, HERO, { armor: A, handR: looking > 0 ? mix2(handR, [hgx + 150, ht + 40], looking) : handR, snapR: snap > .5 ? bump(t, 1.1, 1.35) : undefined,
      wide: t > 1.55 && t < 3.3, mouthO: t > 1.6 && t < 3.0, mouth: t < 1.0 ? .6 : (looking > 0 ? .9 : 0), happy: t < .9 && think > .5, chestGlow: full ? .2 + .15 * Math.sin(t * 3) : 0,
      look: looking > 0 ? [18, 14] : (t > 1.6 && t < 3 ? [-10, -8] : [0, 0]), blink: blinkAmt(t, [4.6, 6.6]), headRot: think * .08 });
    armorFlights(t, 1.7, [1650, 330], hgx, hgy); clankFlash(t, 1.7, hgx, hgy);
    shards(t, 1.6, [1600, 360]);
    // toast pops out of the toaster and arcs into Dave's mug
    if (t > 1.75 && t < 2.6) { const u = R(t, 1.75, 2.6, x => x), x = mix(955, dgx + 30, u), y = mix(530, 534, u) - Math.sin(u * Math.PI) * 330;
      X.save(); X.translate(x, y); X.rotate(u * 9); shape(X, g => rrPath(g, -24, -26, 48, 52, 10), '#d9a35a', 4); X.restore(); }
    burst('SNAP!', hgx + 260, ht - 120, .7, bump(t, 1.1, 1.6), .15);
    burst('CRASH!', 1560, 230, .9, bump(t, 1.6, 2.3), -.12);
  }
  letterbox();
} },
/* 04: rule card */
{ id: '04', dur: 5.4, draw(t) {
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
{ id: '05', dur: 3.8, draw(t) {
  camera(t, [{ a: 0, b: 99, cx: 1180, cy: 560, z: 1.08, dz: .03 }]);
  X.drawImage(BGS.kitchen, 0, 0); windowCracks(1); const u = R(t, .3, 3.4, x => x); windowTape(u);
  const { x, y, w, h } = KWIN, cx = x + w * .62, cy = y + h * .55, strips = [[-150, -90, 150, 90], [-150, 90, 150, -90], [-170, 0, 170, 0]];
  const i = Math.min(2, Math.floor(u * 3)), v = clamp(u * 3 - i), st = strips[i], hand = [cx + mix(st[0], st[2], v), cy + mix(st[1], st[3], v)];
  dave(t, 1260, 944, { noMug: 1, handR: hand, handL: [1110, 640], tapeRoll: 1, look: [16, -12], blink: blinkAmt(t, [2.2]) });
  const gx = 640;
  for (const [k, px, py, rot] of [['chest', gx - 130, 900, -.3], ['legL', gx + 150, 920, 1.4], ['helmet', gx + 40, 905, .2], ['armL', gx - 220, 925, 1.2]]) pieceSprite(k, px, py, rot, .5);
  person(t, gx, 944, HERO, { wavy: 1, look: [20, -6], brow: .4, handL: [gx - 60, TOP(944) - 30], blink: blinkAmt(t, [1.2]) });
  caption('WINDOWS: 1', R(t, .3, .55) * (1 - R(t, 3.4, 3.7)));
  letterbox();
} },
/* 06: bus stop. Music in headphones, he snaps to the beat, the suit drops from the sky, the bus leaves without him */
{ id: '06', dur: 8.0, draw(t) {
  camera(t, [{ a: 0, b: 99, cx: 1000, cy: 560, z: 1.05, dz: .04, shake: t => bump(t, 3.85, 4.2) * 9 }]);
  X.drawImage(BGS.street, 0, 0);
  const bx = t < 1.6 ? mix(1950, 260, outq((t - .3) / 1.3)) : t < 5.0 ? 260 : mix(260, -1100, R(t, 5.0, 6.6, x => x * x));
  bus(bx, t > 1.7 && t < 4.6);
  busStopFront();
  const gx = 800, gy = 944, ht = TOP(gy), A = armorState(t, 2.7);
  const beat = t < 2.6 ? Math.abs(Math.sin(t * Math.PI * 2)) * 8 : 0;
  const snapUp = R(t, 1.5, 1.8) * (1 - R(t, 2.75, 2.95));
  person(t, 1480, gy, GUEST2, { cup: 1, handL: [1480 - 60, gy - 330], look: t > 2.7 ? [-22, 0] : [0, 0], wide: t > 3.0, mouthO: t > 3.2, blink: blinkAmt(t, [1.0, 6.8]) });
  person(t, gx, gy, HERO, { armor: A, headphones: !A.helmet, bounce: beat, happy: t < 2.6, mouth: t < 2.6 ? .8 : (t > 6.4 ? -.8 : 0), headRot: Math.sin(t * Math.PI * 2) * .05 * (t < 2.6),
    handR: snapUp > 0 ? mix2([gx + 112, gy - 212], [gx + 175, ht - 40], snapUp) : undefined, snapR: snapUp > .5 ? Math.max(bump(t, 2.0, 2.2), bump(t, 2.5, 2.7)) : undefined,
    look: t > 5.0 ? [-24, 0] : [0, 0], wide: t > 2.7 && t < 4.4, chestGlow: A.chest ? .2 : 0, blink: blinkAmt(t, [5.6, 7.2]) });
  if (t < 2.6) musicNotes(gx + 120, ht - 120, t, 1 - R(t, 2.3, 2.6));
  armorFlights(t, 2.7, [gx + 300, -300], gx, gy); clankFlash(t, 2.7, gx, gy);
  burst('SNAP!', gx + 270, ht - 150, .6, Math.max(bump(t, 2.0, 2.35), bump(t, 2.5, 2.85)), .15);
  burst('CLANK!', gx - 260, ht - 60, .75, bump(t, 3.85, 4.5), -.1);
  letterbox();
} },
/* 07: counters card (7 snaps, 4 windows) with Dave and a stack of tape */
{ id: '07', dur: 5.6, draw(t) {
  card(t, '#4a3a52', () => {
    const n1 = Math.min(7, Math.floor(R(t, .4, 1.4, x => x) * 7)), n2 = Math.min(4, Math.floor(R(t, 1.6, 2.4, x => x) * 4));
    X.save(); X.translate(150, 230); X.scale(pop(t, .3, 1), pop(t, .3, 1)); X.translate(-150, -230); fillR(X, 150, 230, 820, 190, 18, '#fde047', 8); text('6:00 PM', 190, 210, 64, '#fde047', 'left', 'Bangers', 8); text(`SNAPS: ${n1}`, 200, 360, 130, '#141014'); X.restore();
    if (t > 1.5) { X.save(); X.translate(150, 470); X.scale(pop(t, 1.5, 1), pop(t, 1.5, 1)); X.translate(-150, -470); fillR(X, 150, 470, 820, 190, 18, '#fde047', 8); text(`WINDOWS: ${n2}`, 200, 600, 130, '#141014'); X.restore(); }
    X.save(); X.translate(1430, 990); X.scale(.85, .85); X.translate(-1430, -990); dave(t, 1430, 990, { noMug: 1, tapeRoll: 1, handR: [1580, 640], handL: [1300, 700], blink: blinkAmt(t, [2.8]) }); X.restore();
    for (let i = 0; i < 4; i++) if (t > 3.2 + i * .25) { const y = 600 - i * 52; shape(X, g => g.ellipse(1640, y, 60, 26, 0, 0, 7), '#c9c4b8'); shape(X, g => g.ellipse(1640, y, 24, 10, 0, 0, 7), '#4a3a52', 4); }
  });
  letterbox();
} },
/* 08: the party. Everyone is happy, he keeps his hands in his pockets */
{ id: '08', dur: 5.0, draw(t) { party(t, 'hands'); } },
/* 09: everybody starts snapping to the music; he sweats */
{ id: '09', dur: 5.4, draw(t) { party(t, 'snapping'); } },
/* 10: the power goes out */
{ id: '10', dur: 4.2, draw(t) { party(t, 'dark'); } },
/* 11: close-up in the dark: fine, one snap */
{ id: '11', dur: 4.4, draw(t) { party(t, 'onesnap'); } },
/* 12: the suit crashes in, his chest lights the room, the speaker plugs into it, everyone dances */
{ id: '12', dur: 6.8, draw(t) { party(t, 'suit'); } },
/* 13: Dave's wish: new windows; he blows the candles out */
{ id: '13', dur: 6.2, draw(t) { party(t, 'wish'); } },
];

function party(t, mode) {
  const gy = 944, hg = 1520, ht = TOP(gy);
  let shots;
  if (mode === 'snapping') shots = [{ a: 0, b: 2.8, cx: 960, cy: 560, z: 1.02, dz: .03 }, { a: 2.8, b: 99, cx: 1322, cy: 440, z: 1.62, dz: .05, blur: 1 }];
  else if (mode === 'onesnap') shots = [{ a: 0, b: 99, cx: 1322, cy: 440, z: 1.62, dz: .06, blur: 1 }];
  else if (mode === 'wish') shots = [{ a: 0, b: 99, cx: 1000, cy: 400, z: 1.42, dz: .05 }];
  else if (mode === 'suit') shots = [{ a: 0, b: 99, cx: 960, cy: 560, z: 1.0, dz: .03, shake: t => bump(t, .2, .6) * 9 }];
  else shots = [{ a: 0, b: 99, cx: 960, cy: 560, z: 1.02, dz: .03 }];
  const s = camera(t, shots);
  X.drawImage(s.blur ? BGS.livingB : BGS.living, 0, 0);
  const dark = mode === 'dark' ? R(t, .3, .45) : (mode === 'onesnap' || mode === 'suit' || mode === 'wish') ? 1 : 0;
  const suitT0 = .4, A = mode === 'suit' ? armorState(t, suitT0) : (mode === 'wish' ? armorState(99, 0) : {});
  const lit = mode === 'wish' ? 1 - R(t, 3.0, 3.15) : 1;
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
  const wishEyes = mode === 'wish' && t > .4 && t < 2.6;
  dave(t, dg, gy - 30, { partyHat: 1, blink: wishEyes ? 1 : blinkAmt(t, [2.2, 4.4]), blowO: mode === 'wish' ? bump(t, 2.7, 3.3) : 0, lift: mode === 'wish' ? R(t, 4.6, 5.1) * (1 - R(t, 5.8, 6.2)) : 0, steam: 1,
    happy: mode === 'wish' && t > 3.3 && t < 4.5, look: mode === 'hands' ? [14, 0] : [5, 0] });
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
  if (mode === 'wish' && t > .5 && t < 2.8) {           // thought bubble: a brand-new window
    const a = R(t, .5, .8) * (1 - R(t, 2.5, 2.8)); X.save(); X.globalAlpha = a;
    for (const [x, y, r] of [[1085, 300, 14], [1125, 262, 22]]) shape(X, g => g.arc(x, y, r, 0, 7), '#fff');
    shape(X, g => g.ellipse(1300, 200, 190, 110, 0, 0, 7), '#fff'); fillR(X, 1220, 140, 160, 120, 6, '#bfe3ff', 6);
    X.strokeStyle = OUT; X.lineWidth = 6; X.beginPath(); X.moveTo(1300, 140); X.lineTo(1300, 260); X.moveTo(1220, 200); X.lineTo(1380, 200); X.stroke();
    text('✦', 1390, 160, 50, '#fde047', 'center', 'serif', 5); X.restore(); }
  if (mode === 'wish') { const f = bump(t, 2.8, 3.3); if (f > 0) { X.save(); X.globalAlpha = f * .7; X.strokeStyle = '#fff'; X.lineWidth = 6; for (let i = -1; i <= 1; i++) { X.beginPath(); X.moveTo(990, 560 + i * 20); X.lineTo(1000 + 40 * f, 600 + i * 30); X.stroke(); } X.restore(); } }
  letterbox();
}

/* ---------- page API ---------- */
let CUR = null;
window.init = id => {
  BGS.bedN = bgBedroom(true); BGS.bedD = bgBedroom(false); BGS.kitchen = bgKitchen(false); BGS.kitchenB = blurOf(BGS.kitchen);
  BGS.street = bgStreet(); BGS.living = bgLiving(); BGS.livingB = blurOf(BGS.living);
  CUR = SCENES.find(s => s.id === id); return CUR.dur;
};
window.render = t => renderSoft(CUR.draw, t);
window.SCENES_META = SCENES.map(s => ({ id: s.id, dur: s.dur }));
