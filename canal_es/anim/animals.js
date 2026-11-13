/* Talking animals (ep03): cut-out animals from AI-painted parts (cut/animals/*.png), code-driven mouths and heads,
   and the episode's signature look — a speech bubble that starts as the animal's sound («MIAU») and scrambles into words.

   drawAnimal(g, 'croqueta', x, y, s, { open, tilt, nod, head: 'bored'|'wide', flip })   front view, sitting; x, y = ground point
   drawSpr(g, 'catWalk', x, y, h, { flip, rot, bob })                                       any single sprite, bottom-centre at x, y, h world px tall
   pigeonTalk(g, x, y, s, { open, front, flip, tint, tilt })                                 Pepe and the park gang, beak opens with p.open
   talkBubble(X, cam, wx, wy, lineId, sound, { dx, dy, w })                                  the translation bubble for a voiced line */
const ANI = {};
const ANI_FILES = ['catBody', 'catHeadBored', 'catHeadWide', 'catSleep', 'catWalk', 'dogABody', 'dogAHead', 'dogARun', 'dogBBody', 'dogBHead', 'dogBStand',
  'canelaBody', 'canelaHead', 'canelaRun', 'firuBody', 'firuHead', 'firuStand', 'hamBody', 'hamHead', 'hamHeadSide', 'cage', 'prairie', 'mosquito',
  'parrot', 'turtle', 'roofCat', 'bowl', 'choco', 'cookie', 'plant'];
const ANI_BASE = (document.currentScript && document.currentScript.src || '').replace(/[^/]*$/, '');
const ANI_READY = Promise.all(ANI_FILES.map(n => new Promise((ok, bad) => { const im = new Image(); im.onload = () => { ANI[n] = im; ok(); };
  im.onerror = () => bad(new Error('animals: cannot load ' + n)); im.src = ANI_BASE + 'cut/animals/' + n + '.png'; })));

/* per animal: body + head images (same sheet scale), neck top on the body (fraction of width, px from top),
   head socket (fractions of the head image that sit on the neck), mouth (fractions of the head) and world px per image px */
const ANIMALS = {
  croqueta: { body: 'catBody', heads: { bored: 'catHeadBored', wide: 'catHeadWide' }, neck: [.534, 30], sock: [.5, .86], mouth: [.5, .755, .13], k: .30, col: '#e8914a' },
  dogA:     { body: 'dogABody', heads: { n: 'dogAHead' }, neck: [.5, 26], sock: [.5, .80], mouth: [.5, .665, .2], k: .34, col: '#e2a55a' },
  dogB:     { body: 'dogBBody', heads: { n: 'dogBHead' }, neck: [.5, 22], sock: [.47, .86], mouth: [.445, .78, .17], k: .30, col: '#f4efe6' },
  canela:   { body: 'canelaBody', heads: { n: 'canelaHead' }, neck: [.43, 24], sock: [.5, .86], mouth: [.5, .79, .11], k: .30, col: '#c98a52' },
  firu:     { body: 'firuBody', heads: { n: 'firuHead' }, neck: [.495, 28], sock: [.48, .72], mouth: [.47, .775, .15], k: .33, col: '#5a4a44' },
  hamster:  { body: 'hamBody', heads: { n: 'hamHead', side: 'hamHeadSide' }, neck: [.5, 40], sock: [.5, .80], mouth: [.5, .665, .1], k: .22, col: '#eab062' },
};
function aniImg(g, name, x, y, w, h) { const I = ANI[name]; if (I) g.drawImage(I, x, y, w, h); }
/* an open mouth on a head drawn at the origin, image box (0,0)-(hw,hh); open 0..1 */
function aniMouth(g, hw, hh, m, open) { if (open <= .04) return; const mx = m[0] * hw, my = m[1] * hh, w = m[2] * hw * (.75 + .25 * open), h = hw * (.03 + .11 * open);
  g.save(); g.beginPath(); g.ellipse(mx, my + h * .35, w / 2, h / 2 + 2, 0, 0, Math.PI * 2); g.fillStyle = '#4a1d2c'; g.fill();
  g.clip(); g.beginPath(); g.ellipse(mx, my + h * .95, w * .32, h * .42, 0, 0, Math.PI * 2); g.fillStyle = '#e8788a'; g.fill(); g.restore();
  g.beginPath(); g.ellipse(mx, my + h * .35, w / 2, h / 2 + 2, 0, 0, Math.PI * 2); g.lineWidth = Math.max(3, hw * .012); g.strokeStyle = '#2a1420'; g.stroke(); }
