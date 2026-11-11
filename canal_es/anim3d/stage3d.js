/* Stylized 3D stage for the channel (Three.js 0.170, MIT).
   3D brings depth and camera moves; everything visible is drawn in the channel's look:
   - sets are built from our AI-painted plates (facades, sidewalks, back walls, sky) with toon light and plum ink lines;
   - characters and props are our own 2D drawings (drawChar, propPot, drawPigeon...) on cards in 3D space;
   - the frozen-time look is our own compose2: the stage renders a full colour pass (A) and a mask pass (M) of the
     things that keep their colour, with correct occlusion, and compose2 does grey world / colour / wipe / ¡CLAP!.
   Loaded as a module by the episode page; exposes window.S3D. Classic scene scripts call it at render time. */
import * as THREE from 'three';
const T = THREE, INK = '#2d1b2e', BASE = new URL('../anim/cut/bg/', import.meta.url).href;
export const PX = 1 / 300;   // metres per episode-world pixel (characters drawn at s = S0 are ~1.7 m tall)

// ---------------------------------------------------------------- materials
const grad = (() => { const t = new T.DataTexture(new Uint8Array([95, 175, 255]), 3, 1, T.RedFormat); t.minFilter = t.magFilter = T.NearestFilter; t.needsUpdate = true; return t; })();
export const toon = opt => new T.MeshToonMaterial(Object.assign({ gradientMap: grad }, opt));
const inkLine = new T.LineBasicMaterial({ color: INK, transparent: true, opacity: .72 });
const inkHull = new T.MeshBasicMaterial({ color: INK, side: T.BackSide });
export function edged(geo, mats) { const m = new T.Mesh(geo, mats); m.add(new T.LineSegments(new T.EdgesGeometry(geo, 30), inkLine)); return m; }
export function hulled(geo, mat, k = 1.05) { const m = new T.Mesh(geo, mat), h = new T.Mesh(geo, inkHull); h.scale.setScalar(k); m.add(h); return m; }

// ---------------------------------------------------------------- painted plates
const PLATES = {}, PLATE_FILES = ['street', 'streetRain', 'party'];
const loadImg = src => new Promise((ok, bad) => { const im = new Image(); im.onload = () => ok(im); im.onerror = () => bad(new Error('cannot load ' + src)); im.src = src; });
// crop a box given in fractions of the plate (x0, y0, x1, y1) into a repeatable texture
export function crop(plate, [x0, y0, x1, y1], rx = 1, ry = 1) {
  const im = PLATES[plate], w = Math.round((x1 - x0) * im.width), h = Math.round((y1 - y0) * im.height), c = document.createElement('canvas'); c.width = w; c.height = h;
  c.getContext('2d').drawImage(im, x0 * im.width, y0 * im.height, w, h, 0, 0, w, h);
  const t = new T.CanvasTexture(c); t.colorSpace = T.SRGBColorSpace; t.wrapS = t.wrapT = T.RepeatWrapping; t.repeat.set(rx, ry); t.anisotropy = 8; return t;
}

// ---------------------------------------------------------------- renderer (shared)
let GL = null;
function renderer() { if (!GL) { GL = new T.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true }); GL.setPixelRatio(1); GL.setSize(W, H); GL.outputColorSpace = T.SRGBColorSpace; } return GL; }

