/* Locations for ep01. Each set is painted once into an offscreen canvas (SETS[name].bg),
   floor line at y = FLOOR unless noted. Foreground pieces that must cover characters
   (desks, tables, goal net) are separate functions in FG. */
const FLOOR = 940;
const SET_BUILDERS = {}, SETS_CACHE = {};
const SETS = new Proxy({}, { get: (o, k) => SETS_CACHE[k] || (SETS_CACHE[k] = SET_BUILDERS[k]()) });
function mkCanvas(w = W, h = H) { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; }
function vgrad(g, y0, y1, stops) { const gr = g.createLinearGradient(0, y0, 0, y1); stops.forEach(([o, c]) => gr.addColorStop(o, c)); return gr; }
function windowFrame(g, x, y, w, h, sky, frame = '#f4efe6', bars = true) {
  g.save(); g.beginPath(); g.rect(x, y, w, h); g.clip(); sky(g, x, y, w, h); g.restore();
  g.strokeStyle = OUT; g.lineWidth = 16; g.strokeRect(x, y, w, h); g.strokeStyle = frame; g.lineWidth = 9; g.strokeRect(x, y, w, h);
  if (bars) { g.lineWidth = 14; g.strokeStyle = OUT; g.beginPath(); g.moveTo(x + w / 2, y); g.lineTo(x + w / 2, y + h); g.stroke(); g.lineWidth = 7; g.strokeStyle = frame; g.stroke(); }
  shape(g, q => q.rect(x - 24, y + h, w + 48, 22), frame, 4);
}
function skyDay(g, x, y, w, h, t = 0) { g.fillStyle = vgrad(g, y, y + h, [[0, '#8fc7ef'], [1, '#d6eefc']]); g.fillRect(x, y, w, h);
  for (const [cx, cy, s] of [[x + w * .25, y + h * .3, 1], [x + w * .72, y + h * .2, .8]]) { g.fillStyle = '#ffffff'; for (const [dx, dy, r] of [[0, 0, 34], [36, -10, 40], [74, 0, 32], [36, 12, 34]]) { g.beginPath(); g.arc(cx + dx * s, cy + dy * s, r * s, 0, 7); g.fill(); } } }
function skyMorning(g, x, y, w, h) { g.fillStyle = vgrad(g, y, y + h, [[0, '#9fd0f0'], [.7, '#fde1b0'], [1, '#ffcf8a']]); g.fillRect(x, y, w, h);
  g.fillStyle = '#fff3c4'; g.beginPath(); g.arc(x + w * .7, y + h * .78, 44, 0, 7); g.fill();
  g.fillStyle = '#9db8a8'; for (let i = 0; i < 6; i++) { const bx = x + i * w / 6; g.fillRect(bx + 6, y + h - 40 - (i % 3) * 22, w / 6 - 12, 80); } }
function skyNight(g, x, y, w, h) { g.fillStyle = vgrad(g, y, y + h, [[0, '#141a3a'], [1, '#2c3566']]); g.fillRect(x, y, w, h); const r = rnd(9); g.fillStyle = '#ffffff';
  for (let i = 0; i < 60; i++) { g.globalAlpha = .4 + r() * .6; g.beginPath(); g.arc(x + r() * w, y + r() * h * .8, 1 + r() * 2, 0, 7); g.fill(); } g.globalAlpha = 1; }
function skyRain(g, x, y, w, h) { g.fillStyle = vgrad(g, y, y + h, [[0, '#7d8b9c'], [1, '#aab6c2']]); g.fillRect(x, y, w, h);
  g.fillStyle = '#8994a3'; for (const [cx, cy] of [[x + w * .2, y + h * .2], [x + w * .6, y + h * .15], [x + w * .85, y + h * .3]]) for (const [dx, dy, r] of [[0, 0, 70], [70, -20, 80], [140, 0, 64]]) { g.beginPath(); g.arc(cx + dx, cy + dy, r, 0, 7); g.fill(); } }
