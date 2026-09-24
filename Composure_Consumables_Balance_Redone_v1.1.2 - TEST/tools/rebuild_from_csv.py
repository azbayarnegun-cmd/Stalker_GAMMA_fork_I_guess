#!/usr/bin/env python3
"""Build Consumables Balance Redone v1.1.2 from Composure Redone 1.xlsx."""

from __future__ import annotations

import csv
import math
import shutil
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
IN_PLACE = SCRIPT_DIR.name == "tools" and (SCRIPT_DIR.parent / "gamedata").is_dir()
if IN_PLACE:
    ROOT = SCRIPT_DIR.parent
    SOURCE = ROOT / "balance/Food_table.csv"
    BASE = ROOT
    OUT = ROOT
else:
    ROOT = SCRIPT_DIR
    SOURCE = ROOT / "work_redone/Food_table.csv"
    WORKBOOK_SOURCE = ROOT / "upload/Composure Redone 1.xlsx"
    BASE = ROOT / "outputs/Composure_Consumables_Sheet_Driven_v2.0.1"
    OUT = ROOT / "outputs/Composure_Consumables_Balance_Redone_v1.1.2"

# Spreadsheet display units -> native GAMMA LTX units.
MSV_TO_LTX = 0.000044
PROTECTION_POINT_TO_LTX = 0.00035
STAMINA_PERCENT_TO_LTX = 1.0 / 20.0
# GAMMA's Rest tooltip displays -20 percentage points per eat_sleepiness unit.
# The workbook stores intended percentage changes as decimals (15% = 0.15).
SLEEPINESS_PERCENT_TO_LTX = 5.0

PERCENT_COLUMNS = {
    "Satiety", "Thirst", "Sleepiness", "Alcohol", "Stamina Recovery",
    "Health change", "Chemical Res",
}

EXPECTED_HEADERS = [
    "Cat.", "Name", "Weight", "Uses", "Cost", "Composure Tier",
    "Satiety \nTier", "Instant Composure", "Gradual Composure",
    "Composure Duration", "Total Composure", "Satiety", "Thirst",
    "Sleepiness", "Alcohol", "Duration", "Stamina Recovery",
    "Total stamina recovery", "Health change", "Radiation",
    "Radiation restoration", "Total radiation restoration", "Radiation Res",
    "Chemical Res", "Psychic Res", "Weight Carried", "ID", "Tier",
]


def present(value: object) -> bool:
    return value is not None and str(value).strip() != ""


def number(value: object) -> float:
    text = str(value).strip().replace(",", "")
    if text.endswith("%"):
        return float(text[:-1]) / 100.0
    return float(text)


def fmt(value: float) -> str:
    if abs(value) < 5e-14:
        return "0"
    if float(value).is_integer():
        return str(int(value))
    return format(float(value), ".12g")


def signed(value: float) -> str:
    return ("+" if value > 0 else "") + fmt(value)


def lua_string(value: object) -> str:
    text = str(value).replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f'"{text}"'


def duration_text(seconds: float) -> str:
    seconds_i = int(round(seconds))
    if seconds_i % 60 == 0 and seconds_i > 0:
        minutes = seconds_i // 60
        return f"{minutes} min"
    return f"{seconds_i} sec"


def read_rows() -> list[dict[str, str]]:
    with SOURCE.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        if headers != EXPECTED_HEADERS:
            raise ValueError(f"Unexpected CSV headers: {headers!r}")
        rows = [{key: (value or "").strip() for key, value in row.items()} for row in reader]
    if not rows:
        raise ValueError("CSV contains no consumables")
    ids = [row["ID"] for row in rows]
    if any(not section for section in ids):
        raise ValueError("Every row must have an ID")
    duplicates = sorted({section for section in ids if ids.count(section) > 1})
    if duplicates:
        raise ValueError(f"Duplicate IDs: {duplicates}")
    return rows


