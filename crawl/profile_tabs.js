// Capture every section of the logged-in /profile page on uatnew.
// The sidebar swaps the right-hand panel client-side, so each item is clicked
// and the panel's text and markup saved. Needs the session from crawl/login.js.
// Usage: node crawl/profile_tabs.js [outDir] ["Sidebar item"]
// The output holds the account holder's details, so it goes to a directory
// outside the repo by default; content/profile.md is the redacted transcription.

const fs = require('fs');
const os = require('os');
const path = require('path');
const { chromium } = require('playwright-core');

const HOST = 'uatnew.goldenpi.com';
const AUTH = path.join(__dirname, '.auth', 'uat.json');
const OUT = process.argv[2] || fs.mkdtempSync(path.join(os.tmpdir(), 'gp-profile-'));

// Same lookup as snap.js: the newest cached chromium build.
function chromiumPath() {
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

const ITEMS = ['User Details', 'Demat', 'Personal Details', 'Investor Details', 'Bank',
  'Exchange Details', 'Reports And Documents', 'Account Closure', 'Orders', 'Form 121 Center',
  'Portfolio'];
const ONLY = process.argv[3];

// What a plain render leaves closed: FAQ answers, dropdown options and the
// other order tabs.
async function extras(page, item) {
  const main = () => page.evaluate(() => document.querySelector('main').innerText);
  const more = {};
  if (item === 'Form 121 Center') {
    more.faq = [];
    const qs = page.locator('#form121-page-wrap section button[aria-expanded]');
    for (let i = 0; i < await qs.count(); i++) {
      await qs.nth(i).click();
      await page.waitForTimeout(500);
      more.faq.push(await qs.nth(i).locator('xpath=..').innerText());
    }
  }
  if (item === 'Reports And Documents') {
    more.options = {};
    for (const id of ['profile-report-type', 'profile-report-fy']) {
      await page.locator(`#${id}`).click();
      await page.waitForTimeout(500);
      more.options[id] = await page.locator(`#${id}-listbox`).innerText().catch(() => null);
      await page.keyboard.press('Escape');
      await page.waitForTimeout(300);
    }
  }
  if (item === 'Orders') {
    more.orderTabs = {};
    for (const t of ['IPO', 'Fixed Deposit', 'Sovereign Gold Bonds']) {
      await page.getByText(t, { exact: true }).first().click();
      await page.waitForLoadState('networkidle').catch(() => {});
      await page.waitForTimeout(1500);
      more.orderTabs[t] = await main();
      await page.screenshot({ path: path.join(OUT, `orders-${t.toLowerCase().replace(/\W+/g, '-')}.png`), fullPage: true });
    }
  }
  return more;
}

(async () => {
  if (!fs.existsSync(AUTH)) throw new Error('no saved session: run node crawl/login.js first');
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ executablePath: chromiumPath() });
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 1000 }, storageState: AUTH });
  await ctx.addCookies([{ name: 'gp-locale', value: 'en', domain: HOST, path: '/' }]);
  const page = await ctx.newPage();
  await page.goto(`https://${HOST}/profile`, { waitUntil: 'networkidle', timeout: 120000 });
  await page.waitForTimeout(3000);
  if (!/\/profile/.test(page.url())) throw new Error(`redirected to ${page.url()}: session expired, run node crawl/login.js`);

  const out = { url: page.url(), sidebar: null, tabs: {} };
  for (const item of ITEMS.filter((i) => !ONLY || i === ONLY)) {
    const link = page.getByText(item, { exact: true }).first();
    if (!(await link.count())) { out.tabs[item] = null; console.log(`${item}: not in sidebar`); continue; }
    await link.click();
    await page.waitForLoadState('networkidle').catch(() => {});
    await page.waitForTimeout(2000);
    const slug = item.toLowerCase().replace(/\W+/g, '-');
    out.tabs[item] = { url: page.url(), text: await page.evaluate(() => document.body.innerText) };
    Object.assign(out.tabs[item], await extras(page, item));
    fs.writeFileSync(path.join(OUT, `${slug}.html`), await page.content());
    await page.screenshot({ path: path.join(OUT, `${slug}.png`), fullPage: true });
    console.log(`${item}: ${page.url()} ${out.tabs[item].text.length} chars`);
    // Orders, Portfolio and Form 121 are routes of their own; come back for the next item.
    if (!/\/profile/.test(page.url())) {
      await page.goto(`https://${HOST}/profile`, { waitUntil: 'networkidle' });
      await page.getByText('Selected Profile').first().waitFor({ timeout: 30000 });
    }
  }
  fs.writeFileSync(path.join(OUT, ONLY ? 'profile.one.json' : 'profile.tabs.json'), JSON.stringify(out, null, 1));
  await browser.close();
  console.log(`\nsaved to ${OUT}`);
})().catch((e) => { console.error(e.message); process.exit(1); });
