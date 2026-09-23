# Amami Italia — Design System

Extracted from the homepage (`src/index.html` + `src/_assets/amami-home.css`), which is
the locked source of truth. Every other page is rebuilt to match this.

Kept at the repo root, not in `src/`, so it is not served.

---

## 0. The one idea you need

The homepage is **a 1366px-wide artboard, scaled**. It is not a set of breakpoints with
hand-picked sizes. Every length is *the comp's own pixel value divided by 1366*, written
as `vw`:

```
comp measurement 96.04px  ->  96.04 / 1366  =  7.031vw
```

So the whole page is one drawing that grows and shrinks together, and proportions hold at
any width. `max()` wraps a value only to put a **floor** under it for phones:

```css
padding-top: max(30px, 7.031vw);   /* 7.031vw above ~427px wide, 30px below */
```

**Never** use `max()` as a ceiling, and never introduce a fixed px size for anything that
scales. If you need a new measurement, take it from the comp and divide by 1366. If the
comp has no opinion, copy the nearest existing value rather than inventing one.

Two full-bleed lines are sized so the text spans **exactly 100vw** for their exact string.
Change the words and you must recompute the `vw`. See §3.

---

## 1. Stylesheets, and what governs what

| file | scope | notes |
|---|---|---|
| `_assets/amami.css` | site-wide tokens, shared components | 818 lines. `:root` palette, `.btn`, `.wrap`, `.eyebrow`, `.lede`, per-page blocks |
| `_assets/amami-home.css` | homepage only | loaded by `/` only. Owns everything prefixed `.hm-` |
| `_assets/amami-header.css` | header + nav overlay + mobile bar | self-contained, declares its own `--h-*` tokens |
| `_assets/amami-footer.css` | footer | self-contained, declares its own `--f-*` tokens |

Header and footer deliberately **do not read `:root`**. They carry their own tokens so they
can be dropped onto a page that never loads `amami.css` (the restored `/reservation/`)
without restyling that page's body. Preserve that property.

`amami.css` gives every `<section>` block padding. Each homepage section clears it by
setting its own `padding` shorthand — do the same on new sections rather than editing
`amami.css`.

---

## 2. Colour

### Brand book palette (AMAMI BRAND BOOK, p.12) — the source of truth since 2026-09-23

| brand name | value | token(s) on the site | used for |
|---|---|---|---|
| Charcoal Black | `#161616` | `--hm-panel`, `--f-ink` | dark panels, type on cream |
| Warm Beige | `#eee9da` | `--hm-cream`, `--f-cream` | the ground, type on dark |
| Mist Blue | `#cbd6e3` | `--hm-silver`, `--h-bronze-lit` | titles and icons on dark panels; header/nav hover and active states |
| Tuscan Brown | `#462e24` | `--h-cocoa`, `--cocoa` | the header's Reserve button |
| Medium Rare Red | `#812b28` | `--hm-red`, `--f-red` | the red band, type and buttons on cream |

