#!/usr/bin/env python3
"""Pull GoldenPi's light-theme design tokens out of their compiled stylesheet.

Reads CSS on stdin, writes a single :root block on stdout.

Their sheet defines the same variable twice -- once for light, once for dark
(--app-page-bg is #f7f5f2 light / #1a1510 dark). Selector order alone is not
enough to tell them apart, so blocks are classified by selector and dark ones
are kept separately, emitted as comments for the later dark-theme pass.
"""
import re
import sys

# Core palette, emitted first and sanity-checked. Value = expected light value.
EXPECTED = {
    "--mustard": "#d4af37",
    "--app-page-bg": "#f7f5f2",
    "--app-heading-color": "#322811",
    "--white": "#fff",
}
CORE = [
    "--mustard", "--white", "--app-page-bg", "--app-heading-color", "--subtext",
    "--bg-light", "--light-stroke", "--background", "--foreground", "--card",
    "--card-foreground", "--muted", "--muted-foreground", "--border", "--primary",
    "--primary-foreground", "--accent", "--accent-foreground", "--ring",
]

DECL = re.compile(r"(--[A-Za-z0-9_-]+)\s*:\s*([^;}]+)")


def blocks(css):
    """Yield (selector, declaration-text) for every rule, at any nesting depth."""
    i, n, start = 0, len(css), 0
    stack = []
    while i < n:
        c = css[i]
        if c == "{":
            sel = css[start:i].strip().replace("\n", " ")
            stack.append((sel, i + 1))
            start = i + 1
        elif c == "}":
            if stack:
                sel, body_start = stack.pop()
                # strip nested rules so we only keep this block's own declarations
                body = re.sub(r"[^{}]*\{[^{}]*\}", "", css[body_start:i])
                yield sel, body
            start = i + 1
        i += 1


def is_dark(sel):
    return "data-theme=dark" in sel or re.search(r"\.dark\b", sel)


def is_light_root(sel):
    if is_dark(sel):
        return False
    return ":root" in sel or ":host" in sel or "data-theme=light" in sel


def main():
    css = sys.stdin.read()
    light, dark = {}, {}
    for sel, body in blocks(css):
        if is_light_root(sel):
            target = light
        elif is_dark(sel):
            target = dark
        else:
            continue
        for name, value in DECL.findall(body):
            target[name] = value.strip()

    # Variables defined once outside any :root block (e.g. --mustard on a utility
    # class) still belong to the palette; pick them up if nothing else claimed them.
    for name, value in DECL.findall(css):
        light.setdefault(name, value.strip())

    bad = [k for k, v in EXPECTED.items() if light.get(k, "").lower() != v]
    if bad:
        sys.stderr.write(
            "tokens.py: light values look wrong for %s -> %s\n"
            % (bad, {k: light.get(k) for k in bad})
        )
        sys.exit(1)

    out = [
        "/* GoldenPi design tokens - harvested from uatnew.goldenpi.com",
        "   Light theme only. Dark values are listed at the bottom for the later pass.",
        "   Regenerate with: ./crawl/assets.sh */",
        "",
        ":root {",
        "  /* --- core palette --- */",
    ]
    for k in CORE:
        if k in light:
            out.append("  %s: %s;" % (k, light[k]))
    out.append("")
    out.append("  /* --- component tokens --- */")
    for k in sorted(light):
        if k not in CORE and not k.startswith("--lightningcss"):
            out.append("  %s: %s;" % (k, light[k]))
    out.append("}")

    out.append("")
    out.append("/* dark theme (phase D)")
    for k in sorted(dark):
        if not k.startswith("--lightningcss"):
            out.append("  %s: %s;" % (k, dark[k]))
    out.append("*/")
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
