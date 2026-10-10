#!/usr/bin/env python3
"""user-explore-app5.html: user-explore-app2.html with a colour per card block,
from the collection-explore4 variants:

  High yield bonds    brand gold, soft wash  (returns, GoldenPi's own colour)
  Live NCD IPOs       slate blue, cool       (a new issue, set apart from the shelves)
  Highly rated bonds  sage, light            (safety, calm)

Bond shelves use collection-explore's card (gp-ucard, no note strip); Refer &
Earn is refer-and-earn.html's header card. The rest is app2's, unchanged.

    python3 pages/_explore_app5.py
"""
import os
import re

import _explore_app as X
import _explore_app2 as A

OUT = os.path.join(X.HERE, "user-explore-app5.html")


def ucard_css():
    """collection-explore's card rules, copied out of assets/final.css (this
    shell does not load it), so the two pages cannot drift apart."""
    css = open(os.path.join(os.path.dirname(X.HERE), "assets", "final.css"), encoding="utf-8").read()
    a = css.index("/* Bond Utsav card (bond-utsav.html)")
    b = css.index("/* Bond Utsav iteration 2")
    c = css.index(".gp-ucard__initial {")
    return css[a:b] + css[c:css.index("}", c) + 1] + "\n"


STYLE = """
/* user-explore-app5: shelves use collection-explore's card (no note strip);
   one colour per card block, from collection-explore4's gold, slate and sage. */
.xb-bonds { --gp-gradient-bond-card: #f7efd6; }
@media (min-width: 640px) {
  .xb-bonds { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }
  .xb-bonds > :nth-child(3) { display: flex; }  /* app2 hides the third card at tablet width */
}

/* High yield: brand gold, soft wash */
.cv-gold .gp-ucard { border-color: #e9d9a6; background: linear-gradient(135deg, #f7efd6 0%, #fcf8ec 36%, #fff 64%); }
.cv-gold .gp-ucard__tags span { background: #f5ecd0; }
.cv-gold .gp-ucard:hover { border-color: #d4af37; }

/* Live NCD IPO: slate blue, cool */
.cv-slate .xb-ipo { border-color: #c9d7e8; background: linear-gradient(135deg, #e1e9f3 0%, #f2f6fa 40%, #fff 72%); }
.cv-slate .xb-ipo h3 { color: #1d2f48; }
.cv-slate .xb-ipo__id img { border-color: #c9d7e8; }
.cv-slate .xb-ipo__facts { border-top-color: #c9d7e8; }
.cv-slate .xb-ipo__facts dt { color: #4a5f7a; }

/* Highly rated: sage, light (the user's reference card) */
.cv-sage .gp-ucard { border-color: #d5e5d9; background: linear-gradient(135deg, #dce9df 0%, #f3f7f4 38%, #fff 62%); }
.cv-sage .gp-ucard__rate-value { color: #0a0a0a; }
.cv-sage .gp-ucard__rate-value span { color: #5b4bb0; }
.cv-sage .gp-ucard__tags span { background: #e2ece4; }
.cv-sage .gp-ucard:hover { border-color: #b9d3bf; box-shadow: 0 18px 32px -22px rgba(60, 110, 75, 0.45); }
"""


def refer_css():
    """refer-and-earn.html's header stage and card pair, copied out of
    assets/final.css, minus the phone-only floating share button."""
    css = open(os.path.join(os.path.dirname(X.HERE), "assets", "final.css"), encoding="utf-8").read()
    a = css.index(".gp-refer-stage {")
    b = css.index(".gp-refer-share { margin-top")
    c = css.index("/* Card pair.")
    d = css.index("/* Step rail")
    return css[a:b] + css[c:d]


