#!/usr/bin/env python3
"""Generate pages/corporate-bonds.html.

This page is the former corporate-bonds.html (now archived as
corporate-bonds-old.html) with four improvements ported in from the taste2
exploration. It keeps the same stack, the same shared header and
footer, and the same gp-* components, so the change a developer implements is a
small diff rather than a new design system.

Only the tabbed listing is generated, because it is repetitive and data-driven.
Everything else lives in _final_shell.html and is edited by hand.

Each tab draws rows actually captured from uatnew.goldenpi.com on 2026-09-25.
Nothing is invented. Where a tab's best match was captured on another page (the
NCD IPOs, the Muthoot Capital bond and its stated minimum), the panel says so.

Run: python3 pages/_final.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://uatnew.goldenpi.com"

A = "GPID102720.AKARA-CAPITAL-ADVISORS-PRIVATE-LIMITED-2x.png"
N = "GPID104095.Neogrowth-new-logo-1-.jpg"
B = "GPID107347.Best-Capital.png"
E = "GPID100778.EDELWEISS-FINANCIAL-SERVICES-LIMITED.png"
M = "GPID100936.MUTHOOT-FINCORP-LIMITED_1-2x.png"

# issuer, logo, returns, rating, fourth-column value, fifth-column value, href
AKARA_13 = ("AKARA", A, "13.00%", "ACUITE BBB+", "Monthly", "3-Dec-2027",
            "/bonds/GPID107435/akara-1300-bond-yield?src=view_details&tenureDate=03-Dec-2027")
NEO = ("NEOGROWTH", N, "13.00%", "ICRA BBB", "Half Yearly", "30-Apr-2028",
       "/bonds/GPID107371/neogrowth-1300-bond-yield?src=view_details&tenureDate=30-Apr-2028")
BEST = ("BEST CAPITAL", B, "13.00%", "IVR BBB", "Monthly", "11-Sep-2029",
        "/bonds/GPID107433/best-capital-1300-bond-yield?src=view_details&tenureDate=11-Sep-2029")
AKARA_12 = ("AKARA", A, "12.78%", "ACUITE BBB+", "Monthly", "3-Dec-2027",
            "/bonds/GPID107435/akara-1278-bond-yield?src=view_details&tenureDate=03-Dec-2027")
EDEL = ("EDELWEISS FINANCIAL SERVICES LIMITED", E, "10.00%", "A+/STABLE CRISIL",
        "Fast Filling", "5-Oct-2026",
        "/bond-ipo/GPID100778/edelweiss-financial-services-limited?src=preview")
MUTH_IPO = ("MUTHOOT FINCORP LIMITED", M, "9.25%", "AA/STABLE CRISIL",
            "Fast Filling", "22-Sep-2026",
            "/bond-ipo/GPID100936/muthoot-fincorp-limited?src=preview")
MUTH_CAP = ("MUTHOOT CAPITAL", M, "9.70%", "CRISIL AA-", "&#8377;30,000", "24-Aug-2029",
            "/bonds/INE296G07333/muthoot-capital-925-bond-yield?src=view_details&tenureDate=24-Aug-2029")

TABS = [
    dict(id="utsav", label="Bond Utsav Deals", icon="pre-login-active-offers.svg",
         col4="Payout", col5="Maturity Date", rows=[AKARA_13, NEO, BEST, AKARA_12],
         more=("View All", "/bond-utsav"), note=None),

    dict(id="rated", label="High Rated Bonds", icon="pre-login-aaa-rated.svg",
         col4="Status", col5="Closes On", rows=[EDEL, MUTH_IPO],
         more=("View all highly rated bonds", "/collections/highly-rated-bonds"),
         note="The highest rated issues in this snapshot are the two live NCD IPOs."),

    dict(id="thirtyk", label="Bonds at &#8377;30K", icon="pre-login-bonds-at-10k.svg",
         col4="Min. Investment", col5="Maturity Date", rows=[MUTH_CAP],
         more=("View bonds under &#8377;10,000", "/collections/bonds-at-10000"),
         note="Minimum investment as listed by the issuer."),

    dict(id="monthly", label="Bonds for Monthly Income", icon="monthly-bonds.svg",
         col4="Payout", col5="Maturity Date", rows=[AKARA_13, BEST, AKARA_12],
         more=("View all monthly income bonds", "/collections/bonds-to-earn-monthly-fixed-income"),
         note=None),

    dict(id="yield", label="11%+ Yield Bonds", icon="pre-login-home-highest-yield.svg",
         col4="Payout", col5="Maturity Date", rows=[AKARA_13, NEO, BEST, AKARA_12],
         more=("View all high yield bonds", "/collections/high-yield-bonds"), note=None),

    dict(id="ipo", label="NCD IPO", icon="pre-login-ncd-ipo.svg",
         col4="Status", col5="Closes On", rows=[EDEL, MUTH_IPO],
         more=("View all ongoing NCD IPOs", "/collections/best-ongoing-ipos"), note=None),
]


def row_html(r, i, col4, col5):
    """One listing row, in the page's existing .gp-row markup."""
    name, logo, ret, rating, four, five, href = r
    link = BASE + href.replace("&", "&amp;")
    return (
        '            <article class="gp-row" style="--r:%d">\n'
        '              <div class="gp-row__identity">\n'
        '                <img class="gp-row__logo" src="../assets/img/%s" alt="">\n'
        '                <a class="gp-row__name gp-row__link" href="%s">%s</a>\n'
        '              </div>\n'
        '              <div><div class="gp-row__label">Returns</div>'
        '<div class="gp-row__value gp-row__value--returns">%s</div></div>\n'
        '              <div><div class="gp-row__label">Credit Rating</div>'
        '<div class="gp-row__value">%s</div></div>\n'
        '              <div><div class="gp-row__label">%s</div>'
        '<div class="gp-row__value">%s</div></div>\n'
        '              <div><div class="gp-row__label">%s</div>'
        '<div class="gp-row__value">%s</div></div>\n'
        '              <div class="gp-row__actions">\n'
        '                <button type="button" title="Add to watchlist">'
        '<img src="../assets/img/goolden-bookmark.svg" alt="Add to watchlist"></button>\n'
        '                <button type="button" title="Share">'
        '<img src="../assets/img/golden-share.svg" alt="Share"></button>\n'
        '              </div>\n'
        '            </article>'
    ) % (i, logo, link, name, ret, rating, col4, four, col5, five)


