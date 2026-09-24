# BODYCAM — PiP & 3DSS (+ modded exes gamedata)

**Status:** uploaded 2026-09-24 (MO2 `meta.ini` files removed; they only held the download path).

| Folder | What it is |
|---|---|
| `BODYCAM - PiP & 3DSS Compatibility Patch/` | Compatibility patch **v1.7** making PiP scopes work with 3DSS. 34 r3 scope shaders (`models_scope_*`, `models_reflex_*`, `scope_custom_*.h`, `svp_hooks_*.h`, `scope_color_write`), 3 textures (`scope_glass/wpn_scope_pso_1m2-1_lens_diff`, `wpn/scope_utility/inside_blurred`), and 2 DLTX configs: `mod_system_scope_glass.ltx` and `mod_system_zzz…_pip_3dss_contract.ltx` (hybrid reflex/magnifier: `e0t2_magd` reticle type 12 with 3 magnifications, `uh1_magd`, plus their `_off` variants). |
| `Modded exes gamedata 2026.9.2/` | `db/mods/00_modded_exes_gamedata.db0` (binary archive, MO2 version d2026.9.2) |
| `Modded exes gamedata MT-TEST 2026.7.13/` | `db/mods/00_modded_exes_gamedata.db0` from `STALKER-Anomaly-modded-exes-MT-TEST_2026.7.13.zip` (MO2 folder was "Demorilzed 7.13") |

- **Main BODYCAM PiP mod:** only the compatibility patch was uploaded. If the base mod is a separate MO2 entry, upload it too.
- **MO2 order:** the patch overrides shaders from GAMMA's `410- 3DSS for GAMMA` (downloaded, not stored in this repo), so it must have **higher priority** than 3DSS and the base BODYCAM mod.
- **Two engine gamedata versions:** both folders ship the *same path* (`db/mods/00_modded_exes_gamedata.db0`) with *different* contents, so only the higher one in MO2 is used. Keep only the one matching your installed exes (`bin/`). Stock GAMMA 0.9.5 uses engine MT-TEST 2026.5.5.
- **File conflicts with this repo:** none (checked against `G.A.M.M.A/modpack_addons/*` and `modpack_patches/`). The overlap is intended and is only with the downloaded 3DSS files.
- `.db0` files are binary archives and can't be read in a cloud session.
- **Source links:** _(fill in)_
- **My changes:** none
