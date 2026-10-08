#!/usr/bin/env python3
"""user-fixed-deposits-app.html: the logged-in Fixed Deposits page in the
user-explore-app design (Figma HRSMFFccdLgqf1YwD7oyc9 40:2105, light version).

Same build as user-explore-app: the first block in black and gold, everything
after it light, bond-details3's navbar (FD marked current) and footer, and the
account rail. Content is user-fixed-deposits.html's (production capture of
2026-09-26): greeting, FD options, calculator, steps, bond collections,
explainer, blog, trust figures and FAQ. Its "No Closing Bell" bond banner is
left out: the dark first block takes its place. The calculator is live, with the
quarterly compounding the capture's figures come from (8.25% over 60 months on
2,00,000 gives 3,00,852.79).

    python3 pages/_bond_beta.py && python3 pages/_fd_app.py
"""
import os

import _explore_app as X

OUT = os.path.join(X.HERE, "user-fixed-deposits-app.html")
IMG = "../assets/img/"
LIVE_FD = "https://goldenpi.com/fixed-deposits"

# DATA: bank FDs, goldenpi.com 2026-09-26 (as user-fixed-deposits.html).
BANK_FDS = [("GPID105192.Unity.png", "Unity Small Finance Bank", "8.5%", "Insured upto ₹5L", "7 D - 60 M"),
            ("GPID105191.Suryoday.png", "Suryoday Small Finance Bank", "8.5%", "Insured upto ₹5L", "7 D - 60 M"),
            ("GPID106947.utkarsh_logo.png", "Utkarsh Small Finance Bank", "8.25%", "CRISIL AAA", "7 D - 60 M")]

COLLECTIONS = [
    ("GPIDO09029.newly_added_bonds.png", "Newly Launched Bonds: Latest Bond Opportunities", "",
     "https://goldenpi.com/collections/newly-launched-bonds"),
    ("highly-rated-bonds.svg", "Highly Rated Bonds (A or Above)",
     "A collection of bonds which are rated 'A' or above by credit rating agencies such as CRISIL, ICRA, etc.",
     "https://goldenpi.com/collections/highly-rated-bonds"),
    ("high-yield-bonds.svg", "High Yield Bonds: Earn Higher Returns 14%*",
     "A collection of bonds where yield is more than 11%.", "https://goldenpi.com/collections/high-yield-bonds"),
    ("bonds-to-earn-monthly-fixed-income.svg", "Bonds to Earn Monthly Fixed Income",
     "A collection of bonds which provide fixed interest payout every month.",
     "https://goldenpi.com/collections/bonds-to-earn-monthly-fixed-income"),
    ("bonds-at-discounted-price.svg", "Bonds at Discounted Price",
     "A collection of bonds where current market price is less than the face value.",
     "https://goldenpi.com/collections/bonds-at-discounted-price"),
]

PLANS = [("GPID105191.Suryoday.png", "Suryoday Small Finance Bank", "8.25%"),
         ("GPID100016.Shriram-Squircle.png", "Shriram Finance", "7.5%")]

BLOG = [("30-Lakh-Fixed-Deposit-Interest-Per-Month.jpg",
         "30 Lakhs Fixed Deposit Interest Per Month: How Much Will You Earn in 2026", "July 24, 2026"),
        ("1-Lakh-Fixed-Deposit-Monthly-Interest-Rate.jpg",
         "₹1 Lakh Fixed Deposit Monthly Interest: Best FDs for Regular Income", "July 23, 2026"),
        ("Bond-vs-Fixed-Deposits.jpg",
         "Bonds vs Fixed Deposits 2026: Tax and Liquidity Comparison for Indian Investors", "July 19, 2026")]

STATS = [("₹3000 Cr+", "worth of bonds available on the platform everyday"),
         ("18 Lac+", "registered users &amp; growing"),
         ("₹6300 Cr+", "total transaction through our platform"),
         ("500+ Bonds", "explore from variety of bonds")]

PARTNERS = [("centrum.png", "Centrum"), ("AxisSecurities.png", "Axis Securities"),
            ("AnandRathi.webp", "Anand Rathi"), ("Sakthi-Finance-logo.png", "Sakthi Finance")]

