# Composure Feedback v1.2.6

Combined presentation and immersion package for the modular Composure system
for S.T.A.L.K.E.R. Anomaly/GAMMA.

## Requirement

Install **Composure Core v2.1.0 or newer** first. Feedback reads:

```lua
composure_framework.get_snapshot()
```

Feedback does not contain the Framework and does not generate gameplay stress
or recovery. The HUD tester is the only optional mutation path and is disabled
by default.

## v1.2.0 minimalist Check HUD

Pressing Framework's Check Composure key now opens a passive top-centre display:

```text
                 Holding steady.
       <<<   [==========---------]
```

- A short Thoughts status appears above the tier-coloured bar.
- One to five loss arrows occupy a fixed slot to the left.
- One to five gain arrows occupy an equal fixed slot to the right.
- The bar never shifts when direction or intensity changes.
- The ongoing net rate is smoothed for one second, uses a stable dead zone,
  and must hold a new direction briefly before the arrows switch sides.
- Instant changes pulse the bar but do not corrupt the ongoing rate indicator.
- Default timing is 0.75-second fade in, four seconds fully visible, and
  1.25-second fade out. Pressing Check again reverses or refreshes the fade.
- Position, opacity, timing, smoothing and all four arrow thresholds are
  configurable in MCM.

Minimalist Check is the new default. Detailed diagnostics remains available
and keeps the gain/loss totals, modifier list, caps, locks and Combat Stress
test information.

The HUD uses only `AddDialogToRender`; it does not register as an input owner
and does not block GAMMA's F7 debug menu. It is destroyed and rebuilt on level
changes to prevent duplicate windows.

Thoughts Extended may overwrite Feedback's Thoughts script. HUD v3.3 first
uses `composure_thoughts.get_status_description(snapshot)` when available and
then uses an identical internal fallback, so either load order remains safe.

## v1.2.1 correction

- Reduces the minimalist HUD to approximately one tenth of v1.2.0's visible area.
- Uses a 140-unit container, 70-unit bar, small status font and five-pixel arrows.
- Migrates to a new display-mode MCM key so an old saved `mode=0` cannot silently
  force the large detailed panel after upgrading.
- Explicitly shows the status control and rejects blank/whitespace status API results.
- Keeps detailed diagnostics in a separate panel that is hidden in Minimalist Check mode.

## v1.2.2 crash correction

- Replaces the unsupported `letterica14` XML font with GAMMA's proven `letterica16`.
- Enlarges the status row just enough to prevent the valid font from clipping.
- Uses a fresh `display_mode_v122` setting where `0` is Minimalist Check and
  `1` is Detailed diagnostics, matching MCM's first/default list position.

## v1.2.3 text controls

- Adds `Show top status text`, applying to both HUD modes.
- Uses spaced pipe separators for every Detailed diagnostics segment because
  some X-Ray render paths collapse newline characters inside a complex TextWnd.
- Example: `GAIN TOTAL +0.00/min  |  LOSS TOTAL +0.00/min  |  TOTAL IMPROVING`.

## v1.2.4 check-only lifecycle

- Removes the separate HUD-mode selector and retires `Live: always visible`.
- The complete HUD is now created only by Check Composure, follows the configured
  fade-in/hold/fade-out timing, and is destroyed after fading out.
- Adds `Show detailed diagnostics` as an independent toggle, disabled by default.
- When enabled, GAIN/LOSS/TOTAL, active modifiers, caps, locks and Combat Stress
  information appear with the bar and fade out with it.
- Top status text remains independently controlled by `Show top status text`.

## v1.2.5 segmented-bar correction

- Replaces the continuous bar texture with 35 narrow vertical segments.
- Uses dim full-length segments as the background and tier-coloured filled
  segments up to the current Composure value.
- Replaces the contradictory Live/Minimal bar, value and direction controls
  with one universal toggle for each.
- Uses fresh MCM keys so old profiles that disabled both bars cannot suppress
  the new Check display.

