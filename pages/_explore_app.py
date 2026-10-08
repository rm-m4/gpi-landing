#!/usr/bin/env python3
"""user-explore-app.html: the user's Figma "New User" explore screen
(file HRSMFFccdLgqf1YwD7oyc9, node 40:2105), in a light version.

Built the way bond-details3 is: the first block (headline + launch-event card)
stays in the Figma's black-and-gold, every block after it is light, in the
harvested tokens, and the navbar and footer are bond-details3's own (the final
dark navbar and the footer-ggn-login footer). The page reuses bond-details3's
head and footer, as bond-details6 does, so the chrome cannot drift.

Copy and figures are the Figma's sample content (Navi Finserv, 13.29%, the
Suryoday launch card,); every block carries a DATA comment.
The Figma's three spellings of the minimum investment ("MIN INV.", "MIN.",
"MIN INVESTMENT .") are one label here. Assets are the Figma's, in
assets/img/explore-app/.

    python3 pages/_bond_beta.py && python3 pages/_explore_app.py
"""
import os
import re

import _bond_beta as B
import _portfolio as P

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "bond-details3.html")
OUT = os.path.join(HERE, "user-explore-app.html")
REVEAL = os.path.join(HERE, "_reveal.js")
# The portfolio page's gold card and its info sheet, lifted as-is: only their rules from portfolio.css.
GCARD_CSS = ("<style>\n/* portfolio.css: the gold card and its info sheet, as on portfolio.html */\n%s\n"
             "@keyframes pf-sheen { from { transform: translateX(-120%%); } to { transform: translateX(120%%); } }\n"
             "@keyframes pf-up { from { transform: translateY(40px); opacity: 0; } to { transform: none; opacity: 1; } }\n"
             "@keyframes pf-fade { from { opacity: 0; } to { opacity: 1; } }\n"
             "@media (prefers-reduced-motion: reduce) { .pf-sheet, .pf-sheet::backdrop { animation: none !important; } }\n</style>\n"
             % B.css_rules(open(os.path.join(ROOT_DIR := os.path.dirname(HERE), "assets/portfolio.css"), encoding="utf-8").read(),
                           lambda sel: all(x.strip().startswith((".pf-gcard", ".pf-info", ".pf-sheet", ".pf-def", ".pf-ytm"))
                                          for x in sel.split(","))))
IMG = "../assets/img/explore-app/"
# Bond cards and the launch card link to the one bond detail page in the repo,
# standing in for each issue's own page.
BOND_HREF = "bond-details3.html"

STATS = [("stat-trophy.png", "Zero Defaults"), ("stat-users.png", "15 Lacs+ Users"),
         ("stat-5pct.png", "Curated Bonds"), ("stat-sebi.png", "Sebi Registered")]

COLLECTIONS = [("col-ncd-ipo.png", "NCD IPO", "collections-ncd-ipo.html"),
               ("col-high-returns.png", "High Returns", "collections-high-returns.html"),
               ("col-short-term.png", "Short Term", "collections-short-term.html"),
               ("col-gold-backed.png", "Gold Backed", "collections-gold-backed.html"),
               ("col-starts-10k.png", "Starts ₹10k", "collections-starts-10k.html"),
               ("col-high-rated.png", "High Rated", "collections-highly-rated.html")]

# Every card in the Figma carries the same sample bond.
BOND = {"name": "Navi Finserv", "rate": "13.29", "sold": "87% Sold", "min": "Min Inv. ₹1L",
        "rating": "AA+", "payout": "Monthly", "tenure": "3Y 1M"}


def ic(name, cls=""):
    """A single-colour Figma icon, tinted by CSS through a mask (as nb-ic does)."""
    return '<span class="xa-ic %s" style="--i: url(%s%s)" aria-hidden="true"></span>' % (cls, IMG, name)


def arrow_btn(label, href=None, sr=""):
    inner = '<span>%s</span>%s' % (label, ic("arrow.svg"))
    extra = ' <span class="sr-only">%s</span>' % sr if sr else ""
    if href:
        return '<a class="xa-view" href="%s">%s%s</a>' % (href, inner, extra)
    return '<button type="button" class="xa-view">%s%s</button>' % (inner, extra)


def head(title, sub, view, nav=""):
    return ('<header class="xa-head"><div><h2 class="xa-head__title">%s</h2><p class="xa-head__sub">%s</p></div>'
            '<div class="xa-head__end">%s%s</div></header>' % (title, sub, nav, view))


def hero():
    bars = "".join('<i style="--i:%d"%s></i>' % (k, ' class="on"' if k < 20 else "") for k in range(25))
    facts = "".join('<div><dt>%s</dt><dd>%s</dd></div>' % kv for kv in
                    (("Tenure", "2 Yrs"), ("Payout", "Monthly"), ("Min Inv.", "₹5k")))
    return """<section class="xa-hero" aria-labelledby="xa-title">
  <span class="xa-hero__rays" aria-hidden="true"><img src="{img}hero-rays.jpg" alt=""></span>
  <h1 class="xa-hero__title xa-in" id="xa-title"><span class="xa-gold">Earn More</span> than Traditional FDs</h1>
  <p class="xa-hero__sub xa-in" style="--d:1">Bonds earn up to <span class="xa-gold">12.85% annual returns</span> nearly double what most bank FDs offer.</p>
  <!-- DATA: the featured launch issue (Figma sample). -->
  <article class="xa-launch xa-in" style="--d:2">
    <span class="xa-launch__streak xa-launch__streak--a" aria-hidden="true"><img src="{img}hero-glow.jpg" alt=""></span>
    <span class="xa-launch__streak xa-launch__streak--b" aria-hidden="true"><img src="{img}hero-glow.jpg" alt=""></span>
    <div class="xa-launch__body">
      <p class="xa-launch__eyebrow">Launch Event</p>
      <h2 class="xa-launch__name">Suryoday Bank of Smiles</h2>
      <dl class="xa-launch__facts">{facts}<div class="xa-launch__sold"><dt>Soldout 87%</dt><dd class="xa-seg" role="img" aria-label="87% sold">{bars}</dd></div></dl>
    </div>
    <div class="xa-launch__side">
      <p class="xa-launch__rate"><span data-count="13.15">13.15</span><small>%</small></p>
      <a class="xa-launch__cta" href="{href}">Explore</a>
    </div>
  </article>
</section>""".format(img=IMG, facts=facts, bars=bars, href=BOND_HREF)