function floorBoards(g, y, col1, col2, w = W, h = H) { g.fillStyle = col1; g.fillRect(0, y, w, h - y); g.strokeStyle = col2; g.lineWidth = 3; for (let yy = y + 30; yy < h; yy += 34 + (yy - y) * .15) { g.beginPath(); g.moveTo(0, yy); g.lineTo(w, yy); g.stroke(); }
  g.strokeStyle = OUT; g.lineWidth = 5; g.beginPath(); g.moveTo(0, y); g.lineTo(w, y); g.stroke(); }
function poster(g, x, y, w, h, col, draw) { g.save(); g.translate(x, y); g.rotate((x % 7 - 3) * .006); shape(g, q => q.rect(-w / 2, -h / 2, w, h), col, 4); if (draw) draw(g, w, h); g.restore(); }

/* ---- school hallway (wide: 2600 px so the camera can track a walk) */
SET_BUILDERS.hallway = () => { const w = 2600, c = mkCanvas(w, H), g = c.getContext('2d');
  g.fillStyle = vgrad(g, 0, FLOOR, [[0, '#efe3cc'], [1, '#e2d3b8']]); g.fillRect(0, 0, w, FLOOR);
  g.fillStyle = '#5b8f8a'; g.fillRect(0, 560, w, FLOOR - 560); line(g, [[0, 560], [w, 560]], OUT, 5);
  for (let x = 120; x < w; x += 640) { // ceiling lights
    shape(g, q => rrPath(q, x, 20, 260, 26, 8), '#fbf7ea', 4); const gr = g.createRadialGradient(x + 130, 40, 10, x + 130, 40, 380); gr.addColorStop(0, 'rgba(255,250,220,.35)'); gr.addColorStop(1, 'rgba(255,250,220,0)'); g.fillStyle = gr; g.fillRect(x - 300, 0, 860, 500); }
  // lockers
  const lockerCols = ['#4f86b8', '#4a7eae'];
  for (let x = 40, i = 0; x < w - 100; i++) {
    if (i % 7 === 3) { // classroom door with small window
      shape(g, q => q.rect(x + 10, 250, 230, FLOOR - 250), '#a97a4e', 5); shape(g, q => q.rect(x + 60, 300, 130, 160), '#cfe6f2', 5);
      circ(g, x + 205, 640, 12, '#e3b44c', 4); shape(g, q => rrPath(q, x + 60, 200, 130, 40, 6), '#2f3b4a', 4); text(g, 'AULA ' + (2 + i), x + 125, 230, 30, '#ffffff', 'Bangers', 'center'); x += 280; continue; }
    for (let k = 0; k < 4; k++) { const lx = x + k * 78; shape(g, q => q.rect(lx, 300, 74, FLOOR - 320), lockerCols[(k + i) % 2], 5);
      g.strokeStyle = OUT; g.lineWidth = 3; for (let v = 0; v < 4; v++) { g.beginPath(); g.moveTo(lx + 16, 330 + v * 12); g.lineTo(lx + 58, 330 + v * 12); g.stroke(); }
      shape(g, q => rrPath(q, lx + 54, 560, 10, 46, 4), '#d8dde3', 3); }
    x += 4 * 78 + 40;
    if (i % 3 === 1) { poster(g, x - 20, 200, 120, 150, '#fbfaf6', (q, pw, ph) => { text(q, '¡FÚTBOL!', 0, -30, 34, '#c0262d', 'Bangers', 'center'); propBall(q, 0, 30, 30); }); }
  }
  // bulletin board with Pepe's "wanted" poster (easter egg)
  shape(g, q => q.rect(1240, 120, 330, 160), '#c99a5b', 6);
  poster(g, 1310, 200, 100, 120, '#fbfaf6', (q) => { drawPigeon(q, -6, 30, .42, {}); text(q, 'PEPE', 0, -36, 24, OUT, 'Bangers', 'center'); });
  poster(g, 1420, 190, 110, 90, '#ffe7a3', (q) => { text(q, 'EXAMEN', 0, -6, 26, OUT, 'Bangers', 'center'); text(q, 'MARTES', 0, 22, 22, '#c0262d', 'Bangers', 'center'); });
  poster(g, 1515, 205, 70, 100, '#cfe9d4');
  // floor tiles
  g.fillStyle = '#d9cdb4'; g.fillRect(0, FLOOR, w, H - FLOOR); g.fillStyle = '#cbbd9f';
  for (let y = FLOOR, r = 0; y < H; y += 46, r++) for (let x = (r % 2) * 80; x < w; x += 160) g.fillRect(x, y, 80, 46);
  line(g, [[0, FLOOR], [w, FLOOR]], OUT, 5);
  return { bg: c, w };
};

