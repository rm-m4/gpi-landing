// Render the local pages and report anything broken.
// Fails loudly on 404s, console errors and images that never decoded, then saves a
// full-page screenshot per page for visual comparison against crawl/shots/.
// Usage: node crawl/check.js [page.html ...]

const fs = require('fs');
const path = require('path');
const http = require('http');
const { chromium } = require('playwright-core');

const ROOT = path.join(__dirname, '..');
const OUT = path.join(ROOT, 'crawl', 'local-shots');
const PORT = 8123;

const TYPES = {
  '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg', '.JPG': 'image/jpeg', '.webp': 'image/webp',
  '.gif': 'image/gif', '.ico': 'image/x-icon', '.avif': 'image/avif',
};

// Per-page behaviour assertions.
// 404s, console errors and overflow all stay silent when a <style> or <script>
// block goes missing -- which is exactly what happened when pages/_build.py once
// sliced the shared footer through to </body>. These catch that class of bug:
// each one fails if the page's own CSS or JS is not actually doing its job.

// Shared: a page whose data-reveal blocks never became visible is broken.
async function noneHidden(page) {
  const n = await page.evaluate(() =>
    [...document.querySelectorAll('[data-reveal],[data-r]')].filter(
      (el) => parseFloat(getComputedStyle(el).opacity) < 0.9).length);
  return n ? [`${n} revealed block(s) still at opacity 0`] : [];
}

// The category tablist, on every page that has one.
async function tabChecks(page, expect) {
  const problems = [];
  // Panels hold listing rows on most pages, but issuer cards on fixed deposits.
  const item = expect.item || '.gp-row';
  const inkX = () => page.locator('.gp-tabs__ink').evaluate(
    (el) => new DOMMatrixReadOnly(getComputedStyle(el).transform).m41);
  const ids = await page.locator('.gp-tab').evaluateAll(
    (els) => els.map((e) => e.id.replace(/^tab-/, '')));

  if (ids.length !== expect.count) problems.push(`${ids.length} tabs, expected ${expect.count}`);

  const first = await page.locator(`#panel-${ids[0]} ${item}`).count();
  if (first !== expect.firstRows)
    problems.push(`first panel has ${first} ${item}, expected ${expect.firstRows}`);

  const x0 = await inkX();
  const last = ids[ids.length - 1];
  await page.locator(`#tab-${last}`).click();
  await page.waitForTimeout(700);

  if ((await inkX()) === x0) problems.push('tab indicator did not move');
  if (!(await page.locator(`#panel-${last}`).isVisible())) problems.push('target panel did not open');
  if (await page.locator(`#panel-${ids[0]}`).isVisible()) problems.push('previous panel stayed open');

  await page.locator(`#tab-${last}`).press('ArrowLeft');
  await page.waitForTimeout(400);
  const sel = await page.locator('.gp-tab[aria-selected="true"]').getAttribute('id');
  const want = `tab-${ids[ids.length - 2]}`;
  if (sel !== want) problems.push(`ArrowLeft selected ${sel}, expected ${want}`);

  // Only ever one panel open.
  const open = await page.locator('.gp-panel.is-on').count();
  if (open !== 1) problems.push(`${open} panels open, expected 1`);
  return problems;
}

async function fdChecks(page) {
  const problems = [];
  const maturity = () => page.locator('#fd-maturity').innerText();
  const before = await maturity();
  await page.locator('#fd-amount').fill('1000000');
  await page.locator('#fd-amount').dispatchEvent('input');
  if ((await maturity()) === before) problems.push('FD calculator did not react to input (script missing?)');

  const chip = await page.locator('.fd-chip').first().evaluate((el) => getComputedStyle(el).borderRadius);
  if (parseFloat(chip) < 100) problems.push(`.fd-chip is unstyled (border-radius ${chip}) - page <style> missing?`);
  return problems;
}

