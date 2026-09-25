#!/bin/bash
# Fetch a uatnew.goldenpi.com page. Needs gp-locale cookie or / 307-loops.
# usage: ./fetch.sh /path-or-slash  -> crawl/raw/<slug>.html
set -euo pipefail
p="${1:-/}"
slug=$(echo "$p" | sed 's#^/##; s#/$##; s#[/?=&]#_#g'); slug="${slug:-home}"
out="$(dirname "$0")/raw/$slug.html"
curl -sS --max-time 60 --compressed \
  -b "gp-locale=en" \
  -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36" \
  -H "Accept: text/html,application/xhtml+xml" \
  "https://uatnew.goldenpi.com$p" -o "$out"
echo "$out  $(wc -c < "$out") bytes"
