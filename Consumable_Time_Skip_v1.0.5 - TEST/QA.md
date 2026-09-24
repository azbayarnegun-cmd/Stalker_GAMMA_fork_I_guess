# QA status - v1.0.5

- Preserves the v1.0.1 safe creature classification fix for X-Ray userdata.
- Uses strict prepared-drink/tobacco IDs plus configuration-based strong-alcohol detection.
- Beer and ordinary cigarettes are explicitly excluded.
- Registered alcohol, prepared tea/coffee and slow tobacco are allowed during an
  active emission or psy-storm only inside GAMMA-registered event cover.
- The late callback bridge cannot authorize beer, ordinary cigarettes, ground
  coffee, exposed use, non-event use, or unregistered item categories.
- Busy and external simulated-time locks remain authoritative.
- Uses one cached pre-use safety scan per matching consumption.
- Advances world time and forces ALife once per simulation step.
- Does not emit undefined custom X-Ray callback names.
- Includes an optional, public-API-only Composure bridge; no Composure file is overwritten.
- Ages active Composure modifiers, caps and recovery locks by simulated elapsed time.
- Defers compatible slow-tobacco Composure recovery until waking.
- Reports actual elapsed minutes after completion or interruption.
- Static package/localization checks are included in `tests/static_qa.py`.
- Live engine validation remains required because item packs and callbacks vary by GAMMA installation.
