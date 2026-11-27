# Style: Soft friendly

Approachable and calm: rounded shapes, gentle tinted surfaces, clear friendly type, soft depth.

- **Use for:** Consumer apps, onboarding, family and lifestyle products, Android apps in a Material-like idiom.
- **Not for:** Finance and legal reporting, dense professional tools.
- **Schemes:** light and dark (both sets below).

| | Specification |
|---|---|
| Type | Display: Plus Jakarta Sans. Body: Plus Jakarta Sans. Figures and code: JetBrains Mono. Weights: 400, 600 and 700. Sizes (px): 12, 14, 16, 18, 22, 30, 40; body is 16; display tracking -0.01em; line height 1.5 for text, 1.1 for display. |
| Colour | A soft neutral base, one confident accent, and a pale tint of the accent for selected and highlighted surfaces. No purple-to-blue gradients. The accent may be used as text colour on the page background (5.0:1). |
| Space | 4px base; gutter 16; section 48; touch-sized controls (48px); generous padding inside cards (20). |
| Shape | Radius 12 for controls, 20 for cards, pill for chips. Borders only where needed. |
| Depth | Two soft shadows: resting and raised. |
| Imagery | Simple illustration or photography with rounded corners; one illustration style. |
| Motion | 200ms ease-out; a small scale or lift on press. |
| Charts | Rounded bar ends, accent plus two tints, large direct labels. |

**What makes it look expensive**
1. Concentric corners everywhere (inner radius = outer minus inset).
2. One icon family at one weight, optically centred.
3. Tinted surfaces instead of extra borders to group things.

**What makes it look cheap:** Emoji as icons; a different pastel on every card; shadows that are grey smudges under everything; tiny targets inside big rounded cards.

## Token block (paste first; set `--accent` and `--accent-ink` for this product, change nothing else)

```css
:root {
  --font-display: "Plus Jakarta Sans", ui-rounded, "SF Pro Rounded", "Hiragino Maru Gothic ProN", system-ui, sans-serif;
  --font-body: "Plus Jakarta Sans", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, "SF Mono", Menlo, Consolas, "DejaVu Sans Mono", monospace;
  --fs-1: 12px; --fs-2: 14px; --fs-3: 16px; --fs-4: 18px; --fs-5: 22px; --fs-6: 30px; --fs-7: 40px;
  --lh: 1.5; --track-display: -0.01em;
  --bg: #FAFAFC; --surface: #FFFFFF; --ink: #1F2233; --ink-2: #5B6078; --line: #E3E5EF;
  --accent: #0B7A6B; --accent-ink: #FFFFFF;
  --ok: #1B8038; --warn: #A16000; --bad: #D32F2F;
  --r-1: 12px; --r-2: 20px; --r-3: 28px; --border: 1px solid var(--line);
  --shadow-1: 0 1px 3px rgb(31 34 51 / 0.08); --shadow-2: 0 10px 30px rgb(31 34 51 / 0.12);
  --dur: 200ms;
}
@media (prefers-color-scheme: dark) { :root {
  --bg: #15171E; --surface: #1E212B; --ink: #EEF0F6; --ink-2: #A6ABBD; --line: #2E3240;
  --accent: #5FD4C2; --accent-ink: #0B1F1C;
  --ok: #57C984; --warn: #F0B429; --bad: #FF8A80;
} }
```

Fonts: JetBrains Mono, Plus Jakarta Sans are open-licence families (see `libraries.md`
for how to load them). In a single file with no network the system stacks after each name take over; the
style then rests on its sizes, spacing, shape and colour, which is why those are fixed here.
Measured contrast of this palette: ink on bg 15.1:1; ink on surface 15.7:1; ink-2 on bg 5.9:1; ink-2 on surface 6.2:1; accent-ink on accent 5.2:1; accent on bg 5.0:1.
`--ok`, `--warn` and `--bad` are for a status only (on time, due, late; passed, at risk, failed), always with a
word or an icon; each measures at least 4.5:1 as text on `--bg` and `--surface`. A pale status surface is
`color-mix(in srgb, var(--bad) 12%, var(--surface))` with `--ink` text. A status is never shown in the accent.
