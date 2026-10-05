// Drive goldenpi.com/bond-utsav (production) category tabs and record every
// tab's rows, the 24x7 Order tooltip and both banner images.
// Production is an Angular build with different markup from UAT, hence a
// separate script from utsav_tabs.js. -> crawl/rendered/prod_bond-utsav.tabs.json
// Usage: node crawl/utsav_prod_tabs.js

const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright-core');

const ROW = '.instrument-container .ncd-card-wrapper';

function chromiumPath() {
  const cache = ['Library/Caches/ms-playwright', '.cache/ms-playwright']
    .map((d) => path.join(process.env.HOME, d)).find((d) => fs.existsSync(d));
  const b = fs.readdirSync(cache).filter((d) => /^chromium-\d+$/.test(d))
    .sort((x, y) => Number(x.split('-')[1]) - Number(y.split('-')[1])).pop();
  return ['chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing',
    'chrome-mac/Chromium.app/Contents/MacOS/Chromium', 'chrome-linux/chrome']
    .map((r) => path.join(cache, b, r)).find(fs.existsSync);
}

const banner = (page) => page.$eval('.bond-utsav-container',
  (e) => getComputedStyle(e).backgroundImage.replace(/^url\("?|"?\)$/g, ''));

(async () => {
  const browser = await chromium.launch({ executablePath: chromiumPath() });
  const out = { captured: new Date().toISOString(), source: 'https://goldenpi.com/bond-utsav', tabs: [] };

  const mob = await browser.newPage({ viewport: { width: 390, height: 844 } });
  await mob.goto('https://goldenpi.com/bond-utsav', { waitUntil: 'networkidle' });
  out.bannerMobile = await banner(mob);
  await mob.close();

  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto('https://goldenpi.com/bond-utsav', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2500);
  out.banner = await banner(page);
  out.heading = await page.$eval('.tab-headings', (e) => e.textContent.trim());
  out.subheading = await page.$eval('.tabs-subheadings', (e) => e.textContent.trim());
  out.columns = await page.$$eval('.new-arrival-desktop-column-container .each-detail-heading', (x) => x.map((e) => e.textContent.trim()));

  // The tooltip renders as a popup elsewhere in the DOM; diff the page text.
  const lines = async () => (await page.evaluate(() => document.body.innerText)).split('\n');
  const before = new Set(await lines());
  await page.locator(`${ROW} .amo tooltip-component img`).first().hover();
  await page.waitForTimeout(1200);
  out.tooltip = (await lines()).filter((l) => l.trim() && !before.has(l)).join(' ').trim();
  await page.mouse.move(0, 0);

  const tabs = await page.$$eval('.tab-section', (x) => x.map((e) => ({
    label: e.querySelector('.tab-section-title').textContent.trim(),
    icon: e.querySelector('img').getAttribute('src'),
  })));
  for (let t = 0; t < tabs.length; t++) {
    await page.click(`.tab-section >> nth=${t}`);
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2500);
    let n = -1;
    for (let i = 0; i < 30; i++) {
      const c = await page.$$eval(ROW, (x) => x.length);
      if (c === n && i > 2) break;
      n = c;
      await page.evaluate(async (sel) => {
        [...document.querySelectorAll(sel)].pop()?.scrollIntoView();
        for (let k = 0; k < 6; k++) { window.scrollBy(0, 300); await new Promise((r) => setTimeout(r, 250)); }
      }, ROW);
      await page.waitForTimeout(1500);
    }
    await page.evaluate(() => window.scrollTo(0, 0));
    const rows = await page.$$eval(ROW, (rs) => rs.map((r) => {
      const q = (s) => (r.querySelector(s)?.textContent || '').replace(/\s+/g, ' ').trim();
      return {
        href: r.querySelector('a.ncd-card-stretched-link')?.getAttribute('href'),
        logo: r.querySelector('img.issuer-logo')?.getAttribute('src'),
        issuer: q('.issuer-name'),
        tag: q('.makerting-tag'),
        amo: !!r.querySelector('.amo'),
        rate: q('.coupon span'),
        was: q('.strike-through-yield'),
        rating: q('.credit-rating'),
        ratingColor: r.querySelector('.credit-rating')?.style.color || '',
        maturity: q('.details-container .each-detail:last-of-type .each-detail-data'),
        remaining: q('.remianing-tenure'),
      };
    }));
    const empty = rows.length ? '' : await page.$eval('.no-card-container', (e) => e.innerText.trim());
    out.tabs.push({ ...tabs[t], count: rows.length, empty, rows });
    console.log(tabs[t].label.padEnd(20), rows.length);
  }
  fs.writeFileSync(path.join(__dirname, 'rendered', 'prod_bond-utsav.tabs.json'), JSON.stringify(out, null, 1));
  await browser.close();
})();
