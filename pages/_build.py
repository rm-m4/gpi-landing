#!/usr/bin/env python3
"""Keep the shared promo bar, header and footer identical across the pages.

These are intentionally duplicated in every .html file -- this is a static
prototype and developers will rebuild them as components -- but hand-editing four
copies drifts. corporate-bonds.html is the reference page, and it is generated,
so edit the shell in _final_shell.html, run _final.py, then run this. The -old
archives are deliberately absent from ACTIVE: they are frozen snapshots and must
not be re-synced. Then run:

    python3 pages/_build.py

Every other page's shell is replaced with that one, with only the nav's active
item and the nav icon adjusted per page.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REFERENCE = "corporate-bonds.html"

# corporate-bonds-taste*.html and -final.html are deliberately absent: the minimalist-ui direction
# is standalone and shares no shell with the others.

# page -> (nav label that is active, or None)
ACTIVE = {
    "index.html": None,
    "bond-ipo-online-taste.html": "Bonds",
    "fixed-deposits-taste.html": "FD",
    "index-taste.html": None,
    "index-alt.html": None,
    "corporate-bonds.html": "Bonds",
    "fixed-deposits.html": "FD",
    "bond-ipo-online.html": "Bonds",
    "corporate-bonds-alt.html": "Bonds",
    "bond-ipo-online-alt.html": "Bonds",
    "fixed-deposits-alt.html": "FD",
}

SHELL_START = '<a class="gp-skip"'
SHELL_END = '<main id="main-content">'
FOOTER_START = "<!-- ============================================================== footer -->"
# End *inclusive* at </footer>, not at </body>: a page may carry its own <style> or
# <script> after the footer, and slicing to </body> would silently delete it.
FOOTER_END = "</footer>"


def slice_between(text, start, end, what, path, inclusive=False):
    try:
        i = text.index(start)
        j = text.index(end, i)
    except ValueError:
        sys.exit("%s: could not locate %s" % (path, what))
    return i, (j + len(end) if inclusive else j)


def set_active(shell, active_label):
    """Mark one nav item current and give it the '-selected' icon."""
    shell = shell.replace(' aria-current="page"', "")
    shell = re.sub(r'header-nav-(bonds|fd)-selected\.svg', r'header-nav-\1.svg', shell)
    if not active_label:
        return shell

    pattern = re.compile(
        r'(<a class="gp-nav__link" href="[^"]+")(>\s*<img src="\.\./assets/img/header-nav-)'
        r'([a-z-]+)(\.svg" alt="">\s*' + re.escape(active_label) + r'\s*</a>)'
    )

    def mark(m):
        return "%s aria-current=\"page\"%s%s-selected%s" % (
            m.group(1), m.group(2), m.group(3), m.group(4))

    shell, n = pattern.subn(mark, shell, count=1)
    if n != 1:
        sys.exit("could not mark nav item %r as active" % active_label)
    return shell


def main():
    ref = open(os.path.join(HERE, REFERENCE), encoding="utf-8").read()
    i, j = slice_between(ref, SHELL_START, SHELL_END, "shell", REFERENCE)
    shell = ref[i:j]
    fi, fj = slice_between(ref, FOOTER_START, FOOTER_END, "footer", REFERENCE, inclusive=True)
    footer = ref[fi:fj]

    changed = 0
    for name, active in ACTIVE.items():
        path = os.path.join(HERE, name)
        if not os.path.exists(path) or name == REFERENCE:
            continue
        page = open(path, encoding="utf-8").read()
        before = page

        i, j = slice_between(page, SHELL_START, SHELL_END, "shell", name)
        page = page[:i] + set_active(shell, active) + page[j:]
        fi, fj = slice_between(page, FOOTER_START, FOOTER_END, "footer", name, inclusive=True)
        page = page[:fi] + footer + page[fj:]

        if page != before:
            open(path, "w", encoding="utf-8").write(page)
            changed += 1
        print("%-24s %s" % (name, "updated" if page != before else "unchanged"))

    print("\n%d page(s) updated from %s" % (changed, REFERENCE))


if __name__ == "__main__":
    main()
