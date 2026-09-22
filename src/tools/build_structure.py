#!/usr/bin/env python3
"""
Amami Italia — structural build.

Generates every URL in Amami_Italia_Website_Architecture.pdf (31 URLs, 11
templates) as static HTML with one shared stylesheet and one shared script.

WHY A GENERATOR AND NOT 31 HAND-WRITTEN FILES: the header, the full-screen
nav, the sticky mobile bar and the four-column footer are global elements in
the spec. Hand-copied into 31 pages they drift within a week. Edit this file
and re-run it; never edit a generated page.

WHAT IT DOES NOT DO: it does not touch the existing WordPress capture. Old
URLs keep working, so nothing breaks while the new structure is reviewed. The
redirect map (spec section 18) is a separate step.

MISSING MEDIA: every image and video the spec asks for that does not exist in
wp-content/uploads is rendered as a labelled placeholder naming the shoot and
the crop, so the gaps are visible and briefable rather than silently blank.
"""
import datetime
import json, pathlib, html
import re
from menu_data import MENUS, LEGEND_NOTES
from i18n_it import IT

# A text node in the HTML carries the source's line breaks and indentation, so
# any dictionary key written across more than one line never matched. Both
# sides are looked up with their internal whitespace collapsed.
IT_LOOKUP = {" ".join(k.split()): v for k, v in IT.items()}
from media_map import MEDIA, GALLERY

ROOT = pathlib.Path(__file__).resolve().parent.parent

SITE = {
    "name": "Amami Italia",
    "tagline": "Tuscan restaurant, lounge & catering in Brampton",
    "street": "6261 Mayfield Rd, #140",
    "city": "Brampton, ON L6P 0X9",
    "phone_display": "905-794-3366",
    "phone_href": "tel:+19057943366",
    "email": "info@amamiitalia.com",
    "instagram": "https://www.instagram.com/amamiitalia_official",
    "opentable": "https://www.opentable.ca/booking/restref/availability?lang=en-CA&restRef=1470808&otSource=Restaurant%20website",
    "maps": "https://www.google.com/maps/dir/?api=1&destination=6261+Mayfield+Rd+%23140,+Brampton,+ON+L6P+0X9",
    "logo": "/wp-content/uploads/2025/09/amami-logo.png",
}

# The Apps Script web app every form on the site posts to (apps-script/forms.gs).
# Empty until it is deployed — while it is empty the forms fall back to opening a
# pre-filled email to info@amamiitalia.com, so an enquiry still reaches someone.
# Setup steps: FORMS-SETUP.md.
FORMS_ENDPOINT = ""

# The origin every absolute URL is built from — canonical, og:url, the share
# images and the schema. It is the Vercel deployment today; flip this one line
# to https://www.amamiitalia.com when the domain is cut over.
ORIGIN = "https://amami-italia.vercel.app"

# The container that already runs on the WordPress site, so the new build
# reports into the same place. Everything else — GA4, the Meta pixel, the
# conversion tags — is configured inside it rather than hard-coded here.
GTM_ID = "GTM-MNHMB7C9"
GTM_HEAD = ("<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':"
            "new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],"
            "j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src="
            "'https://www.googletagmanager.com/gtm.js?id='+i+dl;"
            "f.parentNode.insertBefore(j,f);})"
            "(window,document,'script','dataLayer','%s');</script>\n" % GTM_ID)
GTM_BODY = ('<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=%s"'
            ' height="0" width="0" style="display:none;visibility:hidden"></iframe>'
            "</noscript>\n" % GTM_ID)

# One source for hours — header, footer, Visit page and schema all read this.
HOURS = {"sun": [12, 21], "mon": None, "tue": [12, 22], "wed": [12, 22],
         "thu": [12, 22], "fri": [12, 23], "sat": [12, 23]}
HOURS_ROWS = [("Monday", "Closed"), ("Tuesday – Thursday", "12pm – 10pm"),
              ("Friday – Saturday", "12pm – 11pm"), ("Sunday", "12pm – 9pm")]

NAV = [("Menu", "/menu/"), ("Our Story", "/our-story/"), ("After Dark", "/after-dark/"),
       ("Events", "/events/"), ("Reservations", "/reservation/")]

EXPLORE = [("Menu", "/menu/"), ("Our Story", "/our-story/"), ("After Dark", "/after-dark/"),
           ("Events", "/events/"), ("Catering", "/catering/"),
           ("Journal", "/journal/"), ("Gift Cards", "/gift-cards/"),
           ("Careers", "/careers/"), ("Press", "/press/"),
           ("Visit", "/visit/"), ("FAQ", "/visit/faq/"), ("Contact", "/visit/contact/")]

LEGAL = [("Privacy", "/legal/privacy/"), ("Cookies", "/legal/cookies/"),
         ("Accessibility", "/legal/accessibility/"),
         ("Reservation Terms", "/legal/reservation-terms/"),
         ("Gift Card Terms", "/legal/gift-card-terms/"),
         ("Terms of Use", "/legal/terms/")]


def slug(t):
    """Anchor id from a course name."""
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


# A slot with no file yet, where the reason matters enough to say on the page.
SLOT_NOTE = {
    "chef_isabella": (
        "Chef Isabella",
        "Candid or direct-flash portrait of Chef Isabella in her own kitchen — flour "
        "on the counter, a plate in her hand. Not a posed corporate headshot. The two "
        "chef photographs already in the library are of the previous chef and carry "
        "his name on the jacket, so neither can stand in here."),
}


def img(slot, kind="wide", loading="lazy", sizes="100vw"):
    """A real photograph if we have one for this slot, else a labelled gap."""
    if slot not in MEDIA:
        note = SLOT_NOTE.get(slot)
        if note:
            return ph(note[0], note[1], kind, 1)
        return ph(slot.replace("_", " "), "No file for this slot yet.", kind)
    src, alt = MEDIA[slot]
    return ('<img class="media media--%s" src="%s" alt="%s" loading="%s" '
            'decoding="async" sizes="%s">' % (kind, src, html.escape(alt), loading, sizes))


def panel(word, sub, href, label, slot=None, video=None, first=False, over="",
          actions=None):
    """One home panel: photograph, one large word, one action.

    The reference stacks these as inset cards with the brand ground showing
    around them — except the hero, which runs edge to edge and full height with
    a line above the name and no button, because the header already carries
    Reserve. `first` gets that treatment; `over` is the line above the word.
    """
    if video:
        src, alt = MEDIA[video]
        bg = ('<video class="panel__media" autoplay muted loop playsinline '
              'preload="metadata" aria-label="%s"><source src="%s" type="video/mp4"></video>'
              % (html.escape(alt), src))
    elif slot in MEDIA:
        src, alt = MEDIA[slot]
        bg = ('<img class="panel__media" src="%s" alt="%s" %s decoding="async" sizes="100vw">'
              % (src, html.escape(alt), 'fetchpriority="high"' if first else 'loading="lazy"'))
    else:
        bg = '<div class="panel__media panel__media--gap">%s</div>' % ph(
            word, "Full-bleed panel background.", "hero")
    tag = "h1" if first else "h2"
    if actions:
        # The hero carries the client's two actions (2026-09-03). Everything
        # below it still gets the single ghost button.
        action = ('<div class="panel__act">%s</div>'
                  % "".join('<a class="btn btn--ghost" href="%s">%s</a>' % (h, l)
                            for h, l in actions))
    elif first:
        action = ""
    else:
        action = '<a class="btn btn--ghost" href="%s">%s</a>' % (href, label)
    return """<section class="panel%s">
  %s
  <div class="panel__inner">
    %s
    <%s class="panel__word%s">%s</%s>
    %s
    %s
  </div>
</section>""" % (" panel--first" if first else "", bg,
                 '<p class="panel__over">%s</p>' % over if over else "",
                 tag, " panel__word--line" if len(word.split()) > 2 else "", word, tag,
                 '<p class="panel__sub">%s</p>' % sub if sub else "", action)


def mosaic(title, copy, facts, slots):
    """The room-and-copy block from the reference: an edge-to-edge photo mosaic
    with one dark text panel carrying a bold name, copy and a capacity line."""
    tiles = "".join('<div class="mosaic__tile">%s</div>' % img(s, "tile") for s in slots)
    fact = "".join('<p class="mosaic__fact"><strong>%s</strong> %s</p>' % (k, v) for k, v in facts)
    return """<section class="mosaic">
  <div class="mosaic__grid">%s</div>
  <div class="mosaic__text">
    <h2 class="mosaic__name">%s</h2>
    <p>%s</p>
    %s
  </div>
</section>""" % (tiles, title, copy, fact)


def ph(what, spec, kind="wide", shoot=None):
    """A visible, briefable gap where an asset is still to be shot."""
    tag = f"Shoot {shoot}" if shoot else "Asset required"
    return (f'<div class="ph ph--{kind}">'
            f'<span class="ph__label">{tag}</span>'
            f'<span class="ph__what">{html.escape(what)}</span>'
            f'<span class="ph__spec">{html.escape(spec)}</span></div>')


def form_attrs(kind):
    """The attributes that connect a form to the handler, plus the honeypot and
    the status line the script writes into."""
    return ' data-amami-form="%s" data-endpoint="%s" data-mailto="%s"' % (
        kind, FORMS_ENDPOINT, SITE["email"])


FORM_TAIL = ('<input type="text" name="company_website" tabindex="-1" autocomplete="off" '
             'aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px">'
             '<p class="form-status" role="status" aria-live="polite"></p>')


def cta(kind):
    """Primary action buttons. One booking system per revenue line (spec 1.1 #5)."""
    if kind == "reserve":
        # The reservation page published 2026-08-20 carries the OpenTable
        # widget, so Reserve lands there rather than jumping off-site.
        return '<a class="btn btn--solid" href="/reservation/" data-gtm="reserve">Reserve a Table</a>'
    if kind == "lounge":
        # There is no Toast account to link to. Lounge tables run through the
        # same OpenTable booking as the dining room.
        return '<a class="btn btn--solid" href="/reservation/" data-gtm="lounge">Reserve a Table</a>'
    if kind == "event":
        return '<a class="btn btn--solid" href="/events/#enquiry" data-gtm="event-enquiry">Event Enquiry</a>'
    if kind == "catering":
        return '<a class="btn btn--solid" href="/catering/#enquiry" data-gtm="catering-enquiry">Catering Enquiry</a>'
    if kind == "directions":
        return f'<a class="btn btn--solid" href="{SITE["maps"]}" target="_blank" rel="noopener">Get Directions</a>'
    if kind == "purchase":
        return '<a class="btn btn--solid" href="/gift-cards/#buy">Buy a Gift Card</a>'
    if kind == "apply":
        return '<a class="btn btn--solid" href="/careers/#apply">Apply</a>'
    if kind == "media":
        return '<a class="btn btn--solid" href="/press/#media">Media Enquiry</a>'
    if kind == "menu":
        return '<a class="btn btn--solid" href="/menu/">See the Menu</a>'
    return ""



# Which real photograph fronts each page. Anything not listed falls back to a gap.
HERO_SLOT = {
    "/after-dark/": "room_lounge", "/events/": "room_private",
    "/catering/": "table_setting", "/visit/": "room_evening",
    # /our-story/chef/ deliberately has NO hero photograph. The only two chef
    # pictures in the library (chef_plate, chef_kitchen) are both of Gianluca
    # Martinucci, with his name embroidered on the jacket — see ASSET-CREDITS.md.
    # The page falls through to a labelled placeholder until Isabella is shot.
    "/gift-cards/": "wine_table", "/menu/dining/": "pasta_finish",
    "/menu/pizza/": "pizza", "/menu/after-dark/": "cocktail_smoke",
    "/menu/wine/": "wine_pour", "/menu/cocktails/": "cocktail_smoke",
    "/menu/tasting/": "dish_dark", "/menu/catering/": "table_setting",
}


NEEDS_SHOOT = {
    "/our-story/chef/":
        ("Chef Isabella — hero", "Landscape, full bleed. To shoot."),
}