async function homeChecks(page) {
  const problems = [];
  const bg = await page.locator('.home-hero').evaluate((el) => getComputedStyle(el).backgroundImage);
  if (bg === 'none') problems.push('.home-hero has no background image - page <style> missing?');
  const rows = await page.locator('.viz-root tbody tr').count();
  if (rows !== 6) problems.push(`chart table view has ${rows} rows, expected 6`);
  return problems;
}

const BEHAVIOUR = {
  // --- live pages -----------------------------------------------------------
  'corporate-bonds.html': async (page) => {
    const problems = await tabChecks(page, { count: 6, firstRows: 4 });
    // The Milestones count-up was replaced by the Golden Experience strip.
    const golden = await page.locator('.gp-stats .gp-stats__item').count();
    if (golden !== 4) problems.push(`Golden Experience strip has ${golden} items, expected 4`);
    return problems.concat(await noneHidden(page));
  },

  'index.html': async (page) => {
    const problems = await tabChecks(page, { count: 6, firstRows: 4 });
    return problems.concat(await homeChecks(page), await noneHidden(page));
  },

  'fixed-deposits.html': async (page) => {
    const problems = await tabChecks(page, { count: 3, firstRows: 3, item: '.gp-card' });
    return problems.concat(await fdChecks(page), await noneHidden(page));
  },

  'bond-ipo-online.html': async (page) => noneHidden(page),

  // --- archives, which keep their original behaviour ------------------------
  'fixed-deposits-old.html': fdChecks,
  'index-old.html': homeChecks,

  // --- design explorations --------------------------------------------------
  'corporate-bonds-taste.html': async (page) => {
    const problems = [];
    const item = page.locator('details.faq__item').first();
    const before = await item.evaluate((e) => e.open);
    await item.locator('summary').click();
    if ((await item.evaluate((e) => e.open)) === before) problems.push('minimal FAQ did not toggle');
    const hidden = await page.evaluate(() =>
      [...document.querySelectorAll('[data-r]')].filter(
        (el) => parseFloat(getComputedStyle(el).opacity) < 0.9).length);
    if (hidden) problems.push(`${hidden} revealed block(s) still at opacity 0`);
    return problems;
  },

  'corporate-bonds-taste2.html': async (page) => {
    const problems = [];
    const d = page.locator('details').first();
    const before = await d.evaluate((e) => e.open);
    await d.locator('summary').click();
    if ((await d.evaluate((e) => e.open)) === before) problems.push('FAQ did not toggle');
    const bez = await page.locator('.bezel').first().evaluate((el) => {
      const core = el.querySelector('.bezel__core');
      return {
        pad: parseFloat(getComputedStyle(el).paddingTop),
        outer: parseFloat(getComputedStyle(el).borderTopLeftRadius),
        inner: core ? parseFloat(getComputedStyle(core).borderTopLeftRadius) : -1,
      };
    });
    if (!(bez.pad > 0 && bez.inner > 0 && bez.inner < bez.outer))
      problems.push(`double-bezel not nesting: ${JSON.stringify(bez)}`);
    return problems.concat(await noneHidden(page));
  },

  'corporate-bonds-taste3.html': async (page) => {
    const problems = [];
    const active = () => page.evaluate(() =>
      [...document.querySelectorAll('.dots button')].findIndex(
        (d) => d.getAttribute('aria-selected') === 'true'));
    const ret = () => page.locator('[data-f="ret"]').innerText();
    const i0 = await active();
    const r0 = await ret();
    await page.locator('.dots button').nth(1).click();
    await page.waitForTimeout(400);
    if ((await active()) === i0) problems.push('carousel dot did not change the active banner');
    if ((await ret()) === r0) problems.push('floating metrics did not swap with the banner');
    const onCount = await page.locator('.slide.is-on').count();
    if (onCount !== 1) problems.push(`${onCount} banners active, expected 1`);
    return problems.concat(await noneHidden(page));
  },
};



