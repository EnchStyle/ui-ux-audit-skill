# Style: Dense console

An instrument panel for people who use it all day: maximum information per screen, strict alignment, colour only for status.

- **Use for:** Operations and finance dashboards, admin tools, tables with many rows, monitoring.
- **Not for:** First-time or occasional users, marketing pages, phones as the main device.
- **Schemes:** light and dark (both sets below).

| | Specification |
|---|---|
| Type | Display: IBM Plex Sans. Body: IBM Plex Sans. Figures and code: IBM Plex Mono. Weights: 400 and 600. Sizes (px): 11, 12, 13, 14, 16, 20, 28; body is 13; display tracking 0; line height 1.4 for text, 1.1 for display. |
| Colour | Neutral chrome. Red, amber and green exist only as status, always with a word or icon. The accent marks selection and the main action. The accent may be used as text colour on the page background (6.2:1). |
| Space | 4px base; gutter 12; section 32; row height 32; controls 32; no decorative space. |
| Shape | Radius 2 for controls and cells, 4 for panels. 1px borders define every region. |
| Depth | None, except one shadow for menus. |
| Imagery | None. Data only. |
| Motion | 100ms on state change; no entrance animation. |
| Charts | Thin lines, small multiples, shared scales; mono figures on axes; status colours only for thresholds. |

**What makes it look expensive**
1. Every number right-aligned in tabular figures with one precision per column.
2. One row height and one cell padding through the whole product.
3. A single dominant answer per view even at high density.

**What makes it look cheap:** Large cards with one number each; rounded friendly shapes; decorative colour on tiles; airy spacing that pushes data below the first screen.

## Token block (paste first; set `--accent` and `--accent-ink` for this product, change nothing else)

```css
:root {
  --font-display: "IBM Plex Sans", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --font-body: "IBM Plex Sans", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --font-mono: "IBM Plex Mono", ui-monospace, "SF Mono", Menlo, Consolas, "DejaVu Sans Mono", monospace;
  --fs-1: 11px; --fs-2: 12px; --fs-3: 13px; --fs-4: 14px; --fs-5: 16px; --fs-6: 20px; --fs-7: 28px;
  --lh: 1.4; --track-display: 0;
  --bg: #FFFFFF; --surface: #F3F4F6; --ink: #14171A; --ink-2: #4B5560; --line: #C9CED4;
  --accent: #1257D6; --accent-ink: #FFFFFF;
  --ok: #1A7A35; --warn: #995B00; --bad: #C82D2D;
  --r-1: 2px; --r-2: 4px; --r-3: 4px; --border: 1px solid var(--line);
  --shadow-1: none; --shadow-2: 0 4px 12px rgb(0 0 0 / 0.16);
  --dur: 100ms;
}
@media (prefers-color-scheme: dark) { :root {
  --bg: #121416; --surface: #1C1F23; --ink: #ECEFF2; --ink-2: #A9B2BC; --line: #3A4048;
  --accent: #7FB0FF; --accent-ink: #0B1220;
  --ok: #57C984; --warn: #F0B429; --bad: #FF8A80;
} }
```

Fonts: IBM Plex Mono, IBM Plex Sans are open-licence families (see `libraries.md`
for how to load them). In a single file with no network the system stacks after each name take over; the
style then rests on its sizes, spacing, shape and colour, which is why those are fixed here.
Measured contrast of this palette: ink on bg 18.0:1; ink on surface 16.3:1; ink-2 on bg 7.6:1; ink-2 on surface 6.9:1; accent-ink on accent 6.2:1; accent on bg 6.2:1.
`--ok`, `--warn` and `--bad` are for a status only (on time, due, late; passed, at risk, failed), always with a
word or an icon; each measures at least 4.5:1 as text on `--bg` and `--surface`. A pale status surface is
`color-mix(in srgb, var(--bad) 12%, var(--surface))` with `--ink` text. A status is never shown in the accent.
