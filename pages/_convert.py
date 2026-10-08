#!/usr/bin/env python3
"""Convert the remaining landing pages to the corporate-bonds styling.

Reads the frozen -old archives and writes index.html, fixed-deposits.html and
bond-ipo-online.html. corporate-bonds.html is not handled here: it has its own
generator, pages/_final.py.

What "converted" means, matching what was done to corporate-bonds:
  1. load assets/final.css on top of site.css, changing no other stylesheet
  2. the category tab row becomes a real tablist with a sliding indicator, and
     the heading that repeated the active tab is removed
  3. collections move from three equal columns to an asymmetric bento
  4. reviews move from a horizontal scroller to a grid
  5. duplicate column labels at desktop disappear (handled by final.css)

Tab rows draw on data captured 2026-09-25. Nothing is invented; a tab with no
captured match says so rather than showing fabricated rows.

Run: python3 pages/_convert.py
"""
import os
import re
import sys

import _final as F

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = F.BASE

# Fixed deposit issuers, from the comparison table captured on /fixed-deposits.
# name, logo, highest returns, payout, insured, new account needed, href
FD = {
    "unity": ("UNITY SMALL FINANCE BANK", "GPID105192.Unity.png", "4.00-8.50%",
              "Cumulative, Monthly, Quarterly", "Yes", "No",
              "/fixed-deposits/GPID105192/unity-small-finance-bank?src=view_details"),
    "suryoday": ("SURYODAY SMALL FINANCE BANK", "GPID105191.Suryoday.png", "4.00-8.50%",
                 "Cumulative", "Yes", "No",
                 "/fixed-deposits/GPID105191/suryoday-bank?src=view_details"),
    "utkarsh": ("UTKARSH SMALL FINANCE BANK", "GPID106947.utkarsh_logo.png", "4.00-8.25%",
                "Cumulative", "Yes", "No",
                "/fixed-deposits/GPID106947/utkarsh-small-finance-bank?src=view_details"),
    "shriram": ("SHRIRAM FINANCE", "GPID100016.Shriram-Squircle.png", "6.64-8.05%",
                "Cumulative, Monthly, Quarterly, Half-Yearly, Yearly", "No", "No",
                "/fixed-deposits/GPID100016/shriram-finance-limited?src=view_details"),
    "mahindra": ("MAHINDRA FINANCE", "GPID105193.Mahindra-Squircle.png", "6.40-7.80%",
                 "Cumulative, Monthly, Quarterly, Half-Yearly, Yearly", "No", "No",
                 "/fixed-deposits/GPID105193/mahindra-finance?src=view_details"),
    "bajaj": ("BAJAJ FINANCE LTD", "GPID100379.Bajaj-Finserv.png", "6.41-7.75%",
              "Cumulative, Monthly, Quarterly, Half-Yearly, Yearly", "No", "No",
              "/fixed-deposits/GPID100379/baja-finance-limited-co?src=view_details"),
}


# The listing tab's FD rows, from the user's screenshot of the live FD list
# (2026-09-26): highest returns, secured, tenure. Name, logo and link come
# from FD above.
FD_TAB = {
    "unity": ("8.5%", "Insured upto &#8377;5L", "7 days-60 months"),
    "suryoday": ("8.5%", "Insured upto &#8377;5L", "7 days-60 months"),
}


def fd_row(key, i):
    name, logo, _, _, _, _, href = FD[key]
    ret, secured, tenure = FD_TAB[key]
    return (
        '            <article class="gp-row" style="--r:%d">\n'
        '              <div class="gp-row__identity">\n'
        '                <img class="gp-row__logo" src="../assets/img/%s" alt="">\n'
        '                <a class="gp-row__name gp-row__link" href="%s%s">%s</a>\n'
        '              </div>\n'
        '              <div><div class="gp-row__label">Highest Returns</div>'
        '<div class="gp-row__value gp-row__value--returns">%s</div></div>\n'
        '              <div><div class="gp-row__label">Secured</div>'
        '<div class="gp-row__value gp-row__value--secured">%s</div></div>\n'
        '              <div><div class="gp-row__label">Tenure</div>'
        '<div class="gp-row__value">%s</div></div>\n'
        '              <div></div>\n'
        '              <div class="gp-row__actions">\n'
        '                <button type="button" title="Share"><img src="../assets/img/golden-share.svg" alt="Share"></button>\n'
        '              </div>\n'
        '            </article>' % (i, logo, BASE, href.replace("&", "&amp;"),
                                    name, ret, secured, tenure))


CREAM_OPEN = '      <div class="rounded-2xl border border-[#f0e6c8] bg-[#fdf8e9] p-4 sm:p-6">'
CREAM_CLOSE = '      </div>'


def cream(inner):
    """Wrap a block in the cream panel corporate-bonds uses for its listing."""
    return "%s\n%s\n%s" % (CREAM_OPEN, inner, CREAM_CLOSE)


