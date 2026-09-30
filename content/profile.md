# /profile (logged in)

Source: `https://uatnew.goldenpi.com/profile`, captured 2026-09-30 with
`node crawl/profile_tabs.js` (clicks every sidebar item; needs the session from
`crawl/login.js`). The raw capture holds the account holder's details, so it is
written outside the repo and only this redacted transcription is tracked.

Labels, headings, helper copy and statuses below are verbatim. **Every value is a
placeholder**: personal values are replaced with the sample persona the Figma
file uses (Rohit Sharma); order and Form 121 rows keep the issuer, ISIN and
figures of the UAT test account, which are not personal.

Design: Figma `HRSMFFccdLgqf1YwD7oyc9`, section 21:2427. Frames: Demat desktop
21:1015 and mobile 21:1605, Nominee Details desktop 21:1688 and mobile 21:2199,
Add a new nominee (mobile) 21:979.

## Sidebar

Live, KYC completed: Selected Profile (switcher) / initials + name / User Details /
Demat / Personal Details / Investor Details / Bank / Exchange Details / Reports And
Documents / Account Closure / Orders / Portfolio / Form 121 Center / Logout.

Live, KYC not completed (user screenshot): User Details / Orders / Portfolio /
Form 121 Center / Logout.

Figma: Selected profile / photo + name / User Details / Demat / Reports and
documents / Nominee Details / Logout.

Routes: the items up to Account Closure swap a panel on `/profile`. Orders is
`/profile/orders`, Portfolio `/profile/portfolio`, Form 121 Center
`/profile/form121-center`. Below desktop width the live page shows the same items
as a horizontal tablist labelled "Profile navigation".

