# Natural Recovery (own mod, built 2026-09-26)

`Natural_Recovery_v1.0.0/`: standalone add-on that slowly restores overall HP (the red bar, engine health 0.0–1.0) based on GAMMA limb health (`zzz_player_injuries.health` / `maxhp`: head 11, torso 11, arms and legs 5 each = 42).

| Limb state | Rule | Overall HP |
|---|---|---|
| Healthy | all limbs at max | +0.10 per in-game hour |
| Damaged | total ≥ 60%, head and torso ≥ 6, no limb at 0 | +0.03 per in-game hour |
| Badly hurt | anything else | none |

- **Ceiling:** recovery stops at limb ratio (total / 42).
- **Blockers:** bleeding, hit within 60 s (`actor_on_before_hit`), satiety < 0.15, thirst indicator ≥ 3 (`actor_status_thirst.get_water_deprivation(true)`), radiation > 0.10.
- **Awake:** `actor_on_update` every 1 real s, in-game time delta via `game.get_game_time():diffSec`. Jumps > 600 game s per tick (time skips) are ignored; nothing counts while `actor_is_sleeping` / `sleep_active` is set.
- **Sleep:** `actor_on_sleep(hours)` replays BHS limb healing (1 point/hour, head → torso → right arm → left arm → right leg → left leg) from the last awake limb snapshot, applying the tier each hour. Unified Simulated Time's sleep wrapper still sends `actor_on_sleep`.
- **Files:** `natural_recovery.script`, `natural_recovery_mcm.script`, `configs/text/eng/ui_st_natural_recovery.xml`. No overrides, no conflicts with GAMMA or other custom mods.
- **Tested:** both scripts compile under LuaJIT 2.1. A mocked-API simulation passes: healthy 1 h +10%, damaged 1 h +3%, ceiling holds at 81% with 34/42 limbs, a broken limb or bleeding gives 0, a hit pauses 60 s, 8 h sleep from head 5 and HP 30% → 75%, a 2 h time jump is ignored. **Not yet tested in-game.**