/* ---- bedroom (morning) */
SET_BUILDERS.bedroom = () => { const c = mkCanvas(), g = c.getContext('2d');
  g.fillStyle = vgrad(g, 0, FLOOR, [[0, '#b7cde6'], [1, '#a5bedb']]); g.fillRect(0, 0, W, FLOOR);
  windowFrame(g, 1180, 150, 520, 400, skyMorning);
  for (const s of [-1, 1]) shape(g, q => { const x = s < 0 ? 1120 : 1700; q.moveTo(x, 110); q.lineTo(x + 80, 110); q.quadraticCurveTo(x + 40 + s * 30, 400, x + 70 * (s < 0 ? 1 : .2), 620); q.lineTo(x + (s < 0 ? 0 : -10), 620); q.closePath(); }, '#e98a6a', 4);
  line(g, [[1100, 108], [1800, 108]], OUT, 8);
  // poster
  poster(g, 330, 260, 240, 300, '#2f3b5a', (q) => { propBall(q, 0, -30, 70); text(q, 'GOOOL', 0, 110, 56, '#fde047', 'Bangers', 'center'); });
  // TV on a dresser (scene 12)
  shape(g, q => q.rect(1560, 640, 300, 300), '#9b6b45', 5); for (let i = 0; i < 2; i++) { shape(g, q => q.rect(1580, 664 + i * 136, 260, 120), '#a87650', 4); circ(g, 1710, 724 + i * 136, 9, '#e3b44c', 3); }
  // shelf + plant
  shape(g, q => q.rect(560, 470, 260, 18), '#9b6b45', 4); propBook(g, 600, 440, 30, 56, '#c0262d'); propBook(g, 634, 440, 30, 56, '#4f86b8'); propBook(g, 668, 444, 30, 48, '#5aa37a'); propPot(g, 760, 468, .45);
  floorBoards(g, FLOOR, '#c99a6b', '#b5865a');
  shape(g, q => q.ellipse(960, 1010, 420, 50, 0, 0, 7), '#e8c36a', 4); // rug
  return { bg: c };
};
/* bed in front of the bedroom wall: drawn in the world layer before the hero (headboard) and after (blanket) */
function bedBack(g) { shape(g, q => rrPath(q, 80, 560, 70, 400, 14), '#7a5a9a', 5); shape(g, q => rrPath(q, 150, 700, 820, 200, 18), '#f4efe6', 5); shape(g, q => rrPath(q, 160, 640, 260, 100, 40), '#ffffff', 5); }
function bedFront(g, cover = 1) { shape(g, q => { q.moveTo(380, 760 - 40 * cover); q.quadraticCurveTo(700, 700 - 40 * cover, 980, 740 - 30 * cover); q.lineTo(990, 930); q.lineTo(370, 930); q.closePath(); }, '#e98a3a', 5);
  g.strokeStyle = 'rgba(255,255,255,.4)'; g.lineWidth = 6; for (let i = 0; i < 4; i++) { g.beginPath(); g.moveTo(460 + i * 130, 790); g.lineTo(500 + i * 130, 900); g.stroke(); }
  shape(g, q => rrPath(q, 140, 900, 860, 50, 10), '#7a5a9a', 5); }
function nightstand(g) { shape(g, q => q.rect(1000, 760, 150, 180), '#9b6b45', 5); shape(g, q => q.rect(1015, 790, 120, 60), '#a87650', 4); }

