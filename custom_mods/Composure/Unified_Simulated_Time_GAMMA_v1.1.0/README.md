# Unified Simulated Time - GAMMA v1.1.0

One MO2-ready replacement for:

- Simulated Time Skip v1.2.0
- Immersive Campfire Saving - GAMMA Compatibility
- Level Transition Travel Simulator 4

## What it does

- Runs game-time passage in configurable 1-10 minute ALife steps.
- Simulates normal sleep by default.
- Simulates level-transition travel **before** GAMMA unloads the current map.
- Level travel uses a protected dynamic schedule: up to 30 minutes = 1 step,
  31-60 = 2 steps, 61-120 = 4 steps, and 121+ = 5 steps.
- Forces nearby enemies offline and refreshes GAMMA's actor invulnerability
  window during the transition-only blackout.
- Prevents emission and psy-storm startup throughout travel while still aging
  their countdowns. An active event blocks travel; an event that became due in
  transit is restored after arrival with a two-real-minute grace period.
- Uses the old transition mod's route-specific durations with a configurable
  fallback for newer/unknown GAMMA routes.
- Adds immersive campfire saving: near a lit fire, saving causes a blackout and
  passes 15-30 minutes before the save completes.
- Optionally simulates GAMMA Books, anabiotic shelter, Placeable Campfires, DAO
  flash anomalies and Soulslike respawns.
- Optionally advances active Composure modifiers through the compatibility bridge
  supplied by Consumable Time-Skip.

Every feature is independently configurable in **MCM > Unified Simulated Time**.

## Important compatibility design

This build does not contain or replace any of these GAMMA files:

- `ui_sr_teleport.script`
- `ui_main_menu.script`
- `ui_save_dialog.script`
- `level_input.script`
- `bind_campfire.script`
- `zzz_simulated_time_travel.script`

The old global Travel catch-all is intentionally excluded. It caused the log
sequence `async no-ChangeLevel -> Disconnect -> Destroying level`. The new
runtime transition wrapper delays GAMMA's original `OnMsgOk`, completes the
simulation, and only then resumes the untouched transition method.

## Composure and Consumable Time-Skip

- Consumable Time-Skip remains a separate addon and can stay enabled.
- Each addon checks the other's active state and avoids overlapping skips.
- If `consumable_time_skip_composure.script` is installed, simulated steps age
  active Composure modifiers by the exact game minutes elapsed.
- If Composure or the bridge is absent, this addon remains functional.

## Installation

1. Disable/remove standalone **Simulated Time Skip v1.2.0**.
2. Disable/remove standalone **Immersive Campfire Saving GAMMA Compat**.
3. Disable/remove **Level Transition Travel Simulator 4**.
4. If either old travel/campfire mod was installed manually, restore/verify
   GAMMA's base files first.
5. Install this ZIP as one MO2 mod and enable it after YACS/MCM.
6. Keep your Composure modules and Consumable Time-Skip enabled.

Do not reinstall Simulated Time Skip's optional Travel/catch-all file on top of
this addon.

## Default MCM configuration

- Master simulation: enabled
- General step size: 3 minutes (level travel uses the dynamic schedule above)
- Composure integration: enabled
- Sleep: enabled
- Level-transition travel: enabled
- Unknown route duration: 60-120 minutes
- Immersive campfire saving: enabled
- Campfire saving: 15-30 minutes, five-second blackout
- Books/anabiotic/placeable campfire/flash/Soulslike: disabled

## Console test

From a loaded disposable save:

```lua
unified_time_skip_integrations.test_transition(15)
```

This tests the simulation and overlay without changing maps.
