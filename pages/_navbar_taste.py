#!/usr/bin/env python3
"""Generate navbar-variants-taste.html: the navbar lab redone under the taste
skill. Same entry points and the same eight variants as navbar-variants.html
(pages/_navbar.py); three things differ, each a rule that version broke:

  1. Theme is the navbar's only, and dark is off-black: the page content
     and its theme are left exactly as corporate-bonds.html has them.
  2. One icon family. Phosphor (regular, and fill for the current page) for
     every UI icon; the Bond Utsav badge stays as brand artwork.
  3. Every control is a real control: search is a <button>, so it is
     keyboard-reachable.

The current page sits in a raised pill on a quiet track; a second pill
follows the pointer or focus across the links and settles back (feedback,
and off under reduced motion). Styles are assets/navbar-taste.css.

Run: python3 pages/_navbar_taste.py
"""
import os
import re

import _navbar as N

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = "../assets/img/"
PH = "https://unpkg.com/@phosphor-icons/web@2.1.1/src/%s/style.css"

ICON = {  # Phosphor names, one family
    "Bonds": "chart-pie-slice", "FD": "bank", "Refer &amp; Earn": "gift",
    "Portfolio": "briefcase", "bell": "bell", "search": "magnifying-glass", "user": "user",
}


def ph(name, fill=False):
    return '<i class="ph%s ph-%s" aria-hidden="true"></i>' % ("-fill" if fill else "", name)


def header(icons, theme, state, preview=False):
    key = "%s-%s-%s" % (icons, theme, state)
    show = icons == "icons"
    login = state == "login"
    tag, nav = ("div", "div") if preview else ("header", "nav")
    links = []
    for label, guest, user, _ in N.LINKS:
        cur = label == N.CURRENT
        art = ""
        if show:
            art = ('<img class="tn-badge" src="%sheader-nav-bond-utsav.svg" alt="">' % IMG
                   if label == "Bond Utsav" else ph(ICON[label], fill=cur))
        links.append('        <a class="tn__link%s" href="%s"%s>%s<span>%s</span></a>\n' % (
            " is-current" if cur else "", user if login else guest,
            ' aria-current="page"' if cur and not preview else "", art, label))
    if login:
        # On phones the links are the bottom tab bar, and Portfolio joins it.
        links.append('        <a class="tn__link tn__link--m" href="portfolio.html">%s<span>Portfolio</span></a>\n'
                     % (ph(ICON["Portfolio"]) if show else ""))
        actions = (
            '      <button type="button" class="tn__btn tn__search-btn" aria-label="Search">%s</button>\n'
            '      <button type="button" class="tn__btn" aria-label="Notifications">%s</button>\n'
            '      <a class="tn__pill" href="portfolio.html">%s<span>Portfolio</span></a>\n'
            '      <!-- DATA: the account holder\'s initials. -->\n'
            '      <button type="button" class="tn__avatar" aria-label="Account menu">IN</button>\n'
            % (ph(ICON["search"]), ph(ICON["bell"]), ph(ICON["Portfolio"]) if show else ""))
    else:
        actions = (
            '      <button type="button" class="tn__btn tn__search-btn" aria-label="Search">%s</button>\n'
            '      <button type="button" class="gp-cta gp-cta--primary tn__login">%s<span>Login / Sign up</span></button>\n'
            % (ph(ICON["search"]), ph(ICON["user"]) if show else ""))
    return (
        '<%s class="tn tn--%s" data-v="%s" data-theme-of="%s"%s>\n'
        '  <div class="gp-shell tn__inner">\n'
        '    <a class="tn__logo" href="%s">'
        '<img class="tn__logo-light" src="%sgoldenpi-logo.svg" alt="GoldenPi" width="132" height="30">'
        '<img class="tn__logo-dark" src="%sgoldenpi-logo-white.svg" alt="" width="132" height="30"></a>\n'
        '    <%s class="tn__nav"%s>\n'
        '      <div class="tn__track">\n'
        '        <span class="tn__glide" aria-hidden="true"></span>\n'
        '%s      </div>\n'
        '    </%s>\n'
        '    <button type="button" class="tn__search">%s<span>Search for bonds, FD or IPO</span></button>\n'
        '    <div class="tn__actions">\n%s    </div>\n'
        '  </div>\n'
        '</%s>\n') % (
        tag, icons, key, theme,
        "" if preview or key == N.DEFAULT else " hidden",
        "user-explore.html" if login else "index.html", IMG, IMG,
        nav, "" if preview else ' aria-label="Primary"', "".join(links), nav,
        ph(ICON["search"]), actions, tag)


