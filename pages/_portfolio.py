#!/usr/bin/env python3
"""Generate the portfolio pages from the Figma section "24 sept"
(file HRSMFFccdLgqf1YwD7oyc9, node 4:145).

    portfolio.html              <- Active Holdings (4:146) + Future Repayment (4:5329)
    portfolio-matured.html      <- Matured/Closed bonds (4:697)
    portfolio-no-kyc.html       <- No KYC, no holding (4:2731)
    portfolio-no-holdings.html  <- After KYC, no holding (4:2282)
    portfolio-bond.html         <- Future Repayment finserv (4:1156)
    portfolio-fd.html           <- Future Repayment Unity Bank (4:1833)

The mobile frames (4:4027 ...) set the phone layout, and three frames supply
the sheets: Active / Lifetime investment info (4:6702, 4:6738) and the
investment-figure definitions (4:4015). The achievement strip copy comes from
the two "Texts - Portfolio Amt" frames (4:5959 > zero, 4:6602 = zero).

Every figure, name and date is the design's sample data, not captured from a
live account: each block is marked <!-- DATA: ... --> for the API.

Shell (head, logged-in header, footer, shared scripts) comes from
_user.shell(), so these pages match the user-* pages. Page CSS is
assets/portfolio.css; behaviour is _portfolio.js, inlined.

Run: python3 pages/_portfolio.py
"""
import os

import _user as U

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = "../assets/img/portfolio/"
R = "&#8377;"


def img(name, alt="", w=None, h=None, cls=None):
    return '<img src="%s%s" alt="%s"%s%s%s>' % (
        IMG, name, alt, ' width="%s"' % w if w else "", ' height="%s"' % h if h else "",
        ' class="%s"' % cls if cls else "")


def info_btn(sheet, label, cls="pf-info"):
    return ('<button type="button" class="%s" data-sheet="%s" aria-label="%s">%s</button>'
            % (cls, sheet, label, img("info.svg", w=12, h=12)))


# ------------------------------------------------------------- gold cards

LOGO = ('<span class="pf-gcard__logo">%s%s</span>'
        % (img("card-mark.svg", cls="m"), img("card-wordmark.svg", "GoldenPi", cls="w")))
TAG = '<p class="pf-gcard__tag">Your wealth<br>partner for life</p>'


def gcard(bg, label, body, band=None, sheet=None):
    band_html = ""
    if band:
        band_html = ('        <div class="pf-gcard__band"><span>%s</span>%s</div>\n'
                     % (band, info_btn(sheet, "What %s means" % band.lower()) if sheet else ""))
    return ('      <article class="pf-gcard" aria-label="%s">\n'
            '        %s\n'
            '        <div class="pf-gcard__body">%s%s\n%s        </div>\n%s'
            '      </article>\n') % (label, img(bg, cls="pf-gcard__bg"), LOGO, TAG, body, band_html)


def stats(items):
    cells = "".join(
        '<div><dt>%s%s</dt><dd><span class="r">%s</span>%s</dd></div>'
        % (k, img("info.svg", w=12, h=12) if tip else "", R, v) for k, v, tip in items)
    return '          <dl class="pf-gcard__stats">%s</dl>\n' % cells


def card_active():
    return gcard("card-active.jpg", "Active investment", (
        '          <p class="pf-gcard__big"><span class="pf-gcard__amt"><span class="c">%s</span>'
        '<span class="n">25</span><span class="u">Cr</span></span>'
        '<span class="pf-gcard__what">Outstanding</span></p>\n' % R)
        + stats([("Total Invested", "100Cr", False), ("Repaid", "80Cr", True), ("Gains", "5Cr", False)]),
        "Active investment", "sheet-active")


def card_active_zero():
    return gcard("card-active.jpg", "Active investment", (
        '          <p class="pf-gcard__big"><span class="pf-gcard__amt"><span class="c">%s</span>'
        '<span class="n">0</span></span><span class="pf-gcard__what">Current value</span></p>\n'
        '          <p class="pf-gcard__note">No investments yet &mdash; your journey starts here.</p>\n' % R),
        "Active investment", "sheet-active")


def card_lifetime():
    return gcard("card-lifetime.jpg", "Lifetime investment", (
        '          <p class="pf-gcard__big"><span class="pf-gcard__amt pf-gcard__amt--pct">'
        '<span class="n">14.20</span><span class="u">%</span></span>'
        '<span class="pf-gcard__what">YTM earned</span></p>\n')
        + stats([("Total Invested", "120Cr", False), ("Repaid", "90Cr", True), ("Gains", "7Cr", False)]),
        "Lifetime investment", "sheet-lifetime")


