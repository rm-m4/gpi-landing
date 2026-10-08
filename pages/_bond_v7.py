#!/usr/bin/env python3
"""bond-details7.html: bond-details5 with the header card and the highlights
card from the user's Figma (file HRSMFFccdLgqf1YwD7oyc9, node 37:222):
the dark hero (37:417) and "Reasons to invest" (37:548).

Copied as designed, Inter and all, except for width: both cards fill
bond-details5's column instead of the Figma's 629px. Every figure and sentence
is bond-details3's (Mahaveer), read the same way bond-details5 reads it; the
Figma's Navi Finserv sample copy is not used. Its two labels with no Mahaveer
equivalent ("Anytime Liquidity", "<issuer> on GoldenPi") are kept as design
labels. bond-details5 itself is not touched.

    python3 pages/_bond_beta.py && python3 pages/_bond_v7.py
"""
import os
import re

import _bond_v4 as V4
import _bond_v5 as V5
import _bond_beta as B

OUT = os.path.join(V5.HERE, "bond-details7.html")
IMG = V5.IMG
esc, lead, sample = V4.esc, V4.lead, V4.sample


def header(d):
    stats = dict(d["stats"])
    cells = [("Returns", stats["Returns"]), ("Tenure", stats["Tenure"]),
             ("Credit Rating", stats["Credit rating"]), ("Security", "%sx" % B.HL_COVER)]
    items = []
    for (label, value), (f, w, h, l, t) in zip(cells, V5.STAT_ICONS):
        items.append('<div class="b7-stat"><span class="b7-stat__ico" aria-hidden="true">'
                     '<img src="%s%s" alt="" style="width:%dpx;height:%dpx;left:%dpx;top:%dpx"></span>'
                     '<dl><dt>%s</dt><dd>%s</dd></dl></div>' % (IMG, f, w, h, l, t, esc(label), esc(value)))
    # Payout: shown only in the phone layout's tile grid (the Figma's desktop row has four).
    payout = '<div class="b7-stat b7-stat--payout"><dl><dt>Payout</dt><dd>%s</dd></dl></div>' % esc(stats["Payout"])
    lit = round(d["sold_pct"] / 100 * 12)
    segs = "".join('<i%s></i>' % (' class="on"' if k < lit else "") for k in range(12))
    return f'''
<header class="b7-hc" aria-labelledby="b7-name">
  <div class="b7-hc__top">
    <div class="b7-hc__id">
      <span class="b7-hc__ring"><img src="{esc(d["logo"])}" alt="Mahaveer Finance India Limited logo" width="76" height="76"></span>
      <div class="b7-hc__names"><h1 id="b7-name">{esc(d["name"])}</h1><p>{esc(d["kind"])}</p></div>
    </div>
    <div class="b7-hc__acts">
      <span class="b7-pill b7-pill--sell"><i class="b7-dot" aria-hidden="true"></i>{esc(d["sell"])}</span>
      <button type="button" class="b7-hc__save" aria-label="Add to watchlist"><img src="{IMG}bookmark.svg" alt="" width="13.333" height="16.667"></button>
    </div>
  </div>
  <div class="b7-hc__stats">{'<span class="b7-hc__div" aria-hidden="true"></span>'.join(items)}{payout}</div>
  <div class="b7-hc__foot">
    <p class="b7-sold"><i class="b7-dot b7-sold__dot" aria-hidden="true"></i><span class="b7-sold__d">Sold {d["sold_pct"]}%</span><span class="b7-sold__m">{esc(d["sold"])}</span><span class="b7-sold__segs" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="{d["sold_pct"]}" aria-label="{esc(d["sold"])}">{segs}</span></p>
    <span class="b7-pill b7-pill--dash"><i class="b7-dot" aria-hidden="true"></i>{esc(d["form121"])}</span>
  </div>
</header>'''


