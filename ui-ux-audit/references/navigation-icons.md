# Category 11: Navigation, Flows and Icons

## Navigation

- **Current location is unmistakable**: the active item differs by more than a faint tint (weight,
  colour or an indicator bar) and carries `aria-current="page"`.
- **Same navigation everywhere**: same items, same order, same style on every page of a product.
- **Tabs switch views of the same content; navigation moves between sections.** Mixing the two
  confuses the user's map.
- **Depth gets breadcrumbs** beyond two levels; every crumb except the current page is a link.
- **Overflow**: too many items go into a "More" menu or a horizontal scroller with a visible cue;
  never clipped mid-word, never wrapped onto a second line on desktop.
- **Links are links**: real `href`s for navigation (so open-in-new-tab works), buttons for actions.
  On a static page, links to `#` are Wiring to confirm, not a scored finding.

## Flows

- **Progress is honest**: "Step 2 of 4", and steps do not multiply after the user commits.
- **Back preserves state**; it never throws the user out of the whole flow.
- **No dead ends**: every error, empty and success state offers a next action.
- **Leaving with unsaved input** gets one clear confirmation, not silent loss and not guilt.
- **A primary CTA goes where its label says.** "Start planning" that scrolls to a newsletter form is a
  broken promise: Critical on a landing page's primary action.

## Icons

- **One family, one style** (all outline or all filled), one stroke weight.
- **One size per role** on the 16/20/24px optical grid; odd sizes (18, 22) sit between optical sizes.
- **One meaning per icon** across the product.
- **Labels**: icon-only is acceptable for universal glyphs (close, search, menu) with an accessible
  name; everything else gets a visible label or at least a tooltip plus an accessible name.
- **Alignment**: optically centred against adjacent text; `flex-shrink: 0` so icons never squash.
- **Emoji are not icons** in interface chrome: they render differently per platform and cannot be
  styled.
