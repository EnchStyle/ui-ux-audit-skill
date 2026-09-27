---
name: ui-ux-audit
description: "Audits web UI and raises it from competent to exceptional. Catches what AI tools ship and people notice at once: broken or shifting layouts, cards and values off a shared line, orphaned words and lone grid items, drifting radii, gutters, ratios and component sizes, text overflow, missing states, poor contrast, small targets, accessibility gaps, dishonest charts and numbers, and generic AI-looking visuals. Use whenever the user asks to audit, review, check, critique, fix, polish or improve a page, screen, dashboard, report, component, screenshot or design, or says things like 'looks off', 'looks AI-generated', 'is this ready to ship', 'spacing is weird', 'cards don't line up', 'make it look high-end'. Also use when building or restyling a whole page, dashboard, analytics report or component (HTML, CSS, React, Tailwind, SVG charts) so these failures never ship; skip it for one-line edits. Includes a measuring script and profiles for landing pages, dashboards, analytics reports, e-commerce and children's apps."
---

# UI/UX Audit

Find the interface problems AI tools ship, report them with fixes (audit), or avoid them while building
(build mode), and push the visual quality from correct to exceptional.

Most AI UI failures share one cause: the model writes a plausible snapshot of one state at one width,
never sees the rendered result, and carries no design system from one component to the next. So the
page looks right in a screenshot and breaks when content grows, the viewport narrows, an error occurs,
or a second component arrives with slightly different padding. The cure is to measure the render
instead of reasoning about it, and to hold every element to one global system.

## Modes

| Mode | Triggered by | Read | Output |
|---|---|---|---|
| **Full audit** | "audit this page", "is this ready to ship", "full review" | This file, the matching profile, `references/visual-excellence.md`, `references/alignment-consistency.md`, `references/user-simulation.md`, then the category references for what the page contains (table below) | Scored report |
| **Quick review** | "why does this card look off", "check this button" | This file and the one or two references the question touches | Short answer, no score |
| **Build** | Creating or restyling a page, dashboard, report or component | This file, the matching profile, `references/visual-excellence.md` and `references/alignment-consistency.md`; the pre-flight checklist below stands in for the category references, so open those only when a question comes up | The code, then a short hand-over |

A matching profile overrides the universal defaults wherever they differ.

## Step 1: measure the render

Run the bundled script on the page before judging anything:

```
python3 <skill folder>/scripts/uicheck.py page.html --json checks.json --shots shots/
```

It needs Python Playwright with Chromium (it also accepts an http(s) URL; add `--dark` for the dark
theme, `--widths 320,360,768,1280,1440` to change widths). It renders at 360, 768 and 1280px and
measures horizontal overflow, contrast, target sizes, unnamed controls, invisible focus, unsized
media, heading order, small text, widows and wrapping button labels, lone grid items, card rows off a
shared line, tile values off a baseline, side-by-side control heights, non-concentric corners,
near-miss left edges, padding asymmetry, mixed media ratios, icon and chip size drift, gutters,
table header alignment, long tables without a sticky header, heading proximity, and a census of
radii, shadows, font sizes, families and section paddings.

- The script measures; you judge. Every item it reports is a candidate, not a finding: confirm it on
  the screenshots, decide whether it matters, and group items with one cause into one finding.
- Text over gradients or images is counted, not measured: sample the pixels behind it.
- Look at every screenshot yourself at all three widths. The script cannot see hierarchy, rhythm,
  crowding, visual weight, the idea behind the design or whether it looks exceptional.
- If the page needs a build step (TSX, Tailwind without a build), bundle it quickly (esbuild) or map
  the classes to CSS by hand, and say what stood in for what. If fonts are missing, name the stand-ins:
  line breaks, widows and wraps depend on the font, so report those as font-dependent.
- No Playwright available: read the code, reason carefully, and label measurements as estimates.
- Screenshot only: judge what a picture can show (hierarchy, contrast, spacing, alignment, copy,
  visual quality); state sizes as estimates against a named reference; never invent line numbers or
  class names; put code-dependent items under Verify; mark the score "provisional".

## Step 2: walk it as the user (full audits)

Before the category sweep, walk the main flow as the real user, a constrained user (keyboard only, or
200% zoom, or colour-blind) and an edge-case-data user (empty, long, many). Only the walk catches
contradictory states, controls that relabel without acting, and happy-path-only flows. Details in
`references/user-simulation.md`. Skip it for a single static element.

