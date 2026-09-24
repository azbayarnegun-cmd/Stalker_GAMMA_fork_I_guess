# Static QA

The included checks validate:

- MO2 package layout and XML.
- Lua parsing with the available Lua interpreter.
- Core API 2 dependency and `source_type = combat` metadata.
- Human-only stalker filtering for hits and bullet sources.
- Three canonical phases and default rates.
- 30/70 event splitting and both rolling instant caps.
- Deferred queue persistence and the combined continuous cap.
- Recovery lock, event publication, actual-loss accounting and bounded rebound.
- F6 diagnostics and guarded test actions.
- Detailed on-screen test status and public test-state fields for Feedback HUD.
- Safe `string.format` diagnostics compatible with GAMMA's one-string `printf` behavior.
- GAMMA callback registration for NPC targeting, hits and bullets.
- No Lua features newer than Lua 5.1.

Run:

```text
python tests/static_qa.py
python tests/model_qa.py
```