Built grouping (user's request, 2026-09-30): Personal Details and Investor Details
fold into User Details; Exchange Details folds into Demat; Nominee Details is added
from Figma.

## User Details

User Details
Manage your personal information and account preferences

### Profile
- name, then **KYC Completed** (green, tick) or **Complete KYC** (red, alert)
- Investor type: Resident Indian Citizen (not completed: "—", with an edit control)
- Password (edit): XXXXXXXXX
- MPIN (edit): XXXX
- Risk Appetite (edit): AGGRESSIVE
- Default Communication Language: dropdown, English selected (options not captured)

### Contact Details (edit)
- Mobile number: 91-XXXXX + last 5 digits, then "Phone Verified"
- Email: masked local part, then "Email Verified"

## Personal Details

Personal Details
View and update your personal information

### Personal Details (edit)
PAN (masked, XXXXXX + last 4) / DOB (d-Mon-yyyy) / Gender / Nationality /
Father/Spouse Name / Political Connection (No) / Resident Status / Address.
Empty values render as "--".

## Investor Details

Investor Details
Your investor profile and related information

### Investor Details (edit)
Income: 5-10 Lakhs / Occupation: Private Sector / Marital Status: Single

## Demat

Live: "Demat Account" / "Manage your Demat Account & information" / card "Demat
Details" (edit) with a "Default" badge: Demat Account Number, DP ID, Broker Name
(DP), Depository, Account Holder Name, PAN.

Figma (the finalised design, used for the build):

Demat Account, with an ACTIVE badge
Manage your GoldenPi Demat Account & account information

- Demat Account Number: 12081600XXXX1234 (copy)
- DP ID: 12081600 (copy)
- Broker Name (DP): GoldenPi Securities Pvt. Ltd.
- Depository: CDSL
- Account Type: Individual - Resident
- Account Holder Name: Rohit Sharma
- PAN: ECY******B
- Demat Linked Bank Account: XXXX XXXX 1234
- Your Demat account with us is lifetime free.
- Close Demat Account →

## Exchange Details

Exchange Details
Exchange and UCC information linked to your account

### Exchange Details
- UCC Number: (initials + 6 digits)@GSPL
- Exchange Enabled: BSE, NSE
- Download KYC Application Form (button)

## Bank

Bank
Manage your bank and virtual account details

### Bank Account Details (edit)
Each account: IFSC Code / Account Number (XXXXXXXX + last 6) / Bank Name. The
first carries a "Default" badge. Two accounts on the captured profile.

## Nominee Details (Figma only)

Nominee Details
Manage your nominee information for seamless transfers

- Jiya Sharma, tag "Minor", edit
- Date of Birth: 10 Dec 2017 / Relationship: Daughter / Allocation Percentage: 50%
- Add more nominees
- Add Nominee
- By proceeding you confirm these details are accurate. You will e-sign the
  nomination form using your registered mobile OTP.

Mobile, card title "Personal Details": Full Name / Relationship / Date Of Birth /
Allocation Percentage.

Empty state, screen title "Add Nominee":

Add a new nominee
You can add up to 3 nominees for your account.
Protect your investments for the future
Add a nominee so your bonds can be smoothly transferred to your chosen nominee when needed.
Add Nominee

## Reports And Documents

Reports And Documents
Download statements and documents

### Reports
- Report type: AGTS (Annual Global Transaction Statement) (only option)
- Financial year: 2025-2026 (Apr 2025 - Mar 2026) (only option)
- Download report

## Account Closure

Account Closure
Request permanent closure of your GoldenPi account

### Account Closure
Account closure is permanent and irreversible. [Close my account](mailto:contact-us@goldenpi.com,
subject "Account closure request: <UCC>", body "I request the GoldenPi team to
close my account with GoldenPi. I understand that this change will be irreversible.")

For any complaints, visit: [SCORES](https://scores.sebi.gov.in/scores-home)

## Orders (/profile/orders)

Orders. Tabs: IPO / Bonds / Fixed Deposit / Sovereign Gold Bonds (Bonds opens first).

### Bonds

Pending order (each: "Listed Asset" tag, logo, name, ISIN, Cancel; then "Select
your payment method. Continue"):

| Issuer | ISIN | Order Date | Investment | Units | Tenure | YTM | Status |
|---|---|---|---|---|---|---|---|
| NEOGROWTH | INE814O07634 | 28-Sep-2026 | ₹ 3,05,825.40 | 3 | 19 Months | 13% | Pending |
| BEST CAPITAL | INE04UP07246 | 28-Sep-2026 | ₹ 29,865.85 | 3 | 36 Months | 13% | Pending |

Order history (settled rows end with "Download Deal sheet"; Mamta has no Listed
Asset tag):

| Issuer | ISIN | Date | Investment | Units | Type | YTM / Yield | Status |
|---|---|---|---|---|---|---|---|
| AKARA | INE08XP07522 | 1-Oct-2026 | ₹ 1,00,169.51 | 1 | Buy | YTM 13% | Processing |
| MUTHOOT MCRED | INE101Q07BZ6 | 7-Jul-2026 | ₹ 9,932.77 | 1 | Buy | Yield 10.9% | Deal Settled |
| ADANI ENTERPRISES | INE423A07492 | 28-Apr-2026 | ₹ 1,007.92 | 1 | Buy | YTM 8.6% | Deal Settled |
| ADANI ENTERPRISES | INE423A07492 | 9-Apr-2026 | ₹ 1,003.51 | 1 | Buy | YTM 8.6% | Deal Settled |
| MAMTA PROJECTS PVT LTD | INE0GA407226 | 1-Feb-2023 | ₹ 2,98,050.00 | 3 | Buy | YTM 15.1% | Deal Settled |

### IPO

Online Orders. Each application: "Application no: …", issuer, Refresh, "Last
updated on" + timestamp, "Created on : " + timestamp, "CDSL: " + masked demat,
PAN Number, Total Investment, Total Units, UPI Handle, DP Status, Payment Status,
View series, Cancel Application, "IPO Closed".

| Application no | Issuer | Last updated on | Created on | Total Investment | Total Units | DP Status | Payment Status |
|---|---|---|---|---|---|---|---|
| 58216352 | INDEL MONEY LIMITED | 20-Aug-2026 9:30:12 AM | 18-Aug-2026 1:31:21 PM | ₹ 15,000.00 | 15 | Verification Successful | Approved By Bank |
| 57183205 | PAISALO DIGITAL LIMITED | 14-Aug-2026 9:30:08 AM | 10-Aug-2026 10:01:25 AM | ₹ 10,000.00 | 10 | Verification Successful | Approved By Bank |

Offline Orders: No orders found!

### Fixed Deposit

Pending order: UNITY SMALL FINANCE BANK, Refresh, Remove. Order Date 28-Sep-2026 /
Investment ₹ 5,000.00 / Tenure 501 D / Payout Mode On Maturity / Interest Rate 8% /
Status Pending. "Your order is pending. Pay now and complete your investment. Continue"

Order history:

- UNITY SMALL FINANCE BANK, "Payment Date: 3-Jun-2026 1:39:47 PM". Investment
  ₹ 1,000.00 / Tenure 7 D / Payout Mode On Maturity / Interest Rate 4% / Maturity
  Date 10-Jun-2026 / Maturity Amount ₹ 1,001.00 / Current Status FD Rejected.
  "Your FD is rejected and any amount deducted will be credited back in 4-5 business days."
  (two more identical-shaped rejected rows on the account)
- SHRIRAM FINANCE, "Booking Date: 2023-11-06". Investment ₹ 5,000.00 / Tenure 12 M /
  Payout Mode Yearly / Interest Rate 7.8% / Maturity Date 2024-11-06 / Maturity
  Amount ₹ 5,000.00 / Current Status FD Booked.
  "Click Here to know more about redemption and maturity of your FD."

### Sovereign Gold Bonds

Order history: No orders found!

## Form 121 Center (/profile/form121-center)

Form 121 Center, with a "SECURE & ENCRYPTED" badge
Stop TDS deductions on your bond interest — file in minutes.

₹72.82
AVOID TDS DEDUCTIONS
Eligible for Form 121? Submit your declaration to receive bond interest payouts without TDS deduction, subject to issuer approval.

PENDING FORM 121: 1 / DEADLINE: 31 Mar

| Issuer | ISIN | Investment | Coupon (Fixed) | Payout | Save Amount | State |
|---|---|---|---|---|---|---|
| ADANI ENTERPRISES LIMITED | INE423A07492 | ₹2,000 | 8.48% | Quarterly | ₹8.56 | "File Form 121" button, "NOT FILED TDS" |
| MUTHOOT MCRED LIMITED | INE101Q07BZ6 | ₹10,000 | 9.65% | Monthly | ₹64.26 | "SUBMITTED" |

Filing Form 121 does not guarantee exemption from TDS. GoldenPi only facilitates submission of the form to the issuer. Acceptance of the declaration and the final TDS decision are at the issuer's discretion.

### Frequently Asked Questions

**Why does this matter for you? SEO** / Real money, real impact
(the trailing "SEO" is on the UAT page as captured; it reads as a stray CMS token
and is left out of the build)

Say you invest ₹1,00,000 in a bond at 10% interest. That’s ₹10,000 in annual interest.

Without Form 121, the bond issuer deducts 10% TDS — you only receive ₹9,000. With Form 121 filed, you receive the full ₹10,000.

That difference compounds over time. Across multiple bonds over multiple years, it adds up to real money sitting in your pocket instead of waiting in a tax refund cycle.

**Who should file it?** / Check if you qualify

Form 121 is most useful if:

- Your total annual income is below ₹2.5 lakh (basic exemption limit)
- You fall under a lower tax slab and don't want TDS deducted upfront
- You prefer to manage your tax liability at filing time rather than through automatic deductions

Even if your income is above the exemption limit, filing Form 121 prevents unnecessary upfront deduction and improves your cash flow through the year.

**Is it complicated?** / Takes about 2 minutes

Not at all. GoldenPi pre-fills most of the form using your KYC details — your name, PAN, address, and contact information are already there. You only need to confirm a few income details and give your consent.

There are no physical documents to sign, no trips to an office, and no back-and-forth with the Bond Issuer. GoldenPi submits the form on your behalf.

**Ready to invest and file?** / Get started in one place

Browse bonds on GoldenPi, make your first investment, and file Form 121 right here — all in one place.
