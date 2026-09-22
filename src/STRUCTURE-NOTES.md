# Amami Italia — structure build, state and open questions

Live: **https://amami-italia.vercel.app** (Vercel project `amami-italia`, team
the-ethereal-agency). All 37 URLs from the architecture document return 200.

`amamiitalia.com` and `www.amamiitalia.com` are **not** pointed at this project
yet — they still serve the old WordPress site. Nothing public changed.

## No WordPress in the new build

The new site is plain static HTML, CSS and one small JS file. No PHP, no
theme, no plugins, no database, no build step.

- `_assets/amami.css`, `_assets/amami.js` — the whole front end.
- `tools/build_structure.py` — generates every page from one place.
- `tools/menu_data.py` — the menu content.
- Forms use the Google Apps Script pattern already in `apps-script/`, which
  runs off-site and so does not need WordPress.

`index-wp-legacy.html` keeps the original WordPress capture for reference. The
`wp-content/` folder is still on disk only because the old media lives there;
no new page loads anything from it.

## Menus are HTML, not a PDF

75 items are published as live HTML text — names, descriptions, prices,
vegetarian and gluten-free marks, add-ons, and the gratuity and split-cheque
notes. Selectable, translatable and indexable. No PDF and no flattened image
of a menu anywhere.

- `/menu/dining/` — 32 items: Antipasti, Primi Piatti, Secondi, Contorni, Dolci
- `/menu/after-dark/` — 43 items: Porto & dessert wine, Digestivi, Liquore,
  Grappa, Caffè e Specialità

Transcribed by hand from `1787148406161-Amami Menu 2026.pdf`, which is
image-only — no embedded text to extract.

## Colours and fonts are the brand's own

Taken from the live site's own declarations, not invented:

| Token | Value | |
|---|---|---|
| `--bronze` | `#a87a41` | brand bronze |
| `--bronze-lit` | `#ca9d75` | lit bronze, most-used accent |
| `--cream` | `#fdf8f4` | brand cream |
| `--cream-warm` | `#f7efe6` | blush |
| `--ink` | `#0b0908` | ground |
| `--warm` | `#433e37` | warm brown |
| `--serif` | Cormorant Garamond | matches the site's `--am-serif` |
| `--sans` | Jost | matches the site's `--am-sans` |

## Layouts follow the reference screenshots

Built from `~/Downloads/Amami structure/` (the ANIML Steakhouse captures), not
from the architecture document's prose:

- **Home** — a vertical stack of full-bleed panels, each one photograph, one
  large word and one action, with the brand ground showing as a frame between
  them. The architecture's ten beats survive as destinations, not paragraphs.
- **Nav** — full-screen overlay, large serif links, Reserve and the contact
  details on the right, circular close button.
- **Menu hub** — the menu names as a row of large serif tabs over a photo grid.
- **Our Story** — very large centred title on the brand ground, then blocks of
  photograph against a dark panel with centred copy.
- **Events / After Dark** — edge-to-edge photo mosaic with one dark text panel
  carrying a bold room name and a capacity line.
- **Contact band** — a room photograph, a map card, then three columns.

## Real media is wired in

`tools/media_map.py` maps 20 named slots to the files we actually have,
classified by looking at a contact sheet of every candidate rather than
guessing from camera filenames. 22 files are on the pages, including
`dining-loop.mp4` behind the home hero and the real pizza photograph.

## Where the gaps are

31 labelled placeholders across 14 pages, down from 85. Each states on the
page what belongs there, so nothing is silently missing.

| Page | Gaps |
|---|---|
| `/menu/wine/`, `/menu/cocktails/`, `/menu/catering/` | 4 each |
| `/menu/pizza/` | 3 |
| the six local landing pages | 2 each |
| `/menu/tasting/`, `/our-story/chef/` | 1 each |

Most remaining gaps are missing **lists**, not missing photographs.

## Open questions — content, not code

Nothing technical is blocking. These need answers from the client.

1. **Who is the chef?** The printed 2026 menu says *"Crafted by Chef Isabella
   Comello"* and *"made with love, by Linda, in our kitchen"*. The
   architecture document is built around *Chef Gianluca Martinucci*,
   and the home page, `/our-story/` and `/our-story/chef/` all carry that
   claim. One of the two is out of date. This is the biggest open item —
   several pages change depending on the answer.
2. **Is there pizza?** The architecture has `/menu/pizza/` ("Dal Forno") and
   there is a real pizza photograph in the media library, but the 2026 printed
   menu has no pizza section. The page exists and now carries that photograph;
   it needs the actual list of pizzas and prices.
3. **"Dopo Cena" is used twice.** The printed menu uses it for after-dinner
   drinks; the architecture uses it as the display name for After Dark small
   plates. One needs renaming.
4. Wine, cocktail, tasting and catering lists — not in the printed menu.
5. Six photography shoots.
6. Toast Tables link for the lounge; gift-card provider; Google rating and
   review excerpts; parking and accessibility facts; lounge age policy;
   tasting-menu notice period; legal copy.

## Still to do

- Point `amamiitalia.com` at this project when the content is signed off.
- Redirect map from the old WordPress URLs.
- `sitemap.xml`, `robots.txt`, 404 wiring.
- Schema: Restaurant, Menu, FAQPage, BreadcrumbList.
- Wire the ~50 existing photos into slots (camera filenames, so they need
  sorting first).
- Deploy the Apps Script endpoints for the event, catering and contact forms.
