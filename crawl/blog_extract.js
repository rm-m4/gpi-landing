// Read the blog captures (goldenpi.com/blog, a WordPress + Soledad site) into JSON.
// Input: crawl/rendered/prod_blog*.html from `node crawl/snap.js --prod /blog/ ...`.
// Output: crawl/rendered/prod_blog.json (landing) and prod_blog_post.json (article),
// plus content/prod_blog*.md for review against the screenshots.
// Thumbnails go through their resizer (gpi-img.php?u=<cloudfront url>); the original
// CloudFront URL is kept so crawl/blog_images.sh can fetch it.
// Usage: node crawl/blog_extract.js

const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright-core');

const R = path.join(__dirname, 'rendered');
const PAGES = {
  landing: 'prod_blog.html',
  post: 'prod_blog_fixed-deposit_hdfc-bank-fixed-deposits-fds-and-interest-rates.html',
};

function chromiumPath() {
  const cache = ['Library/Caches/ms-playwright', '.cache/ms-playwright']
    .map((d) => path.join(process.env.HOME, d)).find((d) => fs.existsSync(d));
  const b = fs.readdirSync(cache).filter((d) => /^chromium-\d+$/.test(d))
    .sort((x, y) => x.split('-')[1] - y.split('-')[1]).pop();
  return ['chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing',
    'chrome-mac/Chromium.app/Contents/MacOS/Chromium', 'chrome-linux/chrome']
    .map((r) => path.join(cache, b, r)).find(fs.existsSync);
}

// Runs in the page. Shared helpers are defined inline so each evaluate is standalone.
const HELPERS = `
  const T = (el) => (el ? el.textContent.replace(/\\s+/g, ' ').trim() : '');
  const img = (el) => {
    if (!el) return '';
    const raw = el.getAttribute('data-bgset') || el.getAttribute('data-src') || el.getAttribute('src')
      || ((el.getAttribute('style') || '').match(/url\\(['"]?([^'")]+)/) || [])[1] || '';
    const m = raw.match(/[?&]u=([^&]+)/);
    return m ? decodeURIComponent(m[1]) : raw;
  };
  const card = (el) => {
    const a = el.querySelector('.entry-title a, h2 a, h3 a');
    return {
      title: T(a), href: a ? a.href : '',
      img: img(el.querySelector('.penci-image-holder, img')),
      author: T(el.querySelector('.author-url')),
      authorHref: (el.querySelector('.author-url') || {}).href || '',
      date: T(el.querySelector('time')),
      datetime: (el.querySelector('time') || { getAttribute: () => '' }).getAttribute('datetime'),
      excerpt: T(el.querySelector('.mag-excerpt, .entry-excerpt')),
    };
  };
  // Inline HTML reduced to the tags an article needs; every attribute dropped but href.
  const clean = (el) => {
    const c = el.cloneNode(true);
    c.querySelectorAll('script,style,noscript,.ez-toc-section,.ez-toc-section-end,#ez-toc-container').forEach((n) => n.remove());
    const keep = new Set(['STRONG','B','EM','I','A','BR','SPAN','SUP','SUB']);
    const walk = (n) => {
      for (const k of [...n.children]) {
        walk(k);
        if (!keep.has(k.tagName)) { k.replaceWith(...k.childNodes); continue; }
        if (k.tagName === 'SPAN' || k.tagName === 'I' && !k.textContent.trim()) { k.replaceWith(...k.childNodes); continue; }
        const href = k.getAttribute('href');
        [...k.attributes].forEach((a) => k.removeAttribute(a.name));
        if (href) k.setAttribute('href', href);
      }
    };
    walk(c);
    return c.innerHTML.replace(/\\s+/g, ' ').replace(/&nbsp;/g, ' ').trim();
  };
  const menu = () => [...document.querySelectorAll('#navigation .menu > li, .main-navigation .menu > li')].slice(0, 12).map((li) => ({
    label: T(li.querySelector(':scope > a')), href: (li.querySelector(':scope > a') || {}).href || '',
    children: [...li.querySelectorAll(':scope > ul > li > a')].map((a) => ({ label: T(a), href: a.href })),
  }));
`;

