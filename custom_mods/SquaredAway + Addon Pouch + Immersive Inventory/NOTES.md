# Inventory set: Squared Away, Layered Pouches, HD Icons, FIUT, Seamless Sort

**Status:** Squared Away now complete (chat zip); rest partially uploaded 2026-09-24 (MO2 `meta.ini` files removed). The web upload had **exactly 100 files**, GitHub's per-upload limit, and Squared Away and Layered Pouches arrived with configs only. Their scripts, UI XML and textures are most likely missing and need a second upload.

| Folder | Version | What it is | Uploaded so far |
|---|---|---|---|
| `Squared Away 3.1.0/` | 3.1.0 | Rigs, pouches, boxes (`amp_*`): item defs (`mod_system_amp_boxes/amp_rigs/zz_amp_pouches.ltx`), scripts (`zzz_armor_mag_pouches`, `zzz_amp_grid`, `zzz_amp_weardev`, `zzz_amp_compat`, MCMs, `zzz_zzz_qaw_meds_pocket_only`), UI (`zzz_amp*.xml`, `actor_menu_grid_16.xml`, `ui_inventory_16.xml`), textures (`ui_actor_menu.dds` 62 MB, `ui_amp_boxes.dds`, `ui_amp_rigs.dds`), sounds, trader stock, crafting, loadouts | **Complete** (71 files; full zip via chat 2026-09-24) |
| `SA_Layered_Pouches_1.5.3_SA310_PouchGrid_r11/` | 1.5.3 (for SA 3.1.0, PouchGrid r11) | Layered pouches addon for Squared Away (`amp_layers`) | 31 config/text files; **no scripts (incomplete?)** |
| `HD_Inventory_Icons_Framework/` | MO2 d2026.9.4 | HD icon framework and icon layering/overrides | 14 scripts |
| `FIUT_StashOnly_v1.0.0/` | 1.0.0 | Category headers in stash inventory | 7 files |
| `501-_Seamless_Inventory_Sort/` | MO2 d2026.9.4 | Keeps SortingPlus order after modifying/moving items. **Requires SortingPlus** (GAMMA `110- SortingPlus`) | 4 files |

## Conflicts with GAMMA (same file path, the higher MO2 priority wins)
All in `HD_Inventory_Icons_Framework/gamedata/scripts/`:

| Script | Also shipped by GAMMA addon(s) |
|---|---|
| `utils_ui.script` | `G.A.M.M.A. UI`, `G.A.M.M.A. Guns Have No Condition` |
| `utils_ui_icon_rotation_fix_mcm.script` | `G.A.M.M.A. UI`, `G.A.M.M.A. Icons replacer and fixes` |
| `aaa_rax_icon_override_mcm.script` | `G.A.M.M.A. Icons replacer and fixes`, `G.A.M.M.A. Guns Have No Condition`, `207- Mags Redux`, Tiskar's icon fixes |
| `rax_icon_layers.script`, `yyy_mag_sorting.script` | `207- Mags Redux`, `ATHI's/Anomaly Magazines Redux` |
| `zzz_rax_sortingplus_mcm.script` | `110- SortingPlus` |
| `icon_overlayer_mcm.script` | `418- Dynamic Icons Indicators` |
| `meat_spoiling.script` | `ilrathCXV's Meat Spoiling Timer in Tooltips` |

The HD Icons framework is built to replace these, so it must load **after (higher priority than)** all of them. Any GAMMA change in these scripts (e.g. `utils_ui.script` from `G.A.M.M.A. UI`) is lost while it wins. That's the first place to look if tooltips, condition bars or icons misbehave.

**Squared Away 3.1.0 conflicts with GAMMA:**
- `configs/ui/ui_inventory_16.xml`: also in `G.A.M.M.A. Accurate Defense Values`.
- `textures/ui/ui_actor_menu.dds`: also in `G.A.M.M.A. Accurate Defense Values` and `G.A.M.M.A. Guns Have No Condition`.
Squared Away needs its versions for the grid/rig UI, so it must load after those. GAMMA's inventory layout/texture changes from them are replaced.

