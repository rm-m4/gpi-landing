#!/usr/bin/env python3
"""user-fixed-deposits-app2.html: the logged-in Fixed Deposits landing, new
version, in user-explore-app7's language.

  1. three promoted FDs on app6/7's dark rotating stage
  2. FD security is our topmost priority
  3. Bank FDs     4. NBFC FDs   (collection-explore cards: slate, gold)
  5. Top PSU Banks vs FDs on GoldenPi (the user's heading): SBI's and
     Unity's highest rates, and Traditional Banks vs GoldenPi FDs
  6. the returns calculator, last

In app7's 70:30 split; the rail carries the user's first-FD offer (their copy).

Every rate, tenure, payout and protection line is captured: content/
prod_user_fixed-deposits.md (the promoted three, DICGC line, "RBI-regulated"),
fixed-deposits.md (bank and NBFC plans, Traditional Banks, Trusted Platform)
and beta_fixed-deposits_GPID105192_unity.md (the SBI comparison). The section
heading "FD security is our topmost priority" is the user's. SBI is the only
PSU bank with a captured rate, so the comparison is against SBI alone.

    python3 pages/_fd_app2.py
"""
import os
import re

import _explore_app as X
import _explore_app2 as A
import _explore_app6 as G
import _explore_app7 as S
import _fd_app as FD

OUT = os.path.join(X.HERE, "user-fixed-deposits-app2.html")
IMG = "../assets/img/"
UNITY = "fd-details.html"   # the one FD detail page in the repo
LIVE_FD = FD.LIVE_FD


def need(name, *strings):
    text = A.content(name)
    for s in strings:
        A.need(text, s)


# -------------------------------------------------------------------- data
# Two kinds of FD (the user's rule): a Bank FD is protected by DICGC insurance up
# to ₹5 lakh; an NBFC FD by its credit rating. A card shows only the issuer, its
# logo, the most a user can earn, and that one protection line.
DICGC = ("DICGC insurance", "up to &#8377;5 lakh")   # prod_user_fixed-deposits.md: "DICGC insurance up to ₹5 lakh"
# (logo, name, href, max rate, rating or None)
BANKS = [("GPID105192.Unity.png", "Unity Small Finance Bank", UNITY, "8.50", None),
         ("GPID105191.Suryoday.png", "Suryoday Small Finance Bank", LIVE_FD, "8.50", None),
         ("GPID106947.utkarsh_logo.png", "Utkarsh Small Finance Bank", LIVE_FD, "8.25", None)]
# Ratings: Mahindra's "AAA Rated" is in the capture; Shriram's and Bajaj's are
# the user's (2026-10-10), not yet in a capture.
NBFCS = [("GPID100016.Shriram-Squircle.png", "Shriram Finance", LIVE_FD, "8.05", "AAA Rated"),
         ("GPID105193.Mahindra-Squircle.png", "Mahindra Finance", LIVE_FD, "7.80", "AAA Rated"),
         ("GPID100379.Bajaj-Finserv.png", "Bajaj Finance Ltd", LIVE_FD, "7.75", "AAA Rated")]
# The promoted three: the user FD page's "Available Fixed Deposit Options" (all banks).
PROMOTED = BANKS


def check():
    need("fixed-deposits", "UNITY SMALL FINANCE BANK", "4.00-8.50%", "4.00-8.25%", "SHRIRAM FINANCE", "6.64-8.05%",
         "MAHINDRA FINANCE", "6.40-7.80%", "AAA Rated", "Returns upto", "BAJAJ FINANCE LTD", "6.41-7.75%", "Traditional Banks", "5 - 7%",
         "Cumulative, Monthly, Quarterly, Half-Yearly, Yearly", "Monthly, Quarterly, At maturity",
         "Compare FDs from leading banks and NBFCs in one place")
    need("prod_user_fixed-deposits", "Highest returns up to 8.5% pa", "DICGC insurance up to ₹5 lakh",
         "Invest in RBI-regulated small banks and NBFCs with Annual returns up to 8.5%", "Insured upto ₹5L",
         "CRISIL AAA", "7 D - 60 M", "Explore Fixed Deposit")
    need("beta_fixed-deposits_GPID105192_unity", "7.20%", "18.06% Higher", "8.50%",
         "Comparison of highest returns across all tenures and age groups", "Equal RBI Protection",
         "DICGC Insurance Upto ₹5 Lacs for both State Bank of India & Unity Small Finance Bank")


