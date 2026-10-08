#!/usr/bin/env python3
"""user-corporate-bonds3.html: the logged-in bonds page, in two acts.

1. Why bonds: the greeting, the 15% headline figure, the Bank FD comparison
   and the four reasons to hold bonds.
2. Investment options: the Collections explorer from user-corporate-bonds2
   (pages/_explore_bonds.py), one tab per collection with its bond cards.

Then live IPOs, reviews and the FAQ, as on the other user pages. Every string
comes from content/*.md: the reasons from this page's own FAQ, the FD
comparison and the diversify line from goldenpi.com/invest-in-bonds, the
15% figure and the CTA label from uatnew /corporate-bonds.

    python3 pages/_explore_bonds3.py
"""
import os
import re

import _explore_bonds as X

U, esc = X.U, X.esc
HERE = X.HERE
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "user-corporate-bonds3.html")


def content(name):
    with open(os.path.join(ROOT, "content", name + ".md"), encoding="utf-8") as f:
        return f.read()


def need(text, s):
    if s not in text:
        raise SystemExit("not in the capture any more, re-check the copy: %r" % s)
    return s


def reasons():
    """[(title, body, icon)]: the three halves of this page's FAQ answer
    'Why should I invest in Bonds and Debentures?', then diversification."""
    answer = dict(U.faqs("corporate-bonds"))["Why should I invest in Bonds and Debentures?"]
    out = [tuple(a.split(" – ", 1)) for a in answer]
    iib = content("prod_invest-in-bonds")
    out.append(("Diversify Your Portfolio with Bonds", need(iib,
                "Bonds have historically demonstrated a lower correlation with equities, "
                "making them an effective tool for reducing volatility.")))
    icons = ["money-profit.png", "online-money.png", "no-tax.png", "diversify-portfolio.png"]
    return [(t, b, i) for (t, b), i in zip(out, icons)]


def why():
    iib = content("prod_invest-in-bonds")
    cb = content("corporate-bonds")
    note = content("prod_user_corporate-bonds")
    risk = re.search(r"- (Fixed returns do not constitute guaranteed or assured returns\. "
                     r"Investments in corporate debt.*?default in payment\.)", note).group(1)
    items = "\n".join(
        '          <li class="wb__reason">\n'
        '            <img src="../assets/img/%s" alt="" width="56" height="56" loading="lazy">\n'
        '            <h3>%s</h3>\n'
        '            <p>%s</p>\n'
        '          </li>' % (i, esc(t), esc(b)) for t, b, i in reasons())
    need(cb, "Fixed returns as high as 15%")
    need(cb, "Explore Our Corporate Bonds List")
    need(iib, "Bonds can offer higher returns, diversification, liquidity, and tax benefits compared to "
              "fixed deposits, with some risks involved.")
    return '''  <!-- ============================================================= why bonds -->
  <!-- Act one: why bonds. Greeting, the 15%% figure and the Bank FD comparison,
       then the four reasons. DATA: first name of the logged-in account. -->
  <section class="wb gp-shell" aria-labelledby="wb-title">
    <div class="wb__hero">
      <div class="wb__copy">
        <h1 class="wb__title" id="wb-title">Hi %s, Explore Corporate Bonds</h1>
        <p class="wb__sub">Discover reliable income and stable capital growth with Corporate Bond Investments</p>
        <p class="wb__figure">Fixed returns as high as <span class="gp-hero__figure"><span data-count>15</span>%%</span></p>
        <a class="gp-cta gp-cta--primary wb__cta" href="#collections">Explore Our Corporate Bonds List</a>
      </div>
      <!-- DATA: FD vs bond comparison, goldenpi.com/invest-in-bonds 2026-09-28. -->
      <figure class="wb__fd">
        <h2 class="wb__fd-title">Get better Returns than Bank FDs</h2>
        <p class="wb__fd-sub">Bonds can offer higher returns, diversification, liquidity, and tax benefits compared to fixed deposits, with some risks involved.</p>
        <p class="wb__fd-earn">1&nbsp;Lac Invested could earn <b>&#8377; <span data-count data-sep>15,000</span></b> more in 5 years</p>
        <div class="gp-vbars wb__bars" data-reveal>
          <div class="gp-vbars__col" style="--h:%.0f%%"><span class="gp-vbars__val">6.80%%</span><span class="gp-vbars__bar"></span><span class="gp-vbars__label">Bank Deposit</span></div>
          <div class="gp-vbars__col gp-vbars__col--bond" style="--h:100%%"><span class="gp-vbars__val">11.02%%</span><span class="gp-vbars__bar"></span><span class="gp-vbars__label">Bond</span></div>
        </div>
        <figcaption class="wb__fd-note">Based on pre-tax returns of high rated bonds (AA rated ) &amp; SBI FD returns (AAA rated)**</figcaption>
      </figure>
    </div>

    <div class="wb__why">
      <h2 class="wb__why-title">Why should I invest in Bonds and Debentures?</h2>
      <ul class="wb__reasons gp-stagger" role="list" data-reveal>
%s
      </ul>
      <p class="wb__risk">%s</p>
    </div>
  </section>
''' % (U.NAME, 6.80 / 11.02 * 100, items, esc(risk))


