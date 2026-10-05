#!/usr/bin/env python3
"""Write bond-utsav-live.html from the production capture of goldenpi.com/bond-utsav.

bond-utsav.html is built from UAT, which shows a card grid. Production (the
Angular site) shows the same campaign as a dark, gold-ribbed row list: a
marketing ribbon, logo and issuer, a 24x7 Order chip, then Returns (with the
struck-through earlier rate), Credit Rating and Tenure. This page keeps that
UI and its data, restyled in the repo's tokens and Satoshi.

Data: crawl/rendered/prod_bond-utsav.tabs.json, written by
crawl/utsav_prod_tabs.js (every tab, every row, the tooltip, both banners).
Shell (promo bar, header, footer) is lifted from refer-and-earn.html as
_utsav.py does, then kept in sync by _build.py. CSS: BOND UTSAV LIVE block
at the end of final.css. Run:

    python3 pages/_utsav_live.py && python3 pages/_build.py
"""
import html
import json
import os

from _utsav import HERE, ROOT, MAIN, FOOTER, SHELL_FROM, ROW_SPLIT, logo_names

PROD = "https://goldenpi.com"
DATA = os.path.join(ROOT, "crawl", "rendered", "prod_bond-utsav.tabs.json")
# Seen in the production capture: the popup close icon and the empty-tab icon.
CLOSE_ICON = "https://d2tfvseypdp8pf.cloudfront.net/assets/img/close.svg"
INFO_ICON = "https://goldenpi.com/assets/img/info-copy.svg"  # the chip's infoicon attribute
EMPTY_ICON = "https://d2tfvseypdp8pf.cloudfront.net/assets/img/Circular_Error_ indicator.svg"
BG = "https://goldenpi.com/assets/img/bond-utsav/tabs-bg.png"
BG_MOBILE = "https://goldenpi.com/assets/img/bond-utsav/tabs-mob-bg.png"
# Production colours the rating green (rgb(5, 107, 69)) on some rows.
GREEN = "rgb(5, 107, 69)"

e = html.escape


def localise(urls):
    """Local file name for each URL, fetching what assets/img lacks."""
    names = logo_names([{"cards": [{"logo": u} for u in urls]}])
    return lambda u: "../assets/img/" + names[u]


def slug(label):
    return "-".join(label.lower().split())


def row(r, i, img):
    was = ('\n          <s><span class="sr-only">was </span>%s</s>' % e(r["was"])) if r["was"] else ""
    tag = '\n  <p class="gp-lrow__tag">%s</p>' % e(r["tag"]) if r["tag"] else ""
    amo = ('''
  <button type="button" class="gp-lrow__amo" popovertarget="amo-tip">24x7 Order
    <img src="%s" alt="" width="14" height="14"><span class="sr-only">: what this means</span>
  </button>''' % img(INFO_ICON)) if r["amo"] else ""
    rating = ' class="is-green"' if r["ratingColor"] == GREEN else ""
    return f'''<li class="gp-lrow{"" if r["tag"] else " gp-lrow--untagged"}" style="--i:{min(i, 11)}">{tag}
  <a class="gp-lrow__link" href="{e(PROD + r["href"])}" aria-label="View {e(r["issuer"])}"></a>
  <div class="gp-lrow__id">
    <span class="gp-lrow__logo"><img src="{e(img(r["logo"]))}" alt="" width="40" height="40" loading="lazy"></span>
    <h3 class="gp-lrow__issuer">{e(r["issuer"])}</h3>
  </div>{amo}
  <dl class="gp-lrow__data">
    <div class="gp-lrow__ret"><dt>Returns</dt><dd><strong>{e(r["rate"])}</strong>{was}</dd></div>
    <div><dt>Credit Rating</dt><dd{rating}>{e(r["rating"])}</dd></div>
    <div><dt>Tenure</dt><dd>{e(r["maturity"])} <small>{e(r["remaining"])}</small></dd></div>
  </dl>
</li>'''


def listing(data, img):
    buttons, panels = [], []
    for k, t in enumerate(data["tabs"]):
        on, s = k == 0, slug(t["label"])
        buttons.append(
            f'''<button type="button" class="gp-pill" role="tab" id="tab-{s}"
                      aria-controls="panel-{s}" aria-selected="{str(on).lower()}"{"" if on else ' tabindex="-1"'}>
                <img src="{e(img(t["icon"]))}" alt="" width="30" height="30">{e(t["label"])}
              </button>''')
        if t["rows"]:
            body = '<ol class="gp-lrows">\n%s\n          </ol>' % "\n".join(
                row(r, i, img) for i, r in enumerate(t["rows"]))
        else:
            body = f'''<div class="gp-empty-state gp-ulive-empty" role="status">
            <img src="{e(img(EMPTY_ICON))}" alt="no result" width="96" height="96">
            <p>{e(t["empty"])}</p>
          </div>'''
        panels.append(
            f'''<div class="gp-panel{" is-on" if on else ""}" id="panel-{s}"
             role="tabpanel" aria-labelledby="tab-{s}"{"" if on else " hidden"}>
          {body}
        </div>''')
    rows = [buttons[:ROW_SPLIT], buttons[ROW_SPLIT:]]
    strip = "\n".join('            <div class="gp-pills__row" role="none">\n              %s\n            </div>'
                      % "\n              ".join(r) for r in rows)
    return strip, "\n\n        ".join(panels)


