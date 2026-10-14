#!/usr/bin/env python3
"""Write explore-prelogin.html: web-v1's Explore (user-explore-app7.html) for a
visitor who is not logged in (2026-10-13, user's brief). Changes from the
logged-in page:

  - the navbar keeps the logged-in tabs (on phones, the bottom tab bar) and Search,
    with Login / Sign up in place of notifications, Portfolio and the avatar; the
    footer is the guest one;
  - the rail loses the portfolio cards and pending orders (and the portfolio
    info sheets they open); in their place one signup card: one icon, one line,
    one CTA;
  - the page is gated: the hero, the stats, "why invest" and the High Return
    shelf show, its foot fading into a login gate; everything after it (Live NCD
    IPOs included) is left out of the page (not hidden: there is nothing
    to scroll or tab to past the gate). The footer, with its disclosures, stays.

Copy: the rail line is signup.html's tagline and its CTA "Start investing"; the
gate's CTA is the guest navbar's "Login / Sign up"; the gate's one line is new UI
copy, marked in the page.

Taste-skill pre-flight (2026-10-13, redesign-preserve: the logged-in page as is,
the new parts checked): one accent (gold), cards on the page's 24px radius, tinted shadows, Phosphor icons, no dashes in visible copy, one
h1; the gate rises in with data-reveal like the sections before it. web-v1 publishes it as explore-prelogin.html.

    python3 pages/_explore_prelogin.py && python3 pages/_web_v1.py
"""
import os
import re

import _build as B
import _fd_prelogin as F

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "user-explore-app7.html")
OUT_NAME = "explore-prelogin.html"


def read(p):
    return open(p, encoding="utf-8").read()


def guest_header(h):
    """The logged-in navbar for a guest: the same tabs (on phones, the bottom tab
    bar), with Bonds pointing here; Search kept; Notifications, the Portfolio pill
    and the avatar swapped for the guest bar's Login / Sign up."""
    h = h.replace('data-v="plain-dark-login"', 'data-v="plain-dark-guest"', 1)
    h, a = re.subn(r'\s*<button type="button" class="nb__btn" aria-label="Notifications">.*?</button>', "", h, count=1, flags=re.S)
    h, b = re.subn(r'\s*<a class="nb__pill" href="portfolio.html">.*?<button type="button" class="nb__avatar"[^>]*>[^<]*</button>',
                   '\n      <button type="button" class="gp-cta gp-cta--primary nb__login"><span>Login / Sign up</span></button>', h, count=1, flags=re.S)
    h, c = re.subn(r'<a class="nb__link([^"]*)" href="user-explore-app7.html"', r'<a class="nb__link\1" href="explore-prelogin.html"', h, count=1)
    if (a, b, c) != (1, 1, 1):
        raise SystemExit("user-explore-app7.html: navbar changed shape (%d %d %d)" % (a, b, c))
    return h


def signup_card():
    tag = re.search(r'<p class="gp-auth__tagline">(.*?)</p>', read(F.SIGNUP)).group(1)
    return f'''<aside class="xb-rail x7r" aria-label="Sign up">
  <!-- COPY: signup.html's tagline; one CTA to signup.html, "Start investing" (the
       premium pages' label; user's choice, 2026-10-13, over one label per intent). -->
  <section class="xpl-card">
    <!-- the icon is GoldenPi's own mark (taste-skill: an icon that means the line, "India's trusted
         bond investment platform", rather than a generic add-user glyph) -->
    <span class="xpl-icon xpl-icon--lg xpl-icon--mark" aria-hidden="true"><img src="../assets/img/portfolio/card-mark.svg" alt="" width="26" height="27"></span>
    <p class="xpl-card__line">{tag}</p>
    <a class="xpl-cta" href="signup.html">Start investing <i class="ph-bold ph-arrow-right" aria-hidden="true"></i></a>
  </section>
</aside>'''


GATE = '''<section class="xpl-gate" data-reveal aria-labelledby="xpl-gate-t">
  <span class="xpl-icon xpl-icon--lg" aria-hidden="true"><i class="ph ph-lock-simple"></i></span>
  <!-- COPY: invented (UI line for the gate, 2026-10-13); the CTA is the guest navbar's. -->
  <h2 id="xpl-gate-t">Log in to continue exploring.</h2>
  <a class="xpl-cta" href="signup.html">Login / Sign up</a>
</section>'''

