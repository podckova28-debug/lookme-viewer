const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:2560,height:1440}});
const bg='data:image/png;base64,'+fs.readFileSync(process.argv[2]).toString('base64');
const font=fs.readFileSync(process.argv[3]).toString('base64');
await p.setContent(`<style>@font-face{font-family:"MontX";src:url(data:font/ttf;base64,${font}) format("truetype")}body{margin:0;width:2560px;height:1440px;position:relative;overflow:hidden;font-family:"Montserrat","Montserrat Thin ExtraBold",Arial;font-weight:800;color:#fff}
.bg{position:absolute;inset:0;background:url(${bg}) center/cover}
.tint{position:absolute;inset:0;background:linear-gradient(90deg,rgba(20,24,60,0) 35%,rgba(20,24,60,.55) 58%,rgba(20,24,60,.7))}
.safe{position:absolute;left:507px;top:508px;width:1546px;height:423px;display:flex;align-items:center;justify-content:flex-end;text-align:right}
h1{font-size:124px;margin:0;line-height:1;letter-spacing:-1px;text-shadow:0 4px 18px rgba(0,0,0,.45)}
p{font-size:48px;margin:16px 0 0;opacity:.95;text-shadow:0 2px 10px rgba(0,0,0,.5)}
.chip{display:inline-block;margin-top:24px;padding:12px 30px;border-radius:999px;background:#63E7A5;color:#202020;font-size:34px}
</style><div class="bg"></div><div class="tint"></div>
<div class="safe"><div><h1>Мерлиоша<br>объясняет</h1><p>Бытовая техника изнутри. Сейчас разберёмся.</p><span class="chip">новый выпуск каждую неделю</span></div></div>`);
await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(300);
await p.screenshot({path:process.argv[4]});await b.close();})();
