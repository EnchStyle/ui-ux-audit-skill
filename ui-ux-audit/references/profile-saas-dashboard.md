# Profile: SaaS and Operational Dashboards

Severities are set only in `severity-registry.md`; the codes in brackets below are its rows.

Data-dense tools used repeatedly by the same people: admin consoles, operations and revenue
dashboards, back-office tables, internal tools. These rules override the universal defaults.

Detection: dashboard, admin, console or back-office framing; screens dominated by KPI tiles, tables,
charts, filters and bulk actions; or the user saying so. For data pages that are read, presented or
printed rather than operated, use `profile-analytics-report.md`.

Main task: see whether things are on track and act on what needs attention.

Source of truth: the theme or token file and the table and chart components, if available. Most
findings here route through `data-viz-tables.md`: treat its honesty rules as primary.

Simulation persona: an operator at the start of a shift with two minutes to answer "are we on track
and what needs attention", using mouse and keyboard on a laptop; a manager opening the same view on a
phone between meetings.

## Overrides: density is the feature

- **Density is correct here.** Do not flag "needs more breathing room"; airy layouts that push the
  data below the first screen are the fault here (`other`, Warning).
- **Dense but scannable**: one row height, clear grouping, strict alignment. Touching text or no row
  separation is `other`, Warning.
- **Type**: 12 to 14px for tables, labels, ticks and secondary data is correct. Flag only below 12px or
  failing contrast.
- **Pointer-first targets**: 32 to 40px controls with room around them are correct. A destructive row action
  directly beside another action with no separation is `other`, Warning; with no confirmation either it is
  `destructive-no-confirm`.

## Overrides: honesty and comparability come first

- A selector that changes labels but not figures, figures that disagree, missing data drawn as zero,
  exaggerated axes: see the Honesty and data rows of the registry. On this profile `chart-axis` is a Blocker and
  `chart-colour-only` is Critical.
- **One primary answer per view**; one tile anatomy; deltas with sign, magnitude and basis.
- **Freshness is visible** (`stale-data`); a claimed refresh interval must be real.

## Overrides: keyboard efficiency

- Keyboard operability of core flows is a primary path; the general rules apply.
- Shortcuts are discoverable and never fire while typing in a field; single-key shortcuts can be
  turned off or remapped (SC 2.1.4).
- Focus order runs filters, then table, then row actions; focus always visible.

## Overrides: structure and state

- **Persistent navigation** with the current section clearly marked (`nav-current`); breadcrumbs on drill-downs.
- **Filters and sort survive reload** when losing them discards real work (a long filtered
  investigation): `other`, Warning. Otherwise it is a suggestion, not a finding.
- **Bulk actions**: selection count, a header checkbox with an indeterminate state, "select all"
  disambiguated across pages, a toolbar that states how many rows it affects.
- **Destructive bulk actions** need confirmation and, where possible, undo (`destructive-no-confirm`).
- **Latency**: every server action shows pending and outcome; long jobs report progress.

## Visual quality for dashboards

Rate it like any page (`visual-excellence.md`). Exceptional dashboards feel calm: one dominant answer,
muted chrome, status colour used sparingly, strict alignment (one gutter, one tile anatomy, values on
one baseline, chart plot areas aligned to panel titles), and fewer boxes. Dark mode is not required
unless the product offers it; when it does, audit both themes.

When building one, the first screen opens with the answer in words and a number, with its parts beside it in
the status colours. Next comes one view shaped like the work (Depth and finish in `visual-excellence.md`), then
the filters as one quiet row above the full list. Filters never push the answer down, and every status keeps
one mark in every view.

## What not to flag here

Density itself; 12px data type; 32px pointer controls with spacing; terse domain abbreviations;
bracketed accounting negatives; fixed per-type decimal places; contained table scrolling on phones
with a visible cue.
