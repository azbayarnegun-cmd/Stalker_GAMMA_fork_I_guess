# 50 SA Immersive Inventory Access v1.0.11 C5 1.5s

Final self-contained animation-path test build.

Timing update: the inventory window cannot open until at least 1.5 seconds of
the backpack opening animation have played. Slower weight/config-driven timing
is preserved. The closing animation uses the same clamped speed.

Hold Tab calls the live function confirmed by the v1.0.8 diagnostic:
`immersive_backpacks_fdda.open_backpack(equipped_backpack, equipped_backpack:id())`

The bundled FDDA path now defaults its animation on when the missing Immersive
Backpacks MCM module is unavailable and opens full inventory through an internal
bridge when the missing binder is unavailable. It hides/restores only the weapon
HUD during the session and never changes active_slot.

Expected markers:
- `[SA-INV-ACCESS] C5: calling immersive_backpacks_fdda.open_backpack ...`
- `[SA-INV-ACCESS] C5: weapon HUD hidden`
- `[SA-INV-ACCESS] C5: opening animation started speed=... window_delay=1.50s`
- `[SA-INV-ACCESS] C5: full inventory opened through internal bridge`
- `[SA-INV-ACCESS] C5: closing animation started`
- `[SA-INV-ACCESS] C5: weapon HUD restored`

Disable older experimental `50` builds and test only this v1.0.11 C5 build.
