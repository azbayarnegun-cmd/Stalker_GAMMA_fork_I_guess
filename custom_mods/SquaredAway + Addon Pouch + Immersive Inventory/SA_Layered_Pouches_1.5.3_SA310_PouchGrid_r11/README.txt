SA Layered Pouches Addon 1.5.3 - SquaredAway 3.1.0 video-confirmed patch r9

REQUIRES:
  SquaredAway 3.1.0-test
  Quick Action Wheel - HarukaSai (for the Add to QAW integration)

INSTALL:
  Load this addon AFTER SquaredAway 3.1.0-test, Quick Action Wheel and
  G.A.M.M.A. Quick Action Wheel Balance.
  Disable the previous Layered Pouches build and its separate rig/QAW hotfixes.

PORT NOTES:
- Rebased the Layered Pouches integration onto SquaredAway 3.1.0-test.
- Preserves SquaredAway 3.1.0 ZoneGrid/rig changes instead of replacing them with the old 2.25 core.
- Restores fitted pouch zones, detached side view, pouch ownership routing, cross-view drag/drop, Layered capacity/stack bridges, and AMP attachment-panel hooks.
- Keeps the 3.1.0 transient inventory/deferred-display safety paths.
- This patch preserves Layered Pouches 1.5.3 content while rebasing its integration scripts on SquaredAway 3.1.0-test.
- Includes the multi-pouch rendering and safe right-click Use fixes from the tested 3.1.0 port.
- Loot and autoloot now remain in the backpack; pouch filling is manual.
- Restores persistent Add to Quick Action Wheel for worn-rig and fitted-pouch items.
- Adds stock GAMMA Use to items stored in worn-rig pockets.
- Ordinary backpack cargo is not eligible for manual Add to Quick Action Wheel.
- r3 makes backpack-to-pouch drops use the measured pouch grid instead of the
  unreliable decorative-window hover owner.
- r3 keeps Add to QAW available when the selected wheel tab is dynamic or full
  by choosing the next compatible regular tab.
- r3 removes the harmless double-release engine errors seen while stripping a rig.
- r4 teaches QAW's injected custom action about the real Layered side-container id.
- r4 extends SquaredAway's meds-wheel pocket filter to fitted Layered pouches,
  preventing the wheel from becoming empty after moving medicine out of the rig.
- r5 catches backpack-to-pouch and pouch-to-backpack transfers on Sota's early
  mouse release, before its stale-hover check can suppress On_CC_DragDrop.
- r5 avoids unsupported UIInfoItem equality comparisons in rig tooltips.
- r6 gives a confirmed fitted-pouch grid cell priority over AMP's broad docked
  panel background, preventing valid storage drops from becoming attachment attempts.
- r6 restores the native side-container hit test with measured geometry as fallback.
- r7 blocks Sota UI's underlying trash/drop-outside action across the entire
  fitted-pouch column. Invalid items stay in their source container instead of
  falling into the world. Occupied pouch cells now use the same side hit test.
- r9 restores the geometry-aware release path removed by the r8 diagnostic
  rollback. Video evidence confirmed that the decorative pouch panel owns the
  cursor while its underlying cell container reports false; the measured
  visible storage rectangle is therefore authoritative for pouch drops.
- Test on a backup save first.

EXPECTED LOGS:
  [GRID] version 0.65.0-test+Layered-1.5.3-r7-for-SA3.1.0 loading
  [AMP] version 3.1.0-test+Layered-1.5.3-port-r7 loading
  [AMP-LAYERS] version 1.5.3-port-r7 for SquaredAway 3.1.0-test ready
