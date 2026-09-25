// Render uatnew.goldenpi.com pages with a real browser.
// Plain curl only returns gp-skeleton placeholders for the data-driven sections;
// the card values (returns, ratings, maturity) exist only after client-side fetch.
// Usage: node crawl/snap.js [/path ...]   (defaults to the batch-1 pages)

const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright-core');

const BASE = 'https://uatnew.goldenpi.com';
const OUT_HTML = path.join(__dirname, 'rendered');
const OUT_SHOTS = path.join(__dirname, 'shots');

const DEFAULT_PAGES = ['/', '/corporate-bonds', '/fixed-deposits', '/bond-ipo-online'];

// Playwright browsers are already cached on this machine; pick the newest chromium build
// rather than hardcoding a version that a future `playwright install` would bump.
function chromiumPath() {
  const cache = path.join(process.env.HOME, 'Library/Caches/ms-playwright');
  const builds = fs
    .readdirSync(cache)
    .filter((d) => /^chromium-\d+$/.test(d))
    .sort((a, b) => Number(a.split('-')[1]) - Number(b.split('-')[1]));
  if (!builds.length) throw new Error(`no cached chromium in ${cache}`);
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

const slugify = (p) => p.replace(/^\/|\/$/g, '').replace(/[/?=&]/g, '_') || 'home';

// Lazy sections mount on intersection, so nothing below the fold renders until scrolled.
async function scrollThrough(page) {
  await page.evaluate(async () => {
    const step = Math.round(window.innerHeight * 0.8);
    for (let y = 0; y < document.body.scrollHeight + step; y += step) {
      window.scrollTo(0, y);
      await new Promise((r) => setTimeout(r, 450));
    }
    window.scrollTo(0, 0);
    await new Promise((r) => setTimeout(r, 600));
  });
}

async function snap(ctx, urlPath) {
  const slug = slugify(urlPath);
  const page = await ctx.newPage();
  await page.goto(BASE + urlPath, { waitUntil: 'networkidle', timeout: 120000 });
  await page.waitForTimeout(2500);
  await scrollThrough(page);
  // A second settle pass: scrolling kicks off a fresh wave of fetches.
  await page.waitForLoadState('networkidle').catch(() => {});
  await page.waitForTimeout(2500);

  const html = await page.content();
  fs.writeFileSync(path.join(OUT_HTML, `${slug}.html`), html);
  await page.screenshot({ path: path.join(OUT_SHOTS, `${slug}-desktop.png`), fullPage: true });

  const skeletons = (html.match(/gp-skeleton/g) || []).length;
  await page.setViewportSize({ width: 390, height: 844 });
  await page.waitForTimeout(1200);
  await scrollThrough(page);
  await page.screenshot({ path: path.join(OUT_SHOTS, `${slug}-mobile.png`), fullPage: true });
  await page.close();

  console.log(`${slug.padEnd(20)} html=${html.length} skeletons=${skeletons}`);
  return skeletons;
}

(async () => {
  fs.mkdirSync(OUT_HTML, { recursive: true });
  fs.mkdirSync(OUT_SHOTS, { recursive: true });
  const pages = process.argv.slice(2).length ? process.argv.slice(2) : DEFAULT_PAGES;

  const browser = await chromium.launch({ executablePath: chromiumPath() });
  const ctx = await browser.newContext({
    viewport: { width: 1440, height: 1000 },
    deviceScaleFactor: 2,
  });
  // Without gp-locale the site 307-redirects `/` to itself forever.
  await ctx.addCookies([
    { name: 'gp-locale', value: 'en', domain: 'uatnew.goldenpi.com', path: '/' },
  ]);

  let left = 0;
  for (const p of pages) {
    try {
      left += await snap(ctx, p);
    } catch (e) {
      console.error(`FAIL ${p}: ${e.message}`);
      process.exitCode = 1;
    }
  }
  await browser.close();
  console.log(`\ntotal skeletons remaining: ${left}`);
})();
