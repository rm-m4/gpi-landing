#!/usr/bin/env python3
"""Extract page copy from the rendered GoldenPi captures into reviewable markdown.

The site is div-soup (almost no <table>, <p> or <ul>), so tag names tell us little.
Instead we walk to the *leaf blocks* -- the smallest elements that contain text and
no text-bearing children -- and emit one line each. For a bond card that yields
"Returns" / "13.00%" / "Credit Rating" / "ACUITE BBB+" in order, which is exactly
what we need to rebuild it.

Usage: python3 crawl/extract.py [slug ...]   -> content/<slug>.md, content/<slug>.assets.txt
"""
import html
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "crawl", "rendered")
DST = os.path.join(ROOT, "content")

DROP = {"script", "style", "noscript", "template", "svg", "head"}
# Dropped but self-closing: they never emit an end tag, so they must not open a skip
# region -- doing so would swallow the rest of the document.
DROP_VOID = {"link", "meta", "base"}
VOID = {"img", "br", "hr", "input", "source", "area", "col", "embed", "track", "wbr"}
HEADINGS = {"h1": 1, "h2": 2, "h3": 3, "h4": 4, "h5": 5, "h6": 6}

# Wrapper classes that mark a real page section (found by inspecting the live markup).
INLINE = {
    "a", "b", "strong", "em", "i", "u", "s", "small", "sup", "sub", "mark", "code",
    "span", "br", "abbr", "cite", "q", "time", "bdi", "wbr", "font",
}

SECTION_HINTS = (
    "home-hero", "cb-hero", "fd-hero", "bio-hero", "issuer-section", "gp-page-shell",
    "gp-webinar-block", "fd-calc-block", "cb-faq", "site-footer", "home-assets",
    "home-collections", "gp-happy-users", "issuer-blog", "gp-assets-row-card",
)


class Node:
    __slots__ = ("tag", "attrs", "kids", "text")

    def __init__(self, tag, attrs=None):
        self.tag = tag
        self.attrs = attrs or {}
        self.kids = []
        self.text = ""


class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root")
        self.stack = [self.root]
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in DROP_VOID:
            return
        if self.skip:
            if tag in DROP:
                self.skip += 1
            return
        if tag in DROP:
            self.skip = 1
            return
        n = Node(tag, dict(attrs))
        self.stack[-1].kids.append(n)
        if tag not in VOID:
            self.stack.append(n)

    def handle_endtag(self, tag):
        if self.skip:
            if tag in DROP:
                self.skip -= 1
            return
        if tag in VOID:
            return
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        if self.skip or not data.strip():
            return
        n = Node("#text")
        n.text = data
        self.stack[-1].kids.append(n)


def flat_text(node):
    if node.tag == "#text":
        return node.text
    if node.tag == "img":
        return ""
    return "".join(flat_text(k) for k in node.kids)


def clean(s):
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def first_link(node):
    if node.tag == "a" and node.attrs.get("href"):
        return node.attrs["href"]
    for k in node.kids:
        if k.tag != "#text":
            found = first_link(k)
            if found:
                return found
    return None


def section_label(node):
    cls = node.attrs.get("class", "")
    nid = node.attrs.get("id", "")
    for hint in SECTION_HINTS:
        if hint in cls or hint in nid:
            return hint
    return None


def collect_images(node, images):
    if node.tag == "img":
        src = node.attrs.get("src", "")
        if src and not src.startswith("data:"):
            images.append((src, node.attrs.get("alt", "")))
        return
    for k in node.kids:
        if k.tag != "#text":
            collect_images(k, images)