## Step 3: sweep the categories

| # | Category | Reference |
|---|---|---|
| 1 | Typography and text breaking | `structure-typography.md` |
| 2 | Layout and spacing | `structure-typography.md` |
| 3 | Visual hierarchy | `structure-typography.md` |
| 4 | Colour, contrast, dark mode | `color-states-forms.md` |
| 5 | Component states | `color-states-forms.md` |
| 6 | Forms | `color-states-forms.md` |
| 7 | Touch and interaction | `interaction-responsive-a11y.md` |
| 8 | Responsive behaviour | `interaction-responsive-a11y.md` |
| 9 | Accessibility | `interaction-responsive-a11y.md` |
| 10 | Alignment, consistency and tokens | `alignment-consistency.md` |
| 11 | Navigation and icons | `navigation-icons.md` |
| 12 | Motion | `motion-performance.md` |
| 13 | Performance and layout shift | `motion-performance.md` |
| 14 | Visual quality and distinctiveness | `visual-excellence.md` |
| 15 | Content, copy and honesty | `content-honesty.md` |
| 16 | Charts, tables, dashboards | `data-viz-tables.md` |

All references live in `references/`. A full audit covers every category the page contains; a quick
review covers the ones the question touches.

## Severity

Judge by harm to the user, never by how easy the fix is.

| Severity | Points | Meaning |
|---|---|---|
| **Blocker** | 12 | Stops a core task, deceives the user, or creates legal or accessibility exposure: content or the primary action unreachable, keyboard trap or focus removed everywhere, data loss, a dark pattern, a chart or number that misleads. |
| **Critical** | 8 | Major harm on a common path: body or CTA contrast below AA, horizontal scroll at 360px, a missing empty or error state on a primary flow, placeholder as the only label, a control with no accessible name, unsized media shifting the layout, figures that contradict each other, a control that visibly relabels without acting. |
| **Warning** | 4 | Degrades the experience: off-system spacing, cards or values off a shared line at desktop, mixed ratios or control heights, a lone grid item, duplicate CTA intent, weak hierarchy, a generic or forgettable landing page. |
| **Polish** | 1 | Refinement: widows, nested corners, near-miss edges of a few pixels, padding asymmetry, straight quotes, tone slips. |

Defaults for frequent findings (depart only with a reason tied to this page):