def card_member():
    return ('      <article class="pf-gcard" aria-label="Member card">\n'
            '        %s\n'
            '        <div class="pf-gcard__body">%s%s</div>\n'
            '        <p class="pf-gcard__member"><b>Ashish Kashyap</b>'
            '<span>GG169218<br>Member since 2022</span></p>\n'
            '      </article>\n') % (img("card-member.jpg", cls="pf-gcard__bg"), LOGO, TAG)


def dots(n, label):
    return ('    <div class="pf-dots">%s</div>\n'
            % "".join('<button type="button" aria-label="%s %d of %d"></button>' % (label, k + 1, n)
                      for k in range(n)))


def cards(zero=False):
    slides = [card_active_zero() if zero else card_active(), card_lifetime(), card_member()]
    return ('  <!-- DATA: portfolio totals and the member card, sample values from the design. -->\n'
            '  <div class="pf-cards" data-pf-carousel>\n'
            '    <div class="pf-track" tabindex="0" aria-label="Portfolio cards">\n%s    </div>\n%s  </div>\n'
            % ("".join(slides), dots(len(slides), "Card")))


# ----------------------------------------------------- achievement strip

ACH_INVESTED = [
    ("Legendary", "cash.png", "You Received %s60,000 in Interest with us" % R, "You Deserve that Overdue Vacation!"),
    ("Legendary", "strip-podium.png", "Nifty 50 (1Y): 7.9% &middot; Your YTM: 13.88%", "Kudos to Investing like a BOSS!!"),
    ("1.42M Investors", "strip-shield.png", "1.42M Investors &middot; %s4,300 Cr Invested &middot; 8 Years" % R,
     "You&rsquo;re Joining a Real Fixed-Income Community"),
]
ACH_ZERO = [
    ("1.42M Investors", "strip-shield.png", "1.42M Investors &middot; %s4,300 Cr Invested &middot; 8 Years" % R,
     "You&rsquo;re Joining a Real Fixed-Income Community"),
    ("Refer &amp; Grow", "pray.png", "Thanks for Your Continued Trust in us", "Thanks for Your Continued Trust in us"),
]


def strip(items):
    slides = "".join(
        '      <article class="pf-ach"><span class="pf-ach__tag">%s</span>%s'
        '<p class="pf-ach__title">%s</p><p class="pf-ach__sub">%s</p></article>\n'
        % (tag, img(icon, w=50, h=50), title, sub) for tag, icon, title, sub in items)
    return ('  <!-- DATA: achievement messages; the design switches sets when the portfolio is zero. -->\n'
            '  <div class="pf-strip" data-pf-carousel data-auto>\n'
            '    <div class="pf-track" aria-label="Milestones">\n%s    </div>\n%s  </div>\n'
            % (slides, dots(len(items), "Milestone")))


# ------------------------------------------------------------ note cards

def note(icon, title, text, link=None, href=None, ring=False, extra=""):
    icon_html = ('<span class="pf-note__icon pf-note__icon--ring">%s</span>' % img(icon, w=20, h=20)
                 if ring else img(icon, w=44, h=44, cls="pf-note__icon"))
    link_html = ""
    if link:
        arrow = img("arrow.svg", w=16, h=16)
        link_html = ('<a class="pf-link" href="%s">%s %s</a>' % (href, link, arrow) if href
                     else '<button type="button" class="pf-link">%s %s</button>' % (link, arrow))
    return ('  <div class="pf-note">%s<div><p class="pf-note__title">%s</p>%s%s%s</div></div>\n'
            % (icon_html, title, '<p class="pf-note__text">%s</p>' % text if text else "", extra, link_html))


STATEMENT = lambda: note("statement.png", "Need a Portfolio Statement?",
                         "Download a consolidated report of all your holdings and returns.", "Download Report")


# ------------------------------------------------------------ dialogs

