# Profile: Marketing and Landing Pages (including pricing)

Severities are set only in `severity-registry.md`; the codes in brackets below are its rows.

Public pages whose job is to make a stranger understand a value and take one action: home, product,
feature, campaign and pricing pages. The reader is unconverted, impatient and often on a phone. These
rules override the universal defaults; everything else keeps its universal rule.

Detection: hero sections, marketing copy, pricing tables, lead-capture or newsletter forms, routes
such as /, /pricing, /product, /features, or the user saying so.

Main task: a stranger understands the offer and takes the one main action.

Source of truth: find the page's single conversion goal first (the primary CTA). Judge every element
by whether it advances that goal. If the goal is unclear from the page, that is the first finding.

Simulation persona: a potential customer arriving from a search or an ad, on a phone, giving the page
ten seconds to answer "what is this, is it for me, what do I do next".

## Overrides: one message, one action

- **The first screen answers what, for whom and what next**, at 1280 × 800 and 360 × 740: a headline
  that says what the product does (two to eight words), a subline of about twenty words, one dominant
  CTA (`purpose-unclear`, `primary-action`). The script captures both first screens.
- **One primary CTA.** Two equally weighted primary buttons split intent (`primary-action`). Demote the
  rest to secondary styling.
- **Same action, same label**: repeating the primary CTA down the page is correct; three labels for one
  destination is `term-drift`.
- **The CTA keeps its promise**: "Start free trial" leads to a trial, not a newsletter (`cta-mismatch`).

## Overrides: proof must be real

- **Unsourced precise numbers, testimonials, customer logos and faked product screens** on a page presented as
  real are `unsourced-claim` and `placeholder-content` (see `content-honesty.md`).
- **Logo walls** hold real marks the company can show a relationship with, without captions under
  each.

## Overrides: visual quality is part of the job

- The page is the brand's flagship: rate visual quality and give moves in every audit
  (`visual-excellence.md`). The AI default look makes the brand invisible (`visual-generic`); ground the
  replacement in the product.
- **Section shapes vary**; the hero shows the product; each feature and each step shows the product doing
  that job as a small view built from sample content (labelled once as an example), not an icon above a
  paragraph; one accent; one radius and shadow system; every
  card row and plan row aligned (`alignment-consistency.md`). Plan cards whose buttons or prices sit
  at different heights are `card-rows` at Critical, because buyers compare them.

## Overrides: pricing

- **Every price shows currency, billing period and VAT treatment** ("€24 per editor per month, excl.
  VAT"). Missing period or VAT: `price-unclear`.
- **The recommended plan is marked in text** ("Recommended"), not by colour or border alone (`other`, Warning).
- **Discount arithmetic is correct**; struck-through prices are real prior prices.
- **Urgency is real**: timers that reset and offers that never end are `dark-pattern`.
- **A requested set of plan tiers** is not the "three identical cards" tell.

## Overrides: performance is conversion

- **Unsized hero media or layout shift on load** moves the CTA under the cursor (`media-unsized`).
- **The hero image is the largest paint**: modern format, responsive `srcset`, `fetchpriority="high"`,
  budget about 200 KB; no autoplaying background video without a poster.
- Headline and CTA render and work before below-the-fold assets load.

## Overrides: lead forms

- **Only the fields the conversion needs** (email alone for a newsletter). Extra fields: `form-burden`.
- **Visible labels, inline errors, a visible success state**; the submit button names the reward ("Get
  the guide").
- An unwired form on a static page goes under Wiring to confirm. If it shows a success message that is untrue,
  that message is `false-feedback`.

## Reminders

- Accessibility applies in full: marketing pages habitually ship low-contrast text on gradients and
  navigation that keyboards cannot open.
- Navigation fits one line at every desktop width shipped; on phones, hiding section links is fine
  when the primary CTA and essential destinations (sign in, pricing) stay reachable.