def tabstrip(tabs):
    """tabs: list of dicts with id, label, icon, head (5 column names), body."""
    buttons, panels = [], []
    for k, t in enumerate(tabs):
        sel = "true" if k == 0 else "false"
        buttons.append(
            '            <button type="button" class="gp-tab" role="tab" id="tab-%s"\n'
            '                    aria-controls="panel-%s" aria-selected="%s"%s>\n'
            '              <img src="../assets/img/%s" alt="">%s\n'
            '            </button>' % (
                t["id"], t["id"], sel, "" if k == 0 else ' tabindex="-1"', t["icon"], t["label"]))
        panels.append(
            '        <div class="gp-panel%s" id="panel-%s"\n'
            '             role="tabpanel" aria-labelledby="tab-%s"%s>\n%s\n        </div>' % (
                " is-on" if k == 0 else "", t["id"], t["id"],
                "" if k == 0 else " hidden", t["body"]))

    return ('        <div class="gp-tabs mb-6">\n'
            '          <div class="gp-tabs__track" role="tablist" aria-label="%s">\n'
            '            <span class="gp-tabs__ink" aria-hidden="true"></span>\n'
            '%s\n'
            '          </div>\n'
            '        </div>\n\n%s' % ("Categories", "\n\n".join(buttons), "\n\n".join(panels)))


def listing_body(rows_html, head, more_label, more_href):
    return (
        '          <div class="gp-rows__head">\n'
        '            <span></span><span>%s</span><span>%s</span>\n'
        '            <span>%s</span><span>%s</span><span></span>\n'
        '          </div>\n\n'
        '          <div class="gp-rows">\n%s\n          </div>\n\n'
        '          <div class="mt-5 text-center">\n'
        '            <a class="t-small font-bold t-bronze underline" href="%s%s">%s</a>\n'
        '          </div>' % (head[0], head[1], head[2], head[3],
                              rows_html, BASE, more_href, more_label))


MAIN = ['index', 'corporate-bonds', 'fixed-deposits', 'bond-ipo-online']


def hero_ground(html):
    """Give the hero the shared warm wash.

    corporate-bonds wrapped its hero in a section carrying the gradient;
    fixed-deposits and bond-ipo-online opened straight onto .gp-shell, so they
    sat flat on the page background and the set did not read as one design.
    """
    open_tag = '<section class="gp-shell pt-6 pb-2">'
    if open_tag not in html:
        sys.exit('hero section not found')
    i = html.index(open_tag)
    close = html.index('  </section>', i)
    inner = html[i + len(open_tag):close]
    return (html[:i]
            + '<section class="gp-hero">\n    <div class="gp-shell pt-6 pb-2">'
            + inner.rstrip() + '\n    </div>\n'
            + html[close:])


def count_up(html):
    """Milestone figures count up on first view, as on corporate-bonds."""
    return html.replace('<dt class="t-h1 t-gold">', '<dt class="t-h1 t-gold" data-count>')



# ---------------------------------------------------------- issuer design system
# Components lifted from /issuers/akara-capital-advisors-private-limited, which
# is a from-scratch page on the new site and so the reference for new work.

def issuer_ctas(html):
    """Swap the flat gold pill for the gradient CTA the issuer page uses."""
    html = html.replace('class="gp-btn gp-btn--primary gp-btn--sm',
                        'class="gp-cta gp-cta--primary gp-cta--sm')
    html = html.replace('class="gp-btn gp-btn--primary', 'class="gp-cta gp-cta--primary')
    html = html.replace('class="gp-btn gp-btn--ghost', 'class="gp-cta gp-cta--secondary')
    return html


def common(html, slug):
    """Steps every converted page gets."""
    # The -old archives were repointed at each other before this ran, so the
    # source carries archive links. Send them back to the live pages: a live
    # page must never navigate into the frozen set.
    for m in MAIN:
        html = html.replace('href="%s-old.html"' % m, 'href="%s.html"' % m)

    html = html.replace('<link rel="stylesheet" href="../assets/site.css">',
                        '<link rel="stylesheet" href="../assets/site.css">\n'
                        '<link rel="stylesheet" href="../assets/final.css">', 1)
    html = html.replace('</title>',
        '</title>\n<!-- Converted 2026-09-26 to match corporate-bonds.html: additive\n'
        '     assets/final.css only, same stack, same gp-* components. The page as\n'
        '     it stood before is archived at %s-old.html.\n'
        '     Generated by pages/_convert.py. -->' % slug, 1)
    # Reviews: scroller becomes a grid, as on corporate-bonds.
    for heading in ('Why 15 Lakh+ Users Trust GoldenPi for Bond Investing',
                    'Why 15 Lakh+ Users Trust GoldenPi', 'Happy users'):
        needle = '<h2 class="gp-section__title">%s</h2>' % heading
        if needle in html:
            i = html.index('<div class="gp-scroller">', html.index(needle))
            html = (html[:i] + '<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">'
                    + html[i + len('<div class="gp-scroller">'):])
            break
    return F.review_marquee(F.blog_cards(html))


def collections(html, after=None, title="Explore Corporate Bond Collections"):
    """The shared five-card collections bento: swapped in where the page has
    its own collections section, otherwise added after the section holding `after`."""
    if F.MARK in html:
        i = html.index(F.MARK)
        j = html.index("  </section>\n", i) + len("  </section>\n")
    else:
        i = j = html.index("  </section>\n", html.index(after)) + len("  </section>\n")
        html = html[:i] + "\n" + html[i:]
        i = j = i + 1
    return html[:i] + F.collections(title) + html[j:]