FAQ = [
    ("What is GoldenPi?",
     ["As a SEBI-registered debt broker &amp; OBPP (Online Bond Providing Platform), trust and transparency are at the heart of what we do. With a family of over 900k+ registered users, GoldenPi is one of the intuitive online platforms that lets anyone explore and invest in fixed income securities such as bonds and debentures, NCD IPOs and Corporate Fixed Deposits etc. with just a few clicks. Our goal is to bring fixed returns to your portfolio, with options that cater to diverse financial goals and preferences.We believe in simplification of complexities, hence the investment process on our platform is super user-friendly, making it easier for you to select the right products that align with your financial goals. Whether it's the stability of government bonds or the attractive yields of corporate NCDs, GoldenPi caters to a wide spectrum of investment needs, ensuring that every investor can find a product that suits their risk appetite and return expectations."]),
    ("What are the unique features of GoldenPi? Why should I consider buying Bonds from GoldenPi?",
     ["GoldenPi has the most extensive collection of bonds and debentures on its platform. So customers get access to most of the bonds available in the Bond market at any given time.",
      "Most of the large Bond Institutions in India are enlisted on our site as our suppliers with us. This enables our system to zero in on the best price(lowest) for a Bond in the secondary market. Well, most of the time!",
      "GoldenPi takes care of the entire bond investment process starting from KYC processing until bond units get transferred to the customer's Demat account."]),
    ("Why should I invest in Bonds and Debentures?",
     ["Potentially higher returns – Depending on the issuer and credit rating, some bonds may offer better coupon rates than traditional Fixed Deposits.",
      "Tradability and liquidity – Listed bonds can be bought and sold on stock exchanges, which may provide greater liquidity compared to FDs, which are generally locked in until maturity.",
      "Tax benefits on specific bonds – Certain notified bonds, such as those under Section 54EC (e.g., NHAI, REC, PFC, IRFC), allow exemption from capital gains tax under specific conditions."]),
    ("How do I start investing in fixed income securities on GoldenPi?",
     ["Select the bond and specify the number of units you want to purchase.",
      "Make the payment online using Razorpay via net banking or UPI.",
      "Payment is made on T-day (Transaction Day).",
      "The bond is credited to your Demat account on T+1 (the next business day)."]),
]


def hero():
    logo, name, rate, secured, tenure = BANK_FDS[0]
    return """<section class="xa-hero" aria-labelledby="xa-title">
  <span class="xa-hero__rays" aria-hidden="true"><img src="{x}hero-rays.jpg" alt=""></span>
  <!-- DATA: first name of the logged-in account. -->
  <h1 class="xa-hero__title xa-in" id="xa-title">Hi <span class="xa-gold">INVESTOR</span>, Explore Fixed Deposit</h1>
  <p class="xa-hero__sub xa-in" style="--d:1">Invest in RBI-regulated small banks and NBFCs with Annual returns up to <span class="xa-gold">8.5%</span></p>
  <!-- DATA: the highest-return bank FD (goldenpi.com 2026-09-26). -->
  <article class="xa-launch xa-in" style="--d:2">
    <span class="xa-launch__streak xa-launch__streak--a" aria-hidden="true"><img src="{x}hero-glow.jpg" alt=""></span>
    <span class="xa-launch__streak xa-launch__streak--b" aria-hidden="true"><img src="{x}hero-glow.jpg" alt=""></span>
    <div class="xa-launch__body">
      <p class="xa-launch__eyebrow">Bank FD</p>
      <h2 class="xa-launch__name"><img class="fa-logo" src="{i}{logo}" alt="" width="36" height="36">{name}</h2>
      <dl class="xa-launch__facts"><div><dt>Secured</dt><dd>{secured}</dd></div><div><dt>Tenure</dt><dd>{tenure}</dd></div></dl>
    </div>
    <div class="xa-launch__side">
      <p class="fa-launch__label">Highest Returns</p>
      <p class="xa-launch__rate"><span data-count="{num}">{num}</span><small>%</small></p>
      <a class="xa-launch__cta" href="#fa-opts">Explore</a>
    </div>
  </article>
</section>""".format(x=X.IMG, i=IMG, logo=logo, name=name, secured=secured, tenure=tenure,
                     num=rate.rstrip("%"))


def fd_options():
    rows = "".join("""<li style="--i:{k}" class="fa-fd">
  <img src="{i}{logo}" alt="" width="40" height="40">
  <h3 class="fa-fd__name">{name}</h3>
  <dl class="fa-fd__facts"><div><dt>Highest Returns</dt><dd class="fa-fd__rate">{rate}</dd></div><div><dt>Secured</dt><dd><span class="fa-tag">{secured}</span></dd></div><div><dt>Tenure</dt><dd>{tenure}</dd></div></dl>
</li>""".format(k=k, i=IMG, logo=l, name=n, rate=r, secured=s, tenure=t) for k, (l, n, r, s, t) in enumerate(BANK_FDS))
    tabs = [("bank", "bank-fd.svg", "Bank FD"), ("tax", "tax-saving-fd.svg", "Tax Saving FD"), ("nbfc", "nbfc-fd.svg", "NBFC FD")]
    tablist = "".join('<button type="button" role="tab" id="fa-tab-%s" aria-controls="fa-panel-%s" aria-selected="%s"%s>'
                      '<img src="%s%s" alt="" width="24" height="24">%s</button>'
                      % (k, k, "true" if n == 0 else "false", "" if n == 0 else ' tabindex="-1"', IMG, f, t)
                      for n, (k, f, t) in enumerate(tabs))
    notes = "".join('<li><img src="%scheck_circle.svg" alt="" width="16" height="16">%s</li>' % (IMG, t)
                    for t in ("DICGC insurance up to ₹5 lakh", "Monthly and quarterly payouts available"))
    empty = lambda k, what: (
        '<div class="fa-panel fa-empty" role="tabpanel" id="fa-panel-%s" aria-labelledby="fa-tab-%s" hidden>'
        '<p>%s FDs were not captured: the live page renders only the selected tab.</p>'
        '<a class="xa-view" href="%s"><span>See the live fixed deposit list</span>%s</a></div>'
        % (k, k, what, LIVE_FD, X.ic("arrow.svg")))
    return ('<section class="fa-opts" id="fa-opts" data-reveal aria-labelledby="fa-opts-t">%s'
            '<div class="fa-tabs" role="tablist" aria-label="Fixed deposit type">%s</div>'
            '<div class="fa-panel" role="tabpanel" id="fa-panel-bank" aria-labelledby="fa-tab-bank">'
            '<ul class="fa-notes">%s</ul>'
            '<!-- DATA: bank FDs, goldenpi.com 2026-09-26. -->\n<ul class="fa-fds">%s</ul></div>%s%s</section>'
            % (X.head('<span id="fa-opts-t">Available Fixed Deposit Options</span>', "Highest returns up to 8.5% pa",
                      X.arrow_btn("View", LIVE_FD, "all fixed deposits")),
               tablist, notes, rows, empty("tax", "Tax saving"), empty("nbfc", "NBFC")))


