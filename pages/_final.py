#!/usr/bin/env python3
"""Generate pages/corporate-bonds.html.

This page is the former corporate-bonds.html (now archived as
corporate-bonds-old.html) with four improvements ported in from the taste2
exploration. It keeps the same stack, the same shared header and
footer, and the same gp-* components, so the change a developer implements is a
small diff rather than a new design system.

Only the tabbed listing is generated, because it is repetitive and data-driven.
Everything else lives in _final_shell.html and is edited by hand.

Each tab draws rows actually captured from uatnew.goldenpi.com on 2026-09-25.
Nothing is invented. Where a tab's best match was captured on another page (the
NCD IPOs, the Muthoot Capital bond and its stated minimum), the panel says so.

Run: python3 pages/_final.py
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://uatnew.goldenpi.com"

A = "GPID102720.AKARA-CAPITAL-ADVISORS-PRIVATE-LIMITED-2x.png"
N = "GPID104095.Neogrowth-new-logo-1-.jpg"
B = "GPID107347.Best-Capital.png"
E = "GPID100778.EDELWEISS-FINANCIAL-SERVICES-LIMITED.png"
M = "GPID100936.MUTHOOT-FINCORP-LIMITED_1-2x.png"

# issuer, logo, returns, rating, fourth-column value, fifth-column value, href
AKARA_13 = ("AKARA", A, "13.00%", "ACUITE BBB+", "Monthly", "3-Dec-2027",
            "/bonds/GPID107435/akara-1300-bond-yield?src=view_details&tenureDate=03-Dec-2027")
NEO = ("NEOGROWTH", N, "13.00%", "ICRA BBB", "Half Yearly", "30-Apr-2028",
       "/bonds/GPID107371/neogrowth-1300-bond-yield?src=view_details&tenureDate=30-Apr-2028")
BEST = ("BEST CAPITAL", B, "13.00%", "IVR BBB", "Monthly", "11-Sep-2029",
        "/bonds/GPID107433/best-capital-1300-bond-yield?src=view_details&tenureDate=11-Sep-2029")
AKARA_12 = ("AKARA", A, "12.78%", "ACUITE BBB+", "Monthly", "3-Dec-2027",
            "/bonds/GPID107435/akara-1278-bond-yield?src=view_details&tenureDate=03-Dec-2027")
EDEL = ("EDELWEISS FINANCIAL SERVICES LIMITED", E, "10.00%", "A+/STABLE CRISIL",
        "Fast Filling", "5-Oct-2026",
        "/bond-ipo/GPID100778/edelweiss-financial-services-limited?src=preview")
MUTH_IPO = ("MUTHOOT FINCORP LIMITED", M, "9.25%", "AA/STABLE CRISIL",
            "Fast Filling", "22-Sep-2026",
            "/bond-ipo/GPID100936/muthoot-fincorp-limited?src=preview")
MUTH_CAP = ("MUTHOOT CAPITAL", M, "9.70%", "CRISIL AA-", "&#8377;30,000", "24-Aug-2029",
            "/bonds/INE296G07333/muthoot-capital-925-bond-yield?src=view_details&tenureDate=24-Aug-2029")

TABS = [
    dict(id="utsav", label="Bond Utsav Deals", icon="pre-login-active-offers.svg",
         col4="Payout", col5="Maturity Date", rows=[AKARA_13, NEO, BEST, AKARA_12],
         more=("View All", "/bond-utsav"), note=None),

    dict(id="rated", label="High Rated Bonds", icon="pre-login-aaa-rated.svg",
         col4="Status", col5="Closes On", rows=[EDEL, MUTH_IPO],
         more=("View all highly rated bonds", "/collections/highly-rated-bonds"),
         note="The highest rated issues in this snapshot are the two live NCD IPOs."),

    dict(id="thirtyk", label="Bonds at &#8377;30K", icon="pre-login-bonds-at-10k.svg",
         col4="Min. Investment", col5="Maturity Date", rows=[MUTH_CAP],
         more=("View bonds under &#8377;10,000", "/collections/bonds-at-10000"),
         note="Minimum investment as listed by the issuer."),

    dict(id="monthly", label="Bonds for Monthly Income", icon="monthly-bonds.svg",
         col4="Payout", col5="Maturity Date", rows=[AKARA_13, BEST, AKARA_12],
         more=("View all monthly income bonds", "/collections/bonds-to-earn-monthly-fixed-income"),
         note=None),

    dict(id="yield", label="11%+ Yield Bonds", icon="pre-login-home-highest-yield.svg",
         col4="Payout", col5="Maturity Date", rows=[AKARA_13, NEO, BEST, AKARA_12],
         more=("View all high yield bonds", "/collections/high-yield-bonds"), note=None),

    dict(id="ipo", label="NCD IPO", icon="pre-login-ncd-ipo.svg",
         col4="Status", col5="Closes On", rows=[EDEL, MUTH_IPO],
         more=("View all ongoing NCD IPOs", "/collections/best-ongoing-ipos"), note=None),
]


def row_html(r, i, col4, col5):
    """One listing row, in the page's existing .gp-row markup."""
    name, logo, ret, rating, four, five, href = r
    link = BASE + href.replace("&", "&amp;")
    return (
        '            <article class="gp-row" style="--r:%d">\n'
        '              <div class="gp-row__identity">\n'
        '                <img class="gp-row__logo" src="../assets/img/%s" alt="">\n'
        '                <a class="gp-row__name gp-row__link" href="%s">%s</a>\n'
        '              </div>\n'
        '              <div><div class="gp-row__label">Returns</div>'
        '<div class="gp-row__value gp-row__value--returns">%s</div></div>\n'
        '              <div><div class="gp-row__label">Credit Rating</div>'
        '<div class="gp-row__value">%s</div></div>\n'
        '              <div><div class="gp-row__label">%s</div>'
        '<div class="gp-row__value">%s</div></div>\n'
        '              <div><div class="gp-row__label">%s</div>'
        '<div class="gp-row__value">%s</div></div>\n'
        '              <div class="gp-row__actions">\n'
        '                <button type="button" title="Add to watchlist">'
        '<img src="../assets/img/goolden-bookmark.svg" alt="Add to watchlist"></button>\n'
        '                <button type="button" title="Share">'
        '<img src="../assets/img/golden-share.svg" alt="Share"></button>\n'
        '              </div>\n'
        '            </article>'
    ) % (i, logo, link, name, ret, rating, col4, four, col5, five)