def card(fd, k):
    """An FD: logo and issuer, "Returns upto" the maximum rate, and its one
    protection line (DICGC for a bank, the credit rating for an NBFC)."""
    logo, name, href, rate, rating = fd
    line = '<p class="fdc__safe%s"><img src="%s%s" alt="" width="20" height="20"><span><b>%s</b> %s</span></p>'
    if rating is None:
        safe = line % ("", IMG, "shield.png", DICGC[0], DICGC[1])
    elif rating:
        safe = line % ("", IMG, "high-rated-collection.png", rating, "Credit rating")
    else:  # DATA: rating not captured yet
        safe = ("<!-- DATA: credit rating not captured; confirm before handoff. -->"
                + line % (" fdc__safe--tbc", IMG, "high-rated-collection.png", "Credit rating", "to be confirmed"))
    return ('<a class="gp-ucard fdc" href="%s" style="--i:%d">'
            '<div class="fdc__id"><span class="gp-ucard__logo"><img src="%s%s" alt="" width="44" height="44"></span>'
            '<h3 class="gp-ucard__issuer">%s</h3></div>'
            '<div class="fdc__rate"><span>Returns upto</span><p class="gp-ucard__rate-value">%s<span>%%</span></p></div>%s</a>'
            % (href, k, IMG, logo, name, rate, safe))


# ------------------------------------------------------------------ blocks
def promoted():
    slots = "".join('<div class="xs-slot" data-pos="%d">%s</div>' % (pos, card(fd, 0))
                    for pos, fd in zip((0, 1, -1), PROMOTED))
    return ('<section class="xa-hero xs" aria-labelledby="xs-t"><!-- DATA: the three promoted FDs, goldenpi.com 2026-09-26. -->'
            '<div class="xs__head"><h1 id="xs-t">Explore <span class="xs__gold">Fixed Deposit</span></h1>'
            '<p>Highest returns <span class="xs__gold">up to 8.5%%</span> pa</p></div>'
            '<div class="xs-stage" tabindex="0" role="region" aria-roledescription="carousel" '
            'aria-label="Promoted fixed deposits. Use the left and right arrow keys to turn the cards.">%s</div></section>' % slots)


# app7's "Why invest in bonds on GoldenPi?" block (x7w), same look and markup.
# Copy is the user's (2026-10-10), two typos corrected.
SECURITY = [("shield", IMG + "bd5/tile-shield.png", "DICGC insured up to ₹5 lakh",
             "Your deposits are insured up to ₹5 lakh per depositor per bank, under DICGC rules."),
            ("bank", IMG + "Goverment.png", "RBI-registered NBFCs",
             "Only high rated NBFCs with AAA credit rating, to ensure your investment safety.")]


def security():
    tiles = "".join('<li class="x7w__tile x7w__tile--%s"><span class="x7w__art"><img src="%s" alt="" loading="lazy"></span>'
                    '<h3>%s</h3><p>%s</p></li>' % t for t in SECURITY)
    return ('<section class="x7w" data-reveal aria-labelledby="x8sec-t"><h2 id="x8sec-t">Your FD security is our priority</h2>'
            '<ul class="x7w__tiles">%s</ul></section>' % tiles)


