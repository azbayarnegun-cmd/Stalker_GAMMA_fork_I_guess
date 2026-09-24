# Composure Recovery v1.0.0

Optional safe-state recovery addon for S.T.A.L.K.E.R. Anomaly/GAMMA.

Requires **Composure Core v2.1.0** or another package exposing
`composure_framework` API 2.

## Default behavior

```text
Recovery rate:   +0.020 per second (+1.2/minute)
Recovery target: 65
Safety delay:    15 seconds
Pass Out:        blocked at 0
```

Recovery begins only when all of these are true:

- Core is available.
- The addon is enabled.
- The actor is alive.
- Current Composure is above 0 and below the configured target.
- No Framework recovery lock is active.
- No human or mutant within the configured distance is registered as actively fighting the actor.
- The actor has not recently taken damage.
- The actor has not recently fired a weapon.
- The safety delay has fully elapsed.

The addon adds one explicit slow-lane source:

```text
recovery.safe_passive
```

It never changes loss values, tiers, caps, health, stamina, hunger, thirst or
psy-health. Recovery is flat; there are no tier multipliers.

## Safety detection

Recovery uses GAMMA/Anomaly's established callbacks:

- `actor_on_before_hit`
- `actor_on_weapon_fired`
- `xr_combat_ignore.fighting_with_actor_npcs`

Combat and future gameplay modules should also use Framework recovery locks.
When a lock clears, Recovery waits through the full safety delay instead of
starting immediately.

## Target protection

Recovery reduces its final scheduled rate when close to the target. This keeps
the Framework's next slow tick from overshooting the configured target under
normal operation. Other explicit recovery sources remain independent and may
raise Composure above this target.

## MCM settings

- Enable Composure Recovery
- Recovery rate per second
- Recovery target
- Safety delay
- Respect recovery locks
- Block recovery at Pass Out
- Detect active combat
- Combat detection distance
- Combat inertia
- Reset delay when damaged
- Reset delay when firing
- Diagnostic key (F9)
- Debug logging

## Install

Install after Core:

```text
1. Composure Core v2.1.0
2. Composure Recovery v1.0.0
3. Other gameplay and presentation modules
```

Do not use Composure Main v1 alongside this addon. Main contains the retired
passive-recovery system and would create a second recovery source.

## Public inspection API

```lua
composure_recovery.get_version()
composure_recovery.is_recovering()
composure_recovery.get_diagnostics()
```
