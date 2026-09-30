#!/usr/bin/env python3
"""Build an audit report page from summary.json, inp.<group>.json and prose.<group>.html.

prose.<group>.html is the hand-written page with {{placeholders}}; this fills in
the tables so the numbers in the report are always the measured ones.
Usage: python3 perf/report.py perf/2026-09-30 guest   -> report.html
       python3 perf/report.py perf/2026-09-30 auth    -> report-auth.html
"""
import html, json, os, re, sys

D, GROUP = sys.argv[1], sys.argv[2]
S = json.load(open(os.path.join(D, 'summary.json')))
# A page still mid-run has no desktop result yet.
ROWS = [r for r in S['rows'] if r['group'] == GROUP and 'desktop' in r]
# (good, poor) limits; above poor is Poor, between is Needs work.
LIMITS = {'lcp': (2500, 4000), 'cls': (0.1, 0.25), 'tbt': (200, 600), 'fcp': (1800, 3000),
          'si': (3400, 5800), 'ttfb': (800, 1800), 'tti': (3800, 7300), 'inp': (200, 500)}
COLS = ['lcp', 'cls', 'tbt', 'fcp', 'si', 'ttfb', 'tti']
e = html.escape


def band(k, v):
    g, p = LIMITS[k]
    return 'good' if v <= g else 'warn' if v <= p else 'poor'


def fmt(k, v):
    if k == 'cls':
        return f'{v:.3f}'
    if k in ('tbt', 'ttfb', 'inp'):
        return f'{v:.0f} ms'
    return f'{v / 1000:.1f} s'


def page_th(r):
    return f'<th scope="row"><b>{e(r["slug"])}</b><code>{e(r["path"])}</code></th>'


def metric_rows(form, rows=None):
    out = []
    for r in rows or ROWS:
        m = r[form]['metrics']
        tds = []
        for k in COLS:
            rng = f'<small>{fmt(k, m[k]["min"])} – {fmt(k, m[k]["max"])}</small>' if r[form]['n'] > 1 else ''
            tds.append(f'<td class="num"><span class="v {band(k, m[k]["med"])}">{fmt(k, m[k]["med"])}</span>{rng}</td>')
        rng = f'<small>{m["score"]["min"]} – {m["score"]["max"]}</small>' if r[form]['n'] > 1 else ''
        tds.append(f'<td class="num"><span class="score">{m["score"]["med"]:.0f}</span>{rng}</td>')
        out.append(f'<tr>{page_th(r)}{"".join(tds)}</tr>')
    return '\n'.join(out)


def lcp_rows():
    out = []
    for r in ROWS:
        m = r['mobile']
        n = m.get('lcpNode') or {}
        ph = m.get('phases') or {}
        sel = (n.get('selector') or '').split(' > ')[-1]
        is_img = 'resourceLoadDelay' in ph
        kind = ('Background image' if is_img and not sel.startswith('img') else 'Image') if is_img else 'Text'
        label = (n.get('nodeLabel') or '').replace('\n', ' ')[:70]
        d = m.get('discovery')
        disc = '—' if not d else '<span class="v good">Passes</span>' if all(d.values()) else '<span class="v poor">Fails</span><small>' + ', '.join(
            t for key, t in (('priorityHinted', 'no fetchpriority'), ('requestDiscoverable', 'not in HTML'), ('eagerlyLoaded', 'lazy-loaded')) if not d[key]) + '</small>'
        cell = lambda key: f'{ph[key]} ms' if key in ph else '—'
        what = f'<b>{kind}</b> {e(label)}<small><code>{e(sel)}</code></small>' if n else '<span class="muted">not reported in the median run</span>'
        out.append(f'<tr>{page_th(r)}<td class="sel">{what}</td><td class="num">{cell("timeToFirstByte")}</td><td class="num">{cell("resourceLoadDelay")}</td>'
                   f'<td class="num">{cell("resourceLoadDuration")}</td><td class="num">{cell("elementRenderDelay")}</td><td class="num">{disc}</td></tr>')
    return '\n'.join(out)


