# QA status — v1.2.6

Automated checks cover package structure, Core separation, XML parsing, MCM
localization, bundled OGG headers, expected breathing pools, heartbeat asset,
consumer API boundaries, Status Thoughts density/cooldown rules, and the main
Audio/Visual threshold contracts.

Release results:

- 132/132 static package checks passed.
- 41/41 deterministic behavior-model checks passed.
- 15/15 deterministic HUD-model checks passed.
- 135/135 OGG assets decoded as mono 44.1 kHz Vorbis metadata.

Static validation cannot prove runtime availability of GAMMA's selected sound
backend, HUD renderer, stock PPE files, console vignette command, or FOV API.
Complete `TESTING.md` before promoting this release from test-ready to
live-stable.

## v1.1.1 combat-reaction contract

- Feedback registers listeners for `combat.near_miss` and `combat.actor_hit`.
- Listener code is read-only with respect to Composure Framework state.
- Near-miss metadata `extreme` selects the stronger reaction path.
- Actor-hit metadata `health_loss_percent` modulates hit severity.
- Edge pulses merge with the existing passive vignette renderer, attack immediately, and decay automatically.
- Default edge targets are 12-22% normal near miss, 25-40% extreme near miss, and 30-50% actor hit before user scaling/safety caps.
- Separate edge-strength and edge-duration controls do not directly alter camera movement.
- Camera reactions respect compatibility camera blocks and Accessibility profile.

## v1.2.0 HUD contract

- The passive Check HUD remains render-only and never registers as an input owner.
- The bar is centred in a fixed 460-pixel layout with equal five-arrow side zones.
- Ongoing trend uses Framework `net_rate`, one-second smoothing, a configurable
  dead zone and a direction-change delay.
- Instant deltas only pulse the bar and do not alter arrow direction.
- Fade-in, hold and fade-out are separate reversible lifecycle states.
- Thoughts status lookup is protected and has a built-in fallback for the
  current Thoughts Extended overwrite pattern.
- Level changes and actor destruction remove the window before it can rebuild.
