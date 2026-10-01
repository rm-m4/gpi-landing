#!/usr/bin/env python3
"""Generate refer-and-earn-with-referral.html: Refer & Earn, logged in, for an
account that has referred people.

    refer-and-earn-with-referral.html  <- refer-and-earn.html + the staging page
                                          (stagingnew.goldenpi.com/refer-and-earn,
                                          screenshot of 2026-10-01, logged in)

The hero, steps, caps and FAQ are lifted from refer-and-earn.html so the two
cannot drift; the shell is the logged-in one from _user.shell(). Two blocks are
new, transcribed from the staging screenshot: Your Referral Summary and My
Referrals. Their figures and rows are that account's, marked DATA for the API.

Run: python3 pages/_refer.py
"""
import html
import os
import re

import _user as U

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "refer-and-earn.html"
OUT = "refer-and-earn-with-referral.html"
R = "&#8377;"

# DATA: the account's referral summary, staging snapshot 2026-10-01.
BALANCE = "5,700.00"
SUMMARY = [("Total Referral", "8"), ("Successful Referrals", "1"),
           ("Total Rewards Earned", R + "5,700.00"), ("Total Rewards Settled", "--")]
# DATA: page 1 of the account's referrals. (name, signup date, earned, cap);
# earned None is a referral that has not invested yet.
REFERRALS = [
    ("Referral Points Testing", "21-Sep-2026", 5700, 10000),
    ("new web referral tag", "21-Sep-2026", None, None),
    ("rwes", "19-Sep-2026", None, None),
    ("test", "19-Sep-2026", None, None),
    ("name", "19-Sep-2026", None, None),
]
PENDING = "Reward will be available after first investment"

NOTE_SUMMARY = ("Note: The balance referral bonus amount for a month will be automatically transferred to "
                "your KYC registered bank account by the first week of the next month. Your one time KYC "
                "should be completed for receiving the referral bonus amount.")
NOTE_REFERRALS = ("Note: The referred user must invest at least %s1,00,000 in corporate bonds with a minimum "
                  "remaining tenure of 365 days within 90 days of signing up. You will get flat 1%% reward up "
                  "to %s2,000 for each eligible investment, and up to %s10,000 for every referral." % (R, R, R))


def inr(n):
    """12345 -> 12,345 (amounts here stay under a lakh)."""
    return "{:,}".format(n)


def initials(name):
    return "".join(w[0] for w in name.split()[:2]).upper()


def summary():
    stats = "\n".join(
        '          <div>\n            <dt>%s</dt>\n            <dd>%s</dd>\n          </div>' % s
        for s in SUMMARY)
    return U.section("referral summary", (
        '      <!-- DATA: the account\'s referral summary. -->\n'
        '      <div class="gp-rsum">\n'
        '        <div class="gp-rsum__balance">\n'
        '          <h2 class="gp-rsum__title">Your Referral Summary</h2>\n'
        '          <div class="gp-rsum__amount">\n'
        '            <img src="../assets/img/coin-icon.png" alt="" width="44" height="44">\n'
        '            <p><span>Balance Amount</span><strong>%s%s</strong></p>\n'
        '          </div>\n'
        '        </div>\n'
        '        <dl class="gp-rsum__stats">\n%s\n        </dl>\n'
        '      </div>\n'
        '      <p class="gp-rnote">%s</p>') % (R, BALANCE, stats, NOTE_SUMMARY))


def status(earned, cap):
    if earned is None:
        return '<span class="gp-rstatus gp-rstatus--pending">%s</span>' % PENDING
    return ('<span class="gp-rstatus gp-rstatus--earned"><span>%s%s / %s%s</span>'
            '<meter min="0" max="%d" value="%d" aria-label="%s%s of the %s%s cap earned"></meter></span>'
            % (R, inr(earned), R, inr(cap), cap, earned, R, inr(earned), R, inr(cap)))


def referrals():
    rows = "\n".join(
        '            <tr>\n'
        '              <td data-label="Referral"><span class="gp-rref"><span class="gp-rref__avatar"'
        ' aria-hidden="true">%s</span>%s</span></td>\n'
        '              <td data-label="Signup date">%s</td>\n'
        '              <td data-label="Reward Status">%s</td>\n'
        '            </tr>' % (initials(n), html.escape(n), d, status(e, c)) for n, d, e, c in REFERRALS)
    return U.section("my referrals", (
        U.head("My Referrals") +
        '      <!-- DATA: the account\'s referrals, page 1 of 2; the pager fetches the next page. -->\n'
        '      <div class="gp-rtable">\n'
        '        <table>\n'
        '          <thead>\n'
        '            <tr><th scope="col">Referral</th><th scope="col">Signup date</th>'
        '<th scope="col">Reward Status</th></tr>\n'
        '          </thead>\n'
        '          <tbody>\n%s\n          </tbody>\n'
        '        </table>\n'
        '        <nav class="gp-rpager" aria-label="Referral pages">\n'
        '          <button type="button" aria-label="Previous page" disabled>&lsaquo;</button>\n'
        '          <button type="button" aria-current="page" aria-label="Page 1">1</button>\n'
        '          <button type="button" aria-label="Page 2">2</button>\n'
        '          <button type="button" aria-label="Next page">&rsaquo;</button>\n'
        '        </nav>\n'
        '      </div>\n'
        '      <p class="gp-rnote">%s</p>') % (rows, NOTE_REFERRALS))


def main():
    with open(os.path.join(HERE, SRC), encoding="utf-8") as f:
        src = f.read()
    body = src[src.index('<main id="main-content">') + len('<main id="main-content">'):src.index("</main>")]
    faq = body.index("  <!-- ================================================================= faq -->")
    body = body[:faq] + summary() + "\n" + referrals() + "\n" + body[faq:]
    # The breadcrumb's Home is the logged-in home.
    body = body.replace('<a href="index.html" class="hover:text-ink">Home</a>',
                        '<a href="user-explore.html" class="hover:text-ink">Home</a>', 1)

    title = re.search(r"<title>(.*?)</title>", src).group(1)
    desc = re.search(r'<meta name="description" content="([^"]*)">', src).group(1)
    top, bottom = U.shell(title, desc, None)
    top = top.replace("generated by pages/_user.py from the goldenpi.com capture of 2026-09-26.",
                      "generated by pages/_refer.py from refer-and-earn.html and the staging capture "
                      "of 2026-10-01.", 1)
    # Refer & Earn is the current nav item, and points at this page.
    top = top.replace('<a class="gp-nav__link" href="refer-and-earn.html">',
                      '<a class="gp-nav__link" href="%s" aria-current="page">' % OUT, 1)
    # The reward card's tilt script follows the footer on the source page.
    tilt = re.search(r"<script>\n// Reward card tilts.*?</script>\n", src, re.S).group(0)
    bottom = bottom.replace("</body>", tilt + "</body>", 1)

    page = top + body + bottom
    with open(os.path.join(HERE, OUT), "w", encoding="utf-8") as f:
        f.write(page)
    print("%-36s %6d bytes" % (OUT, len(page)))


if __name__ == "__main__":
    main()
