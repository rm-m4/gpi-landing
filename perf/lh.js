// Lighthouse performance runs for uatnew.goldenpi.com: 3 mobile + 1 desktop per
// page, one at a time. Resumable: a run whose JSON already exists is skipped.
// -> perf/<date>/lh/<slug>.<mobile|desktop>.<n>.json (screenshots stripped)
// Usage: node perf/lh.js <pages.json> [outDir]
//   pages.json: [{ "slug": "home", "path": "/" }, ...]
//   LH_PORT=9222 attaches to an already-running (logged-in) Chrome instead of
//   launching one, and keeps its cookies and storage (the HTTP cache is emptied
//   before each run).

const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const BASE = 'https://uatnew.goldenpi.com';
const CHROME = `${process.env.HOME}/Library/Caches/ms-playwright/chromium-1234/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing`;
const PAGES = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const OUT = path.join(process.argv[3] || path.join(__dirname, new Date().toISOString().slice(0, 10)), 'lh');
const PORT = process.env.LH_PORT;
const DROP = ['screenshot-thumbnails', 'final-screenshot', 'full-page-screenshot'];

const CLEAR_CACHE = `(async () => {
  const b = await require('playwright-core').chromium.connectOverCDP('http://localhost:${PORT}');
  const ctx = b.contexts()[0], page = await ctx.newPage();
  await (await ctx.newCDPSession(page)).send('Network.clearBrowserCache');
  await page.close(); await b.close();
})()`;

fs.mkdirSync(OUT, { recursive: true });
const tmp = path.join(os.tmpdir(), `lh-${process.pid}.json`);

for (const { slug, path: p } of PAGES) {
  for (const [form, n] of [['mobile', 1], ['mobile', 2], ['mobile', 3], ['desktop', 1]]) {
    const file = path.join(OUT, `${slug}.${form}.${n}.json`);
    if (fs.existsSync(file)) continue;
    const args = ['-y', 'lighthouse@13.5.0', BASE + p, '--only-categories=performance', '--output=json',
      `--output-path=${tmp}`, '--quiet', '--max-wait-for-load=60000',
      // Without gp-locale the site 307-redirects to itself.
      `--extra-headers=${JSON.stringify({ Cookie: 'gp-locale=en' })}`,
      ...(form === 'desktop' ? ['--preset=desktop'] : []),
      ...(PORT ? [`--port=${PORT}`, '--disable-storage-reset'] : ['--chrome-flags=--headless=new'])];
    // With a logged-in Chrome the session cookies must not be replaced by the header.
    if (PORT) args.splice(args.findIndex((a) => a.startsWith('--extra-headers')), 1);
    // An attached Chrome keeps its HTTP cache between runs; empty it so every run is a cold load.
    if (PORT) spawnSync('node', ['-e', CLEAR_CACHE], { cwd: __dirname, timeout: 30000 });
    const r = spawnSync('npx', args, { env: { ...process.env, CHROME_PATH: CHROME }, encoding: 'utf8', timeout: 240000 });
    if (r.status !== 0 || !fs.existsSync(tmp)) {
      console.log(`${slug} ${form} ${n} FAILED`, (r.stderr || '').trim().split('\n').pop());
      continue;
    }
    const lhr = JSON.parse(fs.readFileSync(tmp, 'utf8'));
    fs.unlinkSync(tmp);
    for (const k of DROP) delete lhr.audits[k];
    delete lhr.i18n; delete lhr.timing; delete lhr.categoryGroups;
    fs.writeFileSync(file, JSON.stringify(lhr));
    const a = lhr.audits;
    console.log(slug.padEnd(34), form.padEnd(7), n, 'score', Math.round((lhr.categories.performance.score || 0) * 100),
      'LCP', Math.round(a['largest-contentful-paint'].numericValue), 'CLS', a['cumulative-layout-shift'].numericValue.toFixed(3),
      'TBT', Math.round(a['total-blocking-time'].numericValue), lhr.runtimeError ? `ERR ${lhr.runtimeError.code}` : '', lhr.finalDisplayedUrl.replace(BASE, ''));
  }
}
