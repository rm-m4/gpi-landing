#!/usr/bin/env python3
"""bond-details5.html and bond-details6.html: the Mahaveer bond page with the
user's Figma design (file HRSMFFccdLgqf1YwD7oyc9, node 29:1409, "In Stock").

bond-details5 is bond-details3 itself, components and all, with only the
Figma's header card and highlights swapped in (both highlights variants, one
under the other). bond-details6 is the whole page
in the Figma's design, at its 1018px width, in bond-details3's section order.

From the Figma (bond-details6): the dark header card, the highlights card (its first
variant), the returns calculator, the white accordion cards and the gold-ruled
section labels. Its own sample copy (Navi Finserv, 11.73%, "Zero TDS",
"No brokerage", the AU Bank logo) is not used: every figure and sentence is
bond-details3's, read the same way bond-details4 reads it. The highlights'
sample figures stay marked as sample data.

Assets are the Figma's, downloaded to assets/img/bd5/.

    python3 pages/_bond_beta.py && python3 pages/_bond_v5.py
"""
import os

import _bond_beta as B
import _bond_v4 as V4

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "bond-details5.html")
# bond-details6: the whole page in the Figma's design, at its own width, 1018px (629px column + 360px rail).
# bond-details5: bond-details3's page and components, with only the header card and highlights from the Figma.
OUT6 = os.path.join(HERE, "bond-details6.html")
NARROW = ("<style>.b5 { max-width: 1018px; }\n"
          "@media (min-width: 1024px) { .b5-layout { grid-template-columns: minmax(0, 629px) 360px; } }</style>\n")
IMG = "../assets/img/bd5/"
esc, amt, lead, sample = V4.esc, V4.amt, V4.lead, V4.sample


def crop(name, box_w, box_h, left, top, w, h, cls=""):
    """An image cropped inside a fixed box, as the Figma frames it (percentages are the design's)."""
    return ('<span class="b5-crop %s" style="width:%spx;height:%spx" aria-hidden="true">'
            '<img src="%s%s" alt="" style="left:%s;top:%s;width:%s;height:%s"></span>'
            % (cls, box_w, box_h, IMG, name, left, top, w, h))


# ------------------------------------------------------------------ header
STAT_ICONS = [  # (file, inner box w, h, left, top) inside the 36px tile, from the Figma
    ("stat-returns.png", 54, 36, -11, 0),
    ("stat-tenure.png", 37, 24, 0, 7),
    ("stat-rating.png", 36, 24, 0, 6),
    ("stat-security.png", 36, 24, 0, 6),
]


def crumbs(d):
    links = "".join('<a href="%s">%s</a><span aria-hidden="true">&rsaquo;</span>' % (esc(h), esc(x))
                     for h, x in d["crumbs"])
    return ('<nav class="b5-crumbs" aria-label="Breadcrumb">%s<span aria-current="page">%s</span></nav>'
            % (links, esc(d["crumb_here"])))


def header(d):
    stats = dict(d["stats"])
    cells = [("Returns", stats["Returns"]), ("Tenure", stats["Tenure"]),
             ("Credit Rating", stats["Credit rating"]), ("Security", "%sx" % B.HL_COVER)]
    items = []
    for (label, value), (f, w, h, l, t) in zip(cells, STAT_ICONS):
        items.append('<div class="b5-stat"><span class="b5-stat__ico" aria-hidden="true">'
                     '<img src="%s%s" alt="" style="width:%dpx;height:%dpx;left:%dpx;top:%dpx"></span>'
                     '<dl><dt>%s</dt><dd>%s</dd></dl></div>' % (IMG, f, w, h, l, t, esc(label), esc(value)))
    lit = round(d["sold_pct"] / 100 * 12)
    segs = "".join('<i%s></i>' % (' class="on"' if k < lit else "") for k in range(12))
    return f'''
<header class="b5-hc" aria-labelledby="b5-name">
  <div class="b5-hc__top">
    <div class="b5-hc__id">
      <span class="b5-hc__logo"><img src="{esc(d["logo"])}" alt="Mahaveer Finance India Limited logo" width="42" height="42"></span>
      <div><h1 id="b5-name">{esc(d["name"])}</h1><p>{esc(d["kind"])}</p></div>
    </div>
    <div class="b5-hc__acts">
      <span class="b5-pill b5-pill--gold">{esc(d["sell"])}</span>
      <button type="button" class="b5-hc__save" aria-label="Add to watchlist"><img src="{IMG}bookmark.svg" alt="" width="13.3333" height="16.6667"></button>
    </div>
  </div>
  <div class="b5-hc__stats">{'<span class="b5-hc__div" aria-hidden="true"></span>'.join(items)}</div>
  <div class="b5-hc__foot">
    <p class="b5-sold"><span>Sold {d["sold_pct"]}%</span><span class="b5-sold__segs" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="{d["sold_pct"]}" aria-label="{esc(d["sold"])}">{segs}</span></p>
    <span class="b5-pill b5-pill--dash">{esc(d["form121"])}</span>
  </div>
</header>'''


# --------------------------------------------------------------- highlights
def proof(d):
    """The three proof figures (sample data in v3), icon over value over label."""
    items = [
        (crop("proof-money.png", 40, 40, "-11.25%", "-10%", "120%", "120%"), d["repaid"][0], d["repaid"][1]),
        (crop("proof-people.png", 51, 45, "1.96%", "-4.44%", "96.08%", "108.89%"), d["investors"][1], d["investors"][0]),
        (crop("proof-100.png", 69, 41, "-5.8%", "-39.02%", "105.8%", "178.05%"), d["repayments"][1], d["repayments"][0]),
    ]
    return '<span class="b5-proof__div" aria-hidden="true"></span>'.join(
        '<div><span class="b5-proof__ico">%s</span><dl><dt>%s</dt><dd>%s</dd></dl></div>' % (ico, sample(v), esc(l))
        for ico, v, l in items)


