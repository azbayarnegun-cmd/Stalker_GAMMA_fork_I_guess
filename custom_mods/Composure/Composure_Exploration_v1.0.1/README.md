# Composure Exploration v1.0.1

Environmental Composure pressure and persistent Expedition Strain for STALKER GAMMA.

## Requirements

- Composure Core / Framework API 2
- MCM (for configuration)
- Composure Recovery is recommended, but not required
- Unified Simulated Time v1.1.0 is recommended for the level-transition integration

## What it does

- Renames the old design profile `surface_day` to `surface_outdoor`.
- Applies workbook-authored base loss rates: Surface `0.25`, Underground `0.75`, Deep Lab `1.50` Composure per in-game minute.
- Adds night, weather, anomaly, companion, lit-campfire, and Expedition Strain adjustments.
- Enforces a workbook-authored maximum of `5.00` loss/minute and a Composure floor of `50`.
- Pauses direct exploration loss in combat and briefly after damage/firing.
- Maintains a Framework recovery lock while exploration pressure is active.
- Persists Expedition Strain across saves and levels.

## Expedition Strain

| Unsafe exposure | Multiplier |
|---:|---:|
| 0-59 min | x1.00 |
| 60-119 min | x1.05 |
| 120-179 min | x1.15 |
| 180-239 min | x1.20 |
| 240-359 min | x1.30 |
| 360-479 min | x1.40 |
| 480+ min | x1.50 |

Friendly bases remove four exposure minutes per elapsed minute and can reach zero. A lit-campfire rest removes two exposure minutes per rested minute, but only 60 minutes per allowance and never below 60 exposure minutes. The allowance rearms after 120 minutes of unsafe exploration.

## Time skips

- Outdoor/unsafe consumable skips continue exploration and exposure.
- Campfire rest suppresses direct exploration loss and applies capped exposure relief.
- Level-transition blackout scales all Framework Composure adjustments, positive or negative, to `x0.25` while Expedition exposure advances at `x1.00`.
- The transition rule is attached at runtime to `simulated_time.advance`; no Unified Time Skip file is overwritten.

## Anomalies

The included detector performs a conservative nearby-object scan for anomaly-zone section names. GAMMA anomaly implementations that do not expose zone objects to `level.iterate_nearest` can integrate through:

```lua
composure_exploration.set_anomaly_distance(distance_metres, actor_is_inside)
composure_exploration.clear_anomaly_distance()
```

Only the strongest anomaly band applies. Defaults are 10-25 m `+0.25/min`, below 10 m `+0.50/min`, inside `+0.75/min`, followed by a five-second exit grace.

## Public integration API

```lua
composure_exploration.get_exposure_minutes()
composure_exploration.reduce_exposure(minutes, source_id)
composure_exploration.add_exposure(minutes, source_id)
composure_exploration.set_level_profile("surface_outdoor" | "underground" | "deep_lab" | "auto")
composure_exploration.begin_level_transition()
composure_exploration.end_level_transition()
composure_exploration.get_diagnostics()
```

Consumables can call `reduce_exposure` in future spreadsheet-driven updates without changing this module.

## MO2 order

1. Composure Core
2. Composure Recovery
3. Composure Consumables Sheet Driven
4. Composure Feedback
5. Composure Combat
6. Composure Thoughts Extended
7. **Composure Exploration**
8. Consumable Time Skip
9. Unified Simulated Time GAMMA

Exploration uses unique files and replaces no existing mod. Its position before the time-skip packages makes ownership clear; the runtime bridge remains compatible even though Unified loads later.

## Diagnostics

Press `F7` to print/show the current profile, rate, exposure minutes, nearest detected anomaly, lifecycle state, elapsed game minutes, clock sample count, Recovery-lock state, and transition state. Debug logging is optional in MCM.

## v1.0.1 lifecycle fix

- Replaces the retained `CTime` reference with an immutable numeric game timestamp.
- Adds explicit `level_changing`, `arrival_grace`, `clock_wait`, `active`, and `inactive` lifecycle states.
- Uses a five-real-second arrival grace and requires two valid clock samples before resuming.
- Applies no exploration loss, exposure, or Exploration recovery lock during arrival initialization.
- Clears stale locks before level changes, loads, deaths, and clock faults.
- A six-second clock watchdog releases Recovery and waits safely for the clock instead of freezing Composure.
- Re-registers the transition adjustment policy after destination loading.
- Discards the destination-loading time gap so transition exposure cannot be counted twice.

## Balance source

Built from `Composure_Exploration_v1.0.0_Balance(1).xlsx`. The workbook values are the source of truth; finalized post-sheet design additions are documented in `BALANCE_ADDITIONS.md`.
