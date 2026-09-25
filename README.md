# GoldenPi landing pages — batch 1

Static rebuilds of four `uatnew.goldenpi.com` pages, with all copy taken from the
live site rather than written fresh. Meant as a build reference for developers.

**Status: workable, not yet polished.** Every section, every piece of copy and every
link is in place and responsive. Visual refinement is a deliberate second pass.

## Look at them

```bash
python3 -m http.server 8000      # from this directory
open http://localhost:8000/pages/corporate-bonds.html
```

Opening the `.html` files directly from disk also works — there is no build step.

| Page | Source URL |
|---|---|
| `pages/index.html` | `/` |
| `pages/corporate-bonds.html` | `/corporate-bonds` |
| `pages/fixed-deposits.html` | `/fixed-deposits` |
| `pages/bond-ipo-online.html` | `/bond-ipo-online` |

## Layout

```
pages/          the four pages + _build.py (keeps header/footer in sync)
assets/
  tokens.css    1795 design tokens harvested from the live stylesheet
  site.css      shared shell + components (header, rows, FAQ, footer)
  img/          104 images pulled from the site and its CDNs
  img-map.tsv   original URL -> local filename
content/        extracted copy, one markdown file per page (the source of truth)
crawl/          the capture pipeline (see below)
  raw/          server-rendered HTML
  rendered/     browser-rendered HTML (the data sections only exist here)
  shots/        screenshots of the live site
  local-shots/  screenshots of these pages, for comparison
```

## Notes for developers

- **Styling** is Tailwind via CDN plus `assets/site.css`. The Tailwind colour names
  (`gold`, `ink`, `page`, `subtext`, `stroke`, `bronze`, `gain`) map to the real
  tokens in `tokens.css`, so they should line up with the existing app.
- **Font** is Satoshi from Fontshare, the same source the live site uses.
- **Live data is hardcoded.** Every block that the real site fetches is marked
  `<!-- DATA: ... -->` with the snapshot date. That is what needs wiring up:
  the bond rows, FD issuer lists, IPO lists, the promo strip and the reviews.
- **Header and footer are duplicated per file** on purpose — it is a static
  prototype. `python3 pages/_build.py` copies them from `corporate-bonds.html`
  (the reference page) into the others, so edit them there.
- **No JS framework.** The FAQ is `<details>`, carousels are CSS scroll-snap. The
  only script is the FD returns calculator in `fixed-deposits.html`.
- **Not yet done:** dark theme (the token values are harvested and sit commented at
  the bottom of `tokens.css`), and the visual polish pass.

## Re-running the capture

The site 307-redirects `/` to itself without a `gp-locale=en` cookie, and its data
sections are client-rendered, so plain `curl` only returns skeleton placeholders.
The pipeline handles both:

```bash
./crawl/fetch.sh /corporate-bonds   # server-rendered HTML  -> crawl/raw/
node crawl/snap.js                  # browser-rendered HTML -> crawl/rendered/ + shots
./crawl/assets.sh                   # images + design tokens -> assets/
python3 crawl/extract.py            # copy -> content/*.md
node crawl/check.js                 # render these pages, fail on 404s / overflow
```

`crawl/snap.js` and `crawl/check.js` use the Playwright Chromium already cached on
this machine (`playwright-core` is the only dependency — no browser download).

`crawl/check.js` is the one to run after any edit: it serves the folder, loads each
page, and reports 404s, console errors, images that never decoded, and horizontal
overflow at 390px.