def calculator():
    chips = "".join("<li>%s</li>" % t for t in ("Senior citizen", "Female", "Tax Saver", "Bank FD", "NBFC"))
    plans = "".join("""<li class="fa-plan" style="--i:{k}"><img src="{i}{logo}" alt="" width="40" height="40"><h3>{name}</h3>
  <button type="button" class="xa-gold-btn xa-gold-btn--sm">Invest</button>
  <dl><div><dt>Returns</dt><dd class="fa-gain">{rate}</dd></div><div><dt>Tenure</dt><dd>60 Months</dd></div><div><dt>Payout</dt><dd>Cumulative</dd></div></dl></li>""".format(k=k, i=IMG, logo=l, name=n, rate=r)
                    for k, (l, n, r) in enumerate(PLANS))
    return """<section class="fa-calc" id="fd-calculator" data-reveal aria-labelledby="fa-calc-t">
{head}
<!-- DATA: the calculator's defaults and plans as captured. Rate is the best plan's (8.25%);
     the profile chips are shown, not wired: production applies them server side. -->
<div class="fa-calc__card">
  <ul class="fa-chips" aria-label="Investor profile">{chips}</ul>
  <div class="fa-calc__grid">
    <div class="fa-calc__inputs">
      <div class="fa-field"><div class="fa-field__top"><label for="fa-amount">Investment Amount</label><output id="fa-amount-out" for="fa-amount">₹ 2,00,000</output></div>
        <input id="fa-amount" type="range" min="10000" max="10000000" step="10000" value="200000" style="--p:1.9%"><div class="fa-field__scale"><span>₹10,000</span><span>₹1 Cr</span></div></div>
      <div class="fa-field"><div class="fa-field__top"><label for="fa-tenure">Tenure (Months)</label><output id="fa-tenure-out" for="fa-tenure">60</output></div>
        <input id="fa-tenure" type="range" min="6" max="60" step="6" value="60" style="--p:100%"><div class="fa-field__scale"><span>6</span><span>60</span></div></div>
      <div class="fa-field fa-field--row"><label for="fa-payout">Payout Mode</label>
        <select id="fa-payout"><option value="cumulative">On maturity</option><option value="periodic">Interest</option></select>
        <span class="fa-rate">Interest Rate <b class="fa-gain">8.25%</b></span></div>
    </div>
    <dl class="fa-calc__out" aria-live="polite">
      <div><dt>Invested Amount</dt><dd id="fa-invested">₹ 2,00,000</dd></div>
      <div><dt>FD Gains</dt><dd id="fa-gains" class="fa-gain">₹ 1,00,852.79</dd></div>
      <div class="fa-calc__total"><dt>Maturity Amount</dt><dd id="fa-maturity">₹ 3,00,852.79</dd></div>
    </dl>
  </div>
  <p class="fa-calc__plans-t">Here are the best FD plans for you!</p>
  <ul class="fa-plans">{plans}</ul>
</div>
</section>""".format(head=X.head('<span id="fa-calc-t">Let\'s find the best FD offerings for your needs!</span>', "", ""),
                     chips=chips, plans=plans)


def steps():
    items = [("ipo-2.png", "Choose the desired FD"), ("ipo-1.png", "Share Required Details"),
             ("ipo-3.png", "Make payment to Invest")]
    lis = "".join('<li style="--i:%d"><span class="fa-steps__ic"><img src="%s%s" alt="" width="40" height="40"></span>'
                  '<span class="fa-steps__num">0%d</span><p>%s</p></li>' % (k, IMG, f, k + 1, t) for k, (f, t) in enumerate(items))
    return ('<section class="fa-steps" data-reveal aria-labelledby="fa-steps-t">%s<ol>%s</ol></section>'
            % (X.head('<span id="fa-steps-t">How to invest in a FD?</span>', "", ""), lis))


def collections():
    tiles = "".join('<li style="--i:%d"><a class="fa-col%s" href="%s"><img src="%s%s" alt="" width="40" height="40">'
                    '<span><strong>%s</strong>%s</span></a></li>'
                    % (k, " fa-col--wide" if k == 0 else "", h, IMG, f, t, "<em>%s</em>" % d if d else "")
                    for k, (f, t, d, h) in enumerate(COLLECTIONS))
    return ('<section class="fa-cols" data-reveal aria-labelledby="fa-cols-t">%s<ul class="fa-cols__grid">%s</ul></section>'
            % (X.head('<span id="fa-cols-t">Our Bond Collections</span>', "",
                      X.arrow_btn("View all", "collections-all-bonds.html", "bond collections")), tiles))