REFER_STYLE = """
/* Refer & Earn: refer-and-earn.html's header card, sized for the 70% column,
   without app2's steps. */
.xr { --gp-gradient-bond-card: linear-gradient(-71.23deg, #cb9b11 1.58%, #eabe42 24.77%,
    #f7d880 51.26%, #f5dc95 70.66%, #efcc69 83.91%, #be9009 100%); --gp-radius-lg: 20px; }
.xr .gp-refer-stage { gap: 28px; padding: 28px 20px; }
@media (min-width: 768px) {
  .xr .gp-refer-stage { grid-template-columns: minmax(0, 1.15fr) minmax(0, 0.85fr); gap: 32px 40px; padding: 40px; }
}
/* one step above the page's ~30px section titles, not three */
.xr .gp-refer-h1 { max-width: 16ch; font-size: clamp(26px, 2.6vw, 34px); font-weight: 700; }
.xr .gp-refer-sub { font-size: 15px; }
.xr-cta { margin-top: 26px; padding: 0 26px; }
/* Light stage: cream in place of the refer page's ink; the page's own dark button reads on it. */
.xr .gp-refer-stage {
  background:
    radial-gradient(520px 360px at 82% 38%, rgba(230, 179, 37, 0.20), transparent 70%),
    linear-gradient(160deg, #fffaf0 0%, #f8eed3 100%);
  box-shadow: inset 0 0 0 1px rgba(212, 175, 55, 0.35);
  color: #322811;
}
.xr .gp-refer-kicker { color: #8a6520; }
.xr .gp-refer-h1 { color: #322811; }
.xr .gp-refer-sub { color: #5c5240; }
.xr .gp-refer-sub strong { color: #8a6520; }
.xr .gp-refer-card--back { background: linear-gradient(145deg, #f3e3b4, #e9d29a); box-shadow: inset 0 0 0 1px rgba(166, 124, 0, 0.25); }
.xr .gp-refer-card--front { box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.55), inset 0 -1px 0 rgba(120, 88, 0, 0.35),
  0 24px 40px -20px rgba(120, 88, 0, 0.45); }
.xr .gp-refer-cards { width: min(100%, 320px); margin: 8px auto; }
.xr .gp-refer-card__figure { font-size: clamp(40px, 5vw, 56px); }
"""


def refer():
    """refer-and-earn.html's header card (kicker, heading, sub, card pair). Copy as on refer-and-earn.html; the CTA links there,
    as app2's did."""
    r = A.content("refer-and-earn")
    for f in ("Make your GoldenPi Clan now", "High Yielding Fixed Return Investments on GoldenPi",
              "earn referral rewards every time your friend invests"):
        A.need(r, f)
    return ('<section class="xr" data-reveal aria-labelledby="xr-t"><div class="gp-refer-stage">'
            '<div class="gp-refer-copy"><p class="gp-refer-kicker">Refer &amp; Earn</p>'
            '<h2 class="gp-refer-h1" id="xr-t">Make your GoldenPi Clan now</h2>'
            '<p class="gp-refer-sub">Invite your friends to the world of <strong>High Yielding Fixed Return Investments '
            'on GoldenPi</strong> and earn referral rewards every time your friend invests</p>'
            '<a class="xa-gold-btn xr-cta" href="refer-and-earn.html">Refer now</a></div>'
            '<div class="gp-refer-cards" aria-hidden="true"><div class="gp-refer-card gp-refer-card--back"></div>'
            '<div class="gp-refer-card gp-refer-card--front">'
            '<img class="gp-refer-card__logo" src="../assets/img/goldenpi-logo.svg" alt="" width="104" height="24">'
            '<img class="gp-refer-card__gift" src="../assets/img/refer-and-earn-step-3-gift-desktop.png" alt="" width="56" height="66">'
            '<p class="gp-refer-card__label">Refer &amp; Earn Upto</p><p class="gp-refer-card__figure">&#8377;5 Lacs</p></div></div>'
            '<p class="sr-only">Refer &amp; Earn Upto &#8377;5 Lacs</p></div></section>')


HELP_STYLE = """
/* Need help: the support illustration, the copy and hours, then the two ways
   to reach the team as tappable tiles. Icons are the site's phone and mail
   SVGs, masked to one bronze so they read as one family. */
.xh { display: grid; gap: 24px; padding: 28px; border-radius: 20px; background: #fff; border: 1px solid var(--line); }
@media (min-width: 900px) { .xh { grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); align-items: center; gap: 32px; padding: 32px; } }
.xh__intro { display: grid; grid-template-columns: 72px minmax(0, 1fr); gap: 20px; align-items: center; }
.xh__intro img { width: 72px; height: auto; }
.xh h2 { margin: 0; font-size: 22px; line-height: 1.25; font-weight: 700; color: var(--ink); }
.xh__sub { margin: 6px 0 0; max-width: 42ch; font-size: 14px; line-height: 1.55; color: var(--sub); }
.xh__hours { margin: 10px 0 0; font-size: 13px; color: var(--sub); }
.xh__hours b { font-weight: 600; color: var(--ink); }
.xh__ways { display: grid; gap: 10px; }
.xh__way { display: flex; align-items: center; gap: 14px; min-width: 0; padding: 14px 16px; border-radius: 14px;
  background: #faf6ea; border: 1px solid transparent; color: var(--ink); text-decoration: none;
  transition: border-color .25s ease, background-color .25s ease, transform .25s ease; }
.xh__way:hover { border-color: rgba(212, 175, 55, .6); background: #f7efd6; }
.xh__way:active { transform: scale(.99); }
.xh__way:focus-visible { outline: 2px solid #d4af37; outline-offset: 2px; }
.xh__disc { flex: none; display: grid; place-items: center; width: 40px; height: 40px; border-radius: 50%; background: #fff; }
.xh__ic { width: 20px; height: 20px; background: #8a6520; -webkit-mask: var(--m) center / contain no-repeat; mask: var(--m) center / contain no-repeat; }
.xh__way small { display: block; font-size: 12px; color: var(--sub); }
.xh__way b { display: block; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 15px; font-weight: 600; }
.xh__arrow { margin-left: auto; flex: none; color: #8a6520; font-size: 18px; line-height: 1; transition: transform .25s ease; }
.xh__way:hover .xh__arrow { transform: translateX(3px); }
@media (max-width: 639px) { .xh { padding: 20px 16px; } .xh__intro { grid-template-columns: 56px minmax(0, 1fr); gap: 14px; } .xh__intro img { width: 56px; } }
@media (prefers-reduced-motion: reduce) { .xh__way, .xh__arrow { transition: none; } .xh__way:active { transform: none; } }
"""


