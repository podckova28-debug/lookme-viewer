/* Shared episode helpers: scene registry, narration-keyed timing, lip sync, camera shots, speech bubble.
   Same as the top of ep01/scenes1.js; new episodes load this instead of copying it. */
let SID = 's01';
const SC = {};
const T = () => TIM.scenes[SID];
const Lt = id => T().L[id][0], Ld = id => T().L[id][1], Le = id => Lt(id) + Ld(id), Lm = (id, f) => Lt(id) + Ld(id) * f;
const speaking = (t, id) => t >= Lt(id) && t <= Le(id);
/* lip sync: mouth follows the loudness envelope of the actual voice line (vo_env.js) */
const talk = (t, id) => { if (!speaking(t, id)) return 0; const e = typeof VO_ENV !== 'undefined' && VO_ENV[id];
  if (e) { const f = (t - Lt(id)) * 30, i = Math.floor(f), u = f - i, a = e[Math.min(i, e.length - 1)] || 0, b = e[Math.min(i + 1, e.length - 1)] || 0; return clamp(mix(a, b, u) * .9); }
  return .25 + .45 * Math.abs(Math.sin((t - Lt(id)) * 13)) * (1 - .4 * Math.abs(Math.sin((t - Lt(id)) * 3.1))); };
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
