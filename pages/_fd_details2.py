#!/usr/bin/env python3
"""fd-details2.html: the Unity Small Finance Bank FD page, new version, from the
user's Figma (HRSMFFccdLgqf1YwD7oyc9, node 138:579), on user-explore-app7's
shell (final navbar, FD current) and language.

Left (70%): the dark header card, Popular Tenures, All Available Tenures,
Reason to Invest, and the SBI comparison. Right (30%): the calculator, sticky.
Then the FAQ beside Need Help, and the scan-to-download card.

Content: content/beta_fixed-deposits_GPID105192_unity.md (captured 2026-10-08).
Where the Figma frame holds placeholders (an Indel breadcrumb, Akara FAQs, 6.50%
rows, "24M - 36M", "Top PSU Banks 6.00%", "₹3.8 Lac Cr AUM", "Number of
Investors"), the captured Unity values are used instead. Design-only copy kept:
"Reason to Invest", "Invest With Confidence / Ease", "Instant Booking", "No New
Bank A/C", "Flexible Tenures".

The calculator opens on the captured figures (₹1,00,000 at 8.50% for 1Y 4M 16D
gives ₹12,280.83) and recomputes live with quarterly compounding over the
tenure's days / 365.25, within ₹0.30 of that figure; production's own formula
should replace it when wired.

    python3 pages/_fd_details2.py
"""
import os
import re

import _explore_app as X
import _explore_app2 as A
import _explore_app7 as S

OUT = os.path.join(X.HERE, "fd-details2.html")
IMG = "../assets/img/"
R = "&#8377;"

# -------------------------------------------------------------------- data
# (tenure, payout, regular, senior, badge, years, months, days) from the capture.
TENURES = [("1Y 4M 16D", "On Maturity", "8.00", "8.50", "Highest Rate", 1, 4, 16),
           ("1Y 4M 16D", "Monthly", "8.00", "8.50", "", 1, 4, 16),
           ("1Y", "On Maturity", "7.50", "8.00", "", 1, 0, 0),
           ("1Y", "Quarterly", "7.50", "8.00", "", 1, 0, 0),
           ("5Y", "On Maturity", "6.75", "7.25", "", 5, 0, 0),
           ("6M 1D", "On Maturity", "6.25", "6.75", "", 0, 6, 1),
           ("7D", "On Maturity", "4.00", "4.00", "Short Term", 0, 0, 7)]
POPULAR = [(0, "Highest Return"), (6, "Lowest Tenure")]   # rows of TENURES
FAQS = None  # read from the capture in faq()


def capture():
    with open(os.path.join(X.ROOT_DIR, "content", "beta_fixed-deposits_GPID105192_unity.md"), encoding="utf-8") as f:
        return f.read()


def check(c):
    for s in ("UNITY SMALL FINANCE BANK", "Returns Upto", "8.50%", "Withdraw Anytime", "Popular Tenures", "Highest Return",
              "Lowest Tenure", "All Available Tenures", "Sr. Citizen", "Highest Rate", "Short Term",
              "State Bank of India vs Unity Small Finance Bank", "7.20%", "18.06% Higher",
              "Comparison of highest returns across all tenures and age groups", "Equal RBI Protection",
              "DICGC Insurance Upto ₹5 Lacs for both State Bank of India & Unity Small Finance Bank",
              "About Unity Small Finance Bank", "Investor coverage from 334 locations across India",
              "Start investing with just ₹1,000", "BharatPe & Centrum Group", "Physical Branches", "~400",
              "Customer Base", "18+ Lakh", "Total Deposits", "11,000+ Crore", "Investment Amount",
              "Interest Rate & Tenure", "Senior Citizen", "₹ 1,00,000", "₹ 12,280.83", "₹ 1,12,280.83", "Invest Now",
              "Insured by DICGC (Owned by RBI)", "By proceeding, I agree to the Terms & Conditions", "Need Help",
              "Talk to our Support Team for free. We will help you through your investment journey.", "Contact Us"):
        if s not in c:
            raise SystemExit("not in the capture any more, re-check: %r" % s)
    for t, p, reg, sr, _b, *_ in TENURES:
        if not re.search(r"%s\n%s\n%s%%\n%s%%" % (re.escape(t), p, reg, sr), c):
            raise SystemExit("tenure row changed: %s %s" % (t, p))


# ------------------------------------------------------------------ blocks
def breadcrumb():
    return ('<nav class="f2-crumb" aria-label="Breadcrumb"><a href="user-explore.html">Home</a><span aria-hidden="true">&rsaquo;</span>'
            '<a href="user-fixed-deposits-app2.html">Fixed Deposits</a><span aria-hidden="true">&rsaquo;</span>'
            '<span aria-current="page">Unity Small Finance Bank</span></nav>')