def dark_sheet(id_, title, defs):
    body = ""
    for icon, name, text, ytm, formula in defs:
        body += ('      <div class="pf-def"><div class="pf-def__head"><span><span class="pf-def__icon">%s</span>%s</span>%s</div>'
                 '<p>%s</p>%s</div>\n') % (
            img(icon), name, '<span class="pf-ytm">%s</span>' % ytm if ytm else "", text,
            '<div class="pf-def__formula">%s</div>' % formula if formula else "")
    return ('<dialog class="pf-sheet" id="%s" aria-labelledby="%s-t">\n'
            '  <div class="pf-sheet__head"><span class="pf-sheet__handle"></span>'
            '<button type="button" class="pf-sheet__close" data-close aria-label="Close">%s</button></div>\n'
            '  <div class="pf-sheet__body">\n      <h2 id="%s-t" class="sr-only">%s</h2>\n%s  </div>\n</dialog>\n'
            % (id_, id_, img("cross-white.svg"), id_, title, body))


SHEETS = dark_sheet("sheet-active", "Active investment", [
    ("cash.png", "Outstanding Amount",
     "The value of all your active investments. This is the amount you will receive if holding the investments "
     "till maturity. This excludes already sold or matured investments.",
     None, "Outstanding Amount = (Invested + Gains) &minus; Repaid"),
    ("info-invested.png", "Total Invested", "Total amount invested in all your active investments.", None, None),
    ("info-gains.png", "Gains", "Total gains from your active investments, including interest that has been repaid and accrued",
     "10.75% YTM", None),
    ("info-repaid.png", "Repaid", "Total amount repaid to you across all your active investments including both "
     "interest and principal repayment", None, None),
]) + dark_sheet("sheet-lifetime", "Lifetime investment", [
    ("cash.png", "YTM Earned", "The weighted XIRR returns from all your investments which has been matured", None, None),
    ("info-invested.png", "Total Invested", "Total amount invested in all your lifetime investments, including active, "
     "matured, and sold investments.", None, None),
    ("info-gains.png", "Gains", "Total gains from your lifetime investments, including interest that has been repaid and accrued",
     "10.75% YTM", None),
    ("info-repaid.png", "Repaid", "Total amount repaid to you across all your lifetime investments, including matured "
     "and sold investments.", None, None),
])

# The design titles this sheet "Sample UI >> actual text in right", a note to
# the developer; it explains the Investment Details panel, so it takes that name.
SHEET_DETAILS = (
    '<dialog class="pf-sheet pf-sheet--light" id="sheet-details" aria-labelledby="sheet-details-t">\n'
    '  <div class="pf-sheet__head"><span class="pf-sheet__handle"></span>'
    '<button type="button" class="pf-sheet__close" data-close aria-label="Close">%s</button></div>\n'
    '  <div class="pf-sheet__body">\n'
    '    <h2 id="sheet-details-t">Investment Details</h2>\n'
    '    <!-- DATA: the amounts in brackets are this holding\'s. -->\n'
    '    <dl>\n'
    '      <div><dt>Invested Amount (%s2,50,000)</dt><dd>The total amount you have invested in this product.</dd></div>\n'
    '      <div><dt>Current Value (%s2,60,000)</dt><dd>The current worth of your active investment. Calculation:<br>'
    'Current Value = (Invested Amount &minus; Amount Repaid) + Accrued Gains</dd></div>\n'
    '      <div><dt>Total Returns (%s3,00,000)</dt><dd>The total amount you will receive from this investment by the time it matures.</dd></div>\n'
    '      <div><dt>Repaid Till Date (%s28,000)</dt><dd>The amount already repaid and credited to your bank account.</dd></div>\n'
    '    </dl>\n  </div>\n</dialog>\n') % (img("cross-dark.svg"), R, R, R, R)


# ------------------------------------------------------------- pieces

def crumb(current="Portfolio", parent=None):
    mid = '        <a href="%s">Portfolio</a>\n        <span aria-hidden="true">&rsaquo;</span>\n' % parent if parent else ""
    return ('      <nav class="gp-crumb" aria-label="Breadcrumb">\n'
            '        <a href="user-explore.html">Home</a>\n        <span aria-hidden="true">&rsaquo;</span>\n'
            '%s        <span aria-current="page">%s</span>\n      </nav>\n' % (mid, current))


def titlerow(status):
    return ('  <div class="pf-titlerow"><h1 class="pf-title">Portfolio Metrics</h1>'
            '<span class="pf-status">%s</span></div>\n' % status)


USER = ('  <!-- DATA: account holder; the chevron opens the family-account switcher. -->\n'
        '  <button type="button" class="pf-user" aria-haspopup="true">%s<strong>Rohit Sharma</strong>%s</button>\n'
        % (img("avatar.png", w=44, h=44), img("chevron-down.svg", w=20, h=20)))


