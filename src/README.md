# Amami Italia — amamiitalia.com

Static build of the Amami Italia restaurant site, deployed on Vercel.

## What this is

The original site runs on WordPress (theme `rolanda` + `rolanda-child`, Elementor,
Contact Form 7, Yoast) on SiteGround, backed by MySQL. That stack needs PHP 8.2 and a
MySQL 8.4 server, neither of which Vercel runs.

This repository is the **rendered output** of that site — the finished HTML, CSS, JS and
media that a visitor actually receives — captured from the live site and rewritten so
every internal link resolves locally. Visually and structurally it is the same site, but
it is served as static files, so it loads considerably faster and has no database,
no PHP, and no plugin surface to patch.

## Structure

```
index.html                  homepage
<page-slug>/index.html      one directory per page, matching the live URLs
wp-content/uploads/         media library
wp-content/plugins|themes/  CSS + JS assets referenced by the pages
wp-includes/                WordPress core JS/CSS the pages depend on
vercel.json                 routing, caching, redirects
```

URLs are identical to the live site (`/about-us/`, `/dining-menu/`, …), so existing
links, search rankings and the redirect map all continue to line up.

## Live integrations

| Feature | How it works here | Status |
| --- | --- | --- |
| Table reservations | OpenTable widget + `restref` form (`rid=1470808`) | Fully working — external service |
| Contact form | Contact Form 7, submitted by AJAX to `https://amamiitalia.com/wp-json/contact-form-7/v1/…` | Working — see caveat below |
| Instagram / social | Embedded external widgets | Fully working |
| Google Tag Manager | Inline script | Fully working |

### Contact form caveat

The contact form still posts to the WordPress REST API on `amamiitalia.com`, which
returns permissive CORS headers, so submissions succeed from this domain.

**This depends on the WordPress install staying online.** If `amamiitalia.com` is ever
pointed at this Vercel project, that endpoint disappears and the form must be replaced
with a serverless handler (e.g. a Vercel Function emailing via Resend) before cutover.
Reservations are unaffected — they never touch WordPress.

## Updating content

There is no CMS here. To refresh a page after it changes in WordPress, re-run the
capture for that URL and re-run the link normalizer, or edit the HTML directly.

## Local preview

```sh
npx serve .
```
