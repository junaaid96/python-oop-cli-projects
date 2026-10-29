# 01 · Project structure

```
16_django_freelance_hub/
├── manage.py            # CLI: runserver, migrate, shell, test, createsuperuser
├── hub_site/            # the *project*: settings, root URLs, WSGI/ASGI entry points
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py / asgi.py
└── marketplace/         # an *app*: one feature area, reusable
    ├── models.py  admin.py  forms.py  views.py  urls.py
    ├── serializers.py  api_views.py  api_urls.py  permissions.py
    ├── services.py      # business rules (not a Django convention, but a good one)
    ├── migrations/
    └── templates/marketplace/
```

- **Project** = configuration. **App** = a feature (models + views + URLs). A project has many apps; list them in `INSTALLED_APPS`.
- Create them with `django-admin startproject hub_site .` and `python manage.py startapp marketplace`.
- Namespace templates as `templates/<app>/...` so two apps can both have `list.html`.

## Request lifecycle
1. The WSGI/ASGI server calls Django with an `HttpRequest`.
2. **Middleware** runs top to bottom (security, sessions, CSRF, auth...).
3. The **URL resolver** matches `ROOT_URLCONF` patterns and picks a view.
4. The **view** talks to models/services and returns an `HttpResponse` (often via a template).
5. Middleware runs bottom to top on the response.

## Where logic goes
| Layer | Responsibility |
|---|---|
| models / QuerySets | data shape, simple derived data, reusable queries |
| services | business rules that touch several models, transactions |
| views / viewsets | HTTP: parse input, call services, choose response |
| templates / serializers | presentation |

"Fat models, thin views" is the classic advice; a small `services.py` keeps models from becoming god objects (see [SOLID](../14_solid_principles.md)).

## Exercises
1. Write a management command `list_routes` in `marketplace/management/commands/` that prints every URL pattern.
2. Add a second app, `reviews`, and wire its URLs under `/reviews/`.
