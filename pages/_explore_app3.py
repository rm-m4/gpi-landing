#!/usr/bin/env python3
"""user-explore-app3.html: the post-login home, redesigned as a quiet-luxury page.

Design read: a post-login home for affluent bond and NCD IPO investors, private-bank
register, GoldenPi's black / gold / white. Dials: variance 6, motion 4, density 3.
One dark theme for the whole page (the navbar and footer are already black), gold
only on money figures and the one Refer band, near-black / gold pills for actions.
Every section uses a different layout family:

  greeting + spotlight deal with a deal switcher | portfolio card + pending orders
  live NCD IPO as a full-width band
  bonds as a ledger, High yield / Highly rated tabs
  collections as a pill row
  why bonds: statement left, three reasons right, brand stats under it
  Refer & Earn as the single gold band
  Need help + the app, side by side

Content is user-explore-app2's (same sources and DATA marks): deals, IPO, the
collections capture, refer, contact, play-store and the FAQ's three reasons.

    python3 pages/_explore_app3.py
"""
import os

import _explore_app as X
import _explore_app2 as E

OUT = os.path.join(X.HERE, "user-explore-app3.html")
esc, R, C, W = E.esc, E.R, E.C, E.W
LOGO = "../assets/img/"


# ------------------------------------------------------------------- top
def spotlight():
    """One deal at a time, chosen from a tab list beside it. Without JS the first panel shows and the
    tabs are inert labels."""
    panels, tabs = [], []
    for k, (logo, name, rate, label, payout, mat, href) in enumerate(E.DEALS):
        rating = label.split("&middot; ", 1)[1]
        panels.append(
            '<div class="lx-deal" role="tabpanel" id="lx-deal-%d" aria-labelledby="lx-tab-%d"%s>'
            '<div class="lx-deal__id"><span class="lx-logo"><img src="%s%s" alt="" width="40" height="40"></span>'
            '<div><h2>%s</h2><p>Bond Utsav deal</p></div></div>'
            '<p class="lx-deal__rate">%s</p><p class="lx-deal__cap">Fixed returns</p>'
            '<dl class="lx-deal__terms"><div><dt>Rating</dt><dd>%s</dd></div><div><dt>Payout</dt><dd>%s</dd></div>'
            '<div><dt>Maturity</dt><dd>%s</dd></div></dl>'
            '<a class="lx-btn lx-btn--gold" href="%s">View bond <span class="sr-only">%s</span></a></div>'
            % (k, k, "" if k == 0 else " hidden", LOGO, logo, name, rate, rating, payout, mat, esc(href), name))
        tabs.append('<button type="button" role="tab" class="lx-tab" id="lx-tab-%d" aria-controls="lx-deal-%d" aria-selected="%s" tabindex="%d">'
                    '<span class="lx-logo lx-logo--sm"><img src="%s%s" alt="" width="28" height="28"></span>'
                    '<span class="lx-tab__name">%s</span><span class="lx-tab__rate">%s</span></button>'
                    % (k, k, "true" if k == 0 else "false", 0 if k == 0 else -1, LOGO, logo, name, rate))
    return ('<!-- DATA: top 3 Bond Utsav deals, index.html snapshot 2026-09-25. -->\n'
            '<section class="lx-spot" aria-labelledby="lx-spot-t"><h2 class="sr-only" id="lx-spot-t">Bond Utsav top deals</h2>'
            '<div class="lx-spot__stage">%s</div>'
            '<div class="lx-tabs" role="tablist" aria-label="Bond Utsav top deals">%s</div></section>'
            % ("".join(panels), "".join(tabs)))


