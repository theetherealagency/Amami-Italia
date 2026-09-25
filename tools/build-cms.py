#!/usr/bin/env python3
"""Fill the editable parts of the site from content/site/*.json (the admin portal's data).

Run from the repo root:  python3 tools/build-cms.py

Pages carry small markers on the parts the client can change; everything else
(layout, classes, fonts, the OpenTable widget) is left exactly as it is:

  data-cms="key"        text. The element's text becomes the value in the page's
                        language; if it has a data-it attribute, that gets the
                        Italian (the site's usual <span data-it="…">English</span>).
  data-cms-html="key"   a short run of formatted writing (<p>, <em>, <a> …).
  data-cms-list="key"   a <ul>: one <li> per line of the list.
  data-cms-opt="key"    an enquiry <option>: "<room name> · <capacity>".
  data-cms-img="key"    a <picture>: the photo (desktop and phone) and its alt text.
  data-cms-menu="p:s"   a menu list: the dishes of section s on menu page p.

Values live in content/site/events.json and content/site/menu.json under
"slots" (and "menus" for the dishes). Text values are {"en": …, "it": …}.
The event date and time are set once ("event.date", "event.time") and every
page that shows them (events, the event page, its search-engine data) follows.

A page is only rewritten where its value changed, so running this with nothing
new changes nothing.
"""
import datetime
import glob
import html
import json
import os
import re
import sys
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'src')
SITE = os.path.join(ROOT, 'content', 'site')

MONTHS = {'en': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                 'October', 'November', 'December'],
          'it': ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre',
                 'ottobre', 'novembre', 'dicembre']}
DAYS = {'en': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        'it': ['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica']}


def esc(s):
    return html.escape(s or '', quote=True)


def load():
    slots, menus = {}, {}
    for f in sorted(glob.glob(os.path.join(SITE, '*.json'))):
        d = json.load(open(f, encoding='utf-8'))
        slots.update(d.get('slots', {}))
        menus.update(d.get('menus', {}))
    return slots, menus


def derived(slots):
    """The formatted forms of the event date and time, in both languages."""
    out = {}
    d = (slots.get('event.date') or {}).get('value')
    t = (slots.get('event.time') or {}).get('value')
    if not d or not t:
        return out
    day = datetime.date.fromisoformat(d)
    hh, mm = (int(x) for x in t.split(':'))
    long_en = f'{DAYS["en"][day.weekday()]}, {MONTHS["en"][day.month - 1]} {day.day}, {day.year}'
    long_it = f'{DAYS["it"][day.weekday()]} {day.day} {MONTHS["it"][day.month - 1]} {day.year}'
    h12 = hh % 12 or 12
    ampm = 'AM' if hh < 12 else 'PM'
    t_en = f'{h12} {ampm}' if mm == 0 else f'{h12}:{mm:02d} {ampm}'
    t_it = f'{hh}:{mm:02d}'
    out['event.date_long'] = {'en': long_en, 'it': long_it}
    out['event.time_card'] = {'en': t_en, 'it': f'Ore {t_it}'}
    out['event.time_fact'] = {'en': t_en, 'it': t_it}
    it_short = f'ore {hh}' if mm == 0 else f'ore {t_it}'
    out['event.sub'] = {'en': f'{long_en} · {t_en}', 'it': f'{long_it} · {it_short}'}
    start = datetime.datetime(day.year, day.month, day.day, hh, mm, tzinfo=ZoneInfo('America/Toronto'))
    out['event.start_iso'] = {'value': start.isoformat()}
    return out


def pick(v, lang):
    if isinstance(v, dict):
        return v.get(lang) if v.get(lang) not in (None, '') else v.get('en', '')
    return v or ''


# ---- markers ---------------------------------------------------------------

def set_attr(tag, name, value):
    """Set (or add) an attribute on a start tag."""
    if re.search(rf'\s{name}="[^"]*"', tag):
        return re.sub(rf'(\s{name}=")[^"]*(")', lambda m: m.group(1) + value + m.group(2), tag, count=1)
    return tag[:-1] + f' {name}="{value}">'


def elements(s, attr):
    """Yield (start, end_of_open_tag, close_start, close_end, key, open_tag) for marked elements."""
    for m in re.finditer(rf'<(\w+)\b[^>]*\s{attr}="([^"]+)"[^>]*>', s):
        tag, key = m.group(1), m.group(2)
        depth, close = 1, None
        for t in re.finditer(rf'<(/?){tag}\b[^>]*>', s[m.end():]):
            depth += -1 if t.group(1) else 1
            if depth == 0:
                close = m.end() + t.start()
                break
        if close is None:
            continue
        yield m.start(), m.end(), close, close + len(tag) + 3, key, m.group(0)


def replace_all(s, attr, render):
    out, pos = [], 0
    for a, b, c, d, key, open_tag in list(elements(s, attr)):
        if a < pos:
            continue
        new = render(key, open_tag, s[b:c])
        if new is None:
            continue
        new_open, new_inner = new
        out.append(s[pos:a])
        out.append(new_open + new_inner + s[c:d])
        pos = d
    out.append(s[pos:])
    return ''.join(out)


SAFE_TAGS = {'p', 'em', 'strong', 'b', 'i', 'a', 'br', 'ul', 'ol', 'li', 'h2', 'h3', 'blockquote', 'span'}