def scripts(html, tabs=True):
    """Add the shared behaviour before </body>.

    The archived pages carry data-reveal markup but never had the script that
    drives it, so the reveal is added here as well. Both scripts are additive:
    without them the page still renders complete and visible.
    """
    parts = []
    if tabs:
        parts.append(open(os.path.join(HERE, "_tabs.js"), encoding="utf-8").read())
    parts.append(open(os.path.join(HERE, "_reveal.js"), encoding="utf-8").read())
    block = "\n\n".join("<script>\n%s</script>" % p for p in parts)
    if "</body>" not in html:
        sys.exit("no </body> to insert before")
    return html.replace("</body>", "%s\n\n</body>" % block, 1)


# ---------------------------------------------------------------------- index

def home_tabs():
    """The homepage's six category tabs; user-explore reuses them."""
    rows = lambda rs, c4, c5: "\n\n".join(
        F.row_html(r, i, c4, c5) for i, r in enumerate(rs))

    tabs = [
        dict(id="utsav", label="Bond Utsav Deals", icon="pre-login-active-offers.svg",
             body=listing_body(rows([F.AKARA_13, F.NEO, F.BEST, F.AKARA_12], "Payout", "Maturity Date"),
                               ("Returns", "Credit Rating", "Payout", "Maturity Date"),
                               "View All", "/bond-utsav")),
        dict(id="yield", label="11%+ Yield Bonds", icon="pre-login-home-highest-yield.svg",
             body=listing_body(rows([F.AKARA_13, F.NEO, F.BEST, F.AKARA_12], "Payout", "Maturity Date"),
                               ("Returns", "Credit Rating", "Payout", "Maturity Date"),
                               "View all high yield bonds", "/collections/high-yield-bonds")),
        dict(id="thirtyk", label="Bonds at &#8377;30K", icon="pre-login-bonds-at-10k.svg",
             body=listing_body(rows([F.MUTH_CAP], "Min. Investment", "Maturity Date"),
                               ("Returns", "Credit Rating", "Min. Investment", "Maturity Date"),
                               "View bonds under &#8377;10,000", "/collections/bonds-at-10000")),
        dict(id="monthly", label="Bonds for Monthly Income", icon="monthly-bonds.svg",
             body=listing_body(rows([F.AKARA_13, F.BEST, F.AKARA_12], "Payout", "Maturity Date"),
                               ("Returns", "Credit Rating", "Payout", "Maturity Date"),
                               "View all monthly income bonds",
                               "/collections/bonds-to-earn-monthly-fixed-income")),
        dict(id="ipo", label="NCD IPO", icon="pre-login-ncd-ipo.svg",
             body=listing_body(rows([F.EDEL, F.MUTH_IPO], "Status", "Closes On"),
                               ("Returns", "Credit Rating", "Status", "Closes On"),
                               "View all ongoing NCD IPOs", "/collections/best-ongoing-ipos")),
        dict(id="fd", label="Fixed Deposits", icon="cfd-icon.svg",
             body=listing_body("\n\n".join(fd_row(k, i) for i, k in enumerate(FD_TAB)),
                               ("Highest Returns", "Secured", "Tenure", ""),
                               "Compare all fixed deposits", "/fixed-deposits")),
    ]
    return tabs


PARTNERS = [("Sakthi-Finance-logo.png", "Sakthi Finance"), ("centrum.png", "Centrum"),
            ("axis-securities.png", "Axis Securities"), ("anand-rathi.webp", "Anand Rathi")]
# (icon, value, unit, label): the platform milestones.
MILESTONES = [("users.png", "18", "Lac+", "registered users &amp; growing"),
              ("portfolio/info-gains.png", "&#8377;6300", "Cr+", "total transaction through our platform"),
              ("portfolio/cash.png", "&#8377;3000", "Cr+", "worth of bonds available on the platform everyday")]


def home_proof():
    """The heading, milestone cards and partner marquee between the hero and the
    asset tabs. The milestones and the sub-line are from the uatnew message
    bundle (landing.stats.heading and the milestone strings), read 2026-09-30.
    The heading is the user's own wording, given 2026-09-30; it takes the place
    of the "Trusted by leading financial institutions" label over the logos."""
    # The card is a wrapper inside each item: the item staggers in (gp-stagger
    # owns its transition), the card answers the pointer.
    stats = "".join(
        '        <li class="gp-proof__stat"><div class="gp-proof__card">\n'
        '          <span class="gp-proof__icon"><img src="../assets/img/%s" alt="" width="42" height="42"></span>\n'
        '          <div><p class="gp-proof__value"><span class="gp-proof__roll"><span>%s <small>%s</small></span></span></p>'
        '<p class="gp-proof__what">%s</p></div>\n        </div></li>\n' % m for m in MILESTONES)
    # Two sets per half so the strip outruns a wide screen; the second half is
    # the copy that makes the loop seamless.
    logos = "".join('<li><img src="../assets/img/%s" alt="%s" height="30"></li>' % p for p in PARTNERS) * 2
    clones = "".join('<li aria-hidden="true"><img src="../assets/img/%s" alt="" height="30"></li>' % f
                     for f, _ in PARTNERS) * 2
    # gp-proof--band: numbers and logos are one full-width band with a ground of
    # its own, under a centred heading: the figures as columns and the partner
    # logos as its foot. The earlier layout, separate cards above a
    # row of logo chips, is kept at index-proof-cards.html.
    return ('  <!-- ============================================================ proof -->\n'
            '  <section data-reveal class="gp-proof gp-proof--band" aria-labelledby="home-proof-title">\n'
            '  <div class="gp-shell">\n'
            '    <div data-reveal class="gp-proof__head">\n'
            '      <h2 class="gp-proof__title" id="home-proof-title">Trusted by 18 Lac+ users '
            '<span>and leading institutions</span></h2>\n'
            '      <p class="gp-proof__sub">Buy Bonds Online in India - Corporate Bonds, NCD IPOs &amp; Fixed Deposits</p>\n'
            '    </div>\n'
            '    <div data-reveal class="gp-proof__panel">\n'
            '      <!-- DATA: platform milestones. -->\n'
            '      <ul data-reveal class="gp-proof__stats gp-stagger" role="list">\n%s      </ul>\n'
            '      <div class="gp-proof__partners">\n'
            '        <div class="gp-logos"><ul class="gp-logos__track" role="list">%s%s</ul></div>\n'
            '      </div>\n    </div>\n  </div>\n  </section>\n\n' % (stats, logos, clones))


