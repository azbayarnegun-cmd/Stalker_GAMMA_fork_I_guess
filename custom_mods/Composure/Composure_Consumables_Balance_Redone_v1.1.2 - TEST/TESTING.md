# In-game smoke test

Use a disposable save and set the Consumables MCM Instant and Gradual scales to
1.00. Fully restart the game after installing or rebuilding the mod.

1. Spawn fresh Boar Chops C (`meat_boar`): 1 use, raw satiety `0.52`, cost 1034.
2. Spawn fresh raw Boar Chops (`mutant_part_boar_chop`): 1 use, raw satiety `0.16`.
3. Spawn a fresh Flask (`flask`): 4 uses and raw thirst `-2.00` per use.
4. Hover the items and confirm a separated `COMPOSURE EFFECTS` block appears.
   Rest must appear only once as GAMMA's native stat.
5. Confirm native Rest displays approximately: vodka -25%, coffee +15%, energy
   drink +10%, heavy meal -15%, light meal -5%, chocolate/protein +5%, and
   cigarettes +2.5% per use.
6. Confirm a cigarette gives +5 instant Composure and +5 over 30 seconds.
7. Check one other multi-use item and confirm its use counter matches the workbook.
8. Search the newest `xray_*.log` for `SCRIPT ERROR` and `stack trace`.

Existing partially used inventory objects may retain old condition/use state;
always use newly spawned or purchased items for max-use testing.
