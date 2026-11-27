# Libraries and ready-made design systems

Use a trustworthy library instead of rebuilding what it already does well, but only one whose existence you
have confirmed, and never on its default theme.

## Three rules

1. **Never from memory.** Do not write a package name, version, component name, option or import path unless
   it is in this file or you have just confirmed it. Confirm with the registry or the files:
   `npm view <package> version license` (or the package page), then read the package's own documentation for
   the exact names. If you cannot confirm that something exists, do not use it: build it by hand or choose
   another. Names change: on 26 November 2026 `@base-ui-components/react` was marked deprecated in favour of
   `@base-ui/react`, and Shoelace had been succeeded by Web Awesome.
2. **Never on defaults.** A library left on its default theme makes the page look like every other page that
   uses it. Before the first component is placed, set the library's theme from the style's token block
   (`style-library.md`): font family, text colour, background, accent, border colour, radius. The column
   "Theme it by" says where.
3. **Match the deliverable.** Many deliverables are one HTML file opened from disk. For those use only the
   rows marked "one file: yes", pasted inline (a `<script>` or `<style>` element containing the library file),
   never linked to a content delivery network, so the file still works offline. Version numbers below are what
   was current on the date checked; look up the current one before use.

## Approved list (verified 26 November 2026 from the npm registry record and each project's own repository)

"One file" means: the published stand-alone file was pasted into a single HTML page and ran with no network
request (tested in Chromium). Sizes are compressed (gzip) sizes of that file.

### Charts

| Library (package) | Licence | Version, last commit | One file | Accessibility | Use when | Not when | Theme it by |
|---|---|---|---|---|---|---|---|
| Hand-written SVG | none | | yes | Full control: real text, title, description | A handful of simple charts in a report; house templates that require it; anything that must print | Many chart types or interaction | The style tokens directly |
| Observable Plot (`@observablehq/plot`, needs `d3`) | ISC | 0.6.19, 5 November 2026 | yes, 68 KB + 91 KB | SVG with labelled marks and axes; `ariaLabel`, `ariaDescription` | Analytical charts with little code; reports | Heavy interaction, dashboards with live updates | `style: {fontFamily, fontSize}` and `color: {range: [...]}` on each plot |
| Apache ECharts (`echarts`) | Apache-2.0 | 6.1.0, 4 October 2026 | yes, 361 KB | `aria: {show: true}` writes a description (off by default); decal patterns; use `renderer: 'svg'` so text is real | Interactive dashboards, many chart types, large data | Small static pages (size) | `echarts.registerTheme(name, {color: [...], textStyle: {fontFamily}})` and pass the name to `echarts.init` |
| Chart.js (`chart.js`) | MIT | 4.6.2, 26 November 2026 | yes, 71 KB | Canvas: invisible to assistive technology unless you add `role="img"`, `aria-label` and fallback content; text cannot be measured by `uicheck.py` | Simple interactive charts where size matters | Reports that must be accessible or printed sharply | `Chart.defaults.font.family`, `Chart.defaults.color`, `Chart.defaults.borderColor`, and dataset colours |
| uPlot (`uplot`) | MIT | 1.6.32, 25 November 2026 | yes, 22 KB | Canvas, as above | Very large time series | Anything else | Series `stroke` and axis options |

Not approved without the user's agreement: Highcharts (commercial licence), ApexCharts (free only under 2
million US dollars of annual revenue; paid above that or when embedded in a product), Plotly (1 450 KB).
On phones: Swift Charts (Apple, first party), Compose or the platform's own drawing on Android, `fl_chart`
for Flutter (MIT, version 1.3.0), `victory-native` for React Native (MIT, 43.1.0).

### Icons

| Library (package) | Licence | Version, last commit | One file | Use when | Theme it by |
|---|---|---|---|---|---|
| Lucide (`lucide-static` for files, `lucide` for the script) | ISC | 1.81.0, 26 November 2026 | yes: paste each SVG inline (under 1 KB each); do not paste the whole script (116 KB) for a few icons | Default outline set | `stroke-width` and size on the SVG; `currentColor` |
| Tabler Icons (`@tabler/icons`) | MIT | 3.53.0, 25 November 2026 | yes, inline SVG | A larger outline set | As above |
| Phosphor (`@phosphor-icons/core`) | MIT | 2.1.1 (2024), repository active January 2026 | yes, inline SVG | When several weights (thin to fill) are needed | Choose one weight folder |
| Material Symbols (`@material-symbols/svg-400`) | Apache-2.0 | 0.49.0, 23 October 2026 | yes, inline SVG | Android and Material-style screens | One style (outlined, rounded or sharp) |

