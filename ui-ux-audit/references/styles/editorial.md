# Style: Editorial

A well-set publication: a serif with character for headlines, a calm text face, narrow measure, figures and pull-outs that carry the argument.

- **Use for:** Reports that argue a case, long-form landing pages, research summaries, thought pieces.
- **Not for:** Operational dashboards, dense tools, checkout.
- **Schemes:** light only.

| | Specification |
|---|---|
| Type | Display: Newsreader. Body: Source Sans 3. Figures and code: IBM Plex Mono. Weights: display 500, body 400 and 600. Sizes (px): 13, 15, 18, 22, 30, 44, 64; body is 18; display tracking -0.01em; line height 1.6 for text, 1.1 for display. |
| Colour | Paper and ink. The accent appears in rules, figure highlights and links, never as a large fill. The accent may be used as text colour on the page background (8.2:1). |
| Space | 4px base; gutter 32; section 112; text column of 66 characters with figures allowed to break wider. |
| Shape | Radius 0 to 2. Hairline rules above headings and around figures. |
| Depth | None. |
| Imagery | Charts with a headline that states the finding and a source line; photographs with captions; no stock illustration. |
| Motion | None beyond link and focus states. |
| Charts | Ink for axes and labels, accent for the highlighted series, muted warm greys for the rest; direct labels, no legend boxes. |

**What makes it look expensive**
1. Headline, standfirst, body and caption are four clearly different sizes and weights, used the same way everywhere.
2. Each figure has a finding as its headline and a small source line.
3. Real quotation marks, dashes and non-breaking spaces; no widows in headlines.

**What makes it look cheap:** Serif used for everything including small labels; cards and shadows around paragraphs; centred body text; decorative drop capitals.

## Token block (paste first; set `--accent` and `--accent-ink` for this product, change nothing else)

```css
:root {
  --font-display: "Newsreader", "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
  --font-body: "Source Sans 3", Seravek, "Gill Sans Nova", Ubuntu, Calibri, "DejaVu Sans", sans-serif;
  --font-mono: "IBM Plex Mono", ui-monospace, "SF Mono", Menlo, Consolas, "DejaVu Sans Mono", monospace;
  --fs-1: 13px; --fs-2: 15px; --fs-3: 18px; --fs-4: 22px; --fs-5: 30px; --fs-6: 44px; --fs-7: 64px;
  --lh: 1.6; --track-display: -0.01em;
  --bg: #FBFAF7; --surface: #F1EEE7; --ink: #1A1A18; --ink-2: #5A574F; --line: #D8D3C7;
  --accent: #8C2A1C; --accent-ink: #FFFFFF;
  --ok: #1A7A35; --warn: #995B00; --bad: #C82D2D;
  --r-1: 0px; --r-2: 2px; --r-3: 2px; --border: 1px solid var(--line);
  --shadow-1: none; --shadow-2: none;
  --dur: 120ms;
}
```

Fonts: IBM Plex Mono, Newsreader, Source Sans 3 are open-licence families (see `libraries.md`
for how to load them). In a single file with no network the system stacks after each name take over; the
style then rests on its sizes, spacing, shape and colour, which is why those are fixed here.
Measured contrast of this palette: ink on bg 16.7:1; ink on surface 15.0:1; ink-2 on bg 6.9:1; ink-2 on surface 6.2:1; accent-ink on accent 8.5:1; accent on bg 8.2:1.
`--ok`, `--warn` and `--bad` are for a status only (on time, due, late; passed, at risk, failed), always with a
word or an icon; each measures at least 4.5:1 as text on `--bg` and `--surface`. A pale status surface is
`color-mix(in srgb, var(--bad) 12%, var(--surface))` with `--ink` text. A status is never shown in the accent.
