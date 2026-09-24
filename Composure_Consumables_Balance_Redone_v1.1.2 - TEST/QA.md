# Validation

- CSV rows: 83
- Unique item IDs: 83
- Cooked mutant rows: 30
- Raw mutant rows: 10
- Every represented gameplay field is explicitly written, including zero values.
- `mutant_part_boar_chop` is directly patched; no cooked/raw alias is assumed.
- Ukrainian Combat Ration zero gradual duration normalized to 90 seconds.
- Category stacking groups: meat, food, drink, alcohol, comfort food and smokes.
- Rest values use the verified GAMMA display conversion: `-20 * eat_sleepiness`.
- Composure uses the clean separated fallback because the active Sota UI does not
  render runtime-added native rows even after successful registration.
- Cigarettes: -2.5% Sleepiness, +5 instant and +5 gradual Composure over 30 seconds.
- Generated LTX sections and Composure mappings: 83 each.
