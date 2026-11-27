# Style: Warm craft

Made by people: warm paper tones, a soft serif with personality, hand-made imagery, unhurried spacing.

- **Use for:** Food, craft, wellness, independent shops, hospitality.
- **Not for:** Software tools, finance, anything dense.
- **Schemes:** light only.

| | Specification |
|---|---|
| Type | Display: Fraunces. Body: Work Sans. Figures and code: IBM Plex Mono. Weights: display 500, body 400 and 600. Sizes (px): 13, 15, 17, 21, 28, 40, 60; body is 17; display tracking -0.01em; line height 1.6 for text, 1.1 for display. |
| Colour | Warm neutrals from the product itself (flour, clay, leaf); one natural accent; photographs supply the rest. The accent may be used as text colour on the page background (5.9:1). |
| Space | 4px base; gutter 24; section 96; roomy cards (24); measure 62 characters. |
| Shape | Radius 8 for controls, 12 for cards and images. Thin warm borders. |
| Depth | Barely any: one faint warm shadow under images. |
| Imagery | Real photographs in natural light or one hand-drawn illustration style; never stock. |
| Motion | Gentle 250ms fades. |
| Charts | Rarely needed; if so, ink lines with the accent and hand-labelled values. |

**What makes it look expensive**
1. One photographic treatment (light, crop, ratio) for every image.
2. Prices and details set quietly in the sans, names in the serif.
3. Warm greys throughout: no cold grey anywhere.

**What makes it look cheap:** Cool greys mixed with warm paper; script fonts; texture images as backgrounds; three accent colours.

## Token block (paste first; set `--accent` and `--accent-ink` for this product, change nothing else)

```css
:root {
  --font-display: "Fraunces", "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
  --font-body: "Work Sans", Seravek, "Gill Sans Nova", Ubuntu, Calibri, "DejaVu Sans", sans-serif;
  --font-mono: "IBM Plex Mono", ui-monospace, "SF Mono", Menlo, Consolas, "DejaVu Sans Mono", monospace;
  --fs-1: 13px; --fs-2: 15px; --fs-3: 17px; --fs-4: 21px; --fs-5: 28px; --fs-6: 40px; --fs-7: 60px;
  --lh: 1.6; --track-display: -0.01em;
  --bg: #FAF5EC; --surface: #FFFDF8; --ink: #2B2118; --ink-2: #6B5B4B; --line: #E3D7C4;
  --accent: #2F6B3F; --accent-ink: #FFFFFF;
  --ok: #1B8038; --warn: #A16000; --bad: #C82D2D;
  --r-1: 8px; --r-2: 12px; --r-3: 12px; --border: 1px solid var(--line);
  --shadow-1: 0 1px 2px rgb(43 33 24 / 0.08); --shadow-2: 0 12px 28px rgb(43 33 24 / 0.12);
  --dur: 250ms;
}
```

Fonts: Fraunces, IBM Plex Mono, Work Sans are open-licence families (see `libraries.md`
for how to load them). In a single file with no network the system stacks after each name take over; the
style then rests on its sizes, spacing, shape and colour, which is why those are fixed here.
Measured contrast of this palette: ink on bg 14.5:1; ink on surface 15.5:1; ink-2 on bg 6.0:1; ink-2 on surface 6.4:1; accent-ink on accent 6.4:1; accent on bg 5.9:1.
`--ok`, `--warn` and `--bad` are for a status only (on time, due, late; passed, at risk, failed), always with a
word or an icon; each measures at least 4.5:1 as text on `--bg` and `--surface`. A pale status surface is
`color-mix(in srgb, var(--bad) 12%, var(--surface))` with `--ink` text. A status is never shown in the accent.
