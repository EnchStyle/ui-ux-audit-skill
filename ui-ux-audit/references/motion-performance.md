# Categories 12 and 13: Motion, Performance and Layout Shift

Severities are set only in `severity-registry.md`; the codes in brackets below are its rows.

## Category 12: Motion

- **Every animation has a job**: orient (where did this come from), confirm (the tap registered) or
  relate (this expanded from that). Decoration that loops forever is noise and a template tell.
- **Durations**: 150 to 300ms for interface transitions, 300 to 500ms for page-level ones; under 100ms
  reads as a glitch, over 500ms as lag.
- **Easing**: ease-out for entering, ease-in for leaving, ease-in-out for moving; linear only for
  progress and marquees.
- **Choreography**: one orchestrated moment beats scattered effects; staggers of 20 to 50ms with a
  capped total.
- **Reduced motion is required** (`motion-reduce`): wrap non-essential motion in
  `@media (prefers-reduced-motion: no-preference)` or override it under `reduce`; remove parallax,
  large zooms, shakes and autoplaying carousels; keep simple fades.
- **Cheap properties**: animate `transform` and `opacity` for movement. Short colour or shadow
  transitions on hover (200ms or less) are fine. Animating width, height, top, left, margin or padding
  forces layout every frame.
- **No layout shift from state changes**: expanding elements animate inside reserved space.
- **Interruptible**: reversing a hover mid-animation reverses smoothly; animations never block input.

## Category 13: Performance and layout stability

- **Every image and embed has dimensions** (`width` and `height` attributes or `aspect-ratio`). Unsized
  media is the main cause of layout shift. A fast local render hides the shift, so the script tests whether space
  is reserved (`media-unsized`).
- **Reserved space for late content**: banners, embeds and async panels render into boxes of their
  final size; content injected at the top after load (a cookie bar pushing the page down) is `other`, Critical: the control the user was about to press moves.
- **Targets** (Core Web Vitals, 75th percentile): Largest Contentful Paint 2.5s or less, Interaction to
  Next Paint 200ms or less, Cumulative Layout Shift 0.1 or less. Measure when the page can run;
  otherwise report risk patterns under Verify.