def experience():
    cells = "".join('<li><img src="%s%s" alt="" width="44" height="44"><span>%s</span></li>' % (IMG, f, t)
                    for f, t in STATS)
    return ('<section class="xa-exp" data-reveal aria-labelledby="xa-exp-t">'
            '<h2 class="xa-rule" id="xa-exp-t">The Golden Experience Of Investing</h2>'
            '<ul class="xa-exp__row">%s</ul>'
            '<button type="button" class="xa-exp__view">View</button></section>' % cells)


def collections():
    tiles = "".join('<li><a class="xa-col" href="%s"><img src="%s%s" alt="" width="44" height="44"><span>%s</span></a></li>'
                    % (h, IMG, f, t) for f, t, h in COLLECTIONS)
    return ('<section class="xa-cols" data-reveal aria-labelledby="xa-cols-t">'
            '<h2 class="xa-rule" id="xa-cols-t">Collections</h2><ul class="xa-cols__row">%s</ul></section>' % tiles)


def bond(kind, shield="shield.svg", i=0):
    b = BOND
    return """<li style="--i:{i}"><a class="xa-bond xa-bond--{kind}" href="{href}">
  <span class="xa-bond__sold">{sold}</span>
  <span class="xa-bond__rate">{rate}<small>%</small></span>
  <h3 class="xa-bond__name">{name}</h3>
  <span class="xa-bond__min">{min}</span>
  <dl class="xa-bond__facts"><div><dt>Rating</dt><dd><img src="{img}{shield}" alt="" width="8" height="8">{rating}</dd></div><div><dt>Payout</dt><dd>{payout}</dd></div><div><dt>Tenure</dt><dd>{tenure}</dd></div></dl>
</a></li>""".format(i=i, kind=kind, href=BOND_HREF, img=IMG, shield=shield, **b)


def shelf(kind, title, sub, href, count, shield="shield.svg", carousel=False):
    cards = "".join(bond(kind, shield, k) for k in range(count))
    sid = "xa-%s" % kind
    track = '<ul class="xa-shelf__row%s" id="%s-row"%s>%s</ul>' % (
        " xa-track" if carousel else "", sid, ' tabindex="0" aria-label="%s"' % title if carousel else "", cards)
    nav = carousel_nav(sid + "-row", title) if carousel else ""
    return ('<!-- DATA: %s bonds (Figma sample, one bond repeated). -->\n'
            '<section class="xa-shelf xa-shelf--%s" data-reveal aria-labelledby="%s-t">%s%s</section>'
            % (title, kind, sid, head('<span id="%s-t">%s</span>' % (sid, title), sub,
                                      arrow_btn("View", href, "all %s" % title.lower() if title.endswith("Bonds") else "all %s bonds" % title), nav), track))


def carousel_nav(target, label):
    return ('<div class="xa-nav" data-track="%s">'
            '<button type="button" class="xa-nav__btn" data-dir="-1" aria-label="Previous %s">%s</button>'
            '<button type="button" class="xa-nav__btn" data-dir="1" aria-label="Next %s">%s</button></div>'
            % (target, label, ic("arrow.svg", "xa-ic--flip"), label, ic("arrow.svg")))


def try_strip():
    feats = "".join('<li>%s<span>%s</span></li>' % (ic(f, "xa-ic--gold").replace('" aria', ';--s:%s" aria' % sz, 1), t) for f, sz, t in
                    (("ic-graph.svg", "11px", "No volatility"), ("ic-bag.svg", "11px", "Sell anytime"), ("ic-lock.svg", "16px", "Fixed high returns")))
    return ('<!-- DATA: starting yield (Figma sample). -->\n'
            '<section class="xa-try" data-reveal aria-label="Try bonds">'
            '<div><p class="xa-try__lead">Try bonds today start with ₹10,000.</p><ul class="xa-try__feats">%s</ul></div>'
            '<p class="xa-try__rate">13.29<small>%%</small></p></section>' % feats)


def do_more():
    cards = [
        ("do-webinar.png", 64, "Build a 12%+ stable monthly income portfolio.",
         '<span class="xa-do__pill">Online Webinar</span>', '<button type="button" class="xa-gold-btn">Join Today, 4:00 PM</button>'),
        ("do-community.png", 60, "Join India's biggest bond community",
         '<span class="xa-do__meta">5L+ Investors • Exclusive Deals</span>', '<button type="button" class="xa-gold-btn">Join Community</button>'),
        ("do-gift.png", 60, "Refer &amp; Earn",
         '<span class="xa-do__meta">Refer and get rewarded with offers and discounts</span>',
         '<a class="xa-gold-btn" href="refer-and-earn.html">Refer now</a>'),
    ]
    lis = "".join('<li style="--i:%d" class="xa-do"><img src="%s%s" alt="" width="%d" height="%d"><h3>%s</h3>%s%s</li>'
                  % (k, IMG, f, s, s, t, extra, cta) for k, (f, s, t, extra, cta) in enumerate(cards))
    return ('<!-- DATA: webinar time and community figures (Figma sample). -->\n'
            '<section class="xa-domore" data-reveal aria-labelledby="xa-do-t">%s'
            '<ul class="xa-domore__row">%s</ul></section>'
            % (head('<span id="xa-do-t">Do More with GoldenPi</span>', "Unlock Smarter Fixed Income Opportunities",
                    arrow_btn("View", None, "more from GoldenPi")), lis))


def kyc_art():
    """The Figma's KYC illustration (node 40:2704), its layers at the design's offsets."""
    layers = [  # (file, left, top, width, height, extra class/style)
        ("kyc-beam1.svg", 13.11, 0, 91.309, 66.95, "xa-art__beam"),
        ("kyc-beam2.svg", 0, 25.09, 119.606, 54.623, "xa-art__beam"),
        ("kyc-p0.svg", 10.89, 82.73, 97.381, 3.141, ""),
        ("kyc-p1.svg", 11.35, 67.39, 95.701, 15.712, ""),
        ("kyc-p2.svg", 11.35, 79.49, 95.701, 3.601, ""),
        ("kyc-p3.svg", 11.89, 66.44, 94.817, 13.97, ""),
    ]
    out = "".join('<img class="%s" src="%s%s" alt="" style="left:%spx;top:%spx;width:%spx;height:%spx">'
                  % (c, IMG, f, l, t, w, h) for f, l, t, w, h, c in layers)
    out += ('<img class="xa-art__beam" src="%skyc-ray1.svg" alt="" style="left:18.35px;top:24.08px;width:6.795px;height:42.76px;transform:rotate(-2.12deg)">'
            '<img class="xa-art__beam" src="%skyc-ray2.svg" alt="" style="left:92.58px;top:24.17px;width:6.776px;height:42.884px;transform:rotate(17.83deg)">'
            '<img class="xa-art__shield" src="%skyc-shield.png" alt="" style="left:41.64px;top:7.99px;width:43px;height:54px">' % (IMG, IMG, IMG))
    # Its light beams are black-to-amber with screen blending: they need the
    # dark ground they were drawn on, so the art sits in a small dark tile.
    return '<span class="xa-art-well" aria-hidden="true"><span class="xa-art">%s</span></span>' % out