def hero_media(page, shoot=3):
    """Full-bleed hero: a real photograph where we have one for this page."""
    slot = HERO_SLOT.get(page["url"])
    if slot:
        return img(slot, "hero", loading="eager")
    named = NEEDS_SHOOT.get(page["url"])
    if named:
        return ph(named[0], named[1], "hero", 1)
    return ph(page["nav_label"] + " hero", "Full-bleed landscape, evening light.", "hero", shoot)


SHARE_SLOTS = {"room_wide", "room_evening", "room_lounge", "room_private", "room_bar",
               "room_booths", "table_setting", "pasta_finish", "pasta_truffle", "dish_dark",
               "cocktail_smoke", "wine_pour", "wine_table", "server_wine",
               "pizza"}


def share_image(page):
    """The 1200x630 card a link preview or an ad creative will use.

    Every photograph in the library is portrait, so the wide crops are built
    once by tools/make_share_images.py and pointed at here — a portrait handed
    to Facebook, WhatsApp or an ad platform gets cropped through the middle of
    the subject.
    """
    slot = page.get("share") or HERO_SLOT.get(page["url"]) or "room_evening"
    if slot not in SHARE_SLOTS:
        slot = "room_evening"
    alt = MEDIA[slot][1]
    return ORIGIN + "/_assets/share/%s.jpg" % slot, alt


def schema(page):
    """Structured data. The Restaurant record on the home page carries the
    facts an ad platform, a map card or an answer engine asks for; inner pages
    carry their breadcrumb trail. Hours come from the same HOURS map the header
    and footer read, so they cannot drift."""
    blocks = []
    if page["url"] == "/":
        days = {"mon": "Monday", "tue": "Tuesday", "wed": "Wednesday", "thu": "Thursday",
                "fri": "Friday", "sat": "Saturday", "sun": "Sunday"}
        opens = [{"@type": "OpeningHoursSpecification", "dayOfWeek": days[k],
                  "opens": "%02d:00" % v[0], "closes": "%02d:00" % v[1]}
                 for k, v in HOURS.items() if v]
        street, city = SITE["street"], SITE["city"]
        locality, rest = city.split(",", 1)
        region, postal = rest.strip().split(" ", 1)
        blocks.append({
            "@context": "https://schema.org",
            "@type": "Restaurant",
            "@id": ORIGIN + "/#restaurant",
            "name": SITE["name"],
            "description": SITE["tagline"] + ".",
            "url": ORIGIN + "/",
            "image": [share_image(page)[0]],
            "logo": ORIGIN + SITE["logo"],
            "telephone": "+1-905-794-3366",
            "email": SITE["email"],
            "priceRange": "$$$",
            "servesCuisine": ["Italian", "Tuscan"],
            "address": {"@type": "PostalAddress", "streetAddress": street,
                        "addressLocality": locality.strip(), "addressRegion": region,
                        "postalCode": postal, "addressCountry": "CA"},
            "openingHoursSpecification": opens,
            "acceptsReservations": ORIGIN + "/reservation/",
            "hasMenu": ORIGIN + "/menu/",
            "sameAs": [SITE["instagram"]],
        })
    if page.get("crumbs"):
        items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": ORIGIN + "/"}]
        for n, (label, url) in enumerate(page["crumbs"], start=2):
            items.append({"@type": "ListItem", "position": n, "name": label,
                          "item": ORIGIN + url})
        items.append({"@type": "ListItem", "position": len(items) + 1,
                      "name": page["nav_label"], "item": ORIGIN + page["url"]})
        blocks.append({"@context": "https://schema.org", "@type": "BreadcrumbList",
                       "itemListElement": items})
    return "".join('<script type="application/ld+json">%s</script>\n' % json.dumps(b)
                   for b in blocks)


def head(page):
    crumbs = ""
    if page.get("crumbs"):
        parts = ['<a href="/">Home</a>']
        for label, url in page["crumbs"]:
            parts.append(f'<span>/</span><a href="{url}">{label}</a>')
        parts.append(f'<span>/</span>{html.escape(page["nav_label"])}')
        crumbs = f'<nav class="wrap crumbs" aria-label="Breadcrumb">{"".join(parts)}</nav>'
    url = ORIGIN + page["url"]
    img_url, img_alt = share_image(page)
    title = html.escape(page["title"])
    desc = html.escape(page["description"])
    it_title = IT.get(page["title"])
    title_it = ' data-title-it="%s"' % html.escape(it_title, quote=True) if it_title else ""
    return f"""<!doctype html>
<html lang="en-CA"{title_it}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0b0908">
<meta name="robots" content="index,follow,max-image-preview:large">

<!-- Link previews and ad creatives. Every page carries its own 1200x630 card,
     so a shared link never falls back to a cropped portrait or to nothing. -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:locale" content="en_CA">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{img_url}">
<meta property="og:image:secure_url" content="{img_url}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{html.escape(img_alt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{img_url}">
<meta name="twitter:image:alt" content="{html.escape(img_alt)}">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,400&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/_assets/amami.css">
<link rel="stylesheet" href="/_assets/amami-header.css">
<link rel="stylesheet" href="/_assets/amami-footer.css">
{schema(page)}{GTM_HEAD}</head>
<body class="{page.get('body_class','')}" data-hours='{json.dumps(HOURS)}'>
{GTM_BODY}<a class="sr-only" href="#main">Skip to content</a>
{header()}
{overlay(page)}
<main id="main">
{crumbs}
"""


def lang_switch(extra=""):
    """The English / Italian dropdown. Two of these ship: one in the header's
    right-hand group for the desktop, one beside Reserve for a phone. The
    switch script drives every [data-lang-set] on the page, so more than one
    control is fine and they stay in step."""
    return """<details class="lang%s">""" % ((" " + extra) if extra else "") + """
    <summary><span data-lang-current>EN</span></summary>
    <div class="lang__menu">
      <button type="button" data-lang-set="en">English</button>
      <button type="button" data-lang-set="it">Italiano</button>
    </div>
  </details>"""


def lang_switch_panel():
    """The same choice inside the menu panel, where the phone header has no room."""
    return """<div class="lang--panel">
      <dt>Language</dt>
      <dd class="lang__row">
        <button type="button" data-lang-set="en">English</button>
        <button type="button" data-lang-set="it">Italiano</button>
      </dd>
    </div>"""


def header():
    links = "".join(f'<a href="{u}">{l}</a>' for l, u in NAV)
    return f"""<header class="hdr">
  <div class="hdr__ml">
    <a class="btn btn--line hdr__resm" href="/reservation/" data-gtm="reserve">Reserve now</a>
    {lang_switch("lang--m")}
  </div>
  <a class="hdr__logo" href="/" aria-label="{SITE['name']} home">
    <img src="{SITE['logo']}" alt="{SITE['name']}" width="120" height="34">
  </a>
  <nav class="hdr__nav" aria-label="Primary">{links}</nav>
  <div class="hdr__right">
    <span class="hours-status" data-hours-status>&nbsp;</span>
    {lang_switch()}
    {cta("reserve")}
    <button class="burger" type="button" data-nav-open aria-label="Open menu">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>"""


def overlay(page):
    rows = []
    for label, url in [("Home", "/")] + NAV:
        current = ' aria-current="page"' if url == page["url"] else ""
        rows.append('<a href="%s"%s>%s</a>' % (url, current, label))
    items = "".join(rows)
    return f"""<div class="nav-overlay" data-nav-overlay aria-hidden="true" role="dialog" aria-label="Menu">
  <button class="nav-close" type="button" data-nav-close aria-label="Close menu">&times;</button>
  <nav class="nav-overlay__menu" aria-label="Site">{items}</nav>
  <div class="nav-overlay__aside">
    {cta("reserve")}
    <dl>
      <dt>Phone</dt><dd><a href="{SITE['phone_href']}">{SITE['phone_display']}</a></dd>
      <dt>Address</dt><dd>{SITE['street']}<br>{SITE['city']}</dd>
      <dt>Today</dt><dd><span data-hours-status>&nbsp;</span></dd>
    </dl>
    {lang_switch_panel()}
  </div>
</div>"""


def hours_line():
    """The week on one line. Same source as the hours table, shortened, so the
    footer can state the hours without spending four rows on them."""
    short = {"Monday": "Mon", "Tuesday – Thursday": "Tue–Thu",
             "Friday – Saturday": "Fri–Sat", "Sunday": "Sun"}
    parts = [f"{short.get(d, d)} {t.replace(' – ', '–').replace('12pm–', '12–').lower()}"
             for d, t in HOURS_ROWS]
    return " &middot; ".join(parts)


def footer_markup():
    """The site's one footer. Brand, the facts, then legal — the list of every
    page used to sit under the logo and was removed at the client's request
    (2026-08-31) because it read as a wall of links on a phone. The pages it
    linked are still in sitemap.xml, so they stay discoverable; EXPLORE is kept
    because the sitemap is built from it.
    """
    legal = "".join(f'<a href="{u}">{l}</a>' for l, u in LEGAL)
    return f"""<footer class="ftr">
  <div class="ftr__wrap">
    <div class="ftr__top">
      <a class="ftr__brand" href="/">
        <img src="{SITE['logo']}" alt="{SITE['name']}" width="112" height="36">
        <span>{SITE['tagline']}.</span>
      </a>
      <form class="ftr__nl" action="#" method="post" aria-label="Newsletter signup"{form_attrs("newsletter")}>
        <label for="nl">Join the Amami table</label>
        <span class="ftr__nlrow">
          <input id="nl" type="email" name="email" placeholder="you@example.com" required>
          <button type="submit">Sign up</button>
        </span>
        {FORM_TAIL}
      </form>
    </div>
    <div class="ftr__meta">
      <p><span>{SITE['street']}, {SITE['city']}</span><i class="sep">&middot;</i>
        <a href="{SITE['maps']}" target="_blank" rel="noopener">Directions</a></p>
      <p>{hours_line()}</p>
      <p><a href="{SITE['phone_href']}">{SITE['phone_display']}</a><i class="sep">&middot;</i>
        <a href="mailto:{SITE['email']}">{SITE['email']}</a><i class="sep">&middot;</i>
        <a href="{SITE['instagram']}" target="_blank" rel="noopener">Instagram</a></p>
    </div>
    <div class="ftr__legal">{legal}<span>&copy; <span id="yr">2026</span> {SITE['name']}</span></div>
  </div>
</footer>"""


def mobile_bar():
    """The four quick actions pinned to the bottom on phones (spec 5.2).
    Part of the site's chrome, so the static pages get it too."""
    return f"""<nav class="mobile-bar" aria-label="Quick actions">
  <a href="/reservation/">Reserve</a>
  <a href="/menu/">Menu</a>
  <a href="{SITE['phone_href']}">Call</a>
  <a href="{SITE['maps']}" target="_blank" rel="noopener">Directions</a>
</nav>"""


def footer():
    return f"""</main>
{footer_markup()}
{mobile_bar()}
<script>document.getElementById('yr').textContent=new Date().getFullYear()</script>
<script src="/_assets/amami.js" defer></script>
<script src="/_assets/amami-i18n.js"></script>
</body>
</html>
"""


# ===========================================================================
#  Templates — eleven, per spec 1.2
# ===========================================================================

def ot_widget():
    """OpenTable's compact booking card. The full flow lives on /reservation/;
    this is the "find a table" card the reference puts on the home page."""
    return (
        '<div class="homebook__card">\n'
        '<script type="text/javascript" src="https://www.opentable.ca/widget/reservation/loader'
        '?rid=1470808&amp;type=standard&amp;theme=standard&amp;color=1&amp;dark=false'
        '&amp;iframe=true&amp;domain=ca&amp;lang=en-CA&amp;newtab=false'
        '&amp;ot_source=Restaurant%20website&amp;cfe=true"></script>\n'
        '<noscript><a class="btn btn--solid" href="/reservation/">Reserve a Table</a></noscript>\n'
        '</div>')


