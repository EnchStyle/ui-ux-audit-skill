# Style: Neo-brutalist

Loud and blunt on purpose: thick black outlines, flat saturated blocks, hard offset shadows, big type.

- **Use for:** Creative studios, events, youth and indie brands, playful landing pages.
- **Not for:** Finance, health, public services, long reading, data-heavy reports.
- **Schemes:** light only.

| | Specification |
|---|---|
| Type | Display: Archivo Black. Body: Space Grotesk. Figures and code: Space Mono. Weights: display 400 (the face is already black), body 500 and 700. Sizes (px): 13, 15, 17, 22, 32, 52, 88; body is 17; display tracking -0.02em; line height 1.45 for text, 1.1 for display. |
| Colour | Ink, paper, and two or three flat colours at most. Text is always ink; colour is for blocks and buttons. Check every pair for contrast. The accent must not be used as text colour on the page background (1.4:1). |
| Space | 4px base; gutter 24; section 80; chunky padding (24) inside blocks; plenty of white space between loud elements. |
| Shape | Radius 0 (or one fixed 12, never mixed). 3px ink borders on every block and control. |
| Depth | Solid offset shadow, never blurred: 6px 6px 0 ink; pressed state moves the element into its shadow. |
| Imagery | Cut-out photographs, stickers, simple shapes; rotated a few degrees at most. |
| Motion | Snappy 100ms; press pushes the element 4px into its shadow. |
| Charts | Flat fills with ink outlines, bars only, values printed large on the bars. |

**What makes it look expensive**
1. One border weight and one shadow offset everywhere.
2. Strict alignment underneath the loudness: a real grid.
3. Generous empty space so that each loud block can be read.

**What makes it look cheap:** Blurred shadows or gradients mixed in; more than three colours; low-contrast pairs such as yellow on white; small thin type.

## Token block (paste first; set `--accent` and `--accent-ink` for this product, change nothing else)

```css
:root {
  --font-display: "Archivo Black", "Helvetica Neue", Helvetica, Arial, sans-serif;
  --font-body: "Space Grotesk", "Helvetica Neue", Helvetica, Arial, sans-serif;
  --font-mono: "Space Mono", ui-monospace, "SF Mono", Menlo, Consolas, "DejaVu Sans Mono", monospace;
  --fs-1: 13px; --fs-2: 15px; --fs-3: 17px; --fs-4: 22px; --fs-5: 32px; --fs-6: 52px; --fs-7: 88px;
  --lh: 1.45; --track-display: -0.02em;
  --bg: #FFFDF5; --surface: #FFFFFF; --ink: #111111; --ink-2: #3D3D3D; --line: #111111;
  --accent: #FFD400; --accent-ink: #111111;
  --ok: #1B8038; --warn: #A16000; --bad: #D32F2F;
  --r-1: 0px; --r-2: 0px; --r-3: 0px; --border: 3px solid var(--ink);
  --shadow-1: 4px 4px 0 var(--ink); --shadow-2: 8px 8px 0 var(--ink);
  --dur: 100ms;
}
```

Fonts: Archivo Black, Space Grotesk, Space Mono are open-licence families (see `libraries.md`
for how to load them). In a single file with no network the system stacks after each name take over; the
style then rests on its sizes, spacing, shape and colour, which is why those are fixed here.
Measured contrast of this palette: ink on bg 18.5:1; ink on surface 18.9:1; ink-2 on bg 10.7:1; ink-2 on surface 10.9:1; accent-ink on accent 13.2:1; accent on bg 1.4:1.
`--ok`, `--warn` and `--bad` are for a status only (on time, due, late; passed, at risk, failed), always with a
word or an icon; each measures at least 4.5:1 as text on `--bg` and `--surface`. A pale status surface is
`color-mix(in srgb, var(--bad) 12%, var(--surface))` with `--ink` text. A status is never shown in the accent.
