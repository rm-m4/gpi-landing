#!/usr/bin/env python3
"""bond-mahaveer.html: beta.goldenpi.com's bond detail page, kept in its own design.

Unlike the redesigned pages this one is their DOM and their compiled CSS
(assets/beta/), so it looks exactly like beta. The input is the capture made by
`node crawl/bond_expand.js <dir>`: every section opened (collapsed panels are not
in their DOM at all), the four <canvas> charts saved as images, and the Cashflow
Timeline modal's markup. This script then:

- drops their scripts, and points CSS and /_next/static/media images at local copies
- closes Documents, Cashflow and Financial Ratio again, as beta loads them
- adds the modal back, hidden, and a small script for the toggles

    python3 pages/_bond_beta.py
"""
import os
import re
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAP = os.path.join(ROOT, "crawl/rendered/beta_bonds_INE911L07154_mahaveer-1200-bond-yield")
OUT = os.path.join(ROOT, "pages/bond-mahaveer.html")
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


def main():
    html = clean(open(CAP + ".expanded.html").read())
    for t in CLOSED:
        html = close(html, t)
    modal = clean(open(CAP + ".timeline.html").read()).replace('aria-hidden="true"', "")
    html = html.replace("</body>", '<div id="cashflow-modal" hidden>%s</div>%s</body>' % (modal, SCRIPT), 1)
    html = html.replace("<head>", "<head>\n<!-- Generated by pages/_bond_beta.py from the beta.goldenpi.com capture; do not edit. -->", 1)
    open(OUT, "w").write(html)
    print("%s  %d bytes" % (os.path.relpath(OUT, ROOT), len(html)))


if __name__ == "__main__":
    main()
