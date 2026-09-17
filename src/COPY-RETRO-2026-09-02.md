# Amami Italia — site copy, retro pass

Written 2 September 2026. Nothing here is live yet. Read it, mark it up, send it to the
client, then I put it into `tools/build_structure.py` and rebuild.

Two decisions you made that this whole document follows:

1. **Chef Isabella Comello replaces Gianluca Martinucci everywhere his name appears.**
2. **The Lucca framing stays.** "Da Lucca a Brampton", the Tuscan claim, the story page —
   all of it is untouched. Only the chef changes.

Register: family trattoria. Hand-painted sign, not a film poster. Warm, short, a bit
blunt. Contractions everywhere. No three-part lists with a nice beat at the end, no
"not this, but that", no lines that sound wise and mean nothing.

---

## Before anything gets built — five things I need from you

**1. Facts about Isabella.** There is nothing about her in the repo, the menu, or the
capture beyond one line on the printed menu: *"Crafted by Chef Isabella Comello."*
The chef page currently makes five specific factual claims and every one of them was
written about Gianluca:

- born and raised in Lucca
- learned tordelli from his mother and grandmother
- in restaurants by sixteen
- in Canada since 2014
- APCI certified

None of those move onto Isabella's name without you confirming them. Everywhere the copy
below needs one, it says `[ISABELLA: …]` in brackets. Fill them in and the page works. Leave
them and the page ships with holes in it.

**2. Who Linda is.** The printed menu also says *"made with love, by Linda, in our kitchen."*
That line is already in exactly the voice you picked. If Linda is Isabella's mother, or the
owner, or the one who actually makes the dessert, that is worth a paragraph on the story
page. If it is a leftover from an older menu, tell me and I'll drop it.

**3. Whether "Tordelli di Nonna Lia" is real.** It is on the chef page today as a signature
dish. It is not on the 2026 printed menu and not in `tools/menu_data.py`. I have replaced it
below with dishes that are actually on the menu. If the tordelli is a real thing the kitchen
makes off-menu, say so and it goes back.

**4. One line from Isabella in her own words.** Anything — why she cooks what she cooks,
what she eats on her day off, what she thinks people order wrong. One real sentence from her
beats a page of anything I write. This is the single highest-value thing you could get me.

**5. Six small facts, listed at the end of this document.** Parking count, accessibility
detail, lounge age policy, cake policy, drive times, and how gift cards are actually bought.
Each one is currently a placeholder sitting on a live page.

---

## The thing to fix first, before any of the pretty copy

Six pages are showing internal build notes to guests. These are not tone problems, they are
"the scaffolding is still up" problems, and they read worse than any wording issue:

| Page | What a guest reads today |
|---|---|
| `/visit/faq/` | "Publish every fact — these answer guests, local search and AI answer engines at the same time." |
| `/visit/faq/` | "FAQPage schema to be emitted from this list." |
| `/visit/` | "Come and find us. An invitation rather than a directory listing." |
| `/visit/contact/` | "One form, routed by subject, so nothing lands in the wrong inbox." |
| `/date-night-brampton/` and the other five landing pages | "To write." / "Publish the range." / "One action, stated plainly." |
| every unpublished menu page | "Awaiting the current list from the kitchen." |

All six are replaced below.

---

# Page by page

## `/` — Home

The home page is a stack of full-bleed panels. Each panel is one photograph, one word, one
line, one button. Then a booking block at the bottom.

### Panel 1 — the hero (video)

- **Over-line:** Welcome to
- **Word:** Amami
- **NOW:** It means love me. Tuscan cooking on Mayfield Road.
- **NEW:** It means love me. Come in, we'll feed you.
- **Button:** Reserve a Table

Alternate, if the client wants Brampton in the first line for search:
*It means love me. Tuscan cooking, Mayfield Road, Brampton.*

### Panel 2 — Dinner

- **Word:** Dinner
- **NOW:** (no line)
- **NEW:** The sauce has been on since this morning.
- **Button:** View Menus

### Panel 3 — Pizza

- **Word:** Pizza
- **NEW:** Out of the oven and straight to you. Don't let it sit.
- **Button:** View Menus

Careful here: the pizza page has no list on it. The panel can say the pizza is good, it
cannot send someone to a menu that isn't there. See `/menu/pizza/` below.

### Panel 4 — After Dark

