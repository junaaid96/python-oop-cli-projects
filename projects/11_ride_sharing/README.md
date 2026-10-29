# 11 · Ride Sharing (Intermediate → Advanced) · migrated

Originally [`junaaid96/ride_sharing`](https://github.com/junaaid96/ride_sharing). Its git history is preserved in this repo.

**Concepts:** abstract `User` base class, inheritance, encapsulation, a state machine with an explicit transition table, matching with `min(key=...)`, fare tables, surge pricing.

```bash
uv run ride-sharing
```

Locations are simple grid points (`x,y` in km), so the project works anywhere.

## What changed from the original
- `ride_request` actually picks the nearest available driver of the requested vehicle type.
- `Ride.start_drive`/`end_ride` were empty stubs; rides now follow REQUESTED → STARTED → COMPLETED (or CANCELLED) and invalid moves raise errors.
- Fares, wallet payments, driver earnings and ratings were added.
- PEP 8 names: `RideSharing` instead of `Ride_Sharing`.

## Exercises
1. Add ride pooling: two riders heading the same way share a car and split the fare.
2. Replace the fare table with a `PricingStrategy` (see project 09).
3. Add a driver app menu (go online/offline, accept/decline requests).
4. Simulate a day: random riders and drivers on the grid, then print statistics.
