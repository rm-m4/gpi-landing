// Read each issuer logo's dominant brand colour, for the per-card accent on
// user-corporate-bonds3.html. Logos with no real colour (black, grey, white)
// are left out, and their cards keep the gold.
// Usage: node crawl/logo_accents.js [logo files...]   -> assets/logo-accents.json
//   with no arguments, every logo the bonds3 page shows.

const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright-core');

const ROOT = path.dirname(__dirname);
const IMG = path.join(ROOT, 'assets', 'img');
const OUT = path.join(ROOT, 'assets', 'logo-accents.json');

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
  ]) if (fs.existsSync(path.join(dir, rel))) return path.join(dir, rel);
  throw new Error('no Chromium binary under ' + dir);
}

// Runs in the page: the hue bucket holding the most saturated, mid-light
// pixels wins, and its average is the accent. Under 4% coloured pixels = none.
function dominant(src) {
  return new Promise((resolve) => {
    const im = new Image();
    im.onload = () => {
      const c = document.createElement('canvas');
      c.width = c.height = 48;
      const x = c.getContext('2d');
      x.drawImage(im, 0, 0, 48, 48);
      const d = x.getImageData(0, 0, 48, 48).data;
      const buckets = {};
      let opaque = 0, coloured = 0;
      for (let i = 0; i < d.length; i += 4) {
        if (d[i + 3] < 200) continue;
        opaque++;
        const r = d[i] / 255, g = d[i + 1] / 255, b = d[i + 2] / 255;
        const max = Math.max(r, g, b), min = Math.min(r, g, b), l = (max + min) / 2;
        const s = max === min ? 0 : (max - min) / (1 - Math.abs(2 * l - 1));
        if (s < 0.35 || l < 0.18 || l > 0.82) continue;
        coloured++;
        let h = max === r ? (g - b) / (max - min) : max === g ? 2 + (b - r) / (max - min) : 4 + (r - g) / (max - min);
        h = ((h * 60) + 360) % 360;
        const k = Math.floor(h / 15);
        const o = buckets[k] || (buckets[k] = { n: 0, r: 0, g: 0, b: 0 });
        o.n++; o.r += d[i]; o.g += d[i + 1]; o.b += d[i + 2];
      }
      if (!opaque || coloured / opaque < 0.04) return resolve(null);
      const top = Object.values(buckets).sort((a, b) => b.n - a.n)[0];
      const hex = (v) => Math.round(v / top.n).toString(16).padStart(2, '0');
      resolve('#' + hex(top.r) + hex(top.g) + hex(top.b));
    };
    im.onerror = () => resolve(null);
    im.src = src;
  });
}

(async () => {
  let files = process.argv.slice(2);
  if (!files.length) {
    const page = fs.readFileSync(path.join(ROOT, 'pages', 'user-corporate-bonds3.html'), 'utf8');
    files = [...new Set([...page.matchAll(/gp-ucard__logo"><img src="\.\.\/assets\/img\/([^"]+)"/g)].map((m) => m[1]))];
  }
  const browser = await chromium.launch({ executablePath: chromiumPath() });
  const page = await browser.newPage();
  const out = {};
  for (const f of files.sort()) {
    const ext = path.extname(f).slice(1).toLowerCase().replace('jpg', 'jpeg');
    const data = 'data:image/' + ext + ';base64,' + fs.readFileSync(path.join(IMG, f)).toString('base64');
    const acc = await page.evaluate(dominant, data);
    if (acc) out[f] = acc;
  }
  await browser.close();
  fs.writeFileSync(OUT, JSON.stringify(out, null, 2) + '\n');
  console.log('%s  %d of %d logos have a colour', path.relative(ROOT, OUT), Object.keys(out).length, files.length);
})();
