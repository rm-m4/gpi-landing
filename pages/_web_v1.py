#!/usr/bin/env python3
"""web-v1/: the final logged-in pages as one self-contained folder, for
stakeholders to review (zip it, or serve it anywhere). Replicas: the pages in
pages/ are only read, never changed.

Every page sits flat in web-v1/ under a short name, with its own copy of the
assets it uses (web-v1/assets/, same layout as assets/). Links between the
pages point at each other; a link to a page outside the set keeps its look
but loses its href, so a reviewer never lands on a missing page.

bond-utsav4 still carries the guest navbar; its copy takes the logged-in one,
as _prototype.py gives bond-utsav5 (Bond Utsav's own footer stays).

Also writes the Web V1 tab of all-pages.html (the panel between its markers).

    python3 pages/_prototype.py && python3 pages/_web_v1.py
"""
import os
import re
import shutil
from urllib.parse import unquote

import _prototype as P

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "web-v1")

# in pill order, as all-pages.html lists them
_AP = open(os.path.join(HERE, "all-pages.html"), encoding="utf-8").read()
COLLECTIONS = list(dict.fromkeys(re.findall(r'<a href="(collections2-[a-z0-9-]+\.html)"', _AP)))
# source page -> name in web-v1, grouped as the Web V1 tab lists them
GROUPS = [
    ("Home and bonds", [("user-explore-app7.html", "explore.html", "Explore (home)"),
                        ("bond-details7.html", "bond-details.html", "Bond details"),
                        ("ipo-details.html", "ipo-details.html", "NCD IPO details")]),
    ("Collections", [(f, f.replace("collections2-", "collections-"), None) for f in COLLECTIONS]),
    ("Fixed deposits", [("user-fixed-deposits-app2.html", "fixed-deposits.html", "Fixed Deposits"),
                        ("fd-details2.html", "fd-details.html", "FD details")]),
    ("Pre-login", [("explore-prelogin.html", "explore-prelogin.html", "Explore (pre-login)"),
                   ("signup.html", "signup.html", "Sign up")]),
    ("Account", [("portfolio.html", "portfolio.html", "Portfolio"),
                 ("bond-utsav4.html", "bond-utsav.html", "Bond Utsav"),
                 ("refer-and-earn-with-referral.html", "refer-and-earn.html", "Refer &amp; Earn")]),
]
MAP = {src: dst for _, rows in GROUPS for src, dst, _ in rows}
# other names the pages use for the same destinations (the prototype's map,
# plus the Bond Utsav and Refer & Earn pages these replace)
ALIAS = dict({k: MAP[v] for k, v in P.HREF.items() if v in MAP},
             **{"bond-utsav5.html": "bond-utsav.html", "bond-utsav.html": "bond-utsav.html",
                "refer-and-earn.html": "refer-and-earn.html"})
LINK = re.compile(r'\shref="([a-z0-9-]+\.html)(#[^"]*)?"')
ASSET = re.compile(r'\.\./assets/([^"\'()\s,]+)')
CSS_URL = re.compile(r'url\(\s*["\']?(?!data:|https?:|#)([^"\')]+)["\']?\s*\)')


def label(src):
    """The page's name as all-pages.html lists it, else its <title>."""
    m = re.search(r'<a href="%s"><strong>(.*?)</strong>' % re.escape(src), _AP)
    if m:
        return m.group(1)
    m = re.search(r"<title>(.*?)</title>", open(os.path.join(HERE, src), encoding="utf-8").read(), re.S)
    return re.sub(r"\s*\|.*$", "", m.group(1)).strip() if m else src


def relink(page):
    def one(m):
        name, frag = m.group(1), m.group(2) or ""
        dst = MAP.get(name) or ALIAS.get(name)
        return ' href="%s%s"' % (dst, frag) if dst else ""
    return LINK.sub(one, page)


