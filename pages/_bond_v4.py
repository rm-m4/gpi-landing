#!/usr/bin/env python3
"""bond-details4.html: the Mahaveer bond page, redesigned from scratch.

bond-details3 is beta's page with passes on top. This one keeps only its
content and rebuilds the main column in its own markup: a light header
with the four headline figures, a sticky returns calculator, an in-page
section bar, the cashflow as one disclosure per year, the four financial
series as small multiples instead of tabs, and the bond's details as one
deduplicated list. Header and footer are bond-details3's.

Every figure and sentence is read from the generated bond-details3.html
(so the merges and splits already made there carry over) or, for the
financial series, from beta's own data payload. Nothing is typed in here.
The highlights' sample figures stay marked as sample data, as in v3.

    python3 pages/_bond_beta.py && python3 pages/_bond_v4.py
"""
import html as H
import os
import re

import _bond_beta as B

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "bond-details3.html")
OUT = os.path.join(HERE, "bond-details4.html")
esc = H.escape
ICONS = ('<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/regular/style.css">'
         '<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/fill/style.css">')


# ------------------------------------------------------------- reading v3
class Text:
    """bond-details3's main column as a list of text runs, in order."""

    def __init__(self, main):
        main = re.sub(r"<(script|style|svg)\b.*?</\1>", "", main, flags=re.S)
        self.t = [s for s in (H.unescape(x).strip() for x in re.split(r"<[^>]+>", main)) if s]

    def at(self, label, start=0):
        try:
            return self.t.index(label, start)
        except ValueError:
            raise SystemExit("bond-details4: %r not found in bond-details3" % label)

    def after(self, label, start=0):
        return self.t[self.at(label, start) + 1]

    def pairs(self, start, stop):
        """[(label, value)] for the runs in [start, stop)."""
        run = self.t[start:stop]
        if len(run) % 2:
            raise SystemExit("bond-details4: odd label/value run at %d" % start)
        return list(zip(run[0::2], run[1::2]))


def money(s):
    return float(s.replace("₹", "").replace(",", "").strip())


def read(h):
    main = h[h.index("<main"):h.index("</main>")]
    T = Text(main)
    t = T.t
    d = {}

    # Header
    d["logo"] = re.search(r'<img src="([^"]+)" alt="Mahaveer Finance India Limited logo"', main).group(1)
    d["crumbs"] = re.findall(r'<a class="[^"]*" href="([^"]+)">([^<]+)</a>', main[:main.index("</nav>")])
    d["crumb_here"] = t[2]
    d["name"], d["kind"], d["sell"] = t[3], t[4], t[5]
    ov = T.at("Bond overview")
    d["stats"] = T.pairs(ov + 1, ov + 9)
    d["sold"] = t[ov + 9]
    d["form121"] = t[ov + 10]
    d["sold_pct"] = int(re.match(r"(\d+)%", d["sold"]).group(1))

    # Highlights (sample figures stay marked, as in v3)
    r = T.at("Reasons to")
    d["reasons_title"] = t[r] + " " + t[r + 1]
    d["reasons"] = [t[r + 2], t[r + 3]]
    bb = T.at("Backed By")
    d["backers"] = (t[bb], t[bb + 1], t[bb + 2])
    d["repaid"] = (t[bb + 3], t[bb + 4])
    d["investors"] = ("Investors", T.after("Investors"))
    d["repayments"] = ("Repayments", T.after("Repayments"))
    c = T.at("Invest with Confidence")
    d["confidence_title"] = t[c]
    d["confidence"] = [(t[c + 1], t[c + 2]), (t[c + 3], t[c + 4])]

    # Calculator
    k = T.at("Returns Calculator")
    d["calc_title"] = t[k]
    d["invest"] = T.after("Investment Amount", k)
    d["ytm"] = T.after("Total Returns", k)
    d["returns"] = t[T.at("Total Returns", k) + 3]
    d["receivable"] = T.after("Total Receivable", k)
    d["timeline_cta"], d["invest_cta"] = t[T.at("Cashflow Timeline", k)], t[T.at("Invest Now", k)]
    d["save_tds"] = t[T.at("save on TDS")]

    # Cashflow: desktop year rows (year, interest, principal) and payouts.
    s, e = T.at("Units:"), T.at("Download Cashflow")
    years, cur, i = [], None, s
    while i < e:
        x = t[i]
        if re.fullmatch(r"\d{4}", x) and i + 2 < e and t[i + 1].startswith("₹") and t[i + 2].startswith("₹"):
            cur = {"year": x, "interest": t[i + 1], "principal": t[i + 2], "rows": []}
            years.append(cur)
            i += 3
            continue
        if re.fullmatch(r"\d{1,2} [A-Z][a-z]{2}", x) and cur is not None:
            mat = t[i + 1] == "(Maturity)"
            j = i + (2 if mat else 1)
            cur["rows"].append((x, mat and t[i + 1], t[j], t[j + 1]))
            i = j + 2
            continue
        i += 1
    if not years or sum(len(y["rows"]) for y in years) < len(years):
        raise SystemExit("bond-details4: cashflow not parsed")
    d["years"] = years
    d["events"] = {t[i - 1]: t[i] for i in range(s, e) if re.fullmatch(r"\d+ Events?", t[i])}
    d["cf_note"] = t[e + 1]
    d["cf_download"] = t[e]
    sp = T.at("Principal", T.at("Total Receivable", T.at("Cashflow")))
    d["split"] = ((t[sp], t[sp + 1]), (t[sp + 3], t[sp + 4]))

    # Company information
    a = T.at("About the Issuer")
    d["facts"] = T.pairs(a + 2, a + 8)
    d["about"] = [B.clean(p) for p in re.findall(r"<p>(.*?)</p>", re.search(
        r'<div class="about-issuer__content[^"]*">(.*?)</div>', main, re.S).group(1), re.S)]
    ks, rf, cf = T.at("Key Strengths"), T.at("Risk Factors"), T.at("Company Financials")
    d["strengths"] = [t[i] for i in range(ks + 1, rf) if not re.fullmatch(r"\d\d", t[i])]
    d["watch"] = [t[i] for i in range(T.at("Watch OUT") + 1, cf) if not re.fullmatch(r"\d\d", t[i])]

    # Ratios
    f = T.at("Financial Ratio")
    d["fy"] = t[f + 1]
    d["ratios"] = [tuple(t[f + 2 + 3 * n: f + 5 + 3 * n]) for n in range(4)]

    # Documents
    d["tax"] = (t[T.at("Tax Deduction")], T.after("Tax Deduction"))
    d["docs"] = []
    for name in ("Information Memorandum", "Rating Rationale"):
        j = main.index(name)
        href = re.findall(r'href="([^"]+)"', main[main.rfind("<a ", 0, j):j])[-1]
        meta, action = t[T.at(name) + 1], t[T.at(name) + 2]
        d["docs"].append((name, meta, action, href))

    # More Bond Details, deduplicated: beta's list, then the investment part.
    m = T.at("More Bond Details", T.at("More Bond Details") + 1) + 1
    spec = T.pairs(m, T.at("Issue Size", m + 1))
    inv0 = T.at("Minimum Investment")
    seen = {k for k, _ in spec}
    spec += [(k, v) for k, v in T.pairs(inv0, T.at("Minimum Investment", inv0 + 1)) if k not in seen]
    d["spec"] = spec

    # App band
    d["app"] = ("Download App", T.after("Download App"))
    d["qr"] = re.search(r'<img class="a3__qr" src="([^"]+)"', main).group(1)
    return d


