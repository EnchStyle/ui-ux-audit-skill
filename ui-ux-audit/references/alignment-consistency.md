# Category 10: Alignment, Consistency and Tokens

This category targets the defining AI failure: every component is a one-off. With no persistent design
system, the second button gets fresh padding, the third card a new radius, and a row of cards lines up
on the outside while everything inside floats. People see these faults instantly; tools rarely do.
Audit across components, not within them, and measure rather than eyeball: `scripts/uicheck.py`
reports each check below under the key named in brackets.

## The global system block (write it first in build mode, look for it in audits)

Every value that repeats comes from one place. In plain CSS, custom properties at `:root`; in Tailwind,
the theme config.

```css
:root {
  /* type: one scale, ratio about 1.25 */
  --fs-xs: .8125rem; --fs-sm: .875rem; --fs-md: 1rem; --fs-lg: 1.25rem;
  --fs-xl: 1.5625rem; --fs-2xl: 1.953rem; --fs-3xl: 2.441rem; --fs-4xl: 3.052rem;
  /* spacing: 4px base */
  --sp-1: 4px; --sp-2: 8px; --sp-3: 12px; --sp-4: 16px; --sp-6: 24px; --sp-8: 32px;
  --sp-12: 48px; --sp-16: 64px; --sp-24: 96px;
  --gutter: var(--sp-6);            /* one gap between cards at each level */
  --section: var(--sp-24);          /* one vertical rhythm between sections */
  /* shape */
  --r-sm: 6px; --r-md: 10px; --r-lg: 16px; --r-pill: 999px;
  --shadow-1: 0 1px 2px rgb(15 23 42 / .06), 0 1px 3px rgb(15 23 42 / .08);
  --shadow-2: 0 8px 24px rgb(15 23 42 / .10);
  /* controls */
  --ctl-sm: 32px; --ctl-md: 40px; --ctl-lg: 48px; --chip: 24px;
  --icon-sm: 16px; --icon-md: 20px; --icon-lg: 24px;
  /* media ratios */
  --ratio-card: 16 / 9; --ratio-thumb: 4 / 3; --ratio-avatar: 1;
  /* content widths */
  --measure: 65ch; --container: 1200px;
}
```

Components consume these and nothing else. A value used twice that is not a token is a token
waiting to be extracted.

## Checks

Each check: what to look for, how to measure, the fix, the default severity. Group all occurrences of
one kind into one finding.

### Shared edges [near_miss_edges]
Everything in a section starts on the same left edge: heading, intro, card grid, table, chart plot
area. A deliberate offset (a hanging label, an indented quote) is fine; a near miss of 1 to 6px looks
like a mistake, and nothing reads as sloppier. Common causes: a heading container with different
padding from the grid, a card grid with a negative margin, a chart plot area inset differently from
the panel title. Fix: one container and one inset per level; align the chart plot area to the panel's
text edge. Polish; Warning when it is in the hero or a primary grid.

### Card rows share inner lines [card_rows]
Equal-height cards still float their content to the top, so titles, chips, prices and buttons land
at different heights when copy differs in length. First choice: the grid owns the rows and each card
spans them with `grid-template-rows: subgrid` (widely supported since 2023), so every part lines up
without clipping copy. Fallback: card as a flex column, variable parts reserved with `min-height` in
`lh` units (for example `min-height: 3lh` for a three-line description), footer pinned with
`margin-top: auto`. Verify with deliberately uneven copy. Warning at desktop widths; Critical when
the misaligned part is a price or primary CTA that users compare across cards; Polish when it happens
only at phone widths.

### Tile values on one baseline [baselines]
In a row of KPI or stat tiles, the values sit on one line. A label that wraps in one tile pushes its
value down. Fix: subgrid rows, or reserve two lines for labels (`min-height: 2lh`), or shorten labels
so none wraps at any width. Warning at desktop widths; Polish at phone widths only.

### No lone item on the last row [grid_orphans]
A fixed set (features, plans, stats, team, logos, tags) whose last row holds a single item looks
unfinished. Fix: choose counts that divide the column count at each breakpoint (6 or 9 for three
columns, 4 or 8 for four), let a featured item span two columns, or change the column count per
breakpoint so the set balances. Catalogues and long lists that load more are exempt: a partial last
row is expected. Warning at the main desktop and phone layouts; Polish at in-between widths.

### No single word alone on a last line [widows]
Headings, card titles, button labels, short intros and captions never end with one word alone, at
any width you ship. Fix: `text-wrap: balance` on headings and short text (Chromium balances up to six
lines, Firefox up to ten); `text-wrap: pretty` on paragraphs (Chromium and Safari only, and it only
avoids short last lines in some cases); `&nbsp;` between the last two words of key headlines; a
tighter `max-width` so the break falls earlier. A button label that wraps to two lines is a sizing
fault: shorten the label or widen the button. Widows depend on the font, so check with the real font
and name stand-ins. Polish (one finding for all).