function drawAnimal(g, kind, x, y, s, p = {}) {
  const A = ANIMALS[kind], B = ANI[A.body]; if (!B) return; const k = A.k * s, f = p.flip || 1;
  const bw = B.width * k, bh = B.height * k, sq = 1 + (p.squash || 0);
  g.save(); g.translate(x, y + (p.bob || 0)); g.scale(f, 1 / sq);
  aniImg(g, A.body, -bw * A.neck[0], -bh, bw, bh);
  const hn = A.heads[p.head] || Object.values(A.heads)[0], H = ANI[hn], hw = H.width * k, hh = H.height * k;
  const nx = 0, ny = -bh + A.neck[1] * k;   // neck top in world (relative to x, y)
  g.translate(nx + (p.hx || 0), ny + (p.nod || 0) * 10 * s); g.rotate((p.tilt || 0) + (p.open || 0) * .03 * Math.sin((p.t || 0) * 11));
  const sock = p.head === 'side' ? [.45, .8] : A.sock;
  g.translate(-sock[0] * hw, -sock[1] * hh);
  aniImg(g, hn, 0, 0, hw, hh);
  if (p.head !== 'side') aniMouth(g, hw, hh, A.mouth, p.open || 0);
  g.restore();
  return [x + f * (A.mouth[0] - sock[0]) * hw, y + ny + (A.mouth[1] - sock[1]) * hh];   // world point of the mouth, for bubbles
}
/* the world point of an animal's mouth without drawing (same geometry as drawAnimal) */
function animalMouthAt(kind, x, y, s, p = {}) { const A = ANIMALS[kind], B = ANI[A.body], k = A.k * s, H = ANI[A.heads[p.head] || Object.values(A.heads)[0]];
  if (!B || !H) return [x, y - 200 * s]; const bh = B.height * k, hw = H.width * k, hh = H.height * k, ny = -bh + A.neck[1] * k;
  return [x + (p.flip || 1) * (A.mouth[0] - A.sock[0]) * hw, y + ny + (A.mouth[1] - A.sock[1]) * hh]; }
function drawSpr(g, name, x, y, h, p = {}) { const I = ANI[name] || (typeof SPR !== "undefined" && SPR[name]); if (!I) return; const w = I.width / I.height * h;
  g.save(); g.translate(x, y + (p.bob || 0)); g.rotate(p.rot || 0); g.scale(p.flip || 1, 1); if (p.alpha != null) g.globalAlpha *= p.alpha;
  g.drawImage(I, -w / 2, -h, w, h); g.restore(); }

