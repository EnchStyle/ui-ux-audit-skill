# Category 16: Charts, Tables and Dashboards

Data UI fails on precision, comparability and honesty, and sample data rarely stresses any of them.
Recompute every figure that appears more than once; check that every control changes what it claims
to change.

## Honesty (Blocker on analytics products, Critical elsewhere)

- **Axes**: bar and column charts start at zero. A line chart may zoom its value range when the range
  is stated on the chart ("axis from 40 to 60"); an unstated truncated axis that exaggerates a
  difference is a Blocker on analytics products.
- **Figures that should agree, agree**: a headline tile, the table total and the text quoting it are
  the same number. A mismatch means one of them is wrong.
- **Controls do what they say**: a period or market selector that changes a label but not the data, or
  applies to some widgets while claiming to apply to all, is Critical.
- **Missing data is not zero**: an empty series is an explicit empty state ("No readings from the north
  sites since 06:00"), never a flat line at zero or a tile reading "0 MW".
- **Deltas** show direction by sign or arrow as well as colour, with magnitude and basis ("+4.2% vs
  prior 7 days").

## Charts

- **A title that states the point** ("Spot price peaked at 142 £/MWh on Tuesday") or at least what is
  measured; axis titles with units; sensible tick density at every width. A chart missing its title,
  axis titles, units or text alternative is one Warning finding per chart.
- **Series**: colourblind-safe and distinguishable without colour (direct labels at line ends, markers
  or dash patterns); past about six series, group, filter or use small multiples. The same series keeps
  the same colour in every chart. Series told apart only by colour, or marks below 3:1: Critical on
  analytics products, Warning elsewhere.
- **Room for labels**: the plot area starts after the widest tick label, lines never run through axis
  labels, and direct labels that would collide are offset with leader lines or moved to a legend.
- **Semantic colour locked**: if green means good, it means good everywhere; whether "up" is good
  depends on the metric (rising churn is bad), so colour follows meaning, not direction.
- **Contrast of marks**: lines and bars that carry meaning need 3:1 against the background, in every
  theme.
- **Sparklines** carry an anchor: the current value, and a baseline or min and max.
- **Responsive**: charts redraw at their container's width; labels stay at 12px or more; legends
  move below; tick counts drop. A chart with a fixed pixel width that overflows is Critical.
- **Tooltips** work with touch and keyboard, not only hover, and do not clip at the edges.
- **Text alternative**: a caption stating the finding, or an accessible data table.

## Tables

- **Alignment by type**: numbers right-aligned with tabular figures and headers aligned the same way;
  text left; never centred data columns.
- **Units in the header** ("Amount (USD)"), not repeated in every cell.
- **Sticky header** on tables longer than about 15 rows (`thead th { position: sticky; top: 0 }`),
  so scrolled rows keep their meaning (uicheck `table_sticky`): Warning. A sticky identifying column
  on very wide tables is a bonus.
- **Sort state visible** (column and direction, plus `aria-sort`).
- **One separator strategy** (zebra, hairlines or space), consistent row height.
- **Truncated values recoverable** (hover, focus, copy); middle ellipsis for addresses and hashes,
  where both ends carry meaning.
- **One number format per metric**: thousands separators, fixed decimals per data type, locale-aware.
  Three precisions for the same metric on one screen is Critical.
- **States**: skeleton rows while loading; an empty result that says why and differs from an error;
  pagination or virtualisation beyond a few hundred rows.
- **Phones**: a contained horizontal scroller with a visible cue, or rows collapsed into cards.

## Dashboards

- **One primary answer per view**: the most important metric dominates; twelve equal tiles is
  overchoice (Warning).
- **One tile anatomy**: label, value, change, timeframe, always in the same positions and format.
- **Comparable things share scales and timeframes**, or state the difference.
- **Freshness** shown ("Updated 14:32"); silent staleness on operational or financial data is Critical,
  and a "refreshes every 5 minutes" claim that never refreshes is a false statement.
- **Precision restraint**: show the precision that supports the decision, from one central formatter.
- **Live data**: fixed-width, tabular values so layouts do not breathe; brief, throttled change
  highlights; new rows never steal the scroll position.
