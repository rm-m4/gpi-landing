#!/usr/bin/env python3
"""Profile, new design, for web: two designer files (user, 2026-11-19),
kept as given in crawl/design/, become two pages.

  crawl/design/profile-v59.html        -> pages/profile2.html (desktop)
  crawl/design/profile-mobile-v22.html -> pages/profile-mobile2.html (phone)

The desktop design drops its own drawn navbar and sits in the site's logged-in
shell (portfolio.html's navbar; the login footer, put in by _build.py). Its
stylesheet is scoped under .pv so its resets (*, body, button) cannot reach
the shared navbar and footer. The phone design is an app screen with its own
top bar, so it stays whole. Both keep the design's Inter: that is the design.

Each gets the same small hover and press layer (MOTION), the taste-skill rule.

    python3 pages/_profile_v1.py && python3 pages/_build.py && python3 pages/_prototype.py && python3 pages/_web_v1.py
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.join(os.path.dirname(HERE), "crawl", "design")
SHELL = os.path.join(HERE, "portfolio.html")

ICONS = os.path.join(os.path.dirname(HERE), "assets", "img", "profile-icons")


def glyph(name, cls="rp-i"):
    """A Lucide glyph from taste-skill's icons.mjs (assets/img/profile-icons/ui-*.svg),
    inlined so it takes the text colour."""
    svg = open(os.path.join(ICONS, "ui-%s.svg" % name), encoding="utf-8").read().strip()
    svg = re.sub(r'\s(width|height)="24"', "", svg, count=2)
    return svg.replace("<svg ", '<svg class="%s" aria-hidden="true" focusable="false" ' % cls, 1)


def glyph_paths(name):
    """The drawing inside a Lucide glyph, for the design's own <symbol> sprite."""
    svg = open(os.path.join(ICONS, "ui-%s.svg" % name), encoding="utf-8").read()
    return svg[svg.index(">") + 1:svg.rindex("</svg>")]


# taste-skill motion layer (references/motion.md): a button steps 1px up on a
# fine-pointer hover and sinks 1px with scale .985 on press; 150ms in, 120ms out,
# 90ms press; one ease, cubic-bezier(.2,.8,.2,1). Colour changes ride the same timing.
MOTION = """
/* Hover and press layer (pages/_profile_v1.py; taste-skill motion.md). */
%(s)sbutton,%(s)sa,%(s)s.rp-chip>span{transition:background-color 120ms cubic-bezier(.2,.8,.2,1),color 120ms cubic-bezier(.2,.8,.2,1),border-color 120ms cubic-bezier(.2,.8,.2,1),box-shadow 120ms cubic-bezier(.2,.8,.2,1),transform 120ms cubic-bezier(.2,.8,.2,1)}
@media (hover:hover) and (pointer:fine){
  %(s)sbutton:hover,%(s)sa:hover,%(s)s.rp-chip>span:hover{transition-duration:150ms}
  %(s)s.btn:hover,%(s)s.dbtn:hover,%(s)s.cta:hover,%(s)s.nbtn:hover,%(s)s.rp-btn:hover{transform:translateY(-1px)}
}
%(s)s.btn:active,%(s)s.dbtn:active,%(s)s.cta:active,%(s)s.nbtn:active,%(s)s.rp-btn:active,%(s)s.ed:active,%(s)s.cp:active,%(s)s.addlink:active,%(s)s.addmore:active,%(s)s.rp-row:active,%(s)s.rp-chip:active>span{transform:translateY(1px) scale(.985);transition-duration:90ms}
@media (prefers-reduced-motion:reduce){
  %(s)sbutton,%(s)sa,%(s)s.rp-chip>span{transition-property:background-color,color,border-color}
  %(s)s.btn:hover,%(s)s.dbtn:hover,%(s)s.cta:hover,%(s)s.nbtn:hover,%(s)s.rp-btn:hover,%(s)s.btn:active,%(s)s.dbtn:active,%(s)s.cta:active,%(s)s.nbtn:active,%(s)s.rp-btn:active,%(s)s.ed:active,%(s)s.cp:active,%(s)s.addlink:active,%(s)s.addmore:active,%(s)s.rp-row:active,%(s)s.rp-chip:active>span{transform:none}
}
"""

