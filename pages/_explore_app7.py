#!/usr/bin/env python3
"""user-explore-app7.html: the Collection page from the user's Figma
(HRSMFFccdLgqf1YwD7oyc9, node 130:224), built on user-explore-app6's parts.

Left: app6's rotating deal stage, The Golden Experience strip, Why invest in
bonds, High Return (sage), Choose Your Category, High Rated (gold), Short Term
(slate), and the scan-to-download card. Right: portfolio.html's card carousel
and app6's pending orders. Header: the finalised navbar, not Figma's.

Copy: the Figma frame is the source for strings the live capture does not have
(the strip's figures, the three reasons, "Choose Your Category", the scan
card); everything else is captured. Bonds are collections.tabs.json; the
design's struck-out old rates have no data, so they are left out.

    python3 pages/_explore_app7.py
"""
import os
import re

import _explore_app as X
import _explore_app2 as A
import _explore_app5 as F
import _explore_app6 as G
import _portfolio as P

OUT = os.path.join(X.HERE, "user-explore-app7.html")
ROOT = os.path.dirname(X.HERE)
I7 = "../assets/img/explore-app7/"
IMG = "../assets/img/"


# ------------------------------------------------------------- golden strip
# Figma 130:496, three of its four stats (the user dropped "Invested"), on one line
# at every width. Figures from the design, not the live capture (DATA).
GOLDEN = [(IMG + "bd5/proof-people.png", 51, 45, "20 Lacs+ Users"),
          (I7 + "stat-trophy.png", 37, 37, "Top 5% Bonds"),
          (I7 + "stat-zero.png", 46, 46, "Zero Defaults")]


def golden():
    return ('<!-- DATA: figures from the Figma design (130:496), not the live capture. -->'
            '<section class="x7g" data-reveal aria-labelledby="x7g-t"><h2 id="x7g-t">The Golden Experience Of Investing</h2><ul>%s</ul></section>'
            % "".join('<li><img src="%s" alt="" width="%d" height="%d" loading="lazy">%s</li>' % g for g in GOLDEN))


# ---------------------------------------------------------------- why bonds
# Figma 130:539: three tinted tiles. Copy from the design.
WHY = [("shield", IMG + "bd5/tile-shield.png", "Bonds are Senior Secured",
        "For every &#8377;1 you invest, there is at least &#8377;1+ security available which protects the investors"),
       ("clock", IMG + "bd5/tile-clock.png", "Bonds offer fixed returns",
        "You can earn fixed returns of <b>9% - 13.5% P.A.</b> on Senior Secured bonds available on GoldenPi")]
# The design's third tile, "Bonds have zero lock-ins" (sell anytime), is left
# out for now at the user's request.


def why():
    tiles = "".join('<li class="x7w__tile x7w__tile--%s"><span class="x7w__art"><img src="%s" alt="" loading="lazy"></span>'
                    '<h3>%s</h3><p>%s</p></li>' % w for w in WHY)
    return ('<section class="x7w" data-reveal aria-labelledby="x7w-t"><h2 id="x7w-t">Why invest in bonds on GoldenPi?</h2>'
            '<ul class="x7w__tiles">%s</ul></section>' % tiles)


# ------------------------------------------------------------------ shelves
SHELVES = [("high-returns", "High Return", "sage"), ("highly-rated", "High Rated", "gold"), ("short-term", "Short Term", "slate")]
SHELF_N = 6


def shelf(slug, title, tone):
    cards = "".join(F.bond(c, i) for i, c in enumerate(A.C.DATA["tabs"][slug]["cards"][:SHELF_N]))
    sid = "x7s-" + slug
    return ('<!-- DATA: first %d bonds of /collections/%s, collections.tabs.json snapshot. -->\n'
            '<section class="x7s x7s--%s" data-reveal aria-labelledby="%s"><h2 id="%s">%s</h2>'
            '<div class="x7s__row">%s</div></section>' % (SHELF_N, slug, tone, sid, sid, title, cards))


