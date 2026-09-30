#!/usr/bin/env python3
"""Generate the logged-in profile pages.

    profile.html         <- /profile, KYC completed: every section
    profile-no-kyc.html  <- /profile before KYC: User Details and Orders only

Copy and structure come from content/profile.md, the uatnew capture of
2026-09-30 (crawl/profile_tabs.js). The Demat and Nominee sections follow the
Figma section 21:2427 (file HRSMFFccdLgqf1YwD7oyc9): Demat 21:1015 / 21:1605,
Nominee Details 21:1688 / 21:2199, Add a new nominee 21:979.

Grouping asked for on 2026-09-30, where the live sidebar has one item each:
User Details also holds Personal Details and Investor Details, and Demat also
holds Exchange Details. On the live site Orders and Form 121 Center are routes
of their own (/profile/orders, /profile/form121-center); here they are panels
of the one page, addressed by hash.

Every value is a placeholder marked <!-- DATA: ... -->. Personal values are the
Figma sample persona, never a real account.

Shell comes from _user.shell(). Card surfaces, the sheet and the tablist
behaviour are reused from assets/portfolio.css and _portfolio.js; the rest is
assets/profile.css and _profile.js, inlined.

Run: python3 pages/_profile.py
"""
import os

import _user as U

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = "../assets/img/"
P = IMG + "profile/"
R = "&#8377;"
NAME = "Rohit Sharma"


def icon(name, w=16, h=None, alt="", cls=""):
    return '<img src="%s%s" alt="%s" width="%d" height="%d"%s>' % (
        P, name, alt, w, h or w, ' class="%s"' % cls if cls else "")


def edit(what):
    return ('<button type="button" class="pr-edit" aria-label="Edit %s">%s</button>'
            % (what, icon("profile-edit.webp")))


def copy(value, what):
    return ('<button type="button" class="pr-copy" data-copy="%s" aria-label="Copy %s">%s</button>'
            % (value, what, icon("copy.svg")))


def fields(items, cls=""):
    """items: (label, value html[, extra class]). A <dl>, one cell per pair."""
    cells = "".join('<div%s><dt>%s</dt><dd>%s</dd></div>'
                    % (' class="%s"' % c[0] if c else "", k, v) for k, v, *c in items)
    return '      <dl class="pr-fields%s">%s</dl>\n' % (cls, cells)


def card(title, body, after="", sub=None, cls=""):
    head = ""
    if title:
        head = ('      <div class="pr-card__head"><h3 class="pr-card__title">%s</h3>%s</div>\n' % (title, after)
                + ('      <p class="pr-card__sub">%s</p>\n' % sub if sub else ""))
    return '    <section class="pr-card%s">\n%s%s    </section>\n' % (cls, head, body)


def panel(id_, title, sub, body, badge="", back=None):
    return ('  <section class="pr-panel" id="%s" aria-labelledby="%s-t" data-panel>\n'
            '    <a class="pr-back" href="#profile-menu">%s<span>%s</span></a>\n'
            '    <header class="pr-head"><div><h2 class="pr-title" id="%s-t">%s</h2>'
            '%s</div>%s</header>\n%s  </section>\n'
            % (id_, id_, icon("back.svg", 20, alt="Back to profile menu"), back or title, id_, title,
               '<p class="pr-sub">%s</p>' % sub if sub else "", badge, body))


# ---------------------------------------------------------------- sidebar

NAV_FULL = [("user-details", "User Details"), ("demat", "Demat"), ("bank", "Bank"),
            ("nominee", "Nominee Details"), ("reports", "Reports And Documents"),
            ("account-closure", "Account Closure"), ("orders", "Orders"),
            ("portfolio.html", "Portfolio"), ("form-121", "Form 121 Center")]
# Before KYC the live sidebar is this short. Form 121 was not captured for such
# an account, so its item opens the KYC-completed page.
NAV_NO_KYC = [("user-details", "User Details"), ("orders", "Orders"),
              ("portfolio-no-kyc.html", "Portfolio"), ("profile.html#form-121", "Form 121 Center")]