| Finding | Default |
|---|---|
| Focus indicator removed with no replacement, across the page | Blocker |
| Focus indicator present but below 3:1 against its surroundings | Warning |
| A control keyboard users cannot reach or operate (a clickable `div`) | Critical, on every profile |
| Keyboard order illogical but complete (an opened menu placed before its toggle) | Warning |
| Skipped heading levels | Warning |
| Icon-only control with no accessible name | Critical |
| Horizontal scroll at 360px | Critical; Blocker when content or the primary action becomes unreachable |
| Body or CTA text below 4.5:1 (3:1 for large text), including CTA labels on gradients | Critical |
| Placeholder as the only label | Critical |
| Missing empty, error or completion state on a primary flow; an empty result shown as real zeros | Critical |
| A success message that is untrue ("Copied", "Sent", "Saved" when nothing happened) | Critical (a progress message that ends with nothing is Wiring) |
| Chart axis or scale that exaggerates; figures that should agree but do not | Blocker on analytics products, Critical elsewhere |
| Chart missing its title, axis titles, units or text alternative | Warning (one finding per chart) |
| Chart series told apart only by colour, or series marks below 3:1 | Critical on analytics products, Warning elsewhere |
| Long table (more than about 15 rows) with no sticky header | Warning |
| A control whose code updates labels or captions to claim a new state while the data stays the same | Critical. A native select or button with no handler at all is Wiring to confirm |
| Target below 24 × 24px without 24px spacing (WCAG 2.5.8) | Critical on a primary control, Warning otherwise |
| Primary touch control 24 to 43px on a touch-first product | Warning |
| Images or embeds with no `width` and `height` or `aspect-ratio` | Critical, judged from the code. A local render showing no shift does not clear it: inline or cached images decode before paint, real network images do not |
| Card rows or tile values off a shared line | Warning at desktop widths; Critical when users compare the misaligned price or CTA; Polish when it happens only at phone widths |
| Plot areas of side-by-side charts at different heights | Polish |
| Lone item on the last row of a fixed set (features, plans, stats) | Warning at the main desktop and phone layouts; Polish at in-between widths; catalogues exempt |
| Drift in section padding, gutter, control height, media ratio, or between different radius systems (sharp and round) | Warning (one finding per property) |
| Small drift within one system: radii 2 to 4px apart, chip heights, icon sizes, button padding | Polish (one finding per property) |
| Navigation hidden on phones with no menu, when it holds destinations users need (sign in, pricing, a shop's categories) | Critical |
| Headline that does not say what the product does | Warning; Critical only when nothing on the first screen says what it is |
| Generic template look or forgettable design on a landing or marketing page (see Visual quality) | Warning; on dashboards, reports, shops and apps the visual verdict is advice, not scored |
| Contained scroller (nav strip, table) with no visible cue that more is hidden | Polish |
| Widows, nested corners, near-miss edges, padding asymmetry | Polish (group each kind into one finding) |

When torn between two severities, choose the lower and say why. Inflated audits get ignored.

## Scoring

**Score = 100 minus points, floored at 0.** Polish findings together deduct at most 5 points. Only
findings confirmed on the page as it is count; Verify and Wiring items are listed but not scored.
Count per severity and compute in code, then show the arithmetic:
`100 − (1×12) − (2×8) − (4×4) − min(5, 3×1) = 53/100`.

Verdicts: 90 to 100 Ready to ship; 70 to 89 Ship after fixing the top findings; 40 to 69 Significant
rework; below 40 Do not ship. Any Blocker means "Do not ship" whatever the score.

## What not to flag

These are the usual sources of noise. Leave them out of the scored findings:

- **Wiring a static page cannot have.** Links to `#`, buttons without handlers, pagination, export,
  search over data the page does not hold, forms with no endpoint. List them once, unscored, under
  **Wiring to confirm**. The exception: the page shows a result that is false (a filter that relabels
  the view but not the data, a success message after a failed copy, a count that contradicts the
  table). That is a finding.
- **Latent problems the page's own data cannot trigger** (a fixed axis that would clip a spike that
  never occurs). Put them under Verify if the data will be live; otherwise drop them. Unsized media
  is not latent: it is a confirmed finding from the code.
- **House floors that are not standards.** WCAG sets no minimum font size. 12px chart ticks, table
  headers and labels are normal in dense data UI; 13 to 15px secondary copy is fine. Flag type size
  only below 12px, or body reading copy below 16px on a reading page (Polish; Warning below 14px).
- **Targets that pass WCAG 2.5.8** through the spacing or inline exception: text links in sentences
  and link lists (footers, breadcrumbs), dense 32px controls with room around them on pointer-first
  dashboards.
- **Control boundaries a text label already identifies.** WCAG 1.4.11 asks for 3:1 on the parts
  needed to identify a control: text-field edges, checkboxes, toggles, icon-only buttons. A labelled
  select or text button does not need a 3:1 border.
- **Missing dark mode** unless the product has or promises one; **token hygiene** (raw hex, magic
  numbers) unless it causes visible drift; **meta tags, favicons, company disclosures and legal
  advice**, which belong to other reviews.
- **Deliberate, consistent choices**: a labelled zoomed axis, a contained horizontal table scroller
  with a visible cue, dense controls on a pointer-first tool, a chosen aesthetic executed well,
  documented exceptions, established domain conventions (bracketed accounting negatives, locale
  number formats, contract-month labels). If you disagree with a deliberate choice, ask under
  Questions; do not score it.
- **The same root cause twice.** One finding lists every occurrence.
- **Pure taste.** Every finding names who it hurts and how.

## Alignment and consistency: the global system

People notice at once what AI tools miss: a heading 4px off the grid below it, one card alone on the
last row, prices at three heights across a row, a 40px input beside a 48px button, an inner corner
that does not follow the outer one, a single word alone on a heading's last line. Treat the page as
one system with global settings for type scale, spacing, gutters, radii, control and chip heights,
icon sizes and media ratios, and audit every element against it. `references/alignment-consistency.md`
lists each check with its measurement, fix and severity. In build mode, write that system first (the
global block described there) and derive every component from it.

## Visual quality: raise it

Correct is not the bar; distinctive and clear is. In every full audit, rate the visual quality
(Exceptional, Distinctive with slips, Competent but forgettable, Generic template, Inconsistent) and
give two to four concrete moves grounded in this product, not a style lecture.

