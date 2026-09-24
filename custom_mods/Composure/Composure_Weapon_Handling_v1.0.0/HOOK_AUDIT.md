# Weapon Handling v1.0.0 — Hook audit

Primary references:

- [GAMMA `axr_main.script`](https://github.com/Grokitach/Stalker_GAMMA/blob/main/G.A.M.M.A/modpack_patches/gamedata/scripts/axr_main.script)
- [GAMMA Modded Exes `lua_help_ex.script`](https://github.com/Grokitach/Stalker_GAMMA/blob/main/G.A.M.M.A/modpack_patches/gamedata/scripts/lua_help_ex.script)
- [GAMMA Enhanced Recoil implementation](https://github.com/Grokitach/Stalker_GAMMA/blob/main/G.A.M.M.A/modpack_addons/G.A.M.M.A.%20Enhanced%20Recoil/gamedata/scripts/grok_bo_enhanced_recoil.script)

## Proven GAMMA callbacks

GAMMA's `axr_main.script` declares callbacks used by this addon:

- `actor_on_update`
- `actor_on_weapon_fired`
- `actor_on_weapon_zoom_in`
- `actor_on_weapon_zoom_out`
- `actor_on_jump`
- `actor_on_land`
- `actor_item_to_slot`
- `on_level_changing`
- `actor_on_net_destroy`

Movement state is sampled with GAMMA's established `IsMoveState("mcSprint")`, `IsMoveState("mcCrouch")`, and `IsMoveState("mcAccel")` helpers. Actor movement speed uses `db.actor:get_movement_speed()` with protected fallback.

## Proven Modded Exes weapon methods

The GAMMA `lua_help_ex.script` CWeapon export documents getters/setters used here:

- `Get/SetCamRelaxSpeed`
- `Get/SetCamDispersion`
- `Get/SetCamDispersionInc`
- `Get/SetCamMaxAngleVert`
- `Get/SetCamMaxAngleHorz`
- `Get/SetCamStepAngleHorz`
- Zoom equivalents for every field above
- `Get/SetZoomRotateTime`

The addon captures every available getter independently. A missing field is skipped. If no audited getter is present, the native adapter reports unsupported and performs no weapon writes.

## Deliberately unused methods

The following are not used because they change ballistics or can degrade input:

- `SetFireDispersion`
- `Set_PDM_Base`, velocity, acceleration, crouch, and attachment PDM setters
- `SetFirstBulletDisp`
- `SetHitPower`, impulse, or fire distance
- `SetCrosshairInertion` because no matching getter was documented for safe baseline restoration
- Forced actor direction or continuous camera effectors

## Enhanced Recoil coexistence

GAMMA Enhanced Recoil reacts to `actor_on_weapon_fired` with short camera and PPE effectors. Weapon Handling changes the weapon's native camera-recoil properties and does not overwrite Enhanced Recoil scripts/configs. The mechanisms can stack perceptually, so combined live testing is mandatory.

## Result

Native v1 includes dynamic Weapon Stability, movement/stance context, shot accumulation, recoil strength, recoil recovery, and ADS timing. True continuous sway is exported as an adapter signal until a reversible implementation is proven.

The v1.0.0 release also provides a local preview value and log diagnostics. Preview only substitutes the value passed into the handling model; it never writes to Framework or save data.