# taste-skill system layer over the desktop design (references/system.md): text
# people read at 16px, one solid primary (no gradient button), glyphs in the text
# colour with 44px tap targets, one link look, spacing on the 4/8/12/16/24/32/48 scale.
SYSTEM_CSS = """
/* System layer (pages/_profile_v1.py; taste-skill system.md). */
.pv .head p,.pv .view p:not(.note){font-size:16px;line-height:24px}
.pv .main{padding-top:32px}
.pv .head{gap:8px}
.pv .head h1{margin-bottom:4px}
.pv .nbtn{width:auto;height:44px;padding:0 24px;background:#e6b325;color:var(--ink);font:600 16px Inter,system-ui,sans-serif;gap:8px}

.pv .lk:not(.danger),.pv .lnk{color:var(--gold-text);text-decoration:underline;text-decoration-color:rgba(138,100,0,.35);text-underline-offset:3px}
.pv .lk:not(.danger):hover,.pv .lnk:hover{text-decoration-color:currentColor}
.pv .lk.danger{text-decoration:underline;text-decoration-color:rgba(179,38,30,.35);text-underline-offset:3px}
.pv .lk.danger:hover{text-decoration-color:currentColor}
@media (max-width:999px){.pv .rp-toast{bottom:calc(86px + env(safe-area-inset-bottom,0px))}}  /* above the site's phone tab bar (navbar.css, 62px) */
@media (max-width:640px){
  .pv .main{padding-top:24px}
  .pv main#content{padding:24px 20px}
  .pv .grid,.pv .grid.c2,.pv .grid.c3,.pv .grid.c4,.pv .grid.c6{grid-template-columns:minmax(0,1fr);gap:20px}
  .pv .grid>*{grid-column:auto}
}
"""
PEN = '<symbol id="pen2" viewBox="0 0 24 24">%s</symbol>'  # Lucide pen-line (icons.mjs ui:pen-line), both pages
# The edit button: a 16px pen in the text colour, a 44px target that does not
# push the label's line taller (taste-skill: 44px taps, quiet glyphs).
ED_CSS = """
%(s)s.ed{display:inline-grid;place-items:center;width:44px;height:44px;margin:-12px -12px -12px -8px;padding:0;border:0;border-radius:12px;background:none;color:var(--ink-2,#514834);vertical-align:middle;cursor:pointer}
%(s)s.ed svg,%(s)s.ed svg.i{width:16px;height:16px}
%(s)s.ed:hover{background:#fbf4e1;color:var(--ink,#322811)}
%(s)s.ed:focus-visible{outline:2px solid var(--ink,#322811);outline-offset:-4px}
"""

# One masking rule for the whole profile (user, 2026-11-20): one mask character
# (•); an identifier shows its last four, after a fixed run of four (•••• 4321,
# as cards print it; the phone without +91); an email keeps its first two
# letters and its domain; a date of birth shows its year (•• ••• 1990). The
# father's or spouse's name is shown whole (user, 2026-11-20).
# DATA: the years and the name are samples (user's name; years assumed).
MASKS = (("ro•••••@gmail.com", "ro••••@gmail.com"), ("+91 ••••• •4321", "•••• 4321"),
         ("ABCDE••••F", "•••• 234F"), ("A/c XXXXX", "A/c •••• "), ("•••• •••• 9889", "•••• 9889"),
         ("HDFC0XXXXXX", "HDFC0••••••"), ("SBIN0XXXXXX", "SBIN0••••••"),
         ("[DD-MMM-YYYY]", "•• ••• 1990"), ("[DD MMM YYYY]", "•• ••• 1992"),
         ("[Full name]", "Rajat Kumar Sharma"))


def mask(text, name):
    for old, new in MASKS:
        text = text.replace(old, new)
    for left in ("A/c XXXX", "0XXXXXX", "[DD", "[Full", "••••• •", "••••••@"):
        need(left not in text, "%s: unmasked or off-pattern value %r left" % (name, left))
    return text


# Communication language: a value with the page's pen, edited in the reports'
# bottom sheet (one component), confirmed by the same toast (user, 2026-11-20).
LANGS = ("English", "हिन्दी (Hindi)")
LANG_PEN = '<svg class="i" aria-hidden="true"><use href="#pen2"/></svg>'


def lang_html():
    opts = "".join('<label class="rp-opt"><input type="radio" name="lang" value="%s"%s><span><b>%s</b></span></label>'
                   % (l, " checked" if k == 0 else "", l) for k, l in enumerate(LANGS))
    return ('<div class="k">Communication language <button type="button" class="ed" data-lang aria-haspopup="dialog" '
            'aria-label="Edit communication language">%s</button></div><div class="v" id="lang-v">%s</div>'
            '<div class="rp rp-lang"><dialog class="rp-sheet" aria-labelledby="lang-t">'
            '<div class="rp-grab" aria-hidden="true"></div>'
            '<div class="rp-sheet-h"><h3 id="lang-t" tabindex="-1" autofocus>Communication language</h3>'
            '<button type="button" class="rp-x" data-close aria-label="Close">%s</button></div>'
            '<fieldset class="rp-field"><legend class="rp-sr">Communication language</legend><div class="rp-langs">%s</div></fieldset>'
            '<button type="button" class="rp-btn rp-cta">Save language</button></dialog>'
            '<div class="rp-toast" role="status" aria-live="polite">%s<span class="rp-toast-t"></span>'
            '<button type="button" class="rp-toast-x" aria-label="Dismiss">%s</button></div></div>'
            % (LANG_PEN, LANGS[0], glyph("x"), opts, glyph("check"), glyph("x")))


LANG_SEL = r'<label class="k" for="lang">Communication language</label><select id="lang" class="sel(?: lang)?"><option>English</option><option>[^<]*</option></select>'