def build():
    buttons, panels = [], []
    for k, t in enumerate(TABS):
        sel = "true" if k == 0 else "false"
        tabindex = "" if k == 0 else ' tabindex="-1"'
        buttons.append(
            '            <button type="button" class="gp-tab" role="tab" id="tab-%s"\n'
            '                    aria-controls="panel-%s" aria-selected="%s"%s>\n'
            '              <img src="../assets/img/%s" alt="">%s\n'
            '            </button>' % (t["id"], t["id"], sel, tabindex, t["icon"], t["label"]))

        note = ('          <p class="gp-panel__note">%s</p>\n' % t["note"]) if t["note"] else ""
        rows = "\n\n".join(row_html(r, i, t["col4"], t["col5"]) for i, r in enumerate(t["rows"]))
        more_label, more_href = t["more"]
        panels.append(
            '        <div class="gp-panel%s" id="panel-%s"\n'
            '             role="tabpanel" aria-labelledby="tab-%s"%s>\n'
            '%s'
            '          <div class="gp-rows__head">\n'
            '            <span>Issuer</span><span>Returns</span><span>Credit Rating</span>\n'
            '            <span>%s</span><span>%s</span><span></span>\n'
            '          </div>\n\n'
            '          <div class="gp-rows">\n%s\n          </div>\n\n'
            '          <div class="mt-5 text-center">\n'
            '            <a class="t-small font-bold t-bronze underline" href="%s%s">%s</a>\n'
            '          </div>\n'
            '        </div>' % (
                " is-on" if k == 0 else "", t["id"], t["id"],
                "" if k == 0 else " hidden", note,
                t["col4"], t["col5"], rows, BASE, more_href, more_label))

    return "\n\n".join(buttons), "\n\n".join(panels)


