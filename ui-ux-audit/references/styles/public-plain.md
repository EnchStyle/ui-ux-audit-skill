# Style: Public-service plain

Nothing between the person and the task: large plain type, one column, one thing per page, obvious controls.

- **Use for:** Forms, applications, public and internal services, health and finance tasks, anything used once by everyone.
- **Not for:** Brand-led marketing, dense expert tools.
- **Schemes:** light only.

| | Specification |
|---|---|
| Type | Display: Public Sans. Body: Public Sans. Figures and code: IBM Plex Mono. Weights: 400 and 700. Sizes (px): 14, 16, 19, 24, 32, 44, 56; body is 19; display tracking 0; line height 1.5 for text, 1.1 for display. |
| Colour | Black on white. One strong action colour for the main button; links underlined; a high-visibility focus ring (3px ink outline with a 3px yellow offset). The accent may be used as text colour on the page background (7.9:1). |
| Space | 5px base; gutter 30; section 60; single column up to 40rem wide. |
| Shape | Radius 0. Inputs with a 2px ink border. |
| Depth | None. |
| Imagery | None unless it explains the task. |
| Motion | None. |
| Charts | Bars and lines in ink and one colour, labelled directly, with the data table beneath. |

**What makes it look expensive**
1. Body text at 19px with generous line height; nothing below 16px.
2. One question or decision per page, with the question as the heading.
3. Error summary at the top plus a message beside each field.

**What makes it look cheap:** Several columns; placeholder text as labels; pale grey text; icon-only buttons.

## Token block (paste first; set `--accent` and `--accent-ink` for this product, change nothing else)

```css
:root {
  --font-display: "Public Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;
  --font-body: "Public Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;
  --font-mono: "IBM Plex Mono", ui-monospace, "SF Mono", Menlo, Consolas, "DejaVu Sans Mono", monospace;
  --fs-1: 14px; --fs-2: 16px; --fs-3: 19px; --fs-4: 24px; --fs-5: 32px; --fs-6: 44px; --fs-7: 56px;
  --lh: 1.5; --track-display: 0;
  --bg: #FFFFFF; --surface: #F2F4F5; --ink: #101214; --ink-2: #4A5157; --line: #8D969C;
  --accent: #0B5D3B; --accent-ink: #FFFFFF;
  --ok: #1A7A35; --warn: #995B00; --bad: #C82D2D;
  --r-1: 0px; --r-2: 0px; --r-3: 0px; --border: 2px solid var(--ink);
  --shadow-1: none; --shadow-2: none;
  --dur: 0ms;
}
```

Fonts: IBM Plex Mono, Public Sans are open-licence families (see `libraries.md`
for how to load them). In a single file with no network the system stacks after each name take over; the
style then rests on its sizes, spacing, shape and colour, which is why those are fixed here.
Measured contrast of this palette: ink on bg 18.8:1; ink on surface 17.0:1; ink-2 on bg 8.1:1; ink-2 on surface 7.3:1; accent-ink on accent 7.9:1; accent on bg 7.9:1.
`--ok`, `--warn` and `--bad` are for a status only (on time, due, late; passed, at risk, failed), always with a
word or an icon; each measures at least 4.5:1 as text on `--bg` and `--surface`. A pale status surface is
`color-mix(in srgb, var(--bad) 12%, var(--surface))` with `--ink` text. A status is never shown in the accent.
