#!/usr/bin/env python3
"""Write home-premium7.html: the homepage in black, white and gold, from
home-premium2's and home-premium3's content, told as one story.

  Black, the offer
    1 the deal     premium2's centred hero; the top three deals as one term sheet,
                   three columns behind a single gold rule, not a card carousel
    2 the account  three instruments, one golden account, as a low strip
  White, the reasoning (one switch: a rounded edge rising over the black)
    3 the case     why bonds: what Rs 1 lakh earns as rising columns, four reasons
    4 the trust    why investors choose GoldenPi, premium3's bento
    5 the proof    platform numbers on a black slab, then the reviews
  Black, the pocket
    6 the app      premium3's finale, with a QR big enough to scan from the screen

Design pass with ui-ux-pro-max (2026-10-11): scroll-triggered storytelling,
spacious density, standard motion. Its Cormorant/Montserrat pairing is not
used: the repo's typeface is Satoshi. Motion is CSS on the shared reveal and
count-up scripts; nothing moves under reduced motion, nothing loops idle.

Chrome (head links, navbar, footer, the count-up and reveal scripts) is
home-premium3's; only its page styles, <body> class and <main> are replaced.
Copy is the two pages' own; nothing new is written here.

    python3 pages/_premium7.py && python3 pages/_build.py
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "home-premium3.html")
OUT = os.path.join(HERE, "home-premium7.html")
IMG = "../assets/img/"

# DATA: top 3 Bond Utsav deals, index.html snapshot 2026-09-25, as home-premium2 shows them.
DEALS = [
    ("Akara", "GPID102720.AKARA-CAPITAL-ADVISORS-PRIVATE-LIMITED-2x.png", "13.00", "ACUITE BBB+", "Monthly", "3-Dec-2027",
     "https://uatnew.goldenpi.com/bonds/GPID107435/akara-1300-bond-yield?src=view_details&amp;tenureDate=03-Dec-2027"),
    ("NeoGrowth", "GPID104095.Neogrowth-new-logo-1-.jpg", "13.00", "ICRA BBB", "Half Yearly", "30-Apr-2028",
     "https://uatnew.goldenpi.com/bonds/GPID107371/neogrowth-1300-bond-yield?src=view_details&amp;tenureDate=30-Apr-2028"),
    ("Best Capital", "GPID107347.Best-Capital.png", "13.00", "IVR BBB", "Monthly", "11-Sep-2029",
     "https://uatnew.goldenpi.com/bonds/GPID107433/best-capital-1300-bond-yield?src=view_details&amp;tenureDate=11-Sep-2029"),
]

# (label, rate, GoldenPi's own) -- home-premium2's ladder
EARN = [("Savings account", 2.7, False), ("Large bank FD", 6.5, False),
        ("FDs on GoldenPi", 8.5, True), ("Bonds on GoldenPi", 13.8, True)]

REVIEWS = [
    ("Ankit Sharma", "GoldenPi made bond investing simple and transparent. I could compare yields and complete everything online."),
    ("Priya Nair", "Clear listings and support when I needed help with KYC. Fixed income finally feels accessible."),
    ("Rahul Mehta", "I started with NCD IPOs and now use GoldenPi for secondary bonds too. Smooth experience overall."),
    ("Sneha Kapoor", "The collections helped me shortlist bonds that match my goals without wading through noise."),
    ("Vikram Joshi", "Reliable platform with SEBI registration. That trust factor mattered before I invested."),
]

ARROW = '<i class="ph-bold ph-arrow-right" aria-hidden="true"></i>'
STARS = '<span class="p7-stars" role="img" aria-label="5 out of 5">&#9733;&#9733;&#9733;&#9733;&#9733;</span>'

STYLE = r"""<style>
/* home-premium7: page-only styles, p7- prefix. Black, warm white and one gold.
   Radius rule: pills for controls, 28px for panels, 16px for inner tiles,
   12px for logo chips, 48px for the act edge. */
