#!/usr/bin/env python3
"""Assert the generated legal pages carry the captured text word for word.

Compares every word inside <main> of crawl/rendered/<slug>.expanded.html with
the generated page (minus its section rail). Exits non-zero on any difference.
"""
import difflib, html, re, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def words(s):
    return html.unescape(re.sub(r"<[^>]+>", " ", s)).split()

bad = 0
for s in ["privacy-policy", "terms-and-conditions"]:
    src = open(os.path.join(ROOT, "crawl/rendered", s + ".expanded.html")).read()
    src = re.sub(r"<svg.*?</svg>", "", src, flags=re.S)
    src = src[src.find("<h1"):]
    out = open(os.path.join(ROOT, "pages", s + ".html")).read()
    out = out[out.find("<h1"):out.find("</main>")]
    out = re.sub(r'<nav class="gp-sidenav".*?</nav>', "", out, flags=re.S)
    a, b = words(src), words(out)
    ops = [o for o in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if o[0] != "equal"]
    print("%-22s %5d words  %s" % (s, len(a), "identical" if not ops else "%d differences" % len(ops)))
    for o in ops[:10]:
        print("   ", o[0], a[o[1]:o[2]][:10], "->", b[o[3]:o[4]][:10])
    bad += len(ops)
sys.exit(1 if bad else 0)
