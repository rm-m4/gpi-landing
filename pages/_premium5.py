#!/usr/bin/env python3
"""Write home-premium55.html: the homepage in black, white and gold, told as six
chapters, from home-premium2's and home-premium3's content.

  Act one, black: the gold
    the deal      top picks as a rate board, not a card carousel
    the account   three instruments, one golden account
    the case      why bonds: what Rs 1 lakh earns, four reasons
  Act two, off-white, one switch (a rounded edge rising over the black):
    the trust     why investors choose GoldenPi; the key turns as it arrives
    the proof     platform numbers and reviews
    the pocket    the app, a real screen (app7 at 390px, assets/img/premium5/)

Reviewed against taste-skill (2026-10-11): no section numbers or pagination,
stacked section headers, one theme switch, gold metal only on the h1 and the
figures, no comparison tracks, no div-built screens, no idle loops.

Chrome (head links, navbar, footer and its styles, the shared count-up and
reveal scripts) is home-premium3's; only its page styles, <body> class and
<main> are replaced. Copy is the two pages' own; nothing new is written here.

    python3 pages/_premium5.py && python3 pages/_build.py
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "home-premium3.html")
OUT = os.path.join(HERE, "home-premium55.html")
IMG = "../assets/img/"

# DATA: index.html snapshot 2026-09-25, as home-premium2 and 3 show them.
DEALS = [
    ("Akara", "GPID102720.AKARA-CAPITAL-ADVISORS-PRIVATE-LIMITED-2x.png", "Bond Utsav deal", "13.00",
     [("Rating", "ACUITE BBB+"), ("Payout", "Monthly"), ("Maturity", "3-Dec-2027")],
     "https://uatnew.goldenpi.com/bonds/GPID107435/akara-1300-bond-yield?src=view_details&amp;tenureDate=03-Dec-2027"),
    ("NeoGrowth", "GPID104095.Neogrowth-new-logo-1-.jpg", "Bond Utsav deal", "13.00",
     [("Rating", "ICRA BBB"), ("Payout", "Half Yearly"), ("Maturity", "30-Apr-2028")],
     "https://uatnew.goldenpi.com/bonds/GPID107371/neogrowth-1300-bond-yield?src=view_details&amp;tenureDate=30-Apr-2028"),
    ("Best Capital", "GPID107347.Best-Capital.png", "Bond Utsav deal", "13.00",
     [("Rating", "IVR BBB"), ("Payout", "Monthly"), ("Maturity", "11-Sep-2029")],
     "https://uatnew.goldenpi.com/bonds/GPID107433/best-capital-1300-bond-yield?src=view_details&amp;tenureDate=11-Sep-2029"),
    ("Muthoot Fincorp", "GPID100936.MUTHOOT-FINCORP-LIMITED_1-2x.png", "NCD IPO", "9.25",
     [("Type", "NCD IPO"), ("Apply", "At issue"), ("From", "&#8377;10,000")],
     "https://uatnew.goldenpi.com/bond-ipo/GPID100936/muthoot-fincorp-limited?src=preview"),
]

REVIEWS = [
    ("Ankit Sharma", "GoldenPi made bond investing simple and transparent. I could compare yields and complete everything online."),
    ("Priya Nair", "Clear listings and support when I needed help with KYC. Fixed income finally feels accessible."),
    ("Rahul Mehta", "I started with NCD IPOs and now use GoldenPi for secondary bonds too. Smooth experience overall."),
    ("Sneha Kapoor", "The collections helped me shortlist bonds that match my goals without wading through noise."),
    ("Vikram Joshi", "Reliable platform with SEBI registration. That trust factor mattered before I invested."),
]

# (label, rate, GoldenPi's own) -- home-premium2's ladder
EARN = [("Savings account", 2.7, False), ("Large bank FD", 6.5, False),
        ("FDs on GoldenPi", 8.5, True), ("Bonds on GoldenPi", 13.8, True)]

ARROW = '<i class="ph-bold ph-arrow-right" aria-hidden="true"></i>'

STYLE = r"""<style>
/* home-premium5: page-only styles, p5- prefix. Black, off-white and one gold.
   Two acts: black for the offer, one switch to off-white for the proof.
   Radius rule: pills for controls, 24px for panels, 14px for inner tiles,
   12px for issuer logo chips, 48px for the act edge and the phone. */
