// usage: node still.js PAGE.html[?query] OUT.png t1 [t2 ...]  -> renders window.render(t) and saves PNG(s) (OUT gets _t suffix if several)
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [page_, out, ...ts] = process.argv.slice(2); const [f, q] = page_.split('?');
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', e => console.error('PAGE ERROR', e.message)); p.on('console', m => { if (m.type() === 'error') console.error('console', m.text()); });
  await p.goto('file://' + path.resolve(f) + (q ? '?' + q : '')); await p.evaluate(() => window.ready);
  for (const t of ts.length ? ts : ['0']) {
    await p.evaluate(t => window.render(t), parseFloat(t));
    const d = await p.evaluate(() => document.getElementById('c').toDataURL('image/png'));
    const o = ts.length > 1 ? out.replace(/\.png$/, `_${t}.png`) : out;
    require('fs').writeFileSync(o, Buffer.from(d.split(',')[1], 'base64'));
  }
  await b.close();
})();
