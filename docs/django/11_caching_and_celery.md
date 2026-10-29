# 11 · Caching & background jobs

## Cache framework
Backends: local memory (dev), Redis (`django.core.cache.backends.redis.RedisCache`, built in since 4.0), Memcached, database.

```python
from django.core.cache import cache


def open_project_count() -> int:
    return cache.get_or_set("open_project_count", lambda: Project.objects.open().count(), 60)
```
- Per-view: `@cache_page(60)`; template fragments: `{% cache 60 sidebar %}`.
- Invalidate on writes (`cache.delete(key)` in a service or `post_save` signal) or use short TTLs.
- Never cache per-user data under a shared key.

## Celery basics
For slow or retryable work (email, PDFs, webhooks) do it **outside** the request.

```python
# hub_site/celery.py
app = Celery("hub_site")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


# marketplace/tasks.py
@shared_task(bind=True, autoretry_for=(ConnectionError,), retry_backoff=True, max_retries=5)
def notify_client(self, proposal_id: int) -> None:
    proposal = Proposal.objects.select_related("project__client").get(pk=proposal_id)
    send_mail(...)


# in the service, after the DB commit:
transaction.on_commit(lambda: notify_client.delay(proposal.pk))
```
Rules: pass IDs, not model objects; make tasks **idempotent** (safe to run twice); use `on_commit` so the worker never reads uncommitted data; periodic jobs with `celery beat`. Broker: Redis or RabbitMQ.

**Django 6.0 Tasks framework:** `django.tasks` adds a built-in `@task` decorator and `enqueue()` API with pluggable backends. Django ships only dev/testing backends, so production still needs a worker backend (e.g. `django-tasks`) — or Celery.

## Exercises
1. Cache the open-project count and clear it when a project is created.
2. Send a (console backend) email when a proposal is accepted, using `on_commit`.
