# Composure (own mod suite)

**Status:** uploaded 2026-09-24 (2 web uploads, 115 files; MO2 `meta.ini` files removed). Each folder is one MO2 mod and includes its README, QA/TESTING notes and `tests/`.

A modular "composure" (stress/nerve) system for GAMMA. **Core** owns the value, and the other modules push changes into it or read it through `composure_framework` **API 2**.

| Folder | Version (from VERSION.txt) | Role |
|---|---|---|
| `Composure_Core_v1.0.0/` | **Core v2.1.0**, API 2 (the folder name says 1.0.0) | Required foundation (`composure_framework.script`). Replaces the old Composure Framework v2 + Composure Main v1 (disable those) |
| `Composure_Combat_v1.0.1/` | 1.0.1 | Firefight pressure; tells Core when recovery is unsafe. Don't run with the retired `composure_combat_stress_addon_v5` |
| `Composure_Recovery_v1.0.0/` | 1.0.0 | Safe-state recovery: +0.020/s to 65 after a 15 s safety delay; pass-out blocked at 0 |
| `Composure_Exploration_v1.0.1/` | 1.0.1 | Environmental pressure + persistent Expedition Strain; integrates with Unified Simulated Time |
| `Composure_Consumables_Balance_Redone_v1.1.2 - TEST/` | 1.1.2 TEST | Consumable effects on composure (replaces older Consumables/Redux/Combined); `balance/` holds the xlsx/csv sources, rebuilt with `tools/rebuild_from_csv.py` |
| `Composure_Thoughts_Extended_v4.1.0 - TEST/` | 4.1.0 TEST | Read-only "thoughts" messages; ships a `composure_hud.script` override based on Feedback 1.2.6 |
| `Composure_Weapon_Handling_v1.0.0/` | 1.0.0 | Composure affects sway/recoil/stability/movement (reads a snapshot only). Needs GAMMA's modded exes |
| `Consumable_Time_Skip_v1.0.5 - TEST/` | 1.0.5 TEST | Strong alcohol 120 min, tea/coffee 30 min, slow tobacco 15 min of world time; Composure optional |
| `Unified_Simulated_Time_GAMMA_v1.1.0/` | 1.1.0 | Replaces Simulated Time Skip 1.2.0 + Immersive Campfire Saving GAMMA compat + Level Transition Travel Simulator 4; steps time in 1–10 min A-Life steps |

**MO2 order (from the READMEs):** Core → Feedback (optional) → Recovery → Combat → Consumables → Exploration → Thoughts Extended → Weapon Handling. Time-Skip and Unified Simulated Time are independent.

**File conflicts:** none with GAMMA (`G.A.M.M.A/modpack_addons/*`, `modpack_patches/`), none with the other `custom_mods`, none between the Composure folders.

**Installed in-game but not uploaded** (seen in `xray_hitech.log`, 22 Sep 2026): `composure_heartbeat` (heartbeat audio), `composure_visuals` (vignette textures `ui\composure_visuals\vignette_*`) and `composure_hud` (probably the **Feedback** module). Upload them to back them up.

**Log observations (22 Sep 2026):** Composure ran without script errors. Heartbeat reported `errors=0` and tiers `medium`/`medium_low`. Cosmetic bug: Exploration logs `arrival validated with %d clock samples` without filling in the number (unformatted `printf`, same as SA addon 50).

- **My changes:** none