def hero():
    fact = '<div class="f2-hero__fact"><img src="%s" alt="" width="32" height="32"><dl><dt>%s</dt><dd>%s</dd></dl></div>'
    return ('<section class="f2-hero" aria-labelledby="f2-name">'
            '<div class="f2-hero__top"><img class="f2-hero__logo" src="%sGPID105192.Unity.png" alt="" width="80" height="80">'
            '<h1 id="f2-name">Unity Small Finance Bank</h1>'
            '<span class="f2-hero__chip"><i aria-hidden="true"></i>Withdraw Anytime</span>'
            '<button type="button" class="f2-hero__share" aria-label="Share this FD" data-f2-share><img src="%sshare-icon.svg" alt="" width="18" height="18"></button></div>'
            '<div class="f2-hero__facts">%s%s%s</div></section>'
            % (IMG, IMG,
               fact % (IMG + "fd-details2/returns-coins.png", "Returns Upto", "8.50%"),
               fact % (IMG + "fd-details2/tenure-calendar.png", "Tenure", "7D - 5Y"),
               fact % (IMG + "fd-details2/dicgc-shield.png", "RBI&rsquo;s DICGC Insurance Upto", R + "5 Lacs")))


def popular():
    cards = ""
    for k, (row, label) in enumerate(POPULAR):
        t, p, reg, sr, *_ = TENURES[row]
        cards += ('<label class="f2-pop__card f2-pop__card--%d"><input type="radio" name="f2-pop" value="%d"%s>'
                  '<span class="f2-pop__rate">%s%%</span><span class="f2-pop__meta">%s &middot; %s</span>'
                  '<span class="f2-pop__tag">%s</span></label>' % (k, row, " checked" if k == 0 else "", sr, t, p, label))
    return ('<section class="f2-card f2-pop" aria-labelledby="f2-pop-t"><h2 id="f2-pop-t">Popular Tenures</h2>'
            '<div class="f2-pop__grid" role="radiogroup" aria-labelledby="f2-pop-t">%s</div></section>' % cards)


def all_tenures():
    rows = ""
    for k, (t, p, reg, sr, badge, *_) in enumerate(TENURES):
        b = '<span class="f2-badge f2-badge--%s">%s</span>' % ("hi" if badge == "Highest Rate" else "short", badge) if badge else ""
        rows += ('<tr%s><td><label><input type="radio" name="f2-row" value="%d"%s><span>%s<small class="f2-all__p">%s</small></span></label></td>'
                 '<td>%s</td><td class="f2-rate">%s%%</td><td class="f2-rate">%s%%%s</td></tr>'
                 % (' class="is-on"' if k == 0 else "", k, " checked" if k == 0 else "", t, p, p, reg, sr, b))
    return ('<section class="f2-card f2-all" aria-labelledby="f2-all-t"><h2 id="f2-all-t">All Available Tenures</h2>'
            '<div class="f2-all__scroll"><table><thead><tr><th scope="col">Tenure<span class="f2-all__p"> / Payout</span></th><th scope="col">Payout</th>'
            '<th scope="col">Regular</th><th scope="col">Sr. Citizen</th></tr></thead><tbody>%s</tbody></table></div></section>' % rows)


def reasons():
    tile = ('<li class="f2-why__tile f2-why__tile--%s"><div><h3>%s</h3><ul>%s</ul></div>'
            '<img src="%s" alt="" width="84" height="84" loading="lazy"></li>')
    li = lambda items: "".join("<li>%s</li>" % i for i in items)
    return ('<section class="f2-card f2-why" aria-labelledby="f2-why-t"><h2 id="f2-why-t">Reason to Invest</h2><ul class="f2-why__grid">%s%s</ul></section>'
            % (tile % ("conf", "Invest With Confidence", li(["~400 Physical Branches", "18+ Lakh Customer Base", "11,000+ Crore Total Deposits"]),
                       IMG + "bd5/tile-shield.png"),
               tile % ("ease", "Invest With Ease", li(["Instant Booking", "No New Bank A/C", "Flexible Tenures"]),
                       IMG + "bd5/tile-clock.png")))


def compare():
    return ('<section class="f2-cmp" aria-labelledby="f2-cmp-t">'
            '<h2 id="f2-cmp-t">State Bank of India <span class="f2-cmp__vs">vs</span> <span class="f2-cmp__us">Unity Small Finance Bank</span></h2>'
            '<div class="f2-cmp__chart" role="img" aria-label="Highest returns: State Bank of India 7.20%%, Unity Small Finance Bank 8.50%%, 1.30%% extra">'
            '<div class="f2-cmp__col"><b>7.20%%</b><span class="f2-cmp__bar f2-cmp__bar--them"><img src="%sportfolio/bank.png" alt="" width="48" height="48"></span>'
            '<span class="f2-cmp__name">State Bank of India</span></div>'
            '<div class="f2-cmp__gain" aria-hidden="true"><span class="f2-cmp__pill">+1.30%% Extra</span>'
            '<svg viewBox="0 0 200 90" preserveAspectRatio="none"><path d="M4 86 C 70 70, 120 30, 192 8" fill="none" stroke="#f4e3a6" stroke-width="2"/>'
            '<path d="M182 4 L194 7 L186 16" fill="none" stroke="#f4e3a6" stroke-width="2"/></svg></div>'
            '<div class="f2-cmp__col f2-cmp__col--us"><b>8.50%%</b><span class="f2-cmp__bar f2-cmp__bar--us"><img src="%sGPID105192.Unity.png" alt="" width="44" height="44"></span>'
            '<span class="f2-cmp__name">Unity Small Finance Bank</span></div></div>'
            '<div class="f2-cmp__cards"><div><h3>Equal RBI <span>Protection</span></h3><ul>'
            '<li>DICGC Insurance Upto %s5 Lacs for both State Bank of India &amp; Unity Small Finance Bank</li></ul></div>'
            '<div><h3>About Unity Small Finance Bank</h3><ul><li>Investor coverage from 334 locations across India</li>'
            '<li>Start investing with just %s1,000</li><li>Founded By BharatPe &amp; Centrum Group</li></ul></div></div>'
            '<p class="f2-cmp__note">Comparison of highest returns across all tenures and age groups</p></section>'
            % (IMG, IMG, R, R))