def build_index():
    html = open(os.path.join(HERE, "index-old.html"), encoding="utf-8").read()
    html = common(html, "index")

    # The plain "trusted by" row under the hero goes; the proof section that
    # replaces it sits after the asset tabs, ahead of the webinar.
    start = html.index('  <!-- ========================================================== trusted -->')
    end = html.index('  <!-- ====================================================== asset explorer -->', start)
    html = html[:start] + html[end:]
    # The tabs now follow the hero directly, so they take the section rhythm
    # from final.css instead of the small top padding they had under that row.
    tight = '<section data-reveal class="gp-section pt-4" id="home-assets">'
    assert tight in html
    html = html.replace(tight, '<section data-reveal class="gp-section" id="home-assets">', 1)
    at = html.index('  <!-- =========================================================== webinar -->')
    html = html[:at] + home_proof() + html[at:]

    tabs = home_tabs()

    # Swap the static tab row and the heading beneath it for the real tablist.
    start = html.index('        <div class="gp-scroller !grid-cols-none mb-6"')
    end = html.index('        <div class="mt-5 text-center">', start)
    end = html.index('</div>', html.index('View All</a>', end)) + len('</div>')
    html = html[:start] + tabstrip(tabs) + "\n" + html[end:]

    # Hero stats: three tiles, one row at every width; the Minimum
    # Investment tile was dropped at the user's request (2026-10-01).
    tile = html.index('        <div class="rounded-xl border border-[#4a3f2a] bg-[#241c14]/70 p-4">\n'
                      '          <img src="../assets/img/coin-icon.png"')
    html = html[:tile] + html[html.index('</div>\n', tile) + len('</div>\n'):]
    # From sm the grid keeps its four columns so each tile keeps its old
    # width; the fourth slot stays empty. Phones get the three in one row.
    grid = '<dl class="mt-8 grid max-w-2xl grid-cols-2 gap-3 sm:grid-cols-4">'
    assert grid in html
    html = html.replace(grid, '<dl class="mt-8 grid max-w-2xl grid-cols-3 gap-2 sm:grid-cols-4 sm:gap-3">', 1)

    # The heading's asset rolls through the three products (user request,
    # 2026-10-01). The heading's text stays the live one for screen readers
    # and search; the roller is decoration, and stops on NCD IPOs without motion.
    word = '<span class="text-gold">NCD IPOs</span>'
    assert word in html
    html = html.replace(word, (
        '<span class="sr-only">NCD IPOs</span>'
        '<span class="gp-roll text-gold" aria-hidden="true"><span class="gp-roll__track">'
        '<span>NCD IPOs</span><span>Fixed Deposits</span><span>Corporate Bonds</span><span>NCD IPOs</span>'
        '</span></span>'), 1)
    html = html.replace('<div class="rounded-xl border border-[#4a3f2a] bg-[#241c14]/70 p-4">',
                        '<div class="rounded-xl border border-[#4a3f2a] bg-[#241c14]/70 p-3 sm:p-4">', 3)

    html = collections(html)
    html = F.faq_with_help(html)
    return scripts(html)


# -------------------------------------------------------------- fixed deposits

