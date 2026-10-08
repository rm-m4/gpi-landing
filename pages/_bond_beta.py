#!/usr/bin/env python3
"""bond-details.html, bond-details2.html and bond-details3.html: beta.goldenpi.com's bond detail page, kept in its own design.

Unlike the redesigned pages this one is their DOM and their compiled CSS
(assets/beta/), so it looks exactly like beta. The input is the capture made by
`node crawl/bond_expand.js <dir>`: every section opened (collapsed panels are not
in their DOM at all), the four <canvas> charts saved as images, and the Cashflow
Timeline modal's markup. This script then:

- drops their scripts, and points CSS and /_next/static/media images at local copies
- closes Documents, Cashflow and Financial Ratio again, as beta loads them
- removes the floating "Invest Smarter" app-download QR card
- adds the modal back, hidden, and a small script for the toggles

    python3 pages/_bond_beta.py
"""
import os
from decimal import Decimal
import re
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAP = os.path.join(ROOT, "crawl/rendered/beta_bonds_INE911L07154_mahaveer-1200-bond-yield")
OUT = os.path.join(ROOT, "pages/bond-details.html")
# Same page, Company Financials and Financial Ratio merged; see merge_financials().
OUT2 = os.path.join(ROOT, "pages/bond-details2.html")
# bond-details2 with a design pass on its new pieces; see fin_v3().
OUT3 = os.path.join(ROOT, "pages/bond-details3.html")
MEDIA = os.path.join(ROOT, "assets/beta/media")
BETA = "https://beta.goldenpi.com"
# Root-relative links that have a page in this repo; the rest go to beta.
LOCAL = {"/": "index.html", "/corporate-bonds": "corporate-bonds.html"}
CLOSED = ("Documents", "Cashflow", "Financial Ratio")


def media(path):
    """/_next/static/media/x.svg -> ../assets/beta/media/x.svg, fetched once."""
    name = path.rsplit("/", 1)[1]
    dest = os.path.join(MEDIA, name)
    if not os.path.exists(dest):
        os.makedirs(MEDIA, exist_ok=True)
        urllib.request.urlretrieve(BETA + path, dest)
    return "../assets/beta/media/" + name


def clean(html):
    html = re.sub(r"<script\b.*?</script>", "", html, flags=re.S)
    html = re.sub(r"<noscript\b.*?</noscript>", "", html, flags=re.S)
    html = re.sub(r'<style id="googleidentityservice.*?</style>', "", html, flags=re.S)
    html = re.sub(r'<link[^>]*(googleidentityservice|rel="(preload|modulepreload|preconnect|dns-prefetch)")[^>]*>', "", html)
    html = re.sub(r'href="/_next/static/chunks/([^"]+\.css)"', r'href="../assets/beta/\1"', html)
    # next/image: src is a resizer URL wrapping the real one; srcset is the same again.
    html = re.sub(r'\s(srcset|imagesizes)="[^"]*"', "", html)

    def img(m):
        real = urllib.parse.unquote(m.group(1).split("&")[0])
        return 'src="%s"' % (media(real) if real.startswith("/_next/static/media/") else real)

    html = re.sub(r'src="/_next/image\?url=([^"]+)"', img, html)
    html = re.sub(r'src="(/_next/static/media/[^"]+)"', lambda m: 'src="%s"' % media(m.group(1)), html)

    def link(m):
        p = m.group(1).replace("&amp;", "&")
        return 'href="%s"' % LOCAL.get(p, BETA + m.group(1))

    return re.sub(r'href="(/[^"_][^"]*|/)"', link, html)


def close(html, title):
    """Collapse one gp-expand section, matching beta's closed markup."""
    m = re.search(r'<button type="button" class="gp-expand__summary[^"]*" id="([^"]+)" aria-expanded="true" aria-controls="([^"]+)">(?:(?!</button>).)*?%s' % re.escape(title), html, re.S)
    if not m:
        raise SystemExit("section not found: " + title)
    btn, panel = m.group(1), m.group(2)
    head = html[: m.start()]
    w = head.rfind('class="gp-expand ')
    head = head[:w] + head[w:].replace(" is-open", "", 1)
    tail = html[m.start():]
    tail = tail.replace('id="%s" aria-expanded="true"' % btn, 'id="%s" aria-expanded="false"' % btn, 1)
    tail = re.sub(r'(gp-expand__chevron) is-open', r"\1", tail, count=1)
    tail = tail.replace('<div id="%s"' % panel, '<div hidden id="%s"' % panel, 1)
    return head + tail


def span(html, start, after=0):
    """(start, end) of the <div> that opens with `start`, children and all."""
    i = html.index(start, after)
    depth = 0
    for m in re.finditer(r"<(/?)div\b", html[i:]):
        depth += -1 if m.group(1) else 1
        if not depth:
            return i, i + m.end() + html[i + m.end():].index(">") + 1
    raise SystemExit("unclosed div: " + start)


def drop(html, start):
    """Remove the <div> opening with `start`, children and all."""
    i, j = span(html, start)
    return html[:i] + html[j:]


SCRIPT = """
<script>
// Stand-in for beta's React handlers: section accordions, cashflow years,
// and the Cashflow Timeline modal. Class names are theirs.
(function () {
  document.querySelectorAll('.gp-expand__summary').forEach(function (b) {
    b.addEventListener('click', function () {
      var open = b.getAttribute('aria-expanded') !== 'true';
      b.setAttribute('aria-expanded', open);
      document.getElementById(b.getAttribute('aria-controls')).hidden = !open;
      b.closest('.gp-expand').classList.toggle('is-open', open);
      var c = b.querySelector('.gp-expand__chevron');
      if (c) c.classList.toggle('is-open', open);
    });
  });
  document.addEventListener('click', function (e) {
    var t = e.target.closest('.bond-cashflow-year-header-in-panel--toggle, .bond-cashflow-year-header-mobile');
    if (!t) return;
    var tl = t.closest('.bond-cashflow-timeline');
    var open = t.getAttribute('aria-expanded') !== 'true';
    tl.querySelectorAll('[aria-expanded]').forEach(function (x) { x.setAttribute('aria-expanded', open); });
    var c = tl.querySelector('.bond-cashflow-year-payouts-collapse');
    c.classList.toggle('bond-cashflow-year-payouts-collapse--open', open);
    c.setAttribute('aria-hidden', !open);
    var row = tl.closest('.bond-cashflow-year-expanded-row');
    if (row) row.classList.toggle('bond-cashflow-year-row--collapsed', !open);
  });
  var modal = document.getElementById('cashflow-modal');
  function show(on) { modal.hidden = !on; document.body.style.overflow = on ? 'hidden' : ''; }
  document.querySelectorAll('.bond-cashflow-sidebar__timeline-btn').forEach(function (b) {
    b.addEventListener('click', function () { show(true); });
  });
  modal.addEventListener('click', function (e) {
    if (e.target.closest('.site-modal__close') || e.target.classList.contains('site-modal__overlay')) show(false);
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') show(false); });
})();
</script>
"""


# ------------------------------------------------------------ bond-details2
# Company Financials and Financial Ratio merged into one section, and the four
# charts into one, behind beta's own tab bar (the mobile card, used at every
# width). Bars are markup, not canvas, so they can animate and go negative.

SUBTITLE = {"AUM": "Assets under management", "PAT": "Profit after tax"}  # as beta labels them
# Beta's tab label classes, active and idle; the script swaps between them.
TAB_ON = "relative inline-block max-w-full whitespace-nowrap transition-colors duration-200 ease-out motion-reduce:transition-none text-icon-gold text-xs font-bold leading-[35px] tracking-[0.0833em]"
TAB_OFF = "relative inline-block max-w-full whitespace-nowrap transition-colors duration-200 ease-out motion-reduce:transition-none text-icon-gold text-[10px] font-bold leading-[12.81px] tracking-[0.1em] uppercase"
UNDERLINE = '<img alt="" aria-hidden="true" draggable="false" width="48" height="3" class="company-financials-tab-indicator__image absolute inset-x-0 top-full mt-px" src="../assets/beta/media/company-financials-tab-underline.1z5upzfnx1ej_.svg">'


def series(raw):
    """[(name, [(year, rupees), ...])] from the page's own data payload."""
    block = re.search(r'\\"companyFinancials\\":\{\\"series\\":\[(.*?)\]', raw).group(1)
    out = []
    for name, charts in re.findall(r'\\"name\\":\\"(.*?)\\",\\"charts\\":\{(.*?)\}', block):
        name = name.replace("\\\\u0026", "&").replace("\\u0026", "&")
        out.append((name, [(y, float(v)) for y, v in re.findall(r'\\"(\d{4})\\":(-?[\d.]+)', charts)]))
    return out


def crore(v):
    """7630000000 -> '₹763Cr', -12500000 -> '-₹1.25Cr', 0 -> '₹0Cr' (en-IN grouping)."""
    cr = round(abs(v) / 1e7, 2)
    whole, frac = divmod(cr, 1)
    s = str(int(whole))
    if len(s) > 3:  # Indian grouping: last three digits, then pairs
        head, tail = s[:-3], s[-3:]
        s = ",".join([head[max(0, k - 2):k] for k in range(len(head), 0, -2)][::-1]) + "," + tail
    if frac:
        s += ("%.2f" % frac)[1:].rstrip("0")
    return ("-" if v < 0 else "") + "&#8377;" + s + "Cr"


def scale(values):
    """Zero line and bar extents as % of the plot, for any mix of signs.

    Returns (zero_from_top, [(top, height), ...]). The range always spans 0,
    so positive bars rise from the zero line and negative ones hang below it.
    """
    hi, lo = max(0.0, *values), min(0.0, *values)
    rng = (hi - lo) or 1.0  # all zero: flat bars on a zero line at the bottom
    zero = hi / rng * 100
    bars = []
    for v in values:
        h = abs(v) / rng * 100
        bars.append((zero - h if v > 0 else zero, h))
    return zero, bars


