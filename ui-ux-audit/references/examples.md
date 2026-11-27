# Worked Examples

These anchor the finding format, the use of registry codes and the report shape. Match their structure; never
copy their content.

## One finding per severity

```
**B1 [focus-missing] Keyboard focus is invisible on every control** (`styles.css:4`; all 23 focusable elements)
**Found:** `*:focus { outline: none }` with no `:focus-visible` replacement; uicheck: no visible change on 23 of 23.
**Why:** Keyboard users cannot see where they are, so the dashboard cannot be used without a mouse.
**Fix:** Delete the reset and add `:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px }`.
```
(Blocker because it affects every control; on some controls only it would be Critical.)

```
**C1 [page-overflow] The page scrolls sideways on phones** (`.logo-strip`, 520px fixed width; 360)
**Found:** At 360px the document is 520px wide (uicheck: overflow 160px, widest element `.logo-strip`).
**Why:** Every phone visitor gets a page that slides sideways on the first screen.
**Fix:** `.logo-strip { width: 100%; flex-wrap: wrap; justify-content: center; gap: var(--sp-4) }`.
```

```
**C2 [card-rows] Plan buttons sit at three heights** (`.plan` cards, 3 of 3; 1280)
**Found:** "Choose plan" buttons start at 854, 957 and 1058px (uicheck card-rows, spread 204px): feature lists
differ in length and nothing pins the footer.
**Why:** Buyers compare plans across the row; a ragged button line slows the comparison and looks broken.
**Fix:** `.plans { display: grid; grid-template-rows: auto auto 1fr auto }` and
`.plan { display: grid; grid-row: span 4; grid-template-rows: subgrid }`.
```
(`card-rows` is Warning by default; Critical here because the part is the button buyers compare.)

```
**W1 [tile-baseline] Tile values sit on two lines** (`.tile`, row of four; 1280)
**Found:** "Timed slots over 90% full" wraps, pushing its value 20px below the other three (uicheck).
**Why:** A row of values is read as one line; the dropped value looks like an error.
**Fix:** Reserve two label lines (`.tile dt { min-height: 2lh }`) or use subgrid rows across the tiles.
```

```
**P1 [widow]** h1 at 1280 ends with "plan" alone; two h2s at 360. Fix: `h1, h2, h3 { text-wrap: balance }` and `&nbsp;` before the last word of the h1.
```

All ten pale labels on a page are one `contrast-text` finding that lists them; six charts without axis titles
are one `chart-labels` finding. Never one finding per occurrence.

## Report header

```
# UI audit: operations dashboard
**Score:** 100 − (1×12) − (3×8) − (4×4) − min(5, 2) = 46/100
**Verdict:** Do not ship
**Profile:** SaaS / dashboard. **Style:** Quiet product
**Checked:** uicheck run 7c1e40ab at 360/768/1280, light; 6 screenshots viewed; walk of 18 controls; Liberation Sans stood in for Inter
**Visual quality:** Inconsistent: radius-drift and gutter-drift are both present
**Top 3:** B1 restore visible focus; C1 make the period selector change the figures; C2 add sign and arrow to every change
```

## Task walk

```
## Task walk
| Task | Completed | Steps | Hesitations |
|---|---|---|---|
| See what needs attention this morning | Yes | 1 | 1: four equal tiles, none dominant (W3) |
| Compare this week with last week | No: the period selector changes captions only (C1) | 2 | 1 |
| Reach Jobs with the keyboard | Yes | 4 tab stops | 1: focus cannot be seen (B1) |
```

## Visual quality section, landing page

```
## Visual quality
Generic template: three tells (centred gradient hero; three identical icon cards; an uppercase label above
every section). See W4.

**W4 [visual-generic] The page could belong to any product** (whole page)
**Found:** Three template tells; nothing on the first screen is specific to a data-freshness product.
**Why:** A visitor comparing five tools cannot tell this one apart, so the brand does no work.
**Fix:** 1. Replace the hero illustration with the product's lineage view: a stale table turning amber, then
red, with the alert that fires. 2. Set the headline at 56px with tight tracking over 17px body text.
3. Make "How it works" a full-width three-step strip with real screenshots.
```

## Wiring line (static pages)

```
## Wiring to confirm
Export CSV, pagination and the five navigation links (href="#") have no handlers; confirm they are wired before launch.
```
(The newsletter form on the same page shows "Subscribed" without sending anything: that is not wiring but
`false-feedback`, a scored finding, because the message is untrue as displayed.)

## Quick review

User pastes one button and says "something feels off":

```
Two issues; the worse is a layout jump on hover.

**W1 [other] The button grows 2px on hover** (`.btn:hover { border: 2px solid }`)
**Found:** The border exists only on hover, so the button and its row shift.
**Why:** Movement on hover reads as a glitch.
**Fix:** `border: 2px solid transparent` by default; change only the colour on hover.

**P1 [other]** "Submit" names the mechanism, not the outcome. Fix: "Subscribe".

Spacing, contrast and focus otherwise check out. Not seen: the form it sits in.
```
