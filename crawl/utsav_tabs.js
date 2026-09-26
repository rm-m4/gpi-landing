// Drive /bond-utsav's category tabs and record every tab's cards.
// Only the open tab is rendered and each tab lazy-loads as it scrolls, so the
// snap.js capture holds All Bonds alone. -> crawl/rendered/bond-utsav.tabs.json
// Usage: node crawl/utsav_tabs.js

const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright-core');

const CARD = '.bond-utsav-bonds a.gp-secondary-bond-card-link';

function chromiumPath() {
  // macOS and Linux cache locations for `npx playwright install chromium`.
  const cache = ['Library/Caches/ms-playwright', '.cache/ms-playwright']
    .map((d) => path.join(process.env.HOME, d)).find((d) => fs.existsSync(d));
  if (!cache) throw new Error('no Chromium found: run `npx playwright install chromium` once');
  const builds = fs
    .readdirSync(cache)
    .filter((d) => /^chromium-\d+$/.test(d))
    .sort((a, b) => Number(a.split('-')[1]) - Number(b.split('-')[1]));
  if (!builds.length) throw new Error('no Chromium found: run `npx playwright install chromium` once');
  const dir = path.join(cache, builds[builds.length - 1]);
  for (const rel of [
    'chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing',
    'chrome-mac/Chromium.app/Contents/MacOS/Chromium',
    'chrome-linux/chrome',
  ]) {
    const p = path.join(dir, rel);
    if (fs.existsSync(p)) return p;
  }
  throw new Error(`no chromium executable under ${dir}`);
}

(async () => {
  const browser = await chromium.launch({ executablePath: chromiumPath() });
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  // Without gp-locale the site 307-redirects to itself.
  await ctx.addCookies([{ name: 'gp-locale', value: 'en', domain: 'uatnew.goldenpi.com', path: '/' }]);
  const page = await ctx.newPage();
  await page.goto('https://uatnew.goldenpi.com/bond-utsav', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2500);

  const tabs = await page.$$eval('.bond-utsav-tabs__desktop button',
    (bs) => bs.map((b) => [b.dataset.slug, b.textContent.trim()]));
  const out = { captured: new Date().toISOString(), tabs: [] };

  for (const [slug, label] of tabs) {
    await page.click(`.bond-utsav-tabs__desktop button[data-slug="${slug}"]`);
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2500);
    // The next page loads when the last card nears the viewport; a jump to the
    // bottom skips past the sentinel, so walk down from the last card instead.
    let n = -1;
    for (let i = 0; i < 30; i++) {
      const c = await page.$$eval(CARD, (x) => x.length);
      if (c === n && i > 2) break;
      n = c;
      await page.evaluate(async (sel) => {
        const last = [...document.querySelectorAll(sel)].pop();
        if (last) last.scrollIntoView();
        for (let k = 0; k < 6; k++) { window.scrollBy(0, 300); await new Promise((r) => setTimeout(r, 250)); }
      }, CARD);
      await page.waitForTimeout(1500);
    }
    await page.evaluate(() => window.scrollTo(0, 0));

    const cards = await page.$$eval(CARD, (as) => as.map((a) => {
      const q = (s) => (a.querySelector(s)?.textContent || '').replace(/ /g, '').trim();
      const m = [...a.querySelectorAll('.gp-secondary-bond-card__metric-value')].map((x) => x.textContent.trim());
      return {
        href: a.getAttribute('href'),
        logo: a.querySelector('img')?.getAttribute('src'),
        issuer: q('.gp-secondary-bond-card__issuer'),
        tags: [...a.querySelectorAll('.gp-secondary-bond-card__tag')].map((x) => x.textContent.trim()),
        rate: q('.gp-secondary-bond-card__rate-value span'),
        sold: q('.gp-secondary-bond-card__rate-meta'),
        tenure: m[0], payout: m[1], rating: m[2],
        note: q('.gp-secondary-bond-card__urgency-text'),
      };
    }));
    out.tabs.push({ slug, label, count: cards.length, cards });
    console.log(slug.padEnd(36), cards.length);
  }
  fs.writeFileSync(path.join(__dirname, 'rendered', 'bond-utsav.tabs.json'), JSON.stringify(out, null, 1));
  await browser.close();
})();
