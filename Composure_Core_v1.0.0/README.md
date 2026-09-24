# Composure Core v2.1.0

Required state foundation for the modular Composure project for
S.T.A.L.K.E.R. Anomaly/GAMMA.

This release replaces **Composure Framework v2 + Composure Main v1** with one
clean foundation. It deliberately contains no stress sources, passive recovery,
hidden balance multipliers, HUD, audio, visuals, or weapon effects.

## Install / upgrade

Install this folder as an MO2 mod so `gamedata/` is at the mod root.

Disable these old packages before enabling Core:

- Composure Framework v2
- Composure Main v1

Do not run Main v1 with Core. Main would re-register its old tier multipliers
and passive recovery, defeating the direct-value balance model.

Existing Framework v2 saves are preserved because Core intentionally retains:

```text
script module: composure_framework
save key:      composure_framework_v2
API version:   2
MCM path:      composure_framework
```

Existing HUD, Audio, Heartbeat, Visuals, Weapon Handling, Combat and future
add-ons can continue calling `composure_framework` without code changes.

## Core ownership

Core owns only:

- Authoritative Composure value from 0 to 100
- Canonical tiers and starting value 65
- Save/load and legacy 0-120 migration
- Instant and continuous adjustment APIs
- Timed-effect persistence
- Caps and recovery locks
- Event/listener and adjustment-policy APIs
- Owner isolation and cleanup
- Snapshots, history and diagnostics
- Bounded fast/slow scheduler lanes

Canonical tiers:

| Tier | Range |
|---|---:|
| High | 86-100 |
| Medium-High | 70-85 |
| Medium | 55-69 |
| Medium-Low | 40-54 |
| Low | 16-39 |
| Breaking Point | 1-15 |
| Pass Out | 0 |

## Direct-value balance rule

Core registers no adjustment policy of its own:

```text
Requested -5 -> applied -5, limited only by 0
Requested +5 -> applied +5, limited only by 100, recovery locks and active caps
```

Removed from the active foundation:

- Tier loss multipliers
- Tier recovery multipliers
- Global loss/recovery multipliers
- Main's natural/passive recovery
- Main's tier notifications and F10 fallback display

Adjustment policies remain available as a public extension API. This is needed
for explicit timed mechanics such as a consumable's Recovery Potency or Loss
Resistance. Such policies must identify their owner and duration; Core itself
does not secretly scale adjustments.

## Example API

```lua
local FW = composure_framework

FW.apply_instant("combat.near_miss", -2.0, {
    owner = "composure_combat",
    category = "combat",
})

FW.add_temporary_modifier("consumables.tea", 0.05, 60, {
    owner = "composure_consumables",
    lane = "slow",
    persist = true,
    category = "consumable",
})

FW.set_recovery_lock("combat.aftershock", 20, {
    owner = "composure_combat",
    category = "combat",
})
```

## Public API index

State: `get_value`, `set_value`, `apply_delta`, `apply_instant`, `get_range`,
`get_tier`, `get_tier_info`, `set_tier_definitions`, `clear_tier_definitions`.

Modifiers: `upsert_modifier`, `add_modifier`, `add_temporary_modifier`,
`remove_modifier`, `has_modifier`, `set_modifier_enabled`,
`get_active_modifiers`, `get_net_rate`, `get_direction`, `get_group_totals`.

Caps/locks: `set_cap`, `remove_cap`, `get_active_caps`, `get_effective_cap`,
`set_recovery_lock`, `clear_recovery_lock`, `is_recovery_locked`,
`get_recovery_locks`.

Extension: `register_adjustment_policy`, `unregister_adjustment_policy`,
`register_listener`, `unregister_listener`, `emit_event`,
`register_check_display`, `unregister_check_display`.

Ownership/inspection: `set_owner_enabled`, `is_owner_enabled`,
`clear_owner_effects`, `clear_owner`, `get_snapshot`, `get_recent_events`,
`clear_history`, `get_version`, `get_api_version`, `supports`,
`get_diagnostics`, `debug_dump`.

## Current modular installation

During stabilization, install consumer modules separately after Core:

```text
1. Composure Core v2.1.0
2. Composure HUD v3.1.0
3. Composure Audio / Heartbeat
4. Composure Visuals v1.1.0
5. Gameplay modules such as Recovery, Consumables and Combat
```

HUD, Audio and Visuals should be integrated into the final Core package only
after their in-game behavior is stable.