def portfolio_card():
    """portfolio.html's Active investment card, exactly (pages/_portfolio.py)."""
    return ("<!-- DATA: portfolio totals, sample values from the portfolio design. -->\n"
            + P.card_active().strip().replace('<article class="pf-gcard"', '<article class="pf-gcard" data-reveal', 1))


# Its info button opens portfolio.html's "Active investment" definitions sheet.
SHEET = P.SHEETS[:P.SHEETS.index('<dialog class="pf-sheet" id="sheet-lifetime"')]


def rail():
    return """<aside class="xa-rail" aria-label="Your account">
  <h2 class="xa-rail__label">My Investment</h2>
  <div class="xa-kyc" data-reveal>
    <div><p class="xa-kyc__text">Complete your 1 time KYC<br>&amp; Earn upto 14% return</p>
    <p class="xa-kyc__time"><img src="{img}kyc-bolt.svg" alt="" width="16" height="18">It just takes 2mins</p></div>
    {art}
  </div>
  <h2 class="xa-rail__label">Invest to unlock your portfolio</h2>
  <!-- DATA: portfolio values, shown once the investor has holdings. -->
  {port}
  <div class="xa-pending" data-reveal>
    <h2 class="xa-pending__title">Pending KYC Verification Required<span class="xa-pending__dot" aria-hidden="true"></span></h2>
    <div class="xa-pending__row">
      <span class="xa-pending__state"><span class="xa-pending__face">{face}</span>Pending</span>
      <button type="button" class="xa-gold-btn xa-gold-btn--sm">Start Now<img src="{img}arrow-sm.svg" alt="" width="12" height="12"></button>
    </div>
  </div>
</aside>""".format(img=IMG, art=kyc_art(), port=portfolio_card(), face=ic("kyc-face.svg"))


def body():
    main = (experience() + collections()
            + shelf("gold", "High-Yield", "Maximize your returns", "collections-high-returns.html", 3)
            + shelf("rose", "High Rated", "Secure your portfolio with A+ rated bonds", "collections-highly-rated.html", 3,
                    shield="shield-rose.svg")
            + try_strip()
            + shelf("light", "Trending Bonds", "Prioritizing safety and liquidity.", "collections-all-bonds.html", 4,
                    carousel=True)
            + do_more())
    return ('<main id="main-content" class="xa-page"><div class="xa"><div class="xa-hero-wrap">%s</div>%s'
            '<div class="xa-main">%s</div></div></main>' % (hero(), rail(), main))


