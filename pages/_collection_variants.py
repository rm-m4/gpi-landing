#!/usr/bin/env python3
"""collection-explore4.html: bond card colour variants, side by side.

No filter tabs. The same six bonds (from the Collections capture) in every
block, two rows each, so colour and intensity are the only thing that
changes. Each block says why the colour is there. Cards, shell and the
per-issuer --acc come from pages/_explore_bonds3.py.

    python3 pages/_collection_variants.py
"""
import os
import re

import _explore_bonds as X
import _explore_bonds3 as B

OUT = os.path.join(B.HERE, "collection-explore4.html")

# (key, name, why, swatches). The why is a design note for the reviewer,
# not product copy. Swatches name the fixed colours each block uses.
VARIANTS = [
    ("gold", "Brand gold, soft wash",
     "GoldenPi's own mustard at about 12%, fading to white. The safe default: every card reads "
     "as GoldenPi first and the issuer second, and it matches the gold rate and buttons.",
     ["#d4af37", "#f7efd6", "#a67c00"]),
    ("sage", "Sage, light",
     "The reference card. Green says growth and calm, and this muted sage stays clear of the "
     "brighter gain green (#06963c) the site already uses for positive numbers.",
     ["#dce9df", "#d5e5d9", "#5b4bb0"]),
    ("sage-deep", "Sage, deeper",
     "The same sage at about twice the strength, with a darker rule under the header. Use it when "
     "the cards have to separate more from the cream page background.",
     ["#c7dccc", "#a9c9b1", "#2f5a3b"]),
    ("slate", "Slate blue, cool",
     "Blue is the colour Indian investors read as bank and PSU. It suits the Government and Public "
     "Bank collections, and cools the warm page so the gold rate stands out more.",
     ["#e1e9f3", "#c9d7e8", "#2c4a72"]),
    ("issuer-quiet", "Issuer colour, quiet",
     "Each card takes its issuer's logo colour as an 8% wash and a tinted border, with no bar. "
     "Helps scan a long list by brand without turning the grid into a patchwork.",
     []),
    ("issuer-bold", "Issuer colour, bold",
     "What user-corporate-bonds3 ships now: a 6px bar and a 20% corner wash in the logo colour. "
     "Strongest brand recall, but six different colours per two rows gets busy.",
     []),
    ("ink", "Brand gold on ink",
     "The heading ink as a surface, as on the FD comparison card. The most premium read, and it "
     "suits one featured row; a whole grid of dark cards gets heavy on a light page.",
     ["#221b0c", "#e8c766", "#f4e9c8"]),
    ("hairline", "Bronze hairline, no fill",
     "The lowest intensity: white cards, no wash, only a bronze hairline and cream tags. The logos "
     "carry all the colour. Closest to a data table and the least decorated.",
     ["#ffffff", "#8a6520", "#f7f5f2"]),
]

