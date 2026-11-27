# ui-ux-audit

A Claude skill that audits and builds interfaces: web pages, dashboards, analytics reports, shops and mobile apps. It measures the rendered page instead of guessing, scores findings from one fixed table, and raises landing pages, dashboards and reports from competent to distinctive.

Almost every AI interface failure has one root cause: the model generates a plausible static snapshot of a single state (the happy path, on desktop), cannot see the rendered result, and carries no design system from one generation to the next. The output looks right in a screenshot and breaks when content grows, the viewport shrinks, an error occurs, or a second component arrives with slightly different padding. This skill forces all of that into view.

## What it does

Three modes, chosen from how you ask:

1. **Full audit.** "Run a full UI audit" or "is this ready to ship". Claude runs the measuring script (360, 768 and 1280px, or an iPhone or Android device), walks the main task, then goes down the severity registry: one test, one severity and one tie-break per code. The report has a 0 to 100 score, a verdict, findings by severity, a visual quality rating, and the fixes that stop each failure returning. A second script checks the report's format and arithmetic before it is sent.
2. **Quick review.** "Why does this card look off". Two to five findings, no score.
3. **Build.** When Claude creates or restyles a page, dashboard, report or app screen, it sets an art direction, writes one token block first (type scale, spacing, radii, control heights, colours with computed contrast), plans the task and the state views, computes every figure, then measures and fixes until the script lists nothing.

### Scripts

| Script | What it does |
|---|---|
| `scripts/uicheck.py` | Renders a page or a flow of screens and lists candidates under registry codes: overflow, contrast, target sizes, unnamed controls, focus, clipped text, widows, card rows and tile values off a shared line, control heights, switch options of different widths, nested radii, near-miss edges, heading proximity, table alignment, safe areas and more. It also clicks every control, walks the tab order, and checks dark, print, loading, empty and error views. Fit is measured three times: in the main pass, in a font pass when a font the page asks for is not installed, and in a pass with 15px scrollbars. It reports a control wider than its box (`control-overflow`), scrolling nobody asked for (`scroll-unexpected`), a scroll area inside another (`scroll-nested`) and a sticky table header that scrolls away. It writes close-ups of controls and box edges at twice the size and a screenshot of every scroll area scrolled to its end, and with `--baseline` it compares a page with its state before a change. It lists candidates; Claude confirms each one. |
| `scripts/reportcheck.py` | Checks a full-audit report before it is sent: format, codes, allowed severities, length and the score arithmetic. |
| `scripts/shotcheck.py` | Measures screenshots when there is no code: contrast, sizes and safe areas, marked as estimates. |

Requirements: Python 3 with Playwright and Chromium (`pip install playwright`, then `playwright install chromium`). `shotcheck.py` needs Pillow, and for its text checks the tesseract program with the pytesseract module; without them it runs the remaining checks and says so.

### Finding format

```
**C2 [contrast-text] Hero subline is too pale to read** (`.hero p`; 360, 768, 1280)
**Found:** the fact, with the measurement or the code line
**Why:** who it hurts and how, one line
**Fix:** the smallest concrete change
```

## Test results (v3.0.0 against v2.0.0)

Measured on eight purpose-built test interfaces (117 planted defects on six of them, one clean page, one deliberately unconventional page), five fresh-context audits per interface and version, scored against answer keys:

| Measure | v2.0 | v3.0 |
|---|---|---|
| Planted defects found | 97.8% (572 of 585) | 99.8% (584 of 585) |
| Blocker and Critical defects found | 98.5% (266 of 270) | 100% (270 of 270) |
| Findings that are real (arguable ones counted as wrong) | 97% (590 of 609) | 99% (590 of 595) |
| Score range across five runs, worst interface | 12 points | 3 points |
| Clean page: runs with a finding above Polish | 1 of 5 | 0 of 5 |
| Reports that follow the required format | 10 of 28 measured | 40 of 40 |
| Planted defects listed by the measuring script | 61 of 117 | 83 of 117 |

Build mode: seven briefs and 27 pairs of builds, each pair judged twice with the sides swapped. Blind judges preferred the v3.0 build to the v2.0 build in 44 of 54 judgements (landing pages 18 of 24, dashboards 14 of 18, board report 6 of 6, iPhone app 6 of 6), and to a build made with no skill in 42 of 42.

After the last changes to the text, 32 further audits: every planted defect found except one Polish item missed once, and both clean pages scored 100 in six of six runs.

