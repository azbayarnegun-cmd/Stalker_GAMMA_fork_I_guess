# v4.1.0 QA

## 2026-09-12 readability and manual-check verification

- Automatic thought default: 6 seconds; MCM range: 2-12 seconds.
- Standard fades: 0.7 seconds in and 1.3 seconds out.
- Check activation remains a 0.6-second hold; release after activation does not cancel it.
- Holding the key through completion is latched as one check and cannot restart the sequence until the key is released.
- Accumulating default interval: 0.8 seconds; reflection default interval: 1.4 seconds.
- Final picture default: 5 seconds followed by a 1-second fade.
- Automatic/event processing is suppressed for 3 seconds after the manual sequence completes.
- New timing options have matching English MCM labels and descriptions.
- The runtime remains read-only and adds no inventory enumeration or Composure mutation.

## 2026-09-03 hotfix verification

- Parsed all three Lua scripts successfully with `luaparser` 4.2.0.
- Parsed both XML files successfully with `lxml`.
- Verified the companion Consumables Balance payload types: `Drink`, `Food`, `Food - MRE`, `Comfort food`, `Mutant food`, `Raw`, `Alcohol`, and `Cigar*`.
- Confirmed the read-only design remains intact: no Composure value mutation or inventory enumeration was added.
- Source log showed normal initialization, successful hold/release checks, and no Thoughts Lua exception.

Static validation completed on 2026-09-03.

- Lua parser: PASS (`composure_thoughts.script`, `composure_thoughts_mcm.script`, `composure_hud.script`).
- XML parser: PASS (UI and English string table).
- MCM localization coverage: PASS; every non-layout option has a resolved label.
- Loot runtime/state/MCM removal: PASS.
- Inventory enumeration absence: PASS.
- Creature access order: PASS; the sole `obj:alive()` call is protected and reached only after `IsMonster`/`IsStalker` classification.
- Combined creature scan and default 3-second throttle: PASS.
- Corpse FIFO bound (32), 15 m default, cone and distance roll markers: PASS.
- Mutant 35 m default, distance roll, hostile preference/fallback, encounter latch, and 9-second continuous grace markers: PASS.
- Needs cache (5 seconds), 45-90-second opportunity, severity chances, hysteresis, cooldown, and combat suppression markers: PASS.
- Five-slot cap and hold/release callbacks: PASS.
- No Composure, inventory, health, stamina, or need mutation calls in Thoughts runtime: PASS.
- HUD tier-color override removal: PASS.

Runtime smoke tests still recommended in the target GAMMA installation because optional needs modules and engine UI callbacks vary between loadouts. F6 cycles every non-mutating diagnostic branch for this purpose.
