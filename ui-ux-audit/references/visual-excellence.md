# Visual quality: what separates professional design from AI output and templates

The bar is a page that a design-literate person trusts and remembers: clear first, then specific, then
precise. Distinctive never excuses a slower read, a weaker hierarchy or a less honest chart.

Professional work differs from generated and templated work in eight ways that can be checked. Each is a rule
to build by and a check to audit with. They are what "looks expensive" is made of: nothing here is decoration.

## The eight checks

| # | Professional work | Build rule | Audit check (measure) | Code |
|---|---|---|---|---|
| 1 | **Restraint** | Every visual element has a job (group, rank, signal state, show the product). At most one large gradient, no glow shadows, no emoji as icons, a badge only where there is a status, blur only on a floating layer | Decoration census from `uicheck.py`: `large_gradients` above 1, `glow_shadows` above 0, `emoji_in_interface` above 0, `blur_surfaces` on content, pills on more than a third of cards | `decoration`, or a tell for `visual-generic` |
| 2 | **A clear focal point** | One thing per screen is clearly the largest or strongest: the headline, the key figure or the product. The next thing is clearly smaller | "First screen: largest text" from the script: the largest is at least 1.3 times the next size. On dashboards: not more than six equal tiles with nothing larger | `hierarchy-flat` |
| 3 | **Deliberate white space** | Space comes from the scale; space inside a group is smaller than space between groups; sections share one rhythm | `section-rhythm`, `gutter-drift`, `heading-proximity`, `pad-asymmetry` | those codes |
| 4 | **A tight type system** | At most two families and one monospace; six or seven sizes from one scale; two or three weights; text lines of 45 to 90 characters | Census: families, weights, number of sizes; `type-scale-drift`; `line-length` | those codes |
| 5 | **Optical alignment** | Shared left edges; values on one baseline; matching parts of cards on one line; icons centred on the text beside them; concentric corners | `edge-near-miss`, `tile-baseline`, `card-rows`, `radius-nested`, `icon-sizes`; look at icon and text pairs on the screenshot | those codes |
| 6 | **Consistent detail at small sizes** | One border weight, one icon stroke and size per role, one radius per component type, one control height per size, one focus ring | Census: radii, shadows, icon strokes; `control-heights`, `chip-heights`, `radius-drift`, `shadow-drift` | those codes |
| 7 | **Real content** | The actual product, real or computed numbers, specific words. Sample data is labelled. No lorem ipsum, no invented customers, quotes or logos, no grey boxes | `placeholder-content` from the script; read every claim | `placeholder-content`, `unsourced-claim` |
| 8 | **Considered empty and edge states** | Loading, empty, error and long content are designed, not left to chance | `--states` run; click census flags; the longest value on the page still fits | `state-empty`, `state-error`, `text-clipped`, `text-spill` |

In build mode, go through the eight after the script is clean and fix anything a check shows, then go through
Depth and finish below. In an audit they are not extra findings: each maps to registry codes that the registry
pass already covers.

## Depth and finish (build mode)

Restraint removes ornament, never information. In this skill's blind comparisons (pairs of pages built from one
brief, judged on which looks more professional and more expensive) the plainer page lost almost every time. The
winner carried more real detail, every piece of it doing a job. Seven things decided it. Plan them before the
code and check them at the end on the full-page screenshots:

1. **Every section shows something.** A feature is shown as a small view of the product doing that job (the
   invoice as the customer receives it, the map with the parcel on it), a step as its screen, a result as a chart or a ruled
   figure. A heading with paragraphs, or numbered text alone, reads as unfinished. A method note, a list of
   questions and legal text are the exceptions.
2. **No band is half empty.** At 1280 the content of every band reaches across its grid, text beside its view.
   When half the width is empty, add the supporting piece, or narrow the column and centre it.
3. **The answer leads.** A dashboard or a report opens with the answer as the largest thing on the screen
   ("7 of 40 deliveries are late") and its parts beside it as figures in the status colours. Filters sit
   below the answer in one quiet row.
4. **One view is made for this data.** The main view follows the shape of the data: things in time become a
   timeline with now marked, things in places a map or a plan, parts of a whole one divided bar, stages a
   sequence, a level a gauge against its limit. A table or a list of cards alone is the fallback and comes last.
5. **One strong contrast.** One dark or saturated full-width band (the hero, the proof or the closing call)
   against the page ground, and one accent that keeps one meaning.
6. **Status is designed.** Every state (ready, late, waiting) has one mark used everywhere, a pill or a ruled
   label, always with its word. States that need action carry the status colours; routine states stay
   neutral, so that colour keeps its meaning. This is information, not a badge to cut.