CHEV = icon("chevron.svg", 11, 6, cls="pr-nav__chev")


def sidebar(items):
    links = ""
    for k, (href, label) in enumerate(items):
        page = "." in href
        links += ('        <li><a href="%s%s"%s>%s%s</a></li>\n'
                  % ("" if page else "#", href, ' aria-current="page"' if k == 0 else "", label, CHEV))
    return ('<aside class="pr-side" id="profile-menu" aria-label="Profile">\n'
            '  <!-- DATA: account holder; the chevron opens the family-account switcher. -->\n'
            '  <button type="button" class="pr-switch" aria-haspopup="true">Selected Profile%s</button>\n'
            '  <div class="pr-who"><span class="pr-avatar"><img src="%savatar.jpg" alt="" width="75" height="75"></span>'
            '<p>%s</p></div>\n'
            '  <nav class="pr-nav" aria-label="Profile navigation">\n      <ul role="list">\n%s      </ul>\n  </nav>\n'
            '  <button type="button" class="pr-logout">Logout%s</button>\n'
            '</aside>\n' % (icon("chevron-down.svg", 11, 6), P, NAME, links, CHEV))


# ------------------------------------------------------------ user details

def user_details(kyc):
    if kyc:
        status = ('<p class="pr-kyc pr-kyc--ok">KYC Completed%s</p>' % icon("completed-icon.svg", 18))
        investor = ("Investor type", "Resident Indian Citizen")
    else:
        status = '<p class="pr-kyc pr-kyc--todo"><button type="button">Complete KYC</button></p>'
        investor = ("Investor type" + edit("investor type"), "&mdash;")
    lang = ('<select class="pr-select" id="pr-lang"><option selected>English</option></select>')
    profile = (
        '      <!-- DATA: account holder, KYC state and preferences. Each pencil opens its edit modal. -->\n'
        '      <div class="pr-id"><span class="pr-avatar pr-avatar--lg">'
        '<img src="%savatar.jpg" alt="" width="96" height="96"></span>'
        '<div><p class="pr-id__name">%s</p>%s</div></div>\n' % (P, NAME, status)
        + fields([investor,
                  ("Password" + edit("password"), "XXXXXXXXX"),
                  ("MPIN" + edit("MPIN"), "XXXX"),
                  ("Risk Appetite" + edit("risk appetite"), "AGGRESSIVE"),
                  ('<label for="pr-lang">Default Communication Language</label>', lang, "pr-span2")], " pr-fields--3")
        + '      <hr class="pr-rule">\n'
        '      <div class="pr-card__head"><h3 class="pr-card__title">Contact Details</h3>%s</div>\n'
        % edit("contact details")
        + fields([("Mobile number", '91-XXXXX43210<span class="pr-ok">%sPhone Verified</span>' % icon("verified-tick.svg", 18)),
                  ("Email", 'XXXXXXrma@example.com<span class="pr-ok">%sEmail Verified</span>' % icon("verified-tick.svg", 18))],
                 " pr-fields--2"))
    body = card("Profile", profile)
    if kyc:
        body += card("Personal Details", (
            '      <!-- DATA: KYC record. Empty values render as "--", as on the live page. -->\n'
            + fields([("PAN", "ECY******B"), ("DOB", "14-Aug-1990"), ("Gender", "Male"),
                      ("Nationality", "--"), ("Father/Spouse Name", "--"), ("Political Connection", "No"),
                      ("Resident Status", "--"),
                      ("Address", "42, 5th Cross, Indiranagar, Bengaluru, Karnataka, 560038", "pr-span2")],
                     " pr-fields--3")), edit("personal details"), "View and update your personal information")
        body += card("Investor Details", (
            '      <!-- DATA: investor profile. -->\n'
            + fields([("Income", "5-10 Lakhs"), ("Occupation", "Private Sector"), ("Marital Status", "Single")],
                     " pr-fields--3")), edit("investor details"), "Your investor profile and related information")
    return panel("user-details", "User Details", "Manage your personal information and account preferences", body)