def highlights(d):
    # The Figma leads with Strong Financials (clamped, with "more"), then Strong Backing.
    reasons = sorted(d["reasons"], key=lambda r: not r.startswith("Strong Financials"))
    pts = "".join('<li><img src="%sthumbs-up.svg" alt="" width="12.468" height="12.468"><p class="b7-clamp">%s</p></li>'
                  % (IMG, lead(r)) for r in reasons)
    (cov_t, cov_p), (sell_t, _) = d["confidence"][1], d["confidence"][0]
    b = d["backers"]
    logos = "".join('<img src="%s%s" alt="" width="%s" height="22.96"%s>' % (IMG, f, w, c)
                    for f, w, c in (("lender-1.png", "22.96", ""), ("lender-2.png", "21.28", ""),
                                    ("lender-4.png", "22.96", ' class="is-round"')))
    art = lambda f, left, w, x: ('<span class="b7-tile__art" aria-hidden="true"><span style="left:%dpx">'
                                 '<img src="%s%s" alt="" style="left:%s;width:%s"></span></span>' % (x, IMG, f, left, w))
    proof = [
        ('<span class="b7-proof__ico b7-proof__ico--money"><img src="%sproof-money.png" alt=""></span>' % IMG,
         d["repaid"][0], "Repaid"),
        ('<span class="b7-proof__ico b7-proof__ico--people"><img src="%sproof-people.png" alt=""></span>' % IMG,
         d["investors"][1], d["investors"][0]),
        ('<span class="b7-proof__ico b7-proof__ico--100"><span><img src="%sproof-100.png" alt=""></span></span>' % IMG,
         d["repayments"][1], d["repayments"][0]),
    ]
    proof_html = '<span class="b7-proof__div" aria-hidden="true"></span>'.join(
        '<div>%s<dl><dt>%s</dt><dd>%s</dd></dl></div>' % (ico, sample(v), esc(l)) for ico, v, l in proof)
    return f'''
<section class="b7-hl" aria-labelledby="b7-reasons">
  <h2 class="b7-eye" id="b7-reasons">{esc(d["reasons_title"])}</h2>
  <div class="b7-reasons">
    <div class="b7-reasons__list"><ul id="b7-rl">{pts}</ul>
      <button type="button" class="b7-more" aria-expanded="false" aria-controls="b7-rl">more</button></div>
    <div class="b7-backers"><h3>{esc("Key " + b[1])}</h3><div class="b7-backers__logos" role="img" aria-label="{esc(b[2])}">{logos}</div></div>
  </div>
  <h2 class="b7-eye">Key Highlights</h2>
  <div class="b7-tiles">
    <article class="b7-tile b7-tile--green">
      <div><p class="b7-tile__eye">{esc(d["kind"])}</p><h3>{esc(cov_t)}</h3><p class="b7-tile__p">Each ₹1 you invest is secured by ₹{B.HL_COVER} of assets.</p></div>
      {art("tile-shield.png", "-15.09%", "75%", 2)}
    </article>
    <article class="b7-tile b7-tile--peach">
      <div><p class="b7-tile__eye">Anytime Liquidity</p>
        <h3 class="b7-tile__fact"><i class="b7-dot b7-dot--lg" aria-hidden="true"></i>{esc(sell_t)}</h3>
        <h3 class="b7-tile__fact"><i class="b7-dot b7-dot--lg" aria-hidden="true"></i>{esc(d["form121"])}</h3></div>
      {art("tile-clock.png", "-14.48%", "75.19%", 6)}
    </article>
  </div>
  <div class="b7-proof">
    <p class="b7-proof__t">{esc(d["name"])} on GoldenPi</p>
    <div class="b7-proof__row">{proof_html}</div>
  </div>
</section>'''


def cashflow_block(m, tot, chip):
    """One cashflow block (the page's card or the Timeline modal): the TDS note
    goes, Principal + Interest leave the receivable card and become the table
    header's totals (on phones, a two-figure strip). Download stays where it was."""
    sums = ('<dl class="b7-cf-sums"><div><dt>Interest</dt><dd>%s</dd></div>'
            '<div><dt>Principal</dt><dd>%s</dd></div></dl>' % (tot["Interest"], tot["Principal"]))
    steps = [
        (re.search(r'<p class="bond-cashflow-tds-disclaimer m-0">.*?</p>', m).group(0), ""),
        (re.search(r'<div class="rs">.*?</span></span></div>', m, re.S).group(0), ""),
        (re.search(r'<div class="rs rs--mobile">.*?</span></span></div>', m, re.S).group(0), sums),
        ('<th class="bond-cashflow-th px-2 py-3 text-left">Date</th>',
         '<th class="bond-cashflow-th px-2 py-3 text-left">Date</th>'),
        ('<th class="bond-cashflow-th px-2 py-3 text-left">Interest</th>',
         '<th class="bond-cashflow-th px-2 py-3 text-left">Interest<span class="b7-cf-sum">%s</span></th>' % tot["Interest"]),
        ('<th class="bond-cashflow-th px-2 py-3 text-left">Principal</th>',
         '<th class="bond-cashflow-th px-2 py-3 text-left">Principal<span class="b7-cf-sum">%s</span></th>' % tot["Principal"]),
    ]
    for old, new in steps:
        if m.count(old) != 1:
            raise SystemExit("bond-details7 cashflow: expected one of %r" % old[:60])
        m = m.replace(old, new)
    return m


def cashflow_modal(h, d):
    """bond-details7's cashflow, on the page and in the Timeline modal: a
    "Form 121 available to save TDS" chip beside the heading, totals in the
    table header. The other bond pages keep theirs."""
    chip = '<span class="b7-cf-chip"><i class="b7-dot" aria-hidden="true"></i>Form 121 available to save TDS</span>'
    tot = dict(re.findall(r'<span class="rs__label">(\w+)</span><span class="rs__value[^"]*">(₹ [\d,]+\.\d\d)</span>', h)[:2])
    if set(tot) != {"Principal", "Interest"}:
        raise SystemExit("bond-details7 cashflow: receivable split not found")
    # Page card: from its heading to the modal.
    i = h.index('<h2 class="sr-only">Cashflow</h2>')
    j = h.index('<div id="cashflow-modal"')
    page = cashflow_block(h[i:j], tot, chip)
    title = '<span class="gp-expand__title">Cashflow</span>'
    if page.count(title) != 1:
        raise SystemExit("bond-details7 cashflow: page title not found")
    page = page.replace(title, '<span class="b7-cf-sumrow">%s%s</span>' % (title, chip))
    # Starts open as a glimpse: the summary and the first years, fading out.
    m_btn = re.search(r'<button type="button" class="gp-expand__summary[^"]*" id="[^"]+" aria-expanded="false" aria-controls="([^"]+)">', page)
    body = '<div hidden id="%s"' % m_btn.group(1)
    if page.count(body) != 1:
        raise SystemExit("bond-details7 cashflow: page body not found")
    page = page.replace(m_btn.group(0), m_btn.group(0).replace('aria-expanded="false"', 'aria-expanded="true"'), 1)
    page = page.replace(body, '<div id="%s"' % m_btn.group(1), 1)
    page = page.replace('<div id="%s"' % m_btn.group(1), '<div id="%s" data-b7-peek' % m_btn.group(1), 1)
    h = h[:i] + page + h[j:]
    k = h.rfind('<div class="gp-expand ', 0, i + len('<h2 class="sr-only">Cashflow</h2>'))
    h = h[:k] + h[k:].replace('class="gp-expand ', 'class="gp-expand is-open b7-peek ', 1)
    # Modal.
    i = h.index('<div id="cashflow-modal"')
    j = h.index("<script", i)
    m = cashflow_block(h[i:j], tot, chip)
    old = '<h2 class="bond-cashflow-timeline-modal__title">Cashflow Timeline</h2>'
    if m.count(old) != 1:
        raise SystemExit("bond-details7 cashflow: modal title not found")
    m = m.replace(old, '<div class="b7-cf-head"><h2 class="b7-cf-title">Cashflow Timeline</h2>%s</div>' % chip)
    return h[:i] + m + h[j:]


