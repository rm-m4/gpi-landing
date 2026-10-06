// Render uatnew.goldenpi.com pages with a real browser.
// Plain curl only returns gp-skeleton placeholders for the data-driven sections;
// the card values (returns, ratings, maturity) exist only after client-side fetch.
// Usage: node crawl/snap.js [--auth] [--prod] [/path ...]   (defaults to the batch-1 pages)
// --auth loads the session crawl/login.js saved, for the logged-in /user/* pages.
// It is opt-in: public pages render differently when logged in.

const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright-core');

// --prod captures goldenpi.com instead, for pages UAT does not have. Its files
// get a prod_ prefix so they never overwrite the UAT capture of the same path.
const PROD = process.argv.includes('--prod');
// --beta captures beta.goldenpi.com, prefixed beta_ for the same reason.
const BETA = process.argv.includes('--beta');
const HOST = PROD ? 'goldenpi.com' : BETA ? 'beta.goldenpi.com' : 'uatnew.goldenpi.com';
const BASE = `https://${HOST}`;
const OUT_HTML = path.join(__dirname, 'rendered');
const OUT_SHOTS = path.join(__dirname, 'shots');

const DEFAULT_PAGES = ['/', '/corporate-bonds', '/fixed-deposits', '/bond-ipo-online'];

// Pick the newest cached chromium build
// rather than hardcoding a version that a future `playwright install` would bump.
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

const slugify = (p) => (PROD ? 'prod_' : BETA ? 'beta_' : '')
  + (p.replace(/\?.*$/, '').replace(/^\/|\/$/g, '').replace(/[/?=&]/g, '_') || 'home');

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

// Logged-in pages show the account holder. The captures are a design handoff,
// so personal details are swapped for placeholders in the live DOM (text,
// attributes and inline script state alike) before anything is saved or
// screenshotted. Returns what it replaced, so the saved file can be verified.
const PUBLIC_EMAILS = ['contact-us@goldenpi.com', 'grievance-gspl@goldenpi.com'];

async function redact(page) {
  return page.evaluate((publicEmails) => {
    const found = new Set();
    const greet = document.body.innerText.match(/\bHi ([A-Z][A-Za-z]+)\b/);
    const name = greet ? greet[1] : null;
    const rules = [
      [/\b[6-9]\d{9}\b/g, () => '9000000000'],
      [/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g,
        // "LIMITED@2x.png" is a retina image name, not an address.
        (m) => (publicEmails.includes(m.toLowerCase()) || /\.(png|jpe?g|svg|webp|gif|avif)$/i.test(m)
          ? m : 'investor@example.com')],
    ];
    if (name && name !== 'INVESTOR') rules.unshift([new RegExp('\\b' + name + '\\b', 'gi'), () => 'INVESTOR']);
    const fix = (v) => {
      let out = v;
      for (const [re, to] of rules) out = out.replace(re, (m) => { if (to(m) !== m) found.add(m); return to(m); });
      return out;
    };
    const walker = document.createTreeWalker(document.documentElement, NodeFilter.SHOW_TEXT);
    let n;
    while ((n = walker.nextNode())) { const v = fix(n.nodeValue); if (v !== n.nodeValue) n.nodeValue = v; }
    for (const el of document.querySelectorAll('*')) {
      for (const a of [...el.attributes]) { const v = fix(a.value); if (v !== a.value) el.setAttribute(a.name, v); }
    }
    // Production asks for the MPIN on every new session with a full-screen
    // lock over the page. It is not page content, so hide it for the shots.
    const lock = [...document.querySelectorAll('body *')].find(
      (e) => e.children.length === 0 && /ENTER MPIN/.test(e.textContent));
    for (let e = lock; e; e = e.parentElement) {
      if (getComputedStyle(e).position === 'fixed') { e.style.display = 'none'; break; }
    }
    document.body.style.overflow = 'auto';
    // The header avatar carries initials, which no pattern above catches.
    document.querySelectorAll('.header-initial').forEach((el) => {
      if (el.textContent.trim() !== 'IN') { found.add(el.textContent.trim()); el.textContent = 'IN'; }
    });
    return [...found];
  }, PUBLIC_EMAILS);
}

async function snap(ctx, urlPath, auth) {
  const slug = slugify(urlPath);
  const page = await ctx.newPage();
  await page.goto(BASE + urlPath, { waitUntil: 'networkidle', timeout: 120000 });
  if ((/\/signup/.test(page.url()) && !urlPath.startsWith('/signup')) || (urlPath.startsWith('/user/') && !page.url().includes('/user/'))) {
    await page.close();
    throw new Error(`redirected to ${page.url()}: session missing or expired, run node crawl/login.js${PROD ? ' --prod' : ''}`);
  }
  await page.waitForTimeout(2500);
  await scrollThrough(page);
  // A second settle pass: scrolling kicks off a fresh wave of fetches.
  await page.waitForLoadState('networkidle').catch(() => {});
  await page.waitForTimeout(2500);

  const secrets = auth ? await redact(page) : [];
  const html = await page.content();
  // Initials are too short to search for safely; everything else must be gone.
  const leaked = secrets.filter((v) => v.length > 3 && html.toLowerCase().includes(v.toLowerCase()));
  if (leaked.length) throw new Error(`redaction left ${leaked.length} value(s) in the HTML; nothing saved`);
  fs.writeFileSync(path.join(OUT_HTML, `${slug}.html`), html);
  if (auth) await redact(page);
  await page.screenshot({ path: path.join(OUT_SHOTS, `${slug}-desktop.png`), fullPage: true });

  const skeletons = (html.match(/gp-skeleton/g) || []).length;
  await page.setViewportSize({ width: 390, height: 844 });
  await page.waitForTimeout(1200);
  await scrollThrough(page);
  if (auth) await redact(page);
  await page.screenshot({ path: path.join(OUT_SHOTS, `${slug}-mobile.png`), fullPage: true });
  await page.close();

  console.log(`${slug.padEnd(20)} html=${html.length} skeletons=${skeletons}`);
  return skeletons;
}

(async () => {
  fs.mkdirSync(OUT_HTML, { recursive: true });
  fs.mkdirSync(OUT_SHOTS, { recursive: true });
  const args = process.argv.slice(2);
  const auth = args.includes('--auth');
  const paths = args.filter((a) => !a.startsWith('--'));
  const pages = paths.length ? paths : DEFAULT_PAGES;
  const AUTH = path.join(__dirname, '.auth', PROD ? 'prod.json' : 'uat.json');
  if (auth && !fs.existsSync(AUTH)) throw new Error('no saved session: run node crawl/login.js first');

  const browser = await chromium.launch({ executablePath: chromiumPath() });
  const ctx = await browser.newContext({
    viewport: { width: 1440, height: 1000 },
    deviceScaleFactor: 2,
    ...(auth ? { storageState: AUTH } : {}),
  });
  // Without gp-locale the site 307-redirects `/` to itself forever.
  await ctx.addCookies([
    { name: 'gp-locale', value: 'en', domain: HOST, path: '/' },
  ]);

  let left = 0;
  for (const p of pages) {
    try {
      left += await snap(ctx, p, auth);
    } catch (e) {
      console.error(`FAIL ${p}: ${e.message}`);
      process.exitCode = 1;
    }
  }
  await browser.close();
  console.log(`\ntotal skeletons remaining: ${left}`);
})();