- **Word:** After Dark
- **NEW:** The plates go away. Nobody goes home.
- **Button:** The Lounge

### Panel 5 — The Room

- **Word:** The Room
- **NEW:** Two of you or twenty of you, it's the same room.
- **Button:** Our Story

### Panel 6 — Private Dining

- **Word:** Private Dining
- **NEW:** Shut the door on twenty-two of you.
- **Button:** Enquire

### Panel 7 — Catering

- **Word:** Catering
- **NEW:** We'll bring it to you. Trays, not boxes.
- **Button:** Enquire

### Booking block (bottom of the page, `#book`)

- **NOW:** Make a Reservation
- **NEW:** Book a table
- **NOW:** Eight or more is best arranged by phone — 905-794-3366.
- **NEW:** Eight or more, just call. 905-794-3366. It's quicker than typing.

### Hours block (phones only)

- **NOW:** Hours of Operation
- **NEW:** When we're open

### Meta description (search results, link previews)

- **NOW:** Tuscan cooking in Brampton, led by Chef Gianluca Martinucci of Lucca. Dining, lounge and catering on Mayfield Road.
- **NEW:** Tuscan cooking in Brampton, from Chef Isabella Comello. Dining, lounge and catering on Mayfield Road.

---

## `/our-story/` — Da Lucca a Brampton

Lucca stays. This is the restaurant's story, not the chef's.

### Page head

- **Title:** Da Lucca a Brampton *(unchanged)*
- **NOW:** Amami means love me. It is a Tuscan kitchen on Mayfield Road, cooking the food of Lucca for Brampton, Caledon and Vaughan.
- **NEW:** Amami means love me. It's a Tuscan kitchen on Mayfield Road, cooking the way Lucca cooks.

### Block 1 — Da Lucca / Where it came from

- **NOW:** Lucca sits inside its walls in northern Tuscany. Its cooking is plainer than the Italy most people picture — bread, beans, olive oil, a short list of things done properly.
- **NEW:** Lucca is a town in Tuscany with the wall still round it. People expect Italy to be showy. Lucca isn't. It's bread and beans and good oil, and it's very good.

### Block 2 — Il Mestiere / The craft that travelled

- **NOW:** Technique arrives with a person, not from a book. Pasta is rolled here, sauces are built here, and the kitchen is run by someone who learned it where it comes from.
- **NEW:** You don't learn this out of a book. You learn it standing next to someone who already knows. The pasta gets rolled here in the morning. The sauces get started before the doors open.

The old version ended on "someone who learned it where it comes from" — that was a claim
about Gianluca. It's gone.

### Block 3 — A Brampton / The room on Mayfield Road

- **NOW:** The room seats a Tuesday dinner for two and a table of twenty on a Saturday. It is warm, it is loud when it should be, and it is ten minutes from Caledon and Vaughan.
- **NEW:** Two of you on a Tuesday or twenty on a Saturday, it's the same room. It gets loud. That isn't a fault. Caledon and Vaughan are both a short drive.

### New Block 4 — the chef

There is currently no link from the story page to the chef page, which is odd given the
chef page exists. Adding a fourth block:

