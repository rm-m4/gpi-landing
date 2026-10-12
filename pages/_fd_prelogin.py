#!/usr/bin/env python3
"""Write premium-fd2.html: the pre-login FD landing page. Everything on the
logged-in FD page web-v1 shows as /fixed-deposits (user-fixed-deposits-app2.html)
stays as it is (the FD carousel, security, Bank and NBFC FDs, PSU vs GoldenPi,
the calculator), with three changes for a visitor who is not logged in:

  - the navbar is the premium pages' guest bar, logo and CTA only;
  - the right rail opens with a signup nudge (signup.html's headline, tagline
    and trust points, one "Start investing" button to signup.html), the
    first-FD offer under it;
  - home-premium15's branding sections follow at full width: why investors
    choose GoldenPi, invest 24x7, happy users and the app download;
  - the footer is the guest footer (footer-ggn-guest.html), not the logged-in one.

Taste-skill (2026-10-12): the rail card is the page's one black surface above
the fold besides the hero; one gold accent; pills for controls; no new copy.

    python3 pages/_fd_prelogin.py
"""
import os
import re

import _build as B

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "user-fixed-deposits-app2.html")
BRAND = os.path.join(HERE, "home-premium15.html")
SIGNUP = os.path.join(HERE, "signup.html")
OUT_NAME = "premium-fd2.html"
IMG = "../assets/img/"


def read(p):
    return open(p, encoding="utf-8").read()


def guest_navbar():
    p = read(BRAND)
    m = re.search(r'<header class="(nb [^"]*)" data-v="([^"]+)">(.*?)</header>', p, re.S)
    return '<div class="%s" data-v="%s">%s</div>' % (m.group(1), m.group(2), m.group(3))


def signup_card():
    s = read(SIGNUP)
    tag = re.search(r'<p class="gp-auth__tagline">(.*?)</p>', s).group(1)
    trust = re.findall(r'<li><img src="([^"]+)" alt="[^"]*" width="(\d+)" height="(\d+)"><span>(.*?)</span></li>', s)
    assert len(trust) == 3
    items = "".join(f'<li><img src="{src}" alt="" width="{w}" height="{h}"><span>{t}</span></li>' for src, w, h, t in trust)
    return f'''<section class="pfd-signup" aria-labelledby="pfd-signup-t">
  <!-- COPY: signup.html's headline, tagline and trust points; one CTA to signup.html (the premium pages' "Start investing"). -->
  <h2 id="pfd-signup-t">Invest Smarter. Earn <em>Better.</em></h2>
  <p class="pfd-signup__tag">{tag}</p>
  <ul class="pfd-signup__trust" role="list">{items}</ul>
  <a class="pfd-signup__cta" href="signup.html">Start investing <i class="ph-bold ph-arrow-right" aria-hidden="true"></i></a>
</section>'''


def brand_sections():
    p = read(BRAND)
    m = p[p.index("<main"):p.index("</main>")]
    out = []
    for key in ("h3-why", "h3-track", "h3-voices"):
        i = m.index('aria-labelledby="%s"' % key)
        i = m.rindex("<section", 0, i)
        out.append(m[i:m.index("</section>", i) + len("</section>")])
    i = m.index('<section class="h3-finale"')
    out.append(m[i:m.index("</section>", i) + len("</section>")])
    return out


def brand_css():
    p = read(BRAND)
    i = p.index("<style>\n/* home-premium: page-only styles")
    return p[i:p.index("</style>", p.index("/* home-premium14: home-premium12 in light.")) + len("</style>")]