# ---------------------------------------------------------------- markup
def lead(text):
    """'Label: rest' -> '<b>Label</b> rest' (beta's own split points)."""
    m = re.match(r"([^:]{3,40}):\s*(.*)", text, re.S)
    return "<b>%s</b> %s" % (esc(m.group(1)), esc(m.group(2))) if m else esc(text)


def sample(text):
    return '<!-- DATA: placeholder --><span class="b4-sample" title="Sample data">%s</span>' % esc(text)


def amt(s, cls=""):
    """A per-unit rupee figure the calculator rescales."""
    return '<span class="b4-amt%s" data-amt="%.2f">%s</span>' % (cls, money(s), esc(s))


def header(d):
    crumbs = "".join('<a href="%s">%s</a><i class="ph ph-caret-right" aria-hidden="true"></i>' % (esc(h), esc(x))
                     for h, x in d["crumbs"])
    (l0, v0), *rest = d["stats"]
    stats = "".join('<div><dt>%s</dt><dd>%s</dd></div>' % (esc(k), esc(v)) for k, v in rest)
    return f'''
<header class="b4-hero" aria-labelledby="b4-name">
  <nav class="b4-crumbs" aria-label="Breadcrumb">{crumbs}<span aria-current="page">{esc(d["crumb_here"])}</span></nav>
  <div class="b4-id">
    <img class="b4-logo" src="{esc(d["logo"])}" alt="Mahaveer Finance India Limited logo" width="64" height="64">
    <div>
      <h1 id="b4-name" class="b4-name">{esc(d["name"])}</h1>
      <p class="b4-kind">{esc(d["kind"])}</p>
    </div>
  </div>
  <ul class="b4-tags" aria-label="Features">
    <li><i class="ph ph-arrows-left-right" aria-hidden="true"></i>{esc(d["sell"])}</li>
    <li><i class="ph ph-receipt" aria-hidden="true"></i>{esc(d["form121"])}</li>
  </ul>
  <dl class="b4-figures">
    <div class="b4-figures__lead"><dt>{esc(l0)}</dt><dd>{esc(v0)}</dd></div>
    {stats}
  </dl>
  <div class="b4-sold">
    <span class="b4-sold__bar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="{d["sold_pct"]}" aria-label="{esc(d["sold"])}"><span style="width:{d["sold_pct"]}%"></span></span>
    <span class="b4-sold__label">{esc(d["sold"])}</span>
  </div>
</header>'''


def calculator(d):
    return f'''
<aside class="b4-rail" aria-labelledby="b4-calc-title">
  <div class="b4-calc">
    <h2 id="b4-calc-title" class="b4-calc__title">{esc(d["calc_title"])}</h2>
    <div class="b4-step" role="group" aria-label="Units">
      <button type="button" class="b4-step__btn" data-step="-1" aria-label="Decrease units" disabled><i class="ph ph-minus" aria-hidden="true"></i></button>
      <input class="b4-step__input" type="number" inputmode="numeric" min="1" value="1" aria-label="Units">
      <button type="button" class="b4-step__btn b4-step__btn--up" data-step="1" aria-label="Increase units"><i class="ph ph-plus" aria-hidden="true"></i></button>
    </div>
    <dl class="b4-calc__rows">
      <div><dt>Investment Amount</dt><dd>{amt(d["invest"])}</dd></div>
      <div><dt>Total Returns <span class="b4-badge">{esc(d["ytm"])}</span></dt><dd class="b4-gain">+ {amt(d["returns"])}</dd></div>
      <div class="b4-calc__total"><dt>Total Receivable</dt><dd>{amt(d["receivable"])}</dd></div>
    </dl>
    <a class="b4-btn b4-btn--ghost" href="#cashflow">{esc(d["timeline_cta"])}<i class="ph ph-arrow-down" aria-hidden="true"></i></a>
    <button type="button" class="b4-btn b4-btn--gold">{esc(d["invest_cta"])}<i class="ph ph-arrow-up-right" aria-hidden="true"></i></button>
  </div>
</aside>'''


