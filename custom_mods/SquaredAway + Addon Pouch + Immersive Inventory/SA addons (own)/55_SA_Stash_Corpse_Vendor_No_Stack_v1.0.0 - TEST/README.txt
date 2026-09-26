SA Stash, Corpse & Vendor No-Stack v1.0.0
=========================================

Standalone load-after compatibility override for:
  10_SA_Inventory_Framework_Core_v1.0.1 - STABLE

Stashes, corpses and vendor/trade lists now obey the same stack ceilings as
the player's Squared Away inventory. The active values still come from:
  gamedata/configs/items/settings/zzz_grid_stacks.ltx

Ordinary items therefore default to one object per square. Existing configured
exceptions remain unchanged, including bolts, ammunition boxes, letters,
injections and cigars.

External lists keep their normal dimensions, scrolling and automatic packing.
They do not receive the player's equipment zones, backpack capacity limit,
rotation layout, saved hand placement or overflow/drop logic.

Install this as its own mod and load it after Core, Rigs, Balance, QuickWheel
and Immersive Access. It intentionally overrides only zzz_amp_grid.script and
is tied to the stable Core v1.0.1 script baseline. Do not combine it with an
experimental Core grid-script replacement.
