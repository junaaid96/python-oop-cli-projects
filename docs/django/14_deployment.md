# 14 · Deployment

1. **App server**: `gunicorn hub_site.wsgi --workers 3` (sync) or `uvicorn hub_site.asgi:application` (async). `runserver` is for development only.
2. **Database**: PostgreSQL (`psycopg[binary]`). Run `migrate` as a release step, not at container start on every replica.
3. **Static files**: `collectstatic` into `STATIC_ROOT`, served by `whitenoise` or a CDN. User uploads go to object storage (S3 + `django-storages`).
4. **Config**: env vars (see [10](10_settings_and_config.md)), `DEBUG=0`, `check --deploy` clean.
5. **Reverse proxy / HTTPS**: a load balancer or nginx terminates TLS; set `SECURE_PROXY_SSL_HEADER` if it does.
6. **Workers**: Celery worker + beat as separate processes.
7. **Observability**: logs to stdout, error tracking (Sentry), a `/healthz` view.

## Minimal Dockerfile
Add `gunicorn` (and `psycopg[binary]`) to the `django` dependency group first.
```dockerfile
FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --group django
COPY projects/16_django_freelance_hub/ ./
ENV DJANGO_DEBUG=0 PYTHONUNBUFFERED=1
RUN uv run python manage.py collectstatic --noinput
USER nobody
CMD ["uv", "run", "gunicorn", "hub_site.wsgi", "--bind", "0.0.0.0:8000"]
```
Hosts that run this as-is: Fly.io, Render, Railway, any container platform or a VM.
