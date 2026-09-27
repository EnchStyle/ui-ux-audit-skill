# Method: walk the page as the user, then sweep

The category checklist catches broken rules. It does not catch experiential failures: a control that
relabels the view but does not change the data, a CTA that goes somewhere its label did not promise, a
flow that works on the happy path and dead-ends on the empty state, a screen that is perfect at desktop
and unusable at 360px. Those surface only when you use the page as a person would. Walk first, then
sweep; write what the walk finds in the normal finding format.

## Three walks

1. **The real user in their real context.** The profile names the persona (for example a finance lead
   on a laptop between meetings, an operator scanning a dashboard at the start of a shift, a manager
   reading a report on a phone). Do the job the page exists for, end to end: what do they see first,
   what do they click first, does the result match the promise, can they get back?
2. **A constrained user**, one at least: keyboard only (tab order, visible focus, no traps), 200% zoom
   (reflow, clipping), colour-blind (is any meaning carried by colour alone?), or imprecise touch
   (target size and spacing).
3. **An edge-case-data user**: empty first visit, far more items than the layout expects, very long
   names, emails, numbers and translated strings, a slow network.

## At each step, ask

- Is the first thing seen the thing that matters most here?
- Is the first thing reached for obviously interactive, and does it do what its label says?
- Does every control actually change what it claims to change? (Change the period, the market, the
  filter: do the numbers move?)
- Do the figures agree with each other (tiles, tables, text, charts)?
- What happens on a double click, a click during loading, a mistaken click? Can the user undo or go
  back?
- At 360, 768 and 1280px: anything overflowing, squeezed, hidden or out of reach?

## States to trace

For each interactive component on the main flow, note in your working (not in the report) what the
user sees and can do when it is loading, empty, populated with typical and with extreme content, in
error and disabled. The empty and error states are the ones AI omits most often. A cell you did not
verify reads "not checked", never a guessed pass.

## Honesty

Say what the input could not confirm (screen-reader output, touch latency, network timing, fonts
that were not available) and put it under Verify with the severity it would take. Score only what the
page showed.
