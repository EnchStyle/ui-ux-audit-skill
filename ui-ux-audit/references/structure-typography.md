# Categories 1 to 3: Typography, Layout and Spacing, Visual Hierarchy

Examples use plain CSS with Tailwind equivalents where common. Alignment across components (shared
edges, card rows, baselines, orphans, widows, radii, control heights) is in
`alignment-consistency.md`; this file covers what happens inside a block.

## Category 1: Typography and text breaking

- **Overflow from long tokens.** Emails, URLs, IDs, hashes and compound words push flex and grid
  children wider than their container. Fix: `min-width: 0` (`min-w-0`) on the flex child holding text,
  `minmax(0, 1fr)` grid tracks, and `overflow-wrap: anywhere` on user content. `overflow-wrap:
  break-word` (Tailwind `break-words`) is not enough: it breaks only after layout and does not shrink
  the min-content width, so the track still widens. `flex-shrink: 0` on icons and avatars.
- **A control starving a text column.** A badge, toggle or button group sharing a row with text takes
  width from it, collapsing a sentence into a one-word-per-line ribbon or breaking a timestamp or email
  mid-value. `min-width: 0` controls how text wraps, not how much room it gets: the fix is width. Give
  the text its own row at narrow widths and move the control below it; stack a value under its label
  instead of `justify-content: space-between`. Verify at 360px with real long content. Critical at
  common phone widths; Warning otherwise.
- **Truncation needs all three parts**: `overflow: hidden`, `text-overflow: ellipsis`,
  `white-space: nowrap` (Tailwind `truncate`), or `line-clamp` for several lines. Truncated values
  expose the full value on hover, focus or copy.
- **Line length** 45 to 75 characters for reading text (`max-width: 65ch`). Paragraphs running the
  full width of a desktop layout are a Warning on reading pages.
- **Line height**: about 1.5 to 1.65 for body text, 1.1 to 1.25 for headings. Display type at
  `line-height: 1` clips descenders and accents (ą, ę, į, ų in Lithuanian); use at least 1.1.
- **Type size**: body reading copy 16px on reading pages; secondary copy 13 to 15px is fine; data
  labels, chart ticks and table headers at 12px are normal in dense data UI. Flag text below 12px
  (Warning), and body reading copy below 16px only on reading pages (Polish; Warning below 14px).
  Inputs below 16px make iOS zoom on focus.
- **Letter spacing**: add tracking to all-caps labels; none on lowercase body; tighten large display
  sizes slightly.
- **Tabular figures** (`font-variant-numeric: tabular-nums`) for timers, prices, scores and table
  numbers, so digits do not jitter. Some system fonts already have equal-width digits; the property
  costs nothing and protects the rest.
- **Heading levels** in order (h1, h2, h3); the tag is structure, the class is size. A section meant
  for another page starts at h2.
- **Font loading**: `font-display: swap` plus a metric-matched fallback (`size-adjust`) so text neither
  vanishes nor jumps. Named fonts that never load (no `@font-face`, not a system font) mean the design
  was never seen as intended: Polish, and name the stand-in in the report.

## Category 2: Layout and spacing

- **Spacing on the scale.** Values off the 4 or 8px scale (`13px`, `gap-[7px]`) usually paper over a
  layout problem: find the cause before changing the number.
- **One owner per gap.** A parent's `gap` or `space-y` plus a child's margin doubles gaps; section
  margins defined on both neighbours double them too. Prefer `gap` in flex and grid.
- **Fixed heights on variable content** clip text as soon as it grows. Use `min-height` or let
  content size the box; fixed heights are for media and decorative regions.
- **Centring**: one mechanism per element (the parent's alignment, or `place-items`), not three
  stacked.
- **Z-index ladder**: content 0 to 10, sticky header 30, dropdowns 40, modals 50, toasts 60.
  `z-index: 9999` is a smell; a modal under a sticky header is a Blocker waiting for a click.
- **Conflicting declarations** (`px-4 px-2`, two `margin` rules for one element) matter only when they
  produce a visible fault; then fix the cause, not just the duplicate.

## Category 3: Visual hierarchy

- **One primary action per view.** Four or more sibling actions with identical weight and no clear
  primary make users stall (Warning); six or more is overchoice (Critical on a conversion page).
  Content lists, navigation and tables are exempt.
- **Size, weight and contrast follow importance.** The largest, highest-contrast element is the most
  important one. A primary CTA at 60% opacity beside full-contrast decoration is inverted hierarchy.
- **Hero discipline** (landing pages): the headline, subline and primary CTA fit the first screen at
  1280 × 800 and at 360 × 740; headline two lines or fewer on desktop; at most four text elements.
  Supporting proof, logos and features move below.
- **Scan paths.** Key information and the primary action sit where eyes land (top left to right, then
  down); nothing essential stranded bottom right in a dense grid.
- **Section repetition.** The same layout family (three centred cards, image-left/text-right) more than
  twice in a row reads as a template. Vary the shape.
- **Eyebrow restraint.** A small uppercase label above a heading now and then is fine; above every
  section it becomes the templated rhythm.
- **Whitespace is structure.** Group with proximity before boxes and borders; space inside a group is
  smaller than space between groups.