def highlights(d):
    pts = "".join("<li>%s</li>" % lead(p) for p in d["reasons"])
    (cov_t, cov_p), (sell_t, sell_p) = d["confidence"][1], d["confidence"][0]
    b = d["backers"]
    lenders = "".join('<img src="%s%s" alt="" width="%d" height="41"%s>' % (IMG, f, w, r)
                      for f, w, r in (("lender-1.png", 41, ""), ("lender-2.png", 38, ""),
                                      ("lender-4.png", 41, ' class="is-round"')))
    proof_html = proof(d)
    return f'''
<section class="b5-card b5-hl" aria-labelledby="b5-reasons">
  <div class="b5-hl__reasons">
    <img class="b5-hl__hand" src="{IMG}reasons-hand.png" alt="" width="150" height="146">
    <div><h2 id="b5-reasons">{esc(d["reasons_title"])}</h2><ul>{pts}</ul></div>
  </div>
  <div class="b5-hl__tiles">
    <article class="b5-tile b5-tile--green">
      {crop("tile-shield.png", 174, 87, "-15.09%", "0", "75%", "100%")}
      <p class="b5-tile__eye">{esc(d["kind"])}</p>
      <h3>{esc(cov_t)}</h3><p>{esc(cov_p)}</p>
    </article>
    <article class="b5-tile b5-tile--peach">
      {crop("tile-clock.png", 174, 87, "-14.48%", "0", "75.19%", "100%")}
      <h3>{esc(sell_t)}</h3><p>{esc(sell_p)}</p>
      <h3 class="b5-tile__more">{esc(d["form121"])}</h3>
    </article>
  </div>
  <div class="b5-proof">{proof_html}</div>
  <div class="b5-lenders">
    <div><h3>{esc(b[1])}</h3><p>{sample(b[2])}</p></div>
    <div class="b5-lenders__logos" aria-hidden="true">{lenders}</div>
  </div>
</section>'''


def highlights2(d):
    """The Figma's second highlights variant (node 29:1897), laid out after the
    user's reference (2026-10-07): two equal columns under one rule, the proof
    figures in their own band, then the backers. Same content as highlights()."""
    pts = "".join("<li>%s</li>" % esc(p) for p in d["reasons"])
    (cov_t, cov_p), (sell_t, sell_p) = d["confidence"][1], d["confidence"][0]
    b = d["backers"]
    logos = "".join('<img src="%s%s" alt="" width="%d" height="64"%s>' % (IMG, f, w, r)
                    for f, w, r in (("lender-1.png", 64, ""), ("lender-2.png", 59, ""),
                                    ("lender-4.png", 64, ' class="is-round"')))
    return f'''
<section class="b5-card b5-h2" aria-labelledby="b5-reasons2">
  <div class="b5-h2__cols">
    <div class="b5-h2__col">
      <img class="b5-h2__art" src="{IMG}reasons-hand.png" alt="" width="150" height="146">
      <p class="b5-h2__eye">{esc(d["kind"])}</p>
      <h2 id="b5-reasons2">{esc(d["reasons_title"])}</h2>
      <ul>{pts}</ul>
    </div>
    <div class="b5-h2__col b5-h2__col--right">
      <article>
        {crop("tile-shield.png", 174, 87, "-15.09%", "0", "75%", "100%", "b5-h2__art")}
        <p class="b5-h2__eye">{esc(d["kind"])}</p>
        <h3>{esc(cov_t)}</h3><p>{esc(cov_p)}</p>
      </article>
      <article>
        {crop("tile-clock.png", 174, 87, "-14.48%", "0", "75.19%", "100%", "b5-h2__art")}
        <h3>{esc(sell_t)}</h3><p>{esc(sell_p)}</p>
        <h3 class="b5-h2__stat">{esc(d["form121"])}</h3>
      </article>
    </div>
  </div>
  <div class="b5-h2__proof">{proof(d)}</div>
  <div class="b5-h2__back">
    <div class="b5-h2__logos" aria-hidden="true">{logos}</div>
    <div><p class="b5-h2__eye">{esc(b[0])}</p><h3>{esc(b[1])}</h3><p>{sample(b[2])}</p></div>
  </div>
</section>'''


# --------------------------------------------------------------- accordions
def acc(title, body, open_=False, extra=""):
    return ('<details class="b5-acc"%s><summary><span class="b5-acc__t">%s%s</span>'
            '<img class="b5-acc__chev" src="%schevron-down.svg" alt="" width="16" height="16"></summary>'
            '<div class="b5-acc__body">%s</div></details>' % (" open" if open_ else "", esc(title), extra, IMG, body))


def label(text):
    return '<h2 class="b5-label"><span aria-hidden="true"></span>%s<span aria-hidden="true"></span></h2>' % esc(text)


