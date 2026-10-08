#!/usr/bin/env python3
"""fd-details.html: beta's FD page for Unity Small Finance Bank, built the way
ipo-details.html is.

bond-details7.html is the template and is only read: its page shell
(breadcrumb, phone toolbar, two-column grid, phone invest bar), its dark
header card and its app QR band. Everything FD-only is production's own
markup, taken from beta's rendered page as it loads (nothing opened):
Popular Tenures, All Available Tenures, the bank comparison card, Why Unity,
the FD calculator, the FAQ and Need Help. Their CSS rules are vendored from
production into assets/beta/fd.css by crawl/vendor_css.py.

Content: content/beta_fixed-deposits_GPID105192_unity.md (captured 2026-10-08).
Production markup: crawl/rendered/beta_fixed-deposits_GPID105192_unity-small-finance-bank/rendered.html.

    python3 pages/_fd_details.py && python3 crawl/vendor_css.py fd   # css only when production changes
"""
import os
import re
import urllib.parse
import urllib.request

import _bond_beta as B

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(HERE, "bond-details7.html")
OUT = os.path.join(HERE, "fd-details.html")
CAP = os.path.join(ROOT, "crawl/rendered/beta_fixed-deposits_GPID105192_unity-small-finance-bank/rendered.html")
IMG = os.path.join(ROOT, "assets/img/fd")

NAME = "UNITY SMALL FINANCE BANK"


