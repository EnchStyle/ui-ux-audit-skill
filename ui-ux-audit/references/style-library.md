# Style library: choose one, then hold it

A style here is a small, complete set of decisions (type, colour logic, spacing, shape, depth, imagery,
motion) that belong together. Use the library when the user names a style or a mood, when several pages or
products must look alike, and for reports and analyses, where a strict typographic style tested best. Using
one token block unchanged on every screen is what makes two builds of the same brief look alike and one flow
look like one product. For other new landing pages, dashboards and apps the art direction step in `SKILL.md`
decides the look (in this skill's blind tests it was preferred to a library style applied by rule); its
result is still written as a token block in the form used here and held in the same way.

**A house template or brand system always wins.** When the user has one, its fonts, colours and components are
the style: write "Style: house system" and use this file only to judge consistency. When the user gives only a
brand colour, choose a style below and replace its accent with that colour (check the contrast pairs again).

## The twelve styles

Each has its own file in `references/styles/`. Read only the one you choose.

| Style | File | In one line | Schemes |
|---|---|---|---|
| Swiss grid | `swiss-grid.md` | Strict grid, one grotesque, black and white with one signal colour, no corners or shadows | light |
| Editorial | `editorial.md` | A well-set publication: serif headlines, narrow measure, figures with findings | light |
| Quiet product | `quiet-product.md` | Neutral software: hairlines, small precise type, one sparing accent | light and dark |
| Dense console | `dense-console.md` | Instrument panel: maximum data, strict alignment, colour only for status | light and dark |
| Public-service plain | `public-plain.md` | Large plain type, one column, one thing per page, obvious controls | light |
| Soft friendly | `soft-friendly.md` | Rounded, tinted, gentle depth, approachable | light and dark |
| Neo-brutalist | `neo-brutalist.md` | Thick outlines, flat colour blocks, hard offset shadows, big type | light |
| Dark premium | `dark-premium.md` | A dark stage with one spotlight and one warm accent | dark |
| Warm craft | `warm-craft.md` | Warm paper, a soft serif, hand-made imagery, unhurried | light |
| Luxury minimal | `luxury-minimal.md` | Vast white space, a large high-contrast serif, almost no colour | light |
| Technical mono | `technical-mono.md` | Engineering drawing: monospace labels, grid lines, one working colour | light and dark |
| Glass layered | `glass-layered.md` | Solid content with translucent floating bars, as on current iPhone software | light and dark |

## Selection: the first row that matches wins

When a library style is wanted and the user has not named one, decide from the brief, the audience and the
content, never from taste. Go down the rows in order and take the first that fits; the second name is the alternative when the first is ruled out by the "Not for" line in its
file or by something the user said. The same brief must give the same style every time.

| # | The brief is | Style | Alternative |
|---|---|---|---|
| 1 | A form, application or step-by-step service for the general public or all staff | Public-service plain | Quiet product |
| 2 | A tool operated all day by trained staff where one screen must hold more than about 40 rows or figures, or the user asks for density | Dense console | Quiet product |
| 3 | Any other dashboard, admin or product screen | Quiet product | Swiss grid |
| 4 | A report or analysis read by managers, a board or clients, mostly charts and tables | Swiss grid | Editorial |
| 5 | A report or page that argues a case in prose, long reading | Editorial | Swiss grid |
| 6 | An iPhone or iPad app that follows the platform | Glass layered | Soft friendly |
| 7 | An Android app, or a consumer app for families and everyday tasks on any phone | Soft friendly | Quiet product |
| 8 | Marketing for developer tools, infrastructure, data or crypto analytics | Technical mono | Dark premium |
| 9 | A product launch or showcase where one product is the hero | Dark premium | Quiet product |
| 10 | Food, craft, wellness, an independent shop, hospitality with a homely tone | Warm craft | Soft friendly |
| 11 | Premium retail, fashion, architecture, high-end hospitality, a portfolio | Luxury minimal | Swiss grid |
| 12 | A creative studio, an event, a youth or indie brand that should be loud | Neo-brutalist | Swiss grid |
| 13 | Marketing for business software or a service | Swiss grid | Quiet product |
| 14 | Anything else | Swiss grid | Quiet product |

When the user names a style, a mood ("bold", "calm", "premium") or a reference, map it to the nearest style and
say so. Say the choice in one line of the hand-over: "Style: Swiss grid (row 4: a board report, mostly charts)".

## Make it this product's

A style is a foundation, not a finished design. Used as it comes, with its stock accent and no element of its
own, it is the template look in another costume: in this skill's blind tests, builds like that lost to builds
made with no style at all. Before any markup, write four lines as a comment under the token block and hold
them on every screen of the product:

1. **Accent.** The user's brand colour, or one hue from the subject's own world (the green of a pharmacy cross for a
   health service, safety yellow for a building site, the ink of a ticket) in place of the stock accent. Set `--accent` and
   `--accent-ink` once; the script checks the pairs.
2. **Focal point.** The one answer, figure or headline each screen leads with, in the style's largest or
   second-largest size; everything else on the first screen is clearly smaller.
3. **Signature.** One element built from this product's own content and seen nowhere else: the route
   map that redraws as a parcel moves, the seat plan that fills as tickets sell, the gauge that falls as stock runs down.
   It is content doing its job, never an ornament, and never initials in a circle standing in for a picture.
4. **Name.** The product's name with presence: a wordmark in the display face (with a simple glyph if it
   helps) in a header that carries the accent or the ink colour.