# ---------------------------------------------------------------- live IPO
def ipo():
    """app2's live NCD IPO card (SMC, content/beta_bond-ipo_GPID104212_smc.md), in
    purple, its status as two pills (the user's call)."""
    html = A.ipo()
    for old, new in [('<section class="xb-ipos" data-reveal', '<section class="xb-ipos x7i" data-reveal'),
                     ('<p class="xb-ipo__live"><i aria-hidden="true"></i>NCD IPO live &middot; Closes on 9-Oct-2026</p>',
                      '<p class="x7i__pills"><span class="x7i__pill x7i__pill--live"><i aria-hidden="true"></i>NCD IPO live</span>'
                      '<span class="x7i__pill">Closes on 9-Oct-2026</span></p>'),
                     ('<p class="xa-head__sub">Apply to new bond issues before they close.</p>', ''),
                     # the bond cards' rate style: value in ink, the % in purple
                     ('<dd>Up to 10%</dd>', '<dd>Up to 10<span>%</span></dd>')]:
        if html.count(old) != 1:
            raise SystemExit("app2's IPO card changed, re-check: %r" % old)
        html = html.replace(old, new)
    # no "View all" (the user's call; the other shelves have none either)
    html, n = re.subn(r'<div class="xa-head__end">.*?</a></div>', '', html, count=1, flags=re.S)
    if n != 1:
        raise SystemExit("app2's IPO heading changed, re-check")
    return html


# ----------------------------------------------------------------- category
# Figma 130:590: the collections as pills, each linking to its collection page.
CATS = [("explore-app7/cat-high-returns.png", 30, "High Returns", "collections-high-returns.html"),
        ("high-rated-collection.png", 24, "High Rated", "collections-highly-rated.html"),
        ("short-term.png", 30, "Short Term", "collections-short-term.html"),
        ("explore-app7/cat-gold-backed.png", 22, "Gold Backed", "collections-gold-backed.html"),
        ("bd5/proof-money.png", 30, "Starts &#8377;10k", "collections-starts-10k.html"),
        ("Goverment.png", 30, "Govt Bonds", "collections-government-bonds.html"),
        ("explore-app7/cat-monthly.png", 30, "Monthly Payout", "collections-monthly-payout.html"),
        ("explore-app7/cat-ncd-ipo.png", 22, "NCD IPO", "collections-ncd-ipo.html")]


def categories():
    for _, _, _, href in CATS:
        if not os.path.exists(os.path.join(X.HERE, href)):
            raise SystemExit("no such collection page: " + href)
    pills = "".join('<li><a class="x7c__pill" href="%s"><img src="%s%s" alt="" width="%d" height="%d">%s</a></li>'
                    % (href, IMG, f, s, s, t) for f, s, t, href in CATS)
    arrow = '<button type="button" class="x7c__arrow%s" data-x7c="%d" aria-label="%s"><img src="%sprofile/back.svg" alt="" width="20" height="20"></button>'
    return ('<section class="x7c" data-reveal aria-labelledby="x7c-t"><div class="x7c__head"><h2 id="x7c-t">Choose Your Category</h2>'
            '<div class="x7c__arrows">%s%s</div></div><ul class="x7c__row">%s</ul></section>'
            % (arrow % ("", -1, "Scroll categories left", IMG), arrow % (" x7c__arrow--next", 1, "Scroll categories right", IMG), pills))


# ----------------------------------------------------------------- app card
def app_card():
    # Figma 130:1738. Only Google Play's URL is in the capture (A.PLAY); the
    # App Store half of the badge artwork is not a link until its URL is known.
    return ('<section class="x7a" data-reveal aria-labelledby="x7a-t"><div class="x7a__copy">'
            '<h2 id="x7a-t"><img src="%ssmartphone.svg" alt="" width="17" height="24">Scan with your phone camera</h2>'
            '<p>Works on iPhone &amp; Android</p>'
            '<div class="x7a__stores"><img src="%sstore-badges.png" alt="Download on the App Store, Get it on Google Play" width="377" height="396">'
            '<a class="x7a__play" href="%s" target="_blank" rel="noopener"><span class="sr-only">Get it on Google Play</span></a></div></div>'
            '<span class="x7a__qr"><img src="%sapp-qr.svg" alt="QR code to download the GoldenPi app" width="104" height="104" loading="lazy"></span>'
            '</section>' % (I7, I7, A.PLAY, I7))


