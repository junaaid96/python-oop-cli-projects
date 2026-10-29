# 16 · FreelanceHub: Django + DRF (Capstone)

A small freelance marketplace: **clients** post projects, **freelancers** send proposals, the client accepts one. It has server-rendered HTML pages, a Django admin and a versioned REST API. Rebuilt from an earlier interview-prep project and trimmed to what teaches the most.

**Concepts:** custom user model, `TextChoices`, FK/M2M, indexes, DB constraints, custom QuerySets, N+1 fixes, migrations, FBV vs CBV, templates, `ModelForm`, auth mixins, admin, DRF serializers/viewsets/routers/`@action`, token auth, permissions, pagination, search/ordering, throttling, a service layer with `transaction.atomic` + `select_for_update`, 12-factor settings, pytest-django.

Read along: [Django track](../../docs/django/README.md).

```bash
cd projects/16_django_freelance_hub
uv run python manage.py migrate
uv run python manage.py createsuperuser      # then log in at /admin/ and add data
uv run python manage.py runserver            # http://127.0.0.1:8000/
uv run pytest                                # from the repo root
```

## API
| Method | URL | Who |
|---|---|---|
| GET | `/api/v1/projects/?search=django&ordering=-budget&status=open` | anyone |
| POST | `/api/v1/projects/` | clients |
| PATCH/DELETE | `/api/v1/projects/{id}/` | the owner |
| GET/POST | `/api/v1/projects/{id}/proposals/` | owner reads, freelancers post |
| POST | `/api/v1/proposals/{id}/accept/` | the owner |
| POST | `/api/v1/auth/token/` | `{"username", "password"}` → token |

```bash
TOKEN=$(curl -s -X POST localhost:8000/api/v1/auth/token/ -d username=ada -d password=... | jq -r .token)
curl -H "Authorization: Token $TOKEN" -X POST localhost:8000/api/v1/projects/ \
     -d title="Build a REST API" -d description="DRF" -d budget=500
```

## Layout
| File | Role |
|---|---|
| `hub_site/settings.py` | env-driven settings, DRF config, production hardening |
| `marketplace/models.py` | User, Skill, Project, Proposal, `ProjectQuerySet` |
| `marketplace/services.py` | business rules (submit, accept) |
| `marketplace/views.py`, `forms.py`, `templates/` | HTML pages |
| `marketplace/serializers.py`, `api_views.py`, `permissions.py`, `api_urls.py` | REST API |
| `tests/` | 17 pytest-django tests: ORM, query counts, services, pages, API |

## Exercises
1. Add `django-filter` with `budget_min`/`budget_max` filters.
2. Add a `Review` model (client rates freelancer after completion) with an API endpoint.
3. Send an email on acceptance with `transaction.on_commit` and Celery (see [guide 11](../../docs/django/11_caching_and_celery.md)).
4. Switch to PostgreSQL via `DATABASE_URL` and add a `CheckConstraint` on budget.
5. Generate OpenAPI docs with `drf-spectacular`.
