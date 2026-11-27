# Style: Swiss grid

Order made visible: a strict column grid, one grotesque typeface, flush-left text, large size contrast, one signal colour.

- **Use for:** Analytics reports, corporate and institutional pages, data-heavy landing pages, annual reviews.
- **Not for:** Playful consumer products, children, luxury retail.
- **Schemes:** light only.

| | Specification |
|---|---|
| Type | Display: Inter. Body: Inter. Figures and code: IBM Plex Mono. Weights: 400 and 700 only. Sizes (px): 12, 14, 16, 20, 28, 44, 72; body is 16; display tracking -0.02em; line height 1.5 for text, 1.1 for display. |
| Colour | White, black and greys carry almost everything; the one colour marks the single most important thing on each screen (the main action, the key figure). Never a second colour, never a gradient. The accent may be used as text colour on the page background (5.9:1). |
| Space | 4px base; gutter 24; section 96; 12-column grid, with content starting on a column line; measure 62 characters. |
| Shape | Radius 0. Rules of 1px (light) and 2px (ink) instead of boxes. |
| Depth | None. No shadows; separation by rules and white space. |
| Imagery | Real data, charts and photographs in strict rectangles aligned to the grid; no illustration. |
| Motion | Almost none: 120ms opacity on state change. |
| Charts | Black and grey series with the accent for the one series that matters; 1px axes; no chart borders or backgrounds. |

**What makes it look expensive**
1. Every left edge sits on a column line, including chart plot areas.
2. A display size at least 2.5 times the body size, set tight, with deliberate line breaks.
3. Numbers in tabular figures with units in small capitals or a smaller size.

**What makes it look cheap:** Centred text; rounded cards or shadows; a second accent colour; body text stretched across the full width.

## Token block (paste first; set `--accent` and `--accent-ink` for this product, change nothing else)

```css
:root {
  --font-display: "Inter", "Helvetica Neue", Helvetica, Arial, sans-serif;
  --font-body: "Inter", "Helvetica Neue", Helvetica, Arial, sans-serif;
  --font-mono: "IBM Plex Mono", ui-monospace, "SF Mono", Menlo, Consolas, "DejaVu Sans Mono", monospace;
  --fs-1: 12px; --fs-2: 14px; --fs-3: 16px; --fs-4: 20px; --fs-5: 28px; --fs-6: 44px; --fs-7: 72px;
  --lh: 1.5; --track-display: -0.02em;
  --bg: #FFFFFF; --surface: #F4F4F1; --ink: #111111; --ink-2: #55554F; --line: #D7D7D2;
  --accent: #C8102E; --accent-ink: #FFFFFF;
  --ok: #1A7A35; --warn: #995B00; --bad: #C82D2D;
  --r-1: 0px; --r-2: 0px; --r-3: 0px; --border: 1px solid var(--line);
  --shadow-1: none; --shadow-2: none;
  --dur: 120ms;
}
```

Fonts: IBM Plex Mono, Inter are open-licence families (see `libraries.md`
for how to load them). In a single file with no network the system stacks after each name take over; the
style then rests on its sizes, spacing, shape and colour, which is why those are fixed here.
Measured contrast of this palette: ink on bg 18.9:1; ink on surface 17.1:1; ink-2 on bg 7.5:1; ink-2 on surface 6.8:1; accent-ink on accent 5.9:1; accent on bg 5.9:1.
`--ok`, `--warn` and `--bad` are for a status only (on time, due, late; passed, at risk, failed), always with a
word or an icon; each measures at least 4.5:1 as text on `--bg` and `--surface`. A pale status surface is
`color-mix(in srgb, var(--bad) 12%, var(--surface))` with `--ink` text. A status is never shown in the accent.
