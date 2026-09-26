#!/usr/bin/env python3
"""Write bond-utsav.html from the capture of uatnew.goldenpi.com/bond-utsav.

The page is a banner, a heading and ten category pills over a grid of bond
cards: 227 cards across the tabs, all captured 2026-09-26 by
crawl/utsav_tabs.js into crawl/rendered/bond-utsav.tabs.json. Hand-writing
that many cards drifts, so this generates them, like _legal.py. It also
writes bond-utsav2.html, the review iteration (2026-09-26): same markup and
data, its changes scoped under .gp-utsav-v2 in final.css, plus "p.a." after
the rate and the compact stuck strip (STUCK_JS). Promo bar,
header and footer are lifted from refer-and-earn.html and then kept in sync by
_build.py. Run:

    python3 pages/_utsav.py && python3 pages/_build.py
"""
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "crawl"))
import images  # noqa: E402  (crawl/images.py: naming + fetch, shared)

UAT = "https://uatnew.goldenpi.com"
SHELL_FROM = "refer-and-earn.html"
MAIN = '<main id="main-content">'
FOOTER = "<!-- ============================================================== footer -->"

# The live All Bonds pill has no icon; the pill design the user supplied
# (2026-09-26) gives it their chart icon, which the live page uses on Non NBFC
# Bonds. Every icon is theirs.
ALL_BONDS_ICON = "all-bonds.svg"
TAB_ICONS = {
    "newly-launched-bonds": "GPIDO09029.newly_launch_app.png",
    "high-yield-bonds": "app-high-yield-bonds.png",
    "highly-rated-bonds": "app-highly-rated-bonds.png",
    "bonds-at-30000": "app-starts-at-10k-bonds.png",
    "bonds-for-short-term-investment": "app-bonds-for-short-term-investment.png",
    "bonds-to-earn-monthly-fixed-income": "app-monthly-payout.png",
    "gold-backed-bonds": "app-gold-backed-bonds.png",
    "state-government-guranteed-bonds": "app-govt-backed.png",
    "non-nbfc-bonds": "all-bonds.svg",
}

# The pills stick under the header, so a pill chosen deep in a long list
# would show the new panel from the middle. Bring its top back into view.
SCROLL_JS = """
(function () {
  var strip = document.querySelector('.gp-utsav-listing .gp-pills');
  if (!strip) return;
  strip.addEventListener('click', function (ev) {
    var tab = ev.target.closest('[role="tab"]');
    if (!tab) return;
    var panel = document.getElementById(tab.getAttribute('aria-controls'));
    if (panel && panel.getBoundingClientRect().top < strip.getBoundingClientRect().bottom) {
      var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      panel.scrollIntoView({ behavior: still ? 'auto' : 'smooth', block: 'start' });
    }
  });
})();
"""

# Iteration 2: once the strip sticks under the header it folds to one short
# row, so it stops covering a fifth of the screen. A sentinel above it says
# when; the strip keeps its full height (transparent below the bar) so the
# grid does not jump as it folds.
STUCK_JS = """
(function () {
  var strip = document.querySelector('.gp-utsav-v2 .gp-pills');
  if (!strip || !('IntersectionObserver' in window)) return;
  var mark = document.createElement('div');
  mark.setAttribute('aria-hidden', 'true');
  strip.parentNode.insertBefore(mark, strip);
  new IntersectionObserver(function (entries) {
    var e = entries[0], stuck = !e.isIntersecting && e.boundingClientRect.top < e.rootBounds.top;
    if (stuck === (strip.getAttribute('data-stuck') === 'true')) return;
    if (stuck) strip.style.height = strip.offsetHeight + 'px';
    else strip.style.height = '';
    strip.setAttribute('data-stuck', String(stuck));
    window.dispatchEvent(new Event('resize'));
    var on = strip.querySelector('[aria-selected="true"]');
    if (stuck && on) on.scrollIntoView({ block: 'nearest', inline: 'center' });
  }, { rootMargin: '-67px 0px 0px 0px' }).observe(mark);
})();
"""

e = html.escape


