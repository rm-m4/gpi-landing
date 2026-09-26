#!/usr/bin/env python3
"""Write investment-options-list-view.html from the capture of
uatnew.goldenpi.com/investment-options/list-view (Discover Bonds).

A filter sidebar, a sort control and 80 bond rows, all captured 2026-09-26 by
crawl/listview_ui.js into crawl/rendered/list-view.ui.json (rows, every filter
group including those behind More Filters, the sort list, and the copy that
only shows once filters are applied). The rows reuse the listing on
corporate-bonds (gp-panel / gp-rows / gp-row); promo bar, header and footer
come from refer-and-earn.html and are then kept in sync by _build.py. Run:

    python3 pages/_listview.py && python3 pages/_build.py

Filtering and sorting run in the page over the snapshot. Each row carries the
ids of the filter options it matches (data-f), worked out here from its
captured values, so the script only compares sets. Options the row data cannot
answer (issuer type, tax, seniority...) still select, count and chip, but do
not narrow the list: they are marked data-wired="false" and need the API.
"""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _utsav import logo_names, UAT, SHELL_FROM, MAIN, FOOTER  # noqa: E402  shared shell + logo fetch

OUT = "investment-options-list-view.html"
e = html.escape

# Live opens the first three groups and shows seven before More Filters.
OPEN_GROUPS = 3
FIRST_GROUPS = 7
# Their chip prefixes the group name for Yield only ("Yield: 11% +"); the
# other captured chip ("AAA (Low Risk)") has none.
CHIP_PREFIX = {"yield": "Yield: "}

GRADES = ["AAA", "AA+", "AA", "AA-", "A+", "A", "A-", "BBB+", "BBB", "BBB-"]
PAYMENTS = {"pf-annual": "Yearly", "pf-monthly": "Monthly", "pf-quarterly": "Quarterly",
            "pf-half-yearly": "Half Yearly", "pf-payment-on-maturity": "On Maturity"}


def rupees(s):
    """'₹29.9K' -> 29900, '₹10.6L' -> 1060000."""
    m = re.fullmatch(r"₹([\d.]+)([KLC]r?)?", s.replace(",", ""))
    mult = {"K": 1e3, "L": 1e5, "Cr": 1e7, None: 1}[m.group(2)]
    return round(float(m.group(1)) * mult)


def months(s):
    """'2Y 11M' -> 35."""
    y = re.search(r"(\d+)Y", s)
    mo = re.search(r"(\d+)M", s)
    return (int(y.group(1)) * 12 if y else 0) + (int(mo.group(1)) if mo else 0)