One family, one weight, one size per role. Icons are hidden from assistive technology; the button carries the
name. Never emoji as icons. SF Symbols: Apple's licence for use outside Apple platforms could not be read on
the date checked, so use them only in apps for Apple platforms.

### Typefaces

All of these are published under the SIL Open Font License 1.1 (commercial use, web embedding and bundling
allowed; the font may not be sold by itself) and exist as packages named `@fontsource-variable/<name>` or
`@fontsource/<name>` (each with `index.css` and the font files): Inter, Geist, Geist Mono, IBM Plex Sans, IBM
Plex Serif, IBM Plex Mono, Source Sans 3, Source Serif 4, Newsreader, Fraunces, Public Sans, Atkinson
Hyperlegible Next, Plus Jakarta Sans, Figtree, Manrope, Work Sans, Hanken Grotesk, Space Grotesk, Space Mono,
JetBrains Mono, Sora, Outfit, Instrument Sans, Instrument Serif, Cormorant Garamond, Playfair Display,
Archivo, Archivo Black, Open Sans, Roboto, Roboto Flex, DM Sans, Lora, Literata, Nunito.

- A build with a bundler: install the package and import its style sheet.
- One file, online use allowed: the user's own hosted font files.
- One file, offline: either embed the font file as a base64 `@font-face` (the Latin variable file of Inter is
  48 KB), or rely on the system stack that follows the font name in each style's token block. Say which in the
  hand-over, because line breaks differ.
- At most two families and one monospace. Load only the weights the style names.

### Web components and style sheets

| Library (package) | Licence | Version, last commit | One file | Accessibility | Use when | Not when | Theme it by |
|---|---|---|---|---|---|---|---|
| Hand-written HTML and CSS from the style tokens | none | | yes | Yours to get right | Landing pages, reports, most single files | Complex widgets (comboboxes, date pickers) | The token block |
| Open Props (`open-props`) | MIT | 1.7.23, 11 October 2026 | yes, 8 KB | Not applicable (variables only) | You want ready scales for size, shadow and easing | You already have a style's tokens | Use its variables inside your tokens |
| Pico CSS (`@picocss/pico`) | MIT | 2.1.1, repository 4 October 2026 | yes, 11 KB | Styles semantic HTML, so native behaviour is kept | Quick forms and documents with no classes | Dashboards, distinctive brands | `--pico-font-family`, `--pico-primary`, `--pico-border-radius`, `--pico-background-color`, `--pico-color` |
| Bootstrap (`bootstrap`) | MIT | 5.3.9, 26 November 2026 | yes, 30 KB + 23 KB | Depends on your markup; some default colours fail contrast and must be checked | The user's project already uses it | A page that must not look like Bootstrap, unless fully re-themed | `--bs-body-font-family`, `--bs-body-bg`, `--bs-body-color`, `--bs-primary`, `--bs-border-radius`, and button variables |
| GOV.UK Frontend (`govuk-frontend`) | MIT | 6.6.0, 23 November 2026 | style sheet yes (16 KB); its fonts and images need its assets folder | Extensively tested patterns for forms | Public-service forms for bodies entitled to the look | Any other brand: copy the patterns, not the identity | Its `--govuk-` variables |
| Tailwind CSS (`tailwindcss`) | MIT | 4.3.5, 25 November 2026 | browser build (`@tailwindcss/browser`, 74 KB) works in one file, but Tailwind says it is for development only | Not applicable | Projects with a build step | A single-file deliverable meant for production | `@theme { --color-...; --font-...; --radius-... }` mapped from the style tokens |
| daisyUI (`daisyui`) | MIT | 5.8.3, 26 November 2026 | style sheet alone is 65 KB compressed (over 1 MB raw) | Class-based; behaviour is yours | With Tailwind in a build | Single files | `--color-primary`, `--color-base-100`, `--color-base-content`, `--radius-box`, `--radius-field` |
| Alpine.js (`alpinejs`) | MIT | 3.17.5, 5 October 2026 | yes, 20 KB | Behaviour only: you supply roles and names | Small interactions in a single file | Applications | Not applicable |