def logo_names(tabs):
    """Local file for every logo URL, fetching the ones only other tabs showed."""
    path = os.path.join(ROOT, "assets", "img-map.tsv")
    rows = [r.split("\t", 1) for r in open(path, encoding="utf-8").read().splitlines() if "\t" in r]
    names = dict(rows)
    taken = set(names.values())
    added = []
    for u in sorted({c["logo"] for t in tabs for c in t["cards"] if c.get("logo")}):
        if u in names:
            continue
        n = images.safe_name(u)
        if n in taken:
            sys.exit("logo name collision: %s" % n)
        if not images.fetch(u, os.path.join(images.IMG_DIR, n)):
            sys.exit("could not fetch %s" % u)
        names[u] = n
        taken.add(n)
        added.append("%s\t%s" % (u, n))
    if added:
        with open(path, "a", encoding="utf-8") as f:
            f.write("\n".join(added) + "\n")
        print("fetched %d logos" % len(added))
    return names


def card(c, i, logos, pa=False):
    """The card from the user's Figma (HRSMFFccdLgqf1YwD7oyc9, node 1:499), filled
    with the captured fields. Parts the capture lacks are left out: no sold line,
    no tags, no struck-through old yield ("was": the capture has none yet). The
    note strip stays when empty, as in the design."""
    sold = '\n          <p class="gp-ucard__sold">%s</p>' % e(c["sold"]) if c["sold"] else ""
    tags = ('\n    <div class="gp-ucard__tags">%s</div>' % "".join("<span>%s</span>" % e(t) for t in c["tags"])
            if c["tags"] else "")
    was = '\n      <s class="gp-ucard__was">%s%%</s>' % e(c["was"]) if c.get("was") else ""
    note = ('<img src="../assets/img/utsav-card-bolt.png" alt="" width="16" height="16"><span>%s</span>' % e(c["note"])
            if c["note"] else "")
    pa = "<small>p.a.</small>" if pa else ""
    return f'''<a class="gp-ucard" href="{e(UAT + c["href"])}" style="--i:{min(i, 11)}">
  <div class="gp-ucard__body">
    <div class="gp-ucard__id">
      <span class="gp-ucard__logo"><img src="../assets/img/{e(logos[c["logo"]])}" alt="" width="42" height="42"></span>
      <div>
        <h3 class="gp-ucard__issuer">{e(c["issuer"])}</h3>{sold}
      </div>
    </div>
    <div class="gp-ucard__rate">
      <p class="gp-ucard__rate-value">{e(c["rate"])}<span>%</span>{pa}</p>{was}
    </div>{tags}
    <dl class="gp-ucard__metrics">
      <div><dt>Tenure</dt><dd>{e(c["tenure"])}</dd></div>
      <div><dt>Payout</dt><dd>{e(c["payout"])}</dd></div>
      <div><dt>Rating</dt><dd>{e(c["rating"])}</dd></div>
    </dl>
  </div>
  <p class="gp-ucard__note">{note}</p>
</a>'''


# Two rows of five, as the live page splits them. One scroller holds both
# rows on phones, so they move together; from 768px the rows centre and wrap.
ROW_SPLIT = 5


def listing(tabs, logos, pa=False):
    buttons, panels = [], []
    for k, t in enumerate(tabs):
        on = k == 0
        slug = t["slug"].replace("_", "-")
        icon = TAB_ICONS.get(t["slug"], ALL_BONDS_ICON)
        buttons.append(
            f'''<button type="button" class="gp-pill" role="tab" id="tab-{slug}"
                      aria-controls="panel-{slug}" aria-selected="{str(on).lower()}"{"" if on else ' tabindex="-1"'}>
                <img src="../assets/img/{icon}" alt="" width="30" height="30">{e(t["label"])}
              </button>''')
        cards = "\n".join(card(c, i, logos, pa) for i, c in enumerate(t["cards"]))
        panels.append(
            f'''<div class="gp-panel{" is-on" if on else ""}" id="panel-{slug}"
             role="tabpanel" aria-labelledby="tab-{slug}"{"" if on else " hidden"}>
          <div class="gp-utsav-grid">
{cards}
          </div>
        </div>''')
    rows = [buttons[:ROW_SPLIT], buttons[ROW_SPLIT:]]
    strip = "\n".join('            <div class="gp-pills__row" role="none">\n              %s\n            </div>'
                      % "\n              ".join(r) for r in rows)
    return strip, "\n\n        ".join(panels)


