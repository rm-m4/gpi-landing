# signup

**Title:** Sign up

**Meta description:** Buy Bonds, Debentures & Fixed Income investments online in India. SEBI-registered debt broker and OBPP license holder.

**Source:** https://uatnew.goldenpi.com/signup

- [Skip to main content](#main-content)

<!-- section: gp-page-shell -->

- Invest Smarter.
- Earn Better.
- India’s trusted bond investment platform with returns up to 14%
- 16 lacs+Users
- SEBIRegistered
- ZeroDefault

### Get Started

- Sign in with Google
- or
- Continue
- [By continuing, you agree to our Privacy Policy & Terms & Conditions](/privacy-policy)

<!-- section: auth strings (hand-appended 2026-09-28) -->

## Auth strings, from the page's `auth` translation bundle

Read out of the RSC payload in `crawl/rendered/signup.html`. The live sign-up
**popup** (user-supplied screenshot, 2026-09-28) uses the plain keys; the
`/signup` **page** uses the `…Page` / `signInWithGoogle` / `continue` keys.

| Key | Popup | Page |
|---|---|---|
| Google button | Continue with Google | Sign in with Google |
| Input placeholder | Enter Phone Number or Email | Enter Mobile Number/Email |
| Input aria-label | Email or mobile number | Email or mobile number |
| CTA | Get OTP | Continue |
| Legal | By continuing, I agree <Privacy Policy> and <T&C> | By continuing, you agree to our <Privacy Policy> & <Terms & Conditions> |
| Form title | — | Get Started |

Shared: headline "Invest Smarter." / "Earn <highlight>Better.</highlight>";
tagline "India’s trusted bond investment platform with returns up to 14%";
divider "or"; trust "16 lacs+ Users" (alt "Illustration of GoldenPi users"),
"SEBI Registered" (alt "SEBI registered shield"), "Zero Default"
(alt "Zero default record"). Labels are `text-transform: capitalize`, so
"16 lacs+" renders "16 Lacs+".

### OTP step (shown after Get OTP; not captured by render, strings only)

- OTP Verification
- We’ve sent an OTP to {contact}
- Edit email or phone number (edit icon aria)
- One-time password (group label); OTP digit {position} (cell label)
- OTP valid for {time} mins
- Proceed / Verifying...
- Resend OTP / Resend OTP in {seconds}s / Resend limit reached
- Enter the complete OTP
- Login with password
