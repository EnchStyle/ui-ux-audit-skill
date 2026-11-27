# Usability: simple to use, to navigate and to understand

A first-time user, with no instructions, should know what the screen is for, what to do next, where they are
and how to go back. Each rule below is a build rule and an audit check; the registry code is in brackets.
Sources are at the end.

## 1. The purpose is clear within five seconds  [`purpose-unclear`]

- **Build:** the first screen states in the user's own words what this is and who it is for: a heading of
  two to eight words that names the thing, and one supporting line. A report opens with its conclusions; a
  dashboard with the answer to "are we on track"; an app screen with a title that names the place.
- **Check:** look at the first-screen screenshot for five seconds, then answer without looking again: what is
  this, who is it for, what can I do here? If the heading alone does not answer the first question, it is
  `purpose-unclear` (Critical when nothing on the first screen answers it).

## 2. One main action per screen; the next step is always visible  [`primary-action`, `dead-end`]

- **Build:** exactly one control carries the filled, highest-contrast style; everything else is secondary
  (outline or text). Repeat the same action with the same label at natural breaks rather than adding new ones.
  Every state, including error, empty and success, offers a next step.
- **Check:** the script lists the filled buttons on the first screen. None, or two or more of equal weight with
  different destinations, is `primary-action`. A state with no next step is `dead-end`.
- **Why:** when two actions look equally important the user must stop and choose; most stop and leave.

## 3. Navigation: where am I, how do I go back, how do I reach the main sections
[`nav-current`, `nav-back`, `nav-hidden`, `nav-broken`, `nav-structure`]

- **Build:** the current place is marked by more than a tint (weight, an indicator, `aria-current`). Every
  screen below the top level has a visible way back; every sheet and dialog a visible way out. Main sections are
  reachable from every screen. Keep top-level choices to seven or fewer (three to five in a phone bottom bar)
  and depth to three levels; show top-level links directly when there are four or fewer, even on phones, because
  hidden navigation is found about half as often.
- **Check:** `nav-current` from the navigation census (`current_marked`) and the screenshot; `nav-back` by
  looking at every non-top screen; `nav-broken` from the click census; `nav-structure` by counting.

## 4. Plain words  [`jargon`, `cta-mismatch`, `term-drift`]

- **Build:** labels use the words the audience uses. Spell out an abbreviation at first use or in the label
  itself ("Average handling time", not "AHT"). A button is a verb naming the outcome, and it does exactly
  that. One name per thing.
- **Check:** list every abbreviation and internal term on the screen; any that the stated audience would not
  know and that is never explained is `jargon`. Established terms of the audience's own trade are not jargon
  (an accountant knows "VAT"; a board member does not know "AHT").

## 5. Progressive disclosure  [`overload`, `form-burden`]

- **Build:** show what most users need most of the time; put advanced options one step away behind a control
  whose label says what is there. No more than two levels of disclosure. Ask only for the fields the task
  needs; one question or decision per step when the task is unfamiliar. Prefill the likely value and offer
  the common answers as one tap (Today, Yesterday, Earlier) before a picker or a typed field. Choices that
  matter stay in view: a row of filters wraps onto a second line on a phone instead of scrolling sideways.
- **Check:** the script reports the number of interactive elements on the first screen. More than about nine
  ungrouped, equal-weight choices, or every feature shown at once with no order of importance, is `overload`.
  Density in a tool used daily is not overload when it is grouped and aligned.

## 6. Errors: prevent, explain, recover  [`destructive-no-confirm`, `state-error`, `false-feedback`]

- **Build:** prevent first (constrain inputs, disable what cannot work and say why, confirm or offer undo for
  anything destructive, never place a destructive control beside the main one). When an error happens: text
  beside its source, with an icon, saying what went wrong and what to do; never colour alone; keep what the
  user typed.
- **Check:** from the click census: submit each form empty, operate each destructive control, choose a filter
  with no match. Read what the page shows.

## Sources (checked 26 November 2026)

- Jakob Nielsen, "10 Usability Heuristics for User Interface Design", Nielsen Norman Group (1994, reviewed 30
  January 2024): visibility of system status; match with the real world; user control and freedom; consistency
  and standards; error prevention; recognition rather than recall; aesthetic and minimalist design; help users
  recover from errors. https://www.nngroup.com/articles/ten-usability-heuristics/
- Jakob Nielsen, "Progressive Disclosure", Nielsen Norman Group (2006): the split must be right, the way to the
  rest obvious, and more than two levels hurts. https://www.nngroup.com/articles/progressive-disclosure/
- Tim Neusesser and Evan Sunwall, "Error-Message Guidelines", Nielsen Norman Group (2023).
  https://www.nngroup.com/articles/error-message-guidelines/
- Kara Pernice and Raluca Budiu, "Hamburger Menus and Hidden Navigation Hurt UX Metrics", Nielsen Norman Group
  (2016). https://www.nngroup.com/articles/hamburger-menus/
- GOV.UK Service Manual, "Structuring forms" (one thing per page).
  https://www.gov.uk/service-manual/design/form-structure
- Apple Human Interface Guidelines, "Entering data" (change log 21 June 2023): prefill reasonable default
  values; offer choices instead of requiring text entry.
  https://developer.apple.com/design/human-interface-guidelines/entering-data
- Apple Human Interface Guidelines (Toolbars, Tab bars, Modality) and Android Developers (Navigation bar) for
  the platform navigation rules; see `mobile.md`.