LANG_JS = """
// Communication language (pages/_profile_v1.py): the pen opens the sheet; Save
// sets the value and confirms in the toast. ?lang=1 opens it (review state).
(function () {
  var w = document.querySelector('.rp-lang'); if (!w) return;
  var sheet = w.querySelector('.rp-sheet'), v = document.getElementById('lang-v'), b = document.querySelector('[data-lang]'),
      toast = w.querySelector('.rp-toast'), tt;
  function open() { sheet.querySelectorAll('input').forEach(function (r) { r.checked = r.value === v.textContent; }); sheet.showModal(); }
  b.addEventListener('click', open);
  sheet.querySelector('[data-close]').addEventListener('click', function () { sheet.close(); });
  sheet.addEventListener('click', function (e) { if (e.target === sheet && e.clientY < sheet.getBoundingClientRect().top) sheet.close(); });
  sheet.addEventListener('close', function () { b.focus(); });
  sheet.querySelector('.rp-cta').addEventListener('click', function () {
    var r = sheet.querySelector('input:checked'); sheet.close();
    if (r.value === v.textContent) return;
    v.textContent = r.value;
    toast.querySelector('.rp-toast-t').textContent = 'Communication language changed to ' + r.value + '.';
    toast.classList.add('on'); clearTimeout(tt); tt = setTimeout(function () { toast.classList.remove('on'); }, 6000);
  });
  toast.querySelector('.rp-toast-x').addEventListener('click', function () { toast.classList.remove('on'); });
  if (new URLSearchParams(location.search).get('lang')) open();
})();
"""


# The phone page's screen header reads like the desktop page's at phone width:
# a plain back arrow, then the screen's name as its heading (user, 2026-11-20).
PBAR_CSS = """
.pbar{justify-content:flex-start;gap:4px;height:auto;min-height:44px;margin:16px 0 16px -10px}
.pback{position:static;transform:none;width:44px;height:44px;border:0;border-radius:12px;background:none;color:var(--ink,#322811)}
.pback:hover{background:#fbf4e1}
.pback svg{width:20px;height:20px}
.pbar h1{font:600 20px/28px Inter!important;color:var(--ink,#322811)}
"""


def contact_first(text, view, name):
    """Contact is the first block of User details (user, 2026-11-20)."""
    i = text.index(view); j = text.index("</section>", i)
    cards = text[i:j].split('<div class="card">')
    need(len(cards) == 4 and "<h2>Contact</h2>" in cards[2], "%s: User details cards not as expected" % name)
    cards[1], cards[2] = cards[2], cards[1]
    return text[:i] + '<div class="card">'.join(cards) + text[j:]


# Phones (the design's 920px breakpoint) work like profile-mobile-v22: the menu
# first, a section opens as its own screen with a back arrow (user, 2026-11-19).
# History entries make the phone's own Back return to the menu.
PHONE_CSS = """
/* Phones: menu first, each section its own screen (pages/_profile_v1.py). */
.pv .pv-back{display:none}
@media (max-width:920px){
  .pv .main:not(.is-open) > .bc,.pv .main:not(.is-open) > #content{display:none}
  .pv .main.is-open > .side{display:none}
  .pv .pv-back{display:inline-flex;align-items:center;gap:8px;min-height:44px;margin:0 0 8px -8px;padding:0 8px;border-radius:12px;color:var(--ink);font:600 16px/24px Inter,system-ui,sans-serif}
  .pv .pv-back .rp-i{width:20px;height:20px}
  .pv .pv-back{margin:0 0 16px -8px;font:600 20px/28px Inter,system-ui,sans-serif;text-align:left}
  .pv .view .head h1{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
  .pv .view .crumbs2{display:none}
}
"""
PHONE_JS = """
(function () {
  var phone = matchMedia('(max-width:920px)'), main = document.querySelector('.main');
  function openScreen(push) {
    if (!phone.matches || main.classList.contains('is-open')) return;
    main.classList.add('is-open');
    if (push) history.pushState({ pv: 1 }, '');
    window.scrollTo(0, 0);
  }
  function hub() { main.classList.remove('is-open'); window.scrollTo(0, 0); }
  $$('.side [data-go]').forEach(function (b) { b.addEventListener('click', function () { openScreen(true); }); });
  document.querySelector('[data-hub]').addEventListener('click', function () {
    if (history.state && history.state.pv) history.back(); else hub();
  });
  addEventListener('popstate', function () { if (!(history.state && history.state.pv)) hub(); });
  // the back row reads as the open screen's heading (user, 2026-11-20)
  var back = document.querySelector('[data-hub]'), backT = back.querySelector('.pv-back-t');
  function label() { var h = document.querySelector('.view.on .head h1'); backT.textContent = h ? h.textContent : 'Profile'; }
  new MutationObserver(label).observe(main, { subtree: true, attributes: true, attributeFilter: ['class'] });
  label();
  if (new URLSearchParams(location.search).get('view')) openScreen(false);
})();
"""


# ------------------------------------------------ reports and documents
# profile-mobile-v22's pattern on both pages (user, 2026-11-19): two lists,
# Investment reports and Important documents. A report row opens a bottom sheet:
# file type (real file icons, no text), time period (a field that opens in place,
# the four periods the user gave), how to get it (Download or Email), then ONE
# primary button that says what happens: Download Now, or Request report with the
# email line. Confirming closes the sheet and shows a toast. Report and document
# names, the masked email, "Request report" and the request toast are the
# design's own. One block, so both pages carry the same component.
REPORTS = ["Portfolio holdings", "Cashflow statement", "Transaction summary"]
DOCS = ["KYC application form", "AGTS report (FY 2025–26)"]
PERIODS = [("Previous financial year", "2025–26"), ("Current financial year", "2026–27"),
           ("All time", ""), ("Last 30 days", "")]