STYLE = r"""<style>
/* explore-prelogin (pages/_explore_prelogin.py): the signup rail card, the fade
   and the login gate. One gold CTA style for both; pills for controls.
   Premium (2026-10-13, taste-skill; the two pre-login blocks only, the page as is):
   both are the premium pages' black surface, the same black as the navbar and
   footer, so they read as GoldenPi's own voice on the light page: a gold glow from
   the top, a gold hairline, a faint top highlight for an edge, gold-ring icons,
   cream copy; the gold pill CTA unchanged. One accent: gold. Radii 24px, as the page's cards.
   The gate is the light version of the same block (user, 2026-10-13): white with the
   gold glow and hairline, an ink heading, the icon ring in bronze. */
.xpl-card, .xpl-gate { position: relative; isolation: isolate; text-align: center; border-radius: 24px; color: #f4e9c8;
  background: radial-gradient(90% 70% at 50% 0%, rgba(212,175,55,.22), transparent 62%), linear-gradient(180deg, #14110c, #0b0906);
  border: 1px solid rgba(212,175,55,.28);
  box-shadow: inset 0 1px 0 rgba(255,236,190,.08), 0 30px 60px -34px rgba(50,40,17,.55); }
.xpl-card { display: grid; justify-items: center; align-content: center; gap: 24px; min-height: 340px; padding: 44px 26px 36px; }  /* a taller rectangle (user, 2026-10-13) */
/* side by side with the hero (the page's own 1200px breakpoint): the card matches its height */
@media (min-width: 1200px) { .xpl-card { min-height: 411px; gap: 28px; } }
/* one icon, shared by the rail card and the gate: a gold ring on black */
.xpl-icon { display: grid; place-items: center; width: 44px; height: 44px; border-radius: 50%; color: #edc967; font-size: 22px;
  background: radial-gradient(circle at 50% 30%, rgba(212,175,55,.22), rgba(212,175,55,.06) 70%); border: 1px solid rgba(237,201,103,.5);
  box-shadow: 0 0 0 6px rgba(212,175,55,.06), 0 10px 30px -10px rgba(212,175,55,.45); }
.xpl-icon--lg { width: 56px; height: 56px; font-size: 26px; }
.xpl-icon--mark img { display: block; width: 28px; height: auto; filter: drop-shadow(0 2px 8px rgba(236,155,38,.35)); }
.xpl-card__line { margin: 0; max-width: 26ch; font-size: 18px; line-height: 1.45; font-weight: 500; letter-spacing: -.01em; color: #fff; }
.xpl-cta { display: inline-flex; align-items: center; justify-content: center; gap: 10px; min-height: 48px; padding: 0 24px; border-radius: 999px;
  background: linear-gradient(100deg, #f7e4a1, #d4af37 55%, #b8902c); color: #1a1408; font-size: 15px; font-weight: 700; white-space: nowrap;
  transition: transform .2s, filter .2s; }
.xpl-card .xpl-cta { width: 100%; min-height: 52px; font-size: 16px; }
.xpl-cta:hover { filter: brightness(1.05); }
.xpl-cta:active { transform: scale(.98); }
.xpl-cta i { transition: transform .2s; } .xpl-cta:hover i { transform: translateX(4px); }
.xpl-cta:focus-visible { outline: 2px solid #f2d98a; outline-offset: 3px; }
/* the page fades into the gate: a wash of the page colour over the foot of the shelf
   above (it stays clickable; the wash lets clicks through) */
.xpl-gate::before { content: ""; position: absolute; left: -24px; right: -24px; bottom: 100%; height: 120px; pointer-events: none;
  background: linear-gradient(180deg, rgba(247,245,242,0), var(--page, #f7f5f2) 92%); }
.xpl-gate { display: grid; justify-items: center; gap: 20px; margin: -40px 0 0; padding: 52px 24px 56px; }
.xpl-gate { color: #14120d; border-color: rgba(212,175,55,.32);
  background: radial-gradient(90% 70% at 50% 0%, rgba(212,175,55,.16), transparent 62%), linear-gradient(180deg, #fffdf8, #fff);
  box-shadow: inset 0 1px 0 #fff, 0 30px 60px -36px rgba(50,40,17,.3); }
.xpl-gate .xpl-icon { color: #8a6520; background: radial-gradient(circle at 50% 30%, #fbf3dc, #f5e9c6 70%); border-color: rgba(184,144,44,.45);
  box-shadow: 0 0 0 6px rgba(212,175,55,.08), 0 10px 30px -12px rgba(184,144,44,.45); }
.xpl-gate h2 { margin: 0; font-size: clamp(24px, 2.6vw, 32px); line-height: 1.2; font-weight: 700; letter-spacing: -.025em; color: #14120d; }
.xpl-gate .xpl-cta:focus-visible { outline-color: #8a6520; }
.xpl-gate .xpl-cta { min-height: 52px; padding: 0 32px; font-size: 16px; }
.nb .nb__login { border-radius: 999px; }  /* shape lock: every control on this page is a pill */
@media (max-width: 767px) {
  .xpl-gate { margin-top: -24px; padding: 40px 20px 44px; }
  /* phones: the signup card becomes a bar fixed above the bottom tab bar (62px + the
     safe area): line left, CTA right, no icon; the page pads for it, so nothing
     ends up underneath */
  .xb-rail.x7r { position: fixed; left: 12px; right: 12px; bottom: calc(62px + env(safe-area-inset-bottom, 0px) + 10px); z-index: 39; display: block; }
  .xpl-card { grid-template-columns: minmax(0, 1fr) auto; justify-items: start; align-items: center; gap: 12px; min-height: 0;
    padding: 12px 12px 12px 16px; border-radius: 20px; text-align: left; box-shadow: inset 0 1px 0 rgba(255,236,190,.08), 0 18px 40px -12px rgba(11,9,6,.55); }
  .xpl-card .xpl-icon { display: none; }
  .xpl-card__line { max-width: none; font-size: 13px; line-height: 1.35; }
  .xpl-card .xpl-cta { width: auto; min-height: 44px; padding: 0 16px; font-size: 14px; }
  body { padding-bottom: calc(62px + env(safe-area-inset-bottom, 0px) + 100px); }
}
</style>
"""