## v1.2.6 Check key fix

- Adds a rebindable `Check Composure key` to MCM, defaulting to F10.
- The key directly calls the HUD show path; Core v2.1.0 exposes a display
  registry but does not itself bind a key after Composure Main was retired.
- The segmented bar and any enabled diagnostics now appear only after this key
  is pressed and then follow the configured fade lifecycle.

Disable the standalone versions before enabling this package:

- Composure HUD v3.1.0
- Composure Audio v1.0.4
- Composure Heartbeat v1.0.0
- Composure Visuals v1.2.1
- Any earlier Status Thoughts test package

Install order:

```text
1. Composure Core v2.1.0+
2. Composure Feedback v1.2.0
3. Recovery / Combat / Consumables / Weapon Handling and other gameplay addons
```

## Included systems

### HUD

- Live Feedback and Minimal Immersion modes.
- Value, tier, direction, rate, cap, lock, and strongest active causes.
- Passive `AddDialogToRender` window that does not own gameplay input.
- Optional tester: minus/equals changes Composure by 3. Disabled by default.
- Optional active-modifier list with one to eight visible sources.
- Shared Live Test value previews every Feedback system without changing Core.

### Audio

Physical actor breathing keeps priority. Composure breathing is evaluated only
after health, stamina, movement, and other physical breathing conditions.

| Composure | Composure breathing |
|---:|---|
| 55-100 | None; physical breathing remains independent |
| 40-54 | Intermittent light stress pool (`breath_1_*`) |
| 16-39 | Heavy pool (`breath_2_*`) |
| 1-15 | Rapid panic pool (`breath_3_*`) |
| 0 | Composure breathing silent |

All normal and masked actor sound variants needed by the retained Natural
Breathing controller are bundled. No sound installer is required.

Breathing volume, randomized volume variation, and the masked-volume
multiplier are independently configurable.

Heartbeat is silent at 71-100, begins faintly at 70, and scales smoothly to
the configured maximum near one Composure. Defaults are 65-135 BPM, sudden-loss
spikes enabled, and a final slow pass-out beat. Feedback Scaled is now the
default backend, volume can be amplified to 2.0, and F3 plays a test beat.

### Visuals

- No continuous visual effects at 55-100.
- Clear-center edge vignette starts gradually at 54.
- Limited full-screen blur and tightly capped darkness begin below 40.
- Optional FOV narrowing starts at 54 and is disabled by default.
- Pass-out fade at zero.
- UI-overlay vignette with `vignette_control` fallback.
- Separate edge-intensity, inward-spread, and maximum-opacity settings.
- Compatibility API for scopes, binoculars, PDA, night vision, scripted
  cameras, psy effects, emissions, underground areas, and night conditions.
- Combat event reactions consume `combat.near_miss` and `combat.actor_hit` from
  Composure Combat without changing Combat detection or Core state.
- Combat edge pulses attack immediately on the event frame, then fade through
  the normal Visuals update loop instead of waiting for the next 100 ms tick.
- Normal near misses target roughly 12-22% edge opacity for 0.25-0.35 s;
  extreme near misses target 25-40% for 0.40-0.60 s; hostile human hits target
  30-50% for 0.45-0.70 s before user scaling and safety caps.
- Reaction strength scales with current Composure. High Composure stays subtler;
  low Composure produces a stronger response. Separate MCM controls now scale
  normal near-miss, extreme near-miss, and hit edge strength plus edge duration
  without directly changing camera movement. Accessibility suppresses combat
  camera motion and strongly reduces the edge pulse.

Profiles: Subtle, Default, Cinematic, and Accessibility.

### Status Thoughts