FY_DEFAULT = 1
# file type -> its icon from icons.mjs (file set, vscode-icons, MIT). No permitted
# set has a CSV icon, so CSV takes the plain-text file icon (a CSV is plain text).
FORMATS = [("Excel", "excel.svg"), ("PDF", "pdf2.svg"), ("CSV", "text.svg")]
FMT_DEFAULT = "PDF"
CTA = "Download Now"
# DATA: the user's ID, the sample the user gave; replaces the design's client ID + KYC line.
USER_LINE = ("Client ID RS20XXXXX · KYC verified", "ID: RM1234")
SELP = r'\s*<button class="selp"[^>]*>Selected profile <svg[^>]*><use href="#down"/></svg></button>'


def period(p):
    return "%s (%s)" % p if p[1] else p[0]


def reports_html():
    chev, dl = glyph("chevron-right"), glyph("download")
    rows = "".join('<li><button type="button" class="rp-row" data-report="%s" aria-haspopup="dialog">'
                   '<span class="rp-row-t">%s</span>%s</button></li>\n' % (r, r, chev) for r in REPORTS)
    docs = "".join('<li><button type="button" class="rp-row" data-doc="%s" aria-label="Download %s">'
                   '<span class="rp-row-t">%s</span>%s</button></li>\n' % (d, d, d, dl) for d in DOCS)
    fmts = "".join('<label class="rp-chip" title="%s"><input type="radio" name="rp-fmt" value="%s"%s>'
                   '<span><img src="../assets/img/profile-icons/%s" alt="" width="28" height="28">'
                   '<span class="rp-sr">%s</span></span></label>'
                   % (label, label, " checked" if label == FMT_DEFAULT else "", icon, label)
                   for label, icon in FORMATS)
    opts = "".join('<label class="rp-opt"><input type="radio" name="rp-fy" value="%s"%s><span><b>%s</b>%s</span></label>'
                   % (period(p), " checked" if k == FY_DEFAULT else "", p[0], "<small>%s</small>" % p[1] if p[1] else "")
                   for k, p in enumerate(PERIODS))
    return ('<div class="rp">\n'
            '<section class="rp-group" aria-labelledby="rp-h-reports"><h2 id="rp-h-reports">Investment reports</h2>\n'
            '<ul class="rp-list" role="list">\n%(rows)s</ul></section>\n'
            '<section class="rp-group" aria-labelledby="rp-h-docs"><h2 id="rp-h-docs">Important documents</h2>\n'
            '<ul class="rp-list" role="list">\n%(docs)s</ul></section>\n'
            '<dialog class="rp-sheet" aria-labelledby="rp-sheet-t">\n'
            '  <div class="rp-grab" aria-hidden="true"></div>\n'
            '  <div class="rp-sheet-h"><h3 id="rp-sheet-t" tabindex="-1" autofocus>%(first)s</h3>'
            '<button type="button" class="rp-x" data-close aria-label="Close">%(x)s</button></div>\n'
            '  <div class="rp-field"><div class="rp-lbl" id="rp-fy-l">Choose time period</div>\n'
            '  <details class="rp-fy"><summary aria-describedby="rp-fy-l"><span class="rp-fy-v">%(fy)s</span>%(down)s</summary>\n'
            '    <fieldset><legend class="rp-sr">Choose time period</legend>%(opts)s</fieldset></details></div>\n'
            '  <fieldset class="rp-field rp-field-fmt"><legend class="rp-lbl">File type</legend><div class="rp-chips">%(fmts)s</div></fieldset>\n'
            '  <button type="button" class="rp-btn rp-cta"><span class="rp-cta-t">%(cta)s</span></button>\n'
            '</dialog>\n'
            '<!-- DATA: the toast confirms the request in this prototype; in the app it shows once the server accepts it. -->\n'
            '<div class="rp-toast" role="status" aria-live="polite">%(check)s<span class="rp-toast-t"></span>'
            '<button type="button" class="rp-toast-x" aria-label="Dismiss">%(x)s</button></div>\n'
            '</div>' % dict(rows=rows, docs=docs, first=REPORTS[0], x=glyph("x"), fmts=fmts,
                            fy=period(PERIODS[FY_DEFAULT]), down=glyph("chevron-down"), opts=opts,
                            cta=CTA, check=glyph("check")))


