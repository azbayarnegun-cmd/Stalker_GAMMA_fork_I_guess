# Composure Weapon Handling v1.0.0 — Build QA

Build: `1.0.0`

## Automated results

- Six required runtime modules: PASS
- Framework v2 read-only contract: PASS
- No legacy `composure_manager` dependency: PASS
- No ballistics/damage/RPM/PDM setters: PASS
- No forced camera or input manipulation: PASS
- Effect begins at 69 and is neutral at 70+: PASS
- Pass Out value 0 disables native effects: PASS
- Native setter/getter baseline pairing: PASS
- Baseline-derived targets; no multiplicative drift: PASS
- Cleanup restoration paths: PASS
- Movement/crouch/sprint inputs: PASS
- Shot accumulation and rapid-fire path: PASS
- Adapter-only sway boundary: PASS
- External disturbance API: PASS
- Local preview does not write Framework state: PASS
- Configurable F11 diagnostic path: PASS
- Retired breathing/audio/feedback code absent: PASS
- MCM clamps and localization coverage: PASS
- Numerical stability bounds: PASS
- Pure Lua stability runtime harness: PASS
- Lua 5.1 syntax for all scripts: PASS
- Localization XML parse: PASS

Total Python contract tests: **17 passed**.

## Requires live GAMMA validation

- Exact perceived recoil strength with each GAMMA weapon class
- Combined feel with GAMMA Enhanced Recoil
- Attachment/upgrade baseline invalidation across installed weapon packs
- Modded Exes method availability in the user's exact GAMMA build
- MCM rendering and option-change behavior
- Save/load and level-transition restoration against live engine objects

The package is implementation-complete but should be treated as a first live-test build until the in-game matrix in `TESTING.md` is completed.