def explainer():
    chips = "".join("<li>%s</li>" % t for t in ("FD", "NBFC", "Payout", "Cumulative Payout"))
    return """<section class="fa-what" data-reveal aria-labelledby="fa-what-t">
  <div class="fa-what__card">
    <div>
      <h2 class="xa-head__title" id="fa-what-t">What is a Fixed Deposit Investment?</h2>
      <p class="fa-what__body">FDs (Fixed Deposits) are investment options from banks, NBFCs, and corporates in India. You can choose to receive a lump sum money at maturity or get regular interest payouts (monthly, quarterly, or yearly). Senior citizens often get better rates. Through GoldenPi you can now invest in these FDs through a seamless online journey without opening a new bank account.</p>
      <div class="fa-what__means"><span>What it means?</span><ul>{chips}</ul></div>
    </div>
    <img class="fa-what__art" src="{i}post-login-cfd-home.svg" alt="" width="200" height="200">
  </div>
  <div class="fa-band"><img src="{i}calc.svg" alt="" width="56" height="40"><p>Calculate Your FD Returns Here</p>
    <a class="xa-gold-btn xa-gold-btn--sm" href="#fd-calculator">Calculate Now</a></div>
</section>""".format(i=IMG, chips=chips)


def blog():
    cards = "".join('<li style="--i:%d"><a class="fa-post" href="https://goldenpi.com/blog">'
                    '<span class="fa-post__media"><img src="%s%s" alt="" width="1600" height="900" loading="lazy"></span>'
                    '<span class="fa-post__body"><strong>%s</strong><time>%s</time><span class="fa-post__more">Read more%s</span></span></a></li>'
                    % (k, IMG, f, t, d, X.ic("arrow.svg")) for k, (f, t, d) in enumerate(BLOG))
    return ('<!-- DATA: blog feed, goldenpi.com 2026-09-26. The live cards have no link in the markup, so these point at /blog. -->\n'
            '<section class="fa-blog" data-reveal aria-labelledby="fa-blog-t">%s<ul class="fa-blog__row">%s</ul></section>'
            % (X.head('<span id="fa-blog-t">Your guide to invest smartly</span>', "",
                      X.arrow_btn("View", "https://goldenpi.com/blog", "all articles")), cards))


def trusted():
    stats = "".join('<li style="--i:%d"><strong>%s</strong><span>%s</span></li>' % (k, v, l) for k, (v, l) in enumerate(STATS))
    logos = "".join('<li><img src="%s%s" alt="%s" height="32"></li>' % (IMG, f, a) for f, a in PARTNERS)
    return ('<section class="fa-trust" data-reveal aria-labelledby="fa-trust-t">'
            '<h2 class="xa-rule" id="fa-trust-t">Trusted by 18 Lac+ users and Market Leaders</h2>'
            '<ul class="fa-trust__stats">%s</ul><ul class="fa-trust__logos" aria-label="Market leaders we work with">%s</ul></section>'
            % (stats, logos))


def faq():
    items = "".join('<details class="fa-q"%s><summary>%s<span class="fa-q__ic" aria-hidden="true"></span></summary>'
                    '<div class="fa-q__a">%s</div></details>'
                    % (" open" if k == 0 else "", q, "".join("<p>%s</p>" % p for p in a)) for k, (q, a) in enumerate(FAQ))
    return """<section class="fa-faq" data-reveal aria-labelledby="fa-faq-t">
{head}
<div class="fa-faq__grid">
  <div class="fa-faq__list">{items}</div>
  <aside class="fa-help">
    <img class="fa-help__art" src="{i}support-icon.svg" alt="" width="120" height="120">
    <p class="fa-help__t"><img src="{i}phone-icon.svg" alt="" width="20" height="20">Need Help</p>
    <p class="fa-help__d">Talk to our Support Team for free. We will help you through your investment journey.</p>
    <a class="xa-gold-btn" href="https://goldenpi.com/contact-us">Contact Us</a>
  </aside>
</div>
</section>""".format(head=X.head('<span id="fa-faq-t">Frequently Asked Questions</span>', "", ""), items=items, i=IMG)


def body():
    main = fd_options() + calculator() + steps() + collections() + explainer() + blog() + trusted() + faq()
    return ('<main id="main-content" class="xa-page"><div class="xa"><div class="xa-hero-wrap">%s</div>%s'
            '<div class="xa-main">%s</div></div></main>' % (hero(), X.rail(), main))


