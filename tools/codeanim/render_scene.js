// usage: node render_scene.js PAGE.html SCENE_ID OUT.mp4 [sheetOnly: comma list of times -> png]
const { chromium } = require('playwright'); const { spawn } = require('child_process'); const path = require('path'); const fs = require('fs');
(async () => {
  const [page_, id, out, sheet] = process.argv.slice(2); const fps = 24;
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + path.resolve(page_)); await p.evaluate(() => window.ready);
  const dur = await p.evaluate(id => window.init(id), id);
  if (errs.length) { console.error(errs.join('\n')); process.exit(1); }
  if (sheet) {
    for (const t of sheet.split(',').map(Number)) { const d = await p.evaluate(t => { window.render(t); return document.getElementById('c').toDataURL('image/jpeg', .9); }, t); fs.writeFileSync(`${out}_${t}.jpg`, Buffer.from(d.split(',')[1], 'base64')); }
    if (errs.length) console.error(errs.join('\n')); await b.close(); return;
  }
  const n = Math.round(dur * fps);
  const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-crf', '17', '-pix_fmt', 'yuv420p', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = 0; i < n; i++) {
    const d = await p.evaluate(t => { window.render(t); return document.getElementById('c').toDataURL('image/jpeg', .95); }, i / fps);
    if (!ff.stdin.write(Buffer.from(d.split(',')[1], 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); if (errs.length) console.error(errs.join('\n')); await b.close(); console.log(id, 'frames', n);
})();
