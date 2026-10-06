#!/usr/bin/env python3
"""Generate navbar-variants.html: a lab for the header's next entry points.

    Bonds, FD, Bond Utsav, Refer & Earn  <>  search  <>  Notifications,
    Portfolio, account (logged in) or Login / Sign up (guest)

Eight variants: with or without icons, light or dark, guest or logged in.
All eight render in a sticky slot at the top of the page, one visible; the
lab section lists them as previews, and choosing one (or flipping the three
switches) moves it to the top. Below that is corporate-bonds.html as it
stands, so a variant is judged over real content, scrolled. The choice is
kept in the URL hash, so a link opens the same variant.

Labels, links and icons are the current header's (corporate-bonds.html and
user-explore.html); Collection is dropped and Portfolio added, its icon the
briefcase from the portfolio Figma. Styles are assets/navbar.css.

Run: python3 pages/_navbar.py
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = "../assets/img/"

LINKS = [  # label, guest href, logged-in href, icon
    ("Bonds", "corporate-bonds.html", "user-corporate-bonds.html", "header-nav-bonds.svg"),
    ("FD", "fixed-deposits.html", "user-fixed-deposits.html", "header-nav-fd.svg"),
    ("Bond Utsav", "bond-utsav.html", "bond-utsav.html", None),
    ("Refer &amp; Earn", "refer-and-earn.html", "refer-and-earn.html", "header-nav-ref-earn.svg"),
]
CURRENT = "Bonds"  # the content below is the corporate bonds page

ICONS = [("icons", "With icons"), ("plain", "Without icons")]
THEMES = [("light", "Light"), ("dark", "Dark")]
STATES = [("login", "Logged in"), ("guest", "Guest")]
DEFAULT = "icons-light-login"  # closest to the header on the site today


def ic(name, cls="nb-ic"):
    """An icon drawn as a mask, so it takes the text colour in either theme."""
    return '<span class="%s" style="--i: url(%s%s)" aria-hidden="true"></span>' % (cls, IMG, name)


def header(icons, theme, state, preview=False):
    key = "%s-%s-%s" % (icons, theme, state)
    show = icons == "icons"
    login = state == "login"
    tag, nav = ("div", "div") if preview else ("header", "nav")
    links = []
    for label, guest, user, icon in LINKS:
        art = ""
        if show:
            art = ('<img class="nb-ic" src="%sheader-nav-bond-utsav.svg" alt="">' % IMG
                   if icon is None else ic(icon))
        cur = ' aria-current="page"' if label == CURRENT and not preview else (
            ' data-current' if label == CURRENT else "")
        links.append('        <a class="nb__link%s" href="%s"%s>%s<span>%s</span></a>\n'
                     % (" is-current" if label == CURRENT else "", user if login else guest, cur, art, label))
    if login:
        # On phones the links are the bottom tab bar, and Portfolio joins it.
        links.append('        <a class="nb__link nb__link--m" href="portfolio.html">%s<span>Portfolio</span></a>\n'
                     % (ic("header-nav-portfolio.svg") if show else ""))
        actions = (
            '      <button type="button" class="nb__btn nb__search-btn" aria-label="Search">%s</button>\n'
            '      <button type="button" class="nb__btn" aria-label="Notifications">%s</button>\n'
            '      <a class="nb__pill" href="portfolio.html">%s<span>Portfolio</span></a>\n'
            '      <!-- DATA: the account holder\'s initials. -->\n'
            '      <button type="button" class="nb__avatar" aria-label="Account menu">IN</button>\n'
            % (ic("header-search.svg"), ic("notify-bell.svg"),
               ic("header-nav-portfolio.svg") if show else ""))
    else:
        actions = (
            '      <button type="button" class="nb__btn nb__search-btn" aria-label="Search">%s</button>\n'
            '      <button type="button" class="gp-cta gp-cta--primary nb__login">%s<span>Login / Sign up</span></button>\n'
            % (ic("header-search.svg"),
               '<img src="%suser-icon.svg" alt="" width="15" height="15">' % IMG if show else ""))
    return (
        '<%s class="nb nb--%s nb--%s" data-v="%s"%s>\n'
        '  <div class="gp-shell nb__inner">\n'
        '    <a class="nb__logo" href="%s"><img src="%sgoldenpi-logo%s.svg" alt="GoldenPi" width="132" height="30"></a>\n'
        '    <%s class="nb__nav"%s>\n%s    </%s>\n'
        '    <div class="nb__search">%s<span>Search for bonds, FD or IPO</span></div>\n'
        '    <div class="nb__actions">\n%s    </div>\n'
        '  </div>\n'
        '</%s>\n') % (
        tag, theme, icons, key,
        "" if preview or key == DEFAULT else " hidden",
        "user-explore.html" if login else "index.html", IMG, "-white" if theme == "dark" else "",
        nav, "" if preview else ' aria-label="Primary"', "".join(links), nav,
        ic("header-search.svg"), actions, tag)


def name(icons, theme, state):
    return "%s, %s, %s" % (dict(STATES)[state], dict(THEMES)[theme].lower(), dict(ICONS)[icons].lower())


def variants():
    return [(i, t, s) for s, _ in STATES for t, _ in THEMES for i, _ in ICONS]


def switch(group, legend, options, value):
    return ('      <fieldset class="nb-seg">\n        <legend>%s</legend>\n        <div class="nb-seg__track">\n%s'
            '        </div>\n      </fieldset>\n') % (legend, "".join(
                '          <label><input type="radio" name="%s" value="%s"%s><span>%s</span></label>\n'
                % (group, v, " checked" if v == value else "", label) for v, label in options))


def lab():
    d = DEFAULT.split("-")
    items = "".join(
        '      <li class="nb-item%s">\n'
        '        <div class="nb-item__head">\n'
        '          <h3>%s</h3>\n'
        '          <button type="button" class="nb-pick" data-v="%s" aria-pressed="%s">%s</button>\n'
        '        </div>\n'
        '        <div class="nb-frame nb-frame--%s" inert aria-hidden="true">\n%s        </div>\n'
        '      </li>\n' % (
            " is-on" if "-".join(v) == DEFAULT else "", name(*v), "-".join(v),
            "true" if "-".join(v) == DEFAULT else "false",
            "At top" if "-".join(v) == DEFAULT else "Move to top", v[1],
            re.sub(r"(?m)^", "          ", header(*v, preview=True)))
        for v in variants())
    return (
        '  <!-- ============================================================ navbar lab -->\n'
        '  <section class="nb-lab" aria-labelledby="nb-lab-title">\n'
        '    <div class="gp-shell">\n'
        '      <h2 id="nb-lab-title">Navbar variants</h2>\n'
        '      <p class="nb-lab__lede">Pick a variant and it moves to the top of the page. Scroll the corporate bonds page below to see how it sits over real content.</p>\n'
        '    <form class="nb-controls" id="nb-controls" aria-label="Navbar variant">\n%s%s%s    </form>\n'
        '    <ol class="nb-list">\n%s    </ol>\n'
        '    </div>\n'
        '  </section>\n') % (
        switch("state", "State", STATES, d[2]),
        switch("theme", "Theme", THEMES, d[1]),
        switch("icons", "Icons", ICONS, d[0]), items)


JS = r"""<script>
// Navbar lab. The chosen variant is the one header in the top slot without
// [hidden]; the switches and the "Move to top" buttons both choose it, and
// the URL hash keeps it. Without script the default variant shows.
(function () {
  var slot = document.getElementById('nb-slot');
  var form = document.getElementById('nb-controls');
  var names = ['icons', 'theme', 'state'];
  var valid = {};
  slot.querySelectorAll('.nb').forEach(function (h) { valid[h.dataset.v] = true; });
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function current() {
    var v = {};
    names.forEach(function (n) { v[n] = form.elements[n].value; });
    return v.icons + '-' + v.theme + '-' + v.state;
  }
  function setForm(key) {
    key.split('-').forEach(function (part, i) { form.elements[names[i]].value = part; });
  }
  function apply(key, animate) {
    slot.querySelectorAll('.nb').forEach(function (h) {
      var on = h.dataset.v === key;
      h.hidden = !on;
      if (on && animate && !reduce) {
        h.classList.remove('is-entering'); void h.offsetWidth; h.classList.add('is-entering');
      }
    });
    document.querySelectorAll('.nb-pick').forEach(function (b) {
      var on = b.dataset.v === key;
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
      b.textContent = on ? 'At top' : 'Move to top';
      b.closest('.nb-item').classList.toggle('is-on', on);
    });
    try { history.replaceState(null, '', '#' + key); } catch (e) {}
  }

  form.addEventListener('change', function () { apply(current(), true); });
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.nb-pick');
    if (!b) return;
    setForm(b.dataset.v);
    apply(b.dataset.v, true);
    window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
  });

  var start = location.hash.slice(1);
  if (valid[start]) { setForm(start); apply(start, false); }

  // Scrolled state: a sentinel just above the slot, watched, not a scroll listener.
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
    page = re.sub(r"<title>.*?</title>", "<title>Navbar variants | GoldenPi</title>", page, count=1, flags=re.S)
    page = page.replace("</title>", "</title>\n<!-- Navbar lab, generated by pages/_navbar.py from "
                        "corporate-bonds.html. Not a product page. -->", 1)
    page = page.replace('<link rel="stylesheet" href="../assets/final.css">',
                        '<link rel="stylesheet" href="../assets/final.css">\n'
                        '<link rel="stylesheet" href="../assets/navbar.css">', 1)
    a = page.index("<!-- ============================================================== header -->")
    b = page.index("</header>", a) + len("</header>\n")
    slot = ('<!-- ============================================================== header -->\n'
            '<!-- Every variant, one shown: pages/_navbar.py. -->\n'
            '<div class="nb-slot" id="nb-slot">\n%s</div>\n') % "".join(header(*v) for v in variants())
    page = page[:a] + slot + page[b:]
    page = page.replace('<main id="main-content">\n', '<main id="main-content">\n' + lab(), 1)
    page = page.replace("</body>", JS + "</body>", 1)
    with open(os.path.join(HERE, "navbar-variants.html"), "w", encoding="utf-8") as f:
        f.write(page)
    print("navbar-variants.html %d bytes" % len(page))


if __name__ == "__main__":
    main()