RP_CSS = """
/* Reports and documents (pages/_profile_v1.py): one component on both pages:
   profile-mobile-v22's lists and report sheet, on taste-skill's system
   (16px reading text, 44px+ targets, one solid primary, spacing 4/8/12/16/24/32). */
.rp{--rp-ink:#322811;--rp-ink-2:#514834;--rp-muted:#6b665c;--rp-line:#ece7dd;--rp-div:#f2efe9;--rp-chip:#f3efe8;--rp-dark:#2e2615;--rp-gold:#e6b325;--rp-gold-soft:#fbf4e1;display:flex;flex-direction:column;gap:32px;color:var(--rp-ink);font-family:Inter,system-ui,sans-serif}
.rp *{box-sizing:border-box}
.rp ul{list-style:none;margin:0;padding:0}
.rp fieldset{border:0;margin:0;padding:0;min-width:0}
.rp-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.rp-i{width:20px;height:20px;flex:none}

/* the two lists: rows on the view's own edge, the hover tint bleeding 12px past it */
.rp-group h2{margin:0 0 8px;font:600 18px/26px Inter,system-ui,sans-serif;color:var(--rp-ink)}
.rp-list{margin:0 -12px}
.rp-list li+li{border-top:1px solid var(--rp-div)}
.rp-row{display:flex;align-items:center;gap:12px;width:100%;min-height:56px;margin:0;padding:0 12px;border:0;border-radius:12px;background:none;font:500 16px/24px Inter,system-ui,sans-serif;color:var(--rp-ink-2);text-align:left;cursor:pointer}
.rp-row-t{flex:1;min-width:0}
.rp-row .rp-i{color:var(--rp-muted)}
.rp-row:hover{background:#faf8f4;color:var(--rp-ink)}
.rp-row:hover .rp-i{color:var(--rp-ink)}
.rp-row:focus-visible{outline:2px solid #b38600;outline-offset:-2px}

/* the report sheet */
.rp .rp-sheet{position:fixed;inset:auto 0 0 0;width:100%;max-width:480px;max-height:92vh;margin:0 auto;overflow:auto;border:0;border-radius:24px 24px 0 0;padding:8px 24px calc(24px + env(safe-area-inset-bottom));background:#fff;color:var(--rp-ink);box-shadow:0 -8px 32px rgba(20,16,8,.18)}
.rp .rp-sheet[open]{animation:rp-up 240ms cubic-bezier(.22,1,.36,1)}
.rp .rp-sheet::backdrop{background:rgba(20,16,8,.45)}
@keyframes rp-up{from{transform:translateY(100%)}}
.rp-grab{width:40px;height:4px;border-radius:4px;background:#e3ddd1;margin:0 auto 16px}
.rp-sheet-h{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-bottom:24px}
.rp-sheet h3{margin:0;font:600 20px/28px Inter,system-ui,sans-serif}
.rp-sheet h3:focus{outline:none}  /* focus lands on the title when the sheet opens; no ring on a heading */
.rp-lang{display:contents}
.rp-langs{border:1px solid var(--rp-line);border-radius:14px;padding:0 16px}
.rp-x{display:grid;place-items:center;width:44px;height:44px;margin:-8px -12px -8px 0;border:0;border-radius:12px;background:none;color:var(--rp-muted);cursor:pointer}
.rp-x:hover{background:var(--rp-chip);color:var(--rp-ink)}
.rp-x:focus-visible{outline:2px solid var(--rp-ink);outline-offset:2px}
.rp-field{margin:0 0 24px!important}
.rp-lbl{display:block;margin:0 0 8px;padding:0;font:500 14px/20px Inter,system-ui,sans-serif;color:var(--rp-muted)}

.rp-chips{display:flex;gap:8px}
.rp-chip{position:relative}
.rp-chip input{position:absolute;opacity:0;width:1px;height:1px}
.rp-chip>span{display:grid;place-items:center;width:52px;height:44px;border:1px solid var(--rp-line);border-radius:12px;background:#fff;cursor:pointer}
.rp-chip img{width:22px;height:22px;display:block}
.rp-chip>span:hover{border-color:#d9d1bf}
.rp-chip input:checked+span{border:1.5px solid var(--rp-dark);background:var(--rp-gold-soft)}
.rp-chip input:focus-visible+span{outline:2px solid var(--rp-ink);outline-offset:2px}

.rp-fy{border:1px solid var(--rp-line);border-radius:14px}
.rp-fy:hover,.rp-fy[open]{border-color:#d9d1bf}
.rp-fy summary{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:52px;padding:0 16px;list-style:none;cursor:pointer;border-radius:14px;font:500 16px/24px Inter,system-ui,sans-serif}
.rp-fy summary::-webkit-details-marker{display:none}
.rp-fy summary:focus-visible{outline:2px solid var(--rp-ink);outline-offset:2px}
.rp-fy summary .rp-i{color:var(--rp-muted)}
.rp-fy[open] summary .rp-i{transform:rotate(180deg)}
.rp-fy fieldset{padding:0 16px 4px;border-top:1px solid var(--rp-div)}
.rp-opt{display:flex;gap:12px;padding:12px 0;cursor:pointer}
.rp-opt+.rp-opt{border-top:1px solid var(--rp-div)}
.rp-opt input{appearance:none;-webkit-appearance:none;width:22px;height:22px;margin:1px 0 0;border-radius:50%;border:2px solid #8a8273;flex:none;display:grid;place-items:center;cursor:pointer}
.rp-opt input:checked{border-color:var(--rp-dark)}
.rp-opt input:checked::after{content:"";width:10px;height:10px;border-radius:50%;background:var(--rp-dark)}
.rp-opt input:focus-visible{outline:2px solid var(--rp-ink);outline-offset:2px}
.rp-opt b{display:block;font:500 16px/24px Inter,system-ui,sans-serif}
.rp-opt small{font:500 13px/20px Inter,system-ui,sans-serif;color:var(--rp-muted)}


.rp .rp-btn{display:flex;align-items:center;justify-content:center;gap:8px;width:100%;height:52px;margin:0;border-radius:999px;border:0;background:var(--rp-gold);font:600 16px Inter,system-ui,sans-serif;color:var(--rp-ink);cursor:pointer}
.rp .rp-btn:hover{background:#d9a71c}
.rp .rp-btn:focus-visible{outline:2px solid var(--rp-ink);outline-offset:2px}

.rp-toast{position:fixed;left:16px;right:16px;bottom:24px;max-width:448px;margin:0 auto;display:flex;align-items:flex-start;gap:12px;padding:16px 8px 16px 16px;border-radius:16px;background:#1f7a45;color:#fff;font:500 15px/22px Inter,system-ui,sans-serif;box-shadow:0 8px 24px rgba(20,16,8,.22);opacity:0;transform:translateY(12px);transition:opacity 200ms cubic-bezier(.2,.8,.2,1),transform 200ms cubic-bezier(.2,.8,.2,1);visibility:hidden;z-index:30}
.rp-toast.on{opacity:1;transform:none;visibility:visible}
.rp-toast>.rp-i{margin-top:1px}
.rp-toast-t{flex:1}
.rp-toast-x{display:grid;place-items:center;width:44px;height:44px;margin:-12px 0 -12px 0;border:0;border-radius:12px;background:none;color:#fff;cursor:pointer}
.rp-toast-x:hover{background:rgba(255,255,255,.14)}
.rp-toast-x:focus-visible{outline:2px solid #fff;outline-offset:-2px}

@media (max-width:640px){.rp .rp-sheet{padding:8px 16px calc(16px + env(safe-area-inset-bottom))}}
@media (prefers-reduced-motion:reduce){.rp .rp-sheet[open]{animation:none}.rp-toast{transition:opacity 120ms linear;transform:none}}
"""