def calc():
    opts = "".join('<option value="%d"%s>%s &middot; %s</option>' % (k, " selected" if k == 0 else "", t, p)
                   for k, (t, p, *_r) in enumerate(TENURES))
    return ('<!-- DATA: defaults as captured (₹1,00,000, 1Y 4M 16D, Senior Citizen rate 8.50%%). Recomputed live with an\n'
            '     approximation of production\'s formula; wire production\'s own when building. -->'
            '<section class="f2-card f2-calc" id="f2-calc" aria-labelledby="f2-calc-t"><h2 id="f2-calc-t" class="sr-only">FD returns calculator</h2>'
            '<label class="f2-field"><span>Investment Amount</span><span class="f2-input"><span aria-hidden="true">%s</span>'
            '<input id="f2-amt" type="text" inputmode="numeric" value="1,00,000" aria-label="Investment Amount in rupees"></span></label>'
            '<label class="f2-field"><span>Interest Rate &amp; Tenure</span><select id="f2-ten">%s</select></label>'
            '<label class="f2-switch"><input type="checkbox" id="f2-sr" checked><span class="f2-switch__ui" aria-hidden="true"></span>Senior Citizen</label>'
            '<dl class="f2-out" aria-live="polite"><div><dt>Interest Rate</dt><dd id="f2-rate">8.50%%</dd></div>'
            '<div><dt>Investment Amount</dt><dd id="f2-inv">%s 1,00,000</dd></div>'
            '<div><dt>Interest Earned</dt><dd id="f2-int" class="f2-gain">%s 12,280.83</dd></div>'
            '<div><dt>Maturity Amount</dt><dd id="f2-mat" class="f2-gain">%s 1,12,280.83</dd></div></dl>'
            '<button type="button" class="f2-cta">Invest Now <img src="%sportfolio/arrow.svg" alt="" width="16" height="16"></button>'
            '<p class="f2-insured"><img src="%sportfolio/check-green.svg" alt="" width="14" height="14">Insured by DICGC (Owned by RBI)</p>'
            '<p class="f2-terms">By proceeding, I agree to the <a href="terms-and-conditions.html">Terms &amp; Conditions</a></p></section>'
            % (R, opts, R, R, R, IMG, IMG))


def faq(c):
    body = c[c.index("Frequently asked questions\n") + len("Frequently asked questions\n"):c.index("\nNeed Help\n")]
    lines = [l for l in body.split("\n") if l.strip()]
    pairs = list(zip(lines[0::2], lines[1::2]))
    items = "".join('<details class="f2-faq__item"%s><summary>%s</summary><p>%s</p></details>'
                    % (" open" if k == 0 else "", A.esc(q), A.esc(a)) for k, (q, a) in enumerate(pairs))
    return ('<section class="f2-card f2-faq" aria-labelledby="f2-faq-t"><h2 id="f2-faq-t">Frequently asked questions</h2>%s</section>'
            % items)


def help_card():
    return ('<section class="f2-card f2-help" aria-labelledby="f2-help-t">'
            '<img src="../assets/beta/media/support-icon.1ehk__1qamba-.svg" alt="" width="160" height="160" loading="lazy">'
            '<h2 id="f2-help-t"><img src="%sphone-icon.svg" alt="" width="18" height="18">Need Help</h2>'
            '<p>Talk to our Support Team for free. We will help you through your investment journey.</p>'
            '<a class="f2-cta f2-cta--sm" href="contact-us.html">Contact Us <img src="%sportfolio/arrow.svg" alt="" width="14" height="14"></a></section>'
            % (IMG, IMG))


def body():
    c = capture()
    check(c)
    return ('<main id="main-content" class="xa-page"><div class="f2">%s'
            '<div class="f2-a">%s%s</div><aside class="f2-side" aria-label="Calculator">%s</aside>'
            '<div class="f2-b">%s%s%s</div><div class="f2-q">%s</div><aside class="f2-h" aria-label="Help">%s</aside>'
            '<div class="f2-app">%s</div></div></main>'
            % (breadcrumb(), hero(), popular(), calc(), all_tenures(), reasons(), compare(), faq(c), help_card(), S.app_card()))


