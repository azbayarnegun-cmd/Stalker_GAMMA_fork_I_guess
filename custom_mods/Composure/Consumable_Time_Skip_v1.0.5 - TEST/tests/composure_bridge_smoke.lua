local modifiers = {
    gain = { id = "gain", owner = "test", rate = 0.1, lane = "slow", enabled = true, remaining_ms = 120000 },
    loss = { id = "loss", owner = "test", rate = -0.1, lane = "slow", enabled = true, remaining_ms = 60000 },
}
local locks = {
    lock = { id = "lock", owner = "test", enabled = true, remaining_ms = 30000 },
}
local value = 50

local function rows(source)
    local out = {}
    for _, entry in pairs(source) do out[#out + 1] = entry end
    return out
end

composure_framework = {}
function composure_framework.get_snapshot()
    return { modifiers = rows(modifiers), caps = {}, recovery_locks = rows(locks) }
end
function composure_framework.get_value() return value end
function composure_framework.apply_delta(_, amount, opts)
    if amount > 0 and next(locks) and not opts.bypass_recovery_lock then return 0 end
    value = value + amount
    return amount
end
function composure_framework.remove_modifier(id) modifiers[id] = nil end
function composure_framework.upsert_modifier(id, rate, opts)
    modifiers[id] = {
        id = id, owner = opts.owner, rate = rate, lane = opts.lane,
        enabled = opts.enabled, remaining_ms = opts.duration * 1000,
    }
end
function composure_framework.remove_cap() end
function composure_framework.set_cap() end
function composure_framework.clear_recovery_lock(id) locks[id] = nil end
function composure_framework.set_recovery_lock(id, duration, opts)
    locks[id] = { id = id, owner = opts.owner, enabled = opts.enabled, remaining_ms = duration * 1000 }
end

local bridge = {}
setmetatable(bridge, { __index = _G })
assert(loadfile("gamedata/scripts/consumable_time_skip_composure.script", "t", bridge))()
consumable_time_skip_composure = bridge
assert(consumable_time_skip_composure.advance(3) == true)
assert(math.abs(value - 53) < 0.0001, "unexpected simulated modifier value: " .. tostring(value))
assert(next(modifiers) == nil, "timed modifiers did not expire")
assert(next(locks) == nil, "recovery lock did not expire")
print("PASS: Composure bridge smoke test")
