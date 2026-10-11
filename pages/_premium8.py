#!/usr/bin/env python3
"""Write home-premium8.html: the homepage in black, white and gold, told with as
few words as the page can carry. Figures do the talking; prose is cut, not
rewritten.

  the deal      headline, then the top 3 Bond Utsav rates as one ruled row
  the account   three instruments as a large type index, one figure each
  the case      what Rs 1 lakh earns, as coin stacks on an ivory sheet
  the trust     a giant 5%, then three reasons, titles only
  the proof     three platform figures and one review
  the pocket    a large QR, Google Play and the real app screen

Reviewed against taste-skill (2026-10-11): one dark theme, one gold accent,
20px surfaces and pill controls, one small label in the hero and no other
eyebrows, no em-dashes, no div-built screens, no scroll listeners, every motion
behind prefers-reduced-motion. Generated imagery was unavailable (Figma AI
usage limit); the visuals are the brand's pi mark, issuer logos and the app.

Chrome (head links, navbar, footer, the shared count-up and reveal scripts) is
home-premium3's; only its page styles, <body> class and <main> are replaced.
Every string is home-premium2's or home-premium3's own; nothing new is written.

    python3 pages/_premium8.py && python3 pages/_build.py
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "home-premium3.html")
OUT = os.path.join(HERE, "home-premium8.html")
IMG = "../assets/img/"

# DATA: top 3 Bond Utsav deals, index.html snapshot 2026-09-25, as home-premium2 shows them.
DEALS = [
    ("Akara", "GPID102720.AKARA-CAPITAL-ADVISORS-PRIVATE-LIMITED-2x.png", "13.00", "ACUITE BBB+", "Monthly",
     "https://uatnew.goldenpi.com/bonds/GPID107435/akara-1300-bond-yield?src=view_details&amp;tenureDate=03-Dec-2027"),
    ("NeoGrowth", "GPID104095.Neogrowth-new-logo-1-.jpg", "13.00", "ICRA BBB", "Half Yearly",
     "https://uatnew.goldenpi.com/bonds/GPID107371/neogrowth-1300-bond-yield?src=view_details&amp;tenureDate=30-Apr-2028"),
    ("Best Capital", "GPID107347.Best-Capital.png", "13.00", "IVR BBB", "Monthly",
     "https://uatnew.goldenpi.com/bonds/GPID107433/best-capital-1300-bond-yield?src=view_details&amp;tenureDate=11-Sep-2029"),
]

# (name, href, figure, figure label, icon): home-premium2's bento, prose cut.
INSTRUMENTS = [
    ("Corporate Bonds", "corporate-bonds.html", "13.8%", "Returns, up to", "ph-certificate"),
    ("Fixed Deposits", "fixed-deposits.html", "8.5%", "Highest returns", "ph-vault"),
    ("NCD IPOs", "bond-ipo-online.html", None, "Live now", "ph-rocket-launch"),
]

# (label, rate, GoldenPi's own): home-premium2's ladder. The rupee figure is the
# rate on the figure's own Rs 1 lakh for one year.
EARN = [("Savings account", 2.7, False), ("Large bank FD", 6.5, False),
        ("FDs on GoldenPi", 8.5, True), ("Bonds on GoldenPi", 13.8, True)]

# home-premium3's bento, titles only.
REASONS = [("ph-hand-coins", "Zero brokerage"), ("ph-shield-check", "One of the first OBPPs"),
           ("ph-globe-hemisphere-east", "Investing options for NRIs")]

ARROW = '<i class="ph-bold ph-arrow-up-right" aria-hidden="true"></i>'


def deal(i, d):
    name, logo, rate, rating, payout, url = d
    return f"""
        <a class="p8-deal" href="{url}" style="--i:{i}" aria-label="{name}, {rate}% returns, know more">
          <span class="p8-deal__who"><img src="{IMG}{logo}" alt="" width="40" height="40">{name}</span>
          <span class="p8-deal__rate"><span data-count>{rate}</span><small>%</small></span>
          <span class="p8-deal__meta">{rating}<span aria-hidden="true">/</span>{payout}</span>
          <span class="p8-deal__go">{ARROW}</span>
        </a>"""


def instrument(i, x):
    name, href, fig, label, icon = x
    figure = (f'<span class="p8-idx__fig">{fig}<small>{label}</small></span>' if fig
              else f'<span class="p8-idx__live">{label}</span>')
    return f"""
        <a class="p8-idx__row" href="{href}" style="--i:{i}">
          <i class="ph-thin {icon} p8-idx__icon" aria-hidden="true"></i>
          <span class="p8-idx__name">{name}</span>
          {figure}
          <span class="p8-idx__go">{ARROW}</span>
        </a>"""


def coin(i, e):
    label, rate, own = e
    rupees = "{:,}".format(round(rate * 1000))
    return f"""
          <li class="p8-coin{' p8-coin--gold' if own else ''}" style="--f:{rate / 13.8:.3f}; --i:{i}">
            <span class="p8-coin__amt">&#8377;<span data-count>{rupees}</span></span>
            <span class="p8-coin__stack" aria-hidden="true"></span>
            <span class="p8-coin__lbl"><b>{rate}%</b>{label}</span>
          </li>"""


def reason(i, r):
    icon, title = r
    return f'<li style="--i:{i}"><i class="ph-light {icon}" aria-hidden="true"></i>{title}</li>'


STYLE = r"""<style>
/* home-premium8: page-only styles, p8- prefix. Written by pages/_premium8.py.
   Black is the market, ivory is the paper you own, gold is what it pays.
   Shape lock: surfaces 20px, controls are pills, rows are unboxed. */
