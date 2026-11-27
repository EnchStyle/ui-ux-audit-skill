# Style: Glass layered

Content first, controls floating above it on translucent material, as current iPhone software does.

- **Use for:** iPhone and iPad apps, media and photo-led apps, overlays on rich content.
- **Not for:** Text-heavy tools, Android-first products, low-end devices, anything where contrast cannot be guaranteed.
- **Schemes:** light and dark (both sets below).

| | Specification |
|---|---|
| Type | Display: Inter. Body: Inter. Figures and code: JetBrains Mono. Weights: 400, 600 and 700. Sizes (px): 11, 13, 15, 17, 22, 28, 34; body is 15; display tracking -0.01em; line height 1.4 for text, 1.1 for display. |
| Colour | Solid, legible content surfaces; translucency only on the navigation layer (bars, sheets, floating controls). One accent. The accent may be used as text colour on the page background (4.8:1). |
| Space | 4px base; gutter 16; section 32; 44px controls; system margins of 16 to 20. |
| Shape | Radius 12 for controls, 20 for cards, 28 for sheets, full pill for floating bars. |
| Depth | Translucent navigation bars: background at 72% opacity with a 20px blur and a hairline edge; content never on glass. A pinned action (a button that stays at the bottom) sits on an opaque bar with a hairline, so rows never show through or around it. |
| Imagery | The subject itself: photographs, or one icon or illustration family drawn for this product (the dish, the parcel, the place) in the accent and its tints; the bars float over it. |
| Motion | 200 to 300ms spring-like ease; honours the reduced-motion setting with a plain fade. |
| Charts | Solid surfaces under charts; system-like colours; large touch targets on points. |

**What makes it look expensive**
1. Text on glass still measures 4.5:1 against the worst pixels behind it.
2. Glass on one layer only; everything else solid.
3. Platform type sizes (17 body, 13 footnote) and 44px targets.

**What makes it look cheap:** Glass cards for content; blur over busy images with thin text; glass everywhere on a web dashboard; coloured glows; the stock blue for every element, status included.

## Token block (paste first; set `--accent` and `--accent-ink` for this product, change nothing else)

```css
:root {
  --font-display: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --font-body: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, "SF Mono", Menlo, Consolas, "DejaVu Sans Mono", monospace;
  --fs-1: 11px; --fs-2: 13px; --fs-3: 15px; --fs-4: 17px; --fs-5: 22px; --fs-6: 28px; --fs-7: 34px;
  --lh: 1.4; --track-display: -0.01em;
  --bg: #F2F3F7; --surface: #FFFFFF; --ink: #0F1115; --ink-2: #5A6070; --line: #DADDE5;
  --accent: #0B63E5; --accent-ink: #FFFFFF;
  --ok: #1A7A35; --warn: #995B00; --bad: #C82D2D;
  --r-1: 12px; --r-2: 20px; --r-3: 28px; --border: 1px solid var(--line);
  --shadow-1: 0 1px 2px rgb(0 0 0 / 0.06); --shadow-2: 0 12px 32px rgb(0 0 0 / 0.18);
  --dur: 250ms;
}
@media (prefers-color-scheme: dark) { :root {
  --bg: #0C0D10; --surface: #17191E; --ink: #F3F4F7; --ink-2: #A5ABB8; --line: #2A2E37;
  --accent: #6AA9FF; --accent-ink: #06101F;
  --ok: #57C984; --warn: #F0B429; --bad: #FF8A80;
} }
```

Fonts: Inter, JetBrains Mono are open-licence families (see `libraries.md`
for how to load them). In a single file with no network the system stacks after each name take over; the
style then rests on its sizes, spacing, shape and colour, which is why those are fixed here.
Measured contrast of this palette: ink on bg 17.0:1; ink on surface 18.9:1; ink-2 on bg 5.7:1; ink-2 on surface 6.3:1; accent-ink on accent 5.3:1; accent on bg 4.8:1.
`--ok`, `--warn` and `--bad` are for a status only (on time, due, late; passed, at risk, failed), always with a
word or an icon; each measures at least 4.5:1 as text on `--bg` and `--surface`. A pale status surface is
`color-mix(in srgb, var(--bad) 12%, var(--surface))` with `--ink` text. A status is never shown in the accent.
