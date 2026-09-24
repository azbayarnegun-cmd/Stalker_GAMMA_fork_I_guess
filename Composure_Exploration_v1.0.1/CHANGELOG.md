# Changelog

## v1.0.1

- Fixed Composure freezing after a simulated level transition.
- Replaced mutable game-time object tracking with a scalar timestamp.
- Reduced arrival grace from 30 seconds to 5 seconds.
- Arrival requires two valid game-clock samples before Exploration resumes.
- Exploration no longer holds Recovery locked during destination initialization.
- Added stale-clock/lock watchdog and lifecycle diagnostics.
- Prevented destination loading from duplicating transition exposure.
- Preserved all v1.0.0 workbook balance values.