def cashflow(d):
    yrs = []
    for n, y in enumerate(d["years"]):
        rows = "".join('<tr><th scope="row">%s%s</th><td>%s</td><td>%s</td></tr>'
                       % (esc(dt), ' <span class="b4-mat">%s</span>' % esc(m) if m else "", amt(i), amt(p))
                       for dt, m, i, p in y["rows"])
        yrs.append(f'''<details class="b4-year"{" open" if n == 0 else ""}>
      <summary><span class="b4-year__y">{esc(y["year"])}</span><span class="b4-year__ev">{esc(d["events"].get(y["year"], ""))}</span><span class="b4-year__a">{amt(y["interest"])}</span><span class="b4-year__a">{amt(y["principal"])}</span><i class="b5-yc" aria-hidden="true"></i></summary>
      <table class="b4-pay"><thead class="sr-only"><tr><th scope="col">Date</th><th scope="col">Interest</th><th scope="col">Principal</th></tr></thead><tbody>{rows}</tbody></table>
    </details>''')
    (pl, pv), (il, iv) = d["split"]
    body = f'''<div class="b4-cfsum">
    <div><span>Investment Amount</span><strong>{amt(d["invest"])}</strong></div>
    <div class="b4-cfsum__total"><span>Total Receivable</span><strong>{amt(d["receivable"])}</strong>
      <p class="b4-split"><span>{esc(pl)} <b>{amt(pv)}</b></span><span aria-hidden="true">+</span><span>{esc(il)} <b class="b4-gain">{amt(iv)}</b></span></p></div>
  </div>
  <div class="b4-years" role="group" aria-label="Payouts by year">
    <div class="b4-years__head" aria-hidden="true"><span>Date</span><span></span><span>Interest</span><span>Principal</span></div>
    {"".join(yrs)}
  </div>
  <div class="b4-cffoot"><p>{esc(d["cf_note"])}</p><button type="button" class="b4-link">{esc(d["cf_download"])}</button></div>'''
    return '<div id="cashflow">%s</div>' % acc("Cashflow", body)


def company(d, data):
    facts = "".join('<div class="b5-fact"><dt>%s</dt><dd>%s</dd></div>' % (esc(k), esc(v)) for k, v in d["facts"])
    about = '<dl class="b5-facts">%s</dl><div class="b5-prose">%s</div>' % (facts, "".join("<p>%s</p>" % p for p in d["about"]))
    sw = ('<div class="b4-sw"><div class="b4-sw__col b4-sw__col--good"><h4>Key Strengths</h4><ol>%s</ol></div>'
          '<div class="b4-sw__col b4-sw__col--watch"><h4>Watch out</h4><ol>%s</ol></div></div>'
          % ("".join("<li>%s</li>" % lead(x) for x in d["strengths"]), "".join("<li>%s</li>" % lead(x) for x in d["watch"])))
    cards = []
    for name, pts in data:
        zero, ext = B.scale([v for _, v in pts])
        ch = B.change(pts)
        delta = ('<p class="b4-delta b4-delta--%s">%s %.1f%% <span>vs %s</span></p>'
                 % ("up" if ch[0] >= 0 else "down", "&#9650;" if ch[0] >= 0 else "&#9660;", abs(ch[0]), ch[1])) if ch else ""
        bars = "".join('<li><span class="b4-bar" style="--top:%.1f%%;--h:%.1f%%"><b>%s</b></span><span class="b4-bar__y">%s</span></li>'
                       % (top, h, B.crore(v), y) for (y, v), (top, h) in zip(pts, ext))
        t = B.SUBTITLE.get(name, name)
        cards.append('<article class="b4-fin"><h3>%s</h3><p class="b4-fin__v">%s <span>%s</span></p>%s'
                     '<ol class="b4-bars" style="--zero:%.1f%%" aria-label="%s by year">%s</ol></article>'
                     % (esc(t), B.crore(pts[-1][1]), pts[-1][0], delta, zero, esc(t), bars))
    ratios = "".join('<div><dt>%s</dt><dd>%s</dd><dd class="b4-ok">%s</dd></div>' % (esc(a), esc(b), esc(c.title()))
                     for a, b, c in d["ratios"])
    fin = ('<div class="b4-fins">%s</div><h3 class="b5-fy">Financial Ratio <span class="b5-fy__tag">'
           '<i aria-hidden="true"></i>%s</span></h3><dl class="b4-ratios">%s</dl>' % ("".join(cards), esc(d["fy"]), ratios))
    return ('<section id="company" aria-labelledby="b5-co">%s' % label("Company Information").replace("<h2 ", '<h2 id="b5-co" ', 1)
            + acc("About the Issuer", about, open_=True) + acc("Strength / Weaknesses", sw)
            + acc("Company Financials", fin) + "</section>")


def documents(d):
    docs = "".join(
        '<li><a href="%s" target="_blank" rel="noopener noreferrer"><span><b>%s</b><small>%s</small></span>'
        '<span class="b4-doc__act">%s</span></a></li>' % (esc(h), esc(n), esc(m), esc(a)) for n, m, a, h in d["docs"])
    tt, tx = d["tax"]
    spec = "".join('<div%s><dt>%s</dt><dd>%s</dd></div>' % (' class="b4-spec__wide"' if len(v) > 32 else "", esc(k), esc(v))
                   for k, v in d["spec"])
    body_docs = '<ul class="b4-docs b5-docs">%s</ul><p class="b4-tax"><span><b>%s</b> %s</span></p>' % (docs, esc(tt), esc(tx))
    return ('<section id="documents" aria-labelledby="b5-do">%s' % label("Documents and More Details").replace("<h2 ", '<h2 id="b5-do" ', 1)
            + acc("Documents", body_docs) + acc("More Bond Details", '<dl class="b4-spec">%s</dl>' % spec) + "</section>")


def app_band(d):
    t, s = d["app"]
    return ('<section class="b5-card b5-app" aria-labelledby="b5-app"><div><h2 id="b5-app">%s</h2><p>%s</p></div>'
            '<img src="%s" alt="%s" width="110" height="136" loading="lazy"></section>' % (esc(t), esc(s), esc(d["qr"]), esc(s)))


