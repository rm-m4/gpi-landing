# Implementation tracker

Project context and rules live in `CLAUDE.md`. This file tracks state only.

**Last updated:** 2026-09-25
**Content snapshot:** 2026-09-25 (all hardcoded data carries this date)
**Now:** All four landing pages converted to the agreed styling and promoted.

**Scope from 2026-09-26: the four live pages only.** `index.html`,
`corporate-bonds.html`, `fixed-deposits.html`, `bond-ipo-online.html`. The four
`-old` archives and the seven design explorations (`-alt`, `-taste`, `-taste2`,
`-taste3`) are frozen; the direction is settled and editing them only adds churn.
`crawl/check.js` still runs across all eighteen, because a regression in a frozen
page means something shared broke.

---

## Batch 1 — status

Scope agreed with the user: 4 pages, static HTML + Tailwind CDN, light theme only.

| Phase | State | Evidence |
|---|---|---|
| A · Capture | done | 4 rendered pages, 8 live screenshots, 104 images, 1840 tokens |
| B · Extract | done | `content/*.md`, 1545 lines, checked against screenshots |
| C · Build | done | `node crawl/check.js` → all clean |
| D · Polish | **not started** | blocked on user review of C |

### Pages

| Page | Source | Built | Checks | Notes |
|---|---|---|---|---|
| `pages/index.html` | `/` | yes | clean | Hero banner art, asset tabs, FD scroller, bubble chart |
| `pages/corporate-bonds.html` | `/corporate-bonds` | yes | clean | Reference page — shared shell is edited here |
| `pages/fixed-deposits.html` | `/fixed-deposits` | yes | clean | Working FD returns calculator, 7-issuer comparison table |
| `pages/bond-ipo-online.html` | `/bond-ipo-online` | yes | clean | Live + closed IPO tables, 4-step flow |

### Pipeline built

| Script | Does |
|---|---|
| `crawl/fetch.sh` | Server-rendered HTML with the `gp-locale` cookie |
| `crawl/snap.js` | Browser render + auto-scroll + desktop/mobile screenshots |
| `crawl/images.py` | Harvests every referenced image, strips Next.js hashes |
| `crawl/tokens.py` | Splits light/dark custom properties out of their stylesheet |
| `crawl/assets.sh` | Runs the two above |
| `crawl/extract.py` | HTML → reviewable markdown, leaf-block walker |
| `crawl/check.js` | Serves + renders pages, fails on 404s / errors / overflow |
| `pages/_build.py` | Syncs header + footer from the reference page |

---

## Issuer design system components

`/issuers/akara-capital-advisors-private-limited` is a from-scratch page on the new
site, so it is the reference for how new work should look. It is captured in
`crawl/raw/` and `crawl/rendered/`. Values below were read out of their compiled
stylesheet, not eyeballed:

| Token | Value |
|---|---|
| gold gradient | `linear-gradient(135deg, #fdf2d0 0%, #e6b325 50%, #b38600 100%)` |
| card radius | 20px (stat variant 15px) |
| card shadow | `0 2px 1px rgba(0,0,0,.02)` plus a `#fdf3d4` hairline along the bottom |
| CTA | pill, 14px/24px padding, gradient fill, `#322811` text |
| FAQ layout | `minmax(0,1fr) 360px`, 30px gap, stacking below 900px |

Ported into `assets/final.css` as `.gp-cta`, `.gp-block`, `.gp-faq-layout` and
`.gp-need-help`. Applied to **fixed-deposits** first:

- every CTA now uses the gold gradient; the secondary carries the same gradient as
  its border through a padding-box / border-box pair
- "Why invest in with GoldenPi?" became three blocks: white card, 20px radius,
  hairline, and the icon in a 40px gold-gradient squircle. Same copy, new shape.
- the FAQ sits beside a Need Help card matching `issuer-need-help`: the 237px
  support illustration, a phone icon beside the title, and a Contact Us CTA

The other three live pages have not been converted yet.

---

## Consistency across the live set

A structural audit on 2026-09-26 found the four live pages were not sharing three
things. Behaviour checks had all passed, because they assert that a page works,
never that it looks like the others.

