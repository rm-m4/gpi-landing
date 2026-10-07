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

## Where the project stands

Batch 1 is built and converted. The four live pages are the deliverable:
`index.html`, `corporate-bonds.html`, `fixed-deposits.html`,
`bond-ipo-online.html`.

**Scope, from 2026-09-26: those four only.** The `-old` archives and the seven
design explorations (`-alt`, `-taste`, `-taste2`, `-taste3`) are frozen. The
direction is settled; editing them adds churn without moving the deliverable.
`crawl/check.js` still runs across all eighteen, because a regression in a frozen
page means something shared broke.

**Three of the four are generated.** Editing the HTML directly is lost on the next
run. `_final.py` writes corporate-bonds.html from `_final_shell.html`;
`_convert.py` writes the other three from the `-old` archives; `_tabs.js` and
`_reveal.js` are injected by both so the pages cannot drift apart.

## The method, for the next batch

Phases run in order. Designing before capture is how invented copy gets in.

| Phase | Output | Gate before moving on |
|---|---|---|
| **A · Capture** | `crawl/raw/`, `crawl/rendered/`, `crawl/shots/`, `assets/` | Pages render fully, all assets downloaded |
| **B · Extract** | `content/*.md` | Read each file against its screenshot; nothing missing |
| **C · Build** | `pages/*.html` | `node crawl/check.js` clean on every page |
| **D · Polish** | — | Separate pass, only after the user reviews C |

## Two corrections worth not repeating

**Enhance, do not re-platform.** Asked to fold good ideas from an exploration into
the main page, the first attempt lifted that exploration wholesale: its own
stylesheet, its own nav, its own component system, with the content grafted in.
That is a re-platform, and it fails the rule above. The rebuild kept the stack and
ported four specific changes, which came to 150 additive CSS lines. When in doubt,
measure the diff a developer would have to implement.

**Check that pages look like a set, not just that they work.** After the
conversion, two pages were missing the cream listing panel the other two had, so
the four did not read as one design. Every automated check passed, because they
assert behaviour and errors, never shared visual structure. Compare pages against
each other by eye or by structure, not only against the checker.

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

- **Static HTML + Tailwind CDN + two stylesheets** (`site.css`, plus the
  additive `final.css` on the live pages). No build step, opens in a
  browser instantly, fastest to iterate on visually. Tailwind colour names map onto
  the harvested tokens so the markup lines up with their Next.js app.
- **Header and footer duplicated per page, not templated.** Developers will
  rebuild them as components anyway; a partial system would be cost with no
  payoff. `pages/_build.py` syncs them so they cannot drift.
- **No JS framework, native platform features first.** FAQ is `<details>`,
  carousels are CSS scroll-snap. Scripts are the FD returns calculator, the
  category tablist and the scroll reveal, all progressive enhancement: without
  them every page still renders complete and visible.
- **Live data hardcoded from a dated snapshot**, every block marked
  `<!-- DATA: ... -->` so developers know exactly what to wire up.

## Rules for working in this repo

- **Never write marketing, product or legal copy.** If it is not in `content/*.md`,
  go capture it. Rates, ratings, tenures and disclaimers are regulated content.
- **Never invent a URL.** Every link must point at a path the crawl actually saw.
  If the live site uses a control that is not a link (the Login button opens a
  modal), do not turn it into one.
- **Put shared CSS in `assets/final.css`, not `assets/site.css`.** The frozen
  pages load `site.css` too, so changing it moves them. Only the four live pages
  load `final.css`.
- **Every new page gets a row in `pages/all-pages.html`**, under Final or
  Iterations (and a group within it). `check.js` fails with `not listed:` until
  it does; the tab counts update themselves.
- **Run `node crawl/check.js` after any edit.** It fails on 404s, console errors,
  images that never decoded, and horizontal overflow at 390px.
- **Edit the shared shell in `pages/_final_shell.html`**, not in
  `corporate-bonds.html`: that page is generated and direct edits are lost. Then
  `python3 pages/_final.py` and `python3 pages/_build.py`.
- **Re-capture rather than hand-patch** when the UAT site changes.
- Accessibility basics are not part of the polish phase — one `<h1>` per page, real
  `alt` text, keyboard-reachable controls, visible focus. Those ship in phase C.

## Commands

```bash
python3 pages/_final.py      # -> corporate-bonds.html
python3 pages/_convert.py    # -> index, fixed-deposits, bond-ipo-online
python3 pages/_utsav.py      # -> bond-utsav.html (from crawl/rendered/bond-utsav.tabs.json)
python3 pages/_utsav_live.py # -> bond-utsav-live.html (production UI, from prod_bond-utsav.tabs.json)
python3 pages/_profile.py    # -> profile.html, profile-no-kyc.html (content/profile.md + Figma 21:2427)
python3 pages/_refer.py      # -> refer-and-earn-with-referral.html (refer-and-earn.html + staging capture)
python3 pages/_explore_bonds.py # -> user-corporate-bonds2.html (post-login bonds + Collections, merged)
python3 pages/_bond_v4.py    # -> bond-details4.html (reads bond-details3.html: run _bond_beta.py first)
python3 pages/_bond_v5.py    # -> bond-details5.html, bond-details6.html (Figma 29:1409 design at 1200 / 1018px)
python3 pages/_footer_ggn.py # -> footer-ggn-prelogin-bonds.html (prelogin-home footer + footer-bonds SEO part)
python3 pages/_build.py      # sync header/footer across pages
node crawl/check.js          # verify every page, run after any change
python3 -m http.server 8000  # then open /pages/<name>.html
```

Capture, when the UAT site changes:

```bash
./crawl/fetch.sh /corporate-bonds   # server-rendered HTML  -> crawl/raw/
node crawl/snap.js                  # browser-rendered HTML -> crawl/rendered/ + shots
./crawl/assets.sh                   # images + design tokens -> assets/
python3 crawl/extract.py            # copy -> content/*.md
node crawl/utsav_tabs.js            # every Bond Utsav tab -> bond-utsav.tabs.json
node crawl/utsav_prod_tabs.js       # same on goldenpi.com -> prod_bond-utsav.tabs.json
node crawl/profile_tabs.js          # every /profile section (logged in) -> a temp dir, never the repo: it holds personal data
```

`playwright-core` is the only dependency. It needs a cached Chromium: on a new
machine run `npm ci && npx playwright install chromium` once.

## Current state

See **`TRACKER.md`** for what is done and what is next, and **`README.md`**
for the developer handoff. The repo is private at `rm-m4/gpi-landing`, default
branch `main`.
