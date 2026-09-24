SA Cloth-Heavy Equipment Recipes v1.0.1 TEST
================================================

PURPOSE
-------
Increases Basic Cloth use across rig addon pouches, detachable pouches,
Hunter/Sustainment pouches and belts. Canister T1 instead uses Fabric 2 x10.

LOAD ORDER
----------
Load after:
  20_SA_Rigs_Belts_Pouches
  30_SA_Equipment_Balance v1.0.4
  90_SA_Rig_Pocket_Rebalance v1.1.0 TEST

Module 70 Fabric Salvage is compatible and unchanged. It may load before this.

V1.0.1 FIX
----------
- Renamed the DLTX recipe file so it is parsed after Module 30 v1.0.4.
- Fixes Module 30 silently restoring its lower-cloth recipe values even when
  this addon is enabled and placed later in MO2.
- Adds an in-game startup diagnostic showing whether the final merged recipes
  contain this addon's expected cloth values.

SCOPE
-----
- Overrides 39 existing recipe keys.
- Does not add duplicate crafting outputs.
- Preserves existing Fabric 2/3/4 quantities except Canister T1 Fabric 2 x5 -> x10.
- Preserves previous-tier upgrade requirements.
- Every recipe uses no more than four ingredient types.
- Does not change item prices, traders, loot, salvage, pocket layouts or QAW behavior.

ROLLBACK
--------
Disable this addon to restore the recipes supplied by Modules 30 and 90.
