#!/usr/bin/env python3
"""investor-resources.html: goldenpi.com/investor-resources in the index.html
design (its head, header and dark footer, read from the generated index.html).

Copy comes from the capture, crawl/rendered/prod_investor-resources.html
(node crawl/snap.js --prod /investor-resources, 2026-10-07): the title, the
intro line, the three group headings and the 18 card labels. On goldenpi.com
the cards are script-driven, not links; each one here points at the same
document the goldenpi.com footer links under that name (footer-bonds.html's
"Important Information" chips, from the production capture). The capture's
Note to Investors and SMARTODR text is goldenpi.com's footer, which index's
own footer already carries, so it is not repeated in the page body.

    python3 pages/_convert.py && python3 pages/_build.py && python3 pages/_investor_resources.py
"""
import html
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CAP = os.path.join(ROOT, "crawl", "rendered", "prod_investor-resources.html")
OUT = os.path.join(HERE, "investor-resources.html")
esc = html.escape


def key(label):
    return re.sub(r"[^a-z0-9]", "", html.unescape(label).lower())


def links():
    """{normalised label: href} from footer-bonds' Important Information chips."""
    h = open(os.path.join(HERE, "footer-bonds.html"), encoding="utf-8").read()
    band = h[h.index('id="ft-info"'):h.index('id="ft-links"')]
    return {key(t): href for href, t in re.findall(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>', band)}


def capture():
    h = open(CAP, encoding="utf-8").read()
    h = h[h.index("<investor-resources>"):h.index('<div class="copy-right-tnc">')]
    title = html.unescape(re.search(r"<h1>(.*?)</h1>", h).group(1)).strip()
    intro = html.unescape(re.search(r"</h1><p>(.*?)</p>", h).group(1)).strip()
    groups = []
    for head, grid in re.findall(r'<h2 class="section-heading">(.*?)</h2><div class="links-grid">(.*?)</div></div>', h, re.S):
        cards = [html.unescape(c).strip() for c in re.findall(r'<span class="link-title">(.*?)</span>', grid)]
        groups.append((html.unescape(head).strip(), cards))
    if len(groups) != 3 or sum(len(c) for _, c in groups) != 18:
        raise SystemExit("investor-resources: capture changed (%d groups)" % len(groups))
    return title, intro, groups


def card(label, href, n):
    ext = href.startswith("http")
    kind = "ZIP" if href.endswith(".zip") else "PDF" if href.endswith(".pdf") else "Page"
    icon = {"ZIP": "ph-file-zip", "PDF": "ph-file-pdf", "Page": "ph-file-text"}[kind]
    arrow = "ph-download-simple" if kind == "ZIP" else "ph-arrow-up-right" if ext else "ph-arrow-right"
    target = ' target="_blank" rel="noopener noreferrer"' if ext else ""
    return ('        <a class="ir-card" href="%s"%s style="--i:%d">\n'
            '          <span class="ir-card__ico" aria-hidden="true"><i class="ph %s"></i></span>\n'
            '          <span class="ir-card__txt"><span class="ir-card__t">%s</span><span class="ir-card__k">%s</span></span>\n'
            '          <i class="ph %s ir-card__go" aria-hidden="true"></i>\n'
            '        </a>' % (esc(href), target, n, icon, esc(label), kind, arrow))


def body(title, intro, groups, hrefs):
    secs = []
    for g, (head, cards) in enumerate(groups):
        missing = [c for c in cards if key(c) not in hrefs]
        if missing:
            raise SystemExit("investor-resources: no footer link for %s" % missing)
        grid = "\n".join(card(c, hrefs[key(c)], n) for n, c in enumerate(cards))
        secs.append('    <section class="ir-group" aria-labelledby="ir-g%d" data-reveal>\n'
                    '      <h2 class="ir-group__title" id="ir-g%d">%s</h2>\n'
                    '      <div class="ir-grid">\n%s\n      </div>\n'
                    '    </section>' % (g, g, esc(head), grid))
    return ('  <!-- ======================================================== investor resources -->\n'
            '  <!-- Copy: goldenpi.com/investor-resources, captured 2026-10-07. Links: the goldenpi.com\n'
            '       footer\'s documents of the same name (the live cards are script-driven). -->\n'
            '  <div class="gp-shell ir">\n'
            '    <nav class="ir-crumbs t-small" aria-label="Breadcrumb">\n'
            '      <a href="index.html">Home</a><span aria-hidden="true">&rsaquo;</span>'
            '<span aria-current="page">%s</span>\n'
            '    </nav>\n'
            '    <header class="ir-head">\n'
            '      <h1 class="ir-title">%s</h1>\n'
            '      <p class="ir-intro">%s</p>\n'
            '    </header>\n'
            '%s\n'
            '  </div>\n' % (esc(title), esc(title), esc(intro), "\n".join(secs)))


STYLE = """<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/regular/style.css">
<style>
/* investor-resources: index.html's tokens and type, one radius scale
   (cards 16px, icon tiles 12px), one gold accent. */
.ir { padding-top: 24px; padding-bottom: 72px; }
.ir-crumbs { display: flex; align-items: center; gap: 8px; color: var(--subtext); }
.ir-crumbs a { color: inherit; text-decoration: none; }
.ir-crumbs a:hover { color: var(--app-heading-color); }
.ir-crumbs [aria-current] { color: var(--app-heading-color); font-weight: 500; }
.ir-head { max-width: 62ch; margin: 28px 0 48px; }
.ir-title { margin: 0; color: var(--app-heading-color); font-size: clamp(32px, 4.4vw, 48px); line-height: 1.08; font-weight: 700; letter-spacing: -0.02em; }
.ir-intro { margin: 14px 0 0; color: var(--subtext); font-size: 17px; line-height: 1.6; }
.ir-group + .ir-group { margin-top: 48px; }
.ir-group__title { display: flex; align-items: center; gap: 12px; margin: 0 0 18px; color: var(--app-heading-color); font-size: 20px; line-height: 28px; font-weight: 700; }
.ir-group__title::after { content: ""; flex: 1; height: 1px; background: var(--light-stroke, #e7e3d9); }
.ir-grid { display: grid; gap: 14px; }
@media (min-width: 640px) { .ir-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (min-width: 1024px) { .ir-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; } }
.ir-card {
  display: grid; grid-template-columns: 44px minmax(0, 1fr) 20px; align-items: center; gap: 14px;
  min-height: 76px; padding: 14px 18px 14px 16px; border: 1px solid #ece6d6; border-radius: 16px;
  background: #fff; color: var(--app-heading-color); text-decoration: none;
  box-shadow: 0 1px 2px rgba(50, 40, 17, 0.04);
  transition: border-color 0.2s ease, box-shadow 0.25s ease, transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}
.ir-card:hover { border-color: #d4af37; box-shadow: 0 14px 28px -20px rgba(138, 101, 32, 0.5); transform: translateY(-2px); }
.ir-card:active { transform: translateY(0); }
.ir-card:focus-visible { outline: 2px solid #d4af37; outline-offset: 3px; }
.ir-card__ico { display: grid; place-items: center; width: 44px; height: 44px; border-radius: 12px; background: #fbf5e3; color: #8a6520; font-size: 22px; }
.ir-card__txt { display: flex; flex-direction: column; gap: 2px; min-width: 0; }
.ir-card__t { font-size: 15.5px; line-height: 1.35; font-weight: 600; }
.ir-card__k { color: var(--subtext); font-size: 11px; font-weight: 700; letter-spacing: 0.08em; }
.ir-card__go { color: #b9a77e; font-size: 18px; transition: color 0.2s ease, transform 0.25s cubic-bezier(0.16, 1, 0.3, 1); }
.ir-card:hover .ir-card__go { color: #8a6520; transform: translate(2px, -2px); }
@media (max-width: 639px) {
  .ir { padding-top: 16px; padding-bottom: 48px; }
  .ir-head { margin: 20px 0 32px; }
  .ir-intro { font-size: 15px; }
  .ir-group + .ir-group { margin-top: 36px; }
  .ir-card { min-height: 68px; }
}
@media (prefers-reduced-motion: reduce) { .ir-card, .ir-card__go { transition: none; } .ir-card:hover { transform: none; } }
</style>
"""


def main():
    title, intro, groups = capture()
    index = open(os.path.join(HERE, "index.html"), encoding="utf-8").read()
    top = index[:index.index('<main id="main-content">')]
    bottom = index[index.index("</main>"):]
    top = re.sub(r"<title>.*?</title>", "<title>%s | GoldenPi</title>" % esc(title), top, count=1, flags=re.S)
    top = re.sub(r'<meta name="description" content="[^"]*">',
                 '<meta name="description" content="%s">' % esc(intro), top, count=1)
    top = re.sub(r'<meta property="og:title" content="[^"]*">',
                 '<meta property="og:title" content="%s | GoldenPi">' % esc(title), top, count=1)
    top = re.sub(r'<meta property="og:description" content="[^"]*">',
                 '<meta property="og:description" content="%s">' % esc(intro), top, count=1)
    top = top.replace(' aria-current="page"', "")
    top = top.replace("</head>", "<!-- Generated by pages/_investor_resources.py from the goldenpi.com capture and "
                      "index.html's shell; do not edit. -->\n" + STYLE + "</head>", 1)
    page = top + '<main id="main-content">\n' + body(title, intro, groups, links()) + bottom
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page)
    print("%s  %d bytes" % (os.path.relpath(OUT, ROOT), len(page)))


if __name__ == "__main__":
    main()
