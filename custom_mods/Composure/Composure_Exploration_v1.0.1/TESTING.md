# v1.0.1 live regression test

1. Start outdoors with Composure above the Exploration floor, preferably 55-65.
2. Press F7 and confirm `lifecycle=active`, at least two clock samples, and a nonzero elapsed value appearing over time.
3. Use a level transition that invokes Unified Simulated Time.
4. Confirm the log contains:
   - `Unified Simulated Time bridge installed`
   - `level-transition context ended: complete`
   - `arrival initialization: actor_first_update; grace 5.0s`
   - `arrival validated with ... clock samples`
5. During the five-second arrival grace, confirm no Exploration loss is applied.
6. After grace, press F7. It should report `lifecycle=active`, `lock=true` in an unsafe area, and elapsed game minutes should continue updating.
7. Remain outdoors above 50 Composure. The value should resume moving toward the Exploration floor.
8. Enter a friendly base. Exploration must clear its lock and Recovery should begin after Recovery's own safety delay.

Failure-safe check: if the game clock cannot be read, F7 should report `clock_wait` and `lock=false`; Composure must never remain frozen by Exploration.
