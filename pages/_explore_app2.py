#!/usr/bin/env python3
"""user-explore-app2.html: user-explore-app.html re-composed.

The page is one 70/30 split from the top. Left: the black header card with the
top three deals in home-premium2's rotating carousel, then high yield bonds, the live NCD IPO, collections, highly rated bonds, Refer &
Earn, Need help, why bonds and a closing app card. Right, sticky: the portfolio
card and pending orders.

Copy sources: the deals are home-premium2's (index.html snapshot); shelves are
crawl/rendered/collections.tabs.json; Refer & Earn is content/refer-and-earn.md;
Need help is content/prod_user_explore.md; contact lines are
content/contact-us.md; why bonds is user-corporate-bonds3's; the app card is
content/play-store.md. Pending orders are sample copy (DATA).

    python3 pages/_explore_app2.py
"""
import html
import importlib.util
import os
import re

import _bond_beta as B
import _explore_app as X
import _explore_bonds3 as W

HERE = X.HERE
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "user-explore-app2.html")
_spec = importlib.util.spec_from_file_location("colpages", os.path.join(HERE, "_collections.py"))  # the name clashes with stdlib's
C = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C)
esc = html.escape
IMG = X.IMG
R = "&#8377;"


def content(name):
    return W.content(name)


def need(text, s):
    return W.need(text, s)


# -------------------------------------------------------------- header deals
# home-premium2's three Bond Utsav deals (index.html snapshot 2026-09-25), links as crawled.
DEALS = [
    ("GPID104095.Neogrowth-new-logo-1-.jpg", "NeoGrowth", "13.00%", "Fixed returns &middot; ICRA BBB", "Half Yearly", "30-Apr-2028",
     "https://uatnew.goldenpi.com/bonds/GPID107371/neogrowth-1300-bond-yield?src=view_details&tenureDate=30-Apr-2028"),
    ("GPID102720.AKARA-CAPITAL-ADVISORS-PRIVATE-LIMITED-2x.png", "Akara", "13.00%", "Fixed returns &middot; ACUITE BBB+", "Monthly", "3-Dec-2027",
     "https://uatnew.goldenpi.com/bonds/GPID107435/akara-1300-bond-yield?src=view_details&tenureDate=03-Dec-2027"),
    ("GPID107347.Best-Capital.png", "Best Capital", "13.00%", "Fixed returns &middot; IVR BBB", "Monthly", "11-Sep-2029",
     "https://uatnew.goldenpi.com/bonds/GPID107433/best-capital-1300-bond-yield?src=view_details&tenureDate=11-Sep-2029"),
]


def hero():
    cards = "".join(
        '<article class="xb-deal" data-pos="%d"><div class="xb-deal__top"><img src="../assets/img/%s" alt="" width="44" height="44">'
        '<div><h2>%s</h2><span>Bond Utsav deal</span></div></div>'
        '<p class="xb-deal__rate">%s</p><p class="xb-deal__label">%s</p>'
        '<div class="xb-deal__foot"><dl><div><dt>Payout</dt><dd>%s</dd></div><div><dt>Maturity Date</dt><dd>%s</dd></div></dl>'
        '<a href="%s">View bond %s<span class="sr-only">: %s</span></a></div></article>'
        % (k - 1, logo, name, rate, label, payout, mat, esc(href), X.ic("arrow.svg"), name)
        for k, (logo, name, rate, label, payout, mat, href) in enumerate(DEALS))
    return """<div class="xb-hero__head">
    <h1 class="xa-hero__title xa-in" id="xa-title">Welcome back, <span data-user="first-name">Investor</span></h1>
    <p class="xa-hero__sub xa-in" style="--d:1">Today&#39;s top bond deals and live NCD IPOs, with fixed returns up to <span class="xa-gold">13%</span>.</p>
</div>
<section class="xa-hero xb-hero" aria-label="Bond Utsav top deals">
  <!-- DATA: top 3 Bond Utsav deals, index.html snapshot 2026-09-25 (as on home-premium2). -->
  <div class="xb-stage xa-in" style="--d:2" role="region" aria-roledescription="carousel" aria-label="Top deals">
    {cards}
  </div>
</section>""".format(cards=cards)


# ---------------------------------------------------------- collections, IPO
def collections():
    pills = "".join('<li><a class="xb-pill" href="%s"><img src="%s%s" alt="" width="28" height="28">%s</a></li>' % (h, IMG, f, t)
                    for f, t, h in X.COLLECTIONS)
    return ('<section class="xb-cols" data-reveal aria-labelledby="xa-cols-t">%s<ul class="xb-pills">%s</ul></section>'
            % (X.head('<span id="xa-cols-t">Find bonds by goal</span>', "Curated collections, from NCD IPOs to short term bonds.", ""), pills))


def ipo():
    """The live NCD IPO (ipo-details.html's issue). Figures from content/beta_bond-ipo_GPID104212_smc.md."""
    smc = content("beta_bond-ipo_GPID104212_smc")
    for f in ("IPO LIVE", "9-OCT-2026", "Coupon upto", "\n10%\n", "₹10,000", "ICRA A", "Secured"):
        need(smc, f)
    facts = "".join('<div><dt>%s</dt><dd>%s</dd></div>' % kv for kv in
                    (("Coupon", "Up to 10%"), ("Min. investment", R + "10,000"), ("Rating", "ICRA A"), ("Security", "Secured")))
    return ('<!-- DATA: the live NCD IPO, beta snapshot 2026-10-08. -->\n'
            '<section class="xb-ipos" data-reveal aria-labelledby="xb-ipos-t">%s'
            '<article class="xb-ipo" aria-labelledby="xb-ipo-t">'
            '<div class="xb-ipo__id"><img src="../assets/img/ipo/smc-logo.png" alt="" width="48" height="48">'
            '<div><p class="xb-ipo__live"><i aria-hidden="true"></i>NCD IPO live &middot; Closes on 9-Oct-2026</p>'
            '<h3 id="xb-ipo-t">SMC Global Securities Limited</h3></div></div>'
            '<dl class="xb-ipo__facts">%s</dl>'
            '<a class="xa-gold-btn xb-ipo__cta" href="ipo-details.html">Apply now</a></article></section>'
            % (X.head('<span id="xb-ipos-t">Live NCD IPOs</span>', "Apply to new bond issues before they close.",
                      X.arrow_btn("View all", "collections-ncd-ipo.html", "NCD IPOs")), facts))


