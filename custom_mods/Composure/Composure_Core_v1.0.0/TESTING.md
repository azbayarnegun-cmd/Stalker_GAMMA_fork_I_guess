# Composure Core v2.1.0 test plan

## Automated QA

Run:

```text
python3 tests/static_qa.py
```

## Clean-upgrade smoke test

1. Disable Composure Framework v2 and Composure Main v1.
2. Enable Core v2.1.0 in their place, before all consumer modules.
3. Load an existing save and confirm the saved Composure value is unchanged.
4. Confirm the log contains `v2.1.0 API 2 initialized` and no script error.
5. Call `composure_framework.debug_dump()` from a temporary console/test hook.
6. Confirm the snapshot reports the correct value and canonical tier.
7. With no gameplay modules active, wait at least two minutes. The value must not change.
8. Apply `-5` with `apply_instant`; confirm the actual change is exactly `-5` unless clamped at zero.
9. Apply `+5`; confirm the actual change is exactly `+5` unless clamped at 100, blocked by a recovery lock, or limited by a cap.
10. Confirm existing HUD, Audio, Heartbeat and Visuals still read the snapshot.

## Save and scheduler tests

1. Save during a persistent timed modifier and reload.
2. Confirm its remaining time is restored without a large catch-up tick.
3. Confirm non-persistent condition leases do not return after reload.
4. Change levels with fast and slow modifiers active; confirm no drain/recovery spike.
5. Load a legacy save containing `composure_mvp = 80`; confirm migration to approximately 66.67 and no second migration on the next load.

## Release exit criteria

- No `composure_main.script` or `composure_main_mcm.script` in the package.
- No built-in adjustment policy or passive recovery source.
- Direct positive and negative deltas apply without hidden scaling.
- Existing Framework v2 save identity and API 2 compatibility are preserved.
- No engine errors across new game, load, death/reload and level change.