STYLE = r"""<style>
/* premium-fd2 (pages/_fd_prelogin.py): the signup card in the rail, and the
   full-width branding band from home-premium15 under the FD content. */
.pfd-signup { position: relative; overflow: hidden; display: grid; gap: 14px; padding: 24px; border-radius: 20px; color: #f4e9c8;
  background: radial-gradient(80% 60% at 100% 0%, rgba(212,175,55,.24), transparent 60%), #0b0906; border: 1px solid rgba(212,175,55,.28);
  box-shadow: 0 30px 60px -36px rgba(50,40,17,.6); }
.pfd-signup h2 { margin: 0; font-size: 26px; line-height: 1.15; font-weight: 800; letter-spacing: -.02em; color: #fff; }
.pfd-signup h2 em { font-style: normal; color: #edc967; }
.pfd-signup__tag { margin: 0; font-size: 14px; line-height: 1.5; color: #c9bc9c; }
.pfd-signup__trust { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px; margin: 4px 0 0; padding: 12px 6px; list-style: none; border-radius: 16px; background: rgba(255,255,255,.04); border: 1px solid rgba(212,175,55,.14); }
.pfd-signup__trust li { display: grid; justify-items: center; gap: 6px; text-align: center; font-size: 12px; line-height: 1.3; color: #e9dfc6; }
.pfd-signup__trust img { width: auto; height: 34px; object-fit: contain; }
.pfd-signup__cta { display: inline-flex; align-items: center; justify-content: center; gap: 10px; min-height: 52px; margin-top: 6px; border-radius: 999px;
  background: linear-gradient(100deg, #f7e4a1, #d4af37 55%, #b8902c); color: #1a1408; font-size: 16px; font-weight: 700; transition: transform .3s, filter .3s; }
.pfd-signup__cta:hover { filter: brightness(1.05); }
.pfd-signup__cta:active { transform: scale(.98); }
.pfd-signup__cta i { transition: transform .3s; } .pfd-signup__cta:hover i { transform: translateX(4px); }
.pfd-signup__cta:focus-visible { outline: 2px solid #edc967; outline-offset: 3px; }
.x8r { top: 88px; }
/* the guest navbar's CTA: this page has no final.css, so the pill is set here */
.nb__login { display: inline-flex; align-items: center; height: 40px; padding: 0 20px; border: 0; border-radius: 999px; background: linear-gradient(100deg, #f7e4a1, #d4af37 55%, #b8902c); color: #1a1408; font-size: 14px; font-weight: 600; white-space: nowrap; }
/* the branding band: full width under the FD grid */
.pfd-brand { margin-top: 72px; }
.pfd-brand .h3-sec { padding: clamp(72px, 9vw, 112px) 0; }
@media (max-width: 767px) { .pfd-brand { margin-top: 48px; } .pfd-brand .h3-sec { padding: 64px 0; } }
</style>
"""


def main():
    page = read(SRC)
    # guest navbar, logo and CTA only
    page, n1 = re.subn(r'<header><div class="nb [^"]*" data-v="plain-dark-login">.*?</header>', lambda m: "<header>" + guest_navbar() + "</header>", page, count=1, flags=re.S)
    # rail: signup card, then the offer
    page, n2 = re.subn(r'(<aside class="xb-rail x8r" aria-label=")Offers(">)', r"\1Sign up and offers\2" + signup_card().replace("\\", "\\\\"), page, count=1)
    # branding band after the FD grid, inside <main>
    k = page.index("</main>")
    band = '<div class="h14 pfd-brand">\n' + "\n".join(brand_sections()) + "\n</div>\n"
    page = page[:k] + band + page[k:]
    # styles and icons
    head = brand_css() + "\n" + STYLE
    if "phosphor-icons" not in page:
        head += '<script src="https://unpkg.com/@phosphor-icons/web@2.1.1"></script>\n'
    page = page.replace("</head>", head + "</head>", 1)
    page, n3 = re.subn(r"<title>.*?</title>", "<title>Fixed Deposits | GoldenPi</title>", page, count=1)
    # guest footer (the source carries the logged-in one); keep final.css out, as the source does
    had_final = "final.css" in page
    page = B.ggn_footer(OUT_NAME, page)
    if not had_final:
        page = page.replace('<link rel="stylesheet" href="../assets/final.css">\n', "", 1)
    if (n1, n2, n3) != (1, 1, 1) or "nb__avatar" in page:
        raise SystemExit("user-fixed-deposits-app2.html changed shape (%d %d %d)" % (n1, n2, n3))
    if re.search("[–—]", band + signup_card()):
        raise SystemExit("a dash slipped in")
    open(os.path.join(HERE, OUT_NAME), "w", encoding="utf-8").write(page)
    print(OUT_NAME)


if __name__ == "__main__":
    main()
