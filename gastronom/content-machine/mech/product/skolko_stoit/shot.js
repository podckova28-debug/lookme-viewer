const { chromium } = require('playwright');
const D = process.argv[2];
(async () => {
  const b = await chromium.launch();
  for (const [scheme, w] of [['light', 390], ['dark', 390], ['light', 820]]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 }, colorScheme: scheme });
    const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    await p.goto('file://' + D + '/page/mihalych_cost.html'); await p.waitForTimeout(700);
    const sw = await p.evaluate(() => document.documentElement.scrollWidth);
    const H = await p.evaluate(() => document.documentElement.scrollHeight);
    console.log(scheme, w, 'scrollWidth', sw, 'height', H, 'errors', errs.filter(e => !/fonts\.g/.test(e)));
    await p.screenshot({ path: `${D}/page/v3_${scheme}_${w}.png`, fullPage: true });
  }
  await b.close();
})();
