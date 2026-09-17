# Amami Italia — Keywords & Traffic Sources

Two different questions, two different tools. GA4 answers one of them and cannot
answer the other.

| Question | Tool | Status |
|---|---|---|
| What did people **search** to find us? | Google Search Console | Domain already verified — needs access + GA4 link |
| **How** did they arrive (channel, referrer, campaign)? | GA4 Acquisition reports | Live now via the GA4 tag |
| What did they search **on our site**? | GA4 site search | Not possible — the site has no search box |

---

## 1. Keywords: GA4 will never show them

Google encrypted organic search queries in 2011. In GA4 every organic visit collapses
to `google / organic` with the keyword stripped — the old "(not provided)". No tag, no
container, no configuration brings it back. **Search Console is the only source of real
search queries**, and it reports on impressions and clicks in search, not on sessions.

### Good news — the domain is already verified

`amamiitalia.com` has **two `google-site-verification` DNS TXT records**:

```
google-site-verification=5L0ZlvrHh-yOWG05hWyFCyJHcDPtEbyr5OymHvza4_A
google-site-verification=JtOc5TUMnYC52_z8MsoJErQ5giAHo6B3RKILNGDE71E
```

Two tokens means two separate Google accounts verified this domain at some point —
likely the previous agency plus someone else. Search Console has therefore been
**collecting data all along**, including historical keyword data you can look at
immediately. The question is only whether your account can open it.

1. Go to [search.google.com/search-console](https://search.google.com/search-console)
   signed in as `mgilani@etherealpr.com` and see if the property is listed.
2. If it isn't, ask whoever holds it to add you: Settings → Users and permissions →
   Add user → **Full** permission.
3. **If nobody knows who owns those tokens**, verify it yourself — you don't need DNS
   access, because you now control the GTM container:
   Add property → **URL prefix** → `https://amamiitalia.com/` → choose
   **Google Tag Manager** as the verification method. GSC checks for `GTM-MNHMB7C9`
   on the page, which is already there. Works as long as you have Publish rights on
   that container.

> Verifying a new property starts its data collection from that day forward for *your*
> view, but Search Console backfills up to 16 months of history once verified. You
> won't be starting from zero.

### Where the keywords live once you're in

- **Performance → Search results** → *Queries* tab. Every search term that produced an
  impression, with clicks, CTR and average position.
- Filter by **Page** to see which queries drive which page — e.g. what people search
  before landing on `/catering-services/`.
- **Search type: Image / Video** and the **Discover** tab are separate; for a restaurant
  the *Web* tab is where the value is.
- Queries with high impressions and low CTR are your title/description rewrites. High
  position but low clicks usually means the meta description isn't selling.

### Link Search Console to GA4

This puts query data inside GA4 so you can see keywords next to behaviour:

**GA4 → Admin → Product links → Search Console links → Link** → pick the property →
choose the web stream → confirm.

Then **enable the reports**, which GA4 hides by default:
**Reports → Library** → find the *Search Console* collection → **Publish**. Two reports
appear under Acquisition: *Queries* and *Google organic search traffic*.

---

## 2. How people are arriving — this already works

The GA4 tag collects acquisition data with no extra setup. **Reports → Acquisition →
Traffic acquisition**, and switch the dimension to suit:

| Dimension | Answers |
|---|---|
| Session default channel group | Organic Search / Direct / Referral / Organic Social / Email / Paid |
| Session source / medium | `google / organic`, `instagram.com / referral`, `(direct) / (none)` |
| Session campaign | Your UTM campaigns |
| Landing page | Which page they entered on |

**Realtime → by source** is the fastest way to sanity-check that any of this works.

### The gap: untagged links make good traffic look like Direct

Anything arriving without a referrer — an Instagram bio tap, a QR code, an email
signature click, a link pasted into WhatsApp — lands in GA4 as **Direct / (none)** and
becomes invisible. Fix it by tagging every link you control:

| Where the link lives | Use this URL |
|---|---|
| Google Business Profile website button | `https://amamiitalia.com/?utm_source=gbp&utm_medium=organic_local&utm_campaign=google_business_profile` |
| Instagram bio | `https://amamiitalia.com/?utm_source=instagram&utm_medium=social&utm_campaign=bio_link` |
| Instagram story / link sticker | `https://amamiitalia.com/?utm_source=instagram&utm_medium=social&utm_campaign=story` |
| Facebook page | `https://amamiitalia.com/?utm_source=facebook&utm_medium=social&utm_campaign=page_link` |
| Newsletter | `https://amamiitalia.com/?utm_source=email&utm_medium=email&utm_campaign=newsletter_2026_09` |
| Staff email signatures | `https://amamiitalia.com/?utm_source=email_signature&utm_medium=email&utm_campaign=staff` |
| OpenTable listing | `https://amamiitalia.com/?utm_source=opentable&utm_medium=referral&utm_campaign=listing` |
| In-store QR / table tent | `https://amamiitalia.com/?utm_source=qr&utm_medium=offline&utm_campaign=table_tent` |
| Printed menu / flyer | `https://amamiitalia.com/?utm_source=print&utm_medium=offline&utm_campaign=flyer` |

Rules that keep the reports clean:
- Lowercase everything. `Instagram` and `instagram` become two separate rows.
- Never UTM-tag internal links between your own pages — it restarts the session and
  destroys the original attribution.
- `utm_medium=social` maps to GA4's *Organic Social* channel; `utm_medium=email` to
  *Email*. Made-up mediums fall into *Unassigned*, so stick to the values above.

**Google Business Profile deserves its own mention.** For a Brampton restaurant it's
often the single biggest driver, and the clicks land as Direct unless tagged. GBP also
has its own built-in stats (searches, calls, direction requests) worth reading
alongside GA4 — those are people who never reach the website at all.

---

## 3. Also worth doing

- **Bing Webmaster Tools** — free, gives Bing/Copilot search queries, and imports
  directly from Search Console in a couple of clicks. Small traffic share, zero effort.
- **The site has no search box.** If you ever add one, GA4 site search reveals what
  visitors want and can't find — for a restaurant that's usually menu items, allergen
  info, and parking. Genuinely useful, and it's the one keyword source you'd fully own.
- **`robots.txt` points at `http://amamiitalia.com/sitemap_index.xml`.** It redirects to
  HTTPS and works fine, but it's worth correcting in Yoast → Settings → Site features →
  so crawlers get the canonical URL directly.
- **`reservation_click` is where these two worlds meet.** Once Search Console is linked
  and UTMs are in place, you can ask the question that matters: which channel and which
  search terms actually produce booking clicks, rather than just traffic.
