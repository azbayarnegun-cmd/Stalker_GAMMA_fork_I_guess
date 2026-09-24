-- Standalone Lua 5.1 exercise for the pure Weapon Stability module.

local clock = 1000
function time_global() return clock end

dofile("gamedata/scripts/composure_weapon_stability.script")

local config = {
    start_composure = 69,
    overall_strength = 1,
    max_stability_loss = 0.55,
    burst_recovery = 0.35,
    enable_dynamic_stability = true,
    sprint_penalty = 0.45,
    moving_penalty = 0.18,
    crouch_bonus = 0.12,
    stationary_bonus = 0.08,
    stability_recovery = 0.55,
    enable_shot_accumulation = true,
    instability_per_shot = 0.08,
    automatic_extra = 0.04,
    preserve_first_shot = true,
}

local still = {
    moving = false, sprinting = false, crouched = false,
    airborne = false, landing = false,
}
local sprint = {
    moving = true, sprinting = true, crouched = false,
    airborne = false, landing = false,
}

local high = update(100, still, 0.1, config)
assert(high.severity == 0 and high.ceiling == 1)

reset()
local low = update(25, still, 0.1, config)
local before = low.current
for _ = 1, 4 do
    on_shot(config)
    clock = clock + 100
end
local fired = update(25, still, 0.1, config)
assert(fired.shot_load > 0 and fired.current < before)

reset()
local moved = update(25, sprint, 0.1, config)
assert(moved.movement_load == config.sprint_penalty)

set_disturbance("test", 0.25, { owner = "qa", ttl = 0.5 })
local disturbed = update(25, still, 0.1, config)
assert(disturbed.disturbance_load > 0.24)
clock = clock + 600
local expired = update(25, still, 0.1, config)
assert(expired.disturbance_load == 0)

print("Stability runtime harness: OK")