def calculator(d):
    return f'''
<aside class="b5-rail" aria-labelledby="b5-calc-t">
  <div class="b5-calc">
    <h2 id="b5-calc-t">{esc(d["calc_title"])}</h2>
    <div class="b5-step" role="group" aria-label="Units">
      <button type="button" class="b4-step__btn b5-step__minus" data-step="-1" aria-label="Decrease units" disabled>&minus;</button>
      <input class="b4-step__input" type="number" inputmode="numeric" min="1" value="1" aria-label="Units">
      <button type="button" class="b4-step__btn b5-step__plus" data-step="1" aria-label="Increase units">+</button>
    </div>
    <dl class="b5-calc__rows">
      <div><dt>Investment Amount</dt><dd>{amt(d["invest"])}</dd></div>
      <div><dt>Total Returns <img src="{IMG}info.svg" alt="" width="12" height="12"> <span class="b5-ytm">{esc(d["ytm"])}</span></dt><dd class="b5-gain">+ {amt(d["returns"])}</dd></div>
      <div class="b5-calc__total"><dt>Total Receivable <img src="{IMG}info-2.svg" alt="" width="12" height="12"></dt><dd class="b5-gain">{amt(d["receivable"])}</dd></div>
    </dl>
    <a class="b5-btn b5-btn--line" href="#cashflow">{esc(d["timeline_cta"])}<img src="{IMG}chevron-right.svg" alt="" width="17" height="17"></a>
    <button type="button" class="b5-btn b5-btn--gold">{esc(d["invest_cta"])}<img src="{IMG}arrow-up-right.svg" alt="" width="17.021" height="17.021"></button>
  </div>
</aside>'''


