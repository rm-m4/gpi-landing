#!/usr/bin/env python3
"""user-corporate-bonds2.html: the logged-in bonds page and the Collections
pages merged into one place to explore bonds.

user-corporate-bonds.html asks the user to pick bonds three different ways
(the deals tabs, the filter list, the collection cards) and then sends them
to eleven separate Collections pages. Here the collections are the one
picker: a tab per collection, each holding that collection's captured bonds,
count and sort. The deals tabs, filter list and collection cards
go, and so does the banner; the page's other sections (quiz, live IPOs, explainer, guides, trust,
FAQ) stay as they are.

Sources: crawl/rendered/collections.tabs.json (uatnew, 2026-09-28) for the
collections, and pages/_user.py (goldenpi.com, 2026-09-26) for the rest.

    python3 pages/_explore_bonds.py
"""
import importlib.util
import os
import re

import _user as U

HERE = os.path.dirname(os.path.abspath(__file__))
# "_collections" is also a CPython built-in, which a plain import finds first.
_spec = importlib.util.spec_from_file_location("collections_page", os.path.join(HERE, "_collections.py"))
K = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(K)
OUT = os.path.join(HERE, "user-corporate-bonds2.html")
esc = U.esc
SHOWN = 6  # cards before "View All"; the rest open in place


def panel(p, on):
    t = K.DATA["tabs"][p["slug"]]
    cards = t["cards"]
    if cards:
        grid = "\n".join(K.card(c, i) for i, c in enumerate(cards[:SHOWN]))
        body = '        <div class="ex__grid">\n%s\n        </div>\n' % grid
        if len(cards) > SHOWN:
            rest = "\n".join(K.card(c, i) for i, c in enumerate(cards[SHOWN:]))
            body += ('        <details class="ex__more">\n'
                     '          <summary>View All</summary>\n'
                     '          <div class="ex__grid">\n%s\n          </div>\n'
                     '        </details>\n' % rest)
        meta = ('          <p class="ex__meta"><b>%s</b><span>%s</span></p>\n'
                % (esc(t["count"]), esc(t["sort"])))
    else:
        # NCD IPOs are listed live further down; the empty state points there.
        more = (' <a href="#live-ipos">Live NCD IPOs</a>' if p["slug"] == "ncd-ipo" else "")
        body = ('        <div class="ex__empty" role="status">\n'
                '          <img src="../assets/img/empty-state-icon.svg" alt="" width="96" height="96">\n'
                '          <p>%s</p>\n'
                '          <p class="ex__empty-link">%s</p>\n'
                '        </div>\n' % (K.EMPTY_TEXT, more.strip()))
        meta = ""
    return ('      <div class="ex__panel" role="tabpanel" id="ex-%s" aria-labelledby="ex-tab-%s"%s>\n'
            '%s%s'
            '      </div>' % (p["slug"], p["slug"], "" if on else " hidden",
                             '        <div class="ex__bar">\n%s        </div>\n' % meta if meta else "", body))


def explorer():
    tabs = "\n".join(
        '        <button type="button" class="ex__tab" role="tab" id="ex-tab-%s" aria-controls="ex-%s" '
        'aria-selected="%s" tabindex="%d"><img src="../assets/img/%s" alt="" width="28" height="28">'
        '<span>%s</span></button>'
        % (p["slug"], p["slug"], "true" if k == 0 else "false", 0 if k == 0 else -1, K.local(p["icon"]),
           esc(p["label"]))
        for k, p in enumerate(K.DATA["pills"]))
    panels = "\n".join(panel(p, k == 0) for k, p in enumerate(K.DATA["pills"]))
    return ('  <!-- ========================================================== explorer -->\n'
            '  <!-- The Collections pages, folded in: one tab per collection.\n'
            '       DATA: cards, counts and sort, uatnew collections %s. -->\n'
            '  <section class="ex" id="collections" aria-label="Bond collections">\n'
            '    <div class="gp-shell">\n'
            '      <div class="ex__rail" role="tablist" aria-label="Bond collections">\n%s\n      </div>\n'
            '%s\n'
            '    </div>\n'
            '  </section>\n' % (K.DATA["captured"], tabs, panels))


