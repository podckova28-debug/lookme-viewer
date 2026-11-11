/* Ep01: stylized 3D shots (painted look, ?hyb=1). They replace the 2D version of a scene, or part of it,
   with the same lines, timing and freeze events, so the mix and the probe do not change.
   - s00 cold open: bullet time around the frozen flower pot, the frozen street, the hero sprints in, rewind;
   - s08 frozen rain: the hero walks through hanging drops that part around him;
   - s13 the forty minutes alone: a slow orbit around the hero inside the frozen party.
   Stages are built once per page (window.S3D comes from anim3d/stage3d.js). */
(() => {
  const SC2D = { s00: SC.s00, s08: SC.s08, s13: SC.s13 }, STAGES = {};
  const use3d = () => HYB && window.S3D;
  const stage = (name, build) => STAGES[name] || (STAGES[name] = build(window.S3D));
  const sig = p => JSON.stringify(p, (k, v) => typeof v === 'function' ? undefined : typeof v === 'number' ? Math.round(v * 100) / 100 : v);
  const UMB = ['#c0262d', '#3a6fb0', '#2f8f5a', '#e0a32a'];
  function umbrella(col) { return (g, x, y) => { g.save(); g.translate(x, y); line(g, [[0, 0], [0, -260]], '#2a2a30', 7);
    shape(g, q => { q.moveTo(-190, -250); q.quadraticCurveTo(0, -420, 190, -250); q.quadraticCurveTo(95, -275, 0, -250); q.quadraticCurveTo(-95, -275, -190, -250); q.closePath(); }, col, 5); g.restore(); }; }
  // frozen pedestrians: [name, x, z, pose extras]
  function crowd(st, list) { list.forEach(([n, x, z, p], i) => { const pose = Object.assign({ still: 1, t: 0, blink: 0, walk: 1, phase: .7 + i * 1.3, mouth: .2 }, p);
    st.char('ex' + i + n, n).at(x, .18, z).redraw(pose, sig(pose)); }); }

  /* ============================================================== s00: cold open */
  function s00(X, t) {
    const st = stage('s00', D => { const s = new D.Stage({ fog: ['#cfdcec', 34, 120], hemi: ['#fff6e8', '#6a5a60', 1.3], sun: ['#fff0d8', 1.55, [-10, 18, 6]] });
      D.street(s, 'street', { left: [{ w: 10 }, { w: 13, h: 7.2, tex: 'school' }], right: [{ w: 8 }, { w: 12, h: 12.8, tex: 'orange' }], trees: [[-5.6, -15], [5.6, -19], [-5.6, -34]] });
      s.potFrom = D.balcony(s, 6.6, -4);
      crowd(s, [['ex2', 6.5, -7.6, { flip: -1, look: [-10, 4], open: .4 }], ['ex3', 7.1, -9.5, { look: [10, 0] }], ['ex1', -6.8, -6, { look: [12, 2], hR: [150, -420] }],
        ['ex4', -7.4, -12.5, { flip: -1 }], ['ex5', -6.3, -21, { look: [-8, 6] }], ['ex6', 7.6, -17, { flip: -1, look: [6, 0] }], ['nacho', -6.6, -28, { look: [14, -4], open: .6 }]]);
      // soil crumbs frozen around the falling pot
      s.crumbs = D.points(s, 40, .05, D.dropTexture(true)); s.crumbs.mat.color = new D.THREE.Color('#6b4a33');
      for (let i = 0; i < 40; i++) { const a = i * 2.4, r = .12 + (i % 7) * .05; s.crumbs.pos.set([7.75 + Math.cos(a) * r, 2.5 + (i % 5) * .07 + Math.sin(a * 1.7) * .08, -4 + Math.sin(a) * r], i * 3); } s.crumbs.update();
      return s; });
    const D = window.S3D, run0 = Lt('s00_03') - .2, run1 = Le('s00_03') + .3, rw = Lm('s00_05', .5);
    const tr = t < rw ? t : Math.max(0, rw - (t - rw) * 4), running = tr > run0 && tr < run1;
    const POT = [7.75, 2.32, -4.0];
    st.card('pot', 300, 300, (g, x, y) => propPot(g, x, y - 30 * .7, .7, .08), { shadow: false, pad: 20 }).at(...POT).redraw({}, 'pot');
    const vblink = bump(t, Lm('s00_02', .55), Lm('s00_02', .55) + .22);   // clue: she blinks (payoff in s19)
    const rp = { still: 1, t: 0, blink: vblink, look: [4, 18], mouth: .1, hR: [20, -380], holdR: (q, x, y) => propPhone(q, x, y - 40, .55, 76, -.1) };
    st.char('ren', 'valeria').at(7.65, .18, -4).redraw(rp, 'r' + Math.round(vblink * 10));
    st.card('pepe', 240, 200, (g, x, y, p) => drawPigeon(g, x, y, .6, p), { shadow: false, pad: 12 }).colored(1).at(7.62, 7.68, -3.25).redraw({ flip: -1, tilt: .25 * bump(t, Lt('s00_04'), Lt('s00_04') + 1.2) });
    // hero: sprints out of the depth of the frozen street, stops under the pot, looks up
    const k = R(tr, run0, run1, outC), hp = { t, walk: running ? 1 : 0, phase: tr * 13, lean: running ? (t < rw ? .14 : -.14) : 0, look: [16, -6], mouth: -.3, brow: .7, wide: .5, sweat: tr > run1 ? 1 : 0 };
    if (tr > run1) { hp.look = [8, -22]; hp.hR = [150, -560]; hp.open = .4; }
    const hero = st.char('hero', 'tu').colored(1).at(mix(2.4, 6.3, k), .18, mix(-26, -3.2, k)).show(tr > run0 - .05).redraw(hp);
    // camera: bullet time around the pot -> crane up over the frozen street -> runner's view -> under the pot
    const K = [
      { t: 0, pos: [5.6, 1.2, -0.7], at: [7.7, 2.0, -4.3], fov: 34 },
      { t: Lt('s00_02') - .35, pos: [4.7, 1.5, -1.6], at: [7.7, 2.0, -4.1], fov: 34 },
      { t: Lt('s00_02') + .25, pos: [3.3, 2.5, 2.2], at: [6.9, 2.0, -5.2], fov: 40 },
      { t: Lt('s00_03') - .2, pos: [2.2, 3.6, 5.4], at: [5.8, 3.0, -7.0], fov: 40 },
      { t: Lt('s00_03') - .15, cut: 1, pos: [3.4, 1.35, 3.4], at: [4.6, 1.35, -12], fov: 40 },
      { t: Le('s00_03') + .3, pos: [3.9, 1.3, 1.6], at: [6.2, 1.5, -6.5], fov: 40 },
      { t: Lt('s00_04') - .1, cut: 1, pos: [5.05, 1.05, -0.95], at: [7.25, 1.95, -4.0], fov: 40 },
      { t: rw, pos: [5.35, 1.12, -1.25], at: [7.25, 2.0, -4.0], fov: 38 },
    ];
    const c = D.key(K, tr); st.look(c.pos, c.at, c.fov);
    D.frame(X, st, { amt: 1 }, LOOK.street);
    const [px, py] = st.project(POT[0], POT[1] - .25, POT[2]), hd = st.project(7.65, 1.62, -4), pe = st.project(7.62, 7.8, -3.25);
    window.__focus = hd; window.__pepe = pe;
    if (t < Lt('s00_02') - .05) sticker(X, '50 cm', R(t, Le('s00_01') - .6, Le('s00_01') - .3, outC), px + 70, py - 40, 70);
    if (running && t < rw) speedLines(X, ...st.project(hero.grp.position.x, 1.1, hero.grp.position.z), .6, t);
    rewindFX(X, R(t, rw, rw + .25), t);
    if (t > T().dur - .25) { X.save(); X.globalAlpha = R(t, T().dur - .25, T().dur, lin); X.fillStyle = '#ffffff'; X.fillRect(0, 0, W, H); X.restore(); }
  }

  /* ============================================================== s08: frozen rain (street part) */
  function s08(X, t) {
    const st = stage('s08', D => { const s = new D.Stage({ fog: ['#8c98ad', 24, 95] });
      D.street(s, 'streetRain', { left: [{ w: 9, tex: 'cream' }], trees: [[-5.6, -24], [5.6, -40]] });
      const UMBR = (i) => ({ hR: [70, -480], holdR: umbrella(UMB[i % 4]) });
      crowd(s, ['ex1', 'ex2', 'ex3', 'ex4', 'ex5', 'ex6', 'nacho', 'ex2', 'ex1', 'ex3'].map((n, i) => [n, (i % 2 ? -1 : 1) * (5.7 + (i * 37 % 10) / 7), -5 - i * 6.2, Object.assign({ flip: i % 3 ? 1 : -1, look: [(i * 13 % 20) - 10, 4] }, i % 3 !== 1 ? UMBR(i) : {})]));
      s.N = 9000; s.base = []; let sd = 5; const r = () => (sd = (sd * 16807) % 2147483647) / 2147483647;
      for (let i = 0; i < s.N; i++) { const far = r() < .3; s.base.push([(r() - .5) * (far ? 17 : 12), r() * (far ? 9 : 5.5), far ? -12 - r() * 60 : 9 - r() * 21]); }
      s.rain = D.points(s, s.N, .34, D.dropTexture(false)); s.streak = s.rain.mat;
      s.bead = new D.THREE.PointsMaterial({ map: D.dropTexture(true), size: .15, transparent: true, depthWrite: false, alphaTest: .4 });
      return s; });
    const D = window.S3D, tc = Lt('s08_02') + .15, walkT0 = Lt('s08_04') - .2, home = Lt('s08_05') - .1, frozen = t >= tc;
    // hero: walks out of school with a hand over his head, claps, looks at the hanging drops, walks home dodging them
    let z = t < tc ? mix(-9, -6.2, R(t, 0, tc - .35, lin)) : t < walkT0 ? -6.2 : mix(-6.2, 2.0, R(t, walkT0, home, lin));
    const hp = { t, walk: (t < tc - .35 || t > walkT0) ? 1 : 0, phase: t * 7.5, look: [0, -10], mouth: -.5, brow: .6, hR: [60, -660] };
    if (t > tc - .45 && t < tc + .6) { const G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = clapHands(t, tc, G, .25); hp.armsFront = 1; }
    if (t > tc + .5) { hp.hR = null; hp.look = [Math.sin((t - tc) * 1.4) * 16, -12]; hp.wide = .5; hp.mouth = .6; hp.brow = .2; }
    if (t > Lt('s08_03') + .4 && t < walkT0) { hp.hR = [140, -600]; hp.look = [16, -16]; }   // pokes a hanging drop
    if (t > walkT0) { hp.look = [Math.sin(t * 1.7) * 14, -6]; hp.mouth = .9; hp.wide = 0; hp.lean = Math.sin(t * 4) * .1; }
    st.char('hero', 'tu').colored(1).at(Math.sin(t * 4) * .25 * (t > walkT0), .18, z).redraw(hp);
    // rain: falls until the clap, then hangs; the drops on his path part as he walks through
    const ft = Math.min(t, tc), b = st.base, pos = st.rain.pos; st.rain.p.material = frozen ? st.bead : st.streak;
    for (let i = 0; i < st.N; i++) { const [x, y0, zz] = b[i]; let y = ((y0 - ft * 11) % 9 + 9) % 9, px = x;
      const r = Math.hypot(x, zz - z); if (frozen && t > walkT0 && r < 1.0 && y < 2.2 && zz > z - .2) px += Math.sign(x || 1) * (1 - r) * 1.1;
      pos[i * 3] = px; pos[i * 3 + 1] = y + .05; pos[i * 3 + 2] = zz; }
    st.rain.update();
    const push = R(t, tc + .4, walkT0, io), back = R(t, walkT0, home, lin);
    st.look([Math.sin(t * .35) * .5, 1.35 + .25 * push, z + 5.2 - 1.6 * push + 1.0 * back], [0, 1.2 + .2 * push, z - 3], 38);
    const [cx, cy] = st.project(0, 1.35, z);
    D.frame(X, st, freezeState(t, [{ t: tc, x: cx, y: cy, screen: 1 }], { cx: W / 2, cy: H / 2, z: 1 }), LOOK.streetRain);
    if (t > tc - .02 && t < tc + .14) { X.save(); X.globalAlpha = 1 - Math.abs(t - tc - .05) / .1; X.fillStyle = '#fff'; X.fillRect(0, 0, W, H); X.restore(); }
  }

  /* ============================================================== s13: forty minutes alone in the frozen party */
  function s13(X, t) {
    const st = stage('s13', D => { const s = new D.Stage({ fog: null, hemi: ['#fff1e0', '#7a5a50', 1.35], sun: ['#ffe2c0', 1.2, [-6, 10, 8]] });
      D.room(s, 'party', { w: 9.6, d: 8, side: '#eaa57c' });
      s.card('table', 900, 260, (g, x, y) => g.drawImage(SPR.partyTable, x - 415, y - 194, 830, 194), { billboard: false, shadow: false, pad: 10 }).at(0, 0, -1.4).redraw({}, 't');
      s.card('cake', 360, 300, (g, x, y) => propCake(g, x, y - 40, .8, 1, 0, true), { billboard: false, shadow: false, pad: 10 }).at(0, .6, -1.35).redraw({}, 'c');
      [['ex1', -1.9, 1], ['ex4', -1.0, 2], ['ex5', 1.0, 3], ['ex2', 1.9, 4]].forEach(([n, x, sd]) => { const p = { still: 1, t: 0, blink: 0, look: [x < 0 ? 12 : -12, 6], mouth: .6, open: .5, armsFront: 1 };
        [p.hL, p.hR] = POSE.clap(.15 + .1 * sd, charGeom(CAST[n], p)); s.char('g' + n, n).at(x, 0, -2.3).redraw(p, 'g'); });
      const np = { still: 1, t: 0, blink: 0, marker: 1, look: [0, 8], mouth: 1, armsFront: 1 }; [np.hL, np.hR] = POSE.clap(.1, charGeom(CAST.nacho, np));
      s.card('nacho', 760, 1100, (g, x, y) => { drawChar(g, 'nacho', Object.assign({ x, y, s: S0, noShadow: 1 }, np)); const S = S0 * CAST.nacho.s, hy = y + S * (charGeom(CAST.nacho, np).top - 100);
        partyHat(g, x, hy - CAST.nacho.r * S * .95, .8); }, { k: 2 }).at(0, 0, -2.35).redraw({}, 'n');
      return s; });
    const D = window.S3D, a0 = Lt('s13_13b') - .1, a1 = Lt('s13_14') - .1, u = R(t, a0, a1, io);
    const hp = { t, slump: .7, lid: .45, mouth: -.4, sweat: 1, look: [Math.sin((t - a0) * 1.2) * 16, 4], hL: [-40, -300], hR: [40, -300], armsFront: 1 };
    st.char('hero', 'tu').colored(1).at(2.1, 0, .2).redraw(hp);
    // orbit around the hero, slowly pulling out: alone in the middle of the song
    const ang = mix(-.42, .32, u), rad = mix(2.9, 4.4, u), tgt = [mix(1.7, 1.1, u), 1.25, mix(-.4, -.8, u)];
    st.look([2.1 + Math.sin(ang) * rad, mix(1.45, 2.0, u), .2 + Math.cos(ang) * rad], tgt, 40);
    D.frame(X, st, { amt: 1 }, LOOK.party);
    bigCounter(X, 'APLAUSO:', '40 MINUTOS', 1, 70, 60);
  }

  SC.s00 = (X, t) => use3d() ? s00(X, t) : SC2D.s00(X, t);
  SC.s08 = (X, t) => use3d() && t < Lt('s08_05') - .1 ? s08(X, t) : SC2D.s08(X, t);
  SC.s13 = (X, t) => use3d() && t > Lt('s13_13b') - .1 && t < Lt('s13_14') - .1 ? s13(X, t) : SC2D.s13(X, t);
})();