# Issuer cards as the page already draws them. Returns and badges are the
# issuers' own, captured 2026-09-25: the bank three from the homepage FD
# carousel, the NBFC three from this page.
# key: (name, logo, badge, badge classes, returns, href)
FD_CARDS = {
    "unity": ("UNITY SMALL FINANCE BANK", "GPID105192.Unity.png", "Monthly Payout",
              "bg-[#eaf4fd] text-[#19386d]", "8.50%",
              "/fixed-deposits/GPID105192/unity-small-finance-bank?src=view_details"),
    "suryoday": ("SURYODAY SMALL FINANCE BANK", "GPID105191.Suryoday.png",
                 "Starts Investing with &#8377;1,000", "bg-[#eefaf2] text-gain", "8.50%",
                 "/fixed-deposits/GPID105191/suryoday-bank?src=view_details"),
    "utkarsh": ("UTKARSH SMALL FINANCE BANK", "GPID106947.utkarsh_logo.png",
                "Sr. Citizens get additional benefit", "bg-[#eaf4fd] text-[#19386d]", "8.25%",
                "/fixed-deposits/GPID106947/utkarsh-small-finance-bank?src=view_details"),
    "shriram": ("SHRIRAM FINANCE", "GPID100016.Shriram-Squircle.png",
                "Sr. Citizens get additional benefit", "bg-[#eaf4fd] text-[#19386d]", "8.05%",
                "/fixed-deposits/GPID100016/shriram-finance-limited?src=view_details"),
    "mahindra": ("MAHINDRA FINANCE", "GPID105193.Mahindra-Squircle.png", "AAA Rated",
                 "bg-[#eefaf2] text-gain", "7.80%",
                 "/fixed-deposits/GPID105193/mahindra-finance?src=view_details"),
    "bajaj": ("BAJAJ FINANCE LTD", "GPID100379.Bajaj-Finserv.png", "Instant Booking",
              "bg-[#fdf0e6] text-[#a05a1f]", "7.75%",
              "/fixed-deposits/GPID100379/baja-finance-limited-co?src=view_details"),
}


def fd_card(key):
    name, logo, badge, badge_cls, ret, href = FD_CARDS[key]
    return (
        '            <article class="gp-card gp-card--link overflow-hidden text-center">\n'
        '              <div class="p-6">\n'
        '                <img src="../assets/img/%s" alt="Issuer logo" width="60" height="60" class="mx-auto">\n'
        '                <h3 class="mt-4 t-h4">%s</h3>\n'
        '                <p class="mt-3 inline-block rounded-full %s px-3 py-1 t-caption font-semibold">%s</p>\n'
        '              </div>\n'
        '              <div class="bg-[#fdf8e9] px-6 py-5">\n'
        '                <p class="t-caption t-muted">Returns upto</p>\n'
        '                <p class="t-figure t-bronze">%s</p>\n'
        '                <a class="gp-btn gp-btn--primary gp-btn--sm mt-3" href="%s%s">Know More</a>\n'
        '              </div>\n'
        '            </article>' % (logo, name, badge_cls, badge, ret, BASE,
                                    href.replace("&", "&amp;")))


def fd_panel(keys):
    return ('          <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">\n%s\n          </div>'
            % "\n\n".join(fd_card(k) for k in keys))


# Same structure as the corporate-bonds hero. The eyebrow is this page's own
# "Invest Online in Under 5 Minutes": FDs are not SEBI products, so the
# corporate-bonds eyebrow and trust strip would be wrong here. The rate line
# stays inside the h1, styled as the figure line. The three features sit in one
# row at desktop, stacked on the icon, with sentence-case captions so they fit.
# The h1 first line is the product owner's wording (2026-09-26), not the
# captured "Fixed Deposits Online".
FD_FEATURES = [
    ("gold-shield.svg", "Upto &#8377;5L Secured", "RBI's DICGC Insurance"),
    ("gold-flash.svg", "Instant Withdrawal", "No penalty on early closure"),
    ("cal.svg", "Save Tax", "Under 80C"),
]

FD_HERO = '''<div class="grid gap-8 md:grid-cols-[1.1fr_0.9fr] md:items-center">
      <div data-reveal>
        <p class="gp-eyebrow mb-5">Invest Online in Under 5 Minutes</p>

        <h1 class="t-h1">
          <span class="t-bronze">High Return Fixed Deposits to Invest Online</span>
          <span class="mt-4 block t-h3 text-ink">Earn up to <span class="gp-hero__figure">8.5%% p.a.</span> Interest rate</span>
        </h1>

        <ul class="mt-6 grid gap-3 sm:grid-cols-3 max-w-xl">
%s
        </ul>

        <div class="mt-8 flex flex-wrap items-center gap-4">
          <a class="gp-btn gp-btn--primary" href="#explore-fds">Explore our FD offerings</a>
          <a class="gp-btn gp-btn--ghost" href="corporate-bonds.html">Explore Our Corporate Bonds List</a>
        </div>
      </div>
''' % "\n".join(
    '          <li class="gp-card flex items-center gap-3 px-4 py-3 sm:flex-col sm:items-start sm:gap-2">\n'
    '            <img src="../assets/img/%s" alt="" width="26" height="26">\n'
    '            <span>\n'
    '              <span class="block t-small font-bold">%s</span>\n'
    '              <span class="block t-small t-muted">%s</span>\n'
    '            </span>\n'
    '          </li>' % f for f in FD_FEATURES)


# The locker is goldenpi.com/fixed-deposits' own hero art (post-login-cfd.png,
# its .hero-gif-bg background). Production draws the three chips over it with a
# Lottie; here they are the same cards as before, as real text, placed where
# production puts them. Copy stays the UAT wording.
FD_ART = '''<div class="relative mx-auto w-full max-w-[460px]">
        <img src="../assets/img/post-login-cfd.png" width="587" height="544"
             class="w-full h-auto mix-blend-multiply [mask-image:radial-gradient(closest-side,#000_65%,transparent)]" alt="Money locker with gold coins">
        <ul>
          <li class="gp-card absolute left-0 top-[14%] flex items-center gap-2 px-3 py-2 t-small font-semibold max-w-[75%]">
            <img src="../assets/img/percentage-icon.png" alt="" width="20" height="20">
            Extra Returns for Senior citizens and women
          </li>
          <li class="gp-card absolute right-0 top-[48%] flex items-center gap-2 px-3 py-2 t-small font-semibold">
            <img src="../assets/img/coin-icon.png" alt="" width="20" height="20">
            Starts at &#8377;1,000
          </li>
          <li class="gp-card absolute left-[4%] bottom-[12%] flex items-center gap-2 px-3 py-2 t-small font-semibold">
            <img src="../assets/img/gold-flash.svg" alt="" width="20" height="20">
            Instant Booking
          </li>
        </ul>
      </div>'''


