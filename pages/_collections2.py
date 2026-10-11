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


# The top of the page in the user's design (2026-10-11 screenshot): a smaller
# title and a larger intro, both in heading ink, the intro folded to three
# lines behind Read More / Read Less, and roomier pills with larger icons.
# The copy stays the captured copy.
TOP_CSS = """
.c2-top { gap: 24px; }
.c2-top .gp-coltitle { font-size: clamp(26px, 2.4vw, 32px); line-height: 1.2; font-weight: 700; letter-spacing: -.01em; color: var(--app-heading-color); }
.c2-top .gp-colintro { max-width: none; color: var(--app-heading-color); font-size: clamp(16px, 1.45vw, 20px); line-height: 1.6; }
.c2-top .gp-colintro h2 { font-size: 1.05em; }
.c2-top .gp-colintro :first-child { margin-top: 0; }  /* the CMS wraps its paragraphs in a div */
.c2-top .gp-colintro :last-child { margin-bottom: 0; }
.c2-top .gp-colintro.is-folded { display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 3; line-clamp: 3; overflow: hidden; }  /* three whole lines, heading included */
.c2-more { align-self: flex-start; margin-top: -12px; padding: 0; border: 0; background: none; font: inherit; font-size: clamp(16px, 1.45vw, 20px); font-weight: 600;
  color: var(--app-heading-color); text-decoration: underline; text-underline-offset: 4px; cursor: pointer; }
.gp-colintro .c2-more { margin: 0 0 0 8px; }  /* open: at the end of the text */
.c2-more:focus-visible { outline: 2px solid var(--mustard); outline-offset: 2px; border-radius: 4px; }
.c2-top .gp-colpills { margin-top: 4px; }
.c2-top .gp-colpills__track { gap: 16px 18px; }
.c2-top .gp-pill { gap: 12px; padding: 6px 24px 6px 14px; font-weight: 600; box-shadow: 0 2px 6px rgba(50, 40, 17, .06); }
.c2-top .gp-pill img { width: 34px; height: 34px; }
@media (max-width: 767px) {
  .c2-top .gp-colpills__track { gap: 10px; }
  .c2-top .gp-pill { padding: 5px 18px 5px 10px; gap: 8px; }
  .c2-top .gp-pill img { width: 28px; height: 28px; }
}
"""

# Read More / Read Less: without script the intro shows in full and no button.
MORE_JS = """<script>
(function () {
  var intro = document.querySelector('.c2-top .gp-colintro');
  if (!intro) return;
  intro.classList.add('is-folded');
  if (intro.scrollHeight <= intro.clientHeight + 2) { intro.classList.remove('is-folded'); return; }
  intro.id = intro.id || 'c2-intro';
  var b = document.createElement('button');
  b.type = 'button'; b.className = 'c2-more'; b.setAttribute('aria-controls', intro.id);
  function show(open) {
    intro.classList.toggle('is-folded', !open);
    b.textContent = open ? 'Read Less' : 'Read More';
    b.setAttribute('aria-expanded', open);
    // open: at the end of the text, as in the design; folded: under it
    var last = intro;
    while (last.lastElementChild && last.lastElementChild !== b) last = last.lastElementChild;
    if (open && /^(P|LI)$/.test(last.tagName)) last.appendChild(b); else intro.after(b);
  }
  b.addEventListener('click', function () { show(intro.classList.contains('is-folded')); b.focus(); });
  show(false);
})();
</script>
"""


def main():
    old_name, old_card = C.page_name, C.card
    C.page_name = lambda slug: "collections2-%s.html" % slug
    C.card = lambda c, i: re.sub(r'\n  <p class="gp-ucard__note">.*?</p>', "", old_card(c, i), flags=re.S)
    style = ("<style>\n/* user-explore-app7's bond cards (_collections2.py) */\n%s\n%s</style>\n</head>"
             % (card_css(), TOP_CSS))
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
            page, n = re.subn(r'<div class="gp-colmain">', '<div class="gp-colmain c2-top">', page, count=1)
            if n != 1:
                raise SystemExit("%s: gp-colmain not found" % slug)
            k = page.rindex("</body>")
            page = page[:k] + MORE_JS + page[k:]
            with open(path, "w", encoding="utf-8") as f:
                f.write(page)
    finally:
        C.page_name, C.card = old_name, old_card


if __name__ == "__main__":
    main()
