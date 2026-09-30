// A headless Chrome holding the saved UAT login, for Lighthouse to attach to:
//   node perf/auth_chrome.js &   then   LH_PORT=9222 node perf/lh.js <pages.json>
// Loads crawl/.auth/uat.json (from crawl/login.js) into a throwaway profile,
// prints whether the session is still valid, then stays up until killed.

const fs = require('fs');
const os = require('os');
const path = require('path');
const { chromium } = require('playwright-core');

const EXE = `${process.env.HOME}/Library/Caches/ms-playwright/chromium-1234/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing`;
const BASE = 'https://uatnew.goldenpi.com';
const state = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'crawl', '.auth', 'uat.json'), 'utf8'));

(async () => {
  const ctx = await chromium.launchPersistentContext(fs.mkdtempSync(path.join(os.tmpdir(), 'lh-auth-')), {
    executablePath: EXE, args: ['--remote-debugging-port=9222'],
  });
  await ctx.addCookies([...state.cookies, { name: 'gp-locale', value: 'en', domain: 'uatnew.goldenpi.com', path: '/' }]);
  const page = await ctx.newPage();
  for (const o of state.origins || []) {
    await page.goto(o.origin + '/robots.txt');
    await page.evaluate((items) => items.forEach(({ name, value }) => localStorage.setItem(name, value)), o.localStorage);
  }
  await page.goto(BASE + '/user/explore', { waitUntil: 'networkidle', timeout: 90000 });
  console.log('session', page.url().includes('/user/') ? 'VALID' : 'EXPIRED', page.url());
  await page.close();
})();
