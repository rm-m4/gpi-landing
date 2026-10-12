#!/usr/bin/env python3
"""Write premium-bonds.html and premium-fd.html: pre-login landing pages for bonds
and fixed deposits in the premium homepage language (home-premium16's shell: a
black hero with the post-login white cards in home-premium11's carousel, then
light sections, each a shade paler).

Content and cards come from the logged-in pages web-v1 shows as /explore and
/fixed-deposits (user-explore-app7.html, user-fixed-deposits-app2.html), keeping
only what a visitor who is not logged in can use: no pending orders, no portfolio.

  premium-bonds  hero carousel, the golden experience strip, why bonds, the
                 collections as one tabbed rail, the live NCD IPO, categories, app
  premium-fd     hero carousel, first-FD offer, security, Bank / NBFC tabs,
                 PSU vs GoldenPi, the returns calculator, app

Reviewed against taste-skill (2026-10-12): one dark-to-light switch, one gold
accent, cards 22px and controls pills, each layout used once per page, no
eyebrows, no em-dashes, motion only on reveal and on a change of state, all of
it off under reduced motion. Collections and FD lists are one tabbed section,
not three repeated rails.

Chrome (head, navbar, footer, shared scripts, page styles, the carousel script)
is home-premium16's; this writes the <main>, the title and one style block.

    python3 pages/_premium_landing.py && python3 pages/_build.py
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SHELL = os.path.join(HERE, "home-premium16.html")
BONDS_SRC = os.path.join(HERE, "user-explore-app7.html")
FD_SRC = os.path.join(HERE, "user-fixed-deposits-app2.html")
IMG = "../assets/img/"
ARROW = '<i class="ph-bold ph-arrow-right" aria-hidden="true"></i>'


def read(p):
    return open(p, encoding="utf-8").read()


def main_of(page):
    return page[page.index("<main"):page.index("</main>")]


def section(main, cls):
    i = main.index('class="%s"' % cls)
    return main[i:main.index("</section>", i)]


def cards(html):
    return re.findall(r'<a class="gp-ucard[^"]*".*?</a>', html, re.S)


def carousel(three):
    """home-premium11's carousel; the middle card starts in front."""
    slots = "".join('\n      <div class="h2-card h16c" data-pos="%s">%s</div>' % (p, c) for p, c in zip(("-1", "0", "1"), three))
    return ('\n    <div class="h2-stage hp-in" style="--d:4" role="region" aria-roledescription="carousel" aria-label="Top picks">'
            '\n      <button type="button" class="h2-arrow h2-arrow--prev" aria-label="Previous"><i class="ph-bold ph-caret-left" aria-hidden="true"></i></button>'
            + slots +
            '\n      <button type="button" class="h2-arrow h2-arrow--next" aria-label="Next"><i class="ph-bold ph-caret-right" aria-hidden="true"></i></button>'
            '\n    </div>')


def hero(title_html, sub, ctas, three, data_note):
    return f'''  <section class="h2-hero pl-hero" aria-labelledby="pl-title">
    <div class="hp-shell h2-head">
      <h1 class="h3-h1 hp-in" style="--d:1" id="pl-title">{title_html}</h1>
      <p class="h3-lead hp-in" style="--d:2">{sub}</p>
      <div class="hp-hero__ctas hp-in" style="--d:3">{ctas}</div>
    </div>
    <!-- DATA: {data_note} -->{carousel(three)}
  </section>'''


def tabs(gid, label, items):
    """One tabbed rail: items are (id, label, cards_html, more_href or None)."""
    btns = "".join(f'<button type="button" role="tab" class="pl-tab" id="{gid}-t{k}" aria-controls="{gid}-p{k}" aria-selected="{str(k == 0).lower()}" tabindex="{0 if k == 0 else -1}">{lab}</button>'
                   for k, (_, lab, _, _) in enumerate(items))
    panels = "".join(f'''
        <div class="pl-panel" id="{gid}-p{k}" role="tabpanel" aria-labelledby="{gid}-t{k}"{"" if k == 0 else " hidden"}>
          <div class="pl-rail">{body}</div>{f'<a class="pl-more" href="{more}">View all {lab} {ARROW}</a>' if more else ''}
        </div>''' for k, (_, lab, body, more) in enumerate(items))
    return f'<div class="pl-tabs" role="tablist" aria-label="{label}">{btns}</div>{panels}'


def finale():
    shell = main_of(read(SHELL))
    i = shell.index('  <section class="h3-finale"')
    return shell[i:shell.index("</section>", i) + len("</section>")]


