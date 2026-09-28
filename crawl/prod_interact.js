// Drive the four production product/company pages for copy that only exists
// after interaction: media "SEE MORE" pages, tooltip text, Closed IPOs, the
// "Why invest in Bonds?" video. -> crawl/rendered/prod_interact.json
// plus crawl/rendered/prod_<slug>.expanded.html
// Usage: node crawl/prod_interact.js

const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright-core');

function chromiumPath() {
  const cache = ['Library/Caches/ms-playwright', '.cache/ms-playwright']
    .map((d) => path.join(process.env.HOME, d)).find((d) => fs.existsSync(d));
  if (!cache) throw new Error('no Chromium found: run `npx playwright install chromium` once');
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
  throw new Error(`no chromium executable under ${dir}`);
}

const OUT = path.join(__dirname, 'rendered');
const text = (s) => s.replace(/\s+/g, ' ').trim();

// Hover every tooltip trigger and read whatever new text appears.
async function tooltips(page) {
  const out = [];
  const tips = await page.$$('tooltip-component');
  for (const t of tips) {
    if (!(await t.isVisible())) continue;
    const label = text(await t.evaluate((e) => (e.closest('li,span,td,div,p') || e).innerText));
    await t.scrollIntoViewIfNeeded();
    await t.hover().catch(() => {});
    await page.waitForTimeout(400);
    // The tooltip mounts a <tool-tip-bond-details> in a popup outside the trigger.
    const tip = await page.$$eval('tool-tip-bond-details', (els) => els
      .filter((e) => e.getClientRects().length).map((e) => e.innerText.trim()).filter(Boolean));
    out.push({ label, tip: [...new Set(tip.map(text))] });
    await page.mouse.move(0, 0);
    await page.keyboard.press('Escape');
    await page.waitForTimeout(300);
  }
  return out;
}

(async () => {
  const browser = await chromium.launch({ executablePath: chromiumPath() });
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  await ctx.addCookies([{ name: 'gp-locale', value: 'en', domain: 'goldenpi.com', path: '/' }]);
  const res = {};
  for (const slug of ['media', 'sovereign-gold-bond', 'government-securities', 'bond-better-return-fds']) {
    const page = await ctx.newPage();
    await page.goto(`https://goldenpi.com/${slug}`, { waitUntil: 'networkidle', timeout: 120000 });
    await page.waitForTimeout(2500);
    const r = (res[slug] = {});
    if (slug === 'media') {
      for (let i = 0; i < 40; i++) {
        const more = page.locator('p.see-more');
        if (!(await more.count()) || !(await more.first().isVisible())) break;
        const before = await page.locator('media-coverage a').count();
        await more.first().click();
        await page.waitForTimeout(1500);
        if ((await page.locator('media-coverage a').count()) === before) break;
      }
      r.cards = await page.$$eval('media-coverage a', (as) => as.map((a) => ({
        href: a.href,
        img: a.querySelector('img')?.src,
        texts: [...a.querySelectorAll('h1,h2,h3,h4,h5,h6,p')].map((p) => p.innerText.replace(/\s+/g, ' ').trim()),
      })));
      r.seeMoreLeft = await page.locator('p.see-more').count();
    } else {
      r.tooltips = await tooltips(page);
    }
    if (slug === 'bond-better-return-fds') {
      await page.locator('closed-ipo .heading-container').click();
      await page.waitForTimeout(2500);
      r.closedIpos = text(await page.locator('closed-ipo').innerText());
      r.closedIpoHtml = await page.locator('closed-ipo').innerHTML();
      const vid = page.locator('text=Why invest in Bonds?').first();
      if (await vid.count()) {
        await vid.click().catch(() => {});
        await page.waitForTimeout(1500);
        r.iframes = await page.$$eval('iframe', (f) => f.map((x) => x.src).filter(Boolean));
      }
      await page.keyboard.press('Escape');
      // Learn about Bonds cards open videos/posts from click handlers.
      r.learn = [];
      const cards = page.locator('learn-about-bonds-ncd .each-blog');
      for (let i = 0; i < (await cards.count()); i++) {
        const [popup] = await Promise.all([
          ctx.waitForEvent('page', { timeout: 4000 }).catch(() => null),
          cards.nth(i).click().catch(() => {}),
        ]);
        await page.waitForTimeout(1500);
        r.learn.push({
          url: popup ? popup.url() : page.url(),
          iframes: await page.$$eval('iframe', (f) => f.map((x) => x.src).filter((s) => /youtu|vimeo/.test(s))),
        });
        if (popup) await popup.close();
        if (!page.url().includes(slug)) await page.goBack();
        await page.keyboard.press('Escape');
        await page.waitForTimeout(500);
      }
    }
    fs.writeFileSync(path.join(OUT, `prod_${slug}.expanded.html`), await page.content());
    await page.close();
    console.log(slug, JSON.stringify(r).length);
  }
  fs.writeFileSync(path.join(OUT, 'prod_interact.json'), JSON.stringify(res, null, 2));
  await browser.close();
})();
