# QA summary

- Runtime-only wrappers; no GAMMA base-script replacements.
- Old asynchronous global Travel/catch-all excluded.
- Level transition resumes only after simulated travel completes.
- Route-specific transition duration table preserved under a private filename.
- Simulated Time Skip and Consumable Time-Skip mutual-active guards present.
- Composure bridge is optional and guarded.
- Campfire save cleans UI, PPE and audio on completion/load/death/transition.
- Simulation core restores ALife and overlay state on abort.
- Level transitions use exactly 1/2/4/5 planned steps by duration band.
- Transition-only actor protection is refreshed and restored after arrival/error.
- Emission and psy-storm startup is held during travel while their countdowns
  age; due events receive a two-real-minute post-arrival grace period.
- Active emissions and psy-storms block level-transition simulation.
- MCM options and localization validated.
- Archive must install with `gamedata` at its root.
