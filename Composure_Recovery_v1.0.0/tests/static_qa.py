#!/usr/bin/env python3
"""Static contract checks for Composure Recovery v1.0.0."""

from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "gamedata/scripts/composure_recovery.script"
MCM = ROOT / "gamedata/scripts/composure_recovery_mcm.script"
XML = ROOT / "gamedata/configs/text/eng/composure_recovery.xml"

checks = []


def check(name, condition):
    checks.append((name, bool(condition)))


source = SCRIPT.read_text(encoding="utf-8")
mcm = MCM.read_text(encoding="utf-8")
xml_text = XML.read_text(encoding="utf-8")

check("runtime script exists", SCRIPT.is_file())
check("MCM script exists", MCM.is_file())
check("localization exists", XML.is_file())
check("version 1.0.0", 'local VERSION = "1.0.0"' in source)
check("Framework API 2 required", "local REQUIRED_FRAMEWORK_API = 2" in source)
check("stable owner", 'local OWNER = "composure_recovery"' in source)
check("stable modifier id", 'local MODIFIER_ID = "recovery.safe_passive"' in source)
check("default rate 0.020/s", "local recovery_rate = 0.02" in source)
check("default target 65", "local recovery_target = 65" in source)
check("default delay 15", "local recovery_delay = 15" in source)
check("slow lane recovery", 'lane = "slow"' in source)
check("target-aware rate", "remaining / configured_slow_interval_seconds()" in source)
check("recovery lock check", "composure_framework.is_recovery_locked()" in source)
check("Pass Out block", "block_at_pass_out and value <= 0" in source)
check("GAMMA combat table", "xr_combat_ignore.fighting_with_actor_npcs" in source)
check("combat distance squared", "combat_distance * combat_distance" in source)
check("damage callback", 'RegisterScriptCallback("actor_on_before_hit"' in source)
check("weapon-fire callback", 'RegisterScriptCallback("actor_on_weapon_fired"' in source)
check("actor update callback", 'RegisterScriptCallback("actor_on_update"' in source)
check("load callback", 'RegisterScriptCallback("load_state"' in source)
check("level-change callback", 'RegisterScriptCallback("on_level_changing"' in source)
check("lifecycle delay", "unsafe_until_ms = now_ms() + recovery_delay * 1000" in source)
check("diagnostics API", "function get_diagnostics()" in source)
check("F9 diagnostics", "DIK_F9" in source and "DIK_F9" in mcm)
check("protected MCM access", "pcall(composure_recovery_mcm.get_config" in source)
check("protected Framework diagnostics", "pcall(composure_framework.get_diagnostics)" in source)
check("no set-value bypass", "composure_framework.set_value" not in source)
check("no direct instant recovery", "composure_framework.apply_instant" not in source)
check("no tier multiplier", "tier_multiplier" not in source and "loss_multiplier" not in source)
check("no health mutation", not re.search(r"\b(set_health|change_health)\b", source))
check("no stamina mutation", not re.search(r"\b(set_power|change_power)\b", source))

expected_options = {
    "enabled", "recovery_rate", "recovery_target", "recovery_delay",
    "respect_recovery_locks", "block_at_pass_out", "detect_active_combat",
    "combat_distance", "combat_inertia", "reset_on_damage",
    "reset_on_weapon_fire", "debug_key", "debug_log",
}
option_ids = set(re.findall(r'\{\s*id\s*=\s*"([a-z0-9_]+)"\s*,\s*type\s*=', mcm))
option_ids = {item for item in option_ids if not item.startswith("line")}
check("all expected MCM options", option_ids == expected_options)

try:
    root = ET.fromstring(xml_text)
    localization_ids = {node.attrib.get("id") for node in root.findall("string")}
    check("localization XML parses", True)
    check("all MCM options localized", all(
        f"ui_mcm_composure_recovery_{item}" in localization_ids
        for item in option_ids
    ))
except ET.ParseError:
    check("localization XML parses", False)
    check("all MCM options localized", False)

code_without_line_comments = "\n".join(line.split("--", 1)[0] for line in source.splitlines())
code_without_strings = re.sub(r'"(?:\\.|[^"\\])*"', '""', code_without_line_comments)
check("no goto", not re.search(r"\bgoto\b", code_without_strings))
check("no Lua 5.3 bitwise operators", not re.search(
    r"(?<![<>=~])[|&](?![|&])", code_without_strings
))

failed = [name for name, ok in checks if not ok]
for name, ok in checks:
    print(("PASS" if ok else "FAIL") + "  " + name)
print(f"\n{len(checks) - len(failed)}/{len(checks)} checks passed")
sys.exit(1 if failed else 0)
