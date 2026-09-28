#!/usr/bin/env python3
"""Write one page per collection from uatnew.goldenpi.com/collections/<slug>:

    collections-all-bonds.html, collections-highly-rated.html, ... (11 pages)

The live pills are buttons that load /collections/<slug>, a separate page per
collection with its own intro, bonds and CMS copy, so here each pill is a link
to its sibling page. Pages cross-fade into each other (cross-document View
Transitions) with the title and pill row held in place.

Source is crawl/rendered/collections.tabs.json (crawl/collections_tabs.js):
every card after the list finished rendering, the intro after Read More, each
FAQ answer read by opening it, and the CMS blocks in document order.

Parts come from the finalised set: the Bond Utsav card (the user's Figma) and
pill, the corporate-bonds stat strip, the issuer page's section rail, and the
FAQ + Need Help layout. Page CSS is the COLLECTIONS block at the end of
final.css.

    python3 pages/_collections.py && python3 pages/_build.py
"""
import html
import json
import os
import re

import _prod

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
UAT = "https://uatnew.goldenpi.com"
esc = html.escape

DATA = json.load(open(os.path.join(ROOT, "crawl", "rendered", "collections.tabs.json"), encoding="utf-8"))
UTSAV = json.load(open(os.path.join(ROOT, "crawl", "rendered", "bond-utsav.tabs.json"), encoding="utf-8"))
IMG = _prod.IMG
local = _prod.local

# Live shows nothing at all for an empty NCD IPO list; Tax Free shows this.
# One empty state for both, their words.
EMPTY_TEXT = "Currently no bond available for this collection"


def page_name(slug):
    return "collections-%s.html" % slug


# ------------------------------------------------------------------ logos
# The collection cards carry no logo; the same bonds on Bond Utsav do. The two
# captures link a bond by different ids (GPID vs ISIN), so match on the slug
# and tenure date. IRFC and PFC come from the production logo set; anything
# else falls back to its initial in the logo slot.
def _key(h):
    m = re.search(r"tenureDate=([^&]+)", h)
    return h.split("?")[0].rstrip("/").split("/")[-1], m.group(1) if m else ""


LOGOS = {}
for t in UTSAV["tabs"]:
    for c in t["cards"]:
        LOGOS[_key(c["href"])] = c["logo"]
        LOGOS.setdefault((_key(c["href"])[0], ""), c["logo"])
BY_ISSUER = {
    "Indian Railway Finance Corporation Limited": "GPID100094.INDIAN-RAILWAY-FINANCE-CORPORATION-LIMITED.png",
    "Power Finance Corporation Limited": "GPID100099.POWER-FINANCE-CORPORATION-LTD.png",
}


def logo(c):
    u = LOGOS.get(_key(c["href"])) or LOGOS.get((_key(c["href"])[0], ""))
    if u:
        return '<img src="../assets/img/%s" alt="" width="42" height="42">' % local(u)
    if c["issuer"] in BY_ISSUER:
        return '<img src="../assets/img/%s" alt="" width="42" height="42">' % BY_ISSUER[c["issuer"]]
    return '<span class="gp-ucard__initial" aria-hidden="true">%s</span>' % esc(c["issuer"][:1])


# ------------------------------------------------------------------ cards
def card(c, i):
    """The Bond Utsav card (the user's Figma), filled with the collection
    card's fields: issuer, % sold, rate, tags, rating / payout / tenure and
    the note. The note strip keeps its height when empty, as on Utsav."""
    m = {k.title(): v for k, v in c["metrics"]}  # innerText reads their CSS uppercase
    rate = c["rate"].replace("%", "").strip()
    sold = '\n        <p class="gp-ucard__sold">%s</p>' % esc(c["meta"]) if c["meta"] else ""
    tags = ('\n    <div class="gp-ucard__tags">%s</div>' % "".join("<span>%s</span>" % esc(t) for t in c["tags"])
            if c["tags"] else "")
    note = c["note"].lstrip("⚡").strip()
    note = ('<img src="../assets/img/utsav-card-bolt.png" alt="" width="16" height="16"><span>%s</span>' % esc(note)
            if note else "")
    return '''<a class="gp-ucard" href="%s" style="--i:%d">
  <div class="gp-ucard__body">
    <div class="gp-ucard__id">
      <span class="gp-ucard__logo">%s</span>
      <div>
        <h3 class="gp-ucard__issuer">%s</h3>%s
      </div>
    </div>
    <div class="gp-ucard__rate">
      <p class="gp-ucard__rate-value">%s<span>%%</span></p>
    </div>%s
    <dl class="gp-ucard__metrics">
      <div><dt>Rating</dt><dd>%s</dd></div>
      <div><dt>Payout</dt><dd>%s</dd></div>
      <div><dt>Tenure</dt><dd>%s</dd></div>
    </dl>
  </div>
  <p class="gp-ucard__note">%s</p>
</a>''' % (esc(UAT + c["href"]), min(i, 11), logo(c), esc(c["issuer"]), sold, esc(rate), tags,
           esc(m.get("Rating", "")), esc(m.get("Payout", "")), esc(m.get("Tenure", "")), note)


