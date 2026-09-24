#!/usr/bin/env python3
"""Static contract checks for Composure Core v2.1.0."""

from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "gamedata/scripts/composure_framework.script"
MCM = ROOT / "gamedata/scripts/composure_framework_mcm.script"
XML = ROOT / "gamedata/configs/text/eng/composure_framework.xml"

checks = []


def check(name, condition):
    checks.append((name, bool(condition)))


source = SCRIPT.read_text(encoding="utf-8")
mcm = MCM.read_text(encoding="utf-8")
xml_text = XML.read_text(encoding="utf-8")

check("core script exists", SCRIPT.is_file())
check("MCM script exists", MCM.is_file())
check("English text exists", XML.is_file())
check("Core version 2.1.0", 'local VERSION = "2.1.0"' in source)
check("API version 2 retained", "local API_VERSION = 2" in source)
check("0-100 range", "local MIN_VALUE = 0" in source and "local MAX_VALUE = 100" in source)
check("starting value 65", "local starting_value = 65" in source)
check("v2 save key retained", 'local SAVE_KEY = "composure_framework_v2"' in source)
check("legacy save key retained", 'local LEGACY_SAVE_KEY = "composure_mvp"' in source)
check("proportional legacy migration", "MAX_VALUE / 120" in source)

expected_tiers = {
    "high": 86,
    "medium_high": 70,
    "medium": 55,
    "medium_low": 40,
    "low": 16,
    "breaking_point": 1,
    "pass_out": 0,
}
for tier, minimum in expected_tiers.items():
    check(f"tier {tier} starts at {minimum}", bool(re.search(
        rf'id\s*=\s*"{tier}"\s*,\s*min\s*=\s*{minimum}\b', source
    )))

check("fast callback", 'RegisterScriptCallback("actor_on_update"' in source)
check("save callback", 'RegisterScriptCallback("save_state"' in source)
check("load callback", 'RegisterScriptCallback("load_state"' in source)
check("error isolation", source.count("pcall(") >= 4)
check("owner collision protection", source.count("owner_conflict(") >= 6)
check("bounded scheduler catch-up", "max_fast_dt_ms" in source and "max_slow_dt_ms" in source)
check("persistent timed entries", "collect_persistent" in source and "restore_registry" in source)
check("owner cleanup", "function clear_owner(owner)" in source)
check("modifier API", "function upsert_modifier" in source)
check("instant API", "function apply_instant" in source)
check("cap API", "function set_cap" in source)
check("recovery lock API", "function set_recovery_lock" in source)
check("policy extension API", "function register_adjustment_policy" in source)
check("listener API", "function register_listener" in source)
check("snapshot API", "function get_snapshot" in source)
check("diagnostics API", "function get_diagnostics" in source)
check("MCM intervals", "fast_interval" in mcm and "slow_interval" in mcm)
check("Core MCM label", "Composure - Core" in xml_text)

runtime_text = "\n".join(
    path.read_text(encoding="utf-8", errors="ignore")
    for path in (ROOT / "gamedata").rglob("*") if path.is_file()
)
check("no Main gameplay script", not (ROOT / "gamedata/scripts/composure_main.script").exists())
check("no Main MCM script", not (ROOT / "gamedata/scripts/composure_main_mcm.script").exists())
check("no built-in tier multiplier policy", "main.tier_multipliers" not in source)
check("no passive recovery source", "main.natural_recovery" not in source)
check("no global multiplier settings", "global_loss_multiplier" not in source and "global_recovery_multiplier" not in source)
check("no HUD implementation", not (ROOT / "gamedata/configs/ui").exists())
check("no audio assets", not (ROOT / "gamedata/sounds").exists())
check("no visual assets", "composure_visuals" not in runtime_text)
check("no legacy manager overwrite", not (ROOT / "gamedata/scripts/composure_manager.script").exists())

try:
    ET.parse(XML)
    check("localization XML parses", True)
except ET.ParseError:
    check("localization XML parses", False)

check("no goto", not re.search(r"\bgoto\b", source))
check("no bitwise operators", not re.search(r"(?<![<>=~])[|&](?![|&])", source))

failed = [name for name, ok in checks if not ok]
for name, ok in checks:
    print(("PASS" if ok else "FAIL") + "  " + name)
print(f"\n{len(checks) - len(failed)}/{len(checks)} checks passed")
sys.exit(1 if failed else 0)