# --------------------------------------------------------------------- rail
def rail():
    # Figma 130:2235: the first card is black and reads "Current Value".
    cards = P.cards().replace('<span class="pf-gcard__what">Outstanding</span>', '<span class="pf-gcard__what">Current value</span>', 1)
    # app6's pending orders (DATA), under the cards as on app6.
    orders = ('<!-- DATA: pending orders, sample copy. -->'
              '<section class="xb-orders" data-reveal aria-labelledby="xb-orders-t">'
              '<h2 class="xa-rail__label" id="xb-orders-t">Pending orders <span class="xb-count">%d</span></h2>%s</section>'
              % (len(G.ORDER_ROWS), G.orders()))
    return '<aside class="xb-rail x7r" aria-label="Your account">%s%s</aside>' % (cards, orders)


def body():
    G.golden = golden  # app6's hero() appends golden(); use the Figma strip
    return ('<main id="main-content" class="xa-page"><div class="xa xb x7"><div class="xa-hero-wrap">%s</div>%s'
            '<div class="xa-main">%s</div></div></main>'
            % (G.hero(), rail(), "".join([why()] + [shelf(*SHELVES[0]), ipo(), categories()] + [shelf(*s) for s in SHELVES[1:]] + [app_card()])))


def header(page):
    """The finalised logged-in navbar (as on portfolio.html: _navbar's plain dark
    header with icons, from _user.shell and _build.py), not Figma's; no item is
    current on this page."""
    with open(os.path.join(X.HERE, "portfolio.html"), encoding="utf-8") as f:
        final = re.search(r'<div class="gp-shell nb__inner">.*?</div>\s*(?=</header>)', f.read(), re.S).group(0)
    final = final.replace(' aria-current="page"', "")
    # The phone bottom bar's Portfolio tab (nb__link--m, phone-only) is dropped here.
    final, d = re.subn(r'<a class="nb__link nb__link--m[^"]*"[^>]*>.*?</a>\s*', "", final, count=1, flags=re.S)
    if d != 1:
        raise SystemExit("the navbar's phone Portfolio tab is gone, re-check")
    page, n = re.subn(r'<div class="gp-shell nb__inner">.*?</div>\s*(?=</div></header>)', lambda m: final, page, count=1, flags=re.S)
    page, k = re.subn(r'<div class="nb nb--dark nb--plain" ', '<div class="nb nb--dark nb--plain nb--micons" ', page, count=1)
    if n != 1 or k != 1:
        raise SystemExit("the shell's navbar changed, re-check")
    return page


def css(names):
    return P_CSS(lambda sel: all(x.strip().startswith(names) for x in sel.split(",")))


def P_CSS(keep):
    return X.B.css_rules(open(os.path.join(ROOT, "assets", "portfolio.css"), encoding="utf-8").read(), keep)


def carousel_js():
    """portfolio.html's carousel and card sheen, cut from _portfolio.js (its
    sheets are already handled by this shell's script)."""
    js = open(os.path.join(X.HERE, "_portfolio.js"), encoding="utf-8").read()
    a = js.index("  // ------------------------------------------------------------ carousels")
    b = js.index("  // ---------------------------------------------------------------- sheets")
    return ("<script>\n(function () {\n  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;\n%s})();\n</script>\n"
            % js[a:b])


