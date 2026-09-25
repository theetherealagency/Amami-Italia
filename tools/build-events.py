#!/usr/bin/env python3
"""Build every event page from content/events/<slug>.json, in English and Italian.

Run from the repo root:  python3 tools/build-events.py

Each published event (no "draft": true) gets /events/<slug>/ and
/it/events/<slug>/, made from tools/templates/event.{en,it}.html (the site's
own head, header and footer), plus its entries in src/sitemap.xml. A page whose
event was deleted or turned back into a draft is removed. Pages this script
owns carry <meta name="amami-generated" content="event">; nothing else under
src/events/ is ever touched.

Once an event's date has passed (Toronto time) its page stays up for Google,
without the booking button. The Events page panel and its "More events" list
are filled by tools/build-cms.py from the same files (see upcoming()).
"""
import datetime
import glob
import html
import json
import os
import re
import shutil
import sys
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'src')
EVENTS = os.path.join(ROOT, 'content', 'events')
TPL = os.path.join(ROOT, 'tools', 'templates')
UP = os.path.join(SRC, 'wp-content', 'uploads')
HOST = 'https://amami-italia.vercel.app'          # same canonical host as every page
TZ = ZoneInfo('America/Toronto')
MARK = '<meta name="amami-generated" content="event">'

MONTHS = {'en': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                 'October', 'November', 'December'],
          'it': ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre',
                 'ottobre', 'novembre', 'dicembre']}
DAYS = {'en': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        'it': ['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica']}
T = {
    'en': dict(date='Date', time='Time', where='Where', where_v='Amami Italia, 6261 Mayfield Rd, #140, Brampton, at Airport Road',
               all='All events', end='Your table is waiting.', reserve='Reserve a Table', res='/reservation/', ev='/events/',
               past='This evening took place on {d}.', label='The evening', lang='en-CA'),
    'it': dict(date='Data', time='Ora', where='Dove', where_v='Amami Italia, 6261 Mayfield Rd, #140, Brampton, all’altezza di Airport Road',
               all='Tutti gli eventi', end='Il tuo tavolo ti aspetta.', reserve='Prenota un tavolo', res='/it/reservation/', ev='/it/events/',
               past='Questa serata si è svolta il {d}.', label='La serata', lang='it-IT'),
}


def esc(s):
    return html.escape(s or '', quote=True)


def today():
    return datetime.datetime.now(TZ).date()


def load():
    out = []
    for f in sorted(glob.glob(os.path.join(EVENTS, '*.json'))):
        e = json.load(open(f, encoding='utf-8'))
        name = os.path.basename(f)[:-5]
        if e.get('slug') != name:
            sys.exit(f'{f}: "slug" must match the file name')
        for lang in ('en', 'it'):
            if not (e.get(lang) or {}).get('title'):
                sys.exit(f'{f}: needs a title in "{lang}"')
        if not re.match(r'^\d{4}-\d\d-\d\d$', e.get('date', '')) or not re.match(r'^\d\d:\d\d$', e.get('time', '')):
            sys.exit(f'{f}: needs a date (YYYY-MM-DD) and a time (HH:MM)')
        out.append(e)
    return out


def published(events):
    return sorted([e for e in events if not e.get('draft')], key=lambda e: (e['date'], e['time']))


def upcoming(events):
    """Published events from today on, soonest first; the featured one (if any is still ahead) goes first."""
    t = today().isoformat()
    up = [e for e in published(events) if e['date'] >= t]
    feat = [e for e in up if e.get('featured')]
    if feat:
        up.remove(feat[0])
        up.insert(0, feat[0])
    return up


def long_date(d, lang):
    day = datetime.date.fromisoformat(d)
    if lang == 'it':
        return f'{DAYS["it"][day.weekday()]} {day.day} {MONTHS["it"][day.month - 1]} {day.year}'
    return f'{DAYS["en"][day.weekday()]}, {MONTHS["en"][day.month - 1]} {day.day}, {day.year}'


def clock(t, lang, style='fact'):
    hh, mm = (int(x) for x in t.split(':'))
    if lang == 'en':
        h12 = hh % 12 or 12
        return f'{h12} {"AM" if hh < 12 else "PM"}' if mm == 0 else f'{h12}:{mm:02d} {"AM" if hh < 12 else "PM"}'
    if style == 'sub':
        return f'ore {hh}' if mm == 0 else f'ore {hh}:{mm:02d}'
    if style == 'card':
        return f'Ore {hh}:{mm:02d}'
    return f'{hh}:{mm:02d}'