| Was missing | Where | Fixed by |
|---|---|---|
| warm gold hero wash | fixed-deposits, bond-ipo-online | `.gp-hero` promoted out of corporate-bonds' private `<style>` into `assets/final.css` |
| highlighted key figure in the hero | fixed-deposits, bond-ipo-online | `.gp-hero__figure` on `8.5% p.a.` and `as high as 15%` |
| milestone count-up | bond-ipo-online | `data-count` on its three figures |
| cream listing panel | fixed-deposits, bond-ipo-online | fixed earlier the same day |

`index.html` keeps a different hero on purpose: it is GoldenPi's dark banner, and
that is the homepage's own treatment.

**`crawl/check.js` now runs a cross-page consistency pass** on a full run. It
compares the live four against corporate-bonds for the hero ground, the tablist,
the reveal markup, the section heading treatment and the FAQ, with named
exemptions (bond-ipo-online has no category tabs on the live site). Negative
tested: removing the hero ground from one page makes it fail with
`fixed-deposits.html is missing .gp-hero, .home-hero (hero ground)`.

---

## Live set, as of 2026-09-26

| URL | Was | Archive |
|---|---|---|
| `index.html` | the faithful homepage | `index-old.html` |
| `corporate-bonds.html` | `corporate-bonds-final.html` | `corporate-bonds-old.html` |
| `fixed-deposits.html` | the faithful FD page | `fixed-deposits-old.html` |
| `bond-ipo-online.html` | the faithful IPO page | `bond-ipo-online-old.html` |

All four load `assets/site.css` plus the additive `assets/final.css` (137 lines,
overriding nothing), keep the shared header and footer, and keep every `gp-*`
component. No page loads `alt.css`, `taste.css`, `lux.css`, `spark.css` or
`minimal.css`; those belong to the exploration variants only.

**What conversion changed, per page**

| | index | corporate-bonds | fixed-deposits | bond-ipo-online |
|---|---|---|---|---|
| tabs become a real tablist | 6 tabs, listing rows | 6 tabs, listing rows | 3 tabs, issuer cards | no tabs on this page |
| repeated heading removed | yes | yes | n/a | n/a |
| collections bento | yes | yes | n/a | n/a |
| reviews grid | yes | yes | yes | yes |
| scroll reveal script | added | already had it | added | added |

The three archived pages carried `data-reveal` markup but never had the script
driving it, so the reveal was dead on them. It is wired up on the live set.

On fixed deposits the tabs filter the **issuer cards**, not a new row table:
the page already carries a full comparison table lower down, and adding rows
would have been a third copy of the same six issuers. Tax Saving FD shows an
honest empty state, because no tax saving deposit was in the capture.

**Archives are frozen.** They are absent from `pages/_build.py` so the shell
sync cannot touch them, they are marked with an ARCHIVE comment, and their
internal links point at each other. A live page never links into the archive
and an archive never links out; `crawl/check.js` runs over both sets.

**Generators.** `_final.py` writes corporate-bonds.html from `_final_shell.html`;
`_convert.py` writes the other three from the `-old` archives; `_tabs.js` and
`_reveal.js` are shared by both so the behaviour cannot drift; `_taste.py` reads
the `-old` archives so re-running reproduces what was reviewed.

---

## Next up

### 1. UI polish pass — batch 1 (phase D) — **awaiting a direction choice**

All four pages built in **three** directions. Compare, pick one, retire the other two.

| Page | Faithful | Elevated | Taste |
|---|---|---|---|
| Homepage | `index.html` | `index-alt.html` | `index-taste.html` |
| Corporate bonds | `corporate-bonds.html` | `corporate-bonds-alt.html` | `corporate-bonds-taste.html` |
| Fixed deposits | `fixed-deposits.html` | `fixed-deposits-alt.html` | `fixed-deposits-taste.html` |
| Bond IPOs | `bond-ipo-online.html` | `bond-ipo-online-alt.html` | `bond-ipo-online-taste.html` |

**Faithful** — same layouts, properly executed: warm hero wash, highlighted key
figures, gold rule under centred section heads, card accent + lift, scroll reveal.

**Elevated** — dark hero stage with a gradient headline, proof (15L+ / ₹2,500Cr /
₹10,000Cr) pulled up into the hero, left-aligned section heads with trailing rules,
and one dark band per page to break the scroll: milestones on corporate-bonds and
bond-ipo, the bubble chart on the homepage, the bonds cross-sell on fixed-deposits.

