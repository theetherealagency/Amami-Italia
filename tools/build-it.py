# Regenerates the static Italian tree (/it/**) from the English pages.
#   cd src && python3 ../tools/build-it.py
# Idempotent. Italian copy comes from data-it attributes in the EN source, page
# titles from data-title-it on <html>, meta descriptions / OG alts from the dicts
# below. Also converts any leftover EN|IT buttons to links, adds hreflang to the
# seven EN pages, rewrites the sitemap alternates and gates amami-i18n.js.
#
# Run it after ANY edit to one of the seven English pages, then commit src/it/.
import re, glob, html, os

HOST = "https://amami-italia.vercel.app"
PAGES = {  # EN path -> IT path
    "/": "/it/", "/menu/": "/it/menu/", "/our-story/": "/it/our-story/", "/after-dark/": "/it/after-dark/",
    "/events/": "/it/events/", "/reservation/": "/it/reservation/", "/contact/": "/it/contact/",
}
IT_DESC = {
    "/": "Cucina toscana a Brampton, dalla Chef Isabella Comello. Pasta, vino e serate lunghe su Mayfield Road.",
    "/menu/": "Pasta tirata ogni mattina, bistecca frollata quarantacinque giorni in casa, trentadue piatti secondo lo standard APCI. I menù di Amami Italia, Brampton.",
    "/our-story/": "Da Lucca a Brampton: una sala toscana a Brampton, aperta nel novembre 2025, con la Chef Isabella Comello in cucina. Autenticità italiana certificata APCI.",
    "/after-dark/": "After Dark da Amami Italia, Brampton: la stessa sala, più tardi. Quarantatré etichette al bicchiere — amaro, grappa, porto, caffè corretto — musica dal vivo quasi ogni fine settimana, uso esclusivo per 30 seduti o 60 in piedi.",
    "/events/": "Quattro spazi privati per fino a 120 ospiti da Amami Italia, Brampton: una sala privata a porte chiuse, una tavolata, il salotto e l’intero locale. Menù fissi costruiti intorno alla vostra serata.",
    "/reservation/": "Prenota un tavolo da Amami Italia a Brampton. Prenota online con OpenTable o chiama il 905-794-3366. Abito semi-formale per il servizio serale; gruppi da otto in su per telefono.",
    "/contact/": "Amami Italia, 6261 Mayfield Rd #140, Brampton — all’angolo tra Airport Rd e Mayfield Rd, con parcheggio pubblico. Orari, telefono, email e indicazioni.",
}
IT_OGALT = {
    "/": "La sala di sera, il bar sullo sfondo", "/menu/": "Pasta rifinita al pass", "/our-story/": "La sala, luce calda sotto la pergola",
    "/after-dark/": "Luce calda sul salotto", "/events/": "Il tavolo privato sotto gli specchi", "/reservation/": "I divanetti curvi accanto alle finestre",
    "/contact/": "Il bancone del bar e la sala",
}


def esc_attr(t): return html.escape(t, quote=True)
def esc_text(t): return html.escape(t, quote=False)


def url_of(file):
    return "/" + file.replace("index.html", "")


def switch_links(en_url, it_url, active):
    a = lambda l: 'aria-current="true"' if l == active else 'aria-current="false"'
    return (f'<a href="{en_url}" hreflang="en-CA" lang="en" {a("en")}>EN</a><i aria-hidden="true">|</i>'
            f'<a href="{it_url}" hreflang="it" lang="it" {a("it")}>IT</a>')


def panel_links(en_url, it_url, active):
    a = lambda l: 'aria-current="true"' if l == active else 'aria-current="false"'
    return (f'<a href="{en_url}" hreflang="en-CA" lang="en" {a("en")}><span data-it="English">English</span></a>\n        '
            f'<a href="{it_url}" hreflang="it" lang="it" {a("it")}><span data-it="Italiano">Italiano</span></a>')


RX_SWITCH = re.compile(r'<button type="button" data-lang-set="en" lang="en">EN</button>\s*<i aria-hidden="true">\|</i>\s*<button type="button" data-lang-set="it" lang="it">IT</button>')
RX_PANEL = re.compile(r'<button type="button" data-lang-set="en"><span data-it="English">English</span></button>\s*<button type="button" data-lang-set="it"><span data-it="Italiano">Italiano</span></button>')


