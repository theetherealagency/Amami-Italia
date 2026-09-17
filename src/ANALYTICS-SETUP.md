# Amami Italia — Tracking Setup

New GTM container: **GTM-MNHMB7C9**

---

## 1. Live site state (verified 2026-08-21, after install)

Tags reach the live WordPress site through the **Tracking Code Manager v2.5.0
(IntellyWP)** plugin — not the theme.

| Tag | ID | Where |
|---|---|---|
| Google Tag Manager | `GTM-MNHMB7C9` | TCM → HEAD (script) + BODY (noscript) |
| GA4 gtag.js | `G-6M7M54NGTF` | TCM → HEAD, **hardcoded** |
| Ahrefs verification | — | TCM → HEAD |
| Restaurant schema (JSON-LD) | — | TCM → HEAD |

The old container `GTM-P5SKMJV7` has been **fully removed** — zero references remain.
Good: no double-container problem.

> **Still one double-count risk.** GA4 `G-6M7M54NGTF` is hardcoded in Tracking Code
> Manager. Do **not** also add a GA4 Configuration tag for `G-6M7M54NGTF` inside
> `GTM-MNHMB7C9` — you'd count every pageview twice. Either leave GA4 hardcoded and use
> GTM for events only, or move GA4 into GTM *and* delete the hardcoded gtag from TCM.

> **Note:** the GA4 property changed from `G-7H5DR4RWX3` to `G-6M7M54NGTF` at some point
> after 2026-08-17. The static rebuild in this repo still carries the old
> `G-7H5DR4RWX3` on all 34 pages and needs updating before that site goes anywhere.

## 2. Installing GTM-MNHMB7C9 on the live WordPress site

You don't need to edit the theme. Use the plugin that's already there.

1. Log in to `amamiitalia.com/wp-admin`.
2. Go to **Settings → Tracking Code Manager** (sometimes under its own
   "Tracking Code Manager" menu item).
3. **Add new tracking code** → name it `GTM-MNHMB7C9 head`.
   Position: **HEAD** (as high as possible). Paste:

```html
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-MNHMB7C9');</script>
<!-- End Google Tag Manager -->
```

4. **Add new tracking code** again → name it `GTM-MNHMB7C9 body`.
   Position: **BODY**. Paste:

```html
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-MNHMB7C9"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
```

5. Set both to load on **all pages**, save, then hard-refresh the site and confirm
   with the GTM preview / Tag Assistant.

Note: Tracking Code Manager's "BODY" placement may land near the closing `</body>`
rather than immediately after the opening tag. That's fine — the `noscript` iframe
only serves visitors with JavaScript disabled, which is a rounding error in traffic.
If you want it exactly after `<body>`, it has to go in `rolanda-child/header.php`.

### If the plugin is ever removed
Add to `wp-content/themes/rolanda-child/functions.php` instead:

```php
add_action( 'wp_head', function () { ?>
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-MNHMB7C9');</script>
<!-- End Google Tag Manager -->
<?php }, 1 );

add_action( 'wp_body_open', function () { ?>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-MNHMB7C9"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
<?php }, 1 );
```

Use the **child** theme (`rolanda-child`), never `rolanda` — a parent theme update
would wipe it.

---

## 3. Static rebuild (this repo) — already done

`GTM-MNHMB7C9` is installed on **all 34 HTML pages** in this repo: the head snippet
immediately after `<head>`, the noscript immediately after `<body>`. Nothing further
to do here; it deploys with the site.

---

## 4. Tracking "everything" — the event layer

GTM on its own only gives you pageviews. Actual interactions come from
`analytics/gtm-event-tracking.html` in this repo.

**Install it in GTM, not in the page files.** That way it covers the WordPress site
and the static rebuild from one place, and changing it never means editing WordPress.

1. GTM → **Tags → New → Custom HTML**
2. Paste the entire contents of `analytics/gtm-event-tracking.html`
3. Trigger: **Initialization — All Pages**
4. Name: `Site — interaction tracking`
5. Save → Preview → Publish

### Events it pushes to `dataLayer`

| Event | When | Parameters |
|---|---|---|
| `reservation_click` | any OpenTable link clicked | `link_url`, `link_text`, `link_location`, `booking_provider` |
| `phone_click` | `tel:` link clicked | `phone_number`, `link_text`, `link_location` |
| `email_click` | `mailto:` link clicked | `email_address`, `link_text`, `link_location` |
| `social_click` | Instagram / Facebook / TikTok / X | `social_network`, `link_url`, `link_location` |
| `outbound_click` | any other off-domain link | `link_url`, `link_domain`, `link_text`, `link_location` |
| `file_download` | pdf / jpg / png / doc link | `file_url`, `file_extension`, `link_text` |
| `menu_item_save` | "Save X to your list" on `/drinks/` | `item_name`, `saved`, `page_path` |
| `menu_item_add` | "Add X to your order" on `/drinks/` | `item_name`, `page_path` |
| `carousel_nav` | wine carousel prev/next | `direction`, `carousel_name`, `page_path` |
| `form_submit` | any form submitted | `form_name`, `form_id`, `page_path` |
| `form_submit_success` | Contact Form 7 mail actually sent | `form_name`, `form_id`, `page_path` |
| `form_error` | CF7 validation or mail failure | `form_name`, `error_type`, `page_path` |
| `scroll_depth` | 25 / 50 / 75 / 90 % | `percent_scrolled`, `page_path` |
| `engaged_visit` | 15s on page | `page_path` |