# ------------------------------------------------------------------ bonds
def bonds_main():
    m = main_of(read(BONDS_SRC))
    top = cards(section(m, "xa-hero xs"))
    high_ret, high_rated, short = (cards(section(m, c)) for c in ("x7s x7s--sage", "x7s x7s--gold", "x7s x7s--slate"))
    stats = re.findall(r'<li><img src="([^"]+)"[^>]*>([^<]+)</li>', section(m, "x7g"))
    why = section(m, "x7w")
    tiles = re.findall(r'<li class="x7w__tile x7w__tile--(\w+)"><span class="x7w__art"><img src="([^"]+)"[^>]*></span><h3>(.*?)</h3><p>(.*?)</p></li>', why)
    cats = re.findall(r'<a class="x7c__pill" href="collections2-([^"]+)"><img src="([^"]+)"[^>]*>([^<]+)</a>', section(m, "x7c"))
    ipo = section(m, "xb-ipos x7i")
    ipo_logo = re.search(r'<img src="([^"]+)"', ipo).group(1)
    ipo_name = re.search(r'<h3 id="xb-ipo-t">([^<]+)</h3>', ipo).group(1)
    ipo_close = re.search(r'<span class="x7i__pill">([^<]+)</span>', ipo).group(1)
    ipo_facts = re.findall(r'<div><dt>([^<]+)</dt><dd>(.*?)</dd></div>', ipo)
    assert len(top) == 3 and stats and len(tiles) == 2 and len(cats) == 8 and len(ipo_facts) == 4

    ctas = (f'<a class="hp-btn hp-btn--gold" href="signup.html">Start investing {ARROW}</a>'
            '<a class="hp-btn hp-btn--ghost" href="collections-all-bonds.html">View all bonds</a>')
    out = [hero('Invest in <em>Senior Secured Bonds</em>', '9-14% Fixed returns', ctas, top,
                "the three top deals and their cards, as on web-v1/explore (user-explore-app7.html, collections.tabs.json snapshot).")]
    out.append(f'''
  <section class="h3-sec pl-sec pl-s1" aria-labelledby="pl-proof-t">
    <div class="hp-shell">
      <h2 class="pl-kicker" id="pl-proof-t">The Golden Experience Of Investing</h2>
      <ul data-reveal class="pl-proof" role="list">{"".join(f'<li><img src="{src}" alt="" width="48" height="48" loading="lazy">{txt}</li>' for src, txt in stats)}</ul>
    </div>
  </section>''')
    out.append(f'''
  <section class="h3-sec pl-sec pl-s2" aria-labelledby="pl-why-t">
    <div class="hp-shell">
      <h2 data-reveal class="h3-h2" id="pl-why-t">Why invest in bonds on <em>GoldenPi</em>?</h2>
      <ul data-reveal class="pl-tiles" role="list">{"".join(f'<li class="pl-tile pl-tile--{k}"><img src="{src}" alt="" loading="lazy"><h3>{h}</h3><p>{p}</p></li>' for k, src, h, p in tiles)}</ul>
    </div>
  </section>''')
    rails = [("ret", "High Return", "".join(high_ret), "collections-high-returns.html"),
             ("rated", "High Rated", "".join(high_rated), "collections-highly-rated.html"),
             ("short", "Short Term", "".join(short), "collections-short-term.html")]
    out.append(f'''
  <section class="h3-sec pl-sec pl-s3" aria-labelledby="pl-col-t">
    <div class="hp-shell">
      <h2 data-reveal class="h3-h2" id="pl-col-t">Choose Your <em>Category</em></h2>
      <div data-reveal class="pl-cats">{"".join(f'<a class="pl-cat" href="collections-{slug}"><img src="{src}" alt="" width="40" height="40" loading="lazy">{lab}</a>' for slug, src, lab in cats)}</div>
      <div data-reveal class="pl-browse">
        {tabs("col", "Collections", rails)}
      </div>
    </div>
  </section>''')
    facts = "".join(f'<div><dt>{dt}</dt><dd>{dd}</dd></div>' for dt, dd in ipo_facts)
    out.append(f'''
  <section class="h3-sec pl-sec pl-s4" aria-labelledby="pl-ipo-t">
    <div class="hp-shell">
      <h2 data-reveal class="h3-h2" id="pl-ipo-t">Live <em>NCD IPOs</em></h2>
      <!-- DATA: the live NCD IPO as on web-v1/explore. -->
      <article data-reveal class="pl-ipo" aria-labelledby="pl-ipo-name">
        <div class="pl-ipo__id"><img src="{ipo_logo}" alt="" width="56" height="56"><div><p class="pl-ipo__pills"><span class="pl-live">NCD IPO live</span><span>{ipo_close}</span></p><h3 id="pl-ipo-name">{ipo_name}</h3></div></div>
        <dl class="pl-ipo__facts">{facts}</dl>
        <a class="hp-btn hp-btn--gold pl-ipo__cta" href="ipo-details.html">Apply now {ARROW}</a>
      </article>
    </div>
  </section>''')
    out.append("\n" + finale())
    return "\n".join(out)


