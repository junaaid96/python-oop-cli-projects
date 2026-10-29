# 08 · Admin

The admin is a free back-office generated from models. See [`marketplace/admin.py`](../../projects/16_django_freelance_hub/marketplace/admin.py).

```python
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin[Project]):
    list_display = ("title", "client", "budget", "status")
    list_filter = ("status", "skills")
    search_fields = ("title", "description")
    list_select_related = ("client",)  # avoid N+1 on the list page
    inlines = (ProposalInline,)  # edit children on the parent page
```

Useful options: `readonly_fields`, `autocomplete_fields` (for big FK lists), `raw_id_fields`, `date_hierarchy`, `actions` (bulk operations), `get_queryset` overrides.

Rules:
- The admin is for trusted staff, not end users.
- Move it off `/admin/` in production, enforce strong passwords/2FA, and keep `is_staff` rare.
- Extend `UserAdmin` for a custom user so password hashing keeps working.

Try it: `uv run python projects/16_django_freelance_hub/manage.py migrate && ... createsuperuser && ... runserver`, then open `/admin/`.

## Exercises
1. Add a "Mark as completed" admin action.
2. Show `proposal_count` in `list_display` using an annotated `get_queryset`.
