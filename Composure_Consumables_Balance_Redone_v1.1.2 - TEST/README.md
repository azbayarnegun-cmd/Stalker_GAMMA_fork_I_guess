# Composure Consumables — Balance Redone v1.1.2

Complete replacement for the older Composure Consumables/Redux/Combined builds.

## Requirements

- Composure Core exposing `composure_framework` API 2.
- Consumable Time-Skip is optional and remains compatible.

## Install / MO2 order

1. Composure Core v1.0.0
2. Composure Recovery v1.0.0
3. Composure Feedback v1.1.1
4. Composure Combat v1.0.1
5. Composure Thoughts Extended v4.1.0
6. **Composure Consumables — Balance Redone v1.1.2**
7. Unified Simulated Time GAMMA v1.2.0
8. Consumable Time Skip v1.0.3

Disable all older consumables balance builds: Composure Consumables v1.1.2,
Composure Consumables Redux v1.2.0, Composure Consumables and Rebalance Combined,
Redux 3 Balance Addon v1.0.x, and the temporary Mutant Food Satiety 1% test.

This mod replaces Sheet Driven v2.0.0/v2.0.1 and every older
Consumables/Redux/Combined balance package. Do not enable them together.

## What is controlled by the workbook

The 83 workbook rows control weight, uses, cost, satiety, thirst, sleepiness, alcohol,
health, radiation, booster duration, stamina recovery, radiation restoration,
radiation/chemical/psychic protection, carried weight, and instant/gradual
Composure. Tier and Total columns are documentation only.

The raw Zone-produced sections (for example `mutant_part_boar_chop`) and cooked
`meat_*` sections are separate rows and are both patched.

For exact Composure values, set Instant and Gradual scales in the Consumables
MCM to 1.00. Tobacco/cigar fixed effects retain Time-Skip compatibility.

The workbook's `Thirst Viewer` column is informational only. The mod exports the
raw `Thirst` value directly to `eat_thirstiness`.

Sleepiness changes are applied per use, including every use of multi-use packs:

- vodka: +25%; beer: +10%
- heavy meals: +15%; medium meals: +10%; light meals: +5%
- coffee: -15%; energy drinks: -10%
- cigarettes: -2.5%; protein bars and chocolate: -5%

GAMMA displays the engine's `eat_sleepiness` field as **Rest**, using 20 display
percentage points per raw unit with the opposite sign. The builder converts the
workbook's intended percentages to that native scale: a heavy meal's +15%
Sleepiness displays as Rest -15%, while coffee's -15% Sleepiness displays as
Rest +15%. Rest is shown only by GAMMA's native stat row.

The active Sota/GAMMA item panel accepts runtime stat registration but does not
render those added rows. Composure therefore uses a reliable compact block by
default: `COMPOSURE EFFECTS • Instant | Over time/After-effect | Duration`.
It does not repeat Rest. Cigarettes provide +5 instant and +5 gradual Composure
over 30 seconds per use.

Gradual Composure effects are separated into six stacking groups: meat, food,
drink, alcohol, comfort food and smokes. A new effect replaces only an effect
in its own category; unrelated categories can remain active together.

## Future sheet updates

Edit `balance/Composure_Redone_1.xlsx`, export the `Consumables Balance`
sheet as CSV UTF-8, remove the display-only `Thirst Viewer` column, and replace
`balance/Food_table.csv`. Then run `python tools/rebuild_from_csv.py` from the mod folder. The
script validates duplicates, required values, percentage conversion and gradual
durations before replacing the generated LTX and Composure data files.

The Ukrainian Combat Ration has gradual Composure but a zero duration in the
workbook. The builder normalizes that single invalid duration to 90 seconds so
its gradual +6 effect is not silently discarded.