STRIP = """      <!-- Their "Golden Experience" strip, which the live list repeats after
           every six cards; shown once here, after the first six. -->
      <div class="gp-colstrip">
        <p class="gp-divider">The Golden Experience of Investing</p>
        <div class="gp-stats">
          <div class="gp-stats__item"><img src="../assets/img/trophy.png" alt="" width="36" height="36"><span class="gp-stats__value">Zero Defaults</span></div>
          <div class="gp-stats__item"><img src="../assets/img/shield.png" alt="" width="36" height="36"><span class="gp-stats__value">Sebi Registered</span></div>
          <div class="gp-stats__item"><img src="../assets/img/5percent.png" alt="" width="36" height="36"><span class="gp-stats__value">Curated Bonds</span></div>
          <div class="gp-stats__item"><img src="../assets/img/users.png" alt="" width="36" height="36"><span class="gp-stats__value">18 lacs+ Users</span></div>
        </div>
      </div>"""


def listing(cards):
    if not cards:
        return """      <div class="gp-empty-state gp-colempty" role="status">
        <img src="../assets/img/empty-state-icon.svg" alt="No bonds" width="120" height="120">
        <p>%s</p>
      </div>""" % EMPTY_TEXT
    first = "\n".join(card(c, i) for i, c in enumerate(cards[:6]))
    rest = "\n".join(card(c, i) for i, c in enumerate(cards[6:]))
    few = " gp-colgrid--one" if len(cards) == 1 else ""
    out = '      <div class="gp-colgrid%s">\n%s\n      </div>' % (few, first)
    if rest:
        out += "\n" + STRIP + '\n      <div class="gp-colgrid">\n%s\n      </div>' % rest
    return out


