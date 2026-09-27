# Categories 4 to 6: Colour and Contrast, Component States, Forms

## Category 4: Colour, contrast and dark mode

- **Contrast (WCAG 2.2 AA).** 4.5:1 for normal text, 3:1 for large text (24px, or 18.66px bold). Compute
  it from the rendered colours; for text over gradients or images, sample the pixels behind the text
  and report the lowest ratio. Body or CTA text below the bar is Critical; decorative text Warning.
  APCA is not a normative standard: use WCAG 2 ratios.
- **Non-text contrast (1.4.11), 3:1** applies to what a user needs to identify a control or read a
  graphic: text-field boundaries, checkboxes, radio buttons, toggles, icon-only buttons, focus
  indicators, chart lines and bars that carry meaning. A select or button already identified by its
  text label does not need a 3:1 border.
- **Buttons on gradients and photos.** Check every CTA against its whole background: the light end of
  a gradient, a ghost button over a photo with no scrim.
- **Placeholder and helper text** often lands near 2.5:1 on white; keep it readable (4.5:1).
- **Colour is never the only signal.** Errors, success, selection, deltas and chart series pair colour
  with text, an icon, a sign, a shape or a pattern.
- **One accent, one grey family, semantic colours kept semantic.** Red means error or destruction
  only; if the brand colour is red, destructive actions get their own treatment (icon, wording,
  distinct shade). Warm and cool greys mixed on one page read as two products.
- **Saturated colour is for accents**, not long text.
- **Theme lock.** One theme per page; a single deliberate full-bleed contrast section is fine; flipping
  back and forth between themes is not.

### Dark mode (only when the product has or promises one)

A missing dark theme is not a finding unless the product offers one or the brief asks for it. When
it exists: designed, not inverted (dark grey base, not `#000`; desaturated accents); elevation by
lighter surfaces, not shadows; the same tokens with swapped values; chart palettes defined per theme
and checked for contrast on the dark background; logos and images legible. Check contrast again in
the dark theme (`uicheck.py --dark`).

## Category 5: Component states

AI ships the happy path. Every interactive component on a primary flow has all of these; a missing
one is Critical on a primary flow, Warning on a secondary one.

- **Loading**: skeletons shaped like the final content; buttons that start async work show a pending
  state and block double submission.
- **Empty**: explains what would appear and offers the action that fills it. An empty result is never
  drawn as authoritative zeros or a flat line at zero.
- **Error**: says what happened and how to recover (retry, edit), inline for forms.
- **Disabled**: visibly different beyond opacity, ideally with the reason.
- **Hover, focus-visible, active, selected**: each distinct; nothing essential is hover-only.
- **Long content**: 200-character titles, 40-character names, 7-digit numbers. Trace them.
- **Reserved space for state changes**: a border or ring that appears on hover or focus is present
  but transparent in the default state (or uses `outline`), so nothing shifts.
- **Modals**: focus moves in and is trapped, Escape closes, focus returns to the trigger, the title
  labels the dialog, the page behind does not scroll.
- **Menus**: click outside and Escape close; arrow keys move; long lists scroll inside the menu.
- **Optimistic updates** roll back visibly on failure; silent failure after an optimistic update is a
  data-loss Blocker.
- **Crash containment**: a failing widget shows a recovery message in its region, never a blank page.
- **False feedback**: a toast or confirmation that reports success when the action failed or could not
  run (a "Copied" toast after a failed copy, "Sent" when nothing was sent) is Critical: the page states
  something untrue. A progress message ("Preparing file") that ends with nothing is Wiring to confirm.

On a static page, a missing backend is not a missing state: list inert submissions under Wiring to
confirm. A prototype form whose confirmation reads as if it was sent ("Request received") goes there
too, with a note that it becomes a Blocker if shipped unwired; a form that honestly says nothing was
sent is correct.

## Category 6: Forms

- **Visible label above every field**; the placeholder only shows format. Placeholder as the only
  label is Critical.
- **Real association**: `<label for>` matching the input `id`, or the input inside the label.
- **Errors**: in text below the field, specific ("Enter an email like name@example.com"), with
  `aria-invalid` and `aria-describedby`; focus moves to the first error on submit.
- **Validation timing**: on blur or submit, then live once an error shows; never while the user is
  still typing the first characters.
- **Required fields** marked (or optional ones, if most are required).
- **Submission**: pending state, double-submit blocked, visible success, and input preserved on failure
  (a form wiped on error is a Blocker).
- **Input types and autocomplete**: `type="email"`, `inputmode="numeric"`, `autocomplete` tokens for
  names, addresses and payment. A date typed with slashes needs a keyboard that has them.
- **Layout**: one column by default; field width hints at the expected length.
- **Destructive confirmations** name the object ("Delete 'Q3 report'?"), and the destructive button is
  distinct and not focused by default.
- **Only necessary fields.** Each extra field on a sign-up or lead form costs completions.