def bars(name, points):
    """The bar chart itself (fin-chart), shared by bond-details2 and 3."""
    vals = [v for _, v in points]
    zero, extents = scale(vals)
    neg, pos = any(v < 0 for v in vals), any(v > 0 for v in vals) or not any(vals)
    cols = []
    for k, ((year, v), (top, h)) in enumerate(zip(points, extents)):
        kind = "neg" if v < 0 else "pos"
        cols.append(
            '<li class="fin-col fin-col--%s" style="--i:%d">'
            '<span class="fin-bar" style="top:%.2f%%;height:%.2f%%"><span class="fin-bar__fill"></span>'
            '<span class="fin-bar__value">%s</span></span>'
            '<span class="fin-col__year">%s</span></li>' % (kind, k, top, h, crore(v), year))
    label = "; ".join("%s %s" % (y, crore(v).replace("&#8377;", "Rs ")) for y, v in points)
    return (
        '<div class="fin-chart%s%s" role="img" aria-label="%s: %s">'
        '<div class="fin-plot"><span class="fin-zero" style="top:%.2f%%"></span><ol class="fin-cols">%s</ol></div></div>'
    ) % (" fin-chart--neg" if neg else "", " fin-chart--pos" if pos else "",
         name.replace("&", "&amp;"), label, zero, "".join(cols))


def chart(name, points, idx):
    pill = SUBTITLE.get(name)
    head = ('<header class="flex min-h-[22px] items-center justify-start"><span class="inline-flex h-[22px] shrink-0 items-center justify-center rounded-full bg-light-yellow px-[10px] py-px text-xs leading-[16.5px] font-medium text-bond-financial-accent max-w-none text-left">%s</span></header>' % pill) if pill else ""
    return (
        '<div class="bond-company-financials-mobile-card__panel" role="tabpanel" id="fin-panel-%d" aria-labelledby="fin-tab-%d"%s '
        'style="padding-inline:12px;padding-top:13px;min-height:252px"><article class="flex flex-col">%s%s'
        '</article></div>'
    ) % (idx, idx, "" if idx == 0 else " hidden", head, bars(name, points))


def tabs(data):
    btns = []
    for i, (name, _) in enumerate(data):
        n = name.replace("&", "&amp;")
        btns.append(
            '<button type="button" role="tab" id="fin-tab-%d" aria-controls="fin-panel-%d" aria-selected="%s" tabindex="%d" '
            'class="bond-company-financials-tab-button flex shrink-0 cursor-pointer flex-col items-center border-none bg-transparent p-0 transition-[color] duration-200 ease-out motion-reduce:transition-none">'
            '<span class="inline-block pb-[9px]"><span class="bond-company-financials-tab-label">'
            '<span class="bond-company-financials-tab-label__sizer text-icon-gold text-xs font-bold leading-[35px] tracking-[0.0833em]" aria-hidden="true">%s</span>'
            '<span class="bond-company-financials-tab-label__sizer text-icon-gold text-[10px] font-bold leading-[12.81px] tracking-[0.1em] uppercase" aria-hidden="true">%s</span>'
            '<span class="fin-tab-text %s">%s%s</span></span></span></button>'
            % (i, i, "true" if i == 0 else "false", 0 if i == 0 else -1, n, n, TAB_ON if i == 0 else TAB_OFF, n, UNDERLINE if i == 0 else ""))
    return (
        '<div class="bond-company-financials-mobile-card fin-card">'
        '<div class="bond-company-financials-mobile-card__tab-bar bg-financial-tab relative overflow-visible" style="min-height:48px">'
        '<div class="bond-company-financials-mobile-card__tab-scroll flex items-start overflow-x-auto overflow-y-visible" role="tablist" aria-label="Company Financials" style="gap:20px;padding-inline:20px;padding-top:9px">'
        '%s</div></div>%s</div>' % ("".join(btns), "".join(chart(n, p, i) for i, (n, p) in enumerate(data))))


STYLE2 = """
<style>
/* bond-details2: the merged financials chart. Colours and type are beta's
   bar-graph tokens; the red for losses is their --color-red-600. */
.fin-chart { padding: 10px 8px 20px; }
.fin-plot { position: relative; height: 200px; margin: 0 4px; }
/* Room for the value labels: above the plot when bars rise, below when they hang. */
.fin-chart--pos .fin-plot { margin-top: 26px; }
.fin-chart--neg .fin-plot { margin-bottom: 26px; }
.fin-zero { position: absolute; left: 0; right: 0; height: 1px; background: var(--light-stroke); }
.fin-chart--neg .fin-zero { background: var(--subtext); opacity: .35; }
.fin-cols { position: absolute; inset: 0; display: grid; grid-auto-flow: column; grid-auto-columns: 1fr; margin: 0; padding: 0; list-style: none; }
.fin-col { position: relative; }
.fin-bar { position: absolute; left: 50%; width: min(56px, 46%); transform: translateX(-50%); }
.fin-bar__fill { position: absolute; inset: 0; min-height: 2px; border-radius: 6px 6px 2px 2px;
  background: linear-gradient(180deg, var(--bar-graph-gold-gradient-start), var(--bar-graph-gold-gradient-end));
  transform-origin: bottom; }
.fin-col--neg .fin-bar__fill { border-radius: 2px 2px 6px 6px; transform-origin: top;
  background: linear-gradient(0deg, #f58a8a, var(--color-red-600, #e40014)); }
.fin-bar__value { position: absolute; left: 50%; transform: translateX(-50%); white-space: nowrap;
  font-size: var(--bar-graph-gold-value-size-desktop); font-weight: var(--bar-graph-gold-value-weight);
  line-height: var(--bar-graph-gold-value-lh); color: var(--bar-graph-gold-value-color); }
.fin-col--pos .fin-bar__value { bottom: 100%; margin-bottom: 4px; }
.fin-col--neg .fin-bar__value { top: 100%; margin-top: 4px; color: var(--color-red-600, #e40014); }
.fin-col__year { position: absolute; left: 0; right: 0; bottom: -26px; text-align: center;
  font-size: var(--bar-graph-gold-axis-size); font-weight: var(--bar-graph-gold-axis-weight); color: var(--bar-graph-gold-axis-color); }
.fin-chart { padding-bottom: 34px; }
/* A negative bar's label sits where the year would; drop the year below it. */
.fin-chart--neg .fin-col__year { bottom: -52px; }
.fin-chart--neg { padding-bottom: 60px; }
@media (max-width: 1023px) {
  .fin-plot { height: 170px; }
  .fin-bar__value { font-size: var(--bar-graph-gold-value-size-mobile); font-weight: var(--bar-graph-gold-value-weight-mobile); }
  .fin-col__year { font-weight: var(--bar-graph-gold-axis-weight-mobile); color: var(--bar-graph-gold-axis-color-mobile); }
}
/* The fill animation. Only armed once the script runs (html.fin-js), so the
   chart is complete without it; is-drawn replays it on every tab switch. */
.fin-js .fin-bar__fill { transform: scaleY(0); transition: transform .7s cubic-bezier(.22,.8,.26,1) calc(var(--i) * 90ms); }
.fin-js .fin-bar__value { opacity: 0; transition: opacity .3s ease calc(var(--i) * 90ms + .45s); }
.fin-js .is-drawn .fin-bar__fill { transform: scaleY(1); }
.fin-js .is-drawn .fin-bar__value { opacity: 1; }
@media (prefers-reduced-motion: reduce) {
  .fin-js .fin-bar__fill, .fin-js .fin-bar__value { transition: none; }
}
.fin-card { margin-bottom: 4px; }
.fin-ratios-head { display: flex; align-items: center; gap: 12px; margin: 22px 0 12px; font-size: 16px; line-height: 24px; font-weight: 700; color: var(--darker-brown); }
</style>
"""

SCRIPT2 = """
<script>
// Financials tabs and the bar fill. Tab markup and classes are beta's.
(function () {
  var card = document.querySelector('.fin-card');
  if (!card) return;
  document.documentElement.classList.add('fin-js');
  var tabs = [].slice.call(card.querySelectorAll('[role=tab]'));
  var line = card.querySelector('.company-financials-tab-indicator__image');
  var ON = %s, OFF = %s;
  function draw(panel) {
    var c = panel.querySelector('.fin-chart');
    c.classList.remove('is-drawn');
    void c.offsetWidth;  // restart the transition
    c.classList.add('is-drawn');
  }
  function select(t) {
    tabs.forEach(function (x) {
      var on = x === t, text = x.querySelector('.fin-tab-text');
      x.setAttribute('aria-selected', on);
      x.tabIndex = on ? 0 : -1;
      text.className = 'fin-tab-text ' + (on ? ON : OFF);
      if (on) text.appendChild(line);
      document.getElementById(x.getAttribute('aria-controls')).hidden = !on;
    });
    draw(document.getElementById(t.getAttribute('aria-controls')));
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { select(t); });
    t.addEventListener('keydown', function (e) {
      var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if (!d) return;
      var n = tabs[(i + d + tabs.length) %% tabs.length];
      n.focus(); select(n);
    });
  });
  // First fill when the chart scrolls into view (or its section is opened).
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      draw(card.querySelector('[role=tabpanel]:not([hidden])'));
      io.disconnect();
    });
  }, { threshold: 0.35 });
  io.observe(card);
})();
</script>
""" % (repr(TAB_ON), repr(TAB_OFF))


