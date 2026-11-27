# Severity registry

This is the only place where severities are set. Other files describe what to look for and how to fix it; when
they seem to disagree with this table, the table wins. The aim is that the same page audited twice gets the same
findings, at the same severities, with the same score.

## How to use it

1. Go down the table once for every audit. For each row decide: present, absent, or cannot tell (Verify).
2. **One finding per code per page** (per flow, when several screens form one task). The finding lists every place
   it occurs and takes the highest severity any occurrence earns. Ten pale labels are one `contrast-text` finding;
   six charts without axis titles are one `chart-labels` finding. Counting per occurrence is what made scores swing.
3. Use the severity in the table. Change it only when the "Changes when" column says so and you can quote the
   fact that triggers it. There is no other reason to move a severity.
4. A defect with no row gets the code `other`: apply the three tests below in order and take the first that is true.
   An `other` finding is never above Critical unless you quote the evidence for a Blocker test.
5. Script check names are the codes in this table, so a candidate from `uicheck.py` already tells you its row.
6. Verify and Wiring items are listed, never scored.

## The four levels

| Level | Points | Test (first that is true) |
|---|---|---|
| **Blocker** | 12 | (a) A user cannot finish the page's main task at a supported width, by touch or by keyboard: the control is missing, covered, cut off or unreachable. (b) The page shows something untrue that a user would act on with money, data or a decision: a figure, a chart scale, a price, stock, urgency. (c) An action destroys data or commits money with no confirmation and no undo. |
| **Critical** | 8 | A common path is broken or much harder for a whole group (phone, keyboard, screen reader, low vision, touch), or the page states something false or contradictory that does not reach (b). |
| **Warning** | 4 | Everyone can finish, but understanding, speed or trust visibly suffers; inconsistency that is seen at a glance. |
| **Polish** | 1 | Seen only on inspection. All Polish findings together cost at most 5 points, so a long list of refinements cannot outweigh one real fault. |

"Main task" and "main action" mean the one job the page exists for (profile files name it) and the control that
completes it. "Main desktop width" is 1280; "phone width" is 360 (or the device width); 768 is the in-between width.

## Table

### Reach, layout and text

| Code | Finding | Severity | Changes when |
|---|---|---|---|
| `page-overflow` | The page scrolls sideways at phone width | Critical | |
| `content-cut-off` | Content or a control cut off by the screen edge or a clipping container, with no way to scroll to it | Critical | Blocker when the main action, a total or a figure the task needs is what is cut off |
| `control-obscured` | A control or content stays covered by a fixed bar or floating button however far the page scrolls | Critical | Blocker when it is the main action. Warning when only text that is repeated elsewhere is covered |
| `text-clipped` | Text cut by a fixed height or width with no ellipsis and no way to read the rest | Warning | Critical when the hidden text is a value, a price, a control label or an error |
| `text-spill` | Text runs outside its box | Warning | |
| `text-overlap` | Text drawn over other text | Warning | Critical when either cannot be read |
| `control-overflow` | A control, a group of controls or a line of text is wider than the box it sits in and sticks out of it, still fully visible | Warning | Polish when it only reaches 4px or less into the box's padding. When part of it is cut off or covered the finding is `content-cut-off`, never both |
| `scroll-unexpected` | A box scrolls that nobody meant to scroll: `overflow-x` alone was set, which makes it scroll down as well, or elements that cannot be seen stretch its scroll area into empty space | Warning | Critical when a fixed panel or a panel that fills the screen scrolls as a whole, or when a header, footer or action is carried out of reach. A box with `overflow: hidden` that is only stretched stays at Warning: it has no scrollbar, yet it jumps when something inside takes focus |
| `scroll-nested` | A scroll area inside another that scrolls the same way (a tall table box inside a page that scrolls, a scroller inside a panel that scrolls) | Warning | Polish when the inner area is under a third of the screen height. Not a finding for a text area, a list box, a menu or a dialog that opens over the page, a panel fixed beside the page, or a sideways strip inside a page that scrolls down |
| `nav-hidden` | Destinations or controls (filters, sort, actions, sign-in) shown at desktop width are hidden at phone width with no menu or other way to reach them | Critical | Not a finding when every hidden link only jumps to a section of the same scrolling page. A link named for an account, a purchase or another page (Sign in, Basket, Contact) is a destination whatever address the prototype gives it |
| `small-text` | Rendered text under 12px (chart ticks in scaled graphics included) | Warning | Critical under 9px, or when it is the only label of a control or axis |
| `line-length` | Reading text over 90 characters per line | Warning | Polish outside reports and articles |
| `widow` | One word alone on the last line of a heading or short text | Polish | |
| `label-wrap` | A button label that wraps | Polish | |