# ------------------------------------------------------------------ demat

def demat():
    body = card("", (
        '      <!-- DATA: demat account, Figma 21:1015. -->\n'
        + fields([("Demat Account Number", "12081600XXXX1234" + copy("12081600XXXX1234", "demat account number")),
                  ("DP ID", "12081600" + copy("12081600", "DP ID")),
                  ("Broker Name (DP)", "GoldenPi Securities Pvt. Ltd."), ("Depository", "CDSL"),
                  ("Account Type", "Individual - Resident"), ("Account Holder Name", NAME),
                  ("PAN", "ECY******B"), ("Demat Linked Bank Account", "XXXX XXXX 1234")], " pr-fields--demat")
        + '      <div class="pr-card__foot"><p class="pr-free">%sYour Demat account with us is lifetime free.</p>'
          '<button type="button" class="pr-close">Close Demat Account &rarr;</button></div>\n' % icon("shield.svg", 14)),
        cls=" pr-card--demat")
    body += card("Exchange Details", (
        '      <!-- DATA: trading account. -->\n'
        + fields([("UCC Number", "RS123456@GSPL"), ("Exchange Enabled", "BSE, NSE")], " pr-fields--demat")
        + '      <button type="button" class="pr-dl">%sDownload KYC Application Form</button>\n'
        % icon("download-deal-sheet.svg", 20)), sub="Exchange and UCC information linked to your account")
    return panel("demat", "Demat Account", "Manage your GoldenPi Demat Account &amp; account information", body,
                 badge='<span class="pr-badge pr-badge--live">Active</span>')


# ------------------------------------------------------------------- bank

BANKS = [("HDFC0001234", "XXXXXXXX001234", "HDFC Bank"), ("SBIN0001234", "XXXXXXXX005678", "State Bank of India")]


def bank():
    rows = ""
    for k, (ifsc, acc, name) in enumerate(BANKS):
        rows += '      <div class="pr-bank">%s%s</div>\n' % (
            fields([("IFSC Code", ifsc), ("Account Number", acc), ("Bank Name", name)], " pr-fields--3").strip(),
            '<span class="pr-badge pr-badge--ok">Default</span>' if k == 0 else "")
    body = card("Bank Account Details", "      <!-- DATA: linked bank accounts; the first is the default. -->\n" + rows,
                edit("bank account details"))
    return panel("bank", "Bank", "Manage your bank and virtual account details", body)


# ---------------------------------------------------------------- nominee

def nominee():
    body = (
        '    <!-- DATA: nominees, Figma 21:1688. Up to three. -->\n'
        '    <section class="pr-card pr-card--flush">\n'
        '      <div class="pr-nominee__head"><h3 class="pr-nominee__name">Jiya Sharma</h3>'
        '<span class="pr-chip">Minor</span>'
        '<button type="button" class="pr-edit pr-edit--tile" aria-label="Edit nominee Jiya Sharma">%s</button></div>\n'
        % icon("profile-edit.webp")
        + fields([("Date of Birth", "10 Dec 2017"), ("Relationship", "Daughter"), ("Allocation Percentage", "50%")],
                 " pr-fields--nominee")
        + '    </section>\n'
        '    <button type="button" class="pr-more" data-sheet="sheet-nominee">%sAdd more nominees</button>\n'
        % icon("plus-soft.svg")
        + '    <p class="pr-notice">%s<span>By proceeding you confirm these details are accurate. '
          'You will e-sign the nomination form using your registered mobile OTP.</span></p>\n' % icon("info.svg", 12)
        + '    <button type="button" class="pr-gold">%sAdd Nominee</button>\n' % icon("plus.svg"))
    return panel("nominee", "Nominee Details", "Manage your nominee information for seamless transfers", body,
                 back="Add Nominee")