def walk(node, out, images, section=None):
    """Emit leaf blocks in document order. Returns True if anything was emitted."""
    label = section_label(node)
    if label and label != section:
        out.append(("section", label))
        section = label

    if node.tag == "img":
        src = node.attrs.get("src", "")
        if src and not src.startswith("data:"):
            images.append((src, node.attrs.get("alt", "")))
        return False

    # Mixed content -- a paragraph whose own text is interleaved with <strong>/<a>.
    # Descending would emit only the inline fragments and drop the sentence around
    # them, so keep the element whole.
    kids = [k for k in node.kids if k.tag != "#text"]
    has_own_text = any(k.tag == "#text" and k.text.strip() for k in node.kids)
    if has_own_text and kids and all(k.tag in INLINE for k in kids):
        for kid in kids:
            collect_images(kid, images)
        text = clean(flat_text(node))
        if text:
            out.append(("h", HEADINGS[node.tag], text) if node.tag in HEADINGS
                       else ("t", text, first_link(node)))
            return True
        return False

    emitted = False
    for kid in kids:
        if walk(kid, out, images, section):
            emitted = True

    if emitted:
        return True

    text = clean(flat_text(node))
    if not text:
        return False
    if node.tag in HEADINGS:
        out.append(("h", HEADINGS[node.tag], text))
    else:
        out.append(("t", text, first_link(node)))
    return True


def render(slug, doc, out, images):
    lines = ["# %s" % slug, ""]
    title = clean(doc.get("title", ""))
    if title:
        lines += ["**Title:** %s" % title]
    desc = clean(doc.get("description", ""))
    if desc:
        lines += ["", "**Meta description:** %s" % desc]
    if slug.startswith("prod_"):
        # prod_user_explore -> https://goldenpi.com/user/explore
        src = "https://goldenpi.com/" + slug[len("prod_"):].replace("user_", "user/", 1)
    else:
        src = "https://uatnew.goldenpi.com/%s" % ("" if slug == "home" else slug)
    lines += ["", "**Source:** %s" % src, ""]

    prev = None
    for item in out:
        if item == prev:  # the site duplicates blocks for mobile/desktop variants
            continue
        prev = item
        if item[0] == "section":
            lines += ["", "<!-- section: %s -->" % item[1], ""]
        elif item[0] == "h":
            lines += ["", "%s %s" % ("#" * min(item[1] + 1, 6), item[2]), ""]
        else:
            text, href = item[1], item[2]
            lines.append("- [%s](%s)" % (text, href) if href else "- %s" % text)

    md = "\n".join(lines)
    md = re.sub(r"\n{3,}", "\n\n", md) + "\n"
    with open(os.path.join(DST, "%s.md" % slug), "w", encoding="utf-8") as f:
        f.write(md)

    seen, rows = set(), []
    for src, alt in images:
        name = src.split("/")[-1].split("?")[0]
        if "_next%2Fstatic%2Fmedia%2F" in src:
            name = src.split("_next%2Fstatic%2Fmedia%2F")[1].split("&")[0]
        if name in seen:
            continue
        seen.add(name)
        rows.append("%s\t%s" % (name, alt))
    with open(os.path.join(DST, "%s.assets.txt" % slug), "w", encoding="utf-8") as f:
        f.write("\n".join(rows) + "\n")
    return len(lines), len(rows)


def extract(slug):
    with open(os.path.join(SRC, "%s.html" % slug), encoding="utf-8", errors="replace") as f:
        raw = f.read()
    doc = {}
    m = re.search(r"<title>(.*?)</title>", raw, re.S)
    if m:
        doc["title"] = m.group(1)
    m = re.search(r'<meta name="description" content="(.*?)"', raw, re.S)
    if m:
        doc["description"] = m.group(1)

    p = Tree()
    p.feed(raw)
    body = p.root
    for node in p.root.kids:
        if node.tag == "html":
            for k in node.kids:
                if k.tag == "body":
                    body = k

    out, images = [], []
    walk(body, out, images)
    return render(slug, doc, out, images)


def main():
    os.makedirs(DST, exist_ok=True)
    slugs = sys.argv[1:] or [f[:-5] for f in sorted(os.listdir(SRC)) if f.endswith(".html")]
    for slug in slugs:
        n, imgs = extract(slug)
        print("%-20s %4d lines  %2d images" % (slug, n, imgs))


if __name__ == "__main__":
    main()