def t_home(p):
    """Home as the reference builds it: a stack of full-bleed panels, each one
    photograph, one word, one action, then the booking block. Structure
    unchanged; the client's copy (2026-09-03) fills the panel lines, which were
    empty, and the booking block."""
    panels = [
        panel("Dinner looks better in red.",
              "Pasta. Vino. Late nights. That’s the plan.",
              "", "", video="hero_loop", first=True, over="Amami Italia",
              actions=[("/reservation/", "Book a Table"), ("/menu/", "See the Menu")]),
        panel("Dinner", "No shortcuts. Just sauce.", "/menu/dining/",
              "Take a Look at the Menu", slot="pasta_finish"),
        panel("Pizza", "", "/menu/pizza/", "View Menus", slot="pizza"),
        panel("After Dark", "Eat slow. Stay late.", "/after-dark/", "The Lounge",
              slot="cocktail_smoke"),
        panel("The Room", "Come for dinner. Lose track of time.", "/our-story/",
              "Our Story", slot="room_wide"),
        panel("Private Dining", "You invite them. We feed them.", "/events/", "Enquire",
              slot="room_private"),
        panel("Catering", "A little Italy. A lot of amore.", "/catering/", "Enquire",
              slot="table_setting"),
    ]
    tail = """<section class="homebook" id="book">
  <div class="wrap">
    <h2 class="homebook__h">Your table is waiting.</h2>
    <p class="homebook__lede">Bring a date. Bring the group chat. Bring the person who
       always steals fries.</p>
    <p class="homebook__lede">Just don’t skip the tiramisu.</p>
    %s
    <p class="homebook__note">Eight or more is best arranged by phone &mdash;
      <a href="%s">%s</a>.</p>
  </div>
</section>""" % (ot_widget(), SITE["phone_href"], SITE["phone_display"])
    return "\n".join(panels) + "\n" + tail


def t_menu_hub(p):
    """Menu hub. The reference's editorial band and serif tab row up top, then
    the two menus we actually publish as full photographic doors, then the rest
    as a quiet index that says plainly which lists are still coming.

    Dish counts are read out of menu_data, so the page can never claim more
    than is published.
    """
    tabs = [("Dining", "/menu/dining/"), ("Pizza", "/menu/pizza/"),
            ("After Dark", "/menu/after-dark/"), ("Wine", "/menu/wine/"),
            ("Cocktails", "/menu/cocktails/"), ("Tasting", "/menu/tasting/"),
            ("Catering", "/menu/catering/")]
    row = "".join('<a class="tabrow__tab" href="%s">%s</a>' % (u, l) for l, u in tabs)

    def count(url):
        return sum(len(course[2]) for course in MENUS.get(url, []))

    # The two published menus, as doors you can see into.
    doors = [
        ("/menu/dining/", "Pranzo e Cena", "Dining", "pasta_finish",
         "Thirty-two dishes. The steaks are aged 45 days, sold by the kilo.",
         "%d dishes &middot; 12pm until close" % count("/menu/dining/")),
        ("/menu/after-dark/", "Dopo Cena", "After Dark", "cocktail_smoke",
         "Port, amari, grappa. Coffee with something in it.",
         "%d pours &middot; port, amaro, grappa, caff&egrave;" % count("/menu/after-dark/")),
    ]
    doorhtml = "".join("""<a class="mdoor" href="%s">
    <span class="mdoor__media">%s</span>
    <span class="mdoor__en">%s</span>
    <span class="mdoor__it">%s</span>
    <span class="mdoor__desc">%s</span>
    <span class="mdoor__fact">%s</span>
    <span class="mdoor__go">Read the menu</span>
  </a>""" % (url, img(slot, "tile"), en, it, desc, fact)
                       for url, it, en, slot, desc, fact in doors)

    # The five that are not printed yet. Named, linked, and honest about it.
    rest = [
        ("/menu/pizza/", "Dal Forno", "Pizza", "Out of the oven."),
        ("/menu/wine/", "La Cantina", "Wine", "Tuscany first."),
        ("/menu/cocktails/", "Aperitivi &amp; Cocktails", "Cocktails", "Aperitivo, and after."),
        ("/menu/tasting/", "Degustazione", "Tasting", "Isabella’s run. Needs notice."),
        ("/menu/catering/", "Fuori Casa", "Catering", "Out the door."),
    ]
    resthtml = "".join("""<a class="mindex__item" href="%s">
    <span class="mindex__en">%s</span>
    <span class="mindex__it">%s</span>
    <p class="mindex__desc">%s</p>
    <span class="mindex__soon">List to come</span>
  </a>""" % (url, en, it, desc) for url, it, en, desc in rest)

    tiles = "".join('<a class="tile" href="/after-dark/">%s</a>' % img(s, "tile")
                    for s in GALLERY[:10])

    src, alt = MEDIA["hero_loop"]
    video = ('<video class="menuband__video" autoplay muted loop playsinline '
             'preload="metadata" aria-label="%s"><source src="%s" type="video/mp4"></video>'
             % (html.escape(alt), src))

    return """<section class="menuband">
  %s
  <div class="wrap">
    <p class="eyebrow menuband__eyebrow">The Menu</p>
    <h1 class="menuband__title menuband__title--line">Order like you mean it.</h1>
    <p class="menuband__lede">Start with something to share. End with something sweet.
       Somewhere in the middle, have the pasta.</p>
    <div class="menuband__row"><div class="tabrow">%s</div></div>
  </div>
</section>
<section class="mdoors-sec">
  <div class="mdoors">%s</div>
</section>
<section class="wrap">
  <div class="section-head">
    <p class="eyebrow">Also on the menu</p>
    <h2 class="display" style="font-size:clamp(1.6rem,3vw,2.2rem)">The other five lists</h2>
    <p class="lede">Not up yet. Call and ask.</p>
  </div>
  <div class="mindex">%s</div>
</section>
<section class="tilegrid">%s</section>
<section class="wrap" style="text-align:center">
  <h2 class="display" style="font-size:clamp(1.6rem,3vw,2.2rem)">Go on. Order another plate.</h2>
  <p class="lede" style="margin-inline:auto">Nobody remembers the night they played it safe.</p>
  %s
</section>""" % (video, row, doorhtml, resthtml, tiles, cta("reserve"))


# The client's category lines (2026-09-03). The Italian course name stays as
# the heading — it is what the printed menu says — and their line sits under it,
# with the course's own functional note kept where it carries a fact.
COURSE_LINES = {
    "Antipasti": ("Start here", "A little something before the main event."),
    "Primi Piatti": ("The pasta", "Twirl first. Talk later."),
    "Secondi": ("The main thing",
                "Big flavours. Clean plates. All served with grilled seasonal "
                "vegetables and fingerling potatoes."),
    "Dolci": ("Sweet talk", "You were always going to order dessert."),
}


def t_menu_page(p):
    """A single menu. Anchor nav + real dish list + the page's booking route.

    Dishes come from tools/menu_data.py, transcribed from the current printed
    menu. Every price and description is live HTML text — never a PDF, never an
    image of a menu — so it is readable, searchable and indexable (spec
    principle 4, "publish every fact").
    """
    courses = MENUS.get(p["url"])
    if courses:
        sections = [c[0] for c in courses]
    else:
        sections = p.get("courses", ["Antipasti", "Primi", "Secondi", "Contorni", "Dolci"])

    anchors = "".join('<a class="btn" href="#%s">%s</a>' % (slug(s), s) for s in sections)
    blocks = []

    if courses:
        for course in courses:
            name, note, items = course[0], course[1], course[2]
            foot = course[3] if len(course) > 3 else ""
            rows = []
            for dn, desc, price, tags, add in items:
                marks = "".join(
                    '<abbr class="dish__tag" title="%s">%s</abbr>'
                    % ({"v": "Vegetarian", "gf": "Gluten free"}[t], t.upper())
                    for t in tags)
                rows.append(
                    '<div class="dish">'
                    '<div><span class="dish__name">%s</span>%s</div>'
                    '<span class="dish__price">%s</span>'
                    '%s%s</div>'
                    % (dn, marks,
                       price if price.endswith("/kg") else "$" + price,
                       '<p class="dish__desc">%s</p>' % desc if desc else "",
                       '<p class="dish__add">%s</p>' % add if add else ""))
            eyebrow, line = COURSE_LINES.get(name, ("", ""))
            if line:
                note = line
            blocks.append(
                '<section class="wrap" id="%s">\n'
                '  <div class="section-head">%s'
                '<h2 class="display" style="font-size:clamp(1.7rem,3.4vw,2.6rem)">%s</h2>%s</div>\n'
                '  <div class="menu-list">%s</div>%s\n'
                '</section>'
                % (slug(name),
                   '<p class="eyebrow">%s</p>' % eyebrow if eyebrow else "",
                   name,
                   '<p class="lede">%s</p>' % note if note else "",
                   "".join(rows),
                   '<p class="menu-foot">%s</p>' % foot if foot else ""))
        notes = ('<section class="wrap"><ul class="menu-notes">%s</ul></section>'
                 % "".join("<li>%s</li>" % n for n in LEGEND_NOTES))
    else:
        for sec in sections:
            blocks.append(
                '<section class="wrap" id="%s">\n'
                '  <div class="section-head">'
                '<h2 class="display" style="font-size:clamp(1.7rem,3.4vw,2.6rem)">%s</h2></div>\n'
                '  %s\n</section>'
                % (slug(sec), sec,
                   ph("%s list" % sec,
                      "This list isn’t up yet. Call %s and we’ll read it to you."
                      % SITE["phone_display"],
                      "text")))
        notes = ('<section class="wrap"><ul class="menu-notes">%s</ul></section>'
                 % "".join("<li>%s</li>" % n for n in LEGEND_NOTES))

    return """<section class="wrap page-top">
  <div class="section-head" style="text-align:center">
    <p class="eyebrow">%s</p>
    <h1 class="display">%s</h1>
    <p class="lede" style="margin-inline:auto">%s</p>
  </div>
  <div class="grid" data-anchor-nav style="grid-auto-flow:column;grid-auto-columns:max-content;
       overflow-x:auto;justify-content:center;padding-bottom:.5rem">%s</div>
</section>
%s
%s
<section class="wrap" style="text-align:center">
  %s
  <p class="eyebrow" style="margin-top:1.2rem">Hungry yet?</p>
</section>""" % (p["nav_label"], p["display"], p["meaning"], anchors,
                 "".join(blocks), notes, cta(p["action"]))


def t_story(p):
    """Our Story. The client's About copy sits at the top and closes the page;
    the three blocks in the middle tell the restaurant's story (the town
    framing was dropped at the client's request, 2026-09-22)."""
    blocks = [("Toscana", "Where it came from",
               "A Tuscan town with the wall still round it. Bread, beans, good oil.",
               "room_booth_one"),
              ("Il Mestiere", "How it gets made",
               "Pasta rolled in the morning. Sauce on before we open.", "pasta_truffle"),
              ("A Brampton", "The room",
               "Two on a Tuesday. Twenty on a Saturday. It gets loud.", "room_wide")]
    out = []
    for i, (it, en, copy, slot) in enumerate(blocks):
        flip = " storyblock--flip" if i % 2 else ""
        out.append("""<section class="storyblock%s">
  <div class="storyblock__media">%s</div>
  <div class="storyblock__text">
    <p class="eyebrow">%s</p>
    <h2 class="storyblock__h">%s</h2>
    <p>%s</p>
  </div>
</section>""" % (flip, img(slot, "tile"), it, en, copy))

    return """<section class="pagehead">
  <div class="pagehead__media">%s</div>
  <div class="wrap">
    <p class="eyebrow pagehead__k">Tuscan at heart. Brampton at home.</p>
    <h1 class="pagehead__title pagehead__title--line">Italian food. Italian energy.</h1>
    <p class="pagehead__lede">No rules—except never leave without dessert.</p>
    <div class="pagehead__copy">
      <p>Long dinners, loud tables, first dates, family birthdays, and “let’s just get
         one drink” that turns into a full evening.</p>
    </div>
  </div>
</section>
%s
<section class="wrap" style="text-align:center">
  <h2 class="display" style="font-size:clamp(1.7rem,3.4vw,2.4rem)">A table worth staying at.</h2>
  <p class="lede" style="margin-inline:auto">Eat slowly. Pour generously. Make room for one more.</p>
  %s
</section>""" % (
        img("room_wide", "hero", loading="eager"), "".join(out), cta("reserve"))