/* ---- kitchen (daylight) */
SET_BUILDERS.kitchen = () => { const c = mkCanvas(), g = c.getContext('2d');
  g.fillStyle = vgrad(g, 0, FLOOR, [[0, '#f5e7b8'], [1, '#efdca4']]); g.fillRect(0, 0, W, FLOOR);
  windowFrame(g, 1180, 140, 560, 330, skyDay);
  for (let i = 0; i < 4; i++) { const x = 60 + i * 250; shape(g, q => rrPath(q, x, 90, 230, 260, 6), '#7fc4b0', 4); shape(g, q => rrPath(q, x + 186, 200, 9, 40, 4), '#e0b45c', 3); }
  shape(g, q => rrPath(q, 1780, 120, 160, 820, 14), '#e6ebef', 5); line(g, [[1780, 420], [1940, 420]], OUT, 5); shape(g, q => rrPath(q, 1800, 300, 12, 90, 5), '#9aa3ad', 3); shape(g, q => rrPath(q, 1800, 450, 12, 120, 5), '#9aa3ad', 3);
  // magnet: Pepe drawing on the fridge
  poster(g, 1860, 220, 70, 80, '#fbfaf6', (q) => drawPigeon(q, -4, 22, .26, {}));
  shape(g, q => q.rect(-10, 600, 1790, 30), '#e7e0d2', 4); shape(g, q => q.rect(-10, 630, 1790, 310), '#6fb5a1', 4);
  for (let i = 0; i < 7; i++) { const x = 24 + i * 250; shape(g, q => rrPath(q, x, 656, 226, 250, 6), '#7fc4b0', 4); shape(g, q => rrPath(q, x + 96, 680, 40, 9, 4), '#e0b45c', 3); }
  propPot(g, 1640, 600, .5);
  g.fillStyle = '#e9e1d2'; g.fillRect(0, FLOOR, W, H - FLOOR); g.fillStyle = '#d9cfbd'; for (let y = FLOOR, r = 0; y < H; y += 50, r++) for (let x = (r % 2) * 70; x < W; x += 140) g.fillRect(x, y, 70, 50);
  line(g, [[0, FLOOR], [W, FLOOR]], OUT, 5);
  return { bg: c };
};
function kitchenTable(g) { shape(g, q => q.rect(560, 780, 800, 30), '#c98d5a', 5); for (const x of [600, 1300]) shape(g, q => q.rect(x, 810, 26, 150), '#b07848', 4); }

/* ---- classroom */
SET_BUILDERS.classroom = () => { const c = mkCanvas(), g = c.getContext('2d');
  g.fillStyle = vgrad(g, 0, FLOOR, [[0, '#d9e5d0'], [1, '#c9d8bf']]); g.fillRect(0, 0, W, FLOOR);
  shape(g, q => q.rect(420, 120, 1080, 440), '#f8fbfb', 8); shape(g, q => q.rect(400, 560, 1120, 20), '#b9c2c9', 4);
  g.strokeStyle = '#3a6fb0'; g.lineWidth = 6; g.font = '64px "Comic Neue", ComicNeue, sans-serif';
  text(g, 'x² + 2x − 15 = 0', 520, 260, 70, '#3a6fb0', 'ComicNeue'); text(g, 'x = ?', 520, 370, 70, '#c0262d', 'ComicNeue');
  line(g, [[1100, 300], [1300, 430]], '#3a6fb0', 5); line(g, [[1100, 430], [1300, 300]], '#3a6fb0', 5);
  for (const x of [80, 1600]) windowFrame(g, x, 160, 260, 340, skyDay);
  drawPigeon(g, 1720, 498, .45, {}); // Pepe on the window sill
  shape(g, q => q.arc(1780, 90, 46, 0, 7), '#fbfaf6', 5); line(g, [[1780, 90], [1780, 62]], OUT, 5); line(g, [[1780, 90], [1800, 100]], OUT, 5);
  floorBoards(g, FLOOR, '#b98a5c', '#a87a4e');
  return { bg: c };
};
function desk(g, x, y = FLOOR, s = 1) { g.save(); g.translate(x, y); g.scale(s, s); shape(g, q => q.rect(-150, -260, 300, 24), '#d6a46a', 5); shape(g, q => q.rect(-140, -236, 280, 90), '#c4945c', 4); for (const dx of [-130, 118]) shape(g, q => q.rect(dx, -146, 12, 146), '#6b6f78', 3); g.restore(); }
function teacherDesk(g, x) { shape(g, q => q.rect(x - 230, 700, 460, 30), '#9b6b45', 5); shape(g, q => q.rect(x - 220, 730, 440, 210), '#8a5d3b', 5); }

