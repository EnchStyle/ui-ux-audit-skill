# Profile: SaaS and Operational Dashboards

Data-dense tools used repeatedly by the same people: admin consoles, operations and revenue
dashboards, back-office tables, internal tools. These rules override the universal defaults.

Detection: dashboard, admin, console or back-office framing; screens dominated by KPI tiles, tables,
charts, filters and bulk actions; or the user saying so. For data pages that are read, presented or
printed rather than operated, use `profile-analytics-report.md`.

Source of truth: the theme or token file and the table and chart components, if available. Most
findings here route through `data-viz-tables.md`: treat its honesty rules as primary.

Simulation persona: an operator at the start of a shift with two minutes to answer "are we on track
and what needs attention", using mouse and keyboard on a laptop; a manager opening the same view on a
phone between meetings.

## Overrides: density is the feature

- **Density is correct here.** Do not flag "needs more breathing room"; airy layouts that push the
  data below the fold are the Warning.
- **Dense but scannable**: one row height, clear grouping, strict alignment. Touching text or no row
  separation is a Warning.
- **Type**: 12 to 14px for tables, labels, ticks and secondary data is correct. Flag only below 12px or
  failing contrast.
- **Pointer-first targets**: 32 to 40px controls with room around them are correct. Adjacent
  destructive row actions that are easy to mis-click are Critical.

## Overrides: honesty and comparability come first

- A selector that changes labels but not figures, figures that disagree, missing data drawn as zero,
  exaggerated axes: see `data-viz-tables.md` (Critical to Blocker).
- **One primary answer per view**; one tile anatomy; deltas with sign, magnitude and basis.
- **Freshness is visible**; a claimed refresh interval must be real.

## Overrides: keyboard efficiency

- Keyboard operability of core flows is a primary path; the universal defaults apply (a control
  keyboard users cannot reach is Critical; focus removed everywhere is a Blocker).
- Shortcuts are discoverable and never fire while typing in a field; single-key shortcuts can be
  turned off or remapped (SC 2.1.4).
- Focus order runs filters, then table, then row actions; focus always visible.

## Overrides: structure and state

- **Persistent navigation** with the current section clearly marked; breadcrumbs on drill-downs.
- **Filters and sort survive reload** when losing them discards real work (a long filtered
  investigation): Warning. Otherwise it is a suggestion, not a finding.
- **Bulk actions**: selection count, a header checkbox with an indeterminate state, "select all"
  disambiguated across pages, a toolbar that states how many rows it affects.
- **Destructive bulk actions** need confirmation and, where possible, undo: none of either is a
  Blocker.
- **Latency**: every server action shows pending and outcome; long jobs report progress.

## Visual quality for dashboards

Rate it like any page (`visual-excellence.md`). Exceptional dashboards feel calm: one dominant answer,
muted chrome, status colour used sparingly, strict alignment (one gutter, one tile anatomy, values on
one baseline, chart plot areas aligned to panel titles), and fewer boxes. Dark mode is not required
unless the product offers it; when it does, audit both themes.

## What not to flag here

Density itself; 12px data type; 32px pointer controls with spacing; terse domain abbreviations;
bracketed accounting negatives; fixed per-type decimal places; contained table scrolling on phones
with a visible cue.
