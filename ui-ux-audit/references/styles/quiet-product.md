# Style: Quiet product

Software that gets out of the way: neutral surfaces, hairline borders, small precise type, one accent used sparingly.

- **Use for:** Software dashboards, settings, developer and productivity tools, product marketing for the same.
- **Not for:** Brands that must feel warm, luxurious or loud.
- **Schemes:** light and dark (both sets below).

| | Specification |
|---|---|
| Type | Display: Geist. Body: Geist. Figures and code: Geist Mono. Weights: 400, 500 and 600. Sizes (px): 12, 13, 14, 16, 20, 28, 40; body is 14; display tracking -0.015em; line height 1.5 for text, 1.1 for display. |
| Colour | A quiet tinted page with white surfaces on it. The accent is for the name, the main action, the current item and the key figure or series; status colours appear only with a status. The accent may be used as text colour on the page background (6.0:1). |
| Space | 4px base; gutter 16; section 64; dense but aligned; measure 70 characters for any prose. |
| Shape | Radius 6 for controls, 8 for cards, 12 for dialogs. Group with space and the surface colour first; a 1px border only on controls and where two surfaces of one colour meet. |
| Depth | One soft shadow for things that float (menus, dialogs); cards are flat white surfaces on the tinted page. |
| Imagery | The product itself: real interface, real data. |
| Motion | 150ms ease-out on hover, focus and opening; nothing loops. |
| Charts | Grey grid at low contrast, accent for the main series, two further greys; 12px labels; no fills under lines unless one series. |

**What makes it look expensive**
1. One border colour and one radius per component type, everywhere.
2. Text set in three greys with clear roles (primary, secondary, disabled) and nothing in between.
3. Numbers in tabular figures; icons at one size and stroke.

**What makes it look cheap:** A thin outlined box around everything; coloured gradients or glows on a neutral base; shadows on every card; more than one accent; large rounded pills for everything.

## Token block (paste first; set `--accent` and `--accent-ink` for this product, change nothing else)

```css
:root {
  --font-display: "Geist", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --font-body: "Geist", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --font-mono: "Geist Mono", ui-monospace, "SF Mono", Menlo, Consolas, "DejaVu Sans Mono", monospace;
  --fs-1: 12px; --fs-2: 13px; --fs-3: 14px; --fs-4: 16px; --fs-5: 20px; --fs-6: 28px; --fs-7: 40px;
  --lh: 1.5; --track-display: -0.015em;
  --bg: #F6F6F3; --surface: #FFFFFF; --ink: #171717; --ink-2: #5F5F5A; --line: #E2E2DD;
  --accent: #0A56D0; --accent-ink: #FFFFFF;
  --ok: #1B8038; --warn: #A16000; --bad: #C82D2D;
  --r-1: 6px; --r-2: 8px; --r-3: 12px; --border: 1px solid var(--line);
  --shadow-1: 0 1px 2px rgb(0 0 0 / 0.06); --shadow-2: 0 8px 24px rgb(0 0 0 / 0.12);
  --dur: 150ms;
}
@media (prefers-color-scheme: dark) { :root {
  --bg: #0E0E10; --surface: #17171A; --ink: #EDEDED; --ink-2: #A0A0A6; --line: #2A2A2E;
  --accent: #6AA5FF; --accent-ink: #06142B;
  --ok: #57C984; --warn: #F0B429; --bad: #FF8A80;
} }
```

Fonts: Geist, Geist Mono are open-licence families (see `libraries.md`
for how to load them). In a single file with no network the system stacks after each name take over; the
style then rests on its sizes, spacing, shape and colour, which is why those are fixed here.
Measured contrast of this palette: ink on bg 16.6:1; ink on surface 17.9:1; ink-2 on bg 5.9:1; ink-2 on surface 6.4:1; accent-ink on accent 6.5:1; accent on bg 6.0:1.
`--ok`, `--warn` and `--bad` are for a status only (on time, due, late; passed, at risk, failed), always with a
word or an icon; each measures at least 4.5:1 as text on `--bg` and `--surface`. A pale status surface is
`color-mix(in srgb, var(--bad) 12%, var(--surface))` with `--ink` text. A status is never shown in the accent.
