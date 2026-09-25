#!/bin/bash
# Harvest images and light-theme design tokens from uatnew.goldenpi.com.
#   images -> assets/img/ + assets/img-map.tsv   (crawl/images.py)
#   tokens -> assets/tokens.css                  (crawl/tokens.py)
# Safe to re-run: existing images are kept, only missing ones are fetched.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BASE="https://uatnew.goldenpi.com"
COOKIE="gp-locale=en"

echo "==> images"
python3 "$ROOT/crawl/images.py"

echo "==> design tokens"
grep -ohE '/_next/static/chunks/[A-Za-z0-9._-]+\.css' "$ROOT"/crawl/raw/*.html | sort -u |
  while read -r c; do curl -sS --max-time 90 -b "$COOKIE" "$BASE$c"; done |
  python3 "$ROOT/crawl/tokens.py" > "$ROOT/assets/tokens.css"
echo "    wrote assets/tokens.css ($(grep -c -- '--' "$ROOT/assets/tokens.css") declarations)"