def account():
    orders = "".join(
        '<li><div><p class="lx-order__name">%s</p><p class="lx-order__meta">%s &middot; %s</p></div>'
        '<span class="lx-order__state lx-order__state--%s">%s</span></li>'
        % (n, m, amt, tone, st) for n, m, amt, st, cta, tone in E.ORDERS)
    return ('<aside class="lx-acct" aria-label="Your account">'
            + X.portfolio_card().replace(" data-reveal", "", 1) +
            '<!-- DATA: pending orders, sample copy. -->\n'
            '<section class="lx-orders" aria-labelledby="lx-orders-t"><h2 id="lx-orders-t">Pending orders <span>%d</span></h2>'
            '<ul>%s</ul><a class="lx-link" href="portfolio.html">Go to portfolio</a></section></aside>' % (len(E.ORDERS), orders))


def top():
    return ('<section class="lx-top lx-shell">'
            '<header class="lx-greet"><h1 id="lx-title">Welcome back, <span data-user="first-name">Investor</span></h1>'
            '<p>Today&#39;s top bond deals and live NCD IPOs, with fixed returns up to <b>13%%</b>.</p></header>'
            '<div class="lx-top__grid">%s%s</div></section>' % (spotlight(), account()))


# ------------------------------------------------------------------- IPO
def ipo():
    E.need(E.content("beta_bond-ipo_GPID104212_smc"), "9-OCT-2026")
    facts = "".join('<div><dt>%s</dt><dd>%s</dd></div>' % kv for kv in
                    (("Coupon", "Up to 10%"), ("Min. investment", R + "10,000"), ("Rating", "ICRA A"), ("Security", "Secured")))
    return ('<!-- DATA: the live NCD IPO, beta snapshot 2026-10-08. -->\n'
            '<section class="lx-ipo" data-reveal aria-labelledby="lx-ipo-t"><div class="lx-shell lx-ipo__in">'
            '<div class="lx-ipo__head"><p class="lx-live"><i aria-hidden="true"></i>NCD IPO live, closes on 9-Oct-2026</p>'
            '<h2 id="lx-ipo-t"><span class="lx-logo"><img src="../assets/img/ipo/smc-logo.png" alt="" width="40" height="40"></span>'
            'SMC Global Securities Limited</h2></div>'
            '<dl class="lx-ipo__facts">%s</dl>'
            '<div class="lx-ipo__cta"><a class="lx-btn lx-btn--gold" href="ipo-details.html">Apply now</a>'
            '<a class="lx-link" href="collections-ncd-ipo.html">All NCD IPOs</a></div></div></section>' % facts)


# ---------------------------------------------------------------- ledger
def ledger():
    tabs, panels = [], []
    for k, (slug, title, sub, href) in enumerate(E.SHELVES):
        rows = []
        for c in C.DATA["tabs"][slug]["cards"][:4]:
            m = {a.title(): b for a, b in c["metrics"]}
            note = c["note"].lstrip("⚡").strip()
            rows.append('<li><a class="lx-row" href="%s"><span class="lx-logo">%s</span>'
                        '<span class="lx-row__id"><b>%s</b><small>%s</small></span>'
                        '<span class="lx-row__m">%s</span><span class="lx-row__m">%s</span>'
                        '<span class="lx-row__rate">%s<small>%%</small></span></a></li>'
                        % (esc(C.UAT + c["href"]), C.logo(c), esc(c["issuer"]), esc(note), esc(m.get("Rating", "")),
                           esc(m.get("Tenure", "")), esc(c["rate"].replace("%", "").strip())))
        on = k == 0
        tabs.append('<button type="button" role="tab" class="lx-seg" id="lx-led-tab-%d" aria-controls="lx-led-%d" aria-selected="%s" tabindex="%d">%s</button>'
                    % (k, k, "true" if on else "false", 0 if on else -1, esc(title)))
        panels.append('<div class="lx-led" role="tabpanel" id="lx-led-%d" aria-labelledby="lx-led-tab-%d"%s>'
                      '<p class="lx-led__sub">%s</p>'
                      '<div class="lx-led__head" aria-hidden="true"><span>Bond</span><span>Rating</span><span>Tenure</span><span>Yield</span></div>'
                      '<ul>%s</ul><a class="lx-link" href="%s">View all %s</a></div>'
                      % (k, k, "" if on else " hidden", esc(sub), "".join(rows), href, esc(title.lower())))
    return ('<!-- DATA: first four bonds of /collections/high-returns and /highly-rated, collections.tabs.json snapshot. -->\n'
            '<section class="lx-bonds lx-shell" data-reveal aria-labelledby="lx-bonds-t">'
            '<header class="lx-sec"><h2 id="lx-bonds-t">Featured bonds</h2>'
            '<div class="lx-segs" role="tablist" aria-label="Bond lists">%s</div></header>%s</section>'
            % ("".join(tabs), "".join(panels)))


