# Style: Technical mono

An engineering drawing: monospace labels, visible grid and measurements, one working colour, everything annotated.

- **Use for:** Developer tools, infrastructure, data and crypto analytics, technical documentation and specifications.
- **Not for:** General consumers, children, luxury.
- **Schemes:** light and dark (both sets below).

| | Specification |
|---|---|
| Type | Display: JetBrains Mono. Body: Inter. Figures and code: JetBrains Mono. Weights: 400 and 700. Sizes (px): 11, 12, 14, 16, 20, 28, 44; body is 14; display tracking 0; line height 1.55 for text, 1.1 for display. |
| Colour | Paper or terminal base, ink, and one working colour for live values and the main action. The accent may be used as text colour on the page background (5.6:1). |
| Space | 4px base; gutter 16; section 64; visible 8px or column grid lines allowed as a motif. |
| Shape | Radius 0 to 2. 1px solid and dashed lines; corner marks and index numbers as ornament with a job. |
| Depth | None. |
| Imagery | Diagrams, code, real output, tables. |
| Motion | Instant or 80ms; a blinking cursor is the only loop allowed. |
| Charts | Step lines and bars with 1px strokes, mono tick labels, dashed reference lines, values annotated at the ends. |

**What makes it look expensive**
1. Monospace for labels, figures and code only; prose in the sans.
2. Every figure carries its unit and timestamp.
3. Labels aligned to a character grid.

**What makes it look cheap:** Monospace body text in long paragraphs; neon green on black with glow; fake terminal windows with invented output; random ASCII decoration.

## Token block (paste first; set `--accent` and `--accent-ink` for this product, change nothing else)

```css
:root {
  --font-display: "JetBrains Mono", ui-monospace, "SF Mono", Menlo, Consolas, "DejaVu Sans Mono", monospace;
  --font-body: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, "SF Mono", Menlo, Consolas, "DejaVu Sans Mono", monospace;
  --fs-1: 11px; --fs-2: 12px; --fs-3: 14px; --fs-4: 16px; --fs-5: 20px; --fs-6: 28px; --fs-7: 44px;
  --lh: 1.55; --track-display: 0;
  --bg: #F7F8F5; --surface: #FFFFFF; --ink: #10140F; --ink-2: #4D5A4A; --line: #C8D0C4;
  --accent: #B43A06; --accent-ink: #FFFFFF;
  --ok: #1B8038; --warn: #A16000; --bad: #D32F2F;
  --r-1: 0px; --r-2: 2px; --r-3: 2px; --border: 1px solid var(--line);
  --shadow-1: none; --shadow-2: none;
  --dur: 80ms;
}
@media (prefers-color-scheme: dark) { :root {
  --bg: #0D100D; --surface: #151A15; --ink: #E6EDE3; --ink-2: #9DAA99; --line: #2B332A;
  --accent: #7CE38B; --accent-ink: #07130A;
  --ok: #57C984; --warn: #F0B429; --bad: #FF8A80;
} }
```

Fonts: Inter, JetBrains Mono are open-licence families (see `libraries.md`
for how to load them). In a single file with no network the system stacks after each name take over; the
style then rests on its sizes, spacing, shape and colour, which is why those are fixed here.
Measured contrast of this palette: ink on bg 17.4:1; ink on surface 18.6:1; ink-2 on bg 6.8:1; ink-2 on surface 7.3:1; accent-ink on accent 5.9:1; accent on bg 5.6:1.
`--ok`, `--warn` and `--bad` are for a status only (on time, due, late; passed, at risk, failed), always with a
word or an icon; each measures at least 4.5:1 as text on `--bg` and `--surface`. A pale status surface is
`color-mix(in srgb, var(--bad) 12%, var(--surface))` with `--ink` text. A status is never shown in the accent.