def validate_row(row: dict[str, str]) -> None:
    required = [
        "Weight", "Uses", "Cost", "Instant Composure", "Gradual Composure",
        "Satiety", "Thirst", "Sleepiness", "Alcohol", "Duration",
        "Stamina Recovery", "Health change", "Radiation",
        "Radiation restoration", "Radiation Res", "Chemical Res",
        "Psychic Res", "Weight Carried",
    ]
    for column in required:
        if not present(row[column]):
            raise ValueError(f"{row['ID']}: missing required {column}")
        number(row[column])
    uses = number(row["Uses"])
    if uses < 1 or not uses.is_integer():
        raise ValueError(f"{row['ID']}: Uses must be a positive integer")
    if number(row["Weight"]) < 0 or number(row["Cost"]) < 0:
        raise ValueError(f"{row['ID']}: Weight and Cost cannot be negative")
    gradual = number(row["Gradual Composure"])
    duration = number(row["Composure Duration"]) if present(row["Composure Duration"]) else 0
    if gradual != 0 and duration <= 0 and row["ID"] != "ration_ukr":
        raise ValueError(f"{row['ID']}: gradual Composure requires a positive duration")


def composure_duration(row: dict[str, str]) -> float:
    duration = number(row["Composure Duration"]) if present(row["Composure Duration"]) else 0
    if row["ID"] == "ration_ukr" and number(row["Gradual Composure"]) != 0 and duration <= 0:
        return 90.0
    return duration


def stacking_group(category: str) -> str:
    if category in {"Raw", "Mutant food"}:
        return "consumables_meat"
    if category in {"Food", "Food - MRE"}:
        return "consumables_food"
    if category == "Drink":
        return "consumables_drink"
    if category == "Alcohol":
        return "consumables_alcohol"
    if category == "Comfort food":
        return "consumables_comfort_food"
    if category in {"Cigar", "Cigar - Long", "Cigar - Ingredient"}:
        return "consumables_smokes"
    raise ValueError(f"Unknown category for stacking group: {category}")


def build_ltx(rows: list[dict[str, str]]) -> str:
    lines = [
        "; Generated from balance/Food_table.csv — do not hand-edit.",
        "; Complete sheet-driven consumables balance. Percent cells become decimals.",
        "; Radiation display units use 0.000044 raw units per point.",
        "",
    ]
    for row in rows:
        section = row["ID"]
        uses = int(number(row["Uses"]))
        chemical_points = number(row["Chemical Res"]) * 100.0
        values = [
            ("use_condition", "true" if uses > 1 else "false"),
            ("max_uses", str(uses)),
            ("cost", fmt(number(row["Cost"]))),
            ("inv_weight", fmt(number(row["Weight"]))),
            ("eat_satiety", fmt(number(row["Satiety"]))),
            ("eat_thirstiness", fmt(number(row["Thirst"]))),
            ("eat_sleepiness", fmt(number(row["Sleepiness"]) * SLEEPINESS_PERCENT_TO_LTX)),
            ("eat_alcohol", fmt(number(row["Alcohol"]))),
            ("eat_health", fmt(number(row["Health change"]))),
            ("eat_radiation", fmt(number(row["Radiation"]) * MSV_TO_LTX)),
            ("boost_time", fmt(number(row["Duration"]))),
            ("boost_power_restore", fmt(number(row["Stamina Recovery"]) * STAMINA_PERCENT_TO_LTX)),
            ("boost_radiation_restore", fmt(number(row["Radiation restoration"]) * MSV_TO_LTX)),
            ("boost_radiation_protection", fmt(number(row["Radiation Res"]) * PROTECTION_POINT_TO_LTX)),
            ("boost_chemburn_protection", fmt(chemical_points * PROTECTION_POINT_TO_LTX)),
            ("boost_telepat_protection", fmt(number(row["Psychic Res"]) * PROTECTION_POINT_TO_LTX)),
            ("boost_max_weight", fmt(number(row["Weight Carried"]))),
        ]
        if uses > 1:
            values.insert(1, ("condition_bar", "uses_progess_bar"))
        lines.extend([f"; {row['Cat.']} — {row['Name']}", f"![{section}]"])
        width = max(len(key) for key, _ in values)
        lines.extend(f"{key.ljust(width)} = {value}" for key, value in values)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_composure_data(rows: list[dict[str, str]]) -> str:
    lines = [
        "-- Generated from balance/Food_table.csv. Do not hand-edit balance values.",
        "local rows = {",
    ]
    for index, row in enumerate(rows, 1):
        section = row["ID"]
        instant = number(row["Instant Composure"])
        gradual = number(row["Gradual Composure"])
        duration = composure_duration(row)
        activation = "On use" if instant != 0 or gradual != 0 else "None"
        fixed = section in {"cigar", "hand_rolling_tobacco", "tobacco"}
        group = stacking_group(row["Cat."])
        phrases = []
        if instant != 0:
            phrases.append(f"{signed(instant)} Composure instantly")
        if gradual != 0:
            phrases.append(f"{signed(gradual)} Composure over {duration_text(duration)}")
        info = "; ".join(phrases) if phrases else "No direct Composure change"
        fixed_text = ", fixed_effect = true" if fixed else ""
        lines.extend([
            f"    {{ key = \"sheet_{index:03d}_{section}\", type = {lua_string(row['Cat.'])}, name = {lua_string(row['Name'])},",
            f"      sections = {{ {lua_string(section)} }}, instant = {fmt(instant)}, gradual = {fmt(gradual)}, duration = {fmt(duration)}, sleepiness = {fmt(number(row['Sleepiness']))}{fixed_text},",
            f"      resistance = nil, gain_buff = nil, stacking_group = {lua_string(group)}, activation = {lua_string(activation)},",
            f"      rationale = \"Sheet-driven balance profile.\", info = {lua_string(info)}, hover = {lua_string('COMPOSURE EFFECTS' + chr(10) + '• ' + info)} }},",
        ])
    lines.extend([
        "}",
        "",
        "local by_section = {}",
        "for _, row in ipairs(rows) do",
        "    for _, section in ipairs(row.sections) do by_section[section] = row end",
        "end",
        "",
        "function get_rows() return rows end",
        "function get(section) return section and by_section[section] or nil end",
        "function get_section_count() local n = 0 for _ in pairs(by_section) do n = n + 1 end return n end",
        "function get_balance_version() return \"balance-redone-v1.1.2\" end",
        "",
    ])
    return "\n".join(lines)


