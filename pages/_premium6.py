#!/usr/bin/env python3
"""Write home-premium6.html: the homepage in black, white and gold, from
home-premium2's and home-premium3's content, built around one idea, the bond
certificate. Black is the market, white is the paper you own, gold is what it
pays. White never fills a whole section; it is the paper the facts are printed on.

  the deal      top 3 Bond Utsav deals as paper tickets laid on the black, all
                three readable at once (not a card carousel)
  the account   three instruments, one golden account, as one low ruled row
  the case      why bonds: what Rs 1 lakh earns, as stacks of coins on paper
  the trust     why investors choose GoldenPi, premium3's bento
  the proof     platform numbers, then one review at a time, picked by name
  the pocket    the app: a large QR, Google Play and the real app screen

Reviewed against taste-skill (2026-10-11): dark page with no theme flip, one
gold accent, radius 20px surfaces and pill controls, no eyebrows, no section
numbers, no em-dashes, no comparison tracks, no div-built screens, no scroll
listeners, every motion behind prefers-reduced-motion.

IMAGES: the generated hero, case and proof images were not made (Figma AI
usage limit). Each slot is a CSS custom property on .p6 (--p6-img-hero,
--p6-img-proof); set it to url(...) once the images exist. The page reads
complete without them.

Chrome (head links, navbar, footer and its styles, the shared count-up and
reveal scripts) is home-premium3's; only its page styles, <body> class and
<main> are replaced. Copy is the two pages' own; nothing new is written here.

    python3 pages/_premium6.py && python3 pages/_build.py
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "home-premium3.html")
OUT = os.path.join(HERE, "home-premium6.html")
IMG = "../assets/img/"

# DATA: top 3 Bond Utsav deals, index.html snapshot 2026-09-25, as home-premium2 shows them.
DEALS = [
    ("Akara", "GPID102720.AKARA-CAPITAL-ADVISORS-PRIVATE-LIMITED-2x.png", "13.00",
     [("Rating", "ACUITE BBB+"), ("Payout", "Monthly"), ("Maturity", "3-Dec-2027")],
     "https://uatnew.goldenpi.com/bonds/GPID107435/akara-1300-bond-yield?src=view_details&amp;tenureDate=03-Dec-2027"),
    ("NeoGrowth", "GPID104095.Neogrowth-new-logo-1-.jpg", "13.00",
     [("Rating", "ICRA BBB"), ("Payout", "Half Yearly"), ("Maturity", "30-Apr-2028")],
     "https://uatnew.goldenpi.com/bonds/GPID107371/neogrowth-1300-bond-yield?src=view_details&amp;tenureDate=30-Apr-2028"),
    ("Best Capital", "GPID107347.Best-Capital.png", "13.00",
     [("Rating", "IVR BBB"), ("Payout", "Monthly"), ("Maturity", "11-Sep-2029")],
     "https://uatnew.goldenpi.com/bonds/GPID107433/best-capital-1300-bond-yield?src=view_details&amp;tenureDate=11-Sep-2029"),
]

# DATA: reviews, same set as index.html.
REVIEWS = [
    ("Ankit Sharma", "GoldenPi made bond investing simple and transparent. I could compare yields and complete everything online."),
    ("Priya Nair", "Clear listings and support when I needed help with KYC. Fixed income finally feels accessible."),
    ("Rahul Mehta", "I started with NCD IPOs and now use GoldenPi for secondary bonds too. Smooth experience overall."),
    ("Sneha Kapoor", "The collections helped me shortlist bonds that match my goals without wading through noise."),
    ("Vikram Joshi", "Reliable platform with SEBI registration. That trust factor mattered before I invested."),
]

# (label, rate, GoldenPi's own): home-premium2's ladder. The rupee figure is
# the rate applied to the figure's own Rs 1 lakh, simple interest for a year.
EARN = [("Savings account", 2.7, False), ("Large bank FD", 6.5, False),
        ("FDs on GoldenPi", 8.5, True), ("Bonds on GoldenPi", 13.8, True)]

ARROW = '<i class="ph-bold ph-arrow-right" aria-hidden="true"></i>'


def ticket(i, d):
    name, logo, rate, facts, url = d
    dl = "".join('<div><dt>%s</dt><dd>%s</dd></div>' % f for f in facts)
    return f"""
        <li class="p6-tk" style="--i:{i}">
          <article class="p6-tk__paper">
            <div class="p6-tk__main">
              <div class="p6-tk__who"><img src="{IMG}{logo}" alt="" width="44" height="44"><p><b>{name}</b><span>Bond Utsav deal</span></p></div>
              <dl>{dl}</dl>
            </div>
            <div class="p6-tk__stub">
              <p class="p6-tk__rate">{rate}<small>%</small></p>
              <p class="p6-tk__lbl">Returns</p>
              <a class="p6-tk__go" href="{url}" aria-label="Know more about {name}">Know more {ARROW}</a>
            </div>
          </article>
        </li>"""


def earn_col(i, e):
    label, rate, own = e
    rupees = "{:,}".format(round(rate * 1000))
    return f"""
            <li class="p6-coin{' p6-coin--gold' if own else ''}" style="--h:{rate / 13.8 * 100:.1f}%; --i:{i}">
              <span class="p6-coin__amt">&#8377;<span data-count>{rupees}</span></span>
              <span class="p6-coin__stack" aria-hidden="true"></span>
              <span class="p6-coin__rate">{rate}%</span>
              <span class="p6-coin__lbl">{label}</span>
            </li>"""


def review_tab(i, r):
    name = r[0]
    on = i == 0
    return (f'<button type="button" role="tab" class="p6-who" id="p6-t{i}" aria-controls="p6-q{i}" '
            f'aria-selected="{str(on).lower()}" tabindex="{0 if on else -1}">'
            f'<span class="p6-who__mono" aria-hidden="true">{name[0]}</span><b>{name}</b></button>')


def review(i, r):
    name, text = r
    return f"""
          <figure class="p6-q{' is-on' if i == 0 else ''}" id="p6-q{i}" role="tabpanel" aria-labelledby="p6-t{i}" tabindex="0">
            <div class="p6-stars" aria-label="5 out of 5">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
            <blockquote>&ldquo;{text}&rdquo;</blockquote>
            <figcaption>{name}</figcaption>
          </figure>"""


STYLE = r"""<style>
/* home-premium6: page-only styles, p6- prefix. Written by pages/_premium6.py.
   Tokens: black is the market, paper is what you own, gold is what it pays.
   Shape lock: surfaces 20px, paper tickets 18px, controls are pills. */