STYLE = """<style>
/* user-fixed-deposits-app: the FD page's own blocks, on user-explore-app's tokens (.xa-page). */
.xa-launch__name:has(.fa-logo) { display: flex; align-items: center; gap: 12px; }
.fa-logo { display: block; flex: none; width: 36px; height: 36px; border-radius: 50%; background: #fff; padding: 3px;
  box-shadow: 0 0 0 1px rgba(40, 32, 8, .15); }
.fa-launch__label { font-size: 10px; line-height: 12px; font-weight: 700; letter-spacing: .8px; text-transform: uppercase; margin-bottom: -10px; }
.xa-head__sub:empty { display: none; }
.xa-head__end:empty { display: none; }

/* FD options: segmented tabs + list */
.fa-tabs { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 4px; padding: 4px; border-radius: 16px;
  background: #efe9dc; border: 1px solid var(--line); }
.fa-tabs button { display: flex; align-items: center; justify-content: center; gap: 8px; height: 48px; border: 0; border-radius: 12px; cursor: pointer;
  font: inherit; font-size: 14px; font-weight: 700; color: var(--sub); background: transparent;
  transition: background-color .3s var(--ease), color .3s var(--ease), box-shadow .3s var(--ease); }
.fa-tabs button img { width: 22px; height: 22px; filter: grayscale(1) opacity(.55); transition: filter .3s var(--ease); }
.fa-tabs button:hover { color: var(--ink); }
.fa-tabs button[aria-selected="true"] { color: var(--ink); background: var(--card); box-shadow: 0 1px 2px rgba(80, 60, 10, .08), 0 8px 18px -12px rgba(80, 60, 10, .35); }
.fa-tabs button[aria-selected="true"] img { filter: none; }
.fa-panel { margin-top: 16px; }
.fa-panel[hidden] { display: none; }
.fa-notes { display: flex; flex-wrap: wrap; gap: 8px 24px; margin-bottom: 14px; }
.fa-notes li { display: flex; align-items: center; gap: 6px; font-size: 13px; font-weight: 500; color: var(--ink); }
.fa-fds { display: grid; gap: 12px; }
.fa-fd { display: grid; grid-template-columns: 40px minmax(0, 1fr) auto; align-items: center; gap: 16px; padding: 16px 20px; border-radius: 20px;
  background: var(--card); border: 1px solid var(--line); box-shadow: var(--shadow); transition: transform .35s var(--ease), border-color .35s var(--ease); }
.fa-fd:hover { transform: translateY(-2px); border-color: rgba(212, 175, 55, .55); }
.fa-fd > img { width: 40px; height: 40px; border-radius: 50%; object-fit: contain; }
.fa-fd__name { font-size: 15px; line-height: 1.3; font-weight: 700; color: var(--ink); }
.fa-fd__facts { display: grid; grid-template-columns: 110px 140px 90px; gap: 16px; align-items: start; }
.fa-fd__facts dd { min-height: 26px; display: flex; align-items: center; }
.fa-fd__facts dt, .fa-plan dt, .fa-calc__out dt { font-size: 10px; line-height: 12px; font-weight: 700; letter-spacing: .8px; text-transform: uppercase; color: var(--sub); }
.fa-fd__facts dd { margin-top: 4px; font-size: 14px; font-weight: 700; color: var(--ink); }
.fa-fd__rate, .fa-gain { color: #06963c; }
.fa-fd__facts .fa-fd__rate { color: #06963c; font-size: 22px; line-height: 1.1; font-weight: 700; letter-spacing: -.5px; }
.fa-tag { display: inline-block; padding: 3px 10px; border-radius: 999px; font-size: 11px; font-weight: 700; color: var(--ink); background: var(--cream);
  border: 1px solid rgba(212, 175, 55, .3); white-space: nowrap; }
.fa-empty { display: grid; justify-items: start; gap: 14px; padding: 28px; border-radius: 20px; background: var(--card); border: 1px dashed rgba(138, 101, 32, .35); }
.fa-empty p { font-size: 14px; color: var(--sub); max-width: 52ch; }

/* Calculator */
.fa-calc__card { padding: 24px; border-radius: 24px; background: var(--card); border: 1px solid var(--line); box-shadow: var(--shadow); }
.fa-chips, .fa-what__means ul { display: flex; flex-wrap: wrap; gap: 8px; }
.fa-chips li, .fa-what__means li { padding: 6px 12px; border-radius: 999px; font-size: 13px; font-weight: 500; color: var(--ink); background: var(--page); border: 1px solid var(--line); }
.fa-calc__grid { margin-top: 22px; display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(0, .85fr); gap: 28px; align-items: stretch; }
.fa-calc__inputs { display: grid; gap: 22px; align-content: start; }
.fa-field__top { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
.fa-field label { font-size: 14px; font-weight: 700; color: var(--ink); }
.fa-field output { padding: 6px 12px; border-radius: 10px; font-size: 15px; font-weight: 700; color: var(--ink); background: var(--page);
  border: 1px solid var(--line); font-variant-numeric: tabular-nums; }
.fa-field input[type=range] { -webkit-appearance: none; appearance: none; width: 100%; height: 6px; margin: 16px 0 8px; border-radius: 999px; cursor: pointer;
  background: linear-gradient(90deg, #c9a227 var(--p, 50%), #ebe5d6 var(--p, 50%)); }
.fa-field input[type=range]::-webkit-slider-thumb { -webkit-appearance: none; width: 22px; height: 22px; border-radius: 50%; background: #fff;
  border: 2px solid #8a6520; box-shadow: 0 4px 10px -2px rgba(166, 124, 0, .45); transition: transform .2s var(--ease); }
.fa-field input[type=range]::-moz-range-thumb { width: 18px; height: 18px; border-radius: 50%; background: #fff; border: 2px solid #8a6520; }
.fa-field input[type=range]:active::-webkit-slider-thumb { transform: scale(1.12); }
.fa-field__scale { display: flex; justify-content: space-between; font-size: 11px; color: var(--sub); }
.fa-field--row { display: flex; flex-wrap: wrap; align-items: center; gap: 12px; }
.fa-field select { height: 38px; padding: 0 12px; border-radius: 10px; font: inherit; font-size: 14px; font-weight: 500; color: var(--ink);
  background: var(--card); border: 1px solid #9a8f76; }
.fa-rate { margin-left: auto; padding: 6px 12px; border-radius: 999px; font-size: 13px; font-weight: 500; color: var(--bronze); background: var(--cream); }
.fa-calc__out { display: grid; align-content: center; gap: 16px; padding: 24px; border-radius: 20px;
  background: linear-gradient(150deg, #fffdf6, var(--cream)); border: 1px solid rgba(229, 184, 102, .45); }
.fa-calc__out dd { margin-top: 4px; font-size: 20px; font-weight: 700; color: var(--ink); font-variant-numeric: tabular-nums; }
.fa-calc__out dd.fa-gain { color: #06963c; }
.fa-calc__total { padding-top: 16px; border-top: 1px solid rgba(212, 175, 55, .35); }
.fa-calc__total dd { font-size: 28px; letter-spacing: -.5px; }
.fa-calc__plans-t { margin: 26px 0 12px; font-size: 15px; font-weight: 700; color: var(--bronze); }
.fa-plans { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
.fa-plan { display: grid; grid-template-columns: 40px minmax(0, 1fr) auto; align-items: center; gap: 14px 12px; padding: 16px; border-radius: 18px;
  background: var(--page); border: 1px solid var(--line); }
.fa-plan > img { width: 40px; height: 40px; border-radius: 50%; object-fit: contain; background: #fff; }
.fa-plan h3 { font-size: 14px; font-weight: 700; color: var(--ink); }
.fa-plan dl { grid-column: 1 / -1; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); padding-top: 12px; border-top: 1px solid var(--line); }
.fa-plan dl div + div { padding-left: 12px; border-left: 1px solid var(--line); }
.fa-plan dd { margin-top: 4px; font-size: 14px; font-weight: 700; color: var(--ink); white-space: nowrap; }
.fa-plan dd.fa-gain { color: #06963c; }

/* Steps: one rail, three stops */
.fa-steps ol { position: relative; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; list-style: none; padding: 0; margin: 0; }
.fa-steps ol::before { content: ""; position: absolute; left: 16%; right: 16%; top: 32px; height: 1px;
  background: repeating-linear-gradient(90deg, rgba(138, 101, 32, .45) 0 6px, transparent 6px 12px); }
.fa-steps li { position: relative; display: grid; justify-items: center; align-content: start; gap: 8px; text-align: center; }
.fa-steps__num { margin-top: 4px; }
.fa-steps__ic { display: grid; place-items: center; width: 64px; height: 64px; border-radius: 50%; background: var(--card);
  border: 1px solid rgba(212, 175, 55, .4); box-shadow: 0 10px 24px -14px rgba(166, 124, 0, .55); }
.fa-steps__num { font-size: 11px; font-weight: 700; letter-spacing: 1.5px; color: var(--bronze); }
.fa-steps li p { font-size: 15px; font-weight: 700; color: var(--ink); }

/* Collections bento: 2 then 3 */
.fa-cols__grid { display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 14px; }
.fa-cols__grid li { grid-column: span 2; }
.fa-cols__grid li:nth-child(1) { grid-column: span 4; }
.fa-col { display: flex; align-items: center; gap: 14px; height: 100%; min-height: 104px; padding: 18px; border-radius: 20px; background: var(--card);
  border: 1px solid var(--line); box-shadow: var(--shadow); transition: transform .35s var(--ease), border-color .35s var(--ease); }
.fa-col:hover { transform: translateY(-3px); border-color: rgba(212, 175, 55, .55); }
.fa-col img { flex: none; width: 40px; height: 40px; object-fit: contain; }
.fa-col strong { display: block; font-size: 14px; line-height: 1.35; font-weight: 700; color: var(--ink); }
.fa-col em { display: block; margin-top: 4px; font-style: normal; font-size: 12px; line-height: 1.45; color: var(--sub); }
.fa-col--wide { background: linear-gradient(120deg, #fffdf6, var(--cream)); border-color: rgba(229, 184, 102, .45); }
.fa-col--wide strong { font-size: 17px; }

/* Explainer + calc band */
.fa-what__card { display: grid; grid-template-columns: minmax(0, 1fr) 180px; gap: 28px; align-items: center; padding: 28px; border-radius: 24px;
  background: var(--card); border: 1px solid var(--line); box-shadow: var(--shadow); }
.fa-what__body { margin-top: 12px; font-size: 14px; line-height: 1.65; color: var(--sub); max-width: 62ch; }
.fa-what__means { margin-top: 18px; display: flex; flex-wrap: wrap; align-items: center; gap: 10px; }
.fa-what__means > span { font-size: 13px; font-weight: 700; color: var(--ink); }
.fa-what__art { width: 180px; height: auto; }
.fa-band { margin-top: 14px; display: flex; align-items: center; gap: 16px; padding: 14px 18px 14px 20px; border-radius: 20px;
  background: linear-gradient(120deg, #fffdf6, var(--cream)); border: 1px solid rgba(229, 184, 102, .45); }
.fa-band p { flex: 1; font-size: 16px; font-weight: 700; color: var(--ink); }

/* Blog */
.fa-blog__row { display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr); grid-template-rows: auto auto; gap: 16px; }
.fa-blog__row > li:first-child { grid-row: span 2; }
.fa-blog__row > li:not(:first-child) .fa-post { flex-direction: row; }
.fa-blog__row > li:not(:first-child) .fa-post { align-items: center; }
.fa-blog__row > li:not(:first-child) .fa-post__media { flex: none; width: 44%; margin: 12px 0 12px 12px; border-radius: 12px; }
.fa-blog__row > li:first-child .fa-post__body strong { font-size: 18px; line-height: 1.4; }
.fa-post { display: flex; flex-direction: column; height: 100%; overflow: hidden; border-radius: 20px; background: var(--card); border: 1px solid var(--line);
  box-shadow: var(--shadow); transition: transform .35s var(--ease); }
.fa-post:hover { transform: translateY(-3px); }
.fa-post__media { aspect-ratio: 16 / 9; overflow: hidden; }
.fa-post__media img { width: 100%; height: 100%; object-fit: cover; transition: transform .6s var(--ease); }
.fa-post:hover .fa-post__media img { transform: scale(1.04); }
.fa-post__body { flex: 1; display: flex; flex-direction: column; gap: 8px; padding: 16px; }
.fa-post__body strong { font-size: 14px; line-height: 1.45; font-weight: 700; color: var(--ink); }
.fa-post__body time { font-size: 12px; color: var(--sub); }
.fa-post__more { margin-top: auto; display: inline-flex; align-items: center; gap: 4px; font-size: 13px; font-weight: 700; color: var(--bronze); }
.fa-post__more .xa-ic { width: 16px; height: 16px; transition: transform .3s var(--ease); }
.fa-post:hover .fa-post__more .xa-ic { transform: translateX(3px); }

/* Trust */
.fa-trust { display: grid; gap: 18px; }
.fa-trust .xa-rule { text-transform: none; }
.fa-trust__stats { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); padding: 22px 8px; border-radius: 20px; background: var(--card);
  border: 1px solid var(--line); box-shadow: var(--shadow); }
.fa-trust__stats li { display: grid; gap: 6px; padding: 0 16px; text-align: center; }
.fa-trust__stats li + li { border-left: 1px solid var(--line); }
.fa-trust__stats strong { font-size: 24px; line-height: 1.1; font-weight: 700; letter-spacing: -.5px;
  background: linear-gradient(118deg, #d4af37 0%, #a67c00 55%, #8a6520 100%); -webkit-background-clip: text; background-clip: text; color: transparent; }
.fa-trust__stats span { font-size: 12px; line-height: 1.4; color: var(--sub); }
.fa-trust__logos { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-around; gap: 20px 32px; padding: 4px 8px; }
.fa-trust__logos img { height: 30px; width: auto; filter: grayscale(1); opacity: .7; transition: filter .3s, opacity .3s; }
.fa-trust__logos img:hover { filter: none; opacity: 1; }

/* FAQ + help */
.fa-faq__grid { display: grid; grid-template-columns: minmax(0, 1fr) 240px; gap: 16px; align-items: start; }
.fa-faq__list { display: grid; gap: 10px; }
.fa-q { border-radius: 18px; background: var(--card); border: 1px solid var(--line); transition: border-color .3s var(--ease); }
.fa-q[open] { border-color: rgba(212, 175, 55, .55); }
.fa-q summary { display: flex; align-items: center; justify-content: space-between; gap: 16px; padding: 16px 18px; cursor: pointer; list-style: none;
  font-size: 15px; line-height: 1.4; font-weight: 700; color: var(--ink); }
.fa-q summary::-webkit-details-marker { display: none; }
.fa-q__ic { position: relative; flex: none; width: 28px; height: 28px; border-radius: 50%; background: var(--cream); }
.fa-q__ic::before, .fa-q__ic::after { content: ""; position: absolute; left: 50%; top: 50%; width: 11px; height: 1.5px; border-radius: 1px;
  background: var(--bronze); transform: translate(-50%, -50%); transition: transform .3s var(--ease); }
.fa-q__ic::after { transform: translate(-50%, -50%) rotate(90deg); }
.fa-q[open] .fa-q__ic::after { transform: translate(-50%, -50%) rotate(0deg); }
.fa-q__a { padding: 0 18px 18px; display: grid; gap: 10px; font-size: 14px; line-height: 1.65; color: var(--sub); }
.fa-help { position: sticky; top: 96px; display: grid; justify-items: start; gap: 10px; padding: 22px; border-radius: 20px;
  background: linear-gradient(160deg, #fffdf6, var(--cream)); border: 1px solid rgba(229, 184, 102, .45); }
.fa-help__art { width: 96px; height: 96px; }
.fa-help__t { display: flex; align-items: center; gap: 8px; font-size: 16px; font-weight: 700; color: var(--ink); }
.fa-help__d { font-size: 13px; line-height: 1.55; color: var(--sub); }
.fa-help .xa-gold-btn { margin-top: 6px; width: 100%; }

@media (max-width: 860px) {
  .fa-fd { grid-template-columns: 40px minmax(0, 1fr); }
  .fa-fd__facts { grid-column: 1 / -1; grid-template-columns: repeat(3, minmax(0, 1fr)); }
}
@media (max-width: 767px) {
  .fa-launch__label { flex-basis: 100%; margin-bottom: -12px; }
  .xa-launch__side:has(.fa-launch__label) { flex-wrap: wrap; }
  .fa-fd__facts { grid-template-columns: repeat(3, max-content); justify-content: space-between; gap: 12px; }
  .fa-fd__facts dt { white-space: nowrap; }
  .fa-fd__facts .fa-fd__rate { font-size: 20px; }
  .fa-fd { padding: 16px; }
  .fa-tabs button { flex-direction: column; gap: 4px; height: 64px; font-size: 12px; }
  .fa-calc__card { padding: 18px; }
  .fa-calc__grid, .fa-plans, .fa-faq__grid, .fa-what__card { grid-template-columns: minmax(0, 1fr); }
  .fa-rate { margin-left: 0; }
  .fa-steps ol { grid-template-columns: minmax(0, 1fr); gap: 18px; }
  .fa-steps ol::before { left: 32px; right: auto; top: 32px; bottom: 32px; width: 1px; height: auto;
    background: repeating-linear-gradient(180deg, rgba(138, 101, 32, .45) 0 6px, transparent 6px 12px); }
  .fa-steps li { grid-template-columns: 64px auto 1fr; justify-items: start; align-items: center; text-align: left; gap: 14px; }
  .fa-cols__grid { grid-template-columns: minmax(0, 1fr); }
  .fa-cols__grid li, .fa-cols__grid li:nth-child(1) { grid-column: auto; }
  .fa-what__card { padding: 20px; }
  .fa-what__art { width: 140px; justify-self: center; }
  .fa-band { flex-wrap: wrap; }
  .fa-blog__row { grid-auto-flow: column; grid-template-columns: none; grid-auto-columns: 264px; overflow-x: auto; scroll-snap-type: x mandatory;
    scrollbar-width: none; padding: 4px 16px 22px; margin: -4px -16px -18px; scroll-padding-inline: 16px; }
  .fa-blog__row > li { scroll-snap-align: start; }
  .fa-blog__row { grid-template-rows: none; }
  .fa-blog__row > li:first-child { grid-row: auto; }
  .fa-blog__row > li:not(:first-child) .fa-post { flex-direction: column; align-items: stretch; }
  .fa-blog__row > li:not(:first-child) .fa-post__media { width: auto; margin: 0; border-radius: 0; }
  .fa-blog__row > li:first-child .fa-post__body strong { font-size: 14px; }
  .fa-trust__stats { grid-template-columns: repeat(2, minmax(0, 1fr)); row-gap: 20px; }
  .fa-trust__stats li:nth-child(3) { border-left: 0; }
  .fa-help { position: static; }
}
</style>
"""

