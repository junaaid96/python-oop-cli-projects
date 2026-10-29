# 03 · Migrations

Migrations are versioned, Python-described schema changes.

```bash
python manage.py makemigrations          # diff models -> new file in migrations/
python manage.py migrate                 # apply to the database
python manage.py showmigrations          # what's applied
python manage.py sqlmigrate marketplace 0001   # see the SQL
python manage.py migrate marketplace 0001      # roll back to 0001
python manage.py makemigrations --check --dry-run   # fail if models and migrations drift
```

## Rules
- Commit migration files; never edit an applied migration — add a new one.
- Set `AUTH_USER_MODEL` **before** the first migration.
- Data migrations use `RunPython` with `apps.get_model(...)` (the historical model, not an import):

```python
def fill_slugs(apps, schema_editor):
    Project = apps.get_model("marketplace", "Project")
    for p in Project.objects.filter(slug=""):
        p.slug = slugify(p.title)
        p.save(update_fields=["slug"])


operations = [migrations.RunPython(fill_slugs, migrations.RunPython.noop)]
```

## Zero-downtime changes (expand → migrate → contract)
1. Add the new column as nullable (old code still works).
2. Deploy code that writes both; backfill with a data migration.
3. Make it non-null / drop the old column in a later release.

Large tables: add indexes concurrently on PostgreSQL (`AddIndexConcurrently`, `atomic = False`).

## Exercises
1. Add `slug` to `Project` using the three steps above.
2. Squash migrations with `squashmigrations` and read the result.