.p6 {
  --k: #0c0b09; --k2: #14130f; --k3: #1d1b16;
  --paper: #f6f5f1; --paper-2: #ebe9e2; --ink: #15130e; --ink-2: #5b574d;
  --gold: #d4af37; --gold-hi: #ecd27f; --gold-lo: #9c7b22;
  --tx: #f4f2ed; --tx-2: #aaa69c; --line: rgba(244, 242, 237, 0.1);
  --ease: cubic-bezier(0.16, 1, 0.3, 1);
  --p6-img-hero: none; --p6-img-proof: none;
  background: var(--k);
}
body.p6-page { background: #0c0b09; }
.p6 main { color: var(--tx); font-family: "Satoshi", system-ui, sans-serif; }
.p6 main ::selection { background: var(--gold); color: var(--ink); }
/* Film grain, fixed and inert so it never repaints with the scroll. */
.p6-page::after {
  content: ""; position: fixed; inset: 0; z-index: 60; pointer-events: none; opacity: 0.05;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}
.p6-shell { width: min(1240px, 100% - 32px); margin-inline: auto; }
@media (min-width: 768px) { .p6-shell { width: min(1240px, 100% - 64px); } }
.p6-sec { padding-block: clamp(72px, 9vw, 128px); }

.p6-h1, .p6-h2 { color: var(--tx); font-weight: 700; letter-spacing: -0.035em; text-wrap: balance; }
.p6-h1 { font-size: clamp(40px, 4.5vw, 66px); line-height: 1.02; }
.p6-h2 { font-size: clamp(32px, 3.7vw, 54px); line-height: 1.06; max-width: 18ch; }
.p6-h1 em, .p6-h2 em { font-style: normal; color: var(--gold); }
.p6-lead { margin-top: 18px; max-width: 54ch; color: var(--tx-2); font-size: clamp(16px, 1.25vw, 18px); line-height: 1.6; }

.p6-btn {
  display: inline-flex; align-items: center; gap: 10px; min-height: 52px; padding: 0 26px;
  border-radius: 999px; font-weight: 700; font-size: 16px; white-space: nowrap;
  transition: transform 0.35s var(--ease), background-color 0.35s var(--ease), border-color 0.35s var(--ease);
}
.p6-btn i { transition: transform 0.35s var(--ease); }
.p6-btn:hover i { transform: translateX(4px); }
.p6-btn:active { transform: scale(0.98); }
.p6-btn--gold { background: var(--gold); color: var(--ink); }
.p6-btn--gold:hover { background: var(--gold-hi); }
.p6-btn--line { border: 1px solid rgba(244, 242, 237, 0.28); color: var(--tx); }
.p6-btn--line:hover { border-color: var(--gold); }
.p6 a:focus-visible, .p6 button:focus-visible, .p6 [tabindex]:focus-visible { outline: 2px solid var(--gold); outline-offset: 3px; }

/* ------------------------------------------------------------ the deal */
.p6-hero {
  position: relative; overflow: hidden; isolation: isolate;
  padding-block: clamp(40px, 6vw, 88px) clamp(64px, 7vw, 104px);
  background:
    radial-gradient(52% 64% at 80% 44%, rgba(212, 175, 55, 0.2), transparent 70%),
    radial-gradient(30% 40% at 100% 0%, rgba(236, 210, 127, 0.12), transparent 70%),
    var(--p6-img-hero) center / cover no-repeat, var(--k);
}
.p6-hero::after { /* the table edge: a hairline of gold light under the deals */
  content: ""; position: absolute; left: 0; right: 0; bottom: 0; height: 1px; z-index: -1;
  background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.5) 60%, transparent);
}
.p6-hero__grid { display: grid; gap: 56px; align-items: center; }
@media (min-width: 1024px) {
  .p6-hero__grid { grid-template-columns: minmax(0, 1fr) minmax(0, 530px); gap: 64px; min-height: min(640px, calc(100dvh - 200px)); }
}
.p6-trust { display: flex; flex-wrap: wrap; gap: 10px 22px; margin-top: 26px; color: var(--tx-2); font-size: 15px; }
.p6-trust li { display: inline-flex; align-items: center; gap: 8px; }
.p6-trust i { color: var(--gold); font-size: 18px; }
.p6-ctas { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 36px; }