# Options the captured row values can answer, as tests on one row.
WIRED = {
    "ip-highest-safety": lambda r: r["grade"] == "AAA",
    "ip-fixed-regular-income": lambda r: r["y"] > 11,
    "ip-invest-short-time": lambda r: r["m"] <= 36,
    "cr-aaa": lambda r: r["grade"] == "AAA",
    "cr-aa": lambda r: r["grade"].startswith("AA") and r["grade"] != "AAA",
    "cr-a": lambda r: not r["grade"].startswith("AA"),
    "yield-highly-safe": lambda r: r["y"] <= 8,
    "yield-safe": lambda r: 8 < r["y"] < 11,
    "yield-high-returns": lambda r: r["y"] >= 11,
    "ia-less-50k": lambda r: r["min"] < 50_000,
    "ia-50k-to-2lacs": lambda r: 50_000 <= r["min"] < 200_000,
    "ia-2-5-lacs": lambda r: 200_000 <= r["min"] < 500_000,
    "ia-5-10-lacs": lambda r: 500_000 <= r["min"] < 1_000_000,
    "ia-10-50-lacs": lambda r: 1_000_000 <= r["min"] < 5_000_000,
    "ia-more-50-lacs": lambda r: r["min"] >= 5_000_000,
    "tr-less-than-1": lambda r: r["m"] < 12,
    "tr-1-5-yrs": lambda r: 12 <= r["m"] < 60,
    "tr-5-10-yrs": lambda r: 60 <= r["m"] < 120,
    "tr-more-than-10-yrs": lambda r: r["m"] >= 120,
    "ina-ncd-ipo": lambda r: r["kind"] == "ipo",
    "ina-ncd": lambda r: r["kind"] == "bond",
    **{k: (lambda v: lambda r: r["pay"] == v)(v) for k, v in PAYMENTS.items()},
    # Thrice yearly: no captured row pays that way, so it matches none.
    "pf-thrice-yearly": lambda r: False,
}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def row(c, i, logos):
    r = {"grade": c["grade"], "y": float(c["yield"].rstrip("%")), "m": months(c["tenure"]),
         "min": rupees(c["minInvestment"]), "pay": c["payments"], "kind": c["kind"]}
    f = " ".join(k for k, test in WIRED.items() if test(r))
    safety = len(GRADES) - GRADES.index(c["grade"])
    ipo = (f'\n    <p class="gp-lv-row__ipo"><span class="gp-lv-row__ipo-tag">{e(c["ipoTag"])}</span>'
           f'{e(c["closes"])}</p>' if c["ipoTag"] else "")
    watch = ('\n    <button type="button" aria-label="Add to watchlist" aria-pressed="false">'
             '<img src="../assets/img/goolden-bookmark.svg" alt="" width="20" height="20"></button>'
             if c["watchlist"] else "")
    return f'''<article class="gp-row gp-lv-row" style="--r:{min(i, 11)}" data-i="{i}" data-f="{f}"
         data-min="{r["min"]}" data-yield="{r["y"]}" data-safety="{safety}" data-tenure="{r["m"]}">
  <div class="gp-row__identity">
    <img class="gp-row__logo" src="../assets/img/{e(logos[c["logo"]])}" alt="">
    <a class="gp-row__name gp-row__link" href="{e(UAT + c["href"])}" aria-label="Issuer: {e(c["issuer"])}">{e(c["issuer"])}</a>{ipo}
  </div>
  <div><div class="gp-row__label">Yield</div><div class="gp-row__value gp-row__value--returns">{e(c["yield"])}</div></div>
  <div><div class="gp-row__label">Rating</div><div class="gp-row__value">{e(c["agency"])} {e(c["grade"])}</div></div>
  <div><div class="gp-row__label">Payments</div><div class="gp-row__value">{e(c["payments"])}</div></div>
  <div><div class="gp-row__label">Tenure</div><div class="gp-row__value">{e(c["tenure"])}</div></div>
  <div class="gp-row__actions">{watch}
    <button type="button" aria-label="Share"><img src="../assets/img/golden-share.svg" alt="" width="16" height="16"></button>
  </div>
</article>'''


CHEVRON = ('<svg viewBox="0 0 16 16" width="16" height="16" fill="none" aria-hidden="true">'
           '<path d="m4 6 4 4 4-4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
           'stroke-linejoin="round"/></svg>')


def group(g, k):
    key = g["id"].replace("bond-list-accordion-", "")
    opts = []
    for o in g["options"]:
        oid = o["id"].replace("bond-list-", "")
        wired = oid in WIRED
        opts.append(
            f'''<li><label class="gp-lv-opt">
                <input type="{o["type"]}" name="{e(key)}" value="{e(oid)}" id="lv-{slug(oid)}"{"" if wired else ' data-wired="false"'}
                       data-chip="{e(CHIP_PREFIX.get(key, "") + o["text"])}">
                <span>{e(o["text"])}</span>
              </label></li>''')
    return f'''<details class="gp-lv-group"{" open" if k < OPEN_GROUPS else ""}>
            <summary>{e(g["title"])}{CHEVRON}</summary>
            <fieldset>
              <legend class="sr-only">{e(g["legend"])}</legend>
              <ul>
              {"".join(opts)}
              </ul>
            </fieldset>
          </details>'''