// ---------------------------------------------------------------- stage
export class Stage {
  constructor({ fog = ['#9aa6ba', 28, 100], sky = null, hemi = ['#eef2ff', '#5a5060', 1.25], sun = ['#fff1dc', 1.35, [-8, 16, 10]] } = {}) {
    this.scene = new T.Scene(); this.cards = {};
    this.cam = new T.PerspectiveCamera(40, W / H, .05, 260);
    if (sky) this.scene.background = sky;
    if (fog) this.scene.fog = new T.Fog(fog[0], fog[1], fog[2]);
    this.scene.add(new T.HemisphereLight(hemi[0], hemi[1], hemi[2]));
    const d = new T.DirectionalLight(sun[0], sun[1]); d.position.set(...sun[2]); this.scene.add(d);
  }
  add(o) { this.scene.add(o); return o; }
  // camera: position, look-at target, vertical field of view for 16:9 (vertical frames get a wider one)
  look(pos, target, fov = 40) { const c = this.cam; c.fov = H > W ? fov * 1.55 : fov; c.aspect = W / H; c.updateProjectionMatrix(); c.position.set(...pos); c.lookAt(...target); c.updateMatrixWorld(); }
  project(x, y, z) { const v = new T.Vector3(x, y, z).project(this.cam); return [(v.x + 1) / 2 * W, (1 - v.y) / 2 * H, v.z < 1]; }
  // a 2D drawing on a card in 3D. draw(g, p) draws with its anchor at canvas (w/2, h - pad): feet or base of the prop.
  // opt: billboard (turn to face the camera around Y), k (supersampling), shadow (blob under it)
  card(key, w, h, draw, opt = {}) {
    if (this.cards[key]) return this.cards[key];
    const k = opt.k || 1, pad = opt.pad ?? 40, c = document.createElement('canvas'); c.width = w * k; c.height = h * k; const g = c.getContext('2d');
    const tex = new T.CanvasTexture(c); tex.colorSpace = T.SRGBColorSpace; tex.anisotropy = 8;
    const geo = new T.PlaneGeometry(w * PX, h * PX).translate(0, (h / 2 - pad) * PX, 0);
    const mesh = new T.Mesh(geo, new T.MeshBasicMaterial({ map: tex, alphaTest: .5, side: T.DoubleSide, fog: true }));
    const grp = new T.Group(); grp.add(mesh);
    if (opt.shadow !== false) { const b = new T.Mesh(new T.CircleGeometry(.42, 24), new T.MeshBasicMaterial({ color: '#1a1424', transparent: true, opacity: .26, depthWrite: false }));
      b.rotation.x = -Math.PI / 2; b.scale.set(1, .42, 1); b.position.y = .012; grp.add(b); }
    this.scene.add(grp);
    let last = null;
    const card = { grp, mesh, billboard: opt.billboard !== false,
      at(x, y, z) { grp.position.set(x, y, z); return card; },
      colored(on) { mesh.userData.colored = !!on; mesh.renderOrder = on ? 10 : 0; return card; },
      redraw(p, sig) { if (sig != null && sig === last) return card; last = sig;   // frozen cards draw once
        g.setTransform(k, 0, 0, k, 0, 0); g.clearRect(0, 0, w, h); draw(g, w / 2, h - pad, p); tex.needsUpdate = true; return card; },
      show(v) { grp.visible = v; return card; } };
    return (this.cards[key] = card);
  }
  // character card: drawChar with the episode's scale; frozen characters (p.still) are drawn once
  char(key, cname, opt = {}) { return this.card(key, opt.w || 760, opt.h || 980, (g, x, y, p) => drawChar(g, cname, Object.assign({ x, y, s: S0, noShadow: 1 }, p)), Object.assign({ k: 2 }, opt)); }
  // two passes: everything in colour into A; then only the coloured things, occluded by the world's depth, into M
  render(A, M) {
    const gl = renderer(), sc = this.scene, cam = this.cam;
    for (const c of Object.values(this.cards)) if (c.billboard) c.grp.rotation.set(0, Math.atan2(cam.position.x - c.grp.position.x, cam.position.z - c.grp.position.z), 0);
    gl.setSize(W, H); gl.setClearColor(0x000000, 1); gl.clear(); gl.render(sc, cam);
    A.setTransform(1, 0, 0, 1, 0, 0); A.drawImage(gl.domElement, 0, 0);
    const off = [], bg = sc.background;
    sc.traverse(o => { if (!o.material || o.userData.colored) return; for (const m of [].concat(o.material)) if (m.colorWrite) { m.colorWrite = false; off.push(m); } });
    sc.background = null; gl.setClearColor(0x000000, 0); gl.clear(); gl.render(sc, cam);
    for (const m of off) m.colorWrite = true; sc.background = bg;
    M.setTransform(1, 0, 0, 1, 0, 0); M.clearRect(0, 0, W, H); M.drawImage(gl.domElement, 0, 0);
  }
}

