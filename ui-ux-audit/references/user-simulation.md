# Method: walk the main task, then go down the registry

The registry catches broken rules. It does not catch a control that relabels the view without changing the
data, a button that leads somewhere its label did not promise, a flow that works on the happy path and
dead-ends on an empty result, or a screen that a first-time user cannot work out. Those appear only when the
page is used. The walk is measured as tasks, not judged by impression: can a first-time user finish, in how
many steps, and where do they hesitate.

## 1. Name the tasks

Take the main task from the profile (a visitor understands the offer and starts a trial; an operator finds what
needs attention; a reader gets the three conclusions; a shopper adds the right product and reaches checkout; an
app user completes the flow the screens show). Add at most two secondary tasks that the navigation promises
(reach a named section, go back, change a filter).

## 2. Walk each task three ways

1. **First-time user.** Use only what the screenshots show. For each step name the element this user would
   press first, from its label and position alone; then confirm in the click census or the code what that
   element really does. Count the steps to the goal.
2. **Constrained user**, at least one: keyboard only (tab walk: order, visible focus, nothing unreachable);
   touch on a phone (target sizes, nothing on hover, nothing under a fixed bar); low vision (contrast, 200%
   zoom); colour-blind (is any meaning carried by colour alone?).
3. **Awkward data.** Use what the page itself can produce: a filter with no match, the empty form submitted, the
   longest name already in the data, a destructive action. Do not invent data the page cannot show; that goes
   under Verify.

## 3. Evidence the script gives you

The click census operates each distinct control once on a fresh copy of the page and reports what changed.
Read its flags as candidates:

| Flag | Registry row to check |
|---|---|
| `only_echoes_the_choice` (a selector changed only text that repeats the option) | `control-relabels` |
| `list_emptied_without_message` | `state-empty` |
| `removed_content_without_confirmation` | `destructive-no-confirm` (not when the same screen puts it back in one step) |
| `success_message_with_no_download_or_request` | `false-feedback` |
| `error_shown_by_style_only` | `state-error` |
| `label_and_destination_share_no_word`, `broken_anchor`, `broken_link` | `cta-mismatch`, `nav-broken` |
| `nothing_changed` | Wiring to confirm (or `other` when the page holds the data the control would act on) |

The tab walk gives the order of stops, backward jumps and stops that cannot be seen (`focus-order`); pointer
elements the keyboard cannot reach are under `keyboard-unreachable`; controls that stay covered are under
`control-obscured`. The script does not read meaning: whether "Add to basket" should work on an out-of-stock
item, or whether two figures describe the same thing, is for you to read.

## 4. Count hesitations

A hesitation is a point where a first-time user has to stop and work something out. Count only these, so that
two walks of the same page give the same number:

- two or more controls of equal visual weight compete for the next step (`primary-action`);
- the label of the needed control does not contain the word for what the user wants (`jargon`, `cta-mismatch`);
- the needed control is outside the first screen with nothing pointing to it, or hidden behind hover or a
  gesture (`hover-only`, `gesture-only`, `nav-hidden`);
- the screen does not say where the user is or how to go back (`nav-current`, `nav-back`);
- more than seven choices are offered at one step with no grouping (`overload`, `nav-structure`);
- an action gives no visible result within a second, or a result that is untrue (`false-feedback`);
- an error or empty state gives no next step (`dead-end`, `state-empty`, `state-error`).

## 5. Report it

```
## Task walk
| Task | Completed | Steps | Hesitations |
|---|---|---|---|
| Start a free trial | No: the button leads to the newsletter form (C3) | 1 | 2: two equal buttons (W2); label and destination differ (C3) |
| Reach Pricing on a phone | No: links hidden, no menu (C1) | - | 1 |
```

Every "No" and every hesitation cites a finding ID; a hesitation with no registry row is not reported. A cell
you could not check reads "not checked", never a guessed pass.