### Accessibility

| Code | Finding | Severity | Changes when |
|---|---|---|---|
| `contrast-text` | Text under 4.5:1, or under 3:1 at 24px (18.66px bold) and above. Disabled controls and pure decoration are exempt | Critical | Warning when the only failing text is the placeholder of a field that has a visible label |
| `contrast-control` | The edge that identifies a field, checkbox or icon-only control, or a chart mark, under 3:1 | Warning | |
| `focus-missing` | No visible change on keyboard focus | Critical | Blocker when nine in ten or more of the controls show none (a skip link that only slides into view does not count as showing focus): the page cannot be operated by keyboard |
| `focus-weak` | Focus change under 3:1 | Warning | |
| `focus-order` | Tab order jumps against the visual order, or stops on things that cannot be seen | Warning | |
| `keyboard-unreachable` | A control with a click handler that the keyboard cannot reach | Critical | Blocker when it is the only way to do the main task |
| `keyboard-trap` | Focus cannot leave a component | Blocker | |
| `name-missing` | A control with no accessible name | Critical | |
| `label-placeholder` | A field whose only label is its placeholder | Critical | Warning when it has an accessible name but no visible label |
| `alt-missing` | An informative image with no alt attribute | Warning | Critical when the image is the whole content of a link or button, or carries data |
| `heading-order` | Skipped heading level, no h1, or several h1 | Warning | |
| `target-small` | A target under 24 x 24px whose 24px circle touches another target | Warning | Critical when it is the main action or a control of the main task |
| `target-touch` | A control under the comfortable size on a touch-first product (44px on iPhone and phone-width web, 48px on Android) | Warning | Profiles may raise it |
| `zoom-blocked` | No viewport meta tag, or one that stops pinch zoom | Critical | |
| `lang-missing` | No language on the page | Warning | |
| `motion-reduce` | Animation that keeps running under the reduced-motion setting | Warning | |
| `colour-only` | State, selection, error or direction of change shown by colour alone | Critical | |
| `hover-only` | A control or needed content that appears only on hover | Critical | Blocker when it is the main action |
| `gesture-only` | An action available only by swipe, long press or pinch | Critical | |

### States and behaviour

| Code | Finding | Severity | Changes when |
|---|---|---|---|
| `false-feedback` | A message that says something happened when it did not ("Sent", "Saved", "Downloaded") | Critical | Blocker when the user will rely on it for a payment, an order or saved work |
| `control-relabels` | A control that changes a caption or label but not the data it claims to change | Critical | Blocker on the analytics report profile |
| `state-empty` | An empty result shown as blank space or as real zeros | Critical | Verify when nothing on the page can produce the empty state |
| `state-error` | An error shown by colour alone, or with no message and no way to recover | Critical | Verify when nothing on the page can produce the error |
| `destructive-no-confirm` | Deleting or clearing with no confirmation and no undo | Blocker | Critical when it removes one saved item. Not a finding when the same screen puts it back in one step and nothing the user typed is lost (a tag removed from a picker, a filter chip): an action undone that easily is not destructive |
| `media-unsized` | Image or video with no reserved space (the layout jumps when it loads) | Warning | Critical when it is in the first screen or wider than a third of the page |

### Honesty and data

