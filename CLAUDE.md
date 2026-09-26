# CLAUDE.md — G.A.M.M.A. fork

Fork of [Grokitach/Stalker_GAMMA](https://github.com/Grokitach/Stalker_GAMMA): Grok's Automated Modular Modpack for S.T.A.L.K.E.R. Anomaly (X-Ray engine, Lua scripting). Current release: GAMMA 0.9.5 (definition version in `G.A.M.M.A_definition_version.txt`). The game runs on Windows only; nothing here can be built or run in this container.

## Repository layout

| Path | What it is |
|---|---|
| `G.A.M.M.A/modpack_data/modpack_maker_list.txt` | Download list the GAMMA launcher reads. One addon per line, tab-separated: download URL (moddb/github), subfolders to install (`:`-separated, `0` = whole archive), author, name, moddb page. Lines starting with a space (e.g. ` Audio`) are section headers. |
| `G.A.M.M.A/modpack_data/modlist.txt` | Mod Organizer 2 load order. `+` = enabled, `-` = disabled, `*_separator` = group header. **First line = highest priority** (wins file conflicts); the bottom of the file loads first. |
| `G.A.M.M.A/modpack_addons/` | Addon folders shipped from this repo (~385). Each contains a `gamedata/` tree, sometimes a `meta.ini`. |
| `G.A.M.M.A/modpack_patches/` | Files copied straight into the game install (`gamedata`, `bin`, `db`, `appdata`). Holds the modded-exes Lua side (`options_modded_exes_*.script`, `_g_patches.script`, `axr_main.script`, `dxml_core.script`, imgui helpers) and `appdata/user.ltx` plus weather presets. |
| `Patchnotes.md` | Changelog for the current release; read it for design intent. |
| `moddb_mirrors.txt` | Mirror URLs for downloads. |

### Three kinds of addon folders in `modpack_addons/`
1. **`NNN- Name - Author`**: GAMMA's *overrides* for an addon that is downloaded from moddb/github. `NNN` is that addon's line number in `modpack_maker_list.txt`, so line 117 → `117- Gotta Go Fast - Grokitach` and line 140 → `140- Weapon Parts Overhaul - arti`. These folders often contain just one or two files (e.g. WPO only overrides `arti_jamming.script`); the rest of the addon comes from the download.
2. **`G.A.M.M.A. <Feature>`**: GAMMA's own addons, containing the core gameplay changes (see below).
3. **`<Modder>'s <Thing>`** (e.g. `G_FLAT's ...`, `SaloEater's ...`, `Momopate's ...`): community fixes and tweaks hosted directly in the repo.

Also present: `*_separator` folders (MO2 group headers), and design spreadsheets (`artefacts_values.xlsx`, `gamma_ammo_weapon_table.xlsx`, `toolkits_chance.xlsx`).

To enable or disable an addon, flip `+`/`-` on its line in `modlist.txt` (see commit dc4ae367, which disabled `483- Alife Plus` and `482- Xlib`). To add a downloaded addon, add a line to `modpack_maker_list.txt` **and** a matching `+NNN- Name - Author` line in `modlist.txt`.

## How Anomaly modding works

- **Override by path**: files are merged into one virtual `gamedata/`. When two enabled addons ship the same path, the higher-priority one in `modlist.txt` wins completely. This causes most conflicts, so before editing a file, `find` every addon that ships the same path.
- **Scripts** (`gamedata/scripts/*.script`): Lua 5.1/LuaJIT. Each file is a global namespace named after the file (`zzz_player_injuries.some_func`). Entry point is `on_game_start()`, which registers callbacks with `RegisterScriptCallback("actor_on_first_update", fn)`, `"actor_on_update"`, `"on_key_press"`, `"save_state"`/`"load_state"`, `"on_option_change"`, etc. Files load alphabetically, so `zzz_`/`aaaa_` prefixes control order. **Monkey-patching** (reassigning another script's function, e.g. `aaaa_monkeys.script`) is the usual way to change base behaviour without replacing the file.
- **Configs** (`gamedata/configs/*.ltx`): INI-like sections `[section]:parent`. **DLTX** files named `mod_<base>_<anything>.ltx` (e.g. `mod_system_*.ltx` patches `system.ltx`) edit sections without replacing files: `![sec]` modifies an existing section, `!![sec]` deletes it, `@[sec]` modifies it or creates it if missing, and `!key` deletes a key. Many `z`s in a name force late loading, so that file wins (e.g. `mod_system_zzzzzzzzzzzzzzzzzzzzzzzzz_gamma_outfits_balances.ltx`).
- **DXML** (`modxml_*.script`, core in `modpack_patches/gamedata/scripts/dxml_core.script`) patches UI/text XML at load time.
- **MCM** (Mod Configuration Menu): per-addon settings in `*_mcm.script`. GAMMA's default MCM values live in `G.A.M.M.A. MCM values - Rename to keep your personal changes/gamedata/configs/axr_options.ltx`. MCM defaults that change between upstream addon updates are a recurring source of breakage.
- **Engine**: Demonized's multithreaded modded exes (MT test branch); their options scripts are in `modpack_patches/gamedata/scripts/options_modded_exes_*.script`.

## Where the gameplay systems live

All paths are relative to `G.A.M.M.A/modpack_addons/`.

| System | Main addon folders / files |
|---|---|
| Economy, trade, loot | `G.A.M.M.A. Economy (don't disable, turn on Black Market to buy gear)`: trader configs `gamedata/configs/items/trade/*.ltx`, NPC loadouts, `wpo_loot.script`, `item_recipe.script`, and `target_prior.script` (NPC target priority, performance-sensitive). Also `G.A.M.M.A. Dynamic Loot Balance`, `G.A.M.M.A. No trade with random stalkers`, `G.A.M.M.A. Rare Stashes Balance`. |
| Weapons & gunplay | `140- Weapon Parts Overhaul - arti` (jamming), `G.A.M.M.A. Weapon Pack`, `G.A.M.M.A. Enhanced Recoil`, `G.A.M.M.A. Unjam Reload on the same key`, `ATHI's Mags Redux ...`, `G.A.M.M.A. Guns Have No Condition` |
| Repair, crafting, upgrades | `G.A.M.M.A. Arti Recipes Overhaul` (recipes, `ammo_maker.script`, workshop injection), `G.A.M.M.A. Upgrades Overhaul` (`aaaa_monkeys.script`, per-weapon `items/weapons/upgrades/*_up.ltx`), `G.A.M.M.A. Armors repair like WPO`, `G.A.M.M.A. Expert toolkits tier 5`, `G.A.M.M.A. Repair Kit Renaming` |
| Armor & outfits | `G.A.M.M.A. Outfits Balances` (DLTX stat blocks plus `tools/` sources), `G.A.M.M.A. Armors Balancing`, `G.A.M.M.A. Exo Balance`, `G.A.M.M.A. Accurate Defense Values` |
| Healing & meds | `G.A.M.M.A. Medications Balance`: `zzz_player_injuries.script` (per-limb health), `mod_system_drugs_balance_bhs_GAMMA.ltx` |
| Artefacts | `G.A.M.M.A. Artefacts Reinvention` (melter/combining `grok_artefacts_melter_*.script`, random spawner/condition, `ui_workshop.script`), `Flueno's Safer Artifact Melting` |
| Progression & start | `G.A.M.M.A. Starting Loadouts` (`new_game_loadouts.ltx`), `G.A.M.M.A. Starting Locations`, `G.A.M.M.A. Miracle Machine Remake`, `G.A.M.M.A. Psy Fields in the North`, `156- No Exos in the South - Grokitach`, `G.A.M.M.A. Fast Travel Limiter Rebalance` |
| AI & A-Life | `G.A.M.M.A. AI Rework` (`schemes_ai_gamma.script`, `xr_danger.script`, `xr_combat_camper.script`, smart-terrain logic), `G.A.M.M.A. Alife optimization` (`alife.ltx`, smart defs), `G.A.M.M.A. Alife fixes`, `G.A.M.M.A. NPC Spawns`, `G.A.M.M.A. Companions Rework`, `G.A.M.M.A. Dynamic Despawner` |
| Mutants | `G.A.M.M.A. Mutants Overhaul` (`creatures/m_*.ltx`) |
| Tasks | `G.A.M.M.A. Dynamic Tasks Balance` (`tm_dynamic.ltx`, `tasks_assault.script`), `G.A.M.M.A. Quests Rebalance`, `G.A.M.M.A. Bounty Squads Rework` |
| Survival | `G.A.M.M.A. Sleep Balance`, `G.A.M.M.A. Cooking Overhaul`, `G.A.M.M.A. Radiation Dynamic Areas`, `G.A.M.M.A. Psy rework` |
| UI / HUD | `G.A.M.M.A. UI`, `G.A.M.M.A. Minimalist HUD`, `G.A.M.M.A. Icons*` |

Design pillars (from README / Patchnotes): the Zone gets harder and more rewarding further north; weapon and armor trading is removed; gear progression is gated by toolkits found in rare stashes; guns found on enemies need repairs and parts; health is tracked per limb; artefacts are strengthened by combining them; the North opens after the Miracle Machine and Brain Scorcher.

## Custom mods (`custom_mods/`)

The user's own mods, run on top of GAMMA; see `custom_mods/README.md` for the layout and index table. They are **not** in `modlist.txt` or `modpack_maker_list.txt`.
- One folder per mod: `custom_mods/<Mod Name> - <Author>/gamedata/...`, plus an optional `NOTES.md` (source, version, MO2 position, local changes).
- When a mod is added or changed, update the index table in `custom_mods/README.md`.
- Before editing a custom mod, check which of its `gamedata/` paths are also shipped by `G.A.M.M.A/modpack_addons/*`, since the same override rule applies. Its MO2 position (in `NOTES.md`) decides which file wins.
- Big binaries in `custom_mods/` are Git LFS objects (`.gitattributes`). Git LFS isn't installed in cloud sessions, so those files show up as small pointer files. Only edit text files (`.script`, `.ltx`, `.xml`).

## Working conventions

- Upstream accepts PRs to **`dev2`**. In this fork, work happens on `claude/*` branches.
- Commit messages are short, lowercase-ish summaries of the gameplay effect (e.g. "More frequent artefacts spawn", "Heavily optimised target_prior.script (from 11ms to 5.50ms per call)").
- Balance changes usually go in DLTX `mod_*.ltx` files, not edits to whole base configs.
- Keep edits minimal and local. Many scripts are community-authored and upstream updates overwrite them.
- **Verification** (no game available): grep for every addon that ships the same file path; check the `modlist.txt` order/flags; syntax-check Lua with `luac -p` / `luajit -bl` if one is installed (neither is by default); check that DLTX section names exist in the base configs.