# --------------------------------------------------------------------- FD
def fd_main():
    m = main_of(read(FD_SRC))
    top = cards(section(m, "xa-hero xs"))
    banks, nbfcs = cards(section(m, "x7s x7s--slate")), cards(section(m, "x7s x7s--gold"))
    offer = re.search(r'<h2 id="x8offer-t">(.*?)</h2>', section(m, "x8offer")).group(1)
    sec = section(m, "x7w")
    sec_h = re.search(r'<h2 id="x8sec-t">(.*?)</h2>', sec).group(1)
    tiles = re.findall(r'<li class="x7w__tile x7w__tile--(\w+)"><span class="x7w__art"><img src="([^"]+)"[^>]*></span><h3>(.*?)</h3><p>(.*?)</p></li>', sec)
    cmp = section(m, "x8cmp")
    rows = re.findall(r'<tr><th scope="row">([^<]+)</th><td>([^<]+)</td><td>([^<]+)</td></tr>', cmp)
    note = re.search(r'<p class="x8cmp__note">([^<]+)</p>', cmp).group(1)
    calc = section(m, "fa-calc")
    plans = re.findall(r'<li class="fa-plan"[^>]*><img src="([^"]+)"[^>]*><h3>([^<]+)</h3>.*?<dd class="fa-gain">([^<]+)</dd></div><div><dt>Tenure</dt><dd>([^<]+)</dd></div><div><dt>Payout</dt><dd>([^<]+)</dd>', calc, re.S)
    assert len(top) == 3 and banks and nbfcs and len(tiles) == 2 and len(rows) == 3 and len(plans) == 2

    ctas = (f'<a class="hp-btn hp-btn--gold" href="signup.html">Start investing {ARROW}</a>'
            '<a class="hp-btn hp-btn--ghost" href="#fd-calculator">Calculate returns</a>')
    out = [hero('Explore <em>Fixed Deposit</em>', 'Highest returns up to 8.5% pa', ctas, top,
                "the three FDs and their cards, as on web-v1/fixed-deposits (user-fixed-deposits-app2.html).")]
    out.append(f'''
  <section class="h3-sec pl-sec pl-s1 pl-sec--slim" aria-labelledby="pl-offer-t">
    <div class="hp-shell">
      <div data-reveal class="pl-offer"><img src="{IMG}refer-earn-gift.png" alt="" width="72" height="72"><h2 id="pl-offer-t">{offer}</h2><a class="hp-btn hp-btn--gold" href="signup.html">Start investing {ARROW}</a></div>
    </div>
  </section>''')
    out.append(f'''
  <section class="h3-sec pl-sec pl-s2" aria-labelledby="pl-sec-t">
    <div class="hp-shell">
      <h2 data-reveal class="h3-h2" id="pl-sec-t">Your FD security is our <em>priority</em></h2>
      <ul data-reveal class="pl-tiles" role="list">{"".join(f'<li class="pl-tile pl-tile--{k}"><img src="{src}" alt="" loading="lazy"><h3>{h}</h3><p>{p}</p></li>' for k, src, h, p in tiles)}</ul>
    </div>
  </section>''')
    out.append(f'''
  <section class="h3-sec pl-sec pl-s3" aria-labelledby="pl-fds-t">
    <div class="hp-shell">
      <h2 data-reveal class="h3-h2" id="pl-fds-t">Bank and NBFC <em>FDs</em></h2>
      <div data-reveal class="pl-browse pl-browse--fd">
        {tabs("fdtype", "FD type", [("bank", "Bank FD", "".join(banks), None), ("nbfc", "NBFC FD", "".join(nbfcs), None)])}
      </div>
    </div>
  </section>''')
    table = "".join(f'<tr><th scope="row">{a}</th><td>{b}</td><td>{c}</td></tr>' for a, b, c in rows)
    out.append(f'''
  <section class="h3-sec pl-sec pl-s4" aria-labelledby="pl-cmp-t">
    <div class="hp-shell">
      <h2 data-reveal class="h3-h2" id="pl-cmp-t">Top PSU Banks vs <em>FDs on GoldenPi</em></h2>
      <!-- DATA: highest returns across tenures and age groups, as on web-v1/fixed-deposits. -->
      <div data-reveal class="pl-cmp">
        <div class="pl-cmp__chart" role="img" aria-label="Highest returns: PSU bank FD 7.20%, FD on GoldenPi 8.50%, 1.30% extra">
          <div class="pl-cmp__col"><b>7.20%</b><span class="pl-cmp__bar" style="--h:72%"></span><span>PSU Bank FD</span></div>
          <span class="pl-cmp__pill">+1.30% Extra</span>
          <div class="pl-cmp__col pl-cmp__col--us"><b>8.50%</b><span class="pl-cmp__bar" style="--h:100%"></span><span>FD on GoldenPi</span></div>
        </div>
        <table class="pl-cmp__table"><thead><tr><th scope="col"><span class="sr-only">Feature</span></th><th scope="col">Traditional Banks</th><th scope="col">GoldenPi FDs</th></tr></thead><tbody>{table}</tbody></table>
      </div>
      <p class="pl-note">{note}</p>
    </div>
  </section>''')
    plan_li = "".join(f'<li class="pl-plan"><img src="{src}" alt="" width="40" height="40"><h3>{name}</h3><dl><div><dt>Returns</dt><dd>{r}</dd></div><div><dt>Tenure</dt><dd>{t}</dd></div><div><dt>Payout</dt><dd>{po}</dd></div></dl><a class="hp-btn hp-btn--gold pl-plan__cta" href="signup.html">Invest</a></li>'
                      for src, name, r, t, po in plans)
    out.append(f'''
  <section class="h3-sec pl-sec pl-s5" id="fd-calculator" aria-labelledby="pl-calc-t">
    <div class="hp-shell">
      <h2 data-reveal class="h3-h2" id="pl-calc-t">Let's find the best FD offerings for your <em>needs</em>!</h2>
      <!-- DATA: the calculator's defaults and its two plans as captured; the rate is the best plan's (8.25%). -->
      <div data-reveal class="pl-calc">
        <div class="pl-calc__in">
          <div class="pl-field"><div class="pl-field__top"><label for="fa-amount">Investment Amount</label><output id="fa-amount-out" for="fa-amount">&#8377; 2,00,000</output></div>
            <input id="fa-amount" type="range" min="10000" max="10000000" step="10000" value="200000"><div class="pl-field__scale"><span>&#8377;10,000</span><span>&#8377;1 Cr</span></div></div>
          <div class="pl-field"><div class="pl-field__top"><label for="fa-tenure">Tenure (Months)</label><output id="fa-tenure-out" for="fa-tenure">60</output></div>
            <input id="fa-tenure" type="range" min="6" max="60" step="6" value="60"><div class="pl-field__scale"><span>6</span><span>60</span></div></div>
          <div class="pl-field pl-field--row"><label for="fa-payout">Payout Mode</label>
            <select id="fa-payout"><option value="cumulative">On maturity</option><option value="periodic">Interest</option></select>
            <span class="pl-rate">Interest Rate <b>8.25%</b></span></div>
        </div>
        <dl class="pl-calc__out" aria-live="polite">
          <div><dt>Invested Amount</dt><dd id="fa-invested">&#8377; 2,00,000</dd></div>
          <div><dt>FD Gains</dt><dd id="fa-gains" class="pl-gain">&#8377; 1,00,852.79</dd></div>
          <div class="pl-calc__total"><dt>Maturity Amount</dt><dd id="fa-maturity">&#8377; 3,00,852.79</dd></div>
        </dl>
      </div>
      <p data-reveal class="pl-plans-t">Here are the best FD plans for you!</p>
      <ul data-reveal class="pl-plans" role="list">{plan_li}</ul>
    </div>
  </section>''')
    out.append("\n" + finale())
    return "\n".join(out)