def lab():
    d = N.DEFAULT.split("-")
    rows = []
    for v in N.variants():
        k = "-".join(v)
        on = k == N.DEFAULT
        rows.append(
            '      <li class="tn-row%s">\n'
            '        <div class="tn-row__head">\n'
            '          <h3>%s</h3>\n'
            '          <button type="button" class="tn-pick" data-v="%s" aria-pressed="%s">%s</button>\n'
            '        </div>\n'
            '        <div class="tn-frame" data-frame-theme="%s" inert aria-hidden="true">\n%s        </div>\n'
            '      </li>\n' % (" is-on" if on else "", N.name(*v), k, "true" if on else "false",
                               "At top" if on else "Move to top", v[1],
                               re.sub(r"(?m)^", "          ", header(*v, preview=True))))
    return (
        '  <!-- ============================================================ navbar lab -->\n'
        '  <section class="tn-lab" aria-labelledby="tn-lab-title">\n'
        '    <div class="gp-shell">\n'
        '      <h2 id="tn-lab-title">Navbar variants</h2>\n'
        '      <p class="tn-lab__lede">Choose a variant to put it at the top, then scroll the corporate bonds page below to see how it sits over real content.</p>\n'
        '      <form class="tn-controls" id="tn-controls" aria-label="Navbar variant">\n%s%s%s      </form>\n'
        '      <ol class="tn-list">\n%s      </ol>\n'
        '    </div>\n'
        '  </section>\n') % (
        N.switch("state", "State", N.STATES, d[2]),
        N.switch("theme", "Theme", N.THEMES, d[1]),
        N.switch("icons", "Icons", N.ICONS, d[0]), "".join(rows))


