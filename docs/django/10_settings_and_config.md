# 10 · Settings & 12-factor config

The [12-factor app](https://12factor.net/config) stores config in the **environment**, so the same code runs in dev, CI and production. See [`hub_site/settings.py`](../../projects/16_django_freelance_hub/hub_site/settings.py).

```python
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-insecure-key-change-me")
DEBUG = env_bool("DJANGO_DEBUG", True)
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost").split(",")
```

- Secrets (keys, DB passwords, API tokens) never go in git. Commit a `.env.example` with fake values; load a local `.env` with `django-environ` or your process manager.
- Split settings (`settings/base.py`, `development.py`, `production.py`) when environments diverge a lot; for small projects env vars + one file is simpler.
- Databases from one URL: `dj-database-url` → `DATABASES = {"default": dj_database_url.config()}`.
- `DEBUG=False` in production, always. Then `ALLOWED_HOSTS` and static files must be set up.
- Logging: configure `LOGGING` to stdout in containers (factor XI: logs are streams).

## Exercises
1. Read `DATABASE_URL` with `dj-database-url` and fall back to SQLite.
2. Add a `LOGGING` dict that logs SQL queries only when `DJANGO_LOG_SQL=1`.
