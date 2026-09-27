# Profile: Children's Learning App (ages 4 to 9)

Touch-first learning and reading apps for young children, with parent-facing settings. These rules
override the universal defaults; everything else keeps its universal rule.

Detection: child-facing learning, reading or spelling screens, reward and streak mechanics, parent
gates, large tiles and mascots, or the user saying so.

Source of truth: the project's theme and token files and any design-system notes. When the profile and
the project's config disagree, the config wins, and the disagreement is itself worth mentioning.

Simulation personas: a five-year-old who was just handed the tablet, cannot read instructions yet and
taps imprecisely; a parent on a phone with thirty seconds between tasks, for settings and purchases.

## Overrides: touch

- **Primary game and learning targets 56 to 64px; everything else 48px minimum**, with 12 to 16px
  between targets. Below these floors: Critical.
- **Every tap gives physical feedback** and game actions are protected from double-firing.
- **Game surfaces** set `touch-action: manipulation` and `user-select: none` so rapid or long taps do
  not zoom, select or open callouts (Polish when missing: modern mobile browsers already suppress
  most double-tap zoom).

## Overrides: type and reading

- **Instructions 18px or more; reading content 20 to 24px or more**; line height at least 1.6 for
  reading text.
- **Unambiguous letterforms**: single-storey "a" and "g" preferred for beginners; I, l and 1
  distinguishable; no thin weights.
- **Never set learning words in capitals** (`text-transform: uppercase` removes the word shapes
  beginners rely on): Critical on reading content.

## Overrides: colour

- **Aim for 7:1 contrast on text children read** (WCAG AAA); 4.5 to 7:1 is a Warning here.
- **Feedback never relies on colour alone**: correct and incorrect pair colour with an icon, motion
  and, optionally, sound.

## Conduct rules (Blockers)

- **No autoplaying audio**; sound follows a tap, and mute is reachable from every screen.
- **No pressure or shame**: no streak threats, no comparisons with friends, no countdowns, no "are you
  sure you want to stop?".
- **Mistakes never punish**: neutral or warm feedback and an immediate retry; no full-screen red, no
  harsh buzzers, no "Wrong! Try harder."
- **Purchases, external links and settings sit behind a parent gate**, visually separate from the
  child's screens.
- **Rewards are short and skippable** (one to two seconds, tap to skip).
- **No vestibular triggers** (shakes, large zooms, parallax), even outside reduced-motion settings.

## Aesthetic

Follow the project's design system. Bold, solid colours, chunky borders and hard shadows are on
brand for many children's apps and are not findings in themselves; judge consistency and craft
within whatever system the project uses.

## Illustrated characters (if the app uses them)

Characters drawn side by side must share one invisible bounding box so none looks larger or floats.
For a `0 0 100 100` viewBox: content between y 8 and 92 and x 4 and 96, centred on x 50, total height
74 to 82; appendages (ears, tails) overlap the body by at least 2px and are drawn before the head so
the head covers their bases; no sharp triangles or fangs; decorations clipped to the silhouette.

## Expo or React Native

Check that press feedback and shadows have native equivalents; wrap screens with bottom controls in a
safe-area view; size pressables properly rather than relying on `hitSlop`.