STYLE = """<style>
/* collection-explore4: card colour variants. Base card is .gp-ucard
   (assets/final.css); each .cv--<key> block restyles colour only. */
.cv { padding: 40px 0 24px; }
.cv__title { margin: 0; color: var(--app-heading-color); font-size: clamp(26px, 3vw, 36px); font-weight: 700; line-height: 1.15; letter-spacing: -0.02em; }
.cv__lead { margin: 10px 0 0; max-width: 65ch; color: var(--subtext); font-size: 16px; line-height: 1.55; }
.cv__block { margin-top: 56px; padding-top: 32px; border-top: 1px solid #e7e3d9; }
.cv__head { display: grid; gap: 10px; margin-bottom: 24px; }
.cv__name { margin: 0; color: var(--app-heading-color); font-size: 22px; font-weight: 700; line-height: 1.25; }
.cv__why { margin: 0; max-width: 72ch; color: var(--subtext); font-size: 15px; line-height: 1.55; }
.cv__sw { display: flex; flex-wrap: wrap; gap: 8px; margin: 4px 0 0; padding: 0; list-style: none; }
.cv__sw li { display: inline-flex; align-items: center; gap: 8px; padding: 4px 10px 4px 4px; border: 1px solid #e7e3d9; border-radius: 999px; background: var(--white); color: #4a4a4a; font-size: 12px; font-weight: 500; font-variant-numeric: tabular-nums; }
.cv__sw i { width: 18px; height: 18px; border-radius: 50%; box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.08); }
.cv .gp-ucard { position: relative; }

/* Brand gold, soft */
.cv--gold .gp-ucard { border-color: #e9d9a6; background: linear-gradient(135deg, #f7efd6 0%, #fcf8ec 36%, var(--white) 64%); }
.cv--gold .gp-ucard__tags span { background: #f5ecd0; }
.cv--gold .gp-ucard:hover { border-color: #d4af37; }

/* Sage, light (the reference card) */
.cv--sage .gp-ucard { border-color: #d5e5d9; background: linear-gradient(135deg, #dce9df 0%, #f3f7f4 38%, var(--white) 62%); }
.cv--sage .gp-ucard__rate-value { color: #0a0a0a; }
.cv--sage .gp-ucard__rate-value span { color: #5b4bb0; }
.cv--sage .gp-ucard__tags span { background: #e2ece4; }
.cv--sage .gp-ucard:hover { border-color: #b9d3bf; box-shadow: 0 18px 32px -22px rgba(60, 110, 75, 0.45); }

/* Sage, deeper */
.cv--sage-deep .gp-ucard { border-color: #a9c9b1; background: linear-gradient(160deg, #c7dccc 0%, #e4eee6 45%, #f7faf8 100%); }
.cv--sage-deep .gp-ucard__metrics { padding-top: 18px; border-top: 1px solid #b9d3bf; }
.cv--sage-deep .gp-ucard__rate-value { color: #2f5a3b; }
.cv--sage-deep .gp-ucard__tags span { background: #fff; color: #2f5a3b; }
.cv--sage-deep .gp-ucard__metrics div + div { border-left-color: #b9d3bf; }
.cv--sage-deep .gp-ucard:hover { box-shadow: 0 18px 32px -20px rgba(47, 90, 59, 0.5); }

/* Slate blue, cool */
.cv--slate .gp-ucard { border-color: #c9d7e8; background: linear-gradient(135deg, #e1e9f3 0%, #f2f6fa 40%, var(--white) 66%); }
.cv--slate .gp-ucard__issuer { color: #1d2f48; }
.cv--slate .gp-ucard__tags span { background: #e6edf6; color: #2c4a72; }
.cv--slate .gp-ucard:hover { border-color: #9fb6d3; box-shadow: 0 18px 32px -20px rgba(44, 74, 114, 0.45); }

/* Issuer colour, quiet and bold: --acc is set per card from its logo */
.cv--issuer-quiet .gp-ucard, .cv--issuer-bold .gp-ucard { --a: var(--acc, #d4af37); }
.cv--issuer-quiet .gp-ucard {
  border-color: color-mix(in srgb, var(--a) 30%, #e7e3d9);
  background: radial-gradient(420px 200px at 0% 0%, color-mix(in srgb, var(--a) 8%, transparent), transparent 75%), var(--white);
}
.cv--issuer-quiet .gp-ucard__tags span { background: color-mix(in srgb, var(--a) 7%, #f7f5f2); }
.cv--issuer-quiet .gp-ucard:hover { border-color: color-mix(in srgb, var(--a) 55%, #e7e3d9); }
.cv--issuer-bold .gp-ucard {
  border-color: color-mix(in srgb, var(--a) 55%, #e7e3d9);
  background: radial-gradient(460px 220px at 0% 0%, color-mix(in srgb, var(--a) 20%, transparent), transparent 75%), var(--white);
  box-shadow: 0 10px 24px -18px color-mix(in srgb, var(--a) 70%, transparent);
}
.cv--issuer-bold .gp-ucard::before { content: ""; position: absolute; inset: 0 0 auto; height: 6px; background: var(--a); }
.cv--issuer-bold .gp-ucard__logo { background: var(--white); box-shadow: 0 0 0 1px color-mix(in srgb, var(--a) 40%, transparent); }
.cv--issuer-bold .gp-ucard__tags span { background: color-mix(in srgb, var(--a) 15%, #f7f5f2); }
.cv--issuer-bold .gp-ucard:hover { box-shadow: 0 18px 32px -20px color-mix(in srgb, var(--a) 80%, transparent); }

/* Brand gold on ink */
.cv--ink .gp-ucard {
  border-color: #3a2f16; color: #f4e9c8;
  background: radial-gradient(420px 200px at 100% 0%, rgba(212, 175, 55, 0.22), transparent 65%), #221b0c;
}
.cv--ink .gp-ucard__rate-value { color: #e8c766; }
.cv--ink .gp-ucard__metrics dt { color: rgba(244, 233, 200, 0.68); }
.cv--ink .gp-ucard__metrics div + div { border-left-color: rgba(244, 233, 200, 0.2); }
.cv--ink .gp-ucard__tags span { background: rgba(255, 248, 228, 0.1); color: #f4e9c8; }
.cv--ink .gp-ucard__logo { background: var(--white); }
.cv--ink .gp-ucard:hover { border-color: #8a6520; box-shadow: 0 18px 32px -18px rgba(34, 27, 12, 0.6); }

/* Bronze hairline, no fill */
.cv--hairline .gp-ucard { border: 1px solid rgba(138, 101, 32, 0.35); background: var(--white); }
.cv--hairline .gp-ucard__tags span { background: #f7f5f2; }
.cv--hairline .gp-ucard:hover { border-color: #8a6520; box-shadow: 0 14px 28px -22px rgba(138, 101, 32, 0.5); }

@media (max-width: 639px) {
  .cv { padding-top: 24px; }
  .cv__block { margin-top: 40px; padding-top: 24px; }
}
</style>
"""


