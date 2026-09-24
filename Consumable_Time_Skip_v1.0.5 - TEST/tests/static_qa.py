#!/usr/bin/env python3
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "gamedata/scripts/consumable_time_skip.script"
MCM = ROOT / "gamedata/scripts/consumable_time_skip_mcm.script"
XML = ROOT / "gamedata/configs/text/eng/consumable_time_skip.xml"
DDS = ROOT / "gamedata/textures/ui/consumable_time_skip/black.dds"
BRIDGE = ROOT / "gamedata/scripts/consumable_time_skip_composure.script"
EVENT_BRIDGE = ROOT / "gamedata/scripts/zzz_consumable_time_skip_event_safe.script"

errors = []
for path in (SCRIPT, MCM, BRIDGE, EVENT_BRIDGE, XML, DDS):
    if not path.is_file():
        errors.append(f"missing: {path.relative_to(ROOT)}")

if XML.is_file():
    try:
        ET.parse(XML)
    except ET.ParseError as exc:
        errors.append(f"localization XML invalid: {exc}")

if SCRIPT.is_file():
    text = SCRIPT.read_text(encoding="utf-8")
    required = (
        'RegisterScriptCallback("actor_on_item_before_use"',
        'RegisterScriptCallback("actor_on_item_use"',
        "a:force_update()",
        "_change_game_time(0, 0, minutes)",
        "function register_item(",
        "function test(",
        "function abort(",
        "release_deferred_composure",
        "elapsed_text",
        "tobacco_animation_delay",
        "hand_rolling_tobacco",
        "brewed_coffee",
        "is_strong_alcohol",
        "sheltered_event_consumable",
        "psi_storm_active",
        "psi_storm_manager",
        "xr_conditions.surge_started",
        "surge_manager.actor_in_cover",
        "function can_allow_sheltered_event_consumable(",
    )
    for token in required:
        if token not in text:
            errors.append(f"core token missing: {token}")

if MCM.is_file():
    text = MCM.read_text(encoding="utf-8")
    for token in ("alcohol_minutes", "allow_sheltered_event_consumables",
                  "coffee_minutes", "tobacco_minutes",
                  "tobacco_animation_delay", "advance_composure", "tester_key"):
        if token not in text:
            errors.append(f"MCM token missing: {token}")

if BRIDGE.is_file():
    text = BRIDGE.read_text(encoding="utf-8")
    for token in ("function advance(", "get_snapshot", "apply_delta",
                  "age_modifier", "age_cap", "age_lock"):
        if token not in text:
            errors.append(f"Composure bridge token missing: {token}")

if EVENT_BRIDGE.is_file():
    text = EVENT_BRIDGE.read_text(encoding="utf-8")
    for token in ('RegisterScriptCallback("actor_on_item_before_use"',
                  "can_allow_sheltered_event_consumable", "flags.ret_value = true"):
        if token not in text:
            errors.append(f"emission bridge token missing: {token}")

if errors:
    print("FAIL")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("PASS: Consumable Time-Skip static QA")