| Code | Finding | Severity | Changes when |
|---|---|---|---|
| `figures-disagree` | One quantity shown with different values (tile, table total, text, chart) | Critical | Blocker on the analytics report profile |
| `number-format` | One metric written in different precisions or formats | Warning | Critical when there are three or more forms |
| `chart-axis` | A bar chart whose value axis does not start at zero, or any broken or zoomed axis not stated on the chart | Critical | Blocker on the analytics report and dashboard profiles |
| `chart-colour-only` | Series told apart only by colour | Warning | Critical on the analytics report and dashboard profiles |
| `chart-labels` | A chart with no title, no axis titles or units (when values are not labelled directly), or no text alternative | Warning | |
| `chart-consistency` | The same series in different colours in different charts; unlike scales side by side with no note | Warning | |
| `chart-pair` | Charts or panels placed side by side as a pair with plot areas of different heights or baselines, so the pair does not line up | Polish | |
| `unsourced-claim` | Precise claims, testimonials or customer logos with no source, on a page presented as real | Critical | Warning outside landing pages. Not a finding when the page labels the content as sample data |
| `placeholder-content` | Lorem ipsum, "your headline here", empty grey boxes presented as the product | Critical | |
| `dark-pattern` | Pre-ticked paid extra or consent, confirmshaming, a countdown that restarts, scarcity or activity produced by the page's own code, costs revealed at the last step | Blocker | Verify when the code does not show the urgency or scarcity to be invented |
| `discount-wrong` | A discount label that does not match the prices beside it | Critical | |
| `price-unclear` | A price with no currency, period or tax statement where a buyer needs it | Warning | Critical on a checkout total |
| `stale-data` | Operational or financial data with no "updated" time | Warning | |

### Consistency (all measured by the script)

| Code | Finding | Severity | Changes when |
|---|---|---|---|
| `card-rows` | Matching parts of cards in one row at different heights | Warning | Critical when the part is a price or the button buyers compare (plans, products). Polish when it happens only below 1280 |
| `tile-baseline` | Values in a row of tiles off one line. If the same row also appears under `card-rows`, report it here only | Warning | Polish when it happens only at phone width |
| `grid-lone-item` | One item alone on the last row of a fixed set | Warning | Polish when only at 768. Lists that grow (products, articles, results) are exempt |
| `control-heights` | Side-by-side controls of different heights | Warning | |
| `segment-widths` | The options of one switch (a segmented control or toggle: two to five choices side by side in one shared box, one of them shown as selected) have different widths, so the control looks lopsided and the selected pill changes size with the choice | Warning | Polish when the widest is less than a fifth wider than the narrowest. Not a finding for underlined tabs, navigation links, filter chips or separate buttons: their width follows the label |
| `section-rhythm` | Ordinary sections with more than two different vertical paddings | Warning | |
| `gutter-drift` | Same-level rows of boxes with gaps that differ by 4px or more | Warning | |
| `media-ratios` | Mixed aspect ratios in one set | Warning | |
| `heading-proximity` | A heading nearer to the block above than to its own content | Warning | |
| `table-align` | Numeric cells not right-aligned, or headers aligned differently from their cells | Warning | |
| `table-sticky` | A table over 15 rows whose header scrolls away, also when it is declared sticky and an overflow box around the table stops it sticking | Warning | |
| `radius-drift` | More than three radius steps, or different radii on the same kind of component (two cards, two panels) | Warning | Polish when the steps are within 4px of each other. One radius for controls and another for cards is a system, not drift |
| `shadow-drift` | More than two shadow styles | Polish | |
| `type-scale-drift` | Font sizes less than 1px apart, or more than nine sizes on a page | Polish | |
| `icon-sizes` | Icons of one role at different sizes or stroke weights, or mixed filled and outlined styles | Polish | |
| `chip-heights` | One kind of chip or badge at different heights | Polish | |
| `radius-nested` | An inner corner that does not follow the outer one (only when the inset is smaller than the outer radius) | Polish | |
| `edge-near-miss` | A left edge 2 to 6px off the edge everything else shares | Polish | |
| `pad-asymmetry` | A box with visibly unequal top and bottom space | Polish | |
| `term-drift` | One thing called by several names | Polish | |

### Usability and navigation (`usability.md`)

