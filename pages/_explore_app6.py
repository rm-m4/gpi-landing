#!/usr/bin/env python3
"""user-explore-app6.html: user-explore-app5.html, with each bond shelf as one
swipeable row: two cards in view and a glimpse of the third (CSS scroll-snap),
and the header card as a dark stage of three bond cards that rotate right to
left on click (the user's mock). Header lines: "Invest in Senior Secured
Bonds" (content/bond-utsav.md), "9-14% Fixed returns" (content/play-store.md).
Otherwise the same body, styles and script as pages/_explore_app5.py.

    python3 pages/_explore_app6.py
"""
import os
import re

import _explore_app as X
import _explore_app2 as A
import _explore_app5 as F

OUT = os.path.join(X.HERE, "user-explore-app6.html")
SHELF_N = 6  # bonds per swipe row

STYLE = """
/* Bond shelves: one row that swipes. 2.2 cards in view, so the third peeks
   in as the cue to swipe; each card snaps to the left edge. No script:
   touch, trackpad and Shift+wheel scroll it, and Tab brings each card in. */
.xb-bonds {
  display: flex; gap: 16px; overflow-x: auto; overscroll-behavior-x: contain;
  scroll-snap-type: x mandatory; scrollbar-width: none;
  padding: 4px 0 10px; margin: -4px 0 -10px;  /* room for the card's hover lift and shadow */
}
.xb-bonds::-webkit-scrollbar { display: none; }
.xb-bonds > .gp-ucard, .xb-bonds > :nth-child(3) { display: flex; flex: 0 0 calc((100% - 32px) / 2.2); scroll-snap-align: start; }
@media (max-width: 639px) { .xb-bonds > .gp-ucard, .xb-bonds > :nth-child(3) { flex-basis: 86%; } }
@media (prefers-reduced-motion: no-preference) { .xb-bonds { scroll-behavior: smooth; } }
"""


