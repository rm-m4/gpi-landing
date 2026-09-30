// DOM size for every known uatnew.goldenpi.com page: element count, depth,
// widest parent and serialized size, after scrolling to trigger lazy sections.
// Mobile (390px) and desktop (1440px). -> perf/<date>/dom-size.json
// Usage: node perf/dom_size.js [outDir]

const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright-core');

const EXE = `${process.env.HOME}/Library/Caches/ms-playwright/chromium-1234/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing`;
const BASE = 'https://uatnew.goldenpi.com';
const OUT = process.argv[2] || path.join(__dirname, new Date().toISOString().slice(0, 10));

const PAGES = [
  '/', '/corporate-bonds', '/fixed-deposits', '/bond-ipo-online', '/bond-utsav',
  '/about-us', '/contact-us', '/careers', '/refer-and-earn', '/signup', '/faq',
  '/privacy-policy', '/terms-and-conditions', '/investment-options/list-view',
  '/issuers/akara-capital-advisors-private-limited',
  ...['all-bonds', 'gold-backed', 'government-bonds', 'high-returns', 'highly-rated', 'monthly-payout',
    'ncd-ipo', 'public-sector-bank-bonds', 'short-term', 'starts-10k', 'tax-free-bonds',
    'best-ongoing-ipos', 'bonds-at-10000', 'bonds-at-discounted-price', 'bonds-maturing-within-a-year',
    'bonds-to-earn-monthly-fixed-income', 'high-yield-bonds', 'highly-rated-bonds', 'newly-launched-bonds',
    'state-government-guranteed-bonds'].map((s) => `/collections/${s}`),
  '/bonds/GPID100072/rec-54ec-bond-525-bond-yield',
  '/fixed-deposits/GPID100016/shriram-finance-limited',
  '/bond-ipo/GPID104322/adani-enterprises-limited',
  '/careers/job-details/product-manager-bangalore-india',
];

// Runs in the page. Counts elements in the document (not iframes).
function measure() {
  let depth = 0, deepest = '', widest = 0, widestSel = '';
  const label = (el) => el.tagName.toLowerCase() + (el.id ? `#${el.id}` : '') +
    (typeof el.className === 'string' && el.className.trim() ? `.${el.className.trim().split(/\s+/)[0]}` : '');
  const walk = (el, d) => {
    if (d > depth) { depth = d; deepest = label(el); }
    if (el.children.length > widest) { widest = el.children.length; widestSel = label(el); }
    for (const c of el.children) walk(c, d + 1);
  };
  walk(document.documentElement, 1);
  const html = document.documentElement.outerHTML;
  return {
    elements: document.getElementsByTagName('*').length,
    depth, deepest, maxChildren: widest, widest: widestSel,
    domKB: Math.round(new Blob([html]).size / 1024),
    svgElements: document.querySelectorAll('svg *').length,
    iframes: document.querySelectorAll('iframe').length,
    scrollHeight: document.documentElement.scrollHeight,
  };
}

(async () => {
  const browser = await chromium.launch({ executablePath: EXE });
  const rows = [];
  for (const p of PAGES) {
    const row = { page: p };
    for (const [key, vp] of [['mobile', { width: 390, height: 844, isMobile: true, hasTouch: true }], ['desktop', { width: 1440, height: 900 }]]) {
      const { width, height, ...rest } = vp;
      const ctx = await browser.newContext({ viewport: { width, height }, ...rest });
      await ctx.addCookies([{ name: 'gp-locale', value: 'en', domain: 'uatnew.goldenpi.com', path: '/' }]);
      const page = await ctx.newPage();
      try {
        const res = await page.goto(BASE + p, { waitUntil: 'networkidle', timeout: 90000 });
        row.status = res.status();
        row.finalUrl = page.url().replace(BASE, '');
        const initial = await page.evaluate(measure);
        // Scroll to the bottom so lazy sections render, then measure again.
        for (let i = 0; i < 40; i++) {
          const done = await page.evaluate(() => { window.scrollBy(0, innerHeight); return innerHeight + scrollY >= document.documentElement.scrollHeight - 2; });
          await page.waitForTimeout(250);
          if (done) break;
        }
        await page.waitForLoadState('networkidle').catch(() => {});
        await page.waitForTimeout(800);
        row[key] = { initial, scrolled: await page.evaluate(measure) };
      } catch (e) { row[key] = { error: e.message.split('\n')[0] }; }
      await ctx.close();
    }
    rows.push(row);
    const m = row.mobile.scrolled || {}, d = row.desktop.scrolled || {};
    console.log(p.padEnd(58), row.status, 'mobile', m.elements, 'desktop', d.elements, 'depth', d.depth);
  }
  fs.mkdirSync(OUT, { recursive: true });
  fs.writeFileSync(path.join(OUT, 'dom-size.json'), JSON.stringify({ captured: new Date().toISOString(), rows }, null, 2));
  await browser.close();
})();
