#!/usr/bin/env python3
"""user-explore-app4.html: user-explore-app3's layout in GoldenPi's light scheme.

Same markup and sections as v3 (pages/_explore_app3.py), on the brand's cream page
(#f7f5f2) with white panels, near-black type and yellow-gold accents. The spotlight
deal stays the page's one black card. Figures that sit on light use the deep gold
(#a67c00) so they keep contrast; buttons are yellow (#edc967) or black pills.

    python3 pages/_explore_app4.py
"""
import os

import _explore_app as X
import _explore_app3 as V

OUT = os.path.join(X.HERE, "user-explore-app4.html")

LIGHT = """<style>
/* user-explore-app4: the light scheme over v3's tokens. */
.lx--light { --bg: #f7f5f2; --panel: #ffffff; --panel-2: #fbf9f4; --hair: rgba(50, 40, 17, .1); --gline: rgba(212, 175, 55, .45);
  --ink: #1d1a14; --sub: #5f5a50; --dim: #8a8478; --gold: #a67c00; }
.lx--light :focus-visible { outline-color: #a67c00; }
.lx--light .lx-btn--gold { color: #12100b; background: #edc967; }
.lx--light .lx-btn--gold:hover { background: #e4bb48; }
.lx--light .lx-btn--ink { color: #edc967; background: #12100b; }
.lx--light .lx-logo { border: 1px solid var(--hair); }

/* the spotlight keeps v3's dark tokens: the page's one black card */
.lx--light .lx-spot { --ink: #f4efe3; --sub: rgba(244, 239, 227, .6); --dim: rgba(244, 239, 227, .42); --hair: rgba(255, 255, 255, .08);
  --gold: #e2c372; color: var(--ink); border: 0;
  background: radial-gradient(70% 90% at 0% 0%, rgba(212, 175, 55, .2), transparent 60%), #12100b;
  box-shadow: 0 30px 60px -36px rgba(50, 40, 17, .55); }
.lx--light .lx-spot .lx-btn--gold { background: #e2c372; }
.lx--light .lx-spot .lx-logo { border: 0; }

.lx--light .lx-orders { box-shadow: 0 1px 2px rgba(50, 40, 17, .04); }
.lx--light .lx-orders h2 span { background: #edc967; }
.lx--light .lx-order__state--warn { color: #b25a00; }

.lx--light .lx-ipo { background: linear-gradient(90deg, rgba(237, 201, 103, .22), rgba(255, 255, 255, .6) 60%); }
.lx--light .lx-live { color: #06963c; }
.lx--light .lx-live i { background: #06963c; }

.lx--light .lx-segs { background: #fff; }
.lx--light .lx-seg[aria-selected="true"] { color: #12100b; background: #edc967; }
.lx--light .lx-row:hover { background: rgba(50, 40, 17, .03); }
.lx--light .lx-pill:hover { border-color: #d4af37; }

.lx--light .lx-stats { border-top-color: rgba(212, 175, 55, .55); }
.lx--light .lx-app { background: radial-gradient(80% 100% at 100% 0%, rgba(237, 201, 103, .25), transparent 60%), #fff; }
.lx--light .lx-app__qr { border: 1px solid var(--hair); }
</style>
"""


def main():
    X.assemble(V.body().replace('<main id="main-content" class="lx">', '<main id="main-content" class="lx lx--light">', 1), OUT,
               "Explore | GoldenPi",
               "pages/_explore_app4.py (user-explore-app3.html's layout in the light white / black / yellow scheme)",
               style=V.STYLE + LIGHT, script=V.SCRIPT)


if __name__ == "__main__":
    main()