def tablist(cls, id_, labels, label, selected=0, ink=False):
    tabs = "".join(
        '<button type="button" role="tab" id="%s-t%d" aria-controls="%s-p%d" aria-selected="%s"%s>%s</button>'
        % (id_, k, id_, k, "true" if k == selected else "false", "" if k == selected else ' tabindex="-1"', t)
        for k, t in enumerate(labels))
    return ('  <div class="%s" role="tablist" aria-label="%s" data-pf-tabs>%s%s</div>\n'
            % (cls, label, '<span class="pf-seg__ink" aria-hidden="true"></span>' if ink else "", tabs))


def panel(id_, k, inner, selected=0):
    return ('  <div role="tabpanel" id="%s-p%d" aria-labelledby="%s-t%d" class="pf-stack%s"%s>\n%s  </div>\n'
            % (id_, k, id_, k, " is-on" if k == selected else "", "" if k == selected else " hidden", inner))


def kv(title, items, cls="", title_cls="", after_title=""):
    cells = "".join('<div><dt>%s</dt><dd%s>%s</dd></div>' % (k, ' class="pf-gain"' if g else "", v)
                    for k, v, g in items)
    return ('  <section class="pf-panel">\n    <h2 class="pf-panel__title%s">%s%s</h2>\n'
            '    <dl class="pf-kv%s">%s</dl>\n  </section>\n' % (title_cls, title, after_title, cls, cells))


def table(caption, heads, rows, hide=()):
    """rows: list of lists of (html, label, cls). First cell is the row's name."""
    th = "".join('<th scope="col"%s>%s</th>' % (' class="pf-hide-sm"' if k in hide else "", h)
                 for k, h in enumerate(heads))
    body = ""
    for r in rows:
        tds = ""
        for k, (html, cls) in enumerate(r):
            classes = " ".join(c for c in (cls, "pf-hide-sm" if k in hide else "") if c)
            tds += '<td data-label="%s"%s>%s</td>' % (heads[k], ' class="%s"' % classes if classes else "", html)
        body += "        <tr>%s</tr>\n" % tds
    return ('  <div class="pf-tablecard">\n    <table class="pf-table">\n      <caption class="sr-only">%s</caption>\n'
            '      <thead><tr>%s</tr></thead>\n      <tbody>\n%s      </tbody>\n    </table>\n  </div>\n'
            % (caption, th, body))


CHEV = '<span class="pf-chev" aria-hidden="true">%s</span>' % img("chevron-down.svg", w=14, h=14)


def name_link(name, href):
    return '<a href="%s">%s</a>%s' % (href, name, CHEV)


def date(d, y):
    return '<span class="pf-date"><b>%s</b> <span>&lsquo;%s</span></span>' % (d, y)


# -------------------------------------------------------------- pages

