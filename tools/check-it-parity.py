#!/usr/bin/env python3
"""Check that every bilingual page and its /it/ twin are the same page.

Run from the repo root:  python3 tools/check-it-parity.py
Exits 1 and lists the differences if any pair has drifted apart in
stylesheets, scripts, body class, main-content structure, images or links
(Italian links may point at /it/ twins; the OpenTable lang is expected to
differ). Added 2026-09-24 after /it/menu/ shipped without amami-menu.css.
"""
import re
import sys
from html.parser import HTMLParser

PAGES = ['', 'menu/', 'our-story/', 'after-dark/', 'events/', 'reservation/', 'contact/', 'journal/']
# every Journal post is bilingual too (content/journal/posts/<slug>.json)
import os as _os
_POSTS = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), 'content', 'journal', 'posts')
PAGES += sorted(f[:-5] + '/' for f in _os.listdir(_POSTS) if f.endswith('.json')) if _os.path.isdir(_POSTS) else []


class Main(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inmain = False
        self.seq, self.imgs, self.links = [], [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'main':
            self.inmain = True
        if not self.inmain:
            return
        cls = a.get('class') or ''
        self.seq.append(tag + ('.' + cls.split()[0] if cls else ''))
        if tag in ('img', 'source'):
            self.imgs.append((a.get('src') or a.get('srcset') or '').split(' ')[0])
        if tag == 'a':
            href = a.get('href', '')
            href = href.replace('/it/', '/', 1) if href.startswith('/it/') else href
            self.links.append(re.sub(r'lang=(en-CA|it-IT)', 'lang=*', href))

    def handle_endtag(self, tag):
        if tag == 'main':
            self.inmain = False


def facts(path):
    html = open(path, encoding='utf-8').read()
    m = Main()
    m.feed(html)
    body = re.search(r'<body class="([^"]*)"', html)
    return {
        'stylesheets': re.findall(r'<link rel="stylesheet" href="([^"]+)"', html),
        'scripts': re.findall(r'<script[^>]*src="([^"]+)"', html),
        'body class': sorted((body.group(1) if body else '').split()),
        'structure': m.seq,
        'images': m.imgs,
        'links': m.links,
    }


def main():
    bad = 0
    for pg in PAGES:
        en, it = facts('src/' + pg + 'index.html'), facts('src/it/' + pg + 'index.html')
        diffs = [k for k in en if en[k] != it[k]]
        print(('OK   ' if not diffs else 'DIFF ') + '/' + pg + ('' if not diffs else '  ' + ', '.join(diffs)))
        bad += bool(diffs)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