### Concentric corners [nested_radius]
An element inset inside a rounded container takes `inner radius = outer radius − inset` (a card with
16px radius and 8px padding holds an image with 8px radius). Equal radii at a small inset make the
corners look pinched. Polish.

### One height per control size [control_heights]
Inputs, selects and buttons that sit side by side share one height from the control tokens
(`--ctl-md: 40px`). A 40px input beside a 48px button is the classic newsletter-row fault; filter
bars with three different heights the dashboard one. Set `height` or `min-height` from the token and
`box-sizing: border-box`; align with `align-items: stretch` or matching heights, never by nudging.
Warning.

### One size per repeated component [chip_heights, icon_sizes]
Chips, badges and status pills: one height (`--chip`), one padding, one text size, whether or not
they hold an icon. Icons: one size per role (16 inline, 20 in controls, 24 in navigation), one stroke
weight, one family. Buttons: one height per size. Polish; Warning when the drift is in a primary
component.

### One media ratio per set [ratios]
Images, thumbnails, video posters and sparklines in one set share one aspect ratio from a token, with
`aspect-ratio` on the box and `object-fit: cover` on the image. Mixed ratios make a row of cards
ragged even when the boxes line up. Warning.

### One section rhythm [census: section_padding]
Sections share one vertical padding (or one small set tied to roles: hero, standard section, closing
band). Five different paddings for five ordinary sections (64, 96, 80, 72px) is drift the eye reads
as uneven pacing. Fix: one `--section` token, with a smaller step on phones. Warning.

### One gutter per level [gutters]
Gaps between cards are the same wherever cards sit at the same level (all KPI rows, all panel rows).
A tighter gap for a strip of small tiles can be deliberate; 24px in one row of panels and 16px in the
next is drift, and it knocks every edge below it out of line. Use `gap: var(--gutter)` on every grid.
Warning.

### Padding that reads as equal [pad_asymmetry]
A box whose bottom space is visibly larger than its top usually has a last child with a bottom
margin (a `p` inside a card). Fix: space children with `gap` in a flex or grid column, or
`> :last-child { margin-bottom: 0 }`. Polish.

### Headings belong to what follows [heading_prox]
The space above a heading is clearly larger than the space below it (about twice), so the heading
groups with its own content. A heading closer to the previous section than to its own content reads
as a caption for the wrong thing. Warning.

### Tables align by type [table_align]
Numeric columns are right-aligned with tabular figures, and their headers are aligned the same way.
Text columns left-aligned. Never centre data columns. Warning.

### Census: radii, shadows, type sizes [census]
One radius scale (at most three steps plus pill and circle), one elevation language (one shadow style
at one or two levels, or borders instead), type sizes from the scale. A value that appears once is
drift unless it is documented. Two radius systems on one screen (sharp beside round) or two shadow
languages: Warning. Small drift within one system (radii 2 to 4px apart, a one-off button padding):
Polish.

### Optical alignment (by eye on the screenshots)
- Icons beside text centre on the cap height, not the line box; play and arrow glyphs are nudged
  towards their visual centre.
- Text inside pills and buttons is vertically centred (flex centring or line-height equal to height).
- Numbers in a column align on the decimal point: same decimals per column, tabular figures.
- Quote marks hang outside the text edge in large pull quotes (negative `text-indent`;
  `hanging-punctuation` works only in Safari).
- Icons, avatars and logos in a row look the same size, which may mean slightly different boxes
  for different shapes.
Polish.

### Inner spacing smaller than outer spacing
Space inside a group is smaller than space between groups (padding 16px inside cards, 24px between
cards, 96px between sections). When inner and outer spacing are equal, grouping disappears and
everything floats. Warning.

## Cross-component drift census

- **Buttons:** collect every variant. There should be a small deliberate set (primary, secondary,
  ghost, destructive; sizes from the control tokens). Each one-off padding, radius or weight is drift.
- **Cards:** one radius, one border or shadow treatment, one inner padding.
- **Same concept, same component:** two date pickers, two empty-state layouts or two modal designs in
  one product mean a component was regenerated instead of reused. Fix by consolidating, not restyling
  both.
- **Interaction patterns:** the same action behaves the same everywhere (inline edit versus modal,
  toasts from one corner, one destructive confirmation pattern).

## Token health (report only when it causes visible drift)

Colours, spacing, radii, shadows and type come from tokens with purpose names (`--color-danger`, not
`--red-500`). Dark mode swaps token values centrally. Raw hex values scattered through components
explain why drift happens: mention them in the Fix of the drift finding rather than as a finding of
their own.