const LANDING = `${HELPERS}
  const slides = [...document.querySelectorAll('.penci-owl-featured-area .swiper-slide')].map((s) => {
    const a = s.querySelector('h2 a, h3 a');
    return { title: T(a), href: a ? a.href : '', img: img(s.querySelector('.penci-image-holder, img')),
      cats: [...s.querySelectorAll('.featured-cat a')].map((c) => ({ label: T(c), href: c.href })),
      date: T(s.querySelector('time')) };
  });
  const sections = [...document.querySelectorAll('section.home-featured-cat')].map((s) => {
    const more = s.querySelector('.penci-featured-cat-seemore a');
    return {
      name: T(s.querySelector('.penci-homepage-title .inner-arrow > span > span, .inner-arrow')),
      layout: s.className.includes('style-1') && !s.className.includes('style-13') ? 'lead+list' : 'grid',
      more: more ? more.href : '', moreLabel: more ? T(more).replace(T(more.querySelector('.screen-reader-text')), '').trim() : '',
      posts: [...s.querySelectorAll('article.item, .mag-post-box')].map(card),
    };
  });
  return { title: document.title, h1: T(document.querySelector('h1')), menu: menu(), slides, sections };
`;

const POST = `${HELPERS}
  const art = document.querySelector('article.post');
  const entry = art.querySelector('.inner-post-entry');
  const blocks = [];
  for (const el of entry.children) {
    const cls = el.className || '';
    if (el.tagName === 'P') { const h = clean(el); if (h) blocks.push({ type: 'p', html: h }); }
    else if (/^H[2-4]$/.test(el.tagName)) blocks.push({ type: el.tagName.toLowerCase(), text: T(el), id: (el.querySelector('.ez-toc-section') || {}).id || '' });
    else if (el.tagName === 'UL' && cls.includes('latest-posts')) blocks.push({ type: 'latest', posts: [...el.querySelectorAll('li')].map((li) => ({ title: T(li.querySelector('a.wp-block-latest-posts__post-title, a:not(:has(img))')), href: (li.querySelector('a') || {}).href, img: img(li.querySelector('img')) })) });
    else if (el.tagName === 'UL' || el.tagName === 'OL') blocks.push({ type: el.tagName.toLowerCase(), items: [...el.children].map(clean) });
    else if (el.tagName === 'FIGURE' && el.querySelector('table')) {
      const rows = [...el.querySelectorAll('tr')].map((tr) => [...tr.children].map((td) => ({ text: T(td), tag: td.tagName.toLowerCase(), colspan: td.colSpan, rowspan: td.rowSpan })));
      blocks.push({ type: 'table', rows });
    }
    else if (cls.includes('gpi-custom-widget-box')) {
      const toc = [...el.querySelectorAll('#ez-toc-container a')].map((a) => ({ label: T(a), href: a.getAttribute('href') }));
      const content = el.querySelector('.gpi-custom-widget-content') || [...el.querySelectorAll(':scope > p')];
      blocks.push({ type: 'box', title: T(el.querySelector('.gpi-custom-widget-title')),
        html: content.nodeType ? clean(content) : content.map(clean).join('</p><p>'),
        links: content.nodeType ? [...content.querySelectorAll('a')].map((a) => ({ label: T(a), href: a.href })) : [],
        toc, tocTitle: T(el.querySelector('.ez-toc-title')) });
    }
    else if (cls.includes('ad-container')) {
      const hd = el.querySelector('.ad-headline-div');
      blocks.push({ type: 'ad', badge: T(el.querySelector('.ad-content > span')),
        head: T(hd).replace(T(hd.querySelector('span')), '').trim(), accent: T(hd.querySelector('span')),
        sub: T(el.querySelector('.ad-content p')),
        cards: [...el.querySelectorAll('.ad-card')].map((c) => ({ icon: img(c.querySelector('img')), lines: [...c.querySelectorAll('*')].filter((n) => !n.children.length && T(n)).map(T) })),
        text: [...el.querySelectorAll('*')].filter((n) => !n.children.length && T(n)).map(T),
        cta: [...el.querySelectorAll('a')].map((a) => ({ label: T(a), href: a.href })) });
    }
    else if (cls.includes('gpi-author-card')) {
      blocks.push({ type: 'author', kicker: T(el.querySelector('h2, h3, h4')),
        text: [...el.querySelectorAll('.gpi-author-card-details-zone *')].filter((n) => !n.children.length && T(n)).map(T),
        photo: img(el.querySelector('img')),
        links: [...el.querySelectorAll('a')].map((a) => ({ label: T(a) || a.getAttribute('aria-label') || '', href: a.href })) });
    }
  }
  const crumbs = [...document.querySelectorAll('.penci-breadcrumb a, .penci-breadcrumb span:not(.bc-sep) > span, .penci-breadcrumb .breadcrumb_last')].map((n) => ({ label: T(n), href: n.href || '' })).filter((c) => c.label);
  const sidebar = [...document.querySelectorAll('#sidebar aside.widget, .penci-sidebar-content aside.widget')].map((w) => ({
    title: T(w.querySelector('.widget-title')),
    items: w.querySelector('.side-newsfeed')
      ? [...w.querySelectorAll('.penci-feed')].map((li) => ({ title: T(li.querySelector('.side-item-text a, h4 a, a[title]') || li.querySelector('a')), href: (li.querySelector('a') || {}).href, date: T(li.querySelector('time, .side-item-meta')) }))
      : [...w.querySelectorAll('a')].map((a) => ({ title: T(a), href: a.href })),
  }));
  const related = [...document.querySelectorAll('.post-related .item-related')].map((it) => ({
    title: T(it.querySelector('h3 a')), href: (it.querySelector('h3 a') || {}).href, img: img(it.querySelector('.penci-image-holder, img')), date: T(it.querySelector('time, .date')),
  }));
  const prev = document.querySelector('.prev-post');
  const comment = document.querySelector('#respond');
  return {
    title: document.title, menu: menu(), crumbs,
    h1: T(art.querySelector('h1')), heroImg: img(art.querySelector('.post-image img')), heroAlt: (art.querySelector('.post-image img') || { alt: '' }).alt,
    author: T(art.querySelector('.post-box-meta-single .author-url, .post-box-meta-single a')),
    authorHref: (art.querySelector('.post-box-meta-single a') || {}).href || '',
    byline: T(art.querySelector('.post-box-meta-single')),
    date: T(art.querySelector('.post-box-meta-single time, time')),
    blocks, sidebar, related,
    prev: prev ? { label: T(prev.querySelector('.prev-post-title, span')), title: T(prev.querySelector('h5, .prev-post-title + *, a')), href: (prev.querySelector('a') || {}).href } : null,
    share: [...art.querySelectorAll('.tags-share-box .dt-share')].map(T),
    comment: comment ? { title: T(comment.querySelector('#reply-title')), labels: [...comment.querySelectorAll('label, .comment-notes')].map(T), submit: (comment.querySelector('[type=submit]') || {}).value } : null,
  };
`;