def t_chef(p):
    """Chef Isabella Comello. Written to the client's copy (2026-09-03).

    Nothing biographical is asserted here that has not been supplied: the page
    is built out of what she does and one line in her own words, not a CV. The
    three signature dishes are the ones that are actually on the printed 2026
    menu — the tordelli and the wild boar ragù that stood here before were on
    neither the menu nor menu_data.py.
    """
    dishes = [
        ("Bistecca alla Fiorentina", "Forty-five days, by the kilo."),
        ("Gnocchi al Pesto", "Pesto, pine nuts, stracciatella."),
        ("Agnello alla Griglia", "Rosemary, lemon, off the grill."),
    ]
    cards = "".join('<div class="card"><h3>%s</h3><p style="margin:0">%s</p></div>' % d
                    for d in dishes)
    return f"""<section class="hero">
  <div class="hero__media">{hero_media(p, 1)}</div>
  <div><p class="eyebrow">Chef Isabella</p>
  <h1 class="display">Meet Chef Isabella. She takes pasta personally.</h1>
  <p class="lede" style="margin-inline:auto">The sauce has a boss.</p></div>
</section>
<section class="wrap"><div class="split">
  <div>{ph("Chef Isabella", "Candid, vertical. To shoot.", "tall", 1)}</div>
  <div>
    <h2 class="display" style="font-size:clamp(1.8rem,3.6vw,2.6rem)">From Chef Isabella’s kitchen</h2>
    <p class="lede">Chef Isabella is the heart of the Amami kitchen.</p>
    <p>No fuss. No shortcuts. Just Italian food done properly.</p>
    <blockquote class="pullq"><p>“If you’re not using bread to finish the sauce,
       we’re not done yet.”</p><cite>Chef Isabella</cite></blockquote>
  </div>
</div></section>
<section class="wrap">
  <div class="section-head">
    <h2 class="display" style="font-size:clamp(1.7rem,3.4vw,2.4rem)">She doesn’t rush the sauce. Neither should you.</h2>
  </div>
  <div class="grid grid--3">{cards}</div>
  <div style="text-align:center;margin-top:2.4rem">{cta("reserve")}</div>
</section>"""


def t_experience(p):
    """After Dark / Events / Catering — one template, three configurations."""
    spaces = p.get("spaces", [])
    blocks = []
    # Two layouts. "split" is the original: two photographs beside a text
    # column. "mosaic" is the reference block. Events keeps split, which is how
    # it was before the reference pass.
    pools = [["room_private", "table_setting", "room_booths"],
             ["room_lounge", "cocktail_smoke", "room_evening"],
             ["room_wide", "wine_pour", "room_bar"]]
    layout = p.get("layout", "mosaic")
    for i, (name, desc, cap) in enumerate(spaces):
        slots = pools[i % len(pools)]
        if layout == "split":
            blocks.append("""<section class="wrap"><div class="split">
  <div class="grid" style="gap:14px">%s
    %s</div>
  <div>
    <h2 class="display" style="font-size:clamp(1.6rem,3.2vw,2.3rem);text-transform:uppercase;letter-spacing:.04em">%s</h2>
    <p class="lede">%s</p>
    <p class="eyebrow">Capacity &middot; %s</p>
    %s
  </div>
</div></section>""" % (img(slots[0], "wide"), img(slots[1], "wide"),
                       name, desc, cap, cta(p["action"])))
        else:
            tiles = "".join('<div class="mosaic__tile">%s</div>' % img(sl, "tile") for sl in slots)
            blocks.append("""<section class="mosaic">
  <div class="mosaic__grid">%s</div>
  <div class="mosaic__text">
    <h2 class="mosaic__name">%s</h2>
    <p>%s</p>
    <p class="mosaic__fact"><strong>Capacity |</strong> %s</p>
    %s
  </div>
</section>""" % (tiles, name, desc, cap, cta(p["action"])))
    form = ""
    if p["action"] in ("event", "catering"):
        which = "Event" if p["action"] == "event" else "Catering"
        form = f"""<section class="wrap" id="enquiry">
  <div class="section-head" style="text-align:center">
    <h2 class="display" style="font-size:clamp(1.7rem,3.4vw,2.4rem)">{which} enquiry</h2>
    <p class="lede" style="margin-inline:auto">Tell us what you are planning and we will come back to you with dates, space and a per-head price.</p>
  </div>
  <form class="grid grid--2" style="max-width:820px;margin-inline:auto" action="#" method="post"{form_attrs(p["action"])}>
    <div class="field"><label for="fn">First name</label><input id="fn" name="firstName" required></div>
    <div class="field"><label for="ln">Last name</label><input id="ln" name="lastName" required></div>
    <div class="field"><label for="em">Email</label><input id="em" type="email" name="email" required></div>
    <div class="field"><label for="tel">Phone</label><input id="tel" type="tel" name="phone"></div>
    <div class="field"><label for="dt">Date</label><input id="dt" type="date" name="date"></div>
    <div class="field"><label for="pax">Guests</label><input id="pax" type="number" min="1" name="guests"></div>
    <div class="field" style="grid-column:1/-1"><label for="msg">What are you planning?</label>
      <textarea id="msg" name="message" rows="4"></textarea></div>
    <div style="grid-column:1/-1"><button class="btn btn--solid" type="submit">Send enquiry</button>
      <p class="eyebrow" style="margin-top:.8rem">We answer within a business day.</p></div>
    {FORM_TAIL}
  </form>
</section>"""
    book = ""
    return f"""<section class="hero">
  <div class="hero__media">{hero_media(p)}</div>
  <div><p class="eyebrow">{p["nav_label"]}</p><h1 class="display">{p["display"]}</h1>
  <p class="lede" style="margin-inline:auto">{p["meaning"]}</p>
  <div class="hero__actions">{cta(p["action"])}</div></div>
</section>
{"".join(blocks)}
{book}{form}
"""


def t_after_dark(p):
    """After Dark, built on the nightlife reference the client sent: an
    oversized wordmark laid over the photograph, a bronze panel carrying type
    with a picture cutting across it, and one dark card of small copy. The
    facts are the ones the site already publishes — the after-dinner list and
    the two rooms' capacities — so nothing is invented to fill the layout.
    """
    room_tpl = ('<article class="adroom">\n'
                '    <div class="adroom__media">%s</div>\n'
                '    <h3 class="adroom__name">%s</h3>\n'
                '    <p class="adroom__copy">%s</p>\n'
                '    <p class="adroom__cap">%s</p>\n'
                '  </article>')
    rooms = "".join(room_tpl % (img(slot, "tile"), name, desc, cap)
                    for (name, desc, cap), slot
                    in zip(p.get("spaces", []), ["room_lounge", "room_bar"]))

    return """<section class="adhero">
  <div class="adhero__media">%s</div>
  <div class="adhero__in">
    <p class="eyebrow adhero__k">After Dark</p>
    <h1 class="adhero__mark">Raise the<span>Bar</span></h1>
    <p class="admark"><b>From 10pm</b><i>&#9733;</i>The lounge<i>&#9733;</i>Port, amaro, grappa<i>&#9733;</i>Music</p>
    <div class="adhero__act">%s<a class="btn adbtn--line" href="/menu/after-dark/">See the list</a></div>
  </div>
</section>
<section class="adcollage">
  <div class="adpanel">
    <p class="adpanel__type">The room<br>doesn&rsquo;t empty<br>at ten</p>
    <div class="adpanel__inset">%s</div>
  </div>
  <div class="adcard">
    <div class="adcard__media">%s</div>
    <div class="adcard__body">
      <p class="adcard__k">After dinner, at Amami</p>
      <p>Dinner finishes and nobody asks you to leave.</p>
      <p>Forty-three things to drink. Twelve seats at the counter.</p>
      <a class="adcard__go" href="/menu/after-dark/">Read the after-dark list</a>
    </div>
  </div>
</section>
<section class="adrooms">%s</section>
<section class="adend">
  <div class="adend__media">%s</div>
  <div class="adend__in">
    <p class="adend__word">After<span>Dark</span></p>
    <p class="adend__copy">Taking the room for the night? Send us the date.</p>
    <div class="adend__act">%s<a class="btn adbtn--line" href="/events/">Ask about a private night</a></div>
  </div>
</section>""" % (img("cocktail_smoke", "hero", loading="eager"), cta("lounge"),
                 img("room_evening", "tile"), img("server_wine", "tile"),
                 rooms, img("room_lounge", "tile"), cta("lounge"))


CAP_SEATED = ('<svg viewBox="0 0 24 24" aria-hidden="true" class="gbcap__i">'
              '<path d="M7 11V5.5A2.5 2.5 0 0 1 9.5 3h5A2.5 2.5 0 0 1 17 5.5V11'
              'M5 11h14v3.6H5zM7.2 14.6V21M16.8 14.6V21" fill="none" stroke="currentColor" '
              'stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>')
CAP_STANDING = ('<svg viewBox="0 0 24 24" aria-hidden="true" class="gbcap__i">'
                '<circle cx="8" cy="5.4" r="2.4" fill="none" stroke="currentColor" stroke-width="1.4"/>'
                '<circle cx="16.5" cy="6.4" r="2" fill="none" stroke="currentColor" stroke-width="1.4"/>'
                '<path d="M3.6 20v-6a4.4 4.4 0 0 1 8.8 0v6M14 20v-5a3.6 3.6 0 0 1 6.6-2" '
                'fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>')


def t_events(p):
    """Group Booking & Private Events, built to the client's second reference.

    Everything sits on the brand ground: the title, the two actions, a short
    paragraph, two photographs, a capacity row read straight off what the site
    already publishes, then the practical block — hours, dress code, address
    and contact. No number here is invented; a room whose seated or standing
    figure has never been published simply does not show that figure.
    """
    caps = [("Full Buyout", [("120", "standing")]),
            ("The Private Room", [("16–22", "seated")]),
            ("The Long Table", [("24–30", "seated")]),
            ("The Lounge", [("30", "seated"), ("60", "standing")])]
    cols = []
    for name, figures in caps:
        nums = "".join(
            '<span class="gbcap__fig"><span class="gbcap__n">%s</span>%s'
            '<span class="gbcap__l">%s</span></span>'
            % (n, CAP_SEATED if kind == "seated" else CAP_STANDING, kind.title())
            for n, kind in figures)
        cols.append('<div class="gbcap__col"><p class="gbcap__name">%s</p>'
                    '<div class="gbcap__nums">%s</div></div>' % (name, nums))

    vsrc, valt = MEDIA["hero_loop"]
    form = ("""<section class="gbform" id="enquiry">
  <video class="gbform__bg" autoplay muted loop playsinline preload="metadata"
         aria-label="%s"><source src="%s" type="video/mp4"></video>
  <div class="wrap gbform__in">""" % (html.escape(valt), vsrc)) + """
  <div class="section-head" style="text-align:center">
    <p class="eyebrow">You invite them. We feed them.</p>
    <h2 class="display" style="font-size:clamp(1.7rem,3.4vw,2.4rem)">Tell us what you’re planning</h2>
    <p class="lede" style="margin-inline:auto">Date, how many, which room.</p>
  </div>
  <form class="grid grid--2" style="max-width:820px;margin-inline:auto" action="#" method="post" """ + form_attrs("event") + """>
    <div class="field"><label for="fn">First name</label><input id="fn" name="firstName" required></div>
    <div class="field"><label for="ln">Last name</label><input id="ln" name="lastName" required></div>
    <div class="field"><label for="em">Email</label><input id="em" type="email" name="email" required></div>
    <div class="field"><label for="tel">Phone</label><input id="tel" type="tel" name="phone"></div>
    <div class="field"><label for="dt">Date</label><input id="dt" type="date" name="date"></div>
    <div class="field"><label for="pax">Guests</label><input id="pax" type="number" min="1" name="guests"></div>
    <div class="field" style="grid-column:1/-1"><label for="msg">What are you planning?</label>
      <textarea id="msg" name="message" rows="4"></textarea></div>
    <div style="grid-column:1/-1"><button class="btn btn--solid" type="submit">Plan Your Party</button>
      <p class="eyebrow" style="margin-top:.8rem">We answer within a business day.</p></div>
    """ + FORM_TAIL + """
  </form>
  </div>
</section>"""

    return """<section class="gb">
  <div class="wrap">
    <h1 class="gb__title">Make a night of it.</h1>
    <p class="gb__sub">Birthdays. Engagements. Work wins.<br>Or just a very serious excuse
       to eat pasta with your favourite people.</p>
    <div class="gb__act">
      <a class="btn btn--line" href="#enquiry">Plan Your Party</a>
      <a class="btn btn--line" href="/menu/">See the Menus</a>
    </div>
    <p class="gb__copy">Celebrations are best served family-style.</p>
    <p class="gb__copy">Bring the guest list. Bring the good outfit. Bring a reason to toast.</p>
    <p class="gb__copy"><a href="mailto:%s">%s</a> &middot; <a href="%s">%s</a></p>
  </div>
</section>
<section class="gbshots">
  <figure>%s</figure>
  <figure>%s</figure>
</section>
<section class="gbcap">
  <div class="wrap">
    <p class="gbcap__rule"><span>Capacity</span></p>
    <div class="gbcap__row">%s</div>
  </div>
</section>
<section class="gbinfo">
  <div class="wrap">
    <h2 class="gbinfo__h">Dress Code</h2>
    <p class="gbinfo__p">Semi formal for evening service. Collared shirts, dress trousers
       or an elegant dress.</p>
  </div>
</section>
%s""" % (SITE["email"], SITE["email"], SITE["phone_href"], SITE["phone_display"],
         img("room_private", "tile"), img("room_wide", "tile"),
         "".join(cols), form)


