# 02 · Models & ORM

A model is a class; each attribute is a column. See [`marketplace/models.py`](../../projects/16_django_freelance_hub/marketplace/models.py).

```python
class Project(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    skills = models.ManyToManyField(Skill, blank=True, related_name="projects")
    budget = models.DecimalField(max_digits=10, decimal_places=2)  # never float for money
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["status", "-created_at"])]
```

## Relations
| Field | Meaning | Reverse access |
|---|---|---|
| `ForeignKey` | many-to-one | `user.projects.all()` |
| `OneToOneField` | one-to-one (profiles) | `user.profile` |
| `ManyToManyField` | many-to-many (join table) | `skill.projects.all()` |

`on_delete`: `CASCADE` (delete children), `PROTECT` (refuse), `SET_NULL` (needs `null=True`), `RESTRICT`.

## QuerySets are lazy
```python
qs = Project.objects.filter(status="OPEN")  # no SQL yet
qs = qs.exclude(budget__lt=100).order_by("-budget")
list(qs)  # SQL runs here
```
Lookups: `title__icontains`, `budget__gte`, `client__username`, `skills__name__in`. Use `Q` for OR (`Q(a) | Q(b)`) and `F` to reference columns (`F("bid") * 2`). Aggregate with `annotate(n=Count("proposals"))` and `aggregate(Avg("budget"))`.

## The N+1 problem
```python
for p in Project.objects.all():  # 1 query
    print(p.client.username)  # +1 query per project  -> N+1
```
| Fix | For | How |
|---|---|---|
| `select_related("client")` | FK / one-to-one | SQL JOIN, one query |
| `prefetch_related("skills")` | M2M / reverse FK | second query, joined in Python |
| `Prefetch("proposals", queryset=...)` | filtered prefetch | custom queryset |

The test `test_with_related_avoids_n_plus_one` proves that 5 projects + their clients + skills cost exactly **2** queries. Find N+1s with `django-debug-toolbar` or `CaptureQueriesContext`.

## Custom QuerySets
`ProjectQuerySet.open().with_related()` reads like English and is reused by HTML views, the API and admin. Prefer this to copy-pasted filters.

## Other must-knows
- `get_or_create`, `update_or_create`, `bulk_create`, `bulk_update`, `qs.update()` (one SQL `UPDATE`, skips `save()`/signals).
- `only()` / `defer()` / `values()` for fewer columns; `exists()` instead of `count() > 0`; `iterator()` for huge tables.
- `transaction.atomic` + `select_for_update()` for race-free changes (see `services.accept_proposal`).
- Constraints (`UniqueConstraint`, `CheckConstraint`) are enforced by the database: the last line of defence.

## Exercises
1. Add `Project.objects.cheaper_than(amount)` and test it.
2. Add a `CheckConstraint` so `budget > 0` and test that an invalid row raises `IntegrityError`.
