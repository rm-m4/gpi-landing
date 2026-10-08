#!/usr/bin/env python3
"""ipo-details.html: beta's NCD IPO page for SMC Global Securities, built from
bond-details7's blocks.

bond-details7.html is the template and is only read, never written. Every
block the two pages share (header card, Company Information, Strength /
Weaknesses, Company Financials, Documents, Returns Calculator, app QR band,
phone invest bar) keeps bond-details7's markup and CSS; only the content is
SMC's. The two IPO-only blocks, Popular IPO Series and the IPO Series table,
are production's own markup (beta's server-rendered HTML) with production's
CSS rules, vendored in assets/beta/ipo.css.

Content: content/beta_bond-ipo_GPID104212_smc.md (captured 2026-10-08).
Production markup: crawl/rendered/beta_bond-ipo_GPID104212_smc-global-securities-limited/ssr.html.

    python3 pages/_bond_beta.py && python3 pages/_bond_v7.py && python3 pages/_ipo_details.py
"""
import os
import re

import _bond_beta as B

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(HERE, "bond-details7.html")
OUT = os.path.join(HERE, "ipo-details.html")
SSR = os.path.join(ROOT, "crawl/rendered/beta_bond-ipo_GPID104212_smc-global-securities-limited/ssr.html")

NAME = "SMC GLOBAL SECURITIES LIMITED"
LOGO = "../assets/img/ipo/smc-logo.png"
FACTS = [("Annual Revenue", "998.53 Cr (FY-2026)"), ("Year Of Inception", "1994"), ("Industry", "Corporate"),
         ("Head Office", "NEW DELHI"), ("Type Of Issuer", "Corporate"), ("Current MD/CEO", "Mr. Subhash C. Aggarwal")]
ABOUT = ("<p>SMC Global Securities Limited (SMC) is an Indian financial services company that provides a range of "
         "services to corporates, institutions, high-net-worth individuals, and retail clients. Founded in 1990, SMC "
         "has accumulated over three decades of experience in the financial sector.</p>")
STRENGTHS = ["Profitability: PAT grew from ₹29.73 cr (FY20) to ~₹144 cr (FY24), 4-year CAGR 36.5%.",
             "Diversified business profile: Equities, commodities, currency, debt , PMS , depository and clearing",
             "Experienced Promoters: Mr. Subhash Chand Aggarwal, 40+ yrs in capital markets",
             "Long operating track record : 30+ yrs in capital markets with strong retail network &amp; ~2 lakh NSE clients."]
WATCH = ["Regulatory risks:Operations exposed to changing laws and regulations.",
         "Inherent market volatility :Weakening sentiment caused sharp trading drop; PAT down ~25% to ₹105 cr in FY25 (vs ₹141 cr FY24).",
         "Highly competitive landscape: Intense competition from low-cost players may pressure profitability"]
CR = 10 ** 7
FIN = [("Revenue", [("2024", 883.46 * CR), ("2025", 955.38 * CR), ("2026", 998.53 * CR)]),
       ("PAT", [("2024", 141.03 * CR), ("2025", 105.26 * CR), ("2026", 81.31 * CR)]),
       ("Net Worth", [("2024", 883.80 * CR), ("2025", 962.57 * CR), ("2026", 1018.70 * CR)]),
       ("Cash & Cash Eq.", [("2024", 52.93 * CR), ("2025", 15.27 * CR), ("2026", 52.82 * CR)])]
RATIOS = [("Debt to Equity Ratio", "0.83x", "HEALTHY", "good"),
          ("Operating Cash Flow to Debt Ratio", "1.98", "HEALTHY", "good"),
          ("Interest Coverage Ratio", "11.5%", "BALANCED RISK", "warning")]
IM_URL = "https://storage.googleapis.com/gpi-prod-ncd-files/parimary/prospectus/SMC%20Global%20NCD%20IPO%20Prospectus%205%20OCT%2026.pdf"
RATING_URL = "https://www.icra.in/Rationale/ShowRationaleReport?Id=145557"
FORM_URL = "https://www.incometaxindia.gov.in/documents/d/guest/form-no-121-1"
TRUSTEE = ("DBI Trusteeship Services Limited", "Universal Building, Sir PM Road, Fort, Mumbai ? 400 001")
REGISTRAR = ("MUFG Intime India Private Limited (formerly Link Intime India Private Limited)",
             "C 101, Embassy 247, L. B. S Marg, Vikhroli West, Mumbai 400 083")