def contact_band():
    """The location block that sits directly above the footer, as in the
    reference: a full-bleed room photograph, a cream location card, then the
    three contact columns. It belongs on the two pages a guest lands on when
    they are ready to come in. The reservation page is the restored 2026-08-20
    one and carries its own layout, so on this build that leaves
    /visit/contact/ — and nowhere else, so it never reads as a second footer.
    """
    src, alt = MEDIA["room_evening"]
    return """<section class="cband" id="contact-band">
  <img class="cband__bg" src="%s" alt="%s" loading="lazy" decoding="async" sizes="100vw">
  <div class="cband__inner">
    <a class="cband__map" href="%s" target="_blank" rel="noopener">
      <svg class="cband__mark" viewBox="0 0 24 32" aria-hidden="true" focusable="false">
        <path d="M12 1c-5 0-9 4-9 9 0 6.6 9 21 9 21s9-14.4 9-21c0-5-4-9-9-9z"
              fill="none" stroke="currentColor" stroke-width="1.3"/>
        <circle cx="12" cy="10" r="3.1" fill="currentColor"/>
      </svg>
      <span class="cband__pin">%s</span>
      <span class="cband__addr">%s<br>%s</span>
      <span class="cband__maplabel">Open in Google Maps</span>
    </a>
    <h2 class="cband__title">Contact</h2>
    <div class="cband__cols">
      <div><a href="/">amamiitalia.com</a><br><a href="%s" target="_blank" rel="noopener">@amamiitalia_official</a></div>
      <div><a href="mailto:%s">%s</a><br><a href="%s">%s</a></div>
      <div>%s<br>%s</div>
    </div>
  </div>
</section>""" % (src, html.escape(alt), SITE["maps"], SITE["name"],
                 SITE["street"], SITE["city"], SITE["instagram"],
                 SITE["email"], SITE["email"], SITE["phone_href"], SITE["phone_display"],
                 SITE["street"], SITE["city"])


def t_visit(p):
    rows = "".join(f"<tr><th scope='row' style='text-align:left;padding:.5rem 1.4rem .5rem 0;font-weight:400'>{d}</th>"
                   f"<td style='padding:.5rem 0'>{t}</td></tr>" for d, t in HOURS_ROWS)
    return f"""<section class="wrap page-top">
  <div class="section-head" style="text-align:center">
    <p class="eyebrow">Visit</p><h1 class="display">Vieni a Trovarci</h1>
    <p class="lede" style="margin-inline:auto">Come and find us. Mayfield Road, top end of Brampton.</p>
  </div>
  <div class="split">
    <div>{img("room_evening", "tile")}</div>
    <div>
      <h2 class="display" style="font-size:clamp(1.6rem,3vw,2.1rem)">Hours</h2>
      <table style="border-collapse:collapse;margin-bottom:1.6rem">{rows}</table>
      <p class="eyebrow" data-hours-status>&nbsp;</p>
      <h2 class="display" style="font-size:clamp(1.6rem,3vw,2.1rem);margin-top:1.4rem">Address</h2>
      <p class="lede">{SITE['street']}<br>{SITE['city']}</p>
      <div class="hero__actions">{cta("directions")}
        <a class="btn" href="{SITE['phone_href']}">Call {SITE['phone_display']}</a></div>
    </div>
  </div>
</section>
<section class="wrap">
  <div class="grid grid--3">
    <div class="card"><h3>Parking</h3><p style="margin:0">Free, right outside the door.</p></div>
    <div class="card"><h3>Getting in</h3><p style="margin:0">Step-free entry and an accessible washroom.</p></div>
    <div class="card"><h3>Getting here</h3><p style="margin:0">Mayfield, top of Brampton.
      Caledon, Bolton and Vaughan are a short drive.</p></div>
  </div>
</section>
"""


def t_faq(p):
    qs = [("Do you take reservations?", "Yes. Online or by phone."),
          ("Is there parking?", "Free, right outside."),
          ("Can you handle allergies?",
           "Yes. Tell us when you book, and again at the table."),
          ("Do you have a tasting menu?", "The degustazione. It needs notice."),
          ("Is the lounge age-restricted?", "Call and ask — %s." % SITE["phone_display"]),
          ("Can we book the whole room?", "Yes. A hundred and twenty if you take the lot.")]
    items = "".join(f"""<details class="card" style="margin-bottom:14px">
  <summary style="cursor:pointer;font-family:var(--serif);font-size:1.25rem">{q}</summary>
  <p style="margin:.8rem 0 0">{a}</p></details>""" for q, a in qs)
    return f"""<section class="wrap page-top">
  <div class="section-head" style="text-align:center"><p class="eyebrow">FAQ</p>
    <h1 class="display">Buono a Sapersi</h1>
    <p class="lede" style="margin-inline:auto">Things people ask us.</p></div>
  {items}
  <div style="text-align:center;margin-top:2rem">{cta("reserve")}</div>
</section>"""


def t_contact(p):
    return f"""<section class="wrap page-top">
  <div class="section-head" style="text-align:center"><p class="eyebrow">Contact</p>
    <h1 class="display">Ciao, bella.</h1>
    <p class="lede" style="margin-inline:auto">Find us. Call us. Come hungry.</p>
    <p class="lede" style="margin-inline:auto">Got a question? Planning something special?
      Need to know if there is room for one more?</p>
    <p class="lede" style="margin-inline:auto">Send us a note.</p></div>
  <form class="grid grid--2" style="max-width:820px;margin-inline:auto" action="#" method="post"{form_attrs("contact")}>
    <div class="field" style="grid-column:1/-1"><label for="topic">What is it about?</label>
      <select id="topic" name="topic">
        <option>General</option><option>Reservation</option><option>Private dining or events</option>
        <option>Catering</option><option>Press</option><option>Careers</option>
      </select></div>
    <div class="field"><label for="cn">Name</label><input id="cn" name="name" required></div>
    <div class="field"><label for="ce">Email</label><input id="ce" type="email" name="email" required></div>
    <div class="field" style="grid-column:1/-1"><label for="cm">Message</label>
      <textarea id="cm" name="message" rows="5"></textarea></div>
    <div style="grid-column:1/-1"><button class="btn btn--solid" type="submit">Send</button></div>
    {FORM_TAIL}
  </form>
</section>
{contact_band()}"""


def t_lounge(p):  # archived — not in PAGES, kept so the page can come back
    """The Lounge — the bar as its own room, then the photographs that used to
    sit on the gallery page. Booking routes to After Dark, which is the
    late-night programme in the same space."""
    tiles = "".join('<figure class="tile">%s</figure>' % img(k, "tile")
                    for k in ["room_lounge", "cocktail_smoke", "room_bar", "wine_pour",
                              "wine_table", "server_wine", "room_evening", "table_setting",
                              "room_booth_one", "room_wide"])
    return """<section class="hero">
  <div class="hero__media">%s</div>
  <div><p class="eyebrow">Lounge</p><h1 class="display">Il Salotto</h1>
  <p class="lede" style="margin-inline:auto">The sitting room. A seat at the counter, an aperitivo
     before dinner, and somewhere to stay after it.</p>
  <div class="hero__actions">%s</div></div>
</section>
<section class="storyblock">
  <div class="storyblock__media">%s</div>
  <div class="storyblock__text">
    <p class="eyebrow">Il Banco</p>
    <h2 class="storyblock__h">The bar</h2>
    <p>Twelve seats at the counter. Negroni, spritz, an amaro list that runs long, and the
       short plate list from the kitchen while it is open.</p>
  </div>
</section>
<section class="storyblock storyblock--flip">
  <div class="storyblock__media">%s</div>
  <div class="storyblock__text">
    <p class="eyebrow">Aperitivo</p>
    <h2 class="storyblock__h">Before dinner</h2>
    <p>Come early, sit at the bar, order one thing and decide the rest later. No reservation
       needed for the counter.</p>
  </div>
</section>
<section class="tilegrid">%s</section>
<section class="wrap" style="text-align:center">
  <p class="lede" style="margin-inline:auto">Late nights in the same room are
     <a href="/after-dark/">Amami After Dark</a>.</p>
  %s
</section>""" % (img("room_lounge", "hero", loading="eager"), cta("lounge"),
                 img("room_bar", "tile"), img("cocktail_smoke", "tile"),
                 tiles, cta("reserve"))


def t_journal_index(p):
    posts = [("From Italy to Brampton", "/from-italy-to-brampton-amami-italia/"),
             ("Romantic dining in Brampton", "/romantic-dining-in-brampton/"),
             ("What makes a luxury Italian restaurant different", "/what-makes-a-luxury-italian-restaurant-in-brampton-different/"),
             ("Why Italian food works for corporate events", "/why-italian-food-works-for-corporate-events/")]
    cards = "".join(f'<a class="card" href="{u}" style="text-decoration:none"><h3>{t}</h3>'
                    f'<p class="eyebrow" style="margin:.6rem 0 0">Read</p></a>' for t, u in posts)
    return f"""<section class="wrap page-top">
  <div class="section-head" style="text-align:center"><p class="eyebrow">Journal</p>
    <h1 class="display">Il Quaderno</h1>
    <p class="lede" style="margin-inline:auto">The notebook.</p></div>
  <div class="grid grid--2">{cards}</div>
</section>"""


def t_landing(p):
    cards = "".join('<div class="card"><h3>%s</h3><p style="margin:0">%s</p></div>' % c
                    for c in p.get("cards", []))
    return f"""<section class="hero">
  <div class="hero__media">{ph(p["nav_label"] + " hero", "Full-bleed landscape.", "hero", 3)}</div>
  <div><p class="eyebrow">{p["nav_label"]}</p><h1 class="display">{p["display"]}</h1>
  <p class="lede" style="margin-inline:auto">{p["meaning"]}</p>
  <div class="hero__actions">{cta(p["action"])}</div></div>
</section>
<section class="wrap">
  <div class="split">
    <div>{ph("Supporting image", "Landscape.", "wide", 3)}</div>
    <div><h2 class="display" style="font-size:clamp(1.7rem,3.4vw,2.4rem)">{p["h2"]}</h2>
      <p class="lede">{p["body"]}</p></div>
  </div>
</section>
<section class="wrap">
  <div class="grid grid--3">{cards}</div>
  <div style="text-align:center;margin-top:2.4rem">{cta(p["action"])}</div>
</section>
"""


def t_utility(p):
    return f"""<section class="wrap page-top">
  <div class="section-head"><p class="eyebrow">{p["nav_label"]}</p><h1 class="display">{p["display"]}</h1></div>
  <div style="max-width:var(--measure)">
    <p class="lede">{p["meaning"]}</p>
    <p>Still being written. If you need an answer now, call
       <a href="{SITE['phone_href']}">{SITE['phone_display']}</a> or write to
       <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p>
  </div>
</section>"""