STYLE = """<style>
/* bond-details5: the Figma's components (node 29:1409) over bond-details4's
   inner section styles. Satoshi throughout, the project's typeface; the
   Figma mixes in Inter. */
.b5 { --ink: #322811; --sub: #666666; --gold-grad: linear-gradient(147.7deg, #fdf2d0 0%, #e6b325 50%, #b38600 100%);
  --light-yellow: #fdf3d4; --green: #00b256; max-width: 1200px; padding-top: 18px; }
.b5-layout { display: grid; grid-template-columns: minmax(0, 1fr); gap: 30px; }
@media (min-width: 1024px) {
  .b5-layout { grid-template-columns: minmax(0, 1fr) 360px; column-gap: 29px; align-items: start; }
  .b5-main { grid-column: 1; }
  .b5-rail { grid-column: 2; grid-row: 1 / span 2; position: sticky; top: calc(var(--header-height, 96px) + 16px); }
}
.b5-main { display: grid; gap: 30px; min-width: 0; }
.b5-crumbs { display: flex; flex-wrap: wrap; align-items: center; gap: 12px; margin: 0 0 24px; color: var(--sub); font-size: 13px; font-weight: 500; }
.b5-crumbs a { text-decoration: none; }
.b5-crumbs [aria-current] { color: var(--ink); }
.b5-crop { position: relative; display: block; flex: none; overflow: hidden; }
.b5-crop img { position: absolute; max-width: none; }

/* Header card */
.b5-hc { padding: 19px 20px 24px; border-radius: 20px; color: #fff;
  background: radial-gradient(889px 348px at 100% 100%, #27272a 0%, #18181b 40%, #0c0c0e 70%, #060607 85%, #000 100%); }
.b5-hc__top { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; }
.b5-hc__id { display: flex; align-items: center; gap: 24px; min-width: 0; }
.b5-hc__logo { display: grid; place-items: center; flex: none; width: 79px; height: 79px; border: 2px solid #edc967; border-radius: 50%; }
.b5-hc__logo img { width: 56px; height: 56px; border-radius: 50%; object-fit: cover; }
.b5-hc h1 { color: rgba(255, 255, 255, 0.9); font-size: 28px; line-height: 31px; font-weight: 700; }
.b5-hc__id p { margin-top: 8px; color: rgba(255, 255, 255, 0.5); font-size: 14px; line-height: 16px; font-weight: 500; }
.b5-hc__acts { display: flex; align-items: center; gap: 20px; flex: none; }
.b5-pill { display: inline-flex; align-items: center; justify-content: center; height: 40px; padding: 8px 14px; border-radius: 45px; font-size: 14px; font-weight: 500; white-space: nowrap; }
.b5-pill--gold { border: 1px solid rgba(255, 255, 255, 0.1); color: #edc967; }
.b5-pill--dash { height: auto; min-width: 164px; border: 0.5px dashed rgba(255, 255, 255, 0.4); color: #fff; }
.b5-hc__save { display: grid; place-items: center; width: 40px; height: 40px; border: 0.86px solid rgba(255, 255, 255, 0.1); border-radius: 50%; background: rgba(0, 0, 0, 0.4); backdrop-filter: blur(10px); cursor: pointer; }
.b5-hc__save:focus-visible, .b5-btn:focus-visible { outline: 2px solid #edc967; outline-offset: 2px; }
.b5-hc__stats { display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 28px 0; }
.b5-hc__div { width: 1px; height: 25px; background: rgba(219, 207, 178, 0.25); }
.b5-stat { display: flex; align-items: center; gap: 8px; }
.b5-stat__ico { position: relative; flex: none; width: 36px; height: 36px; border-radius: 8px; overflow: hidden; }
.b5-stat__ico img { position: absolute; object-fit: cover; max-width: none; }
.b5-stat dt { color: rgba(255, 255, 255, 0.6); font-size: 14px; line-height: 13.5px; font-weight: 500; white-space: nowrap; }
.b5-stat dd { margin-top: 8px; color: rgba(255, 255, 255, 0.9); font-size: 16px; font-weight: 700; white-space: nowrap; }
.b5-hc__foot { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 12px; }
.b5-sold { display: flex; align-items: center; gap: 10px; color: #ececec; font-size: 14px; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; }
.b5-sold__segs { display: flex; gap: 2px; }
.b5-sold__segs i { width: 6.91px; height: 6px; border-radius: 2px; opacity: 0.8; background: linear-gradient(139deg, rgba(253, 242, 208, 0.5) 25%, rgba(230, 179, 37, 0.5) 78%, rgba(179, 134, 0, 0.5) 100%); }
.b5-sold__segs i.on { background: linear-gradient(139deg, #fdf2d0 25%, #e6b325 78%, #b38600 100%); }

/* Cards */
.b5-card { padding: 32px; border-radius: 24px; background: #fff; }
.b5-hl { display: grid; gap: 24px; }
.b5-hl__reasons { display: flex; gap: 20px; padding: 24px; border-radius: 20px; background: #fff7e8; border-bottom: 1px solid #fff0d4; }
.b5-hl__hand { flex: none; width: 150px; height: 145.714px; object-fit: contain; object-position: bottom; }
.b5-hl h2 { color: #20231f; font-size: 20px; line-height: 1.08; font-weight: 700; }
.b5-hl ul { margin-top: 20px; display: grid; gap: 21px; padding-left: 21px; list-style: disc; color: #252525; font-size: 14px; line-height: 1.5; }
.b5-hl ul b { font-weight: 700; }
.b5-hl__tiles { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.b5-tile { display: flex; flex-direction: column; gap: 4px; padding: 20px; border-radius: 20px; color: #252525; font-size: 14px; line-height: 1.5; }
.b5-tile .b5-crop { margin-bottom: 12px; }
.b5-tile--green { background: #e8f7ee; border-bottom: 1px solid #e1f2e8; }
.b5-tile--peach { background: #fff1e8; border-bottom: 1px solid #f7e6db; }
.b5-tile__eye { margin-bottom: 12px; color: #7a571f; font-size: 13px; font-weight: 700; }
.b5-tile h3 { color: #171f29; font-size: 20px; line-height: 1.2; font-weight: 700; }
.b5-tile__more { margin-top: 12px; }
.b5-proof { display: flex; align-items: center; justify-content: center; min-height: 125px; padding: 16px 0; border-radius: 20px; background: #fcfbf6; border-bottom: 1px solid #fdf2d0; }
.b5-proof > div { display: flex; flex-direction: column; align-items: center; gap: 4px; width: 174px; text-align: center; }
.b5-proof__ico { display: grid; place-items: center; height: 45px; }
.b5-proof dt { color: var(--ink); font-size: 16px; line-height: 27.5px; font-weight: 500; }
.b5-proof dd { color: #252525; font-size: 14px; line-height: 1.5; }
.b5-proof__div { width: 1px; height: 50px; background: rgba(231, 227, 217, 0.6); }
.b5-lenders { display: flex; align-items: center; gap: 20px; padding: 20px; border-radius: 20px; background: #f4fbfd; border-bottom: 1px solid #e6f5fa; }
.b5-lenders > div:first-child { flex: 1; min-width: 0; }
.b5-lenders h3 { color: #20231f; font-size: 20px; line-height: 1.08; font-weight: 700; }
.b5-lenders p { margin-top: 10px; color: #252525; font-size: 14px; line-height: 1.5; }
.b5-lenders__logos { display: flex; align-items: center; flex: none; }
.b5-lenders__logos img { height: 41px; object-fit: cover; }
.b5-lenders__logos img.is-round { border-radius: 50%; }

/* Highlights, second variant (Figma 29:1897, laid out after the user's
   reference). One 8px rhythm: 8 inside a group, 16 / 24 between parts,
   40 between bands. Hairlines, no fills: the illustrations carry the colour. */
.b5-h2 { --rule: #e9e3d6; padding: 40px; border-radius: 20px; color: #252525; }
.b5-h2__cols { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); }
.b5-h2__col { display: flex; flex-direction: column; min-width: 0; padding-right: 32px; }
.b5-h2__col--right { padding: 0 0 0 32px; border-left: 1px solid var(--rule); }
.b5-h2__art { margin-bottom: 24px; }
img.b5-h2__art { width: 150px; height: 146px; object-fit: contain; object-position: left bottom; }
.b5-h2__eye { color: #936e30; font-size: 15px; line-height: 1.5; font-weight: 700; }
.b5-h2 h2, .b5-h2 h3 { color: #20231f; font-size: 20px; line-height: 1.25; font-weight: 700; letter-spacing: -0.01em; }
.b5-h2__col > .b5-h2__eye + h2 { margin-top: 16px; }
.b5-h2 ul { margin-top: 24px; padding-left: 20px; list-style: disc; display: grid; gap: 20px; font-size: 15px; line-height: 1.6; }
.b5-h2 ul li::marker { color: #b9a77e; }
.b5-h2 article { display: flex; flex-direction: column; font-size: 15px; line-height: 1.6; }
.b5-h2 article + article { margin-top: 32px; padding-top: 32px; border-top: 1px solid var(--rule); }
.b5-h2 article .b5-h2__eye { margin-bottom: 8px; }
.b5-h2 article h3 + p { margin-top: 8px; }
.b5-h2__stat { margin-top: 24px; }
.b5-h2__proof { display: flex; align-items: flex-start; justify-content: space-around; margin-top: 40px; padding: 40px 0; border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule); }
.b5-h2__proof > div { display: flex; flex-direction: column; align-items: center; gap: 12px; flex: 1; text-align: center; }
.b5-h2__proof .b5-proof__ico { display: grid; place-items: center; height: 45px; }
.b5-h2__proof dt { color: var(--ink); font-size: 18px; line-height: 1.4; font-weight: 500; }
.b5-h2__proof dd { margin-top: 2px; font-size: 15px; line-height: 1.5; }
.b5-h2__proof .b5-proof__div { align-self: center; width: 1px; height: 56px; background: var(--rule); }
.b5-h2__back { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); align-items: center; padding-top: 40px; }
.b5-h2__back > div:last-child { display: flex; flex-direction: column; gap: 8px; padding-left: 32px; font-size: 15px; line-height: 1.5; }
.b5-h2__logos { display: flex; align-items: center; }
.b5-h2__logos img { height: 64px; margin-right: -16px; object-fit: cover; }
.b5-h2__logos img:last-child { margin-right: 0; }
.b5-h2__logos img.is-round { border-radius: 50%; }

/* Section label and accordions */
.b5-main > section:not(.b5-card) { display: grid; gap: 16px; }
.b5-label { display: flex; align-items: center; justify-content: center; gap: 8px; color: var(--ink); font-size: 14px; line-height: 12px; font-weight: 700; }
.b5-label span { width: 24px; height: 1px; opacity: 0.7; background: linear-gradient(170deg, #fdf2d0 0%, #e6b325 50%, #b38600 100%); }
.b5-acc { border-radius: 22px; background: #fff; border-bottom: 1px solid var(--light-yellow); filter: drop-shadow(0 2px 1px rgba(0, 0, 0, 0.02)); }
.b5-acc > summary { display: flex; align-items: center; justify-content: space-between; gap: 12px; min-height: 56px; padding: 0 24px; cursor: pointer; list-style: none; }
.b5-acc > summary::-webkit-details-marker { display: none; }
.b5-acc > summary:focus-visible { outline: 2px solid #e6b325; outline-offset: -2px; border-radius: 22px; }
.b5-acc__t { color: var(--ink); font-size: 16px; font-weight: 700; }
.b5-acc__chev { flex: none; transition: transform 0.25s ease; }
.b5-acc[open] > summary .b5-acc__chev { transform: scaleY(-1); }
.b5-acc__body { padding: 4px 24px 24px; }
#cashflow { scroll-margin-top: calc(var(--header-height, 96px) + 16px); }

.b5-facts { display: flex; flex-wrap: wrap; gap: 14px; margin-bottom: 20px; }
.b5-fact { min-width: 180px; padding: 14px 24px; border-radius: 20px; background: #fcfbfa; box-shadow: 0 40px 100px -20px rgba(179, 134, 0, 0.08); }
.b5-fact dt { color: var(--sub); font-size: 14px; line-height: 18px; font-weight: 500; }
.b5-fact dd { margin-top: 3px; color: var(--ink); font-size: 14px; font-weight: 700; }
.b5-prose { display: grid; gap: 21px; color: var(--sub); font-size: 14px; line-height: 21px; font-weight: 500; }
.b5-prose strong { color: var(--ink); }
.b5-fy { display: flex; align-items: center; gap: 12px; margin: 24px 0 14px; color: var(--ink); font-size: 16px; font-weight: 700; }
.b5-fy__tag { display: inline-flex; align-items: center; gap: 8px; font-size: 14px; line-height: 12px; letter-spacing: 0.28px; text-transform: uppercase; }
.b5-fy__tag i { width: 8px; height: 8px; border-radius: 50%; background: #22c55e; }
.b5-docs a { grid-template-columns: 1fr auto; }
.b5-yc { width: 16px; height: 16px; background: url(../assets/img/bd5/chevron-down.svg) center / 16px no-repeat; transition: transform 0.25s ease; }
.b4-year[open] > summary .b5-yc { transform: scaleY(-1); }
.b5 .b4-years__head, .b5 .b4-year > summary { grid-template-columns: 70px 1fr 1fr 1fr 16px; }
.b5 .b4-pay tr { grid-template-columns: calc(70px + 8px + (100% - 70px - 16px - 32px) / 3) 1fr 1fr 16px; }

/* Calculator */
.b5-calc { padding: 20px; border-radius: 22px; background: #fff; border-bottom: 1px solid var(--light-yellow); box-shadow: 0 2px 2px rgba(0, 0, 0, 0.02); }
.b5-calc h2 { color: var(--ink); font-size: 16px; line-height: 26.25px; font-weight: 700; }
.b5-step { position: relative; display: grid; grid-template-columns: 36px 1fr 36px; align-items: center; height: 48px; margin: 13px 14px 13px; padding: 0 5px; border: 0.86px solid #e7e3d9; border-radius: 100px; }
.b5-step .b4-step__btn { width: 36px; height: 36px; border: 0; border-radius: 50%; display: grid; place-items: center; color: var(--ink); font: inherit; font-weight: 700; cursor: pointer; }
.b5-step__minus { background: #faf9f6; font-size: 26px !important; font-weight: 500 !important; }
.b5-step__plus { background: linear-gradient(103.2deg, #fdf2d0 0%, #e6b325 50%, #b38600 100%); font-size: 20.6px !important; }
.b5-step .b4-step__btn:disabled { opacity: 0.45; cursor: not-allowed; }
.b5-step .b4-step__input { width: 100%; border: 0; background: transparent; text-align: center; font: inherit; font-size: 18px; font-weight: 700; letter-spacing: 0.43px; color: var(--ink); -moz-appearance: textfield; }
.b5-step .b4-step__input::-webkit-inner-spin-button { -webkit-appearance: none; }
.b5-calc__rows { padding: 0 8px; }
.b5-calc__rows > div { display: flex; align-items: center; justify-content: space-between; gap: 8px; padding: 6px 0; }
.b5-calc__rows dt { display: inline-flex; align-items: center; gap: 6px; color: var(--ink); font-size: 13px; font-weight: 500; letter-spacing: 0.13px; }
.b5-calc__rows dd { color: var(--ink); font-size: 14px; font-weight: 500; white-space: nowrap; }
.b5-ytm { padding: 2px 6px; border-radius: 3.5px; background: rgba(34, 197, 94, 0.1); color: var(--green); font-size: 10px; font-weight: 700; letter-spacing: 0.2px; }
.b5-calc .b5-gain { color: var(--green); font-weight: 700; }
.b5-calc__total { margin-top: 8px; padding-top: 14px !important; border-top: 1px solid #fdf3d4; }
.b5-calc__total dd { font-size: 18px; line-height: 28px; }
.b5-btn { display: flex; align-items: center; justify-content: center; gap: 6px; width: 297px; max-width: 100%; margin: 13px auto 0; border-radius: 100px; color: var(--ink); font: inherit; font-size: 14px; font-weight: 700; text-decoration: none; cursor: pointer; }
.b5-btn--line { height: 40px; border: 0.5px solid #fdf2d0; background: #fff; }
.b5-btn--gold { height: 44px; border: 0; background: var(--gold-grad); }
.b5-btn:active { transform: scale(0.98); }
.b5-app { display: flex; align-items: center; justify-content: space-between; gap: 20px; }
.b5-app h2 { color: var(--ink); font-size: 20px; font-weight: 700; }
.b5-app p { margin-top: 6px; color: var(--sub); font-size: 14px; }
.b5-app img { flex: none; width: 110px; height: auto; }

@media (max-width: 767px) {
  .b5-hc__top { flex-direction: column; }
  .b5-hc__id { gap: 14px; }
  .b5-hc__logo { width: 64px; height: 64px; }
  .b5-hc__logo img { width: 46px; height: 46px; }
  .b5-hc h1 { font-size: 24px; }
  .b5-hc__stats { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
  .b5-hc__div { display: none; }
  .b5-card { padding: 20px 16px; }
  .b5-hl__reasons { flex-direction: column; padding: 20px; }
  .b5-hl__hand { width: 110px; height: 107px; }
  .b5-hl__tiles { grid-template-columns: 1fr; }
  .b5-proof { flex-wrap: wrap; }
  .b5-proof > div { width: 33%; }
  .b5-proof__div { display: none; }
  .b5-proof dt { font-size: 14px; white-space: nowrap; }
  .b5-lenders { flex-direction: column; align-items: flex-start; }
  .b5-h2 { padding: 24px 20px; }
  .b5-h2__cols, .b5-h2__back { grid-template-columns: 1fr; }
  .b5-h2__col { padding: 0; }
  .b5-h2__col--right { margin-top: 32px; padding: 32px 0 0; border-left: 0; border-top: 1px solid var(--rule); }
  .b5-h2__proof { margin-top: 32px; padding: 32px 0; }
  .b5-h2__proof dt { font-size: 15px; white-space: nowrap; }
  .b5-h2__proof dd { font-size: 13px; }
  .b5-h2__back { gap: 20px; padding-top: 32px; }
  .b5-h2__back > div:last-child { padding-left: 0; }
  .b5-acc > summary { padding: 0 16px; }
  .b5-acc__body { padding: 4px 16px 20px; }
  .b5-fact { min-width: 0; flex: 1 1 40%; padding: 12px 16px; }
  .b5 .b4-years__head, .b5 .b4-year > summary { grid-template-columns: 52px 1fr 1fr 16px; }
  .b5 .b4-pay tr { grid-template-columns: 1fr 1fr 1fr; }
  .b5-app img { width: 84px; }
}
@media (prefers-reduced-motion: reduce) { .b5-acc__chev, .b5-yc { transition: none; } }
</style>
"""