def faq_with_help(html, contact_href=BASE + "/contact-us"):
    """Put the FAQ accordion and a Need Help card side by side, as on the
    Akara issuer page. Shared by all four live pages."""
    i = html.index('<div class="gp-faq">')
    j = html.index('</div>', html.rindex('</details>', i)) + len('</div>')

    # Structure matches issuer-need-help exactly: the 237px support illustration,
    # a small phone icon beside the title, and an arrow inside the CTA.
    help_card = (
        '\n\n        <aside class="gp-need-help">\n'
        '          <img class="gp-need-help__image" src="../assets/img/support-icon.svg"\n'
        '               alt="" width="237" height="237">\n'
        '          <p class="gp-need-help__title">\n'
        '            <img src="../assets/img/phone-icon.svg" alt="" width="20" height="20">\n'
        '            Need Help\n'
        '          </p>\n'
        '          <p class="gp-need-help__desc">Talk to our Support Team for free. We will\n'
        '            help you through your investment journey.</p>\n'
        '          <a class="gp-cta gp-cta--primary" href="%s">\n'
        '            Contact Us\n'
        '            <img class="gp-cta__arrow" src="../assets/img/arrow-right.svg"\n'
        '                 alt="" width="16" height="16">\n'
        '          </a>\n'
        '        </aside>' % contact_href)

    return (html[:i] + '<div class="gp-faq-layout">\n        ' + html[i:j]
            + help_card + '\n      </div>' + html[j:])


BLOG_CARD = re.compile(
    r'<article class="gp-card gp-card--link flex overflow-hidden">\s*'
    r'<div class="flex flex-1 flex-col p-5">\s*'
    r'<p class="t-caption t-bronze">(.*?)</p>\s*'
    r'<h3 class="mt-2 t-lead font-bold">(.*?)</h3>\s*'
    r'<p class="mt-2 t-small t-muted">(.*?)</p>\s*'
    r'<a class="[^"]*"\s*href="([^"]+)">Read more</a>\s*'
    r'</div>\s*'
    r'<img src="([^"]+)"[^>]*>\s*'
    r'</article>', re.S)


def blog_cards(html):
    """Blog cards take the Akara issuer page's gp-blogcard shape.

    Same category, title, date, link and image per card; the whole card
    becomes the link, with the image in a rounded square on the right.
    """
    html, n = BLOG_CARD.subn(lambda m: (
        '<a class="gp-blogcard" href="%s">\n'
        '          <span class="gp-blogcard__body">\n'
        '            <span class="gp-blogcard__cat">%s</span>\n'
        '            <span class="gp-blogcard__title">%s</span>\n'
        '            <span class="gp-blogcard__meta">%s</span>\n'
        '            <span class="gp-blogcard__more">Read more\n'
        '              <img src="../assets/img/SVG-1.png" alt="" width="14" height="14"></span>\n'
        '          </span>\n'
        '          <img class="gp-blogcard__media gp-blogcard__media--photo" src="%s" alt="" width="380" height="280">\n'
        '        </a>' % (m.group(4), m.group(1), m.group(2), m.group(3), m.group(5))), html)
    if n != 3:
        raise SystemExit("expected 3 blog cards, converted %d" % n)
    return html


REVIEW = re.compile(
    r'<figure class="gp-card flex h-full flex-col p-5">\s*'
    r'<figcaption[^>]*>\s*<span[^>]*>(.*?)</span>\s*<span[^>]*>(.*?)</span>\s*</figcaption>\s*'
    r'<p[^>]*aria-label="([^"]*)">(.*?)</p>\s*'
    r'<blockquote[^>]*>(.*?)</blockquote>\s*</figure>', re.S)