.p8 {
  --k: #0a0908; --k2: #12110e; --line: rgba(244, 242, 237, 0.1);
  --paper: #f5f4f0; --paper-2: #e9e7e0; --ink: #14120d; --ink-2: #5d5950;
  --gold: #d4af37; --gold-hi: #ecd27f; --gold-lo: #9c7b22;
  --tx: #f4f2ed; --tx-2: #a9a59b;
  --ease: cubic-bezier(0.16, 1, 0.3, 1);
  background: var(--k);
}
body.p8-page { background: #0a0908; }
.p8 main { color: var(--tx); font-family: "Satoshi", system-ui, sans-serif; }
.p8 main ::selection { background: var(--gold); color: var(--ink); }
.p8-page::after { /* fixed film grain, never repaints with the scroll */
  content: ""; position: fixed; inset: 0; z-index: 60; pointer-events: none; opacity: 0.045;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}
.p8-shell { width: min(1240px, 100% - 32px); margin-inline: auto; }
@media (min-width: 768px) { .p8-shell { width: min(1240px, 100% - 80px); } }
.p8-sec { padding-block: clamp(96px, 12vw, 176px); }
.p8-h2 { color: var(--tx); font-size: clamp(34px, 4.2vw, 60px); font-weight: 700; letter-spacing: -0.04em; line-height: 1.04; max-width: 16ch; text-wrap: balance; }
.p8 em { font-style: normal; color: var(--gold); }
.p8 a:focus-visible { outline: 2px solid var(--gold); outline-offset: 4px; }

.p8-btn { display: inline-flex; align-items: center; gap: 10px; min-height: 54px; padding: 0 28px; border-radius: 999px; font-size: 16px; font-weight: 700; white-space: nowrap; transition: transform 0.35s var(--ease), background-color 0.35s var(--ease), border-color 0.35s var(--ease); }
.p8-btn:active { transform: scale(0.98); }
.p8-btn--gold { background: var(--gold); color: var(--ink); }
.p8-btn--gold:hover { background: var(--gold-hi); }
.p8-btn--line { border: 1px solid rgba(244, 242, 237, 0.26); color: var(--tx); }
.p8-btn--line:hover { border-color: var(--gold); }
.p8-btn i { transition: transform 0.35s var(--ease); }
.p8-btn:hover i { transform: translateX(4px); }

/* ------------------------------------------------------------ the deal */
.p8-hero {
  position: relative; isolation: isolate; overflow: hidden;
  display: flex; flex-direction: column; justify-content: space-between; gap: 72px;
  min-height: calc(100dvh - 72px); padding-block: clamp(56px, 8vw, 96px) clamp(40px, 5vw, 64px);
  background: radial-gradient(48% 60% at 86% 30%, rgba(212, 175, 55, 0.16), transparent 70%), var(--k);
}
.p8-hero__pi { position: absolute; z-index: -1; right: -6vw; top: 50%; width: min(64vw, 860px); height: auto; transform: translateY(-58%); pointer-events: none; }
.p8-cred { color: var(--tx-2); font-size: 14px; letter-spacing: 0.04em; }
.p8-cred i { color: var(--gold); margin-right: 6px; }
.p8-h1 { margin-top: 28px; color: var(--tx); font-size: clamp(46px, 6.6vw, 96px); font-weight: 700; letter-spacing: -0.05em; line-height: 0.98; }
.p8-h1 span { display: block; }
.p8-ctas { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 44px; }

.p8-deals { display: grid; border-top: 1px solid var(--line); position: relative; }
.p8-deals::before { /* a line of gold light runs once along the rule */
  content: ""; position: absolute; top: -1px; left: 0; width: 32%; height: 1px;
  background: linear-gradient(90deg, transparent, var(--gold-hi), transparent); opacity: 0;
}
@media (min-width: 900px) { .p8-deals { grid-template-columns: repeat(3, 1fr); } }
.p8-deal {
  position: relative; display: grid; grid-template-columns: 1fr auto; align-items: end; gap: 6px 16px;
  padding: 26px 0 8px;
}
.p8-deal + .p8-deal { border-top: 1px solid var(--line); }
@media (min-width: 900px) {
  .p8-deal { padding: 30px 32px 6px; }
  .p8-deal:first-child { padding-left: 0; }
  .p8-deal + .p8-deal { border-top: 0; border-left: 1px solid var(--line); }
}
.p8-deal__who { grid-column: 1 / -1; display: flex; align-items: center; gap: 12px; color: var(--tx); font-size: 16px; font-weight: 500; }
.p8-deal__who img { width: 40px; height: 40px; padding: 4px; border-radius: 999px; background: #fff; object-fit: contain; }
.p8-deal__rate { margin-top: 18px; color: var(--gold); font-size: clamp(48px, 4.6vw, 68px); font-weight: 700; letter-spacing: -0.05em; line-height: 0.9; font-variant-numeric: tabular-nums; }
.p8-deal__rate small { font-size: 0.42em; letter-spacing: 0; margin-left: 2px; }
.p8-deal__meta { grid-column: 1; color: var(--tx-2); font-size: 14px; }
.p8-deal__meta span { margin-inline: 8px; opacity: 0.4; }
.p8-deal__go { grid-column: 2; grid-row: 2 / 4; align-self: center; display: grid; place-items: center; width: 48px; height: 48px; border-radius: 999px; border: 1px solid var(--line); color: var(--tx); transition: background-color 0.4s var(--ease), color 0.4s var(--ease), border-color 0.4s var(--ease), transform 0.4s var(--ease); }
.p8-deal:hover .p8-deal__go { background: var(--gold); border-color: var(--gold); color: var(--ink); transform: rotate(45deg); }

@media (prefers-reduced-motion: no-preference) {
  .p8-rise { animation: p8-rise 1.1s var(--ease) backwards; animation-delay: calc(var(--d, 0) * 120ms); }
  .p8-deal { animation: p8-rise 1s var(--ease) backwards; animation-delay: calc(600ms + var(--i) * 140ms); }
  .p8-deals::before { animation: p8-sweep 2.4s var(--ease) 1.1s; }
  .p8-hero__pi { animation: p8-fade 2.4s var(--ease) backwards 0.2s; }
}
@keyframes p8-rise { from { opacity: 0; transform: translateY(28px); } }
@keyframes p8-fade { from { opacity: 0; } }
@keyframes p8-sweep { 0% { opacity: 0; transform: translateX(-30%); } 20% { opacity: 1; } 100% { opacity: 0; transform: translateX(310%); } }

/* --------------------------------------------------------- the account */
.p8-idx { margin-top: 56px; border-top: 1px solid var(--line); }
.p8-idx__row {
  position: relative; isolation: isolate; display: grid; align-items: center; gap: 8px 24px;
  grid-template-columns: auto 1fr auto; padding: 28px 0; border-bottom: 1px solid var(--line);
}
@media (min-width: 768px) { .p8-idx__row { grid-template-columns: 64px 1fr auto 56px; padding: 34px 0; } }
.p8-idx__row::before { /* the row fills with gold from the left on hover */
  content: ""; position: absolute; inset: 0; z-index: -1; background: linear-gradient(90deg, rgba(212, 175, 55, 0.1), transparent 70%);
  transform: scaleX(0); transform-origin: left; transition: transform 0.7s var(--ease);
}
.p8-idx__row:hover::before { transform: none; }
.p8-idx__icon { color: var(--gold); font-size: 40px; }
.p8-idx__name { color: var(--tx); font-size: clamp(28px, 4.4vw, 60px); font-weight: 500; letter-spacing: -0.04em; line-height: 1; transition: transform 0.7s var(--ease); }
.p8-idx__row:hover .p8-idx__name { transform: translateX(12px); }
.p8-idx__fig { grid-column: 2; color: var(--gold); font-size: clamp(22px, 2.2vw, 30px); font-weight: 700; letter-spacing: -0.03em; text-align: left; }
.p8-idx__fig small { display: block; color: var(--tx-2); font-size: 13px; font-weight: 400; letter-spacing: 0; }
.p8-idx__live { grid-column: 2; justify-self: start; padding: 6px 14px; border: 1px solid rgba(212, 175, 55, 0.5); border-radius: 999px; color: var(--gold-hi); font-size: 13px; font-weight: 700; }
@media (min-width: 768px) { .p8-idx__fig, .p8-idx__live { grid-column: 3; justify-self: end; text-align: right; } }
.p8-idx__go { display: none; }
@media (min-width: 768px) { .p8-idx__go { display: grid; place-items: center; width: 48px; height: 48px; border-radius: 999px; border: 1px solid var(--line); color: var(--tx); transition: all 0.4s var(--ease); } }
.p8-idx__row:hover .p8-idx__go { background: var(--gold); border-color: var(--gold); color: var(--ink); transform: rotate(45deg); }
@media (max-width: 767px) { .p8-idx__icon { grid-row: span 2; font-size: 32px; } }
@media (prefers-reduced-motion: no-preference) {
  .reveal-ready .p8-idx[data-reveal] { opacity: 1; transform: none; }
  .reveal-ready .p8-idx .p8-idx__row { opacity: 0; transform: translateY(24px); transition: opacity 0.8s var(--ease), transform 0.9s var(--ease); transition-delay: calc(var(--i) * 120ms); }
  .reveal-ready .p8-idx.is-in .p8-idx__row { opacity: 1; transform: none; }
}

/* ------------------------------------------------------------ the case */
.p8-sheet {
  display: grid; gap: 48px; padding: clamp(32px, 5vw, 72px); border-radius: 20px; color: var(--ink);
  background: radial-gradient(70% 70% at 100% 0%, rgba(212, 175, 55, 0.16), transparent 60%), linear-gradient(160deg, #fbfaf7, var(--paper-2));
  box-shadow: 0 60px 120px -50px rgba(0, 0, 0, 0.9);
}
@media (min-width: 1024px) { .p8-sheet { grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr); align-items: end; } }
.p8-sheet .p8-h2 { color: var(--ink); }
.p8-sheet__cap { margin-top: 20px; color: var(--ink-2); font-size: 15px; }
.p8-sheet__cap b { display: block; color: var(--ink); font-size: 18px; }
.p8-coins { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: clamp(10px, 2vw, 24px); align-items: end; }
.p8-coin__amt { margin-bottom: 10px; color: var(--ink-2); font-size: clamp(14px, 1.4vw, 18px); font-weight: 700; font-variant-numeric: tabular-nums; }
.p8-coin--gold .p8-coin__amt { color: var(--ink); }
.p8-coin__stack { display: block; height: calc(var(--f) * clamp(190px, 22vw, 290px)); border-radius: 12px 12px 4px 4px; background: repeating-linear-gradient(to top, #d3d0c7 0 9px, #bdb9ae 9px 10px); transform-origin: bottom; }
.p8-coin { display: flex; flex-direction: column; }
.p8-coin--gold .p8-coin__stack { background: linear-gradient(90deg, rgba(255, 255, 255, 0.3), transparent 45%, rgba(0, 0, 0, 0.14)), repeating-linear-gradient(to top, var(--gold) 0 9px, var(--gold-lo) 9px 10px); }
.p8-coin__lbl { margin-top: 14px; color: var(--ink-2); font-size: 12px; line-height: 1.35; }
.p8-coin__lbl b { display: block; color: var(--ink); font-size: clamp(18px, 2vw, 26px); letter-spacing: -0.02em; }
.p8-coin--gold .p8-coin__lbl b { color: var(--gold-lo); }
@media (prefers-reduced-motion: no-preference) {
  .reveal-ready .p8-sheet .p8-coin__stack { transform: scaleY(0.02); transition: transform 1.4s var(--ease); transition-delay: calc(250ms + var(--i) * 150ms); }
  .reveal-ready .p8-sheet.is-in .p8-coin__stack { transform: none; }
}

/* ----------------------------------------------------------- the trust */
.p8-five { display: grid; gap: 24px; align-items: end; margin-top: 48px; }
@media (min-width: 900px) { .p8-five { grid-template-columns: auto 1fr; gap: 56px; } }
.p8-five__num {
  font-size: clamp(150px, 22vw, 300px); font-weight: 900; letter-spacing: -0.07em; line-height: 0.8;
  background: linear-gradient(170deg, var(--gold-hi), var(--gold) 45%, var(--gold-lo)); -webkit-background-clip: text; background-clip: text; color: transparent;
}
.p8-five__line { padding-bottom: 8px; color: var(--tx); font-size: clamp(22px, 2.4vw, 32px); font-weight: 500; letter-spacing: -0.02em; max-width: 14ch; }
.p8-reasons { display: grid; margin-top: 64px; border-top: 1px solid var(--line); }
@media (min-width: 768px) { .p8-reasons { grid-template-columns: repeat(3, 1fr); } }
.p8-reasons li { display: flex; align-items: center; gap: 16px; padding: 28px 0; color: var(--tx); font-size: 19px; font-weight: 500; }
.p8-reasons li + li { border-top: 1px solid var(--line); }
@media (min-width: 768px) { .p8-reasons li + li { border-top: 0; border-left: 1px solid var(--line); padding-left: 32px; } }
.p8-reasons i { color: var(--gold); font-size: 30px; }
@media (prefers-reduced-motion: no-preference) {
  .reveal-ready .p8-five .p8-five__num { opacity: 0; transform: translateY(40px) scale(0.96); transform-origin: left bottom; transition: opacity 1.2s var(--ease), transform 1.4s var(--ease); }
  .reveal-ready .p8-five.is-in .p8-five__num { opacity: 1; transform: none; }
}

/* ----------------------------------------------------------- the proof */
.p8-proof { border-block: 1px solid var(--line); background: radial-gradient(40% 70% at 50% 0%, rgba(212, 175, 55, 0.1), transparent 70%), var(--k2); }
.p8-stats { display: grid; gap: 36px; }
@media (min-width: 900px) { .p8-stats { grid-template-columns: repeat(3, 1fr); gap: 0; } .p8-stats > div + div { padding-left: 48px; border-left: 1px solid var(--line); } }
.p8-stats dt { color: var(--gold); font-size: clamp(52px, 6vw, 88px); font-weight: 700; letter-spacing: -0.05em; line-height: 1; font-variant-numeric: tabular-nums; white-space: nowrap; }
.p8-stats dt small { margin-left: 6px; color: var(--tx); font-size: 0.32em; letter-spacing: 0; }
.p8-stats dd { margin-top: 12px; color: var(--tx-2); font-size: 15px; max-width: 24ch; }
.p8-quote { margin: clamp(80px, 9vw, 128px) auto 0; max-width: 820px; text-align: center; }
.p8-quote__stars { color: var(--gold); font-size: 18px; letter-spacing: 6px; }
.p8-quote blockquote { margin-top: 24px; color: var(--tx); font-size: clamp(26px, 3vw, 42px); font-weight: 500; letter-spacing: -0.03em; line-height: 1.22; text-wrap: balance; }
.p8-quote figcaption { margin-top: 24px; color: var(--tx-2); font-size: 15px; }

/* ---------------------------------------------------------- the pocket */
.p8-app { display: grid; gap: 56px; align-items: center; }
@media (min-width: 1024px) { .p8-app { grid-template-columns: minmax(0, 1fr) auto minmax(0, 300px); gap: 64px; } }
.p8-app__icon { width: 64px; height: 64px; border-radius: 16px; margin-bottom: 32px; box-shadow: 0 18px 44px -14px rgba(212, 175, 55, 0.5); }
.p8-play { display: inline-flex; align-items: center; gap: 12px; margin-top: 40px; min-height: 58px; padding: 0 24px; border-radius: 999px; background: var(--tx); color: var(--ink); transition: background-color 0.35s var(--ease), transform 0.35s var(--ease); }
.p8-play:hover { background: #fff; }
.p8-play:active { transform: scale(0.98); }
.p8-play i { font-size: 24px; }
.p8-play span { font-size: 11px; line-height: 1.15; }
.p8-play b { display: block; font-size: 17px; }
.p8-qr { justify-self: center; text-align: center; }
.p8-qr img { display: block; width: clamp(200px, 20vw, 248px); height: auto; filter: drop-shadow(0 30px 50px rgba(0, 0, 0, 0.6)); }
.p8-qr p { margin-top: 16px; color: var(--tx-2); font-size: 14px; }
.p8-phone { justify-self: center; width: min(280px, 72vw); padding: 10px; border-radius: 44px; background: #050504; border: 1px solid rgba(244, 242, 237, 0.14); box-shadow: 0 60px 100px -40px rgba(0, 0, 0, 0.9), 0 0 0 6px rgba(212, 175, 55, 0.07); }
.p8-phone img { display: block; width: 100%; height: auto; border-radius: 34px; }
@media (max-width: 1023px) { .p8-qr { display: none; } }
@media (prefers-reduced-motion: no-preference) {
  .reveal-ready .p8-app .p8-phone { opacity: 0; transform: translateY(80px); transition: opacity 1s var(--ease) 0.25s, transform 1.4s var(--ease) 0.25s; }
  .reveal-ready .p8-app.is-in .p8-phone { opacity: 1; transform: none; }
}
.p8-risk { margin-top: clamp(72px, 8vw, 112px); padding-top: 28px; border-top: 1px solid var(--line); color: #8d897f; font-size: 13px; line-height: 1.6; }
</style>"""

MAIN = r"""<main id="main-content">

  <!-- COPY: every string is home-premium2's or home-premium3's own, cut down, never
       rewritten. Rates, issuers, stats, the review and the risk line come from
       index.html's dated snapshot through those pages. -->

  <!-- ============================================================ the deal -->
  <section class="p8-hero" aria-labelledby="p8-title">
    <img class="p8-hero__pi" src="@IMG@pi.svg" alt="" width="331" height="298">
    <div class="p8-shell">
      <p class="p8-cred p8-rise" style="--d:0"><i class="ph-fill ph-seal-check" aria-hidden="true"></i>SEBI registered Debt Broker. OBPP license holder.</p>
      <h1 class="p8-h1" id="p8-title"><span class="p8-rise" style="--d:1">The <em>golden</em> experience</span><span class="p8-rise" style="--d:2">of investing.</span></h1>
      <div class="p8-ctas p8-rise" style="--d:3">
        <a class="p8-btn p8-btn--gold" href="signup.html">Start investing <i class="ph-bold ph-arrow-right" aria-hidden="true"></i></a>
        <a class="p8-btn p8-btn--line" href="corporate-bonds.html">Explore bonds</a>
      </div>
    </div>
    <!-- DATA: top 3 Bond Utsav deals, index.html snapshot 2026-09-25. -->
    <nav class="p8-shell p8-deals" aria-label="Top bonds">@DEALS@
    </nav>
  </section>

  <!-- ========================================================= the account -->
  <section class="p8-sec" aria-labelledby="p8-assets">
    <div class="p8-shell">
      <h2 data-reveal class="p8-h2" id="p8-assets">Three instruments. One golden account.</h2>
      <div data-reveal class="p8-idx">@INDEX@
      </div>
    </div>
  </section>

  <!-- ============================================================ the case -->
  <section class="p8-sec" style="padding-top: 0" aria-labelledby="p8-whybonds">
    <div class="p8-shell">
      <!-- DATA: savings and bank FD rows are indicative market rates, not GoldenPi
           listings; the two gold rows are the snapshot highs from index.html. Each
           rupee figure is that rate on Rs 1,00,000 for one year. -->
      <div data-reveal class="p8-sheet">
        <div>
          <h2 class="p8-h2" id="p8-whybonds">Why bonds belong in your portfolio.</h2>
          <p class="p8-sheet__cap"><b>What &#8377;1 lakh can earn in a year</b>Indicative annual rates, before tax</p>
        </div>
        <ol class="p8-coins" role="list">@COINS@
        </ol>
      </div>
    </div>
  </section>

  <!-- =========================================================== the trust -->
  <section class="p8-sec" style="padding-top: 0" aria-labelledby="p8-why">
    <div class="p8-shell">
      <h2 data-reveal class="p8-h2" id="p8-why">Why investors choose <em>GoldenPi</em>.</h2>
      <div data-reveal class="p8-five">
        <p class="p8-five__num" aria-hidden="true">5%</p>
        <p class="p8-five__line">Only 5% of bonds make the cut.</p>
      </div>
      <ul data-reveal class="p8-reasons" role="list">@REASONS@</ul>
    </div>
  </section>

  <!-- =========================================================== the proof -->
  <section class="p8-sec p8-proof" aria-labelledby="p8-proof">
    <div class="p8-shell">
      <h2 class="sr-only" id="p8-proof">Happy users</h2>
      <!-- DATA: platform milestones, same figures as index.html. -->
      <dl data-reveal class="p8-stats">
        <div><dt><span data-count>18</span><small>Lac+</small></dt><dd>registered users &amp; growing</dd></div>
        <div><dt>&#8377;<span data-count>6300</span><small>Cr+</small></dt><dd>total transaction through our platform</dd></div>
        <div><dt>&#8377;<span data-count>3000</span><small>Cr+</small></dt><dd>worth of bonds available on the platform everyday</dd></div>
      </dl>
      <!-- DATA: one review from index.html's set, its first sentence. -->
      <figure data-reveal class="p8-quote">
        <div class="p8-quote__stars" aria-label="5 out of 5">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <blockquote>&ldquo;GoldenPi made bond investing simple and transparent.&rdquo;</blockquote>
        <figcaption>Ankit Sharma</figcaption>
      </figure>
    </div>
  </section>

  <!-- ========================================================== the pocket -->
  <section class="p8-sec" aria-labelledby="p8-get">
    <div data-reveal class="p8-shell p8-app">
      <div>
        <img class="p8-app__icon" src="@IMG@play/app-icon.png" alt="GoldenPi app icon" width="64" height="64">
        <h2 class="p8-h2" id="p8-get">Your <em>Golden Experience</em> is one tap away.</h2>
        <a class="p8-play" href="https://play.google.com/store/apps/details?id=com.goldenpi.gpimobileapp"><i class="ph-fill ph-google-play-logo" aria-hidden="true"></i><span>Get it on<b>Google Play</b></span></a>
      </div>
      <div class="p8-qr">
        <img src="@IMG@mobile-app-qr.svg" alt="QR code to download the GoldenPi app" width="248" height="306">
        <p>Scan to download GoldenPi app and get voucher</p>
      </div>
      <!-- The app's own explore screen, captured at 390px (home-premium5's asset). -->
      <div class="p8-phone"><img src="@IMG@premium5/app-explore.jpg" alt="The GoldenPi app's explore screen" width="780" height="1688" loading="lazy"></div>
    </div>
    <div class="p8-shell">
      <p class="p8-risk">Risk Disclosure: Fixed returns do not constitute guaranteed or assured returns. Investments in corporate debt, municipal debt, and securitized instruments are subject to credit, market, and default risks, including delays or defaults in payments. Read all offer documents carefully.</p>
    </div>
  </section>

</main>"""


def main():
    page = open(SRC, encoding="utf-8").read()
    page, n1 = re.subn(r"<style>\n/\* home-premium: page-only styles.*?</style>", lambda m: STYLE, page, count=1, flags=re.S)
    page, n2 = re.subn(r'<body class="h3-page">', '<body class="p8-page p8">', page, count=1)
    main_html = (MAIN.replace("@DEALS@", "".join(deal(i, d) for i, d in enumerate(DEALS)))
                 .replace("@INDEX@", "".join(instrument(i, x) for i, x in enumerate(INSTRUMENTS)))
                 .replace("@COINS@", "".join(coin(i, e) for i, e in enumerate(EARN)))
                 .replace("@REASONS@", "".join(reason(i, r) for i, r in enumerate(REASONS)))
                 .replace("@IMG@", IMG))
    page, n3 = re.subn(r'<main id="main-content">.*?</main>', lambda m: main_html, page, count=1, flags=re.S)
    page, n4 = re.subn(r"<title>.*?</title>", "<title>GoldenPi | The Golden Experience of Investing</title>", page, count=1)
    if (n1, n2, n3, n4) != (1, 1, 1, 1) or "@" in re.sub(r"@(media|keyframes|import|font-face|supports)", "", main_html):
        raise SystemExit("home-premium3.html changed shape (%d %d %d %d), or a placeholder was left" % (n1, n2, n3, n4))
    if re.search("[–—]", main_html + STYLE):
        raise SystemExit("an en or em dash slipped into the page")
    open(OUT, "w", encoding="utf-8").write(page)
    print("home-premium8.html")


if __name__ == "__main__":
    main()