EMBED = """<style>
/* bond-details5: only the header card and highlights are the Figma's; they sit
   in bond-details3's own column, so the .b4/.b5 wrapper gives up its page box. */
.b5-embed { max-width: none; margin: 0; padding: 0; display: grid; gap: 30px; }
/* Group headings (bond-details3's "Company Information" / "Documents and More
   Details") as small all-caps labels: they name a group, so they should not
   compete with the card titles under them. Cards sit close inside a group;
   groups stand apart. */
.ci { gap: 12px; margin-top: 12px; }
.ci__title { margin: 0 0 4px 4px; color: #8a6520; font-size: 12px; line-height: 16px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; }
@media (max-width: 639px) { .ci { gap: 10px; margin-top: 8px; } .ci__title { font-size: 11px; line-height: 16px; } }
/* Beta hides its breadcrumb below md; bond-details5 shows it on phones too,
   under the mobile top bar. */
@media (max-width: 767px) {
  .bond-details-page nav[aria-label="Breadcrumb"] { display: block !important; padding: 4px 0 0; margin-bottom: -12px; }
  .bond-details-page nav[aria-label="Breadcrumb"] ol { flex-wrap: nowrap; overflow-x: auto; scrollbar-width: none; white-space: nowrap; }
}
</style>
"""