7. **Nothing looks unfinished.** No dashed outline or grey box standing for a picture, no empty cells, no date
   field or select left in the browser's default look (keep it native, style it with the tokens), no "sample"
   tag on every row (say it once per screen), no cut-off value, no button alone on a line, no heading or
   caption ending in one orphan word, no heading pressed against the band above it, no pale outline standing
   for a value in a chart (data marks are solid).

Clear a script candidate by repairing the element, never by deleting the detail it sits in: a page that passes
because it holds less is the plain page that loses.

## Template tells (count them for the rating)

A tell is counted when it is present and the brief or brand does not ask for it:

1. A violet, indigo or blue-to-purple gradient, a glowing button, or blurred colour blobs behind a centred hero.
2. A centred hero followed by a row of three or four identical icon cards.
3. A small uppercase label above every section heading (the census counts them).
4. Numbered 01, 02, 03 markers on things that are not a sequence.
5. Glass or blur as the default surface for content.
6. Looping decorative animation.
7. Emoji used as icons.
8. A default typeface with no decision behind it together with slate greys (system sans on white rounded cards
   on a pale grey page with one saturated button colour).
9. Every section the same shape: the same centred stack or the same card grid three or more times in a row.
10. A library's untouched default theme (default chart colours and fonts, stock button blue).
11. A "premium" costume worn with no reason in the subject: cream with a display serif and terracotta,
    near-black with an acid accent and monospace labels.
12. A badge, pill or tag on most cards that states no status (a status pill on an order, a ticket or a delivery
    is information).

Three or more tells: "Generic template" (on a landing page this is the one scored finding, `visual-generic`).
Fewer, with no designed element made for this product: "Competent but forgettable", which is advice and never
scored. The rating rules are in SKILL.md. A page that follows one style from
`style-library.md` consistently is not generic because of that style's own conventions.

## Moves (two to four with every rating)

A move is a concrete change grounded in this product's subject, audience and content, small enough to act on.
"Make it more premium" is not a move; "lead the hero with the live freshness monitor from section 3, at full
width, and cut the three icon cards to one annotated screenshot" is. When a landing page has the `visual-generic` finding, the moves go in its Fix.

### Landing pages
- **Product-led hero.** Show the product doing its job: a real screenshot, a working mini-component, or real
  output. Replace abstract illustrations and gradient blobs.
- **Headline says what it does and for whom** in two to eight words; the subline adds about twenty.
- **A typographic signature.** A large display size with tight tracking and a deliberate, balanced line break,
  against quiet body text.
- **Vary section shapes.** Follow a split hero with a full-width proof band, then a stacked narrative, then a
  dense comparison.
- **Proof with specifics.** Real customer names and outcomes with sources, or none.
- **One accent, one main action**, repeated with the same label at natural breaks.

### Dashboards
- **One primary metric dominant**; supporting tiles smaller and quieter.
- **Group by the question** the user asks ("Are we on track?", "What needs attention?"), not by data source.
- **One tile anatomy**: label, value, change with sign and basis, timeframe, in fixed positions.
- **Fewer boxes.** Spacing, alignment and a subtle surface change instead of borders around everything.
- **Status colour sparingly** so that red means something.
- **Freshness visible** ("Updated 14:32").

### Analytics reports and data pages
- **Headline every figure with its finding** ("Parcel volume fell 6% in August"); the neutral description goes
  in the caption.
- **One chart grammar**: the same axis style, gridlines, fonts, number formats and series colours in every figure.
- **Key numbers in tiles that match the text and tables exactly.**
- **Annotate** the events that explain the data; show targets and prior periods as reference lines.
- **Method and sources** in a short, visible note; a layout that prints.

### Apps
- **One title, one main action per screen**; system-like controls; the same token block on every screen.
- **Thumb-sized targets with air between them**; the main action in the lower half.

### Any page
- Tighten to the system: one radius scale, one gutter, one control height.
- Remove one decorative element for every one you add.
- Make the first screen answer "what is this and what do I do" before anything else.

## Where the eight come from

Restraint and focus: "aesthetic and minimalist design" among Nielsen's heuristics (extra elements compete with
the ones that matter). Type: Butterick's key rules (body 15 to 25px, 45 to 90 characters, 120 to 145% line
spacing, few typefaces) and Apple's typography guidance (few typefaces, no thin weights). Consistency at small
sizes and optical alignment: the token and grid discipline shared by the design systems cited in
`style-library.md`. Real content and states: Apple's Loading guidance and the error-message guidelines cited
in `usability.md`. Depth and finish comes from the reasons blind judges gave when comparing pairs of
builds made with and without this skill; the figures are in the skill's test report.