`form_name` resolves to: `catering_enquiry`, `newsletter_signup`, `customer_feedback`,
`blog_comment`, `contact_form`, `opentable_widget`.

### Wiring these into GA4

For each event you care about:
1. **Triggers → New → Custom Event**, event name = the name from the table above.
2. **Variables → New → Data Layer Variable** for each parameter you want
   (e.g. `link_text`, `item_name`, `percent_scrolled`).
3. **Tags → New → GA4 Event**, event name = same, add the parameters, attach the trigger.
4. In GA4: **Admin → Custom definitions** → register each parameter as a custom
   dimension, or it won't show up in reports.
5. Mark `reservation_click`, `phone_click`, and `form_submit_success` as
   **key events** (conversions) in GA4.

---

## 5. Known gaps

- **The phone number is mostly not clickable.** `905-794-3366` appears as plain text
  **68 times** across the site but only **2** of those are real `tel:` links. Every
  plain-text instance is an untracked call and an untappable number on mobile. Worth
  fixing in the theme/Elementor content — it's a conversion problem, not just a
  tracking one.
- **OpenTable is a separate domain.** `reservation_click` records the click; whether
  the booking completed happens on `opentable.ca` and GA4 can't see it. For real
  booking numbers you need OpenTable's own reporting, or their GA integration.
- The two embedded OpenTable widget forms open in a new tab (`target="_blank"`);
  they're caught as `form_submit` with `form_name: opentable_widget`.
- No Meta pixel, Microsoft Clarity, or Google Ads conversion tag is on the site.
  Add them as tags inside `GTM-MNHMB7C9` if you want them.

---

## 6. Troubleshooting: "I installed it but it's not working"

### SiteGround cache — this is almost always the cause

SiteGround serves an NGINX **Dynamic Cache** in front of WordPress. Response headers
show it:

```
x-cache-enabled: True
x-proxy-cache-info: DT:1
```

A cached copy of the HTML keeps being served to visitors *after* you change a tag, so
the site looks untouched. Confirmed on 2026-08-21:

| Request | GTM container in HTML |
|---|---|
| `https://amamiitalia.com/` | `GTM-P5SKMJV7` (stale cached copy) |
| `https://amamiitalia.com/?cachebust=99123` | `GTM-MNHMB7C9` ✅ |

Same page, same moment. The install was correct the whole time — only the cache was old.

**Resolved 2026-08-21 without a purge.** SiteGround's Dynamic Cache has a TTL and
expired on its own a short while later. Re-checked across `/`, `/menu/`, `/contact-us/`
and `/book-a-table/` — every page now serves `GTM-MNHMB7C9` + `G-6M7M54NGTF` with zero
references to the old container. Nothing needed clearing.

**If a future tag change looks stuck and you can't reach Site Tools:**
- **Just wait.** Dynamic Cache expires by itself — that's what happened here.
- **Save any page in `wp-admin`.** A content update triggers an automatic purge; opening
  a page and hitting Update with no changes is usually enough.
- **SG Optimizer plugin**, if installed: `wp-admin` → SG Optimizer → Caching → Purge SG
  Cache. Needs only WordPress admin, not the hosting panel.
- **Site Tools** (needs the hosting login, which may sit with the client):
  Speed → Caching → Dynamic Cache → flush.
- Verify with `?cachebust=123` rather than guessing — a cache-busted URL always shows
  the true HTML.

### Other things that look like "not working"

- **Container never published.** A brand-new GTM container with no published version
  loads but fires nothing. In GTM, top right → **Submit → Publish**. Until you do,
  Preview mode works but the live site records nothing.
- **No tags inside the container.** GTM itself is only a loader. An empty container is
  correctly installed and still sends zero data to GA4. You need at least a GA4
  Configuration tag (or the events from section 4).
- **Looking in the wrong GA4 report.** Realtime shows data in seconds; standard reports
  lag up to 24–48h. Judge by **Realtime**, not by Acquisition on day one.
- **Ad/tracking blockers.** uBlock, Brave shields, and Safari ITP block
  `googletagmanager.com` outright. Test in a clean Chrome profile with extensions off.
- **Tag Assistant is the real diagnostic.** GTM → **Preview**, enter the site URL, and
  watch tags fire per interaction. If a tag shows "Not fired", the trigger is wrong —
  not the install.

