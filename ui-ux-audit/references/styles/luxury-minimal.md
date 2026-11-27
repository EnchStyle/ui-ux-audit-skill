# Style: Luxury minimal

Confidence through absence: vast white space, a high-contrast serif used large, tiny precise labels, almost no colour.

- **Use for:** Premium retail, hospitality, architecture, fashion, portfolios.
- **Not for:** Dense information, tools, anything that must explain a lot.
- **Schemes:** light only.

| | Specification |
|---|---|
| Type | Display: Cormorant Garamond. Body: Hanken Grotesk. Figures and code: IBM Plex Mono. Weights: display 400 and 500, body 400. Sizes (px): 11, 13, 16, 20, 30, 56, 96; body is 16; display tracking -0.01em; line height 1.6 for text, 1.1 for display. |
| Colour | Black, white and one warm grey. Photography carries all colour. The main button is ink. The accent may be used as text colour on the page background (19.3:1). |
| Space | 8px base; gutter 40; section 160; margins of a sixth of the width on desktop. |
| Shape | Radius 0. Hairlines only. |
| Depth | None. |
| Imagery | Large, few, excellent photographs; one per screen is enough. |
| Motion | Slow 400ms fades; nothing bounces. |
| Charts | Avoid; if essential, a single hairline chart in ink. |

**What makes it look expensive**
1. Labels in small capitals at 11 to 12px with 0.12em tracking, used sparingly.
2. One image or one sentence per screen, given all the room.
3. Perfectly even margins and a visible baseline rhythm.

**What makes it look cheap:** Crowding the page; gold gradients; several typefaces; buttons with rounded corners and shadows.

## Token block (paste first; set `--accent` and `--accent-ink` for this product, change nothing else)

```css
:root {
  --font-display: "Cormorant Garamond", Didot, "Bodoni MT", "Noto Serif Display", Georgia, serif;
  --font-body: "Hanken Grotesk", "Helvetica Neue", Helvetica, Arial, sans-serif;
  --font-mono: "IBM Plex Mono", ui-monospace, "SF Mono", Menlo, Consolas, "DejaVu Sans Mono", monospace;
  --fs-1: 11px; --fs-2: 13px; --fs-3: 16px; --fs-4: 20px; --fs-5: 30px; --fs-6: 56px; --fs-7: 96px;
  --lh: 1.6; --track-display: -0.01em;
  --bg: #FFFFFF; --surface: #F7F6F4; --ink: #0E0E0E; --ink-2: #5E5E5E; --line: #DAD7D2;
  --accent: #0E0E0E; --accent-ink: #FFFFFF;
  --ok: #1B8038; --warn: #A16000; --bad: #D32F2F;
  --r-1: 0px; --r-2: 0px; --r-3: 0px; --border: 1px solid var(--line);
  --shadow-1: none; --shadow-2: none;
  --dur: 400ms;
}
```

Fonts: Cormorant Garamond, Hanken Grotesk, IBM Plex Mono are open-licence families (see `libraries.md`
for how to load them). In a single file with no network the system stacks after each name take over; the
style then rests on its sizes, spacing, shape and colour, which is why those are fixed here.
Measured contrast of this palette: ink on bg 19.3:1; ink on surface 17.9:1; ink-2 on bg 6.5:1; ink-2 on surface 6.0:1; accent-ink on accent 19.3:1; accent on bg 19.3:1.
`--ok`, `--warn` and `--bad` are for a status only (on time, due, late; passed, at risk, failed), always with a
word or an icon; each measures at least 4.5:1 as text on `--bg` and `--surface`. A pale status surface is
`color-mix(in srgb, var(--bad) 12%, var(--surface))` with `--ink` text. A status is never shown in the accent.