**Taste** — built against the `leonxlnx/taste-skill` audit. Design read: redesign-preserve
of a regulated fixed-income marketplace, trust-first language. Dials `VARIANCE 4 /
MOTION 3 / DENSITY 5`, because the skill's own table puts regulated and trust-first
at 3-4 variance and says quiet constraints override aesthetic preference. So this
direction is **calmer** than the elevated one, not louder. Changes it makes:

| Rule | Applied |
|---|---|
| 4.11 Page Theme Lock | one light theme throughout; no dark band dropped into a cream page (this is what the elevated direction does, and the skill calls it out explicitly) |
| 4.7 Hero stack | headline + subtext + CTAs only, subtext ≤ 20 words; the SEBI trust strip moved out into its own band below the hero |
| 4.7 Eyebrow restraint | eyebrows above section headings dropped; headings left-aligned, no centred gold mark |
| 9.C | three-equal-card feature rows replaced with an asymmetric lead + hairline list |
| 4.10 Testimonials | quotes cut to a glanceable length, attribution given a role, avatar squircles not circles |
| 9.G Em-dash ban | all em/en dashes removed from copy we wrote |
| Redesign audit | tinted shadows, tabular figures, grain overlay, active/pressed states |

Shared styling: **`assets/alt.css`** for the elevated pages, **`assets/taste.css`** for
the taste pages, each linked only by its own variants so they cannot drift.
`pages/_taste.py` regenerates the taste variants from the faithful pages.

#### `corporate-bonds-final.html` - the production candidate

**This is `corporate-bonds.html` plus four ported improvements, not a redesign.**
Same stack (Tailwind CDN + `assets/site.css`), same shared header and footer, same
`gp-*` components, same gold pill buttons. `assets/final.css` is 137 additive lines
and overrides nothing in `site.css`.

A first attempt took taste2 wholesale and grafted the content in. That was wrong:
a new stylesheet, a floating island nav, bezels and film grain amount to a
re-platform, and `CLAUDE.md` says a developer should recognise the page and lift
markup across rather than translate it. Rebuilt from the faithful page instead.

| Ported from taste2 | How |
|---|---|
| Bento collections | asymmetric Tailwind spans (4/2, 2/2/2, 6) on the existing `.gp-card` |
| Tabs keep, heading goes | `Special Corporate Bond Deals for you!` removed; the active tab names the list |
| Tab selection animation | one indicator moved by transform and width, drawn as the pill that was already there; panels cross-fade, rows stagger at 50ms |
| taste2 explainer | four benefit tiles replaced with `coupon-schedule.svg` in a `.gp-card` |
| taste2 reviews | horizontal scroller becomes a three-column grid of `.gp-card` |

**The tabs really filter.** Six tabs, sixteen rows, all captured 2026-09-25, nothing
invented. High Rated and NCD IPO draw the two live issues from the bond-ipo capture;
Bonds at 30K draws the Muthoot Capital bond with its stated minimum. The fourth and
fifth columns relabel per tab (Payout / Status / Min. Investment, Maturity Date /
Closes On) because those are genuinely different things.

Also fixed here: the column labels rendered twice at desktop, once in the header row
and once inside each row. The in-row labels are the mobile fallback, so they are now
hidden from 761px up. Scoped to this page's panels, so `site.css` is untouched.

Keyboard support follows the tablist pattern. Milestone figures count up on first
view. Everything degrades to a working listing without JS.

Generated: edit `pages/_final.py` for tab data or `pages/_final_shell.html` for the
rest, then run `python3 pages/_final.py`. `crawl/check.js` asserts the indicator
moves, the right panel opens, the previous closes, row counts per tab, ArrowLeft
selection, and that the count-up settles on the true figure.

#### `corporate-bonds-taste3.html` - the three-banner hero

Structure borrowed from `rbp-sparkdesign-template.vercel.app`, which the user
pointed at specifically for its hero: **three banners on a carousel** with floating
chips laid over the media, corner pills and dot navigation. GoldenPi's palette and
Satoshi throughout; the reference's white/sage/lavender becomes their cream and gold.

Standalone: `assets/spark.css`, excluded from `pages/_build.py`.

- **The carousel is real.** Auto-advances every 5.2s, dots switch banners, pauses on
  hover, focus and tab-hide, disabled under `prefers-reduced-motion`. The floating
  metrics card re-writes itself per banner, and every value in it is GoldenPi's own.