def collections():
    pills = "".join('<li><a class="lx-pill" href="%s"><img src="%s%s" alt="" width="28" height="28">%s</a></li>'
                    % (h, X.IMG, f, t) for f, t, h in X.COLLECTIONS)
    return ('<section class="lx-cols lx-shell" data-reveal aria-labelledby="lx-cols-t">'
            '<h2 id="lx-cols-t">Find bonds by goal</h2><ul>%s</ul></section>' % pills)


# ------------------------------------------------------------------ why
def why():
    reasons = "".join('<li><h3>%s</h3><p>%s</p></li>' % (esc(t), esc(b)) for t, b, i in W.reasons()[:3])
    stats = "".join('<li>%s</li>' % t for f, t in X.STATS)
    return ('<section class="lx-why lx-shell" data-reveal aria-labelledby="lx-why-t">'
            '<div class="lx-why__lead"><h2 id="lx-why-t">Why bonds belong in your portfolio</h2>'
            '<p>Fixed returns, regular payouts and the option to sell on the exchange.</p></div>'
            '<ol class="lx-why__list">%s</ol>'
            '<ul class="lx-stats" aria-label="The Golden Experience Of Investing">%s</ul></section>' % (reasons, stats))


# ---------------------------------------------------------------- refer
def refer():
    return ('<section class="lx-refer" data-reveal aria-labelledby="lx-refer-t"><div class="lx-shell lx-refer__in">'
            '<div><h2 id="lx-refer-t">Invite friends, earn up to &#8377;5 Lacs</h2>'
            '<p>You earn 1% of each friend&#39;s investment, up to &#8377;2,000 each time, for up to 50 friends.</p></div>'
            '<a class="lx-btn lx-btn--ink" href="refer-and-earn.html">Refer now</a></div></section>')


# --------------------------------------------------------- help and app
def close():
    return ('<section class="lx-close lx-shell" data-reveal aria-label="Help and app">'
            '<div class="lx-help"><h2>Need help?</h2>'
            '<p>Talk to our Support Team for free. We will help you through your investment journey.</p>'
            '<dl><div><dt>Call</dt><dd><a href="tel:080-45685666">080-45685666</a></dd></div>'
            '<div><dt>Email</dt><dd><a href="mailto:contact-us@goldenpi.com">contact-us@goldenpi.com</a></dd></div>'
            '<div><dt>Hours</dt><dd>Mon to Fri, 9:00 am to 6:30 pm</dd></div></dl>'
            '<a class="lx-link" href="contact-us.html">Contact us</a></div>'
            '<div class="lx-app"><div><img class="lx-app__icon" src="../assets/img/play/app-icon.png" alt="" width="48" height="48">'
            '<h2>Invest and track on the go</h2>'
            '<p>Buy bonds, apply to NCD IPOs and track every payout, 24x7, in one app.</p>'
            '<a class="lx-btn lx-btn--gold" href="%s">Get it on Google Play</a></div>'
            '<img class="lx-app__qr" src="../assets/beta/media/mobile-app-qr.3wptrea2l_26s.svg" alt="Scan to download GoldenPi app" '
            'width="120" height="148" loading="lazy"></div></section>' % esc(E.PLAY))


def body():
    return ('<main id="main-content" class="lx">%s%s%s%s%s%s%s</main>'
            % (top(), ipo(), ledger(), collections(), why(), refer(), close()))