STYLE = """
/* user-explore-app7: Figma 130:224. */
/* the final navbar is a bottom tab bar under 1000px; navbar.css makes room for
   it via .nb-slot, which this shell lacks, so do the same here */
@media (max-width: 999px) { body:has(.nb--micons) { padding-bottom: calc(62px + env(safe-area-inset-bottom, 0px)); } }

/* layout: Figma's 790 / 360 split, 30 apart */
@media (min-width: 1200px) { .xa.xb.x7 { grid-template-columns: minmax(0, 79fr) minmax(0, 36fr); column-gap: 30px; } }
.x7 .xa-main { gap: 40px; }

/* the Golden Experience strip (130:496) */
.x7g { margin-top: 40px; }
.x7g h2 { display: flex; align-items: center; justify-content: center; gap: 8px; margin: 0 0 12px; font-size: 14px; line-height: 12px; font-weight: 700; color: #322811; }
.x7g h2::before, .x7g h2::after { content: ""; width: 24px; height: 1px; opacity: .7; background: linear-gradient(170deg, #fdf2d0 0%, #e6b325 50%, #b38600 100%); }
.x7g ul { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); align-items: end; margin: 0; padding: 14px 16px 18px; list-style: none;
  border-radius: 22px; background: #fff; border-bottom: 1px solid #fdf3d4; box-shadow: 0 2px 1px rgba(0, 0, 0, .02); }
.x7g li { display: grid; justify-items: center; gap: 16px; text-align: center; font-size: 14px; font-weight: 500; color: #322811; }
.x7g li + li { border-left: 1px solid rgba(231, 227, 217, .6); }
.x7g img { object-fit: contain; }
@media (max-width: 639px) { .x7g ul { padding: 14px 4px 16px; } .x7g li { gap: 12px; padding-inline: 4px; font-size: 13px; } }

/* Why invest in bonds (130:539) */
.x7w { display: grid; gap: 20px; padding: 20px; border-radius: 24px; background: #fff; overflow: hidden; }
.x7w h2 { margin: 0; font-size: 14px; line-height: 1.5; font-weight: 600; letter-spacing: .7px; text-transform: uppercase; color: #a67c00; }
.x7w__tiles { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; margin: 0; padding: 0; list-style: none; }
.x7w__tile { display: grid; align-content: start; gap: 12px; min-height: 236px; padding: 20px; border-radius: 20px; overflow: hidden; border-bottom: 1px solid #e1f2e8; }
.x7w__tile--shield { background: #e8f7ee; }
.x7w__tile--clock { background: #fff1e8; }
.x7w__tile--lock { background: rgba(245, 243, 255, .7); gap: 10px; }
.x7w__art { display: block; height: 75px; }
.x7w__art img { display: block; height: 75px; width: auto; max-width: none; }
.x7w__tile--shield .x7w__art { width: 71px; overflow: hidden; }
.x7w__tile--shield .x7w__art img { margin-left: -22.6px; }
.x7w__tile--clock .x7w__art img { margin-left: -15.7px; }
.x7w__tile--lock .x7w__art img { margin-left: 6px; }
.x7w h3 { margin: 0; font-size: 16px; line-height: 19.5px; font-weight: 600; color: #7a571f; }
.x7w p { margin: 0; font-size: 14px; line-height: 21px; color: #252525; }
.x7w p b { font-weight: 500; }
@media (max-width: 767px) { .x7w__tiles { grid-template-columns: minmax(0, 1fr); } .x7w__tile { min-height: 0; } }

/* shelves (130:589, 130:881, 130:1259): one swipe row, 355px cards, a glimpse of the third */
.x7s { display: grid; gap: 20px; }

/* live NCD IPO: app2's card with a light purple wash (the % accent on the FD cards), status as pills, black CTA */
.x7 .x7i .xa-head h2 { font-size: 18px; line-height: 28px; font-weight: 600; color: #322811; }
.x7 .x7i .xb-ipo { padding: 24px; gap: 20px; border-radius: 23.4px; border: 1px solid #e9e3f2; box-shadow: none;
  background: linear-gradient(135deg, #f4f0fa 0%, #faf8fc 40%, #fff 72%); }
.x7 .x7i .xb-ipo__id img { border-color: #e9e3f2; }
.x7 .x7i .xb-ipo h3 { margin-top: 8px; font-size: 18px; font-weight: 600; color: #322811; }
.x7i__pills { display: flex; flex-wrap: wrap; gap: 6px; margin: 0; }
.x7i__pill { display: inline-flex; align-items: center; gap: 6px; height: 24px; padding: 0 10px; border-radius: 999px;
  font-size: 12px; font-weight: 600; color: #5c4a7a; background: #fff; border: 1px solid #e9e3f2; white-space: nowrap; }
.x7i__pill--live { color: #047a31; background: #e8f6ee; border-color: #cfeedc; }  /* 4.9:1 on its fill */
.x7i__pill--live i { width: 6px; height: 6px; border-radius: 50%; background: #06963c; }
@media (prefers-reduced-motion: no-preference) { .x7i__pill--live i { animation: xb-live 2s ease-in-out infinite; } }
.x7 .x7i .xb-ipo__facts { border-top-color: #e9e3f2; }
.x7 .x7i .xb-ipo__facts dt { font-size: 13px; color: var(--sub); }
.x7 .x7i .xb-ipo__facts dd { font-size: 16px; font-weight: 600; color: #322811; }
.x7 .x7i .xb-ipo__facts dd span { color: #472d75; }
.x7 .x7i .xb-ipo__cta { background: #14110c; color: #fff; }
.x7 .x7i .xb-ipo__cta:hover { background: #2a2419; }
.x7 .x7i .xb-ipo__cta:focus-visible { outline: 2px solid #14110c; outline-offset: 2px; }
@media (max-width: 639px) {
  .x7 .x7i .xb-ipo { padding: 18px 16px; }
  .x7 .x7i .xb-ipo__id { align-items: flex-start; }
  .x7i__pill { height: 22px; padding: 0 8px; font-size: 11px; }
  .x7 .x7i .xb-ipo h3 { font-size: 16px; }
}
.x7s h2, .x7c h2 { margin: 0; font-size: 18px; line-height: 28px; font-weight: 600; color: #322811; }
.x7s__row { display: flex; gap: 20px; overflow-x: auto; overscroll-behavior-x: contain; scroll-snap-type: x mandatory; scrollbar-width: none;
  padding: 4px 0 10px; margin: -4px 0 -10px; }
.x7s__row::-webkit-scrollbar { display: none; }
.x7s .gp-ucard { flex: 0 0 min(355px, 86%); min-height: 208px; scroll-snap-align: start; border-radius: 23.4px; border-width: 1.17px; }
.x7s .gp-ucard__body { padding: 25px 23px 22px; row-gap: 22px; column-gap: 16px; }
.x7s .gp-ucard__id { gap: 17px; }
.x7s .gp-ucard__logo { width: 40px; height: 40px; border-radius: 12px; }
.x7s .gp-ucard__issuer { font-size: 16px; font-weight: 600; }
.x7s .gp-ucard__sold { font-size: 12px; font-weight: 600; }
.x7s .gp-ucard__rate-value { color: #0a0a0a; font-size: 35px; line-height: 41px; letter-spacing: -1.17px; }
.x7s .gp-ucard__rate-value span { color: #472d75; font-size: 14px; }
.x7s .gp-ucard__tags { gap: 8px; }
.x7s .gp-ucard__tags span { padding: 4px 8px; border-radius: 20px; font-size: 12px; color: #0a0a0a; }
.x7s .gp-ucard__metrics dt { font-size: 12px; }
.x7s .gp-ucard__metrics dd { font-size: 14.7px; font-weight: 600; }
.x7s--sage .gp-ucard { border-color: #d8e9db; background: linear-gradient(-46.6deg, #fff 49.8%, #d8e9db 99.5%); }
.x7s--sage .gp-ucard__tags span { background: #e6f1e8; }
.x7s--gold .gp-ucard { border-color: #f2ecc3; background: linear-gradient(-46.6deg, #fff 49.8%, #efeabd 99.5%); }
.x7s--gold .gp-ucard__tags span { background: #f7f6eb; }
.x7s--slate .gp-ucard { border-color: #c2daf0; background: linear-gradient(-45.6deg, #fff 41.2%, #c7def2 99.5%); }
.x7s--slate .gp-ucard__tags span { background: #e9f4ff; }

/* Choose Your Category (130:590) */
.x7c { display: grid; gap: 16px; }
.x7c__head { display: flex; align-items: center; justify-content: space-between; gap: 16px; }
.x7c__arrows { display: flex; gap: 10px; }
.x7c__arrow { display: grid; place-items: center; width: 32px; height: 32px; padding: 0; border: 0; border-bottom: 1px solid #fdf3d4; border-radius: 999px;
  background: none; cursor: pointer; }
.x7c__arrow--next img { transform: scaleX(-1); }
.x7c__arrow:hover { background: #fff; }
.x7c__arrow:focus-visible { outline: 2px solid #d4af37; outline-offset: 2px; }
.x7c__row { display: flex; gap: 14px; margin: 0; padding: 0 0 4px; list-style: none; overflow-x: auto; scroll-behavior: smooth; scrollbar-width: none; }
.x7c__row::-webkit-scrollbar { display: none; }
.x7c__row > li { flex: none; }
.x7c__pill { display: flex; align-items: center; gap: 4px; height: 50px; padding: 10px 16px; border-radius: 20px; white-space: nowrap;
  background: #fff; border-bottom: 1px solid #fdf3d4; box-shadow: 0 2px 1px rgba(0, 0, 0, .02);
  font-size: 12px; line-height: 16px; font-weight: 700; color: #322811; text-decoration: none; transition: background-color .2s ease, color .2s ease; }
.x7c__pill img { object-fit: contain; }
.x7c li:first-child .x7c__pill, .x7c__pill:hover { background: #0e0a00; color: #fff; border-color: #0e0a00; }
.x7c__pill:focus-visible { outline: 2px solid #d4af37; outline-offset: 2px; }
@media (prefers-reduced-motion: reduce) { .x7c__row { scroll-behavior: auto; } .x7c__pill { transition: none; } }

/* scan to download (130:1738) */
.x7a { position: relative; display: flex; align-items: center; justify-content: space-between; gap: 24px; padding: 26px 28px; border-radius: 20px;
  background: #fff; border: 1px solid rgba(231, 227, 217, .47); box-shadow: 0 2px 1px rgba(0, 0, 0, .02); overflow: hidden; }
.x7a__copy { display: grid; gap: 10px; min-width: 0; }
.x7a h2 { display: flex; align-items: center; gap: 9px; margin: 0; font-size: 20.5px; line-height: 1.25; font-weight: 600; color: #191814; }
.x7a p { margin: 0; font-size: 14px; line-height: 1.5; color: #252525; }
.x7a__stores { position: relative; width: 274px; height: 46px; margin-top: 12px; overflow: hidden; }
.x7a__stores img { position: absolute; left: -38px; top: -306.4px; width: 376.7px; height: 396.3px; max-width: none; }
.x7a__play { position: absolute; top: 0; right: 0; width: 49%; height: 100%; border-radius: 10px; }
.x7a__play:focus-visible { outline: 2px solid #d4af37; outline-offset: 2px; }
.x7a__qr { flex: none; display: grid; place-items: center; width: 130px; height: 130px; border-radius: 18px; background: #fff;
  box-shadow: inset 0 0 0 2px #d4af37; }
.x7a__qr img { width: 104px; height: 104px; }
@media (max-width: 639px) { .x7a { padding: 20px 16px; } .x7a__qr { display: none; } }

/* phones: the desktop's 3D stage, not a swipe row. The three cards share one
   grid cell, so the stage is as tall as the tallest card; the sides tilt away
   and peek out behind the front one (.xs clips them). Tap a side card or swipe
   to turn. Narrow cards give the issuer room (smaller rate; a long one-word
   name breaks rather than run into the rate) */
@media (max-width: 899px) {
  .x7 .xs { overflow: clip; }  /* hidden still lets a tap scroll it sideways */
  .x7 .xs-stage { display: grid; grid-template-columns: minmax(0, 1fr); overflow: visible; perspective: 1000px; padding: 4px 0 8px; touch-action: pan-y; scroll-snap-type: none; }
  .x7 .xs-slot, .x7 .xs-slot[data-pos] { grid-area: 1 / 1; position: relative; left: auto; top: auto; justify-self: center; display: flex;
    width: min(86%, 400px); transform-style: preserve-3d;
    transition: transform .7s cubic-bezier(.16, 1, .3, 1), opacity .5s ease, filter .5s ease; }
  .x7 .xs-slot[data-pos="0"] { z-index: 3; transform: none; opacity: 1; filter: none; }
  .x7 .xs-slot[data-pos="1"] { z-index: 2; transform: translateX(40%) rotateY(-24deg) scale(.84); opacity: .6; filter: saturate(.85); cursor: pointer; }
  .x7 .xs-slot[data-pos="-1"] { z-index: 1; transform: translateX(-40%) rotateY(24deg) scale(.84); opacity: .6; filter: saturate(.85); cursor: pointer; }
  .x7 .xs-slot .gp-ucard { flex: 1; min-height: 0; }
}
@media (max-width: 899px) and (prefers-reduced-motion: reduce) { .x7 .xs-slot { transition: none; } }
@media (max-width: 639px) {
  /* phones: the deal stage runs edge to edge, flush under the navbar (cancels
     .xa's 16px gutter and 16px top padding), and the portfolio cards go */
  .x7 .xa-hero-wrap { margin: -16px -16px 0; }
  .x7 .xs { border-radius: 0; }
  .x7 .x7g { margin-inline: 16px; }  /* only the stage bleeds; the strip keeps the gutter */
  .x7r .pf-cards { display: none; }
  .x7 .x7w { margin-inline: -16px; border-radius: 0; padding-inline: 16px; }  /* Why invest: edge to edge too */
  .x7 .gp-ucard__issuer { overflow-wrap: anywhere; }  /* phones only: desktop cards have room */
  .x7 .xs { padding-inline: 12px; }
  .x7 .xs .xs__head { padding-inline: 4px; }
  .x7 .gp-ucard__body { padding: 20px 18px; column-gap: 10px; row-gap: 18px; }
  .x7 .gp-ucard__id { gap: 10px; }
  .x7 .gp-ucard__rate-value { font-size: 28px; line-height: 30px; letter-spacing: -.8px; }
  .x7 .gp-ucard__rate-value span { font-size: 13px; }
}
/* rail: portfolio.html's card carousel and explainer notes */
.x7r { display: grid; gap: 16px; align-content: start; }
/* every card black and white (Figma's first card, applied to all three) */
.x7r .pf-gcard { color: rgba(255, 255, 255, .85); background: linear-gradient(116deg, #000 35.9%, #313131 96.4%); }
.x7r .pf-gcard__bg { display: none; }
.x7r .pf-gcard__stats dd { color: rgba(255, 255, 255, .85); }
/* the logo stays exactly as on the gold card; only the info icons turn white */
.x7r .pf-gcard__band .pf-info img, .x7r .pf-gcard__stats img { filter: brightness(0) invert(1); }
.x7r .pf-gcard__band { background: rgba(255, 255, 255, .06); }
/* the dots stay 8px but take a 24px-tall tap area; not wider, as they sit
   2px apart and wider areas would overlap (the design's tight cluster) */
.x7r .pf-dots button { position: relative; }
.x7r .pf-dots button::after { content: ""; position: absolute; inset: -8px 0; }
"""