def url(slug, lang):
    return ('/it' if lang == 'it' else '') + f'/events/{slug}/'


def have(base, suffix):
    return os.path.exists(os.path.join(UP, base.replace('/wp-content/uploads/', '') + suffix))


def srcset(base, widths, ext):
    got = [(w, f'{base}-{w}w.{ext}') for w in widths if have(base, f'-{w}w.{ext}')]
    return ', '.join(f'{u} {w}w' for w, u in got)


def hero(e, lang):
    desk = e['photo']['desk']
    mob = e['photo'].get('mob') or desk
    alt = esc(e[lang].get('photo_alt') or e[lang]['title'])
    src = next((f'{desk}{x}' for x in ('-1200w.jpg', '-800w.jpg', '.jpg') if have(desk, x)), desk + '.jpg')
    w, h = e['photo'].get('w') or 1200, e['photo'].get('h') or 1065
    return (f'<picture><source media="(max-width:760px)" type="image/webp" srcset="{srcset(mob, (480, 800, 1200), "webp")}" sizes="100vw">'
            f'<source type="image/webp" srcset="{srcset(desk, (800, 1200, 1600, 2000), "webp")}" sizes="100vw">'
            f'<img class="pg-hero__img" src="{src}" alt="{alt}" width="{w}" height="{h}" fetchpriority="high" decoding="async"></picture>')


def main_html(e, lang):
    t, L = T[lang], e[lang]
    past = e['date'] < today().isoformat()
    cta = (f'  <p class="pg-sec__cta"><a class="pg-btn pg-btn--fill" href="{t["res"]}" data-gtm="{esc(e.get("gtm") or e["slug"] + "-reserve")}">'
           f'{esc(L.get("cta") or t["reserve"])}</a></p>\n') if not past else \
          f'  <p class="pg-sec__cta">{esc(t["past"].format(d=long_date(e["date"], lang)))}</p>\n'
    after = f'  <div class="pg-prose">{L["after_html"]}</div>\n' if (L.get('after_html') or '').strip() else ''
    return f'''<main id="main">

<!-- Event page, built from content/events/{e["slug"]}.json by tools/build-events.py. Edit it in the admin portal. -->
<section class="pg-hero">
  {hero(e, lang)}
  <div class="pg-hero__scrim" aria-hidden="true"></div>
  <h1 class="pg-hero__h">{esc(L["title"])}</h1>
  <p class="pg-hero__sub">{esc(long_date(e["date"], lang))} · {esc(clock(e["time"], lang, "sub"))}</p>
</section>

<section class="pg-sec pg-sec--tight" aria-label="{t["label"]}">
  <div class="pg-prose">
    {(L.get("intro_html") or "").strip()}
  </div>
  <dl class="pg-facts pg-facts--3"><div class="pg-fact"><dt>{t["date"]}</dt><dd>{esc(long_date(e["date"], lang))}</dd></div><div class="pg-fact"><dt>{t["time"]}</dt><dd>{esc(clock(e["time"], lang))}</dd></div><div class="pg-fact"><dt>{t["where"]}</dt><dd>{esc(t["where_v"])}</dd></div></dl>
{cta}{after}  <p class="pg-sec__cta"><a class="pg-btn pg-btn--red" href="{t["ev"]}">{t["all"]}</a></p>
</section>

<section class="pg-end">
  <h2 class="pg-end__h">{t["end"]}</h2>
  <a class="pg-btn pg-btn--fill" href="{t["res"]}" data-gtm="reserve">{t["reserve"]}</a>
</section>
</main>'''


def og_image(e):
    if e.get('og_image'):
        return e['og_image']
    base = e['photo']['desk']
    return base + ('-1200x630.jpg' if have(base, '-1200x630.jpg') else '-1200w.jpg')


