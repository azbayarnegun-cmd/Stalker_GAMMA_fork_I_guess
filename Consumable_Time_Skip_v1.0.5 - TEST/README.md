# Consumable Time-Skip v1.0.5

Standalone S.T.A.L.K.E.R. Anomaly/GAMMA addon that turns selected long-use consumables into stepped world time passage.

## Included items

- Strong alcoholic drinks: 120 in-game minutes. Detection requires `kind = i_drink` and positive `eat_alcohol`.
- Beer: explicitly excluded, including section IDs containing `beer`.
- Prepared tea and coffee: 30 minutes (`tea`, `coffee`, `brewed_coffee`).
- Ground coffee: excluded.
- Slow tobacco: 15 minutes (`hand_rolling_tobacco`, `cigar`).
- Regular/lucky/Russian cigarettes and `cigar1`/`cigar2`/`cigar3`: excluded.
- All other items remain vanilla unless registered through the public API.

## Simulation and safety

- Smooth fade to black and input lock.
- Time advances in three-minute steps with `alife():force_update()` after every step.
- Fully enclosed surge-safe cover is checked once and can protect the entire skip.
- Outdoors, each step checks hostile humans at 40 m and mutants at 20 m.
- Active/recent combat or an enemy already targeting the actor blocks consumption,
  except registered time-skip consumables during an active emission or psy-storm
  while the actor is inside GAMMA-registered event cover.
- In registered shelter, the exception covers strong alcohol, prepared tea and
  coffee, Cuban cigar, and hand-rolling tobacco.
- These consumables remain blocked during emissions/psy-storms when exposed.
- A new threat or actor hit interrupts an outdoor skip with a hard cut and short wake disorientation.
- The vanilla consumable effect is retained because the skip begins after `actor_on_item_use`.
- The pre-use safety scan is cached for the matching consumption, avoiding a duplicate full scan.
- Simulated Time Skip's active lock is respected, so two skips cannot run simultaneously.
- Slow-tobacco blackout waits for the smoking animation (8 seconds by default).
- On waking, a message reports the actual completed time. Interrupted skips report only elapsed steps.

## Composure compatibility

The included `consumable_time_skip_composure.script` is optional and automatically inert if Composure Framework is absent. No Framework file is overwritten.

When enabled in MCM, each completed time step advances active Framework modifiers, passive recovery/drain, caps and recovery locks. Timed entries are shortened by elapsed simulated time. If interrupted, only completed steps are processed.

With Composure Consumables v1.1.3 or newer, the newly consumed slow-tobacco gradual effect is deferred until waking, so its 30-second recovery is not consumed inside the time-skip.

## Installation

Install the archive as one MO2 mod. Keep it below MCM and item-animation frameworks. It uses callbacks and does not overwrite their scripts.

Requires a current GAMMA/Anomaly setup with Mod Configuration Menu. Composure Framework remains optional.

The included late compatibility bridge is intentionally narrow: it only permits
CTS-recognized alcohol, prepared tea/coffee and slow tobacco during an active
emission or psy-storm when GAMMA confirms registered shelter.

## Public and test API

```lua
consumable_time_skip.register_item("my_coffee", 30, "st_cts_coffee")
consumable_time_skip.register_meal("my_proper_meal")
consumable_time_skip.get_registered_duration("vodka")
consumable_time_skip.test(5, false)
consumable_time_skip.test(5, true)
consumable_time_skip.test_threat_scan()
consumable_time_skip.test_enclosure()
consumable_time_skip.abort("manual_test")
```

Enable the MCM tester and press F10 for a no-item test.

## Known boundaries

- Indoor safety uses GAMMA/Anomaly's surge-cover test. Semi-open shelters may remain classified as outdoors.
- Event-shelter permission can be disabled in MCM without disabling normal time-skip use.
- Dynamic strong-alcohol detection depends on the effective item configuration exposing `kind = i_drink` and positive `eat_alcohol`.
- Engine/mod systems that use only real wall-clock time require explicit compatibility. Base game time, ALife, and the included Composure bridge are advanced explicitly.