# The empty state (Figma 21:979), reused as the entry to adding another nominee.
SHEET_NOMINEE = (
    '<dialog class="pf-sheet pf-sheet--light pr-sheet" id="sheet-nominee" aria-labelledby="sheet-nominee-t">\n'
    '  <div class="pf-sheet__head"><span class="pf-sheet__handle"></span>'
    '<button type="button" class="pf-sheet__close" data-close aria-label="Close">'
    '<img src="%sportfolio/cross-dark.svg" alt=""></button></div>\n'
    '  <div class="pf-sheet__body">\n'
    '    <div><h2 id="sheet-nominee-t">Add a new nominee</h2>'
    '<p class="pr-sub">You can add up to 3 nominees for your account.</p></div>\n'
    '    <div class="pr-empty"><span class="pr-empty__icon">%s</span>'
    '<h3>Protect your investments for the future</h3>'
    '<p>Add a nominee so your bonds can be smoothly transferred to your chosen nominee when needed.</p>'
    '<button type="button" class="pr-gold">%sAdd Nominee</button></div>\n'
    '  </div>\n</dialog>\n' % (IMG, icon("nominee.svg", 36), icon("plus.svg")))


# ---------------------------------------------------------------- reports

def reports():
    body = card("Reports", (
        '      <!-- DATA: report types and financial years; one of each on the captured account. -->\n'
        '      <div class="pr-form">\n'
        '        <div><label for="pr-report-type">Report type</label>'
        '<select class="pr-select" id="pr-report-type"><option selected>AGTS (Annual Global Transaction Statement)</option></select></div>\n'
        '        <div><label for="pr-report-fy">Financial year</label>'
        '<select class="pr-select" id="pr-report-fy"><option selected>2025-2026 (Apr 2025 - Mar 2026)</option></select></div>\n'
        '      </div>\n'
        '      <button type="button" class="pr-dl">%sDownload report</button>\n' % icon("download-deal-sheet.svg", 20)),
        after='<img src="%sportfolio/statement.png" alt="" width="56" height="56" class="pr-card__art">' % IMG)
    return panel("reports", "Reports And Documents", "Download statements and documents", body)


def closure():
    mail = ("mailto:contact-us@goldenpi.com?subject=Account%20closure%20request%3A%20RS123456"
            "&amp;body=I%20request%20the%20GoldenPi%20team%20to%20close%20my%20account%20with%20GoldenPi."
            "%20I%20understand%20that%20this%20change%20will%20be%20irreversible.")
    body = card("Account Closure", (
        '      <!-- DATA: the mail subject carries the account\'s UCC. -->\n'
        '      <p class="pr-text">Account closure is permanent and irreversible. <a href="%s">Close my account</a></p>\n'
        '      <p class="pr-text">For any complaints, visit: '
        '<a href="https://scores.sebi.gov.in/scores-home" target="_blank" rel="noopener noreferrer">SCORES</a></p>\n'
        % mail))
    return panel("account-closure", "Account Closure", "Request permanent closure of your GoldenPi account", body)


# ----------------------------------------------------------------- orders

LISTED = '<img class="pr-order__tag" src="%slisted-tag.svg" alt="Listed Asset" width="137" height="22">' % P


def logo(src, name):
    if not src:
        return '<span class="pr-logo" aria-hidden="true">%s</span>' % name[:2].upper()
    return '<span class="pr-logo"><img src="%s%s" alt="" width="40" height="40"></span>' % (IMG, src)


def status(text):
    kind = {"Pending": "wait", "Processing": "wait", "Deal Settled": "ok", "FD Booked": "ok",
            "Verification Successful": "ok", "Approved By Bank": "ok", "FD Rejected": "bad"}.get(text)
    return '<span class="pr-st pr-st--%s">%s</span>' % (kind, text) if kind else text