def review_marquee(html):
    """Reviews become a strip that drifts left on a loop.

    Same reviewers, stars and quotes. The set is rendered twice so the loop is
    seamless; the copy is aria-hidden so screen readers hear each review once.
    CSS pauses it on hover and stops it under reduced motion.
    """
    grid = '<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">'
    first = REVIEW.search(html)
    if not first:
        raise SystemExit("no review cards found")
    start = html.rindex(grid, 0, first.start())
    end = html.index('</div>', [m for m in REVIEW.finditer(html)][-1].end()) + len('</div>')
    cards = REVIEW.findall(html[start:end])

    def card(c, hidden):
        initial, name, label, stars, quote = c
        return (
            '          <figure class="gp-review"%s>\n'
            '            <figcaption class="gp-review__head">\n'
            '              <span class="gp-review__avatar">%s</span>\n'
            '              <span>\n'
            '                <span class="gp-review__name">%s</span>\n'
            '                <span class="gp-review__stars" aria-label="%s">%s</span>\n'
            '              </span>\n'
            '            </figcaption>\n'
            '            <blockquote class="gp-review__text">%s</blockquote>\n'
            '          </figure>' % (' aria-hidden="true"' if hidden else '',
                                     initial, name, label, stars, quote.strip()))

    track = "\n".join([card(c, False) for c in cards] + [card(c, True) for c in cards])
    return (html[:start]
            + '<div class="gp-reviews">\n        <div class="gp-reviews__track" style="--n:%d">\n%s\n'
              '        </div>\n      </div>' % (len(cards), track)
            + html[end:])


def primary_ctas(html):
    """Every primary CTA takes the gradient gp-cta look the FD page uses.

    Ghost buttons are left alone; only fixed-deposits swaps those too.
    """
    html = html.replace('class="gp-btn gp-btn--primary gp-btn--sm',
                        'class="gp-cta gp-cta--primary gp-cta--sm')
    return html.replace('class="gp-btn gp-btn--primary', 'class="gp-cta gp-cta--primary')


# Sections the product owner removed from the product pages (2026-09-26):
# the "Why invest" blocks, and the how-to-invest steps.
DROPPED_HEADINGS = (
    "Why invest in Corporate Bonds with GoldenPi?",
    "Why invest in with GoldenPi?",
    "Why to invest in Bond IPO with GoldenPi",
    "Invest in Corporate Bonds in 3 easy steps",
    "How to Invest in Bond IPOs Online",
)


def drop_sections(html):
    """Remove each listed section present, banner comment to closing tag.

    The "Why 15 Lakh+ Users Trust GoldenPi" reviews section is a different
    one and stays.
    """
    dropped = 0
    for heading in DROPPED_HEADINGS:
        needle = '<h2 class="gp-section__title">%s</h2>' % heading
        if needle in html:
            h = html.index(needle)
            start = html.rindex('  <!-- ====', 0, h)
            end = html.index('  </section>\n', h) + len('  </section>\n')
            html = html[:start] + html[end:].lstrip('\n')
            dropped += 1
    if not dropped:
        raise SystemExit("none of the dropped sections found")
    return html


# The platform strip from the Akara issuer page ("The Golden Experience of
# Investing"), copy and icons as captured there. It replaces the Milestones
# figures inside the reviews section (product owner's call, 2026-09-26).
GOLDEN = [
    ("trophy.png", "Zero Defaults"),
    ("shield.png", "Sebi Registered"),
    ("5percent.png", "Curated Bonds"),
    ("users.png", "18 lacs+ Users"),
]


def golden_experience(html, add=False):
    """Drop the Milestones section; add the Golden Experience strip as its own
    section just before the reviews, built exactly as on the Akara page.

    Pages that had a Milestones section get the strip; add=True gives it to a
    page that never had one (fixed-deposits).
    """
    banner = '  <!-- ======================================================== milestones -->'
    if banner in html:
        start = html.index(banner)
        end = html.index('  </section>\n', start) + len('  </section>\n')
        html = html[:start] + html[end:].lstrip('\n')
    elif not add:
        return html

    items = "\n".join(
        '        <div class="gp-stats__item">\n'
        '          <img src="../assets/img/%s" alt="" width="36" height="36">\n'
        '          <span class="gp-stats__value">%s</span>\n'
        '        </div>' % g for g in GOLDEN)
    section = (
        '  <!-- ================================================ golden experience -->\n'
        '  <section data-reveal class="gp-section gp-section--tight gp-section--flush-top">\n'
        '    <div class="gp-shell">\n'
        '      <p class="gp-divider">The Golden Experience of Investing</p>\n'
        '      <div class="gp-stats">\n%s\n      </div>\n'
        '    </div>\n'
        '  </section>\n\n' % items)
    # Its own section, directly before the reviews section.
    reviews = html.index('<div class="gp-reviews">')
    banner_at = html.rindex('  <!-- ====', 0, reviews)
    return html[:banner_at] + section + html[banner_at:]


