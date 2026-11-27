# Changelog

## 3.0.0 (2026-11-27)

- **Severity registry** `references/severity-registry.md`: 95 codes, each with one test, one severity and one tie-break. It replaces severity statements that were spread over 14 files and contradicted each other in places.
- **Measuring script** rewritten: check names equal registry codes; it clicks every control, walks the tab order, emulates iPhone and Android with safe areas, and checks dark, print, loading, empty and error views. It lists 83 of 117 planted test defects against 61 before.
- **Two new scripts:** `reportcheck.py` checks a report's format, codes and arithmetic before it is sent; `shotcheck.py` measures screenshots when there is no code.
- **Mobile:** `references/mobile.md` and a mobile app profile, with each platform figure cited and dated.
- **Build mode:** token block first, a usability plan, state views, a section on depth and finish (every section shows something, the heading states the answer, one view made for the data, status designed), and a rule never to recall a library from memory.
- **Style library:** twelve named styles with token blocks and computed contrast, for named styles, matching series and reports.
- **New references:** `usability.md`, `libraries.md`, `style-library.md` and `styles/`.
- **Switches:** the options of one segmented control or toggle get one width (`segment-widths`): a registry row, a script check and a build rule.
- **Fit of controls and scroll areas** (from feedback of a project that used the skill): three registry codes with script checks, `control-overflow` (a control wider than the box around it), `scroll-unexpected` (scrolling that no style rule asked for, or a scroll area stretched by elements nobody sees) and `scroll-nested`; the sticky header check now tests the effect.
- **Fonts and scrollbars:** when a font the page asks for is not installed, the script repeats the fit checks with a font of the same widths where one exists, otherwise with a wider font of the same kind as an upper bound; a further pass draws 15px scrollbars. Reports name the browser, the fonts drawn and the scrollbars, and never list fit as clean when the real font was not drawn.
- **Evidence for the eye:** close-ups at twice the size, one sheet per width, and a screenshot of every scroll area scrolled to its end.
- **Changes to an existing page:** `uicheck.py --baseline` compares with the page before the change; build mode measures before and after, also for small repairs, and has rules for a house style sheet laid over an existing page and for text that only screen readers get.
- **Tests:** `tests/` holds five acceptance tests with their pages (`python3 tests/run_tests.py`).
- **Corrections** to four factual statements: lists of links are not covered by the inline exception to the 24px target rule; relative luminance uses the threshold 0.04045; EN 301 549 is given with both its cited version (3.2.1) and the newer one; subgrid support is dated (every major browser since September 2023).
- Test results in the README. Audits: 584 of 585 planted defects found over 40 runs, no finding on the clean page. Builds: preferred to 2.0.0 builds in 44 of 54 blind judgements.

## 2.0.0 (2026-09-26)

- **Measuring script** `scripts/uicheck.py`: renders at 360, 768 and 1280px and measures 25 checks, including alignment faults (lone grid items, card rows and tile values off a shared line, control heights, nested radii, near-miss edges, padding asymmetry, media ratios, gutters, chip and icon sizes, sticky headers) plus a census of radii, shadows, type sizes and section paddings.
- **Alignment and consistency** reference with a global system block (type scale, spacing, gutters, radii, control heights, media ratios) and a measured check for each fault.
- **Visual quality** reference: rating scale, AI default looks (including the generic SaaS look), moves per page type. Scored on landing pages; advice on dashboards, reports, shops and apps.
- **Build mode** replaces prevention: art direction from three sketched directions, global system first, every figure computed and checked twice, measure-and-fix loop, cold self-review.
- **Precision:** new "What not to flag" rules (static-page wiring, latent issues, house font floors, WCAG 2.5.8 and 1.4.11 exceptions, missing dark mode, deliberate choices) and default severities for about 30 common findings. Scoring caps Polish at 5 points.
- **New profile:** analytics reports. Kids-app profile renamed `profile-kids-app.md`; all profiles updated.
- **Corrections:** `overflow-wrap: anywhere` over `break-word`, accurate `text-wrap` support, subgrid first, axe-core does not catch removed focus rings, current WCAG 2.2, EN 301 549 and European Accessibility Act status.
- Reference files reorganised: `consistency-tokens-nav.md` split into `alignment-consistency.md` and `navigation-icons.md`; `anti-slop-copy.md` split into `visual-excellence.md` and `content-honesty.md`.
- Benchmark results in the README.

## 1.1.0 (2026-06-15)

- New **simulate-the-user-first** method (`references/user-simulation.md`): walk the flow as the target user, a constrained user, and an edge-case-data user before the category sweep. It catches experiential failures a static scan misses (contradictory states, mislabelled scope, happy-path-only flows). Wired into the full-audit procedure.
- Three new **bundled category profiles**: SaaS / dashboard, marketing / landing, and e-commerce. The skill now switches profile by product type, with the universal defaults as the fallback.
- **Layout:** added the "fixed-width sibling starves a text column" rule (the fix is width, not `break-words`) to the typography/layout reference.
- Profiles standardised to a `profile-*.md` naming convention; profile section and README updated to list all bundled profiles.

## 1.0.0 (2026-06-10)

Initial public release.

- 15 audit categories across 10 reference files
- Three modes: full scored audit, quick review, silent prevention during UI coding
- Severity rubric (Blocker/Critical/Warning/Polish) with 0-100 scoring and verdict bands
- Durable-fix tooling map (lint rules and automated tests per failure family)
- Worked examples anchoring the finding format and report shape
- Example kids-app project profile doubling as a profile template