- **Landing and marketing pages**: the page is the brand's flagship, so "Competent but forgettable"
  and "Generic template" are scored Warning findings, with the moves written into the finding's Fix.
- **Dashboards, analytics reports, shops and apps**: clarity comes first, so the rating and moves go
  in the Visual quality section, unscored, whatever the rating. Hierarchy faults that are verifiable
  (no dominant metric, twelve equal tiles, chrome louder than the data) are ordinary findings.
- Measurable faults (section rhythm, radii, grey families, alignment) are always their own findings,
  never folded into the visual verdict.

When the project has a brand system or house template, its fonts and colours are fixed: raise
quality through hierarchy, rhythm, alignment, data-ink and copy inside it. Details and a library of
moves per page type are in `references/visual-excellence.md`.

## Finding format

Each finding has an ID (B1, C1, W1, P1 in report order) and a short title:

```
**C2. Delta direction shown by colour alone** (`#kpi-grid .delta`, 12 tiles)
**Found:** <what is wrong, with the measurement or snippet>
**Why:** <who it hurts, one line>
**Fix:** <the smallest concrete change>
**Prevent:** <tool or rule that stops the family; first finding of a family only>
```

Keep Found and Why to one or two lines. Polish items take one line each.

## Full audit report

```
# UI audit: <page>
**Score:** <arithmetic> = NN/100. **Verdict:** <band, or Do not ship if any Blocker>
**Profile:** <name or none>. **Checked:** <uicheck at 360/768/1280, screenshots, keyboard walk; stand-ins>
**Visual quality:** <rating>, <one line on why>
**Top 3:** <IDs, one line each>

## Blockers (N) / ## Critical (N) / ## Warnings (N) / ## Polish (N)
## Visual quality: <the rating and two to four concrete moves tied to this page (on landing pages the moves also sit in the finding's Fix)>
## User walk: <two to four lines the walk found that the checklist did not, citing IDs>
## Verify (N): <what the input could not confirm, each with the severity it becomes if confirmed>
## Wiring to confirm: <one line listing inert controls a static page cannot have>
## Clean: <one line naming categories checked with nothing found>
## Durable fixes: <one to three tools matched to the stack>
## Questions: <at most three, each with the assumption made>
```

Omit empty sections. About 1,200 words for one page. No preamble. For several pages, score each
separately and add a short cross-page summary; never average unrelated pages.

## Quick review

Open with one line: how many issues and the worst. Then two to five findings in severity order in the
finding format (Prevent only if one tool stops the whole family). Close with at most two lines on what
depends on code you did not see. About 400 words, no score unless asked, fixes inline.

## Build mode

1. **Art direction first.** Before any code, sketch three directions in your working notes, each
   with: the idea in one sentence (what makes the page specific to this product, data and
   audience), a type pairing and scale, a palette drawn from the subject's own world (freight:
   kraft, container rust and ink; energy: slate and signal amber) rather than default SaaS blues,
   teals and greens, one signature element, and a layout motif. Pick the most specific direction
   that stays clear; the safe option is usually the generic one, so never pick it by default.
   Test the choice against the default looks in `references/visual-excellence.md`, including the
   generic SaaS look (system sans, white rounded cards on grey, one saturated button colour,
   numbered section chips): if a stranger could not tell this page from ten other AI-built pages,
   choose again. With no web fonts, character comes from system stacks used with intent (a serif
   display stack such as `"Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif` against
   a sans body, or a condensed stack for data), a large display size with tight tracking, weight,
   colour and composition (at least one full-bleed band; not every section an equal card grid).
   The signature element is real content set large: the product's own output or the data's most
   telling view. A house template or brand system, when there is one, replaces these choices.
2. **Write the global system block** (`references/alignment-consistency.md`): type scale, spacing
   scale, gutters, radius steps, control and chip heights, icon sizes, media ratios, colour roles for
   light and dark themes, content widths. Components use only these values.
3. **Build every state and width**: loading, empty, error, disabled, long content; 360, 768, 1280
   and 1440px. Include a skip link. Dashboards and reports follow the system colour scheme with a
   light and a dark theme from the same tokens.
