# Worked Examples

These anchor the finding format, severity judgement and report shape. Match their structure; never
copy their content.

## One finding per severity

```
**B1. Keyboard focus is invisible everywhere** (`styles.css:4`, all 23 focusable elements)
**Found:** `*:focus { outline: none }` with no `:focus-visible` replacement; uicheck reports focus
invisible on every focusable element at 1280px.
**Why:** Keyboard users cannot see where they are, so the dashboard is unusable without a mouse (WCAG 2.4.7).
**Fix:** Delete the reset and add `:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px }`.
**Prevent:** A CI grep that fails on `outline: none` without a `:focus-visible` rule (axe-core does not catch this).
```

```
**C1. The page scrolls sideways on phones** (`.logo-strip`, 520px fixed width)
**Found:** At 360px the document is 520px wide (uicheck overflow 160px); the whole page pans sideways.
**Why:** Every phone visitor gets a broken, wobbling page on the first screen.
**Fix:** `.logo-strip { width: 100%; flex-wrap: wrap; justify-content: center; gap: var(--sp-4) }`.
**Prevent:** Playwright screenshots at 360px that fail when `scrollWidth > innerWidth`.
```

```
**C2. Plan buttons sit at three heights** (`.plan` cards, 3 of 3)
**Found:** "Choose plan" buttons start at 854, 957 and 1058px at 1280 (uicheck card_rows, spread 204px)
because feature lists differ in length and nothing pins the footer.
**Why:** Buyers compare plans across the row; a ragged button line makes the table look broken and
slows the comparison.
**Fix:** Let the plan grid own the rows: `.plans { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr));
grid-template-rows: auto auto 1fr auto; gap: var(--gutter) }` and
`.plan { display: grid; grid-row: span 4; grid-template-rows: subgrid }`.
```
(Card-row misalignment defaults to Warning; this one is Critical because the misaligned element is the
primary CTA users compare.)

```
**W1. KPI values sit on two different lines** (`.tile`, row of four at 1280px)
**Found:** "Timed slots over 90% full" wraps to two lines, pushing its value 20px below the other three
(uicheck baselines, spread 20px).
**Why:** The eye reads a row of values as one line; the dropped value looks like an error.
**Fix:** Reserve two label lines (`.tile dt { min-height: 2lh }`) or use subgrid rows across the tiles.
```

```
**P1. Single words alone on heading lines** (h1 at 1280px "plan"; two h2s at 360px)
**Found:** uicheck widows: the hero headline ends with "plan" alone; "Everything accounts payable needs,
in one / place" at 360px.
**Fix:** `h1, h2, h3 { text-wrap: balance }` and `&nbsp;` between the last two words of the hero headline.
```

## Visual quality section (full audit)

```
**Visual quality:** Competent but forgettable. Clean, accessible and consistent, but nothing on the
page is specific to a data-freshness product; with another logo it could sell anything.

**W4. Visual design has no point of view** (whole page)
Moves:
1. Replace the abstract hero illustration with the product's lineage view: a stale table turning
   amber, then red, with the alert that fires. It says what the product does in one glance.
2. Set the headline at 56px with tight tracking and a balanced two-line break; keep body at 17px
   so the scale has real contrast.
3. Break the run of four identical centred sections: make "How it works" a full-width three-step
   strip with real screenshots, and the integrations a dense logo grid.
```

## Wiring line (static pages)

```
## Wiring to confirm
Export CSV, pagination, the five nav links (href="#") and the newsletter form have no handlers or
endpoints; confirm they are wired before launch (the form would be a Blocker if shipped unwired,
because it shows "Subscribed" without sending anything).
```

## Report header (condensed)

```
# UI audit: operations dashboard
**Score:** 100 − (1×12) − (3×8) − (4×4) − min(5, 2×1) = 46/100. **Verdict:** Do not ship (1 Blocker).
**Profile:** SaaS / dashboard. **Checked:** uicheck at 360/768/1280, screenshots, keyboard walk,
period selector exercised; Liberation Sans stood in for Inter.
**Visual quality:** Inconsistent: three card radii and two grey families on one screen.
**Top 3:** B1 restore focus visibility; C1 make the period selector change the figures; C2 add sign
and arrow to every delta.
```

## Quick review

User pastes one button and says "something feels off":

```
Two issues, the worse is a layout jump on hover.

**W1. The button grows 2px on hover** (`.btn:hover { border: 2px solid }`)
**Found:** The border exists only on hover, so the button and its row shift.
**Why:** Movement on hover reads as a glitch.
**Fix:** `border: 2px solid transparent` by default; change only the colour on hover.

**P1. "Submit" names the mechanism, not the outcome**
**Fix:** "Subscribe".

Spacing, contrast and focus otherwise check out.
```
