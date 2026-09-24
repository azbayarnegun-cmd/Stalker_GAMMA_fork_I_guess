from pathlib import Path
import re
import sys
import zipfile

root = Path(__file__).resolve().parents[1]
script = (root / "gamedata/scripts/composure_exploration.script").read_text(encoding="utf-8")
mcm = (root / "gamedata/scripts/composure_exploration_mcm.script").read_text(encoding="utf-8")
xml = (root / "gamedata/configs/text/eng/composure_exploration.xml").read_text(encoding="utf-8")

checks = []
def check(name, condition):
    checks.append((name, bool(condition)))

for token in (
    'supports(2)', 'apply_delta("exploration.tick"', 'set_recovery_lock',
    'clear_recovery_lock', 'register_adjustment_policy', 'transition_composure_scale',
    'transition_exposure_scale', 'exposure_minutes', 'campfire_relief_used',
    'function reduce_exposure', 'function set_anomaly_distance',
    'RegisterScriptCallback("save_state"', 'RegisterScriptCallback("load_state"',
    'RegisterScriptCallback("actor_on_sleep"', 'surface_outdoor',
    'local VERSION = "1.0.1"', 'current_game_stamp', 'last_game_stamp',
    'valid_time_samples', 'lifecycle_state', 'arrival_grace', 'clock_wait',
    'clock watchdog cleared stale recovery lock', 'prepare_level_change',
    'deactivate_lifecycle', 'recovery_lock_active',
): check("script token: " + token, token in script)

defaults = {
    "surface_outdoor_rate": "0.25",
    "underground_rate": "0.75",
    "deep_lab_rate": "1.50",
    "maximum_loss_per_minute": "5.00",
    "exploration_floor": "50",
    "companion_multiplier": "0.75",
    "anomaly_near_add": "0.25",
    "transition_composure_scale": "0.25",
    "transition_exposure_scale": "1.00",
    "campfire_relief_rate": "2.00",
    "campfire_max_relief_minutes": "60",
    "campfire_minimum_exposure": "60",
    "campfire_relief_reset_minutes": "120",
    "entry_grace_seconds": "5",
}
for key, value in defaults.items():
    check(f"MCM default {key}={value}", re.search(rf"{key}\s*=\s*{re.escape(value)}(?:\D|$)", mcm) is not None)

ids = re.findall(r'id\s*=\s*"([a-z0-9_]+)"', mcm)
for item_id in ids:
    if item_id.startswith("line") or item_id == "composure_exploration":
        continue
    check("localization: " + item_id, f'ui_mcm_composure_exploration_{item_id}' in xml)

check("no old profile name", "surface_day" not in script and "surface_day" not in mcm)
check("no retained CTime reference", "last_game_time" not in script)
check("grace clears lock", 'lifecycle_state == "arrival_grace"' in script and 'clear_runtime_lock()' in script)
check("level change callback", 'RegisterScriptCallback("on_before_level_changing", prepare_level_change)' in script)
check("no existing mod file overwrite", "simulated_time.script" not in [p.name for p in root.rglob("*") if p.is_file()])

failed = [name for name, passed in checks if not passed]
print(f"{len(checks) - len(failed)}/{len(checks)} checks passed")
if failed:
    for name in failed: print("FAIL:", name)
    sys.exit(1)
