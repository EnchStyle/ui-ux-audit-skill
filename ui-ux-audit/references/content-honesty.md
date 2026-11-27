# Category 15: Content, Copy and Honesty

Severities are set only in `severity-registry.md`; the codes in brackets below are its rows.

Words and numbers are design material, and on a page that asks for trust they are the most important
material. This category covers fabricated content, dark patterns, copy quality and localisation.

## Fabricated or unsupported content

- **Unsourced precise claims.** "Trusted by 12,400 teams", "3.2x faster", "98.7% accuracy" with no
  source, date or basis read as claims and are treated as claims. Source them, label them as sample
  data, or remove them (`unsourced-claim`).
- **Invented testimonials and customers.** Quotes with stock names or headshots presented as real.
  On a page presented as real they belong to the same `unsourced-claim` finding as unsourced numbers; on
  a page that labels its content as sample they are not a finding. A plain text list of customer names is fine; the
  problem is invention, not typography.
- **Faked product.** Grey-rectangle "screenshots", fake dashboards and terminal windows presented as
  the product. Use a real screenshot, a working component, or an honestly labelled placeholder
  (`placeholder-content`).
- **Placeholder text** (lorem ipsum, "Your headline here") in something presented as finished
  (`placeholder-content`).
- **Illustrative data** is fine when labelled on the page ("Illustrative data, not a forecast").

## Dark patterns (`dark-pattern`)

Confirmshaming ("No thanks, I prefer wasting time"); pre-ticked consent or upsell boxes; costs
revealed only at the last step; countdown timers that reset or offers that never end; fake scarcity
or activity ("Only 2 left", "23 people viewing") without real data; trick wording on subscription or
destructive actions; cancellation much harder than sign-up; guilt or streak pressure aimed at
children. Name the mechanism and the honest alternative. They are Blockers because they make people pay, share or stay
against their intent; several are also restricted by consumer protection law, which is worth mentioning as a risk,
not as legal advice. Scarcity or urgency that the code does not show to be invented goes under Verify.

## Copy and microcopy

- **Buttons are verbs naming the outcome**: "Save changes", "Start free trial", "Download report".
  Not "Submit", "OK", "Click here". The label carries through: "Publish" leads to "Published".
- **One label per action.** "Get started", "Sign up" and "Try it now" pointing to one place read as
  three actions (`term-drift`). Repeating the same label down a page is correct.
- **Say what it does.** See `purpose-unclear` and `usability.md`.
- **Specific beats clever.** Flag broken grammar, unclear referents, forced metaphors, filler
  ("crafted with intention", "elegantly simple", "the future of X") and unfalsifiable superlatives.
- **One register and one term per concept** across the page ("workspace" or "project", not both).
- **Errors and empty states** say what happened and how to fix it, without apology or vagueness.
- **Prices** show the currency, the billing period and whether VAT is included; discounts are
  arithmetically correct ("-40%" must be 40%).
- **Typography of copy**: sentence case for UI labels unless the brand says otherwise, curly quotes
  and apostrophes in body text, no em dashes used as a crutch in interface copy.

## Localisation (when the product ships in more than one language)

- Lithuanian, German, Finnish and Russian strings run 20 to 40% longer than English: buttons, tabs and
  navigation must survive the longest language without wrapping, clipping or overflowing a fixed
  width. Test with the real strings.
- Dates, numbers and currency come from one locale-aware formatter (`Intl.NumberFormat`,
  `Intl.DateTimeFormat`). Locale conventions are correct, not drift: Lithuanian "48 212" and "94,6 %".
- No text baked into images; the page `lang` matches the content.
- Right-to-left only when planned: logical properties (`margin-inline-start`) and mirrored
  directional icons.