def t_simple(p):
    """Gift cards, careers, press — a heading, a purpose, one action."""
    extra = ""
    if p["url"] == "/gift-cards/":
        extra = f'<div class="card" id="buy" style="max-width:640px;margin:2rem auto 0">{ph("Gift card purchase widget", "Provider not yet chosen.", "wide")}</div>'
    if p["url"] == "/careers/":
        extra = """<section id="apply" class="grid grid--2" style="max-width:820px;margin:2rem auto 0">
  <div class="field"><label for="an">Name</label><input id="an" name="name"></div>
  <div class="field"><label for="ae">Email</label><input id="ae" type="email" name="email"></div>
  <div class="field" style="grid-column:1/-1"><label for="ar">Role</label><input id="ar" name="role"></div>
  <div class="field" style="grid-column:1/-1"><label for="am">Message</label><textarea id="am" rows="4"></textarea></div>
</section>"""
    if p["url"] == "/press/":
        extra = f"""<div class="grid grid--3" style="margin-top:2rem">
  <div class="card"><h3>Coverage</h3><p style="margin:0">Logos and links to add.</p></div>
  <div class="card"><h3>Press kit</h3><p style="margin:0">Images, bio, fact sheet &mdash; to assemble.</p></div>
  <div class="card" id="media"><h3>Media enquiry</h3><p style="margin:0">
    <a href="mailto:{SITE['email']}">{SITE['email']}</a></p></div>
</div>"""
    return f"""<section class="wrap page-top">
  <div class="section-head" style="text-align:center"><p class="eyebrow">{p["nav_label"]}</p>
    <h1 class="display">{p["display"]}</h1>
    <p class="lede" style="margin-inline:auto">{p["meaning"]}</p></div>
  <div style="text-align:center">{cta(p["action"])}</div>
  {extra}
</section>"""


def t_404(p):
    return f"""<section class="wrap page-top" style="text-align:center;min-height:60vh">
  <h1 class="display">Ti Sei Perso?</h1>
  <p class="lede" style="margin-inline:auto">It happens. Here’s the menu, a table, and
     how to find us.</p>
  <div class="hero__actions"><a class="btn" href="/menu/">A Tavola &mdash; the menu</a>
    {cta("reserve")}<a class="btn" href="/visit/">Vieni a Trovarci &mdash; visit</a></div>
</section>"""


# ===========================================================================
#  The 31 URLs (spec section 04)
# ===========================================================================

MENU_CRUMB = [("Menu", "/menu/")]
STORY_CRUMB = [("Our Story", "/our-story/")]
VISIT_CRUMB = [("Visit", "/visit/")]

PAGES = [
    dict(url="/", body_class="is-panels", nav_label="Home", display="Amami", tpl=t_home, action="reserve",
         title="Amami Italia — Tuscan Restaurant & Lounge in Brampton",
         description="Tuscan cooking in Brampton, from Chef Isabella Comello. Pasta, vino and late nights on Mayfield Road.",
         meaning="Love me."),

    dict(url="/menu/", share="pasta_finish", nav_label="Menu", display="A Tavola", tpl=t_menu_hub, action="menu",
         title="Menu — Tuscan Restaurant in Brampton | Amami Italia",
         description="Seven menus: dining, pizza, After Dark, wine, cocktails, chef's tasting and catering.",
         meaning="To the table."),

    dict(url="/menu/dining/", nav_label="Dining", display="Pranzo e Cena", tpl=t_menu_page,
         action="reserve", crumbs=MENU_CRUMB,
         title="Dining Menu — Italian Restaurant in Brampton | Amami Italia",
         description="Lunch and dinner. Hand-made pasta, Neapolitan pizza and 45-day dry-aged beef.",
         meaning="Lunch and dinner, from noon until we close."),

    dict(url="/menu/pizza/", nav_label="Pizza", display="Dal Forno", tpl=t_menu_page,
         action="reserve", crumbs=MENU_CRUMB, courses=["Rosse", "Bianche", "Calzoni"],
         title="Pizza Menu — Neapolitan Pizza in Brampton | Amami Italia",
         description="Neapolitan pizza from the oven. San Marzano DOP tomatoes.",
         meaning="From the oven."),

    dict(url="/menu/after-dark/", nav_label="After Dark", display="Dopo Cena", tpl=t_menu_page,
         action="lounge", crumbs=MENU_CRUMB, courses=["Small plates", "Late bites", "Sweet"],
         title="After Dark Small Plates — Late Night in Brampton | Amami Italia",
         description="Late small plates in the lounge.",
         meaning="After dinner."),

    dict(url="/menu/wine/", nav_label="Wine", display="La Cantina", tpl=t_menu_page,
         action="reserve", crumbs=MENU_CRUMB,
         courses=["Toscana", "Italy by region", "Sparkling", "By the glass"],
         title="Wine List — Italian Wine in Brampton | Amami Italia",
         description="Tuscan and Italian wine, by the glass and by the bottle.",
         meaning="A good idea in a bottle."),

    dict(url="/menu/cocktails/", nav_label="Cocktails", display="Aperitivi & Cocktails",
         tpl=t_menu_page, action="lounge", crumbs=MENU_CRUMB,
         courses=["Aperitivi", "Signatures", "Classics", "Zero proof"],
         title="Cocktails & Aperitivo — Lounge in Brampton | Amami Italia",
         description="Aperitivo hour and signature cocktails, including the limoncello spritz.",
         meaning="Aperitivo, and what to drink before dinner."),

    dict(url="/menu/tasting/", nav_label="Tasting Menu", display="Degustazione", tpl=t_menu_page,
         action="reserve", crumbs=MENU_CRUMB, courses=["The sequence"],
         title="Chef's Tasting Menu — Brampton | Amami Italia",
         description="The chef's own sequence. Notice period applies.",
         meaning="The tasting."),

    dict(url="/menu/catering/", nav_label="Catering", display="Fuori Casa", tpl=t_menu_page,
         action="catering", crumbs=MENU_CRUMB,
         courses=["Trays & platters", "Pasta", "Mains", "Dolci"],
         title="Catering Menu — Italian Catering in Brampton | Amami Italia",
         description="Catering menu for offices, homes and celebrations across Brampton and Caledon.",
         meaning="Away from home."),

    dict(url="/our-story/", share="room_wide", nav_label="Our Story", display="Tuscan at heart. Brampton at home.", tpl=t_story,
         action="reserve",
         title="Our Story — Tuscan Restaurant in Brampton | Amami Italia",
         description="Tuscan at heart, Brampton at home. How the cooking, the chef and the room came together.",
         meaning="Tuscan at heart. Brampton at home."),

    dict(url="/our-story/chef/", nav_label="Chef Isabella", display="Chef Isabella",
         tpl=t_chef, action="reserve", crumbs=STORY_CRUMB,
         title="Chef Isabella Comello — Amami Italia, Brampton",
         description="Chef Isabella is the heart of the Amami kitchen. Handmade pasta, slow-cooked sauce, extra parmigiano.",
         meaning="She takes pasta personally."),

    dict(url="/after-dark/", nav_label="After Dark", display="Amami After Dark",
         tpl=t_after_dark, action="lounge",
         title="Amami After Dark — Late Night Lounge in Brampton",
         description="The restaurant becomes a lounge. Cocktails, small plates and DJ nights.",
         meaning="Late in the room: cocktails, a short plate list and the lounge.",
         spaces=[("The Lounge", "Music up, plates smaller.", "Standing 60 · seated 30"),
                 ("The Bar", "Twelve seats, no reservation.", "12 at the bar")]),

    # /events/ is the "Catering & Events" page as published on 2026-08-20 —
    # the client asked for that version back, so the file is restored from the
    # 2026-08-20 deployment and the generator leaves it alone. It carries the
    # older chrome; reskinning it into this design system is a separate job.
    # Built to the events reference in the client's deck (2026-09-01): a title
    # card, then one block per space — photographs filling the frame with a
    # black panel of copy set into the corner and a capacity line. This replaces
    # the restored 2026-08-20 catering page, which stays in git history.
    dict(url="/events/", nav_label="Events", display="Eventi e Sala Privata", tpl=t_events,
         action="event", share="room_private",
         title="Events & Private Dining in Brampton | Amami Italia",
         description="Birthdays, engagements, work wins. Private dining and full buyouts on Mayfield Road.",
         meaning="Make a night of it.",
         spaces=[("The Private Room",
                  "Fully private, for milestone dinners, corporate tables and celebrations.",
                  "16–22", "seated"),
                 ("The Long Table",
                  "A single table through the middle of the room, for a party that wants to be seen.",
                  "24–30", "seated"),
                 ("Full Buyout",
                  "The whole room, dining and lounge, with the kitchen and the bar to yourself.",
                  "Up to 120", "standing")]),

    dict(url="/catering/", nav_label="Catering", display="Amami Fuori Casa", tpl=t_experience,
         action="catering",
         title="Italian Catering in Brampton & Caledon | Amami Italia",
         description="Amami, away from home. Catering for offices, homes and celebrations.",
         meaning="Amami, away from home.",
         spaces=[("Drop-off", "Trays and platters, delivered.", "10–100"),
                 ("Full service", "Our people come with it.", "20–200")]),

    dict(url="/visit/", nav_label="Visit", display="Vieni a Trovarci", tpl=t_visit, action="directions",
         title="Visit — Hours, Location & Parking | Amami Italia Brampton",
         description="Hours, address, parking and accessibility. 6261 Mayfield Rd, Brampton.",
         meaning="Come and find us."),

    dict(url="/visit/faq/", nav_label="FAQ", display="Buono a Sapersi", tpl=t_faq, action="reserve",
         crumbs=VISIT_CRUMB,
         title="FAQ — Amami Italia, Brampton",
         description="Reservations, parking, allergies, the tasting menu and private dining.",
         meaning="Good to know."),

    dict(url="/visit/contact/", nav_label="Contact", display="Scrivici", tpl=t_contact, action="reserve",
         crumbs=VISIT_CRUMB,
         title="Contact — Amami Italia, Brampton",
         description="Contact Amami Italia in Brampton by email, phone or the enquiry form.",
         meaning="Write to us."),

    # The reservation page as published 2026-08-20 — "Reserve a table / Tell us
    # when", the party-size/date/time selectors that carry through to the
    # OpenTable widget, and the "Before you come" notes. Restored rather than
    # regenerated, so the generator leaves the file alone.
    dict(url="/reservation/", nav_label="Reservations", display="Prenota",
         tpl=t_simple, action="reserve", static="the page published 2026-08-20",
         share="table_setting",
         title="Reserve a Table | Amami Italia",
         description="Book a table at Amami Italia on Mayfield Road, Brampton.",
         meaning="Book."),

    # /lounge/ is archived at the client's request (2026-08-31): the template
    # t_lounge is left in place, but the page is not built and the URL 308s to
    # /after-dark/, which is the same room. Put the dict back to bring it back.

    dict(url="/gift-cards/", nav_label="Gift Cards", display="Regala Amami", tpl=t_simple,
         action="purchase",
         title="Gift Cards — Amami Italia, Brampton",
         description="Give Amami. Gift cards for dining, the lounge and catering.",
         meaning="Hard to wrap. Easy to spend."),

    dict(url="/journal/", share="room_booths", nav_label="Journal", display="Il Quaderno", tpl=t_journal_index,
         action="reserve",
         title="Journal — Amami Italia, Brampton",
         description="Notes on Tuscan cooking, the room and Brampton.",
         meaning="Notes. Some about food, some about Brampton."),

    dict(url="/careers/", share="room_wide", nav_label="Careers", display="Lavora con Noi", tpl=t_simple, action="apply",
         title="Careers — Work at Amami Italia, Brampton",
         description="Front of house and kitchen roles at Amami Italia.",
         meaning="If you can cook, come and talk to us."),

    dict(url="/press/", share="room_wide", nav_label="Press", display="Si Parla di Noi", tpl=t_simple, action="media",
         title="Press & Recognition — Amami Italia, Brampton",
         description="Coverage, press kit and media enquiries.",
         meaning="People are talking about us."),

    # --- occasion landing pages ---
    dict(url="/date-night-brampton/", share="table_setting", nav_label="Date night", display="Una Sera per Due",
         tpl=t_landing, action="reserve",
         title="Date Night in Brampton — Italian Restaurant | Amami Italia",
         description="Date night in Brampton: Tuscan cooking, a low-lit room and a lounge to move to.",
         meaning="An evening for two, and nobody rushing you.",
         h2="Dinner, then the lounge",
         body="Get a booth. Order the burrata. Stay for the lounge.",
         cards=[("What to expect", "Low light. Nobody hurrying you."),
                ("What it costs", "Pasta from $28, secondi from $38."),
                ("How to book", "Online, or %s." % SITE["phone_display"])]),

    dict(url="/corporate-dining-brampton/", share="room_private", nav_label="Corporate dining", display="Cene di Lavoro",
         tpl=t_landing, action="event",
         title="Corporate Dining in Brampton — Private Rooms | Amami Italia",
         description="Corporate dinners and client entertaining in Brampton, with private rooms.",
         meaning="Dinner where people can actually hear each other.",
         h2="A room that can hold a conversation",
         body="Sixteen to twenty-two, with the door shut. Set menus if you want the bill known first.",
         cards=[("What to expect", "A door that closes."),
                ("What it costs", "Set menus, per head."),
                ("How to book", "Event enquiry, or %s." % SITE["phone_display"])]),

    dict(url="/celebrations-brampton/", share="room_private", nav_label="Celebrations", display="Le Feste",
         tpl=t_landing, action="event",
         title="Birthdays & Celebrations in Brampton | Amami Italia",
         description="Birthdays, anniversaries and celebrations in Brampton.",
         meaning="Get everyone in one room.",
         h2="Bring everyone",
         body="Twenty-two in the private room. Thirty at the long table. A hundred and twenty if you take the building.",
         cards=[("What to expect", "Family-style. Loud either way."),
                ("Gratuity", "18% for six or more."),
                ("How to book", "Event enquiry, or %s." % SITE["phone_display"])]),

    # --- catchment landing pages ---
    dict(url="/italian-restaurant-caledon/", share="room_wide", nav_label="Caledon", display="Da Caledon",
         tpl=t_landing, action="reserve",
         title="Italian Restaurant near Caledon | Amami Italia, Brampton",
         description="Tuscan dining minutes from Caledon, on Mayfield Road in north Brampton.",
         meaning="Down the hill from Caledon.",
         h2="Minutes from Caledon",
         body="Mayfield Road, the Caledon side of Brampton. Park outside, free.",
         cards=[("Where we are", "6261 Mayfield Rd, #140."),
                ("When we’re open", "Tuesday to Sunday from noon."),
                ("How to book", "Online, or %s." % SITE["phone_display"])]),

    dict(url="/italian-restaurant-bolton/", share="room_wide", nav_label="Bolton", display="Da Bolton",
         tpl=t_landing, action="reserve",
         title="Italian Restaurant near Bolton | Amami Italia, Brampton",
         description="Tuscan dining a short drive from Bolton.",
         meaning="A short run from Bolton.",
         h2="A short drive from Bolton",
         body="Mayfield Road, straight across the top of Brampton. Free parking.",
         cards=[("Where we are", "6261 Mayfield Rd, #140."),
                ("When we’re open", "Tuesday to Sunday from noon."),
                ("How to book", "Online, or %s." % SITE["phone_display"])]),

    dict(url="/italian-restaurant-vaughan/", share="room_wide", nav_label="Vaughan & Woodbridge",
         display="Da Vaughan", tpl=t_landing, action="reserve",
         title="Italian Restaurant near Vaughan & Woodbridge | Amami Italia",
         description="Tuscan dining for Vaughan and Woodbridge, on Mayfield Road.",
         meaning="Worth the drive from Vaughan and Woodbridge.",
         h2="For Vaughan and Woodbridge",
         body="West along Mayfield and you’re here. Free parking.",
         cards=[("Where we are", "6261 Mayfield Rd, #140."),
                ("When we’re open", "Tuesday to Sunday from noon."),
                ("How to book", "Online, or %s." % SITE["phone_display"])]),

    dict(url="/404/", nav_label="Not found", display="Ti Sei Perso?", tpl=t_404, action="reserve",
         title="Page not found | Amami Italia",
         description="That page does not exist. Here is the menu, reservations and how to find us.",
         meaning="Lost?"),
]

