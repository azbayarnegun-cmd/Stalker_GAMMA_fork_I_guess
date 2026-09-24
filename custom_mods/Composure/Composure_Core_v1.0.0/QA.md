# Composure Core v2.1.0 QA

## Automated scope

Static QA verifies:

- Core package layout and localization
- Version 2.1.0 with API compatibility level 2
- Canonical 0-100 value and tier thresholds
- Existing Framework v2 save key
- Legacy 0-120 migration
- Save/load and bounded scheduler callbacks
- Instant, continuous, timed, cap, recovery-lock, event and snapshot APIs
- Protected callback execution and owner collision rejection
- Absence of Main, built-in balance multipliers and passive recovery
- Absence of HUD, Audio and Visuals in this foundation release
- LuaJIT/Lua 5.1-safe source patterns

## Still requires in-game verification

Static checks cannot prove engine callback order, MCM rendering, save
serialization, exact scheduler timing, or compatibility with every current
consumer module. Complete `TESTING.md` before declaring the package stable.