def order(name, src, meta, cells, listed=True, action="", foot=""):
    return ('      <article class="pr-order">%s\n'
            '        <header class="pr-order__head">%s<div><h4>%s</h4><p>%s</p></div>%s</header>\n'
            '  %s%s      </article>\n'
            % (LISTED if listed else "", logo(src, name), name, meta, action,
               fields([(k, status(v)) for k, v in cells], " pr-fields--row"), foot))


CANCEL = '<button type="button" class="pr-ghost">%sCancel</button>' % icon("remove-btn.svg")
DEAL = ('        <p class="pr-order__foot"><button type="button" class="pr-dl pr-dl--sm">%sDownload Deal sheet</button></p>\n'
        % icon("download-deal-sheet.svg", 18))
PAY = ('        <p class="pr-order__note">%s <button type="button" class="pr-textbtn">Continue</button></p>\n')

BOND_PENDING = [
    ("NEOGROWTH", "GPID104095.Neogrowth-new-logo-1-.jpg", "INE814O07634", "28-Sep-2026", "3,05,825.40", "3", "19 Months", "13%"),
    ("BEST CAPITAL", "GPID107347.Best-Capital.png", "INE04UP07246", "28-Sep-2026", "29,865.85", "3", "36 Months", "13%"),
]
BOND_HISTORY = [
    ("AKARA", "GPID102720.AKARA-CAPITAL-ADVISORS-PRIVATE-LIMITED-2x.png", "INE08XP07522", "1-Oct-2026", "1,00,169.51", "1", "YTM", "13%", "Processing", True),
    ("MUTHOOT MCRED", "GPID103446.MUTHOOTTU-MINI-FINANCIERS-LTD-2x.png", "INE101Q07BZ6", "7-Jul-2026", "9,932.77", "1", "Yield", "10.9%", "Deal Settled", True),
    ("ADANI ENTERPRISES", "GPID104322.ADANI-ENTERPRISES-LIMITED.png", "INE423A07492", "28-Apr-2026", "1,007.92", "1", "YTM", "8.6%", "Deal Settled", True),
    ("ADANI ENTERPRISES", "GPID104322.ADANI-ENTERPRISES-LIMITED.png", "INE423A07492", "9-Apr-2026", "1,003.51", "1", "YTM", "8.6%", "Deal Settled", True),
    ("MAMTA PROJECTS PVT LTD", "profile/mamta.png", "INE0GA407226", "1-Feb-2023", "2,98,050.00", "3", "YTM", "15.1%", "Deal Settled", False),
]
EMPTY = '      <p class="pr-none">No orders found!</p>\n'


def orders_bonds():
    out = '      <h3 class="pr-h3">Pending order</h3>\n      <!-- DATA: open bond orders. -->\n'
    for n, src, isin, d, inv, units, tenure, ytm in BOND_PENDING:
        out += order(n, src, isin, [("Order Date", d), ("Investment", R + " " + inv), ("Units", units),
                                    ("Tenure", tenure), ("YTM", ytm), ("Status", "Pending")],
                     action=CANCEL, foot=PAY % "Select your payment method.")
    out += '      <h3 class="pr-h3">Order history</h3>\n      <!-- DATA: past bond orders, newest first. -->\n'
    for n, src, isin, d, inv, units, ylabel, y, st, listed in BOND_HISTORY:
        out += order(n, src, isin, [("Date", d), ("Investment", R + " " + inv), ("Units", units), ("Type", "Buy"),
                                    (ylabel, y), ("Status", st)],
                     listed=listed, foot=DEAL if st == "Deal Settled" else "")
    return out


IPOS = [("58216352", "INDEL MONEY LIMITED", "GPID102671.INDEL-MONEY-LIMITED-2x.png", "20-Aug-2026 9:30:12 AM",
         "18-Aug-2026 1:31:21 PM", "15,000.00", "15"),
        ("57183205", "PAISALO DIGITAL LIMITED", None, "14-Aug-2026 9:30:08 AM", "10-Aug-2026 10:01:25 AM",
         "10,000.00", "10")]