def build():
    buttons, panels = [], []
    for k, t in enumerate(TABS):
        sel = "true" if k == 0 else "false"
        tabindex = "" if k == 0 else ' tabindex="-1"'
        buttons.append(
            '            <button type="button" class="gp-tab" role="tab" id="tab-%s"\n'
            '                    aria-controls="panel-%s" aria-selected="%s"%s>\n'
            '              <img src="../assets/img/%s" alt="">%s\n'
            '            </button>' % (t["id"], t["id"], sel, tabindex, t["icon"], t["label"]))

        note = ('          <p class="gp-panel__note">%s</p>\n' % t["note"]) if t["note"] else ""
        rows = "\n\n".join(row_html(r, i, t["col4"], t["col5"]) for i, r in enumerate(t["rows"]))
        more_label, more_href = t["more"]
        panels.append(
            '        <div class="gp-panel%s" id="panel-%s"\n'
            '             role="tabpanel" aria-labelledby="tab-%s"%s>\n'
            '%s'
            '          <div class="gp-rows__head">\n'
            '            <span>Issuer</span><span>Returns</span><span>Credit Rating</span>\n'
            '            <span>%s</span><span>%s</span><span></span>\n'
            '          </div>\n\n'
            '          <div class="gp-rows">\n%s\n          </div>\n\n'
            '          <div class="mt-5 text-center">\n'
            '            <a class="t-small font-bold t-bronze underline" href="%s%s">%s</a>\n'
            '          </div>\n'
            '        </div>' % (
                " is-on" if k == 0 else "", t["id"], t["id"],
                "" if k == 0 else " hidden", note,
                t["col4"], t["col5"], rows, BASE, more_href, more_label))

    return "\n\n".join(buttons), "\n\n".join(panels)


def main():
    buttons, panels = build()
    src = open(os.path.join(HERE, "_final_shell.html"), encoding="utf-8").read()
    for token in ("<!--TABS-->", "<!--PANELS-->", "<!--TABJS-->"):
        if token not in src:
            raise SystemExit("_final_shell.html is missing %s" % token)
    js = open(os.path.join(HERE, "_tabs.js"), encoding="utf-8").read()
    out = (src.replace("<!--TABS-->", buttons)
              .replace("<!--PANELS-->", panels)
              .replace("<!--TABJS-->", "<script>\n%s</script>" % js))
    path = os.path.join(HERE, "corporate-bonds.html")
    open(path, "w", encoding="utf-8").write(out)
    print("wrote %s  (%d tabs, %d rows)" % (
        os.path.basename(path), len(TABS), sum(len(t["rows"]) for t in TABS)))


if __name__ == "__main__":
    main()
