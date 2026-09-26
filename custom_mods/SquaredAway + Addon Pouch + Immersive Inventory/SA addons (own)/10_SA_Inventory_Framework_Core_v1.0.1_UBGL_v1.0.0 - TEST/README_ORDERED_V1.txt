10_SA_Inventory_Framework_Core_v1.0.1_UBGL_v1.0.0

Load first in the SA ordered V1 stack.

Minimal test branch based directly on v1.0.1 STABLE.

Only two functional changes:
- The existing shotgun reload permission bridge reads grenade_class while an
  attached launcher is active.
- AmmoCheck One-Key consults that bridge immediately before starting an
  underbarrel reload.

Result: VOG-25 and M203/M209 ammunition in general inventory cannot authorize
a reload. A matching round must be inside a yellow reload pocket.

Changes from v1.0.0:
- Fixes rig unequip/equip magazine rebuild path so loaded magazines keep their magazine_binder round data.
- Keeps the merged rotate event hotfix from V1 stable.

Recommended order:
10_SA_Inventory_Framework_Core_v1.0.1_UBGL_v1.0.0
20_SA_Rigs_Belts_Pouches_v1.0.0
30_SA_Equipment_Balance_v1.0.0
40_SA_Combat_Access_QuickWheel_v1.0.0
50_SA_Immersive_Inventory_Access_v1.0.1
