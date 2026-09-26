// Drive /investment-options/list-view and record what only exists after
// interaction: the collapsed filter groups, More Filters, the sort list, and
// every bond row (lazy-loaded as the list scrolls).
// -> crawl/rendered/list-view.ui.json
// Usage: node crawl/listview_ui.js

const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright-core');

const CARD = '.bond-list-page__list .gp-assets-row-card-link-wrap';

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
  await page.goto('https://uatnew.goldenpi.com/investment-options/list-view', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2500);

  // Walk down from the last row until no more load.
  let n = -1;
  for (let i = 0; i < 40; i++) {
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

  const cards = await page.$$eval(CARD, (ws) => ws.map((w) => {
    const q = (s) => (w.querySelector(s)?.textContent || '').replace(/ /g, ' ').trim();
    const metric = (k) => q(`[data-metric="${k}"] .gp-assets-row-card__metric-value`);
    const card = w.querySelector('article');
    return {
      id: (card?.dataset.testid || '').replace('gp-assets-row-card-', ''),
      kind: [...card.classList].find((c) => c.startsWith('gp-assets-row-card--'))?.replace('gp-assets-row-card--', ''),
      href: w.querySelector('a')?.getAttribute('href'),
      logo: w.querySelector('.gp-assets-row-card__logo-img')?.getAttribute('src'),
      issuer: q('.gp-assets-row-card__name'),
      ipoTag: q('.gp-assets-row-card__ipo-tag'),
      closes: q('.gp-assets-row-card__closes-on'),
      minInvestment: metric('minInvestment'),
      yield: metric('yield'),
      payments: metric('payments'),
      tenure: metric('tenure'),
      agency: q('.gp-assets-row-card__rating-agency'),
      grade: q('.gp-assets-row-card__rating-grade'),
      watchlist: !!w.querySelector('[aria-label="Add to watchlist"], [aria-label="Remove from watchlist"]'),
      share: !!w.querySelector('.gp-assets-row-card__share'),
    };
  }));
  console.log('cards', cards.length);

  // Open every collapsed filter group, then More Filters, and read them all.
  for (const t of await page.$$('.bond-list-sidebar .bond-list-accordion__trigger[aria-expanded="false"]')) {
    await t.click();
    await page.waitForTimeout(400);
  }
  const more = await page.$('.bond-list-sidebar__more');
  if (more) {
    await more.click();
    await page.waitForTimeout(800);
    for (const t of await page.$$('.bond-list-sidebar .bond-list-accordion__trigger[aria-expanded="false"]')) {
      await t.click();
      await page.waitForTimeout(400);
    }
  }
  const groups = await page.$$eval('.bond-list-sidebar .bond-list-accordion', (as) => as.map((a) => {
    const panel = a.querySelector('.bond-list-accordion__panel');
    return {
      id: a.querySelector('.bond-list-accordion__trigger')?.getAttribute('aria-controls'),
      title: a.querySelector('.bond-list-accordion__trigger')?.textContent.trim(),
      legend: panel?.querySelector('legend')?.textContent.trim() || '',
      options: [...(panel?.querySelectorAll('label') || [])].map((l) => ({
        id: l.getAttribute('for'),
        type: l.querySelector('input')?.type || '',
        text: l.textContent.replace(/\s+/g, ' ').trim(),
      })),
      // Anything that is not a labelled option (sliders, inputs, notes).
      other: [...(panel?.querySelectorAll('input:not(.bond-list-options__input), [role="slider"], p, small') || [])]
        .map((x) => `${x.tagName.toLowerCase()}${x.type ? '[' + x.type + ']' : ''} ${x.getAttribute('placeholder') || x.getAttribute('aria-label') || x.textContent.trim()}`.trim()),
    };
  }));
  const moreText = await page.$eval('.bond-list-sidebar__more', (b) => b.textContent.trim()).catch(() => '');

  // Sort list.
  await page.click('.bond-list-page__sort .gp-select__trigger');
  await page.waitForTimeout(600);
  const sort = await page.$$eval('[role="listbox"] [role="option"]', (os) => os.map((o) => ({
    text: o.textContent.trim(), selected: o.getAttribute('aria-selected') === 'true',
  })));
  await page.keyboard.press('Escape');

  const help = await page.evaluate(() => {
    const h = [...document.querySelectorAll('h1,h2,h3,h4')].find((x) => /Need Help/.test(x.textContent));
    const box = h?.parentElement?.parentElement;
    return box ? {
      title: h.textContent.trim(),
      text: [...box.querySelectorAll('p')].map((p) => p.textContent.trim()),
      links: [...box.querySelectorAll('a,button')].map((a) => ({ text: a.textContent.trim(), href: a.getAttribute('href') })),
      images: [...box.querySelectorAll('img')].map((i) => i.getAttribute('src')),
    } : null;
  });

  const count = await page.$eval('.bond-list-page__count', (x) => x.textContent.trim());

  // Copy that only exists once filters are applied: the applied line, Clear
  // All, the chips, and the no-results state (AAA plus 11%+ matches nothing).
  await page.click('label[for="bond-list-cr-aaa"]');
  await page.waitForTimeout(2500);
  await page.click('label[for="bond-list-yield-high-returns"]');
  await page.waitForTimeout(3000);
  const states = await page.evaluate(() => {
    const side = document.querySelector('.bond-list-sidebar');
    const main = document.querySelector('.bond-list-page__main');
    const empty = main.querySelector('img[src*="empty-state"]');
    return {
      clear: side.querySelector('.bond-list-sidebar__clear')?.textContent.trim(),
      applied: side.querySelector('.bond-list-sidebar__applied')?.textContent.trim(),
      chips: [...side.querySelectorAll('.bond-list-sidebar__chips li')].map((l) => ({
        text: l.textContent.replace('×', '').trim(),
        remove: l.querySelector('button')?.getAttribute('aria-label'),
      })),
      count: main.querySelector('.bond-list-page__count')?.textContent.trim(),
      emptyIcon: empty?.getAttribute('src'),
      emptyAlt: empty?.getAttribute('alt'),
      emptyText: empty?.closest('[role="status"], div')?.parentElement?.textContent.trim(),
    };
  });

  const out = {
    captured: new Date().toISOString(),
    count,
    sortLabel: 'Sort By',
    sort, groups, moreText, help, states, cards,
    // Phone sheet buttons (bond-list-drawer), read off the live sheet 2026-09-26.
    sheet: { title: 'Filter', clear: 'Clear', apply: 'Apply', sortTitle: 'Sort By' },
  };
  fs.writeFileSync(path.join(__dirname, 'rendered', 'list-view.ui.json'), JSON.stringify(out, null, 1));
  console.log('groups', groups.map((g) => `${g.title}:${g.options.length}`).join(' | '));
  console.log('sort', sort.map((s) => s.text).join(' | '));
  await browser.close();
})();
