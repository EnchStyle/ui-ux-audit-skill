# Category 14: Visual Quality and Distinctiveness

The bar is a page that a design-literate person remembers and trusts: distinctive, precise and clear.
Clear comes first. Distinctive never excuses a slower read, a weaker hierarchy or a less honest chart.

## Rate it (every full audit of a landing page, dashboard or analytics page)

| Rating | What it looks like | Landing and marketing pages | Dashboards, reports, shops, apps |
|---|---|---|---|
| **Exceptional** | A clear idea specific to this product, executed with precision; nothing to add | No finding | No finding |
| **Distinctive with slips** | A real idea, but execution slips (alignment, rhythm, one-off values) | The slips as their own findings | Same |
| **Competent but forgettable** | Correct and tidy, but no idea: swap the logo and it could be any product | Warning: "Visual design has no point of view", moves in the Fix | Rating and moves in the Visual quality section, unscored |
| **Generic template** | The AI default look (tells below) regardless of subject | Warning: name the tells, moves in the Fix | Rating and moves in the Visual quality section, unscored |
| **Inconsistent** | Several systems on one page: radii, greys, type scales, card styles | The consistency findings (Category 10) | Same |

For dashboards and reports, distinctiveness never outranks clarity: the verifiable hierarchy faults
(no dominant answer, twelve equal tiles, chrome louder than the data) are ordinary findings, and the
aspirational moves are advice.

A rating always comes with two to four **moves**: concrete changes grounded in this product's
subject, audience and content, each small enough to act on. "Make it more premium" is not a move;
"lead the hero with the live freshness monitor from section 3, at full width, and cut the three icon
cards to a single annotated screenshot" is.

## What high-end looks like

1. **One idea, carried through.** A signature grounded in the product: a live product component in
   the hero, the real data as the main visual, a distinctive typographic system, a precise grid with
   a strong structural motif. One idea, repeated with discipline, beats five decorations.
2. **Typographic contrast and voice.** A clear scale (ratio about 1.25 to 1.333) with a display size
   meaningfully larger than body; weight contrast; tighter tracking on large display type; generous
   leading for reading; line length 60 to 75 characters; tabular figures in data. At most two
   families, each with a job. Emphasis inside a headline uses the same family (italic or weight), not
   a stray serif word.
3. **Colour with restraint and intent.** A tinted neutral base that matches the brand's temperature,
   one accent reserved for action and the key data, semantic colours kept for meaning. Dark themes
   designed, not inverted: dark grey base, lighter surfaces for elevation, desaturated accents.
4. **Composition and rhythm.** A visible grid; sections that vary in shape (split, full-bleed,
   stacked narrative, dense data) instead of the same centred stack repeated; one vertical rhythm;
   asymmetry only where it has a reason; space used for grouping before boxes and borders.
5. **Craft in the details.** Shared edges, concentric corners, one control height, no orphans, no
   widows, balanced headings, optical alignment, real states. Details are where "expensive" is
   perceived (`references/alignment-consistency.md`).
6. **Real content.** The actual product, real numbers, specific copy. Illustrative data is labelled as
   such. Nothing faked (`references/content-honesty.md`).
7. **Data as the hero** (dashboards and analytics). One primary answer per view; chart titles that
   state the finding; direct labels instead of legends; muted grids and axes so the data carries the
   ink; comparison built in (versus target, prior period, plan); annotations that explain spikes;
   small multiples instead of rainbow spaghetti.
8. **Motion with a job.** One orchestrated entrance, fast responsive feedback, nothing looping for
   attention; all of it honours reduced motion.

## Brand systems and house templates

When the project has a brand system, design tokens or a house template (a corporate report template,
say), its fonts, colours and components are fixed. Audit execution within it and raise quality
through hierarchy, rhythm, alignment, data-ink, chart grammar and copy. Never propose new brand
colours or fonts; propose better use of the ones that exist. A deviation from the house system is
itself a finding.

## The AI default looks (flag when unjustified by the brief)

- Violet or indigo gradients, glowing purple CTAs, blurred mesh blobs behind a centred hero.
- Centred hero over a gradient with a big-number stat row; three identical icon feature cards; a
  small uppercase eyebrow label above every section; numbered 01/02/03 markers on things that are not
  a sequence.
- Glassmorphism as the default surface; scattered infinite micro-animations.
- An unconsidered default typeface and slate greys where the brand wanted personality.
- The generic SaaS look: system sans, white rounded cards on a light grey page, one saturated button
  colour, numbered section chips, every section the same centred stack. Clean, and indistinguishable
  from a thousand others.
- The "premium" defaults swapped in for each other: warm cream with a display serif and terracotta,
  near-black with one acid accent and monospace labels, hairline broadsheet columns. Each is fine when
  the subject calls for it; as a reflex it makes every brand invisible.

Report the pattern, why it reads as templated, and the replacement grounded in this product. "This is
generic" is not a finding; "centred gradient hero plus three icon cards is the template answer; for a
freshness monitor, lead with the product's own lineage view showing a stale table turning red" is.

## Moves library

### Landing pages
- **Product-led hero.** Show the product doing its job: a real screenshot, a working mini-component,
  or real output. Replace abstract illustrations and gradient blobs.
- **Headline says what it does and for whom** in two to eight words; the subline adds about twenty.
- **A typographic signature.** Large display size with tight tracking and a deliberate line break
  (balanced), set against quiet body text.
- **Vary section shapes.** Follow a split hero with a full-bleed proof band, then a stacked narrative,
  then a dense comparison. Never three identical centred sections in a row.
- **Proof with specifics.** Real customer names and outcomes with sources, or none.
- **One accent, one primary action**, repeated with the same label at natural break points.

### Dashboards
- **One primary metric dominant**; supporting tiles smaller and quieter.
- **Group by the question** the user asks ("Are we on track?", "What needs attention?"), not by data
  source.
- **One tile anatomy**: label, value, change with sign and basis, timeframe, in fixed positions.
- **Fewer boxes.** Use spacing, alignment and a subtle surface change instead of borders around
  everything.
- **Status colour sparingly** so red means something; neutral when on track.
- **Freshness visible** ("Updated 14:32").

### Analytics reports and data pages
- **Headline every figure with its finding** ("Parcel volume fell 6% in August") and put the neutral
  description in the caption.
- **One chart grammar**: same axis style, gridlines, fonts, number formats, and the same colour for
  the same series in every figure.
- **Key numbers in tiles that match the text and tables exactly.**
- **Annotate** the events that explain the data; show targets and prior periods as reference lines.
- **Method and sources** in a short, visible note; print-friendly layout.

### Any page
- Tighten to the global system: one radius scale, one gutter, one control height.
- Remove one decorative element for every one you add.
- Make the first screen answer "what is this and what do I do" before anything else.
