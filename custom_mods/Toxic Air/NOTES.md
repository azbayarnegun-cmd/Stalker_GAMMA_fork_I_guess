# Toxic Air add-ons

**Status:** uploaded 2026-09-24 via chat zips (MO2 `meta.ini` removed). Two small config mods on top of **Toxic Air v2 Redux** (base mod, also uploaded here; SA addon 40 requires it).

| Folder | MO2 version | Files | What it does |
|---|---|---|---|
| `Toxic_Air_v2_REDUX_by_Priler/` | base mod | 108 (zip + separate `textures.zip`, both via chat) | Gas masks/filters and oxygen tanks: `toxic_air.script` + MCM, QAW compat, filter-refill-on-drag, crafter/loadout helpers, item configs (`items_oxygentanks.ltx`, `items_anm_filters.ltx`, filter disassembly), UI, anims, meshes, sounds, textures (`ui_oxygen_tank*.dds`, `ui_toxic_air.dds`, `usable_items/filter/*`) |
| `Toxic_Air_economy_rebalance_for_GAMMA/` | d2026.9.6 | `configs/items/items/items_oxygentanks.ltx` | Rebalanced prices for the oxygen tanks (`af_oxygen_tank_*`) and gas-mask filters (`af_mask_filter_*`) |
| `ToxicAir_BigCanisters_v2 - TEST/` | d2026.9.13 (own TEST) | the same `items_oxygentanks.ltx` + `textures/ui/ui_oxygen_tank_big.dds` | The rebalance file with the 5 oxygen tanks turned into 1×3 inventory items using the new `ui_oxygen_tank_big` icon sheet, and **lower prices** |

## Three copies of the same file
The base mod and both add-ons ship `configs/items/items/items_oxygentanks.ltx`, so MO2 reads only the highest-priority one. Intended order: Redux → rebalance → BigCanisters. With BigCanisters last, **neither the base values nor the rebalance are used**. All its values come through BigCanisters' copy, with these differences:

| Section | Rebalance | BigCanisters |
|---|---|---|
| `af_oxygen_tank_1` | 1-high icon, 7795 | 1×3 big icon, **2500** |
| `af_oxygen_tank_1soviet` | 4500 | **2038** |
| `af_oxygen_tank_2` | 13438 | **1438** |
| `af_oxygen_tank_3` | 23551 | **3551** |
| `af_oxygen_tank_3military` | 65893 | **7138** |
| 4 mask filters (lines ~238–340) | 3707 / 4232 / 3713 / 3192 | **712 / 2313 / 1713 / 2813** |

## BigCanisters v3 (my build, 2026-09-24)
`ToxicAir_BigCanisters_v3/`: **big 1×3 tanks with the rebalance prices.** Built from the rebalance file with v2's `icons_texture` / `inv_grid_*` values merged in per section, plus v2's `ui_oxygen_tank_big.dds`.
- Checked by diff: vs the rebalance, only icon/grid lines differ; vs v2, only the 17 `cost` lines differ.
- Use it **instead of** the rebalance and v2 (all three replace `items_oxygentanks.ltx`). MO2: Toxic Air v2 Redux → BigCanisters v3. See `ToxicAir_BigCanisters_v3/README.txt` for the full price table.

- **File conflicts with GAMMA** (Redux only; its textures don't clash):
  - `custom_functor_autoinject.script`: also in `G.A.M.M.A. Arti Recipes Overhaul` (and disabled Mags Redux). **Same code**, only comment/blank-line differences, so it's harmless either way.
  - `trader_autoinject.script`: also in `G.A.M.M.A. Weapon Pack`, `G.A.M.M.A. Arti Recipes Overhaul`, `245- Hideout Furniture`. Toxic Air's copy is **older**: it lacks GAMMA Weapon Pack's `not npc` nil check and the Sidorovich/Forester (`esc_m_trader`, `red_m_lesnik`) 20 m distance fix. If Toxic Air loads after GAMMA, that fix is lost. Safest: delete Toxic Air's `trader_autoinject.script` in MO2 (or load it before GAMMA's addons) so GAMMA's newer copy wins.
  - `toxic_air_qaw_compat.script`: also in SA addon 40, which replaces it intentionally.
- **My changes:** created BigCanisters v3
