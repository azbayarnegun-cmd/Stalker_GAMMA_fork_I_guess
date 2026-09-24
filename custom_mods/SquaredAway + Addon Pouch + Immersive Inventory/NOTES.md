# Inventory set: Squared Away, Layered Pouches, HD Icons, FIUT, Seamless Sort

**Status:** partially uploaded 2026-09-24 (MO2 `meta.ini` files removed). The web upload had **exactly 100 files**, GitHub's per-upload limit, and Squared Away and Layered Pouches arrived with configs only. Their scripts, UI XML and textures are most likely missing and need a second upload.

| Folder | Version | What it is | Uploaded so far |
|---|---|---|---|
| `Squared Away 3.1.0/` | 3.1.0 | Rigs, pouches, boxes (`amp_*`): item defs, crafting/parts, trader stock (`items/trade/mod_trade_*_amp.ltx`), death loot, GAMMA tier/treasure hooks (`mod_grok_items_tier_amp.ltx`, `mod_grok_treasure_manager_amp.ltx`), start loadouts, Mags Redux outfit loadouts, grid packs/stacks, SortingPlus config | 41 config files; **no scripts / UI / textures (incomplete?)** |
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

No path conflicts for Squared Away, Layered Pouches, FIUT or Seamless Sort (they use DLTX `mod_*` / `zzz_*` files). Squared Away's trade DLTX stacks on top of GAMMA's trader configs (`G.A.M.M.A. Economy`).

- **"Immersive Inventory":** not identified in this upload. Tell me which folder it is, or upload it.
- **Source links:** _(fill in)_
- **MO2 order:** _(fill in)_
- **My changes:** none