def element(h, start):
    """End index of the element whose start tag begins at `start` (balanced on that tag name)."""
    tag = re.match(r"<(\w+)", h[start:]).group(1)
    depth = 0
    for t in re.finditer(r"<(/?)%s\b[^>]*>" % tag, h[start:]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            return start + t.end()
    raise SystemExit("fd-details: unbalanced <%s> at %d" % (tag, start))


def find(h, needle, after=0):
    i = h.find(needle, after)
    if i < 0:
        raise SystemExit("fd-details: not found: %s" % needle[:90])
    return i


def swap(h, old, new, count=1):
    if h.count(old) != count:
        raise SystemExit("fd-details: expected %d of %r, found %d" % (count, old[:80], h.count(old)))
    return h.replace(old, new)


# ------------------------------------------------------- production blocks

def local_img(src):
    """Production image URL (often /_next/image?url=...) -> a local copy's path."""
    src = src.replace("&amp;", "&")
    if src.startswith("/_next/image"):
        src = urllib.parse.unquote(urllib.parse.parse_qs(urllib.parse.urlparse(src).query)["url"][0])
    if src.startswith("/_next/static/media/"):
        return B.media(src)
    if src.startswith("https://"):
        name = urllib.parse.unquote(src.rsplit("/", 1)[1]).replace(" ", "-")
        dest = os.path.join(IMG, name)
        if not os.path.exists(dest):
            os.makedirs(IMG, exist_ok=True)
            with urllib.request.urlopen(src, timeout=60) as r, open(dest, "wb") as f:
                f.write(r.read())
        return "../assets/img/fd/" + name
    raise SystemExit("fd-details: unexpected image %s" % src)


def clean(html):
    """Production markup -> static: local images, no srcset or React-only attributes."""
    html = re.sub(r'\s(?:srcSet|srcset|sizes)="[^"]*"', "", html)
    html = re.sub(r'(<img\b[^>]*?\ssrc=")([^"]+)(")', lambda m: m.group(1) + local_img(m.group(2)) + m.group(3), html)
    return html


PROD = None


def production(start_needle):
    """The production element starting at `start_needle` in the rendered capture."""
    global PROD
    if PROD is None:
        PROD = open(CAP, encoding="utf-8").read()
    i = find(PROD, start_needle)
    return clean(PROD[i:element(PROD, i)])


def calculator():
    """The sidebar's contents: production's checkout card and its sticky bar."""
    global PROD
    production('<section class="fd-checkout-card')
    i = find(PROD, '<section class="fd-checkout-card')
    aside = PROD.rfind("<aside", 0, i)
    inner = PROD[PROD.index(">", aside) + 1:element(PROD, aside) - len("</aside>")]
    return clean(inner)


def faq_row():
    """FAQ and Need Help: production's row under the main grid. Production renders an answer only once its
    question is opened, so this row comes from the capture with every FAQ open, closed again here
    (aria-expanded false, body hidden) for bond-details7's accordion script to toggle."""
    s = open(CAP.replace("rendered.html", "expanded.html"), encoding="utf-8").read()
    i = find(s, '<section class="ipo-surface-card fd-faq')
    row = s.rfind('<div class="mt-2 grid w-full grid-cols-1', 0, i)
    html = s[row:element(s, row)]
    n = html.count('class="gp-expand__summary" aria-expanded="true"')
    html = html.replace('class="gp-expand__summary" aria-expanded="true"', 'class="gp-expand__summary" aria-expanded="false"')
    html = re.sub(r'(<div id="[^"]+" role="region")', r"\1 hidden", html)
    html = html.replace("gp-expand--faq is-open ", "gp-expand--faq ")
    html = re.sub(r'(class="gp-expand__chevron[^"]*?) is-open', r"\1", html)
    if n != 8 or html.count(" hidden class=\"gp-expand__body\"") + html.count('role="region" hidden') < 8:
        raise SystemExit("fd-details: expected 8 FAQs to close, found %d" % n)
    return clean(html)


# ---------------------------------------------------------- template edits

def chrome(h):
    h = re.sub(r"<title>.*?</title>", "<title>Unity Small Finance Bank FD | GoldenPi</title>", h, count=1, flags=re.S)
    h = re.sub(r'<meta name="description" content="[^"]*">',
               '<meta name="description" content="Unity Small Finance Bank fixed deposit: tenures, rates, returns and FAQs.">',
               h, count=1)
    h = re.sub(r"<!-- Generated by pages/_bond_v7\.py.*?-->",
               "<!-- Generated by pages/_fd_details.py from bond-details7.html (shell, header card, QR band) and beta's "
               "Unity SFB FD page (content, FD blocks); do not edit. -->", h, count=1, flags=re.S)
    h = swap(h, 'href="corporate-bonds.html">Bonds</a>', 'href="fixed-deposits.html">Fixed Deposits</a>')
    h, n = re.subn(r'(aria-current="page">)MAHAVEER(</li>)', r"\g<1>%s\2" % NAME, h, count=1)
    if n != 1:
        raise SystemExit("fd-details: breadcrumb not found")
    h, n = re.subn(r'<button type="button" class="bond-header-action-trigger" aria-label="Add to watchlist" aria-pressed="false">'
                   r'<img([^>]*?)src="[^"]*"([^>]*)></button>',
                   r'<button type="button" class="bond-header-action-trigger" aria-label="Share"><img\1src="../assets/beta/media/'
                   r'share-action-mobile.16f54imqsowrz.svg"\2></button>', h, count=1)
    if n != 1:
        raise SystemExit("fd-details: phone toolbar not found")
    # The bond's Cashflow Timeline modal and the script lines that open it.
    a = find(h, '<div id="cashflow-modal" hidden>')
    h = h[:a] + h[element(h, a):]
    h, n = re.subn(r"\n  var modal = document\.getElementById\('cashflow-modal'\);.*?if \(e\.key === 'Escape'\) show\(false\); \}\);",
                   "", h, count=1, flags=re.S)
    if n != 1:
        raise SystemExit("fd-details: cashflow modal script not found")
    return h.replace("</head>", '<link rel="stylesheet" href="../assets/beta/ipo.css">\n'
                     '<link rel="stylesheet" href="../assets/beta/fd.css">\n' + HEADER_CSS + '</head>', 1)


# The header: bond-details7's black card, redesigned for the FD (design-taste-frontend read: regulated FD
# product header for retail savers, trust-first premium; dials variance 5 / motion 3 / density 4; the page's
# one dark block). Asymmetric split: the rate leads on the left, the DICGC cover is promoted on the right,
# and Why Unity's facts close the card as a divided strip. Every string is captured copy; graphics are
# bond-details7's 3D icon set.
FACTS = [("Total Deposits", "11,000+ Crore"), ("Customer Base", "18+ Lakh"), ("Physical Branches", "~400"),
         ("Founded By", "BharatPe &amp; Centrum Group")]
BD5 = "../assets/img/bd5/"


def hero(h):
    a = find(h, '<header class="b7-hc"')
    logo = local_img("https://s3.ap-south-1.amazonaws.com/production.goldenpi.com/static/images/logos/GPID105192.Unity.png")
    facts = "".join('<div><dt>%s</dt><dd>%s</dd></div>' % f for f in FACTS)
    card = (
        '<header class="fdh" aria-labelledby="fdh-name">'
        '<div class="fdh__top"><span class="fdh__ring"><img src="%s" alt="%s logo" width="64" height="64"></span>'
        '<h1 id="fdh-name">%s</h1>'
        '<button type="button" class="fdh__share" aria-label="Share"><img src="../assets/beta/media/share-action-desktop.2j-atjt_xvh2t.svg" '
        'alt="" width="40" height="40"></button></div>'
        '<div class="fdh__body">'
        '<div class="fdh__rate">'
        '<p class="fdh__label">Returns Upto</p>'
        '<p class="fdh__big">8.50%%</p>'
        '<p class="fdh__split"><span><b>8.50%%</b> Sr. Citizen</span><span><b>8.00%%</b> Regular</span></p>'
        '<p class="fdh__tenure">1Y 4M 16D &middot; On Maturity</p>'
        '<ul class="fdh__perks" role="list">'
        '<li><img src="%stile-clock.png" alt="" width="40" height="40">Withdraw Anytime</li>'
        '<li><img src="%sreasons-hand.png" alt="" width="40" height="40">Start investing with just &#8377;1,000</li>'
        '</ul></div>'
        '<div class="fdh__cover"><img class="fdh__shield" src="%stile-shield.png" alt="" width="96" height="96">'
        '<p class="fdh__cover-k">DICGC Insurance Upto</p><p class="fdh__cover-v">&#8377;5 Lacs</p>'
        '<p class="fdh__cover-by">Insured by RBI&#39;s DICGC</p></div>'
        '</div>'
        '<div class="fdh__why"><h2>Why Unity Small Finance Bank</h2><dl>%s</dl></div>'
        '</header>' % (logo, NAME, NAME, BD5, BD5, BD5, facts))
    return h[:a] + card + h[element(h, a):]


HEADER_CSS = """<style>
/* fd-details header (see hero() in pages/_fd_details.py). bond-details7's black card and gold, Inter like it.
   Radius rule: card 20px, panels 16px, controls full pill. One accent: #edc967. */
.fdh { position: relative; overflow: hidden; display: grid; gap: 22px; padding: 22px 24px 0; border-radius: 20px; color: #fff;
  font-family: Inter, satoshi, system-ui, sans-serif; font-variant-numeric: tabular-nums;
  background: radial-gradient(889.54px 347.9px at 100% 100%, #27272a 0%, #18181b 40%, #0c0c0e 70%, #060607 85%, #0a0a0b 100%); }
:where(.fdh) :where(p, h1, h2, dl, dd, ul) { margin: 0; }
.fdh__top { display: flex; align-items: center; gap: 18px; }
.fdh__ring { flex: none; display: grid; place-items: center; width: 64px; height: 64px; border: 2px solid #edc967; border-radius: 9999px; }
.fdh__ring img { width: 58px; height: 58px; border-radius: 50%; object-fit: cover; }
.fdh h1 { flex: 1; min-width: 0; font-size: 24px; line-height: 1.2; font-weight: 600; letter-spacing: -0.01em; color: rgba(255, 255, 255, .92); text-wrap: balance; }
.fdh__share { flex: none; display: grid; place-items: center; width: 40px; height: 40px; padding: 0; border: 0; border-radius: 9999px; background: none; cursor: pointer; }
.fdh__share:focus-visible { outline: 2px solid #edc967; outline-offset: 2px; }

.fdh__body { display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr); gap: 20px; align-items: stretch; }
.fdh__label { font-size: 13px; font-weight: 500; color: rgba(255, 255, 255, .55); }
.fdh__big { margin-top: 2px; font-size: 56px; line-height: 1; font-weight: 700; letter-spacing: -0.03em; color: #edc967; }
.fdh__split { display: flex; flex-wrap: wrap; gap: 6px 16px; margin-top: 12px; font-size: 13px; color: rgba(255, 255, 255, .6); }
.fdh__split b { font-weight: 600; color: rgba(255, 255, 255, .92); }
.fdh__split span + span { padding-left: 16px; border-left: 1px solid rgba(255, 255, 255, .14); }
.fdh__tenure { display: inline-block; margin-top: 12px; padding: 5px 12px; border-radius: 9999px; border: 1px solid rgba(255, 255, 255, .12);
  font-size: 12px; font-weight: 500; color: rgba(255, 255, 255, .75); }
.fdh__perks { display: grid; gap: 12px; margin-top: 22px; padding: 0; list-style: none; }
.fdh__perks li { display: flex; align-items: center; gap: 12px; font-size: 14px; font-weight: 500; color: rgba(255, 255, 255, .88); }
.fdh__perks img { flex: none; width: 44px; height: 44px; padding: 6px; border-radius: 9999px; object-fit: contain;
  background: rgba(255, 255, 255, .06); box-shadow: inset 0 0 0 1px rgba(255, 255, 255, .08); }

.fdh__cover { display: grid; justify-items: start; align-content: center; gap: 2px; padding: 20px; border-radius: 16px;
  border: 1px solid rgba(237, 201, 103, .28);
  background: radial-gradient(240px 160px at 85% 0%, rgba(237, 201, 103, .18), transparent 70%), rgba(255, 255, 255, .03); }
.fdh__shield { width: 88px; height: 88px; margin: -6px 0 6px -8px; object-fit: contain; filter: drop-shadow(0 10px 22px rgba(237, 201, 103, .28)); }
.fdh__cover-k { font-size: 13px; font-weight: 500; color: rgba(255, 255, 255, .6); }
.fdh__cover-v { font-size: 38px; line-height: 1.1; font-weight: 700; letter-spacing: -0.02em; color: #fff; }
.fdh__cover-by { margin-top: 6px; font-size: 13px; font-weight: 500; color: #edc967; }

.fdh__why { margin: 0 -24px; padding: 18px 24px 20px; border-top: 1px solid rgba(255, 255, 255, .08); background: rgba(255, 255, 255, .025); }
.fdh__why h2 { font-size: 13px; font-weight: 600; color: rgba(255, 255, 255, .7); }
.fdh__why dl { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); margin-top: 12px; }
.fdh__why dl > div { padding: 0 14px; border-left: 1px solid rgba(255, 255, 255, .1); }
.fdh__why dl > div:first-child { padding-left: 0; border-left: 0; }
.fdh__why dt { font-size: 12px; color: rgba(255, 255, 255, .5); }
.fdh__why dd { margin-top: 4px; font-size: 14px; line-height: 1.3; font-weight: 600; color: rgba(255, 255, 255, .92); }

@media (max-width: 767px) {
  .fdh { gap: 18px; padding: 18px 16px 0; }
  .fdh__top { gap: 14px; }
  .fdh__ring { width: 52px; height: 52px; }
  .fdh__ring img { width: 46px; height: 46px; }
  .fdh h1 { font-size: 20px; }
  .fdh__body { grid-template-columns: minmax(0, 1fr); gap: 16px; }
  .fdh__big { font-size: 48px; }
  .fdh__cover { grid-template-columns: auto minmax(0, 1fr); column-gap: 14px; align-items: center; padding: 14px 16px; }
  .fdh__shield { grid-row: span 3; width: 60px; height: 60px; margin: 0; }
  .fdh__cover-v { font-size: 26px; }
  .fdh__why { margin: 0 -16px; padding: 16px; }
  .fdh__why dl { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px 0; }
  .fdh__why dl > div:nth-child(3) { padding-left: 0; border-left: 0; }
}
</style>
"""


def main_column(h):
    """Highlights, phone calculator, Cashflow and the two Company/Documents groups are the bond's; production's FD
    blocks take their place. The QR band stays last."""
    a = h.rfind('<div class="b4 b5 b5-embed">', 0, find(h, '<section class="b7-hl"'))
    h = h[:a] + h[element(h, a):]
    main = find(h, '<div class="block lg:hidden"><section aria-labelledby="bond-cashflow-sidebar-title-mobile">')
    qr = find(h, '<section class="gp-expand gp-expand--card a3"', main)
    blocks = ("<!-- Production markup (beta, rendered 2026-10-08): FD blocks as the page loads them. -->"
              + production('<section class="ipo-surface-card ipo-series-cards fd-recommended-tenures')
              + production('<section class="ipo-surface-card ipo-series-table fd-all-tenures')
              + production('<section class="fd-comparison'))
    return h[:main] + blocks + h[qr:]


def sidebar(h):
    """bond-details7's calculator section in the desktop rail -> production's FD checkout card."""
    a = find(h, '<section aria-labelledby="bond-cashflow-sidebar-title-desktop">')
    return h[:a] + calculator() + h[element(h, a):]


def faq(h):
    """Production's FAQ + Need Help row sits under the two-column grid, inside the same shell."""
    a = find(h, '<div class="issuer-main')
    shell = find(h, '<div class="issuer-shell">', a)
    grid = find(h, "<div class=\"grid", shell)
    end = element(h, grid)
    return h[:end] + faq_row() + h[end:]


def invest_bar(h):
    # bond-details7's own bar is the last one (production's sidebar has a summary of the same name).
    a = h.rfind('aria-label="Investment summary"')
    bar = h[a:find(h, "</aside>", a)]
    new = swap(bar, ">₹ 9,368.14</span>", ">₹ 1,00,000</span>")
    new = re.sub(r'<p class="m-0 inline-flex items-center gap-1\.5">.*?</p>', "", new, count=1, flags=re.S)
    return h.replace(bar, new, 1)


def main():
    h = open(SRC, encoding="utf-8").read()
    for step in (chrome, hero, main_column, sidebar, faq, invest_bar):
        h = step(h)
    body = h[h.index("<main"):h.index("</main>")]
    for stale in ("Mahaveer", "MAHAVEER", "9,368.14", "11,108.45", "_next/"):
        if stale in body:
            print("note: %d x %r left in <main>" % (body.count(stale), stale))
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(h)
    print("fd-details.html  %d bytes" % len(h))


if __name__ == "__main__":
    main()