def merge_financials(html, data, render=None):
    """Swap the four charts for the tabbed one; move Financial Ratio inside.

    render(data, fy, ratios_html) -> section body; bond-details3 passes its own.
    """
    # Lift the ratios panel out, then delete its own section.
    r0 = html.index('class="gp-expand gp-expand--card ipo-collapsible-section bond-financial-ratios-section"')
    r0 = html.rfind("<div ", 0, r0)
    ri, rj = span(html, html[r0:r0 + 200].split(">")[0], r0)
    ratios_section = html[ri:rj]
    pi, pj = span(ratios_section, '<div data-testid="bond-financial-ratios">')
    ratios = re.sub(r'<button type="button" class="bond-company-financials-disclaimer-link[^"]*">Important Disclaimer</button>', "", ratios_section[pi:pj])
    fy = re.search(r"</span>(FY \d{4}-\d{2})</span>", ratios_section).group(1)
    html = html[:ri] + html[rj:]

    ci, cj = span(html, '<div data-testid="bond-company-financials">')
    if render:  # bond-details3 keeps beta's title, "Company Financials"
        return html[:ci] + render(data, fy, ratios) + html[cj:]
    head = (
        '<h3 class="fin-ratios-head">Financial Ratio'
        '<span class="text-darker-brown inline-flex items-center gap-2 text-sm leading-3 font-bold tracking-[0.02em] uppercase">'
        '<span class="size-2 shrink-0 rounded-full bg-[var(--bond-ratio-good-text)]" aria-hidden="true"></span>%s</span></h3>' % fy)
    # Beta's "Important Disclaimer" links (charts and ratios) are left out of this version.
    new = ('<div data-testid="bond-company-financials"><div class="flex flex-col gap-3.5">%s</div>%s%s</div>'
           % (tabs(data), head, ratios))
    # The section title names both halves now.
    html = html[:ci] + new + html[cj:]
    return html.replace('<span class="gp-expand__title">Company Financials</span>',
                        '<span class="gp-expand__title">Company Financials &amp; Ratios</span>', 1)


# About the Issuer tiles for bond-details2, as the user specified on 2026-10-06.
# PAT here is the user's figure; the capture's own data says INR 30Cr (FY2026).
ISSUER_TILES = [("Annual Revenue", "210 CR (FY - 26)"), ("Year of Inception", "1981"), ("PAT", "56Cr")]


def issuer_tiles(html):
    """Replace both About the Issuer fact lists (desktop and mobile) with ISSUER_TILES."""
    for kind in ("desktop", "mobile"):
        tiles = "".join(
            '<div class="about-issuer__fact--ncd-%s"><dt class="about-issuer__fact-label">%s</dt>'
            '<dd class="about-issuer__fact-value">%s</dd></div>' % (kind, k, v) for k, v in ISSUER_TILES)
        html, n = re.subn(r'(<dl class="m-0 about-issuer__facts--ncd-%s">).*?(</dl>)' % kind,
                          lambda m: m.group(1) + tiles + m.group(2), html, count=1, flags=re.S)
        if not n:
            raise SystemExit("About the Issuer %s facts not found" % kind)
    return html


# App download block for bond-details2, after the last section. Beta shows this
# QR as a floating nudge (removed above); here it sits in the flow. Copy is
# beta's own: mobileAppDownloadNudge.downloadLabel and .qrAlt.
APP_BLOCK = (
    '<section class="gp-expand gp-expand--card bd2-app" aria-labelledby="bd2-app-h">'
    '<div class="bd2-app__text"><h2 id="bd2-app-h" class="bd2-app__title">Download App</h2>'
    '<p class="bd2-app__sub">Scan to download GoldenPi app and get voucher</p></div>'
    '<img class="bd2-app__qr" src="../assets/beta/media/mobile-app-qr.3wptrea2l_26s.svg" '
    'alt="Scan to download GoldenPi app and get voucher" width="153" height="189" loading="lazy">'
    '</section>')

APP_STYLE = """
<style>
.bd2-app { display: flex; align-items: center; justify-content: space-between; gap: 20px; padding: 20px 24px; }
.bd2-app__title { margin: 0; font-size: 16px; line-height: 24px; font-weight: var(--font-weight-bold, 700); color: var(--darker-brown); }
.bd2-app__sub { margin: 4px 0 0; font-size: 14px; line-height: 20px; color: var(--subtext); }
.bd2-app__qr { flex: none; width: 153px; height: 189px; border-radius: 20px; box-shadow: 0 8px 24px #5148341f; }
@media (max-width: 479px) { .bd2-app { flex-direction: column; text-align: center; } }
</style>
"""


def app_block(html):
    """Insert APP_BLOCK after the last gp-expand section (Cashflow)."""
    last = html.rindex('<div class="gp-expand gp-expand--card')
    _, end = span(html, '<div class="gp-expand gp-expand--card', last)
    return html[:end] + APP_BLOCK + html[end:]


# Footer for bond-details2: pages/footer-ggn-login.html's footer replaces beta's.
# Its styles are an inline block on that page plus the .ft rules in final.css;
# only those rules come across, since the rest of final.css would restyle
# beta's own gp-* classes. Read at build time, so footer-ggn-login edits follow.
FOOTER_SRC = os.path.join(ROOT, "pages/footer-ggn-login.html")


def css_rules(css, keep):
    """Top-level rules (and @media blocks, filtered inside) whose selector passes keep()."""
    out, i, n = [], 0, len(css)
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    n = len(css)
    while i < n:
        j = css.find("{", i)
        if j < 0:
            break
        sel = css[i:j].strip()
        depth, k = 1, j + 1
        while depth and k < n:
            depth += {"{": 1, "}": -1}.get(css[k], 0)
            k += 1
        body = css[j + 1:k - 1]
        if sel.startswith("@media") or sel.startswith("@supports"):
            inner = css_rules(body, keep)
            if inner:
                out.append("%s {\n%s\n}" % (sel, inner))
        elif not sel.startswith("@") and keep(sel):
            out.append("%s {%s}" % (sel, body))
        i = k
    return "\n".join(out)


def footer_login4(html):
    src = open(FOOTER_SRC).read()
    foot = re.search(r'<footer class="ft\b.*?</footer>', src, re.S).group(0)
    styles = "\n".join(b for b in re.findall(r"<style>(.*?)</style>", src, re.S) if ".ft" in b)
    final = css_rules(open(os.path.join(ROOT, "assets/final.css")).read(),
                      lambda sel: all(re.match(r"\s*\.ft\b", x) for x in sel.split(",")))
    # gp-shell is site.css's content width; scoped so it only sizes the footer and navbar.
    shell = css_rules(open(os.path.join(ROOT, "assets/site.css")).read(),
                      lambda sel: sel.strip() == ".gp-shell").replace(".gp-shell", ".ft .gp-shell, .nb .gp-shell")
    script = [b for b in re.findall(r"<script>(.*?)</script>", src, re.S) if ".ft-love" in b]
    i = html.index('<footer class="site-footer"')
    j = html.index("</footer>", i) + len("</footer>")
    html = html[:i] + foot + html[j:]
    # The two site.css tokens those rules lean on, scoped to the footer and
    # navbar (both size their gp-shell with --gp-max).
    tokens = ".ft, .nb { --gp-max: 1200px; --ease: cubic-bezier(0.22, 0.61, 0.36, 1); }"
    html = html.replace("</head>", "<style>\n/* footer-ggn-login */\n%s\n%s\n%s\n%s\n</style>\n</head>" % (tokens, shell, final, styles), 1)
    return html.replace("</body>", "".join("<script>%s</script>" % b for b in script) + "</body>", 1)


# Navbar for bond-details2: "Logged in, dark, without icons" from
# pages/navbar-variants.html replaces beta's site-header. Its styles are the
# nb-scoped assets/navbar.css; beta's promo strip above the header stays.
NAVBAR_SRC = os.path.join(ROOT, "pages/navbar-variants.html")


def navbar(html):
    src = open(NAVBAR_SRC).read()
    i, j = span(src, '<div class="nb nb--dark nb--plain" data-v="plain-dark-login">')
    a = html.index('<header class="site-header">')
    b = html.index("</header>", a) + len("</header>")
    html = html[:a] + "<header>" + src[i:j] + "</header>" + html[b:]
    return html.replace("</head>", '<link rel="stylesheet" href="../assets/navbar.css">\n</head>', 1)


def chrome(html):
    """bond-details2: no announcement toast or issuer rows, one side gutter.

    Beta's content shell is 1200px with --issuer-gutter 15px, dropping to 0
    from 1024px up, so on desktop it ran 20px wider each side than the navbar
    and footer (gp-shell: 1200px, 20px gutter) and met the screen edge between
    1024 and 1200px. One 20px gutter at every width lines all three up.
    """
    html = drop(html, '<div class="gp-toast"')
    # The logo + issuer-name row atop Strength / Weaknesses and Documents.
    html = drop(html, '<div class="strengths-weaknesses__ncd-heading"')
    html = drop(html, '<div class="bond-documents-hero"')
    return html.replace("</head>", "<style>:root { --issuer-gutter: 20px !important; }</style>\n</head>", 1)


# Cashflow for bond-details2: Interest and Principal columns, no TDS anywhere
# in it (the on-page section and the Timeline modal share this markup).
# Beta's columns are "Total Receivable*" (each payout as interest + principal)
# and "After 10% TDS*". Both new columns come from the first one, so every
# figure is a pre-TDS value beta itself shows; year totals are summed here.
ROW = re.compile(
    r'(<td class="[^"]*bond-cashflow-col-receivable-cell">)<div class="bond-cashflow-receivable-cell bond-cashflow-receivable-cell--split">'
    r'<span class="bond-cashflow-receivable-amount-line">₹ ([\d,]+\.\d\d)<span class="bond-cashflow-plus-icon"> \+ </span>₹ ([\d,]+\.\d\d)</span>'
    r'<span class="bond-cashflow-receivable-desc">[^<]*</span></div></td>'
    r'(<td class="[^"]*bond-cashflow-col-net-cell">)<div class="bond-cashflow-receivable-cell bond-cashflow-receivable-cell--split">.*?</div></td>')
YEAR_TDS = re.compile(r'(<td class="bond-cashflow-year-amount [^"]*">)₹ ([\d,]+\.\d\d)</td>(<td class="bond-cashflow-year-amount [^"]*">)₹ [\d,]+\.\d\d</td>')


def money(text):
    return Decimal(text.replace(",", ""))


def inr(d):
    """Decimal -> '₹ 1,23,456.78' (Indian grouping, two places)."""
    whole, frac = ("%.2f" % d).split(".")
    if len(whole) > 3:
        head, tail = whole[:-3], whole[-3:]
        whole = ",".join([head[max(0, k - 2):k] for k in range(len(head), 0, -2)][::-1]) + "," + tail
    return "₹ %s.%s" % (whole, frac)