:root {
  --p5-k: #0a0907; --p5-k2: #12100c; --p5-w: #fcfcfb;
  --p5-gold: #d4af37; --p5-gold-hi: #f3dc8f; --p5-bronze: #8a6520;
  --p5-ink: #0a0907; --p5-sub: #5a564e; --p5-line: #e9e5dc;
  --p5-on-k: #fff; --p5-sub-k: rgba(255,255,255,.62); --p5-line-k: rgba(212,175,55,.18);
  --p5-metal: linear-gradient(100deg, #f7e4a1 0%, #d4af37 42%, #a8841f 68%, #f1d77e 100%);
  --p5-ease: cubic-bezier(.16,1,.3,1);
}
body.p5-page { background: var(--p5-k); }
.p5 { color: var(--p5-ink); }
.p5-shell { max-width: 1240px; margin: 0 auto; padding: 0 20px; }
@media (min-width: 768px) { .p5-shell { padding: 0 40px; } }
.p5-sec { position: relative; padding: 128px 0; overflow-x: clip; }
@media (max-width: 767px) { .p5-sec { padding: 80px 0; } }
.p5-dark { background: var(--p5-k); color: var(--p5-on-k); }
.p5-act2 { position: relative; margin-top: -48px; border-radius: 48px 48px 0 0; background: var(--p5-w); color: var(--p5-ink); box-shadow: 0 -40px 80px -40px rgba(212,175,55,.25); }
@media (max-width: 767px) { .p5-act2 { margin-top: -32px; border-radius: 32px 32px 0 0; } }

.p5-h2 { font-size: clamp(2.25rem, 4.6vw, 3.75rem); line-height: 1.04; letter-spacing: -.035em; font-weight: 700; max-width: 16ch; }
.p5-h1 em { font-style: normal; background: var(--p5-metal); -webkit-background-clip: text; background-clip: text; color: transparent; }
.p5-h2 em { font-style: normal; color: var(--p5-gold); }
.p5-act2 .p5-h2 em { color: var(--p5-bronze); }
.p5-lead { font-size: 1.125rem; line-height: 1.65; color: var(--p5-sub); max-width: 46ch; }
.p5-dark .p5-lead { color: var(--p5-sub-k); }
.p5-dark .p5-lead, .p5-act2 .p5-lead { margin-top: 0; }
.p5-head { display: grid; gap: 20px; margin-bottom: 64px; max-width: 760px; }  /* stacked: one message per section */

/* controls */
.p5-btn { display: inline-flex; align-items: center; gap: 10px; height: 54px; padding: 0 28px; border-radius: 999px; font-weight: 700; font-size: 16px; white-space: nowrap; transition: transform .3s var(--p5-ease), background-color .3s, color .3s, border-color .3s, box-shadow .3s; }
.p5-btn:active { transform: scale(.98); }
.p5-btn--gold { background: var(--p5-gold); color: var(--p5-k); box-shadow: 0 10px 30px -12px rgba(212,175,55,.6); }
.p5-btn--gold:hover { background: var(--p5-gold-hi); }
.p5-btn--ghost { border: 1px solid rgba(255,255,255,.22); color: #fff; }
.p5-btn--ghost:hover { border-color: var(--p5-gold); color: var(--p5-gold-hi); }
.p5-btn--black { background: var(--p5-k); color: #fff; }
.p5-btn--black:hover { background: #26221a; }
.p5-btn i { font-size: 18px; transition: transform .3s var(--p5-ease); }
.p5-btn:hover i { transform: translateX(3px); }
.p5-link { display: inline-flex; align-items: center; gap: 8px; font-weight: 700; }
.p5-link i { transition: transform .3s var(--p5-ease); }
.p5-link:hover i { transform: translateX(4px); }
.p5 :focus-visible { outline: 2px solid var(--p5-gold); outline-offset: 3px; border-radius: 8px; }

/* ===================================================== 01 the deal (hero) */
.p5-hero { position: relative; overflow: hidden; background: var(--p5-k); color: #fff; isolation: isolate; }
.p5-hero::before { content: ""; position: absolute; inset: 0; z-index: -1; pointer-events: none;
  background: radial-gradient(42% 55% at 76% 42%, rgba(212,175,55,.2), transparent 70%), radial-gradient(30% 40% at 8% 100%, rgba(212,175,55,.08), transparent 70%); }
.p5-hero__grid { display: grid; gap: 56px; align-items: center; padding: 72px 0 80px; }
@media (min-width: 1024px) { .p5-hero__grid { grid-template-columns: minmax(0, 1.25fr) minmax(400px, .75fr); gap: 64px; min-height: min(820px, calc(100dvh - 72px)); padding: 56px 0; } }
.p5-trust { display: flex; flex-wrap: wrap; gap: 10px 22px; font-size: 14px; font-weight: 500; color: var(--p5-sub-k); }
.p5-trust li { display: inline-flex; align-items: center; gap: 8px; }
.p5-trust i { color: var(--p5-gold); font-size: 16px; }
.p5-h1 { margin-top: 28px; font-size: clamp(2.75rem, 4.6vw, 4.25rem); line-height: 1.04; letter-spacing: -.04em; font-weight: 700; }
.p5-hero__cta { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 44px; }

/* the rate board: one deal told in full, the others as an index beneath */
.p5-board { position: relative; border-radius: 24px; padding: 28px; border: 1px solid var(--p5-line-k);
  background: linear-gradient(180deg, rgba(255,255,255,.045), rgba(255,255,255,.01)), var(--p5-k2);
  box-shadow: inset 0 1px 0 rgba(255,255,255,.06), 0 60px 120px -40px rgba(0,0,0,.9); }
@media (min-width: 768px) { .p5-board { padding: 36px; } }
.p5-board__head { font-size: 14px; font-weight: 700; color: var(--p5-gold); }
.p5-deal { padding: 28px 0 30px; border-bottom: 1px solid var(--p5-line-k); }
.p5-deal[hidden] { display: none; }
.p5-deal__who { display: flex; align-items: center; gap: 14px; }
.p5-deal__who img { width: 44px; height: 44px; border-radius: 12px; background: #fff; object-fit: contain; padding: 4px; }
.p5-deal__who b { display: block; font-size: 1.125rem; }
.p5-deal__who span { font-size: 13px; color: var(--p5-sub-k); }
.p5-deal__rate { margin-top: 22px; display: flex; align-items: baseline; gap: 14px; }
.p5-deal__rate strong { font-size: clamp(4rem, 6.2vw, 5.75rem); line-height: .9; letter-spacing: -.05em; font-weight: 700; font-variant-numeric: tabular-nums;
  background: var(--p5-metal); -webkit-background-clip: text; background-clip: text; color: transparent; padding-bottom: .04em; }
.p5-deal__rate strong small { font-size: .42em; letter-spacing: 0; }
.p5-deal__rate span { font-size: 14px; color: var(--p5-sub-k); }
.p5-deal__facts { margin-top: 22px; display: grid; grid-template-columns: repeat(3, auto); justify-content: space-between; gap: 12px; }
.p5-deal__facts dt { font-size: 12px; color: var(--p5-sub-k); }
.p5-deal__facts dd { margin-top: 4px; font-weight: 700; white-space: nowrap; }
.p5-deal .p5-link { margin-top: 24px; color: var(--p5-gold-hi); }
.p5-list { display: grid; margin-top: 10px; }
.p5-tab { position: relative; display: grid; grid-template-columns: 34px 1fr auto; align-items: center; gap: 12px; width: 100%; padding: 15px 0; text-align: left; color: var(--p5-sub-k); border-bottom: 1px solid rgba(255,255,255,.06); transition: color .3s; }
.p5-tab:last-child { border-bottom: 0; }
.p5-tab:hover, .p5-tab[aria-selected="true"] { color: #fff; }
.p5-tab__logo { width: 28px; height: 28px; border-radius: 8px; background: #fff; object-fit: contain; padding: 2px; }
.p5-tab__name { font-weight: 700; }
.p5-tab__name small { margin-left: 8px; font-size: 12px; font-weight: 500; opacity: .6; }
.p5-tab__rate { font-weight: 700; font-variant-numeric: tabular-nums; }
.p5-tab__bar { position: absolute; left: 0; right: 0; bottom: -1px; height: 1px; overflow: hidden; }
.p5-tab__bar::after { content: ""; position: absolute; inset: 0; background: var(--p5-gold); transform: scaleX(0); transform-origin: left; }
.p5-tab[aria-selected="true"] .p5-tab__bar::after { transform: none; }

/* shared enter: a panel's parts rise in turn when it is selected */
@keyframes p5-rise { from { opacity: 0; transform: translateY(14px); filter: blur(4px); } }
@keyframes p5-fill { from { transform: scaleX(0); } to { transform: none; } }
@media (prefers-reduced-motion: no-preference) {
  .is-enter > * { animation: p5-rise .7s var(--p5-ease) both; }
  .is-enter > :nth-child(2) { animation-delay: .06s; }
  .is-enter > :nth-child(3) { animation-delay: .12s; }
  .is-enter > :nth-child(4) { animation-delay: .18s; }
  .is-enter > :nth-child(5) { animation-delay: .24s; }
  /* auto-advance: the selected row's hairline fills, then the next row takes over */
  [data-auto] [aria-selected="true"] .p5-tab__bar::after,
  [data-auto] [aria-selected="true"] .p5-voice__bar::after { animation: p5-fill var(--p5-t, 6s) linear both; }
  [data-auto]:hover [aria-selected="true"] *::after, [data-auto]:focus-within [aria-selected="true"] *::after,
  [data-auto].is-off [aria-selected="true"] *::after { animation-play-state: paused; }
  /* hero load-in: words first, then the board */
  .p5-in { animation: p5-rise 1s var(--p5-ease) both; animation-delay: calc(var(--d, 0) * 90ms + 100ms); }
}

/* =================================================== 02 the account (black) */
.p5-inst { border-top: 1px solid var(--p5-line-k); }
.p5-inst > li { border-bottom: 1px solid var(--p5-line-k); }
.p5-inst__row { position: relative; display: grid; gap: 18px; padding: 36px 0; isolation: isolate; }
@media (min-width: 1024px) {
  .p5-inst__row { grid-template-columns: 56px minmax(0, 1.1fr) minmax(0, 1.15fr) 150px; align-items: center; gap: 40px; padding: 44px 28px; margin: 0 -28px; border-radius: 24px; }
  .p5-inst__row::before { content: ""; position: absolute; inset: 0; z-index: -1; border-radius: inherit; background: linear-gradient(100deg, rgba(212,175,55,.12), rgba(212,175,55,.02) 60%); opacity: 0; transition: opacity .5s var(--p5-ease); }
  .p5-inst__row:hover::before, .p5-inst__row:focus-visible::before { opacity: 1; }
}
.p5-inst__row * { transition: color .35s, transform .35s var(--p5-ease); }
.p5-inst__ic { display: grid; place-items: center; width: 56px; height: 56px; border-radius: 14px; font-size: 26px; color: var(--p5-gold); border: 1px solid var(--p5-line-k); }
.p5-inst__row:hover .p5-inst__ic { transform: rotate(-8deg); }
.p5-inst__name { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; font-size: clamp(1.75rem, 3vw, 2.5rem); line-height: 1.1; letter-spacing: -.03em; font-weight: 700; }
.p5-inst__desc { display: block; margin-top: 10px; color: var(--p5-sub-k); line-height: 1.6; max-width: 48ch; }
.p5-inst__facts { display: flex; flex-wrap: wrap; gap: 14px 28px; }
.p5-inst__fact b { display: block; white-space: nowrap; font-size: 1.5rem; line-height: 1.1; letter-spacing: -.02em; font-weight: 700; font-variant-numeric: tabular-nums; }
.p5-inst__fact span { font-size: 13px; color: var(--p5-sub-k); }
.p5-inst__row:hover .p5-inst__fact b, .p5-inst__row:hover .p5-inst__go { color: var(--p5-gold-hi); }
@media (max-width: 1023px) { .p5-inst__facts:empty { display: none; } }
.p5-inst__go { display: inline-flex; align-items: center; gap: 8px; font-weight: 700; justify-self: start; }
@media (min-width: 1024px) { .p5-inst__go { justify-self: end; } }
.p5-inst__row:hover .p5-inst__go i { transform: translateX(4px); }
.p5-inst__go i { transition: transform .3s var(--p5-ease); }
.p5-live { display: inline-flex; align-items: center; gap: 8px; height: 28px; padding: 0 12px; border-radius: 999px; font-size: 12px; font-weight: 700; letter-spacing: .02em; color: #3ccf75; background: rgba(60,207,117,.12); }
.p5-live::before { content: ""; width: 7px; height: 7px; border-radius: 50%; background: currentColor; }
@media (prefers-reduced-motion: no-preference) { .p5-live::before { animation: p5-pulse 1.8s ease-out infinite; } }
@keyframes p5-pulse { 0% { box-shadow: 0 0 0 0 rgba(60,207,117,.45); } 100% { box-shadow: 0 0 0 9px rgba(60,207,117,0); } }

/* ===================================================== 03 the case (black) */
.p5-case { display: grid; gap: 56px; }
@media (min-width: 1024px) { .p5-case { grid-template-columns: 1.15fr .85fr; gap: 80px; align-items: start; } }
.p5-earn { border-radius: 24px; padding: 32px; border: 1px solid var(--p5-line-k); background: var(--p5-k2); }
@media (min-width: 768px) { .p5-earn { padding: 44px; } }
.p5-earn figcaption b { display: block; font-size: 1.5rem; letter-spacing: -.02em; }
.p5-earn figcaption span { display: block; margin-top: 6px; font-size: 14px; color: var(--p5-sub-k); }
.p5-earn ol { display: grid; gap: 26px; margin-top: 40px; }
.p5-earn li { display: grid; grid-template-columns: 1fr auto; gap: 10px 16px; align-items: end; }
.p5-earn__name { font-size: 15px; color: var(--p5-sub-k); }
.p5-earn__val { text-align: right; font-variant-numeric: tabular-nums; }
.p5-earn__val b { display: block; font-size: 1.5rem; line-height: 1; letter-spacing: -.02em; }
.p5-earn__val small { font-size: 13px; color: var(--p5-sub-k); }
.p5-earn__track { grid-column: 1 / -1; height: 10px; }  /* no background track: the bars compare to each other */
.p5-earn__bar { display: block; height: 100%; width: calc(var(--v) / 13.8 * 100%); border-radius: inherit; background: rgba(255,255,255,.3); transform-origin: left; }
.p5-earn .is-gp .p5-earn__name { color: #fff; font-weight: 700; }
.p5-earn .is-gp .p5-earn__val b { background: var(--p5-metal); -webkit-background-clip: text; background-clip: text; color: transparent; }
.p5-earn .is-gp .p5-earn__bar { background: var(--p5-metal); box-shadow: 0 0 24px rgba(212,175,55,.35); }
@media (prefers-reduced-motion: no-preference) {
  .reveal-ready .p5-earn .p5-earn__bar { transform: scaleX(0); transition: transform 1.4s var(--p5-ease); transition-delay: calc(var(--i) * 160ms + 200ms); }
  .reveal-ready .p5-earn.is-in .p5-earn__bar { transform: none; }
}
.p5-why { display: grid; }
.p5-why li { display: grid; grid-template-columns: 48px 1fr; gap: 18px; padding: 26px 0; border-top: 1px solid var(--p5-line-k); }
.p5-why li:last-child { border-bottom: 1px solid var(--p5-line-k); }
.p5-why i { display: grid; place-items: center; width: 48px; height: 48px; border-radius: 14px; font-size: 22px; color: var(--p5-gold); background: rgba(212,175,55,.08); border: 1px solid var(--p5-line-k); }
.p5-why b { display: block; font-size: 1.125rem; }
.p5-why p { margin-top: 4px; color: var(--p5-sub-k); line-height: 1.55; }

/* ==================================================== 04 the trust (white) */
.p5-cut { display: grid; gap: 40px; align-items: center; }
@media (min-width: 1024px) { .p5-cut { grid-template-columns: 1.1fr .9fr; gap: 64px; } }
.p5-cut__num { font-size: clamp(8rem, 20vw, 17rem); line-height: .82; letter-spacing: -.07em; font-weight: 900; font-variant-numeric: tabular-nums;
  background: linear-gradient(170deg, #f1d77e 0%, #d4af37 38%, #8a6520 100%); -webkit-background-clip: text; background-clip: text; color: transparent; padding-bottom: .06em; }
.p5-cut h3 { margin-top: 16px; font-size: clamp(1.5rem, 2.4vw, 2rem); line-height: 1.2; letter-spacing: -.02em; font-weight: 700; max-width: 24ch; }
.p5-cut p { margin-top: 14px; color: var(--p5-sub); line-height: 1.65; max-width: 50ch; }
.p5-cut__art { position: relative; display: grid; place-items: center; aspect-ratio: 1; max-width: 460px; width: 100%; justify-self: center; }
.p5-cut__art::before { content: ""; position: absolute; inset: 8%; border-radius: 50%; background: radial-gradient(circle, rgba(212,175,55,.22), rgba(212,175,55,0) 68%); }
.p5-cut__art::after { content: ""; position: absolute; inset: 4%; border-radius: 50%; border: 1px solid var(--p5-line); }
.p5-cut__art img { position: relative; width: 88%; height: auto; filter: drop-shadow(0 40px 40px rgba(138,101,32,.28)); }
@media (prefers-reduced-motion: no-preference) {  /* the key turns once, as the proof begins */
  .reveal-ready .p5-cut__art img { transform: translateX(-28px) rotate(-14deg); transition: transform 1.6s var(--p5-ease) .2s; }
  .reveal-ready .p5-cut__art.is-in img { transform: none; }
}
.p5-three { margin-top: 88px; }
.p5-three li { display: grid; gap: 8px 48px; padding: 30px 0; border-top: 1px solid var(--p5-line); }
@media (min-width: 900px) { .p5-three li { grid-template-columns: 56px minmax(0, 1fr) minmax(0, 1.3fr); align-items: baseline; } }
.p5-three i { font-size: 28px; color: var(--p5-bronze); align-self: center; }
.p5-three b { font-size: clamp(1.25rem, 2vw, 1.625rem); letter-spacing: -.02em; }
.p5-three p { color: var(--p5-sub); line-height: 1.6; max-width: 54ch; }

/* ==================================================== 05 the proof (black) */
.p5-nums { display: grid; gap: 0; border-top: 1px solid var(--p5-line); border-bottom: 1px solid var(--p5-line); }
@media (min-width: 900px) { .p5-nums { grid-template-columns: 1.15fr 1fr 1fr; } .p5-nums li + li { border-left: 1px solid var(--p5-line); padding-left: 40px; } }
.p5-nums li { padding: 36px 0; }
@media (max-width: 899px) { .p5-nums li + li { border-top: 1px solid var(--p5-line); } }
.p5-nums b { display: block; white-space: nowrap; font-size: clamp(2.5rem, 4.2vw, 3.75rem); line-height: 1; letter-spacing: -.04em; font-weight: 700; font-variant-numeric: tabular-nums;
  background: linear-gradient(170deg, #e2c35a 0%, #b8902c 45%, #8a6520 100%); -webkit-background-clip: text; background-clip: text; color: transparent; padding-bottom: .05em; }
.p5-nums span { display: block; margin-top: 12px; color: var(--p5-sub); max-width: 28ch; }
.p5-voices { display: grid; gap: 48px; margin-top: 88px; }
@media (min-width: 1024px) { .p5-voices { grid-template-columns: 1fr 300px; gap: 96px; align-items: center; } }
.p5-quote { position: relative; min-height: 15rem; }
.p5-quote[hidden] { display: none; }
.p5-quote > i { display: block; font-size: 56px; color: var(--p5-gold); }
.p5-quote__stars, .p5-quote > i { color: var(--p5-bronze); }
.p5-quote__stars { margin-top: 18px; letter-spacing: 4px; color: var(--p5-gold); }
.p5-quote blockquote { margin-top: 14px; font-size: clamp(1.5rem, 3vw, 2.375rem); line-height: 1.3; letter-spacing: -.02em; font-weight: 500; max-width: 26ch; }
.p5-quote figcaption { margin-top: 24px; font-weight: 700; color: var(--p5-sub); }
.p5-voice-list { display: grid; }
.p5-voice { position: relative; display: flex; align-items: center; gap: 14px; width: 100%; padding: 14px 0; text-align: left; color: var(--p5-sub); font-weight: 700; border-bottom: 1px solid var(--p5-line); transition: color .3s; }
.p5-voice:hover, .p5-voice[aria-selected="true"] { color: var(--p5-ink); }
.p5-voice__av { display: grid; place-items: center; width: 40px; height: 40px; border-radius: 50%; font-size: 15px; color: var(--p5-bronze); border: 1px solid var(--p5-line); transition: background-color .3s, color .3s; }
.p5-voice[aria-selected="true"] .p5-voice__av { background: var(--p5-k); color: var(--p5-gold); border-color: var(--p5-k); }
.p5-voice__bar { position: absolute; left: 0; right: 0; bottom: -1px; height: 1px; overflow: hidden; }
.p5-voice__bar::after { content: ""; position: absolute; inset: 0; background: var(--p5-bronze); transform: scaleX(0); transform-origin: left; }
.p5-voice[aria-selected="true"] .p5-voice__bar::after { transform: none; }
@media (max-width: 1023px) {
  .p5-voice-list { grid-auto-flow: column; grid-auto-columns: max-content; gap: 10px; overflow-x: auto; scrollbar-width: none; }
  .p5-voice { border: 0; padding: 0; }
  .p5-voice__name, .p5-voice__bar { display: none; }  /* phone: the initials alone */
  .p5-voice__av { width: 48px; height: 48px; }
}

/* =================================================== 06 the pocket (white) */
.p5-app { display: grid; gap: 64px; align-items: center; }
@media (min-width: 1024px) { .p5-app { grid-template-columns: 1fr 1fr; gap: 80px; } }
.p5-app__list { display: grid; gap: 14px; margin-top: 32px; }
.p5-app__list li { display: flex; align-items: center; gap: 12px; font-weight: 500; }
.p5-app__list i { display: grid; place-items: center; width: 32px; height: 32px; border-radius: 50%; font-size: 16px; color: var(--p5-bronze); background: rgba(212,175,55,.14); }
.p5-get { display: flex; flex-wrap: wrap; align-items: center; gap: 28px; margin-top: 44px; }
.p5-get .p5-btn i { font-size: 22px; }
.p5-qr { display: flex; align-items: center; gap: 14px; }
.p5-qr img { width: 88px; height: 88px; padding: 6px; border-radius: 14px; border: 1px solid var(--p5-line); background: #fff; }
.p5-qr p { font-size: 13px; color: var(--p5-sub); max-width: 18ch; line-height: 1.45; }
.p5-qr b { display: block; color: var(--p5-ink); font-size: 15px; }
@media (max-width: 767px) { .p5-qr { display: none; } }
.p5-act2 .p5-sec:first-child { padding-top: 120px; }
.p5-stage { position: relative; display: grid; place-items: center; padding: 24px 0; }
.p5-stage::before { content: ""; position: absolute; width: min(520px, 100%); aspect-ratio: 1; border-radius: 50%; background: radial-gradient(circle at 50% 45%, #f6e3a3 0%, #d4af37 45%, rgba(212,175,55,0) 71%); opacity: .55; }
.p5-phone { position: relative; width: 300px; max-width: 100%; border-radius: 48px; padding: 10px; background: linear-gradient(145deg, #3a3730, #0a0907 40%, #2a2721); box-shadow: 0 0 0 1px rgba(10,9,7,.6), 0 50px 100px -30px rgba(10,9,7,.5); }
.p5-phone img { display: block; width: 100%; height: auto; border-radius: 38px; }
@media (prefers-reduced-motion: no-preference) {
  .reveal-ready .p5-stage .p5-phone { transform: translateY(40px) rotate(-3deg); opacity: 0; transition: transform 1.2s var(--p5-ease), opacity .8s; }
  .reveal-ready .p5-stage.is-in .p5-phone { transform: none; opacity: 1; }
  .reveal-ready .p5-stage[data-reveal] { opacity: 1; transform: none; }  /* the parts move, not the stage */
}
.p5-risk { margin-top: 96px; padding-top: 28px; border-top: 1px solid var(--p5-line); font-size: 13px; line-height: 1.6; color: var(--p5-sub); max-width: 110ch; }
</style>"""


def deal_panel(i, d):
    name, logo, tag, rate, facts, href = d
    facts = "".join("<div><dt>%s</dt><dd>%s</dd></div>" % f for f in facts)
    return ('      <div class="p5-deal%s" id="p5-deal-%d" role="tabpanel" aria-labelledby="p5-dtab-%d"%s>\n'
            '        <div class="p5-deal__who"><img src="%s%s" alt="" width="44" height="44"><div><b>%s</b><span>%s</span></div></div>\n'
            '        <p class="p5-deal__rate"><strong>%s<small>%%</small></strong><span>Returns</span></p>\n'
            '        <dl class="p5-deal__facts">%s</dl>\n'
            '        <a class="p5-link" href="%s" aria-label="Know more about %s">Know more %s</a>\n'
            '      </div>\n') % ("" if i else " is-enter", i + 1, i + 1, " hidden" if i else "",
                                 IMG, logo, name, tag, rate, facts, href, name, ARROW)


def deal_tab(i, d):
    name, tag, rate = d[0], d[2], d[3]
    short = "Bond" if tag == "Bond Utsav deal" else tag
    return ('        <button type="button" class="p5-tab" role="tab" id="p5-dtab-%d" aria-controls="p5-deal-%d" aria-selected="%s"%s>'
            '<img class="p5-tab__logo" src="%s%s" alt="" width="28" height="28"><span class="p5-tab__name">%s<small>%s</small></span>'
            '<span class="p5-tab__rate">%s%%</span><span class="p5-tab__bar" aria-hidden="true"></span></button>\n') % (
        i + 1, i + 1, "true" if i == 0 else "false", "" if i == 0 else ' tabindex="-1"', IMG, d[1], name, short, rate)


def quote(i, r):
    name, text = r
    return ('        <figure class="p5-quote%s" id="p5-rev-%d" role="tabpanel" aria-labelledby="p5-rtab-%d"%s>\n'
            '          <i class="ph-fill ph-quotes" aria-hidden="true"></i>\n'
            '          <div class="p5-quote__stars" role="img" aria-label="5 out of 5">&#9733;&#9733;&#9733;&#9733;&#9733;</div>\n'
            '          <blockquote>%s</blockquote>\n'
            '          <figcaption>%s</figcaption>\n'
            '        </figure>\n') % ("" if i else " is-enter", i + 1, i + 1, " hidden" if i else "", text, name)


def voice(i, r):
    name = r[0]
    return ('          <button type="button" class="p5-voice" role="tab" id="p5-rtab-%d" aria-controls="p5-rev-%d" aria-selected="%s"%s aria-label="%s">'
            '<span class="p5-voice__av" aria-hidden="true">%s</span><span class="p5-voice__name">%s</span>'
            '<span class="p5-voice__bar" aria-hidden="true"></span></button>\n') % (
        i + 1, i + 1, "true" if i == 0 else "false", "" if i == 0 else ' tabindex="-1"', name, name[0], name)


def earn_row(i, e):
    label, rate, gp = e
    return ('          <li%s style="--v:%s; --i:%d"><span class="p5-earn__name">%s</span>'
            '<span class="p5-earn__val"><b>%s%%</b><small>&#8377;%s</small></span>'
            '<span class="p5-earn__track"><span class="p5-earn__bar"></span></span></li>\n') % (
        ' class="is-gp"' if gp else "", rate, i, label, rate, "{:,}".format(round(rate * 1000)), )


MAIN = """<main id="main-content">
  <!-- COPY: every line is home-premium2's or home-premium3's own (their sources
       are noted there). The chapter numbers are structure, not copy.
       DATA: deals, rates, figures and reviews are the index.html snapshot
       2026-09-25, as those pages show them. The rupee figures beside the
       ladder are the rates applied to the ladder's Rs 1 lakh, nothing more. -->

  <!-- ================================================ 01 the deal -->
  <section class="p5-hero" aria-labelledby="p5-title">
    <div class="p5-shell p5-hero__grid">
      <div>
        <ul class="p5-trust p5-in" style="--d:0">
          <li><i class="ph-fill ph-seal-check" aria-hidden="true"></i>SEBI registered Debt Broker</li>
          <li><i class="ph-fill ph-seal-check" aria-hidden="true"></i>OBPP license holder</li>
          <li><i class="ph-fill ph-seal-check" aria-hidden="true"></i>Fixed returns up to 13.8%</li>
        </ul>
        <h1 class="p5-h1 p5-in" style="--d:1" id="p5-title">The golden experience <em>of investing.</em></h1>
        <div class="p5-hero__cta p5-in" style="--d:2">
          <a class="p5-btn p5-btn--gold" href="signup.html">Start investing @ARROW@</a>
          <a class="p5-btn p5-btn--ghost" href="corporate-bonds.html">Explore bonds</a>
        </div>
      </div>

      <!-- DATA: top picks, index.html snapshot 2026-09-25 (the three Bond Utsav
           deals and the open NCD IPO). One is told in full; the rest wait in
           the index beneath it, so every deal is on screen at once. -->
      <div class="p5-board p5-in" style="--d:4" data-rotator data-auto>
        <p class="p5-board__head">Top picks today</p>
@PANELS@        <div class="p5-list" role="tablist" aria-label="Top picks today">
@TABS@        </div>
      </div>
    </div>
  </section>

  <!-- ================================================ 02 the account -->
  <section class="p5-sec p5-dark" aria-labelledby="p5-assets">
    <div class="p5-shell">
      <div class="p5-head" data-reveal>
        <div><h2 class="p5-h2" id="p5-assets">Three instruments. <em>One golden account.</em></h2></div>
        <p class="p5-lead">Everything fixed income, under one login and one KYC. Pick the payout, the tenure and the risk you are comfortable with.</p>
      </div>
      <ol class="p5-inst">
        <li data-reveal><a class="p5-inst__row" href="corporate-bonds.html">
          <i class="p5-inst__ic ph-light ph-certificate" aria-hidden="true"></i>
          <span><span class="p5-inst__name">Corporate Bonds</span><span class="p5-inst__desc">Lend to established Indian companies and collect fixed interest on a schedule you choose. Every bond is credit rated, every cash flow shown upfront.</span></span>
          <span class="p5-inst__facts"><span class="p5-inst__fact"><b>13.8%</b><span>Returns, up to</span></span><span class="p5-inst__fact"><b>Monthly</b><span>Payouts available</span></span><span class="p5-inst__fact"><b>A or above</b><span>Highly rated picks</span></span></span>
          <span class="p5-inst__go">Explore bonds @ARROW@</span>
        </a></li>
        <li data-reveal><a class="p5-inst__row" href="fixed-deposits.html">
          <i class="p5-inst__ic ph-light ph-bank" aria-hidden="true"></i>
          <span><span class="p5-inst__name">Fixed Deposits</span><span class="p5-inst__desc">Book FDs with leading small finance banks and NBFCs, without opening a new bank account.</span></span>
          <span class="p5-inst__facts"><span class="p5-inst__fact"><b>8.5%</b><span>Highest returns</span></span><span class="p5-inst__fact"><b>&#8377;5L</b><span>Insured upto</span></span></span>
          <span class="p5-inst__go">Explore FDs @ARROW@</span>
        </a></li>
        <li data-reveal><a class="p5-inst__row" href="bond-ipo-online.html">
          <i class="p5-inst__ic ph-light ph-rocket-launch" aria-hidden="true"></i>
          <span><span class="p5-inst__name">NCD IPOs <span class="p5-live">Live now</span></span><span class="p5-inst__desc">Apply to new bond issues at face value, straight into your demat, before they list.</span></span>
          <span class="p5-inst__facts"></span>
          <span class="p5-inst__go">See open IPOs @ARROW@</span>
        </a></li>
      </ol>
    </div>
  </section>

  <!-- ================================================ 03 the case -->
  <section class="p5-sec p5-dark" aria-labelledby="p5-whybonds">
    <div class="p5-shell">
      <div class="p5-head" data-reveal>
        <div><h2 class="p5-h2" id="p5-whybonds">Why bonds belong in <em>your portfolio.</em></h2></div>
        <p class="p5-lead">Bonds sit between the safety of a deposit and the growth of equity. You know what you will earn, and when, on the day you invest.</p>
      </div>
      <div class="p5-case">
        <!-- DATA: savings and bank FD rows are indicative market rates, not GoldenPi
             listings; the two gold rows are the snapshot highs from index.html. -->
        <figure class="p5-earn" data-reveal>
          <figcaption><b>What &#8377;1 lakh can earn in a year</b><span>Indicative annual rates, before tax</span></figcaption>
          <ol>
@EARN@          </ol>
        </figure>
        <ul class="p5-why" data-reveal>
          <li><i class="ph ph-calendar-check" aria-hidden="true"></i><div><b>Predictable income</b><p>Interest lands on fixed dates, monthly to yearly.</p></div></li>
          <li><i class="ph ph-trend-up" aria-hidden="true"></i><div><b>Higher than FDs</b><p>Rated corporate debt typically pays a premium over bank deposits.</p></div></li>
          <li><i class="ph ph-anchor-simple" aria-hidden="true"></i><div><b>Steadier than stocks</b><p>Returns are set at purchase, not by daily market moods.</p></div></li>
          <li><i class="ph ph-chart-pie-slice" aria-hidden="true"></i><div><b>Real diversification</b><p>Spread across issuers, ratings and maturities.</p></div></li>
        </ul>
      </div>
    </div>
  </section>

  <!-- ================================================ 04 the trust -->
  <div class="p5-act2">
  <section class="p5-sec" aria-labelledby="p5-whygp">
    <div class="p5-shell">
      <div class="p5-head" data-reveal><div><h2 class="p5-h2" id="p5-whygp">Why investors choose <em>GoldenPi.</em></h2></div></div>
      <div class="p5-cut">
        <div data-reveal>
          <div class="p5-cut__num" aria-hidden="true">5%</div>
          <h3>Only 5% of bonds make the cut.</h3>
          <p>No matter if you chase great returns with corporate bonds or park your money in government-backed bonds, the due diligence has already been handled.</p>
        </div>
        <div class="p5-cut__art" data-reveal><img src="@IMG@premium5/why-lock.png" alt="" width="760" height="634" loading="lazy" decoding="async"></div>
      </div>
      <ul class="p5-three">
        <li data-reveal><i class="ph ph-receipt-x" aria-hidden="true"></i><b>Zero brokerage</b><p>No hidden charges, so the return you see is the return you get.</p></li>
        <li data-reveal><i class="ph ph-medal" aria-hidden="true"></i><b>One of the first OBPPs</b><p>Infrastructure built by people who've spent two decades earning Indian investors' trust.</p></li>
        <li data-reveal><i class="ph ph-globe-hemisphere-east" aria-hidden="true"></i><b>Investing options for NRIs</b><p>Select bonds are open to NRI investors, a direct, digital way into India's fixed-income market without tiring stacks of paperwork.</p></li>
      </ul>
    </div>
  </section>

  <!-- ================================================ 05 the proof -->
  <section class="p5-sec" aria-labelledby="p5-reviews">
    <div class="p5-shell">
      <div class="p5-head" data-reveal><div><h2 class="p5-h2" id="p5-reviews">Happy users</h2></div></div>
      <!-- DATA: platform milestones, same figures as index.html. -->
      <ul class="p5-nums" data-reveal>
        <li><b data-count>18 Lac+</b><span>registered users &amp; growing</span></li>
        <li><b data-count>&#8377;6,300 Cr+</b><span>total transaction through our platform</span></li>
        <li><b data-count>&#8377;3,000 Cr+</b><span>worth of bonds available on the platform everyday</span></li>
      </ul>
      <!-- DATA: reviews, same set as index.html. -->
      <div class="p5-voices" data-rotator data-auto style="--p5-t:7s">
        <div>
@QUOTES@        </div>
        <div class="p5-voice-list" role="tablist" aria-label="Reviews">
@VOICES@        </div>
      </div>
    </div>
  </section>

  <!-- ================================================ 06 the pocket -->
  <section class="p5-sec" aria-labelledby="p5-app">
    <div class="p5-shell">
      <div class="p5-app">
        <div data-reveal>
          
          <h2 class="p5-h2" id="p5-app">Your Golden Experience is <em>one tap away.</em></h2>
          <p class="p5-lead" style="margin-top:20px">Build a monthly income stream, protect capital ahead of a goal, or stop watching your money lose ground to inflation.</p>
          <ul class="p5-app__list">
            <li><i class="ph-bold ph-bell-ringing" aria-hidden="true"></i>Alerts the moment an NCD IPO opens</li>
            <li><i class="ph-bold ph-calendar-dots" aria-hidden="true"></i>Every holding and payout date in one view</li>
            <li><i class="ph-bold ph-lightning" aria-hidden="true"></i>Invest with UPI in a few taps</li>
          </ul>
          <div class="p5-get">
            <a class="p5-btn p5-btn--black" href="https://play.google.com/store/apps/details?id=com.goldenpi.gpimobileapp"><i class="ph-fill ph-google-play-logo" aria-hidden="true"></i>Get it on Google Play</a>
            <div class="p5-qr"><img src="@IMG@mobile-app-qr.svg" alt="QR code to download the GoldenPi app" width="88" height="88" loading="lazy"><p><b>Download App</b>Scan to download GoldenPi app and get voucher</p></div>
          </div>
        </div>
        <!-- The app's own screen: user-explore-app7.html at 390px, captured 2026-10-11. -->
        <div class="p5-stage" data-reveal aria-hidden="true">
          <div class="p5-phone"><img src="@IMG@premium5/app-explore.jpg" alt="" width="780" height="1688" loading="lazy" decoding="async"></div>
        </div>
      </div>
      <p class="p5-risk">Risk Disclosure: Fixed returns do not constitute guaranteed or assured returns. Investments in corporate debt, municipal debt, and securitized instruments are subject to credit, market, and default risks, including delays or defaults in payments. Read all offer documents carefully.</p>
    </div>
  </section>
  </div>
</main>"""

# One tab rotator, two uses (the deal board and the reviews). Without script
# the first panel shows and the index still lists every deal / reviewer.
SCRIPT = """<script>
// home-premium5: tab rotators. Auto-advance is CSS: the selected tab's hairline
// fills (p5-fill), and its animationend selects the next tab. Hover, focus,
// an offscreen board or a hidden tab pause it; reduced motion has no fill,
// so nothing advances on its own.
(function () {
  document.querySelectorAll('[data-rotator]').forEach(function (root) {
    var tabs = [].slice.call(root.querySelectorAll('[role="tab"]'));
    var panels = tabs.map(function (t) { return document.getElementById(t.getAttribute('aria-controls')); });
    var cur = 0;
    function select(n, focus) {
      cur = n;
      tabs.forEach(function (t, k) {
        var on = k === n;
        t.setAttribute('aria-selected', String(on));
        t.tabIndex = on ? 0 : -1;
        panels[k].hidden = !on;
        panels[k].classList.toggle('is-enter', on);
      });
      if (focus) tabs[n].focus();
    }
    tabs.forEach(function (t, k) {
      t.addEventListener('click', function () { select(k); });
      t.addEventListener('keydown', function (e) {
        var i = { ArrowRight: k + 1, ArrowDown: k + 1, ArrowLeft: k - 1, ArrowUp: k - 1, Home: 0, End: tabs.length - 1 }[e.key];
        if (i === undefined) return;
        e.preventDefault();
        select((i + tabs.length) % tabs.length, true);
      });
    });
    root.addEventListener('animationend', function (e) {
      if (e.animationName === 'p5-fill') select((cur + 1) % tabs.length);
    });
    function off(v) { root.classList.toggle('is-off', v); }
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) { off(!es[0].isIntersecting || document.hidden); }).observe(root);
    }
    document.addEventListener('visibilitychange', function () { if (document.hidden) off(true); });
  });
})();
</script>
"""


def main():
    page = open(SRC, encoding="utf-8").read()
    page, n1 = re.subn(r"<style>\n/\* home-premium: page-only styles.*?</style>", lambda m: STYLE, page, count=1, flags=re.S)
    page, n2 = re.subn(r'<body class="h3-page">', '<body class="p5-page p5">', page, count=1)
    main_html = (MAIN.replace("@PANELS@", "".join(deal_panel(i, d) for i, d in enumerate(DEALS)))
                 .replace("@TABS@", "".join(deal_tab(i, d) for i, d in enumerate(DEALS)))
                 
                 .replace("@QUOTES@", "".join(quote(i, r) for i, r in enumerate(REVIEWS)))
                 .replace("@VOICES@", "".join(voice(i, r) for i, r in enumerate(REVIEWS)))
                 .replace("@EARN@", "".join(earn_row(i, e) for i, e in enumerate(EARN)))
                 .replace("@ARROW@", ARROW).replace("@IMG@", IMG))
    page, n3 = re.subn(r'<main id="main-content">.*?</main>', lambda m: main_html, page, count=1, flags=re.S)
    page, n4 = re.subn(r"<title>.*?</title>", "<title>GoldenPi | The Golden Experience of Investing</title>", page, count=1)
    k = page.rindex("</body>")
    page = page[:k] + SCRIPT + page[k:]
    if (n1, n2, n3, n4) != (1, 1, 1, 1) or "@" in re.sub(r"@(media|keyframes|import|font-face|supports)", "", main_html):
        raise SystemExit("home-premium3.html changed shape (%d %d %d %d), or a placeholder was left" % (n1, n2, n3, n4))
    open(OUT, "w", encoding="utf-8").write(page)
    print("home-premium55.html")


if __name__ == "__main__":
    main()
