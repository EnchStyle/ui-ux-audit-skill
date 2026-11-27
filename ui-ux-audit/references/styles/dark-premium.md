# Style: Dark premium

A dark stage for one product: deep surfaces, light used like a spotlight, large confident type, very little colour.

- **Use for:** Product launches, data and crypto products, developer platforms, media.
- **Not for:** Forms-heavy services, long reading, print.
- **Schemes:** dark only.

| | Specification |
|---|---|
| Type | Display: Sora. Body: Inter. Figures and code: JetBrains Mono. Weights: display 600, body 400 and 500. Sizes (px): 12, 14, 16, 20, 28, 48, 80; body is 16; display tracking -0.03em; line height 1.55 for text, 1.1 for display. |
| Colour | Near-black base (never pure black), surfaces that get lighter as they rise, one warm accent. At most one large gradient or glow on the page, behind the hero product. The accent may be used as text colour on the page background (10.4:1). |
| Space | 4px base; gutter 24; section 128; wide margins; measure 60 characters. |
| Shape | Radius 10 for controls, 16 for cards. Hairline borders one step lighter than the surface. |
| Depth | Elevation by lighter surface, not by shadow; one inner highlight on the top edge of raised cards. |
| Imagery | The product, large, real and lit; real data in charts. |
| Motion | One orchestrated entrance of 400ms; 150ms feedback; nothing loops. |
| Charts | Light lines on dark, accent for the main series, grid at very low contrast; check every mark at 3:1. |

**What makes it look expensive**
1. Body text in off-white, not white; secondary text clearly dimmer but still 4.5:1.
2. A single light source: highlights on top edges only.
3. Huge headline with tight tracking and a deliberate two-line break.

**What makes it look cheap:** Purple or blue neon glows everywhere; pure black with pure white; glass cards over busy gradients; thin grey text that fails contrast.

## Token block (paste first; set `--accent` and `--accent-ink` for this product, change nothing else)

```css
:root {
  --font-display: "Sora", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --font-body: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, "SF Mono", Menlo, Consolas, "DejaVu Sans Mono", monospace;
  --fs-1: 12px; --fs-2: 14px; --fs-3: 16px; --fs-4: 20px; --fs-5: 28px; --fs-6: 48px; --fs-7: 80px;
  --lh: 1.55; --track-display: -0.03em;
  --bg: #0B0C0F; --surface: #14161B; --ink: #F2F3F5; --ink-2: #A7ABB4; --line: #2A2D35;
  --accent: #E7B56A; --accent-ink: #1A1205;
  --ok: #57C984; --warn: #F0B429; --bad: #FF8A80;
  --r-1: 10px; --r-2: 16px; --r-3: 24px; --border: 1px solid var(--line);
  --shadow-1: inset 0 1px 0 rgb(255 255 255 / 0.06); --shadow-2: 0 20px 60px rgb(0 0 0 / 0.5);
  --dur: 150ms;
}
```

Fonts: Inter, JetBrains Mono, Sora are open-licence families (see `libraries.md`
for how to load them). In a single file with no network the system stacks after each name take over; the
style then rests on its sizes, spacing, shape and colour, which is why those are fixed here.
Measured contrast of this palette: ink on bg 17.6:1; ink on surface 16.3:1; ink-2 on bg 8.5:1; ink-2 on surface 7.9:1; accent-ink on accent 9.9:1; accent on bg 10.4:1.
`--ok`, `--warn` and `--bad` are for a status only (on time, due, late; passed, at risk, failed), always with a
word or an icon; each measures at least 4.5:1 as text on `--bg` and `--surface`. A pale status surface is
`color-mix(in srgb, var(--bad) 12%, var(--surface))` with `--ink` text. A status is never shown in the accent.
