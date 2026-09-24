# Test checklist

1. Enable the tester in MCM and press F10 outdoors. Confirm fade, stepped clock advance, and return.
2. Repeat with a hostile human inside 40 m and mutant inside 20 m; confirm hard-cut interruption.
3. Test in fully enclosed surge-safe cover; confirm the protected skip completes.
4. Try a qualifying item while detected/in recent combat; confirm use is blocked before consumption.
5. Confirm strong alcohol advances 120 minutes, while beer remains instant.
6. Confirm `tea`, `coffee`, and `brewed_coffee` advance 30 minutes; `ground_coffee` remains instant.
7. Confirm `hand_rolling_tobacco` and `cigar` advance 15 minutes.
8. Confirm cigarettes and `cigar1`/`cigar2`/`cigar3` remain instant.
9. With Composure active, add a temporary modifier, run a five-minute protected test, and confirm its value and lifetime advance.
10. Interrupt an outdoor skip and confirm Composure processes only elapsed completed steps.
11. Save/load and change levels after completion and interruption; confirm input and HUD remain normal.
12. During an active emission, enter GAMMA-recognized event cover and test strong
    alcohol, prepared tea, prepared coffee, Cuban cigar and hand-rolling tobacco.
    Confirm each can be used and starts its configured protected skip.
13. Repeat step 12 during an active psy-storm.
14. During either event, leave registered cover and try the same items. Confirm
    the event restriction remains and no CTS skip starts.
15. Confirm beer, ground coffee and ordinary cigarettes remain excluded both
    inside and outside event shelter.

Useful console calls:

```lua
consumable_time_skip.test(5, false)
consumable_time_skip.test(5, true)
consumable_time_skip.test_threat_scan()
consumable_time_skip.test_enclosure()
consumable_time_skip.get_registered_duration("beer")
consumable_time_skip.get_registered_duration("vodka")
```

Enable debug logging and search `xray_*.log` for `[CTS]`. Start/queue lines include the exact item section, duration and precheck state; block/interruption lines include the reason.