// --------------------------------------------------------------- consistency
// The four live pages must read as one design. Behaviour assertions never catch
// this: a page can pass every check and still be missing the shared hero ground
// or listing panel, which is exactly what happened twice. This compares the live
// set against corporate-bonds and reports anything only some of them have.
const LIVE = ['index.html', 'corporate-bonds.html', 'fixed-deposits.html', 'bond-ipo-online.html'];

// Signal -> pages allowed to lack it, with the reason.
const SHARED = {
  '.gp-hero, .home-hero': { exempt: [], why: 'hero ground' },
  '.gp-tabs__track': { exempt: ['bond-ipo-online.html'], why: 'category tabs; this page has none on the live site' },
  '[data-reveal]': { exempt: [], why: 'scroll reveal markup' },
  '.gp-section__head--marked': { exempt: [], why: 'section heading treatment' },
  '.gp-faq': { exempt: [], why: 'FAQ component' },
};

async function consistencyReport(browser, port) {
  const seen = {};
  for (const page of LIVE) {
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
    const pg = await ctx.newPage();
    await pg.goto(`http://localhost:${port}/pages/${page}`, { waitUntil: 'domcontentloaded' });
    seen[page] = {};
    for (const sel of Object.keys(SHARED)) {
      seen[page][sel] = await pg.locator(sel).count();
    }
    // The cream listing panel is a utility combination, not a class.
    seen[page]['cream listing panel'] = await pg
      .locator('.rounded-2xl.border.bg-\\[\\#fdf8e9\\]').count()
      .catch(() => 0);
    await ctx.close();
  }

  const problems = [];
  for (const [sel, rule] of Object.entries(SHARED)) {
    for (const page of LIVE) {
      if (rule.exempt.includes(page)) continue;
      if (!seen[page][sel]) problems.push(`${page} is missing ${sel} (${rule.why})`);
    }
  }
  return problems;
}

// Scroll-reveal animations only fire as sections enter the viewport, so a
// full-page screenshot taken without scrolling captures them still hidden.
// Walk the page first, then return to the top.
async function scrollThrough(page) {
  await page.evaluate(async () => {
    const step = Math.round(window.innerHeight * 0.8);
    for (let y = 0; y < document.body.scrollHeight + step; y += step) {
      window.scrollTo(0, y);
      await new Promise((r) => setTimeout(r, 160));
    }
    window.scrollTo(0, 0);
    await new Promise((r) => setTimeout(r, 400));
  });
}

async function checkAccordion(page) {
  const item = page.locator('details.gp-faq__item').first();
  if (!(await item.count())) return [];
  const before = await item.evaluate((e) => e.open);
  await item.locator('summary').click();
  const after = await item.evaluate((e) => e.open);
  return before === after ? ['FAQ accordion did not toggle'] : [];
}

function chromiumPath() {
  const cache = path.join(process.env.HOME, 'Library/Caches/ms-playwright');
  const builds = fs.readdirSync(cache).filter((d) => /^chromium-\d+$/.test(d))
    .sort((a, b) => Number(a.split('-')[1]) - Number(b.split('-')[1]));
  const dir = path.join(cache, builds[builds.length - 1]);
  for (const rel of [
    'chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing',
    'chrome-mac/Chromium.app/Contents/MacOS/Chromium',
    'chrome-linux/chrome',
  ]) {
    const p = path.join(dir, rel);
    if (fs.existsSync(p)) return p;
  }
  throw new Error('no chromium found');
}

