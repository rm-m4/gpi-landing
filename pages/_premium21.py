#!/usr/bin/env python3
"""Write home-premium21.html: home-premium31's whole page, with its first fold
replaced by home-premium20's walk through the gate (2026-10-12), in a dark and a
light theme.

From home-premium20: the hero's styles (scoped to .st, without 20's page-wide
resets, skip link and overlay nav), its reduced-motion class script, the pinned
section and the three.js module. From home-premium31: everything else, with its
site navbar (synced by _build.py) as the one nav, and its sections after the hero.

Themes: dark is home-premium3's styles (the black hero runs into black sections);
light is 31's own white overrides, which key on body.h31, so the theme is that one
class. The hero has both too: in light, a daylit colonnade, a bright space past the
gate and ink copy (HERO_LIGHT_CSS, and the palette swap patched into 20's scene
script by light_scene()); it switches live with the toggle. The choice follows the system
setting until the visitor uses the toggle, which is then remembered; it is set by
an inline script at the top of <body>, before first paint, so neither theme
flashes. The toggle is added to the navbar by script, since _build.py rewrites
the navbar markup.

    python3 pages/_premium21.py && python3 pages/_build.py
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "home-premium21.html"


# Before first paint: the saved choice, else the system setting. h31 is the light theme.
THEME_BOOT = """<script>
(function () {
  var t = null;
  try { t = localStorage.getItem("gp-theme"); } catch (e) {}
  if (t !== "light" && t !== "dark") t = matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
  document.body.classList.toggle("h31", t === "light");
})();
</script>"""

THEME_CSS = """.gp-theme { display: inline-grid; place-items: center; width: 40px; height: 40px; margin-right: 10px; border-radius: 999px;
  border: 1px solid rgba(236,230,216,.28); background: transparent; color: #f4e9c8; font-size: 18px; cursor: pointer;
  transition: border-color .2s, background-color .2s, transform .15s; }