STYLE = """<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
<style>
/* bond-details7: Figma 37:222's hero (37:417) and "Reasons to invest" (37:548),
   values as designed; only the width follows bond-details5's column. */
.b7-hc, .b7-hl { font-family: Inter, satoshi, system-ui, sans-serif; }
.b7-dot { flex: none; width: 5.25px; height: 5.25px; border-radius: 9999px; background: #22c55e; box-shadow: 0 0 8px #22c55e; }
.b7-dot--lg { width: 8px; height: 8px; }

/* Hero card (37:417): 246px tall at 629px, content inset 20px. */
.b7-hc { position: relative; overflow: hidden; display: grid; gap: 4px; padding: 20px 20px 26px; border-radius: 20px; color: #fff;
  background: radial-gradient(889.54px 347.9px at 100% 100%, #27272a 0%, #18181b 40%, #0c0c0e 70%, #060607 85%, #000 100%); }
.b7-hc__top { display: flex; align-items: flex-start; justify-content: space-between; gap: 20px; }
.b7-hc__id { display: flex; align-items: center; gap: 24px; min-width: 0; }
.b7-hc__ring { flex: none; display: grid; place-items: center; width: 79.06px; height: 79.06px; border: 2px solid #edc967; border-radius: 500px; }
.b7-hc__ring img { width: 75.63px; height: 75.63px; margin: -2px; border-radius: 50%; object-fit: cover; background: rgba(0, 0, 0, .2); }
.b7-hc__names { display: grid; gap: 8px; min-width: 0; }
.b7-hc h1 { margin: 0; font-size: 28px; line-height: 30.938px; font-weight: 600; color: rgba(255, 255, 255, .9); }
.b7-hc__names p { margin: 0; font-size: 14px; line-height: 16px; font-weight: 500; color: rgba(255, 255, 255, .5); text-transform: capitalize; }
.b7-hc__acts { flex: none; display: flex; align-items: center; gap: 20px; }
.b7-pill { display: inline-flex; align-items: center; justify-content: center; gap: 10px; padding: 8px 11px; border-radius: 45px; white-space: nowrap;
  font-size: 14px; font-weight: 500; text-transform: capitalize; }
.b7-pill--sell { height: 40px; min-width: 128px; line-height: 16px; color: #edc967; border: 1px solid rgba(255, 255, 255, .1); }
.b7-pill--dash { min-width: 164px; line-height: 11.602px; color: #fff; border: .5px dashed #fdf2d0; }
.b7-hc__save { position: relative; flex: none; width: 40px; height: 40px; padding: 0; border-radius: 8615px; cursor: pointer;
  background: rgba(0, 0, 0, .4); border: .862px solid rgba(255, 255, 255, .1); -webkit-backdrop-filter: blur(10.339px); backdrop-filter: blur(10.339px); }
.b7-hc__save img { position: absolute; left: 50%; top: 50%; width: 13.333px; height: 16.667px; transform: translate(-50%, -50%); }
.b7-hc__stats { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 20px; min-height: 90px; padding-right: 80px; }
.b7-hc .b7-stat--payout, .b7-sold__m, .b7-sold__dot { display: none; }
.b7-hc__div { width: 1px; height: 25px; background: rgba(219, 207, 178, .25); opacity: .54; }
.b7-stat { display: flex; align-items: center; gap: 8px; }
.b7-stat__ico { position: relative; flex: none; width: 36px; height: 36px; overflow: hidden; border-radius: 8px; }
.b7-stat__ico img { position: absolute; max-width: none; object-fit: cover; }
.b7-stat dl { margin: 0; display: grid; gap: 8px; }
.b7-stat dt { font-size: 14px; line-height: 13.5px; font-weight: 500; color: rgba(255, 255, 255, .6); text-transform: capitalize; white-space: nowrap; }
.b7-stat dd { margin: 0; font-size: 16px; line-height: normal; font-weight: 600; color: rgba(255, 255, 255, .9); white-space: nowrap; }
.b7-hc__foot { display: flex; align-items: center; justify-content: space-between; gap: 16px; }
.b7-sold { margin: 0; display: flex; align-items: center; gap: 10px; font-family: satoshi, system-ui, sans-serif;
  font-size: 14px; line-height: 12px; font-weight: 700; letter-spacing: .5px; text-transform: uppercase; color: #ececec; }
.b7-sold__segs { display: flex; gap: 2px; }
.b7-sold__segs i { width: 6.91px; height: 6px; border-radius: 2px; opacity: .8; border: 1px solid rgba(246, 213, 122, .01);
  background: linear-gradient(139deg, rgba(253, 242, 208, .5) 25%, rgba(230, 179, 37, .5) 78.365%, rgba(179, 134, 0, .5) 100%); }
.b7-sold__segs i.on { background: linear-gradient(139deg, #fdf2d0 25%, #e6b325 78.365%, #b38600 100%); }

/* Reasons to invest card (37:550). */
.b7-hl { display: grid; gap: 16px; padding: 20px; border-radius: 24px; background: #fff; overflow: hidden; }
.b7-eye { margin: 0; font-size: 14px; line-height: 1.5; font-weight: 600; letter-spacing: .7px; text-transform: uppercase; color: #a67c00; }
.b7-reasons { display: flex; align-items: flex-start; justify-content: space-between; gap: 32px; padding: 28px 24px;
  border-radius: 20px; background: #fff7e8; border-bottom: 1px solid #fff0d4; }
.b7-reasons__list { flex: 1; min-width: 0; max-width: 460px; display: grid; justify-items: start; gap: 10px; }
.b7-reasons ul { margin: 0; padding: 0; list-style: none; display: grid; gap: 14px; overflow: hidden; transition: height .35s cubic-bezier(.16, 1, .3, 1); }
@media (prefers-reduced-motion: reduce) { .b7-reasons ul { transition: none; } }
.b7-more { margin-left: 25px; }
.b7-reasons li { display: flex; align-items: flex-start; gap: 4px; }
.b7-reasons li > img { flex: none; width: 12.468px; height: 12.468px; margin: 4.99px 4.27px 0 4.27px; }
.b7-reasons li p { margin: 0; font-size: 14px; line-height: 1.5; font-weight: 400; color: #252525; }
.b7-reasons li b { font-weight: 700; }
.b7-clamp { display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 2; overflow: hidden; }
.is-open .b7-clamp { display: block; }
.b7-more { padding: 0; border: 0; background: none; cursor: pointer; font: inherit; font-size: 14px; line-height: 1.5; color: #252525;
  text-decoration: underline; text-underline-position: from-font; }
.b7-backers { flex: none; display: grid; align-content: center; gap: 20px; width: 166px; min-height: 153px; padding: 30px 20px;
  border-radius: 20px; background: #fff; border-bottom: 1px solid #fff; }
.b7-backers h3 { margin: 0; max-width: 130px; font-size: 13px; line-height: 1.5; font-weight: 600; color: #7a571f; text-transform: capitalize; }
.b7-backers__logos { display: flex; align-items: center; gap: 15px; height: 24px; }
.b7-backers__logos img { height: 22.96px; object-fit: cover; }
.b7-backers__logos img.is-round { border-radius: 113px; }
.b7-tiles { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }
.b7-tile { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; min-height: 169px; padding: 30px 20px;
  border-radius: 20px; overflow: hidden; }
.b7-tile--green { background: #e8f7ee; border-bottom: 1px solid #e1f2e8; }
.b7-tile--peach { background: #fff1e8; border-bottom: 1px solid #f7e6db; }
.b7-tile > div { display: grid; align-content: start; gap: 16px; min-width: 0; }
.b7-tile__eye { margin: 0; font-size: 13px; line-height: 1.5; font-weight: 600; color: #7a571f; text-transform: capitalize; white-space: nowrap; }
.b7-tile h3 { margin: 0; font-size: 20px; line-height: 1.2; font-weight: 600; color: #171f29; }
.b7-tile--green h3 { margin-bottom: -12px; }
.b7-tile__p { margin: 0; font-size: 14px; line-height: 1.5; color: #252525; }
.b7-tile__fact { display: flex; align-items: center; gap: 10px; white-space: nowrap; }
.b7-tile__art { position: relative; flex: none; width: 81px; height: 87px; }
.b7-tile__art > span { position: absolute; top: -1px; width: 150px; height: 75px; overflow: hidden; }
.b7-tile__art img { position: absolute; top: 0; height: 100%; max-width: none; }
.b7-proof { position: relative; display: grid; justify-items: center; align-content: center; gap: 16px; min-height: 147px; padding: 8px;
  border-radius: 20px; background: rgba(245, 243, 255, .7); overflow: hidden; }
.b7-proof__t { margin: 0; display: flex; align-items: center; gap: 8px; font-size: 13px; line-height: 1.5; font-weight: 600; color: #7a571f; text-transform: capitalize; }
.b7-proof__t::before, .b7-proof__t::after { content: ""; width: 24px; height: 1px; opacity: .7; background: linear-gradient(90deg, rgba(179, 135, 40, 0), #b38728); }
.b7-proof__t::after { transform: scaleX(-1); }
.b7-proof__row { display: flex; align-items: flex-start; justify-content: center; }
.b7-proof__row > .b7-proof__div { align-self: center; }
.b7-proof__row > div { display: grid; justify-items: center; gap: 4px; width: 174px; text-align: center; }
.b7-proof__div { width: 1px; height: 50px; background: rgba(231, 227, 217, .6); opacity: .54; }
.b7-proof__ico { position: relative; display: block; height: 40px; overflow: hidden; }
.b7-proof__ico img { position: absolute; max-width: none; }
.b7-proof__ico--money { width: 40px; }
.b7-proof__ico--money img { left: -11.25%; top: -10%; width: 120%; height: 120%; }
.b7-proof__ico--people { width: 51px; height: 40px; overflow: visible; }
.b7-proof__ico--people img { left: 1px; top: -1.85px; width: 49px; height: 49px; }
.b7-proof__ico--100 { width: 40px; overflow: visible; }
.b7-proof__ico--100 > span { position: absolute; left: -11.5px; top: -1px; width: 69px; height: 41px; overflow: hidden; }
.b7-proof__ico--100 img { left: -5.8%; top: -39.02%; width: 105.8%; height: 178.05%; }
.b7-proof dl { margin: 0; }
.b7-proof dt { font-size: 16px; line-height: 27.5px; font-weight: 500; color: #322811; }
.b7-proof dt .b4-sample { border: 0; text-decoration: none; }
.b7-proof dd { margin: 0; font-size: 14px; line-height: 1.5; color: #252525; }

/* Cashflow, page card and Timeline modal (bond-details7). */
.b7-cf-head { display: flex; flex-wrap: wrap; align-items: center; gap: 10px 14px; margin-bottom: 18px; padding-right: 44px; }
.b7-cf-title { margin: 0; font-size: 20px; line-height: 28px; font-weight: 700; color: #322811; }
.b7-cf-sumrow { display: flex; flex: 1; flex-wrap: wrap; align-items: center; gap: 8px 12px; margin-right: 12px; }
.b7-cf-head .b7-cf-chip, .b7-cf-sumrow .b7-cf-chip { margin-left: auto; }
.b7-cf-chip { display: inline-flex; align-items: center; gap: 7px; padding: 6px 12px; border-radius: 999px; white-space: nowrap;
  font-size: 12px; line-height: 16px; font-weight: 600; color: #0b7a3e; background: #f0faf4; border: 0; }
.bond-cashflow-receivable-panel { display: flex; align-items: center; justify-content: center; }
.bond-cashflow-th { vertical-align: bottom; }
/* Quiet header: small muted labels, totals as the one emphasis, air above and below
   (beta's table rules are specific, so these hold with !important). */
.bond-details-cashflow .bond-cashflow-summary-grid { margin-bottom: 20px !important; }
.bond-details-cashflow .bond-cashflow-th { padding-top: 0 !important; padding-bottom: 14px !important; vertical-align: top !important;
  font-size: 12px !important; line-height: 16px !important; font-weight: 600 !important; letter-spacing: .06em !important;
  text-transform: uppercase !important; color: #8a8378 !important; }
.bond-details-cashflow .bond-cashflow-table-head tr { border-bottom: 1px solid #efe9dc; }
.bond-details-cashflow .bond-cashflow-table-head + tbody > tr:first-child > td,
#cashflow-modal .bond-cashflow-table-body-scroll { padding-top: 14px !important; }
.b7-cf-sum { display: block; margin-top: 6px; font-size: 16px; line-height: 22px; font-weight: 600; letter-spacing: 0; text-transform: none; color: #322811; font-variant-numeric: tabular-nums; }
.b7-cf-sum--label { font-weight: 500; color: #322811; }
.b7-cf-sum.is-gain, .b7-cf-sums .is-gain { color: #0b8a43; }
.b7-cf-sums { display: none; margin: 0; }


@media (max-width: 767px) {
  .b7-cf-head { margin: 0 0 14px; padding: 18px 56px 0 16px; }
  .b7-cf-title { font-size: 18px; line-height: 24px; }
  .b7-cf-chip { font-size: 12px; padding: 4px 10px; }
  .b7-cf-sums { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; padding: 12px 16px 0; }
  .b7-cf-sums dt { font-size: 12px; color: #8a8378; }
  .b7-cf-sums dd { margin: 2px 0 0; font-size: 16px; font-weight: 700; color: #322811; font-variant-numeric: tabular-nums; }
}

@media (max-width: 767px) {
  /* Phones: a centred fold. Logo in the gold ring, name, type, sold bar, then
     the facts as tiles (three, then two), pills last. */
  .b7-hc { display: flex; flex-wrap: wrap; justify-content: center; gap: 0 10px; padding: 26px 16px 20px; text-align: center; }
  .b7-hc__top, .b7-hc__acts, .b7-hc__foot { display: contents; }
  .b7-hc__id { order: 1; flex-basis: 100%; flex-direction: column; gap: 14px; }
  .b7-hc__ring { width: 104px; height: 104px; border-width: 2px; }
  .b7-hc__ring img { width: 100px; height: 100px; }
  .b7-hc__names { justify-items: center; gap: 8px; }
  .b7-hc h1 { font-size: 26px; line-height: 30px; font-weight: 700; letter-spacing: .01em; text-transform: uppercase; }
  .b7-hc__names p { font-size: 13px; letter-spacing: .14em; text-transform: uppercase; color: rgba(255, 255, 255, .55); }
  .b7-sold { order: 2; flex-basis: 100%; flex-direction: column; gap: 10px; margin-top: 14px; font-size: 13px; letter-spacing: .08em; }
  .b7-sold__d { display: none; }
  .b7-sold__m { display: inline; }
  .b7-sold > .b7-dot { display: none; }
  .b7-sold__m::before { content: ""; display: inline-block; width: 9px; height: 9px; margin-right: 8px; border-radius: 50%; background: #22c55e; box-shadow: 0 0 8px #22c55e; vertical-align: 1px; }
  .b7-hc__stats { order: 3; flex-basis: 100%; display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 10px; min-height: 0; margin: 18px 0 16px; padding-right: 0; }
  .b7-hc__div { display: none; }
  .b7-stat { grid-column: span 2; justify-content: center; padding: 14px 6px; border-radius: 16px;
    background: rgba(255, 255, 255, .06); border: 1px solid rgba(255, 255, 255, .08); }
  .b7-stat:nth-of-type(1) { order: 1; } .b7-stat:nth-of-type(2) { order: 2; } .b7-hc .b7-stat--payout { order: 3; display: flex; }
  .b7-stat:nth-of-type(3) { order: 4; grid-column: span 3; } .b7-stat:nth-of-type(4) { order: 5; grid-column: span 3; }
  .b7-stat__ico { display: none; }
  .b7-stat dl { justify-items: center; gap: 6px; }
  .b7-stat dt { font-size: 13px; line-height: 16px; }
  .b7-stat dd { font-size: 16px; line-height: 20px; }
  .b7-pill--sell { order: 4; height: 34px; min-width: 0; }
  .b7-pill--dash { order: 5; min-width: 0; padding: 8px 12px; }
  .b7-hc__save { display: none; }
  .b7-hl { padding: 16px; }
  .b7-reasons { flex-direction: column; padding: 20px 16px; }
  .b7-backers { width: 100%; min-height: 0; padding: 20px; }
  .b7-tiles { grid-template-columns: minmax(0, 1fr); }
  .b7-tile { padding: 24px 20px; }
  .b7-proof__row { display: grid; grid-template-columns: minmax(0, 1fr) 1px minmax(0, 1fr) 1px minmax(0, 1fr); width: 100%; align-items: start; }
  .b7-proof__row > div { width: auto; min-width: 0; padding: 0 4px; }
  .b7-proof__row > .b7-proof__div { height: 44px; align-self: end; margin-bottom: 4px; }
  .b7-proof__row dt { font-size: 14px; line-height: 20px; margin-top: 4px; }
  .b7-proof__row dd { font-size: 12px; line-height: 16px; }
  .b7-proof__ico { transform: scale(.85); }
}
/* Phones: one gutter, lighter nesting, so the highlights read edge to edge. */
@media (max-width: 639px) {
  :root { --issuer-gutter: 12px !important; }
  .b7-hl { padding: 16px 12px; gap: 12px; border-radius: 20px; }
  .b7-reasons { padding: 16px 14px; gap: 14px; }
  .b7-reasons li > img { margin-left: 0; }
  .b7-backers { padding: 14px 16px; gap: 12px; display: flex; align-items: center; justify-content: space-between; }
  .b7-backers h3 { max-width: 110px; }
  .b7-tile { padding: 18px 16px; min-height: 0; }
  .b7-proof { padding: 14px 6px; }
}

/* Below 1024px beta switches the cashflow to its own mobile layout; bond-details7
   keeps the desktop one (summary cards, Date / Interest / Principal header with
   totals, three-column years) at every width. */
@media (max-width: 1023px) {
  .bond-details-cashflow .bond-cashflow-mobile-summary-wrap,
  .bond-details-cashflow .bond-cashflow-year-header-mobile,
  .bond-details-cashflow .bond-cashflow-mobile-payout-header,
  .bond-details-cashflow .bond-cashflow-mobile-table-download,
  .b7-cf-sums { display: none !important; }
  .bond-details-cashflow .bond-cashflow-summary-grid { display: grid !important; grid-template-columns: minmax(0, 1fr); gap: 12px; }
  .bond-details-cashflow .bond-cashflow-content .bond-cashflow-table-head { display: table-header-group !important; }
  .bond-details-cashflow .bond-cashflow-year-header-desktop { display: table !important; width: 100%; }
  .bond-details-cashflow .bond-cashflow-content .bond-cashflow-footer-download { display: inline-flex !important; }
  .bond-details-cashflow .bond-cashflow-th, .bond-details-cashflow .bond-cashflow-year-amount,
  .bond-details-cashflow .bond-cashflow-expanded-amount { padding-left: 8px !important; }
  .bond-details-cashflow .bond-cashflow-year-date { padding-left: 8px !important; }
  .bond-details-cashflow .bond-cashflow-year-date > span { gap: 10px !important; }
  .bond-details-cashflow .bond-cashflow-expanded-date-td { padding-left: 34px !important; }
  .bond-details-cashflow .bond-cashflow-year-amount, .bond-details-cashflow .bond-cashflow-receivable-amount-line { font-size: 14px !important; }
  .b7-cf-sum { font-size: 15px; }
  /* One column grid for every table in the block, so header, years and payouts line up. */
  .bond-details-cashflow table { table-layout: fixed !important; width: 100% !important; }
  .bond-details-cashflow col.bond-cashflow-col-date { width: 30% !important; }
  .bond-details-cashflow col.bond-cashflow-col-receivable, .bond-details-cashflow col.bond-cashflow-col-net { width: 35% !important; }
  .bond-details-cashflow .bond-cashflow-th { vertical-align: top !important; }
  .bond-details-cashflow .bond-cashflow-year-amount, .bond-details-cashflow .bond-cashflow-receivable-amount-line,
  .b7-cf-sum { white-space: nowrap; }
  .bond-details-cashflow .bond-cashflow-expanded-date-td { padding-left: 30px !important; }
  .bond-details-cashflow .bond-cashflow-timeline, .bond-details-cashflow .bond-cashflow-timeline-payouts { padding-left: 0 !important; }
  .bond-details-cashflow .bond-cashflow-timeline-line { left: 14px !important; }
  /* Summary cards at their desktop type scale. */
  .bond-details-cashflow .bond-cashflow-investment-panel, .bond-details-cashflow .bond-cashflow-receivable-panel { padding: 16px !important; }
  .bond-details-cashflow .bond-cashflow-summary-label { font-size: 13px !important; }
  .bond-details-cashflow .bond-cashflow-investment-amount, .bond-details-cashflow .bond-cashflow-receivable-amount { font-size: 20px !important; line-height: 28px !important; }
  /* Header chip: next to the title when it fits, else its own line from the left. */
  .b7-cf-chip { font-size: 11px; padding: 5px 10px; }
  .b7-cf-head .b7-cf-chip { margin-left: 0; }
  #cashflow-modal .bond-cashflow-table-body-scroll { padding-top: 6px !important; }
  #cashflow-modal .bond-cashflow-footer-meta { padding: 12px 8px 0; }
  .bond-details-cashflow .bond-cashflow-th { padding-bottom: 10px !important; }
  .bond-details-cashflow .bond-cashflow-table-head + tbody > tr:first-child > td,
  #cashflow-modal .bond-cashflow-table-body-scroll { padding-top: 8px !important; }
  .bond-details-cashflow .bond-cashflow-summary-grid { margin-bottom: 16px !important; }
}
/* Rounded on every corner in both states. */
.b7-peek.gp-expand--card { border-radius: 24px !important; overflow: hidden; }
.b7-peek [data-b7-peek] { border-radius: 0 0 24px 24px; }
/* Page cashflow: opens as a glimpse that fades out; a click shows it all.
   The Timeline pop-up is always complete. */
.b7-peek [data-b7-peek] { position: relative; isolation: isolate; max-height: 182px; overflow: hidden; cursor: pointer;
  transition: max-height .5s cubic-bezier(.16, 1, .3, 1); }
.b7-peek [data-b7-peek]::after { content: ""; position: absolute; left: 0; right: 0; bottom: 0; z-index: 20; height: 110px; pointer-events: none;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, .85) 45%, #fff 80%); }
.b7-peek__more { position: absolute; left: 50%; bottom: 12px; z-index: 21; transform: translateX(-50%); display: inline-flex; align-items: center; gap: 6px;
  height: 36px; padding: 0 16px; border-radius: 999px; cursor: pointer; white-space: nowrap; font: inherit; font-size: 14px; font-weight: 700;
  color: #8a6520; background: #fff; border: 1px solid rgba(138, 101, 32, .3); box-shadow: 0 8px 20px -10px rgba(80, 60, 10, .35); }
.b7-peek__more:hover { border-color: #8a6520; }
.b7-peek.is-full [data-b7-peek] { max-height: 3000px; cursor: auto; }
.b7-peek.is-full [data-b7-peek]::after, .b7-peek.is-full .b7-peek__more { display: none; }
@media (max-width: 767px) { .b7-peek [data-b7-peek] { max-height: 270px; } }
@media (prefers-reduced-motion: reduce) { .b7-peek [data-b7-peek] { transition: none; } }
/* App band (bond-details7). */
.a3 { position: relative; overflow: hidden; padding: 26px 28px !important; gap: 28px !important;
  background: radial-gradient(520px 260px at 0% 0%, #fdf3d4 0%, rgba(253, 243, 212, 0) 70%), #fff !important; }
.a3__title { font-size: 22px !important; line-height: 30px !important; letter-spacing: -.015em; }
.a3__sub { margin-top: 6px !important; max-width: 40ch !important; font-size: 15px !important; }
.b7-app__hint { display: inline-flex; align-items: center; gap: 8px; margin: 18px 0 0; font-size: 12px; font-weight: 700;
  letter-spacing: .08em; text-transform: uppercase; color: #8a6520; }
.b7-app__hint::after { content: ""; width: 28px; height: 1px; background: linear-gradient(90deg, #b38728, rgba(179, 135, 40, 0)); }
.b7-app__qr { flex: none; display: grid; place-items: center; padding: 12px; border-radius: 18px; background: #fff;
  border: 1px solid #e8d9a8; box-shadow: 0 12px 28px -14px rgba(166, 124, 0, .45); }
.b7-app__qr img { display: block; width: 104px; height: 104px; }
@media (max-width: 639px) {
  .a3 { padding: 20px 16px !important; gap: 16px !important; }
  .a3__title { font-size: 18px !important; line-height: 24px !important; }
  .a3__sub { font-size: 13px !important; }
  .b7-app__hint { display: none; }
  .b7-app__qr { padding: 8px; border-radius: 14px; }
  .b7-app__qr img { width: 76px; height: 76px; }
}
/* "1 Unit" in the Returns Calculator stepper. */
.bond-cashflow-sidebar__stepper label { gap: 6px; }
.bond-cashflow-sidebar__stepper label input { width: 3ch !important; max-width: none !important; text-align: right !important; }
.bond-cashflow-sidebar__stepper label input, .b7-unit { font-family: satoshi, system-ui, sans-serif !important;
  font-size: 22px !important; line-height: 32px !important; font-weight: 700 !important; color: #322811 !important; }
/* The number leads; "Unit" is its quieter label, on the same baseline. */
.bond-cashflow-sidebar__stepper label { align-items: baseline !important; }
.b7-unit { font-size: 16px !important; font-weight: 500 !important; color: #6b6457 !important; }
</style>
"""