/* ---- street outside school, with a balcony above (flowerpot) ; variant: rain */
function buildStreet(sky) { const c = mkCanvas(), g = c.getContext('2d');
  sky(g, 0, 0, W, FLOOR);
  // apartment building with balcony (right)
  shape(g, q => q.rect(1180, 40, 760, 900), '#e7b38b', 5);
  for (let r = 0; r < 3; r++) for (let k = 0; k < 3; k++) { const x = 1240 + k * 230, y = 90 + r * 250; shape(g, q => q.rect(x, y, 150, 170), '#bfe0f2', 5); line(g, [[x + 75, y], [x + 75, y + 170]], OUT, 4); }
  shape(g, q => q.rect(1200, 300, 360, 24), '#cfd5da', 5); for (let i = 0; i < 9; i++) line(g, [[1210 + i * 42, 324], [1210 + i * 42, 410]], OUT, 5); line(g, [[1200, 410], [1560, 410]], OUT, 7);
  // school fence and gate (left)
  shape(g, q => q.rect(0, 380, 900, 560), '#f0e6d2', 5); text(g, 'ESCUELA SECUNDARIA', 450, 470, 64, '#2f3b4a', 'Bangers', 'center');
  for (let i = 0; i < 4; i++) { shape(g, q => q.rect(60 + i * 210, 540, 150, 170), '#bfe0f2', 5); }
  // tree
  shape(g, q => q.rect(1000, 520, 50, 420), '#8a5d3b', 5); for (const [dx, dy, r] of [[0, -40, 120], [-90, 20, 90], [90, 20, 96], [0, 60, 100]]) circ(g, 1025 + dx, 470 + dy, r, '#5a9a5c', 5);
  // sidewalk + road
  g.fillStyle = '#c9c4bb'; g.fillRect(0, FLOOR - 10, W, H); line(g, [[0, FLOOR - 10], [W, FLOOR - 10]], OUT, 5);
  g.strokeStyle = '#b2aca2'; g.lineWidth = 4; for (let x = 0; x < W; x += 180) { g.beginPath(); g.moveTo(x, FLOOR - 10); g.lineTo(x - 60, H); g.stroke(); }
  return { bg: c };
}
SET_BUILDERS.street = () => buildStreet(skyDay);
SET_BUILDERS.streetRain = () => buildStreet(skyRain);

/* ---- football field */
SET_BUILDERS.field = () => { const c = mkCanvas(), g = c.getContext('2d');
  skyDay(g, 0, 0, W, 560);
  shape(g, q => q.rect(-10, 300, 900, 280), '#e9d7b8', 5); for (let i = 0; i < 6; i++) shape(g, q => q.rect(40 + i * 140, 360, 90, 90), '#bfe0f2', 4);
  text(g, 'ESCUELA', 440, 340, 44, '#2f3b4a', 'Bangers', 'center');
  for (let x = 0; x < W; x += 34) line(g, [[x, 470], [x, 580]], '#8b95a1', 4); line(g, [[0, 480], [W, 480]], '#8b95a1', 5);
  for (let i = 0; i < 12; i++) { g.fillStyle = i % 2 ? '#7fbf6a' : '#74b45f'; g.fillRect(i * 160, 560, 160, H - 560); }
  line(g, [[0, 560], [W, 560]], OUT, 5);
  g.strokeStyle = '#ffffff'; g.lineWidth = 8; g.beginPath(); g.moveTo(1150, 640); g.lineTo(1920, 640); g.moveTo(1150, 640); g.lineTo(1050, 1080); g.stroke();
  g.fillStyle = '#ffffff'; g.beginPath(); g.ellipse(800, 900, 14, 7, 0, 0, 7); g.fill(); // penalty spot
  drawPigeon(g, 300, 590, .4, { flip: -1 }); // Pepe on the grass, far away
  return { bg: c };
};
function goal(g, front) { // goal on the right: posts + net
  if (!front) { g.save(); g.strokeStyle = 'rgba(255,255,255,.55)'; g.lineWidth = 2; for (let x = 1330; x <= 1880; x += 22) { g.beginPath(); g.moveTo(x, 300); g.lineTo(x + 30, 610); g.stroke(); } for (let y = 300; y <= 610; y += 22) { g.beginPath(); g.moveTo(1330, y); g.lineTo(1880, y + 10); g.stroke(); } g.restore(); return; }
  for (const x of [1300, 1880]) tube(g, [[x, 280], [x, 640]], '#ffffff', 16); tube(g, [[1300, 280], [1880, 280]], '#ffffff', 16);
}