| Code | Finding | Severity | Changes when |
|---|---|---|---|
| `purpose-unclear` | The first screen does not say what this is and who it is for | Warning | Critical when nothing on the first screen says it (headline, subline, visual) |
| `primary-action` | No main action on the first screen, or two different actions of equal weight | Warning | Critical with three or more different actions as equal filled buttons on a landing page's first screen. The same action repeated (header and hero) counts once. On dashboards, reports and account pages the first screen may hold the answer or summary instead: not a finding when the action is one scroll or one tap from it |
| `cta-mismatch` | A control leads somewhere its label did not promise | Warning | Critical when it is the main action |
| `nav-current` | Navigation does not mark where the user is | Warning | |
| `nav-back` | No visible way back or out of a screen, sheet or step | Critical | Warning on Android, where the system back gesture always exists |
| `nav-broken` | A navigation link goes to the wrong place or nowhere (a missing anchor or file), or a path the page draws cannot be used to move: breadcrumb levels, tabs or earlier steps that are plain text, or whose only link is the page the user is already on | Warning | Critical when the main task needs that destination |
| `nav-structure` | More than seven top-level choices, more than five in a phone bottom bar, or more than three levels with no breadcrumb | Warning | |
| `jargon` | Abbreviations or internal terms the audience would not use, never explained | Warning | |
| `overload` | A first screen with many competing choices and no grouping or order of importance | Warning | |
| `dead-end` | An error, empty or success state that offers no next step | Warning | |
| `form-burden` | Fields the task does not need | Warning | |

### Mobile (`mobile.md`)

| Code | Finding | Severity | Changes when |
|---|---|---|---|
| `safe-area` | Controls under the status bar, camera cut-out or home indicator | Critical | Warning when only non-interactive content is affected |
| `platform-mix` | Conventions of the other platform (floating action button or drawer on iPhone; back chevron with centred title or iPhone switches on Android) | Warning | |
| `input-zoom` | iPhone text fields under 16px (the page zooms on focus) | Warning | |
| `keyboard-cover` | The on-screen keyboard covers the field being typed in or the control that submits it | Critical | Verify when it cannot be shown from the layout |
| `keyboard-type` | A field asks for an on-screen keyboard that lacks a character its own format needs (a digits-only keypad where a decimal point, a slash or a minus sign is needed), or the wrong keyboard for the data | Critical | Blocker when the field is required for the main task. Read `inputmode`, `type` and the validation rule together; say it was judged from the code |
| `permission-timing` | A permission requested at launch, or with no reason given | Warning | |
| `text-scaling` | Layout that clips or overlaps at 200% text size | Warning | |
| `offline-state` | Network content with no loading, offline or retry state | Warning | Verify when the code is not available |

### Visual quality (`visual-excellence.md`)

| Code | Finding | Severity | Changes when |
|---|---|---|---|
| `visual-generic` | Landing pages only: three or more template tells, so the rating is "Generic template". Every tell is listed inside this one finding | Warning | Not scored on other profiles. "Competent but forgettable" is advice on every profile and is never scored |
| `hierarchy-flat` | Landing pages: no dominant element (the largest text on the first screen is under 1.3 times the next). Any profile: more than six equal tiles with nothing larger | Warning | On reports, dashboards and app screens a title the size of the key figures is normal: advice under Visual quality, not a finding |
| `decoration` | Decoration with no job: emoji used as icons, glow shadows, blur as the default surface, more than one large gradient | Polish | On a landing page it is listed inside `visual-generic` instead |
| `style-drift` | Screens of one flow that use different fonts, radii, sizes or shadows | Warning | |

## Which code when two fit

- A field with a placeholder and no other name: `label-placeholder`, not `name-missing`.
- A total row that is not the sum of its rows: `figures-disagree`.
- A defect that exists only in the dark theme or only in one state keeps its ordinary code; say where in the location.
- A success message on a control with no backend is `false-feedback` when it is true of nothing the user can
  check: no file arrived, nothing was sent, the page is as it was. When the control changes what the page shows
  and the message describes that change (a date moved on, a row ticked off), the prototype works as far as a
  page can: one line under Wiring that nothing is saved yet. The missing backend alone is always Wiring.