STYLE = """<style>
/* user-explore-app: Figma 40:2105, light version. Hero in the Figma's black and
   gold; everything after it in the harvested light tokens. Scoped to .xa-page. */
.xa-page {
  --ink: #322811; --sub: #666666; --bronze: #8a6520; --gold: #d4af37; --line: #e7e3d9;
  --cream: #fbf6e9; --card: #ffffff; --page: #f7f5f2;
  --gold-grad: linear-gradient(135deg, #f9e29c 0%, #d4af37 30%, #a67c00 70%, #c6a34f 100%);
  --ease: cubic-bezier(0.16, 1, 0.3, 1);
  --shadow: 0 1px 2px rgba(80, 60, 10, .05), 0 12px 28px -14px rgba(80, 60, 10, .22);
  background: var(--page); color: var(--ink); padding-bottom: 72px;
}
/* Resets in :where() so they never outrank a component rule. */
:where(.xa-page) *, :where(.xa-page) *::before, :where(.xa-page) *::after { box-sizing: border-box; }
:where(.xa-page) :where(h1, h2, h3, p, ul, dl, dd) { margin: 0; padding: 0; }
:where(.xa-page) ul { list-style: none; }
:where(.xa-page) a { color: inherit; text-decoration: none; }
.xa-page :focus-visible { outline: 2px solid var(--bronze); outline-offset: 3px; border-radius: 12px; }
.xa-page .sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
.xa-ic { display: inline-block; width: 18px; height: 18px; flex: none; background: currentColor;
  -webkit-mask: var(--i) center / contain no-repeat; mask: var(--i) center / contain no-repeat; }
.xa-ic--flip { transform: scaleX(-1); }
.xa-ic--gold { width: 16px; height: 16px; background: var(--gold-grad); -webkit-mask-size: var(--s, 16px); mask-size: var(--s, 16px); }
.xa-gold { background: linear-gradient(170deg, #f9e29c 0%, #d4af37 30%, #a67c00 70%, #c6a34f 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent; }

/* Layout: main column + 360px rail, on the navbar's 1200px shell. */
/* The container is 1200px itself; the screen gutter sits outside it. */
.xa { width: min(1200px, 100% - 40px); margin: 0 auto; padding: 24px 0 0; display: grid; gap: 28px;
  grid-template-areas: "hero" "rail" "main"; grid-template-columns: minmax(0, 1fr); }
.xa-hero-wrap { grid-area: hero; min-width: 0; }
.xa-rail { grid-area: rail; min-width: 0; }
.xa-main { grid-area: main; min-width: 0; display: grid; grid-template-columns: minmax(0, 1fr); gap: 40px; }
.xa-main > * { min-width: 0; }
/* Two columns from 1200px: below that the main column would drop under ~700px and the
   three-across cards, plans and CTAs stop fitting. Tablets get the rail as a 2x2 band. */
@media (min-width: 768px) and (max-width: 1199px) {
  .xa-rail { grid-template-columns: repeat(2, minmax(0, 1fr)); column-gap: 20px; align-items: start; }
  .xa-rail > :nth-child(1) { grid-area: 1 / 1; }
  .xa-rail > :nth-child(2) { grid-area: 2 / 1; }
  .xa-rail > :nth-child(3) { grid-area: 1 / 2; }
  .xa-rail > .xa-rail__label:nth-child(3) { margin-top: 0; }
  .xa-rail > :nth-child(4) { grid-area: 2 / 2; }
  .xa-rail > :nth-child(5) { grid-column: 1 / -1; margin-top: 4px; }
}
@media (min-width: 1200px) {
  /* Hero and main share one 810px column; the 1200px shell leaves a 30px gutter to the rail. */
  .xa { grid-template-areas: "hero rail" "main rail"; grid-template-columns: minmax(0, 810px) 360px;
    justify-content: space-between; column-gap: 30px; row-gap: 36px; padding-top: 32px; }
  .xa-rail { align-self: start; position: sticky; top: 96px; }
}

/* ---------------------------------------------------------------- hero (dark) */
.xa-hero { position: relative; isolation: isolate; overflow: hidden; border-radius: 24px; padding: 28px 28px 30px;
  background: #0a0805; box-shadow: 0 30px 60px -30px rgba(50, 40, 17, .55); }
/* The Figma's "bg" light rays (node 40:2175), framed and cropped as the design has them. */
.xa-hero__rays { position: absolute; left: 112px; top: -98px; width: 904px; height: 372px; overflow: hidden; z-index: -1; pointer-events: none;
  -webkit-mask-image: linear-gradient(90deg, transparent, #000 30%); mask-image: linear-gradient(90deg, transparent, #000 30%); }
.xa-hero__rays img { position: absolute; left: 0; top: -29.49%; width: 100%; height: 139.87%; max-width: none; }
.xa-hero__title { font-size: clamp(22px, 3vw, 26px); line-height: 1.44; font-weight: 700; color: rgba(255, 255, 255, .9); letter-spacing: -.01em; }
.xa-hero__sub { margin-top: 8px; font-size: 16px; line-height: 1.4; font-weight: 500; color: rgba(255, 255, 255, .8); max-width: 60ch; }
.xa-hero__sub .xa-gold { background-image: linear-gradient(173deg, #f9e29c 21%, #e9b50c 60%, #a67c00 100%); }

.xa-launch { position: relative; margin-top: 30px; display: flex; gap: 32px; align-items: flex-end; justify-content: space-between;
  min-height: 165px; padding: 26px 32px 24px 41px; border-radius: 20px; overflow: hidden; color: #000;
  background:
    radial-gradient(ellipse 141% 141% at 100% 100%, #fedb37 0%, #fdb931 8%, #ce992d 19%, #9f7928 30%, #8a6e2f 40%, rgba(138, 110, 47, 0) 80%),
    radial-gradient(ellipse 141% 141% at 0% 0%, #ffffff 0%, #ffffd6 4%, #ffffac 8%, #e8da88 23%, #d1b464 38%, #bb9c4e 50%, #a58337 62.5%, #81672b 81%, #5d4a1f 100%);
  box-shadow: 0 0 0 1px rgba(255, 255, 255, .1), 0 24px 50px -20px rgba(212, 175, 55, .45); }
/* A slow gold sheen crossing the card once it is in view, then on hover. */
.xa-launch::after { content: ""; position: absolute; inset: 0; pointer-events: none; transform: translateX(-120%);
  background: linear-gradient(105deg, transparent 35%, rgba(255, 255, 255, .45) 50%, transparent 65%); }
.xa-launch:hover::after, .xa-launch.is-lit::after { animation: xa-sheen 1.4s var(--ease); }
@keyframes xa-sheen { to { transform: translateX(120%); } }
.xa-launch__streak { position: absolute; overflow: hidden; mix-blend-mode: lighten; transform: rotate(180deg); pointer-events: none; }
.xa-launch__streak img { position: absolute; max-width: none; height: 169.92%; top: -69.08%; }
.xa-launch__streak--a { left: 10.95%; right: 2.77%; top: -0.5%; height: 12.5%; }
.xa-launch__streak--a img { width: 128.59%; left: -24.67%; }
.xa-launch__streak--b { left: 0; right: 8.47%; top: 0; height: 12.5%; }
.xa-launch__streak--b img { width: 121.21%; left: -6.53%; }
.xa-launch__body, .xa-launch__side { position: relative; }
.xa-launch__body { flex: 1; min-width: 0; }
.xa-launch__eyebrow { font-size: 10px; line-height: 13.5px; font-weight: 700; letter-spacing: 2.25px; text-transform: uppercase; }
.xa-launch__name { margin-top: 9px; font-size: clamp(22px, 3vw, 28px); line-height: 1.2; font-weight: 400; letter-spacing: -.6px; }
.xa-launch__facts { margin-top: 16px; display: flex; flex-wrap: wrap; gap: 12px 30px; }
@media (min-width: 1100px) { .xa-launch__facts { flex-wrap: nowrap; } }
.xa-launch__facts dt, .xa-launch__facts dd { white-space: nowrap; }
.xa-launch__facts dt { font-size: 10px; line-height: 12px; font-weight: 700; letter-spacing: .8px; text-transform: uppercase; }
.xa-launch__facts dd { margin-top: 2px; font-size: 16px; line-height: 28px; font-weight: 700; }
.xa-seg { display: flex; gap: 2px; padding-top: 12px; }
.xa-seg i { width: 6.9px; height: 6px; border-radius: 1px; background: rgba(40, 32, 8, .1); }
.xa-seg i.on { background: #4a3608; opacity: .8; border-radius: 2px; }
.xa-launch__side { flex: none; display: flex; flex-direction: column; align-items: flex-end; gap: 15px; }
.xa-launch__rate { display: flex; align-items: flex-end; gap: 4px; font-size: 60px; line-height: 1; font-weight: 500; letter-spacing: -2px; font-variant-numeric: tabular-nums; }
.xa-launch__rate small { font-size: 28px; line-height: 36px; font-weight: 400; color: #111; letter-spacing: 0; }
.xa-launch__cta { display: inline-flex; align-items: center; justify-content: center; width: 145px; height: 35px; border-radius: 44px;
  font-size: 12px; line-height: 14px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #fcfcfc;
  background: radial-gradient(ellipse 140% 140% at 100% 100%, #27272a 8%, #252528 54%, #171719 77%, #090909 100%);
  box-shadow: 0 20px 20px -6px rgba(0, 0, 0, .3); transition: transform .3s var(--ease), box-shadow .3s var(--ease); }
.xa-launch__cta:hover { transform: translateY(-2px); box-shadow: 0 24px 24px -8px rgba(0, 0, 0, .4); }
.xa-launch__cta:active { transform: scale(.98); }

/* Entrance: headline, sub, card in sequence. */
@media (prefers-reduced-motion: no-preference) {
  .xa-in { animation: xa-up .9s var(--ease) both; animation-delay: calc(var(--d, 0) * 110ms + 80ms); }
  .xa-seg i { transform-origin: left; animation: xa-seg .5s var(--ease) both; animation-delay: calc(var(--i) * 28ms + 700ms); }
}
@keyframes xa-up { from { opacity: 0; transform: translateY(18px); } }
@keyframes xa-seg { from { opacity: 0; transform: scaleX(.2); } }

/* ------------------------------------------------------------- light blocks */
.xa-rule { display: flex; align-items: center; justify-content: center; gap: 8px; font-size: 14px; line-height: 12px; font-weight: 700;
  text-transform: capitalize; color: var(--bronze); }
.xa-rule::before, .xa-rule::after { content: ""; width: 24px; height: 1px; opacity: .7; background: linear-gradient(90deg, rgba(179, 135, 40, 0), #b38728); }
.xa-rule::after { transform: scaleX(-1); }

.xa-exp { position: relative; display: grid; gap: 14px; padding-bottom: 12px; }
.xa-exp__row { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); align-items: center; padding: 20px 16px;
  border-radius: 20px; background: var(--card); border: 1px solid var(--line); box-shadow: var(--shadow); }
.xa-exp__row li { display: flex; flex-direction: column; align-items: center; gap: 12px; text-align: center;
  font-size: 14px; line-height: 1.2; font-weight: 500; letter-spacing: .5px; color: var(--ink); }
.xa-exp__row li + li { border-left: 1px solid var(--line); }
.xa-exp__row img { width: 44px; height: 44px; object-fit: contain; transition: transform .4s var(--ease); }
.xa-exp__row li:hover img { transform: translateY(-3px) scale(1.06); }
.xa-exp__view { position: absolute; left: 50%; bottom: 0; transform: translateX(-50%); padding: 4px 11px; border: 0; border-radius: 45px; cursor: pointer;
  font: inherit; font-size: 10px; line-height: 11.6px; font-weight: 700; letter-spacing: .39px; text-transform: uppercase; color: #000;
  background: var(--gold-grad); box-shadow: inset 0 1px 2px rgba(255, 255, 255, .6), 0 8px 18px -6px rgba(166, 124, 0, .5); }

.xa-cols { display: grid; gap: 14px; }
.xa-cols__row { display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 14px; }
.xa-col { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px; height: 120px; padding: 10px 8px 12px;
  border-radius: 20px; background: var(--card); border: 1px solid var(--line); box-shadow: var(--shadow);
  font-size: 14px; line-height: 16.5px; font-weight: 500; letter-spacing: .14px; text-align: center; color: var(--ink);
  transition: transform .35s var(--ease), border-color .35s var(--ease), box-shadow .35s var(--ease); }
.xa-col img { width: 44px; height: 44px; object-fit: contain; transition: transform .45s var(--ease); }
.xa-col:hover { transform: translateY(-3px); border-color: rgba(212, 175, 55, .55); box-shadow: 0 18px 34px -18px rgba(166, 124, 0, .45); }
.xa-col:hover img { transform: scale(1.1) rotate(-4deg); }
.xa-col:active { transform: scale(.98); }

/* Section header + View pill */
.xa-head { display: flex; align-items: flex-end; justify-content: space-between; gap: 16px; margin-bottom: 20px; }
.xa-head__title { font-size: 18px; line-height: 28px; font-weight: 700; color: var(--ink); }
.xa-head__sub { margin-top: 3px; font-size: 14px; line-height: 19.5px; color: var(--sub); }
.xa-shelf--gold .xa-head__title { color: var(--bronze); }
.xa-shelf--rose .xa-head__title { color: #a35a3c; }
.xa-view { flex: none; display: inline-flex; align-items: center; gap: 6px; height: 38px; padding: 0 14px 0 18px; border-radius: 999px; cursor: pointer;
  font: inherit; font-size: 14px; font-weight: 700; text-transform: uppercase; color: var(--bronze);
  background: linear-gradient(157deg, rgba(255, 255, 255, .9), rgba(255, 255, 255, .5)); border: 1px solid rgba(138, 101, 32, .22);
  transition: background-color .3s var(--ease), border-color .3s var(--ease); }
.xa-view .xa-ic { transition: transform .3s var(--ease); }
.xa-view:hover { border-color: var(--bronze); }
.xa-view:hover .xa-ic { transform: translateX(3px); }

/* Bond cards: gold and rose keep the Figma's metal; Trending turns light. */
.xa-shelf__row { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 19px; }
.xa-bond { position: relative; display: grid; grid-template-columns: 1fr auto; grid-template-rows: auto auto auto 1fr;
  height: 172px; padding: 16px 18px 14px; border-radius: 20px; overflow: hidden; color: #282008;
  transition: transform .4s var(--ease), box-shadow .4s var(--ease); }
.xa-bond::after { content: ""; position: absolute; inset: 0; pointer-events: none; transform: translateX(-120%);
  background: linear-gradient(105deg, transparent 35%, rgba(255, 255, 255, .35) 50%, transparent 65%); }
.xa-bond:hover { transform: translateY(-4px); }
.xa-bond:hover::after { animation: xa-sheen 1.1s var(--ease); }
.xa-bond:active { transform: scale(.98); }
.xa-bond__sold { grid-column: 1; grid-row: 1; align-self: start; justify-self: start; padding: 3px 9px; border-radius: 999px; font-size: 10px; line-height: 13.5px; font-weight: 700;
  letter-spacing: .9px; text-transform: uppercase; color: #3e2d11; background: rgba(40, 32, 8, .1); border: 1px solid rgba(40, 32, 8, .1);
  -webkit-backdrop-filter: blur(6px); backdrop-filter: blur(6px); }
.xa-bond__rate { grid-column: 2; grid-row: 1 / 3; margin-top: -8px; align-self: start; font-size: 26px; line-height: 35px; font-weight: 500; letter-spacing: -1px; font-variant-numeric: tabular-nums; }
.xa-bond__rate small { margin-left: 2px; font-size: 12px; font-weight: 400; letter-spacing: 0; color: #342600; }
.xa-bond__name { grid-column: 1 / -1; margin-top: 6px; font-size: 16px; line-height: 21.88px; font-weight: 700; }
.xa-bond__min { grid-column: 1 / -1; font-size: 11px; line-height: 13.5px; font-weight: 700; text-transform: uppercase; }
.xa-bond__facts { grid-column: 1 / -1; align-self: end; display: grid; grid-template-columns: repeat(3, 1fr); height: 58px; align-items: center;
  border-radius: 12px; background: rgba(40, 32, 8, .05); border: 1px solid rgba(40, 32, 8, .1); text-align: center; }
.xa-bond__facts div + div { border-left: 1px solid rgba(40, 32, 8, .1); }
.xa-bond__facts dt { font-size: 10px; line-height: 10.5px; font-weight: 700; text-transform: uppercase; color: #342600; }
.xa-bond__facts dd { margin-top: 6px; display: flex; align-items: center; justify-content: center; gap: 3px;
  font-size: 12px; line-height: 15px; font-weight: 700; letter-spacing: -.12px; }
.xa-bond--gold { border: 1px solid rgba(246, 213, 122, .1);
  background:
    radial-gradient(ellipse 141% 141% at 100% 100%, #fedb37 0%, #fdb931 8%, #ce992d 19%, #9f7928 30%, #8a6e2f 40%, rgba(138, 110, 47, 0) 80%),
    radial-gradient(ellipse 141% 141% at 0% 0%, #ffffff 0%, #ffffd6 4%, #ffffac 8%, #e8da88 16.5%, #d1b464 25%, #b49a53 38%, #977f42 52%, #7a6530 65%, #5d4a1f 79%, #5d4a1f 100%);
  box-shadow: 0 20px 40px -10px rgba(237, 201, 103, .35); }
.xa-bond--gold:hover { box-shadow: 0 26px 46px -12px rgba(212, 175, 55, .55); }
.xa-bond--rose { color: #39160f; border: 1px solid rgba(255, 219, 207, .4);
  background: radial-gradient(ellipse 141% 141% at 100% 100%, #ffdbcf 0%, #e0a995 20%, #c38c77 35%, #a66e58 50%, #8e5744 75%, #75402f 100%);
  box-shadow: 0 20px 40px -10px rgba(224, 169, 149, .45); }
.xa-bond--rose:hover { box-shadow: 0 26px 46px -12px rgba(195, 140, 119, .6); }
.xa-bond--rose .xa-bond__sold { color: #39160f; background: rgba(57, 22, 15, .1); border-color: rgba(57, 22, 15, .1); }
.xa-bond--rose .xa-bond__rate small, .xa-bond--rose .xa-bond__facts dt { color: #39160f; }
.xa-bond--rose .xa-bond__facts, .xa-bond--rose .xa-bond__facts div + div { border-color: rgba(57, 22, 15, .1); }
.xa-bond--light { color: var(--ink); background: var(--card); border: 1px solid var(--line); box-shadow: var(--shadow); }
.xa-bond--light::after { background: linear-gradient(105deg, transparent 35%, rgba(237, 201, 103, .18) 50%, transparent 65%); }
.xa-bond--light:hover { border-color: rgba(212, 175, 55, .55); box-shadow: 0 22px 40px -20px rgba(166, 124, 0, .4); }
.xa-bond--light .xa-bond__sold { color: var(--ink); background: var(--cream); border-color: rgba(212, 175, 55, .3); }
.xa-bond--light .xa-bond__rate small, .xa-bond--light .xa-bond__facts dt { color: var(--sub); }
.xa-bond--light .xa-bond__min { color: var(--sub); font-weight: 500; letter-spacing: .6px; }
.xa-bond--light .xa-bond__name { font-weight: 500; font-size: 18px; }
.xa-bond--light .xa-bond__facts { background: #faf7f0; border-color: var(--line); }
.xa-bond--light .xa-bond__facts div + div { border-color: var(--line); }

/* Carousels: scroll-snap tracks with prev/next. */
.xa-track { display: grid; grid-auto-flow: column; grid-template-columns: none; gap: 14px; overflow-x: auto; scroll-snap-type: x mandatory;
  overscroll-behavior-x: contain; scrollbar-width: none; padding: 4px 4px 26px; margin: -4px -4px -22px; scroll-padding-inline: 4px; }
.xa-track::-webkit-scrollbar { display: none; }
.xa-track > li { scroll-snap-align: start; }
.xa-shelf--light .xa-track { grid-auto-columns: calc((100% - 2 * 19px) / 3); gap: 19px; }
.xa-head__end { flex: none; display: flex; align-items: center; gap: 8px; }
.xa-nav { display: flex; gap: 8px; }
.xa-nav__btn { display: grid; place-items: center; width: 38px; height: 38px; border-radius: 999px; cursor: pointer; color: var(--bronze);
  background: var(--card); border: 1px solid var(--line); transition: border-color .3s var(--ease), transform .2s var(--ease), opacity .3s; }
.xa-nav__btn:hover { border-color: var(--bronze); }
.xa-nav__btn:active { transform: scale(.94); }
.xa-nav__btn:disabled { opacity: .35; cursor: default; }

/* Try-bonds strip */
.xa-try { position: relative; overflow: hidden; display: flex; align-items: center; justify-content: space-between; gap: 20px;
  padding: 18px 34px 18px 20px; border-radius: 20px; background: linear-gradient(120deg, #fffdf6, var(--cream));
  border: 1px solid rgba(229, 184, 102, .45); box-shadow: 0 20px 40px -24px rgba(166, 124, 0, .35); }
.xa-try::before, .xa-try::after { content: ""; position: absolute; width: 300px; height: 300px; border-radius: 50%; background: #edc967;
  filter: blur(75px); opacity: .22; pointer-events: none; }
.xa-try::before { left: -25px; top: -187px; }
.xa-try::after { left: 315px; top: 3px; }
.xa-try > * { position: relative; }
.xa-try__lead { font-size: 14px; line-height: 1.36; font-weight: 500; color: var(--bronze); }
.xa-try__feats { margin-top: 10px; display: flex; flex-wrap: wrap; gap: 8px 40px; }
.xa-try__feats li { display: flex; align-items: center; gap: 4px; font-size: 14px; line-height: 1.36; font-weight: 500; color: var(--ink); }
.xa-try__rate { flex: none; font-size: 40px; line-height: 35px; font-weight: 500; letter-spacing: -1.75px;
  background: linear-gradient(118deg, #d4af37 0%, #a67c00 55%, #8a6520 100%); -webkit-background-clip: text; background-clip: text; color: transparent; }
.xa-try__rate small { margin-left: 4px; font-size: 20px; letter-spacing: 0; }

/* Do More */
.xa-domore__row { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 19px; }
.xa-do { display: flex; flex-direction: column; min-height: 263px; padding: 24px 20px 20px; border-radius: 20px; background: var(--card);
  border: 1px solid var(--line); box-shadow: var(--shadow); transition: transform .4s var(--ease), box-shadow .4s var(--ease); }
.xa-do:hover { transform: translateY(-3px); box-shadow: 0 22px 40px -20px rgba(166, 124, 0, .4); }
.xa-do img { object-fit: contain; transition: transform .5s var(--ease); }
.xa-do:hover img { transform: translateY(-4px) rotate(-5deg); }
.xa-do h3 { margin-top: 16px; font-size: 19px; line-height: 26.25px; font-weight: 500; color: var(--ink); max-width: 237px; }
.xa-do__pill { align-self: flex-start; margin-top: 12px; padding: 3px 10px; border-radius: 999px; font-size: 9px; line-height: 13.5px; font-weight: 700;
  letter-spacing: .45px; text-transform: uppercase; color: var(--bronze); background: rgba(237, 201, 103, .14); border: 1px solid rgba(212, 175, 55, .35); }
.xa-do__meta { margin-top: 10px; font-size: 10.5px; line-height: 14px; font-weight: 700; letter-spacing: 1.05px; text-transform: uppercase; color: #6b7280; }
.xa-do .xa-gold-btn { margin-top: auto; }
.xa-do__pill, .xa-do__meta { margin-bottom: 20px; }
.xa-gold-btn { display: inline-flex; align-items: center; justify-content: center; gap: 5px; height: 43px; border: 0; border-radius: 44px; cursor: pointer;
  font: inherit; font-size: 10.5px; line-height: 14px; font-weight: 700; letter-spacing: 1.05px; text-transform: uppercase; color: #000;
  background: var(--gold-grad); box-shadow: inset 0 1px 2px rgba(255, 255, 255, .6), 0 12px 22px -12px rgba(166, 124, 0, .7);
  transition: transform .3s var(--ease), box-shadow .3s var(--ease), filter .3s; }
.xa-gold-btn:hover { transform: translateY(-2px); filter: saturate(1.1); box-shadow: inset 0 1px 2px rgba(255, 255, 255, .6), 0 16px 26px -12px rgba(166, 124, 0, .8); }
.xa-gold-btn:active { transform: scale(.98); }
.xa-gold-btn--sm { height: 30px; padding: 0 15px; font-size: 12px; letter-spacing: 1px; }

/* ---------------------------------------------------------------- rail */
.xa-rail { display: grid; gap: 16px; }
.xa-rail__label { font-size: 16px; line-height: 20px; font-weight: 500; color: var(--sub); }
.xa-rail__label:not(:first-child) { margin-top: 21px; }
.xa-kyc { display: flex; align-items: center; justify-content: space-between; gap: 2px; padding: 20px 18px; border-radius: 20px;
  background: linear-gradient(140deg, #ffffff 40%, var(--cream)); border: 1px solid rgba(212, 175, 55, .3);
  box-shadow: 0 8px 20px rgba(245, 158, 11, .16); }
.xa-kyc > div:first-child { flex: 1; min-width: 0; }
.xa-kyc__text { white-space: nowrap; font-size: 13px; line-height: 1.4; font-weight: 500; letter-spacing: .13px; color: var(--ink); }
.xa-kyc__time { margin-top: 20px; display: flex; align-items: center; gap: 10px; font-size: 13px; line-height: 1.36; font-weight: 600; color: #b25a00; }
.xa-art-well { flex: none; display: grid; place-items: center; width: 112px; height: 96px; border-radius: 16px; isolation: isolate; overflow: hidden;
  background: radial-gradient(ellipse 90% 80% at 50% 0%, #2a2112 0%, #0f0f0f 70%); box-shadow: inset 0 1px 0 rgba(255, 255, 255, .08); }
.xa-art { position: relative; width: 120px; height: 87px; flex: none; transform: scale(.9); }
.xa-art img { position: absolute; max-width: none; }
.xa-art__beam { mix-blend-mode: screen; }
@media (prefers-reduced-motion: no-preference) {
  .xa-art__shield { animation: xa-float 4.5s ease-in-out infinite; }
  .xa-art__beam { animation: xa-glow 4.5s ease-in-out infinite; }
}
@keyframes xa-float { 50% { transform: translateY(-3px); } }
@keyframes xa-glow { 50% { opacity: .55; } }
.xa-pending { margin-top: 21px; padding: 19px 18px 18px; border-radius: 20px; background: var(--card); border: 1px solid var(--line); box-shadow: var(--shadow); }
.xa-pending__title { display: flex; align-items: center; gap: 7px; font-size: 16px; line-height: 28px; font-weight: 700; color: var(--ink); white-space: nowrap; }
.xa-pending__dot { width: 5.25px; height: 5.25px; border-radius: 50%; background: #ef4444; box-shadow: 0 0 8px rgba(239, 68, 68, .6); }
@media (prefers-reduced-motion: no-preference) { .xa-pending__dot { animation: xa-pulse 2s ease-in-out infinite; } }
@keyframes xa-pulse { 50% { box-shadow: 0 0 0 5px rgba(239, 68, 68, 0), 0 0 8px rgba(239, 68, 68, .2); } }
.xa-pending__row { margin-top: 14px; display: flex; align-items: center; justify-content: space-between; gap: 12px; }
.xa-pending__state { display: flex; align-items: center; gap: 7px; font-size: 9px; line-height: 13.5px; font-weight: 700; letter-spacing: .9px; text-transform: uppercase; color: #6b7280; }
.xa-pending__face { display: grid; place-items: center; width: 33px; height: 33px; border-radius: 50%; color: var(--bronze); background: var(--cream); border: 1px solid var(--line); }
.xa-pending__face .xa-ic { width: 19.5px; height: 19.5px; }

/* Scroll reveal, children staggered (pages/_reveal.js adds .reveal-ready). */
.reveal-ready .xa-page [data-reveal] { opacity: 0; transform: translateY(22px); transition: opacity .8s var(--ease), transform .8s var(--ease); }
.reveal-ready .xa-page [data-reveal].is-in { opacity: 1; transform: none; }
.reveal-ready .xa-page [data-reveal] li[style*="--i"] { opacity: 0; transform: translateY(16px);
  transition: opacity .7s var(--ease), transform .7s var(--ease); transition-delay: calc(var(--i) * 80ms + 120ms); }
.reveal-ready .xa-page [data-reveal].is-in li[style*="--i"] { opacity: 1; transform: none; }

/* ------------------------------------------------------------- small screens */
@media (max-width: 767px) {
  .xa { width: calc(100% - 32px); padding: 16px 0 0; gap: 24px; }
  .xa-main { gap: 34px; }
  .xa-hero { padding: 22px 16px 18px; border-radius: 20px; }
  .xa-hero__rays { left: -380px; }
  .xa-hero__sub { font-size: 14px; }
  .xa-launch { flex-direction: column; align-items: stretch; gap: 18px; padding: 22px 18px 18px; }
  .xa-launch__side { flex-direction: row; align-items: center; justify-content: space-between; }
  .xa-launch__rate { font-size: 46px; }
  .xa-launch__facts { gap: 12px 22px; }
  .xa-exp__row { grid-template-columns: repeat(2, minmax(0, 1fr)); row-gap: 22px; }
  .xa-exp__row li:nth-child(3) { border-left: 0; }
  .xa-cols__row, .xa-shelf__row:not(.xa-track) { display: grid; grid-auto-flow: column; grid-template-columns: none; overflow-x: auto;
    scroll-snap-type: x mandatory; scrollbar-width: none; padding: 4px 16px 22px; margin: -4px -16px -18px; scroll-padding-inline: 16px; }
  .xa-cols__row { grid-auto-columns: 104px; }
  .xa-shelf__row:not(.xa-track) { grid-auto-columns: 239px; }
  .xa-cols__row > li, .xa-shelf__row > li { scroll-snap-align: start; }
  .xa-cols__row::-webkit-scrollbar, .xa-shelf__row::-webkit-scrollbar { display: none; }
  .xa-track { padding-inline: 16px; margin-inline: -16px; scroll-padding-inline: 16px; }
  .xa-domore__row { grid-template-columns: none; grid-auto-flow: column; grid-auto-columns: 262px; overflow-x: auto; scroll-snap-type: x mandatory;
    scrollbar-width: none; padding: 4px 16px 22px; margin: -4px -16px -18px; scroll-padding-inline: 16px; }
  .xa-domore__row > li { scroll-snap-align: start; }
  .xa-shelf--light .xa-track { grid-auto-columns: 239px; }
  .xa-nav { display: none; }
  .xa-try { flex-direction: column; align-items: flex-start; padding: 18px; }
  .xa-try__feats { gap: 8px 20px; }
  .xa-pending__title { white-space: normal; font-size: 15px; line-height: 22px; }
}
</style>
"""

