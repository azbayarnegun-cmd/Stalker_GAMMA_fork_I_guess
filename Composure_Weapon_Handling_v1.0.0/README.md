# Composure Weapon Handling v1.0.0

Optional gameplay addon for S.T.A.L.K.E.R. GAMMA, Composure Core v2.1+, and GAMMA Modded Exes.

Weapon Handling reads `composure_framework.get_snapshot()` and never changes Composure. It changes the stalker's ability to control a weapon, not the weapon's damage, penetration, ammunition, muzzle velocity, projectile behavior, condition, or mechanical shot dispersion.

## Install and load order

Use this order in MO2:

1. Composure Core v2.1+
2. Composure Feedback (optional)
3. Composure Combat / Recovery / Consumables (optional)
4. Composure Weapon Handling v1.0.0

The package has uniquely named scripts and localization. It does not replace global weapon configuration files. Do not install older Weapon Handling releases at the same time.

## Handling progression

- **70–100:** no handling penalty.
- **50–69:** minor instability and recoil-control effects.
- **40–49:** moderate instability and recovery delay.
- **16–39:** major instability, slow settling, and poor sustained-fire control.
- **1–15:** severe instability and a low stability ceiling.
- **0:** no added behavior; Pass Out belongs to Breakdowns.

Effects start smoothly at 69 by default and use the exact Composure value.

## Weapon Stability

One normalized Weapon Stability state drives the addon. Composure sets the maximum settled ceiling. Movement, sprinting, jumping, landing, recent shots, and external disturbances lower current stability. Crouching and remaining stationary improve the target and recovery rate without removing the Composure ceiling.

The native adapter uses reversible Modded Exes getters/setters for:

- Hip-fire and zoom camera recoil
- Recoil increase per shot
- Recoil angle limits
- Hip-fire and zoom recoil relaxation speed
- Weapon ADS transition time

Every applied value is recalculated from a captured baseline. The addon never repeatedly multiplies an already-modified target. Switching weapons, disabling the addon, changing options, changing levels, or destroying the actor restores the captured values.

## First-shot and burst behavior

The weapon's current handling targets are applied before a shot. The fired callback then adds temporary shot instability, so a settled first shot remains useful while subsequent rapid shots become harder. Shots within 180 ms receive extra accumulation. After firing stops, shot load recovers continuously and more slowly at low Composure.

## True sway limitation

The audited GAMMA scripting surface provides safe recoil and ADS setters but no equivalent native setter for continuous player aim sway. This build therefore does **not** fake sway by changing bullet dispersion or forcing camera angles.

Instead it publishes a normalized `sway_signal` from 0 to 1 through an adapter API. A future renderer/HUD-motion addon with a proven sway mechanism can consume that signal without changing this package.

```lua
composure_weapon_core.register_sway_adapter("my_sway", function(signal, state)
    -- Apply a safe external sway implementation here.
end, {
    owner = "my_addon",
    cleanup = function()
        -- Restore the external sway implementation here.
    end,
})
```

## External disturbances

Combat and Physical State integrations can apply temporary stability pressure directly:

```lua
composure_weapon_core.set_disturbance("near_miss", 0.25, {
    owner = "composure_combat",
    ttl = 0.8,
})
```

Or through Framework:

```lua
composure_framework.emit_event("composure_weapon.disturbance", {
    id = "explosion",
    amount = 0.40,
    duration = 1.2,
}, { owner = "composure_combat" })
```

Clear integrations with `clear_disturbance(id)` or `clear_disturbance_owner(owner)`.

## Public state

`composure_weapon_core.get_snapshot()` returns the current value, tier, severity, stability ceiling, current/target stability, movement load, shot load, external load, handling pressure, sway signal, movement context, and enabled state.

## Testing and diagnostics

The MCM includes a handling-only preview. Enable it and set a value from 0–100 to test the full curve without changing the Framework value or save state. The live snapshot exposes both `value` and `source_value`, plus `preview_enabled`.

Press the configurable diagnostic key (F11 by default) for an immediate log snapshot. Optional periodic logging reports current stability, ceiling, pressure, movement load, shot load, external load, and active state.

## Module ownership

- `composure_weapon_core.script`: Framework polling, callbacks, integration API, lifecycle.
- `composure_weapon_stability.script`: continuous stability model, shot load, external disturbances.
- `composure_weapon_recoil.script`: reversible Modded Exes weapon values.
- `composure_weapon_movement.script`: movement, sprint, crouch, ADS, jump, and landing context.
- `composure_weapon_sway.script`: optional adapter registry; no native camera/dispersion writes.
- `composure_weapon_mcm.script`: defaults, preview controls, diagnostics, and MCM schema.

## Compatibility notes

- Requires Composure Core v2.1+ and the Modded Exes included with GAMMA for the weapon-fired callback and native weapon setters.
- Composure Feedback is optional. Weapon Handling contains no breathing, heartbeat, HUD, thoughts, visual, or audio code.
- GAMMA Enhanced Recoil uses shot camera animations. This addon does not replace those files; live testing should confirm the combined strength is comfortable.
- Attachment or upgrade changes can recalculate native weapon values. Inventory-to-slot changes invalidate the baseline; after unusual in-place attachment changes, switch weapons once to force a fresh capture.
- No save data is required. Stability and shot disturbances are intentionally transient and reset on load/level changes.

See `TESTING.md` for the live verification matrix and `HOOK_AUDIT.md` for implementation decisions.