HERO_STYLE = """
/* Header card: a dark stage, two captured lines, three bond cards in 3D.
   Front card sage (collection-explore3), side cards gold (collection-explore4),
   tilted away and dimmed. Positions live on .xs-slot so the card keeps its own hover lift. */
.xs { position: relative; overflow: hidden; padding: 36px 40px 44px; border-radius: 20px; color: #f4e9c8;
  background: linear-gradient(180deg, #0c0a06 0%, #13100a 38%, #3a2e16 72%, #77602f 100%); }  /* ink to gold, the user's mock */
.xs__head { display: flex; flex-wrap: wrap; align-items: baseline; justify-content: space-between; gap: 8px 24px; }
.xs__head h1, .xs__head p { margin: 0; font-size: clamp(18px, 1.8vw, 22px); line-height: 1.3; font-weight: 600; color: #f4e9c8; }
.xs__gold { color: #edc967; }
.xs-stage { position: relative; height: 270px; margin-top: 32px; perspective: 1400px; outline: none; }
.xs-stage:focus-visible { outline: 2px solid #edc967; outline-offset: 8px; border-radius: 24px; }
.xs-slot { position: absolute; top: 16px; left: 50%; width: min(400px, 50%); transform-style: preserve-3d;
  transition: transform .7s cubic-bezier(.16, 1, .3, 1), opacity .5s ease, filter .5s ease; }
.xs-slot[data-pos="0"] { z-index: 3; transform: translateX(-50%) translateZ(0); }
.xs-slot[data-pos="1"] { z-index: 2; transform: translateX(calc(-50% + 50%)) rotateY(-22deg) scale(.82); opacity: .6; filter: saturate(.85); cursor: pointer; }
.xs-slot[data-pos="-1"] { z-index: 1; transform: translateX(calc(-50% - 50%)) rotateY(22deg) scale(.82); opacity: .6; filter: saturate(.85); cursor: pointer; }
.xs-slot[data-pos="1"]:hover, .xs-slot[data-pos="-1"]:hover { opacity: .8; }
.xs-slot .gp-ucard { min-height: 232px; }  /* one height, tags or not */
/* front: sage */
.xs-slot[data-pos="0"] .gp-ucard { border-color: #d5e5d9; background: linear-gradient(135deg, #dce9df 0%, #f3f7f4 38%, #fff 62%);
  box-shadow: 0 30px 60px -24px rgba(0, 0, 0, .65); }
.xs-slot[data-pos="0"] .gp-ucard__rate-value { color: #0a0a0a; }
.xs-slot[data-pos="0"] .gp-ucard__rate-value span { color: #5b4bb0; }
.xs-slot[data-pos="0"] .gp-ucard__tags span { background: #e2ece4; }
/* sides: gold */
.xs-slot:not([data-pos="0"]) .gp-ucard { border-color: #e9d9a6; background: linear-gradient(135deg, #f7efd6 0%, #fcf8ec 36%, #fff 64%); }
.xs-slot:not([data-pos="0"]) .gp-ucard__tags span { background: #f5ecd0; }
.xs-slot:not([data-pos="0"]) .gp-ucard:hover { transform: none; box-shadow: none; }
/* The Golden Experience Of Investing: the live site's stat strip (as in
   _collections.STRIP), moved under the stage; app2's copy lower down is dropped. */
.xg { margin-top: 28px; }
.xg h2 { display: flex; align-items: center; justify-content: center; gap: 16px; margin: 0 0 16px; font-size: 18px; font-weight: 600; color: var(--ink); text-align: center; }
.xg h2::before, .xg h2::after { content: ""; width: 40px; height: 1px; background: #d4af37; }
.xg ul { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); margin: 0; padding: 20px 8px; list-style: none;
  border-radius: 20px; background: #fff; border: 1px solid var(--line); }
.xg li { display: grid; justify-items: center; gap: 10px; padding: 4px 12px; text-align: center; font-size: 15px; font-weight: 500; color: var(--ink); }
.xg li + li { border-left: 1px solid var(--line); }
.xg img { width: 48px; height: 48px; object-fit: contain; }
@media (max-width: 639px) {
  .xg ul { grid-template-columns: repeat(2, minmax(0, 1fr)); row-gap: 16px; }
  .xg li:nth-child(3) { border-left: 0; }
}
/* no greeting row: the stage starts the page */
.xa.xb { grid-template-areas: "hero" "rail" "main"; }
@media (min-width: 1200px) { .xa.xb { grid-template-areas: "hero rail" "main rail"; } }
/* phones and narrow tablets: a plain swipe row */
@media (max-width: 899px) {
  .xs { padding: 24px 16px 28px; }
  .xs-stage { height: auto; display: flex; gap: 12px; margin-top: 20px; overflow-x: auto; scroll-snap-type: x mandatory; scrollbar-width: none; perspective: none; }
  .xs-stage::-webkit-scrollbar { display: none; }
  .xs-slot, .xs-slot[data-pos] { position: static; flex: 0 0 min(86%, 400px); width: auto; transform: none; opacity: 1; filter: none; cursor: auto; scroll-snap-align: center; }
}
@media (prefers-reduced-motion: reduce) { .xs-slot { transition: none; } }
"""

HERO_SCRIPT = """<script>
// Header stage: a click on the right card turns the cards right to left (the
// left card turns them back); arrow keys do the same. Side cards are hidden
// from assistive tech and the tab order. Without this the cards keep their places.
(function () {
  var stage = document.querySelector('.xs-stage');
  if (!stage) return;
  var slots = [].slice.call(stage.querySelectorAll('.xs-slot'));
  var wide = window.matchMedia('(min-width: 900px)');
  function sync() {
    slots.forEach(function (s) {
      var side = wide.matches && s.dataset.pos !== '0', a = s.querySelector('a');
      if (side) { s.setAttribute('aria-hidden', 'true'); a.tabIndex = -1; } else { s.removeAttribute('aria-hidden'); a.removeAttribute('tabindex'); }
    });
  }
  function shift(d) {
    slots.forEach(function (s) { var p = +s.dataset.pos - d; s.dataset.pos = p > 1 ? -1 : p < -1 ? 1 : p; });
    sync();
  }
  slots.forEach(function (s) {
    s.addEventListener('click', function (e) {
      var p = +s.dataset.pos;
      if (p && wide.matches) { e.preventDefault(); shift(p); }
    });
  });
  stage.addEventListener('keydown', function (e) {
    if (!wide.matches) return;
    if (e.key === 'ArrowRight') { e.preventDefault(); shift(1); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); shift(-1); }
  });
  wide.addEventListener('change', sync);
  sync();
})();
</script>
"""