/* The deck: three tickets laid on the table, slightly askew, all readable. */
.p6-deck { display: grid; gap: 0; width: 100%; max-width: 530px; justify-self: center; }
.p6-tk {
  --r: -2.2deg; --x: 0px;
  position: relative; z-index: calc(3 - var(--i));
  filter: drop-shadow(0 24px 34px rgba(0, 0, 0, 0.55)) drop-shadow(0 2px 2px rgba(0, 0, 0, 0.3));
  transform: translateX(var(--x)) rotate(var(--r));
  transition: transform 0.6s var(--ease);
}
.p6-tk + .p6-tk { margin-top: -14px; }
.p6-tk:nth-child(2) { --r: 1.6deg; --x: 26px; }
.p6-tk:nth-child(3) { --r: -0.8deg; --x: 8px; }
.p6-tk:hover, .p6-tk:focus-within { z-index: 4; transform: translateX(var(--x)) translateY(-8px) rotate(0deg); }
.p6-tk__paper {
  --stub: 168px;
  display: grid; grid-template-columns: minmax(0, 1fr) var(--stub);
  border-radius: 18px; color: var(--ink);
  background:
    repeating-radial-gradient(circle at 100% 0, rgba(156, 123, 34, 0.07) 0 1px, transparent 1px 7px),
    linear-gradient(135deg, #fbfaf7, var(--paper-2));
  /* Two punched notches where the stub tears off. */
  -webkit-mask:
    radial-gradient(circle 11px at calc(100% - var(--stub)) 0, #0000 98%, #000) top / 100% 51% no-repeat,
    radial-gradient(circle 11px at calc(100% - var(--stub)) 100%, #0000 98%, #000) bottom / 100% 51% no-repeat;
          mask:
    radial-gradient(circle 11px at calc(100% - var(--stub)) 0, #0000 98%, #000) top / 100% 51% no-repeat,
    radial-gradient(circle 11px at calc(100% - var(--stub)) 100%, #0000 98%, #000) bottom / 100% 51% no-repeat;
}
.p6-tk__main { padding: 22px 22px 20px 24px; }
.p6-tk__who { display: flex; align-items: center; gap: 12px; }
.p6-tk__who img { width: 58px; height: 44px; padding: 4px; border-radius: 12px; object-fit: contain; background: #fff; border: 1px solid rgba(21, 19, 14, 0.08); }
.p6-tk__who b { display: block; font-size: 18px; letter-spacing: -0.01em; }
.p6-tk__who span { display: block; color: var(--gold-lo); font-size: 12px; font-weight: 700; letter-spacing: 0.02em; }
.p6-tk dl { display: grid; grid-template-columns: repeat(3, auto); justify-content: space-between; gap: 6px 16px; margin-top: 18px; padding-top: 14px; border-top: 1px solid rgba(21, 19, 14, 0.1); }
.p6-tk dt { color: var(--ink-2); font-size: 12px; }
.p6-tk dd { margin-top: 2px; font-size: 14px; font-weight: 700; white-space: nowrap; }
.p6-tk__stub {
  display: flex; flex-direction: column; justify-content: center; padding: 18px 20px;
  border-left: 2px dashed rgba(21, 19, 14, 0.18); border-radius: 0 18px 18px 0;
  background: linear-gradient(160deg, #1b1914, #0f0e0b); color: var(--tx);
}
.p6-tk__rate { color: var(--gold); font-size: 38px; font-weight: 700; letter-spacing: -0.03em; line-height: 1; font-variant-numeric: tabular-nums; }
.p6-tk__rate small { font-size: 0.55em; margin-left: 1px; }
.p6-tk__lbl { margin-top: 4px; color: var(--tx-2); font-size: 13px; }
.p6-tk__go { display: inline-flex; align-items: center; gap: 6px; white-space: nowrap; margin-top: 14px; color: var(--tx); font-size: 14px; font-weight: 700; }
.p6-tk__go::after { content: ""; position: absolute; inset: 0; } /* the whole ticket is the link target */
.p6-tk__go i { color: var(--gold); transition: transform 0.35s var(--ease); }
.p6-tk:hover .p6-tk__go i { transform: translateX(4px); }

@media (max-width: 767px) {
  .p6-tk:nth-child(n) { --r: 0deg; --x: 0px; }
  .p6-tk:nth-child(2) { --r: 1deg; }
  .p6-tk + .p6-tk { margin-top: 12px; }
  .p6-tk__paper { --stub: 126px; }
  .p6-tk__go { font-size: 13px; gap: 4px; }
  .p6-tk__main { padding: 18px 14px 16px 16px; }
  .p6-tk dl { grid-template-columns: 1fr 1fr; justify-content: stretch; }
  .p6-tk__stub { padding: 14px; }
  .p6-tk__rate { font-size: 30px; }
}

/* Hero entrance: copy rises, then the deals are laid down one by one. */
@media (prefers-reduced-motion: no-preference) {
  .p6-rise { animation: p6-rise 0.9s var(--ease) both; animation-delay: calc(var(--d, 0) * 110ms); }
  .p6-tk { animation: p6-deal 1s var(--ease) backwards; animation-delay: calc(450ms + var(--i) * 160ms); }
}
@keyframes p6-rise { from { opacity: 0; transform: translateY(22px); } }
@keyframes p6-deal { from { opacity: 0; transform: translateX(var(--x)) translateY(60px) rotate(calc(var(--r) * -3)); } }

/* --------------------------------------------------------- the account */
.p6-acct { padding-block: clamp(64px, 7vw, 96px); }
.p6-inst { display: grid; margin-top: 40px; border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); }
@media (min-width: 900px) { .p6-inst { grid-template-columns: 1.35fr 1fr 1fr; } }
.p6-inst__item {
  position: relative; display: flex; flex-direction: column; gap: 10px; padding: 28px 28px 26px;
  transition: background-color 0.4s var(--ease);
}
.p6-inst__item + .p6-inst__item { border-top: 1px solid var(--line); }
@media (min-width: 900px) {
  .p6-inst__item + .p6-inst__item { border-top: 0; border-left: 1px solid var(--line); }
  .p6-inst__item:first-child { padding-left: 0; }
}
.p6-inst__item::after { /* gold rule grows along the top edge on hover */
  content: ""; position: absolute; left: 0; right: 0; top: -1px; height: 2px; background: var(--gold);
  transform: scaleX(0); transform-origin: left; transition: transform 0.5s var(--ease);
}
.p6-inst__item:hover::after, .p6-inst__item:focus-visible::after { transform: scaleX(1); }
.p6-inst__item:hover { background: rgba(212, 175, 55, 0.04); }
.p6-inst__head { display: flex; align-items: center; gap: 12px; }
.p6-inst__head i { color: var(--gold); font-size: 26px; }
.p6-inst__head h3 { font-size: 22px; font-weight: 700; letter-spacing: -0.02em; }
.p6-live { margin-left: auto; padding: 4px 10px; border: 1px solid rgba(212, 175, 55, 0.45); border-radius: 999px; color: var(--gold-hi); font-size: 12px; font-weight: 700; }
.p6-inst__item > p { color: var(--tx-2); font-size: 15px; line-height: 1.55; max-width: 46ch; }
.p6-inst__facts { display: flex; flex-wrap: wrap; gap: 8px 28px; margin-top: 4px; }
.p6-inst__facts dt { color: var(--tx); font-size: 22px; font-weight: 700; letter-spacing: -0.02em; font-variant-numeric: tabular-nums; }
.p6-inst__facts div:first-child dt { color: var(--gold); }
.p6-inst__facts dd { color: var(--tx-2); font-size: 13px; }
.p6-more { display: inline-flex; align-items: center; gap: 6px; margin-top: auto; padding-top: 6px; color: var(--tx); font-size: 15px; font-weight: 700; }
.p6-more i { color: var(--gold); transition: transform 0.35s var(--ease); }
.p6-inst__item:hover .p6-more i { transform: translateX(4px); }

/* ------------------------------------------------------------ the case */
.p6-case { display: grid; gap: 48px; align-items: center; }
@media (min-width: 1024px) { .p6-case { grid-template-columns: minmax(0, 1.05fr) minmax(0, 1fr); gap: 72px; } }
.p6-ledger {
  padding: clamp(24px, 3vw, 40px); border-radius: 20px; color: var(--ink);
  background:
    radial-gradient(80% 60% at 100% 0%, rgba(212, 175, 55, 0.14), transparent 60%),
    linear-gradient(160deg, #fbfaf7, var(--paper-2));
  box-shadow: 0 40px 80px -30px rgba(0, 0, 0, 0.7);
}
.p6-ledger h3 { font-size: clamp(20px, 1.8vw, 24px); font-weight: 700; letter-spacing: -0.02em; }
.p6-ledger small { display: block; margin-top: 4px; color: var(--ink-2); font-size: 13px; }
.p6-coins { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: clamp(10px, 2vw, 22px); align-items: end; height: clamp(280px, 30vw, 340px); margin-top: 28px; }
.p6-coin { display: grid; grid-template-rows: auto 1fr auto auto; height: 100%; text-align: center; }
.p6-coin__amt { align-self: end; margin-bottom: 8px; color: var(--ink-2); font-size: clamp(13px, 1.3vw, 16px); font-weight: 700; font-variant-numeric: tabular-nums; }
.p6-coin--gold .p6-coin__amt { color: var(--ink); }
.p6-coin__stack {
  display: block; align-self: end; height: var(--h); border-radius: 10px 10px 4px 4px;
  /* Stacked coins: a rim line every 9px. */
  background: repeating-linear-gradient(to top, #cfccc3 0 8px, #b9b5aa 8px 9px);
  transform-origin: bottom;
}
.p6-coin--gold .p6-coin__stack {
  background:
    linear-gradient(90deg, rgba(255, 255, 255, 0.28), transparent 40%, rgba(0, 0, 0, 0.12)),
    repeating-linear-gradient(to top, var(--gold) 0 8px, var(--gold-lo) 8px 9px);
}
.p6-coin__rate { margin-top: 12px; font-size: clamp(18px, 2vw, 24px); font-weight: 700; letter-spacing: -0.02em; }
.p6-coin--gold .p6-coin__rate { color: var(--gold-lo); }
.p6-coin__lbl { margin-top: 2px; color: var(--ink-2); font-size: 12px; line-height: 1.35; }
@media (prefers-reduced-motion: no-preference) {
  .reveal-ready .p6-ledger .p6-coin__stack { transform: scaleY(0.02); transition: transform 1.3s var(--ease); transition-delay: calc(200ms + var(--i) * 140ms); }
  .reveal-ready .p6-ledger.is-in .p6-coin__stack { transform: none; }
}
.p6-points { display: grid; gap: 26px 32px; margin-top: 36px; }
@media (min-width: 640px) { .p6-points { grid-template-columns: 1fr 1fr; } }
.p6-points li { display: grid; grid-template-columns: 40px 1fr; gap: 2px 14px; }
.p6-points i { grid-row: span 2; display: grid; place-items: center; width: 40px; height: 40px; border-radius: 999px; border: 1px solid rgba(212, 175, 55, 0.4); color: var(--gold); font-size: 20px; }
.p6-points b { font-size: 17px; }
.p6-points span { color: var(--tx-2); font-size: 15px; line-height: 1.5; }

/* ----------------------------------------------------------- the trust */
.p6-bento { display: grid; gap: 16px; margin-top: 44px; }
@media (min-width: 900px) {
  .p6-bento { grid-template-columns: 1.15fr 1fr 1fr; grid-template-rows: auto auto; }
  .p6-cell--big { grid-row: span 2; }
  .p6-cell--wide { grid-column: span 2; }
}
.p6-cell {
  position: relative; overflow: hidden; display: flex; flex-direction: column; gap: 10px;
  padding: clamp(24px, 2.6vw, 34px); border-radius: 20px;
  background: var(--k2); border: 1px solid var(--line);
  transition: border-color 0.5s var(--ease), transform 0.5s var(--ease);
}
.p6-cell:hover { border-color: rgba(212, 175, 55, 0.4); transform: translateY(-3px); }
.p6-cell > i { color: var(--gold); font-size: 30px; margin-bottom: 18px; }
.p6-cell h3 { color: var(--tx); font-size: 22px; font-weight: 700; letter-spacing: -0.02em; }
.p6-cell p { color: var(--tx-2); font-size: 15px; line-height: 1.55; max-width: 44ch; }
.p6-cell--big {
  justify-content: flex-end; min-height: 380px; color: var(--ink);
  background:
    repeating-radial-gradient(circle at 0 0, rgba(156, 123, 34, 0.07) 0 1px, transparent 1px 8px),
    linear-gradient(160deg, #fbfaf7, var(--paper-2));
  border-color: transparent;
}
.p6-cell--big h3 { color: var(--ink); font-size: clamp(24px, 2.2vw, 30px); }
.p6-cell--big p { color: var(--ink-2); }
.p6-cell .p6-big { margin-bottom: auto; max-width: none; color: var(--gold-lo); font-size: clamp(110px, 13vw, 190px); font-weight: 900; letter-spacing: -0.06em; line-height: 0.9; }
.p6-cell--wide {
  background:
    radial-gradient(70% 140% at 100% 50%, rgba(212, 175, 55, 0.22), transparent 60%),
    var(--k2);
}
.p6-cell--wide .p6-globe { position: absolute; right: -24px; bottom: -48px; font-size: 220px; color: rgba(212, 175, 55, 0.14); pointer-events: none; }
.p6-cell--wide > *:not(.p6-globe) { position: relative; max-width: 52ch; }
@media (prefers-reduced-motion: no-preference) {
  .reveal-ready .p6-bento[data-reveal] { opacity: 1; transform: none; }
  .reveal-ready .p6-bento .p6-cell { opacity: 0; transform: translateY(24px); transition: opacity 0.7s var(--ease), transform 0.8s var(--ease), border-color 0.5s var(--ease); transition-delay: calc(var(--i) * 110ms); }
  .reveal-ready .p6-bento.is-in .p6-cell { opacity: 1; transform: none; }
  .reveal-ready .p6-bento.is-in .p6-cell:hover { transform: translateY(-3px); transition-delay: 0s; }
}

/* ----------------------------------------------------------- the proof */
.p6-proof {
  position: relative; isolation: isolate; overflow: hidden;
  background:
    radial-gradient(50% 80% at 85% 0%, rgba(212, 175, 55, 0.16), transparent 70%),
    var(--p6-img-proof) center / cover no-repeat, var(--k2);
  border-block: 1px solid var(--line);
}
.p6-stats { display: grid; gap: 28px; margin-top: 44px; }
@media (min-width: 900px) { .p6-stats { grid-template-columns: repeat(3, 1fr); gap: 0; } .p6-stats > div + div { padding-left: 40px; border-left: 1px solid var(--line); } }
.p6-stats dt { color: var(--gold); font-size: clamp(48px, 5.4vw, 80px); font-weight: 700; letter-spacing: -0.045em; line-height: 1; font-variant-numeric: tabular-nums; white-space: nowrap; }
.p6-stats dt small { margin-left: 4px; color: var(--tx); font-size: 0.36em; font-weight: 700; letter-spacing: 0; }
.p6-stats dd { margin-top: 10px; color: var(--tx-2); font-size: 15px; max-width: 26ch; }

.p6-voices { display: grid; gap: 32px; margin-top: clamp(56px, 6vw, 88px); padding-top: clamp(40px, 5vw, 64px); border-top: 1px solid var(--line); }
@media (min-width: 900px) { .p6-voices { grid-template-columns: 280px minmax(0, 1fr); gap: 64px; align-items: center; } }
.p6-whos { display: none; }
.p6-js .p6-whos { display: flex; gap: 8px; overflow-x: auto; scrollbar-width: none; }
@media (min-width: 900px) { .p6-js .p6-whos { flex-direction: column; } }
.p6-who {
  display: inline-flex; flex: none; align-items: center; gap: 12px; padding: 8px 18px 8px 8px; border-radius: 999px;
  border: 1px solid transparent; color: var(--tx-2); font-size: 15px; text-align: left;
  transition: color 0.3s var(--ease), border-color 0.3s var(--ease), background-color 0.3s var(--ease);
}
.p6-who:hover { color: var(--tx); }
.p6-who[aria-selected="true"] { color: var(--tx); border-color: rgba(212, 175, 55, 0.4); background: rgba(212, 175, 55, 0.07); }
.p6-who__mono { display: grid; place-items: center; width: 36px; height: 36px; border-radius: 999px; border: 1px solid rgba(212, 175, 55, 0.5); color: var(--gold); font-weight: 700; }
.p6-who[aria-selected="true"] .p6-who__mono { background: var(--gold); color: var(--ink); border-color: var(--gold); }
.p6-qs { display: grid; gap: 40px; }
.p6-js .p6-qs { gap: 0; }
.p6-js .p6-q { grid-area: 1 / 1; }
.p6-js .p6-q:not(.is-on) { visibility: hidden; opacity: 0; }
.p6-q { transition: opacity 0.6s var(--ease), transform 0.6s var(--ease); }
@media (prefers-reduced-motion: no-preference) { .p6-js .p6-q:not(.is-on) { transform: translateY(12px); } }
.p6-stars { color: var(--gold); font-size: 18px; letter-spacing: 4px; }
.p6-q blockquote { margin-top: 16px; color: var(--tx); font-size: clamp(22px, 2.4vw, 34px); font-weight: 500; line-height: 1.3; letter-spacing: -0.02em; max-width: 34ch; text-wrap: pretty; }
.p6-q figcaption { margin-top: 20px; color: var(--tx-2); font-size: 15px; }

/* ---------------------------------------------------------- the pocket */
.p6-app {
  position: relative; overflow: hidden; display: grid; gap: 40px; align-items: center;
  padding: clamp(28px, 4.5vw, 64px); border-radius: 20px; border: 1px solid var(--line);
  background:
    radial-gradient(60% 90% at 90% 100%, rgba(212, 175, 55, 0.22), transparent 70%),
    linear-gradient(160deg, var(--k3), var(--k2));
}
@media (min-width: 1024px) { .p6-app { grid-template-columns: minmax(0, 1.2fr) minmax(0, 0.8fr); } }
.p6-app__icon { width: 72px; height: 72px; border-radius: 18px; margin-bottom: 28px; box-shadow: 0 16px 40px -12px rgba(212, 175, 55, 0.45); }
.p6-get { display: flex; flex-wrap: wrap; align-items: center; gap: 28px; margin-top: 36px; }
.p6-qr { display: block; width: 200px; height: auto; }
.p6-get__side { display: grid; gap: 14px; }
.p6-get__side p { color: var(--tx-2); font-size: 15px; max-width: 24ch; line-height: 1.5; }
.p6-get__side p b { display: block; color: var(--tx); font-size: 17px; }
.p6-play { display: inline-flex; align-items: center; gap: 12px; width: max-content; min-height: 56px; padding: 0 22px; border-radius: 999px; background: var(--tx); color: var(--ink); transition: transform 0.35s var(--ease), background-color 0.35s var(--ease); }
.p6-play:hover { background: #fff; }
.p6-play:active { transform: scale(0.98); }
.p6-play i { font-size: 24px; }
.p6-play span { font-size: 11px; line-height: 1.15; }
.p6-play b { display: block; font-size: 17px; }
.p6-phone { justify-self: center; width: min(280px, 72vw); padding: 10px; border-radius: 44px; background: #050504; border: 1px solid rgba(244, 242, 237, 0.14); box-shadow: 0 50px 90px -30px rgba(0, 0, 0, 0.8), 0 0 0 6px rgba(212, 175, 55, 0.08); transform: rotate(3deg); }
.p6-phone img { display: block; width: 100%; height: auto; border-radius: 34px; }
@media (max-width: 767px) { .p6-qr { width: 168px; } .p6-phone { transform: none; } }
@media (prefers-reduced-motion: no-preference) {
  .reveal-ready .p6-app .p6-phone { transform: translateY(60px) rotate(8deg); opacity: 0; transition: transform 1.2s var(--ease) 0.2s, opacity 0.8s var(--ease) 0.2s; }
  .reveal-ready .p6-app.is-in .p6-phone { transform: rotate(3deg); opacity: 1; }
}
.p6-risk { margin-top: 28px; color: #8f8b81; font-size: 13px; line-height: 1.6; max-width: 110ch; }
</style>"""

MAIN = r"""<main id="main-content">

  <!-- COPY: every headline, line and label is home-premium2's or home-premium3's
       own; nothing on this page is new copy. Rates, issuers, stats, reviews and
       the risk line come from index.html's dated snapshot through those pages. -->

  <!-- ============================================================ the deal -->
  <section class="p6-hero" aria-labelledby="p6-title">
    <div class="p6-shell p6-hero__grid">
      <div>
        <h1 class="p6-h1 p6-rise" style="--d:1" id="p6-title">The <em>golden</em> experience of investing.</h1>
        <ul class="p6-trust p6-rise" style="--d:2" role="list">
          <li><i class="ph-fill ph-seal-check" aria-hidden="true"></i>SEBI registered Debt Broker</li>
          <li><i class="ph-fill ph-seal-check" aria-hidden="true"></i>OBPP license holder</li>
          <li><i class="ph-fill ph-seal-check" aria-hidden="true"></i>Fixed returns up to 13.8%</li>
        </ul>
        <div class="p6-ctas p6-rise" style="--d:3">
          <a class="p6-btn p6-btn--gold" href="signup.html">Start investing @ARROW@</a>
          <a class="p6-btn p6-btn--line" href="corporate-bonds.html">Explore bonds</a>
        </div>
      </div>
      <!-- DATA: top 3 Bond Utsav deals, index.html snapshot 2026-09-25. -->
      <ul class="p6-deck" role="list" aria-label="Top bonds">@TICKETS@
      </ul>
    </div>
  </section>

  <!-- ========================================================= the account -->
  <section class="p6-acct" aria-labelledby="p6-assets">
    <div class="p6-shell">
      <h2 data-reveal class="p6-h2" id="p6-assets">Three instruments. One golden account.</h2>
      <p data-reveal class="p6-lead">Everything fixed income, under one login and one KYC. Pick the payout, the tenure and the risk you are comfortable with.</p>
      <div data-reveal class="p6-inst">
        <a class="p6-inst__item" href="corporate-bonds.html">
          <div class="p6-inst__head"><i class="ph ph-certificate" aria-hidden="true"></i><h3>Corporate Bonds</h3></div>
          <p>Lend to established Indian companies and collect fixed interest on a schedule you choose. Every bond is credit rated, every cash flow shown upfront.</p>
          <dl class="p6-inst__facts">
            <div><dt>13.8%</dt><dd>Returns, up to</dd></div>
            <div><dt>Monthly</dt><dd>Payouts available</dd></div>
            <div><dt>A or above</dt><dd>Highly rated picks</dd></div>
          </dl>
          <span class="p6-more">Explore bonds @ARROW@</span>
        </a>
        <a class="p6-inst__item" href="fixed-deposits.html">
          <div class="p6-inst__head"><i class="ph ph-vault" aria-hidden="true"></i><h3>Fixed Deposits</h3></div>
          <p>Book FDs with leading small finance banks and NBFCs, without opening a new bank account.</p>
          <dl class="p6-inst__facts">
            <div><dt>8.5%</dt><dd>Highest returns</dd></div>
            <div><dt>&#8377;5L</dt><dd>Insured upto</dd></div>
          </dl>
          <span class="p6-more">Explore FDs @ARROW@</span>
        </a>
        <a class="p6-inst__item" href="bond-ipo-online.html">
          <div class="p6-inst__head"><i class="ph ph-rocket-launch" aria-hidden="true"></i><h3>NCD IPOs</h3><span class="p6-live">Live now</span></div>
          <p>Apply to new bond issues at face value, straight into your demat, before they list.</p>
          <span class="p6-more">See open IPOs @ARROW@</span>
        </a>
      </div>
    </div>
  </section>

  <!-- ============================================================ the case -->
  <section class="p6-sec" style="padding-top: 0" aria-labelledby="p6-whybonds">
    <div class="p6-shell p6-case">
      <!-- DATA: savings and bank FD rows are indicative market rates, not GoldenPi
           listings; the two gold rows are the snapshot highs from index.html. Each
           rupee figure is that rate on Rs 1,00,000 for one year. -->
      <figure data-reveal class="p6-ledger">
        <h3>What &#8377;1 lakh can earn in a year</h3>
        <small>Indicative annual rates, before tax</small>
        <ol class="p6-coins" role="list">@EARN@
        </ol>
      </figure>
      <div>
        <h2 data-reveal class="p6-h2" id="p6-whybonds">Why bonds belong in your portfolio.</h2>
        <p data-reveal class="p6-lead">Bonds sit between the safety of a deposit and the growth of equity. You know what you will earn, and when, on the day you invest.</p>
        <ul data-reveal class="p6-points" role="list">
          <li><i class="ph ph-calendar-check" aria-hidden="true"></i><b>Predictable income</b><span>Interest lands on fixed dates, monthly to yearly.</span></li>
          <li><i class="ph ph-trend-up" aria-hidden="true"></i><b>Higher than FDs</b><span>Rated corporate debt typically pays a premium over bank deposits.</span></li>
          <li><i class="ph ph-waves" aria-hidden="true"></i><b>Steadier than stocks</b><span>Returns are set at purchase, not by daily market moods.</span></li>
          <li><i class="ph ph-chart-pie-slice" aria-hidden="true"></i><b>Real diversification</b><span>Spread across issuers, ratings and maturities.</span></li>
        </ul>
      </div>
    </div>
  </section>

  <!-- =========================================================== the trust -->
  <section class="p6-sec" style="padding-top: 0" aria-labelledby="p6-why">
    <div class="p6-shell">
      <h2 data-reveal class="p6-h2" id="p6-why">Why investors choose <em>GoldenPi</em>.</h2>
      <div data-reveal class="p6-bento">
        <article class="p6-cell p6-cell--big" style="--i:0">
          <p class="p6-big" aria-hidden="true">5%</p>
          <h3>Only 5% of bonds make the cut.</h3>
          <p>No matter if you chase great returns with corporate bonds or park your money in government-backed bonds, the due diligence has already been handled.</p>
        </article>
        <article class="p6-cell" style="--i:1"><i class="ph ph-hand-coins" aria-hidden="true"></i><h3>Zero brokerage</h3><p>No hidden charges, so the return you see is the return you get.</p></article>
        <article class="p6-cell" style="--i:2"><i class="ph ph-shield-check" aria-hidden="true"></i><h3>One of the first OBPPs</h3><p>Infrastructure built by people who've spent two decades earning Indian investors' trust.</p></article>
        <article class="p6-cell p6-cell--wide" style="--i:3"><i class="ph-thin ph-globe-hemisphere-east p6-globe" aria-hidden="true"></i><i class="ph ph-globe-hemisphere-east" aria-hidden="true"></i><h3>Investing options for NRIs</h3><p>Select bonds are open to NRI investors, a direct, digital way into India's fixed-income market without tiring stacks of paperwork.</p></article>
      </div>
    </div>
  </section>

  <!-- =========================================================== the proof -->
  <section class="p6-sec p6-proof" aria-labelledby="p6-voices">
    <div class="p6-shell">
      <h2 data-reveal class="p6-h2" id="p6-voices">Happy users</h2>
      <!-- DATA: platform milestones, same figures as index.html. -->
      <dl data-reveal class="p6-stats">
        <div><dt><span data-count>18</span><small>Lac+</small></dt><dd>registered users &amp; growing</dd></div>
        <div><dt>&#8377;<span data-count>6300</span><small>Cr+</small></dt><dd>total transaction through our platform</dd></div>
        <div><dt>&#8377;<span data-count>3000</span><small>Cr+</small></dt><dd>worth of bonds available on the platform everyday</dd></div>
      </dl>
      <!-- DATA: reviews, same set as index.html. Without script every quote shows;
           with it, one at a time, chosen by reviewer. -->
      <div data-reveal class="p6-voices">
        <div class="p6-whos" role="tablist" aria-label="Reviews">@TABS@</div>
        <div class="p6-qs">@QUOTES@
        </div>
      </div>
    </div>
  </section>

  <!-- ========================================================== the pocket -->
  <section class="p6-sec" aria-labelledby="p6-get">
    <div class="p6-shell">
      <div data-reveal class="p6-app">
        <div>
          <img class="p6-app__icon" src="@IMG@play/app-icon.png" alt="GoldenPi app icon" width="72" height="72">
          <h2 class="p6-h2" id="p6-get">Your <em>Golden Experience</em> is one tap away.</h2>
          <p class="p6-lead">Build a monthly income stream, protect capital ahead of a goal, or stop watching your money lose ground to inflation.</p>
          <div class="p6-get">
            <img class="p6-qr" src="@IMG@mobile-app-qr.svg" alt="QR code to download the GoldenPi app" width="200" height="247">
            <div class="p6-get__side">
              <p><b>Download App</b>Scan to download GoldenPi app and get voucher</p>
              <a class="p6-play" href="https://play.google.com/store/apps/details?id=com.goldenpi.gpimobileapp"><i class="ph-fill ph-google-play-logo" aria-hidden="true"></i><span>Get it on<b>Google Play</b></span></a>
            </div>
          </div>
        </div>
        <!-- The app's own explore screen, captured at 390px (home-premium5's asset). -->
        <div class="p6-phone"><img src="@IMG@premium5/app-explore.jpg" alt="The GoldenPi app's explore screen" width="780" height="1688" loading="lazy"></div>
      </div>
      <p class="p6-risk">Risk Disclosure: Fixed returns do not constitute guaranteed or assured returns. Investments in corporate debt, municipal debt, and securitized instruments are subject to credit, market, and default risks, including delays or defaults in payments. Read all offer documents carefully.</p>
    </div>
  </section>

</main>"""

SCRIPT = r"""<script>
// home-premium6: reviews picked by name. Progressive enhancement: without this
// every quote is listed and the name strip stays hidden.
(function () {
  var list = document.querySelector('.p6-whos');
  if (!list) return;
  document.documentElement.classList.add('p6-js');
  var tabs = [].slice.call(list.querySelectorAll('[role="tab"]'));
  function select(n, focus) {
    tabs.forEach(function (t, k) {
      var on = k === n;
      t.setAttribute('aria-selected', String(on));
      t.tabIndex = on ? 0 : -1;
      var q = document.getElementById(t.getAttribute('aria-controls'));
      q.classList.toggle('is-on', on);
      q.setAttribute('aria-hidden', String(!on));
      q.tabIndex = on ? 0 : -1;
    });
    if (focus) tabs[n].focus();
  }
  tabs.forEach(function (t, k) {
    t.addEventListener('click', function () { select(k); });
    t.addEventListener('keydown', function (e) {
      var i = null;
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') i = (k + 1) % tabs.length;
      else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') i = (k - 1 + tabs.length) % tabs.length;
      else if (e.key === 'Home') i = 0;
      else if (e.key === 'End') i = tabs.length - 1;
      if (i === null) return;
      e.preventDefault();
      select(i, true);
    });
  });
  select(0);
})();
</script>
"""


def main():
    page = open(SRC, encoding="utf-8").read()
    page, n1 = re.subn(r"<style>\n/\* home-premium: page-only styles.*?</style>", lambda m: STYLE, page, count=1, flags=re.S)
    page, n2 = re.subn(r'<body class="h3-page">', '<body class="p6-page p6">', page, count=1)
    main_html = (MAIN.replace("@TICKETS@", "".join(ticket(i, d) for i, d in enumerate(DEALS)))
                 .replace("@EARN@", "".join(earn_col(i, e) for i, e in enumerate(EARN)))
                 .replace("@TABS@", "".join(review_tab(i, r) for i, r in enumerate(REVIEWS)))
                 .replace("@QUOTES@", "".join(review(i, r) for i, r in enumerate(REVIEWS)))
                 .replace("@ARROW@", ARROW).replace("@IMG@", IMG))
    page, n3 = re.subn(r'<main id="main-content">.*?</main>', lambda m: main_html, page, count=1, flags=re.S)
    page, n4 = re.subn(r"<title>.*?</title>", "<title>GoldenPi | The Golden Experience of Investing</title>", page, count=1)
    k = page.rindex("</body>")
    page = page[:k] + SCRIPT + page[k:]
    if (n1, n2, n3, n4) != (1, 1, 1, 1) or "@" in re.sub(r"@(media|keyframes|import|font-face|supports)", "", main_html):
        raise SystemExit("home-premium3.html changed shape (%d %d %d %d), or a placeholder was left" % (n1, n2, n3, n4))
    if re.search("[–—]", main_html + STYLE):
        raise SystemExit("an en or em dash slipped into the page")
    open(OUT, "w", encoding="utf-8").write(page)
    print("home-premium6.html")


if __name__ == "__main__":
    main()
