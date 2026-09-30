#!/usr/bin/env python3
"""Reduce perf/<date>/lh/*.json to one row per page -> perf/<date>/summary.json.

Mobile values are the median of the runs with the min-max range; the LCP
element, breakdown and insights come from the run with the median LCP.
Usage: python3 perf/summarize.py perf/2026-09-30 [lh-warm]   (second arg: runs folder, default lh)
"""
import glob, json, os, statistics, sys
from collections import defaultdict

D = sys.argv[1]
LH = sys.argv[2] if len(sys.argv) > 2 else 'lh'
BASE = 'https://uatnew.goldenpi.com'
METRICS = {  # key -> audit id
    'lcp': 'largest-contentful-paint', 'cls': 'cumulative-layout-shift', 'tbt': 'total-blocking-time',
    'fcp': 'first-contentful-paint', 'si': 'speed-index', 'ttfb': 'server-response-time', 'tti': 'interactive',
}
INSIGHTS = ['render-blocking-insight', 'document-latency-insight', 'image-delivery-insight', 'cache-insight',
            'unused-javascript', 'unused-css-rules', 'legacy-javascript-insight', 'duplicated-javascript-insight',
            'font-display-insight', 'cls-culprits-insight', 'forced-reflow-insight', 'dom-size-insight',
            'third-parties-insight', 'unsized-images', 'mainthread-work-breakdown', 'bootup-time',
            'network-dependency-tree-insight', 'modern-http-insight', 'non-composited-animations']


def vals(lhr):
    a = lhr['audits']
    v = {k: a[i].get('numericValue') for k, i in METRICS.items()}
    v['score'] = round((lhr['categories']['performance']['score'] or 0) * 100)
    return v


def detail(lhr):
    a = lhr['audits']
    out = {'finalUrl': lhr['finalDisplayedUrl'].replace(BASE, ''), 'error': (lhr.get('runtimeError') or {}).get('code')}
    items = (a['lcp-breakdown-insight'].get('details') or {}).get('items') or []
    for it in items:
        if it.get('type') == 'table':
            out['phases'] = {r['subpart']: round(r['duration']) for r in it['items']}
        if it.get('type') == 'node':
            out['lcpNode'] = {k: it.get(k) for k in ('selector', 'nodeLabel', 'snippet')}
    for it in (a['lcp-discovery-insight'].get('details') or {}).get('items') or []:
        if it.get('type') == 'checklist':
            out['discovery'] = {k: v['value'] for k, v in it['items'].items()}
    obs = a['metrics']['details']['items'][0]
    out['observed'] = {k: obs.get(k) for k in ('observedFirstContentfulPaint', 'observedLargestContentfulPaint', 'observedLoad', 'observedDomContentLoaded')}
    out['resources'] = {r['resourceType']: [r['requestCount'], r['transferSize']] for r in a['resource-summary']['details']['items']}
    out['bytes'] = a['total-byte-weight'].get('numericValue')
    dom = (a['dom-size-insight'].get('details') or {}).get('items') or []
    out['dom'] = {r['statistic']: r['value']['value'] for r in dom if isinstance(r.get('value'), dict)}
    ins = {}
    for k in INSIGHTS:
        x = a.get(k)
        if not x:
            continue
        e = {'score': x.get('score'), 'display': x.get('displayValue'), 'savings': x.get('metricSavings')}
        its = (x.get('details') or {}).get('items') or []
        if k in ('render-blocking-insight', 'image-delivery-insight', 'cache-insight', 'unused-javascript', 'unsized-images', 'bootup-time', 'mainthread-work-breakdown'):
            keep = ('url', 'totalBytes', 'wastedBytes', 'wastedMs', 'total', 'scripting', 'group', 'groupLabel', 'duration', 'cacheLifetimeMs')
            e['items'] = [{f: i[f] for f in keep if f in i} for i in its[:8]]
            e['count'] = len(its)
        ins[k] = e
    out['insights'] = ins
    shifts = (a['layout-shifts'].get('details') or {}).get('items') or []
    out['shifts'] = [{'score': round(s['score'], 4), 'node': (s.get('node') or {}).get('selector'), 'label': (s.get('node') or {}).get('nodeLabel')} for s in shifts[:4]]
    tp = (a['third-parties-insight'].get('details') or {}).get('items') or []
    out['thirdParties'] = [{'entity': t.get('entity'), 'bytes': t.get('transferSize'), 'ms': round(t.get('mainThreadTime') or 0)} for t in tp[:8]]
    return out


runs = defaultdict(lambda: defaultdict(list))
for f in sorted(glob.glob(os.path.join(D, LH, '*.json'))):
    slug, form, _n, _ = os.path.basename(f).rsplit('.', 3)
    runs[slug][form].append(json.load(open(f)))

order = [p for name in ('guest', 'auth') if os.path.exists(os.path.join(D, name + '.json'))
         for p in [dict(x, group=name) for x in json.load(open(os.path.join(D, name + '.json')))]]
rows = []
for p in order:
    r = runs.get(p['slug'])
    if not r:
        continue
    row = dict(p)
    for form in ('mobile', 'desktop'):
        ls = r.get(form) or []
        if not ls:
            continue
        vs = [vals(l) for l in ls]
        agg = {k: {'med': statistics.median(v[k] for v in vs), 'min': min(v[k] for v in vs), 'max': max(v[k] for v in vs)} for k in vs[0]}
        mid = sorted(ls, key=lambda l: l['audits']['largest-contentful-paint']['numericValue'])[len(ls) // 2]
        row[form] = {'n': len(ls), 'metrics': agg, **detail(mid)}
    rows.append(row)

first = next(iter(next(iter(runs.values())).values()))[0]
json.dump({'lighthouse': first['lighthouseVersion'], 'ua': first['environment']['hostUserAgent'],
           'fetched': first['fetchTime'], 'rows': rows}, open(os.path.join(D, 'summary.json' if LH == 'lh' else f'summary.{LH}.json'), 'w'), indent=1)
for row in rows:
    m = row.get('mobile', {}).get('metrics')
    d = row.get('desktop', {}).get('metrics')
    if m:
        print(f"{row['slug']:<34} LCP {m['lcp']['med']/1000:5.1f}s CLS {m['cls']['med']:.3f} TBT {m['tbt']['med']:4.0f} FCP {m['fcp']['med']/1000:.1f}s "
              f"TTFB {m['ttfb']['med']:5.0f} score {m['score']['med']:.0f} | desktop LCP {d['lcp']['med']/1000 if d else 0:.1f}s CLS {d['cls']['med'] if d else 0:.3f}")