RP_JS = """
// Reports and documents (pages/_profile_v1.py). The files do not exist here, so
// each action confirms in the toast; the developers wire the real calls.
// ?view=reports&sheet=1 opens the first report's sheet,
// &toast=1 shows the confirmation (review states, as the design's ?view= does).
(function () {
  var rp = document.querySelector('.rp:not(.rp-lang)'); if (!rp) return;
  var sheet = rp.querySelector('.rp-sheet'), title = sheet.querySelector('#rp-sheet-t'),
      fy = sheet.querySelector('.rp-fy'), fyv = sheet.querySelector('.rp-fy-v'),
      cta = sheet.querySelector('.rp-cta'),
      toast = rp.querySelector('.rp-toast'), toastT = toast.querySelector('.rp-toast-t'), from = null, tt;
  function say(s) {
    toastT.textContent = s; toast.classList.add('on'); clearTimeout(tt);
    tt = setTimeout(function () { toast.classList.remove('on'); }, 6000);
  }
  toast.querySelector('.rp-toast-x').addEventListener('click', function () { toast.classList.remove('on'); });
  function picked(name) { return sheet.querySelector('input[name=' + name + ']:checked'); }
  function open(b) { from = b; title.textContent = b.dataset.report; fy.open = false; sheet.showModal(); }
  rp.querySelectorAll('[data-report]').forEach(function (b) { b.addEventListener('click', function () { open(b); }); });
  sheet.querySelectorAll('input[name=rp-fy]').forEach(function (r) {
    r.addEventListener('change', function () { fyv.textContent = r.value; });
    // a pointer pick closes the field; arrow keys keep it open while choosing
    r.addEventListener('click', function (e) { if (e.detail) { fy.open = false; fy.querySelector('summary').focus(); } });
  });
  cta.addEventListener('click', function () {
    var name = title.textContent, fmt = picked('rp-fmt').value;
    sheet.close();
    say(name + ' (' + fmt + ', ' + fyv.textContent + ') is downloading.');
  });
  sheet.querySelector('[data-close]').addEventListener('click', function () { sheet.close(); });
  sheet.addEventListener('click', function (e) {  // a tap on the scrim, not on the sheet's own padding
    if (e.target === sheet && e.clientY < sheet.getBoundingClientRect().top) sheet.close();
  });
  sheet.addEventListener('close', function () { if (from) from.focus(); from = null; });
  rp.querySelectorAll('[data-doc]').forEach(function (b) { b.addEventListener('click', function () { say(b.dataset.doc + ' is downloading.'); }); });
  var q = new URLSearchParams(location.search);
  if (q.get('sheet')) open(rp.querySelector('[data-report]'));
  if (q.get('toast')) say(REPORT_TOAST);
})();
""".replace("REPORT_TOAST", "'Portfolio holdings (PDF, Current financial year (2026–27)) is downloading.'")
BACK = ('<button type="button" class="pv-back" data-hub aria-label="Back to profile">'
        + glyph("arrow-left") + '<span class="pv-back-t">Profile</span></button>')

# Section names (user, 2026-11-19), wherever the design shows them: the menu,
# each screen's heading, the nominee steps' crumb and the script that sets it.
RENAME = ((">Demat<", ">Demat details<"), ("Bond nomination", "Nominee details"),
          ("Bank account details", "Bank accounts"))


def rename(text, name):
    for old, new in RENAME:
        need(old in text, "%s: %r not found" % (name, old))
        text = text.replace(old, new)
    return text


def need(cond, msg):
    if not cond:
        raise SystemExit("_profile_v1.py: " + msg)


def between(text, a, b):
    i = text.index(a) + len(a)
    return text[i:text.index(b, i)]


def scope_sel(sel, s):
    sel = sel.strip()
    if sel in (":root", "html", "body", "*"):
        return s if sel != "*" else s + " *"
    sel = re.sub(r"^(?:html|body|:root)\b", s, sel)
    return sel if sel.startswith(s) else "%s %s" % (s, sel)