SCRIPT = """<script>
// user-explore-app: carousel buttons, the launch rate count-up and card sheen.
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  document.querySelectorAll('.xa-nav').forEach(function (nav) {
    var track = document.getElementById(nav.dataset.track);
    var btns = nav.querySelectorAll('button');
    function sync() {
      var max = track.scrollWidth - track.clientWidth - 2;
      btns[0].disabled = track.scrollLeft <= 2;
      btns[1].disabled = track.scrollLeft >= max;
      nav.hidden = max <= 0;
    }
    btns.forEach(function (b) {
      b.addEventListener('click', function () {
        var step = track.firstElementChild.getBoundingClientRect().width + 14;
        track.scrollBy({ left: step * +b.dataset.dir, behavior: reduce ? 'auto' : 'smooth' });
      });
    });
    track.addEventListener('scroll', sync, { passive: true });
    window.addEventListener('resize', sync);
    sync();
  });

  // The portfolio card's info button: portfolio.html's definitions sheet.
  document.addEventListener('click', function (e) {
    var open = e.target.closest('[data-sheet]');
    if (open) { var d = document.getElementById(open.getAttribute('data-sheet')); if (d && d.showModal) d.showModal(); return; }
    if (e.target.closest('[data-close]')) { e.target.closest('dialog').close(); return; }
    if (e.target.tagName === 'DIALOG') e.target.close();
  });

  if (reduce || !('IntersectionObserver' in window)) return;
  var gio = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-lit'); gio.unobserve(e.target); } });
  }, { threshold: 0.5 });
  document.querySelectorAll('.pf-gcard').forEach(function (c) { gio.observe(c); });
  var card = document.querySelector('.xa-launch');
  var num = card && card.querySelector('[data-count]');
  if (!card) return;
  var io = new IntersectionObserver(function (es) {
    if (!es[0].isIntersecting) return;
    io.disconnect();
    setTimeout(function () { card.classList.add('is-lit'); }, 900);
    var end = parseFloat(num.dataset.count), dp = (num.dataset.count.split('.')[1] || '').length, t0 = null, dur = 1100;
    function tick(t) {
      t0 = t0 || t;
      var p = Math.min((t - t0) / dur, 1), e = 1 - Math.pow(1 - p, 4);
      num.textContent = (end * (0.82 + 0.18 * e)).toFixed(dp);
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }, { threshold: 0.4 });
  io.observe(card);
})();
</script>
"""


