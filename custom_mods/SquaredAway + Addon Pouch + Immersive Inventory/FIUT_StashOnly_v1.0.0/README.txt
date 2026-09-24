FIUT Stash Only v1.0.0 - scoped adaptation of uploaded FIUT

Disable the original FIUT package. Install this standalone replacement
below Sorting Plus, Seamless Inventory Sort, UI mods and SquaredAway in MO2.
Keep your shotgun fix and dump-pouch fix enabled. Restart the game.
Do not run both FIUT packages together: the original's extra scripts would
still affect personal inventory. No sortingplus.ltx replacement is included.

Open a world/workbench stash and select the existing category/kind sort
mode. Headers label the categories, show weight totals, and support collapse.
This version uses your existing Sorting Plus category order. It does not
force sort mode or reorder the player-side panel. No draggable pairing panel,
personal item rules, global category-order editor or magazine cleanup script.
Backpack, equipment, rigs, pouches, corpses and trade panels are excluded.
Unknown container contexts fail closed (no FIUT processing).

Scope check uses Anomaly's npc_bag + loot mode + npc_is_box == true.
Special mod containers without that standard stash context are not supported.
Header/tint controls are allocated only for the shared external-container
panel; corpses bypass processing and reset clears any old stash decorations.
Existing FIUT cosmetics saved in MCM may still be read; no full FIUT MCM
panel is shipped. Default appearance applies when those settings are absent.

Sorting/header layout work runs only while viewing an eligible stash. Existing
FIUT signature caching and throttled change checks are retained. Large stashes
can still pause during layout rebuilds; no measured FPS claim is made.

Test on a backup save: open stash, choose kind/category sort, transfer items,
collapse/reopen sections, close then open corpse/trader/inventory. Confirm
player backpack/rig/pouch layout is unchanged. Test a large stash and reopen.
Verified: script compiles; source scope tests exclude player panels, corpses,
trade and unknown context; no executable global MCM writes. Engine/UI tests
are still needed. If headers are absent, send log and a stash screenshot.
