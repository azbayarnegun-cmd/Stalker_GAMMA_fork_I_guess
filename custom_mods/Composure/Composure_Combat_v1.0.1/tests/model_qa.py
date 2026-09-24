#!/usr/bin/env python3
"""Deterministic balance-model checks for Combat v1 defaults."""
import sys

errors = []
checks = 0


def check(condition, message):
    global checks
    checks += 1
    if not condition:
        errors.append(message)


INSTANT_FRACTION = 0.30
CAP_1S = 5.0
CAP_3S = 7.5
CONTINUOUS_CAP = 0.30


def split(raw, budget=999):
    instant = min(raw * INSTANT_FRACTION, budget)
    return instant, raw - instant


for raw, expected in [
    (1.0, (0.30, 0.70)),
    (1.5, (0.45, 1.05)),
    (2.5, (0.75, 1.75)),
    (3.5, (1.05, 2.45)),
    (5.0, (1.50, 3.50)),
]:
    actual = split(raw)
    check(abs(actual[0] - expected[0]) < 1e-9, f"instant split failed for {raw}")
    check(abs(actual[1] - expected[1]) < 1e-9, f"deferred split failed for {raw}")
    check(abs(sum(actual) - raw) < 1e-9, f"split must conserve raw stress for {raw}")

# If the instant budget is exhausted, the blocked instant part becomes deferred.
instant, deferred = split(5.0, budget=0.25)
check(abs(instant - 0.25) < 1e-9, "instant rolling budget not honored")
check(abs(deferred - 4.75) < 1e-9, "capped instant stress must move to deferred")
check(abs(instant + deferred - 5.0) < 1e-9, "capped split must conserve raw stress")

# Rolling-window example: four rapid 5-point events request 1.5 each.
requests = [1.5, 1.5, 1.5, 1.5]
used_1s = 0
used_3s = 0
applied = []
for request in requests:
    budget = max(0, min(CAP_1S - used_1s, CAP_3S - used_3s))
    value = min(request, budget)
    applied.append(value)
    used_1s += value
    used_3s += value
check(sum(applied) <= CAP_1S + 1e-9, "one-second cap exceeded")
check(sum(applied) <= CAP_3S + 1e-9, "three-second cap exceeded")
check(abs(sum(applied) - 5.0) < 1e-9, "rapid-event cap should stop at exactly five")

# Continuous capacity is shared: sustained pressure gets first claim and
# deferred pressure uses only the remainder.
for sustained, deferred_request, expected in [
    (0.10, 0.20, 0.30),
    (0.20, 0.20, 0.30),
    (0.30, 0.20, 0.30),
    (0.00, 0.50, 0.30),
]:
    deferred_used = min(deferred_request, max(0, CONTINUOUS_CAP - sustained))
    total = sustained + deferred_used
    check(abs(total - expected) < 1e-9, f"continuous sharing failed for {sustained}/{deferred_request}")
    check(total <= CONTINUOUS_CAP + 1e-9, "continuous cap exceeded")

# Rebound is bounded by actual combat loss, percentage, configured maximum and
# room below the encounter start. It never refunds unrelated losses.
def rebound(actual_combat_loss, percentage, maximum, start, current):
    return min(actual_combat_loss * percentage, maximum, max(0, start - current))


check(rebound(10, 1.0, 30, 65, 50) == 10, "full rebound should restore actual combat loss")
check(rebound(40, 1.0, 30, 65, 10) == 30, "rebound maximum not enforced")
check(rebound(20, 1.0, 30, 65, 60) == 5, "rebound must not exceed encounter start")
check(rebound(10, 0.5, 30, 65, 40) == 5, "rebound percentage not enforced")
check(rebound(10, 1.0, 30, 65, 70) == 0, "rebound must not apply above encounter start")

if errors:
    print(f"FAILED: {len(errors)} of {checks} checks")
    for error in errors:
        print(" -", error)
    sys.exit(1)
print(f"PASS: {checks}/{checks} model checks")