def write_docs(rows: list[dict[str, str]]) -> None:
    readme = """# Composure Consumables — Balance Redone v1.1.2

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
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")
    (OUT / "VERSION.txt").write_text("Composure Consumables — Balance Redone v1.1.2\n", encoding="utf-8")
    testing = """# In-game smoke test

Use a disposable save and set the Consumables MCM Instant and Gradual scales to
1.00. Fully restart the game after installing or rebuilding the mod.

1. Spawn fresh Boar Chops C (`meat_boar`): 1 use, raw satiety `0.52`, cost 1034.
2. Spawn fresh raw Boar Chops (`mutant_part_boar_chop`): 1 use, raw satiety `0.16`.
3. Spawn a fresh Flask (`flask`): 4 uses and raw thirst `-2.00` per use.
4. Hover the items and confirm a separated `COMPOSURE EFFECTS` block appears.
   Rest must appear only once as GAMMA's native stat.
5. Confirm native Rest displays approximately: vodka -25%, coffee +15%, energy
   drink +10%, heavy meal -15%, light meal -5%, chocolate/protein +5%, and
   cigarettes +2.5% per use.
6. Confirm a cigarette gives +5 instant Composure and +5 over 30 seconds.
7. Check one other multi-use item and confirm its use counter matches the workbook.
8. Search the newest `xray_*.log` for `SCRIPT ERROR` and `stack trace`.

Existing partially used inventory objects may retain old condition/use state;
always use newly spawned or purchased items for max-use testing.
"""
    (OUT / "TESTING.md").write_text(testing, encoding="utf-8")
    qa = f"""# Validation

