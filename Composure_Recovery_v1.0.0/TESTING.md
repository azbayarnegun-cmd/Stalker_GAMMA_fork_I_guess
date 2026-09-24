# Composure Recovery v1.0.0 test plan

## Automated check

Run:

```text
python3 tests/static_qa.py
```

## In-game smoke test

1. Install Core v2.1.0, Recovery v1.0.0 and HUD v3.1.0.
2. Ensure old Composure Main v1 is disabled.
3. Set Composure below 65 with the HUD tester.
4. Wait 15 seconds without damage, firing or combat.
5. Confirm recovery begins at approximately +1.2 points per minute.
6. Press F9; confirm the state reports `recovering`.
7. Fire once; confirm recovery stops immediately and the delay returns to 15 seconds.
8. Take damage; confirm the same reset behavior.
9. Enter combat with a human and a mutant separately; confirm both block recovery within 100 metres.
10. Apply a Framework recovery lock; confirm recovery stops and waits 15 seconds after the lock expires.
11. Set Composure to 64.95; confirm recovery settles at approximately 65 without a meaningful overshoot.
12. Set Composure to 0; confirm passive recovery does not revive the actor.
13. Save/load and change levels while recovering; confirm the source is removed and the safety delay restarts.

## MCM test

1. Change rate, target and delay; confirm each applies without restarting the game.
2. Disable combat detection and confirm only hits, firing and Framework locks stop recovery.
3. Disable the addon and confirm `recovery.safe_passive` disappears.
4. Re-enable it and confirm recovery returns only after the configured delay.

## Exit criteria

- No script errors on new game, load, death/reload or level change.
- No passive recovery during active human or mutant combat.
- No recovery through a Framework lock.
- No automatic recovery from Pass Out at zero.
- No duplicate recovery source when Core is used without Main.
