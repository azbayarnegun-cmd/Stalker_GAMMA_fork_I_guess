# Alife mod set — damian_sirbu

**Status:** uploaded (source zips unpacked here; MO2 `meta.ini` and each mod's own `.gitignore` removed). Each subfolder is one MO2 mod with its `gamedata/` and `doc/` (readme, changelog, architecture).

| Folder | Version | What it does | Requires |
|---|---|---|---|
| `xlibs/` | 1.8.5 | Shared library (`x*.script`); no gameplay on its own | — |
| `AlifePlus/` | 1.8.7 | NPC trade/market cycle at trader smarts, loot claim, stashes, squad activities, news/chatter (`ap_*`) | xlibs, MCM |
| `AlifeTactics/` | 1.2.0 | NPC combat AI: accuracy, crossfire, stance, noise, first aid, NPC weapon jamming (`at_*`); DLTX tweaks in `configs/ai_tweaks/mod_xr_danger_at.ltx`, `mod_xr_eat_medkit_at.ltx` | xlibs, MCM, modded exes (Demonized 2025.9.10+) |
| `AlifeBalance/` | 1.1.3 | Steers smart-terrain population/squad sizes toward the declared spawn config (`ab_*`) | xlibs, MCM |
| `AlifeGuard/` | 1.3.1 | Sanitizes NPC inventories, smart terrains and offline/online state (`ag_*`) | xlibs, MCM |

- **Sources:** github.com/damiansirbu-stalker (AlifePlus, AlifeTactics, xlibs …), moddb `alifeplus-v1-0-01`, `xlibs-1001`.
- **Relation to GAMMA:** GAMMA lists Alife Plus and Xlib (`modpack_maker_list.txt` lines 483/482) but **disables** them in `modlist.txt` (upstream commit dc4ae367, unstable MCM defaults). I run this newer set instead.
- **File conflicts with GAMMA:** none. Checked every `gamedata/` path against `G.A.M.M.A/modpack_addons/*` and `modpack_patches/` (2026-09-24). All files use their own prefixes.
- **Settings the mods' docs ask for on GAMMA:**
  - Options > Gameplay > General > **NPC loot distance = 0** (GAMMA sets 12 m; AlifePlus's loot claim replaces it). Console: `run_string ui_options.set("gameplay/general/npc_loot_distance", 0)`.
  - **Useful Idiots → "no NPC looting" OFF** (on by default in GAMMA), otherwise nothing feeds AlifePlus trade/market.
  - GAMMA's Stealth Overhaul ships an older `xr_combat_ignore` that wins over the modded-exe one. AlifeTactics's docs mention this; nothing to do.
- **Overlaps to keep in mind:** AlifeTactics tweaks `xr_danger` via DLTX, and GAMMA's `G.A.M.M.A. AI Rework` replaces `xr_danger.script`. AlifeBalance reads `G.A.M.M.A. NPC Spawns` as the target population.
- **MO2 position:** _(fill in; xlibs must load before the others)_
- **My changes:** none
