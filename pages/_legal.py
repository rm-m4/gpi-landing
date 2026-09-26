#!/usr/bin/env python3
"""Write privacy-policy.html and terms-and-conditions.html from the capture.

The legal text is regulated content, so it is never retyped. It is read out of
crawl/rendered/<slug>.expanded.html -- the live page's <main> with every
accordion opened -- and only re-wrapped: rich text keeps its words, links and
lists; runs of <br><br> become paragraphs. Classes and ids are dropped.

The live pages hide each section in a collapsed accordion. Here every section is
open, with a sticky rail of anchors beside it, because a policy is read, not
browsed. The shell (promo bar, header, footer) is borrowed from
refer-and-earn.html and re-synced by _build.py afterwards.

    python3 pages/_legal.py && python3 pages/_build.py
"""
import html
import os
import re
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
UAT = "https://uatnew.goldenpi.com"

PAGES = {
    "privacy-policy": {
        "title": "Privacy Policy | GoldenPi Securities",
        "desc": "Learn how GoldenPi Securities collects, uses, shares, and protects your personal "
                "and financial information on www.goldenpi.com under applicable Indian law.",
    },
    "terms-and-conditions": {
        "title": "Terms &amp; Conditions | GoldenPi Securities",
        "desc": "Read GoldenPi Terms &amp; Conditions covering registration, transactions, "
                "communications, liability, and dispute resolution for platform investors.",
    },
}

VOID = {"br", "img", "hr", "input", "meta", "link", "path"}
KEEP = {"a", "ul", "ol", "li", "br", "strong", "b", "em", "i", "u"}


# ------------------------------------------------------------------ tiny DOM
class Node:
    def __init__(self, tag, attrs):
        self.tag, self.attrs, self.kids = tag, dict(attrs), []

    def cls(self):
        return self.attrs.get("class", "").split()

    def find_all(self, pred):
        for k in self.kids:
            if isinstance(k, Node):
                if pred(k):
                    yield k
                yield from k.find_all(pred)

    def find(self, pred):
        return next(self.find_all(pred), None)

    def text(self):
        return re.sub(r"\s+", " ", "".join(
            k if isinstance(k, str) else k.text() for k in self.kids)).strip()


class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("root", {})
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs)
        self.stack[-1].kids.append(n)
        if tag not in VOID:
            self.stack.append(n)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        self.stack[-1].kids.append(data)


def parse(path):
    t = Tree()
    t.feed(open(path, encoding="utf-8").read())
    return t.root


def by_class(name):
    return lambda n: name in n.cls()


# ------------------------------------------------------------ rich text out
def inline(node):
    """Serialise children, keeping only the tags that carry meaning."""
    out = []
    for k in node.kids:
        if isinstance(k, str):
            out.append(html.escape(k, quote=False))
        elif k.tag in KEEP:
            if k.tag == "br":
                out.append("<br>")
                continue
            attr = ""
            if k.tag == "a":
                href = k.attrs.get("href", "")
                if href.startswith("/"):
                    href = UAT + href
                attr = ' href="%s"' % html.escape(href)
            out.append("<%s%s>%s</%s>" % (k.tag, attr, inline(k), k.tag))
        else:
            out.append(inline(k))
    return "".join(out)


def paragraphs(node):
    """Rich text -> <p> blocks. Their copy separates paragraphs with <br><br>."""
    raw = re.sub(r"\s+", " ", inline(node))
    blocks = []
    for chunk in re.split(r"(?:\s*<br>\s*){2,}", raw):
        # Lists stand on their own; the text either side becomes paragraphs.
        for part in re.split(r"(<ul>.*?</ul>|<ol>.*?</ol>)", chunk):
            part = re.sub(r"^(\s*<br>\s*)+|(\s*<br>\s*)+$", "", part).strip()
            if not part:
                continue
            if part.startswith(("<ul>", "<ol>")):
                blocks.append(part.replace("<li>", "\n  <li>").replace("</ul>", "\n</ul>"))
            else:
                blocks.append("<p>%s</p>" % part)
    return "\n".join(blocks)


def slug(text):
    text = re.sub(r"^\d+\.\s*", "", text)
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


# --------------------------------------------------------------- structure
def read(slug_):
    root = parse(os.path.join(ROOT, "crawl", "rendered", slug_ + ".expanded.html"))
    page = {
        "h1": root.find(by_class("legal-page__heading")).text(),
        "revision": root.find(by_class("legal-page__revision")).text(),
        "intro": paragraphs(root.find(by_class("legal-page__intro"))),
        "lead_heading": None,
        "sections": [],
    }
    sub_head = root.find(by_class("legal-page__secondary-heading"))
    if sub_head:
        page["lead_heading"] = sub_head.text()
    sec = root.find(by_class("legal-page__secondary"))
    page["secondary"] = paragraphs(sec)

    for child in root.find(by_class("legal-page__sections")).kids:
        if not isinstance(child, Node):
            continue
        if "gp-expand-group" in child.cls():
            items = [(e.find(by_class("gp-expand__title")).text(),
                      paragraphs(e.find(by_class("gp-expand__html"))))
                     for e in child.find_all(by_class("gp-expand"))]
            head = child.find(by_class("gp-expand-group__heading"))
            if head:
                title, body = head.text(), ""
            else:
                # A group with no heading of its own: its first row is the lead.
                (title, body), items = items[0], items[1:]
        else:
            title = child.find(by_class("gp-expand__title")).text()
            body = paragraphs(child.find(by_class("gp-expand__html")))
            items = []
        page["sections"].append({"id": slug(title), "title": title, "body": body, "items": items})
    return page