Loaded from a network or a build only (they fetch their parts on demand): Web Awesome (`@awesome.me/webawesome`,
MIT core with a paid tier, 3.15.0, the successor to Shoelace) and Ionic (`@ionic/core`, MIT, 9.0.14, components
that follow iPhone and Android styling, usable from a script tag when online).

### React component libraries (a build step is required)

| Library (package) | Licence | Version, last commit | Accessibility | Use when | Theme it by |
|---|---|---|---|---|---|
| React Aria Components (`react-aria-components`) | Apache-2.0 | 1.22.1, 25 November 2026 | Follows the ARIA patterns; tested with VoiceOver, JAWS, NVDA and TalkBack; unstyled | Accessibility matters most; custom look | Your own CSS from the tokens |
| Base UI (`@base-ui/react`) | MIT | 1.9.0, 26 November 2026 | Roles, keyboard and focus handled; you add visible focus, names and contrast; unstyled | Unstyled parts with a custom look | Your own CSS from the tokens |
| Radix Primitives (`radix-ui`) | MIT | 1.8.1, 14 October 2026 | Follows ARIA practices; keyboard and focus handled; you supply labels | Existing projects that use it | Your own CSS from the tokens |
| shadcn/ui (`shadcn` command) | MIT | 4.23.1, 25 November 2026 | Inherits from the primitives it copies in | A team wants component source it owns | Its theme variables, read from the project after installation; replace every default value |
| Mantine (`@mantine/core`), MUI (`@mui/material`) | MIT | 9.8.2 and 9.6.0, November 2026 | Styled, broad coverage | Internal tools that need many ready components fast | The theme object: fonts, primary colour, radius, spacing, all from the tokens |

### Motion

| Library (package) | Licence | Version, last commit | One file | Use when |
|---|---|---|---|---|
| Plain CSS transitions and the reduced-motion media query | none | | yes | Almost always: the styles ask for 80 to 400ms state changes and nothing more |
| Motion (`motion`) | MIT | 14.14.0, 24 November 2026 | yes, 63 KB | Orchestrated sequences, gestures |
| Anime.js (`animejs`) | MIT | 4.5.0, 9 August 2026 | yes, 40 KB | Timelines on a small page |
| GSAP (`gsap`) | Free "standard licence" owned by Webflow, not open source | 3.15.1, 3 November 2026 | yes, 28 KB | Complex timelines; not inside a no-code animation tool that competes with Webflow |

Not approved: `lottie-web` (last commit November 2024).

### Phone apps

| Platform | Use | Notes |
|---|---|---|
| iPhone, native | SwiftUI with the system components, text styles and symbols | First party; follows the platform by default |
| Android, native | Jetpack Compose Material 3 (`androidx.compose.material3:material3`) | First party; theme through `MaterialTheme` (colour scheme, typography, shapes); controls already meet 48 dp |
| React Native | `react-native-paper` (MIT, 5.15.5, Material 3 components, theme through its provider), `@react-navigation/native` (MIT, 7.5.2), `react-native-safe-area-context` (MIT, 5.11.1), `react-native-reanimated` (MIT, 4.8.0), `lucide-react-native` (ISC) | All active in November 2026 |
| Flutter | The built-in Material and Cupertino widgets; `fl_chart` for charts | Built in: no extra dependency |
| Installable web app | The web rows above, plus Ionic when online | Follow `mobile.md` for safe areas and targets |

## In an audit

A page that shows a library's untouched defaults (Bootstrap blue `rgb(13, 110, 253)` buttons, default chart
colours and fonts, the library's stock radius beside a different one elsewhere) counts as a template tell for
the visual rating, and any resulting mismatch is the ordinary consistency finding. A script, style sheet or
component that the page references but that does not exist is `other`, Critical: the feature it was for is
missing.

## How these facts were checked

Versions, licence fields and package sizes: the npm registry record of each package. Last commit: the
project's own git repository. Licence wording for GSAP, ApexCharts and the Open Font License: the licence
pages. Accessibility statements: each project's own documentation. Single-file results and theming variable
names: by loading the published files in a browser and reading the style sheets. The scripts that did this
(`libcheck.py`, `libsingle.py`) are described in the test report; rerun the registry check before relying on
a version number.