- **Italian label:** La Cucina
- **Heading:** Whose kitchen it is
- **Copy:** The kitchen is Isabella's. `[ISABELLA: one sentence — how long she's been running it, or where she learned]`
- **Link:** Meet Chef Isabella

---

## `/our-story/chef/` — the chef page

This is the page that changes most. URL stays the same, which is lucky — there's no name in it.

### Everything that renames

| Where | Now | New |
|---|---|---|
| Nav label | Chef Gianluca | Chef Isabella |
| Page title (browser tab, search) | Chef Gianluca Martinucci — Amami Italia, Brampton | Chef Isabella Comello — Amami Italia, Brampton |
| Display heading | Le Mani di Gianluca | Le Mani di Isabella |
| Eyebrow | Chef Gianluca | Chef Isabella |
| Meta description | Born in Lucca, APCI certified, in Canada since 2014. | `[ISABELLA: needs a real one-liner]` |

### Hero

- **Eyebrow:** Chef Isabella
- **Heading:** Le Mani di Isabella
- **NOW:** Gianluca's hands. Ties the chef directly to the craft.
- **NEW:** Everything that leaves that kitchen went through her hands first.

The old sub-line — "Ties the chef directly to the craft" — was a note to the designer about
why the heading was chosen. It has been sitting on the live page as body copy.

### Section — who she is

- **NOW (all of it about Gianluca, all of it removed):** Born and raised in Lucca. Learned tordelli from his mother and grandmother. In restaurants by sixteen. In Canada since 2014. APCI certified.

- **NEW, once you fill the brackets:**

  > She's been cooking since she was `[ISABELLA: age]`. She learned it from `[ISABELLA: who]`,
  > in `[ISABELLA: where]`, and she's been running this kitchen since `[ISABELLA: year]`.
  > Ask her what's good tonight and she'll tell you what she'd eat herself.

- **NEW, if you get nothing at all** — this version claims nothing and still reads:

  > Ask her what's good tonight and she'll tell you what she'd eat herself. That's usually
  > the right answer.

- **Heading for the section:** currently "Born in Lucca". That claim goes with Gianluca.
  Use **"In the kitchen"** until you know where she's from. If she is from Lucca, say so and
  the old heading comes straight back — it's the better one.

### Section — Signatures

Three cards. All three currently name dishes; only one of them is on the menu.

| Now | On the 2026 menu? | New |
|---|---|---|
| Tordelli di Nonna Lia — "The family recipe." | No. Not in the printed menu or `menu_data.py`. | Replaced — see below, unless you tell me it's real |
| Bistecca alla Fiorentina — "45-day dry-aged, on the bone." | Yes, $190/kg | Kept, reworded |
| Wild boar ragù — "Tuscan, slow, unfashionable, correct." | No. Nowhere on the menu. | Replaced |

Replacements, all real, all priced on the current menu:

- **Bistecca alla Fiorentina** — T-bone, aged forty-five days, sold by the kilo. Order it for the table, not for yourself.
- **Gnocchi al Pesto** — Potato gnocchi, basil pesto, pine nuts, stracciatella on top. The one people come back for.
- **Agnello alla Griglia** — Lamb chops, rosemary and lemon, straight off the grill.

"The one people come back for" is a claim about the gnocchi. If the kitchen would rather
that sat on a different dish, move it — but one of the three should carry it, because a list
of three dishes with no opinion in it is just a menu again.

### If you get a quote from her

Put it here, between the bio and the signatures, big, in the serif, with her name under it.
One real sentence from Isabella is worth more than this entire page.

---

## `/menu/` — A Tavola (the menu hub)

### Top band

- **Eyebrow:** Menu
- **Title:** A Tavola *(unchanged)*

### Editorial paragraph

- **NOW:** These pages are built and named. The kitchen and the bar are still sending the current lists, and they go up as text the day they arrive.
- **NEW:** Seven lists. Two of them are up. The other five go up the day the kitchen hands them over.

Guests do not need to know what "built and named" means. They need to know why five links
lead to empty pages, which the new line tells them in one sentence.

### The two published menus

**Dining door**

- **NOW:** Antipasti through dolci. Gnocchi al pesto, saffron risotto, lamb chops, and the tomahawk and fiorentina, both aged 45 days and cut by the kilo.
- **NEW:** Starters through dessert, thirty-two dishes. The tomahawk and the fiorentina are aged forty-five days and sold by the kilo, so bring somebody with you.
- **Fact line:** 32 dishes · 12pm until close

**After Dark door**

- **NOW:** What the bar works from once the plates go away. Tawny port, a long row of amari, grappa, and coffee with something in it.
- **NEW:** What the bar pours once the plates are gone. Port, amari, grappa. Coffee with something in it.
- **Fact line:** 43 pours · port, amaro, grappa, caffè

### The five that aren't printed yet

- **Section heading:** The other five lists *(unchanged)*
- **NOW:** These pages are built and named. The kitchen and the bar are still sending the current lists…
- **NEW:** Not up yet. Call and we'll tell you what's on.
- **Label on each:** "List to come" → **"Not up yet"**

Short blurbs, unchanged except for tightening:

- Pizza — Neapolitan, out of the oven.
- Wine — Tuscany first, then the rest of Italy.
- Cocktails — The aperitivo hour and whatever else the bar's got.
- Tasting — Isabella's own run of dishes. Needs notice.
- Catering — Trays, pasta and mains, out the door.

### Closing line

- **NOW:** Book the table first — the menu will still be here.
- **NEW:** Book the table first. The menu isn't going anywhere.

---

## The seven menu pages

Each one has an eyebrow, an Italian heading, and a one-line lede. Only the lede changes.

| URL | Heading | Now | New |
|---|---|---|---|
| `/menu/dining/` | Pranzo e Cena | Lunch and dinner. | Lunch and dinner, from noon until we close. |
| `/menu/pizza/` | Dal Forno | From the oven. | From the oven. Ask us what's on tonight. |
| `/menu/after-dark/` | Dopo Cena | After dinner. | After dinner. Stay where you are. |
| `/menu/wine/` | La Cantina | The cellar. | The cellar. Tuscany first, then the rest of Italy. |
| `/menu/cocktails/` | Aperitivi & Cocktails | Aperitivo, and what to drink before dinner. | Aperitivo, and whatever else you want from the bar. |
| `/menu/tasting/` | Degustazione | The tasting. | Isabella's own run of dishes. Give us notice. |
| `/menu/catering/` | Fuori Casa | Away from home. | Away from home. Trays, pasta and mains, out the door. |

### The placeholder that sits on five of them

- **NOW:** Dish names, one-line descriptions and prices as HTML text. Awaiting the current list from the kitchen.
- **NEW:** This list isn't up yet. Call 905-794-3366 and we'll read it to you.

That is a build note with a job number in it, currently facing customers on five pages.

### Foot of every menu page

- **NOW:** Ready to book?
- **NEW:** Hungry yet?

The two legend notes are contractual and stay word for word: *Automatic gratuity of 18%
applies to parties of six or more.* / *Maximum of three separate checks per table, split evenly.*

---

## `/after-dark/` — Raise the Bar

The client wrote "Raise the Bar" themselves, so it stays.

### Hero

- **Label:** After Dark
- **Heading:** Raise the Bar *(client's, unchanged)*
- **Marquee strip:** From 10pm ★ The lounge ★ Port, amaro, grappa ★ Music *(unchanged — the star strip is the most retro thing on the site already)*
- **Buttons:** Reserve a Table / See the list

### Big type panel

- **NOW & NEW:** The room doesn't empty at ten

Leave it. It's the best line on the site.

### Dark card

- **NOW:** Dinner service turns over and the room stays open. Forty-three pours after the plates go away — tawny port, a long row of amari, grappa, and coffee with something in it. The counter takes twelve. The lounge takes sixty standing, thirty seated. Come for one, stay for the room.
- **NEW:**
  > Dinner turns over and nobody makes you leave. Forty-three things to drink once the
  > plates are gone — port, amari, grappa, and coffee with something in it.
  >
  > Twelve seats at the counter. Sixty standing in the lounge, thirty if you're sitting.
  > Come in for one and see how it goes.

### The two rooms

- **The Lounge** — *NOW:* Cocktails, small plates and music once dinner service turns over.
  **NEW:** Once dinner turns over, this is where it carries on. Music up, plates smaller.
  *Capacity: standing 60 · seated 30*
- **The Bar** — *NOW:* The aperitivo hour, and where the signatures are made.
  **NEW:** Twelve seats, no reservation. Sit here if you're early, or on your own.
  *Capacity: 12 at the bar*

### Closing band

- **NOW:** Planning a night for a group, or taking the room for the evening? Tell us the date and how many.
- **NEW:** Taking the room for a night? Send us the date and the number.

---

## `/events/` — Group Booking & Private Events

### Title card

- **Heading:** Group Booking & Private Events *(unchanged)*
- **Sub:** 8+ Guests & Private Events *(unchanged)*
- **Buttons:** Event Enquiry / See the Menus

### First paragraph

- **NOW:** A corporate table, a birthday, a wedding lunch or the whole room for an evening — the private room seats twenty-two, the long table thirty, and the building holds a hundred and twenty when you take all of it.
- **NEW:** A birthday, a work dinner, a wedding lunch, or the whole building. The private room seats twenty-two. The long table down the middle takes thirty. Take everything and it holds a hundred and twenty.

### Second paragraph

- **NOW:** For groups of eight or more, or a private event, write to info@amamiitalia.com or call 905-794-3366.
- **NEW:** Eight or more, or anything private — call 905-794-3366, or write to info@amamiitalia.com.

### Capacity row

Unchanged. The four columns (Full Buyout 120 standing, Private Room 16–22 seated, Long Table
24–30 seated, Lounge 30 seated / 60 standing) are real published numbers and shouldn't be
touched without the client changing them.

### Dress code

- **NOW:** Semi formal for evening service. Collared shirts, dress trousers or an elegant dress.
- **NEW:** Evenings are semi formal. Collared shirt and trousers, or a dress.

This is the client's own rule, so the edit is only to shorten it. Confirm before changing
the meaning at all.

### Enquiry form

- **Eyebrow:** Event enquiry
- **NOW:** Tell us what you are planning
- **NEW:** Tell us what you're planning
- **NOW:** Date, headcount and which room, and we will come back to you with what is free and a per-head price.
- **NEW:** Give us the date, how many, and which room. We'll come back with what's free and a price per head.
- **Button:** Send enquiry
- **NOW:** We reply within one business day.
- **NEW:** We answer within a business day.

---

## `/catering/` — Amami Fuori Casa

### Hero

- **Eyebrow:** Catering
- **Heading:** Amami Fuori Casa *(unchanged)*
- **NOW:** Amami, away from home.
- **NEW:** The same kitchen, at your place.

### Drop-off

- **NOW:** Trays and platters delivered, set out by you.
- **NEW:** We cook it, you set it out. Trays and platters, delivered.
- *Capacity: 10–100*

### Full service

- **NOW:** Our team, on site, start to finish.
- **NEW:** Our people come with the food and stay until it's cleared.
- *Capacity: 20–200*

### Enquiry form

Same wording as the events form, with "Catering enquiry" as the eyebrow.

---

## `/visit/` — Vieni a Trovarci

### Page head

- **NOW:** Come and find us. An invitation rather than a directory listing.
- **NEW:** Come and find us. Mayfield Road, top end of Brampton.

"An invitation rather than a directory listing" is a note from the architecture document
about what the page should feel like. It's been printed on the page instead.

### Hours

Table unchanged — Monday closed, Tuesday to Thursday 12pm–10pm, Friday and Saturday
12pm–11pm, Sunday 12pm–9pm.

### Three cards

- **Parking** — *NOW:* Free on-site parking. Count and accessible bays to confirm.
  **NEW:** Free parking, right outside. `[CONFIRM: how many bays, and how many accessible]`
- **Accessibility** — *NOW:* Step-free entry, accessible washroom. Details to confirm.
  **NEW:** Step-free in, accessible washroom. `[CONFIRM: anything else worth saying]`
- **Getting here** — *NOW:* Mayfield Road at Brampton's northern edge; minutes from Caledon, Bolton and Vaughan.
  **NEW:** We're on Mayfield at the top of Brampton. Caledon, Bolton and Vaughan are all a short drive.

---

## `/visit/faq/` — Buono a Sapersi

### Page head

- **NOW:** Good to know. Publish every fact — these answer guests, local search and AI answer engines at the same time.
- **NEW:** Things people ask us.

The second half of that sentence is an SEO instruction from the build spec. It is live, in
body copy, on the FAQ page. This is the single worst line on the site.

### The six questions

| Question | Now | New |
|---|---|---|
| Do you take reservations? | Yes — OpenTable, and by phone. | Yes. Book online or call. Walk in and we'll do what we can. |
| Is there parking? | Free on-site parking. | Free, on site. |
| Can you handle allergies? | Yes. Tell us when you book and again at the table. | Yes. Tell us when you book, and tell your server again when you sit down. |
| Do you have a tasting menu? | Degustazione, with a notice period — see the menu page. | Yes, the degustazione. It needs notice, so call and ask. |
| Is the lounge age-restricted? | Policy to confirm and publish here. | `[CONFIRM — this is a placeholder facing customers]` |
| Can we book the whole room? | Yes — private dining and full buyouts. | Yes. A hundred and twenty when you take all of it. |

### Also delete

"FAQPage schema to be emitted from this list." is printed under the questions. It's a
to-do for me, not a sentence for a guest.

---

## `/visit/contact/` — Scrivici

- **NOW:** Write to us. One form, routed by subject, so nothing lands in the wrong inbox.
- **NEW:** Write to us. Pick what it's about and it goes to the right person.
- **Form labels:** unchanged
- **Button:** Send

The location card above the footer is unchanged.

---

## `/reservation/` — Prenota

This page is the restored 2026-08-20 one with the OpenTable booking flow embedded, so its
copy lives in the HTML rather than the generator. Changes are small.

- **Heading:** Reserve a table *(unchanged)*
- **NOW:** Tell us when.
- **NEW:** Tell us when, and how many.
- **"Before you come" notes** — rewrite as:
  - Eight or more, call us instead. 905-794-3366.
  - Gratuity of 18% on parties of six or more.
  - Allergies: tell us here, and tell your server again at the table.
  - `[CONFIRM: how long a table is held if you're late]`

---

## `/gift-cards/` — Regala Amami

- **NOW:** Give Amami.
- **NEW:** Give somebody dinner.
- **Punchy alternate for the panel or a card:** Hard to wrap. Easy to spend.
- **The widget box** currently says "Gift card purchase widget — provider not yet chosen."
  Until one is: **Ask for one at the front, or call 905-794-3366.** `[CONFIRM: is that true?]`

---

## `/journal/` — Il Quaderno

- **NOW:** The notebook.
- **NEW:** Notes. Some about food, some about Brampton.

The four posts listed are from the old WordPress site. Worth checking they still say
something the new site would want to stand behind.

---

## `/careers/` — Lavora con Noi

- **NOW:** Work with us.
- **NEW:** If you can cook, or carry four plates without looking at them, come and talk to us.

`[CONFIRM: are they actually hiring?]` If not, the honest version is: **Nothing open right
now. Leave your name anyway.**

---

## `/press/` — Si Parla di Noi

- **Heading and lede:** People are talking about us. *(unchanged — already the right voice)*
- The three cards say "Logos and links to add", "Images, bio, fact sheet — to assemble" and
  a media email. Until there's real coverage, cut the first two cards and leave the email.
  An empty press page with one working address beats three cards admitting they're empty.

---

## The three occasion pages

All three currently show three cards reading **"To write."**, **"Publish the range."** and
**"One action, stated plainly."** Those are briefs to the copywriter, live on the page.

### `/date-night-brampton/` — Una Sera per Due

- **NOW:** An evening for two.
- **NEW:** An evening for two, and nobody rushing you.
- **Heading:** Dinner, then the lounge *(unchanged)*
- **NOW:** What the evening actually looks like, from arrival to the last drink.
- **NEW:** Get a booth, order the burrata, take your time over the pasta. When they clear the plates you don't have to go anywhere — the lounge is the same room, later.
- **Cards:**
  - What to expect → Low light, a booth if we've got one, and no one hurrying you out.
  - What it costs → `[CONFIRM: two courses and a glass each, roughly $X]`
  - How to book → Online, or call 905-794-3366.

### `/corporate-dining-brampton/` — Cene di Lavoro

- **NOW:** Working dinners.
- **NEW:** Dinner where people can hear each other.
- **Heading:** A room that can hold a conversation *(unchanged — it's good)*
- **NOW:** Capacities, set menus and the notice period, stated plainly.
- **NEW:** The private room takes sixteen to twenty-two with the door shut. Set menus if you want the bill known before anyone orders. Give us a few days and it's easier on everybody.
- **Cards:**
  - What to expect → A door that closes. Sixteen to twenty-two seated.
  - What it costs → `[CONFIRM: set menu price per head]`
  - How to book → Event enquiry form, or call 905-794-3366.

### `/celebrations-brampton/` — Le Feste

- **NOW:** The celebrations.
- **NEW:** Get everyone in one room.
- **Heading:** Bring everyone *(unchanged)*
- **NOW:** Group sizes, cake policy, timings and what a celebration here includes.
- **NEW:** Birthdays, anniversaries, christenings, whatever it is. Twenty-two in the private room, thirty down the long table, a hundred and twenty if you take the building.
- **Cards:**
  - What to expect → The private room, the long table, or all of it.
  - Cake → `[CONFIRM: can people bring their own, and is there a fee?]`
  - How to book → Event enquiry form, or call 905-794-3366.

---

## The three catchment pages

Same problem — the body copy is a brief. All three need one real fact each: the drive.

### `/italian-restaurant-caledon/` — Da Caledon

- **NOW:** From Caledon. / Minutes from Caledon / Where we are relative to Caledon, drive time and parking.
- **NEW lede:** Down the hill from Caledon.
- **NEW body:** We're on Mayfield, so from most of Caledon it's `[CONFIRM: X]` minutes. Park outside, free.

### `/italian-restaurant-bolton/` — Da Bolton

- **NEW lede:** A short run from Bolton.
- **NEW body:** `[CONFIRM: X]` minutes down `[CONFIRM: which road]`. Free parking when you get here.

### `/italian-restaurant-vaughan/` — Da Vaughan

- **NEW lede:** Worth the drive from Vaughan and Woodbridge.
- **NEW body:** `[CONFIRM: X]` minutes west along Mayfield. Free parking, and you won't be circling for it.

I'm not inventing drive times. Three real numbers from Google Maps at 7pm on a Friday is a
five-minute job and it's the only thing on these pages a local actually wants to know.

---

## `/404/` — Ti Sei Perso?

- **NOW:** Lost? Here are the three places people usually want.
- **NEW:** Lost? It happens. Here's the menu, a table, and how to find us.

---

## `/legal/` and the six policy pages

- **NOW:** This policy is being finalised. For anything urgent, call or email us and we will answer directly.
- **NEW:** This one's still being written. If you need an answer now, call 905-794-3366 or write to info@amamiitalia.com.

---

## Site furniture

### Footer

- **Newsletter label:** Join the Amami table *(unchanged — it's already the right voice)*
- **Button:** Sign up *(unchanged)*
- **Tagline under the logo:** Tuscan restaurant, lounge & catering in Brampton. *(unchanged — this one has a job to do for search)*

### Buttons across the site

| Now | Keep or change |
|---|---|
| Reserve a Table | Keep |
| Reserve now (phone header) | Keep |
| View Menus | Keep |
| Event Enquiry | Keep |
| Catering Enquiry | Keep |
| Get Directions | Keep |
| Read the menu | Keep |
| See the list | Keep |

Buttons are the one place not to get clever. "Reserve a Table" is clear in a way that
"Grab a seat" isn't, and the whole booking funnel is measured on those clicks.

---

# Punchy lines, for wherever you need them

Signage, Instagram, the panel headings, a print ad. Not all of these belong on the site.

- Come in, we'll feed you.
- The sauce has been on since this morning.
- The room doesn't empty at ten.
- Two of you or twenty of you, it's the same room.
- Ask her what's good tonight and she'll tell you what she'd eat herself.
- Sold by the kilo, so bring somebody.
- Nobody's rushing you.
- Sit down. Bread's coming.
- The plates go away. Nobody goes home.
- Loud on a Saturday, and that's the point.
- Shut the door on twenty-two of you.
- Hard to wrap. Easy to spend.
- Twelve seats at the counter, no reservation.
- Tuesday is a good night to eat properly.
- It means love me. That's the whole idea.

---

# The list of facts I still need

| # | What | Where it's blocking |
|---|---|---|
| 1 | Isabella — age started, who taught her, where, how long at Amami | `/our-story/chef/`, `/our-story/`, home meta |
| 2 | One sentence from Isabella in her own words | `/our-story/chef/` |
| 3 | Who Linda is | `/our-story/`, possibly the chef page |
| 4 | Is "Tordelli di Nonna Lia" a real dish here | `/our-story/chef/` |
| 5 | Parking bay count + accessible bays | `/visit/` |
| 6 | Lounge age policy | `/visit/faq/` |
| 7 | Cake policy for celebrations | `/celebrations-brampton/` |
| 8 | Drive times from Caledon, Bolton, Vaughan | the three catchment pages |
| 9 | How gift cards are actually bought today | `/gift-cards/` |
| 10 | Are they hiring | `/careers/` |
| 11 | Date-night and corporate price ranges | two landing pages |
| 12 | How long a late table is held | `/reservation/` |

---

# What it costs to ship this

Two things worth knowing before you approve it:

**The Italian translation is keyed on the exact English string.** `tools/i18n_it.py` holds
404 entries, each one matched against the English word for word. Every line changed above
needs its Italian entry rewritten or the site falls back to English on that line. That's the
real work in this pass — probably longer than the English rewrite itself.

**Two pages don't run through the generator.** `/reservation/` is the restored 2026-08-20
page and `/events/` was until recently. Their copy is patched, not generated, so their
changes are done by hand and have to be checked separately after a rebuild.
