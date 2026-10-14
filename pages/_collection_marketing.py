#!/usr/bin/env python3
"""collection-explore5.html: collection-explore4's bond card colour variants, with
each card's marketing line kept (2026-10-13).

collection-explore4 shows the cards without the strip under their metrics (the
gp-ucard__note: "Fast Growing Gold Lender", "Equity Listed with ₹2,400 Cr+ Market
Cap", ...). This is the same page with it, so the line can be judged against each
colour: the same blocks, design notes and six bonds, from the same capture.
Nothing here is written; the lines are the capture's.

collection-explore6.html is the same page with the strip's separator line left
off (user, 2026-10-14): the strip's own tint is the only boundary.

    python3 pages/_collection_marketing.py
"""
import os
import re

import _collection_variants as V
import _explore_bonds as X
import _explore_bonds3 as B

OUT = os.path.join(B.HERE, "collection-explore5.html")
OUT6 = os.path.join(B.HERE, "collection-explore6.html")  # the same, without the line over the strip


# The marketing line (gp-ucard__note) in each block's own colours (taste-skill: one
# palette per card, top to bottom; and every line at WCAG AA, 4.5:1, for its 12.6px
# text, which final.css's #a67c00 on gold misses at about 3.3:1). Each strip takes
# the card's tints and a hairline in its border colour; the text takes the card's
# darkest ink: bronze, deep sage, the slate tags' navy, the issuer colour darkened,
# light gold on ink. The hairline block keeps to its rule: no fill, a bronze line.
NOTE_STYLE = """<style>
.cv__block .gp-ucard__note { border-top: 1px solid transparent; }
.cv--gold .gp-ucard__note { background: linear-gradient(90deg, #f5ecd0, #fbf6e6); border-top-color: #e9d9a6; color: #8a6520; }
.cv--sage .gp-ucard__note { background: linear-gradient(90deg, #e2ece4, #f3f7f4); border-top-color: #d5e5d9; color: #2f5a3b; }
.cv--sage-deep .gp-ucard__note { background: linear-gradient(90deg, #c7dccc, #dceadf); border-top-color: #b9d3bf; color: #2f5a3b; }
.cv--slate .gp-ucard__note { background: linear-gradient(90deg, #e6edf6, #f2f6fa); border-top-color: #c9d7e8; color: #2c4a72; }
.cv--issuer-quiet .gp-ucard__note { background: color-mix(in srgb, var(--a) 7%, #f7f5f2); border-top-color: color-mix(in srgb, var(--a) 22%, transparent);
  color: color-mix(in srgb, var(--a) 45%, #1d1a14); }
.cv--issuer-bold .gp-ucard__note { background: color-mix(in srgb, var(--a) 15%, #f7f5f2); border-top-color: color-mix(in srgb, var(--a) 35%, transparent);
  color: color-mix(in srgb, var(--a) 45%, #1d1a14); }
.cv--ink .gp-ucard__note { background: linear-gradient(90deg, rgba(212,175,55,.16), rgba(212,175,55,.06)); border-top-color: rgba(212,175,55,.22); color: #f2d98a; }
.cv--hairline .gp-ucard__note { background: none; border-top-color: rgba(138,101,32,.35); color: #8a6520; }
</style>
"""


def cards():
    """collection-explore4's six bonds (V.cards picks them), with the note strip."""
    html = B.accents(X.explorer())
    out, seen = [], set()
    for c in re.findall(r'<a class="gp-ucard" .*?</a>', html, re.S):
        issuer = re.search(r'gp-ucard__issuer">([^<]+)<', c).group(1)
        if "--acc:" not in c or "gp-ucard__tags" not in c or issuer in seen:
            continue
        seen.add(issuer)
        out.append(c)
        if len(out) == 6:
            break
    if len(out) < 6 or sum('class="gp-ucard__note"' in c for c in out) < 6:
        raise SystemExit("the capture's six bonds changed, or lost their marketing lines")
    return "\n".join(out)


def main():
    grid = cards()
    body = ('  <!-- DATA: six bonds from the uatnew collections capture, repeated in every block,\n'
            '       each with its marketing line (gp-ucard__note), as captured. -->\n'
            '  <div class="cv gp-shell">\n'
            '    <h1 class="cv__title">Bond card colour variants, with marketing lines</h1>\n'
            '    <p class="cv__lead">collection-explore4 with each card\'s marketing line kept under its '
            'metrics: the same six bonds in every block, so colour and intensity are the only change.</p>\n'
            + "\n".join(V.block(*v, grid) for v in V.VARIANTS) +
            '\n  </div>')
    variants = [
        (OUT, "Bond card colour variants, with marketing lines", "", NOTE_STYLE),
        (OUT6, "Bond card colour variants, with marketing lines (no separator)",
         " The strip has no line over it; its tint alone sets it off.",
         NOTE_STYLE + "<style>\n.cv__block .gp-ucard__note { border-top: 0; }  /* no separator line */\n</style>\n"),
    ]
    for out, title, extra, note_css in variants:
        page_body = body.replace("Bond card colour variants, with marketing lines</h1>", title + "</h1>", 1)
        page_body = page_body.replace("so colour and intensity are the only change.</p>", "so colour and intensity are the only change." + extra + "</p>", 1)
        html = B.page(page_body, "Design exploration: bond card colour variants, with each card's marketing line.", V.STYLE + note_css)
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
        print("%s  %d bytes" % (os.path.relpath(out, B.ROOT), len(html)))

if __name__ == "__main__":
    main()
