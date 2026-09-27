# ui-ux-audit

A Claude skill that audits web UI for the failures AI consistently ships, measures the render instead of guessing, and raises landing pages, dashboards and analytics pages from competent to exceptional.

Almost every AI UI failure traces back to one root cause: the model generates a plausible static snapshot of a single state (the happy path, on desktop), it cannot see the rendered result, and it carries no persistent design system across generations. The output looks right in a screenshot and breaks the moment content grows, the viewport shrinks, an error occurs, or a second component is generated with slightly different padding. This skill forces all of that into view.

## What it does

Three modes, chosen automatically from how you ask:

1. **Full audit.** "Run a full UI audit" or "is this ready to ship". Claude renders the page with the bundled measuring script (`scripts/uicheck.py`, Python Playwright) at 360, 768 and 1280px, walks the flow as the real user, a constrained user and an edge-case-data user, then sweeps 16 categories. The report gives a 0-100 score with the arithmetic shown, a ship verdict, findings by severity (Blocker 12, Critical 8, Warning 4, Polish 1, with Polish capped at 5 points), a visual-quality rating with concrete improvements, and the tools that stop each failure family returning.
2. **Quick review.** "Why does this card look off". Two to five findings, no score.
3. **Build.** When Claude creates or restyles a page, dashboard or report, it chooses a distinctive art direction, writes one global design system first (type scale, spacing, gutters, radii, control heights, media ratios), computes and double-checks every figure, then measures and fixes until the checks are clean.

The 16 categories: typography, layout and spacing, visual hierarchy, colour and contrast, component states, forms, touch, responsive behaviour, accessibility (WCAG 2.2), alignment and consistency, navigation and icons, motion, performance, visual quality, content and honesty, and charts, tables and dashboards.

### Alignment and consistency

The skill holds every element to one global system and measures the faults people notice at once but AI tools miss: headings a few pixels off the grid, a lone card on the last row, prices or KPI values off a shared line, a 40px input beside a 48px button, inner corners that do not follow the outer card, mixed media ratios, drifting gutters, chip and icon sizes, and single words alone on a heading line.

### Measuring script

`scripts/uicheck.py page.html --json checks.json --shots shots/` reports overflow, contrast, target sizes, unnamed controls, invisible focus, unsized media, heading order, small text, widows, lone grid items, card rows and tile values off a shared line, control heights, nested radii, near-miss edges, padding asymmetry, media ratios, icon and chip sizes, gutters, table alignment, missing sticky headers, heading proximity, and a census of radii, shadows, font sizes and section paddings. It measures; Claude judges.

Requirements: Python 3 with Playwright and Chromium (`pip install playwright`, then `playwright install chromium`). It accepts a local HTML file or an http(s) URL; `--dark` checks the dark theme and `--widths` changes the widths.

### Finding format

```
**C2. Delta direction shown by colour alone** (`#kpi-grid .delta`, 12 tiles)
**Found:** what is wrong, with the measurement or snippet
**Why:** who it hurts
**Fix:** the smallest concrete change
**Prevent:** the tool or rule that stops recurrence
```

## Benchmark (v2.0.0)

Measured on 15 purpose-built test pages (98 planted faults, 3 clean controls), 3 runs per version, graded blind against answer keys:

| Measure | No skill | v1.1 | v2.0 |
|---|---|---|---|
| Planted faults found | 86% | 97% | 99% |
| Blocker and Critical faults found | 95% | 100% | 100% |
| Scored findings (Warning and above) that are real | 74% | 72% | 97% |
| Decoys wrongly flagged per audit | 0.56 | 0.69 | 0.11 |
| Serious false alarms on clean pages | 0.56 | 0.22 | 0 |
| Severity judged right | 80% | 89% | 96% |
| Score spread across repeat runs (mean) | 12.6 | 7.0 | 4.9 |
| Subtle alignment faults found | 85% | 89% | 98% |

Build mode (landing page and dashboard briefs, 3 builds each, two blind judges): overall 7.5 against 7.0 without the skill on the landing page, and 7.7 against 6.8 on the dashboard. Cost per audit is about the same as v1.1 and about 20% above no skill. Caveats: test pages, answer keys and graders are AI-built; fonts were stand-ins.

## Install

### Claude.ai (web, desktop, mobile)

1. Download `ui-ux-audit.skill` from this repository (or from Releases).
2. In Claude, open Settings, find Skills, and upload the file.
3. If you do not see a Skills section, check availability for your plan at https://support.claude.com

### Claude Code / Claude Desktop

Copy the `ui-ux-audit/` folder into your skills directory:

```bash
# personal (available in all projects)
mkdir -p ~/.claude/skills && cp -r ui-ux-audit ~/.claude/skills/

# or project-scoped (committed with the repo)
mkdir -p .claude/skills && cp -r ui-ux-audit .claude/skills/
```

Run `/skills` in Claude Code to confirm it loaded. Docs: https://code.claude.com/docs/en/skills

The skill follows the open SKILL.md Agent Skills standard, so it also works in other coding agents that support the format.

## Use

- "Run a full UI audit" on pasted code, project files, or screenshots
- "Review this component" / "fix the spacing" / "is this ready to ship"
- Or just let it work: it guides Claude automatically during any UI coding

Screenshot-only input is supported with reduced confidence (visual checks only, sizes as labeled estimates).

## Customize: project profiles

Profiles override the universal defaults for a kind of product. Five ship in the box: marketing and landing (including pricing), SaaS and operational dashboards, analytics reports, e-commerce, and children's learning apps. When a project has a house template or brand system, the skill audits within it and raises quality through hierarchy, alignment and copy rather than new fonts or colours. To add a profile, copy an existing `references/profile-*.md`, keep its structure (a `Detection:` line, a source-of-truth note, a simulation persona, `## Overrides:` sections) and register it in the Project profiles section of `SKILL.md`.

## Structure

```
ui-ux-audit/
├── SKILL.md                              modes, measuring, severity defaults, scoring, reports, build mode
├── scripts/
│   └── uicheck.py                        measuring script (Python Playwright + Chromium)
└── references/
    ├── alignment-consistency.md          global system block and alignment checks (category 10)
    ├── visual-excellence.md              visual-quality rating, AI default looks, moves per page type (14)
    ├── user-simulation.md                walk the page as the user
    ├── structure-typography.md           categories 1-3
    ├── color-states-forms.md             categories 4-6
    ├── interaction-responsive-a11y.md    categories 7-9
    ├── navigation-icons.md               category 11
    ├── motion-performance.md             categories 12-13
    ├── content-honesty.md                category 15: fake content, dark patterns, copy, localisation
    ├── data-viz-tables.md                category 16
    ├── durable-fixes.md                  failure-to-tooling map
    ├── examples.md                       worked findings and report shapes
    ├── profile-marketing-landing.md
    ├── profile-saas-dashboard.md
    ├── profile-analytics-report.md
    ├── profile-ecommerce.md
    └── profile-kids-app.md
```

The core file loads on every trigger; reference files load only when needed.

## Credits

Built from research across the Claude skills ecosystem. Patterns informed by Anthropic's skill-creator and frontend-design skills, Leonxlnx/taste-skill, and community design-audit skills. Standards referenced: WCAG 2.2, EN 301 549, Apple HIG, Core Web Vitals.

## License

MIT