**Squared Away files replaced by your own addons (intended):** `zzz_amp_grid.script` (10, then 55), `zzz_armor_mag_pouches.script` (62), and `mod_grok_items_tier_amp.ltx`, `mod_grok_treasure_manager_amp.ltx`, `zzz_grid_stacks.ltx` (30).

**Still undefined:** `amp_pouch_provisions`, `amplayer_sustainment_pouch_t1`–`t3` are modified by your addons but not defined in any uploaded file. They're probably in the full Layered Pouches.

No path conflicts for FIUT or Seamless Sort (they use DLTX `mod_*` / `zzz_*` files). Squared Away's trade DLTX stacks on top of GAMMA's trader configs (`G.A.M.M.A. Economy`).

- **"Immersive Inventory"** = addon `50_SA_Immersive_Inventory_Access` in `SA addons (own)/` (see below).
- **Source links:** _(fill in)_
- **MO2 order:** _(fill in)_
- **My changes:** none

## SA addons (own) — `SA addons (own)/`

Uploaded 2026-09-24. Folder numbers are the MO2 load order (lower first; later ones override earlier ones). This upload was **also exactly 100 files** (the web limit). `10`, `20` and `30` have no README/meta.ini while the others do, so some of their files may be missing.

| # | Addon | Version / build | Purpose |
|---|---|---|---|
| 10 | SA Inventory Framework Core (+ UBGL 1.0.0) | 1.0.1 TEST | Core: grid (`zzz_amp_grid.script`), `magazine_binder.script`, ammo-check MCMs |
| 20 | SA Rigs, Belts & Pouches (Sustainment Visibility) | 1.0.2 TEST | Rig/belt/pouch configs |
| 30 | SA Equipment Balance (Workshop Compatible Recipes) | 1.0.4 TEST | Equipment balance + recipes, craft-recipe diagnostic |
| 40 | SA Combat Access & QuickWheel | 1.0.0 (stable V1) | Quick Action Wheel access. Requires 10 + 30, **Quick Action Wheel (HarukaSai)** and **Toxic Air v2 Redux** |
| 50 | SA Immersive Inventory Access | 1.0.11 C5 1.5s STABLE | Hold Tab plays the backpack animation (bundled `immersive_backpacks_fdda`), opens the inventory after ≥1.5 s, hides the weapon HUD meanwhile. Disable older `50` builds |
| 55 | SA Stash, Corpse & Vendor No-Stack | 1.0.0 TEST | Load-after override of 10's grid for stash/corpse/vendor windows |
| 62 | SA UBGL & Utility Fix | 1.0.1 TEST | Late-load fix; armor mag pouches |
| 70 | SA Basic Fabric Salvage | 1.1.0 TEST | More Basic Fabric (`prt_o_fabrics_1`) from salvage; no trader/loot changes |
| 90 | SA Rig Pocket Rebalance | 1.1.0 TEST | Rig pocket rebalance + trade script, MCM |
| 95 | SA Cloth-Heavy Equipment Recipes | 1.0.1 TEST | More Basic Cloth in pouch/rig recipes |

**Conflicts with GAMMA (same path, higher MO2 priority wins):**
- `10/.../scripts/magazine_binder.script`: also in `207- Mags Redux` and `ATHI's/Anomaly Magazines Redux`. 10 must win for the SA grid to work.
- `40/.../scripts/haru_quick_action_wheel_mcm.script`: also in `G.A.M.M.A. Quick Action Wheel Balance`. GAMMA's QAW balance values are replaced while 40 wins.

**Conflicts between the addons themselves (intended overrides):**
- `zzz_amp_grid.script`: 10 and 55 (55 overrides 10).
- `ammo_check_onekey_mcm.script`: 10 and 62 (62 overrides 10).