def weight_rows():
    out = []
    mb = lambda b: f'{b / 1e6:.1f} MB' if b >= 1e6 else f'{b / 1e3:.0f} KB'
    for r in ROWS:
        m = r['mobile']
        res = m['resources']
        total = res['total'][1]
        img = res['image'][1]
        out.append(f'<tr>{page_th(r)}<td class="num"><span class="v {"poor" if total > 4e6 else "warn" if total > 1.6e6 else "good"}">{mb(total)}</span></td>'
                   f'<td class="num">{res["total"][0]}</td><td class="num">{mb(res["script"][1])}<small>{res["script"][0]} files</small></td>'
                   f'<td class="num">{mb(res["stylesheet"][1])}<small>{res["stylesheet"][0]} files</small></td>'
                   f'<td class="num"><span class="v {"poor" if img > 3e6 else "warn" if img > 1e6 else "good"}">{mb(img)}</span><small>{res["image"][0]} files</small></td>'
                   f'<td class="num">{mb(res["font"][1])}</td><td class="num">{mb(res["third-party"][1])}<small>{res["third-party"][0]} requests</small></td>'
                   f'<td class="num">{m["dom"].get("Total elements", "—")}</td></tr>')
    return '\n'.join(out)


def inp_rows():
    out = []
    for _ in (1,):
        for row in json.load(open(os.path.join(D, f'inp.{GROUP}.json')))['rows']:
            taps = [t for t in row['taps'] if 'duration' in t]
            if not taps:
                out.append(f'<tr>{page_th(row)}<td colspan="5" class="muted">No in-page control to tap without navigating away</td></tr>')
                continue
            w = max(taps, key=lambda t: t['duration'])
            val = '&lt; 16 ms' if w.get('under16') else fmt('inp', w['duration'])
            part = lambda key: f'{w[key]} ms' if key in w else '—'
            out.append(f'<tr>{page_th(row)}<td class="num"><span class="v {band("inp", w["duration"])}">{val}</span><small>{len(taps)} tap{"s" if len(taps) > 1 else ""}</small></td>'
                       f'<td class="sel">{e(w["kind"])}: {e(w["label"])}</td><td class="num">{part("inputDelay")}</td><td class="num">{part("processing")}</td><td class="num">{part("presentation")}</td></tr>')
    return '\n'.join(out)


# Mobile medians from the 2026-09-28 audit (LCP ms, Lighthouse score), for the pages both audits cover.
PREV = {'home': (9200, 63), 'corporate-bonds': (7300, 71), 'fixed-deposits': (8800, 68), 'bond-ipo-online': (9300, 64),
        'bond-utsav': (8200, 69), 'collections-all-bonds': (14700, 66), 'list-view': (6800, 72), 'about-us': (6000, 74)}


def compare_rows():
    out = []
    for r in ROWS:
        if r['slug'] not in PREV:
            continue
        lcp0, sc0 = PREV[r['slug']]
        m = r['mobile']['metrics']
        d = m['lcp']['med'] - lcp0
        # Under 1 s either way is inside the run-to-run spread seen on these pages.
        word = 'No real change' if abs(d) < 1000 else 'Faster' if d < 0 else 'Slower'
        out.append(f'<tr>{page_th(r)}<td class="num"><span class="v {band("lcp", lcp0)}">{fmt("lcp", lcp0)}</span></td>'
                   f'<td class="num"><span class="v {band("lcp", m["lcp"]["med"])}">{fmt("lcp", m["lcp"]["med"])}</span><small>{fmt("lcp", m["lcp"]["min"])} – {fmt("lcp", m["lcp"]["max"])}</small></td>'
                   f'<td class="num">{d / 1000:+.1f} s<small>{word}</small></td><td class="num">{sc0}</td><td class="num"><span class="score">{m["score"]["med"]:.0f}</span></td></tr>')
    return '\n'.join(out)


FILL = {
    'compare_rows': compare_rows(),
    'mobile': metric_rows('mobile'), 'desktop': metric_rows('desktop'),
    'lcp_rows': lcp_rows(), 'weight_rows': weight_rows(), 'inp_rows': inp_rows(),
    'style': open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'report-style.html')).read(),
}
# Repeat-visit (warm cache) runs, when summarize.py was also pointed at lh-warm.
WARM = os.path.join(D, 'summary.lh-warm.json')
if os.path.exists(WARM):
    FILL['mobile_warm'] = metric_rows('mobile', [r for r in json.load(open(WARM))['rows'] if r['group'] == GROUP])
OUT = os.path.join(D, 'report.html' if GROUP == 'guest' else f'report-{GROUP}.html')
page = open(os.path.join(D, f'prose.{GROUP}.html')).read()
page = re.sub(r'\{\{(\w+)\}\}', lambda m: FILL[m.group(1)], page)
open(OUT, 'w').write(page)
print('wrote', OUT, len(page) // 1024, 'KB')