def page_portfolio():
    holdings = [("Kotak Mahindra Prime Limited", "2,60,000", "60,000", "2,10,000", "19 Jun", "26"),
                ("Poonawalla Fincorp Limited", "2,60,000", "60,000", "2,10,000", "19 Jun", "26"),
                ("Kotak Mahindra Prime Limited", "2,60,000", "60,000", "2,10,000", "19 Jun", "26")]
    hold_rows = [[(name_link(n, "portfolio-bond.html"), "pf-name"), (R + a, ""), (R + b, "pf-up"),
                  (R + c, ""), (date(d, y), "pf-soft")] for n, a, b, c, d, y in holdings]
    holdings_panel = (
        "  <!-- DATA: active bond holdings. Rows open the holding; the design has one bond detail page. -->\n"
        + kv("Active Investment", [("Total Invested", R + "100 Cr", False), ("Repaid", R + "80 Cr", False),
                                   ("Outstanding", R + "25 Cr", False), ("Gains", R + "5 Cr", False),
                                   ("Returns (XIRR)", "14.8%", True)])
        + table("Active bond holdings", ["Name", "Invested", "Repaid", "Outstanding", "Maturity"], hold_rows, hide=(4,)))

    payouts = [("08 Jun", "26", "Bajaj Finance Bond", "5,000", "Interest"),
               ("20 Jun", "26", "Shriram Finance NCD", "5,000", "Interest"),
               ("08 Jun", "26", "Keertana Finance", "4,800", "Principal + Interest"),
               ("22 Jul", "26", "Navi Finserv", "5,150", "Principal + Interest")]
    pay_rows = [[(date(d, y), "pf-name"), (n, "pf-soft"), (R + a, ""), (t, "pf-soft")] for d, y, n, a, t in payouts]
    chips = "".join('<button type="button" aria-pressed="%s">%s</button>' % ("true" if k == 1 else "false", c)
                    for k, c in enumerate(["This Month", "This Quarter", "This Financial Year", "Next Financial Year"]))
    future_panel = (
        '  <div class="pf-filters">\n    <div class="pf-chips" aria-label="Period">%s</div>\n'
        '    <button type="button" class="pf-switch" role="switch" aria-checked="false">'
        '<span class="pf-switch__track"></span>TDS Breakdown</button>\n  </div>\n' % chips
        + "  <!-- DATA: payouts in the selected period. -->\n"
        + kv("Repayment Summary", [("Upcoming Payouts", "4", False), ("Total Cashflow", R + "19,950", False),
                                   ("Interest Expected", R + "10,950", False), ("Principal Repayment", R + "9,000", False)],
             cls=" pf-kv--sub pf-kv--ink")
        + table("Upcoming bond payouts", ["Dates", "Name", "Payout Amount", "Payout Type"], pay_rows))

    fd_rows = [[(name_link("Unity Bank", "portfolio-fd.html"), "pf-name"), (R + "2,50,000", ""), (R + "28,000", "pf-up"),
                (R + "30,000", ""), ('<span class="pf-date"><b>15 Mar</b> <span>2027</span></span>', "pf-soft")]]
    fd_panel = ("  <!-- DATA: FD holdings; the row repeats the Unity Bank holding's own figures. -->\n"
                + table("Fixed deposit holdings", ["Name", "Invested", "Repaid", "Outstanding", "Maturity"], fd_rows, hide=(4,)))
    sip_panel = ('  <div class="pf-empty">%s<h2>No holdings yet</h2></div>\n' % img("briefcase.svg", w=60, h=60))

    bonds = (tablist("pf-seg", "view", ["Holdings", "Future Repayment"], "Bond view", ink=True)
             + panel("view", 0, holdings_panel) + panel("view", 1, future_panel))
    main = (titlerow("Invested") + USER
            + tablist("pf-assets", "asset", ["Bonds", "FD", "SIP"], "Asset type")
            + panel("asset", 0, bonds) + panel("asset", 1, fd_panel) + panel("asset", 2, sip_panel))
    hero = cards() + strip(ACH_INVESTED)
    side = (STATEMENT()
            + note("moneybag.png", "Explore your Matured Investments", R + "3,40,046 from your matured investment",
                   "View past Investments", "portfolio-matured.html")
            + note("check-green.svg", "You Received %s50,000 in Interest" % R,
                   "Credited directly to your linked bank account. You deserve that overdue vacation.", ring=True))
    return layout(main, hero, side) + SHEETS


SIMILAR = [("Akara Capital",), ("Midland Microfin",), ("Lucina Development",)]


def similar():
    cards_html = "".join(
        '  <article class="pf-sim">\n'
        '    <div class="pf-sim__top"><div><h3 class="pf-sim__name">%s</h3>'
        '<div class="pf-sim__tags"><span>High-Yield</span><span>Bond Utsav</span><span>Gold Backed</span></div></div>'
        '<div><p class="pf-sim__rate">13.29<small>%%</small></p><p class="pf-sim__sold">87%% Sold</p></div></div>\n'
        '    <dl><div><dt>Tenure</dt><dd>3Y 1M</dd></div><div><dt>Payout</dt><dd>Monthly</dd></div>'
        '<div><dt>Rating</dt><dd>+AA</dd></div></dl>\n'
        '    <p class="pf-sim__foot">&#9889; Act now &mdash; 3 left, 100%% sold out soon.</p>\n'
        '  </article>\n' % n for (n,) in SIMILAR)
    return ('  <!-- DATA: recommended bonds; sample cards from the design, not live listings. -->\n'
            '  <section class="pf-similar"><h2>Similar bonds to Invest</h2>\n%s  </section>\n' % cards_html)


