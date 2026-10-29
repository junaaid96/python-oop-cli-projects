# 04 · Ticket Booking (Beginner → Intermediate) · migrated

Originally [`junaaid96/ticket-booking-system`](https://github.com/junaaid96/ticket-booking-system) ("Star Cinema"). Its git history is preserved in this repo.

**Concepts:** composition, custom exception hierarchies, atomic operations, sets, type aliases (`type Seat = ...`).

```bash
uv run ticket-booking
```

## What changed from the original
- `Hall` no longer *inherits* from `Star_Cinema`; `Cinema` *has* halls (composition over inheritance).
- Each show owns its seat map (previously all shows in a hall shared seats).
- Bookings are all-or-nothing and raise typed exceptions instead of printing.
- Input/output are injected so the menu is unit-tested.

## Exercises
1. Add ticket prices per seat class (front rows cheaper) and print a receipt.
2. Add cancellation with a refund policy.
3. Save cinemas and bookings to JSON and reload them.
4. Suggest the best N adjacent free seats closest to the centre.
