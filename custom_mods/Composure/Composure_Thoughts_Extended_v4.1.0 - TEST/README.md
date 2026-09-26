# Composure Thoughts Extended v4.1.0

Read-only presentation addon for the modular Composure system in S.T.A.L.K.E.R. Anomaly/GAMMA.

## Requirements and load order

- Composure Core v1.0.0 or newer (framework API 2).
- Composure Feedback v1.2.6 is recommended and should load before this addon.
- Install v4.1.0 after/remove older Thoughts Extended versions; do not run multiple versions.

This archive also contains a small `composure_hud.script` compatibility override based on Feedback v1.2.6. It keeps the top HUD status and bar locked to the current condition-tier color. Short-term gain/loss remains visible through the adjacent direction arrows.

## Check Composure

Hold **X** for 0.6 seconds to start the check. Once it begins, you may release X; the sequence continues on its own, holds the complete picture for 5 seconds by default, then fades for 1 second. Automatic and event thoughts stay suppressed for 3 seconds after completion.

The top HUD already reports the condition tier, so the first check thought reports total direction instead. The remaining thoughts identify available current positive/negative sources and past positive/negative sources. Missing categories are skipped; the system never invents a cause.

- Positive direction reveals counter-pressure first, then `Even so...`, then supporting causes.
- Negative direction runs the circle in reverse and uses `But...`.
- Neutral reveals current opposing causes, then eligible memories, without a connector.
- Past memories require at least 5 points of actual accumulated Composure change from the same source.
- Maximum simultaneous real thoughts remains five.

MCM offers two check presentations:

1. **Accumulating Circle** (default): thoughts appear every 0.8 seconds by default and remain.
2. **Reflection Sequence**: thoughts appear one at a time at 1.75 times the configured sequence interval, then the complete cause picture appears.

MCM controls the sequence interval (0.4-2 seconds) and final-picture duration (2-12 seconds). Automatic/random thoughts pause while the manual check is active and resume after its completion cooldown.

## Readability timing

Automatic thoughts now last 6 seconds by default, with a 0.7-second fade-in and 1.3-second fade-out. The MCM lifetime range is 2-12 seconds.

## Detection changes

- One combined creature enumeration every 3 seconds (configurable).
- Creature type is proven with `IsMonster`/`IsStalker` before guarded `alive()` access.
- Corpse awareness: 15 m default, 90-degree forward cone, nearest eligible corpse, 25% at 15 m scaling linearly to 100% at 3 m.
- A corpse is cached only after its thought displays. The transient FIFO cache stores at most 32 IDs and clears on load, death, or level transition.
- Mutant awareness: 35 m default, nearest hostile living mutant preferred, 25% at 35 m scaling to 100% at 10 m.
- Once detected, the mutant encounter remains active without further chance rolls and ends only after 9 continuous seconds with no valid mutant, producing an aftermath thought.
- Corpse/mutant context never changes Composure.

## Needs-aware physical thoughts

The old random physical pool has been removed. A read-only cache samples supported need APIs every 5 seconds. Supported categories are hunger, thirst, sleepiness, stamina/exhaustion, overweight, and cold when a reliable installed temperature module exposes it. Missing APIs disable their category; there is no false random fallback.

Opportunities occur every 45-90 seconds, select the most severe available need, use severity chances of 25/55/85/100%, apply a 180-second per-need cooldown, and suppress physical thoughts during combat. Nothing mutates needs, inventory, health, stamina, or Composure.

## Removed

Loot Thoughts are fully removed, including inventory enumeration, state, trigger, and MCM option.

## Diagnostics

F6 cycles non-mutating branches for human/mutant corpses, mutant start/sustained/aftermath, and each needs category. Verbose diagnostics log candidate distance/chance, encounter transitions, need source/severity, physical rolls, and manual checks.

## Performance and safety

- No inventory enumeration.
- No permanent per-frame world scan.
- Creature scan: 3 seconds; needs cache: 5 seconds.
- UI frame work exists only while thought records are visible.
- All optional integrations are guarded and degrade by disabling only the unavailable feature.
