/* Ep02: stylized 3D shots (painted look, ?hyb=1). Same lines and timing as the 2D versions they replace.
   - s00 cold open and s14 the question: the street outside school, Renata walks up, her ghost from five seconds ahead
     already stands in front of you asking. The camera moves around them.
   Ghosts are cards marked "colored": the first render has them hidden (the present), the second render keeps only them
   (occluded by the world's depth) and that layer goes through ghostFX like the 2D ghosts. */
(() => {
  const SC2D = { s00: SC.s00, s14: SC.s14 }, STAGES = {};
  const use3d = () => HYB && window.S3D;
  const CAMI = { cx: W / 2, cy: H / 2, z: 1 };
  // positions along the right-hand sidewalk; the camera looks at the school from the road, so screen-right is +z
  const X0 = 7.0, HERO_Z = -8.0, GHOST_Z = -6.6, REN_STOP = -5.5;
  function streetStage() {
    return STAGES.street || (STAGES.street = (D => { const s = new D.Stage({ fog: ['#d8c9b8', 30, 120], hemi: ['#fff3e0', '#6a5a60', 1.3], sun: ['#ffe2b8', 1.6, [-12, 14, 8]] });
      D.street(s, 'street', { left: [{ w: 9 }, { w: 12, h: 12.8, tex: 'orange' }], right: [{ w: 4 }, { w: 14, h: 7.2, tex: 'school' }, { w: 12, h: 12.8, tex: 'orange' }], trees: [[5.6, -13.5], [-5.6, -18], [5.6, -30]] });
      s.hero = s.card('hero', 760, 980, (g, x, y, p) => { drawChar(g, 'tu', Object.assign({ x, y, s: S0, noShadow: 1 }, p)); futEyes(g, 'tu', Object.assign({ x, y, s: S0 }, p), p.eyes || 0); }, { k: 2 });
      s.ren = s.char('ren', 'valeria');
      s.ghost = s.char('ghost', 'valeria', { shadow: false }).colored(1);
      s.pepe = s.card('pepe', 240, 200, (g, x, y, p) => drawPigeon(g, x, y, .6, p), { shadow: false, pad: 12 });
      s.walkers = [['ex3', 8.3, -16, -0.6], ['ex5', 8.5, -1, 0.6]].map(([n, x, z, v]) => ({ card: s.char('w' + n, n), x, z, v }));
      return s; })(window.S3D));
  }
  // render the present (ghosts hidden), then the ghosts alone, and composite them as the hologram
  function frameF(X, st, ga, t) {
    const A = layer('A'), M = layer('M'); CUR_LOOK = LOOK.street || {}; window.__camz = 1;
    st.ghost.show(false); st.render(A, M); compose2(X, { A, M, cam: CAMI }, { amt: 0 }); window.__cam = CAMI; window.__ghost = ga;
    if (ga > 0) { st.ghost.show(true); const A2 = layer('A2'), F = layer('F'); st.render(A2, F); futVignette(X, ga); ghostFX(X, F, ga, t); }
  }
  function people(st, tt) { for (const w of st.walkers) { const z = w.z + w.v * tt; w.card.at(w.x, .18, z).redraw({ t: tt, walk: 1, phase: z * 2.6, flip: w.v > 0 ? -1 : 1 }); } }
  const key = (K, t) => window.S3D.key(K, t);

  /* ============================================================== s00: cold open */
  function s00(X, t) {
    const st = streetStage(), rw = Lm('s00_05', .45), tr = t < rw ? t : Math.max(0, rw - (t - rw) * 4);
    people(st, tr);
    const rz = mix(-0.5, REN_STOP, R(tr, 0, 13, lin)), walking = tr < 13;
    st.ren.at(X0 + .2, .18, rz).redraw({ t: tr, walk: walking ? 1 : 0, phase: rz * 2.6, flip: -1, look: [-10, 2], mouth: .2, hR: [70, -330], holdR: (g, x, y) => propBook(g, x + 4, y - 20, 70, 90, '#4f86b8', .2) });
    const hp = { t, look: [14, 0], mouth: -.1, brow: .5, wide: .4 };
    if (t > Lt('s00_04')) { hp.open = .5 * R(t, Lt('s00_04'), Lt('s00_04') + .5); hp.sweat = 1; hp.brow = .8; hp.lean = .06; }
    if (t > rw) { hp.wide = 0; hp.open = 0; }
    const ga = vis(t, .2, rw - .2, .5); hp.eyes = ga;
    st.hero.at(X0, .18, HERO_Z).redraw(hp);
    st.ghost.at(X0, .18, GHOST_Z).redraw({ t, flip: -1, look: [-14, 0], open: .2 + .5 * Math.abs(Math.sin(t * 9)) * (Math.sin(t * 1.3) > -.3 ? 1 : 0), blush: .5, hL: [-60, -330], hR: [40, -470] });
    st.pepe.at(8.4, .18, -10.4).redraw({ flip: 1, peck: Math.max(0, Math.sin(t * 2.2)) * .6 });
    const K = [
      { t: 0, pos: [5.0, 1.55, -6.7], at: [X0, 1.5, HERO_Z], fov: 30 },
      { t: Lt('s00_02') - .2, pos: [5.2, 1.5, -7.3], at: [X0, 1.5, HERO_Z], fov: 30 },
      { t: Lt('s00_02') - .15, cut: 1, pos: [2.2, 1.7, -5.0], at: [X0, 1.25, -6.8], fov: 40 },
      { t: Lt('s00_03') - .15, pos: [2.6, 2.0, -7.9], at: [X0, 1.25, -6.6], fov: 40 },
      { t: Lt('s00_03') - .1, cut: 1, pos: [5.1, 1.65, -5.2], at: [X0, 1.72, GHOST_Z], fov: 38 },
      { t: Lt('s00_04') - .15, pos: [5.0, 1.65, -5.6], at: [X0, 1.72, GHOST_Z], fov: 38 },
      { t: Lt('s00_04') - .1, cut: 1, pos: [5.3, 1.55, -7.0], at: [X0, 1.52, HERO_Z], fov: 32 },
      { t: rw - .05, pos: [5.8, 1.55, -7.5], at: [X0, 1.55, HERO_Z], fov: 28 },
      { t: rw, cut: 1, pos: [0.5, 4.2, 1.0], at: [X0 - .5, 1.2, -7.0], fov: 44 },
      { t: T().dur, pos: [0.8, 4.6, 2.2], at: [X0 - .5, 1.2, -7.0], fov: 44 },
    ];
    const c = key(K, t); st.look(c.pos, c.at, c.fov);
    frameF(X, st, ga, t);
    if (t > Lt('s00_02') && t < rw) { const [bx, by] = st.project(X0, 2.15, GHOST_Z); bubble(X, '¿…?', bx, by, R(t, Lt('s00_02'), Lt('s00_02') + .3, back) * ga, 64); }
    futHUD(X, ga, 5 - (t / (rw + 1.5)) * 5);
    rewindFX(X, R(t, rw, rw + .25), t);
    if (t > T().dur - .25) { X.save(); X.globalAlpha = R(t, T().dur - .25, T().dur, lin); X.fillStyle = '#ffffff'; X.fillRect(0, 0, W, H); X.restore(); }
  }

  /* ============================================================== s14: the question, answered too early */
  function s14(X, t) {
    const st = streetStage(), arrive = Lt('s14_05') + 2.5, blurt = Lt('s14_08'), leaveG = Lt('s14_11');
    people(st, t + 20);
    const rz = mix(-0.5, REN_STOP, R(t, Lt('s14_02'), arrive, io)), walking = t > Lt('s14_02') && t < arrive;
    const rp = { t, walk: walking ? 1 : 0, phase: rz * 2.6, flip: -1, look: [-10, 2], mouth: .3, blush: .4, hR: [70, -330], holdR: (g, x, y) => propBook(g, x + 4, y - 20, 70, 90, '#4f86b8', .2) };
    if (t > blurt) { rp.walk = 0; rp.wide = .7; rp.open = .2; rp.mouth = 0; rp.brow = .5; rp.blush = 0; }
    if (speaking(t, 's14_10')) { rp.open = talk(t, 's14_10'); rp.wide = .3; rp.brow = .8; }
    if (t > Le('s14_10')) { rp.lid = .4; rp.mouth = -.2; rp.wide = 0; }
    st.ren.at(X0 + .2, .18, rz).redraw(rp);
    const hp = { t, look: [14, 0], mouth: .1 };
    if (t > Lt('s14_03')) { hp.wide = .4; hp.brow = .4; }
    if (t > Lt('s14_05')) { hp.mouth = -.1; hp.brow = .7; hp.sweat = t > Lt('s14_06') ? 1 : 0; hp.rot = t > Lt('s14_07') ? Math.sin(t * 30) * .02 : 0; }
    if (speaking(t, 's14_08') || (t > blurt && t < Lt('s14_09'))) { hp.open = speaking(t, 's14_08') ? talk(t, 's14_08') : 0; hp.mouth = .9; hp.wide = .8; const G = charGeom(CAST.tu, hp); [hp.hL, hp.hR] = POSE.stretch(R(t, blurt, blurt + .3, back) * .9, G); }
    if (t > Lt('s14_09')) { hp.hL = hp.hR = null; hp.mouth = -.3; hp.sweat = 1; hp.wide = .2; }
    const ga1 = vis(t, Lt('s14_03') + .3, blurt - .1), ga2 = vis(t, leaveG - .2, T().dur), ga = Math.max(ga1, ga2); hp.eyes = ga;
    st.hero.at(X0, .18, HERO_Z).redraw(hp);
    if (ga2 > 0) { const u = R(t, leaveG + .3, leaveG + 3.5, lin), z = REN_STOP + 5.5 * u; st.ghost.at(X0 + .2, .18, z).redraw({ t, flip: 1, walk: u > 0 && u < 1 ? 1 : 0, phase: z * 2.6, look: [10, 4], mouth: -.2 }); }
    else st.ghost.at(X0, .18, GHOST_Z).redraw({ t, flip: -1, look: [-14, 0], blush: .6, open: speaking(t, 's14_04') ? talk(t, 's14_04') : .1, hL: [-60, -330], hR: [40, -470] });
    st.pepe.at(8.4, .18, -10.4).redraw({ flip: 1, peck: Math.max(0, Math.sin(t * 2.2)) * .6 });
    const K = [
      { t: 0, pos: [0.5, 4.4, 1.6], at: [X0 - .5, 1.2, -7.0], fov: 44 },
      { t: Lt('s14_02') - .1, pos: [2.6, 1.7, -4.4], at: [X0, 1.3, -6.0], fov: 40 },
      { t: Lt('s14_03') - .1, cut: 1, pos: [5.1, 1.55, -6.8], at: [X0, 1.5, HERO_Z], fov: 30 },
      { t: Lt('s14_04') - .1, cut: 1, pos: [2.4, 1.6, -5.2], at: [X0, 1.35, -6.6], fov: 38 },
      { t: Lt('s14_05') - .15, pos: [2.8, 1.8, -7.6], at: [X0, 1.35, -6.6], fov: 38 },
      { t: Lt('s14_05') - .1, cut: 1, pos: [5.1, 1.6, -5.0], at: [X0, 1.55, GHOST_Z], fov: 32 },
      { t: Lt('s14_06') - .1, cut: 1, pos: [5.4, 1.55, -7.1], at: [X0, 1.52, HERO_Z], fov: 32 },
      { t: blurt - .1, pos: [5.9, 1.55, -7.6], at: [X0, 1.53, HERO_Z], fov: 26 },
      { t: blurt - .05, cut: 1, pos: [3.2, 1.5, -6.6], at: [X0, 1.35, -6.8], fov: 38 },
      { t: Lt('s14_09') - .1, cut: 1, pos: [5.3, 1.6, -4.7], at: [X0 + .2, 1.55, REN_STOP], fov: 32 },
      { t: Lt('s14_10') - .1, cut: 1, pos: [3.0, 1.55, -6.5], at: [X0, 1.35, -6.8], fov: 38 },
      { t: leaveG - .1, cut: 1, pos: [2.0, 2.2, -8.6], at: [X0, 1.2, -4.8], fov: 42 },
      { t: T().dur, pos: [2.2, 2.4, -9.4], at: [X0, 1.2, -4.0], fov: 42 },
    ];
    const c = key(K, t); st.look(c.pos, c.at, c.fov);
    frameF(X, st, ga, t);
    if (speaking(t, 's14_04')) { const [bx, by] = st.project(X0, 2.15, GHOST_Z); bubble(X, '¿FERIA DE CIENCIAS?', bx, by, ga1, 50); }
    if (t > blurt && t < Lt('s14_09') + .5) { const [bx, by] = st.project(X0, 2.15, HERO_Z); bubble(X, '¡SÍ! ¡SÍ QUIERO!', bx, by, R(t, blurt, blurt + .2, back), 58); }
    futHUD(X, ga, ga2 > 0 ? hudN(t, leaveG - .2, leaveG + 4.5) : hudN(t, Lt('s14_03') + .3, arrive + .6));
  }

  SC.s00 = (X, t) => use3d() ? s00(X, t) : SC2D.s00(X, t);
  SC.s14 = (X, t) => use3d() ? s14(X, t) : SC2D.s14(X, t);
})();