4. **Answer the brief, and compute every figure.** Map each question in the brief to the section
   that answers it and check it is answered visibly, also after filtering (a comparison across
   regions over time needs the regions in the trend charts). Titles, captions and summary
   sentences update with the filters. Calculate each displayed number in code from the source data,
   then recompute a sample a second way (for example in Python) and compare, including after each
   filter change. The method note must describe exactly what the code does (weighted versus simple
   means, periods, exclusions), and every section must use the same method. Never invent a figure;
   label chosen thresholds as choices.
5. **Measure and look.** Run `scripts/uicheck.py`, then look at every screenshot. Fix until overflow,
   contrast, unnamed controls, invisible focus, unsized media, heading skips, card rows, baselines,
   control heights, nested radii, grid orphans and heading widows are all zero, and the census shows
   at most three radius steps (plus pills and circles) and two shadow levels. Re-run after every fix.
6. **Judge your own page cold.** Look at the 1280 and 360 screenshots as a design director seeing
   it among ten competitors, and score visual distinctiveness, clarity and craft from 1 to 10. If
   distinctiveness is below 8, change the direction (type, palette, composition, signature), not
   just details; then measure again.
7. **Hand over** in about 200 words: the file, what it does, the measurements that passed,
   assumptions made, at most three questions. No audit report.

Pre-flight checklist (the failures that slip through most often):

1. Flex children holding text have `min-width: 0`; grid tracks use `minmax(0, 1fr)`; user content and
   long tokens use `overflow-wrap: anywhere` (not `break-word`, which does not shrink the min-content
   width).
2. Headings and short text use `text-wrap: balance`; paragraphs `text-wrap: pretty` (Chromium and
   Safari only), plus `&nbsp;` between the last two words of key headlines.
3. Sibling cards align inner rows with `grid-template-rows: subgrid`; fallback: reserved heights in
   `lh` units and footers pinned with `margin-top: auto`.
4. Fixed sets (features, plans, stats) divide evenly into the column count at every breakpoint.
5. Inner radius = outer radius minus inset; one control height per size; one chip height; one media
   ratio per set, with `aspect-ratio` and `object-fit: cover`.
6. Every interactive element has hover, `:focus-visible` and active states; focus is never removed
   without a replacement.
7. Loading, empty, error, disabled and completion states exist; an empty result never shows as zeros.
8. Contrast meets AA: 4.5:1 body text, 3:1 large text and the parts that identify a control.
9. Labels sit above inputs; errors are text below the field, never colour alone.
10. Images and embeds have `width` and `height` or `aspect-ratio`.
11. Motion uses transform and opacity, 150 to 300ms, and honours `prefers-reduced-motion`.
12. Numbers use `font-variant-numeric: tabular-nums`, right-aligned in tables with matching headers,
    one format and precision per metric, and every figure agrees with every other.
13. Charts have a title that states the point, labelled axes with units, zero-based bars, direct
    labels where possible, and colour that is never the only signal. The plot area starts after the
    widest tick label; direct labels that would collide are offset or moved to a legend.
14. Tables show their rows in the page flow (or paginate); no fixed-height inner scroll box that hides
    rows on desktop. Navigation keeps every section reachable on phones (a menu if links are hidden).
15. Copy is specific; buttons are verbs naming the outcome; prices show currency, period and VAT.

## Project profiles

Detect the profile from routes, file names, content or the user's words, and read it before auditing
or building. Apply one; for a page that mixes two (a report with a dashboard section), use the one that
fits the main job and say so.

- **Marketing / landing**: `references/profile-marketing-landing.md` (includes pricing pages).
- **SaaS / dashboard**: `references/profile-saas-dashboard.md` (operational tools used daily).
- **Analytics report**: `references/profile-analytics-report.md` (data pages read, presented or printed).
- **E-commerce**: `references/profile-ecommerce.md` (storefronts and checkout).
- **Children's learning app**: `references/profile-kids-app.md` (touch-first, ages 4 to 9).

To add a profile for a new kind of product, copy the structure of an existing one: a `Detection:` line,
a source-of-truth note, a simulation persona, and `## Overrides:` sections stating only differences.

## Honesty

State what the input could not confirm: real screen-reader output, touch latency, network timing,
fonts that were not available. A named gap beats a guessed pass. Never report a measurement you did
not take; never score what you could not see.

`references/examples.md` has worked findings at every severity; `references/durable-fixes.md` maps
failure families to the tools that stop them returning.
