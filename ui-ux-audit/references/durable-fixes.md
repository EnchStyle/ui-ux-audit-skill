# Durable Fixes: stop failures coming back

A finding fixed by hand returns the next time code is generated; a finding fixed by tooling stays
fixed. End each full audit with the one to three tools that would prevent the largest failure families
found, matched to the stack. Many people using this skill direct AI tools rather than write code, so
give each as the one-line instruction to paste into a coding assistant, not raw configuration.

| Failure family (categories) | Tool | Instruction to give the assistant |
|---|---|---|
| Alignment and consistency drift: card rows, baselines, orphans, widows, control heights, radii, gutters (10) | This skill's `scripts/uicheck.py` in a pre-commit or CI step | "Run uicheck.py on every page before commit and fail when card_rows, baselines, control_heights, grid_orphans, nested_radius or heading widows are not empty." |
| Layout breaks at 360px, visual regressions (2, 8, 10) | Playwright screenshot tests | "Add Playwright visual tests that screenshot each page at 360, 768 and 1280px with long-content fixtures and fail on unexpected changes." |
| Runtime accessibility: names, contrast, landmarks (4, 9) | axe-core via Playwright | "Add an accessibility test that runs axe-core on every page and fails on violations." |
| Removed focus rings (9) | A grep or stylelint rule | "Fail the build when CSS sets outline: none or outline: 0 without a :focus-visible replacement." (axe-core does not detect this.) |
| Off-scale values, raw colours, one-off radii (2, 10) | Design tokens plus stylelint (plain CSS) or eslint-plugin-tailwindcss (Tailwind) | "Move every colour, radius, shadow, gap and control height into CSS custom properties at :root and add a lint rule that fails on raw hex values and off-scale pixel values in components." |
| JSX accessibility: alt text, labels, click handlers on divs (5, 6, 9) | eslint-plugin-jsx-a11y (React only) | "Add eslint-plugin-jsx-a11y with the strict config and fix what it reports." |
| Markup validity in plain HTML (9) | html-validate | "Run html-validate on every HTML file in CI." |
| Layout shift and slow loads (13) | Lighthouse CI | "Add Lighthouse CI with budgets: CLS 0.1, LCP 2.5s; fail when exceeded." |
| Inconsistent number and date formats (16) | One formatting module | "Create one module wrapping Intl.NumberFormat and Intl.DateTimeFormat and replace every inline toFixed or hand-built string with it." |
| Broken flows: forms, dialogs, filters that do not filter (5, 6, 16) | Playwright functional tests | "Write Playwright tests that submit each form with valid and invalid data, open and close each dialog with mouse and keyboard, and check that each filter changes the figures it claims to change." |

Rules: one recommendation per failure family; proportionate to the project (a one-page prototype gets
the single most useful tool); ordered by how many findings each would have prevented; never a tool
that does not fit the stack. When the same family returns in a later audit, installing its tool
becomes the top priority.
