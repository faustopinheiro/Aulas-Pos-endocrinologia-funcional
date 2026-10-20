const { chromium } = require(process.env.PW_PATH || 'playwright');
(async () => {
  const [html, pdf] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + html, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const r = await p.evaluate(() => [...document.querySelectorAll('.page')].map((pg, i) => {
    const inner = pg.querySelector('.inner'); if (!inner) return null;
    const ib = inner.getBoundingClientRect(); let max = 0;
    inner.querySelectorAll('*').forEach(e => { const r = e.getBoundingClientRect(); if (r.height) max = Math.max(max, r.bottom); });
    return { page: i + 1, overflowPx: Math.round(max - ib.bottom) };
  }));
  console.log(JSON.stringify(r.filter(Boolean)));
  console.log('fonts:', await p.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family).filter((v, i, a) => a.indexOf(v) === i).join(',')));
  await p.pdf({ path: pdf, format: 'A4', printBackground: true, preferCSSPageSize: true });
  await b.close();
})();