STYLE = r"""
/* premium landing pages (pages/_premium_landing.py): pl- prefix, on top of
   home-premium16's styles. Shape rule: cards 22px, inner panels 16px,
   controls pills. Sections step paler from sand to white, as on home-premium14. */
.pl-hero .h2-stage { margin-top: 48px; }
.pl-hero .h3-h1 { max-width: 24ch; }
.pl-hero { padding-bottom: clamp(56px, 7vw, 96px); }
.pl-sec { padding: clamp(72px, 9vw, 112px) 0; }
.pl-sec--slim { padding: clamp(32px, 4vw, 48px) 0; }
.h14 .pl-s1 { background: #efe9dc; } .h14 .pl-s2 { background: #f4efe6; } .h14 .pl-s3 { background: #f8f5ef; }
.h14 .pl-s4 { background: #fbf9f5; } .h14 .pl-s5 { background: #fdfcfa; }
.pl-kicker { display: flex; align-items: center; justify-content: center; gap: 16px; font-size: 18px; font-weight: 600; color: #322811; text-align: center; }
.pl-kicker::before, .pl-kicker::after { content: ""; width: 40px; height: 1px; background: #d4af37; }

/* the golden experience strip */
.pl-proof { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); margin-top: 24px; padding: 24px 8px; border-radius: 22px; background: #fff; border: 1px solid #e7e3d9; }
.pl-proof li { display: grid; justify-items: center; gap: 12px; padding: 4px 12px; text-align: center; font-size: 17px; font-weight: 600; color: #322811; }
.pl-proof li + li { border-left: 1px solid #e7e3d9; }
.pl-proof img { width: 48px; height: 48px; object-fit: contain; }

/* two feature tiles with their 3D art */
.pl-tiles { display: grid; gap: 16px; margin-top: 40px; }
@media (min-width: 768px) { .pl-tiles { grid-template-columns: 1fr 1fr; } }
.pl-tile { position: relative; overflow: hidden; display: grid; align-content: start; gap: 10px; padding: clamp(24px, 3vw, 36px); border-radius: 22px; border: 1px solid #e7e3d9;
  background: linear-gradient(160deg, #e6f1e9 0%, #f7fbf8 60%, #fff 100%); }
.pl-tile:nth-child(2) { background: linear-gradient(160deg, #fdeee2 0%, #fff8f3 60%, #fff 100%); }
.pl-tile img { width: 76px; height: 76px; object-fit: contain; margin-bottom: 12px; }
.pl-tile h3 { font-size: 1.35rem; font-weight: 700; color: #322811; }
.pl-tile p { max-width: 46ch; line-height: 1.6; color: #6b6150; }
.pl-tile p b { color: #322811; }

/* categories and the tabbed card rail */
.pl-cats { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin-top: 36px; }
.pl-cat { display: flex; align-items: center; gap: 12px; padding: 16px 18px; border-radius: 22px; background: #fff; border: 1px solid #e7e3d9; font-weight: 600; color: #322811;
  transition: transform .4s cubic-bezier(.16, 1, .3, 1), border-color .4s, box-shadow .4s; }
.pl-cat img { width: 40px; height: 40px; object-fit: contain; }
.pl-cat:hover { transform: translateY(-3px); border-color: rgba(184,144,44,.55); box-shadow: 0 18px 36px -24px rgba(50,40,17,.35); }
.pl-browse { margin-top: 48px; }
.pl-tabs { display: flex; flex-wrap: wrap; gap: 8px; }
.pl-tab { min-height: 44px; padding: 0 20px; border-radius: 999px; border: 1px solid #e0d9c8; background: #fff; color: #322811; font-weight: 600; transition: background-color .3s, color .3s, border-color .3s; }
.pl-tab:hover { border-color: #b8902c; }
.pl-tab[aria-selected="true"] { background: #1a1510; border-color: #1a1510; color: #f4e9c8; }
.pl-tab:focus-visible, .pl-cat:focus-visible { outline: 2px solid #b8902c; outline-offset: 3px; }
.pl-panel { margin-top: 20px; }
.pl-rail { display: grid; grid-auto-flow: column; grid-auto-columns: minmax(340px, 360px); gap: 16px; overflow-x: auto; scroll-snap-type: x mandatory;
  margin-inline: -20px; padding: 4px 20px 16px; scroll-padding-inline: 20px; scrollbar-width: thin; }
.pl-rail > .gp-ucard { scroll-snap-align: start; background: #fff; }
.pl-rail .gp-ucard__issuer { overflow-wrap: anywhere; }
.pl-more { display: inline-flex; align-items: center; gap: 8px; margin-top: 8px; font-weight: 700; color: #8a6520; }
.pl-more i { transition: transform .3s; } .pl-more:hover i { transform: translateX(4px); }
/* FD lists: three cards, no rail needed on desktop */
.pl-browse--fd .pl-rail { grid-auto-flow: row; grid-template-columns: repeat(3, minmax(0, 1fr)); overflow: visible; margin: 0; padding: 0; }

/* FD cards (the post-login .fdc), outside their .x8 page wrapper */
.fdc { display: grid; align-content: start; gap: 18px; padding: 20px; border-radius: 20px; min-height: 0; }
.fdc__id { display: flex; align-items: center; gap: 12px; min-width: 0; }
.fdc .gp-ucard__logo { width: 44px; height: 44px; border-radius: 12px; background: #fff; }
.fdc .gp-ucard__issuer { font-size: 15px; line-height: 1.3; font-weight: 600; }
.fdc__rate { display: grid; gap: 2px; }
.fdc__rate > span { font-size: 12px; font-weight: 500; color: #6b6150; }
.fdc .gp-ucard__rate-value { color: #0a0a0a; font-size: 34px; line-height: 38px; letter-spacing: -1px; text-align: left; }
.fdc .gp-ucard__rate-value span { color: #472d75; font-size: 14px; }
.fdc__safe { display: flex; align-items: center; gap: 10px; margin: 0; padding-top: 14px; border-top: 1px solid rgba(50, 40, 17, .1); }
.fdc__safe img { flex: none; width: 24px; height: 24px; object-fit: contain; }
.fdc__safe span { display: grid; gap: 1px; font-size: 12px; line-height: 1.35; color: #6b6150; }
.fdc__safe b { font-size: 14px; font-weight: 600; color: #322811; }
.fdc__safe--tbc img { filter: grayscale(1); opacity: .5; }
#fdtype-p0 .fdc { border-color: #c2daf0; background: linear-gradient(-45.6deg, #fff 41.2%, #c7def2 99.5%); }
#fdtype-p1 .fdc { border-color: #f2ecc3; background: linear-gradient(-46.6deg, #fff 49.8%, #efeabd 99.5%); }
.pl-hero .h16c .fdc { min-height: 0; }

/* the live NCD IPO: the one black card on the light page */
.pl-ipo { display: grid; gap: 28px; align-items: center; margin-top: 36px; padding: clamp(24px, 3vw, 40px); border-radius: 22px; color: #f4e9c8;
  background: radial-gradient(60% 120% at 100% 0%, rgba(212,175,55,.22), transparent 60%), #0b0906; box-shadow: 0 40px 80px -40px rgba(50,40,17,.6); }
@media (min-width: 1024px) { .pl-ipo { grid-template-columns: 1.1fr 1.4fr auto; } }
.pl-ipo__id { display: flex; align-items: center; gap: 16px; }
.pl-ipo__id img { width: 56px; height: 56px; padding: 4px; border-radius: 16px; background: #fff; object-fit: contain; }
.pl-ipo__id h3 { margin-top: 8px; font-size: 1.3rem; font-weight: 700; color: #fff; }
.pl-ipo__pills { display: flex; flex-wrap: wrap; gap: 8px; font-size: 12px; }
.pl-ipo__pills span { padding: 4px 10px; border-radius: 999px; border: 1px solid rgba(212,175,55,.35); color: #e9dfc6; }
.pl-ipo__pills .pl-live { border-color: rgba(60,207,117,.45); color: #3ccf75; }
.pl-ipo__facts { display: grid; grid-template-columns: repeat(4, auto); justify-content: space-between; gap: 16px; }
.pl-ipo__facts dt { font-size: 12px; color: #a99c7e; }
.pl-ipo__facts dd { margin-top: 4px; font-size: 1.2rem; font-weight: 700; color: #fff; white-space: nowrap; }
.pl-ipo__cta { justify-self: start; }

/* FD offer */
.pl-offer { display: flex; flex-wrap: wrap; align-items: center; gap: 16px 24px; padding: 20px 28px; border-radius: 22px;
  background: linear-gradient(100deg, #f7e4a1 0%, #e6c65c 50%, #d4af37 100%); color: #1a1408; }
.pl-offer img { width: 72px; height: 72px; object-fit: contain; }
.pl-offer h2 { flex: 1 1 280px; font-size: clamp(1.15rem, 1.8vw, 1.5rem); font-weight: 700; line-height: 1.3; }
.pl-offer .hp-btn--gold { background: #1a1510; color: #f4e9c8; }

/* PSU vs GoldenPi: two columns, no track behind them */
.pl-cmp { display: grid; gap: 40px; align-items: center; margin-top: 40px; }
@media (min-width: 1024px) { .pl-cmp { grid-template-columns: .9fr 1.1fr; } }
.pl-cmp__chart { display: grid; grid-template-columns: 1fr auto 1fr; align-items: end; gap: 16px; height: 300px; padding: 28px; border-radius: 22px; background: #fff; border: 1px solid #e7e3d9; }
.pl-cmp__col { display: grid; grid-template-rows: auto 1fr auto; justify-items: center; gap: 10px; height: 100%; text-align: center; font-size: 14px; color: #6b6150; }
.pl-cmp__col b { font-size: 1.6rem; color: #322811; }
.pl-cmp__bar { align-self: end; width: 72px; height: var(--h); border-radius: 16px 16px 6px 6px; background: #e7e1d3; }
.pl-cmp__col--us .pl-cmp__bar { background: linear-gradient(180deg, #f7e4a1, #d4af37 55%, #b8902c); }
.pl-cmp__col--us b { color: #8a6520; }
.pl-cmp__pill { align-self: center; padding: 6px 12px; border-radius: 999px; background: #1a1510; color: #f4e9c8; font-size: 13px; font-weight: 700; white-space: nowrap; }
.pl-cmp__table { width: 100%; border-collapse: separate; border-spacing: 0; overflow: hidden; border-radius: 22px; background: #fff; border: 1px solid #e7e3d9; font-size: 15px; }
.pl-cmp__table th, .pl-cmp__table td { padding: 18px 20px; text-align: left; color: #322811; }
.pl-cmp__table thead th { background: #1a1510; color: #f4e9c8; font-weight: 600; }
.pl-cmp__table tbody tr + tr > * { border-top: 1px solid #efe9dc; }
.pl-cmp__table tbody th { font-weight: 600; }
.pl-cmp__table td:last-child { color: #8a6520; font-weight: 600; }
.pl-note { margin-top: 16px; font-size: 13px; color: #7d725c; }
@media (prefers-reduced-motion: no-preference) {
  .reveal-ready .pl-cmp .pl-cmp__bar { transform: scaleY(.04); transform-origin: bottom; transition: transform 1.1s cubic-bezier(.16, 1, .3, 1) .2s; }
  .reveal-ready .pl-cmp.is-in .pl-cmp__bar { transform: none; }
}

/* the calculator: inputs on white, results on the black panel */
.pl-calc { display: grid; overflow: hidden; margin-top: 40px; border-radius: 22px; background: #fff; border: 1px solid #e7e3d9; box-shadow: 0 30px 60px -40px rgba(50,40,17,.35); }
@media (min-width: 900px) { .pl-calc { grid-template-columns: 1.2fr .8fr; } }
.pl-calc__in { display: grid; gap: 28px; padding: clamp(24px, 3vw, 40px); }
.pl-field__top { display: flex; justify-content: space-between; align-items: baseline; gap: 12px; }
.pl-field label { font-weight: 600; color: #322811; }
.pl-field output { font-size: 1.2rem; font-weight: 700; color: #322811; font-variant-numeric: tabular-nums; }
.pl-field input[type="range"] { width: 100%; margin-top: 14px; accent-color: #b8902c; }
.pl-field__scale { display: flex; justify-content: space-between; margin-top: 6px; font-size: 12px; color: #7d725c; }
.pl-field--row { display: flex; flex-wrap: wrap; align-items: center; gap: 12px 16px; }
.pl-field select { min-height: 44px; padding: 0 14px; border-radius: 999px; border: 1px solid #e0d9c8; background: #fff; color: #322811; font-weight: 600; }
.pl-field select:focus-visible, .pl-field input:focus-visible { outline: 2px solid #b8902c; outline-offset: 3px; }
.pl-rate { margin-left: auto; color: #6b6150; } .pl-rate b { color: #8a6520; }
.pl-calc__out { display: grid; align-content: center; gap: 22px; padding: clamp(24px, 3vw, 40px); color: #f4e9c8;
  background: radial-gradient(70% 70% at 100% 0%, rgba(212,175,55,.2), transparent 60%), #0b0906; }
.pl-calc__out dt { font-size: 13px; color: #a99c7e; }
.pl-calc__out dd { margin-top: 4px; font-size: 1.35rem; font-weight: 700; color: #fff; font-variant-numeric: tabular-nums; }
.pl-calc__out .pl-gain { color: #edc967; }
.pl-calc__total { padding-top: 20px; border-top: 1px solid rgba(212,175,55,.2); }
.pl-calc__total dd { font-size: clamp(1.8rem, 3vw, 2.4rem); letter-spacing: -.02em; }
.pl-plans-t { margin-top: 40px; font-size: 1.15rem; font-weight: 700; color: #322811; }
.pl-plans { display: grid; gap: 12px; margin-top: 16px; }
@media (min-width: 900px) { .pl-plans { grid-template-columns: 1fr 1fr; } }
.pl-plan { display: grid; grid-template-columns: 40px 1fr auto; align-items: center; gap: 14px 16px; padding: 18px 20px; border-radius: 22px; background: #fff; border: 1px solid #e7e3d9; }
.pl-plan img { width: 40px; height: 40px; border-radius: 12px; object-fit: contain; }
.pl-plan h3 { font-weight: 700; color: #322811; }
.pl-plan dl { grid-column: 2 / -1; display: flex; flex-wrap: wrap; gap: 6px 28px; }
.pl-plan dt { font-size: 12px; color: #7d725c; } .pl-plan dd { font-weight: 700; color: #322811; }
.pl-plan dl div:first-child dd { color: #8a6520; }
.pl-plan__cta { grid-row: 1; grid-column: 3; height: 44px; padding: 0 20px; }

/* phones */
@media (max-width: 767px) {
  .pl-proof { grid-template-columns: repeat(3, minmax(0, 1fr)); padding: 18px 4px; }
  .pl-proof li { font-size: 13px; padding: 4px 6px; }
  .pl-proof img { width: 36px; height: 36px; }
  .pl-cats { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .pl-cat { padding: 12px 14px; font-size: 14px; }
  .pl-cat img { width: 32px; height: 32px; }
  .pl-rail, .pl-browse--fd .pl-rail { grid-auto-flow: column; grid-template-columns: none; grid-auto-columns: min(84%, 320px); overflow-x: auto; margin-inline: -20px; padding: 4px 20px 16px; scrollbar-width: none; }
  .pl-rail::-webkit-scrollbar { display: none; }
  .pl-ipo__facts { grid-template-columns: repeat(2, auto); }
  .pl-cmp__chart { height: 260px; padding: 20px; }
  .pl-cmp__table th, .pl-cmp__table td { padding: 14px 12px; font-size: 13px; }
  .pl-plan { grid-template-columns: 40px 1fr; }
  .pl-plan__cta { grid-row: auto; grid-column: 1 / -1; justify-content: center; }
}
"""