SCRIPT = """<script>
// user-fixed-deposits-app: FD type tabs and the returns calculator.
(function () {
  var tabs = [].slice.call(document.querySelectorAll('.fa-tabs [role="tab"]'));
  function pick(n, focus) {
    tabs.forEach(function (t, k) {
      var on = k === n;
      t.setAttribute('aria-selected', String(on));
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
    });
    if (focus) tabs[n].focus();
  }
  tabs.forEach(function (t, k) {
    t.addEventListener('click', function () { pick(k); });
    t.addEventListener('keydown', function (e) {
      var d = { ArrowRight: 1, ArrowLeft: -1 }[e.key];
      if (d) { e.preventDefault(); pick((k + d + tabs.length) % tabs.length, true); }
    });
  });

  // Quarterly compounding on maturity, simple interest when paid out: the
  // capture's 2,00,000 at 8.25% for 60 months gives 3,00,852.79.
  var RATE = 8.25;
  var amount = document.getElementById('fa-amount');
  var tenure = document.getElementById('fa-tenure');
  var payout = document.getElementById('fa-payout');
  if (!amount) return;
  function inr(n, paise) {
    return '\\u20B9 ' + n.toLocaleString('en-IN', { minimumFractionDigits: paise ? 2 : 0, maximumFractionDigits: paise ? 2 : 0 });
  }
  function update() {
    var p = +amount.value, m = +tenure.value, r = RATE / 100;
    var maturity = payout.value === 'cumulative' ? p * Math.pow(1 + r / 4, m / 3) : p * (1 + r * m / 12);
    document.getElementById('fa-amount-out').textContent = inr(p);
    document.getElementById('fa-tenure-out').textContent = m;
    document.getElementById('fa-invested').textContent = inr(p);
    document.getElementById('fa-gains').textContent = inr(maturity - p, true);
    document.getElementById('fa-maturity').textContent = inr(maturity, true);
    [amount, tenure].forEach(function (el) {
      el.style.setProperty('--p', ((el.value - el.min) / (el.max - el.min) * 100) + '%');
    });
  }
  [amount, tenure, payout].forEach(function (el) { el.addEventListener('input', update); });
  update();
})();
</script>
"""


def main():
    X.assemble(body(), OUT, "Fixed Deposits | GoldenPi",
               "pages/_fd_app.py (user-fixed-deposits.html content in the user-explore-app design; "
               "navbar and footer from bond-details3.html)",
               style=STYLE, script=SCRIPT, current="user-fixed-deposits.html")


if __name__ == "__main__":
    main()
