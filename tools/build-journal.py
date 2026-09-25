#!/usr/bin/env python3
"""Build the Journal (Il Quaderno) from content/journal/, in English and Italian.

Run from the repo root:  python3 tools/build-journal.py

Content lives in two places (see content/journal/README.md):
  content/journal/categories.json   category slug -> {"en": name, "it": name}
  content/journal/posts/<slug>.json one file per post, with an "en" and an "it"
                                    block: title, photo_alt, excerpt, body_html,
                                    seo_title, seo_description (what Google shows)

It writes, and overwrites:
  src/journal/index.html  + src/it/journal/index.html   the list, newest first,
                                                          with category filters
  src/<slug>/index.html   + src/it/<slug>/index.html    one page per post
and refreshes the Journal entries in src/sitemap.xml.

The page chrome (head, header, footer) is taken from an existing page of each
language, so the Journal always matches the rest of the site. Never hand-edit
the generated files: change the JSON and run this again.
"""
import datetime
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'src')
CONTENT = os.path.join(ROOT, 'content', 'journal')
HOST = 'https://amami-italia.vercel.app'          # same canonical host as every page
UP = os.path.join(SRC, 'wp-content', 'uploads')

T = {
    'en': dict(kicker='Journal', sub='Notes on the cooking, the room and Brampton.', all='All', read='Read',
               all_posts='All posts', end='Your table is waiting.', reserve='Reserve a Table',
               reserve_href='/reservation/', posts_label='Posts', cats_label='Categories',
               list_title='Journal — Amami Italia, Brampton',
               list_desc='Notes on the cooking, the room and Brampton, from Amami Italia.',
               months=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                       'September', 'October', 'November', 'December'],
               locale='en_CA', lang='en-CA'),
    'it': dict(kicker='Giornale', sub='Appunti sulla cucina, sulla sala e su Brampton.', all='Tutti', read='Leggi',
               all_posts='Tutti gli articoli', end='Il tuo tavolo ti aspetta.', reserve='Prenota un tavolo',
               reserve_href='/it/reservation/', posts_label='Articoli', cats_label='Categorie',
               list_title='Il Quaderno — Amami Italia, Brampton',
               list_desc='Appunti sulla cucina, sulla sala e su Brampton, da Amami Italia.',
               months=['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto',
                       'settembre', 'ottobre', 'novembre', 'dicembre'],
               locale='it_IT', lang='it-IT'),
}
CHROME = {'en': 'contact/index.html', 'it': 'it/contact/index.html'}   # template page per language


def esc(s):
    return html.escape(s or '', quote=True)


def month(d, lang):
    y, m, _ = d.split('-')
    return f"{T[lang]['months'][int(m) - 1]} {y}"


def url(slug, lang):
    return ('/it' if lang == 'it' else '') + (f'/{slug}/' if slug else '/journal/')


def picture(base, w, h, alt, sizes, cls, eager):
    """<picture> with WebP + JPEG srcsets built from the sizes that exist on disk."""
    rel = base.replace('/wp-content/uploads/', '')
    steps = []
    for n in (480, 800, 1200):
        if os.path.exists(os.path.join(UP, f'{rel}-{n}w.jpg')):
            steps.append((f'{base}-{n}w', n))
    steps.append((base, w))
    jpg = ', '.join(f'{b}.jpg {n}w' for b, n in steps)
    webp = ', '.join(f'{b}.webp {n}w' for b, n in steps
                     if os.path.exists(os.path.join(UP, (b.replace('/wp-content/uploads/', '')) + '.webp')))
    load = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    src = f'<source type="image/webp" srcset="{webp}" sizes="{sizes}">' if webp else ''
    return (f'<picture>{src}<img class="{cls}" src="{base}.jpg" srcset="{jpg}" alt="{esc(alt)}"\n'
            f'       width="{w}" height="{h}" {load} sizes="{sizes}"></picture>')


def chrome(lang):
    return open(os.path.join(SRC, CHROME[lang]), encoding='utf-8').read()