- **Banners are typographic, not photographic.** GoldenPi's product art
  (`ncd-hero.png`) has its own badges baked in, which collided with the floating
  chips and left one clipped. Each banner is now a gradient ground with a ghosted
  figure, so there is no asset conflict.
- Also borrowed: the category pill row, the big-type gallery cards, the list-style
  rows, and the FAQ-plus-side-card split.
- The reference's three-equal-card feature row was **not** copied: taste-skill 9.C
  bans it. That content became an asymmetric split instead.

`crawl/check.js` asserts the carousel advances, the metrics swap with it, and
exactly one banner is active at a time.

#### `corporate-bonds-taste2.html` - the high-end pass

An enhancement of the faithful `corporate-bonds.html`, built to the bundle's
**`high-end-visual-design`** skill. Its Variance Engine was rolled to
**Editorial Luxury** (warm creams, film grain, high-contrast type) and
**Asymmetrical Bento**, because GoldenPi's harvested palette is already warm cream
and gold; the alternative archetype, Ethereal Glass, means OLED black and neon orbs
and would be a different company.

Standalone: own stylesheet `assets/lux.css`, excluded from `pages/_build.py`.

| Technique | Where |
|---|---|
| Double-bezel (outer shell + inner core, concentric radii, inset highlight) | every card, the listing, the hero art |
| Button-in-button trailing icon with magnetic hover | all CTAs |
| Fluid island nav, detached floating glass pill | header |
| Scroll interpolation: 16px lift + blur resolving over 800ms, 90ms stagger | all major blocks |
| Film grain + warm light pooling, both fixed and pointer-events-none | page ground |
| Asymmetrical bento (7/5, 4/4/4, 6/6/12 spans) | collections, why-us, quotes, blog |

New image drawn for it: `assets/img/coupon-schedule.svg`, a timeline of monthly
coupon payments and the principal returned at maturity.

`crawl/check.js` asserts the double-bezel actually nests (shell padding present,
inner radius smaller than outer) so the signature technique cannot silently regress.

#### `corporate-bonds-taste.html` is a special case

Rebuilt from scratch against the bundle's **`minimalist-ui`** skill, on the user's
instruction to write content, animation and imagery as needed. It is the only page
that is fully standalone: no `site.css`, no Tailwind, no shared shell, its own
`assets/minimal.css`. `pages/_build.py` deliberately excludes it, and
`pages/_taste.py` will overwrite it if re-run, so regenerate the other three by name.

- **Prose written for this page**, section intros and explanations. Every number,
  credit rating, issuer name, date, FAQ answer and legal line is GoldenPi's own and
  unchanged. Nothing about rates, ratings or regulatory status was invented.
- **Three illustrations drawn for it**, in `assets/img/ink/`: continuous-line ink
  sketches with one offset pastel shape, which is what the skill specifies.
- **Deviations from minimalist-ui, all for brand fidelity:** Satoshi instead of an
  editorial serif (the skill suggests Instrument Serif; the bundle's own taste-skill
  bans that font by name), CTA in GoldenPi's ink `#322811` rather than `#111111`, and
  gold kept as the single spot accent. Recorded at the top of `assets/minimal.css`.

**One deliberate deviation:** the skill bans em-dashes outright, but GoldenPi's own
footer line reads `© Copyright 2017 – 2026`. `CLAUDE.md` puts content fidelity above
presentation for their regulated copy, so that one en-dash is preserved on every
taste page. Every other dash we wrote is gone.

Shared foundation, already landed in `assets/site.css` and used by both:

- [x] Type ramp — `--t-caption` … `--t-display`, replacing 10 ad-hoc `text-[Npx]` sizes
- [x] Spacing scale `--s-1`…`--s-9` and a two-level section rhythm
- [x] `.t-*` utility classes so pages stop hand-rolling sizes
- [x] Card interaction (`.gp-card--link`, `.gp-card--accent`) and warm elevation
- [x] Scroll reveal via one IntersectionObserver, with reduced-motion and print guards

Still to do once a direction is chosen:

- [ ] Apply the winner to `index`, `fixed-deposits`, `bond-ipo-online`
- [ ] Retire the losing variant file
- [ ] Bubble chart — hover tooltip layer (currently native SVG `<title>` only)
- [ ] Dark theme — values already harvested, commented at the bottom of `tokens.css`
- [ ] Extract the resulting rules into `.claude/skills/gpi-design/` before batch 2