def orders_ipo():
    out = '      <h3 class="pr-h3">Online Orders</h3>\n      <!-- DATA: IPO applications; PAN and UPI handle masked here. -->\n'
    for app, n, src, upd, made, inv, units in IPOS:
        meta = ('Application no: %s<br>Last updated on %s<br>Created on : %s<br>CDSL: XXXXXXXXXX001234'
                % (app, upd, made))
        foot = ('        <p class="pr-order__foot"><button type="button" class="pr-textbtn">View series</button>'
                '<button type="button" class="pr-textbtn" disabled>Cancel Application</button>'
                '<span class="pr-chip">IPO Closed</span></p>\n')
        out += order(n, src, meta, [("PAN Number", "ECY******B"), ("Total Investment", R + " " + inv),
                                    ("Total Units", units), ("UPI Handle", "XXXXXX3210@ybl"),
                                    ("DP Status", "Verification Successful"), ("Payment Status", "Approved By Bank")],
                     listed=False, action='<button type="button" class="pr-ghost">Refresh</button>', foot=foot)
    return out + '      <h3 class="pr-h3">Offline Orders</h3>\n' + EMPTY


def orders_fd():
    unity, shriram = "GPID105192.Unity.png", "GPID100016.Shriram-Squircle.png"
    out = '      <h3 class="pr-h3">Pending order</h3>\n      <!-- DATA: open FD orders. -->\n'
    out += order("UNITY SMALL FINANCE BANK", unity, "Fixed Deposit",
                 [("Order Date", "28-Sep-2026"), ("Investment", R + " 5,000.00"), ("Tenure", "501 D"),
                  ("Payout Mode", "On Maturity"), ("Interest Rate", "8%"), ("Status", "Pending")], listed=False,
                 action='<button type="button" class="pr-ghost">Refresh</button>'
                        '<button type="button" class="pr-ghost">%sRemove</button>' % icon("remove-btn.svg"),
                 foot=PAY % "Your order is pending. Pay now and complete your investment.")
    out += '      <h3 class="pr-h3">Order history</h3>\n      <!-- DATA: past FD orders. -->\n'
    out += order("UNITY SMALL FINANCE BANK", unity, "Payment Date: 3-Jun-2026 1:39:47 PM",
                 [("Investment", R + " 1,000.00"), ("Tenure", "7 D"), ("Payout Mode", "On Maturity"),
                  ("Interest Rate", "4%"), ("Maturity Date", "10-Jun-2026"), ("Maturity Amount", R + " 1,001.00"),
                  ("Current Status", "FD Rejected")], listed=False,
                 foot='        <p class="pr-order__note pr-order__note--bad">Your FD is rejected and any amount '
                      'deducted will be credited back in 4-5 business days.</p>\n')
    out += order("SHRIRAM FINANCE", shriram, "Booking Date: 2023-11-06",
                 [("Investment", R + " 5,000.00"), ("Tenure", "12 M"), ("Payout Mode", "Yearly"),
                  ("Interest Rate", "7.8%"), ("Maturity Date", "2024-11-06"), ("Maturity Amount", R + " 5,000.00"),
                  ("Current Status", "FD Booked")], listed=False,
                 foot='        <p class="pr-order__note"><button type="button" class="pr-textbtn">Click Here</button> '
                      'to know more about redemption and maturity of your FD.</p>\n')
    return out


ORDER_TABS = ["IPO", "Bonds", "Fixed Deposit", "Sovereign Gold Bonds"]