# The header deals (app2's DEALS: Akara, NeoGrowth, Best Capital at 13.00%), as
# collection-explore cards: left, front, right.
HERO_BONDS = [("NEOGROWTH", -1), ("AKARA", 0), ("BEST CAPITAL", 1)]


def hero():
    found = {}
    for c in A.C.DATA["tabs"]["all-bonds"]["cards"]:
        if c["issuer"] in dict(HERO_BONDS) and c["rate"].startswith("13.00") and c["issuer"] not in found:
            found[c["issuer"]] = c
    if len(found) != len(HERO_BONDS):
        raise SystemExit("header deals not in collections.tabs.json any more: %s" % sorted(found))
    slots = "".join('<div class="xs-slot" data-pos="%d">%s</div>' % (pos, F.bond(found[name], 0))
                    for name, pos in HERO_BONDS)
    return ('<section class="xa-hero xs" aria-labelledby="xs-t">'
            '<!-- DATA: the three top deals, collections.tabs.json snapshot. -->'
            '<div class="xs__head"><h1 id="xs-t">Invest in <span class="xs__gold">Senior Secured Bonds</span></h1>'
            '<p><span class="xs__gold">9-14%%</span> Fixed returns</p></div>'
            '<div class="xs-stage" tabindex="0" role="region" aria-roledescription="carousel" '
            'aria-label="Top deals. Use the left and right arrow keys to turn the cards.">%s</div></section>' % slots
            + golden())


# The live site's strip (_collections.STRIP; content/*.md: "18 lacs+ Users", "Zero Defaults").
GOLDEN = [("users.png", "18 lacs+ Users"), ("5percent.png", "Curated Bonds"),
          ("shield.png", "Sebi Registered"), ("trophy.png", "Zero Defaults")]


def golden():
    for _, t in GOLDEN:
        if t not in A.C.STRIP:
            raise SystemExit("not in the site's stat strip any more: %r" % t)
    return ('<section class="xg" data-reveal aria-labelledby="xg-t"><h2 id="xg-t">The Golden Experience Of Investing</h2><ul>%s</ul></section>'
            % "".join('<li><img src="../assets/img/%s" alt="" width="48" height="48" loading="lazy">%s</li>' % g for g in GOLDEN))


ORDERS_STYLE = """
/* Pending orders: one card per order. Issuer logo; name, then units and amount
   (one style, one line), then the status; the action on the right. */
.xo-list { display: grid; gap: 10px; margin: 0; padding: 0; list-style: none; }
.xo { display: grid; grid-template-columns: 40px minmax(0, 1fr) auto; column-gap: 12px; align-items: center;
  padding: 16px; border-radius: 16px; background: #fff; border: 1px solid var(--line); }
.xo__logo { align-self: start; }
.xo__logo { width: 40px; height: 40px; border-radius: 12px; object-fit: contain; background: #fff; border: 1px solid var(--line); padding: 3px; }
.xo__name { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 15px; line-height: 1.35; font-weight: 600; color: var(--ink); }
.xo__meta { margin-top: 2px; font-size: 13px; line-height: 1.4; color: var(--sub); white-space: nowrap; }
.xo__meta b { font-weight: 500; color: #4a4336; font-variant-numeric: tabular-nums; }  /* a step under the name */
.xo__status { display: inline-block; margin-top: 8px; padding: 3px 10px; border-radius: 999px; font-size: 12px; font-weight: 600; line-height: 1.4; }
.xo__status--warn { color: #8f4a00; background: #fdeed8; }
.xo__status--info { color: #5c5240; background: #f1eee6; }
.xo__btn { flex: none; height: 34px; padding: 0 16px; border-radius: 999px; font: inherit; font-size: 13px; font-weight: 700; cursor: pointer;
  transition: background-color .2s ease, transform .2s ease; }
.xo__btn--primary { color: #fff; background: #14110c; border: 1px solid #14110c; }
.xo__btn--primary:hover { background: #2b2418; }
.xo__btn--ghost { color: var(--ink); background: none; border: 1px solid var(--line); }
.xo__btn--ghost:hover { border-color: #14110c; }
.xo__btn:active { transform: scale(.97); }
.xo__btn:focus-visible { outline: 2px solid #d4af37; outline-offset: 2px; }
@media (prefers-reduced-motion: reduce) { .xo__btn { transition: none; } .xo__btn:active { transform: none; } }
"""

