# Stable Manager Data Model Notes

## Invariant Data
A few models exist to hold invariant data, or to provide some identifiable form of continuity. These are
* Stable - Records the stable name, house and disciplines. 

## Temporal Relationships
The current state for each Broadcast Week will be captured in a collection of week-by-week snapshot tables built around StableWeek, these tables will include:
* PilotWeek to capture pilot experience / wounds / training over the course of the week.
* MechWeek to capture the current load-out of the mech (less likely to change, but the data volume is still minimal.
* LedgerItem captures stable expenses and details throughout the week (the Ledger model will be folded into StableWeek).
* Stable Action to capture actions taken by the stable during the week.

