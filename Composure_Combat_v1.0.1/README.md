# Composure Combat v1.0.1

Standalone human-firefight pressure module for S.T.A.L.K.E.R. GAMMA.

It observes combat, submits explicit Composure changes to Core and reports
whether recovery is unsafe. It does not own the authoritative value and does
not contain HUD, audio, visual or weapon-handling effects.

## Requirements and installation

1. Install **Composure Core v2.1.0**.
2. Install this package after Core in MO2.
3. Install **Composure Consumables v1.0.0** after Combat if both are used.
4. Do not enable the retired `composure_combat_stress_addon_v5` simultaneously.

The module requires `composure_framework` API 2 and fails closed when Core is
missing.

## v1 ownership boundary

Combat v1 tracks human stalkers only:

- Human NPCs actively targeting the actor.
- Human-fired bullets passing near the actor.
- Health removed by human NPC attacks.
- Human hostile count, proximity limit and held-weapon threat.
- Sustained human firefights, combat ending, recovery lock and rebound.

Mutants, anomalies, radiation, psy damage, weather, hunger, falls and self
damage are intentionally excluded. A later mutant module can submit
`source_type = "mutant_combat"` without changing this human system.

## Three phases

| Phase | Typical condition | Default sustained pressure |
|---|---|---:|
| Alert | One confirmed human threat | -0.10/s |
| Engaged | Multiple threats or stronger combined weapon threat | -0.20/s |
| Overwhelmed | Four or more threats or very high threat score | -0.30/s |

There is a two-second grace period before sustained drain begins. Discrete hits
and near misses still react immediately. Phase changes are smoothed by threat
TTL and a ten-second combat-end inertia.

The maximum combined continuous loss is **-0.30/s** by default. This cap covers
both sustained firefight pressure and deferred hit/near-miss stress.

## Event stress: 30% immediate, 70% deferred

Every hit or near miss produces one raw stress value:

```text
Raw event stress
├── 30% requested immediately
└── remaining 70% placed in a deferred queue
```

If the instant window is already capped, the blocked instant share moves into
the deferred queue instead of disappearing.

Defaults:

- Instant cap: **-5 per rolling second**.
- Instant cap: **-7.5 per rolling three seconds**.
- Deferred duration: **30 seconds** nominally.
- Continuous drain cap: **-0.30/s**.

During a full Overwhelmed phase, sustained pressure can occupy the entire
continuous budget. Deferred stress waits and drains after pressure eases. This
keeps automatic fire or several rapid hits from causing an instant pass-out.

## Human hit values

| Health removed by one hit | Raw stress |
|---:|---:|
| Up to 5% | -1.0 |
| 5-10% | -1.5 |
| 10-15% | -2.5 |
| 15-20% | -3.5 |
| Over 20% | -5.0 |

Only an attacker for which GAMMA reports `is_stalker()` is accepted.

## Near misses

Normal hostile near misses begin inside 3 m. Extremely close bullets begin
inside 1 m. Repeated bullets use a diminishing three-stage response:

| Type | First | Repeated | Saturated |
|---|---:|---:|---:|
| Normal | -0.45 | -0.30 | -0.15 |
| Extreme | -0.75 | -0.50 | -0.25 |

The stage moves one step back toward the full startle response every three
seconds without another near miss. Actor-fired, friendly, unrelated and actual
actor-hit bullets do not count as near misses.

## Recovery lock and rebound

Core recovery remains locked throughout active danger and the resolution
cooldown. By default:

1. Active danger ends after ten seconds without a confirmed human threat.
2. Rebound waits another twenty safe seconds.
3. Combat restores up to 100% of the actual loss caused by that encounter,
   capped at 30 points and never exceeding the encounter starting value.
4. Unresolved deferred combat stress is discarded when rebound resolves.

Rebound does not activate at zero Composure and therefore cannot automatically
revive the actor from Pass Out.

Rebound accounting uses Core's actual applied deltas. Therefore, protection
from Consumables reduces both the original loss and the amount eligible for
rebound. Radiation, mutant, environmental and consumable losses are never
refunded merely because they occurred during a firefight.

## Consumables integration

All human Combat losses include:

```lua
metadata = { source_type = "combat" }
```

Combat-protection drugs can therefore reduce Combat loss without protecting
against radiation, pain, psy or other sources. Rebound uses
`source_type = "combat_rebound"` and bypasses potency policies to restore an
exact, bounded amount.

## Events published through Core

```text
combat.started
combat.resumed
combat.near_miss
combat.actor_hit
combat.intensity_changed
combat.overwhelmed
combat.ended
combat.rebound
combat.completed
```

Presentation modules can listen to these events without Combat directly
controlling HUD, audio, visuals or weapon behavior.

## Testing and diagnostics

F6 prints phase, hostile count, threat score, deferred amount, recorded Combat
loss and rebound cooldown.

For controlled tests, enable **Test Mode**, select an F6 action and press F6:

- Simulate normal or extreme near miss.
- Simulate a 10% human hit.
- Force Alert, Engaged or Overwhelmed.
- End the current encounter.

Leave Test Mode disabled during ordinary play. See `TESTING.md` for the full
first-pass validation sequence.
