#!/usr/bin/env python3
"""Generate pages/corporate-bonds-final.html.

The tabbed listing is data-driven: each tab draws from rows actually captured
from uatnew.goldenpi.com on 2026-09-25. Nothing here is invented. Where a tab's
natural match lives on another captured page (the NCD IPOs, the Muthoot Capital
bond with its 30,000 minimum), the row carries a note saying so.

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

# name, logo, returns, rating, payout, last-column value, href
AKARA_13 = ("AKARA", A, "13.00%", "ACUITE BBB+", "Monthly", "3 Dec 2027",
            "/bonds/GPID107435/akara-1300-bond-yield?src=view_details&tenureDate=03-Dec-2027")
NEO = ("NEOGROWTH", N, "13.00%", "ICRA BBB", "Half Yearly", "30 Apr 2028",
       "/bonds/GPID107371/neogrowth-1300-bond-yield?src=view_details&tenureDate=30-Apr-2028")
BEST = ("BEST CAPITAL", B, "13.00%", "IVR BBB", "Monthly", "11 Sep 2029",
        "/bonds/GPID107433/best-capital-1300-bond-yield?src=view_details&tenureDate=11-Sep-2029")
AKARA_12 = ("AKARA", A, "12.78%", "ACUITE BBB+", "Monthly", "3 Dec 2027",
            "/bonds/GPID107435/akara-1278-bond-yield?src=view_details&tenureDate=03-Dec-2027")
EDEL = ("EDELWEISS FINANCIAL SERVICES LIMITED", E, "10.00%", "A+/STABLE CRISIL", "Fast filling", "5 Oct 2026",
        "/bond-ipo/GPID100778/edelweiss-financial-services-limited?src=preview")
MUTH_IPO = ("MUTHOOT FINCORP LIMITED", M, "9.25%", "AA/STABLE CRISIL", "Fast filling", "22 Sep 2026",
            "/bond-ipo/GPID100936/muthoot-fincorp-limited?src=preview")
MUTH_CAP = ("MUTHOOT CAPITAL", M, "9.70%", "CRISIL AA-", "Min. &#8377;30,000", "24 Aug 2029",
            "/bonds/INE296G07333/muthoot-capital-925-bond-yield?src=view_details&tenureDate=24-Aug-2029")

TABS = [
    dict(id="utsav", label="Bond Utsav Deals", icon="pre-login-active-offers.svg",
         col4="Payout", last="Maturity date", rows=[AKARA_13, NEO, BEST, AKARA_12],
         more=("View all Bond Utsav deals", "/bond-utsav"), note=None),

    dict(id="rated", label="High Rated Bonds", icon="pre-login-aaa-rated.svg",
         col4="Status", last="Closes on", rows=[EDEL, MUTH_IPO],
         more=("View all highly rated bonds", "/collections/highly-rated-bonds"),
         note="The highest rated issues in this snapshot are the two live NCD IPOs."),

    dict(id="thirtyk", label="Bonds at &#8377;30K", icon="pre-login-bonds-at-10k.svg",
         col4="Minimum", last="Maturity date", rows=[MUTH_CAP],
         more=("View bonds under &#8377;10,000", "/collections/bonds-at-10000"),
         note="Minimum investment as listed by the issuer."),

    dict(id="monthly", label="Bonds for Monthly Income", icon="monthly-bonds.svg",
         col4="Payout", last="Maturity date", rows=[AKARA_13, BEST, AKARA_12],
         more=("View all monthly income bonds", "/collections/bonds-to-earn-monthly-fixed-income"),
         note=None),

    dict(id="yield", label="11%+ Yield Bonds", icon="pre-login-home-highest-yield.svg",
         col4="Payout", last="Maturity date", rows=[AKARA_13, NEO, BEST, AKARA_12],
         more=("View all high yield bonds", "/collections/high-yield-bonds"), note=None),

    dict(id="ipo", label="NCD IPO", icon="pre-login-ncd-ipo.svg",
         col4="Status", last="Closes on", rows=[EDEL, MUTH_IPO],
         more=("View all ongoing NCD IPOs", "/collections/best-ongoing-ipos"), note=None),
]

ARROW_UR = ('<svg viewBox="0 0 16 16" fill="none"><path d="M4 12L12 4M12 4H6M12 4v6" '
            'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>')
ARROW_R = ('<svg viewBox="0 0 16 16" fill="none"><path d="M3 8h10M9 4l4 4-4 4" '
           'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def row_html(r, i, col4="Payout"):
    name, logo, ret, rating, payout, last, href = r
    return f'''          <a class="row" style="--r:{i}" href="{BASE}{href.replace('&', '&amp;')}">
            <span class="row__id"><img src="../assets/img/{logo}" alt="">{name}</span>
            <span><span class="row__k">Returns</span><span class="row__v row__v--up">{ret}</span></span>
            <span><span class="row__k">Credit rating</span><span class="row__v">{rating}</span></span>
            <span><span class="row__k">{col4}</span><span class="row__v">{payout}</span></span>
            <span><span class="row__k">Date</span><span class="row__v">{last}</span></span>
          </a>'''


def tabs_html():
    buttons, panels = [], []
    for k, t in enumerate(TABS):
        sel = "true" if k == 0 else "false"
        buttons.append(
            f'''        <button type="button" class="tab" role="tab" id="tab-{t["id"]}"
                aria-controls="panel-{t["id"]}" aria-selected="{sel}"{"" if k == 0 else ' tabindex="-1"'}>
          <img src="../assets/img/{t["icon"]}" alt="">{t["label"]}
        </button>''')

        note = (f'\n        <p class="panel__note">{t["note"]}</p>' if t["note"] else "")
        rows = "\n\n".join(row_html(r, i, t["col4"]) for i, r in enumerate(t["rows"]))
        more_label, more_href = t["more"]
        panels.append(
            f'''      <div class="panel{" is-on" if k == 0 else ""}" id="panel-{t["id"]}"
           role="tabpanel" aria-labelledby="tab-{t["id"]}"{"" if k == 0 else " hidden"}>{note}

        <div class="rows__head">
          <span>Issuer</span><span>Returns</span><span>Credit rating</span>
          <span>{t["col4"]}</span><span>{t["last"]}</span>
        </div>

{rows}

        <p style="padding:22px 26px 6px">
          <a class="tlink" href="{BASE}{more_href}">{more_label} {ARROW_R}</a>
        </p>
      </div>''')
    return "\n\n".join(buttons), "\n\n".join(panels)


def main():
    buttons, panels = tabs_html()
    src = open(os.path.join(HERE, "_final_shell.html"), encoding="utf-8").read()
    out = src.replace("<!--TABS-->", buttons).replace("<!--PANELS-->", panels)
    path = os.path.join(HERE, "corporate-bonds-final.html")
    open(path, "w", encoding="utf-8").write(out)
    rows = sum(len(t["rows"]) for t in TABS)
    print("wrote %s  (%d tabs, %d rows)" % (os.path.basename(path), len(TABS), rows))


if __name__ == "__main__":
    main()