JS = r"""<script>
// Navbar lab (taste). One header in the top slot is shown; its theme is set
// on the slot only, so the page content keeps its own theme. Switches, "Move to top" and the
// URL hash all choose it. A glide pill follows pointer or focus across the
// links and settles back on the current page.
(function () {
  var slot = document.getElementById('tn-slot');
  var form = document.getElementById('tn-controls');
  var names = ['icons', 'theme', 'state'];
  var valid = {};
  slot.querySelectorAll('.tn').forEach(function (h) { valid[h.dataset.v] = true; });
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function current() {
    return names.map(function (n) { return form.elements[n].value; }).join('-');
  }
  function setForm(key) {
    key.split('-').forEach(function (part, i) { form.elements[names[i]].value = part; });
  }
  function apply(key) {
    var shown;
    slot.querySelectorAll('.tn').forEach(function (h) {
      h.hidden = h.dataset.v !== key;
      if (!h.hidden) shown = h;
    });
    slot.dataset.theme = shown.dataset.themeOf;
    document.querySelectorAll('.tn-pick').forEach(function (b) {
      var on = b.dataset.v === key;
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
      b.textContent = on ? 'At top' : 'Move to top';
      b.closest('.tn-row').classList.toggle('is-on', on);
    });
    settle(shown, false);
    try { history.replaceState(null, '', '#' + key); } catch (e) {}
  }

  // Glide: a pill placed under a link with transform, never layout properties.
  function place(track, link, animate) {
    var g = track.querySelector('.tn__glide');
    if (!link) { g.style.opacity = '0'; return; }
    g.style.transition = animate && !reduce ? '' : 'none';
    g.style.width = link.offsetWidth + 'px';
    g.style.transform = 'translateX(' + link.offsetLeft + 'px)';
    g.style.opacity = '1';
  }
  function settle(header, animate) {
    if (!header) return;
    var track = header.querySelector('.tn__track');
    place(track, track.querySelector('.tn__link.is-current'), animate);
  }
  slot.addEventListener('pointerover', function (e) {
    var a = e.target.closest('.tn__link');
    if (a) place(a.parentNode, a, true);
  });
  slot.addEventListener('focusin', function (e) {
    var a = e.target.closest('.tn__link');
    if (a) place(a.parentNode, a, true);
  });
  slot.addEventListener('pointerleave', function () { settle(slot.querySelector('.tn:not([hidden])'), true); });
  slot.addEventListener('focusout', function (e) {
    if (!slot.contains(e.relatedTarget)) settle(slot.querySelector('.tn:not([hidden])'), true);
  });
  window.addEventListener('resize', function () { settle(slot.querySelector('.tn:not([hidden])'), false); });

  form.addEventListener('change', function () { apply(current()); });
  window.addEventListener('hashchange', function () {
    var k = location.hash.slice(1);
    if (valid[k]) { setForm(k); apply(k); }
  });
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.tn-pick');
    if (!b) return;
    setForm(b.dataset.v);
    apply(b.dataset.v);
    window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
  });

  // Start: the hash if it names a variant, else the default with the
  // visitor's colour scheme.
  var start = location.hash.slice(1);
  if (!valid[start]) {
    start = form.elements.icons.value + '-' +
      (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light') + '-' +
      form.elements.state.value;
  }
  setForm(start);
  apply(start);
  document.fonts && document.fonts.ready.then(function () { settle(slot.querySelector('.tn:not([hidden])'), false); });

  // Scrolled state from a watched sentinel, not a scroll listener.
  if ('IntersectionObserver' in window) {
    var mark = document.createElement('div');
    mark.setAttribute('aria-hidden', 'true');
    slot.parentNode.insertBefore(mark, slot);
    new IntersectionObserver(function (es) {
      slot.classList.toggle('is-scrolled', !es[0].isIntersecting);
    }).observe(mark);
  }
})();
</script>
"""


def main():
    with open(os.path.join(HERE, "corporate-bonds.html"), encoding="utf-8") as f:
        page = f.read()
    page = re.sub(r"<title>.*?</title>", "<title>Navbar variants, taste | GoldenPi</title>", page, count=1, flags=re.S)
    page = page.replace("</title>", "</title>\n<!-- Navbar lab under the taste skill, generated by "
                        "pages/_navbar_taste.py from corporate-bonds.html. Not a product page. -->", 1)
    page = page.replace('<link rel="stylesheet" href="../assets/final.css">',
                        '<link rel="stylesheet" href="../assets/final.css">\n'
                        '<link rel="stylesheet" href="%s">\n<link rel="stylesheet" href="%s">\n'
                        '<link rel="stylesheet" href="../assets/navbar-taste.css">' % (PH % "regular", PH % "fill"), 1)
    a = page.index("<!-- ============================================================== header -->")
    b = page.index("</header>", a) + len("</header>\n")
    slot = ('<!-- ============================================================== header -->\n'
            '<!-- Every variant, one shown: pages/_navbar_taste.py. -->\n'
            '<div class="tn-slot" id="tn-slot">\n%s</div>\n') % "".join(header(*v) for v in N.variants())
    page = page[:a] + slot + page[b:]
    page = page.replace('<main id="main-content">\n', '<main id="main-content">\n' + lab(), 1)
    page = page.replace("</body>", JS + "</body>", 1)
    with open(os.path.join(HERE, "navbar-variants-taste.html"), "w", encoding="utf-8") as f:
        f.write(page)
    print("navbar-variants-taste.html %d bytes" % len(page))


if __name__ == "__main__":
    main()