SCRIPT = """<script>
// Page cashflow glimpse: a click on the faded card, its button or its heading
// opens it in full; the heading then folds it back to the glimpse.
(function () {
  var card = document.querySelector('.b7-peek');
  if (!card) return;
  var body = card.querySelector('[data-b7-peek]');
  var sum = card.querySelector('.gp-expand__summary');
  var btn = document.createElement('button');
  btn.type = 'button'; btn.className = 'b7-peek__more'; btn.textContent = 'View Full Cashflow';
  body.appendChild(btn);
  function full(on) {
    card.classList.toggle('is-full', on);
    sum.setAttribute('aria-expanded', 'true');
  }
  card.addEventListener('click', function (e) {
    if (e.target.closest('.gp-expand__summary')) {
      e.stopImmediatePropagation();
      full(!card.classList.contains('is-full'));
      return;
    }
    if (!card.classList.contains('is-full') && e.target.closest('[data-b7-peek]')) {
      e.stopImmediatePropagation(); e.preventDefault();
      full(true);
    }
  }, true);
})();
// Cashflow years: the open-row styling follows the toggle (the capture
// marks 2026 open and nothing ever cleared it, so it kept its padding).
document.addEventListener('click', function (e) {
  var t = e.target.closest('.bond-cashflow-year-header-in-panel--toggle, .bond-cashflow-year-header-mobile');
  if (!t) return;
  var panel = t.closest('.bond-cashflow-year-expanded-panel');
  if (panel) panel.classList.toggle('bond-cashflow-year-expanded-panel--open', t.getAttribute('aria-expanded') === 'true');
});
// bond-details7: "more" grows the reasons panel to the full text; the
// panel gets taller, the lenders card and layout around it stay put.
document.querySelectorAll('.b7-more').forEach(function (b) {
  var list = document.getElementById(b.getAttribute('aria-controls'));
  var timer;
  b.addEventListener('click', function () {
    var from = list.offsetHeight;
    var open = !list.classList.contains('is-open');
    list.classList.toggle('is-open', open);
    var to = open ? list.scrollHeight : list.offsetHeight;
    clearTimeout(timer);
    list.style.height = from + 'px';
    list.offsetHeight; // commit the start height before animating
    list.style.height = to + 'px';
    timer = setTimeout(function () { list.style.height = ''; }, 400);
    b.setAttribute('aria-expanded', String(open));
    b.textContent = open ? 'less' : 'more';
  });
});
</script>
"""


