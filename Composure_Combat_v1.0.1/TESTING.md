# Composure Combat v1.0.1 — in-game test plan

Use a disposable save with Composure Core v2.1.0. For exact readings, enable
the Composure HUD live display and Combat diagnostic logging.

## Controlled F6 tests

1. Open MCM > Composure Combat.
2. Enable Test Mode.
3. Select `Simulate 10% human hit`, press F6 and confirm:
   - Raw stress is 1.5.
   - About 0.45 is requested instantly.
   - About 1.05 enters the deferred queue.
4. Select `Simulate normal near miss`; the first raw value should be 0.45.
5. Repeat it quickly; raw values should diminish to 0.30 and 0.15.
6. Wait three seconds per step and confirm the near-miss stage recovers.

## Phase tests

Force each phase for fifteen seconds:

| F6 action | Expected default rate after 2 s grace |
|---|---:|
| Force Alert | -0.10/s |
| Force Engaged | -0.20/s |
| Force Overwhelmed | -0.30/s |

F6 status must identify the selected phase. No single forced phase may exceed
the configured continuous cap.

## Cap test

Rapidly simulate several large hits. Confirm:

- Raw instant requests never exceed 5 inside one rolling second.
- Raw instant requests never exceed 7.5 inside three rolling seconds.
- Excess instant stress moves to the deferred total.
- Sustained plus deferred pressure never exceeds 0.30/s by default.

## Real human firefight

1. Enter combat with one human NPC. Confirm Alert starts and recovery locks.
2. Add more human attackers. Confirm Engaged then Overwhelmed can occur.
3. Let hostile bullets pass close without hitting. Confirm near-miss events.
4. Take human gunfire damage. Confirm the health-loss band is recorded.
5. Confirm actor-fired and unrelated bullets produce no near-miss stress.

## Exclusion tests

The following must not create Combat hit stress:

- Mutant attacks.
- Radiation ticks.
- Anomaly damage.
- Falling damage.
- Hunger/thirst/condition damage.
- Self damage.

Mutants entering a human fight remain ignored by v1; the human encounter
continues normally.

## Consumables source protection

1. Use a drug providing `combat` loss resistance.
2. Simulate a hit and compare Core's actual applied loss against the raw value.
3. Confirm the matching percentage reduces both instant and continuous Combat loss.
4. Confirm radiation-only protection does not reduce Combat loss.

## Rebound test

1. Note the encounter starting Composure.
2. Accumulate only Combat-generated loss.
3. Select `End current encounter` or safely leave combat.
4. Remain safe through the rebound delay.
5. Confirm rebound restores recorded actual Combat loss without exceeding:
   - The encounter starting value.
   - The configured rebound percentage.
   - The configured maximum rebound.
6. Add a non-combat loss during the encounter and verify it is not refunded.
7. Set Composure to zero before resolution and verify rebound does not revive the actor.

## Save/load

1. Save with an active encounter and deferred pressure.
2. Reload and press F6.
3. Confirm start value, actual Combat loss, deferred total and cooldown persist.
4. Save during rebound cooldown and confirm its remaining delay resumes.

## Logs

Search `appdata/logs/xray_*.log` for:

```text
[composure_combat:v1]
SCRIPT ERROR
stack trace
```

No repeated missing-Core warnings, callback errors or modifier ownership errors
should occur.
