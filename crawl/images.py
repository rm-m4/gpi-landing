#!/usr/bin/env python3
"""Download every image the captured pages reference into assets/img/.

Regex over raw URL characters is not enough here: issuer logos live on S3 under
paths with literal spaces and parentheses ("GPID107347.Best Capital.png"), which
any whitespace-delimited pattern truncates. So URLs are read out of the attributes
that contain them (src, srcset, data-src, style url()) where quotes give a real
boundary, then percent-encoded on the way out.

Writes assets/img-map.tsv: original URL -> local filename.
"""
import os
import re
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(ROOT, "assets", "img")
BASE = "https://uatnew.goldenpi.com"
EXT = (".png", ".jpg", ".jpeg", ".svg", ".webp", ".gif", ".avif", ".ico")

ATTR = re.compile(r'(?:src|data-src|poster)="([^"]+)"', re.I)
SRCSET = re.compile(r'srcset="([^"]+)"', re.I)
CSSURL = re.compile(r"url\(&quot;([^&]+)&quot;\)|url\(['\"]?([^'\")]+)['\"]?\)", re.I)


def candidates(html):
    for m in ATTR.finditer(html):
        yield m.group(1)
    for m in SRCSET.finditer(html):
        for part in m.group(1).split(","):
            url = part.strip().split(" ")[0]
            if url:
                yield url
    for m in CSSURL.finditer(html):
        yield m.group(1) or m.group(2)


def normalise(u):
    u = u.strip().rstrip("\\").replace("&amp;", "&")
    if u.startswith("//"):
        u = "https:" + u
    if u.startswith("/_next/image"):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(u).query)
        inner = q.get("url", [""])[0]
        if not inner.startswith("/"):
            return None
        u = inner
    if u.startswith("/"):
        u = BASE + u
    if not u.startswith("http"):
        return None
    path = urllib.parse.urlparse(u).path
    return u if path.lower().endswith(EXT) else None


# Next.js stamps a content hash into bundled asset names
# ("hero-shield.2mjcc1ya410_2.png"). Strip it so the page markup we hand to
# developers reads as hero-shield.png. Collisions are checked for in main().
HASH = re.compile(r"\.[a-z0-9_-]{10,16}(?=\.[A-Za-z0-9]+$)")


def safe_name(url):
    base = urllib.parse.unquote(urllib.parse.urlparse(url).path.split("/")[-1])
    if "/_next/static/media/" in url:
        base = HASH.sub("", base)
    return re.sub(r"[^A-Za-z0-9._-]+", "-", base)


def encode(url):
    p = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit(
        (p.scheme, p.netloc, urllib.parse.quote(p.path, safe="/%"), p.query, "")
    )


def fetch(url, dest):
    for attempt in (url, url.replace("http://", "https://", 1)):
        req = urllib.request.Request(
            encode(attempt),
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
                "Cookie": "gp-locale=en",
                "Accept": "image/avif,image/webp,image/*,*/*",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                data = r.read()
            if data:
                with open(dest, "wb") as f:
                    f.write(data)
                return True
        except Exception:
            continue
    return False


def main():
    os.makedirs(IMG_DIR, exist_ok=True)
    urls = set()
    for sub in ("rendered", "raw"):
        d = os.path.join(ROOT, "crawl", sub)
        if not os.path.isdir(d):
            continue
        for fn in os.listdir(d):
            if not fn.endswith(".html"):
                continue
            with open(os.path.join(d, fn), encoding="utf-8", errors="replace") as f:
                html = f.read()
            for c in candidates(html):
                u = normalise(c)
                if u:
                    urls.add(u)

    print("    %d distinct image URLs" % len(urls))

    names = {}
    for u in sorted(urls):
        n = safe_name(u)
        if n in names:
            # Two different URLs would land on the same file: keep both by falling
            # back to the un-stripped name rather than silently overwriting one.
            n = re.sub(r"[^A-Za-z0-9._-]+", "-", urllib.parse.unquote(u.split("/")[-1]))
        names[n] = u

    rows, ok, fail = [], 0, 0
    for u in sorted(urls):
        name = next(n for n, v in names.items() if v == u)
        dest = os.path.join(IMG_DIR, name)
        # Re-runs after a naming change: adopt the already-downloaded file.
        legacy = os.path.join(IMG_DIR, re.sub(r"[^A-Za-z0-9._-]+", "-",
                                              urllib.parse.unquote(u.split("/")[-1])))
        if not os.path.exists(dest) and os.path.exists(legacy):
            os.rename(legacy, dest)
        rows.append("%s\t%s" % (u, name))
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            ok += 1
            continue
        if fetch(u, dest):
            ok += 1
        else:
            fail += 1
            print("    MISS %s" % u)

    with open(os.path.join(ROOT, "assets", "img-map.tsv"), "w", encoding="utf-8") as f:
        f.write("\n".join(rows) + "\n")
    print("    downloaded/present: %d   failed: %d" % (ok, fail))
    return 0


if __name__ == "__main__":
    sys.exit(main())
