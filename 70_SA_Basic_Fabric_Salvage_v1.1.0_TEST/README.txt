SA Basic Fabric Salvage v1.1.0 TEST

PURPOSE
  Makes Basic Fabric (prt_o_fabrics_1) substantially more available without
  changing traders, stashes, loot tables, or higher fabric tiers.

CHANGES
  1. More eligible dismantles
     - Every outfit/armor, even if its original parts table has no Basic Fabric.
     - Every helmet/mask.
     - GAMMA/Anomaly backpacks.
     - Layered chest rigs, belts, and pouches from the SA equipment modules.
     - Other dismantlable items whose section names identify them as backpacks,
       chest rigs, pouches, belts, sleeping bags, or sleepbags.

  2. More potential Basic Fabric rolls
     - Helmet/mask: 1 total roll.
     - Light outfit below 12 kg: 2 total rolls.
     - Medium/heavy outfit at least 12 kg: 3 total rolls.
     - Small pouch/belt/sleeping bag: 1 total roll.
     - Backpack/chest rig: 2 total rolls.

     Existing Basic Fabric entries count toward those totals; the addon does
     not blindly duplicate an item's original fabric roll. Added rolls use the
     same GAMMA recovery chance: global disassembly chance + item condition.
     This means damaged gear can still return zero fabric.

  3. Basic Fabric conversion
     Right-click any faction patch in the actor inventory and select:
       Sew Basic Fabric (2 patches + 2 thread)

     Cost: any 2 faction patches + 2 sewing_thread
     Result: 1 prt_o_fabrics_1

     Mixed factions are accepted. A normal workshop recipe cannot express
     "any two faction patches," so this is an inventory right-click conversion
     rather than a row in the workshop recipe screen.

INSTALLATION / LOAD ORDER
  Install as a separate MO2 mod and load it late, after GAMMA's Part
  Disassembly Fix, Custom Dynamic Functors, and the SA equipment modules.

  IMPORTANT: v1.1.0 replaces v1.0.0. Disable or delete v1.0.0; do not run both.
  Restart the game completely after enabling v1.1.0. Existing saves are supported.

REQUIREMENTS
  - GAMMA's current item_parts.script / Part Disassembly Fix.
  - custom_functor_autoinject.script (Custom Dynamic Functors; included in GAMMA).

STARTUP CHECK
  The log should contain both lines:
    [SA-FABRIC-SALVAGE] v1.1.0 salvage patch installed
    [SA-FABRIC-SALVAGE] v1.1.0 patch recipe registered

TEST
  1. Carry any two faction patches and two separate sewing_thread items.
  2. Right-click one patch and run the conversion. Confirm all four inputs are
     consumed and one Basic Fabric appears.
  3. Dismantle several helmets, light/heavy outfits, backpacks, rigs, belts,
     and pouches at different conditions. Results are condition-scaled and random.

PERFORMANCE
  Negligible continuous cost. Salvage classification/rolls run only when an item
  is dismantled. The recipe scans the actor inventory only when its action runs.
