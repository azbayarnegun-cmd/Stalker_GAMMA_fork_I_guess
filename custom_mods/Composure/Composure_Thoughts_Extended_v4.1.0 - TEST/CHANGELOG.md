# Changelog

## 4.1.0

- Increased the default automatic-thought lifetime from 3.8 to 6 seconds and expanded the MCM range to 12 seconds.
- Smoothed normal thought presentation with a 0.7-second fade-in and 1.3-second fade-out.
- Changed Check Composure so releasing X after the 0.6-second activation no longer cancels the sequence.
- Slowed the accumulating presentation to 0.8 seconds per thought and the reflection presentation to 1.4 seconds per thought by default.
- Added MCM controls for check sequence speed and final-picture duration.
- The completed cause picture now remains for 5 seconds by default, fades for 1 second, and suppresses automatic/event thoughts for 3 seconds after completion.

## 4.0.2

- Fixed Consumables Balance `Drink`, `Food - MRE`, `Raw`, and `Cigar*` payload types being treated as unknown.
- Consumable event and Check Composure thoughts now identify the actual drink or food instead of using generic placeholder text.
- Needs diagnostics now log only severity changes instead of repeating every five seconds.

## 4.0.1

- Added hold-X Check Composure circular/reflection presentation.
- Added total-direction colors and source-specific current/past thoughts.
- Added 5-point minimum for remembered modifier sources.
- Reworked corpse and mutant awareness with safe typed access, distance probability, nearest-target selection, corpse FIFO, and mutant aftermath grace.
- Replaced false random physical flavor with guarded needs-aware polling.
- Removed Loot Thoughts and all inventory enumeration.
- Cached MCM reads and expanded non-mutating F6 diagnostics.
- Included Feedback v1.2.6 HUD compatibility override so tier color never flashes to instant-delta color.
