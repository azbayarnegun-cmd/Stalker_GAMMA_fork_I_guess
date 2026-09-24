SA Equipment Balance v1.0.4

Optional economy and inventory-balance package. Requires SA Rigs, Belts &
Pouches v1.0.0 and loads after it.

INCLUDED
  corrected pouch and belt progression based on rigs balance.xlsx
  chest-rig values that exceed their required pouch inputs
  family-specific progressive recipes for pouches, belts and all 16 rigs
  construction-only medical-pouch recipes: no bandages, medkits or syringes
  reinforced Canister recipes using fabric, fasteners and plastic
  completed pouch/belt distribution across the 25 Layered Pouches traders
  stash/tier distribution for rig pouches and chest rigs
  global non-stack policy and one-item-per-cell Food Containers

Higher-tier recipes consume their immediately previous tier. The original item
section IDs remain available for save compatibility. The legacy base belt is
withdrawn from traders but not deleted.

V1.0.1 BALANCE CORRECTIONS
  Y3 Twin Magazine Pouch: 20,000 RU
  Y5 Drum Pouch: 32,500 RU, above the consumed Y4 pouch
  Parts Pouch no longer consumes a Small Universal Pouch; it is a separate
  specialist product rather than a capacity upgrade
  chest rigs: 30,000-135,000 RU, leaving value for harness materials after
  their required built-in pouch components are consumed

V1.0.2 CRAFT REGISTRATION FIX
  consolidates all pouch, belt, chest-rig and canister recipes into one
  canonical late-loading craft patch
  loads after ordinary craft-table patches to prevent the SA recipes being
  removed by a later section edit
  adds a one-time [SA-CRAFT-DIAG] startup report for resolved recipe presence

V1.0.3 COMPLETE RECIPE PROGRESSION
  assigns every one of the 55 active outputs to an explicit manual tier
  Basic I: 10 small/T1 starter recipes
  Basic II: 11 medium/T2 upgrade recipes
  Advanced I: 10 large/T3 or first specialist recipes
  Advanced II: 24 top-tier pouches, belts and component-dependent chest rigs
  keeps retired Magazine Pouch T3 and legacy Canister aliases hidden for save
  compatibility instead of exposing duplicate products
  expands [SA-CRAFT-DIAG] from representative checks to all 55 recipe outputs
  corrects diagnostic summary formatting

V1.0.4 WORKSHOP COMPATIBILITY FIX
  limits every recipe to three or four ingredient types, matching GAMMA's
  workshop_autoinject requirement of 6, 8 or 10 recipe tokens
  fixes Medical T1 and Sustainment T1 being silently omitted from the UI
  fixes the same omission across 42 affected upgrades, belts, pouches and rigs
  preserves all 55 outputs, manual tiers and progressive previous-tier inputs
  adds runtime UI-compatibility counts to [SA-CRAFT-DIAG]

Replace v1.0.0/v1.0.1/v1.0.2/v1.0.3 with v1.0.4. Do not enable multiple versions.
v1.0.4 Workshop-Compatible Recipes

Adds crafting and trader integration for the two strict utility pouches in
20_SA_Rigs_Belts_Pouches_v1.0.1_Utility_Pouches. T1 costs 5,000 RU and uses
Basic I; T2 costs 10,000 RU, uses Basic II and upgrades from T1.