def page(data, logos, name, v2=False):
    tabs = data["tabs"]
    buttons, panels = listing(tabs, logos, pa=v2)
    v = " gp-utsav-v2" if v2 else ""

    shell = open(os.path.join(HERE, SHELL_FROM), encoding="utf-8").read()
    head = shell[:shell.index(MAIN)]
    head = head.replace("<title>Refer &amp; Earn | GoldenPi</title>", "<title>Bond Utsav | GoldenPi</title>")
    head = head[:head.index("<!-- Refer & Earn, rebuilt")] + (
        "<!-- GENERATED by pages/_utsav.py from crawl/rendered/bond-utsav.tabs.json.\n"
        "     Edit the generator, not this file. Copy verbatim from\n"
        "     uatnew.goldenpi.com/bond-utsav (captured 2026-09-26); see content/bond-utsav.md. -->\n"
    ) + head[head.index('<meta name="description"'):]
    head = head.replace(
        head[head.index('<meta name="description"'):head.index(">", head.index('<meta name="description"')) + 1],
        '<meta name="description" content="Explore curated bond categories and invest in senior secured bonds on GoldenPi Bond Utsav.">')
    footer = shell[shell.index(FOOTER):shell.index("</footer>") + len("</footer>")]
    js = "\n".join(open(os.path.join(HERE, f), encoding="utf-8").read() for f in ("_tabs.js", "_reveal.js"))

    total = sum(t["count"] for t in tabs)
    main_html = f'''{MAIN}

  <!-- ============================================================== banner -->
  <!-- Their campaign banner, supplied as art by GoldenPi marketing. Full bleed
       under the header like the homepage hero, no breadcrumb (user,
       2026-09-26): the offer is baked into the image, so it is shown as it is,
       not re-typeset. Not a link on the live page. Alt text is theirs. -->
  <section class="gp-utsav-hero{v}">
    <picture class="gp-utsav-banner">
      <source media="(max-width: 767px)" srcset="../assets/img/bondUtsavBanner-mobile.webp" width="1634" height="1750">
      <img src="../assets/img/bondUtsavBanner-desktop.webp" alt="Bond Utsav promotional banner"
           width="5834" height="1880" fetchpriority="high">
    </picture>
  </section>

  <!-- ========================================================== categories -->
  <!-- DATA: {total} cards across {len(tabs)} tabs, API-driven and infinite-scrolled
       on the live page. Snapshot {data["captured"][:10]}, every tab driven by
       crawl/utsav_tabs.js. Cards link to the bond page the live card links to. -->
  <section class="gp-section gp-section--tight gp-utsav-listing gp-utsav-listing--pills{v}" aria-labelledby="utsav-heading">
    <div class="gp-shell">
      <div class="gp-section__head gp-section__head--marked gp-utsav-head" data-reveal>
        <h1 id="utsav-heading" class="gp-section__title">Select A Category</h1>
        <p class="gp-section__sub">Invest in Senior Secured Bonds and earn returns up to <span class="gp-hero__figure">13.8% p.a.</span></p>
      </div>

      <div>
        <div class="gp-pills">
          <div class="gp-pills__track" role="tablist" aria-label="Select A Category">
{buttons}
          </div>
        </div>

        {panels}
      </div>
    </div>
  </section>
</main>

'''
    out = head + main_html + footer + "\n\n<script>\n" + js + SCROLL_JS + (STUCK_JS if v2 else "") + "</script>\n\n</body>\n</html>\n"
    open(os.path.join(HERE, name), "w", encoding="utf-8").write(out)
    print("wrote %s  (%d tabs, %d cards)" % (name, len(tabs), total))


def main():
    data = json.load(open(os.path.join(ROOT, "crawl", "rendered", "bond-utsav.tabs.json"), encoding="utf-8"))
    logos = logo_names(data["tabs"])
    page(data, logos, "bond-utsav.html")
    page(data, logos, "bond-utsav2.html", v2=True)


if __name__ == "__main__":
    main()