STYLE = """
/* fd-details2: Figma 138:579 on app7's shell. */
.f2 { display: grid; gap: 24px; max-width: 1180px; margin: 0 auto; padding: 16px 20px 64px;
  grid-template-columns: minmax(0, 79fr) minmax(0, 36fr); column-gap: 30px;
  grid-template-areas: "crumb crumb" "a side" "b side" "q h" "app ."; align-items: start; }
.f2 > nav { grid-area: crumb; } .f2-a { grid-area: a; } .f2-b { grid-area: b; } .f2-side { grid-area: side; align-self: stretch; }
.f2-q { grid-area: q; } .f2-h { grid-area: h; } .f2-app { grid-area: app; }
.f2-a, .f2-b { display: grid; gap: 24px; min-width: 0; }
.f2-side .f2-calc { position: sticky; top: 96px; }
.f2-crumb { display: flex; gap: 8px; font-size: 12px; color: var(--sub); }
.f2-crumb a { color: var(--sub); text-decoration: none; } .f2-crumb a:hover { color: #322811; }
.f2-crumb [aria-current] { color: #322811; font-weight: 500; }
.f2-card { padding: 24px; border-radius: 24px; background: #fff; border: 1px solid rgba(231, 227, 217, .6); }
.f2-card h2, .f2-why h2 { margin: 0 0 18px; font-size: 18px; line-height: 1.3; font-weight: 600; color: #322811; }

/* header card */
.f2-hero { display: grid; gap: 22px; padding: 24px 28px; border-radius: 24px; color: #fff; overflow: hidden;
  background: radial-gradient(420px 160px at 100% 100%, rgba(52, 84, 196, .55), transparent 70%), linear-gradient(180deg, #050506 0%, #0b0f1d 100%); }
.f2-hero__top { display: flex; align-items: center; gap: 20px; }
.f2-hero__logo { flex: none; width: 80px; height: 80px; border-radius: 50%; }
.f2-hero h1 { margin: 0; flex: 1; min-width: 0; font-size: 26px; line-height: 1.25; font-weight: 500; color: #fff; }
.f2-hero__chip { display: inline-flex; align-items: center; gap: 8px; height: 40px; padding: 0 16px; border-radius: 999px; white-space: nowrap;
  border: 1px solid rgba(255, 255, 255, .14); background: rgba(255, 255, 255, .04); color: #edc967; font-size: 14px; font-weight: 500; }
.f2-hero__chip i { width: 7px; height: 7px; border-radius: 50%; background: #22c55e; }
.f2-hero__share { flex: none; display: grid; place-items: center; width: 40px; height: 40px; padding: 0; border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, .18); background: none; cursor: pointer; }
.f2-hero__share img { filter: brightness(0) invert(1); }
.f2-hero__share:focus-visible { outline: 2px solid #edc967; outline-offset: 2px; }
.f2-hero__facts { display: flex; flex-wrap: wrap; gap: 16px 28px; }
.f2-hero__fact { display: flex; align-items: center; gap: 10px; }
.f2-hero__fact + .f2-hero__fact { padding-left: 28px; border-left: 1px solid rgba(255, 255, 255, .14); }
.f2-hero__fact img { width: 32px; height: 32px; object-fit: contain; }
.f2-hero__fact:first-child img { object-fit: cover; }  /* Figma crops the coins' 3:2 image to a square */
.f2-hero__fact dl { margin: 0; } .f2-hero__fact dt { font-size: 14px; color: rgba(255, 255, 255, .75); }
.f2-hero__fact dd { margin: 2px 0 0; font-size: 16px; font-weight: 600; }

/* popular tenures */
.f2-pop__grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 22px; }
.f2-pop__card { position: relative; display: grid; gap: 8px; padding: 20px 20px 0; border-radius: 14px; border: 1px solid #e7e3d9;
  overflow: hidden; cursor: pointer; transition: border-color .2s ease, box-shadow .2s ease; }
.f2-pop__card input { position: absolute; top: 22px; right: 20px; width: 18px; height: 18px; margin: 0; accent-color: #c69a1c; }
.f2-pop__card:has(input:checked) { border-color: #c69a1c; box-shadow: 0 0 0 1px #c69a1c inset; }
.f2-pop__card:has(input:focus-visible) { outline: 2px solid #d4af37; outline-offset: 2px; }
.f2-pop__rate { font-size: 30px; line-height: 1.1; font-weight: 500; color: #322811; font-variant-numeric: tabular-nums; }
.f2-pop__meta { font-size: 12px; color: #4a4336; }
.f2-pop__tag { margin: 14px -20px 0; padding: 8px; text-align: center; font-size: 13px; font-weight: 500; }
.f2-pop__card--0 .f2-pop__tag { background: #fbefc8; color: #a67c00; }
.f2-pop__card--1 .f2-pop__tag { background: #e3edfb; color: #2c5aa0; }

/* all tenures */
.f2-all__scroll { overflow-x: auto; }
.f2-all table { width: 100%; border-collapse: separate; border-spacing: 0 4px; font-size: 14px; }
.f2-all th { padding: 0 16px 14px; text-align: left; font-size: 13px; font-weight: 500; color: #322811; border-bottom: 1px solid #ece8de; }
.f2-all td { padding: 14px 16px; color: #4a4336; white-space: nowrap; }
.f2-all td:first-child { border-radius: 14px 0 0 14px; } .f2-all td:last-child { border-radius: 0 14px 14px 0; }
.f2-all tr.is-on td { background: #f5f3ee; }
.f2-all label { display: flex; align-items: center; gap: 22px; font-weight: 500; color: #322811; cursor: pointer; }
.f2-all input { width: 18px; height: 18px; margin: 0; accent-color: #c69a1c; }
.f2-all input:focus-visible { outline: 2px solid #d4af37; outline-offset: 2px; }
.f2-all__p { display: none; }
.f2-rate { color: #a67c00 !important; font-weight: 500; font-variant-numeric: tabular-nums; }
.f2-badge { margin-left: 10px; padding: 2px 10px; border-radius: 999px; font-size: 11px; font-weight: 500; }
.f2-badge--hi { background: #fbefc8; color: #8a6520; } .f2-badge--short { background: #e3f7ea; color: #1f8a4c; }

/* reason to invest */
.f2-why__grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; margin: 0; padding: 0; list-style: none; }
.f2-why__tile { display: flex; justify-content: space-between; gap: 12px; padding: 20px; border-radius: 16px; }
.f2-why__tile--conf { background: #e8f7ee; } .f2-why__tile--ease { background: #fff1e8; }
.f2-why__tile h3 { margin: 0 0 12px; font-size: 13px; font-weight: 500; color: #7a571f; }
.f2-why__tile ul { display: grid; gap: 10px; margin: 0; padding: 0; list-style: none; }
.f2-why__tile li { position: relative; padding-left: 18px; font-size: 14px; font-weight: 600; color: #322811; }
.f2-why__tile li::before { content: ""; position: absolute; left: 0; top: 6px; width: 7px; height: 7px; border-radius: 50%; background: #22c55e; }
.f2-why__tile img { flex: none; width: 84px; height: 84px; object-fit: contain; }

/* comparison */
.f2-cmp { display: grid; gap: 28px; padding: 32px 36px 28px; border-radius: 24px; background: #0e0f12; color: #fff; }
.f2-cmp h2 { margin: 0; font-size: 26px; line-height: 1.25; font-weight: 600; color: #f1f1f1; }
.f2-cmp__vs { font-size: 16px; color: rgba(255, 255, 255, .5); } .f2-cmp__us { color: #edc967; }
.f2-cmp__chart { position: relative; display: grid; grid-template-columns: 1fr 180px 1fr; align-items: end; max-width: 560px; width: 100%;
  margin: 0 auto; padding-bottom: 0; border-bottom: 1px solid rgba(255, 255, 255, .25); }
.f2-cmp__col { display: grid; justify-items: center; gap: 12px; }
.f2-cmp__col b { font-size: 20px; font-weight: 600; } .f2-cmp__col--us b { color: #edc967; }
.f2-cmp__bar { display: grid; place-items: center; width: 110px; border-radius: 10px 10px 0 0; }
.f2-cmp__bar--them { height: 126px; background: linear-gradient(180deg, #3b3423, #16130c); border: 1px solid rgba(237, 201, 103, .3); border-bottom: 0; }
.f2-cmp__bar--them img { width: 48px; height: 48px; object-fit: contain; }
.f2-cmp__bar--us { height: 200px; background: linear-gradient(105deg, #f7d880 0%, #c69a1c 55%, #8a6520 100%); }
.f2-cmp__bar--us img { width: 52px; height: 52px; filter: grayscale(1) brightness(1.6) contrast(4); mix-blend-mode: multiply; }  /* disc to white, then multiplied away: only the glyph stays */
.f2-cmp__name { position: absolute; bottom: -28px; font-size: 13px; font-weight: 500; color: rgba(255, 255, 255, .85); }
.f2-cmp__col { position: relative; padding-bottom: 0; }
.f2-cmp__gain { position: relative; align-self: stretch; }
.f2-cmp__gain svg { position: absolute; left: -10px; right: -10px; bottom: 120px; height: 90px; width: calc(100% + 20px); }
.f2-cmp__pill { position: absolute; left: 50%; bottom: 196px; transform: translateX(-50%); white-space: nowrap; padding: 4px 12px; border-radius: 999px;
  border: 1px solid #edc967; color: #edc967; font-size: 12px; font-weight: 600; }
.f2-cmp__cards { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px; margin-top: 28px; }
.f2-cmp__cards > div { padding: 18px 20px; border-radius: 16px; border: 1px solid rgba(255, 255, 255, .16); }
.f2-cmp__cards h3 { margin: 0 0 10px; font-size: 16px; font-weight: 600; } .f2-cmp__cards h3 span { color: #edc967; }
.f2-cmp__cards ul { display: grid; gap: 8px; margin: 0; padding: 0; list-style: none; font-size: 13px; line-height: 1.5; color: rgba(255, 255, 255, .85); }
.f2-cmp__cards li { position: relative; padding-left: 14px; }
.f2-cmp__cards li::before { content: ""; position: absolute; left: 0; top: 7px; width: 5px; height: 5px; border-radius: 50%; background: #22c55e; }
.f2-cmp__note { margin: 0; font-size: 11px; color: rgba(255, 255, 255, .6); }
/* the "Higher" arrow and pill slide in once when the chart is seen (Figma's 0.5s ease-out) */
@media (prefers-reduced-motion: no-preference) {
  .f2-cmp.is-seen .f2-cmp__gain { animation: f2-slide .5s ease-out both; }
}
@keyframes f2-slide { from { transform: translateX(-120px); opacity: 0; } to { transform: none; opacity: 1; } }

/* calculator */
.f2-calc { display: grid; gap: 16px; padding: 22px; }
.f2-field { display: grid; gap: 8px; font-size: 13px; color: var(--sub); }
.f2-input, .f2-field select { display: flex; align-items: center; gap: 6px; height: 46px; padding: 0 18px; border-radius: 999px; border: 0;
  background: #f5f3ee; font: inherit; font-size: 15px; font-weight: 500; color: #322811; }
.f2-input input { flex: 1; min-width: 0; border: 0; background: none; font: inherit; color: inherit; outline: none; }
.f2-input:focus-within, .f2-field select:focus-visible { outline: 2px solid #d4af37; outline-offset: 1px; }
.f2-switch { display: inline-flex; align-items: center; gap: 10px; font-size: 13px; color: #4a4336; cursor: pointer; }
.f2-switch input { position: absolute; opacity: 0; width: 1px; height: 1px; }
.f2-switch__ui { position: relative; width: 38px; height: 22px; border-radius: 999px; background: #d9d4c7; transition: background-color .2s ease; }
.f2-switch__ui::after { content: ""; position: absolute; top: 3px; left: 3px; width: 16px; height: 16px; border-radius: 50%; background: #fff; transition: transform .2s ease; }
.f2-switch input:checked + .f2-switch__ui { background: linear-gradient(105deg, #f7d880, #c69a1c); }
.f2-switch input:checked + .f2-switch__ui::after { transform: translateX(16px); }
.f2-switch input:focus-visible + .f2-switch__ui { outline: 2px solid #d4af37; outline-offset: 2px; }
.f2-out { display: grid; gap: 12px; margin: 0; }
.f2-out div { display: flex; justify-content: space-between; gap: 12px; font-size: 13px; }
.f2-out dt { color: var(--sub); } .f2-out dd { margin: 0; font-weight: 600; color: #322811; font-variant-numeric: tabular-nums; }
.f2-out dd.f2-gain { color: #06963c; }
.f2-cta { display: inline-flex; align-items: center; justify-content: center; gap: 8px; height: 50px; border: 0; border-radius: 999px; cursor: pointer;
  background: linear-gradient(105deg, #f7d880 0%, #e6b325 45%, #b38600 100%); color: #322811; font: inherit; font-size: 15px; font-weight: 600;
  text-decoration: none; transition: filter .2s ease, transform .2s ease; }
.f2-cta:hover { filter: brightness(1.05); } .f2-cta:active { transform: scale(.98); }
.f2-cta:focus-visible { outline: 2px solid #322811; outline-offset: 2px; }
.f2-cta--sm { height: 44px; padding: 0 24px; font-size: 14px; }
.f2-insured, .f2-terms { margin: -6px 0 0; display: flex; justify-content: center; align-items: center; gap: 6px; font-size: 11px; color: #4a4336; }
.f2-terms a { color: #8a6520; }

/* FAQ, help */
.f2-faq__item { margin-top: 12px; border-radius: 14px; background: #faf8f3; }
.f2-faq__item summary { display: flex; justify-content: space-between; gap: 16px; padding: 16px 18px; font-size: 14px; font-weight: 600; color: #322811;
  cursor: pointer; list-style: none; }
.f2-faq__item summary::-webkit-details-marker { display: none; }
.f2-faq__item summary::after { content: "\\2304"; color: var(--sub); transition: transform .2s ease; }
.f2-faq__item[open] summary::after { transform: rotate(180deg); }
.f2-faq__item summary:focus-visible { outline: 2px solid #d4af37; outline-offset: -2px; border-radius: 14px; }
.f2-faq__item p { margin: 0; padding: 0 18px 16px; font-size: 13px; line-height: 1.6; color: #4a4336; }
.f2-help { display: grid; justify-items: center; gap: 10px; text-align: center; }
.f2-help > img { width: 160px; height: 160px; }
.f2-help h2 { display: flex; align-items: center; gap: 8px; margin: 0; font-size: 22px; }
.f2-help p { margin: 0 0 6px; max-width: 32ch; font-size: 13px; line-height: 1.55; color: #322811; }

@media (prefers-reduced-motion: reduce) { .f2-cta, .f2-switch__ui, .f2-switch__ui::after, .f2-pop__card { transition: none; } }

/* tablets and phones: one column in Figma 139:761's order (tenures, then the calculator) */
@media (max-width: 1023px) {
  .f2 { display: flex; flex-direction: column; align-items: stretch; }
  .f2-a > *, .f2-b > * { min-width: 0; }
  .f2-a, .f2-b { display: contents; }
  .f2-all { order: 1; } .f2-side { order: 2; } .f2-why { order: 3; } .f2-cmp { order: 4; }
  .f2-q { order: 5; } .f2-h { order: 6; } .f2-app { order: 7; }
  .f2-side .f2-calc { position: static; }
}
/* phones: Figma 139:761 */
@media (max-width: 639px) {
  .f2 { padding: 12px 16px 40px; gap: 20px; }
  .f2-card { padding: 20px 16px; border-radius: 20px; }
  .f2-card h2, .f2-why h2 { font-size: 16px; font-weight: 700; }
  .f2-hero { gap: 22px; padding: 20px; border-radius: 20px;
    background: radial-gradient(140% 140% at 100% 100%, rgba(0, 38, 147, .8) 0%, #172554 20%, #0f172a 60%, #020617 100%); }
  .f2-hero__top { display: grid; grid-template-columns: 69px minmax(0, 1fr) auto; column-gap: 13px; row-gap: 4px; }
  .f2-hero__logo { grid-row: span 2; width: 69px; height: 69px; border: 2px solid #edc967; }
  .f2-hero h1 { align-self: end; font-size: 20px; }
  .f2-hero__chip { grid-column: 2; align-self: start; justify-self: start; height: auto; padding: 0; border: 0; background: none; font-size: 12px; }
  .f2-hero__chip i { width: 5px; height: 5px; box-shadow: 0 0 8px #22c55e; }
  .f2-hero__share { grid-column: 3; grid-row: 1 / span 2; align-self: center; width: 36px; height: 36px; }
  .f2-hero__facts { display: grid; grid-template-columns: 1fr 1fr; gap: 22px 0; }
  .f2-hero__fact { justify-content: center; gap: 8px; }
  .f2-hero__fact img { width: 36px; height: 36px; }
  .f2-hero__fact + .f2-hero__fact { padding-left: 0; border-left: .5px solid rgba(217, 217, 217, .3); }
  .f2-hero__fact:last-child { grid-column: 1 / -1; flex-direction: row-reverse; justify-content: space-between; border-left: 0; }
  .f2-hero__fact:last-child img { width: 64px; height: 64px; }
  .f2-hero__fact dt { font-size: 14px; color: rgba(255, 255, 255, .6); }
  .f2-hero__fact dd { margin-top: 8px; color: rgba(255, 255, 255, .9); }
  .f2-hero__fact:last-child dt { font-size: 13px; }
  .f2-pop__grid { gap: 8px; }
  .f2-pop__card { gap: 4px; padding: 10px 10px 0; border-radius: 16px; border: .5px solid rgba(242, 137, 0, .5); }
  .f2-pop__card--1 { border-color: #acc7f9; }
  .f2-pop__card:has(input:checked) { border-color: #edc967; box-shadow: 0 0 0 1px #edc967 inset; }
  .f2-pop__card input { top: 10px; right: 10px; }
  .f2-pop__rate { font-size: 16px; font-weight: 700; }
  .f2-pop__meta { font-size: 12px; color: #666; }
  .f2-pop__tag { margin: 10px -10px 0; font-size: 12px; font-weight: 700; }
  .f2-pop__card--0 .f2-pop__tag { background: #ffe7c7; color: #db7924; }
  .f2-pop__card--1 .f2-pop__tag { background: #e5eeff; color: #3b63ae; }
  /* tenures: Figma's three columns, payout under the tenure and the badge under the rate */
  .f2-all__scroll { margin-inline: -16px; }
  .f2-all th:nth-child(2), .f2-all td:nth-child(2) { display: none; }
  .f2-all td, .f2-all th { padding-inline: 12px; white-space: normal; }
  .f2-all th:not(:first-child), .f2-all td:not(:first-child) { text-align: center; }
  .f2-all .f2-all__p { display: inline; }
  .f2-all label .f2-all__p { display: block; font-size: 12px; font-weight: 400; color: #666; }
  .f2-all label { gap: 14px; }
  .f2-badge { display: block; margin: 2px 0 0; padding: 0; background: none !important; color: #06963c !important; font-size: 12px; }
  .f2-why__grid, .f2-cmp__cards { grid-template-columns: minmax(0, 1fr); }
  .f2-cmp { gap: 20px; padding: 20px; border-radius: 24px; background: #0e1015; }
  .f2-cmp h2 { font-size: 16px; font-weight: 700; color: #e9e9e9; }
  .f2-cmp__vs { font-size: 15px; font-weight: 400; color: #8e94a2; } .f2-cmp__us { color: #d4af37; }
  .f2-cmp__chart { grid-template-columns: minmax(0, 1fr) 98px minmax(0, 1fr); margin-bottom: 44px; }
  .f2-cmp__col b { font-size: 18px; }
  .f2-cmp__bar { width: 87px; } .f2-cmp__bar--us { width: 91px; }
  .f2-cmp__bar--them { height: 124px; border-radius: 12px 12px 0 0; border-color: #d7caaa; background: linear-gradient(180deg, #403a2e, #221f1a 29%, #1a1815 73%); }
  .f2-cmp__bar--us { border-radius: 20px 20px 0 0; border: 1px solid #ffefa3; }
  .f2-cmp__name { top: calc(100% + 8px); bottom: auto; left: 50%; transform: translateX(-50%); width: 120px; font-size: 12px; font-weight: 600; text-align: center; color: #f5f7fa; }
  .f2-cmp__cards { margin-top: 0; gap: 16px; }
  .f2-cmp__cards > div { padding: 0; border: 0; }
  .f2-help { grid-template-columns: minmax(0, 1fr) 120px; justify-items: start; column-gap: 8px; text-align: left; }
  .f2-help > img { grid-column: 2; grid-row: 1 / span 3; align-self: center; width: 120px; height: 120px; }
  .f2-help > :not(img) { grid-column: 1; }
  .f2-help h2 { font-size: 18px; }
  .f2-help .f2-cta { background: #fff; border: 1px solid #edc967; }
}
"""

