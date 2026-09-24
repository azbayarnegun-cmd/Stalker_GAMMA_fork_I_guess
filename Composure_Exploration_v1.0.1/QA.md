# QA

- Workbook balance values unchanged from v1.0.0.
- Entry grace changed from 30 seconds to a maximum of 5 seconds.
- No retained `CTime` userdata reference remains.
- Destination-loading time is discarded instead of reapplied.
- Arrival and clock-wait states explicitly clear the Exploration recovery lock.
- Level change, load, death, and option-change cleanup paths are registered.
- Transition scale remains 0.25 and transition exposure scale remains 1.00.
- The mod overwrites only its own v1.0.0 files.
