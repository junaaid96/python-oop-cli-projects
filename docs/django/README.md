# Django & DRF track

Concept guides for building web apps and APIs with **Django 6** and **Django REST Framework 3.16+**. Every guide points at real code in [projects/16_django_freelance_hub](../../projects/16_django_freelance_hub).

> Versions: Django 6.1 is the current release, 6.0 the previous one, and 5.2 the LTS (supported until April 2028). Check [the download page](https://www.djangoproject.com/download/) for dates. The ideas below also apply to 5.2.

| # | Guide | You'll learn |
|---|---|---|
| 01 | [Project structure](01_project_structure.md) | project vs app, settings, `manage.py`, request lifecycle |
| 02 | [Models & ORM](02_models_and_orm.md) | fields, relations, QuerySets, N+1, `select_related`/`prefetch_related` |
| 03 | [Migrations](03_migrations.md) | `makemigrations`, data migrations, zero-downtime rules |
| 04 | [Views: FBV vs CBV](04_views.md) | function views, generic views, mixins |
| 05 | [Templates](05_templates.md) | inheritance, tags, filters, auto-escaping |
| 06 | [Forms](06_forms.md) | `Form`, `ModelForm`, validation, CSRF |
| 07 | [Auth & permissions](07_auth_and_permissions.md) | custom user, login, groups, permissions |
| 08 | [Admin](08_admin.md) | `ModelAdmin`, inlines, performance |
| 09 | [Django REST Framework](09_drf.md) | serializers, viewsets, routers, auth, permissions, pagination, filtering, throttling, testing |
| 10 | [Settings & 12-factor config](10_settings_and_config.md) | env vars, split settings, secrets |
| 11 | [Caching & Celery](11_caching_and_celery.md) | cache framework, background jobs |
| 12 | [Security checklist](12_security_checklist.md) | `check --deploy`, HTTPS, CSRF, XSS, SQL injection |
| 13 | [Testing with pytest-django](13_testing.md) | fixtures, `django_db`, API tests, query counts |
| 14 | [Deployment](14_deployment.md) | gunicorn/uvicorn, static files, PostgreSQL, Docker |
| 15 | [Interview Q&A](15_interview_qa.md) | 40 common Django/DRF questions with short answers |

Suggested order: 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08, then build the project's HTML pages; 09 → 13 for the API; 10, 11, 12, 14 before you ship.
