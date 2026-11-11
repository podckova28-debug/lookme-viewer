// Stills of a 3D shot: node still3d.js PAGE.html OUT_PREFIX CUES_JSON t1 t2 ...
const http = require('http'), fs = require('fs'), path = require('path'), { chromium } = require('playwright');
const [PAGE, OUT, CUES, ...TS] = process.argv.slice(2), ROOT = path.resolve(__dirname, '..');
const TYPES = { '.js': 'text/javascript', '.html': 'text/html', '.png': 'image/png', '.jpg': 'image/jpeg', '.ttf': 'font/ttf' };
const server = http.createServer((q, r) => { const p = path.join(ROOT, decodeURIComponent(q.url.split('?')[0]));
  if (!p.startsWith(ROOT) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { r.writeHead(404); return r.end(); }
  r.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(r); }).listen(0, async () => {
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', e => console.error('PAGE ERROR', e.message)); p.on('console', m => { if (m.type() === 'error') console.error('console', m.text()); });
  const rel = path.relative(ROOT, path.resolve(PAGE)).split(path.sep).join('/');
  await p.goto(`http://127.0.0.1:${server.address().port}/${rel}?hyb=1&cues=${encodeURIComponent(CUES)}`); await p.waitForFunction('window.ready === true', null, { timeout: 120000 });
  // the hero's arm springs integrate over time: step through from 0 so every still matches the video
  let last = 0; for (const t of TS.map(Number).sort((a, b) => a - b)) {
    for (let u = last; u < t; u += 1 / 24) await p.evaluate(u => window.render(u), u);
    await p.evaluate(t => window.render(t), t); last = t;
    const d = await p.evaluate(() => document.getElementById('c').toDataURL('image/png'));
    fs.writeFileSync(`${OUT}_${t}.png`, Buffer.from(d.split(',')[1], 'base64')); }
  await b.close(); server.close(); });