def convert_switch(s, en_url, it_url, active):
    s = RX_SWITCH.sub(switch_links(en_url, it_url, active), s)
    s = RX_PANEL.sub(panel_links(en_url, it_url, active), s)
    return s


def hreflang_block(en_url, it_url):
    return (f'<link rel="alternate" hreflang="en-CA" href="{HOST}{en_url}">\n'
            f'<link rel="alternate" hreflang="it" href="{HOST}{it_url}">\n'
            f'<link rel="alternate" hreflang="x-default" href="{HOST}{en_url}">\n')


def add_hreflang(head, en_url, it_url):
    head = re.sub(r'\n?<link rel="alternate" hreflang="[^"]*" href="[^"]*">', '', head)  # idempotent
    return re.sub(r'(<link rel="canonical" href="[^"]*">\n?)', lambda m: m.group(1) + hreflang_block(en_url, it_url), head, count=1)


# ---------- 1. every EN page: html[data-lang="en"], switch -> links ----------
files = sorted(f for f in glob.glob("**/*.html", recursive=True) if not f.startswith("it/"))
touched = 0
for f in files:
    s = open(f, encoding="utf-8").read()
    m = re.search(r'<html[^>]*>', s)
    if not m:
        continue
    o = s
    tag = m.group(0)
    if "data-lang=" not in tag:
        s = s.replace(tag, tag[:-1] + ' data-lang="en">', 1)
    en_url = url_of(f)
    it_url = PAGES.get(en_url, "/it/")
    s = convert_switch(s, en_url, it_url, "en")
    if en_url in PAGES:
        i = s.find("</head>"); s = add_hreflang(s[:i], en_url, it_url) + s[i:]
    if s != o:
        open(f, "w", encoding="utf-8").write(s); touched += 1
print("EN files touched:", touched, "of", len(files))

# ---------- 2. the Italian tree ----------
RX_LEAF = re.compile(r'<(\w+)([^>]*?\sdata-it="([^"]*)"[^>]*)>([^<]*)</\1>')


def bake(body):
    def rep(m):
        it = html.unescape(m.group(3))
        return f'<{m.group(1)}{m.group(2)}>{esc_text(it)}</{m.group(1)}>'
    body = RX_LEAF.sub(rep, body)

    def ph(m):
        tag = m.group(0); itv = re.search(r'data-it-placeholder="([^"]*)"', tag).group(1)
        return re.sub(r'placeholder="[^"]*"', f'placeholder="{itv}"', tag, count=1)
    body = re.sub(r'<(?:input|textarea)\b[^>]*data-it-placeholder="[^"]*"[^>]*>', ph, body)
    return body


def rewrite_links(body):
    for en, it in PAGES.items():
        body = body.replace(f'href="{en}"', f'href="{it}"')
    return body