def scope(css, s):
    """Prefix every selector with s; @media is walked, @keyframes left alone."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)  # a comment before a selector would hide it from the prefix
    out, i = [], 0
    while i < len(css):
        j = css.find("{", i)
        if j < 0:
            out.append(css[i:])
            break
        head = css[i:j]
        depth, k = 1, j + 1
        while depth:
            depth += {"{": 1, "}": -1}.get(css[k], 0)
            k += 1
        body = css[j + 1:k - 1]
        h = head.strip()
        lead = head[:len(head) - len(head.lstrip())]
        if h.startswith("@media") or h.startswith("@supports"):
            out.append("%s%s{%s}" % (lead, h, scope(body, s)))
        elif h.startswith("@"):
            out.append(head + "{" + body + "}")
        else:
            out.append("%s%s{%s}" % (lead, ",".join(scope_sel(x, s) for x in h.split(",")), body))
        i = k
    return "".join(out)


def desktop():
    src = open(os.path.join(DESIGN, "profile-v59.html"), encoding="utf-8").read()
    need(src.count("<style>") == 1, "profile-v59: expected one <style>")
    css = between(src, "<style>", "</style>")
    # The design's drawn navbar is replaced by the site's, so its styles go too.
    css, n = re.subn(r"/\* navbar \*/.*?(?=/\* layout \*/)", "", css, count=1, flags=re.S)
    need(n == 1, "profile-v59: navbar styles not found")
    body = between(src, "<body>", "</body>")
    body, n1 = re.subn(r'<a class="skip" href="#content">[^<]*</a>\n', "", body, count=1)
    body, n2 = re.subn(r'<nav class="nav" aria-label="Main">.*?</nav>\n\n', "", body, count=1, flags=re.S)
    need(n1 == n2 == 1, "profile-v59: skip link or navbar not found")
    need('<main id="content" tabindex="-1">' in body, "profile-v59: #content not found")
    body = body.replace('<main id="content" tabindex="-1">', '<main id="content" tabindex="-1">' + BACK, 1)
    body = body[:body.rindex("</script>")] + PHONE_JS + RP_JS + LANG_JS + body[body.rindex("</script>"):]
    body, n = re.subn(r'(<section class="view" id="reports">\s*<div class="head">.*?</div></div>\n)\s*<div class="card">.*?(?=\n\s*</section>)',
                      lambda m: m.group(1) + reports_html(), body, count=1, flags=re.S)
    need(n == 1, "profile-v59: reports view not found")
    # Printed [placeholders] read as unfinished (taste-skill: no placeholder): KYC
    # values masked by the page's one rule (MASKS), an unknown broker as the
    # page's own dash.
    need("[Broker name]" in body, "profile-v59: [Broker name] not found")
    body = mask(body.replace("[Broker name]", "—"), "profile-v59")
    body, n = re.subn(LANG_SEL, lambda m: lang_html(), body, count=1)
    need(n == 1, "profile-v59: language select not found")
    body = contact_first(body, '<section class="view on" id="personal">', "profile-v59")
    # Under the name: the user ID alone, no client ID or KYC line (user, 2026-11-19).
    body = rename(body, "profile-v59")
    need(USER_LINE[0] in body, "profile-v59: client ID line not found")
    body = body.replace(*USER_LINE)
    body, n = re.subn(SELP, "", body, count=1)  # no profile switcher (user, 2026-11-19)
    need(n == 1, "profile-v59: Selected profile control not found")
    # No breadcrumb, and each sub-screen shows its heading alone (user, 2026-11-19).
    body, n = re.subn(r'\s*<nav class="bc" aria-label="Breadcrumb">.*?</nav>', "", body, count=1, flags=re.S)
    need(n == 1, "profile-v59: breadcrumb not found")
    body = body.replace("if(it) document.getElementById('bc-cur').textContent=it.textContent;",
                        "if(it && document.getElementById('bc-cur')) document.getElementById('bc-cur').textContent=it.textContent;")
    need("if(it && document.getElementById('bc-cur'))" in body, "profile-v59: breadcrumb script line not found")
    body, n = re.subn(r'(</h1>)<p>[^<]*</p>', r'\1', body)
    need(n == 8, "profile-v59: expected 8 sub-screen descriptions, found %d" % n)
    # No href="#": SCORES goes to the address the goldenpi.com capture links
    # (content/prod_footer.md); in-page actions are buttons, so they say what they
    # are to a screen reader.
    for old, new in (('<a class="lk" href="#">SCORES</a>', '<a class="lk" href="https://scores.sebi.gov.in/" rel="noopener" target="_blank">SCORES</a>'),):
        need(old in body, "profile-v59: %s not found" % old)
        body = body.replace(old, new)
    body, n = re.subn(r'<a (class="(?:nbtn|lk danger|btn p lg)") href="#"((?: data-go="[a-z]+")?)>(.*?)</a>',
                      r'<button type="button" \1\2>\3</button>', body)
    need(n == 5, "profile-v59: expected 5 in-page actions, found %d" % n)
    need('href="#"' not in body.replace('href="#content"', ""), "profile-v59: a href=\"#\" is left")
    # The gold-gradient pencil becomes Lucide's (icons.mjs), drawn in the text colour.
    body, n = re.subn(r'<symbol id="pen2" [^>]*>.*?</symbol>', lambda m: PEN % glyph_paths("pen-line"), body, count=1, flags=re.S)
    need(n == 1, "profile-v59: pen2 glyph not found")

    shell = open(SHELL, encoding="utf-8").read()
    m = re.search(r'<!-- =+ header -->\n<div class="nb-slot">\n.*?</header>\n</div>\n', shell, re.S)
    need(m, "portfolio.html: navbar not found")
    nav = m.group(0).replace(" is-current", "").replace(' aria-current="page"', "")
    # The shared navbar and footer are built on Tailwind's base (box-sizing and the
    # rest of its preflight); every logged-in page loads it, so this one does too.
    t = re.search(r'<script src="https://cdn\.tailwindcss\.com"></script>\n<script>\n  tailwind\.config = .*?</script>', shell, re.S)
    need(t, "portfolio.html: Tailwind block not found")
    tailwind = t.group(0)
    page = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Profile | GoldenPi</title>
<!-- Post-login page, generated by pages/_profile_v1.py from crawl/design/profile-v59.html. -->
<!-- DATA: every name, number and account on this page is the design's sample. -->
<meta name="description" content="Your GoldenPi profile.">
<link rel="icon" href="../assets/img/goldenpi-logo.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700,900&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="../assets/site.css">
<link rel="stylesheet" href="../assets/final.css">
<link rel="stylesheet" href="../assets/user.css">
%s
<link rel="stylesheet" href="../assets/navbar.css">
<style>
/* The design's own stylesheet, scoped under .pv (pages/_profile_v1.py). */
%s
%s%s%s%s</style>
</head>
<body>

<a class="gp-skip" href="#content">Skip to main content</a>

%s
<div class="pv">
%s
</div>

<!-- ============================================================== footer -->
<footer class="ft"></footer>

</body>
</html>
""" % (tailwind, scope(css, ".pv"), MOTION % {"s": ".pv "}, SYSTEM_CSS + PHONE_CSS, RP_CSS, ED_CSS % {"s": ".pv "}, nav, body.strip())
    open(os.path.join(HERE, "profile2.html"), "w", encoding="utf-8").write(page)