# bond-details5's navbar in the Figma header's colours (node 29:1520). Scoped
# to this page: assets/navbar.css is shared.
NAV = """<style>
.nb--dark {
  --nb-bg: rgba(14, 10, 0, 0.94); --nb-solid: #0e0a00; --nb-ink: #ffffff; --nb-muted: rgba(255, 255, 255, 0.6);
  --nb-line: rgba(255, 255, 255, 0.05); --nb-field: transparent; --nb-field-line: rgba(255, 255, 255, 0.15);
  --nb-active: #edc967; --nb-rule: #edc967;
}
.nb--dark.nb { -webkit-backdrop-filter: blur(12px); backdrop-filter: blur(12px); }
.nb--dark .nb__link.is-current::after {
  left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, rgba(237, 201, 103, 0) 0%, #edc967 50%, rgba(237, 201, 103, 0) 100%);
  box-shadow: 0 -6px 16px 2px rgba(237, 201, 103, 0.35);
}
.nb--dark .nb__search {
  background: linear-gradient(172.85deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0) 100%), rgba(255, 255, 255, 0.02);
  -webkit-backdrop-filter: blur(14px); backdrop-filter: blur(14px);
}
.nb--dark .nb__search .nb-ic, .nb--dark .nb__search-btn .nb-ic { color: #edc967; }
.nb--dark .nb__actions::before { content: ""; width: 1px; height: 21px; margin-right: 4px; background: rgba(255, 255, 255, 0.1); }
.nb--dark .nb__btn { border-color: transparent; background: transparent; color: rgba(255, 255, 255, 0.85); }
.nb--dark .nb__btn:hover { border-color: rgba(255, 255, 255, 0.15); }
.nb--dark .nb__avatar {
  border: 0; color: #000; font-weight: 700;
  background: linear-gradient(103.19deg, #fdf2d0 0%, #e6b325 50%, #b38600 100%);
}
</style>
"""