- First-person thoughts appear at randomized points inside a center-screen region.
- Horizontal and vertical radii are configurable; horizontal radius zero restores the invisible center line.
- One to five thoughts can fade independently in a single group.
- Lower Composure increases frequency and group density.
- Automatic triggering uses a cooldown followed by a tier-weighted chance roll.
- Meaningful instant Composure changes can trigger contextual thoughts.
- Low and Breaking Point can include occasional short all-caps panic words.
- Only one group is active at once; a stronger event replaces the current group.
- F6 displays a test group without changing Composure.

## Default diagnostic and test controls

| Control | Function |
|---|---|
| `-` / `=` | HUD tester -3/+3 when explicitly enabled |
| F3 | Immediate heartbeat test |
| F4 | Heartbeat diagnostics |
| F5 | Visuals diagnostics |
| F6 | Status Thoughts test group |

Audio, Heartbeat, HUD, Visuals, and Thoughts each retain an independent MCM
enable switch. A failure in one system should not stop the other systems.

## Audio asset note

The actor audio pool was supplied for this build from the same upstream actor
audio set used by the earlier Natural Breathing package. Before public
redistribution, retain the upstream attribution and independently verify that
your intended distribution complies with its audio licensing terms.

## Release status

This package has automated structural and behavioral validation. X-Ray render,
PPE, FOV, and audio-backend behavior still require the in-game checklist in
`TESTING.md` before calling the package live-stable.

## v1.0.1 hotfix

- Hardened heartbeat playback, changed the default backend, and added F3 testing.
- Expanded heartbeat volume from 0-1 to 0-2 and disabled legacy auto-muting by default.
- Added breathing volume, variation, and masked-volume settings.
- Added a shared live test Composure value for all Feedback systems.
- Expanded the HUD modifier list from three to eight sources.
- Added genuinely randomized Status Thought positions and region-size settings.
- Expanded vignette intensity and separated edge darkness from inward spread.

## v1.0.2 hotfix

- Status Thought midpoints now spawn only on the configurable invisible ellipse outline; the interior is never sampled. Text remains center-aligned around each anchor.
- Live HUD now separates Gain and Loss sources, shows their totals, timed-source seconds, and the authoritative net total.
- Feedback Test now preserves live modifier/rate diagnostics while overriding only the presentation value and tier.
- Live HUD can show detailed Combat Stress test state from Combat v1.0.1.
- Heartbeat backend 0 now uses GAMMA's proven normal 2D playback path with live volume/frequency control.
- Rebuilt Heartbeat, HUD, and Visual list settings with numeric localized entries, removing `NIL` list labels.
- Corrected formatted Feedback diagnostics so values replace `%` placeholders in X-Ray logs.

## v1.1.0

- Added presentation-only reactions for Composure Combat `combat.near_miss` and `combat.actor_hit` events.
- Normal near misses: 0.15-0.25 s fatigue jolt plus a subtle edge pulse.
- Extreme near misses: 0.28-0.40 s stronger shock pulse.
- Human actor hits: 0.27-0.42 s shell-shock pulse.
- Reaction strength scales with current Composure and optional MCM intensity.
- Added camera spam protection and stronger-effect priority so a normal near miss cannot overwrite an active hit reaction.
- Combat detection and Composure values remain owned by Combat/Core; Feedback only presents the event.

## v1.1.1

- Increased combat edge-pulse readability after live GAMMA testing showed the v1.1.0 pulses were easy to miss.
- Edge pulses now render immediately when the Combat event arrives instead of waiting for the next Visuals update tick.
- Normal near miss: target 12-22% edge opacity, 0.25-0.35 s.
- Extreme near miss: target 25-40% edge opacity, 0.40-0.60 s.
- Hostile human actor hit: target 30-50% edge opacity, 0.45-0.70 s.
- Added `Near-Miss Edge Strength`, `Extreme Near-Miss Strength`, `Hit Edge Strength`, and `Combat Edge Duration` MCM controls.
- Edge-specific controls do not directly change camera movement, so edge feedback can be amplified independently.
- Existing compatibility blocks, Accessibility behavior, diminishing near-miss stages, camera spam protection, and stronger-effect priority are retained.