def mobile():
    src = open(os.path.join(DESIGN, "profile-mobile-v22.html"), encoding="utf-8").read()
    need(src.count("</style>") == 1, "profile-mobile-v22: expected one <style>")
    page = src.replace("<title>Profile – GoldenPi</title>",
                       "<title>Profile | GoldenPi</title>\n<!-- Phone page, generated by pages/_profile_v1.py "
                       "from crawl/design/profile-mobile-v22.html. -->\n"
                       '<meta name="description" content="Your GoldenPi profile.">\n'
                       '<link rel="icon" href="../assets/img/goldenpi-logo.svg">', 1)
    page = page.replace("</style>", MOTION % {"s": ""} + RP_CSS + ED_CSS % {"s": ""} + PBAR_CSS + "</style>", 1)
    page = mask(page, "profile-mobile-v22")
    page, n = re.subn(LANG_SEL, lambda m: lang_html(), page, count=1)
    need(n == 1, "profile-mobile-v22: language select not found")
    page = contact_first(page, '<section class="view" id="user">', "profile-mobile-v22")
    page, n = re.subn(r'<symbol id="pen2" [^>]*>.*?</symbol>', lambda m: PEN % glyph_paths("pen-line"), page, count=1, flags=re.S)
    need(n == 1, "profile-mobile-v22: pen2 glyph not found")
    page = rename(page, "profile-mobile-v22")
    need(USER_LINE[0] in page, "profile-mobile-v22: client ID line not found")
    page = page.replace(*USER_LINE)
    page, n = re.subn(SELP, "", page, count=1)
    need(n == 1, "profile-mobile-v22: Selected profile control not found")
    # Each sub-screen shows its heading alone (user, 2026-11-19).
    page, n = re.subn(r'(<div class="pbody">)<p class="pd">[^<]*</p>', r'\1', page)
    need(n == 6, "profile-mobile-v22: expected 6 sub-screen descriptions, found %d" % n)
    # Reports and documents: the block replaces the list and its two bottom
    # sheets (and the script and toast that ran them).
    page, n1 = re.subn(r'(<section class="view" id="reports">.*?<div class="pbody">)<div class="panel">.*?</div>\n  <p class="note">[^<]*</p>(</div></section>)',
                       lambda m: m.group(1) + reports_html() + m.group(2), page, count=1, flags=re.S)
    page, n2 = re.subn(r'<div class="scrim" id="scrim"></div>\n.*?<div class="toast" id="toast".*?</div>\n', "", page, count=1, flags=re.S)
    page, n3 = re.subn(r"const scrim = .*?\n\n(?=function show)", "", page, count=1, flags=re.S)
    need(n1 == n2 == n3 == 1, "profile-mobile-v22: reports, sheets or their script not found")
    page = page[:page.rindex("</script>")] + RP_JS + LANG_JS + page[page.rindex("</script>"):]
    need(page != src and "pages/_profile_v1.py" in page, "profile-mobile-v22: <title> not found")
    open(os.path.join(HERE, "profile-mobile2.html"), "w", encoding="utf-8").write(page)


def selfcheck():
    got = scope("/* c */:root{--a:1}*{margin:0}body .x,a:hover{c:1}@media (max-width:9px){.y{c:2}}@keyframes k{to{o:1}}", ".pv")
    need(got == ".pv{--a:1}.pv *{margin:0}.pv .x,.pv a:hover{c:1}@media (max-width:9px){.pv .y{c:2}}@keyframes k{to{o:1}}",
         "scope() self-check failed: " + got)


if __name__ == "__main__":
    selfcheck()
    desktop()
    mobile()
    print("profile2.html, profile-mobile2.html")
