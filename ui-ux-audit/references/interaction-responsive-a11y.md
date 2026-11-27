# Categories 7 to 9: Touch and Interaction, Responsive Behaviour, Accessibility

Severities are set only in `severity-registry.md`; the codes in brackets below are its rows.

## Category 7: Touch and interaction

- **Target size.** The floor is WCAG 2.2 SC 2.5.8 (AA): at least 24 × 24px, unless a 24px circle centred on
  the undersized target touches no other target and no other undersized target's circle (spacing exception), or
  the target is a link inside a sentence (inline exception). Lists of links such as footers and breadcrumbs are
  not covered by the inline exception: they pass by size or by spacing. Below the floor: `target-small`. The
  comfortable size on touch-first products is 44px (48 on Android); that is platform guidance, not the standard
  (`target-touch`). Dense 32px controls on a pointer-first dashboard with room around them are correct.
- **Spacing between targets**: leave a clear gap between adjacent tappable controls (8px is a workable minimum;
  Apple suggests about 12 points around bordered controls). A destructive action never sits directly beside the
  main one: a slip of the finger should not delete anything.
- **Visual size versus hit area**: extend a small-looking control's hit area with padding or a
  pseudo-element instead of inflating the visual.
- **Press feedback**: every tap shows it registered (a slight scale or shift, a colour change).
- **Hover is an enhancement**: anything required to operate the page works without hover.
- **Safe areas**: bottom bars, floating buttons and toasts respect `env(safe-area-inset-bottom)` (`safe-area`;
  see `mobile.md`).
- **Scrolling**: no scroll hijacking; carousels use scroll snap and do not trap vertical scrolling.
- **One scroll area per region** [`scroll-nested`, `scroll-unexpected`]. A scroll area inside another that
  scrolls the same way is hard to control: the finger or the wheel moves one when the other was meant. Apple's
  guidance says not to put a scroll view inside another with the same orientation, and to show one scroll view
  per screen as a rule on the iPhone (Human Interface Guidelines, Scroll views, read 27 November 2026); a
  sideways strip inside a page that scrolls down is fine. So: a page that scrolls holds no tall box with its
  own vertical scroll, and an app shell (the page itself does not scroll) gives each panel exactly one inner
  scroller, with the panel's header and actions outside it.
- **Scrolling nobody asked for.** Setting only `overflow-x: hidden` on a box makes it scroll down as well: the
  other direction computes to `auto`. `overflow: hidden` removes the scrollbar but the box can still be scrolled
  by script and by focus, so a stretched one jumps and cannot be scrolled back. `overflow-x: clip` clips without
  making a scroll area (measured in Chromium 158: the same panel has 3 796px to scroll with `hidden` and none
  with `clip`); use it when the wish is only to stop sideways spill.
- **Scrollbars take width where they are drawn.** On Windows and Linux desktops a scrollbar is about 15px of the
  box it belongs to; nested scroll areas lose it once each. Playwright hides scrollbars by default, so a
  screenshot never shows one: read the script's `_scrollbars` pass. `scrollbar-gutter: stable` reserves the
  space so content does not shift when a scrollbar appears.
- **Drag** always has a non-drag alternative.

## Category 8: Responsive behaviour

- **360px is the narrow truth.** Any page-level horizontal scroll is `page-overflow`; find the fixed width,
  unwrapped row or missing `min-width: 0` that causes it.
- **The awkward middle.** Check 768px: two-column layouts that look right at 1280px often squeeze to
  unreadable columns there.
- **Every multi-column block declares its narrow behaviour**; type steps down on phones (`clamp()`),
  body text does not.
- **Wide tables and nav strips**: a contained horizontal scroller is an accepted pattern. Without a
  visible cue that more is hidden (an edge fade, shadow, arrow or hint, or an item cut mid-word
  with nothing else to signal it), it is worth a Polish `other` finding at most. A sticky first column is a bonus.
  Page-level overflow from a table is `page-overflow`.
- **Navigation collapse.** Desktop navigation fits on one line at every desktop width you ship (a nav
  that wraps at 1280px is `other`, Warning). Hiding secondary section links on phones is fine when the page
  is one scroll and the primary action stays; hiding destinations a phone user needs (sign in,
  pricing, contact, a shop's categories) with no menu is `nav-hidden`.
- **Do not hide load-bearing content** at a breakpoint; reorder or collapse it.
- **Modals on phones** become full-screen or bottom sheets.
- **Short viewports**: landscape phones and 700px-tall laptop windows must not push the primary action
  out of a `height: 100vh` hero; prefer `min-height: 100svh`.
- **Media** is fluid (`max-width: 100%; height: auto`), embeds sit in aspect-ratio boxes.

## Category 9: Accessibility

Contrast (Category 4) and forms (Category 6) carry their own accessibility rules.

- **Semantic elements**: `<button>` for actions, `<a href>` for navigation, lists as lists, landmarks
  (`header`, `nav`, `main`, `footer`). A `<div onclick>` is invisible to keyboards and screen readers
  (`keyboard-unreachable`; the script also finds click listeners added in code).
- **Keyboard**: every action reachable and operable; tab order follows visual order (an opened mobile
  menu placed before its toggle in the DOM breaks this); Escape closes overlays; arrow keys inside
  menus, tabs and radio groups.
- **Focus visible**: removing the outline without a `:focus-visible` replacement is `focus-missing`
  (SC 2.4.7); the indicator needs 3:1 against the colours beside it (SC 1.4.11, `focus-weak`), and the focused
  control must not be hidden under sticky bars (SC 2.4.11).
- **Focus management**: opening a dialog moves focus in; closing returns it; removing an item moves
  focus to a sensible neighbour; route changes move focus to the new heading.
- **Names**: every interactive element has an accessible name; links make sense out of context; icons
  inside named buttons are `aria-hidden`.
- **Text for screen readers only** is absolutely positioned, so it needs a positioned parent close by:
  `position: absolute; top: 0; left: 0; width: 1px; height: 1px; margin: -1px; overflow: hidden;
  clip-path: inset(50%); white-space: nowrap` inside a `position: relative` cell, row or label. Without one it
  is placed against the nearest positioned ancestor, which may be a fixed panel or the page, and stretches that
  box's scroll area: an unexpected scrollbar, empty space below the content, a panel that jumps (React Aria and
  WordPress document the same side effect for their hidden-text components, read 27 November 2026). Either a
  positioned parent or `top: 0; left: 0` alone removes the stretch; use both. After adding such text, run the
  script again: `scroll-unexpected` names the elements that stretch a box.
- **Images**: meaningful images have alt text; decorative ones `alt=""`; charts have a text
  alternative (a caption with the finding, or a data table).
- **ARIA**: native elements first; state attributes (`aria-expanded`, `aria-pressed`,
  `aria-current="page"`, `aria-sort`) kept in sync; `aria-live="polite"` for async status messages.
- **Single-key shortcuts** (a bare "/" for search) need a way to turn them off or remap them, or to
  work only when the control has focus (SC 2.1.4).
- **Motion**: non-essential animation respects `prefers-reduced-motion`.
- **Zoom and reflow**: usable at 200% zoom and 320px width; never disable pinch zoom.
- **Standard and law.** Audit against WCAG 2.2 AA (W3C Recommendation of 12 December 2024). The European
  Accessibility Act has applied since 28 June 2025. Its technical standard is EN 301 549: version 3.2.1 (WCAG
  2.1) is the one cited in the Official Journal; version 4.1.1 (WCAG 2.2) was published on 2 September 2026
  and was still awaiting citation on 26 November 2026. Mention this as a risk, not as legal advice; it does not
  change a severity.