def assemble(main_html, out, title, comment, style="", script="", current=None):
    """bond-details3's head, navbar and footer around main_html. current: the
    navbar link (its href) to mark as the current page, in place of Bonds."""
    h = open(SRC, encoding="utf-8").read()
    page_head = h[:h.index("<main")]
    page_head = page_head.replace(
        "<!-- Generated by pages/_bond_beta.py from the beta.goldenpi.com capture; do not edit. -->",
        "<!-- Generated by %s; do not edit. -->" % comment, 1)
    if current:
        page_head = page_head.replace('<a class="nb__link is-current" href="user-corporate-bonds.html" data-current>',
                                      '<a class="nb__link" href="user-corporate-bonds.html">', 1)
        page_head = page_head.replace('<a class="nb__link" href="%s">' % current,
                                      '<a class="nb__link is-current" href="%s" data-current>' % current, 1)
    page_head = page_head.replace("</head>", STYLE + GCARD_CSS + style + "</head>", 1)
    tail = h[h.index("</main>") + len("</main>"):]
    tail = B.drop(tail, '<div id="cashflow-modal"')
    for marker in ("// Stand-in for beta's React handlers", "// bond-details3 financials"):
        k = tail.index(marker)
        tail = tail[:tail.rfind("<script>", 0, k)] + tail[tail.index("</script>", k) + len("</script>"):]
    # The bond page's title and SEO tags go; this page gets its own title.
    tail = re.sub(r'<meta (?:name|property)="(?:description|keywords|og:[^"]*|twitter:[^"]*)" content="[^"]*">', "", tail)
    tail = re.sub(r'<link rel="canonical"[^>]*>', "", tail)
    tail = re.sub(r"<title>.*?</title>", "<title>%s</title>" % title, tail, count=1, flags=re.S)
    reveal = open(REVEAL, encoding="utf-8").read()
    tail = tail.replace("</body>", "<script>%s</script>%s%s</body>" % (reveal, SCRIPT, script), 1)
    page = page_head + main_html.replace("</main>", "</main>\n" + SHEET, 1) + tail
    if "MAHAVEER" in page.upper().split("<MAIN")[1].split("</MAIN>")[0]:
        raise SystemExit("%s: bond page content leaked into main" % os.path.basename(out))
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    print("%s  %d bytes" % (os.path.relpath(out, os.path.dirname(HERE)), len(page)))


def main():
    assemble(body(), OUT, "Explore | GoldenPi",
             "pages/_explore_app.py (Figma HRSMFFccdLgqf1YwD7oyc9 40:2105, light version; "
             "navbar and footer from bond-details3.html)")


if __name__ == "__main__":
    main()