# Legal hub + six children
PAGES.append(dict(url="/legal/", nav_label="Legal", display="Legal", tpl=t_utility, action="",
                  title="Legal | Amami Italia",
                  description="Privacy, cookies, accessibility and terms.",
                  meaning="Policies and terms for Amami Italia."))
for label, url in LEGAL:
    PAGES.append(dict(url=url, nav_label=label, display=label, tpl=t_utility, action="",
                      crumbs=[("Legal", "/legal/")],
                      title=f"{label} | Amami Italia",
                      description=f"{label} policy for Amami Italia, Brampton.",
                      meaning=f"{label} policy."))


# Booking on the page, not on opentable.ca. The availability page is the only
# OpenTable surface that carries the whole journey — find a table, pick a time,
# add your details — so it is what is embedded. It rendered when it was built
# this morning; later the same day it started returning a frame that will not
# paint from this network, which looks like rate limiting rather than a policy
# change (their own widget canvas, a different path, keeps serving).
#
# So the embed is primary and a link sits under it, and the page never ends up
# with nothing bookable on it. If OpenTable has genuinely stopped allowing this,
# the fallback below becomes the booking route and the honest fix is OpenTable's
# reservation API, which needs partner credentials from them.
OT_EMBED = (
    '<div class="rs-form rs-otembed">\n'
    # never lazy: a booking form that waits for a scroll reads as a broken page
    '<iframe title="Book a table at Amami Italia"\n'
    '        src="https://www.opentable.ca/booking/restref/availability'
    '?rid=1470808&amp;restref=1470808&amp;lang=en-CA'
    '&amp;otSource=Restaurant%20website"\n'
    '        style="display:block;width:100%;height:clamp(720px,86vh,1040px);'
    'border:0;background:transparent"></iframe>\n'
    '</div>\n'
    '<p class="rs-alt-note">Every step happens here &mdash; find a table, pick a time, '
    'add your details. If the form does not load, '
    '<a href="' + SITE["opentable"] + '" target="_blank" rel="noopener">book on OpenTable</a>. '
    'Eight or more is best arranged by phone.</p>\n'
)


def patch_reservation_widget(src):
    """Put the whole OpenTable booking flow where the captured page had a dummy form.

    The 2026-08-20 page carried the theme's `qodef-reservation-form`, whose
    hidden `rid` and `restref` were both `1` — it was never wired to the
    restaurant, so no widget ever appeared. Everything between the "Book online"
    label and the "prefer to speak to someone" line is replaced: the dummy form,
    and the two carry-through buttons that existed to compensate for it.

    Anchoring on those two labels rather than on the markup being replaced keeps
    this idempotent — it re-patches its own output on the next build, so the
    embed can be changed here and every build picks it up.

    The page's own booking JS starts `if(!form) return;`, so it stands down on
    its own once the form is gone.
    """
    head = '<span class="rs-k rs-k--sm">Book online</span>'
    tail = '<p class="rs-call">'
    i = src.find(head)
    if i == -1:
        return src, None
    j = src.find(tail, i)
    if j == -1:
        return src, "booking section found but its end marker moved"
    body = src[i + len(head):j]
    if body.strip() == OT_EMBED.strip():
        return src, None
    return src[:i + len(head)] + "\n" + OT_EMBED + src[j:], \
        "full OpenTable booking flow in place of the dummy form"


RS_GROUP = """<!--amami:groupline-->
<section class="rs-notes">
<span class="rs-k rs-k--sm">More people. More pasta. More fun.</span>
<div class="rs-note">
<span class="rs-note-k">Groups</span>
<p>Bringing the whole crew? <a href="/events/#enquiry">Plan your party</a>.</p>
</div>
</section>
<!--/amami:groupline-->"""


RS_NOTES = """<!--amami:rsnotes-->
<section class="rs-notes">
<span class="rs-k rs-k--sm">Before you come</span>
<div class="rs-note"><span class="rs-note-k">Dress</span>
<p>Semi formal in the evening. Collared shirt and trousers, or a dress.</p></div>
<div class="rs-note"><span class="rs-note-k">Running late</span>
<p>Call us.</p></div>
<div class="rs-note"><span class="rs-note-k">Larger tables</span>
<p>Six or more, call. Gratuity of 18% applies.</p></div>
<div class="rs-note"><span class="rs-note-k">The lounge</span>
<p>Port, amaro, grappa, coffee. No table wine.</p></div>
</section>
<!--/amami:rsnotes-->"""


def patch_reservation_copy(src):
    """The client's reservation copy (2026-09-03) on the restored page.

    The page predates the generator, so its words live in its own HTML. Both
    replacements write a fixed string over whatever is there, which makes the
    patch idempotent — it can re-patch its own output on the next build.
    """
    notes = []
    new_h1 = '<h1 class="rs-title">Pull up a chair.</h1>' 
    out = re.sub(r'<h1 class="rs-title">.*?</h1>', new_h1, src, count=1, flags=re.S)
    if out != src:
        notes.append("reservation title")
        src = out

    new_lede = ('<p class="rs-lede">Dinner\u2019s ready when you are.</p>\n'
                '<p class="rs-lede">Come hungry.</p>')
    out = re.sub(r'<p class="rs-lede">.*?</p>(\s*<p class="rs-lede">.*?</p>)*',
                 new_lede, src, count=1, flags=re.S)
    if out != src:
        notes.append("reservation lede")
        src = out

    # The "Before you come" block still carried two [TBC] placeholders and the
    # old long lines. Replaced whole, and marker-wrapped so later builds replace
    # it rather than find one already there and leave it.
    if "<!--amami:rsnotes-->" in src:
        i = src.index("<!--amami:rsnotes-->")
        j = src.index("<!--/amami:rsnotes-->") + len("<!--/amami:rsnotes-->")
        if src[i:j] != RS_NOTES:
            src = src[:i] + RS_NOTES + src[j:]
            notes.append("before-you-come refreshed")
    else:
        m = re.search(r'<section class="rs-notes">(?:(?!</section>).)*?Before you come'
                      r'.*?</section>', src, re.S)
        if m:
            src = src[:m.start()] + RS_NOTES + src[m.end():]
            notes.append("before-you-come rewritten ([TBC] placeholders removed)")

    # An aphorism the page closed on. Gone.
    out = re.sub(r'<section class="rs-philosophy">.*?</section>', "", src, count=1, flags=re.S)
    if out != src:
        src = out
        notes.append("closing line removed")

    # The embed note explained the widget the guest is already looking at.
    out = re.sub(r'<p class="rs-alt-note">.*?</p>',
                 '<p class="rs-alt-note">Not loading? '
                 '<a href="https://www.opentable.ca/booking/restref/availability?'
                 'lang=en-CA&restRef=1470808&otSource=Restaurant%20website" target="_blank" '
                 'rel="noopener">Book on OpenTable</a>. Eight or more, call us.</p>',
                 src, count=1, flags=re.S)
    if out != src:
        src = out
        notes.append("embed note shortened")

    if "<!--amami:groupline-->" in src:
        i = src.index("<!--amami:groupline-->")
        j = src.index("<!--/amami:groupline-->") + len("<!--/amami:groupline-->")
        if src[i:j] != RS_GROUP:
            src = src[:i] + RS_GROUP + src[j:]
            notes.append("group-dining block refreshed")
    else:
        anchor = '<section class="rs-notes">'
        if anchor in src:
            src = src.replace(anchor, RS_GROUP + "\n" + anchor, 1)
            notes.append("group-dining block added")
    return src, ", ".join(notes)


def social_meta(page):
    """Canonical + link-preview tags, as a block, so the static pages can carry
    exactly what the generated ones do."""
    url = ORIGIN + page["url"]
    img_url, img_alt = share_image(page)
    title = html.escape(page["title"])
    desc = html.escape(page["description"])
    it_title = IT.get(page["title"])
    title_it = ' data-title-it="%s"' % html.escape(it_title, quote=True) if it_title else ""
    return f"""<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:locale" content="en_CA">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{img_url}">
<meta property="og:image:secure_url" content="{img_url}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{html.escape(img_alt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{img_url}">
<meta name="twitter:image:alt" content="{html.escape(img_alt)}">
"""