SCRIPT = r"""<script>
// premium landing pages: the tabbed rails. Without this the first panel is the
// only one shown and the others stay hidden.
(function () {
  document.querySelectorAll('.pl-tabs').forEach(function (list) {
    var tabs = [].slice.call(list.querySelectorAll('[role="tab"]'));
    function pick(n, focus) {
      tabs.forEach(function (t, k) {
        var on = k === n;
        t.setAttribute('aria-selected', String(on));
        t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
      });
      if (focus) tabs[n].focus();
    }
    tabs.forEach(function (t, k) {
      t.addEventListener('click', function () { pick(k); });
      t.addEventListener('keydown', function (e) {
        var d = { ArrowRight: 1, ArrowLeft: -1 }[e.key];
        if (d) { e.preventDefault(); pick((k + d + tabs.length) % tabs.length, true); }
      });
    });
  });
})();
</script>
"""

# The FD calculator, as on user-fixed-deposits-app2.html: quarterly compounding on
# maturity, simple interest when paid out (2,00,000 at 8.25% for 60 months gives
# 3,00,852.79, the captured figure).
CALC = r"""<script>
(function () {
  var RATE = 8.25;
  var amount = document.getElementById('fa-amount'), tenure = document.getElementById('fa-tenure'), payout = document.getElementById('fa-payout');
  if (!amount) return;
  function inr(n, paise) {
    return '₹ ' + n.toLocaleString('en-IN', { minimumFractionDigits: paise ? 2 : 0, maximumFractionDigits: paise ? 2 : 0 });
  }
  function update() {
    var p = +amount.value, m = +tenure.value, r = RATE / 100;
    var maturity = payout.value === 'cumulative' ? p * Math.pow(1 + r / 4, m / 3) : p * (1 + r * m / 12);
    document.getElementById('fa-amount-out').textContent = inr(p);
    document.getElementById('fa-tenure-out').textContent = m;
    document.getElementById('fa-invested').textContent = inr(p);
    document.getElementById('fa-gains').textContent = inr(maturity - p, true);
    document.getElementById('fa-maturity').textContent = inr(maturity, true);
  }
  [amount, tenure, payout].forEach(function (el) { el.addEventListener('input', update); });
  update();
})();
</script>
"""