SECTIONS = [("highlights", None), ("cashflow", "Cashflow"), ("company", "Company Information"),
            ("financials", "Company Financials"), ("documents", "Documents and More Details")]


def section_nav():
    links = "".join('<a href="#%s">%s</a>' % (i, esc(lab)) for i, lab in SECTIONS if lab)
    return '<nav class="b4-tabs" aria-label="On this page"><div class="b4-tabs__track">%s</div></nav>' % links


def highlights(d):
    pts = "".join("<li><span>%s</span></li>" % lead(p) for p in d["reasons"])
    conf = "".join('<li><i class="ph %s" aria-hidden="true"></i><div><h3>%s</h3><p>%s</p></div></li>'
                   % (ic, esc(h), esc(p)) for ic, (h, p) in zip(("ph-arrows-left-right", "ph-shield-check"), d["confidence"]))
    b = d["backers"]
    proof = (f'<div><dt>{esc(b[0])} {esc(b[1])}</dt><dd>{sample(b[2])}</dd></div>'
             f'<div><dt>{esc(d["repaid"][1])}</dt><dd>{sample(d["repaid"][0])}</dd></div>'
             f'<div><dt>{esc(d["investors"][0])}</dt><dd>{sample(d["investors"][1])}</dd></div>'
             f'<div><dt>{esc(d["repayments"][0])}</dt><dd>{sample(d["repayments"][1])}</dd></div>')
    return f'''
<section class="b4-sec" id="highlights" aria-labelledby="b4-reasons">
  <div class="b4-why">
    <div>
      <h2 id="b4-reasons" class="b4-h2">{esc(d["reasons_title"])}</h2>
      <ol class="b4-reasons">{pts}</ol>
    </div>
    <div class="b4-conf">
      <h3 class="b4-eyebrow">{esc(d["confidence_title"])}</h3>
      <ul>{conf}</ul>
    </div>
  </div>
  <dl class="b4-proof">{proof}</dl>
</section>'''


def cashflow(d):
    yrs = []
    for n, y in enumerate(d["years"]):
        rows = "".join(
            '<tr><th scope="row">%s%s</th><td>%s</td><td>%s</td></tr>'
            % (esc(dt), ' <span class="b4-mat">%s</span>' % esc(mat) if mat else "", amt(i), amt(p))
            for dt, mat, i, p in y["rows"])
        ev = d["events"].get(y["year"], "")
        yrs.append(f'''<details class="b4-year"{" open" if n == 0 else ""}>
      <summary><span class="b4-year__y">{esc(y["year"])}</span><span class="b4-year__ev">{esc(ev)}</span><span class="b4-year__a">{amt(y["interest"])}</span><span class="b4-year__a">{amt(y["principal"])}</span><i class="ph ph-caret-down" aria-hidden="true"></i></summary>
      <table class="b4-pay"><thead class="sr-only"><tr><th scope="col">Date</th><th scope="col">Interest</th><th scope="col">Principal</th></tr></thead><tbody>{rows}</tbody></table>
    </details>''')
    (pl, pv), (il, iv) = d["split"]
    return f'''
<section class="b4-sec" id="cashflow" aria-labelledby="b4-cf">
  <h2 id="b4-cf" class="b4-h2">Cashflow</h2>
  <div class="b4-cfsum">
    <div><span>Investment Amount</span><strong>{amt(d["invest"])}</strong></div>
    <div class="b4-cfsum__total"><span>Total Receivable</span><strong>{amt(d["receivable"])}</strong>
      <p class="b4-split"><span>{esc(pl)} <b>{amt(pv)}</b></span><span aria-hidden="true">+</span><span>{esc(il)} <b class="b4-gain">{amt(iv)}</b></span></p></div>
  </div>
  <div class="b4-years" role="group" aria-label="Payouts by year">
    <div class="b4-years__head" aria-hidden="true"><span>Date</span><span></span><span>Interest</span><span>Principal</span></div>
    {"".join(yrs)}
  </div>
  <div class="b4-cffoot">
    <p>{esc(d["cf_note"])}</p>
    <button type="button" class="b4-link"><i class="ph ph-download-simple" aria-hidden="true"></i>{esc(d["cf_download"])}</button>
  </div>
</section>'''


def company(d):
    facts = "".join("<div><dt>%s</dt><dd>%s</dd></div>" % (esc(k), esc(v)) for k, v in d["facts"])
    about = "".join("<p>%s</p>" % p for p in d["about"])
    st = "".join("<li>%s</li>" % lead(x) for x in d["strengths"])
    wo = "".join("<li>%s</li>" % lead(x) for x in d["watch"])
    return f'''
<section class="b4-sec" id="company" aria-labelledby="b4-co">
  <h2 id="b4-co" class="b4-h2">Company Information</h2>
  <h3 class="b4-h3">About the Issuer</h3>
  <dl class="b4-facts">{facts}</dl>
  <div class="b4-prose">{about}</div>
  <h3 class="b4-h3">Strength / Weaknesses</h3>
  <div class="b4-sw">
    <div class="b4-sw__col b4-sw__col--good"><h4><i class="ph ph-trend-up" aria-hidden="true"></i>Key Strengths</h4><ol>{st}</ol></div>
    <div class="b4-sw__col b4-sw__col--watch"><h4><i class="ph ph-warning" aria-hidden="true"></i>Watch out</h4><ol>{wo}</ol></div>
  </div>
</section>'''