- A selector that changes captions only: `control-relabels`. A control that changes nothing at all: Wiring, unless the
  page already holds the data it would act on (a sort button over rows on the page), then `other`, Warning.
- Sideways scroll: `page-overflow`. Content that is cut off with no scroll: `content-cut-off`.
- Something wider than its box: still fully visible, `control-overflow`; partly cut off or covered, `content-cut-off`;
  text against its own box, `text-spill`. One of the three, never two.
- **Fit and the font.** Where a font was not installed, the main passes show a stand-in, and a narrower stand-in
  hides what the real font pushes out of its box. A fit candidate marked `_font-check` is a finding when the
  output says a font of the same widths drew it, and a risk when a wide font did: list the risk under Verify
  with its code. Never write fit under Clean for text whose real font was not drawn. What only the scrollbar
  pass lists (`_scrollbars`) is a finding: desktop browsers on Windows and Linux draw those scrollbars.
- Components on one screen that differ from each other (cards with three radii and four shadows) are scored
  where they differ, under `radius-drift`, `shadow-drift` or `type-scale-drift`, and as one finding when one
  restyle of that component clears them all. `style-drift` is only what still differs between screens once each
  screen is consistent in itself: a fault inside one screen is not scored a second time as a difference between
  screens.
- **One fix, one finding.** When a single change would clear two rows (a 40px field beside a 48px button is both
  `control-heights` and `target-touch`), report the row with the higher severity, or the earlier row when they are
  equal, and name the other code in Found. Two findings for one fault is what inflates and unsettles a score. The same repair made to several parts of one component is one fix as well: labels for all the fields of one form (`label-placeholder`, naming `name-missing` for a field that has no placeholder either), one radius and one shadow for the cards of one list (`radius-drift`, naming `shadow-drift`).
- **Stand-in fonts.** A widow, wrap or baseline candidate measured with a stand-in font is still a finding: the fix
  (balanced wrapping, a reserved line) holds for any font. Say which font stood in; do not move it to Verify.
- **`other` findings** take the lowest level whose test is plainly true; Critical or Blocker needs the quoted fact
  that meets that level's test. Where a profile names a level for one of its own rules, that level stands.

## Not findings

A finding needs a code and a fact. These are not facts about a defect:

- **A value that is the same everywhere.** Sharp corners on every element, 13px data type throughout, one heavy
  border weight, very large display type, a consistent wide offset: each is a choice. The registry scores
  variation, never the value. This is what keeps a deliberate, unconventional design from being marked down.
- **Decoration cut on purpose.** A decorative element hidden from assistive technology that bleeds past the page
  edge or is cropped by its container is a choice; check only that it causes no sideways scroll.
- **A convention stated on the page**: a zoomed axis that says so, a table that scrolls inside its own container
  with a visible cue, sample data labelled as sample, a prototype form that says nothing was sent.
- **Wiring a static page cannot have**: links to `#`, buttons with no handler, export, pagination, search over data
  the page does not hold, list items that all open the one detail screen a prototype has. One unscored line under
  Wiring. Wiring means the element is right and only its
  destination or handler is missing. Markup that is built wrong stays wrong when the backend arrives, so it is a
  finding: breadcrumb levels that are plain text while the current page is the link (`nav-broken`), a tab that is
  a paragraph, a button that is a `div` (`keyboard-unreachable`).
- **Problems the page's own content cannot trigger** (a title that would overflow if it were longer). Verify.
- **Content the page could add.** An audit judges what is on the page. Information a reader might also want (a
  price for another option, a longer explanation) goes under Questions, unless a row requires it
  (`price-unclear`, `chart-labels`, `purpose-unclear`, `stale-data`).
- **House floors that are not standards**: 12px ticks and table headers, 13 to 15px secondary copy, 32px controls
  with room around them on a pointer-first tool, no dark theme, raw colour values that cause no visible drift.
  A size that the user's own design system sets for a secondary line (a source line, caption or footnote at 11px)
  is not `small-text`: say so under Clean. Control labels, values and body text keep the row.
- **Taste.** If no row fits and none of the three tests is true, leave it out or put it under Questions.