# ------------------------------------------------------------ bond shelves
# Titles are prod_user_explore.md's "Our Bond Collections"; cards are each collection's first four.
# Subs are each collection's captured intro, cut down.
SHELVES = [
    ("high-returns", "High yield bonds", "Coupons of 9% to 13% from BBB- to A+ rated issuers, for more credit risk.",
     "collections-high-returns.html"),
    ("highly-rated", "Highly rated bonds", "Rated A, AA or AAA, with a low to negligible probability of default.",
     "collections-highly-rated.html"),
]


SHELF_N = 3  # cards per shelf


def bond(c, i):
    """The /collections card, cut to name, return, rating, tenure and its marketing line."""
    m = {k.title(): v for k, v in c["metrics"]}
    note = c["note"].lstrip("⚡").strip()
    note = ('<p class="xb-bond__note"><img src="../assets/img/utsav-card-bolt.png" alt="" width="14" height="14">%s</p>' % esc(note)
            if note else "")
    return ('<a class="xb-bond" href="%s" style="--i:%d"><div class="xb-bond__main">'
            '<div class="xb-bond__top"><span class="gp-ucard__logo">%s</span><p class="xb-bond__rate">%s<small>%%</small></p></div>'
            '<h3 class="xb-bond__name">%s</h3>'
            '<p class="xb-bond__facts"><span><span class="sr-only">Rating </span>%s</span><span><span class="sr-only">Tenure </span>%s</span></p></div>%s</a>'
            % (esc(C.UAT + c["href"]), i, C.logo(c), esc(c["rate"].replace("%", "").strip()), esc(c["issuer"]),
               esc(m.get("Rating", "")), esc(m.get("Tenure", "")), note))


def shelves():
    """{slug: shelf section}."""
    out = {}
    for slug, title, sub, href in SHELVES:
        cards = "".join(bond(c, i) for i, c in enumerate(C.DATA["tabs"][slug]["cards"][:SHELF_N]))
        sid = "xb-%s" % slug
        out[slug] = ('<!-- DATA: first three bonds of /collections/%s, collections.tabs.json snapshot. -->\n'
                   '<section class="xb-shelf" data-reveal aria-labelledby="%s">'
                   '%s<div class="xb-bonds">%s</div></section>'
                   % (slug, sid, X.head('<span id="%s">%s</span>' % (sid, esc(title)), esc(sub),
                                        X.arrow_btn("View all", href, title.lower())), cards))
    return out


# ----------------------------------------------------------------- refer
def refer():
    r = content("refer-and-earn")
    # The capture's three steps and figures, in sentence case.
    for s in ("Share Your Unique GoldenPi Referral Link With Your Friends.",
              "You Earn 1% Of Their Investment Amount (Up To ₹2,000 Per Investment).",
              "Earn up to ₹5 Lacs In Rewards", "Refer Up To 50 Friends And Earn Reward For Each Successful Investment."):
        need(r, s)
    steps = [("Share your link", "Send your unique GoldenPi referral link to friends."),
             ("They invest in bonds", "You earn 1% of their investment, up to ₹2,000 each time."),
             ("Earn up to ₹5 Lacs", "Refer up to 50 friends and earn on every successful investment.")]
    lis = "".join('<li style="--i:%d"><b>%s</b><span>%s</span></li>' % (k, esc(t), esc(b)) for k, (t, b) in enumerate(steps))
    return ('<section class="xb-refer" data-reveal aria-labelledby="xb-refer-t">'
            '<div class="xb-refer__head"><img src="%sdo-gift.png" alt="" width="64" height="64">'
            '<div><h2 class="xa-head__title" id="xb-refer-t">Invite friends, earn up to &#8377;5 Lacs</h2>'
            '<p class="xa-head__sub">Refer &amp; Earn, in three steps.</p></div>'
            '<a class="xa-gold-btn xb-refer__cta" href="refer-and-earn.html">Refer now</a></div>'
            '<ol class="xb-steps">%s</ol></section>' % (IMG, lis))


# ------------------------------------------------------------------ help
def help_band():
    prod, cu = content("prod_user_explore"), content("contact-us")
    need(prod, "Talk to our Support Team for free. We will help you through your investment journey.")
    need(cu, "Our working hours are 9:00 am to 6:30 pm from Monday to Friday.")
    need(cu, "contact-us@goldenpi.com"), need(cu, "080-45685666")
    return ('<section class="xb-help" data-reveal aria-labelledby="xb-help-t">'
            '<img class="xb-help__icon" src="../assets/beta/media/support-icon.1ehk__1qamba-.svg" alt="" width="44" height="44">'
            '<div class="xb-help__copy"><h2 id="xb-help-t">Need help?</h2>'
            '<p>Talk to our Support Team for free. We will help you through your investment journey.</p></div>'
            '<dl class="xb-help__lines"><div><dt>Call</dt><dd><a href="tel:080-45685666">080-45685666</a></dd></div>'
            '<div><dt>Email</dt><dd><a href="mailto:contact-us@goldenpi.com">contact-us@goldenpi.com</a></dd></div>'
            '<div><dt>Hours</dt><dd>Mon to Fri, 9:00 am to 6:30 pm</dd></div></dl>'
            '<a class="xa-gold-btn xb-help__cta" href="contact-us.html">Contact us</a></section>')


