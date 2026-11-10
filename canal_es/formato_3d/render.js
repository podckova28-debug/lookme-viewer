// Render: Three.js scene in headless Chromium → frames → ffmpeg, plus the voice-over timeline.
// Usage: node render.js 1080 1920 out_vertical.mp4
const http = require('http'), fs = require('fs'), path = require('path'), {spawn, execFileSync} = require('child_process');
const {chromium} = require('playwright');
const [W, H, OUT] = [+process.argv[2] || 1080, +process.argv[3] || 1920, process.argv[4] || 'out.mp4'];
const FPS = 30, VO = path.join(__dirname, '../ep01/vo_v3');

// Voice-over timeline: line id, pause before it (s)
const LINES = [['s08_01', 0.6], ['s08_02', 0.7], ['s08_03', 1.0], ['s08_04', 0.8], ['s08_05', 0.9], ['s08_06', 0.7]];
const dur = f => +execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).toString();
let t = 0; const at = {};
for (const [id, pause] of LINES) { t += pause; at[id] = t; t += dur(`${VO}/${id}.wav`); }
const END = t + 1.2;
const cues = {freeze: at.s08_02 + 0.15, walk: at.s08_04, arrive: at.s08_05 + 0.8, end: END};

// voice track: each line delayed to its start
const vo = path.join(__dirname, `vo_${W}x${H}.wav`);
execFileSync('ffmpeg', ['-v', 'error', '-y', ...LINES.flatMap(([id]) => ['-i', `${VO}/${id}.wav`]), '-filter_complex',
  LINES.map(([id], i) => `[${i}]adelay=${Math.round(at[id] * 1000)}:all=1[a${i}]`).join(';') + ';' +
  LINES.map((_, i) => `[a${i}]`).join('') + `amix=inputs=${LINES.length}:normalize=0,apad=whole_dur=${END}`, '-ar', '48000', vo]);

const server = http.createServer((q, r) => {
  const p = path.join(__dirname, decodeURIComponent(q.url.split('?')[0]));
  if (!p.startsWith(__dirname) || !fs.existsSync(p)) { r.writeHead(404); return r.end(); }
  r.writeHead(200, {'Content-Type': p.endsWith('.js') ? 'text/javascript' : 'text/html'}); fs.createReadStream(p).pipe(r);
}).listen(0, async () => {
  const port = server.address().port;
  const browser = await chromium.launch({args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist']});
  const page = await browser.newPage({viewport: {width: W, height: H}});
  page.on('pageerror', e => console.error('page error:', e.message));
  await page.goto(`http://127.0.0.1:${port}/scene.html?w=${W}&h=${H}&cues=${encodeURIComponent(JSON.stringify(cues))}`);
  await page.waitForFunction('window.ready === true');
  const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-i', vo,
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest', OUT],
    {stdio: ['pipe', 'inherit', 'inherit']});
  const frames = Math.ceil(END * FPS), t0 = Date.now();
  for (let i = 0; i < frames; i++) {
    await page.evaluate(t => window.renderAt(t), i / FPS);
    const b64 = await page.evaluate(() => document.querySelector('canvas').toDataURL('image/jpeg', 0.92).split(',')[1]);
    if (!ff.stdin.write(Buffer.from(b64, 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 60 === 0) console.log(`frame ${i}/${frames} ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
  await browser.close(); server.close(); fs.unlinkSync(vo);
  console.log(`DONE ${OUT} ${END.toFixed(1)}s video, ${((Date.now() - t0) / 1000).toFixed(0)}s render`, JSON.stringify(cues));
});
