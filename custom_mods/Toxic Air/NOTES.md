# Toxic Air add-ons

**Status:** uploaded 2026-09-24 via chat zips (MO2 `meta.ini` removed). Both are small config mods on top of **Toxic Air v2 Redux** (the base mod isn't in GAMMA and isn't uploaded; SA addon 40 requires it).

| Folder | MO2 version | Files | What it does |
|---|---|---|---|
| `Toxic_Air_economy_rebalance_for_GAMMA/` | d2026.9.6 | `configs/items/items/items_oxygentanks.ltx` | Rebalanced prices for the oxygen tanks (`af_oxygen_tank_*`) and gas-mask filters (`af_mask_filter_*`) |
| `ToxicAir_BigCanisters_v2 - TEST/` | d2026.9.13 (own TEST) | the same `items_oxygentanks.ltx` + `textures/ui/ui_oxygen_tank_big.dds` | The rebalance file with the 5 oxygen tanks turned into 1×3 inventory items using the new `ui_oxygen_tank_big` icon sheet, and **lower prices** |

## They replace the same file
Both ship `configs/items/items/items_oxygentanks.ltx`, so MO2 reads only the higher-priority one. With BigCanisters loaded after the rebalance, **the rebalance mod has no effect**. All its values come through BigCanisters' copy, with these differences:

| Section | Rebalance | BigCanisters |
|---|---|---|
| `af_oxygen_tank_1` | 1-high icon, 7795 | 1×3 big icon, **2500** |
| `af_oxygen_tank_1soviet` | 4500 | **2038** |
| `af_oxygen_tank_2` | 13438 | **1438** |
| `af_oxygen_tank_3` | 23551 | **3551** |
| `af_oxygen_tank_3military` | 65893 | **7138** |
| 4 mask filters (lines ~238–340) | 3707 / 4232 / 3713 / 3192 | **712 / 2313 / 1713 / 2813** |

If the cheaper prices aren't intended, copy the rebalance costs into BigCanisters' file (only the `icons_texture` / `inv_grid_*` lines need to differ).

- **File conflicts with GAMMA:** none (Toxic Air isn't part of GAMMA).
- **My changes:** none