def page(lang, en_url, it_url, title, desc, og_img, og_alt, og_type, main, jsonld=None):
    """Wrap `main` in the language's head/header/footer, with every per-page field set."""
    s = chrome(lang)
    head, rest = s.split('</head>', 1)
    here = en_url if lang == 'en' else it_url
    abs_ = lambda u: HOST + u
    head = re.sub(r'<html[^>]*>', f'<html lang="{T[lang]["lang"]}" data-lang="{lang}">', head, 1)
    head = re.sub(r'<title>[^<]*</title>', f'<title>{esc(title)}</title>', head, 1)
    for pat, val in [(r'(<meta name="description" content=")[^"]*', desc),
                     (r'(<meta property="og:title" content=")[^"]*', title),
                     (r'(<meta property="og:description" content=")[^"]*', desc),
                     (r'(<meta name="twitter:title" content=")[^"]*', title),
                     (r'(<meta name="twitter:description" content=")[^"]*', desc),
                     (r'(<meta property="og:image:alt" content=")[^"]*', og_alt),
                     (r'(<meta name="twitter:image:alt" content=")[^"]*', og_alt)]:
        head = re.sub(pat, lambda m: m.group(1) + esc(val), head, 1)
    for pat in (r'(<meta property="og:image" content=")[^"]*', r'(<meta property="og:image:secure_url" content=")[^"]*',
                r'(<meta name="twitter:image" content=")[^"]*'):
        head = re.sub(pat, lambda m: m.group(1) + og_img, head, 1)
    head = re.sub(r'(<meta property="og:type" content=")[^"]*', lambda m: m.group(1) + og_type, head, 1)
    head = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + abs_(here), head, 1)
    head = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + abs_(here), head, 1)
    head = re.sub(r'(<link rel="alternate" hreflang="en-CA" href=")[^"]*', lambda m: m.group(1) + abs_(en_url), head)
    head = re.sub(r'(<link rel="alternate" hreflang="it" href=")[^"]*', lambda m: m.group(1) + abs_(it_url), head)
    head = re.sub(r'(<link rel="alternate" hreflang="x-default" href=")[^"]*', lambda m: m.group(1) + abs_(en_url), head)
    head = re.sub(r'\n<script type="application/ld\+json">.*?</script>', '', head, flags=re.S)
    if jsonld:
        head += '<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False) + '</script>\n'
    # language switch in the header and the menu overlay
    rest = re.sub(r'(<a href=")[^"]*(" hreflang="en-CA")', lambda m: m.group(1) + en_url + m.group(2), rest)
    rest = re.sub(r'(<a href=")[^"]*(" hreflang="it")', lambda m: m.group(1) + it_url + m.group(2), rest)
    rest = re.sub(r'<main id="main">.*?</main>', lambda m: main, rest, count=1, flags=re.S)
    return head + '</head>' + rest


