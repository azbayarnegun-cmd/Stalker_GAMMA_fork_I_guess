#!/usr/bin/env python3
"""Cross-check the v1.1.2 sheet export, Rest conversion, and tooltip data."""

from __future__ import annotations

import csv
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "balance/Food_table.csv"
LTX_PATH = ROOT / "gamedata/configs/mod_system_zzzzzzzzzz_sheet_consumables.ltx"
DATA_PATH = ROOT / "gamedata/scripts/composure_consumables_data.script"
TOOLTIP_PATH = ROOT / "gamedata/scripts/zzz_composure_consumables_tooltip.script"


def close(actual: float, expected: float, item: str) -> None:
    if not math.isclose(actual, expected, rel_tol=0, abs_tol=1e-9):
        raise AssertionError(f"{item}: expected {expected}, got {actual}")


with CSV_PATH.open(encoding="utf-8-sig", newline="") as handle:
    rows = list(csv.DictReader(handle))

assert len(rows) == 83, f"expected 83 CSV rows, got {len(rows)}"
by_id = {row["ID"].strip(): row for row in rows}
assert len(by_id) == len(rows), "duplicate CSV IDs"

ltx_text = LTX_PATH.read_text(encoding="utf-8")
ltx_sleepiness = {
    section: float(value)
    for section, value in re.findall(
        r"!\[([^\]]+)\][\s\S]*?^eat_sleepiness\s*=\s*([-+0-9.eE]+)\s*$",
        ltx_text,
        re.MULTILINE,
    )
}

data_text = DATA_PATH.read_text(encoding="utf-8")
data_rows = {
    section: (float(instant), float(gradual), float(duration), float(sleepiness))
    for section, instant, gradual, duration, sleepiness in re.findall(
        r'sections = \{ "([^"]+)" \}, instant = ([-+0-9.eE]+), '
        r'gradual = ([-+0-9.eE]+), duration = ([-+0-9.eE]+), '
        r'sleepiness = ([-+0-9.eE]+)',
        data_text,
    )
}

assert len(ltx_sleepiness) == len(rows), "LTX section count differs from CSV"
assert len(data_rows) == len(rows), "runtime data count differs from CSV"
for section, row in by_id.items():
    expected = float(row["Sleepiness"])
    close(ltx_sleepiness[section], expected * 5, f"{section} LTX sleepiness")
    close(data_rows[section][3], expected, f"{section} runtime sleepiness")

expected_sleepiness = {
    "energy_drink": -0.10,
    "coffee_drink": -0.15,
    "brewed_coffee": -0.15,
    "ground_coffee": -0.15,
    "chocolate": -0.05,
    "chocolate_p": -0.05,
    "protein": -0.05,
    "vodka_quality": 0.25,
    "bottle_metal": 0.25,
    "vodka2": 0.25,
    "vodka": 0.25,
    "beer": 0.10,
}
for section, expected in expected_sleepiness.items():
    close(float(by_id[section]["Sleepiness"]), expected, section)

expected_rest_display = {
    "energy_drink": 10,
    "coffee_drink": 15,
    "brewed_coffee": 15,
    "ground_coffee": 15,
    "chocolate": 5,
    "chocolate_p": 5,
    "protein": 5,
    "vodka_quality": -25,
    "bottle_metal": -25,
    "vodka2": -25,
    "vodka": -25,
    "beer": -10,
}
for section, expected in expected_rest_display.items():
    close(-ltx_sleepiness[section] * 20, expected, f"{section} Rest display")

cigarettes = [row for row in rows if row["Cat."].strip() == "Cigar"]
assert cigarettes, "no cigarette rows found"
for row in cigarettes:
    section = row["ID"].strip()
    close(float(row["Sleepiness"]), -0.025, f"{section} sleepiness")
    close(float(row["Instant Composure"]), 5, f"{section} instant")
    close(float(row["Gradual Composure"]), 5, f"{section} gradual")
    close(float(row["Composure Duration"]), 30, f"{section} duration")
    instant, gradual, duration, _ = data_rows[section]
    close(instant, 5, f"{section} runtime instant")
    close(gradual, 5, f"{section} runtime gradual")
    close(duration, 30, f"{section} runtime duration")

meal_categories = {"Raw", "Mutant food", "Food", "Food - MRE"}
comfort_meals = {"salmon", "kolbasa", "nuts", "sausage", "raisins"}
for section, row in by_id.items():
    if row["Cat."].strip() not in meal_categories and section not in comfort_meals:
        continue
    satiety = float(row["Satiety"])
    expected = 0.15 if satiety >= 0.30 else 0.10 if satiety >= 0.15 else 0.05
    close(float(row["Sleepiness"]), expected, f"{section} meal tier")

tooltip = TOOLTIP_PATH.read_text(encoding="utf-8")
assert 'cfg("try_native_rows", false)' in tooltip
assert 'cfg("composure_block", true)' in tooltip
assert 'colored_line("Sleepiness"' not in tooltip
assert 'table.concat(segments, "  |  ")' in tooltip
assert 'COMPOSURE EFFECTS  •  ' in tooltip
assert 'composure_tooltip:redone-v1.1.2' in tooltip
assert 'get_balance_version() return "balance-redone-v1.1.2"' in data_text

for xml_path in (ROOT / "gamedata/configs").rglob("*.xml"):
    ET.parse(xml_path)

print(f"PASS: {len(rows)} consumables synchronized; {len(cigarettes)} cigarette rows validated")