# Test data, not the issuer's: the last financials tab (Cash & Cash Eq.) becomes a PAT-like series that goes
# negative, so the design shows how the chart draws losses.
HYPO = ("negative test data", [("2024", 96000000.0), ("2025", -128000000.0), ("2026", -41000000.0)])


# Loss bars in the same gold as the rest (bond-details3 colours them red), hanging below the zero line.
NEG_CSS = """<style>
.f3 .fin-col--neg .fin-bar__fill { background: linear-gradient(0deg, var(--bar-graph-gold-gradient-start), var(--bar-graph-gold-gradient-end)); }
.f3 .fin-col--neg:not(:last-child) .fin-bar__fill { background: linear-gradient(0deg, #f3e2a9, #ebd38c); }
.f3 .fin-col--neg .fin-bar__value { color: var(--bar-graph-gold-value-color); }
.f3 .fin-col--neg:not(:last-child) .fin-bar__value { color: var(--subtext); }
</style>"""


def negative_tab(h):
    """bond-details3's financials tabs and panels re-rendered with the Cash & Cash Eq. tab swapped for HYPO."""
    data = [HYPO if n == "Cash & Cash Eq." else (n, pts)
            for n, pts in B.series(open(B.CAP + ".expanded.html", encoding="utf-8").read())]
    assert HYPO in data
    new = B.fin_v3(data, "", "", ratios=[("", "", "", "")])  # ratios are cut; the page keeps its own
    new = new[:new.index('<div class="f3-ratios">')]
    a = h.index('<div data-testid="bond-company-financials" class="f3">')
    b = h.index('<div class="f3-ratios">', a)
    return h[:a] + "<!-- DATA: the last tab is test data, not the issuer's -->" + new + h[b:]


def hybrid(h, d):
    """bond-details5: bond-details3 as it is, with its header card and
    highlights block swapped for the Figma's."""
    for start, new in (('<section class="hc"', header(d)), ('<section class="hl"', highlights(d) + highlights2(d))):
        i = h.index(start)
        j = h.index("</section>", i) + len("</section>")
        h = h[:i] + '<div class="b4 b5 b5-embed">%s</div>' % new + h[j:]
    h = negative_tab(h)
    h = h.replace("<!-- Generated by pages/_bond_beta.py from the beta.goldenpi.com capture; do not edit. -->",
                  "<!-- Generated by pages/_bond_v5.py: bond-details3.html with the Figma's header card and "
                  "highlights (HRSMFFccdLgqf1YwD7oyc9 29:1409); do not edit. -->", 1)
    return h.replace("</head>", V4.ICONS + V4.STYLE + STYLE + EMBED + NAV + NEG_CSS + "</head>", 1)


def main():
    h = open(V4.SRC, encoding="utf-8").read()
    d = V4.read(h)
    data = B.series(open(B.CAP + ".expanded.html", encoding="utf-8").read())
    body = ('<main id="main-content"><div class="b4 b5">%s<div class="b5-layout"><div class="b5-main">%s%s%s%s%s%s</div>%s</div></div>%s</main>'
            % (crumbs(d), header(d), highlights(d), cashflow(d),
               company(d, data), documents(d), app_band(d), calculator(d), V4.mobile_bar(d)))
    head = h[:h.index("<main")]
    head = head.replace("<!-- Generated by pages/_bond_beta.py from the beta.goldenpi.com capture; do not edit. -->",
                        "<!-- Generated by pages/_bond_v5.py (bond-details6: Figma HRSMFFccdLgqf1YwD7oyc9 29:1409 at its "
                        "1018px width, content from bond-details3.html); do not edit. -->", 1)
    head = head.replace("</head>", V4.ICONS + V4.STYLE + STYLE + NARROW + "</head>", 1)
    tail = h[h.index("</main>") + len("</main>"):]
    tail = B.drop(tail, '<div id="cashflow-modal"')
    for marker in ("// Stand-in for beta's React handlers", "// bond-details3 financials"):
        k = tail.index(marker)
        tail = tail[:tail.rfind("<script>", 0, k)] + tail[tail.index("</script>", k) + len("</script>"):]
    tail = tail.replace("</body>", V4.SCRIPT + "</body>", 1)
    for out, text in ((OUT, hybrid(h, d)), (OUT6, head + body + tail)):
        with open(out, "w", encoding="utf-8") as f:
            f.write(text)
        print("%s  %d bytes" % (os.path.relpath(out, os.path.dirname(HERE)), len(text)))


if __name__ == "__main__":
    main()