def write(path, text):
    full = os.path.join(SRC, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(text)


def main():
    cats = json.load(open(os.path.join(CONTENT, 'categories.json'), encoding='utf-8'))
    posts = []
    for f in sorted(os.listdir(os.path.join(CONTENT, 'posts'))):
        if f.endswith('.json'):
            p = json.load(open(os.path.join(CONTENT, 'posts', f), encoding='utf-8'))
            if not p.get('en') or not p.get('it'):
                sys.exit(f'{f}: needs both an "en" and an "it" block')
            if p['category'] not in cats:
                sys.exit(f'{f}: unknown category "{p["category"]}" (add it to categories.json)')
            posts.append(p)
    posts.sort(key=lambda p: p['date'], reverse=True)
    used = [c for c in cats if any(p['category'] == c for p in posts)]

    for lang in ('en', 'it'):
        t = T[lang]
        # --- the list ---
        chips = ''.join(f'<li><a href="{url(None, lang)}#{c}" data-cat="{c}" aria-current="false">{esc(cats[c][lang])}</a></li>'
                        for c in used)
        cards = []
        for p in posts:
            L = p[lang]
            cards.append(f'''    <article class="pg-card" data-cat="{p['category']}">
      {picture(p['photo']['base'], p['photo']['width'], p['photo']['height'], L['photo_alt'], '(max-width:760px) 88vw, 40vw', 'pg-card__img', False)}
      <div class="pg-card__body">
        <h2 class="pg-card__it">{esc(L['title'])}</h2>
        <p class="pg-card__en"><span class="pg-card__cat">{esc(cats[p['category']][lang])}</span> &middot; <time datetime="{p['date']}">{month(p['date'], lang)}</time></p>
        <p class="pg-card__lede">{esc(L['excerpt'])}</p>
        <a class="pg-btn pg-card__cta" href="{url(p['slug'], lang)}">{t['read']}</a>
      </div>
    </article>''')
        main = f'''<main id="main">

<!-- Generated by tools/build-journal.py from content/journal/ — edit the JSON, not this file. -->
<section class="pg-head">
  <p class="pg-head__k">{t['kicker']}</p>
  <h1 class="pg-head__h">Il Quaderno</h1>
  <p class="pg-head__sub">{t['sub']}</p>
  <ul class="pg-anchors pg-anchors--cats" aria-label="{t['cats_label']}"><li><a href="{url(None, lang)}" data-cat="" aria-current="true">{t['all']}</a></li>{chips}</ul>
</section>

<section class="pg-sec pg-sec--tight" aria-label="{t['posts_label']}">
  <div class="pg-cards">
{chr(10).join(cards)}
  </div>
</section>

<section class="pg-end">
  <h2 class="pg-end__h">{t['end']}</h2>
  <a class="pg-btn pg-btn--fill" href="{t['reserve_href']}" data-gtm="reserve">{t['reserve']}</a>
</section>
<script>/* category filter: every post shows without script; with it, a category
   button (or a #category link) shows only that category's posts */
(function(){{var chips=document.querySelectorAll('.pg-anchors--cats a'),cards=document.querySelectorAll('.pg-card[data-cat]');
function show(c){{for(var i=0;i<cards.length;i++)cards[i].hidden=!!c&&cards[i].getAttribute('data-cat')!==c;
for(var j=0;j<chips.length;j++)chips[j].setAttribute('aria-current',chips[j].getAttribute('data-cat')===c?'true':'false');}}
for(var k=0;k<chips.length;k++)chips[k].addEventListener('click',function(e){{e.preventDefault();var c=this.getAttribute('data-cat');
history.replaceState(null,'',c?'#'+c:location.pathname);show(c);}});
function fromHash(){{show(location.hash.slice(1));}}window.addEventListener('hashchange',fromHash);if(location.hash)fromHash();}})();</script>
</main>'''
        first = posts[0]
        write(url(None, lang).lstrip('/') + 'index.html',
              page(lang, '/journal/', '/it/journal/', t['list_title'], t['list_desc'],
                   HOST + first['photo']['base'] + '.jpg', first[lang]['photo_alt'], 'website', main))

        # --- the posts ---
        for p in posts:
            L = p[lang]
            cat = cats[p['category']][lang]
            main = f'''<main id="main">

<!-- Generated by tools/build-journal.py from content/journal/posts/{p['slug']}.json — edit the JSON, not this file. -->
<article>
<section class="pg-hero">
  {picture(p['photo']['base'], p['photo']['width'], p['photo']['height'], L['photo_alt'], '100vw', 'pg-hero__img', True)}
  <div class="pg-hero__scrim" aria-hidden="true"></div>
  <h1 class="pg-hero__h pg-hero__h--post">{esc(L['title'])}</h1>
  <p class="pg-hero__sub"><a href="{url(None, lang)}">Il Quaderno</a> &middot; <a href="{url(None, lang)}#{p['category']}">{esc(cat)}</a> &middot; <time datetime="{p['date']}">{month(p['date'], lang)}</time></p>
</section>

<section class="pg-sec pg-sec--tight">
  <div class="pg-prose">
{L['body_html']}
  </div>
  <p class="pg-sec__cta"><a class="pg-btn pg-btn--red" href="{url(None, lang)}">{t['all_posts']}</a></p>
</section>
</article>

<section class="pg-end">
  <h2 class="pg-end__h">{t['end']}</h2>
  <a class="pg-btn pg-btn--fill" href="{t['reserve_href']}" data-gtm="reserve">{t['reserve']}</a>
</section>
</main>'''
            img = HOST + p['photo']['base'] + '.jpg'
            ld = {'@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': L['title'],
                  'description': L['seo_description'], 'image': img, 'datePublished': p['date'],
                  'inLanguage': T[lang]['lang'], 'articleSection': cat,
                  'mainEntityOfPage': HOST + url(p['slug'], lang),
                  'author': {'@type': 'Organization', 'name': 'Amami Italia'},
                  'publisher': {'@type': 'Organization', 'name': 'Amami Italia',
                                'logo': {'@type': 'ImageObject', 'url': HOST + '/wp-content/uploads/2025/09/amami-logo.png'}}}
            write(url(p['slug'], lang).lstrip('/') + 'index.html',
                  page(lang, url(p['slug'], 'en'), url(p['slug'], 'it'), L['seo_title'], L['seo_description'],
                       img, L['photo_alt'], 'article', main, ld))

    # --- sitemap: drop old Journal entries, add these with their language pairs ---
    sm_path = os.path.join(SRC, 'sitemap.xml')
    sm = open(sm_path, encoding='utf-8').read()
    ours = {'/journal/', '/it/journal/'} | {u for p in posts for u in (url(p['slug'], 'en'), url(p['slug'], 'it'))}
    sm = re.sub(r'\s*<url><loc>' + re.escape(HOST) + r'(/[^<]*)</loc>.*?</url>',
                lambda m: '' if m.group(1) in ours else m.group(0), sm, flags=re.S)
    today = datetime.date.today().isoformat()
    rows = []
    for en_u, it_u, pr in [('/journal/', '/it/journal/', '0.6')] + [(url(p['slug'], 'en'), url(p['slug'], 'it'), '0.5') for p in posts]:
        alt = (f'<xhtml:link rel="alternate" hreflang="en-CA" href="{HOST}{en_u}"/>'
               f'<xhtml:link rel="alternate" hreflang="it" href="{HOST}{it_u}"/>'
               f'<xhtml:link rel="alternate" hreflang="x-default" href="{HOST}{en_u}"/>')
        for u in (en_u, it_u):
            rows.append(f'  <url><loc>{HOST}{u}</loc><lastmod>{today}</lastmod><priority>{pr}</priority>{alt}</url>')
    sm = sm.replace('</urlset>', '\n'.join(rows) + '\n</urlset>')
    open(sm_path, 'w', encoding='utf-8').write(sm)
    print(f'built {len(posts)} posts x 2 languages + 2 list pages; sitemap has {sm.count("<url>")} URLs')


if __name__ == '__main__':
    main()
