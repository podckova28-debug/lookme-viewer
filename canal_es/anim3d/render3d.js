// Render a stylized 3D shot: node render3d.js PAGE.html OUT.mp4 SECONDS [CUES_JSON] [AUDIO.wav]
// Serves canal_es/ over http (ES modules need it), renders window.render(t) at 24 fps with WebGL (SwiftShader) into ffmpeg.
const http = require('http'), fs = require('fs'), path = require('path'), { spawn } = require('child_process'), { chromium } = require('playwright');
const [PAGE, OUT, SECS, CUES = '{}', AUDIO] = process.argv.slice(2), ROOT = path.resolve(__dirname, '..'), FPS = 24;
const TYPES = { '.js': 'text/javascript', '.html': 'text/html', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.ttf': 'font/ttf' };
const server = http.createServer((q, r) => { const p = path.join(ROOT, decodeURIComponent(q.url.split('?')[0]));
  if (!p.startsWith(ROOT) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { r.writeHead(404); return r.end(); }
  r.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(r); }).listen(0, async () => {
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', e => { console.error('PAGE ERROR', e.message); process.exitCode = 1; }); p.on('console', m => { if (m.type() === 'error') console.error('console', m.text()); });
  const rel = path.relative(ROOT, path.resolve(PAGE)).split(path.sep).join('/');
  await p.goto(`http://127.0.0.1:${server.address().port}/${rel}?hyb=1&cues=${encodeURIComponent(CUES)}`); await p.waitForFunction('window.ready === true', null, { timeout: 120000 });
  const args = ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-'];
  if (AUDIO) args.push('-i', AUDIO, '-c:a', 'aac', '-b:a', '192k', '-shortest');
  const ff = spawn('ffmpeg', [...args, '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', OUT], { stdio: ['pipe', 'inherit', 'inherit'] });
  const n = Math.round(parseFloat(SECS) * FPS), t0 = Date.now();
  for (let i = 0; i < n; i++) {
    const d = await p.evaluate(t => { window.render(t); return document.getElementById('c').toDataURL('image/jpeg', .93); }, i / FPS);
    if (!ff.stdin.write(Buffer.from(d.split(',')[1], 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 48 === 0) console.log(`frame ${i}/${n} ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close(); server.close(); console.log('done', OUT, ((Date.now() - t0) / 1000).toFixed(0) + 's');
});