def clean_html(v):
    """Keep writing tags; drop scripts, styles, event handlers and javascript: links."""
    v = re.sub(r'(?is)<(script|style|iframe|object|embed)\b.*?</\1>', '', v or '')
    v = re.sub(r'(?i)\son\w+="[^"]*"', '', v)
    v = re.sub(r'(?i)href="\s*javascript:[^"]*"', 'href="#"', v)
    return re.sub(r'</?(\w+)\b[^>]*>', lambda m: m.group(0) if m.group(1).lower() in SAFE_TAGS else '', v)


def dish(it):
    tags = ''
    if it.get('v'):
        tags += '<abbr class="dish__tag" title="Vegetarian">V</abbr>'
    if it.get('gf'):
        tags += '<abbr class="dish__tag" title="Gluten free"><span data-it="SG">GF</span></abbr>'
    out = (f'<div class="dish"><div><span class="dish__name">{esc(it.get("name"))}</span>{tags}</div>'
           f'<span class="dish__price">{esc(price(it.get("price")))}</span>')
    for k, cls in (('desc', 'dish__desc'), ('add', 'dish__add')):
        v = it.get(k) or {}
        if v.get('en'):
            out += f'<p class="{cls}"><span data-it="{esc(v.get("it") or v["en"])}">{esc(v["en"])}</span></p>'
    return out + '</div>'


def price(p):
    p = (p or '').strip()
    return '$' + p if re.match(r'^\d', p) else p


def swap_picture(inner, open_tag, v, lang):
    """Point a <picture>'s desktop and phone images at new files, keeping every other attribute."""
    def base_of(url):
        return re.sub(r'(-\d+w)?\.(jpe?g|webp|png)$', '', url)

    def fix(tag):
        mob = tag.startswith('<source') and re.search(r'media="[^"]*max-width:760px', tag) is not None
        want = v.get('mob') if mob else v.get('desk')
        if not want:
            return tag
        urls = re.findall(r'(/wp-content/uploads/[^\s",]+)', tag)
        for u in set(urls):
            b = base_of(u)
            if b != want:
                tag = tag.replace(u, want + u[len(b):])
        if tag.startswith('<img'):
            alt = pick(v.get('alt'), lang)
            if alt:
                tag = set_attr(tag, 'alt', esc(alt))
            if not mob and v.get('w') and v.get('h') and re.search(r'\swidth="', tag):
                tag = set_attr(set_attr(tag, 'width', str(v['w'])), 'height', str(v['h']))
        return tag
    return open_tag, re.sub(r'<(?:source|img)\b[^>]*>', lambda m: fix(m.group(0)), inner)


def build_file(path, lang, slots, menus):
    s = open(path, encoding='utf-8').read()
    orig = s

    def text(key, open_tag, inner):
        if key not in slots:
            return None
        v = slots[key]
        new_open = open_tag
        if 'data-it="' in open_tag:
            new_open = set_attr(open_tag, 'data-it', esc(pick(v, 'it')))
        return new_open, esc(pick(v, lang))
    s = replace_all(s, 'data-cms', text)

    s = replace_all(s, 'data-cms-html', lambda k, o, i: (o, clean_html(pick(slots[k], lang))) if k in slots else None)

    def lst(key, open_tag, inner):
        if key not in slots:
            return None
        ind = re.match(r'\s*', inner).group(0) or '\n    '
        tail = re.search(r'\s*$', inner).group(0)
        items = ''.join(f'{ind}<li><span data-it="{esc(pick(x, "it"))}">{esc(pick(x, lang))}</span></li>'
                        for x in slots[key].get('items', []))
        return open_tag, items + tail
    s = replace_all(s, 'data-cms-list', lst)

    def opt(key, open_tag, inner):
        name, cap = slots.get(key + '.name'), slots.get(key + '.cap')
        if not name or not cap:
            return None
        new_open = set_attr(open_tag, 'data-it', esc(f'{pick(name, "it")} · {pick(cap, "it")}'))
        return new_open, esc(f'{pick(name, lang)} · {pick(cap, lang)}')
    s = replace_all(s, 'data-cms-opt', opt)

    s = replace_all(s, 'data-cms-img', lambda k, o, i: swap_picture(i, o, slots[k], lang) if k in slots else None)

    def menu(key, open_tag, inner):
        page, sec = key.split(':', 1)
        secs = {x['id']: x for x in (menus.get(page) or {}).get('sections', [])}
        if sec not in secs:
            return None
        return open_tag, ''.join(dish(it) for it in secs[sec].get('items', []))
    s = replace_all(s, 'data-cms-menu', menu)

    if 'event.start_iso' in slots and 'data-cms-event' in s:
        s = re.sub(r'("startDate": ")[^"]*(")', lambda m: m.group(1) + slots['event.start_iso']['value'] + m.group(2), s)

    if s != orig:
        open(path, 'w', encoding='utf-8').write(s)
        return True
    return False


def main():
    slots, menus = load()
    slots.update(derived(slots))
    changed = []
    for path in glob.glob(os.path.join(SRC, '**', '*.html'), recursive=True):
        rel = os.path.relpath(path, SRC)
        if rel.startswith('admin'):
            continue
        s = open(path, encoding='utf-8').read()
        if 'data-cms' not in s:
            continue
        lang = 'it' if rel.startswith('it' + os.sep) else 'en'
        if build_file(path, lang, slots, menus):
            changed.append(rel)
    print(f'build-cms: {len(changed)} page(s) updated' + (': ' + ', '.join(sorted(changed)) if changed else ''))


if __name__ == '__main__':
    sys.exit(main())
