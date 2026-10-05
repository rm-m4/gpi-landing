#!/bin/bash
# Fetch every image the blog captures reference and write web-ready copies.
# Reads the URLs out of crawl/rendered/prod_blog*.json (run crawl/blog_extract.js first).
# Originals land in crawl/blog-orig/ (not committed); assets/img/blog/ gets each one
# as JPEG at 1200px and 640px wide, for srcset (sips: macOS only, no extra installs).
# Not AVIF: sips writes AVIF files that decode to a size but paint nothing in Chrome.
set -euo pipefail
cd "$(dirname "$0")/.."
orig=crawl/blog-orig; out=assets/img/blog
mkdir -p "$orig" "$out"
python3 - <<'EOF' > "$orig/urls.txt"
import json, re
seen = set()
for f in ('crawl/rendered/prod_blog.json', 'crawl/rendered/prod_blog_post.json'):
    for u in re.findall(r'"(https://[^"]+\.(?:png|jpe?g|webp))"', open(f).read()):
        # WordPress sizes (-1024x575, -300x300) point at the same art: fetch the full one,
        # except author photos, which only exist cropped.
        full = u if 'uploads/2026/07/10164806' in u else re.sub(r'-\d+x\d+(\.\w+)$', r'\1', u)
        if full not in seen:
            seen.add(full); print(full)
EOF
while read -r u; do
  name=$(basename "${u%%\?*}"); name=$(python3 -c "import sys,urllib.parse;print(urllib.parse.unquote(sys.argv[1]).replace('@','-').replace('%','').replace('₹',''))" "$name")
  base="${name%.*}"
  [ -s "$orig/$name" ] || curl -sS --max-time 60 -A "Mozilla/5.0" "$u" -o "$orig/$name"
  # The banner's two icons are small transparent PNGs: copy them as they are.
  case "$name" in *-icon.png) cp "$orig/$name" "$out/$name"; printf '%s\t%s\n' "$u" "$base"; continue;; esac
  # -Z also upscales, so cap each size at the original's longest side.
  w=$(sips -g pixelWidth -g pixelHeight "$orig/$name" | awk '/pixel/{if($2>m)m=$2}END{print m}')
  sips -s format jpeg -s formatOptions 78 -Z $(( w < 1200 ? w : 1200 )) "$orig/$name" --out "$out/$base.jpg" >/dev/null
  sips -s format jpeg -s formatOptions 72 -Z $(( w < 640 ? w : 640 )) "$orig/$name" --out "$out/$base-640.jpg" >/dev/null
  printf '%s\t%s\n' "$u" "$base"
done < "$orig/urls.txt" > "$out/map.tsv"
echo "$(wc -l < "$out/map.tsv") images -> $out  ($(du -sh "$orig" | cut -f1) originals, $(du -sh "$out" | cut -f1) optimised)"
