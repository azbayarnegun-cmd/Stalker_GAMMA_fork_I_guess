SA Inventory Framework Rotate Event Hotfix v1.0.0

For the combined SA_Inventory_Framework_Compatibility stack.

Fixes item rotation not responding after changing the rotate hotkey away from R.
The original SquaredAway/AMP rotation logic only polled key_state() during menu frames.
This patch keeps that behavior, but also catches the rotate key from on_key_press while an item is actually held/dragged.

Load after SA_Inventory_Framework_Compatibility_v1.0.0.
Contains only gamedata/scripts/zzz_armor_mag_pouches.script.