def fd_hero(html):
    """Replace the hero: left column rebuilt, right column becomes the locker art."""
    start = html.index('<div class="grid gap-8 md:grid-cols-[1.1fr_0.9fr] md:items-center">')
    ul = html.index('<ul class="grid gap-3 sm:grid-cols-2', start)
    end = html.index('</ul>', ul) + len('</ul>')
    html = html[:start] + FD_HERO + '\n      ' + FD_ART + html[end:]
    return html.replace('<nav class="t-small t-muted mb-5" aria-label="Breadcrumb">',
                        '<nav class="t-small t-muted mb-6" aria-label="Breadcrumb">', 1)


def build_fd():
    html = open(os.path.join(HERE, "fixed-deposits-old.html"), encoding="utf-8").read()
    html = common(html, "fixed-deposits")

    # Tax saving deposits were not in the captured listing, so that panel says
    # so rather than showing rows that were never there.
    empty = (
        '          <div class="gp-card p-10 text-center">\n'
        '            <p class="t-body t-muted m-0">No tax saving deposits were listed in this\n'
        '              snapshot. On the live platform they appear here under Section 80C.</p>\n'
        '            <p class="mt-4 m-0"><a class="t-small font-bold t-bronze underline"\n'
        '               href="%s/fixed-deposits">See the live fixed deposit list</a></p>\n'
        '          </div>' % BASE)

    tabs = [
        dict(id="bank", label="Bank FD", icon="bank-fd.svg",
             body=fd_panel(["unity", "suryoday", "utkarsh"])),
        dict(id="tax", label="Tax Saving FD", icon="tax-saving-fd.svg", body=empty),
        dict(id="nbfc", label="NBFC FD", icon="nbfc-fd.svg",
             body=fd_panel(["shriram", "mahindra", "bajaj"])),
    ]

    # Replace the static tab row, the feature line under it, and the card grid
    # it was supposed to be filtering.
    start = html.index('      <div class="mb-4 flex flex-wrap justify-center gap-2">')
    anchor = html.index('<!-- DATA: FD issuer list', start)
    end = html.index('</div>\n    </div>\n  </section>', anchor) + len('</div>\n')
    html = html[:start] + cream(tabstrip(tabs)) + "\n" + html[end:]
    html = collections(html, 'role="tablist"')
    html = fd_hero(html)
    html = hero_ground(html)
    html = F.drop_sections(html)
    html = F.golden_experience(html, add=True)
    html = F.faq_with_help(html)
    html = issuer_ctas(html)
    return scripts(html)


# --------------------------------------------------------------- bond ipo page

# Same structure as the corporate-bonds hero: eyebrow, h1, figure line, body,
# two CTAs, trust strip. All copy is captured: the h1 and figure line from the
# hero, the body line from this page's meta description, the ghost CTA label
# from the corporate-bonds hero. The art is square (1226x1220), so it gets its
# real ratio and a smaller cap than corporate-bonds' landscape image.
IPO_HERO = '''<div class="grid gap-8 md:grid-cols-[1.05fr_0.95fr] md:items-center">
        <div data-reveal>
          <p class="gp-eyebrow mb-5">Fixed income &middot; SEBI regulated</p>

          <h1 class="t-h1">
            <span class="t-bronze">Apply NCD IPOs Online</span><br>
            <span class="t-bronze">Latest Bond Issues &amp; Dates</span>
          </h1>

          <p class="mt-4 t-h3">
            Invest as low as &#8377;10k and get returns as high as
            <span class="gp-hero__figure">15%</span>
          </p>

          <p class="mt-4 max-w-md t-body t-muted">
            Explore live NCD IPOs, returns, credit ratings, and apply digitally.
          </p>

          <div class="mt-8 flex flex-wrap items-center gap-4">
            <a class="gp-btn gp-btn--primary" href="#explore-ipos">Start Investing</a>
            <a class="gp-btn gp-btn--ghost" href="corporate-bonds.html">Explore Our Corporate Bonds List</a>
          </div>

          <p class="mt-8 flex items-center gap-2.5 rounded-xl border border-stroke bg-white px-4 py-3 t-small t-muted max-w-lg">
            <img src="../assets/img/ipo-hero-shield-img.png" alt="" width="18" height="18">
            <span>GoldenPi is a
              <a class="font-semibold t-bronze underline" href="https://www.sebi.gov.in/">SEBI registered Debt broker</a>
              and
              <a class="font-semibold t-bronze underline" href="https://www.sebi.gov.in/">OBPP License Holder</a>
            </span>
          </p>
        </div>

        <img src="../assets/img/ipo-hero.png" width="1226" height="1220"
             class="w-full max-w-[420px] h-auto justify-self-center"
             alt="Invest in NCD IPOs online on GoldenPi">
      </div>'''


