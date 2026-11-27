# Profile: Analytics Reports and Data Pages

Severities are set only in `severity-registry.md`; the codes in brackets below are its rows.

Pages that present analysis to be read, discussed, presented or printed: management reports, market
and portfolio analyses, quarterly reviews, research write-ups with charts, tiles and tables. Unlike a
dashboard, the reader visits once or occasionally and needs the argument, not a console. These rules
override the universal defaults.

Detection: a report or analysis framing (period in the title, sections such as summary, method,
findings, recommendations), figures with captions, tiles summarising a period, print styles, or the
user saying so. A house report template, when one exists, is the source of truth for fonts, colours,
tile and figure blocks: audit execution within it.

Main task: get the conclusions in two minutes and check that the numbers support them.

Simulation personas: a senior manager reading on a laptop before a meeting, wanting the three
conclusions in two minutes; the same person opening it on a phone; an analyst checking whether the
numbers add up.

## Overrides: the argument first

- **The top of the page states the conclusions**: a summary with the key numbers that the rest of the
  report supports. A report that makes the reader assemble the conclusion is `purpose-unclear`.
- **Every figure has a headline stating its finding** and a caption stating what is measured, the unit,
  the period and the source. Missing titles, axis titles, units or text alternatives are `chart-labels`.
- **Tiles, tables and text agree to the unit.** Recompute totals in code; any mismatch is `figures-disagree`,
  a Blocker on this profile because the reader acts on the figures. `chart-axis` and `control-relabels` are
  Blockers here for the same reason, and `chart-colour-only` is Critical.
- **Method and assumptions are visible**: a short method note naming sources, periods, exclusions and
  how figures were calculated, so a reader can replicate them.

## Overrides: one chart grammar

- Same axis style, gridlines, number format and decimal rules in every figure; the same series keeps
  the same colour everywhere; zero-based bars; comparisons (target, prior period) as reference lines;
  annotations for events that explain the data.
- Direct labels instead of legends where there is room.

## Overrides: reading layout

- **Line length 60 to 75 characters** for prose; longer lines are `line-length`.
- **Tiles in a row share one anatomy and one baseline** (`alignment-consistency.md`); labels that wrap
  in one tile push its value off the line.
- **Tables**: numbers right-aligned with matching headers, units in headers, totals row distinct,
  contained horizontal scroll on phones with a cue.
- **Language and locale**: number, date and currency formats follow the report's language (Lithuanian:
  "48 212", "94,6 %", "2026-09-26" or "2026 m. rugsėjo 26 d."); the page `lang` matches.

## Overrides: print and export

- A print stylesheet (render it with `uicheck.py --print`): no navigation or interactive chrome, figures not split across pages
  (`break-inside: avoid`), colours that survive greyscale or print (patterns or labels, not colour
  alone), URLs of sources visible.
- An export button that shows progress and then produces nothing goes under Wiring to confirm; one
  that claims success ("Report downloaded") when nothing happened is `false-feedback`.

## Visual quality for reports

Exceptional reports look calm and authoritative: a clear typographic hierarchy, generous but
consistent spacing, one accent used for the data that matters, charts with high data-ink and
explanatory headlines, and tiles that summarise without decoration. Within a house template, raise
quality through hierarchy, alignment, chart grammar and copy, not new colours or fonts.

When building one, the page opens with the answer as its headline and the key figures ruled or banded in the
accent; every chart carries its annotation (target line, the event that explains a change); and the method
note uses the whole grid, in two columns or beside its table, never a half-width strip.

## What not to flag here

Dense tables in appendices; 12px chart ticks and table headers; locale number formats; a single
deliberate dark header band from the house template; the absence of a dark theme.