# ------------------------------------------------------------- rich text
def clean(h):
    """Their CMS rich text, kept as markup, with the editor's attributes and
    empty spacer paragraphs removed. Links stay where they point."""
    h = re.sub(r"<button[^>]*>.*?</button>", "", h, flags=re.S)
    h = re.sub(r'\s(class|style|value|id|data-[\w-]+)="[^"]*"', "", h)
    h = re.sub(r"<p>\s*(<br>)?\s*</p>", "", h)
    h = re.sub(r"<(/?)h1>", r"<\1h2>", h)
    h = re.sub(r'<a href="(/[^"]*)"', r'<a href="%s\1"' % UAT, h)
    h = h.replace("<a ", '<a class="underline" ')
    return h.strip()


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def body_blocks(t):
    out = []
    for b in t["body"]:
        if b["kind"] == "about":
            out.append(_prod.section('      <div class="gp-colcopy">\n%s\n      </div>' % clean(b["html"])))
        elif b["kind"] == "links":
            links = re.findall(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', b["html"], re.S)
            title = re.search(r'cms-link-list__title[^>]*>(.*?)<', b["html"], re.S)
            items = "\n".join(
                '          <li><a href="%s">%s<span aria-hidden="true">&rsaquo;</span></a></li>'
                % (esc(href if href.startswith("http") else UAT + href), esc(re.sub("<[^>]+>", "", lab).strip()))
                for href, lab in links)
            out.append(_prod.section("""      <div class="gp-collinks">
        <h2 class="gp-section__title text-left">%s</h2>
        <ul>
%s
        </ul>
      </div>""" % (esc(title.group(1).strip()) if title else "", items)))
        elif b["kind"] == "article":
            nav = "\n".join('          <a%s href="%s">%s</a>' % (' class="is-on"' if k == 0 else "", esc(h), esc(lab))
                            for k, (h, lab) in enumerate(b["nav"]))
            secs = "\n".join('          <section id="%s">\n%s\n          </section>' % (esc(s["id"]), clean(s["html"]))
                             for s in b["sections"])
            out.append(_prod.section("""      <div class="gp-navlayout">
        <nav class="gp-sidenav" aria-label="Page sections">
%s
        </nav>
        <div class="gp-article">
%s
        </div>
      </div>""" % (nav, secs)))
        elif b["kind"] == "faq":
            items = [(f["q"], clean(f["a"])) for f in t["faqs"]]
            out.append(_prod.faq(esc(b["title"]), items))
    return "".join(out)


# ------------------------------------------------------------------- page
HEAD_NOTE = ("Collection page, rebuilt from uatnew.goldenpi.com/collections/{slug} "
             "on the finalised components.\n     Generated by pages/_collections.py from "
             "crawl/rendered/collections.tabs.json (captured {snap}).")

EXTRA = """
<script>
// The open pill scrolls into view on phones, where the row is a scroller.
(function () {
  var on = document.querySelector('.gp-colpills [aria-current="page"]');
  if (on && on.scrollIntoView) on.scrollIntoView({ block: 'nearest', inline: 'center' });
})();
// Section rail: mark the section in view. The links work without it.
(function () {
  var nav = document.querySelector('.gp-sidenav');
  if (!nav || !('IntersectionObserver' in window)) return;
  var links = [].slice.call(nav.querySelectorAll('a'));
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      links.forEach(function (a) { a.classList.toggle('is-on', a.hash === '#' + e.target.id); });
    });
  }, { rootMargin: '-30% 0px -60% 0px' });
  links.forEach(function (a) { var s = document.querySelector(a.hash); if (s) io.observe(s); });
})();
</script>
"""


def build(slug):
    t = DATA["tabs"][slug]
    pill = ['              <a class="gp-pill" href="%s"%s><img src="../assets/img/%s" alt="" width="30" height="30">%s</a>'
            % (page_name(p["slug"]), ' aria-current="page"' if p["slug"] == slug else "", local(p["icon"]), esc(p["label"]))
            for p in DATA["pills"]]
    # Always two rows, never wrapping, in one scroller so both rows slide
    # together (phones and desktop alike).
    half = (len(pill) + 1) // 2
    pills = "\n".join('            <div class="gp-colpills__row">\n%s\n            </div>' % "\n".join(r)
                      for r in (pill[:half], pill[half:]))
    intro = clean(t["introHtml"])
    count = ""
    if t["cards"]:
        count = """      <div class="gp-colbar">
        <p><b>%s</b></p>
        <p class="t-muted">%s</p>
      </div>""" % (esc(t["count"]), esc(t["sort"]))

    body = """
  <!-- ============================================================== top -->
  <section class="gp-hero gp-colhero">
    <div class="gp-shell pt-6 pb-2">
      <nav class="t-small t-muted mb-6" aria-label="Breadcrumb">
        <a href="index.html" class="hover:text-ink">Home</a>
        <span class="mx-1.5">&rsaquo;</span>
        <a href="collections-all-bonds.html" class="hover:text-ink">Collections</a>
        <span class="mx-1.5">&rsaquo;</span>
        <span class="text-ink font-medium">%s</span>
      </nav>

      <div class="gp-collayout">
        <div class="gp-colmain">
          <h1 class="t-h1 gp-coltitle">%s</h1>
          <div class="gp-colintro">
%s
          </div>

          <!-- Each pill loads its own collection page, as on the live site. -->
          <nav class="gp-colpills" aria-label="Collection filters">
            <div class="gp-colpills__track">
%s
            </div>
          </nav>

%s
          <!-- DATA: bond cards, API-driven. Snapshot %s. -->
%s
        </div>

        <aside class="gp-colside" aria-label="More from GoldenPi">
          <img class="gp-colside__banner" src="../assets/img/Banner2.png" width="840" height="1000"
               alt="No Closing Bell for Smart Investors. Now Invest 24 hrs, 7 days, 365 days. Yield up to 13.40%% p.a. Min. Investment &#8377;30,000/-. Credit rating upto AA. Download on the App Store, get it on Google Play.">
          <a class="gp-colside__card" href="https://www.youtube.com/watch?v=QnYvSdEFPdo&amp;vl=en-IN&amp;themeRefresh=1" target="_blank" rel="noopener noreferrer">
            <span class="gp-colside__play" aria-hidden="true"><img src="../assets/img/play-icon.svg" alt="" width="14" height="14"></span>
            <span>
              <span class="gp-colside__title">How Bond Investments Work?</span>
              <span class="gp-colside__text">Watch a 2-minute explainer video on bond return &amp; payout for Investment</span>
            </span>
          </a>
          <div class="gp-colside__card gp-colside__card--refer">
            <span>
              <span class="gp-colside__title">Refer &amp; Earn <img src="../assets/img/refer-earn-gift.png" alt="" width="24" height="24"></span>
              <span class="gp-colside__text">Invite your friends &amp; Earn up to 5Lacs</span>
            </span>
            <a class="gp-colside__cta" href="refer-and-earn.html">Refer Now!</a>
          </div>
        </aside>
      </div>
    </div>
  </section>
""" % (esc(t["title"]), esc(t["title"]), intro, pills, count, DATA["captured"], listing(t["cards"]))
    body += body_blocks(t)

    head = _prod.HEAD.format(title=esc(t["docTitle"]), desc=esc(t["metaDesc"]), note="", slug="x", snap="")
    head = re.sub(r"<!-- .*? -->", "<!-- %s -->" % HEAD_NOTE.format(slug=slug, snap=DATA["captured"]), head, count=1, flags=re.S)
    # Cross-document View Transitions: switching pills cross-fades the page
    # while the title and pill row hold still. Both pages must opt in, so it
    # lives here rather than in final.css.
    head = head.replace("</head>", """<style>
  @view-transition { navigation: auto; }
  .gp-coltitle { view-transition-name: col-title; }
  .gp-colpills { view-transition-name: col-pills; }
  @media (prefers-reduced-motion: reduce) { @view-transition { navigation: none; } }
</style>
</head>""")
    out = head + _prod.SHELL + '<main id="main-content">\n' + body + "\n</main>\n\n" + _prod.FOOTER + "\n" + _prod.SCRIPTS + EXTRA
    out += "\n</body>\n</html>\n"
    open(os.path.join(HERE, page_name(slug)), "w", encoding="utf-8").write(out)
    print("wrote pages/%s  (%d bonds)" % (page_name(slug), len(t["cards"])))


if __name__ == "__main__":
    for p in DATA["pills"]:
        build(p["slug"])
