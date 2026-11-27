# Profile: Mobile Apps

Phone apps of any kind: native iPhone and Android, React Native, Flutter, and web apps that are installed or
used full screen on a phone. These rules override the general ones; everything else keeps its general rule.
Read `mobile.md` with this profile: it holds the platform rules, the measurement path and the sources.

Detection: phone-sized screens, a bottom bar or top app bar, screens that push and pop, sheets, a web manifest
or `apple-mobile-web-app-capable`, Swift, Kotlin, Dart or React Native source, device screenshots, or the user
saying so. A children's app uses `profile-kids-app.md` on top of this one.

Source of truth: the platform the screen claims to follow. Decide first: iPhone conventions, Android
conventions, or one brand system used on both. Judge every screen against that one choice and name it in the
report ("Profile: Mobile app, iPhone conventions, flow of 3 screens").

Main task: the task the flow of screens exists for (send a payment, book a class). The main action is the
control that completes it.

Simulation personas: someone standing on a train holding the phone in one hand, thumb only, with a poor
connection; the same person with the system text size turned up and dark appearance on; a first-time user who
has never seen the app and reads nothing.

## Overrides: a flow is one audit

- Audit every screen of the flow together: one report, one score, each finding listing the screens it is on.
  Run `uicheck.py` with all screens in one call so that `style-drift` is checked.
- A defect on one screen of the main task counts for the flow.

## Overrides: touch first

- `target-touch` applies to every control: 44px on iPhone and phone-width web, 48px on Android.
- `hover-only` and `gesture-only` are checked on every screen: there is no hover, and a gesture is never the
  only way.
- `control-obscured`: the last item of every list and the last control of every form must scroll clear of fixed
  bars and floating buttons.

## Overrides: the system's share of the screen

- `safe-area` is checked whenever the screen runs edge to edge (`viewport-fit=cover`, any native screen).
- `zoom-blocked`, `input-zoom` and `text-scaling` are checked on every screen with text entry or reading.
- Both appearances are measured when the app has dark styles; a defect in one appearance keeps its ordinary code.

## Overrides: navigation

- Every screen answers: where am I (`nav-current`), how do I go back (`nav-back`: Critical on iPhone and web,
  Warning on Android), how do I reach the main sections.
- A bottom bar holds three to five destinations and is for navigation only (`nav-structure`).
- Conventions of the other platform on a screen are `platform-mix`.

## Overrides: states that phones meet daily

- Empty, loading, offline and error states are part of the flow. One the screens show broken is `state-empty`
  or `state-error`; one the input cannot show is listed under Verify as `offline-state`.
- A permission asked at launch, or with no reason, is `permission-timing`.

## Visual quality for apps

The rating is advice, not scored. A good app screen is quiet: one title, one main action, system-like
controls, generous touch spacing, and one style held on every screen. Platform chrome copied from the other
platform, or web cards and hover effects on a phone, are the tells here.

## What not to flag here

Platform-standard patterns used as the platform documents them (a tab bar, a large title, a floating action
button on Android); 11 to 13 point secondary text on iPhone; the absence of a desktop layout; the absence of
a hamburger menu.