- CSV rows: {len(rows)}
- Unique item IDs: {len({row['ID'] for row in rows})}
- Cooked mutant rows: {sum(row['Cat.'] == 'Mutant food' for row in rows)}
- Raw mutant rows: {sum(row['Cat.'] == 'Raw' for row in rows)}
- Every represented gameplay field is explicitly written, including zero values.
- `mutant_part_boar_chop` is directly patched; no cooked/raw alias is assumed.
- Ukrainian Combat Ration zero gradual duration normalized to 90 seconds.
- Category stacking groups: meat, food, drink, alcohol, comfort food and smokes.
- Rest values use the verified GAMMA display conversion: `-20 * eat_sleepiness`.
- Composure uses the clean separated fallback because the active Sota UI does not
  render runtime-added native rows even after successful registration.
- Cigarettes: -2.5% Sleepiness, +5 instant and +5 gradual Composure over 30 seconds.
- Generated LTX sections and Composure mappings: {len(rows)} each.
"""
    (OUT / "QA.md").write_text(qa, encoding="utf-8")


def stamp_script_versions() -> None:
    for relative in [
        "gamedata/scripts/composure_consumables.script",
        "gamedata/scripts/composure_consumables_mcm.script",
        "gamedata/scripts/zzz_composure_consumables_tooltip.script",
    ]:
        path = OUT / relative
        text = path.read_text(encoding="utf-8")
        text = text.replace("Composure Consumables v1.1.3", "Composure Consumables — Balance Redone v1.1.2")
        text = text.replace("Composure Consumables — Sheet Driven v2.0.1", "Composure Consumables — Balance Redone v1.1.2")
        text = text.replace("Composure Consumables — Balance Redone v1.0.0", "Composure Consumables — Balance Redone v1.1.2")
        text = text.replace("Composure Consumables — Balance Redone v1.1.0", "Composure Consumables — Balance Redone v1.1.2")
        text = text.replace("Composure Consumables — Balance Redone v1.1.1", "Composure Consumables — Balance Redone v1.1.2")
        text = text.replace("composure_tooltip:v1.1.3", "composure_tooltip:redone-v1.1.2")
        text = text.replace("composure_tooltip:sheet-v2.0.1", "composure_tooltip:redone-v1.1.2")
        text = text.replace("composure_tooltip:redone-v1.0.0", "composure_tooltip:redone-v1.1.2")
        text = text.replace("composure_tooltip:redone-v1.1.0", "composure_tooltip:redone-v1.1.2")
        text = text.replace("composure_tooltip:redone-v1.1.1", "composure_tooltip:redone-v1.1.2")
        text = text.replace('local VERSION = "1.1.3"', 'local VERSION = "1.1.2"')
        text = text.replace('local VERSION = "1.1.0"', 'local VERSION = "1.1.2"')
        text = text.replace('local VERSION = "1.1.1"', 'local VERSION = "1.1.2"')
        path.write_text(text, encoding="utf-8")


def build() -> None:
    rows = read_rows()
    for row in rows:
        validate_row(row)
    if not IN_PLACE:
        if OUT.exists():
            shutil.rmtree(OUT)
        shutil.copytree(BASE, OUT)
        # Old QA scripts describe a different workbook and are not shipped.
        shutil.rmtree(OUT / "tests", ignore_errors=True)
    (OUT / "balance").mkdir(parents=True, exist_ok=True)
    (OUT / "tools").mkdir(parents=True, exist_ok=True)
    if not IN_PLACE:
        shutil.copy2(SOURCE, OUT / "balance/Food_table.csv")
        (OUT / "balance/Composure_Consumables_Balance.xlsx").unlink(missing_ok=True)
        shutil.copy2(WORKBOOK_SOURCE, OUT / "balance/Composure_Redone_1.xlsx")
    (OUT / "gamedata/configs/mod_system_item_uses.ltx").unlink(missing_ok=True)
    (OUT / "gamedata/configs/mod_system_zzzzzzzzzz_sheet_consumables.ltx").write_text(build_ltx(rows), encoding="utf-8")
    (OUT / "gamedata/scripts/composure_consumables_data.script").write_text(build_composure_data(rows), encoding="utf-8")
    stamp_script_versions()
    write_docs(rows)
    if not IN_PLACE:
        shutil.copy2(Path(__file__), OUT / "tools/rebuild_from_csv.py")
    print(f"Built {OUT} from {len(rows)} rows")


if __name__ == "__main__":
    build()