def main():
    h = open(V4.SRC, encoding="utf-8").read()
    d = V4.read(h)
    # Start from exactly what bond-details5 is, then swap its two Figma blocks.
    h = V5.hybrid(h, d)
    for old in (V5.header(d), V5.highlights(d) + V5.highlights2(d)):
        new = header(d) if old.lstrip().startswith("<header") else highlights(d)
        tag = '<div class="b4 b5 b5-embed">%s</div>' % old
        if tag not in h:
            raise SystemExit("bond-details7: bond-details5 block not found")
        h = h.replace(tag, '<div class="b4 b5 b5-embed">%s</div>' % new, 1)
    h = h.replace("<!-- Generated by pages/_bond_v5.py: bond-details3.html with the Figma's header card and "
                  "highlights (HRSMFFccdLgqf1YwD7oyc9 29:1409); do not edit. -->",
                  "<!-- Generated by pages/_bond_v7.py: bond-details5 with the header card and highlights "
                  "of Figma HRSMFFccdLgqf1YwD7oyc9 37:222; do not edit. -->", 1)
    h = cashflow_modal(h, d)
    # Returns Calculator stepper reads "1 Unit" (the number stays the editable input).
    h, n = re.subn(r'(bond-cashflow-sidebar__stepper">(?:(?!</label>).)*?<input )([^>]*aria-label="Units"[^>]*>)(</label>)',
                   r'\1\2<span class="b7-unit">Unit</span>\3', h, flags=re.S)
    if n != 2:
        raise SystemExit("bond-details7: expected 2 calculator steppers, found %d" % n)
    # Company Information and Documents groups start collapsed.
    for title in ("About the Issuer", "Strength / Weaknesses", "Company Financials"):
        h = B.close(h, title)
    # App band: one line of copy and the code alone (the image's own "Invest
    # Smarter / Download the App" lettering is cropped off in app-qr.svg).
    old = re.search(r'<div class="a3__text">.*?<img class="a3__qr"[^>]*>', h, re.S)
    if not old:
        raise SystemExit("bond-details7: app band not found")
    h = h.replace(old.group(0),
        '<div class="a3__text"><h2 id="a3-h" class="a3__title">The Golden Experience of Investing</h2>'
        '<p class="a3__sub">Download the GoldenPi app and invest on the go.</p>'
        '<p class="b7-app__hint">Scan with your phone</p></div>'
        '<span class="b7-app__qr"><img src="%sapp-qr.svg" alt="QR code to download the GoldenPi app" width="113" height="113" loading="lazy"></span>'
        % IMG, 1)
    for old, new in (('class="ci__title">Documents and More Details<', 'class="ci__title">Documents and More<'),
                     ('<h3 class="sr-only">More Bond Details<', '<h3 class="sr-only">Other Bond Details<'),
                     ('<span class="gp-expand__title">More Bond Details<', '<span class="gp-expand__title">Other Bond Details<')):
        if h.count(old) != 1:
            raise SystemExit("bond-details7: heading not found: " + old)
        h = h.replace(old, new)
    h = h.replace("</head>", STYLE + "</head>", 1).replace("</body>", SCRIPT + "</body>", 1)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(h)
    print("%s  %d bytes" % (os.path.relpath(OUT, os.path.dirname(V5.HERE)), len(h)))


if __name__ == "__main__":
    main()