.gp-theme:hover { border-color: #d4af37; background: rgba(212,175,55,.12); }
.gp-theme:active { transform: scale(.94); }
.gp-theme:focus-visible { outline: 2px solid #f2d98a; outline-offset: 3px; }
.gp-theme .ph-sun, .h31 .gp-theme .ph-moon { display: none; }
.h31 .gp-theme .ph-sun { display: inline; }"""

# The toggle, put into the navbar's actions (the navbar is rewritten by _build.py).
THEME_JS = """<script>
(function () {
  var actions = document.querySelector(".nb__actions");
  if (!actions) return;
  var b = document.createElement("button");
  b.type = "button"; b.className = "gp-theme";
  b.innerHTML = '<i class="ph ph-moon" aria-hidden="true"></i><i class="ph ph-sun" aria-hidden="true"></i>';
  function label() {
    var light = document.body.classList.contains("h31");
    b.setAttribute("aria-label", light ? "Switch to dark theme" : "Switch to light theme");
    b.setAttribute("aria-pressed", String(light));
  }
  b.addEventListener("click", function () {
    var light = !document.body.classList.contains("h31");
    document.body.classList.toggle("h31", light);
    try { localStorage.setItem("gp-theme", light ? "light" : "dark"); } catch (e) {}
    label();
  });
  label();
  actions.insertBefore(b, actions.firstChild);
})();
</script>
"""


# The hero's copy, scrims and stage in the light theme.
HERO_LIGHT_CSS = """
/* light theme (home-premium21): the hero's copy in ink on a daylit scene */
.h31 .st { --ink: #e9e2d4; }
.h31 .st-copy::before { background: radial-gradient(42% 30% at 50% 52%, rgba(240,234,222,.78), transparent 100%); }
.h31 .st-a, .h31 .st-sub { color: #14120d; text-shadow: 0 1px 24px rgba(250,246,238,.8); }
.h31 .st-gold { color: #8a6520; }
.h31 .st-pill--line { color: #14120d; border-color: rgba(20,18,13,.3); background: rgba(255,255,255,.5); }
.h31 .st-pill--line:hover { border-color: #8a6520; }
.h31 .st-stage::after { opacity: .07; mix-blend-mode: multiply; }
"""


def light_scene(module):
    """Patch home-premium20's scene script with a light palette, applied whenever
    body.h31 is on (and re-applied live when the toggle flips it). Each patch
    must match exactly once, so a change in 20 fails loudly here."""
    def rep(a, b):
        nonlocal module
        if module.count(a) != 1:
            raise SystemExit("%s: home-premium20's scene changed near %r" % (OUT, a[:50]))
        module = module.replace(a, b)
    rep('s.add(new THREE.HemisphereLight(0x3d3322, 0x000000, .3));',
        'const hemi = new THREE.HemisphereLight(0x3d3322, 0x000000, .3); s.add(hemi);')
    rep('    render(p, dt) {', '''    // Theme: dark is 20's own; light is daylight stone and a bright space past the gate.
    theme(light) {
      const v = light
        ? { bg: 0xe9e2d4, near: 10, far: 56, exp: 1, sky: 0xfff6e6, ground: 0x8a7a60, hemi: 2.4, stone: 0xe4dccb, wall: 0xd9d0bf, hall: 0xf3ece0, floor: [3.4, 3.2, 2.85], env: 1.6 }  // floor > 1: it multiplies a dark tile texture
        : { bg: 0x050403, near: 6, far: 38, exp: .85, sky: 0x3d3322, ground: 0x000000, hemi: .3, stone: 0x8a806c, wall: 0x241f19, hall: 0x3a2c12, floor: [.6, .54, .45], env: .45 };
      s.background.setHex(v.bg); s.fog.color.setHex(v.bg); s.fog.near = v.near; s.fog.far = v.far;
      renderer.toneMappingExposure = v.exp;
      hemi.color.setHex(v.sky); hemi.groundColor.setHex(v.ground); hemi.intensity = v.hemi;
      stone.color.setHex(v.stone); wall.color.setHex(v.wall); bronze.color.setHex(v.hall); floor.material.color.setRGB(...v.floor); s.environmentIntensity = v.env;  // env: gold reflects a bright room by day
    },
    render(p, dt) {''')
    rep('  scene = build(THREE);', '''  scene = build(THREE);
  const light = () => document.body.classList.contains("h31");
  scene.theme(light());
  new MutationObserver(() => { scene.theme(light()); drawn = -1; wake(); if (!story) tick(performance.now()); })
    .observe(document.body, { attributes: true, attributeFilter: ["class"] });''')
    return module


def read(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return f.read()


def one(pattern, text, what, flags=re.S):
    m = re.findall(pattern, text, flags)
    if len(m) != 1:
        raise SystemExit("%s: expected one %s, found %d" % (OUT, what, len(m)))
    return m[0]


def hero_parts(src):
    css = one(r"<style>\n(.*?)</style>", src, "hero style block")
    keep = []
    for line in css.splitlines():
        if re.match(r"\s*(\* \{|body \{|a \{|\.st-skip|\.st-nav)", line):
            continue  # 20's page-wide resets and its own nav: 31 has both already
        keep.append(line)
    css = "\n".join(keep).replace(":root {", ".st {", 1)  # tokens scoped, so site.css's --ease stays its own
    head_js = one(r'(<script>if \(!matchMedia\("\(prefers-reduced-motion: reduce\)"\)\.matches\).*?</script>)', src, "js-story script")
    section = one(r'(<section class="st">.*?</section>)', src, "hero section")
    section, n = re.subn(r'\n    <header class="st-nav">.*?</header>', "", section, flags=re.S)
    section = section.replace('<main class="st-copy" id="st-main">', '<div class="st-copy">', 1).replace("    </main>\n", "    </div>\n", 1)
    if n != 1 or "<main" in section:
        raise SystemExit("%s: home-premium20's hero changed shape" % OUT)
    module = one(r'(<script type="module">.*?</script>)', src, "three.js module")
    return css, head_js, section, module


def main():
    css, head_js, section, module = hero_parts(read("home-premium20.html"))
    module = light_scene(module)
    css += HERO_LIGHT_CSS
    page = read("home-premium31.html")

    # 31's first fold out, 20's in.
    page, n = re.subn(r'  <!-- =+ chapter 1 · unveiling -->\n  <section class="h3-hero".*?</section>\n',
                      "  <!-- the first fold: home-premium20's walk through the gate -->\n  " + section + "\n", page, count=1, flags=re.S)
    if n != 1:
        raise SystemExit("%s: home-premium31's hero not found" % OUT)

    # 31's white block stays (it is the light theme, on body.h31); after it, what the
    # dark theme needs from it: the spaced card fan (31 scopes it to .h31), and the
    # duo's divider in gold rather than its light grey.
    i = page.index("/* home-premium31: white, black and gold.")
    j = page.index("</style>", i)
    fixes = [l.replace(".h31 ", ".h21 ") for l in page[i:j].splitlines() if "h3-fan" in l]
    fixes += [
        ".h21:not(.h31) .h31-duo > div + div { border-left-color: rgba(212,175,55,.16); }",
        ".h21 .h3-h2 { font-weight: 700; }  /* one type system: under the hero's 500-weight lines, 900 shouted */",
        THEME_CSS,
    ]
    page = page[:j] + "/* home-premium21: the dark theme's share of 31's fixes, and the theme toggle */\n" + "\n".join(fixes) + "\n" + page[j:]
    page = page.replace('<body class="h3-page h31">', '<body class="h3-page h21">\n' + THEME_BOOT, 1)
    k = page.rindex("</body>")
    page = page[:k] + THEME_JS + page[k:]

    page = page.replace("</head>", "%s\n<style>\n/* home-premium20's hero (pages/_premium21.py) */\n%s</style>\n</head>" % (head_js, css), 1)
    k = page.rindex("</body>")
    page = page[:k] + module + "\n" + page[k:]
    page = page.replace("<title>", "<!-- Generated by pages/_premium21.py from home-premium20 and home-premium31; edit those, not this. -->\n<title>", 1)

    with open(os.path.join(HERE, OUT), "w", encoding="utf-8") as f:
        f.write(page)
    print("wrote pages/" + OUT)


if __name__ == "__main__":
    main()