def financials(d, data):
    cards = []
    for name, pts in data:
        vals = [v for _, v in pts]
        zero, ext = B.scale(vals)
        ch = B.change(pts)
        delta = ""
        if ch:
            pct, py = ch
            up = pct >= 0
            delta = ('<p class="b4-delta b4-delta--%s"><i class="ph ph-arrow-%s" aria-hidden="true"></i>%.1f%% <span>vs %s</span></p>'
                     % ("up" if up else "down", "up-right" if up else "down-right", abs(pct), py))
        bars = "".join(
            '<li><span class="b4-bar" style="--top:%.1f%%;--h:%.1f%%"><b>%s</b></span><span class="b4-bar__y">%s</span></li>'
            % (top, h, B.crore(v), y) for (y, v), (top, h) in zip(pts, ext))
        cards.append(f'''<article class="b4-fin">
      <h3>{esc(B.SUBTITLE.get(name, name))}</h3>
      <p class="b4-fin__v">{B.crore(pts[-1][1])} <span>{pts[-1][0]}</span></p>{delta}
      <ol class="b4-bars" style="--zero:{zero:.1f}%" aria-label="{esc(B.SUBTITLE.get(name, name))} by year">{bars}</ol>
    </article>''')
    ratios = "".join('<div><dt>%s</dt><dd>%s</dd><dd class="b4-ok">%s</dd></div>' % (esc(a), esc(b), esc(c.title()))
                     for a, b, c in d["ratios"])
    return f'''
<section class="b4-sec" id="financials" aria-labelledby="b4-fi">
  <h2 id="b4-fi" class="b4-h2">Company Financials</h2>
  <div class="b4-fins">{"".join(cards)}</div>
  <h3 class="b4-h3">Financial Ratio <span class="b4-fy">{esc(d["fy"])}</span></h3>
  <dl class="b4-ratios">{ratios}</dl>
</section>'''


def documents(d):
    docs = "".join(
        f'<li><a href="{esc(h)}" target="_blank" rel="noopener noreferrer"><i class="ph ph-file-text" aria-hidden="true"></i>'
        f'<span><b>{esc(n)}</b><small>{esc(m)}</small></span><span class="b4-doc__act">{esc(a)}'
        f'<i class="ph {"ph-download-simple" if a == "Download" else "ph-arrow-up-right"}" aria-hidden="true"></i></span></a></li>'
        for n, m, a, h in d["docs"])
    spec = "".join('<div%s><dt>%s</dt><dd>%s</dd></div>' % (' class="b4-spec__wide"' if len(v) > 32 else "", esc(k), esc(v))
                   for k, v in d["spec"])
    tt, tx = d["tax"]
    return f'''
<section class="b4-sec" id="documents" aria-labelledby="b4-do">
  <h2 id="b4-do" class="b4-h2">Documents and More Details</h2>
  <ul class="b4-docs">{docs}</ul>
  <p class="b4-tax"><i class="ph ph-info" aria-hidden="true"></i><span><b>{esc(tt)}</b> {esc(tx)}</span></p>
  <h3 class="b4-h3">More Bond Details</h3>
  <dl class="b4-spec">{spec}</dl>
</section>'''


def app_band(d):
    t, s = d["app"]
    return f'''
<section class="b4-app" aria-labelledby="b4-app">
  <div><h2 id="b4-app" class="b4-h2">{esc(t)}</h2><p>{esc(s)}</p></div>
  <img src="{esc(d["qr"])}" alt="{esc(s)}" width="120" height="148" loading="lazy">
</section>'''


def mobile_bar(d):
    return f'''
<div class="b4-mbar">
  <div><span>Investment Amount</span><strong>{amt(d["invest"])}</strong><small>{esc(d["save_tds"])}</small></div>
  <button type="button" class="b4-btn b4-btn--gold">{esc(d["invest_cta"])}<i class="ph ph-arrow-up-right" aria-hidden="true"></i></button>
</div>'''


