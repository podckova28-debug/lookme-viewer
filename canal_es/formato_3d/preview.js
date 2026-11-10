// Quick check: a few stills at half size. node preview.js
const http=require('http'),fs=require('fs'),path=require('path');const {chromium}=require('playwright');
fs.mkdirSync(path.join(__dirname,'preview'),{recursive:true});
const s=http.createServer((q,r)=>{const p=path.join(__dirname,q.url.split('?')[0]);if(!fs.existsSync(p)){r.writeHead(404);return r.end()}r.writeHead(200,{'Content-Type':p.endsWith('.js')?'text/javascript':'text/html'});fs.createReadStream(p).pipe(r)}).listen(0,async()=>{
 const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
 for(const [w,h] of [[540,960],[960,540]]){const pg=await b.newPage({viewport:{width:w,height:h}});pg.on('pageerror',e=>console.error('ERR',e.message));
  await pg.goto(`http://127.0.0.1:${s.address().port}/scene.html?w=${w}&h=${h}`);await pg.waitForFunction('window.ready===true');
  for(const t of [1,2.6,5,8,11]){const t0=Date.now();await pg.evaluate(t=>renderAt(t),t);await pg.screenshot({path:`preview/${w}x${h}_t${t}.png`});console.log(w,h,t,Date.now()-t0,'ms')}}
 await b.close();s.close()});
