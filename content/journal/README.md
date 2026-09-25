# Journal (Il Quaderno) — content format

Every Journal post is one JSON file in `content/journal/posts/<slug>.json`.
`python3 tools/build-journal.py` (run from the repo root) turns them into:

- `/journal/` and `/it/journal/` — the list, newest first, with category filters
- `/<slug>/` and `/it/<slug>/` — the post, in English and Italian
- the Journal entries in `src/sitemap.xml`

A client portal (or anyone) publishes a post by writing this file and running
the build; nothing else needs touching. The Journal is linked only from the
small "Journal" / "Il Quaderno" link in every page's footer bar — never from
the home page or the top menu.

## A post

```json
{
  "slug": "truffle-season-at-amami",
  "date": "2026-10-05",
  "category": "italian-dining",
  "photo": {
    "base": "/wp-content/uploads/2026/10/truffle-pasta",
    "width": 1600,
    "height": 2400
  },
  "en": {
    "title": "Truffle Season at Amami",
    "photo_alt": "Tagliatelle with shaved white truffle",
    "excerpt": "One sentence for the Journal list.",
    "body_html": "<p>The writing…</p><h2>A heading</h2><p>…</p>",
    "seo_title": "Truffle Season in Brampton | Amami Italia",
    "seo_description": "What Google shows under the title: 120–155 characters.",
    "og_image": "",
    "og_alt": ""
  },
  "it": { "…same keys, in Italian…": "" }
}
```

| Field | What it is | Rules |
|---|---|---|
| `slug` | the address: `amamiitalia…/<slug>/` | lowercase, hyphens, must match the file name; never change it once published |
| `date` | publish date | `YYYY-MM-DD`; the list is sorted by it |
| `category` | one key from `categories.json` | add new categories there first (with `en` and `it` names) |
| `photo.base` | the photo, without extension | the build expects `<base>.jpg` (and `<base>.webp`) at `width` px wide, plus `-480w`, `-800w`, `-1200w` versions of each where they exist; new files get new names (uploads are cached for a year) |
| `title` | the post title | shown on the page and the list |
| `photo_alt` | one line describing the photo | for Google Images and screen readers |
| `excerpt` | one sentence | shown on the Journal list |
| `body_html` | the writing | `<p>`, `<h2>`, `<h3>`, `<ul>/<li>`, `<strong>`, `<em>`, `<a>` only; Italian links point at `/it/…` pages where they exist |
| `seo_title` | **what Google shows as the title** | max 60 characters, end with ` \| Amami Italia` |
| `seo_description` | **what Google shows under the title** | 120–155 characters, a real sentence |

Both `en` and `it` are required; the build stops and says which file is
incomplete. `og_image` / `og_alt` are optional (the share card uses the photo).