def element(h, start):
    """End index of the element whose start tag begins at `start` (balanced on that tag name)."""
    tag = re.match(r"<(\w+)", h[start:]).group(1)
    depth = 0
    for t in re.finditer(r"<(/?)%s\b[^>]*>" % tag, h[start:]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            return start + t.end()
    raise SystemExit("ipo-details: unbalanced <%s> at %d" % (tag, start))


def find(h, needle, after=0):
    i = h.find(needle, after)
    if i < 0:
        raise SystemExit("ipo-details: not found: %s" % needle[:80])
    return i


def swap(h, old, new, count=1):
    if h.count(old) != count:
        raise SystemExit("ipo-details: expected %d of %r, found %d" % (count, old[:80], h.count(old)))
    return h.replace(old, new)


def production(cls):
    """A production <section> from beta's server-rendered IPO page, by class."""
    s = open(SSR, encoding="utf-8").read()
    i = find(s, '<section class="%s' % cls)
    return s[i:element(s, i)]


# ------------------------------------------------------------------ blocks

def hero(h):
    a = find(h, '<header class="b7-hc"')
    old = h[a:element(h, a)]
    new = re.sub(r'<img src="[^"]*" alt="[^"]*logo" width="76" height="76">',
                 '<img src="%s" alt="%s logo" width="76" height="76">' % (LOGO, NAME), old)
    new = swap(new, '<h1 id="b7-name">Mahaveer</h1><p>Senior Secured Bond</p>', '<h1 id="b7-name">%s</h1>' % NAME)
    new = swap(new, 'Sell Anytime</span>', 'IPO Live</span>')
    new, n = re.subn(r'<button type="button" class="b7-hc__save" aria-label="Add to watchlist">.*?</button>',
                     '<button type="button" class="b7-hc__save" aria-label="Share"><img src="../assets/beta/media/'
                     'share-action-desktop.2j-atjt_xvh2t.svg" alt="" width="40" height="40"></button>', new, flags=re.S)
    if n != 1:
        raise SystemExit("ipo-details: hero action not found")
    # Four stats, as in bond-details7. Beta's fifth, Issue Size, reads "--" for this issue.
    stats = [("Coupon upto", "10%", "stat-returns.png", "width:54px;height:36px;left:-11px;top:0px"),
             ("Min Investment", "₹10,000", "proof-money.png", "width:36px;height:30px;left:0px;top:3px"),
             ("Credit Rating", "ICRA A", "stat-rating.png", "width:36px;height:24px;left:0px;top:6px"),
             ("Security", "Secured", "stat-security.png", "width:36px;height:24px;left:0px;top:6px")]
    div = '<span class="b7-hc__div" aria-hidden="true"></span>'
    cells = div.join(
        '<div class="b7-stat"><span class="b7-stat__ico" aria-hidden="true"><img src="../assets/img/bd5/%s" alt="" style="%s">'
        '</span><dl><dt>%s</dt><dd>%s</dd></dl></div>' % (img, st, k, v) for k, v, img, st in stats)
    a2 = find(new, '<div class="b7-hc__stats">')
    new = new[:a2] + '<div class="b7-hc__stats">%s</div>' % cells + new[element(new, a2):]
    new, n = re.subn(r'<p class="b7-sold">.*?</p>',
                     '<p class="b7-sold"><i class="b7-dot b7-sold__dot" aria-hidden="true"></i><span class="b7-sold__d">Subscribed 0%</span>'
                     '<span class="b7-sold__m">Subscribed 0%</span><span class="b7-sold__segs" role="progressbar" aria-valuemin="0" '
                     'aria-valuemax="100" aria-valuenow="0" aria-label="Subscribed 0%">' + "<i></i>" * 12 + '</span></p>', new, flags=re.S)
    if n != 1:
        raise SystemExit("ipo-details: sold meter not found")
    new = swap(new, 'Form 121 Available</span>', 'Closes on 9-Oct-2026</span>')
    return h.replace(old, new, 1)


def drop_highlights(h):
    a = h.rfind('<div class="b4 b5 b5-embed">', 0, find(h, '<section class="b7-hl"'))
    return h[:a] + h[element(h, a):]


def series_and_cashflow(h):
    """The bond's Cashflow card goes; production's Popular IPO Series and IPO Series take its place, above the
    phone calculator (production shows the calculator after the series on phones)."""
    a = find(h, '<div class="gp-expand is-open b7-peek')
    h = h[:a] + h[element(h, a):]
    mobile_calc = find(h, '<div class="block lg:hidden"><section aria-labelledby="bond-cashflow-sidebar-title-mobile">')
    blocks = ("<!-- Production markup (beta SSR), Series V selected as production loads it. -->"
              + production("ipo-surface-card ipo-series-cards") + production("ipo-surface-card ipo-series-table"))
    return h[:mobile_calc] + blocks + h[mobile_calc:]


def calculator(h):
    h = swap(h, 'value="1" style=""><span class="b7-unit">Unit</span>', 'value="10" style=""><span class="b7-unit">Units</span>', 2)
    h = swap(h, '12.00% YTM</span>', '10% YTM</span>', 2)
    h = swap(h, '+ <!-- -->₹ 1,740.31</dd>', '+ <!-- -->₹ 4,785</dd>', 2)
    h, n1 = re.subn(r'(class="bond-cashflow-sidebar__label">Investment Amount</dt><dd class="bond-cashflow-sidebar__value">)₹ 9,368\.14',
                    r'\g<1>₹ 10,000', h)
    h, n2 = re.subn(r'(<dd class="bond-cashflow-sidebar__value bond-cashfl[^"]*">)₹ 11,108\.45', r'\g<1>₹ 14,785', h)
    if (n1, n2) != (2, 2):
        raise SystemExit("ipo-details: calculator amounts %d/%d" % (n1, n2))
    # The two "i" buttons open bond-only explainers; Cashflow Timeline is the bond's schedule.
    h, n = re.subn(r'<button type="button" class="inline-flex shrink-0 cursor-pointer[^"]*" aria-label="Total (?:Returns|Receivable)"'
                   r'[^>]*>.*?</button>', "", h, flags=re.S)
    if n != 4:
        raise SystemExit("ipo-details: expected 4 calculator info buttons, found %d" % n)
    h, n = re.subn(r'<button class="gp-btn[^"]*bond-cashflow-sidebar__timeline-btn" type="button">Cashflow Timeline<svg.*?</svg></button>',
                   "", h, flags=re.S)
    if n != 2:
        raise SystemExit("ipo-details: expected 2 Cashflow Timeline buttons, found %d" % n)
    h = swap(h, 'bond-cashflow-sidebar__invest-btn" type="button">Invest Now<', 'bond-cashflow-sidebar__invest-btn" type="button">Apply IPO<', 2)
    # Production's series line under the stepper, and its allocation notice under the card.
    h, n = re.subn(r'(<span class="b7-unit">Units</span></label><button[^>]*>.*?</button></div>)',
                   r'\1<p class="ipo-returns-calculator__series-info">Series V | 9.57% | Monthly | 60 Months</p>', h, flags=re.S)
    if n != 2:
        raise SystemExit("ipo-details: stepper not found (%d)" % n)
    notice = ('<aside class="ipo-fcfs-notice" aria-label="Allocation notice"><span class="ipo-fcfs-notice__icon-wrap" aria-hidden="true">'
              '<img alt="" width="20" height="20" src="../assets/beta/media/ipo-info.3ylkoosekh2u8.svg"></span>'
              '<p class="ipo-fcfs-notice__text">NCD IPOs are allocated on first come first serve basis</p></aside>')
    out, k = [], 0
    for m in re.finditer(r'<section aria-labelledby="bond-cashflow-sidebar-title-(?:mobile|desktop)">', h):
        end = element(h, m.start())
        out.append(h[k:end] + notice)
        k = end
    if len(out) != 2:
        raise SystemExit("ipo-details: expected 2 calculator sections, found %d" % len(out))
    return "".join(out) + h[k:]


def about(h):
    a = find(h, '<div data-testid="bond-about-issuer">')
    b = element(h, a)
    blk = h[a:b]
    for kind in ("desktop", "mobile"):
        m = re.search(r'(<dl class="m-0 about-issuer__facts--ncd-%s[^"]*"[^>]*>)<div class="([^"]*)">.*?</dl>' % kind, blk, re.S)
        if not m:
            raise SystemExit("ipo-details: about facts (%s) not found" % kind)
        facts = "".join('<div class="%s"><dt class="about-issuer__fact-label">%s</dt><dd class="about-issuer__fact-value">%s</dd></div>'
                        % (m.group(2), k, v) for k, v in FACTS)
        blk = blk.replace(m.group(0), m.group(1) + facts + "</dl>", 1)
    c = find(blk, '<div class="about-issuer__content')
    blk = blk[:c] + re.match(r"<div[^>]*>", blk[c:]).group(0) + ABOUT + "</div>" + blk[element(blk, c):]
    return h[:a] + blk + h[b:]


def strengths(h):
    a = find(h, '<div data-testid="bond-strength-weaknesses">')
    b = element(h, a)
    blk = h[a:b]
    lists = list(re.finditer(r'(<ol class="strengths-weaknesses__ncd-factor-l[^"]*">)<li class="([^"]*)"><span class="([^"]*)" aria-hidden="true">01</span>'
                             r'<p class="([^"]*)">.*?</ol>', blk, re.S))
    if len(lists) != 2:
        raise SystemExit("ipo-details: expected 2 strength lists, found %d" % len(lists))
    for m, items in reversed(list(zip(lists, (STRENGTHS, WATCH)))):
        li = "".join('<li class="%s"><span class="%s" aria-hidden="true">%02d</span><p class="%s">%s</p></li>'
                     % (m.group(2), m.group(3), k + 1, m.group(4), t) for k, t in enumerate(items))
        blk = blk[:m.start()] + m.group(1) + li + "</ol>" + blk[m.end():]
    return h[:a] + blk + h[b:]


def financials(h):
    a = find(h, '<div data-testid="bond-company-financials" class="f3">')
    return h[:a] + B.fin_v3(FIN, "FY 2024-25", "", RATIOS) + h[element(h, a):]


def documents(h):
    a = find(h, '<div data-testid="bond-documents">')
    b = element(h, a)
    blk = h[a:b]
    c = find(blk, '<p class="bond-documents-action-card__info-b')
    blk = (blk[:c] + re.match(r"<p[^>]*>", blk[c:]).group(0)
           + 'You can submit your Form 121 to the registrar and debenture trustee of the bond to avoid the Tax deduction. '
             '<a href="%s" target="_blank" rel="noopener noreferrer">Download Form</a></p>' % FORM_URL + blk[element(blk, c):])
    blk, n1 = re.subn(r'href="https://storage\.googleapis\.com/[^"]*\.pdf"', 'href="%s"' % IM_URL, blk, count=1)
    blk, n2 = re.subn(r'href="https://www\.careratings\.com/[^"]*"', 'href="%s"' % RATING_URL, blk, count=1)
    if (n1, n2) != (1, 1):
        raise SystemExit("ipo-details: document links %d/%d" % (n1, n2))
    blk = swap(blk, "Rating Date • 19-May-2026", "Rating Date • 14-Sep-2026")

    # Production's IPO Documents carry the issuer facts; bond-details7's Other Bond Details grid shows them.
    def dfield(k, v, sub=None, full=False):
        return ('<div class="bond-documents-desktop-field%s"><p class="bond-documents-desktop-field__label">%s</p>'
                '<p class="bond-documents-desktop-field__value">%s</p>%s</div>' % (
                    " bond-documents-desktop-field--full" if full else "", k, v,
                    '<p class="bond-documents-desktop-field__label">%s</p>' % sub if sub else ""))

    def mrow(*fields, stacked=False):
        cells = "".join('<div class="bond-documents-mobile-field%s"><p class="bond-documents-mobile-field__label">%s</p>'
                        '<p class="bond-documents-mobile-field__value">%s</p>%s</div>' % (
                            " bond-documents-mobile-field--full" if stacked else "", k, v,
                            '<p class="bond-documents-mobile-field__label">%s</p>' % sub if sub else "") for k, v, sub in fields)
        return ('<div class="bond-documents-mobile-row"><div class="bond-documents-mobile-row__fields%s">%s</div></div>'
                % (" bond-documents-mobile-row__fields--stacked" if stacked else "", cells))

    facts = ('<div class="bond-documents-subsection-block"><div class="bond-documents-mobile-grid">'
             + mrow(("Issuer Name", NAME, None), stacked=True)
             + mrow(("Face Value", "₹1,000", None), ("Mode of Issue", "Public Placement", None))
             + mrow(("Trustee Details", TRUSTEE[0], TRUSTEE[1]), stacked=True)
             + mrow(("Registrar Details", REGISTRAR[0], REGISTRAR[1]), stacked=True)
             + '</div><div class="bond-documents-desktop-grid">'
             + dfield("Issuer Name", NAME, full=True) + dfield("Face Value", "₹1,000") + dfield("Mode of Issue", "Public Placement")
             + '<div class="col-span-4"><div class="bond-documents-divider" aria-hidden="true"></div></div>'
             + dfield("Trustee Details", TRUSTEE[0], TRUSTEE[1], full=True)
             + dfield("Registrar Details", REGISTRAR[0], REGISTRAR[1], full=True)
             + '</div></div><div class="bond-documents-divider" aria-hidden="true"></div>')
    blk = swap(blk, '<div class="bond-documents-panel">', '<div class="bond-documents-panel">' + facts)
    h = h[:a] + blk + h[b:]
    # Other Bond Details is the bond's own sheet: the whole card goes.
    i = find(h, '<h3 class="sr-only">Other Bond Details')
    card = h.rfind('<div class="gp-expand gp-expand--card', 0, i)
    h = h[:card] + h[element(h, card):]
    return h


def invest_bar(h):
    a = find(h, 'aria-label="Investment summary"')
    bar = h[a:find(h, "</aside>", a)]
    new = swap(bar, ">₹ 9,368.14</span>", ">₹ 10,000</span>")
    new = re.sub(r'<p class="m-0 inline-flex items-center gap-1\.5">.*?</p>', "", new, count=1, flags=re.S)
    new = swap(new, 'type="button">Invest Now<', 'type="button">Apply IPO<')
    return h.replace(bar, new, 1)


def chrome(h):
    h = re.sub(r"<title>.*?</title>", "<title>SMC Global Securities Limited NCD IPO | GoldenPi</title>", h, count=1, flags=re.S)
    h = re.sub(r'<meta name="description" content="[^"]*">',
               '<meta name="description" content="SMC Global Securities Limited NCD IPO: series, coupon, returns, issuer financials and documents.">',
               h, count=1)
    h = re.sub(r"<!-- Generated by pages/_bond_v7\.py.*?-->",
               "<!-- Generated by pages/_ipo_details.py from bond-details7.html (blocks) and beta's SMC IPO page (content, "
               "series blocks); do not edit. -->", h, count=1, flags=re.S)
    h = swap(h, 'href="corporate-bonds.html">Bonds</a>', 'href="bond-ipo-online.html">NCD IPO</a>')
    h, n = re.subn(r'(aria-current="page">)MAHAVEER(</li>)', r"\g<1>%s\2" % NAME, h, count=1)
    if n != 1:
        raise SystemExit("ipo-details: breadcrumb not found")
    # Phone toolbar: production has Share where the bond page has Add to watchlist.
    h, n = re.subn(r'<button type="button" class="bond-header-action-trigger" aria-label="Add to watchlist" aria-pressed="false">'
                   r'<img([^>]*?)src="[^"]*"([^>]*)></button>',
                   r'<button type="button" class="bond-header-action-trigger" aria-label="Share"><img\1src="../assets/beta/media/'
                   r'share-action-mobile.16f54imqsowrz.svg"\2></button>', h, count=1)
    if n != 1:
        raise SystemExit("ipo-details: phone toolbar not found")
    a = find(h, '<div id="cashflow-modal" hidden>')
    h = h[:a] + h[element(h, a):]
    # ...and the script lines that open it (the accordion handlers in the same script stay).
    h, n = re.subn(r"\n  var modal = document\.getElementById\('cashflow-modal'\);.*?if \(e\.key === 'Escape'\) show\(false\); \}\);",
                   "", h, count=1, flags=re.S)
    if n != 1:
        raise SystemExit("ipo-details: cashflow modal script not found")
    style = ('<link rel="stylesheet" href="../assets/beta/ipo.css">\n<style>\n'
             '/* Production sizes the three series cards for its 870px column; bond-details7\'s column is\n'
             '   narrower, so on desktop they share its width instead of running past the card. */\n'
             '@media (min-width: 1024px) { .ipo-series-cards__track > .ipo-series-card { flex: 1 1 0; min-width: 0; } }\n'
             '</style>\n')
    return h.replace("</head>", style + "</head>", 1)


def main():
    h = open(SRC, encoding="utf-8").read()
    for step in (chrome, hero, drop_highlights, series_and_cashflow, calculator, about, strengths, financials, documents, invest_bar):
        h = step(h)
    body = h[h.index("<main"):h.index("</main>")]
    for stale in ("Mahaveer", "MAHAVEER", "9,368.14", "11,108.45", "Invest Now"):
        if stale in body:
            print("note: %d x %r left in <main>" % (body.count(stale), stale))
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(h)
    print("ipo-details.html  %d bytes" % len(h))


if __name__ == "__main__":
    main()