The site had drifted to `#77312c` / `#ede9dc` / `#cdd6e2` (the SVG's values) and used
gold `#ca9d75` for hovers; all four were snapped to the brand book on 2026-09-23 (the gold
became Mist Blue — the token is still named `--h-bronze-lit`). The red band's Tuscan
drawing is an opaque JPEG with the red baked in: it was re-tinted and renamed
`home-band-tuscany-812b28.jpg`. **If the red ever changes again, re-tint that image too.**

### Homepage palette (on `body.is-home`)

| token | value | used for |
|---|---|---|
| `--hm-cream` | `#eee9da` | the artboard ground, and type on dark |
| `--hm-red` | `#812b28` | the band, and type on cream |
| `--hm-panel` | `#161616` | the two split panels |
| `--hm-silver` | `#cbd6e3` | split-panel titles and the line icons |
| `--hm-scrim` | `#080809` | both photographic gradients |

### Site-wide palette (`amami.css :root`)

```
--cocoa      #462e24    --bronze      #a87a41    --ink        #0b0908
--cocoa-deep #33211a    --bronze-lit  #ca9d75    --ink-soft   #141110
--cocoa-lit  #5d3f31    --cream       #fdf8f4    --stone      #433e37
--warm       #433e37    --cream-warm  #f7efe6    --line       rgba(253,248,244,.16)
--warm-deep  #2a2621
```

`--cocoa` is a **brown**, not a maroon — it was changed from `#812b28` on 2026-09-01
because the client did not want red. The homepage's `#77312c` is local to
`amami-home.css` for that reason. Do not promote it into `:root`, and do not use
`--cocoa` on the homepage.

No gradients other than the two photographic scrims. No drop shadows. No rounded corners
anywhere — `border-radius: 0` is the house default.

---

## 3. Type

Three faces, and only these three.

```css
--serif:  'Cormorant Garamond', Georgia, 'Times New Roman', serif;   /* titles */
--sans:   'Poppins', 'Helvetica Neue', system-ui, sans-serif;        /* body, buttons */
--accent: 'Forward Serif', 'Poppins', ...;                           /* accent lines */
```

Loaded from Google Fonts: Cormorant Garamond 300/400/500 + italic 400, Poppins
300/400/500/600. **Forward Serif is not on Google Fonts and no file has been supplied**,
so `--accent` currently falls back to Poppins. Anywhere `--accent` is used will change
appearance the day that font is dropped in — that is intended.

### The scale, as built

| role | comp px | size | family / weight | tracking | line-height | colour |
|---|---:|---|---|---|---|---|
| Hero word (full-bleed) | 146.73 | `10.8vw` | serif 300 | `-.05em` | 1 | cream |
| Band headline (full-bleed) | 104.39 | `7.63vw` | serif 300 | `-.05em` | 1 | cream |
| Section title (The Room) | 78.52 | `max(30px,5.748vw)` | serif 300 | `-.05em` | 1 | red |
| Panel title (split blocks) | 47.39 | `max(22px,3.469vw)` | serif 300 | `-.05em` | .94 | silver |
| After Dark words | 50.52 | `max(18px,3.698vw)` | sans 300 | `.2em` | 1 | cream |
| Closing heading | 31.47 | `max(20px,2.304vw)` | accent 400 | — | 1.2 | cream |
| Body lede | 17.51 | `max(11px,1.282vw)` | sans 400 | — | 1.2 | cream |
| Hero claim | 15.58 | `max(8.5px,1.14vw)` | sans 400 | `.2em` | 2.057 | cream |
| Room sub | 15.48 | `max(11.5px,1.133vw)` | accent 400 | — | 1.5 | panel |
| Button label | 15.85 | `max(9.5px,1.16vw)` | sans 300 | `.2em` | — | per colourway |

All titles are `text-transform: uppercase`. Ledes and subs are sentence case.

### Type positions are set from measured baselines

Cormorant Garamond's advance widths match the comp's to a tenth of a pixel. Positions were
derived by measuring where the baseline actually falls, not by guessing leading. Example —
the hero word's baseline must sit on the hero's bottom edge; with `line-height:1` the
baseline falls `.818em` down the box and the comp wants it at `1.013em`, hence:

```css
transform: translateY(.195em);
```

If you change a title's size or face, re-measure rather than nudging by eye.

### The two full-bleed lines

Their `vw` is derived from the string's own width-to-size ratio, so the line lands exactly
edge to edge:

```
font-size = 100vw / (rendered width ÷ font size)
```

`WELCOME TO AMAMI` measures 9.256× its font size, so `100/9.256 = 10.8vw`.
`DINNER LOOKS BETTER IN RED.` measures 13.1×, so `100/13.1 = 7.63vw`.

**Changing either string requires recomputing its `vw`**, or the line will no longer reach
the edges (or will overflow). Measure the replacement in the browser at a known font size,
divide, and set the new value. `white-space: nowrap` + `text-align: center` means any
residual overflow spills symmetrically.

---

## 4. Vertical rhythm

All from the comp, as `vw`. This is the page's cadence — reuse these numbers on new
sections rather than picking round ones.

| gap | comp px | value |
|---|---:|---|
| Section top padding (The Room) | 96.04 | `max(30px,7.031vw)` |
| Section bottom padding (The Room) | 95.04 | `max(34px,6.958vw)` |
| Title → sub | 3.83 | `max(3px,.28vw)` |
| Sub → image | 19.27 | `max(16px,1.411vw)` |
| Image → action | 41.68 | `max(22px,3.051vw)` |
| Band top padding | 34.98 | `max(18px,2.561vw)` |
| Band headline → action | 48.51 | `max(20px,3.551vw)` |
| Action → After Dark | 84.86 | `max(30px,6.212vw)` |
| → Private Dining block | 125.77 | `max(40px,9.207vw)` |
| → Catering block | 64.22 | `max(24px,4.701vw)` |
| → Closing section | 155.94 | `max(44px,11.416vw)` |
| Panel padding (top / sides / bottom) | 52.73 / 30 / 68.79 | `max(20px,3.861vw)` / `max(12px,2.196vw)` / `max(26px,5.036vw)` |

Panels distribute their three items with `justify-content: space-between` — the comp's
even spacing falls out of that automatically for both the two-line and one-line titles.

---

## 5. Widths and grid

| element | comp px | value |
|---|---:|---|
| Artboard | 1366 | — |
| Hero height | 762.2 | `max(520px,55.797vw)` |
| Band painted height | 729.42 | `53.398vw` |
| Closing min-height | 736.48 | `53.913vw` |
| Room illustration | 960 | `70.278vw` |
| Split block | 1109.55 | `81.226vw`, columns `51.7% / 48.3%` |
| After Dark figure | 444.9 | `32.57vw` |
| Page gutter (hero row) | 84 | `max(14px,6.142vw)` |
| Page gutter (room, band, closing) | — | `max(14px,4vw)` |
| Footer / shared wrap | — | `max-width:1240px`, padding `clamp(20px,5vw,64px)` |

The split block mirrors by swapping the column ratio (`.hm-split--flip`), not by reordering
markup on desktop.

---

## 6. Components

### Buttons

The comp has no button as such: **a 1px rule, a wide-tracked label, nothing else.** One
rule, two colourways.

```css
.hm-btn {
  min-width: max(112px, 12.027vw);      /* 164.29 comp */
  height:    max(36px, 3.226vw);        /* 44.07 comp  */
  padding-inline: max(9px, .886vw);
  border: 1px solid #fff;               /* white on photography */
  font-size: max(9.5px, 1.16vw);
  letter-spacing: .2em;
  text-indent: .2em;                    /* puts back what tracking steals on the right */
  text-transform: uppercase;
}
.hm-btn--red { border-color: var(--hm-red); color: var(--hm-red); }  /* on cream */
```

Hover fills with the border colour and inverts the label. No scaling, no shadow, no radius.
`text-indent` is load-bearing — without it the label sits optically left.

The band's action is the one oversized variant: `min-width max(180px,24.599vw)`,
`height max(38px,3.704vw)`, `font-size max(10px,1.332vw)`.

**Button labels are fixed by the design** and sized to their containers: `BOOK A TABLE`,
`TAKE A LOOK AT THE MENU`, `OUR STORY`, `ENQUIRE`.

### Headings

Title, optional sub, optional image, one action — in that order, centred. That is the
whole vocabulary. There is no eyebrow/kicker on the homepage; `amami.css` defines
`.eyebrow` for other pages but the homepage does not use it.

### Split block (photograph + panel)

The pattern behind Private Dining and Catering, and the one to reuse for any
"image beside a statement" need:

- one grid, `51.7% / 48.3%`, `81.226vw` wide, centred
- photograph sets the row height via `aspect-ratio: 573.5/605.18`; the panel stretches
- panel is `--hm-panel`, centred, `space-between`, holding: lede → (icon + title) → action
- mirrored by flipping the column ratio

### Line icons

Drawn assets, not a font: `amami-icon-cloche.svg` (`max(38px,5.214vw)`),
`amami-icon-chair.svg` (`max(31px,4.241vw)`), `amami-mark-gold.svg`
(`max(48px,7.03vw)`). Extracted from the comp's own vectors. Icon sits `max(12px,1.7vw)`
above its title.

---

## 7. Image treatment

- **Everything is `object-fit: cover`** with an explicit `width`/`height` on the tag.
- **No filters, no duotone, no overlay tints.** The only darkening is the two scrims.
- **Hero scrim** — the comp's gradient exactly: nothing until 40.6% down, then to solid
  `#080809` at the bottom edge. This is what lets cream type sit on a white tablecloth.
  ```css
  linear-gradient(to bottom, rgba(8,9,9,0) 40.6%, var(--hm-scrim) 100%)
  ```
- **Closing scrim** — the same gradient inverted: solid at the top edge, gone by 61.4%.
- **Hero** is a four-photograph crossfade: each holds 4.8s, dissolves over 1.2s, 24s total.
  Slide 1 carries a negative delay so it is at full opacity on load. Composed pictures get
  an `object-position` that keeps their subject in frame when a narrow viewport crops.
- **Ratios in use:** hero `2400×1339` (the banner's own 1366:762.2), split `573.5/605.18`,
  After Dark `1532/2036`, room film `16/9`.
- Hero image is preloaded and `fetchpriority="high"`; everything else is `loading="lazy"`
  and `fetchpriority="low"`.

### Cache rule — important

`vercel.json` serves `/wp-content/uploads/*` with
`Cache-Control: public, max-age=31536000, immutable`. **Overwriting an asset at the same
path does nothing for anyone who already loaded the page.** Always ship a changed asset
under a new filename (`team-walk-1s.mp4`, `-v2`, a hash) and update the references.

---

## 8. Header

Fixed, full width, 76px tall, `z-index: 60`.

```css
background: rgba(11,9,8,.86);
backdrop-filter: blur(10px);
border-bottom: 1px solid rgba(253,248,244,.16);
```

It is **translucent dark at all scroll positions** — it does not currently transition from
transparent over the hero. (§4 of the brief asks for that behaviour; it is a change, not a
preservation.)

- Logo centred, 34px tall.
- Inline nav appears at `min-width: 1024px`; below that it collapses to a burger that opens
  a full-screen overlay (`z-index: 80`, 350ms opacity/visibility).
- Overlay goes two-column at `min-width: 900px` (`1.15fr / .85fr`).
- Hours status appears at `min-width: 1024px`.
- A fixed four-item quick-action bar sits at the bottom below `1024px`; `body` gets
  `padding-bottom: 64px` to clear it.
- Nav links: `.8125rem`, `.12em` tracking, uppercase, `opacity .86` → 1 on hover with
  `--h-bronze-lit`.

---

## 9. Footer

Three rows, not four columns: brand + newsletter, the facts, legal.
`max-width: 1240px`, padding `clamp(20px,5vw,64px)`, background `#141110`, hairline top
border. Newsletter label is `.62rem` / `.2em` / uppercase / bronze. Inputs and buttons are
square, transparent, hairline-bordered; the button inverts to bronze on hover.

Links are `color: inherit`, no underline, → `--f-bronze-lit` on hover.

---

## 10. Breakpoints

| width | what happens |
|---|---|
| `≤ 760px` | Homepage collapses: split blocks stack (`1fr`, `min(88vw,520px)`, photo → `4/3`); After Dark words leave the photograph and sit above it in a flex row; band headline is allowed to wrap (`max-width:14ch`) and the band's painted height becomes `auto`; hero row becomes one centred column; **gold mark is hidden** (at 48px it is a smudge); room illustration goes to `92vw` |
| `≥ 761px` | After Dark words are absolutely placed on the photograph (`display:contents` on their wrapper) |
| `≥ 900px` | Nav overlay becomes two columns |
| `≤ 1023px` | Mobile quick-action bar visible, `body` padded for it |
| `≥ 1024px` | Header inline nav + hours visible, burger hidden, mobile bar hidden |

The `≤760px` block is the one place the homepage departs from the comp — the artboard is a
desktop drawing and has nothing to say about phones. Treat it as interpretation, and keep
new mobile work in the same spirit: stack, don't shrink; drop ornament rather than
compress it.

---

## 11. Motion

Currently only two things move, both on the homepage:

- Hero crossfade, 24s linear infinite.
- The Room film: a 1s MP4 on loop, the team walking on the spot. Poster is the opening
  frame so the section looks like the original drawing before it plays.

`@media (prefers-reduced-motion: reduce)` disables the crossfade (holding slide 1) and
stops the film. **Any motion added must honour this**, and must animate `transform` and
`opacity` only — nothing that shifts layout.

---

## 12. Rules for building a new page

1. **Compose from the patterns above.** Section title + sub + action; split block; full-bleed
   photograph with a scrim; black panel. If a page needs something the homepage has no
   pattern for, the answer is almost always a simpler arrangement of these, not a new
   component.
2. **Take measurements from the comp**, divided by 1366. Don't invent round numbers.
3. **Don't add** a type size, a button style, a section padding or a colour that isn't in
   this document.
4. **Character counts matter.** The type was set around specific line lengths. A heading
   that runs materially longer will rewrap and break the composition — and for the two
   full-bleed lines it breaks the edge-to-edge fit outright.
5. **Restraint is the brief.** Large type, wide margins, few elements per screen. No
   gradients, no shadows, no rounded cards. When in doubt, remove something.
