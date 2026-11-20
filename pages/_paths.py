"""Where the page sets live (user, 2026-11-20): web/ is the released set
(_web_v1.py builds it), pages/ is the Iteration tab, migration/ the Migration
tab (frozen records). A generator reads and writes a page through find() and
write_page(), so a page that moved to migration/ keeps working from its script.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MIGRATION = os.path.join(ROOT, "migration")
LINK = re.compile(r'\b(href|src|action|poster)=(["\'])([^"\']*)\2')


def find(name):
    """The page's path: migration/ when it lives there, else pages/."""
    path = os.path.join(MIGRATION, name)
    return path if os.path.exists(path) else os.path.join(HERE, name)


def up_links(html, name):
    """A migration/ page's links to its old neighbours in pages/ go up a level."""
    mig = set(os.listdir(MIGRATION)) | {name}

    def fix(m):
        url = m.group(3)
        if not url or re.match(r"(\.\./|/|#|\$|[a-z]+:)", url) or re.split(r"[?#]", url)[0] in mig:
            return m.group(0)
        return "%s=%s../pages/%s%s" % (m.group(1), m.group(2), url, m.group(2))
    return LINK.sub(fix, html)


def write_page(name, html):
    path = find(name)
    if path.startswith(MIGRATION):
        html = up_links(html, name)
    open(path, "w", encoding="utf-8").write(html)


if __name__ == "__main__":
    t = up_links('<a href="index.html#x"><img src="../assets/a.png"><a href="${u}"><a href="https://x">', "a.html")
    assert t == '<a href="../pages/index.html#x"><img src="../assets/a.png"><a href="${u}"><a href="https://x">', t
    print("ok")