STYLE = """<style>
/* user-explore-app3: quiet luxury, one dark theme. Locks: accent gold (#d4af37 / #e2c372) on figures and the
   Refer band only; radius 20px panels, 14px tiles, pill controls; hairlines instead of boxes wherever possible. */
.lx { --bg: #0b0a08; --panel: #13110d; --panel-2: #1a1712; --hair: rgba(255, 255, 255, .08); --gline: rgba(226, 195, 114, .22);
  --ink: #f4efe3; --sub: rgba(244, 239, 227, .6); --dim: rgba(244, 239, 227, .42); --gold: #e2c372; --gold-deep: #d4af37;
  --ease: cubic-bezier(.16, 1, .3, 1);
  background: var(--bg); color: var(--ink); font-family: satoshi, system-ui, sans-serif; padding-bottom: 96px; }
:where(.lx) *, :where(.lx) *::before, :where(.lx) *::after { box-sizing: border-box; }
:where(.lx) :where(h1, h2, h3, p, ul, ol, dl, dd) { margin: 0; padding: 0; }
:where(.lx) :where(ul, ol) { list-style: none; }
:where(.lx) a { color: inherit; text-decoration: none; }
.lx :focus-visible { outline: 2px solid var(--gold); outline-offset: 3px; border-radius: 10px; }
.lx .sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
.lx-shell { width: min(1200px, 100% - 40px); margin-inline: auto; }
.lx section + section { margin-top: 112px; }

.lx-btn { display: inline-flex; align-items: center; justify-content: center; height: 48px; padding: 0 26px; border-radius: 999px;
  font-size: 15px; font-weight: 600; white-space: nowrap; transition: background .25s, transform .25s var(--ease); }
.lx-btn:active { transform: scale(.98); }
.lx-btn--gold { color: #12100b; background: var(--gold); }
.lx-btn--gold:hover { background: #ecd394; }
.lx-btn--ink { color: var(--gold); background: #12100b; }
.lx-btn--ink:hover { background: #262017; }
.lx-link { display: inline-flex; align-items: center; gap: 8px; font-size: 14px; font-weight: 600; color: var(--gold); }
.lx-link::after { content: ""; width: 18px; height: 1px; background: currentColor; transition: width .3s var(--ease); }
.lx-link:hover::after { width: 30px; }
.lx-logo { flex: none; display: grid; place-items: center; width: 48px; height: 48px; border-radius: 14px; background: #fff; overflow: hidden; }
.lx-logo img { width: 78%; height: 78%; object-fit: contain; }
.lx-logo .gp-ucard__initial { font-weight: 700; color: #12100b; }
.lx-logo--sm { width: 34px; height: 34px; border-radius: 10px; }

/* top: greeting, spotlight + switcher, account */
.lx-top { padding-top: 56px; }
.lx-greet h1 { font-size: clamp(34px, 4vw, 52px); line-height: 1.08; font-weight: 500; letter-spacing: -.035em; }
.lx-greet p { margin-top: 14px; font-size: 17px; color: var(--sub); }
.lx-greet b { font-weight: 600; color: var(--gold); }
.lx-top__grid { margin-top: 44px; display: grid; grid-template-columns: minmax(0, 1fr) 360px; gap: 28px; align-items: start; }
.lx-spot { display: grid; grid-template-columns: minmax(0, 1fr) 240px; border-radius: 20px; overflow: hidden; border: 1px solid var(--gline);
  background: radial-gradient(70% 90% at 0% 0%, rgba(212, 175, 55, .16), transparent 60%), var(--panel); }
.lx-spot__stage { display: grid; padding: 36px; }
.lx-deal { grid-area: 1 / 1; display: grid; align-content: start; gap: 0; }
.lx-deal[hidden] { display: none; }
.lx-deal.is-in > * { animation: lx-rise .7s var(--ease) both; }
.lx-deal.is-in > :nth-child(2) { animation-delay: .05s; } .lx-deal.is-in > :nth-child(3) { animation-delay: .1s; }
.lx-deal.is-in > :nth-child(4) { animation-delay: .15s; } .lx-deal.is-in > :nth-child(5) { animation-delay: .2s; }
@keyframes lx-rise { from { opacity: 0; transform: translateY(12px); } }
@media (prefers-reduced-motion: reduce) { .lx-deal.is-in > * { animation: none; } }
.lx-deal__id { display: flex; align-items: center; gap: 14px; }
.lx-deal__id h2 { font-size: 19px; font-weight: 600; }
.lx-deal__id p { margin-top: 2px; font-size: 13px; color: var(--dim); }
.lx-deal__rate { margin-top: 36px; font-size: clamp(64px, 8vw, 104px); line-height: .9; font-weight: 500; letter-spacing: -.05em; color: var(--gold);
  font-variant-numeric: tabular-nums; }
.lx-deal__cap { margin-top: 10px; font-size: 14px; color: var(--sub); }
.lx-deal__terms { display: flex; flex-wrap: wrap; gap: 14px 40px; margin: 36px 0 32px; padding-top: 22px; border-top: 1px solid var(--hair); }
.lx-deal__terms dt { font-size: 12px; color: var(--dim); }
.lx-deal__terms dd { margin: 4px 0 0; font-size: 16px; font-weight: 600; }
.lx-deal .lx-btn { justify-self: start; }
.lx-tabs { display: grid; align-content: stretch; border-left: 1px solid var(--hair); background: rgba(0, 0, 0, .18); }
.lx-tab { display: grid; grid-template-columns: auto minmax(0, 1fr); grid-template-areas: "logo name" "logo rate"; align-content: center; gap: 2px 12px;
  padding: 18px 20px; border: 0; border-bottom: 1px solid var(--hair); background: none; color: var(--sub); text-align: left; cursor: pointer; font: inherit;
  transition: background .25s, color .25s; }
.lx-tab:last-child { border-bottom: 0; }
.lx-tab .lx-logo { grid-area: logo; opacity: .7; transition: opacity .25s; }
.lx-tab__name { grid-area: name; font-size: 14px; font-weight: 600; }
.lx-tab__rate { grid-area: rate; font-size: 13px; font-variant-numeric: tabular-nums; }
.lx-tab:hover { color: var(--ink); background: rgba(255, 255, 255, .03); }
.lx-tab[aria-selected="true"] { color: var(--ink); background: rgba(226, 195, 114, .07); box-shadow: inset 2px 0 0 var(--gold); }
.lx-tab[aria-selected="true"] .lx-logo { opacity: 1; }
.lx-tab[aria-selected="true"] .lx-tab__rate { color: var(--gold); }

.lx-acct { display: grid; gap: 20px; }
.lx-orders { padding: 22px 22px 20px; border-radius: 20px; background: var(--panel); border: 1px solid var(--hair); }
.lx-orders h2 { display: flex; align-items: center; gap: 10px; font-size: 15px; font-weight: 600; }
.lx-orders h2 span { display: grid; place-items: center; min-width: 22px; height: 22px; border-radius: 999px; font-size: 12px; color: #12100b; background: var(--gold); }
.lx-orders ul { margin: 8px 0 16px; }
.lx-orders li { display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 14px 0; }
.lx-orders li + li { border-top: 1px solid var(--hair); }
.lx-order__name { font-size: 14px; font-weight: 600; }
.lx-order__meta { margin-top: 3px; font-size: 12px; color: var(--dim); }
.lx-order__state { flex: none; font-size: 12px; font-weight: 600; }
.lx-order__state--warn { color: #f0a35e; }
.lx-order__state--info { color: var(--gold); }

/* IPO band */
.lx-ipo { border-block: 1px solid var(--gline); background: linear-gradient(90deg, rgba(212, 175, 55, .07), transparent 60%); }
.lx-ipo__in { display: grid; grid-template-columns: minmax(0, 1.3fr) minmax(0, 1.6fr) auto; align-items: center; gap: 40px; padding-block: 44px; }
.lx-live { display: flex; align-items: center; gap: 8px; font-size: 13px; font-weight: 600; color: #5fd08a; }
.lx-live i { width: 7px; height: 7px; border-radius: 50%; background: #5fd08a; }
@media (prefers-reduced-motion: no-preference) { .lx-live i { animation: lx-pulse 2.4s ease-in-out infinite; } }
@keyframes lx-pulse { 0%, 100% { box-shadow: 0 0 0 0 rgba(95, 208, 138, .45); } 60% { box-shadow: 0 0 0 7px rgba(95, 208, 138, 0); } }
.lx-ipo h2 { margin-top: 14px; display: flex; align-items: center; gap: 14px; font-size: 24px; line-height: 1.25; font-weight: 500; letter-spacing: -.015em; }
.lx-ipo__facts { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); }
.lx-ipo__facts div { padding-left: 20px; border-left: 1px solid var(--hair); }
.lx-ipo__facts dt { font-size: 12px; color: var(--dim); }
.lx-ipo__facts dd { margin: 6px 0 0; font-size: 18px; font-weight: 600; white-space: nowrap; }
.lx-ipo__facts div:first-child dd { color: var(--gold); }
.lx-ipo__cta { display: grid; justify-items: center; gap: 14px; }

/* ledger */
.lx-sec { display: flex; align-items: end; justify-content: space-between; gap: 24px; flex-wrap: wrap; }
.lx-sec h2, .lx-cols h2, .lx-why h2 { font-size: clamp(26px, 2.6vw, 34px); line-height: 1.15; font-weight: 500; letter-spacing: -.025em; }
.lx-segs { display: inline-flex; padding: 4px; border-radius: 999px; border: 1px solid var(--hair); background: var(--panel); }
.lx-seg { height: 38px; padding: 0 18px; border: 0; border-radius: 999px; background: none; color: var(--sub); font: inherit; font-size: 14px; font-weight: 600; cursor: pointer;
  transition: background .25s, color .25s; }
.lx-seg[aria-selected="true"] { color: #12100b; background: var(--gold); }
.lx-led__sub { margin-top: 14px; font-size: 15px; color: var(--sub); }
.lx-led__head, .lx-row { display: grid; grid-template-columns: minmax(0, 1fr) 110px 110px 130px; align-items: center; gap: 20px; }
.lx-led__head { margin-top: 36px; padding: 0 20px 12px 88px; font-size: 12px; color: var(--dim); border-bottom: 1px solid var(--hair); }
.lx-led__head span:last-child { text-align: right; }
.lx-led ul { margin-bottom: 24px; }
.lx-row { grid-template-columns: auto minmax(0, 1fr) 110px 110px 130px; padding: 20px; border-bottom: 1px solid var(--hair); transition: background .25s; }
.lx-row:hover { background: rgba(255, 255, 255, .025); }
.lx-row__id { display: grid; gap: 4px; min-width: 0; }
.lx-row__id b { font-size: 16px; font-weight: 600; }
.lx-row__id small { font-size: 13px; color: var(--dim); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.lx-row__m { font-size: 15px; font-weight: 500; color: var(--sub); }
.lx-row__rate { text-align: right; font-size: 30px; font-weight: 500; letter-spacing: -.03em; color: var(--gold); font-variant-numeric: tabular-nums; }
.lx-row__rate small { font-size: 15px; margin-left: 2px; letter-spacing: 0; }

/* collections */
.lx-cols ul { margin-top: 28px; display: flex; flex-wrap: wrap; gap: 12px; }
.lx-pill { display: inline-flex; align-items: center; gap: 10px; height: 56px; padding: 0 22px 0 14px; border-radius: 999px; border: 1px solid var(--hair);
  background: var(--panel); font-size: 15px; font-weight: 600; transition: border-color .25s, transform .25s var(--ease); }
.lx-pill:hover { border-color: var(--gline); transform: translateY(-2px); }
.lx-pill img { width: 28px; height: 28px; object-fit: contain; }

/* why */
.lx-why { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); gap: 28px 72px; }
.lx-why__lead p { margin-top: 18px; max-width: 34ch; font-size: 16px; line-height: 1.6; color: var(--sub); }
.lx-why__list { display: grid; }
.lx-why__list li { display: grid; gap: 8px; padding: 24px 0; border-top: 1px solid var(--hair); }
.lx-why__list li:first-child { padding-top: 0; border-top: 0; }
.lx-why__list h3 { font-size: 18px; font-weight: 600; }
.lx-why__list p { font-size: 15px; line-height: 1.65; color: var(--sub); max-width: 62ch; }
.lx-stats { grid-column: 1 / -1; margin-top: 40px; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); border-top: 1px solid var(--gline); }
.lx-stats li { padding: 28px 0 0; font-size: clamp(18px, 1.8vw, 22px); font-weight: 500; letter-spacing: -.01em; color: var(--gold); }
.lx-stats li + li { padding-left: 24px; border-left: 1px solid var(--hair); }

/* refer: the one gold surface */
.lx-refer { background: linear-gradient(120deg, #e8c96f 0%, #d4af37 55%, #b8922a 100%); color: #12100b; }
.lx-refer__in { display: flex; align-items: center; justify-content: space-between; gap: 32px; padding-block: 56px; }
.lx-refer h2 { font-size: clamp(26px, 2.8vw, 36px); line-height: 1.15; font-weight: 600; letter-spacing: -.025em; }
.lx-refer p { margin-top: 10px; font-size: 16px; color: rgba(18, 16, 11, .72); }

/* help + app */
.lx-close { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 28px; }
.lx-help, .lx-app { padding: 36px; border-radius: 20px; border: 1px solid var(--hair); background: var(--panel); }
.lx-close h2 { font-size: 24px; font-weight: 500; letter-spacing: -.015em; }
.lx-help > p, .lx-app p { margin-top: 10px; font-size: 15px; line-height: 1.6; color: var(--sub); max-width: 44ch; }
.lx-help dl { margin: 24px 0; display: grid; gap: 10px; }
.lx-help dl div { display: flex; gap: 16px; font-size: 15px; }
.lx-help dt { width: 52px; color: var(--dim); }
.lx-help dd { margin: 0; font-weight: 600; }
.lx-help dd a:hover { color: var(--gold); }
.lx-app { display: flex; align-items: center; justify-content: space-between; gap: 24px;
  background: radial-gradient(80% 100% at 100% 0%, rgba(212, 175, 55, .14), transparent 60%), var(--panel); }
.lx-app__icon { border-radius: 12px; margin-bottom: 18px; }
.lx-app .lx-btn { margin-top: 24px; }
.lx-app__qr { flex: none; padding: 10px; border-radius: 14px; background: #fff; }

/* reveal (pages/_reveal.js adds .reveal-ready) */
.reveal-ready .lx [data-reveal] { opacity: 0; transform: translateY(24px); transition: opacity .9s var(--ease), transform .9s var(--ease); }
.reveal-ready .lx [data-reveal].is-in { opacity: 1; transform: none; }

/* the portfolio card keeps its own gold; on a dark page it needs no outer shadow */
.lx .pf-gcard { margin: 0; }

@media (max-width: 1099px) {
  .lx-top__grid { grid-template-columns: minmax(0, 1fr); }
  .lx-acct { grid-template-columns: repeat(2, minmax(0, 1fr)); align-items: start; }
  .lx-ipo__in { grid-template-columns: minmax(0, 1fr); gap: 28px; }
  .lx-ipo__cta { justify-items: start; grid-auto-flow: column; align-items: center; gap: 24px; justify-content: start; }
  .lx-why { grid-template-columns: minmax(0, 1fr); }
}
@media (max-width: 767px) {
  .lx { padding-bottom: 64px; }
  .lx-shell { width: calc(100% - 32px); }
  .lx section + section { margin-top: 72px; }
  .lx-top { padding-top: 28px; }
  .lx-top__grid { margin-top: 28px; }
  .lx-acct { grid-template-columns: minmax(0, 1fr); }
  .lx-spot { grid-template-columns: minmax(0, 1fr); }
  .lx-spot__stage { padding: 24px 20px; }
  .lx-deal__rate { margin-top: 24px; }
  .lx-deal__terms { gap: 14px 28px; margin: 24px 0; }
  .lx-deal .lx-btn { justify-self: stretch; }
  .lx-tabs { grid-auto-flow: column; grid-auto-columns: minmax(0, 1fr); border-left: 0; border-top: 1px solid var(--hair); }
  .lx-tab { grid-template-columns: minmax(0, 1fr); grid-template-areas: "name" "rate"; padding: 14px 12px; border-bottom: 0; border-right: 1px solid var(--hair); }
  .lx-tab:last-child { border-right: 0; }
  .lx-tab .lx-logo { display: none; }
  .lx-tab[aria-selected="true"] { box-shadow: inset 0 2px 0 var(--gold); }
  .lx-ipo__in { padding-block: 32px; }
  .lx-ipo h2 { font-size: 20px; }
  .lx-ipo__facts { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px 0; }
  .lx-ipo__facts div:nth-child(3) { padding-left: 0; border-left: 0; }
  .lx-ipo__facts div:first-child { padding-left: 0; border-left: 0; }
  .lx-ipo__cta { grid-auto-flow: row; justify-items: stretch; justify-content: stretch; }
  .lx-sec { align-items: start; }
  .lx-segs { width: 100%; } .lx-seg { flex: 1; padding: 0 10px; font-size: 13px; }
  .lx-led__head { display: none; }
  .lx-row { grid-template-columns: auto minmax(0, 1fr) auto; grid-template-areas: "logo id rate" "logo meta rate"; gap: 4px 14px; padding: 16px 0; }
  .lx-row .lx-logo { grid-area: logo; width: 40px; height: 40px; }
  .lx-row__id { grid-area: id; } .lx-row__id small { display: none; }
  .lx-row__m { grid-area: meta; font-size: 13px; }
  .lx-row__m + .lx-row__m { display: none; }
  .lx-row__rate { grid-area: rate; font-size: 24px; }
  .lx-pill { height: 48px; font-size: 14px; }
  .lx-stats { grid-template-columns: repeat(2, minmax(0, 1fr)); row-gap: 20px; }
  .lx-stats li:nth-child(3) { padding-left: 0; border-left: 0; }
  .lx-refer__in { flex-direction: column; align-items: stretch; padding-block: 40px; }
  .lx-close { grid-template-columns: minmax(0, 1fr); }
  .lx-help, .lx-app { padding: 24px 20px; }
  .lx-app__qr { display: none; }
}
</style>
"""

SCRIPT = """<script>
// Tabs: the spotlight's deal switcher and the ledger's two lists. Arrow keys move between tabs.
(function () {
  [].forEach.call(document.querySelectorAll('.lx [role=tablist]'), function (list) {
    var tabs = [].slice.call(list.querySelectorAll('[role=tab]'));
    function pick(t) {
      tabs.forEach(function (x) {
        var on = x === t, panel = document.getElementById(x.getAttribute('aria-controls'));
        x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1;
        panel.hidden = !on;
        if (on) { panel.classList.remove('is-in'); void panel.offsetWidth; panel.classList.add('is-in'); }
      });
    }
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { pick(t); });
      t.addEventListener('keydown', function (e) {
        var d = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key];
        if (!d) return;
        e.preventDefault();
        var n = tabs[(i + d + tabs.length) % tabs.length]; n.focus(); pick(n);
      });
    });
  });
})();
</script>
"""


def main():
    X.assemble(body(), OUT, "Explore | GoldenPi",
               "pages/_explore_app3.py (user-explore-app2.html's content, redesigned as one dark luxury page)",
               style=STYLE, script=SCRIPT)


if __name__ == "__main__":
    main()