# ------------------------------------------------------------ why bonds
def why():
    # The FAQ answer's three reasons, one card each.
    items = "".join('<li style="--i:%d"><img src="../assets/img/%s" alt="" width="44" height="44" loading="lazy"><h3>%s</h3><p>%s</p></li>'
                    % (k, i, esc(t), esc(b)) for k, (t, b, i) in enumerate(W.reasons()[:3]))
    stats = "".join('<li>%s</li>' % t for f, t in X.STATS)
    return ('<section class="xb-why" data-reveal aria-labelledby="xb-why-t">%s<ul class="xb-why__grid">%s</ul>'
            '<div class="xb-why__exp"><h2 class="xa-rule">The Golden Experience Of Investing</h2><ul class="xb-why__stats">%s</ul></div></section>'
            % (X.head('<span id="xb-why-t">Why bonds belong in your portfolio</span>', "", ""), items, stats))


# ------------------------------------------------------------- app blocks
PLAY = "https://play.google.com/store/apps/details?id=com.goldenpi.gpimobileapp"


def app_close():
    ps = content("play-store")
    for s in ("GoldenPi: Buy Bonds, FDs & IPO", "Invest 24x7 and track your investments at One Place",
              "Earn 9-14% Fixed returns on Corp. & Govt. Bonds", "Zero Defaults Till Date", "100% Timely Repayment"):
        need(ps, s)
    return ('<section class="xb-app" data-reveal aria-labelledby="xb-app-t">'
            '<div class="xb-app__copy"><img class="xb-app__icon" src="../assets/img/play/app-icon.png" alt="" width="56" height="56">'
            '<h2 id="xb-app-t">Invest and track on the go</h2>'
            '<p>Buy bonds, apply to NCD IPOs and track every payout, 24x7, in one app.</p>'
            '<ul><li>Earn 9-14%% Fixed returns on Corp. &amp; Govt. Bonds</li><li>Zero Defaults Till Date</li><li>100%% Timely Repayment</li></ul>'
            '<a class="xa-gold-btn xb-app__cta" href="%s">Get it on Google Play</a></div>'
            '<img class="xb-app__qr" src="../assets/beta/media/mobile-app-qr.3wptrea2l_26s.svg" alt="Scan to download GoldenPi app" width="132" height="163" loading="lazy">'
            '</section>' % esc(PLAY))


# ------------------------------------------------------------------ rail
# Sample copy (the user asked for it written): pending orders have no capture yet.
ORDERS = [("Muthoot Fincorp bond", "10 units", R + "1,00,520", "Payment pending", "Pay now", "warn"),
          ("SMC Global NCD IPO", "Series V &middot; 5 units", R + "50,000", "Awaiting allotment", "Track", "info")]


def rail():
    orders = "".join(
        '<li class="xb-order"><div><p class="xb-order__name">%s</p><p class="xb-order__meta">%s &middot; %s</p>'
        '<span class="xb-tag xb-tag--%s">%s</span></div><button type="button" class="xb-chip">%s</button></li>'
        % (n, m, amt, tone, st, cta) for n, m, amt, st, cta, tone in ORDERS)
    return """<aside class="xb-rail" aria-label="Your account">
  {port}
  <!-- DATA: pending orders, sample copy. -->
  <section class="xb-orders" data-reveal aria-labelledby="xb-orders-t">
    <h2 class="xa-rail__label" id="xb-orders-t">Pending orders <span class="xb-count">{n}</span></h2>
    <ul class="xb-box xb-list">{orders}</ul>
  </section>
</aside>""".format(port=X.portfolio_card(), n=len(ORDERS), orders=orders)


def body():
    sh = shelves()
    main = (sh["high-returns"] + ipo() + collections() + sh["highly-rated"] + refer() + help_band() + why() + app_close())
    head, card = hero().split("\n<section", 1)
    # The greeting has the first row to itself, so the portfolio card starts level with the deals card.
    return ('<main id="main-content" class="xa-page"><div class="xa xb"><div class="xb-head">%s</div>'
            '<div class="xa-hero-wrap"><section%s</div>%s'
            '<div class="xa-main">%s</div></div></main>' % (head, card, rail(), main))


