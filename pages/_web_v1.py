#!/usr/bin/env python3
"""web/: the released pages as one self-contained folder (was web-v1/ until
2026-11-20). Replicas: the pages in pages/ are only read, never changed.

Every page sits flat in web/ under a short name, with its own copy of the
assets it uses (web/assets/, same layout as assets/). Links between the
pages point at each other; a link to a page outside the set keeps its look
but loses its href, so a reviewer never lands on a missing page.

bond-utsav4 still carries the guest navbar; its copy takes the logged-in one,
as _prototype.py gives bond-utsav5 (Bond Utsav's own footer stays). bond-utsav6
(pre-login, as bond-utsav2.html) takes the logged-in navbar and footer too.

Every page with the site navbar takes portfolio.html's (the final one, its own
item marked current; pre-login pages keep Login / Sign up), and every page with
a footer takes footer-ggn-login's, pre-login included (user, 2026-11-20). No
link leaves the folder, so nothing points at pages/ or migration/.

Also writes the Web tab of all-pages.html (the panel between its markers).

    python3 pages/_prototype.py && python3 pages/_web_v1.py
"""
import os
import re
import shutil
from urllib.parse import unquote

import _build as B
import _prototype as P

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "web")

# in pill order, as all-pages.html lists them
_AP = open(os.path.join(HERE, "all-pages.html"), encoding="utf-8").read()
COLLECTIONS = list(dict.fromkeys(re.findall(r'<a href="(collections2-[a-z0-9-]+\.html)"', _AP)))
# source page -> name in web/, grouped as the Web tab lists them
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
                 ("bond-utsav6.html", "bond-utsav2.html", "Bond Utsav 2"),  # user, 2026-10-14
                 ("refer-and-earn-with-referral.html", "refer-and-earn.html", "Refer &amp; Earn"),
                 ("profile2.html", "profile.html", "Profile"),  # user, 2026-11-19
                 ("profile-mobile2.html", "profile-mobile.html", "Profile (phone)")]),
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


NAVBAR = re.compile(r"<header\b[^>]*>.*?</header>", re.S)  # the site navbar is the page's first <header>
# the navbar item each page marks current, by destination (none: no mark)
CURRENT = dict({d: "Bonds" for d in ("explore.html", "bond-details.html", "ipo-details.html")},
               **{d: "Bonds" for d in MAP.values() if d.startswith("collections-")},
               **{"fixed-deposits.html": "FD", "fd-details.html": "FD", "bond-utsav.html": "Bond Utsav",
                  "bond-utsav2.html": "Bond Utsav", "refer-and-earn.html": "Refer &amp; Earn",
                  "portfolio.html": "Portfolio"})


def final_navbar():
    page = open(os.path.join(HERE, "portfolio.html"), encoding="utf-8").read()
    m = NAVBAR.search(page)
    if not m or "nb__avatar" not in m.group(0):
        raise SystemExit("portfolio.html: logged-in navbar not found")
    return re.sub(r' is-current| aria-current="page"', "", m.group(0))


def final_chrome(src, dst, page):
    """The final navbar and footer (see the docstring)."""
    if "nb__avatar" in page:  # logged in: portfolio's navbar, this page's item current
        nav, label = final_navbar(), CURRENT.get(dst)
        if label:
            nav, n = re.subn(r'class="(nb__link[^"]*)"( href="[^"]*")(><span[^>]*></span>|><img[^>]*>)<span>%s</span>' % re.escape(label),
                             r'class="\1 is-current"\2 aria-current="page"\3<span>%s</span>' % label, nav, count=1)
            if n != 1:
                raise SystemExit("%s: navbar item %s not found" % (dst, label))
        page, n = NAVBAR.subn(lambda m: nav, page, count=1)
        if n != 1:
            raise SystemExit("%s: navbar not found" % src)
    return B.ggn_footer(src, page, "footer-ggn-login.html")


def tab():
    rows = []
    for title, items in GROUPS:
        lis = "".join('    <li><a href="../web/%s"><strong>%s</strong><span>%s</span></a></li>\n'
                      % (dst, name or label(src), dst) for src, dst, name in items)
        rows.append('  <h3>%s</h3>\n  <ul class="ap-list">\n%s  </ul>\n' % (title, lis))
    return ('  <section id="panel-web" role="tabpanel" aria-labelledby="tab-web">\n  <h2>Web</h2>\n\n'
            '  <p class="ap-sub">The released pages, in web/ (pages/_web_v1.py).</p>\n\n'
            + "\n".join(rows) + "  </section>\n")


def index_tab():
    path = os.path.join(HERE, "all-pages.html")
    page = open(path, encoding="utf-8").read()
    start, end = "  <!-- ================================================================= web -->\n", \
                 "  <!-- ================================================================ final -->\n"
    i, j = page.index(start) + len(start), page.index(end)
    page = page[:i] + tab() + "\n" + page[j:]
    if page.count('id="tab-web"') != 1 or page.count('id="panel-web"') != 1:
        raise SystemExit("all-pages.html: Web tab not written, re-check its markup")
    open(path, "w", encoding="utf-8").write(page)


def main():
    done = set()
    for src, dst in MAP.items():
        page = open(os.path.join(HERE, src), encoding="utf-8").read()
        if src in ("bond-utsav4.html", "bond-utsav6.html"):
            page = P.logged_in(src, page)
            if "nb__avatar" not in page:
                raise SystemExit("%s: logged-in navbar not applied" % src)
        page = final_chrome(src, dst, page)
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
        '<title>GoldenPi Web</title>\n<a href="explore.html">Open the pages</a>\n')
    index_tab()
    print("web/  %d pages, %d asset files" % (len(MAP), len(done)))


if __name__ == "__main__":
    main()
