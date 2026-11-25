const { chromium } = require('playwright');
(async () => {
  const [,, url, out, w, full] = process.argv;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: +w, height: +w < 600 ? 844 : 900 }, deviceScaleFactor: +(process.env.DPR||1) });
  const errs=[]; p.on('pageerror', e=>errs.push(e.message)); p.on('console', m=>{if(m.type()==='error')errs.push(m.text())});
  await p.goto(url, { waitUntil: 'networkidle' }).catch(()=>{});
  await p.waitForTimeout(400);
  await p.screenshot({ path: out, fullPage: full === '1' });
  const ov = await p.evaluate(()=>document.documentElement.scrollWidth - window.innerWidth);
  console.log(out, 'overflow', ov, errs.slice(0,3).join(' | '));
  await b.close();
})();