def fd_list(slug, title, tone, fds):
    return ('<!-- DATA: %s plans, fixed-deposits.md (goldenpi.com 2026-09-26). -->\n'
            '<section class="x7s x7s--%s" data-reveal aria-labelledby="x8-%s"><h2 id="x8-%s">%s</h2>'
            '<div class="x8__grid">%s</div></section>'
            % (title, tone, slug, slug, title, "".join(card(fd, k) for k, fd in enumerate(fds))))


def compare():
    # The PSU bar is State Bank of India, the one PSU bank with a captured rate; the note says so.
    rows = [("Highest Returns", "5 - 7%", "up to 8.5% pa"),
            ("Insured", "Yes", "Yes, Bank FDs (Insured upto ₹5L)"),
            ("New Bank A/C Required", "Yes", "No")]
    table = "".join('<tr><th scope="row">%s</th><td>%s</td><td>%s</td></tr>' % r for r in rows)
    return ('<!-- DATA: 7.20%% is State Bank of India\'s and 8.50%% Unity SFB\'s highest rate (Unity FD page, beta 2026-10-08);\n'
            '     the table is Traditional Banks vs GoldenPi FDs from fixed-deposits.md. -->'
            '<section class="x8cmp" data-reveal aria-labelledby="x8cmp-t">'
            '<h2 id="x8cmp-t">Top PSU Banks <span class="x8cmp__vs">vs</span> <span class="x8cmp__us">FDs on GoldenPi</span></h2>'
            '<div class="x8cmp__grid">'
            '<div class="x8cmp__chart" role="img" aria-label="Highest returns: PSU bank FD (State Bank of India) 7.20%%, FD on GoldenPi (Unity Small Finance Bank) 8.50%%, 1.30%% extra">'
            '<div class="x8cmp__col"><b>7.20%%</b><span class="x8cmp__bar x8cmp__bar--psu" style="height:%dpx">'
            '<img src="%sportfolio/bank.png" alt="" width="44" height="44"></span><span class="x8cmp__name">PSU Bank FD</span></div>'
            '<div class="x8cmp__gain" aria-hidden="true"><span class="x8cmp__pill">+1.30%% Extra</span>'
            '<svg viewBox="0 0 120 60" preserveAspectRatio="none"><path d="M4 56 C 44 50, 76 26, 112 8" fill="none" stroke="#f4e3a6" stroke-width="1.5" vector-effect="non-scaling-stroke"/>'
            '<path d="M102 5 L114 7 L108 17" fill="none" stroke="#f4e3a6" stroke-width="1.5" vector-effect="non-scaling-stroke"/></svg></div>'
            '<div class="x8cmp__col x8cmp__col--us"><b>8.50%%</b><span class="x8cmp__bar x8cmp__bar--us" style="height:%dpx">'
            '<img src="%sgoldenpi-logo-white.svg" alt="" width="44" height="44"></span><span class="x8cmp__name">FD on GoldenPi</span></div></div>'
            '<table class="x8cmp__table"><thead><tr><th scope="col"><span class="sr-only">Feature</span></th>'
            '<th scope="col">Traditional Banks</th><th scope="col">GoldenPi FDs</th></tr></thead><tbody>%s</tbody></table></div>'
            '<p class="x8cmp__note">Comparison of highest returns across all tenures and age groups. PSU bank: State Bank of India; '
            'GoldenPi: Unity Small Finance Bank.</p></section>'
            % (150, IMG, 200, IMG, table))  # bars 150 / 200px: shortened for contrast (the user's call), not to scale


def rail():
    # The user's offer copy (not in the capture); terms to follow from the business.
    return ('<aside class="xb-rail x8r" aria-label="Offers"><section class="x8offer" aria-labelledby="x8offer-t">'
            '<img src="%srefer-earn-gift.png" alt="" width="88" height="88">'
            '<h2 id="x8offer-t">Invest in your first FD and get a &#8377;500 Amazon voucher.</h2>'
            '</section></aside>' % IMG)  # no CTA: the user's call