# The webinar block, as the live site builds it: copy and figures on the left,
# the YouTube webinar on the right. The embed URL, its autoplay/mute params and
# the iframe's allow list are as captured from uatnew.goldenpi.com/ on
# 2026-09-25. The disclaimer is about the faces in that video, so it sits
# under the video as its caption.
WEBINAR = '''  <!-- =========================================================== webinar -->
  <section data-reveal class="gp-section gp-section--tight gp-section--flush-top">
    <div class="gp-shell">
      <div class="gp-card gp-webinar">
        <div class="gp-webinar__body">
          <p class="gp-webinar__issuer">Muthoot Capital</p>
          <h2 class="gp-webinar__title">Webinar with Muthoot Capital&rsquo;s CEO</h2>

          <dl class="gp-webinar__facts">
            <div><dt>Returns Up to</dt><dd class="gp-webinar__returns">9.70%</dd></div>
            <div><dt>Credit Rating</dt><dd>CRISIL AA-</dd></div>
            <div><dt>Min. Investment</dt><dd>&#8377;30,000</dd></div>
          </dl>

          <a class="gp-cta gp-cta--primary gp-webinar__cta"
             href="https://uatnew.goldenpi.com/bonds/INE296G07333/muthoot-capital-925-bond-yield?src=view_details&amp;tenureDate=24-Aug-2029">Invest Now</a>
        </div>

        <figure class="gp-webinar__media">
          <div class="gp-webinar__frame">
            <iframe src="https://www.youtube.com/embed/bITuF1qC5Kg?autoplay=1&amp;mute=1&amp;rel=0"
                    title="Webinar with Muthoot Capital&rsquo;s CEO" loading="lazy"
                    allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>
          </div>
          <figcaption class="gp-webinar__note">
            No celebrities are part of the advertisement, all faces displayed are in the capacity of Business Representatives.
          </figcaption>
        </figure>
      </div>
    </div>
  </section>
'''


def webinar(html):
    """Replace the webinar section, where a page has one, with WEBINAR."""
    banner = '  <!-- =========================================================== webinar -->'
    if banner not in html:
        return html
    start = html.index(banner)
    end = html.index('  </section>\n', start) + len('  </section>\n')
    return html[:start] + WEBINAR + html[end:]


MARK = "  <!-- ======================================================== collections -->\n"


def collections(title=None):
    """The shell's five-card collections bento, so every page draws the same one."""
    src = open(os.path.join(HERE, "_final_shell.html"), encoding="utf-8").read()
    start = src.index(MARK)
    sec = src[start:src.index("  </section>\n", start) + len("  </section>\n")]
    return sec.replace("Explore our extensive Corporate Bonds Collections", title) if title else sec


def main():
    buttons, panels = build()
    src = open(os.path.join(HERE, "_final_shell.html"), encoding="utf-8").read()
    for token in ("<!--TABS-->", "<!--PANELS-->", "<!--TABJS-->"):
        if token not in src:
            raise SystemExit("_final_shell.html is missing %s" % token)
    js = open(os.path.join(HERE, "_tabs.js"), encoding="utf-8").read()
    out = (src.replace("<!--TABS-->", buttons)
              .replace("<!--PANELS-->", panels)
              .replace("<!--TABJS-->", "<script>\n%s</script>" % js))
    path = os.path.join(HERE, "corporate-bonds.html")
    out = golden_experience(drop_sections(primary_ctas(review_marquee(blog_cards(faq_with_help(out))))))
    open(path, "w", encoding="utf-8").write(out)
    print("wrote %s  (%d tabs, %d rows)" % (
        os.path.basename(path), len(TABS), sum(len(t["rows"]) for t in TABS)))


if __name__ == "__main__":
    main()
