# Mobile: iPhone, Android, cross-platform and installable web apps

A phone screen is not a narrow web page. The user holds it in one hand, touches instead of pointing, cannot
hover, loses part of the screen to the system, changes the text size, and loses the network. The usual AI
failure is web habit carried over: hover-dependent controls, small targets, desktop navigation shrunk down,
and the two platforms' conventions ignored or mixed. Sources and dates are at the end; nothing here is from
memory.

## Which path

| What you were given | Do this | What you get |
|---|---|---|
| Web technology: mobile web page, installable web app, web view, a web build of a React Native or Flutter app | `uicheck.py screen1.html screen2.html --device iphone` (or `android`), all screens of the flow in one call | Measured: everything below marked M |
| Native source (Swift, Kotlin, React Native, Flutter) with no way to run it | Read the code against the signals table below, and ask for simulator, emulator or device screenshots of each screen in light and dark | Code facts are confirmed; anything visual is Verify until screenshots arrive |
| Screenshots only | `shotcheck.py shots/*.png --platform ios` (or `android`) | Measured from pixels and estimates, each labelled; score provisional |

Screenshots come from the simulator's or emulator's own screenshot function or from a real device. Ask for one
per screen and state, at the device's native resolution, uncropped, with the status bar showing.

## Measured or estimated

| Fact | Web technology (`uicheck --device`) | Screenshot (`shotcheck`) | Native source only |
|---|---|---|---|
| Text contrast | M | M (pixels of each text box) | Verify |
| Text size | M (rendered pixels) | M in pixels; points are an estimate unless `--scale` is given | From code: fixed sizes |
| Target size | M, against 44 or 48 | Estimate (an image cannot say what is tappable) | From code: fixed frames |
| Safe areas | M (insets are injected, then controls inside them are listed) | M when the home indicator is found in the image; otherwise not assessed | From code: inset handling |
| Control covered by a bar or floating button | M (`control-obscured`) | Estimate from one frame | Verify |
| Hover-only controls, zoom blocked, field font size | M | Cannot be seen | From code |
| Navigation, back, current place, platform conventions | Look at the screenshots | Look | Read the navigation code |
| Text scaling to 200%, keyboard covering fields, offline states, permission timing | Verify unless a state is provided | Verify | From code |
| Screen-reader output, real touch feel, real device rendering | Never: say so | Never | Never |

The safe-area insets that `uicheck.py` injects (59 top and 34 bottom for `iphone`, 24 and 24 for `android`) are
test values, not platform constants: the check is whether the layout moves its controls out of whatever the
device reports. It runs only when the page sets `viewport-fit=cover`, because without it Safari keeps the page
inside the safe area by itself.

## Rules

Each rule: what to build, what to check, the registry code.

### Safe areas and edges  [`safe-area`, `control-obscured`]
- Controls and text stay out of the status bar, camera cut-out and home-indicator areas; backgrounds may
  extend to the edges. Apple: respect the system safe areas. Android 15 and later draw every app edge to edge:
  pad tappable views with the system-bar insets, scrolling content with system-bar and cut-out insets, and
  swipeable views with the system-gesture insets.
- Web: `viewport-fit=cover` needs `padding: env(safe-area-inset-*)` on fixed bars. React Native: safe-area
  insets from `react-native-safe-area-context`. Flutter: `SafeArea`. SwiftUI and Compose respect insets unless
  the code turns them off.
- Fixed bottom bars and floating buttons never cover the last item: the scrolling area ends with padding equal
  to the bar plus the inset.

