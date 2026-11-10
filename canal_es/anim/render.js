// usage: node render.js PAGE.html[?query] SECONDS OUT.mp4 [FROM]  (renders window.render(t) at 24 fps)
const { chromium } = require('playwright'); const { spawn } = require('child_process'); const path = require('path');
(async () => {
  const [page_, secs, out, from_] = process.argv.slice(2); const fps = 24, n = Math.round(parseFloat(secs) * fps), t0 = parseFloat(from_ || '0');
  const [f, q] = page_.split('?');
  const b = await chromium.launch({ args: ['--allow-file-access-from-files'] }); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', e => { console.error('PAGE ERROR', e.message); process.exitCode = 1; });
  await p.goto('file://' + path.resolve(f) + (q ? '?' + q : '')); await p.evaluate(() => window.ready);
  const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = 0; i < n; i++) {
    const d = await p.evaluate(t => { window.render(t); return document.getElementById('c').toDataURL('image/jpeg', 0.93); }, t0 + i / fps);
    if (!ff.stdin.write(Buffer.from(d.split(',')[1], 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close(); console.log('frames', n);
})();