def page_matured():
    rows = [("Kotak Mahindra Prime Limited", "Matured"), ("Poonawalla Fincorp Limited", "Matured"),
            ("Kotak Mahindra Prime Limited", "Sold")]
    trs = [[('%s<br><span class="pf-tag">%s</span>' % (n, s), "pf-name"), ("19 Jun &lsquo;26", "pf-soft"),
            (R + "4.00L", "pf-soft"), (R + "2,60,000", ""), ("14.8%", "pf-soft")] for n, s in rows]
    main = (titlerow("Matured") + USER
            + tablist("pf-assets", "asset", ["Bonds", "FD", "SIP"], "Asset type")
            + panel("asset", 0, "  <!-- DATA: matured and sold bond holdings. -->\n"
                    + kv("Matured/Sold Investment", [("Returns (XIRR)", "14.8%", True), ("Invested", R + "5.0L", False),
                                                     ("Amount Received", R + "28,000", False), ("Gains", R + "30,000", False)])
                    + table("Matured and sold bonds", ["Name", "Date", "Amount Received", "Invested", "Returns"], trs))
            + panel("asset", 1, '  <div class="pf-empty">%s<h2>No holdings yet</h2></div>\n' % img("briefcase.svg", w=60, h=60))
            + panel("asset", 2, '  <div class="pf-empty">%s<h2>No holdings yet</h2></div>\n' % img("briefcase.svg", w=60, h=60)))
    hero = note("bond-cert.png", "Explore your current Holding", "you&rsquo;ve received %s3,40,046 from them" % R,
                "Active Portfolio", "portfolio.html")
    return layout(main, hero, similar(), crumbs=crumb("Matured", "portfolio.html"))


TRUST = [("trust-zero-default.png", "Zero Defaults"), ("trust-sebi.png", "Sebi Registered"),
         ("five-percent.png", "Curated Bonds"), ("trust-users.png", "16 Lacs+ Users"), ("5500cr.png", "Total Transaction")]


def trust():
    items = "".join('<li><img src="%s" alt="" height="40">%s</li>'
                    % ("../assets/img/" + i if i.startswith("trust-") else IMG + i, t) for i, t in TRUST)
    return ('  <section class="pf-stack" style="gap:14px">\n    <h2 class="pf-ruled">The Golden Experience Of Investing</h2>\n'
            '    <ul class="pf-trust" role="list">%s</ul>\n  </section>\n' % items)


def empty_side(extra_first=False):
    video = ('  <div class="pf-note"><button type="button" class="pf-play" aria-label="Play the explainer">%s</button>'
             '<div><p class="pf-note__title">How bond investments work?</p>'
             '<p class="pf-note__text">Watch a 2- minute explainer on bond return &amp; payout</p></div></div>\n'
             % img("play.svg"))
    opts = [("medal.png", "Highly Rated"), ("calendar.png", "Regular income"), ("cash.png", "Regular income"),
            ("podium.png", "High Returns")]
    purpose = ('  <section class="pf-purpose"><h2>What is the purpose of your investment?</h2><div>%s</div></section>\n'
               % "".join('<button type="button">%s%s</button>' % (img(i, w=20, h=20), t) for i, t in opts))
    refer = ('  <section class="pf-refer"><div><h2>Refer &amp; Earn %s</h2><p>get rewarded with<br>offers and discounts</p></div>'
             '<a class="gp-cta gp-cta--secondary" href="refer-and-earn.html">Refer Now %s</a></section>\n'
             % (img("gift.png", w=24, h=24), img("arrow-up-right.svg", w=12, h=12)))
    return video + (refer + purpose if extra_first else purpose + refer)


def page_no_kyc():
    main = ('  <div><h1 class="pf-lead">Make your First Investment &amp; experience the Golden Standard of Investing</h1>'
            '<p class="pf-lead-sub">Join 1.42M investors who trust GoldenPi for fixed income</p></div>\n'
            '  <div class="pf-empty">%s<h2>No holdings yet</h2>'
            '<p>Complete your KYC. Make your first investment to start tracking your holdings and earnings here.</p>'
            '<button type="button" class="gp-cta gp-cta--primary">Start KYC %s</button></div>\n'
            % (img("briefcase.svg", w=60, h=60), img("arrow.svg", w=16, h=16))
            + '  <section class="pf-stack" style="gap:16px">\n    <h2 class="pf-h2">Complete KYC &amp; start Earning</h2>\n'
            '    <ol class="gp-steps">\n'
            '      <li><p class="gp-steps__num"><span>01</span></p><p class="gp-steps__title">Complete KYC</p>'
            '<p class="gp-steps__desc">Quick digital onboarding with PAN and Aadhaar.</p></li>\n'
            '      <li><p class="gp-steps__num"><span>02</span></p><p class="gp-steps__title">Choose Bond</p>'
            '<p class="gp-steps__desc">Select from our curated list of high-yield bonds</p></li>\n'
            '      <li><p class="gp-steps__num"><span>03</span></p><p class="gp-steps__title">Start Earning</p>'
            '<p class="gp-steps__desc">Receive interest directly in your bank account.</p></li>\n'
            '    </ol>\n  </section>\n'
            + trust())
    return layout(main, cards(zero=True) + strip(ACH_ZERO), empty_side()) + SHEETS


