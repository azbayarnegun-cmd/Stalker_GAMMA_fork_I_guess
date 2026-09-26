#!/usr/bin/env python3
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "gamedata/scripts/composure_combat.script"
MCM = ROOT / "gamedata/scripts/composure_combat_mcm.script"
XML = ROOT / "gamedata/configs/text/eng/composure_combat.xml"
errors = []
checks = 0


def check(condition, message):
    global checks
    checks += 1
    if not condition:
        errors.append(message)


for rel in [
    "README.md", "TESTING.md", "QA.md", "VERSION.txt",
    "gamedata/scripts/composure_combat.script",
    "gamedata/scripts/composure_combat_mcm.script",
    "gamedata/configs/text/eng/composure_combat.xml",
]:
    check((ROOT / rel).is_file(), f"missing {rel}")

core = SCRIPT.read_text(encoding="utf-8")
mcm = MCM.read_text(encoding="utf-8")
xml_root = ET.parse(XML).getroot()
strings = {node.attrib.get("id") for node in xml_root.findall("string")}
check("ui_mcm_menu_composure_combat" in strings, "MCM menu localization missing")
check('local VERSION = "1.0.1"' in core, "release script version is not 1.0.1")

mcm_ids = set(re.findall(r'\{ id = "([a-zA-Z0-9_]+)"', mcm))
for setting in sorted(mcm_ids - {f"line{i}" for i in range(1, 10)}):
    check(f"ui_mcm_composure_combat_{setting}" in strings,
          f"missing localization for MCM setting {setting}")

for token in [
    'REQUIRED_FRAMEWORK_API = 2',
    'source_type = "combat"',
    'source_type = "combat_rebound"',
    'obj:is_stalker()',
    'npc:best_enemy()',
    'RegisterScriptCallback("npc_on_fighting_actor"',
    'RegisterScriptCallback("actor_on_hit_callback"',
    'RegisterScriptCallback("bullet_on_update"',
    'RegisterScriptCallback("bullet_on_impact"',
    'RegisterScriptCallback("bullet_on_remove"',
    'instant_fraction = 0.30',
    'instant_cap_1s = 5.0',
    'instant_cap_3s = 7.5',
    'maximum_continuous_rate = 0.30',
    'deferred_queue',
    'danger_remaining_ms',
    'cooldown_remaining_ms',
    'set_recovery_lock',
    'register_listener',
    'encounter_combat_loss',
    'bypass_policies = true',
    'and before > 0',
    'debug_key = cfg("debug_key"',
    'test_mode',
    'COMBAT STRESS TEST',
    'forced_remaining_ms',
    'near_miss_stage = near_miss_stage',
]:
    check(token in core, f"core missing required token: {token}")

for phase, rate in (("alert", "0.10"), ("engaged", "0.20"), ("overwhelmed", "0.30")):
    check(re.search(rf'{phase}\s*=\s*{re.escape(rate)}', core) is not None,
          f"missing default {phase} rate {rate}")

for event in [
    "combat.started", "combat.resumed", "combat.near_miss",
    "combat.actor_hit", "combat.intensity_changed", "combat.overwhelmed",
    "combat.ended", "combat.rebound", "combat.completed",
]:
    # Event-specific ones can be constructed as "combat." .. event_name.
    if event in {"combat.near_miss", "combat.actor_hit"}:
        check('emit("combat." .. event_name' in core, "dynamic combat event publication missing")
    else:
        check(f'"{event}"' in core, f"missing event {event}")

for forbidden in ["goto ", "::", "//", "<const>", "table.unpack"]:
    check(forbidden not in core + mcm, f"Lua 5.1-incompatible token found: {forbidden}")

texlua = shutil.which("texlua")
if texlua:
    with tempfile.NamedTemporaryFile("w", suffix=".lua", delete=False) as loader:
        loader.write(f'assert(loadfile("{SCRIPT.as_posix()}"))\n')
        loader.write(f'assert(loadfile("{MCM.as_posix()}"))\n')
        loader.write('print("Lua parse OK")\n')
        loader_path = loader.name
    result = subprocess.run([texlua, loader_path], capture_output=True, text=True)
    Path(loader_path).unlink(missing_ok=True)
    check(result.returncode == 0, f"Lua parser failed: {result.stderr or result.stdout}")

if errors:
    print(f"FAILED: {len(errors)} of {checks} checks")
    for error in errors:
        print(" -", error)
    sys.exit(1)
print(f"PASS: {checks}/{checks} static checks")
