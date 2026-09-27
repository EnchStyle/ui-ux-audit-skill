# Categories 7 to 9: Touch and Interaction, Responsive Behaviour, Accessibility

## Category 7: Touch and interaction

- **Target size.** The legal floor is WCAG 2.2 SC 2.5.8 (AA): at least 24 × 24px, unless a 24px circle
  centred on the target does not touch another target (spacing exception), or the target is a link
  inside a sentence or list of text (inline exception). Below that floor: Critical on a primary
  control, Warning otherwise. The comfortable size for primary controls on touch-first products is
  44px (48px on Android): a primary control of 24 to 43px there is a Warning. Dense 32px controls on
  a pointer-first dashboard with room around them are correct. Profiles may raise the floor.
- **Spacing between targets**: at least 8px between adjacent tappable controls; row actions in dense
  tables are the usual offender. Mis-clickable adjacent destructive actions are Critical.
- **Visual size versus hit area**: extend a small-looking control's hit area with padding or a
  pseudo-element instead of inflating the visual.
- **Press feedback**: every tap shows it registered (a slight scale or shift, a colour change).
- **Hover is an enhancement**: anything required to operate the page works without hover.
- **Safe areas**: bottom bars, floating buttons and toasts respect `env(safe-area-inset-bottom)`.
- **Scrolling**: no scroll hijacking; carousels use scroll snap and do not trap vertical scrolling.
- **Drag** always has a non-drag alternative.

## Category 8: Responsive behaviour

- **360px is the narrow truth.** Any page-level horizontal scroll is Critical; find the fixed width,
  unwrapped row or missing `min-width: 0` that causes it.
- **The awkward middle.** Check 768px: two-column layouts that look right at 1280px often squeeze to
  unreadable columns there.
- **Every multi-column block declares its narrow behaviour**; type steps down on phones (`clamp()`),
  body text does not.
- **Wide tables and nav strips**: a contained horizontal scroller is an accepted pattern. Without a
  visible cue that more is hidden (an edge fade, shadow, arrow or hint, or an item cut mid-word
  with nothing else to signal it), it is a Polish finding, not more. A sticky first column is a bonus.
  Page-level overflow from a table is Critical.
- **Navigation collapse.** Desktop navigation fits on one line at every desktop width you ship (a nav
  that wraps at 1280px is a Warning). Hiding secondary section links on phones is fine when the page
  is one scroll and the primary action stays; hiding destinations a phone user needs (sign in,
  pricing, contact, a shop's categories) with no menu is Critical.
- **Do not hide load-bearing content** at a breakpoint; reorder or collapse it.
- **Modals on phones** become full-screen or bottom sheets.
- **Short viewports**: landscape phones and 700px-tall laptop windows must not push the primary action
  out of a `height: 100vh` hero; prefer `min-height: 100svh`.
- **Media** is fluid (`max-width: 100%; height: auto`), embeds sit in aspect-ratio boxes.

## Category 9: Accessibility

Contrast (Category 4) and forms (Category 6) carry their own accessibility rules.

- **Semantic elements**: `<button>` for actions, `<a href>` for navigation, lists as lists, landmarks
  (`header`, `nav`, `main`, `footer`). A `<div onclick>` is invisible to keyboards and screen readers:
  Critical, Blocker when it is the only route to a core task.
- **Keyboard**: every action reachable and operable; tab order follows visual order (an opened mobile
  menu placed before its toggle in the DOM breaks this); Escape closes overlays; arrow keys inside
  menus, tabs and radio groups.
- **Focus visible**: removing the outline without a `:focus-visible` replacement is a Blocker; the
  indicator needs 3:1 against its surroundings and must not be clipped by `overflow: hidden` or hidden
  under sticky headers (SC 2.4.11).
- **Focus management**: opening a dialog moves focus in; closing returns it; removing an item moves
  focus to a sensible neighbour; route changes move focus to the new heading.
- **Names**: every interactive element has an accessible name; links make sense out of context; icons
  inside named buttons are `aria-hidden`.
- **Images**: meaningful images have alt text; decorative ones `alt=""`; charts have a text
  alternative (a caption with the finding, or a data table).
- **ARIA**: native elements first; state attributes (`aria-expanded`, `aria-pressed`,
  `aria-current="page"`, `aria-sort`) kept in sync; `aria-live="polite"` for async status messages.
- **Single-key shortcuts** (a bare "/" for search) need a way to turn them off or remap them, or to
  work only when the control has focus (SC 2.1.4).
- **Motion**: non-essential animation respects `prefers-reduced-motion`.
- **Zoom and reflow**: usable at 200% zoom and 320px width; never disable pinch zoom.
- **Standard and law.** Audit against WCAG 2.2 AA. The European Accessibility Act has applied since
  28 June 2025 to many consumer-facing products and services in the EU (e-commerce, banking,
  transport, e-books among them; microenterprises providing services are exempt). Its harmonised
  standard is EN 301 549 (V3.2.1 maps to WCAG 2.1; V4.1.1, aligned with WCAG 2.2, was published in
  September 2026). Where the Act applies, an accessibility failure on a core flow can be a Blocker.
  Say this as a risk, not legal advice.
