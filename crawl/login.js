// Log in by hand, once, and keep the session for snap.js.
// The /user/* pages need a session and login is OTP-based, so a person logs in
// in a visible window; this script only waits for a /user/ page and saves the
// cookies and local storage.
// Usage: node crawl/login.js [--prod]
//   then: node crawl/snap.js --auth [--prod] /user/explore ...
// UAT sends you to /signup; production (--prod) opens the homepage, where you
// log in from the header's Login/Sign Up popup. Use mobile/email + OTP: Google
// sign-in refuses automated browsers.
// The session lands in crawl/.auth/, which is git-ignored: it is a live login.

const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright-core');

const PROD = process.argv.includes('--prod');
const HOST = PROD ? 'goldenpi.com' : 'uatnew.goldenpi.com';
const BASE = `https://${HOST}`;
const AUTH = path.join(__dirname, '.auth', PROD ? 'prod.json' : 'uat.json');

// Same lookup as snap.js: the newest cached chromium build.
function chromiumPath() {
  // macOS and Linux cache locations for `npx playwright install chromium`.
  const cache = ['Library/Caches/ms-playwright', '.cache/ms-playwright']
    .map((d) => path.join(process.env.HOME, d)).find((d) => fs.existsSync(d));
  if (!cache) throw new Error('no Chromium found: run `npx playwright install chromium` once');
  const builds = fs.readdirSync(cache).filter((d) => /^chromium-\d+$/.test(d))
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
  const browser = await chromium.launch({ executablePath: chromiumPath(), headless: false });
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  await ctx.addCookies([{ name: 'gp-locale', value: 'en', domain: HOST, path: '/' }]);
  const page = await ctx.newPage();
  await page.goto(PROD ? BASE : `${BASE}/signup?returnUrl=%2Fuser%2Fexplore`);

  console.log(`Log in in the browser window (${HOST}), with mobile/email + OTP.`);
  console.log('If it does not move to a /user/ page by itself, open /user/explore there.');
  console.log('Waiting up to 10 minutes...');
  // Watch every tab, not just the first: a login popup or a new tab would
  // otherwise leave this waiting on a page that has closed.
  const deadline = Date.now() + 10 * 60 * 1000;
  let done = null;
  while (!done) {
    if (Date.now() > deadline) throw new Error('timed out waiting for a /user/ page');
    if (!browser.isConnected()) throw new Error('browser window was closed before login finished');
    done = ctx.pages().find((p) => p.url().includes('/user/'));
    if (!done) await new Promise((r) => setTimeout(r, 1000));
  }
  await done.waitForLoadState('networkidle').catch(() => {});

  fs.mkdirSync(path.dirname(AUTH), { recursive: true });
  await ctx.storageState({ path: AUTH });
  fs.chmodSync(AUTH, 0o600);
  console.log(`Session saved to ${path.relative(process.cwd(), AUTH)}`);
  await browser.close();
})();
