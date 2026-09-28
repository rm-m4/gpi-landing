// Drive uatnew.goldenpi.com/collections/<slug> for every pill on the
// collection page and record what only a browser shows: every bond card
// (lazy, rendered as the list scrolls), the intro after Read More, the count
// line, the sidebar and the page's closing copy.
// -> crawl/rendered/collections.tabs.json, crawl/rendered/collections_<slug>.html
// Usage: node crawl/collections_tabs.js

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

const BASE = 'https://uatnew.goldenpi.com';
const OUT = path.join(__dirname, 'rendered');

async function settle(page) {
  // Scroll until the card count stops growing: the list renders as it scrolls.
  let last = -1;
  for (let i = 0; i < 60; i++) {
    const n = await page.locator('article.collection-bond-card').count();
    if (n === last && i > 3) break;
    last = n;
    await page.evaluate(() => window.scrollBy(0, window.innerHeight));
    await page.waitForTimeout(700);
  }
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(500);
}

(async () => {
  const browser = await chromium.launch({ executablePath: chromiumPath() });
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  await ctx.addCookies([{ name: 'gp-locale', value: 'en', domain: 'uatnew.goldenpi.com', path: '/' }]);
  const page = await ctx.newPage();
  await page.goto(`${BASE}/collections/all-bonds`, { waitUntil: 'networkidle', timeout: 120000 });
  // The pill row is duplicated for mobile and desktop; read the visible one.
  const pills = await page.$$eval('nav[aria-label="Collection filters"] button[data-slug]', (bs) => {
    const seen = new Set();
    return bs.filter((b) => b.offsetParent).map((b) => ({
      slug: b.dataset.slug, label: b.innerText.trim(), icon: b.querySelector('img')?.src || '',
    })).filter((p) => !seen.has(p.slug) && seen.add(p.slug));
  });
  const out = { captured: new Date().toISOString().slice(0, 10), pills, tabs: {} };

  for (const pill of pills) {
    await page.goto(`${BASE}/collections/${pill.slug}`, { waitUntil: 'networkidle', timeout: 120000 });
    await page.waitForTimeout(1500);
    const url = page.url();
    const more = page.locator('button.gp-read-more[aria-expanded="false"]').first();
    if (await more.count()) { await more.click().catch(() => {}); await page.waitForTimeout(400); }
    await settle(page);
    const tab = await page.evaluate(() => {
      const t = (e) => (e ? e.innerText.replace(/\s+/g, ' ').trim() : '');
      const cards = [...document.querySelectorAll('article.collection-bond-card')].map((a) => ({
        href: a.closest('a')?.getAttribute('href') || '',
        issuer: t(a.querySelector('.gp-bond-gold-card__issuer')),
        tags: [...a.querySelectorAll('.gp-bond-gold-card__tag')].map(t),
        rate: t(a.querySelector('.gp-bond-gold-card__rate-value')),
        meta: t(a.querySelector('.gp-bond-gold-card__rate-meta')),
        metrics: [...a.querySelectorAll('.gp-bond-gold-card__metric')].map((m) => [
          t(m.querySelector('.gp-bond-gold-card__metric-label')), t(m.querySelector('.gp-bond-gold-card__metric-value'))]),
        note: t(a.querySelector('.gp-bond-gold-card__urgency')),
      }));
      const intro = document.querySelector('.collection-intro');
      return {
        title: t(document.querySelector('h1')),
        docTitle: document.title,
        metaDesc: document.querySelector('meta[name="description"]')?.content || '',
        introHtml: intro ? intro.innerHTML : '',
        count: t([...document.querySelectorAll('p,span,div')].find((e) => /^Showing \d+ Bonds?$/.test(e.innerText?.trim()))),
        sort: t([...document.querySelectorAll('button,p,span')].find((e) => /^Sort By:/.test(e.innerText?.trim()))),
        empty: t(document.querySelector('.gp-empty-state, [class*="empty"]')),
        cards,
      };
    });
    // The body below the cards is the collection's own CMS copy. FAQs open
    // one at a time, so each is clicked and read in turn.
    const faqs = [];
    const sums = page.locator('.issuer-faq .gp-expand__summary');
    for (let k = 0; k < (await sums.count()); k++) {
      const b = sums.nth(k);
      if ((await b.getAttribute('aria-expanded')) !== 'true') { await b.click().catch(() => {}); await page.waitForTimeout(250); }
      const id = await b.getAttribute('aria-controls');
      faqs.push({
        q: (await b.innerText()).trim(),
        a: await page.evaluate((id) => { const r = document.getElementById(id); const x = r && r.querySelector('.gp-rich-text'); return x ? x.innerHTML : ''; }, id),
      });
    }
    tab.body = await page.evaluate(() => {
      // Every CMS block on the page, in document order, wherever the layout
      // nests it (some collections put copy beside the cards, some below).
      const sel = '.cms-section:not(.collection-intro), .collection-section, .issuer-faq, [class^="cms-link-list"], [class*=" cms-link-list"]';
      const all = [...document.querySelectorAll('.issuer-main ' + sel.split(', ').join(', .issuer-main '))];
      const top = all.filter((e) => !all.some((o) => o !== e && o.contains(e)));
      return top.map((c) => {
        if (c.matches('.collection-section')) return {
          kind: 'article',
          nav: [...c.querySelectorAll('.collection-sidenav__link')].map((a) => [a.getAttribute('href'), a.innerText.trim()]),
          sections: [...c.querySelectorAll('.collection-nav-layout__content--desktop article')].map((a) => ({
            id: a.id, html: (a.querySelector('.gp-rich-text') || a).innerHTML })),
        };
        if (c.matches('.issuer-faq')) {
          const wrap = c.closest('section') || c.parentElement;
          const h = wrap.querySelector('h2:not(.sr-only), h3');
          return { kind: 'faq', title: h ? h.innerText.trim() : '' };
        }
        if (c.matches('.cms-section')) {
          const r = c.querySelector('.gp-rich-text');
          return { kind: 'about', html: r ? r.innerHTML : c.innerHTML };
        }
        return { kind: 'links', text: c.innerText.trim(), html: c.outerHTML.replace(/<svg[\s\S]*?<\/svg>/g, '') };
      });
    });
    tab.faqs = faqs;
    tab.url = url;
    out.tabs[pill.slug] = tab;
    fs.writeFileSync(path.join(OUT, `collections_${pill.slug}.html`), await page.content());
    console.log(pill.slug.padEnd(18), url.replace(BASE, ''), tab.cards.length, tab.count);
  }

  // Page furniture, the same on every pill: read once from all-bonds.
  await page.goto(`${BASE}/collections/all-bonds`, { waitUntil: 'networkidle' });
  await settle(page);
  out.furniture = await page.evaluate(() => {
    const t = (e) => ((e && e.innerText) || '').trim();
    const aside = document.querySelector('aside') || document.querySelector('[class*="sidebar"]');
    const strips = [...document.querySelectorAll('*')].filter((e) => e.children.length && /^The Golden Experience of Investing/.test(t(e))).slice(-1);
    const moreAbout = [...document.querySelectorAll('h2,h3')].find((h) => /More About/i.test(h.innerText));
    return {
      asideText: t(aside), asideHtml: aside ? aside.innerHTML : '',
      stripText: strips[0] ? t(strips[0]) : '', stripHtml: strips[0] ? strips[0].outerHTML : '',
      moreAboutHtml: moreAbout ? moreAbout.parentElement.outerHTML : '',
    };
  });
  fs.writeFileSync(path.join(OUT, 'collections.tabs.json'), JSON.stringify(out, null, 2));
  await browser.close();
})();
