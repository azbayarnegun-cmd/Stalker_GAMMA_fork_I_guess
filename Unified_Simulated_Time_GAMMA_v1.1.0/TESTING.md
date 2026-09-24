# Live test plan

Use a disposable save.

1. Open MCM and confirm **Unified Simulated Time** appears.
2. Run `unified_time_skip_integrations.test_transition(15)` and confirm exactly
   15 game minutes pass, the overlay closes, and controls return.
3. Sleep for one hour and confirm the full simulation completes.
4. Use a normal level changer. The black travel overlay must finish before the
   autosave, disconnect and map loading begin.
5. After arriving, confirm an elapsed travel-time message appears.
6. Confirm the log reports the correct dynamic count: 30 minutes = 1 step,
   31-60 = 2, 61-120 = 4, and 121+ = 5.
7. Begin a transition near hostile actors. During the blackout there must be no
   hostile hit damage; protection must be gone after arrival.
8. Attempt travel during an active emission/psy-storm. The transition must be
   blocked with a message.
9. When an event is scheduled to begin during travel, confirm it does not start
   under the blackout or immediately on arrival. It may start after the
   two-real-minute grace period.
10. Test an underground transition; its route-table duration should be only a few
   minutes where defined.
11. Disable **Simulate level-transition travel** in MCM and confirm transitions
   return to ordinary GAMMA behavior with no added time.
12. Near a lit campfire, quicksave and confirm the blackout, 15-30 minute passage,
   save creation, restored audio, and restored controls.
13. Disable **Immersive campfire saving** and confirm saving follows normal
   GAMMA/YACS behavior.
14. Start Consumable Time-Skip and confirm another unified simulation cannot
    overlap it.
15. With Composure enabled, compare timed modifier durations before and after a
    15-minute test. Only simulated minutes should be processed.
16. Save, load, die, and change maps after testing; no black screen or altered
    ALife settings should remain.

With Debug Logging enabled, search the X-Ray log for:

```text
[SIM]
[unified_time_skip]
[immersive_campfire_compat]
SCRIPT ERROR
stack trace
```