def cards():
    """Six bonds from the first collection, each a different issuer with a
    logo colour and tags, without the note strip."""
    html = B.accents(X.explorer())
    out, seen = [], set()
    for c in re.findall(r'<a class="gp-ucard" .*?</a>', html, re.S):
        issuer = re.search(r'gp-ucard__issuer">([^<]+)<', c).group(1)
        if "--acc:" not in c or "gp-ucard__tags" not in c or issuer in seen:
            continue
        seen.add(issuer)
        out.append(re.sub(r'\n  <p class="gp-ucard__note">.*?</p>', "", c))
        if len(out) == 6:
            return "\n".join(out)
    raise SystemExit("fewer than six coloured, tagged bonds in the capture")


def block(key, name, why, sw, grid):
    chips = ""
    if sw:
        chips = ('\n      <ul class="cv__sw" aria-label="Colours used">%s</ul>'
                 % "".join('<li><i style="background:%s"></i>%s</li>' % (h, h) for h in sw))
    return '''    <section class="cv__block cv--%s" aria-labelledby="cv-%s">
      <div class="cv__head">
        <h2 class="cv__name" id="cv-%s">%s</h2>
        <p class="cv__why">%s</p>%s
      </div>
      <div class="ex__grid">
%s
      </div>
    </section>''' % (key, key, key, name, B.esc(why), chips, grid)


def main():
    grid = cards()
    body = ('  <!-- DATA: six bonds from the uatnew collections capture, repeated in every block. -->\n'
            '  <div class="cv gp-shell">\n'
            '    <h1 class="cv__title">Bond card colour variants</h1>\n'
            '    <p class="cv__lead">The same six bonds in every block, so colour and intensity are the only '
            'change. Each block notes why the colour fits and where it falls short.</p>\n'
            + "\n".join(block(*v, grid) for v in VARIANTS) +
            '\n  </div>')
    html = B.page(body, "Design exploration: bond card colour variants.", STYLE)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print("%s  %d bytes" % (os.path.relpath(OUT, B.ROOT), len(html)))


if __name__ == "__main__":
    main()