def main():
    data = json.load(open(DATA, encoding="utf-8"))
    tabs = data["tabs"]
    img = localise([data["banner"], data["bannerMobile"], BG, BG_MOBILE, CLOSE_ICON, INFO_ICON, EMPTY_ICON]
                   + [t["icon"] for t in tabs] + [r["logo"] for t in tabs for r in t["rows"]])
    buttons, panels = listing(data, img)
    head_txt, sub = data["heading"], data["subheading"]
    lead, figure = sub.rsplit(" up to ", 1)
    c1, c2, c3 = data["columns"]

    shell = open(os.path.join(HERE, SHELL_FROM), encoding="utf-8").read()
    head = shell[:shell.index(MAIN)]
    head = head.replace("<title>Refer &amp; Earn | GoldenPi</title>",
                        "<title>GoldenPi Bond Utsav | Invest in Bonds Online with returns up to 14%</title>")
    head = head[:head.index("<!-- Refer & Earn, rebuilt")] + (
        "<!-- GENERATED by pages/_utsav_live.py from crawl/rendered/prod_bond-utsav.tabs.json.\n"
        "     Edit the generator, not this file. UI and copy from production,\n"
        "     goldenpi.com/bond-utsav (captured %s). -->\n" % data["captured"][:10]
    ) + head[head.index('<meta name="description"'):]
    d0 = head.index('<meta name="description"')
    head = head.replace(head[d0:head.index(">", d0) + 1],
                        '<meta name="description" content="Discover a special collection of bonds for limited time on '
                        'GoldenPi, India&#x27;s Trusted online platform for buying Listed Corporate Bonds. Start Investing '
                        'with just ₹10000 &amp; Earn up to 14%">')
    head = head.replace("</head>", "<style>\n  .gp-ulive-listing { --ulive-bg: url(%s); }\n"
                        "  @media (max-width: 767px) { .gp-ulive-listing { --ulive-bg: url(%s); } }\n</style>\n</head>"
                        % (img(BG), img(BG_MOBILE)), 1)
    footer = shell[shell.index(FOOTER):shell.index("</footer>") + len("</footer>")]
    js = "\n".join(open(os.path.join(HERE, f), encoding="utf-8").read() for f in ("_tabs.js", "_reveal.js"))

    total = sum(t["count"] for t in tabs)
    main_html = f'''{MAIN}

  <!-- ============================================================== banner -->
  <!-- Production's campaign banner, art from GoldenPi marketing with the offer
       baked in, so it is shown as it is. Not a link on the live page. -->
  <section class="gp-utsav-hero gp-ulive-hero">
    <picture class="gp-utsav-banner">
      <source media="(max-width: 767px)" srcset="{e(img(data["bannerMobile"]))}">
      <img src="{e(img(data["banner"]))}" alt="Bond Utsav promotional banner" fetchpriority="high">
    </picture>
  </section>

  <!-- ========================================================== categories -->
  <!-- DATA: {total} rows across {len(tabs)} tabs, API-driven and infinite-scrolled
       on the live page. Snapshot {data["captured"][:10]} from goldenpi.com, every tab
       driven by crawl/utsav_prod_tabs.js. Rows link where the live row links. -->
  <section class="gp-ulive-listing" aria-labelledby="utsav-heading">
    <div class="gp-shell">
      <div class="gp-ulive-head" data-reveal>
        <h1 id="utsav-heading">{e(head_txt)}</h1>
        <p>{e(lead)} up to <strong>{e(figure)}</strong></p>
      </div>

      <div class="gp-utsav-listing">
        <div class="gp-pills">
          <div class="gp-pills__track" role="tablist" aria-label="{e(head_txt)}">
{buttons}
          </div>
        </div>

        <div class="gp-ulive-cols" aria-hidden="true"><span>{e(c1)}</span><span>{e(c2)}</span><span>{e(c3)}</span></div>

        {panels}
      </div>
    </div>
  </section>

  <!-- The 24x7 Order explainer: production opens it from the chip's info icon.
       Native popover, so it needs no script. Copy verbatim. -->
  <div id="amo-tip" class="gp-ulive-tip" popover>
    <div class="gp-ulive-tip__head">
      <p class="gp-ulive-tip__title">24x7 Order</p>
      <button type="button" popovertarget="amo-tip" popovertargetaction="hide" aria-label="Close">
        <img src="{e(img(CLOSE_ICON))}" alt="" width="14" height="14">
      </button>
    </div>
    <p>{e(data["tooltip"])}</p>
  </div>
</main>

'''
    out = head + main_html + footer + "\n\n<script>\n" + js + "</script>\n\n</body>\n</html>\n"
    open(os.path.join(HERE, "bond-utsav-live.html"), "w", encoding="utf-8").write(out)
    print("wrote bond-utsav-live.html  (%d tabs, %d rows)" % (len(tabs), total))


if __name__ == "__main__":
    main()
