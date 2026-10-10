#!/usr/bin/env python3
"""Write collections2-<slug>.html (11 pages): the collections set with
user-explore-app7's bond cards (Figma 130:224).

Each page is _collections.build()'s, unchanged but for the cards: app7's card
(no note strip, as F.bond) in app7's sizes and tints. The tints follow app7's
shelves (High Returns sage, Highly Rated gold, Short Term slate); the other
collections take the three in turn, in pill order. Card CSS is read out of
_explore_app7.STYLE, so the two cannot drift.

    python3 pages/_collections2.py && python3 pages/_build.py && python3 pages/_prototype.py
"""
import os
import re

import _build as B
import _explore_app7 as S

C = S.A.C  # _collections.py, loaded by app2 under another name (it clashes with stdlib's)

HERE = os.path.dirname(os.path.abspath(__file__))
TONES = ("sage", "gold", "slate")
FIXED = {slug: tone for slug, _, tone in S.SHELVES}  # app7's own shelves


def tones():
    out, n = {}, 0
    for p in C.DATA["pills"]:
        if p["slug"] in FIXED:
            out[p["slug"]] = FIXED[p["slug"]]
        else:
            out[p["slug"]] = TONES[n % 3]
            n += 1
    return out


def card_css():
    """app7's .x7s card rules, re-scoped to the grid; the shelf row's flex and
    snap stay behind (the grid sizes the cards here)."""
    rules = re.findall(r"^\.x7s(?:--\w+)? \.gp-ucard[^{]*\{[^}]*\}", S.STYLE, re.M)
    if len(rules) < 10:
        raise SystemExit("app7's card rules moved, re-check _explore_app7.STYLE")
    css = "\n".join(re.sub(r"^\.x7s(--\w+)? ", lambda m: ".c2%s " % (m.group(1) or ""), r) for r in rules)
    return re.sub(r"\s*(flex|scroll-snap-align): [^;]+;", "", css)


def logged_in(name, page):
    """app7's logged-in navbar in place of the guest one; _build.py keeps it
    (and gives the logged-in footer) since the header now has the avatar."""
    page, n = re.subn(r'<div class="nb-slot">\n<header class="nb [^"]*" data-v="plain-dark-guest">.*?</header>\n</div>\n',
                      lambda m: B.navbar(name, 'class="nb__avatar"'), page, count=1, flags=re.S)
    if n != 1:
        raise SystemExit("%s: guest navbar not found" % name)
    return page


def main():
    old_name, old_card = C.page_name, C.card
    C.page_name = lambda slug: "collections2-%s.html" % slug
    C.card = lambda c, i: re.sub(r'\n  <p class="gp-ucard__note">.*?</p>', "", old_card(c, i), flags=re.S)
    style = "<style>\n/* user-explore-app7's bond cards (_collections2.py) */\n%s\n</style>\n</head>" % card_css()
    try:
        for slug, tone in tones().items():
            C.build(slug)
            path = os.path.join(HERE, C.page_name(slug))
            with open(path, encoding="utf-8") as f:
                page = f.read()
            page = page.replace('href="collections-', 'href="collections2-')  # breadcrumb, pills
            page = re.sub(r'class="gp-colgrid', 'class="c2 c2--%s gp-colgrid' % tone, page)
            page = page.replace("</head>", style, 1)
            page = logged_in(C.page_name(slug), page)
            with open(path, "w", encoding="utf-8") as f:
                f.write(page)
    finally:
        C.page_name, C.card = old_name, old_card


if __name__ == "__main__":
    main()