# -------------------------------------------------------------------- page
def render(slug_, page):
    rail, doc = [], []
    for s in page["sections"]:
        rail.append('          <a href="#%s">%s</a>' % (s["id"], html.escape(s["title"])))
        parts = ['<section id="%s" class="gp-legal__section">' % s["id"],
                 "<h2>%s</h2>" % html.escape(s["title"])]
        if s["body"]:
            parts.append(s["body"])
        for title, body in s["items"]:
            parts.append('<h3 id="%s">%s</h3>' % (slug(title), html.escape(title)))
            parts.append(body)
        parts.append("</section>")
        doc.append("\n".join(parts))

    lead = ""
    if page["lead_heading"]:
        lead = '<h2 class="gp-legal__lead-title">%s</h2>\n' % html.escape(page["lead_heading"])

    return """<main id="main-content">

  <!-- ================================================================ hero -->
  <section class="gp-hero gp-legal-hero">
    <div class="gp-shell pt-6 pb-10">
      <nav class="t-small t-muted mb-6" aria-label="Breadcrumb">
        <a href="index.html" class="hover:text-ink">Home</a>
        <span class="mx-1.5">&rsaquo;</span>
        <span class="text-ink font-medium">{h1}</span>
      </nav>
      <h1 class="t-h1">{h1}</h1>
      <span class="gp-legal-hero__rule" aria-hidden="true"></span>
      <p class="gp-badge gp-legal-hero__date">{revision}</p>
    </div>
  </section>

  <!-- ============================================================ document -->
  <!-- Generated by pages/_legal.py from crawl/rendered/{slug}.expanded.html.
       Verbatim text; on the live page each section is a collapsed accordion. -->
  <section class="gp-section gp-section--tight gp-section--flush-top">
    <div class="gp-shell">
      <div class="gp-navlayout gp-legal">
        <nav class="gp-sidenav" aria-label="{h1} sections">
{rail}
        </nav>
        <article class="gp-article gp-legal__doc">
<div class="gp-legal__intro">
{intro}
</div>
{lead}<div class="gp-legal__callout">
{secondary}
</div>
{doc}
        </article>
      </div>
    </div>
  </section>
</main>""".format(
        h1=html.escape(page["h1"]), revision=html.escape(page["revision"]), slug=slug_,
        rail="\n".join(rail), intro=page["intro"], lead=lead,
        secondary=page["secondary"], doc="\n\n".join(doc))


SCRIPT = """
<script>
// Rail follows the reader: the section nearest the top of the viewport is
// marked current. Plain anchors without it, so nothing depends on this.
(function () {
  if (!('IntersectionObserver' in window)) return;
  var links = {};
  document.querySelectorAll('.gp-legal .gp-sidenav a').forEach(function (a) {
    links[a.getAttribute('href').slice(1)] = a;
  });
  var current = null;
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      if (current) current.classList.remove('is-on');
      current = links[e.target.id];
      if (!current) return;
      current.classList.add('is-on');
      // Keep the active link in view inside the rail (the phone strip scrolls sideways).
      var rail = current.parentNode;
      rail.scrollTo({ left: current.offsetLeft - 16, top: current.offsetTop - rail.clientHeight / 2 });
    });
  }, { rootMargin: '-20% 0px -70% 0px' });
  document.querySelectorAll('.gp-legal__section').forEach(function (s) { io.observe(s); });
})();
</script>
"""


def main():
    shell = open(os.path.join(HERE, "refer-and-earn.html"), encoding="utf-8").read()
    head, rest = shell.split('<main id="main-content">', 1)
    footer = rest.split("</main>", 1)[1]
    footer = footer[: footer.index("</footer>") + len("</footer>")]

    for slug_, meta in PAGES.items():
        page = read(slug_)
        top = re.sub(r"<title>.*?</title>", "<title>%s</title>" % meta["title"], head, flags=re.S)
        top = re.sub(r"<!-- Refer & Earn.*?-->",
                     "<!-- %s, generated by pages/_legal.py from uatnew.goldenpi.com/%s\n"
                     "     (captured 2026-09-26). Do not edit by hand. -->" % (page["h1"], slug_),
                     top, flags=re.S)
        top = re.sub(r'<meta name="description" content="[^"]*">',
                     '<meta name="description" content="%s">' % meta["desc"], top)
        out = top + render(slug_, page) + footer + "\n" + SCRIPT + "\n</body>\n</html>\n"
        path = os.path.join(HERE, slug_ + ".html")
        open(path, "w", encoding="utf-8").write(out)

        # Phase B record: the same text, as reviewable markdown.
        md = ["# %s" % page["h1"], "", page["revision"], "", re.sub(r"<[^>]+>", "", page["intro"])]
        if page["lead_heading"]:
            md += ["", "## " + page["lead_heading"]]
        md += ["", re.sub(r"<[^>]+>", "", page["secondary"])]
        for s in page["sections"]:
            md += ["", "## " + s["title"]]
            if s["body"]:
                md += ["", re.sub(r"<[^>]+>", "", s["body"])]
            for t, b in s["items"]:
                md += ["", "### " + t, "", re.sub(r"<[^>]+>", "", b)]
        open(os.path.join(ROOT, "content", slug_ + ".sections.md"), "w",
             encoding="utf-8").write(html.unescape("\n".join(md)) + "\n")
        print("%-24s %d sections" % (slug_ + ".html", len(page["sections"])))


if __name__ == "__main__":
    main()