def cell(td, amount):
    return '%s<div class="bond-cashflow-receivable-cell"><span class="bond-cashflow-receivable-amount-line">%s</span></div></td>' % (td, amount)


def cashflow_split(html):
    log = []

    def year(block):
        rows = ROW.findall(block)
        n_rows = block.count('<tr class="bond-cashflow-payout-row">')
        if not rows or len(rows) != n_rows:
            raise SystemExit("cashflow: parsed %d of %d payout rows" % (len(rows), n_rows))
        interest = sum(money(i) for _, i, _, _ in rows)
        principal = sum(money(p) for _, _, p, _ in rows)
        m = YEAR_TDS.search(block)
        gross = money(m.group(2))
        if abs(interest + principal - gross) > Decimal("0.01"):
            raise SystemExit("cashflow: %s + %s != beta's %s" % (interest, principal, gross))
        yr = re.search(r"</span>(\d{4})</span></td>", block).group(1)
        log.append((yr, len(rows), interest, principal, gross))
        block = ROW.sub(lambda r: cell(r.group(1), "₹ " + r.group(2)) + cell(r.group(4), "₹ " + r.group(3)), block)
        block = YEAR_TDS.sub(lambda r: "%s%s</td>%s%s</td>" % (r.group(1), inr(interest), r.group(3), inr(principal)), block, count=1)
        # Mobile shows one figure per year: the year's total, before TDS.
        return re.sub(r'(<span class="bond-cashflow-year-header-mobile__amount">)₹ [\d,]+\.\d\d', lambda r: r.group(1) + inr(interest + principal), block, count=1)

    out, at = [], 0
    while True:
        k = html.find('<div class="bond-cashflow-timeline">', at)
        if k < 0:
            break
        i, j = span(html, '<div class="bond-cashflow-timeline">', k)
        out.append(html[at:i] + year(html[i:j]))
        at = j
    html = "".join(out) + html[at:]

    for old, new in (
        ('text-left">Total Receivable*</th>', 'text-left">Interest</th>'),
        ('text-left">After 10% TDS*</th>', 'text-left">Principal</th>'),
        ('<th scope="col">Total Receivable*</th><th scope="col">Payout</th>', '<th scope="col">Interest</th><th scope="col">Principal</th>'),
        ('<span class="bond-cashflow-mobile-payout-header__payout">Payout</span>',
         '<span class="bond-cashflow-mobile-payout-header__payout">Interest</span><span class="bond-cashflow-mobile-payout-header__payout">Principal</span>'),
        ('<p class="bond-cashflow-tds-disclaimer m-0">*10% TDS For Resident Indians. File Form 121 To Avoid TDS</p>', ""),
    ):
        if old not in html:
            raise SystemExit("cashflow: not found: " + old)
        html = html.replace(old, new)
    # "(Part Maturity)" under each date goes; the final "(Maturity)" stays.
    part = '<span class="bond-cashflow-maturity-label mt-0.5 block">(Part Maturity)</span>'
    if part not in html:
        raise SystemExit("cashflow: no (Part Maturity) labels found")
    html = html.replace(part, "")
    while '<div class="bond-cashflow-payout-toggle-wrap' in html:
        html = drop(html, '<div class="bond-cashflow-payout-toggle-wrap')

    # Nothing about TDS may remain in the Cashflow section or the modal.
    first = html.index('class="bond-cashflow-content')
    sec = html.rfind('<div class="gp-expand gp-expand--card', 0, first)
    for name, (i, j) in (("section", span(html, '<div class="gp-expand gp-expand--card', sec)),
                         ("modal", span(html, '<div id="cashflow-modal"'))):
        if "TDS" in html[i:j]:
            k = html.index("TDS", i)
            raise SystemExit("cashflow %s: TDS still present: %s" % (name, re.sub(r"<[^>]+>", " ", html[k - 120:k + 40])))
    for yr, n, i, p, g in log:
        print("  cashflow %s: %d payout(s)  interest %s  principal %s  = %s (beta pre-TDS %s)" % (yr, n, inr(i), inr(p), inr(i + p), inr(g)))
    return html.replace("</head>", CASHFLOW_STYLE + "</head>", 1)


# Beta's mobile table collapses the first amount column to width 0 and shows
# only the second; with two real columns both must show, and the mobile header
# grows a third track to match.
CASHFLOW_STYLE = """<style>
@media (max-width: 1023px) {
  .bond-cashflow-content .bond-cashflow-col-receivable,
  .bond-cashflow-content .bond-cashflow-inner-table--payouts col.bond-cashflow-col-receivable { width: auto; }
  .bond-cashflow-content .bond-cashflow-col-receivable-cell {
    display: table-cell; text-align: left; vertical-align: top;
    padding-left: var(--bond-cashflow-mobile-payout-pl); padding-right: 0;
  }
  .bond-cashflow-mobile-payout-header {
    grid-template-columns: var(--bond-cashflow-mobile-date-header-width) minmax(0, 1fr) minmax(0, 1fr);
  }
}
</style>
"""


# ------------------------------------------------------------ bond-details3
# bond-details2 with a design pass on the parts built for it (taste:redesign).
# Copy and figures are unchanged; the only new numbers are year-on-year
# changes, computed from beta's own series.

def ratio_list(ratios_html):
    """[(label, value, assessment, tone)] from beta's desktop ratio list."""
    out = re.findall(
        r'<p class="text-darker-brown col-start-1[^"]*">([^<]+)</p>.*?--bond-ratio-(\w+)-text.*?'
        r'ratio-assessment-label[^"]*">([^<]+)</span>.*?<span class="text-darker-brown col-start-5[^"]*">([^<]+)</span>',
        ratios_html, re.S)
    if len(out) != ratios_html.count("ratio-assessment-label") // 2 or not out:
        raise SystemExit("ratios: parsed %d rows" % len(out))
    return [(label, value, assessment, tone) for label, tone, assessment, value in out]


def change(points):
    """(pct, prev_year) for the last value against the one before, or None."""
    if len(points) < 2 or points[-2][1] == 0:
        return None
    (py, pv), (_, lv) = points[-2], points[-1]
    return (lv - pv) / abs(pv) * 100, py


def fin_v3(data, fy, ratios_html, ratios=None):
    """ratios: [(label, value, assessment, tone)] in place of parsing beta's markup."""
    tabs, panels = [], []
    for i, (name, points) in enumerate(data):
        n = name.replace("&", "&amp;")
        on = i == 0
        tabs.append('<button type="button" role="tab" class="f3-tab" id="f3-tab-%d" aria-controls="f3-panel-%d" aria-selected="%s" tabindex="%d">%s</button>'
                    % (i, i, "true" if on else "false", 0 if on else -1, n))
        year, last = points[-1]
        delta = change(points)
        meta = ""
        if delta:
            pct, prev = delta
            up = pct >= 0
            meta = ('<p class="f3-meta"><span class="f3-delta f3-delta--%s">%s %.1f%%</span> vs %s</p>'
                    % ("up" if up else "down", "&#9650;" if up else "&#9660;", abs(pct), prev))
        eyebrow = SUBTITLE.get(name, name)
        panels.append(
            '<div class="f3-panel" role="tabpanel" id="f3-panel-%d" aria-labelledby="f3-tab-%d"%s>'
            '<div class="f3-callout"><p class="f3-eyebrow">%s</p><p class="f3-figure">%s</p><p class="f3-year">%s</p>%s</div>'
            '%s</div>' % (i, i, "" if on else " hidden", eyebrow.replace("&", "&amp;"), crore(last), year, meta, bars(name, points)))
    tiles = "".join(
        '<div class="f3-ratio" style="--t:var(--bond-ratio-%s-text);--s:var(--bond-ratio-%s-surface);--b:var(--bond-ratio-%s-border)">'
        '<dt>%s</dt><dd>%s</dd><span class="f3-chip">%s</span></div>' % (tone, tone, tone, label, value, assessment)
        for label, value, assessment, tone in ratios or ratio_list(ratios_html))
    return (
        '<div data-testid="bond-company-financials" class="f3">'
        '<div class="f3-tabs" role="tablist" aria-label="Company Financials">%s</div>%s'
        '<div class="f3-ratios"><h3 class="f3-ratios__head">Financial Ratio<span class="f3-fy">%s</span></h3>'
        '<dl class="f3-ratio-grid">%s</dl></div></div>' % ("".join(tabs), "".join(panels), fy, tiles))


APP_BLOCK3 = (
    '<section class="gp-expand gp-expand--card a3" aria-labelledby="a3-h">'
    '<div class="a3__text"><h2 id="a3-h" class="a3__title">Download App</h2>'
    '<p class="a3__sub">Scan to download GoldenPi app and get voucher</p></div>'
    '<img class="a3__qr" src="../assets/beta/media/mobile-app-qr.3wptrea2l_26s.svg" '
    'alt="Scan to download GoldenPi app and get voucher" width="153" height="189" loading="lazy">'
    '</section>')


def app_block3(html):
    return app_block(html).replace(APP_BLOCK, APP_BLOCK3, 1)