def help_card():
    """Need help, re-composed. Copy as app2's help_band(), from
    prod_user_explore.md and contact-us.md."""
    A.help_band()  # runs app2's checks that the copy is still in the capture
    way = ('<a class="xh__way" href="%s"><span class="xh__disc"><span class="xh__ic" style="--m: url(../assets/img/%s)" aria-hidden="true"></span></span>'
           '<span><small>%s</small><b>%s</b></span><span class="xh__arrow" aria-hidden="true">&rarr;</span></a>')
    return ('<section class="xh" data-reveal aria-labelledby="xh-t">'
            '<div class="xh__intro"><img src="../assets/img/need-help-img.svg" alt="" width="117" height="158">'
            '<div><h2 id="xh-t">Need help?</h2>'
            '<p class="xh__sub">Talk to our Support Team for free. We will help you through your investment journey.</p>'
            '<p class="xh__hours">Hours <b>Mon to Fri, 9:00 am to 6:30 pm</b></p></div></div>'
            '<div class="xh__ways">%s%s</div></section>'
            % (way % ("tel:080-45685666", "phone-icon.svg", "Call", "080-45685666"),
               way % ("mailto:contact-us@goldenpi.com", "mail.svg", "Email", "contact-us@goldenpi.com")))


def bond(c, i):
    """collection-explore's card, without the note strip."""
    return re.sub(r'\n  <p class="gp-ucard__note">.*?</p>', "", A.C.card(c, i))


def body(shelf_n=4):
    A.bond = bond  # shelves() looks bond up at call time
    A.SHELF_N = shelf_n  # 4: two rows of two; the card needs ~400px, the 70% column fits two
    b = A.body()
    for old, new in [('<section class="xb-shelf" data-reveal aria-labelledby="xb-high-returns">',
                      '<section class="xb-shelf cv-gold" data-reveal aria-labelledby="xb-high-returns">'),
                     ('<section class="xb-ipos" data-reveal', '<section class="xb-ipos cv-slate" data-reveal'),
                     ('<section class="xb-shelf" data-reveal aria-labelledby="xb-highly-rated">',
                      '<section class="xb-shelf cv-sage" data-reveal aria-labelledby="xb-highly-rated">'),
                     # the user's heading for the collections pills, in place of "Find bonds by goal"
                     ('<span id="xa-cols-t">Find bonds by goal</span>', '<span id="xa-cols-t">Choose a bond category</span>')]:
        if b.count(old) != 1:
            raise SystemExit("app2's markup changed, re-check: %r" % old)
        b = b.replace(old, new)
    b, n = re.subn(r'<section class="xb-refer".*?</section>', lambda m: refer(), b, count=1, flags=re.S)
    if n != 1:
        raise SystemExit("app2's Refer & Earn block not found")
    b, n = re.subn(r'<section class="xb-help".*?</section>', lambda m: help_card(), b, count=1, flags=re.S)
    if n != 1:
        raise SystemExit("app2's Need help block not found")
    return b


def main():
    X.assemble(body(), OUT, "Explore | GoldenPi",
               "pages/_explore_app5.py (user-explore-app2.html with a gold, slate and sage card block)",
               style=A.STYLE + "<style>\n" + ucard_css() + refer_css() + STYLE + REFER_STYLE + HELP_STYLE + "</style>\n", script=A.SCRIPT)


if __name__ == "__main__":
    main()