STYLE = """<style>
/* bond-details4: built from scratch on GoldenPi's tokens. One radius scale:
   cards 20px, tiles 14px, controls fully round. */
.b4 {
  --ink: #322811; --sub: #666666; --gold: #d4af37; --bronze: #8a6520; --gain: #06963c; --warn: #b45309;
  --line: #ebe4d3; --card: #ffffff; --tint: #fbf8f1; --page: #f7f5f2;
  max-width: 1200px; margin: 0 auto; padding: 16px 20px 120px; color: var(--ink);
  font-family: "Satoshi", ui-sans-serif, system-ui, sans-serif; font-variant-numeric: tabular-nums;
}
.b4 *, .b4 *::before, .b4 *::after { box-sizing: border-box; }
/* Zero-specificity reset, so every component rule below wins over it. */
:where(.b4) :where(h1, h2, h3, h4, p, ol, ul, dl, dd) { margin: 0; padding: 0; }
:where(.b4) :where(ol, ul) { list-style: none; }
.b4 a { color: inherit; }
.b4 .sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
.b4-layout { display: grid; grid-template-columns: minmax(0, 1fr); gap: 20px; }
@media (min-width: 1024px) {
  .b4-layout { grid-template-columns: minmax(0, 1fr) 340px; column-gap: 28px; align-items: start; }
  .b4-hero { grid-column: 1; grid-row: 1; }
  .b4-rail { grid-column: 2; grid-row: 1 / span 3; position: sticky; top: calc(var(--header-height, 96px) + 16px); }
  .b4-tabs { grid-column: 1; grid-row: 2; }
  .b4-main { grid-column: 1; grid-row: 3; }
}

/* Hero */
.b4-hero { padding: 8px 0 4px; }
.b4-crumbs { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; margin-bottom: 20px; color: var(--sub); font-size: 12px; font-weight: 500; }
.b4-crumbs a { text-decoration: none; }
.b4-crumbs a:hover { color: var(--ink); }
.b4-crumbs [aria-current] { color: var(--ink); }
.b4-id { display: flex; align-items: center; gap: 16px; }
.b4-logo { width: 64px; height: 64px; border-radius: 16px; border: 1px solid var(--line); background: var(--card); object-fit: contain; }
.b4-name { font-size: 32px; line-height: 38px; font-weight: 700; letter-spacing: -0.02em; }
.b4-kind { margin-top: 2px; color: var(--sub); font-size: 15px; }
.b4-tags { display: flex; flex-wrap: wrap; gap: 8px; margin: 18px 0 24px; }
.b4-tags li { display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; border-radius: 999px; background: var(--card); border: 1px solid var(--line); font-size: 13px; font-weight: 500; }
.b4-tags i { color: var(--bronze); font-size: 15px; }
.b4-figures { display: grid; grid-template-columns: 1.3fr repeat(3, 1fr); border-radius: 20px; background: var(--card); border: 1px solid var(--line); }
.b4-figures > div { padding: 18px 20px; }
.b4-figures > div + div { border-left: 1px solid var(--line); }
.b4-figures dt { color: var(--sub); font-size: 13px; font-weight: 500; }
.b4-figures dd { margin-top: 6px; font-size: 20px; line-height: 26px; font-weight: 700; }
.b4-figures__lead dd { color: var(--gain); font-size: 34px; line-height: 38px; letter-spacing: -0.02em; }
.b4-sold { display: flex; align-items: center; gap: 12px; margin-top: 14px; }
.b4-sold__bar { flex: 1; max-width: 220px; height: 6px; border-radius: 999px; background: #ece4cf; overflow: hidden; }
.b4-sold__bar span { display: block; height: 100%; border-radius: inherit; background: linear-gradient(90deg, #e9cf74, var(--gold)); }
.b4-sold__label { font-size: 13px; font-weight: 700; color: var(--bronze); }

/* Calculator rail */
.b4-calc { padding: 22px; border-radius: 20px; background: var(--card); border: 1px solid var(--line); box-shadow: 0 24px 48px -32px rgba(138, 101, 32, 0.35); }
.b4-calc__title { font-size: 17px; font-weight: 700; }
.b4-step { display: grid; grid-template-columns: 44px 1fr 44px; align-items: center; margin: 16px 0 18px; padding: 4px; border-radius: 999px; border: 1px solid var(--line); }
.b4-step__btn { width: 44px; height: 44px; border: 0; border-radius: 50%; background: #f3efe5; color: var(--ink); font-size: 18px; cursor: pointer; display: grid; place-items: center; }
.b4-step__btn--up { background: linear-gradient(135deg, #f1d77f, #c8a02a); }
.b4-step__btn:disabled { opacity: 0.45; cursor: not-allowed; }
.b4-step__btn:focus-visible, .b4-step__input:focus-visible { outline: 2px solid var(--gold); outline-offset: 2px; }
.b4-step__input { width: 100%; border: 0; background: transparent; text-align: center; font: inherit; font-size: 22px; font-weight: 700; color: var(--ink); -moz-appearance: textfield; }
.b4-step__input::-webkit-inner-spin-button, .b4-step__input::-webkit-outer-spin-button { -webkit-appearance: none; }
.b4-calc__rows > div { display: flex; align-items: baseline; justify-content: space-between; gap: 12px; padding: 7px 0; }
.b4-calc__rows dt { display: flex; align-items: center; gap: 6px; color: var(--sub); font-size: 14px; }
.b4-calc__rows dd { font-size: 15px; font-weight: 700; white-space: nowrap; }
.b4-calc__total { margin-top: 6px; padding-top: 12px !important; border-top: 1px solid var(--line); }
.b4-calc__total dt { color: var(--ink); font-weight: 700; }
.b4-calc__total dd { color: var(--gain); font-size: 22px; }
.b4-badge { padding: 1px 6px; border-radius: 6px; background: #e8f6ed; color: var(--gain); font-size: 11px; font-weight: 700; }
.b4-gain { color: var(--gain); }
.b4-btn { display: flex; align-items: center; justify-content: center; gap: 8px; width: 100%; min-height: 46px; margin-top: 12px; border-radius: 999px; font: inherit; font-size: 15px; font-weight: 700; text-decoration: none; cursor: pointer; transition: transform 0.15s ease, box-shadow 0.2s ease; }
.b4-btn:active { transform: scale(0.98); }
.b4-btn:focus-visible { outline: 2px solid var(--ink); outline-offset: 2px; }
.b4-btn--ghost { border: 1px solid var(--gold); background: var(--card); color: var(--ink); }
.b4-btn--gold { border: 0; background: linear-gradient(100deg, #f6e3a0, #d4af37 55%, #b8901f); color: var(--ink); box-shadow: 0 10px 22px -12px rgba(184, 144, 31, 0.8); }

/* Section bar */
.b4-tabs { position: sticky; top: var(--header-height, 96px); z-index: 5; margin: 4px -20px 0; padding: 10px 20px; background: color-mix(in srgb, var(--page) 92%, transparent); backdrop-filter: blur(8px); }
.b4-tabs__track { display: flex; gap: 6px; overflow-x: auto; scrollbar-width: none; }
.b4-tabs__track::-webkit-scrollbar { display: none; }
.b4-tabs a { flex: none; padding: 8px 14px; border-radius: 999px; color: var(--sub); font-size: 14px; font-weight: 500; text-decoration: none; transition: background-color 0.2s ease, color 0.2s ease; }
.b4-tabs a:hover { color: var(--ink); }
.b4-tabs a.is-on { background: var(--ink); color: #fff; }
.b4-tabs a:focus-visible { outline: 2px solid var(--gold); outline-offset: 2px; }

/* Sections */
.b4-main { display: grid; gap: 20px; }
.b4-sec { scroll-margin-top: calc(var(--header-height, 96px) + 70px); padding: 28px; border-radius: 20px; background: var(--card); border: 1px solid var(--line); }
.b4-h2 { font-size: 22px; line-height: 28px; font-weight: 700; letter-spacing: -0.01em; }
.b4-h3 { margin: 28px 0 14px; font-size: 16px; font-weight: 700; display: flex; align-items: center; gap: 10px; }
.b4-eyebrow { color: var(--bronze); font-size: 12px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }
.b4-sample { text-decoration: underline dashed rgba(138, 101, 32, 0.55); text-underline-offset: 4px; }

.b4-why { display: grid; gap: 24px; }
@media (min-width: 768px) { .b4-why { grid-template-columns: 1.25fr 1fr; gap: 32px; } }
.b4-reasons { margin-top: 16px; counter-reset: r; display: grid; gap: 14px; }
.b4-reasons li { counter-increment: r; display: grid; grid-template-columns: 28px 1fr; gap: 10px; color: var(--sub); font-size: 15px; line-height: 23px; }
.b4-reasons li::before { content: counter(r); display: grid; place-items: center; width: 26px; height: 26px; border-radius: 50%; background: var(--tint); border: 1px solid var(--line); color: var(--bronze); font-size: 12px; font-weight: 700; }
.b4-reasons b, .b4-sw b { color: var(--ink); }
.b4-conf { padding: 20px; border-radius: 14px; background: var(--tint); }
.b4-conf ul { margin-top: 14px; display: grid; gap: 16px; }
.b4-conf li { display: grid; grid-template-columns: 24px 1fr; gap: 10px; }
.b4-conf i { color: var(--bronze); font-size: 22px; }
.b4-conf h3 { font-size: 15px; font-weight: 700; }
.b4-conf p { margin-top: 2px; color: var(--sub); font-size: 14px; line-height: 20px; }
.b4-proof { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1px; margin-top: 24px; border-radius: 14px; overflow: hidden; background: var(--line); border: 1px solid var(--line); }
@media (min-width: 768px) { .b4-proof { grid-template-columns: repeat(4, minmax(0, 1fr)); } }
.b4-proof > div { padding: 14px 16px; background: var(--card); }
.b4-proof dt { color: var(--sub); font-size: 12px; line-height: 16px; }
.b4-proof dd { margin-top: 4px; font-size: 16px; font-weight: 700; }

/* Cashflow */
.b4-cfsum { display: grid; grid-template-columns: 1fr 1.4fr; gap: 12px; margin: 18px 0 20px; }
.b4-cfsum > div { padding: 16px 18px; border-radius: 14px; background: var(--tint); }
.b4-cfsum > div > span { display: block; color: var(--sub); font-size: 13px; }
.b4-cfsum strong { display: block; margin-top: 4px; font-size: 22px; font-weight: 700; }
.b4-cfsum__total { background: #eef8f1 !important; }
.b4-cfsum__total strong { color: var(--gain); }
.b4-split { display: flex; flex-wrap: wrap; gap: 4px 10px; margin-top: 8px; color: var(--sub); font-size: 13px; }
.b4-split span { display: inline; }
.b4-split b { color: var(--ink); }
.b4-split .b4-gain { color: var(--gain); }
.b4-years__head, .b4-year > summary { display: grid; grid-template-columns: 90px 1fr 1fr 1fr 20px; align-items: center; gap: 8px; }
.b4-years__head { padding: 0 16px 8px; color: var(--sub); font-size: 12px; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; }
.b4-years__head span:nth-child(2) { visibility: hidden; }
.b4-year { border-top: 1px solid var(--line); }
.b4-year > summary { padding: 14px 16px; cursor: pointer; list-style: none; font-weight: 700; }
.b4-year > summary::-webkit-details-marker { display: none; }
.b4-year > summary:focus-visible { outline: 2px solid var(--gold); outline-offset: -2px; border-radius: 10px; }
.b4-year > summary i { color: var(--sub); transition: transform 0.25s ease; }
.b4-year[open] > summary i { transform: rotate(180deg); }
.b4-year__ev { justify-self: start; padding: 2px 8px; border-radius: 999px; background: #fbf0cc; color: var(--bronze); font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; }
.b4-pay { width: 100%; border-collapse: collapse; margin-bottom: 8px; }
.b4-pay tr { display: grid; grid-template-columns: calc(90px + 8px + (100% - 90px - 20px - 32px) / 3) 1fr 1fr 20px; gap: 8px; padding: 8px 16px; }
.b4-pay tr::after { content: ""; }
.b4-pay th, .b4-pay td { padding: 0; text-align: left; font-size: 14px; font-weight: 500; }
.b4-pay th { color: var(--sub); padding-left: 16px; position: relative; }
.b4-pay th::before { content: ""; position: absolute; left: 0; top: 50%; width: 7px; height: 7px; margin-top: -4px; border-radius: 50%; border: 1.5px solid var(--gold); }
.b4-mat { margin-left: 6px; padding: 1px 6px; border-radius: 6px; background: #fbf0cc; color: var(--bronze); font-size: 11px; font-weight: 700; }
.b4-cffoot { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 12px; margin-top: 8px; padding-top: 16px; border-top: 1px solid var(--line); }
.b4-cffoot p { flex: 1 1 320px; color: var(--sub); font-size: 13px; line-height: 19px; }
.b4-link { display: inline-flex; align-items: center; gap: 6px; padding: 0; border: 0; background: none; color: var(--bronze); font: inherit; font-size: 14px; font-weight: 700; cursor: pointer; text-decoration: underline; text-underline-offset: 3px; }
.b4-link:focus-visible { outline: 2px solid var(--gold); outline-offset: 3px; }

/* Company */
.b4-facts { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; margin-bottom: 18px; }
.b4-facts > div { padding: 14px 16px; border-radius: 14px; background: var(--tint); }
.b4-facts dt { color: var(--sub); font-size: 12px; }
.b4-facts dd { margin-top: 4px; font-size: 16px; font-weight: 700; }
.b4-prose { display: grid; gap: 12px; max-width: 70ch; color: var(--sub); font-size: 15px; line-height: 24px; }
.b4-prose strong { color: var(--ink); }
.b4-sw { display: grid; gap: 14px; }
@media (min-width: 768px) { .b4-sw { grid-template-columns: 1fr 1fr; } }
.b4-sw__col { padding: 18px; border-radius: 14px; border: 1px solid var(--line); }
.b4-sw__col h4 { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; font-size: 13px; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; }
.b4-sw__col--good h4 { color: var(--gain); }
.b4-sw__col--watch h4 { color: var(--warn); }
.b4-sw__col--good { background: #f4fbf6; border-color: #d6eedd; }
.b4-sw__col--watch { background: #fdf8ef; border-color: #f1e2c4; }
.b4-sw ol { display: grid; gap: 12px; }
.b4-sw li { color: var(--sub); font-size: 14px; line-height: 21px; }

/* Financials: small multiples */
.b4-fins { display: grid; gap: 12px; margin-top: 18px; }
@media (min-width: 640px) { .b4-fins { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
.b4-fin { padding: 18px; border-radius: 14px; background: var(--tint); }
.b4-fin h3 { color: var(--sub); font-size: 13px; font-weight: 500; }
.b4-fin__v { margin-top: 4px; font-size: 24px; font-weight: 700; letter-spacing: -0.01em; }
.b4-fin__v span { color: var(--sub); font-size: 13px; font-weight: 500; letter-spacing: 0; }
.b4-delta { display: inline-flex; align-items: center; gap: 4px; margin-top: 4px; font-size: 13px; font-weight: 700; }
.b4-delta span { color: var(--sub); font-weight: 500; }
.b4-delta--up { color: var(--gain); }
.b4-delta--down { color: #c0392b; }
.b4-bars { position: relative; display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; height: 140px; margin-top: 14px; padding-bottom: 20px; }
.b4-bars li { position: relative; }
.b4-bar { position: absolute; left: 12%; right: 12%; top: var(--top); height: var(--h); min-height: 2px; border-radius: 8px 8px 3px 3px; background: linear-gradient(180deg, #e9cf74, #c9a133); transform-origin: bottom; }
.b4-bars li:not(:last-child) .b4-bar { background: #e6dcc2; }
.b4-bar b { position: absolute; left: 50%; bottom: 100%; transform: translateX(-50%); padding-bottom: 4px; white-space: nowrap; font-size: 11px; font-weight: 700; }
.b4-bar__y { position: absolute; left: 0; right: 0; bottom: -20px; text-align: center; color: var(--sub); font-size: 12px; }
.b4-bars li { height: 100%; }
.b4-fy { padding: 2px 8px; border-radius: 999px; background: var(--tint); border: 1px solid var(--line); color: var(--sub); font-size: 12px; font-weight: 500; }
.b4-ratios { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
@media (min-width: 768px) { .b4-ratios { grid-template-columns: repeat(4, minmax(0, 1fr)); } }
.b4-ratios > div { padding: 14px 16px; border-radius: 14px; border: 1px solid var(--line); }
.b4-ratios dt { color: var(--sub); font-size: 12px; line-height: 16px; min-height: 32px; }
.b4-ratios dd { margin-top: 6px; font-size: 18px; font-weight: 700; }
.b4-ratios .b4-ok { display: inline-flex; align-items: center; gap: 5px; margin-top: 6px; color: var(--gain); font-size: 12px; }
.b4-ratios .b4-ok::before { content: ""; width: 6px; height: 6px; border-radius: 50%; background: var(--gain); }

/* Documents */
.b4-docs { display: grid; gap: 10px; margin-top: 18px; }
@media (min-width: 768px) { .b4-docs { grid-template-columns: 1fr 1fr; } }
.b4-docs a { display: grid; grid-template-columns: 40px 1fr auto; align-items: center; gap: 12px; padding: 14px 16px; border-radius: 14px; border: 1px solid var(--line); text-decoration: none; transition: border-color 0.2s ease, background-color 0.2s ease; }
.b4-docs a:hover { border-color: var(--gold); background: var(--tint); }
.b4-docs a:focus-visible { outline: 2px solid var(--gold); outline-offset: 2px; }
.b4-docs a > i { display: grid; place-items: center; width: 40px; height: 40px; border-radius: 50%; background: var(--tint); color: var(--bronze); font-size: 20px; }
.b4-docs b { display: block; font-size: 15px; }
.b4-docs small { display: block; margin-top: 2px; color: var(--sub); font-size: 12px; }
.b4-doc__act { display: inline-flex; align-items: center; gap: 4px; color: var(--bronze); font-size: 13px; font-weight: 700; }
.b4-tax { display: flex; gap: 10px; margin-top: 12px; padding: 14px 16px; border-radius: 14px; background: var(--tint); color: var(--sub); font-size: 14px; line-height: 21px; }
.b4-tax i { color: var(--bronze); font-size: 18px; margin-top: 1px; }
.b4-tax b { color: var(--ink); }
.b4-spec { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px 20px; }
@media (min-width: 768px) { .b4-spec { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
.b4-spec dt { color: var(--sub); font-size: 12px; }
.b4-spec dd { margin-top: 3px; font-size: 15px; font-weight: 700; line-height: 21px; overflow-wrap: break-word; }
.b4-spec__wide { grid-column: 1 / -1; }

/* App band */
.b4-app { display: flex; align-items: center; justify-content: space-between; gap: 20px; padding: 24px 28px; border-radius: 20px; background: linear-gradient(120deg, #fffaf0, #f7ecd0); border: 1px solid #efdfb6; }
.b4-app p { margin-top: 6px; color: var(--sub); font-size: 15px; }
.b4-app img { flex: none; width: 110px; height: auto; }

/* Mobile bar */
.b4-mbar { position: fixed; left: 0; right: 0; bottom: 0; z-index: 30; display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 12px 20px calc(12px + env(safe-area-inset-bottom)); background: var(--card); border-top: 1px solid var(--line); box-shadow: 0 -12px 28px -20px rgba(50, 40, 17, 0.4); }
.b4-mbar span { display: block; color: var(--sub); font-size: 12px; }
.b4-mbar strong { display: block; font-size: 18px; }
.b4-mbar small { display: block; color: var(--gain); font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; }
.b4-mbar .b4-btn { width: auto; margin: 0; padding: 0 22px; }
@media (min-width: 1024px) { .b4-mbar { display: none; } .b4 { padding-bottom: 48px; } }
/* As on bond-details3, the invest bar owns the bottom edge on phones: the
   header's bottom tab bar steps aside rather than stacking under it. */
@media (max-width: 999px) { .nb__nav { display: none !important; } }

@media (max-width: 1023px) {
  .b4-rail { order: 0; }
}
@media (max-width: 767px) {
  .b4-name { font-size: 26px; line-height: 32px; }
  .b4-figures { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .b4-figures__lead { grid-column: 1 / -1; border-bottom: 1px solid var(--line); }
  .b4-figures > div + div { border-left: 0; }
  .b4-figures > div:nth-child(n + 3) { border-left: 1px solid var(--line); }
  .b4-figures > div { padding: 14px; }
  .b4-figures dd { font-size: 16px; }
  .b4-figures__lead dd { font-size: 28px; line-height: 32px; }
  .b4-sec { padding: 20px 16px; }
  .b4-cfsum { grid-template-columns: 1fr; }
  .b4-years__head, .b4-year > summary { grid-template-columns: 52px 1fr 1fr 16px; }
  .b4-years__head span:nth-child(2), .b4-year__ev { display: none; }
  .b4-year > summary { padding: 12px 8px; font-size: 14px; }
  .b4-years__head { padding: 0 8px 8px; }
  .b4-pay tr { grid-template-columns: 1fr 1fr 1fr; padding: 8px; }
  .b4-pay th, .b4-pay td { font-size: 13px; }
  .b4-facts { grid-template-columns: 1fr 1fr; }
  .b4-app img { width: 84px; }
}
@media (prefers-reduced-motion: reduce) {
  .b4 * { transition: none !important; }
}
</style>
"""

