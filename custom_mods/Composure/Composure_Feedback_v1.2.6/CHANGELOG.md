# Composure Feedback v1.2.6

## v1.2.6

- Added the missing rebindable Check Composure input, default F10.
- Connected the input directly to the transient HUD show lifecycle.

## v1.2.5

- Added the requested narrow segmented/tick bar style.
- Consolidated duplicate bar/value/direction settings into universal controls.
- Added fresh defaults to recover from old profiles with both bars disabled.

## v1.2.4

- Removed persistent/always-visible HUD behavior.
- Made every display check-triggered with fade-in, hold and fade-out.
- Replaced the separate HUD mode with a `Show detailed diagnostics` toggle.

## v1.2.3

- Added a universal top-status-text MCM toggle.
- Replaced unreliable diagnostic newlines with explicit spaced pipe separators.

## v1.2.2

- Fixed the fatal `CUIXmlInit::InitFont` crash caused by unsupported `letterica14`.
- Restored the proven `letterica16` font with a non-clipping compact status row.
- Fixed the MCM mode-value reversal so Minimalist Check is value zero/default.

## v1.2.1

- Reduced the minimalist Check HUD to approximately one tenth of its prior area.
- Fixed persisted v1.1.x mode settings forcing the oversized detailed view.
- Fixed missing status text with explicit visibility and protected fallback handling.
- Separated detailed diagnostics from the compact HUD container.

## v1.2.0

- Replaced the top-right Check panel with a centred minimalist HUD.
- Added tier-based Thoughts status descriptions.
- Added fixed left loss and right gain arrow zones.
- Added five configurable net-rate intensity levels.
- Added one-second smoothing, a stable dead zone and direction hysteresis.
- Added slow reversible fade-in, hold and fade-out lifecycle.
- Added instant gain/loss bar pulses independent of the ongoing trend.
- Added position, opacity, timing and trend MCM controls.
- Preserved the detailed diagnostic mode and all non-HUD Feedback systems.
- Added safe HUD teardown/recreation on actor and level lifecycle events.