def orders(kyc):
    none = '      <h3 class="pr-h3">Order history</h3>\n' + EMPTY
    if kyc:
        bodies, sel = [orders_ipo(), orders_bonds(), orders_fd(), none], 1
    else:
        # DATA: an account with no orders; the live page's own empty copy.
        bodies, sel = [none] * 4, 1
    tabs = "".join(
        '<button type="button" role="tab" id="orders-t%d" aria-controls="orders-p%d" aria-selected="%s"%s>%s</button>'
        % (k, k, "true" if k == sel else "false", "" if k == sel else ' tabindex="-1"', t)
        for k, t in enumerate(ORDER_TABS))
    body = '    <div class="pr-pills" role="tablist" aria-label="Order type" data-pf-tabs>%s</div>\n' % tabs
    for k, b in enumerate(bodies):
        body += ('    <div role="tabpanel" id="orders-p%d" aria-labelledby="orders-t%d" class="pr-orders%s"%s>\n%s    </div>\n'
                 % (k, k, " is-on" if k == sel else "", "" if k == sel else " hidden", b))
    return panel("orders", "Orders", None, body)


# --------------------------------------------------------------- form 121

F121 = [("ADANI ENTERPRISES LIMITED", "GPID104322.ADANI-ENTERPRISES-LIMITED.png", "INE423A07492", "2,000", "8.48%",
         "Quarterly", "8.56", False),
        ("MUTHOOT MCRED LIMITED", "GPID103446.MUTHOOTTU-MINI-FINANCIERS-LTD-2x.png", "INE101Q07BZ6", "10,000", "9.65%",
         "Monthly", "64.26", True)]

FAQ = [
    ("Why does this matter for you?", "Real money, real impact",
     "<p>Say you invest &#8377;1,00,000 in a bond at 10% interest. That&rsquo;s &#8377;10,000 in annual interest.</p>"
     "<p>Without Form 121, the bond issuer deducts 10% TDS &mdash; you only receive &#8377;9,000. With Form 121 filed, "
     "you receive the full &#8377;10,000.</p>"
     "<p>That difference compounds over time. Across multiple bonds over multiple years, it adds up to real money "
     "sitting in your pocket instead of waiting in a tax refund cycle.</p>"),
    ("Who should file it?", "Check if you qualify",
     "<p>Form 121 is most useful if:</p><ul>"
     "<li>Your total annual income is below &#8377;2.5 lakh (basic exemption limit)</li>"
     "<li>You fall under a lower tax slab and don't want TDS deducted upfront</li>"
     "<li>You prefer to manage your tax liability at filing time rather than through automatic deductions</li></ul>"
     "<p>Even if your income is above the exemption limit, filing Form 121 prevents unnecessary upfront deduction "
     "and improves your cash flow through the year.</p>"),
    ("Is it complicated?", "Takes about 2 minutes",
     "<p>Not at all. GoldenPi pre-fills most of the form using your KYC details &mdash; your name, PAN, address, and "
     "contact information are already there. You only need to confirm a few income details and give your consent.</p>"
     "<p>There are no physical documents to sign, no trips to an office, and no back-and-forth with the Bond Issuer. "
     "GoldenPi submits the form on your behalf.</p>"),
    ("Ready to invest and file?", "Get started in one place",
     "<p>Browse bonds on GoldenPi, make your first investment, and file Form 121 right here &mdash; all in one place.</p>"),
]