/* Pepe and the gang. Same body/head sprites as drawPigeon (cutout.js); p.open opens the beak; p.tint = [hueDeg, brightness] for the other pigeons */
function pigeonTalk(g, x, y, s, p = {}) {
  const f = p.flip || 1, open = p.open || 0;
  g.save(); g.translate(x, y); g.scale(s * f, s);
  if (p.tint) g.filter = `hue-rotate(${p.tint[0]}deg) brightness(${p.tint[1]}) saturate(${p.tint[2] || 1})`;
  spr(g, 'pepeBody', -108, -118, 176, 122);
  g.translate(30, -96 + (p.peck || 0) * 30); g.rotate((p.tilt || 0) + (p.peck || 0) * .5);
  if (p.front) { g.scale(1 / f, 1); const w = 56, h = 86, x0 = -28, y0 = -84; spr(g, 'pepeFront', x0, y0, w, h);
    if (open > .04) { const bx = x0 + .49 * w, by = y0 + .47 * h, o = open;   // lower beak drops, upper beak redrawn on top
      g.filter = 'none'; g.beginPath(); g.ellipse(bx, by + 2 + 3 * o, 4 + 2 * o, 1 + 5 * o, 0, 0, 7); g.fillStyle = '#d0607a'; g.fill();
      g.beginPath(); g.moveTo(bx - 6, by + 2 + 6 * o); g.lineTo(bx + 6, by + 2 + 6 * o); g.lineTo(bx, by + 8 + 8 * o); g.closePath(); g.fillStyle = '#55596a'; g.fill(); g.lineWidth = 1.4; g.strokeStyle = '#2a1420'; g.stroke();
      if (p.tint) g.filter = `hue-rotate(${p.tint[0]}deg) brightness(${p.tint[1]}) saturate(${p.tint[2] || 1})`;
      const I = SPR.pepeFront, sx = .36 * I.width, sy = .33 * I.height, sw = .27 * I.width, sh = .19 * I.height;
      g.drawImage(I, sx, sy, sw, sh, x0 + .36 * w, y0 + .33 * h, .27 * w, .19 * h); } }
  else { const w = 80, h = 84, x0 = -34, y0 = -82; spr(g, 'pepeHead', x0, y0, w, h);
    if (open > .04) { const hx = x0 + .80 * w, hy = y0 + .43 * h, tip = x0 + 1.0 * w, o = open;
      g.filter = 'none'; g.beginPath(); g.moveTo(hx, hy); g.lineTo(tip - 2, hy + 2); g.lineTo(tip - 5, hy + 2 + 8 * o); g.lineTo(hx, hy + 4); g.closePath(); g.fillStyle = '#d0607a'; g.fill();
      g.beginPath(); g.moveTo(hx, hy + 3 + 1 * o); g.lineTo(tip - 6, hy + 3 + 8 * o); g.lineTo(hx + 3, hy + 7 + 3 * o); g.closePath(); g.fillStyle = '#55596a'; g.fill(); g.lineWidth = 1.4; g.strokeStyle = '#2a1420'; g.stroke();
      if (p.tint) g.filter = `hue-rotate(${p.tint[0]}deg) brightness(${p.tint[1]}) saturate(${p.tint[2] || 1})`;
      const I = SPR.pepeHead, sx = .78 * I.width, sy = .25 * I.height, sw = .22 * I.width, sh = .2 * I.height;
      g.drawImage(I, sx, sy, sw, sh, x0 + .78 * w, y0 + .25 * h, .22 * w, .2 * h); } }
  g.restore();
  return p.front ? [x + f * 30 * s, y + (-96 - 84 + .47 * 86) * s] : [x + f * (30 - 34 + 76) * s, y + (-96 - 82 + .45 * 84) * s];
}

/* ---------------------------------------------------------------- the translation bubble */
const SCRAMBLE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ¡¿!?#@%&*';
function wrapLines(g, s, maxW) { const words = s.split(' '), out = []; let cur = '';
  for (const w of words) { const tst = cur ? cur + ' ' + w : w; if (g.measureText(tst).width > maxW && cur) { out.push(cur); cur = w; } else cur = tst; }
  if (cur) out.push(cur); return out; }
/* golden rings from a mouth (screen coords) while the animal talks */
function soundRings(X, sx, sy, k, t, flip = 1) { if (k <= 0) return; X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.lineCap = 'round';
  for (let i = 0; i < 3; i++) { const u = ((t * 1.6 + i / 3) % 1), r = 18 + u * 70; X.globalAlpha = clamp(k) * (1 - u) * .9; X.strokeStyle = '#ffd34d'; X.lineWidth = 6 - 3 * u;
    X.beginPath(); X.arc(sx, sy, r, flip > 0 ? -.7 : Math.PI - .7, flip > 0 ? .7 : Math.PI + .7); X.stroke(); }
  X.restore(); }
/* wx, wy: speaker's mouth in world coords. The bubble sits above-left/right of it (o.dx, o.dy in screen px), the tail points at the mouth.
   For the first .3 s it shows the animal's sound, then the letters scramble into the translated line, typed at the speed of the voice. */