/* ---- party room (Nacho's living room) */
SET_BUILDERS.party = () => { const c = mkCanvas(), g = c.getContext('2d');
  g.fillStyle = vgrad(g, 0, FLOOR, [[0, '#f2c58f'], [1, '#e9b57a']]); g.fillRect(0, 0, W, FLOOR);
  windowFrame(g, 120, 160, 360, 320, skyDay);
  // garland
  const flags = 'FELIZ CUMPLE NACHO'; g.strokeStyle = OUT; g.lineWidth = 4; g.beginPath(); g.moveTo(560, 120); g.quadraticCurveTo(1100, 260, 1700, 120); g.stroke();
  for (let i = 0; i < flags.length; i++) { const u = i / (flags.length - 1), x = mix(590, 1670, u), y = 120 + Math.sin(u * Math.PI) * 70 + 4; if (flags[i] === ' ') continue;
    shape(g, q => { q.moveTo(x - 26, y); q.lineTo(x + 26, y); q.lineTo(x, y + 70); q.closePath(); }, ['#e07a8a', '#6fb3e0', '#f0d06a', '#5aa37a', '#9c6fcf'][i % 5], 3); text(g, flags[i], x, y + 38, 32, OUT, 'Bangers', 'center'); }
  // sofa
  shape(g, q => rrPath(q, 1300, 600, 560, 220, 30), '#5a6fb0', 5); shape(g, q => rrPath(q, 1340, 720, 480, 140, 20), '#6a80c4', 5);
  // balloons
  for (const [x, y, col] of [[620, 360, '#e07a8a'], [700, 320, '#6fb3e0'], [1800, 300, '#f0d06a'], [1720, 360, '#9c6fcf']]) { line(g, [[x, y + 70], [x + 10, y + 300]], OUT, 3); ell(g, x, y, 54, 66, 0, col); g.fillStyle = 'rgba(255,255,255,.5)'; g.beginPath(); g.ellipse(x - 18, y - 24, 12, 18, -.4, 0, 7); g.fill(); }
  // photo frame: Nacho and Pepe (easter egg)
  shape(g, q => q.rect(900, 330, 150, 120), '#fbfaf6', 6); drawPigeon(g, 975, 430, .38, {});
  floorBoards(g, FLOOR, '#b07a52', '#9d6b46');
  return { bg: c };
};
function partyTable(g) { shape(g, q => q.rect(560, 760, 800, 30), '#f4efe6', 5); shape(g, q => q.rect(580, 790, 760, 150), '#e07a8a', 5); g.fillStyle = 'rgba(255,255,255,.5)'; for (let x = 600; x < 1330; x += 60) { g.beginPath(); g.arc(x, 800, 14, 0, Math.PI); g.fill(); } }

