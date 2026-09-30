// Lab INP probe for uatnew.goldenpi.com: mobile viewport, 4x CPU slowdown, real
// taps on up to three in-page controls (buttons, tabs, accordions; never links,
// so the page does not navigate). Reads Event Timing entries per interaction.
// -> perf/<date>/inp.<name>.json
// Usage: node perf/inp.js <pages.json> [outDir] [storageState.json]

const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright-core');

const EXE = `${process.env.HOME}/Library/Caches/ms-playwright/chromium-1234/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing`;
const BASE = 'https://uatnew.goldenpi.com';
const PAGES = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const OUT = process.argv[3] || path.join(__dirname, new Date().toISOString().slice(0, 10));
const AUTH = process.argv[4];

// Runs in the page before any script: keep the slowest entry per interaction.
function observe() {
  window.__inp = {};
  new PerformanceObserver((list) => {
    for (const e of list.getEntries()) {
      if (!e.interactionId) continue;
      const prev = window.__inp[e.interactionId];
      if (!prev || e.duration > prev.duration) {
        window.__inp[e.interactionId] = {
          type: e.name, duration: e.duration,
          inputDelay: Math.round(e.processingStart - e.startTime),
          processing: Math.round(e.processingEnd - e.processingStart),
          presentation: Math.round(e.startTime + e.duration - e.processingEnd),
        };
      }
    }
  }).observe({ type: 'event', durationThreshold: 16, buffered: true });
}

// Tag up to three visible, tappable, non-navigating controls in the first two screens.
function pick() {
  const out = [];
  const seen = new Set();
  // In-page controls first; the header button goes last because its menu covers the page.
  const els = [...document.querySelectorAll('main [role="tab"], main summary, main [aria-expanded], main button:not([disabled])'),
    ...document.querySelectorAll('header button:not([disabled])')];
  for (const el of els) {
    if (el.closest('a[href]') || el.type === 'submit') continue;
    const r = el.getBoundingClientRect();
    if (r.width < 24 || r.height < 24 || r.top < 0 || r.top > innerHeight * 2 || r.left < 0 || r.right > innerWidth) continue;
    const label = (el.getAttribute('aria-label') || el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40);
    const kind = el.closest('header') ? 'header button' : el.getAttribute('role') === 'tab' ? 'tab' : el.tagName === 'SUMMARY' || el.hasAttribute('aria-expanded') ? 'toggle' : 'button';
    if (!label || seen.has(kind)) continue; // one of each kind, for variety
    seen.add(kind);
    el.setAttribute('data-inp-probe', String(out.length));
    out.push({ kind, label });
    if (out.length === 3) break;
  }
  return out;
}

(async () => {
  const browser = await chromium.launch({ executablePath: EXE });
  const rows = [];
  for (const { slug, path: p } of PAGES) {
    const ctx = await browser.newContext({
      viewport: { width: 412, height: 823 }, isMobile: true, hasTouch: true, deviceScaleFactor: 1.75,
      ...(AUTH ? { storageState: AUTH } : {}),
    });
    await ctx.addCookies([{ name: 'gp-locale', value: 'en', domain: 'uatnew.goldenpi.com', path: '/' }]);
    const page = await ctx.newPage();
    await page.addInitScript(observe);
    const row = { slug, path: p, taps: [] };
    try {
      // Some logged-in pages poll and never go network-idle; settle for load plus a bounded wait.
      await page.goto(BASE + p, { waitUntil: 'load', timeout: 90000 });
      await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
      row.finalUrl = page.url().replace(BASE, '');
      const cdp = await ctx.newCDPSession(page);
      await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
      const targets = await page.evaluate(pick);
      for (let i = 0; i < targets.length; i++) {
        const before = await page.evaluate(() => Object.keys(window.__inp));
        const loc = page.locator(`[data-inp-probe="${i}"]`);
        try {
          await loc.scrollIntoViewIfNeeded({ timeout: 3000 });
          await loc.tap({ timeout: 3000 });
        } catch (e) { row.taps.push({ ...targets[i], error: e.message.split('\n')[0] }); continue; }
        await page.waitForTimeout(1500);
        if (page.url().replace(BASE, '') !== row.finalUrl) {
          // The control was a navigation. Come back, re-tag the same controls and carry on.
          row.taps.push({ ...targets[i], error: 'navigated' });
          await page.goto(BASE + p, { waitUntil: 'load', timeout: 90000 });
          await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
          await page.evaluate(pick);
          continue;
        }
        const after = await page.evaluate(() => window.__inp);
        const fresh = Object.entries(after).filter(([id]) => !before.includes(id)).map(([, v]) => v);
        const worst = fresh.sort((a, b) => b.duration - a.duration)[0];
        // No entry means the interaction finished under the 16 ms reporting floor.
        row.taps.push({ ...targets[i], ...(worst || { duration: 16, under16: true }) });
      }
    } catch (e) { row.error = e.message.split('\n')[0]; }
    await ctx.close();
    rows.push(row);
    console.log(slug.padEnd(34), row.error || row.taps.map((t) => `${t.kind}:${t.error || t.duration}`).join('  ') || 'no tappable control');
  }
  fs.mkdirSync(OUT, { recursive: true });
  fs.writeFileSync(path.join(OUT, `inp.${path.basename(process.argv[2], '.json')}.json`), JSON.stringify({ captured: new Date().toISOString(), rows }, null, 2));
  await browser.close();
})();