TITLES = {"premium-bonds.html": "Corporate Bonds | GoldenPi", "premium-fd.html": "Fixed Deposits | GoldenPi"}


# premium-bonds only: the carousel's front card in black, not home-premium16's sage
# (user, 2026-10-12). premium-fd keeps the sage.
BLACK_FRONT = """.h16c[data-pos="0"] .gp-ucard { border-color: #2b2b2b; background: linear-gradient(135deg, #2e2e2e 0%, #161616 40%, #0a0a0a 100%); color: #f5f5f5; }
.h16c[data-pos="0"] .gp-ucard * { color: inherit; }
.h16c[data-pos="0"] .gp-ucard__rate-value, .h16c[data-pos="0"] .gp-ucard__rate-value span { color: #fff; }
.h16c[data-pos="0"] .gp-ucard__metrics dt, .h16c[data-pos="0"] .gp-ucard__sold { color: #a3a3a3; }
.h16c[data-pos="0"] .gp-ucard__tags span { background: #2b2b2b; }
"""


def build(name, main_html, extra_js="", extra_css=""):
    page = read(SHELL)
    i, j = page.index("<main"), page.index("</main>") + len("</main>")
    page = page[:i] + '<main id="main-content">\n' + main_html + "\n</main>" + page[j:]
    page, n = re.subn(r"<title>.*?</title>", "<title>%s</title>" % TITLES[name], page, count=1)
    k = page.index("/* home-premium14: home-premium12 in light.")
    k = page.index("</style>", k)
    page = page[:k] + STYLE + extra_css + page[k:]
    b = page.rindex("</body>")
    page = page[:b] + SCRIPT + extra_js + page[b:]
    if n != 1 or re.search("[–—]", main_html):
        raise SystemExit("%s: shell changed shape, or a dash slipped in" % name)
    open(os.path.join(HERE, name), "w", encoding="utf-8").write(page)
    print(name)


def main():
    build("premium-bonds.html", bonds_main(), extra_css=BLACK_FRONT)
    build("premium-fd.html", fd_main(), CALC)


if __name__ == "__main__":
    main()