SCRIPT = """<script>
// fd-details2: tenure pickers stay in step with the calculator; the calculator
// recomputes (quarterly compounding over the tenure's days / 365.25 for On
// Maturity, simple interest for payouts); the chart's arrow slides in once.
(function () {
  var T = %s;
  var amt = document.getElementById('f2-amt'), ten = document.getElementById('f2-ten'), sr = document.getElementById('f2-sr');
  if (!amt) return;
  var inr = function (v) { return '\\u20b9 ' + v.toLocaleString('en-IN', { minimumFractionDigits: v %% 1 ? 2 : 0, maximumFractionDigits: 2 }); };
  var first = true;
  // a fixed day count (365.25-day years, 30.4375-day months), so results don't drift with today's date: 1Y 4M 16D = 503 days
  function days(t) { return Math.round(t[5] * 365.25 + t[6] * 30.4375 + t[7]); }
  function calc() {
    var t = T[+ten.value], r = parseFloat(sr.checked ? t[3] : t[2]) / 100;
    var p = parseInt(amt.value.replace(/[^0-9]/g, ''), 10) || 0, n = days(t) / 365.25;
    var gain = t[1] === 'On Maturity' ? p * (Math.pow(1 + r / 4, 4 * n) - 1) : p * r * n;
    gain = Math.round(gain * 100) / 100;
    document.getElementById('f2-rate').textContent = (r * 100).toFixed(2) + '%%';
    if (first) { first = false; return; }   // keep the captured figures until the user changes something
    document.getElementById('f2-inv').textContent = inr(p);
    document.getElementById('f2-int').textContent = inr(gain);
    document.getElementById('f2-mat').textContent = inr(Math.round((p + gain) * 100) / 100);
  }
  function pick(i) {
    ten.value = i;
    document.querySelectorAll('input[name="f2-row"]').forEach(function (x) { x.checked = +x.value === i; x.closest('tr').classList.toggle('is-on', x.checked); });
    document.querySelectorAll('input[name="f2-pop"]').forEach(function (x) { x.checked = +x.value === i; });
    calc();
  }
  document.addEventListener('change', function (e) {
    if (e.target.name === 'f2-row' || e.target.name === 'f2-pop') pick(+e.target.value);
    else if (e.target === ten) pick(+ten.value);
    else if (e.target === sr) calc();
  });
  amt.addEventListener('input', function () {
    var p = parseInt(amt.value.replace(/[^0-9]/g, ''), 10);
    amt.value = isNaN(p) ? '' : p.toLocaleString('en-IN');
    calc();
  });
  calc();
  var share = document.querySelector('[data-f2-share]');
  if (share) share.addEventListener('click', function () {
    if (navigator.share) navigator.share({ title: document.title, url: location.href }).catch(function () {});
    else if (navigator.clipboard) navigator.clipboard.writeText(location.href);
  });
  var cmp = document.querySelector('.f2-cmp');
  if (cmp && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { cmp.classList.add('is-seen'); io.disconnect(); } }, { threshold: .4 });
    io.observe(cmp);
  } else if (cmp) cmp.classList.add('is-seen');
})();
</script>
"""


def main():
    import json
    script = SCRIPT % json.dumps([list(t) for t in TENURES])
    X.assemble(body(), OUT, "Unity Small Finance Bank FD | GoldenPi",
               "pages/_fd_details2.py (Unity FD page, new version: Figma 138:579 on user-explore-app7's shell)",
               style=A.STYLE + "<style>\n" + S.STYLE + STYLE + "</style>\n", script=script)
    with open(OUT, encoding="utf-8") as f:
        page = S.header(f.read())
    page, n = re.subn(r'<a class="nb__link" href="user-fixed-deposits(?:-app2)?.html">',  # portfolio.html may be prototype-wired
                      '<a class="nb__link is-current" href="user-fixed-deposits.html" aria-current="page">', page, count=1)
    if n != 1:
        raise SystemExit("FD link not found in the navbar")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page)


if __name__ == "__main__":
    main()
