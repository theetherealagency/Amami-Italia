#!/usr/bin/env python3
"""Stamp every /_assets/*.css and *.js reference with ?v=<content hash>.

Run from the repo root after any change to src/_assets (and after the Journal
build):  python3 tools/version-assets.py
Browsers may keep /_assets files for a while; a new hash is a new URL, so a
changed stylesheet reaches every visitor at once and never pairs new HTML with
old CSS (2026-09-25: the footer form showed stacked, unstyled fields).
"""
import glob, hashlib, os, re
SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src')
h = {}
for f in glob.glob(os.path.join(SRC, '_assets', '*.css')) + glob.glob(os.path.join(SRC, '_assets', '*.js')):
    h['/_assets/' + os.path.basename(f)] = hashlib.sha1(open(f, 'rb').read()).hexdigest()[:8]
pat = re.compile(r'((?:href|src)=")(/_assets/[A-Za-z0-9._-]+\.(?:css|js))(?:\?v=[0-9a-f]*)?(")')
n = 0
for f in glob.glob(os.path.join(SRC, '**', '*.html'), recursive=True):
    if '/wp-content/' in f:
        continue
    s = open(f, encoding='utf-8').read()
    t = pat.sub(lambda m: m.group(1) + m.group(2) + ('?v=' + h[m.group(2)] if m.group(2) in h else '') + m.group(3), s)
    if t != s:
        open(f, 'w', encoding='utf-8').write(t); n += 1
print(f'stamped {len(h)} asset files into {n} pages')