def main():
    data = json.load(open(os.path.join(os.path.dirname(HERE), "crawl", "rendered", "list-view.ui.json"),
                      encoding="utf-8"))
    cards, st, sheet = data["cards"], data["states"], data["sheet"]
    logos = logo_names([{"cards": cards}])
    groups = data["groups"]
    first = "\n          ".join(group(g, k) for k, g in enumerate(groups[:FIRST_GROUPS]))
    rest = "\n          ".join(group(g, k) for k, g in enumerate(groups[FIRST_GROUPS:], FIRST_GROUPS))
    more_on, less = data["moreText"].replace("−", "").strip(), "More Filters"
    sort_opts = "\n".join(
        f'            <option value="{slug(s["text"])}"{" selected" if s["selected"] else ""}>{e(s["text"])}</option>'
        for s in data["sort"])
    rows = "\n".join(row(c, i, logos) for i, c in enumerate(cards))
    n = len(cards)
    help_ = data["help"]

    shell = open(os.path.join(HERE, SHELL_FROM), encoding="utf-8").read()
    head = shell[:shell.index(MAIN)]
    head = head.replace("<title>Refer &amp; Earn | GoldenPi</title>", "<title>Discover Bonds | GoldenPi</title>")
    head = head[:head.index("<!-- Refer & Earn, rebuilt")] + (
        "<!-- GENERATED by pages/_listview.py from crawl/rendered/list-view.ui.json.\n"
        "     Edit the generator, not this file. Copy verbatim from\n"
        "     uatnew.goldenpi.com/investment-options/list-view (captured 2026-09-26);\n"
        "     see content/investment-options_list-view.md. -->\n"
    ) + head[head.index('<meta name="description"'):]
    d0 = head.index('<meta name="description"')
    head = head.replace(head[d0:head.index(">", d0) + 1],
                        '<meta name="description" content="Explore and filter corporate bonds, G-Secs, and NCD IPOs on GoldenPi.">')
    footer = shell[shell.index(FOOTER):shell.index("</footer>") + len("</footer>")]
    js = open(os.path.join(HERE, "_reveal.js"), encoding="utf-8").read() + "\n" + open(
        os.path.join(HERE, "_listview.js"), encoding="utf-8").read()

    main_html = f'''{MAIN}

  <!-- ============================================================== head -->
  <!-- The live page opens straight on the breadcrumb and the list; the
       heading is its title and breadcrumb label, the line its meta
       description. -->
  <section class="gp-hero gp-lv-hero">
    <div class="gp-shell pt-6 pb-6">
      <nav class="t-small t-muted mb-5" aria-label="Breadcrumb">
        <a href="index.html" class="hover:text-ink">Home</a>
        <span class="mx-1.5">&rsaquo;</span>
        <span class="text-ink font-medium" aria-current="page">Discover Bonds</span>
      </nav>
      <h1 class="gp-section__title">Discover Bonds</h1>
      <p class="gp-section__sub">Explore and filter corporate bonds, G-Secs, and NCD IPOs on GoldenPi.</p>
    </div>
  </section>

  <!-- ============================================================ listing -->
  <!-- DATA: {len(cards)} rows, API-driven and filtered / sorted server-side on the
       live page (?cr=aaa&sortBy=ytmc-desc). Snapshot {data["captured"][:10]} by
       crawl/listview_ui.js; here the page filters and sorts that snapshot. -->
  <section class="gp-section gp-section--tight gp-lv" aria-label="Bonds">
    <div class="gp-shell">
      <div class="gp-lv__bar" role="toolbar" aria-label="Filter and sort">
        <button type="button" class="gp-lv__bar-btn" aria-controls="lv-filters" aria-expanded="false" data-open-filters>
          Filters <span class="gp-lv__badge" data-applied-badge hidden>0</span>
        </button>
        <span class="gp-lv__bar-divider" aria-hidden="true"></span>
        <label class="gp-lv__sort gp-lv__sort--bar">
          <span class="sr-only">Sort By</span>
          <select data-sort aria-label="Sort By">
{sort_opts}
          </select>
          {CHEVRON}
        </label>
      </div>

      <div class="gp-lv__layout">
        <aside class="gp-lv-filter" id="lv-filters" aria-label="Filter">
          <header class="gp-lv-filter__head">
            <h2 class="gp-lv-filter__title">{e(sheet["title"])}</h2>
            <button type="button" class="gp-lv-filter__clear" data-clear hidden>{e(st["clear"])}</button>
            <button type="button" class="gp-lv-filter__close" data-close-filters aria-label="Close">&times;</button>
            <p class="gp-lv-filter__applied" aria-live="polite"><span data-applied>0</span> filter applied</p>
          </header>
          <ul class="gp-lv-chips" data-chips aria-label="Applied filters"></ul>

          <form class="gp-lv-filter__groups" data-filters>
          {first}
          <div class="gp-lv-filter__more" id="lv-more" hidden>
          {rest}
          </div>
          </form>
          <button type="button" class="gp-lv-filter__more-btn" aria-expanded="false" aria-controls="lv-more"
                  data-more data-more-text="{e(less)}" data-less-text="{e(more_on)}">
            <span aria-hidden="true">+</span><span>{e(less)}</span>
          </button>

          <footer class="gp-lv-filter__foot">
            <button type="button" class="gp-cta gp-cta--secondary" data-clear-sheet>{e(sheet["clear"])}</button>
            <button type="button" class="gp-cta gp-cta--primary" data-close-filters>{e(sheet["apply"])}</button>
          </footer>
        </aside>

        <div class="gp-lv__main">
          <div class="gp-lv__toolbar">
            <p class="gp-lv__count" aria-live="polite">Showing <span data-count>{n}</span> Bonds</p>
            <label class="gp-lv__sort">
              <span>{e(data["sortLabel"])}:</span>
              <select data-sort>
{sort_opts}
              </select>
              {CHEVRON}
            </label>
          </div>

          <div class="gp-panel is-on gp-lv__panel">
            <div class="gp-rows__head" aria-hidden="true">
              <span></span><span>Yield</span><span>Rating</span>
              <span>Payments</span><span>Tenure</span><span></span>
            </div>
            <div class="gp-rows" data-rows>
{rows}
            </div>
            <div class="gp-empty-state gp-lv__empty" role="status" data-empty hidden>
              <img src="../assets/img/empty-state-icon.svg" alt="{e(st["emptyAlt"])}" width="120" height="120">
              <p>{e(st["emptyText"])}</p>
            </div>
          </div>

          <!-- Same block as the issuer page. Contact Us is a button on the live
               page (it opens support there), so it stays one. -->
          <aside class="gp-need-help gp-need-help--row" data-reveal>
            <img class="gp-need-help__image" src="../assets/img/support-icon.svg" alt="" width="237" height="237">
            <div>
              <p class="gp-need-help__title">
                <img src="../assets/img/phone-icon.svg" alt="" width="20" height="20">
                {e(help_["title"])}
              </p>
              <p class="gp-need-help__desc">{e(help_["text"][0])}</p>
              <button type="button" class="gp-cta gp-cta--primary">
                Contact Us
                <img class="gp-cta__arrow" src="../assets/img/arrow-right.svg" alt="" width="16" height="16">
              </button>
            </div>
          </aside>
        </div>
      </div>
    </div>
    <div class="gp-lv__scrim" data-close-filters hidden></div>
  </section>
</main>

'''
    out = head + main_html + footer + "\n\n<script>\n" + js + "</script>\n\n</body>\n</html>\n"
    open(os.path.join(HERE, OUT), "w", encoding="utf-8").write(out)
    print("wrote %s  (%d rows, %d filter groups)" % (OUT, len(cards), len(groups)))


if __name__ == "__main__":
    main()