def page(e, lang):
    tpl = open(os.path.join(TPL, f'event.{lang}.html'), encoding='utf-8').read()
    L = e[lang]
    title = L.get('seo_title') or f'{L["title"]} | Amami Italia'
    desc = L.get('seo_description') or L.get('summary') or ''
    hh, mm = (int(x) for x in e['time'].split(':'))
    d = datetime.date.fromisoformat(e['date'])
    start = datetime.datetime(d.year, d.month, d.day, hh, mm, tzinfo=TZ).isoformat()
    ld = {'@context': 'https://schema.org', '@type': 'Event', 'name': L['title'],
          'description': L.get('ld_description') or desc, 'startDate': start,
          'eventStatus': 'https://schema.org/EventScheduled',
          'eventAttendanceMode': 'https://schema.org/OfflineEventAttendanceMode',
          'image': HOST + og_image(e), 'inLanguage': T[lang]['lang'],
          'location': {'@type': 'Restaurant', 'name': 'Amami Italia', 'servesCuisine': 'Italian',
                       'address': {'@type': 'PostalAddress', 'streetAddress': '6261 Mayfield Rd, #140', 'addressLocality': 'Brampton',
                                   'addressRegion': 'ON', 'postalCode': 'L6P 0X9', 'addressCountry': 'CA'},
                       'telephone': '+1-905-794-3366',
                       'areaServed': ['Brampton', 'Castlemore', 'Caledon', 'Bolton', 'Vaughan', 'Peel Region']},
          'organizer': {'@type': 'Organization', 'name': 'Amami Italia', 'url': HOST + '/'},
          'offers': {'@type': 'Offer', 'url': HOST + T[lang]['res'], 'availability': 'https://schema.org/LimitedAvailability'}}
    out = tpl
    for k, v in (('TITLE', esc(title)), ('DESC', esc(desc)), ('OG_IMAGE', HOST + og_image(e)),
                 ('OG_ALT', esc(L.get('og_alt') or L.get('photo_alt') or L['title'])),
                 ('JSONLD', json.dumps(ld, ensure_ascii=False).replace('</', '<\\/')), ('SLUG', e['slug'])):
        out = out.replace('{{' + k + '}}', v)
    return out.replace('{{MAIN}}', main_html(e, lang))


def main():
    events = load()
    pub = published(events)
    live = set()
    for e in pub:
        for lang in ('en', 'it'):
            rel = url(e['slug'], lang).strip('/')
            live.add(rel)
            path = os.path.join(SRC, rel, 'index.html')
            new = page(e, lang)
            old = open(path, encoding='utf-8').read() if os.path.exists(path) else None
            if old is not None and MARK not in old and 'amami-generated' not in old and e['slug'] != 'bistecca-alla-fiorentina':
                sys.exit(f'{rel}/ exists and was not made by this script; pick another address')
            if old != new:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                open(path, 'w', encoding='utf-8').write(new)
    # remove pages whose event is gone or back to draft (only pages this script made)
    for base in ('events', os.path.join('it', 'events')):
        for d in sorted(os.listdir(os.path.join(SRC, base))):
            full = os.path.join(SRC, base, d, 'index.html')
            rel = os.path.join(base, d).replace(os.sep, '/')
            if os.path.isfile(full) and rel not in live and MARK in open(full, encoding='utf-8').read():
                shutil.rmtree(os.path.dirname(full))
                print(f'removed {rel}/ (no longer published)')
    # sitemap
    sm_path = os.path.join(SRC, 'sitemap.xml')
    sm = open(sm_path, encoding='utf-8').read()
    ours = re.compile(re.escape(HOST) + r'(?:/it)?/events/[a-z0-9-]+/</loc>')
    sm = re.sub(r'\s*<url><loc>[^<]*</loc>.*?</url>', lambda m: '' if ours.search(m.group(0)) else m.group(0), sm, flags=re.S)
    rows = []
    for e in pub:
        en_u, it_u = HOST + url(e['slug'], 'en'), HOST + url(e['slug'], 'it')
        alt = (f'<xhtml:link rel="alternate" hreflang="en-CA" href="{en_u}"/><xhtml:link rel="alternate" hreflang="it" href="{it_u}"/>'
               f'<xhtml:link rel="alternate" hreflang="x-default" href="{en_u}"/>')
        for u in (en_u, it_u):
            rows.append(f'  <url><loc>{u}</loc><lastmod>{e.get("modified") or e["date"]}</lastmod><priority>0.7</priority>{alt}</url>')
    if rows:
        sm = sm.replace('</urlset>', '\n'.join(rows) + '\n</urlset>')
    open(sm_path, 'w', encoding='utf-8').write(sm)
    print(f'build-events: {len(pub)} published event(s), {len(upcoming(events))} upcoming')


if __name__ == '__main__':
    main()
