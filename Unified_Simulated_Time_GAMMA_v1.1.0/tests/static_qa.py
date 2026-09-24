#!/usr/bin/env python3
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "gamedata/scripts"
CONFIGS = ROOT / "gamedata/configs"

errors = []
checks = 0


def check(condition, message):
    global checks
    checks += 1
    if not condition:
        errors.append(message)


required = (
    SCRIPTS / "simulated_time.script",
    SCRIPTS / "unified_time_skip_integrations.script",
    SCRIPTS / "unified_time_skip_mcm.script",
    SCRIPTS / "immersive_campfire_saving_compat.script",
    CONFIGS / "misc/unified_level_transition_routes.ltx",
    CONFIGS / "text/eng/st_simulated_time.xml",
    CONFIGS / "text/eng/unified_time_skip.xml",
    CONFIGS / "unlocalizers/unlocalizer_simulated_time_sleep.ltx",
    ROOT / "README.md",
    ROOT / "TESTING.md",
    ROOT / "VERSION.txt",
)
for path in required:
    check(path.is_file(), f"missing {path.relative_to(ROOT)}")

for forbidden in (
    "gamedata/scripts/ui_sr_teleport.script",
    "gamedata/scripts/ui_main_menu.script",
    "gamedata/scripts/ui_save_dialog.script",
    "gamedata/scripts/level_input.script",
    "gamedata/scripts/bind_campfire.script",
    "gamedata/scripts/zzz_simulated_time_travel.script",
    "gamedata/configs/sr_teleport_sections.ltx",
):
    check(not (ROOT / forbidden).exists(), f"forbidden override: {forbidden}")

for xml in (CONFIGS / "text/eng/st_simulated_time.xml",
            CONFIGS / "text/eng/unified_time_skip.xml"):
    try:
        ET.parse(xml)
        check(True, f"XML parses: {xml.name}")
    except ET.ParseError as exc:
        check(False, f"invalid XML {xml.name}: {exc}")

core = (SCRIPTS / "simulated_time.script").read_text(encoding="utf-8")
for token in (
    "function advance(total_minutes, opts)",
    "function advance_sync(total_minutes, step_size)",
    "function abort(reason)",
    "pcall(s.on_abort, reason",
    "requested_steps = tonumber(opts.steps)",
    "advance_composure(step)",
    'unified_cfg("step_minutes", DEFAULT_STEP)',
    'RegisterScriptCallback("on_before_level_changing"',
    "pcall(restore_alife, s.saved)",
    "hide_overlay()",
):
    check(token in core, f"core token missing: {token}")

integrations = (SCRIPTS / "unified_time_skip_integrations.script").read_text(encoding="utf-8")
for token in (
    "ui_sr_teleport.msg_box_ui",
    "class_ref.OnMsgOk = wrapped_transition",
    "begin_transition(self, args, captured_original)",
    "simulated_time.passthrough = true",
    "suppress_transition_clock = true",
    "clear_transition_clock_guard",
    "choose_transition_minutes(section)",
    "unified_level_transition_routes.ltx",
    'enabled("sleep_enabled")',
    'enabled("books_enabled")',
    'enabled("anabiotic_enabled")',
    'enabled("placeable_campfire_enabled")',
    'enabled("flash_enabled")',
    'enabled("soulslike_enabled")',
    "consumable_time_skip.is_active",
    "function test_transition(minutes)",
    "transition_step_count(minutes)",
    "hold_environment_events(next_minutes)",
    "remaining_after_travel(environment_before, minutes)",
    "restore_environment_countdown(",
    "protect_actor_for_transition()",
    "on_abort = function(reason, sim_state)",
    "apply_arrival_event_grace(state)",
    "st_uts_transition_blocked_anomaly",
):
    check(token in integrations, f"integration token missing: {token}")

campfire = (SCRIPTS / "immersive_campfire_saving_compat.script").read_text(encoding="utf-8")
for token in (
    'cfg("campfire_save_enabled")',
    "bind_campfire.get_nearby_campfire",
    "ui_save_dialog.UISaveDialog or ui_save_dialog.save_dialog",
    'RegisterScriptCallback("on_before_save_input"',
    "consumable_time_skip.is_active",
    "consumable_time_skip_composure.advance",
    "simulated_time.passthrough = true",
):
    check(token in campfire, f"campfire token missing: {token}")

mcm = (SCRIPTS / "unified_time_skip_mcm.script").read_text(encoding="utf-8")
mcm_keys = (
    "master_enabled", "step_minutes", "composure_integration", "show_messages",
    "debug_log", "sleep_enabled", "level_transition_enabled",
    "transition_fallback_min", "transition_fallback_max", "campfire_save_enabled",
    "campfire_require_mode", "campfire_radius", "campfire_min_minutes",
    "campfire_max_minutes", "campfire_fade_seconds", "campfire_mute_audio",
    "campfire_force_alife", "books_enabled", "anabiotic_enabled",
    "placeable_campfire_enabled", "flash_enabled", "soulslike_enabled",
)
for key in mcm_keys:
    check(f'id = "{key}"' in mcm, f"MCM option missing: {key}")

xml_text = (CONFIGS / "text/eng/unified_time_skip.xml").read_text(encoding="utf-8")
for key in mcm_keys:
    check(f'id="ui_mcm_unified_time_skip_{key}"' in xml_text,
          f"MCM label missing: {key}")

routes = (CONFIGS / "misc/unified_level_transition_routes.ltx").read_text(
    encoding="utf-8", errors="replace")
section_count = sum(1 for line in routes.splitlines()
                    if line.strip().startswith("[") and line.strip().endswith("]"))
check(section_count >= 90, f"route table unexpectedly small: {section_count} sections")
check("hours_min" in routes and "minutes_max" in routes, "route duration fields missing")

combined_lua = "\n".join(path.read_text(encoding="utf-8") for path in SCRIPTS.glob("*.script"))
for forbidden in ("goto ", "::", "//", "<const>", "table.unpack"):
    check(forbidden not in combined_lua, f"LuaJIT-incompatible token: {forbidden}")

check("async no-ChangeLevel" not in combined_lua,
      "broken asynchronous Travel catch-all code was retained")

if errors:
    print(f"FAILED: {len(errors)} of {checks} checks")
    for error in errors:
        print(" -", error)
    sys.exit(1)
print(f"PASS: {checks}/{checks} static checks")
