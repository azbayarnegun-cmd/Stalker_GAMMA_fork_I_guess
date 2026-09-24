# Changelog

## v1.1.2

- Corrected GAMMA Rest conversion. Workbook percentages now export at five times
  the raw `eat_sleepiness` values used in v1.1.0/v1.1.1, matching the native
  `Rest = -20 × eat_sleepiness` display scale.
- Rest targets now display as intended: vodka -25%, heavy meals -15%, light
  meals -5%, coffee +15%, energy drinks +10%, cigarettes +2.5%, and
  chocolate/protein +5%.
- Rest remains native and is never duplicated by the Composure tooltip.
- Restored reliable Composure information for Sota UI with a clean separated
  `COMPOSURE EFFECTS` block. Experimental runtime icon rows are off by default.

## v1.1.1

- Reworked item information into native GAMMA-style Composure icon rows.
- Rest now uses GAMMA's native stat row only; removed the duplicate custom
  Sleepiness line.
- Native rows are enabled by default with new setting keys, so v1.1.0's saved
  fallback preferences cannot keep the broken run-on text active.
- The compact fallback is now opt-in and uses clear inline separators.

## v1.1.0

- Rebalanced Sleepiness per use: vodka +25%, beer +10%, meals +5–15%,
  coffee -15%, energy drinks -10%, cigarettes -2.5%, and chocolate/protein -5%.
- Normalized cigarette effects to +5 instant and +5 gradual Composure over 30 seconds.
- Added signed Sleepiness values to the compatibility tooltip. Red means increased
  tiredness; green means reduced tiredness.
- Added generated runtime Sleepiness data and cross-file regression validation.