written = []
for en_url, it_url in PAGES.items():
    src = ("index.html" if en_url == "/" else en_url.strip("/") + "/index.html")
    s = open(src, encoding="utf-8").read()
    i = s.find("</head>"); head, rest = s[:i], s[i:]
    title_it = re.search(r'data-title-it="([^"]*)"', head).group(1)
    head = re.sub(r'<html[^>]*>', lambda m: re.sub(r'\slang="[^"]*"', ' lang="it-IT"', re.sub(r'\sdata-lang="[^"]*"', ' data-lang="it"', m.group(0))), head, count=1)
    head = re.sub(r'<title>.*?</title>', f'<title>{title_it}</title>', head, count=1, flags=re.S)
    desc = esc_attr(IT_DESC[en_url]); alt = esc_attr(IT_OGALT[en_url])
    head = re.sub(r'(<meta name="description" content=")[^"]*', r'\g<1>' + desc, head, count=1)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*', r'\g<1>' + desc, head, count=1)
    head = re.sub(r'(<meta name="twitter:description" content=")[^"]*', r'\g<1>' + desc, head, count=1)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', r'\g<1>' + title_it, head, count=1)
    head = re.sub(r'(<meta name="twitter:title" content=")[^"]*', r'\g<1>' + title_it, head, count=1)
    head = re.sub(r'(<meta property="og:image:alt" content=")[^"]*', r'\g<1>' + alt, head, count=1)
    head = re.sub(r'(<meta name="twitter:image:alt" content=")[^"]*', r'\g<1>' + alt, head, count=1)
    head = re.sub(r'(<meta property="og:locale" content=")[^"]*', r'\g<1>it_IT', head, count=1)
    head = re.sub(r'(<link rel="canonical" href=")[^"]*', r'\g<1>' + HOST + it_url, head, count=1)
    head = re.sub(r'(<meta property="og:url" content=")[^"]*', r'\g<1>' + HOST + it_url, head, count=1)
    head = add_hreflang(head, en_url, it_url)
    head = re.sub(r'"inLanguage":\s*"[^"]*"', '"inLanguage": "it"', head)
    rest = bake(rest)
    rest = rewrite_links(rest)
    # the EN half of the switch must keep pointing at the English page
    rest = rest.replace(f'<a href="{it_url}" hreflang="en-CA"', f'<a href="{en_url}" hreflang="en-CA"')
    rest = rest.replace('aria-label="Language"', 'aria-label="Lingua"')
    rest = re.sub(r'aria-current="true"', 'aria-current="false"', rest)
    rest = rest.replace(f'<a href="{it_url}" hreflang="it" lang="it" aria-current="false">', f'<a href="{it_url}" hreflang="it" lang="it" aria-current="true">')
    out = "it" + ("/index.html" if en_url == "/" else en_url.rstrip("/") + "/index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(head + rest)
    written.append((out, len(RX_LEAF.findall(s)), rest.count('href="/it/')))
for w in written:
    print("wrote", w[0], "| data-it baked:", w[1], "| /it/ links:", w[2])

# ---------- 3. sitemap ----------
sm = open("sitemap.xml", encoding="utf-8").read()
if "xmlns:xhtml" not in sm:
    sm = sm.replace('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml"', 1)


def alts(en_url, it_url):
    return (f'<xhtml:link rel="alternate" hreflang="en-CA" href="{HOST}{en_url}"/>'
            f'<xhtml:link rel="alternate" hreflang="it" href="{HOST}{it_url}"/>'
            f'<xhtml:link rel="alternate" hreflang="x-default" href="{HOST}{en_url}"/>')


sm = re.sub(r'<xhtml:link[^>]*/>', '', sm)
sm = re.sub(r'\n  <url><loc>' + re.escape(HOST) + r'/it/[^<]*</loc>.*?</url>', '', sm)
for en_url, it_url in PAGES.items():
    rx = re.compile(r'(<url><loc>' + re.escape(HOST + en_url) + r'</loc>)(<lastmod>[^<]*</lastmod>)(<priority>([^<]*)</priority></url>)')
    m = rx.search(sm)
    if not m:
        print("sitemap: no EN entry for", en_url, "— add one by hand"); continue
    pr = m.group(4)
    sm = sm.replace(m.group(0), m.group(1) + m.group(2) + m.group(3).replace("</url>", alts(en_url, it_url) + "</url>")
                    + f'\n  <url><loc>{HOST}{it_url}</loc>{m.group(2)}<priority>{pr}</priority>{alts(en_url, it_url)}</url>', 1)
open("sitemap.xml", "w", encoding="utf-8").write(sm)
print("sitemap /it/ entries:", sm.count("<loc>" + HOST + "/it/"))

# ---------- 4. i18n.js: a page that names its language is left alone ----------
j = open("_assets/amami-i18n.js", encoding="utf-8").read()
if 'hasAttribute("data-lang")' not in j:
    j = j.replace('  var root = document.documentElement;\n',
                  '  var root = document.documentElement;\n'
                  '  /* Pages built in one language (html[data-lang]) keep it; the EN | IT\n'
                  '     switch on them is a pair of links to the counterpart page, so there\n'
                  '     is nothing to swap here. */\n'
                  '  if (root.hasAttribute("data-lang")) return;\n', 1)
    open("_assets/amami-i18n.js", "w", encoding="utf-8").write(j)

# ---------- 5. leftovers ----------
left = [f for f in glob.glob("**/*.html", recursive=True) if 'data-lang-set' in open(f, encoding="utf-8").read()]
print("files still containing data-lang-set buttons:", left, len(left))
