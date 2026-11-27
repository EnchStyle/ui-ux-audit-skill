---
name: "ui-ux-audit"
description: "Audits and builds interfaces: web pages, dashboards, analytics reports, shops and mobile apps (iPhone, Android, React Native, Flutter, installable web apps). Catches what AI tools ship and people notice at once: broken or shifting layouts, cards and values off a shared line, orphaned words, drifting radii and spacing, clipped text, missing states, poor contrast, small targets, controls hidden on phones or under the notch, dishonest charts and numbers, confusing navigation, and generic AI-looking visuals. Use whenever the user asks to audit, review, check, critique, fix, polish or improve a page, screen, flow, dashboard, report, component, screenshot or design, or says 'looks off', 'looks AI-generated', 'is this ready to ship', 'make it look high-end'. Also use when building or restyling a page, dashboard, report, app screen or component, to pick one visual style and hold it; skip it for one-line edits. Includes measuring scripts, a severity registry, a style library and product profiles."
---

# UI/UX Audit

Find the interface problems AI tools ship and report them with fixes (audit), or avoid them while building
(build), on the web and on phones.

Most AI interface failures share one cause: the model writes a plausible picture of one state at one width,
never sees the render, and carries no design system from one component to the next. The cure is to measure the
render instead of reasoning about it, to hold every element to one system, and to score with one fixed table so
that two audits of the same page agree.

## Modes

| Mode | When | Read | Run |
|---|---|---|---|
| **Full audit** | "audit this", "is this ready to ship", "full review" | This file, `references/severity-registry.md`, the matching profile, `references/user-simulation.md`. Open a category reference only for a registry row you marked present or could not decide | `uicheck.py` (or `shotcheck.py` for images), then `reportcheck.py` on the report |
| **Quick review** | A question about one element or one symptom | This file and the registry rows the question touches; at most two category references | `uicheck.py` when there is a page to render |
| **Build** | Creating, restyling or changing a page, screen, flow or component. A repair to an existing page counts, however small it looks: measure before and after (step 7) | This file, the matching profile, `references/style-library.md`, `references/visual-excellence.md`, `references/usability.md`; `references/libraries.md` before using any library; `references/mobile.md` for phone screens | `uicheck.py` until clean |

Read what the mode lists and no more: a skipped file loses its rule, and loading everything buries the rules
that matter. A matching profile overrides the general rules wherever it says so.

## Step 1: measure the render

```
python3 <skill>/scripts/uicheck.py page.html --out out/                              # web page
python3 <skill>/scripts/uicheck.py s1.html s2.html s3.html --device iphone --out out/ # phone screens (or android)
python3 <skill>/scripts/shotcheck.py shots/*.png --platform ios --out out/            # screenshots only
```

`uicheck.py` renders at 360, 768 and 1280px (or the phone), in the dark scheme too when the page has dark
styles, and writes `out/checks.json`, first-screen and full-page screenshots, one sheet of close-ups per width
in `out/crops/` (control groups, form rows and panel edges at twice the size) and, for each scroll area, a
screenshot scrolled to its end. It prints candidates under the same codes the registry uses, then a focus test,
a tab walk, a click census (every distinct control operated once), the figures to cross-check, a census of
tokens and decoration, the fonts that were not available, the environment, and a **run id**. It also draws the
page with stand-ins for missing fonts and with real scrollbars; what only those passes list is marked
`_font-check` and `_scrollbars`. Other inputs: an address works like a file; `--attr data-theme=dark` for themes
switched by an attribute; `--states loading,empty,error`; `--print`; for a page that needs a build step, bundle
it first and say what stood in for what.

- **Candidates are not findings.** Confirm each on a screenshot or in the code. What you cannot confirm is
  dropped or goes under Verify. Open `checks.json` when the output says more items are there.
- **Look at every screenshot, close-up sheet and scrolled-to-the-end screenshot.** The script cannot see
  hierarchy, crowding, or whether the design has an idea. A button cut off at a panel edge is a few pixels on a
  full-page image, and a full-page image of an app shell is one screen: the close-ups and the end-of-scroll
  images are where those show.
