// node render.js S [frames] -> frames/S/0000.png ; screenshots of the page at each time step
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const S = +process.argv[2], N = +(process.argv[3] || 96), only = process.argv[4];
  const dir = path.join(__dirname, 'frames', String(S)); fs.mkdirSync(dir, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
  p.on('console', m => console.log('page:', m.text())); p.on('pageerror', e => console.log('ERR', e.message));
  await p.goto('file://' + path.join(__dirname, 'flash.html') + '?s=' + S);
  await p.evaluate(() => window.ready);
  const list = only ? only.split(',').map(Number) : [...Array(N).keys()];
  for (const i of list) {
    await p.evaluate(t => window.renderAt(t), i / 24);
    await p.screenshot({ path: path.join(dir, String(i).padStart(4, '0') + '.png') });
  }
  await b.close(); console.log('done', S, list.length);
})();