STYLE3 = """
<style>
/* bond-details3: design pass on the merged financials, ratios, app band. */
.f3 { display: grid; gap: 20px; }
.f3-tabs { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 4px; padding: 4px;
  border-radius: 9999px; background: #faf6ec; border: 1px solid var(--light-yellow); }
.f3-tab { border: 0; border-radius: 9999px; padding: 10px 8px; background: transparent; cursor: pointer;
  font: inherit; font-size: 13px; line-height: 1.2; font-weight: 700; color: var(--subtext);
  transition: background-color .2s ease, color .2s ease, box-shadow .2s ease; }
.f3-tab:hover { color: var(--darker-brown); }
.f3-tab:active { transform: translateY(1px); }
.f3-tab[aria-selected="true"] { background: var(--white); color: var(--darker-brown);
  box-shadow: 0 1px 2px rgba(80, 60, 10, .08), 0 0 0 1px var(--light-yellow); }
.f3-tab:focus-visible { outline: 2px solid var(--icon-gold); outline-offset: 2px; }

.f3-panel { display: grid; grid-template-columns: minmax(170px, .75fr) minmax(0, 1.6fr); gap: 8px 28px; align-items: end;
  padding: 22px 22px 6px; border-radius: 20px; border: 1px solid var(--light-yellow);
  background: radial-gradient(420px 200px at 0% 0%, rgba(212, 175, 55, .10), transparent 70%), var(--white); }
.f3-panel[hidden] { display: none; }
.f3-callout { align-self: start; display: grid; justify-items: start; gap: 6px; padding-top: 2px; }
.f3-eyebrow { margin: 0; padding: 2px 10px; border-radius: 9999px; background: var(--light-yellow);
  font-size: 12px; line-height: 18px; font-weight: 500; color: var(--bond-financial-accent); }
.f3-figure { margin: 8px 0 0; font-size: clamp(30px, 3.2vw, 38px); line-height: 1.05; font-weight: 700;
  letter-spacing: -0.02em; color: var(--darker-brown); font-variant-numeric: tabular-nums; }
.f3-year { margin: 0; font-size: 12px; font-weight: 500; color: var(--subtext); }
.f3-meta { margin: 6px 0 0; display: flex; align-items: center; gap: 6px; font-size: 12px; color: var(--subtext); }
.f3-delta { display: inline-flex; align-items: center; gap: 4px; padding: 3px 8px; border-radius: 6px;
  font-weight: 700; font-variant-numeric: tabular-nums; }
.f3-delta--up { color: #06963c; background: #eef8f1; }
.f3-delta--down { color: var(--color-red-600, #e40014); background: #fef2f2; }
/* The chart sits in the panel; earlier years recede so the latest leads. */
.f3 .fin-chart { padding-left: 0; padding-right: 0; }
.f3 .fin-plot { height: 180px; }
.f3 .fin-col:not(:last-child) .fin-bar__fill { background: linear-gradient(180deg, #f3e2a9, #ebd38c); }
.f3 .fin-col--neg:not(:last-child) .fin-bar__fill { background: linear-gradient(0deg, #fbd5d5, #f5a9a9); }
.f3 .fin-col:not(:last-child) .fin-bar__value { color: var(--subtext); font-weight: 500; }
.f3 .fin-bar__value { font-variant-numeric: tabular-nums; }

.f3-ratios__head { display: flex; align-items: center; gap: 12px; margin: 4px 0 12px;
  font-size: 16px; line-height: 24px; font-weight: 700; color: var(--darker-brown); }
.f3-fy { display: inline-flex; align-items: center; gap: 6px; font-size: 12px; font-weight: 700;
  letter-spacing: .02em; color: var(--subtext); }
.f3-fy::before { content: ""; width: 6px; height: 6px; border-radius: 50%; background: var(--bond-ratio-good-text); }
.f3-ratio-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin: 0; }
.f3-ratio { display: flex; flex-direction: column; gap: 4px; padding: 16px; border-radius: 16px;
  background: var(--white); border: 1px solid var(--light-stroke); transition: border-color .2s ease, transform .2s ease; }
.f3-ratio:hover { border-color: var(--light-yellow); transform: translateY(-1px); }
.f3-ratio dt { font-size: 12px; line-height: 16px; font-weight: 500; color: var(--subtext); }
.f3-ratio dd { margin: 0; font-size: 22px; line-height: 30px; font-weight: 700; letter-spacing: -0.01em;
  color: var(--darker-brown); font-variant-numeric: tabular-nums; }
.f3-chip { align-self: flex-start; margin-top: 4px; padding: 3px 8px; border-radius: 6px; border: 1px solid var(--b);
  background: var(--s); color: var(--t); font-size: 10px; line-height: 12px; font-weight: 700; letter-spacing: .08em; }

.a3 { display: grid !important; grid-template-columns: minmax(0, 1fr) auto; align-items: center; gap: 24px;
  padding: 20px 20px 20px 28px;
  background: radial-gradient(520px 220px at 0% 0%, rgba(212, 175, 55, .14), transparent 65%), var(--white) !important; }
.a3__title { margin: 0; font-size: 20px; line-height: 28px; font-weight: 700; letter-spacing: -0.01em; color: var(--darker-brown); }
.a3__sub { margin: 6px 0 0; max-width: 32ch; font-size: 14px; line-height: 21px; color: var(--subtext); text-wrap: pretty; }
.a3__qr { width: 116px; height: auto; border-radius: 16px; box-shadow: 0 8px 24px rgba(166, 124, 0, .16); }

/* Amounts line up in columns. */
[class*="cashflow"], [class*="calculator"], .about-issuer__fact-value { font-variant-numeric: tabular-nums; }

@media (max-width: 767px) {
  /* Size tabs to their labels so "Cash & Cash Eq." stays on one line. */
  .f3-tabs { display: flex; }
  .f3-tab { flex: 1 1 auto; white-space: nowrap; font-size: 12px; padding: 9px 10px; }
  .f3-panel { grid-template-columns: minmax(0, 1fr); padding: 18px 16px 4px; }
  .f3 .fin-plot { height: 150px; }
  .f3-ratio-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
  .f3-ratio { padding: 14px; }
  .a3 { gap: 16px; padding: 18px; }
  .a3__qr { width: 92px; }
}
</style>
"""

SCRIPT3 = """
<script>
// bond-details3 financials: tabs and the bar fill (same mechanism as v2).
(function () {
  var root = document.querySelector('.f3');
  if (!root) return;
  document.documentElement.classList.add('fin-js');
  var tabs = [].slice.call(root.querySelectorAll('[role=tab]'));
  function draw(panel) {
    var c = panel.querySelector('.fin-chart');
    c.classList.remove('is-drawn');
    void c.offsetWidth;  // restart the transition
    c.classList.add('is-drawn');
  }
  function select(t) {
    tabs.forEach(function (x) {
      var on = x === t;
      x.setAttribute('aria-selected', on);
      x.tabIndex = on ? 0 : -1;
      document.getElementById(x.getAttribute('aria-controls')).hidden = !on;
    });
    draw(document.getElementById(t.getAttribute('aria-controls')));
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { select(t); });
    t.addEventListener('keydown', function (e) {
      var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if (!d) return;
      var n = tabs[(i + d + tabs.length) % tabs.length];
      n.focus(); select(n);
    });
  });
  var io = new IntersectionObserver(function (es) {
    if (!es[0].isIntersecting) return;
    draw(root.querySelector('[role=tabpanel]:not([hidden])'));
    io.disconnect();
  }, { threshold: 0.35 });
  io.observe(root);
})();
</script>
"""


# Top card for bond-details3: beta's header and its five overview tiles become
# one dark card (the user's reference: logo in a gold ring, name, attributes,
# icon stats with dividers, sold meter). Every value is read from beta's own
# markup. The reference's "Sell Anytime" and "Form 121 Available" are not
# claims beta makes for this bond, so they are not here.
ICON = {  # 20px line icons, one stroke weight, drawn for this card
    "Returns": '<path d="M4 16l5-5 4 4 7-7"/><path d="M15 8h5v5"/>',
    "Tenure": '<rect x="3.5" y="5" width="17" height="15" rx="3"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
    "Payout": '<path d="M17 3l3 3-3 3"/><path d="M4 11V9a3 3 0 0 1 3-3h13"/><path d="M7 21l-3-3 3-3"/><path d="M20 13v2a3 3 0 0 1-3 3H4"/>',
    "Security": '<path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6z"/><path d="M9 12l2 2 4-4"/>',
}
GAUGE = ('<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke-width="2.6" stroke-linecap="round" aria-hidden="true">'
         '<path d="M4 16a8 8 0 0 1 3.1-6.3" stroke="#e5484d"/><path d="M9.5 8.4a8 8 0 0 1 5 0" stroke="#f0b429"/>'
         '<path d="M16.9 9.7A8 8 0 0 1 20 16" stroke="#30a46c"/>'
         '<path d="M12 16l3.2-4.4" stroke="#f4e9c8" stroke-width="1.8"/><circle cx="12" cy="16" r="1.6" fill="#f4e9c8" stroke="none"/></svg>')
SAVE = '<path d="M6 3.5h12a1 1 0 0 1 1 1V21l-7-4.5L5 21V4.5a1 1 0 0 1 1-1z"/><path d="M12 7.5v6M9 10.5h6"/>'