/* ---- park: day and night, bench in the middle */
function buildPark(night) { const c = mkCanvas(), g = c.getContext('2d');
  (night ? skyNight : skyDay)(g, 0, 0, W, 700);
  if (night) { g.fillStyle = '#fdf6d8'; g.beginPath(); g.arc(1600, 180, 70, 0, 7); g.fill(); g.fillStyle = '#2c3566'; g.beginPath(); g.arc(1630, 160, 64, 0, 7); g.fill(); }
  for (const [x, s] of [[200, 1.1], [520, .8], [1500, .9], [1800, 1.2]]) { shape(g, q => q.rect(x - 22 * s, 700 - 240 * s, 44 * s, 300 * s), night ? '#3e3048' : '#8a5d3b', 5); for (const [dx, dy, r] of [[0, -60, 130], [-100, 10, 100], [100, 10, 104]]) circ(g, x + dx * s, 700 - 300 * s + dy * s, r * s, night ? '#2f4a4a' : '#5a9a5c', 5); }
  g.fillStyle = night ? '#24402e' : '#86c470'; g.fillRect(0, 680, W, H); line(g, [[0, 680], [W, 680]], OUT, 5);
  g.fillStyle = night ? '#5a5466' : '#e3d3ae'; g.beginPath(); g.moveTo(700, 680); g.lineTo(1220, 680); g.lineTo(1500, H); g.lineTo(420, H); g.closePath(); g.fill();
  // lamp post
  tube(g, [[1420, 940], [1420, 380]], '#2f3440', 18); shape(g, q => rrPath(q, 1380, 330, 80, 60, 12), night ? '#fff2b0' : '#dfe6ea', 5);
  if (night) { const gr = g.createRadialGradient(1420, 360, 10, 1420, 600, 520); gr.addColorStop(0, 'rgba(255,236,160,.45)'); gr.addColorStop(1, 'rgba(255,236,160,0)'); g.fillStyle = gr; g.fillRect(800, 300, 1200, 700); }
  return { bg: c };
}
SET_BUILDERS.park = () => buildPark(false); SET_BUILDERS.parkNight = () => buildPark(true);
function bench(g, front) { // seat at y≈800
  if (!front) { shape(g, q => rrPath(q, 640, 640, 640, 40, 8), '#b0743f', 5); shape(g, q => rrPath(q, 640, 690, 640, 40, 8), '#b0743f', 5); return; }
  shape(g, q => rrPath(q, 620, 790, 680, 40, 8), '#c4864b', 5); for (const x of [660, 1240]) shape(g, q => q.rect(x, 830, 22, 110), '#2f3440', 4);
}

/* ---- bathroom: tiles, mirror, sink */
SET_BUILDERS.bathroom = () => { const c = mkCanvas(), g = c.getContext('2d');
  g.fillStyle = '#d7eef2'; g.fillRect(0, 0, W, FLOOR); g.strokeStyle = '#b9dbe2'; g.lineWidth = 4; for (let x = 0; x < W; x += 90) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x, FLOOR); g.stroke(); } for (let y = 0; y < FLOOR; y += 90) { g.beginPath(); g.moveTo(0, y); g.lineTo(W, y); g.stroke(); }
  shape(g, q => q.rect(-10, 640, W + 20, 300), '#f4efe6', 5);
  shape(g, q => rrPath(q, 690, 80, 540, 470, 20), '#9aa3ad', 6); // mirror frame
  shape(g, q => q.ellipse(960, 650, 260, 40, 0, 0, 7), '#ffffff', 5);
  shape(g, q => rrPath(q, 940, 560, 40, 70, 8), '#c8ced6', 4); shape(g, q => { q.moveTo(950, 572); q.lineTo(1060, 572); q.lineTo(1060, 600); q.lineTo(1040, 600); q.lineTo(1040, 590); q.lineTo(950, 590); q.closePath(); }, '#c8ced6', 4);
  shape(g, q => q.rect(1500, 300, 160, 260), '#e07a8a', 5);
  g.fillStyle = '#c9e4ea'; g.fillRect(0, FLOOR, W, H - FLOOR); line(g, [[0, FLOOR], [W, FLOOR]], OUT, 5);
  return { bg: c };
};
function mirrorGlass(g) { g.fillStyle = '#e8f6fb'; g.fillRect(710, 100, 500, 430); g.strokeStyle = 'rgba(255,255,255,.8)'; g.lineWidth = 12; g.beginPath(); g.moveTo(760, 160); g.lineTo(840, 120); g.moveTo(780, 210); g.lineTo(900, 150); g.stroke(); }

/* draw a set into the world layer */
function drawSet(g, name) { g.drawImage(SETS[name].bg, 0, 0); }