def page_no_holdings():
    main = ('  <div><h1 class="pf-lead">Explore curated bonds and fixed-income opportunities designed to help your money grow steadily</h1>'
            '<p class="pf-lead-sub">Join 1.42 million+ investors building wealth with trusted fixed-income investments.</p></div>\n'
            '  <div class="pf-empty">%s<h2>No holdings yet</h2>'
            '<p>Your KYC is complete. Make your first investment to start tracking your holdings and earnings here.</p>'
            '<a class="gp-cta gp-cta--primary" href="user-corporate-bonds.html">Start Investing %s</a></div>\n'
            % (img("briefcase.svg", w=60, h=60), img("arrow.svg", w=16, h=16))
            + trust())
    return layout(main, cards(zero=True) + strip(ACH_ZERO), empty_side(extra_first=True)) + SHEETS


def holder(logo, name, meta, fill=False):
    return ('  <div class="pf-holder"><span class="pf-holder__logo%s">%s</span>'
            '<div><h1>%s</h1><p class="pf-holder__meta">%s</p></div></div>\n'
            % (" pf-holder__logo--fill" if fill else "", img(logo, "%s logo" % name), name, meta))


DETAILS_INFO = info_btn("sheet-details", "What these figures mean")


def page_bond():
    inv = ("  <!-- DATA: this holding's figures. -->\n"
           + kv("Investment Details", [("Invested", R + "2,50,000", False), ("Repaid Till Date", R + "28,000", False),
                                        ("Outstanding", R + "30,000", False), ("Expected Gains", R + "10,000 (14.2%)", False)],
                cls=" pf-kv--ink", title_cls=" pf-panel__title--ink", after_title=DETAILS_INFO))
    bond = kv("Bond Details", [("Total Units", "200", False), ("ISIN", "INE001A07QN4", False),
                               ("Maturity Date", "15 Mar 2027", False), ("Interest Payout", "Monthly", False),
                               ("Coupon", "11.2%", False)], cls=" pf-kv--ink", title_cls=" pf-panel__title--ink")
    fut = [("15 Jan 25", "&#8377;6,750", "Interest"), ("19 March26", "&#8377;6,750", "Interest"),
           ("15 Jan 25", "&#8377;6,750", "Interest + Principal"), ("19 March26", "2,50,000", "Maturity")]
    fut_rows = [[(d, "pf-name"), (a, ""), (t, "pf-soft")] for d, a, t in fut]
    tx = [[('15 Jan 25<br><span class="pf-tag pf-tag--buy">Buy</span>', "pf-name"), (R + "6,750", ""), ("+120", "pf-soft"), ("14.2%", "pf-soft")],
          [('19 Mar 26<br><span class="pf-tag">Sold</span>', "pf-name"), (R + "6,750", ""), ("-80", "pf-soft"), ("13.8%", "pf-soft")]]
    main = (holder("navi-logo.png", "Navi Finserv", "Senior &middot; Secured &middot; Listed<br>A+ Rated")
            + inv + bond
            + '  <div class="pf-filters"><h2 class="pf-h2">Future Repayment</h2>'
            '<button type="button" class="pf-switch" role="switch" aria-checked="true"><span class="pf-switch__track"></span>TDS</button></div>\n'
            + "  <!-- DATA: this holding's payout schedule. -->\n"
            + table("Future repayments", ["Date", "Payout Amount", "Payout Type"], fut_rows)
            + '  <h2 class="pf-h2">Transaction Summary</h2>\n'
            + table("Transactions", ["Date", "Amount", "Units", "Yield"], tx))
    stat = ('  <!-- DATA: issuer track record. -->\n'
            '  <div class="pf-stats">'
            '<div>%s<b>Zero</b><span>Defaults Ever</span></div>'
            '<div>%s<b>100%%</b><span>Repayments</span></div>'
            '<div>%s<b>%s910 Cr</b><span>Repaid</span></div>'
            '<div>%s<b>1,932+</b><span>To Investors</span></div></div>\n'
            % ('<img src="../assets/img/trust-zero-default.png" alt="" width="40" height="40">', img("hundred.png", w=40, h=40),
               img("rupee-coin.png", w=40, h=40), R, img("cash.png", w=40, h=40)))
    side_top = (stat
                + note("bond-scroll.png", "Bond Cashflow", "Check your all interest and principal payout timeline", "Download Cashflow")
                + note("form121.png", 'Form 121 <span class="pf-badge-ok">Submitted</span>',
                       "Interest payouts without TDS, subject to eligibility &amp; approval.")
                + note("moneybag.png", "Looking to sell your bond?",
                       "Initiate a sell request, and we&rsquo;ll help connect you with interested buyers.", "Proceed to sell"))
    return layout(main, side_top, similar(), crumbs=crumb("Navi Finserv", "portfolio.html"), detail=True) + SHEET_DETAILS