### Touch targets and reach  [`target-touch`, `target-small`]
- iPhone: 44 x 44 points by default (28 is Apple's stated minimum, not a goal), about 12 points between
  bordered controls. Android: at least 48 x 48 density-independent pixels. Web at phone width: 44px.
- Put the main action where it can be reached without changing grip: the centre and lower part of the screen.
  The top corners cost a stretch, so they suit back and secondary actions. (Observation of 1 333 people: 49%
  one-handed, 36% cradled, 15% two-handed; the author later corrected the reach maps: people touch mostly the
  centre.)

### Navigation patterns  [`nav-back`, `nav-current`, `nav-structure`, `platform-mix`]

| Pattern | Use it for | iPhone | Android |
|---|---|---|---|
| Bottom bar | Moving between three to five top-level sections of equal weight | Tab bar: navigation only, never actions; always visible except under a modal; short one-word label plus symbol; avoid a "More" overflow | Navigation bar: three to five destinations, the same on every screen, the selected one highlighted |
| Stack (push) | Going deeper into one section | Toolbar with the standard back button and symbol (not the word "Back"), a short title | Top app bar with an Up arrow; the system back gesture must also work |
| Sheet | One short task tied to the screen behind it | Medium and large heights with a grabber; always Cancel or Back paired with Done; one sheet at a time | Bottom sheet or full-screen dialog with a close control |
| Drawer | Many destinations that do not fit a bar | Not a phone convention; use a tab bar, or a sidebar on iPad | Navigation drawer or rail on larger windows |

Every pushed screen and every modal has a visible way back or out (`nav-back`): on iPhone this is Critical
because nothing else on the device goes back; on Android it is a Warning because the system gesture exists.
The current section is always marked (`nav-current`).

### Gestures  [`gesture-only`, `hover-only`]
- Every gesture has a visible control that does the same thing: a delete button as well as swipe to delete, a
  Back button as well as the edge swipe. Standard gestures keep their standard meaning. Nothing depends on
  hover: there is no hover on a phone.

### Text scaling  [`text-scaling`, `zoom-blocked`, `input-zoom`]
- iPhone: use the system text styles (Body 17, Subhead 15, Footnote 13, Caption 12 and 11 points at the
  default size); never below 11 points; layouts survive 200% (stack side-by-side items, let rows grow).
  Android: text in scale-independent pixels; the system scales to 200%; test at that size.
- Web: never `user-scalable=no` or `maximum-scale` below 2; fields at 16px or more on iPhone so the page does
  not zoom on focus (browser behaviour, observed; not in a standard).

### Keyboard  [`keyboard-cover`]
- The focused field and the control that submits it stay visible above the keyboard: scroll the form, do not
  pin the submit button to the bottom of a fixed-height screen. Use the right keyboard for the field (email,
  number). React Native: `KeyboardAvoidingView` or keyboard-aware scrolling. Flutter: let the scaffold resize.

### Platform conventions that differ  [`platform-mix`]

| | iPhone | Android |
|---|---|---|
| Back | Back button at top left, symbol only | Up arrow at top left plus system back gesture |
| Title | Centred or large title that shrinks on scroll | Left-aligned title in the top app bar |
| Main action | One prominent button at the trailing edge of the toolbar, or in the content | Floating action button, or a button in the content |
| Bottom bar | Tab bar | Navigation bar |
| Switches, pickers, alerts | System controls | Material controls |
| Icons | SF Symbols style | Material Symbols style |
| Fonts | System font (San Francisco) | System font (Roboto) |

A cross-platform app either follows each platform (preferred for system controls and navigation) or uses one
consistent brand system on both; what it must not do is mix the two platforms on one screen.

### Offline and slow network  [`offline-state`, `state-empty`]
- Show placeholders at once and replace them as content arrives; a determinate bar when the time is known, a
  spinner when it is not. Every network view has an offline or failed state with a retry, and an empty state
  that says why it is empty and what to do.

### Permissions  [`permission-timing`]
- Ask when the user starts the feature that needs it, never at launch unless the app cannot work without it;
  say why in one specific sentence; keep the app usable after a refusal. A screen shown before the system
  prompt has one button ("Continue"), no "Allow" wording and no imitation of the system prompt.

### Light and dark  [`contrast-text` with "dark" in the location]
- Follow the system setting (no app-only switch); every colour has a light and a dark value; check contrast in
  both: at least 4.5:1. Images and icons are checked in both.

## Signals in native source

| Look for | Means | Code |
|---|---|---|
| React Native: `allowFontScaling={false}`, a low `maxFontSizeMultiplier`, fixed heights on text containers | Text cannot grow | `text-scaling` |
| React Native: no safe-area handling (`react-native-safe-area-context`) around screens with bars | Bars under the system areas | `safe-area` |
| React Native: a `Pressable` smaller than 44 with no `hitSlop`; no `accessibilityLabel` on icon buttons; no `KeyboardAvoidingView` or scrolling on forms | Small or unnamed controls; keyboard over fields | `target-touch`, `name-missing`, `keyboard-cover` |
| Flutter: `TextScaler.noScaling`; screens with bars and no `SafeArea`; a small tappable icon with no semantic label | As above | as above |
| SwiftUI: fixed point sizes instead of text styles; `ignoresSafeArea` on content; fixed frames under 44 points on buttons; `dynamicTypeSize` capped at a small size | As above | as above |
| Compose: text sizes not in scale-independent pixels; a clickable element under 48 dp; `contentDescription = null` on a clickable icon; no inset handling after `enableEdgeToEdge()` | As above | as above |
| Any: a swipe or long-press handler with no button that does the same | Gesture only | `gesture-only` |
| Any: permission request in the app's start-up code | Asked at launch | `permission-timing` |

Report these with the file and line you read. They are facts about the code; what the screen looks like stays
under Verify until there is a screenshot.

## Sources (checked 26 November 2026)

- Apple Human Interface Guidelines: Accessibility (9 June 2025), Layout (9 September 2026), Tab bars (8 June
  2026), Toolbars (16 December 2025), Sheets (24 March 2026), Modality, Gestures (28 October 2026), Typography
  (16 December 2025), Privacy, Dark Mode, Loading. https://developer.apple.com/design/human-interface-guidelines/
- Android Developers: Display content edge-to-edge (10 November 2026), Accessibility in apps (10 November 2026),
  Navigation bar (18 November 2026), Predictive back gesture, Request runtime permissions, Android 14 features
  (font scaling). https://developer.android.com/
- Material Design 3 site (m3.material.io) could not be read by the fetch tool; Material facts here come from
  Android Developers.
- React Native 0.88: Accessibility, Text, Pressable, KeyboardAvoidingView. Flutter: Accessibility (31 July 2026), TextScaler, SafeArea.
- Apple Developer Documentation: SwiftUI `ignoresSafeArea(_:edges:)`, `dynamicTypeSize(_:)`.
- WebKit, "Designing Websites for iPhone X" (safe-area insets and `viewport-fit`).
- W3C, Web Content Accessibility Guidelines 2.2, 2.5.8 Target Size, 2.5.1 Pointer Gestures, 1.4.4 Resize Text.
- Steven Hoober, "How Do Users Really Hold Mobile Devices?", UXmatters, 2013.