// ---------------------------------------------------------------- sets
let seed = 11; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
const WALLS = ['#d79a7c', '#d9c9b4', '#c9a184', '#bfb4c9', '#cfa58f'];
export function tree(st, x, z, s = 1) {
  const trunk = edged(new T.CylinderGeometry(.16 * s, .22 * s, 2.6 * s, 10), toon({ color: '#7a4b2e' })); trunk.position.set(x, 1.3 * s, z); st.add(trunk);
  for (const [dx, dy, dz, r] of [[0, 3.6, 0, 1.15], [-.85, 3.0, .1, .9], [.85, 3.0, -.1, .9], [0, 2.8, .55, .9]]) {
    const b = hulled(new T.SphereGeometry(r * s, 20, 14), toon({ color: dy > 3.2 ? '#6fa65a' : '#5e9450' }), 1.045); b.position.set(x + dx * s, dy * s, z + dz * s); st.add(b); }
}
function lamp(st, x, z) {
  const pole = edged(new T.CylinderGeometry(.07, .09, 4.4, 10), toon({ color: '#3a3f4a' })); pole.position.set(x, 2.2, z); st.add(pole);
  const head = edged(new T.BoxGeometry(.48, .3, .48), toon({ color: '#fff3c4', emissive: '#4a4020' })); head.position.set(x, 4.5, z); st.add(head);
}
// A street running along -z: road |x| < 5, sidewalks 5..9, buildings from 9 out. plate: 'street' | 'streetRain'
export function street(st, plate, opt = {}) {
  seed = opt.seed || 11;
  const P = { orange: [.632, .283, .992, .513], cream: [.02, .451, .45, .699], school: [0, .354, .468, .858], sky: [0, 0, .6, .33], walk: [0, .868, 1, 1] };
  st.scene.background = crop(plate, P.sky); st.scene.background.wrapS = st.scene.background.wrapT = T.ClampToEdgeWrapping;
  const road = new T.Mesh(new T.PlaneGeometry(10, 260), toon({ color: plate === 'streetRain' ? '#4a4f5c' : '#55586a' })); road.rotation.x = -Math.PI / 2; road.position.z = -100; st.add(road);
  const walkTex = crop(plate, P.walk, 1, 20);
  for (const s of [-1, 1]) { const m = toon({ color: '#9a948e' }), top = toon({ map: walkTex });
    const sw = edged(new T.BoxGeometry(4, .18, 260), [m, m, top, m, m, m]); sw.position.set(s * 7, .09, -100); st.add(sw); }
  for (let z = 10; z > -220; z -= 5) { const d = new T.Mesh(new T.PlaneGeometry(.22, 2.2), toon({ color: '#ead8a2' })); d.rotation.x = -Math.PI / 2; d.position.set(0, .01, z); st.add(d); }
  if (plate === 'streetRain') for (let i = 0; i < 20; i++) { const p = new T.Mesh(new T.CircleGeometry(1, 24), new T.MeshBasicMaterial({ color: '#9fb2cc', transparent: true, opacity: .45, depthWrite: false }));
    p.rotation.x = -Math.PI / 2; p.scale.set(.6 + (i * 37 % 10) / 8, .25 + (i * 53 % 7) / 18, 1); p.position.set(((i * 71) % 9) - 4.5, .015, 4 - i * 9.3); st.add(p); }
  // opt.left / opt.right: hand-placed buildings first (from z = 10 down), e.g. { w: 13, h: 7.2, tex: 'school' }; random ones after
  for (const s of [-1, 1]) for (let z = 10, i = 0; z > -210; i++) {
    const spec = (s < 0 ? opt.left : opt.right || [])?.[i] || {};
    let w = spec.w || 9 + Math.round(rnd() * 2) * 4.5, h = spec.h || 9.6 + Math.round(rnd() * 3) * 3.2, tex = spec.tex || (rnd() < .55 ? 'orange' : 'cream');
    const front = toon({ map: tex === 'school' ? crop(plate, P.school) : tex === 'orange' ? crop(plate, P.orange, w / 4.6, h / 3.1) : crop(plate, P.cream, w / 7.5, h / 3.3) });
    const wall = toon({ color: WALLS[Math.floor(rnd() * WALLS.length)] }), d = 7;
    const b = edged(new T.BoxGeometry(d, h, w), s < 0 ? [front, wall, wall, wall, wall, wall] : [wall, front, wall, wall, wall, wall]);
    b.position.set(s * (9 + d / 2), h / 2, z - w / 2); st.add(b);
    const l = edged(new T.BoxGeometry(d + .5, .4, w + .3), toon({ color: '#e9ded0' })); l.position.set(s * (9 + d / 2), h + .2, z - w / 2); st.add(l);
    z -= w + .6; }
  for (let z = -2; z > -170; z -= 16) { lamp(st, -5.4, z); lamp(st, 5.4, z - 8); }
  for (const [x, z] of opt.trees || []) tree(st, x, z);
}
// a balcony on the right-hand facade (x = 9): slab and railing; returns the point the pot fell from
export function balcony(st, y, z) {
  const slab = edged(new T.BoxGeometry(1.4, .16, 2.4), toon({ color: '#d9cfc2' })); slab.position.set(8.3, y, z); st.add(slab);
  const bar = toon({ color: '#3a3346' });
  const top = edged(new T.BoxGeometry(.08, .08, 2.4), bar); top.position.set(7.62, y + 1.0, z); st.add(top);
  for (let k = -1.1; k <= 1.1; k += .2) { const b = new T.Mesh(new T.CylinderGeometry(.025, .025, 1.0, 6), bar); b.position.set(7.62, y + .5, z + k); st.add(b); }
  for (const s of [-1, 1]) { const b = edged(new T.BoxGeometry(1.4, .08, .08), bar); b.position.set(8.3, y + 1.0, z + s * 1.18); st.add(b); }
  return [7.75, y + .2, z];
}
// a room: the plate is the back wall, its bottom strip the floor; toon side walls
export function room(st, plate, { w = 9.6, d = 8, wallTop = .865, side = '#e9a77a' } = {}) {
  const im = PLATES[plate], h = w * (wallTop * im.height) / im.width;
  st.scene.background = new T.Color(side); if (st.scene.fog) st.scene.fog.far = 400;
  const back = new T.Mesh(new T.PlaneGeometry(w, h), toon({ map: crop(plate, [0, 0, 1, wallTop]) })); back.position.set(0, h / 2, -d / 2); st.add(back);
  const floor = new T.Mesh(new T.PlaneGeometry(w, d * 1.6), toon({ map: crop(plate, [0, wallTop + .01, 1, 1], 1, 6) })); floor.rotation.x = -Math.PI / 2; floor.position.set(0, 0, d * .3 - d / 2 + d * .5); st.add(floor);
  for (const s of [-1, 1]) { const sw = edged(new T.BoxGeometry(.2, h, d * 1.6), toon({ color: side })); sw.position.set(s * w / 2, h / 2, d * .3); st.add(sw); }
  const base = edged(new T.BoxGeometry(w, .14, .06), toon({ color: '#f4ede2' })); base.position.set(0, .07, -d / 2 + .03); st.add(base);
  return { w, h, d };
}
// drop sprite like the 2D episode's: ink-outlined bead when frozen, a soft streak while falling
export function dropTexture(frozen) { const c = document.createElement('canvas'); c.width = c.height = 64; const g = c.getContext('2d');
  if (frozen) { g.fillStyle = '#d6ecff'; g.strokeStyle = INK; g.lineWidth = 5; g.beginPath(); g.ellipse(32, 34, 13, 20, 0, 0, 7); g.fill(); g.stroke(); g.fillStyle = '#fff'; g.beginPath(); g.arc(27, 25, 5, 0, 7); g.fill(); }
  else { const gr = g.createLinearGradient(0, 0, 0, 64); gr.addColorStop(0, 'rgba(225,238,255,0)'); gr.addColorStop(1, 'rgba(225,238,255,.95)'); g.strokeStyle = gr; g.lineWidth = 5; g.lineCap = 'round'; g.beginPath(); g.moveTo(34, 2); g.lineTo(30, 62); g.stroke(); }
  const t = new T.CanvasTexture(c); t.colorSpace = T.SRGBColorSpace; return t; }