Status has its own tokens: a late job is `--bad` and says "late"; it is never painted in the accent.

## Holding the style

1. Paste the style's token block as the first thing in the style sheet, with the product's accent. Components
   use only its variables: no new colour, size, radius or shadow is typed anywhere else.
2. Every screen of a flow, and every later page of the same product, carries the same block unchanged. Pass
   all screens to `uicheck.py` in one call; it prints `style-drift` when fonts, radii, sizes or shadows differ.
3. Styles marked "light and dark" include both sets; dashboards, reports and apps use both through
   `prefers-color-scheme`. Styles marked with one scheme stay in it.
4. Follow the "expensive" list and avoid the "cheap" list in the file; they are the difference between the
   style and a costume of it.
5. A library (charts, components) is themed to the tokens before it is used; see `libraries.md`.
6. Do not blend two styles. If the brief truly needs a second voice (a marketing page and its app), use two
   styles on two surfaces, never on one screen.

## In an audit

Name the style the page is closest to in the report header ("Style: Neo-brutalist", "house system" or "none
recognisable"). A style's own conventions are not findings: sharp corners, thick borders, very large type, a
dark page, dense rows, a narrow column. Variation inside the page is: two radius families, three greys with
no role, a second accent. A page with no recognisable style and several template tells is what
`visual-generic` and the rating describe.

## Why these twelve

They are the distinct directions found in current, documented practice, not a list of fashions:

- Grid-led, typographic design systems for products and reports: IBM Carbon separates a "productive" type set
  for product screens from an "expressive" one for editorial pages (Dense console, Quiet product, Editorial).
  https://carbondesignsystem.com/elements/typography/overview/
- Public services: the GOV.UK Design System's large type scale (19px body) and one thing per page
  (Public-service plain). https://design-system.service.gov.uk/styles/type-scale/
- Neutral product design systems with a grid, one typeface family and a high-contrast neutral palette, for
  example Vercel's Geist (Quiet product, Technical mono). https://vercel.com/geist/introduction
- Platform styles: Apple's Liquid Glass for the control layer (Glass layered) and Material 3 with dynamic
  colour and rounded shapes on Android (Soft friendly).
  https://developer.apple.com/design/human-interface-guidelines/materials
  https://developer.android.com/develop/ui/compose/designsystems/material3
- Named visual trends with published usability guidance: neobrutalism and glassmorphism (Nielsen Norman Group,
  2025 and 2024). https://www.nngroup.com/articles/neobrutalism/ https://www.nngroup.com/articles/glassmorphism/
- Typographic rules shared by all of them (body 15 to 25px, 45 to 90 characters per line, line spacing 120 to
  145%): Matthew Butterick, Practical Typography. https://practicaltypography.com/summary-of-key-rules.html

These sources were studied for principles. No style here reproduces a product's design, brand or assets: the
palettes and token values are this skill's own, and each palette's contrast is computed in its file.
All checked 26 November 2026.