SCRIPT = """<script>
// bond-details4: the units stepper rescales every per-unit figure, and the
// section bar marks the section in view. The page reads correctly without it.
(function () {
  var input = document.querySelector('.b4-step__input');
  var down = document.querySelector('.b4-step__btn[data-step="-1"]');
  var amts = [].slice.call(document.querySelectorAll('[data-amt]'));
  var fmt = new Intl.NumberFormat('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  function set(n) {
    n = Math.max(1, Math.min(9999, Math.floor(Number(n) || 1)));
    input.value = n;
    down.disabled = n <= 1;
    amts.forEach(function (el) { el.textContent = '\\u20b9 ' + fmt.format(Number(el.dataset.amt) * n); });
  }
  if (input) {
    document.querySelectorAll('.b4-step__btn').forEach(function (b) {
      b.addEventListener('click', function () { set(Number(input.value) + Number(b.dataset.step)); });
    });
    input.addEventListener('change', function () { set(input.value); });
  }
  var links = [].slice.call(document.querySelectorAll('.b4-tabs a'));
  if (!('IntersectionObserver' in window) || !links.length) return;
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      links.forEach(function (a) {
        var on = a.hash === '#' + e.target.id;
        a.classList.toggle('is-on', on);
        if (on) a.scrollIntoView({ block: 'nearest', inline: 'nearest' });
      });
    });
  }, { rootMargin: '-35% 0px -55% 0px' });
  links.forEach(function (a) { var s = document.querySelector(a.hash); if (s) io.observe(s); });
})();
</script>
"""


