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


def fd_row(key, i):
    name, logo, ret, payout, insured, newac, href = FD[key]
    return (
        '            <article class="gp-row" style="--r:%d">\n'
        '              <div class="gp-row__identity">\n'
        '                <img class="gp-row__logo" src="../assets/img/%s" alt="">\n'
        '                <a class="gp-row__name gp-row__link" href="%s%s">%s</a>\n'
        '              </div>\n'
        '              <div><div class="gp-row__label">Highest Returns</div>'
        '<div class="gp-row__value gp-row__value--returns">%s</div></div>\n'
        '              <div><div class="gp-row__label">Available Payout</div>'
        '<div class="gp-row__value">%s</div></div>\n'
        '              <div><div class="gp-row__label">Insured</div>'
        '<div class="gp-row__value">%s</div></div>\n'
        '              <div><div class="gp-row__label">New Bank A/C</div>'
        '<div class="gp-row__value">%s</div></div>\n'
        '              <div class="gp-row__actions"></div>\n'
        '            </article>' % (i, logo, BASE, href.replace("&", "&amp;"),
                                    name, ret, payout, insured, newac))


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


def listing_body(rows_html, head, more_label, more_href, note=None):
    note_html = ('          <p class="gp-panel__note">%s</p>\n' % note) if note else ""
    return (
        '%s'
        '          <div class="gp-rows__head">\n'
        '            <span>Issuer</span><span>%s</span><span>%s</span>\n'
        '            <span>%s</span><span>%s</span><span></span>\n'
        '          </div>\n\n'
        '          <div class="gp-rows">\n%s\n          </div>\n\n'
        '          <div class="mt-5 text-center">\n'
        '            <a class="t-small font-bold t-bronze underline" href="%s%s">%s</a>\n'
        '          </div>' % (note_html, head[0], head[1], head[2], head[3],
                              rows_html, BASE, more_href, more_label))


MAIN = ['index', 'corporate-bonds', 'fixed-deposits', 'bond-ipo-online']


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
    return html


def bento(html, spans):
    """Collections: three equal columns become an asymmetric bento."""
    i = html.index('Corporate Bond Collections')
    old = '<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">'
    gi = html.index(old, i)
    html = html[:gi] + '<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-6">' + html[gi + len(old):]
    end = html.index('View all Bond Collections', gi)
    seg = html[gi:end]
    card = 'class="gp-card gp-card--link gp-card--accent flex items-center gap-4 p-5"'
    for sp in spans:
        seg = seg.replace(card, 'class="gp-card gp-card--link gp-card--accent gp-bento-cell %s '
                                'flex items-center gap-4 p-5"' % sp, 1)
    return html[:gi] + seg + html[end:]


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

def build_index():
    html = open(os.path.join(HERE, "index-old.html"), encoding="utf-8").read()
    html = common(html, "index")

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
                               "View bonds under &#8377;10,000", "/collections/bonds-at-10000",
                               note="Minimum investment as listed by the issuer.")),
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
             body=listing_body("\n\n".join(fd_row(k, i) for i, k in enumerate(
                                   ["unity", "suryoday", "utkarsh", "shriram", "mahindra", "bajaj"])),
                               ("Highest Returns", "Available Payout", "Insured", "New Bank A/C"),
                               "Compare all fixed deposits", "/fixed-deposits")),
    ]

    # Swap the static tab row and the heading beneath it for the real tablist.
    start = html.index('        <div class="gp-scroller !grid-cols-none mb-6"')
    end = html.index('        <div class="mt-5 text-center">', start)
    end = html.index('</div>', html.index('View All</a>', end)) + len('</div>')
    html = html[:start] + tabstrip(tabs) + "\n" + html[end:]

    html = bento(html, ['lg:col-span-4', 'lg:col-span-2', 'lg:col-span-2',
                        'lg:col-span-2', 'lg:col-span-2', 'lg:col-span-6'])
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
    html = html[:start] + tabstrip(tabs) + "\n" + html[end:]
    return scripts(html)


# --------------------------------------------------------------- bond ipo page

def build_ipo():
    html = open(os.path.join(HERE, "bond-ipo-online-old.html"), encoding="utf-8").read()
    # No category tabs and no collections grid on this page, so it takes the
    # stylesheet and the reviews grid only.
    return scripts(common(html, "bond-ipo-online"), tabs=False)


def main():
    for name, fn in (("index.html", build_index),
                     ("fixed-deposits.html", build_fd),
                     ("bond-ipo-online.html", build_ipo)):
        out = fn()
        open(os.path.join(HERE, name), "w", encoding="utf-8").write(out)
        print("%-24s tabs:%d panels:%d final.css:%d" % (
            name, out.count('class="gp-tab"'), out.count('class="gp-panel'),
            out.count("final.css")))


if __name__ == "__main__":
    main()
