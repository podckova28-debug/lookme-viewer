// usage: node probe.js OUT.json [hz]  -> per scene: clap events + frozen state sampled at hz
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const out = process.argv[2], hz = parseFloat(process.argv[3] || '10');
  const T = JSON.parse(fs.readFileSync(path.join(__dirname, 'timing.json'))); const res = {};
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  for (const sid of T.order) {
    await p.goto('file://' + path.join(__dirname, 'ep01.html') + '?scene=' + sid); await p.evaluate(() => window.ready);
    const dur = T.scenes[sid].dur, frz = [], seg = [];
    for (let t = 0; t < dur; t += 1 / hz) { const r = await p.evaluate(t => { window.render(t); return [window.__frz || 0, window.__seg || '']; }, t); frz.push(r[0]); seg.push(r[1]); }
    const ev = await p.evaluate(s => EVENTS[s] || null, sid);
    let cuts = 0; for (let i = 1; i < seg.length; i++) if (seg[i] !== seg[i - 1]) cuts++; res[sid] = { frz, hz, ev, cuts }; process.stdout.write(sid + ' ');
  }
  fs.writeFileSync(out, JSON.stringify(res)); await b.close(); console.log('ok');
})();
