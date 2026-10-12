"""home-premium44.html: the three home-premium concepts stacked in one page,
every section of each, in order (1, then 2, then 3), nothing dropped or edited.
For export to Figma, where the sections are reworked.

Chrome (head, navbar, footer, scripts) is home-premium2's. Its CSS already
holds 1's (the shared rules); 3's own rules are appended. 3 was designed on a
dark page, so its sections sit in one dark band in place of body.h3-page.
Ids in 2 and 3 get a -2 / -3 suffix (they repeat 1's), and their h1s become
h2s so the page keeps one h1 (both are styled by class, so nothing moves).
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "home-premium44.html")

BAND_CSS = """
/* ---- home-premium44: 3's sections as one dark band (3's page ground and text) ---- */
.h4-band { background: #0b0906; color: #c9bc9c; }
"""


def read(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return f.read()


def one(pattern, page, what):
    m = re.search(pattern, page, re.S)
    if not m:
        raise SystemExit("%s not found, re-check the source page" % what)
    return m


def inner_main(page, name):
    return one(r'<main id="main-content">(.*?)</main>', page, name + " <main>").group(1)


def suffix(html, n):
    """Ids, and what points at them, get -n; the h1 becomes an h2."""
    html = re.sub(r'\b(id|for|aria-labelledby|aria-describedby|aria-controls)="([^"]+)"',
                  lambda m: '%s="%s"' % (m.group(1), " ".join(x + "-%d" % n for x in m.group(2).split())), html)
    html = re.sub(r'href="#([^"]+)"', r'href="#\1-%d"' % n, html)
    return re.sub(r"<h1\b(.*?)</h1>", r"<h2\1</h2>", html, flags=re.S)


def main():
    p1, p2, p3 = read("home-premium.html"), read("home-premium11.html"), read("home-premium3.html")

    # 3's own CSS follows its marker; its body-level dark rules give way to the band
    css3 = one(r"/\* ---- home-premium3:.*?(?=</style>)", p3, "home-premium3 CSS").group(0)
    css3 = re.sub(r"body\.h3-page \{[^}]*\}\s*|\.h3-page main \{[^}]*\}\s*", "", css3)

    stacked = (inner_main(p1, "home-premium") + suffix(inner_main(p2, "home-premium2"), 2)
               + '<div class="h4-band">%s</div>' % suffix(inner_main(p3, "home-premium3"), 3))
    page = re.sub(r'(<main id="main-content">).*?(</main>)', lambda m: m.group(1) + stacked + m.group(2),
                  p2, count=1, flags=re.S)
    page = re.sub(r"(/\* ---- home-premium2:.*?)(</style>)", lambda m: m.group(1) + css3 + BAND_CSS + m.group(2),
                  page, count=1, flags=re.S)
    if "h4-band {" not in page or page.count("<h1") != 1:
        raise SystemExit("merge did not apply, re-check home-premium11")

    ids = re.findall(r'\sid="([^"]+)"', page)
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        raise SystemExit("duplicate ids after merge: %s" % dup)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page)
    print("pages/home-premium44.html  %d bytes" % len(page))


if __name__ == "__main__":
    main()