:root {
  --p7-k: #0a0907; --p7-k2: #13110d; --p7-k3: #1c1913; --p7-w: #fbfaf7; --p7-w2: #f3f0e9;
  --p7-gold: #d4af37; --p7-gold-hi: #f3dc8f; --p7-bronze: #8a6520;
  --p7-ink: #0a0907; --p7-sub: #57534a; --p7-line: #e7e2d6;
  --p7-sub-k: rgba(255,255,255,.66); --p7-line-k: rgba(212,175,55,.2);
  --p7-metal: linear-gradient(100deg, #f7e4a1 0%, #d4af37 40%, #a8841f 66%, #f1d77e 100%);
  --p7-ease: cubic-bezier(.16,1,.3,1);
}
body.p7-page { background: var(--p7-k); }
.p7 { color: var(--p7-ink); }
.p7-shell { max-width: 1240px; margin: 0 auto; padding: 0 20px; }
@media (min-width: 768px) { .p7-shell { padding: 0 40px; } }
.p7-sec { position: relative; padding: 120px 0; overflow-x: clip; }
@media (max-width: 767px) { .p7-sec { padding: 80px 0; } }
.p7-dark { background: var(--p7-k); color: #fff; }
.p7-act2 { position: relative; margin-top: -48px; border-radius: 48px 48px 0 0; background: var(--p7-w); color: var(--p7-ink); box-shadow: 0 -40px 90px -40px rgba(212,175,55,.3); }
@media (max-width: 767px) { .p7-act2 { margin-top: -32px; border-radius: 32px 32px 0 0; } }

.p7-h2 { font-size: clamp(2.125rem, 4.4vw, 3.5rem); line-height: 1.05; letter-spacing: -.035em; font-weight: 700; max-width: 17ch; text-wrap: balance; }
.p7-h2 em, .p7-h1 em { font-style: normal; background: var(--p7-metal); -webkit-background-clip: text; background-clip: text; color: transparent; }
.p7-act2 .p7-h2 em { background: none; color: var(--p7-bronze); }
.p7-lead { font-size: 1.125rem; line-height: 1.65; color: var(--p7-sub); max-width: 48ch; }
.p7-dark .p7-lead { color: var(--p7-sub-k); }
.p7-head { display: grid; gap: 20px; margin-bottom: 56px; }

/* controls */
.p7-btn { display: inline-flex; align-items: center; gap: 10px; min-height: 54px; padding: 0 28px; border-radius: 999px; font-weight: 700; font-size: 16px; white-space: nowrap; transition: transform .3s var(--p7-ease), background-color .3s, color .3s, border-color .3s, box-shadow .3s; }
.p7-btn:active { transform: scale(.98); }
.p7-btn--gold { background: var(--p7-gold); color: var(--p7-k); box-shadow: 0 12px 32px -12px rgba(212,175,55,.65); }
.p7-btn--gold:hover { background: var(--p7-gold-hi); }
.p7-btn--ghost { border: 1px solid rgba(255,255,255,.24); color: #fff; }
.p7-btn--ghost:hover { border-color: var(--p7-gold); color: var(--p7-gold-hi); }
.p7-btn i { font-size: 18px; transition: transform .3s var(--p7-ease); }
.p7-btn:hover i { transform: translateX(3px); }
.p7-link { display: inline-flex; align-items: center; gap: 8px; font-weight: 700; }
.p7-link i { transition: transform .3s var(--p7-ease); }
.p7 :focus-visible { outline: 2px solid var(--p7-gold); outline-offset: 3px; border-radius: 8px; }

/* ============================================================ 1 the deal */
.p7-hero { position: relative; overflow: hidden; isolation: isolate; padding: 88px 0 112px; text-align: center; }
.p7-hero::before { content: ""; position: absolute; inset: 0; z-index: -1; pointer-events: none;
  background: radial-gradient(50% 45% at 50% 0%, rgba(212,175,55,.22), transparent 72%), radial-gradient(40% 40% at 50% 100%, rgba(212,175,55,.1), transparent 70%); }
.p7-hero__pi { position: absolute; z-index: -1; left: 50%; top: 40px; width: min(820px, 120vw); height: auto; transform: translateX(-50%); opacity: .6; pointer-events: none; }
.p7-trust { display: flex; flex-wrap: wrap; justify-content: center; gap: 10px 24px; font-size: 14px; font-weight: 500; color: var(--p7-sub-k); }
.p7-trust li { display: inline-flex; align-items: center; gap: 8px; }
.p7-trust i { color: var(--p7-gold); font-size: 16px; }
.p7-h1 { margin: 28px auto 0; font-size: clamp(2.5rem, 6vw, 5.25rem); line-height: 1.04; letter-spacing: -.045em; font-weight: 700; text-wrap: balance; }
.p7-h1 > * { display: block; }
@media (min-width: 1024px) { .p7-h1 > * { white-space: nowrap; } }  /* two lines on desktop, by request */
.p7-hero__cta { display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; margin-top: 40px; }

/* the term sheet: three deals, one panel, one gold rule across the top */
.p7-sheet { position: relative; margin-top: 72px; border: 1px solid var(--p7-line-k); border-radius: 28px; background: linear-gradient(180deg, var(--p7-k3), var(--p7-k2)); text-align: left;
  box-shadow: 0 60px 120px -50px rgba(212,175,55,.35), inset 0 1px 0 rgba(255,255,255,.06); }
.p7-sheet__rule { position: absolute; left: 28px; right: 28px; top: -1px; height: 2px; background: var(--p7-metal); border-radius: 2px; transform-origin: left; }
.p7-sheet__list { display: grid; }
@media (min-width: 900px) { .p7-sheet__list { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
.p7-deal { position: relative; padding: 32px 28px 28px; transition: background-color .4s; }
.p7-deal + .p7-deal { border-top: 1px solid var(--p7-line-k); }
@media (min-width: 900px) { .p7-deal { padding: 40px 36px 36px; } .p7-deal + .p7-deal { border-top: 0; border-left: 1px solid var(--p7-line-k); } }
.p7-deal:first-child { border-radius: 28px 28px 0 0; }
.p7-deal:last-child { border-radius: 0 0 28px 28px; }
@media (min-width: 900px) { .p7-deal:first-child { border-radius: 28px 0 0 28px; } .p7-deal:last-child { border-radius: 0 28px 28px 0; } }
.p7-deal:hover, .p7-deal:focus-within { background: rgba(212,175,55,.06); }
.p7-deal__top { display: flex; align-items: center; gap: 14px; }
.p7-chip { flex: none; display: grid; place-items: center; width: 48px; height: 48px; border-radius: 12px; background: #fff; overflow: hidden; }
.p7-chip img { width: 40px; height: 40px; object-fit: contain; }
.p7-deal h3 { font-size: 18px; font-weight: 700; color: #fff; }
.p7-deal__tag { display: block; font-size: 13px; color: var(--p7-gold); font-weight: 500; }
.p7-deal__rate { margin-top: 28px; display: flex; align-items: baseline; gap: 4px; line-height: .9; }
.p7-deal__rate b { font-size: clamp(3.25rem, 5.4vw, 4.5rem); font-weight: 700; letter-spacing: -.05em; background: var(--p7-metal); -webkit-background-clip: text; background-clip: text; color: transparent; font-variant-numeric: tabular-nums; }
.p7-deal__rate span { font-size: 1.5rem; font-weight: 700; color: var(--p7-gold); }
.p7-deal__label { margin-top: 10px; font-size: 14px; color: var(--p7-sub-k); }
.p7-deal dl { display: grid; grid-template-columns: repeat(3, auto); justify-content: start; gap: 6px 28px; margin-top: 28px; padding-top: 20px; border-top: 1px dashed rgba(255,255,255,.14); }
.p7-deal dt { font-size: 12px; color: var(--p7-sub-k); }
.p7-deal dd { font-size: 14px; font-weight: 700; color: #fff; white-space: nowrap; }
@media (max-width: 899px) {
  .p7-deal { display: grid; grid-template-columns: 1fr auto; align-items: center; column-gap: 16px; }
  .p7-deal__rate { margin-top: 0; grid-column: 2; grid-row: 1; }
  .p7-deal__rate b { font-size: 2.25rem; }
  .p7-deal h3 { font-size: 16px; white-space: nowrap; }
  .p7-deal__rate span { font-size: 1.125rem; }
  .p7-deal__label { display: none; }
  .p7-deal dl, .p7-deal__go { grid-column: 1 / -1; }
  .p7-deal dl { margin-top: 20px; padding-top: 16px; }
  .p7-deal__go { margin-top: 8px; justify-self: start; }
}
@media (max-width: 420px) { .p7-deal dl { gap: 6px 18px; } .p7-deal dd { font-size: 13px; } }
.p7-deal__go { margin-top: 28px; color: var(--p7-gold-hi); min-height: 44px; }
.p7-deal__go::after { content: ""; position: absolute; inset: 0; border-radius: inherit; }  /* whole column is the target */
.p7-deal:hover .p7-deal__go i { transform: translateX(4px); }

@media (prefers-reduced-motion: no-preference) {
  .p7-rise { animation: p7-rise 1s var(--p7-ease) both; animation-delay: calc(var(--d, 0) * 110ms); }
  .p7-sheet__rule { animation: p7-draw 1.6s var(--p7-ease) .55s both; }
  .p7-deal { animation: p7-rise 1s var(--p7-ease) both; animation-delay: calc(500ms + var(--i) * 140ms); }
}
@keyframes p7-rise { from { opacity: 0; transform: translateY(24px); } }
@keyframes p7-draw { from { transform: scaleX(0); } }

/* ========================================================= 2 the account */
.p7-sec--tight { padding: 40px 0 128px; }
@media (max-width: 767px) { .p7-sec--tight { padding: 16px 0 96px; } }
.p7-inst { display: grid; border-top: 1px solid rgba(255,255,255,.12); border-bottom: 1px solid rgba(255,255,255,.12); }
@media (min-width: 900px) { .p7-inst { grid-template-columns: 1.3fr 1fr 1fr; } }
.p7-inst li + li { border-top: 1px solid rgba(255,255,255,.12); }
@media (min-width: 900px) { .p7-inst li + li { border-top: 0; border-left: 1px solid rgba(255,255,255,.12); } }
.p7-inst a { position: relative; display: grid; grid-template-columns: auto 1fr auto; grid-template-areas: "icon name arrow" "icon fact arrow"; align-items: center; column-gap: 18px; row-gap: 4px; padding: 28px 8px; transition: background-color .4s; }
@media (min-width: 900px) { .p7-inst a { padding: 32px 32px; } .p7-inst li:first-child a { padding-left: 0; } }
.p7-inst a::after { content: ""; position: absolute; left: 0; right: 0; top: -1px; height: 2px; background: var(--p7-metal); transform: scaleX(0); transform-origin: left; transition: transform .6s var(--p7-ease); }
.p7-inst a:hover::after, .p7-inst a:focus-visible::after { transform: scaleX(1); }
.p7-inst a > i { grid-area: icon; color: var(--p7-gold); font-size: 30px; }
.p7-inst h3 { grid-area: name; font-size: 20px; font-weight: 700; }
.p7-inst__fact { grid-area: fact; display: flex; align-items: baseline; gap: 10px; font-size: 13px; color: var(--p7-sub-k); }
.p7-inst__fact b { font-size: 22px; font-weight: 700; color: var(--p7-gold-hi); font-variant-numeric: tabular-nums; }
.p7-inst__arrow { grid-area: arrow; display: grid; place-items: center; width: 44px; height: 44px; border-radius: 999px; border: 1px solid rgba(255,255,255,.14); color: var(--p7-gold-hi); transition: background-color .3s, color .3s, border-color .3s, transform .4s var(--p7-ease); }
.p7-inst a:hover .p7-inst__arrow { background: var(--p7-gold); border-color: var(--p7-gold); color: var(--p7-k); transform: rotate(-45deg); }
.p7-inst__fact .p7-live { display: inline-flex; align-items: center; gap: 8px; font-size: 16px; font-weight: 700; color: var(--p7-gold-hi); }
.p7-live::before { content: ""; width: 8px; height: 8px; border-radius: 99px; background: #3ecf72; box-shadow: 0 0 0 4px rgba(62,207,114,.18); }

/* ============================================================ 3 the case */
.p7-case { display: grid; gap: 48px; }
@media (min-width: 1024px) { .p7-case { grid-template-columns: minmax(0, 1.1fr) minmax(0, .9fr); gap: 72px; align-items: stretch; } }
.p7-earn { padding: 36px 32px 28px; border-radius: 28px; background: #fff; border: 1px solid var(--p7-line); box-shadow: 0 30px 60px -40px rgba(10,9,7,.25); }
.p7-earn figcaption b { display: block; font-size: 20px; font-weight: 700; }
.p7-lakh { display: inline-block; padding: 0 .12em; font-size: 1.6em; line-height: 1.1; letter-spacing: -.03em; color: var(--p7-bronze);
  background: linear-gradient(transparent 58%, rgba(212,175,55,.32) 58%); }
.reveal-ready .p7-earn .p7-lakh { background-size: 0% 100%; background-repeat: no-repeat; transition: background-size 1s var(--p7-ease) .2s; }
.reveal-ready .p7-earn.is-in .p7-lakh { background-size: 100% 100%; }
.p7-earn figcaption small { display: block; margin-top: 4px; font-size: 13px; color: var(--p7-sub); }
.p7-cols { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; align-items: end; height: 300px; margin-top: 32px; padding-bottom: 0; border-bottom: 1px solid var(--p7-line); }
@media (max-width: 480px) { .p7-cols { gap: 8px; height: 260px; } }
.p7-col { display: flex; flex-direction: column; justify-content: flex-end; gap: 10px; height: 100%; text-align: center; }
.p7-col__amt { font-size: 15px; font-weight: 700; font-variant-numeric: tabular-nums; white-space: nowrap; }
@media (max-width: 480px) { .p7-col__amt { font-size: 13px; } }
.p7-col__bar { height: calc(var(--h) * 82%); border-radius: 12px 12px 0 0; background: var(--p7-w2); transform-origin: bottom; }
.p7-col--gp .p7-col__bar { background: var(--p7-metal); box-shadow: 0 -10px 40px -12px rgba(212,175,55,.6); }
.p7-col--gp .p7-col__amt { color: var(--p7-bronze); }
.p7-labels { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin-top: 14px; text-align: center; }
@media (max-width: 480px) { .p7-labels { gap: 8px; } }
.p7-labels li { font-size: 13px; line-height: 1.35; color: var(--p7-sub); }
.p7-labels b { display: block; font-size: 15px; color: var(--p7-ink); }
.p7-labels .is-gp b { color: var(--p7-bronze); }
.reveal-ready .p7-earn .p7-col__bar { transform: scaleY(0); transition: transform 1.4s var(--p7-ease); transition-delay: calc(var(--i) * 150ms + 250ms); }
.reveal-ready .p7-earn .p7-col__amt { opacity: 0; transition: opacity .6s; transition-delay: calc(var(--i) * 150ms + 900ms); }
.reveal-ready .p7-earn.is-in .p7-col__bar { transform: none; }
.reveal-ready .p7-earn.is-in .p7-col__amt { opacity: 1; }
.p7-points { display: grid; align-content: center; }
.p7-points li { display: grid; grid-template-columns: 48px 1fr; gap: 4px 18px; padding: 24px 0; border-top: 1px solid var(--p7-line); }
.p7-points li:last-child { border-bottom: 1px solid var(--p7-line); }
.p7-points i { grid-row: span 2; display: grid; place-items: center; width: 48px; height: 48px; border-radius: 999px; background: var(--p7-k); color: var(--p7-gold); font-size: 22px; }
.p7-points b { font-size: 18px; font-weight: 700; }
.p7-points span { font-size: 15px; line-height: 1.6; color: var(--p7-sub); }

/* =========================================================== 4 the trust */
.p7-sec--flush { padding-top: 0; }
.p7-bento { display: grid; gap: 16px; }
@media (min-width: 900px) { .p7-bento { grid-template-columns: 1.15fr 1fr 1fr; grid-template-rows: auto auto; } .p7-cell--big { grid-row: span 2; } .p7-cell--wide { grid-column: span 2; } }
.p7-cell { position: relative; overflow: hidden; padding: 32px; border-radius: 28px; background: #fff; border: 1px solid var(--p7-line); transition: border-color .4s, transform .5s var(--p7-ease), box-shadow .5s; }
.p7-cell:hover { border-color: rgba(212,175,55,.6); transform: translateY(-4px); box-shadow: 0 30px 60px -36px rgba(138,101,32,.4); }
.p7-cell > i { display: grid; place-items: center; width: 52px; height: 52px; border-radius: 999px; background: var(--p7-k); color: var(--p7-gold); font-size: 24px; }
.p7-cell h3 { margin-top: 24px; font-size: 22px; font-weight: 700; letter-spacing: -.01em; }
.p7-cell p { margin-top: 10px; font-size: 15px; line-height: 1.65; color: var(--p7-sub); max-width: 52ch; }
.p7-cell--big { display: flex; flex-direction: column; min-height: 460px; background: var(--p7-k); border-color: var(--p7-k); color: #fff; }
.p7-cell--big:hover { border-color: rgba(212,175,55,.6); }
.p7-cell--big p { color: var(--p7-sub-k); position: relative; }
.p7-cell--big h3 { position: relative; }
.p7-cell .p7-big { position: relative; margin: 0; max-width: none; font-size: clamp(6rem, 13vw, 10rem); line-height: .85; font-weight: 700; letter-spacing: -.06em; background: var(--p7-metal); -webkit-background-clip: text; background-clip: text; color: transparent; }
.p7-cell__art { position: absolute; right: -24px; top: 150px; width: 220px; height: auto; opacity: .9; pointer-events: none; }
.p7-cell--big .p7-cell__body { margin-top: auto; padding-top: 120px; }
@media (max-width: 899px) { .p7-cell--big { min-height: 0; } .p7-cell--big .p7-cell__body { padding-top: 56px; } .p7-cell__art { width: 150px; right: -24px; top: -16px; } }
.reveal-ready .p7-cell--big .p7-cell__art { transform: translate(30px, -30px) rotate(12deg); transition: transform 1.6s var(--p7-ease) .2s; }
.reveal-ready .p7-cell--big.is-in .p7-cell__art { transform: none; }

/* =========================================================== 5 the proof */
.p7-nums { display: grid; gap: 1px; overflow: hidden; border-radius: 28px; background: rgba(212,175,55,.22); color: #fff; }
@media (min-width: 768px) { .p7-nums { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
.p7-nums li { padding: 40px 36px; background: var(--p7-k); }
.p7-nums b { display: block; font-size: clamp(2.75rem, 5vw, 4rem); line-height: 1; font-weight: 700; letter-spacing: -.04em; background: var(--p7-metal); -webkit-background-clip: text; background-clip: text; color: transparent; font-variant-numeric: tabular-nums; }
.p7-nums b small { font-size: .5em; letter-spacing: -.01em; }
.p7-nums span { display: block; margin-top: 14px; font-size: 15px; line-height: 1.5; color: var(--p7-sub-k); max-width: 26ch; }
.p7-voices { display: grid; gap: 16px; margin-top: 16px; }
@media (min-width: 1024px) { .p7-voices { grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr); } }
.p7-voice { display: flex; flex-direction: column; justify-content: space-between; gap: 24px; padding: 28px; border-radius: 16px; background: #fff; border: 1px solid var(--p7-line); }
.p7-voice--lead { position: relative; padding: 44px 40px; border-radius: 28px; background: var(--p7-w2); border-color: transparent; }
.p7-voice--lead::before { content: "\201C"; position: absolute; top: 4px; right: 32px; font-size: 180px; line-height: 1; font-weight: 700; color: var(--p7-gold); opacity: .35; pointer-events: none; }
.p7-voice.p7-voice--lead blockquote { position: relative; font-size: clamp(1.5rem, 2.6vw, 2.125rem); line-height: 1.3; letter-spacing: -.02em; font-weight: 500; }
.p7-voice blockquote { font-size: 15px; line-height: 1.6; }
.p7-voices__rest { display: grid; gap: 16px; }
@media (min-width: 640px) { .p7-voices__rest { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 639px) {
  .p7-voices__rest { grid-auto-flow: column; grid-auto-columns: 84%; overflow-x: auto; scroll-snap-type: x mandatory; scrollbar-width: none; margin: 0 -20px; padding: 0 20px 4px; scroll-padding: 0 20px; }
  .p7-voices__rest::-webkit-scrollbar { display: none; }
  .p7-voices__rest .p7-voice { scroll-snap-align: start; }
  .p7-voice--lead { padding: 36px 24px; }
  .p7-voice--lead::before { font-size: 120px; right: 16px; opacity: .22; }
}
.p7-voice figcaption { display: flex; align-items: center; gap: 12px; font-size: 15px; }
.p7-voice figcaption > span:first-child { display: grid; place-items: center; width: 40px; height: 40px; border-radius: 999px; background: var(--p7-k); color: var(--p7-gold); font-weight: 700; }
.p7-voice figcaption b { display: block; }
.p7-stars { color: var(--p7-gold); letter-spacing: 2px; font-size: 14px; }

/* ============================================================== 6 the app */
.p7-finale { position: relative; overflow: hidden; isolation: isolate; padding: 128px 0 96px; text-align: center; }
.p7-finale::before { content: ""; position: absolute; inset: 0; z-index: -1; pointer-events: none; background: radial-gradient(45% 50% at 50% 38%, rgba(212,175,55,.2), transparent 72%); }
.p7-finale__icon { width: 112px; height: 112px; margin: 0 auto; border-radius: 26px; box-shadow: 0 30px 60px -20px rgba(212,175,55,.5); }
.p7-finale .p7-h2 { margin: 40px auto 0; max-width: 15ch; }
.p7-finale .p7-lead { margin: 20px auto 0; }
.p7-get { display: grid; justify-items: center; gap: 28px; margin-top: 56px; }
@media (min-width: 768px) { .p7-get { grid-template-columns: auto auto; justify-content: center; align-items: center; gap: 56px; text-align: left; } }
.p7-qr { position: relative; padding: 14px; border-radius: 28px; background: linear-gradient(145deg, rgba(243,220,143,.9), rgba(168,132,31,.9)); box-shadow: 0 40px 80px -30px rgba(212,175,55,.55); }
.p7-qr img { display: block; width: 224px; height: auto; border-radius: 18px; }
@media (min-width: 1024px) { .p7-qr img { width: 260px; } }
.p7-get__text { display: grid; gap: 20px; justify-items: center; max-width: 320px; }
@media (min-width: 768px) { .p7-get__text { justify-items: start; } }
.p7-get__text p { font-size: 16px; line-height: 1.6; color: var(--p7-sub-k); }
.p7-get__text p b { display: block; font-size: 22px; color: #fff; margin-bottom: 4px; }
.p7-play { display: inline-flex; align-items: center; gap: 12px; min-height: 60px; padding: 0 26px 0 20px; border-radius: 999px; background: #fff; color: var(--p7-k); transition: background-color .3s, transform .3s var(--p7-ease); }
.p7-play:hover { background: var(--p7-gold-hi); }
.p7-play:active { transform: scale(.98); }
.p7-play i { font-size: 28px; }
.p7-play span { display: grid; text-align: left; font-size: 12px; line-height: 1.2; }
.p7-play b { font-size: 18px; }
.reveal-ready .p7-qr[data-reveal] { transform: translateY(32px) scale(.94); }
.reveal-ready .p7-qr[data-reveal].is-in { transform: none; transition: opacity .8s, transform 1.2s var(--p7-ease); }
.p7-risk { margin: 96px auto 0; max-width: 820px; font-size: 13px; line-height: 1.65; color: rgba(255,255,255,.5); }
</style>"""

MAIN = r"""<main id="main-content">

  <!-- COPY: headlines and descriptions are home-premium2's and home-premium3's,
       written for those concepts, not captured from the live site. Rates,
       issuers, stats, reviews and the risk line come from index.html's dated
       snapshot. -->

  <!-- ======================================================== 1 the deal -->
  <section class="p7-hero p7-dark" aria-labelledby="p7-title">
    <img class="p7-hero__pi" src="@IMG@pi.svg" alt="" width="331" height="298">
    <div class="p7-shell">
      <ul class="p7-trust p7-rise" style="--d:0" role="list">
        <li><i class="ph-fill ph-seal-check" aria-hidden="true"></i>SEBI registered Debt Broker</li>
        <li><i class="ph-fill ph-seal-check" aria-hidden="true"></i>OBPP license holder</li>
        <li><i class="ph-fill ph-seal-check" aria-hidden="true"></i>Fixed returns up to 13.8%</li>
      </ul>
      <h1 class="p7-h1 p7-rise" style="--d:1" id="p7-title"><span>The golden</span> <em>experience of investing.</em></h1>
      <div class="p7-hero__cta p7-rise" style="--d:2">
        <a class="p7-btn p7-btn--gold" href="signup.html">Start investing @ARROW@</a>
        <a class="p7-btn p7-btn--ghost" href="corporate-bonds.html">Explore bonds</a>
      </div>

      <!-- DATA: top 3 Bond Utsav deals, index.html snapshot 2026-09-25. -->
      <div class="p7-sheet" role="region" aria-label="Top bonds">
        <span class="p7-sheet__rule" aria-hidden="true"></span>
        <div class="p7-sheet__list" role="list">@DEALS@</div>
      </div>
    </div>
  </section>

  <!-- ===================================================== 2 the account -->
  <section class="p7-sec p7-sec--tight p7-dark" aria-labelledby="p7-assets">
    <div class="p7-shell">
      <div class="p7-head" data-reveal>
        <h2 class="p7-h2" id="p7-assets">Three instruments. <em>One golden account.</em></h2>
      </div>
      <ul class="p7-inst" role="list">
        <li data-reveal><a href="corporate-bonds.html"><i class="ph ph-certificate" aria-hidden="true"></i><h3>Corporate Bonds</h3><span class="p7-inst__fact"><b>13.8%</b>Returns, up to</span><span class="p7-inst__arrow">@ARROW@</span></a></li>
        <li data-reveal style="transition-delay:.1s"><a href="fixed-deposits.html"><i class="ph ph-vault" aria-hidden="true"></i><h3>Fixed Deposits</h3><span class="p7-inst__fact"><b>8.5%</b>Highest returns</span><span class="p7-inst__arrow">@ARROW@</span></a></li>
        <li data-reveal style="transition-delay:.2s"><a href="bond-ipo-online.html"><i class="ph ph-rocket-launch" aria-hidden="true"></i><h3>NCD IPOs</h3><span class="p7-inst__fact"><b class="p7-live">Live now</b>See open IPOs</span><span class="p7-inst__arrow">@ARROW@</span></a></li>
      </ul>
    </div>
  </section>

  <div class="p7-act2">
  <!-- ======================================================== 3 the case -->
  <section class="p7-sec" aria-labelledby="p7-whybonds">
    <div class="p7-shell">
      <div class="p7-head" data-reveal>
        <h2 class="p7-h2" id="p7-whybonds">Why bonds belong in your <em>portfolio.</em></h2>
        <p class="p7-lead">Bonds sit between the safety of a deposit and the growth of equity. You know what you will earn, and when, on the day you invest.</p>
      </div>
      <div class="p7-case">
        <!-- DATA: savings and bank FD rows are indicative market rates, not GoldenPi
             listings; the two gold rows are the snapshot highs from index.html.
             Amounts are each rate applied to Rs 1,00,000 for a year. -->
        <figure class="p7-earn" data-reveal>
          <figcaption><b>What <span class="p7-lakh">&#8377;1 lakh</span> can earn in a year</b><small>Indicative annual rates, before tax</small></figcaption>
          <div class="p7-cols" aria-hidden="true">@COLS@</div>
          <ul class="p7-labels" role="list">@LABELS@</ul>
        </figure>
        <ul class="p7-points" data-reveal role="list">
          <li><i class="ph ph-calendar-check" aria-hidden="true"></i><b>Predictable income</b><span>Interest lands on fixed dates, monthly to yearly.</span></li>
          <li><i class="ph ph-trend-up" aria-hidden="true"></i><b>Higher than FDs</b><span>Rated corporate debt typically pays a premium over bank deposits.</span></li>
          <li><i class="ph ph-waves" aria-hidden="true"></i><b>Steadier than stocks</b><span>Returns are set at purchase, not by daily market moods.</span></li>
          <li><i class="ph ph-chart-pie-slice" aria-hidden="true"></i><b>Real diversification</b><span>Spread across issuers, ratings and maturities.</span></li>
        </ul>
      </div>
    </div>
  </section>

  <!-- ======================================================= 4 the trust -->
  <section class="p7-sec p7-sec--flush" aria-labelledby="p7-whygp">
    <div class="p7-shell">
      <div class="p7-head" data-reveal><h2 class="p7-h2" id="p7-whygp">Why investors choose <em>GoldenPi.</em></h2></div>
      <div class="p7-bento">
        <article class="p7-cell p7-cell--big" data-reveal>
          <img class="p7-cell__art" src="@IMG@premium5/why-lock.png" alt="" width="760" height="633" loading="lazy" decoding="async">
          <p class="p7-big">5%</p>
          <div class="p7-cell__body">
            <h3>Only 5% of bonds make the cut.</h3>
            <p>No matter if you chase great returns with corporate bonds or park your money in government-backed bonds, the due diligence has already been handled.</p>
          </div>
        </article>
        <article class="p7-cell" data-reveal style="transition-delay:.1s"><i class="ph ph-hand-coins" aria-hidden="true"></i><h3>Zero brokerage</h3><p>No hidden charges, so the return you see is the return you get.</p></article>
        <article class="p7-cell" data-reveal style="transition-delay:.2s"><i class="ph ph-shield-check" aria-hidden="true"></i><h3>One of the first OBPPs</h3><p>Infrastructure built by people who've spent two decades earning Indian investors' trust.</p></article>
        <article class="p7-cell p7-cell--wide" data-reveal style="transition-delay:.3s"><i class="ph ph-globe-hemisphere-east" aria-hidden="true"></i><h3>Investing options for NRIs</h3><p>Select bonds are open to NRI investors, a direct, digital way into India's fixed-income market without tiring stacks of paperwork.</p></article>
      </div>
    </div>
  </section>

  <!-- ======================================================= 5 the proof -->
  <section class="p7-sec p7-sec--flush" aria-labelledby="p7-reviews">
    <div class="p7-shell">
      <div class="p7-head" data-reveal><h2 class="p7-h2" id="p7-reviews">Happy users</h2></div>
      <!-- DATA: platform milestones, same figures as index.html. -->
      <ul class="p7-nums" data-reveal role="list">
        <li><b data-count>18 <small>Lac+</small></b><span>registered users &amp; growing</span></li>
        <li><b data-count>&#8377;6300 <small>Cr+</small></b><span>total transaction through our platform</span></li>
        <li><b data-count>&#8377;3000 <small>Cr+</small></b><span>worth of bonds available on the platform everyday</span></li>
      </ul>
      <!-- DATA: reviews, same set as index.html. -->
      <div class="p7-voices">@LEAD@<div class="p7-voices__rest" role="region" aria-label="More reviews" tabindex="0">@REST@</div></div>
    </div>
  </section>
  </div>

  <!-- ========================================================= 6 the app -->
  <section class="p7-finale p7-dark" aria-labelledby="p7-get">
    <div class="p7-shell">
      <img class="p7-finale__icon" data-reveal src="@IMG@play/app-icon.png" alt="GoldenPi app icon" width="180" height="180" loading="lazy">
      <h2 class="p7-h2" data-reveal id="p7-get">Your <em>Golden Experience</em> is one tap away.</h2>
      <p class="p7-lead" data-reveal>Build a monthly income stream, protect capital ahead of a goal, or stop watching your money lose ground to inflation.</p>
      <div class="p7-get">
        <div class="p7-qr" data-reveal><img src="@IMG@mobile-app-qr.svg" alt="QR code to download the GoldenPi app" width="153" height="189" loading="lazy"></div>
        <div class="p7-get__text" data-reveal style="transition-delay:.15s">
          <p><b>Download App</b>Scan to download GoldenPi app and get voucher</p>
          <a class="p7-play" href="https://play.google.com/store/apps/details?id=com.goldenpi.gpimobileapp"><i class="ph-fill ph-google-play-logo" aria-hidden="true"></i><span>Get it on<b>Google Play</b></span></a>
        </div>
      </div>
      <p class="p7-risk">Risk Disclosure: Fixed returns do not constitute guaranteed or assured returns. Investments in corporate debt, municipal debt, and securitized instruments are subject to credit, market, and default risks, including delays or defaults in payments. Read all offer documents carefully.</p>
    </div>
  </section>

</main>"""


def deal(i, d):
    name, logo, rate, rating, payout, maturity, url = d
    return f"""
          <article class="p7-deal" role="listitem" style="--i:{i}">
            <div class="p7-deal__top"><span class="p7-chip"><img src="{IMG}{logo}" alt="" width="40" height="40"></span><div><h3>{name}</h3><span class="p7-deal__tag">Bond Utsav deal</span></div></div>
            <p class="p7-deal__rate"><b>{rate}</b><span>%</span></p>
            <p class="p7-deal__label">Returns</p>
            <dl><div><dt>Rating</dt><dd>{rating}</dd></div><div><dt>Payout</dt><dd>{payout}</dd></div><div><dt>Maturity</dt><dd>{maturity}</dd></div></dl>
            <a class="p7-link p7-deal__go" href="{url}" aria-label="Know more about {name}">Know more {ARROW}</a>
          </article>"""


def col(i, e):
    label, rate, gp = e
    top = max(r for _, r, _ in EARN)
    amt = f"&#8377;{round(rate * 1000):,}"
    return (f'<div class="p7-col{" p7-col--gp" if gp else ""}" style="--i:{i}">'
            f'<span class="p7-col__amt">{amt}</span><span class="p7-col__bar" style="--h:{rate / top:.3f}"></span></div>')


def label(e):
    name, rate, gp = e
    cls = ' class="is-gp"' if gp else ""
    return f'<li{cls}><b>{rate}%</b>{name}<span class="sr-only">, &#8377;{round(rate * 1000):,} a year</span></li>'


def voice(r, lead=False):
    name, text = r
    cls = "p7-voice p7-voice--lead" if lead else "p7-voice"
    return (f'<figure class="{cls}" data-reveal><div>{STARS if not lead else ""}<blockquote>&ldquo;{text}&rdquo;</blockquote></div>'
            f'<figcaption><span aria-hidden="true">{name[0]}</span><span><b>{name}</b>{STARS if lead else ""}</span></figcaption></figure>')


def main():
    assert round(13.8 * 1000) == 13800 and f"{round(2.7 * 1000):,}" == "2,700"
    page = open(SRC, encoding="utf-8").read()
    page, n1 = re.subn(r"<style>\n/\* home-premium: page-only styles.*?</style>", lambda m: STYLE, page, count=1, flags=re.S)
    page, n2 = re.subn(r'<body class="h3-page">', '<body class="p7-page p7">', page, count=1)
    main_html = (MAIN.replace("@DEALS@", "".join(deal(i, d) for i, d in enumerate(DEALS)))
                 .replace("@COLS@", "".join(col(i, e) for i, e in enumerate(EARN)))
                 .replace("@LABELS@", "".join(label(e) for e in EARN))
                 .replace("@LEAD@", voice(REVIEWS[0], lead=True))
                 .replace("@REST@", "".join(voice(r) for r in REVIEWS[1:]))
                 .replace("@ARROW@", ARROW).replace("@IMG@", IMG))
    page, n3 = re.subn(r'<main id="main-content">.*?</main>', lambda m: main_html, page, count=1, flags=re.S)
    page, n4 = re.subn(r"<title>.*?</title>", "<title>GoldenPi | The Golden Experience of Investing</title>", page, count=1)
    if (n1, n2, n3, n4) != (1, 1, 1, 1) or "@" in main_html:
        raise SystemExit("home-premium3.html changed shape (%d %d %d %d), or a placeholder was left" % (n1, n2, n3, n4))
    open(OUT, "w", encoding="utf-8").write(page)
    print("home-premium7.html")


if __name__ == "__main__":
    main()