STYLE = """<style>
/* user-explore-app2: one 70/30 split from the top: header card and content left, account rail right. */
.xa.xb { grid-template-areas: "head" "hero" "rail" "main"; }
.xb-head { grid-area: head; min-width: 0; margin-bottom: -12px; }
@media (min-width: 1200px) {
  .xb-head { margin-bottom: -20px; }
  .xa.xb { grid-template-areas: "head ." "hero rail" "main rail"; grid-template-columns: minmax(0, 7fr) minmax(0, 3fr); column-gap: 28px; }
  .xb-rail { align-self: start; position: sticky; top: 96px; }
}
.xb-rail { grid-area: rail; min-width: 0; display: grid; gap: 16px; }
@media (min-width: 768px) and (max-width: 1199px) {
  .xb-rail { grid-template-columns: repeat(2, minmax(0, 1fr)); column-gap: 20px; align-items: start; }
}

/* header card: copy left-aligned on top, the three deals rotate below (home-premium2) */
.xb-hero { padding: 32px; }
.xb-hero__head .xa-hero__title { color: var(--ink); }
.xb-hero__head .xa-hero__sub { color: var(--sub); }
.xb-hero__head .xa-hero__sub .xa-gold { background-image: linear-gradient(170deg, #c69a1c 0%, #a67c00 60%, #8a6520 100%); }
/* Two in view: the front deal on the left, the next one behind it on the right, blurred. Click it to bring it forward;
   the third waits, hidden, behind that. Widths are % of the stage so the back card's right edge meets the stage's. */
.xb-stage { position: relative; height: 290px; }
.xb-deal { position: absolute; left: 0; top: 0; width: 64%; padding: 26px; border-radius: 20px; color: #f4e9c8; transform-origin: 100% 50%;
  background: linear-gradient(160deg, #2a2216 0%, #17130d 100%); border: 1px solid rgba(212, 175, 55, .22);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, .06), 0 40px 80px -30px rgba(0, 0, 0, .7);
  transition: transform .7s var(--ease), opacity .7s var(--ease), filter .7s var(--ease); }
.xb-deal[data-pos="0"] { z-index: 3; background: linear-gradient(160deg, #e6c65c 0%, #c99d24 100%); border-color: transparent; color: #0f0d0a; }
.xb-deal[data-pos="1"] { z-index: 2; transform: translateX(56.25%) scale(.9); opacity: .6; filter: blur(1.5px); cursor: pointer; }
.xb-deal[data-pos="1"]:hover { opacity: .75; filter: blur(.5px); }
.xb-deal[data-pos="-1"] { z-index: 1; transform: translateX(56.25%) scale(.8); opacity: 0; filter: blur(3px); pointer-events: none; }
.xb-deal__top { display: flex; align-items: center; gap: 12px; }
.xb-deal__top img { width: 44px; height: 44px; border-radius: 12px; background: #fff; object-fit: contain; padding: 4px; }
.xb-deal__top h2 { font-size: 17px; line-height: 1.3; font-weight: 700; }
.xb-deal__top span { font-size: 13px; opacity: .75; }
.xb-deal__rate { margin-top: 22px; font-size: 52px; line-height: 1; font-weight: 800; letter-spacing: -.03em; color: #fff; font-variant-numeric: tabular-nums; }
.xb-deal[data-pos="0"] .xb-deal__rate { color: #0f0d0a; }
.xb-deal__label { margin-top: 6px; font-size: 13px; opacity: .75; }
.xb-deal__foot { margin-top: 22px; padding-top: 16px; border-top: 1px solid rgba(212, 175, 55, .2); display: flex; align-items: end; justify-content: space-between; gap: 16px; }
.xb-deal[data-pos="0"] .xb-deal__foot { border-color: rgba(15, 13, 10, .18); }
.xb-deal__foot dl { display: flex; gap: 24px; margin: 0; }
.xb-deal__foot dt { font-size: 12px; opacity: .7; }
.xb-deal__foot dd { margin: 2px 0 0; font-weight: 700; white-space: nowrap; }
.xb-deal__foot a { display: inline-flex; align-items: center; gap: 6px; font-size: 14px; font-weight: 700; white-space: nowrap; color: #d4af37; }
.xb-deal[data-pos="0"] .xb-deal__foot a { color: #0f0d0a; }
.xb-deal__foot .xa-ic { width: 14px; height: 14px; }
@media (max-width: 1023px) {
  .xb-stage { height: auto; display: grid; margin-top: 0; grid-auto-flow: column; grid-auto-columns: min(86%, 400px); gap: 12px; overflow-x: auto;
    scroll-snap-type: x mandatory; margin: 0 -16px; padding: 0 16px 4px; scrollbar-width: none; }
  .xb-deal, .xb-deal[data-pos] { position: static; width: auto; margin: 0; transform: none; opacity: 1; filter: none; pointer-events: auto; scroll-snap-align: center; cursor: auto; }
  .xb-deal__rate { font-size: 44px; }
  .xb-deal__foot { flex-wrap: wrap; }
}
@media (max-width: 767px) { .xb-hero { padding: 22px 16px 20px; } }

/* collections heading, live IPO strip */
.xa-cols .xa-head { margin-bottom: 16px; }
.xb-ipo { display: grid; grid-template-columns: minmax(0, 1fr) auto; grid-template-areas: "id cta" "facts facts"; align-items: center; gap: 18px 20px; padding: 20px 22px;
  border-radius: 20px; background: linear-gradient(110deg, #fffaf0, #fff 60%); border: 1px solid rgba(212, 175, 55, .45); box-shadow: var(--shadow); }
.xb-ipo__id { grid-area: id; display: flex; align-items: center; gap: 12px; min-width: 0; }
.xb-ipo__id img { flex: none; width: 48px; height: 48px; border-radius: 12px; object-fit: contain; background: #fff; border: 1px solid var(--line); }
.xb-ipo h3 { margin-top: 4px; font-size: 16px; line-height: 1.35; font-weight: 700; color: var(--ink); }
.xb-ipo__live { display: flex; align-items: center; gap: 6px; font-size: 12px; font-weight: 600; color: #06963c; }
.xb-ipo__live i { width: 7px; height: 7px; border-radius: 50%; background: #06963c; }
@media (prefers-reduced-motion: no-preference) { .xb-ipo__live i { animation: xb-live 2s ease-in-out infinite; } }
@keyframes xb-live { 50% { box-shadow: 0 0 0 5px rgba(6, 150, 60, 0); } 0%, 100% { box-shadow: 0 0 0 0 rgba(6, 150, 60, .35); } }
.xb-ipo__facts { grid-area: facts; padding-top: 16px; border-top: 1px solid var(--line); display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin: 0; }
.xb-ipo__facts dt { font-size: 12px; color: var(--sub); }
.xb-ipo__facts dd { margin: 2px 0 0; font-size: 15px; font-weight: 700; color: var(--ink); white-space: nowrap; }
.xb-ipo__cta { grid-area: cta; padding: 0 22px; }
@media (max-width: 639px) {
  .xb-ipo { grid-template-columns: minmax(0, 1fr); grid-template-areas: "id" "facts" "cta"; padding: 18px 16px; }
  .xb-ipo__facts { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .xb-ipo__cta { width: 100%; }
}


/* shelves: compact bond cards, two across */
.xb-shelf .xa-head { align-items: center; }
.xb-bonds { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }
.xb-bond { display: flex; flex-direction: column; overflow: hidden; border-radius: 14px; background: #fff; border: 1px solid var(--line);
  transition: transform .3s var(--ease), border-color .3s var(--ease); }
.xb-bond__main { display: grid; gap: 14px; padding: 18px 18px 16px; }
.xb-bond__top { display: flex; align-items: flex-start; justify-content: space-between; gap: 10px; }
.xb-bond .gp-ucard__logo { flex: none; display: grid; place-items: center; width: 44px; height: 44px; border-radius: 50%; overflow: hidden; background: #fff; border: 1px solid var(--line); }
.xb-bond .gp-ucard__logo img { width: 100%; height: 100%; object-fit: contain; }
.xb-bond .gp-ucard__initial { font-weight: 700; color: var(--bronze); }
.xb-bond__name { min-width: 0; margin-top: -4px; font-size: 15px; line-height: 1.3; font-weight: 700; color: var(--ink); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.xb-bond__rate { font-size: 30px; line-height: 1; font-weight: 500; letter-spacing: -.03em; color: #a67c00; font-variant-numeric: tabular-nums; }
.xb-bond__rate small { font-size: 15px; margin-left: 2px; letter-spacing: 0; }
.xb-bond__facts { display: flex; align-items: center; gap: 12px; padding-top: 12px; border-top: 1px solid var(--line); font-size: 14px; font-weight: 600; color: var(--ink); }
.xb-bond__facts > span + span { padding-left: 12px; border-left: 1px solid var(--line); }
.xb-bond__note { display: flex; align-items: center; gap: 6px; margin-top: auto; padding: 9px 18px; font-size: 12px; line-height: 1.35; font-weight: 600; color: #8a6520;
  background: #faf6ea; min-height: calc(2 * 1.35em + 18px); }
.xb-bond__note img { flex: none; }
@media (max-width: 1023px) and (min-width: 640px) { .xb-bonds { grid-template-columns: repeat(2, minmax(0, 1fr)); } .xb-bonds > :nth-child(3) { display: none; } }
@media (max-width: 639px) { .xb-bonds { grid-template-columns: minmax(0, 1fr); } }

/* refer */
.xb-refer { padding: 24px; border-radius: 24px; background: linear-gradient(140deg, #fff 40%, var(--cream)); border: 1px solid rgba(212, 175, 55, .3); }
.xb-refer__head { display: flex; align-items: center; gap: 16px; }
.xb-refer__head > div { flex: 1; min-width: 0; }
.xb-refer__cta { padding: 0 22px; }
.xb-steps { margin: 22px 0 0; padding: 0; list-style: none; counter-reset: s; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }
.xb-steps li { counter-increment: s; display: grid; align-content: start; gap: 6px; padding: 16px; border-radius: 16px; background: #fff; border: 1px solid var(--line); }
.xb-steps li::before { content: counter(s); display: grid; place-items: center; width: 28px; height: 28px; border-radius: 50%;
  font-size: 13px; font-weight: 700; color: #0f0d0a; background: var(--gold-grad); }
.xb-steps b { font-size: 15px; line-height: 1.35; color: var(--ink); }
.xb-steps span { font-size: 13px; line-height: 1.5; color: var(--sub); }
@media (max-width: 767px) {
  .xb-refer { padding: 18px 16px; }
  .xb-refer__head { flex-wrap: wrap; }
  .xb-refer__cta { width: 100%; }
  .xb-steps { grid-template-columns: minmax(0, 1fr); }
}

/* Need help, full width of the column */
.xb-help { display: grid; grid-template-columns: auto minmax(0, 1fr) auto auto; align-items: center; gap: 20px; padding: 20px 22px;
  border-radius: 20px; background: #fff; border: 1px solid var(--line); box-shadow: var(--shadow); }
.xb-help h2 { font-size: 17px; font-weight: 700; color: var(--ink); }
.xb-help__copy p { margin-top: 4px; font-size: 13px; line-height: 1.5; color: var(--sub); max-width: 40ch; }
.xb-help__lines { display: grid; gap: 4px; margin: 0; font-size: 13px; }
.xb-help__lines div { display: flex; gap: 8px; }
.xb-help__lines dt { width: 42px; color: var(--sub); }
.xb-help__lines dd { margin: 0; font-weight: 600; color: var(--ink); }
.xb-help__lines a:hover { color: var(--bronze); }
.xb-help__cta { padding: 0 22px; }
@media (max-width: 1023px) { .xb-help { grid-template-columns: auto minmax(0, 1fr); } .xb-help__lines, .xb-help__cta { grid-column: 2; justify-self: start; } }
@media (max-width: 639px) { .xb-help { grid-template-columns: minmax(0, 1fr); padding: 18px 16px; } .xb-help__lines, .xb-help__cta { grid-column: 1; } .xb-help__cta { width: 100%; } }

/* why bonds: three reason cards, then the stats strip */
.xb-why .xa-head__sub:empty { display: none; }
.xb-why__grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }
.xb-why__grid li { display: grid; align-content: start; gap: 10px; padding: 20px; border-radius: 14px; background: #fff; border: 1px solid var(--line); }
.xb-why__grid img { width: 44px; height: 44px; object-fit: contain; margin-bottom: 4px; }
.xb-why__grid h3 { font-size: 15px; line-height: 1.35; font-weight: 700; color: var(--ink); }
.xb-why__grid p { font-size: 13px; line-height: 1.55; color: var(--sub); }
.xb-why__exp { display: grid; gap: 20px; margin-top: 40px; }
.xb-why__stats { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); }
.xb-why__stats li { display: grid; justify-items: center; gap: 8px; font-size: 13px; font-weight: 600; color: var(--ink); text-align: center; }
.xb-why__stats li + li { border-left: 1px solid var(--line); }
.xb-why__stats img { width: 36px; height: 36px; object-fit: contain; }
@media (max-width: 767px) { .xb-why__grid { grid-template-columns: minmax(0, 1fr); } .xb-why__exp { margin-top: 32px; } }
@media (max-width: 639px) { .xb-why__stats { grid-template-columns: repeat(2, minmax(0, 1fr)); row-gap: 16px; } .xb-why__stats li:nth-child(3) { border-left: 0; } }

/* closing app card: the page's second dark surface, a bookend to the header */
.xb-app { position: relative; overflow: hidden; display: flex; align-items: center; justify-content: space-between; gap: 24px; padding: 28px; border-radius: 24px; color: #f4e9c8;
  background: radial-gradient(60% 90% at 100% 0%, rgba(212, 175, 55, .22), transparent 70%), #0a0805; }
.xb-app__copy { display: grid; justify-items: start; gap: 10px; min-width: 0; }
.xb-app__icon { border-radius: 14px; }
.xb-app h2 { font-size: 22px; line-height: 1.3; font-weight: 700; color: #fff; }
.xb-app p { font-size: 14px; color: rgba(255, 255, 255, .75); }
.xb-app ul { display: flex; flex-wrap: wrap; gap: 6px 16px; font-size: 13px; color: #edc967; }
.xb-app__cta { margin-top: 6px; padding: 0 22px; }
.xb-app__qr { flex: none; padding: 10px; border-radius: 16px; background: #fff; }
@media (max-width: 639px) { .xb-app { flex-direction: column; align-items: flex-start; padding: 22px 16px; } .xb-app__qr { display: none; } }

/* rail boxes */
.xb-box { padding: 18px; border-radius: 20px; background: #fff; border: 1px solid var(--line); box-shadow: var(--shadow); }
.xb-orders { display: grid; gap: 16px; margin-top: 21px; }
.xb-orders .xa-rail__label { display: flex; align-items: center; gap: 8px; margin-top: 0; }
.xb-count { display: grid; place-items: center; min-width: 22px; height: 22px; padding: 0 6px; border-radius: 999px; font-size: 12px; color: #0f0d0a; background: var(--gold-grad); }
.xb-list { display: grid; padding-top: 6px; padding-bottom: 6px; }
.xb-list > li { display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 12px 0; }
.xb-list > li + li { border-top: 1px solid var(--line); }
.xb-list > li > div { min-width: 0; }
.xb-order__name { font-size: 14px; line-height: 1.4; font-weight: 600; color: var(--ink); }
.xb-order__meta { margin-top: 2px; font-size: 12px; line-height: 1.45; color: var(--sub); }
.xb-tag { display: inline-block; margin-top: 6px; padding: 2px 8px; border-radius: 999px; font-size: 11px; font-weight: 600; }
.xb-tag--warn { color: #b25a00; background: #fff4e5; }
.xb-tag--info { color: var(--bronze); background: var(--cream); }
.xb-chip { flex: none; display: inline-flex; align-items: center; height: 30px; padding: 0 14px; border-radius: 999px; cursor: pointer; font: inherit;
  font-size: 12px; font-weight: 700; color: var(--ink); background: #fff; border: 1px solid rgba(212, 175, 55, .55); transition: background .2s, transform .2s var(--ease); }
.xb-chip:hover { background: var(--cream); }
.xb-chip:active { transform: scale(.97); }

/* Premium pass (design-taste-frontend). Read: post-login home for retail bond and NCD IPO investors, trust-first,
   premium; dials variance 5, motion 4, density 5. Locks: one accent (GoldenPi gold) kept for figures, actions in
   near-black pills; radius 20px panels, 14px nested tiles, full pill controls; cards only where they carry a thing
   you act on (deals, IPO, bonds, rail), sections otherwise sit on the page with spacing and hairlines. */
.xa.xb .xa-main { gap: 56px; }
.xb-deal { border-radius: 14px; }
.xb-hero { border-radius: 20px; background: radial-gradient(60% 75% at 50% 0%, rgba(212, 175, 55, .2), transparent 70%),
  radial-gradient(40% 60% at 50% 100%, rgba(212, 175, 55, .08), transparent 70%), #0d0b08; }
.xb-hero__head { margin-bottom: 20px; }
.xb-hero__head .xa-hero__title { font-size: clamp(28px, 3.2vw, 36px); line-height: 1.15; letter-spacing: -.025em; }
.xb-hero__head .xa-hero__sub { margin-top: 8px; font-size: 16px; }
.xb .xa-head { margin-bottom: 18px; }
.xb .xa-head__title { font-size: 22px; line-height: 1.25; letter-spacing: -.015em; }
.xb .xa-head__sub { margin-top: 4px; }
.xb .xa-gold-btn { height: 44px; padding: 0 22px; font-size: 14px; font-weight: 600; letter-spacing: 0; text-transform: none; color: #fff;
  background: #14110c; box-shadow: none; filter: none; }
.xb .xa-gold-btn:hover { background: #2b2418; transform: none; box-shadow: none; filter: none; }
.xb .xa-gold-btn:active { transform: scale(.98); }
.xb .xa-view { height: auto; padding: 0; border: 0; background: none; font-size: 14px; font-weight: 600; letter-spacing: 0; text-transform: none; color: var(--ink); }
.xb .xa-view:hover { color: var(--bronze); }
.xb .xa-col { height: 104px; border-radius: 14px; border: 1px solid var(--line); box-shadow: none; background: #fff; }
.xb .xa-col:hover { transform: translateY(-2px); border-color: rgba(212, 175, 55, .7); box-shadow: none; }
.xb-ipo { border-radius: 20px; background: #fff; border-color: var(--line); box-shadow: none; }
.xb-bond { border-radius: 14px; border-color: var(--line); }
.xb-bond:hover { transform: translateY(-2px); border-color: rgba(212, 175, 55, .7); box-shadow: none; }
.xb-bond__note { background: #faf6ea; }
/* Refer: the page's one yellow surface; steps are a sequence, not cards */
.xb-refer { border-radius: 20px; border: 0; background: linear-gradient(135deg, #fff6d6 0%, #fde9a6 100%); padding: 28px; }
.xb-steps { gap: 28px; margin-top: 26px; }
.xb-steps li { padding: 0; background: none; border: 0; border-radius: 0; gap: 8px; }
.xb-steps li::before { width: 32px; height: 32px; color: #edc967; background: #14110c; }
/* Help and why sit on the page */
.xb-help { padding: 24px 0; border: 0; border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); border-radius: 0; background: none; box-shadow: none; }
.xb-app { border-radius: 20px; }
.xb-app .xa-gold-btn { background: #edc967; color: #14110c; }
.xb-app .xa-gold-btn:hover { background: #f4d98a; }
.xb-box { border-radius: 20px; box-shadow: 0 1px 2px rgba(50, 40, 17, .04); }
.xb-chip { border-color: var(--line); }
.xb-chip:hover { border-color: #14110c; background: #fff; }
.xb-count { color: #14110c; background: #edc967; }
@media (max-width: 767px) { .xa.xb .xa-main { gap: 44px; } .xb-refer { padding: 20px 16px; } .xb-steps { gap: 18px; } }

/* Clean pass (design-taste-frontend), structure unchanged. Type: Satoshi at medium weight with tight tracking for
   display, 15px floor for reading text. Colour: cream page, white surfaces, near-black ink, gold (#a67c00 on light,
   #e2c372 on black) only on figures. Shape: 20px panels, 14px tiles, pill controls. Depth: hairlines, no shadows
   except the black header card. Rhythm: 72px between sections. */
.xa-page.xa-page { --ink: #1d1a14; --sub: #5f5a50; --line: rgba(50, 40, 17, .1); font-family: satoshi, system-ui, sans-serif; }
.xa.xb .xa-main { gap: 72px; }
.xb-hero__head .xa-hero__title { font-size: clamp(32px, 3.4vw, 44px); line-height: 1.1; font-weight: 500; letter-spacing: -.035em; }
.xb-hero__head .xa-hero__sub { margin-top: 10px; font-size: 17px; }
.xb .xa-head { margin-bottom: 22px; align-items: end; }
.xb .xa-head__title { font-size: clamp(24px, 2.2vw, 28px); line-height: 1.2; font-weight: 500; letter-spacing: -.025em; }
.xb .xa-head__sub { margin-top: 6px; font-size: 15px; line-height: 1.5; }
.xb .xa-view { font-size: 14px; }

/* header card: bigger type in the front deal, a calmer back card */
.xb-hero { box-shadow: 0 30px 60px -36px rgba(50, 40, 17, .55); }
.xb-stage { height: 300px; }
.xb-deal { padding: 28px; }
.xb-deal__top h2 { font-size: 18px; font-weight: 600; }
.xb-deal__rate { margin-top: 26px; font-size: 60px; font-weight: 600; letter-spacing: -.04em; }
.xb-deal__label { font-size: 14px; }
.xb-deal__foot { margin-top: 26px; padding-top: 18px; }
.xb-deal__foot dd { font-size: 15px; }
.xb-deal[data-pos="1"] { opacity: .5; }

/* bond cards */
.xb-bond { border-color: var(--line); }
.xb-bond__main { gap: 16px; padding: 20px 20px 18px; }
.xb-bond__name { font-size: 15px; font-weight: 600; }
.xb-bond__rate { font-size: 32px; font-weight: 500; color: #a67c00; }
.xb-bond__facts { font-size: 14px; font-weight: 500; color: var(--sub); }
.xb-bond__note { font-weight: 500; color: #7a5a14; background: #fbf6e6; }

/* IPO */
.xb-ipo { padding: 24px; border-color: var(--line); }
.xb-ipo h3 { font-size: 18px; font-weight: 600; }
.xb-ipo__facts dt { font-size: 13px; }
.xb-ipo__facts dd { font-size: 16px; font-weight: 600; }
.xb-ipo__facts dd:first-child, .xb-ipo__facts div:first-child dd { color: #a67c00; }

/* collections: pills */
.xb-pills { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; }
@media (max-width: 639px) { .xb-pills { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
.xb-pill { display: flex; align-items: center; gap: 10px; height: 52px; padding: 0 20px 0 12px; border-radius: 999px; background: #fff;
  border: 1px solid var(--line); font-size: 15px; font-weight: 600; color: var(--ink); transition: border-color .25s, transform .25s var(--ease); }
.xb-pill:hover { border-color: #d4af37; transform: translateY(-2px); }
.xb-pill img { width: 28px; height: 28px; object-fit: contain; }

/* refer */
.xb-refer { padding: 32px; }
.xb-refer__head img { width: 56px; height: 56px; }
.xb-refer .xa-head__title { font-size: clamp(24px, 2.4vw, 30px); }
.xb-steps { margin-top: 30px; }
.xb-steps b { font-size: 16px; font-weight: 600; }
.xb-steps span { font-size: 14px; color: #4d4637; }

/* help */
.xb-help { padding: 28px 0; border-color: var(--line); }
.xb-help h2 { font-size: 20px; font-weight: 600; }
.xb-help__copy p, .xb-help__lines { font-size: 14px; }

/* why: three reason cards, then the brand stats as gold type */
.xb-why__grid li { padding: 24px; border-color: var(--line); }
.xb-why__grid h3 { font-size: 16px; font-weight: 600; }
.xb-why__grid p { font-size: 14px; line-height: 1.6; }
.xb-why__exp { margin-top: 48px; gap: 0; }
.xb-why__exp .xa-rule { justify-content: flex-start; margin-bottom: 18px; color: var(--sub); font-weight: 600; }
.xb-why__exp .xa-rule::before { display: none; }
.xb-why__stats { border-top: 1px solid rgba(212, 175, 55, .55); }
.xb-why__stats li { justify-items: start; padding-top: 22px; font-size: clamp(17px, 1.6vw, 20px); font-weight: 500; letter-spacing: -.01em; color: #a67c00; text-align: left; }
.xb-why__stats li + li { padding-left: 20px; }

/* app */
.xb-app { padding: 32px; }
.xb-app h2 { font-size: 24px; font-weight: 600; letter-spacing: -.015em; }
.xb-app p { font-size: 15px; }

/* rail */
.xb-list > li { padding: 16px 0; }
.xb-order__name { font-size: 15px; }
.xb-order__meta { font-size: 13px; }
.xb-tag { padding: 0; margin-top: 6px; background: none !important; font-size: 12px; }
.xb-box { box-shadow: none; border-color: var(--line); }

/* header card v2: shorter (deal laid out across, rate right) and quieter: matte black cards, a gold hairline on
   the front one, gold only on the rate and its link. */
.xb-hero { padding: 24px; background: radial-gradient(55% 80% at 0% 0%, rgba(212, 175, 55, .14), transparent 65%),
  radial-gradient(40% 70% at 100% 100%, rgba(212, 175, 55, .06), transparent 70%), #0d0b08; }
.xb-stage { height: 202px; }
.xb-deal { display: grid; grid-template-columns: minmax(0, 1fr) auto; grid-template-areas: "top rate" "label rate" "foot foot";
  column-gap: 20px; padding: 22px 24px; color: #f4efe3; border: 1px solid rgba(255, 255, 255, .08);
  background: linear-gradient(160deg, #1d1a14 0%, #14120e 100%); box-shadow: inset 0 1px 0 rgba(255, 255, 255, .05); }
.xb-deal[data-pos="0"] { color: #f4efe3; border-color: rgba(226, 195, 114, .45);
  background: linear-gradient(160deg, #241f17 0%, #16130e 100%);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, .07), 0 24px 48px -24px rgba(0, 0, 0, .9); }
.xb-deal__top { grid-area: top; }
.xb-deal__top img { width: 40px; height: 40px; border-radius: 10px; }
.xb-deal__top span { color: rgba(244, 239, 227, .55); opacity: 1; }
.xb-deal__rate, .xb-deal[data-pos="0"] .xb-deal__rate { grid-area: rate; align-self: center; margin: 0; font-size: 52px; font-weight: 500;
  letter-spacing: -.04em; color: #e2c372; }
.xb-deal__label { grid-area: label; margin-top: 10px; font-size: 13px; color: rgba(244, 239, 227, .55); opacity: 1; }
.xb-deal__foot, .xb-deal[data-pos="0"] .xb-deal__foot { grid-area: foot; margin-top: 18px; padding-top: 16px; border-top: 1px solid rgba(255, 255, 255, .08); }
.xb-deal__foot dt { color: rgba(244, 239, 227, .5); opacity: 1; }
.xb-deal__foot dd { font-size: 14px; font-weight: 600; }
.xb-deal__foot a, .xb-deal[data-pos="0"] .xb-deal__foot a { color: #e2c372; }
.xb-deal[data-pos="1"] { opacity: .45; filter: blur(1.5px); }
@media (max-width: 1023px) {
  .xb-stage { height: auto; }
  .xb-deal { grid-template-areas: "top top" "rate rate" "label label" "foot foot"; }
  .xb-deal__rate, .xb-deal[data-pos="0"] .xb-deal__rate { justify-self: start; margin-top: 18px; font-size: 44px; }
}

@media (max-width: 767px) {
  .xa.xb .xa-main { gap: 52px; }
  .xb-deal__rate { font-size: 46px; }
  .xb-refer { padding: 22px 18px; }
  .xb-app { padding: 22px 18px; }
  .xb-pill { height: 46px; font-size: 14px; }
  .xb-why__stats li { padding-left: 0 !important; }
}
</style>
"""

SCRIPT = """<script>
// Deal carousel (home-premium2's): a click on a side card rotates data-pos (-1, 0, 1). Without it the cards keep their places.
(function () {
  var stage = document.querySelector('.xb-stage');
  if (!stage) return;
  var cards = [].slice.call(stage.querySelectorAll('.xb-deal'));
  function shift(d) {
    cards.forEach(function (c) { var p = +c.dataset.pos - d; c.dataset.pos = p > 1 ? -1 : p < -1 ? 1 : p; });
  }
  cards.forEach(function (c) {
    c.addEventListener('click', function (e) {
      var p = +c.dataset.pos;
      if (p && window.matchMedia('(min-width: 1024px)').matches) { e.preventDefault(); shift(p); }
    });
  });
})();
</script>
"""


def main():
    X.assemble(body(), OUT, "Explore | GoldenPi",
               "pages/_explore_app2.py (user-explore-app.html re-composed: deal carousel header, 70/30 split)",
               style=STYLE, script=SCRIPT)


if __name__ == "__main__":
    main()