def svg(paths, size=20):
    return ('<svg viewBox="0 0 24 24" width="%d" height="%d" fill="none" stroke="currentColor" stroke-width="1.6" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (size, size, paths))


# The user's values for the card (2026-10-06): beta shows "CARE BBB+" and
# "3Y 1M 23D"; Security is dropped; the attribute line is reworded.
HEADER_VALUES = {"Credit rating": "BBB+", "Tenure": "38 Months"}
HEADER_DROP = {"Security"}
# Replaces beta's "Senior • Secured • Listed" under the name.
HEADER_ATTRS = "Senior Secured Bond"
# Replaces beta's all-caps "MAHAVEER" as the card's name.
HEADER_NAME = "Mahaveer"
# Stat order on the card: Payout and Credit rating swapped from beta's.
HEADER_ORDER = ["Returns", "Tenure", "Credit rating", "Payout"]
# The user's labels for the card (not in beta's data for this bond). Both are
# plain labels, not controls: the page has nowhere for them to go.
HEADER_SELL = "Sell Anytime"
HEADER_FORM = "Form 121 Available"


def header_card(html):
    a = html.index('<section aria-labelledby="bond-header-title">')
    o = html.index('<section aria-labelledby="bond-overview-title">', a)
    b = html.index("</section>", o) + len("</section>")
    head, over = html[a:o], html[o:b]
    name = re.search(r'<h1 id="bond-header-title" class="sr-only">([^<]+)</h1>', head).group(1)
    logo = re.search(r'<img [^>]*src="([^"]+)"', head).group(1)
    attrs = re.findall(r'</span>([A-Za-z]+)</li>|<li class="inline-flex items-center">([A-Za-z]+)</li>',
                       head[:head.index('</ul>')])
    attrs = [x or y for x, y in attrs]
    sold = int(re.search(r'aria-valuenow="(\d+)"', head).group(1))
    desktop = over[:over.index("</ul>")]
    stats = []
    for li in re.findall(r'<li class="bond-overview-tile bond-overview-tile--desktop.*?</li>', desktop, re.S):
        label = re.search(r'tile__label">([^<]+)<', li).group(1)
        # Everything after the label (and its info button) is the value: "12.00%", or "CARE" + "BBB+".
        rest = li[li.index('class="bond-overview-tile__value'):]
        value = " ".join(t.strip() for t in re.findall(r">([^<>]+)<", rest) if t.strip())
        stats.append((label, value))
    if [l for l, _ in stats] != ["Returns", "Tenure", "Payout", "Credit rating", "Security"] or len(attrs) != 3:
        raise SystemExit("header card: unexpected beta header %r %r" % (stats, attrs))
    stats = [(l, HEADER_VALUES.get(l, v)) for l, v in stats if l not in HEADER_DROP]
    stats.sort(key=lambda st: HEADER_ORDER.index(st[0]))
    filled = round(sold / 100 * 16)  # beta's meter has 16 segments
    items = []
    for label, value in stats:
        # Beta's rating-meter image has a white ground baked in; on the dark
        # card a drawn gauge (red, amber, green arcs and a needle) reads cleanly.
        icon = GAUGE if label == "Credit rating" else svg(ICON[label])
        items.append('<div class="hc-stat"><span class="hc-stat__icon">%s</span><div><dt>%s</dt><dd>%s</dd></div></div>'
                     % (icon, label, value))
    card = (
        '<section class="hc" aria-labelledby="bond-header-title">'
        '<div class="hc__top">'
        '<div class="hc__logo"><img src="%s" alt="Mahaveer Finance India Limited logo" width="64" height="64"></div>'
        '<div class="hc__id"><h1 id="bond-header-title" class="hc__name">%s</h1>'
        '<p class="hc__attrs">%s</p></div>'
        '<div class="hc__actions">'
        '<span class="hc__sell">%s</span>'
        '<button type="button" class="hc__btn" aria-label="Add to watchlist" aria-pressed="false">%s</button>'
        '</div></div>'
        '<h2 class="sr-only">Bond overview</h2><dl class="hc__stats">%s</dl>'
        '<div class="hc__foot"><div class="hc__soldrow"><span class="hc__sold">%d%% Sold Out</span>'
        '<span class="hc__meter" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="%d" aria-label="%d%% Sold Out">%s</span></div>'
        '<span class="hc__form">%s</span>'
        '</div></section>'
    ) % (logo, HEADER_NAME, HEADER_ATTRS,
         HEADER_SELL, svg(SAVE, 18), "".join(items), sold, sold, sold,
         "".join('<i class="%s"></i>' % ("on" if k < filled else "") for k in range(16)), HEADER_FORM)
    html = html[:a] + card + html[b:]
    # No share anywhere on the page: beta's mobile top bar carries one as well.
    share = '<div class="relative inline-flex shrink-0"><button type="button" class="bond-header-action-trigger" aria-label="Share bond"'
    if share not in html:
        raise SystemExit("header card: beta's mobile share button not found")
    while share in html:
        html = drop(html, share)
    return html.replace("</head>", HEADER_STYLE + "</head>", 1)


HEADER_STYLE = """<style>
/* bond-details3 top card. Dark warm ground, gold accents; values are beta's. */
.hc { --hc-ink: #f4e9c8; --hc-muted: #b8a88a; --hc-line: rgba(244, 233, 200, .10);
  position: relative; overflow: hidden; border-radius: 24px; padding: 24px 28px 20px; color: var(--hc-ink);
  background: radial-gradient(120% 140% at 0% 0%, #2b2417 0%, #14110c 52%, #0c0b08 100%);
  box-shadow: 0 18px 40px -18px rgba(40, 28, 6, .55); }
.hc::after { content: ""; position: absolute; inset: 0; pointer-events: none; border-radius: inherit;
  box-shadow: inset 0 1px 0 rgba(244, 233, 200, .08); }
.hc__top { display: flex; align-items: center; gap: 18px; }
.hc__logo { flex: none; width: 72px; height: 72px; padding: 2px; border-radius: 50%;
  background: linear-gradient(167deg, #f7d880, #d4af37 50%, #8a6520); }
.hc__logo img { width: 100%; height: 100%; border-radius: 50%; object-fit: cover; background: #f7f5f2; border: 2px solid #14110c; }
.hc__id { flex: 1; min-width: 0; }
.hc__name { margin: 0; font-size: 28px; line-height: 34px; font-weight: 700; letter-spacing: -0.01em; color: var(--hc-ink); }
.hc__attrs { margin: 4px 0 0; display: flex; flex-wrap: wrap; gap: 8px; font-size: 14px; line-height: 20px; color: var(--hc-muted); }
.hc__attrs [aria-hidden] { opacity: .6; }
.hc__actions { display: flex; align-items: center; gap: 10px; align-self: flex-start; }
.hc__sell { display: inline-flex; align-items: center; height: 44px; padding: 0 18px; border-radius: 9999px;
  border: 1px solid rgba(212, 175, 55, .35); background: rgba(212, 175, 55, .06);
  font-size: 14px; line-height: 20px; font-weight: 700; color: #f0cf6a; white-space: nowrap; }
.hc__btn { width: 44px; height: 44px; display: grid; place-items: center; border-radius: 50%; cursor: pointer;
  color: var(--hc-ink); background: rgba(244, 233, 200, .04); border: 1px solid rgba(244, 233, 200, .16);
  transition: background-color .2s ease, border-color .2s ease, transform .15s ease; }
.hc__btn:hover { background: rgba(244, 233, 200, .10); border-color: rgba(212, 175, 55, .55); }
.hc__btn:active { transform: scale(.96); }
.hc__btn:focus-visible { outline: 2px solid #d4af37; outline-offset: 2px; }

/* Each divider is a flexible spacer with the line centred in it, so the gap
   from the line to the stat on either side is always the same. The 10px
   margin matches the gap the spacer leaves before the next icon. */
.hc__stats { margin: 22px 0 0; display: flex; align-items: center; }
.hc-stat { flex: none; display: flex; align-items: center; gap: 10px; }
.hc-stat + .hc-stat { flex: 1 1 auto; margin-left: 10px; }
.hc-stat + .hc-stat::before { content: ""; flex: 1 1 0; min-width: 24px; align-self: stretch;
  background: linear-gradient(var(--hc-line), var(--hc-line)) center / 1px 100% no-repeat; }
.hc-stat__icon { flex: none; width: 36px; height: 36px; display: grid; place-items: center; border-radius: 12px;
  color: #f0cf6a; background: radial-gradient(circle at 30% 25%, rgba(240, 207, 106, .22), rgba(240, 207, 106, .06)); }
.hc-stat dt { font-size: 13px; line-height: 18px; color: var(--hc-muted); white-space: nowrap; }
.hc-stat dd { margin: 2px 0 0; font-size: 17px; line-height: 22px; font-weight: 700; color: var(--hc-ink);
  white-space: nowrap; font-variant-numeric: tabular-nums; }

.hc__foot { margin-top: 20px; padding-top: 16px; border-top: 1px solid var(--hc-line);
  display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 12px; }
.hc__soldrow { display: flex; align-items: center; gap: 12px; }
.hc__form { display: inline-flex; align-items: center; height: 32px; padding: 0 14px; border-radius: 9999px;
  border: 1px dashed rgba(244, 233, 200, .28); font-size: 13px; line-height: 18px; font-weight: 500;
  color: var(--hc-ink); white-space: nowrap; }
.hc__sold { font-size: 13px; line-height: 18px; font-weight: 700; color: var(--hc-ink); }
.hc__meter { display: inline-flex; gap: 3px; }
.hc__meter i { width: 9px; height: 7px; border-radius: 2px; background: rgba(244, 233, 200, .14); }
.hc__meter i.on { background: linear-gradient(180deg, #f7d880, #c99a1c); }

/* Two per row: the line sits in the middle of the column gap. */
@media (max-width: 1100px) {
  .hc__stats { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px 24px; }
  .hc-stat, .hc-stat + .hc-stat { position: relative; margin-left: 0; }
  .hc-stat + .hc-stat::before { display: none; }
  .hc-stat:nth-child(even)::after { content: ""; position: absolute; left: -12px; top: 0; bottom: 0;
    width: 1px; background: var(--hc-line); }
}
@media (max-width: 767px) {
  .hc { border-radius: 20px; padding: 18px 16px 16px; }
  .hc__logo { width: 56px; height: 56px; }
  .hc__name { font-size: 22px; line-height: 28px; }
  .hc__attrs { font-size: 13px; }
  .hc__btn { display: none; }  /* beta's mobile top bar already has the watchlist button */
  .hc__sell { height: 32px; padding: 0 12px; font-size: 12px; }
  .hc__top { flex-wrap: wrap; }
  .hc__stats { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .hc-stat__icon { width: 32px; height: 32px; border-radius: 10px; }
  .hc-stat dd { font-size: 15px; }
  .hc__meter i { width: 7px; }
}
</style>
"""


# Highlights block for bond-details3, below the top card (user's reference,
# 2026-10-06). Reasons to Invest is beta's; Sell Anytime and the security
# cover are the user's. The rest is the reference's figures as sample
# data, marked in markup (DATA: placeholder) and on screen (dashed underline,
# "Sample data" tooltip) until real Mahaveer figures replace them.
HL_ICON = {
    "reasons": '<path d="M9 6h11M9 12h11M9 18h11"/><path d="M3.5 6l1.2 1.2L7 5M3.5 12l1.2 1.2L7 11M3.5 18l1.2 1.2L7 17"/>',
    "cover": '<path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6z"/><rect x="9" y="10.5" width="6" height="5" rx="1"/><path d="M10.5 10.5V9a1.5 1.5 0 0 1 3 0v1.5"/>',
    "repaid": '<ellipse cx="9" cy="7" rx="5" ry="2.2"/><path d="M4 7v4c0 1.2 2.2 2.2 5 2.2s5-1 5-2.2V7"/><path d="M10 15.6c.8.4 2 .6 3 .6 2.8 0 5-1 5-2.2v-4"/><ellipse cx="15" cy="10" rx="5" ry="2.2"/>',
    "sell": '<circle cx="12" cy="12" r="7"/><path d="M12 8.5V12l2.5 1.5"/><path d="M3.5 9A9 9 0 0 1 9 3.6M20.5 15A9 9 0 0 1 15 20.4"/>',
}


# Security cover as the user gave it (2026-10-06). Beta's Documents section
# says Collateral Cover 1.0x for this bond.
HL_COVER = "1.1"


def sample(text):
    """A placeholder value: visible cue plus a marker developers can grep for."""
    return '<!-- DATA: placeholder --><span class="hl-sample" title="Sample data">%s</span>' % text


def highlights(html):
    # Reasons to Invest moves into this block: beta's bullet text verbatim,
    # split at its own "Label:" points, and its standalone section removed.
    r0 = html.index('<section class="reasons-to-invest"')
    r1 = html.index("</section>", r0) + len("</section>")
    texts = re.findall(r'<span class="reasons-to-invest__text">([^<]+)</span>', html[r0:r1])
    if not texts:
        raise SystemExit("highlights: no Reasons to Invest bullets found")
    points = [p.strip() for t in texts for p in re.split(r"(?<=\.)\s+(?=[A-Z][A-Za-z ]+:)", t)]
    html = html[:r0] + html[r1:]
    icon = lambda k: '<span class="hl-icon">%s</span>' % svg(HL_ICON[k], 26)
    block = (
        '<section class="hl" aria-labelledby="hl-reasons">'
        '<div class="hl__grid">'
        '<article class="hl__cover">%s'
        '<h2 id="hl-reasons" class="hl__title">Reasons to <span class="hl__accent">Invest</span></h2>'
        '<ul class="hl__points">%s</ul>'
        '<div class="hl__backers"><div class="hl__marks" aria-hidden="true"><span>SBI</span><span>IC</span><span>AX</span></div>'
        '<div><p class="hl-eyebrow">Backed By</p><h3 class="hl__subtitle">Lenders &amp; Investors</h3>'
        '<p class="hl__body">%s</p></div></div></article>'
        '<div class="hl__side">'
        '<article class="hl__repaid"><div class="hl__repaid-head">'
        '<p class="hl__figure">%s</p>%s</div>'
        '<p class="hl-eyebrow">Already Repaid To Our Investors</p>'
        '<dl class="hl-stats"><div><dt>Investors</dt><dd>%s</dd></div>'
        '<div><dt>Repayments</dt><dd>%s</dd></div></dl></article>'
        '<article class="hl__sell">%s<h3 class="hl__subtitle">Invest with Confidence</h3>'
        '<dl class="hl-feats">'
        '<div><dt>Sell Anytime</dt><dd>Sell your bond before maturity, subject to market availability.</dd></div>'
        '<div><dt>%sx Security Cover</dt><dd>For every &#8377;1 you invest, the issuer has provided &#8377;%s of assets as collateral.</dd></div>'
        '</dl></article>'
        '</div></div>'
        '</section>'
    ) % (icon("reasons"), "".join("<li>%s</li>" % p for p in points), sample("SBI, ICICI Bank, Axis Bank"),
         sample("&#8377;24 crores"), icon("repaid"), sample("48200+"), sample("100% on-time"),
         icon("cover"), HL_COVER, HL_COVER)
    end = span_section(html, '<section class="hc"')
    html = html[:end] + block + html[end:]
    return html.replace("</head>", HL_STYLE + "</head>", 1)


def span_section(html, start):
    """End index of the <section> opening with `start` (no nested sections)."""
    i = html.index(start)
    return html.index("</section>", i) + len("</section>")


HL_STYLE = """<style>
/* bond-details3 highlights block. Light card in beta's tokens, gold accents. */
.hl { padding: 28px; border-radius: 24px; background: var(--white); box-shadow: var(--shadow-card);
  border-bottom: 1px solid var(--light-yellow); color: var(--darker-brown); }
.hl__grid { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); }
.hl__cover { padding-right: 28px; border-right: 1px solid var(--light-stroke); }
.hl__side { padding-left: 28px; display: grid; align-content: start; }
.hl__repaid { padding-bottom: 22px; border-bottom: 1px solid var(--light-stroke); }
.hl__sell { padding-top: 22px; }
.hl-icon { width: 52px; height: 52px; display: grid; place-items: center; border-radius: 16px; color: #6b4e0a;
  background: radial-gradient(circle at 30% 25%, #fdf2d0, #f1d27a 60%, #e6b325);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, .6), 0 6px 14px rgba(166, 124, 0, .18); }
.hl-eyebrow { margin: 16px 0 0; font-size: 13px; line-height: 18px; font-weight: 500; color: #8a6520; }
.hl__title { margin: 16px 0 0; font-size: 28px; line-height: 34px; font-weight: 700; letter-spacing: -0.01em; }
.hl__subtitle { margin: 14px 0 0; font-size: 22px; line-height: 28px; font-weight: 700; letter-spacing: -0.01em; }
.hl__points { margin: 16px 0 0; padding-left: 18px; list-style: disc; display: grid; gap: 14px;
  font-size: 15px; line-height: 24px; color: #514834; max-width: 46ch; }
.hl__points li::marker { color: #d4af37; }
.hl__accent { color: #c99a1c; }
.hl-feats { margin: 12px 0 0; display: grid; gap: 12px; }
.hl-feats div { padding-left: 14px; border-left: 2px solid #f1d27a; }
.hl-feats dt { font-size: 15px; line-height: 22px; font-weight: 700; color: var(--darker-brown); }
.hl-feats dd { margin: 2px 0 0; font-size: 14px; line-height: 21px; color: var(--subtext); max-width: 44ch; }
.hl__body { margin: 6px 0 0; font-size: 14px; line-height: 21px; color: var(--subtext); max-width: 44ch; }
.hl__repaid-head { display: flex; align-items: center; justify-content: space-between; gap: 16px; }
.hl__figure { margin: 0; font-size: 28px; line-height: 34px; font-weight: 700; letter-spacing: -0.01em;
  font-variant-numeric: tabular-nums; }
.hl__repaid .hl-eyebrow { margin-top: 6px; }
.hl-stats { margin: 16px 0 0; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }
.hl-stats dd { margin: 0; order: -1; font-size: 20px; line-height: 26px; font-weight: 700; font-variant-numeric: tabular-nums; }
.hl-stats div { display: flex; flex-direction: column; gap: 2px; }
.hl-stats dt { font-size: 13px; line-height: 18px; color: var(--subtext); }
/* Placeholder figures stay visibly provisional until real data replaces them. */
.hl-sample { text-decoration: underline dashed rgba(138, 101, 32, .55); text-underline-offset: 4px;
  text-decoration-thickness: 1px; cursor: help; }
/* Lenders & Investors closes the left column, under Reasons to Invest. */
.hl__backers { margin-top: 24px; padding-top: 22px; border-top: 1px solid var(--light-stroke);
  display: flex; align-items: center; gap: 16px; }
.hl__marks { display: flex; flex: none; }
.hl__marks span { width: 46px; height: 46px; display: grid; place-items: center; border-radius: 50%;
  border: 3px solid var(--white); background: #f3eee2; color: #6b5a37; font-size: 12px; font-weight: 700; letter-spacing: .02em; }
.hl__marks span + span { margin-left: -12px; }
.hl__backers .hl__subtitle { font-size: 20px; line-height: 26px; }
.hl__backers .hl-eyebrow { margin-top: 0; }
.hl__backers .hl__subtitle { margin-top: 2px; }
@media (max-width: 767px) {
  .hl { padding: 20px 16px; border-radius: 20px; }
  .hl__grid { grid-template-columns: minmax(0, 1fr); }
  .hl__cover { padding: 0 0 22px; border-right: 0; border-bottom: 1px solid var(--light-stroke); }
  .hl__side { padding: 22px 0 0; }
  .hl__title { font-size: 24px; line-height: 30px; }
  .hl__backers { flex-direction: column; align-items: flex-start; gap: 14px; }
}
</style>
"""


# bond-details3: beta's accordions, grouped under visible headings. Each card
# stays as it is; its sr-only <h2> drops to <h3> under the group heading.
def group(html, first, last, titles, heading, hid):
    a, _ = span(html, first)
    _, b = span(html, last, a)
    body = html[a:b]
    for t in titles:
        old = '<h2 class="sr-only">%s</h2>' % t
        if old not in body:
            raise SystemExit("%s: not found: %s" % (heading, old))
        body = body.replace(old, '<h3 class="sr-only">%s</h3>' % t, 1)
    return (html[:a] + '<section class="ci" aria-labelledby="%s"><h2 id="%s" class="ci__title">%s</h2>%s</section>'
            % (hid, hid, heading, body) + html[b:])


# bond-details3 cashflow: no Invest Now in the on-page card (the modal keeps
# its own), and a pre-TDS note back in beta's disclaimer slot, page and modal.
TDS_NOTE = "Amounts shown are pre-TDS. 10% TDS applies to resident Indians; file Form 121 to save on it."


def cashflow_v3(html):
    sec = html.index('<div class="gp-expand gp-expand--card ipo-collapsible-section"><h2 class="sr-only">Cashflow</h2>')
    i, j = span(html, '<div class="gp-expand gp-expand--card ipo-collapsible-section"><h2 class="sr-only">Cashflow</h2>', sec)
    card, n = re.subn(r'<button class="gp-btn [^"]*" type="button">Invest Now<svg.*?</svg></button>', "", html[i:j], count=1)
    if not n:
        raise SystemExit("cashflow v3: Invest Now not found in the Cashflow card")
    html = html[:i] + card + html[j:]
    meta = '<div class="bond-cashflow-footer-meta">'
    if html.count(meta) != 2:
        raise SystemExit("cashflow v3: expected 2 footers (page, modal), found %d" % html.count(meta))
    html = html.replace(meta, meta + '<p class="bond-cashflow-tds-disclaimer m-0">%s</p>' % TDS_NOTE)
    html = receivable_split(html)
    # Beta's modal keeps its short disclaimer on one line; this one wraps.
    style = "<style>.bond-cashflow-timeline-modal .bond-cashflow-footer--timeline-modal .bond-cashflow-tds-disclaimer { white-space: normal; }</style>"
    return html.replace("</head>", style + "</head>", 1)


# Total Receivable, split into principal and interest. The figures are the
# sums of the table's own year rows, so the card and the table agree; beta's
# headline total is rounded on its own and can differ from them by a paisa.
YEAR_ROW = re.compile(r'<td class="bond-cashflow-year-amount [^"]*">₹ ([\d,]+\.\d\d)</td><td class="bond-cashflow-year-amount [^"]*">₹ ([\d,]+\.\d\d)</td>')


def receivable_split(html):
    rows = YEAR_ROW.findall(html[:html.index('<div id="cashflow-modal"')])
    interest = sum(money(i) for i, _ in rows)
    principal = sum(money(p) for _, p in rows)
    shown = money(re.search(r'bond-cashflow-receivable-amount block">₹ ([\d,]+\.\d\d)', html).group(1))
    if not rows or abs(interest + principal - shown) > Decimal("0.05"):
        raise SystemExit("receivable split: rows %s + %s vs card %s" % (interest, principal, shown))
    part = '<span class="rs__part"><span class="rs__label">%s</span><span class="rs__value%s">%s</span></span>'
    body = (part % ("Principal", "", inr(principal)) + '<span class="rs__plus" aria-hidden="true">+</span>'
            + part % ("Interest", " rs__value--gain", inr(interest)))
    desk = '<div class="rs">%s</div>' % body
    mob = '<div class="rs rs--mobile">%s</div>' % body
    amount = re.compile(r'(<span class="bond-cashflow-receivable-amount block">₹ [\d,]+\.\d\d</span>)')
    metrics_end = '</div><div class="bond-cashflow-mobile-summary__units-row">'
    html, n1 = amount.subn(r"\1" + desk.replace("\\", "\\\\"), html)
    n2 = html.count(metrics_end)
    html = html.replace(metrics_end, "</div>" + mob + '<div class="bond-cashflow-mobile-summary__units-row">')
    if n1 != 2 or n2 != 2:
        raise SystemExit("receivable split: expected 2 cards and 2 mobile summaries, found %d, %d" % (n1, n2))
    return html.replace("</head>", RS_STYLE + "</head>", 1)


RS_STYLE = """<style>
/* Total Receivable breakdown: a hairline, then principal + interest as two stats. */
.rs { display: grid; grid-template-columns: 1fr auto 1fr; align-items: end; width: 100%; margin-top: 12px; padding-top: 12px;
  border-top: 1px solid rgba(6, 150, 60, 0.18); font-variant-numeric: tabular-nums; }
.rs__part { display: flex; flex-direction: column; gap: 2px; }
.rs__label { font-size: 12px; line-height: 16px; color: var(--subtext); }
.rs__value { font-size: 15px; line-height: 20px; font-weight: 700; color: var(--darker-brown); }
.rs__value--gain { color: #06963c; }
.rs__plus { padding: 0 12px 2px; font-size: 14px; color: var(--subtext); }
/* Mobile: the same split, left-aligned under beta's summary metrics. */
.rs--mobile { margin-top: 0; padding: 10px 16px 2px; border-top: 1px solid var(--light-stroke); text-align: left; }
@media (max-width: 1023px) { .rs:not(.rs--mobile) { display: none; } }
@media (min-width: 1024px) { .rs--mobile { display: none; } }
/* Beta fixes the modal's two summary panels at one height; let them grow together. */
.bond-cashflow-timeline-modal .bond-cashflow-investment-panel,
.bond-cashflow-timeline-modal .bond-cashflow-receivable-panel { height: auto; min-height: var(--bond-cashflow-timeline-modal-panel-height); padding-block: 14px; }
.bond-cashflow-receivable-details { width: 100%; }
</style>
"""


SEBI = "More Bond Details"


def split_documents(html, doc):
    """Beta's Documents card holds Key Details, Investment Details and the files.
    The two detail blocks move to their own card after it, under SEBI; the files stay."""
    a, b = span(html, doc)
    card = html[a:b]
    blocks = []
    for _ in range(2):
        i, j = span(card, '<div class="bond-documents-subsection-block">')
        blocks.append(card[i:j])
        card = card[:i] + card[j:]
    for _ in range(2):
        card = drop(card, '<div class="bond-documents-divider"')
    i, j = span(card, '<div class="bond-documents-action-stack">')
    files = card[i:j]
    divider = '<div class="bond-documents-divider" aria-hidden="true"></div>'
    params = card[:i] + blocks[0] + divider + blocks[1] + card[j:]
    # The card title covers both blocks; their own sub-titles go.
    params, n = re.subn(r'<p class="bond-documents-subsection-title">(Key Details|Investment Details)</p>', "", params)
    if n != 2:
        raise SystemExit("split documents: expected 2 sub-titles, found %d" % n)
    params = params.replace('documents-list--ncd"', 'documents-list--ncd sebi-params"', 1)
    params = re.sub(r'<span class="gp-expand__title">.*?</span></span>', '<span class="gp-expand__title">%s</span>' % SEBI, params, count=1)
    params = params.replace('<h2 class="sr-only">Documents</h2>', '<h2 class="sr-only">%s</h2>' % SEBI, 1)
    params = re.sub(r'(id|aria-controls|aria-labelledby)="(_R_1ukbaav5ubsnlrivb[^"]*)"', r'\1="\2sebi"', params)
    if SEBI not in params or 'sebi"' not in params:
        raise SystemExit("split documents: card markup changed")
    return html[:a] + card + params + html[b:]


def company_info(html):
    card = '<div class="gp-expand gp-expand--card is-open ipo-collapsible-section '
    # Cashflow moves up, ahead of the company sections.
    i, j = span(html, '<div class="gp-expand gp-expand--card ipo-collapsible-section"><h2 class="sr-only">Cashflow</h2>')
    cashflow, html = html[i:j], html[:i] + html[j:]
    k = html.index(card + 'about-issuer')
    html = html[:k] + cashflow + html[k:]
    html = group(html, card + 'about-issuer', card + 'financials-table',
                 ("About the Issuer", "Strength / Weaknesses", "Company Financials"), "Company Information", "ci-h")
    doc = '<div class="gp-expand gp-expand--card ipo-collapsible-section documents-list'
    html = split_documents(html, doc)
    html = group(html, doc, doc + ' documents-list--ncd sebi-params', ("Documents", SEBI), "Documents and More Details", "od-h")
    return html.replace("</head>", CI_STYLE + "</head>", 1)


CI_STYLE = """<style>
/* Company Information, Documents and More Details: a heading over beta's cards, same spacing as the column. */
.ci { display: flex; flex-direction: column; gap: inherit; }
.ci__title { margin: 0; font-size: 20px; line-height: 28px; font-weight: 700; letter-spacing: -0.01em; color: var(--darker-brown); }
@media (max-width: 639px) { .ci__title { font-size: 18px; line-height: 24px; } }
</style>
"""


def check():
    """The scale handles every sign mix; run on each build."""
    assert scale([10, 20, 40]) == (100.0, [(75.0, 25.0), (50.0, 50.0), (0.0, 100.0)])
    assert scale([-10, -40]) == (0.0, [(0.0, 25.0), (0.0, 100.0)])
    z, b = scale([30, -10])
    assert z == 75.0 and b == [(0.0, 75.0), (75.0, 25.0)]
    assert scale([0, 0]) == (0.0, [(0.0, 0.0), (0.0, 0.0)])
    assert crore(7630000000) == "&#8377;763Cr" and crore(-12500000) == "-&#8377;1.25Cr"
    assert crore(132400000000) == "&#8377;13,240Cr" and crore(1e14) == "&#8377;1,00,00,000Cr"
    assert change([("2025", 100.0), ("2026", 131.5)]) == (31.5, "2025")
    assert change([("2025", -20.0), ("2026", -10.0)]) == (50.0, "2025")  # loss narrowed: up
    assert change([("2025", 10.0), ("2026", -10.0)]) == (-200.0, "2025")
    assert change([("2025", 0.0), ("2026", 5.0)]) is None and change([("2026", 5.0)]) is None


def main():
    check()
    raw = open(CAP + ".expanded.html").read()
    html = clean(raw)
    for t in CLOSED:
        html = close(html, t)
    html = drop(html, '<div class="mobile-app-download-nudge ')
    modal = clean(open(CAP + ".timeline.html").read()).replace('aria-hidden="true"', "")
    html = html.replace("</body>", '<div id="cashflow-modal" hidden>%s</div>%s</body>' % (modal, SCRIPT), 1)
    mark = "<head>\n<!-- Generated by pages/_bond_beta.py from the beta.goldenpi.com capture; do not edit. -->"
    v1 = html.replace("<head>", mark, 1)
    v2 = merge_financials(html, series(raw))
    for step in (issuer_tiles, app_block, footer_login4, navbar, chrome, cashflow_split):
        v2 = step(v2)
    v2 = v2.replace("<head>", mark, 1)
    v2 = v2.replace("</head>", STYLE2 + APP_STYLE + "</head>", 1).replace("</body>", SCRIPT2 + "</body>", 1)
    v3 = merge_financials(html, series(raw), render=fin_v3)
    for step in (issuer_tiles, app_block3, footer_login4, navbar, chrome, cashflow_split, cashflow_v3, header_card, highlights, company_info):
        v3 = step(v3)
    v3 = v3.replace("<head>", mark, 1)
    v3 = v3.replace("</head>", STYLE2 + APP_STYLE + STYLE3 + "</head>", 1).replace("</body>", SCRIPT3 + "</body>", 1)
    for path, page in ((OUT, v1), (OUT2, v2), (OUT3, v3)):
        open(path, "w").write(page)
        print("%s  %d bytes" % (os.path.relpath(path, ROOT), len(page)))


if __name__ == "__main__":
    main()
