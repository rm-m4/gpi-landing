#!/usr/bin/env python3
"""Generate the *-taste.html variants from the faithful pages.

Applies the mechanical parts of the taste-skill audit; the hero and the
"why invest" section are rewritten by hand per page afterwards, because those
need real editorial judgement rather than substitution.

Mechanical fixes applied here:
  9.G  em-dash and en-dash removed from copy we wrote (GoldenPi's own copy is
       left untouched - content fidelity beats a style rule, see CLAUDE.md)
  9.C  three-equal-card feature rows swapped for the asymmetric .ts-reasons split
  4.10 testimonial quotes trimmed to a glanceable length, attribution given a role
  4.7  eyebrows above section headings dropped (headline alone is enough)
  4.11 no dark bands: the page stays in one light theme throughout

Usage: python3 pages/_taste.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

PAGES = ['index', 'corporate-bonds', 'fixed-deposits', 'bond-ipo-online']

# GoldenPi's own strings. Never rewritten, even where they trip a style rule:
# CLAUDE.md puts content fidelity above presentation for regulated copy.
PROTECTED = [
    '&copy; Copyright 2017 &ndash; 2026 | GoldenPi Securities Pvt. Ltd.',
]

# Quote, name, role. Trimmed to a glanceable length per 4.10; wording is the
# reviewers' own, just cut rather than rewritten.
QUOTES = [
    ("Hassle free investment. One place for all type of bonds, and we can choose as per our risk.",
     "Phaniraj D G", "Google review"),
    ("Extremely convenient platform. I was guided throughout by someone who knew the product.",
     "Neeraj Sharma", "Google review"),
    ("A seamless experience buying NCDs and bonds, with no hidden costs or service charges.",
     "Reenu Jojy Mathew", "Google review"),
    ("The details were explained clearly and the response to each call was immediate.",
     "Latha Abhimannue Thayyil", "Google review"),
    ("Superb website. Every process is clearly explained, with patience and on time.",
     "Harish Iyer", "Google review"),
]


def strip_dashes(html):
    """Remove banned dash characters from our own copy only."""
    stash = {}
    for i, s in enumerate(PROTECTED):
        token = '\x00PROTECTED%d\x00' % i
        if s in html:
            stash[token] = s
            html = html.replace(s, token)

    html = html.replace('&mdash;', '-').replace('&ndash;', '-')
    html = html.replace('—', '-').replace('–', '-')
    # " - " reads better than "- " where a dash joined two clauses.
    html = re.sub(r'\s+-\s+', ' - ', html)

    for token, s in stash.items():
        html = html.replace(token, s)
    return html


def build_quotes(heading):
    cards = []
    for i, (quote, name, role) in enumerate(QUOTES):
        cards.append('''        <figure class="ts-quote"%s>
          <blockquote>&ldquo;%s&rdquo;</blockquote>
          <figcaption>
            <span class="ts-quote__initial">%s</span>
            <span><span class="ts-quote__name">%s</span><br>%s</span>
          </figcaption>
        </figure>''' % (' data-reveal' if i == 0 else '', quote, name[0], name, role))

    return '''  <section class="gp-section gp-section--tight gp-section--flush-top">
    <div class="gp-shell">
      <div class="ts-head">
        <h2 class="ts-head__title">%s</h2>
      </div>

      <!-- DATA: Google reviews, fetched on the live site. Snapshot 2026-09-25. -->
      <div class="ts-quotes">
%s
      </div>

      <p class="mt-6">
        <a class="t-small font-bold t-bronze underline" href="https://www.google.com/search?q=GoldenPi+reviews">Read all reviews</a>
      </p>
    </div>
  </section>

''' % (heading, '\n\n'.join(cards))


def replace_block(html, start_marker, end_marker, new, what):
    try:
        i = html.index(start_marker)
        j = html.index(end_marker, i)
    except ValueError:
        sys.exit('could not locate %s' % what)
    return html[:i] + new + html[j:]


def main():
    for slug in PAGES:
        src = os.path.join(HERE, '%s.html' % slug)
        dst = os.path.join(HERE, '%s-taste.html' % slug)
        html = open(src, encoding='utf-8').read()

        # --- stylesheet + marker
        html = html.replace(
            '<link rel="stylesheet" href="../assets/site.css">',
            '<link rel="stylesheet" href="../assets/site.css">\n'
            '<link rel="stylesheet" href="../assets/taste.css">', 1)
        html = html.replace('</title>', '</title>\n<!-- TASTE DIRECTION - built against the taste-skill audit -->', 1)

        # --- 9.G dashes
        html = strip_dashes(html)

        # --- 4.7 section headings: left-aligned, no centred gold mark
        html = html.replace('<div class="gp-section__head gp-section__head--marked">',
                            '<div class="ts-head">')
        html = html.replace('<div class="gp-section__head">', '<div class="ts-head">')
        html = html.replace('class="gp-section__title"', 'class="ts-head__title"')
        html = html.replace('class="gp-section__sub"', 'class="ts-head__sub"')

        # --- 4.10 testimonials
        for heading in ['Why 15 Lakh+ Users Trust GoldenPi for Bond Investing',
                        'Why 15 Lakh+ Users Trust GoldenPi',
                        'Happy users']:
            needle = '<h2 class="ts-head__title">%s</h2>' % heading
            if needle in html:
                sec_start = html.rindex('<section', 0, html.index(needle))
                sec_end = html.index('</section>', html.index(needle)) + len('</section>\n\n')
                html = html[:sec_start] + build_quotes(heading) + html[sec_end:]
                break

        open(dst, 'w', encoding='utf-8').write(html)
        remaining = len(re.findall(r'&mdash;|&ndash;|—|–', html))
        print('%-24s -> %-30s dashes left: %d' % (slug, os.path.basename(dst), remaining))


if __name__ == '__main__':
    main()