function talkBubble(X, cam, wx, wy, id, sound, o = {}) {
  const L = id ? T().L[id] : [o.t0, o.d]; if (!L) return; const t0 = L[0], d = L[1], t = o.t;   // id null: an unvoiced gag line (o.text, o.t0, o.d)
  const hold = o.hold == null ? .3 : o.hold, a = R(t, t0 - .04, t0 + .12, outC) * (1 - R(t, t0 + d + hold, t0 + d + hold + .2));   // short pre-roll and hold: no bubble leaks into the neighbouring shot
  if (a <= 0) return;
  const txt = o.text || (typeof VO_TEXT !== 'undefined' && VO_TEXT[id]) || id; let [mx, my] = worldToScreen(cam, wx, wy);
  mx = clamp(mx, 90, W - 90); my = clamp(my, 260, H - 150);   // speaker off-screen: the bubble sits at that edge, tail pointing out
  const size = o.size || 54, maxW = o.w || 700;
  X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.font = `bold ${size}px ComicNeue`;
  const lines = wrapLines(X, txt, maxW), lw = Math.max(...lines.map(l => X.measureText(l).width)), lh = size * 1.12;
  const bw = Math.max(lw, 160) + 56, bh = lines.length * lh + 40;
  const rr = (o.r || 110) * (cam.z || 1);   // speaker's head radius on screen: side bubbles sit beside the head, centred ones above it
  let bx, by; if (o.dx == null) { bx = mx - bw / 2; by = my - rr * 1.7 - bh; } else { bx = o.dx < 0 ? mx - rr * 1.15 - bw : mx + rr * 1.15; by = my - rr * .9 - bh * .6; }
  bx = clamp(bx, 30, W - bw - 30); by = clamp(by, 24, H - bh - 30);
  const s = .85 + .15 * back(R(t, t0 - .04, t0 + .2)); X.translate(bx + bw / 2, by + bh / 2); X.scale(s, s); X.translate(-bw / 2, -bh / 2); X.globalAlpha = clamp(a);
  // tail toward the mouth
  const tx = clamp(mx - bx, 50, bw - 50), ty = bh, ex = tx + (mx - bx - tx) * .5, ey = ty + Math.max(30, ((my - by) - ty) * .5);   // a short tail aimed at the mouth
  X.beginPath(); X.moveTo(tx - 26, ty - 4); X.quadraticCurveTo(tx - 6, (ty + ey) / 2, ex, ey); X.quadraticCurveTo(tx + 10, (ty + ey) / 2, tx + 26, ty - 4); X.closePath();
  X.fillStyle = '#fff6dc'; X.fill(); X.lineWidth = 6; X.strokeStyle = '#2a1420'; X.stroke();
  X.beginPath(); rrPath(X, 0, 0, bw, bh, 30); X.fillStyle = '#fff6dc'; X.fill(); X.lineWidth = 6; X.strokeStyle = '#2a1420'; X.stroke();
  X.fillStyle = '#fff6dc'; X.fillRect(tx - 22, bh - 8, 44, 10);   // hide the seam where the tail joins
  // paw badge
  X.save(); X.translate(bw - 14, 14); X.fillStyle = '#ffd34d'; X.beginPath(); X.arc(0, 0, 26, 0, 7); X.fill(); X.lineWidth = 5; X.strokeStyle = '#2a1420'; X.stroke(); X.fillStyle = '#2a1420';
  X.beginPath(); X.ellipse(0, 6, 9, 7, 0, 0, 7); X.fill(); for (const [px, py] of [[-10, -5], [-3, -11], [5, -11], [11, -4]]) { X.beginPath(); X.arc(px, py, 3.6, 0, 7); X.fill(); } X.restore();
  // text: sound -> scramble -> words typed with the voice
  const ph = t - t0, typed = clamp((ph - .25) / Math.max(.3, d * .92));
  X.fillStyle = '#2a1420'; X.textAlign = 'left'; X.textBaseline = 'alphabetic';
  if (ph < .22) { X.font = `${size * 1.25}px Bangers`; X.textAlign = 'center'; X.fillText(sound, bw / 2, bh / 2 + size * .42); }
  else { let budget = Math.max(1, Math.round(typed * txt.length)); const r = rnd(Math.floor(t * 24) + 7);
    lines.forEach((l, i) => { let shown = '';
      for (let c = 0; c < l.length; c++) { if (budget > 0) { shown += l[c]; budget--; } else if (budget > -3 && l[c] !== ' ') { shown += SCRAMBLE[Math.floor(r() * SCRAMBLE.length)]; budget--; } else break; }
      budget--; X.fillText(shown, 28, 20 + lh * (i + .82)); }); }
  X.restore();
}