def copy_asset(rel, done):
    """Copy assets/<rel> (and, for CSS, what its url()s point at)."""
    rel = rel.split("?")[0].split("#")[0]
    if rel in done:
        return
    done.add(rel)
    src = os.path.join(ROOT, "assets", rel)
    if not os.path.isfile(src):
        src = os.path.join(ROOT, "assets", unquote(rel))
    if not os.path.isfile(src):
        raise SystemExit("asset not found: assets/%s" % rel)
    dst = os.path.join(OUT, "assets", os.path.relpath(src, os.path.join(ROOT, "assets")))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    if src.endswith(".css"):
        base = os.path.dirname(os.path.relpath(src, os.path.join(ROOT, "assets")))
        for u in CSS_URL.findall(open(src, encoding="utf-8").read()):
            path = os.path.normpath(os.path.join(base, u))
            if not path.startswith(".."):
                copy_asset(path, done)


def tab():
    rows = []
    for title, items in GROUPS:
        lis = "".join('    <li><a href="../web-v1/%s"><strong>%s</strong><span>%s</span></a></li>\n'
                      % (dst, name or label(src), dst) for src, dst, name in items)
        rows.append('  <h3>%s</h3>\n  <ul class="ap-list">\n%s  </ul>\n' % (title, lis))
    return ('  <section id="panel-web-v1" role="tabpanel" aria-labelledby="tab-web-v1">\n  <h2>Web V1</h2>\n\n'
            '  <p class="ap-sub">The final pages, as the stakeholder folder web-v1/ (pages/_web_v1.py).</p>\n\n'
            + "\n".join(rows) + "  </section>\n")


def index_tab():
    path = os.path.join(HERE, "all-pages.html")
    page = open(path, encoding="utf-8").read()
    start, end = "  <!-- ============================================================== web v1 -->\n", \
                 "  <!-- ================================================================ final -->\n"
    if start not in page:  # first run: the tab button and an empty panel slot
        page = page.replace('        <button type="button" role="tab" id="tab-final" aria-controls="panel-final" aria-selected="true">',
                            '        <button type="button" role="tab" id="tab-web-v1" aria-controls="panel-web-v1" aria-selected="true">'
                            'Web V1<span class="ap-count"></span></button>\n'
                            '        <button type="button" role="tab" id="tab-final" aria-controls="panel-final" aria-selected="false" tabindex="-1">', 1)
        page = page.replace(end, start + end, 1)
    i, j = page.index(start) + len(start), page.index(end)
    page = page[:i] + tab() + "\n" + page[j:]
    if page.count('id="tab-web-v1"') != 1 or page.count('id="panel-web-v1"') != 1:
        raise SystemExit("all-pages.html: Web V1 tab not written, re-check its markup")
    open(path, "w", encoding="utf-8").write(page)


def main():
    done = set()
    for src, dst in MAP.items():
        page = open(os.path.join(HERE, src), encoding="utf-8").read()
        if src == "bond-utsav4.html":
            page = P.logged_in(src, page)
            if "nb__avatar" not in page:
                raise SystemExit("bond-utsav4: logged-in navbar not applied")
        page = P.BOND.sub('href="bond-details7.html"', page)
        page = P.FD_CARD.sub(r'\1href="fd-details2.html"', page)
        page = relink(page)
        for rel in ASSET.findall(page):
            copy_asset(rel, done)
        # A url() held in a custom property (the navbar's --i icons) resolves
        # against the stylesheet that uses it, assets/navbar.css, so it keeps ../assets/.
        page = re.sub(r"(--[\w-]+:\s*url\()\.\./assets/", r"\1@KEEP@", page)
        page = page.replace("../assets/", "assets/").replace("@KEEP@", "../assets/")
        os.makedirs(OUT, exist_ok=True)
        open(os.path.join(OUT, dst), "w", encoding="utf-8").write(page)
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(
        '<!doctype html>\n<meta charset="utf-8">\n<meta http-equiv="refresh" content="0; url=explore.html">\n'
        '<title>GoldenPi Web V1</title>\n<a href="explore.html">Open the pages</a>\n')
    index_tab()
    print("web-v1/  %d pages, %d asset files" % (len(MAP), len(done)))


if __name__ == "__main__":
    main()