# Pending bond orders (DATA): app2's sample Muthoot order, then the two pending
# bond orders of the Figma persona (content/profile.md, /profile/orders: "Pending",
# each followed by "Select your payment method. Continue", so payment is what's pending).
ORDER_ROWS = [("GPID100936.MUTHOOT-FINCORP-LIMITED_1-2x.png", "Muthoot Fincorp bond", "10 units", "&#8377;1,00,520",
               "Payment pending", "warn", "Pay now", "primary"),
              ("GPID104095.Neogrowth-new-logo-1-.jpg", "NeoGrowth bond", "3 units", "&#8377;3,05,825.40",
               "Payment pending", "warn", "Pay now", "primary"),
              ("GPID107347.Best-Capital.png", "Best Capital bond", "3 units", "&#8377;29,865.85",
               "Payment pending", "warn", "Pay now", "primary")]


def orders():
    return '<ul class="xo-list">%s</ul>' % "".join(
        '<li class="xo"><img class="xo__logo" src="../assets/img/%s" alt="" width="40" height="40">'
        '<div><p class="xo__name">%s</p><p class="xo__meta"><b>%s</b> &middot; <b>%s</b></p>'
        '<span class="xo__status xo__status--%s">%s</span></div>'
        '<button type="button" class="xo__btn xo__btn--%s">%s<span class="sr-only"> for %s</span></button></li>'
        % (logo, name, meta, amt, tone, status, kind, cta, name) for logo, name, meta, amt, status, tone, cta, kind in ORDER_ROWS)


def body():
    for f in ("Invest in Senior Secured Bonds", ):
        A.need(A.content("bond-utsav"), f)
    A.need(A.content("play-store"), "9-14% Fixed returns")
    b, n = re.subn(r'<section class="xa-hero xb-hero".*?</section>', lambda m: hero(), F.body(SHELF_N), count=1, flags=re.S)
    if n != 1:
        raise SystemExit("app2's header card not found")
    b, n = re.subn(r'<ul class="xb-box xb-list">.*?</ul>', lambda m: orders(), b, count=1, flags=re.S)
    if n != 1:
        raise SystemExit("app2's pending orders not found")
    b, n = re.subn(r'<span class="xb-count">\d+</span>', '<span class="xb-count">%d</span>' % len(ORDER_ROWS), b, count=1)
    if n != 1:
        raise SystemExit("app2's order count not found")
    b, n = re.subn(r'<div class="xb-why__exp">.*?</ul></div>', "", b, count=1, flags=re.S)
    if n != 1:
        raise SystemExit("app2's Golden Experience strip not found")
    # No greeting: the stage opens the page and its first line is the h1.
    b, n = re.subn(r'<div class="xb-head">.*?</div></div>', "", b, count=1, flags=re.S)
    if n != 1:
        raise SystemExit("app2's greeting not found")
    return b


def main():
    X.assemble(body(), OUT, "Explore | GoldenPi",
               "pages/_explore_app6.py (user-explore-app5.html with a rotating header stage and swipeable bond shelves)",
               style=A.STYLE + "<style>\n" + F.ucard_css() + F.refer_css() + F.STYLE + F.REFER_STYLE + F.HELP_STYLE + STYLE + HERO_STYLE + ORDERS_STYLE + "</style>\n", script=A.SCRIPT + HERO_SCRIPT)


if __name__ == "__main__":
    main()
