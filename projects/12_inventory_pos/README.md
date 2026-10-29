# 12 · Inventory & Point of Sale (Advanced)

A cashier console with stock tracking, stackable discount rules, tax and receipts.

**Concepts:** Strategy + Composite patterns (`Discount`, `BestOf`), callbacks/closures as observers, `csv`, `Decimal` rounding modes, atomic checkout.

```bash
uv run inventory-pos
```

## Exercises
1. Add a `Coupon` discount that can be used only once.
2. Add returns/refunds that restock items.
3. Store sales in SQLite and print an end-of-day Z-report.
4. Add a barcode scanner simulation (read SKUs from a text file).