def main():
    h = open(SRC, encoding="utf-8").read()
    d = read(h)
    raw = open(B.CAP + ".expanded.html", encoding="utf-8").read()
    data = B.series(raw)

    body = ('<main id="main-content"><div class="b4"><div class="b4-layout">%s%s%s<div class="b4-main">%s%s%s%s%s%s</div>'
            '</div></div>%s</main>'
            % (header(d), calculator(d), section_nav(), highlights(d), cashflow(d), company(d),
               financials(d, data), documents(d), app_band(d), mobile_bar(d)))

    head = h[:h.index("<main")]
    head = head.replace("<!-- Generated by pages/_bond_beta.py from the beta.goldenpi.com capture; do not edit. -->",
                        "<!-- Generated by pages/_bond_v4.py from bond-details3.html and the beta.goldenpi.com "
                        "capture; do not edit. -->", 1)
    head = head.replace("</head>", ICONS + STYLE + "</head>", 1)
    tail = h[h.index("</main>") + len("</main>"):]
    tail = B.drop(tail, '<div id="cashflow-modal"')
    for marker in ("// Stand-in for beta's React handlers", "// bond-details3 financials"):
        k = tail.index(marker)
        a, b = tail.rfind("<script>", 0, k), tail.index("</script>", k) + len("</script>")
        tail = tail[:a] + tail[b:]
    tail = tail.replace("</body>", SCRIPT + "</body>", 1)
    page = head + body + tail
    if "₹" not in page or "DATA: placeholder" not in page:
        raise SystemExit("bond-details4: content missing")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page)
    print("%s  %d bytes" % (os.path.relpath(OUT, os.path.dirname(HERE)), len(page)))


if __name__ == "__main__":
    main()