- **A stand-in font is not a pass for fit.** With a missing font the main passes show what a visitor without it
  sees, not what the house font does to the layout. Fit counts as measured only where the output says a font of
  the same widths drew the text. What the font pass lists with a wide stand-in is a risk: Verify, with its code.
  With no stand-in at all, fit goes under Verify, never under Clean.
- **The script does not judge meaning.** Read and look for: chart honesty (axis start, how series are told
  apart), figures that should agree (use the figures list), claims and copy, meaning carried by colour alone,
  charts drawn on canvas, and every usability row.
- **A fix is finished only when a new run no longer lists it.** Quote the new run id.
- **No browser available:** read the code, write "no browser: estimates only" in Checked, and call the score
  provisional.
- **Screenshots only** (a design, a native app): run `shotcheck.py`; it says which numbers are measured and
  which are estimates. Judge only what an image shows; put the rest under Verify; call the score provisional.
- **Native app source** (Swift, Kotlin, React Native, Flutter): follow `references/mobile.md`.

Never report a measurement you did not take, a selector you did not see, or a screenshot you did not open.
The scripts are in `scripts/` beside this file. Never say that one is missing or could not run without quoting
the command you tried and the error it gave.

## Step 2: walk the main task (full audits)

Name the page's main task (the profile says what it is) and walk it as `references/user-simulation.md`
describes: as the real user, as a constrained user, and with awkward data. Use the click census and tab walk
as evidence of what each control does. Record whether the task can be completed, in how many steps, and each
hesitation.

## Step 3: go down the registry

Take `references/severity-registry.md` from top to bottom once. For every row: present, absent, or Verify.
One finding per code; severity from the table. Category references explain what to look for and how to fix:

| Registry group | Reference |
|---|---|
| Reach, layout and text | `structure-typography.md`, `interaction-responsive-a11y.md` |
| Accessibility | `interaction-responsive-a11y.md`, `color-states-forms.md` |
| States and behaviour | `color-states-forms.md`, `motion-performance.md` |
| Honesty and data | `content-honesty.md`, `data-viz-tables.md` |
| Consistency | `alignment-consistency.md` |
| Usability and navigation | `usability.md`, `navigation-icons.md` |
| Mobile | `mobile.md` |
| Visual quality | `visual-excellence.md`, `style-library.md` |

## Scoring

**Score = 100 − 12 per Blocker − 8 per Critical − 4 per Warning − at most 5 for all Polish, floored at 0.**
Do not add it up by hand: `scripts/reportcheck.py` prints the score line and verdict computed from your findings.
Verdicts: 90 to 100 Ready to ship; 70 to 89 Ship after fixing the top findings; 40 to 69 Significant rework;
below 40 Do not ship. Any Blocker means Do not ship. Screens that form one task are one flow with one score;
unrelated pages are scored separately and never averaged.

## Visual quality rating

