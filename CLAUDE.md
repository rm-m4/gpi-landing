# GoldenPi landing pages — project context

## What this project is

GoldenPi (`goldenpi.com`) is a SEBI-registered debt broker and OBPP license holder —
an Indian platform for buying corporate bonds, NCD IPOs and fixed deposits online.
Their next-generation site is in development at **`uatnew.goldenpi.com`**.

This repo rebuilds pages from that UAT site as **beautiful, self-contained static
landing pages**, to be handed to GoldenPi's developers as a build reference.

It is a design deliverable, not a fork of the product. Nothing here runs against
their API, and nothing here ships to production as-is.

## Vision

> Take the real content of a page that already exists, and give it a presentation
> good enough that the developers want to build it.

Three commitments follow from that, in priority order:

1. **Content fidelity is non-negotiable.** Copy comes from the live site, captured
   and saved before any design work starts. We never invent marketing copy,
   product claims, rates, ratings or legal text. If a page says "returns as high as
   15%", ours says exactly that — this is regulated financial content.
2. **Stay close to what it is built with.** Same brand tokens, same typeface, same
   section order, same URLs. A developer should recognise the page and be able to
   lift markup straight across, not translate it.
3. **Then make it beautiful.** Design is the value we add on top — but it is added
   *after* the content is captured and verified, never in place of it.

## Working method

The project runs in three phases per batch of pages. They are deliberately
sequential — designing before capture is how invented copy gets in.

| Phase | Output | Gate before moving on |
|---|---|---|
| **A · Capture** | `crawl/raw/`, `crawl/rendered/`, `crawl/shots/`, `assets/` | Pages render fully, all assets downloaded |
| **B · Extract** | `content/*.md` | Read each file against its screenshot; nothing missing |
| **C · Build** | `pages/*.html` | `node crawl/check.js` clean on every page |
| **D · Polish** | — | Separate pass, only after the user reviews C |

"Workable" (phase C) means every section present, real copy, real links,
responsive, nothing broken. It does not mean finished-looking. Phase D is where
typography, spacing, motion and dark theme get their attention.

## What the site forces on us

These are verified constraints, not guesses. They shape the whole pipeline.

- **`/` 307-redirects to itself without a `gp-locale=en` cookie.** Every request
  must send it. This is why a naive crawler fails on this site.
- **Copy is server-rendered; data is not.** Headings, SEO prose, full FAQ answers
  and the footer all come back from `curl`. The bond rows, FD issuer lists, IPO
  lists, promo strip and reviews are client-fetched and appear only as
  `gp-skeleton` placeholders — they need a real browser, scrolled to the bottom to
  trigger the lazy sections.
- **Assets live in three places**: bundled under `/_next/static/media/`, and on S3
  and CloudFront. Some S3 paths contain literal spaces and parentheses, so URLs
  must be read out of HTML attributes, not matched with a whitespace-delimited
  regex.
- **The homepage bubble chart is a `<canvas>`** — its values are not in the DOM and
  had to be read off a screenshot.

## Design system (harvested, not invented)

Pulled from their own compiled stylesheet into `assets/tokens.css` — 1840
declarations, light theme, with the dark values kept commented for later.

| Role | Token | Value |
|---|---|---|
| Primary | `--mustard` | `#d4af37` |
| Page background | `--app-page-bg` | `#f7f5f2` (dark: `#1a1510`) |
| Heading ink | `--app-heading-color` | `#322811` (dark: `#f4e9c8`) |
| Body / subtext | `--subtext` | `#666666` |
| Card | `--white` | `#ffffff` |
| Border | `--light-stroke` | `#e7e3d978` |
| Gain / positive | — | `#06963c` |
| Bronze (links, eyebrows) | — | `#8a6520` |

Typeface is **Satoshi** (Fontshare, weights 400/500/700/900), the same source the
live site uses.

## Stack decisions (and why)

- **Static HTML + Tailwind CDN + one shared stylesheet.** No build step, opens in a
  browser instantly, fastest to iterate on visually. Tailwind colour names map onto
  the harvested tokens so the markup lines up with their Next.js app.
- **Header and footer duplicated per page, not templated.** It's a four-page
  prototype and developers will rebuild them as components; a partial system would
  be cost with no payoff. `pages/_build.py` syncs them from the reference page so
  they cannot drift.
- **No JS framework, native platform features first.** FAQ is `<details>`,
  carousels are CSS scroll-snap. The only script is the FD returns calculator.
- **Live data hardcoded from a dated snapshot**, every block marked
  `<!-- DATA: ... -->` so developers know exactly what to wire up.

## Rules for working in this repo

- **Never write marketing, product or legal copy.** If it is not in `content/*.md`,
  go capture it. Rates, ratings, tenures and disclaimers are regulated content.
- **Never invent a URL.** Every link must point at a path the crawl actually saw.
  If the live site uses a control that is not a link (the Login button opens a
  modal), do not turn it into one.
- **Run `node crawl/check.js` after any edit.** It fails on 404s, console errors,
  images that never decoded, and horizontal overflow at 390px.
- **Edit the shared shell in `pages/corporate-bonds.html`**, the reference page,
  then run `python3 pages/_build.py`.
- **Re-capture rather than hand-patch** when the UAT site changes.
- Accessibility basics are not part of the polish phase — one `<h1>` per page, real
  `alt` text, keyboard-reachable controls, visible focus. Those ship in phase C.

## Commands

```bash
./crawl/fetch.sh /corporate-bonds   # server-rendered HTML  -> crawl/raw/
node crawl/snap.js                  # browser-rendered HTML -> crawl/rendered/ + shots
./crawl/assets.sh                   # images + design tokens -> assets/
python3 crawl/extract.py            # copy -> content/*.md
python3 pages/_build.py             # sync header/footer across pages
node crawl/check.js                 # verify every page
python3 -m http.server 8000         # then open /pages/<name>.html
```

`playwright-core` is the only dependency; it drives the Chromium already cached on
this machine, so there is no browser download.

## Current state

See **`TRACKER.md`** for what is done, what is in flight, and what is next.