def form121():
    body = (
        '    <!-- DATA: TDS this account can avoid, open declarations and the filing deadline. -->\n'
        '    <section class="pr-card pr-f121">\n'
        '      <img src="%sportfolio/form121.png" alt="" width="72" height="72" class="pr-f121__art">\n'
        '      <div class="pr-f121__lead"><p class="pr-f121__amt">%s72.82</p>'
        '<p class="pr-f121__tag">Avoid TDS deductions</p>'
        '<p class="pr-text">Eligible for Form 121? Submit your declaration to receive bond interest payouts '
        'without TDS deduction, subject to issuer approval.</p></div>\n'
        '      <dl class="pr-f121__stats"><div><dt>Pending Form 121</dt><dd class="pr-st--bad">1</dd></div>'
        '<div><dt>Deadline</dt><dd class="pr-st--wait">31 Mar</dd></div></dl>\n'
        '    </section>\n'
        '    <!-- DATA: holdings eligible for Form 121. -->\n' % (IMG, R))
    for n, src, isin, inv, coupon, payout, save, done in F121:
        action = ('<span class="pr-badge pr-badge--ok">Submitted</span>' if done
                  else '<button type="button" class="pr-gold pr-gold--sm">File Form 121</button>')
        foot = "" if done else '        <p class="pr-order__foot pr-order__foot--end"><span class="pr-flag">Not filed TDS</span></p>\n'
        body += ('    <article class="pr-order pr-order--f121">\n'
                 '        <header class="pr-order__head">%s<div><h3>%s</h3></div>%s</header>\n'
                 '        <div class="pr-tile"><p class="pr-tile__isin">%s</p>\n  %s        </div>\n%s    </article>\n'
                 % (logo(src, n), n, action, isin,
                    fields([("Investment", R + inv), ("Coupon (Fixed)", coupon), ("Payout", payout),
                            ("Save Amount", '<span class="pr-save">%s%s</span>' % (R, save))], " pr-fields--row"), foot))
    body += ('    <p class="pr-fine">Filing Form 121 does not guarantee exemption from TDS. GoldenPi only facilitates '
             'submission of the form to the issuer. Acceptance of the declaration and the final TDS decision are at '
             'the issuer\'s discretion.</p>\n'
             '    <section class="pr-faq" aria-labelledby="f121-faq-t">\n'
             '      <h3 class="pr-eyebrow" id="f121-faq-t">Frequently Asked Questions</h3>\n')
    for q, hint, a in FAQ:
        body += ('      <details class="pr-faq__item"><summary><span><b>%s</b><small>%s</small></span>%s</summary>'
                 '<div class="pr-faq__body">%s</div></details>\n' % (q, hint, icon("chevron-down.svg", 11, 6), a))
    body += '    </section>\n'
    return panel("form-121", "Form 121 Center", "Stop TDS deductions on your bond interest &mdash; file in minutes.",
                 body, badge='<span class="pr-badge pr-badge--ok pr-badge--caps">Secure &amp; Encrypted</span>')


# ------------------------------------------------------------------ pages

def page(kyc):
    if kyc:
        nav = NAV_FULL
        panels = (user_details(True) + demat() + bank() + nominee() + reports() + closure()
                  + orders(True) + form121())
    else:
        nav, panels = NAV_NO_KYC, user_details(False) + orders(False)
    return ('  <section class="gp-shell pr" data-profile>\n'
            '    <h1 class="sr-only">Profile</h1>\n'
            '    <div class="pr-grid">\n%s<div class="pr-main">\n%s</div>\n    </div>\n  </section>\n%s'
            % (sidebar(nav), panels, SHEET_NOMINEE if kyc else ""))


PAGES = [("profile.html", True), ("profile-no-kyc.html", False)]
DESC = "Manage your GoldenPi profile, demat and bank details, nominees, orders and Form 121."


def main():
    js = "".join(open(os.path.join(HERE, f), encoding="utf-8").read() for f in ("_portfolio.js", "_profile.js"))
    for out, kyc in PAGES:
        top, bottom = U.shell("Profile | GoldenPi", DESC, None)
        top = top.replace('<link rel="stylesheet" href="../assets/user.css">',
                          '<link rel="stylesheet" href="../assets/user.css">\n'
                          '<link rel="stylesheet" href="../assets/portfolio.css">\n'
                          '<link rel="stylesheet" href="../assets/profile.css">', 1)
        top = top.replace("generated by pages/_user.py from the goldenpi.com capture of 2026-09-26",
                          "generated by pages/_profile.py from the uatnew /profile capture of 2026-09-30 "
                          "and the Figma section 21:2427", 1)
        bottom = bottom.replace("</body>", "<script>\n%s</script>\n</body>" % js, 1)
        html = top + "\n" + page(kyc) + bottom
        with open(os.path.join(HERE, out), "w", encoding="utf-8") as f:
            f.write(html)
        print("%-22s %6d bytes" % (out, len(html)))


if __name__ == "__main__":
    main()
