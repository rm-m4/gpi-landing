# GoldenPi landing pages

Static rebuilds of four `uatnew.goldenpi.com` pages, with all copy taken from the
live site rather than written fresh. Meant as a build reference for developers.

Every rate, credit rating, issuer name, maturity date and legal line is GoldenPi's
own, captured **2026-09-25** and reproduced unchanged. Nothing about returns,
ratings or regulatory status was invented.

## Look at them

```bash
python3 -m http.server 8000      # from this directory
open http://localhost:8000/pages/corporate-bonds.html
```

Opening the `.html` files from disk works too. There is no build step to view them,
though three of the four pages are generated from templates (see below).

## The four live pages

| Page | Source URL |
|---|---|
| `pages/index.html` | `/` |
| `pages/corporate-bonds.html` | `/corporate-bonds` |
| `pages/fixed-deposits.html` | `/fixed-deposits` |
| `pages/bond-ipo-online.html` | `/bond-ipo-online` |

These four are the deliverable. Everything else in `pages/` is history and can be
ignored when implementing:

- `*-old.html` — each page as it stood before the 2026-09-26 styling pass, kept so
  the change is reviewable. Frozen.
- `*-alt.html`, `*-taste.html`, `corporate-bonds-taste2.html`,
  `corporate-bonds-taste3.html` — design directions that were compared before one
  was chosen. Frozen.

## What a developer needs to know

**The stack is deliberately close to yours.** Tailwind via CDN plus two stylesheets,
no framework, no build:

```html
<link rel="stylesheet" href="../assets/site.css">   <!-- shell + components -->
<link rel="stylesheet" href="../assets/final.css">  <!-- 150 additive lines -->
```

`final.css` overrides nothing in `site.css`. It adds the category tab strip and its
sliding indicator, the tab panels, and a couple of layout helpers.

**Colours and type are yours.** `assets/tokens.css` holds 1840 custom properties
harvested from your own compiled stylesheet, light theme. Primary is
`--mustard: #d4af37`, page `#f7f5f2`, ink `#322811`. Type is Satoshi from Fontshare,
the same source your site uses.

**Components are reusable.** `gp-header`, `gp-footer`, `gp-card`, `gp-row`,
`gp-btn`, `gp-section`, `gp-faq`, `gp-tabs`. The header and footer are duplicated
per file on purpose, since you will rebuild them as components anyway.

**Live data is hardcoded.** Every block your site fetches is marked
`<!-- DATA: ... -->` with the snapshot date. That is the wiring list: the bond
listing and its tab filters, the FD issuer cards, the IPO lists, the promo strip
and the reviews.

**Not built:** dark theme. The values are harvested and sit commented at the bottom
of `assets/tokens.css`, so it is a mechanical pass rather than a rebuild.

## Layout

```
pages/
  index.html  corporate-bonds.html  fixed-deposits.html  bond-ipo-online.html
  *-old.html, *-alt.html, *-taste*.html      frozen history
  _final.py      generates corporate-bonds.html from _final_shell.html
  _convert.py    generates the other three from the -old archives
  _final_shell.html                          page body for corporate-bonds
  _tabs.js, _reveal.js                       shared behaviour, injected by both
  _build.py      syncs the header and footer across pages
assets/
  tokens.css     1840 design tokens harvested from your stylesheet
  site.css       shared shell and components
  final.css      additive layer the four live pages load
  alt/taste/lux/spark/minimal.css            used only by the frozen explorations
  img/           108 images pulled from the site and its CDNs
  img-map.tsv    original URL -> local filename
content/         extracted copy, one markdown file per page, the source of truth
crawl/           the capture pipeline (below)
```

## Editing

Three of the four pages are generated. Editing the `.html` directly is lost on the
next run.

```bash
python3 pages/_final.py      # -> corporate-bonds.html
python3 pages/_convert.py    # -> index, fixed-deposits, bond-ipo-online
python3 pages/_build.py      # sync header/footer across pages
node crawl/check.js          # verify every page
```

`crawl/check.js` serves the folder, renders each page, and fails on 404s, console
errors, images that never decoded, horizontal overflow at 390px, and per-page
behaviour assertions (the tabs advance, the right panel opens, the FD calculator
computes, nothing is left invisible). Run it after any change.

## Re-running the capture

The site 307-loops `/` without a `gp-locale=en` cookie, and its data sections are
client-rendered, so plain `curl` returns only skeleton placeholders. The pipeline
handles both:

```bash
./crawl/fetch.sh /corporate-bonds   # server-rendered HTML  -> crawl/raw/
node crawl/snap.js                  # browser-rendered HTML -> crawl/rendered/ + shots
./crawl/assets.sh                   # images + design tokens -> assets/
python3 crawl/extract.py            # copy -> content/*.md
```

`playwright-core` is the only dependency; it drives the Chromium already cached on
this machine, so there is no browser download.