### 2. Batch 2 — pages not yet built

Decided when batch 1 is signed off. Inventory from the crawl:

| Candidate | Shape | Effort |
|---|---|---|
| `/bond-utsav` | Campaign page, heavily data-driven | medium |
| `/refer-and-earn` | Short marketing page | low |
| `/about-us` | Mostly static copy — leadership, vision, partners | low |
| `/careers` | Static + job listings | low |
| 11 × `/collections/*` | One template, 11 content sets | medium (one design) |
| `/faq`, `/contact-us`, `/privacy-policy`, `/terms-and-conditions` | Utility pages | low |
| `/bonds/<id>/*`, `/fixed-deposits/<id>/*` | Product detail — complex, data-heavy | high |

The 11 collection slugs: `all-bonds`, `best-ongoing-ipos`, `bonds-at-10000`,
`bonds-at-discounted-price`, `bonds-maturing-within-a-year`,
`bonds-to-earn-monthly-fixed-income`, `high-yield-bonds`, `highly-rated-bonds`,
`newly-launched-bonds`, `state-government-guranteed-bonds`, `tax-free-bonds`.

---

## Open items

| # | Item | Impact | Proposed action |
|---|---|---|---|
| 1 | 4 orphan images in `assets/img/` left by the filename-cleanup pass — `GPID100133.logo.png`, `GPID100778.edel.png`, `GPID104212.Screenshot2024-08-2016121.jpeg`, `no-result-man-with-loud-speaker.2_lhqtc1ijwq_.svg` | cosmetic; 108 files on disk vs 104 in `img-map.tsv` | delete once the user confirms — needs explicit sign-off |
| 2 | Hardcoded snapshot data goes stale as UAT changes | pages show old rates over time | re-run `snap.js` + `extract.py` before any handoff |
| 3 | The UAT site links one FAQ reference relatively, resolving to a dead path | theirs, not ours | ours points at `goldenpi.com/blog`; worth reporting to their team |
| 4 | `GPID103493.jpeg` 404s on their S3 | one issuer logo unavailable upstream | not referenced by our pages; no action |

## Fixed

| Date | Bug | Cause | Fix |
|---|---|---|---|
| 2026-09-25 | FD returns calculator was dead and its profile chips rendered as plain text | an early `pages/_build.py` sliced the shared footer through to `</body>`, deleting the page's own `<style>` and `<script>` | `_build.py` now ends the slice at `</footer>`; script and styles restored; `crawl/check.js` gained behaviour assertions that fail when a page's own CSS/JS stops working |
| 2026-09-25 | Homepage hero lost its background art | same `_build.py` slice | hero styles moved into `<head>` |
| 2026-09-25 | Scroll-reveal left every below-fold section at `opacity: 0` in full-page captures — and would have done the same in print/PDF | `IntersectionObserver` never fires without scrolling | `crawl/check.js` now scrolls before capturing; `@media print` forces revealed state |
| 2026-09-25 | Sticky header repeated down every full-page screenshot | Chromium paints `position: sticky` into each band of the capture | header pinned to `position: static` for the screenshot only |

Both were invisible to the original checker — a dead script produces no 404,
no console error and no layout overflow. That gap is now closed, and the new
assertion was negative-tested by re-breaking the page and confirming it fails.

## Decisions made

| Decision | Reason |
|---|---|
| Playwright over plain `curl` for data sections | `curl` returns only `gp-skeleton` placeholders |
| Harvest their design tokens rather than choose a palette | "stay close to what it's built with"; devs recognise the variable names |
| Header "Login / Sign up" is a `<button>`, not a link | live site opens a modal; a `/login` route would be invented |
| Homepage bubble chart rebuilt as inline SVG | original is `<canvas>`; values read off a screenshot, palette validated |
| Header/footer duplicated, synced by script | four-page prototype; a template system would be unused complexity |
| Light theme first | layouts still in flux; dark is a mechanical pass once they settle |
| Keep Tailwind + Satoshi on their CDNs; do **not** vendor them locally | user's call, 2026-09-25. Pages need a network connection for layout and typography; all content, images and data are local and work offline. Acceptable for a reference artifact — revisit only if it has to be handed over for offline use |
