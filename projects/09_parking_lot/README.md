# 09 · Parking Lot (Intermediate)

A multi-level lot with spot sizes, tickets and swappable pricing.

**Concepts:** `IntEnum`, inheritance with frozen dataclasses, Strategy pattern (`PricingStrategy`), a greedy allocation rule, time arithmetic.

```bash
uv run parking-lot
uv run parking-lot --pricing daily
```

## Exercises
1. Add an `EVSpot` with charging fees (a decorator around the pricing strategy).
2. Add a display board per level using the Observer pattern.
3. Add monthly passes (a pricing strategy that returns 0 for pass holders).
4. Persist active tickets so a restart doesn't lose cars.