def ipo_hero(html):
    start = html.index('<div class="grid gap-8 md:grid-cols-[1.05fr_0.95fr] md:items-center">')
    end = html.index('</div>', html.index('alt="Invest in NCD IPOs online on GoldenPi">', start)) + len('</div>')
    html = html[:start] + IPO_HERO + html[end:]
    return html.replace('<nav class="t-small t-muted mb-5" aria-label="Breadcrumb">',
                        '<nav class="t-small t-muted mb-6" aria-label="Breadcrumb">', 1)


def build_ipo():
    html = open(os.path.join(HERE, "bond-ipo-online-old.html"), encoding="utf-8").read()
    html = common(html, "bond-ipo-online")

    # No tabs on this page, but the live IPO listing gets the same cream panel
    # corporate-bonds puts its listing in, so the two pages read as a set.
    start = html.index('      <!-- DATA: live IPO list')
    end = html.index('    </div>\n  </section>', start)
    inner = html[start:end].rstrip()
    html = html[:start] + cream(inner) + "\n" + html[end:]
    html = collections(html, '<!-- DATA: live IPO list')
    html = ipo_hero(html)
    html = hero_ground(html)
    html = count_up(html)
    html = F.faq_with_help(html)
    html = F.drop_sections(html)
    return scripts(html, tabs=True)


def fold_footer(html):
    """Index only: the copyright line becomes a full-width row under the link
    columns, its right edge the toggle for everything after it (documents,
    disclosures, SEO copy), which starts closed."""
    copy = '    <p class="ft-copy">&copy; Copyright 2017 - 2026 | GoldenPi Securities Pvt. Ltd.</p>\n'
    bands = '\n    <nav class="ft-band" aria-labelledby="ft-info"'
    for s in (copy, bands, "\n</footer>"):
        if html.count(s) != 1:
            raise SystemExit("fold_footer: footer markup changed, %r not found once" % s.strip()[:40])
    # Columns: Invest, Company, Legal, then New to GoldenPi with the
    # "Read more about bond investments" links folded into it.
    read = re.search(r'\n\n      <nav class="ft-col" aria-labelledby="ft-read".*?</nav>', html, re.S)
    new = re.search(r'      <nav class="ft-col" aria-labelledby="ft-new".*?(        </ul>)', html, re.S)
    if not (read and new):
        raise SystemExit("fold_footer: footer link columns not found")
    items = "".join(re.findall(r" *<li>.*?</li>\n", read.group(0)))
    html = (html[:new.start()] + F.legal_col(html) + "\n\n" + html[new.start():new.start(1)]
            + items + html[new.start(1):read.start()] + html[read.end():])
    # The Important links chips join the end of Important Information.
    links = re.search(r'\n    <nav class="ft-band" aria-labelledby="ft-links".*?</nav>', html, re.S)
    info = re.search(r'<nav class="ft-band" aria-labelledby="ft-info".*?(\n      </div>\n    </nav>)', html, re.S)
    if not (links and info):
        raise SystemExit("fold_footer: Important links / Important Information bands not found")
    chips = "".join(re.findall(r"\n        <a [^\n]*</a>", links.group(0)))
    html = html[:info.start(1)] + chips + html[info.start(1):links.start()] + html[links.end():]
    # Terms and Privacy now live in the Legal column, so the band drops them.
    for label in ("Terms &amp; Conditions", "Privacy Policy"):
        chip = re.search(r'\n        <a href="[^"]+">%s</a>' % re.escape(label), html)
        if not chip:
            raise SystemExit("fold_footer: %s chip not found" % label)
        html = html[:chip.start()] + html[chip.end():]
    # The registration IDs and compliance contacts leave Risk Disclosure and
    # sit, always visible, under the link columns: plain lines, no cards.
    reg = re.search(r'\n *<dl class="ft-reg">\n(.*?)\n *</dl>((?:\n *<p>.*?</p>){3})', html, re.S)
    if not reg:
        raise SystemExit("fold_footer: registration block not found")
    ids = re.sub(r"(?m)^ *", "        ", reg.group(1))
    paras = re.sub(r"(?m)^ *<p>", "      <p>", reg.group(2))
    html = html[:reg.start()] + html[reg.end():]
    # Contact Us and CIN leave the brand block; CIN joins the IDs after SEBI.
    brand = re.search(r'\n *<p class="ft-brand__tel[^"]*">Contact Us: .*?</p>\n *<p>CIN: ([^<]+)</p>', html)
    if not brand:
        raise SystemExit("fold_footer: brand Contact Us / CIN lines not found")
    html = html[:brand.start()] + html[brand.end():]
    sub = "\n        <p>(A wholly owned subsidiary of GoldenPi Technologies Pvt Ltd)</p>"
    if html.count(sub) != 1:
        raise SystemExit("fold_footer: subsidiary line not found")
    html = html.replace(sub, "", 1)
    sebi = re.search(r"(?m)^ *<div><dt>SEBI Registration No\.:</dt>.*?</div>", ids)
    ids = ids[:sebi.end()] + "\n        <div><dt>CIN:</dt><dd>%s</dd></div>" % brand.group(1) + ids[sebi.end():]
    end_cols = '\n    </div>\n\n    <nav class="ft-band" aria-labelledby="ft-info"'
    if html.count(end_cols) != 1:
        raise SystemExit("fold_footer: end of link columns not found")
    html = html.replace(end_cols, '\n    </div>\n\n'
                        '    <div class="ft-regs" data-reveal>\n'
                        '      <dl class="ft-ids">\n' + ids + '\n      </dl>' + paras + '\n    </div>\n'
                        + end_cols[len('\n    </div>\n'):], 1)
    html = html.replace(copy, "", 1)
    html = html.replace(bands, "\n  </div>\n\n"
                        '  <details class="ft-fold">\n'
                        '    <summary class="gp-shell">\n'
                        '      <span class="ft-copy">&copy; Copyright 2017 - 2026 | GoldenPi Securities Pvt. Ltd.</span>\n'
                        '      <span class="ft-fold__btn">Read More</span>\n'
                        '    </summary>\n'
                        '  <div class="gp-shell ft__inner">\n' + bands, 1)
    # The outer fold is the only toggle: Note to Investors shows in full once open.
    more = re.search(r'\n *<details class="ft-more">\n *<summary>Read More</summary>(.*?)\n *</details>', html, re.S)
    if not more:
        raise SystemExit("fold_footer: Note to Investors read-more not found")
    html = html[:more.start()] + more.group(1) + html[more.end():]
    # Important Information goes, after the fold is built on it (it holds the Important links too, merged above).
    info = re.search(r'\n    <nav class="ft-band" aria-labelledby="ft-info".*?</nav>', html, re.S)
    if not info:
        raise SystemExit("fold_footer: Important Information band not found")
    html = html[:info.start()] + html[info.end():]
    # A heading for the BSE Investor Protection Fund link, inside Note to Investors.
    bse = '\n          <p><a class="u" href="https://www.bseipf.com/investors_education.html">'
    if html.count(bse) != 1:
        raise SystemExit("fold_footer: BSE IPF link not found")
    html = html.replace(bse, '\n          <h2 class="ft-sub">Investor Education</h2>' + bse, 1)
    # Its three paragraphs (the link, the "educated investor" line and the
    # first disclaimer) read as one, the line no longer bold.
    edu = re.search(r'\n          <p>(<a class="u" href="https://www\.bseipf\.com/[^"]*">[^<]*</a>)</p>'
                    r'\n *<p><strong>([^<]*)</strong></p>\n *<p>(The information shown on the website[^<]*)</p>', html)
    if not edu:
        raise SystemExit("fold_footer: Investor Education paragraphs not found")
    html = html[:edu.start()] + '\n          <p>%s %s %s</p>' % edu.groups() + html[edu.end():]
    return html.replace("\n</footer>", "\n  </details>\n</footer>", 1)