def main():
    page = read(SRC)
    # guest navbar, logo and Login / Sign up only
    page, n1 = re.subn(r'<header><div class="nb [^"]*" data-v="plain-dark-login">.*?</header>',
                       lambda m: guest_header(m.group(0)), page, count=1, flags=re.S)
    # rail: the portfolio cards and pending orders out, the signup card in
    page, n2 = re.subn(r'<aside class="xb-rail x7r" aria-label="Your account">.*?</aside>',
                       lambda m: signup_card(), page, count=1, flags=re.S)
    # the portfolio info sheets those cards opened
    page, n3 = re.subn(r'\s*<dialog class="pf-sheet".*?</dialog>', "", page, flags=re.S)
    # the gate, straight after the High Return shelf; the sections after it (Live NCD
    # IPOs, removed from this page by the user 2026-10-13, and the rest) are left out
    i = page.index('<div class="xa-main">')
    j = page.index('<section class="xb-ipos', i)
    k = page.index('<section class="x7a"', j)
    k = page.index("</section>", k) + len("</section>")
    page = page[:j] + GATE + page[k:]
    # styles, icons, title, guest footer
    head = STYLE
    if "phosphor-icons" not in page:
        head += '<script src="https://unpkg.com/@phosphor-icons/web@2.1.1"></script>\n'
    page = page.replace("</head>", head + "</head>", 1)
    page, n4 = re.subn(r"<title>.*?</title>", "<title>Explore Bonds | GoldenPi</title>", page, count=1)
    had_final = "final.css" in page
    page = B.ggn_footer(OUT_NAME, page)
    if not had_final:
        page = page.replace('<link rel="stylesheet" href="../assets/final.css">\n', "", 1)
        page = page.replace("</style>\n</head>", ".nb__login { display: inline-flex; align-items: center; height: 40px; padding: 0 20px; border: 0; border-radius: 999px; background: linear-gradient(100deg, #f7e4a1, #d4af37 55%, #b8902c); color: #1a1408; font-size: 14px; font-weight: 600; white-space: nowrap; }\n</style>\n</head>", 1)
    gone = [w for w in ("nb__avatar", 'class="xb-ipos', "data-pf-carousel>", "class=\"xb-orders\"", 'class="x7s x7s--gold"', 'class="x7a"') if w in page]
    if (n1, n2, n4) != (1, 1, 1) or n3 != 2 or gone:
        raise SystemExit("user-explore-app7.html changed shape (%d %d %d %d) %s" % (n1, n2, n3, n4, gone))
    open(os.path.join(HERE, OUT_NAME), "w", encoding="utf-8").write(page)
    print(OUT_NAME)


if __name__ == "__main__":
    main()