# Text nodes inside these must not be wrapped in a span.
# <html> and <head> are always on the stack, so they must not be listed here.
# "span!" marks a span this pass already added: without it a static page
# would gain a nested span around the same text on every build.
NO_SPAN = ("title", "option", "textarea", "script", "style", "select", "span!")
_SEG = re.compile(r"(<script\b.*?</script>|<style\b.*?</style>|<[^>]+>)", re.S | re.I)
_TAGNAME = re.compile(r"<\s*(/?)\s*([a-zA-Z0-9-]+)")


_SPAN_IT = re.compile(r'<span data-it="[^"]*">((?:(?!<span data-it=)(?!</span>).)*?)</span>', re.S)
_ATTR_IT = re.compile(r'\s+data-it="[^"]*"')


def strip_italian(page_html):
    """Undo a previous annotation pass.

    A static page keeps whatever was baked into it, so without this the Italian
    frozen into it on an earlier build never picks up a correction to the
    dictionary. Stripping first makes the dictionary the only source and makes
    the pass idempotent.
    """
    prev = None
    while prev != page_html:
        prev = page_html
        page_html = _SPAN_IT.sub(lambda m: m.group(1), page_html)
    return _ATTR_IT.sub("", page_html)


def annotate_italian(page_html):
    """Mark every translatable text node with its Italian.

    The switch is a client-side swap, so both languages ship in the page: the
    English stays as the element's text and the Italian rides along in data-it.
    Keying the dictionary on the English text means a string nobody has
    translated yet simply stays English.
    """
    out, stack, hits = [], [], 0
    for seg in _SEG.split(page_html):
        if not seg:
            continue
        if seg.startswith("<"):
            m = _TAGNAME.match(seg)
            if m:
                closing, name = m.group(1), m.group(2).lower()
                if closing:
                    if stack and stack[-1] in (name, name + "!"):
                        stack.pop()
                elif ("</%s" % name) in seg.lower():
                    # a whole <script>…</script> or <style>…</style> block came
                    # through as one segment: it opens and closes here, so it
                    # must not be pushed and left on the stack for good
                    pass
                elif not seg.rstrip().endswith("/>") and name not in (
                        "br", "img", "input", "meta", "link", "hr", "source"):
                    stack.append(name + "!" if name == "span" and "data-it=" in seg else name)
            out.append(seg)
            continue
        text = seg.strip()
        italian = IT_LOOKUP.get(" ".join(text.split()))
        if not italian:
            out.append(seg)
            continue
        # <option> and <textarea> cannot hold a span, so the attribute goes on
        # the element itself — the switch swaps textContent either way.
        if stack and stack[-1] in ("option", "textarea"):
            for k in range(len(out) - 1, -1, -1):
                if out[k].startswith("<") and not out[k].startswith("</"):
                    if "data-it=" not in out[k]:
                        out[k] = out[k].rstrip(">").rstrip("/") + \
                            ' data-it="%s">' % html.escape(italian, quote=True)
                    break
            out.append(seg)
            continue
        if any(t in NO_SPAN for t in stack):
            out.append(seg)
            continue
        lead = seg[:len(seg) - len(seg.lstrip())]
        trail = seg[len(seg.rstrip()):]
        out.append('%s<span data-it="%s">%s</span>%s'
                   % (lead, html.escape(italian, quote=True), text, trail))
        hits += 1
    return "".join(out), hits


def patch_static(target, page):
    """Keep a hand-held page's own body, but give it the site's header and footer.

    The restored pages predate this generator and came with the old theme's
    chrome. Rather than leave the site wearing two different headers and two
    different footers, both are swapped for the real ones on every build, and
    the stylesheets they need (plus the brand fonts and the header's script)
    are added. Nothing else on the page is touched — amami.css is deliberately
    NOT linked, because its body and element rules would restyle everything
    below the header.
    """
    if not target.exists():
        return "missing on disk — nothing to patch"
    # Undo the previous pass's annotations FIRST. Every patch below anchors on
    # the page's own text, and an annotated page has that text wrapped in spans
    # — which is why the booking block stopped being updated after the first
    # build and kept an embed that had since been replaced.
    src = strip_italian(target.read_text())
    notes = []

    # The captured theme ships a desktop header and a mobile one. Both go; the
    # page's own <header class="rs-head"> and the like must survive, so this
    # matches on the theme's ids rather than on the tag.
    for hid in ("qodef-page-header", "qodef-page-mobile-header"):
        i = src.find('<header id="%s"' % hid)
        if i == -1:
            continue
        j = src.find("</header>", i)
        if j == -1:
            continue
        src = src[:i] + src[j + len("</header>"):]
        notes.append("%s removed" % hid)

    # The chrome is wrapped in markers so a later build REPLACES it instead of
    # seeing one already there and leaving it alone. Without this the header on
    # these two pages froze at whatever the nav looked like the day it was first
    # inserted — it was still offering Lounge and Visit after both had gone.
    chrome = "<!--amami:chrome-->" + header() + overlay(page) + "<!--/amami:chrome-->"
    if "<!--amami:chrome-->" in src:
        head_i = src.index("<!--amami:chrome-->")
        tail_i = src.index("<!--/amami:chrome-->") + len("<!--/amami:chrome-->")
        if src[head_i:tail_i] != chrome:
            src = src[:head_i] + chrome + src[tail_i:]
            notes.append("header and nav overlay refreshed")
    else:
        m = re.search(r"<body[^>]*>", src)
        if m:
            body_tag = m.group(0)
            if "has-amami-hdr" not in body_tag:
                if 'class="' in body_tag:
                    body_tag = body_tag.replace('class="', 'class="has-amami-hdr ', 1)
                else:
                    body_tag = body_tag[:-1] + ' class="has-amami-hdr">'
            if "data-hours" not in body_tag:
                body_tag = body_tag[:-1] + " data-hours='%s'>" % json.dumps(HOURS)
            src = src[:m.start()] + body_tag + chrome + src[m.end():]
            notes.append("site header and nav overlay added")

    src, note = patch_reservation_widget(src)
    if note:
        notes.append(note)

    src, note = patch_reservation_copy(src)
    if note:
        notes.append(note)

    lower = src.lower()
    i, j = lower.find("<footer"), lower.rfind("</footer>")
    if i != -1 and j != -1:
        new = src[:i] + footer_markup() + src[j + len("</footer>"):]
        if new != src:
            src, _ = new, notes.append("footer replaced with the site footer")
    else:
        notes.append("no <footer> element found")

    for link in ('<link rel="stylesheet" href="/_assets/amami-header.css">',
                 '<link rel="stylesheet" href="/_assets/amami-footer.css">',
                 '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:'
                 'ital,wght@0,300;0,400;0,500;1,400&family=Poppins:wght@300;400;500;600'
                 '&display=swap" rel="stylesheet">'):
        if link not in src and "</head>" in src:
            src = src.replace("</head>", link + "\n</head>", 1)
            notes.append("head link added")

    bar = "<!--amami:bar-->" + mobile_bar() + "<!--/amami:bar-->"
    if "<!--amami:bar-->" in src:
        b0 = src.index("<!--amami:bar-->")
        b1 = src.index("<!--/amami:bar-->") + len("<!--/amami:bar-->")
        if src[b0:b1] != bar:
            src = src[:b0] + bar + src[b1:]
            notes.append("quick-action bar refreshed")
    elif "</body>" in src:
        src = src.replace("</body>", bar + "\n</body>", 1)
        notes.append("mobile quick-action bar added")

    # The captured head still points its canonical at amamiitalia.com — at
    # /catering-services/ in the events page's case, which is not even this
    # URL any more — and its link-preview tags came from the old page. Both are
    # replaced with this build's, so an ad or a shared link resolves to the
    # page it actually landed on and shows the right card.
    before = src
    src = re.sub(r"\s*<link[^>]*rel=[\"']canonical[\"'][^>]*>", "", src)
    src = re.sub(r"\s*<link[^>]*rel=[\"']canonical[\"'][^>]*/>", "", src)
    src = re.sub(r"\s*<meta[^>]*(?:og:|twitter:)[^>]*>", "", src)
    if "</head>" in src:
        src = src.replace("</head>", social_meta(page) + "</head>", 1)
        if src != before:
            notes.append("canonical and link-preview tags rewritten")

    # Tracking, so a restored page reports into the same container as the rest of
    # the site rather than whatever was on it the day it was captured. Marked, so
    # a later build recognises its own work instead of stripping and re-adding it
    # in a different place every run.
    if "<!--amami:gtm-->" not in src:
        # whatever container the capture came with goes first
        src = re.sub(r"<script[^>]*>[^<]{0,600}?GTM-[A-Z0-9]{6,}[^<]{0,600}?</script>", "", src)
        src = re.sub(r"<noscript>\s*<iframe[^>]*googletagmanager[^>]*>\s*</iframe>\s*</noscript>",
                     "", src, flags=re.I)
        if "</head>" in src:
            src = src.replace("</head>", "<!--amami:gtm-->" + GTM_HEAD + "<!--/amami:gtm-->\n</head>", 1)
        m = re.search(r"<body[^>]*>", src)
        if m:
            src = src[:m.end()] + "\n" + GTM_BODY + src[m.end():]
        notes.append("GTM added")

    for src_tag in ('<script src="/_assets/amami.js" defer></script>',
                    '<script src="/_assets/amami-i18n.js"></script>'):
        if src_tag not in src and "</body>" in src:
            src = src.replace("</body>", src_tag + "\n</body>", 1)
            notes.append("switch script added")
    script = '<!-- scripts in place -->'
    if script not in src and "</body>" in src:
        src = src.replace("</body>", script + "\n</body>", 1)
        notes.append("header script added")

    src, hits = annotate_italian(src)
    if hits:
        notes.append("%d strings marked for the language switch" % hits)

    target.write_text(src)
    return "; ".join(notes) if notes else "already current"


def write_sitemap():
    """A sitemap built from PAGES.

    It matters more than usual here: the footer no longer lists every page, so
    Catering, Journal, Gift Cards, Careers, Press, Visit, FAQ and Contact have
    no link from the site's chrome. This is what keeps them discoverable. The
    404 page is left out.
    """
    today = datetime.date.today().isoformat()
    urls = []
    for p in PAGES:
        if p["url"] == "/404/":
            continue
        priority = "1.0" if p["url"] == "/" else "0.8" if p["url"].count("/") == 2 else "0.6"
        urls.append("  <url><loc>%s%s</loc><lastmod>%s</lastmod>"
                    "<priority>%s</priority></url>" % (ORIGIN, p["url"], today, priority))
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls) + "\n</urlset>\n")
    (ROOT / "robots.txt").write_text(
        "User-agent: *\n"
        "Allow: /\n\n"
        "# The old file pointed at amamiitalia.com's WordPress sitemap over http.\n"
        "Sitemap: %s/sitemap.xml\n" % ORIGIN)
    return len(urls)


def main():
    written, kept = [], []
    for p in PAGES:
        p.setdefault("meaning", "")
        target = ROOT / p["url"].strip("/") / "index.html" if p["url"] != "/" else ROOT / "index.html"
        # A page marked `static` is hand-held HTML that predates this generator.
        # It is listed here so the nav and the sitemap still know about it, but
        # the file on disk is the deliverable — never overwrite it.
        if p.get("static"):
            kept.append((p["url"], patch_static(target, p)))
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        page_html, _ = annotate_italian(head(p) + p["tpl"](p) + footer())
        target.write_text(page_html)
        written.append((p["url"], target.relative_to(ROOT)))
    n = write_sitemap()
    print(f"{len(written)} pages written, {len(kept)} kept as published, "
          f"{n} URLs in sitemap.xml\n")
    for url, path in written:
        print(f"  {url:36} -> {path}")
    for url, why in kept:
        print(f"  {url:36} -- kept, {why}")
    print("\nHome is written to index.html. The original WordPress capture is\n"
          "kept as index-wp-legacy.html and in git history.")


if __name__ == "__main__":
    main()