function md(name, data) {
  const L = [`# ${name}`, '', `Source: goldenpi.com, captured ${new Date().toISOString().slice(0, 10)}. Generated by crawl/blog_extract.js.`, ''];
  const dump = (v, d = 0) => {
    const pad = '  '.repeat(d);
    if (Array.isArray(v)) v.forEach((x) => { if (typeof x === 'object') { L.push(`${pad}-`); dump(x, d + 1); } else L.push(`${pad}- ${x}`); });
    else if (v && typeof v === 'object') Object.entries(v).forEach(([k, x]) => {
      if (x === '' || x == null || (Array.isArray(x) && !x.length)) return;
      if (typeof x === 'object') { L.push(`${pad}- **${k}**`); dump(x, d + 1); } else L.push(`${pad}- **${k}**: ${x}`);
    });
  };
  dump(data);
  return L.join('\n') + '\n';
}

(async () => {
  const browser = await chromium.launch({ executablePath: chromiumPath() });
  const page = await browser.newPage({ javaScriptEnabled: false });
  for (const [kind, file] of Object.entries(PAGES)) {
    await page.setContent(fs.readFileSync(path.join(R, file), 'utf8'), { waitUntil: 'domcontentloaded' });
    const data = await page.evaluate(new Function(kind === 'landing' ? LANDING : POST));
    const slug = kind === 'landing' ? 'prod_blog' : 'prod_blog_post';
    fs.writeFileSync(path.join(R, `${slug}.json`), JSON.stringify(data, null, 1));
    fs.writeFileSync(path.join(__dirname, '..', 'content', `${slug}.md`), md(data.title, data));
    console.log(slug, kind === 'landing'
      ? `slides=${data.slides.length} sections=${data.sections.map((s) => `${s.name}:${s.posts.length}`).join(',')}`
      : `blocks=${data.blocks.length} sidebar=${data.sidebar.length} related=${data.related.length}`);
  }
  await browser.close();
})();