# app6's stage script, on at every width (app6 turns it off below 900px for
# its swipe row), plus a swipe that turns the cards like the arrow keys.
HERO_JS = G.HERO_SCRIPT.replace("'(min-width: 900px)'", "'all'") + """<script>
(function () {
  var stage = document.querySelector('.xs-stage'), x0 = null;
  if (!stage) return;
  stage.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  stage.addEventListener('touchend', function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0; x0 = null;
    if (Math.abs(dx) > 40) stage.dispatchEvent(new KeyboardEvent('keydown', { key: dx < 0 ? 'ArrowRight' : 'ArrowLeft' }));
  }, { passive: true });
})();
</script>
"""

ARROWS_JS = """<script>
// Choose Your Category: the arrows scroll the pill row by most of its width.
(function () {
  var row = document.querySelector('.x7c__row');
  if (!row) return;
  document.querySelectorAll('[data-x7c]').forEach(function (b) {
    b.addEventListener('click', function () { row.scrollBy({ left: +b.dataset.x7c * row.clientWidth * 0.8 }); });
  });
})();
</script>
"""


def main():
    rail_css = css((".pf-cards", ".pf-track", ".pf-dots"))
    lifetime = P.SHEETS[P.SHEETS.index('<dialog class="pf-sheet" id="sheet-lifetime"'):]
    X.assemble(body().replace("</main>", "</main>\n" + lifetime, 1), OUT, "Collections | GoldenPi",
               "pages/_explore_app7.py (the Collection page from Figma 130:224, on user-explore-app6's parts)",
               style=A.STYLE + "<style>\n" + F.ucard_css() + G.HERO_STYLE + G.ORDERS_STYLE + rail_css + STYLE + "</style>\n",
               script=A.SCRIPT + HERO_JS + carousel_js() + ARROWS_JS)
    with open(OUT, encoding="utf-8") as f:
        page = header(f.read())
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page)


if __name__ == "__main__":
    main()