def page_fd():
    inv = ("  <!-- DATA: this deposit's figures. -->\n"
           + kv("Investment Details", [("Invested", R + "2,50,000", False), ("Repaid Till Date", R + "28,000", False),
                                        ("Outstanding", R + "30,000", False), ("Total Interest", R + "10,000 (9.2%)", False)],
                cls=" pf-kv--ink", title_cls=" pf-panel__title--ink", after_title=DETAILS_INFO)
           + kv("Transaction Details", [("Invested On", "15 Jun 2023", False), ("Maturity On", "15 Mar 2027", False),
                                         ("Interest", "11.2%", False), ("Payout", "Yearly", False)],
                cls=" pf-kv--ink", title_cls=" pf-panel__title--ink"))
    rep = [("15 Jan 25", "Interest"), ("19 March26", "Interest"), ("15 Jan 25", "Interest"), ("19 March26", "Interest + Principal")]
    rows = [[(d, "pf-name"), (R + "6,750", ""), (t, "pf-soft")] for d, t in rep]
    main = (holder("unity-logo.png", "Unity Bank", "DICGC Insured upto %s5L" % R, fill=True)
            + inv + '  <h2 class="pf-h2">Repayment</h2>\n'
            + "  <!-- DATA: this deposit's payout schedule. -->\n"
            + table("Repayments", ["Dates", "Payout Amount", "Payout Type"], rows))
    manage = note("bank.png", "Manage Your FD", None, "Proceed", extra=(
        '<ul class="pf-note__list"><li>Early withdrawals</li><li>View FD receipt</li>'
        '<li>Nominee update</li><li>Bank account updates</li></ul>'))
    return layout(main, manage, "", crumbs=crumb("Unity Bank", "portfolio.html"), detail=True) + SHEET_DETAILS


def layout(main, hero, side, crumbs=None, detail=False):
    return ('  <section class="gp-shell pf">\n%s'
            '    <div class="pf-grid%s">\n'
            '<div class="pf-main">\n%s</div>\n'
            '<aside class="pf-hero" aria-label="Portfolio summary">\n%s</aside>\n'
            '<aside class="pf-side" aria-label="More for you">\n%s</aside>\n'
            '    </div>\n  </section>\n'
            % (crumbs or crumb(), " pf-grid--detail" if detail else "", main, hero, side))


PAGES = [
    ("portfolio.html", "Portfolio", page_portfolio),
    ("portfolio-matured.html", "Matured Investments", page_matured),
    ("portfolio-no-kyc.html", "Portfolio", page_no_kyc),
    ("portfolio-no-holdings.html", "Portfolio", page_no_holdings),
    ("portfolio-bond.html", "Navi Finserv", page_bond),
    ("portfolio-fd.html", "Unity Bank FD", page_fd),
]

DESC = "Track your bond and fixed deposit holdings, repayments and returns on GoldenPi."


def main():
    js = open(os.path.join(HERE, "_portfolio.js"), encoding="utf-8").read()
    for out, title, build in PAGES:
        top, bottom = U.shell("%s | GoldenPi" % title, DESC, None)
        top = top.replace('<link rel="stylesheet" href="../assets/user.css">',
                          '<link rel="stylesheet" href="../assets/user.css">\n'
                          '<link rel="stylesheet" href="../assets/portfolio.css">', 1)
        top = top.replace("generated by pages/_user.py from the goldenpi.com capture of 2026-09-26",
                          "generated by pages/_portfolio.py from the Figma section 24 sept (node 4:145)", 1)
        bottom = bottom.replace("</body>", "<script>\n%s</script>\n</body>" % js, 1)
        page = top + "\n" + build() + bottom
        with open(os.path.join(HERE, out), "w", encoding="utf-8") as f:
            f.write(page)
        print("%-28s %6d bytes" % (out, len(page)))


if __name__ == "__main__":
    main()
