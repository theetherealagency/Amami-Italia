# Amami Italia — working brief for the next Claude session

You are picking up the amamiitalia.etherealpr.com build from another Claude Code session (Srishti's, 21 Sep 2026).
Everything below is current as of commit `194dec8` on `main`. Read this whole file, then `design-system.md`,
then `HANDOFF-2026-09-21.md` before touching anything. Do not re-derive what is written here.

---

## 1. Where things are

| | |
|---|---|
| Repo | `github.com/theetherealagency/Amami-Italia`, branch `main`. Static HTML — no build step, no framework, no npm in the site itself. |
| Site root | `src/` — every page is `src/<path>/index.html`. Shared CSS/JS in `src/_assets/`. Images under `src/wp-content/uploads/` (WordPress-era paths kept on purpose). |
| Live | https://amamiitalia.etherealpr.com — Vercel project **amami-italia** (`prj_ctLKopDHaBjSvL5l13XQv3RbzQQH`, team `team_CuPVTaxmQI9MYWKoB8nAK2A7`). Auto-deploys from `main` in ~30–60 s. **Root Directory is `src`** — if everything 404s after a deploy, that setting has been lost. |
| Wrong project | `prj_dW2toCkEkZFy0STjKoqaSdnDAlq8` is *amami-landing*. Not this site. |
| Config | `src/vercel.json` — `trailingSlash: true`, `cleanUrls: false`, and **`/wp-content/uploads/*` is served `Cache-Control: immutable`** (see §3, rule 1). |
| Design system | `design-system.md` (repo root) — tokens, type, spacing, the vw-scaling rule, component inventory. The homepage is the reference implementation. |
| Hand-off | `HANDOFF-2026-09-21.md` — what shipped against the master brief, files changed, **the open decisions**, copy removed. |
| Brief the work was built to | `/Users/srishtikundnani/Downloads/amami-claude-code-master-prompt.md` (Srishti's machine; ask her for a copy if you need §7 wording verbatim). |
| Tools | `tools/serve.py` (no-store dev server), `tools/build-it.py` (regenerates `/it/`), `tools/verify.js` (headless verification). |

## 2. Page map

**The seven brief pages** (rebuilt, bilingual, motion, `<picture>`/WebP, 44px targets):
`/` · `/menu/` · `/our-story/` · `/after-dark/` · `/events/` · `/reservation/` · `/contact/`
and their Italian mirrors `/it/`, `/it/menu/`, … `/it/contact/` (generated — **never hand-edit `src/it/`**).

**Rebuilt 2026-09-23 on the same `.pg-*` kit (English only; IT switch points at `/it/`):** `/catering/`, `/careers/`, `/gift-cards/`,
`/legal/` + six policies, `/menu/dining/`, `/menu/after-dark/`, the five coming-soon menus (`pizza`, `wine`, `cocktails`, `tasting`, `catering`),
`/visit/faq/`, `/press/`, `/journal/`, `/our-story/chef/`, the three occasion and three town landing pages, `/404/`, and the five journal posts.
Each is plain static HTML with the `/contact/` page's head, header and footer; edit it directly. New kit pieces in `amami-pages.css`:
`.pg-head` (cream page head), `.pg-anchors`, `.pg-menu` + `.dish` rows, `.pg-notes`, `.pg-prose` (posts/legal), `.pg-faq`, `.pg-facts--3`.
Open `TODO(legal)`, `TODO(menu)`, `TODO(gift-cards)` comments mark copy the client still has to supply — do not invent it.

**Redirected 2026-09-23** (see `src/vercel.json`): the raw WordPress copies (`/about-us/`, `/book-a-table/`, `/contact-us/`, `/dining-menu/`,
`/food-menu/`, `/drinks/`, `/lounge-menu/`, `/catering-menu/`, `/catering-services/`, `/dining-experience/`, `/privacy-policy-2/`, archives,
`/test/`, `/thank-you/`, `/site-map/`) and the duplicate `/visit/`, `/visit/contact/` → their new pages. Still raw WordPress, left on purpose:
`/christmas-menu/`, `/new-years-menu/`, `/valentines-day-menu/`.

## 3. Rules that will bite you if you skip them

1. **Changed asset ⇒ new filename.** `/wp-content/uploads/*` is `immutable` for a year. Overwriting `home-room-poster.jpg` in place means nobody sees the change (this happened; the fix was `home-room-poster-1s.jpg`). Add a suffix, update every reference.
2. **The seven EN pages are the source for `/it/`.** After editing any of them: `cd src && python3 ../tools/build-it.py`, then commit `src/it/` with your change. Italian text lives in `data-it="…"` attributes on leaf elements in the EN source; page titles in `data-title-it` on `<html>`; meta descriptions and OG alts in the dicts at the top of `build-it.py`. New copy without a `data-it` stays English on the Italian page — add the Italian when you add the English.
3. **Lengths are `vw`, not `px`.** The comp is a 1366-wide artboard; every length is `comp_px / 1366` as `vw`, with `max(Npx, Xvw)` floors only where text would become unreadable. Full-bleed headlines are `100vw / measured-width-ratio`. Follow `design-system.md`; do not introduce breakpoint-specific pixel values on desktop.
4. **Footer and header are byte-identical on all pages.** Edit them with a regex across every `*.html`, not in one file. Header switch markup: `<a href="/x/" hreflang="en-CA" lang="en" aria-current="true|false">EN</a><i aria-hidden="true">|</i><a href="/it/x/" hreflang="it" lang="it" …>IT</a>` (legacy pages point IT at `/it/`).
5. **Hours have one source.** `data-hours` on `<body>` (JSON, `[open, close]`, a day may be `[[12,15],[17,22]]`, close may be `null` = "open from, close not stated"), the footer `<dl class="ftr__hours">`, the contact page and the JSON-LD `openingHoursSpecification` all carry the same set. Change all four together, on every page.
6. **Do not invent facts.** The brief's §7 items (chef credit, lounge hours, wine policy, group size, the salad) are `TODO(...)` comments in source. Resolve one only when the client answers; then remove the TODO and update `HANDOFF-2026-09-21.md`.
7. **Motion CSS: keep `:where()`.** `.motion main > section:where(:not(.pg-hero):not(.hm-hero))` deliberately has low specificity so `.is-in` wins. Adding `:not()` outside `:where()` will hide whole sections again.
8. **`<picture>` must stay `display:contents`** (`body.is-home picture`, `body.is-page picture`) or the `<img>` stops being the grid child and every split layout breaks.
9. **Verify with headless Chrome, not the desktop-app browser pane.** The pane frequently runs `visibilityState: "hidden"`: IntersectionObserver, scroll events, rAF and lazy images never fire there and screenshots come out as a blank cream rectangle. Chrome there also served stale CSS despite cache-busting. Use `tools/serve.py` + `tools/verify.js`.
10. **Fonts by role (brand book):** headlines Cormorant Garamond; subtitles / accent lines **IM Fell English italic** (`--accent` in `amami.css`, loaded on every page via the Google Fonts link `&family=IM+Fell+English:ital@0;1`); body Poppins. IM Fell stands in for the comp's Forward Serif, which is personal-use only and is not shipped. Do not add Forward Serif unless a licence arrives.
11. **Brand palette only (brand book p.12):** Charcoal Black `#161616`, Warm Beige `#eee9da`, Mist Blue `#cbd6e3`, Tuscan Brown `#462e24`, Medium Rare Red `#812b28`. The old gold `#ca9d75` is gone (header token `--h-bronze-lit` is now Mist Blue). Photos with colour baked in (e.g. the home band `home-band-tuscany-812b28.jpg`) were re-tinted and renamed, per rule 1.
12. **Photos: hands and close-ups only.** No stock photos where a face or a non-staff person is visible. Client photos (Private Dining, Catering, chef `chef-isabella-cocktail.*` developed from `DSC9929.ARW`) are fine. The home Explore/Menu slides are `home-pasta-hand-4, 3, 2, 6, 1`.
13. **OpenTable is sized by script, not a fixed loader.** Home and Reservation (EN and IT) have `<div class="ot-slot">` plus an inline script: `type=wide` (840×350) when the slot is ≥ 860px wide, else `tall` (288×490); `iframe=true&newtab=false` keeps booking on the page. `/it/` pages use `lang=it-IT` (supported; the widget renders in Italian).
14. **`build-it.py` does not translate image `alt` text or the OpenTable `lang`.** Both were set by hand in `src/it/` (Italian alts on `it/index.html`, `it/our-story/`, `it/reservation/`). After a rebuild, re-apply them or teach the script a `data-alt-it` attribute. No python/node on Priyanka's machine; local loop there is `tools/serve.ps1` (port 8765) + headless Chrome with `--force-prefers-reduced-motion`.
16. **After Dark is a teaser until it relaunches.** `/after-dark/` and `/it/after-dark/` say something is coming, never what (no hours, pours or dates), then point to the wine list ("While you wait" → contact). The nav link carries `data-soon` (hover preview) and `data-soon-tag` (overlay tag) on every page. `/menu/after-dark/` and `/drinks/` redirect (302) to `/after-dark/`; the menu hub's After Dark card is now "La Cantina". To relaunch: rebuild the page, drop the two data attributes with one regex, remove the redirects.
15. **Phone header (< 1024px)** hides Reserve and centres the logo (`amami-header.css`).

## 4. Architecture, briefly

- `src/_assets/amami.css` — tokens (`--ink`, `--cream`, `--accent` face), base type.
- `amami-header.css` / `amami-footer.css` — shared chrome. Footer: `.ftr__wrap{width:81.226vw}`, six `.ftr__grid` squares, four `.ftr__cols`, `.ftr__bar`.
- `amami-home.css` — homepage only (`body.is-home`): hero crossfade (`.hm-hero__img--1..4`), two-line word swap (`@keyframes hm-word-swap`), `.hm-ad` Explore/Menu slideshow (5 slides, grayscale), `.hm-split`, `.hm-close`, home motion block.
- `amami-pages.css` — the inner-page kit (`body.is-page`): `.pg-hero`, `.pg-sec`, `.pg-cards`/`.pg-card`, `.pg-split`(`--bleed`,`--flip`), `.pg-tiles`, `.pg-facts`, `.pg-form`, `.pg-contact`, `.pg-map{filter:grayscale(1)}`, `.pg-btn`(`--red`,`--fill`), motion block.
- `amami.js` — nav overlay; **hours status** (`[data-hours-status]`, EN/IT strings, split days); forms (`data-amami-form`, `MSG.en/it` chosen from `<html lang>`, honeypot `company_website`, mailto fallback when `data-endpoint` is empty); **§4 motion** IIFE (adds `body.motion`, IO threshold .2 → `.is-in` once, `.is-scrolled` when `scrollingElement.scrollTop > 24`, `.pg-hero.is-ready`; skipped under `prefers-reduced-motion`).
- `amami-i18n.js` — legacy in-place EN/IT swap. Returns immediately when `<html data-lang>` is present (every page now), so it is effectively dormant. Safe to leave.
- Homepage inline script — hides the header (`body.hdr-hidden`) until pointer move / scroll; pauses the team-walk video under reduced motion.
- Language: `<html lang="en-CA" data-lang="en">` / `lang="it-IT" data-lang="it"`. CSS keyed on `[data-lang="it"]` (e.g. hero line sizes). `hreflang` en-CA / it / x-default in `<head>` of the 14 pages and as `xhtml:link` in `sitemap.xml`.
- SEO: unique `<title>` + description per page naming Brampton; OG/Twitter image (`/_assets/share/*.jpg`, 1200×630) + alt; `Restaurant` JSON-LD on `/` and `/it/`. **Canonical/OG host is still `https://amami-italia.vercel.app`** everywhere (pre-existing) — switch in one regex pass when the production domain is decided.

## 5. Local loop

```bash
git clone https://github.com/theetherealagency/Amami-Italia.git && cd Amami-Italia
python3 tools/serve.py 8791 src            # http://localhost:8791 — no caching, ever
# edit src/… ; if you touched one of the seven EN pages:
(cd src && python3 ../tools/build-it.py)   # regenerates src/it/** + sitemap alternates
cd tools && npm i puppeteer-core && node verify.js http://localhost:8791 ./shots && cd ..
git add -A && git commit && git push origin main
# then confirm live, e.g.
curl -s https://amamiitalia.etherealpr.com/it/menu/ | grep -o '<title>[^<]*'
```

Image variants (WebP + width srcset) were generated with `sharp` (Node): widths 480/800/1200/1600/2400 + native, written next to the original as `<name>-<w>w.webp` / `.jpg`. If you add a photo, generate the same set and wrap it:
`<picture><source type="image/webp" srcset="…-480w.webp 480w, …"><img src="….jpg" srcset="…" sizes="(max-width:760px) 88vw, 40vw" width height loading="lazy" decoding="async" alt></picture>`.

## 6. Open items — what to do when the answer arrives

| Item | Where | Action on answer |
|---|---|---|
| Fri/Sat closing hour | all pages | Set `"fri": [12, 23]`-style in `data-hours` (regex all `*.html`), add `"closes"` to the Fri/Sat JSON-LD entry, change footer `12PM–late` (+ `data-it`) and the contact page; remove `TODO(hours)`; rebuild `/it/`. |
| Chef credit (§7.1) | `src/our-story/index.html` | Adjust copy + `data-it`; remove TODO; rebuild `/it/`. |
| Lounge hours (§7.2), wine policy (§7.3) | `src/after-dark/index.html` | Add the confirmed sentence(s) with `data-it`; remove TODOs; rebuild. |
| Group size (§7.4) | `src/index.html`, `src/reservation/index.html` | Currently "eight or more by phone" in both; change both (+ `data-it`, + meta description on /reservation) if the client picks six/18%. |
| "Mandy's Signature Salad" (§7.5) | `src/menu/dining/index.html`, `src/food-menu/index.html` | Flagged only. Remove the dish *only* on the owner's explicit instruction. |
| Geo coordinates | `src/index.html`, `src/it/index.html` JSON-LD | Add `"geo": {"@type":"GeoCoordinates","latitude":…,"longitude":…}` from the Google Business Profile. Nominatim only returns street-level points — do not use them. |
| Instagram feed | footer, all pages | **Built.** `src/api/instagram.js` (Vercel function, hourly edge cache) + the last block of `amami.js` swap the six `.ftr__grid` stills for the six newest posts, each linked to its post; images relay through `/api/instagram/?img=` (CDN hosts allowlisted). It goes live the moment a token is set in Vercel → Project → Settings → Environment Variables, then redeploy: `IG_TOKEN` = an Instagram-Login token (IGAA…, 60 days), **or** `IG_TOKEN` = a Meta system-user token (EAA…, never expires) + `IG_USER_ID` = the Instagram business account id. Check with `GET /api/instagram/` (`source:"graph"`, six posts). Without a token it tries Instagram's public feed, which answers 429 as of 2026-09, and the stills stay. |
| Facebook URL | footer `.ftr__bar` | Add the link next to Instagram once supplied (`TODO(facebook)`). |
| Canonical host | every page + sitemap | One regex: `https://amami-italia.vercel.app` → production domain. |
| Forward Serif licence | `amami.css` | Only if a commercial licence is bought: add `@font-face`, switch `--accent`, re-measure the full-bleed headline ratios in `design-system.md`. |

## 7. Things that were tried and rejected (don't redo them)

- Client-side-only Italian (in-place `data-it` swap at the EN URL) — replaced by static `/it/` pages for SEO and consistency.
- VP9 alpha WebM for the team-walk film — alpha was dropped by the encoder; the illustration ships as an opaque MP4 (`team-walk-1s.mp4`, 1.0 s loop) over a matching poster.
- Blanket `body.is-home main > section{padding:0}` — out-specificed section paddings; each section sets its own.
- `.hm-split__img{height:100%}` — breaks aspect ratio; it is `height:auto`.
- Stagger via `transition-delay` on `.is-in > :nth-child(n)` — children have no transition, it only delayed hover states; removed.

## 8. Contacts / accounts touched

- Srishti Kundnani — skundnani@etherealpr.com (owner of this build; ask her for the master brief and the Vercel token).
- Anna — ajohny@etherealpr.com (fonts on the Drive; an *unsent* Gmail draft to her about the Forward Serif licence exists in Srishti's account).
- Instagram: @amamiitalia_official. Phone 905-794-3366. Address 6261 Mayfield Rd #140, Brampton ON L6P 0X9.
