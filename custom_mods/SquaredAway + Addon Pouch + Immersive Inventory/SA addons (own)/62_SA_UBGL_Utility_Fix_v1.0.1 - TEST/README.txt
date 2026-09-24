SA UBGL & Utility Fix v1.0.1
============================

Late-load compatibility addon for the stable SA Inventory V1 baseline.

LOAD ORDER
  Install after Core, Rigs, Balance, QuickWheel, Immersive Access and the
  slot-55 external no-stack addon. This mod should occupy slot 62.

THIS MOD MUST WIN THESE FILES IN MO2
  gamedata/scripts/zzz_armor_mag_pouches.script
  gamedata/scripts/ammo_check_onekey_mcm.script
  gamedata/configs/items/settings/amp_layers_extra_08.ltx

FIXES
  - Resolves the active rifle correctly while its underbarrel launcher is in
    grenade mode.
  - Reads grenade_class and permits VOG-25/M203/M209 reloads only when a
    matching round is stored in a yellow reload pocket.
  - Covers the native reload key, One-Key Reload and the magazine mod's later
    grenade-mode pass-through.
  - Blocks Mouse 1's empty-launcher automatic reload when no matching round is
    in a yellow pocket, while still allowing an already-loaded grenade to fire.
  - Adds GAMMA's actual Multitool section, leatherman_tool, to the dedicated
    Utility Pouch whitelist.

TEST
  1. Put a VOG-25 or M203/M209 round only in general inventory or a Grenade
     Pouch. Switch to the empty underbarrel launcher and click Mouse 1. Its
     automatic reload must be refused.
  2. Move the matching round into a yellow magazine pocket and click Mouse 1.
     The automatic reload must work. Click again to fire the loaded grenade.
  3. Drag the Multitool into either Utility Pouch. It must fit.

EXPECTED LOG MARKERS
  UBGLUtilityFix-1.0.1
  [SA-UBGL] REFUSED Mouse 1 auto-reload ... no yellow pocket match
  [SA-UBGL] allowed Mouse 1 auto-reload ... yellow pocket match

Built from the stable Core v1.0.1 script baseline. Do not combine it with the
reverted experimental Core v1.0.2/v1.0.3 or older slot-62 reload fixes.
