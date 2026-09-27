# Changelog

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