Every full audit gives one rating, decided by what can be counted (the tells are listed in
`references/visual-excellence.md`; the script's decoration census counts several of them):

1. **Inconsistent**: two or more of `radius-drift`, `section-rhythm`, `gutter-drift`, `type-scale-drift`,
   `shadow-drift`, `style-drift` are present.
2. **Generic template**: three or more template tells.
3. **Competent but forgettable**: fewer than three tells, but the design has no idea of its own: it is the
   platform or framework default look. Test: name one designed element made for this product (a layout device,
   a type treatment, an illustration or chart style, a signature component). A logo, a single icon, the subject
   matter and platform-standard components do not count. If none can be named, it is this rating.
4. **Distinctive with slips**: one can be named (name it), with consistency or visual findings at Warning or
   above.
5. **Exceptional**: one can be named, with nothing above Polish in those groups.

Take the first that applies. Only rating 2 on a landing page is scored (the single Warning `visual-generic`,
because tells can be counted); every other rating, on every profile, is advice. When there is a house template or brand system, its fonts
and colours are fixed: judge execution inside it and never propose new ones.

## Report (full audit)

Write exactly this shape, then pass the draft to the checker on standard input and fix what it lists until it
prints OK: `python3 <skill>/scripts/reportcheck.py - --checks out/checks.json <<'DRAFT'` … `DRAFT`. No report
file is needed; the report is your reply.

```
# UI audit: <page or flow>
**Score:** 100 − (B×12) − (C×8) − (W×4) − min(5, P) = NN/100
**Verdict:** <band>
**Profile:** <name>. **Style:** <the house template or brand system the user named, or "none given">
**Checked:** uicheck run <id> (<browser, fonts drawn, scrollbars: the words the script prints>) at <widths or device>, <light and dark>; <n> screenshots viewed; walk of <n> controls; <limits, and the user's own environment where it was not reproduced>
**Visual quality:** <rating>: <one line why>
**Top 3:** <ID and title; ID and title; ID and title>

## Blockers (N)
## Critical (N)
## Warnings (N)
## Polish (N)
## Task walk
<task | completed or not | steps | hesitations, citing finding IDs>
## Visual quality
<the rating, the element that makes the page specific or the tells counted, and two to four concrete moves>
## Verify (N)
<what the input could not confirm, each with the code and severity it would take>
## Wiring to confirm
<one line listing inert controls a static page cannot have>
## Clean
<one line: registry groups checked with nothing found>
## Durable fixes
<one to three tools from durable-fixes.md, each as a sentence to paste into a coding assistant>
## Questions
<at most three, each with the assumption made>
```

Findings under Blockers, Critical and Warnings:

```
**C2 [contrast-text] Hero subline is too pale to read** (`.hero p`; 360, 768, 1280)
**Found:** <the fact, with the measurement or the code line>
**Why:** <who it hurts and how, one line>
**Fix:** <the smallest concrete change>
```

Polish findings take one line: `**P1 [widow]** <where>. Fix: <change>.` IDs run B1, C1, W1, P1 in order. The
code in brackets is the registry code. Omit a section only when it is empty (Task walk always stays). About
1 200 words for a page and 1 500 for a flow with up to ten findings, plus 40 words for each finding beyond ten:
an audit nobody finishes reading fixes nothing. If it does not fit, shorten Why and Fix; never drop a finding
to save words. No text before the first line.

## Quick review

One line first: how many issues and the worst. Then two to five findings in the finding format, most severe
first. Cover the whole element asked about (its layout, its figures against the script's cross-check list,
its states), not only the symptom named. End with at most two lines on what depends on code you did not see. About 400 words, no score.

## Build mode

1. **Profile and brief.** Pick the profile. Write one sentence saying what the screen is for and who uses it;
   it appears on the first screen in the user's words, as the subline of a landing page and beside the heading
   elsewhere. On a dashboard or a report the heading is the answer itself ("4 deliveries are running late", "Revenue
   rose 6% in the quarter"); controls such as filters come after the answer, not before it.
2. **Art direction first, then one token block.** A house template or brand system, when there is one,
   replaces these choices. When the user names a style or a mood, wants several pages or products to match, or
   the page is a report or analysis, take the style from `references/style-library.md` (its table chooses when
   no name is given) and make it this product's as that file says. Otherwise, before any code, sketch three
   directions in your working notes, each with: the idea in one sentence (what makes the page specific to
   this product, data and audience), a type pairing and scale, a palette drawn from the subject's own world
   (freight: kraft, container rust and ink; energy: slate and signal amber) rather than default SaaS blues,
   teals and greens, one signature element, and a layout motif. Pick the most specific direction that stays
   clear; the safe option is usually the generic one, so never pick it by default. Test the choice against
   the template tells in `references/visual-excellence.md`: if a stranger could not tell this page from ten
   other AI-built pages, choose again. With no web fonts, character comes from system stacks used with intent
   (a serif display stack such as `"Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif` against a
   sans body, or a condensed stack for data), a large display size with tight tracking, weight, colour and
   composition (at least one full-bleed band; not every section an equal card grid). The signature element
   is real content set large: the product's own output or the data's most telling view.
   Either way, write the result as one token block in the form the style files use (fonts, seven sizes,
   colours including `--ok`, `--warn` and `--bad`, radii, shadows; a light and a dark set for dashboards,
   reports and apps) as the first thing in the style sheet. Components use only its values, and every screen
   of a flow carries the same block: that is what stops drift between screens.
   Then list the sections and, beside each, the view it will show (Depth and finish in
   `references/visual-excellence.md`): a section planned as words alone needs a reason.
3. **Plan for use** (`references/usability.md`): one main action per screen, a next step always visible,
   navigation that shows where the user is and how to go back, plain labels, advanced options tucked away.
4. **Real content, computed figures.** Use the user's content or sample content labelled as sample. Compute
   every displayed number in code from the source data, recompute a sample a second way, and make every
   section use the same method; describe the method in a short note. Never invent a figure, a customer, a quote
   or a logo. Titles and captions follow the filters.
5. **Libraries** only from `references/libraries.md`, themed to the style tokens, never left on their defaults,
   never recalled from memory.
6. **Every state and width.** Loading, empty, error, disabled and long content; 320 to 1440px, or the phone
   sizes in `references/mobile.md`. A page with states reads `?state=loading|empty|error` from its address
   and shows that state, so the script and the user can see each one.
7. **Measure.** `python3 <skill>/scripts/uicheck.py page.html --widths 320,360,768,1280,1440 --states loading,empty,error --out out/`
   (add `--device` for phone screens; pass every screen of a flow in one call to get the style-drift check).
   Fix until these are empty: page-overflow, content-cut-off, control-obscured, text-clipped, text-spill,
   text-overlap, contrast-text, false-feedback, focus-missing, keyboard-unreachable, name-missing, label-placeholder,
   alt-missing, heading-order, zoom-blocked, hover-only, media-unsized, card-rows, tile-baseline,
   control-heights, segment-widths, grid-lone-item, radius-nested, heading-proximity, safe-area, style-drift, and widow on
   headings, control-overflow, scroll-unexpected, scroll-nested and table-sticky, in the `_font-check` and
   `_scrollbars` passes too: a layout that only fits a narrow stand-in font, or only without scrollbars, does
   not fit. Run again after every fix. Clear a candidate by repairing the element, never by deleting the
   detail it sits in.
   Keep the first clean run (`cp out/checks.json out/baseline.json`) and run every later change set with
   `--baseline out/baseline.json`, repairs made for accessibility included: a fix for one row can break another
   (hidden text that stretches a panel, a label that widens a switch). Clear every line it prints under
   "regression" before handing over. The run also lists fonts that were not available: its screenshots show what visitors
   without those fonts will see, so if a display face has fallen back to a default-looking one, change the
   stack until the stand-in still looks intended.
   **A house or framework style sheet laid over an existing page**: take the baseline first. A shared component
   class (callout, card, note) restyles everything inside it, so weight, size and padding of any control in
   it change too: wrap text in text components, and measure again every control that ends up inside one (the
   regression pass lists controls whose type or padding changed). Search both style sheets for class names
   they share (`.title`, `.body`, `.note`): the system's type rule will land on the page's layout element.
8. **Look as a stranger.** From the first-screen screenshots alone answer: what is this, who is it for, what is
   the main action, where am I, what is the largest thing on the screen? If any answer needs the code, fix the
   design. Then go through the eight checks and Depth and finish in `references/visual-excellence.md` on the
   full-page screenshots, section by section.
   Last, judge the page cold: look at the 1280 and 360 screenshots as a design director seeing it among ten
   competitors, and score visual distinctiveness, clarity, craft and finish from 1 to 10. If distinctiveness
   is below 8, change the direction (type, palette, composition, signature), not just details; if finish is
   below 8, add the views that are missing; then measure again.
9. **Hand over** in about 200 words: the file, the direction or style and why, the run id with the environment
   the script prints (browser, fonts drawn, scrollbars), what passed, what was not reproduced of the user's own
   environment (their browser and system, the house font), assumptions, at most three questions. No audit report.

Pre-flight checklist (the failures that slip through most often):

1. Flex children holding text have `min-width: 0`; grid tracks use `minmax(0, 1fr)`; user content uses
   `overflow-wrap: anywhere`.
2. Headings use `text-wrap: balance`; key headlines also have `&nbsp;` between the last two words.
3. Sibling cards align inner rows with `grid-template-rows: subgrid`, or reserved heights and pinned footers.
4. Fixed sets divide evenly into the column count at every breakpoint, or the last item spans the row.
5. Inner radius = outer radius − inset; one control height per size; one width for the options of a switch; one media ratio per set.
6. Every control has hover, `:focus-visible` and active states; nothing essential appears on hover only.
7. Loading, empty, error and completion states exist; an empty result is never drawn as zeros;
   `[hidden] { display: none !important }`, so that no display rule shows a message that is marked hidden.
8. Contrast: 4.5:1 for text, 3:1 for large text and for the edges that identify a control.
9. Labels sit above fields; errors are text beside the field, never colour alone.
10. Images and embeds have `width` and `height` or `aspect-ratio`.
11. Motion uses transform and opacity, 150 to 300ms, and stops under `prefers-reduced-motion`.
12. Numbers use tabular figures, right-aligned in tables with matching headers, one format per metric.
13. Charts: a title that states the point, axis titles with units, bars from zero, direct labels, never colour
    as the only signal.
14. Phones: a viewport meta tag that allows zoom, a menu for anything hidden, safe-area padding on fixed bars,
    44px (iPhone) or 48px (Android) controls, fields at 16px or more.
15. Copy is specific; buttons are verbs naming the outcome; prices show currency, period and tax.
16. Text for screen readers only: `position: absolute; top: 0; left: 0; width: 1px; height: 1px; margin: -1px;
    overflow: hidden; clip-path: inset(50%); white-space: nowrap`, inside a `position: relative` cell, row or
    label. With no positioned parent nearby it is placed against a distant one and stretches that box.
17. One scroll area per region, never one inside another that scrolls the same way. In an app shell the page
    does not scroll and each panel has exactly one inner scroller. To clip a panel sideways use
    `overflow-x: clip`; `overflow-x: hidden` alone makes it scroll down as well, and `overflow: hidden` hides a
    stretched scroll area without removing it.
18. A long table keeps its header in view by sticking to whatever scrolls: no overflow box around a table that
    scrolls with the page. On phones a wide table becomes stacked rows, or pages of 15 rows or fewer in a
    sideways scroller with the first column sticky.
19. A switch or button row in a narrow panel: label above, options of one width, room to spare in the font pass.

## Profiles

Choose the profile from the content or the user's words, read it before auditing or building, and name it in
the report. Use one; when a page mixes two, use the one that fits its main job. When none fits, use no profile:
the general rules apply and the visual rating is advice.

- **Marketing / landing**: `references/profile-marketing-landing.md` (includes pricing pages).
- **SaaS / dashboard**: `references/profile-saas-dashboard.md` (tools operated daily).
- **Analytics report**: `references/profile-analytics-report.md` (data pages read, presented or printed).
- **E-commerce**: `references/profile-ecommerce.md` (storefronts and checkout).
- **Mobile app**: `references/profile-mobile-app.md` (native, cross-platform and installable web apps).
- **Children's learning app**: `references/profile-kids-app.md` (touch-first, ages 4 to 9).

A new profile copies the structure of an existing one: a `Detection:` line, a source-of-truth note, the main
task, a simulation persona, and `## Overrides:` sections that state only differences.

## Honesty

State what the input could not confirm: real screen-reader output, a real device, touch latency, network
timing, fonts that were not available. A named gap beats a guessed pass. Never score what you could not see.

`references/examples.md` has worked findings at every severity; `references/durable-fixes.md` maps failure
families to the tools that stop them returning.
