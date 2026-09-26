Natural Recovery v1.0.0 (for S.T.A.L.K.E.R. GAMMA)
=================================================

Slowly restores OVERALL health (the red HP bar) depending on how healthy your
limbs are in GAMMA's body health system.

HOW IT WORKS
  Limbs fully healed (all at max)                -> +10% HP per in-game hour
  Limbs damaged (>= 60% of limb points, head and
  torso >= 6 of 11, no broken limb)              -> +3% HP per in-game hour
  Badly hurt (anything worse)                    -> no recovery

  HP ceiling: natural recovery stops at your limb condition.
  Example: limbs at 75% -> HP recovers up to 75%. Use meds to go higher.

  Blocked while: bleeding, hit in the last 60 s, satiety < 0.15,
  thirst at orange or worse, radiation > 0.10.

  Uses in-game time. Awake at GAMMA's default time speed, +10%/h is about
  +1.7% per real minute. While sleeping, each hour first heals 1 limb point
  (GAMMA: head -> torso -> right arm -> left arm -> right leg -> left leg),
  then the matching recovery rate is applied.

SETTINGS
  MCM -> Natural Recovery: rates, thresholds, ceiling, blockers, sleep.

REQUIRES
  GAMMA (G.A.M.M.A. Medications Balance provides zzz_player_injuries), MCM.
  Works with Unified Simulated Time (sleep still triggers the sleep event).

INSTALL
  Install as a new mod in Mod Organizer 2. Any position works: it adds new
  files only (natural_recovery*.script, ui_st_natural_recovery.xml).
  Safe to add or remove mid-save.