def write_footer_page(page):
    """footer-ggn-prelogin-home.html: index.html's footer (fold and all) on a
    page of its own, in the black / white / gold scheme (ft--black). Built
    from the index output, so the two cannot drift."""
    head = page[:page.index("<body>")]
    head = re.sub(r"<title>.*?</title>", "<title>Footer, pre-login home | GoldenPi</title>", head, count=1, flags=re.S)
    head = re.sub(r'<meta name="description" content="[^"]*">',
                  '<meta name="description" content="GoldenPi site footer for the pre-login homepage: navigation, '
                  'registration details and compliance contacts.">', head, count=1)
    i = page.index('<footer class="ft ft--dark"')
    foot = page[i:].replace('<footer class="ft ft--dark"', '<footer class="ft ft--dark ft--black"', 1)
    # The ggn footers drop "State Government Guaranteed Bonds" from the New to
    # GoldenPi column (user, 2026-10-07); the Collections chip of that name stays.
    sgg = re.search(r'\s*<li><a class="ft-link" href="[^"]*">State Government Guaranteed Bonds</a></li>', foot)
    if not sgg:
        raise SystemExit("footer-ggn-prelogin-home: State Government Guaranteed Bonds link not found")
    foot = foot[:sgg.start()] + foot[sgg.end():]
    body = ('<body>\n\n<a class="gp-skip" href="#footer">Skip to footer</a>\n\n'
            '<main>\n  <h1 class="sr-only">GoldenPi footer, pre-login home</h1>\n</main>\n\n'
            '<!-- index.html\'s footer, black scheme. Generated by pages/_convert.py; do not edit. -->\n')
    with open(os.path.join(HERE, "footer-ggn-prelogin-home.html"), "w", encoding="utf-8") as f:
        f.write(head + body + foot)


def main():
    for name, fn in (("index.html", build_index),
                     ("fixed-deposits.html", build_fd),
                     ("bond-ipo-online.html", build_ipo)):
        out = F.webinar(F.golden_experience(F.primary_ctas(fn())))
        if name == "index.html":
            out = F.dark_footer(fold_footer(F.new_footer(out)))
            write_footer_page(out)
        open(os.path.join(HERE, name), "w", encoding="utf-8").write(out)
        print("%-24s tabs:%d panels:%d final.css:%d" % (
            name, out.count('class="gp-tab"'), out.count('class="gp-panel'),
            out.count("final.css")))


if __name__ == "__main__":
    main()