def options():
    """Act two: the explorer, under a heading of its own."""
    ex = X.explorer()
    head = ('    <div class="gp-shell">\n'
            '      <h2 class="wb__options-title">Explore our extensive Corporate Bonds Collections</h2>\n')
    need(content("corporate-bonds"), "Explore our extensive Corporate Bonds Collections")
    return ex.replace('    <div class="gp-shell">\n', head, 1)


STYLE = """<style>
/* user-corporate-bonds3: act one, why bonds. The explorer below is
   user-corporate-bonds2's block, unchanged. */
.wb { padding-top: 32px; }
.wb__hero {
  display: grid; gap: 20px; align-items: stretch;
  padding: 20px; border: 1px solid #f0e6c8; border-radius: 28px;
  background: radial-gradient(900px 360px at 0% 0%, rgba(212, 175, 55, 0.16), transparent 60%), var(--white);
}
@media (min-width: 900px) { .wb__hero { grid-template-columns: 1.15fr 1fr; gap: 28px; padding: 28px; } }
.wb__copy { display: flex; flex-direction: column; align-items: flex-start; justify-content: center; padding: 12px 8px; }
@media (min-width: 900px) { .wb__copy { padding: 16px 12px 16px 20px; } }
.wb__title { margin: 0; color: var(--app-heading-color); font-size: clamp(26px, 3.4vw, 42px); font-weight: 700; line-height: 1.15; letter-spacing: -0.02em; }
.wb__title [data-user] { color: #8a6520; }
.wb__sub { margin: 12px 0 0; max-width: 46ch; color: var(--subtext); font-size: 16px; line-height: 1.55; }
.wb__figure { margin: 28px 0 0; color: var(--app-heading-color); font-size: clamp(20px, 2.2vw, 26px); font-weight: 500; line-height: 1.3; }
.wb__figure .gp-hero__figure { font-size: 1.5em; }
.wb__cta { margin-top: 28px; }

/* The comparison card: the page's one dark surface, the header's ink. */
.wb__fd {
  margin: 0; display: flex; flex-direction: column; padding: 28px 24px 22px; border-radius: 22px;
  background: radial-gradient(520px 260px at 100% 0%, rgba(212, 175, 55, 0.22), transparent 65%), #221b0c;
  color: #f4e9c8;
}
.wb__fd-title { margin: 0; color: #fff8e4; font-size: 22px; font-weight: 700; line-height: 1.25; }
.wb__fd-sub { margin: 8px 0 0; color: rgba(244, 233, 200, 0.72); font-size: 14px; line-height: 1.5; }
.wb__fd-earn { margin: 18px 0 0; font-size: 15px; color: rgba(244, 233, 200, 0.85); }
.wb__fd-earn b { color: #e8c766; font-size: 22px; font-weight: 900; font-variant-numeric: tabular-nums; }
.wb__bars { height: 180px; margin-top: 18px; }
.wb__bars .gp-vbars__bar { background: rgba(255, 248, 228, 0.14); }
.wb__bars .gp-vbars__col--bond .gp-vbars__bar { background: var(--gp-gradient-gold); }
.wb__bars .gp-vbars__val, .wb__bars .gp-vbars__label { color: rgba(244, 233, 200, 0.8); }
.wb__bars .gp-vbars__col--bond .gp-vbars__val { color: #e8c766; }
.wb__fd-note { margin-top: auto; padding-top: 16px; color: rgba(244, 233, 200, 0.6); font-size: 12px; line-height: 1.5; }

.wb__why { margin-top: 40px; }
.wb__why-title, .wb__options-title { margin: 0 0 20px; color: var(--app-heading-color); font-size: clamp(20px, 2.2vw, 26px); font-weight: 700; line-height: 1.25; }
.wb__reasons { display: grid; gap: 12px; margin: 0; padding: 0; list-style: none; }
@media (min-width: 640px) { .wb__reasons { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (min-width: 1100px) { .wb__reasons { grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; } }
.wb__reason { padding: 20px; border: 1px solid var(--light-stroke); border-radius: 20px; background: var(--white); }
.wb__reason img { display: block; width: 48px; height: 48px; object-fit: contain; }
.wb__reason h3 { margin: 14px 0 0; color: var(--app-heading-color); font-size: 16px; font-weight: 700; line-height: 1.3; }
.wb__reason p { margin: 6px 0 0; color: var(--subtext); font-size: 14px; line-height: 1.55; }
.wb__risk { margin: 16px 0 0; max-width: 110ch; color: var(--subtext); font-size: 12px; line-height: 1.55; }

.wb + .ex { padding-top: 48px; }
.wb__options-title { scroll-margin-top: 96px; }
#collections { scroll-margin-top: 80px; }
@media (max-width: 639px) {
  .wb { padding-top: 20px; }
  .wb__copy { padding: 4px 0; }
  .wb__fd { padding: 22px 18px 18px; }
  .wb__bars { height: 150px; gap: 28px; }
  .wb__reason { display: grid; grid-template-columns: 40px 1fr; column-gap: 14px; padding: 16px; }
  .wb__reason img { grid-row: span 2; width: 40px; height: 40px; }
  .wb__reason h3 { margin: 0; }
}
</style>
"""


def main():
    text = U.md("corporate-bonds")
    title = re.search(r"\*\*Title:\*\* (.+)", text).group(1)
    desc = re.search(r"\*\*Meta description:\*\* (.+)", text).group(1)
    top, bottom = U.shell(esc(title), U.html.escape(desc), "bonds")
    top = top.replace("<!-- Post-login page, generated by pages/_user.py",
                      "<!-- Post-login bonds page: why bonds, then the Collections explorer. Generated by\n"
                      "     pages/_explore_bonds3.py; base page by pages/_user.py", 1)
    ipos = U.live_ipos().replace('<section data-reveal class="', '<section id="live-ipos" data-reveal class="', 1)
    body = "\n".join([why(), options(), ipos, U.trusted("corporate-bonds"), U.faq("corporate-bonds")])
    page = U.F.primary_ctas(top + "\n" + body + bottom)
    page = (page.replace("</head>", X.STYLE + STYLE + "</head>", 1)
                .replace("</body>", X.SCRIPT + "</body>", 1))
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page)
    print("%s  %d bytes" % (os.path.relpath(OUT, ROOT), len(page)))


if __name__ == "__main__":
    main()