STYLE = """<style>
/* user-corporate-bonds2: the collections explorer. Cards are the shared
   .gp-ucard; everything else is this block. */
.ex { padding: 40px 0 8px; }
.ex__rail {
  display: flex; gap: 8px; overflow-x: auto; scroll-snap-type: x proximity; scrollbar-width: none;
  margin: 0 -20px; padding: 2px 20px 14px;
}
.ex__rail::-webkit-scrollbar { display: none; }
.ex__rail { scroll-padding-inline: 20px; }
/* Desktop: all eleven in view, wrapping; phones keep the scroller. */
@media (min-width: 768px) { .ex__rail { flex-wrap: wrap; overflow: visible; margin: 0; padding: 2px 0 14px; } }
.ex__tab {
  flex: none; scroll-snap-align: start; display: inline-flex; align-items: center; gap: 8px;
  min-height: 44px; padding: 6px 14px 6px 8px; border: 1px solid var(--light-stroke); border-radius: 999px;
  background: var(--white); color: var(--app-heading-color); font: inherit; font-size: 14px; font-weight: 500;
  cursor: pointer; transition: background-color 0.2s ease, border-color 0.2s ease, color 0.2s ease;
}
.ex__tab img { width: 28px; height: 28px; object-fit: contain; }
.ex__tab:hover { border-color: #d3ad5c; }
.ex__tab:focus-visible { outline: 2px solid var(--mustard); outline-offset: 2px; }
.ex__tab[aria-selected="true"] { background: var(--app-heading-color); border-color: var(--app-heading-color); color: #fff; }

.ex__panel { padding-top: 12px; }
.ex__bar { display: flex; flex-wrap: wrap; align-items: flex-end; justify-content: space-between; gap: 8px 24px; margin-bottom: 18px; }
.ex__meta { flex: 1; display: flex; flex-wrap: wrap; align-items: baseline; justify-content: space-between; gap: 4px 12px; margin: 0; font-size: 13px; line-height: 18px; color: var(--subtext); }
.ex__meta b { color: var(--app-heading-color); font-size: 14px; }

.ex__grid { display: grid; gap: 16px; }
@media (min-width: 700px) { .ex__grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px; } }
@media (min-width: 1100px) { .ex__grid { grid-template-columns: repeat(3, minmax(0, 1fr)); } }

.ex__more { margin-top: 20px; }
.ex__more > summary {
  display: flex; width: max-content; margin: 0 auto; padding: 10px 24px; border: 1px solid #d3ad5c; border-radius: 999px;
  color: var(--bronze, #8a6520); font-size: 14px; font-weight: 700; cursor: pointer; list-style: none;
}
.ex__more > summary::-webkit-details-marker { display: none; }
.ex__more > summary:focus-visible { outline: 2px solid var(--mustard); outline-offset: 2px; }
.ex__more[open] > summary { display: none; }

.ex__empty { display: flex; flex-direction: column; align-items: center; gap: 8px; padding: 40px 16px; border-radius: 24px; background: var(--white); text-align: center; }
.ex__empty p { margin: 0; color: var(--app-heading-color); font-size: 16px; font-weight: 500; }
.ex__empty-link a { color: var(--bronze, #8a6520); font-weight: 700; text-decoration: underline; }
.ex__empty-link:empty { display: none; }

@media (max-width: 639px) {
  .ex { padding-top: 28px; }
}
@media (prefers-reduced-motion: no-preference) {
  .ex__panel:not([hidden]) .gp-ucard { animation: gp-row-in 0.45s ease both; animation-delay: calc(var(--i, 0) * 40ms); }
}
@media (prefers-reduced-motion: reduce) { .ex__tab { transition: none; } }
</style>
"""

SCRIPT = """<script>
// Collections explorer tabs. Without this, All Bonds is the open panel.
(function () {
  var tabs = [].slice.call(document.querySelectorAll('.ex__tab'));
  function select(n, focus) {
    tabs.forEach(function (t, k) {
      var on = k === n;
      t.setAttribute('aria-selected', String(on));
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
    });
    if (focus) tabs[n].focus();
    tabs[n].scrollIntoView({ block: 'nearest', inline: 'nearest' });
  }
  tabs.forEach(function (t, k) {
    t.addEventListener('click', function () { select(k); });
    t.addEventListener('keydown', function (e) {
      var i = { ArrowRight: (k + 1) % tabs.length, ArrowLeft: (k - 1 + tabs.length) % tabs.length,
                Home: 0, End: tabs.length - 1 }[e.key];
      if (i === undefined) return;
      e.preventDefault();
      select(i, true);
    });
  });
})();
</script>
"""


def main():
    text = U.md("corporate-bonds")
    title = re.search(r"\*\*Title:\*\* (.+)", text).group(1)
    desc = re.search(r"\*\*Meta description:\*\* (.+)", text).group(1)
    top, bottom = U.shell(esc(title), U.html.escape(desc), "bonds")
    top = top.replace("<!-- Post-login page, generated by pages/_user.py",
                      "<!-- Post-login bonds page merged with the Collections pages, generated by\n"
                      "     pages/_explore_bonds.py; base page by pages/_user.py", 1)
    ipos = U.live_ipos().replace('<section data-reveal class="', '<section id="live-ipos" data-reveal class="', 1)
    body = "\n".join([
        U.greet("Hi %s, Explore Corporate Bonds" % U.NAME,
                "Discover reliable income and stable capital growth with Corporate Bond Investments",
                "post-login-ncd.svg"),
        explorer(),
        ipos,
        U.quiz(),
        U.explainer("What is a Corporate Bond?",
                    ["Corporate Bonds are debt securities regulated by SEBI and issued by corporations "
                     "to raise capital from investors.",
                     "These bonds offer higher yields compared to other fixed income securities, "
                     "offering relatively attractive returns to investors."],
                    ["Debt Security", "Yield", "Fixed Income Security"], "post-login-ncd-info.svg"),
        U.faq("corporate-bonds"),
    ])
    page = U.F.primary_ctas(top + "\n" + body + bottom)
    page = page.replace("</head>", STYLE + "</head>", 1).replace("</body>", SCRIPT + "</body>", 1)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page)
    print("%s  %d bytes" % (os.path.relpath(OUT, os.path.dirname(HERE)), len(page)))


if __name__ == "__main__":
    main()
