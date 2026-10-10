#!/usr/bin/env python3
"""Wire the post-login prototype together (the user's map, 2026-10-10):

  Home, Bonds          -> user-explore-app7.html
  a bond card          -> bond-details7.html
  the IPO card         -> ipo-details.html        (already so on app7)
  FD                   -> user-fixed-deposits-app2.html
  an FD card           -> fd-details2.html
  Bond Utsav           -> bond-utsav5.html        (given the logged-in navbar)
  Portfolio, Refer & Earn: unchanged

Only the pages below are rewired; every other page keeps its links. The pages
are generated (and _build.py resyncs navbars), so run this LAST:

    python3 pages/_prototype.py
"""
import os
import re
import sys

import _build as B

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = ["user-explore-app7.html", "bond-details7.html", "ipo-details.html", "user-fixed-deposits-app2.html",
         "fd-details2.html", "bond-utsav5.html", "portfolio.html"]
HREF = {"index.html": "user-explore-app7.html", "user-explore.html": "user-explore-app7.html",
        "user-corporate-bonds.html": "user-explore-app7.html", "corporate-bonds.html": "user-explore-app7.html",
        "user-fixed-deposits.html": "user-fixed-deposits-app2.html", "fixed-deposits.html": "user-fixed-deposits-app2.html",
        "bond-utsav.html": "bond-utsav5.html", "fd-details.html": "fd-details2.html"}
BOND = re.compile(r'href="https://uatnew\.goldenpi\.com/bonds/[^"]*"')            # bond cards (live-site links)
FD_CARD = re.compile(r'(<a class="gp-ucard fdc" )href="https://goldenpi\.com/fixed-deposits"')  # app2's FD cards


def logged_in(name, page):
    """bond-utsav5 was built with the guest navbar: give it _build's logged-in one, Bond Utsav current."""
    m = re.search(r'<div class="nb-slot">\n<header class="nb [^"]*" data-v="plain-dark-guest">.*?</header>\n</div>\n', page, re.S)
    if not m:
        return page
    B.ACTIVE[name] = "Bond Utsav"
    return page[:m.start()] + B.navbar(name, 'class="nb__avatar"') + page[m.end():]


def wire(name):
    path = os.path.join(HERE, name)
    page = before = open(path, encoding="utf-8").read()
    if name == "bond-utsav5.html":
        page = logged_in(name, page)
    page = re.sub(r'href="([^"#]+\.html)"', lambda m: 'href="%s"' % HREF.get(m.group(1), m.group(1)), page)
    page = BOND.sub('href="bond-details7.html"', page)
    page = FD_CARD.sub(r'\1href="fd-details2.html"', page)
    if page != before:
        open(path, "w", encoding="utf-8").write(page)
    left = sorted(set(re.findall(r'href="(%s)"' % "|".join(map(re.escape, HREF)), page)))
    if left:
        sys.exit("%s: still links %s" % (name, left))
    return page != before


if __name__ == "__main__":
    print("prototype: rewired %d of %d pages" % (sum(wire(n) for n in PAGES), len(PAGES)))
