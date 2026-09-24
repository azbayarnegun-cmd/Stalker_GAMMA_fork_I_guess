SA Rig Pocket Rebalance v1.1.0 TEST
===================================

LOAD ORDER
----------
Load after:
  20_SA_Rigs_Belts_Pouches
  30_SA_Equipment_Balance

This replaces 90_SA_Rig_Pocket_Rebalance v1.0.0. Do not enable both.

WHAT IT CHANGES
---------------
- Rebalances all 16 chest rigs into four built-in-pocket tiers.
- Every rig retains the two addon-pouch fittings supplied by Module 20.
- Adds red medical-pocket variants, with a maximum of two red pockets.
- Keeps Tarzan-M22 as the only drum-pocket rig.
- Replaces all 16 rig recipes so their ingredients match their visible pockets.
- Moves rig crafting through Basic I, Basic II, Advanced I and Advanced II.
- Makes compact and long magazine pouches parallel Basic-I variants.
- Moves the first red medical pouch recipe to Basic II.
- Uses the recommended 75% price table as the static base price.

MCM PRICE PRESETS
-----------------
Rig Rebalance -> Price preset
  Full price (100%)
  Balanced (75%) [default]
  Affordable (50%)

The item configuration uses Balanced 75% values. This makes trader affordability
checks and normal tooltip prices correct for the default setting. Full and
Affordable use actor_on_trade to correct the completed transaction amount.

IMPORTANT TEST LIMITATION
-------------------------
The 100% and 50% MCM choices alter the money transaction after the trade completes.
The trade window may continue to display the static 75% value. At 50%, the actor
must temporarily possess the displayed 75% amount before the refund is applied.

TEST
----
1. Fully restart the game.
2. Confirm these startup lines:
   [SA-RIG-RB] v1.1.0 TEST loaded; static price baseline=75%
   [SA-RIG-RB] trade correction registered
3. Open MCM -> Rig Rebalance and choose a preset.
4. Buy or sell one rig and close the trader.
5. Check the money change and send the log. A transaction line will show the
   section, callback sell flag, original transaction cost, preset and correction.

DISABLE / ROLLBACK
------------------
Disable this addon to restore Module 20/30 layouts, recipes and prices.