Two faults reported from a real project (a switch wider than its box once the real font is drawn, and a fixed panel that scrolls for thousands of pixels because of hidden screen-reader text) were rebuilt as test pages. The earlier script passed both; the script now reports both, with no new candidate on the 13 test pages. In 13 further audits the two faults were found in 7 of 7 audits of those pages and the clean pages scored 100 in 5 of 5. The pages and a test runner are in `tests/` (`python3 tests/run_tests.py`, 5 tests).

Limits of this evidence: test interfaces, answer keys, builders and judges are AI models; 27 pairs of builds put the true preference rate between about 58% and 91%; nothing was tested on a real phone or with a screen reader; fonts on the test machine were stand-ins, and the font pass gives an upper bound, not the real font; no page was built from nothing with the text as changed after the project feedback, so the build figures belong to the text before it.

## Install

### Claude (web, desktop, mobile)

1. Download `ui-ux-audit.skill` from this repository (it is a ZIP archive of the `ui-ux-audit/` folder).
2. In Claude, open your skills list (**Customize > Skills**, or **Plugins > Skills**, depending on the app version), add a skill by upload and choose the file.
3. If an older version is installed, do not add a second copy: open the skill's **...** menu and choose **Upload new version**. It replaces all files of the skill and keeps earlier versions in its version history.

Skills need code execution to be enabled. Help: https://support.claude.com/en/articles/12512180-use-skills-in-claude

### Claude Code

Copy the `ui-ux-audit/` folder into your skills directory:

```bash
# personal (available in all projects)
mkdir -p ~/.claude/skills && cp -r ui-ux-audit ~/.claude/skills/

# or project-scoped (committed with the repository)
mkdir -p .claude/skills && cp -r ui-ux-audit .claude/skills/
```

The skill follows the open SKILL.md Agent Skills standard, so it also works in other coding agents that support the format.

## Use

- "Run a full UI audit" on pasted code, project files or screenshots
- "Review this component", "fix the spacing", "is this ready to ship"
- "Build a dashboard for ...", "restyle this in Swiss grid"

Screenshot-only input is supported with reduced confidence: sizes are estimates and the verdict is provisional.

## Profiles and styles

Six product profiles change the defaults for a kind of product: marketing and landing (including pricing), SaaS and operational dashboards, analytics reports, e-commerce, mobile apps, and children's learning apps. To add one, copy an existing `references/profile-*.md`, keep its structure and register it in the Profiles section of `SKILL.md`.

Twelve named styles, each a token block with computed contrast: Swiss grid, Editorial, Quiet product, Dense console, Public-service plain, Soft friendly, Neo-brutalist, Dark premium, Warm craft, Luxury minimal, Technical mono, Glass layered. They are used when you name a style, when a page must match a series, and for reports; otherwise build mode sets its own art direction.

## Structure

```
ui-ux-audit/
├── SKILL.md                              modes, measuring, registry pass, scoring, report, build mode
├── scripts/
│   ├── uicheck.py                        measuring script (Playwright and Chromium)
│   ├── reportcheck.py                    report format and arithmetic check
│   └── shotcheck.py                      screenshot measuring script
└── references/
    ├── severity-registry.md              every code: test, severity, tie-break
    ├── visual-excellence.md              visual quality rating; depth and finish for build mode
    ├── usability.md                      build rules and audit checks for the main task
    ├── style-library.md                  twelve styles, selection table, hold rule
    ├── styles/                           one token block per style (12 files)
    ├── mobile.md                         iPhone and Android rules, cited and dated
    ├── libraries.md                      verified libraries; never recall one from memory
    ├── alignment-consistency.md
    ├── structure-typography.md
    ├── color-states-forms.md
    ├── interaction-responsive-a11y.md
    ├── navigation-icons.md
    ├── motion-performance.md
    ├── content-honesty.md
    ├── data-viz-tables.md
    ├── user-simulation.md
    ├── durable-fixes.md
    ├── examples.md
    └── profile-*.md                      six product profiles
```

The core file loads on every trigger; reference files load only when needed.

`tests/` is part of this repository, not of the skill: five acceptance tests for the measuring script with their pages. Run them with `python3 tests/run_tests.py`.

## Credits

Patterns informed by Anthropic's skill-creator and frontend-design skills, Leonxlnx/taste-skill, and community design-audit skills. Standards referenced: WCAG 2.2, EN 301 549, Apple Human Interface Guidelines, Android and Material guidance, Core Web Vitals.

## License

MIT
