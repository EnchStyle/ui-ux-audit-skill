# Profile: E-commerce Storefronts and Checkout

Product listings, product pages, basket and checkout. These rules override the universal defaults.

Detection: product grids or cards, prices, add-to-basket buttons, variant pickers, quantity steppers,
basket or checkout routes, or the user saying so.

Source of truth: the theme tokens, the product-card and price components, and the basket and checkout
state logic when available. Storefronts usually sell across regions, so locale checks for currency,
tax and address formats apply at Warning minimum.

Simulation persona: a shopper on a phone, one-handed, comparing two products and checking the total
before paying.

## Overrides: price and availability clarity

- **The price paid is visible before adding to basket**, in the buyer's currency, with tax treatment
  where the locale expects it (EU prices include VAT). Ambiguous or hidden price: Critical.
- **No surprise costs at the last step**: shipping, tax and surcharges disclosed before payment
  (Blocker if revealed only at the end).
- **Stock state is honest**: an out-of-stock option never keeps an active add-to-basket that succeeds
  (Critical).
- **Scarcity and urgency are real** (Blocker if fabricated).
- **Sale prices are honest**: the struck-through price is a real prior price; the percentage matches
  the arithmetic (Critical if not).

## Overrides: grid and card consistency

- **Every card in a grid shares one anatomy**: image ratio, title line count, price position, badge
  slot, rating slot, button line (`alignment-consistency.md`). Drift is a Warning; Critical when it
  breaks the grid at a common width.
- **Bounded content**: titles clamp to a fixed line count; missing ratings or badges keep their
  reserved space.
- **Badges** use one vocabulary in one corner and never cover the product's focal point.
- **Catalogue grids** may end with a partial last row; that is not an orphan finding.

## Overrides: media and variants

- **Product images have fixed dimensions or aspect ratios** (layout shift on a grid is Critical).
- **The gallery**: clear selected thumbnail, keyboard navigation, a zoom with an escape, a no-image
  fallback.
- **Selected variant is shown by more than colour** (border plus check, `aria-pressed` or radio
  semantics): colour-only selection is Critical.
- **Unavailable variants are visibly disabled with the reason in text**; selecting a variant updates
  price, image and stock together.
- **Quantity steppers** enforce limits and accept typed values.
- **Swatches, size buttons and quantity steppers are primary controls on phones**: 44px targets.
  Smaller (24 to 43px) is a Warning; below 24px without spacing, Critical.

## Overrides: basket and checkout (the strictest bar)

- **A confusing or broken checkout step is a Blocker.**
- **Progress and a way back** on every step, without losing entered data or basket contents.
- **Guest checkout** exists unless the brief justifies an account (Critical if missing).
- **Inline field errors in text**, focus to the first error, input preserved.
- **Every state built**: empty basket with a route back, item removed with undo, payment declined,
  address invalid, shipping unavailable, coupon invalid, and a pay button that cannot be pressed twice
  (double charge risk is a Blocker).
- **Correct autocomplete** tokens for names, addresses and cards.

## Overrides: phone first

- A layout that works only at desktop is a Critical responsive failure.
- On product pages, add to basket stays within reach on phones (sticky bar or near the top); stranded
  far below the fold is a Warning.
- Filters and sort open in an accessible sheet with a visible applied count and "clear all".

## Content

Real product photography or honestly labelled placeholders; ratings, review counts and "bestseller"
labels from real data; buttons that name the outcome ("Add to basket", "Pay €89.00"); one term for the
basket throughout.