const serve = () =>
  new Promise((res) => {
    const srv = http.createServer((req, rq) => {
      const rel = decodeURIComponent(req.url.split('?')[0]).replace(/^\/+/, '');
      const file = path.join(ROOT, rel);
      if (!file.startsWith(ROOT) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
        rq.writeHead(404).end('not found');
        return;
      }
      rq.writeHead(200, { 'Content-Type': TYPES[path.extname(file)] || 'application/octet-stream' });
      fs.createReadStream(file).pipe(rq);
    });
    srv.listen(PORT, () => res(srv));
  });

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const pages = process.argv.slice(2).length
    ? process.argv.slice(2)
    // Underscore-prefixed files are templates and generators, not pages.
    : fs.readdirSync(path.join(ROOT, 'pages'))
        .filter((f) => f.endsWith('.html') && !f.startsWith('_'));

  const srv = await serve();
  const browser = await chromium.launch({ executablePath: chromiumPath() });
  let problems = 0;

  for (const file of pages) {
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 2 });
    const page = await ctx.newPage();
    const bad = [];
    page.on('console', (m) => { if (m.type() === 'error') bad.push(`console: ${m.text()}`); });
    page.on('pageerror', (e) => bad.push(`pageerror: ${e.message}`));
    page.on('response', (r) => { if (r.status() >= 400) bad.push(`${r.status()} ${r.url()}`); });

    await page.goto(`http://localhost:${PORT}/pages/${file}`, { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(1200);
    await scrollThrough(page);

    // Images that resolved but never produced pixels.
    const broken = await page.evaluate(() =>
      [...document.images].filter((i) => !i.complete || i.naturalWidth === 0).map((i) => i.getAttribute('src')));
    broken.forEach((s) => bad.push(`image did not decode: ${s}`));

    const slug = file.replace(/\.html$/, '');
    // A position:sticky header is painted into every band of a full-page
    // capture, so it appears repeated down the image. Pin it for the shot only.
    // Covers both shells: .gp-header on the shared pages, .top on the standalone
    // minimalist page.
    const unstick = async (p) => p.addStyleTag({ content: '.gp-header,.top,.nav{position:static !important}' });
    await unstick(page);
    await page.screenshot({ path: path.join(OUT, `${slug}-desktop.png`), fullPage: true });

    // Behaviour assertions run after the screenshot, since they mutate the page.
    try {
      bad.push(...(await checkAccordion(page)));
      if (BEHAVIOUR[file]) bad.push(...(await BEHAVIOUR[file](page)));
    } catch (e) {
      bad.push(`behaviour check threw: ${e.message.split('\n')[0]}`);
    }

    // Phone pass in its own context. Resizing an already-rendered page leaves a
    // stale document height behind and Chromium's fullPage capture then stitches
    // the same content twice, so load it fresh at 390px instead.
    const mctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
    const mpage = await mctx.newPage();
    mpage.on('response', (r) => { if (r.status() >= 400) bad.push(`${r.status()} ${r.url()} (mobile)`); });
    await mpage.goto(`http://localhost:${PORT}/pages/${file}`, { waitUntil: 'networkidle', timeout: 60000 });
    await mpage.waitForTimeout(900);
    await scrollThrough(mpage);
    await unstick(mpage);
    await mpage.screenshot({ path: path.join(OUT, `${slug}-mobile.png`), fullPage: true });

    // Horizontal overflow at phone width is the most common responsive break.
    const overflow = await mpage.evaluate(() =>
      document.documentElement.scrollWidth - document.documentElement.clientWidth);
    if (overflow > 2) bad.push(`horizontal overflow at 390px: ${overflow}px`);
    await mctx.close();

    console.log(`${slug.padEnd(20)} ${bad.length ? `${bad.length} PROBLEM(S)` : 'ok'}`);
    bad.slice(0, 12).forEach((b) => console.log(`    ${b}`));
    problems += bad.length;
    await ctx.close();
  }

  // Cross-page consistency, only on a full run.
  if (process.argv.slice(2).length === 0) {
    const drift = await consistencyReport(browser, PORT);
    if (drift.length) {
      console.log('\nconsistency');
      drift.forEach((d) => console.log(`    ${d}`));
      problems += drift.length;
    } else {
      console.log('\nconsistency        the four live pages share the same structure');
    }
  }

  await browser.close();
  srv.close();
  console.log(problems ? `\n${problems} problem(s)` : '\nall clean');
  process.exitCode = problems ? 1 : 0;
})();
