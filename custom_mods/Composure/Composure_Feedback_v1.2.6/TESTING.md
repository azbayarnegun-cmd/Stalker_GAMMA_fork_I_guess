# Composure Feedback v1.2.6 — In-game testing

## Minimalist Check HUD

1. Select `Minimalist Check` in MCM and press the configured Check Composure key.
2. Confirm the status line and bar appear at top-centre, fade in for 0.75 seconds,
   remain fully visible for four seconds, then fade out for 1.25 seconds.
3. Press Check during fade-out and confirm the same window reverses smoothly
   toward full opacity instead of duplicating or flashing.
4. Apply a slow loss and confirm one to five coloured left arrows appear left
   of the fixed bar. Apply recovery and confirm green right arrows occupy the
   equal right slot. Confirm no arrows inside the configured dead zone.
5. Apply an instant delta and confirm the bar pulses without changing the
   direction represented by the ongoing rate.
6. Change levels, press Check, and confirm exactly one HUD window appears.
7. Open GAMMA's F7 menu while the HUD is visible and confirm it is not blocked.
8. Wait without pressing Check and confirm the bar never appears or remains visible.
9. Toggle `Show detailed diagnostics`; confirm the pipe-separated report appears
   only when enabled and always fades out with the bar.
10. Confirm the bar uses 35 narrow tick segments: dim segments show the unfilled
    range and tier-coloured segments fill to the current Composure value.
11. Press F10 (or the configured Check Composure key) while in normal gameplay;
    confirm the HUD appears, then fades away. Confirm the key does not trigger
    while an inventory, dialogue or MCM screen owns input.

## v1.1.1 focused checks

1. Open HUD, Heartbeat, and Visuals list settings. Confirm every list shows a real label and never `NIL`.
2. Leave Heartbeat backend on **Reliable Scaled**, set volume to `2.00`, and press the heartbeat test key. Then verify scheduled beats at Feedback Test values `70`, `40`, `16`, and `1`.
3. Enable random Status Thoughts and press its test key several times. Treat the configured radii as an invisible ellipse: every text window must remain center-aligned and its midpoint must sit on the ellipse outline, never inside the ellipse.
4. Register at least two positive and two negative timed modifiers. Live HUD must show Gain Total, numbered gain sources, Loss Total, numbered loss sources with remaining seconds, and the authoritative Total.
5. Install Combat v1.0.1, enable Combat Test Mode, select each F6 action, and confirm Live HUD shows phase, encounter, hostiles, threat, sustained rate, deferred loss, encounter loss, start value, recovery lock, and forced-phase time.

Use a disposable save. Install Core first and disable all standalone Feedback
components to prevent duplicate scripts or sounds.

## 1. Dependency and isolation

1. Start at Composure 65 and confirm there are no missing-Framework errors.
2. Disable each MCM subsystem separately and verify the others continue.
3. Change levels and load a save; confirm no stuck HUD, vignette, FOV, thought,
   heartbeat, or breathing sound remains.

## 2. HUD and tester

1. Enable HUD tester and use minus/equals.
2. Confirm each press requests exactly -3/+3 and the displayed tier follows.
3. Open F7 while the persistent HUD is visible; the debug menu must still open.
4. Test Live Feedback and Minimal Immersion independently.
5. Enable the shared Live Test value and move its slider. HUD, breathing,
   heartbeat, visuals, and thoughts must follow without changing saved Composure.
6. Enable active modifiers and verify the HUD can show up to eight sources.

## 3. Breathing

Walk through 55, 54, 40, 39, 16, 15, 1, and 0.

- 55: no Composure breathing.
- 54-40: light `breath_1` pool.
- 39-16: heavy `breath_2` pool.
- 15-1: rapid `breath_3` pool.
- 0: no new Composure breathing cycle.

Repeat with and without a respirator. Exhaust the actor and verify physical
stamina breathing takes priority instead of two simultaneous breath cycles.

## 4. Heartbeat

Enable Heartbeat preview and test 71, 70, 55, 40, 16, 1, and 0. Confirm:

- Silence at 71.
- Barely audible onset at 70.
- Continuous BPM and volume scaling rather than tier jumps.
- Sudden-loss spike after a five-point or larger drop.
- One slower beat at zero, followed by silence.

Press F3 first; it must play one immediate beat at the configured volume. Use
F4 and try all three audio backends if the default still produces no sound.

## 5. Visuals

Use Visuals preview before gameplay testing.

- 55: no effect.
- 54: faint clear-center edge effect begins.
- Below 40: limited blur and slight darkness begin.
- 15-1: strongest configured but playable effects.
- 0: fade to black.

Use F5 to inspect targets and backend status. Test scopes, PDA, night vision,
night, underground areas, emissions, and level transitions. Confirm FOV returns
to its previous value when Visuals is disabled or suppressed.

## 6. Status Thoughts

1. Press F6 at each canonical tier.
2. Confirm positions change inside the configured center-screen region and never
   capture input. Set horizontal radius to zero to test the center-line layout.
3. Confirm group density rises from one thought to as many as five near Breaking Point.
4. Confirm each line fades independently and only occasional short panic text is all caps.
5. Apply a meaningful instant loss/gain and confirm event thoughts respect the threshold.
6. Open PDA or another full-screen UI; automatic thoughts should not open over occupied input.

Report the X-Ray log segment around any failed F4/F5 diagnostic or UI/audio error.

## Combat reaction test

Requires Composure Combat v1.0.1+ for live events.

1. Enable `Combat reaction effects`, `Combat edge pulse`, and `Combat camera pulse` in Composure Feedback - Visuals. Leave the four new edge sliders at `1.00` for the baseline test.
2. At high Composure, trigger a normal hostile bullet near miss. Confirm the edge pulse appears immediately and remains clearly visible for roughly 0.25-0.35 s.
3. Trigger an extreme near miss inside Combat's extreme radius. Confirm the edge response is clearly stronger, roughly 25-40% target opacity, and lasts about 0.40-0.60 s.
4. Take a measurable hit from a hostile human. Confirm a strong immediate edge response, roughly 30-50% target opacity, plus the shell-shock camera pulse for about 0.45-0.70 s.
5. Repeat the same events at low Composure. Confirm stronger edge intensity than at high Composure.
6. Raise only `Near-Miss Edge Strength` to `2.00`. Confirm normal near-miss edge feedback becomes much stronger while camera behavior is unchanged. Repeat for `Extreme Near-Miss Strength` and `Hit Edge Strength`.
7. Set `Combat Edge Duration` to `2.00`. Confirm only edge-pulse persistence increases; camera duration should not double.
8. Switch to Accessibility profile. Confirm combat camera movement is suppressed and the edge response is strongly reduced.
9. Spam automatic-fire near misses. Confirm the camera does not restart on every bullet and stronger hit/shock effects are not replaced by a normal fatigue pulse.
10. Enter scope, PDA, or another compatibility state that blocks camera/vignette. Confirm the corresponding combat reaction channel is suppressed.
11. Disable `Combat reaction effects`. Confirm Combat still changes Composure normally but Feedback produces no combat event pulse.