---

## 7. Importable container: `analytics/GTM-MNHMB7C9-container-import.json`

Full-coverage GTM container — **37 tags, 35 triggers, 35 variables**. Import and publish;
nothing to build by hand.

| | Contents |
|---|---|
| **Tags (37)** | GA4 Configuration (Google Tag) · interaction-tracking Custom HTML tag · 35 GA4 Event tags |
| **Triggers (35)** | One Custom Event trigger per dataLayer event |
| **Variables (35)** | 34 Data Layer Variables + a constant holding the GA4 Measurement ID |

### Everything it tracks

**Conversions**
`reservation_click` (OpenTable) · `phone_click` · `email_click` · `form_submit_success`

**Clicks & navigation**
`cta_click` (theme `.qodef-button`, with style variant) · `nav_click` (header / mobile /
dropdown) · `breadcrumb_click` · `back_to_top_click` · `mobile_menu_toggle` ·
`outbound_click` · `social_click` · `share_click` (Facebook / Twitter / LinkedIn popups) ·
`file_download`

**Content engagement**
`menu_item_save` · `menu_item_add` · `carousel_nav` (wine list + Swiper) ·
`lightbox_open` (Magnific / gallery) · `accordion_toggle` · `section_view`
(IntersectionObserver) · `map_engagement` (Google Maps iframe) · `video_start` ·
`video_complete`

**Forms — full funnel**
`form_start` (first field focus) → `form_submit` → `form_submit_success` / `form_error`.
Named forms: `catering_enquiry`, `newsletter_signup`, `customer_feedback`,
`blog_comment`, `contact_form`, `opentable_widget`.

**Attention**
`scroll_depth` (25/50/75/90) · `engaged_visit` (15s) · `time_on_page` (30/60/120/180s) ·
`exit_intent` · `text_copy` · `print_page`

**Site health & UX**
`rage_click` (3+ clicks on one element inside a second) · `js_error` ·
`page_not_found` (404 with referrer) · `web_vitals` (LCP, CLS, INP)

Every handler is keyed to markup verified on this site — theme button/nav classes, the
`.wn-ico` wine buttons, `.qodef-share-link` popups, the footer Maps iframe, Contact
Form 7's own AJAX events. No speculative selectors.

### > Do this first, or you will double-count every pageview

The container includes a **GA4 Configuration tag for `G-6M7M54NGTF`** — and that exact
same GA4 ID is currently **hardcoded in Tracking Code Manager**. Leave both and GA4
loads twice on every page: doubled users, doubled sessions, wrecked history.

Pick one, before or immediately after importing:

- **Recommended — GTM owns GA4.** In `wp-admin` → Tracking Code Manager, delete the
  `gtag.js` snippet for `G-6M7M54NGTF` from the HEAD entry. Leave the GTM head/body
  snippets alone. GA4 then loads only from the container.
- **Or — TCM keeps GA4.** Leave Tracking Code Manager as is and **delete the
  "GA4 - Configuration (Google Tag)" tag** from GTM after importing. The event tags
  still work; they carry their own Measurement ID.

### Import steps

1. GTM → container `GTM-MNHMB7C9` → **Admin → Import Container**
2. Choose the JSON file
3. Workspace: **Existing** (or a new one — easy to discard if you dislike it)
4. Import option:
   - **Merge → Rename conflicting tags/triggers/variables** if the container already has
     anything in it. Safest — it can't overwrite your work.
   - **Overwrite** only if the container is completely empty.
5. Review the preview summary, then **Confirm**
6. **Preview** and click through the site — a reservation link, the phone number, a form
7. **Submit → Publish**

### After importing

- The Measurement ID lives in one place: the **`CONST - GA4 Measurement ID`** variable.
  Change GA4 property later and you edit that single variable, not 36 tags.
- Open one GA4 Event tag and confirm the **Measurement ID** field populated. If it looks
  empty, pick `{{CONST - GA4 Measurement ID}}` from the variable picker — GTM
  occasionally reshuffles this field between versions.
- In **GA4 → Admin → Custom definitions**, register the parameters you want in reports
  (`link_text`, `item_name`, `form_name`, `percent_scrolled`, `cta_style`, `lcp_ms`, …).
  Unregistered parameters are collected but never appear in reports. GA4 allows 50
  event-scoped custom dimensions — register the ones you'll actually read, not all 34.
- Mark `reservation_click`, `phone_click`, and `form_submit_success` as **key events**.
- Account and container IDs in the file are placeholders (`0`); GTM remaps them on
  import. Expected, not a problem.

### Volume note

`rage_click`, `text_copy`, `js_error`, `time_on_page` and `scroll_depth` are chatty. GA4
caps free properties at 10M events/month — nowhere near a risk at restaurant traffic
levels, but if you ever see quota warnings, pause those five tags first. They're
diagnostics, not conversions.