def body():
    check()
    # app7's 70:30 split: the stage and every section left, the offer in the sticky rail.
    main = "".join([security(), fd_list("banks", "Bank FD", "slate", BANKS),
                    fd_list("nbfcs", "NBFC FD", "gold", NBFCS), compare(), FD.calculator()])
    return ('<main id="main-content" class="xa-page"><div class="xa xb x7 x8"><div class="xa-hero-wrap">%s</div>%s'
            '<div class="xa-main">%s</div></div></main>' % (promoted(), rail(), main))


STYLE = """
/* user-fixed-deposits-app2: app7's 70:30 split and language. */
@media (min-width: 1200px) { .xa.xb.x8 { grid-template-columns: minmax(0, 79fr) minmax(0, 36fr); column-gap: 30px; } }
.x8 .xa-main { gap: 48px; }

/* the offer card (rail) */
/* black, white and gold (the user's call): black card, white copy, gold hairline and button */
.x8offer { position: relative; overflow: hidden; display: grid; gap: 16px; justify-items: start; padding: 28px 24px 24px; border-radius: 24px;
  color: #fff; border: 1px solid rgba(237, 201, 103, .55);
  background: radial-gradient(320px 180px at 100% 0%, rgba(237, 201, 103, .2), transparent 70%), linear-gradient(135deg, #1a1712 0%, #0b0a08 100%);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, .08), 0 24px 48px -24px rgba(0, 0, 0, .6); }
.x8offer img { width: 88px; height: 88px; filter: drop-shadow(0 8px 10px rgba(80, 55, 0, .3)); }
.x8offer h2 { margin: 0; font-size: 22px; line-height: 1.3; font-weight: 700; letter-spacing: -.01em; color: #fff; }
/* one card in the rail: full width wherever the rail sits under the stage (app7's rail is two columns there) */
.x8 .xb-rail { grid-template-columns: minmax(0, 1fr); }
@media (min-width: 640px) and (max-width: 1199px) { .x8offer { grid-template-columns: auto minmax(0, 1fr); align-items: center; } }
.x8 .xa-head__title, .x8 .xa-main > section:not(.x7w) > h2 { margin: 0; font-size: 18px; line-height: 28px; font-weight: 600; color: #322811; }
.x8 .xs__head h1 { margin: 0; font-size: clamp(18px, 1.8vw, 22px); line-height: 1.3; font-weight: 600; color: #f4e9c8; }
/* the promoted stage: wider cards for the bank names */
@media (min-width: 900px) { .x8 .xs-slot { width: min(420px, 50%); } }
/* names wrap beside the rate; facts stay on one line */
.x8 .gp-ucard__id > div { min-width: 0; }
.x8 .xs .gp-ucard__sold { white-space: normal; }
.x8 .gp-ucard__metrics dt, .x8 .gp-ucard__metrics dd { white-space: nowrap; }

/* FD security: app7's x7w; the bank tile takes the second tint */
.x8 .x7w__tile--bank { background: #fff1e8; }

/* FD card: issuer, the most you can earn, one protection line. Three to a row. */
.x8__grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }
.x8 .fdc { display: grid; align-content: start; gap: 18px; padding: 20px; border-radius: 20px; border-width: 1.17px; min-height: 0; }
.x8 .fdc__id { display: flex; align-items: center; gap: 12px; min-width: 0; }
.x8 .fdc .gp-ucard__logo { width: 44px; height: 44px; border-radius: 12px; background: #fff; }
.x8 .fdc .gp-ucard__issuer { font-size: 15px; line-height: 1.3; font-weight: 600; }
.x8 .fdc__rate { display: grid; gap: 2px; }
.x8 .fdc__rate > span { font-size: 12px; font-weight: 500; color: var(--sub); }
.x8 .fdc .gp-ucard__rate-value { color: #0a0a0a; font-size: 34px; line-height: 38px; letter-spacing: -1px; text-align: left; }
.x8 .fdc .gp-ucard__rate-value span { color: #472d75; font-size: 14px; }
.x8 .fdc__safe { display: flex; align-items: center; gap: 10px; margin: 0; padding-top: 14px; border-top: 1px solid rgba(50, 40, 17, .1); }
.x8 .fdc__safe img { flex: none; width: 24px; height: 24px; object-fit: contain; }
.x8 .fdc__safe span { display: grid; gap: 1px; font-size: 12px; line-height: 1.35; color: var(--sub); }
.x8 .fdc__safe b { font-size: 14px; font-weight: 600; color: #322811; }
.x8 .fdc__safe--tbc img { filter: grayscale(1); opacity: .5; }
.x8 .fdc__safe--tbc b { color: var(--sub); }
.x8 .x7s--slate .fdc { border-color: #c2daf0; background: linear-gradient(-45.6deg, #fff 41.2%, #c7def2 99.5%); }
.x8 .x7s--gold .fdc { border-color: #f2ecc3; background: linear-gradient(-46.6deg, #fff 49.8%, #efeabd 99.5%); }
.x8 .xs .fdc { min-height: 0; }
@media (max-width: 767px) {
  .x8__grid { display: flex; overflow-x: auto; scroll-snap-type: x mandatory; scrollbar-width: none; margin: -4px 0 -10px; padding: 4px 0 10px; }
  .x8__grid::-webkit-scrollbar { display: none; }
  .x8__grid > .fdc { flex: 0 0 min(72%, 280px); scroll-snap-align: start; }
}
.x8 .gp-ucard__sold { color: #5c5240; white-space: nowrap; }
.x8 .x7s .gp-ucard__rate-value { font-size: 30px; line-height: 34px; letter-spacing: -.9px; }

/* comparison: fd-details2's dark chart, with the table on the same surface */
.x8 .xa-main > section.x8cmp > h2 { color: #f1f1f1; }
.x8cmp { display: grid; gap: 28px; padding: 32px 32px 24px; border-radius: 24px; color: #fff; background: #0e1015;
  background-image: radial-gradient(520px 220px at 0% 100%, rgba(237, 201, 103, .12), transparent 70%); }
.x8cmp__vs { font-weight: 400; color: #8e94a2; } .x8cmp__us { color: #edc967; }
.x8cmp__grid { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1.15fr); gap: 40px; align-items: end; }
.x8cmp__chart { display: grid; grid-template-columns: 1fr 120px 1fr; align-items: end; padding-bottom: 36px; border-bottom: 1px solid rgba(255, 255, 255, .2); }
.x8cmp__col { position: relative; display: grid; justify-items: center; gap: 12px; }
.x8cmp__col b { font-size: 20px; font-weight: 700; font-variant-numeric: tabular-nums; } .x8cmp__col--us b { color: #edc967; }
.x8cmp__bar { display: grid; place-items: center; width: 88px; }
.x8cmp__bar--psu { border-radius: 12px 12px 0 0; border: 1px solid #d7caaa; border-bottom: 0; background: linear-gradient(180deg, #403a2e, #221f1a 29%, #1a1815 73%); }
.x8cmp__bar--psu img { width: 44px; height: 44px; object-fit: contain; }
.x8cmp__bar--us { width: 92px; border-radius: 20px 20px 0 0; border: 1px solid #ffefa3; border-bottom: 0;
  background: linear-gradient(105deg, #f7d880 0%, #c69a1c 55%, #8a6520 100%); box-shadow: 0 15px 22px rgba(0, 0, 0, .5); }
/* the logo's mark only (left of the wordmark), inked dark on gold */
.x8cmp__bar--us img { width: 44px; height: 44px; object-fit: cover; object-position: left center; filter: brightness(0); opacity: .85; }
.x8cmp__name { position: absolute; top: calc(100% + 10px); width: 130px; font-size: 13px; font-weight: 600; text-align: center; color: #f5f7fa; }
.x8cmp__gain { position: relative; align-self: stretch; }
.x8cmp__gain svg { position: absolute; left: -16px; right: -16px; bottom: 150px; width: calc(100% + 32px); height: 48px; }
.x8cmp__pill { position: absolute; left: 50%; bottom: 206px; transform: translateX(-50%); white-space: nowrap; padding: 4px 12px; border-radius: 999px;
  border: 1px solid #edc967; color: #edc967; font-size: 12px; font-weight: 600; }
@media (prefers-reduced-motion: no-preference) {
  .x8cmp.is-in .x8cmp__gain { animation: x8-slide .5s ease-out both; }
}
@keyframes x8-slide { from { transform: translateX(-40px); opacity: 0; } to { transform: none; opacity: 1; } }
.x8cmp__table { width: 100%; border-collapse: collapse; font-size: 14px; }
.x8cmp__table th, .x8cmp__table td { padding: 14px 12px; text-align: left; vertical-align: top; line-height: 1.45; }
.x8cmp__table thead th { padding-top: 0; font-size: 13px; font-weight: 600; color: rgba(255, 255, 255, .6); }
.x8cmp__table thead th:last-child { color: #edc967; }
.x8cmp__table tbody th { width: 30%; font-weight: 500; color: rgba(255, 255, 255, .6); }
.x8cmp__table tbody td { color: rgba(255, 255, 255, .75); }
.x8cmp__table tbody td:last-child { font-weight: 600; color: #fff; }
.x8cmp__table tbody tr > * { border-top: 1px solid rgba(255, 255, 255, .12); }
.x8cmp__note { margin: 0; font-size: 11px; line-height: 1.5; color: rgba(255, 255, 255, .55); }

@media (max-width: 899px) { .x8cmp__grid { grid-template-columns: minmax(0, 1fr); gap: 52px; } .x8cmp__chart { max-width: 420px; width: 100%; justify-self: center; } }
@media (max-width: 767px) {
}
@media (max-width: 639px) {
  .x8 .xa-main { gap: 40px; }
  /* offer: one compact row, gift beside the copy */
  .x8offer { grid-template-columns: auto minmax(0, 1fr); align-items: center; gap: 14px; padding: 14px 16px; border-radius: 20px; }
  .x8offer img { width: 52px; height: 52px; }
  .x8offer h2 { font-size: 15px; line-height: 1.35; }
  .x8cmp { padding: 24px 16px 20px; gap: 24px; }
  .x8cmp__chart { grid-template-columns: 1fr 90px 1fr; }
  .x8cmp__name { width: 110px; font-size: 12px; }
  .x8 .gp-ucard__metrics dt { white-space: nowrap; }
  .x8 .gp-ucard__metrics div + div { padding-left: 12px; }
  .x8 .gp-ucard__metrics div:not(:last-child) { padding-right: 12px; }
  .x8cmp__table th, .x8cmp__table td { padding: 12px 8px; font-size: 13px; }
}
"""


def header(page):
    """app7's final navbar, with FD current."""
    page = S.header(page)
    page, n = re.subn(r'<a class="nb__link" href="user-fixed-deposits(?:-app2)?.html">',  # portfolio.html may be prototype-wired
                      '<a class="nb__link is-current" href="user-fixed-deposits.html" aria-current="page">', page, count=1)
    if n != 1:
        raise SystemExit("FD link not found in the navbar")
    return page


def main():
    X.assemble(body(), OUT, "Fixed Deposits | GoldenPi",
               "pages/_fd_app2.py (logged-in FD landing, new version, in user-explore-app7's language)",
               style=A.STYLE + FD.STYLE + "<style>\n" + S.F.ucard_css() + G.HERO_STYLE + S.STYLE + STYLE + "</style>\n",
               script=A.SCRIPT + S.HERO_JS + FD.SCRIPT)
    with open(OUT, encoding="utf-8") as f:
        page = header(f.read())
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page)


if __name__ == "__main__":
    main()