export function points(st, n, size, tex) { const pos = new Float32Array(n * 3), geo = new T.BufferGeometry(); geo.setAttribute('position', new T.BufferAttribute(pos, 3));
  const mat = new T.PointsMaterial({ map: tex, size, transparent: true, depthWrite: false, alphaTest: .3 }); const p = new T.Points(geo, mat); st.add(p);
  return { p, pos, mat, update() { geo.attributes.position.needsUpdate = true; } }; }

// ---------------------------------------------------------------- frame helpers for scene scripts
const CAMI = { cx: W / 2, cy: H / 2, z: 1 };
// render the stage and composite with the episode's freeze look; f = freezeState(...) or { amt }
export function frame(X, st, f, look) { const A = layer('A'), M = layer('M'); CUR_LOOK = look || {}; window.__camz = 1;
  st.render(A, M); compose2(X, { A, M, cam: CAMI }, f); window.__cam = CAMI; }
export const key = (list, t) => {   // camera keyframes [{t, pos, at, fov}], eased between neighbours
  let i = 0; while (i + 1 < list.length && t >= list[i + 1].t) i++;
  const a = list[i], b = list[i + 1]; if (!b || b.cut || t <= a.t) return a;   // a key with cut: 1 starts a new shot (hard cut)
  const u = io((t - a.t) / (b.t - a.t)), m = (p, q) => p.map((v, j) => v + (q[j] - v) * u);
  return { pos: m(a.pos, b.pos), at: m(a.at, b.at), fov: a.fov + ((b.fov ?? a.fov) - a.fov) * u };
};

window.S3D = { THREE, Stage, street, balcony, room, tree, crop, toon, edged, hulled, dropTexture, points, frame, key, PX };
window.S3D_READY = Promise.all(PLATE_FILES.map(n => loadImg(BASE + n + '.jpg').then(im => { PLATES[n] = im; }))).then(() => true);
