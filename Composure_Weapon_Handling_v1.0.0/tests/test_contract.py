#!/usr/bin/env python3
"""Static and numerical contract checks for Weapon Handling v1."""

from pathlib import Path
import math
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "gamedata" / "scripts"
CORE = (SCRIPTS / "composure_weapon_core.script").read_text(encoding="utf-8")
STABILITY = (SCRIPTS / "composure_weapon_stability.script").read_text(encoding="utf-8")
RECOIL = (SCRIPTS / "composure_weapon_recoil.script").read_text(encoding="utf-8")
SWAY = (SCRIPTS / "composure_weapon_sway.script").read_text(encoding="utf-8")
MCM = (SCRIPTS / "composure_weapon_mcm.script").read_text(encoding="utf-8")


def smoothstep(value: float) -> float:
    value = min(1.0, max(0.0, value))
    return value * value * (3 - 2 * value)


def severity(composure: float, start: float = 69) -> float:
    return smoothstep((start + 1 - composure) / start)


class WeaponContract(unittest.TestCase):
    def test_six_named_modules_exist(self):
        expected = {
            "composure_weapon_core.script",
            "composure_weapon_stability.script",
            "composure_weapon_recoil.script",
            "composure_weapon_movement.script",
            "composure_weapon_sway.script",
            "composure_weapon_mcm.script",
        }
        self.assertEqual(expected, {path.name for path in SCRIPTS.glob("*.script")})

    def test_no_retired_breathing_or_feedback_code(self):
        names = {path.name for path in SCRIPTS.glob("*.script")}
        self.assertFalse(any("breath" in name or "audio" in name or "visual" in name for name in names))

    def test_framework_is_read_only(self):
        self.assertIn("composure_framework.get_snapshot", CORE)
        all_text = "\n".join(path.read_text(encoding="utf-8") for path in SCRIPTS.glob("*.script"))
        for forbidden in (
            "composure_manager",
            "composure_framework.adjust",
            "composure_framework.set_value",
            "composure_framework.register_modifier",
            "composure_framework.register_cap",
            "composure_framework.register_recovery_lock",
        ):
            self.assertNotIn(forbidden, all_text)

    def test_ballistics_are_never_written(self):
        all_text = "\n".join(path.read_text(encoding="utf-8") for path in SCRIPTS.glob("*.script"))
        for forbidden in (
            "SetFireDispersion", "Set_PDM_", "SetFirstBulletDisp", "SetHitPower",
            "SetHitImpulse", "SetFireDistance", "SetRPM", "SetRealRPM",
        ):
            self.assertNotIn(forbidden, all_text)

    def test_no_forced_camera_or_input(self):
        all_text = "\n".join(path.read_text(encoding="utf-8") for path in SCRIPTS.glob("*.script"))
        for forbidden in (
            "add_cam_effector", "set_actor_direction", "disable_input", "only_allow_movekeys",
        ):
            self.assertNotIn(forbidden, all_text)

    def test_effect_starts_at_69_and_zero_is_disabled(self):
        self.assertIn("start_composure = 69", MCM)
        self.assertEqual(severity(70), 0)
        self.assertGreater(severity(69), 0)
        self.assertTrue(all(a <= b for a, b in zip(
            [severity(v) for v in (69, 60, 50, 40, 16, 1)],
            [severity(v) for v in (60, 50, 40, 16, 1, 0)],
        )))
        self.assertIn("value > 0", CORE)

    def test_native_setters_have_matching_getters(self):
        pairs = re.findall(r'getter = "([A-Za-z0-9_]+)", setter = "([A-Za-z0-9_]+)"', RECOIL)
        self.assertGreaterEqual(len(pairs), 10)
        for getter, setter in pairs:
            self.assertTrue(getter.startswith("Get"))
            self.assertTrue(setter.startswith("Set"))
        self.assertNotIn("SetCrosshairInertion", RECOIL)

    def test_targets_derive_from_baseline(self):
        self.assertIn("for key, value in pairs(baseline)", RECOIL)
        self.assertIn("baseline.cam_disp * recoil_mult", RECOIL)
        self.assertIn("baseline.cam_relax * recovery_mult", RECOIL)
        self.assertNotRegex(RECOIL, re.compile(r"last_targets\.[a-z_]+\s*\*"))

    def test_cleanup_restores_baseline(self):
        self.assertIn("local function restore()", RECOIL)
        self.assertIn("baseline[field.key]", RECOIL)
        for callback in ("on_option_change", "on_level_changing", "actor_on_net_destroy"):
            self.assertIn(f'RegisterScriptCallback("{callback}"', CORE)

    def test_dynamic_inputs_and_counterplay_exist(self):
        movement = (SCRIPTS / "composure_weapon_movement.script").read_text(encoding="utf-8")
        for state in ("mcSprint", "mcCrouch", "mcAccel"):
            self.assertIn(state, movement)
        for term in ("shot_load", "crouch_bonus", "stationary_bonus", "movement_load"):
            self.assertIn(term, STABILITY)

    def test_shot_accumulation_uses_fired_callback(self):
        self.assertIn('RegisterScriptCallback("actor_on_weapon_fired"', CORE)
        self.assertIn("function on_shot(config)", STABILITY)
        self.assertIn("automatic_extra", STABILITY)
        self.assertIn("preserve_first_shot", STABILITY)

    def test_sway_is_adapter_only(self):
        self.assertIn("function register_adapter", SWAY)
        self.assertIn("native_sway = false", SWAY)
        self.assertNotIn("SetFireDispersion", SWAY)
        self.assertNotIn("add_cam_effector", SWAY)

    def test_external_disturbance_event(self):
        self.assertIn("composure_weapon.disturbance", CORE)
        self.assertIn("function set_disturbance", STABILITY)
        self.assertIn("function clear_owner", STABILITY)

    def test_preview_is_local_and_diagnostic_is_configurable(self):
        self.assertIn('preview_enabled = cfg("preview_enabled", false)', CORE)
        self.assertIn("config.preview_enabled and config.preview_composure or source_value", CORE)
        self.assertIn('preview_enabled = false', MCM)
        self.assertIn('preview_composure = 25', MCM)
        self.assertIn('diagnostic_key = KEY_F11', MCM)
        self.assertIn('RegisterScriptCallback("on_key_press"', CORE)

    def test_mcm_ranges_are_playable(self):
        self.assertIn("max = 0.75", MCM)
        self.assertIn("max = 0.60", MCM)
        self.assertIn("max = 0.80", MCM)
        self.assertNotIn("max = 2.0", MCM)

    def test_localization_covers_mcm_options(self):
        xml = (ROOT / "gamedata" / "configs" / "text" / "eng" / "composure_weapon.xml").read_text(encoding="utf-8")
        option_ids = re.findall(r'{ id = "([a-z0-9_]+)"', MCM)
        for option_id in option_ids:
            if option_id.startswith("line"):
                continue
            self.assertIn(f"ui_mcm_composure_weapon_{option_id}", xml)

    def test_default_ceiling_is_bounded(self):
        for value in range(0, 101):
            ceiling = max(0.15, min(1.0, 1 - severity(value) * 0.55))
            self.assertTrue(math.isfinite(ceiling))
            self.assertGreaterEqual(ceiling, 0.15)
            self.assertLessEqual(ceiling, 1.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
